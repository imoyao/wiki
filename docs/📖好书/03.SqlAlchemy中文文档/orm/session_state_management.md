---
title: 状态管理
date: 2021-02-20 22:41:47
permalink: /sqlalchemy/orm/session_state_management/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
状态管理[¶](#state-management "Permalink to this headline")
===========================================================

Quickie 介绍对象状态[¶](#quickie-intro-to-object-states "Permalink to this headline")
------------------------------------------------------------------------------------

了解实例在会话中可以具有的状态很有帮助：

-   **Transient** -
    一个不在会话中的实例，不会保存到数据库中；即它没有数据库身份。这种对象与 ORM 唯一的关系是它的类有一个与它关联的`mapper()`。

-   **Pending** - when you [`add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")
    a transient instance, it becomes pending.
    它仍然没有被实际刷新到数据库，但它会在下一次刷新时发生。

-   **持久** -
    存在于会话中且在数据库中具有记录的实例。通过刷新来获得持久性实例，以便挂起的实例变为持久性，或通过查询数据库查找现有实例（或将其他会话的持久实例移动到本地会话中）。

-   **已删除** -
    在刷新中已删除的实例，但事务尚未完成。处于这种状态的对象本质上与“挂起”状态相反；当会话的事务提交时，对象将移至分离状态。或者，当会话的事务回滚时，被删除的对象将*返回*为持久状态。

    版本 1.1 中已更改：“已删除”状态是与“持久”状态不同的新添加的会话对象状态。

-   **Detached** -
    与数据库中的记录相对应或先前对应的实例，但当前不在任何会话中。分离的对象将包含数据库标识标记，但是因为它与会话没有关联，所以不知道该数据库标识是否实际存在于目标数据库中。分离的对象可以正常使用，除非它们无法加载先前标记为“已过期”的未加载属性或属性。

要深入了解所有可能的状态转换，请参阅描述每个转换的[Object Lifecycle
Events](session_events.html#session-lifecycle-events)部分，以及如何以编程方式跟踪每个转换。

### 获取对象的当前状态[¶](#getting-the-current-state-of-an-object "Permalink to this headline")

任何映射对象的实际状态都可以在任何时候使用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")系统查看：

    >>> from sqlalchemy import inspectplain
    >>> insp = inspect(my_object)
    >>> insp.persistent
    True

也可以看看

[`InstanceState.transient`](internals.html#sqlalchemy.orm.state.InstanceState.transient "sqlalchemy.orm.state.InstanceState.transient")

[`InstanceState.pending`](internals.html#sqlalchemy.orm.state.InstanceState.pending "sqlalchemy.orm.state.InstanceState.pending")

[`InstanceState.persistent`](internals.html#sqlalchemy.orm.state.InstanceState.persistent "sqlalchemy.orm.state.InstanceState.persistent")

[`InstanceState.deleted`](internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")

[`InstanceState.detached`](internals.html#sqlalchemy.orm.state.InstanceState.detached "sqlalchemy.orm.state.InstanceState.detached")

会话属性[¶](#session-attributes "Permalink to this headline")
-------------------------------------------------------------

[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本身的行为有点像集合式集合。所有存在的项目都可以使用迭代器接口访问：

    for obj in session:plainplain
        print(obj)

可以使用常规的“包含”语义测试存在性：

    if obj in session:plain
        print("Object is present")

会话还跟踪所有新创建的（即挂起的）对象，自上次加载或保存之后发生更改的所有对象（即“脏”）以及标记为已删除的所有对象：

    # pending objects recently added to the Sessionplainplain
    session.new

    # persistent objects which currently have changes detected
    # (this collection is now created on the fly each time the property is called)
    session.dirty

    # persistent objects that have been marked as deleted via session.delete(obj)
    session.deleted

    # dictionary of all persistent objects, keyed on their
    # identity key
    session.identity_map

(Documentation: [`Session.new`](session_api.html#sqlalchemy.orm.session.Session.new "sqlalchemy.orm.session.Session.new"),
[`Session.dirty`](session_api.html#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty"),
[`Session.deleted`](session_api.html#sqlalchemy.orm.session.Session.deleted "sqlalchemy.orm.session.Session.deleted"),
[`Session.identity_map`](session_api.html#sqlalchemy.orm.session.Session.identity_map "sqlalchemy.orm.session.Session.identity_map")).

会话参照行为[¶](#session-referencing-behavior "Permalink to this headline")
---------------------------------------------------------------------------

会话中的对象是*弱引用的*。这意味着，当它们在外部应用程序中取消引用时，它们也会从[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中超出范围，并且会受到 Python 解释器的垃圾回收。例外情况包括挂起的对象，标记为已删除的对象或挂起更改的持久对象。完全刷新后，这些集合全部为空，并且所有对象都被弱引用。

要使[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中的对象保持强引用状态，通常只需要一个简单的方法。外部管理的强引用行为的示例包括将对象加载到与其主键相关的本地字典中，或者将对象加载到它们需要保持引用的时间范围内的列表或集合中。如果需要，可以将这些集合与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联，方法是将它们放入[`Session.info`](session_api.html#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")字典中。

基于事件的方法也是可行的。当所有对象保持在[persistent](glossary.html#term-persistent)状态时，为所有对象提供“强引用”行为的简单配方如下所示：

    from sqlalchemy import eventplainplainplain

    def strong_reference_session(session):
        @event.listens_for(session, "pending_to_persistent")
        @event.listens_for(session, "deleted_to_persistent")
        @event.listens_for(session, "detached_to_persistent")
        @event.listens_for(session, "loaded_as_persistent")
        def strong_ref_object(sess, instance):
            if 'refs' not in sess.info:
                sess.info['refs'] = refs = set()
            else:
                refs = sess.info['refs']

            refs.add(instance)


        @event.listens_for(session, "persistent_to_detached")
        @event.listens_for(session, "persistent_to_deleted")
        @event.listens_for(session, "persistent_to_transient")
        def deref_object(sess, instance):
            sess.info['refs'].discard(instance)

Above, we intercept the [`SessionEvents.pending_to_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.pending_to_persistent "sqlalchemy.orm.events.SessionEvents.pending_to_persistent"),
[`SessionEvents.detached_to_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.detached_to_persistent "sqlalchemy.orm.events.SessionEvents.detached_to_persistent"),
[`SessionEvents.deleted_to_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.deleted_to_persistent "sqlalchemy.orm.events.SessionEvents.deleted_to_persistent")
and [`SessionEvents.loaded_as_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.loaded_as_persistent "sqlalchemy.orm.events.SessionEvents.loaded_as_persistent")
event hooks in order to intercept objects as they enter the
[persistent](glossary.html#term-persistent) transition, and the
[`SessionEvents.persistent_to_detached()`](events.html#sqlalchemy.orm.events.SessionEvents.persistent_to_detached "sqlalchemy.orm.events.SessionEvents.persistent_to_detached")
and [`SessionEvents.persistent_to_deleted()`](events.html#sqlalchemy.orm.events.SessionEvents.persistent_to_deleted "sqlalchemy.orm.events.SessionEvents.persistent_to_deleted")
hooks to intercept objects as they leave the persistent state.

对于任何[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以调用上面的函数，以便在每个会话[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

    from sqlalchemy.orm import Session

    my_session = Session()
    strong_reference_session(my_session)

它也可能被任何[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")调用：

    from sqlalchemy.orm import sessionmaker

    maker = sessionmaker()
    strong_reference_session(maker)

合并[¶ T0\>](#merging "Permalink to this headline")
---------------------------------------------------

[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")从外部对象将状态转换为会话中新的或已存在的实例。它还将传入的数据与数据库状态进行协调，产生将用于下一次刷新的历史流，或者可以使得产生状态的简单“转移”而不产生更改历史或访问数据库。用法如下：

    merged_object = session.merge(existing_object)plainplain

给定一个实例时，它遵循以下步骤：

-   它检查实例的主键。如果存在，它会尝试在本地标识映射中找到该实例。如果`load=True`标志处于默认状态，它还会检查数据库中是否存在本地主键。

-   如果给定实例没有主键，或者在给定主键时没有找到实例，则创建一个新实例。

-   然后将给定实例的状态复制到位于/新创建的实例上。对于源实例上存在的属性，该值将传输到目标实例。对于源上不存在的映射属性，属性在目标实例上过期，放弃其现有值。

    如果`load=True`标志保留为其默认值，则此复制过程将发出事件并为源对象上存在的每个属性加载目标对象的卸载集合，以便可以调整传入状态数据库中存在什么。如果`load`作为`False`传递，则传入的数据将直接“加盖”而不会产生任何历史记录。

-   如`merge`级联所示（请参阅[Cascades](cascades.html#unitofwork-cascades)），操作级联到相关的对象和集合。

-   新实例返回。

使用[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")时，给定的“源”实例不会被修改，也不会与目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联，并且仍然可以与任何数量的其他[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象。[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
is useful for taking the state of any kind of object structure without
regard for its origins or current session associations and copying its
state into a new session. 这里有一些例子：

-   从文件读取对象结构并希望将其保存到数据库的应用程序可能解析文件，构建结构，然后使用[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")将其保存到数据库中，以确保该文件中的数据用于形成结构中每个元素的主键。之后，当文件发生变化时，可以重新运行相同的进程，产生稍微不同的对象结构，然后再次`merged`，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")将会自动更新数据库以反映这些更改，使用主键从数据库加载每个对象，然后使用给定的新状态更新其状态。

-   应用程序正在将对象存储在内存缓存中，并同时被许多[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象共享。[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
    is used each time an object is retrieved from the cache to create a
    local copy of it in each [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    which requests it.
    缓存的对象保持分离状态；只有它的状态被移动到本身对个人[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象本地的副本中。

    在缓存用例中，通常使用`load=False`标志来消除协调对象状态与数据库的开销。还有一个名为[`merge_result()`](query.html#sqlalchemy.orm.query.Query.merge_result "sqlalchemy.orm.query.Query.merge_result")的[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")的“批量”版本，设计用于与缓存扩展的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象一起使用
    - 请参阅section [Dogpile Caching](examples.html#examples-caching)。

-   应用程序想要将一系列对象的状态转换为由工作线程或其他并发系统维护的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
    makes a copy of each object to be placed into this new
    [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session").
    在操作结束时，父线程/进程维护它所启动的对象，并且线程/工作者可以继续处理这些对象的本地副本。

    在“线程/进程之间的传输”用例中，应用程序可能也希望使用`load=False`标志以避免数据传输时出现开销和冗余 SQL 查询。

### 合并提示[¶](#merge-tips "Permalink to this headline")

[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
is an extremely useful method for many purposes.
然而，它处理瞬态/分离对象与持久对象之间错综复杂的边界，以及状态的自动传输。可以在这里呈现的各种各样的场景通常需要对对象状态更谨慎的方法。合并的常见问题通常涉及有关传递给[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")的对象的一些意想不到的状态。

让我们使用 User 和 Address 对象的规范例子：

    class User(Base):plain
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)
        addresses = relationship("Address", backref="user")

    class Address(Base):
        __tablename__ = 'address'

        id = Column(Integer, primary_key=True)
        email_address = Column(String(50), nullable=False)
        user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

假设`User`对象具有一个`Address`，它已经是持久的：

    >>> u1 = User(name='ed', addresses=[Address(email_address='ed@ed.com')])plain
    >>> session.add(u1)
    >>> session.commit()

我们现在创建`a1`，一个会话之外的对象，我们要在现有的`Address`之上合并：

    >>> existing_a1 = u1.addresses[0]plain
    >>> a1 = Address(id=existing_a1.id)

如果我们这样说，会发生一个惊喜：

    >>> a1.user = u1
    >>> a1 = session.merge(a1)
    >>> session.commit()
    sqlalchemy.orm.exc.FlushError: New instance <Address at 0x1298f50>
    with identity key (<class '__main__.Address'>, (1,)) conflicts with
    persistent instance <Address at 0x12a25d0>

这是为什么 ？我们没有注意到我们的瀑布。将`a1.user`赋值给级联到`User.addresses`的 backref 的持久对象，并使我们的`a1`对象处于挂起状态，就好像我们已经添加它。现在我们在会话中有*两个*
`Address`对象：

    >>> a1 = Address()plainplain
    >>> a1.user = u1
    >>> a1 in session
    True
    >>> existing_a1 in session
    True
    >>> a1 is existing_a1
    False

上面，我们的`a1`在会话中已经挂起。随后的[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")操作本质上什么都不做。Cascade
can be configured via the [`cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")
option on [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
although in this case it would mean removing the `save-update` cascade from the `User.addresses`
relationship - and usually, that behavior is extremely convenient. The
solution here would usually be to not assign `a1.user` to an object already persistent in the target session.

[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的`cascade_backrefs=False`选项也将阻止`Address`通过`a1添加到会话中.user = u1`分配。

关于级联操作的更多细节在[Cascades](cascades.html#unitofwork-cascades)。

意外状态的另一个例子：

    >>> a1 = Address(id=existing_a1.id, user_id=u1.id)
    >>> assert a1.user is None
    >>> True
    >>> a1 = session.merge(a1)
    >>> session.commit()
    sqlalchemy.exc.IntegrityError: (IntegrityError) address.user_id
    may not be NULL

在这里，我们访问了 a1.user，它返回了默认值`None`，它作为这个访问的结果放在我们对象的`__dict__`中`a1`通常，此操作不会创建更改事件，因此在刷新过程中`user_id`属性优先。但是当我们将`Address`对象合并到会话中时，操作等同于：

    >>> existing_a1.id = existing_a1.idplain
    >>> existing_a1.user_id = u1.id
    >>> existing_a1.user = None

Where above, both `user_id` and `user` are assigned to, and change events are emitted for both.
`user`关联优先，而 None 应用于`user_id`，导致失败。

大多数[`merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")问题可以通过首先检查来检查
- 会话中的对象是否过早？

    >>> a1 = Address(id=existing_a1, user_id=user.id)
    >>> assert a1 not in session
    >>> a1 = session.merge(a1)

或者在对象上有我们不想要的状态？检查`__dict__`是检查以下内容的快速方法：

    >>> a1 = Address(id=existing_a1, user_id=user.id)plainplainplain
    >>> a1.user
    >>> a1.__dict__
    {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x1298d10>,
        'user_id': 1,
        'id': 1,
        'user': None}
    >>> # we don't want user=None merged, remove it
    >>> del a1.user
    >>> a1 = session.merge(a1)
    >>> # success
    >>> session.commit()

清除日期[¶ T0\>](#expunging "Permalink to this headline")
---------------------------------------------------------

清除从会话中删除对象，将持久实例发送到分离状态，并将待处理实例发送到瞬态：

    session.expunge(obj1)

要删除所有项目，请调用[`expunge_all()`](session_api.html#sqlalchemy.orm.session.Session.expunge_all "sqlalchemy.orm.session.Session.expunge_all")（此方法以前称为`clear()`）。

刷新/过期[¶](#refreshing-expiring "Permalink to this headline")
---------------------------------------------------------------

[Expiring](glossary.html#term-expiring)意味着保存在一系列对象属性中的数据库持久数据被删除，这样当下次访问这些属性时，就会发出一个 SQL 查询，它将刷新数据库中的数据。

当我们谈论数据到期时，我们通常会谈论处于[persistent](glossary.html#term-persistent)状态的对象。例如，如果我们加载一个对象如下：

    user = session.query(User).filter_by(name='user1').first()plainplainplain

上面的`User`对象是持久的，并且有一系列属性存在；如果我们要查看它的`__dict__`，我们会看到加载状态：

    >>> user.__dict__plain
    {
      'id': 1, 'name': u'user1',
      '_sa_instance_state': <...>,
    }

其中`id`和`name`指数据库中的那些列。`_sa_instance_state`是 SQLAlchemy 内部使用的非数据库持久化值（它指向实例的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")）。虽然与本节不直接相关，但如果我们想要了解它，我们应该使用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数来访问它）。

此时，我们的`User`对象中的状态与加载的数据库行的状态匹配。但是在使用诸如[`Session.expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")之类的方法使对象过期时，我们看到状态被删除：

    >>> session.expire(user)
    >>> user.__dict__
    {'_sa_instance_state': <...>}

我们看到，虽然内部“状态”仍然存在，但与`id`和`name`列对应的值已消失。如果我们要访问这些列中的一个并且正在观察 SQL，我们会看到：

    >>> print(user.name)plainplain
    SELECT user.id AS user_id, user.name AS user_name
    FROM user
    WHERE user.id = ?
    (1,)
    user1

以上，在访问过期属性`user.name`时，ORM 通过发出用户行的 SELECT 来启动[lazy
load](glossary.html#term-lazy-load)以从数据库中检索最新状态这个用户提到的。之后，再次填充`__dict__`：

    >>> user.__dict__plainplain
    {
      'id': 1, 'name': u'user1',
      '_sa_instance_state': <...>,
    }

注意

当我们在`__dict__`里面查看时，为了看到 SQLAlchemy 用对象属性做些什么，我们**不应该修改`__dict__`的内容。直接，至少就 SQLAlchemy
ORM 所维护的属性而言（SQLA 领域之外的其他属性都可以）。**这是因为 SQLAlchemy 使用[descriptors](glossary.html#term-descriptors)来跟踪我们对对象所做的更改，并且当我们直接修改`__dict__`时，ORM 将无法跟踪我们改变了一些。

[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")和[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")的另一个关键行为是丢弃对象上所有未刷新的更改。也就是说，如果我们要修改`User`上的属性：

    >>> user.name = 'user2'plainplainplain

但是我们在没有先调用[`flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")的情况下调用[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")，我们的`'user2'`的未决值将被丢弃：

    >>> session.expire(user)
    >>> user.name
    'user1'

可以使用[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")方法将实例的所有 ORM 映射属性标记为“过期”：

    # expire all ORM-mapped attributes on obj1plain
    session.expire(obj1)

它也可以传递一个字符串属性名称列表，引用特定的属性来标记为过期：

    # expire only attributes obj1.attr1, obj1.attr2plain
    session.expire(obj1, ['attr1', 'attr2'])

[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")方法有一个类似的接口，但不是过期，而是立即为对象的行发出立即的 SELECT：

    # reload all attributes on obj1plain
    session.refresh(obj1)

[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")也接受字符串属性名称列表，但与[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")不同，期望至少有一个名称是列映射属性的名称：

    # reload obj1.attr1, obj1.attr2plain
    session.refresh(obj1, ['attr1', 'attr2'])

[`Session.expire_all()`](session_api.html#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")方法允许我们实时调用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中包含的所有对象的[`Session.expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")

    session.expire_all()plain

### 什么实际上加载[¶](#what-actually-loads "Permalink to this headline")

标有[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")或加载[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")的对象发出的 SELECT 语句根据以下几个因素而变化：

-   过期属性的负载仅由**列映射属性**触发。虽然任何类型的属性都可以标记为过期，包括[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")映​​射属性，但访问过期的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")属性将仅为该属性发出加载，使用标准的面向关系的延迟加载。面向列的属性（即使过期）不会作为此操作的一部分加载，而是在访问任何面向列的属性时加载。
-   [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")映​​射的属性不会加载，以响应正在访问的到期的基于列的属性。
-   关于关系，对于未经列映射的属性，[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")比[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")更具限制性。调用[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")并传递仅包含关系映射属性的名称列表实际上会引发错误。无论如何，非急切加载[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")属性将不会包含在任何刷新操作中。
-   通过[`lazy`](relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship")参数配置为“急切加载”的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")属性将在[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")的情况下加载，如果没有属性名称被指定，或者如果他们的名字被包含在要被刷新的属性列表中。
-   在过期属性加载期间或刷新期间，配置为[`deferred()`](loading_columns.html#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")的属性通常不会加载。直接访问时，[`deferred()`](loading_columns.html#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")的卸载属性自己加载，或者如果访问该组中的未加载属性的延迟属性“组”的一部分。
-   对于在访问时加载的过期属性，联合继承表映射将发出一个SELECT，通常只包含那些存在未加载属性的表。此处的操作足够复杂，只能加载父表或子表，例如，如果最初过期的列的子集仅包含这些表中的一个或另一个。
-   当在已连接的继承表映射上使用[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")时，发出的 SELECT 类似于在目标对象的类上使用[`Session.query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")时的 SELECT。这通常是所有那些设置为映射一部分的表。

### 何时过期或刷新[¶](#when-to-expire-or-refresh "Permalink to this headline")

只要会话引用的事务结束，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")就会自动使用到期功能。这意味着，无论何时[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")或[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")被调用，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中的所有对象都会过期，到[`Session.expire_all()`](session_api.html#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")方法。其基本原理是事务的结束是一个划分点，在这个点上没有更多的上下文可用来了解数据库的当前状态，因为任何数量的其他事务都可能影响它。只有当新事务开始时，我们才能再次访问数据库的当前状态，此时可能发生了任何数量的更改。

事务隔离

当然，大多数数据库能够一次处理多个事务，甚至包含相同的数据行。当关系数据库处理涉及相同表或行的多个事务时，这是数据库的[isolation](glossary.html#term-isolation)方面起作用的时候。不同数据库的隔离行为差异很大，甚至可以将单个数据库配置为以不同方式运行（通过所谓的隔离级别设置）。从这个意义上说，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")不能完全预测何时第二次发出的相同 SELECT 语句肯定会返回我们已有的数据，或者将返回新数据。因此，作为最佳猜测，它假设在事务范围内，除非知道已经发出 SQL 表达式来修改特定行，否则不需要刷新行，除非明确告知这样做。

当需要强制对象从数据库中重新加载其数据时，会使用[`Session.expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")和[`Session.refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")方法，那些知道当前数据状态可能已过时的情况。其原因可能包括：

-   some SQL has been emitted within the transaction outside of the
    scope of the ORM’s object handling, such as if a
    [`Table.update()`](core_metadata.html#sqlalchemy.schema.Table.update "sqlalchemy.schema.Table.update")
    construct were emitted using the [`Session.execute()`](session_api.html#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
    method;
-   如果应用程序试图获取已知在并发事务中修改的数据，并且还知道隔离规则实际上允许此数据可见。

第二个要点有一个重要的警告，即“还知道隔离规则实际上允许这些数据可见”。这意味着不能认为发生在另一个数据库连接上的 UPDATE 在本地仍然可见；在很多情况下，它不会。这就是为什么如果希望使用[`expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")或[`refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")来查看正在进行的事务之间的数据，理解隔离行为是非常重要的。

也可以看看

[`Session.expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")

[`Session.expire_all()`](session_api.html#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")

[`Session.refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")

[isolation](glossary.html#term-isolation) - glossary explanation of
isolation which includes links to Wikipedia.

[The SQLAlchemy Session
In-Depth](http://techspot.zzzeek.org/2012/11/14/pycon-canada-the-sqlalchemy-session-in-depth/)
- a video + slides with an in-depth discussion of the object lifecycle
including the role of data expiration.
