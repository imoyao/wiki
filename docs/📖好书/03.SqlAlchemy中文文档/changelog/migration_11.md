---
title: migration_11
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/d70838/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
SQLAlchemy 1.1有哪些新特性？[¶](#what-s-new-in-sqlalchemy-1-1 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍 SQLAlchemy 版本 1.0 和 SQLAlchemy 版本 1.1 之间的变化。

引言[¶ T0\>](#introduction "Permalink to this headline")
--------------------------------------------------------

本指南介绍 SQLAlchemy
1.1 版中的新增功能，并介绍影响用户将其应用程序从 1.0 系列 SQLAlchemy 迁移到 1.1 的更改。

请仔细阅读关于行为变化的章节，以了解行为中潜在的向后不兼容的变化。

平台/安装程序更改[¶](#platform-installer-changes "Permalink to this headline")
------------------------------------------------------------------------------

### Setuptools 现在需要安装[¶](#setuptools-is-now-required-for-install "Permalink to this headline")

SQLAlchemy的`setup.py`文件多年来都支持使用Setuptools并且没有安装；支持使用直线Distutils的“后备”模式。由于Setuptools-less
Python环境现在还没有人听说过，为了更全面地支持Setuptools的特性，特别是支持py.test与它的集成以及诸如“extras”之类的东西，`setup.py`

也可以看看

[Installation Guide](intro.html#installation)

[＃3489 T0\>](http://www.sqlalchemy.org/trac/ticket/3489)

### 启用/禁用C扩展构建仅通过环境变量[¶](#enabling-disabling-c-extension-builds-is-only-via-environment-variable "Permalink to this headline")

只要有可能，C扩展默认在安装过程中生成。要禁用C扩展构建，可以使用`DISABLE_SQLALCHEMY_CEXT`环境变量，从 SQLAlchemy 0.8.6 /
0.9.4 开始。之前使用`--without-cextensions`参数的方法已被删除，因为它依赖于setuptools的不推荐使用的功能。

也可以看看

[Installing the C Extensions](intro.html#c-extensions)

[＃3500 T0\>](http://www.sqlalchemy.org/trac/ticket/3500)

新功能和改进 - ORM [¶](#new-features-and-improvements-orm "Permalink to this headline")
---------------------------------------------------------------------------------------

### 新会话生命周期事件[¶](#new-session-lifecycle-events "Permalink to this headline")

The [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
has long supported events that allow some degree of tracking of state
changes to objects, including [`SessionEvents.before_attach()`](orm_events.html#sqlalchemy.orm.events.SessionEvents.before_attach "sqlalchemy.orm.events.SessionEvents.before_attach"),
[`SessionEvents.after_attach()`](orm_events.html#sqlalchemy.orm.events.SessionEvents.after_attach "sqlalchemy.orm.events.SessionEvents.after_attach"),
and [`SessionEvents.before_flush()`](orm_events.html#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush").
Session文档还在[Quickie Intro to Object
States](orm_session_state_management.html#session-object-states)中记录主要对象状态。但是，从来没有过跟踪对象的系统，因为它们通过这些转换。此外，由于对象在“持久”和“分离”状态之间起作用，“被删除”对象的状态历史上一直很模糊。

为了清理这个区域并且允许会话状态转换的领域完全透明，添加了一系列新事件，这些事件旨在涵盖对象可能在状态之间转换的各种可能方式，并且另外“已删除”状态具有在会话对象状态范围内被赋予了自己的官方名称。

#### 新的状态转换事件[¶](#new-state-transition-events "Permalink to this headline")

现在可以根据旨在覆盖特定转换的会话级别事件来拦截诸如[persistent](glossary.html#term-persistent)，[pending](glossary.html#term-pending)等对象的所有状态之间的转换。当对象移动到[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中时，会跳出[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，甚至是使用[`Session.rollback()`](orm_session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")明确存在于[`SessionEvents`](orm_events.html#sqlalchemy.orm.events.SessionEvents "sqlalchemy.orm.events.SessionEvents")的界面中。

In total, there are **ten new events**.
这些事件的摘要位于新编写的文档部分[Object Lifecycle
Events](orm_session_events.html#session-lifecycle-events)中。

#### 添加新对象状态“已删除”，已删除对象不再是“持久性”[¶](#new-object-state-deleted-is-added-deleted-objects-no-longer-persistent "Permalink to this headline")

始终将[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中对象的[persistent](glossary.html#term-persistent)状态记录为具有有效数据库标识的对象；然而，对于在刷新内删除的对象，它们一直处于灰色区域，它们并未真正“脱离”[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，因为它们仍可在回滚中恢复，但并不真正“持久”，因为它们的数据库标识已被删除，并且它们不存在于标识映射中。

为了解决给定新事件的灰色区域，引入了一个新的对象状态[deleted](glossary.html#term-deleted)。这种状态存在于“持久”和“分离”状态之间。通过[`Session.delete()`](orm_session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")标记为删除的对象保持“持久”状态，直到刷新结束；此时，它将从身份映射中移除，移至“已删除”状态，并调用[`SessionEvents.persistent_to_deleted()`](orm_events.html#sqlalchemy.orm.events.SessionEvents.persistent_to_deleted "sqlalchemy.orm.events.SessionEvents.persistent_to_deleted")钩子。如果回滚[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的事务，该对象将作为持久性恢复；调用[`SessionEvents.deleted_to_persistent()`](orm_events.html#sqlalchemy.orm.events.SessionEvents.deleted_to_persistent "sqlalchemy.orm.events.SessionEvents.deleted_to_persistent")转换。否则，如果[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的事务被提交，则调用[`SessionEvents.deleted_to_detached()`](orm_events.html#sqlalchemy.orm.events.SessionEvents.deleted_to_detached "sqlalchemy.orm.events.SessionEvents.deleted_to_detached")转换。

此外，对于处于新“已删除”状态的对象，[`InstanceState.persistent`](orm_internals.html#sqlalchemy.orm.state.InstanceState.persistent "sqlalchemy.orm.state.InstanceState.persistent")访问器**不再返回 True**；相反，[`InstanceState.deleted`](orm_internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")访问器已得到增强，可以可靠地报告此新状态。当对象被分离时，[`InstanceState.deleted`](orm_internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")将返回 False，而[`InstanceState.detached`](orm_internals.html#sqlalchemy.orm.state.InstanceState.detached "sqlalchemy.orm.state.InstanceState.detached")存取器则为True。要确定某个对象是在当前事务中还是在之前的事务中被删除，请使用[`InstanceState.was_deleted`](orm_internals.html#sqlalchemy.orm.state.InstanceState.was_deleted "sqlalchemy.orm.state.InstanceState.was_deleted")访问器。

#### 强身份地图已弃用[¶](#strong-identity-map-is-deprecated "Permalink to this headline")

新系列过渡事件的灵感之一是能够在物体进出身份地图时对物体进行防漏跟踪，以便可以保持物体移入和移出的“强参照物”地图。有了这个新功能，就不再需要[`Session.weak_identity_map`](orm_session_api.html#sqlalchemy.orm.session.Session.params.weak_identity_map "sqlalchemy.orm.session.Session")参数和相应的`StrongIdentityMap`对象。由于“强引用”行为曾经是唯一可用的行为，并且许多应用程序都是为了承担此行为而编写的，所以此选项在 SQLAlchemy 中保留了很多年。长久以来，建议对象的强参考跟踪不是[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的固有工作，而是应用程序需要构建的应用程序级构造；新的事件模型甚至可以复制强身份地图的确切行为。有关说明如何替换强身份映射的新配方，请参见[Session
Referencing
Behavior](orm_session_state_management.html#session-referencing-behavior)。

[＃2677 T0\>](http://www.sqlalchemy.org/trac/ticket/2677)

### 新的 init\_scalar()事件在ORM级别[¶](#new-init-scalar-event-intercepts-default-values-at-orm-level "Permalink to this headline")处截取默认值

对于非持久对象，首次访问尚未设置的属性时，ORM会生成`None`值：

    >>> obj = MyObj()
    >>> obj.some_value
    None

对于这个 Python 内部值来说，有一个用例与 Core 生成的默认值相对应，甚至在该对象被保存之前。为了适应这种用例，添加了一个新事件[`AttributeEvents.init_scalar()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.init_scalar "sqlalchemy.orm.events.AttributeEvents.init_scalar")。在[Attribute
Instrumentation](orm_examples.html#examples-instrumentation)处的新示例`active_column_defaults.py`演示了一个示例用法，因此效果可以是：

    >>> obj = MyObj()
    >>> obj.some_value
    "my default"

[＃1311 T0\>](http://www.sqlalchemy.org/trac/ticket/1311)

### 有关“不可干扰”类型的更改[¶](#changes-regarding-unhashable-types "Permalink to this headline")

[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象具有众所周知的“扣除”返回行的行为，该行包含至少一个ORM映射实体（例如，完全映射的对象，而不是单个列值）。这样做的主要目的是使实体的处理能够与标识映射一起平稳地工作，包括适应通常在已加入的加载加载中表示的重复实体，以及何时使用连接来过滤额外的列。

此重复数据删除依赖于行内元素的可否性。通过引入Postgresql的特殊类型，如[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")，[`postgresql.HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")和[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")，行中类型的体验是不可及的，遇到问题比以前更普遍。

事实上，SQLAlchemy从0.8版本开始在数据类型中包含一个标记，标记为“不可干扰”，但是此标志在内置类型中并未一致使用。如[ARRAY
and JSON types now correctly specify
“unhashable”](#change-3499-postgresql)，现在可以为所有Postgresql的“结构”类型一致地设置此标志。

由于[`NullType`](core_type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")用于引用未知类型的任何表达式，因此“不可用”标志也设置在[`NullType`](core_type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")类型中。

另外，所谓的“不可干扰”类型的处理与以前的版本略有不同；在内部，我们使用`id()`函数从这些结构中获取“散列值”，就像我们对任何普通的映射对象一样。这取代了之前对对象应用计数器的方法。

[＃3499 T0\>](http://www.sqlalchemy.org/trac/ticket/3499)

### 添加了特定的检查以传递映射类，实例为 SQL 文字[¶](#specific-checks-added-for-passing-mapped-classes-instances-as-sql-literals "Permalink to this headline")

现在，键入系统对 SQLAlchemy“可检查”对象在上下文中的传递进行了特定的检查，否则这些对象将作为文字值处理。任何可合法作为 SQL 值传递的 SQLAlchemy 内置对象都包含一个为该对象提供有效 SQL 表达式的方法`__clause_element__()`。对于不提供此功能的 SQLAlchemy 对象（如映射类，映射器和映射实例），会发出更多信息性错误消息，而不是让 DBAPI 接收对象并稍后失败。下面举例说明一个例子，其中基于字符串的属性`User.name`与`User()`的完整实例进行比较，而不是针对字符串值：

    >>> some_user = User()
    >>> q = s.query(User).filter(User.name == some_user)
    ...
    sqlalchemy.exc.ArgumentError: Object <__main__.User object at 0x103167e90> is not legal as a SQL literal value

当在`User.name == some_user`之间进行比较时，立即发生异常。以前，像上面这样的比较会产生一个 SQL 表达式，只有在解析成 DBAPI 执行调用后才会失败；映射的`User`对象最终将成为DBAPI将拒绝的绑定参数。

请注意，在上面的示例中，表达式失败，因为`User.name`是基于字符串的（例如列向导）属性。The change does *not* impact
the usual case of comparing a many-to-one relationship attribute to an
object, which is handled distinctly:

    >>> # Address.user refers to the User mapper, soplain
    >>> # this is of course still OK!
    >>> q = s.query(Address).filter(Address.user == some_user)

[＃3321 T0\>](http://www.sqlalchemy.org/trac/ticket/3321)

### 新的可索引 ORM 扩展[¶](#new-indexable-orm-extension "Permalink to this headline")

[Indexable](orm_extensions_indexable.html)扩展是对混合属性功能的扩展，它允许构建引用“可索引”数据类型的特定元素（如数组或 JSON 字段）的属性：

    class Person(Base):
        __tablename__ = 'person'

        id = Column(Integer, primary_key=True)
        data = Column(JSON)

        name = index_property('data', 'name')

以上，在初始化为空字典之后，`name`属性将从JSON列`data`读取/写入字段`"name"`：

    >>> person = Person(name='foobar')plain
    >>> person.name
    foobar

当该属性被修改时，该扩展还会触发一个更改事件，因此不需要使用[`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")来跟踪此更改。

也可以看看

[Indexable](orm_extensions_indexable.html)

### 允许在默认[¶](#new-options-allowing-explicit-persistence-of-null-over-a-default "Permalink to this headline")上显式保持NULL的新选项

与作为[JSON “null” is inserted as expected with ORM operations,
regardless of column default
present](#change-3514)，基本的[`TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")类现在支持[`TypeEngine.evaluates_none()`](core_type_api.html#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")方法，该方法允许将属性上的`None`值的肯定集保留为 NULL，而不是从 INSERT 语句中省略列，它具有使用列级别缺省的效果。这允许将现有对象级别的技术分配给属性的`sql.null()`的映射器级配置。

也可以看看

[Forcing NULL on a column with a
default](orm_persistence_techniques.html#session-forcing-null)的列上强制NULL

[＃3250 T0\>](http://www.sqlalchemy.org/trac/ticket/3250)

### 进一步修复单表继承查询[¶](#further-fixes-to-single-table-inheritance-querying "Permalink to this headline")

Continuing from 1.0’s [Change to single-table-inheritance criteria when
using from\_self(), count()](migration_10.html#migration-3177), the
[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
should no longer inappropriately add the “single inheritance” criteria
when the query is against a subquery expression such as an exists:

    class Widget(Base):
        __tablename__ = 'widget'
        id = Column(Integer, primary_key=True)
        type = Column(String)
        data = Column(String)
        __mapper_args__ = {'polymorphic_on': type}


    class FooWidget(Widget):
        __mapper_args__ = {'polymorphic_identity': 'foo'}

    q = session.query(FooWidget).filter(FooWidget.data == 'bar').exists()

    session.query(q).all()

生产：

    SELECT EXISTS (SELECT 1
    FROM widget
    WHERE widget.data = :data_1 AND widget.type IN (:type_1)) AS anon_1

在内部的 IN 子句是适当的，为了限制到 FooWidget 对象，但是以前 IN 子句也会在子查询的外面再次生成。

[＃3582 T0\>](http://www.sqlalchemy.org/trac/ticket/3582)

### 当数据库[¶](#improved-session-state-when-a-savepoint-is-cancelled-by-the-database "Permalink to this headline")取消 SAVEPOINT 时改进了会话状态

MySQL的一个常见情况是当事务内发生死锁时，SAVEPOINT被取消。[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")已被修改，以稍微更优雅地处理这种失败模式，以使外部的非保存点事务仍然可用：

    s = Session()
    s.begin_nested()

    s.add(SomeObject())

    try:
        # assume the flush fails, flush goes to rollback to the
        # savepoint and that also fails
        s.flush()
    except Exception as err:
        print("Something broke, and our SAVEPOINT vanished too")

    # this is the SAVEPOINT transaction, marked as
    # DEACTIVE so the rollback() call succeeds
    s.rollback()

    # this is the outermost transaction, remains ACTIVE
    # so rollback() or commit() can succeed
    s.rollback()

这个问题是[＃2696](http://www.sqlalchemy.org/trac/ticket/2696)的一个延续，我们发出警告，以便在 Python
2 上运行时可以看到原始错误，即使 SAVEPOINT 异常优先。在 Python
3 中，异常是链接的，因此两个失败都会单独报告。

[＃3680 T0\>](http://www.sqlalchemy.org/trac/ticket/3680)

### 错误的“新实例X与持久性实例Y冲突”flush flush fixed [¶](#erroneous-new-instance-x-conflicts-with-persistent-instance-y-flush-errors-fixed "Permalink to this headline")

[`Session.rollback()`](orm_session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法负责删除插入到数据库中的对象，例如从挂起转移到持久，在现在的回滚事务中。使这种状态变化的对象在弱引用集合中被跟踪，并且如果一个对象从该集合中被垃圾收集，[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")不再担心它（否则它不会为插入操作交易中的许多新对象）。但是，如果应用程序在回滚发生之前重新加载事务内的相同垃圾收集行，则会出现问题；如果对该对象的强引用保留在下一个事务中，则该对象未被插入并且应该被移除的事实将会丢失，并且flush会错误地引发错误：

    from sqlalchemy import Column, create_engine
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)

    e = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(e)

    s = Session(e)

    # persist an object
    s.add(A(id=1))
    s.flush()

    # rollback buffer loses reference to A

    # load it again, rollback buffer knows nothing
    # about it
    a1 = s.query(A).first()

    # roll back the transaction; all state is expired but the
    # "a1" reference remains
    s.rollback()

    # previous "a1" conflicts with the new one because we aren't
    # checking that it never got committed
    s.add(A(id=1))
    s.commit()

上述计划将提高：

    FlushError: New instance <User at 0x7f0287eca4d0> with identity key
    (<class 'test.orm.test_transaction.User'>, ('u1',)) conflicts
    with persistent instance <User at 0x7f02889c70d0>

这个错误是，当上面的异常被引发时，工作单元正在对原始对象进行操作，假设它是一个活动行，事实上该对象已经过期，并且经过测试发现它已经消失。修复程序现在测试这个条件，所以在我们看到的SQL日志中：

    BEGIN (implicit)

    INSERT INTO a (id) VALUES (?)
    (1,)

    SELECT a.id AS a_id FROM a LIMIT ? OFFSET ?
    (1, 0)

    ROLLBACK

    BEGIN (implicit)

    SELECT a.id AS a_id FROM a WHERE a.id = ?
    (1,)

    INSERT INTO a (id) VALUES (?)
    (1,)

    COMMIT

在上面，工作单元现在为我们将要报告的行做一个 SELECT，作为冲突，看到它不存在，并正常进行。只有在我们在任何情况下都会错误地引发异常的情况下才会产生此 SELECT 的费用。

[＃3677 T0\>](http://www.sqlalchemy.org/trac/ticket/3677)

### 用于加入继承映射的passive\_deletes功能[¶](#passive-deletes-feature-for-joined-inheritance-mappings "Permalink to this headline")

现在，由于[`Session.delete()`](orm_session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")，连接表继承映射现在可以允许 DELETE 继续执行，它仅为基表发出 DELETE，而不是子类表，允许配置 ON
DELETE
CASCADE 为配置的外键进行。这是使用[`orm.mapper.passive_deletes`(orm_mapping_api.html#sqlalchemy.orm.mapper.params.passive_deletes "sqlalchemy.orm.mapper")选项配置的：

    from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()


    class A(Base):
        __tablename__ = "a"
        id = Column('id', Integer, primary_key=True)
        type = Column(String)

        __mapper_args__ = {
            'polymorphic_on': type,
            'polymorphic_identity': 'a',
            'passive_deletes': True
        }


    class B(A):
        __tablename__ = 'b'
        b_table_id = Column('b_table_id', Integer, primary_key=True)
        bid = Column('bid', Integer, ForeignKey('a.id', ondelete="CASCADE"))
        data = Column('data', String)

        __mapper_args__ = {
            'polymorphic_identity': 'b'
        }

通过上面的映射，在基本映射器上配置[`orm.mapper.passive_deletes`](orm_mapping_api.html#sqlalchemy.orm.mapper.params.passive_deletes "sqlalchemy.orm.mapper")选项；它对于具有选项集的映射器的后代的所有非基本映射器都有效。对于`B`类型的对象，DELETE 不再需要检索`b_table_id`的主键值（如果未加载），也不需要为表本身发出DELETE语句：

    session.delete(some_b)plain
    session.commit()

将发出 SQL 如下：

    DELETE FROM a WHERE a.id = %(id)s
    {'id': 1}
    COMMIT

与往常一样，目标数据库必须具有启用 ON DELETE CASCADE 的外键支持。

[＃2349 T0\>](http://www.sqlalchemy.org/trac/ticket/2349)

### 相同名称的backrefs在应用于具体继承子类时不会引发错误[¶](#same-named-backrefs-will-not-raise-an-error-when-applied-to-concrete-inheritance-subclasses "Permalink to this headline")

以下映射总是可以没有问题：

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        b = relationship("B", foreign_keys="B.a_id", backref="a")

    class A1(A):
        __tablename__ = 'a1'
        id = Column(Integer, primary_key=True)
        b = relationship("B", foreign_keys="B.a1_id", backref="a1")
        __mapper_args__ = {'concrete': True}

    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)

        a_id = Column(ForeignKey('a.id'))
        a1_id = Column(ForeignKey('a1.id'))

在上面，尽管类`A`和类`A1`有一个名为`b`的关系，所以不会发生冲突警告或错误，因为类`A1`

但是，如果以其他方式配置关系，则会发生错误：

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)


    class A1(A):
        __tablename__ = 'a1'
        id = Column(Integer, primary_key=True)
        __mapper_args__ = {'concrete': True}


    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)

        a_id = Column(ForeignKey('a.id'))
        a1_id = Column(ForeignKey('a1.id'))

        a = relationship("A", backref="b")
        a1 = relationship("A1", backref="b")

此修补程序增强了 backref 功能，因此不会发出错误，还会在映射程序逻辑中进行额外的检查以绕过要替换的属性的警告。

[＃3630 T0\>](http://www.sqlalchemy.org/trac/ticket/3630)

### 混合属性和方法现在传播docstring以及.info [¶](#hybrid-properties-and-methods-now-propagate-the-docstring-as-well-as-info "Permalink to this headline")

混合方法或属性现在将反映原始文档字符串中存在的`__doc__`值：

    class A(Base):plain
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)

        name = Column(String)

        @hybrid_property
        def some_name(self):
            """The name field"""
            return self.name

现在，`A.some_name.__doc__`的上述值现在符合：

    >>> A.some_name.__doc__
    The name field

但是，要实现这一点，混合属性的机制必然变得更加复杂。以前，混合类的级别访问器是一个简单的pass-thru，也就是说，这个测试会成功：

    >>> assert A.name is A.some_name

通过改变，由`A.some_name`返回的表达式被封装在它自己的`QueryableAttribute`包装器中：

    >>> A.some_name
    <sqlalchemy.orm.attributes.hybrid_propertyProxy object at 0x7fde03888230>

大量的测试进入确保这个包装器正常工作，包括像[Custom Value
Object](http://techspot.zzzeek.org/2011/10/21/hybrids-and-value-agnostic-types/)配方那样的复杂方案，但是我们会看到用户没有发生其他回归。

作为这种变化的一部分，现在还从混合描述符本身传播`hybrid_property.info`集合，而不是从基础表达式传播。也就是说，访问`A.some_name.info`现在会返回您从`inspect(A).all_orm_descriptors['some_name'].info`获得的相同字典：

    >>> A.some_name.info['foo'] = 'bar'
    >>> from sqlalchemy import inspect
    >>> inspect(A).all_orm_descriptors['some_name'].info
    {'foo': 'bar'}

请注意，这个`.info`字典与混合描述符可能直接代理的映射属性的**分开**这是从 1.0 开始的行为变化。包装器仍将代理镜像属性的其他有用属性，如[`QueryableAttribute.property`](orm_internals.html#sqlalchemy.orm.attributes.QueryableAttribute.property "sqlalchemy.orm.attributes.QueryableAttribute.property")和`QueryableAttribute.class_`。

[＃3653 T0\>](http://www.sqlalchemy.org/trac/ticket/3653)

### Session.merge 解决了与持久[¶](#session-merge-resolves-pending-conflicts-the-same-as-persistent "Permalink to this headline")相同的未决冲突

[`Session.merge()`](orm_session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")方法现在将跟踪图中给定的对象的身份，以在发出INSERT之前保持主键唯一性。当遇到相同身份的重复对象时，遇到对象时非主键属性被**覆盖**，这基本上是非确定性的。此行为与持久对象（即通过主键已位于数据库中的对象）已被处理的方式相匹配，因此此行为在内部更一致。

鉴于：

    u1 = User(id=7, name='x')
    u1.orders = [
        Order(description='o1', address=Address(id=1, email_address='a')),
        Order(description='o2', address=Address(id=1, email_address='b')),
        Order(description='o3', address=Address(id=1, email_address='c'))
    ]

    sess = Session()
    sess.merge(u1)

在上面，我们将一个`User`对象与三个新的`Order`对象合并，每个对象引用一个不同的`Address`对象，但是每个对象都被赋予相同的主键。[`Session.merge()`](orm_session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")的当前行为是查找此`Address`对象的标识映射，并将其用作目标。If the object is present,
meaning that the database already has a row for `Address` with primary key “1”, we can see that the
`email_address` field of the `Address` will be overwritten three times, in this case with the values
a, b and finally c.

但是，如果主键“1”的`Address`行不存在，[`Session.merge()`](orm_session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")会改为创建三个单独的`Address`然后我们会在 INSERT 时发生主键冲突。新行为是为这些`Address`对象建议的主键在单独的字典中进行跟踪，以便我们将三个建议的`Address`对象的状态合并到一个`Address`要插入的对象。

如果原始案例发出某种警告，即在单一合并树中存在冲突数据，可能会更好一些，但是对于持久性案例，价值的非确定性合并已经持续多年。它现在匹配待处理的案例。对于这两种情况，警告冲突值的功能仍然可行，但会增加相当大的性能开销，因为在合并期间必须对每个列值进行比较。

[＃3601 T0\>](http://www.sqlalchemy.org/trac/ticket/3601)

### 修复涉及多对一对象的移动，并使用用户启动的 foriegn 键操作[¶](#fix-involving-many-to-one-object-moves-with-user-initiated-foriegn-key-manipulations "Permalink to this headline")

一个错误已经被修复，涉及用另一个对象替换对象的多对一引用的机制。在属性操作期间，先前引用的对象的位置现在使用数据库提交的外键值，而不是当前的外键值。修复的主要效果是，即使外键属性事先被手动移动到新值，在进行多对一更改时，对集合的 backref 事件也会更准确地触发。Assume
a mapping of the classes `Parent` and
`SomeClass`, where `SomeClass.parent` refers to `Parent` and
`Parent.items` refers to the collection of
`SomeClass` objects:

    some_object = SomeClass()
    session.add(some_object)
    some_object.parent_id = some_parent.id
    some_object.parent = some_parent

在上面，我们创建了一个挂起的对象`some_object`，将它的外键操作为`Parent`来引用它，*然后*我们实际建立了关系。在错误修复之前，backref 不会被触发：

    # before the fixplain
    assert some_object not in some_parent.items

现在的修正是，当我们试图找到`some_object.parent`的前一个值时，我们忽略手动设置的父ID，然后查找数据库提交的值。在这种情况下，它是None，因为对象处于挂起状态，所以事件系统将`some_object.parent`记录为净更改：

    # after the fix, backref fired off for some_object.parent = some_parent
    assert some_object in some_parent.items

虽然不鼓励操纵由关系管理的外键属性，但对此用例的支持有限。为了允许加载进行而操纵外键的应用程序通常会利用[`Session.enable_relationship_loading()`](orm_session_api.html#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")和`RelationshipProperty.load_on_pending`特性，这些特性会导致关系发出延迟加载基于内存中不存在的外键值。无论这些功能是否在使用中，这种行为改善现在都将显而易见。

[＃3708 T0\>](http://www.sqlalchemy.org/trac/ticket/3708)

### 使用多模实体对 Query.correlate 方法的改进[¶](#improvements-to-the-query-correlate-method-with-polymoprhic-entities "Permalink to this headline")

在最近的SQLAlchemy版本中，由多种形式的“多态”查询生成的SQL具有比以前更加“平坦”的形式，其中几个表的JOIN不再无条件地捆绑到子查询中。为了适应这种情况，现在，[`Query.correlate()`](orm_query.html#sqlalchemy.orm.query.Query.correlate "sqlalchemy.orm.query.Query.correlate")方法从这种多态选择中提取单个表并确保所有都是子查询的“关联”的一部分。假设映射文档中的`Person/Manager/Engineer->Company`设置，使用with\_polymorphic：

    sess.query(Person.name)
                .filter(
                    sess.query(Company.name).
                    filter(Company.company_id == Person.company_id).
                    correlate(Person).as_scalar() == "Elbonia, Inc.")

上面的查询现在生成：

    SELECT people.name AS people_nameplain
    FROM people
    LEFT OUTER JOIN engineers ON people.person_id = engineers.person_id
    LEFT OUTER JOIN managers ON people.person_id = managers.person_id
    WHERE (SELECT companies.name
    FROM companies
    WHERE companies.company_id = people.company_id) = ?

Before the fix, the call to `correlate(Person)`
would inadvertently attempt to correlate to the join of
`Person`, `Engineer` and
`Manager` as a single unit, so `Person` wouldn’t be correlated:

    -- old, incorrect queryplain
    SELECT people.name AS people_name
    FROM people
    LEFT OUTER JOIN engineers ON people.person_id = engineers.person_id
    LEFT OUTER JOIN managers ON people.person_id = managers.person_id
    WHERE (SELECT companies.name
    FROM companies, people
    WHERE companies.company_id = people.company_id) = ?

对多态映射使用相关的子查询仍然有一些未完善的边缘。例如，如果`Person`与所谓的“具体多态联合”查询多态链接，则上述子查询可能无法正确引用此子查询。在所有情况下，完全引用“多态”实体的方法是首先从它创建一个[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")对象：

    # works with all SQLAlchemy versions and all types of polymorphic
    # aliasing.

    paliased = aliased(Person)
    sess.query(paliased.name)
                .filter(
                    sess.query(Company.name).
                    filter(Company.company_id == paliased.company_id).
                    correlate(paliased).as_scalar() == "Elbonia, Inc.")

[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")构造保证“多态可选”包装在子查询中。通过在相关的子查询中明确地引用它，正确地使用多态形式。

[＃3662 T0\>](http://www.sqlalchemy.org/trac/ticket/3662)

### 查询的字符串化将向会话查询正确的方言[¶](#stringify-of-query-will-consult-the-session-for-the-correct-dialect "Permalink to this headline")

在[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象上调用`str()`会查询[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中是否使用正确的“绑定”，以便呈现 SQL 被传递给数据库。特别是，假设[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")与适当的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")相关联，这允许引用特定于方言的 SQL 结构的[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")是可呈现的。以前，如果与映射关联的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")本身绑定到目标[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，此行为才会生效。

如果底层[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")和[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")都不与任何绑定的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")相关联，则使用“默认”方言的回退来生成SQL字符串。

也可以看看

[“Friendly” stringification of Core SQL constructs without a
dialect](#change-3631)

[＃3081 T0\>](http://www.sqlalchemy.org/trac/ticket/3081)

### 加入了同一个实体在一行中出现多次的急切加载[¶](#joined-eager-loading-where-the-same-entity-is-present-multiple-times-in-one-row "Permalink to this headline")

已经做了一个修复，即通过加入的加载加载来加载属性，即使实体已经从不包含该属性的“路径”上的行加载。这是一个很难重现的深层用例，但总体思路如下：

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        b_id = Column(ForeignKey('b.id'))
        c_id = Column(ForeignKey('c.id'))

        b = relationship("B")
        c = relationship("C")


    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)
        c_id = Column(ForeignKey('c.id'))

        c = relationship("C")


    class C(Base):
        __tablename__ = 'c'
        id = Column(Integer, primary_key=True)
        d_id = Column(ForeignKey('d.id'))
        d = relationship("D")


    class D(Base):
        __tablename__ = 'd'
        id = Column(Integer, primary_key=True)


    c_alias_1 = aliased(C)
    c_alias_2 = aliased(C)

    q = s.query(A)
    q = q.join(A.b).join(c_alias_1, B.c).join(c_alias_1.d)
    q = q.options(contains_eager(A.b).contains_eager(B.c, alias=c_alias_1).contains_eager(C.d))
    q = q.join(c_alias_2, A.c)
    q = q.options(contains_eager(A.c, alias=c_alias_2))

上面的查询发出 SQL 如下所示：

    SELECTplain
        d.id AS d_id,
        c_1.id AS c_1_id, c_1.d_id AS c_1_d_id,
        b.id AS b_id, b.c_id AS b_c_id,
        c_2.id AS c_2_id, c_2.d_id AS c_2_d_id,
        a.id AS a_id, a.b_id AS a_b_id, a.c_id AS a_c_id
    FROM
        a
        JOIN b ON b.id = a.b_id
        JOIN c AS c_1 ON c_1.id = b.c_id
        JOIN d ON d.id = c_1.d_id
        JOIN c AS c_2 ON c_2.id = a.c_id

我们可以看到`c`表是从两次中选择的；一次在`Abc  - ＆gt； c_alias_1`的上下文中，另一个在`Ac  - ＆gt； c_alias_2`。Also, we can see that it is quite possible that the
`C` identity for a single row is the **same** for
both `c_alias_1` and `c_alias_2`, meaning two sets of columns in one row result in only one new
object being added to the identity map.

上面的查询选项只需要在`c_alias_1`的上下文中加载属性`C.d`，而不是`c_alias_2`。因此，无论我们在标识映射中获得的最终`C`对象是否具有加载的`C.d`属性，都取决于遍历映射的方式，而不是完全随机的，实质上不是-deterministic。The
fix is that even if the loader for `c_alias_1` is
processed after that of `c_alias_2` for a single row
where they both refer to the same identity, the `C.d` element will still be loaded.
以前，加载器并不试图修改已经通过不同路径加载的实体的加载。首先到达实体的加载器一直是非确定性的，因此这种修复可能在某些情况下可以检测到，而不是其他情况下的行为改变。

该修复包括针对“多个路径到一个实体”案例的两种变体的测试，修复应该涵盖此类性质的所有其他场景。

[＃3431 T0\>](http://www.sqlalchemy.org/trac/ticket/3431)

### DISTINCT + ORDER BY [¶](#columns-no-longer-added-redundantly-with-distinct-order-by "Permalink to this headline")不再重复添加列

像下面这样的查询现在只会增加SELECT列表中缺少的那些列，而没有重复：

    q = session.query(User.id, User.name.label('name')).\
        distinct().\
        order_by(User.id, User.name, User.fullname)

生产：

    SELECT DISTINCT user.id AS a_id, user.name AS name,
     user.fullname AS a_fullname
    FROM a ORDER BY user.id, user.name, user.fullname

以前，它会产生：

    SELECT DISTINCT user.id AS a_id, user.name AS name, user.name AS a_name,plain
      user.fullname AS a_fullname
    FROM a ORDER BY user.id, user.name, user.fullname

在上面，`user.name`列被不必要地添加。结果不会受到影响，因为在任何情况下附加列都不包含在结果中，但列是不必要的。

此外，当传递表达式到[`Query.distinct()`](orm_query.html#sqlalchemy.orm.query.Query.distinct "sqlalchemy.orm.query.Query.distinct")使用Postgresql
DISTINCT ON格式时，上面的“列添加”逻辑完全禁用。

当查询绑定到一个子查询中用于加入的加载时，“增加列表”规则必然更具侵略性，因此ORDER
BY仍然可以被满足，所以这种情况保持不变。

[＃3641 T0\>](http://www.sqlalchemy.org/trac/ticket/3641)

### 将新的MutableList和MutableSet助手添加到突变跟踪扩展[¶](#new-mutablelist-and-mutableset-helpers-added-to-the-mutation-tracking-extension "Permalink to this headline")中

新的帮助类[`MutableList`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")和[`MutableSet`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")已被添加到[Mutation
Tracking](orm_extensions_mutable.html)扩展中，以补充现有的[`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")助手。

[＃3297 T0\>](http://www.sqlalchemy.org/trac/ticket/3297)

### 新的“raise”加载器策略[¶](#new-raise-loader-strategy "Permalink to this headline")

为了帮助防止在加载一系列对象之后发生不需要的延迟加载，可以应用新的“lazy
='raise'”策略和相应的加载程序选项[`orm.raiseload()`](orm_loading_relationships.html#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload")关系属性，当访问非热切加载的属性以进行读取时，会导致该属性引发`InvalidRequestError`：

    >>> from sqlalchemy.orm import raiseload
    >>> a1 = s.query(A).options(raiseload(A.bs)).first()
    >>> a1.bs
    Traceback (most recent call last):
    ...
    sqlalchemy.exc.InvalidRequestError: 'A.bs' is not available due to lazy='raise'

[＃3512 T0\>](http://www.sqlalchemy.org/trac/ticket/3512)

### Mapper.order\_by 已弃用[¶](#mapper-order-by-is-deprecated "Permalink to this headline")

来自SQLAlchemy最初版本的这个旧参数是ORM原始设计的一部分，它将[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象作为面向公众的查询结构。这个角色早已被[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象取代，我们使用[`Query.order_by()`](orm_query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")来指示结果的排序，以一种对任意组合SELECT语句，实体和SQL表达式。There
are many areas in which [`Mapper.order_by`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.params.order_by "sqlalchemy.orm.mapper.Mapper")
doesn’t work as expected (or what would be expected is not clear), such
as when queries are combined into unions; these cases are not supported.

[＃3394 T0\>](http://www.sqlalchemy.org/trac/ticket/3394)

新功能和改进 - 核心[¶](#new-features-and-improvements-core "Permalink to this headline")
----------------------------------------------------------------------------------------

### CTE 支持 INSERT，UPDATE，DELETE [¶](#cte-support-for-insert-update-delete "Permalink to this headline")

其中一个最广泛要求的功能是支持与 INSERT，UPDATE，DELETE 一起使用的公用表表达式（CTE），现在已经实现。INSERT
/ UPDATE /
DELETE 既可以从 SQL 顶部的 WITH 子句中绘制，也可以在更大的语句的上下文中用作 CTE 本身。

作为此更改的一部分，包含 CTE 的 SELECT
INSERT 将现在将 CTE 呈现在整个语句的顶部，而不是像 1.0 中那样嵌套在 SELECT 语句中。

下面是一个在一个语句中呈现 UPDATE，INSERT 和 SELECT 全部的例子：

    >>> from sqlalchemy import table, column, select, literal, exists
    >>> orders = table(
    ...     'orders',
    ...     column('region'),
    ...     column('amount'),
    ...     column('product'),
    ...     column('quantity')
    ... )
    >>>
    >>> upsert = (
    ...     orders.update()
    ...     .where(orders.c.region == 'Region1')
    ...     .values(amount=1.0, product='Product1', quantity=1)
    ...     .returning(*(orders.c._all_columns)).cte('upsert'))
    >>>
    >>> insert = orders.insert().from_select(
    ...     orders.c.keys(),
    ...     select([
    ...         literal('Region1'), literal(1.0),
    ...         literal('Product1'), literal(1)
    ...     ]).where(~exists(upsert.select()))
    ... )
    >>>
    >>> print(insert)  # note formatting added for clarity
    WITH upsert AS
    (UPDATE orders SET amount=:amount, product=:product, quantity=:quantity
     WHERE orders.region = :region_1
     RETURNING orders.region, orders.amount, orders.product, orders.quantity
    )
    INSERT INTO orders (region, amount, product, quantity)
    SELECT
        :param_1 AS anon_1, :param_2 AS anon_2,
        :param_3 AS anon_3, :param_4 AS anon_4
    WHERE NOT (
        EXISTS (
            SELECT upsert.region, upsert.amount,
                   upsert.product, upsert.quantity
            FROM upsert))

[＃2551 T0\>](http://www.sqlalchemy.org/trac/ticket/2551)

### 在窗口函数中支持 RANGE 和 ROWS 规范[¶](#support-for-range-and-rows-specification-within-window-functions "Permalink to this headline")

新的[`expression.over.range_`](core_sqlelement.html#sqlalchemy.sql.expression.over.params.range_ "sqlalchemy.sql.expression.over")和[`expression.over.rows`](core_sqlelement.html#sqlalchemy.sql.expression.over.params.rows "sqlalchemy.sql.expression.over")参数允许窗口函数的 RANGE 和 ROWS 表达式：

    >>> from sqlalchemy import funcplain

    >>> print func.row_number().over(order_by='x', range_=(-5, 10))
    row_number() OVER (ORDER BY x RANGE BETWEEN :param_1 PRECEDING AND :param_2 FOLLOWING)

    >>> print func.row_number().over(order_by='x', rows=(None, 0))
    row_number() OVER (ORDER BY x ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

    >>> print func.row_number().over(order_by='x', range_=(-2, None))
    row_number() OVER (ORDER BY x RANGE BETWEEN :param_1 PRECEDING AND UNBOUNDED FOLLOWING)

[`expression.over.range_`](core_sqlelement.html#sqlalchemy.sql.expression.over.params.range_ "sqlalchemy.sql.expression.over")和[`expression.over.rows`](core_sqlelement.html#sqlalchemy.sql.expression.over.params.rows "sqlalchemy.sql.expression.over")指定为 2 元组，指定特定范围的负值和正值，“CURRENT
ROW”为 0，无对于 UNBOUNDED。

也可以看看

[Window Functions](core_tutorial.html#window-functions)

[＃3049 T0\>](http://www.sqlalchemy.org/trac/ticket/3049)

### 支持SQL LATERAL关键字[¶](#support-for-the-sql-lateral-keyword "Permalink to this headline")

目前已知 LATERAL 关键字仅受 Postgresql
9.3 及更高版本支持，但因为它是 SQL 关键字添加到 Core 的标准支持的一部分。[`Select.lateral()`](core_selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")的实现采用了特殊的逻辑，而不仅仅是呈现 LATERAL 关键字，以允许从相同的 FROM 子句派生的表与相关的可选择的关联。横向相关性：

    >>> from sqlalchemy import table, column, select, true
    >>> people = table('people', column('people_id'), column('age'), column('name'))
    >>> books = table('books', column('book_id'), column('owner_id'))
    >>> subq = select([books.c.book_id]).\
    ...      where(books.c.owner_id == people.c.people_id).lateral("book_subq")
    >>> print(select([people]).select_from(people.join(subq, true())))
    SELECT people.people_id, people.age, people.name
    FROM people JOIN LATERAL (SELECT books.book_id AS book_id
    FROM books WHERE books.owner_id = people.people_id)
    AS book_subq ON true

也可以看看

[LATERAL correlation](core_tutorial.html#lateral-selects)

[`Lateral`](core_selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")

[`Select.lateral()`](core_selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")

[＃2857 T0\>](http://www.sqlalchemy.org/trac/ticket/2857)

### 支持 TABLESAMPLE [¶](#support-for-tablesample "Permalink to this headline")

可以使用[`FromClause.tablesample()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")方法呈现 SQL 标准 TABLESAMPLE，该方法返回类似于别名的[`TableSample`](core_selectable.html#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构：

    from sqlalchemy import funcplain

    selectable = people.tablesample(
                func.bernoulli(1),
                name='alias',
                seed=func.random())
    stmt = select([selectable.c.people_id])

假设`people`具有列`people_id`，则上述语句将呈现为：

    SELECT alias.people_id FROM
    people AS alias TABLESAMPLE bernoulli(:bernoulli_1)
    REPEATABLE (random())

[＃3718 T0\>](http://www.sqlalchemy.org/trac/ticket/3718)

### `.autoincrement`指令不再为组合主键列启用[¶](#the-autoincrement-directive-is-no-longer-implicitly-enabled-for-a-composite-primary-key-column "Permalink to this headline")

SQLAlchemy 一直具有为单列整数主键启用后端数据库的“自动增量”功能的便利功能；通过“autoincrement”，我们的意思是数据库列将包含数据库提供的任何 DDL 指令，以指示自动递增的整数标识符，例如 MySQL 上的 Postgresql 或 AUTO\_INCREMENT 上的 SERIAL 关键字，另外方言将接收这些生成的使用适合该后端的技术执行[`Table.insert()`](core_metadata.html#sqlalchemy.schema.Table.insert "sqlalchemy.schema.Table.insert")构造的值。

改变的是，该功能不再为*复合*主键自动开启；以前，一个表格定义如：

    Table(plain
        'some_table', metadata,
        Column('x', Integer, primary_key=True),
        Column('y', Integer, primary_key=True)
    )

将“自动增量”语义应用于`'x'`列，仅仅是因为它首先在主键列的列表中。为了禁用此功能，必须在所有列上关闭`autoincrement`：

    # old way
    Table(
        'some_table', metadata,
        Column('x', Integer, primary_key=True, autoincrement=False),
        Column('y', Integer, primary_key=True, autoincrement=False)
    )

使用新行为，组合主键将不会有自动增量语义，除非使用`autoincrement=True`显式标记列：

    # column 'y' will be SERIAL/AUTO_INCREMENT/ auto-generating
    Table(
        'some_table', metadata,
        Column('x', Integer, primary_key=True),
        Column('y', Integer, primary_key=True, autoincrement=True)
    )

In order to anticipate some potential backwards-incompatible scenarios,
the [`Table.insert()`](core_metadata.html#sqlalchemy.schema.Table.insert "sqlalchemy.schema.Table.insert")
construct will perform more thorough checks for missing primary key
values on composite primary key columns that don’t have autoincrement
set up; given a table such as:

    Table(plainplain
        'b', metadata,
        Column('x', Integer, primary_key=True),
        Column('y', Integer, primary_key=True)
    )

一个INSERT发出没有值的表将产生异常：

    CompileError: Column 'b.x' is marked as a member of the primary
    key for table 'b', but has no Python-side or server-side default
    generator indicated, nor does it indicate 'autoincrement=True',
    and no explicit value is passed.  Primary key columns may not
    store NULL. Note that as of SQLAlchemy 1.1, 'autoincrement=True'
    must be indicated explicitly for composite (e.g. multicolumn)
    primary keys if AUTO_INCREMENT/SERIAL/IDENTITY behavior is
    expected for one of the columns in the primary key. CREATE TABLE
    statements are impacted by this change as well on most backends.

对于从服务器端默认或不常见的主键值（如触发器）接收主键值的列，可以使用[`FetchedValue`](core_defaults.html#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")指示存在值生成器：

    Table(
        'b', metadata,
        Column('x', Integer, primary_key=True, server_default=FetchedValue()),
        Column('y', Integer, primary_key=True, server_default=FetchedValue())
    )

对于组合主键实际上旨在将NULL存储在其一个或多个列中（仅在SQLite和MySQL中受支持）的情况，请指定具有`nullable=True`的列：

    Table(
        'b', metadata,
        Column('x', Integer, primary_key=True),
        Column('y', Integer, primary_key=True, nullable=True)
    )

在相关更改中，可以在具有客户端或服务器端默认值的列上将`autoincrement`标志设置为 True。在 INSERT 期间，这通常不会对列的行为产生太大影响。

也可以看看

[No more generation of an implicit KEY for composite primary key w/
AUTO\_INCREMENT](#change-mysql-3216)的组合主键生成隐式KEY

[＃3216 T0\>](http://www.sqlalchemy.org/trac/ticket/3216)

### 支持 IS DISTINCT FROM 和 IS NOT DISTINCT FROM [¶](#support-for-is-distinct-from-and-is-not-distinct-from "Permalink to this headline")

New operators [`ColumnOperators.is_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
and [`ColumnOperators.isnot_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
allow the IS DISTINCT FROM and IS NOT DISTINCT FROM sql operation:

    >>> print column('x').is_distinct_from(None)
    x IS DISTINCT FROM NULL

处理提供了NULL，True和False：

    >>> print column('x').isnot_distinct_from(False)
    x IS NOT DISTINCT FROM false

对于没有这个运算符的 SQLite，会呈现“IS”/“IS
NOT”，它在 SQLite 上的工作方式与其他后端不同：

    >>> from sqlalchemy.dialects import sqlite
    >>> print column('x').is_distinct_from(None).compile(dialect=sqlite.dialect())
    x IS NOT NULL

### 核心和 ORM 支持 FULL OUTER JOIN [¶](#core-and-orm-support-for-full-outer-join "Permalink to this headline")

The new flag [`FromClause.outerjoin.full`](core_selectable.html#sqlalchemy.sql.expression.FromClause.outerjoin.params.full "sqlalchemy.sql.expression.FromClause.outerjoin"),
available at the Core and ORM level, instructs the compiler to render
`FULL OUTER JOIN` where it would normally render
`LEFT OUTER JOIN`:

    stmt = select([t1]).select_from(t1.outerjoin(t2, full=True))

该标志也适用于 ORM 级别：

    q = session.query(MyClass).outerjoin(MyOtherClass, full=True)plainplain

[＃1957 T0\>](http://www.sqlalchemy.org/trac/ticket/1957)

### ResultSet列匹配增强；文本SQL的位置列设置[¶](#resultset-column-matching-enhancements-positional-column-setup-for-textual-sql "Permalink to this headline")

作为[＃918](http://www.sqlalchemy.org/trac/ticket/918)的一部分对1.0系列中的[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")系统进行了一系列改进，它重新组织内部以将与游标绑定的结果列与表/
ORM 元数据在位置上，而不是通过匹配名称，对于包含有关要返回的结果行的完整信息的编译 SQL 结构。这可以显着节省 Python 开销，并且可以将 ORM 和 Core
SQL 表达式链接到结果行的准确性更高。在 1.1 中，这种重组已经在内部得到了进一步研究，并且通过使用最近添加的[`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法，也可以用于纯文本SQL结构。

#### TextAsFrom.columns()现在在位置上工作[¶](#textasfrom-columns-now-works-positionally "Permalink to this headline")

在 0.9 中添加的[`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法在位置上接受基于列的参数；在 1.1 中，当所有列在位置上通过时，这些列与最终结果集的相关性也在位置上执行。这里的关键优势在于，现在可以将文本 SQL 链接到 ORM 级别的结果集，而无需处理不明确或重复的列名称，或者必须将标签方案与 ORM 级别标签方案相匹配。现在需要的仅仅是传递给[`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")的文本SQL和列参数中相同的列顺序：

    from sqlalchemy import text
    stmt = text("SELECT users.id, addresses.id, users.id, "
         "users.name, addresses.email_address AS email "
         "FROM users JOIN addresses ON users.id=addresses.user_id "
         "WHERE users.id = 1").columns(
            User.id,
            Address.id,
            Address.user_id,
            User.name,
            Address.email_address
         )

    query = session.query(User).from_statement(text).\
        options(contains_eager(User.addresses))
    result = query.all()

以上，文本SQL包含三次“id”列，这通常是不明确的。Using the new feature, we
can apply the mapped columns from the `User` and
`Address` class directly, even linking the
`Address.user_id` column to the `users.id` column in textual SQL for fun, and the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
object will receive rows that are correctly targetable as needed,
including for an eager load.

这种变化是**向后不兼容**，其中的代码将列传递给方法的顺序与文本语句中存在的顺序不同。希望这种影响会很低，因为事实上这种方法总是被记录下来，说明按照与文本SQL语句相同的顺序传递的列，尽管内部没有检查为了这。该方法本身在任何情况下仅添加0.9，可能尚未广泛使用。有关如何处理使用它的应用程序的行为更改的注意事项在[TextClause.columns()
will match columns positionally, not by name, when passed
positionally](#behavior-change-3501)。

也可以看看

[Specifying Result-Column
Behaviors](core_tutorial.html#sqlexpression-text-columns) - 在Core教程中

[TextClause.columns() will match columns positionally, not by name, when
passed positionally](#behavior-change-3501) - backwards compatibility
remarks

#### 位置匹配对于core\_ORM SQL结构[¶](#positional-matching-is-trusted-over-name-based-matching-for-core-orm-sql-constructs "Permalink to this headline")的基于名称的匹配值得信赖

此更改的另一方面是匹配列的规则也已被修改，以便更加充分地依赖编译SQL结构的“位置”匹配。给出如下的声明：

    ua = users.alias('ua')
    stmt = select([users.c.user_id, ua.c.user_id])

上述声明将编译为：

    SELECT users.user_id, ua.user_id FROM users, users AS uaplain

在 1.0 中，上面的语句在执行时会使用位置匹配与其原始编译构造相匹配，但由于语句包含重复的`'user_id'`标签，所以“模糊列”规则仍然会涉及防止从一行中获取列。从 1.1 开始，“模糊列”规则不会影响从列结构到 SQL 列的完全匹配，这是 ORM 用于读取列的内容：

    result = conn.execute(stmt)
    row = result.first()

    # these both match positionally, so no error
    user_id = row[users.c.user_id]
    ua_id = row[ua.c.user_id]

    # this still raises, however
    user_id = row['user_id']

#### [¶](#much-less-likely-to-get-an-ambiguous-column-error-message "Permalink to this headline")不太可能出现“模糊列”错误消息

作为这种改变的一部分，错误消息的措辞`不明确 列 名称 '＆lt； name＆gt； t4> in 结果 set！ 'use_labels' / t10> on 选择 语句。` has been dialed back; as this message should now be extremely
rare when using the ORM or Core compiled SQL constructs, it merely
states
`Ambiguous column name '<name>' in result set column descriptions`, and only when a result column is retrieved using the string
name that is actually ambiguous, e.g. `row['user_id']` in the above example.
它现在还引用了呈现的SQL语句本身中实际不明确的名称，而不是指示用于提取的构造本地的键或名称。

[＃3501 T0\>](http://www.sqlalchemy.org/trac/ticket/3501)

### 支持Python的本地`enum`类型和兼容形式[¶](#support-for-python-s-native-enum-type-and-compatible-forms "Permalink to this headline")

现在可以使用任何符合PEP-435枚举类型来构造[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型。使用此模式时，输入值和返回值是实际的枚举对象，而不是字符串值：

    import enumplainplain
    from sqlalchemy import Table, MetaData, Column, Enum, create_engine


    class MyEnum(enum.Enum):
        one = "one"
        two = "two"
        three = "three"


    t = Table(
        'data', MetaData(),
        Column('value', Enum(MyEnum))
    )

    e = create_engine("sqlite://")
    t.create(e)

    e.execute(t.insert(), {"value": MyEnum.two})
    assert e.scalar(t.select()) is MyEnum.two

[＃3292 T0\>](http://www.sqlalchemy.org/trac/ticket/3292)

### Core结果行容纳的负整数索引[¶](#negative-integer-indexes-accommodated-by-core-result-rows "Permalink to this headline")

The [`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")
object now accomodates single negative integer indexes like a regular
Python sequence, both in the pure Python and C-extension version.
以前，负值只能在切片中使用：

    >>> from sqlalchemy import create_engineplain
    >>> e = create_engine("sqlite://")
    >>> row = e.execute("select 1, 2, 3").first()
    >>> row[-1], row[-2], row[1], row[-2:2]
    3 2 2 (2,)

### 现在，`Enum`类型对值进行了 Python 验证[¶](#the-enum-type-now-does-in-python-validation-of-values "Permalink to this headline")

为了适应 Python 本地枚举对象以及边缘情况，例如在 ARRAY 中使用非本地 ENUM 类型并且 CHECK 约束不可行的情况，现在[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")数据类型添加
- 使用[`Enum.validate_strings`](core_type_basics.html#sqlalchemy.types.Enum.params.validate_strings "sqlalchemy.types.Enum")标志时，输入值的Python验证（1.1.0b2）：

    >>> from sqlalchemy import Table, MetaData, Column, Enum, create_engine
    >>> t = Table(
    ...     'data', MetaData(),
    ...     Column('value', Enum("one", "two", "three", validate_strings=True))
    ... )
    >>> e = create_engine("sqlite://")
    >>> t.create(e)
    >>> e.execute(t.insert(), {"value": "four"})
    Traceback (most recent call last):
      ...
    sqlalchemy.exc.StatementError: (exceptions.LookupError)
    "four" is not among the defined enum values
    [SQL: u'INSERT INTO data (value) VALUES (?)']
    [parameters: [{'value': 'four'}]]

此验证在默认情况下处于关闭状态，因为已经存在用户不希望进行此类验证（例如字符串比较）的用例。对于非字符串类型，它必然发生在所有情况下。当返回来自数据库的值时，检查也无条件地发生在结果处理端。

此验证除了使用非本机枚举类型时创建CHECK约束的现有行为外。现在可以使用新的[`Enum.create_constraint`](core_type_basics.html#sqlalchemy.types.Enum.params.create_constraint "sqlalchemy.types.Enum")标志禁止创建此CHECK约束。

[＃3095 T0\>](http://www.sqlalchemy.org/trac/ticket/3095)

### 在所有情况下，非本地布尔整型值强制为零/一/无[¶](#non-native-boolean-integer-values-coerced-to-zero-one-none-in-all-cases "Permalink to this headline")

[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")数据类型将 Python 布尔值强制为不具有本机布尔类型的后端的整数值，例如 SQLite 和 MySQL。在这些后端上，通常会建立 CHECK 约束，以确保数据库中的值实际上是这两个值中的一个。但是，MySQL 会忽略 CHECK 约束，约束是可选的，并且现有数据库可能没有此约束。[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")数据类型已被修复，使得已经是整数值的传入 Python 端值被强制为 0 或 1，而不仅仅是按原样传递；另外，结果的 int-to-boolean 处理器的 C 扩展版本现在使用相同的 Python 布尔值解释，而不是断言一个确切的一个或零值。现在，这与纯 Python 的 int-to-boolean 处理器一致，并且更加宽容数据库中已存在的数据。None
/ NULL 的值与之前一样保留为 None / NULL。

[＃3730 T0\>](http://www.sqlalchemy.org/trac/ticket/3730)

### 大的参数和行值现在在日志和异常显示中被截断[¶](#large-parameter-and-row-values-are-now-truncated-in-logging-and-exception-displays "Permalink to this headline")

现在，在记录，异常报告以及`repr()`期间的显示期间，将截断作为 SQL 语句的绑定参数以及结果行中存在的大值的大值。该行本身：

    >>> from sqlalchemy import create_engineplainplain
    >>> import random
    >>> e = create_engine("sqlite://", echo='debug')
    >>> some_value = ''.join(chr(random.randint(52, 85)) for i in range(5000))
    >>> row = e.execute("select ?", [some_value]).first()
    ... (lines are wrapped for clarity) ...
    2016-02-17 13:23:03,027 INFO sqlalchemy.engine.base.Engine select ?
    2016-02-17 13:23:03,027 INFO sqlalchemy.engine.base.Engine
    ('E6@?>9HPOJB<<BHR:@=TS:5ILU=;JLM<4?B9<S48PTNG9>:=TSTLA;9K;9FPM4M8M@;NM6GU
    LUAEBT9QGHNHTHR5EP75@OER4?SKC;D:TFUMD:M>;C6U:JLM6R67GEK<A6@S@C@J7>4=4:P
    GJ7HQ6 ... (4702 characters truncated) ... J6IK546AJMB4N6S9L;;9AKI;=RJP
    HDSSOTNBUEEC9@Q:RCL:I@5?FO<9K>KJAGAO@E6@A7JI8O:J7B69T6<8;F:S;4BEIJS9HM
    K:;5OLPM@JR;R:J6<SOTTT=>Q>7T@I::OTDC:CC<=NGP6C>BC8N',)
    2016-02-17 13:23:03,027 DEBUG sqlalchemy.engine.base.Engine Col ('?',)
    2016-02-17 13:23:03,027 DEBUG sqlalchemy.engine.base.Engine
    Row (u'E6@?>9HPOJB<<BHR:@=TS:5ILU=;JLM<4?B9<S48PTNG9>:=TSTLA;9K;9FPM4M8M@;
    NM6GULUAEBT9QGHNHTHR5EP75@OER4?SKC;D:TFUMD:M>;C6U:JLM6R67GEK<A6@S@C@J7
    >4=4:PGJ7HQ ... (4703 characters truncated) ... J6IK546AJMB4N6S9L;;9AKI;=
    RJPHDSSOTNBUEEC9@Q:RCL:I@5?FO<9K>KJAGAO@E6@A7JI8O:J7B69T6<8;F:S;4BEIJS9HM
    K:;5OLPM@JR;R:J6<SOTTT=>Q>7T@I::OTDC:CC<=NGP6C>BC8N',)
    >>> print(row)
    (u'E6@?>9HPOJB<<BHR:@=TS:5ILU=;JLM<4?B9<S48PTNG9>:=TSTLA;9K;9FPM4M8M@;NM6
    GULUAEBT9QGHNHTHR5EP75@OER4?SKC;D:TFUMD:M>;C6U:JLM6R67GEK<A6@S@C@J7>4
    =4:PGJ7HQ ... (4703 characters truncated) ... J6IK546AJMB4N6S9L;;9AKI;
    =RJPHDSSOTNBUEEC9@Q:RCL:I@5?FO<9K>KJAGAO@E6@A7JI8O:J7B69T6<8;F:S;4BEIJS9H
    MK:;5OLPM@JR;R:J6<SOTTT=>Q>7T@I::OTDC:CC<=NGP6C>BC8N',)

[＃2837 T0\>](http://www.sqlalchemy.org/trac/ticket/2837)

### 具有 LIMIT / OFFSET / ORDER BY 的 UNION 或类似 SELECT 的选项现在将嵌入的选择符括起来[¶](#a-union-or-similar-of-selects-with-limit-offset-order-by-now-parenthesizes-the-embedded-selects "Permalink to this headline")

与其他人一样，SQLite 缺乏能力驱动的问题现在已得到增强，可用于所有支持的后端。我们引用的查询是 SELECT 语句的 UNION，它们本身包含行限制或排序功能，其中包括 LIMIT，OFFSET 和/或 ORDER
BY：

    (SELECT x FROM table1 ORDER BY y LIMIT 1) UNION
    (SELECT x FROM table2 ORDER BY y LIMIT 2)

上面的查询需要在每个子选择内部进行括号，以便正确地对子结果进行分组。在SQLAlchemy
Core中生成上述语句如下所示：

    stmt1 = select([table1.c.x]).order_by(table1.c.y).limit(1)
    stmt2 = select([table1.c.x]).order_by(table2.c.y).limit(2)

    stmt = union(stmt1, stmt2)

以前，上面的构造不会为内部 SELECT 语句产生括号，产生一个在所有后端都失败的查询。

The above formats will **continue to fail on SQLite**; additionally, the
format that includes ORDER BY but no LIMIT/SELECT will **continue to
fail on Oracle**.
这不是一个向后不兼容的更改，因为查询失败时没有括号；通过修复，查询至少可以在所有其他数据库上工作。

在所有情况下，为了生成一个有限的 SELECT 语句的 UNION，它也适用于 SQLite，并且在所有情况下都适用于 Oracle，子查询必须是 ALIAS 的 SELECT：

    stmt1 = select([table1.c.x]).order_by(table1.c.y).limit(1).alias().select()
    stmt2 = select([table2.c.x]).order_by(table2.c.y).limit(2).alias().select()

    stmt = union(stmt1, stmt2)

此解决方法适用于所有SQLAlchemy版本。在ORM中，它看起来像：

    stmt1 = session.query(Model1).order_by(Model1.y).limit(1).subquery().select()
    stmt2 = session.query(Model2).order_by(Model2.y).limit(1).subquery().select()

    stmt = session.query(Model1).from_statement(stmt1.union(stmt2))

这里的行为有许多类似于在[Many JOIN and LEFT OUTER JOIN expressions will
no longer be wrapped in (SELECT \* FROM ..) AS
ANON\_1](migration_09.html#feature-joins-09)中；但是在这种情况下，我们选择不添加新的重写行为来适应 SQLite 的这种情况。现有的重写行为已经非常复杂了，而使用括号化 SELECT 语句的 UNION 的情况比那个特性的“右嵌套连接”用例要少得多。

[＃2528 T0\>](http://www.sqlalchemy.org/trac/ticket/2528)

### 对Core [¶](#json-support-added-to-core "Permalink to this headline")添加了 JSON 支持

由于 MySQL 现在除了 Postgresql
JSON 数据类型之外还有一个 JSON 数据类型，所以现在内核获得了一个[`sqlalchemy.types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")数据类型，它们是这两个数据类型的基础。使用这种类型允许以对 Postgresql 和 MySQL 不可知的方式访问“getitem”运算符以及“getpath”运算符。

新的数据类型还对NULL值的处理以及表达式处理进行了一系列改进。

也可以看看

[MySQL JSON Support](#change-3547)

[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")

[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")

[`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")

[＃3619 T0\>](http://www.sqlalchemy.org/trac/ticket/3619)

#### JSON“null”按预期插入 ORM 操作，而不管列默认存在[¶](#json-null-is-inserted-as-expected-with-orm-operations-regardless-of-column-default-present "Permalink to this headline")

The [`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")
type and its descendant types [`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
and [`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")
have a flag [`types.JSON.none_as_null`](core_type_basics.html#sqlalchemy.types.JSON.params.none_as_null "sqlalchemy.types.JSON")
which when set to True indicates that the Python value `None` should translate into a SQL NULL rather than a JSON NULL
value. This flag defaults to False, which means that the column should
*never* insert SQL NULL or fall back to a default unless the
[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")
constant were used.
但是，在两种情况下，ORM可能会失败；一种是当列中还包含default或server\_default值时，映射属性上的正值`None`仍然会导致列级别的默认值被触发，替换`None`

    obj = MyObject(json_value=None)plainplain
    session.add(obj)
    session.commit()   # would fire off default / server_default, not encode "'none'"

The other is when the [`Session.bulk_insert_mappings()`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")
method were used, `None` would be ignored in all
cases:

    session.bulk_insert_mappings(
        MyObject,
        [{"json_value": None}])  # would insert SQL NULL and/or trigger defaults

[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型现在实现了[`TypeEngine.should_evaluate_none`](core_type_api.html#sqlalchemy.types.TypeEngine.should_evaluate_none "sqlalchemy.types.TypeEngine.should_evaluate_none")标志，表示`None`在这里不应忽略；它会根据[`types.JSON.none_as_null`(core_type_basics.html#sqlalchemy.types.JSON.params.none_as_null "sqlalchemy.types.JSON")的值自动进行配置。感谢[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)，我们可以区分何时值`None`由用户主动设置，而不是根本不设置。

如果该属性根本没有设置，那么列级别的默认值*将*触发并且/或者SQL
NULL按预期插入，就像以前的行为一样。下面说明两个变体：

    obj = MyObject(json_value=None)
    session.add(obj)
    session.commit()   # *will not* fire off column defaults, will insert JSON 'null'

    obj = MyObject()
    session.add(obj)
    session.commit()   # *will* fire off column defaults, and/or insert SQL NULL

该功能也适用于新的基础[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型及其后代类型。

[＃3514 T0\>](http://www.sqlalchemy.org/trac/ticket/3514)

#### 新的 JSON.NULL 常量已添加[¶](#new-json-null-constant-added "Permalink to this headline")

为了确保应用程序始终能够完全控制[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")，[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")，[`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")的值级别，或[`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")列应该接收到SQL
NULL或JSON `"null"`值时，常量[`types.JSON.NULL`](core_type_basics.html#sqlalchemy.types.JSON.NULL "sqlalchemy.types.JSON.NULL")已被添加，与[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")结合使用可以完全确定 SQL
NULL 和 JSON `"null"`之间的关系，无论[`types.JSON.none_as_null`(core_type_basics.html#sqlalchemy.types.JSON.params.none_as_null "sqlalchemy.types.JSON")被设定为：

    from sqlalchemy import null
    from sqlalchemy.dialects.postgresql import JSON

    obj1 = MyObject(json_value=null())  # will *always* insert SQL NULL
    obj2 = MyObject(json_value=JSON.NULL)  # will *always* insert JSON string "null"

    session.add_all([obj1, obj2])
    session.commit()

该功能也适用于新的基础[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型及其后代类型。

[＃3514 T0\>](http://www.sqlalchemy.org/trac/ticket/3514)

### 阵列支持添加到核心；新的 ANY 和所有运算符[¶](#array-support-added-to-core-new-any-and-all-operators "Permalink to this headline")

Along with the enhancements made to the Postgresql
[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
type described in [Correct SQL Types are Established from Indexed Access
of ARRAY, JSON, HSTORE](#change-3503), the base class of
[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
itself has been moved to Core in a new class [`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY").

数组是 SQL 标准的一部分，也有几个面向数组的函数，如`array_agg()`和`unnest()`。为了支持这些结构不仅适用于 PostgreSQL，而且还适用于未来其他具有阵列能力的后端，例如 DB2，SQL 表达式的大部分数组逻辑现在位于 Core 中。[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型still
**仅适用于 Postgresql**，但它可以直接使用，支持特殊的数组用例，例如索引访问，以及支持ANY和所有：

    mytable = Table("mytable", metadata,
            Column("data", ARRAY(Integer, dimensions=2))
        )

    expr = mytable.c.data[5][6]

    expr = mytable.c.data[5].any(12)

In support of ANY and ALL, the [`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")
type retains the same [`types.ARRAY.Comparator.any()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.any "sqlalchemy.types.ARRAY.Comparator.any")
and [`types.ARRAY.Comparator.all()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.all "sqlalchemy.types.ARRAY.Comparator.all")
methods from the PostgreSQL type, but also exports these operations to
new standalone operator functions [`sql.expression.any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")
and [`sql.expression.all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_").
这两个函数以更传统的SQL方式工作，允许使用右侧表达形式，如：

    from sqlalchemy import any_, all_

    select([mytable]).where(12 == any_(mytable.c.data[5]))

对于特定于 PostgreSQL 的运算符“contains”，“contained\_by”和“overlapps”，应该继续直接使用[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型，它提供了[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型。

[`sql.expression.any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")和[`sql.expression.all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")运算符在Core级别是开放式的，但是它们对后端数据库的解释是有限的。在Postgresql后端，两个运算符**只接受数组值**。而在MySQL后端，它们**只接受子查询值**。在 MySQL 上，可以使用如下表达式：

    from sqlalchemy import any_, all_

    subq = select([mytable.c.value])
    select([mytable]).where(12 > any_(subq))

[＃3516 T0\>](http://www.sqlalchemy.org/trac/ticket/3516)

### 新函数功能，“WITHIN GROUP”，array\_agg 和集合函数[¶](#new-function-features-within-group-array-agg-and-set-aggregate-functions "Permalink to this headline")

使用新的[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型，我们还可以为返回数组的`array_agg()`
SQL函数实现预先键入的函数，该函数现在可以使用[`array_agg`](core_functions.html#sqlalchemy.sql.functions.array_agg "sqlalchemy.sql.functions.array_agg")

    from sqlalchemy import func
    stmt = select([func.array_agg(table.c.value)])

用于聚合ORDER
BY的Postgresql元素也通过[`postgresql.aggregate_order_by`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by "sqlalchemy.dialects.postgresql.aggregate_order_by")添加：

    from sqlalchemy.dialects.postgresql import aggregate_order_byplain
    expr = func.array_agg(aggregate_order_by(table.c.a, table.c.b.desc()))
    stmt = select([expr])

生产：

    SELECT array_agg(table1.a ORDER BY table1.b DESC) AS array_agg_1 FROM table1plain

PG方言本身也提供一个[`postgresql.array_agg()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array_agg "sqlalchemy.dialects.postgresql.array_agg")包装来确保[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型：

    from sqlalchemy.dialects.postgresql import array_agg
    stmt = select([array_agg(table.c.value).contains('foo')])

Additionally, functions like `percentile_cont()`,
`percentile_disc()`, `rank()`,
`dense_rank()` and others that require an ordering
via `WITHIN GROUP (ORDER BY <expr>)` are now
available via the [`FunctionElement.within_group()`](core_functions.html#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")
modifier:

    from sqlalchemy import funcplain
    stmt = select([
        department.c.id,
        func.percentile_cont(0.5).within_group(
            department.c.salary.desc()
        )
    ])

上面的语句会产生 SQL 类似于：

    SELECT department.id, percentile_cont(0.5)
    WITHIN GROUP (ORDER BY department.salary DESC)

现在为这些函数提供了正确返回类型的占位符，它们包括[`percentile_cont`](core_functions.html#sqlalchemy.sql.functions.percentile_cont "sqlalchemy.sql.functions.percentile_cont")，[`percentile_disc`](core_functions.html#sqlalchemy.sql.functions.percentile_disc "sqlalchemy.sql.functions.percentile_disc")，[`rank`](core_functions.html#sqlalchemy.sql.functions.rank "sqlalchemy.sql.functions.rank")，[`dense_rank`](core_functions.html#sqlalchemy.sql.functions.dense_rank "sqlalchemy.sql.functions.dense_rank")
[`mode`](core_functions.html#sqlalchemy.sql.functions.mode "sqlalchemy.sql.functions.mode")，[`percent_rank`](core_functions.html#sqlalchemy.sql.functions.percent_rank "sqlalchemy.sql.functions.percent_rank")和[`cume_dist`](core_functions.html#sqlalchemy.sql.functions.cume_dist "sqlalchemy.sql.functions.cume_dist")。

[＃3132](http://www.sqlalchemy.org/trac/ticket/3132)
[＃1370](http://www.sqlalchemy.org/trac/ticket/1370)

### TypeDecorator现在自动使用Enum，Boolean和“模式”类型[¶](#typedecorator-now-works-with-enum-boolean-schema-types-automatically "Permalink to this headline")

[`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")类型包括[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")和[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")等类型，除了与数据库类型相对应外，还会生成CHECK约束或Postgresql
ENUM一个新的CREATE TYPE语句的情况下，现在将自动与[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")配方一起工作。以前，[`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")的[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")必须如下所示：

    # old way
    class MyEnum(TypeDecorator, SchemaType):
        impl = postgresql.ENUM('one', 'two', 'three', name='myenum')

        def _set_table(self, table):
            self.impl._set_table(table)

现在，[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")传播这些附加事件，因此可以像其他类型那样完成：

    # new way
    class MyEnum(TypeDecorator):
        impl = postgresql.ENUM('one', 'two', 'three', name='myenum')

[＃2919 T0\>](http://www.sqlalchemy.org/trac/ticket/2919)

### 表对象的多租户模式转换[¶](#multi-tenancy-schema-translation-for-table-objects "Permalink to this headline")

为了支持在许多模式中使用同一组[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的应用程序的用例，例如schema-per-user，新的执行选项[`Connection.execution_options.schema_translate_map`](core_connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map "sqlalchemy.engine.Connection.execution_options")使用这种映射，可以在每个连接的基础上创建一组[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象来引用任何一组模式，而不是指定它们的[`Table.schema`](core_metadata.html#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")
。该翻译适用于 DDL 和 SQL 生成以及 ORM。

例如，如果`User`类分配了架构“per\_user”：

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)

        __table_args__ = {'schema': 'per_user'}

在每次请求时，[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以设置为每次引用不同的模式：

    session = Session()
    session.connection(execution_options={
        "schema_translate_map": {"per_user": "account_one"}})

    # will query from the ``account_one.user`` table
    session.query(User).get(5)

也可以看看

[Translation of Schema Names](core_connections.html#schema-translating)

[＃2685 T0\>](http://www.sqlalchemy.org/trac/ticket/2685)

### “友好”的核心SQL结构的字符串化，没有方言[¶](#friendly-stringification-of-core-sql-constructs-without-a-dialect "Permalink to this headline")

在 Core SQL 构造上调用`str()`现在会在比以前更多的情况下生成一个字符串，支持默认 SQL 中通常不存在的各种 SQL 构造，例如 RETURNING，数组索引和非标准数据类型：

    >>> from sqlalchemy import table, column
    t>>> t = table('x', column('a'), column('b'))
    >>> print(t.insert().returning(t.c.a, t.c.b))
    INSERT INTO x (a, b) VALUES (:a, :b) RETURNING x.a, x.b

现在，`str()`函数调用一个完全独立的方言/编译器，仅用于纯字符串打印而不设置特定的方言，因此更多的“只显示一个字符串！可以添加到这个方言/编译器，而不会影响真正方言的行为。

也可以看看

[Stringify of Query will consult the Session for the correct
dialect](#change-3081)

[＃3631 T0\>](http://www.sqlalchemy.org/trac/ticket/3631)

### type\_coerce函数现在是一个持久化的SQL元素[¶](#the-type-coerce-function-is-now-a-persistent-sql-element "Permalink to this headline")

根据输入，以前的[`expression.type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")函数会返回一个类型为[`BindParameter`](core_sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")或[`Label`](core_sqlelement.html#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")的对象。这将会产生的效果是，在使用表达式转换的情况下，例如将元素从[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")转换为[`BindParameter`](core_sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")，这对于ORM级懒惰至关重要加载时，类型强制信息将不会被使用，因为它已经丢失了。

为了改善这种行为，函数现在返回一个持续的[`TypeCoerce`](core_sqlelement.html#sqlalchemy.sql.expression.TypeCoerce "sqlalchemy.sql.expression.TypeCoerce")容器，该容器围绕给定的表达式，它本身不受影响；此构造由 SQL 编译器明确评估。这允许保持内部表达式的强制，而不管语句如何被修改，包括如果包含的元素被替换为不同的元素，就像 ORM 的延迟加载特性中常见的那样。

说明该效果的测试用例使用了一种异构的 primaryjoin 条件，并结合自定义类型和延迟加载。给定一个将 CAST 用作“绑定表达式”的自定义类型：

    class StringAsInt(TypeDecorator):plain
        impl = String

        def column_expression(self, col):
            return cast(col, Integer)

        def bind_expression(self, value):
            return cast(value, String)

然后，我们将一个表上的字符串“id”列与另一个表上的整数“id”列相等的映射：

    class Person(Base):plain
        __tablename__ = 'person'
        id = Column(StringAsInt, primary_key=True)

        pets = relationship(
            'Pets',
            primaryjoin=(
                'foreign(Pets.person_id)'
                '==cast(type_coerce(Person.id, Integer), Integer)'
            )
        )

    class Pets(Base):
        __tablename__ = 'pets'
        id = Column('id', Integer, primary_key=True)
        person_id = Column('person_id', Integer)

在[`relationship.primaryjoin`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")表达式中，我们使用[`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")来处理通过 lazyloading 传递的绑定参数作为整数，因为我们已经知道这些参数将来自`StringAsInt`类型，它在Python中将值保持为整数。然后我们使用[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")，因此作为 SQL 表达式，VARCHAR“id”列将被 CAST 为常规未转换连接的整数，如同[`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")或[`orm.joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")。也就是说，`.pets`的连接加载看起来像：

    SELECT person.id AS person_id, pets_1.id AS pets_1_id,
           pets_1.person_id AS pets_1_person_id
    FROM person
    LEFT OUTER JOIN pets AS pets_1
    ON pets_1.person_id = CAST(person.id AS INTEGER)

没有联接的ON子句中的CAST，强类型数据库（如Postgresql）将拒绝隐式比较整数和失败。

`.pets`的lazyload情况依赖于在加载时用一个绑定参数替换`Person.id`列，该绑定参数接收一个Python加载的值。这种替换特别适用于我们的[`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")函数的意图会丢失的地方。在更改之前，这个懒惰负载如下所示：

    SELECT pets.id AS pets_id, pets.person_id AS pets_person_id
    FROM pets
    WHERE pets.person_id = CAST(CAST(%(param_1)s AS VARCHAR) AS INTEGER)
    {'param_1': 5}

在上面的例子中，我们看到我们的 Python in-value 值是`5`，先是 CAST 到 VARCHAR，然后返回到 SQL 中的 INTEGER；一个可以工作的双重 CAST，但并不是我们所要求的。

随着更改，即使在将列换出为绑定参数之后，[`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")函数也会维护一个包装，现在查询如下所示：

    SELECT pets.id AS pets_id, pets.person_id AS pets_person_idplain
    FROM pets
    WHERE pets.person_id = CAST(%(param_1)s AS INTEGER)
    {'param_1': 5}

在我们的主要联接中的外部CAST仍然生效的情况下，根据[`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")函数的意图删除了在`StringAsInt`定制类型的一部分中的不必要的CAST。

[＃3531 T0\>](http://www.sqlalchemy.org/trac/ticket/3531)

关键行为改变 - ORM [¶](#key-behavioral-changes-orm "Permalink to this headline")
--------------------------------------------------------------------------------

关键行为改变 - 核心[¶](#key-behavioral-changes-core "Permalink to this headline")
---------------------------------------------------------------------------------

### 当位置通过时，TextClause.columns()将按位置匹配列，而不是按名称匹配[¶](#textclause-columns-will-match-columns-positionally-not-by-name-when-passed-positionally "Permalink to this headline")

[`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法的新行为本身最近在 0.9 系列中添加时，是当列位置传递时没有任何其他关键字参数时，它们被链接到最终结果设置列的位置，并不再名称。希望这种改变的影响很小，因为这个方法总是被记录下来，说明按照与文本 SQL 语句相同的顺序传递的列，这看起来很直观，即使内部结构没有不检查这个。

通过将[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象传递给它的位置的应用程序必须确保这些[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的位置与文本SQL中这些列的位置匹配。

例如，代码如下：

    stmt = text("SELECT id, name, description FROM table")plain

    # no longer matches by name
    stmt = stmt.columns(my_table.c.name, my_table.c.description, my_table.c.id)

将不再按预期工作；现在给出的列的顺序是重要的：

    # correct version
    stmt = stmt.columns(my_table.c.id, my_table.c.name, my_table.c.description)

可能更有可能的是，这样的陈述：

    stmt = text("SELECT * FROM table")plain
    stmt = stmt.columns(my_table.c.id, my_table.c.name, my_table.c.description)

现在有点冒险，因为“\*”规范通常会按照它们出现在表中的顺序传递列。如果表的结构因模式更改而发生更改，则此排序可能不再相同。因此，在使用[`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")时，建议在文本 SQL 中明确列出所需的列，但不必再担心文本 SQL 中的名称本身。

也可以看看

[ResultSet column matching enhancements; positional column setup for
textual SQL](#change-3501)

方言的改进和变化 - Postgresql [¶](#dialect-improvements-and-changes-postgresql "Permalink to this headline")
------------------------------------------------------------------------------------------------------------

### 支持 INSERT..ON CONFLICT（DO UPDATE | DO NOTHING）[¶](#support-for-insert-on-conflict-do-update-do-nothing "Permalink to this headline")

The `ON CONFLICT` clause of `INSERT` added to Postgresql as of version 9.5 is now supported using a
Postgresql-specific version of the [`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
object, via [`sqlalchemy.dialects.postgresql.dml.insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert").
This [`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
subclass adds two new methods [`Insert.on_conflict_do_update()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")
and [`Insert.on_conflict_do_nothing()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing")
which implement the full syntax supported by Posgresql 9.5 in this area:

    from sqlalchemy.dialects.postgresql import insert

    insert_stmt = insert(my_table). \\
        values(id='some_id', data='some data to insert')

    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=[my_table.c.id],
        set_=dict(data='some data to update')
    )

    conn.execute(do_update_stmt)

以上将呈现：

    INSERT INTO my_table (id, data)
    VALUES (:id, :data)
    ON CONFLICT id DO UPDATE SET data=:data_2

也可以看看

[INSERT...ON CONFLICT
(Upsert)](dialects_postgresql.html#postgresql-insert-on-conflict)

[＃3529 T0\>](http://www.sqlalchemy.org/trac/ticket/3529)

### ARRAY和JSON类型现在可以正确指定“不可用”[¶](#array-and-json-types-now-correctly-specify-unhashable "Permalink to this headline")

如[Changes regarding “unhashable”
types](#change-3499)中所述，当查询的选定实体将完整的 ORM 实体与列表达式混合时，ORM 依赖于能够为列值生成散列函数。`hashable=False`标志现在可以在所有 PG 的“数据结构”类型中正确设置，包括[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")和[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")。[`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")和[`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")类型已包含此标志。对于[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")，这是基于[`postgresql.ARRAY.as_tuple`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.params.as_tuple "sqlalchemy.dialects.postgresql.ARRAY")标志的条件，但是不应该再设置该标志来获得数组值存在于组成的ORM行中。

也可以看看

[Changes regarding “unhashable” types](#change-3499)

[Correct SQL Types are Established from Indexed Access of ARRAY, JSON,
HSTORE](#change-3503)

[＃3499 T0\>](http://www.sqlalchemy.org/trac/ticket/3499)

### 通过对ARRAY，JSON，HSTORE的索引访问建立正确的SQL类型[¶](#correct-sql-types-are-established-from-indexed-access-of-array-json-hstore "Permalink to this headline")

For all three of [`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY"),
[`JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
and [`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE"),
the SQL type assigned to the expression returned by indexed access, e.g.
`col[someindex]`, should be correct in all cases.

这包括：

-   分配给[`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")的索引访问的SQL类型考虑了配置的维数。具有三个维度的[`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")将返回一个具有少于一个维度的[`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型的 SQL 表达式。给定一个类型为`ARRAY（Integer， dimensions = 3）`的列，我们现在可以执行下面的表达式：

        int_expr = col[5][6][7]   # returns an Integer expression object

    以前，对`col[5]`的索引访问将返回一个类型为[`Integer`](core_type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")的表达式，我们不能再为其余维度执行索引访问，除非我们使用[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")或[`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")。

-   现在，[`JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")和[`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")类型反映了 Postgresql 本身为索引访问所做的工作。This
    means that all indexed access for a [`JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
    or [`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")
    type returns an expression that itself is *always* [`JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
    or [`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")
    itself, unless the [`astext`{](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")
    modifier is used.
    这意味着无论JSON结构的索引访问最终是指字符串，列表，数字还是其他JSON结构，Postgresql始终认为它本身是JSON，除非它明确地被转换为不同的形式。像[`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型一样，这意味着现在可以直接生成具有多级索引访问的 JSON 表达式：

        json_expr = json_col['key1']['attr1'][5]

-   The “textual” type that is returned by indexed access of
    [`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")
    as well as the “textual” type that is returned by indexed access of
    [`JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
    and [`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")
    in conjunction with the [`astext`{](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")
    modifier is now configurable; it defaults to [`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")
    in both cases but can be set to a user-defined type using the
    [`postgresql.JSON.astext_type`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.params.astext_type "sqlalchemy.dialects.postgresql.JSON")
    or [`postgresql.HSTORE.text_type`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE.params.text_type "sqlalchemy.dialects.postgresql.HSTORE")
    parameters.

也可以看看

[The JSON cast() operation now requires .astext is called
explicitly](#change-3503-cast)

[＃3499](http://www.sqlalchemy.org/trac/ticket/3499)
[＃3487](http://www.sqlalchemy.org/trac/ticket/3487)

### JSON cast()操作现在需要`.astext`被显式调用[¶](#the-json-cast-operation-now-requires-astext-is-called-explicitly "Permalink to this headline")

As part of the changes in [Correct SQL Types are Established from
Indexed Access of ARRAY, JSON, HSTORE](#change-3503), the workings of
the [`ColumnElement.cast()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")
operator on [`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
and [`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")
no longer implictly invoke the
[`postgresql.JSON.Comparator.astext`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")
modifier; Postgresql’s JSON/JSONB types support CAST operations to each
other without the “astext” aspect.

这意味着在大多数情况下，这样做的应用程序：

    expr = json_col['somekey'].cast(Integer)plain

现在需要改变为：

    expr = json_col['somekey'].astext.cast(Integer)

### 带有 ENUM 的 ARRAY 现在会为 ENUM [¶](#array-with-enum-will-now-emit-create-type-for-the-enum "Permalink to this headline")发出CREATE TYPE

像下面这样的表定义现在将按照预期发出CREATE TYPE：

    enum = Enum(
        'manager', 'place_admin', 'carwash_admin',
        'parking_admin', 'service_admin', 'tire_admin',
        'mechanic', 'carwasher', 'tire_mechanic', name="work_place_roles")

    class WorkPlacement(Base):
        __tablename__ = 'work_placement'
        id = Column(Integer, primary_key=True)
        roles = Column(ARRAY(enum))


    e = create_engine("postgresql://scott:tiger@localhost/test", echo=True)
    Base.metadata.create_all(e)

发出：

    CREATE TYPE work_place_roles AS ENUM (plainplain
        'manager', 'place_admin', 'carwash_admin', 'parking_admin',
        'service_admin', 'tire_admin', 'mechanic', 'carwasher',
        'tire_mechanic')

    CREATE TABLE work_placement (
        id SERIAL NOT NULL,
        roles work_place_roles[],
        PRIMARY KEY (id)
    )

[＃2729 T0\>](http://www.sqlalchemy.org/trac/ticket/2729)

### 检查约束现在反映[¶](#check-constraints-now-reflect "Permalink to this headline")

Postgresql 方言现在支持在方法[`Inspector.get_check_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints "sqlalchemy.engine.reflection.Inspector.get_check_constraints")以及`Table.constraints`内的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")反射内反映 CHECK 约束。采集。

### “Plain”和“Materialized”视图可以单独检查[¶](#plain-and-materialized-views-can-be-inspected-separately "Permalink to this headline")

新参数[`PGInspector.get_view_names.include`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names.params.include "sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names")允许指定应返回哪些视图的子类型：

    from sqlalchemy import inspectplain
    insp = inspect(engine)

    plain_views = insp.get_view_names(include='plain')
    all_views = insp.get_view_names(include=('plain', 'materialized'))

[＃3588 T0\>](http://www.sqlalchemy.org/trac/ticket/3588)

### 索引[¶](#added-tablespace-option-to-index "Permalink to this headline")增加了表空间选项

为了指定TABLESPACE，[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象现在接受参数`postgresql_tablespace`，这与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象接受的方式相同。

也可以看看

[Index Storage
Parameters](dialects_postgresql.html#postgresql-index-storage)

[＃3720 T0\>](http://www.sqlalchemy.org/trac/ticket/3720)

### 支持 PyGreSQL [¶](#support-for-pygresql "Permalink to this headline")

现在支持[PyGreSQL](https://pypi.python.org/pypi/PyGreSQL) DBAPI。

也可以看看

[pygresql](dialects_postgresql.html#dialect-postgresql-pygresql)

### “postgres”模块被删除[¶](#the-postgres-module-is-removed "Permalink to this headline")

长期弃用的`sqlalchemy.dialects.postgres`模块将被删除；这已经发出了多年的警告，并且项目应该调用`sqlalchemy.dialects.postgresql`。然而，形式为`postgres://`的引擎网址仍然可以继续使用。

### 支持FOR UPDATE SKIP LOCKED /无密钥更新/用于密钥共享[¶](#support-for-for-update-skip-locked-for-no-key-update-for-key-share "Permalink to this headline")

Core 和 ORM 中的新参数[`GenerativeSelect.with_for_update.skip_locked`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")和[`GenerativeSelect.with_for_update.key_share`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.key_share "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")对“SELECT
... FOR UPDATE”或“SELECT”进行修改。 ..FOR SHARE“查询Postgresql后端：

-   选择无钥匙更新：

        stmt = select([table]).with_for_update(key_share=True)

-   SELECT FOR UPDATE SKIP LOCKED：

        stmt = select([table]).with_for_update(skip_locked=True)

-   选择关键共享：

        stmt = select([table]).with_for_update(read=True, key_share=True)

方言的改进和改变 - MySQL [¶](#dialect-improvements-and-changes-mysql "Permalink to this headline")
--------------------------------------------------------------------------------------------------

### MySQL JSON支持[¶](#mysql-json-support "Permalink to this headline")

一个新类型的[`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")被添加到支持新添加到 MySQL
5.7 的 JSON 类型的 MySQL 方言中。该类型在内部使用`JSON_EXTRACT`函数提供 JSON 的持久性以及基本的索引访问。通过使用 MySQL 和 Postgresql 共同的[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")数据类型，可以实现跨 MySQL 和 Postgresql 的可索引 JSON 列。

也可以看看

[JSON support added to Core](#change-3619)

[＃3547 T0\>](http://www.sqlalchemy.org/trac/ticket/3547)

### 增加了对AUTOCOMMIT“隔离级别”的支持[¶](#added-support-for-autocommit-isolation-level "Permalink to this headline")

The MySQL dialect now accepts the value “AUTOCOMMIT” for the
[`create_engine.isolation_level`](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")
and [`Connection.execution_options.isolation_level`(core_connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")
parameters:

    connection = engine.connect()
    connection = connection.execution_options(
        isolation_level="AUTOCOMMIT"
    )

隔离级别利用了大多数MySQL DBAPI提供的各种“自动提交”属性。

[＃3332 T0\>](http://www.sqlalchemy.org/trac/ticket/3332)

### 不再为复合主键生成隐式 KEY w / AUTO\_INCREMENT [¶](#no-more-generation-of-an-implicit-key-for-composite-primary-key-w-auto-increment "Permalink to this headline")

MySQL 方言具有这样的行为，如果 InnoDB 表上的组合主键在不是第一列的列之一上具有 AUTO\_INCREMENT，例如：

    t = Table(plain
        'some_table', metadata,
        Column('x', Integer, primary_key=True, autoincrement=False),
        Column('y', Integer, primary_key=True, autoincrement=True),
        mysql_engine='InnoDB'
    )

将生成如下的DDL：

    CREATE TABLE some_table (
        x INTEGER NOT NULL,
        y INTEGER NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (x, y),
        KEY idx_autoinc_y (y)
    )ENGINE=InnoDB

注意上面带有自动生成名称的“KEY”；这是多年前在方言中发现的一个变化，以回应AUTO\_INCREMENT 在没有这个额外 KEY 的情况下会在 InnoDB 上失败的问题。

这种解决方法已被删除，并替换为仅在主键中声明AUTO\_INCREMENT列*first*的更好系统：

    CREATE TABLE some_table (plain
        x INTEGER NOT NULL,
        y INTEGER NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (y, x)
    )ENGINE=InnoDB

为了明确控制主键列的排序，显式地使用[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")结构（1.1.0b2）（以及 MySQL 要求的自动增量列的 KEY），例如：

    t = Table(
        'some_table', metadata,
        Column('x', Integer, primary_key=True),
        Column('y', Integer, primary_key=True, autoincrement=True),
        PrimaryKeyConstraint('x', 'y'),
        UniqueConstraint('y'),
        mysql_engine='InnoDB'
    )

随着[The .autoincrement directive is no longer implicitly enabled for a
composite primary key
column](#change-3216)不再为组合主键列隐式启用.autoincrement 指令，现在更容易指定具有或不具有自动增量的组合主键；
[`Column.autoincrement`](core_metadata.html#sqlalchemy.schema.Column.params.autoincrement "sqlalchemy.schema.Column")现在默认为`"auto"`值，并且不再需要`autoincrement=False`指令：

    t = Table(
        'some_table', metadata,
        Column('x', Integer, primary_key=True),
        Column('y', Integer, primary_key=True, autoincrement=True),
        mysql_engine='InnoDB'
    )

方言的改进和改变 - SQLite [¶](#dialect-improvements-and-changes-sqlite "Permalink to this headline")
----------------------------------------------------------------------------------------------------

### 为 SQLite 3.7.16 版本提供了右嵌套连接解决方​​法[¶](#right-nested-join-workaround-lifted-for-sqlite-version-3-7-16 "Permalink to this headline")

在0.9版本中，由[Many JOIN and LEFT OUTER JOIN expressions will no longer
be wrapped in (SELECT \* FROM ..) AS
ANON\_1](migration_09.html#feature-joins-09)Ironically, the version of
SQLite noted in that migration note, 3.7.15.2, was the *last* version of
SQLite to actually have this limitation!
下一个版本是 3.7.16，并且正确地添加了对正确的嵌套连接的支持。在 1.1 中，确定进行此更改的特定 SQLite 版本和源提交的工作已完成（SQlite 的更改日志中引用了隐含短语“增强查询优化器利用传递连接约束”，而不链接到任何问题编号，更改数字或进一步解释），并且当 DBAPI 报告 3.7.16 版或更高版本生效时，此更改中提供的解决方法现已解除。

[＃3634 T0\>](http://www.sqlalchemy.org/trac/ticket/3634)

### 为 SQLite 版本 3.10.0 解决了虚线列名解决方法[¶](#dotted-column-names-workaround-lifted-for-sqlite-version-3-10-0 "Permalink to this headline")

对于数据库驱动程序不报告某些 SQL 结果集的正确列名的问题，特别是在使用 UNION 时，SQLite 方言早就有了一个解决方法。解决方法详见[Dotted
Column
Names](dialects_sqlite.html#sqlite-dotted-column-names)，并要求SQLAlchemy假定任何带有点的列名实际上都是通过此错误行为提供的`tablename.columnname`组合，可以通过`sqlite_raw_colnames`执行选项将其关闭。

从 SQLite 版本 3.10.0 开始，UNION 和其他查询中的 bug 已经修复；就像[Right-nested
join workaround lifted for SQLite version
3.7.16](#change-3634)中描述的更改一样，SQLite 的更改日志仅将其隐含地标识为“添加了 sqlite3\_index\_info 的 colUsed 字段以供 sqlite3\_module.xBestIndex 方法使用”，但是此版本不再需要 SQLAlchemy 对这些虚线列名的翻译，因此在检测到 3.10.0 或更高版本时关闭。

总体而言，从 1.0 系列开始，SQLAlchemy [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")在为 Core 和 ORM
SQL 结构提供结果时，对结果集中的列名的依赖要少得多，因此在任何情况下，此问题的重要性都已减轻。

[＃3633 T0\>](http://www.sqlalchemy.org/trac/ticket/3633)

### 改进了对远程模式的支持[¶](#improved-support-for-remote-schemas "Permalink to this headline")

The SQLite dialect now implements [`Inspector.get_schema_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_schema_names "sqlalchemy.engine.reflection.Inspector.get_schema_names")
and additionally has improved support for tables and indexes that are
created and reflected from a remote schema, which in SQLite is a dataase
that is assigned a name via the `ATTACH` statement;
previously, the\`\`CREATE INDEX\`\` DDL didn’t work correctly for a
schema-bound table and the [`Inspector.get_foreign_keys()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_foreign_keys "sqlalchemy.engine.reflection.Inspector.get_foreign_keys")
method will now indicate the given schema in the results.
不支持跨模式外键。

### PRIMARY KEY 约束名称的反映[¶](#reflection-of-the-name-of-primary-key-constraints "Permalink to this headline")

SQLite 后端现在利用 SQLite 的“sqlite\_master”视图来从原始 DDL 中提取表的主键约束的名称，与最近 SQLAlchemy 版本中的外键约束所实现的方式相同。

[＃3629 T0\>](http://www.sqlalchemy.org/trac/ticket/3629)

### 检查约束现在反映[¶](#id1 "Permalink to this headline")

SQLite方言现在支持在`Table.constraints`内的方法[`Inspector.get_check_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints "sqlalchemy.engine.reflection.Inspector.get_check_constraints")以及[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")反射内反映 CHECK 约束。采集。

### ON DELETE和ON UPDATE外键关键短语现在反映[¶](#on-delete-and-on-update-foreign-key-phrases-now-reflect "Permalink to this headline")

The [`Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")
will now include ON DELETE and ON UPDATE phrases from foreign key
constraints on the SQLite dialect, and the [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
object as reflected as part of a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
will also indicate these phrases.

方言的改进和改变 - SQL Server [¶](#dialect-improvements-and-changes-sql-server "Permalink to this headline")
------------------------------------------------------------------------------------------------------------

### 增加了SQL Server [¶](#added-transaction-isolation-level-support-for-sql-server "Permalink to this headline")的事务隔离级别支持

所有SQL Server方言都通过[`create_engine.isolation_level`(core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")和[`Connection.execution_options.isolation_level`](core_connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")参数支持事务隔离级别设置。支持四种标准级别以及`SNAPSHOT`：

    engine = create_engine(plain
        "mssql+pyodbc://scott:tiger@ms_2008",
        isolation_level="REPEATABLE READ"
    )

也可以看看

[Transaction Isolation Level](dialects_mssql.html#mssql-isolation-level)

[＃3534 T0\>](http://www.sqlalchemy.org/trac/ticket/3534)

### 字符串/ varlength 类型不再在反射[¶](#string-varlength-types-no-longer-represent-max-explicitly-on-reflection "Permalink to this headline")上明确表示“max”

反映[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")，[`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")等类型时其中包括一个长度，SQL
Server下的“un-extended”类型会将“length”参数复制为值`"max"`：

    >>> from sqlalchemy import create_engine, inspect
    >>> engine = create_engine('mssql+pyodbc://scott:tiger@ms_2008', echo=True)
    >>> engine.execute("create table s (x varchar(max), y varbinary(max))")
    >>> insp = inspect(engine)
    >>> for col in insp.get_columns("s"):
    ...     print(col['type'].__class__, col['type'].length)
    ...
    <class 'sqlalchemy.sql.sqltypes.VARCHAR'> max
    <class 'sqlalchemy.dialects.mssql.base.VARBINARY'> max

预计基本类型中的“length”参数只是一个整数值或 None； None 表示 SQL
Server 方言解释为“max”的无限长度。然后修正是这样的，这些长度是 None，所以这些类型对象在非 SQL
Server 上下文中工作：

    >>> for col in insp.get_columns("s"):
    ...     print(col['type'].__class__, col['type'].length)
    ...
    <class 'sqlalchemy.sql.sqltypes.VARCHAR'> None
    <class 'sqlalchemy.dialects.mssql.base.VARBINARY'> None

可能依赖于“长度”值与字符串“max”直接比较的应用程序应该将`None`的值视为同一件事。

[＃3504 T0\>](http://www.sqlalchemy.org/trac/ticket/3504)

### 支持主键上的“非群集”以允许在其他地方群集[¶](#support-for-non-clustered-on-primary-key-to-allow-clustered-elsewhere "Permalink to this headline")

[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")，[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")，[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")上可用的`mssql_clustered`标志现在默认为`None`，并且可以设置为False，这将会为主键特别呈现NONCLUSTERED关键字，从而允许将不同的索引用作“聚集”。

也可以看看

[Clustered Index Support](dialects_mssql.html#mssql-indexes)

### legacy\_schema\_aliasing 标志现在设置为 False [¶](#the-legacy-schema-aliasing-flag-is-now-set-to-false "Permalink to this headline")

SQLAlchemy 1.0.5 introduced the `legacy_schema_aliasing` flag to the MSSQL dialect, allowing so-called “legacy mode”
aliasing to be turned off.
这种别名尝试将模式限定的表转换为别名；给定一个表格如：

    account_table = Table(
        'account', metadata,
        Column('id', Integer, primary_key=True),
        Column('info', String(100)),
        schema="customer_schema"
    )

传统的行为模式将尝试将符合模式的表名称变为别名：

    >>> eng = create_engine("mssql+pymssql://mydsn", legacy_schema_aliasing=True)plain
    >>> print(account_table.select().compile(eng))
    SELECT account_1.id, account_1.info
    FROM customer_schema.account AS account_1

但是，这种别名已被证明是不必要的，并且在许多情况下会产生不正确的 SQL。

在 SQLAlchemy 1.1 中，`legacy_schema_aliasing`标志现在默认为 False，禁用这种行为模式，并允许 MSSQL 方言对使用模式限定的表正常运行。对于可能依赖此行为的应用程序，将标志设置为 True。

[＃3434 T0\>](http://www.sqlalchemy.org/trac/ticket/3434)

方言的改进和改变 - Oracle [¶](#dialect-improvements-and-changes-oracle "Permalink to this headline")
----------------------------------------------------------------------------------------------------

### 支持 SKIP LOCKED [¶](#support-for-skip-locked "Permalink to this headline")

Core 和 ORM 中的新参数[`GenerativeSelect.with_for_update.skip_locked`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")将生成“SELECT
... FOR UPDATE”或“SELECT .. FOR SHARE”查询的“SKIP LOCKED”后缀。
