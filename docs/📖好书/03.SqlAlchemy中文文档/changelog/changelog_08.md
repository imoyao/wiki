---
title: changelog_08
date: 2021-02-20 22:41:29
permalink: /sqlalchemy/fd3512/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
0.8更新日志[¶](#changelog "Permalink to this headline")
=======================================================

0.8.7 [¶ T0\>](#change-0.8.7 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014年7月22日

### ORM [¶ T0\>](#change-0.8.7-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug in subquery eager loading where a long
    chain of eager loads across a polymorphic-subclass boundary in
    conjunction with polymorphic loading would fail to locate the
    subclass-link in the chain, erroring out with a missing property
    name on an [`AliasedClass`](orm_query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass").[¶](#change-e10433635e670cc6b02866d5fca31d7f)

    参考文献：[＃3055](http://www.sqlalchemy.org/trac/ticket/3055)

-   **[orm] [bug]**Fixed ORM bug where the [`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")
    function would mask AttributeErrors or KeyErrors that should raise
    during mapper configuration due to user errors.
    对属性/键错误的捕获更具体，不包括配置步骤。[¶](#change-e8cf642e4e106568a47ada55df3ad138)

    参考文献：[＃3047](http://www.sqlalchemy.org/trac/ticket/3047)

### SQL [¶ T0\>](#change-0.8.7-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug in [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    and other [`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    subclasses where direct association of the type with a
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    would lead to a hang when events (like create events) were emitted
    on the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData").[¶](#change-a15c47336c5543b3fc74834213c1b3bd)

    参考文献：[＃3124](http://www.sqlalchemy.org/trac/ticket/3124)

-   **[sql] [bug]**Fixed a bug within the custom operator plus
    [`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
    system, whereby using a [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    in conjunction with variant would fail with an MRO error when a
    comparison operator was
    used.[¶](#change-54a43ce4f9140ba4a030c184f23dc9f6)

    参考文献：[＃3102](http://www.sqlalchemy.org/trac/ticket/3102)

-   **[sql] [bug]**Fixed bug in INSERT..FROM SELECT construct where
    selecting from a UNION would wrap the union in an anonymous (e.g.
    unlabled) subquery.[¶](#change-2d3949a5f46b25fe3382151b8669ae6b)

    参考文献：[＃3044](http://www.sqlalchemy.org/trac/ticket/3044)

-   修复了当[`Table.update()`](core_metadata.html#sqlalchemy.schema.Table.update "sqlalchemy.schema.Table.update")和[`Table.delete()`](core_metadata.html#sqlalchemy.schema.Table.delete "sqlalchemy.schema.Table.delete")在空的时候会产生一个空的WHERE子句的问题。**[sql]
    [bug]** [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")或[`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")或其他空白表达。这与[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的一致。[¶](#change-f4de3727dd13fd61c02ae2721cfaafc5)

    参考文献：[＃3045](http://www.sqlalchemy.org/trac/ticket/3045)

### 的PostgreSQL [¶ T0\>](#change-0.8.7-postgresql "Permalink to this headline")

-   **[postgresql] [bug]**为PG [`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")类型添加了`hashable=False`标志，这是允许ORM跳过尝试在混合列/实体列表中请求ORM映射的HSTORE列时“散列”。补丁礼貌GunnlaugurÞórBriem。[¶](#change-127ec92a16e57cf51809b91f2b78c9d6)

    参考文献：[＃3053](http://www.sqlalchemy.org/trac/ticket/3053)

-   **[postgresql]
    [bug]**添加了一个新的“断开连接”消息“连接意外关闭”。这似乎与更新版本的SSL有关。拉提请求Antti
    Haapala礼貌。[¶](#change-b3bdb51a69a9c0f277ff16a91bfc9e34)

    参考：[拉取请求bitbucket：13](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/13)

### MySQL的[¶ T0\>](#change-0.8.7-mysql "Permalink to this headline")

-   **[mysql] [bug]**MySQL error 2014 “commands out of sync” appears to
    be raised as a ProgrammingError, not OperationalError, in modern
    MySQL-Python versions; all MySQL error codes that are tested for “is
    disconnect” are now checked within OperationalError and
    ProgrammingError
    regardless.[¶](#change-5e1d2173c0bc6f19d10fa839a3f575fc)

    参考文献：[＃3101](http://www.sqlalchemy.org/trac/ticket/3101)

-   **[mysql] [bug]**Fixed bug where column names added to
    `mysql_length` parameter on an index needed to
    have the same quoting for quoted names in order to be recognized.
    该修复使得引号是可选的，但也提供了旧的行为，以便与使用变通方法的向后兼容。[¶](#change-6ebc4901dda2870745c197767107fd38)

    参考文献：[＃3085](http://www.sqlalchemy.org/trac/ticket/3085)

-   **[mysql]
    [bug]**增加了对使用等号在索引中包含KEY\_BLOCK\_SIZE的表来反映表的支持。拉请求礼貌肖恩McGivern。[¶](#change-adc1cf48426d16ff7afa412b798f7afb)

    参考文献：[拉取请求bitbucket：15](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/15)

### MSSQL [¶ T0\>](#change-0.8.7-mssql "Permalink to this headline")

-   **[mssql] [bug]**Added statement encoding to the “SET
    IDENTITY\_INSERT” statements which operate when an explicit INSERT
    is being interjected into an IDENTITY column, to support non-ascii
    table identifiers on drivers such as pyodbc + unix + py2k that don’t
    support unicode
    statements.[¶](#change-a332694f4a4dea710533a471230b2559)

-   **[mssql] [bug]**In the SQL Server pyodbc dialect, repaired the
    implementation for the `description_encoding`
    dialect parameter, which when not explicitly set was preventing
    cursor.description from being parsed correctly in the case of result
    sets that contained names in alternate encodings.
    这个参数不应该被继续使用。[¶](#change-abc172e784213b6cd1a62bf4af97acdd)

    参考文献：[＃3091](http://www.sqlalchemy.org/trac/ticket/3091)

### 杂项[¶ T0\>](#change-0.8.7-misc "Permalink to this headline")

-   **[bug] [declarative]**The `__mapper_args__`
    dictionary is copied from a declarative mixin or abstract class when
    accessed, so that modifications made to this dictionary by
    declarative itself won’t conflict with that of other mappings.
    关于`version_id_col`和`polymorphic_on`参数的字典被修改，将内部的列替换为正式映射到本地类/表的列。[¶
    t4 \>](#change-4247b43502c3504d7399eff5dbaec535)

    参考文献：[＃3062](http://www.sqlalchemy.org/trac/ticket/3062)

-   **[bug] [ext]**Fixed bug in mutable extension where
    [`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    did not report change events for the `setdefault()` dictionary
    operation.[¶](#change-af885a6f2bdf7de42dea7ecbd89161c8)

    参考文献：[＃3093](http://www.sqlalchemy.org/trac/ticket/3093)，[＃3051](http://www.sqlalchemy.org/trac/ticket/3051)

-   **[bug] [ext]**Fixed bug where [`MutableDict.setdefault()`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict.setdefault "sqlalchemy.ext.mutable.MutableDict.setdefault")
    didn’t return the existing or new value (this bug was not released
    in any 0.8 version).
    请求礼貌托马斯Hervé。[¶](#change-3fc56a563e46ae2b5aff7b904aae4ff9)

    References: [\#3093](http://www.sqlalchemy.org/trac/ticket/3093),
    [\#3051](http://www.sqlalchemy.org/trac/ticket/3051), [pull request
    bitbucket:24](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/24)

0.8.6 [¶ T0\>](#change-0.8.6 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014年3月28日

### 一般[¶ T0\>](#change-0.8.6-general "Permalink to this headline")

-   **[general] [bug]**Adjusted `setup.py` file to
    support the possible future removal of the
    `setuptools.Feature` extension from setuptools.
    如果此关键字不存在，则使用setuptools进行设置仍然会成功，而不会退回到distutils。可以通过设置DISABLE\_SQLALCHEMY\_CEXT环境变量来禁用C扩展构建。无论setuptools是否可用，该变量都适用。[¶](#change-4eb0725a9e53337556a261ca91f628e1)

    参考文献：[＃2986](http://www.sqlalchemy.org/trac/ticket/2986)

### ORM [¶ T0\>](#change-0.8.6-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed ORM bug where changing the primary key of an
    object, then marking it for DELETE would fail to target the correct
    row for DELETE.[¶](#change-8aade2e05c6bfa4d19d23d28d5d85e3c)

    参考文献：[＃3006](http://www.sqlalchemy.org/trac/ticket/3006)

-   **[orm] [bug]**Fixed regression from 0.8.3 as a result of
    [\#2818](http://www.sqlalchemy.org/trac/ticket/2818) where
    [`Query.exists()`](orm_query.html#sqlalchemy.orm.query.Query.exists "sqlalchemy.orm.query.Query.exists")
    wouldn’t work on a query that only had a
    [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    entry but no other
    entities.[¶](#change-3751a74e73168b0beaccedabc93166fc)

    参考文献：[＃2995](http://www.sqlalchemy.org/trac/ticket/2995)

-   **[orm] [bug]**Improved an error message which would occur if a
    query() were made against a non-selectable, such as a
    [`literal_column()`](core_sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column"),
    and then an attempt was made to use [`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
    such that the “left” side would be determined as `None` and then fail.
    现在可以明确检测到这种情况。[¶](#change-721de30f36994714bbaa71cb716e72e3)

-   **[orm] [bug]**从`sqlalchemy.orm.interfaces.__all__`中删除了过期名称，并使用当前名称刷新，以便导入\>
    \*再次运作。[¶](#change-1f6608c117a2d4b77f07a065788123ce)

    参考文献：[＃2975](http://www.sqlalchemy.org/trac/ticket/2975)

### SQL [¶ T0\>](#change-0.8.6-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug in [`tuple_()`](core_sqlelement.html#sqlalchemy.sql.expression.tuple_ "sqlalchemy.sql.expression.tuple_")
    construct where the “type” of essentially the first SQL expression
    would be applied as the “comparison type” to a compared tuple value;
    this has the effect in some cases of an inappropriate “type
    coersion” occurring, such as when a tuple that has a mix of String
    and Binary values improperly coerces target values to Binary even
    though that’s not what they are on the left side. [`tuple_()`](core_sqlelement.html#sqlalchemy.sql.expression.tuple_ "sqlalchemy.sql.expression.tuple_")
    now expects heterogeneous types within its list of
    values.[¶](#change-c61526d344b80f9ac2ea48bdf871a1c8)

    参考文献：[＃2977](http://www.sqlalchemy.org/trac/ticket/2977)

### 的PostgreSQL [¶ T0\>](#change-0.8.6-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**启用了“理智的多行计数”检查psycopg2
    DBAPI，因为它似乎在psycopg2
    2.0.9中受支持。[¶](#change-0e27187508dd3fc6a655238c01a756bd)

-   **[postgresql] [bug]**Fixed regression caused by release 0.8.5 /
    0.9.3’s compatibility enhancements where index reflection on
    Postgresql versions specific to only the 8.1, 8.2 series again
    broke, surrounding the ever problematic int2vector type.
    虽然int2vector支持从8.1开始的数组操作，但显然它只支持从8.3开始的对于varchar的CAST。[¶](#change-4ae0244a30e5c4a1057dc6ad07795cd1)

    参考文献：[＃3000](http://www.sqlalchemy.org/trac/ticket/3000)

### 杂项[¶ T0\>](#change-0.8.6-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug in mutable extension as well as
    [`attributes.flag_modified()`](orm_session_api.html#sqlalchemy.orm.attributes.flag_modified "sqlalchemy.orm.attributes.flag_modified")
    where the change event would not be propagated if the attribute had
    been reassigned to
    itself.[¶](#change-9b1493eda7803b32e8d28a92c52071a4)

    参考文献：[＃2997](http://www.sqlalchemy.org/trac/ticket/2997)

0.8.5 [¶ T0\>](#change-0.8.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2014年2月19日

### ORM [¶ T0\>](#change-0.8.5-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug where [`Query.get()`](orm_query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")
    would fail to consistently raise the [`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")
    that invokes when called on a query with existing criterion, when
    the given identity is already present in the identity
    map.[¶](#change-963fd6f9e65ff48f7f940166e32ee918)

    参考文献：[＃2951](http://www.sqlalchemy.org/trac/ticket/2951)

-   当一个迭代器对象被传递给[`class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper")或类似的错误消息时，修正错误消息，其中错误将无法在字符串格式上呈现。**[orm]
    [bug]**Pullleq礼貌Kyle
    Stark。[¶](#change-3c1858beb196d211a158e6b04a259e9e)

    参考文献：[请求github：58](https://github.com/zzzeek/sqlalchemy/pull/58)

-   **[orm] [bug]**调整[`subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")策略，确保查询在加载过程开始后运行；这是为了使得子查询优先于其他装载者，因为其他的加载者可能在错误的时间因为其他的预先/非加载情况而触及相同的属性。[](#change-299a27df663c00458dac3e27aa894641)

    参考文献：[＃2887](http://www.sqlalchemy.org/trac/ticket/2887)

-   **[orm] [bug]**Fixed bug when using joined table inheritance from a
    table to a select/alias on the base, where the PK columns were also
    not same named; the persistence system would fail to copy primary
    key values from the base table to the inherited table upon
    INSERT.[¶](#change-63f4633bd86bada94c11baebaccf2306)

    参考文献：[＃2885](http://www.sqlalchemy.org/trac/ticket/2885)

-   **[orm] [bug]**[`composite()`](orm_composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
    will raise an informative error message when the columns/attribute
    (names) passed don’t resolve to a Column or mapped attribute (such
    as an erroneous tuple); previously raised an unbound
    local.[¶](#change-75ee98f66c5efa2d8d93820f1b4eaf74)

    参考文献：[＃2889](http://www.sqlalchemy.org/trac/ticket/2889)

### 发动机[¶ T0\>](#change-0.8.5-engine "Permalink to this headline")

-   **[engine] [bug] [pool]**Fixed a critical regression caused by
    [\#2880](http://www.sqlalchemy.org/trac/ticket/2880) where the newly
    concurrent ability to return connections from the pool means that
    the “first\_connect” event is now no longer synchronized either,
    thus leading to dialect mis-configurations under even minimal
    concurrency situations.[¶](#change-b4da74a656ef5e3010bb13f8204f2fb0)

    参考文献：[＃2964](http://www.sqlalchemy.org/trac/ticket/2964)，[＃2880](http://www.sqlalchemy.org/trac/ticket/2880)

### SQL [¶ T0\>](#change-0.8.5-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed bug where calling [`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")
    with an empty list or tuple would raise an IndexError.
    它现在产生一个空的插入结构，就像空字典一样。[¶](#change-eaeab65db0f99940354a433b2c1757e7)

    参考文献：[＃2944](http://www.sqlalchemy.org/trac/ticket/2944)

-   **[sql] [bug]**Fixed bug where [`in_()`](orm_internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.in_ "sqlalchemy.orm.properties.RelationshipProperty.Comparator.in_")
    would go into an endless loop if erroneously passed a column
    expression whose comparator included the `__getitem__()` method, such as a column that uses the
    [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
    type.[¶](#change-33727fb51d625520dbf523e2021cb7ed)

    参考文献：[＃2957](http://www.sqlalchemy.org/trac/ticket/2957)

-   **[sql] [bug]**Fixed issue where a primary key column that has a
    Sequence on it, yet the column is not the “auto increment” column,
    either because it has a foreign key constraint or
    `autoincrement=False` set, would attempt to fire
    the Sequence on INSERT for backends that don’t support sequences,
    when presented with an INSERT missing the primary key value.
    这将发生在像SQLite，MySQL这样的非序列后端上。[¶](#change-a635a18f34a5c52c352eaacb7e5d45db)

    参考文献：[＃2896](http://www.sqlalchemy.org/trac/ticket/2896)

-   **[sql] [bug]**Fixed bug with [`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
    method where the order of the given names would not be taken into
    account when generating the INSERT statement, thus producing a
    mismatch versus the column names in the given SELECT statement.
    还注意到[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")意味着不能使用Python端插入默认值，因为该语句没有VALUES子句。[¶](#change-2a68cc38f848658f1f726522b257ae30)

    参考文献：[＃2895](http://www.sqlalchemy.org/trac/ticket/2895)

-   **[sql] [enhancement]**The exception raised when a
    [`BindParameter`](core_sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
    is present in a compiled statement without a value now includes the
    key name of the bound parameter in the error
    message.[¶](#change-328b0d6b8c257eff2b4edfd2852eb628)

### 的PostgreSQL [¶ T0\>](#change-0.8.5-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**增加了psycopg2断开连接检测的附加信息，“无法将数据发送到服务器”，补充了现有的“无法接收来自服务器的数据”并被用户观察到。
    [¶ T2\>](#change-abe4e69a00c65c9fc72433a2a5aad465)

    参考文献：[＃2936](http://www.sqlalchemy.org/trac/ticket/2936)

-   **[postgresql] [bug]**

    > Postgresql在Postgresql的旧版本（之前的版本）以及其他PG引擎（如Redshift）（假设Redshift的版本报告为\<8.1）时对postgresql反射行为的支持得到了改进。\<
    > span=""\>查询“索引”以及“主键”依赖于检查所谓的“int2vector”数据类型，该数据类型在8.1之前拒绝胁迫数组，导致查询中使用的“ANY()”运算符失败。当PG版本\<8.1被使用时，大量的搜索引擎已经找到了非常黑客但推荐的pg核心开发者查询，因此索引和主键约束反映现在可用于这些版本。\<
    > span=""\>

    [¶](#change-a3d203ef1bb5e3411e9e3e279194848f)

-   **[postgresql] [bug]**Revised this very old issue where the
    Postgresql “get primary key” reflection query were updated to take
    into account primary key constraints that were renamed; the newer
    query fails on very old versions of Postgresql such as version 7, so
    the old query is restored in those cases when server\_version\_info
    \< (8, 0) is detected.[¶](#change-3d5d651a2c1822482b8645ec21a68973)

    参考文献：[＃2291](http://www.sqlalchemy.org/trac/ticket/2291)

### MySQL的[¶ T0\>](#change-0.8.5-mysql "Permalink to this headline")

-   **[mysql] [feature]**添加了新的特定于MySQL的[`mysql.DATETIME`](dialects_mysql.html#sqlalchemy.dialects.mysql.DATETIME "sqlalchemy.dialects.mysql.DATETIME")，其中包括小数秒支持；还增加了对[`mysql.TIMESTAMP`](dialects_mysql.html#sqlalchemy.dialects.mysql.TIMESTAMP "sqlalchemy.dialects.mysql.TIMESTAMP")的小数秒支持。DBAPI支持是有限的，尽管小数秒被MySQL
    Connector / Python支持。补丁由Geert JM
    Vanderkelen提供。[¶](#change-e61353bcbaeea335f62823591b2bd3df)

    参考文献：[＃2941](http://www.sqlalchemy.org/trac/ticket/2941)

-   **[mysql] [bug]**添加了对`分区 BY`和`PARTITIONS`
    MySQL的支持将表关键字指定为`mysql_partition_by='value'`和`mysql_partitions='value'`至[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。拉玛请求提供Marcus
    McCurdy。[¶](#change-dc53ea0fad376d114f411a9855e869fc)

    References: [\#2966](http://www.sqlalchemy.org/trac/ticket/2966),
    [pull request
    bitbucket:12](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/12)

-   **[mysql] [bug]**Fixed bug which prevented MySQLdb-based dialects
    (e.g. pymysql) from working in Py3K, where a check for “connection
    charset” would fail due to Py3K’s more strict value comparison
    rules.
    这个调用在任何情况下都没有考虑到数据库版本，因为服务器版本在那时仍然是None，所以整个方法被简化为依赖于connection.character\_set\_name()。[¶
    t0 \>](#change-e9165d6fdae23130302d540e3bc6d597)

    参考文献：[＃2933](http://www.sqlalchemy.org/trac/ticket/2933)

-   **[mysql]
    [bug]**添加到cymysql方言的一些缺失方法，包括\_get\_server\_version\_info()和\_detect\_charset()。Pullreq礼貌Hajime
    Nakagami。[¶](#change-f55316fde4a189d8126b15e329332461)

    参考文献：[pull request
    github：61](https://github.com/zzzeek/sqlalchemy/pull/61)

### 源码[¶ T0\>](#change-0.8.5-sqlite "Permalink to this headline")

-   **[sqlite]
    [bug]**将唯一约束反射的回溯端口中遗漏的更改恢复为0.8，如果名称中包含保留关键字，那么带有SQLite的[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")列。拉请求罗马Podolyaka。[¶](#change-ead78f92084767f32a375ae68accf5b5)

    参考文献：[请求github：72](https://github.com/zzzeek/sqlalchemy/pull/72)

### MSSQL [¶ T0\>](#change-0.8.5-mssql "Permalink to this headline")

-   **[mssql] [bug] [firebird]**The “asdecimal” flag used with the
    [`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")
    type will now work with Firebird as well as the mssql+pyodbc
    dialects; previously the decimal conversion was not
    occurring.[¶](#change-02b8136f04eac946a40b7db8f2f4f0f3)

-   **[mssql] [bug] [pymssql]**Added “Net-Lib error during Connection
    reset by peer” message to the list of messages checked for
    “disconnect” within the pymssql dialect. 礼貌John
    Anderson。[¶](#change-87840ae63e620637ec1dd97e9f1fbbfc)

    参考文献：[请求github：51](https://github.com/zzzeek/sqlalchemy/pull/51)

### 火鸟[¶ T0\>](#change-0.8.5-firebird "Permalink to this headline")

-   **[firebird] [bug]**火鸟方言会引用以下划线开头的标识符。Courtesy
    Treeve Jelbert。[¶](#change-491c479b04e5d70530ef87406332f723)

    参考文献：[＃2897](http://www.sqlalchemy.org/trac/ticket/2897)

-   **[firebird]
    [bug]**修正了Firebird索引反射中索引内的列未正确排序的错误；现在它们按照RDB
    \$
    FIELD\_POSITION的顺序排序。[¶](#change-8066c3961ec654ddd830fa2e4bb5a2b8)

### 杂项[¶ T0\>](#change-0.8.5-misc "Permalink to this headline")

-   **[bug] [py3k]**Fixed Py3K bug where a missing import would cause
    “literal binary” mode to fail to import “util.binary\_type” when
    rendering a bound parameter. 0.9以不同的方式处理。请求礼貌Andreas
    Zeidler。[¶](#change-5ab170daca7483efaf20de27592c8329)

    参考文献：[pull request
    github：63](https://github.com/zzzeek/sqlalchemy/pull/63)

-   **[bug]
    [declarative]**错误消息，当一个字符串arg发送到[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，它没有解析为类或映射器时，它的工作方式与当收到一个非字符串arg时，它表明有配置错误的关系的名字。[¶](#change-d707bd93370fc840f28c9d8faf6c209f)

    参考文献：[＃2888](http://www.sqlalchemy.org/trac/ticket/2888)

0.8.4 [¶ T0\>](#change-0.8.4 "Permalink to this headline")
----------------------------------------------------------

发布日期：2013年12月8日

### ORM [¶ T0\>](#change-0.8.4-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed a regression introduced by
    [\#2818](http://www.sqlalchemy.org/trac/ticket/2818) where the
    EXISTS query being generated would produce a “columns being
    replaced” warning for a statement with two same-named columns, as
    the internal SELECT wouldn’t have use\_labels
    set.[¶](#change-e092c358f026124d42419bc6ec0e6222)

    参考文献：[＃2818](http://www.sqlalchemy.org/trac/ticket/2818)

### 发动机[¶ T0\>](#change-0.8.4-engine "Permalink to this headline")

-   **[engine] [bug]**A DBAPI that raises an error on
    `connect()` which is not a subclass of
    dbapi.Error (such as `TypeError`,
    `NotImplementedError`, etc.)
    将不会传播异常。以前，特定于`connect()`例程的错误处理将通过方言的[`Dialect.is_disconnect()`](core_internals.html#sqlalchemy.engine.interfaces.Dialect.is_disconnect "sqlalchemy.engine.interfaces.Dialect.is_disconnect")例程错误地运行异常，并将其包装在[`sqlalchemy.exc.DBAPIError`](core_exceptions.html#sqlalchemy.exc.DBAPIError "sqlalchemy.exc.DBAPIError")它现在以与执行过程中发生的相同的方式传播。[¶](#change-4c94e9eaf5cee7f9d244460416e5882e)

    参考文献：[＃2881](http://www.sqlalchemy.org/trac/ticket/2881)

-   **[engine] [bug] [pool]**The [`QueuePool`](core_pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
    has been enhanced to not block new connection attempts when an
    existing connection attempt is blocking.
    以前，在监控溢出的块中，新连接的产生被串行化；溢出计数器现在在连接过程本身之外的其自己的临界区内被改变。[¶](#change-f61deee220ca510a2a34634540647466)

    参考文献：[＃2880](http://www.sqlalchemy.org/trac/ticket/2880)

-   **[engine] [bug] [pool]**Made a slight adjustment to the logic which
    waits for a pooled connection to be available, such that for a
    connection pool with no timeout specified, it will every half a
    second break out of the wait to check for the so-called “abort”
    flag, which allows the waiter to break out in case the whole
    connection pool was dumped; normally the waiter should break out due
    to a notify\_all() but it’s possible this notify\_all() is missed in
    very slim cases.
    这是在0.8.0中首次引入的逻辑的扩展，这个问题偶尔会在压力测试中被观察到。[¶](#change-9f50f03f97a15744f325f3b1f9efe144)

    参考文献：[＃2522](http://www.sqlalchemy.org/trac/ticket/2522)

-   **[engine] [bug]**Fixed bug where SQL statement would be improperly
    ASCII-encoded when a pre-DBAPI [`StatementError`](core_exceptions.html#sqlalchemy.exc.StatementError "sqlalchemy.exc.StatementError")
    were raised within [`Connection.execute()`](core_connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute"),
    causing encoding errors for non-ASCII statements.
    字符串化现在保留在Python
    unicode中，从而避免编码错误。[¶](#change-93068fc8797e8560dedac1d5ab086a48)

    参考文献：[＃2871](http://www.sqlalchemy.org/trac/ticket/2871)

### SQL [¶ T0\>](#change-0.8.4-sql "Permalink to this headline")

-   **[sql] [feature]**通过[`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")方法增加了对“唯一约束”反射的支持。感谢Roman
    Podolyaka的补丁。[¶](#change-fa2f32447a743902b48fa3efd6a94515)

    参考文献：[＃1443](http://www.sqlalchemy.org/trac/ticket/1443)

### 的PostgreSQL [¶ T0\>](#change-0.8.4-postgresql "Permalink to this headline")

-   **[postgresql] [bug]**Fixed bug where index reflection would
    mis-interpret indkey values when using the pypostgresql adapter,
    which returns these values as lists vs. psycopg2’s return type of
    string.[¶](#change-a45c250bf38e2c937f2650c53d1eba72)

    参考文献：[＃2855](http://www.sqlalchemy.org/trac/ticket/2855)

### MSSQL [¶ T0\>](#change-0.8.4-mssql "Permalink to this headline")

-   **[mssql] [bug]**修正了在0.8.0版本中引入索引的`DROP INDEX`如果索引处于备用模式中，MSSQL将不正确地渲染； schemaname /
    tablename将被颠倒。该格式也进行了修改以符合当前的MSSQL文档。Courtesy
    Derek Harland。[¶](#change-811ab40236ae0100f280d4d9293b5b0b)

    参考文献：[pull request
    bitbucket：7](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/7)

### 预言[¶ T0\>](#change-0.8.4-oracle "Permalink to this headline")

-   **[oracle]
    [bug]**增加了ORA-02396“最大空闲时间”的错误代码到cx\_oracle的“is
    disconnect”代码列表。[¶](#change-6c4c2c6ed5c5a6fea521de2db0a7100d)

    参考文献：[＃2864](http://www.sqlalchemy.org/trac/ticket/2864)

-   **[oracle] [bug]**Fixed bug where Oracle `VARCHAR` types given with no length (e.g. for a `CAST` or similar) would incorrectly render `None CHAR` or similar.[¶](#change-b899c8283eb4c7a1212dd4747c28ba83)

    参考文献：[＃2870](http://www.sqlalchemy.org/trac/ticket/2870)

### 杂项[¶ T0\>](#change-0.8.4-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug which prevented the `serializer` extension from working correctly with table or column
    names that contain non-ASCII
    characters.[¶](#change-918754b17d70ee948a39721ec5fac1c0)

    参考文献：[＃2869](http://www.sqlalchemy.org/trac/ticket/2869)

0.8.3 [¶ T0\>](#change-0.8.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2013年10月26日

### ORM [¶ T0\>](#change-0.8.3-orm "Permalink to this headline")

-   **[orm] [feature]**添加了[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    `distinct_target_key`的新选项。这使得子查询预热加载器策略能够将DISTINCT应用到最内层的SELECT子查询中，以协助处理与该关系相对应的最内层查询生成重复行的情况（目前还没有解决内部dupe行问题的一般解决方案但是，当加入最内层子查询之外的子查询会产生欺骗）。当标志被设置为`True`时，DISTINCT被无条件渲染，当它被设置为`None`时，如果最内层关系针对不包含完整的主键。该选项在0.8中默认为False（例如，在所有情况下默认关闭），0.9中的None（例如默认为自动）。感谢Alexander
    Koval为此提供帮助。

    也可以看看

    [Subquery Eager Loading will apply DISTINCT to the innermost SELECT
    for some queries](migration_09.html#change-2836)

    [¶](#change-5f2bdb197c797932107639ab179073f5)

    参考文献：[＃2836](http://www.sqlalchemy.org/trac/ticket/2836)

-   **[orm] [bug]**Fixed bug where list instrumentation would fail to
    represent a setslice of `[0:0]` correctly, which
    in particular could occur when using `insert(0, item)` with the association proxy.
    由于Python集合中的一些怪癖，使用Python
    3而不是2的可能性更大。[¶](#change-312eebb9957781ee59f1076d9f996470)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2807](http://www.sqlalchemy.org/trac/ticket/2807)

-   **[orm] [bug]**Fixed bug where using an annotation such as
    [`remote()`](orm_relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")
    or [`foreign()`](orm_relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")
    on a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    before association with a parent [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    could produce issues related to the parent table not rendering
    within joins, due to the inherent copy operation performed by an
    annotation.[¶](#change-6e089c6d7cb9b25d826af89e8a72abbd)

    参考文献：[＃2813](http://www.sqlalchemy.org/trac/ticket/2813)

-   **[orm] [bug]**Fixed bug where [`Query.exists()`](orm_query.html#sqlalchemy.orm.query.Query.exists "sqlalchemy.orm.query.Query.exists")
    failed to work correctly without any WHERE criterion.
    礼貌弗拉基米尔Magamedov。[¶](#change-8a0f22e5cd148955e268067990e34736)

    参考文献：[＃2818](http://www.sqlalchemy.org/trac/ticket/2818)

-   **[orm]
    [bug]**从0.9反向移植了一个变化，即在多态继承加载中使用的映射器层次的迭代是排序的，这允许为多态查询生成的SELECT语句具有确定性渲染，转向可以帮助缓存SQL字符串本身的缓存方案。[¶](#change-bd6ff2bdbf0cd87d5d91cdb0b8bbaea3)

    参考文献：[＃2779](http://www.sqlalchemy.org/trac/ticket/2779)

-   **[orm] [bug]**Fixed a potential issue in an ordered sequence
    implementation used by the ORM to iterate mapper hierarchies; under
    the Jython interpreter this implementation wasn’t ordered, even
    though cPython and Pypy maintained
    ordering.[¶](#change-e8bba6ebed4c7f4e046a964e48671559)

    参考文献：[＃2794](http://www.sqlalchemy.org/trac/ticket/2794)

-   **[orm] [bug]**Fixed bug in ORM-level event registration where the
    “raw” or “propagate” flags could potentially be mis-configured in
    some “unmapped base class”
    configurations.[¶](#change-8ae1869183642491f4759b99ff363f50)

    参考文献：[＃2786](http://www.sqlalchemy.org/trac/ticket/2786)

-   **[orm] [bug]**性能修正与加载映射实体时使用[`defer()`](orm_loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")选项有关。在加载时将每个对象的延迟可调用应用于实例的函数开销显着高于仅从该行加载数据的开销（请注意，`defer()`旨在减少DB
    /网络开销，不一定函数调用计数）；在所有情况下，函数调用开销都小于从列中加载数据的开销。每个负载创建的“惰性可调用”对象的数量也从N（结果中的总延迟值）减少到1（延迟列的总数）。[¶](#change-e0c26c7eb00d470043e72cb138076e83)

    参考文献：[＃2778](http://www.sqlalchemy.org/trac/ticket/2778)

-   **[orm] [bug]**Fixed bug whereby attribute history functions would
    fail when an object we moved from “persistent” to “pending” using
    the [`make_transient()`](orm_session_api.html#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")
    function, for operations involving collection-based
    backrefs.[¶](#change-9c03ac102f40e916dc98dab9b39dcff9)

    参考文献：[＃2773](http://www.sqlalchemy.org/trac/ticket/2773)

### orm declarative [¶](#change-0.8.3-orm-declarative "Permalink to this headline")

-   **[feature] [orm]
    [declarative]**添加了一个便捷类装饰器[`as_declarative()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.as_declarative "sqlalchemy.ext.declarative.as_declarative")，是[`declarative_base()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")基类用于使用漂亮的类装饰方法来应用。[¶](#change-65c116799fbc9d1d40e71d7c9f431288)

### 发动机[¶ T0\>](#change-0.8.3-engine "Permalink to this headline")

-   **[engine] [feature]**`repr()` for the
    [`URL`](core_engines.html#sqlalchemy.engine.url.URL "sqlalchemy.engine.url.URL")
    of an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    will now conceal the password using asterisks. Courtesy
    GunnlaugurÞórBriem。[¶](#change-d9b738783ea84abacc41fd558aa182bf)

    参考文献：[＃2821](http://www.sqlalchemy.org/trac/ticket/2821)

-   **[engine] [bug]**The regexp used by the [`make_url()`](core_engines.html#sqlalchemy.engine.url.make_url "sqlalchemy.engine.url.make_url")
    function now parses ipv6 addresses, e.g. surrounded by
    brackets.[¶](#change-cf88a1675c925c94bf267aa8591d2ef4)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2851](http://www.sqlalchemy.org/trac/ticket/2851)

-   **[engine] [bug] [oracle]**Dialect.initialize() is not called a
    second time if an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    is recreated, due to a disconnect error. 这解决了Oracle
    8方言中的一个特定问题，但通常dialect.initialize()阶段应该只能用于每种方言一次。[¶](#change-3c8c71f7f42cb422d498b573187ea739)

    参考文献：[＃2776](http://www.sqlalchemy.org/trac/ticket/2776)

-   **[engine] [bug] [pool]**Fixed bug where [`QueuePool`](core_pooling.html#sqlalchemy.pool.QueuePool "sqlalchemy.pool.QueuePool")
    would lose the correct checked out count if an existing pooled
    connection failed to reconnect after an invalidate or recycle
    event.[¶](#change-a95b0f6765fdf5ebdf844806fb2aa122)

    参考文献：[＃2772](http://www.sqlalchemy.org/trac/ticket/2772)

### SQL [¶ T0\>](#change-0.8.3-sql "Permalink to this headline")

-   **[sql] [feature]**为[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")结构[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")添加了新方法。Given
    a list of columns and a selectable, renders
    `INSERT INTO (table) (columns) SELECT ..`.[¶](#change-5c72fe0ff07c34ebffffec6a4542ae43)

    参考文献：[＃722](http://www.sqlalchemy.org/trac/ticket/722)

-   **[sql] [feature]**The [`update()`](core_dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update"),
    [`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert"),
    and [`delete()`](core_dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")
    constructs will now interpret ORM entities as target tables to be
    operated upon, e.g.:

        from sqlalchemy import insert, update, delete

        ins = insert(SomeMappedClass).values(x=5)

        del_ = delete(SomeMappedClass).where(SomeMappedClass.id == 5)

        upd = update(SomeMappedClass).where(SomeMappedClass.id == 5).values(name='ed')

    [¶](#change-7770102ac46e881dbf4291237e0e33d6)

-   **[sql]
    [bug]**固定回归到0.7.9，如果CTE的名称在多个FROM子句中被引用，那么它的名称可能不会被正确引用。[¶](#change-f1bb3cb5a1c3bf0bb7fd96cfb5c1df32)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2801](http://www.sqlalchemy.org/trac/ticket/2801)

-   **[sql] [bug] [cte]**Fixed bug in common table expression system
    where if the CTE were used only as an `alias()`
    construct, it would not render using the WITH
    keyword.[¶](#change-a320ea9f0d44002b0e0a79744920fcd9)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2783](http://www.sqlalchemy.org/trac/ticket/2783)

-   **[sql] [bug]**Fixed bug in [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    DDL where the “quote” flag from a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object would not be
    propagated.[¶](#change-68f18f76eb79a1699492214db9610cae)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2784](http://www.sqlalchemy.org/trac/ticket/2784)

-   **[sql] [bug]**Fixed bug where [`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")
    would not interpret ORM elements with a
    `__clause_element__()` method
    properly.[¶](#change-e0ef7971da8c7643222fa1def3f24581)

    参考文献：[＃2849](http://www.sqlalchemy.org/trac/ticket/2849)

-   **[sql] [bug]**The [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    and [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    types now bypass any custom (e.g. TypeDecorator) type in use when
    producing the CHECK constraint for the “non native” type.
    这样自定义类型不会被包含在CHECK中的表达式中，因为这个表达式违背了“impl”值而不是“装饰”值。[¶](#change-244a726e2b5227f5eb88f0feac261fef)

    参考文献：[＃2842](http://www.sqlalchemy.org/trac/ticket/2842)

-   **[sql] [bug]**The `.unique` flag on
    [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    could be produced as `None` if it was generated
    from a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    that didn’t specify `unique` (where it defaults
    to `None`). 该标志现在总是`True`或`False`。[¶](#change-a4428210d511f08c886403e951a6f7c5)

    参考文献：[＃2825](http://www.sqlalchemy.org/trac/ticket/2825)

-   **[sql] [bug]**Fixed bug in default compiler plus those of
    postgresql, mysql, and mssql to ensure that any literal SQL
    expression values are rendered directly as literals, instead of as
    bound parameters, within a CREATE INDEX statement.
    这也改变了其他DDL的渲染方案，如约束。[¶](#change-487183f04e6da9aa27d8817bca9906d1)

    参考文献：[＃2742](http://www.sqlalchemy.org/trac/ticket/2742)

-   **[sql] [bug]**A [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    that is made to refer to itself in its FROM clause, typically via
    in-place mutation, will raise an informative error message rather
    than causing a recursion
    overflow.[¶](#change-f403fbb0f55df86dac079fb15eb4e7d7)

    参考文献：[＃2815](http://www.sqlalchemy.org/trac/ticket/2815)

-   **[sql] [bug]**不推荐使用[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")上的非工作“模式”参数；提出警告。在0.9中删除。[¶](#change-5e6a31e42152647f14bf8bae4dab5ba4)

    参考文献：[＃2831](http://www.sqlalchemy.org/trac/ticket/2831)

-   **[sql] [bug]**Fixed bug where using the `column_reflect` event to change the `.key` of the
    incoming [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    would prevent primary key constraints, indexes, and foreign key
    constraints from being correctly
    reflected.[¶](#change-675072698df0b30451fcea8d235d1e75)

    参考文献：[＃2811](http://www.sqlalchemy.org/trac/ticket/2811)

-   **[sql] [bug]**The [`ColumnOperators.notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
    operator added in 0.8 now properly produces the negation of the
    expression “IN” returns when used against an empty
    collection.[¶](#change-7012bfcf9dece88f5446b4fd773cd291)

-   **[sql] [bug] [postgresql]**Fixed bug where the expression system
    relied upon the `str()` form of a some
    expressions when referring to the `.c`
    collection on a `select()` construct, but the
    `str()` form isn’t available since the element
    relies on dialect-specific compilation constructs, notably the
    `__getitem__()` operator as used with a
    Postgresql `ARRAY` element.
    该修补程序还添加了一个新的异常类[`UnsupportedCompilationError`](core_exceptions.html#sqlalchemy.exc.UnsupportedCompilationError "sqlalchemy.exc.UnsupportedCompilationError")，这是在编译器被要求编译一些不知道如何去做的情况下引发的。[¶](#change-1694faa8f6477c69858ec6cf648a0ca0)

    参考文献：[＃2780](http://www.sqlalchemy.org/trac/ticket/2780)

### 的PostgreSQL [¶ T0\>](#change-0.8.3-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**从列的服务器默认值的反射中删除了128个字符的截断；此代码原始来自PG系统视图，它为了可读性而截断了字符串。[¶](#change-0d2fbae9923d9363bce65e24adefba23)

    参考文献：[＃2844](http://www.sqlalchemy.org/trac/ticket/2844)

-   **[postgresql] [bug]**括号将应用于复合SQL表达式，并在CREATE
    INDEX语句的列表中呈现。[¶](#change-b2f836d7e1ecf9fb536a07100e079cc5)

    参考文献：[＃2742](http://www.sqlalchemy.org/trac/ticket/2742)

-   **[postgresql]
    [bug]**修复了Postgresql版本字符串在前缀“Postgresql”或“EnterpriseDB”之前的前缀不会被解析的错误。Courtesy
    Scott Schaefer。[¶](#change-4b56ae5537f1f171e43b34d6b652deac)

    参考文献：[＃2819](http://www.sqlalchemy.org/trac/ticket/2819)

### MySQL的[¶ T0\>](#change-0.8.3-mysql "Permalink to this headline")

-   **[mysql] [bug]**版本5.5,5.6的MySQL保留字更新，Hanno
    Schlichting提供。[¶](#change-e43f31fa51abb8d936a70e25174d7889)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2791](http://www.sqlalchemy.org/trac/ticket/2791)

-   **[mysql] [bug]**The change in
    [\#2721](http://www.sqlalchemy.org/trac/ticket/2721), which is that
    the `deferrable` keyword of
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    is silently ignored on the MySQL backend, will be reverted as of
    0.9; this keyword will now render again, raising errors on MySQL as
    it is not understood - the same behavior will also apply to the
    `initially` keyword.
    在0.8中，关键字将保持忽略，但会发出警告。此外，`match`关键字现在会在0.9上产生一个[`CompileError`](core_exceptions.html#sqlalchemy.exc.CompileError "sqlalchemy.exc.CompileError")，并在0.8上发出警告；这个关键字不仅被MySQL默默地忽略，而且打破了ON
    UPDATE / ON DELETE选项。

    要使用在MySQL上不呈现或呈现不同的[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")，请使用自定义编译选项。这个用法的一个例子已经添加到文档中，请参阅[MySQL Foreign Keys](dialects_mysql.html#mysql-foreign-keys)。

    [¶](#change-f8980c12474534ac31102ea813a57a1b)

    参考文献：[＃2721](http://www.sqlalchemy.org/trac/ticket/2721)，[＃2839](http://www.sqlalchemy.org/trac/ticket/2839)

-   **[mysql] [bug]**MySQL-connector dialect now allows options in the
    create\_engine query string to override those defaults set up in the
    connect, including “buffered” and
    “raise\_on\_warnings”.[¶](#change-aada183c3aa9880e9262cd3ee6d0f047)

    参考文献：[＃2515](http://www.sqlalchemy.org/trac/ticket/2515)

### 源码[¶ T0\>](#change-0.8.3-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**新添加的SQLite
    DATETIME参数storage\_format和regexp显然没有完全正确地实现；当论据被接受时，实际上它们将不起作用；这已被修复。[¶](#change-15fd7971b2a7d12d88f6701df1068e0a)

    参考文献：[＃2781](http://www.sqlalchemy.org/trac/ticket/2781)

### 预言[¶ T0\>](#change-0.8.3-oracle "Permalink to this headline")

-   **[oracle] [bug]**Fixed bug where Oracle table reflection using
    synonyms would fail if the synonym and the table were in different
    remote schemas. 补丁修复Kyle
    Derr礼貌。[¶](#change-df45fec86fb2c3ba45a71dfaa6bc589b)

    参考文献：[＃2853](http://www.sqlalchemy.org/trac/ticket/2853)

### 杂项[¶ T0\>](#change-0.8.3-misc "Permalink to this headline")

-   **[feature]**将`system=True`添加到[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")中，将列标记为系统自动创建的列数据库（例如Postgresql
    `oid`或`xmin`）。该列将从`CREATE TABLE`语句中省略，但否则可用于查询。另外，通过生成返回`None`的规则，可以将[`CreateColumn`](core_ddl.html#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")结构应用于允许跳过列的自定义编译规则。[¶](#change-77ffc6dfb1cfdfa745330bb19c5a7f09)

-   **[feature]
    [examples]**改进了`examples/generic_associations`中的示例，包括`discriminator_on_association.py`利用单个表继承进行工作“鉴别者”。还添加了一个真正的“通用外键”示例，该示例与其他流行框架的工作方式类似，因为它使用开放式整数指向任何其他表，前面提到了传统的参照完整性。虽然我们不推荐这种模式，但信息要免费。[¶](#change-512d118321cd5025929f5f9fe0b5f82f)

-   **[bug]
    [examples]**在版本控制示例中创建的历史记录表中添加了“autoincrement =
    False”，因为该表在任何情况下都不应该有autoinc，Patrick Schmid提供[¶
    T2\>](#change-b9729e8544ea5c4cef86dc541f174f91)

0.8.2 [¶ T0\>](#change-0.8.2 "Permalink to this headline")
----------------------------------------------------------

发布时间：2013年7月3日

### ORM [¶ T0\>](#change-0.8.2-orm "Permalink to this headline")

-   **[orm]
    [feature]**添加了一个新的方法[`Query.select_entity_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_entity_from "sqlalchemy.orm.query.Query.select_entity_from")，它将在0.9中替换[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")在0.8中，这两种方法执行相同的功能，以便代码可以根据需要进行迁移以使用[`Query.select_entity_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_entity_from "sqlalchemy.orm.query.Query.select_entity_from")方法。有关详细信息，请参阅0.9迁移指南。[¶](#change-c05bcdba9495b9c08f29a9a3304b5d70)

    参考文献：[＃2736](http://www.sqlalchemy.org/trac/ticket/2736)

-   **[orm]
    [bug]**尝试刷新继承类的对象时发出一个警告，其中多态鉴别符已被分配给该类无效的值[¶
    T2\>](#change-2317157430cb5b525364054990497eb9)

    参考文献：[＃2750](http://www.sqlalchemy.org/trac/ticket/2750)

-   **[orm] [bug]**Fixed bug in polymorphic SQL generation where
    multiple joined-inheritance entities against the same base class
    joined to each other as well would not track columns on the base
    table independently of each other if the string of joins were more
    than two entities long.[¶](#change-14c40b5830402d04cc5573ff79f332eb)

    参考文献：[＃2759](http://www.sqlalchemy.org/trac/ticket/2759)

-   **[orm] [bug]**Fixed bug where sending a composite attribute into
    [`Query.order_by()`](orm_query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")
    would produce a parenthesized expression not accepted by some
    databases.[¶](#change-3f06591039ab2c0ed2a898ffead8c351)

    参考文献：[＃2754](http://www.sqlalchemy.org/trac/ticket/2754)

-   **[orm] [bug]**修复了复合属性与[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")函数之间的交互。以前，当应用别名时，组合属性在比较操作中无法正确工作。[¶](#change-ee0ed481a7e6f8f589ed19bf4e7020b9)

    参考文献：[＃2755](http://www.sqlalchemy.org/trac/ticket/2755)

-   **[orm] [bug] [ext]**Fixed bug where [`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    didn’t report a change event when `clear()` was
    called.[¶](#change-6e0ede3310afa0c7b3abbffef4b0c705)

    参考文献：[＃2730](http://www.sqlalchemy.org/trac/ticket/2730)

-   **[orm] [bug]**Fixed a regression caused by
    [\#2682](http://www.sqlalchemy.org/trac/ticket/2682) whereby the
    evaluation invoked by [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
    and [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")
    would hit upon unsupported `True` and
    `False` symbols which now appear due to the
    usage of `IS`.[¶](#change-12637c141bbfeb7bbcd46cd473878404)

    参考文献：[＃2737](http://www.sqlalchemy.org/trac/ticket/2737)

-   **[orm] [bug]**Fixed a regression from 0.7 caused by this ticket,
    which made the check for recursion overflow in self-referential
    eager joining too loose, missing a particular circumstance where a
    subclass had lazy=”joined” or “subquery” configured and the load was
    a “with\_polymorphic” against the
    base.[¶](#change-885c8bfa8d2c554bbf343bc9537b9b8e)

    参考文献：[＃2481](http://www.sqlalchemy.org/trac/ticket/2481)

-   **[orm] [bug]**Fixed a regression from 0.7 where the contextmanager
    feature of [`Session.begin_nested()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")
    would fail to correctly roll back the transaction when a flush error
    occurred, instead raising its own exception while leaving the
    session still pending a
    rollback.[¶](#change-8f7f445e4299f4950355f914240458aa)

    参考文献：[＃2718](http://www.sqlalchemy.org/trac/ticket/2718)

### orm declarative [¶](#change-0.8.2-orm-declarative "Permalink to this headline")

-   **[feature] [orm] [declarative]**ORM descriptors such as hybrid
    properties can now be referenced by name in a string argument used
    with `order_by`, `primaryjoin`, or similar in [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
    in addition to column-bound
    attributes.[¶](#change-4ff13b29211231fa799c3c09281ee426)

    参考文献：[＃2761](http://www.sqlalchemy.org/trac/ticket/2761)

### 发动机[¶ T0\>](#change-0.8.2-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed bug where the `reset_on_return` argument to various [`Pool`](core_pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
    implementations would not be propagated when the pool was
    regenerated. Courtesy
    Eevee。[¶](#change-50203a688fa4d9aeaca6bd82e0186374)

    参考文献：[请求github：6](https://github.com/zzzeek/sqlalchemy/pull/6)

-   **[engine] [bug] [sybase]**Fixed a bug where the routine to detect
    the correct kwargs being sent to [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
    would fail in some cases, such as with the Sybase
    dialect.[¶](#change-1b593aa7c17313e714731fc32dac43e7)

    参考文献：[＃2732](http://www.sqlalchemy.org/trac/ticket/2732)

### SQL [¶ T0\>](#change-0.8.2-sql "Permalink to this headline")

-   **[sql] [feature]**为[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")提供了一个名为[`TypeDecorator.coerce_to_is_types`](core_custom_types.html#sqlalchemy.types.TypeDecorator.coerce_to_is_types "sqlalchemy.types.TypeDecorator.coerce_to_is_types")的新属性，以便更容易控制如何使用`==`或`!=` to `None`和布尔类型用于生成`IS`表达式，参数。[¶
    T16\>](#change-4ed6ba3989c1e07968a5407fcfca903f)

    参考文献：[＃2734](http://www.sqlalchemy.org/trac/ticket/2734)，[＃2744](http://www.sqlalchemy.org/trac/ticket/2744)

-   **[sql] [bug]**对于[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")结构的相关行为的多个修复，在0.8.0中首次引入：

    -   为了满足这样的用例，其中FROM条目应该向外关联到一个包含另一个的SELECT，然后包含这个SELECT，当通过[`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")建立显式相关性时，前提是目标选择位于WHERE
        / ORDER BY /
        columns子句所包含的链中，而不仅仅是嵌套的FROM子句。This makes
        [`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")
        act more compatibly to that of 0.7 again while still maintaining
        the new “smart” correlation.
    -   当不使用显式关联时，通常的“隐式”关联将其行为限制为立即封闭的SELECT，以最大化与0.7应用程序的兼容性，并且还防止在这种情况下嵌套FROM之间的相关性，保持与0.8.0
        / 0.8的兼容性。 1。
    -   [`Select.correlate_except()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")方法在所有情况下都不会阻止给定的FROM子句相关，并且也会导致FROM子句完全被错误地省略（更像0.7会做的），这已经固定。
    -   调用select.correlate\_except（None）将按照预期将所有FROM子句输入到相关中。

    [¶](#change-9a8da1a66f295972299d1917dabc5c6d)

    参考文献：[＃2668](http://www.sqlalchemy.org/trac/ticket/2668)，[＃2746](http://www.sqlalchemy.org/trac/ticket/2746)

-   **[sql] [bug]**Fixed bug whereby joining a select() of a table “A”
    with multiple foreign key paths to a table “B”, to that table “B”,
    would fail to produce the “ambiguous join condition” error that
    would be reported if you join table “A” directly to “B”; it would
    instead produce a join condition with multiple
    criteria.[¶](#change-eb9b4feabd1d4a81b9f5f3d35270051b)

    参考文献：[＃2738](http://www.sqlalchemy.org/trac/ticket/2738)

-   **[sql] [bug] [reflection]**Fixed bug whereby using
    [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
    across a remote schema as well as a local schema could produce wrong
    results in the case where both schemas had a table of the same
    name.[¶](#change-d7e911a245c7336acac6b0361173f15a)

    参考文献：[＃2728](http://www.sqlalchemy.org/trac/ticket/2728)

-   **[sql] [bug]**删除了来自基类[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")类的“未实现”`__iter__()`调用，而这是在0.8中引入的。
    0，以防止在自定义运算符上实现`__getitem__()`方法，然后在该对象上错误地调用`list()`时出现无限的内存增长循环，导致列元素报告它们实际上是可迭代类型，当您尝试迭代时会抛出错误。没有真正的方式让双方都在这里，所以我们坚持使用Python的最佳实践。仔细在自定义运算符上实现`__getitem__()`！[¶](#change-3910b8156b7ae7cf1764d821698814b1)

    参考文献：[＃2726](http://www.sqlalchemy.org/trac/ticket/2726)

-   **[sql] [bug]
    [mssql]**来自此票证的回归导致不支持的关键字“true”呈现，并添加了逻辑以将此转换为SQL服务器的1/0.
    [¶ t2 \>](#change-540edefe60898115a13643ede2e44b1a)

    参考文献：[＃2682](http://www.sqlalchemy.org/trac/ticket/2682)

### 的PostgreSQL [¶ T0\>](#change-0.8.2-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**已添加对Postgresql
    9.2范围类型的支持。目前，没有提供类型转换，因此目前可以直接使用字符串或psycopg2
    2.5范围扩展类型。补丁礼貌Chris
    Withers。[¶](#change-520bac22f84f0ff81834e864a18c0232)

-   **[postgresql] [feature]**在使用psycopg2
    DBAPI时增加了对“AUTOCOMMIT”隔离的支持。该关键字可通过`isolation_level`执行选项使用。Pope礼貌Roman
    Podolyaka。[¶](#change-034ec567135f8813432798919e6a23ca)

    参考文献：[＃2072](http://www.sqlalchemy.org/trac/ticket/2072)

-   **[postgresql] [bug]**The behavior of [`extract()`](core_sqlelement.html#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")
    has been simplified on the Postgresql dialect to no longer inject a
    hardcoded `::timestamp` or similar cast into the
    given expression, as this interfered with types such as
    timezone-aware datetimes, but also does not appear to be at all
    necessary with modern versions of
    psycopg2.[¶](#change-7399d179ac6fd37c6153e7ba13dda7a9)

    参考文献：[＃2740](http://www.sqlalchemy.org/trac/ticket/2740)

-   **[postgresql] [bug]**Fixed bug in HSTORE type where keys/values
    that contained backslashed quotes would not be escaped correctly
    when using the “non native” (i.e. non-psycopg2) means of translating
    HSTORE data. 补丁由Ryan
    Kelly提供。[¶](#change-ebde2a412e8b54710edc830176e62656)

    参考文献：[＃2766](http://www.sqlalchemy.org/trac/ticket/2766)

-   **[postgresql]
    [bug]**修复了多列Postgresql索引中的列顺序将以错误顺序反映的错误。Courtesy
    Roman Podolyaka。[¶](#change-6d5da1fd63ce10ba7318dca30d36544c)

    参考文献：[＃2767](http://www.sqlalchemy.org/trac/ticket/2767)

-   **[postgresql]
    [bug]**修复了HSTORE类型以正确编码/解码unicode。这一直是开启的，因为hstore是一个文本类型，并且在使用Python
    3时与psycopg2的行为相匹配。礼貌德米特里Mugtasimov。[¶](#change-6badd661ef2ad66c13d5727dd91baf62)

    参考文献：[＃2735](http://www.sqlalchemy.org/trac/ticket/2735)，[请求github：2](https://github.com/zzzeek/sqlalchemy/pull/2)

### MySQL的[¶ T0\>](#change-0.8.2-mysql "Permalink to this headline")

-   **[mysql] [feature]**The `mysql_length`
    parameter used with [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    can now be passed as a dictionary of column names/lengths, for use
    with composite indexes. 非常感谢Roman
    Podolyaka提供的补丁。[¶](#change-449491292fcd4f1aff83eaa0524f783f)

    参考文献：[＃2704](http://www.sqlalchemy.org/trac/ticket/2704)

-   **[mysql] [bug]**Fixed bug when using multi-table UPDATE where a
    supplemental table is a SELECT with its own bound parameters, where
    the positioning of the bound parameters would be reversed versus the
    statement itself when using MySQL’s special
    syntax.[¶](#change-a6e3228b98f64879f8cc5e7d941870a6)

    参考文献：[＃2768](http://www.sqlalchemy.org/trac/ticket/2768)

-   **[mysql] [bug]**为`mysql+gaerdbms`方言添加了另一个条件，用于检测所谓的“开发”模式，我们应该使用`rdbms_mysqldb`补丁礼貌Brett
    Slatkin。[¶](#change-80436389fb1012b0dec8f741ede49f6e)

    参考文献：[＃2715](http://www.sqlalchemy.org/trac/ticket/2715)

-   **[mysql] [bug]**The `deferrable` keyword
    argument on [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    and [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    will not render the `DEFERRABLE` keyword on the
    MySQL dialect.
    很长一段时间，我们放弃了这一点，因为不可延迟的外键与延迟的外键的行为不同，但有些环境只是禁用MySQL上的FK，所以我们在这里不会引起注意。[t0
    \>](#change-abda9a524f74a360af54e6a281537062)

    参考文献：[＃2721](http://www.sqlalchemy.org/trac/ticket/2721)

-   **[mysql]
    [bug]**更新mysqlconnector方言，根据异常中发送的明显字符串消息检查断开连接；针对mysqlconnector
    1.0.9进行了测试。[¶](#change-21da2a634f095070d6fc59a7e9ed8ff6)

### 源码[¶ T0\>](#change-0.8.2-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**将[`sqlalchemy.types.BIGINT`](core_type_basics.html#sqlalchemy.types.BIGINT "sqlalchemy.types.BIGINT")添加到可以通过SQLite方言反映的类型名称列表；礼貌罗素斯图尔特。[¶](#change-df893c816a04361e8ac3efbae7be0245)

    参考文献：[＃2764](http://www.sqlalchemy.org/trac/ticket/2764)

### MSSQL [¶ T0\>](#change-0.8.2-mssql "Permalink to this headline")

-   当在SQL Server
    2000上查询信息模式时，删除了在0.8.1中添加的CAST调用，以帮助解决驱动程序问题，这在2000年显然不兼容。**[mssql]
    [bug]**CAST保持适用于SQL Server
    2005及更高版本。[¶](#change-099b8a881a2fa57ff216a0199b78b136)

    参考文献：[＃2747](http://www.sqlalchemy.org/trac/ticket/2747)

### 火鸟[¶ T0\>](#change-0.8.2-firebird "Permalink to this headline")

-   **[firebird]
    [feature]**为kinterbasdb和fdb方言添加了新的标志`retaining=True`。这将控制发送到DBAPI连接的`commit()`和`rollback()`方法的`retaining`标志的值。由于历史原因，该标志在0.8.2中默认为`True`，但在0.9.0b1中，该标志默认为`False`。[¶](#change-69c1d3c5f9d948061e45bd3047fada44)

    参考文献：[＃2763](http://www.sqlalchemy.org/trac/ticket/2763)

-   **[firebird] [bug]**Type lookup when reflecting the Firebird types
    LONG and INT64 has been fixed so that LONG is treated as INTEGER,
    INT64 treated as BIGINT, unless the type has a “precision” in which
    case it’s treated as NUMERIC. Patch courtesy Russell
    Stuart。[¶](#change-8ec28bdf32933102eee189870c53897d)

    参考文献：[＃2757](http://www.sqlalchemy.org/trac/ticket/2757)

### 杂项[¶ T0\>](#change-0.8.2-misc "Permalink to this headline")

-   **[bug] [ext]**Fixed bug whereby if a composite type were set up
    with a function instead of a class, the mutable extension would trip
    up when it tried to check that column for being a
    [`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
    (which it isn’t).
    礼貌asldevi。[¶](#change-0a42d6a1f8163b19a30432f19fb736df)

-   **[bug] [examples]**Fixed an issue with the “versioning” recipe
    whereby a many-to-one reference could produce a meaningless version
    for the target, even though it was not changed, when backrefs were
    present. 补丁由Matt
    Chisholm提供。[¶](#change-ddb41e891832626d10e5a7619ddf6ab6)

-   **[bug] [examples]**Fixed a small bug in the dogpile example where
    the generation of SQL cache keys wasn’t applying deduping labels to
    the statement the same way [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    normally does.[¶](#change-15c9f4b96d85015500733b401d2d49ee)

-   **[requirements]**现在需要Python
    [mock](https://pypi.python.org/pypi/mock)库来运行单元测试套件。作为Python
    3.3的标准库的一部分，以前的Python安装将需要安装它，以便运行单元测试或使用外部方言的`sqlalchemy.testing`包。[T2\>](#change-b870fcaa80c275cd3aeaa0ba3d5ecdd2)

0.8.1 [¶ T0\>](#change-0.8.1 "Permalink to this headline")
----------------------------------------------------------

发布日期：2013年4月27日

### ORM [¶ T0\>](#change-0.8.1-orm "Permalink to this headline")

-   **[orm] [feature]**Added a convenience method to Query that turns a
    query into an EXISTS subquery of the form
    `EXISTS (SELECT 1 FROM ... WHERE ...)`.[¶](#change-538cfca74b737d41cffcf811beddd163)

    参考文献：[＃2673](http://www.sqlalchemy.org/trac/ticket/2673)

-   **[orm] [bug]**Fixed bug when a query of the form:
    `query(SubClass).options(subqueryload(Baseclass.attrname))`, where `SubClass` is a joined inh of
    `BaseClass`, would fail to apply the
    `JOIN` inside the subquery on the attribute
    load, producing a cartesian product.
    填充的结果仍然是正确的，因为额外的行只是被忽略了，所以这个问题可能会出现在应用程序正常工作时性能下降。[¶](#change-a85f346f7c5a45a6ec0bda0e5e3c792e)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2699](http://www.sqlalchemy.org/trac/ticket/2699)

-   **[orm] [bug]**Fixed bug in unit of work whereby a
    joined-inheritance subclass could insert the row for the “sub” table
    before the parent table, if the two tables had no ForeignKey
    constraints set up between
    them.[¶](#change-33f72d18d004e2a614dd358f917e6949)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2689](http://www.sqlalchemy.org/trac/ticket/2689)

-   **[orm] [bug]**Fixes to the `sqlalchemy.ext.serializer` extension, including that the “id” passed from the pickler
    is turned into a string to prevent against bytes being parsed on
    Py3K, as well as that `relationship()` and
    `orm.join()` constructs are now properly
    serialized.[¶](#change-6b5abc76b93639e02dbac6061c8b93ff)

    参考文献：[＃2698](http://www.sqlalchemy.org/trac/ticket/2698)

-   **[orm] [bug]**A significant improvement to the inner workings of
    query.join(), such that the decisionmaking involved on how to join
    has been dramatically simplified.
    现在，新的测试用例通过了多个连接，这些连接从已经复杂的一系列涉及继承等的连接中延伸出来。从深度嵌套的子查询结构中加入仍然很复杂，并非没有警告，但通过这些改进，边缘案例有望被推到更远的边缘。[¶](#change-b8cd50e1714b608fa9a53cb51fb4c8ef)

    参考文献：[＃2714](http://www.sqlalchemy.org/trac/ticket/2714)

-   **[orm] [bug]**Added a conditional to the unpickling process for ORM
    mapped objects, such that if the reference to the object were lost
    when the object was pickled, we don’t erroneously try to set up
    \_sa\_instance\_state - fixes a NoneType
    error.[¶](#change-c9e76122e927bce00034de429959dcbc)

-   **[orm] [bug]**Fixed bug where many-to-many relationship with
    uselist=False would fail to delete the association row and raise an
    error if the scalar attribute were set to None.
    这是由[＃2229](http://www.sqlalchemy.org/trac/ticket/2229)。[¶](#change-693cd23b4e1f3a578dceac48c89c5508)更改引入的回归。

    参考文献：[＃2710](http://www.sqlalchemy.org/trac/ticket/2710)

-   **[orm]
    [bug]**改进了在Session内创建强引用的实例管理行为；如果对象处于过渡状态或进入分离状态，对象将不再创建内部引用循环
    -
    仅当对象连接到会话时才会创建强引用，并在分离对象时将其删除。这使得对象拥有一个\_\_
    del
    \_\_()方法更为安全，尽管不推荐这样做，因为与backrefs的关系也会产生循环。当带有\_\_
    del
    \_\_()方法的类被映射时，警告已被添加。[¶](#change-7addcdb8589d1b8db248e399c8eff53b)

    参考文献：[＃2708](http://www.sqlalchemy.org/trac/ticket/2708)

-   **[orm] [bug]**Fixed bug whereby ORM would run the wrong kind of
    query when refreshing an inheritance-mapped class where the
    superclass was mapped to a non-Table object, like a custom join() or
    a select(), running a query that assumed a hierarchy that’s mapped
    to individual
    Table-per-class.[¶](#change-f241aa4abf00fdb62f17b6161f0f1dc6)

    参考文献：[＃2697](http://www.sqlalchemy.org/trac/ticket/2697)

-   **[orm] [bug]**Fixed \_\_repr\_\_() on mapper property constructs to
    work before the object is initialized, so that Sphinx builds with
    recent Sphinx versions can read
    them.[¶](#change-cd903a647a5922f6bbc9db890e9f4304)

### orm declarative [¶](#change-0.8.1-orm-declarative "Permalink to this headline")

-   **[bug] [orm] [declarative]**Fixed indirect regression regarding
    [`has_inherited_table()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.has_inherited_table "sqlalchemy.ext.declarative.has_inherited_table"),
    where since it considers the current class’ `__table__`, was sensitive to when it was called.
    这也是0.7的行为，但在0.7中，事情倾向于在`__mapper_args__()`之类的事件中“解决”。[`has_inherited_table()`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.has_inherited_table "sqlalchemy.ext.declarative.has_inherited_table")现在只考虑超类，所以无论何时它被调用（显然假设超类的状态），都应该返回与当前类相同的答案。[¶](#change-2b9d746e218c78a250148a29ad1fef34)

    参考文献：[＃2656](http://www.sqlalchemy.org/trac/ticket/2656)

### SQL [¶ T0\>](#change-0.8.1-sql "Permalink to this headline")

-   **[sql]
    [feature]**松散检查传递给Table()的方言特定参数名称；因为我们想要支持外部方言，并且想要支持没有安装某种方言的参数，它现在只检查参数的格式，而不是在sqlalchemy.dialects中查找这种方言。[¶](#change-3686aff789b10fca55c71c0fe69557df)

-   **[sql] [bug] [mysql]**完全实现了IS和IS NOT运算符的True /
    False常量。An expression like `col.is_(True)`
    will now render `col IS true` on the target
    platform, rather than converting the True/ False constant to an
    integer bound parameter. 当给定True /
    False常量时，这允许`is_()`运算符在MySQL上工作。[¶](#change-a4d2a849342bd0b32b1a6f4a4c088ad6)

    参考文献：[＃2682](http://www.sqlalchemy.org/trac/ticket/2682)

-   **[sql] [bug]**A major fix to the way in which a select() object
    produces labeled columns when apply\_labels() is used; this mode
    produces a SELECT where each column is labeled as in \_, to remove
    column name collisions for a multiple table select.
    解决的办法是，如果两个标签在与表名称相结合时发生碰撞，即“foo.bar\_id”和“foo\_bar.id”，匿名别名将应用于其中一个欺骗。这允许ORM独立处理两个列；以前，在某些情况下，0.7会在默认情况下为被“伪装”的列发出第二个SELECT，并且在0.8中会发出不明确的列错误。应用于.c的“键”。select()的集合也将被删除，以便“指定要替换的”警告不会再发出任何指定use\_labels的select()，尽管这个指定的密钥会被赋予一个匿名标签，友好。[¶
    T0\>](#change-e317ad63213b3197754a3d94f7507a58)

    参考文献：[＃2702](http://www.sqlalchemy.org/trac/ticket/2702)

-   **[sql]
    [bug]**修复了在Connection对象已经关闭后引发错误时断开连接检测错误会引发属性错误的问题。[¶](#change-1f28811ac556b12ce7c452b4a3408f2a)

    参考文献：[＃2691](http://www.sqlalchemy.org/trac/ticket/2691)

-   **[sql] [bug]**Reworked internal exception raises that emit a
    rollback() before re-raising, so that the stack trace is preserved
    from sys.exc\_info() before entering the rollback.
    这样当使用在回滚函数返回前可能已经切换上下文的协程框架时，回溯被保留。[¶](#change-18be80dfecdf0ef6fc3df9f795f45ad4)

    参考文献：[＃2703](http://www.sqlalchemy.org/trac/ticket/2703)

-   **[sql] [bug] [postgresql]**The \_Binary base type now converts
    values through the bytes() callable when run on Python 3; in
    particular psycopg2 2.5 with Python 3.3 seems to now be returning
    the “memoryview” type, so this is converted to bytes before
    return.[¶](#change-36fe44c142145d30fafc44b26a0b2de3)

-   **[sql]
    [bug]**改进了连接自动失效处理。如果发生非断开连接错误，但会导致错误处理中的延迟断开连接错误（发生在MySQL上），则会检测到断开连接条件。当处于无效状态时，连接现在也可以关闭，这意味着在下次使用时它会提升“关闭”，另外，即使错误处理例程中的自动回退失败，并且无论条件是否断开。[¶](#change-8f9807690202ed982e5ae96fe1e87a63)

    参考文献：[＃2695](http://www.sqlalchemy.org/trac/ticket/2695)

-   **[sql] [bug]**Fixed bug whereby a DBAPI that can return “0” for
    cursor.lastrowid would not function correctly in conjunction with
    [`ResultProxy.inserted_primary_key`{](core_connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key").[¶](#change-b320bbb422d328f3f84b0ac64d30eb7d)

### 的PostgreSQL [¶ T0\>](#change-0.8.1-postgresql "Permalink to this headline")

-   **[postgresql] [bug]**打开psycopg2 /
    libpq的“disconnect”检查以检查完整异常层次结构中的所有各种“断开”消息。具体来说，至少有三种不同的异常类型可以看到“意外关闭连接”消息。Courtesy
    Eli Collins。[¶](#change-f67787db3b9ef9d1cb3ccc779ae2d229)

    参考文献：[＃2712](http://www.sqlalchemy.org/trac/ticket/2712)

-   **[postgresql] [bug]** Postgresql
    ARRAY类型的运算符支持输入类型的集合，生成器等。即使未指定维度，也可以无条件地将给定的迭代转换为集合。[¶](#change-365654f1763bc018c6fea3d1adfe7f6d)

    参考文献：[＃2681](http://www.sqlalchemy.org/trac/ticket/2681)

-   **[postgresql]
    [bug]**添加缺少HSTORE类型到postgresql类型名称，以便可以反映类型。[¶](#change-78ea5cd647f43b14fbd184b6c51042bd)

    参考文献：[＃2680](http://www.sqlalchemy.org/trac/ticket/2680)

### MySQL的[¶ T0\>](#change-0.8.1-mysql "Permalink to this headline")

-   **[mysql] [bug]**修复了支持最新的cymysql DBAPI，礼貌Hajime
    Nakagami。[¶](#change-4793f92820e9c93f772dd33adee75002)

-   **[mysql] [bug]**改进了Python
    3上pymysql方言的操作，包括一些重要的解码/字节步骤。由于驱动程序问题，BLOB类型仍然存在问题。礼貌Ben
    Trofatter。[¶](#change-32eca569275c8c9405df1ae6e52e28a7)

    参考文献：[＃2663](http://www.sqlalchemy.org/trac/ticket/2663)

-   **[mysql]
    [bug]**更新了正则表达式，以正确提取谷歌应用引擎v1.7.5及更新版本的错误代码。礼貌Dan
    Ring。[¶](#change-ad0d195d23c8846439e6fa6093c16c37)

### MSSQL [¶ T0\>](#change-0.8.1-mssql "Permalink to this headline")

-   **[mssql] [bug]**Part of a longer series of fixes needed for pyodbc+
    mssql, a CAST to NVARCHAR(max) has been added to the bound parameter
    for the table name and schema name in all information schema queries
    to avoid the issue of comparing NVARCHAR to NTEXT, which seems to be
    rejected by the ODBC driver in some cases, such as FreeTDS (0.91
    only?) 加上传递的unicode绑定参数。这个问题似乎是特定于SQL
    Server信息架构表的，对于那些首先不存在问题的情况，解决方法是无害的。[¶](#change-577130fc7c7f3c64856c9b296fb83a6d)

    参考文献：[＃2355](http://www.sqlalchemy.org/trac/ticket/2355)

-   **[mssql]
    [bug]**增加了对pymssql方言附加“断开连接”消息的支持。礼貌John
    Anderson。[¶](#change-7f3aa37006984fd02c41a09398143685)

-   **[mssql] [bug]**修正了关于“binary”类型和pymssql的Py3K错误。感谢Marc
    Abramowitz。[¶](#change-b830f432c4ee6d47eefab9bd9b667c3f)

    参考文献：[＃2683](http://www.sqlalchemy.org/trac/ticket/2683)

### 杂项[¶ T0\>](#change-0.8.1-misc "Permalink to this headline")

-   **[bug]
    [examples]**修复了缓存示例中长期存在的一个bug，其中在计算缓存键时，不会考虑limit
    /
    offset参数值。\_key\_from\_query()函数被简化为直接从最终编译语句开始工作，以便获得完整语句以及完全处理的参数列表。[¶](#change-b873d75029d2d99647c05b161cb0c2c6)

0.8.0 [¶ T0\>](#change-0.8.0 "Permalink to this headline")
----------------------------------------------------------

发布日期：2013年3月9日

注意

在0.8.0b2中不存在0.8.0的一些新的行为变化。它们出现在移民文件中如下：

-   [The consideration of a “pending” object as an “orphan” has been
    made more aggressive](migration_08.html#legacy-is-orphan-addition)
-   [create\_all() and drop\_all() will now honor an empty list as
    such](migration_08.html#metadata-create-drop-tables)
-   [Correlation is now always
    context-specific](migration_08.html#correlation-context-specific)

### ORM [¶ T0\>](#change-0.8.0-orm "Permalink to this headline")

-   **[orm] [feature]**A meaningful [`QueryableAttribute.info`](orm_internals.html#sqlalchemy.orm.attributes.QueryableAttribute.info "sqlalchemy.orm.attributes.QueryableAttribute.info")
    attribute is added, which proxies down to the `.info` attribute on either the [`schema.Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object if directly present, or the [`MapperProperty`](orm_internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")
    otherwise.
    完整的行为通过测试记录并确保其保持稳定。[¶](#change-0e7766217e564a69e3b6e7d65324ee7e)

    参考文献：[＃2675](http://www.sqlalchemy.org/trac/ticket/2675)

-   **[orm] [feature]**可以在[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")构造已经构建之后设置/更改“级联”属性。这不是正常使用的模式，但我们希望在教程中更改设置以便演示。[¶](#change-eff531fde0b0d3b8012f08ac5f1465c8)

-   **[orm] [feature]**Added new helper function [`was_deleted()`](orm_session_api.html#sqlalchemy.orm.util.was_deleted "sqlalchemy.orm.util.was_deleted"),
    returns True if the given object was the subject of a
    [`Session.delete()`](orm_session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")
    operation.[¶](#change-87e254a9ea3dc3d97f95489d3aaaec97)

    参考文献：[＃2658](http://www.sqlalchemy.org/trac/ticket/2658)

-   **[orm] [feature]**扩展了[*Runtime Inspection
    API*](core_inspection.html)系统，以便可以检索与ORM或其扩展相关联的所有Python描述符。这满足了除了[`hybrid_property`](orm_extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")和[`AssociationProxy`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")之类的扩展类型之外，还能够检查所有[`QueryableAttribute`](orm_internals.html#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")描述符的常见要求。参见[`Mapper.all_orm_descriptors`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")。[¶](#change-6dc63e609423ac03130a8b69d1f641ad)

-   **[orm] [removed]**The undocumented (and hopefully unused) system of
    producing custom collections using an
    `__instrumentation__` datastructure associated
    with the collection has been removed, as this was a complex and
    untested feature which was also essentially redundant versus the
    decorator approach.
    对orm.collections模块的其他内部简化也已完成。[¶](#change-29886b5ee0c5aaede3ccba82d95b9db9)

-   **[orm]
    [bug]**改进了在映射器配置期间检查现有后端名称冲突的情况；现在将测试超类和子类名称冲突，除了当前的映射器，因为这些冲突同样会破坏事物。这是0.8的新功能，但请参阅下面的警告，该警告也将在0.7.11中触发。[¶](#change-70a1eb7113723617f2545f787b42926f)

    参考文献：[＃2674](http://www.sqlalchemy.org/trac/ticket/2674)

-   **[orm] [bug]**Improved the error message emitted when a “backref
    loop” is detected, that is when an attribute event triggers a
    bidirectional assignment between two other attributes with no end.
    这种情况不仅发生在分配了错误类型的对象时，而且当某个属性被错误地配置为反向引用到现有的backref对时。也在0.7.11.
    [¶](#change-3300e27b920eae11534316a004610e0b)

    参考文献：[＃2674](http://www.sqlalchemy.org/trac/ticket/2674)

-   **[orm] [bug]**A warning is emitted when a MapperProperty is
    assigned to a mapper that replaces an existing property, if the
    properties in question aren’t plain column-based properties.
    关系属性的替换很少（从来没有？）意图是什么，通常是指映射器错误配置。也在0.7.11.
    [¶](#change-451e4047465f0e6c6f21abba4b12df50)

    参考文献：[＃2674](http://www.sqlalchemy.org/trac/ticket/2674)

-   **[orm] [bug]**A clear error message is emitted if an event handler
    attempts to emit SQL on a Session within the after\_commit()
    handler, where there is not a viable transaction in
    progress.[¶](#change-d2bf87eacf9c1add55e6572d7d34ee88)

    参考文献：[＃2662](http://www.sqlalchemy.org/trac/ticket/2662)

-   **[orm]
    [bug]**在级联自然主键更新的过程中检测到主键更改将成功，即使键是复合的并且只有部分属性发生更改[¶
    T2\>](#change-cc99daa35226bc12290009d2ecd52ada)

    参考文献：[＃2665](http://www.sqlalchemy.org/trac/ticket/2665)

-   **[orm]
    [bug]**在事务提交后，从会话中删除的对象将完全与该会话关联，即[`object_session()`](orm_session_api.html#sqlalchemy.orm.session.object_session "sqlalchemy.orm.session.object_session")函数将会返回None。[¶](#change-0a139e7ac1f999ad55e5825206c80ac6)

    参考文献：[＃2658](http://www.sqlalchemy.org/trac/ticket/2658)

-   **[orm] [bug]**Fixed bug whereby [`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")
    would set the execution options incorrectly, thereby breaking
    subsequent usage of the [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")
    method. 礼貌Ryan
    Kelly。[¶](#change-1d26b29a64556c35cdb8d59224b641f9)

    参考文献：[＃2661](http://www.sqlalchemy.org/trac/ticket/2661)

-   **[orm] [bug]**Fixed the consideration of the `between()` operator so that it works correctly with the new
    relationship local/remote
    system.[¶](#change-f0fdbb71e66a3cb345017c0e32a9dfcc)

    参考文献：[＃1768](http://www.sqlalchemy.org/trac/ticket/1768)

-   **[orm] [bug]**the consideration of a pending object as an “orphan”
    has been modified to more closely match the behavior as that of
    persistent objects, which is that the object is expunged from the
    [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    as soon as it is de-associated from any of its orphan-enabled
    parents.
    以前，挂起的对象只有在与所有孤立启用的父母关联时才会被清除。新标志`legacy_is_orphan`被添加到[`orm.mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")中，以重新建立传统行为。

    请参阅[The consideration of a “pending” object as an “orphan” has
    been made more
    aggressive](migration_08.html#legacy-is-orphan-addition)，以便详细讨论此更改。

    [¶](#change-e10fe28bb6aac9740cefe7a351f6bc84)

    参考文献：[＃2655](http://www.sqlalchemy.org/trac/ticket/2655)

-   **[orm] [bug]**Fixed the (most likely never used) “@collection.link”
    collection method, which fires off each time the collection is
    associated or de-associated with a mapped object - the decorator was
    not tested or functional.
    装饰器方法现在名为[`collection.linker()`](orm_collections.html#sqlalchemy.orm.collections.collection.linker "sqlalchemy.orm.collections.collection.linker")，尽管名称“link”保持向后兼容。礼貌Luca
    Wehrstedt。[¶](#change-7d72bd6c360c99b27ef15047489fcd85)

    参考文献：[＃2653](http://www.sqlalchemy.org/trac/ticket/2653)

-   **[orm] [bug]**Made some fixes to the system of producing custom
    instrumented collections, mainly that the usage of the @collection
    decorators will now honor the \_\_mro\_\_ of the given class,
    applying the logic of the sub-most classes’ version of a particular
    collection method.
    以前，当对现有的工具类（如[`MappedCollection`](orm_collections.html#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")）进行子类化时，无论自定义方法是否可以正确解析，都是不可预测的。[](#change-bd06b03d181458a8e51b61251f490b82)

    参考文献：[＃2654](http://www.sqlalchemy.org/trac/ticket/2654)

-   **[orm] [bug]**修复了创建任意数量的[`sessionmaker`](orm_session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")对象时可能发生的内存泄漏。由sessionmaker创建的匿名子类在取消引用时不会被垃圾收集，因为事件包中剩余的类级别引用。此问题也适用于任何使用ad-hoc子类与事件分派器结合使用的自定义系统。同样在0.7.10.
    [¶](#change-5bc655fd335b2e5ce6043db01e7e0070)

    参考文献：[＃2650](http://www.sqlalchemy.org/trac/ticket/2650)

-   **[orm] [bug]**[`Query.merge_result()`](orm_query.html#sqlalchemy.orm.query.Query.merge_result "sqlalchemy.orm.query.Query.merge_result")
    can now load rows from an outer join where an entity may be
    `None` without throwing an error. 同样在0.7.10.
    [¶](#change-89cccd82c603a3ec57c6fd0dd77dce2f)

    参考文献：[＃2640](http://www.sqlalchemy.org/trac/ticket/2640)

-   **[orm] [bug]**Fixes to the “dynamic” loader on
    [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
    includes that backrefs will work properly even when autoflush is
    disabled, history events are more accurate in scenarios where
    multiple add/remove of the same object
    occurs.[¶](#change-30c07492fc86836cb428a07cb6a8c472)

    参考文献：[＃2637](http://www.sqlalchemy.org/trac/ticket/2637)

### SQL [¶ T0\>](#change-0.8.0-sql "Permalink to this headline")

-   **[sql] [feature]**Added a new argument to [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    and its base [`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    `inherit_schema`. 当设置为`True`时，该类型将设置与其相关联的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的`schema`属性。这也发生在[`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")操作中；在[`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")发生的情况下，现在[`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")被复制，并且如果`inherit_schema=True`，类型将采用新模式名称传递给方法。The `schema` is important when used with the Postgresql backend, as the
    type results in a `CREATE TYPE`
    statement.[¶](#change-aacb4e3939dfad091a7dc16bfbafa28d)

    参考文献：[＃2657](http://www.sqlalchemy.org/trac/ticket/2657)

-   **[sql] [feature]**[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    now supports arbitrary SQL expressions and/or functions, in addition
    to straight columns. Common modifiers include using
    `somecolumn.desc()` for a descending index and
    `func.lower(somecolumn)` for a case-insensitive
    index, depending on the capabilities of the target
    backend.[¶](#change-4a5b1d5566fb9e0e9cea5fc5b37a9779)

    参考文献：[＃695](http://www.sqlalchemy.org/trac/ticket/695)

-   **[sql] [bug]**The behavior of SELECT correlation has been improved
    such that the [`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")
    and [`Select.correlate_except()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")
    methods, as well as their ORM analogues, will still retain
    “auto-correlation” behavior in that the FROM clause is modified only
    if the output would be legal SQL; that is, the FROM clause is left
    intact if the correlated SELECT is not used in the context of an
    enclosing SELECT inside of the WHERE, columns, or HAVING clause.
    这两种方法现在只将条件指定为默认的“自动关联”，而不是绝对的FROM列表。[¶](#change-6a4406900f98dc286816c64340267f5e)

    参考文献：[＃2668](http://www.sqlalchemy.org/trac/ticket/2668)

-   **[sql] [bug]**Fixed a bug regarding column annotations which in
    particular could impact some usages of the new [`orm.remote()`](orm_relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")
    and `orm.local()` annotation
    functions, where annotations could be lost when the column were used
    in a subsequent
    expression.[¶](#change-f4a089a10d8ca4d92ed313869806e9c1)

    参考文献：[＃1768](http://www.sqlalchemy.org/trac/ticket/1768)，[＃2660](http://www.sqlalchemy.org/trac/ticket/2660)

-   **[sql] [bug]**The [`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
    operator will now coerce values of `None` to
    [`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null").[¶](#change-737388761f92767bc0e26a80c98df139)

    参考文献：[＃2496](http://www.sqlalchemy.org/trac/ticket/2496)

-   **[sql] [bug]**Fixed bug where [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    would fail if a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    had both a foreign key as well as an alternate ”.key” name for the
    column. 同样在0.7.10. [¶](#change-88b4c4ede70d2e60146fa8c717f87544)

    参考文献：[＃2643](http://www.sqlalchemy.org/trac/ticket/2643)

-   **[sql] [bug]**insert().returning() raises an informative
    CompileError if attempted to compile on a dialect that doesn’t
    support RETURNING.[¶](#change-0ed8c15f1a7de2b4ffd2e65c7538bdf4)

    参考文献：[＃2629](http://www.sqlalchemy.org/trac/ticket/2629)

-   **[sql] [bug]**Tweaked the “REQUIRED” symbol used by the compiler to
    identify INSERT/UPDATE bound parameters that need to be passed, so
    that it’s more easily identifiable when writing custom bind-handling
    code.[¶](#change-4e171b865fa50628413956ff3159317b)

    参考文献：[＃2648](http://www.sqlalchemy.org/trac/ticket/2648)

### 架构[¶ T0\>](#change-0.8.0-schema "Permalink to this headline")

-   **[schema] [bug]**[`MetaData.create_all()`](core_metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
    and [`MetaData.drop_all()`](core_metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")
    will now accommodate an empty list as an instruction to not
    create/drop any items, rather than ignoring the
    collection.[¶](#change-ae2a49c7e02214659343b36e72c31470)

    参考文献：[＃2664](http://www.sqlalchemy.org/trac/ticket/2664)

### 的PostgreSQL [¶ T0\>](#change-0.8.0-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**Added support for Postgresql’s traditional
    SUBSTRING function syntax, renders as “SUBSTRING(x FROM y FOR z)”
    when regular `func.substring()` is used.
    Courtesy
    GunnlaugurÞórBriem。[¶](#change-32b040acc96cd80d58b6b4f3180b753b)

    This change is also **backported** to: 0.7.11

    参考文献：[＃2676](http://www.sqlalchemy.org/trac/ticket/2676)

-   **[postgresql]
    [feature]**添加了`postgresql.ARRAY.Comparator.any()`和`postgresql.ARRAY.Comparator.all()`方法，以及独立的表达结构。非常感谢AudriusKažukauskas在这里的出色工作。[¶](#change-225a80e716cad9649123dc76e809d59b)

-   **[postgresql] [bug]**Fixed bug in [`array()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")
    construct whereby using it inside of an [`expression.insert()`](core_dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")
    construct would produce an error regarding a parameter issue in the
    `self_group()`
    method.[¶](#change-3adae518c55ff0255fefd5d431ef4a80)

### MySQL的[¶ T0\>](#change-0.8.0-mysql "Permalink to this headline")

-   **[mysql] [feature]**添加了新的CyMySQL方言，由Hajime
    Nakagami提供[¶](#change-40fad96aac576545c0bcd7b6aaae7df4)

-   **[mysql] [feature]** GAE方言现在接受URL中的用户名/密码参数，由Owen
    Nelson提供[¶](#change-48dd3fb7a18df48d86387567167547c6)

-   **[mysql] [bug] [gae]**为`gaerdbms`方言添加了条件导入，它试图导入rdbms\_apiproxy与rdbms\_googleapi以在开发平台和生产平台上工作。现在也尊重`instance`属性。Courtesy Sean Lynch。同样在0.7.10.
    [¶](#change-53062d4818f1d30f474a193f24789f87)

    参考文献：[＃2649](http://www.sqlalchemy.org/trac/ticket/2649)

-   **[mysql]
    [bug]**如果错误代码无法从异常抛出中提取，则GAE方言不会失败；礼貌Owen
    Nelson。[¶](#change-99ff63b4d0d6fe8559114e5d7176cfb1)

### MSSQL [¶ T0\>](#change-0.8.0-mssql "Permalink to this headline")

-   **[mssql] [feature]**Added `mssql_include` and
    `mssql_clustered` options to [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index"),
    renders the `INCLUDE` and `CLUSTERED` keywords, respectively. Courtesy Derek
    Harland。[¶](#change-1569da9a13f31f585e340e65a8754534)

-   **[mssql] [feature]**DDL for IDENTITY columns is now supported on
    non-primary key columns, by establishing a [`Sequence`](core_defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")
    construct on any integer column. Courtesy Derek
    Harland。[¶](#change-deae19d4bb2ad7bbeee44fa1f771d04c)

    参考文献：[＃2644](http://www.sqlalchemy.org/trac/ticket/2644)

-   **[mssql] [bug]**Added a py3K conditional around unnecessary
    .decode() call in mssql information schema, fixes reflection in
    Py3K. 同样在0.7.10. [¶](#change-99e9dd9a91aef22f4413c883adc1dc7c)

    参考文献：[＃2638](http://www.sqlalchemy.org/trac/ticket/2638)

-   **[mssql]
    [bug]**修复了字符类型CHAR，NCHAR等的“校对”参数的回归停止工作，因为基本字符串类型现在支持“整理”。MSSQL方言中的TEXT，NCHAR，CHAR，VARCHAR类型现在是基本类型的同义词。[¶](#change-a64f093c2a0a7670b2dbd000e77e230c)

### 预言[¶ T0\>](#change-0.8.0-oracle "Permalink to this headline")

-   **[oracle] [bug]** cx\_oracle方言将不再通过`encode()`运行绑定参数名称，因为这在Python
    3中无效，并且阻止了语句的运行正确使用Python
    3。我们现在只在`supports_unicode_binds`为False的情况下进行编码，至少在使用cx\_oracle的版本5时cx\_oracle不是这种情况。[¶](#change-2cc0979a478f094fa54a8b0019792ae9)

### 杂项[¶ T0\>](#change-0.8.0-misc "Permalink to this headline")

-   **[bug]
    [tests]**修复了test\_execute中的“日志记录”导入问题，该问题在某些Linux平台上不起作用。也在0.7.11.
    [¶](#change-3c5bac377a13b20bf0772508894cbe60)

    参考文献：[＃2669](http://www.sqlalchemy.org/trac/ticket/2669)

-   **[bug] [examples]**Fixed a regression in the
    examples/dogpile\_caching example which was due to the change in
    [\#2614](http://www.sqlalchemy.org/trac/ticket/2614).[¶](#change-5e896a6fed3501b6f3e9ee0f8e580fdc)

0.8.0b2 [¶ T0\>](#change-0.8.0b2 "Permalink to this headline")
--------------------------------------------------------------

发布时间：2012年12月14日

### ORM [¶ T0\>](#change-0.8.0b2-orm "Permalink to this headline")

-   **[orm] [feature]**Added [`KeyedTuple._asdict()`](orm_query.html#sqlalchemy.util.KeyedTuple._asdict "sqlalchemy.util.KeyedTuple._asdict")
    and [`KeyedTuple._fields`](orm_query.html#sqlalchemy.util.KeyedTuple._fields "sqlalchemy.util.KeyedTuple._fields")
    to the [`KeyedTuple`](orm_query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")
    class to provide some degree of compatibility with the Python
    standard library `collections.namedtuple()`.[¶](#change-0440aa0e8373498cdeae16c5b150cb90)

    参考文献：[＃2601](http://www.sqlalchemy.org/trac/ticket/2601)

-   **[orm]
    [feature]**允许在为关系定义主要和次要连接时使用同义词。[¶](#change-cfadd6c030d66215e58af3ce677a864f)

-   **[orm] [feature] [extensions]**The [`sqlalchemy.ext.mutable`](orm_extensions_mutable.html#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")
    extension now includes the example [`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")
    class as part of the
    extension.[¶](#change-c6b226a6956872361404c4b013d44c5d)

-   **[orm] [bug]**The [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
    method can now be used with a [`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")
    construct without it interfering with the entities being selected.
    基本上，这样的陈述：

        ua = aliased(User)
        session.query(User.name).select_from(ua).join(User, User.name > ua.name)

    将保持SELECT的列子句作为来自未指定的“用户”，如指定的那样；
    select\_from只发生在FROM子句中：

        SELECT users.name AS users_name FROM users AS users_1
        JOIN users ON users.name < users_1.name

    请注意，此行为与[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")的原始较旧用例形成对比，这是使用不同的可选项重新表示映射实体的情况：

        session.query(User.name).\
          select_from(user_table.select().where(user_table.c.id > 5))

    其中产生：

        SELECT anon_1.name AS anon_1_name FROM (SELECT users.id AS id,
        users.name AS name FROM users WHERE users.id > :id_1) AS anon_1

    后一个用例的“别名”行为阻碍了前一个用例。该方法现在特别考虑像[`expression.select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")或[`expression.alias()`](core_selectable.html#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")这样的SQL表达式，与像[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")

    [¶](#change-8d958f76ee47f7155365772401087d1f)

    参考文献：[＃2635](http://www.sqlalchemy.org/trac/ticket/2635)

-   **[orm] [bug]**The [`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
    type did not allow for the [`MutableBase.coerce()`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")
    method to be used, even though the code seemed to indicate this
    intent, so this now works and a brief example is added.
    作为一个副作用，这个事件处理程序的机制已经改变，所以新的[`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")类型不再添加每个类型的全局事件处理程序。同样在0.7.10.
    [¶](#change-366b3ffffab4272d3ea9d5c58bc6bdaa)

    参考文献：[＃2624](http://www.sqlalchemy.org/trac/ticket/2624)

-   **[orm] [bug]**A second overhaul of aliasing/internal pathing
    mechanics now allows two subclasses to have different relationships
    of the same name, supported with subquery or joined eager loading on
    both simultaneously when a full polymorphic load is
    used.[¶](#change-64d3ae8c4166dd3b314fb1255ed2e4ed)

    参考文献：[＃2614](http://www.sqlalchemy.org/trac/ticket/2614)

-   **[orm] [bug]**Fixed bug whereby a multi-hop subqueryload within a
    particular with\_polymorphic load would produce a KeyError.
    利用与[＃2614](http://www.sqlalchemy.org/trac/ticket/2614)相同的内部路径检修。[¶](#change-e07c11d743d54ffa7ab235cbc3a58029)

    参考文献：[＃2617](http://www.sqlalchemy.org/trac/ticket/2617)

-   **[orm] [bug]**Fixed regression where query.update() would produce
    an error if an object matched by the “fetch” synchronization
    strategy wasn’t locally present. 感谢Scott
    Torborg。[¶](#change-c8eac4ae99fd0082c6ae42044cda7547)

    参考文献：[＃2602](http://www.sqlalchemy.org/trac/ticket/2602)

### 发动机[¶ T0\>](#change-0.8.0b2-engine "Permalink to this headline")

-   **[engine] [feature]**The [`Connection.connect()`](core_connections.html#sqlalchemy.engine.Connection.connect "sqlalchemy.engine.Connection.connect")
    and [`Connection.contextual_connect()`](core_connections.html#sqlalchemy.engine.Connection.contextual_connect "sqlalchemy.engine.Connection.contextual_connect")
    methods now return a “branched” version so that the
    [`Connection.close()`](core_connections.html#sqlalchemy.engine.Connection.close "sqlalchemy.engine.Connection.close")
    method can be called on the returned connection without affecting
    the original. 在使用[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象作为上下文管理器时允许对称：

        with conn.connect() as c: # leaves the Connection open
          c.execute("...")

        with engine.connect() as c:  # closes the Connection
          c.execute("...")

    [¶](#change-28a54006aa013faf00f812929e7c24f9)

-   **[engine] [bug]**Fixed [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
    to correctly use the given [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"),
    if given, without opening a second connection from that connection’s
    [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine").[¶](#change-77b9a2a46687b7655e2116a17db1353e)

    This change is also **backported** to: 0.7.10

    参考文献：[＃2604](http://www.sqlalchemy.org/trac/ticket/2604)

-   **[engine]**不推荐使用[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")的“reflect
    = True”参数。请使用[`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")方法。[¶](#change-3493b2118cfad669ab5817bd37983b18)

### SQL [¶ T0\>](#change-0.8.0b2-sql "Permalink to this headline")

-   **[sql] [feature]**The [`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
    construct now supports multi-valued inserts, that is, an INSERT that
    renders like “INSERT INTO table VALUES (...), (...), ...”.
    Postgresql，SQLite和MySQL支持。非常感谢Idan Kamara为此做了修改。

    也可以看看

    [Multiple-VALUES support for
    Insert](migration_08.html#feature-2623)的多个VALUES支持

    [¶](#change-ccda1d442536d0ccedacde3786a7a049)

    参考文献：[＃2623](http://www.sqlalchemy.org/trac/ticket/2623)

-   **[sql] [bug]**Fixed bug where using server\_onupdate= without
    passing the “for\_update=True” flag would apply the default object
    to the server\_default, blowing away whatever was there.
    明确的for\_update =
    True参数不应该与此用法一起使用（尤其是因为文档显示的示例没有使用它），因此现在使用给定的默认对象的副本在内部进行排列，如果该标志未设置为什么对应于这个参数。[¶](#change-9b15516022fbd264038c54ed46d7b9c9)

    This change is also **backported** to: 0.7.10

    参考文献：[＃2631](http://www.sqlalchemy.org/trac/ticket/2631)

-   **[sql] [bug]**Fixed a regression caused by
    [\#2410](http://www.sqlalchemy.org/trac/ticket/2410) whereby a
    [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    would apply itself back to the original table during a
    [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    operation, as it would parse the SQL expression for a parent table.
    该操作现在复制给定的表达式以对应新表。[¶](#change-6a9d7c37dc85bb3ae8b5101236afc248)

    参考文献：[＃2633](http://www.sqlalchemy.org/trac/ticket/2633)

-   **[sql] [bug]**Fixed bug whereby using a label\_length on dialect
    that was smaller than the size of actual column identifiers would
    fail to render the columns correctly in a SELECT
    statement.[¶](#change-52d00ac5ac3a16908d185a9b7a5979bc)

    参考文献：[＃2610](http://www.sqlalchemy.org/trac/ticket/2610)

-   **[sql] [bug]**The [`DECIMAL`](core_type_basics.html#sqlalchemy.types.DECIMAL "sqlalchemy.types.DECIMAL")
    type now honors the “precision” and “scale” arguments when rendering
    DDL.[¶](#change-d646ee623c01a51de03c5ab41dca6832)

    参考文献：[＃2618](http://www.sqlalchemy.org/trac/ticket/2618)

-   **[sql] [bug]**Made an adjustment to the “boolean”, (i.e.
    `__nonzero__`) evaluation of binary expressions,
    i.e. `x1 == x2`, such that the “auto-grouping”
    applied by [`BinaryExpression`](core_sqlelement.html#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")
    in some cases won’t get in the way of this comparison.
    以前，表达式如下所示：

        expr1 = mycolumn > 2
        bool(expr1 == expr1)

    Would evaluate as `False`, even though this is
    an identity comparison, because `mycolumn > 2`
    would be “grouped” before being placed into the
    [`BinaryExpression`](core_sqlelement.html#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression"),
    thus changing its identity. [`BinaryExpression`](core_sqlelement.html#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")
    now keeps track of the “original” objects passed in. Additionally
    the `__nonzero__` method now only returns if the
    operator is `==` or `!=` -
    all others raise `TypeError`.

    [¶](#change-3a51c5d14168a9eb00ee8360c4058315)

    参考文献：[＃2621](http://www.sqlalchemy.org/trac/ticket/2621)

-   **[sql] [bug]**Fixed a gotcha where inadvertently calling list() on
    a [`ColumnElement`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    would go into an endless loop, if
    [`ColumnOperators.__getitem__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__getitem__ "sqlalchemy.sql.operators.ColumnOperators.__getitem__")
    were implemented. 新的NotImplementedError通过`__iter__()`发出。[¶](#change-bf1c1943e4cb7d7f56b4a8bf06cb5460)

-   **[sql] [bug]**Fixed bug in type\_coerce() whereby typing
    information could be lost if the statement were used as a subquery
    inside of another statement, as well as other similar situations.
    除此之外，当Oracle /
    mssql方言应用限制/偏移量包装时，会导致输入信息丢失。[¶](#change-ebd2310b4e33e8f897da33a8c13a6afd)

    参考文献：[＃2603](http://www.sqlalchemy.org/trac/ticket/2603)

-   **[sql] [bug]**Fixed bug whereby the ”.key” of a Column wasn’t being
    used when producing a “proxy” of the column against a selectable.
    这可能不会发生在0.7版本中，因为0.7在更广泛的场景中并不尊重“.key”。[¶](#change-9f5dab3cd007a03e0d6c9ab38681ab97)

    参考文献：[＃2597](http://www.sqlalchemy.org/trac/ticket/2597)

### 的PostgreSQL [¶ T0\>](#change-0.8.0b2-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**[`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")
    is now available in the Postgresql dialect.
    如果有的话，也会使用psycopg2的扩展。Courtesy
    AudriusKažukauskas。[¶](#change-9d4ccc96c5c80a27fe89287588545998)

    参考文献：[＃2606](http://www.sqlalchemy.org/trac/ticket/2606)

### 源码[¶ T0\>](#change-0.8.0b2-sqlite "Permalink to this headline")

-   **[sqlite]
    [bug]**对0.7.9版本中发布的SQLite相关问题进行更多调整，以便在反映外键时拦截旧版SQLite引用字符。除了拦截双引号外，其他引号字符（如括号，反引号和单引号）现在也被拦截。[¶](#change-b60ca8c89667c3fd095716b23d5c82dc)

    This change is also **backported** to: 0.7.10

    参考文献：[＃2568](http://www.sqlalchemy.org/trac/ticket/2568)

### MSSQL [¶ T0\>](#change-0.8.0b2-mssql "Permalink to this headline")

-   **[mssql] [feature]**支持反映主键约束的“名称”，由Dave
    Moore提供[¶](#change-2cd1695c575daf74cad23ecb835cdd5c)

    参考文献：[＃2600](http://www.sqlalchemy.org/trac/ticket/2600)

-   **[mssql] [bug]**Fixed bug whereby using “key” with Column in
    conjunction with “schema” for the owning Table would fail to locate
    result rows due to the MSSQL dialect’s “schema rendering” logic’s
    failure to take .key into
    account.[¶](#change-b5408177e747087a3a191d706d2ac7e9)

    This change is also **backported** to: 0.7.10

### 预言[¶ T0\>](#change-0.8.0b2-oracle "Permalink to this headline")

-   **[oracle] [bug]**Fixed table reflection for Oracle when accessing a
    synonym that refers to a DBLINK remote database; while the syntax
    has been present in the Oracle dialect for some time, up until now
    it has never been tested.
    该语法已针对链接到自身的示例数据库进行了测试，但在查询远程数据库查找表信息时，对于“所有者”应该使用什么还存在一些不确定性。目前，来自user\_db\_links的“username”的值用于匹配“所有者”。[¶](#change-106aeb155ae3728a0c919c289e4726eb)

    参考文献：[＃2619](http://www.sqlalchemy.org/trac/ticket/2619)

-   **[oracle] [bug]**The Oracle LONG type, while an unbounded text
    type, does not appear to use the cx\_Oracle.LOB type when result
    rows are returned, so the dialect has been repaired to exclude LONG
    from having cx\_Oracle.LOB filtering applied. 同样在0.7.10.
    [¶](#change-ac22d47fb2190de7d5fdd45ea30d4bd0)

    参考文献：[＃2620](http://www.sqlalchemy.org/trac/ticket/2620)

-   **[oracle] [bug]**Repaired the usage of `.prepare()` in conjunction with cx\_Oracle so that a return value of
    `False` will result in no call to
    `connection.commit()`, hence avoiding “no
    transaction” errors.
    现在已经证明两阶段事务以SQLAlchemy和cx\_oracle的方式发挥作用，但是在驱动程序中观察到警告；检查文档的细节。同样在0.7.10.
    [¶](#change-cd9ec13cd0145a84de78a595fe61506f)

    参考文献：[＃2611](http://www.sqlalchemy.org/trac/ticket/2611)

### 火鸟[¶ T0\>](#change-0.8.0b2-firebird "Permalink to this headline")

-   **[firebird] [bug]**为实验性的“firebird +
    fdb”方言添加了“fdb”缺少的导入。[¶](#change-9ff9e7628c1d8b7060924fafe6844fe0)

    参考文献：[＃2622](http://www.sqlalchemy.org/trac/ticket/2622)

### 杂项[¶ T0\>](#change-0.8.0b2-misc "Permalink to this headline")

-   **[feature] [sybase]**反射支持已添加到Sybase方言中。非常感谢Ben
    Trofatter所做的所有开发和测试工作。[¶](#change-cf6d50791e201a7d553f5aa10db3cbdc)

    参考文献：[＃1753](http://www.sqlalchemy.org/trac/ticket/1753)

-   **[feature] [pool]**The [`Pool`](core_pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
    will now log all connection.close() operations equally, including
    closes which occur for invalidated connections, detached
    connections, and connections beyond the pool
    capacity.[¶](#change-960a01e29400ef086e01dfbfafb4913c)

-   **[feature] [pool]**The [`Pool`](core_pooling.html#sqlalchemy.pool.Pool "sqlalchemy.pool.Pool")
    now consults the [`Dialect`](core_internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
    for functionality regarding how the connection should be “auto
    rolled back”, as well as closed.
    这为事务范围赋予了方言的更多控制权，以便我们能够更好地实现像pysqlite和cx\_oracle可能需要的事务变通解决方法。[¶](#change-e08369ab111a8e4b26bc44e495aa0d46)

    参考文献：[＃2611](http://www.sqlalchemy.org/trac/ticket/2611)

-   **[feature] [pool]**添加新的[`PoolEvents.reset()`](core_events.html#sqlalchemy.events.PoolEvents.reset "sqlalchemy.events.PoolEvents.reset")挂钩以在连接自动回滚之前捕获该事件，然后返回到池。与[`ConnectionEvents.rollback()`](core_events.html#sqlalchemy.events.ConnectionEvents.rollback "sqlalchemy.events.ConnectionEvents.rollback")一起，这允许拦截所有回滚事件。[¶](#change-a71308c2787ff6db34f03853edf6dff2)

-   **[informix]**Some cruft regarding informix transaction handling has
    been removed, including a feature that would skip calling
    commit()/rollback() as well as some hardcoded isolation level
    assumptions on begin()..
    由于我们没有任何用户使用它，也没有任何对Informix数据库的访问，所以这种方言的地位还不是很清楚。如果有人访问Informix想要帮助测试这种方言，请告诉我们。[¶](#change-0f4be8723d2662b5128985703f1efe1b)

0.8.0b1 [¶ T0\>](#change-0.8.0b1 "Permalink to this headline")
--------------------------------------------------------------

发布时间：2012年10月30日

### 一般[¶ T0\>](#change-0.8.0b1-general "Permalink to this headline")

-   **[general]
    [removed]**完全移除“sqlalchemy.exc”的同义词。[¶](#change-5cdfbadad1d1ab8b583def86bfe1c3b8)

    参考文献：[＃2433](http://www.sqlalchemy.org/trac/ticket/2433)

-   **[general]** SQLAlchemy 0.8现在的目标是Python 2.5及更高版本。Python
    2.4不再支持。[¶](#change-5bd84bb0a379638a703e8d486a876539)

### ORM [¶ T0\>](#change-0.8.0b1-orm "Permalink to this headline")

-   **[orm] [feature]**Major rewrite of relationship() internals now
    allow join conditions which include columns pointing to themselves
    within composite foreign keys.
    添加了一个用于非常专业化的主连接条件的新API，允许基于SQL函数，CAST等的条件。通过在需要时将注释函数remote()和foreign()嵌入到表达式中进行处理。以前使用半私人\_local\_remote\_pairs方法的食谱可以升级为这种新方法。

    也可以看看

    [Rewritten relationship()
    mechanics](migration_08.html#feature-relationship-08)

    [¶](#change-2b5d7a236365a2a7ca5e6aca63d3dcad)

    参考文献：[＃1401](http://www.sqlalchemy.org/trac/ticket/1401)

-   **[orm] [feature]**New standalone function with\_polymorphic()
    provides the functionality of query.with\_polymorphic() in a
    standalone form.
    它可以应用于查询中的任何实体，包括作为连接的目标来代替“of\_type()”修饰符。[¶](#change-bfb5af4d4d7644b298d000311189fabd)

    参考文献：[＃2333](http://www.sqlalchemy.org/trac/ticket/2333)

-   **[orm] [feature]**The of\_type() construct on attributes now
    accepts aliased() class constructs as well as with\_polymorphic
    constructs, and works with query.join(), any(), has(), and also
    eager loaders subqueryload(), joinedload(),
    contains\_eager()[¶](#change-78a51fb9614f402a7225108f99846c70)

    参考文献：[＃1106](http://www.sqlalchemy.org/trac/ticket/1106)，[＃2438](http://www.sqlalchemy.org/trac/ticket/2438)

-   **[orm]
    [feature]**对映射类进行事件监听的改进允许为实例和映射器事件指定未映射的类。当propagate
    =
    True标志被传递时，已建立的事件将自动设置在该类的子类上，并且事件将在该类自身被最终映射时设置。[¶](#change-93ce3ef6116143e465e8824d6b1d1d77)

    参考文献：[＃2585](http://www.sqlalchemy.org/trac/ticket/2585)

-   **[orm]
    [feature]**使用新的DeferredReflection类，“延迟声明性反射”系统已移入声明性扩展本身。这个类现在用单个和连接表继承用例进行测试。[¶](#change-eb6e1bb92c5ceea0be162479d444103a)

    参考文献：[＃2485](http://www.sqlalchemy.org/trac/ticket/2485)

-   **[orm]
    [feature]**增加了新的核心函数“inspect()”，它作为一个通用的网关来映射到映射器，对象等等。Mapper和InstanceState对象已通过公共API进行了增强，该API允许检查映射属性，包括列绑定或关系绑定属性的过滤器，当前对象状态的检查，属性的历史记录等。[¶
    t0 \>](#change-5a3967b4ed8af452ab323aaa3b5d27f2)

    参考文献：[＃2208](http://www.sqlalchemy.org/trac/ticket/2208)

-   **[orm] [feature]**Calling rollback() within a
    session.begin\_nested() will now only expire those objects that had
    net changes within the scope of that transaction, that is objects
    which were dirty or were modified on a flush.
    这允许begin\_nested()的典型用例（修改对象的一小部分子集）将数据从未在该子事务中修改的较大的封闭对象集中留下。[T0\>](#change-1df6e3552ee895cd48952f95c0f0730a)

    参考文献：[＃2452](http://www.sqlalchemy.org/trac/ticket/2452)

-   **[orm]
    [feature]**增加了实用程序功能Session.enable\_relationship\_loading()，取代了relationship.load\_on\_pending。但是，这两个功能都应该避免。[¶](#change-42a29b97f3f04fca95c888b8ebb68802)

    参考文献：[＃2372](http://www.sqlalchemy.org/trac/ticket/2372)

-   **[orm]
    [feature]**增加了对column\_property()，relationship()，composite()的.info字典参数的支持。所有的MapperProperty类都有一个自动创建的.info字典。[¶](#change-d6ca8c5a4d9259ca52feb4e113633afe)

-   **[orm]
    [feature]**现在，从映射集合中添加/删除无将生成属性事件。以前，在某些情况下，无追加将被忽略。与。[¶](#change-9cbdee6462b2adb613d0260699424d93)相关

    参考文献：[＃2229](http://www.sqlalchemy.org/trac/ticket/2229)

-   **[orm]
    [feature]**在映射集合中存在None现在在刷新期间引发错误。以前，集合中的None值将被默默忽略。[¶](#change-dfe35810c91fadc80cc26fafc4758932)

    参考文献：[＃2229](http://www.sqlalchemy.org/trac/ticket/2229)

-   **[orm]
    [feature]**对于正在更新的表，Query.update()方法现在更加宽松。现在更好地支持Plain
    Table对象，并且update()；可以使用附加的继承子类。子类表将成为更新的目标，如果在WHERE子句中引用了父表，编译器将调用UPDATE..FROM语法，如方言所允许的，以满足WHERE子句。MySQL的多表更新功能也受支持，如果列在“值”字段中由对象指定。PG的DELETE..USING在Core中也不可用。[¶](#change-6849b5ad20a8f598c90e058f7406607e)

-   **[orm]
    [feature]**新会话事件after\_transaction\_create和after\_transaction\_end允许跟踪新的SessionTransaction对象。如果检查对象，可用于确定会话首次变为活动状态以及何时停用。[¶](#change-b6a88424dffec42d164fbc0e90fbd47d)

-   **[orm] [feature]**The Query can now load entity/scalar-mixed
    “tuple” rows that contain types which aren’t hashable, by setting
    the flag “hashable=False” on the corresponding TypeEngine object in
    use.
    返回不可互换类型（通常为列表）的自定义类型可以将此标志设置为False。[¶](#change-8da279230401738c29fde56b8e12e329)

    参考文献：[＃2592](http://www.sqlalchemy.org/trac/ticket/2592)

-   **[orm]
    [feature]**默认查询“自动关联”，与select()一样。以前，在另一个查询中用作子查询将需要显式调用correlate()方法，以便将内部表与外部关联起来。与往常一样，关联（无）禁用关联。[¶](#change-895b051922d21bb69c4c67ce5309b066)

    参考文献：[＃2179](http://www.sqlalchemy.org/trac/ticket/2179)

-   **[orm] [feature]**The after\_attach event is now emitted after the
    object is established in Session.new or Session.identity\_map upon
    Session.add(), Session.merge(), etc., so that the object is
    represented in these collections when the event is called.
    添加before\_attach事件以适应需要自动刷新预连接对象的用例。[¶](#change-8597db755973435d332ab67dcd0cd333)

    参考文献：[＃2464](http://www.sqlalchemy.org/trac/ticket/2464)

-   **[orm]
    [feature]**当在flush的“execute”部分中使用不支持的方法时，会话将产生警告。这些是熟悉的方法add()，delete()等。以及像在after\_insert()，after\_update()等mapper级别的刷新事件中调用的集合和相关对象操作。很长时间以来，SQLAlchemy无法保证结果在执行flush计划时被操纵，但用户仍在执行此操作，因此现在有警告。也许有一天会话会被增强以支持flush中的这些操作，但现在，结果不能得到保证。[¶](#change-fe41acf149abee6a65a1785143121903)

-   **[orm] [feature]**ORM entities can be passed to the core select()
    construct as well as to the select\_from(), correlate(), and
    correlate\_except() methods of select(), where they will be
    unwrapped into
    selectables.[¶](#change-443927d0d360b2d45aec1f0edb4cd52e)

    参考文献：[＃2245](http://www.sqlalchemy.org/trac/ticket/2245)

-   **[orm]
    [feature]**支持基于映射属性自动呈现关系连接条件，并使用核心SQL构造。例如。
    select（[SomeClass]）。其中（SomeClass.somerelationship）将从“someclass”呈现SELECT，并将“somerelationship”的主要连接用作WHERE子句。当在核心SQL上下文中使用时，这改变了“SomeClass.somerelationship”的先前含义；以前，它会“解决”到可选父项，这通常不是有用的。也适用于query.filter()。与。[¶](#change-a67dd1b9a7a101568b19a0bab8f0e7b1)相关

    参考文献：[＃2245](http://www.sqlalchemy.org/trac/ticket/2245)

-   **[orm] [feature]**
    declarative\_base()中的类的注册表现在是一个WeakValueDictionary。因此，取消引用的“Base”的子类将被垃圾收集，如果它们没有被任何其他映射器/超类映射器引用，则为*。*请参阅此票证的下一个注释。[¶](#change-f3c6355a218b2e87fd0f0703b6db668b)

    参考文献：[＃2526](http://www.sqlalchemy.org/trac/ticket/2526)

-   **[orm] [feature]**Conflicts between columns on single-inheritance
    declarative subclasses, with or without using a mixin, can be
    resolved using a new @declared\_attr usage described in the
    documentation.[¶](#change-60840075c7cfa8d1adae037d2c11e7ac)

    参考文献：[＃2472](http://www.sqlalchemy.org/trac/ticket/2472)

-   **[orm] [feature]**
    declared\_attr现在可以在非mixin类上使用，即使这通常仅用于单继承子类列冲突解决方法。[¶](#change-5cd3668a5182df1fe6b544b806615e64)

    参考文献：[＃2472](http://www.sqlalchemy.org/trac/ticket/2472)

-   **[orm] [feature]**declared\_attr can now be used with attributes
    that are not Column or MapperProperty; including any user-defined
    value as well as association proxy
    objects.[¶](#change-b42d3e5638d89a011e7c711e5519fe42)

    参考文献：[＃2517](http://www.sqlalchemy.org/trac/ticket/2517)

-   **[orm] [feature]***Very limited* support for inheriting mappers to
    be GC’ed when the class itself is deferenced.
    映射器不能有其自己的表（即只有单个表inh），没有多态属性。这允许创建声明式映射类的临时子类的用例，在没有表或映射指令的情况下，它们在被单元测试解除引用时被垃圾收集。[¶](#change-5e6f2f1fd27a664f943148e0e20be5cc)

    参考文献：[＃2526](http://www.sqlalchemy.org/trac/ticket/2526)

-   **[orm] [feature]**Declarative now maintains a registry of classes
    by string name as well as by full module-qualified name.
    现在可以根据relationship()中的模块限定字符串查找具有相同名称的多个类。简单的类名称查找，其中多个类共享相同的名称，现在引发一条信息错误消息。[¶](#change-073653e77b313e22c14bb667583872c7)

    参考文献：[＃2338](http://www.sqlalchemy.org/trac/ticket/2338)

-   **[orm]
    [feature]**现在可以提供覆盖任何非ORM类型列的类绑定属性，而不仅仅是描述符。[¶](#change-04cfa3591fc1133acc153a1db8fb823a)

    参考文献：[＃2535](http://www.sqlalchemy.org/trac/ticket/2535)

-   **[orm] [feature]**Added with\_labels and reduce\_columns keyword
    arguments to Query.subquery(), to provide two alternate strategies
    for producing queries with uniquely- named columns. [¶
    T0\>](#change-56649e7f35bc7153f0e7220eab4aec69)

    参考文献：[＃1729](http://www.sqlalchemy.org/trac/ticket/1729)

-   **[orm]
    [feature]**由于过期/属性刷新/收集替换而导致对已插装集合的引用不再与父类关联时发出警告，但接收到附加或移除操作在现在分离的集合上。[¶](#change-89c7b068a74a5e4d7c5cd96c1fcdb81e)

    参考文献：[＃2476](http://www.sqlalchemy.org/trac/ticket/2476)

-   **[orm] [removed]**The legacy “mutable” system of the ORM, including
    the MutableType class as well as the mutable=True flag on PickleType
    and postgresql.ARRAY has been removed.
    ORM使用0.7中引入的sqlalchemy.ext.mutable扩展来检测就地突变。删除MutableType和相关的结构可以从SQLAlchemy的内部消除大量的复杂性。该方法表现不佳，因为它会在使用时扫描会话的全部内容。[¶](#change-9e38576183f7a6782b4f7506ccdf6a64)

    参考文献：[＃2442](http://www.sqlalchemy.org/trac/ticket/2442)

-   **[orm] [removed]**已删除的已删除标识符：

    -   allow\_null\_pks mapper()参数（使用allow\_partial\_pks）
    -   \_get\_col\_to\_prop()映射器方法（使用get\_property\_by\_column()）
    -   Session.merge()的dont\_load参数（使用load = True）
    -   sqlalchemy.orm.shard模块（使用sqlalchemy.ext.horizo​​ntal\_shard）

    [¶](#change-dca2d3ea2b1c7196e57ba9c29726c984)

-   **[orm] [bug]**ORM will perform extra effort to determine that an FK
    dependency between two tables is not significant during flush if the
    tables are related via joined inheritance and the FK dependency is
    not part of the inherit\_condition, saves the user a use\_alter
    directive.[¶](#change-6b9cbc218fc7c96feb638b82e0510096)

    参考文献：[＃2527](http://www.sqlalchemy.org/trac/ticket/2527)

-   **[orm] [bug]**The instrumentation events class\_instrument(),
    class\_uninstrument(), and attribute\_instrument() will now fire off
    only for descendant classes of the class assigned to listen().
    以前，无论传递的“目标”参数如何，都会分配一个事件侦听器来侦听所有类中的所有类。[¶](#change-20d79523a1d3c898c75000b8432ad204)

    参考文献：[＃2590](http://www.sqlalchemy.org/trac/ticket/2590)

-   **[orm] [bug]**with\_polymorphic() produces JOINs in the correct
    order and with correct inheriting tables in the case of sending
    multi-level subclasses in an arbitrary order or with intermediary
    classes missing.[¶](#change-d4fb10b3e74c7cfee50b305f21ad75ba)

    参考文献：[＃1900](http://www.sqlalchemy.org/trac/ticket/1900)

-   **[orm]
    [bug]**改进了加入/子查询加载处理共享公共基础的子类实体链，没有提供特定的“连接深度”。在检测到“循环”之前，将单独链接到每个子类映射器，而不是将基类视为“循环”的源。[¶](#change-670f860895b1ac776c73a9f529b4ff01)

    参考文献：[＃2481](http://www.sqlalchemy.org/trac/ticket/2481)

-   **[orm] [bug]**
    Session.is\_modified()上的“passive”标志不再有任何作用。在任何情况下，is\_modified()都只会查看本地内存中已修改的标志，并且不会发出任何SQL或调用加载程序可调用/初始化程序。[¶](#change-43ab88968711042d804aba10f927a0e7)

    参考文献：[＃2320](http://www.sqlalchemy.org/trac/ticket/2320)

-   **[orm]
    [bug]**使用delete-orphan级联与一对多或多对多而没有single-parent =
    True时发出的警告现在是一个错误。在任何情况下，ORM将无法在此警告后发挥作用。[¶](#change-f6749307d43fd438dc2226c9c36cabdf)

    参考文献：[＃2405](http://www.sqlalchemy.org/trac/ticket/2405)

-   **[orm]
    [bug]**在flush事件（如before\_flush()，before\_update()等）内发出的惰性负载。现在将像在非事件代码中那样起作用，考虑在惰性发射查询中使用的PK
    / FK值。以前，特殊标志将被建立，这会导致延迟加载基于父PK /
    FK值的“前一个”值加载相关项目，特别是在刷新期间调用时；以这种方式加载的信号现在被本地化到工作单元实际需要以这种方式加载的位置。请注意，在调用before\_update()事件之前，UOW有时会加载这些集合，因此，“passive\_updates”的使用与否可能会影响集合是否代表“旧”或“新”数据刷新事件，基于何时发出延迟加载。在用户事件代码依赖于旧行为的极小可能性中，这种改变是向后不相容的。[¶](#change-8983e9238cae7a3307091bab80843317)

    参考文献：[＃2350](http://www.sqlalchemy.org/trac/ticket/2350)

-   **[orm]
    [bug]**继续处理由于事件侦听器引起的额外状态后冲刷；任何从属性角度标记为“脏”的状态，通常是通过after\_insert()，after\_update()等内的列属性设置事件，都会在所有情况下重置“历史记录”标志，而不是只有那些实例那是冲洗的一部分。这具有这样的效果，即该“脏”状态在刷新后不会结转并且不会导致UPDATE语句。为此发出警告；
    set\_committed\_state()方法可用于在不产生历史事件的情况下为对象分配属性。[¶](#change-dc5132d9120b849690569f05152a84cf)

    参考文献：[＃2582](http://www.sqlalchemy.org/trac/ticket/2582)，[＃2566](http://www.sqlalchemy.org/trac/ticket/2566)

-   **[orm]
    [bug]**修复了@declared\_attr列和mixin上直接定义的列之间缓慢发展的断开连接。在这两种情况下，列将被应用到声明的类的表中，但不会应用到已连接的继承子类的表中。以前，直接定义的列将被放置在基本表和子表上，这通常不是我们所期望的。[¶](#change-39a20209d28a327df9e9d29836c7c289)

    参考文献：[＃2565](http://www.sqlalchemy.org/trac/ticket/2565)

-   **[orm] [bug]**Declarative can now propagate a column declared on a
    single-table inheritance subclass up to the parent class’ table,
    when the parent class is itself mapped to a join() or select()
    statement, directly or via joined inheritance, and not just a
    Table.[¶](#change-2e38231d60a59df94e2c8460f26df0ac)

    参考文献：[＃2549](http://www.sqlalchemy.org/trac/ticket/2549)

-   **[orm] [bug]** uselist =
    False与“动态”加载器结合时会发出错误。这是0.7.9中的一个警告。[¶](#change-5f7f7241c49f5c13956148d68788a5b4)

-   **[orm] [moved]**The InstrumentationManager interface and the entire
    related system of alternate class implementation is now moved out to
    sqlalchemy.ext.instrumentation.
    这是一个很少使用的系统，它增加了类仪器机制的复杂性和开销。新的体系结构允许它在InstrumentationManager实际导入之前保持未使用状态，此时它将被引导到内核中。[¶](#change-d949d8b3a5cfeff6d354df74627d5c86)

### 发动机[¶ T0\>](#change-0.8.0b1-engine "Permalink to this headline")

-   **[engine]
    [feature]**连接事件侦听器现在可以与单个Connection对象关联，而不仅仅是Engine对象。[¶](#change-9351c132e3dc4f1e2351b2a8da2e25fa)

    参考文献：[＃2511](http://www.sqlalchemy.org/trac/ticket/2511)

-   **[engine] [feature]**The before\_cursor\_execute event fires off
    for so-called “\_cursor\_execute” events, which are usually
    special-case executions of primary-key bound sequences and
    default-generation SQL phrases that invoke separately when RETURNING
    is not used with
    INSERT.[¶](#change-b45c2b0f2927b785ff1ecf351e774697)

    参考文献：[＃2459](http://www.sqlalchemy.org/trac/ticket/2459)

-   **[engine]
    [feature]**测试套件使用的库已经被移动了一些，以便它们再次成为SQLAlchemy安装的一部分。此外，新的sqlalchemy.testing.suite软件包中还有一套新的测试。这是一个欠发展的系统，希望为外部方言提供一个通用的测试套件。在SQLAlchemy之外维护的方言可以使用新的测试夹具作为他们自己的测试框架，并且可以免费获得一套“合规性”的以方言为重点的测试套件，包括改进的“需求”系统，其中特定的功能和特性可以启用或禁用测试。[¶](#change-22463c2cfb9d39369a05c7604a115970)

-   **[engine]
    [feature]**增加了一个新系统，用于注册进程中的新方言而不使用入口点。请参阅“注册新方言”的文档。[¶](#change-430f3e50d2f127fd14de43289d9a2f3c)

    参考文献：[＃2462](http://www.sqlalchemy.org/trac/ticket/2462)

-   **[engine]
    [feature]**如果未传递“value”或“callable”参数，则“required”标志默认设置为True，如果未显式传递，则在bindparam()上。这将导致语句执行检查绑定参数的最终集合中存在的参数，而不是隐式指定None。[¶](#change-e2fae5f65ab52a26ac82b7f60935da09)

    参考文献：[＃2556](http://www.sqlalchemy.org/trac/ticket/2556)

-   **[engine] [feature]**Various API tweaks to the “dialect” API to
    better support highly specialized systems such as the Akiban
    database, including more hooks to allow an execution context to
    access type processors.[¶](#change-fe0037e95612a977b51439e4b6c0eafb)

-   **[engine] [feature]**
    Inspector.get\_primary\_keys()已弃用；使用Inspector.get\_pk\_constraint()。Courtesy
    Diana Clarke。[¶](#change-9decb8479dcbbd65af523f2c6c173243)

    参考文献：[＃2422](http://www.sqlalchemy.org/trac/ticket/2422)

-   **[engine]
    [feature]**由于我们有时间实现，新的C扩展模块“utils”已被添加用于其他功能加速。[¶](#change-887967cc348c92cb22f612310ccfc257)

-   **[engine] [bug]** Inspector.get\_table\_names()order\_by
    =“foreign\_key”功能现在首先按照dependee对表进行排序，以与util.sort\_tables和metadata.sorted\_tables保持一致。[T2\>](#change-1b4924eaec05f897fcafc0a386d7d0b1)

-   **[engine] [bug]**Fixed bug whereby if a database restart affected
    multiple connections, each connection would individually invoke a
    new disposal of the pool, even though only one disposal is
    needed.[¶](#change-73a085588ec93dbd5c85a150c70daa5e)

    参考文献：[＃2522](http://www.sqlalchemy.org/trac/ticket/2522)

-   **[engine] [bug]**
    .c上的列名称。对于那些明确命名为.key的列，apply\_labels()现在基于\_
    而不是\_ 。[¶](#change-07342ef0c4ddef6d0e85eb475b5f4ddf) T3\> T2\>
    T1\> T0\>

    参考文献：[＃2397](http://www.sqlalchemy.org/trac/ticket/2397)

-   **[engine] [bug]**The autoload\_replace flag on Table, when False,
    will cause any reflected foreign key constraints which refer to
    already-declared columns to be skipped, assuming that the in-Python
    declared column will take over the task of specifying in-Python
    ForeignKey or ForeignKeyConstraint
    declarations.[¶](#change-8d333a7e4e2cdba25bbd707e1969eb49)

-   **[engine] [bug]**The ResultProxy methods inserted\_primary\_key,
    last\_updated\_params(), last\_inserted\_params(),
    postfetch\_cols(), prefetch\_cols() all assert that the given
    statement is a compiled construct, and is an insert() or update()
    statement as is appropriate, else raise
    InvalidRequestError.[¶](#change-1e7b3421e138590585f3eaeed284bf5a)

    参考文献：[＃2498](http://www.sqlalchemy.org/trac/ticket/2498)

-   **[engine]**删除ResultProxy.last\_inserted\_ids，替换为inserted\_primary\_key。[¶](#change-b9d4ab67bbed4b4cbf58ffa3665cc480)

### SQL [¶ T0\>](#change-0.8.0b1-sql "Permalink to this headline")

-   **[sql]
    [feature]**添加了一个新的方法[`Engine.execution_options()`](core_connections.html#sqlalchemy.engine.Engine.execution_options "sqlalchemy.engine.Engine.execution_options")到[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")。此方法与[`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")类似，它创建了一个父对象的副本，它将引用新的选项集。该方法可用于构建每个引擎共享相同基础连接池的分片方案。该方法也针对ORM中的水平碎片配方进行了测试。

    也可以看看

    [`Engine.execution_options()`](core_connections.html#sqlalchemy.engine.Engine.execution_options "sqlalchemy.engine.Engine.execution_options")

    [¶](#change-01459b01c904c45c34254ac95c8db643)

-   **[sql] [feature]**Major rework of operator system in Core, to allow
    redefinition of existing operators as well as addition of new
    operators at the type level.
    新的类型可以从现有的类型创建，这些类型可以添加或重新定义输出到列表达式的操作，类似于ORM如何允许comparator\_factory。新架构将此功能移入Core，以便在任何情况下始终如一地使用该功能，并使用现有类型的传播行为干净地传播。[¶](#change-f532690d0ec3e3a93859eaea05b6f1c3)

    参考文献：[＃2547](http://www.sqlalchemy.org/trac/ticket/2547)

-   **[sql] [feature]**To complement, types can now provide “bind
    expressions” and “column expressions” which allow compile-time
    injection of SQL expressions into statements on a per-column or
    per-bind level.
    这适用于需要在SQL级别增加绑定和结果行为的类型的用例，而不是在Python级别。允许透明加密/解密，使用Postgis函数等方案。[¶](#change-157798fc4c22471e5ffcc78196bc2037)

    参考文献：[＃1534](http://www.sqlalchemy.org/trac/ticket/1534)，[＃2547](http://www.sqlalchemy.org/trac/ticket/2547)

-   **[sql] [feature]**The Core oeprator system now includes the getitem
    operator, i.e. the bracket operator in Python.
    这首先用于为Postgresql
    ARRAY类型提供索引和切片行为，并为定制\_\_getitem\_\_方案的最终用户定义提供了一个钩子，可以在类型级别以及在ORM级别的自定义运算符方案中应用这些方案。lshift
    (\<\<) and="" rshift (\>\>) are also supported as optional
    operators.

    请注意，此更改的效果是ORM与synonym()或其他“描述符包装”方案结合使用的基于描述符的\_\_getitem\_\_方案需要开始使用自定义比较器来维护此行为。

    [¶](#change-b3d03e37a80f9e08cd56e7135f530268)

-   **[sql] [feature]**Revised the rules used to determine the operator
    precedence for the user-defined operator, i.e. that granted using
    the `op()` method.
    以前，在所有情况下都应用了最小的优先级，现在默认优先级为零，低于除“逗号”之外的所有运算符（例如，用于`func`调用的参数列表）和“AS “，也可以通过`op()`方法的”precedence“参数进行自定义。[¶](#change-d5fa44003fbe6e1007f3b136de356241)

    参考文献：[＃2537](http://www.sqlalchemy.org/trac/ticket/2537)

-   **[sql]
    [feature]**将“排序规则”参数添加到所有字符串类型。当存在时，呈现为COLLATE
    。
    T0\>这可以支持COLLATE关键字，现在支持包括MySQL，SQLite和Postgresql在内的多个数据库。[¶](#change-510b1889868d9947ad1950a2e512d61d)

    参考文献：[＃2276](http://www.sqlalchemy.org/trac/ticket/2276)

-   **[sql]
    [feature]**现在可以通过将operators.custom\_op()与UnaryExpression()结合使用自定义一元运算符。[¶](#change-800e35771b07bd8b83965890465964c3)

-   **[sql]
    [feature]**增强的GenericFunction和func。\*允许通过func使用用户定义的GenericFunction子类。\*名称空间自动按类名，可选地使用包名称，以及能够使所呈现的名称与func中识别的名称不同。\*
    [¶ T0\>](#change-5fabc53dcd5920c9dd6725c67706b1cb)

-   **[sql] [feature]**The cast() and extract() constructs will now be
    produced via the func.
    \*访问器，因为用户自然会尝试从func访问这些名称。\*尽管返回的对象不是FunctionElement，它们也可以做预期的事情。[¶](#change-c456cfbbef249505af02d4bed46a65a2)

    参考文献：[＃2562](http://www.sqlalchemy.org/trac/ticket/2562)

-   现在可以使用新的inspect()服务来获取Inspector对象，它是[¶](#change-a82ec299dc0d072667ab30cb57b59f22)的一部分。**[sql]
    [feature]**

    参考文献：[＃2208](http://www.sqlalchemy.org/trac/ticket/2208)

-   **[sql] [feature]**
    column\_reflect事件现在接受Inspector对象作为第一个参数，位于“table”之前。使用这个新事件的0.7版本的代码将需要修改以添加“检查器”对象作为第一个参数。[¶](#change-d58191ed252657f9d6fb0178b62abf4c)

    参考文献：[＃2418](http://www.sqlalchemy.org/trac/ticket/2418)

-   **[sql]
    [feature]**默认情况下，结果集中列定位的行为现在是区分大小写的。多年来，SQLAlchemy会对这些值执行不区分大小写的转换，可能会减少像Oracle和Firebird这样的方言的早期大小写敏感问题。这些问题已经在更现代的版本中得到了更清晰的解决，因此在标识符上调用lower()的性能受到影响。不区分大小写的比较可以通过在create\_engine()上设置“case\_insensitive
    = False”来重新启用。[¶](#change-6c39aca731482d07a19bb63fffd1db07)

    参考文献：[＃2423](http://www.sqlalchemy.org/trac/ticket/2423)

-   **[sql] [feature]**The “unconsumed column names” warning emitted
    when keys are present in insert.values() or update.values() that
    aren’t in the target table is now an
    exception.[¶](#change-f0476d1e752c1114226c2f7b1733e959)

    参考文献：[＃2415](http://www.sqlalchemy.org/trac/ticket/2415)

-   **[sql]
    [feature]**将“MATCH”子句添加到ForeignKey，ForeignKeyConstraint，礼貌Ryan
    Kelly。[¶](#change-fbcc82d903c96f4fc45ae1118e05f293)

    参考文献：[＃2502](http://www.sqlalchemy.org/trac/ticket/2502)

-   **[sql]
    [feature]**从表的别名中增加了对DELETE和UPDATE的支持，假定它与查询中的其他地方相关，Ryan
    Kelly提供。[¶](#change-d72952e44e63b0fc2012138b67d47086)

    参考文献：[＃2507](http://www.sqlalchemy.org/trac/ticket/2507)

-   **[sql] [feature]**select() features a correlate\_except() method,
    auto correlates all selectables except those
    passed.[¶](#change-0ad7f438f6e23fa71b85a5f8d68a4196)

-   **[sql] [feature]**The prefix\_with() method is now available on
    each of select(), insert(), update(), delete(), all with the same
    API, accepting multiple prefix calls, as well as a “dialect name” so
    that the prefix can be limited to one kind of
    dialect.[¶](#change-f4bff6e966d77ff6d933f92d367dcae4)

    参考文献：[＃2431](http://www.sqlalchemy.org/trac/ticket/2431)

-   **[sql]
    [feature]**添加了reduce\_columns()方法来选择()构造，使用util.reduce\_columns实用程序函数内联列替换列以删除等效列。reduce\_columns()还添加了“with\_only\_synonyms”，以将缩减限制为具有相同名称的列。弃用的fold\_equivalents()功能被删除。[¶](#change-7dbf816368fe65f3b7de2d522397a8a6)

    参考文献：[＃1729](http://www.sqlalchemy.org/trac/ticket/1729)

-   **[sql] [feature]**Reworked the startswith(), endswith(), contains()
    operators to do a better job with negation (NOT LIKE), and also to
    assemble them at compilation time so that their rendered SQL can be
    altered, such as in the case for Firebird STARTING
    WITH[¶](#change-8d8e593e41bb7a19ee46c22bc0decfa1)

    参考文献：[＃2470](http://www.sqlalchemy.org/trac/ticket/2470)

-   **[sql] [feature]**为渲染CREATE
    TABLE的系统添加了一个钩子，通过针对新的schema.CreateColumn构造函数构造一个@compiles函数，为每个Column单独提供对渲染的访问。[¶
    T2\>](#change-120cab828675e93105c9e93717edec27)

    参考文献：[＃2463](http://www.sqlalchemy.org/trac/ticket/2463)

-   **[sql]
    [feature]**“标量”选择现在有一个WHERE方法来帮助生成构建。关于SS如何“关联”列的细微调整；新方法不再适用于所选基础Table列的含义。这改善了一些相当深奥的情况，并且那里的逻辑似乎没有任何目的。[¶](#change-9f7e29fc75f561268d93f465d8982eb1)

-   **[sql]
    [feature]**首次使用构造成引用多个远程表的ForeignKeyConstraint()时，会引发一个显式错误。[¶](#change-aaa07a086b42d588284232c42691223e)

    参考文献：[＃2455](http://www.sqlalchemy.org/trac/ticket/2455)

-   **[sql] [feature]**Added [`ColumnOperators.notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_"),
    [`ColumnOperators.notlike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike"),
    [`ColumnOperators.notilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
    to [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators").[¶](#change-7d11577fe3de5f05b5b85e20a72c5d30)

    参考文献：[＃2580](http://www.sqlalchemy.org/trac/ticket/2580)

-   **[sql] [changed]**Most classes in expression.sql are no longer
    preceded with an underscore, i.e. Label, SelectBase, Generative,
    CompareMixin.
    \_BindParamClause也被重命名为BindParameter。这些类的旧下划线名称在可预见的将来仍然可以作为同义词使用。[¶](#change-25bf00fd616dfde5e75310390171c9cb)

-   **[sql] [removed]**The long-deprecated and non-functional
    `assert_unicode` flag on
    [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
    as well as [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
    is removed.[¶](#change-ad44af79c886d1bb283042deb64f9cbe)

-   **[sql] [bug]**Fixed bug where keyword arguments passed to
    `Compiler.process()` wouldn’t
    get propagated to the column expressions present in the columns
    clause of a SELECT statement.
    特别是当由依赖特殊标志的自定义编译方案使用时。[¶](#change-9f11c14207568ba3d31a17ff11ff6602)

    参考文献：[＃2593](http://www.sqlalchemy.org/trac/ticket/2593)

-   **[sql] [bug] [orm]**The auto-correlation feature of
    [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
    and by proxy that of [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query"),
    will not take effect for a SELECT statement that is being rendered
    directly in the FROM list of the enclosing SELECT.
    SQL中的关联仅适用于诸如WHERE，ORDER
    BY，columns子句中的列表达式。[¶](#change-a732049d950faee01eefaa41df6d9bcf)

    参考文献：[＃2595](http://www.sqlalchemy.org/trac/ticket/2595)

-   **[sql]
    [bug]**调整列优先级，使“concat”和“match”运算符与“is”，“like”等相同。当与“IS”结合使用时，这有助于加括号渲染。[¶](#change-4f0b1f3585efc63ec1286fc3774c09b9)

    参考文献：[＃2564](http://www.sqlalchemy.org/trac/ticket/2564)

-   **[sql]
    [bug]**使用带有或不带有其他修饰结构的标签将列表达式应用于select语句将不再将该表达“定位到”底层Column；这会影响依赖列定位以检索结果的ORM操作。也就是说，查询（User.id，User.id.label（'foo'））这样的查询现在将分别跟踪每个“User.id”表达式的值，而不是将它们一起使用。预计任何用户都不会受到此影响；然而，如果select()命名的Column对象具有任意的.label()名称，则使用select()与query.from\_statement()一起使用并试图加载完全组合的ORM实体的功能可能无法正常工作，因为这些将不会对该实体映射的Column对象更长的目标。[¶](#change-e9e2da86a8c37003cda9737252a22e66)

    参考文献：[＃2591](http://www.sqlalchemy.org/trac/ticket/2591)

-   **[sql]
    [bug]**修复了Column“default”参数的解释，因为它是可调用的，不会将ExecutionContext传递给关键字参数参数。[¶](#change-609b199612bf01e7e2389e4bc22e0058)

    参考文献：[＃2520](http://www.sqlalchemy.org/trac/ticket/2520)

-   **[sql] [bug]**All of UniqueConstraint, ForeignKeyConstraint,
    CheckConstraint, and PrimaryKeyConstraint will attach themselves to
    their parent table automatically when they refer to a Table-bound
    Column object directly (i.e. not just string column name), and refer
    to one and only one Table.
    在0.8之前，此行为发生在UniqueConstraint和PrimaryKeyConstraint，而不是ForeignKeyConstraint或CheckConstraint。[¶](#change-da559086155956288e47dfe0ce6c6f63)

    参考文献：[＃2410](http://www.sqlalchemy.org/trac/ticket/2410)

-   **[sql] [bug]**TypeDecorator now includes a generic repr() that
    works in terms of the “impl” type by default.
    这是指定自定义\_\_init\_\_方法的TypeDecorator类的行为更改；如果需要\_\_repr
    \_\_()来提供忠实的构造函数表示，那么这些类型需要重新定义\_\_repr
    \_\_()。[¶](#change-b11441c88863d587366a61b22f263c2d)

    参考文献：[＃2594](http://www.sqlalchemy.org/trac/ticket/2594)

-   **[sql] [bug]**column.label(None) now produces an anonymous label,
    instead of returning the column object itself, consistent with the
    behavior of label(column,
    None).[¶](#change-8893c427938842218beba495ac8f76f1)

    参考文献：[＃2168](http://www.sqlalchemy.org/trac/ticket/2168)

-   **[sql]
    [change]**如果指定了长度，则Text()类型会呈现给定长度。[¶](#change-fb3c268a1d6d367b1d196ef3b07b4d9e)

### 的PostgreSQL [¶ T0\>](#change-0.8.0b1-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**postgresql.ARRAY features an optional
    “dimension” argument, will assign a specific number of dimensions to
    the array which will render in DDL as ARRAY[][]..., also improves
    performance of bind/result
    processing.[¶](#change-2e5a63d698d0ebd04785ccf495e9bad5)

    参考文献：[＃2441](http://www.sqlalchemy.org/trac/ticket/2441)

-   **[postgresql] [feature]**
    postgresql.ARRAY现在支持索引和切片。Python
    []运算符在所有类型为ARRAY的SQL表达式上可用；可以传递整数或简单的片段。切片也可以在UPDATE语句的SET子句的赋值端使用，方法是将它们传入Update.values()；请参阅文档以获取示例。[¶](#change-78619b6fa31af74f1144a57dae7a4f70)

-   **[postgresql]
    [feature]**增加了新的“数组字面量”结构postgresql.array()。基本上是一个“元组”，呈现为ARRAY
    [1,2,3]。[¶](#change-9b6a5818e07607737947ddcbdae34829)

-   **[postgresql] [feature]**增加了对Postgresql
    ONLY关键字的支持，该关键字可以对应于SELECT，UPDATE或DELETE语句中的表。该短语使用with\_hint()建立。礼貌Ryan
    Kelly [¶](#change-041d6fd58a2b6ecaa456a0230daca193)

    参考文献：[＃2506](http://www.sqlalchemy.org/trac/ticket/2506)

-   **[postgresql] [feature]**The “ischema\_names” dictionary of the
    Postgresql dialect is “unofficially” customizable.
    这意味着，可以在这个字典中添加新的类型，例如PostGIS类型，并且PG类型的反射代码应该能够处理具有可变数量参数的简单类型。这里的功能“非官方”有三个原因：

    1.  这不是一个“官方”API。理想情况下，“官方”API将允许以通用方式在方言或全局级别定制类型处理可调用。
    2.  这仅适用于PG方言，特别是因为PG对自定义类型与其他数据库后端有广泛的支持。一个真正的API将在默认的方言级别实现。
    3.  此处的反射代码仅针对简单类型进行测试，可能存在更多构图类型的问题。

    补丁礼貌ÉricLemoine。

    [¶](#change-0e11be03f42037dd59265040930eb6b6)

### MySQL的[¶ T0\>](#change-0.8.0b1-mysql "Permalink to this headline")

-   **[mysql]
    [feature]**为mysql语言添加了TIME类型，接受“fst”参数，它是最近MySQL版本的新“小数秒”说明符。数据类型将解释从驱动程序接收的微秒部分，但请注意，此时大多数/所有MySQL
    DBAPI都不支持返回该值。[¶](#change-2d129ed854bd771095a45bdf0613705c)

    参考文献：[＃2534](http://www.sqlalchemy.org/trac/ticket/2534)

-   **[mysql]
    [bug]**在第一次连接时，Dialect不再发送昂贵的服务器排序规则查询以及服务器封套。这些功能仍然是半专用的。[¶](#change-700a963887f5381be78374ee6cbab43e)

    参考文献：[＃2404](http://www.sqlalchemy.org/trac/ticket/2404)

### 源码[¶ T0\>](#change-0.8.0b1-sqlite "Permalink to this headline")

-   **[sqlite] [feature]**the SQLite date and time types have been
    overhauled to support a more open ended format for input and output,
    using name based format strings and regexps.
    一个新的参数“微秒”也提供了省略时间戳的“微秒”部分的选项。感谢Nathan
    Wright对此的工作和测试。[¶](#change-b5f1f9bec1b77fa7e12fe21090980fcc)

    参考文献：[＃2363](http://www.sqlalchemy.org/trac/ticket/2363)

-   **[sqlite]**Added [`types.NCHAR`](core_type_basics.html#sqlalchemy.types.NCHAR "sqlalchemy.types.NCHAR"),
    [`types.NVARCHAR`](core_type_basics.html#sqlalchemy.types.NVARCHAR "sqlalchemy.types.NVARCHAR")
    to the SQLite dialect’s list of recognized type names for
    reflection.
    SQLite返回给定类型的名称作为返回的名称。[¶](#change-5d430ab66984e1839fc49a94ccc5dacb)

    参考文献：[rc3addcc9ffad](http://www.sqlalchemy.org/trac/changeset/c3addcc9ffad)

### MSSQL [¶ T0\>](#change-0.8.0b1-mssql "Permalink to this headline")

-   **[mssql] [feature]**SQL Server dialect can be given
    database-qualified schema names, i.e. “schema=’mydatabase.dbo’”;
    reflection operations will detect this, split the schema among the
    ”.” to get the owner separately, and emit a “USE mydatabase”
    statement before reflecting targets within the “dbo” owner; the
    existing database returned from DB\_NAME() is then
    restored.[¶](#change-8e3f4625a47111ef4767a2ef9ba24c73)

-   **[mssql] [feature]**updated support for the mxodbc driver; mxodbc
    3.2.1 is recommended for full
    compatibility.[¶](#change-6322f3d6024c987d549a01d768b12959)

-   **[mssql] [bug]**删除了传统行为，通过这种方式将标量SELECT via
    ==的列比较强制转换为SQL服务器方言的IN。这是隐含的行为，在其他情况下失败，因此被删除。依赖于此的代码需要修改以明确使用column.in\_（select）。[¶](#change-38d801b4255682b32f9a913a78a9a3b3)

    参考文献：[＃2277](http://www.sqlalchemy.org/trac/ticket/2277)

### 预言[¶ T0\>](#change-0.8.0b1-oracle "Permalink to this headline")

-   **[oracle] [feature]**使用exclude\_setinputsizes
    dialect参数，可以通过发送要排除的字符串DBAPI类型名称列表来定制从setinputsizes()集中排除的列的类型。此列表先前已修复。该列表现在默认为STRING，UNICODE，从列表中删除CLOB，NCLOB。[¶](#change-ce42a727e4d7a0a75bab19dbddbbfc73)

    参考文献：[＃2561](http://www.sqlalchemy.org/trac/ticket/2561)

-   **[oracle] [bug]**Quoting information is now passed along from a
    Column with quote=True when generating a same-named bound parameter
    to the bindparam() object, as is the case in generated INSERT and
    UPDATE statements, so that unknown reserved names can be fully
    supported.[¶](#change-d8885a06585445bdffa3bb5ab8597e77)

    参考文献：[＃2437](http://www.sqlalchemy.org/trac/ticket/2437)

-   **[oracle] [bug]**
    Oracle中的CreateIndex构造现在将索引的名称限定为父表的名称。以前这个名字被省略了，这显然是在默认模式中创建索引，而不是在表中创建索引。[¶](#change-260439d04d4ab56d9b30d9ac80fbca60)

### 火鸟[¶ T0\>](#change-0.8.0b1-firebird "Permalink to this headline")

-   **[firebird] [feature]**The “startswith()” operator renders as
    “STARTING WITH”, “\~startswith()” renders as “NOT STARTING WITH”,
    using FB’s more efficient
    operator.[¶](#change-55352f849d8075f34ab05c59513144de)

    参考文献：[＃2470](http://www.sqlalchemy.org/trac/ticket/2470)

-   **[firebird]
    [feature]**添加了一个用于fdb驱动程序的实验性方言，但未经测试，因为我无法获取fdb软件包来构建。[¶](#change-274d52dddd6cd76f57ce87648cc1473c)

    参考文献：[＃2504](http://www.sqlalchemy.org/trac/ticket/2504)

-   **[firebird]
    [bug]**当尝试以与MySQL相同的方式发出没有长度的VARCHAR时，会引发CompileError。[¶](#change-1a137fa5bc1551eb7474d03095eebc94)

    参考文献：[＃2505](http://www.sqlalchemy.org/trac/ticket/2505)

-   **[firebird] [bug]**Firebird now uses strict “ansi bind rules” so
    that bound parameters don’t render in the columns clause of a
    statement - they render literally
    instead.[¶](#change-12e7c07b97df9409c6cb6b31012fa796)

-   **[firebird]
    [bug]**支持在Firebird中使用DateTime类型时传递datetime作为日期；其他方言支持这一点。[¶](#change-41375c1893b68568e7e9fca8159598fc)

### 杂项[¶ T0\>](#change-0.8.0b1-misc "Permalink to this headline")

-   **[feature] [access]**利用新的SQLAlchemy方言合规性套件，MS
    Access方言已被移至Bitbucket上的其自己的项目中。The dialect is still
    in very rough shape and probably not ready for general use yet,
    however it does have *extremely* rudimental functionality now.
    [https://bitbucket.org/zzzeek/sqlalchemy-access
    T0\>](https://bitbucket.org/zzzeek/sqlalchemy-access)[¶
    T1\>](#change-fd39f8f8e11ef48c87654cb42253c2bc)

-   **[moved]
    [maxdb]**几年前未运行的MaxDB方言被移出到一个未决的bitbucket项目中，[https://bitbucket.org/zzzeek/sqlalchemy
    -maxdb T2\>](https://bitbucket.org/zzzeek/sqlalchemy-maxdb)[¶
    T3\>](#change-b7848d7bbe509cb980a185cb57f2a3af)

-   **[examples]**烧杯缓存示例已转换为使用[dogpile.cache](https://dogpilecache.readthedocs.io/)。这是一个由Beaker缓存内部部件的相同创建者编写的新缓存库，代表了一个大大改进，简化和现代化的缓存系统。

    也可以看看

    [Dogpile Caching](orm_examples.html#examples-caching)

    [¶](#change-1523176dc77fb5a2a38ee7073b45df68)

    参考文献：[＃2589](http://www.sqlalchemy.org/trac/ticket/2589)


