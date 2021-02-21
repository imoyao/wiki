---
title: session_events
date: 2021-02-20 22:41:47
permalink: /pages/72615b/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
使用事件跟踪对象和会话更改[¶](#tracking-object-and-session-changes-with-events "Permalink to this headline")
============================================================================================================

SQLAlchemy具有在整个Core和ORM中使用的广泛的[Event
Listening](core_event.html)系统。在ORM中，有各种各样的事件监听器钩子，它们在[ORM
Events](events.html)的API级别上记录。多年来，这一系列活动不断增加，包括许多非常有用的新活动以及一些与以前不相关的老活动。本节将尝试介绍主要事件挂钩以及何时可以使用它们。

持久性事件[¶](#persistence-events "Permalink to this headline")
---------------------------------------------------------------

可能最广泛使用的一系列事件是“持久性”事件，它与[flush
process](session_basics.html#session-flushing)相对应。flush是所有关于对象的未决修改的决定，然后以INSERT，UPDATE和DELETE的形式发送到数据库。

### `before_flush()`[¶](#before-flush "Permalink to this headline")

The [`SessionEvents.before_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")
hook is by far the most generally useful event to use when an
application wants to ensure that additional persistence changes to the
database are made when a flush proceeds.
使用[`SessionEvents.before_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")来操作对象以验证其状态，并在持久化之前编写其他对象和引用。Within
this event, it is **safe to manipulate the Session’s state**, that is,
new objects can be attached to it, objects can be deleted, and indivual
attributes on objects can be changed freely, and these changes will be
pulled into the flush process when the event hook completes.

典型的[`SessionEvents.before_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")钩子的任务是扫描集合[`Session.new`](session_api.html#sqlalchemy.orm.session.Session.new "sqlalchemy.orm.session.Session.new")，[`Session.dirty`](session_api.html#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty")和[`Session.deleted`](session_api.html#sqlalchemy.orm.session.Session.deleted "sqlalchemy.orm.session.Session.deleted")为了寻找发生事情的对象。

有关[`SessionEvents.before_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")的说明，请参阅[Versioning
with a History
Table](examples.html#examples-versioned-history)和[Versioning using
Temporal Rows](examples.html#examples-versioned-rows)

### `after_flush()`[¶](#after-flush "Permalink to this headline")

The [`SessionEvents.after_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")
hook is called after the SQL has been emitted for a flush process, but
**before** the state of the objects that were flushed has been altered.
也就是说，您仍然可以检查[`Session.new`](session_api.html#sqlalchemy.orm.session.Session.new "sqlalchemy.orm.session.Session.new")，[`Session.dirty`](session_api.html#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty")和[`Session.deleted`](session_api.html#sqlalchemy.orm.session.Session.deleted "sqlalchemy.orm.session.Session.deleted")集合以查看刚刚刷新的内容，而您还可以使用像[`AttributeState`](internals.html#sqlalchemy.orm.state.AttributeState "sqlalchemy.orm.state.AttributeState")提供的历史跟踪功能来查看刚刚保存的更改。在[`SessionEvents.after_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")事件中，可以根据观察到的变化将附加的SQL发送到数据库。

### `after_flush_postexec()`[¶](#after-flush-postexec "Permalink to this headline")

[`SessionEvents.after_flush_postexec()`](events.html#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")
is called soon after [`SessionEvents.after_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush"),
but is invoked **after** the state of the objects has been modified to
account for the flush that just took place. [`Session.new`](session_api.html#sqlalchemy.orm.session.Session.new "sqlalchemy.orm.session.Session.new")，[`Session.dirty`](session_api.html#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty")和[`Session.deleted`](session_api.html#sqlalchemy.orm.session.Session.deleted "sqlalchemy.orm.session.Session.deleted")集合在这里通常是完全空的。使用[`SessionEvents.after_flush_postexec()`](events.html#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")检查最终对象的标识映射，并可能发出额外的SQL。In
this hook, there is the ability to make new changes on objects, which
means the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
will again go into a “dirty” state; the mechanics of the
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
here will cause it to flush **again** if new changes are detected in
this hook if the flush were invoked in the context of
[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit");
otherwise, the pending changes will be bundled as part of the next
normal flush. 当钩子检测到[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")中的新变化时，计数器确保在100次迭代后停止这方面的无限循环，在[`SessionEvents.after_flush_postexec()`](events.html#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")钩子每次调用时不断添加新的状态以被刷新。

### 映射级事件[¶](#mapper-level-events "Permalink to this headline")

除了flush级别的钩子之外，还有一些钩子更加细化，因为它们是以每个对象为基础调用的，并且基于INSERT，UPDATE或DELETE分解。这些是映射器持久性钩子，它们也非常受欢迎，但是这些事件需要更谨慎地处理，因为它们在已经进行的刷新过程的上下文中进行；许多操作在这里不安全。

这些事件是：

-   [`MapperEvents.before_insert()`](events.html#sqlalchemy.orm.events.MapperEvents.before_insert "sqlalchemy.orm.events.MapperEvents.before_insert")
-   [`MapperEvents.after_insert()`](events.html#sqlalchemy.orm.events.MapperEvents.after_insert "sqlalchemy.orm.events.MapperEvents.after_insert")
-   [`MapperEvents.before_update()`](events.html#sqlalchemy.orm.events.MapperEvents.before_update "sqlalchemy.orm.events.MapperEvents.before_update")
-   [`MapperEvents.after_update()`](events.html#sqlalchemy.orm.events.MapperEvents.after_update "sqlalchemy.orm.events.MapperEvents.after_update")
-   [`MapperEvents.before_delete()`](events.html#sqlalchemy.orm.events.MapperEvents.before_delete "sqlalchemy.orm.events.MapperEvents.before_delete")
-   [`MapperEvents.after_delete()`](events.html#sqlalchemy.orm.events.MapperEvents.after_delete "sqlalchemy.orm.events.MapperEvents.after_delete")

每个事件都会传递[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，映射对象本身以及用于发出INSERT，UPDATE或DELETE语句的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")。这些事件的吸引力是显而易见的，因为如果应用程序想要将某些活动与特定类型的对象通过INSERT持续绑定时，该钩子非常具体；与[`SessionEvents.before_flush()`](events.html#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")事件不同，不需要像[`Session.new`](session_api.html#sqlalchemy.orm.session.Session.new "sqlalchemy.orm.session.Session.new")那样搜索集合以查找目标。但是，当调用这些事件时，表示要发送的每个INSERT，UPDATE，DELETE语句的完整列表的清空计划已经*已经决定*，并且在此阶段不能进行更改。因此对给定对象甚至可能的唯一更改是属性**local**到对象的行。对象或其他对象的任何其他更改都会影响[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的状态，这将无法正常运行。

这些映射级持久性事件中不支持的操作包括：

-   [`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")
-   [`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")
-   映射集合追加，添加，删除，删除，丢弃等。
-   映射关系属性set /
    del事件，即`someobject.related = someotherobject`

传递[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的原因是鼓励**简单的SQL操作直接在[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发生，例如递增计数器或在日志表中插入额外的行。**在处理[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")时，预计将使用核心级SQL操作；例如那些在[SQL
Expression Language Tutorial](core_tutorial.html)中描述的。

也有许多每个对象操作都不需要在flush事件中处理。最常见的替代方法是在`__init__()`方法内简单地建立附加状态以及对象，例如创建要与新对象关联的其他对象。使用[Simple
Validators](mapped_attributes.html#simple-validators)中描述的验证器是另一种方法；这些函数可以拦截对属性的更改，并根据属性更改在目标对象上建立更多的状态更改。通过这两种方法，物体在进入冲洗步骤之前处于正确的状态。

对象生命周期事件[¶](#object-lifecycle-events "Permalink to this headline")
--------------------------------------------------------------------------

事件的另一个用例是跟踪对象的生命周期。这是指在[Quickie Intro to Object
States](session_state_management.html#session-object-states)中首次引入的状态。

版本1.1中的新增功能添加了一个拦截[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中对象的所有可能状态转换的事件系统。

以上所有状态都可以通过事件完全跟踪。每个事件代表一个独特的状态转换，这意味着，起始状态和目标状态都是跟踪的部分。除了最初的瞬态事件之外，所有事件都是以[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象或类的形式出现的，这意味着它们可以与特定的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象关联：

    from sqlalchemy import event
    from sqlalchemy.orm import Session

    session = Session()

    @event.listens_for(session, 'transient_to_pending')
    def object_is_pending(session, obj):
        print("new pending: %s" % obj)

或者使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")类本身以及特定的[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")，这可能是最有用的形式：

    from sqlalchemy import event
    from sqlalchemy.orm import sessionmaker

    maker = sessionmaker()

    @event.listens_for(maker, 'transient_to_pending')
    def object_is_pending(session, obj):
        print("new pending: %s" % obj)

听众当然可以堆叠在一个功能的顶部，这很可能是常见的。例如，要跟踪进入持久状态的所有对象：

    @event.listens_for(maker, "pending_to_persistent")
    @event.listens_for(maker, "deleted_to_persistent")
    @event.listens_for(maker, "detached_to_persistent")
    @event.listens_for(maker, "loaded_as_persistent")
    def detect_all_persistent(session, instance):
        print("object is now persistent: %s" % instance)

### 瞬态[¶ T0\>](#transient "Permalink to this headline")

所有映射对象在第一次构建时都以[transient](glossary.html#term-transient)开始。在这种状态下，对象单独存在，并且与任何[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")没有关联。For
this initial state, there’s no specific “transition” event since there
is no [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
however if one wanted to intercept when any transient object is created,
the [`InstanceEvents.init()`](events.html#sqlalchemy.orm.events.InstanceEvents.init "sqlalchemy.orm.events.InstanceEvents.init")
method is probably the best event.
此事件适用于特定的类或超类。例如，要拦截特定声明基的所有新对象：

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import event

    Base = declarative_base()

    @event.listens_for(Base, "init", propagate=True)
    def intercept_init(instance, args, kwargs):
        print("new transient: %s" % instance)

### 瞬态到待定[¶](#transient-to-pending "Permalink to this headline")

The transient object becomes [pending](glossary.html#term-pending) when
it is first associated with a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
via the [`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")
or [`Session.add_all()`](session_api.html#sqlalchemy.orm.session.Session.add_all "sqlalchemy.orm.session.Session.add_all")
method. 一个对象也可能成为[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的一部分，作为[“cascade”](cascades.html#unitofwork-cascades)中显式添加的引用对象的结果。使用[`SessionEvents.transient_to_pending()`](events.html#sqlalchemy.orm.events.SessionEvents.transient_to_pending "sqlalchemy.orm.events.SessionEvents.transient_to_pending")事件可检测到暂挂转换的暂态：

    @event.listens_for(sessionmaker, "transient_to_pending")
    def intercept_transient_to_pending(session, object_):
        print("transient to pending: %s" % object_)

### 等待持久[¶](#pending-to-persistent "Permalink to this headline")

对于实例，当flush和INSERT语句发生时，[pending](glossary.html#term-pending)对象变为[persistent](glossary.html#term-persistent)。该对象现在拥有一个身份密钥。使用[`SessionEvents.pending_to_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.pending_to_persistent "sqlalchemy.orm.events.SessionEvents.pending_to_persistent")事件跟踪挂起持久化：

    @event.listens_for(sessionmaker, "pending_to_persistent")
    def intercept_pending_to_persistent(session, object_):
        print("pending to persistent: %s" % object_)

### 等待瞬变[¶](#pending-to-transient "Permalink to this headline")

The [pending](glossary.html#term-pending) object can revert back to
[transient](glossary.html#term-transient) if the
[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")
method is called before the pending object has been flushed, or if the
[`Session.expunge()`](session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")
method is called for the object before it is flushed.
使用[`SessionEvents.pending_to_transient()`](events.html#sqlalchemy.orm.events.SessionEvents.pending_to_transient "sqlalchemy.orm.events.SessionEvents.pending_to_transient")事件跟踪挂起到瞬态：

    @event.listens_for(sessionmaker, "pending_to_transient")
    def intercept_pending_to_transient(session, object_):
        print("transient to pending: %s" % object_)

### 加载为持久[¶](#loaded-as-persistent "Permalink to this headline")

从数据库加载时，对象可以直接以[persistent](glossary.html#term-persistent)状态出现在[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中。Tracking
this state transition is synonymous with tracking objects as they are
loaded, and is synonomous with using the [`InstanceEvents.load()`](events.html#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")
instance-level event.
然而，[`SessionEvents.loaded_as_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.loaded_as_persistent "sqlalchemy.orm.events.SessionEvents.loaded_as_persistent")事件是以会话为中心的钩子提供的，以便在通过此特定途径进入持久状态时拦截对象：

    @event.listens_for(sessionmaker, "loaded_as_persistent")
    def intercept_loaded_as_persistent(session, object_):
        print("object loaded into persistent state: %s" % object_)

### 持久到瞬间[¶](#persistent-to-transient "Permalink to this headline")

如果为对象首次添加为待处理的事务调用[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法，持久对象可以恢复到瞬态状态。在ROLLBACK的情况下，使该对象持久化的INSERT语句被回滚，并且该对象从[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")被逐出以再次变为瞬态。使用[`SessionEvents.persistent_to_transient()`](events.html#sqlalchemy.orm.events.SessionEvents.persistent_to_transient "sqlalchemy.orm.events.SessionEvents.persistent_to_transient")事件挂钩跟踪从持久性恢复为瞬态的对象：

    @event.listens_for(sessionmaker, "persistent_to_transient")
    def intercept_persistent_to_transient(session, object_):
        print("persistent to transient: %s" % object_)

### 持续删除[¶](#persistent-to-deleted "Permalink to this headline")

当标记为要删除的对象在刷新过程中从数据库中删除时，持久对象进入[deleted](glossary.html#term-deleted)状态。请注意，这与为目标对象调用[`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")方法时**不一样**。[`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")方法仅**标记**要删除的对象；直到刷新结束后才会发出实际的DELETE语句。在刷新之后，目标对象存在“已删除”状态。

在“已删除”状态下，该对象仅与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")稍有关联。它不存在于身份映射中，也不存在于[`Session.deleted`](session_api.html#sqlalchemy.orm.session.Session.deleted "sqlalchemy.orm.session.Session.deleted")集合中，该集合指向待删除时。

从“已删除”状态，对象可以在事务提交时转到分离状态，或者如果事务被回滚，则返回到持久状态。

使用[`SessionEvents.persistent_to_deleted()`](events.html#sqlalchemy.orm.events.SessionEvents.persistent_to_deleted "sqlalchemy.orm.events.SessionEvents.persistent_to_deleted")跟踪永久删除的转换：

    @event.listens_for(sessionmaker, "persistent_to_deleted")
    def intercept_persistent_to_deleted(session, object_):
        print("object was DELETEd, is now in deleted state: %s" % object_)

### 已删除分离[¶](#deleted-to-detached "Permalink to this headline")

当会话的事务提交时，被删除的对象变为[detached](glossary.html#term-detached)。在[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")方法被调用后，数据库事务是最终的，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")现在完全丢弃已删除的对象并删除与它的所有关联。使用[`SessionEvents.deleted_to_detached()`](events.html#sqlalchemy.orm.events.SessionEvents.deleted_to_detached "sqlalchemy.orm.events.SessionEvents.deleted_to_detached")跟踪已删除到已分离的转换：

    @event.listens_for(sessionmaker, "deleted_to_detached")
    def intercept_deleted_to_detached(session, object_):
        print("deleted to detached: %s" % object_)

注意

当对象处于已删除状态时，可以使用`inspect(object).deleted`访问的[`InstanceState.deleted`](internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")属性返回True。但是，当对象被分离时，[`InstanceState.deleted`](internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")将再次返回False。要检测对象是否被删除，无论它是否被分离，请使用[`InstanceState.was_deleted`](internals.html#sqlalchemy.orm.state.InstanceState.was_deleted "sqlalchemy.orm.state.InstanceState.was_deleted")访问器。

### 持久分离[¶](#persistent-to-detached "Permalink to this headline")

The persistent object becomes [detached](glossary.html#term-detached)
when the object is de-associated with the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
via the [`Session.expunge()`](session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge"),
[`Session.expunge_all()`](session_api.html#sqlalchemy.orm.session.Session.expunge_all "sqlalchemy.orm.session.Session.expunge_all"),
or [`Session.close()`](session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")
methods.

注意

如果一个对象拥有的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")被应用程序取消引用并且由于垃圾收集而被抛弃，则该对象也可能成为**隐式分离的**。在这种情况下，**没有事件被发射**。

使用[`SessionEvents.persistent_to_detached()`](events.html#sqlalchemy.orm.events.SessionEvents.persistent_to_detached "sqlalchemy.orm.events.SessionEvents.persistent_to_detached")事件跟踪从持久移动到分离的对象：

    @event.listens_for(sessionmaker, "persistent_to_detached")
    def intecept_persistent_to_detached(session, object_):
        print("object became detached: %s" % object_)

### 分离到持久[¶](#detached-to-persistent "Permalink to this headline")

使用[`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")或等效方法将分离对象重新关联到会话时，分离的对象将变为持久对象。使用[`SessionEvents.detached_to_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.detached_to_persistent "sqlalchemy.orm.events.SessionEvents.detached_to_persistent")事件跟踪从分离状态回到持久性状态的对象：

    @event.listens_for(sessionmaker, "detached_to_persistent")
    def intecept_detached_to_persistent(session, object_):
        print("object became persistent again: %s" % object_)

### 已删除到持久[¶](#deleted-to-persistent "Permalink to this headline")

当使用[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法回退已删除DELETEd的事务时，[deleted](glossary.html#term-deleted)对象可以恢复为[persistent](glossary.html#term-persistent)状态。使用[`SessionEvents.deleted_to_persistent()`](events.html#sqlalchemy.orm.events.SessionEvents.deleted_to_persistent "sqlalchemy.orm.events.SessionEvents.deleted_to_persistent")事件跟踪已移回到持久状态的已删除对象：

    @event.listens_for(sessionmaker, "transient_to_pending")
    def intercept_transient_to_pending(session, object_):
        print("transient to pending: %s" % object_)

交易事件[¶](#transaction-events "Permalink to this headline")
-------------------------------------------------------------

事务事件允许在[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")级别发生事务边界时以及[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")更改[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象上的事务性状态时通知应用程序。

-   [`SessionEvents.after_transaction_create()`](events.html#sqlalchemy.orm.events.SessionEvents.after_transaction_create "sqlalchemy.orm.events.SessionEvents.after_transaction_create"),
    [`SessionEvents.after_transaction_end()`](events.html#sqlalchemy.orm.events.SessionEvents.after_transaction_end "sqlalchemy.orm.events.SessionEvents.after_transaction_end")
    - these events track the logical transaction scopes of the
    [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    in a way that is not specific to individual database connections.
    这些事件旨在帮助集成事务跟踪系统，如`zope.sqlalchemy`。当应用程序需要将某个外部范围与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的事务范围对齐时使用这些事件。这些钩子反映了[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的“嵌套”事务行为，因为它们跟踪逻辑“子事务”以及“嵌套”（例如SAVEPOINT）事务。
-   [`SessionEvents.before_commit()`](events.html#sqlalchemy.orm.events.SessionEvents.before_commit "sqlalchemy.orm.events.SessionEvents.before_commit"),
    [`SessionEvents.after_commit()`](events.html#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit"),
    [`SessionEvents.after_begin()`](events.html#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin"),
    [`SessionEvents.after_rollback()`](events.html#sqlalchemy.orm.events.SessionEvents.after_rollback "sqlalchemy.orm.events.SessionEvents.after_rollback"),
    [`SessionEvents.after_soft_rollback()`](events.html#sqlalchemy.orm.events.SessionEvents.after_soft_rollback "sqlalchemy.orm.events.SessionEvents.after_soft_rollback")
    - These events allow tracking of transaction events from the
    perspective of database connections.
    [`SessionEvents.after_begin()`](events.html#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin")
    in particular is a per-connection event; a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    that maintains more than one connection will emit this event for
    each connection individually as those connections become used within
    the current transaction.
    当DBAPI连接本身直接接收到回滚或提交指令时，回滚和提交事件即为引用。

属性更改事件[¶](#attribute-change-events "Permalink to this headline")
----------------------------------------------------------------------

属性更改事件允许拦截对象的特定属性何时被修改。这些事件包括[`AttributeEvents.set()`](events.html#sqlalchemy.orm.events.AttributeEvents.set "sqlalchemy.orm.events.AttributeEvents.set")，[`AttributeEvents.append()`](events.html#sqlalchemy.orm.events.AttributeEvents.append "sqlalchemy.orm.events.AttributeEvents.append")和[`AttributeEvents.remove()`](events.html#sqlalchemy.orm.events.AttributeEvents.remove "sqlalchemy.orm.events.AttributeEvents.remove")。这些事件非常有用，特别是对于每个对象验证操作；然而，使用“验证器”钩子通常会更方便，该钩子在幕后使用这些钩子；请参阅[Simple
Validators](mapped_attributes.html#simple-validators)以了解其背景。属性事件也是反向引用机制的后面。属性事件的使用示例位于[Attribute
Instrumentation](examples.html#examples-instrumentation)中。
