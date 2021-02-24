---
title: 弃用的事件接口
date: 2021-02-20 22:41:35
permalink: /sqlalchemy/core/interfaces/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
弃用的事件接口[¶](#module-sqlalchemy.interfaces "Permalink to this headline")
=============================================================================

本节介绍 SQLAlchemy 0.5 中引入的基于类的核心事件接口。ORM 模拟在[Deprecated
ORM Event Interfaces](orm_deprecated.html)中描述。

从版本 0.7 开始弃用：
[Events](event.html)中描述的新事件系统取代了扩展/代理/侦听器系统，为所有事件提供一致的接口，而无需子类化。

执行，连接和光标事件[¶](#execution-connection-and-cursor-events "Permalink to this headline")
---------------------------------------------------------------------------------------------

*class* `sqlalchemy.interfaces。`{.descclassname} `ConnectionProxy`{.descname} [¶](#sqlalchemy.interfaces.ConnectionProxy "Permalink to this definition")
:   允许通过 Connections 拦截语句执行。

    注意plain

    [`ConnectionProxy`](#sqlalchemy.interfaces.ConnectionProxy "sqlalchemy.interfaces.ConnectionProxy")已弃用。请参阅[`ConnectionEvents`](events.html#sqlalchemy.events.ConnectionEvents "sqlalchemy.events.ConnectionEvents")。

    可以实现`execute()`和`cursor_execute()`中的任何一个或两个来拦截已编译的语句和游标级别执行，例如：

        class MyProxy(ConnectionProxy):
            def execute(self, conn, execute, clauseelement,
                        *multiparams, **params):
                print "compiled statement:", clauseelement
                return execute(clauseelement, *multiparams, **params)

            def cursor_execute(self, execute, cursor, statement,
                               parameters, context, executemany):
                print "raw statement:", statement
                return execute(cursor, statement, parameters, context)

    `execute`参数是一个函数，它将完成操作的默认执行行为。应该使用示例中所示的签名。

    代理通过`proxy`参数安装到[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")中：

        e = create_engine('someurl://', proxy=MyProxy())

    `begin`{.descname} （ *conn*，*begin* ） [](#sqlalchemy.interfaces.ConnectionProxy.begin "Permalink to this definition")
    :   拦截begin()事件。

     `begin_twophase`{.descname}(*conn*, *begin\_twophase*, *xid*)[¶](#sqlalchemy.interfaces.ConnectionProxy.begin_twophase "Permalink to this definition")
    :   拦截begin\_twophase()事件。

    `commit`{.descname} （ *conn*，*commit* ） [](#sqlalchemy.interfaces.ConnectionProxy.commit "Permalink to this definition")
    :   拦截commit()事件。

    `commit_twophase  tt> （ conn，commit_twophase，xid，is_prepared  t5 > ） T6> ¶ T7>`{.descname}
    :   拦截commit\_twophase()事件。

    `cursor_execute`{.descname} （ *execute*，*游标*，*语句*，*参数 t5 \>，*上下文*，*executemany* ） [¶](#sqlalchemy.interfaces.ConnectionProxy.cursor_execute "Permalink to this definition")*
    :   拦截低级别的游标execute()事件。

     `execute`{.descname}(*conn*, *execute*, *clauseelement*, *\*multiparams*, *\*\*params*)[¶](#sqlalchemy.interfaces.ConnectionProxy.execute "Permalink to this definition")
    :   拦截高级别的execute()事件。

     `prepare_twophase`{.descname}(*conn*, *prepare\_twophase*, *xid*)[¶](#sqlalchemy.interfaces.ConnectionProxy.prepare_twophase "Permalink to this definition")
    :   拦截prepare\_twophase()事件。

     `release_savepoint`{.descname}(*conn*, *release\_savepoint*, *name*, *context*)[¶](#sqlalchemy.interfaces.ConnectionProxy.release_savepoint "Permalink to this definition")
    :   拦截release\_savepoint()事件。

    `回滚`{.descname} （ *conn*，*回滚* ） [](#sqlalchemy.interfaces.ConnectionProxy.rollback "Permalink to this definition")
    :   拦截回滚()事件。

     `rollback_savepoint`{.descname}(*conn*, *rollback\_savepoint*, *name*, *context*)[¶](#sqlalchemy.interfaces.ConnectionProxy.rollback_savepoint "Permalink to this definition")
    :   拦截rollback\_savepoint()事件。

    `rollback_twophase`{.descname} （ *conn*，*rollback\_twophase*，*xid*，*is\_prepared t5 \> ） T6\> [¶ T7\>](#sqlalchemy.interfaces.ConnectionProxy.rollback_twophase "Permalink to this definition")*
    :   拦截rollback\_twophase()事件。

     `savepoint`{.descname}(*conn*, *savepoint*, *name=None*)[¶](#sqlalchemy.interfaces.ConnectionProxy.savepoint "Permalink to this definition")
    :   截取保存点()事件。

连接池事件[¶](#connection-pool-events "Permalink to this headline")
-------------------------------------------------------------------

*class* `sqlalchemy.interfaces。`{.descclassname} `PoolListener`{.descname} [¶](#sqlalchemy.interfaces.PoolListener "Permalink to this definition")
:   钩入[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")中连接的生命周期。

    注意plain

    [`PoolListener`](#sqlalchemy.interfaces.PoolListener "sqlalchemy.interfaces.PoolListener")
    is deprecated. 请参阅[`PoolEvents`](events.html#sqlalchemy.events.PoolEvents "sqlalchemy.events.PoolEvents")。

    用法：

        class MyListener(PoolListener):
            def connect(self, dbapi_con, con_record):
                '''perform connect operations'''
            # etc.

        # create a new pool with a listener
        p = QueuePool(..., listeners=[MyListener()])

        # add a listener after the fact
        p.add_listener(MyListener())

        # usage with create_engine()
        e = create_engine("url://", listeners=[MyListener()])

    所有标准连接[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")类型都可以接受关键连接生命周期事件的事件侦听器：创建，池检出和检入。连接关闭时不会触发事件。

    For any given DB-API connection, there will be one
    `connect` event, n number of
    `checkout` events, and either n or n - 1
    `checkin` events. （如果通过`detach()`方法将`Connection`从其池中分离出来，它将不会被重新签入。）

    这些是低级对象的低级事件：原始Python DB-API连接，没有SQLAlchemy
    `Connection`包装，`Dialect`服务或`ClauseElement`None

    事件还会收到一个`_ConnectionRecord`，这是一个长期存在的内部`Pool`对象，基本上表示连接池中的“插槽”。`_ConnectionRecord`对象具有一个值得注意的公共属性：`info`，这是一个字典，其内容的范围为记录管理的DB-API连接的生存期。不过，您可以使用此共享存储区域。

    没有必要继承`PoolListener`来处理事件。任何实现一个或多个这些方法的类都可以用作池监听器。`Pool`将检查侦听器对象提供的方法，并根据侦听器的能力将侦听器添加到一个或多个内部事件队列中。就效率和函数调用开销而言，仅仅为您将要使用的钩子提供实现会更好。

    `checkin`{.descname} （ *dbapi\_con*，*con\_record* ） [¶](#sqlalchemy.interfaces.PoolListener.checkin "Permalink to this definition")
    :   连接返回到池时调用。

        请注意，连接可能已关闭，如果连接已失效，则可能为无。`checkin` will not be called for detached connections.
        （他们不回到游泳池。）

        dbapi\_con
        :   原始的DB-API连接
        con\_record
        :   持续管理连接的`_ConnectionRecord`

    `结帐`{.descname} （ *dbapi\_con*，*con\_record*，*con\_proxy* ） [¶ T6\>](#sqlalchemy.interfaces.PoolListener.checkout "Permalink to this definition")
    :   从池中检索连接时调用。

        dbapi\_con
        :   原始的DB-API连接
        con\_record
        :   持续管理连接的`_ConnectionRecord`
        con\_proxy
        :   `_ConnectionFairy`管理当前结帐范围的连接。

        如果您引发`exc.DisconnectionError`，则将丢弃当前连接并检索新的连接。处理所有结帐侦听器将中止并使用新连接重新启动。

    `连接 tt> （ dbapi_con，con_record ） ¶`{.descname}
    :   为每个新的DB-API连接或池的`creator()`调用一次。

        dbapi\_con
        :   新连接的原始DB-API连接（不是SQLAlchemy
            `Connection`包装器）。
        con\_record
        :   持续管理连接的`_ConnectionRecord`

     `first_connect`{.descname}(*dbapi\_con*, *con\_record*)[¶](#sqlalchemy.interfaces.PoolListener.first_connect "Permalink to this definition")
    :   第一次为DB-API连接调用一次。

        dbapi\_con
        :   新连接的原始DB-API连接（不是SQLAlchemy
            `Connection`包装器）。
        con\_record
        :   持续管理连接的`_ConnectionRecord`


