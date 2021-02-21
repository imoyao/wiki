---
title: pooling
date: 2021-02-20 22:41:35
permalink: /pages/ade251/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
连接池[¶](#module-sqlalchemy.pool "Permalink to this headline")
===============================================================

连接池是一种标准技术，用于维护内存中长时间运行的连接以实现高效的重用，并提供对应用程序可能同时使用的连接总数的管理。

特别是对于服务器端Web应用程序，连接池是在内存中维护活动数据库连接的“池”的标准方式，这些连接可以跨请求重用。

SQLAlchemy包含几个与[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")集成的连接池实现。它们也可以直接用于想要将池化添加到其他普通DBAPI方法的应用程序。

连接池配置[¶](#connection-pool-configuration "Permalink to this headline")
--------------------------------------------------------------------------

The [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
returned by the [`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
function in most cases has a [`QueuePool`](#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
integrated, pre-configured with reasonable pooling defaults.
如果您只是阅读本节以了解如何启用共享池 - 恭喜！你已经完成了。

The most common [`QueuePool`](#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
tuning parameters can be passed directly to [`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
as keyword arguments: `pool_size`,
`max_overflow`, `pool_recycle`
and `pool_timeout`. 例如：

    engine = create_engine('postgresql://me@localhost/mydb',
                           pool_size=20, max_overflow=0)

在SQLite的情况下，方言选择[`SingletonThreadPool`](#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")或[`NullPool`](#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")，以提供与SQLite的线程和锁定模型的更大兼容性，并提供合理的默认行为SQLite“内存”数据库，它们将整个数据集保存在单个连接的范围内。

所有的SQLAlchemy池实现都有共同之处：它们都没有“预创建”连接 -
所有实现都等到创建连接之前首次使用。此时，如果没有额外的并发结算请求进行更多连接，则不会创建其他连接。这就是为什么[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")默认使用大小为5的[`QueuePool`](#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")而不考虑应用程序是否真的需要5个连接排队的原因
-
池只有当应用程序实际同时使用5个连接时才会增长到这个大小，在这种情况下，小池的使用是完全适当的默认行为。

切换池实现[¶](#switching-pool-implementations "Permalink to this headline")
---------------------------------------------------------------------------

使用[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")不同类型池的常用方法是使用`poolclass`参数。该参数接受从`sqlalchemy.pool`模块导入的类，并处理为您构建池的详细信息。通用选项包括用SQLite指定[`QueuePool`](#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")：

    from sqlalchemy.pool import QueuePool
    engine = create_engine('sqlite:///file.db', poolclass=QueuePool)

使用[`NullPool`](#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")：

    from sqlalchemy.pool import NullPool
    engine = create_engine(
              'postgresql+psycopg2://scott:tiger@localhost/test',
              poolclass=NullPool)

使用自定义连接功能[¶](#using-a-custom-connection-function "Permalink to this headline")
---------------------------------------------------------------------------------------

所有[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")类接受一个参数`creator`，它是一个可调用的参数，用于创建新的连接。[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")接受这个函数通过一个同名的参数传递给池：

    import sqlalchemy.pool as pool
    import psycopg2

    def getconn():
        c = psycopg2.connect(username='ed', host='127.0.0.1', dbname='test')
        # do things with 'c' to set up
        return c

    engine = create_engine('postgresql+psycopg2://', creator=getconn)

对于大多数“初始化连接”例程，使用[`PoolEvents`](events.html#sqlalchemy.events.PoolEvents "sqlalchemy.events.PoolEvents")事件挂接更方便，因此[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的常用URL参数仍然可用。`creator` is there as a last resort for when a DBAPI has some form of
`connect` that is not at all supported by
SQLAlchemy.

构建一个池[¶](#constructing-a-pool "Permalink to this headline")
----------------------------------------------------------------

要单独使用[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")，`creator`函数是必需的唯一参数，并首先传递，然后是任何其他选项：

    import sqlalchemy.pool as pool
    import psycopg2

    def getconn():
        c = psycopg2.connect(username='ed', host='127.0.0.1', dbname='test')
        return c

    mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)

然后可以使用[`Pool.connect()`](#sqlalchemy.pool.Pool.connect "sqlalchemy.pool.Pool.connect")函数从池中获取DBAPI连接。此方法的返回值是包含在透明代理中的DBAPI连接：

    # get a connection
    conn = mypool.connect()

    # use it
    cursor = conn.cursor()
    cursor.execute("select foo")

透明代理的目的是拦截`close()`调用，这样就不会关闭DBAPI连接，而是返回到池：

    # "close" the connection.  Returns
    # it to the pool.
    conn.close()

代理还会在垃圾收集时将其包含的DBAPI连接返回到池中，尽管它在Python中并不是确定性的，它会立即发生（尽管它通常与cPython一起使用）。

`close()`步骤还执行调用DBAPI连接的`rollback()`方法的重要步骤。这样就可以删除连接上的任何现有事务，不仅可以确保在下次使用时不会保留现有状态，还可以释放表和行锁以及删除任何隔离的数据快照。可以使用[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")的`reset_on_return`选项禁用此行为。

通过将一个特定的预创建的[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")传递给[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的`pool`参数，可以与一个或多个引擎共享：

    e = create_engine('postgresql://', pool=mypool)

池事件[¶](#pool-events "Permalink to this headline")
----------------------------------------------------

连接池支持一个事件接口，该接口允许在第一次连接时，每次新建连接时以及在检出和检入连接时执行钩子。有关详细信息，请参见[`PoolEvents`](events.html#sqlalchemy.events.PoolEvents "sqlalchemy.events.PoolEvents")。

处理断开连接[¶](#dealing-with-disconnects "Permalink to this headline")
-----------------------------------------------------------------------

连接池可以刷新单个连接以及其整个连接集，将之前池连接设置为“无效”。一个常见的用例是允许连接池在数据库服务器重新启动时正常恢复，并且所有以前建立的连接都不再起作用。有两种方法来解决这个问题。

### 断开处理 - 乐观[¶](#disconnect-handling-optimistic "Permalink to this headline")

最常见的方法是让SQLAlchemy在发生时断开连接，此时会刷新池。这假定[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")与[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")结合使用。[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")具有可以检测断开事件并自动刷新池的逻辑。

当[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")尝试使用DBAPI连接，并且引发与“断开”事件相对应的异常时，连接将失效。然后，[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")调用[`Pool.recreate()`](#sqlalchemy.pool.Pool.recreate "sqlalchemy.pool.Pool.recreate")方法，有效地使所有当前未检出的连接失效，以便在下次检出时将其替换为新的连接：

    from sqlalchemy import create_engine, exc
    e = create_engine(...)
    c = e.connect()

    try:
        # suppose the database has been restarted.
        c.execute("SELECT * FROM table")
        c.close()
    except exc.DBAPIError, e:
        # an exception is raised, Connection is invalidated.
        if e.connection_invalidated:
            print("Connection was invalidated!")

    # after the invalidate event, a new connection
    # starts with a new Pool
    c = e.connect()
    c.execute("SELECT * FROM table")

上面的例子说明不需要特别干预，在检测到断开连接事件后，池正常继续。但是，引发了一个例外。在使用ORM
Session的典型Web应用程序中，上述条件将对应于单个请求失败并出现500错误，然后Web应用程序正常继续执行。因此这种方法是“乐观的”，因为频繁的数据库重启是不可预料的。

#### 设置池回收[¶](#setting-pool-recycle "Permalink to this headline")

可以增加“乐观”方法的其他设置是设置池回收参数。此参数可防止池使用特定时间的特定连接，并适用于数据库后端（如MySQL），该后端可自动关闭在特定时间段后过时的连接：

    from sqlalchemy import create_engine
    e = create_engine("mysql://scott:tiger@localhost/test", pool_recycle=3600)

以上，任何已打开超过一小时的DBAPI连接将在下次结帐时失效并被替换。请注意，仅在结帐时发生**失效**，而不是处于签出状态的任何连接。`pool_recycle`是[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")本身的函数，与是否使用[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")无关。

### 断开处理 - 悲观[¶](#disconnect-handling-pessimistic "Permalink to this headline")

以从池中检出的每个连接发出的额外SQL为代价，由checkout事件处理程序建立的“ping”操作可以在使用前检测到无效连接。在现代SQLAlchemy中，最好的方法是使用[`ConnectionEvents.engine_connect()`](events.html#sqlalchemy.events.ConnectionEvents.engine_connect "sqlalchemy.events.ConnectionEvents.engine_connect")事件，假设使用[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，而不仅仅是一个原始[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")对象：

    from sqlalchemy import exc
    from sqlalchemy import event
    from sqlalchemy import select

    some_engine = create_engine(...)

    @event.listens_for(some_engine, "engine_connect")
    def ping_connection(connection, branch):
        if branch:
            # "branch" refers to a sub-connection of a connection,
            # we don't want to bother pinging on these.
            return

        # turn off "close with result".  This flag is only used with
        # "connectionless" execution, otherwise will be False in any case
        save_should_close_with_result = connection.should_close_with_result
        connection.should_close_with_result = False

        try:
            # run a SELECT 1.   use a core select() so that
            # the SELECT of a scalar value without a table is
            # appropriately formatted for the backend
            connection.scalar(select([1]))
        except exc.DBAPIError as err:
            # catch SQLAlchemy's DBAPIError, which is a wrapper
            # for the DBAPI's exception.  It includes a .connection_invalidated
            # attribute which specifies if this connection is a "disconnect"
            # condition, which is based on inspection of the original exception
            # by the dialect in use.
            if err.connection_invalidated:
                # run the same SELECT again - the connection will re-validate
                # itself and establish a new connection.  The disconnect detection
                # here also causes the whole connection pool to be invalidated
                # so that all stale connections are discarded.
                connection.scalar(select([1]))
            else:
                raise
        finally:
            # restore "close with result"
            connection.should_close_with_result = save_should_close_with_result

上述配方的优点是，我们利用SQLAlchemy的工具来检测那些已知指示“断开”情况的DBAPI异常，以及[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")对象正确地使当前连接无效的能力当出现这种情况时允许当前的[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")重新验证到新的DBAPI连接。

对于不使用[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的情况下使用[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")的常见情况，可以使用较老的方法，如下所示：

    from sqlalchemy import exc
    from sqlalchemy import event
    from sqlalchemy.pool import Pool

    @event.listens_for(Pool, "checkout")
    def ping_connection(dbapi_connection, connection_record, connection_proxy):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SELECT 1")
        except:
            # raise DisconnectionError - pool will try
            # connecting again up to three times before raising.
            raise exc.DisconnectionError()
        cursor.close()

以上，[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")对象专门捕获[`DisconnectionError`](exceptions.html#sqlalchemy.exc.DisconnectionError "sqlalchemy.exc.DisconnectionError")，并尝试在放弃然后提升[`InvalidRequestError`](exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")之前创建新的DBAPI连接，最多三次。
，连接失败。上述方法的缺点是我们没有任何简单的方法来确定引发的异常是否是“断开”的情况，因为没有[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")

### 更多关于无效[¶](#more-on-invalidation "Permalink to this headline")

[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")提供了“连接无效”服务，它允许连接的显式失效以及响应于确定使连接不可用的条件的自动失效。

“无效”意味着特定的DBAPI连接将从池中删除并丢弃。如果不清楚连接本身可能未关闭，则在此连接上调用`.close()`方法，但如果此方法失败，则将记录异常，但操作仍在继续。

当使用[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")时，[`Connection.invalidate()`](connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")方法是通常显式失效的入口点。DBAPI连接可能失效的其他条件包括：

-   在调用诸如`connection.execute()`之类的方法时引发的诸如[`OperationalError`](exceptions.html#sqlalchemy.exc.OperationalError "sqlalchemy.exc.OperationalError")的DBAPI异常被检测为指示所谓的“断开”条件。由于Python
    DBAPI没有提供用于确定异常性质的标准系统，因此所有SQLAlchemy方言都包含称为`is_disconnect()`的系统，该系统将检查异常对象的内容，包括字符串消息和任何潜在的包含的错误代码，以确定此异常是否表示连接不再可用。如果是这种情况，则调用[`_ConnectionFairy.invalidate()`](#sqlalchemy.pool._ConnectionFairy.invalidate "sqlalchemy.pool._ConnectionFairy.invalidate")方法，然后丢弃DBAPI连接。
-   当连接返回到池，并调用`connection.rollback()`或`connection.commit()`方法时，由池的“reset on
    return”行为，抛出一个异常。在连接上调用`.close()`的最后一次尝试会被放弃，然后被放弃。
-   当实现[`PoolEvents.checkout()`](events.html#sqlalchemy.events.PoolEvents.checkout "sqlalchemy.events.PoolEvents.checkout")的侦听器引发[`DisconnectionError`](exceptions.html#sqlalchemy.exc.DisconnectionError "sqlalchemy.exc.DisconnectionError")异常时，表明连接将不可用，并且需要进行新的连接尝试。

所有发生的失效都将调用[`PoolEvents.invalidate()`](events.html#sqlalchemy.events.PoolEvents.invalidate "sqlalchemy.events.PoolEvents.invalidate")事件。

使用具有多处理功能的连接池[¶](#using-connection-pools-with-multiprocessing "Permalink to this headline")
--------------------------------------------------------------------------------------------------------

在使用连接池时，以及在使用通过[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")创建的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")时扩展至关重要的是，共享连接**不会共享到分叉进程
T6\>。**TCP连接表示为文件描述符，通常跨进程边界工作，这意味着这将导致代表两个或多个完全独立的Python解释器状态并发访问文件描述符。

有两种方法可以解决这个问题。

首先是在子进程内或在现有的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")内创建一个新的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，在子进程之前调用[`Engine.dispose()`](connections.html#sqlalchemy.engine.Engine.dispose "sqlalchemy.engine.Engine.dispose")进程使用任何连接。这将从池中删除所有现有的连接，以便它可以创建所有新的连接。下面是一个使用`multiprocessing.Process`的简单版本，但是这个想法应该适应使用中的分叉风格：

    eng = create_engine("...")

    def run_in_process():
      eng.dispose()

      with eng.connect() as conn:
          conn.execute("...")

    p = Process(target=run_in_process)

The next approach is to instrument the [`Pool`{.xref .py .py-class
.docutils .literal}](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
itself with events so that connections are automatically invalidated in
the subprocess. 这有点神奇，但可能更加万无一失：

    from sqlalchemy import event
    from sqlalchemy import exc
    import os

    eng = create_engine("...")

    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info['pid'] != pid:
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                    "Connection record belongs to pid %s, "
                    "attempting to check out in pid %s" %
                    (connection_record.info['pid'], pid)
            )

在上面，我们使用类似于[Disconnect Handling -
Pessimistic](#pool-disconnects-pessimistic)中描述的方法来将源自不同父进程的DBAPI连接视为“无效”连接，强制池将连接记录回收为建立新的连接。

API文档 - 可用的池实现[¶](#api-documentation-available-pool-implementations "Permalink to this headline")
---------------------------------------------------------------------------------------------------------

 *class*`sqlalchemy.pool.`{.descclassname}`Pool`{.descname}(*creator*, *recycle=-1*, *echo=None*, *use\_threadlocal=False*, *logging\_name=None*, *reset\_on\_return=True*, *listeners=None*, *events=None*, *\_dispatch=None*, *\_dialect=None*)[¶](#sqlalchemy.pool.Pool "Permalink to this definition")
:   基础：[`sqlalchemy.log.Identified`](internals.html#sqlalchemy.log.Identified "sqlalchemy.log.Identified")

    连接池的抽象基类。

     `__init__`{.descname}(*creator*, *recycle=-1*, *echo=None*, *use\_threadlocal=False*, *logging\_name=None*, *reset\_on\_return=True*, *listeners=None*, *events=None*, *\_dispatch=None*, *\_dialect=None*)[¶](#sqlalchemy.pool.Pool.__init__ "Permalink to this definition")
    :   构建一个池。

        参数：

        -   **creator**[¶](#sqlalchemy.pool.Pool.params.creator) – a
            callable function that returns a DB-API connection object.
            该函数将被调用参数。
        -   **recycle**[¶](#sqlalchemy.pool.Pool.params.recycle) – If
            set to non -1, number of seconds between connection
            recycling, which means upon checkout, if this timeout is
            surpassed the connection will be closed and replaced with a
            newly opened connection. 默认为-1。
        -   **logging\_name**[¶](#sqlalchemy.pool.Pool.params.logging_name)
            – String identifier which will be used within the “name”
            field of logging records generated within the
            “sqlalchemy.pool” logger. 缺省为对象ID的十六进制字符串。
        -   **echo**[¶](#sqlalchemy.pool.Pool.params.echo) – If True,
            connections being pulled and retrieved from the pool will be
            logged to the standard output, as well as pool sizing
            information.
            回声也可以通过启用“sqlalchemy.pool”命名空间的日志记录来实现。默认为False。
        -   **use\_threadlocal**
            [¶](#sqlalchemy.pool.Pool.params.use_threadlocal) -

            如果设置为True，在同一个应用程序线程中重复调用[`connect()`{.xref
            .py .py-meth .docutils
            .literal}](#sqlalchemy.pool.Pool.connect "sqlalchemy.pool.Pool.connect")将保证返回相同的连接对象（如果已从池中检索到并且尚未返回）。默认情况下以单个交易为代价提供轻微的性能优势。提供了[`Pool.unique_connection()`{.xref
            .py .py-meth .docutils
            .literal}](#sqlalchemy.pool.Pool.unique_connection "sqlalchemy.pool.Pool.unique_connection")方法来返回一致的唯一连接，以在设置标志时绕过此行为。

            警告

            [`Pool.use_threadlocal`{.xref .py .py-paramref .docutils
            .literal}](#sqlalchemy.pool.Pool.params.use_threadlocal "sqlalchemy.pool.Pool")标志**不会影响[`Engine.connect()`{.xref
            .py .py-meth .docutils
            .literal}](connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect")的行为。**[`Engine.connect()`{.xref
            .py .py-meth .docutils
            .literal}](connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect")
            makes use of the [`Pool.unique_connection()`{.xref .py
            .py-meth .docutils
            .literal}](#sqlalchemy.pool.Pool.unique_connection "sqlalchemy.pool.Pool.unique_connection")
            method which **does not use thread local context**.
            要产生引用[`Pool.connect()`{.xref .py .py-meth .docutils
            .literal}](#sqlalchemy.pool.Pool.connect "sqlalchemy.pool.Pool.connect")方法的[`Connection`{.xref
            .py .py-class .docutils
            .literal}](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")，请使用[`Engine.contextual_connect()`{.xref
            .py .py-meth .docutils
            .literal}](connections.html#sqlalchemy.engine.Engine.contextual_connect "sqlalchemy.engine.Engine.contextual_connect")。

            请注意，其他SQLAlchemy连接系统如[`Engine.execute()`{.xref
            .py .py-meth .docutils
            .literal}](connections.html#sqlalchemy.engine.Engine.execute "sqlalchemy.engine.Engine.execute")以及orm
            [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")在内部使用[`Engine.contextual_connect()`{.xref
            .py .py-meth .docutils
            .literal}](connections.html#sqlalchemy.engine.Engine.contextual_connect "sqlalchemy.engine.Engine.contextual_connect")所以这些功能与[`Pool.use_threadlocal`](#sqlalchemy.pool.Pool.params.use_threadlocal "sqlalchemy.pool.Pool")设置兼容。

            也可以看看

            [Using the Threadlocal Execution
            Strategy](connections.html#threadlocal-strategy) - contains
            detail on the “threadlocal” engine strategy, which provides
            a more comprehensive approach to “threadlocal” connectivity
            for the specific use case of using [`Engine`{.xref .py
            .py-class .docutils
            .literal}](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            and [`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            objects directly.

        -   **reset\_on\_return**
            [¶](#sqlalchemy.pool.Pool.params.reset_on_return) -

            确定在连接返回到池时执行的连接步骤。reset\_on\_return可以具有以下任何值：

            -   `"rollback"` -
                在连接上调用rollback()来释放锁和事务资源。这是默认值。绝大多数用例都应该保留这个值。
            -   `True` -
                与'rollback'相同，这是为了向后兼容。
            -   `"commit"` -
                在连接上调用commit()来释放锁和事务资源。对于在发出提交时缓存查询计划的数据库（如Microsoft
                SQL
                Server），此处的提交可能是可取的。然而，这个值比'回滚'更危险，因为交易中出现的任何数据变化都是无条件承诺的。
            -   `None` -
                不要在连接上做任何事情。这个设置只能在没有事务支持的数据库上进行，即MySQL
                MyISAM。没有做任何事情，性能可以提高。This setting
                should **never be selected** for a database that
                supports transactions, as it will lead to deadlocks and
                stale state.
            -   `"none"` - 与`None`{.docutils
                .literal}相同

                版本0.9.10中的新功能

            -   `False` -
                与None相同，这是为了向后兼容。

            Changed in version 0.7.6: [`Pool.reset_on_return`{.xref .py
            .py-paramref .docutils
            .literal}](#sqlalchemy.pool.Pool.params.reset_on_return "sqlalchemy.pool.Pool")
            accepts `"rollback"` and
            `"commit"` arguments.

        -   **events**[¶](#sqlalchemy.pool.Pool.params.events) – a list
            of 2-tuples, each of the form `(callable, target)`{.docutils
            .literal} which will be passed to [`event.listen()`{.xref
            .py .py-func .docutils
            .literal}](event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")
            upon construction.
            在此处提供，以便可以在应用方言级侦听器之前通过[`create_engine()`{.xref
            .py .py-func .docutils
            .literal}](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")分配事件侦听器。
        -   **听众** [¶](#sqlalchemy.pool.Pool.params.listeners) -
            弃用。类似于[`PoolListener`](interfaces.html#sqlalchemy.interfaces.PoolListener "sqlalchemy.interfaces.PoolListener")的对象或可调用字典的列表，这些对象或字典在DB-API连接创建，检出并签入池时接收事件。这已被[`listen()`{.xref
            .py .py-func .docutils
            .literal}](event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")取代。

    `连接 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   从池中返回一个DBAPI连接。

        这个连接被调用，当它的`close()`方法被调用时，连接将被返回到池中。

    `处置 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   处置这个池。

        这种方法使检出连接保持开放的可能性，因为它只影响在池中空闲的连接。

        另请参阅[`Pool.recreate()`](#sqlalchemy.pool.Pool.recreate "sqlalchemy.pool.Pool.recreate")方法。

    `重新创建 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回一个新的[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")，它与这个相同的类，并配置相同的创建参数。

        此方法与[`dispose()`](#sqlalchemy.pool.Pool.dispose "sqlalchemy.pool.Pool.dispose")结合使用，以关闭整个[`Pool`{.xref
        .py .py-class .docutils
        .literal}](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")并在其位置创建一个新的。

    ` unique_connection  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   生成一个没有被任何线程本地上下文引用的DBAPI连接。

        当[`Pool.use_threadlocal`{.xref .py .py-paramref .docutils
        .literal}](#sqlalchemy.pool.Pool.params.use_threadlocal "sqlalchemy.pool.Pool")标志未设置为True时，此方法等同于[`Pool.connect()`](#sqlalchemy.pool.Pool.connect "sqlalchemy.pool.Pool.connect")。当[`Pool.use_threadlocal`](#sqlalchemy.pool.Pool.params.use_threadlocal "sqlalchemy.pool.Pool")为True时，[`Pool.unique_connection()`](#sqlalchemy.pool.Pool.unique_connection "sqlalchemy.pool.Pool.unique_connection")方法提供绕过threadlocal上下文的方法。

 *class*`sqlalchemy.pool.`{.descclassname}`QueuePool`{.descname}(*creator*, *pool\_size=5*, *max\_overflow=10*, *timeout=30*, *\*\*kw*)[¶](#sqlalchemy.pool.QueuePool "Permalink to this definition")
:   基础：[`sqlalchemy.pool.Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

    一个[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")，对打开的连接数量施加限制。

    [`QueuePool`](#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
    is the default pooling implementation used for all [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    objects, unless the SQLite dialect is in use.

     `__init__`{.descname}(*creator*, *pool\_size=5*, *max\_overflow=10*, *timeout=30*, *\*\*kw*)[¶](#sqlalchemy.pool.QueuePool.__init__ "Permalink to this definition")
    :   构建一个QueuePool。

        参数：

        -   **creator**[¶](#sqlalchemy.pool.QueuePool.params.creator) –
            a callable function that returns a DB-API connection object,
            same as that of [`Pool.creator`{.xref .py .py-paramref
            .docutils
            .literal}](#sqlalchemy.pool.Pool.params.creator "sqlalchemy.pool.Pool").
        -   **pool\_size**[¶](#sqlalchemy.pool.QueuePool.params.pool_size)
            – The size of the pool to be maintained, defaults to 5.
            这是将永久保存在池中的最大数量的连接。请注意，池开始时没有连接；一旦请求连接数量，连接数量将保持不变。`pool_size`{.docutils
            .literal} can be set to 0 to indicate no size limit; to
            disable pooling, use a [`NullPool`](#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")
            instead.
        -   **max\_overflow**
            [¶](#sqlalchemy.pool.QueuePool.params.max_overflow) -
            池的最大溢出大小。当检出连接的数量达到pool\_size中设置的大小时，其他连接将返回到此限制。当这些附加连接返回到池时，它们将被断开并丢弃。It
            follows then that the total number of simultaneous
            connections the pool will allow is pool\_size +
            max\_overflow, and the total number of “sleeping”
            connections the pool will allow is pool\_size. max\_overflow
            can be set to -1 to indicate no overflow limit; no limit
            will be placed on the total number of concurrent
            connections. 默认为10。
        -   **timeout**[¶](#sqlalchemy.pool.QueuePool.params.timeout) –
            The number of seconds to wait before giving up on returning
            a connection. 默认为30。
        -   **\*\*kw**[¶](#sqlalchemy.pool.QueuePool.params.**kw) –
            Other keyword arguments including [`Pool.recycle`{.xref .py
            .py-paramref .docutils
            .literal}](#sqlalchemy.pool.Pool.params.recycle "sqlalchemy.pool.Pool"),
            [`Pool.echo`{.xref .py .py-paramref .docutils
            .literal}](#sqlalchemy.pool.Pool.params.echo "sqlalchemy.pool.Pool"),
            [`Pool.reset_on_return`{.xref .py .py-paramref .docutils
            .literal}](#sqlalchemy.pool.Pool.params.reset_on_return "sqlalchemy.pool.Pool")
            and others are passed to the [`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
            constructor.

    `连接 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`connect()`](#sqlalchemy.pool.Pool.connect "sqlalchemy.pool.Pool.connect")
        *method of* [`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

        从池中返回一个DBAPI连接。

        这个连接被调用，当它的`close()`方法被调用时，连接将被返回到池中。

    ` unique_connection  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`unique_connection()`](#sqlalchemy.pool.Pool.unique_connection "sqlalchemy.pool.Pool.unique_connection")
        *method of* [`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

        生成一个没有被任何线程本地上下文引用的DBAPI连接。

        当[`Pool.use_threadlocal`{.xref .py .py-paramref .docutils
        .literal}](#sqlalchemy.pool.Pool.params.use_threadlocal "sqlalchemy.pool.Pool")标志未设置为True时，此方法等同于[`Pool.connect()`](#sqlalchemy.pool.Pool.connect "sqlalchemy.pool.Pool.connect")。当[`Pool.use_threadlocal`](#sqlalchemy.pool.Pool.params.use_threadlocal "sqlalchemy.pool.Pool")为True时，[`Pool.unique_connection()`](#sqlalchemy.pool.Pool.unique_connection "sqlalchemy.pool.Pool.unique_connection")方法提供绕过threadlocal上下文的方法。

*class* `sqlalchemy.pool。`{.descclassname} `SingletonThreadPool`{.descname} （ *creator*，*pool\_size = 5*，*\*\* kw* ） [¶](#sqlalchemy.pool.SingletonThreadPool "Permalink to this definition")
:   基础：[`sqlalchemy.pool.Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

    每个线程维护一个连接的池。

    每个线程维护一个连接，永远不会将连接移动到除创建它之外的线程。

    警告

    [`SingletonThreadPool`](#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")将在存在超过`pool_size`大小设置的任意连接上调用`.close()`。如果更多的唯一**线程标识**比使用`pool_size`状态。这种清理是非确定性的，并且对链接到这些线程标识的连接是否当前正在使用不敏感。

    [`SingletonThreadPool`](#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")
    may be improved in a future release, however in its current status
    it is generally used only for test scenarios using a SQLite
    `:memory:` database and is not recommended for
    production use.

    选项与[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")的选项相同，以及：

    参数：

    **pool\_size**
    [¶](#sqlalchemy.pool.SingletonThreadPool.params.pool_size) -
    一次维护连接的线程数。默认为五。

    [`SingletonThreadPool`](#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")
    is used by the SQLite dialect automatically when a memory-based
    database is used. 请参阅[SQLite](dialects_sqlite.html)。

     `__init__`{.descname}(*creator*, *pool\_size=5*, *\*\*kw*)[¶](#sqlalchemy.pool.SingletonThreadPool.__init__ "Permalink to this definition")
    :   

*class* `sqlalchemy.pool。`{.descclassname} `AssertionPool`{.descname} （ *\* args*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.pool.AssertionPool "Permalink to this definition")*
:   基础：[`sqlalchemy.pool.Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

    一个[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")，允许在任何给定的时间最多检出一个连接。

    如果同时检出多个连接，则会引发异常。用于调试使用比期望更多连接的代码。

    Changed in version 0.7: [`AssertionPool`](#sqlalchemy.pool.AssertionPool "sqlalchemy.pool.AssertionPool")
    also logs a traceback of where the original connection was checked
    out, and reports this in the assertion error raised.

*class* `sqlalchemy.pool。`{.descclassname} `NullPool`{.descname} （ *creator*，*recycle = 1*，*echo = None*，*use\_threadlocal = False*，*logging\_name = None*，*reset\_on\_return = True*， *listeners = None*，*events = None*，*\_dispatch = None*，*\_dialect = None* ） t14 \> [¶ T15\>](#sqlalchemy.pool.NullPool "Permalink to this definition")
:   基础：[`sqlalchemy.pool.Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

    不共享连接的池。

    相反，它打开并关闭每个打开/关闭连接的底层DB-API连接。

    此池实现不支持重新连接相关函数，如`recycle`和连接失效，因为没有连接持久存在。

    Changed in version 0.7: [`NullPool`](#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool") is
    used by the SQlite dialect automatically when a file-based database
    is used. 请参阅[SQLite](dialects_sqlite.html)。

*class* `sqlalchemy.pool。`{.descclassname} `StaticPool`{.descname} （ *creator*，*recycle = 1*，*echo = None*，*use\_threadlocal = False*，*logging\_name = None*，*reset\_on\_return = True*， *listeners = None*，*events = None*，*\_dispatch = None*，*\_dialect = None* ） t14 \> [¶ T15\>](#sqlalchemy.pool.StaticPool "Permalink to this definition")
:   基础：[`sqlalchemy.pool.Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")

    完全由一个连接组成的池，用于所有请求。

    此池实施当前不支持重新连接相关的功能，如`recycle`和连接失效（也用于支持自动重新连接），但可以在未来版本中实施。

 *class*`sqlalchemy.pool.`{.descclassname}`_ConnectionFairy`{.descname}(*dbapi\_connection*, *connection\_record*, *echo*)[¶](#sqlalchemy.pool._ConnectionFairy "Permalink to this definition")
:   代理一个DBAPI连接并提供返回解除引用支持。

    这是[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")实现用于为由[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")提供的DBAPI连接提供上下文管理的内部对象。

    “fairy”这个名字的灵感来自于[`_ConnectionFairy`](#sqlalchemy.pool._ConnectionFairy "sqlalchemy.pool._ConnectionFairy")对象的生命周期是暂时的，因为它只持续从池中检出特定DBAPI连接的长度，另外还有一个透明代理，它大部分是看不见的。

    也可以看看

    [`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")

    `_connection_record`{.descname} *=无* [¶](#sqlalchemy.pool._ConnectionFairy._connection_record "Permalink to this definition")
    :   对与DBAPI连接关联的[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")对象的引用。

        目前这是一个可能会改变的内部存取器。

    `连接`{.descname} *=无* [¶](#sqlalchemy.pool._ConnectionFairy.connection "Permalink to this definition")
    :   对正在跟踪的实际DBAPI连接的引用。

    `游标`{.descname} （ *\* args*，*\*\* kwargs* ） [T5\>](#sqlalchemy.pool._ConnectionFairy.cursor "Permalink to this definition")
    :   为基础连接返回一个新的DBAPI游标。

        此方法是`connection.cursor()`
        DBAPI方法的代理。

    `分离 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   将此连接与其池分开。

        这意味着关闭时连接将不再返回到池中，而是直接关闭。包含的ConnectionRecord与DB-API连接分开，并在下次使用时创建一个新连接。

        请注意，由于分离后的连接已从池的知识和控制中移除，因此可能会在分离之后违反池实施施加的任何总体连接限制约束。

    `信息 T0> ¶ T1>`{.descname}
    :   信息字典与该`ConnectionFairy`引用的底层DBAPI连接关联，允许用户定义的数据与连接相关联。

        这里的数据将与DBAPI连接一起进行，包括返回到连接池之后，并在[`_ConnectionFairy`{.xref
        .py .py-class .docutils
        .literal}](#sqlalchemy.pool._ConnectionFairy "sqlalchemy.pool._ConnectionFairy")的后续实例中再次使用。它与[`_ConnectionRecord.info`{.xref
        .py .py-attr .docutils
        .literal}](#sqlalchemy.pool._ConnectionRecord.info "sqlalchemy.pool._ConnectionRecord.info")和[`Connection.info`{.xref
        .py .py-attr .docutils
        .literal}](connections.html#sqlalchemy.engine.Connection.info "sqlalchemy.engine.Connection.info")访问器共享。

     `invalidate`{.descname}(*e=None*, *soft=False*)[¶](#sqlalchemy.pool._ConnectionFairy.invalidate "Permalink to this definition")
    :   将此连接标记为无效。

        此方法可以直接调用，也可以作为[`Connection.invalidate()`](connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")方法的结果调用。当被调用时，DBAPI连接会立即关闭并被池中的进一步使用丢弃。失效机制通过[`_ConnectionRecord.invalidate()`](#sqlalchemy.pool._ConnectionRecord.invalidate "sqlalchemy.pool._ConnectionRecord.invalidate")内部方法进行。

        参数：

        -   **e**
            [¶](#sqlalchemy.pool._ConnectionFairy.invalidate.params.e) -
            指示无效原因的异常对象。
        -   **soft tt\>
            [¶](#sqlalchemy.pool._ConnectionFairy.invalidate.params.soft)
            -**

            如果为True，则连接未关闭；相反，此连接将在下次结帐时回收。

            版本1.0.3中的新功能

        也可以看看

        [More on Invalidation](#pool-connection-invalidation)

    ` is_valid  T0> ¶ T1>`{.descname}
    :   如果[`_ConnectionFairy`](#sqlalchemy.pool._ConnectionFairy "sqlalchemy.pool._ConnectionFairy")仍然指向活动的DBAPI连接，则返回True。

*class* `sqlalchemy.pool。`{.descclassname} `_ConnectionRecord`{.descname} （ *pool* ） t5 \> [¶ T6\>](#sqlalchemy.pool._ConnectionRecord "Permalink to this definition")
:   内部对象，它维护由[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")引用的单个DBAPI连接。

    对于任何特定的DBAPI连接，[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")对象总是存在，而不管该DBAPI连接是否已“检出”。这与[`_ConnectionFairy`](#sqlalchemy.pool._ConnectionFairy "sqlalchemy.pool._ConnectionFairy")形成鲜明对比，它仅在检出时才是DBAPI连接的公共外观。

    一个[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")的存在时间可能比单个DBAPI连接的时间长。例如，如果调用[`_ConnectionRecord.invalidate()`](#sqlalchemy.pool._ConnectionRecord.invalidate "sqlalchemy.pool._ConnectionRecord.invalidate")方法，则与此[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")关联的DBAPI连接将被丢弃，但[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")可以再次使用，在这种情况下，当[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")下一次使用此记录时会生成新的DBAPI连接。

    [`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")与连接池事件一起交付，包括[`PoolEvents.connect()`](events.html#sqlalchemy.events.PoolEvents.connect "sqlalchemy.events.PoolEvents.connect")和[`PoolEvents.checkout()`](events.html#sqlalchemy.events.PoolEvents.checkout "sqlalchemy.events.PoolEvents.checkout")，但[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")

    也可以看看

    [`_ConnectionFairy`](#sqlalchemy.pool._ConnectionFairy "sqlalchemy.pool._ConnectionFairy")

    `连接`{.descname} *=无* [¶](#sqlalchemy.pool._ConnectionRecord.connection "Permalink to this definition")
    :   对正在跟踪的实际DBAPI连接的引用。

        如果[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")已被标记为无效，则可能`None`；如果拥有的池调用此[`_ConnectionRecord`{.xref .py
        .py-class .docutils
        .literal}](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")重新连接，则新的DBAPI连接可能会替换它。

    `信息 T0> ¶ T1>`{.descname}
    :   与DBAPI连接关联的`.info`字典。

        该字典在[`_ConnectionFairy.info`{.xref .py .py-attr .docutils
        .literal}](#sqlalchemy.pool._ConnectionFairy.info "sqlalchemy.pool._ConnectionFairy.info")和[`Connection.info`{.xref
        .py .py-attr .docutils
        .literal}](connections.html#sqlalchemy.engine.Connection.info "sqlalchemy.engine.Connection.info")访问器中共享。

     `invalidate`{.descname}(*e=None*, *soft=False*)[¶](#sqlalchemy.pool._ConnectionRecord.invalidate "Permalink to this definition")
    :   使此[`_ConnectionRecord`](#sqlalchemy.pool._ConnectionRecord "sqlalchemy.pool._ConnectionRecord")持有的DBAPI连接失效。

        此方法针对所有连接失效而被调用，包括调用[`_ConnectionFairy.invalidate()`](#sqlalchemy.pool._ConnectionFairy.invalidate "sqlalchemy.pool._ConnectionFairy.invalidate")或[`Connection.invalidate()`](connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")方法时，以及何时调用任何所谓的“自动失效“情况发生。

        参数：

        -   **e**
            [¶](#sqlalchemy.pool._ConnectionRecord.invalidate.params.e)
            - 指示无效原因的异常对象。
        -   **soft tt\>
            [¶](#sqlalchemy.pool._ConnectionRecord.invalidate.params.soft)
            -**

            如果为True，则连接未关闭；相反，此连接将在下次结帐时回收。

            版本1.0.3中的新功能

        也可以看看

        [More on Invalidation](#pool-connection-invalidation)

汇集普通DB-API连接[¶](#pooling-plain-db-api-connections "Permalink to this headline")
-------------------------------------------------------------------------------------

任何 [**PEP 249**](https://www.python.org/dev/peps/pep-0249)
DB-API模块都可透明地通过连接池进行“代理”。除了`connect()`方法将查询池之外，DB-API的用法与以前完全相同。下面我们用`psycopg2`来说明这一点：

    import sqlalchemy.pool as pool
    import psycopg2 as psycopg

    psycopg = pool.manage(psycopg)

    # then connect normally
    connection = psycopg.connect(database='test', username='scott',
                                 password='tiger')

这产生一个`_DBProxy`对象，它支持与原始DB-API模块相同的`connect()`函数。连接时，返回一个连接代理对象，它将其调用委托给一个真实的DB-API连接对象。这个连接对象被持久地存储在连接池（[`Pool`](#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")的一个实例）中，该连接池对应于发送给`connect()`函数的确切连接参数。

连接代理支持原始连接对象上的所有方法，其中大部分通过`__getattr__()`进行代理。`close()`方法将返回到池的连接，并且`cursor()`方法将返回一个代理游标对象。Both the connection proxy and the
cursor proxy will also return the underlying connection to the pool
after they have both been garbage collected, which is detected via
weakref callbacks (`__del__` is not used).

此外，当连接返回到池时，无条件地在连接上发出`rollback()`。这是释放可能由正常活动导致的连接仍然存在的任何锁定。

默认情况下，`connect()`方法将返回已经在当前线程中检出的相同连接。这允许在给定的线程中使用特定的连接，而不需要在功能之间传递它。要禁用此行为，请为`manage()`函数指定`use_threadlocal=False`。

`sqlalchemy.pool。`{.descclassname} `manage`{.descname} （ *module*，*\*\* params* ） T5\> [¶ T6\>](#sqlalchemy.pool.manage "Permalink to this definition")
:   返回一个DB-API模块的代理，该模块自动将连接集中在一起。

    给定一个DB-API
    2.0模块和池管理参数，为模块返回一个代理，该模块将自动汇集连接，为发送到装饰模块的connect()函数的每个不同的连接参数集创建新的连接池。

    参数：

    -   **模块** [¶](#sqlalchemy.pool.manage.params.module) - DB-API
        2.0数据库模块
    -   **poolclass**[¶](#sqlalchemy.pool.manage.params.poolclass) – the
        class used by the pool module to provide pooling.
        默认为[`QueuePool`](#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")。
    -   **\*\*params**[¶](#sqlalchemy.pool.manage.params.**params) –
        will be passed through to *poolclass*

` sqlalchemy.pool。 T0>  clear_managers  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   删除所有当前的DB-API 2.0管理器。

    所有游泳池和连接都被丢弃。


