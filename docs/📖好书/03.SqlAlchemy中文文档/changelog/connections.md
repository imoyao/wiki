---
title: 连接/引擎
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/ffcb37/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
连接/引擎[¶](#connections-engines "Permalink to this headline")
===============================================================

- [连接/引擎¶](#连接引擎)
  - [我如何配置日志？¶](#我如何配置日志)
  - [我如何汇集数据库连接？我的连接是否合并？¶](#我如何汇集数据库连接我的连接是否合并)
  - [如何将自定义连接参数传递给我的数据库 API？¶](#如何将自定义连接参数传递给我的数据库-api)
  - [“MySQL 服务器已经消失”¶](#mysql-服务器已经消失)
  - [为什么 SQLAlchemy 发出如此多的 ROLLBACK？¶](#为什么-sqlalchemy-发出如此多的-rollback)
    - [我在 MyISAM 上 - 如何关闭它？¶](#我在-myisam-上---如何关闭它)
    - [我在 SQL Server 上 - 如何将这些 ROLLBACKs 转换为 COMMIT？¶](#我在-sql-server-上---如何将这些-rollbacks-转换为-commit)
  - [I am using multiple connections with a SQLite database (typically to test transaction operation), and my test program is not working!¶](#i-am-using-multiple-connections-with-a-sqlite-database-typically-to-test-transaction-operation-and-my-test-program-is-not-working)
  - [如何在使用引擎时获得原始 DBAPI 连接？¶](#如何在使用引擎时获得原始-dbapi-连接)
  - [我如何使用 Python 多处理引擎/连接/会话或 os.fork()？¶](#我如何使用-python-多处理引擎连接会话或-osfork)

我如何配置日志？[¶](#how-do-i-configure-logging "Permalink to this headline")
-----------------------------------------------------------------------------

请参阅[Configuring Logging](core_engines.html#dbengine-logging)。

我如何汇集数据库连接？我的连接是否合并？[¶](#how-do-i-pool-database-connections-are-my-connections-pooled "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------

在大多数情况下，SQLAlchemy 会自动执行应用程序级连接池。除 SQLite 以外，[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")对象将[`QueuePool`](core_pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")作为连接的来源。

有关更多详细信息，请参阅[Engine
Configuration](core_engines.html)和[Connection
Pooling](core_pooling.html)。

如何将自定义连接参数传递给我的数据库 API？[¶](#how-do-i-pass-custom-connect-arguments-to-my-database-api "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------------------

[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")调用直接通过`connect_args`关键字参数接受附加参数：
```plain
    e = create_engine("mysql://scott:tiger@localhost/test",
                        connect_args={"encoding": "utf8"})
```
或者对于基本的字符串和整数参数，通常可以在 URL 的查询字符串中指定它们：
```plain
    e = create_engine("mysql://scott:tiger@localhost/test?encoding=utf8")
```
也可以看看

[Custom DBAPI connect() arguments](core_engines.html#custom-dbapi-args)

“MySQL 服务器已经消失”[¶](#mysql-server-has-gone-away "Permalink to this headline")
----------------------------------------------------------------------------------

这个错误有两个主要原因：

​1.
MySQL 客户端关闭已经空闲一段时间的连接，默认为八个小时。这可以通过在[Connection
Timeouts](dialects_mysql.html#mysql-connection-timeouts)中描述的[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")使用`pool_recycle`设置来避免。

​2. MySQLdb
[DBAPI](glossary.html#term-dbapi)或类似的 DBAPI 以非线程安全的方式使用，或以其他不适当的方式使用。MySQLdb 连接对象不是线程安全的
- 这扩展到任何链接到包含 ORM [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的单个连接的 SQLAlchemy 系统。有关如何在多线程环境中使用[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的背景信息，请参阅[Is
the session
thread-safe?](orm_session_basics.html#session-faq-threadsafe)。

为什么 SQLAlchemy 发出如此多的 ROLLBACK？[¶](#why-does-sqlalchemy-issue-so-many-rollbacks "Permalink to this headline")
--------------------------------------------------------------------------------------------------------------------

SQLAlchemy 目前假定 DBAPI 连接处于“非自动提交”模式 -
这是 Python 数据库 API 的默认行为，这意味着必须假定事务始终在进行中。连接池在返回连接时发出`connection.rollback()`。这样可以释放连接上剩余的任何事务资源。在 Postgresql 或 MSSQL 这样的表资源被大量锁定的数据库中，这非常关键，因此行和表不会在不再使用的连接中锁定。否则应用程序可能会挂起。然而，这不仅仅适用于锁，而且对任何具有任何事务隔离的数据库（包括带 InnoDB 的 MySQL）都同样重要。如果在隔离内已经在该连接上查询了该数据，那么仍旧在旧事务中的任何连接都将返回陈旧数据。有关为什么您可能会在 MySQL 上看到过时数据的背景，请参阅[http://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html](http://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html)

### 我在 MyISAM 上 - 如何关闭它？[¶](#i-m-on-myisam-how-do-i-turn-it-off "Permalink to this headline")

连接池的连接返回行为的行为可以使用`reset_on_return`进行配置：

    from sqlalchemy import create_engineplainplainplainplainplainplainplainplainplain
    from sqlalchemy.pool import QueuePool

    engine = create_engine('mysql://scott:tiger@localhost/myisam_database', pool=QueuePool(reset_on_return=False))

### 我在 SQL Server 上 - 如何将这些 ROLLBACKs 转换为 COMMIT？[¶](#i-m-on-sql-server-how-do-i-turn-those-rollbacks-into-commits "Permalink to this headline")

除了`True`，`False`以外，`reset_on_return`还接受`commit`，`rollback` `None`设置为`commit`会导致 COMMIT，因为任何连接都会返回到池：

    engine = create_engine('mssql://scott:tiger@mydsn', pool=QueuePool(reset_on_return='commit'))plainplainplainplainplainplainplain

I am using multiple connections with a SQLite database (typically to test transaction operation), and my test program is not working![¶](#i-am-using-multiple-connections-with-a-sqlite-database-typically-to-test-transaction-operation-and-my-test-program-is-not-working "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

如果使用 SQLite `:memory:`数据库或 0.7 版之前的 SQLAlchemy 版本，则默认连接池是[`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")，每个线程只维护一个 SQLite 连接。因此，在同一个线程中使用的两个连接实际上是相同的 SQLite 连接。确保你没有使用：memory：数据库，并使用[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")，这是当前 SQLAlchemy 版本中非内存数据库的默认值。

也可以看看

[Threading/Pooling
Behavior](dialects_sqlite.html#pysqlite-threading-pooling) - info on
PySQLite’s behavior.

如何在使用引擎时获得原始 DBAPI 连接？[¶](#how-do-i-get-at-the-raw-dbapi-connection-when-using-an-engine "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------------

使用常规的 SA 引擎级连接，您可以通过[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上的[`Connection.connection`](core_connections.html#sqlalchemy.engine.Connection.connection "sqlalchemy.engine.Connection.connection")属性获取 DBAPI 连接的池代理版本，真正的 DBAPI 连接可以调用`ConnectionFairy.connection`属性 -
但不应该有任何需要访问非池代理的 DBAPI 连接，因为所有方法都通过以下方式代理：
```plain
    engine = create_engine(...)
    conn = engine.connect()
    conn.connection.<do DBAPI things>
    cursor = conn.connection.cursor(<DBAPI specific arguments..>)
```
您必须确保将连接上的任何隔离级别设置或其他特定于操作的设置恢复为正常状态，然后才能将其返回到池。

作为还原设置的替代方法，您可以在[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")或代理连接上调用[`Connection.detach()`](core_connections.html#sqlalchemy.engine.Connection.detach "sqlalchemy.engine.Connection.detach")方法，该方法将从池中断开连接当[`Connection.close()`](core_connections.html#sqlalchemy.engine.Connection.close "sqlalchemy.engine.Connection.close")被调用时它将被关闭并丢弃：
```python
    conn = engine.connect()
    conn.detach()  # detaches the DBAPI connection from the connection pool
    conn.connection.<go nuts>
    conn.close()  # connection is closed for real, the pool replaces it with a new connection
```
我如何使用 Python 多处理引擎/连接/会话或 os.fork()？[¶](#how-do-i-use-engines-connections-sessions-with-python-multiprocessing-or-os-fork "Permalink to this headline")
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

多个 python 进程的关键目标是防止跨进程共享任何数据库连接。根据驱动程序和操作系统的具体情况，这里出现的问题包括从非工作连接到多个进程并发使用的套接字连接，导致断开的消息传递（后者通常最常见）。

SQLAlchemy [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")对象引用现有数据库连接的连接池。所以当这个对象被复制到一个子进程时，目标是确保没有数据库连接继续。有三种通用的方法：

1.  使用[`NullPool`](core_pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")禁用池。这是最简单的一次性系统，可防止[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")多次使用任何连接。

2.  在任何给定的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")上调用[`Engine.dispose()`](core_connections.html#sqlalchemy.engine.Engine.dispose "sqlalchemy.engine.Engine.dispose")，只要在新进程中。在 Python 多处理中，像`multiprocessing.Pool`这样的构造包含了可以执行这个操作的地方的“初始化器”钩子；否则在`os.fork()`的顶部或者`Process`对象开始子 fork 的位置，对[`Engine.dispose()`](core_connections.html#sqlalchemy.engine.Engine.dispose "sqlalchemy.engine.Engine.dispose")

3.  事件处理程序可以应用于连接池，用于测试跨进程边界共享的连接，并使其失效。这看起来像下面这样：
```python
        import os
        import warnings

        from sqlalchemy import event
        from sqlalchemy import exc

        def add_engine_pidguard(engine):
            """Add multiprocessing guards.

            Forces a connection to be reconnected if it is detected
            as having been shared to a sub-process.

            """

            @event.listens_for(engine, "connect")
            def connect(dbapi_connection, connection_record):
                connection_record.info['pid'] = os.getpid()

            @event.listens_for(engine, "checkout")
            def checkout(dbapi_connection, connection_record, connection_proxy):
                pid = os.getpid()
                if connection_record.info['pid'] != pid:
                    # substitute log.debug() or similar here as desired
                    warnings.warn(
                        "Parent process %(orig)s forked (%(newproc)s) with an open "
                        "database connection, "
                        "which is being discarded and recreated." %
                        {"newproc": pid, "orig": connection_record.info['pid']})
                    connection_record.connection = connection_proxy.connection = None
                    raise exc.DisconnectionError(
                        "Connection record belongs to pid %s, "
                        "attempting to check out in pid %s" %
                        (connection_record.info['pid'], pid)
                    )
```
    这些事件一旦创建就会应用于[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")：plainplainplainplainplain
```plain
        engine = create_engine("...")

        add_engine_pidguard(engine)
```
上述策略将适应[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")在进程之间共享的情况。However,
for the case of a transaction-active [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
or [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
being shared, there’s no automatic fix for this; an application needs to
ensure a new child process only initiate new [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
objects and transactions, as well as ORM [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
objects. 对于[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象，从技术上讲，只有在会话当前是事务绑定的情况下才需要这样做，但是单个[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的范围无论如何都是要保留在单个调用堆栈（例如，不是全局对象，不在进程或线程之间共享）。
