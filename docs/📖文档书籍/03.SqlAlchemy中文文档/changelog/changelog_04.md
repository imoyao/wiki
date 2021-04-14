---
title: changelog_04
date: 2021-02-20 22:41:28
permalink: /sqlalchemy/5e9f56/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
0.4 更新日志[¶](#changelog "Permalink to this headline")
=======================================================

0.4.8 [¶ T0\>](#change-0.4.8 "Permalink to this headline")
----------------------------------------------------------

发布日期：2008 年 10 月 12 日

### ORM [¶ T0\>](#change-0.4.8-orm "Permalink to this headline")

-   **[orm]**Fixed bug regarding inherit\_condition passed with “A=B”
    versus “B=A” leading to
    errors[¶](#change-4000d9f2d4389a85854ede3e007aaba5)

    参考文献：[＃1039](http://www.sqlalchemy.org/trac/ticket/1039)

-   **[orm]**在 SessionExtension.before\_flush()中对新的，脏的和删除的集合所做的更改将对该刷新生效。[¶](#change-2690aa1e520f493331cb61a6326c56c4)

-   **[orm]**Added label() method to InstrumentedAttribute to establish
    forwards compatibility with
    0.5.[¶](#change-13623d94e18e8b3b92030ae525a030ec)

### SQL [¶ T0\>](#change-0.4.8-sql "Permalink to this headline")

-   **[sql]**column.in\_(someselect) can now be used as a columns-clause
    expression without the subquery bleeding into the FROM
    clause[¶](#change-7fee195a017ac2215e80b38b868365e9)

    参考文献：[＃1074](http://www.sqlalchemy.org/trac/ticket/1074)

### MySQL 的[¶ T0\>](#change-0.4.8-mysql "Permalink to this headline")

-   **[mysql]**新增 MSMediumInteger 类型[¶](#change-341091ae1d33ebc9cf02df1ca798516a)

    参考文献：[＃1146](http://www.sqlalchemy.org/trac/ticket/1146)

### 源码[¶ T0\>](#change-0.4.8-sqlite "Permalink to this headline")

-   **[sqlite]**提供了一个自定义的 strftime()函数，它处理 1900 年以前的日期。[¶](#change-67cbed9a85982025c41cb138787f8f47)

    参考文献：[＃968](http://www.sqlalchemy.org/trac/ticket/968)

-   **[sqlite]**字符串（和 Unicode 的，UnicodeText 的等）在 sqlite 方言中禁用 convert\_unicode 逻辑，以调整 pysqlite
    2.5.0 的新要求，即只接受 Python unicode 对象；
    [http://itsystementwicklung.de/pipermail/list-pysqlite/2008-March/000018.html
    T0\>](http://itsystementwicklung.de/pipermail/list-pysqlite/2008-March/000018.html)[¶
    T1\>](#change-7cabaeb41bcd3c0b9074d2704bca61c6)

### 预言[¶ T0\>](#change-0.4.8-oracle "Permalink to this headline")

-   **[oracle]**
    has\_sequence()现在将模式名称考虑在内[¶](#change-c1ece36939d26084e64ecd6b3519de17)

    参考文献：[＃1155](http://www.sqlalchemy.org/trac/ticket/1155)

-   **[oracle]**将 BFILE 添加到反射类型列表[¶](#change-e15a9ca2c0e8d6a5e56b4fc468592e10)

    参考文献：[＃1121](http://www.sqlalchemy.org/trac/ticket/1121)

0.4.7p1 [¶ T0\>](#change-0.4.7p1 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2008 年 7 月 31 日

### ORM [¶ T0\>](#change-0.4.7p1-orm "Permalink to this headline")

-   **[orm]**在 scoped\_session 方法中添加了“add()”和“add\_all()”。0.4.7 的解决方法：
```python
        from sqlalchemy.orm.scoping import ScopedSession, instrument
        setattr(ScopedSession, "add", instrument("add"))
        setattr(ScopedSession, "add_all", instrument("add_all"))
```

-   **[orm]**修正了 relation()中 set()和 generator 表达式的非 2.3 兼容用法。[¶](#change-8150f6bc3321b0e5940f462af85fea59)

0.4.7 [¶ T0\>](#change-0.4.7 "Permalink to this headline")
----------------------------------------------------------

发布日期：2008 年 7 月 26 日星期六

### ORM [¶ T0\>](#change-0.4.7-orm "Permalink to this headline")

-   **[orm]**The contains() operator when used with many-to-many will
    alias() the secondary (association) table so that multiple
    contains() calls will not conflict with each
    other[¶](#change-96d6f0048a53ef8280afa881d15981e4)

    参考文献：[＃1058](http://www.sqlalchemy.org/trac/ticket/1058)

-   **[orm]**fixed bug preventing merge() from functioning in
    conjunction with a
    comparable\_property()[¶](#change-043f1fb5d04c32f0e61d5443a46b23e6)

-   **[orm]**the enable\_typechecks=False setting on relation() now only
    allows subtypes with inheriting mappers.
    完全不相关的类型或未针对目标映射器设置映射器继承的子类型仍然是不允许的。[¶](#change-2c1a9b40953961921023dfe557a4326c)

-   **[orm]**为会话添加了 is\_active 标志以检测事务何时正在进行。这个标志总是与真正的“事务性”（0.5 在一个非“autocommit”）会话。[¶](#change-25f41185c603cbb10bde56a17f623433)

    参考文献：[＃976](http://www.sqlalchemy.org/trac/ticket/976)

### SQL [¶ T0\>](#change-0.4.7-sql "Permalink to this headline")

-   **[sql]**Fixed bug when calling select([literal(‘foo’)]) or
    select([bindparam(‘foo’)]).[¶](#change-01ca8336bd39c6bb69577aad5d1d730e)

### 架构[¶ T0\>](#change-0.4.7-schema "Permalink to this headline")

-   **[schema]**create\_all(), drop\_all(), create(), drop() all raise
    an error if the table name or schema name contains more characters
    than that dialect’s configured character limit.
    某些数据库可以在使用过程中处理太长的表名，SQLA 也可以处理这些。但是，由于我们正在数据库的目录表中查找名称，因此各种反射/
    checkfirst-during-create 方案失败。[¶](#change-738cf5e3972ba6f7723c2c7acf6decc9)

    参考文献：[＃571](http://www.sqlalchemy.org/trac/ticket/571)

-   **[schema]**当您在列上表示“index =
    True”时生成的索引名称被截断为适合该方言的长度。另外，名称太长的索引不能通过 Index.drop()显式删除，类似于。[¶](#change-d85ff361d06db88fdb94e3932a143ad0)

    参考文献：[＃571](http://www.sqlalchemy.org/trac/ticket/571)，[＃820](http://www.sqlalchemy.org/trac/ticket/820)

### MySQL 的[¶ T0\>](#change-0.4.7-mysql "Permalink to this headline")

-   **[mysql]**将'CALL'添加到返回结果行的 SQL 关键字列表中。[¶](#change-0514aaebdc79f7f9ff25dca47dc4b225)

### 预言[¶ T0\>](#change-0.4.7-oracle "Permalink to this headline")

-   **[oracle]** Oracle
    get\_default\_schema\_name()在返回之前“标准化”名称，这意味着当标识符被检测为不区分大小写时，它返回一个小写名称[¶](#change-aca4b41d0da66d4a3bd0e82c3a84cf5a)

-   **[oracle]**在创建/删除表时，在搜索现有表时要考虑模式名，以便其他所有者名称空间中具有相同名称的表不会发生冲突[¶](#change-b47186d61937faba11d31de8eb03a326)

    参考文献：[＃709](http://www.sqlalchemy.org/trac/ticket/709)

-   **[oracle]**Cursors now have “arraysize” set to 50 by default on
    them, the value of which is configurable using the “arraysize”
    argument to create\_engine() with the Oracle dialect.
    这将考虑到 cx\_oracle 的默认设置为“1”，这会导致很多往返行程被发送到 Oracle。这实际上与 BLOB
    /
    CLOB 绑定游标一起运行良好，其中有任何可用的数字，但仅限于该行请求的生命周期（因此 BufferedColumnRow 仍然需要，但更少）。[¶](#change-7568973ef20ea5f8c81322c145b9057f)

    参考文献：[＃1062](http://www.sqlalchemy.org/trac/ticket/1062)

-   **[oracle]**

    源码
    :   -   添加 SLFloat 类型，该类型与 SQLite
            REAL 类型关联相匹配。以前，只提供 SLNumeric 来满足 NUMERIC 的亲和力，但这与 REAL 不一样。

    [¶](#change-f9736a0cc3c4e162b300a782b7eca3f9)

### 杂项[¶ T0\>](#change-0.4.7-misc "Permalink to this headline")

-   **[postgres]**修复了 server\_side\_cursors 以正确检测 text()子句。[¶](#change-62dc8bb9ccdb89ab5046417cb1d71934)

-   **[postgres]**添加了 PGCidr 类型[¶](#change-1d3294865f665d0cd4ea5f969d56a278)

    参考文献：[＃1092](http://www.sqlalchemy.org/trac/ticket/1092)

0.4.6 [¶ T0\>](#change-0.4.6 "Permalink to this headline")
----------------------------------------------------------

发布时间：2008 年 5 月 10 日星期六

### ORM [¶ T0\>](#change-0.4.6-orm "Permalink to this headline")

-   **[orm]**解决了最近的关系()重构问题，它修复了多次连接本地表和远程表的异域查看关系，并在连接之间共享一个公共列。[¶](#change-e31fe2fb2fc3ae1652c5eec0dfa0d711)

-   **[orm]**还重新建立了连接多个表的 viewonly 关系()配置。[¶](#change-f75f03e2d2f84749c5a66468e9f1a35f)

-   **[orm]**Added experimental relation() flag to help with
    primaryjoins across functions, etc.,
    \_local\_remote\_pairs=[tuples].
    这补充了一个复杂的 primaryjoin 条件，允许您提供组成关系的本地和远程端的各个列对。还改进了懒加载 SQL 生成以处理在函数和其他表达式中放置绑定参数。（部分进展）[¶](#change-8eaf754f74a237ae2563356bab985463)

    参考文献：[＃610](http://www.sqlalchemy.org/trac/ticket/610)

-   **[orm]**修复了单个表继承，这样你就可以从一个连接表中继承一个没有问题的映射器。[¶](#change-cc35ebaf57ac910c9fbb17727e48eac6)

    参考文献：[＃1036](http://www.sqlalchemy.org/trac/ticket/1036)

-   **[orm]**修正了发生在 Query.order\_by()if 子句自适应发生时的“串联元组”bug。[¶](#change-0ff3c2bd9a30aeb035bd70efcc0b5bb4)

    参考文献：[＃1027](http://www.sqlalchemy.org/trac/ticket/1027)

-   **[orm]**删除了映射选择器需要“别名”的古老断言 -
    如果没有映射器存在，映射器现在会创建自己的别名。尽管在这种情况下，您需要使用类而不是映射的可选项作为列属性的来源
    - 因此仍然会发出警告。[¶](#change-9e5d19c9631cbe865600f279d1869f33)

-   **[orm]**fixes to the “exists” function involving inheritance
    (any(), has(), \~contains()); the full target join will be rendered
    into the EXISTS clause for relations that link to
    subclasses.[¶](#change-dde11f9e942ea94174168e9c076316e5)

-   **[orm]**在主查询行中恢复了对 append\_result()扩展方法的使用，当扩展存在时并且仅返回单个实体结果时[¶](#change-104376c27707b3a37374971243e2423c)

-   **[orm]**还重新建立了连接多个表的 viewonly 关系()配置。[¶](#change-302298aee07ec1d1aac10fe144468a7a)

-   **[orm]**removed ancient assertion that mapped selectables require
    “alias names” - the mapper creates its own alias now if none is
    present.
    尽管在这种情况下，您需要使用类而不是映射的可选项作为列属性的来源 -
    因此仍然会发出警告。[¶](#change-6f570f7ef26a5a9b11b822a63353d962)

-   **[orm]**refined mapper.\_save\_obj() which was unnecessarily
    calling \_\_ne\_\_() on scalar values during
    flush[¶](#change-c3ba9d4b644bae5e507a69b17fad45b3)

    参考文献：[＃1015](http://www.sqlalchemy.org/trac/ticket/1015)

-   **[orm]**added a feature to eager loading whereby subqueries set as
    column\_property() with explicit label names (which is not
    necessary, btw) will have the label anonymized when the instance is
    part of the eager join, to prevent conflicts with a subquery or
    column of the same name on the parent
    object.[¶](#change-71081f223b7ec2f83fe88a95bb74c96b)

    参考文献：[＃1019](http://www.sqlalchemy.org/trac/ticket/1019)

-   **[orm]**set-based collections |=, -=, \^= and &= are stricter about
    their operands and only operate on sets, frozensets or subclasses of
    the collection type.
    以前，他们会接受任何 duck-typed 集合。[¶](#change-1e0e2c1b7d8337b2961576a28f6152dd)

-   **[orm]**添加了一个 dynamic\_dict /
    dynamic\_dict.py 示例，说明了如何将一个简单的方法放置在 dynamic\_loader 之上。[¶](#change-b1518ae6a45f510afd237e22960d4dbc)

### SQL [¶ T0\>](#change-0.4.6-sql "Permalink to this headline")

-   **[sql]**通过.collat​​e（）表达式运算符和 collat​​e（，）sql 函数添加 COLLATE 支持。[¶](#change-c0a253c2a3ac8a52b71f9074c836045e)
    T3\> T2\>

-   **[sql]**Fixed bug with union() when applied to non-Table connected
    select statements[¶](#change-3425affd500ef60da0ceda4319ff76ac)

-   **[sql]**improved behavior of text() expressions when used as FROM
    clauses, such as
    select().select\_from(text(“sometext”))[¶](#change-c946f492d8c12da19c9976c66867241a)

    参考文献：[＃1014](http://www.sqlalchemy.org/trac/ticket/1014)

-   **[sql]**Column.copy() respects the value of “autoincrement”, fixes
    usage with Migrate[¶](#change-79b0f66b8b318392d68b1e09fb21dbad)

    参考文献：[＃1021](http://www.sqlalchemy.org/trac/ticket/1021)

### MSSQL [¶ T0\>](#change-0.4.6-mssql "Permalink to this headline")

-   **[mssql]**在引擎/
    dburi 参数中添加了“odbc\_autotranslate”参数。任何给定的字符串将被传递给 ODBC 连接字符串，如下所示：

    > “AutoTranslate =％s”％odbc\_autotranslate

    [¶](#change-4bf92261ee5df21cc151f29b57009c2d)

    参考文献：[＃1005](http://www.sqlalchemy.org/trac/ticket/1005)

-   **[mssql]**在引擎/
    dburi 参数中添加了“odbc\_options”参数。给定的字符串仅附加到 SQLAlchemy 生成的 odbc 连接字符串。

    这应该可以避免将来添加大量的 ODBC 选项。

    [¶](#change-c27df151a64a19d159ffaed249f8c5ec)

### 火鸟[¶ T0\>](#change-0.4.6-firebird "Permalink to this headline")

-   **[firebird]**处理“SUBSTRING（：string FROM：start
    FOR：length）”builtin。[¶](#change-3135f866ba259ae39feef5c8fd6e9dc8)

### 杂项[¶ T0\>](#change-0.4.6-misc "Permalink to this headline")

-   **[declarative]
    [extension]**联合表继承映射器使用稍微宽松的函数为父表创建“继承条件”，以便尚未声明 Table 对象的其他外键不会触发一个错误。[¶](#change-6e72bcfc5ea35d0926f998977a8d8f6b)

-   **[declarative] [extension]**fixed reentrant mapper compile hang
    when a declared attribute is used within ForeignKey, ie.
    ForeignKey 的（MyOtherClass.someattribute）[¶
    T0\>](#change-7cf86b76b69093e8eaf193d8766bd8ce)

-   **[engines]**现在，可以将池侦听器作为可调用的字典或（可能部分）鸭式 PoolListener 的字典提供，您可以选择。[¶](#change-bd1c9b334fbda8764b59adae68a98d7d)

-   **[engines]**将“rollback\_returned”选项添加到池，这将禁用连接返回时发出的回滚()。这个标志只适用于不支持事务的数据库（即 MySQL
    / MyISAM）。[¶](#change-1026db7afd8b57d4eb7e9698f6304feb)

-   **[ext]**基于集合的关联代理| =， - =，\^
    =和＆=对它们的操作数更严格，仅对集合，frozensets 或其他关联代理进行操作。以前，他们会接受任何 duck-typed 集合。[¶](#change-68c00352100f06ff96b4b08752086944)

0.4.5 [¶ T0\>](#change-0.4.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2008 年 4 月 4 日

### ORM [¶ T0\>](#change-0.4.5-orm "Permalink to this headline")

-   **[orm]**对 session.merge()行为的一个小改动 -
    根据主键属性检查现有对象，而不一定是\_instance\_key。所以广泛要求的能力，即：

    > x = MyObject（id = 1）x = sess.merge（x）

    实际上将加载数据库中 ID 为 1 的 MyObject（如果存在），现在可用。merge()仍将给定对象的状态复制到持久对象，因此类似上述的示例通常会将“x”的所有属性的“None”复制到持久副本上。这些可以使用 session.expire（x）来恢复。

    [¶](#change-2c9bdeacf621a1e5c68e65432e78acc9)

-   **[orm]**在 merge()中也有固定的行为，因此收集元素出现在目的地但不是合并的集合中没有被从目标中移除[¶](#change-ecb686988dd36c2668f8c1f13ab0b426)

-   **[orm]**为“未编译的映射器”添加了更积极的检查，特别有助于声明层[¶](#change-8c3e6ca94ae7018ad418fb8989b56c18)

    参考文献：[＃995](http://www.sqlalchemy.org/trac/ticket/995)

-   **[orm]**The methodology behind “primaryjoin”/”secondaryjoin” has
    been refactored.
    行为应该稍微更智能一些，主要是通过减少错误信息来提高可读性。在少数情况下，它可以比以前更好地解析正确的外键。[¶](#change-92147b4d8f5dc129bb6af919988b1578)

-   **[orm]**新增了 comparable\_property()，将查询 Comparator 行为添加到常规非托管 Python 属性中[¶](#change-e9af0076f84f16dc139143d25c2481c4)

-   **[orm] [‘machines’] [Company.employees.of\_type(Engineer)]**the
    functionality of query.with\_polymorphic() has been added to
    mapper() as a configuration option.

    它通过几种形式设置：
    ```python    
    :   with\_polymorphic ='\*'with\_polymorphic = [mappers]
        with\_polymorphic =（'\*'，可选）with\_polymorphic
        =（[mappers]，可选）
    ```
    这将控制继承的映射器的默认多态加载策略。如果没有给出 selectable，则为所有请求的连接表继承映射器创建外部连接。请注意，自动创建连接与具体的表继承不兼容。

    mapper()现有的 select\_table 标志现在已被弃用，并与 with\_polymorphic（'\*'，select\_table）同义。请注意，select\_table 的底层“内核”已被完全删除，并被更新，更灵活的方法所取代。

    新方法还会自动允许急切加载为子类（如果存在）工作，例如：
    ```python
    sess.query(Company).options(
        eagerload_all(
    ))
    ```
    加载公司对象，他们的员工以及碰巧是工程师的'机器'员工集合。应该尽快引入“with\_polymorphic”查询选项，这将允许每个查询控制 with\_polymorphic()关系。

-   **[orm]**added two “experimental” features to Query, “experimental”
    in that their specific name/behavior is not carved in stone just
    yet: \_values() and \_from\_self(). 我们希望对这些反馈意见。

    -   给\_values（\*列）一列列表达式，并返回一个新的查询，它只返回那些列。评估时，返回值是一个元组列表，就像使用 add\_column()或 add\_entity()时一样，唯一的区别是“实体零”即映射的类不包含在结果中。这意味着在查询中使用 group\_by()和 having()，这是最终有意义的，直到现在，Query 一直是无用的。

        对这种方法的未来改变可能包括它加入，过滤和允许与“结果集”无关的其他选项的能力被删除，所以我们正在寻找的反馈是人们如何使用\_values()...即，在最后，还是人们喜欢在被调用后继续生成。

    -   \_from\_self()编译查询的 SELECT 语句（减去任何渴望的加载器），并返回一个新的从该 SELECT 中选择的 Query。所以基本上你可以从查询中查询而不需要手动提取 SELECT 语句。这为查询[3：5]
        .\_
        from\_self()。filter（某些标准）等操作提供了意义。除了可以快速创建效率较低的高度嵌套查询之外，这里没有太多争议，我们希望对命名选择提供反馈。

    [¶](#change-8b57d2ed0d6bbe58c75f64223341c1c8)

-   **[orm]**query.order\_by() and query.group\_by() will accept
    multiple arguments using \*args (like select() already
    does).[¶](#change-2deb85fd835bde751f8cfd2461527a8e)

-   **[orm]**Added some convenience descriptors to Query:
    query.statement returns the full SELECT construct, query.whereclause
    returns just the WHERE part of the SELECT
    construct.[¶](#change-86eb8853972534a7dafcbff8b9986332)

-   **[orm]**Fixed/covered case when using a False/0 value as a
    polymorphic
    discriminator.[¶](#change-aa4cb730a2e43a1ad4e1443ec05973fe)

-   **[orm]**修正了阻止同义词()属性被用于继承的错误[¶](#change-02cba4fb2cbfa1275190cc9ed35f1d16)

-   **[orm]**修正后缀下划线的 SQL 函数截断[¶](#change-c58703687f6e5690fb29d5c65bec8f2e)

    参考文献：[＃996](http://www.sqlalchemy.org/trac/ticket/996)

-   **[orm]**当一个挂起的实例的属性到期时，当刷新动作被触发并且没有找到结果时，将不会引发错误。[¶](#change-4d790ba27407b3f2c5e5442e941ee625)

-   **[orm]**Session.execute can now find binds from
    metadata[¶](#change-ee82467594e923772bba0a03199886e6)

-   **[orm]**将“self-referential”的定义调整为任何具有公共父元素的两个映射器（这会影响与 Query 连接时是否需要 aliased
    = True）。[¶\< / T2\>](#change-79438d10e98c888cce0932f09a42a26f)

-   **[orm]**Made some fixes to the “from\_joinpoint” argument to
    query.join() so that if the previous join was aliased and this one
    isn’t, the join still happens
    successfully.[¶](#change-f896c87995fe90330fd02cbf21c852bf)

-   **[orm]**

    什锦“级联删除”修复：
    :   -   修复了动态关系的“级联删除”操作，该操作仅在 0.4.2 中针对外键清零行为实施，而不是实际的级联删除
        -   在父对象上调用 session.delete()之前，多对一删除没有删除孤立级联的级联不会删除与父级断开连接的孤儿（一对多已经有此）。
        -   使用 delete-orphan 删除级联将删除孤儿，而不管它是否仍然连接到其还被删除的父级。
        -   当使用继承时，在超类中存在的关系上正确检测到 delete-orphan
            casacde。

    [¶](#change-721ade134b0684d73d040e1d5c61feb9)

    参考文献：[＃895](http://www.sqlalchemy.org/trac/ticket/895)

-   **[orm]**Fixed order\_by calculation in Query to properly alias
    mapper-config’ed order\_by when using
    select\_from()[¶](#change-510cb165c89c094b6cc2b5db3787b360)

-   **[orm]**重构了将集合替换为另一个集合时使用的差异逻辑，存入 collections.bulk\_replace 中，对构建多级集合的任何人都有用。[¶](#change-94f2275e47afba73d8f37f7572917466)

-   **[orm]**级联遍历算法从递归转换为迭代以支持深对象图。[¶](#change-67d9d0b8806c805bf6baa1e8ed8dd735)

### SQL [¶ T0\>](#change-0.4.5-sql "Permalink to this headline")

-   **[sql]**schema-qualified tables now will place the schemaname ahead
    of the tablename in all column expressions as well as when
    generating column labels.
    这可以防止所有情况下的跨模式名称冲突[¶](#change-86518949b9a04cceb5d9eef390e32768)

    参考文献：[＃999](http://www.sqlalchemy.org/trac/ticket/999)

-   **[sql]**can now allow selects which correlate all FROM clauses and
    have no FROM themselves. 这些通常用于标量环境中，即 SELECT
    x，（SELECT x WHERE y）FROM
    table。需要显式的 correlate()调用。[¶](#change-3bb024dda072d0b61145352051204bfc)

-   **[sql]**‘name’ is no longer a required constructor argument for
    Column().
    它（和.key）现在可以推迟到列被添加到表中。[¶](#change-b98de44bd2b73a6b57d74988b3c71e30)

-   **[sql]**like(), ilike(), contains(), startswith(), endswith() take
    an optional keyword argument “escape=”, which is set as the escape
    character using the syntax “x LIKE y ESCAPE
    ‘’”.[¶](#change-d248403840e6a2e0c66b497f9dfd1f44)

    参考文献：[＃791](http://www.sqlalchemy.org/trac/ticket/791)，[＃993](http://www.sqlalchemy.org/trac/ticket/993)

-   **[sql]**random() is now a generic sql function and will compile to
    the database’s random implementation, if
    any.[¶](#change-7f02bb91d56e815b7b631be7c7323f79)

-   **[sql]**
    update()。values()和 insert()。values()接受关键字参数[¶](#change-a08969f0ce6ab98d21abf6e35cebaa1d)

-   **[sql]**Fixed an issue in select() regarding its generation of FROM
    clauses, in rare circumstances two clauses could be produced when
    one was intended to cancel out the other.
    一些有很多急切加载的 ORM 查询可能已经看到了这种症状。[¶](#change-085c87879e1a4fb0d6206454a950a1ce)

-   **[sql]**The case() function now also takes a dictionary as its
    whens parameter. 它还将“THEN”表达式解释为默认值，意思是 case（[（x ==
    y，“foo”）]）会将“foo”解释为绑定值，而不是 SQL 表达式。在这种情况下，使用文本（expr）作为文字 SQL 表达式。对于标准本身，只有存在“value”关键字时，这些才可以是文字字符串，否则 SA 将强制显式使用 text()或 literal()。[¶](#change-fb0089247521d91d7d7bb262cb411a64)

### MySQL 的[¶ T0\>](#change-0.4.5-mysql "Permalink to this headline")

-   **[mysql]**方言用于缓存服务器设置的 connection.info 键已更改，现在命名空间[¶](#change-c22f3fdf2cdf167542da47643dfc68ab)

### MSSQL [¶ T0\>](#change-0.4.5-mssql "Permalink to this headline")

-   **[mssql]**反射表现在会自动加载自动加载表中外键引用的其他表，[¶](#change-c08d60f2100e58e57023f2ea19c2c241)

    参考文献：[＃979](http://www.sqlalchemy.org/trac/ticket/979)

-   **[mssql]**添加了 executemany 检查以跳过标识获取，[¶](#change-bd1313c4dc35f7c1f3a1380578f9c1e5)

    参考文献：[＃916](http://www.sqlalchemy.org/trac/ticket/916)

-   **[mssql]**添加小日期类型的存根[¶](#change-80eac4c5f370dd297d4e3cafbad27a96)

    参考文献：[＃884](http://www.sqlalchemy.org/trac/ticket/884)

-   **[mssql]**为 pyodbc 方言添加了一个新的'driver'关键字参数。如果提供，将替换为 ODBC 连接字符串，默认为'SQL
    Server'。[¶](#change-171f3ad2f4dba5fde36680baa1dc3875)

-   **[mssql]**为 pyodbc 方言增加了一个新的'max\_identifier\_length'关键字参数。[¶](#change-81777f583ac945b32caaf0ee3aee5e0f)

-   **[mssql]**改进 pyodbc +
    Unix。如果您之前无法使用该组合，请再试一次。[¶](#change-4a7ee1c669796dd4516a38bfb42b52ff)

### 预言[¶ T0\>](#change-0.4.5-oracle "Permalink to this headline")

-   **[oracle]**表中的“owner”关键字现在已被弃用，并且与“schema”关键字完全同义。现在可以使用替代的“所有者”属性来反映表，这些属性在 Table 对象中明确声明或不使用“schema”。[¶](#change-34b821a274800e05021e8fb2396ee13c)

-   **[oracle]**搜索同义词的所有“魔法”，DBLINK 等。在表反射期间默认情况下是禁用的，除非您在表对象上指定“oracle\_resolve\_synonyms
    =
    True”。解析同义词必然会导致一些混乱的猜测，我们宁愿在默认情况下离开。设置标志时，表格和相关表格将在所有情况下针对同义词进行解析，这意味着如果某个特定表格存在同义词，则反映将在反映相关表格时使用它。这比以前更加粘性，这就是为什么它默认关闭。[¶](#change-fa31cab3a0232df3b107e07f3910f759)

-   **[oracle]**表中的“owner”关键字现在已被弃用，并且与“schema”关键字完全同义。现在可以使用替代的“所有者”属性来反映表，这些属性在 Table 对象中明确声明或不使用“schema”。[¶](#change-34b821a274800e05021e8fb2396ee13c)

-   **[oracle]**搜索同义词的所有“魔法”，DBLINK 等。在表反射期间默认情况下是禁用的，除非您在表对象上指定“oracle\_resolve\_synonyms
    =
    True”。解析同义词必然会导致一些混乱的猜测，我们宁愿在默认情况下离开。设置标志时，表格和相关表格将在所有情况下针对同义词进行解析，这意味着如果某个特定表格存在同义词，则反映将在反映相关表格时使用它。这比以前更加粘性，这就是为什么它默认关闭。[¶](#change-fa31cab3a0232df3b107e07f3910f759)

### 杂项[¶ T0\>](#change-0.4.5-misc "Permalink to this headline")

-   **[declarative]
    [extension]**“同义词”功能现在可直接与“声明式”使用。使用“描述符”关键字参数传递装饰属性，例如：somekey
    = synonym（'\_ somekey'，descriptor =
    property（g，s））[¶](#change-f5fc92b64655f9897a0758861123e3dc)

-   **[declarative]
    [extension]**“延迟”功能可用于“声明式”。最简单的用法是将 deferred 和 Column 声明在一起，例如：data
    =
    deferred（Column（Text））[¶](#change-1c8b78acb5469017fa9165603b123205)

-   **[declarative] [extension]**Declarative also gained
    @synonym\_for(...) and @comparable\_using(...), front-ends for
    synonym and
    comparable\_property.[¶](#change-92af8493880c77b027ad568e9fea4a4e)

-   **[declarative]
    [extension]**在使用声明性时改进了 mapper 编译；当使用[¶](#change-2e0484c6c3c3b159d5dce42185fd83af)时，已编译的映射器仍然会触发编译其他未编译的映射器

    参考文献：[＃995](http://www.sqlalchemy.org/trac/ticket/995)

-   **[declarative] [extension]**Declarative will complete setup for
    Columns lacking names, allows a more DRY syntax.

    > Foo 类（基地）：
    > :   \_\_tablename\_\_ ='foos'id =列（整型，primary\_key = True）

    [¶](#change-ab9ef5d41c92c8b3e3cf08569f4910fe)

-   **[declarative] [extension]**inheritance in declarative can be
    disabled when sending “inherits=None” to
    \_\_mapper\_args\_\_.[¶](#change-47dc505eeee78f8e4a2036cd9ec269e8)

-   **[declarative] [extension]**declarative\_base() takes optional
    kwarg “mapper”, which is any callable/class/method that produces a
    mapper, such as declarative\_base(mapper=scopedsession.mapper).
    这个属性也可以使用“\_\_mapper\_cls\_\_”属性在单独的声明式类中设置。[¶](#change-d23aa381b803d1871f4a8e5090558669)

-   **[postgres]**将 PG 服务器端游标恢复成形，添加固定单元测试作为默认测试套件的一部分。为光标 ID
    [¶](#change-b6f64ab87a83752e5c837be7a29259da)添加了更好的唯一性

    参考文献：[＃1001](http://www.sqlalchemy.org/trac/ticket/1001)

0.4.4 [¶ T0\>](#change-0.4.4 "Permalink to this headline")
----------------------------------------------------------

发布日期：2008 年 3 月 12 日

### ORM [¶ T0\>](#change-0.4.4-orm "Permalink to this headline")

-   **[orm]**any(), has(), contains(), \~contains(), attribute level ==
    and != now work properly with self-referential relations - the
    clause inside the EXISTS is aliased on the “remote” side to
    distinguish it from the parent table.
    这适用于单表自我引用以及基于继承的自引用。[¶](#change-26d54c6302b65f9de74b3cf2e3a5d512)

-   **[orm]**当与一对一关系的 NULL 进行比较时，关系()级别的==和！=运算符的修复行为[¶](#change-57e9f7b0e107e07a75467467df6a2d2d)

    参考文献：[＃985](http://www.sqlalchemy.org/trac/ticket/985)

-   **[orm]**Fixed bug whereby session.expire() attributes were not
    loading on an polymorphically-mapped instance mapped by a
    select\_table mapper.[¶](#change-6b0aad45ce1f29ad9158b8009df12108)

-   **[orm]**新增了 query.with\_polymorphic() -
    指定从基类继承的类的列表，该列将被添加到查询的 FROM 子句中。允许在 filter()标准中使用子类，并且急切地加载这些子类的属性。[¶](#change-4a735ee740f2ee53043439ca2374e2bd)

-   **[orm]**Your cries have been heard: removing a pending item from an
    attribute or collection with delete-orphan expunges the item from
    the session; no FlushError is raised.
    请注意，如果 session.save()显式地处理了待处理项目，那么属性/集合删除仍会将其敲除。[¶](#change-260b0a787300d2b7ce427e108dcbf68d)

-   **[orm]**session.refresh() and session.expire() raise an error when
    called on instances which are not persistent within the
    session[¶](#change-6af8ad8ff1bc8b70b4267a621b75aa56)

-   **[orm]**修复了使用 join()方法生成多个查询对象时使用相同 Query 的潜在生成 bug。[¶](#change-39aac3cdd599e8bac76663700e034c9e)

-   **[orm]**Fixed bug which was introduced in 0.4.3, whereby loading an
    already-persistent instance mapped with joined table inheritance
    would trigger a useless “secondary” load from its joined table, when
    using the default “select” polymorphic\_fetch.
    这是由于属性在第一次加载过程中被标记为过期，并且没有从先前的“次要”加载取消标记。在任何加载或提交操作成功之后，基于\_\_dict\_\_中的存在，属性现在未到期。[¶](#change-b9f84fa3c8eb53ab3417b2ff57afae13)

-   **[orm]**Deprecated Query methods apply\_sum(), apply\_max(),
    apply\_min(), apply\_avg(). 更好的方法来了……
    [¶](#change-5c46e27af0aab071053f1150c32ad167)

-   **[orm]**relation() can accept a callable for its first argument,
    which returns the class to be related.
    这是为了协助声明性包来定义关系，而没有使用类。[¶](#change-1a2a5f137d66ae4e45a504a7fcb25a9b)

-   **[orm]**Added a new “higher level” operator called “of\_type()”:
    used in join() as well as with any() and has(), qualifies the
    subclass which will be used in filter criterion, e.g.:

    > query.filter（Company.employees.of\_type（工程师）。
    > :   任何（Engineer.name ==”富”））
    >
    > 要么
    >
    > query.join（Company.employees.of\_type（工程师））。
    > :   过滤（Engineer.name ==”富”）

    [¶](#change-a4ea39df253b6f91a5d8204bf227ada0)

-   **[orm]**针对 flush()中潜在的丢失引用错误的预防代码。[¶](#change-1272340a6e01cf700e61e3d2f39cdacf)

-   **[orm]**Expressions used in filter(), filter\_by() and others, when
    they make usage of a clause generated from a relation using the
    identity of a child object (e.g., filter(Parent.child==)), evaluate
    the actual primary key value of at execution time so that the
    autoflush step of the Query can complete, thereby populating the PK
    value of in the case that was
    pending.[¶](#change-664f4f2b4efd0e58806d46ba15d2618a)

-   **[orm]**setting the relation()-level order by to a column in the
    many-to-many “secondary” table will now work with eager loading,
    previously the “order by” wasn’t aliased against the secondary
    table’s alias.[¶](#change-92a43783a44458853e3f87836801b5f0)

-   **[orm]**现有描述符之上的同义词现在是这些描述符的完整代理。[¶](#change-8c8e596e12f51cbaab0d60f9eb39e22a)

### SQL [¶ T0\>](#change-0.4.4-sql "Permalink to this headline")

-   **[sql]**可以根据文本 FROM 子句再次创建选择别名。[¶](#change-361cea88f023decd2edcc9f4bcfb85d9)

    参考文献：[＃975](http://www.sqlalchemy.org/trac/ticket/975)

-   **[sql]**
    bindparam()的值可以是一个可调用的，在这种情况下，它会在语句执行时计算以获取该值。[¶](#change-f29b12fe4c2de26e389d59d438cf1ea8)

-   **[sql]**增加了异常包装/重新连接支持以获取结果集。重新连接适用于那些在结果期间引发可捕获数据错误的数据库（即，不适用于 MySQL）[¶](#change-fa73dc1b6400960fc86f04e571789eac)

    参考文献：[＃978](http://www.sqlalchemy.org/trac/ticket/978)

-   **[sql]**通过 engine.begin\_twophase()，engine.prepare()[¶](#change-82a8a6a9be6beb556e3c11919db1d762)实现“threadlocal”引擎的两阶段 API。

    参考文献：[＃936](http://www.sqlalchemy.org/trac/ticket/936)

-   **[sql]**修正了阻止 UNION 被克隆的 bug。[¶](#change-3ca250e58167aa467bdd74e86f81f8e2)

    参考文献：[＃986](http://www.sqlalchemy.org/trac/ticket/986)

-   **[sql]**Added “bind” keyword argument to insert(), update(),
    delete() and DDL().
    .bind 属性现在可以在这些语句以及 select()上分配。[¶](#change-cace8907ce2c688f149a3b7193cb6f03)

-   **[sql]**Insert statements can now be compiled with extra “prefix”
    words between INSERT and INTO, for vendor extensions like MySQL’s
    INSERT IGNORE INTO
    table.[¶](#change-0e487d0efd2d32fd049531b232a703ea)

### 杂项[¶ T0\>](#change-0.4.4-misc "Permalink to this headline")

-   **[dialects]**无效的 SQLite 连接 URL 现在引发错误。[¶](#change-e896f826ca21ffa3a8aee4ce1aa75540)

-   **[dialects]** postgres
    TIMESTAMP 正确呈现[¶](#change-1f49158d705ba22bde8f415aae01e7df)

    参考文献：[＃981](http://www.sqlalchemy.org/trac/ticket/981)

-   **[dialects]**默认情况下，postgres
    PGArray 是一个“可变”类型；当与 ORM 一起使用时，可变样式相等/写时复制技术用于测试更改。[¶](#change-26c194222a2217765863b953678f61d7)

-   **[extensions]**添加了一个新的超小型“声明式”扩展，它允许 Table 和 mapper()配置在类声明下以内联方式进行。这个扩展不同于 ActiveMapper 和 Elixir，因为它根本不重新定义任何 SQLAlchemy 语义；文字 Column，Table 和 relation()构造用于定义类的行为和表定义。[¶](#change-11410361d1e94b674b2dd45f62aa879c)

0.4.3 [¶ T0\>](#change-0.4.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2008 年 2 月 14 日

### 一般[¶ T0\>](#change-0.4.3-general "Permalink to this headline")

-   **[general]**修正了 Python
    2.3 中各种隐藏和一些不那么隐藏的兼容性问题，这要归功于在 2.3 上运行完整测试套件的新支持。[¶](#change-6edf54fb64a6efb12a4b41bf8fca7e85)

-   **[general]**警告现在发布为类型 exceptions.SAWarning。[¶](#change-8292102deab2ae8658025f199f4dba39)

### ORM [¶ T0\>](#change-0.4.3-orm "Permalink to this headline")

-   **[orm]**Every Session.begin() must now be accompanied by a
    corresponding commit() or rollback() unless the session is closed
    with Session.close(). 这还包括用 transactional =
    True 创建的会话隐含的 begin()。这里介绍的最大变化是，当使用 transactional
    =
    True 创建的会话在 flush()期间引发异常时，必须调用 Session.rollback()或 Session.close()以便该会话在异常后继续。[¶
    T0\>](#change-ed63aadc46e831e27192365c26bcbd40)

-   **[orm]**固定 merge()集合 -
    当将瞬态实体与 backref 的集合合并时加倍的 bug。[¶](#change-4066869a71ee4e92e757eed30c24fcd6)

    参考文献：[＃961](http://www.sqlalchemy.org/trac/ticket/961)

-   **[orm]**merge(dont\_load=True) does not accept transient entities,
    this is in continuation with the fact that merge(dont\_load=True)
    does not accept any “dirty” objects
    either.[¶](#change-f30c07f4ca0f0cba96e2f3cb6182473e)

-   **[orm]**添加了由 scoped\_session 生成的独立“查询”类属性。这提供了 MyClass.query 而不使用 Session.mapper。使用途径：

    > MyClass.query = Session.query\_property()

    [¶](#change-12a5e6022a8effac005d99575c5c415b)

-   **[orm]**尝试访问过期实例属性时没有会话存在时，会引发正确的错误消息[¶](#change-73db7d20e8dbfeedb6ba0b6cc4788aea)

-   **[orm]**dynamic\_loader() / lazy=”dynamic” now accepts and uses the
    order\_by parameter in the same way in which it works with
    relation().[¶](#change-549192f88e74438d43000f482dc4a551)

-   **[orm]**为 Session 添加了 expire\_all()方法。调用所有持久实例的 expire()。这与...
    [¶](#change-ff6e9ef1dbfd714585ff152dd416a7d6)相结合

-   **[orm]**已经部分或完全过期的实例将在定期查询操作期间填充它们的过期属性，从而影响这些对象，从而为每个实例阻止不必要的第二条 SQL 语句。[T2\>](#change-42759467a8bd5b23f099a069100e4e3a)

-   **[orm]**Dynamic relations, when referenced, create a strong
    reference to the parent object so that the query still has a parent
    to call against even if the parent is only created (and otherwise
    dereferenced) within the scope of a single
    expression.[¶](#change-b8b6e98149bfd5318ccf249d510a02ee)

    参考文献：[＃938](http://www.sqlalchemy.org/trac/ticket/938)

-   **[orm]**添加了 mapper()标志“eager\_defaults”。如果设置为 True，则在 INSERT 或 UPDATE 操作期间生成的缺省值会立即被后取回，而不会延迟到稍后。这模仿了旧的 0.3 行为。[¶](#change-45880f45e498cf7f425d5f004b1ec762)

-   **[orm]**query.join() can now accept class-mapped attributes as
    arguments.
    这些可以用于或与琴弦结合使用。特别是，这允许构建多态关系上的子类的连接，即：

    > 查询（公司）.join（['employees'，Engineer.name]）

    [¶](#change-3891a133d4bd12b14d6068cb8f605156)

-   **[orm] [people.join(engineer))] [(‘employees’]
    [Engineer.name]**query.join() can also accept tuples of attribute
    name/some selectable as arguments.
    这允许从多态关系的子类建立连接*，即：*

    > 查询（公司）。加入（
    >
    > )

    [¶](#change-42b75449eedabd47e5cb497bfbb59051)

-   **[orm]**结合多态映射器的 join()行为的一般改进，即从/到多态映射器的连接和正确应用别名。[¶](#change-899c6f1ca175ba0b8f026dc0aa41d68b)

-   **[orm]**Fixed/improved behavior when a mapper determines the
    natural “primary key” of a mapped join, it will more effectively
    reduce columns which are equivalent via foreign key relation.
    这会影响需要将多少个参数发送到 query.get()等。[¶](#change-4701dbe6a7375d90fa6b81601106e759)

    参考文献：[＃933](http://www.sqlalchemy.org/trac/ticket/933)

-   **[orm]**延迟加载器现在可以处理连接条件，其中“绑定”列（即获取作为绑定参数发送的父代码的列）在连接条件中多次出现。具体来说，这允许包含父相关子查询的关系()的常见任务，比如“只选择最近的子项”。[¶](#change-d7ca86341f6b875bc802fc522eda643c)

    参考文献：[＃946](http://www.sqlalchemy.org/trac/ticket/946)

-   **[orm]**Fixed bug in polymorphic inheritance where an incorrect
    exception is raised when base polymorphic\_on column does not
    correspond to any columns within the local selectable of an
    inheriting mapper more than one level
    deep[¶](#change-7ebcbb5cac084dd34f876f1e979346d5)

-   **[orm]**Fixed bug in polymorphic inheritance which made it
    difficult to set a working “order\_by” on a polymorphic
    mapper.[¶](#change-52902ccac0e5570582c25b376fecb10b)

-   **[orm]**在 Query 中修复了一个相当昂贵的调用，它减缓了多态查询的速度。[¶](#change-2202798af2faf2de027d6e9cb53425b2)

-   如果需要，可以在 flush()调用期间加载“被动默认值”和其他“内联”默认值；
    **[orm]**特别是，这允许在外键列引用服务器端生成的非主键列的情况下构建关系()。[¶](#change-1174dcf99d9e604b10ae1b362749fc8d)

    参考文献：[＃954](http://www.sqlalchemy.org/trac/ticket/954)

-   **[orm]**

    其他会话事务修正/更改：
    :   -   修正会话事务管理的错误：在向嵌套事务添加连接时，父连接事务未在连接上启动。
        -   session.transaction 现在始终引用最内层的活动事务，即使在会话事务对象上直接调用 commit
            / rollback 时也是如此。
        -   现在可以准备两阶段交易。
        -   在一个连接上准备两阶段事务失败时，所有连接都会回滚。
        -   当使用嵌套事务时，session.close()没有关闭所有事务。
        -   rollback()以前错误地将当前事务直接设置为可以回滚到的事务的父级。现在它回滚可以处理它的下一个事务，但将当前事务设置为其父项，并停用它们之间的事务。非活动事务只能回滚或关闭，任何其他调用都会导致错误。
        -   对于简单的子事务，commit()的 autoflush 不会冲洗。
        -   当会话不在事务中并且提交事务失败时，unitofwork
            flush 没有关闭失败的事务。

    [¶](#change-33a848efb3c77483bf094e0593a0f304)

-   **[orm]**其他票据：[¶](#change-156ce1b0bbba6a383724228e99b59141)

    参考文献：[＃964](http://www.sqlalchemy.org/trac/ticket/964)，[＃940](http://www.sqlalchemy.org/trac/ticket/940)

### SQL [¶ T0\>](#change-0.4.3-sql "Permalink to this headline")

-   **[sql]**添加了“schema.DDL”，一个可执行的自由格式的 DDL 语句。DDL 可以独立执行或附加到 Table 或 MetaData 实例，并在创建和/或删除对象时自动执行。[¶](#change-6dc387bc33169ccc70dccd8218f63eb6)

-   **[sql]**Table columns and constraints can be overridden on a an
    existing table (such as a table that was already reflected) using
    the ‘useexisting=True’ flag, which now takes into account the
    arguments passed along with
    it.[¶](#change-7a15201e78fb2f315a974ea2f2fdf57e)

-   **[sql]**添加了一个基于可调用的 DDL 事件接口，在 Tables 和 MetaData 创建和删除之前和之后添加了钩子。[¶](#change-9901077c4d7b859ebcf02d4e4c960588)

-   **[sql]**Added generative where() method to delete() and update()
    constructs which return a new object with criterion joined to
    existing criterion via AND, just like
    select().where().[¶](#change-55f9b7d9b3f544d05ee33d474e48e718)

-   **[sql]**Added “ilike()” operator to column operations.
    在 postgres 上编译为 ILIKE，在所有其他上编译为（lower）（y）。[¶](#change-cda5a8913a71356022156500329b8ea2)

    参考文献：[＃727](http://www.sqlalchemy.org/trac/ticket/727)

-   **[sql]**将“now()”添加为通用函数；在 SQLite 上，Oracle 和 MSSQL 编译为“CURRENT\_TIMESTAMP”；
    “now()”在所有其他上。[¶](#change-f9d50ae6c3ab814c61e765a4597db4a7)

    参考文献：[＃943](http://www.sqlalchemy.org/trac/ticket/943)

-   **[sql]**The startswith(), endswith(), and contains() operators now
    concatenate the wildcard operator with the given operand in SQL,
    i.e. “’%’ || ” in all cases, accept text(‘something’) operands
    properly[¶](#change-dc43f597e2f6c04ee681a57b1cdcab9f)

    参考文献：[＃962](http://www.sqlalchemy.org/trac/ticket/962)

-   **[sql]**
    cast()正确接受文本（'something'）和其他非文字操作数[¶](#change-6e11a1c8b10e4f234d4523225bd257ef)

    参考文献：[＃962](http://www.sqlalchemy.org/trac/ticket/962)

-   **[sql]**修复了结果代理中的 bug，其中匿名生成的列标签无法使用其直接字符串名称访问[¶](#change-058b2c299ce6bcfa574f984a4c4a6e71)

-   **[sql]**现在可以定义可延迟的约束。[¶](#change-3115dcb8cdb282b57a31d91ec76e5e43)

-   **[sql]**Added “autocommit=True” keyword argument to select() and
    text(), as well as generative autocommit() method on select(); for
    statements which modify the database through some user-defined means
    other than the usual INSERT/UPDATE/ DELETE etc.
    如果没有事务正在进行，该标志将在执行期间启用“自动提交”行为。[¶](#change-0fdb4ae6ed3cdbc2764f585352789ad5)

    参考文献：[＃915](http://www.sqlalchemy.org/trac/ticket/915)

-   **[sql]**现在 selectable 上的'.c。'属性在其 columns 子句中为每个列表达式获取一个条目。以前，像函数和 CASE 语句这样的“未命名”列没有放在那里。现在，如果没有“名称”可用，他们将使用完整的字符串表示形式。[¶](#change-8ab38a99c33031ed1be3e3d2f2018ad6)

-   **[sql]**a CompositeSelect, i.e. any union(), union\_all(),
    intersect(), etc.
    现在断言每个可选项包含相同数量的列。这符合相应的 SQL 要求。[¶](#change-dee2d53230f0bb2006399dd3a1acc69b)

-   **[sql]**The anonymous ‘label’ generated for otherwise unlabeled
    functions and expressions now propagates outwards at compile time
    for expressions like
    select([select([func.foo()])]).[¶](#change-9aaabc97770589be11258354e4103c20)

-   **[sql]**Building on the above ideas, CompositeSelects now build up
    their ”.c.” collection based on the names present in the first
    selectable only; corresponding\_column() now works fully for all
    embedded selectables.[¶](#change-e38291a9bb6875caafe6ff4eb62837d6)

-   **[sql]**Oracle and others properly encode SQL used for defaults
    like sequences, etc., even if no unicode idents are used since
    identifier preparer may return a cached unicode
    identifier.[¶](#change-effacbc8cacf7eccb6b38ba3cbbae70c)

-   **[sql]**Column and clause comparisons to datetime objects on the
    left hand side of the expression now work (d \< table.c.col).
    （RHS 上的日期时间一直有效，LHS 异常是日期时间实现的一个怪癖。）[¶](#change-1d04331648e18d01c0c95d1e615df08e)

### 杂项[¶ T0\>](#change-0.4.3-misc "Permalink to this headline")

-   **[dialects]**更好地支持 SQLite 中的模式（通过 ATTACH DATABASE ...
    AS 名称链接）。在过去的某些情况下，为 SQLite 生成的 SQL 中省略了模式名称。这不再是这种情况。[¶](#change-f63c306a189efd4f901b963ab28adb1f)

-   **[dialects]**
    SQLite 上的 table\_names 现在也会选取临时表。[¶](#change-9dee0f004a0cf1c0917dc6380650d13a)

-   **[dialects]**在反射操作期间自动检测未指定的 MySQL
    ANSI\_QUOTES 模式，支持在中途更改模式。如果不使用反射，仍然需要手动模式设置。[¶](#change-60a5b994550ff76a748f3c1c1876328e)

-   **[dialects]**修正了 SQLite 的 TIME 列的反映。[¶](#change-d2deeecdb1769a651e3418d54d79a6f7)

-   **[dialects]**最后将 PGMacAddr 类型添加到 postgres
    [¶](#change-df90bbae9a24a548712386fea17c51d7)

    参考文献：[＃580](http://www.sqlalchemy.org/trac/ticket/580)

-   **[dialects]**在 Firebird
    [¶](#change-aa4961efc15ee34be7bcbce396b294c8)下反映与 PK 字段关联的序列（通常使用 BEFORE
    INSERT 触发器）

-   **[dialects]**Oracle assembles the correct columns in the result set
    column mapping when generating a LIMIT/OFFSET subquery, allows
    columns to map properly to result sets even if long-name truncation
    kicks in[¶](#change-b06276ebd78dee4b8b236cfc9f6ea19e)

    参考文献：[＃941](http://www.sqlalchemy.org/trac/ticket/941)

-   **[dialects]** MSSQL 现在在\_is\_select
    regexp 中包含 EXEC，它应该允许使用行返回存储过程。[¶](#change-34c2a03d48cdd10e0016278bc5941d22)

-   **[dialects]** MSSQL 现在使用 ANSI SQL row\_number()函数包含 LIMIT /
    OFFSET 的实验性实现，因此它需要 MSSQL-2005 或更高版本。要启用该功能，请将“has\_window\_funcs”添加到连接的关键字参数中，或将“？has\_window\_funcs
    =
    1”添加到您的 dburi 查询参数中。[¶](#change-1fc2c8bc3c3438aaf84a962c2176c65b)

-   **[ext]**更改了 ext.activemapper 以使用对象库的非事务性会话。[¶](#change-937a4731635f0eb9fc1445d0e3061924)

-   **[ext]**在关联代理列表中修复了“['a'] +
    obj.proxied”二元运算的输出顺序。[¶](#change-9adb592707c367ff5863e266ed996077)

0.4.2p3 [¶ T0\>](#change-0.4.2p3 "Permalink to this headline")
--------------------------------------------------------------

发布于：2008 年 1 月 09 日

### 一般[¶ T0\>](#change-0.4.2p3-general "Permalink to this headline")

-   **[general]**子版本编号方案更改为套件 setuptools 版本号规则；
    easy\_install
    -u 现在应该获得 0.4.2 以上的版本。[¶](#change-65d413b7ad515c5729bde99fb2e96731)

### ORM [¶ T0\>](#change-0.4.2p3-orm "Permalink to this headline")

-   **[orm]**在使用“可变标量”（如 PickleTypes）时修复了 session.dirty 的错误[¶](#change-da292c6c47e2281b50fe3872d622ec66)

-   **[orm]**added a more descriptive error message when flushing on a
    relation() that has non-locally-mapped columns in its primary or
    secondary join
    condition[¶](#change-e84ebdc378fd322dd6276c9b7906ed92)

-   在 InstanceState .\_\_
    cleanup()现在，**[orm]**现在抑制*所有*错误。[¶](#change-d24181f3ffcf556b44aa903e5a74b37e)

-   **[orm]**修复了一个属性历史记录错误，因此将新集合分配给已具有未决更改的基于集合的属性会生成不正确的历史记录[¶](#change-d2a931ab43317f5fcf9c6bdb7f4f4a39)

    参考文献：[＃922](http://www.sqlalchemy.org/trac/ticket/922)

-   **[orm]**fixed delete-orphan cascade bug whereby setting the same
    object twice to a scalar attribute could log it as an
    orphan[¶](#change-d81770ec7c97121d21e6eb326d9bb5da)

    参考文献：[＃925](http://www.sqlalchemy.org/trac/ticket/925)

-   **[orm]**固定级联在+
    =赋值给基于列表的关系上[¶](#change-13a128b105a34070dcf5a5147913fa10)

-   **[orm]**synonyms can now be created against props that don’t exist
    yet, which are later added via add\_property().
    这通常包括 backrefs。（即，您可以为 backrefs 制作同义词而不用担心操作顺序）[¶](#change-331b7392042497e067064bc0ea7a7a43)

    参考文献：[＃919](http://www.sqlalchemy.org/trac/ticket/919)

-   **[orm]**修复了多态“联合”映射器可能发生的错误，该映射器可以回退到“延迟”加载继承表[¶](#change-72cde5697e7ad6e3b60d641e29048733)

-   **[orm]**the “columns” collection on a mapper/mapped class (i.e.
    ‘c’) is against the mapped table, not the select\_table in the case
    of polymorphic “union” loading (this shouldn’t be
    noticeable).[¶](#change-fed49544228d810c496b9938b4c43c75)

-   **[orm]**修复了相当严重的错误，因此可以在 unitofwork.new 集合中多次列出相同的实例；在使用继承映射器和 ScopedSession.mapper 的组合时最为典型，因为每个实例的多个\_\_init\_\_调用可以使用不同的\_state 对象保存()该对象[¶](#change-3ca851d8498ea2458bba602dee5ad8dd)

-   **[orm]**为 Query 添加了非常基本的产生迭代器行为。调用 query.yield\_per（）并在迭代上下文中评估查询；
    N 行的每个集合都将被打包并生成。
    T0\>使用此方法时要格外小心，因为它不会尝试在结果批处理边界上协调加载的集合，如果同一个实例出现在多个批处理中，它的行为也不会很好。这意味着如果一个批量加载的集合在多个批次中被引用，那么它将被清除，并且在所有情况下，属性将被覆盖在多个批次中发生的实例上。[¶](#change-b0ea0f39c7d503288cdab2a995ef5b83)

-   **[orm]**修正集合集合和关联代理集合的 set
    in-set 集合变异操作符。[¶](#change-779e1c774fac07bedf9baab019348183)

    参考文献：[＃920](http://www.sqlalchemy.org/trac/ticket/920)

### SQL [¶ T0\>](#change-0.4.2p3-sql "Permalink to this headline")

-   **[sql]**现在正确导出文本类型，并且不会在 DDL 创建时发出警告；没有长度的字符串类型只会在 CREATE
    TABLE [¶](#change-6a9e11d8c0bcdb3037efda66da46f2b0)期间引发警告

    参考文献：[＃912](http://www.sqlalchemy.org/trac/ticket/912)

-   **[sql]**添加新的 UnicodeText 类型，以指定编码的，不变的文本类型[¶](#change-52447b5d997e550edaff1460987456ea)

-   **[sql]**fixed bug in union() so that select() statements which
    don’t derive from FromClause objects can be
    unioned[¶](#change-c6e6be84c763b537b8b61ef8374ed8fe)

-   **[sql]**由于其“通用”类型，所以将 TEXT 的名称更改为文本；
    TEXT 名称不推荐使用，直到 0.5。没有长度时，字符串到文本的“升级”行为也被弃用，直到 0.5；将在用于 CREATE
    TABLE 语句时发出警告（对于 SQL 表达式，没有长度的字符串仍然正常）[¶](#change-b4c8efafaa4b6fccec8239e9c9d14b0f)

    参考文献：[＃912](http://www.sqlalchemy.org/trac/ticket/912)

-   **[sql]**generative select.order\_by(None) / group\_by(None) was not
    managing to reset order by/group by criterion,
    fixed[¶](#change-11b279a02c641038e4cf01bcf7a3de4c)

    参考文献：[＃924](http://www.sqlalchemy.org/trac/ticket/924)

### 杂项[¶ T0\>](#change-0.4.2p3-misc "Permalink to this headline")

-   **[dialects]**固定反映 mysql 空字符串列的默认值。[¶](#change-266d2296f2e6b99bc2514a5fd438deae)

-   **[ext]**'+'，'\*'，'+ ='和'\*
    ='支持关联代理列表。[¶](#change-564eaa28aa3238cb8107b93c413f59d9)

-   **[dialects]**mssql - narrowed down the test for “date”/”datetime”
    in MSDate/ MSDateTime subclasses so that incoming “datetime” objects
    don’t get mis-interpreted as “date” objects and vice
    versa.[¶](#change-88e678f937cdc36ead073631a00ca08b)

    参考文献：[＃923](http://www.sqlalchemy.org/trac/ticket/923)

-   **[dialects]**修正了对 PGArray 类型的子类型结果处理器缺少的调用。[¶](#change-3ed94dc039b8b2b50313d99519db04d5)

    参考文献：[＃913](http://www.sqlalchemy.org/trac/ticket/913)

0.4.2 [¶ T0\>](#change-0.4.2 "Permalink to this headline")
----------------------------------------------------------

发布于：2008 年 1 月 2 日

### ORM [¶ T0\>](#change-0.4.2-orm "Permalink to this headline")

-   **[orm]**对基于收集的 backrefs 的主要行为改变：它们不再触发延迟加载！“反向”添加和删除将排队并在实际读取和加载时与集合合并；但不要事先触发负载。对于已经注意到这种行为的用户，这应该比在某些情况下使用动态关系更方便；对于那些没有的人来说，在某些情况下，你可能会注意到你的应用比以前少了很多查询。[¶](#change-63f5538d57cbeccd4405271fb765620d)

    参考文献：[＃871](http://www.sqlalchemy.org/trac/ticket/871)

-   **[orm]**可变主键支持。主键列可以自由更改，并且实例的身份将在刷新时更改。另外，支持与关系的外键引用（主键或不键）更新级联，或者与数据库的 ON
    UPDATE
    CASCADE（对于像 Postgres 这样的 DB 所需的）或由 UPDATE 语句形式的 ORM 直接发布的设置标志“passive\_cascades
    = False”。[¶](#change-217b4c5e361c5fb21dea6f5061d41edc)

-   **[orm]**inheriting mappers now inherit the MapperExtensions of
    their parent mapper directly, so that all methods for a particular
    MapperExtension are called for subclasses as well.
    与往常一样，任何 MapperExtension 都可以返回 EXT\_CONTINUE 以继续扩展处理，或者返回 EXT\_STOP 以停止处理。The
    order of mapper resolution is: .

    请注意，如果您分别实例化相同的扩展类，然后将其单独应用于同一继承链中的两个映射器，则该扩展将应用两次到继承类，并且每个方法将被调用两次。

    要将映射器扩展显式应用于每个继承类，但每个操作只调用一次每个方法，请为两个映射器使用扩展的相同实例。

    [¶](#change-e8ea4a2d69bd572ec6dfb581a1a81bc8)

    参考文献：[＃490](http://www.sqlalchemy.org/trac/ticket/490)

-   **[orm]**MapperExtension.before\_update() and after\_update() are
    now called symmetrically; previously, an instance that had no
    modified column attributes (but had a relation() modification) could
    be called with before\_update() but not
    after\_update()[¶](#change-32b5c8ae4f1ba4eae88b6d041b12a29d)

    参考文献：[＃907](http://www.sqlalchemy.org/trac/ticket/907)

-   **[orm]**在 Query 的 select 语句中丢失的列现在在加载期间自动延迟。[¶](#change-27b98340e4e7bca99aa258a02c0b8f4c)

-   **[orm]**mapped classes which extend “object” and do not provide an
    \_\_init\_\_() method will now raise TypeError if non-empty \*args
    or \*\*kwargs are present at instance construction time (and are not
    consumed by any extensions such as the scoped\_session mapper),
    consistent with the behavior of normal Python
    classes[¶](#change-63184f50e7524cf31995dceb7eba804c)

    参考文献：[＃908](http://www.sqlalchemy.org/trac/ticket/908)

-   **[orm]**修正了 filter\_by()与 None 无关的查询错误[¶](#change-e0d48778c2223c5f35f8ee0a6f6241f4)

    参考文献：[＃899](http://www.sqlalchemy.org/trac/ticket/899)

-   **[orm]**improved support for pickling of mapped entities.
    每个实例的 lazy / deferred /
    expired 可调参数现在都是可序列化的，以便它们使用\_state 进行序列化和反序列化。[¶](#change-4790b003fa9887f231b4dab765719240)

-   **[orm]**new synonym() behavior: an attribute will be placed on the
    mapped class, if one does not exist already, in all cases.
    如果某个属性已经存在于该类中，则同义词将使用适当的比较运算符修饰该属性，以便与列表表达式中的任何其他映射属性一样使用该属性（即可用于 filter()等）“代理=真”标志被弃用，不再意味着任何东西。此外，标志“map\_column
    =
    True”将自动生成与同义词名称对应的 ColumnProperty，即：'somename'：synonym（'\_
    somename'，map\_column = True）将名为'somename'的列映射到属性'
    \_somename”。请参阅映射器文档中的示例。[¶](#change-9d03199c53171e51a07d7087bbc50381)

    参考文献：[＃801](http://www.sqlalchemy.org/trac/ticket/801)

-   **[orm]**
    Query.select\_from()现在用给定的参数替换所有现有的 FROM 标准；之前构造 FROM 子句列表的行为通常不是有用的，因为需要 filter()调用来创建连接标准，并且 filter()中引入的新表已将自己添加到 FROM 子句中。新行为不仅允许从主表连接，还允许选择语句。过滤标准，顺序 bys，预先加载子句将被“别名”为给定语句。[¶](#change-784457e85ca18f636410e38e12185882)

-   **[orm]**this month’s refactoring of attribute instrumentation
    changes the “copy-on-load” behavior we’ve had since midway through
    0.3 with “copy-on-modify” in most cases.
    这需要大量的延迟加载操作，总体上工作量更少，因为只有实际修改的属性才能复制其“已提交状态”。只有“可变标量”属性（即腌渍对象或其他可变项目）（首先是加载拷贝改变的原因）才保留旧行为。[¶](#change-3a785137de08700b2cd2a32fba4f0a05)

-   **[orm]
    [attrname]**属性的轻微行为改变是，除了*not*属性外，会导致该属性的 lazyloader 再次触发；
    “del”使属性“无”的有效值。要重新触发属性的“加载器”，请使用 session.expire（instance，）。[¶](#change-b5fb4c5dc6e51819e3330abdfa847cd0)

-   **[orm]**query.filter(SomeClass.somechild == None), when comparing a
    many-to-one property to None, properly generates “id IS NULL”
    including that the NULL is on the right
    side.[¶](#change-2a465341874590d5feb725a00240b735)

-   **[orm]**query.order\_by() takes into account aliased joins, i.e.
    query.join(‘orders’,
    aliased=True).order\_by(Order.id)[¶](#change-3e8fd64d48f2bbde6c0011dd994f32cb)

-   **[orm]**eagerload(), lazyload(), eagerload\_all() take an optional
    second class-or-mapper argument, which will select the mapper to
    apply the option towards.
    这可以选择使用 add\_entity()添加的其他映射器。[¶](#change-e0a2026f22b806fae3b51161f90eb4aa)

-   **[orm]**
    eagerloading 可以通过 add\_entity()添加映射器。[¶](#change-330cf46efeb1b16709defe4dc85891b0)

-   **[orm]**将“级联删除”行为添加到“动态”关系中，就像正常关系一样。如果 passive\_deletes 标志（也就是刚刚添加的）没有设置，则父项的删除将触发子项的全部加载，以便可以相应地删除或更新它们。[¶](#change-3e54b894ee7ef3856d24b7831a0b878e)

-   **[orm]**还包含动态的，实现的正确的 count()行为以及其他辅助方法。[¶](#change-c1b93949b70a2298405d46cc8d9e165c)

-   **[orm]**修复了多态关系中的级联，使得从一个对象到多态集合的级联沿着集合中每个元素所特有的属性集继续级联。[¶](#change-6d7297ea5825ce8f0a6afbfd061aeb45)

-   **[orm]**query.get() and query.load() do not take existing filter or
    other criterion into account; these methods *always* look up the
    given id in the database or return the current instance from the
    identity map, disregarding any existing filter, join, group\_by or
    other criterion which has been
    configured.[¶](#change-a8ef939d2a84ff9c730c84834a7362d0)

    参考文献：[＃893](http://www.sqlalchemy.org/trac/ticket/893)

-   **[orm]**与继承映射器一起增加了对 version\_id\_col 的支持。version\_id\_col 通常在继承关系中设置在基本映射器上，对所有继承映射器都有效。[¶](#change-6bde88eab909a760935eadb9a4ede0f1)

    参考文献：[＃883](http://www.sqlalchemy.org/trac/ticket/883)

-   **[orm]**放宽了具有标签的 column\_property()表达式的规则；现在接受任何 ColumnElement，因为编译器现在会自动标记未标记的 ColumnElement。像 select()语句那样，selectable 仍然需要通过 as\_scalar()或 label()来转换为 ColumnElement。[¶](#change-eafb815c0a21fff7306edd70ede3f73f)

-   **[orm]**固定的 backref
    bug 如果 attr 是 None，那么你不能删除 instance.attr
    [¶](#change-0d02bce2307e213d0540d00aa850c909)

-   **[orm]**several ORM attributes have been removed or made private:
    mapper.get\_attr\_by\_column(), mapper.set\_attr\_by\_column(),
    mapper.pks\_by\_table, mapper.cascade\_callable(),
    MapperProperty.cascade\_callable(), mapper.canload(),
    mapper.save\_obj(), mapper.delete\_obj(), mapper.\_mapper\_registry,
    attributes.AttributeManager[¶](#change-8a557aa11c6f764820c17470e54658ce)

-   **[orm]**为关系属性分配不兼容的集合类型现在引发 TypeError 而不是 sqlalchemy 的 ArgumentError
    [¶](#change-92cef2776421e3d2d6177bee48214fac)

-   **[orm]**如果传入字典中的密钥与集合的 keyfunc 将用于该值的密钥不匹配，则 MappedCollection 的批量分配现在会引发错误。[¶](#change-df17f2469a0bb5f1a22d42fc865f73a4)

    参考文献：[＃886](http://www.sqlalchemy.org/trac/ticket/886)

-   **[orm] [newval2] [newval1]**Custom collections can now specify a
    @converter method to translate objects used in “bulk” assignment
    into a stream of values, as in:
```python
obj.col =
# or
obj.dictcol = {'foo': newval1, 'bar': newval2}
```
MappedCollection 使用这个钩子来确保从集合的角度来看传入的键/值对是合理的。

    [¶](#change-228dca0bafaa198350cfc39cb6561e8c)plainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplain

-   **[orm]**在双向关系的两侧使用 lazy
    =“dynamic”时修复了无限循环问题[¶](#change-abc2dcd6fd504baa411c4ede8eda7189)

    参考文献：[＃872](http://www.sqlalchemy.org/trac/ticket/872)

-   **[orm]**更多修正了应用 Query + eagerloads 的 LIMIT /
    OFFSET 别名，在这种情况下，映射到 select 语句[¶](#change-5d359376de51a0ecf63071076057725e)

    参考文献：[＃904](http://www.sqlalchemy.org/trac/ticket/904)

-   **[orm]**修复了自引用预加载，以便如果同一个映射实例出现在同一个结果集中的两个或多个不同的列集中，则无论是并非所有行都包含该集合的一组“热切”列。当在 join\_depth 打开的情况下获取结果时，这也会显示为 KeyError。[¶](#change-6705a0a328a243a3c879e94a69346ca4)

-   **[orm]**固定的错误，其中当 LIMIT 与继承映射器一起使用时，Query 不会将子查询应用于 SQL，其中只有在父映射器中才有加载器。[¶
    t2 \>](#change-8ce8cb627bff40401582485251bd4caf)

-   **[orm]**澄清了当您尝试更新()具有与会话中已存在的实例相同的身份关键字的实例时发生的错误消息。[¶](#change-a583ca54c9f72d5e381ee158389cc17b)

-   **[orm]**一些澄清和修复合并（实例，dont\_load =
    True）。修复了懒惰加载程序在返回的实例上被禁用的问题。此外，我们目前不支持合并其中未提交更改的实例，在使用 dont\_load
    =
    True 的情况下……现在会引发错误。这是由于合并给定实例的“已提交状态”以正确对应于新复制的实例以及其他已修改状态的复杂性。由于 dont\_load
    =
    True 的用例是缓存，因此给定的实例无论如何不应有任何未提交的更改。我们也复制实例而不使用任何事件，这样新会话上的'dirty'列表就不受影响。[¶](#change-765a4998bb1fb50421b5910813efbcc2)

-   **[orm]**fixed bug which could arise when using
    session.begin\_nested() in conjunction with more than one level deep
    of enclosing session.begin()
    statements[¶](#change-ea7de496771c635bee87d7670889f0ee)

-   **[orm]**修正 session.refresh()与实例具有自定义 entity\_name
    [¶](#change-688cfda7b6b1b358dcef128e1f80b4bb)

    参考文献：[＃914](http://www.sqlalchemy.org/trac/ticket/914)

### SQL [¶ T0\>](#change-0.4.2-sql "Permalink to this headline")

-   **[sql]**通用功能！我们引入一个已知 SQL 函数的数据库，例如 current\_timestamp，coalesce，并创建表示它们的显式函数对象。这些对象具有受约束的参数列表，可识别类型，并且可以按照特定于方言的方式进行编译。所以说 func.char\_length（“foo”，“bar”）会产生一个错误（太多的参数），func.coalesce（datetime.date（2007,10,5），datetime.date（2005,10,15））知道它的返回类型是 Date。我们目前只有几个函数，但会继续添加到系统[¶](#change-f840d15646468f91261fb9f4f827c464)中

    参考文献：[＃615](http://www.sqlalchemy.org/trac/ticket/615)

-   **[sql]**auto-reconnect support improved; a Connection can now
    automatically reconnect after its underlying connection is
    invalidated, without needing to connect() again from the engine.
    这允许绑定到单个连接的 ORM 会话不需要重新连接。在连接失效后，必须回滚连接上的打开事务，否则会引发错误。还修复了断开连接检测未被调用 cursor()，rollback()或 commit()的错误。[¶](#change-50091a15ff9c9366b36b0868152e0df2)

-   **[sql]**为 String 和 create\_engine()添加了新的标志，assert\_unicode
    =（True | False |'warn'|
    None）。对于 Unicode 类型的 create\_engine()和 String，'warn'，默认为 False 或无。当 True 时，导致所有 unicode 转换操作在将非 Unicode 字节串作为绑定参数传递时引发异常。'警告'会导致警告。强烈建议所有支持 unicode 的应用程序正确使用 Python
    unicode 对象（即 u'hello'而不是'hello'），以便数据准确地返回。[¶](#change-4abfbfe6bea22beedb689afde26eee55)

-   **[sql]**generation of “unique” bind parameters has been simplified
    to use the same “unique identifier” mechanisms as everything else.
    这不会影响用户代码，除非可能已针对生成的名称进行了硬编码的任何代码。生成的绑定参数现在具有“\_
    ”的形式，而之前只有同名的第二个绑定才具有此形式。[](#change-1943253ba506b5613bb311d47f20a9de)

-   **[sql]**select().as\_scalar() will raise an exception if the select
    does not have exactly one expression in its columns
    clause.[¶](#change-8295165b5c3dd3ddc3c1d71843d664ad)

-   **[sql]**bindparam() objects themselves can be used as keys for
    execute(), i.e. statement.execute({bind1:’foo’,
    bind2:’bar’})[¶](#change-6e780ec732e6e0f32ed07d926adb7257)

-   **[sql]**向 TypeDecorator，process\_bind\_param()和 process\_result\_value()添加了新的方法，该方法自动利用底层类型的处理。非常适合使用 Unicode 或 Pickletype。TypeDecorator 现在应该成为增强任何现有类型（包括其他 TypeDecorator 子类，如 PickleType）的行为的主要方式。[¶](#change-96927335ae179f9639f2658179eca869)

-   **[sql]**
    selectables（及其他）在其导出列集合中的两列根据名称冲突时将发出警告。[¶](#change-d16902bc09502cb5a78b696a5f86caf1)

-   **[sql]**表格仍然可以在 sqlite 中使用，firebird，模式名称只是被丢弃[¶](#change-a7fd85cad8879a7cb7a882408ae2fc00)

    参考文献：[＃890](http://www.sqlalchemy.org/trac/ticket/890)

-   **[sql]**changed the various “literal” generation functions to use
    an anonymous bind parameter.
    没有太多的变化，除了他们的标签现在看起来像“：param\_1”，“：param\_2”而不是“：literal”[¶](#change-2925ff88bfebf6c66313f6cf18859909)

-   **[sql]**列标签的格式为“tablename.columname”，即现在支持。[¶](#change-2ab31cbdc0db31fb85313f8aa8fd9480)

-   **[sql]**
    select()的 from\_obj 关键字参数可以是标量或列表。[¶](#change-8fa1b1ab3760497c5d0dedf5bc7e031e)

### 火鸟[¶ T0\>](#change-0.4.2-firebird "Permalink to this headline")

-   **[firebird] [backend]**确实反映了域名（部分修复）和 PassiveDefaults
    [¶](#change-296229733dda9c08bbcde17a5331e5fc)

    参考文献：[＃410](http://www.sqlalchemy.org/trac/ticket/410)

-   **[firebird] [3562]
    [backend]**恢复为使用默认 poolclass（为了测试目的，在 0.4.0 中设置为 SingletonThreadPool）[¶](#change-5c5bf54d072226185c9bcd8b439d9bed)

-   **[firebird]
    [backend]**将 func.length()映射到'char\_length'（在 Firebird 的旧版本中，可轻松覆盖 UDF'strlen'）[¶](#change-c4e420a3bd5661f308a26a6dbe3bc067)

### 杂项[¶ T0\>](#change-0.4.2-misc "Permalink to this headline")

-   **[dialects]** sqlite
    SLDate 类型不会错误地呈现日期时间或时间对象的“微秒”部分。[¶](#change-2c81613f5859b7c1f3ceca0a78b13cfd)

-   **[dialects]**

    神谕
    :   -   为 Oracle 增加了断开连接检测支持
        -   一些清理到二进制/原始类型，以便临时检测到 cx\_oracle.LOB

    [¶](#change-8ca793172781cfe8727359f0bb56604c)

    参考文献：[＃902](http://www.sqlalchemy.org/trac/ticket/902)

-   **[dialects]**

    MSSQL
    :   -   PyODBC 不再拥有一个全球性的“设定数量”。
        -   修复 autload 上的非身份整数 PK
        -   更好地支持 convert\_unicode
        -   pyodbc / adodbapi 的日期转换不太严格
        -   符合模式的表格/自动加载

    [¶](#change-e26463d0e09920a810721d5acec0fc1f)

    References: [\#824](http://www.sqlalchemy.org/trac/ticket/824),
    [\#839](http://www.sqlalchemy.org/trac/ticket/839),
    [\#842](http://www.sqlalchemy.org/trac/ticket/842),
    [\#901](http://www.sqlalchemy.org/trac/ticket/901)

0.4.1 [¶ T0\>](#change-0.4.1 "Permalink to this headline")
----------------------------------------------------------

发布于：2007 年 11 月 18 日

### ORM [¶ T0\>](#change-0.4.1-orm "Permalink to this headline")

-   **[orm]**eager loading with LIMIT/OFFSET applied no longer adds the
    primary table joined to a limited subquery of itself; the eager
    loads now join directly to the subquery which also provides the
    primary table’s columns to the result set. 这消除了使用 LIMIT /
    OFFSET 从所有急切加载的 JOIN。[¶](#change-0b89c1898d4084608e81d2938ee20609)

    参考文献：[＃843](http://www.sqlalchemy.org/trac/ticket/843)

-   **[orm]**session.refresh() and session.expire() now support an
    additional argument “attribute\_names”, a list of individual
    attribute keynames to be refreshed or expired, allowing partial
    reloads of attributes on an already-loaded
    instance.[¶](#change-594a0081d5108bf4ee29921c0a5a842e)

    参考文献：[＃802](http://www.sqlalchemy.org/trac/ticket/802)

-   **[orm]**将 op()运算符添加到了检测属性；即 User.name.op（'ilike'）（'％somename％'）[¶](#change-b28a496490baf96e53a35fd41141c45c)

    参考文献：[＃767](http://www.sqlalchemy.org/trac/ticket/767)

-   **[orm]**映​​射类现在可以定义具有任意语义的\_\_eq\_\_，\_\_hash\_\_和\_\_nonzero\_\_方法。orm 现在处理仅基于身份的所有映射实例。（例如'is'vs'=='）[¶](#change-eb31b9d3e5311a271dc3c49b5404c206)

    参考文献：[＃676](http://www.sqlalchemy.org/trac/ticket/676)

-   **[orm]**
    Mapper 上的“属性”访问器被删除；它现在会抛出一个信息异常，解释 mapper.get\_property()和 mapper.iterate\_properties
    [¶](#change-3f023f26f562df58ce90608560fd6504)

-   **[orm]**将 having()方法添加到 Query 中，以与 filter()附加到 WHERE 子句相同的方式将 HAVING 应用于生成的语句。[¶](#change-2fc98bef8342a30df5eaf8d717ab428d)

-   **[orm]**The behavior of query.options() is now fully based on
    paths, i.e. an option such as eagerload\_all(‘x.y.z.y.x’) will apply
    eagerloading to only those paths, i.e. and not ‘x.y.x’;
    eagerload(‘children.children’) applies only to exactly two-levels
    deep, etc.[¶](#change-1ca51b23a65e7b311c38e71e4f06f672)

    参考文献：[＃777](http://www.sqlalchemy.org/trac/ticket/777)

-   **[orm]**PickleType will compare using == when set up with
    mutable=False, and not the is operator.
    要使用是或任何其他比较器，请使用 PickleType（comparator =
    my\_custom\_comparator）发送自定义比较函数。[¶](#change-25697ecfe693193b2646032ae6cbe5e3)

-   **[orm]**query doesn’t throw an error if you use distinct() and an
    order\_by() containing UnaryExpressions (or other)
    together[¶](#change-6541ab9074117cd48928f7885253addf)

    参考文献：[＃848](http://www.sqlalchemy.org/trac/ticket/848)

-   **[orm]**order\_by() expressions from joined tables are properly
    added to columns clause when using
    distinct()[¶](#change-4f9647deaa363941af6a3cc05cd1f193)

    参考文献：[＃786](http://www.sqlalchemy.org/trac/ticket/786)

-   **[orm]**固定错误，其中 Query.add\_column()不接受类绑定属性作为参数；如果将一个无效参数发送到 add\_column()（在 instances()时间），则查询也会引发错误[¶](#change-24e4c45db8fecf131cab8c0a13b7dbed)

    参考文献：[＃858](http://www.sqlalchemy.org/trac/ticket/858)

-   **[orm]**added a little more checking for garbage-collection
    dereferences in InstanceState.\_\_cleanup() to reduce “gc ignored”
    errors on app shutdown[¶](#change-8a9ee44baa74c1b5e3bd072e563eb7c4)

-   **[orm]**会话 API 已经固化：[¶](#change-a42838089d8927d06dc3e4f5fb731b84)

-   **[orm]**
    session.save()是已经存在的对象的错误[¶](#change-5e08c60d85b9c39cc11a409fafc3424f)

    参考文献：[＃840](http://www.sqlalchemy.org/trac/ticket/840)

-   **[orm]**
    session.delete()是*不是*持久对象的错误。[¶](#change-4869e0999f48ab540716a33356319094)

-   **[orm]**session.update() and session.delete() raise an error when
    updating or deleting an instance that is already in the session with
    a different identity.[¶](#change-e629f6ef18ff5d02c5e58f3269d83bb7)

-   **[orm]**The session checks more carefully when determining “object
    X already in another session”; e.g. if you pickle a series of
    objects and unpickle (i.e. as in a Pylons HTTP session or similar),
    they can go into a new session without any
    conflict[¶](#change-01dbce273a2adf5114b01dc0b145907c)

-   **[orm]** merge()包含关键字参数“dont\_load =
    True”。设置此标志将导致合并操作不会响应传入的分离对象加载数据库中的任何数据，并且会接受传入的分离对象，就好像它已经存在于该会话中一样。使用它可以将来自外部缓存系统的分离对象合并到会话中。[¶](#change-70e068257ffe2a9509dde98014d7fc8f)

-   **[orm]**当属性分配给时，延迟列属性不再触发加载操作。在这些情况下，新分配的值将无条件存在于刷新的 UPDATE 语句中。[¶](#change-6ef45e3576f11236b5bc83eb98617664)

-   **[orm]**修复了重新分配集合子集时的截断错误（obj.relation =
    obj.relation [1：]）[¶](#change-91e4cc2655c18b9537f4d744bfdd2708)

    参考文献：[＃834](http://www.sqlalchemy.org/trac/ticket/834)

-   **[orm]**未定义的 backref 配置代码，在现有属性上引入的 backrefs 现在会引发错误[¶](#change-41c6f4041a8bb7bdfbc47fec3d053013)

    参考文献：[＃832](http://www.sqlalchemy.org/trac/ticket/832)

-   **[orm]**改进了 add\_property()等行为，固定涉及同义词/
    deferred。[¶](#change-759a3aea37ad25edb343df437295e6e6)

    参考文献：[＃831](http://www.sqlalchemy.org/trac/ticket/831)

-   **[orm]**修正了 clear\_mappers()行为，以便更好地清理它自己。[¶](#change-5d9a9be98d135fcb8ef55e33ae16b4e9)

-   **[orm]**Fix to “row switch” behavior, i.e. when an INSERT/DELETE is
    combined into a single UPDATE; many-to-many relations on the parent
    object update properly.[¶](#change-c43e29a204caeb3c86ea12bedc74a885)

    参考文献：[＃841](http://www.sqlalchemy.org/trac/ticket/841)

-   **[orm]**修正了关联代理的\_\_hash\_\_，这些集合是不可更改的，就像它们的可变 Python 对象一样。[¶](#change-ccf7e204c172dae174612768df596949)

-   **[orm]**为范围会话添加了 save\_or\_update，\_\_contains\_\_和\_\_iter\_\_方法的代理。[¶](#change-2754c6abcf835f7d57e9369b9cfdcd6a)

-   **[orm]**固定了非常难以复制的问题，其中 Query 的 FROM 子句可能会受到某些生成调用的污染[¶](#change-94bbc737fc90680c013c33b8fd5c6177)

    参考文献：[＃852](http://www.sqlalchemy.org/trac/ticket/852)

### SQL [¶ T0\>](#change-0.4.1-sql "Permalink to this headline")

-   **[sql]**
    bindparam()上的“shortname”关键字参数已被弃用。[¶](#change-c4010d5d99cc7a8ff9d77a8cf6a8aef4)

-   **[sql]**添加了包含运算符（生成“LIKE％％”子句）。[¶](#change-cc475e4294cf5bc311cbfa7da8a7cc8f)

-   **[sql]**anonymous column expressions are automatically labeled.
    例如选择（[x \* 5]）会产生“SELECT x \* 5 AS
    anon\_1”。这允许 labelname 出现在 cursor.description 中，然后可以适当地匹配结果列处理规则。（因为 text()表达式可能代表多列），所以我们不能可靠地使用位置跟踪来处理结果列匹配。[¶](#change-4d5450de721c9aeffc95905577b27182)

-   **[sql]**operator overloading is now controlled by TypeEngine
    objects - the one built-in operator overload so far is String types
    overloading ‘+’ to be the string concatenation operator.
    用户定义的类型也可以通过重写 adapt\_operator（self，op）方法来定义自己的运算符重载。[¶](#change-5378ee3b3457f069b4aece9be3205155)

-   **[sql]**untyped bind parameters on the right side of a binary
    expression will be assigned the type of the left side of the
    operation, to better enable the appropriate bind parameter
    processing to take
    effect[¶](#change-84a5f6328d01750340ded0b38bddf0b1)

    参考文献：[＃819](http://www.sqlalchemy.org/trac/ticket/819)

-   **[sql]**从大多数语句编译中删除正则表达式步骤。还修复了[¶](#change-1c04ab02a23376e994e8ae24241f0a56)

    参考文献：[＃833](http://www.sqlalchemy.org/trac/ticket/833)

-   **[sql]**Fixed empty (zero column) sqlite inserts, allowing inserts
    on autoincrementing single column
    tables.[¶](#change-843aea1d01efb76d3683d2d7c05850a3)

-   **[sql]**修正 text()子句的表达式转换；这修复了各种 ORM 方案，其中文本文本用于 SQL 表达式[¶](#change-b7662d8394714cbb6d9daa235d86c4b6)

-   **[sql]**删除了 ClauseParameters 对象；
    compiled.params 现在返回一个常规字典，以及 result.last\_inserted\_pa​​rams()/
    last\_updated\_pa​​rams()。[¶](#change-36a4d5696bd619c85b8b8b650728d842)

-   **[sql]**修正了 INSERT 语句 w.r.t.主键列上具有基于 SQL 表达式的默认生成器；
    SQL 表达式正常执行内联，但不会触发列的“后取”条件，对于那些通过 cursor.lastrowid
    [¶](#change-246ac6dc033a79f2373e3fc6a80fdfe8)提供的数据库

-   **[sql]**
    func。对象可以被腌制/取消剔除[¶](#change-4313d5275f28eb3f99349b58aad9a963)

    参考文献：[＃844](http://www.sqlalchemy.org/trac/ticket/844)

-   **[sql]**rewrote and simplified the system used to “target” columns
    across selectable expressions.
    在 SQL 方面，这由“对应列()”方法表示。ORM 很大程度上使用该方法来将表达式的元素“修改”为类似的别名表达式，以及将最初绑定到表的结果集列或可选择的别名“对应”表达式作为目标。新的重写功能具有完全一致和准确的行为。[¶](#change-530c7500b6d6596c5e44ff1bcc3bce10)

-   **[sql]**添加了一个字段（“info”），用于存储架构项目的任意数据[¶](#change-9ce2e2e3ce7ee6bc38d6391ca49d1bc1)

    参考文献：[＃573](http://www.sqlalchemy.org/trac/ticket/573)

-   **[sql]**
    Connections 上的“properties”集合已重命名为“info”以匹配模式的可写集合。访问仍然可以通过“属性”名称直到 0.5.
    [¶](#change-e82d8124e2cacd51fd60363bf86daeee)

-   **[sql]**使用 strategy
    ='threadlocal'时修正了 Transaction 上的 close()方法[¶](#change-6e152ccd5b3f9e3f7ee75b1efb1f7acd)

-   **[sql]**修复编译后的绑定参数，使其不会错误填充 None
    [¶](#change-74a921aec37d54b685b3772d6afe21c8)

    参考文献：[＃853](http://www.sqlalchemy.org/trac/ticket/853)

-   **[sql]**.\_execute\_clauseelement becomes a public method
    Connectable.execute\_clauseelement[¶](#change-d7e28424562953a96441f068c4371b86)

### 杂项[¶ T0\>](#change-0.4.1-misc "Permalink to this headline")

-   **[dialects]**增加了对 MaxDB 的实验性支持（版本\> =
    7.6.03.007）。[¶](#change-87d6ffbdea8e609cece2a7580f1cbfd8)

-   **[dialects]**
    oracle 现在将“DATE”反映为 OracleDateTime 列，而不是 OracleDate
    [¶](#change-914074ff8e5eed82fab96d0b8a6b71cc)

-   **[dialects]**增加了对 oracle
    table\_names()函数中模式名称的了解，修复了 metadata.reflect（schema
    ='someschema'）[¶](#change-ea8c17afee12829dee303f9a3b5e9e93)

    参考文献：[＃847](http://www.sqlalchemy.org/trac/ticket/847)

-   **[dialects]**用于选择功能的 MSSQL 匿名标签使确定性[¶](#change-bd6478eaa69e057034c6c987444e39a2)

-   **[dialects]**
    sqlite 会将“DECIMAL”反映为数字列。[¶](#change-538b138b4fd33c8a8761b3953aa54d96)

-   **[dialects]**使访问道检测更加可靠[¶](#change-1b89ee1a9467ff024e61a062369696f0)

    参考文献：[＃828](http://www.sqlalchemy.org/trac/ticket/828)

-   **[dialects]**将方言属性'preexecute\_sequences'重命名为'preexecute\_pk\_sequences'。一个属性 porxy 适用于使用旧名称的 out-of-tree 方言。[¶](#change-b559a79228b5f4bf95f4c9c0621d82e4)

-   **[dialects]**为未知类型的反射增加了测试覆盖率。修正了未知类型反射类型的 sqlite
    / mysql 处理。[¶](#change-cd70ea2a75cf0f0058a871da3c0a7381)

-   **[dialects]**增加了对于 mysql 方言的 REAL（对于开发 REAL\_AS\_FLOAT
    sql 模式的人）。[¶](#change-e8a0ddea13b9ebc8886d4b136d2b1d68)

-   **[dialects]**现在，没有参数的 mysql
    Float，MSFloat 和 MSDouble 产生无参数 DDL，例如'FLOAT'。[¶](#change-0f02a6b3d522bc191f30d77738ee5134)

-   **[misc]**删除未使用的 util.hash()。[¶](#change-e83c6ba370ca3384eed62f241d8b80d9)

0.4.0 [¶ T0\>](#change-0.4.0 "Permalink to this headline")
----------------------------------------------------------

发布时间：2007 年 10 月 17 日

-   （请参阅 0.4.0beta1 开始对 0.3 进行主要更改，以及[http://www.sqlalchemy.org/trac/wiki/WhatsNewIn04](http://www.sqlalchemy.org/trac/wiki/WhatsNewIn04)）[¶
    T2\>](#change-b4fc8b2d58a4d717e756adb83fde5498)

-   增加了对 Sybase 的支持（目前为止，mxODBC）[¶](#change-bcf3dff7b0aa6e5210dcc06d54677447)

    参考文献：[＃785](http://www.sqlalchemy.org/trac/ticket/785)

-   为 PostgreSQL 增加了部分索引支持。在索引上使用 postgres\_where 关键字。[¶](#change-25fce3a42aa163243a076187861b48a8)

-   基于字符串的查询参数解析/配置文件解析器理解布尔值的更广泛的字符串值[¶](#change-50353e4f1d87383f71322fa8c91dc8dc)

    参考文献：[＃817](http://www.sqlalchemy.org/trac/ticket/817)

-   如果另一侧的集合不包含该项目，则支持 noload 集合的 backref 移除对象操作不会失败[¶](#change-c14bc3996acddaff218f64dced993cbc)

    参考文献：[＃813](http://www.sqlalchemy.org/trac/ticket/813)

-   将\_\_len\_\_从“动态”集合中删除，因为它需要发出 SQL“count()”操作，因此迫使所有列表评估发出冗余 SQL
    [¶](#change-3fe165fcf8b210dd06e23fe29c90fdcf)

    参考文献：[＃818](http://www.sqlalchemy.org/trac/ticket/818)

-   inline optimizations added to locate\_dirty() which can greatly
    speed up repeated calls to flush(), as occurs with
    autoflush=True[¶](#change-fed60a94c48be9f1d4fbf64b773478a9)

    参考文献：[＃816](http://www.sqlalchemy.org/trac/ticket/816)

-   IdentifierPreprarer 的\_requires\_quotes 测试现在是基于正则表达式的。任何提供 legal\_characters 或 illegal\_initial\_characters 自定义集合的 out-of-tree 方言都需要移动到正则表达式或覆盖\_requires\_quotes。[¶](#change-6931e3874f7028b6166fbaee26c13735)

-   Firebird has supports\_sane\_rowcount and
    supports\_sane\_multi\_rowcount set to False due to ticket \#370
    (right way).[¶](#change-5a64dfccda02d75cc5a717a5d72f1d75)

-   

    Firebird 反射的改进和修复：
    :   -   现在，FBDialect 模仿 OracleDialect，关于 TABLE 和 COLUMN 名称的区分大小写（请参阅当前文件中的'case\_sensitive
            remotion'主题）。
        -   FBDialect.table\_names()不带系统表（票证：796）。
        -   FB 现在正确反映了 Column 的可空属性。

    [¶](#change-a9896a5318c3109f7c89af2ad2c36bc9)

-   Fixed SQL compiler’s awareness of top-level column labels as used in
    result-set processing; nested selects which contain the same column
    names don’t affect the result or conflict with result-column
    metadata.[¶](#change-7a9f394245eb8aa496bcd282b6cb9d91)

-   query.get() and related functions (like many-to-one lazyloading) use
    compile-time-aliased bind parameter names, to prevent name conflicts
    with bind parameters that already exist in the mapped
    selectable.[¶](#change-d558e9c84b1e5793e3c4a3c171f163af)

-   修正了三层和多层次的 select 和 deferred 继承加载（即没有 select\_table 的 abc 继承）。[¶](#change-05e3bf9bc8a5fbc5cb566b518f8c3d52)

    参考文献：[＃795](http://www.sqlalchemy.org/trac/ticket/795)

-   在 shard.py 中传递给 id\_chooser 的标识永远是一个列表。[¶](#change-5d0fab06b154a736d16cc1f5f05124d6)

-   无参数 ResultProxy.\_row\_processor()现在是类属性\_process\_row。[¶](#change-900edd4aa3ce5b35e0379abe1f1aceec)

-   增加了对 PostgreSQL 8.2
    +插入和更新返回值的支持。[¶](#change-a888d5a2b3097f6a24d949a8c8094ba0)

    参考文献：[＃797](http://www.sqlalchemy.org/trac/ticket/797)

-   PG reflection, upon seeing the default schema name being used
    explicitly as the “schema” argument in a Table, will assume that
    this is the user’s desired convention, and will explicitly set the
    “schema” argument in foreign-key-related reflected tables, thus
    making them match only with Table constructors that also use the
    explicit “schema” argument (even though its the default schema).
    换句话说，SA 假定用户在这种用法中是一致的。[¶](#change-737ba18b8c4d08ef01910aa20772d16a)

-   fixed sqlite reflection of
    BOOL/BOOLEAN[¶](#change-ebf15415b10e013bcf0d9a82f892a217)

    参考文献：[＃808](http://www.sqlalchemy.org/trac/ticket/808)

-   增加了对 MySQL 的 UPDATE 和 LIMIT 的支持。[¶](#change-f1c6c0df2c06bf883b72c36b13e92e75)

-   m2o 上的 null 外键不会触发 lazyload
    [¶](#change-efe5107a0d07dac76612b27de5b70784)

    参考文献：[＃803](http://www.sqlalchemy.org/trac/ticket/803)

-   oracle does not implicitly convert to unicode for non-typed result
    sets (i.e. when no TypeEngine/String/Unicode type is even being
    used; previously it was detecting DBAPI types and converting
    regardless). 应该修正[¶](#change-528c46ca19ca4d864d2acad507616b4c)

    参考文献：[＃800](http://www.sqlalchemy.org/trac/ticket/800)

-   修复长表/列名的匿名标签生成[¶](#change-77dbca629719cb4cb77e1ddf562e7d9a)

    参考文献：[＃806](http://www.sqlalchemy.org/trac/ticket/806)

-   Firebird dialect now uses SingletonThreadPool as
    poolclass.[¶](#change-220b2721e3178a042f4628ddf67103d4)

-   Firebird now uses dialect.preparer to format sequences
    names[¶](#change-a9a8ada8cf6f9e910f573eaa9489415b)

-   修复了 postgres 和多个两阶段事务的破坏情况。两阶段提交和回滚并不会像通常的 dbapi 提交/回滚那样自动以新事务结束。[¶](#change-3a7b59bf8fe3093a054925308b7f4799)

    参考文献：[＃810](http://www.sqlalchemy.org/trac/ticket/810)

-   为\_ScopedExt 映射器扩展添加了一个选项，不会在对象初始化时自动将新对象保存到会话中。[¶](#change-dcfcc254bf2beebefed7c884d53fdbbc)

-   修正了 Oracle 非 ansi 连接语法[¶](#change-5c1e6eaf781c2a9ecb4b8d604b4c12d7)

-   PickleType and Interval types (on db not supporting it natively) are
    now slightly faster.[¶](#change-2d010cff627c0048b473b58acfd31fc3)

-   为 Firebird 添加了浮点和时间类型（FBFloat 和 FBTime）。修正了用于 TEXT 和二进制类型的 BLOB
    SUB\_TYPE。[¶](#change-1aa7ff5a74776a60681a3dc879294a54)

-   更改了 in\_运算符的 API。in\_()现在接受一个参数，它是一个值序列或一个可选参数。传递值作为可变参数的旧 API 仍然有效，但不推荐使用。[¶](#change-90371ac2603990896e47a63773b4be24)

0.4.0beta6 [¶ T0\>](#change-0.4.0beta6 "Permalink to this headline")
--------------------------------------------------------------------

发布于：2007 年 9 月 27 日

-   默认情况下，会话标识映射现在*弱引用*，请使用 weak\_identity\_map =
    False 来使用常规字典。我们正在使用的弱字典是为了检测“脏”的实例而定制的，并且保持对这些实例的临时强引用，直到刷新变化为止。[¶](#change-1df819a6cf9fd245a16b40d9c188c60f)

-   Mapper compilation has been reorganized such that most compilation
    occurs upon mapper construction.
    这使我们对 mapper.compile()的调用更少，并允许基于类的属性强制编译（即 User.addresses
    ==
    7 将编译所有映射器；这是）。唯一需要注意的是，继承的映射器现在在构建时寻找它的继承映射器；因此继承关系中的映射器需要以继承顺序构建（无论如何，这应该是正常情况）。[¶](#change-1d1c0f14569b491f750569e9ee7529b3)

    参考文献：[＃758](http://www.sqlalchemy.org/trac/ticket/758)

-   将“FETCH”添加到 Postgres 检测到的关键字中，以指示结果行保留语句（即除了“SELECT”）。[¶](#change-b7cf4f4d67686ec87fdba236e7d68f25)

-   添加了 SQLite 保留关键字的完整列表，以便它们正确转义。[¶](#change-9547226b45b928b5e944366ec8a0ab93)

-   强化了 Query 的“紧急加载”别名的生成和 Query.instances()之间的关系，这些关键字实际上会抓取热切加载的行。如果别名不是由 EagerLoader 为该语句专门生成的，那么在获取行时 EagerLoader 不会生效。这样可以防止列被意外抓取，因为它们并非意味着这种情况，这可能会发生在文本 SQL 以及一些继承情况中。这一点尤其重要，因为列的“匿名别名”现在使用简单的整数计数来生成标签。[¶](#change-f4cba78c179582e4bb530a36c5e55152)

-   从 clauseelement.compile()中删除了“parameters”参数，替换为“column\_keys”。发送到 execute()的参数只与列名称存在的 insert
    / update 语句编译过程交互，但不与这些列的值相关。产生更一致的 execute
    /
    executemany 行为，在内部简化了一些事情。[¶](#change-066c676b077070c937c1d23f53d45e3a)

-   在 PickleType 中增加了'comparator'关键字参数。默认情况下，“可变”PickleType 使用它们的 dump()表示法对对象进行“深层比较”。但是这对字典不起作用。提供足够的\_\_eq
    \_\_()实现的 Pickled 对象可以使用“PickleType（comparator =
    operator.eq）”来设置。[¶](#change-a57972bf47c37142d2f8450ba8343433)

    参考文献：[＃560](http://www.sqlalchemy.org/trac/ticket/560)

-   新增 session.is\_modified（obj）方法；执行与在刷新操作中发生的相同的“历史”比较操作；设置 include\_collections
    =
    False 的结果与 flush 时确定是否为实例行发出 UPDATE 时所使用的结果相同。[¶](#change-86b7e1bcfc257a95dd46f409ad3ed7d4)

-   将序列添加了“模式”参数；当序列位于备用模式中时，将其与 Postgres /
    Oracle 一起使用。实施的一部分，应该修复。[¶](#change-3353f6e734c51856789b2c7c67e6ba70)

    参考文献：[＃584](http://www.sqlalchemy.org/trac/ticket/584)，[＃761](http://www.sqlalchemy.org/trac/ticket/761)

-   固定反映 mysql 枚举的空字符串。[¶](#change-1b5a20829be72cd57e395d53c965f562)

-   改变了 MySQL 方言使用旧的 LIMIT ，语法，而不是 LIMIT OFFSET
    ，用于使用 3.23 的人。[](#change-d3dde7998c563eec40c710cbada1d8af)
    T3\> T2\> T1\>

    参考文献：[＃794](http://www.sqlalchemy.org/trac/ticket/794)

-   Added ‘passive\_deletes=”all”’ flag to relation(), disables all
    nulling-out of foreign key attributes during a flush where the
    parent object is
    deleted.[¶](#change-9d4fe872e8b59bfeefb5183ab7684f9a)

-   内联执行的列缺省值和 onupdates 将为子查询和其他括号需求表达式添加括号[¶](#change-563c3cbf44802188d12788163d985e16)

-   The behavior of String/Unicode types regarding that they
    auto-convert to TEXT/CLOB when no length is present now occurs
    *only* for an exact type of String or Unicode with no arguments.
    如果使用 VARCHAR 或 NCHAR（String /
    Unicode 的子类）而没有长度，则它们将被方言解释为 VARCHAR /
    NCHAR；没有“魔术”转换发生在那里。这并不令人惊讶，特别是这有助于 Oracle 将基于字符串的绑定参数保存为 VARCHAR，而不是 CLOB。[¶](#change-12d3f310eb9663bf0ecfedbe0a47fbad)

    参考文献：[＃793](http://www.sqlalchemy.org/trac/ticket/793)

-   修复 ShardedSession 与延迟列一起工作[¶](#change-f455b93bc401877daa0ba14fb70ec408)

    参考文献：[＃771](http://www.sqlalchemy.org/trac/ticket/771)

-   User-defined shard\_chooser() function must accept “clause=None”
    argument; this is the ClauseElement passed to
    session.execute(statement) and can be used to determine correct
    shard id (since execute() doesn’t take an
    instance.)[¶](#change-955f25fb13ad169f392d6f1a17e804ac)

-   Adjusted operator precedence of NOT to match ‘==’ and others, so
    that \~(x y) produces NOT (x y), which is better compatible with
    older MySQL versions.. 这不适用于像〜0.3 那样的“〜（x ==
    y）”，因为〜（x == y）编译为“x！=
    y”，但仍然适用于像 BETWEEN 这样的运算符。[¶\< /
    T0\>](#change-e2bee4b5e6c30d433fb8a7e4ae81663a)

    参考文献：[＃764](http://www.sqlalchemy.org/trac/ticket/764)

-   其他门票：,null,。[¶](#change-72a7f7aec701fc5fbf615366585da0c8)

    References: [\#757](http://www.sqlalchemy.org/trac/ticket/757),
    [\#768](http://www.sqlalchemy.org/trac/ticket/768),
    [\#779](http://www.sqlalchemy.org/trac/ticket/779),
    [\#728](http://www.sqlalchemy.org/trac/ticket/728)

0.4.0beta5 [¶ T0\>](#change-0.4.0beta5 "Permalink to this headline")
--------------------------------------------------------------------

没有发布日期

-   连接池修复；
    beta4 的性能更好，但修复了“连接溢出”和其他存在的 bug（如）。[¶](#change-8d770fefd20726d046539230358cf916)

    参考文献：[＃754](http://www.sqlalchemy.org/trac/ticket/754)

-   修正了从自定义继承条件中确定合适的同步子句的错误。[¶](#change-e4680818ac93f4cde5adbfd53ec55dce)

    参考文献：[＃769](http://www.sqlalchemy.org/trac/ticket/769)

-   针对 QueuePool 大小/溢出扩展'engine\_from\_config'强制[¶](#change-2c611a783379e4c4bbf0acadbc498ce5)

    参考文献：[＃763](http://www.sqlalchemy.org/trac/ticket/763)

-   mysql 视图可以再次被反映出来。[¶](#change-a02fe61d853e712245ea2fa9e3cf8182)

    参考文献：[＃748](http://www.sqlalchemy.org/trac/ticket/748)

-   AssociationProxy 现在可以使用自定义的 getter 和 setter。[¶](#change-43e8bb9fe2e39b744b2a496fb3f5ac6f)

-   Fixed malfunctioning BETWEEN in orm
    queries.[¶](#change-80a35e2d5a32af8ce1f16c72e2776cc9)

-   固定 OrderedProperties 酸洗[¶](#change-99c2f326bb6523f16579523728bf307c)

    参考文献：[＃762](http://www.sqlalchemy.org/trac/ticket/762)

-   SQL-expression defaults and sequences now execute “inline” for all
    non-primary key columns during an INSERT or UPDATE, and for all
    columns during an executemany()-style call. inline
    =任何插入/更新语句上的 True 标志也会强制执行单个 execute()的相同行为。result.postfetch\_cols()是以前的单个插入或更新语句包含 SQL 端默认表达式的列的集合。[¶](#change-3a2a0bf70aa28afcbafdd2992791f31d)

-   修正了 PG 的 executemany()行为。[¶](#change-ffca3b05b1018517a278afe82229a29c)

    参考文献：[＃759](http://www.sqlalchemy.org/trac/ticket/759)

-   对于没有默认值的主键列，postgres 反映表的 autoincrement =
    False。[¶](#change-3a401edfbc7ebb4442cd5e73acb6d51e)

-   postgres no longer wraps executemany() with individual execute()
    calls, instead favoring performance.
    由于 psycopg2 不报告 executemany()的正确行数，因此使用 PG 禁用“使用 executemany”的已删除项目的“rowcount”/“concurrency”。[¶](#change-ba060cbd953a2ef43be8d18f2fd83983)

-   **[tickets] [fixed]** [¶](#change-45d7d861a3365452e7c1d9a6ec39b83c)

    参考文献：[＃742](http://www.sqlalchemy.org/trac/ticket/742)

-   **[tickets] [fixed]** [¶](#change-45d7d861a3365452e7c1d9a6ec39b83c)

    参考文献：[＃748](http://www.sqlalchemy.org/trac/ticket/748)

-   **[tickets] [fixed]** [¶](#change-45d7d861a3365452e7c1d9a6ec39b83c)

    参考文献：[＃760](http://www.sqlalchemy.org/trac/ticket/760)

-   **[tickets] [fixed]** [¶](#change-45d7d861a3365452e7c1d9a6ec39b83c)

    参考文献：[＃762](http://www.sqlalchemy.org/trac/ticket/762)

-   **[tickets] [fixed]** [¶](#change-45d7d861a3365452e7c1d9a6ec39b83c)

    参考文献：[＃763](http://www.sqlalchemy.org/trac/ticket/763)

0.4.0beta4 [¶ T0\>](#change-0.4.0beta4 "Permalink to this headline")
--------------------------------------------------------------------

发布时间：2007 年 8 月 22 日星期三

-   当你从'sqlalchemy import
    \*'中清理完名字空间时：[¶](#change-f4d29dc7b02b99ed3260ef11c8fe9840)

-   '表'和'列'不再导入。它们通过直接引用（如'sql.table'和'sql.column'）或 sql 包中的 glob 导入保持可用。当刚开始使用 SQLAlchemy 时，意外地使用 sql.expressions.table 代替 schema.Table 太容易了，同样也是列。[¶](#change-6890b669137922b1f67f9c81c9e393cd)

-   Internal-ish classes like ClauseElement, FromClause, NullTypeEngine,
    etc., are also no longer imported into your
    namespace[¶](#change-2663410f9071b570a253c86fb4d09031)

-   The ‘Smallinteger’ compatibility name (small i!)
    不再导入，但现在仍保留在 schema.py 中。SmallInteger（大我！）仍然是导入的。[¶](#change-487de14a19636219ee9867528df4aee5)

-   The connection pool uses a “threadlocal” strategy internally to
    return the same connection already bound to a thread, for
    “contextual” connections; these are the connections used when you do
    a “connectionless” execution like insert().execute().
    这就像“threadlocal”引擎策略的“部分”版本，但没有线程本地事务部分。我们希望它可以减少连接池开销以及数据库使用量。但是，如果它证明以负面方式影响稳定性，我们会马上回滚。[¶](#change-8b98efdb7b0519850778b7118b3c2e6d)

-   修复绑定参数处理，使得“假”值（如空白字符串）仍然得到处理/编码。[¶](#change-acf296f37f99428d8f44ec69e3890aa0)

-   Fix to select() “generative” behavior, such that calling column(),
    select\_from(), correlate(), and with\_prefix() does not modify the
    original select object[¶](#change-401edf6c4209442b8a393d710989444a)

    参考文献：[＃752](http://www.sqlalchemy.org/trac/ticket/752)

-   Added a “legacy” adapter to types, such that user-defined TypeEngine
    and TypeDecorator classes which define convert\_bind\_param() and/or
    convert\_result\_value() will continue to function.
    还支持调用这些方法的 super()版本。[¶](#change-954a4eace190252f4ee50417a801d00c)

-   添加了 session.prune()，修剪了会话中缓存的实例，这些实例不再在别处引用。（用于强引用身份映射的实用程序）。[¶](#change-044df9e23478cf328cff40782234c4f6)

-   为 Transaction 添加了 close()方法。如果是最外层的事务，则使用回滚关闭事务，否则只会在不影响外层事务的情况下结束。[¶](#change-8d0b91ca4fcfc0ad6d3b9cd553567fba)

-   事务性和非事务性会话与绑定连接更好地集成；
    close()将确保连接事务状态与绑定到 Session 之前的连接事务状态相同。[¶](#change-dfe299aa8afc78c5d63d67f689f3815a)

-   已修改的 SQL 运算符函数为模块级运算符，允许 SQL 表达式为 pickleable。[¶](#change-dc59c0230dc589d9da18567e46119d37)

    参考文献：[＃735](http://www.sqlalchemy.org/trac/ticket/735)

-   对 mapper 类的小调整.\_\_ init\_\_允许 Py2.6 对象.\_\_ init
    \_\_()行为。[¶](#change-91eb02a84f178101962db7b783aa809a)

-   修正了 select()[¶](#change-ff553271888137520292109b17a04720)的'prefix'参数

-   Connection.begin()不再接受 nested =
    True，这个逻辑现在全部在 begin\_nested()中。[¶](#change-e4222fd4e054c51dc51cbb0643020566)

-   修复了涉及级联的新“动态”关系加载器[¶](#change-678e4addb4b749e32601ce1f3fa4f806)

-   **[tickets] [fixed]** [¶](#change-4af6f88998dc3d47b1e2144c8709f9cc)

    参考文献：[＃735](http://www.sqlalchemy.org/trac/ticket/735)

-   **[tickets] [fixed]** [¶](#change-4af6f88998dc3d47b1e2144c8709f9cc)

    参考文献：[＃752](http://www.sqlalchemy.org/trac/ticket/752)

0.4.0beta3 [¶ T0\>](#change-0.4.0beta3 "Permalink to this headline")
--------------------------------------------------------------------

发布日期：2007 年 8 月 16 日

-   SQL 类型优化：[¶](#change-f5cf19f3f7be3f62710b12ab0c1a7f21)

-   新的性能测试显示，结合质量插入/质量选择测试的功能调用少于相同测试运行的 0.3％。[¶](#change-75d0b6d4c9572877034c53d512674299)

-   结果集迭代的一般性能提升约为 10-20％。[¶](#change-b75224a719e77f997a148bc85a071410)

-   In types.AbstractType, convert\_bind\_param() and
    convert\_result\_value() have migrated to callable-returning
    bind\_processor() and result\_processor() methods.
    如果不返回可调用对象，则不会调用前/后处理函数。[¶](#change-ef940138c452b9816295b5d82d66f548)

-   Hooks added throughout base/sql/defaults to optimize the calling of
    bind aram/result processors so that method call overhead is
    minimized.[¶](#change-c35fd87db1a5b5f45a1bf543d34cd61b)

-   为 executemany()方案添加了支持，以便不需要的“最后一行 id”逻辑无法启动，参数不会被过度遍历。[¶](#change-c8f92244fa634dc13e7327afd269b6b4)

-   将'inherit\_foreign\_keys'arg 添加到 mapper()。[¶](#change-17bd7748986ad2bd56cfce9a8078756b)

-   在 sqlite 中增加了对字符串日期传递的支持。[¶](#change-dba458ce8601c7fccb26c149512fbe0d)

-   **[tickets] [fixed]** [¶](#change-54e4755a0af97b6ee1bd86616e80216d)

    参考文献：[＃738](http://www.sqlalchemy.org/trac/ticket/738)

-   **[tickets] [fixed]** [¶](#change-54e4755a0af97b6ee1bd86616e80216d)

    参考文献：[＃739](http://www.sqlalchemy.org/trac/ticket/739)

-   **[tickets] [fixed]** [¶](#change-54e4755a0af97b6ee1bd86616e80216d)

    参考文献：[＃743](http://www.sqlalchemy.org/trac/ticket/743)

-   **[tickets] [fixed]** [¶](#change-54e4755a0af97b6ee1bd86616e80216d)

    References: [\#744](http://www.sqlalchemy.org/trac/ticket/744)

0.4.0beta2 [¶ T0\>](#change-0.4.0beta2 "Permalink to this headline")
--------------------------------------------------------------------

发布时间：2007 年 8 月 14 日

### 预言[¶ T0\>](#change-0.4.0beta2-oracle "Permalink to this headline")

-   **[oracle] [improvements.]**在 LOAD DATA
    INFILE 之后自动提交给 mysql。[¶](#change-27a03f85e379bb466ed82ab2bae62c14)

-   **[oracle]
    [improvements.]**已经添加了一个基本的 SessionExtension 类，允许用户定义的功能在 flush()，commit()和 rollback()边界发生。[¶](#change-2bfda89d7a3397e856da817c3ebe21ef)

-   **[oracle]
    [improvements.]**添加了 engine\_from\_config()函数，以帮助从.ini 样式配置文件中创建 create\_engine()。[¶](#change-eead32c9c30ad838d3dd8335b30c3cc5)

-   **[oracle]
    [improvements.]**base\_mapper()变成一个纯属性。[¶](#change-b0bb14e6d31421d0f6c217f9639275b0)

-   **[oracle]
    [improvements.]**session.execute()和 scalar()可以使用给定的 ClauseElement 来搜索要绑定的表。[¶](#change-15ded3b2513f94c39817cee6f52b785b)

-   **[oracle]
    [improvements.]**会话使用绑定自动从映射器推断表，还使用 base\_mapper，以便继承层次结构自动绑定。[¶](#change-25c6fb3d43b7dc1f4e87ea3b94d97e32)

-   **[oracle]
    [improvements.]**将 ClauseVisitor 遍历移回内联非递归。[¶](#change-c8b69249d8076c0cd3f9d71973a0c16f)

### 杂项[¶ T0\>](#change-0.4.0beta2-misc "Permalink to this headline")

-   **[tickets] [fixed]** [¶](#change-7f72c630ecf1937ef9e22932a61de352)

    参考文献：[＃730](http://www.sqlalchemy.org/trac/ticket/730)

-   **[tickets] [fixed]** [¶](#change-7f72c630ecf1937ef9e22932a61de352)

    参考文献：[＃732](http://www.sqlalchemy.org/trac/ticket/732)

-   **[tickets] [fixed]** [¶](#change-7f72c630ecf1937ef9e22932a61de352)

    参考文献：[＃733](http://www.sqlalchemy.org/trac/ticket/733)

-   **[tickets] [fixed]** [¶](#change-7f72c630ecf1937ef9e22932a61de352)

    参考文献：[＃734](http://www.sqlalchemy.org/trac/ticket/734)

0.4.0beta1 [¶ T0\>](#change-0.4.0beta1 "Permalink to this headline")
--------------------------------------------------------------------

发布日期：2007 年 8 月 12 日

### ORM [¶ T0\>](#change-0.4.0beta1-orm "Permalink to this headline")

-   **[orm]**速度！随着最近对 ResultProxy 的加速，大负载的函数调用总数大大减少。[¶](#change-73240e5294e8bb13d8b6f22802a98b27)

-   **[orm]**test/perf/masseagerload.py reports 0.4 as having the fewest
    number of function calls across all SA versions (0.1, 0.2, and
    0.3).[¶](#change-d6d237dcaf791d97938c5d2cb8ebcff0)

-   **[orm]**新的 collection\_class
    api 和实现。集合现在通过装饰而不是代理进行装饰。您现在可以拥有管理其自己成员资格的集合，并且您的类实例将直接显示在关系属性中。对于大多数用户来说，这些更改是透明的。[¶](#change-4a456a11201666fadfcbbfcb69bd3d5e)

    参考文献：[＃213](http://www.sqlalchemy.org/trac/ticket/213)

-   **[orm]**InstrumentedList (as it was) is removed, and relation
    properties no longer have ‘clear()’, ‘.data’, or any other added
    methods beyond those provided by the collection type.
    当然，您可以将它们添加到自定义类中。[¶](#change-ac7854a38e375ff1341e8a1b2a022235)

-   **[orm]** \_\_ setitem
    \_\_-现在就像现在的赋值一样，为现有值激发删除事件（如果有的话）。[¶](#change-bbebf85d0077a44cbe2ac84913a07d0b)

-   **[orm]**用作集合类的 dict-likes 不再需要更改\_\_iter\_\_语义 -
    itervalues()默认使用。这是一个向后不兼容的变化。[¶](#change-1a0c1db9fbcb17a7c2ba890ea4d9bdc1)

-   **[orm]**在大多数情况下，映射集合的子类化字典不再需要。orm.collections 通过指定的列或您选择的自定义函数提供了关键对象的固定实现。[¶](#change-12084d2d1417fb4bf746fd0665112f5f)

-   **[orm]**集合赋值现在需要一个兼容类型 -
    赋值 None 来清除一个集合或者将一个列表赋给一个 dict 集合现在会引发一个参数错误。[¶](#change-4db3f11e48432727edaead94e272e84a)

-   **[orm]**将 AttributeExtension 移动到接口，并且.delete 现在是.remove 事件方法签名也已被交换。[¶](#change-4431e2ff75387079894f22115c2f811e)

-   **[orm]**对 Query 进行大修：[¶](#change-e23a2954c9bd9fb1bde4aeceefe5d541)

-   **[orm]**不推荐使用所有 selectXXX 方法。生成方法现在是执行任务的标准方法，即 filter()，filter\_by()，all()，one()等。不赞成使用的方法是用新替代文件串入。[¶](#change-2503ad929a0fe516710bf9a1780fd348)

-   **[orm]**类级属性现在可用作查询元素...不再有'.c。'！“Class.c.propname”现在被“Class.propname”取代。支持所有子句运算符，以及更高级别的运算符，如用于标量属性的 Class.prop
    ==
    ，用于收集的 Class.prop.contains（）和 Class.prop.any（基于属性（全部也是否定的）。
    T2\> T1\>
    T0\>基于表格的列表达式以及通过'c'在映射类上安装的列当然仍然完全可用，并且可以与新属性自由混合。[¶](#change-1693eadbe7a1e73418dc29c3c9f5f383)

    参考文献：[＃643](http://www.sqlalchemy.org/trac/ticket/643)

-   **[orm]**删除了古老的 query.select\_by\_attributename()功能。[¶](#change-6a051d0e61d70a59ef63537773b2b738)

-   **[orm]**通过加载加载使用的别名逻辑已被推广，因此它也为 Query 添加了全自动别名支持。It’s
    no longer necessary to create an explicit Alias to join to the same
    tables multiple times; *even for self-referential relationships*.

    -   join()和 outerjoin()接受参数“aliased =
        True”。Yhis 使他们的连接建立在别名表上；随后对 filter()和 filter\_by()的调用会将所有表表达式（是的，使用原始映射表的实际表达式）转换为连接()的持续时间（即直到 reset\_joinpoint()或另一个连接）
        叫做）。
    -   join()和 outerjoin()接受参数“id = ”。 T0\>当与“aliased =
        True”一起使用时，可以通过 add\_entity（cls，id =
        ）引用该 id，以便即使它们来自别名，也可以选择已加入的实例。
    -   join()和 outerjoin()现在可以与自引用关系一起工作！使用“aliased =
        True”，你可以根据需要加入尽可能多的层次，例如 query.join（['children'，'children']，aliased
        = True）；过滤标准将针对最右边的连接表

    [¶](#change-f99a8e52f17864f9bdbcd276ea36c00e)

-   **[orm]**添加了 query.populate\_existing()，将查询标记为重新加载查询中接触的所有实例的所有属性和集合，包括加载实体的实例。[¶](#change-3f64e9fd6a4f77b6f36bda3cef6dc70c)

    参考文献：[＃660](http://www.sqlalchemy.org/trac/ticket/660)

-   **[orm]**新增 eagerload\_all()，允许 eagerload\_all（'x.y.z'）指定给定路径中所有属性的预加载。[¶](#change-d588f4a694c199bddb5e48ec5c218e25)

-   **[orm]**对 Session 进行大修：[¶](#change-a392d359411abd1fdd70fd91eee275f6)

-   **[orm]**“配置”一个名为“sessionmaker()”的会话的新函数。发送各种关键字参数给这个函数一次，返回一个新的类，它根据这个原型创建一个 Session。[¶](#change-b3a93d1308868a3fe8596d48cba80f96)

-   **[orm]**SessionTransaction removed from “public” API.
    您现在可以在 Session 本身上调用 begin()/ commit()/
    rollback()。[¶](#change-d081429019999b17e12865d77c0fe190)

-   **[orm]**会话也支持 SAVEPOINT 事务；调用 begin\_nested()。[¶](#change-d803dd5eca36864f998d6bec158fd580)

-   **[orm]**Session supports two-phase commit behavior when vertically
    or horizontally partitioning (i.e., using more than one engine).
    使用 twophase = True。[¶](#change-e2ebb386a75361f672fdc4c3c1aa6b9d)

-   **[orm]**Session flag “transactional=True” produces a session which
    always places itself into a transaction when first used.
    在 commit()，rollback()或 close()时，事务结束；但是从下一次使用开始。[¶](#change-9a345bfb97770dff468324795e2f74b4)

-   **[orm]**会话支持“autoflush =
    True”。这会在每个查询之前发出 flush()。与事务相结合使用，你可以保存()/
    update()然后查询，新的对象将在那里。在末尾使用 commit()（如果是非事务性的，则使用 flush()）来清除剩余的变化。[¶](#change-80cbb51c05d836b884ed1dc60c229fcb)

-   **[orm]**新的 scoped\_session()函数取代了 SessionContext 和 assignmapper。构建到“sessionmaker()”概念上，以产生一个 Session()构造返回线程本地会话的类。或者，将所有 Session 方法作为类方法调用，即 Session.save（foo）；
    Session.commit()。就像旧的“objectstore”日子一样。[¶](#change-7e824e1c9899b1998d251013e315f0d0)

-   **[orm]**为 Session 添加了新的“绑定”参数，以支持使用 sessionmaker()函数配置多个绑定。[¶](#change-750a1ea55476904ec3c0c11ffc957b4c)

-   **[orm]**添加了一个基本的 SessionExtension 类，允许在 flush()，commit()和 rollback()边界上执行用户定义的功能。[¶](#change-a7615aa7295fda4b76a5dc6b9ad79844)

-   **[orm]**
    dynamic\_loader()可用的基于查询的关系()。这是一个*可写*集合（支持 append()和 remove()），它也是一个实时查询对象。理想的处理非常大的集合，只需要部分加载。[¶](#change-9bd37da16a971ed83453125c1b474094)

-   **[orm]** flush() - 嵌入式行内 INSERT /
    UPDATE 表达式。将任何 SQL 表达式（如“sometable.c.column +
    1”）分配给实例的属性。在 flush()之后，映射器检测表达式并将其直接嵌入 INSERT 或 UPDATE 语句中；该属性在实例中被延迟，以便在下次访问它时加载新值。[¶](#change-f765c92d74ee81bbf71b692a95131664)

-   **[orm]**引入了一个基本的分片（水平缩放）系统。该系统使用修改的会话，该会话可以根据定义“分片策略”的用户定义函数在多个数据库之间分配读写操作。可以根据属性值，循环方法或任何其他用户定义的系统在多个数据库中分发和查询实例及其依赖项。[¶](#change-e9bf598b4653d8e6c0b87142da0e83bd)

    参考文献：[＃618](http://www.sqlalchemy.org/trac/ticket/618)

-   **[orm]**
    Eager 装载已得到增强，可以在更多地方实现更多连接。它现在可以在任意深度上沿着自我指涉和周期性结构发挥作用。加载循环结构时，在 relation()上指定“join\_depth”，表示您希望表加入自己的次数；每个级别都有一个不同的表别名。别名名称本身是在编译时使用简单的计数方案生成的，并且在眼睛上更容易，当然也是完全确定性的。[¶](#change-a02e26a19bf5a4351869a565aed6dbd4)

    参考文献：[＃659](http://www.sqlalchemy.org/trac/ticket/659)

-   **[orm]**添加了复合列属性。这允许您在使用 ORM 时创建一个由多个列表示的类型。新类型的对象在查询表达式，比较，query.get()子句等中是完全可用的。并且就好像他们是常规的单列标量……除非他们不是！在映射器的“属性”字典中使用函数 composite（cls，\*
    columns），并将 cls 的实例创建/映射到单个属性，由与\*列对应的值组成。[¶](#change-3ee39648a350e0ce7f6e88a460ef4222)

    参考文献：[＃211](http://www.sqlalchemy.org/trac/ticket/211)

-   **[orm]**改进了对具有相关子查询的自定义 column\_property()属性的支持，现在可以更好地加载现有的[¶](#change-5e44b305ff3b453bab31a4f4dd315202)

-   **[orm]**Primary key “collapse” behavior; the mapper will analyze
    all columns in its given selectable for primary key “equivalence”,
    that is, columns which are equivalent via foreign key relationship
    or via an explicit inherit\_condition.
    主要用于连接表继承方案，其中继承表中的不同名为 PK 列的应该“折叠”为单值（或更少值）的主键。修复诸如。[¶](#change-16479493bb7436bccac47ec4d52aa7ab)之类的内容

    参考文献：[＃611](http://www.sqlalchemy.org/trac/ticket/611)

-   **[orm]**连接表继承现在将仅针对连接的根表生成所有继承类的主键列。这意味着根表中的每一行都不同于单个实例。如果由于某种罕见的原因，这是不可取的，那么在各个映射器上显式的 primary\_key 设置将覆盖它。[¶](#change-8b14a583258b389d8befb88ffab4616e)

-   **[orm]**When “polymorphic” flags are used with joined-table or
    single-table inheritance, all identity keys are generated against
    the root class of the inheritance hierarchy; this allows query.get()
    to work polymorphically using the same caching semantics as a
    non-polymorphic get.
    请注意，这目前不适用于具体的继承。[¶](#change-5ecb81bd3049827ea00f874dff8a47e2)

-   **[orm]**辅助继承加载：多态映射器可以在没有
    select\_table 参数的情况下构造*。*继承其初始加载中不表示的映射器将立即发出第二个 SQL 查询，每个实例一次（即对于大型列表不是很有效），以加载剩余列。[¶](#change-b92f42ac37b868e4e25064ca4b5d334d)

-   **[orm]**Secondary inheritance loading can also move its second
    query into a column-level “deferred” load, via the
    “polymorphic\_fetch” argument, which can be set to ‘select’ or
    ‘deferred’[¶](#change-e17dea4885205655b3c0e9dc601c5577)

-   **[orm]**现在可以使用 include\_columns /
    exclude\_columns 仅将可用的可选列的子集映射到映射器属性上。[¶](#change-ba1a26695302fe5a0797ba0c2382d86e)

    参考文献：[＃696](http://www.sqlalchemy.org/trac/ticket/696)

-   **[orm]**添加了 undefer\_group()MapperOption，设置一组由“group”加入的“deferred”列作为“undeferred”加载。[¶](#change-d0fafbe316e5579935f88cf76fc3be57)

-   **[orm]**Rewrite of the “deterministic alias name” logic to be part
    of the SQL layer, produces much simpler alias and label names more
    in the style of
    Hibernate[¶](#change-c76aef44f5e7e8717c85b529552921fa)

### SQL [¶ T0\>](#change-0.4.0beta1-sql "Permalink to this headline")

-   **[sql]**速度！子句编译以及 SQL 结构的机制已经被精简和简化到了显着的程度，对 0.3 的语句构建/编译开销提高了 20-30％。[¶](#change-194d03e759795cb2ff68bbe9af23b306)

-   **[sql]**所有“type”关键字参数，如 bindparam()，column()，Column()和 func 的关键字参数()，重命名为“type\_”。
    T2\>这些对象仍将其“type”属性命名为“type”。[¶](#change-78c937a453ae2a2e9d60a9d7a1b498ac)

-   **[sql]**case\_sensitive=(True|False) setting removed from schema
    items, since checking this state added a lot of method call overhead
    and there was no decent reason to ever set it to False.
    表和列名都是小写，将被视为不区分大小写（是的，我们也调整了 Oracle 的大写样式）。[¶](#change-52f227bbb5a90b801adc6ecfd0cc6e3a)

### MySQL 的[¶ T0\>](#change-0.4.0beta1-mysql "Permalink to this headline")

-   **[mysql]**通过反射加载的表名和列名现在是 Unicode。[¶](#change-c9ff316cda3e7c6e32e67deee9bdb175)

-   **[mysql]**现在支持所有标准列类型，包括 SET。[¶](#change-4db25c57037e2e33e840cb086dca3781)

-   **[mysql]**现在可以在一次往返中执行表反射。[¶](#change-5117b0e81758578c4222aa8bbd429983)

-   **[mysql]**现在支持 ANSI 和 ANSI\_QUOTES
    sql 模式。[¶](#change-a5b4e4cd9830ca04727e6cc01578d944)

-   **[mysql]**索引现在反映出来。[¶](#change-3b4260991961474e8042e1a66c9f73b0)

### 预言[¶ T0\>](#change-0.4.0beta1-oracle "Permalink to this headline")

-   **[oracle]**添加了对 OUT 参数的非常基本的支持；使用 sql.outparam（name，type）来设置一个 OUT 参数，就像 bindparam()；执行后，值可通过 result.out\_parameters 字典获得。[¶](#change-cf0060d4bbf9e676c4a7c5beb5f02382)

    参考文献：[＃507](http://www.sqlalchemy.org/trac/ticket/507)

### 杂项[¶ T0\>](#change-0.4.0beta1-misc "Permalink to this headline")

-   **[transactions]**添加了对事务的上下文管理器（带语句）支持。[¶](#change-ef7a1ed2659338f4b08899b9caaab99b)

-   **[transactions]**添加了对两阶段提交的支持，到目前为止可以使用 mysql 和 postgres。[¶](#change-c77644da7acda73068dc7396e5f398af)

-   **[transactions]**增加了一个使用保存点的子事务实现。[¶](#change-df709470ae31b3f45008bbaa141d6d2c)

-   **[transactions]**增加了对保存点的支持。[¶](#change-8ade1ccb1059d3677b8b76a06a346099)

-   **[metadata]**可以从数据库 en-masse 中反映表，而无需事先声明它们。MetaData（engine，reflect
    =
    True）会加载数据库中的所有表，或者使用 metadata.reflect()进行更好的控制。[¶](#change-57d0fe83f069aa4fcd55bfbfe003c8f0)

-   **[metadata]** DynamicMetaData 已重命名为 ThreadLocalMetaData
    [¶](#change-c614e9a639adda152c6ab95d984bf7d5)

-   **[metadata]**
    ThreadLocalMetaData 构造函数现在不带参数。[¶](#change-ec45f540628c12b33729f88a7567a8d3)

-   **[metadata]** BoundMetaData 已被删除 -
    常规 MetaData 等同于[¶](#change-df3a2a76ccedf6eff1bec3c34ea2c717)

-   **[metadata]**数字和浮点类型现在有一个“asdecimal”标志；对于数字，默认为 True，对于 Float，默认为 False。当为 True 时，值以十进制形式返回。当 False 时，值返回为 float()。True
    /
    False 的缺省值已经是 PG 和 MySQL 的 DBAPI 模块的行为。[¶](#change-91306d19b451219b417b42a60215a684)

    参考文献：[＃646](http://www.sqlalchemy.org/trac/ticket/646)

-   **[metadata]**新的 SQL 运算符实现，它从表达式结构中移除所有硬编码的运算符并将它们转移到编译中；允许操作员编译更大的灵活性；例如，“+”在字符串上下文中使用时编译为“||”，或者在 MySQL 上使用“concat（a，b）”；而在数字上下文中则编译为“+”。修复。[¶
    T0\>](#change-08e4ad114c618cb250f9f7dfd398ee15)

    参考文献：[＃475](http://www.sqlalchemy.org/trac/ticket/475)

-   **[metadata]**“匿名”别名和标签名称现在在 SQL 编译时以完全确定性的方式生成...不再是随机的十六进制 ID
    [¶](#change-b3b40957f331feb3c0753ba57969930d)

-   **[metadata]**对 SQL 元素（ClauseElement）的重要架构检修。所有元素都有一个共同的“可变性”框架，允许采用一致的方法对元素进行就地修改以及生成行为。提高 ORM 的稳定性，从而大量使用 SQL 表达式的突变。[¶](#change-e48f6937efaa01d2cb93a212c539a175)

-   **[metadata]**select() and union()’s now have “generative” behavior.
    像 order\_by()和 group\_by()这样的方法返回一个*新的*实例 -
    原始实例保持不变。非生成方法仍然存在。[¶](#change-14a7a270d71f45154959854f228c79f8)

-   **[metadata]**The internals of select/union vastly simplified- all
    decision making regarding “is subquery” and “correlation” pushed to
    SQL generation phase.
    select()元素现在*从不*被它们的封闭容器或任何方言的编译过程所突变[¶](#change-b2f095c257ecd4fc1b70ea9343fab060)

    参考文献：[＃569](http://www.sqlalchemy.org/trac/ticket/569)，[＃52](http://www.sqlalchemy.org/trac/ticket/52)

-   **[metadata]** select（scalar =
    True）参数已弃用；使用 select（..）。as\_scalar()。得到的对象服从完整的“列”接口，并在表达式中播放更好。[¶](#change-cd01f4b5a2b4d78a16a7b4d48f5c73f0)

-   添加 select()。with\_prefix（'foo'）允许在 SELECT
    [¶](#change-10b500c2c9cba9a5927217ff7420f2b0)的 columns 子句之前放置任何关键字集合。**[metadata]**

    参考文献：[＃504](http://www.sqlalchemy.org/trac/ticket/504)

-   **[metadata]**增加了对行[]
    [¶](#change-df8444af8624fed7a285c5b7bf482a29)的数组切片支持

    参考文献：[＃686](http://www.sqlalchemy.org/trac/ticket/686)

-   **[metadata]**结果集可以更好地尝试将 cursor.description 中存在的 DBAPI 类型与方言定义的 TypeEngine 对象进行匹配，然后将其用于结果处理。注意这只对文本 SQL 有效；构造的 SQL 语句总是有一个明确的类型映射。[¶](#change-071fcdfe4ff56a5b234d1de2137bbf1d)

-   **[metadata]**Result sets from CRUD operations close their
    underlying cursor immediately and will also autoclose the connection
    if defined for the operation; this allows more efficient usage of
    connections for successive CRUD operations with less chance of
    “dangling connections”.[¶](#change-5df181a5d5e28fb2cade70322001e596)

-   **[metadata]**列默认和 onupdate
    Python 函数（即传递给 ColumnDefault）可能需要零个或一个参数；一个参数是 ExecutionContext，您可以从中调用“context.parameters
    [someparam]”来访问附加到该语句的其他绑定参数值。用于执行的连接也可用，以便您可以预执行语句。[¶](#change-89948a9f39a2ae2cba3dc69fc35f2d88)

    参考文献：[＃559](http://www.sqlalchemy.org/trac/ticket/559)

-   **[metadata]**新增了“explcit”创建/删除/执行序列支持（即，您可以将“可连接”传递给序列中的每个方法）[¶](#change-3424c25ad26ee106ba392edc6c3a817c)

-   **[metadata]**在操作模式时更好地引用标识符[¶](#change-7bb1f65298c3ca1debf3d2f941ac1247)

-   **[metadata]**标准化无法定位类型的表反射行为；
    NullType 被替换，引发警告。[¶](#change-35fdc74c58ccab72b6a95ed3fd9c27bd)

-   **[metadata]** ColumnCollection（即表上的'c'属性）遵循“\_\_contains
    \_\_”的字典语义[¶](#change-91634a26453429e65ac127027572ca43)

    参考文献：[＃606](http://www.sqlalchemy.org/trac/ticket/606)

-   **[engines]**速度！结果处理和绑定参数处理的机制已被彻底改进，精简和优化，以尽可能少地发出方法调用。质量 INSERT 和质量行集迭代的台架测试显示，0.4 的速度比 0.3 快两倍，使用的函数调用次数减少了 68％。[¶](#change-c2feef689fd707ec3da5f884a6aa2987)

-   **[engines]**You can now hook into the pool lifecycle and run SQL
    statements or other logic at new each DBAPI connection, pool
    check-out and check-in.[¶](#change-dbcb4c5e8906eb7ab54649e1e2eee3e6)

-   **[engines]**连接获得一个.properties 集合，其内容范围为基础 DBAPI 连接的生命周期[¶](#change-fd980057fb18ce87420a619497401906)

-   **[engines]**从池中删除了 auto\_close\_cursors 和 disallow\_open\_cursors 参数；由于游标通常由 ResultProxy 和 Connection 关闭，因此减少开销。[¶](#change-7db700fb15caca564e6d1b470ddbf1c7)

-   **[extensions]**
    proxyengine 暂时被移除，等待实际工作替换。[¶](#change-3b532a60bc0029ec354daf934d3a927a)

-   **[extensions]** SelectResults 已被 Query 取代。SelectResults /
    SelectResultsExt 仍然存在，但只是返回一个稍微修改的 Query 对象以实现向后兼容。来自 SelectResults 的 join\_to()方法不再存在，需要使用 join()。[¶](#change-4365514b9b0ac1a9bf2782c1798256a6)

-   **[postgres]**添加了使用 postgres 数组数据类型的 PGArray 数据类型。[¶](#change-bf48335461a856fcc94af29e957c22d2)


