---
title: 引擎配置
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/core/engines/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
引擎配置[¶](#engine-configuration "Permalink to this headline")
===============================================================

[`引擎`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")是任何 SQLAlchemy 应用程序的基础。它是实际数据库及其[DBAPI](glossary.html#term-dbapi)的“主基”，通过连接池和[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")传递给 SQLAlchemy 应用程序，该应用程序描述了如何与特定类型的数据库/
DBAPI 组合。

一般结构如下：

![](http://sqlalchemy.readthedocs.io/en/latest/_images/sqla_engine_arch.png)

在上面，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")引用了[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")和[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")，它们共同解释了 DBAPI 的模块功能以及数据库的行为。

只用一个调用就可以创建引擎，[`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")：

    from sqlalchemy import create_engineplain
    engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')

The above engine creates a [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
object tailored towards PostgreSQL, as well as a [`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
object which will establish a DBAPI connection at
`localhost:5432` when a connection request is first
received.Note that the [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
and its underlying [`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool") do
**not** establish the first actual DBAPI connection until the
[`Engine.connect()`](connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect")
method is called, or an operation which is dependent on this method such
as [`Engine.execute()`](connections.html#sqlalchemy.engine.Engine.execute "sqlalchemy.engine.Engine.execute")
is invoked. In this way, [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
and [`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool") can
be said to have a *lazy initialization* behavior.

[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")一旦创建，可以直接用于与数据库进行交互，也可以将其传递给[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象以使用 ORM。本节将介绍配置[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的详细信息。下一节[Working
with Engines and Connections](connections.html)将详细介绍[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的类似 API，通常用于非 ORM 应用程序。

支持的数据库[¶](#supported-databases "Permalink to this headline")
------------------------------------------------------------------

SQLAlchemy includes many [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
implementations for various backends.
最常用数据库的方言包含在 SQLAlchemy 中；少数其他人需要另外安装一个单独的方言。

有关各种可用后端的信息，请参阅[Dialects](dialects_index.html)部分。

数据库网址[¶](#database-urls "Permalink to this headline")
----------------------------------------------------------

[`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")函数根据 URL 生成一个[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")对象。这些 URL 遵循[RFC-1738](http://rfc.net/rfc1738.html)，通常可以包含用户名，密码，主机名，数据库名称以及用于其他配置的可选关键字参数。在某些情况下，接受文件路径，而在其他情况下，“数据源名称”替换“主机”和“数据库”部分。数据库 URL 的典型形式是：

    dialect+driver://username:password@host:port/database

方言名称包括 SQLAlchemy 方言的名称，名称如`sqlite`，`mysql`，`postgresql`，`oracle` ，或`mssql`。drivername 是用于使用全部小写字母连接到数据库的 DBAPI 的名称。如果未指定，则将导入“默认”DBAPI（如果可用）
- 此默认值通常是该后端可用的最广泛的驱动程序。

以下是常用连接样式的示例。有关所有包含方言的详细信息的完整索引以及第三方方言的链接，请参见[Dialects](dialects_index.html)。

### 的 PostgreSQL [¶ T0\>](#postgresql "Permalink to this headline")

Postgresql 方言使用 psycopg2 作为默认的 DBAPI。pg8000 也可用作纯 Python 替代品：

    # default
    engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')

    # psycopg2
    engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

    # pg8000
    engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')

有关在[PostgreSQL](dialects_postgresql.html)连接到 Postgresql 的更多注意事项。

### MySQL 的[¶ T0\>](#mysql "Permalink to this headline")

MySQL 方言使用 mysql-python 作为默认的 DBAPI。有许多 MySQL
DBAPI 可用，包括 MySQL 连接器-python 和 OurSQL：

    # default
    engine = create_engine('mysql://scott:tiger@localhost/foo')

    # mysql-python
    engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

    # MySQL-connector-python
    engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')

    # OurSQL
    engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')

有关在[MySQL](dialects_mysql.html)连接到 MySQL 的更多注意事项。

### 甲骨文[¶ T0\>](#oracle "Permalink to this headline")

Oracle 方言使用 cx\_oracle 作为默认的 DBAPI：

    engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')

    engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')

有关在[Oracle](dialects_oracle.html)连接到 Oracle 的更多注意事项。

### Microsoft SQL Server [¶](#microsoft-sql-server "Permalink to this headline")

SQL Server 方言使用 pyodbc 作为默认 DBAPI。pymssql 也可用：

    # pyodbcplain
    engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')

    # pymssql
    engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')

有关在[Microsoft SQL Server](dialects_mssql.html)连接到 SQL
Server 的更多注意事项。

### SQLite 的[¶ T0\>](#sqlite "Permalink to this headline")

SQLite 默认使用 Python 内置模块`sqlite3`连接到基于文件的数据库。

由于 SQLite 连接到本地文件，URL 格式略有不同。URL 的“文件”部分是数据库的文件名。对于相对文件路径，这需要三个斜杠：

    # sqlite://<nohostname>/<path>
    # where <path> is relative:
    engine = create_engine('sqlite:///foo.db')

对于绝对文件路径，三个斜杠后面是绝对路径：

    #Unix/Mac - 4 initial slashes in total
    engine = create_engine('sqlite:////absolute/path/to/foo.db')
    #Windows
    engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
    #Windows alternative using raw string
    engine = create_engine(r'sqlite:///C:\path\to\foo.db')

要使用 SQLite `:memory:`数据库，请指定一个空的 URL：

    engine = create_engine('sqlite://')

有关在[SQLite](dialects_sqlite.html)连接到 SQLite 的更多注意事项。

### 其他[¶ T0\>](#others "Permalink to this headline")

请参阅[Dialects](dialects_index.html)，这是所有其他方言文档的顶级页面。

引擎创建 API [¶](#engine-creation-api "Permalink to this headline")
------------------------------------------------------------------

`sqlalchemy。`{.descclassname} `create_engine`{.descname} （ *\* args*，*\*\* kwargs* / T5\> [¶ T6\>](#sqlalchemy.create_engine "Permalink to this definition")
:   创建一个新的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")实例。

    标准调用形式是将URL作为第一个位置参数发送，通常是指示数据库方言和连接参数的字符串：plain

        engine = create_engine("postgresql://scott:tiger@localhost/test")

    附加的关键字参数可以在它后面建立，它们在结果[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")及其底层[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")和[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")结构上建立各种选项：

        engine = create_engine("mysql://scott:tiger@hostname/dbname",
                                    encoding='latin1', echo=True)

    URL的字符串形式是`dialect[+driver]://user:password@host/dbname[?key=value..]`，其中`dialect`是一个数据库名称，如`mysql`，`oracle`，`postgresql`等，`driver`
    DBAPI的名称，例如`psycopg2`，`pyodbc`，`cx_oracle`等或者，该URL可以是[`URL`](#sqlalchemy.engine.url.URL "sqlalchemy.engine.url.URL")的实例。

    `**kwargs` takes a wide variety of options which
    are routed towards their appropriate components.
    参数可能特定于[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，底层的[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")以及[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")。特定的方言也接受该方言所独有的关键字参数。Here,
    we describe the parameters that are common to most
    [`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")
    usage.

    一旦建立，一旦[`Engine.connect()`](connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect")被调用，新生成的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")将请求来自底层[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")的连接，例如[`Engine.execute()`](connections.html#sqlalchemy.engine.Engine.execute "sqlalchemy.engine.Engine.execute")被调用。当接收到这个请求时，[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")反过来将建立第一个实际的DBAPI连接。The
    [`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")
    call itself does **not** establish any actual DBAPI connections
    directly.

    也可以看看

    [*Engine Configuration*]()

    [*Dialects*](dialects_index.html)

    [Working with Engines and Connections](connections.html)

    参数：

    -   **case\_sensitive = True**
        [¶](#sqlalchemy.create_engine.params.case_sensitive) -

        if False, result column names will match in a case-insensitive
        fashion, that is, `row['SomeColumn']`.

        在版本0.8中更改：默认情况下，结果行名称区分大小写。在版本0.7和之前的版本中，所有匹配都不区分大小写。

    -   **connect\_args**[¶](#sqlalchemy.create_engine.params.connect_args)
        – a dictionary of options which will be passed directly to the
        DBAPI’s `connect()` method as additional
        keyword arguments. 请参阅[Custom DBAPI connect()
        arguments](#custom-dbapi-args)中的示例。
    -   **convert\_unicode = False**
        [¶](#sqlalchemy.create_engine.params.convert_unicode) -

        if set to True, sets the default behavior of
        `convert_unicode` on the [`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
        type to `True`, regardless of a setting of
        `False` on an individual [`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
        type, thus causing all [`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
        -based columns to accommodate Python `unicode` objects. 当使用不支持本地支持Python
        `unicode`对象的DBAPI时，该标志可用作引擎范围的设置，并在收到一个错误时引发错误（如带有FreeTDS的pyodbc）。

        有关此标志指示的更多详细信息，请参阅[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")。

    -   **creator** [¶](#sqlalchemy.create_engine.params.creator) -
        返回DBAPI连接的可调用对象。这个创建函数将被传递到底层连接池，并将用于创建所有新的数据库连接。该函数的使用会导致URL参数中指定的连接参数被绕过。
    -   **echo=False**[¶](#sqlalchemy.create_engine.params.echo) – if
        True, the Engine will log all statements as well as a repr() of
        their parameter lists to the engines logger, which defaults to
        sys.stdout. 可以随时修改`Engine`的`echo`属性，以打开和关闭日志记录。如果设置为字符串`"debug"`，结果行也会打印到标准输出。这个标志最终控制着一个Python记录器；有关如何直接配置日志记录的信息，请参阅[Configuring
        Logging](#dbengine-logging)。
    -   **echo\_pool=False**[¶](#sqlalchemy.create_engine.params.echo_pool)
        – if True, the connection pool will log all checkouts/checkins
        to the logging stream, which defaults to sys.stdout.
        这个标志最终控制着一个Python记录器；有关如何直接配置日志记录的信息，请参阅[Configuring
        Logging](#dbengine-logging)。
    -   **编码** [¶](#sqlalchemy.create_engine.params.encoding) -

        默认为`utf-8`。This is the string encoding
        used by SQLAlchemy for string encode/decode operations which
        occur within SQLAlchemy, **outside of the
        DBAPI.**大多数现代的DBAPI都具有对Python `unicode`对象的一定程度的直接支持，您在Python
        2中看到的形式为`u'some 字符串“ T4>  T2>。`对于DBAPI被检测为不支持Python `unicode`对象的情况，此编码用于确定源/目标编码。对于DBAPI直接处理unicode的情况，**未使用**。

        要正确配置系统以适应Python `unicode`对象，应该将DBAPI配置为根据需要最大程度地处理unicode -
        请参阅[Dialects](dialects_index.html)

        可能需要在DBAPI之外容纳字符串编码的领域包括零个或多个：

        -   the values passed to bound parameters, corresponding to the
            [`Unicode`](type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
            type or the [`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
            type when `convert_unicode` is
            `True`;
        -   the values returned in result set columns corresponding to
            the [`Unicode`](type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
            type or the [`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
            type when `convert_unicode` is
            `True`;
        -   将字符串SQL语句传递给DBAPI的`cursor.execute()`方法；
        -   绑定参数字典中的键的字符串名称传递给DBAPI的`cursor.execute()`以及`cursor.setinputsizes()`方法；
        -   从DBAPI的`cursor.description`属性中检索的字符串列名称。

        When using Python 3, the DBAPI is required to support *all* of
        the above values as Python `unicode`
        objects, which in Python 3 are just known as `str`. 在Python
        2中，DBAPI根本没有指定unicode行为，所以SQLAlchemy必须在每个DBAPI基础上为每个上述值做出决定
        - 实现在它们的行为中完全不一致。

    -   **execution\_options**
        [¶](#sqlalchemy.create_engine.params.execution_options) -
        将应用于所有连接的字典执行选项。请参阅[`execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")
    -   **implicit\_returning=True**[¶](#sqlalchemy.create_engine.params.implicit_returning)
        – When `True`, a RETURNING- compatible
        construct, if available, will be used to fetch newly generated
        primary key values when a single row INSERT statement is emitted
        with no existing returning() clause.
        这适用于那些支持RETURNING或兼容构造的后端，包括Postgresql，Firebird，Oracle，Microsoft
        SQL Server。将其设置为`False`以禁用自动使用RETURNING。
    -   **isolation\_level**
        [¶](#sqlalchemy.create_engine.params.isolation_level) -

        此字符串参数由各种方言解释，以影响数据库连接的事务隔离级别。参数基本上接受这些字符串参数的一些子集：`"SERIALIZABLE"`，`"REPEATABLE_READ"`，`"READ_COMMITTED"`，`"READ_UNCOMMITTED"`和`"AUTOCOMMIT"`。这里的行为因后端而异，应直接咨询个别方言。

        请注意，也可以使用[`Connection.execution_options.isolation_level`](connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")功能在每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")基础上设置隔离级别。

        也可以看看

        [`Connection.default_isolation_level`](connections.html#sqlalchemy.engine.Connection.default_isolation_level "sqlalchemy.engine.Connection.default_isolation_level")
        - 查看默认级别

        [`Connection.execution_options.isolation_level`](connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")
        - 根据[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")设置隔离级别

        [SQLite Transaction
        Isolation](dialects_sqlite.html#sqlite-isolation-level)

        [Postgresql Transaction
        Isolation](dialects_postgresql.html#postgresql-isolation-level)

        [MySQL Transaction
        Isolation](dialects_mysql.html#mysql-isolation-level)

        [Setting Transaction Isolation
        Levels](orm_session_transaction.html#session-transaction-isolation)
        - for the ORM

    -   **label\_length=None**[¶](#sqlalchemy.create_engine.params.label_length)
        – optional integer value which limits the size of dynamically
        generated column labels to that many characters.
        如果小于6，标签生成为“\_（计数器）”。如果`None`，则使用`dialect.max_identifier_length`的值代替。
    -   **listeners**[¶](#sqlalchemy.create_engine.params.listeners) – A
        list of one or more [`PoolListener`](interfaces.html#sqlalchemy.interfaces.PoolListener "sqlalchemy.interfaces.PoolListener")
        objects which will receive connection pool events.
    -   **logging\_name**[¶](#sqlalchemy.create_engine.params.logging_name)
        – String identifier which will be used within the “name” field
        of logging records generated within the “sqlalchemy.engine”
        logger. 缺省为对象ID的十六进制字符串。
    -   **max\_overflow=10**[¶](#sqlalchemy.create_engine.params.max_overflow)
        – the number of connections to allow in connection pool
        “overflow”, that is connections that can be opened above and
        beyond the pool\_size setting, which defaults to five.
        这仅用于[`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")。
    -   **module=None**[¶](#sqlalchemy.create_engine.params.module) –
        reference to a Python module object (the module itself, not its
        string name).
        指定引擎方言使用的备用DBAPI模块。每个子方言引用一个特定的DBAPI，它将在第一次连接之前被导入。此参数导致绕过导入，并改为使用给定的模块。可用于测试DBAPI以及将“模拟”DBAPI实现注入到[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")中。
    -   **paramstyle=None**[¶](#sqlalchemy.create_engine.params.paramstyle)
        – The
        [paramstyle](http://legacy.python.org/dev/peps/pep-0249/#paramstyle)
        to use when rendering bound parameters.
        此样式默认为由DBAPI本身推荐的样式，该样式从DBAPI的`.paramstyle`属性中检索。但是，大多数DBAPI接受多个参数样式，特别是可能希望将“已命名”参数样式更改为“定位”参数样式，反之亦然。当这个属性被传递时，它应该是`"qmark"`，`"numeric"`，`"named"`，`"format"`或`"pyformat"`，并且应该与已知的DBAPI支持的参数样式相对应。
    -   **pool=None**[¶](#sqlalchemy.create_engine.params.pool) – an
        already-constructed instance of [`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool"),
        such as a [`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
        instance.
        如果为非无，则此池将直接用作引擎的基础连接池，绕过URL参数中存在的任何连接参数。有关手动构建连接池的信息，请参阅[Connection
        Pooling](pooling.html)。
    -   **poolclass=None**[¶](#sqlalchemy.create_engine.params.poolclass)
        – a [`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
        subclass, which will be used to create a connection pool
        instance using the connection parameters given in the URL.
        请注意，这与`pool`不同，因为在这种情况下您并未真正实例化池，您只需指出要使用的池的类型。
    -   **pool\_logging\_name**[¶](#sqlalchemy.create_engine.params.pool_logging_name)
        – String identifier which will be used within the “name” field
        of logging records generated within the “sqlalchemy.pool”
        logger. 缺省为对象ID的十六进制字符串。
    -   **pool\_size = 5**
        [¶](#sqlalchemy.create_engine.params.pool_size) -
        在连接池内保持打开的连接数。这与[`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")以及[`SingletonThreadPool`](pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")一起使用。对于[`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")，`pool_size`设置为0表示没有限制；要禁用池化，请将`poolclass`设置为[`NullPool`](pooling.html#sqlalchemy.pool.NullPool "sqlalchemy.pool.NullPool")。
    -   **pool\_recycle=-1**[¶](#sqlalchemy.create_engine.params.pool_recycle)
        – this setting causes the pool to recycle connections after the
        given number of seconds has passed.
        它默认为-1，或者没有超时。例如，设置为3600意味着连接将在一小时后回收。请注意，如果在连接上没有检测到任何活动8小时（尽管可以使用MySQLDB连接本身和服务器配置进行配置），MySQL尤其会自动断开连接。
    -   **pool\_reset\_on\_return ='rollback'**
        [¶](#sqlalchemy.create_engine.params.pool_reset_on_return) -

        设置池的“reset on
        return”行为，即是否在连接返回池时调用`rollback()`，`commit()`或任何内容。在[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")中查看`reset_on_return`的文档字符串。

        New in version 0.7.6.

    -   **pool\_timeout = 30**
        [¶](#sqlalchemy.create_engine.params.pool_timeout) -
        放弃从池中获取连接之前等待的秒数。这仅用于[`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")。
    -   **strategy ='plain'**
        [¶](#sqlalchemy.create_engine.params.strategy) -

        选择备用引擎实现。目前可用的有：

        -   [Using the Threadlocal Execution
            Strategy](connections.html#threadlocal-strategy)描述`threadlocal`策略；
        -   `mock`策略，它将所有语句执行分派给作为参数`executor`传递的函数。请参阅FAQ中的[示例。](http://docs.sqlalchemy.org/en/latest/faq_metadata_schema.html#how-can-i-get-the-create-table-drop-table-output-as-a-string)
    -   **executor=None**[¶](#sqlalchemy.create_engine.params.executor)
        – a function taking arguments
        `(sql, *multiparams, **params)`, to which
        the `mock` strategy will dispatch all
        statement execution. 仅用于`strategy='mock'`。

`sqlalchemy。`{.descclassname} `engine_from_config`{.descname} （ *configuration*，*prefix ='sqlalchemy。'*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.engine_from_config "Permalink to this definition")*
:   使用配置字典创建一个新的引擎实例。

    字典通常由配置文件生成。plain

    对`engine_from_config()`感兴趣的键应加上前缀，例如“ `sqlalchemy.url`，`sqlalchemy.echo`等'prefix'参数表示要搜索的前缀。每个匹配键（在前缀被剥离后）都被视为是[`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")调用的对应关键字参数。

    唯一需要的密钥是（假设默认前缀）`sqlalchemy.url`，它提供[database URL](#database-urls)。

    一组选定的关键字参数将根据字符串值“强制”为其预期类型。这组参数是使用`engine_config_types`存取器的可扩展每个方言。

    参数：

    -   **configuration**[¶](#sqlalchemy.engine_from_config.params.configuration)
        – A dictionary (typically produced from a config file, but this
        is not a requirement).
        键名以'prefix'开头的项目将剥离该前缀，然后传递给create\_engine。
    -   **prefix**[¶](#sqlalchemy.engine_from_config.params.prefix) –
        Prefix to match and then strip from keys in ‘configuration’.
    -   **kwargs**[¶](#sqlalchemy.engine_from_config.params.kwargs) –
        Each keyword argument to `engine_from_config()` itself overrides the corresponding item taken from the
        ‘configuration’ dictionary. 关键字参数应该以*不是*为前缀。

`sqlalchemy.engine.url。 T0>  make_url  T1> （ T2>  name_or_url  T3> ） T4> ¶< / T5>`{.descclassname}
:   给定一个字符串或 unicode 实例，产生一个新的 URL 实例。

    给定的字符串根据RFCplain
    1738规范进行分析。如果传递一个现有的URL对象，只返回该对象。

*class* `sqlalchemy.engine.url。`{.descclassname} `URL`{.descname} （ *drivername*，*=无*，*密码=无*，*主机=无*，*端口=无*，*数据库=无* ，*query = None t\>\> ） [¶](#sqlalchemy.engine.url.URL "Permalink to this definition")*
:   表示用于连接到数据库的 URL 的组件。

    该对象适合直接传递给[`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")调用。URL的字段由[`make_url()`](#sqlalchemy.engine.url.make_url "sqlalchemy.engine.url.make_url")函数从字符串中解析。该URL的字符串格式是RFC-1738样式的字符串。

    所有初始化参数都可用作公共属性。

    参数：

    -   **驱动程序名称**
        [¶](#sqlalchemy.engine.url.URL.params.drivername) -
        数据库后端的名称。该名称将对应于sqlalchemy
        /数据库中的模块或第三方插件。
    -   **用户名** [¶](#sqlalchemy.engine.url.URL.params.username) -
        用户名。
    -   **密码** [¶](#sqlalchemy.engine.url.URL.params.password) -
        数据库密码。
    -   tt\> **主机** [¶](#sqlalchemy.engine.url.URL.params.host) -
        主机的名称。
    -   **端口** [¶](#sqlalchemy.engine.url.URL.params.port) - 端口号。
    -   **数据库** [¶](#sqlalchemy.engine.url.URL.params.database) -
        数据库名称。
    -   **query**[¶](#sqlalchemy.engine.url.URL.params.query) – A
        dictionary of options to be passed to the dialect and/or the
        DBAPI upon connect.

    ` get_dialect  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回与此URL的驱动程序名称对应的SQLAlchemy数据库方言类。

    `translate_connect_args`{.descname} （ *names = []*，*\*\* kw* ） [T5\>](#sqlalchemy.engine.url.URL.translate_connect_args "Permalink to this definition")
    :   将url属性翻译成连接参数字典。

        返回此URL（主机，数据库，用户名，密码，端口
        ）作为一个普通的字典。属性名称默认用作键。从最终字典中省略未设置或错误的属性。

        参数：

        -   **\*\* kw**
            [¶](#sqlalchemy.engine.url.URL.translate_connect_args.params.**kw)
            - 可选的url属性的替代键名称。
        -   **名称**
            [¶](#sqlalchemy.engine.url.URL.translate_connect_args.params.names)
            -
            弃用。与基于关键字的备用名称的用途相同，但将名称与原始位置相关联。

汇集[¶ T0\>](#pooling "Permalink to this headline")
---------------------------------------------------

当`connect()`或`execute()`方法被调用时，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")会向连接池询问连接。默认连接池[`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")将根据需要打开到数据库的连接。As
concurrent statements are executed, [`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
will grow its pool of connections to a default size of five, and will
allow a default “overflow” of ten. 由于[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")实质上是连接池的“主基地”，因此应该为应用程序中建立的每个数据库保留一个[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，而不是创建一个新的为每个连接。

注意

[`QueuePool`](pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
is not used by default for SQLite engines.
有关 SQLite 连接池用法的详细信息，请参阅[SQLite](dialects_sqlite.html)。

有关连接池的更多信息，请参阅[Connection Pooling](pooling.html)。

自定义 DBAPI 连接()参数[¶](#custom-dbapi-connect-arguments "Permalink to this headline")
--------------------------------------------------------------------------------------

在发布`connect()`调用到底层 DBAPI 时使用的自定义参数可能以三种不同的方式发布。可以直接从 URL 字符串中传递基于字符串的参数作为查询参数：

    db = create_engine('postgresql://scott:tiger@localhost/test?argument1=foo&argument2=bar')

如果 SQLAlchemy 的数据库连接器知道特定的查询参数，它可能会将其类型从字符串转换为适当的类型。

[`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")还有一个参数`connect_args`，它是一个将传递给`connect()`的附加字典。这可以在需要字符串以外的参数时使用，并且 SQLAlchemy 的数据库连接器对该参数没有类型转换逻辑：

    db = create_engine('postgresql://scott:tiger@localhost/test', connect_args = {'argument1':17, 'argument2':'bar'})plain

全部最可定制的连接方法是传递一个`creator`参数，该参数指定一个返回 DBAPI 连接的可调用对象：

    def connect():
        return psycopg.connect(user='scott', host='localhost')

    db = create_engine('postgresql://', creator=connect)

配置日志记录[¶](#configuring-logging "Permalink to this headline")
------------------------------------------------------------------

Python 的标准[logging](http://docs.python.org/library/logging.html)模块用于通过 SQLAlchemy 实现信息和调试日志输出。这允许 SQLAlchemy 的日志记录与其他应用程序和库以标准方式集成。The
`echo` and `echo_pool` flags
that are present on [`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine"), as
well as the `echo_uow` flag used on [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
all interact with regular loggers.

本节假定您熟悉上述链接的日志记录模块。所有由 SQLAlchemy 执行的日志都存在于`sqlalchemy`命名空间下面，正如`logging.getLogger('sqlalchemy')`所使用的。当配置日志记录（即通过`logging.basicConfig()`）时，可以打开的 SA 记录器的通用名称空间如下所示：

-   `sqlalchemy.engine` -
    控制 SQL 回显。对于 SQL 查询输出设置为`logging.INFO`，对于查询+结果集输出设置为`logging.DEBUG`。
-   `sqlalchemy.dialects` -
    控制 SQL 方言的自定义日志记录。有关详细信息，请参阅单个方言的文档。
-   `sqlalchemy.pool` -
    控制连接池日志记录。设置为`logging.INFO`或更低以记录连接池检出/检入。
-   `sqlalchemy.orm` -
    控制各种 ORM 功能的记录。设置为`logging.INFO`以获取有关映射器配置的信息。

例如，要使用 Python 日志记录来记录 SQL 查询，而不是`echo=True`标志：

    import logging

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

默认情况下，日志级别在整个`sqlalchemy`名称空间内设置为`logging.WARN`，因此即使在启用了日志记录的应用程序中也不会发生日志操作。

`echo`标志作为[`create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")等关键字参数以及[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")上的`echo`属性存在，当设置为`True`时，将首先尝试确保启用日志记录。不幸的是，`logging`模块没有提供确定输出是否已经配置的方法（注意我们指的是是否设置了日志配置，而不仅仅是设置日志级别）。因此，任何`echo=True`标志都将导致使用 sys.stdout 作为目标对`logging.basicConfig()`的调用。它还使用级别名称，时间戳和记录器名称设置默认格式。请注意，此配置具有将**配置为**到任何现有记录器配置的作用。Therefore,
**when using Python logging, ensure all echo flags are set to False at
all times**, to avoid getting duplicate log lines.

实例的记录器名称（如[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Pool`](pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")）默认使用截断的十六进制标识符字符串。要将其设置为特定名称，请使用[`sqlalchemy.create_engine()`](#sqlalchemy.create_engine "sqlalchemy.create_engine")中的“logging\_name”和“pool\_logging\_name”关键字参数。

注意

SQLAlchemy [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")通过在当前日志记录级别被检测为`logging.INFO`或`logging.DEBUG`时仅发出日志语句来节省 Python 函数调用开销。它仅在从连接池获取新连接时才检查此级别。因此，在更改已运行的应用程序的日志记录配置时，当前处于活动状态的任何[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")或更常见的在事务中处于活动状态的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象都不会记录任何 SQL 根据新配置直到获取新的[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")（在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的情况下，这是在当前事务结束并且新的开始之后）。
