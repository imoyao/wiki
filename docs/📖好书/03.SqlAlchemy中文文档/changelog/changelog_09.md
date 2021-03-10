---
title: changelog_09
date: 2021-02-20 22:41:29
permalink: /sqlalchemy/b2578e/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
0.9 Changelog [¶](#changelog "Permalink to this headline")
==========================================================

0.9.11 [¶ T0\>](#change-0.9.11 "Permalink to this headline")
------------------------------------------------------------

没有发布日期

### 发动机[¶ T0\>](#change-0.9.11-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed critical issue whereby the pool “checkout”
    event handler may be called against a stale connection without the
    “connect” event handler having been called, in the case where the
    pool attempted to reconnect after being invalidated and failed; the
    stale connection would remain present and would be used on a
    subsequent attempt.
    这个问题在 1.0.2 之后的 1.0 系列中有更大的影响，因为它还向事件处理程序提供了一个空白的`.info`字典；在 1.0.2 之前，`.info`字典仍然是前一个。[¶](#change-4c50f070b6a282e0335d9fb87a2131cc)

    参考文献：[＃3497](http://www.sqlalchemy.org/trac/ticket/3497)

### 预言[¶ T0\>](#change-0.9.11-oracle "Permalink to this headline")

-   **[oracle] [bug] [py3k]**Fixed support for cx\_Oracle version 5.2,
    which was tripping up SQLAlchemy’s version detection under Python 3
    and inadvertently not using the correct unicode mode for Python 3.
    这会导致绑定变量被错误地解释为 NULL，并且行无声无息地返回。[¶](#change-0b5a9411f0cb0fb5b9ed763837dacee7)

    参考文献：[＃3491](http://www.sqlalchemy.org/trac/ticket/3491)

0.9.10 [¶ T0\>](#change-0.9.10 "Permalink to this headline")
------------------------------------------------------------

发布日期：2015 年 7 月 22 日

### ORM [¶ T0\>](#change-0.9.10-orm "Permalink to this headline")

-   **[orm] [feature]**向由[`Query.column_descriptions`](orm_query.html#sqlalchemy.orm.query.Query.column_descriptions "sqlalchemy.orm.query.Query.column_descriptions")返回的字典添加了一个新条目`"entity"`。这是指由表达式引用的主要 ORM 映射类或别名类。与`"type"`的现有条目相比，即使从列表达式中提取，它也将始终是映射实体，如果给定表达式是纯粹核心表达式，它将始终为 None。另见[＃3403](http://www.sqlalchemy.org/trac/ticket/3403)，它修复了此功能中的回归，该功能在 0.9.10 中未发布，但在 1.0 版本中发布。[¶](#change-ca4fc751ceaa91a33992ee87c9a525a3)

    参考文献：[＃3320](http://www.sqlalchemy.org/trac/ticket/3320)

-   **[orm] [bug]**[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    doesn’t support joins, subselects, or special FROM clauses when
    using the [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
    or [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")
    methods; instead of silently ignoring these fields if methods like
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    or [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    has been called, a warning is emitted.
    从 1.0.0b5 开始，这会引发错误。[¶](#change-af136f4c0f377ed2650ebb765f409144)

    参考文献：[＃3349](http://www.sqlalchemy.org/trac/ticket/3349)

-   **[orm] [bug]**Fixed bug where the state tracking within multiple,
    nested [`Session.begin_nested()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")
    operations would fail to propagate the “dirty” flag for an object
    that had been updated within the inner savepoint, such that if the
    enclosing savepoint were rolled back, the object would not be part
    of the state that was expired and therefore reverted to its database
    state.[¶](#change-ee81192da55510d7336bb2550e22a385)

    参考文献：[＃3352](http://www.sqlalchemy.org/trac/ticket/3352)

### 发动机[¶ T0\>](#change-0.9.10-engine "Permalink to this headline")

-   **[engine] [bug]**Added the string value `"none"` to those accepted by the [`Pool.reset_on_return`](core_pooling.html#sqlalchemy.pool.Pool.params.reset_on_return "sqlalchemy.pool.Pool")
    parameter as a synonym for `None`, so that
    string values can be used for all settings, allowing utilities like
    [`engine_from_config()`](core_engines.html#sqlalchemy.engine_from_config "sqlalchemy.engine_from_config")
    to be usable without
    issue.[¶](#change-2bc8922c3d02ea661e42e2f54e7c7201)

    参考文献：[＃3375](http://www.sqlalchemy.org/trac/ticket/3375)

### SQL [¶ T0\>](#change-0.9.10-sql "Permalink to this headline")

-   **[sql] [feature]**增加了对[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")中存在的 SELECT 所使用的 CTE 的官方支持。这种行为意外地一直运行到 0.9.9，当它由于作为[＃3248](http://www.sqlalchemy.org/trac/ticket/3248)的一部分的不相关更改而不再起作用时。请注意，这是在 SELECT 之前的 INSERT 之后的 WITH 子句的呈现；在 INSERT，UPDATE，DELETE 顶层呈现的 CTE 的全部功能是针对以后版本的一项新功能。[¶](#change-f8414532972c2d7d0d9d856124692667)

    参考文献：[＃3418](http://www.sqlalchemy.org/trac/ticket/3418)

-   **[sql] [bug]**Fixed issue where a [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    object that used a naming convention would not properly work with
    pickle. 如果使用不带钩的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象来构建附加表格，则跳过该属性会导致不一致和失败。[¶](#change-9a35a9fd17b1c1a118ee92550ccf0b00)

    参考文献：[＃3362](http://www.sqlalchemy.org/trac/ticket/3362)

### 的 PostgreSQL [¶ T0\>](#change-0.9.10-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**修复了长期存在的 bug，其中 psycopg2 方言使用的[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型与非 ascii 值和`native_enum=False`将无法正确解码返回结果。这源于 PG [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")类型曾经是没有“非本地”选项的独立类型。[¶](#change-f48ebfdbd81e4166cec7fa2687c381e8)

    参考文献：[＃3354](http://www.sqlalchemy.org/trac/ticket/3354)

### MySQL 的[¶ T0\>](#change-0.9.10-mysql "Permalink to this headline")

-   **[mysql] [bug]
    [pymysql]**修正了使用 unicode 参数使用“executemany”操作时对 PyMySQL 的 Unicode 支持。SQLAlchemy 现在将语句以及绑定参数作为 unicode 对象传递，因为 PyMySQL 通常在内部使用字符串插值来生成最终语句，而在 executemany 的情况下，仅在最后语句中执行“编码”步骤。[¶
    T0\>](#change-5898fc79f1b4c5e52fc6ecd0a9319733)

    参考文献：[＃3337](http://www.sqlalchemy.org/trac/ticket/3337)

-   **[mysql] [bug] [py3k]**修正了 Py3K 上没有正确使用`ord()`函数的[`mysql.BIT`](dialects_mysql.html#sqlalchemy.dialects.mysql.BIT "sqlalchemy.dialects.mysql.BIT")类型。请求礼貌 David
    Marin。[¶](#change-966802f406201dd8d7ea0b0b85d328ec)

    参考文献：[＃3333](http://www.sqlalchemy.org/trac/ticket/3333)，[请求 github：158](https://github.com/zzzeek/sqlalchemy/pull/158)

### 源码[¶ T0\>](#change-0.9.10-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**Fixed bug in SQLite dialect where reflection of
    UNIQUE constraints that included non-alphabetic characters in the
    names, like dots or spaces, would not be reflected with their
    name.[¶](#change-ca0388dc5ea3dd8415b40032f83e85d0)

    参考文献：[＃3495](http://www.sqlalchemy.org/trac/ticket/3495)

### 杂项[¶ T0\>](#change-0.9.10-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug where when using extended attribute
    instrumentation system, the correct exception would not be raised
    when [`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")
    were called with an invalid input that also happened to not be weak
    referencable, such as an
    integer.[¶](#change-bd0e166193a07e1132fc4c7f5a08f039)

    参考文献：[＃3408](http://www.sqlalchemy.org/trac/ticket/3408)

-   **[bug] [tests] [pypy]**修正了阻止“pypy setup.py
    test”正常工作的导入。[¶](#change-0fcc791335c7b1ce1b81b5dbeaaa9cc1)

    参考文献：[＃3406](http://www.sqlalchemy.org/trac/ticket/3406)

-   **[bug] [ext]**固定从 0.9.9 开始的回归，其中[`as_declarative()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.as_declarative "sqlalchemy.ext.declarative.as_declarative")符号已从`sqlalchemy.ext.declarative`名称空间中移除。 [¶
    T7\>](#change-d74f0c6b46400abe7e625144366f5e3e)

    参考文献：[＃3324](http://www.sqlalchemy.org/trac/ticket/3324)

0.9.9 [¶ T0\>](#change-0.9.9 "Permalink to this headline")
----------------------------------------------------------

发布日期：2015 年 3 月 10 日

### ORM [¶ T0\>](#change-0.9.9-orm "Permalink to this headline")

-   **[orm]
    [feature]**添加了一个新参数[`Session.connection.execution_options`](orm_session_api.html#sqlalchemy.orm.session.Session.connection.params.execution_options "sqlalchemy.orm.session.Session.connection")，它可用于在[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上设置执行选项在交易开始之前首先检查出来。这用于在事务启动之前设置连接上的隔离级别等选项。

    也可以看看

    [Setting Transaction Isolation
    Levels](orm_session_transaction.html#session-transaction-isolation)
    - 新的文档部分详细介绍了使用会话设置事务隔离的最佳实践。

    [¶](#change-257ec602824da39666b558dd308ddd68)

    参考文献：[＃3296](http://www.sqlalchemy.org/trac/ticket/3296)

-   **[orm] [feature]**Added new method [`Session.invalidate()`](orm_session_api.html#sqlalchemy.orm.session.Session.invalidate "sqlalchemy.orm.session.Session.invalidate"),
    functions similarly to [`Session.close()`](orm_session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close"),
    except also calls [`Connection.invalidate()`](core_connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")
    on all connections, guaranteeing that they will not be returned to
    the connection pool.
    这在例如情况下是有用的在进一步使用连接不安全时处理 gevent 超时，即使是回滚。[¶](#change-81f7e383b3862c1f1b3ec7f7a6e0aafe)

-   **[orm] [bug]**Fixed bugs in ORM object comparisons where comparison
    of many-to-one `!= None` would fail if the
    source were an aliased class, or if the query needed to apply
    special aliasing to the expression due to aliased joins or
    polymorphic querying; also fixed bug in the case where comparing a
    many-to-one to an object state would fail if the query needed to
    apply special aliasing due to aliased joins or polymorphic
    querying.[¶](#change-2df829d258aa418fc9764a2c877c271f)

    参考文献：[＃3310](http://www.sqlalchemy.org/trac/ticket/3310)

-   修正了在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的`after_rollback()`处理程序错误地将状态添加到内部断言的情况下会失败的问题。**[orm]
    [bug]** [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")处理程序中，以及警告和移除此状态的任务（由[＃2389](http://www.sqlalchemy.org/trac/ticket/2389)建立）尝试继续。[¶](#change-7b35681c2beaa12811329756cbdad1b5)

    参考文献：[＃3309](http://www.sqlalchemy.org/trac/ticket/3309)

-   **[orm] [bug]**Fixed bug where TypeError raised when
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    called with unknown kw arguments would raise its own TypeError due
    to broken formatting. 请求 Malthe
    Borch 提出请求。[¶](#change-ec432e8e77803ef9276f98ec61867b39)

    参考文献：[请求 github：147](https://github.com/zzzeek/sqlalchemy/pull/147)

-   **[orm] [bug]**Fixed bug in lazy loading SQL construction whereby a
    complex primaryjoin that referred to the same “local” column
    multiple times in the “column that points to itself” style of
    self-referential join would not be substituted in all cases.
    这里确定替代的逻辑已被重新设计为更加开放。[¶](#change-3ce9474490eb936aecbfe90a61b6989b)

    参考文献：[＃3300](http://www.sqlalchemy.org/trac/ticket/3300)

-   **[orm] [bug]**“通配符”加载器选项，特别是由[`orm.load_only()`](orm_loading_columns.html#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")选项设置的选项，以覆盖未明确提及的所有属性，现在考虑给定实体的超类，如果该实体使用继承映射进行映射，那么超类中的属性名也从加载中省略。此外，多态判别器列无条件地包含在列表中，就像主键列一样，所以即使设置了 load\_only()，子类型的多态加载也能正常运行。[¶
    t0 \>](#change-cb85bfd5b9268fd26d4bb6655f9647fc)

    参考文献：[＃3287](http://www.sqlalchemy.org/trac/ticket/3287)

-   **[orm] [bug] [pypy]**Fixed bug where if an exception were thrown at
    the start of a [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    before it fetched results, particularly when row processors can’t be
    formed, the cursor would stay open with results pending and not
    actually be closed.
    对于像 Pypy 这样的解释器来说，这通常只是一个问题，在这种解释器中，光标没有立即被 GC 化，并且在某些情况下会导致事务/锁的打开时间超过所需的时间。[¶](#change-eb4c6d7da5a58814047869eac9bfc873)

    参考文献：[＃3285](http://www.sqlalchemy.org/trac/ticket/3285)

-   **[orm] [bug]**Fixed a leak which would occur in the unsupported and
    highly non-recommended use case of replacing a relationship on a
    fixed mapped class many times, referring to an arbitrarily growing
    number of target mappers.
    当旧的关系被替换时发出警告，但是如果映射已经用于查询，旧的关系仍然会在一些注册表中被引用。[¶](#change-11dd64077e54acf0bf1bb5947c23de22)

    参考文献：[＃3251](http://www.sqlalchemy.org/trac/ticket/3251)

-   **[orm] [bug] [sqlite]**Fixed bug regarding expression mutations
    which could express itself as a “Could not locate column” error when
    using [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    to select from multiple, anonymous column entities when querying
    against SQLite, as a side effect of the “join rewriting” feature
    used by the SQLite
    dialect.[¶](#change-34fb265e26bf9318cfcc46fe62fabfd6)

    参考文献：[＃3241](http://www.sqlalchemy.org/trac/ticket/3241)

-   **[orm] [bug]**Fixed bug where the ON clause for
    [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join"),
    and [`Query.outerjoin()`](orm_query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin")
    to a single-inheritance subclass using `of_type()` would not render the “single table criteria” in the ON
    clause if the `from_joinpoint=True` flag were
    set.[¶](#change-80b153398da9fb25bd731706ec2ce525)

    参考文献：[＃3232](http://www.sqlalchemy.org/trac/ticket/3232)

### 发动机[¶ T0\>](#change-0.9.9-engine "Permalink to this headline")

-   **[engine] [feature]**增加了用于查看事务隔离级别的新用户空间访问器；
    [`Connection.get_isolation_level()`](core_connections.html#sqlalchemy.engine.Connection.get_isolation_level "sqlalchemy.engine.Connection.get_isolation_level")，[`Connection.default_isolation_level`](core_connections.html#sqlalchemy.engine.Connection.default_isolation_level "sqlalchemy.engine.Connection.default_isolation_level")。[¶](#change-f30f7db6662d7e6a49a0036659a63554)

-   **[engine] [bug]**Fixed bug in [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    and pool where the [`Connection.invalidate()`](core_connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")
    method, or an invalidation due to a database disconnect, would fail
    if the `isolation_level` parameter had been used
    with [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options");
    the “finalizer” that resets the isolation level would be called on
    the no longer opened
    connection.[¶](#change-394c5516672e736e3c9559084ec887cd)

    参考文献：[＃3302](http://www.sqlalchemy.org/trac/ticket/3302)

-   **[engine] [bug]**A warning is emitted if the
    `isolation_level` parameter is used with
    [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")
    when a [`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")
    is in play; DBAPIs and/or SQLAlchemy dialects such as psycopg2,
    MySQLdb may implicitly rollback or commit the transaction, or not
    change the setting til next transaction, so this is never
    safe.[¶](#change-e69b88c19910ee3b225c03d45a8a0d07)

    参考文献：[＃3296](http://www.sqlalchemy.org/trac/ticket/3296)

### SQL [¶ T0\>](#change-0.9.9-sql "Permalink to this headline")

-   **[sql] [bug]**将`native_enum`标志添加到[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")的`__repr__()`与 Alembic 自动生成一起使用时很重要。拉请求礼貌 Dimitris
    Theodorou。[¶](#change-3577552ba354e8d369dededa4f306eb8)

    参考文献：[pull request
    bitbucket：41](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/41)

-   **[sql] [bug]**Fixed bug where using a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    that implemented a type that was also a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    would fail with Python’s “Cannot create a consistent method
    resolution order (MRO)” error, when any kind of SQL comparison
    expression were used against an object using this
    type.[¶](#change-a61899ed2d03a8e546f7daf26f476c1c)

    参考文献：[＃3278](http://www.sqlalchemy.org/trac/ticket/3278)

-   **[sql] [bug]**Fixed issue where the columns from a SELECT embedded
    in an INSERT, either through the values clause or as a “from
    select”, would pollute the column types used in the result set
    produced by the RETURNING clause when columns from both statements
    shared the same name, leading to potential errors or mis-adaptation
    when retrieving the returning
    rows.[¶](#change-2bdcbd3f5a1eb1534034bea319ff6eb5)

    参考文献：[＃3248](http://www.sqlalchemy.org/trac/ticket/3248)

### 架构[¶ T0\>](#change-0.9.9-schema "Permalink to this headline")

-   **[schema] [bug]**Fixed bug in 0.9’s foreign key setup system, such
    that the logic used to link a [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    to its parent could fail when the foreign key used
    “link\_to\_name=True” in conjunction with a target [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    that would not receive its parent column until later, such as within
    a reflection + “useexisting” scenario, if the target column in fact
    had a key value different from its name, as would occur in
    reflection if column reflect events were used to alter the .key of
    reflected [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    objects so that the link\_to\_name becomes significant.
    当目标列具有不同的键并使用 link\_to\_name 引用时，也通过类似的方式修复了对列类型的支持。[¶](#change-4174c5d38944ec13bc76cc10181274df)

    参考文献：[＃3298](http://www.sqlalchemy.org/trac/ticket/3298)，[＃1765](http://www.sqlalchemy.org/trac/ticket/1765)

### 的 PostgreSQL [¶ T0\>](#change-0.9.9-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**使用`postgresql_concurrently`添加了对使用 Postgresql 索引的`CONCURRENTLY`关键字的支持。请求 Iuri de Silvio 提出请求。

    也可以看看

    [Indexes with
    CONCURRENTLY](dialects_postgresql.html#postgresql-index-concurrently)

    [¶](#change-2a4614f79e145b5f9d8a3861d75f3006)

    参考：[拉请求 bitbucket：45](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/45)

-   **[postgresql] [bug]**使用 psycopg2 时修复了对 Postgresql
    UUID 类型与 ARRAY 类型的支持。psycopg2 方言现在使用 psycopg2.extras.register\_uuid()挂钩，以便始终将 UUID 值作为 UUID()对象传递给 DBAPI 或从 DBAPI 传递。[`UUID.as_uuid`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.UUID.params.as_uuid "sqlalchemy.dialects.postgresql.UUID")标志仍然有效，除非使用 psycopg2，否则我们需要在禁用时将返回的 UUID 对象转换回字符串。[¶](#change-fc15276f16d5f99614d8b4a54fecfaa5)

    参考文献：[＃2940](http://www.sqlalchemy.org/trac/ticket/2940)

-   **[postgresql] [bug]**Added support for the `postgresql.JSONB` datatype when using psycopg2 2.5.4
    or greater, which features native conversion of JSONB data so that
    SQLAlchemy’s converters must be disabled; additionally, the newly
    added psycopg2 extension `extras.register_default_jsonb` is used to establish a JSON deserializer passed to the
    dialect via the `json_deserializer` argument.
    还修复了 Postgresql 集成测试，它实际上并未将 JSONB 类型与 JSON 类型相反。请求 Mateusz
    Susik 提供。[¶](#change-c632de8dde067c70ccf363e6daeedb9e)

    参考文献：[请求 github：145](https://github.com/zzzeek/sqlalchemy/pull/145)

-   **[postgresql]
    [bug]**在注册 HSTORE 类型时，修复了使用“array\_oid”标志的旧版 psycopg2 版本\<2.4.3，该版本不支持该标志，以及使用 native
    json 串行器钩子“register\_default\_json”与用户定义的 json\_deserializer 在 psycopg2 版本\<2.5 上，其中不包含本地 json
    ¶

-   **[postgresql] [bug]**Fixed bug where Postgresql dialect would fail
    to render an expression in an [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    that did not correspond directly to a table-bound column; typically
    when a [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    construct was one of the expressions within the index; or could
    misinterpret the list of expressions if one or more of them were
    such an expression.[¶](#change-32f226c662282afc1566aa854def390b)

    参考文献：[＃3174](http://www.sqlalchemy.org/trac/ticket/3174)

### MySQL 的[¶ T0\>](#change-0.9.9-mysql "Permalink to this headline")

-   **[mysql]
    [bug]**增加了对'utf8\_bin'排序检查周围的 MySQLdb 方言的版本检查，因为这在 MySQL 服务器\<5.0 中失败。¶

    参考文献：[＃3274](http://www.sqlalchemy.org/trac/ticket/3274)

-   **[mysql] [change]** `gaerdbms`方言不再需要，并且发出弃用警告。Google 现在建议直接使用 MySQLdb 方言。[¶](#change-8ad918e4ff23a5c688ab088a851b3d84)

    参考文献：[＃3275](http://www.sqlalchemy.org/trac/ticket/3275)

### 源码[¶ T0\>](#change-0.9.9-sqlite "Permalink to this headline")

-   **[sqlite]
    [feature]**在 SQLite 中增加了对部分索引（例如使用 WHERE 子句）的支持。请求 Kai
    Groner 提供的请求。

    也可以看看

    [Partial Indexes](dialects_sqlite.html#sqlite-partial-index)

    [¶](#change-2437d88dea80ab7c4b359b0a0b1c5851)

    参考文献：[pull request
    bitbucket：42](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/42)

-   **[sqlite]
    [feature]**为 SQLCipher 后端添加了新的 SQLite 后端。该后端使用 pysqlcipher
    Python 驱动程序提供加密的 SQLite 数据库，这与 pysqlite 驱动程序非常相似。

    也可以看看

    [`pysqlcipher`](dialects_sqlite.html#module-sqlalchemy.dialects.sqlite.pysqlcipher "sqlalchemy.dialects.sqlite.pysqlcipher")

    [¶](#change-e7af5da13cb89fc42bd84e28fe79ec07)

### 杂项[¶ T0\>](#change-0.9.9-misc "Permalink to this headline")

-   **[bug] [ext] [py3k]**Fixed bug where the association proxy list
    class would not interpret slices correctly under Py3K.
    拉尔请求礼貌 Gilles
    Dartiguelongue。[¶](#change-10dacdfe5eb7c9ab611635de10cb4708)

    参考文献：[请求 github：154](https://github.com/zzzeek/sqlalchemy/pull/154)

-   **[bug] [examples]**Updated the [Versioning with a History
    Table](orm_examples.html#examples-versioned-history) example such
    that mapped columns are re-mapped to match column names as well as
    grouping of columns; in particular, this allows columns that are
    explicitly grouped in a same-column-named joined inheritance
    scenario to be mapped in the same way in the history mappings,
    avoiding warnings added in the 0.9 series regarding this pattern and
    allowing the same view of attribute
    keys.[¶](#change-9729fe8589ed3467a037083e5d6d0797)

-   **[bug] [examples]**Fixed a bug in the
    examples/generic\_assocaitions/discriminator\_on\_association.py
    example, where the subclasses of AddressAssociation were not being
    mapped as “single table inheritance”, leading to problems when
    trying to use the mappings
    further.[¶](#change-a2fae0619dae442c213a19d4a76aa3e4)

0.9.8 [¶ T0\>](#change-0.9.8 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014 年 10 月 13 日

### ORM [¶ T0\>](#change-0.9.8-orm "Permalink to this headline")

-   **[orm] [bug] [engine]**Fixed bug that affected generally the same
    classes of event as that of
    [\#3199](http://www.sqlalchemy.org/trac/ticket/3199), when the
    `named=True` parameter would be used.
    一些事件将无法注册，而其他事件不会正确地调用事件参数，通常是在事件被“包装”以便以其他方式进行适应的情况下。“命名”机制已重新排列，不会干扰内部包装函数期望的参数签名。[¶](#change-040cb84155ffafc236b8a0959f655553)

    参考文献：[＃3197](http://www.sqlalchemy.org/trac/ticket/3197)

-   **[orm] [bug]**Fixed bug that affected many classes of event,
    particularly ORM events but also engine events, where the usual
    logic of “de duplicating” a redundant call to
    [`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")
    with the same arguments would fail, for those events where the
    listener function is wrapped.
    断言将在 registry.py 中发生。这一说法现在已经被纳入重复数据删除检查中，并带来更简单的方法来检查重复数据删除的额外好处。[¶](#change-65925a14215a5f14359c76d2e3b04bae)

    参考文献：[＃3199](http://www.sqlalchemy.org/trac/ticket/3199)

-   **[orm]
    [bug]**固定警告，当复杂的自引用 primaryjoin 包含函数时会发出警告，同时指定 remote\_side；警告会建议设置“远程端”。如果 remote\_side 不存在，它现在只会发射。[¶](#change-dc9752643faf4e960c03910d74b7c380)

    参考文献：[＃3194](http://www.sqlalchemy.org/trac/ticket/3194)

### orm declarative [¶](#change-0.9.8-orm-declarative "Permalink to this headline")

-   **[bug] [declarative] [orm]**Fixed “‘NoneType’ object has no
    attribute ‘concrete’” error when using [`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    in conjunction with a subclass that declares
    `__abstract__`.[¶](#change-3e9abe4fb814c36d081c1af0743b68a0)

    参考文献：[＃3185](http://www.sqlalchemy.org/trac/ticket/3185)

### 发动机[¶ T0\>](#change-0.9.8-engine "Permalink to this headline")

-   **[engine] [bug]**The execution options passed to an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    either via [`create_engine.execution_options`](core_engines.html#sqlalchemy.create_engine.params.execution_options "sqlalchemy.create_engine")
    or [`Engine.update_execution_options()`](core_connections.html#sqlalchemy.engine.Engine.update_execution_options "sqlalchemy.engine.Engine.update_execution_options")
    are not passed to the special [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    used to initialize the dialect within the “first connect” event;
    dialects will usually perform their own queries in this phase, and
    none of the current available options should be applied here.
    特别是，“自动提交”选项会导致尝试在此初始连接中自动提交，由于[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的非标准状态，该选项将因 AttributeError 失败。[¶](#change-5ea92686db96cba0e79afedbcc6adf59)

    参考文献：[＃3200](http://www.sqlalchemy.org/trac/ticket/3200)

-   **[engine]
    [bug]**用于确定受 INSERT 或 UPDATE 影响的列的字符串键现在在对“编译缓存”缓存键作出贡献时被排序。这些键以前没有确定性地排序，这意味着相同的语句可以在相同的键上多次缓存，从内存和性能两个方面来说都是这样。[¶](#change-6a98e0632754dd817947fcd39bd2a627)

    参考文献：[＃3165](http://www.sqlalchemy.org/trac/ticket/3165)

### SQL [¶ T0\>](#change-0.9.8-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug where a fair number of SQL elements within
    the sql package would fail to `__repr__()`
    successfully, due to a missing `description`
    attribute that would then invoke a recursion overflow when an
    internal AttributeError would then re-invoke `__repr__()`.[¶](#change-222b0163a38f1bb2a9d159b7278af9fb)

    参考文献：[＃3195](http://www.sqlalchemy.org/trac/ticket/3195)

-   **[sql] [bug]**An adjustment to table/index reflection such that if
    an index reports a column that isn’t found to be present in the
    table, a warning is emitted and the column is skipped.
    对于一些特殊的系统列情况，可能会发生这种情况，正如 Oracle 观察到的那样。[¶](#change-c1ac48f9d293ea2e5f282a620ff1a9cc)

    参考文献：[＃3180](http://www.sqlalchemy.org/trac/ticket/3180)

-   **[sql] [bug]**Fixed bug in CTE where `literal_binds` compiler argument would not be always be correctly
    propagated when one CTE referred to another aliased CTE in a
    statement.[¶](#change-438513ba693d7e6a58994f37a3ed2ca5)

    参考文献：[＃3154](http://www.sqlalchemy.org/trac/ticket/3154)

-   **[sql]
    [bug]**修正了由[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)导致的 0.9.7 回归与错误的单元测试的结合，使得所谓的“模式”类型如[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")和[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")不能再被腌制。[¶](#change-ae836fdd12b932ca0dfa9804e5b52282)

    参考文献：[＃3144](http://www.sqlalchemy.org/trac/ticket/3144)，[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)

### 的 PostgreSQL [¶ T0\>](#change-0.9.8-postgresql "Permalink to this headline")

-   **[postgresql] [feature]
    [pg8000]**通过 pg8000 驱动程序为“理智的多行数”添加支持，主要适用于使用 ORM 进行版本控制时。该功能基于使用的 pg8000
    1.9.14 或更高版本进行版本检测。拉托洛克洛请求礼貌。[¶](#change-348b76a1618d3c820757eb094ebca1ef)

    参考文献：[请求 github：125](https://github.com/zzzeek/sqlalchemy/pull/125)

-   **[postgresql]
    [bug]**重新审视此问题在 0.9.5 中首次被修补，显然 psycopg2 的`.closed`访问器并不像我们假设的那样可靠，所以我们添加了一个当检测到 is-disconnect 场景时，显式检查异常消息“SSL
    SYSCALL 错误：错误的文件描述符”和“SSL
    SYSCALL 错误：EOF 检测到”。我们将继续咨询 psycopg2 的 connection.closed 作为第一次检查。[¶](#change-f9a3e851447589d85ac72da3b5ae6f96)

    参考文献：[＃3021](http://www.sqlalchemy.org/trac/ticket/3021)

-   **[postgresql] [bug]**Fixed bug where Postgresql JSON type was not
    able to persist or otherwise render a SQL NULL column value, rather
    than a JSON-encoded `'null'`.
    为了支持这种情况，更改如下：

    -   现在可以指定[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")值，这将始终导致产生该语句的 NULL 值。
    -   添加了一个新参数[`JSON.none_as_null`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON.params.none_as_null "sqlalchemy.dialects.mysql.JSON")，当 True 表示 Python
        `None`值应该作为 SQL
        NULL 执行，而不是 JSON 编码`'null'`

    对于非 psycopg2 的 DBAPI，即 pg8000，也会修复 NULL 的空值。

    [¶](#change-5e8390463893d41899dc2296b9ed0f34)

    参考文献：[＃3159](http://www.sqlalchemy.org/trac/ticket/3159)

-   **[postgresql] [bug]**
    DBAPI 错误的异常包装系统现在可以容纳非标准 DBAPI 异常，例如 psycopg2
    TransactionRollbackError。这些异常现在将使用`sqlalchemy.exc`中最接近的可用子类进行引发，如果是 TransactionRollbackError，`sqlalchemy.exc.OperationalError`。[¶](#change-90221b5e6266d9262bf64826feba9769)

    参考文献：[＃3075](http://www.sqlalchemy.org/trac/ticket/3075)

-   **[postgresql] [bug]**修正了[`postgresql.array`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")对象中的一个错误，其中与普通 Python 列表的比较将无法使用正确的数组构造函数。拉请求礼貌 Andrew。[¶](#change-7f25bb6d60f7a1279948396ac86574bb)

    参考文献：[＃3141](http://www.sqlalchemy.org/trac/ticket/3141)，[请求 github：124](https://github.com/zzzeek/sqlalchemy/pull/124)

-   **[postgresql]
    [bug]**为函数添加了支持的[`FunctionElement.alias()`](core_functions.html#sqlalchemy.sql.functions.FunctionElement.alias "sqlalchemy.sql.functions.FunctionElement.alias")方法。
    `func`构造。以前，此方法的行为未定义。当前行为模仿 0.9.4 之前的行为，即该函数被转换为具有给定别名的单列 FROM 子句，其中列本身是匿名命名的。[¶](#change-aaaa4815736728bec50c929a09c7fa5a)

    参考文献：[＃3137](http://www.sqlalchemy.org/trac/ticket/3137)

### MySQL 的[¶ T0\>](#change-0.9.8-mysql "Permalink to this headline")

-   **[mysql] [bug] [mysqlconnector]**Mysqlconnector as of version 2.0,
    probably as a side effect of the python 3 merge, now does not expect
    percent signs (e.g. as used as the modulus operator and others) to
    be doubled, even when using the “pyformat” bound parameter format
    (this change is not documented by Mysqlconnector).
    当检测模运算符是否应该呈现为`%%`或`%`时，方言现在检查 py2k 和 mysqlconnector 小于 2.0 版。[¶](#change-32126a623ef93ac44e3e9243d1260fca)

-   **[mysql] [bug] [mysqlconnector]** Unicode
    SQL 现在传递给 MySQLconnector 2.0 及更高版本；对于 Py2k 和 MySQL
    \<2.0，字符串被编码。¶

### 源码[¶ T0\>](#change-0.9.8-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**When selecting from a UNION using an attached
    database file, the pysqlite driver reports column names in
    cursor.description as ‘dbname.tablename.colname’, instead of
    ‘tablename.colname’ as it normally does for a UNION (note that it’s
    supposed to just be ‘colname’ for both, but we work around it).
    此处的列转换逻辑已被调整为检索最右侧的标记，而不是第二个标记，因此它适用于这两种情况。解决方法礼貌 Tony
    Roberts。[¶](#change-fa653d4ec018e069a52b2268725c5b88)

    参考文献：[＃3211](http://www.sqlalchemy.org/trac/ticket/3211)

### MSSQL [¶ T0\>](#change-0.9.8-mssql "Permalink to this headline")

-   **[mssql]
    [bug]**修复了 pymssql 方言中的版本字符串检测问题，以便与 Microsoft SQL
    Azure 一起使用，它将单词“SQL Server”更改为“SQL Azure”。[¶ t2
    \>](#change-80d8c2f1d6da858394e3f7fcf143fa10)

    参考文献：[＃3151](http://www.sqlalchemy.org/trac/ticket/3151)

### 预言[¶ T0\>](#change-0.9.8-oracle "Permalink to this headline")

-   **[oracle] [bug]**Fixed long-standing bug in Oracle dialect where
    bound parameter names that started with numbers would not be quoted,
    as Oracle doesn’t like numerics in bound parameter
    names.[¶](#change-f3121682a918ac059e902d14e81d0d54)

    参考文献：[＃2138](http://www.sqlalchemy.org/trac/ticket/2138)

### 杂项[¶ T0\>](#change-0.9.8-misc "Permalink to this headline")

-   **[bug] [declarative]**Fixed an unlikely race condition observed in
    some exotic end-user setups, where the attempt to check for
    “duplicate class name” in declarative would hit upon a
    not-totally-cleaned-up weak reference related to some other class
    being removed; the check here now ensures the weakref still
    references an object before calling upon it
    further.[¶](#change-1be20931c5cc779a5512e9e3ed985a11)

    参考文献：[＃3208](http://www.sqlalchemy.org/trac/ticket/3208)

-   **[bug]
    [ext]**修正了订购清单中的 bug，如果 reorder\_on\_append 标志被设置为 True，则在收集替换事件期间将抛出物品的顺序。该修复确保排序列表仅影响与该对象显式关联的列表。[¶](#change-f63e94a1795bd303f88294c462bd3b95)

    参考文献：[＃3191](http://www.sqlalchemy.org/trac/ticket/3191)

-   修正了[`ext.mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")无法实现`update()`字典方法的错误，因此无法捕捉更改。**[bug]
    [ext]**拉请求马特 Chisholm。[¶](#change-8d9ef3d42e12a3991355d6db0d7e0590)

-   **[bug] [ext]**Fixed bug where a custom subclass of
    [`ext.mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    would not show up in a “coerce” operation, and would instead return
    a plain [`ext.mutable.MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict").
    拉请求马特 Chisholm。[¶](#change-2995e85c7b79e5acb0500b5f7bef1116)

-   **[bug] [pool]**Fixed bug in connection pool logging where the
    “connection checked out” debug logging message would not emit if the
    logging were set up using `logging.setLevel()`,
    rather than using the `echo_pool` flag.
    已经添加了测试来声明这个日志记录。这是在 0.9.0 中引入的回归。[¶](#change-45bc7ea621ab2ad2ee138f5a0f4af495)

    参考文献：[＃3168](http://www.sqlalchemy.org/trac/ticket/3168)

0.9.7 [¶ T0\>](#change-0.9.7 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014 年 7 月 22 日

### ORM [¶ T0\>](#change-0.9.7-orm "Permalink to this headline")

-   **[orm] [bug] [eagerloading]**Fixed a regression caused by
    [\#2976](http://www.sqlalchemy.org/trac/ticket/2976) released in
    0.9.4 where the “outer join” propagation along a chain of joined
    eager loads would incorrectly convert an “inner join” along a
    sibling join path into an outer join as well, when only descendant
    paths should be receiving the “outer join” propagation;
    additionally, fixed related issue where “nested” join propagation
    would take place inappropriately between two sibling join
    paths.[¶](#change-6d4965c4def4ed6fe2cd5b1dc72055a2)

    参考文献：[＃3131](http://www.sqlalchemy.org/trac/ticket/3131)

-   **[orm] [bug]**Fixed a regression from 0.9.0 due to
    [\#2736](http://www.sqlalchemy.org/trac/ticket/2736) where the
    [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    method no longer set up the “from entity” of the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object correctly, so that subsequent [`Query.filter_by()`](orm_query.html#sqlalchemy.orm.query.Query.filter_by "sqlalchemy.orm.query.Query.filter_by")
    or [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    calls would fail to check the appropriate “from” entity when
    searching for attributes by string
    name.[¶](#change-61d46ddadd1243c644e4afbb5051ce5d)

    参考文献：[＃2736](http://www.sqlalchemy.org/trac/ticket/2736)，[＃3083](http://www.sqlalchemy.org/trac/ticket/3083)

-   **[orm] [bug]**The “evaluator” for query.update()/delete() won’t
    work with multi-table updates, and needs to be set to
    synchronize\_session=False or synchronize\_session=’fetch’; a
    warning is now emitted.
    在 1.0 中，这将被提升为一个完整的例外。[¶](#change-93ffe57d97cc97b691e1697f532fa023)

    参考文献：[＃3117](http://www.sqlalchemy.org/trac/ticket/3117)

-   **[orm] [bug]**Fixed bug where items that were persisted, deleted,
    or had a primary key change within a savepoint block would not
    participate in being restored to their former state (not in session,
    in session, previous PK) after the outer transaction were rolled
    back.[¶](#change-0f516bc305a847469d43e0869d992cdd)

    参考文献：[＃3108](http://www.sqlalchemy.org/trac/ticket/3108)

-   **[orm] [bug]**Fixed bug in subquery eager loading in conjunction
    with [`with_polymorphic()`](orm_inheritance.html#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic"),
    the targeting of entities and columns in the subquery load has been
    made more accurate with respect to this type of entity and
    others.[¶](#change-94424863efab08f99293f7724de969bf)

    参考文献：[＃3106](http://www.sqlalchemy.org/trac/ticket/3106)

-   **[orm]
    [bug]**修复了涉及动态属性的错误，这又是从版本 0.9.5 开始的[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)的回归。与 lazy
    ='dynamic'的自引用关系会在 flush 操作中引发 TypeError。[¶](#change-cfc1f15148c259394c9b3b373392bc15)

    参考文献：[＃3099](http://www.sqlalchemy.org/trac/ticket/3099)

### 发动机[¶ T0\>](#change-0.9.7-engine "Permalink to this headline")

-   **[engine] [feature]**Added new event
    [`ConnectionEvents.handle_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.handle_error "sqlalchemy.events.ConnectionEvents.handle_error"),
    a more fully featured and comprehensive replacement for
    [`ConnectionEvents.dbapi_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.dbapi_error "sqlalchemy.events.ConnectionEvents.dbapi_error").[¶](#change-4062d0afa2a67360ac9e7c97c79f35d4)

    参考文献：[＃3076](http://www.sqlalchemy.org/trac/ticket/3076)

### SQL [¶ T0\>](#change-0.9.7-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug in [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    and other [`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    subclasses where direct association of the type with a
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    would lead to a hang when events (like create events) were emitted
    on the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData").[¶](#change-08a78793c26fd10b053486a483ebad9f)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3124](http://www.sqlalchemy.org/trac/ticket/3124)

-   **[sql] [bug]**Fixed a bug within the custom operator plus
    [`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
    system, whereby using a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    in conjunction with variant would fail with an MRO error when a
    comparison operator was
    used.[¶](#change-be5c6a13348bdb50ab072eded4f844b3)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3102](http://www.sqlalchemy.org/trac/ticket/3102)

-   **[sql] [bug]**Fix bug in naming convention feature where using a
    check constraint convention that includes
    `constraint_name` would then force all
    [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    and [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    types to require names as well, as these implicitly create a
    constraint, even if the ultimate target backend were one that does
    not require generation of the constraint such as Postgresql.
    这些特定约束的命名约定的机制已重新组织，以便在 DDL 编译时完成命名确定，而不是在约束/表构造时完成命令。[¶](#change-346b9ff8fbd8e4eac954bf271b4c6ad6)

    参考文献：[＃3067](http://www.sqlalchemy.org/trac/ticket/3067)

-   **[sql] [bug]**Fixed bug in common table expressions whereby
    positional bound parameters could be expressed in the wrong final
    order when CTEs were nested in certain
    ways.[¶](#change-b79d7dd3f1ca1273c1284f2b2e8c296d)

    参考文献：[＃3090](http://www.sqlalchemy.org/trac/ticket/3090)

-   修正了多值[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")构造无法检查给定的字面 SQL 表达式第一个以后的值的问题。[**[sql]
    [bug]**](#change-9f3a810c852f582cfa2eef2e268ec4ef)

    参考文献：[＃3069](http://www.sqlalchemy.org/trac/ticket/3069)

-   **[sql]
    [bug]**在 Python 版本\<2.6.5 的 dialect\_kwargs 迭代中添加了一个“str()”步骤，解决了“no
    unicode="" keyword="" arg”关键字在一些反射过程中引用。¶

    参考文献：[＃3123](http://www.sqlalchemy.org/trac/ticket/3123)

-   **[sql] [bug]**The [`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
    method will now accept a type class as an argument which is
    internally converted to an instance, using the same convention long
    established by other constructs such as [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column").[¶](#change-8b1c78cb8eeb1975b8c03e0275f0af7b)

    参考文献：[＃3122](http://www.sqlalchemy.org/trac/ticket/3122)

### 的 PostgreSQL [¶ T0\>](#change-0.9.7-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**添加 kw 参数`postgresql_regconfig`到[`ColumnOperators.match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")运算符，允许指定“reg
    config”参数发送到`to_tsquery()`函数。请求 Jonathan
    Vanasco 提供。[¶](#change-d5177977fbaffd2ad0990c4ebf70a9ae)

    References: [\#3078](http://www.sqlalchemy.org/trac/ticket/3078),
    [pull request
    bitbucket:22](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/22)

-   **[postgresql] [feature]**通过[`JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")增加了对 Postgresql
    JSONB 的支持。请求礼貌 Damian
    Dimmich。[¶](#change-b66794b4e3bffb82595c82694c32733b)

    参考文献：[请求 github：101](https://github.com/zzzeek/sqlalchemy/pull/101)

-   **[postgresql] [bug]
    [pg8000]**修正了 0.9.5 版本中新增的 pg8000 隔离级别功能导致的错误，其中引擎级别的隔离级别参数会在连接时产生错误[¶
    t2 \>](#change-42d4d4dfd75600d1aca8205469504bb4)

    参考文献：[＃3134](http://www.sqlalchemy.org/trac/ticket/3134)

### MySQL 的[¶ T0\>](#change-0.9.7-mysql "Permalink to this headline")

-   **[mysql] [bug]**MySQL error 2014 “commands out of sync” appears to
    be raised as a ProgrammingError, not OperationalError, in modern
    MySQL-Python versions; all MySQL error codes that are tested for “is
    disconnect” are now checked within OperationalError and
    ProgrammingError
    regardless.[¶](#change-1548add72e7bdd221e888a5b3d6d9302)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3101](http://www.sqlalchemy.org/trac/ticket/3101)

### 源码[¶ T0\>](#change-0.9.7-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**Fixed a SQLite join rewriting issue where a
    subquery that is embedded as a scalar subquery such as within an IN
    would receive inappropriate substitutions from the enclosing query,
    if the same table were present inside the subquery as were in the
    enclosing query such as in a joined inheritance
    scenario.[¶](#change-5068035ad308233e769418ef305a1621)

    参考文献：[＃3130](http://www.sqlalchemy.org/trac/ticket/3130)

### MSSQL [¶ T0\>](#change-0.9.7-mssql "Permalink to this headline")

-   **[mssql] [feature]**为 SQL Server 2008 启用“多值插入”。拉尔请求 Albert
    Cervin 礼貌。还扩展了对“IDENTITY
    INSERT”模式的检查，以便在语句的 VALUE 子句中存在身份钥匙时包含该身份钥匙。[¶](#change-e5ab682c0b41fbfd0dcfb6c0fa0578f2)

    参考文献：[请求 github：98](https://github.com/zzzeek/sqlalchemy/pull/98)

-   **[mssql] [bug]**Added statement encoding to the “SET
    IDENTITY\_INSERT” statements which operate when an explicit INSERT
    is being interjected into an IDENTITY column, to support non-ascii
    table identifiers on drivers such as pyodbc + unix + py2k that don’t
    support unicode
    statements.[¶](#change-d9cb352dd29f9a5adb545d81d0cac1c9)

    这个改变也被**回退**为：0.8.7

-   **[mssql] [bug]**In the SQL Server pyodbc dialect, repaired the
    implementation for the `description_encoding`
    dialect parameter, which when not explicitly set was preventing
    cursor.description from being parsed correctly in the case of result
    sets that contained names in alternate encodings.
    这个参数不应该被继续使用。[¶](#change-4f728a60ab19f0468d57cf1bf84e2b5a)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3091](http://www.sqlalchemy.org/trac/ticket/3091)

-   **[mssql]
    [bug]**修复了由[＃3025](http://www.sqlalchemy.org/trac/ticket/3025)引起的 0.9.5 的回归，其中用于确定“默认模式”的查询在 SQL
    Server 2000 中无效。对于 SQL Server
    2000，我们回到缺省方言的“模式名称”参数，该参数是可配置的，但默认为'dbo'。[¶](#change-82de60fa2e391061691dd22349c22f5e)

    参考文献：[＃3025](http://www.sqlalchemy.org/trac/ticket/3025)

### 预言[¶ T0\>](#change-0.9.7-oracle "Permalink to this headline")

-   **[oracle] [bug] [tests]**Fixed bug in oracle dialect test suite
    where in one test, ‘username’ was assumed to be in the database URL,
    even though this might not be the
    case.[¶](#change-afb93babbe33115000779944030bb303)

    参考文献：[＃3128](http://www.sqlalchemy.org/trac/ticket/3128)

### 杂项[¶ T0\>](#change-0.9.7-misc "Permalink to this headline")

-   **[bug] [tests]**修正了“python setup.py
    test”没有正确调用 distutils 的错误，并且在测试套件结束时会发出错误。[T2\>](#change-7731e09fca20d7106d8a5a6a10e341f1)

-   **[bug] [declarative]**Fixed bug when the declarative
    `__abstract__` flag was not being distinguished
    for when it was actually the value `False`.
    `__abstract__`标志需要在被测试的级别上进行真实值计算。[¶](#change-905a41f06acdffd4ebc408aee599c147)

    参考文献：[＃3097](http://www.sqlalchemy.org/trac/ticket/3097)

0.9.6 [¶ T0\>](#change-0.9.6 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014 年 6 月 23 日

### ORM [¶ T0\>](#change-0.9.6-orm "Permalink to this headline")

-   **[orm]
    [bug]**恢复[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)的更改
    - 这是一个工作单元修复，通过[＃3061
    t3 在 1.0 中更全面地更新\>。](http://www.sqlalchemy.org/trac/ticket/3061)不幸的是，[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)中的修复产生了一个新问题，即多对一属性的急切加载可以产生一个解释为属性更改的事件。[¶](#change-b34ddce636d140c62cb6b43b92ce3464)

    参考文献：[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)

0.9.5 [¶ T0\>](#change-0.9.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014 年 6 月 23 日

### ORM [¶ T0\>](#change-0.9.5-orm "Permalink to this headline")

-   **[orm] [feature]**The “primaryjoin” model has been stretched a bit
    further to allow a join condition that is strictly from a single
    column to itself, translated through some kind of SQL function or
    expression.
    这是一种实验，但概念的第一个证明是“物化路径”连接条件，其中路径字符串使用“like”与自身进行比较。[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")运算符也被添加到在 primaryjoin 条件中使用的有效运算符列表中。[¶](#change-b14ee29d17139fd41dceb132ae75ee3a)

    参考文献：[＃3029](http://www.sqlalchemy.org/trac/ticket/3029)

-   **[orm]
    [feature]**添加了新的实用程序函数[`make_transient_to_detached()`](orm_session_api.html#sqlalchemy.orm.session.make_transient_to_detached "sqlalchemy.orm.session.make_transient_to_detached")，可用于制造表现如同从会话加载，然后分离的对象。不存在的属性被标记为过期，并且该对象可以被添加到会话中，它将像一个持久的行为一样。[¶](#change-d2f991a8058f33793f0f9fdd996750fa)

    参考文献：[＃3017](http://www.sqlalchemy.org/trac/ticket/3017)

-   **[orm] [bug]**Fixed bug in subquery eager loading where a long
    chain of eager loads across a polymorphic-subclass boundary in
    conjunction with polymorphic loading would fail to locate the
    subclass-link in the chain, erroring out with a missing property
    name on an [`AliasedClass`](orm_query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass").[¶](#change-368bbcba8a65910bc0ebf133019cd593)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3055](http://www.sqlalchemy.org/trac/ticket/3055)

-   **[orm] [bug]**Fixed ORM bug where the [`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")
    function would mask AttributeErrors or KeyErrors that should raise
    during mapper configuration due to user errors.
    对属性/键错误的捕获更具体，不包括配置步骤。[¶](#change-871a7a18ca10428184a782f221a13740)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3047](http://www.sqlalchemy.org/trac/ticket/3047)

-   **[orm] [bug]**Additional checks have been added for the case where
    an inheriting mapper is implicitly combining one of its column-based
    attributes with that of the parent, where those columns normally
    don’t necessarily share the same value.
    这是通过[＃1892](http://www.sqlalchemy.org/trac/ticket/1892)添加的现有支票的扩展。然而，这个新的检查仅发出警告，而不是例外，以允许可能依赖现有行为的应用程序。

    也可以看看

    [I’m getting a warning or error about “Implicitly combining column X
    under attribute Y”](faq_ormconfiguration.html#faq-combining-columns)

    [¶](#change-5ffa32a79580d10d4dc6e1f322b62326)

    参考文献：[＃3042](http://www.sqlalchemy.org/trac/ticket/3042)

-   **[orm] [bug]**Modified the behavior of [`orm.load_only()`](orm_loading_columns.html#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")
    such that primary key columns are always added to the list of
    columns to be “undeferred”; otherwise, the ORM can’t load the row’s
    identity. 显然，可以推迟映射的主键，并且 ORM 将失败，这并没有改变。But
    as load\_only is essentially saying “defer all but X”, it’s more
    critical that PK cols not be part of this
    deferral.[¶](#change-25bfed359ea9ffac545b3582739da0c4)

    参考文献：[＃3080](http://www.sqlalchemy.org/trac/ticket/3080)

-   **[orm] [bug]**Fixed a few edge cases which arise in the so-called
    “row switch” scenario, where an INSERT/DELETE can be turned into an
    UPDATE.
    在这种情况下，将多对一关系设置为无，或者在某些情况下将标量属性设置为无，可能不会将其检测为值的净更改，因此 UPDATE 不会重置上一行中的内容。这是由于一些尚未解决的方式属性历史的工作方式隐含地假设 None 不是真正的“改变”以前未设置的属性。另见[＃3061](http://www.sqlalchemy.org/trac/ticket/3061)。

    注意

    This change has been **REVERTED** in 0.9.6.
    完整的修补程序将在 SQLAlchemy 1.0 版中。

    [¶](#change-7dee9371466176d8e4b29c007477a68a)

    参考文献：[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)

-   **[orm]
    [bug]**与[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)相关，已对工作单元进行了调整，以使相关的多对一对象的加载稍微更积极在要删除的自引用对象的图形的情况下；如果未设置 passive\_deletes，则相关对象的负载将帮助确定正确的删除顺序。[](#change-075684cfd4ae61fbe83f5b7c147fcc8a)

-   **[orm] [bug]**Fixed bug in SQLite join rewriting where anonymized
    column names due to repeats would not correctly be rewritten in
    subqueries.
    这会影响任何类型的子查询+连接的 SELECT 查询。[¶](#change-fa2ca744e5fa4caa260e51dbac157f2e)

    参考文献：[＃3057](http://www.sqlalchemy.org/trac/ticket/3057)

-   **[orm] [bug] [sql]**Fixes to the newly enhanced boolean coercion in
    [\#2804](http://www.sqlalchemy.org/trac/ticket/2804) where the new
    rules for “where” and “having” woudn’t take effect for the
    “whereclause” and “having” kw arguments of the [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    construct, which is also what [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    uses so wasn’t working in the ORM
    either.[¶](#change-45db778576e325692f382fbe4e309669)

    参考文献：[＃3013](http://www.sqlalchemy.org/trac/ticket/3013)

### 发动机[¶ T0\>](#change-0.9.5-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed bug which would occur if a DBAPI exception
    occurs when the engine first connects and does its initial checks,
    and the exception is not a disconnect exception, yet the cursor
    raises an error when we try to close it.
    在这种情况下，当我们试图通过连接池记录游标关闭异常并且失败时，真正的异常将被废除，因为我们试图以在这种特定情况下不合适的方式访问池的记录器。[T0\>](#change-84310c96ae6744a277731d49bbf40a8a)

    参考文献：[＃3063](http://www.sqlalchemy.org/trac/ticket/3063)

-   **[engine] [bug]**Fixed some “double invalidate” situations were
    detected where a connection invalidation could occur within an
    already critical section like a connection.close(); ultimately,
    these conditions are caused by the change in
    [\#2907](http://www.sqlalchemy.org/trac/ticket/2907), in that the
    “reset on return” feature calls out to the Connection/Transaction in
    order to handle it, where “disconnect detection” might be caught.
    然而，[＃2985](http://www.sqlalchemy.org/trac/ticket/2985)中最近发生的变化可能会导致这种情况出现，因为“连接无效”操作的速度更快，因为问题在 0.9.4 上的可重复性高于 0.9.3。

    现在在任何可能出现失效的部分添加检查，以暂停对失效的连接进一步禁止的操作。这包括在引擎级别和池级别的两个修补程序。虽然在高度并发的基因事件中观察到这个问题，但理论上可以发生在连接关闭操作内发生断开连接的任何情况下。

    [¶](#change-b17a4835aab34786d5ecedee0ead17e1)

    参考文献：[＃3043](http://www.sqlalchemy.org/trac/ticket/3043)

### SQL [¶ T0\>](#change-0.9.5-sql "Permalink to this headline")

-   **[sql] [feature]**稍微放宽了[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")的契约，因为您可以指定一个[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")表达式作为目标；如果要通过内联声明或通过[`Table.append_constraint()`](core_metadata.html#sqlalchemy.schema.Table.append_constraint "sqlalchemy.schema.Table.append_constraint")将索引手动添加到表中，则索引不再需要存在表格绑定列。[T11\>](#change-f7babfe631a67d2dbe1627a033f09c8b)

    参考文献：[＃3028](http://www.sqlalchemy.org/trac/ticket/3028)

-   **[sql] [feature]**Added new flag
    [`expression.between.symmetric`](core_sqlelement.html#sqlalchemy.sql.expression.between.params.symmetric "sqlalchemy.sql.expression.between"),
    when set to True renders “BETWEEN SYMMETRIC”.
    还添加了一个新的否定运算符“notbetween\_op”，该运算符现在允许像`〜col.between（x， y）`这样的表达式呈现为“ col NOT BETWEEN x AND
    y“，而不是一个带括号的 NOT 字符串。[¶](#change-af7cd160da5802d1180fd83faee35afd)

    参考文献：[＃2990](http://www.sqlalchemy.org/trac/ticket/2990)

-   **[sql] [bug]**Fixed bug in INSERT..FROM SELECT construct where
    selecting from a UNION would wrap the union in an anonymous (e.g.
    unlabled) subquery.[¶](#change-9f9af41aeaf6c84b4705936f62a45be9)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3044](http://www.sqlalchemy.org/trac/ticket/3044)

-   修复了当[`Table.update()`](core_metadata.html#sqlalchemy.schema.Table.update "sqlalchemy.schema.Table.update")和[`Table.delete()`](core_metadata.html#sqlalchemy.schema.Table.delete "sqlalchemy.schema.Table.delete")在空的时候会产生一个空的 WHERE 子句的问题。**[sql]
    [bug]** [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")或[`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")或其他空白表达。这与[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的一致。[¶](#change-74c445dabb61781a9bd829c5df7d80df)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3045](http://www.sqlalchemy.org/trac/ticket/3045)

-   **[sql] [bug]**The [`Column.nullable`](core_metadata.html#sqlalchemy.schema.Column.params.nullable "sqlalchemy.schema.Column")
    flag is implicitly set to `False` when that
    [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    is referred to in an explicit [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
    for that table. 这种行为现在与[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")本身将[`Column.primary_key`](core_metadata.html#sqlalchemy.schema.Column.params.primary_key "sqlalchemy.schema.Column")标志设置为`True`时的行为相匹配，该行为旨在成为一个完全等效的情况[¶
    T8\>](#change-83df5359e7efaeb82389957dec0cdb65)

    参考文献：[＃3023](http://www.sqlalchemy.org/trac/ticket/3023)

-   **[sql] [bug]**Fixed bug where the [`Operators.__and__()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.__and__ "sqlalchemy.sql.operators.Operators.__and__"),
    [`Operators.__or__()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.__or__ "sqlalchemy.sql.operators.Operators.__or__")
    and [`Operators.__invert__()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.__invert__ "sqlalchemy.sql.operators.Operators.__invert__")
    operator overload methods could not be overridden within a custom
    [`TypeEngine.Comparator`](core_type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")
    implementation.[¶](#change-85577d5daa751d0acb0c47949a0c7e2f)

    参考文献：[＃3012](http://www.sqlalchemy.org/trac/ticket/3012)

-   **[sql] [bug]**Fixed bug in new
    [`DialectKWArgs.argument_for()`](core_sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
    method where adding an argument for a construct not previously
    included for any special arguments would
    fail.[¶](#change-959ca2bf6fe8506aedc7d32093077f73)

    参考文献：[＃3024](http://www.sqlalchemy.org/trac/ticket/3024)

-   **[sql] [bug]**Fixed regression introduced in 0.9 where new “ORDER
    BY ” feature from
    [\#1068](http://www.sqlalchemy.org/trac/ticket/1068) would not apply
    quoting rules to the label name as rendered in the ORDER
    BY.[¶](#change-dfb711b371577e0da5d5793400a73450)

    参考文献：[＃1068](http://www.sqlalchemy.org/trac/ticket/1068)，[＃3020](http://www.sqlalchemy.org/trac/ticket/3020)

-   **[sql] [bug]**将[`Function`](core_functions.html#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")的导入恢复到`sqlalchemy.sql.expression`导入命名空间，该空间在 0.9 开始时被删除[¶
    T7\>](#change-3cdb36857fd1906309e4a9c1af99bbea)

### 的 PostgreSQL [¶ T0\>](#change-0.9.5-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**在使用 pg8000
    DBAPI 时增加了对 AUTOCOMMIT 隔离级别的支持。拉托洛克洛请求礼貌。[¶](#change-911649ad2c23d32ab5dc1670d45c095c)

    参考文献：[请求 github：88](https://github.com/zzzeek/sqlalchemy/pull/88)

-   **[postgresql] [feature]**将新标志[`ARRAY.zero_indexes`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.params.zero_indexes "sqlalchemy.dialects.postgresql.ARRAY")添加到 Postgresql
    [`ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型。当设置为`True`时，在传递到数据库之前，值为 1 将被添加到所有数组索引值，从而允许 Python 样式的基于零的索引和基于 Postgresql
    one 的索引之间具有更好的互操作性。请求礼貌 Alexey
    Terentev。[¶](#change-4fa3bed78a6be8258c6b3e5fd7f621f3)

    参考文献：[＃2785](http://www.sqlalchemy.org/trac/ticket/2785)，[拉取请求 bitbucket：18](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/18)

-   **[postgresql] [bug]**为 PG [`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")类型添加了`hashable=False`标志，这是允许 ORM 跳过尝试在混合列/实体列表中请求 ORM 映射的 HSTORE 列时“散列”。补丁礼貌 GunnlaugurÞórBriem。[¶](#change-d1fc26504bf95db6331661b1c716fa84)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3053](http://www.sqlalchemy.org/trac/ticket/3053)

-   **[postgresql]
    [bug]**添加了一个新的“断开连接”消息“连接意外关闭”。这似乎与更新版本的 SSL 有关。拉提请求 Antti
    Haapala 礼貌。[¶](#change-b4544c9476cfd8dbf4900f17cafbea73)

    这个改变也被**回退**为：0.8.7

    参考：[拉取请求 bitbucket：13](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/13)

-   **[postgresql] [bug]**当确定异常是否为“断开”错误时，现在查阅 psycopg2
    `.closed`访问器；理想情况下，这应该不需要对异常消息进行任何其他检查来检测断开连接，但是我们将保留现有的消息作为后备消息。这应该能够处理新的情况，如“SSL
    EOF”条件。拉德请求礼貌德克米勒。[¶](#change-28077f9da4dc99fa0ea9c3c26c2206b0)

    参考文献：[＃3021](http://www.sqlalchemy.org/trac/ticket/3021)，[请求 github：87](https://github.com/zzzeek/sqlalchemy/pull/87)

-   **[postgresql]
    [enhancement]**在 Postgresql 方言中添加了一个新类型的[`postgresql.OID`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.OID "sqlalchemy.dialects.postgresql.OID")。虽然“oid”通常是 PG 中的私有类型，但在现代版本中并未公开，但有一些 PG 用例，例如可能暴露这些类型的大对象支持，以及某些用户报告的模式反射用例。
    [¶ T0\>](#change-3abc7a84a2cd2a4a6b699bf9051e8c4f)

    参考文献：[＃3002](http://www.sqlalchemy.org/trac/ticket/3002)

### MySQL 的[¶ T0\>](#change-0.9.5-mysql "Permalink to this headline")

-   **[mysql] [bug]**Fixed bug where column names added to
    `mysql_length` parameter on an index needed to
    have the same quoting for quoted names in order to be recognized.
    该修复使得引号是可选的，但也提供了旧的行为，以便与使用变通方法的向后兼容。[¶](#change-33595244b0c4abd0a6977c31c3b4f5fa)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3085](http://www.sqlalchemy.org/trac/ticket/3085)

-   **[mysql]
    [bug]**增加了对使用等号在索引中包含 KEY\_BLOCK\_SIZE 的表来反映表的支持。拉请求礼貌肖恩 McGivern。[¶](#change-d8934497b6707c20ed9dc43c8386e63d)

    这个改变也被**回退**为：0.8.7

    参考文献：[拉取请求 bitbucket：15](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/15)

### MSSQL [¶ T0\>](#change-0.9.5-mssql "Permalink to this headline")

-   **[mssql] [bug]**Revised the query used to determine the current
    default schema name to use the `database_principal_id()` function in conjunction with the
    `sys.database_principals` view so that we can
    determine the default schema independently of the type of login in
    progress (e.g., SQL Server, Windows,
    etc).[¶](#change-0ff915fd49e5ce758c93f7563aebdb56)

    参考文献：[＃3025](http://www.sqlalchemy.org/trac/ticket/3025)

### 火鸟[¶ T0\>](#change-0.9.5-firebird "Permalink to this headline")

-   **[firebird] [bug]**Fixed bug where the combination of “limit”
    rendering as “SELECT FIRST n ROWS” using a bound parameter (only
    firebird has both), combined with column-level subqueries which also
    feature “limit” as well as “positional” bound parameters (e.g. qmark
    style) would erroneously assign the subquery-level positions before
    that of the enclosing SELECT, thus returning parameters which are
    out of order.[¶](#change-d63a34acab255efce997614e69c98053)

    参考文献：[＃3038](http://www.sqlalchemy.org/trac/ticket/3038)

### 杂项[¶ T0\>](#change-0.9.5-misc "Permalink to this headline")

-   **[feature]
    [examples]**添加了一个使用最新关系功能说明物化路径的新示例。Jack
    Zhou 提供的例子。[¶](#change-b027ac056997c7e3f7a6fa31de610989)

    参考文献：[pull request
    bitbucket：21](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/21)

-   **[bug] [declarative]**The `__mapper_args__`
    dictionary is copied from a declarative mixin or abstract class when
    accessed, so that modifications made to this dictionary by
    declarative itself won’t conflict with that of other mappings.
    关于`version_id_col`和`polymorphic_on`参数的字典被修改，将内部的列替换为正式映射到本地类/表的列。[¶
    t4 \>](#change-780993758db8d5169a0b88014034f665)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3062](http://www.sqlalchemy.org/trac/ticket/3062)

-   **[bug] [ext]**Fixed bug in mutable extension where
    [`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    did not report change events for the `setdefault()` dictionary
    operation.[¶](#change-b4a24f8e25cdd80a7862778ebaa5bb60)

    这个改变也被**回退**为：0.8.7

    参考文献：[＃3093](http://www.sqlalchemy.org/trac/ticket/3093)，[＃3051](http://www.sqlalchemy.org/trac/ticket/3051)

-   **[bug] [ext]**Fixed bug where [`MutableDict.setdefault()`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict.setdefault "sqlalchemy.ext.mutable.MutableDict.setdefault")
    didn’t return the existing or new value (this bug was not released
    in any 0.8 version).
    请求礼貌托马斯 Hervé。[¶](#change-6faeea1f65b0b63436eba3a21a4eff20)

    这个改变也被**回退**为：0.8.7

    References: [\#3093](http://www.sqlalchemy.org/trac/ticket/3093),
    [\#3051](http://www.sqlalchemy.org/trac/ticket/3051), [pull request
    bitbucket:24](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/24)

-   **[bug] [testsuite]**In public test suite, shanged to use of
    `String(40)` from less-supported
    `Text` in
    `StringTest.test_literal_backslashes`.
    Pullreq 礼貌 Jan. [¶](#change-aa048eb945e5e5d48d5efed1dd7c64c2)

    参考：[请求 github：95](https://github.com/zzzeek/sqlalchemy/pull/95)

-   **[bug] [tests] [py3k]**更正了运行测试时涉及`imp`模块和 Python
    3.3 或更高版本的一些弃用警告。拉请求马特 Chisholm。[¶](#change-0482bb06234a4584cf24a7b5f94ba4e7)

    References: [\#2830](http://www.sqlalchemy.org/trac/ticket/2830),
    [pull request
    bitbucket:2830](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/2830)

0.9.4 [¶ T0\>](#change-0.9.4 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014 年 3 月 28 日

### 一般[¶ T0\>](#change-0.9.4-general "Permalink to this headline")

-   **[general]
    [feature]**为 pytest 添加了支持以运行测试。除了鼻子之外，这个跑步者目前正在得到支持，并且可能会更喜欢前进。SQLAlchemy 使用的鼻插件系统已经拆分出来，因此它也可以在 pytest 下运行。目前还没有计划放弃对鼻子的支持，我们希望测试套件本身可以继续尽可能不受测试平台的影响。有关使用 pytest 运行测试的更新信息，请参阅文件 README.unittests.rst。

    通过多次指定`--db`和/或`--dburi`标志，测试插件系统也得到了增强，以支持一次运行多个数据库 URL 的测试。这不会为每个数据库运行整个测试套件，而是允许特定于某些后端的测试用例在运行测试时使用该后端。当使用 pytest 作为测试运行器时，系统还会多次运行特定的测试套件，每个数据库运行一次，特别是“方言套件”中的那些测试。计划是 Alembic 还将使用增强型系统，并允许 Alembic 在一次运行中针对多个后端运行迁移操作测试，包括 Alembic 本身未包含的第三方后端。第三方方言和扩展也被鼓励将 SQLAlchemy 的测试套件作为基础进行标准化；请参阅 README.dialects.rst 文件以了解从 SQLAlchemy 测试平台构建的背景。

    [¶](#change-8b07998904f97052927cddc00d64a109)

-   **[general] [bug]**Adjusted `setup.py` file to
    support the possible future removal of the
    `setuptools.Feature` extension from setuptools.
    如果此关键字不存在，则使用 setuptools 进行设置仍然会成功，而不会退回到 distutils。可以通过设置 DISABLE\_SQLALCHEMY\_CEXT 环境变量来禁用 C 扩展构建。无论 setuptools 是否可用，该变量都适用。[¶](#change-aa9491d98f1ead53e0464652e0816e71)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃2986](http://www.sqlalchemy.org/trac/ticket/2986)

-   **[general] [bug]**Fixed some test/feature failures occurring in
    Python 3.4, in particular the logic used to wrap “column default”
    callables wouldn’t work properly for Python
    built-ins.[¶](#change-1c1ca7f7a0d5e6ba577a8a31920eba2d)

    参考文献：[＃2979](http://www.sqlalchemy.org/trac/ticket/2979)

### ORM [¶ T0\>](#change-0.9.4-orm "Permalink to this headline")

-   **[orm]
    [feature]**添加了新的参数[`orm.mapper.confirm_deleted_rows`](orm_mapping_api.html#sqlalchemy.orm.mapper.params.confirm_deleted_rows "sqlalchemy.orm.mapper")。默认为 True，表示一系列 DELETE 语句应该确认游标的行数与匹配的主键的数量相匹配；在大多数情况下（除了使用 version\_id 时），此行为已被取消以支持自引用 ON
    DELETE
    CASCADE 的异常边缘情况；为了适应这种情况，该消息现在只是一个警告，而不是一个例外，并且该标志可用于指示一种映射，该映射需要这种性质的自引用级联删除。另请参阅[＃2403](http://www.sqlalchemy.org/trac/ticket/2403)以了解原始更改的背景。[¶](#change-9e23c7c28f359372f92c6661ec54a74f)

    参考文献：[＃3007](http://www.sqlalchemy.org/trac/ticket/3007)

-   **[orm] [feature]**A warning is emitted if the
    [`MapperEvents.before_configured()`](orm_events.html#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")
    or [`MapperEvents.after_configured()`](orm_events.html#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")
    events are applied to a specific mapper or mapped class, as the
    events are only invoked for the [`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
    target at the general
    level.[¶](#change-4dbefa991bc15832dbd5722613a9ec8b)

-   **[orm] [feature]**Added a new keyword argument
    `once=True` to [`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")
    and [`event.listens_for()`](core_event.html#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for").
    这是一个方便的功能，它将包装给定的侦听器，使其仅被调用一次。[¶](#change-aef7530390a87c53f08a067e5881ebc8)

-   **[orm] [feature]**为[`relationship.innerjoin`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin "sqlalchemy.orm.relationship")添加了一个新选项，用于指定字符串`"nested"`。当设置为`"nested"`而不是`True`时，连接的“链接”将在现有外部连接的右侧加入内部连接，而不是链接为一串外连接。这可能应该是 0.9 发布时的默认行为，因为我们在 ORM 中引入了右嵌套连接的功能，但是我们现在将其保留为非默认值以避免更多的意外。

    也可以看看

    [Right-nested inner joins available in joined eager
    loads](migration_09.html#feature-2976)

    [¶](#change-2363c295319d0823eecd2e63c95663e5)

    参考文献：[＃2976](http://www.sqlalchemy.org/trac/ticket/2976)

-   **[orm] [bug]**Fixed ORM bug where changing the primary key of an
    object, then marking it for DELETE would fail to target the correct
    row for DELETE.[¶](#change-0c43a5d88cf8a178453e8e7bb6dd6346)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃3006](http://www.sqlalchemy.org/trac/ticket/3006)

-   **[orm] [bug]**Fixed regression from 0.8.3 as a result of
    [\#2818](http://www.sqlalchemy.org/trac/ticket/2818) where
    [`Query.exists()`](orm_query.html#sqlalchemy.orm.query.Query.exists "sqlalchemy.orm.query.Query.exists")
    wouldn’t work on a query that only had a
    [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    entry but no other
    entities.[¶](#change-035773212f99eca992be16278ffa7c60)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃2995](http://www.sqlalchemy.org/trac/ticket/2995)

-   **[orm] [bug]**Improved an error message which would occur if a
    query() were made against a non-selectable, such as a
    [`literal_column()`](core_sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column"),
    and then an attempt was made to use [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    such that the “left” side would be determined as `None` and then fail.
    现在可以明确检测到这种情况。[¶](#change-982465365ea40acced9cf15b19a4e419)

    这个改变也是**backported**到：0.8.6

-   **[orm] [bug]**从`sqlalchemy.orm.interfaces.__all__`中删除了过期名称，并使用当前名称刷新，以便导入\>
    \*再次运作。[¶](#change-bafeea020f9eb338bbde39de93481f0b)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃2975](http://www.sqlalchemy.org/trac/ticket/2975)

-   **[orm] [bug]**Fixed a very old behavior where the lazy load emitted
    for a one-to-many could inappropriately pull in the parent table,
    and also return results inconsistent based on what’s in the parent
    table, when the primaryjoin includes some kind of discriminator
    against the parent table, such as
    `and_(parent.id == child.parent_id, parent.deleted == False)`.
    虽然这个主要连接对于一对多来说没有多大意义，但在应用于多对一时更为常见，并且一对多来自后向参考。在这种情况下，从`child`加载行将保持`parent.deleted == False`就像在查询中一样，因此将其放到 FROM 子句中并执行笛卡尔积。现在，新行为将适当替换该参数的本地“parent.deleted”值。尽管通常情况下，真实世界的应用程序可能都希望在任何情况下都使用不同的 primaryjoin 作为 o2m 端。[¶](#change-c7ec7a2b899f6d33f4ef3c25d538daa0)

    参考文献：[＃2948](http://www.sqlalchemy.org/trac/ticket/2948)

-   **[orm] [bug]**Improved the check for “how to join from A to B” such
    that when a table has multiple, composite foreign keys targeting a
    parent table, the [`relationship.foreign_keys`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")
    argument will be properly interpreted in order to resolve the
    ambiguity; previously this condition would raise that there were
    multiple FK paths when in fact the foreign\_keys argument should be
    establishing which one is
    expected.[¶](#change-f407535c51c6656da4cfb08cd1542503)

    参考文献：[＃2965](http://www.sqlalchemy.org/trac/ticket/2965)

-   **[orm] [bug]**增加了对[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")标记的`insert=True`标记的支持带有映射器/实例事件。[¶](#change-d0595b585896aafd0894b807853463d3)

-   **[orm] [bug] [engine]**Fixed bug where events set to listen at the
    class level (e.g. on the [`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
    or [`ClassManager`](orm_internals.html#sqlalchemy.orm.instrumentation.ClassManager "sqlalchemy.orm.instrumentation.ClassManager")
    level, as opposed to on an individual mapped class, and also on
    [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"))
    that also made use of internal argument conversion (which is most
    within those categories) would fail to be
    removable.[¶](#change-efb079e4a2bde52cab05c332aee49e22)

    参考文献：[＃2973](http://www.sqlalchemy.org/trac/ticket/2973)

-   **[orm] [bug]**Fixed regression from 0.8 where using an option like
    [`orm.lazyload()`](orm_loading_relationships.html#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")
    with the “wildcard” expression, e.g. `"*"`,
    would raise an assertion error in the case where the query didn’t
    contain any actual entities.
    这个断言是针对其他情况的，并且在无意中捕捉到这个断言。[¶](#change-8aae354a4b3ff011dd6d9e53507c279f)

-   **[orm] [bug]
    [sqlite]**更多解决 SQLite“加入重写”；在 0.9.3 发布之前实施的[＃2967](http://www.sqlalchemy.org/trac/ticket/2967)修复影响了 UNION 包含嵌套连接的情况。“加入重写”是一种具有广泛可能性的特性，也是我们多年来推出的第一个错综复杂的“SQL 重写”特性，所以我们对其进行了大量迭代（与急切加载在 0.2
    / 0.3 系列中，多晶型负荷在 0.4 /
    0.5）。我们应该很快到那里，谢谢你的支持：）。[¶](#change-f9391466ff5f05d8025167143cffb3a3)

    参考文献：[＃2969](http://www.sqlalchemy.org/trac/ticket/2969)

### 发动机[¶ T0\>](#change-0.9.4-engine "Permalink to this headline")

-   **[engine]
    [feature]**为方言级事件添加了一些新的事件机制；初始实现允许事件处理程序重新定义任意方言在 DBAPI 游标上调用 execute()或 executemany()的特定机制。在这个半公开和实验性的新事件中，支持一些即将到来的事务相关的扩展。[¶](#change-0fbd5944c2467b0bab55d0a60ee42790)

-   **[engine] [feature]**An event listener can now be associated with a
    [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine"),
    after one or more [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    objects have been created (such as by an orm [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    or via explicit connect) and the listener will pick up events from
    those connections.
    以前，性能问题只是在初始阶段将事件从[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")转移到[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")，但我们已经内联了一系列条件检查，以使其成为可能，而无需任何其他功能呼叫。[¶
    T6\>](#change-bf0cfd70bc72b3a0d338585889a63fb4)

    参考文献：[＃2978](http://www.sqlalchemy.org/trac/ticket/2978)

-   **[engine] [bug]**在检测到“断开连接”条件时，[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")重新利用连接缓冲池的机制进行了重大改进；不是丢弃池并明确关闭连接，池将被保留，并更新“代”时间戳以反映当前时间，从而导致所有现有连接在下次检出时被回收。这大大简化了回收过程，消除了在唤醒等待旧池的连接尝试的需要，并消除了在回收操作期间可能创建的许多立即丢弃的“池”对象的争用情况。[T0\>](#change-2f688763d982ec3ef2381d07c51dd435)

    参考文献：[＃2985](http://www.sqlalchemy.org/trac/ticket/2985)

-   **[engine] [bug]**The
    [`ConnectionEvents.after_cursor_execute()`](core_events.html#sqlalchemy.events.ConnectionEvents.after_cursor_execute "sqlalchemy.events.ConnectionEvents.after_cursor_execute")
    event is now emitted for the “\_cursor\_execute()” method of
    [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection");
    this is the “quick” executor that is used for things like when a
    sequence is executed ahead of an INSERT statement, as well as for
    dialect startup checks like unicode returns, charset, etc.
    这里已经调用了[`ConnectionEvents.before_cursor_execute()`](core_events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute "sqlalchemy.events.ConnectionEvents.before_cursor_execute")事件。这里的“executemany”标志现在总是被设置为 False，因为这个事件总是对应于一次执行。以前，如果我们代表 executemany
    INSERT 语句执行操作，则标志可能为 True。[¶](#change-2bdaf42f4d681b56c349b95939f392fb)

### SQL [¶ T0\>](#change-0.9.4-sql "Permalink to this headline")

-   **[sql]
    [feature]**增加了对布尔值的文字渲染的支持，例如“true”/“false”或“1”/“0”。[¶](#change-ae73b72c5883a6bfadd83231bbc945cb)

-   **[sql] [feature]**添加了一个新特性[`schema.conv()`](core_constraints.html#sqlalchemy.schema.conv "sqlalchemy.schema.conv")，其目的是将约束名称标记为已经应用了命名约定。Alembic
    0.6.4 版本中的 Alembic 迁移将使用此标记，以便在迁移脚本中显示约束条件，并标记名称已受命名约定。[¶](#change-eb76a93c5c1ba58cc198d3783e1d4d74)

-   **[sql] [feature]**The new dialect-level keyword argument system for
    schema-level constructs has been enhanced in order to assist with
    existing schemes that rely upon addition of ad-hoc keyword arguments
    to constructs.

    例如，诸如[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")之类的结构将在构建之后再次接受[`Index.kwargs`](core_constraints.html#sqlalchemy.schema.Index.kwargs "sqlalchemy.schema.Index.kwargs")集合内的临时关键字参数：

        idx = Index('a', 'b')plain
        idx.kwargs['mysql_someargument'] = True

    为了适应在构建时允许自定义参数的用例，现在允许此注册：[`DialectKWArgs.argument_for()`](core_sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")方法：

        Index.argument_for('mysql', 'someargument', False)

        idx = Index('a', 'b', mysql_someargument=True)

    也可以看看

    [`DialectKWArgs.argument_for()`](core_sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")

    [¶](#change-da83b2502fb46853ce0e53aa3df91a9a)

    参考文献：[＃2866](http://www.sqlalchemy.org/trac/ticket/2866)，[＃2962](http://www.sqlalchemy.org/trac/ticket/2962)

-   **[sql] [bug]**Fixed bug in [`tuple_()`](core_sqlelement.html#sqlalchemy.sql.expression.tuple_ "sqlalchemy.sql.expression.tuple_")
    construct where the “type” of essentially the first SQL expression
    would be applied as the “comparison type” to a compared tuple value;
    this has the effect in some cases of an inappropriate “type
    coersion” occurring, such as when a tuple that has a mix of String
    and Binary values improperly coerces target values to Binary even
    though that’s not what they are on the left side. [`tuple_()`](core_sqlelement.html#sqlalchemy.sql.expression.tuple_ "sqlalchemy.sql.expression.tuple_")
    now expects heterogeneous types within its list of
    values.[¶](#change-fe06781a0af32115b5a219dbc350cb6b)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃2977](http://www.sqlalchemy.org/trac/ticket/2977)

-   **[sql] [bug]**Fixed an 0.9 regression where a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    that failed to reflect correctly wouldn’t be removed from the parent
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData"),
    even though in an invalid state. Pullreq 礼貌 Roman
    Podoliaka。[¶](#change-ba95c9ab0ff11216d8fe5bb713e2398c)

    参考文献：[＃2988](http://www.sqlalchemy.org/trac/ticket/2988)，[请求 github：78](https://github.com/zzzeek/sqlalchemy/pull/78)

-   **[sql] [bug]**[`MetaData.naming_convention`](core_metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")
    feature will now also apply to [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    objects that are associated directly with a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    instead of just on the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").[¶](#change-e9d783386f345232a96b9a9f34389e43)

-   **[sql] [bug]**Fixed bug in new [`MetaData.naming_convention`](core_metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")
    feature where the name of a check constraint making use of the
    “%(constraint\_name)s” token would get doubled up for the constraint
    generated by a boolean or enum type, and overall duplicate events
    would cause the “%(constraint\_name)s” token to keep compounding
    itself.[¶](#change-50c081ddded08f44824be844d1b15da9)

    参考文献：[＃2991](http://www.sqlalchemy.org/trac/ticket/2991)

-   **[sql] [bug]**Adjusted the logic which applies names to the .c
    collection when a no-name [`BindParameter`](core_sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
    is received, e.g. via `sql.literal()` or similar; the “key” of the bind param is used as the key
    within .c.
    而不是呈现的名称。由于这些绑定在任何情况下都具有“匿名”名称，因此这允许个别绑定参数在可选择的范围内具有其自己的名称，如果它们未被标记的话。[¶](#change-e92ab0a211866ce5780a590de380dd1d)

    参考文献：[＃2974](http://www.sqlalchemy.org/trac/ticket/2974)

-   **[sql] [bug]**在呈现重复列时，[`FromClause.c`](core_selectable.html#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")集合的行为发生了一些变化。发出警告并替换同名旧栏的行为仍然存在一定程度；更换尤其是保持向后兼容性。但是，被替换的列仍然与集合`._all_columns`中的`c`集合保持关联，集合
    tt\>用于构造（如别名和联合），以处理`c`中的列更多地指向实际列在列中的列，而不是唯一的键名集。This
    helps with situations where SELECT statements with same-named
    columns are used in unions and such, so that the union can match the
    columns up positionally and also there’s some chance of
    [`FromClause.corresponding_column()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
    still being usable here (it can now return a column that is only in
    selectable.c.\_all\_columns and not otherwise named).
    我们仍然需要确定这个清单最终可能在哪里，因此强调了新的集合。理论上它会成为 iter（selectable.c）的结果，但这意味着迭代的长度将不再与 keys()的长度匹配，并且需要检出行为。[T0\>](#change-6c78e246b3394d4e4b227f1f06cc54ef)

    参考文献：[＃2974](http://www.sqlalchemy.org/trac/ticket/2974)

-   **[sql] [bug]**Fixed issue in new [`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
    method where the ordering of columns given positionally would not be
    preserved. This could have potential impact in positional situations
    such as applying the resulting [`TextAsFrom`](core_selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")
    object to a union.[¶](#change-650edc97a13474c853b5c10a976a29f0)

### 的 PostgreSQL [¶ T0\>](#change-0.9.4-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**启用了“理智的多行计数”检查 psycopg2
    DBAPI，因为它似乎在 psycopg2
    2.0.9 中受支持。[¶](#change-f238b48f610767a520453ae382fb1992)

    这个改变也是**backported**到：0.8.6

-   **[postgresql] [bug]**Fixed regression caused by release 0.8.5 /
    0.9.3’s compatibility enhancements where index reflection on
    Postgresql versions specific to only the 8.1, 8.2 series again
    broke, surrounding the ever problematic int2vector type.
    虽然 int2vector 支持从 8.1 开始的数组操作，但显然它只支持从 8.3 开始的对于 varchar 的 CAST。[¶](#change-9708a66fcf11605de634853699c1df71)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃3000](http://www.sqlalchemy.org/trac/ticket/3000)

### MySQL 的[¶ T0\>](#change-0.9.4-mysql "Permalink to this headline")

-   **[mysql]
    [bug]**调整了 mysql-connector-python 的设置；在 Py2K 中，“支持 unicode 语句”标志现在为 False，因此 SQLAlchemy 会在发送到数据库之前将*SQL 字符串*（注意：*不是*参数）编码为字节。这似乎允许所有与 unicode 相关的测试通过 mysql 连接器，包括那些使用非 ascii 表/列名称的测试，以及使用 unicode 在 cursor.executemany()下的 TEXT 类型的一些测试。[¶
    T0\>](#change-8fd1f3c05b103698df571c4d15925738)

### 预言[¶ T0\>](#change-0.9.4-oracle "Permalink to this headline")

-   **[oracle]
    [feature]**在 cx\_Oracle 方言中添加了一个新的引擎选项`coerce_to_unicode=True`，该方法将 Python c2\_Oracle
    outputtypehandler 方法恢复为 Python 2 下的 Python
    unicode 转换，在 0.9.2 中由于[＃2911](http://www.sqlalchemy.org/trac/ticket/2911)。尽管有性能方面的问题，但一些使用案例希望 unicode
    coersion 对所有字符串值都是无条件的。请求礼貌 Christoph
    Zwerschke。[¶](#change-3a96f2348877f517e9c2f5950d4c1d1b)

    参考文献：[＃2911](http://www.sqlalchemy.org/trac/ticket/2911)，[请求 github：74](https://github.com/zzzeek/sqlalchemy/pull/74)

-   **[oracle] [bug]**增加了新的数据类型[`oracle.DATE`](dialects_oracle.html#sqlalchemy.dialects.oracle.DATE "sqlalchemy.dialects.oracle.DATE")，它是[`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")的子类。As
    Oracle has no “datetime” type per se, it instead has only
    `DATE`, it is appropriate here that the
    `DATE` type as present in the Oracle dialect be
    an instance of [`DateTime`](core_type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime").
    这个问题不会改变任何类型的行为，因为在任何情况下数据转换都由 DBAPI 处理，但改进的子类布局将有助于检查跨数据库兼容性类型的用例。还从 Oracle 方言中删除了大写的`DATETIME`，因为此类型在该上下文中不起作用。[¶](#change-5861886a0faf27d02c29bdac44e39a74)

    参考文献：[＃2987](http://www.sqlalchemy.org/trac/ticket/2987)

### 杂项[¶ T0\>](#change-0.9.4-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug in mutable extension as well as
    [`attributes.flag_modified()`](orm_session_api.html#sqlalchemy.orm.attributes.flag_modified "sqlalchemy.orm.attributes.flag_modified")
    where the change event would not be propagated if the attribute had
    been reassigned to
    itself.[¶](#change-7ed27baa911abecf8c4b54665d466e1c)

    这个改变也是**backported**到：0.8.6

    参考文献：[＃2997](http://www.sqlalchemy.org/trac/ticket/2997)

-   **[bug] [automap]
    [ext]**添加了对 automap 的支持，以便在两个处于已连接继承关系的类之间不应该创建关系的情况下，将子类链接回这些外键到超类。[¶](#change-50822a3d39ca486f3c066ca9821edd45)

    参考文献：[＃3004](http://www.sqlalchemy.org/trac/ticket/3004)

-   **[bug] [tests]**修复了一些错误的`u''`字符串，它们会阻止测试在 Py3.2 中传递。补丁礼貌 Arfrever
    Frehtes Taifersar
    Arahesis。[¶](#change-65600f5e6f7388343eecd3b62edfa06e)

    参考文献：[＃2980](http://www.sqlalchemy.org/trac/ticket/2980)

-   **[bug] [pool]**Fixed small issue in [`SingletonThreadPool`](core_pooling.html#sqlalchemy.pool.SingletonThreadPool "sqlalchemy.pool.SingletonThreadPool")
    where the current connection to be returned might get inadvertently
    cleaned out during the “cleanup” process. 补丁礼貌 jd23.
    [¶](#change-fe5f6bf9974e7d6f327cb0f51b761366)

-   **[bug] [ext] [py3k]**Fixed bug in association proxy where assigning
    an empty slice (e.g. `x[:] = [...]`) would fail
    on Py3k.[¶](#change-4efb0c1e9b726653c4fc710a9ed431bc)

-   **[bug] [ext]**Fixed a regression in association proxy caused by
    [\#2810](http://www.sqlalchemy.org/trac/ticket/2810) which caused a
    user-provided “getter” to no longer receive values of
    `None` when fetching scalar values from a target
    that is non-present.
    此更改引入的 None 检查现在移入默认 getter，因此用户提供的 getter 也将再次接收 None 值。[¶](#change-30555d2dbceb91ce584663b6726101d0)

    参考文献：[＃2810](http://www.sqlalchemy.org/trac/ticket/2810)

-   **[bug]
    [examples]**修正了版本级别示例中的列级别 INSERT 默认值会阻止写入历史值 NULL 的错误。[¶](#change-e0ab0a5338c4fe508e1a11411752a73c)

0.9.3 [¶ T0\>](#change-0.9.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014 年 2 月 19 日

### ORM [¶ T0\>](#change-0.9.3-orm "Permalink to this headline")

-   **[orm]
    [feature]**添加了新的[`MapperEvents.before_configured()`](orm_events.html#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")事件，该事件允许在[`configure_mappers()`](orm_mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
    `__declare_first__()`钩子在声明中补充`__declare_last__()`。[¶](#change-eb786e8c736c09ac5a33083ba8a84ffd)

-   **[orm] [bug]**Fixed bug where [`Query.get()`](orm_query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")
    would fail to consistently raise the [`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")
    that invokes when called on a query with existing criterion, when
    the given identity is already present in the identity
    map.[¶](#change-96a72422aa09306aa423720d8a97b57c)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2951](http://www.sqlalchemy.org/trac/ticket/2951)

-   **[orm] [bug] [sqlite]**Fixed bug in SQLite “join rewriting” where
    usage of an exists() construct would fail to be rewritten properly,
    such as when the exists is mapped to a column\_property in an
    intricate nested-join scenario.
    还修复了一个有点相关的问题，如果目标是别名表，而不是单独的别名列，那么在 SELECT 语句的 columns 子句上连接重写将失败。[¶](#change-bcd89a790df27cfdcae2a8109b61d16e)

    参考文献：[＃2967](http://www.sqlalchemy.org/trac/ticket/2967)

-   **[orm] [bug]**Fixed an 0.9 regression where ORM instance or mapper
    events applied to a base class such as a declarative base with the
    propagate=True flag would fail to apply to existing mapped classes
    which also used inheritance due to an assertion.
    另外，根据首次分配的方式，修复了在删除此类事件期间可能发生的属性错误。[¶](#change-5d64e437351667e0682df36dc7a55ebb)

    参考文献：[＃2949](http://www.sqlalchemy.org/trac/ticket/2949)

-   **[orm]
    [bug]**改进了组合属性的初始化逻辑，例如调用`MyClass.attribute`不需要执行 configure
    mappers 步骤。它会在没有任何错误的情况下工作。[¶](#change-af92c4a9aa53d0e18016cc10a0c419db)

    参考文献：[＃2935](http://www.sqlalchemy.org/trac/ticket/2935)

-   **[orm] [bug]**More issues with [ticket:2932] first resolved in
    0.9.2 where using a column key of the form
    `<tablename>_<columnname>` matching that of an
    aliased column in the text would still not match at the ORM level,
    which is ultimately due to a core column-matching issue.
    添加了其他规则，以便在使用[`TextAsFrom`](core_selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")构造或使用文字列时考虑列`_label`。[¶](#change-f823d5ff3da539a90fc0cf3f7dac97c5)

    参考文献：[＃2932](http://www.sqlalchemy.org/trac/ticket/2932)

### orm declarative [¶](#change-0.9.3-orm-declarative "Permalink to this headline")

-   **[bug] [orm] [declarative]**Fixed bug where
    [`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    would fail to be fully usable within declarative relationship
    configuration, as its string classname would not be available in the
    registry of classnames at mapper configuration time. The class now
    explicitly adds itself to the class regsitry, and additionally both
    [`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    as well as [`ConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.ConcreteBase "sqlalchemy.ext.declarative.ConcreteBase")
    set themselves up *before* mappers are configured within the
    [`configure_mappers()`](orm_mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
    setup, using the new [`MapperEvents.before_configured()`](orm_events.html#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")
    event.[¶](#change-fdcf86f8dfe04be777c674c066723232)

    参考文献：[＃2950](http://www.sqlalchemy.org/trac/ticket/2950)

### 发动机[¶ T0\>](#change-0.9.3-engine "Permalink to this headline")

-   **[engine] [bug] [pool]**Fixed a critical regression caused by
    [\#2880](http://www.sqlalchemy.org/trac/ticket/2880) where the newly
    concurrent ability to return connections from the pool means that
    the “first\_connect” event is now no longer synchronized either,
    thus leading to dialect mis-configurations under even minimal
    concurrency situations.[¶](#change-a5e88f49d79f6b2a868c6f66b3be7d98)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2964](http://www.sqlalchemy.org/trac/ticket/2964)，[＃2880](http://www.sqlalchemy.org/trac/ticket/2880)

### SQL [¶ T0\>](#change-0.9.3-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug where calling [`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")
    with an empty list or tuple would raise an IndexError.
    它现在产生一个空的插入结构，就像空字典一样。[¶](#change-4bcdb46ed066a2c9b8490bf78da16720)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2944](http://www.sqlalchemy.org/trac/ticket/2944)

-   **[sql] [bug]**Fixed bug where [`in_()`](orm_internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.in_ "sqlalchemy.orm.properties.RelationshipProperty.Comparator.in_")
    would go into an endless loop if erroneously passed a column
    expression whose comparator included the `__getitem__()` method, such as a column that uses the
    [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
    type.[¶](#change-d04236a265c2b96a0d1c28f0cb10ee98)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2957](http://www.sqlalchemy.org/trac/ticket/2957)

-   **[sql] [bug]**Fixed regression in new “naming convention” feature
    where conventions would fail if the referred table in a foreign key
    contained a schema name. 请求礼貌 Thomas
    Farvour。[¶](#change-32e5f45f2c9cbe4cd6ccc0326087b300)

    参考文献：[pull request
    github：67](https://github.com/zzzeek/sqlalchemy/pull/67)

-   **[sql] [bug]**Fixed bug where so-called “literal render” of
    [`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
    constructs would fail if the bind were constructed with a callable,
    rather than a direct value.
    这阻止了 ORM 表达式使用“literal\_binds”编译器标志进行呈现。[¶](#change-e2e7387ca4e9c810c4f780765399985c)

### 的 PostgreSQL [¶ T0\>](#change-0.9.3-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**将[`TypeEngine.python_type`](core_type_api.html#sqlalchemy.types.TypeEngine.python_type "sqlalchemy.types.TypeEngine.python_type")便利访问器添加到[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型中。请求礼貌 Alexey
    Terentev。[¶](#change-2887ae0aba411e9eb86f31766ab46817)

    参考：[请求 github：64](https://github.com/zzzeek/sqlalchemy/pull/64)

-   **[postgresql]
    [bug]**增加了 psycopg2 断开连接检测的附加信息，“无法将数据发送到服务器”，补充了现有的“无法接收来自服务器的数据”并被用户观察到。
    [¶ T2\>](#change-6799209a311c3dc94eac58c106af18da)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2936](http://www.sqlalchemy.org/trac/ticket/2936)

-   **[postgresql] [bug]**

    > Postgresql 在 Postgresql 的旧版本（之前的版本）以及其他 PG 引擎（如 Redshift）（假设 Redshift 的版本报告为\<8.1）时对 postgresql 反射行为的支持得到了改进。\<
    > span=""\>查询“索引”以及“主键”依赖于检查所谓的“int2vector”数据类型，该数据类型在 8.1 之前拒绝胁迫数组，导致查询中使用的“ANY()”运算符失败。当 PG 版本\<8.1 被使用时，大量的搜索引擎已经找到了非常黑客但推荐的 pg 核心开发者查询，因此索引和主键约束反映现在可用于这些版本。\<
    > span=""\>

    [¶](#change-f41983d269d6edd9b36005f803524707)

    这个改变也被**backported**修改为：0.8.5

-   **[postgresql] [bug]**Revised this very old issue where the
    Postgresql “get primary key” reflection query were updated to take
    into account primary key constraints that were renamed; the newer
    query fails on very old versions of Postgresql such as version 7, so
    the old query is restored in those cases when server\_version\_info
    \< (8, 0) is detected.[¶](#change-5433997f376e8e488a886c0c8e165f57)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2291](http://www.sqlalchemy.org/trac/ticket/2291)

-   **[postgresql] [bug]**增加了对“show
    standard\_conforming\_strings”的新增 dialect 启动查询的服务器版本检测；因为这个变量是从 PG
    8.2 开始添加的，所以我们跳过 PG 版本的查询，它们报告早于版本字符串的版本。[¶](#change-4f3cfb3c174030c18a138b13afe7a215)

    参考文献：[＃2946](http://www.sqlalchemy.org/trac/ticket/2946)

### MySQL 的[¶ T0\>](#change-0.9.3-mysql "Permalink to this headline")

-   **[mysql] [feature]**添加了新的特定于 MySQL 的[`mysql.DATETIME`](dialects_mysql.html#sqlalchemy.dialects.mysql.DATETIME "sqlalchemy.dialects.mysql.DATETIME")，其中包括小数秒支持；还增加了对[`mysql.TIMESTAMP`](dialects_mysql.html#sqlalchemy.dialects.mysql.TIMESTAMP "sqlalchemy.dialects.mysql.TIMESTAMP")的小数秒支持。DBAPI 支持是有限的，尽管小数秒被 MySQL
    Connector / Python 支持。补丁由 Geert JM
    Vanderkelen 提供。[¶](#change-ab9ba4668cce1a333145dd002a487a27)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2941](http://www.sqlalchemy.org/trac/ticket/2941)

-   **[mysql] [bug]**添加了对`分区 BY`和`PARTITIONS`
    MySQL 的支持将表关键字指定为`mysql_partition_by='value'`和`mysql_partitions='value'`至[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。拉玛请求提供 Marcus
    McCurdy。[¶](#change-985ed90f90095c4b537ea36d3c1ac546)

    这个改变也被**backported**修改为：0.8.5

    References: [\#2966](http://www.sqlalchemy.org/trac/ticket/2966),
    [pull request
    bitbucket:12](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/12)

-   **[mysql] [bug]**Fixed bug which prevented MySQLdb-based dialects
    (e.g. pymysql) from working in Py3K, where a check for “connection
    charset” would fail due to Py3K’s more strict value comparison
    rules.
    这个调用在任何情况下都没有考虑到数据库版本，因为服务器版本在那时仍然是 None，所以整个方法被简化为依赖于 connection.character\_set\_name()。[¶
    t0 \>](#change-73d5f7e864d7ffd3bf7060a3a52e6d34)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2933](http://www.sqlalchemy.org/trac/ticket/2933)

-   **[mysql] [bug]
    [cymysql]**修正了 cymysql 方言中诸如`'33a-MariaDB'`等版本字符串无法正确解析的错误。拉请求马特施密特。[¶](#change-cec15bf8dc76d9d68418cad966e2a9f1)

    参考文献：[＃2934](http://www.sqlalchemy.org/trac/ticket/2934)，[请求 github：69](https://github.com/zzzeek/sqlalchemy/pull/69)

### 源码[¶ T0\>](#change-0.9.3-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**The SQLite dialect will now skip unsupported
    arguments when reflecting types; such as if it encounters a string
    like `INTEGER(5)`, the [`INTEGER`](core_type_basics.html#sqlalchemy.types.INTEGER "sqlalchemy.types.INTEGER")
    type will be instantiated without the “5” being included, based on
    detecting a `TypeError` on the first
    attempt.[¶](#change-daa887aa6b3dccbb6a979e6d7ecfd2cb)

-   **[sqlite]
    [bug]**支持已经添加到 SQLite 类型反射，以完全支持[http://www.sqlite.org/datatype3.html 中指定的“类型关联”
    T2\>。](http://www.sqlite.org/datatype3.html)在此方案中，位于类型名称中的`INT`，`CHAR`，`BLOB`或`REAL`等关键字通常会将类型与五个亲缘之一。请求礼貌 Erich Blume。

    也可以看看

    [Type Reflection](dialects_sqlite.html#sqlite-type-reflection)

    [¶](#change-c8dda32a20ab1a2a6020cd0b56a025cf)

    参考文献：[请求 github：65](https://github.com/zzzeek/sqlalchemy/pull/65)

### 杂项[¶ T0\>](#change-0.9.3-misc "Permalink to this headline")

-   **[feature]
    [examples]**为版本化行示例添加了可选的“changed”列，以及支持版本化的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")具有显式[`schema`](core_metadata.html#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")请求礼貌 jplaverdure。[¶](#change-6e2fa11bc1b490afa61009b74983d414)

    参考文献：[请求 github：41](https://github.com/zzzeek/sqlalchemy/pull/41)

-   **[bug] [ext]**Fixed bug where the [`AutomapBase`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
    class of the new automap extension would fail if classes were
    pre-arranged in single or potentially joined inheritance patterns.
    修复后的已连接继承问题也可能在使用[`DeferredReflection`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")时潜在地适用。[¶](#change-30674584c851329f071d2f6c65eb6630)

0.9.2 [¶ T0\>](#change-0.9.2 "Permalink to this headline")
----------------------------------------------------------

发布时间：2014 年 2 月 2 日

### ORM [¶ T0\>](#change-0.9.2-orm "Permalink to this headline")

-   **[orm]
    [feature]**添加了一个新参数[`Operators.op.is_comparison`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")。该标志允许来自[`Operators.op()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")的自定义操作被视为“比较”操作符，因此可用于自定义[`relationship.primaryjoin`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")条件。

    也可以看看

    [Using custom operators in join
    conditions](orm_join_conditions.html#relationship-custom-operator)中使用自定义运算符

    [¶](#change-2dc2e780e8373cbbb7b3d14048f7f7dd)

-   **[orm] [feature]**为提供[`join()`](core_selectable.html#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")结构作为[`relationship.secondary`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")的目标，支持得到了改进。复杂的[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")连接条件。该更改包括对查询连接的调整，加入的预加载以不呈现 SELECT 子查询，更改为延迟加载以使“辅助”目标正确包含在 SELECT 中，并更改为声明以更好地支持指定 join()对象以班级为目标。

    新的使用案例有点实验性，但增加了新的文档部分。

    也可以看看

    [Composite “Secondary”
    Joins](orm_join_conditions.html#composite-secondary-join)

    [¶](#change-a8b3a5b9943f34a153c535d66ec180f9)

-   当一个迭代器对象被传递给[`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")或类似的错误消息时，修正错误消息，其中错误将无法在字符串格式上呈现。**[orm]
    [bug]**Pullleq 礼貌 Kyle
    Stark。[¶](#change-1c3f8f5feedf0bfccec2acf81dc4d612)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[请求 github：58](https://github.com/zzzeek/sqlalchemy/pull/58)

-   **[orm] [bug]**Fixed bug in new [`TextAsFrom`](core_selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")
    construct where [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")-
    oriented row lookups were not matching up to the ad-hoc
    [`ColumnClause`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")
    objects that [`TextAsFrom`](core_selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")
    generates, thereby making it not usable as a target in
    [`Query.from_statement()`](orm_query.html#sqlalchemy.orm.query.Query.from_statement "sqlalchemy.orm.query.Query.from_statement").
    还修复了[`Query.from_statement()`](orm_query.html#sqlalchemy.orm.query.Query.from_statement "sqlalchemy.orm.query.Query.from_statement")结构，使其不会将[`TextAsFrom`](core_selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")误认为[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")结构。当调用`Text.columns()`方法以适应[`text.typemap`](core_sqlelement.html#sqlalchemy.sql.expression.text.params.typemap "sqlalchemy.sql.expression.text")参数时，此 bug 也是 0.9 回归。[¶](#change-87563ee95139d715f8d0326c80758a47)

    参考文献：[＃2932](http://www.sqlalchemy.org/trac/ticket/2932)

-   **[orm]
    [bug]**在属性“set”操作的范围内添加了一个新的指令，用于在属性需要延迟加载“old”值的情况下禁用 autoflush，如在替换一对一值或某种多对一时。此时的刷新否则会发生在属性为 None 且可能导致 NULL 违反的地方。[¶](#change-6dde90e6801f9bdf0bec0d5ba49cd086)

    参考文献：[＃2921](http://www.sqlalchemy.org/trac/ticket/2921)

-   **[orm] [bug]**Fixed an 0.9 regression where the automatic aliasing
    applied by [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    and in other situations where selects or joins were aliased (such as
    joined table inheritance) could fail if a user-defined
    [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    subclass were used in the expression.
    在这种情况下，子类将无法传播适应所需的 ORM 特定“注释”。“表达注解”系统已被纠正以解释这种情况。[¶](#change-03749d6f654c1889673b5e0c12e79baf)

    参考文献：[＃2918](http://www.sqlalchemy.org/trac/ticket/2918)

-   **[orm] [bug]**Fixed a bug involving the new flattened JOIN
    structures which are used with [`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")
    (thereby causing a regression in joined eager loading) as well as
    [`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")
    in conjunction with the `flat=True` flag and
    joined-table inheritance; basically multiple joins across a “parent
    JOIN sub” entity using different paths to get to a target class
    wouldn’t form the correct ON conditions.
    在一个别名和连接类的情况下，在计算连接的“左侧”的机制中做出的调整/简化修复了这个问题。[¶](#change-c0f8554831a29dce282bda7f4a1fced7)

    参考文献：[＃2908](http://www.sqlalchemy.org/trac/ticket/2908)

### 发动机[¶ T0\>](#change-0.9.2-engine "Permalink to this headline")

-   **[engine] [feature]
    [pool]**添加了一个新的池事件[`PoolEvents.invalidate()`](core_events.html#sqlalchemy.events.PoolEvents.invalidate "sqlalchemy.events.PoolEvents.invalidate")。当 DBAPI 连接被标记为“invaldated”并从池中丢弃时调用。[¶](#change-8b18bdd2f4b3ca051745c279938e63c4)

### SQL [¶ T0\>](#change-0.9.2-sql "Permalink to this headline")

-   **[sql] [feature]**增加了[`MetaData.reflect.**dialect_kwargs`](core_metadata.html#sqlalchemy.schema.MetaData.reflect.params.**dialect_kwargs "sqlalchemy.schema.MetaData.reflect")以支持反映的所有[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的方言级反射选项。[¶
    T8\>](#change-4f8918d438f70e33f0202a0ebf9ab58b)

-   **[sql]
    [feature]**添加了一项新功能，允许自动命名约定应用于[`Constraint`](core_constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")和[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象。根据 Wiki 中的配方，新功能使用架构事件来设置名称，因为各种架构对象都相互关联。The
    events then expose a configuration system through a new argument
    [`MetaData.naming_convention`](core_metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData").
    This system allows production of both simple and custom naming
    schemes for constraints and indexes on a per-[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    basis.

    也可以看看

    [Configuring Constraint Naming
    Conventions](core_constraints.html#constraint-naming-conventions)

    [¶](#change-7a930bef6cc4cbf8fd14845482204265)

    参考文献：[＃2923](http://www.sqlalchemy.org/trac/ticket/2923)

-   **[sql] [feature]**现在可以在[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")对象上指定选项，与`primary_key=True`旗；使用没有列的[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")对象来实现这个结果。

    Previously, an explicit [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
    would have the effect of those columns marked as
    `primary_key=True` being ignored; since this is
    no longer the case, the [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
    will now assert that either one style or the other is used to
    specify the columns, or if both are present, that the column lists
    match exactly. 如果[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")和[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中标记为`primary_key=True`的列中存在不一致的列，则会发出警告，并且列表的列仅从[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")单独获取，就像以前版本中的情况一样。

    也可以看看

    [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")

    [¶](#change-87912ddc5217c8d309bca24da22147bb)

    参考文献：[＃2910](http://www.sqlalchemy.org/trac/ticket/2910)

-   **[sql]
    [feature]**增强了模式构造和某些 SQL 构造接受特定于方言的关键字参数的系统。This
    system includes commonly the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    and [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    constructs, which accept a wide variety of dialect-specific
    arguments such as `mysql_engine` and
    `postgresql_where`, as well as the constructs
    [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint"),
    [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint"),
    [`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update"),
    [`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
    and [`Delete`](core_dml.html#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete"),
    and also newly added kwarg capability to
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    and [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey").
    改变之处在于参与方言现在可以为这些结构指定可接受的参数列表，如果为特定方言指定了无效关键字，则允许引发参数错误。如果关键字的方言部分无法识别，则仅发出警告；尽管系统实际上会使用 setuptools 入口点来定位非本地方言，但仍支持在卸载该第三方方言的环境中使用某些特定方言特定参数的用例。方言也必须明确地选择加入这个系统，以便不使用这个系统的外部方言不会受到影响。[¶](#change-2df4f7fe29c0f5aa2f957f4a89b0d74d)

    参考文献：[＃2866](http://www.sqlalchemy.org/trac/ticket/2866)

-   **[sql] [bug]**The behavior of [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    has been adjusted such that the schema target of a
    [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    will not be changed unless that schema matches that of the parent
    table.
    也就是说，如果表“schema\_a.user”具有“schema\_b.order.id”的外键，则不论“schema”参数是否传递给[`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")但是，如果表“schema\_a.user”引用“schema\_a.order.id”，则会在父表和引用表上更新“schema\_a”的存在。这是一种行为改变，因此不可能回到 0.8；假设之前的行为是非常有问题的，并且不太可能有人依赖它。

    此外，还添加了一个新参数[`Table.tometadata.referred_schema_fn`](core_metadata.html#sqlalchemy.schema.Table.tometadata.params.referred_schema_fn "sqlalchemy.schema.Table.tometadata")。这指的是一个可调用函数，它将用于确定 tometadata 操作中遇到的任何[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")的新引用模式。这个可调用的函数可以用来恢复到之前的行为或者定制如何在每个约束的基础上处理引用的模式。

    [¶](#change-d4cf4109c92f5c593c0eb29a55e23b2f)

    参考文献：[＃2913](http://www.sqlalchemy.org/trac/ticket/2913)

-   **[sql] [bug]**Fixed bug whereby binary type would fail in some
    cases if used with a “test” dialect, such as a DefaultDialect or
    other dialect with no
    DBAPI.[¶](#change-a2d477b9294340f7ec81a1b359bee6cc)

-   **[sql] [bug] [py3k]**Fixed bug where “literal binds” wouldn’t work
    with a bound parameter that’s a binary type.
    一个类似但不同的问题在 0.8 中得到了解决。[¶](#change-f7ed7a7bdd579cfb59afaf713ec2da5c)

-   **[sql] [bug]**Fixed regression whereby the “annotation” system used
    by the ORM was leaking into the names used by standard functions in
    [`sqlalchemy.sql.functions`](core_functions.html#module-sqlalchemy.sql.functions "sqlalchemy.sql.functions"),
    such as `func.coalesce()` and
    `func.max()`.
    在 ORM 属性中使用这些函数，从而生成它们的注释版本可能会破坏在 SQL 中呈现的实际函数名称。[¶](#change-182243baf075d92a029213dbd8041026)

    参考文献：[＃2927](http://www.sqlalchemy.org/trac/ticket/2927)

-   **[sql] [bug]**Fixed 0.9 regression where the new sortable support
    for [`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")
    would lead to `TypeError` when compared to
    non-tuple types as it attempted to apply tuple() to the “other”
    object unconditionally. The full range of Python comparison
    operators have now been implemented on [`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy"),
    using an approach that guarantees a comparison system that is
    equivalent to that of a tuple, and the “other” object is only
    coerced if it’s an instance of
    RowProxy.[¶](#change-3fe73b94064bab8326605943165bdf71)

    参考文献：[＃2924](http://www.sqlalchemy.org/trac/ticket/2924)，[＃2848](http://www.sqlalchemy.org/trac/ticket/2848)

-   **[sql] [bug]**与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")内联创建的[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")将被跳过。Pullreq 礼貌 Derek
    Harland。[¶](#change-808b13e7a37e3b773154107db0509031)

    参考：[拉取请求 bitbucket：11](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/11)

-   **[sql] [bug] [orm]**Fixed the multiple-table “UPDATE..FROM”
    construct, only usable on MySQL, to correctly render the SET clause
    among multiple columns with the same name across tables.
    这也将仅用于非主表的 SET 子句中用于绑定参数的名称更改为“\_
    ”；因为通常直接使用[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象指定此参数，所以不应该对应用程序产生影响。
    T1\> T0\>该修订对 ORM 中的[`Table.update()`](core_metadata.html#sqlalchemy.schema.Table.update "sqlalchemy.schema.Table.update")以及[`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")生效。[¶](#change-e78b46088d529294a0abdee2cd8fe000)

    参考文献：[＃2912](http://www.sqlalchemy.org/trac/ticket/2912)

### 架构[¶ T0\>](#change-0.9.2-schema "Permalink to this headline")

-   **[schema] [bug]**将`sqlalchemy.schema.SchemaVisitor`还原到`.schema`模块。Pullreq 礼貌 Sean
    Dague。[¶](#change-3a49a58c161e46ce5b9d89e2758041b3)

    参考文献：[请求 github：57](https://github.com/zzzeek/sqlalchemy/pull/57)

### 的 PostgreSQL [¶ T0\>](#change-0.9.2-postgresql "Permalink to this headline")

-   **[postgresql]
    [feature]**添加了一个新的方言级参数`postgresql_ignore_search_path`；这个参数被[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造函数和[`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")方法所接受。当用于 Postgresql 时，即使名称存在于`search_path`中，指定远程模式名称的外键引用表也将保留该模式名称；从 0.7.3 开始的默认行为就是`search_path`中的模式不会被复制到反映的[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象。文档已经更新，详细描述了`pg_get_constraintdef()`函数的行为，以及`postgresql_ignore_search_path`特性如何基本确定我们是否会遵守此函数报告的模式限定或不。

    也可以看看

    [Remote-Schema Table Introspection and Postgresql
    search\_path](dialects_postgresql.html#postgresql-schema-reflection)

    [¶](#change-aff5edc2e351865134d3aecbac9ae00d)

    参考文献：[＃2922](http://www.sqlalchemy.org/trac/ticket/2922)

### MySQL 的[¶ T0\>](#change-0.9.2-mysql "Permalink to this headline")

-   **[mysql]
    [bug]**添加到 cymysql 方言的一些缺失方法，包括\_get\_server\_version\_info()和\_detect\_charset()。Pullreq 礼貌 Hajime
    Nakagami。[¶](#change-c9d1183ac37b97cd9bba811e075e7ee1)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[pull request
    github：61](https://github.com/zzzeek/sqlalchemy/pull/61)

-   **[mysql] [bug] [sql]**Added new test coverage for so-called “down
    adaptions” of SQL types, where a more specific type is adapted to a
    more generic one - this use case is needed by some third party tools
    such as `sqlacodegen`.
    这个测试套件中需要修复的特定情况是将[`mysql.ENUM`](dialects_mysql.html#sqlalchemy.dialects.mysql.ENUM "sqlalchemy.dialects.mysql.ENUM")向下转换为[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")，并将 SQLite 日期类型转换为通用日期类型。`adapt()`方法需要在这里变得更具体，以抵消在基础[`TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")中删除“catch
    all”`**kwargs`在 0.9 中被删除的类。[¶](#change-c46c51b91fba93f95b0a32692149e285)

    参考文献：[＃2917](http://www.sqlalchemy.org/trac/ticket/2917)

-   **[mysql] [bug]** MySQL
    CAST 编译现在考虑了诸如“charset”和“collat​​ion”之类的字符串类型的方面。While
    MySQL wants all character- based CAST calls to use the CHAR type, we
    now create a real CHAR object at CAST time and copy over all the
    parameters it has, so that an expression like
    `cast(x, mysql.TEXT(charset='utf8'))` will
    render `CAST(t.col AS CHAR CHARACTER SET utf8)`.[¶](#change-5e11ddb98a45933e5e3e4cc3649b5932)

-   **[mysql] [bug]**Added new “unicode returns” detection to the MySQL
    dialect and to the default dialect system overall, such that any
    dialect can add extra “tests” to the on-first-connect “does this
    DBAPI return unicode directly?” detection.
    在这种情况下，我们正在使用明确的“utf8\_bin”排序规则类型（在检查此排序规则可用后）专门针对“utf8”编码添加一个检查以检测 MySQLdb
    1.2.3 版中观察到的一些错误的 unicode 行为。虽然 MySQLdb 自 1.2.4 起解决了此问题，但此处的检查应防止回归。该更改还允许“unicode”检查登录引擎日志，这在以前并非如此。[¶](#change-5306ccbcd637857024e7f7526badb84e)

    参考文献：[＃2906](http://www.sqlalchemy.org/trac/ticket/2906)

-   **[mysql] [bug] [engine] [pool]**[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
    now associates a new `RootTransaction` or [`TwoPhaseTransaction`](core_connections.html#sqlalchemy.engine.TwoPhaseTransaction "sqlalchemy.engine.TwoPhaseTransaction")
    with its immediate [`_ConnectionFairy`](core_pooling.html#sqlalchemy.pool._ConnectionFairy "sqlalchemy.pool._ConnectionFairy")
    as a “reset handler” for the span of that transaction, which takes
    over the task of calling commit() or rollback() for the “reset on
    return” behavior of [`Pool`](core_pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
    if the transaction was not otherwise completed.
    这解决了当没有显式回滚或提交时连接关闭时，像 MySQL 两阶段那样的挑剔事务将被正确关闭的问题（例如，在这种情况下，不再提出“XAER\_RMFAIL”
    - 注意这仅在日志记录中显示因为异常不会在池重置内传播）。This issue
    would arise e.g. when using an orm [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    with `twophase` set, and then
    [`Session.close()`](orm_session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")
    is called without an explicit rollback or commit.
    此更改还具有以下效果，即在非自动提交模式下使用[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象时，您现在将在日志中看到明确的“ROLLBACK”，无论会话被丢弃的方式如何。感谢 Jeff
    Dairiki 和 Laurence
    Rowe 将此问题隔离开来。[¶](#change-f9af1f23fa7c0156a51404d81df8f88c)

    参考文献：[＃2907](http://www.sqlalchemy.org/trac/ticket/2907)

### 源码[¶ T0\>](#change-0.9.2-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**Fixed bug whereby SQLite compiler failed to
    propagate compiler arguments such as “literal binds” into a CAST
    expression.[¶](#change-f340e82cab2db7a33792c8734bd3dd2c)

### MSSQL [¶ T0\>](#change-0.9.2-mssql "Permalink to this headline")

-   **[mssql] [feature]**为[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")和[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")结构添加了一个选项`mssql_clustered`在 SQL Server 上，这将`CLUSTERED`关键字添加到 DDL 中的约束结构中。Pullreq 礼貌 Derek
    Harland。[¶](#change-2f279749d1dbc19d2dcab58b0a56c870)

    参考：[拉取请求 bitbucket：11](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/11)

### 预言[¶ T0\>](#change-0.9.2-oracle "Permalink to this headline")

-   **[oracle] [bug]**It’s been observed that the usage of a cx\_Oracle
    “outputtypehandler” in Python 2.xx in order to coerce string values
    to Unicode is inordinately expensive; even though cx\_Oracle is
    written in C, when you pass the Python `unicode`
    primitive to cursor.var() and associate with an output handler, the
    library counts every conversion as a Python function call with all
    the requisite overhead being recorded; this *despite* the fact when
    running in Python 3, all strings are also unconditionally coerced to
    unicode but it does *not* incur this overhead, meaning that
    cx\_Oracle is failing to use performant techniques in Py2K.
    由于 SQLAlchemy 无法轻松地以每列为基础选择此类型的处理程序类型，因此无条件地组装处理程序，从而将开销添加到所有字符串访问。

    所以这个逻辑已经被 SQLAlchemy 自己的 unicode 转换系统所替代，现在它只在 Py2K 中对需要 unicode 的列起作用。当使用 C 扩展时，SQLAlchemy 的系统似乎比 cx\_Oracle 快 2-3 倍。此外，SQLAlchemy 的 unicode 转换功能得到了增强，因此当需要“条件”转换器（现在需要用于 Oracle 后端）时，“已经是 unicode”的检查现在在 C 中执行，不再引入大量开销。

    此更改对 cx\_Oracle 后端有两个影响。一个是 Py2K 中没有被 Unicode 类型或 convert\_unicode
    = True 明确请求的字符串值现在将返回为`str`，而不是`unicode` -
    此行为与后端如 MySQL。另外，当使用 cx\_Oracle 后端请求 unicode 值时，如果 C 扩展名*not*被使用，现在每列有一个额外的 isinstance()检查开销。这种权衡已经被制定出来，因为它可以被解决，并且不会给可能的大部分非 Unicode 字符串的 Oracle 结果列带来性能负担。

    [¶](#change-2cd0a6583e825c62477ab7a3d4770de9)

    参考文献：[＃2911](http://www.sqlalchemy.org/trac/ticket/2911)

### 杂项[¶ T0\>](#change-0.9.2-misc "Permalink to this headline")

-   **[bug] [examples]**Added a tweak to the “history\_meta” example
    where the check for “history” on a relationship-bound attribute will
    now no longer emit any SQL if the relationship is
    unloaded.[¶](#change-b3122f01ed7d8d120a8035233320d558)

-   **[bug] [pool]** [`PoolEvents.reset()`](core_events.html#sqlalchemy.events.PoolEvents.reset "sqlalchemy.events.PoolEvents.reset")事件的参数名称已重命名为`dbapi_connection`和`connection_record`预计这个相对较新且很少使用的事件的现有侦听器在任何情况下都会使用位置风格来接收参数。[¶](#change-34c66a5b820b990e8ccde1cb2eee76c2)

-   **[bug] [cextensions] [py3k]**Fixed an issue where the C extensions
    in Py3K are using the wrong API to specify the top-level module
    function, which breaks in Python 3.4b2.
    Py3.4b2 将 PyMODINIT\_FUNC 改为返回“void”而不是`PyObject *`，所以我们现在确保使用“PyMODINIT\_FUNC”而不是`PyObject *`。拉请求礼貌 cgohlke。[¶](#change-98b1a028c00831d12344a81c2928019c)

    参考文献：[请求 github：55](https://github.com/zzzeek/sqlalchemy/pull/55)

0.9.1 [¶ T0\>](#change-0.9.1 "Permalink to this headline")
----------------------------------------------------------

发布时间：2014 年 1 月 5 日

### ORM [¶ T0\>](#change-0.9.1-orm "Permalink to this headline")

-   **[orm] [feature]
    [extensions]**添加了一个新的**实验性**扩展[`sqlalchemy.ext.automap`](orm_extensions_automap.html#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")。This
    extension expands upon the functionality of Declarative as well as
    the [`DeferredReflection`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")
    class to produce a base class which automatically generates mapped
    classes *and relationships* based on table metadata.

    也可以看看

    [Automap Extension](migration_09.html#feature-automap)

    [Automap](orm_extensions_automap.html)

    [¶](#change-03a1682f97f04e9969b1eedfea573837)

-   **[orm] [bug] [events]**Fixed regression where using a
    `functools.partial()` with the event system
    would cause a recursion overflow due to usage of
    inspect.getargspec() on it in order to detect a legacy calling
    signature for certain events, and apparently there’s no way to do
    this with a partial object.
    相反，我们跳过了传统支票并采用现代风格；检查本身现在只发生在 SessionEvents.after\_bulk\_update 和 SessionEvents.after\_bulk\_delete 事件中。如果分配给“部分”事件侦听器，那么这两个事件将需要新的签名样式。[¶](#change-8aeefcaaa4a378dba8faa4278d991e73)

    参考文献：[＃2905](http://www.sqlalchemy.org/trac/ticket/2905)

-   **[orm] [bug]**Fixed bug where using new [`Session.info`](orm_session_api.html#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")
    attribute would fail if the `.info` argument
    were only passed to the [`sessionmaker`](orm_session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")
    creation call but not to the object itself. Courtesy Robin
    Schoonover。[¶](#change-590902684e2acb993441b174c1ab59a3)

    参考文献：[pull request
    bitbucket：9](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/9)

-   **[orm] [bug]**Fixed regression where we don’t check the given name
    against the correct string class when setting up a backref based on
    a name, therefore causing the error “too many values to unpack”.
    这与 Py3k 转换有关。[¶](#change-53e42d12ab61af327a7559207a6211b4)

    参考文献：[＃2901](http://www.sqlalchemy.org/trac/ticket/2901)

-   **[orm] [bug]**Fixed regression where we apparently still create an
    implicit alias when saying query(B).join(B.cs), where “C” is a
    joined inh class; however, this implicit alias was created only
    considering the immediate left side, and not a longer chain of joins
    along different joined-inh subclasses of the same base.
    只要我们在这种情况下仍然隐含别名，行为就会被拨回一点，这样它就会在各种各样的情况下混淆右侧。[¶](#change-48eab507305f1712468f94e36bc07cfb)

    参考文献：[＃2903](http://www.sqlalchemy.org/trac/ticket/2903)

### orm declarative [¶](#change-0.9.1-orm-declarative "Permalink to this headline")

-   **[bug] [orm] [declarative]**Fixed an extremely unlikely memory
    issue where when using [`DeferredReflection`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")
    to define classes pending for reflection, if some subset of those
    classes were discarded before the
    [`DeferredReflection.prepare()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection.prepare "sqlalchemy.ext.declarative.DeferredReflection.prepare")
    method were called to reflect and map the class, a strong reference
    to the class would remain held within the declarative internals.
    这个“映射类的内部集合”现在使用对这些类本身的弱引用。[¶](#change-0f3dd659714e45e0f577963d43d7d5aa)

-   **[bug] [orm]
    [declarative]**一个准回归，显然在 0.8 中，您可以在声明式中设置一个类级属性，以直接引用一个[`InstrumentedAttribute`](orm_internals.html#sqlalchemy.orm.attributes.InstrumentedAttribute "sqlalchemy.orm.attributes.InstrumentedAttribute")超类或类本身，它或多或少地像一个同义词；在 0.9 中，这没有设置足够的簿记来跟上来自[＃2789](http://www.sqlalchemy.org/trac/ticket/2789)的更自由化的后退逻辑。尽管这个用例从来没有被直接考虑过，但是现在通过声明在“setattr()”级别以及设置子类时检测到，并且镜像/重命名属性现在设置为[`synonym()`](orm_mapped_attributes.html#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")。[¶](#change-4bf7b34989a71c9289696d84c85cc213)

    参考文献：[＃2900](http://www.sqlalchemy.org/trac/ticket/2900)

### SQL [¶ T0\>](#change-0.9.1-sql "Permalink to this headline")

-   **[sql] [feature]**Conjunctions like [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
    and [`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")
    can now accept Python generators as a single argument, e.g.:

        and_(x == y for x, y in tuples)

    这里的逻辑查找单个参数`*args`，其中第一个元素是`types.GeneratorType`的实例。

    [¶](#change-e56929f2d249d5a65bd72271366f4ad3)

### 架构[¶ T0\>](#change-0.9.1-schema "Permalink to this headline")

-   **[schema] [feature]**The [`Table.extend_existing`](core_metadata.html#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")
    and [`Table.autoload_replace`](core_metadata.html#sqlalchemy.schema.Table.params.autoload_replace "sqlalchemy.schema.Table")
    parameters are now available on the [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
    method.[¶](#change-08112f9e5e2d64a1f0236743dbd072a4)

0.9.0 [¶ T0\>](#change-0.9.0 "Permalink to this headline")
----------------------------------------------------------

发布日期：2013 年 12 月 30 日

### ORM [¶ T0\>](#change-0.9.0-orm "Permalink to this headline")

-   **[orm] [feature]**The [`exc.StatementError`](core_exceptions.html#sqlalchemy.exc.StatementError "sqlalchemy.exc.StatementError")
    or DBAPI-related subclass now can accommodate additional information
    about the “reason” for the exception; the [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    now adds some detail to it when the exception occurs within an
    autoflush. This approach is taken as opposed to combining
    [`FlushError`](orm_exceptions.html#sqlalchemy.orm.exc.FlushError "sqlalchemy.orm.exc.FlushError")
    with a Python 3 style “chained exception” approach so as to maintain
    compatibility both with Py2K code as well as code that already
    catches `IntegrityError` or
    similar.[¶](#change-6f14ee03b908f78d8d174e7ef588746d)

-   **[orm] [feature] [backrefs]**Added new argument
    `include_backrefs=True` to the
    [`validates()`](orm_mapped_attributes.html#sqlalchemy.orm.validates "sqlalchemy.orm.validates")
    function; when set to False, a validation event will not be
    triggered if the event was initated as a backref to an attribute
    operation from the other side.

    也可以看看

    [include\_backrefs=False option for
    @validates](migration_09.html#feature-1535)的 include\_backrefs =
    False 选项

    [¶](#change-45720dc1b5014ca04cc355970a4a77ae)

    参考文献：[＃1535](http://www.sqlalchemy.org/trac/ticket/1535)

-   **[orm] [feature]**A new API for specifying the
    `FOR UPDATE` clause of a `SELECT` is added with the new [`Query.with_for_update()`](orm_query.html#sqlalchemy.orm.query.Query.with_for_update "sqlalchemy.orm.query.Query.with_for_update")
    method, to complement the new
    [`GenerativeSelect.with_for_update()`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")
    method. 请求提供 Mario Lassnig 提供的请求。

    也可以看看

    [New FOR UPDATE support on select(),
    Query()](migration_09.html#feature-github-42)上的新 FOR UPDATE 支持

    [¶](#change-1144ec1f7338720f8b1ea74ccda5f49b)

    参考文献：[请求 github：42](https://github.com/zzzeek/sqlalchemy/pull/42)

-   **[orm] [bug]**调整[`subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")策略，确保查询在加载过程开始后运行；这是为了使得子查询优先于其他装载者，因为其他的加载者可能在错误的时间因为其他的预先/非加载情况而触及相同的属性。[](#change-596ed6934e304cb10692a3ddea823f90)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2887](http://www.sqlalchemy.org/trac/ticket/2887)

-   **[orm] [bug]**Fixed bug when using joined table inheritance from a
    table to a select/alias on the base, where the PK columns were also
    not same named; the persistence system would fail to copy primary
    key values from the base table to the inherited table upon
    INSERT.[¶](#change-73f5c9c3d26dc55718454012b0f6cbd7)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2885](http://www.sqlalchemy.org/trac/ticket/2885)

-   **[orm] [bug]**[`composite()`](orm_composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
    will raise an informative error message when the columns/attribute
    (names) passed don’t resolve to a Column or mapped attribute (such
    as an erroneous tuple); previously raised an unbound
    local.[¶](#change-87f8c9385495cffe875cfa574f7a3063)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2889](http://www.sqlalchemy.org/trac/ticket/2889)

-   **[orm] [bug]**Fixed a regression introduced by
    [\#2818](http://www.sqlalchemy.org/trac/ticket/2818) where the
    EXISTS query being generated would produce a “columns being
    replaced” warning for a statement with two same-named columns, as
    the internal SELECT wouldn’t have use\_labels
    set.[¶](#change-a97169e0a5e5a559f46bd8e3f7e58fc4)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2818](http://www.sqlalchemy.org/trac/ticket/2818)

-   **[orm] [bug] [collections] [py3k]**Added support for the Python 3
    method `list.clear()` within the ORM collection
    instrumentation system; pull request courtesy Eduardo
    Schettino.[¶](#change-c178432e123c26d95767915cfd94145b)

    参考文献：[请求 github：40](https://github.com/zzzeek/sqlalchemy/pull/40)

-   **[orm]
    [bug]**关于描述符的一些改进，如混合，同义词，合成，用户定义的描述符等。[`AliasedClass`](orm_query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")继续进行的属性适配变得更加健壮，例如，如果描述符返回另一个插装属性，而不是复合 SQL 表达式元素，则操作仍将继续。Addtionally,
    the “adapted” operator will retain its class; previously, a change
    in class from `InstrumentedAttribute` to
    `QueryableAttribute` (a superclass) would
    interact with Python’s operator system such that an expression like
    `aliased(MyClass.x) > MyClass.x` would reverse
    itself to read `myclass.x < myclass_1.x`.
    修改后的属性也会将新的[`AliasedClass`](orm_query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")作为它的父项，这在以前并不总是这样。[¶](#change-524c3fc2a92c716633ad362ee5de0c41)

    参考文献：[＃2872](http://www.sqlalchemy.org/trac/ticket/2872)

-   **[orm] [bug]**The `viewonly` flag on
    [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    will now prevent attribute history from being written on behalf of
    the target attribute.
    如果对象没有被写入 Session.dirty 列表，如果它发生了变化，这会产生影响。以前，该对象将出现在 Session.dirty 中，但在刷新期间不会发生代表修改后的属性的更改。该属性仍然会发出诸如 backref 事件和用户定义的事件之类的事件，并且仍然会从 backrefs 中接收到突变。

    也可以看看

    [viewonly=True on relationship() prevents history from taking
    effect](migration_09.html#migration-2833)

    [¶](#change-cd9ee851b4fed4be44aa3357d3ea656e)

    参考文献：[＃2833](http://www.sqlalchemy.org/trac/ticket/2833)

-   **[orm] [bug]**添加了对新的[`Session.info`](orm_session_api.html#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")属性对[`scoped_session`](orm_contextual.html#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")的支持。[¶](#change-57380df483eb4573627dd0c4cc6285b2)

-   **[orm] [bug]**Fixed bug where usage of new [`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")
    object would cause the [`Query.column_descriptions`](orm_query.html#sqlalchemy.orm.query.Query.column_descriptions "sqlalchemy.orm.query.Query.column_descriptions")
    attribute to fail.[¶](#change-74dca08530e2aa7327444a66c6c6d823)

-   **[orm] [bug] [sqlite] [sql]**Fixed a regression introduced by the
    join rewriting feature of
    [\#2369](http://www.sqlalchemy.org/trac/ticket/2369) and
    [\#2587](http://www.sqlalchemy.org/trac/ticket/2587) where a nested
    join with one side already an aliased select would fail to translate
    the ON clause on the outside correctly; in the ORM this could be
    seen when using a SELECT statement as a “secondary”
    table.[¶](#change-17f42ee3eb7206b1653e3a04460ff2a5)

    参考文献：[＃2858](http://www.sqlalchemy.org/trac/ticket/2858)

### orm declarative [¶](#change-0.9.0-orm-declarative "Permalink to this headline")

-   **[bug] [orm] [declarative]**Declarative does an extra check to
    detect if the same [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    is mapped multiple times under different properties (which typically
    should be a [`synonym()`](orm_mapped_attributes.html#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")
    instead) or if two or more [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    objects are given the same name, raising a warning if this condition
    is detected.[¶](#change-2160db7c02e08d3477c32ebfe806bf14)

    参考文献：[＃2828](http://www.sqlalchemy.org/trac/ticket/2828)

-   **[bug] [orm] [declarative]**已经增强了[`DeferredReflection`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")类，以便为[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")“secondary”,
    when specified either as a string table name, or as a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    object with only a name and [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    object will also be included in the reflection process when
    [`DeferredReflection.prepare()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection.prepare "sqlalchemy.ext.declarative.DeferredReflection.prepare")
    is called.[¶](#change-93a22c24dfcd871c8f872616c98d3b23)

    参考文献：[＃2865](http://www.sqlalchemy.org/trac/ticket/2865)

-   修正了在 Py2K 中使用[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")时，unicode 文字不会被接受为声明式中类或其他参数的字符串名称的错误。**[bug]
    [orm] [declarative]** \> [¶
    T5\>](#change-abd40b717be4a66e010edbce0f8dacb6)

### 发动机[¶ T0\>](#change-0.9.0-engine "Permalink to this headline")

-   **[engine] [feature]**The [`engine_from_config()`](core_engines.html#sqlalchemy.engine_from_config "sqlalchemy.engine_from_config")
    function has been improved so that we will be able to parse
    dialect-specific arguments from string configuration dictionaries.
    方言类现在可以提供自己的参数类型和字符串转换例程列表。但是，内置方言尚未使用该功能。[¶](#change-9e964e2f4332755c2be06fb8dfad0052)

    参考文献：[＃2875](http://www.sqlalchemy.org/trac/ticket/2875)

-   **[engine] [bug]**A DBAPI that raises an error on
    `connect()` which is not a subclass of
    dbapi.Error (such as `TypeError`,
    `NotImplementedError`, etc.)
    将不会传播异常。以前，特定于`connect()`例程的错误处理将通过方言的[`Dialect.is_disconnect()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.is_disconnect "sqlalchemy.engine.interfaces.Dialect.is_disconnect")例程错误地运行异常，并将其包装在[`sqlalchemy.exc.DBAPIError`](core_exceptions.html#sqlalchemy.exc.DBAPIError "sqlalchemy.exc.DBAPIError")它现在以与执行过程中发生的相同的方式传播。[¶](#change-b41267634efb6a5162eca78021998f59)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2881](http://www.sqlalchemy.org/trac/ticket/2881)

-   **[engine] [bug] [pool]**The [`QueuePool`](core_pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
    has been enhanced to not block new connection attempts when an
    existing connection attempt is blocking.
    以前，在监控溢出的块中，新连接的产生被串行化；溢出计数器现在在连接过程本身之外的其自己的临界区内被改变。[¶](#change-af2f363b02c9b82d6729e8e1c808d636)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2880](http://www.sqlalchemy.org/trac/ticket/2880)

-   **[engine] [bug] [pool]**Made a slight adjustment to the logic which
    waits for a pooled connection to be available, such that for a
    connection pool with no timeout specified, it will every half a
    second break out of the wait to check for the so-called “abort”
    flag, which allows the waiter to break out in case the whole
    connection pool was dumped; normally the waiter should break out due
    to a notify\_all() but it’s possible this notify\_all() is missed in
    very slim cases.
    这是在 0.8.0 中首次引入的逻辑的扩展，这个问题偶尔会在压力测试中被观察到。[¶](#change-33f71100778b84fb526ebd50c7e9468d)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2522](http://www.sqlalchemy.org/trac/ticket/2522)

-   **[engine] [bug]**Fixed bug where SQL statement would be improperly
    ASCII-encoded when a pre-DBAPI [`StatementError`](core_exceptions.html#sqlalchemy.exc.StatementError "sqlalchemy.exc.StatementError")
    were raised within [`Connection.execute()`](core_connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute"),
    causing encoding errors for non-ASCII statements.
    字符串化现在保留在 Python
    unicode 中，从而避免编码错误。[¶](#change-d789c97206bbfdf6d74064846660d3db)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2871](http://www.sqlalchemy.org/trac/ticket/2871)

-   **[engine] [bug]**The [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
    routine and the related [`make_url()`](core_engines.html#sqlalchemy.engine.url.make_url "sqlalchemy.engine.url.make_url")
    function no longer considers the `+` sign to be
    a space within the password field. 解析已经与 RFC
    1738 完全匹配，因为`username`和`password`只有`:`，`@` ，和`/`进行编码。

    也可以看看

    [The “password” portion of a create\_engine() no longer considers
    the + sign as an encoded space](migration_09.html#migration-2873)

    [¶](#change-54ee80068e58a88b092a47a6ddd0353d)

    参考文献：[＃2873](http://www.sqlalchemy.org/trac/ticket/2873)

-   **[engine] [bug]**The [`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")
    object is now sortable in Python as a regular tuple is; this is
    accomplished via ensuring tuple() conversion on both sides within
    the `__eq__()` method as well as the addition of
    a `__lt__()` method.

    也可以看看

    [RowProxy now has tuple-sorting
    behavior](migration_09.html#migration-2848)

    [¶](#change-cc0ce586ee4b6d177eb5504dadba1feb)

    参考文献：[＃2848](http://www.sqlalchemy.org/trac/ticket/2848)

### SQL [¶ T0\>](#change-0.9.0-sql "Permalink to this headline")

-   **[sql] [feature]**New improvements to the [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    construct, including more flexible ways to set up bound parameters
    and return types; in particular, a [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    can now be turned into a full FROM-object, embeddable in other
    statements as an alias or CTE using the new method
    [`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns").
    当构造体在“文字边界”上下文中编译时，[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构也可以呈现“内联”边界参数。

    也可以看看

    [New text() Capabilities](migration_09.html#feature-2877)

    [¶](#change-434eede0d7c5ab434a2634bb1c477426)

    参考文献：[＃2882](http://www.sqlalchemy.org/trac/ticket/2882)，[＃2877](http://www.sqlalchemy.org/trac/ticket/2877)

-   **[sql] [feature]**A new API for specifying the
    `FOR UPDATE` clause of a `SELECT` is added with the new
    [`GenerativeSelect.with_for_update()`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")
    method. This method supports a more straightforward system of
    setting dialect-specific options compared to the
    `for_update` keyword argument of
    [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
    and also includes support for the SQL standard
    `FOR UPDATE OF` clause.
    ORM 还包含一个新的相应方法[`Query.with_for_update()`](orm_query.html#sqlalchemy.orm.query.Query.with_for_update "sqlalchemy.orm.query.Query.with_for_update")。请求提供 Mario
    Lassnig 提供的请求。

    也可以看看

    [New FOR UPDATE support on select(),
    Query()](migration_09.html#feature-github-42)上的新 FOR UPDATE 支持

    [¶](#change-80575a82c6ca1e11cdf9bba117d2a012)

    参考文献：[请求 github：42](https://github.com/zzzeek/sqlalchemy/pull/42)

-   **[sql] [feature]**通过字符串将返回的浮点值强制转换为 Python
    `Decimal`时使用的精度现在可配置。The flag
    `decimal_return_scale` is now supported by all
    [`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")
    and [`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")
    types, which will ensure this many digits are taken from the native
    floating point value when it is converted to string.
    如果不存在，则该类型将使用`.scale`的值，如果类型支持此设置并且它不是 None。否则，使用原始的默认长度 10。

    也可以看看

    [Floating Point String-Conversion Precision Configurable for Native
    Floating Point Types](migration_09.html#feature-2867)

    [¶](#change-b05ab8cbc93a69cb1072bcae721b4ec6)

    参考文献：[＃2867](http://www.sqlalchemy.org/trac/ticket/2867)

-   **[sql] [bug]**Fixed issue where a primary key column that has a
    Sequence on it, yet the column is not the “auto increment” column,
    either because it has a foreign key constraint or
    `autoincrement=False` set, would attempt to fire
    the Sequence on INSERT for backends that don’t support sequences,
    when presented with an INSERT missing the primary key value.
    这将发生在像 SQLite，MySQL 这样的非序列后端上。[¶](#change-17f346ee6ecd1268fbc24fa52ca6fbb7)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2896](http://www.sqlalchemy.org/trac/ticket/2896)

-   **[sql] [bug]**Fixed bug with [`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
    method where the order of the given names would not be taken into
    account when generating the INSERT statement, thus producing a
    mismatch versus the column names in the given SELECT statement.
    还注意到[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")意味着不能使用 Python 端插入默认值，因为该语句没有 VALUES 子句。[¶](#change-8201a57e8a671eba9a5e14fb1d129e71)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2895](http://www.sqlalchemy.org/trac/ticket/2895)

-   **[sql] [bug]**The [`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")
    function, when given a plain literal value, will now apply the given
    type to the given literal value on the bind parameter side according
    to the type given to the cast, in the same manner as that of the
    [`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")
    function. 然而，与[`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")不同，只有当非子句元素值传递给[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")时才会生效。一个现有的类型化构造将保留其类型。[¶](#change-dd267693c4318fbd71e8ff2f00c3839c)

-   [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")类更积极地检查给定的列参数。**[sql]
    [bug]**如果不是字符串，它会检查该对象是否至少是一个[`ColumnClause`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")或解析为 1 的对象，并且`.table`属性（如果存在）指的是一个[`TableClause`](core_selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")或子类，而不像[`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")。否则，会引发[`ArgumentError`](core_exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。[¶](#change-8089bd064566ab520c8d752d8f44b7ea)

    参考文献：[＃2883](http://www.sqlalchemy.org/trac/ticket/2883)

-   **[sql] [bug]** [`ColumnOperators.collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")运算符的优先规则已被修改，因此 COLLATE 运算符的优先级低于比较运算符。这样做的结果是应用于比较的 COLLATE 不会在比较周围产生括号，而后者不会被 MSSQL 等后端解析。对于通过将`Operators.collate()`应用于比较表达式的单个元素而不是整个比较表达式来解决此问题的设置，此更改是向后兼容的。

    也可以看看

    [The precedence rules for COLLATE have been
    changed](migration_09.html#migration-2879)

    [¶](#change-fb4da0d066ca932a5f91af14f8541994)

    参考文献：[＃2879](http://www.sqlalchemy.org/trac/ticket/2879)

-   **[sql] [enhancement]**The exception raised when a
    [`BindParameter`](core_sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
    is present in a compiled statement without a value now includes the
    key name of the bound parameter in the error
    message.[¶](#change-55d6c5d7c76b54deb2d68f5e6ee4e501)

    这个改变也被**backported**修改为：0.8.5

### 架构[¶ T0\>](#change-0.9.0-schema "Permalink to this headline")

-   **[schema] [bug]**Fixed a regression caused by
    [\#2812](http://www.sqlalchemy.org/trac/ticket/2812) where the
    repr() for table and column names would fail if the name contained
    non-ascii characters.[¶](#change-eb0f69af2f52edcebc270889846a3f7d)

    参考文献：[＃2868](http://www.sqlalchemy.org/trac/ticket/2868)

### 的 PostgreSQL [¶ T0\>](#change-0.9.0-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**使用新的[`JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")类型添加了对 Postgresql
    JSON 的支持。非常感谢 Nathan
    Rice 实施和测试这个。[¶](#change-7b58abc6472e6a9756729e397c6ee060)

    参考文献：[＃2581](http://www.sqlalchemy.org/trac/ticket/2581)，[请求 github：50](https://github.com/zzzeek/sqlalchemy/pull/50)

-   **[postgresql] [feature]**通过[`postgresql.TSVECTOR`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.TSVECTOR "sqlalchemy.dialects.postgresql.TSVECTOR")类型增加了对 Postgresql
    TSVECTOR 的支持。请求礼貌 Noufal
    Ibrahim。[¶](#change-77977fae5177b45781690c834e63d13f)

    参考：[拉取请求 bitbucket：8](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/8)

-   **[postgresql] [bug]**Fixed bug where index reflection would
    mis-interpret indkey values when using the pypostgresql adapter,
    which returns these values as lists vs. psycopg2’s return type of
    string.[¶](#change-6c4b7c62d0cebe9f8e7fa158a55c506e)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2855](http://www.sqlalchemy.org/trac/ticket/2855)

-   **[postgresql] [bug]**现在使用 psycopg2
    UNICODEARRAY 扩展来处理带有 psycopg2 +普通“native
    unicode”模式的 unicode 数组，这与 UNICODE 扩展的使用方式一样[¶](#change-0d74908c0a46fa09168e385eecb4f0a1)

-   **[postgresql]
    [bug]**修正了 ENUM 中的值没有针对单引号转义的错误。请注意，这对于手动转义单引号的现有解决方法是向后不兼容的。

    也可以看看

    [Postgresql CREATE TYPE \<x\> AS ENUM now applies quoting to
    values](migration_09.html#migration-2878)

    [¶](#change-278c2212115d7604aa6ba7694c5c5965)

    参考文献：[＃2878](http://www.sqlalchemy.org/trac/ticket/2878)

### MySQL 的[¶ T0\>](#change-0.9.0-mysql "Permalink to this headline")

-   **[mysql] [bug]**改进了 SQL 类型在`__repr__()`中生成的系统，特别是关于宽整型/数字/字符类型各种关键字参数。The
    `__repr__()` is important for use with Alembic
    autogenerate for when Python code is rendered in a migration
    script.[¶](#change-aff523a757357ad13ae691047b8183cd)

    参考文献：[＃2893](http://www.sqlalchemy.org/trac/ticket/2893)

### MSSQL [¶ T0\>](#change-0.9.0-mssql "Permalink to this headline")

-   **[mssql] [bug] [firebird]**The “asdecimal” flag used with the
    [`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")
    type will now work with Firebird as well as the mssql+pyodbc
    dialects; previously the decimal conversion was not
    occurring.[¶](#change-9aad279410ec35f73c2ed835b9775263)

    这个改变也被**backported**修改为：0.8.5

-   **[mssql] [bug] [pymssql]**Added “Net-Lib error during Connection
    reset by peer” message to the list of messages checked for
    “disconnect” within the pymssql dialect. 礼貌 John
    Anderson。[¶](#change-f1ee7d7ea1eb2a0cb21a50ae1dea3fe9)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[请求 github：51](https://github.com/zzzeek/sqlalchemy/pull/51)

-   **[mssql] [bug]**修正了在 0.8.0 版本中引入索引的`DROP INDEX`如果索引处于备用模式中，MSSQL 将不正确地渲染； schemaname /
    tablename 将被颠倒。该格式也进行了修改以符合当前的 MSSQL 文档。Courtesy
    Derek Harland。[¶](#change-b65b88da0221c3f0bb0c2443185a5221)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[pull request
    bitbucket：7](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/7)

### 预言[¶ T0\>](#change-0.9.0-oracle "Permalink to this headline")

-   **[oracle]
    [bug]**增加了 ORA-02396“最大空闲时间”的错误代码到 cx\_oracle 的“is
    disconnect”代码列表。[¶](#change-9be5ac15b91d5ec132c4a6b689d5d15e)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2864](http://www.sqlalchemy.org/trac/ticket/2864)

-   **[oracle] [bug]**Fixed bug where Oracle `VARCHAR` types given with no length (e.g. for a `CAST` or similar) would incorrectly render `None CHAR` or similar.[¶](#change-495a336b8096587d32bf1959ae9c2509)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2870](http://www.sqlalchemy.org/trac/ticket/2870)

### 火鸟[¶ T0\>](#change-0.9.0-firebird "Permalink to this headline")

-   **[firebird] [bug]**火鸟方言会引用以下划线开头的标识符。Courtesy
    Treeve Jelbert。[¶](#change-0e80ff1217d1159ae0303de5c0ed4ec5)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2897](http://www.sqlalchemy.org/trac/ticket/2897)

-   **[firebird]
    [bug]**修正了 Firebird 索引反射中索引内的列未正确排序的错误；现在它们按照 RDB
    \$
    FIELD\_POSITION 的顺序排序。[¶](#change-eea51d8b16bb72d519c6f5a9cb105561)

    这个改变也被**backported**修改为：0.8.5

-   **[firebird] [bug]**Changed the queries used by Firebird to list
    table and view names to query from the `rdb$relations` view instead of the `rdb$relation_fields` and `rdb$view_relations` views.
    新旧查询的变体在许多常见问题和博客中都有提及，但新的查询直接来自“Firebird 常见问题解答”，它似乎是最正式的信息来源。[¶](#change-70bdabe000861535a7e228956add9020)

    参考文献：[＃2898](http://www.sqlalchemy.org/trac/ticket/2898)

### 杂项[¶ T0\>](#change-0.9.0-misc "Permalink to this headline")

-   **[removed]**“informix”和“informixdb”方言已被删除；该代码现在可作为 Bitbucket 上的单独存储库提供。自从首次添加 informixdb 方言以来，IBM-DB 项目已经提供了生产级别的 Informix 支持。[¶](#change-577e7805c86d301deafe2f47a2840148)

-   **[bug]
    [declarative]**错误消息，当一个字符串 arg 发送到[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，它没有解析为类或映射器时，它的工作方式与当收到一个非字符串 arg 时，它表明有配置错误的关系的名字。[¶](#change-b9609d3e6665e3b2e9cbc73bb84adebc)

    这个改变也被**backported**修改为：0.8.5

    参考文献：[＃2888](http://www.sqlalchemy.org/trac/ticket/2888)

-   **[bug] [ext]**Fixed bug which prevented the `serializer` extension from working correctly with table or column
    names that contain non-ASCII
    characters.[¶](#change-7b23b02498aded0119f08fe8df17cb20)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃2869](http://www.sqlalchemy.org/trac/ticket/2869)

-   **[bug] [examples]**修正了阻止 history\_meta
    recipe 使用超过一层深度的连接继承方案的错误。[¶](#change-51a37bd7516f5c6879964cfd09f1be56)

0.9.0b1 [¶ T0\>](#change-0.9.0b1 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2013 年 10 月 26 日

### 一般[¶ T0\>](#change-0.9.0b1-general "Permalink to this headline")

-   **[general] [feature] [py3k]**将 C 扩展移植到 Python
    3，并将在任何受支持的 CPython
    2 或 3 环境下构建。[¶](#change-63557d61147791e2c67e8fe819f1b2b2)

    参考文献：[＃2161](http://www.sqlalchemy.org/trac/ticket/2161)

-   **[general] [feature] [py3k]**现在，Python
    2 和 3 的代码库已经“就地”了，运行 2to3 的需求已被删除。兼容性现在在 Python
    2.6 上正向运行。[¶](#change-e1f88f4751daaf8c4bf39213780dfc1f)

    参考文献：[＃2671](http://www.sqlalchemy.org/trac/ticket/2671)

-   **[general]**对程序包的大量重构已重新组织了许多 Core 模块的导入结构以及 ORM 模块的某些方面。In
    particular `sqlalchemy.sql` has been broken out
    into several more modules than before so that the very large size of
    `sqlalchemy.sql.expression` is now pared down.
    这项努力的重点是大量减少进口周期。Additionally, the system of API
    functions in `sqlalchemy.sql.expression` and
    `sqlalchemy.orm` has been reorganized to
    eliminate redundancy in documentation between the functions vs. the
    objects they produce.[¶](#change-0858791080deb02ea2ef1c8aec366f29)

### ORM [¶ T0\>](#change-0.9.0b1-orm "Permalink to this headline")

-   **[orm] [feature]**添加了[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    `distinct_target_key`的新选项。这使得子查询预热加载器策略能够将 DISTINCT 应用到最内层的 SELECT 子查询中，以协助处理与该关系相对应的最内层查询生成重复行的情况（目前还没有解决内部 dupe 行问题的一般解决方案但是，当加入最内层子查询之外的子查询会产生欺骗）。当标志被设置为`True`时，DISTINCT 被无条件渲染，当它被设置为`None`时，如果最内层关系针对不包含完整的主键。该选项在 0.8 中默认为 False（例如，在所有情况下默认关闭），0.9 中的 None（例如默认为自动）。感谢 Alexander
    Koval 为此提供帮助。

    也可以看看

    [Subquery Eager Loading will apply DISTINCT to the innermost SELECT
    for some queries](migration_09.html#change-2836)

    [¶](#change-9262d71ee52f650e127ee71427812930)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2836](http://www.sqlalchemy.org/trac/ticket/2836)

-   **[orm] [feature]**The association proxy now returns
    `None` when fetching a scalar attribute off of a
    scalar relationship, where the scalar relationship itself points to
    `None`, instead of raising an
    `AttributeError`.

    也可以看看

    [Association Proxy Missing Scalar returns
    None](migration_09.html#migration-2810)

    [¶](#change-7df1b4e6150537b72c4b758277a44288)

    参考文献：[＃2810](http://www.sqlalchemy.org/trac/ticket/2810)

-   **[orm]
    [feature]**增加了新的方法[`AttributeState.load_history()`](orm_internals.html#sqlalchemy.orm.state.AttributeState.load_history "sqlalchemy.orm.state.AttributeState.load_history")，像[`AttributeState.history`](orm_internals.html#sqlalchemy.orm.state.AttributeState.history "sqlalchemy.orm.state.AttributeState.history")一样工作，但也触发加载器可调用。

    也可以看看

    [attributes.get\_history() will query from the DB by default if
    value not present](migration_09.html#change-2787)

    [¶](#change-17ada80ccb89c1e1109f3190e75092b5)

    参考文献：[＃2787](http://www.sqlalchemy.org/trac/ticket/2787)

-   **[orm] [feature]**新增加载选项[`orm.load_only()`](orm_loading_columns.html#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")。这允许将一系列列名指定为仅“加载”那些属性，推迟其余的属性。[¶](#change-3108052346d72a5b370a5dd64588efa8)

    参考文献：[＃1418](http://www.sqlalchemy.org/trac/ticket/1418)

-   **[orm]
    [feature]**加载器选项的系统已经完全重新架构，以构建更加全面的基础，即[`Load`](orm_query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")对象。这个基础允许任何常见的加载器选项，如[`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")，[`defer()`](orm_loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")等。以“链式”样式用于指定路径下的选项，如`joinedload("foo").subqueryload("bar")`。新系统取代了点分隔路径名的使用，选项中的多个属性以及`_all()`选项的用法。

    也可以看看

    [New Query Options API; load\_only()
    option](migration_09.html#feature-1418)

    [¶](#change-44e23631c9a2cd3d7341ba488a0ec775)

    参考文献：[＃1418](http://www.sqlalchemy.org/trac/ticket/1418)

-   **[orm] [feature]**The [`composite()`](orm_composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
    construct now maintains the return object when used in a
    column-oriented [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query"),
    rather than expanding out into individual columns.
    这使得内部使用新的[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")功能。这种行为是向后不相容的；要从将展开的组合列中进行选择，请使用`MyClass.some_composite.clauses`。

    也可以看看

    [Composite attributes are now returned as their object form when
    queried on a per-attribute
    basis](migration_09.html#migration-2824)查询时，复合属性现在以其对象形式返回

    [¶](#change-a1bb82ee5cb482c0985d71e1e82e3b50)

    参考文献：[＃2824](http://www.sqlalchemy.org/trac/ticket/2824)

-   **[orm] [feature]**添加了一个新的构造[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")，它允许将列表达式组指定为一个[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")构造。该列组默认情况下作为单个元组返回。可以重写[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")的行为，以向返回的行提供任何类型的结果处理。当在面向列的[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")中使用时，[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")的行为现在也嵌入到复合属性中。

    也可以看看

    [Column Bundles for ORM queries](migration_09.html#change-2824)

    [Composite attributes are now returned as their object form when
    queried on a per-attribute
    basis](migration_09.html#migration-2824)查询时，复合属性现在以其对象形式返回

    [¶](#change-e3d4b8c06aa3216a8f10452f097a17ae)

    参考文献：[＃2824](http://www.sqlalchemy.org/trac/ticket/2824)

-   **[orm] [feature]**The `version_id_generator`
    parameter of `Mapper` can now be specified to
    rely upon server generated version identifiers, using triggers or
    other database-provided versioning features, or via an optional
    programmatic value, by setting
    `version_id_generator=False`.
    当使用服务器生成的版本标识符时，ORM 将在可用时使用 RETURNING 立即加载新版本值，否则它将发出第二个 SELECT。[¶](#change-ebb167a81b388b8ac090fa33246c48a2)

    参考文献：[＃2793](http://www.sqlalchemy.org/trac/ticket/2793)

-   **[orm] [feature]**The `eager_defaults` flag of
    [`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
    will now allow the newly generated default values to be fetched
    using an inline RETURNING clause, rather than a second SELECT
    statement, for backends that support
    RETURNING.[¶](#change-8ee7cac9783d870a07c279041dd11bc9)

    参考文献：[＃2793](http://www.sqlalchemy.org/trac/ticket/2793)

-   **[orm] [feature]**为[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")添加了一个新属性[`Session.info`](orm_session_api.html#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")；这是一个字典，应用程序可以存储本地到[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的任意数据。The
    contents of [`Session.info`{](orm_session_api.html#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")
    can be also be initialized using the `info`
    argument of [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    or [`sessionmaker`](orm_session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker").[¶](#change-03c6ce5802904e9ebc488ea78ab24b78)

-   **[orm]
    [feature]**现在实现了删除事件侦听器。该功能通过[`event.remove()`](core_event.html#sqlalchemy.event.remove "sqlalchemy.event.remove")函数提供。

    也可以看看

    [Event Removal API](migration_09.html#feature-2268)

    [¶](#change-3fab266a28f41e49452166ecc367921d)

    参考文献：[＃2268](http://www.sqlalchemy.org/trac/ticket/2268)

-   **[orm] [feature]**属性事件通过`AttributeImpl`作为“启动器”标记传递的机制已更改；该对象现在是一个名为[`attributes.Event`](orm_internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")的特定于事件的对象。此外，属性系统不再基于匹配的“启动器”令牌停止事件；这个逻辑已经被移动到特定于 ORM
    backref 事件处理程序，这是一个属性事件重新传播到随后的 append / set /
    remove 操作的典型源。如果方案不使用 backref 处理程序，那么模拟 backrefs 行为的最终用户代码现在必须确保递归事件传播方案被暂停。使用这个新系统，当一个对象被追加到一个集合上时，backref 处理程序现在可以执行“双跳”操作，与一个新的多对一关联，与之前的多对一关联，然后从以前的集合中删除。在此更改之前，不会发生从上一个集合中删除的最后一步。

    也可以看看

    [Backref handlers can now propagate more than one level
    deep](migration_09.html#migration-2789)

    [¶](#change-0dc7109a8a2359edd8e21d7ed70a1462)

    参考文献：[＃2789](http://www.sqlalchemy.org/trac/ticket/2789)

-   **[orm] [feature]**A major change regarding how the ORM constructs
    joins where the right side is itself a join or left outer join. The
    ORM is now configured to allow simple nesting of joins of the form
    `a JOIN (b JOIN c ON b.id=c.id) ON a.id=b.id`,
    rather than forcing the right side into a `SELECT` subquery.
    这应该允许大多数后端显着提高性能，特别是 MySQL。多年来一直存在这种变化的数据库后端 SQLite 现在通过将`SELECT`子查询的生成从 ORM 移动到 SQL 编译器来解决；所以 SQLite 上的右嵌套连接最终仍然会以`SELECT`呈现，而所有其他后端不再受此替代方法的影响。

    作为这种改变的一部分，已经在[`orm.aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")，[`Join.alias()`](core_selectable.html#sqlalchemy.sql.expression.Join.alias "sqlalchemy.sql.expression.Join.alias")中添加了一个新的参数`flat=True`和[`orm.with_polymorphic()`](orm_inheritance.html#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")函数，该函数允许生成一个 JOIN 的“别名”，它将匿名别名应用于连接中的每个组件表，而不是生成子查询。

    也可以看看

    [Many JOIN and LEFT OUTER JOIN expressions will no longer be wrapped
    in (SELECT \* FROM ..) AS
    ANON\_1](migration_09.html#feature-joins-09)中

    [¶](#change-0a9cba0c775121ff87389c9d5a411292)

    参考文献：[＃2587](http://www.sqlalchemy.org/trac/ticket/2587)

-   **[orm] [bug]**Fixed bug where using an annotation such as
    [`remote()`](orm_relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")
    or [`foreign()`](orm_relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")
    on a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    before association with a parent [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    could produce issues related to the parent table not rendering
    within joins, due to the inherent copy operation performed by an
    annotation.[¶](#change-a0c2b843b3a7a6f41d90792cf10e7e3d)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2813](http://www.sqlalchemy.org/trac/ticket/2813)

-   **[orm] [bug]**Fixed bug where [`Query.exists()`](orm_query.html#sqlalchemy.orm.query.Query.exists "sqlalchemy.orm.query.Query.exists")
    failed to work correctly without any WHERE criterion.
    礼貌弗拉基米尔 Magamedov。[¶](#change-ef9f61eaff6e736d97c7a7096da10f37)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2818](http://www.sqlalchemy.org/trac/ticket/2818)

-   **[orm] [bug]**Fixed a potential issue in an ordered sequence
    implementation used by the ORM to iterate mapper hierarchies; under
    the Jython interpreter this implementation wasn’t ordered, even
    though cPython and Pypy maintained
    ordering.[¶](#change-4315e5745177d007461f7bc0247cbb12)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2794](http://www.sqlalchemy.org/trac/ticket/2794)

-   **[orm] [bug]**Fixed bug in ORM-level event registration where the
    “raw” or “propagate” flags could potentially be mis-configured in
    some “unmapped base class”
    configurations.[¶](#change-e0cad55b3c8cd8dfb6d0ee70f9dfe7d0)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2786](http://www.sqlalchemy.org/trac/ticket/2786)

-   **[orm] [bug]**性能修正与加载映射实体时使用[`defer()`](orm_loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")选项有关。在加载时将每个对象的延迟可调用应用于实例的函数开销显着高于仅从该行加载数据的开销（请注意，`defer()`旨在减少 DB
    /网络开销，不一定函数调用计数）；在所有情况下，函数调用开销都小于从列中加载数据的开销。每个负载创建的“惰性可调用”对象的数量也从 N（结果中的总延迟值）减少到 1（延迟列的总数）。[¶](#change-e1a708dde5288510230755ac690de45b)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2778](http://www.sqlalchemy.org/trac/ticket/2778)

-   **[orm] [bug]**Fixed bug whereby attribute history functions would
    fail when an object we moved from “persistent” to “pending” using
    the [`make_transient()`](orm_session_api.html#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")
    function, for operations involving collection-based
    backrefs.[¶](#change-8a5cddc8cb97dec46f5e9e5bf4c4d922)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2773](http://www.sqlalchemy.org/trac/ticket/2773)

-   **[orm]
    [bug]**尝试刷新继承类的对象时发出一个警告，其中多态鉴别符已被分配给该类无效的值[¶
    T2\>](#change-dd4b79b5d51e7c3f475fb2adec886c01)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2750](http://www.sqlalchemy.org/trac/ticket/2750)

-   **[orm] [bug]**Fixed bug in polymorphic SQL generation where
    multiple joined-inheritance entities against the same base class
    joined to each other as well would not track columns on the base
    table independently of each other if the string of joins were more
    than two entities long.[¶](#change-d8b5c05c64292219e59d34a4d1d9edfe)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2759](http://www.sqlalchemy.org/trac/ticket/2759)

-   **[orm] [bug]**Fixed bug where sending a composite attribute into
    [`Query.order_by()`](orm_query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")
    would produce a parenthesized expression not accepted by some
    databases.[¶](#change-0df6c969856f2e6e6ddbed5c093b58f7)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2754](http://www.sqlalchemy.org/trac/ticket/2754)

-   **[orm] [bug]**修复了复合属性与[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")函数之间的交互。以前，当应用别名时，组合属性在比较操作中无法正确工作。[¶](#change-62648da125cd1e7e856bccba57c1c4b9)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2755](http://www.sqlalchemy.org/trac/ticket/2755)

-   **[orm] [bug] [ext]**Fixed bug where [`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    didn’t report a change event when `clear()` was
    called.[¶](#change-c6ec101b2fa17b87ed51b2bcc64f1785)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2730](http://www.sqlalchemy.org/trac/ticket/2730)

-   **[orm] [bug]**Fixed bug where list instrumentation would fail to
    represent a setslice of `[0:0]` correctly, which
    in particular could occur when using `insert(0, item)` with the association proxy.
    由于 Python 集合中的一些怪癖，使用 Python
    3 而不是 2 的可能性更大。[¶](#change-e7e01f7d15796a940fa6608c2a24096c)

    This change is also **backported** to: 0.8.3, 0.7.11

    参考文献：[＃2807](http://www.sqlalchemy.org/trac/ticket/2807)

-   **[orm] [bug]**[`attributes.get_history()`](orm_session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")
    when used with a scalar column-mapped attribute will now honor the
    “passive” flag passed to it; as this defaults to
    `PASSIVE_OFF`, the function will by default
    query the database if the value is not present.
    这是一个行为变化与 0.8。

    也可以看看

    [attributes.get\_history() will query from the DB by default if
    value not present](migration_09.html#change-2787)

    [¶](#change-57cba062cac3ea3d4b9c20737f356339)

    参考文献：[＃2787](http://www.sqlalchemy.org/trac/ticket/2787)

-   **[orm] [bug] [associationproxy]**Added additional criterion to the
    ==, != comparators, used with scalar values, for comparisons to None
    to also take into account the association record itself being
    non-present, in addition to the existing test for the scalar
    endpoint on the association record being NULL. Previously, comparing
    `Cls.scalar == None` would return records for
    which `Cls.associated` were present and
    `Cls.associated.scalar` is None, but not rows
    for which `Cls.associated` is non-present. More
    significantly, the inverse operation `Cls.scalar != None` *would* return `Cls` rows for which
    `Cls.associated` was non-present.

    对`Cls.scalar ！= 'somevalue'`的情况也进行了修改，使其更像是直接的 SQL 比较；只有存在`Cls.associated`的行以及`Associated.scalar`不为 NULL，并且不等于`'somevalue'`。以前，这将是一个简单的`NOT EXISTS`。

    Also added a special use case where you can call
    `Cls.scalar.has()` with no arguments, when
    `Cls.scalar` is a column-based value - this
    returns whether or not `Cls.associated` has any
    rows present, regardless of whether or not
    `Cls.associated.scalar` is NULL or not.

    也可以看看

    [Association Proxy SQL Expression Improvements and
    Fixes](migration_09.html#migration-2751)

    [¶](#change-077302a77471edd431eee122414f0ff1)

    参考文献：[＃2751](http://www.sqlalchemy.org/trac/ticket/2751)

-   **[orm] [bug]**Fixed an obscure bug where the wrong results would be
    fetched when joining/joinedloading across a many-to-many
    relationship to a single-table-inheriting subclass with a specific
    discriminator value, due to “secondary” rows that would come back.
    现在，“辅助”表和右侧表在内部加入了多对多关系的所有 ORM 连接的括号内，以便可以精确地过滤左右连接。最终通过[＃2587](http://www.sqlalchemy.org/trac/ticket/2587)中概述的右嵌套连接解决了这个问题，从而实现了这一改变。

    也可以看看

    [Many JOIN and LEFT OUTER JOIN expressions will no longer be wrapped
    in (SELECT \* FROM ..) AS
    ANON\_1](migration_09.html#feature-joins-09)中

    [¶](#change-04b284e1a49effb2ce153e574641dfb0)

    参考文献：[＃2369](http://www.sqlalchemy.org/trac/ticket/2369)

-   **[orm] [bug]** [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")方法的“自动别名”行为已被关闭。具体行为现在可以通过一个新方法[`Query.select_entity_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_entity_from "sqlalchemy.orm.query.Query.select_entity_from")获得。这里的自动别名行为从来没有很好的文档记录，并且通常不是我们所期望的，因为[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")已经变得更加倾向于控制 JOIN 的呈现方式。[`Query.select_entity_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_entity_from "sqlalchemy.orm.query.Query.select_entity_from")也将在 0.8 中可用，以便依赖于自动别名的应用程序可以将其应用程序移至使用此方法。

    也可以看看

    [Query.select\_from() no longer applies the clause to corresponding
    entities](migration_09.html#migration-2736)

    [¶](#change-6856f4c9574c2e7f8cae541a3af37c17)

    参考文献：[＃2736](http://www.sqlalchemy.org/trac/ticket/2736)

### orm declarative [¶](#change-0.9.0b1-orm-declarative "Permalink to this headline")

-   **[feature] [orm]
    [declarative]**添加了一个便捷类装饰器[`as_declarative()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.as_declarative "sqlalchemy.ext.declarative.as_declarative")，是[`declarative_base()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")基类用于使用漂亮的类装饰方法来应用。[¶](#change-928ad6a6f0e7bf2d61add68c58d2693a)

    This change is also **backported** to: 0.8.3

-   **[feature] [orm] [declarative]**ORM descriptors such as hybrid
    properties can now be referenced by name in a string argument used
    with `order_by`, `primaryjoin`, or similar in [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
    in addition to column-bound
    attributes.[¶](#change-fa2beb10ebb49a0f8c15349cf5a7ca72)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2761](http://www.sqlalchemy.org/trac/ticket/2761)

### 发动机[¶ T0\>](#change-0.9.0b1-engine "Permalink to this headline")

-   **[engine] [feature]**`repr()` for the
    [`URL`](core_engines.html#sqlalchemy.engine.url.URL "sqlalchemy.engine.url.URL")
    of an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    will now conceal the password using asterisks. Courtesy
    GunnlaugurÞórBriem。[¶](#change-e265af1f13013b87ee5cfd3dc4348c0f)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2821](http://www.sqlalchemy.org/trac/ticket/2821)

-   **[engine] [feature]**添加到[`ConnectionEvents`](core_events.html#sqlalchemy.events.ConnectionEvents "sqlalchemy.events.ConnectionEvents")的新事件：

    -   [`ConnectionEvents.engine_connect()`](core_events.html#sqlalchemy.events.ConnectionEvents.engine_connect "sqlalchemy.events.ConnectionEvents.engine_connect")
    -   [`ConnectionEvents.set_connection_execution_options()`](core_events.html#sqlalchemy.events.ConnectionEvents.set_connection_execution_options "sqlalchemy.events.ConnectionEvents.set_connection_execution_options")
    -   [`ConnectionEvents.set_engine_execution_options()`](core_events.html#sqlalchemy.events.ConnectionEvents.set_engine_execution_options "sqlalchemy.events.ConnectionEvents.set_engine_execution_options")

    [¶](#change-d27b9f0357f06e9cf95fd1246c8052ae)

    参考文献：[＃2770](http://www.sqlalchemy.org/trac/ticket/2770)

-   **[engine] [bug] [oracle]**Dialect.initialize() is not called a
    second time if an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    is recreated, due to a disconnect error. 这解决了 Oracle
    8 方言中的一个特定问题，但通常 dialect.initialize()阶段应该只能用于每种方言一次。[¶](#change-3d8267e6caa813efc145b77d062c77ad)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2776](http://www.sqlalchemy.org/trac/ticket/2776)

-   **[engine] [bug] [pool]**Fixed bug where [`QueuePool`](core_pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
    would lose the correct checked out count if an existing pooled
    connection failed to reconnect after an invalidate or recycle
    event.[¶](#change-155adccbc41937b6cb1bc83c19fd47ef)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2772](http://www.sqlalchemy.org/trac/ticket/2772)

-   **[engine] [bug]**Fixed bug where the `reset_on_return` argument to various [`Pool`](core_pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
    implementations would not be propagated when the pool was
    regenerated. Courtesy
    Eevee。[¶](#change-e8091dd32fb1ad01f0003ca4b9687bf5)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[请求 github：6](https://github.com/zzzeek/sqlalchemy/pull/6)

-   **[engine] [bug]**The regexp used by the [`make_url()`](core_engines.html#sqlalchemy.engine.url.make_url "sqlalchemy.engine.url.make_url")
    function now parses ipv6 addresses, e.g. surrounded by
    brackets.[¶](#change-eb0b93a1244b5f1389a13544c801b4cf)

    This change is also **backported** to: 0.8.3, 0.7.11

    参考文献：[＃2851](http://www.sqlalchemy.org/trac/ticket/2851)

-   **[engine] [bug]**The method signature of
    [`Dialect.reflecttable()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.reflecttable "sqlalchemy.engine.interfaces.Dialect.reflecttable"),
    which in all known cases is provided by [`DefaultDialect`](core_internals.html#sqlalchemy.engine.default.DefaultDialect "sqlalchemy.engine.default.DefaultDialect"),
    has been tightened to expect `include_columns`
    and `exclude_columns` arguments without any kw
    option, reducing ambiguity - previously `exclude_columns` was missing.[¶](#change-8fe08fa349b1117af24feae4b1a76bc5)

    参考文献：[＃2748](http://www.sqlalchemy.org/trac/ticket/2748)

### SQL [¶ T0\>](#change-0.9.0b1-sql "Permalink to this headline")

-   **[sql] [feature]**通过[`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")方法增加了对“唯一约束”反射的支持。感谢 Roman
    Podolyaka 的补丁。[¶](#change-e911a8b7deaa9ca6726dfc5d21dfd76d)

    这个改变也被**backported**修改为：0.8.4

    参考文献：[＃1443](http://www.sqlalchemy.org/trac/ticket/1443)

-   **[sql] [feature]**The [`update()`](core_dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update"),
    [`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert"),
    and [`delete()`](core_dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")
    constructs will now interpret ORM entities as target tables to be
    operated upon, e.g.:

        from sqlalchemy import insert, update, deleteplain

        ins = insert(SomeMappedClass).values(x=5)

        del_ = delete(SomeMappedClass).where(SomeMappedClass.id == 5)

        upd = update(SomeMappedClass).where(SomeMappedClass.id == 5).values(name='ed')

    [¶](#change-93cc634b6be87be3a5f50c6295f3ece2)

    This change is also **backported** to: 0.8.3

-   **[sql] [feature] [postgresql] [mysql]**The Postgresql and MySQL
    dialects now support reflection/inspection of foreign key options,
    including ON UPDATE, ON DELETE.
    Postgresql 也反映了 MATCH，DEFERRABLE 和 INITIALLY。Coutesy
    ijl。[¶](#change-8eb029cbdea1c892a1ad62622f54cdba)

    参考文献：[＃2183](http://www.sqlalchemy.org/trac/ticket/2183)

-   **[sql]
    [feature]**现在，在类型化表达式中使用带有“null”类型（例如，没有指定类型）的[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")副本分配了比较列的实际类型。以前，这个逻辑会在给定的[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")上发生。Additionally,
    a similar process now occurs for [`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
    constructs passed to [`ValuesBase.values()`](core_dml.html#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")
    for an [`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
    or [`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")
    construct, within the compilation phase of the construct.

    这些都是微妙的行为变化，可能会影响某些用途。

    也可以看看

    [A bindparam() construct with no type gets upgraded via copy when a
    type is available](migration_09.html#migration-2850)

    [¶](#change-d24a04a8befc766ba1bf79f8656487a5)

    参考文献：[＃2850](http://www.sqlalchemy.org/trac/ticket/2850)

-   **[sql] [feature]**An overhaul of expression handling for special
    symbols particularly with conjunctions, e.g. `None` [`expression.null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")
    [`expression.true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
    [`expression.false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false"),
    including consistency in rendering NULL in conjunctions,
    “short-circuiting” of [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
    and [`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")
    expressions which contain boolean constants, and rendering of
    boolean constants and expressions as compared to “1” or “0” for
    backends that don’t feature `true`/`false` constants.

    也可以看看

    [Improved rendering of Boolean constants, NULL constants,
    conjunctions](migration_09.html#migration-2804)的渲染

    [¶](#change-39321a75ce7fa62c42a70b5096452d0e)

    References: [\#2734](http://www.sqlalchemy.org/trac/ticket/2734),
    [\#2804](http://www.sqlalchemy.org/trac/ticket/2804),
    [\#2823](http://www.sqlalchemy.org/trac/ticket/2823)

-   **[sql]
    [feature]**打字系统现在处理渲染“文字束缚”值的任务，例如，值通常是绑定参数，但由于上下文必须呈现为字符串，通常位于 DDL 结构中，例如 CHECK 约束和索引（请注意，DDL 从[＃2742](http://www.sqlalchemy.org/trac/ticket/2742)使用“文字绑定”值）
    。一个新的方法[`TypeEngine.literal_processor()`](core_type_api.html#sqlalchemy.types.TypeEngine.literal_processor "sqlalchemy.types.TypeEngine.literal_processor")作为基础，并且添加[`TypeDecorator.process_literal_param()`](core_custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")以允许包装本地文字渲染方法。

    也可以看看

    [The typing system now handles the task of rendering “literal bind”
    values](migration_09.html#change-2838)

    [¶](#change-272e70220cd05bb94293b58f14259825)

    参考文献：[＃2838](http://www.sqlalchemy.org/trac/ticket/2838)

-   **[sql] [feature]**The [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    method now produces copies of all [`SchemaItem.info`](core_metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
    dictionaries from all [`SchemaItem`](core_metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")
    objects within the structure including columns, constraints, foreign
    keys, etc.
    由于这些字典是副本，因此它们与原始字典无关。在此之前，只有[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的`.info`字典在此操作中传输，并且仅在适当的位置连接，而不是复制。[¶](#change-98eded5d80636b193ea09e3c9865f4a1)

    参考文献：[＃2716](http://www.sqlalchemy.org/trac/ticket/2716)

-   **[sql] [feature]**The `default` argument of
    [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    now accepts a class or object method as an argument, in addition to
    a standalone function; will properly detect if the “context”
    argument is accepted or
    not.[¶](#change-2f3ab8473c252112e2ebb16aa940261f)

-   **[sql] [feature]**为[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")结构[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")添加了新方法。Given
    a list of columns and a selectable, renders
    `INSERT INTO (table) (columns) SELECT ..`.
    虽然此功能在 0.9 中突出显示，但它也被反向移植到了 0.8.3。

    也可以看看

    [INSERT from SELECT](migration_09.html#feature-722)

    [¶](#change-13e79ff2064616ed83c6e394ab472ee5)

    参考文献：[＃722](http://www.sqlalchemy.org/trac/ticket/722)

-   **[sql] [feature]**为[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")提供了一个名为[`TypeDecorator.coerce_to_is_types`](core_custom_types.html#sqlalchemy.types.TypeDecorator.coerce_to_is_types "sqlalchemy.types.TypeDecorator.coerce_to_is_types")的新属性，以便更容易控制如何使用`==`或`!=` to `None`和布尔类型用于生成`IS`表达式，参数。[¶
    T16\>](#change-3300a90d71384cf7c366f03b14fa1351)

    参考文献：[＃2734](http://www.sqlalchemy.org/trac/ticket/2734)，[＃2744](http://www.sqlalchemy.org/trac/ticket/2744)

-   **[sql] [feature]**A [`label()`](core_sqlelement.html#sqlalchemy.sql.expression.label "sqlalchemy.sql.expression.label")
    construct will now render as its name alone in an
    `ORDER BY` clause, if that label is also
    referred to in the columns clause of the select, instead of
    rewriting the full expression.
    这使数据库有更好的机会在两种不同的情况下优化相同表达式的评估。

    也可以看看

    [Label constructs can now render as their name alone in an ORDER
    BY](migration_09.html#migration-1068)中单独呈现其名称

    [¶](#change-e50ad7b22d3a616aeb47cf832c27097a)

    参考文献：[＃1068](http://www.sqlalchemy.org/trac/ticket/1068)

-   **[sql] [bug]**Fixed bug where [`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")
    would not interpret ORM elements with a
    `__clause_element__()` method
    properly.[¶](#change-4a3641b48480cf313538449a8e5b1c5f)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2849](http://www.sqlalchemy.org/trac/ticket/2849)

-   **[sql] [bug]**The [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    and [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    types now bypass any custom (e.g. TypeDecorator) type in use when
    producing the CHECK constraint for the “non native” type.
    这样自定义类型不会被包含在 CHECK 中的表达式中，因为这个表达式违背了“impl”值而不是“装饰”值。[¶](#change-a5059e2a0d6f7ae306b16d71a6884f3f)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2842](http://www.sqlalchemy.org/trac/ticket/2842)

-   **[sql] [bug]**The `.unique` flag on
    [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    could be produced as `None` if it was generated
    from a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    that didn’t specify `unique` (where it defaults
    to `None`). 该标志现在总是`True`或`False`。[¶](#change-2d486e59e387ed6c8d50bf5d99627cdf)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2825](http://www.sqlalchemy.org/trac/ticket/2825)

-   **[sql] [bug]**Fixed bug in default compiler plus those of
    postgresql, mysql, and mssql to ensure that any literal SQL
    expression values are rendered directly as literals, instead of as
    bound parameters, within a CREATE INDEX statement.
    这也改变了其他 DDL 的渲染方案，如约束。[¶](#change-6f6cd0ca9e6e5050ad6d52b884122ea9)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2742](http://www.sqlalchemy.org/trac/ticket/2742)

-   **[sql] [bug]**A [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    that is made to refer to itself in its FROM clause, typically via
    in-place mutation, will raise an informative error message rather
    than causing a recursion
    overflow.[¶](#change-0e498b684ea9cbcfc3f277d61204d65b)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2815](http://www.sqlalchemy.org/trac/ticket/2815)

-   **[sql] [bug]**Fixed bug where using the `column_reflect` event to change the `.key` of the
    incoming [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    would prevent primary key constraints, indexes, and foreign key
    constraints from being correctly
    reflected.[¶](#change-6e1a5094981c35f027081bae82ca704a)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2811](http://www.sqlalchemy.org/trac/ticket/2811)

-   **[sql] [bug]**The [`ColumnOperators.notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
    operator added in 0.8 now properly produces the negation of the
    expression “IN” returns when used against an empty
    collection.[¶](#change-d12e927d520f09485a8678152c280b4e)

    This change is also **backported** to: 0.8.3

-   **[sql] [bug] [postgresql]**Fixed bug where the expression system
    relied upon the `str()` form of a some
    expressions when referring to the `.c`
    collection on a `select()` construct, but the
    `str()` form isn’t available since the element
    relies on dialect-specific compilation constructs, notably the
    `__getitem__()` operator as used with a
    Postgresql `ARRAY` element.
    该修补程序还添加了一个新的异常类[`UnsupportedCompilationError`](core_exceptions.html#sqlalchemy.exc.UnsupportedCompilationError "sqlalchemy.exc.UnsupportedCompilationError")，这是在编译器被要求编译一些不知道如何去做的情况下引发的。[¶](#change-2c8dbe177a3c8cba08249e3cdeca2362)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2780](http://www.sqlalchemy.org/trac/ticket/2780)

-   **[sql] [bug]**对于[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")结构的相关行为的多个修复，在 0.8.0 中首次引入：

    -   为了满足这样的用例，其中 FROM 条目应该向外关联到一个包含另一个的 SELECT，然后包含这个 SELECT，当通过[`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")建立显式相关性时，前提是目标选择位于 WHERE
        / ORDER BY /
        columns 子句所包含的链中，而不仅仅是嵌套的 FROM 子句。This makes
        [`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")
        act more compatibly to that of 0.7 again while still maintaining
        the new “smart” correlation.
    -   当不使用显式关联时，通常的“隐式”关联将其行为限制为立即封闭的 SELECT，以最大化与 0.7 应用程序的兼容性，并且还防止在这种情况下嵌套 FROM 之间的相关性，保持与 0.8.0
        / 0.8 的兼容性。 1。
    -   [`Select.correlate_except()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")方法在所有情况下都不会阻止给定的 FROM 子句相关，并且也会导致 FROM 子句完全被错误地省略（更像 0.7 会做的），这已经固定。
    -   调用 select.correlate\_except（None）将按照预期将所有 FROM 子句输入到相关中。

    [¶](#change-ec66deaad21dd8b26baa4f0b315154b4)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2668](http://www.sqlalchemy.org/trac/ticket/2668)，[＃2746](http://www.sqlalchemy.org/trac/ticket/2746)

-   **[sql] [bug]**Fixed bug whereby joining a select() of a table “A”
    with multiple foreign key paths to a table “B”, to that table “B”,
    would fail to produce the “ambiguous join condition” error that
    would be reported if you join table “A” directly to “B”; it would
    instead produce a join condition with multiple
    criteria.[¶](#change-69bb8fab2a49ae9f49bba3d45913e256)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2738](http://www.sqlalchemy.org/trac/ticket/2738)

-   **[sql] [bug] [reflection]**Fixed bug whereby using
    [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
    across a remote schema as well as a local schema could produce wrong
    results in the case where both schemas had a table of the same
    name.[¶](#change-875b41219bbc43340ccf3d1e7d1f5fbf)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2728](http://www.sqlalchemy.org/trac/ticket/2728)

-   **[sql] [bug]**删除了来自基类[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")类的“未实现”`__iter__()`调用，而这是在 0.8 中引入的。
    0，以防止在自定义运算符上实现`__getitem__()`方法，然后在该对象上错误地调用`list()`时出现无限的内存增长循环，导致列元素报告它们实际上是可迭代类型，当您尝试迭代时会抛出错误。没有真正的方式让双方都在这里，所以我们坚持使用 Python 的最佳实践。仔细在自定义运算符上实现`__getitem__()`！[¶](#change-413cb4c102d2705b115721cf5917ed43)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2726](http://www.sqlalchemy.org/trac/ticket/2726)

-   **[sql]
    [bug]**固定回归到 0.7.9，如果 CTE 的名称在多个 FROM 子句中被引用，那么它的名称可能不会被正确引用。[¶](#change-97b9ec01528f6ce1a103f8b8800d8b35)

    This change is also **backported** to: 0.8.3, 0.7.11

    参考文献：[＃2801](http://www.sqlalchemy.org/trac/ticket/2801)

-   **[sql] [bug] [cte]**Fixed bug in common table expression system
    where if the CTE were used only as an `alias()`
    construct, it would not render using the WITH
    keyword.[¶](#change-0b6b7933cd03daaa51c88661f6a18a77)

    This change is also **backported** to: 0.8.3, 0.7.11

    参考文献：[＃2783](http://www.sqlalchemy.org/trac/ticket/2783)

-   **[sql] [bug]**Fixed bug in [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    DDL where the “quote” flag from a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object would not be
    propagated.[¶](#change-ee864489da68afbc90051f4bb9d0f94c)

    This change is also **backported** to: 0.8.3, 0.7.11

    参考文献：[＃2784](http://www.sqlalchemy.org/trac/ticket/2784)

-   **[sql] [bug]**在调用“attach”事件之前，“name”属性在[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")上设置，以便可以使用附件事件动态生成名称用于基于父表和/或列的索引。[¶](#change-68ca19e2d66effbff44cb5a9c9633d5f)

    参考文献：[＃2835](http://www.sqlalchemy.org/trac/ticket/2835)

-   **[sql] [bug]**错误的 kw arg“schema”已从[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象中删除。这是一个无所作为的偶然犯罪；当使用这个 kw
    arg 时，在 0.8.3 中发出警告。[¶](#change-f9093cc2030bb467e2b99b6844eee451)

    参考文献：[＃2831](http://www.sqlalchemy.org/trac/ticket/2831)

-   **[sql]
    [bug]**对“引用”标识符的处理方式进行了重新修改，而不是依赖传递的各种`quote=True`标志，这些标志被转换为丰富的字符串对象，其中包含引用信息，这些信息被传递到通用模式结构（如[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")等）。这解决了各种方法的问题，这些方法没有正确地遵守“quote”标志，例如[`Engine.has_table()`](core_connections.html#sqlalchemy.engine.Engine.has_table "sqlalchemy.engine.Engine.has_table")和相关方法。[`quoted_name`](core_sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")对象是一个字符串子类，如果需要也可以明确使用；该对象将保持传递的引用偏好，并且还将绕过由大写符号标准化的方言（如 Oracle，Firebird 和 DB2）执行的“名称规范化”。结果是，“大写”后端现在可以使用强制引用的名称，如小写引用的名称和新的保留字。

    也可以看看

    [Schema identifiers now carry along their own quoting
    information](migration_09.html#change-2812)

    [¶](#change-80f90191c40a63606c13f48bd62758c9)

    参考文献：[＃2812](http://www.sqlalchemy.org/trac/ticket/2812)

-   **[sql] [bug]**根据时刻，将[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象解析为其目标[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")即目标[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")与[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")相同的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")关联，而不是等待第一次构建连接或类似。这与其他改进一起允许更早地检测一些外键配置问题。此处还包括类型传播系统的返工，因此现在应该可靠地将类型设置为`None`在任何[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")上引用另一个[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    - 一旦与其他列关联，该类型将从目标列中复制，现在也适用于组合外键。

    也可以看看

    [Columns can reliably get their type from a column referred to via
    ForeignKey](migration_09.html#migration-1765)引用的列中获取它们的类型

    [¶](#change-6116437230b6aca55206409a957f932e)

    参考文献：[＃1765](http://www.sqlalchemy.org/trac/ticket/1765)

### 的 PostgreSQL [¶ T0\>](#change-0.9.0b1-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**已添加对 Postgresql
    9.2 范围类型的支持。目前，没有提供类型转换，因此目前可以直接使用字符串或 psycopg2
    2.5 范围扩展类型。补丁礼貌 Chris
    Withers。[¶](#change-d1e23a832aab5d9d980590ac352028c9)

    这个改变也被**backported**修改为：0.8.2

-   **[postgresql] [feature]**在使用 psycopg2
    DBAPI 时增加了对“AUTOCOMMIT”隔离的支持。该关键字可通过`isolation_level`执行选项使用。Pope 礼貌 Roman
    Podolyaka。[¶](#change-0c25a8156ec52fca32278f7939a5ec93)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2072](http://www.sqlalchemy.org/trac/ticket/2072)

-   **[postgresql] [feature]**Added support for rendering
    `SMALLSERIAL` when a [`SmallInteger`](core_type_basics.html#sqlalchemy.types.SmallInteger "sqlalchemy.types.SmallInteger")
    type is used on a primary key autoincrement column, based on server
    version detection of Postgresql version 9.2 or
    greater.[¶](#change-e0e1515141ca0c31a3932b72465f0701)

    参考文献：[＃2840](http://www.sqlalchemy.org/trac/ticket/2840)

-   **[postgresql]
    [bug]**从列的服务器默认值的反射中删除了 128 个字符的截断；此代码原始来自 PG 系统视图，它为了可读性而截断了字符串。[¶](#change-c7b42a13889c2700394a72cd53fdf578)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2844](http://www.sqlalchemy.org/trac/ticket/2844)

-   **[postgresql] [bug]**括号将应用于复合 SQL 表达式，并在 CREATE
    INDEX 语句的列表中呈现。[¶](#change-90c077a62f3393fc602fa4e68ef713bd)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2742](http://www.sqlalchemy.org/trac/ticket/2742)

-   **[postgresql]
    [bug]**修复了 Postgresql 版本字符串在前缀“Postgresql”或“EnterpriseDB”之前的前缀不会被解析的错误。Courtesy
    Scott Schaefer。[¶](#change-7a2ed752121c34c9b56e49bf4745e646)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2819](http://www.sqlalchemy.org/trac/ticket/2819)

-   **[postgresql] [bug]**The behavior of [`extract()`](core_sqlelement.html#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")
    has been simplified on the Postgresql dialect to no longer inject a
    hardcoded `::timestamp` or similar cast into the
    given expression, as this interfered with types such as
    timezone-aware datetimes, but also does not appear to be at all
    necessary with modern versions of
    psycopg2.[¶](#change-bf3ab2871c03846506f101f9e3b03dca)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2740](http://www.sqlalchemy.org/trac/ticket/2740)

-   **[postgresql] [bug]**Fixed bug in HSTORE type where keys/values
    that contained backslashed quotes would not be escaped correctly
    when using the “non native” (i.e. non-psycopg2) means of translating
    HSTORE data. 补丁由 Ryan
    Kelly 提供。[¶](#change-a284671030fa2fb228bace39dcecba09)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2766](http://www.sqlalchemy.org/trac/ticket/2766)

-   **[postgresql]
    [bug]**修复了多列 Postgresql 索引中的列顺序将以错误顺序反映的错误。Courtesy
    Roman Podolyaka。[¶](#change-fd3a75fa26f5e1303ec1daf1ede035e9)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2767](http://www.sqlalchemy.org/trac/ticket/2767)

### MySQL 的[¶ T0\>](#change-0.9.0b1-mysql "Permalink to this headline")

-   **[mysql] [feature]**The `mysql_length`
    parameter used with [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    can now be passed as a dictionary of column names/lengths, for use
    with composite indexes. 非常感谢 Roman
    Podolyaka 提供的补丁。[¶](#change-d0a8eb2d08437d50b589f473fab54468)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2704](http://www.sqlalchemy.org/trac/ticket/2704)

-   **[mysql] [feature]**现在，MySQL [`mysql.SET`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET "sqlalchemy.dialects.mysql.SET")类型具有与[`mysql.ENUM`](dialects_mysql.html#sqlalchemy.dialects.mysql.ENUM "sqlalchemy.dialects.mysql.ENUM")相同的自动引用行为。设置值时不需要引号，但是存在的引号将会随警告一起自动检测。这也有助于 Alembic，其中 SET 类型不会用引号渲染。[¶](#change-8d6f26937d8905e155c0deb811a65b8c)

    参考文献：[＃2817](http://www.sqlalchemy.org/trac/ticket/2817)

-   **[mysql] [bug]**The change in
    [\#2721](http://www.sqlalchemy.org/trac/ticket/2721), which is that
    the `deferrable` keyword of
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    is silently ignored on the MySQL backend, will be reverted as of
    0.9; this keyword will now render again, raising errors on MySQL as
    it is not understood - the same behavior will also apply to the
    `initially` keyword.
    在 0.8 中，关键字将保持忽略，但会发出警告。此外，`match`关键字现在会在 0.9 上产生一个[`CompileError`](core_exceptions.html#sqlalchemy.exc.CompileError "sqlalchemy.exc.CompileError")，并在 0.8 上发出警告；这个关键字不仅被 MySQL 默默地忽略，而且打破了 ON
    UPDATE / ON DELETE 选项。

    要使用在 MySQL 上不呈现或呈现不同的[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")，请使用自定义编译选项。这个用法的一个例子已经添加到文档中，请参阅[MySQL
    Foreign Keys](dialects_mysql.html#mysql-foreign-keys)。

    [¶](#change-e43926dc67636d3ba7e0744c194355b2)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2721](http://www.sqlalchemy.org/trac/ticket/2721)，[＃2839](http://www.sqlalchemy.org/trac/ticket/2839)

-   **[mysql] [bug]**MySQL-connector dialect now allows options in the
    create\_engine query string to override those defaults set up in the
    connect, including “buffered” and
    “raise\_on\_warnings”.[¶](#change-2a6ed47e91f911c2105ce955afc32748)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2515](http://www.sqlalchemy.org/trac/ticket/2515)

-   **[mysql] [bug]**Fixed bug when using multi-table UPDATE where a
    supplemental table is a SELECT with its own bound parameters, where
    the positioning of the bound parameters would be reversed versus the
    statement itself when using MySQL’s special
    syntax.[¶](#change-132183eb674d003b5472f2173789f67e)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2768](http://www.sqlalchemy.org/trac/ticket/2768)

-   **[mysql] [bug]**为`mysql+gaerdbms`方言添加了另一个条件，用于检测所谓的“开发”模式，我们应该使用`rdbms_mysqldb`补丁礼貌 Brett
    Slatkin。[¶](#change-b93865e4329f3662cd5b2933bf555218)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2715](http://www.sqlalchemy.org/trac/ticket/2715)

-   **[mysql] [bug]**The `deferrable` keyword
    argument on [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    and [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    will not render the `DEFERRABLE` keyword on the
    MySQL dialect.
    很长一段时间，我们放弃了这一点，因为不可延迟的外键与延迟的外键的行为不同，但有些环境只是禁用 MySQL 上的 FK，所以我们在这里不会引起注意。[t0
    \>](#change-43e1dfe4d4c7f5082a4ca7f2271b21b0)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2721](http://www.sqlalchemy.org/trac/ticket/2721)

-   **[mysql] [bug]**版本 5.5,5.6 的 MySQL 保留字更新，Hanno
    Schlichting 提供。[¶](#change-8770e442e32764b20ee2132358bc9d6d)

    This change is also **backported** to: 0.8.3, 0.7.11

    参考文献：[＃2791](http://www.sqlalchemy.org/trac/ticket/2791)

-   **[mysql]
    [bug]**修复并测试反射中的 MySQL 外键选项的解析；这补充了[＃2183](http://www.sqlalchemy.org/trac/ticket/2183)中的工作，我们开始支持外键选项的反映，例如 ON
    UPDATE / ON DELETE
    cascade。[¶](#change-1fad8db7eac7a5daf1d143084dbc55af)

    参考文献：[＃2839](http://www.sqlalchemy.org/trac/ticket/2839)

-   **[mysql]
    [bug]**改进了对 cymysql 驱动程序的支持，支持版本 0.6.5，礼貌 Hajime
    Nakagami。[¶](#change-e98fa083392ee258da3be2f4cc463340)

### 源码[¶ T0\>](#change-0.9.0b1-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**新添加的 SQLite
    DATETIME 参数 storage\_format 和 regexp 显然没有完全正确地实现；当论据被接受时，实际上它们将不起作用；这已被修复。[¶](#change-e196956853a1c770ffc96aa3ebdb0027)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2781](http://www.sqlalchemy.org/trac/ticket/2781)

-   **[sqlite] [bug]**将[`sqlalchemy.types.BIGINT`](core_type_basics.html#sqlalchemy.types.BIGINT "sqlalchemy.types.BIGINT")添加到可以通过 SQLite 方言反映的类型名称列表；礼貌罗素斯图尔特。[¶](#change-ed8a730c977ad5352148eb228c2b3a31)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2764](http://www.sqlalchemy.org/trac/ticket/2764)

### MSSQL [¶ T0\>](#change-0.9.0b1-mssql "Permalink to this headline")

-   当在 SQL Server
    2000 上查询信息模式时，删除了在 0.8.1 中添加的 CAST 调用，以帮助解决驱动程序问题，这在 2000 年显然不兼容。**[mssql]
    [bug]**CAST 保持适用于 SQL Server
    2005 及更高版本。[¶](#change-02967c3908e9232b5bde5a7b76c9cd7b)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2747](http://www.sqlalchemy.org/trac/ticket/2747)

-   **[mssql] [bug] [pyodbc]**使用 Python 3 +
    pyodbc 修复 MSSQL，包括正确传递语句[¶](#change-bea87c5d2f97257ad289ce3893861719)

    参考文献：[＃2355](http://www.sqlalchemy.org/trac/ticket/2355)

### 预言[¶ T0\>](#change-0.9.0b1-oracle "Permalink to this headline")

-   **[oracle] [feature]
    [py3k]**使用 cx\_oracle 的 Oracle 单元测试现在可以在 Python
    3 下完全传递。[¶](#change-d164453835dc47719c20c02f5a49d116)

-   **[oracle] [bug]**Fixed bug where Oracle table reflection using
    synonyms would fail if the synonym and the table were in different
    remote schemas. 补丁修复 Kyle
    Derr 礼貌。[¶](#change-7db6754b84c59e26d48cb6796899ee20)

    This change is also **backported** to: 0.8.3

    参考文献：[＃2853](http://www.sqlalchemy.org/trac/ticket/2853)

### 火鸟[¶ T0\>](#change-0.9.0b1-firebird "Permalink to this headline")

-   **[firebird]
    [feature]**为 kinterbasdb 和 fdb 方言添加了新的标志`retaining=True`。这将控制发送到 DBAPI 连接的`commit()`和`rollback()`方法的`retaining`标志的值。由于历史原因，该标志在 0.8.2 中默认为`True`，但在 0.9.0b1 中，该标志默认为`False`。[¶](#change-9175f0322dec423ed80f93115ad65aae)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2763](http://www.sqlalchemy.org/trac/ticket/2763)

-   **[firebird] [feature]**The `fdb` dialect is now
    the default dialect when specified without a dialect qualifier, i.e.
    `firebird://`, per the Firebird project
    publishing `fdb` as their official Python
    driver.[¶](#change-76539a1da5603da953dbce6672c8e461)

    参考文献：[＃2504](http://www.sqlalchemy.org/trac/ticket/2504)

-   **[firebird] [bug]**Type lookup when reflecting the Firebird types
    LONG and INT64 has been fixed so that LONG is treated as INTEGER,
    INT64 treated as BIGINT, unless the type has a “precision” in which
    case it’s treated as NUMERIC. Patch courtesy Russell
    Stuart。[¶](#change-11863f3c419f255126f23bd31f39c054)

    这个改变也被**backported**修改为：0.8.2

    参考文献：[＃2757](http://www.sqlalchemy.org/trac/ticket/2757)

### 杂项[¶ T0\>](#change-0.9.0b1-misc "Permalink to this headline")

-   **[feature]**将`system=True`添加到[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")中，将列标记为系统自动创建的列数据库（例如 Postgresql
    `oid`或`xmin`）。该列将从`CREATE TABLE`语句中省略，但否则可用于查询。另外，通过生成返回`None`的规则，可以将[`CreateColumn`](core_ddl.html#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")结构应用于允许跳过列的自定义编译规则。[¶](#change-4376b4db83754e008ed7559a50c2b16c)

    This change is also **backported** to: 0.8.3

-   **[feature]
    [examples]**改进了`examples/generic_associations`中的示例，包括`discriminator_on_association.py`利用单个表继承进行工作“鉴别者”。还添加了一个真正的“通用外键”示例，该示例与其他流行框架的工作方式类似，因为它使用开放式整数指向任何其他表，前面提到了传统的参照完整性。虽然我们不推荐这种模式，但信息要免费。[¶](#change-d810542c0eef5129e99e0dea72af3bb9)

    This change is also **backported** to: 0.8.3

-   **[feature] [core]**为[`UpdateBase.returning()`](core_dml.html#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")添加了一个名为[`ValuesBase.return_defaults()`](core_dml.html#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")的新变体。这允许将任意列添加到语句的 RETURNING 子句中，而不会干扰编译器通常的“隐式返回”功能，该功能用于有效提取新生成的主键值。为支持后端，所有获取值的字典存在于[`ResultProxy.returned_defaults`](core_connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")。[¶](#change-c6ae54dff0bc9fddf9cbe1f7a37fcd59)

    参考文献：[＃2793](http://www.sqlalchemy.org/trac/ticket/2793)

-   **[feature]
    [pool]**添加了“rollback-on-return”的池日志记录和较少使用的“commit-on-return”。这是使用其余池“调试”日志记录启用的。[¶](#change-026a7898970464580f20e377c6428616)

    参考文献：[＃2752](http://www.sqlalchemy.org/trac/ticket/2752)

-   **[bug]
    [examples]**在版本控制示例中创建的历史记录表中添加了“autoincrement =
    False”，因为该表在任何情况下都不应该有 autoinc，Patrick Schmid 提供[¶
    T2\>](#change-95b0a27ef450ed818ac940e3ded22313)

    This change is also **backported** to: 0.8.3

-   **[bug] [ext]**Fixed bug whereby if a composite type were set up
    with a function instead of a class, the mutable extension would trip
    up when it tried to check that column for being a
    [`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
    (which it isn’t).
    礼貌 asldevi。[¶](#change-de133057736a5ba4eb2f13b2226d6189)

    这个改变也被**backported**修改为：0.8.2

-   **[bug] [examples]**Fixed an issue with the “versioning” recipe
    whereby a many-to-one reference could produce a meaningless version
    for the target, even though it was not changed, when backrefs were
    present. 补丁由 Matt
    Chisholm 提供。[¶](#change-b0dcd18db52ac8a72250f771c09f4c4f)

    这个改变也被**backported**修改为：0.8.2

-   **[requirements]**现在需要 Python
    [mock](https://pypi.python.org/pypi/mock)库来运行单元测试套件。作为 Python
    3.3 的标准库的一部分，以前的 Python 安装将需要安装它，以便运行单元测试或使用外部方言的`sqlalchemy.testing`包。[T2\>](#change-47f2cda56e1d7a6b9dffa4b1b316855a)

    这个改变也被**backported**修改为：0.8.2


