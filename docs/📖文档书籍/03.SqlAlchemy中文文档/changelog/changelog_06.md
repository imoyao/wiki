---
title: changelog_06
date: 2021-02-20 22:41:29
permalink: /sqlalchemy/1eaaf3/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
0.6 更新日志[¶](#changelog "Permalink to this headline")
=======================================================

0.6.9 [¶ T0\>](#change-0.6.9 "Permalink to this headline")
----------------------------------------------------------

发布时间：2012 年 5 月 5 日星期六

### 一般[¶ T0\>](#change-0.6.9-general "Permalink to this headline")

-   **[general]**Adjusted the “importlater” mechanism, which is used
    internally to resolve import cycles, such that the usage of
    \_\_import\_\_ is completed when the import of sqlalchemy or
    sqlalchemy.orm is done, thereby avoiding any usage of \_\_import\_\_
    after the application starts new threads,
    fixes.[¶](#change-12863cf30d488f3bc66ad4bcfbbf8fd5)

    参考文献：[＃2279](http://www.sqlalchemy.org/trac/ticket/2279)

### ORM [¶ T0\>](#change-0.6.9-orm "Permalink to this headline")

-   **[orm]
    [bug]**修复了 query.get()中布尔上下文中用户映射对象的不恰当评估。[¶](#change-90dd35d523894cd2e514049899fa3652)

    参考文献：[＃2310](http://www.sqlalchemy.org/trac/ticket/2310)

-   **[orm]
    [bug]**修正了元组无意中传递给 session.query()时引发的错误格式。[¶](#change-48105c68fcefac76f598d7b48e49e120)

    参考文献：[＃2297](http://www.sqlalchemy.org/trac/ticket/2297)

-   **[orm]**Fixed bug whereby the source clause used by query.join()
    would be inconsistent if against a column expression that combined
    multiple entities
    together.[¶](#change-1f18f8d75432f09d5bbc6ac09e88b038)

    参考文献：[＃2197](http://www.sqlalchemy.org/trac/ticket/2197)

-   **[orm]**Fixed bug apparent only in Python 3 whereby sorting of
    persistent + pending objects during flush would produce an illegal
    comparison, if the persistent object primary key is not a single
    integer.[¶](#change-bec888b1020a652a9d416e4e6b261a7e)

    参考文献：[＃2228](http://www.sqlalchemy.org/trac/ticket/2228)

-   **[orm]**Fixed bug where query.join() + aliased=True from a
    joined-inh structure to itself on relationship() with join condition
    on the child table would convert the lead entity into the joined one
    inappropriately.[¶](#change-dad2fbaff0f9f5aa2ebbcf509ad408a3)

    参考文献：[＃2234](http://www.sqlalchemy.org/trac/ticket/2234)

-   **[orm]**Fixed bug whereby mapper.order\_by attribute would be
    ignored in the “inner” query within a subquery eager load. [¶
    T0\>](#change-12f7542f530a786aa0c66534c7a55317)

    参考文献：[＃2287](http://www.sqlalchemy.org/trac/ticket/2287)

-   **[orm]**Fixed bug whereby if a mapped class redefined
    \_\_hash\_\_() or \_\_eq\_\_() to something non-standard, which is a
    supported use case as SQLA should never consult these, the methods
    would be consulted if the class was part of a “composite” (i.e.
    non-single-entity) result
    set.[¶](#change-324c9d754e04e96958acbba0a3dc83ec)

    参考文献：[＃2215](http://www.sqlalchemy.org/trac/ticket/2215)

-   **[orm]**Fixed subtle bug that caused SQL to blow up if:
    column\_property() against subquery + joinedload + LIMIT + order by
    the column property() occurred. [¶
    T0\>](#change-ccbce1aaf7fc09560215d0f41426e87e)

    参考文献：[＃2188](http://www.sqlalchemy.org/trac/ticket/2188)

-   **[orm]**
    with\_parent 产生的连接条件以及对父代使用“动态”关系时将生成唯一的 bindparams，而不是错误地重复相同的 bindparam。[¶
    T0\>](#change-18699e5af1eae1a1ce72667d2f948b1f)

    参考文献：[＃2207](http://www.sqlalchemy.org/trac/ticket/2207)

-   **[orm]**Repaired the “no statement condition” assertion in Query
    which would attempt to raise if a generative method were called
    after from\_statement() were
    called..[¶](#change-c0fbe0ad615ed9a900a904e02ea5ecd8)

    参考文献：[＃2199](http://www.sqlalchemy.org/trac/ticket/2199)

-   **[orm]** Cls.column.collat​​e（“some
    collat​​ion”）现在可用。[¶](#change-91ff76e5a82e6e129deb5a0cad60796d)

    参考文献：[＃1776](http://www.sqlalchemy.org/trac/ticket/1776)

### 发动机[¶ T0\>](#change-0.6.9-engine "Permalink to this headline")

-   **[engine]**Backported the fix for introduced in 0.7.4, which
    ensures that the connection is in a valid state before attempting to
    call rollback()/prepare()/release() on savepoint and two-phase
    transactions.[¶](#change-7da4cdf9f79cae9743a85d40954ac411)

    参考文献：[＃2317](http://www.sqlalchemy.org/trac/ticket/2317)

### SQL [¶ T0\>](#change-0.6.9-sql "Permalink to this headline")

-   **[sql]**Fixed two subtle bugs involving column correspondence in a
    selectable, one with the same labeled subquery repeated, the other
    when the label has been “grouped” and loses itself. 影响。[¶
    T0\>](#change-d49c6908f106df0a29516c49cddab3c2)

    参考文献：[＃2188](http://www.sqlalchemy.org/trac/ticket/2188)

-   **[sql]**Fixed bug whereby “warn on unicode” flag would get set for
    the String type when used with certain dialects. 这个 bug 不在 0.7.
    [¶](#change-08b55ba78d7b3fa1a51925aecafe255b)

-   **[sql]**修正了 select 中的 with\_only\_columns()方法失败，如果通过了 selectable 的话。但是，FROM 行为在这里仍然不正确，因此在任何情况下，您都需要 0.7 来使用该用例。[¶](#change-1897da4753826ae9d5eacb9bce3c482f)

    参考文献：[＃2270](http://www.sqlalchemy.org/trac/ticket/2270)

### 架构[¶ T0\>](#change-0.6.9-schema "Permalink to this headline")

-   **[schema]**当 ForeignKeyConstraint 引用父级中未找到的列名称时，添加了一条信息性错误消息。[¶](#change-0d0176936941374dd977d3cfc229ea75)

### 的 PostgreSQL [¶ T0\>](#change-0.6.9-postgresql "Permalink to this headline")

-   **[postgresql]**修正了与 PG9 中相同的修改索引行为影响重命名列上的主键反射的 bug。[¶](#change-525baeb589c68e1d82ba3a075efda6a4)

    参考文献：[＃2291](http://www.sqlalchemy.org/trac/ticket/2291)，[＃2141](http://www.sqlalchemy.org/trac/ticket/2141)

### MySQL 的[¶ T0\>](#change-0.6.9-mysql "Permalink to this headline")

-   **[mysql]**修正了 OurSQL 方言使用 ANSI 中性引用符号“'”作为 XA 命令而不是'“'。[¶
    T0\>](#change-0698928580db2e78fa0bf2b5d0fb757a)

    参考文献：[＃2186](http://www.sqlalchemy.org/trac/ticket/2186)

-   **[mysql]** CREATE
    TABLE 会将 COLLATE 选项放在 CHARSET 之后，这看起来是 MySQL 的任意规则的一部分，关于它是否会真正起作用。[¶](#change-893dc29708dfe84565bb6b59ebc5d116)

    参考文献：[＃2225](http://www.sqlalchemy.org/trac/ticket/2225)

### MSSQL [¶ T0\>](#change-0.6.9-mssql "Permalink to this headline")

-   **[mssql]
    [bug]**在检索索引名称列表和索引内的列名称时解码传入值。[¶](#change-2ca5517878da9a4646159611f7fadfd5)

    参考文献：[＃2269](http://www.sqlalchemy.org/trac/ticket/2269)

### 预言[¶ T0\>](#change-0.6.9-oracle "Permalink to this headline")

-   **[oracle]**添加 ORA-00028 断开代码，使用 cx\_oracle
    \_Error.code 获取代码，[¶](#change-a0976892727bd6ce76216c086a0e73cf)

    参考文献：[＃2200](http://www.sqlalchemy.org/trac/ticket/2200)

-   **[oracle]**修复了没有生成正确 DDL 的 oracle.RAW 类型。[¶](#change-c9c4f1305df1aa628e2d4f756511f177)

    参考文献：[＃2220](http://www.sqlalchemy.org/trac/ticket/2220)

-   **[oracle]**将 CURRENT 添加到保留字列表中。[¶](#change-eda1d903a91584d2894e843edeb325ce)

    参考文献：[＃2212](http://www.sqlalchemy.org/trac/ticket/2212)

### 杂项[¶ T0\>](#change-0.6.9-misc "Permalink to this headline")

-   **[examples]**调整了 dictlike-polymorphic.py 示例以应用 CAST，使其可以在 PG，其他数据库上工作。[¶](#change-876cb8fb1ac9a1ba6772001f2b81829e)

    参考文献：[＃2266](http://www.sqlalchemy.org/trac/ticket/2266)

0.6.8 [¶ T0\>](#change-0.6.8 "Permalink to this headline")
----------------------------------------------------------

发布：2011 年 6 月 15 日

### ORM [¶ T0\>](#change-0.6.8-orm "Permalink to this headline")

-   **[orm]**针对基于列的实体调用 query.get()是无效的，这种情况现在引发了弃用警告。[¶](#change-5211656e5b9bab3746a031467f734f52)

    参考文献：[＃2144](http://www.sqlalchemy.org/trac/ticket/2144)

-   **[orm]**非主映射器将继承主映射器的\_identity\_class。这样一来，针对通常在继承映射中的类建立的 non\_primary 将生成与主映射器的标识映射兼容的结果[¶](#change-1bb5eb9cd9ead7741537faf42dbb717a)

    参考文献：[＃2151](http://www.sqlalchemy.org/trac/ticket/2151)

-   **[orm]** Backported
    0.7 的身份映射实现，它在去除时不使用互斥锁。这是因为尽管 0.6.7 的调整，一些用户仍然陷入僵局；不使用互斥锁的 0.7 方法似乎不会产生“字典改变大小”问题，这是互斥体的原始基础。[¶](#change-d26ba3de23d7c188bace06d868980bdd)

    参考文献：[＃2148](http://www.sqlalchemy.org/trac/ticket/2148)

-   **[orm]**修复了针对“无法为目标列 q 执行 syncrule”发出的错误消息；映射器'X'不映射此列“以引用正确的映射器。[¶
    T0\>](#change-7a589ce2e13c9008b3def2fd5a90ac23)

    参考文献：[＃2163](http://www.sqlalchemy.org/trac/ticket/2163)

-   **[orm]**Fixed bug where determination of “self referential”
    relationship would fail with no workaround for joined-inh subclass
    related to itself, or joined-inh subclass related to a subclass of
    that with no cols in the sub-sub class in the join
    condition.[¶](#change-fa833bfebba673a74e3bda247932e868)

    参考文献：[＃2149](http://www.sqlalchemy.org/trac/ticket/2149)

-   **[orm]**mapper() will ignore non-configured foreign keys to
    unrelated tables when determining inherit condition between parent
    and child class.
    这相当于已经应用于声明的行为。请注意，0.7 有一个更全面的解决方案，改变了 join()本身如何确定 FK 错误。[¶](#change-ffe3e5b094cad44312444477b1d9c3b5)

    参考文献：[＃2153](http://www.sqlalchemy.org/trac/ticket/2153)

-   **[orm]**Fixed bug whereby mapper mapped to an anonymous alias would
    fail if logging were used, due to unescaped % sign in the alias
    name.[¶](#change-e86ab075b7ef34298069ec75797e7bd8)

    参考文献：[＃2171](http://www.sqlalchemy.org/trac/ticket/2171)

-   **[orm]**Modify the text of the message which occurs when the
    “identity” key isn’t detected on flush, to include the common cause
    that the Column isn’t set up to detect auto-increment
    correctly;.[¶](#change-90aba29b5bd34a14cf4fa753d35659ee)

    参考文献：[＃2170](http://www.sqlalchemy.org/trac/ticket/2170)

-   **[orm]**Fixed bug where transaction-level “deleted” collection
    wouldn’t be cleared of expunged states, raising an error if they
    later became transient.[¶](#change-2f30675b878168f0ac612120144c8b76)

    参考文献：[＃2182](http://www.sqlalchemy.org/trac/ticket/2182)

### 发动机[¶ T0\>](#change-0.6.8-engine "Permalink to this headline")

-   **[engine]**Adjusted the \_\_contains\_\_() method of a RowProxy
    result row such that no exception throw is generated internally;
    NoSuchColumnError() also will generate its message regardless of
    whether or not the column construct can be coerced to a
    string..[¶](#change-81e707c0cdab968a06ef47f7b2d2940e)

    参考文献：[＃2178](http://www.sqlalchemy.org/trac/ticket/2178)

### SQL [¶ T0\>](#change-0.6.8-sql "Permalink to this headline")

-   **[sql]**Fixed bug whereby if FetchedValue was passed to column
    server\_onupdate, it would not have its parent “column” assigned,
    added test coverage for all column default assignment
    patterns.[¶](#change-d38c459e931e28a7c7cd6e4a62af4849)

    参考文献：[＃2147](http://www.sqlalchemy.org/trac/ticket/2147)

-   **[sql]**Fixed bug whereby nesting a label of a select() with
    another label in it would produce incorrect exported columns.
    除此之外，这会破坏另一个 column\_property()的 ORM
    column\_property()映射。[¶
    T0\>](#change-2ae59c579c4c2ced22f234c933eedb03)

    参考文献：[＃2167](http://www.sqlalchemy.org/trac/ticket/2167)

### 的 PostgreSQL [¶ T0\>](#change-0.6.8-postgresql "Permalink to this headline")

-   **[postgresql]**修正了影响 PG9 的错误，因此如果针对名称已更改的列，索引反射将失败。[¶
    T0\>](#change-d7f16be247c5f9c9413e70ca6d68a835)

    参考文献：[＃2141](http://www.sqlalchemy.org/trac/ticket/2141)

-   **[postgresql]**有关数值数组 MATCH 运算符的一些单元测试修正。一个潜在的浮点不准确问题已经修复，MATCH 运算符的某些测试目前只能在面向 EN 的语言环境中执行。[¶
    T0\>](#change-5fb3b20bf3b31a34fb78d3340bf1dcd1)

    参考文献：[＃2175](http://www.sqlalchemy.org/trac/ticket/2175)

### MSSQL [¶ T0\>](#change-0.6.8-mssql "Permalink to this headline")

-   **[mssql]**修正了 MSSQL 方言中的错误，因此应用于模式限定表的别名会泄漏到封闭的 select 语句中。[¶](#change-c07b8fa79245c2fb7647120e9fe7d228)

    参考文献：[＃2169](http://www.sqlalchemy.org/trac/ticket/2169)

-   **[mssql]**修正了在结果集或绑定参数中使用 DATETIME2 类型在“适应”步骤中失败的错误。这个问题不在 0.7 中。[¶](#change-6e28260bf17c92850ac3773eda0fe105)

    参考文献：[＃2159](http://www.sqlalchemy.org/trac/ticket/2159)

0.6.7 [¶ T0\>](#change-0.6.7 "Permalink to this headline")
----------------------------------------------------------

发布于：2011 年 4 月 13 日

### ORM [¶ T0\>](#change-0.6.7-orm "Permalink to this headline")

-   **[orm]**收紧迭代与围绕身份映射迭代删除互斥体，试图减少导致死锁的（非常罕见的）可重入 gc 操作的机会。可以在 0.7 中删除互斥锁。[¶](#change-eed859bebcbe8988e1d4cc3b30ebc835)

    参考文献：[＃2087](http://www.sqlalchemy.org/trac/ticket/2087)

-   **[orm]**为 Query.subquery()添加了 name 参数，以允许将固定名称分配给别名对象。[¶
    T4\>](#change-857bb51b7ea179692c74f9266bdba26d)

    参考文献：[＃2030](http://www.sqlalchemy.org/trac/ticket/2030)

-   **[orm]**当连接表继承映射器在本地映射表上没有主键时（但在超类表上有 pks）时，会发出警告。[¶](#change-4363d0760126c3a958074eb1490c4919)

    参考文献：[＃2019](http://www.sqlalchemy.org/trac/ticket/2019)

-   **[orm]**Fixed bug where “middle” class in a polymorphic hierarchy
    would have no ‘polymorphic\_on’ column if it didn’t also specify a
    ‘polymorphic\_identity’, leading to strange errors upon refresh,
    wrong class loaded when querying from that target.
    在使用单个表继承时也会发出正确的 WHERE 标准。[¶](#change-b9b208bc91c2102e8f0fd7911db16925)

    参考文献：[＃2038](http://www.sqlalchemy.org/trac/ticket/2038)

-   **[orm]**Fixed bug where a column with a SQL or server side default
    that was excluded from a mapping with include\_properties or
    exclude\_properties would result in
    UnmappedColumnError.[¶](#change-a2fb7de3c9754e79e857eab068d7e269)

    参考文献：[＃1995](http://www.sqlalchemy.org/trac/ticket/1995)

-   **[orm]**在异常情况下发生警告，即在取消引用父对象后发生集合上的附加事件或类似事件，这会阻止父会话在会话中被标记为“脏”
    。这在 0.7 中是个例外。[¶](#change-2c07178fa8d7673418fa3709242f8faf)

    参考文献：[＃2046](http://www.sqlalchemy.org/trac/ticket/2046)

-   **[orm]**Fixed bug in query.options() whereby a path applied to a
    lazyload using string keys could overlap a same named attribute on
    the wrong entity.
    注 0.7 具有此修正的更新版本。[¶](#change-59c721c9c15d94a562e9083c84012937)

    参考文献：[＃2098](http://www.sqlalchemy.org/trac/ticket/2098)

-   **[orm]**重写了在尝试刷新非超类型的子类时发生的异常。[¶](#change-5e7605de1fa0c84b6669ddade822cb51)

    参考文献：[＃2063](http://www.sqlalchemy.org/trac/ticket/2063)

-   **[orm]**Some fixes to the state handling regarding backrefs,
    typically when autoflush=False, where the back-referenced collection
    wouldn’t properly handle add/removes with no net change. 感谢 Richard
    Murri 提供的测试案例+补丁。[¶](#change-8d18a5abb18ac58c0bfa0091638be48f)

    参考文献：[＃2123](http://www.sqlalchemy.org/trac/ticket/2123)

-   **[orm]**如果使用 from\_self()，那么“having”子句将从内部复制到外部查询中。[¶](#change-060dd78afd33881d181eec9588947add)

    参考文献：[＃2130](http://www.sqlalchemy.org/trac/ticket/2130)

### 发动机[¶ T0\>](#change-0.6.7-engine "Permalink to this headline")

-   **[engine]**Fixed bug in QueuePool, SingletonThreadPool whereby
    connections that were discarded via overflow or periodic cleanup()
    were not explicitly closed, leaving garbage collection to the task
    instead. 这通常只影响像 Jython 和 Pypy 这样的非引用计数后端。感谢 Jaimy
    Azle 发现这一点。[¶](#change-47dcc1090d3314545b6a9690f9d74116)

    参考文献：[＃2102](http://www.sqlalchemy.org/trac/ticket/2102)

### SQL [¶ T0\>](#change-0.6.7-sql "Permalink to this headline")

-   **[sql]**Column.copy(), as used in table.tometadata(), copies the
    ‘doc’ attribute.[¶](#change-a275b5bc06266dc2cdf5221ac4efa4ae)

    参考文献：[＃2028](http://www.sqlalchemy.org/trac/ticket/2028)

-   **[sql]**增加了对 resultproxy.c 扩展的一些定义，以便扩展编译并在 Python
    2.4 上运行。[¶](#change-ad5304b19826c1a70051cdf7b77c35bc)

    参考文献：[＃2023](http://www.sqlalchemy.org/trac/ticket/2023)

-   **[sql]**The compiler extension now supports overriding the default
    compilation of expression.\_BindParamClause including that the
    auto-generated binds within the VALUES/SET clause of an
    insert()/update() statement will also use the new compilation
    rules.[¶](#change-5a0bb2e6701ec13c1651c09ef85839e5)

    参考文献：[＃2042](http://www.sqlalchemy.org/trac/ticket/2042)

-   **[sql]**为 ResultProxy 添加访问器“returns\_rows”，“is\_insert”[¶](#change-cd2a42bedeaff3d6db0e9583c7366c01)

    参考文献：[＃2089](http://www.sqlalchemy.org/trac/ticket/2089)

-   **[sql]** select()的 limit / offset 关键字以及传递给 select.limit()/
    offset()的值将强制为整数。[¶](#change-2f014c320217753b2e7338e74b17e074)

    参考文献：[＃2116](http://www.sqlalchemy.org/trac/ticket/2116)

### 的 PostgreSQL [¶ T0\>](#change-0.6.7-postgresql "Permalink to this headline")

-   **[postgresql]**When explicit sequence execution derives the name of
    the auto-generated sequence of a SERIAL column, which currently only
    occurs if implicit\_returning=False, now accommodates if the table +
    column name is greater than 63 characters using the same logic
    Postgresql uses.[¶](#change-ab73a9ae528ee69666fab4ec822db451)

    参考文献：[＃1083](http://www.sqlalchemy.org/trac/ticket/1083)

-   **[postgresql]**在“disconnect”异常列表中添加了额外的 libpq 消息，“无法从服务器接收数据”[¶](#change-0d9b1d5d5cbdcb0ca647c9b409c42200)

    参考文献：[＃2044](http://www.sqlalchemy.org/trac/ticket/2044)

-   **[postgresql]**为 postgresql 方言增加了 RESERVED\_WORDS。[¶](#change-934e48213c937d20f95930337f7e57e9)

    参考文献：[＃2092](http://www.sqlalchemy.org/trac/ticket/2092)

-   **[postgresql]**固定 BIT 类型以允许“长度”参数，“变化”参数。反射也是固定的。[¶](#change-9afcfc7fa95e4d1c05cc91e90f14074b)

    参考文献：[＃2073](http://www.sqlalchemy.org/trac/ticket/2073)

### MySQL 的[¶ T0\>](#change-0.6.7-mysql "Permalink to this headline")

-   **[mysql]**oursql dialect accepts the same “ssl” arguments in
    create\_engine() as that of
    MySQLdb.[¶](#change-694da80c3029deb8ea396e5708b75604)

    参考文献：[＃2047](http://www.sqlalchemy.org/trac/ticket/2047)

### 源码[¶ T0\>](#change-0.6.7-sqlite "Permalink to this headline")

-   **[sqlite]**Fixed bug where reflection of foreign key created as
    “REFERENCES ” without col name would
    fail.[¶](#change-ed6a6e71dbdafae0b4f6e0831116d94f)

    参考文献：[＃2115](http://www.sqlalchemy.org/trac/ticket/2115)

### MSSQL [¶ T0\>](#change-0.6.7-mssql "Permalink to this headline")

-   **[mssql]**Rewrote the query used to get the definition of a view,
    typically when using the Inspector interface, to use
    sys.sql\_modules instead of the information schema, thereby allowing
    views definitions longer than 4000 characters to be fully
    returned.[¶](#change-abb1e8cdc1c90914b2196c74eeb32842)

    参考文献：[＃2071](http://www.sqlalchemy.org/trac/ticket/2071)

### 预言[¶ T0\>](#change-0.6.7-oracle "Permalink to this headline")

-   **[oracle]**Using column names that would require quotes for the
    column itself or for a name-generated bind parameter, such as names
    with special characters, underscores, non-ascii characters, now
    properly translate bind parameter keys when talking to
    cx\_oracle.[¶](#change-52cfc9b390aeab5dad8108be21fb6c91)

    参考文献：[＃2100](http://www.sqlalchemy.org/trac/ticket/2100)

-   **[oracle]**Oracle dialect adds use\_binds\_for\_limits=False
    create\_engine() flag, will render the LIMIT/OFFSET values inline
    instead of as binds, reported to modify the execution plan used by
    Oracle.[¶](#change-a0b34ccb9b1535f2c510607844e32242)

    参考文献：[＃2116](http://www.sqlalchemy.org/trac/ticket/2116)

### 火鸟[¶ T0\>](#change-0.6.7-firebird "Permalink to this headline")

-   **[firebird]**如果设置为 False，create\_engine()上的“implicit\_returning”标志将被遵守。[¶](#change-c7435c028a162f66ad2348bf1b312568)

    参考文献：[＃2083](http://www.sqlalchemy.org/trac/ticket/2083)

### 杂项[¶ T0\>](#change-0.6.7-misc "Permalink to this headline")

-   **[informix]**新增 RESERVED\_WORDS
    informix 方言。[¶](#change-a13940d4af6ee75c1a62ada363719185)

    参考文献：[＃2092](http://www.sqlalchemy.org/trac/ticket/2092)

-   **[ext]** horizo​​ntal\_shard
    ShardedSession 类接受通用会话参数“query\_cls”作为构造函数参数，以启用 ShardedQuery 的进一步子类化。[¶](#change-1f8f8c315ffd15103961e7340c643cf5)

    参考文献：[＃2090](http://www.sqlalchemy.org/trac/ticket/2090)

-   **[declarative]**添加了对名称'metadata'用于声明类的列属性的明确检查。[¶](#change-d38e96868aa208c878f6a399209baa56)

    参考文献：[＃2050](http://www.sqlalchemy.org/trac/ticket/2050)

-   **[declarative]**修复引用旧@classproperty 名称引用@declared\_attr
    [¶](#change-04df06651398c4cc53b0100d0d7392f7)的错误消息

    参考文献：[＃2061](http://www.sqlalchemy.org/trac/ticket/2061)

-   **[declarative]**
    \_\_mapper\_args\_\_中不是“可排序”的参数不会被误认为是可以被哈希的可能列参数。[¶](#change-5a35bc6fcdaed2657acdf3a146f57944)

    参考文献：[＃2091](http://www.sqlalchemy.org/trac/ticket/2091)

-   **[documentation]**记录的 SQLite DATE / TIME /
    DATETIME 类型。[¶](#change-4d5a071f11cdecd01c76f3e46df9a46b)

    参考文献：[＃2029](http://www.sqlalchemy.org/trac/ticket/2029)

-   **[examples]**烧杯缓存示例允许 query\_callable()函数使用“query\_cls”参数。[¶](#change-6ad83653aed5df61bea17b14bda619f6)

    参考文献：[＃2090](http://www.sqlalchemy.org/trac/ticket/2090)

0.6.6 [¶ T0\>](#change-0.6.6 "Permalink to this headline")
----------------------------------------------------------

发布时间：2011 年 1 月 8 日

### ORM [¶ T0\>](#change-0.6.6-orm "Permalink to this headline")

-   **[orm]**Fixed bug whereby a non-“mutable” attribute modified event
    which occurred on an object that was clean except for preceding
    mutable attribute changes would fail to strongly reference itself in
    the identity map.
    这会导致对象被垃圾收集，失去了以前未保存在“可变更改”字典中的任何更改的跟踪。[¶](#change-73d44895e2706b7e163324b206400f33)

-   **[orm]**Fixed bug whereby “passive\_deletes=’all’” wasn’t passing
    the correct symbols to lazy loaders during flush, thereby causing an
    unwarranted load.[¶](#change-cc7c109cd2e5f972d7c361a19e549015)

    参考文献：[＃2013](http://www.sqlalchemy.org/trac/ticket/2013)

-   **[orm]**修正了阻止在映射的 select 语句上使用复合映射属性的错误。注意复合材料的工作原理将在 0.7 下显着改变。[¶](#change-a06e3ac0ceb000a16fd9ccd8151858a9)

    参考文献：[＃1997](http://www.sqlalchemy.org/trac/ticket/1997)

-   **[orm]**
    active\_history 标志也被添加到了 composite()中。该标志在 0.6 中没有效果，但是它是一个用于向前兼容的占位符标志，因为它适用于复合材料的 0.7.
    [](#change-78f279b93ff41fe6f4e382ab7a39d1dc)

    参考文献：[＃1976](http://www.sqlalchemy.org/trac/ticket/1976)

-   修正了传递给 Session.delete()的过期对象在删除对象时没有考虑到卸载的引用或集合的缺陷，尽管 passive\_deletes 保持默认的 False 状态。[**[orm]**
    T2\>](#change-e583324a8feefce60c8c25f58fb1489c)

    参考文献：[＃2002](http://www.sqlalchemy.org/trac/ticket/2002)

-   **[orm]**当继承映射器上指定 version\_id\_col 时，如果这些列表达式不相同，则会发出警告。[¶](#change-24a0a0f1cefec7af7929abec55c2677d)

    参考文献：[＃1987](http://www.sqlalchemy.org/trac/ticket/1987)

-   **[orm]**“innerjoin” flag doesn’t take effect along the chain of
    joinedload() joins if a previous join in that chain is an outer
    join, thus allowing primary rows without a referenced child row to
    be correctly returned in
    results.[¶](#change-950897823db98ee106b0d8ae719faea0)

    参考文献：[＃1954](http://www.sqlalchemy.org/trac/ticket/1954)

-   **[orm]**Fixed bug regarding “subqueryload” strategy whereby
    strategy would fail if the entity was an aliased()
    construct.[¶](#change-0a61da9c990ed25523ab57b8e6ff715f)

    参考文献：[＃1964](http://www.sqlalchemy.org/trac/ticket/1964)

-   **[orm]**Fixed bug regarding “subqueryload” strategy whereby the
    join would fail if using a multi-level load of the form from
    A-\>joined-subclass-\>C[¶](#change-1703b90dcfd7ffd0b4f81bcbb70c3d44)

    参考文献：[＃2014](http://www.sqlalchemy.org/trac/ticket/2014)

-   **[orm]**固定 Query 对象的索引值-1。它被错误地转换为导致 IndexError 的空片-1：0.
    [¶](#change-4a73b51d264c9ebf2bfe59749c653a7e)

    参考文献：[＃1968](http://www.sqlalchemy.org/trac/ticket/1968)

-   **[orm]**
    mapper 参数“primary\_key”可以作为单个列以及列表或元组传递。将其说明为标量值的文档示例已更改为列表。[¶](#change-99c12b8a201a49a117b4bb21da31173a)

    参考文献：[＃1971](http://www.sqlalchemy.org/trac/ticket/1971)

-   **[orm]**Added active\_history flag to relationship() and
    column\_property(), forces attribute events to always load the “old”
    value, so that it’s available to
    attributes.get\_history().[¶](#change-ff4076489a43c234bed638b787e33718)

    参考文献：[＃1961](http://www.sqlalchemy.org/trac/ticket/1961)

-   **[orm]**如果组合键中的参数数量太大，而且太小，则会引发 Query.get()。[¶](#change-0ff4a3f02593bf67a026324aec361fc5)

    参考文献：[＃1977](http://www.sqlalchemy.org/trac/ticket/1977)

-   **[orm]**从 0.7 开始的“优化 get”修复的后退，改善了加入继承“load expired
    row”行为的生成。[¶](#change-05860eb2ecae8e9521c06c989b36d3df)

    参考文献：[＃1992](http://www.sqlalchemy.org/trac/ticket/1992)

-   **[orm]**A little more verbiage to the “primaryjoin” error, in an
    unusual condition that the join condition “works” for viewonly but
    doesn’t work for non-viewonly, and foreign\_keys wasn’t used - adds
    “foreign\_keys” to the suggestion.
    也可以将“foreign\_keys”添加到通用“方向”错误的建议中。[¶](#change-dad16deefe860c0ae2a562ef161b1063)

### 发动机[¶ T0\>](#change-0.6.6-engine "Permalink to this headline")

-   **[engine]**现在，仅当明确使用 Unicode 类型时，才会引发针对非 Unicode 绑定数据的“unicode 警告”；而不是在引擎或字符串类型上使用 convert\_unicode
    = True 时[¶](#change-e344fa51f77920bcead6517070be003a)

-   **[engine]**固定内存泄漏在 C 版本的十进制结果处理器中。[¶](#change-060786b76864313d10ab31bd71a4aeb8)

    参考文献：[＃1978](http://www.sqlalchemy.org/trac/ticket/1978)

-   **[engine]**为 RowProxy 的 C 版本实现了序列检查功能，为 RowProxy 的 2.7 样式“collections.Sequence”注册。[¶](#change-a782cc312fd2acd3583135d10d33de6d)

    参考文献：[＃1871](http://www.sqlalchemy.org/trac/ticket/1871)

-   **[engine]**Threadlocal engine methods rollback(), commit(),
    prepare() won’t raise if no transaction is in progress; this was a
    regression introduced in
    0.6.[¶](#change-4d3bfa440284b95d35ecfb86606c4b1d)

    参考文献：[＃1998](http://www.sqlalchemy.org/trac/ticket/1998)

-   **[engine]**Threadlocal engine returns itself upon begin(),
    begin\_nested(); engine then implements contextmanager methods to
    allow the “with”
    statement.[¶](#change-bfd7df5b5e155908748f2e41fef4e6cb)

    参考文献：[＃2004](http://www.sqlalchemy.org/trac/ticket/2004)

### SQL [¶ T0\>](#change-0.6.6-sql "Permalink to this headline")

-   **[sql]**修复了单个非关联运算符的多个链的运算符优先规则。即“x - （y
    - z）”将编译为“x - （y - z）”而不是“x - y - z”。也适用于标签，即“x -
    （y -
    z）.label（'foo'）”[¶](#change-8501b4f05d5a273f29d09e5fda4682b4)

    参考文献：[＃1984](http://www.sqlalchemy.org/trac/ticket/1984)

-   **[sql]**The ‘info’ attribute of Column is copied during
    Column.copy(), i.e. as occurs when using columns in declarative
    mixins.[¶](#change-9329ac8a67c101712cc52dcd1ef51dfe)

    参考文献：[＃1967](http://www.sqlalchemy.org/trac/ticket/1967)

-   **[sql]**为布尔值增加了一个绑定处理器，这些布尔值强制为 int，而 DBAPI 如 pymssql 在值上天真地调用 str()。[¶](#change-313ab80f4ccba634879714775e2d1937)

-   **[sql]**CheckConstraint will copy its ‘initially’, ‘deferrable’,
    and ‘\_create\_rule’ attributes within a
    copy()/tometadata()[¶](#change-c6bca81c575803cd5d89152c9793de63)

    参考文献：[＃2000](http://www.sqlalchemy.org/trac/ticket/2000)

### 的 PostgreSQL [¶ T0\>](#change-0.6.6-postgresql "Permalink to this headline")

-   **[postgresql]**
    IN 子句中的单元素元组表达式正确地括起来，也来自[¶](#change-6dfbe255f49659e489e09c208c1d7bee)

    参考文献：[＃1984](http://www.sqlalchemy.org/trac/ticket/1984)

-   **[postgresql]**确保 psycopg2 和 pg8000 的“数字”基本类型能够识别每个数字，浮点数，整型代码和标量数组。[¶](#change-55c1f840b71087d0e09bb8bc2afa14e4)

    参考文献：[＃1955](http://www.sqlalchemy.org/trac/ticket/1955)

-   **[postgresql]**将 asuuid = True 标志添加到 UUID 类型，将以 Python
    UUID()对象而不是字符串的形式接收和返回值。目前，UUID 类型只能用于 psycopg2.
    [¶](#change-0e07e9da5e3d2dc702aaf8213f255dc2)

    参考文献：[＃1956](http://www.sqlalchemy.org/trac/ticket/1956)

-   **[postgresql]**修正了在池配置+重新创建之后会发生 KeyError 的非 ENUM 支持 PG 版本的问题。[¶](#change-6f1e93205663537c4ef282d5cfc3edef)

    参考文献：[＃1989](http://www.sqlalchemy.org/trac/ticket/1989)

### MySQL 的[¶ T0\>](#change-0.6.6-mysql "Permalink to this headline")

-   **[mysql]**修复了 Jython +
    zxjdbc 的错误处理问题，使得 has\_table()属性再次运行。从 0.6.3 回归（我们没有 Jython
    buildbot，对不起）[¶](#change-15404de376dfeacb313c1bcb2ee66a33)

    参考文献：[＃1960](http://www.sqlalchemy.org/trac/ticket/1960)

### 源码[¶ T0\>](#change-0.6.6-sqlite "Permalink to this headline")

-   **[sqlite]** CREATE
    TABLE 中的 REFERENCES 子句，包含具有相同模式名称的另一个表的远程模式，现在根据 SQLite 的要求呈现没有模式子句的远程名称[¶\<
    / T2\>](#change-6d83957f57c2e3d7f41b95967ddb322c)

    参考文献：[＃1851](http://www.sqlalchemy.org/trac/ticket/1851)

-   **[sqlite]**On the same theme, the REFERENCES clause in a CREATE
    TABLE that includes a remote schema to a *different* schema than
    that of the parent table doesn’t render at all, as cross-schema
    references do not appear to be
    supported.[¶](#change-c7c69439e2cc0ec7af6b3dffa8a3a86f)

### MSSQL [¶ T0\>](#change-0.6.6-mssql "Permalink to this headline")

-   **[mssql]**不幸的是没有正确地测试索引反射的重写，并返回了不正确的结果。现在这个回归是固定的。[¶](#change-445f4c11a73f0a2d7a02c8297f45a174)

    参考文献：[＃1770](http://www.sqlalchemy.org/trac/ticket/1770)

### 预言[¶ T0\>](#change-0.6.6-oracle "Permalink to this headline")

-   **[oracle]**现在使用由语言环境/
    NLS\_LANG 设置确定的小数点字符的 cx\_oracle“十进制检测”逻辑，它使用具有模糊数字特征的结果集列，连接这个字符的检测。使用非周期小数点 NLS\_LANG 设置时，还需要 cx\_oracle
    5.0.3 或更高版本。[¶](#change-2ccadf16ce306a495b45d7e349e3a56d)

    参考文献：[＃1953](http://www.sqlalchemy.org/trac/ticket/1953)

### 火鸟[¶ T0\>](#change-0.6.6-firebird "Permalink to this headline")

-   **[firebird]**Firebird numeric type now checks for Decimal
    explicitly, lets float() pass right through, thereby allowing
    special values such as
    float(‘inf’).[¶](#change-cefc7fd8608289b2871c372d3f415aa1)

    参考文献：[＃2012](http://www.sqlalchemy.org/trac/ticket/2012)

### 杂项[¶ T0\>](#change-0.6.6-misc "Permalink to this headline")

-   **[declarative]**如果\_\_table\_args\_\_不是 tuple 或 dict 格式，并且不是 None，则会产生错误。[¶](#change-1c894bdd6f1952bc473239bc08a14b89)

    参考文献：[＃1972](http://www.sqlalchemy.org/trac/ticket/1972)

-   **[sqlsoup]**Added “map\_to()” method to SqlSoup, which is a
    “master” method which accepts explicit arguments for each aspect of
    the selectable and mapping, including a base class per
    mapping.[¶](#change-589cc5d2ae80b9d8ba7435234c630b85)

    参考文献：[＃1975](http://www.sqlalchemy.org/trac/ticket/1975)

-   **[sqlsoup]**与 map()，with\_labels()，join()方法一起使用的 mapable
    selectables 不再将给定的参数放到内部的“cache”字典中。特别是由于 join()和 select()对象是在方法本身中创建的，这几乎是纯粹的内存泄漏行为。[¶](#change-c8bc4f5b37cc4e77cd766cce0179426c)

-   **[examples]**版本示例现在支持检测关联关系()中的更改。[¶](#change-cdab141baa9b101f65543811538eaad3)

0.6.5 [¶ T0\>](#change-0.6.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2010 年 10 月 24 日

### ORM [¶ T0\>](#change-0.6.5-orm "Permalink to this headline")

-   **[orm]**添加了一个新的“lazyload”选项“immediateload”。在填充对象时自动发出通常的“懒惰”加载操作。这里的用例是加载要放置在脱机缓存中的对象，或者在会话不可用之后以其他方式使用，并且希望直接“选择”加载，而不是“加入”或“子查询”。[¶
    T0\>](#change-05ec37b51f434e62c267fe20d4e58c7e)

    参考文献：[＃1914](http://www.sqlalchemy.org/trac/ticket/1914)

-   **[orm]**New Query methods: query.label(name), query.as\_scalar(),
    return the query’s statement as a scalar subquery with /without
    label; query.with\_entities(\*ent), replaces the SELECT list of the
    query with new entities.
    大致相当于 query.values()的生成形式，它接受映射的实体以及列表达式。[¶](#change-10955dae4ce54a020b91ac0a8757e360)

    参考文献：[＃1920](http://www.sqlalchemy.org/trac/ticket/1920)

-   **[orm]**Fixed recursion bug which could occur when moving an object
    from one reference to another, with backrefs involved, where the
    initiating parent was a subclass (with its own mapper) of the
    previous parent.[¶](#change-d784a2da322b348050aefe3c6258ba39)

-   **[orm]**Fixed a regression in 0.6.4 which occurred if you passed an
    empty list to “include\_properties” on
    mapper()[¶](#change-6af93b4a17eb71913cf760ae65958264)

    参考文献：[＃1918](http://www.sqlalchemy.org/trac/ticket/1918)

-   **[orm]**在 Query 中固定标签错误，NamedTuple 会在任何列表达式未标记时错误应用标签。[¶](#change-b79708d8c7a705b6ac80798508585034)

-   **[orm]**修补了 query.join()将不恰当地调整左侧连接的右侧到右侧的情况[¶](#change-3ce4439ac51efb211009bf9295f36135)

    参考文献：[＃1925](http://www.sqlalchemy.org/trac/ticket/1925)

-   **[orm]**Query.select\_from() has been beefed up to help ensure that
    a subsequent call to query.join() will use the select\_from()
    entity, assuming it’s a mapped entity and not a plain selectable, as
    the default “left” side, not the first entity in the Query object’s
    list of entities.[¶](#change-2520d6ed386bd5f52025b2ea26acaf3c)

-   **[orm]**The exception raised by Session when it is used subsequent
    to a subtransaction rollback (which is what happens when a flush
    fails in autocommit=False mode) has now been reworded (this is the
    “inactive due to a rollback in a subtransaction” message).
    特别是，如果回滚是由 flush()期间的异常引起的，则消息说明是这种情况，并重申在刷新期间发生的原始异常的字符串形式。如果会话由于明确使用了子事务（不是很常见）而被关闭，那么消息只是说明了这种情况。[¶](#change-6ac225a74a7670ddfe45fd42b639020c)

-   **[orm]**The exception raised by Mapper when repeated requests to
    its initialization are made after initialization already failed no
    longer assumes the “hasattr” case, since there’s other scenarios in
    which this message gets emitted, and the message also does not
    compound onto itself multiple times - you get the same message for
    each attempt at usage.
    “编译”这个用词不当的情况正在被用于“初始化”。[¶](#change-d238e9c9585eb81bc60ff2f4cd32320f)

-   **[orm]**Fixed bug in query.update() where ‘evaluate’ or ‘fetch’
    expiration would fail if the column expression key was a class
    attribute with a different keyname as the actual column
    name.[¶](#change-9ec0c4f2f483bf5d304f33c8593de5d9)

    参考文献：[＃1935](http://www.sqlalchemy.org/trac/ticket/1935)

-   **[orm]**在刷新过程中添加了一个断言，确保在“新持久性”对象上不生成持有空值的身份密钥。这可能发生在用户定义的代码无意中触发未完全加载的对象上的刷新。[¶](#change-d84b4cf05c01f57aba9894d09098d696)

-   **[orm]**lazy loads for relationship attributes now use the current
    state, not the “committed” state, of foreign and primary key
    attributes when issuing SQL, if a flush is not in process.
    以前，只会使用数据库提交状态。特别是，这会导致多对一的 get() -
    on-lazyload 操作失败，因为当这些属性被确定并且“提交”状态可能不可用时，autoflush 不会在这些负载上触发。[¶
    T0\>](#change-83d77852281b4f90915f5a66c5aeb2f4)

    参考文献：[＃1910](http://www.sqlalchemy.org/trac/ticket/1910)

-   **[orm]**A new flag on relationship(), load\_on\_pending, allows the
    lazy loader to fire off on pending objects without a flush taking
    place, as well as a transient object that’s been manually “attached”
    to the session.
    请注意，此标志会阻止加载对象时发生的属性事件，因此直到冲刷后才能使用 backrefs。该标志仅用于非常具体的用例。[¶](#change-54bd435e0495c759195b5a89782f09f3)

-   **[orm]**Another new flag on relationship(), cascade\_backrefs,
    disables the “save-update” cascade when the event was initiated on
    the “reverse” side of a bidirectional relationship.
    这是一种更清晰的行为，因此可以将多对一设置为临时对象，而不会将其吸引到子对象的会话中，同时仍允许向前集合级联。我们*可能*在 0.7 中默认为 False。[¶](#change-080a574eb24dbc2249cb0cf42cd0c506)

-   **[orm]**当仅放置在关系的多对一侧时，对“passive\_updates =
    False”的行为稍作改进；文档已经澄清，passive\_updates =
    False 应该是一对多的。[¶](#change-cd1698eb18bf61cf0da5afee7a5e7c4a)

-   **[orm]**在多对一的情况下放置 passive\_deletes =
    True 会发出警告，因为您可能打算将它放在一对多的一面。[¶](#change-cad7611b381713d7cffe14e33ee704bf)

-   **[orm]**Fixed bug that would prevent “subqueryload” from working
    correctly with single table inheritance for a relationship from a
    subclass - the “where type in (x, y, z)” only gets placed on the
    inside, instead of
    repeatedly.[¶](#change-6b88ae16dd7b28d9830d7684992e3cb7)

-   **[orm]**When using from\_self() with single table inheritance, the
    “where type in (x, y, z)” is placed on the outside of the query
    only, instead of repeatedly.
    可以对此进行更多的调整。[¶](#change-34f0bff0696715bf8cb3e59f6d10b4bb)

-   **[orm]**scoped\_session emits a warning when configure() is called
    if a Session is already present (checks only the current
    thread)[¶](#change-b008ec0e6f859c0904e7abd78a62457f)

    参考文献：[＃1924](http://www.sqlalchemy.org/trac/ticket/1924)

-   **[orm]**reworked the internals of mapper.cascade\_iterator() to cut
    down method calls by about 9% in some
    circumstances.[¶](#change-63bb35cc7429215a5a693a352a838a9b)

    参考文献：[＃1932](http://www.sqlalchemy.org/trac/ticket/1932)

### 发动机[¶ T0\>](#change-0.6.5-engine "Permalink to this headline")

-   **[engine]**固定了 0.6.4 中的回归，因此允许光标错误一致的更改一直打破了 result.lastrowid 访问器。已为 result.lastrowid 添加了测试覆盖率。请注意，lastrowid 仅由 Pysqlite 和一些 MySQL 驱动程序支持，因此在一般情况下不会超级有用。[¶](#change-1059318af334dfde665aff47590e8542)

-   **[engine]**the logging message emitted by the engine when a
    connection is first used is now “BEGIN (implicit)” to emphasize that
    DBAPI has no explicit
    begin().[¶](#change-ebd200888550cee6694d854883573fa6)

-   **[engine]**在 metadata.reflect()中添加了“views =
    True”选项，将可用视图的列表添加到正在反映的视图中。[¶](#change-583d616a6e6d2ed7c2874a91f7e8b83a)

    参考文献：[＃1936](http://www.sqlalchemy.org/trac/ticket/1936)

-   **[engine]**engine\_from\_config() now accepts ‘debug’ for ‘echo’,
    ‘echo\_pool’, ‘force’ for ‘convert\_unicode’, boolean values for
    ‘use\_native\_unicode’.[¶](#change-50d5bffb777603ddce658a6a67b8e205)

    参考文献：[＃1899](http://www.sqlalchemy.org/trac/ticket/1899)

### SQL [¶ T0\>](#change-0.6.5-sql "Permalink to this headline")

-   **[sql]**Fixed bug in TypeDecorator whereby the dialect-specific
    type was getting pulled in to generate the DDL for a given type,
    which didn’t always return the correct
    result.[¶](#change-38a4e7cd800b41adf3d50801a7f7cb1b)

-   **[sql]**TypeDecorator can now have a fully constructed type
    specified as its “impl”, in addition to a type
    class.[¶](#change-1f4462b0b5fe565c42d2a26adc200c72)

-   **[sql]**TypeDecorator will now place itself as the resulting type
    for a binary expression where the type coercion rules would normally
    return its impl type - previously, a copy of the impl type would be
    returned which would have the TypeDecorator embedded into it as the
    “dialect” impl, this was probably an unintentional way of achieving
    the desired effect.[¶](#change-9dc92f16ad4db3c34c0aa4eae14c851f)

-   **[sql]**TypeDecorator.load\_dialect\_impl() returns “self.impl” by
    default, i.e. not the dialect implementation type of “self.impl”.
    这可以正确支持编译。行为可以像以前一样以相同的方式被用户覆盖，达到同样的效果。[¶](#change-2b8e904daae0d182fbf0aaa6bca9d64b)

-   **[sql]**添加了 type\_coerce（expr，type\_）表达式元素。在评估表达式和处理结果行时将给定表达式视为给定类型，但不影响除匿名标签之外的 SQL 生成。[¶](#change-29fd8b04b0c6aef95c9455c804c96892)

-   **[sql]**Table.tometadata() now copies Index objects associated with
    the Table as well.[¶](#change-6c855e196152b57c304b333e9770fa07)

-   **[sql]**Table.tometadata() issues a warning if the given Table is
    already present in the target MetaData - the existing Table object
    is returned.[¶](#change-81cb47d5917f4a66ca50b654ececaf77)

-   **[sql]**An informative error message is raised if a Column which
    has not yet been assigned a name, i.e. as in declarative, is used in
    a context where it is exported to the columns collection of an
    enclosing select() construct, or if any construct involving that
    column is compiled before its name is
    assigned.[¶](#change-6c2eaa8e6ce7b6c71555f1222eccbb27)

-   **[sql]**as\_scalar(), label() can be called on a selectable which
    contains a Column that is not yet
    named.[¶](#change-69ad40851eefcd610d8d70ebd3511697)

    参考文献：[＃1862](http://www.sqlalchemy.org/trac/ticket/1862)

-   **[sql]**Fixed recursion overflow which could occur when operating
    with two expressions both of type “NullType”, but not the singleton
    NULLTYPE instance.[¶](#change-fcb44a57a6160aab1d8c4e8427c9b044)

    参考文献：[＃1907](http://www.sqlalchemy.org/trac/ticket/1907)

### 的 PostgreSQL [¶ T0\>](#change-0.6.5-postgresql "Permalink to this headline")

-   **[postgresql]**将“as\_tuple”标志添加到 ARRAY 类型，并将结果作为元组返回，而不是列表以允许哈希。[¶](#change-4d094ee39f2d2bfb4cbd1e9cd2912640)

-   **[postgresql]**修正了防止自定义类型（例如“enum”）构建的“域”被反射的错误。[¶](#change-5b9e6f2e203f6ec007fcf90d5d5d9e90)

    参考文献：[＃1933](http://www.sqlalchemy.org/trac/ticket/1933)

### MySQL 的[¶ T0\>](#change-0.6.5-mysql "Permalink to this headline")

-   **[mysql]**Fixed bug involving reflection of CURRENT\_TIMESTAMP
    default used with ON UPDATE clause, thanks to Taavi
    Burns[¶](#change-e8d0855d359fcbb93416e1b0988fdb8e)

    参考文献：[＃1940](http://www.sqlalchemy.org/trac/ticket/1940)

### MSSQL [¶ T0\>](#change-0.6.5-mssql "Permalink to this headline")

-   **[mssql]**修正了未能正确处理未知类型反射的反射问题。[¶](#change-f16e997950ea6bca39c0a059887dfbfd)

    参考文献：[＃1946](http://www.sqlalchemy.org/trac/ticket/1946)

-   **[mssql]**修正了使用“schema”对表进行别名失败时无法正确编译的错误。[¶](#change-022e82021b20bc2c059207eb8b7234af)

    参考文献：[＃1943](http://www.sqlalchemy.org/trac/ticket/1943)

-   **[mssql]**重写索引的反射以使用 sys。目录，以便任何配置的列名（空格，嵌入逗号等）可以反映出来。请注意，索引的反映需要 SQL
    Server 2005 或更高版本。[¶](#change-9f19687a241d918bf9dd03d0cc3ff3ed)

    参考文献：[＃1770](http://www.sqlalchemy.org/trac/ticket/1770)

-   **[mssql]**现在 mssql +
    pymssql 方言尊重 URL 的“端口”部分，而不是放弃它。[¶](#change-ffe886676fb15f105e1a8cc37dfb6f9d)

    参考文献：[＃1952](http://www.sqlalchemy.org/trac/ticket/1952)

### 预言[¶ T0\>](#change-0.6.5-oracle "Permalink to this headline")

-   **[oracle]**无论检测到 Oracle 的版本，现在都可以使用 create\_engine()的 implicit\_retunring 参数。以前，如果服务器版本信息\<10，那么该标志将被强制为 false。¶

    参考文献：[＃1878](http://www.sqlalchemy.org/trac/ticket/1878)

### 杂项[¶ T0\>](#change-0.6.5-misc "Permalink to this headline")

-   **[declarative]**
    @classproperty（很快/现在@declared\_attr）对不是 mixin 的基类中的\_\_mapper\_args\_\_，\_\_table\_args\_\_，\_\_tablename\_\_生效，以及 mixins
    [¶](#change-b19f9aa816f9e63c03fa209095e76f51)

    参考文献：[＃1922](http://www.sqlalchemy.org/trac/ticket/1922)

-   **[declarative]**@classproperty ‘s official name/location for usage
    with declarative is sqlalchemy.ext.declarative.declared\_attr.
    同样的事情，但它在那里移动，因为它更像是一个特定于声明的“标记”，而不仅仅是一种属性技术。[¶](#change-b9792dc15f6375711ec84bb73ae74272)

    参考文献：[＃1915](http://www.sqlalchemy.org/trac/ticket/1915)

-   **[declarative]**Fixed bug whereby columns on a mixin wouldn’t
    propagate correctly to a single-table, or joined-table, inheritance
    scheme where the attribute name is different than that of the
    column.,.[¶](#change-172b80261166fbfb39ffe45d8499afe2)

    参考文献：[＃1931](http://www.sqlalchemy.org/trac/ticket/1931)，[＃1930](http://www.sqlalchemy.org/trac/ticket/1930)

-   **[declarative]**现在，mixin 可以指定一个覆盖与超类关联的同名列的列。感谢 Oystein
    Haaland。[¶](#change-b0075b372f99003ca5b69e678f306150)

-   **[informix]** *主要*清理/更新 Informix 方言 0.6，礼貌 Florian
    Apolloner。[](#change-8af323a4cf559c67e71f9b667f9548f5)

    参考文献：[＃1906](http://www.sqlalchemy.org/trac/ticket/1906)

-   **[tests]**
    NoseSQLAlchemyPlugin 已经被移动到一个新的包“sqlalchemy\_nose”中，它与“sqlalchemy”一起安装。这样，“nosetests”脚本将一如既往地工作，但也允许-with-coverage 选项在导入 SQLAlchemy 模块之前打开覆盖范围，从而使 coverage 能够正常工作。[¶](#change-e6cb2547ce70b9a4f2dec84481578326)

-   **[misc]**CircularDependencyError now has .cycles and .edges
    members, which are the set of elements involved in one or more
    cycles, and the set of edges as
    2-tuples.[¶](#change-2643e47a8fea315fd31765418be4607e)

    参考文献：[＃1890](http://www.sqlalchemy.org/trac/ticket/1890)

0.6.4 [¶ T0\>](#change-0.6.4 "Permalink to this headline")
----------------------------------------------------------

发布于：2010 年 9 月 07 日

### ORM [¶ T0\>](#change-0.6.4-orm "Permalink to this headline")

-   **[orm]**名称 ConcurrentModificationError 已更改为 StaleDataError，并且已修改描述性错误消息以准确反映问题所在。对于可能在“except：”子句中指定 ConcurrentModificationError 的方案，这两个名称仍可用于可预见的未来。[¶](#change-535033df965223821f740fe36bbc21c8)

-   **[orm]**为身份映射添加了一个互斥体，该互斥体可以针对迭代方法移除操作，而迭代方法现在在返回可迭代之前预缓冲。这是因为 asyncrhonous
    gc 可以随时通过 gc 线程移除项目。[¶](#change-c8ed6002ef9d50947734327801710649)

    参考文献：[＃1891](http://www.sqlalchemy.org/trac/ticket/1891)

-   **[orm]**
    Session 类现在存在于 sqlalchemy.orm。\*中。对于那些需要一步式 Session 构造函数的情况，我们不再使用具有非标准默认值的 create\_session()。然而，大多数用户应该坚持使用 sessionmaker()。[¶](#change-c30b33f0a0466c41b96742c2e74aad91)

-   **[orm]**query.with\_parent() now accepts transient objects and will
    use the non-persistent values of their pk/fk attributes in order to
    formulate the criterion.
    文档还阐明了 with\_parent()。[¶](#change-8dff7e6fded59f4fa37d00624eb71bed)的用途

-   **[orm]**除了字符串之外，mapper()的 include\_properties 和 exclude\_properties 参数现在还接受 Column 对象作为成员。这样可以区分名称相同的 Column 对象，例如 join()中的对象。[¶](#change-2638d82e47303db82e79a9e5c1361b30)

-   **[orm]**如果映射器是针对连接或其他单个可选项（包含多个在其.c 中具有相同名称的列）创建的，则会发出警告。集合，并且这些列没有明确命名为相同或独立属性的一部分（或排除在外）。在 0.7 这个警告将是一个例外。请注意，由于继承而导致组合发生时，不会发出此警告，因此属性仍允许自然被覆盖。在 0.7 中，这会进一步改善。[¶](#change-96944473a095ce6dfc07cbc71640f1d9)

    参考文献：[＃1896](http://www.sqlalchemy.org/trac/ticket/1896)

-   **[orm]**
    mapper()的 primary\_key 参数现在可以指定一系列列，它们只是映射可选项的计算“主键”列的子集，不会引发错误。这有助于可选择的有效主键比可选中实际标记为“primary\_key”的列的数量更简单的情况，例如与主键列上的两个表的联接。[¶](#change-95c2749ceb65bb793c5d3667b070c596)

    参考文献：[＃1896](http://www.sqlalchemy.org/trac/ticket/1896)

-   **[orm]**An object that’s been deleted now gets a flag ‘deleted’,
    which prohibits the object from being re-add()ed to the session, as
    previously the object would live in the identity map silently until
    its attributes were accessed.
    make\_transient()函数现在会重置此标志以及“key”标志。[¶](#change-fa24485df7e6bb87af279c1ebf82e0ec)

-   **[orm]**
    make\_transient()可以在已经是瞬态的实例上安全地调用。[¶](#change-a8fc0dce447503a22a961b5cf7d20ae8)

-   **[orm]**a warning is emitted in mapper() if the polymorphic\_on
    column is not present either in direct or derived form in the mapped
    selectable or in the with\_polymorphic selectable, instead of
    silently ignoring it.
    寻找这个在 0.7 中成为例外。[¶](#change-6b78024db59658489dadbac75c893b54)

-   **[orm]**Another pass through the series of error messages emitted
    when relationship() is configured with ambiguous arguments.
    “foreign\_keys”设置不再提及，因为它几乎不需要，因此用户最好设置正确的 ForeignKey 元数据，这是现在的建议。如果使用'foreign\_keys'并且不正确，则消息表明该属性可能是不必要的。该属性的文档得到了加强。这是因为 ML 上的所有混淆的关系()用户似乎都尝试使用 foreign\_keys，这是由于表元数据更加清晰，这只会使他们更加混淆。[¶](#change-4714288dd0e270666ddd8fcd21827ebc)

-   **[orm]**If the “secondary” table has no ForeignKey metadata and no
    foreign\_keys is set, even though the user is passing screwed up
    information, it is assumed that primary/secondaryjoin expressions
    should consider only and all cols in “secondary” to be foreign.
    在任何情况下，外键都不在其他位置。现在发出警告而不是错误，并且映射成功。[¶](#change-0c977ba4a7beb44f73ec46ff9a6699ac)

    参考文献：[＃1877](http://www.sqlalchemy.org/trac/ticket/1877)

-   **[orm]**Moving an o2m object from one collection to another, or
    vice versa changing the referenced object by an m2o, where the
    foreign key is also a member of the primary key, will now be more
    carefully checked during flush if the change in value of the foreign
    key on the “many” side is the result of a change in the primary key
    of the “one” side, or if the “one” is just a different object.
    在一个案例中，级联数据库可能已经级联了该值，我们需要查看“新”PK 值来执行 UPDATE，而另一个我们需要继续查看“旧”数据库。我们现在看一下“旧”，假设 passive\_updates
    =
    True，除非我们知道这是一个 PK 开关触发了这个变化。[¶](#change-9feca02adf52a0e5fcf4763b9b262443)

    参考文献：[＃1856](http://www.sqlalchemy.org/trac/ticket/1856)

-   **[orm]**
    version\_id\_col 的值可以手动更改，这将导致该行的 UPDATE。版本化的 UPDATE 和 DELETE 现在使用 WHERE 子句中的 version\_id\_col 的“落实”值，而不是挂起的更改值。如果在属性上存在手动更改，版本生成器也会被绕过。[¶](#change-7b40a0ed4bb3ad00531e5ece518709c2)

    参考文献：[＃1857](http://www.sqlalchemy.org/trac/ticket/1857)

-   **[orm]**在与具体继承映射器一起使用时修复了 merge()的用法。这样的映射器通常具有所谓的“具体”属性，这些属性是“禁止”父级传播的子类属性
    -
    这些属性允许 merge()操作无需通过就可以传递。[¶](#change-8665092a2dcfbeb8cfd12fb215aaa1e2)

-   **[orm]**Specifying a non-column based argument for
    column\_mapped\_collection, including string, text() etc., will
    raise an error message that specifically asks for a column element,
    no longer misleads with incorrect information about text() or
    literal().[¶](#change-4510836f41e7d0aacd0767c13db1d59b)

    参考文献：[＃1863](http://www.sqlalchemy.org/trac/ticket/1863)

-   **[orm]**Similarly, for relationship(), foreign\_keys, remote\_side,
    order\_by - all column-based expressions are enforced - lists of
    strings are explicitly disallowed since this is a very common
    error[¶](#change-671bef71f312d0040b6a4caf49decd77)

-   **[orm]**Dynamic attributes don’t support collection population -
    added an assertion for when set\_committed\_value() is called, as
    well as when joinedload() or subqueryload() options are applied to a
    dynamic attribute, instead of failure / silent
    failure.[¶](#change-ca14d6f9dcfb96b5f02b1a2ef13fa35d)

    参考文献：[＃1864](http://www.sqlalchemy.org/trac/ticket/1864)

-   **[orm]**Fixed bug whereby generating a Query derived from one which
    had the same column repeated with different label names, typically
    in some UNION situations, would fail to propagate the inner columns
    completely to the outer
    query.[¶](#change-d81765c5426dca3b1ec2a2f05a542dbb)

    参考文献：[＃1852](http://www.sqlalchemy.org/trac/ticket/1852)

-   **[orm]**object\_session() raises the proper UnmappedInstanceError
    when presented with an unmapped
    instance.[¶](#change-8519514b873baed592912155c0427a1e)

    参考文献：[＃1881](http://www.sqlalchemy.org/trac/ticket/1881)

-   **[orm]**对计算的 Mapper 属性应用进一步的记忆，在大量多态映射配置中，重要的（〜90％）运行时 mapper.py 调用计数减少。[¶](#change-e79a357376a117fe672113952bbe015b)

-   **[orm]**版本控制示例使用的 mapper
    \_get\_col\_to\_prop 私有方法已被弃用；现在使用 mapper.get\_property\_by\_column()，它仍然是公共方法。[¶](#change-a71fab65be706a5c214db3ca5b3abbb9)

-   **[orm]**版本控制示例现在可以正常工作，如果在以前为 NULL 的 col 上进行版本控制。[¶](#change-8d5f4593adc4160b12a49dcee66d174f)

### 发动机[¶ T0\>](#change-0.6.4-engine "Permalink to this headline")

-   **[engine]**Calling fetchone() or similar on a result that has
    already been exhausted, has been closed, or is not a
    result-returning result now raises ResourceClosedError, a subclass
    of InvalidRequestError, in all cases, regardless of backend.
    以前，一些 DBAPI 会引发 ProgrammingError（即 pysqlite），而其他 DBAPI 会返回 None 导致下游破坏（即 MySQL-python）。[¶](#change-589479e3126e16088d4e863148a31849)

-   **[engine]**Fixed bug in Connection whereby if a “disconnect” event
    occurred in the “initialize” phase of the first connection pool
    connect, an AttributeError would be raised when the Connection would
    attempt to invalidate the DBAPI
    connection.[¶](#change-0c3f6fab852e973ab1d2ba1c54362a92)

    参考文献：[＃1894](http://www.sqlalchemy.org/trac/ticket/1894)

-   **[engine]**连接，ResultProxy 以及 Session 使用 ResourceClosedError 为所有“此连接/事务/结果为关闭”类型的错误。[¶](#change-ab05177ef559d382cd656f5e04d11148)

-   **[engine]**可以多次调用 Connection.invalidate()，随后的调用什么也不做。[¶](#change-d4066423ccfa075735e1ebf61f2cbc24)

### SQL [¶ T0\>](#change-0.6.4-sql "Permalink to this headline")

-   **[sql]**Calling execute() on an alias() construct is pending
    deprecation for 0.7, as it is not itself an “executable” construct.
    它目前“代理”了它的内部元素，并且有条件地“可执行”，但这并不是我们现在喜欢的那种模糊性。[¶](#change-480b20f80312b137c4a7324b0d657a63)

-   **[sql]**
    ClauseElement 的 execute()和 scalar()方法现在可以适当地移动到 Executable 子类中。ClauseElement.execute()/
    scalar()仍然存在，并且在 0.7 中处于待弃用状态，但是请注意，如果您不是可执行文件，它们总是会引发错误（除非您是别名()，请参阅前面的注释）[¶
    T0\>](#change-eb5f51e1a650e79182bb020de761924f)

-   **[sql]**为 Numeric-\>
    Integer 添加了基本的数学表达式强制，所以无论表达式的方向如何，结果类型都是 Numeric。[¶](#change-95e0aca2331a7b95d533d515094ccb13)

-   **[sql]**在列上使用“index =
    True”标志时，更改了用于生成截断的“auto”索引名称的方案。截断只能使用自动生成的名称进行，而不是用户定义的名称（而不是用户定义的错误），截断方案本身现在基于标识符名称的 md5 哈希碎片，因此具有相似名称的列上的多个索引仍具有唯一名称。[¶](#change-a584b4c246f0f778263d5dc8e66808ad)

    参考文献：[＃1855](http://www.sqlalchemy.org/trac/ticket/1855)

-   **[sql]**The generated index name also is based on a “max index name
    length” attribute which is separate from the “max identifier length”
    - this to appease MySQL who has a max length of 64 for index names,
    separate from their overall max length of
    255.[¶](#change-cdd20195fab17091c475b43262749a74)

    参考文献：[＃1412](http://www.sqlalchemy.org/trac/ticket/1412)

-   **[sql]**the text() construct, if placed in a column oriented
    situation, will at least return NULLTYPE for its type instead of
    None, allowing it to be used a little more freely for ad-hoc column
    expressions than before.
    然而，literal\_column()仍然是更好的选择。[¶](#change-e0733f3fbe5188168ab9fc6dd0040998)

-   **[sql]**当 ForeignKey 无法解析目标时，添加对父表/列，目标表/列的错误消息中的完整描述[¶](#change-be54ec2b3e2eb3de741a48665fe37d51)

-   **[sql]**Fixed bug whereby replacing composite foreign key columns
    in a reflected table would cause an attempt to remove the reflected
    constraint from the table a second time, raising a
    KeyError.[¶](#change-95d89e7a08c42c04836f4ec67f236a9f)

    参考文献：[＃1865](http://www.sqlalchemy.org/trac/ticket/1865)

-   **[sql]**the \_Label construct, i.e. the one that is produced
    whenever you say somecol.label(), now counts itself in its
    “proxy\_set” unioned with that of its contained column’s proxy set,
    instead of directly returning that of the contained column.
    这允许依赖于\_Labels 本身身份的列对应操作返回正确的结果[¶](#change-0a8949e6824cfb04db55beb3e85e4aed)

-   **[sql]**修复了 ORM
    bug。[¶](#change-babee0cfb69d9dbe635ee89deaa616d3)

    参考文献：[＃1852](http://www.sqlalchemy.org/trac/ticket/1852)

### 的 PostgreSQL [¶ T0\>](#change-0.6.4-postgresql "Permalink to this headline")

-   **[postgresql]**Fixed the psycopg2 dialect to use its
    set\_isolation\_level() method instead of relying upon the base “SET
    SESSION ISOLATION” command, as psycopg2 resets the isolation level
    on each new transaction
    otherwise.[¶](#change-f20cfbd769e0d3362affb83971075073)

### MSSQL [¶ T0\>](#change-0.6.4-mssql "Permalink to this headline")

-   **[mssql]**修正了“default
    schema”查询与 pymssql 后端一起工作的问题。[¶](#change-653ce1cee9e040e6cd9de66cc99d034d)

### 预言[¶ T0\>](#change-0.6.4-oracle "Permalink to this headline")

-   **[oracle]**对于那些可能需要显式 CAST 的情况，向 Oracle 方言添加 ROWID 类型。[¶](#change-c4096e037bacbf97eddd92b0034f98ca)

    参考文献：[＃1879](http://www.sqlalchemy.org/trac/ticket/1879)

-   **[oracle]**Oracle reflection of indexes has been tuned so that
    indexes which include some or all primary key columns, but not the
    same set of columns as that of the primary key, are reflected.
    包含与主键相同的列的索引在反射内跳过，因为在这种情况下索引被假定为自动生成的主键索引。以前，PK 列存在的任何索引都会被跳过。感谢 Kent
    Bower 提供的补丁。[¶](#change-0c48f10bbe06c8a4b97b10e3f86708d7)

    参考文献：[＃1867](http://www.sqlalchemy.org/trac/ticket/1867)

-   **[oracle]**Oracle now reflects the names of primary key constraints
    - also thanks to Kent
    Bower.[¶](#change-ee4487a1aebbf952cb6ceaac4cb47cc8)

    参考文献：[＃1868](http://www.sqlalchemy.org/trac/ticket/1868)

### 火鸟[¶ T0\>](#change-0.6.4-firebird "Permalink to this headline")

-   **[firebird]**修正了列默认值无法反映“default”关键字是否为小写的错误。[¶](#change-92ab44e94581b35f750bf10f4e470570)

### 杂项[¶ T0\>](#change-0.6.4-misc "Permalink to this headline")

-   **[declarative]**如果@classproperty 与常规的类绑定映射器属性属性一起使用，它将被调用以获取初始化期间的实际属性值。目前，对不是混合的声明类的列或关系属性使用@classproperty 没有好处
    -
    评估与不使用@classproperty 同时进行。但是，我们至少允许它按预期运行。[¶](#change-d4f2d73f8008d60634e100a68c13d398)

-   **[declarative]**修正了“无法添加额外列”消息的错误名称。[¶](#change-868509e7b789f5e8a014c772349e3eb7)

-   **[informix]**应用补丁程序以再次获得基本的 Informix 功能。我们依靠最终用户测试来确保 Informix 在某种程度上有效。[¶](#change-431a87a1564f158a2d2ac1b341792ad1)

    参考文献：[＃1904](http://www.sqlalchemy.org/trac/ticket/1904)

-   **[documentation]**The docs have been reorganized such that the “API
    Reference” section is gone - all the docstrings from there which
    were public API are moved into the context of the main doc section
    that talks about it. 主要文档分为“SQLAlchemy Core”和“SQLAlchemy
    ORM”部分，映射器/关系文档已被打破。许多部分被重写和/或重组。[¶](#change-d47912608c4830253d4f01066a3062bb)

-   **[examples]**The beaker\_caching example has been reorganized such
    that the Session, cache manager, declarative\_base are part of
    environment, and custom cache code is portable and now within
    “caching\_query.py”.
    这使得该示例可以更容易地“插入”现有项目。[¶](#change-781cd432413e70f6da98e3dd05fda2be)

-   **[examples]**复制列时，history\_meta 版本控制配方设置“unique =
    False”，以便版本控制表处理多个具有重复值的行。[¶](#change-723cdb6f299e5eb37115fdceb06a6607)

    参考文献：[＃1887](http://www.sqlalchemy.org/trac/ticket/1887)

0.6.3 [¶ T0\>](#change-0.6.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2010 年 7 月 15 日

### ORM [¶ T0\>](#change-0.6.3-orm "Permalink to this headline")

-   **[orm]**在单元工作中删除了错误的多对多加载，这些加载在过期/卸载集合上不必要地触发。只有在 passive\_updates 为 False 并且父主键已更改，或者 passive\_deletes 为 False 并且已发生父项删除时，此加载现在才会发生。[¶](#change-4e1bf9516dda613ab1a572293546c083)

    参考文献：[＃1845](http://www.sqlalchemy.org/trac/ticket/1845)

-   **[orm]**Column-entities (i.e. query(Foo.id)) copy their state more
    fully when queries are derived from themselves + a selectable (i.e.
    from\_self(), union(), etc.
    ），所以 join()等具有正确的工作状态。[¶](#change-e9a54d540af9838dfb180c80efdf1e83)

    参考文献：[＃1853](http://www.sqlalchemy.org/trac/ticket/1853)

-   **[orm]**Fixed bug where Query.join() would fail if querying a
    non-ORM column then joining without an on clause when a FROM clause
    is already present, now raises a checked exception the same way it
    does when the clause is not
    present.[¶](#change-fb73bd1dbda53a059f9cdc6d0d8ccf45)

    参考文献：[＃1853](http://www.sqlalchemy.org/trac/ticket/1853)

-   **[orm]**改进了对“未映射类”的检查，包括超类映射但子类不是的情况。任何尝试访问 cls.\_sa\_class\_manager.mapper 的尝试都会引发 UnmappedClassError()。[¶](#change-03a152a294855452e7463fb4ac21ffd6)

    参考文献：[＃1142](http://www.sqlalchemy.org/trac/ticket/1142)

-   **[orm]**Added “column\_descriptions” accessor to Query, returns a
    list of dictionaries containing naming/typing information about the
    entities the Query will return.
    可以有助于在 ORM 查询之上构建 GUI。[¶](#change-f9299feaa7fe289b5bdc8377a2dcdb09)

### MySQL 的[¶ T0\>](#change-0.6.3-mysql "Permalink to this headline")

-   **[mysql]**The \_extract\_error\_code() method now works correctly
    with each MySQL dialect ( MySQL-python, OurSQL,
    MySQL-Connector-Python, PyODBC).
    以前，重新连接逻辑会失败的 OperationalError 条件，但由于 MySQLdb 和 OurSQL 有自己的重新连接功能，这里没有这些驱动程序的症状，除非有人观看日志。[¶](#change-40d3531e4ce4a40c3c74e0f48699dccc)

    参考文献：[＃1848](http://www.sqlalchemy.org/trac/ticket/1848)

### 预言[¶ T0\>](#change-0.6.3-oracle "Permalink to this headline")

-   **[oracle]**更多调整为 cx\_oracle 十进制处理。不含小数位的“模糊”数字在连接处理程序级被强制为 int。这样做的好处是，ints 会以 int 参数的形式返回，而不会涉及 SQLA 类型的对象，并且不会首先转换为 Decimal。

    不幸的是，一些外来的子查询情况甚至可能会在各个结果行之间看到不同的类型，所以当指示返回 Decimal 时，Numeric 处理程序不能充分利用“native
    decimal”模式，并且必须对每个值运行 isinstance()如果它的 Decimal 已经。重新开放

    [¶](#change-41dfa08c3915f42b47619e4e28ee162f)

    参考文献：[＃1840](http://www.sqlalchemy.org/trac/ticket/1840)

0.6.2 [¶ T0\>](#change-0.6.2 "Permalink to this headline")
----------------------------------------------------------

发布日期：2010 年 7 月 6 日

### ORM [¶ T0\>](#change-0.6.2-orm "Permalink to this headline")

-   **[orm]**Query.join() will check for a call of the form
    query.join(target, clause\_expression), i.e. missing the tuple, and
    raise an informative error message that this is the wrong calling
    form.[¶](#change-edf1e1a95a7fcdc97aa5ad0561516766)

-   **[orm]**Fixed bug regarding flushes on self-referential
    bi-directional many-to-many relationships, where two objects made to
    mutually reference each other in one flush would fail to insert a
    row for both sides.
    从 0.5 开始回归。[¶](#change-d632a942ba2390aa0d69b7b8d3db7726)

    参考文献：[＃1824](http://www.sqlalchemy.org/trac/ticket/1824)

-   **[orm]**the post\_update feature of relationship() has been
    reworked architecturally to integrate more closely with the new 0.6
    unit of work.
    更改的动机是，每个影响同一行的不同外键列的多个“更新后”调用在单个 UPDATE 语句中执行，而不是每行每列一个 UPDATE 语句。在保持一致的行排序的同时，多行更新也被批量分配到 executemany()中。[¶](#change-38b01fe13c4a4ea626916c8378f614d5)

-   **[orm]**
    Query.statement，Query.subquery()等现在将绑定参数的值（即 query.params()指定的值）转移到生成的 SQL 表达式中。以前，这些值不会被传送，绑定参数会显示为 None。[¶](#change-ec68a36d898ae8d2624447dffe1f74b3)

-   **[orm]**子查询-eager-loading 现在可以与包含 params()以及 get()查询的 Query 对象一起使用。[¶](#change-8e80dd442877d5cc6d55d1eb9f2e27ce)

-   **[orm]**Can now call make\_transient() on an instance that is
    referenced by parent objects via many-to-one, without the parent’s
    foreign key value getting temporarily set to None - this was a
    function of the “detect primary key switch” flush handler.
    它现在忽略不再处于“持久”状态的对象，并且父母的外键标识符不受影响。[¶](#change-89c7ce031cec5770d7feff6d59f82173)

-   **[orm]**query.order\_by() now accepts False, which cancels any
    existing order\_by() state on the Query, allowing subsequent
    generative methods to be called which do not support ORDER BY.
    这与传递 None 的已有功能不同，后者禁止任何现有的 order\_by()设置，包括映射器上配置的那些设置。False 将使得它好像从未调用过 order\_by()，而 None 是一个有效的设置。[¶](#change-02c64ac9aea77a533f8caaee63e2dd2e)

-   **[orm]**An instance which is moved to “transient”, has an
    incomplete or missing set of primary key attributes, and contains
    expired attributes, will raise an InvalidRequestError if an expired
    attribute is accessed, instead of getting a recursion
    overflow.[¶](#change-fc22e992cca054293cfca434a70f8339)

-   **[orm]**
    make\_transient()函数现在位于生成的文档中。[¶](#change-f2c43f7ce40d71c11c2f7faf46d66f4a)

-   **[orm]**make\_transient() removes all “loader” callables from the
    state being made transient, removing any “expired” state - all
    unloaded attributes reset back to undefined, None/empty on
    access.[¶](#change-9cb3e05a83cf387929738297b264ccf9)

### SQL [¶ T0\>](#change-0.6.2-sql "Permalink to this headline")

-   **[sql]**具有 convert\_unicode =
    True 的 Unicode 和 String 类型发出的警告不再嵌入传递的实际值。这样，Python 警告注册表的大小不会继续增加，警告会按照警告过滤器设置发出一次，并且大字符串值不会污染输出。[¶](#change-92eb958a7927c4e9caecec020272c06f)

    参考文献：[＃1822](http://www.sqlalchemy.org/trac/ticket/1822)

-   **[sql]**Fixed bug that would prevent overridden clause compilation
    from working for “annotated” expression elements, which are often
    generated by the ORM.[¶](#change-7ac2b12e9e86167b88a0806d4cbbe9fb)

-   **[sql]**
    LIKE 运算符或类似语句的“ESCAPE”参数通过 render\_literal\_value()传递，该函数可能会实现反斜杠的转义。[¶](#change-5e141a144264b09de7321f5569bcd21d)

    参考文献：[＃1400](http://www.sqlalchemy.org/trac/ticket/1400)

-   **[sql]**Fixed bug in Enum type which blew away native\_enum flag
    when used with TypeDecorators or other adaption
    scenarios.[¶](#change-854fbd022574e164314a3322bae40806)

-   **[sql]**Inspector hits bind.connect() when invoked to ensure
    initialize has been called.
    内部名称“.conn”更改为“.bind”，因为它就是这样。[¶](#change-da5d7dd83b9b8e3fa3dfc3c698adee89)

-   **[sql]**Modified the internals of “column annotation” such that a
    custom Column subclass can safely override \_constructor to return
    Column, for the purposes of making “configurational” column classes
    that aren’t involved in proxying,
    etc.[¶](#change-7031856f1234d33d0ce85911ecb27356)

-   **[sql]**Column.copy() takes along the “unique” attribute among
    others, fixes regarding declarative
    mixins[¶](#change-10d73e5cbbe7209624f8a76e237438c6)

    参考文献：[＃1829](http://www.sqlalchemy.org/trac/ticket/1829)

### 的 PostgreSQL [¶ T0\>](#change-0.6.2-postgresql "Permalink to this headline")

-   **[postgresql]**
    render\_literal\_value()被重写，它们转义反斜杠，当前应用于 LIKE 和类似表达式的 ESCAPE 子句。最终，这将必须检测“standard\_conforming\_strings”的完整行为的价值。[¶](#change-a99b1c9cecc1e928c742b45ef8f90cc3)

    参考文献：[＃1400](http://www.sqlalchemy.org/trac/ticket/1400)

-   **[postgresql]**如果在 8.3 版之前的 PG 版本中使用 types.Enum，则不会生成“CREATE
    TYPE”/“DROP TYPE” - supports\_native\_enum 标志完全符合要求[¶ t2
    \>](#change-48af7b36fa4c3f12a67261b2f80d7865)

    参考文献：[＃1836](http://www.sqlalchemy.org/trac/ticket/1836)

### MySQL 的[¶ T0\>](#change-0.6.2-mysql "Permalink to this headline")

-   **[mysql]**对于检测到的 MySQL 版本，MySQL 方言不会发出 CAST()\<4.0.2。\<
    span=""\>这允许在连接上进行 unicode 检查。[¶](#change-91f3d4d5f1ca37036afc83b8e87c588c)

    参考文献：[＃1826](http://www.sqlalchemy.org/trac/ticket/1826)

-   **[mysql]**除了 ANSI\_QUOTES 之外，MySQL 方言现在还检测 NO\_BACKSLASH\_ESCAPES
    sql 模式。[¶](#change-5984734c58273d70156013fa76eb8074)

-   **[mysql]**
    render\_literal\_value()被覆盖，其中转义反斜杠，目前适用于 LIKE 和类似表达式的 ESCAPE 子句。此行为源于检测 NO\_BACKSLASH\_ESCAPES 的值。[¶](#change-a99b1c9cecc1e928c742b45ef8f90cc3)

    参考文献：[＃1400](http://www.sqlalchemy.org/trac/ticket/1400)

### MSSQL [¶ T0\>](#change-0.6.2-mssql "Permalink to this headline")

-   **[mssql]**If server\_version\_info is outside the usual range of
    (8, ), (9, ), (10, ), a warning is emitted which suggests checking
    that the FreeTDS version configuration is using 7.0 or 8.0, not
    4.2.[¶](#change-0e401708966cccc9a7cc010adc04da9a)

    参考文献：[＃1825](http://www.sqlalchemy.org/trac/ticket/1825)

### 预言[¶ T0\>](#change-0.6.2-oracle "Permalink to this headline")

-   **[oracle]**修复了 ora-8 兼容性标志，使得它们不会在实际发生第一个数据库连接之前缓存陈旧值。[¶](#change-8d37a789557837ae28f36a0368b2b8a3)

    参考文献：[＃1819](http://www.sqlalchemy.org/trac/ticket/1819)

-   **[oracle]**Oracle’s “native decimal” metadata begins to return
    ambiguous typing information about numerics when columns are
    embedded in subqueries as well as when ROWNUM is consulted with
    subqueries, as we do for limit/offset.
    我们已经将这些不明确的条件添加到 cx\_oracle“convert to
    Decimal()”处理程序中，以便我们在更多情况下接收数字作为 Decimal，而不是作为浮点数。如果需要的话，它们将被转换为 Integer 或 Float，或者保留为无损 Decimal。[¶](#change-7cd2a1495d29a7ea446ff63e34a7e290)

    参考文献：[＃1840](http://www.sqlalchemy.org/trac/ticket/1840)

### 火鸟[¶ T0\>](#change-0.6.2-firebird "Permalink to this headline")

-   **[firebird]**修复了 do\_execute()中的错误签名，0.6.1 中引入了错误。[¶](#change-8020c6a07179eb3773cff83bf7e318ac)

    参考文献：[＃1823](http://www.sqlalchemy.org/trac/ticket/1823)

-   **[firebird]**Firebird dialect adds CHAR, VARCHAR types which accept
    a “charset” flag, to support Firebird “CHARACTER SET”
    clause.[¶](#change-911be84370c3f1ad4939567277f70d73)

    参考文献：[＃1813](http://www.sqlalchemy.org/trac/ticket/1813)

### 杂项[¶ T0\>](#change-0.6.2-misc "Permalink to this headline")

-   **[declarative]**Added support for @classproperty to provide any
    kind of schema/mapping construct from a declarative mixin, including
    columns with foreign keys, relationships, column\_property,
    deferred.
    这解决了声明性混合中的所有这些问题。如果在 mixin 上指定了任何 MapperProperty 子类而不使用@classproperty，则会产生错误。[¶](#change-586d7016a7038e911f333b3d048f0c80)

    References: [\#1805](http://www.sqlalchemy.org/trac/ticket/1805),
    [\#1796](http://www.sqlalchemy.org/trac/ticket/1796),
    [\#1751](http://www.sqlalchemy.org/trac/ticket/1751)

-   **[declarative]**a mixin class can now define a column that matches
    one which is present on a \_\_table\_\_ defined on a subclass.
    但是，它不能定义\_\_table\_\_中不存在的错误消息，现在这里的错误消息可以工作。[¶](#change-f1e04d8a9d224260a51570d93bc2bf4b)

    参考文献：[＃1821](http://www.sqlalchemy.org/trac/ticket/1821)

-   **[extension]
    [compiler]**当重写编译内置子句结构时，会自动复制'default'编译器，所以如果用户定义的编译器特定于某些后端，则不会引发 KeyError，调用另一个后端的编译。[¶](#change-af1b71d292a858ea4df75271507ce565)

    参考文献：[＃1838](http://www.sqlalchemy.org/trac/ticket/1838)

-   **[documentation]**添加了 Inspector 的文档。[¶](#change-848469658bfe0128fab72a42bba6e792)

    参考文献：[＃1820](http://www.sqlalchemy.org/trac/ticket/1820)

-   **[documentation]**Fixed @memoized\_property and
    @memoized\_instancemethod decorators so that Sphinx documentation
    picks up these attributes and methods, such as
    ResultProxy.inserted\_primary\_key.[¶](#change-4e33e10eba62ee01d6af5ccb29637f33)

    参考文献：[＃1830](http://www.sqlalchemy.org/trac/ticket/1830)

0.6.1 [¶ T0\>](#change-0.6.1 "Permalink to this headline")
----------------------------------------------------------

发布时间：2010 年 5 月 31 日

### ORM [¶ T0\>](#change-0.6.1-orm "Permalink to this headline")

-   **[orm]**修正 0.6.0 中引入的回归，其中涉及对可变属性进行不当历史记录。[¶](#change-3ad0634282071d683ecb076a3c1171ba)

    参考文献：[＃1782](http://www.sqlalchemy.org/trac/ticket/1782)

-   **[orm]**Fixed regression introduced in 0.6.0 unit of work refactor
    that broke updates for bi-directional relationship() with
    post\_update=True.[¶](#change-f27d049a3ba382d9d975d84ab7db1040)

    参考文献：[＃1807](http://www.sqlalchemy.org/trac/ticket/1807)

-   **[orm]**
    session.merge()不会在返回的实例上过期，如果该实例是“挂起”的话。[¶](#change-a5d06f591c00a5eb1caf7412dbddb887)

    参考文献：[＃1789](http://www.sqlalchemy.org/trac/ticket/1789)

-   **[orm]**修正了 CollectionAdapter 的\_\_setstate\_\_方法在反序列化中不失败，其中父 InstanceState 尚未反序列化[¶](#change-b9cf399b6f68b033fd9ea792f88bd39b)

    参考文献：[＃1802](http://www.sqlalchemy.org/trac/ticket/1802)

-   **[orm]**添加内部警告，以防万一没有完整 PK 的实例发生过期并被要求刷新。[¶](#change-284309c7b5f31be13e7f4fa173f0d4e6)

    参考文献：[＃1797](http://www.sqlalchemy.org/trac/ticket/1797)

-   **[orm]**为映射器对 UPDATE，INSERT 和 DELETE 表达式的使用增加了更积极的缓存。假设该语句没有附加每个对象的 SQL 表达式，表达式对象在第一次创建之后由映射器进行高速缓存，并且其编译后的表单在相关引擎期间持久存储在高速缓存字典中。缓存是一个 LRUCache，极少数情况下，映射程序接收的数据量非常大，不同的列模式为 UPDATE。[¶](#change-9092dd0fbb06e94417193ea80605814f)

### SQL [¶ T0\>](#change-0.6.1-sql "Permalink to this headline")

-   **[sql]**
    expr.in\_()现在接受一个 text()构造作为参数。分组括号会自动添加，即用法如 col.in\_（text（“select
    id from table”））。[¶](#change-b08316c6ff8d2199ee21227c71237c3c)

    参考文献：[＃1793](http://www.sqlalchemy.org/trac/ticket/1793)

-   **[sql]**Columns of \_Binary type (i.e. LargeBinary, BLOB, etc.)
    将右侧的“basestring”强制转换为\_Binary，因此需要进行 DBAPI 处理。[¶](#change-72ff9fd4e95f73a9fac5793d46ee1989)

-   **[sql]**添加了 table.add\_is\_dependent\_on（othertable），允许在两个表对象之间手动放置依赖关系规则，以便在 create\_all()，drop\_all()，sorted\_tables 中使用。[¶](#change-8d17b953e1ac169718caf18058bcd4a7)

    参考文献：[＃1801](http://www.sqlalchemy.org/trac/ticket/1801)

-   **[sql]**修正了防止隐式 RETURNING 与包含零的组合主键正常工作的错误。[¶](#change-8952d0409ec113323968a616d7b3ff95)

    参考文献：[＃1778](http://www.sqlalchemy.org/trac/ticket/1778)

-   **[sql]**Fixed errant space character when generating ADD CONSTRAINT
    for a named UNIQUE
    constraint.[¶](#change-82e4196d3222e0f8f2f39d0d56b49b68)

-   **[sql]**Fixed “table” argument on constructor of
    ForeginKeyConstraint[¶](#change-946f08fd63ce4b879c2fba51fc21eccf)

    参考文献：[＃1571](http://www.sqlalchemy.org/trac/ticket/1571)

-   **[sql]**Fixed bug in connection pool cursor wrapper whereby if a
    cursor threw an exception on close(), the logging of the message
    would fail.[¶](#change-e8fbe83ec8fc5eea2bdba7a800b0782f)

    参考文献：[＃1786](http://www.sqlalchemy.org/trac/ticket/1786)

-   **[sql]**the \_make\_proxy() method of ColumnClause and Column now
    use self.\_\_class\_\_ to determine the class of object to be
    returned instead of hardcoding to ColumnClause/Column, making it
    slightly easier to produce specific subclasses of these which work
    in alias/subquery
    situations.[¶](#change-a4876a0985ffddb6e31acca9c07979e7)

-   **[sql]**func.XXX() doesn’t inadvertently resolve to non-Function
    classes (e.g. fixes
    func.text()).[¶](#change-cabf1086effe5bf3e53e5eb62e0a539f)

    参考文献：[＃1798](http://www.sqlalchemy.org/trac/ticket/1798)

### MySQL 的[¶ T0\>](#change-0.6.1-mysql "Permalink to this headline")

-   **[mysql]**
    func.sysdate()在 MySQL 上发出“SYSDATE()”，即结尾括号。[¶](#change-aa357253b7d4e61fb60fe4179f37c4c4)

    参考文献：[＃1794](http://www.sqlalchemy.org/trac/ticket/1794)

### 源码[¶ T0\>](#change-0.6.1-sqlite "Permalink to this headline")

-   **[sqlite]**修正了由于 SQLite AUTOINCREMENT 关键字被渲染而导致“PRIMARY
    KEY”约束移动到列级别时约束的串联约束。[¶](#change-f93c6942e6696df34b2e495e1a798242)

    参考文献：[＃1812](http://www.sqlalchemy.org/trac/ticket/1812)

### 预言[¶ T0\>](#change-0.6.1-oracle "Permalink to this headline")

-   **[oracle]**添加了对低于版本 5 的 cx\_oracle 版本的检查，在这种情况下不会使用不兼容的“输出类型处理程序”。这会影响十进制精度和一些 unicode 处理问题。[¶](#change-921c563fd599609c36d48fca98c94857)

    参考文献：[＃1775](http://www.sqlalchemy.org/trac/ticket/1775)

-   **[oracle]**修复了 use\_ansi =
    False 模式，在几乎所有情况下都产生了破碎的 WHERE 子句。[¶](#change-de39458c5cf40832d3e712046e906059)

    参考文献：[＃1790](http://www.sqlalchemy.org/trac/ticket/1790)

-   **[oracle]**Re-established support for Oracle 8 with cx\_oracle,
    including that use\_ansi is set to False automatically, NVARCHAR2
    and NCLOB are not rendered for Unicode, “native unicode” check
    doesn’t fail, cx\_oracle “native unicode” mode is disabled,
    VARCHAR() is emitted with bytes count instead of char
    count.[¶](#change-c5cd67d9af16519e3e1648d461a6fa18)

    参考文献：[＃1808](http://www.sqlalchemy.org/trac/ticket/1808)

-   **[oracle]**在正常的 Python 2.x 模式下，oracle\_xe
    5 在其连接字符串中不接受 Python unicode 对象 -
    所以我们直接对 str()进行强制转换。在这里连接字符串不支持非 ascii 字符，因为我们不知道我们可以使用什么编码。[¶](#change-42bad8b40515caa95e779b1bb6592e72)

    参考文献：[＃1670](http://www.sqlalchemy.org/trac/ticket/1670)

-   **[oracle]**FOR UPDATE is emitted in the syntactically correct
    position when limit/offset is used, i.e. the ROWNUM subquery.
    但是，Oracle 无法真正使用 ORDER BY 或子查询来处理 FOR
    UPDATE，所以它仍然不是很实用，但至少 SQLA 会通过 Oracle 解析器获取 SQL。[](#change-c4fb3d2d0a0c5a82038662d1a131caa4)

    参考文献：[＃1815](http://www.sqlalchemy.org/trac/ticket/1815)

### 火鸟[¶ T0\>](#change-0.6.1-firebird "Permalink to this headline")

-   **[firebird]**在 has\_table()和 has\_sequence()中使用的查询中添加了一个标签，可用于不会为结果列提供标签的 Firebird 旧版本。[](#change-91fe7d4094c4263398493a015350a1ed)

    参考文献：[＃1521](http://www.sqlalchemy.org/trac/ticket/1521)

-   **[firebird]**当通过查询字符串传递时，为“type\_conv”属性添加整数强制，以便由 Kinterbasdb 正确解释。[¶](#change-0d74fea7bfb3e3c84d0515cc593d4d87)

    参考文献：[＃1779](http://www.sqlalchemy.org/trac/ticket/1779)

-   **[firebird]**将'连接关闭'添加到表示连接断开的异常字符串列表中。[¶](#change-03bb6ab00e44c5f02f340d559a5dab0f)

    参考文献：[＃1646](http://www.sqlalchemy.org/trac/ticket/1646)

### 杂项[¶ T0\>](#change-0.6.1-misc "Permalink to this headline")

-   **[engines]**修正了 Python
    2.4 中的 C 扩展。[¶](#change-df53735fe0fac1271ec8b185d92b917c)

    参考文献：[＃1781](http://www.sqlalchemy.org/trac/ticket/1781)

-   **[engines]**在发生 dispose()后，池类将重复使用相同的“pool\_logging\_name”设置。[¶](#change-bd1c201152d89a2c0a9fce60d6eb9f10)

-   **[engines]**引擎获得“execution\_options”参数和 update\_execution\_options()方法，该方法将应用于此引擎生成的所有连接。[¶](#change-d98f14529ec58cd4e539be4876c55109)

-   **[sqlsoup]**the SqlSoup constructor accepts a base argument which
    specifies the base class to use for mapped classes, the default
    being object.[¶](#change-6bd58738b79dc1de9e4c774f875c967e)

    参考文献：[＃1783](http://www.sqlalchemy.org/trac/ticket/1783)

0.6.0 [¶ T0\>](#change-0.6.0 "Permalink to this headline")
----------------------------------------------------------

发布于：2010 年 4 月 18 日

### ORM [¶ T0\>](#change-0.6.0-orm "Permalink to this headline")

-   **[orm]**工作单元内部已被重写。由于不再依赖递归调用，现在可以刷新大量与对象相关的对象的工作单元而不会发生递归溢出。现在，对于特定的会话状态，内部结构的数量保持不变，而不管映射上存在多少关系。事件流现在对应于线性步骤列表，由映射器和关系基于要完成的实际工作生成，通过单个拓扑排序进行正确排序。刷新操作使用更少的步骤和更少的内存来组装。[¶](#change-3b1217c725cfaca8d0f18b95fec0c71d)

    参考文献：[＃1742](http://www.sqlalchemy.org/trac/ticket/1742)，[＃1081](http://www.sqlalchemy.org/trac/ticket/1081)

-   **[orm]**Along with the UOW rewrite, this also removes an issue
    introduced in 0.6beta3 regarding topological cycle detection for
    units of work with long dependency cycles.
    我们现在使用 Guido 编写的算法（感谢 Guido！）。[¶
    T0\>](#change-97e2870a10f13e39b21451eade7f34e3)

-   **[orm]**one-to-many relationships now maintain a list of positive
    parent-child associations within the flush, preventing previous
    parents marked as deleted from cascading a delete or NULL foreign
    key set on those child objects, despite the end-user not removing
    the child from the old
    association.[¶](#change-2c89e63a7b00b521ab6ebefa3e55a3d8)

    参考文献：[＃1764](http://www.sqlalchemy.org/trac/ticket/1764)

-   **[orm]**集合延迟加载将在多对一的反向关闭默认预加载，因为该加载在定义上是不必要的。[¶](#change-de68f57cafdd0eff2e36aba90d68a8d9)

    参考文献：[＃1495](http://www.sqlalchemy.org/trac/ticket/1495)

-   **[orm]**Session.refresh() now does an equivalent expire() on the
    given instance first, so that the “refresh-expire” cascade is
    propagated.
    以前，refresh()不受“refresh-expire”级联的影响。这是行为与 0.6beta2 行为的变化，其中传递给 refresh()的“lockmode”标志将导致版本检查发生。由于实例首次过期，因此 refresh()会始终将对象升级到最新版本。[¶](#change-60b9bbf87ecba4f952f15d81c023040f)

-   **[orm]**The ‘refresh-expire’ cascade, when reaching a pending
    object, will expunge the object if the cascade also includes
    “delete-orphan”, or will simply detach it
    otherwise.[¶](#change-f00123490bb1d2834b93640ea8cbd25d)

    参考文献：[＃1754](http://www.sqlalchemy.org/trac/ticket/1754)

-   **[orm]**
    id（obj）不再在 topological.py 中内部使用，因为排序函数现在只需要可哈希对象。[¶](#change-446d9794507b3c1360eb69dd3f886c1b)

    参考文献：[＃1756](http://www.sqlalchemy.org/trac/ticket/1756)

-   **[orm]**The ORM will set the docstring of all generated descriptors
    to None by default.
    这可以使用'doc'来覆盖（或者如果使用 Sphinx，属性 docstrings 也可以）。[¶](#change-89d6d3ab3f04efc830987da850dbcd9f)

-   **[orm]**将 kw 参数'doc'添加到所有映射器属性可调参数以及 Column()。将字符串'doc'组装为描述符上的'\_\_doc\_\_'属性。[¶](#change-0c5e8a43f7cfd7406db906494f6c86cb)

-   **[orm]**Usage of version\_id\_col on a backend that supports
    cursor.rowcount for execute() but not executemany() now works when a
    delete is issued (already worked for saves, since those don’t use
    executemany()).
    对于根本不支持 cursor.rowcount 的后端，发出的警告与 save 相同。[¶](#change-bfa16822997c1406790421c29fcddf84)

    参考文献：[＃1761](http://www.sqlalchemy.org/trac/ticket/1761)

-   **[orm]**The ORM now short-term caches the “compiled” form of
    insert() and update() constructs when flushing lists of objects of
    all the same class, thereby avoiding redundant compilation per
    individual INSERT/UPDATE within an individual flush()
    call.[¶](#change-7c8f475376472ec13a1f37c930bcffc9)

-   **[orm]**internal getattr(), setattr(), getcommitted() methods on
    ColumnProperty, CompositeProperty, RelationshipProperty have been
    underscored (i.e. are private), signature has
    changed.[¶](#change-9b2338aa43fcd0bf730a52d5e1a78bf1)

### SQL [¶ T0\>](#change-0.6.0-sql "Permalink to this headline")

-   **[sql]**Restored some bind-labeling logic from 0.5 which ensures
    that tables with column names that overlap another column of the
    form “\_” won’t produce errors if column.\_label is used as a bind
    name during an UPDATE.
    已添加 0.5 中不存在的测试覆盖率。[¶](#change-2ad00fb1fb1dc9fb7c58e6eea6830e93)

    参考文献：[＃1755](http://www.sqlalchemy.org/trac/ticket/1755)

-   **[sql]**somejoin.select(fold\_equivalents=True) is no longer
    deprecated, and will eventually be rolled into a more comprehensive
    version of the feature
    for.[¶](#change-8a0a290dfd11b9c9f0b759cacd2c60e7)

    参考文献：[＃1729](http://www.sqlalchemy.org/trac/ticket/1729)

-   **[sql]**the Numeric type raises an *enormous* warning when expected
    to convert floats to Decimal from a DBAPI that returns floats.
    这包括 SQLite，Sybase，MS-SQL。[¶](#change-f49c7dce36721a3b7fff421faf1e347f)

    参考文献：[＃1759](http://www.sqlalchemy.org/trac/ticket/1759)

-   **[sql]**修复了表达式中的一个错误，该错误导致了具有两个 NULL 类型的表达式的无限循环[¶](#change-79bb81f03cb8e5df4f9dd9a451f01db2)

-   **[sql]**Fixed bug in execution\_options() feature whereby the
    existing Transaction and other state information from the parent
    connection would not be propagated to the
    sub-connection.[¶](#change-9a48a170841006eca908993bdd32d73e)

-   **[sql]**添加了新的'compiled\_cache'执行选项。当连接将子句表达式编译为方言和参数特定的编译对象时，Compiled 对象将被缓存的字典。用户有责任管理该字典的大小，该字典将具有与方言，子句元素，INSERT 或 UPDATE 的 VALUES 或 SET 子句中的列名相对应的键，以及用于 INSERT 或 UPDATE 语句。[¶](#change-60e732c087d2155ba7f95c3372a0b9e0)

-   **[sql]**将 get\_pk\_constraint()添加到 reflection.Inspector，类似于 get\_primary\_keys()，除了返回一个包含约束名称的 dict，用于受支持的后端（迄今为止的 PG）[¶\<
    / T2\>](#change-768b947e2c0ef47ccdae7a24bea4fc76)

    参考文献：[＃1769](http://www.sqlalchemy.org/trac/ticket/1769)

-   **[sql]**Table.create() and Table.drop() no longer apply metadata-
    level create/drop
    events.[¶](#change-9e9da1b03603fbea0a497194ff379a0f)

    参考文献：[＃1771](http://www.sqlalchemy.org/trac/ticket/1771)

### 的 PostgreSQL [¶ T0\>](#change-0.6.0-postgresql "Permalink to this headline")

-   **[postgresql]**在序列名称被更改之后，Postgresql 现在正确反映了与 SERIAL 列相关联的序列名称。感谢 Kumar
    McMillan 提供的补丁。[¶](#change-4a1523bb9932656419cad5bb47984b8f)

    参考文献：[＃1071](http://www.sqlalchemy.org/trac/ticket/1071)

-   **[postgresql]**收到未知数​​字时修复了 psycopg2.\_PGNumeric 类型中缺少的导入。[¶](#change-f9a992cccbd35a7929c4a9fc18106789)

-   **[postgresql]** psycopg2 / pg8000 方言现在知道 REAL []，FLOAT
    []，DOUBLE\_PRECISION []，NUMERIC
    []返回类型而不引发异常[¶](#change-b98fd25854c44f76b567995a581b059f)

-   **[postgresql]**
    Postgresql 反映主键约束的名称（如果存在）。[¶](#change-795011bac9decfbec163b1e926b9af2e)

    参考文献：[＃1769](http://www.sqlalchemy.org/trac/ticket/1769)

### 预言[¶ T0\>](#change-0.6.0-oracle "Permalink to this headline")

-   **[oracle]**现在使用 cx\_oracle 输出转换器，以便 DBAPI 原生返回我们喜欢的值类型：[¶](#change-e256b03edc9a352999ab763c545d8369)

-   **[oracle]**NUMBER values with positive precision + scale convert to
    cx\_oracle.STRING and then to Decimal.
    这使得在使用 cx\_oracle 时数值类型具有完美的精度。[¶](#change-f9a62b0f03f5c58cd9451cf9002cb497)

    参考文献：[＃1759](http://www.sqlalchemy.org/trac/ticket/1759)

-   **[oracle]**现在 STRING /
    FIXED\_CHAR 本地转换为 unicode。SQLAlchemy 的 String 类型不需要应用任何类型的转换。[¶](#change-ddda48d09bea40d9663e1537a8b7b708)

### 火鸟[¶ T0\>](#change-0.6.0-firebird "Permalink to this headline")

-   **[firebird]**通过在 create\_engine()上设置'enable\_rowcount =
    False'，可以基于每个引擎禁用 result.rowcount 的功能。通常，无条件地在任何 UPDATE 或 DELETE 语句之后调用 cursor.rowcount，因为随后关闭了游标并且 Firebird 需要打开游标才能获得行计数。这个电话稍微昂贵，所以它可以被禁用。要在每次执行的基础上重新启用，可以使用'enable\_rowcount
    = True'执行选项。[¶](#change-605572f4fbe5fbe913e1c270b3de66b4)

### 杂项[¶ T0\>](#change-0.6.0-misc "Permalink to this headline")

-   **[engines]**
    C 扩展现在也适用于将自定义序列用作行（而不仅是元组）的 DBAPI。[¶](#change-e0c034dd38e58d6263b4417bd5b20d8a)

    参考文献：[＃1757](http://www.sqlalchemy.org/trac/ticket/1757)

-   **[ext]**编译器扩展现在允许在扩展到子类的基类上使用@compiles 装饰器，在编译器上的@compiles 修饰器不会被基类上的@compiles 修饰器破坏。[¶
    T2\>](#change-aa50f37469eba982996cc17bb2685a72)

-   **[ext]**Declarative will raise an informative error message if a
    non-mapped class attribute is referenced in the string-based
    relationship()
    arguments.[¶](#change-0507e611abb0fe0ac48260501435bd99)

-   **[ext]**进一步修改了声明式中的“mixin”逻辑，以另外允许\_\_mapper\_args\_\_作为 mixin 上的@class 属性，例如动态分配 polymorphic\_identity。[¶](#change-deb0113981b96ffb2348bb3031d2e553)

-   **[examples]**更新了 attribute\_shard.py 示例，以便使用更强大的搜索 Query 的二进制表达式来将列与文本值进行比较。[¶](#change-cbe6875d1367b7c3a0bbeb9dddead99a)

0.6beta3 [¶ T0\>](#change-0.6beta3 "Permalink to this headline")
----------------------------------------------------------------

发布于：2010 年 3 月 28 日

### ORM [¶ T0\>](#change-0.6beta3-orm "Permalink to this headline")

-   **[orm]**主要功能：为关系()添加了新的“子查询”加载功能。这是一个热切的加载选项，它为查询中表示的每个集合生成第二个 SELECT，并同时为所有父母生成。查询重新发布包装在子查询中的原始最终用户查询，将连接应用到目标集合，并将所有这些集合完全加载到一个结果中，类似于“已加入”的加载，但使用所有内部连接，重复获取完整的父行（因为大多数 DBAPI 似乎都这样做，即使列被跳过）。子查询加载可在 mapper 配置级别使用“lazy
    ='subquery'”并在查询选项级别使用“subqueryload（props
    ..）”，“subqueryload\_all（props
    ...）”。[¶](#change-f967d8dbf3c4194f9e0b1af4d5804fd6)

    参考文献：[＃1675](http://www.sqlalchemy.org/trac/ticket/1675)

-   **[orm]**To accommodate the fact that there are now two kinds of
    eager loading available, the new names for eagerload() and
    eagerload\_all() are joinedload() and joinedload\_all().
    在可预见的将来，旧名称仍然是同义词。[¶](#change-18a93528ced9a2629dcac08a74e933e0)

-   **[orm]**The “lazy” flag on the relationship() function now accepts
    a string argument for all kinds of loading: “select”, “joined”,
    “subquery”, “noload” and “dynamic”, where the default is now
    “select”. True / False /
    None 的旧值仍然保留其通常的含义，并且在可预见的未来仍然是同义词。[¶](#change-5660c8fd9cb4729f0f6017950bde5b27)

-   **[orm]**向 Query()构造添加了 with\_hint()方法。这直接调用 select()。with\_hint()并接受实体以及表和别名。请参阅下面的 SQL 部分中的 with\_hint()。[¶](#change-cc53079a38c2d284e5b3d878ed0120c4)

    参考文献：[＃921](http://www.sqlalchemy.org/trac/ticket/921)

-   **[orm]**Fixed bug in Query whereby calling
    q.join(prop).from\_self(...).
    连接（prop）将无法将第二个连接渲染到子查询的外部，当连接到与内部相同的标准时。[¶](#change-3ccda2938593dbe9607247dd4ea3f042)

-   **[orm]**Fixed bug in Query whereby the usage of aliased()
    constructs would fail if the underlying table (but not the actual
    alias) were referenced inside the subquery generated by
    q.from\_self() or
    q.select\_from().[¶](#change-2546a2848e4b1fdee1a5cacf7b6e9177)

-   **[orm]**Fixed bug which affected all eagerload() and similar
    options such that “remote” eager loads, i.e. eagerloads off of a
    lazy load such as query(A).options(eagerload(A.b, B.c)) wouldn’t
    eagerload anything, but using eagerload(“b.c”) would work
    fine.[¶](#change-69588e4d5fc29aebd7af673e5d4ec0ae)

-   **[orm]**查询获得 add\_columns（col）的多版本 add\_columns（\*
    columns）方法。add\_column（col）将来会被弃用。[¶](#change-f79b8419ad3bbd5244a090f0a35e6c22)

-   **[orm]** Query.join()将检测最终结果是否为“FROM A JOIN
    A”，如果是，则会引发错误。[¶](#change-965b0258f91345cb3a06eb1191ba4dd6)

-   **[orm]**Query.join(Cls.propname, from\_joinpoint=True) will check
    more carefully that “Cls” is compatible with the current joinpoint,
    and act the same way as Query.join(“propname”, from\_joinpoint=True)
    in that regard.[¶](#change-33de22e92c0ea512daaf2bf928b86233)

### SQL [¶ T0\>](#change-0.6beta3-sql "Permalink to this headline")

-   **[sql]**添加 with\_hint()方法以选择()构造。指定表/别名，提示文本和可选的方言名称，并且“提示”将在语句的适当位置呈现。适用于 Oracle，Sybase，MySQL。[¶](#change-8921f11442b55f634ffd5da10a321a10)

    参考文献：[＃921](http://www.sqlalchemy.org/trac/ticket/921)

-   **[sql]**Fixed bug introduced in 0.6beta2 where column labels would
    render inside of column expressions already assigned a
    label.[¶](#change-dbf96f0ccd57bb7e5c8878762570f98e)

    参考文献：[＃1747](http://www.sqlalchemy.org/trac/ticket/1747)

### 的 PostgreSQL [¶ T0\>](#change-0.6beta3-postgresql "Permalink to this headline")

-   **[postgresql]**
    psycopg2 方言将通过“sqlalchemy.dialects.postgresql”记录器名称记录 NOTICE 消息。[¶](#change-51b8f6239dcbf5719eeda7f33fb074ad)

    参考文献：[＃877](http://www.sqlalchemy.org/trac/ticket/877)

-   **[postgresql]**
    TIME 和 TIMESTAMP 类型现在可以直接从 postgresql 方言中获得，它将 PG 特有的参数'precision'添加到两者中。'TIME'和'TIMEZONE'类型的'precision'和'timezone'都被正确反映。[¶](#change-b06780742c82dc402af8d0b581c9eebe)

    参考文献：[＃997](http://www.sqlalchemy.org/trac/ticket/997)

### MySQL 的[¶ T0\>](#change-0.6beta3-mysql "Permalink to this headline")

-   **[mysql]**当反射 -
    TINYINT（1）返回时，不要再猜测 TINYINT（1）应该是 BOOLEAN。在表定义中使用布尔值/布尔值来获取布尔转换行为。[¶](#change-683fd67a66959dc8c853731f14b2cc81)

    参考文献：[＃1752](http://www.sqlalchemy.org/trac/ticket/1752)

### 预言[¶ T0\>](#change-0.6beta3-oracle "Permalink to this headline")

-   **[oracle]**The Oracle dialect will issue VARCHAR type definitions
    using character counts, i.e. VARCHAR2(50 CHAR), so that the column
    is sized in terms of characters and not bytes.
    字符类型的列反射也将使用 ALL\_TAB\_COLUMNS.CHAR\_LENGTH 而不是 ALL\_TAB\_COLUMNS.DATA\_LENGTH。当服务器版本为 9 或更高版本时，这两种行为都会生效
    -
    对于版本 8，使用旧行为。[¶](#change-5c94b49a397096685020b6e1e5702ec7)

    参考文献：[＃1744](http://www.sqlalchemy.org/trac/ticket/1744)

### 杂项[¶ T0\>](#change-0.6beta3-misc "Permalink to this headline")

-   **[declarative]**如果 mixin 实现了一个不可预知的\_\_getattribute
    \_\_()，即 Zope 接口，那么使用 mixin 不会中断。[¶](#change-830637c55ffba2f2e096ea3c18f4f4a7)

    参考文献：[＃1746](http://www.sqlalchemy.org/trac/ticket/1746)

-   **[declarative]**在 mixins 上使用@classdecorator 和类似词来定义\_\_tablename\_\_，\_\_table\_args\_\_等。现在可以在该方法引用最终子类上的属性时使用。[¶](#change-bd6f8eba3f3862d4d8d1011707f7b4cf)

    参考文献：[＃1749](http://www.sqlalchemy.org/trac/ticket/1749)

-   **[declarative]**声明式混合中不允许使用外键的关系和列，对不起。[¶](#change-1330f1fe92881e1fd934e9d4505add81)

    参考文献：[＃1751](http://www.sqlalchemy.org/trac/ticket/1751)

-   **[ext]**
    sqlalchemy.orm.shard 模块现在成为扩展名 sqlalchemy.ext.horizo​​ntal\_shard。旧的导入使用了弃用警告。[¶](#change-caaf4140d3b5e7c3c34a1234538341e4)

0.6beta2 [¶ T0\>](#change-0.6beta2 "Permalink to this headline")
----------------------------------------------------------------

发布日期：2010 年 3 月 20 日

### ORM [¶ T0\>](#change-0.6beta2-orm "Permalink to this headline")

-   **[orm]**
    relation()函数的正式名称现在是 relationship()，以消除对关系代数术语的混淆。在可预见的将来，relation()将保持相同的容量。[¶](#change-91f89136c1aa2ba8d36ba9cf940655b3)

    参考文献：[＃1740](http://www.sqlalchemy.org/trac/ticket/1740)

-   **[orm]**为 Mapper 添加了“version\_id\_generator”参数，这是一个可调用的参数，在“version\_id\_col”的当前值的情况下返回下一个版本号。可用于替代版本控制方案，如 uuid，时间戳。[¶](#change-9037d3b9977b0f3a6fcc6590008b9b44)

    参考文献：[＃1692](http://www.sqlalchemy.org/trac/ticket/1692)

-   **[orm]**added “lockmode” kw argument to Session.refresh(), will
    pass through the string value to Query the same as in
    with\_lockmode(), will also do version check for a
    version\_id\_col-enabled
    mapping.[¶](#change-ac4f20719ab810598a0f3c8590bb9e48)

-   **[orm]**Fixed bug whereby calling
    query(A).join(A.bs).add\_entity(B) in a joined inheritance scenario
    would double-add B as a target and produce an invalid
    query.[¶](#change-2edc56abe56b8a124e046abb661dc5db)

    参考文献：[＃1188](http://www.sqlalchemy.org/trac/ticket/1188)

-   **[orm]**Fixed bug in session.rollback() which involved not removing
    formerly “pending” objects from the session before re-integrating
    “deleted” objects, typically occurred with natural primary keys.
    如果它们之间存在主键冲突，则删除的附加内部将失败。以前的“待处理”对象现在先被清除。[¶](#change-58c0d0b1848c816ae294a332245af234)

    参考文献：[＃1674](http://www.sqlalchemy.org/trac/ticket/1674)

-   **[orm]**删除了很多没有人关心的日志记录，日志记录仍然会响应日志级别的实时更改。没有明显的额外开销。[¶](#change-1f41c5a5c9f337a6608e0d4f75069739)

    参考文献：[＃1719](http://www.sqlalchemy.org/trac/ticket/1719)

-   **[orm]**修正了 session.merge()中的错误，它阻止了字典集合的合并。[¶](#change-a1907a9674f8eb93bed9c80372b1b3b1)

-   **[orm]**session.merge() works with relations that specifically
    don’t include “merge” in their cascade options - the target is
    ignored completely.[¶](#change-2388f0254684db431b5a06c72016ec42)

-   如果目标具有该属性的值，即使传入的合并没有该属性的值，session.merge()也不会过期现有目标上的现有标量属性。**[orm]**这可以防止对现有项目造成不必要的负载如果目的地没有 attr，但仍然会将 attr 标记为已到期，这符合延迟 cols 的某些合同。[¶](#change-c3b6834f3e3153d50e1c2975e838d44c)

    参考文献：[＃1681](http://www.sqlalchemy.org/trac/ticket/1681)

-   **[orm]**The “allow\_null\_pks” flag is now called
    “allow\_partial\_pks”, defaults to True, acts like it did in 0.5
    again.
    除此之外，它也在 merge()中实现，使得如果标志为 False，则不会为具有部分 NULL 主键的传入实例发出 SELECT。[¶](#change-666a289821dc312f5ae2b810b4f61a61)

    参考文献：[＃1680](http://www.sqlalchemy.org/trac/ticket/1680)

-   **[orm]**Fixed bug in 0.6-reworked “many-to-one” optimizations such
    that a many-to-one that is against a non-primary key column on the
    remote table (i.e. foreign key against a UNIQUE column) will pull
    the “old” value in from the database during a change, since if it’s
    in the session we will need it for proper history/backref
    accounting, and we can’t pull from the local identity map on a
    non-primary key column.[¶](#change-340360d984e646cb2c8c8da0d5cc11b8)

    参考文献：[＃1737](http://www.sqlalchemy.org/trac/ticket/1737)

-   **[orm]**固定内部错误，如果在单表继承关系()上调用 has()或类似的复杂表达式时会发生。[¶](#change-2848fed5c8fca096477e50f01a83b6c3)

    参考文献：[＃1731](http://www.sqlalchemy.org/trac/ticket/1731)

-   **[orm]**query.one() no longer applies LIMIT to the query, this to
    ensure that it fully counts all object identities present in the
    result, even in the case where joins may conceal multiple identities
    for two or more rows.
    作为奖励，现在也可以用发出 from\_statement()的查询来调用 one()以开始，因为它不再修改查询。[¶](#change-5033bb4d60482fdc7e61d81f6412cea4)

    参考文献：[＃1688](http://www.sqlalchemy.org/trac/ticket/1688)

-   如果查询标识映射中存在的标识符与所请求的标识符不同的类，即使用多态加载时，query.get()现在返回 None。[**[orm]**](#change-52b4d6b9d3562cdaf43788184ae1805f)

    参考文献：[＃1727](http://www.sqlalchemy.org/trac/ticket/1727)

-   **[orm]**A major fix in query.join(), when the “on” clause is an
    attribute of an aliased() construct, but there is already an
    existing join made out to a compatible target, query properly joins
    to the right aliased() construct instead of sticking onto the right
    side of the existing
    join.[¶](#change-655aaf64d072c58ce2e64a5d6dc12323)

    参考文献：[＃1706](http://www.sqlalchemy.org/trac/ticket/1706)

-   **[orm]**Slight improvement to the fix for to not issue needless
    updates of the primary key column during a so-called “row switch”
    operation, i.e. add + delete of two objects with the same
    PK.[¶](#change-fd6cb3f54f47c27d18ce7c8dd343525d)

    参考文献：[＃1362](http://www.sqlalchemy.org/trac/ticket/1362)

-   **[orm]**当属性加载或刷新操作由于对象与任何会话分离而失败时，现在使用 sqlalchemy.orm.exc.DetachedInstanceError。UnboundExecutionError 特定于绑定到会话和语句的引擎。[¶](#change-149e924d04484755c0a14ec239f22076)

-   **[orm]**Query called in the context of an expression will render
    disambiguating labels in all cases.
    请注意，这并不适用于现有的.statement 和.subquery()访问器/方法，它仍然支持默认为 False 的.with\_labels()设置。[¶](#change-7312d2f689d678c6e4d0799defdb8511)

-   **[orm]**Query.union() retains disambiguating labels within the
    returned statement, thus avoiding various SQL composition errors
    which can result from column name
    conflicts.[¶](#change-69ee650c673044a6587e8f1a25fd2e9b)

    参考文献：[＃1676](http://www.sqlalchemy.org/trac/ticket/1676)

-   **[orm]**修正了属性历史记录中无意中在映射实例上调用了\_\_eq\_\_的错误。[¶](#change-9366c0432f49557b000d6930b7f2b0c8)

-   **[orm]**Some internal streamlining of object loading grants a small
    speedup for large results, estimates are around 10-15%.
    给“状态”内部一个良好的固体清理，复杂性较低，数据成员，方法调用，空白字典创建。[¶](#change-9b042559ccc515464dca31a9da9e25d6)

-   **[orm]**
    query.delete()[¶](#change-99a73658e5e4c367df4688c45bbda9aa)的文档说明

    参考文献：[＃1689](http://www.sqlalchemy.org/trac/ticket/1689)

-   **[orm]**在 r6711 中引入了属性设置为 None 时，在多对一关系()中修复级联错误（在 add()中级联删除的项目到会话中）[T2\>](#change-3b02e92cb9ea00b598b21503acc970d0)

-   **[orm]**Calling query.order\_by() or query.distinct() before
    calling query.select\_from(), query.with\_polymorphic(), or
    query.from\_statement() raises an exception now instead of silently
    dropping those
    criterion.[¶](#change-931a758f3fb2e353bb842566bd92c153)

    参考文献：[＃1736](http://www.sqlalchemy.org/trac/ticket/1736)

-   **[orm]**query.scalar() now raises an exception if more than one row
    is returned.
    所有其他行为保持不变。[¶](#change-c2ae6c50721c4f5bc949b93ea8f29055)

    参考文献：[＃1735](http://www.sqlalchemy.org/trac/ticket/1735)

-   **[orm]**Fixed bug which caused “row switch” logic, that is an
    INSERT and DELETE replaced by an UPDATE, to fail when
    version\_id\_col was in
    use.[¶](#change-714ce6498d2c194488bf5337d8787134)

    参考文献：[＃1692](http://www.sqlalchemy.org/trac/ticket/1692)

### SQL [¶ T0\>](#change-0.6beta2-sql "Permalink to this headline")

-   **[sql]**join() will now simulate a NATURAL JOIN by default.
    意思是，如果左侧是连接，它将尝试将右侧连接到左侧的第一个右侧，如果成功，则不会引发任何有关模糊连接条件的例外，即使其他连接目标左侧。[¶
    T0\>](#change-b53712fca734ff4d0164b00e61f53cf1)

    参考文献：[＃1714](http://www.sqlalchemy.org/trac/ticket/1714)

-   **[sql]**The most common result processors conversion function were
    moved to the new “processors” module.
    鼓励方言作者在符合他们的需求时使用这些函数，而不是实现自定义函数。[¶](#change-e6678947026dc69d573ba7f06fa6dcc0)

-   **[sql]**
    SchemaType 和子类 Boolean，Enum 现在是可序列化的，包括它们的 ddl 监听器和其他事件可调用。[¶](#change-787fd3a6677f8ba4f979ea8f6fb383fd)

    参考文献：[＃1694](http://www.sqlalchemy.org/trac/ticket/1694)，[＃1698](http://www.sqlalchemy.org/trac/ticket/1698)

-   **[sql]**Some platforms will now interpret certain literal values as
    non-bind parameters, rendered literally into the SQL statement.
    这支持严格的 SQL-92 规则，这些规则由包括 MS-SQL 和 Sybase 在内的一些平台实施。在此模型中，绑定参数不允许在 SELECT 的 columns 子句中使用，也不允许使用某些不明确的表达式，例如“？=？”。启用此模式后，基本编译器会将绑定呈现为内联文字，但只能跨字符串和数字值显示。其他类型如日期会引发错误，除非方言子类为这些定义了字面渲染函数。bind 参数必须已经有嵌入的文字值，否则会引发错误（即不能使用直接 bindparam（'x'））。方言还可以扩展不接受绑定的区域，例如函数的参数列表（在使用本机 SQL 绑定时不适用于 MS-SQL）。[¶](#change-b8980f5d17caec1e2e5b563b1e15b8b2)

-   **[sql]**将“unicode\_errors”参数添加到 String，Unicode 等行为就像标准库的 string.decode()函数的'errors'关键字参数。该标志要求 convert\_unicode 设置为“force”
    -
    否则，SQLAlchemy 不保证处理 unicode 转换的任务。请注意，此标志为已经返回 unicode 对象的后端（大多数 DBAPI 所执行的操作）的后端操作增加了显着的性能开销。这个标志只能作为从不同或损坏编码的列中读取字符串的绝对最后手段，它只适用于首先接受无效编码的数据库（即 MySQL）。*不是*
    PG，Sqlite 等）[¶](#change-4add0a3ae9513d98fa991274564b4e51)

-   **[sql]**增加了数学否定运算符支持，-x。[¶](#change-fd8105345e50a3b6986674cfa2db831c)

-   **[sql]**FunctionElement subclasses are now directly executable the
    same way any func.foo() construct is, with automatic SELECT being
    applied when passed to
    execute().[¶](#change-375720ffaaf3679f497e76385994a25c)

-   **[sql]**
    func.foo()构造的“type”和“bind”关键字参数现在是“func”构造的本地对象，不属于 FunctionElement 基类的一部分，允许“类型“将在自定义构造函数或类级别变量中处理。[¶](#change-a8e7f19cf6b70ec1d6540a17f847c531)

-   **[sql]**将 keys()方法恢复到 ResultProxy。[¶](#change-4e51f442ae41f22cc4bff3527f97bf33)

-   **[sql]**The type/expression system now does a more complete job of
    determining the return type from an expression as well as the
    adaptation of the Python operator into a SQL operator, based on the
    full left/right/operator of the given expression. 特别是为 Postgresql
    EXTRACT 创建的日期/时间/间隔系统现在已被推广到类型系统中。现在通常不会发生以前经常出现的“列+文字”表达式，迫使“文字”类型与“列”类型相同，现在通常不会发生
    -
    “文字”类型首先从 Python 类型派生假定标准本地 Python 类型+日期类型，然后再回到表达式另一侧的已知类型。如果“后备”类型是兼容的（即来自字符串的 CHAR），则文字方将使用该类型。TypeDecorator 类型在默认情况下覆盖这个以强制无条件地强制“literal”，这可以通过实现 coerce\_compared\_value()方法来改变。也是。[¶](#change-543013779b4c9e5cad66c4531f5053e0)的一部分

    参考文献：[＃1647](http://www.sqlalchemy.org/trac/ticket/1647)，[＃1683](http://www.sqlalchemy.org/trac/ticket/1683)

-   **[sql]**Made sqlalchemy.sql.expressions.Executable part of public
    API, used for any expression construct that can be sent to
    execute().
    FunctionElement 现在继承可执行文件，以便获得 execution\_options()，这些文件也传播到 execute()中生成的 select()。依次可执行的子类\_Generative，它标记支持@\_generative 装饰器的任何 ClauseElement
    -
    为了编译器扩展的好处，这些也可能变成“public”。[¶](#change-4b04f7b3b18249863369ddef13e98ada)

-   **[sql]**A change to the solution for - an end-user defined bind
    parameter name that directly conflicts with a column-named bind
    generated directly from the SET or VALUES clause of an update/insert
    generates a compile error.
    这减少了调用计数并消除了一些不良名称冲突仍然可能发生的情况。[¶](#change-e18872438ff47328adbe402a50ef19b8)

    参考文献：[＃1579](http://www.sqlalchemy.org/trac/ticket/1579)

-   **[sql]**Column() requires a type if it has no foreign keys (this is
    not new).
    如果 Column()没有类型，也没有外键，则会产生错误。[¶](#change-25e52b132f46c6da5df9e4d2d1b3629e)

    参考文献：[＃1705](http://www.sqlalchemy.org/trac/ticket/1705)

-   **[sql]**the “scale” argument of the Numeric() type is honored when
    coercing a returned floating point value into a string on its way to
    Decimal - this allows accuracy to function on SQLite,
    MySQL.[¶](#change-1bd09db2f45aebf370068907a549222d)

    参考文献：[＃1717](http://www.sqlalchemy.org/trac/ticket/1717)

-   **[sql]**the copy() method of Column now copies over uninitialized
    “on table attach” events.
    帮助新的声明式“mixin”功能。[¶](#change-d1540ed7293cf73f522c47764b34b8db)

### MySQL 的[¶ T0\>](#change-0.6beta2-mysql "Permalink to this headline")

-   **[mysql]**修正了 COLLATE 存在的反射错误，可空标志和服务器默认值不会被反映出来。[¶](#change-a35014255c51338d324794124dabec73)

    参考文献：[＃1655](http://www.sqlalchemy.org/trac/ticket/1655)

-   **[mysql]**固定 TINYINT（1）“boolean”列的反射，使用 UNSIGNED 等整数标志定义。[¶](#change-0a377528b158add95b51614355824b86)

-   **[mysql]**进一步修正 mysql 连接器方言[¶](#change-c4476c66267aa9d53e5d3104352f2460)

    参考文献：[＃1668](http://www.sqlalchemy.org/trac/ticket/1668)

-   **[mysql]**
    InnoDB 上的“autoincrement”列不是第一个的复合 PK 表将在 CREATE
    TABLE 中发出明确的“KEY”短语，从而避免错误。[¶](#change-e5eef98bf3b744b814f45de869fa2400)

    参考文献：[＃1496](http://www.sqlalchemy.org/trac/ticket/1496)

-   **[mysql]**增加了对各种 MySQL 关键字的反射/创建表支持。[¶](#change-eabba2ee40f19b4f83f4b62f38ac3b3e)

    参考文献：[＃1634](http://www.sqlalchemy.org/trac/ticket/1634)

-   **[mysql]**修正了在 Windows 主机上反映表可能发生的导入错误[¶](#change-a4024dfc8c4693eea7c02add1a5b72f4)

    参考文献：[＃1580](http://www.sqlalchemy.org/trac/ticket/1580)

### 源码[¶ T0\>](#change-0.6beta2-sqlite "Permalink to this headline")

-   **[sqlite]**将“native\_datetime =
    True”标志添加到 create\_engine()。这会导致 DATE 和 TIMESTAMP 类型在连接上启用 PARSE\_DECLTYPES 的假设下跳过所有绑定参数和结果行处理。请注意，这与“func.current\_date()”不完全兼容，它将作为字符串返回。[¶](#change-686860a49e344194295bd7ddef459b1a)

    参考文献：[＃1685](http://www.sqlalchemy.org/trac/ticket/1685)

### MSSQL [¶ T0\>](#change-0.6beta2-mssql "Permalink to this headline")

-   **[mssql]**重新建立了对 pymssql 方言的支持[¶](#change-c43171d5ad2afdb8be0210f4345e7c3b)

-   **[mssql]**隐式返回，反射等的各种修复 -
    MS-SQL 方言在 0.6 中还不完整（但接近）[¶](#change-afec227c9a875855720b6369b4193326)

-   **[mssql]**增加了对 mxODBC 的基本支持。[¶](#change-0541548f6903480b3a322de8c54929ce)

    参考文献：[＃1710](http://www.sqlalchemy.org/trac/ticket/1710)

-   **[mssql]**删除了 text\_as\_varchar 选项。[¶](#change-dba80448eeea205b1bbaec327ac1de55)

### 预言[¶ T0\>](#change-0.6beta2-oracle "Permalink to this headline")

-   **[oracle]**“out”参数需要 cx\_oracle 支持的类型。如果找不到 cx\_oracle 类型，则会产生错误。[¶](#change-f2a132a1d5c7974e390d588eac834b3b)

-   **[oracle]**Oracle ‘DATE’ now does not perform any result
    processing, as the DATE type in Oracle stores full date+time
    objects, that’s what you’ll get.
    请注意，泛型类型.Date 类型*将*仍然对传入值调用 value.date()，但是。当反映一个表时，反射类型将是'DATE'。[¶](#change-ab6e812d286cec34322fb6829527927b)

-   **[oracle]**增加了对 Oracle 的 WITH\_UNICODE 模式的初步支持。至少，这为 Python
    3 创建了对 cx\_Oracle 的初始支持。当在 Python
    2.xx 中使用 WITH\_UNICODE 模式时，会发出一个大而可怕的警告，要求用户认真考虑使用这种困难的操作模式。[¶](#change-62c558744df2f44f9cb4bf1ff987ce86)

    参考文献：[＃1670](http://www.sqlalchemy.org/trac/ticket/1670)

-   **[oracle]**现在，except\_()方法在 Oracle 上呈现为 MINUS，这在该平台上或多或少是等同的。[¶](#change-774d1f88602325ba20cca6ce5c10734b)

    参考文献：[＃1712](http://www.sqlalchemy.org/trac/ticket/1712)

-   **[oracle]**添加了对 TIMESTAMP WITH TIME
    ZONE 的呈现和反映支持，即 TIMESTAMP（timezone =
    True）。[¶](#change-0e995c38104f4a4175d2a741f88b12bc)

    参考文献：[＃651](http://www.sqlalchemy.org/trac/ticket/651)

-   **[oracle]**现在可以反映 Oracle
    INTERVAL 类型。[¶](#change-21af7340803f01c63bb39084313092b9)

### 杂项[¶ T0\>](#change-0.6beta2-misc "Permalink to this headline")

-   **[py3k]**改进了关于 Python
    3 的安装/测试设置，现在 Distribute 在 Py3k 上运行。distribute\_setup.py 现在包含在内。有关 Python
    3 安装/测试说明，请参阅 README.py3k。[¶](#change-30f2fc874b9df7b7d141eef33c5d2468)

-   **[engines]**增加了一个可选的 C 扩展，通过重新实现 RowProxy 和最常用的结果处理器来加速 sql 层。实际的加速将很大程度上取决于您的 DBAPI 和您的表中使用的数据类型的混合，并且可以从 30％改进到 200％以上。它还为大型查询的 ORM 速度提供了适度（〜15-20％）的间接改进。请注意，默认情况下，*不是*内置/安装。请参阅自述文件以获取安装说明。[¶](#change-cdd5ac4118fc526b3b6e424254f9f575)

-   在“autocommit”场景中，在 DBAPI 连接上调用 commit()之前，执行顺序会从游标中拉取所有 rowcount
    /
    last 插入的 ID 信息。**[engines]**这有助于 mxodbc 与 rowcount，可能是一个好主意。[¶](#change-582f4dfd426b3da60af448476c0d9049)

-   **[engines]**打开日志记录，以便更频繁地调用 isEnabledFor()，以便在下次连接时反映引擎/池日志级别的更改。这增加了少量的方法调用开销。这是微不足道的，并且会在调用 create\_engine()之后正好配置日志时，使所有这些情况的生活变得更加轻松。[¶](#change-8339a8f6f9f054e9871057ff44eb310b)

    参考文献：[＃1719](http://www.sqlalchemy.org/trac/ticket/1719)

-   **[engines]**不推荐使用 assert\_unicode 标志。SQLAlchemy 将在所有要求对非 Unicode
    Unicode 字符串进行编码的情况下以及 Unicode 或 UnicodeType 类型显式传递字符串时发出警告。对于已经接受 Python
    unicode 对象的 DBAPI，String 类型不会做任何事情。[¶](#change-44b744d4299fe9fd0c15e0b51548c21c)

-   **[engines]**绑定参数作为元组而不是列表发送。一些后端驱动程序不会接受绑定参数作为列表。[¶](#change-e486cdddb6da9fcd5b78a7e384f517e3)

-   **[engines]** threadlocal 引擎在 close()时没有正确关闭连接 -
    修正了[¶](#change-31babb385ad99c9c8dfef800a188b08f)

-   **[engines]**如果事务对象不是“活动”，事务对象不会回滚或提交，允许更准确地嵌套 begin
    / rollback / commit。[¶](#change-6a84cce20a490a05b2ae3aa704d0b11f)

-   **[engines]**作为绑定的 Python
    unicode 对象导致 Unicode 类型，而不是字符串，从而消除了不支持 unicode 绑定的驱动程序中的某类 unicode 错误。[¶](#change-2e55f14274c2191236e3104fac4e24de)

-   **[engines]**将 create\_engine()，Pool()构造函数以及“pool\_logging\_name”参数的参数添加到 create\_engine()，该参数过滤到 Pool 的参数。在记录消息的“名称”字段中发出给定的字符串名称，而不是缺省的十六进制标识符字符串。[¶](#change-2a0cef92888b2be98785ecc9a097653c)

    参考文献：[＃1555](http://www.sqlalchemy.org/trac/ticket/1555)

-   **[engines]**
    Dialect 的 visit\_pool()方法被删除，并被 on\_connect()取代。此方法返回一个可调用对象，它在创建每个对象后接收原始 DBAPI 连接。如果为非无，则可调用组件通过连接策略组装成 first\_connect
    / connect
    pool 侦听器。为方言提供更简单的界面。[¶](#change-81eacba0128286c062f03c539e3fb32a)

-   **[engines]**
    StaticPool 现在可以在不打开新连接的情况下初始化，处理和重新创建连接 -
    连接仅在第一次请求时打开。dispose()现在也可以在 AssertionPool 上工作。[¶](#change-6fb3ebb61d325e02bee2444d540be282)

    参考文献：[＃1728](http://www.sqlalchemy.org/trac/ticket/1728)

-   **[ticket: 1673] [metadata]**通过传递“schema =
    None”作为参数，增加了在使用“tometadata”时去除模式信息的功能。如果没有指定 schema，那么该表的模式将被保留。[¶](#change-19e2f337ca9a7555b3e2cd9f34026221)

-   **[declarative]** DeclarativeMeta 独占使用 cls .\_\_
    dict\_\_（不是 dict\_）作为类信息的来源；
    \_as\_declarative 只使用传递给它的 dict\_作为类信息的来源（当使用 DeclarativeMeta 时，它是 cls
    .\_\_
    dict\_\_）。这在理论上应该使定制元类更容易修改传入\_as\_declarative 的状态。[¶](#change-17e6d2319b8bfe217416295a2d06d196)

-   **[declarative]**declarative now accepts mixin classes directly, as
    a means to provide common functional and column-based elements on
    all subclasses, as well as a means to propagate a fixed set of
    \_\_table\_args\_\_ or \_\_mapper\_args\_\_ to subclasses.
    对于\_\_table\_args \_\_ / \_\_
    mapper\_args\_\_从继承的 mixin 到本地的自定义组合，现在可以使用描述符。新的细节都在声明性文档中。感谢 Chris
    Withers 为此付出了努力。[¶](#change-a6fb16c5b4efc1b1336ae57e0611eb05)

    参考文献：[＃1707](http://www.sqlalchemy.org/trac/ticket/1707)

-   **[declarative]**the \_\_mapper\_args\_\_ dict is copied when
    propagating to a subclass, and is taken straight off the class
    \_\_dict\_\_ to avoid any propagation from the parent.
    映射器继承已经从父映射器传播你想要的东西。[¶](#change-712b74c929fe77fb05e228b508010508)

    参考文献：[＃1393](http://www.sqlalchemy.org/trac/ticket/1393)

-   **[declarative]**当一个单表子类指定一个已存在于基类中的列时会引发异常。[¶](#change-cdbe265dab1874af885c1b8130cb2eee)

    参考文献：[＃1732](http://www.sqlalchemy.org/trac/ticket/1732)

-   **[sybase]**为 Sybase 实施了一个初步工作方言，其中包含 Python-Sybase 和 Pyodbc 的子实现。处理表格创建/删除和基本往返功能。尚未包含对 unicode
    /特殊表达式/
    etc 等的反映或全面支持[¶](#change-59b20e0d794888b5924ddb106a96ce97)

-   **[examples]**稍微更改了烧杯缓存示例，以便为 lazyload 缓存提供单独的 RelationCache 选项。该对象通过将几个分组到一个通用结构中，可以更有效地查找任何数量的潜在属性。FromCache 和 RelationCache 都更简单。[¶](#change-2fba82fbacb3e70a6a774aa1e8e81f74)

-   **[documentation]**文档中的主要清理工作将类，函数和方法名称链接到 API 文档中。[¶](#change-e7846468739660d7e6ad96f9435b4871)

    参考文献：[＃1700](http://www.sqlalchemy.org/trac/ticket/1700)

0.6beta1 [¶ T0\>](#change-0.6beta1 "Permalink to this headline")
----------------------------------------------------------------

发布日期：2010 年 2 月 3 日

### ORM [¶ T0\>](#change-0.6beta1-orm "Permalink to this headline")

-   **[orm]**

    query.update()和 query.delete()的更改：
    :   -   query.update()的'expire'选项已被重命名为'fetch'，因此与 query.delete()的匹配。'过期'已弃用并发出警告。
        -   对于同步策略，query.update()和 query.delete()都默认为“评估”。
        -   update()和 delete()的“同步”策略会在失败时产生错误。没有隐含的回退到“获取”。评估失败是基于标准的结构，所以成功/失败是基于代码结构的确定性。

    [¶](#change-dc6ff9eba416b02d740a8dd8fcf216cb)

-   **[orm]**

    多对一关系的增强：
    :   -   多对一的关系现在会在更少的情况下触发延迟加载，包括在大多数情况下不会在更换新代码时获取“旧”值。
        -   现在，对于一个简单加载（称为“use\_get”条件），即 Related-\>
            Sub（Base），使用 get()方法的多对一关系无需重新定义 primaryjoin 条件的基表。
        -   指定具有声明列的外键，即 ForeignKey（MyRelatedClass.id）不会中断发生的“use\_get”条件
        -   relation()，eagerload()和 eagerload\_all()现在具有一个名为“innerjoin”的选项。指定 True 或 False 来控制 eager 连接是否构造为 INNER 或 OUTER 连接。与往常一样，默认为 False。映射器选项将覆盖关系()中指定的任何设置。通常应该设置为多对一，而不是可空的外键关系，以提高连接性能。
        -   当 LIMIT /
            OFFSET 出现时，预加载的行为使得主查询被包装在子查询中，现在对于所有紧急加载都是多对一连接的情况来说是个例外。在这种情况下，由于多对一连接不会将行添加到结果中，所以急切连接与限制/偏移一起直接与父表对齐，而无需额外的子查询开销。

    [¶](#change-b0f39f3d2c314fb24db07687b5d6ce5c)

    References: [\#1186](http://www.sqlalchemy.org/trac/ticket/1186),
    [\#1492](http://www.sqlalchemy.org/trac/ticket/1492),
    [\#1544](http://www.sqlalchemy.org/trac/ticket/1544)

-   **[orm]**
    Session.merge()的增强/改变：[¶](#change-214672957cd89d4ecddac4104c865548)

-   **[orm]** Session.merge()上的“dont\_load =
    True”标志被弃用，现在是“load =
    False”。[¶](#change-2ec8e6a30ef412d4ca9f79d541de4fd2)

-   **[orm]**Session.merge() is performance optimized, using half the
    call counts for “load=False” mode compared to 0.5 and significantly
    fewer SQL queries in the case of collections for “load=True”
    mode.[¶](#change-54940eafb98ef2da97a3d986ce185a1a)

-   **[orm]**merge() will not issue a needless merge of attributes if
    the given instance is the same instance which is already
    present.[¶](#change-2bed1f32297bbc130f45b4d30b89c291)

-   **[orm]**merge() now also merges the “options” associated with a
    given state, i.e. those passed through query.options() which follow
    along with an instance, such as options to eagerly- or lazyily- load
    various attributes.
    这对于构建高度集成的缓存方案至关重要。这是一个微妙的行为变化与 0.5.
    [¶](#change-2bbbf3e1665069128942de0c7eef6060)

-   **[orm]**修正了关于实例状态中存在的“加载路径”的序列化的 bug，当将 merge()与序列化状态的使用以及相关的选项组合起来时，这也是必需的保存。[¶
    T2\>](#change-2a96bff0a75bb240bdfc1fd98a705c7b)

-   **[orm]**全新的 merge()将以一个新的综合示例展示如何将 Beaker 与 SQLAlchemy 集成。请参阅下面的“示例”注释中的注释。[¶](#change-023079a39b7b68c5ea1d0a6ae57374d8)

-   **[orm]**Primary key values can now be changed on a joined-table
    inheritance object, and ON UPDATE CASCADE will be taken into account
    when the flush happens. 使用 SQLite 或 MySQL /
    MyISAM 时，在 mapper()上将新的“passive\_updates”标志设置为 False
    [¶](#change-d92b5ce0bd2745798d570f1d7a477427)

    参考文献：[＃1362](http://www.sqlalchemy.org/trac/ticket/1362)

-   **[orm]**flush() now detects when a primary key column was updated
    by an ON UPDATE CASCADE operation from another primary key, and can
    then locate the row for a subsequent UPDATE on the new PK value.
    当关系()存在以建立关系以及 passive\_updates =
    True 时，会发生这种情况。[¶](#change-acdcc601f3f43f3d50ffd4a7eccab5ee)

    参考文献：[＃1671](http://www.sqlalchemy.org/trac/ticket/1671)

-   **[orm]**the “save-update” cascade will now cascade the pending
    *removed* values from a scalar or collection attribute into the new
    session during an add() operation.
    这样 flush()操作也会删除或修改这些断开项目的行。[¶](#change-7885463e500d075f4f8777f53615642f)

-   **[orm]**现在使用带有“辅助”表的“动态”加载器生成一个查询，其中“辅助”表*不是*别名。这允许辅助 Table 对象用在 relation()的“order\_by”属性中，并且还允许将其用于针对动态关系的过滤标准。[¶](#change-77148312513d999f0abe3daa49304c4d)

    参考文献：[＃1531](http://www.sqlalchemy.org/trac/ticket/1531)

-   **[orm]**relation() with uselist=False will emit a warning when an
    eager or lazy load locates more than one valid value for the row.
    这可能是由于 primaryjoin / secondaryjoin 条件不适合渴望的 LEFT OUTER
    JOIN 或其他条件。[¶](#change-5e3ba4eff181a0ee2c6a2fae40497392)

    参考文献：[＃1643](http://www.sqlalchemy.org/trac/ticket/1643)

-   **[orm]**an explicit check occurs when a synonym() is used with
    map\_column=True, when a ColumnProperty (deferred or otherwise)
    exists separately in the properties dictionary sent to mapper with
    the same keyname.
    而不是默默地替换现有的属性（以及该属性的可能选项），会引发错误。[¶](#change-928ff4154d8bca4127164af262f91d97)

    参考文献：[＃1633](http://www.sqlalchemy.org/trac/ticket/1633)

-   **[orm]**a “dynamic” loader sets up its query criterion at
    construction time so that the actual query is returned from
    non-cloning accessors like
    “statement”.[¶](#change-07718a8de32eb50efa4fbd07e5184cb6)

-   **[orm]**当迭代一个 Query()时返回的“named
    tuple”对象现在可以被 pickleable
    [¶](#change-9dd1e1039ec6832335cf05098fdffa0c)

-   **[orm]**mapping to a select() construct now requires that you make
    an alias() out of it distinctly.
    这可以消除对[¶](#change-06b035d8abba0f380e9761dbd450e938)等问题的混淆

    参考文献：[＃1542](http://www.sqlalchemy.org/trac/ticket/1542)

-   **[orm]**
    query.join()已被重写以提供更一致的行为和更多的灵活性（包括）[¶](#change-2f33bb379421251fd948d3fc38923eb1)

    参考文献：[＃1537](http://www.sqlalchemy.org/trac/ticket/1537)

-   **[orm]**query.select\_from() accepts multiple clauses to produce
    multiple comma separated entries within the FROM clause.
    从多宿主连接()子句中选择时很有用。[¶](#change-6f2e3f51e6cb88f3cc790e88cde5f7c3)

-   **[orm]**query.select\_from() also accepts mapped classes, aliased()
    constructs, and mappers as arguments.
    特别是当从多个连接表类查询以确保完整连接被呈现时，这有助于。[¶](#change-0b82102fe6a1de325bd22dc40d50c613)

-   **[orm]**query.get() can be used with a mapping to an outer join
    where one or more of the primary key values are
    None.[¶](#change-3d610c09f7696ca04d48bc82efab5c5b)

    参考文献：[＃1135](http://www.sqlalchemy.org/trac/ticket/1135)

-   **[orm]**query.from\_self(), query.union(), others which do a
    “SELECT \* from (SELECT...)” type of nesting will do a better job
    translating column expressions within the subquery to the columns
    clause of the outer query.
    这可能与 0.5 后向不兼容，因为这可能会破坏没有应用标签的文字表达式（即 literal（'foo'）等）。[](#change-0138642ce02e6d403c6713a13a4f9802)

    参考文献：[＃1568](http://www.sqlalchemy.org/trac/ticket/1568)

-   **[orm]**关系 primaryjoin 和 secondaryjoin 现在检查它们是否是列表达式，而不仅仅是子句元素。这禁止像 FROM 表达式那样直接放在那里。[¶](#change-e03cf72a3995480562eafd69ef7d11f0)

    参考文献：[＃1622](http://www.sqlalchemy.org/trac/ticket/1622)

-   **[orm]**expression.null() is fully understood the same way None is
    when comparing an object/collection-referencing attribute within
    query.filter(), filter\_by(),
    etc.[¶](#change-0469e777a8df1fc45afc3ecfd6383189)

    参考文献：[＃1415](http://www.sqlalchemy.org/trac/ticket/1415)

-   **[orm]**添加了“make\_transient()”辅助函数，该函数将持久性/分离性实例转换为临时性实例（即，删除 instance\_key 并从任何会话中删除）。[](#change-9d19cad8b2bcb624aa80df1327549f23)

    参考文献：[＃1052](http://www.sqlalchemy.org/trac/ticket/1052)

-   **[orm]**不推荐使用 mapper()上的 allow\_null\_pks 标志，并且该功能默认为“打开”。这意味着对于任何主键列都有一个非空值的行将被视为一个标识。通常只有在映射到外连接时才需要这种情况。[¶](#change-cd19ca85ff6299764da7a16446668186)

    参考文献：[＃1339](http://www.sqlalchemy.org/trac/ticket/1339)

-   **[orm]**the mechanics of “backref” have been fully merged into the
    finer grained “back\_populates” system, and take place entirely
    within the \_generate\_backref() method of RelationProperty.
    这使得 RelationProperty 的初始化过程更简单，并允许设置（例如从 RelationProperty 的子类）更容易地传播到反向引用。内部的 BackRef()消失了，backref()返回一个被 RelationProperty 理解的普通元组。[¶](#change-889fc60ec4cd97646ec09e69b067e826)

-   **[orm]**
    mapper()上的 version\_id\_col 特性在与不支持“rowcount”的方言一起使用时会引发警告。[¶](#change-99cae53917a87e88ac70a5d5a153cdf9)

    参考文献：[＃1569](http://www.sqlalchemy.org/trac/ticket/1569)

-   **[orm]**将“execution\_options()”添加到 Query 中，以便可以将选项传递给结果语句。目前只有 Select 语句具有这些选项，唯一使用的选项是“stream\_results”，而知道“stream\_results”的唯一方言是 psycopg2.
    [¶](#change-d516d907637bb775eebd34e7ee58ed13)

-   **[orm]**
    Query.yield\_per()会自动设置“stream\_results”语句选项。[¶](#change-573842e45f126bdd2938caf4c37f003e)

-   **[orm]**

    已弃用或已删除：
    :   -   mapper()上的'allow\_null\_pks'标志已被弃用。它现在什么都不做，并且在所有情况下都是“开启”的。
        -   sessionmaker()上的'transactional'标志被删除。使用'autocommit
            = True'来表示'transactional = False'。
        -   mapper()上的'polymorphic\_fetch'参数被删除。加载可以使用'with\_polymorphic'选项进行控制。
        -   mapper()上的'select\_table'参数被删除。为此功能使用'with\_polymorphic
            =（“\*”，）'。
        -   同义词()的'代理'参数被删除。这个标志在整个 0.5 中没有做任何事情，因为“代理生成”行为现在是自动的。
        -   将单个元素列表传递给 eagerload()，eagerload\_all()，contains\_eager()，lazyload()，defer()和 undefer()而不是多个位置\*参数已被弃用。
        -   将单个元素列表传递给 query.order\_by()，query.group\_by()，query.join()或 query.outerjoin()而不是多个位置\*参数已弃用。
        -   query.iterate\_instances()被删除。使用 query.instances()。
        -   Query.query\_from\_parent()被删除。使用 sqlalchemy.orm.with\_parent()函数生成一个“父”子句，或者 query.with\_parent()。
        -   query.\_from\_self()被移除，请改用 query.from\_self()。
        -   composite()的“comparator”参数被删除。使用“comparator\_factory”。
        -   RelationProperty.\_get\_join()被删除。
        -   Session 上的'echo\_uow'标志被删除。在“sqlalchemy.orm.unitofwork”名称上使用日志记录。
        -   session.clear()被删除。使用 session.expunge\_all()。
        -   session.save()，session.update()，session.save\_or\_update()被删除。使用 session.add()和 session.add\_all()。
        -   session.flush()上的“objects”标志仍然被弃用。
        -   session.merge()中的“dont\_load = True”标志不赞成使用“load =
            False”。
        -   ScopedSession.mapper 保持不推荐使用。请参阅[http://www.sqlalchemy.org/trac/wiki/UsageRecipes/SessionAwareMapper](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/SessionAwareMapper)中的使用配方
        -   将 InstanceState（内部 SQLAlchemy 状态对象）传递给 attributes.init\_collection()或 attributes.get\_history()已弃用。这些函数是公共 API，通常需要一个常规的映射对象实例。
        -   declarative\_base()的'engine'参数被删除。使用'bind'关键字参数。

    [¶](#change-d843edca2b75b293e8e6826030ff0227)

### SQL [¶ T0\>](#change-0.6beta1-sql "Permalink to this headline")

-   **[sql]**the “autocommit” flag on select() and text() as well as
    select().autocommit() are deprecated - now call
    .execution\_options(autocommit=True) on either of those constructs,
    also available directly on Connection and
    orm.Query.[¶](#change-fb7c367607c59c771a13ad200c90eff3)

-   **[sql]**the autoincrement flag on column now indicates the column
    which should be linked to cursor.lastrowid, if that method is used.
    有关详细信息，请参阅 API 文档。[¶](#change-02d9b147f287fd9766176ef94cdc13cc)

-   **[sql]**an executemany() now requires that all bound parameter sets
    require that all keys are present which are present in the first
    bound parameter set.
    插入/更新语句的结构和行为很大程度上取决于第一个参数集，其中包括哪些缺省值将被触发，并且所有其余缺省值都会执行最小猜测操作，以便不影响性能。出于这个原因，默认情况会以默默的方式“失败”，因为这是现在的防范。[¶](#change-44921036aa99c1e3663922170c206e27)

    参考文献：[＃1566](http://www.sqlalchemy.org/trac/ticket/1566)

-   **[sql]**returning() support is native to insert(), update(),
    delete().
    Postgresql，Firebird，MSSQL 和 Oracle 存在不同级别功能的实现。可以使用列表达式显式调用返回()，这些列表达式通常通过 fetchone()或 first()返回结果集。

    如果正在使用的数据库版本支持它（执行版本号检查），则 insert()构造也将隐式地使用 RETURNING 来获取新生成的主键值。如果没有指定最终用户返回()，则会发生这种情况。

    [¶](#change-e095b275cd65347bb96a118ac93a37c4)

-   **[sql]**union(), intersect(), except() and other “compound” types
    of statements have more consistent behavior w.r.t.
    圆括号。嵌入在另一个元素中的每个复合元素现在将用括号分组 -
    之前，列表中的第一个复合元素不会被分组，因为 SQLite 不喜欢以括号开头的语句。但是，Postgresql 尤其具有关于 INTERSECT 的优先规则，并且对于括号同样适用于所有子元素更为一致。所以现在，SQLite 的解决方法也是以前 PG 的解决方法
    -
    当嵌套复合元素时，第一个通常需要调用“.alias()。select()”以将其包装在子查询中。[¶
    T0\>](#change-8bc93521d51aa26c8f23a0d45da1f78f)

    参考文献：[＃1665](http://www.sqlalchemy.org/trac/ticket/1665)

-   **[sql]**insert() and update() constructs can now embed bindparam()
    objects using names that match the keys of columns.
    这些绑定参数将绕过通常路由到生成的 SQL 的 VALUES 或 SET 子句中显示的那些键。[¶](#change-ddbccf30154057e0b830866c4813ff38)

    参考文献：[＃1579](http://www.sqlalchemy.org/trac/ticket/1579)

-   **[sql]**the Binary type now returns data as a Python string (or a
    “bytes” type in Python 3), instead of the built- in “buffer” type.
    这允许二进制数据的对称往返行程。[¶](#change-2234986f2a344f994dd47e033a358adf)

    参考文献：[＃1524](http://www.sqlalchemy.org/trac/ticket/1524)

-   **[sql]**添加了 tuple\_()构造，允许将表达式集与另一个集进行比较，通常使用 IN 对复合主键或类似进行比较。还接受具有多个列的 IN。“标量选择只能有一列”的错误信息被删除
    -
    将依赖于数据库来报告与 col 不匹配的问题。[¶](#change-d289821e49dd5b365135f2c232b5cf05)

-   **[sql]**User-defined “default” and “onupdate” callables which
    accept a context should now call upon “context.current\_parameters”
    to get at the dictionary of bind parameters currently being
    processed.
    无论是单执行还是执行语句执行，该字典都可以以相同方式使用。[¶](#change-d00d40f3ec5206589179af88c62a6276)

-   **[sql]**multi-part schema names, i.e. with dots such as
    “dbo.master”, are now rendered in select() labels with underscores
    for dots, i.e. “dbo\_master\_table\_column”.
    这是一个“友好”的标签，在结果集中表现更好。[¶](#change-7d51e4139db389357f578e2a93a26383)

    参考文献：[＃1428](http://www.sqlalchemy.org/trac/ticket/1428)

-   **[sql]**removed needless “counter” behavior with select()
    labelnames that match a column name in the table, i.e. generates
    “tablename\_id” for “id”, instead of “tablename\_id\_1” in an
    attempt to avoid naming conflicts, when the table has a column
    actually named “tablename\_id” - this is because the labeling logic
    is always applied to all columns so a naming conflict will never
    occur.[¶](#change-37c425d83297ecedcb415b054cbfb50d)

-   **[sql]**calling expr.in\_([]), i.e. with an empty list, emits a
    warning before issuing the usual “expr != expr” clause. “expr！=
    expr”可能非常昂贵，如果列表为空，则最好是不发出 in\_()，而不是简单地查询或修改标准以适应更复杂的情况。[¶\<
    / T0\>](#change-1577657989ab5d5a2f90784ad84ebc9c)

    参考文献：[＃1628](http://www.sqlalchemy.org/trac/ticket/1628)

-   **[sql]**Added “execution\_options()” to select()/text(), which set
    the default options for the Connection.
    请参阅“引擎”中的注释。[¶](#change-68e1263644f8e10f85069545aa29651b)

-   **[sql]**

    已弃用或已删除：
    :   -   select()上的“标量”标志被删除，使用 select.as\_scalar()。
        -   bindparam()上的“shortname”属性被删除。
        -   postgres\_returning，insert()，update()，delete()上的 firebird\_returning 标志都被弃用，使用新的返回()方法。
        -   加入时的 fold\_equivalents 标志已被弃用（将保持到实施）

    [¶](#change-75e0f1cc822ddf23d6706587c9fff333)

    参考文献：[＃1131](http://www.sqlalchemy.org/trac/ticket/1131)

### 架构[¶ T0\>](#change-0.6beta1-schema "Permalink to this headline")

-   **[schema]**
    MetaData 的\_\_包含\_\_()方法现在接受字符串或表对象作为参数。如果给定表，则首先将参数转换为 table.key，即“[SCHEMANAME。]
    ” [¶ T1\> T0\>](#change-ff302fdf3eae53485eaf643550894fce)

    参考文献：[＃1541](http://www.sqlalchemy.org/trac/ticket/1541)

-   **[schema]**deprecated MetaData.connect() and
    ThreadLocalMetaData.connect() have been removed - send the “bind”
    attribute to bind a
    metadata.[¶](#change-a9146fbceff794c8fb5012e08c8f2197)

-   **[schema]**不赞成使用 metadata.table\_iterator()方法（使用 sorted\_tables）[¶](#change-d414bfe8495de9441bb1bf9a225a8196)

-   **[schema]**不推荐使用 PassiveDefault -
    使用 DefaultClause。[¶](#change-bc8dd4045ac44c12d17016986c52e8a4)

-   **[schema]**the “metadata” argument is removed from DefaultGenerator
    and subclasses, but remains locally present on Sequence, which is a
    standalone construct in
    DDL.[¶](#change-6438f724479e0e0d1cc699f14e1cd25b)

-   **[schema]**从 Index 和 Constraint 对象中删除了公共可变性：

    > -   ForeignKeyConstraint.append\_element()
    > -   Index.append\_column()
    > -   UniqueConstraint.append\_column()
    > -   PrimaryKeyConstraint.add()
    > -   PrimaryKeyConstraint.remove()

    这些应该以声明方式构建（即在一个构造中）。

    [¶](#change-1289d6e528c69ff4828bd5851baaeb61)

-   **[schema]**
    Sequence 上的“start”和“increment”属性现在默认在 Oracle 和 Postgresql 上生成“START
    WITH”和“INCREMENT
    BY”。Firebird 现在不支持这些关键字。[¶](#change-ffb3a65d9b8484533b1fb233f819985e)

    参考文献：[＃1545](http://www.sqlalchemy.org/trac/ticket/1545)

-   **[schema]**
    UniqueConstraint，Index，PrimaryKeyConstraint 都接受列名或列对象列表作为参数。[¶](#change-a8942fa6a4323b73e46a368c718b08e8)

-   **[schema]**

    其他删除的东西：
    :   -   Table.key（不知道这是什么）
        -   Table.primary\_key 不可分配 -
            使用 table.append\_constraint（PrimaryKeyConstraint（...））
        -   Column.bind（通过 column.table.bind 获取）
        -   Column.metadata（通过 column.table.metadata 获取）
        -   Column.sequence（使用 column.default）
        -   ForeignKey（约束= some\_parent）（现在是私人\_constraint）

    [¶](#change-9888d956fff0bd32aa9a418e14e7df29)

-   **[schema]**
    ForeignKey 上的 use\_alter 标志现在是可以使用 DDL()事件系统手动构建的操作的快捷选项。A
    side effect of this refactor is that ForeignKeyConstraint objects
    with use\_alter=True will *not* be emitted on SQLite, which does not
    support ALTER for foreign
    keys.[¶](#change-45384a58304926e78dbc93a8bc4bdbea)

-   **[schema]**现在，ForeignKey 和 ForeignKeyConstraint 对象正确地 copy()所有公共关键字参数。[¶](#change-39be51b87c7530f3281ae5dc05fc5294)

    参考文献：[＃1605](http://www.sqlalchemy.org/trac/ticket/1605)

### 的 PostgreSQL [¶ T0\>](#change-0.6beta1-postgresql "Permalink to this headline")

-   **[postgresql]**新的方言：py3k 上的 pg8000，zxjdbc 和 pypostgresql。[¶](#change-8e276ba771e1923acab769effd7fdebf)

-   **[postgresql]**“postgres”方言现在被命名为“postgresql”！连接字符串如下所示：

    > > postgresql：// scott：tiger @ localhost / test postgresql +
    > > pg8000：// scott：tiger @ localhost / test
    >
    > “postgres”的名字仍然以下列方式向后兼容：
    >
    > > -   有一个“postgres.py”虚拟方言，它允许旧的 URL 工作，即 postgres：//
    > >     scott：tiger @ localhost / test
    > > -   可以从旧的“数据库”模块中导入“postgres”名称，即从“sqlalchemy.databases
    > >     import postgres”以及“方言”，“from
    > >     sqlalchemy.dialects.postgres import base as
    > >     pg”，将发送弃用警告。
    > > -   现在特殊表达式参数被命名为“postgresql\_returning”和“postgresql\_where”，但较旧的“postgres\_returning”和“postgres\_where”名称仍然适用于弃用警告。

    [¶](#change-0ce9ee480a5a66cb9f77e0207f6dfc70)

-   **[postgresql]**“postgresql\_where”现在接受 SQL 表达式，该表达式还可以包含文字，这些文字将根据需要引用。[¶](#change-32e87704d92335d84d218fb1a739484d)

-   **[postgresql]**
    psycopg2 方言现在在所有新连接上使用 psycopg2 的“unicode 扩展”，它允许所有的 String
    / Text
    /等。类型以避免需要将字节串后处理到 unicode（由于其体积而导致的昂贵步骤）。本地返回 unicode 的其他方言（pg8000，zxjdbc）也会跳过 unicode 后期处理。[¶](#change-eb44c66b3b7d732aeac35e9d8ea81bdc)

-   **[postgresql]**添加了新的 ENUM 类型，该类型作为模式级结构存在并扩展了泛型枚举类型。自动将自身与表及其父元数据相关联，以根据需要发出适当的 CREATE
    TYPE / DROP
    TYPE 命令，支持 unicode 标签，支持反射。[¶](#change-38d3d336ce046ae00fc5d2a0a17fae47)

    参考文献：[＃1511](http://www.sqlalchemy.org/trac/ticket/1511)

-   **[postgresql]**
    INTERVAL 支持与 PG 接受的参数相对应的可选“precision”参数。[¶](#change-0efdc52b41c7cbb4edde516d0cf35ebd)

-   **[postgresql]**使用新的 dialect.initialize()功能设置依赖于版本的行为。[¶](#change-ce8ff886d9ea060a749895bb38ba108c)

-   **[postgresql]**somewhat better support for % signs in table/column
    names; psycopg2 can’t handle a bind parameter name of %(foobar)s
    however and SQLA doesn’t want to add overhead just to treat that one
    non-existent use case.[¶](#change-525b22121367b91b5ed308272c08ce24)

    参考文献：[＃1279](http://www.sqlalchemy.org/trac/ticket/1279)

-   **[postgresql]**将 NULL 插入到主键+外键列中将允许引发“not null
    constraint”错误，而不是尝试执行不存在的“col\_id\_seq”序列。[¶
    T2\>](#change-4fe9c121af9d9045fdae2cb23d04a9bd)

    参考文献：[＃1516](http://www.sqlalchemy.org/trac/ticket/1516)

-   **[postgresql]** autoincrement
    SELECT 语句，即从修改行的过程中选择的语句现在可以在服务器端游标模式下工作（指定的游标不用于这种语句）。[¶
    T2\>](#change-cf8ec160ec789b23afbd8a5fffd65a67)

-   **[postgresql]**postgresql dialect can properly detect pg “devel”
    version strings, i.e.
    “8.5devel”[¶](#change-b98cc90c64cb3bba3ab1bda67c0d1dbd)

    参考文献：[＃1636](http://www.sqlalchemy.org/trac/ticket/1636)

-   **[postgresql]**
    psycopg2 现在遵守语句选项“stream\_results”。该选项将覆盖连接设置“server\_side\_cursors”。如果为 true，则服务器端游标将用于该语句。如果为 false，即使连接上的“server\_side\_cursors”为真，它们也不会被使用。[¶](#change-df47fe2890dbf80af0c731002686995e)

    参考文献：[＃1619](http://www.sqlalchemy.org/trac/ticket/1619)

### MySQL 的[¶ T0\>](#change-0.6beta1-mysql "Permalink to this headline")

-   **[mysql]**New dialects: oursql, a new native dialect, MySQL
    Connector/Python, a native Python port of MySQLdb, and of course
    zxjdbc on Jython.[¶](#change-7a47739bb4cdfd029d2ad396df7e6bd3)

-   **[mysql]** VARCHAR /
    NVARCHAR 不会在没有长度的情况下呈现，在传递给 MySQL 之前会产生错误。不影响 CAST，因为无论如何，在 MySQL
    CAST 中都不允许 VARCHAR，在这种情况下，方言呈现 CHAR /
    NCHAR。[¶](#change-7f170bebdb4d3fbbf03679e858799239)

-   **[mysql]**all the \_detect\_XXX() functions now run once underneath
    dialect.initialize()[¶](#change-5a1277f6fa3da9da056c0b6ab7278415)

-   **[mysql]**somewhat better support for % signs in table/column
    names; MySQLdb can’t handle % signs in SQL when executemany() is
    used, and SQLA doesn’t want to add overhead just to treat that one
    non-existent use case.[¶](#change-3392dd5483c5d3b9c1d83017e78bf58e)

    参考文献：[＃1279](http://www.sqlalchemy.org/trac/ticket/1279)

-   **[mysql]**在所有情况下，BINARY 和 MSBinary 类型现在都会生成“BINARY”。省略“length”参数将生成没有长度的“BINARY”。使用 BLOB 生成未经修改的二进制列。[¶](#change-5ecc352d1de84aa90c39746ab807efe1)

-   **[mysql]**不建议使用 MSEnum / ENUM 的“quoting
    ='quoted'”参数。最好依靠自动引用。[¶](#change-188cc3f410c74dcfcbee1067d88343f8)

-   **[mysql]**如果给定的标签名是 unicode 对象，ENUM 现在子类化新的泛型 Enum 类型，并且还隐式处理 unicode 值。[¶](#change-9857837ab57118c270956f183581049e)

-   **[mysql]**如果“nullable =
    False”没有传递给 Column()，并且没有默认值，那么 TIMESTAMP 类型的列现在默认为 NULL。现在这与所有其他类型一致，并且在 TIMESTAMP 的情况下，由于 MySQL 对 TIMESTAMP 列的默认可空性进行“切换”，显式呈现“NULL”。[¶](#change-3a5af57ac623dd1f8cfef840898452b2)

    参考文献：[＃1539](http://www.sqlalchemy.org/trac/ticket/1539)

### 源码[¶ T0\>](#change-0.6beta1-sqlite "Permalink to this headline")

-   **[sqlite]**
    DATE，TIME 和 DATETIME 类型现在可以使用可选的 storage\_format 和 regexp 参数。storage\_format 可用于使用自定义字符串格式来存储这些类型。regexp 允许使用自定义正则表达式来匹配来自数据库的字符串值。[¶](#change-cdd833e10180536b712d6cf4e72992c4)

-   **[sqlite]**现在，Time 和 DateTime 类型默认使用更严格的正则表达式来匹配数据库中的字符串。如果您使用的是以传统格式存储的数据，请使用 regexp 参数。[¶](#change-f1b7d03a6b936597bce7908effb557cc)

-   SQLite 中的**[sqlite]** \_\_ legacy\_microseconds\_\_
    Time 和 DateTime 类型不再受支持。您应该使用 storage\_format 参数。[¶](#change-c35f7a555ea6c9d52e60250e368f50dc)

-   **[sqlite]**Date, Time and DateTime types are now stricter in what
    they accept as bind parameters: Date type only accepts date objects
    (and datetime ones, because they inherit from date), Time only
    accepts time objects, and DateTime only accepts date and datetime
    objects.[¶](#change-7158af5ebe6bfe2924688710bf9d16c4)

-   **[sqlite]**Table() supports a keyword argument
    “sqlite\_autoincrement”, which applies the SQLite keyword
    “AUTOINCREMENT” to the single integer primary key column when
    generating DDL. 将防止生成单独的 PRIMARY
    KEY 约束。[¶](#change-24b4b7e7be9ca2ec058e2bb450f0cde1)

    参考文献：[＃1016](http://www.sqlalchemy.org/trac/ticket/1016)

### MSSQL [¶ T0\>](#change-0.6beta1-mssql "Permalink to this headline")

-   **[mssql]** MSSQL + Pyodbc +
    FreeTDS 现在大部分都可以使用，可能有二进制数据和 unicode 模式标识符的例外。[¶](#change-57d985c44bc4a8846cafda5cde966ab5)

-   **[mssql]**“has\_window\_funcs”标志被删除。LIMIT /
    OFFSET 用法将一直使用 ROW NUMBER，如果在较早版本的 SQL
    Server 上，则操作失败。行为是完全一样的，除了错误是由 SQL 服务器而不是方言引发的，并且不需要标志设置来启用它。[¶](#change-870c7f02908eaf9dd76a606a56561da7)

-   **[mssql]**“auto\_identity\_insert”标志被删除。当 INSERT 语句覆盖已知有序列的列时，此功能始终生效。与“has\_window\_funcs”一样，如果底层驱动程序不支持这种情况，那么在任何情况下都不能执行此操作，所以没有标志是没有意义的。[¶](#change-83e8899feb9e875a26f54ec93b6d891e)

-   **[mssql]**使用新的 dialect.initialize()功能设置版本依赖的行为。[¶](#change-ce8ff886d9ea060a749895bb38ba108c)

-   **[mssql]**删除了不再使用的序列的引用。mssql 中的隐式标识与任何其他方言中的隐式序列的工作方式相同。显式序列通过使用“default
    =
    Sequence()”来启用。有关更多信息，请参阅 MSSQL 方言文档。[¶](#change-23bb79f6af16be836727eca4716407b3)

### 预言[¶ T0\>](#change-0.6beta1-oracle "Permalink to this headline")

-   **[oracle]**单元测试通过 cx\_oracle
    100％！[¶](#change-113b8b0993a9fa2dc0b7edd4704fbb42)

-   **[oracle]**支持 cx\_Oracle 的“native
    unicode”模式，它不需要设置 NLS\_LANG。使用 cx\_oracle 的最新 5.0.2 或更高版本。[¶](#change-ab3ce587a20ea73535ae07213b287bd2)

-   **[oracle]**将一个 NCLOB 类型添加到基类型中。[¶](#change-b2948a9f95dde029f129261698424123)

-   **[oracle]** use\_ansi = False 不会泄露到从也使用 JOIN /
    OUTERJOIN 的子查询中选择的语句的 FROM /
    WHERE 子句中。[¶](#change-7ca8af81feacfd6b9f2ce42f5828e1a4)

-   **[oracle]**为方言添加了本地 INTERVAL 类型。由于在 YEAR TO
    MONTH 中缺少对 cx\_oracle 的支持，目前只支持 DAY TO
    SECOND 间隔类型。[¶](#change-393f3fb1ddbce4735e553646ae6233f1)

    参考文献：[＃1467](http://www.sqlalchemy.org/trac/ticket/1467)

-   **[oracle]**usage of the CHAR type results in cx\_oracle’s
    FIXED\_CHAR dbapi type being bound to
    statements.[¶](#change-0991def0de5a17cae52ca7d4d7bc71fe)

-   **[oracle]**the Oracle dialect now features NUMBER which intends to
    act justlike Oracle’s NUMBER type.
    它是表反射返回的主要数值类型，并尝试根据精度/比例参数返回 Decimal()/
    float / int。[¶](#change-17dc85d30f2488fe7b6895a6e18faf2d)

    参考文献：[＃885](http://www.sqlalchemy.org/trac/ticket/885)

-   **[oracle]** func.char\_length 是 LENGTH
    [的一个通用函数](#change-96d06864792feffb4a6a52695b5756ef)

-   **[oracle]**ForeignKey() which includes onupdate= will emit a
    warning, not emit ON UPDATE CASCADE which is unsupported by
    oracle[¶](#change-8736cc2e4e76ced8e037e0353686bc90)

-   RowProxy()的 keys()方法现在返回结果列名称*normalized*，使其成为 SQLAlchemy 不区分大小写的名称。**[oracle]**这意味着对于不区分大小写的名称，它们将是小写字母，而 DBAPI 通常将它们作为大写名称返回。这允许行键()与进一步的 SQLAlchemy 操作兼容。[¶](#change-f427ca1185fb9a016f0a48f421816d0d)

-   **[oracle]**使用新的 dialect.initialize()功能设置版本相关的行为。[¶](#change-ce8ff886d9ea060a749895bb38ba108c)

-   **[oracle]**using types.BigInteger with Oracle will generate
    NUMBER(19)[¶](#change-695adf4c5253eb83c2d4d5bd3288f373)

    参考文献：[＃1125](http://www.sqlalchemy.org/trac/ticket/1125)

-   **[oracle]**“区分大小写”功能将在反映过程中检测到全小写区分大小写的列名称，并将“quote
    = True”添加到生成的列中，以保持正确的引用。[¶
    T2\>](#change-10e463fe98ba913938ae4afeb008d31f)

### 火鸟[¶ T0\>](#change-0.6beta1-firebird "Permalink to this headline")

-   RowProxy()的 keys()方法现在返回结果列名称*标准化*，使其成为 SQLAlchemy 不区分大小写的名称。**[firebird]**这意味着对于不区分大小写的名称，它们将是小写字母，而 DBAPI 通常将它们作为大写名称返回。这允许行键()与进一步的 SQLAlchemy 操作兼容。[¶](#change-f427ca1185fb9a016f0a48f421816d0d)

-   **[firebird]**使用新的 dialect.initialize()功能设置版本相关的行为。[¶](#change-ce8ff886d9ea060a749895bb38ba108c)

-   **[firebird]**“区分大小写”功能将在反映过程中检测全小写区分大小写的列名称，并将“quote
    = True”添加到生成的列中，以便保持正确的引用。[¶
    T2\>](#change-10e463fe98ba913938ae4afeb008d31f)

### 杂项[¶ T0\>](#change-0.6beta1-misc "Permalink to this headline")

-   **[release]
    [major]**有关整套功能描述，请参阅[http://docs.sqlalchemy.org/en/latest/changelog\_migration\_06.html](http://docs.sqlalchemy.org/en/latest/changelog_migration_06.html)。这份文件是一项正在进行中的工作。[¶](#change-c9d5768f02fc70a1c4200ea76ae3d312)

-   **[release] [major]**
    0.6 版本中包含的所有 bug 修复和功能增强都来自最新的 0.5 版本及以下版本。[¶](#change-dca0b8a1f7cb8e1b45d9da364f11087f)

-   **[release] [major]**目前定位的平台包括 Python 2.4 / 2.5 /
    2.6，Python 3.1，Jython2.5.
    [¶](#change-7001ff18ae62ae8b4d16f9e25afcedbc)

-   **[engines]**transaction isolation level may be specified with
    create\_engine(... isolation\_level=”...”); available on postgresql
    and sqlite.[¶](#change-58e8499ff9cfdf3231dcf8c076a480fb)

    参考文献：[＃443](http://www.sqlalchemy.org/trac/ticket/443)

-   **[engines]**连接有 execution\_options()，这是生成方法，它接受影响语句执行的关键字 w.r.t.DBAPI。当前支持“stream\_results”，导致 psycopg2 为该语句使用服务器端游标，以及“autocommit”，它是 select()和 text()中“autocommit”选项的新位置。select()和 text()也有.execution\_options()以及 ORM
    Query()。[¶](#change-ff2e47b0d631ce1a4cf0a598c8f24df2)

-   **[engines]**修复了入口点驱动方言的导入，不依靠愚蠢的 tb\_info 技巧来确定导入错误状态[¶](#change-e139a9a5cd97f4d218b570024523f623)

    参考文献：[＃1630](http://www.sqlalchemy.org/trac/ticket/1630)

-   **[engines]**将 first()方法添加到 ResultProxy，返回第一行并立即关闭结果集。[¶](#change-90c8f734ee1abef927dbda0035beb0a0)

-   **[engines]**RowProxy objects are now pickleable, i.e. the object
    returned by result.fetchone(), result.fetchall()
    etc.[¶](#change-9dbc573a39f6fcf29d1f3dd9858ce826)

-   **[engines]**RowProxy no longer has a close() method, as the row no
    longer maintains a reference to the parent.
    改为在父代 ResultProxy 上调用 close()，或使用 autoclose。[¶](#change-558e9b15b66e5afa84cb889e23f27300)

-   **[engines]**ResultProxy internals have been overhauled to greatly
    reduce method call counts when fetching columns.
    在获取较大的结果集时可以提供很大的速度提升（高达 100％以上）。当提取没有应用类型级别处理的列和将结果用作元组（而不是字典）时，这种改进会更大。非常感谢 Elixir 的 Gaëtande
    Menten 对这个戏剧性的改进！[¶](#change-ec1f0e67ce08a7a3f706dce2d3fbfae6)

    参考文献：[＃1586](http://www.sqlalchemy.org/trac/ticket/1586)

-   **[engines]**当存在一个组合主键时，依赖后缀“最后插入的 id”获取生成的序列值（即 MySQL，MS-SQL）的数据库现在可以正常工作，其中“自动增量“列不是表中的第一个主键列。[¶](#change-647fd2ee66339752a6882b790cad9b87)

-   **[engines]**
    last\_inserted\_ids()方法已被重命名为描述符“inserted\_primary\_key”。[¶](#change-ab905cc7be5146eb11d1c1de8bd07df9)

-   **[engines]**setting echo=False on create\_engine() now sets the
    loglevel to WARN instead of NOTSET.
    这样即使日志记录为“sqlalchemy.engine”，也可以禁用特定引擎的日志记录。请注意，“echo”的默认设置是 None。[¶](#change-2687369260aafbe26535c7f07241f7df)

    参考文献：[＃1554](http://www.sqlalchemy.org/trac/ticket/1554)

-   **[engines]**ConnectionProxy now has wrapper methods for all
    transaction lifecycle events, including begin(), rollback(),
    commit() begin\_nested(), begin\_prepared(), prepare(),
    release\_savepoint(),
    etc.[¶](#change-17f0cb7bf2b9ebfb365311e17d0bd7f4)

-   **[engines]**连接池日志记录现在使用 INFO 和 DEBUG 日志级别进行日志记录。INFO 用于主要事件，例如无效连接，所有获取/返回日志记录的 DEBUG。echo\_pool 可以像 echo 一样使用 False，None，True 或“debug”。[¶](#change-1fe7fc3f57be368cd7f20fa804fa9056)

-   **[engines]**所有 pyodbc 方言现在支持额外的 pyodbc 特定 kw 参数'ansi'，'unicode\_results'，'autocommit'。[¶](#change-76cd53cd2b1cfd0a85a475a50a5f2ea3)

    参考文献：[＃1621](http://www.sqlalchemy.org/trac/ticket/1621)

-   **[engines]**“threadlocal”引擎已被重写和简化，现在支持 SAVEPOINT 操作。[¶](#change-9b7a4ecd72a4dc2579674f3e678873ff)

-   **[engines]**

    已弃用或删除
    :   -   result.last\_inserted\_ids()已弃用。使用 result.inserted\_primary\_key
        -   dialect.get\_default\_schema\_name（连接）现在通过 dialect.default\_schema\_name 公开。
        -   来自 engine.transaction()和 engine.run\_callable()的“连接”参数被删除
            -
            连接本身现在有这些方法。所有四种方法都接受传递给给定可调用的\*
            args 和\*\* kwargs，以及操作连接。

    [¶](#change-1adc08ecf95db03925768081293804a4)

-   **[reflection/inspection]**Table reflection has been expanded and
    generalized into a new API called
    “sqlalchemy.engine.reflection.Inspector”.
    Inspector 对象提供有关各种模式信息的细粒度信息，并具有扩展空间，包括表名，列名，视图定义，序列，索引等。[¶](#change-fe9d3b373816dc2ba59fe43fa591d219)

-   **[reflection/inspection]**视图现在可以反映为普通表格对象。使用相同的表构造函数，但要注意“有效的”主键和外键约束不是反射结果的一部分；如果需要，必须明确指定它们。[¶](#change-66a10b68814b0d202a3f73d3abaad4c7)

-   **[reflection/inspection]**The existing autoload=True system now
    uses Inspector underneath so that each dialect need only return
    “raw” data about tables and other objects - Inspector is the single
    place that information is compiled into Table objects so that
    consistency is at a
    maximum.[¶](#change-7d9c40c47ab45cde78a91ac3f513b242)

-   **[ddl]**the DDL system has been greatly expanded.
    DDL()类现在扩展了更通用的 DDLElement()，它构成了许多新构造的基础：

    > > -   CREATETABLE()
    > > -   DROPTABLE()
    > > -   AddConstraint()
    > > -   DropConstraint()
    > > -   的 CreateIndex()
    > > -   DropIndex()
    > > -   CreateSequence()
    > > -   DropSequence()
    >
    > 像普通的 DDL()一样，这些支持“on”和“execute-at()”。可以使用 sqlalchemy.ext.compiler 扩展名创建用户定义的 DDLElement 子类并将其链接到编译器。

    [¶](#change-a6a9a63e0053aafa663dea40ade905f0)

-   **[ddl]**传递给 DDL()和 DDLElement()的“on”可调用的签名被修改如下：

    > DDL
    > :   DDLElement 对象本身
    > 事件
    > :   字符串事件名称。
    > 目标
    > :   之前的“schema\_item”，触发事件的 Table 或 MetaData 对象。
    > 连接
    > :   用于该操作的 Connection 对象。
    > \*\*千瓦
    > :   关键字参数。对于创建/删除之前/之后的元数据，CREATE / DROP
    >     DDL 要发布的表对象列表作为 kw 参数“tables”传递。对于依赖于特定表的存在的元数据级 DDL 来说，这是必需的。

    DDL 的“schema\_item”属性已重命名为
    :   “目标”。

    [¶](#change-5db087b2333b39be3609cd5ea92c38fe)

-   **[dialect] [refactor]**Dialect modules are now broken into database
    dialects plus DBAPI implementations. 连接 URL 现在最好使用 dialect +
    driver：// ...指定，即“mysql + mysqldb：// scott：tiger @ localhost
    /
    test”。有关示例，请参阅 0.6 文档。[¶](#change-309ea6a05094c41ff3447b7aeb64cd22)

-   **[dialect]
    [refactor]**外部方言的 setuptools 入口点现在称为“sqlalchemy.dialects”。[¶](#change-c50c8d68a80a22e1cace4b16d0b405e1)

-   **[dialect] [refactor]**the “owner” keyword argument is removed from
    Table.
    使用“模式”来表示任何名称空间要预先添加到表名中。[¶](#change-4dda1aa78046eb29914b005241fb0eb6)

-   **[dialect] [refactor]**
    server\_version\_info 成为一个静态属性[¶](#change-20dfe96a61f245f370f47bd3d9e28791)

-   **[dialect] [refactor]**dialects receive an initialize() event on
    initial connection to determine connection
    properties.[¶](#change-d886ab16ae25f489620c28fd52a6a00a)

-   **[dialect] [refactor]**dialects receive a visit\_pool event have an
    opportunity to establish pool
    listeners.[¶](#change-4861423f4ff36544dc83545d48d8523d)

-   **[dialect]
    [refactor]**缓存的 TypeEngine 类是缓存的每个方言类而不是每个方言。[¶](#change-77a8bc1484dc353cc24fd4772244f757)

-   **[dialect]
    [refactor]**新的 UserDefinedType 应该被用作新类型的基类，它保留了 get\_col\_spec()的 0.5 行为。[¶](#change-4ad2b7d81680c7f34705e3613b7e36fb)

-   **[dialect]
    [refactor]**现在所有类型的 result\_processor()方法接受第二个参数“coltype”，它是 cursor.description 中的 DBAPI 类型参数。这个参数可以帮助某些类型决定最有效的结果值处理。[¶](#change-461c903cb377ff8681ec08be16613ab4)

-   **[dialect]
    [refactor]**已弃用 Dialect.get\_params()已移除[¶](#change-99c23fa8c33e3f526d98bf39d26e3f0f)

-   **[dialect] [refactor]**Dialect.get\_rowcount() has been renamed to
    a descriptor “rowcount”, and calls cursor.rowcount directly.
    需要为某些调用硬连线的方言应覆盖提供不同行为的方法。[¶](#change-6ada9c457b2d323fc3c2bd369bf4e07b)

-   **[dialect] [refactor]**
    DefaultRunner 和子类已被删除。这个对象的工作已经简化并移入 ExecutionContext。支持序列的方言应该在其执行上下文实现中添加一个 fire\_sequence()方法。[¶](#change-c02c74322d7c1ece9af8ad1704c033e1)

    参考文献：[＃1566](http://www.sqlalchemy.org/trac/ticket/1566)

-   **[dialect]
    [refactor]**编译器生成的函数和运算符现在使用形式为“visit\_
    ”和“visit\_ \_fn”的（几乎）常规调度函数来提供定制的处理。 T3\>
    T2\>这代替了在编译器子类中使用直接的访问方法复制“函数”和“操作符”字典的需要，并且还允许编译器子类完全控制渲染，因为完整的\_Function 或\_BinaryExpression 对象被传入。[T0\>](#change-e3eaf58468be38fd781277edac3a7140)

-   **[types]**方言内类型的构造已经彻底改变。方言现在将公开可用的类型定义为大写名称，而内部实现类型使用下划线标识符（即私有）。用 SQL 和 DDL 表示类型的系统已被移至编译器系统。这具有大部分方言中的类型对象少得多的效果。关于这种方言作者的体系结构的详细文档在 lib
    / sqlalchemy /
    dialects\_type\_migration\_guidelines.txt 中。[¶](#change-3bbeb8422b9fa129668159a5fbbccd13)

-   **[types]**类型不再对默认参数进行猜测。特别是 Numeric，Float，NUMERIC，FLOAT，DECIMAL 除非指定，否则不会生成任何长度或比例。[¶](#change-a1738683c3d87b598a5a039c7faed0e0)

-   二进制文件被重命名为 types.LargeBinary，它只产生 BLOB，BYTEA 或类似的“长二进制”类型。**[types]**添加了新的基本 BINARY 和 VARBINARY 类型，以不可知的方式访问这些 MySQL
    / MS-SQL 特定类型。[¶](#change-0e50f446360f471e031c78a9fef201a3)

    参考文献：[＃1664](http://www.sqlalchemy.org/trac/ticket/1664)

-   **[types]**String/Text/Unicode types now skip the unicode() check on
    each result column value if the dialect has detected the DBAPI as
    returning Python unicode objects natively.
    此检查是在第一次连接时使用“SELECT CAST”某些文本“AS
    VARCHAR（10）”或等价物发出的，然后检查返回的对象是否为 Python
    unicode。这使得 native-unicode DBAPI 具有巨大的性能提升，包括 pysqlite
    / sqlite3，psycopg2 和 pg8000.
    [¶](#change-236aba55b2dc30a153e666c8d4fc745f)

-   **[types]**大多数类型的结果处理器已经过检查，可能会提高速度。具体而言，以下通用类型已进行了优化，从而改进了速度：Unicode，PickleType，Interval，TypeDecorator，Binary。此外，以下特定于 dbapi 的实现已得到改进：Sqlite 上的 Time，Date 和 DateTime，Postgresql 上的 ARRAY，MySQL 上的 Time，MySQL 上的 Numeric（as\_decimal
    =
    False），MySQL 上的 python 和 pypostgresql，cx\_oracle 上的 DateTime 以及 cx\_oracle 上的基于 LOB 的类型[¶
    T0\>](#change-48d0f246a76fcd18e2d43a473beab4ba)

-   **[types]**Reflection of types now returns the exact UPPERCASE type
    within types.py, or the UPPERCASE type within the dialect itself if
    the type is not a standard SQL type.
    这意味着现在反射会返回有关反射类型的更准确的信息。[¶](#change-9d4508b066c6e6fd68af58a2488b24a6)

-   **[types]**添加了一个新的 Enum 泛型类型。Enum 是一个模式感知对象，用于支持需要特定 DDL 才能使用枚举或等效数据库的数据库；在 PG 的情况下，它处理 CREATE
    TYPE 的细节，并且在没有本地枚举支持的其他数据库上，将通过生成 VARCHAR
    +内联 CHECK 约束来强制执行枚举。[](#change-7ac9dceee42e42dc8a5c9472df0e1d2a)

    参考文献：[＃1511](http://www.sqlalchemy.org/trac/ticket/1511)，[＃1109](http://www.sqlalchemy.org/trac/ticket/1109)

-   **[types]**
    Interval 类型包含一个“native”标志，用于控制是否选择本地 INTERVAL 类型（postgresql
    +
    oracle）（如果可用）。还添加了“day\_precision”和“second\_precision”参数，它们适当地传播到这些本机类型。与。[¶](#change-ab51cd0f5146920fb998f5c5a93cabdd)相关

    参考文献：[＃1467](http://www.sqlalchemy.org/trac/ticket/1467)

-   **[types]**布尔类型在不支持本机布尔支持的后端上使用时，将生成 CHECK 约束“col
    IN（0，1）”以及基于 int /
    smallint 的列类型。如果需要，可以使用 create\_constraint =
    False 关闭此功能。请注意，MySQL 没有本地布尔型*或*
    CHECK 约束支持，所以此功能在该平台上不可用。[¶](#change-26f9fec07b187541c0098597a7197ff8)

    参考文献：[＃1589](http://www.sqlalchemy.org/trac/ticket/1589)

-   **[types]**当 mutable =
    True 时，PickleType 现在使用==来比较值，除非带有比较函数的“comparator”参数指定为类型。如果没有覆盖\_\_eq
    \_\_()或者没有提供比较函数，那么被腌制的对象将根据标识进行比较（这违背了 mutable
    = True 的目的）。[¶](#change-bbd25c78a1c3340579717367777509bc)

-   **[types]**
    Numeric 和 Float 的默认“precision”和“scale”参数已被删除，现在默认为 None。除非提供这些值，否则默认情况下，NUMERIC 和 FLOAT 将默认呈现为不带数字参数。[¶](#change-23a61cc6adace380c1a9e342d1174c32)

-   **[types]** AbstractType.get\_search\_list()被移除 -
    用于的游戏不再需要。[¶](#change-d18a18e76aea7383243090429523e54c)

-   **[types]**添加了一个通用的 BigInteger 类型，编译为 BIGINT 或 NUMBER（19）。[¶](#change-d76a27861917c6bf030a837acf9ce8fe)

    参考文献：[＃1125](http://www.sqlalchemy.org/trac/ticket/1125)

-   **[types]**使用 autocommit = False，autoflush =
    True，sqlsoup 已被彻底修改为显式支持 0.5 样式会话。SQLSoup 的默认行为现在需要通常使用已添加到其接口的 commit()和 rollback()。explcit
    Session 或 scoped\_session 可以传递给构造函数，从而允许重写这些参数。[¶](#change-05b2ce683e77d35a420cda187f7222ab)

-   **[types]** sqlsoup
    db。.update()和 delete()现在分别调用 query（cls）.update()和 delete()。[¶](#change-55a1682d2cbda5fbf6dd2d58744f5dbe)
    \< / T2\>

-   **[types]**sqlsoup now has execute() and connection(), which call
    upon the Session methods of those names, ensuring that the bind is
    in terms of the SqlSoup object’s
    bind.[¶](#change-a22079daeb20e98393c35a74d11c0259)

-   **[types]**sqlsoup objects no longer have the ‘query’ attribute -
    it’s not needed for sqlsoup’s usage paradigm and it gets in the way
    of a column that is actually named
    ‘query’.[¶](#change-99c1ecd3203ef2d370b542d1b605ca61)

-   **[types]**传递给 association\_proxy 的 proxy\_factory
    callable 的签名现在是（lazy\_collection，creator，value\_attr，association\_proxy），并添加第四个参数，即父 AssociationProxy 参数。允许内置集合的可序列化和子类化。[¶](#change-351b0756ad5ba1266508d1dea1de559e)

    参考文献：[＃1259](http://www.sqlalchemy.org/trac/ticket/1259)

-   **[types]**感谢 Scott
    Torborg，association\_proxy 现在具有基本的比较器方法.any()，.has()，.contains()，==，！=。[¶](#change-c0b751885f79648b1e07bd4f1d5aa0c8)

    参考文献：[＃1372](http://www.sqlalchemy.org/trac/ticket/1372)


