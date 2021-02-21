---
title: event
date: 2021-02-20 22:41:34
permalink: /pages/424986/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
事件[¶ T0\>](#events "Permalink to this headline")
==================================================

SQLAlchemy包含一个事件API，它将各种各样的钩子发布到SQLAlchemy
Core和ORM的内部。

New in version 0.7: The system supersedes the previous system of
“extension”, “proxy”, and “listener” classes.

事件注册[¶](#event-registration "Permalink to this headline")
-------------------------------------------------------------

通过一个API点，[`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")函数或[`listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")装饰器来订阅事件。这些函数接受一个目标，标识要拦截事件的字符串标识符以及用户定义的监听函数。这两个函数的附加位置和关键字参数可以由特定类型的事件支持，这些类型的事件可以为给定的事件函数指定备用接口，或者基于给定的目标提供关于辅助事件目标的指令。

事件的名称和相应侦听器函数的参数签名是从类绑定规范方法派生的，该方法绑定到文档中描述的标记类。例如，[`PoolEvents.connect()`](events.html#sqlalchemy.events.PoolEvents.connect "sqlalchemy.events.PoolEvents.connect")的文档指出事件名称为`"connect"`，并且用户定义的侦听器函数应该接收两个位置参数：

    from sqlalchemy.event import listen
    from sqlalchemy.pool import Pool

    def my_on_connect(dbapi_con, connection_record):
        print("New DBAPI connection:", dbapi_con)

    listen(Pool, 'connect', my_on_connect)

使用[`listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")装饰器来收听看起来像：

    from sqlalchemy.event import listens_for
    from sqlalchemy.pool import Pool

    @listens_for(Pool, "connect")
    def my_on_connect(dbapi_con, connection_record):
        print("New DBAPI connection:", dbapi_con)

命名参数样式[¶](#named-argument-styles "Permalink to this headline")
--------------------------------------------------------------------

听众功能可以接受一些不同的参数风格。以[`PoolEvents.connect()`](events.html#sqlalchemy.events.PoolEvents.connect "sqlalchemy.events.PoolEvents.connect")为例，该函数被记录为接收`dbapi_connection`和`connection_record`参数。We can opt to
receive these arguments by name, by establishing a listener function
that accepts `**keyword` arguments, by passing
`named=True` to either [`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen") or
[`listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for"):

    from sqlalchemy.event import listens_for
    from sqlalchemy.pool import Pool

    @listens_for(Pool, "connect", named=True)
    def my_on_connect(**kw):
        print("New DBAPI connection:", kw['dbapi_connection'])

使用命名参数传递时，函数参数规范中列出的名称将用作字典中的键。

命名样式按名称传递所有参数，而不管函数签名如何，因此只要名称匹配，可以以任意顺序列出具体参数：

    from sqlalchemy.event import listens_for
    from sqlalchemy.pool import Pool

    @listens_for(Pool, "connect", named=True)
    def my_on_connect(dbapi_connection, **kw):
        print("New DBAPI connection:", dbapi_connection)
        print("Connection record:", kw['connection_record'])

在上面，`**kw`的存在告诉[`listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")参数应该通过名称而不是位置传递给函数。

版本0.9.0新增：添加可选的`named`参数调度到事件调用。

目标[¶ T0\>](#targets "Permalink to this headline")
---------------------------------------------------

关于目标，[`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")函数非常灵活。它通常接受类，这些类的实例以及从中派生出适当目标的相关类或对象。例如，上面提到的`"connect"`事件接受[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")类和对象以及[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")类和对象：

    from sqlalchemy.event import listen
    from sqlalchemy.pool import Pool, QueuePool
    from sqlalchemy import create_engine
    from sqlalchemy.engine import Engine
    import psycopg2

    def connect():
        return psycopg2.connect(username='ed', host='127.0.0.1', dbname='test')

    my_pool = QueuePool(connect)
    my_engine = create_engine('postgresql://ed@localhost/test')

    # associate listener with all instances of Pool
    listen(Pool, 'connect', my_on_connect)

    # associate listener with all instances of Pool
    # via the Engine class
    listen(Engine, 'connect', my_on_connect)

    # associate listener with my_pool
    listen(my_pool, 'connect', my_on_connect)

    # associate listener with my_engine.pool
    listen(my_engine, 'connect', my_on_connect)

改性剂[¶ T0\>](#modifiers "Permalink to this headline")
-------------------------------------------------------

有些侦听器允许将修饰符传递给[`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")。这些修饰符有时会为侦听器提供替代调用签名。比如对于ORM事件，一些事件监听器可以有一个返回值来修改后续的处理。默认情况下，没有侦听器需要返回值，但通过传递`retval=True`可以支持此值：

    def validate_phone(target, value, oldvalue, initiator):
        """Strip non-numeric characters from a phone number"""

        return re.sub(r'(?![0-9])', '', value)

    # setup listener on UserContact.phone attribute, instructing
    # it to use the return value
    listen(UserContact.phone, 'set', validate_phone, retval=True)

事件参考[¶](#event-reference "Permalink to this headline")
----------------------------------------------------------

SQLAlchemy Core和SQLAlchemy ORM都具有各种各样的事件钩子：

-   **核心事件** - 这些内容在[Core
    Events](events.html)中进行了描述，并包含特定于连接池生命周期，SQL语句执行，事务生命周期以及模式创建和拆卸的事件挂钩。
-   **ORM Events** - these are described in [ORM
    Events](orm_events.html), and include event hooks specific to class
    and attribute instrumentation, object initialization hooks,
    attribute on-change hooks, session state, flush, and commit hooks,
    mapper initialization, object/result population, and per-instance
    persistence hooks.

API参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

 `sqlalchemy.event.`{.descclassname}`listen`{.descname}(*target*, *identifier*, *fn*, *\*args*, *\*\*kw*)[¶](#sqlalchemy.event.listen "Permalink to this definition")
:   为给定目标注册侦听器函数。

    例如。：

        from sqlalchemy import event
        from sqlalchemy.schema import UniqueConstraint

        def unique_constraint_name(const, table):
            const.name = "uq_%s_%s" % (
                table.name,
                list(const.columns)[0].name
            )
        event.listen(
                UniqueConstraint,
                "after_parent_attach",
                unique_constraint_name)

    使用`once`参数，也可以仅为第一次调用事件调用给定的函数：

        def on_config():
            do_config()

        event.listen(Mapper, "before_configure", on_config, once=True)

    版本0.9.4新增：添加`once=True`至[`event.listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")和[`event.listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")

    注意

    不能在运行目标事件的同时调用[`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")函数。这对线程安全性有影响，也意味着事件不能从侦听器函数内部添加。要运行的事件列表存在于可迭代集合中，不能在迭代过程中进行更改。

    事件注册和删除不是“高速”操作；这是一个配置操作。对于需要快速关联和取消高级事件的系统，请使用从单个侦听器内部处理的可变结构。

    在版本1.0.0中更改： - 现在将`collections.deque()`对象用作事件列表的容器，这些容器显式禁止集合突变被迭代。

    也可以看看

    [`listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")

    [`remove()`](#sqlalchemy.event.remove "sqlalchemy.event.remove")

 `sqlalchemy.event.`{.descclassname}`listens_for`{.descname}(*target*, *identifier*, *\*args*, *\*\*kw*)[¶](#sqlalchemy.event.listens_for "Permalink to this definition")
:   装饰一个函数作为给定目标+标识符的侦听器。

    例如。：

        from sqlalchemy import event
        from sqlalchemy.schema import UniqueConstraint

        @event.listens_for(UniqueConstraint, "after_parent_attach")
        def unique_constraint_name(const, table):
            const.name = "uq_%s_%s" % (
                table.name,
                list(const.columns)[0].name
            )

    使用`once`参数，也可以仅为第一次调用事件调用给定的函数：

        @event.listens_for(Mapper, "before_configure", once=True)
        def on_config():
            do_config()

    版本0.9.4新增：添加`once=True`至[`event.listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")和[`event.listens_for()`](#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")

    也可以看看

    [`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen") -
    事件监听的一般描述

 `sqlalchemy.event.`{.descclassname}`remove`{.descname}(*target*, *identifier*, *fn*)[¶](#sqlalchemy.event.remove "Permalink to this definition")
:   删除一个事件监听器。

    这里的参数应该与发送到[`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")的参数完全匹配。所有通过此调用进行的事件注册将通过使用相同参数调用[`remove()`](#sqlalchemy.event.remove "sqlalchemy.event.remove")进行恢复。

    例如。：

        # if a function was registered like this...
        @event.listens_for(SomeMappedClass, "before_insert", propagate=True)
        def my_listener_function(*arg):
            pass

        # ... it's removed like this
        event.remove(SomeMappedClass, "before_insert", my_listener_function)

    在上面，与`SomeMappedClass`关联的侦听器函数也被传播给`SomeMappedClass`的子类。 [`remove()`](#sqlalchemy.event.remove "sqlalchemy.event.remove")函数将恢复所有这些操作。

    版本0.9.0中的新功能

    注意

    [`remove()`](#sqlalchemy.event.remove "sqlalchemy.event.remove")函数不能在目标事件运行的同时被调用。这对线程的安全性有影响，也意味着一个事件不能从listener函数内部移除。要运行的事件列表存在于可迭代集合中，不能在迭代过程中进行更改。

    事件注册和删除不是“高速”操作；这是一个配置操作。对于需要快速关联和取消高级事件的系统，请使用从单个侦听器内部处理的可变结构。

    在版本1.0.0中更改： - 现在将`collections.deque()`对象用作事件列表的容器，这些容器显式禁止集合突变被迭代。

    也可以看看

    [`listen()`](#sqlalchemy.event.listen "sqlalchemy.event.listen")

 `sqlalchemy.event.`{.descclassname}`contains`{.descname}(*target*, *identifier*, *fn*)[¶](#sqlalchemy.event.contains "Permalink to this definition")
:   如果给定的target / ident / fn设置为侦听，则返回True。

    版本0.9.0中的新功能


