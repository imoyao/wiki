---
title: changelog_07
date: 2021-02-20 22:41:29
permalink: /pages/e6a555/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
0.7更新日志[¶](#changelog "Permalink to this headline")
=======================================================

0.7.11 [¶ T0\>](#change-0.7.11 "Permalink to this headline")
------------------------------------------------------------

没有发布日期

### ORM [¶ T0\>](#change-0.7.11-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug where list instrumentation would fail to
    represent a setslice of `[0:0]` correctly, which
    in particular could occur when using `insert(0, item)` with the association proxy.
    由于Python集合中的一些怪癖，使用Python
    3而不是2的可能性更大。[¶](#change-452dd931d596e8eff62a71b5f6d967bd)

    参考文献：[＃2807](http://www.sqlalchemy.org/trac/ticket/2807)

-   **[orm] [bug]**Fixed bug when a query of the form:
    `query(SubClass).options(subqueryload(Baseclass.attrname))`, where `SubClass` is a joined inh of
    `BaseClass`, would fail to apply the
    `JOIN` inside the subquery on the attribute
    load, producing a cartesian product.
    填充的结果仍然是正确的，因为额外的行只是被忽略了，所以这个问题可能会出现在应用程序正常工作时性能下降。[¶](#change-67c2029e6f187392003eec283687e00e)

    参考文献：[＃2699](http://www.sqlalchemy.org/trac/ticket/2699)

-   **[orm] [bug]**Fixed bug in unit of work whereby a
    joined-inheritance subclass could insert the row for the “sub” table
    before the parent table, if the two tables had no ForeignKey
    constraints set up between
    them.[¶](#change-70b9b9893c9cd22af7e63065e86830bc)

    参考文献：[＃2689](http://www.sqlalchemy.org/trac/ticket/2689)

-   **[orm] [bug]**Improved the error message emitted when a “backref
    loop” is detected, that is when an attribute event triggers a
    bidirectional assignment between two other attributes with no end.
    这种情况不仅发生在分配了错误类型的对象时，而且当某个属性被错误地配置为反向引用到现有的backref对时。[¶](#change-8a5e83498c9c0eded67638e01d96e699)

    参考文献：[＃2674](http://www.sqlalchemy.org/trac/ticket/2674)

-   **[orm] [bug]**A warning is emitted when a MapperProperty is
    assigned to a mapper that replaces an existing property, if the
    properties in question aren’t plain column-based properties.
    关系属性的替换很少（从来没有？）意图是什么，通常是指映射器错误配置。这也会警告，如果backref在继承关系（在0.8中是一个错误）在现有配置上进行自我配置，[¶](#change-efb22c6e4fe4f34fd6705e77ab5f9bfa)

    参考文献：[＃2674](http://www.sqlalchemy.org/trac/ticket/2674)

### 发动机[¶ T0\>](#change-0.7.11-engine "Permalink to this headline")

-   **[engine] [bug]**The regexp used by the [`make_url()`](core_engines.html#sqlalchemy.engine.url.make_url "sqlalchemy.engine.url.make_url")
    function now parses ipv6 addresses, e.g. surrounded by
    brackets.[¶](#change-005cb70429df3b19c76d850725f7a8b3)

    参考文献：[＃2851](http://www.sqlalchemy.org/trac/ticket/2851)

### SQL [¶ T0\>](#change-0.7.11-sql "Permalink to this headline")

-   **[sql]
    [bug]**固定回归到0.7.9，如果CTE的名称在多个FROM子句中被引用，那么它的名称可能不会被正确引用。[¶](#change-8c33bcb081690fa732e3cf2794eac4e3)

    参考文献：[＃2801](http://www.sqlalchemy.org/trac/ticket/2801)

-   **[sql] [bug] [cte]**Fixed bug in common table expression system
    where if the CTE were used only as an `alias()`
    construct, it would not render using the WITH
    keyword.[¶](#change-cbc2ad305d9de1b8db977dd167cdff57)

    参考文献：[＃2783](http://www.sqlalchemy.org/trac/ticket/2783)

-   **[sql] [bug]**Fixed bug in [`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")
    DDL where the “quote” flag from a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object would not be
    propagated.[¶](#change-558878ea1f3882a6457b6019765de96b)

    参考文献：[＃2784](http://www.sqlalchemy.org/trac/ticket/2784)

### 的PostgreSQL [¶ T0\>](#change-0.7.11-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**Added support for Postgresql’s traditional
    SUBSTRING function syntax, renders as “SUBSTRING(x FROM y FOR z)”
    when regular `func.substring()` is used.
    Courtesy
    GunnlaugurÞórBriem。[¶](#change-4be83fabc8054be90db8d9ea622ea32c)

    参考文献：[＃2676](http://www.sqlalchemy.org/trac/ticket/2676)

### MySQL的[¶ T0\>](#change-0.7.11-mysql "Permalink to this headline")

-   **[mysql] [bug]**版本5.5,5.6的MySQL保留字更新，Hanno
    Schlichting提供。[¶](#change-e33b9298191a88a0edca1d40b5ddd554)

    参考文献：[＃2791](http://www.sqlalchemy.org/trac/ticket/2791)

### 杂项[¶ T0\>](#change-0.7.11-misc "Permalink to this headline")

-   **[bug]
    [tests]**修复了test\_execute中的“logging”导入问题，该问题在某些linux平台上无法使用。[¶](#change-2f7a576e7a8d284e37a6743b00f108d6)

    参考文献：[＃2669](http://www.sqlalchemy.org/trac/ticket/2669)，[拉取请求41](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/41)

0.7.10 [¶ T0\>](#change-0.7.10 "Permalink to this headline")
------------------------------------------------------------

发布日期：2013年2月7日

### ORM [¶ T0\>](#change-0.7.10-orm "Permalink to this headline")

-   **[orm] [bug]**修复了创建任意数量的[`sessionmaker`](orm_session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")对象时可能发生的内存泄漏。由sessionmaker创建的匿名子类在取消引用时不会被垃圾收集，因为事件包中剩余的类级别引用。这个问题也适用于任何使用ad-hoc子类与事件分派器结合使用的自定义系统。[¶](#change-db2025d4880044d4cbb1b4c52be875bb)

    参考文献：[＃2650](http://www.sqlalchemy.org/trac/ticket/2650)

-   **[orm] [bug]**[`Query.merge_result()`](orm_query.html#sqlalchemy.orm.query.Query.merge_result "sqlalchemy.orm.query.Query.merge_result")
    can now load rows from an outer join where an entity may be
    `None` without throwing an
    error.[¶](#change-7067a9d674a48894b96003b25993413c)

    参考文献：[＃2640](http://www.sqlalchemy.org/trac/ticket/2640)

-   **[orm] [bug]**The [`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
    type did not allow for the [`MutableBase.coerce()`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableBase.coerce "sqlalchemy.ext.mutable.MutableBase.coerce")
    method to be used, even though the code seemed to indicate this
    intent, so this now works and a brief example is added.
    作为一个副作用，这个事件处理程序的机制已经改变，所以新的[`MutableComposite`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")类型不再添加每个类型的全局事件处理程序。也在0.8.0b2.
    [¶](#change-2ddfafd175eec1a2d9f2b88808c52919)

    参考文献：[＃2624](http://www.sqlalchemy.org/trac/ticket/2624)

-   **[orm] [bug]**Fixed Session accounting bug whereby replacing a
    deleted object in the identity map with another object of the same
    primary key would raise a “conflicting state” error on rollback(),
    if the replaced primary key were established either via
    non-unitofwork-established INSERT statement or by primary key switch
    of another instance.[¶](#change-9534301c57ebb1ebcccf0b9a29165daa)

    参考文献：[＃2583](http://www.sqlalchemy.org/trac/ticket/2583)

### 发动机[¶ T0\>](#change-0.7.10-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
    to correctly use the given [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"),
    if given, without opening a second connection from that connection’s
    [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine").[¶](#change-60e87964fba0b375da4e3e2525694bc3)

    参考文献：[＃2604](http://www.sqlalchemy.org/trac/ticket/2604)

### SQL [¶ T0\>](#change-0.7.10-sql "Permalink to this headline")

-   **[sql] [bug]**Backported adjustment to `__repr__` for [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    to 0.7, allows [`PickleType`](core_type_basics.html#sqlalchemy.types.PickleType "sqlalchemy.types.PickleType")
    to produce a clean `repr()` to help with
    Alembic.[¶](#change-9c4c1ed9adc28c0f4580ffb99fe90993)

    参考文献：[＃2594](http://www.sqlalchemy.org/trac/ticket/2594)，[＃2584](http://www.sqlalchemy.org/trac/ticket/2584)

-   **[sql] [bug]**Fixed bug where [`Table.tometadata()`](core_metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")
    would fail if a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    had both a foreign key as well as an alternate ”.key” name for the
    column.[¶](#change-8f574adb5328ea81c58038e0dc84e0f1)

    参考文献：[＃2643](http://www.sqlalchemy.org/trac/ticket/2643)

-   **[sql] [bug]**Fixed bug where using server\_onupdate= without
    passing the “for\_update=True” flag would apply the default object
    to the server\_default, blowing away whatever was there.
    明确的for\_update =
    True参数不应该与此用法一起使用（尤其是因为文档显示的示例没有使用它），因此现在使用给定的默认对象的副本在内部进行排列，如果该标志未设置为什么对应于这个参数。[¶](#change-ec0e00d90e249bad5a39a8d564525068)

    参考文献：[＃2631](http://www.sqlalchemy.org/trac/ticket/2631)

-   **[sql] [gae] [mysql]**Added a conditional import to the
    `gaerdbms` dialect which attempts to import
    rdbms\_apiproxy vs. rdbms\_googleapi to work on both dev and
    production platforms. 现在也尊重`instance`属性。Courtesy Sean
    Lynch。还支持增强功能以​​允许用户名/密码以及修复从0.8开始的错误代码解释。[¶](#change-681094e6f3e1bffd849392f4ef50efd1)

    参考文献：[＃2649](http://www.sqlalchemy.org/trac/ticket/2649)

### MySQL的[¶ T0\>](#change-0.7.10-mysql "Permalink to this headline")

-   **[mysql]
    [feature]**在OurSQL方言中添加了“raise\_on\_warnings”标志。[¶](#change-9bcc7f0ebf5e91716c978537334baec1)

    参考文献：[＃2523](http://www.sqlalchemy.org/trac/ticket/2523)

-   **[mysql]
    [feature]**在MySQLdb方言中加入了“read\_timeout”标志。[¶](#change-da61da414d2d06ce1fe869fffadd047d)

    参考文献：[＃2554](http://www.sqlalchemy.org/trac/ticket/2554)

### 源码[¶ T0\>](#change-0.7.10-sqlite "Permalink to this headline")

-   **[sqlite]
    [bug]**对0.7.9版本中发布的SQLite相关问题进行更多调整，以便在反映外键时拦截旧版SQLite引用字符。除了拦截双引号外，其他引号字符（如括号，反引号和单引号）现在也被拦截。[¶](#change-9ff462ffd5c5507b484d835789aa8c2d)

    参考文献：[＃2568](http://www.sqlalchemy.org/trac/ticket/2568)

### MSSQL [¶ T0\>](#change-0.7.10-mssql "Permalink to this headline")

-   **[mssql] [bug]**Fixed bug whereby using “key” with Column in
    conjunction with “schema” for the owning Table would fail to locate
    result rows due to the MSSQL dialect’s “schema rendering” logic’s
    failure to take .key into
    account.[¶](#change-026a01a755a3ea79b58ce25a170e4207)

-   **[mssql]
    [bug]**在mssql信息模式中添加了一个Py3K条件，用于在不必要的.decode()调用中修复Py3k中的反射[¶](#change-6a9f365322c513e531df8e04398b73ed)

    参考文献：[＃2638](http://www.sqlalchemy.org/trac/ticket/2638)

### 预言[¶ T0\>](#change-0.7.10-oracle "Permalink to this headline")

-   **[oracle] [bug]**The Oracle LONG type, while an unbounded text
    type, does not appear to use the cx\_Oracle.LOB type when result
    rows are returned, so the dialect has been repaired to exclude LONG
    from having cx\_Oracle.LOB filtering
    applied.[¶](#change-edf0bd57d1a082833b533bbae1afe691)

    参考文献：[＃2620](http://www.sqlalchemy.org/trac/ticket/2620)

-   **[oracle] [bug]**Repaired the usage of `.prepare()` in conjunction with cx\_Oracle so that a return value of
    `False` will result in no call to
    `connection.commit()`, hence avoiding “no
    transaction” errors.
    现在已经证明两阶段事务以SQLAlchemy和cx\_oracle的方式发挥作用，但是在驱动程序中观察到警告；请查看文档以获取详细信息。[¶](#change-cbc0a0886495a3f69359e08b1582633f)

    参考文献：[＃2611](http://www.sqlalchemy.org/trac/ticket/2611)

-   **[oracle]
    [bug]**将setinputsizes()步骤中排除的cx\_oracle类型列表更改为仅包含STRING和UNICODE；
    CLOB和NCLOB被删除。这是为了解决executemany()调用破坏的cx\_oracle行为。在0.8中，应用了相同的更改，但也可以通过exclude\_setinputsizes参数进行配置。[¶](#change-56a98378c99586a41c5d39996c01b27e)

    参考文献：[＃2561](http://www.sqlalchemy.org/trac/ticket/2561)

0.7.9 [¶ T0\>](#change-0.7.9 "Permalink to this headline")
----------------------------------------------------------

发布时间：2012年10月1日

### ORM [¶ T0\>](#change-0.7.9-orm "Permalink to this headline")

-   **[orm] [bug]**Fixed bug mostly local to new AbstractConcreteBase
    helper where the “type” attribute from the superclass would not be
    overridden on the subclass to produce the “reserved for base” error
    message, instead placing a do-nothing attribute there.
    这与使用ConcreteBase以及经典具体映射的所有行为不一致，其中多态基本的“类型”列将在子类中显式禁用，除非明确覆盖。[¶](#change-7ca09fd9ba363a768515fbe6b4bb8064)

-   **[orm] [bug]**当lazy ='dynamic'与uselist =
    False组合时，会发出警告。这是0.8中的异常提升。[¶](#change-27c5a25c7b22fafc80e0458e6f02d61f)

-   **[orm] [bug]**Fixed bug whereby user error in related-object
    assignment could cause recursion overflow if the assignment
    triggered a backref of the same name as a bi-directional attribute
    on the incorrect class to the same target.
    现在提出一个信息错误。[¶](#change-2cf1cdfdb883b1ac858fc99c3fd44c54)

-   **[orm] [bug]**Fixed bug where incorrect type information would be
    passed when the ORM would bind the “version” column, when using the
    “version” feature. 测试Daniel
    Miller提供。[¶](#change-2e086c449ad8b7f942f441534d3a1099)

    参考文献：[＃2539](http://www.sqlalchemy.org/trac/ticket/2539)

-   **[orm] [bug]**Extra logic has been added to the “flush” that occurs
    within Session.commit(), such that the extra state added by an
    after\_flush() or after\_flush\_postexec() hook is also flushed in a
    subsequent flush, before the “commit” completes.
    随后对flush()的调用将继续，直到after\_flush挂钩停止添加新状态。如果每次破坏after\_flush()挂钩添加新内容，“overflow”计数器也会到位。[¶](#change-75a53327aac5791fe98ec087706a2821)

    参考文献：[＃2566](http://www.sqlalchemy.org/trac/ticket/2566)

### 发动机[¶ T0\>](#change-0.7.9-engine "Permalink to this headline")

-   **[engine]
    [feature]**事件系统内存使用的显着改进；实例级集合不再为特定类型的事件创建，除非为该事件建立实例级侦听器。[¶](#change-1ea4b7b984950d31f63149e35daeabd8)

    参考文献：[＃2516](http://www.sqlalchemy.org/trac/ticket/2516)

-   **[engine] [bug]**Fixed bug whereby a disconnect detect + dispose
    that occurs when the QueuePool has threads waiting for connections
    would leave those threads waiting for the duration of the timeout on
    the old pool (or indefinitely if timeout was disabled).
    该修补程序现在通知一个特殊的异常情况下的服务员，并让他们进入新的池。[¶](#change-fdcd7c2b744d1b0517dcd661225c5861)

    参考文献：[＃2522](http://www.sqlalchemy.org/trac/ticket/2522)

-   **[engine] [bug]**在mysql / \_\_
    init\_\_.py中添加了gaerdbms导入，但没有阻止加载新的GAE方言。[¶](#change-930bf2bff085e41ee9f2bb165727c135)

    参考文献：[＃2529](http://www.sqlalchemy.org/trac/ticket/2529)

-   **[engine] [bug]**Fixed cextension bug whereby the “ambiguous column
    error” would fail to function properly if the given index were a
    Column object and not a string.
    请注意，这里还存在一些列定位问题，这些问题在0.8中得到修复。[¶](#change-1611076226ee618bce70e17a998bb142)

    参考文献：[＃2553](http://www.sqlalchemy.org/trac/ticket/2553)

-   **[engine] [bug]**Fixed the repr() of Enum to include the “name” and
    “native\_enum” flags.
    帮助Alembic自动生成。[¶](#change-7a5dc641918acd3079fdf695b99feac6)

### SQL [¶ T0\>](#change-0.7.9-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed the DropIndex construct to support an Index
    associated with a Table in a remote
    schema.[¶](#change-4fa1e0b9d25273b768a3d9102cfc3964)

    参考文献：[＃2571](http://www.sqlalchemy.org/trac/ticket/2571)

-   **[sql] [bug]**Fixed bug in over() construct whereby passing an
    empty list for either partition\_by or order\_by, as opposed to
    None, would fail to generate correctly. Courtesy
    GunnlaugurÞórBriem。[¶](#change-de56e0073210255535e501662d7f096a)

    参考文献：[＃2574](http://www.sqlalchemy.org/trac/ticket/2574)

-   **[sql] [bug]**Fixed CTE bug whereby positional bound parameters
    present in the CTEs themselves would corrupt the overall ordering of
    bound parameters. 这主要影响SQL Server作为具有位置绑定+
    CTE支持的平台。[¶](#change-3f0696f49c0d0cc576c2925339fa8b33)

    参考文献：[＃2521](http://www.sqlalchemy.org/trac/ticket/2521)

-   **[sql] [bug]**Fixed more un-intuitivenesses in CTEs which prevented
    referring to a CTE in a union of itself without it being aliased.
    现在，CTE只对名称进行渲染，仅渲染给定名称的最外面的CTE -
    所有其他引用都以名称呈现。这甚至包括引用同一CTE对象的不同版本的其他CTE
    / SELECT，例如SELECT或SELECT的UNION
    ALL。在这种情况下，我们略微放松了对象身份和词汇身份之间的通常联系。两个不相关的CTE之间的真实姓名冲突现在引发了一个错误。[¶](#change-99a68f579410131cd9c11d84022701d0)

-   **[sql] [bug]**quoting is applied to the column names inside the
    WITH RECURSIVE clause of a common table expression according to the
    quoting rules for the originating
    Column.[¶](#change-2da6697c7fa6a82e5f84b769b2c8b627)

    参考文献：[＃2512](http://www.sqlalchemy.org/trac/ticket/2512)

-   **[sql]
    [bug]**修正0.7.6中引入的回归，在某些“克隆+替换”场景中，SELECT语句的FROM列表可能不正确。[¶](#change-c1a4594a681dd605fd87e2250bf3279b)

    参考文献：[＃2518](http://www.sqlalchemy.org/trac/ticket/2518)

-   **[sql] [bug]**Fixed bug whereby usage of a UNION or similar inside
    of an embedded subquery would interfere with result-column
    targeting, in the case that a result-column had the same ultimate
    name as a name inside the embedded
    UNION.[¶](#change-040c1b57e6448664e4b95f7c38bde6b0)

    参考文献：[＃2552](http://www.sqlalchemy.org/trac/ticket/2552)

-   **[sql]
    [bug]**修复了自0.6开始的有关结果行定位的回归。应该可以使用带有基于字符串的列的select()语句，即select（['id'，'name']）。select\_from（'mytable'），并使该语句可以通过Column对象进行定位这些名字；这是查询（MyClass）.from\_statement（some\_statement）工作的机制。At
    some point the specific case of using select([‘id’]), which is
    equivalent to select([literal\_column(‘id’)]), stopped working here,
    so this has been re-instated and of course
    tested.[¶](#change-b333e57b4e8138a52b594b9762773ecb)

    参考文献：[＃2558](http://www.sqlalchemy.org/trac/ticket/2558)

-   **[sql]
    [bug]**在ColumnOperators基础中添加了缺少的运算符is\_()，isnot()，以便这些可用的运算符像所有其他运算符一样存在于方法中。[/
    T2\>](#change-c8cd2fe962e7e67b56bece706ecebf99)

    参考文献：[＃2544](http://www.sqlalchemy.org/trac/ticket/2544)

### 的PostgreSQL [¶ T0\>](#change-0.7.9-postgresql "Permalink to this headline")

-   **[postgresql]
    [bug]**反映的主键约束中的列现在按约束本身定义的顺序返回，而不是按照表的顺序排列。Courtesy
    GunnlaugurÞórBriem .. [¶](#change-fc212ca64d8b904651fb2c76e5fa8961)

    参考文献：[＃2531](http://www.sqlalchemy.org/trac/ticket/2531)

-   **[postgresql]
    [bug]**在我们用来检测与PG断开的消息列表中添加了“终止连接”，这在服务器重启时出现在某些版本中。[¶
    T2\>](#change-bb9b195b7b37981bc5a03b6ee00066fb)

    参考文献：[＃2570](http://www.sqlalchemy.org/trac/ticket/2570)

### MySQL的[¶ T0\>](#change-0.7.9-mysql "Permalink to this headline")

-   **[mysql] [bug]**更新mysqlconnector接口以使用更新的“client
    flag”和“charset”API，由David
    McNelis提供。[¶](#change-5e04bb001a3d1f81860ab0a3eb880c8c)

### 源码[¶ T0\>](#change-0.7.9-sqlite "Permalink to this headline")

-   **[sqlite]
    [feature]**添加了对SQLite中实现的localtimestamp()SQL函数的支持，由Richard
    Mitchell提供[¶](#change-8b6a9dd463218f41b6c8b796886f842d)

-   **[sqlite] [bug]**Adjusted a very old bugfix which attempted to work
    around a SQLite issue that itself was “fixed” as of sqlite 3.6.14,
    regarding quotes surrounding a table name when using the
    “foreign\_key\_list” pragma. The fix has been adjusted to not
    interfere with quotes that are *actually in the name* of a column or
    table, to as much a degree as possible; sqlite still doesn’t return
    the correct result for foreign\_key\_list() if the target table
    actually has quotes surrounding its name, as *part* of its name
    (i.e. “”“mytable”“”).[¶](#change-8fdfac6e8169a77056e854ede3116b1d)

    参考文献：[＃2568](http://www.sqlalchemy.org/trac/ticket/2568)

-   **[sqlite]
    [bug]**调整列默认反射代码以将非字符串值转换为字符串，以适应不将默认信息作为字符串传递的旧SQLite版本。[¶
    t2 \>](#change-4f3a6c482d01e64bbcadcc806825c71f)

    参考文献：[＃2265](http://www.sqlalchemy.org/trac/ticket/2265)

### MSSQL [¶ T0\>](#change-0.7.9-mssql "Permalink to this headline")

-   **[mssql] [bug]**Fixed compiler bug whereby using a correlated
    subquery within an ORDER BY would fail to render correctly if the
    stament also used LIMIT/OFFSET, due to mis-rendering within the
    ROW\_NUMBER() OVER clause. 修正礼貌sayap
    [¶](#change-06d018a274ae08d49296d57e04e26ec7)

    参考文献：[＃2538](http://www.sqlalchemy.org/trac/ticket/2538)

-   **[mssql]
    [bug]**修正了编译器的bug，如果它有一个“offset”属性，那么给定的select()会被修改，导致构造不能再次正确编译。[/
    T2\>](#change-bd1df339b27f45dc5cda88f5736a4324)

    参考文献：[＃2545](http://www.sqlalchemy.org/trac/ticket/2545)

-   **[mssql]
    [bug]**修正了如果在多个模式中存在相同约束/表的话，主键约束的反射会使列加倍。[¶](#change-71245e957fd2b82f1ba3435287ea9f0d)

0.7.8 [¶ T0\>](#change-0.7.8 "Permalink to this headline")
----------------------------------------------------------

发布时间：2012年6月16日星期六

### ORM [¶ T0\>](#change-0.7.8-orm "Permalink to this headline")

-   **[orm]
    [feature]**不再废弃flush()的'objects'参数，因为已经识别出一些有效的用例。[¶](#change-90a7ad18c89ef080942d51375dd30972)

-   **[orm] [bug]**Fixed bug whereby subqueryload() from a polymorphic
    mapping to a target would incur a new invocation of the query for
    each distinct class encountered in the polymorphic
    result.[¶](#change-cf3b8502914010cbf22dd36d53d49d41)

    参考文献：[＃2480](http://www.sqlalchemy.org/trac/ticket/2480)

-   **[orm] [bug]**Fixed bug in declarative whereby the precedence of
    columns in a joined-table, composite column (typically for id) would
    fail to be correct if the columns contained names distinct from
    their attribute names.
    这会导致针对实体属性的primaryjoin条件不正确。相关的，因为这应该是其中的一部分，这是。[¶](#change-a32af8388995303eab427cf746d301ee)

    参考文献：[＃2491](http://www.sqlalchemy.org/trac/ticket/2491)，[＃1892](http://www.sqlalchemy.org/trac/ticket/1892)

-   **[orm] [bug]**修正了不接受标识参数的identity\_key()函数。[¶
    T0\>](#change-f98e8f725d059fea2dfc556d72b1b131)

    参考文献：[＃2508](http://www.sqlalchemy.org/trac/ticket/2508)

-   **[orm]
    [bug]**修复了populate\_existing选项不会传播给子查询渴望加载器的错误。[¶
    T0\>](#change-4a617743b2bf4279e53c14ee010bc346)

    参考文献：[＃2497](http://www.sqlalchemy.org/trac/ticket/2497)

### 发动机[¶ T0\>](#change-0.7.8-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed memory leak in C version of result proxy
    whereby DBAPIs which don’t deliver pure Python tuples for result
    rows would fail to decrement refcounts correctly.
    最受关注的DBAPI是pyodbc。[¶](#change-348d36798c980e7c202e6fdcc5850810)

    参考文献：[＃2489](http://www.sqlalchemy.org/trac/ticket/2489)

-   **[engine] [bug]**Fixed bug affecting Py3K whereby string positional
    parameters passed to engine/connection execute() would fail to be
    interpreted correctly, due to \_\_iter\_\_ being present on Py3K
    string..[¶](#change-fd4bdaeacedad743b6f3bbcd200ef237)

    参考文献：[＃2503](http://www.sqlalchemy.org/trac/ticket/2503)

### SQL [¶ T0\>](#change-0.7.8-sql "Permalink to this headline")

-   **[sql] [bug]**将BIGINT添加到类型.\_\_
    all\_\_，BIGINT，BINARY，VARBINARY到sqlalchemy模块名称空间，再加上测试以确保不再发生此破坏。[¶](#change-5c6ba9ce1ee5598442500138f0eea997)

    参考文献：[＃2499](http://www.sqlalchemy.org/trac/ticket/2499)

-   **[sql] [bug]**Repaired common table expression rendering to
    function correctly when the SELECT statement contains UNION or other
    compound expressions, courtesy
    btbuilder.[¶](#change-e2fe913b74611147fd04de969da717aa)

    参考文献：[＃2490](http://www.sqlalchemy.org/trac/ticket/2490)

-   **[sql]
    [bug]**修正了bug，即append\_column()在克隆的select()构造中无法正确运行，由GunnlaugurÞórBriem提供。[¶](#change-82d5e8837ecd40049cc656f51882f9dd)

    参考文献：[＃2482](http://www.sqlalchemy.org/trac/ticket/2482)

### 的PostgreSQL [¶ T0\>](#change-0.7.8-postgresql "Permalink to this headline")

-   **[postgresql] [bug]**在反映枚举时删除了不必要的表子句。Courtesy
    GunnlaugurÞórBriem。[¶](#change-2b0b56fe92fecdf3f47b187723fac1d1)

    参考文献：[＃2510](http://www.sqlalchemy.org/trac/ticket/2510)

### MySQL的[¶ T0\>](#change-0.7.8-mysql "Permalink to this headline")

-   **[mysql] [feature]**为Google App Engine添加了一种新的方言。Courtesy
    Richie Foreman。[¶](#change-b9342db19c8d65b942f8bcb7638f0ad3)

    参考文献：[＃2484](http://www.sqlalchemy.org/trac/ticket/2484)

### 预言[¶ T0\>](#change-0.7.8-oracle "Permalink to this headline")

-   **[oracle] [bug]**向oracle添加了ROWID。\* [¶
    T0\>](#change-ad8811c99ec2bf8fc5f2e8ff5e1b91a3)

    参考文献：[＃2483](http://www.sqlalchemy.org/trac/ticket/2483)

0.7.7 [¶ T0\>](#change-0.7.7 "Permalink to this headline")
----------------------------------------------------------

发布时间：2012年5月5日星期六

### ORM [¶ T0\>](#change-0.7.7-orm "Permalink to this headline")

-   **[orm] [feature]**Added prefix\_with() method to Query, calls upon
    select().prefix\_with() to allow placement of MySQL SELECT
    directives in statements. Courtesy Diana Clarke
    [¶](#change-25aac7662d89caf0fb5cbcd3d4145b73)

    参考文献：[＃2443](http://www.sqlalchemy.org/trac/ticket/2443)

-   **[orm] [feature]**为@validates
    include\_removes添加了新标志。如果为True，则collection
    remove和attribute
    del事件也将被发送到验证函数，该函数在使用此标志时接受附加参数“is\_remove”。[¶](#change-9d753c51f57c3c616f604d0db83097d5)

-   **[orm] [bug]**Fixed issue in unit of work whereby setting a
    non-None self-referential many-to-one relationship to None would
    fail to persist the change if the former value was not already
    loaded..[¶](#change-b8f58dbdb7f5047dc8fa39d59cb26288)

    参考文献：[＃2477](http://www.sqlalchemy.org/trac/ticket/2477)

-   **[orm]
    [bug]**修正0.7.6引入的错误，其中column\_mapped\_collection用于映射为连接或其他间接选择的列将无法运行。[¶](#change-f77cf934beb15ca7e09a931e3b100a1a)

    参考文献：[＃2409](http://www.sqlalchemy.org/trac/ticket/2409)

-   **[orm] [bug]**Fixed bug whereby polymorphic\_on column that’s not
    otherwise mapped on the class would be incorrectly included in a
    merge() operation, raising an
    error.[¶](#change-a152eaa87daaa0d2a342246bcb91e574)

    参考文献：[＃2449](http://www.sqlalchemy.org/trac/ticket/2449)

-   **[orm] [bug]**Fixed bug in expression annotation mechanics which
    could lead to incorrect rendering of SELECT statements with aliases
    and joins, particularly when using
    column\_property().[¶](#change-abfe23b5d84195d02cbf3aae199c82cd)

    参考文献：[＃2453](http://www.sqlalchemy.org/trac/ticket/2453)

-   **[orm] [bug]**修正了会阻止OrderingList被pickleable的错误。礼貌Jeff
    Dairiki [¶](#change-879e7b4c03a5046a0e6cc2aee6ab5036)

    参考文献：[＃2454](http://www.sqlalchemy.org/trac/ticket/2454)

-   **[orm] [bug]**Fixed bug in relationship comparisons whereby calling
    unimplemented methods like SomeClass.somerelationship.like() would
    produce a recursion overflow, instead of
    NotImplementedError.[¶](#change-a809abc1a2320cef2ddbf36f9823afac)

### SQL [¶ T0\>](#change-0.7.7-sql "Permalink to this headline")

-   **[sql]
    [feature]**添加了新的连接事件dbapi\_error()。在SQLAlchemy修改游标状态之前调用所有DBAPI级错误传递原始DBAPI异常。[¶](#change-60e0de8dbae77883685d68262a548cb0)

-   **[sql]
    [bug]**在创建索引时不删除警告；虽然这可能不是用户想要的，但它是一个有效的用例，因为索引可能只是某个特定名称索引的占位符。[¶](#change-258642bfde7a22ef72f36f37450b99fa)

-   **[sql] [bug]**如果在调用“with
    engine.begin()”时conn.begin()失败，则新获取的Connection在通常向前传播异常之前显式关闭。[¶\<
    / T2\>](#change-ab71ae4387dd75bf6a53122b28ae899e)

-   **[sql] [bug]**将BINARY，VARBINARY添加到类型.\_\_ all
    \_\_。[¶](#change-e3411e9d22bdbb5992f9e88d3dcaee90)

    参考文献：[＃2474](http://www.sqlalchemy.org/trac/ticket/2474)

### 的PostgreSQL [¶ T0\>](#change-0.7.7-postgresql "Permalink to this headline")

-   **[postgresql] [feature]**Added new for\_update/with\_lockmode()
    options for Postgresql: for\_update=”read”/ with\_lockmode(“read”),
    for\_update=”read\_nowait”/ with\_lockmode(“read\_nowait”).
    这些分别发出“FOR SHARE”和“FOR NOWAREAIT”。Courtesy Diana Clarke
    [¶](#change-60c3844adeb64d1db651beaee5017dbe)

    参考文献：[＃2445](http://www.sqlalchemy.org/trac/ticket/2445)

-   **[postgresql]
    [bug]**在反映域时删除了不必要的表子句。[¶](#change-a0e768a991b47e8fdefbd505b05b3e17)

    参考文献：[＃2473](http://www.sqlalchemy.org/trac/ticket/2473)

### MySQL的[¶ T0\>](#change-0.7.7-mysql "Permalink to this headline")

-   **[mysql] [bug]**Fixed bug whereby column name inside of “KEY”
    clause for autoincrement composite column with InnoDB would double
    quote a name that’s a reserved word. Courtesy Jeff
    Dairiki。[¶](#change-1be3a59937fd9dfcf596e919548e77b0)

    参考文献：[＃2460](http://www.sqlalchemy.org/trac/ticket/2460)

-   **[mysql] [bug]**Fixed bug whereby get\_view\_names() for
    “information\_schema” schema would fail to retrieve views marked as
    “SYSTEM VIEW”. 礼貌Matthew
    Turland。[¶](#change-d53f513885dabbbb9b7b9479dcc6c9fb)

-   **[mysql] [bug]**Fixed bug whereby if cast() is used on a SQL
    expression whose type is not supported by cast() and therefore CAST
    isn’t rendered by the dialect, the order of evaluation could change
    if the casted expression required that it be grouped; grouping is
    now applied to those
    expressions.[¶](#change-665f633590992519d1a2afe8c40aa0b9)

    参考文献：[＃2467](http://www.sqlalchemy.org/trac/ticket/2467)

### 源码[¶ T0\>](#change-0.7.7-sqlite "Permalink to this headline")

-   **[sqlite] [feature]**新增SQLite执行选项“sqlite\_raw\_colnames =
    True”，将绕过尝试从SQLite
    cursor.description返回的列名称中删除“。”。[¶](#change-4d3073c4d8020a0289ac68eed962eaa3)

    参考文献：[＃2475](http://www.sqlalchemy.org/trac/ticket/2475)

-   **[sqlite] [bug]**When the primary key column of a Table is
    replaced, such as via extend\_existing, the “auto increment” column
    used by insert() constructs is reset.
    以前它会继续引用前一个主键列。[¶](#change-8c57451af0004baeb28caf92d4ee90b8)

    参考文献：[＃2525](http://www.sqlalchemy.org/trac/ticket/2525)

### MSSQL [¶ T0\>](#change-0.7.7-mssql "Permalink to this headline")

-   **[mssql]
    [feature]**将临时create\_engine标志supports\_unicode\_bind添加到PyODBC方言中，以强制方言是否将Python
    unicode文字传递给PyODBC。[¶](#change-5948b6fff685d80894bef6e58a19581d)

-   **[mssql] [bug]**在使用pyodbc方言时修复了use\_scope\_identity
    create\_engine()标志。如果设置为False，以前该标志将被忽略。当设置为False时，在每个INSERT之后，您将在“implicit\_returning”设置为False的表中获得最后插入的ID后的“SELECT
    @@ identity”。[¶](#change-f013930a1f1b98f461979f93285819df)

-   **[mssql] [bug]**UPDATE..FROM syntax with SQL Server requires that
    the updated table be present in the FROM clause when an alias of
    that table is also present in the FROM clause.
    当FROM出现在第一位时，更新的表现在总是存在于FROM中。礼貌sayap。[¶](#change-06067c1d141545a78a5e38fea15d3736)

    参考文献：[＃2468](http://www.sqlalchemy.org/trac/ticket/2468)

0.7.6 [¶ T0\>](#change-0.7.6 "Permalink to this headline")
----------------------------------------------------------

发布时间：2012年3月14日星期三

### ORM [¶ T0\>](#change-0.7.6-orm "Permalink to this headline")

-   **[orm]
    [feature]**在会话中添加了“no\_autoflush”上下文管理器，与with一起使用：将临时禁用autoflush。[¶](#change-da251880fd88fa1c37bfa0d587e41173)

-   **[orm]
    [feature]**在Query中添加了cte()方法，从Core中调用公共表表达式支持（见下文）[¶](#change-3dd168b2f746fa1b43aa5a01897c7ef3)

    参考文献：[＃1859](http://www.sqlalchemy.org/trac/ticket/1859)

-   **[orm] [feature]**Added the ability to query for Table-bound column
    names when using
    query(sometable).filter\_by(colname=value).[¶](#change-06c8bf2ebcd62bebb89b05351bf869c6)

    参考文献：[＃2400](http://www.sqlalchemy.org/trac/ticket/2400)

-   **[orm]
    [bug]**修正了事件注册错误，主要显示事件没有在事件与Session类关联后创建的sessionmaker()中注册。[¶
    t2 \>](#change-886ab67fd7fa03ee2c0d177071b3ded4)

    参考文献：[＃2424](http://www.sqlalchemy.org/trac/ticket/2424)

-   **[orm] [bug]**Fixed bug whereby a primaryjoin condition with a
    “literal” in it would raise an error on compile with certain kinds
    of deeply nested expressions which also needed to render the same
    bound parameter name more than
    once.[¶](#change-d6df1da3c271d4360d60721dcd4d93cd)

    参考文献：[＃2425](http://www.sqlalchemy.org/trac/ticket/2425)

-   **[orm]
    [bug]**删除对映射对象进行多次删除时受影响的行数的检查。如果在两行之间存在ON
    DELETE
    CASCADE，我们无法从DBAPI获得准确的行计数；在任何情况下，大多数DBAPI都不支持此特定计数，MySQLdb是值得注意的情况。[¶](#change-c963d79fbb48b092468b8df14fe08b03)

    参考文献：[＃2403](http://www.sqlalchemy.org/trac/ticket/2403)

-   **[orm]
    [bug]**修正了使用attribute\_mapped\_collection或column\_mapped\_collection的对象无法被pickle的问题。[¶](#change-8ce7b5c1f9764f4be9a06bb9f69e52f2)

    参考文献：[＃2409](http://www.sqlalchemy.org/trac/ticket/2409)

-   **[orm] [bug]**Fixed bug whereby MappedCollection would not get the
    appropriate collection instrumentation if it were only used in a
    custom subclass that used
    @collection.internally\_instrumented.[¶](#change-4139f8190200416937260afba0d0f8b1)

    参考文献：[＃2406](http://www.sqlalchemy.org/trac/ticket/2406)

-   **[orm] [bug]**Fixed bug whereby SQL adaption mechanics would fail
    in a very nested scenario involving joined-inheritance,
    joinedload(), limit(), and a derived function in the columns
    clause.[¶](#change-9e5cd50053bb474dbea526f38ba4e148)

    参考文献：[＃2419](http://www.sqlalchemy.org/trac/ticket/2419)

-   **[orm]
    [bug]**修复了CascadeOptions的repr()以包含refresh-expire。还重做了CascadeOptions成为。[¶](#change-f8031eba4bd7fcd731200ea774332cdf)

    参考文献：[＃2417](http://www.sqlalchemy.org/trac/ticket/2417)

-   **[orm] [bug]**Improved the “declarative reflection” example to
    support single-table inheritance, multiple calls to prepare(),
    tables that are present in alternate schemas, establishing only a
    subset of classes as
    reflected.[¶](#change-55aab50690b92c57e72f96dae94d9731)

-   **[orm]
    [bug]**缩放在flush()中应用的测试，以检查UPDATE对一个表内部分为空的PK，只有在真正发生UPDATE时才会发生。[¶\<
    / T2\>](#change-2bd80098953ad4f526aecbdbdb6c7a38)

    参考文献：[＃2390](http://www.sqlalchemy.org/trac/ticket/2390)

-   **[orm] [bug]**Fixed bug whereby if a method name conflicted with a
    column name, a TypeError would be raised when the mapper tried to
    inspect the \_\_get\_\_() method on the method
    object.[¶](#change-1c063ae66277f88058d137e25e63b77b)

    参考文献：[＃2352](http://www.sqlalchemy.org/trac/ticket/2352)

### 发动机[¶ T0\>](#change-0.7.6-engine "Permalink to this headline")

-   **[engine] [feature]**为连接添加了“no\_parameters =
    True”执行选项。如果不存在任何参数，则会将该语句作为cursor.execute（语句）传递，从而在不存在参数集合时调用DBAPIs行为；对于psycopg2和mysql-python，这意味着不会解释字符串中的％符号。这只会发生在这个选项中，而不仅仅是参数列表是空白的，否则这会导致SQL表达式的不一致的行为，这通常会导致百分号转义（并且在编译时，不能提前知道参数是否存在于一些情况）。[¶](#change-2d7d75c321c420f13868c04f48c58024)

    参考文献：[＃2407](http://www.sqlalchemy.org/trac/ticket/2407)

-   **[engine]
    [feature]**将create\_engine的pool\_reset\_on\_return参数添加到控制权，可以控制“连接返回”行为。还为pool.reset\_on\_return添加了新的参数'rollback'，'commit'，None，以允许对连接返回活动的更多控制。[¶](#change-48cbd41778bd9bf524befc7899045bd6)

    参考文献：[＃2378](http://www.sqlalchemy.org/trac/ticket/2378)

-   **[engine] [feature]**为引擎，连接添加了一些体面的上下文管理器：

        with engine.begin() as conn:
            <work with conn in a transaction>

    和：

        with engine.connect() as conn:
            <work with conn>

    在engine.begin()完成，提交或回滚事务时出错都关闭连接。

    [¶](#change-f22f644c754519a55485cda58f78ade4)

-   **[engine] [bug]**添加了对MockConnection（即与strategy
    =“mock”一起使用）的execution\_options()调用，它充当参数传递。[¶](#change-1b194e4331b2ed3e8f8f778123152f56)

### SQL [¶ T0\>](#change-0.7.6-sql "Permalink to this headline")

-   **[sql]
    [feature]**增加了对SQL标准公用表表达式（CTE）的支持，允许SELECT对象作为CTE源（DML尚未支持）。这是通过任何select()构造的cte()方法调用的。[¶](#change-1591463b72830324d33006ffd884fc18)

    参考文献：[＃1859](http://www.sqlalchemy.org/trac/ticket/1859)

-   修正了内核中的内存泄漏问题，当C扩展与特定类型的结果提取一起使用时，尤其是当调用orm
    query.count()时，会发生内存泄漏。[**[sql]
    [bug]**](#change-08dbc44d75c1c124d995d5797c268220)

    参考文献：[＃2427](http://www.sqlalchemy.org/trac/ticket/2427)

-   **[sql] [bug]**Fixed issue whereby attribute-based column access on
    a row would raise AttributeError with non-C version,
    NoSuchColumnError with C version.
    现在在两种情况下都会引发AttributeError。[¶](#change-d8df6d8759ad159ad56f547c506a3983)

    参考文献：[＃2398](http://www.sqlalchemy.org/trac/ticket/2398)

-   **[sql]
    [bug]**添加了对列中的.key作为结果集行中的字符串标识符的支持。.key当前被列为列的“备用”名称，并被以该常量名称具有该键值的列的名称取代。对于SQLAlchemy的下一个主要版本，我们可能会反转此优先级，以便.key优先，但尚未确定。[¶](#change-49687573edf51e35f6e2e138c9d97ed4)

    参考文献：[＃2392](http://www.sqlalchemy.org/trac/ticket/2392)

-   **[sql]
    [bug]**当insert()或update()构造的values()子句中声明不存在列时，会发出警告。将在0.8中移至异常。[¶](#change-343f97bf51f98600f6e8fcd6d441ddbe)

    参考文献：[＃2413](http://www.sqlalchemy.org/trac/ticket/2413)

-   **[sql] [bug]**A significant change to how labeling is applied to
    columns in SELECT statements allows “truncated” labels, that is
    label names that are generated in Python which exceed the maximum
    identifier length (note this is configurable via label\_length on
    create\_engine()), to be properly referenced when rendered inside of
    a subquery, as well as to be present in a result set row using their
    original in-Python
    names.[¶](#change-a77bfc79b387192867cd3cb1d2e792df)

    参考文献：[＃2396](http://www.sqlalchemy.org/trac/ticket/2396)

-   **[sql] [bug]**Fixed bug in new “autoload\_replace” flag which would
    fail to preserve the primary key constraint of the reflected
    table.[¶](#change-c2121d614de6518b5a70afb2a6acc1a8)

    参考文献：[＃2402](http://www.sqlalchemy.org/trac/ticket/2402)

-   **[sql]
    [bug]**当传递的参数不能被解释为列或表达式时，索引会引发。当没有列创建索引时，会发出警告。[¶](#change-e13352b56336bb2ca6357a005becb329)

    参考文献：[＃2380](http://www.sqlalchemy.org/trac/ticket/2380)

### MySQL的[¶ T0\>](#change-0.7.6-mysql "Permalink to this headline")

-   **[mysql]
    [feature]**增加了对MySQL索引和主键约束类型的支持。USING）通过新的mysql\_using参数来索引和PrimaryKeyConstraint，由Diana
    Clarke提供。[¶](#change-36eb1e2c4794e72f98f0ed14abf5e65b)

    参考文献：[＃2386](http://www.sqlalchemy.org/trac/ticket/2386)

-   **[mysql]
    [feature]**增加了对所有MySQL方言的“isolation\_level”参数的支持。感谢mu\_mind这里的补丁。[¶](#change-3df61a1e9f44018504cf0be0185c2a7f)

    参考文献：[＃2394](http://www.sqlalchemy.org/trac/ticket/2394)

### 源码[¶ T0\>](#change-0.7.6-sqlite "Permalink to this headline")

-   **[sqlite]
    [bug]**修正C扩展中的错误，其中字符串格式不会应用于以整数形式返回的数值；这主要影响SQLite，它不会保持数字比例设置。[¶](#change-75ed46e3397d789de20c3c9699f6328d)

    参考文献：[＃2432](http://www.sqlalchemy.org/trac/ticket/2432)

### MSSQL [¶ T0\>](#change-0.7.6-mssql "Permalink to this headline")

-   **[mssql]
    [feature]**在UpdateBase上使用新的with\_hint()方法增加了对MSSQL
    INSERT，UPDATE和DELETE表提示的支持。[¶](#change-24dedd563345980d146ccf072345481c)

    参考文献：[＃2430](http://www.sqlalchemy.org/trac/ticket/2430)

### 预言[¶ T0\>](#change-0.7.6-oracle "Permalink to this headline")

-   **[oracle]
    [feature]**添加了一个新的create\_engine()标志coerce\_to\_decimal =
    False，禁用精度数值处理，通过将所有数值转换为Decimal可以增加大量的开销。[¶
    t2 \>](#change-fb4460bd1ca1980817d3dedb89755c9d)

    参考文献：[＃2399](http://www.sqlalchemy.org/trac/ticket/2399)

-   **[oracle] [bug]**增加了LONG
    [缺少的编译支持¶](#change-985364280fa865032dd045d68431f232)

    参考文献：[＃2401](http://www.sqlalchemy.org/trac/ticket/2401)

-   **[oracle]
    [bug]**将'LEVEL'添加到Oracle的保留字列表中。[¶](#change-b1c0ae3b7d2775d911aaeeb8e3d3c872)

    参考文献：[＃2435](http://www.sqlalchemy.org/trac/ticket/2435)

### 杂项[¶ T0\>](#change-0.7.6-misc "Permalink to this headline")

-   **[bug] [examples]**Altered \_params\_from\_query() function in
    Beaker example to pull bindparams from the fully compiled statement,
    as a quick means to get everything including subqueries in the
    columns clause, etc.[¶](#change-19dae4d37fac9733caba73475b99064b)

0.7.5 [¶ T0\>](#change-0.7.5 "Permalink to this headline")
----------------------------------------------------------

发布时间：2012年1月28日星期六

### ORM [¶ T0\>](#change-0.7.5-orm "Permalink to this headline")

-   **[orm]
    [feature]**在declarative\_base()中添加了“class\_registry”参数。允许两个或更多的声明式库共享相同的类名注册表。[¶](#change-3a102420811437e8993c20361a8d9534)

-   **[orm] [feature]**
    query.filter()接受通过AND连接的多个条件，即query.filter（x == y，z\>
    q，...）[¶\< / T2\>](#change-0c9ac7ca68fc1ad2df5e31c3920b7fb3)

-   **[orm]
    [feature]**增加了关系加载器选项的新功能，以允许“默认”加载器策略。将'\*'传递给任何joinedload()，lazyload()，subqueryload()或noload()，并成为用于所有关系的加载器策略，除了在查询中明确声明的那些策略。感谢即将到来的贡献者Kent
    Bower提供了一个详尽且写得很好的测试套件！[¶](#change-57c1f10c52d34b2117be666480e44fdc)

    参考文献：[＃2351](http://www.sqlalchemy.org/trac/ticket/2351)

-   **[orm]
    [feature]**添加了新的声明性反射示例，说明如何最好地将表反射与声明混合以及使用一些新的特性。[¶](#change-97633f7e42b1537d18cbeea43b26bc27)

    参考文献：[＃2356](http://www.sqlalchemy.org/trac/ticket/2356)

-   **[orm] [bug]**Fixed issue where modified session state established
    after a failed flush would be committed as part of the subsequent
    transaction that begins automatically after manual call to
    rollback().
    会话的状态在rollback()中进行检查，如果存在新状态，将发出警告，并第二次调用restore\_snapshot()，放弃这些更改。[¶](#change-55d8c1fff7aefe4a1f70319dec6adc6b)

    参考文献：[＃2389](http://www.sqlalchemy.org/trac/ticket/2389)

-   **[orm]
    [bug]**固定了0.7.4的回归，从超类中使用已经检测过的列作为“polymorphic\_on”，无法解析底层Column。[¶](#change-b1e956782e806998b21c5c59c63196ea)

    参考文献：[＃2345](http://www.sqlalchemy.org/trac/ticket/2345)

-   **[orm]
    [bug]**如果xyzload\_all()与两个非连接关系不正确地使用，则引发异常[¶](#change-8272906e502e3c17ceaf46c056dd61a7)

    参考文献：[＃2370](http://www.sqlalchemy.org/trac/ticket/2370)

-   **[orm] [bug]**Fixed bug whereby event.listen(SomeClass) forced an
    entirely unnecessary compile of the mapper, making events very hard
    to set up at module import time (nobody noticed this
    ??)[¶](#change-6af3c2131d1f215bc47d9088abe62c4b)

    参考文献：[＃2367](http://www.sqlalchemy.org/trac/ticket/2367)

-   **[orm] [bug]**Fixed bug whereby hybrid\_property didn’t work as a
    kw arg in any(), has().[¶](#change-d7b48db2025736b2d9643cb7b3a0e3c2)

-   **[orm]
    [bug]**确保所有ORM异常的pickleability能够兼容多处理。[¶](#change-b88bd4933dc47c44005e5fdc6794709a)

    参考文献：[＃2371](http://www.sqlalchemy.org/trac/ticket/2371)

-   **[orm] [bug]**implemented standard “can’t set attribute” / “can’t
    delete attribute” AttributeError when setattr/delattr used on a
    hybrid that doesn’t define fset or
    fdel.[¶](#change-a73cc2e518480d53268efadf9b8f7eb8)

    参考文献：[＃2353](http://www.sqlalchemy.org/trac/ticket/2353)

-   **[orm] [bug]**Fixed bug where unpickled object didn’t have enough
    of its state set up to work correctly within the unpickle() event
    established by the mutable object extension, if the object needed
    ORM attribute access within \_\_eq\_\_() or
    similar.[¶](#change-3551999284ff42f7dcdc41a5a7332711)

    参考文献：[＃2362](http://www.sqlalchemy.org/trac/ticket/2362)

-   **[orm] [bug]**Fixed bug where “merge” cascade could mis-interpret
    an unloaded attribute, if the load\_on\_pending flag were used with
    relationship(). 感谢Kent
    Bower进行测试。[¶](#change-abf88e7bed26797a4f92f148de9b72cb)

    参考文献：[＃2374](http://www.sqlalchemy.org/trac/ticket/2374)

-   **[orm]**Fixed regression from 0.6 whereby if “load\_on\_pending”
    relationship() flag were used where a non-“get()” lazy clause needed
    to be emitted on a pending object, it would fail to
    load.[¶](#change-08885bc09f14b67a91d5920966baf2bc)

### 发动机[¶ T0\>](#change-0.7.5-engine "Permalink to this headline")

-   **[engine]
    [bug]**将\_\_reduce\_\_添加到StatementError，DBAPIError列错误中，以便异常可以使用，就像使用多处理时一样。但是，并不是所有的DBAPI都支持这一点，比如psycopg2.
    [¶](#change-9ebe95491ecfb2edd5dc94384c92d141)

    参考文献：[＃2371](http://www.sqlalchemy.org/trac/ticket/2371)

-   **[engine] [bug]**Improved error messages when a non-string or
    invalid string is passed to any of the date/time processors used by
    SQLite, including C and Python
    versions.[¶](#change-b6d472837686e1a147a08b7332fff398)

    参考文献：[＃2382](http://www.sqlalchemy.org/trac/ticket/2382)

-   **[engine] [bug]**Fixed bug whereby a table-bound Column object
    named “\_**” which matched a column labeled as “\_” could match
    inappropriately when targeting in a result set
    row.[¶](#change-ead8712a877501eeed679427b22e44f1)**

    参考文献：[＃2377](http://www.sqlalchemy.org/trac/ticket/2377)

-   **[engine] [bug]**Fixed bug in “mock” strategy whereby correct DDL
    visit method wasn’t called, resulting in “CREATE/DROP SEQUENCE”
    statements being
    duplicated[¶](#change-1d2bfe0a34b8c72c15a364316180688c)

    参考文献：[＃2384](http://www.sqlalchemy.org/trac/ticket/2384)

### SQL [¶ T0\>](#change-0.7.5-sql "Permalink to this headline")

-   **[sql]
    [feature]**新的反射功能“autoload\_replace”；当在表格上设置为False时，表格可以自动加载而不需要替换现有的列。允许构建更灵活的表结构/反射链，包括它有助于将声明与表反射相结合。请参阅wiki上的新示例。[¶](#change-c7de069c3fc21b68e50f220e6a0dffe4)

    参考文献：[＃2356](http://www.sqlalchemy.org/trac/ticket/2356)

-   **[sql]
    [feature]**在sqlalchemy.sql命名空间中添加了“false()”和“true()”表达式结构，尽管不是\_\_all\_\_的一部分。[¶](#change-177b33e20d11306f6f5b91727ba15982)

-   **[sql] [feature]**Dialect-specific compilers now raise CompileError
    for all type/statement compilation issues, instead of
    InvalidRequestError or ArgumentError. CREATE
    TABLE的DDL将重新引发CompileError以包含有问题列的表/列信息。[¶](#change-b3dc079dbd31fcbe3c24aa00c4f0f490)

    参考文献：[＃2361](http://www.sqlalchemy.org/trac/ticket/2361)

-   **[sql] [bug]**Improved the API for add\_column() such that if the
    same column is added to its own table, an error is not raised and
    the constraints don’t get doubled up.
    还有一些反射/声明模式。[¶](#change-39d3b5ddb9f3dcbd42a74dc6df0c998a)

    参考文献：[＃2356](http://www.sqlalchemy.org/trac/ticket/2356)

-   **[sql] [bug]**Fixed issue where the “required” exception would not
    be raised for bindparam() with required=True, if the statement were
    given no parameters at
    all.[¶](#change-37eea1099c4c938a74f03792a2635704)

    参考文献：[＃2381](http://www.sqlalchemy.org/trac/ticket/2381)

### MySQL的[¶ T0\>](#change-0.7.5-mysql "Permalink to this headline")

-   **[mysql]
    [bug]**修正了regexp，它可以滤除未反映的“PARTITION”指令的警告，这要归功于George
    Reilly [¶](#change-f8751618b3a1220a24952e880d8d1ec0)

    参考文献：[＃2376](http://www.sqlalchemy.org/trac/ticket/2376)

### 源码[¶ T0\>](#change-0.7.5-sqlite "Permalink to this headline")

-   **[sqlite] [bug]**the “name” of an FK constraint in SQLite is
    reflected as “None”, not “0” or other integer value.
    在任何情况下，SQLite似乎都不支持约束命名。[¶](#change-117c33e7b1627c5cc26eee90b4ffa6fd)

    参考文献：[＃2364](http://www.sqlalchemy.org/trac/ticket/2364)

-   **[sqlite] [bug]**sql.false() and sql.true() compile to 0 and 1,
    respectively in sqlite[¶](#change-54d9c20f63f1e057ffafe7cd4bff6569)

    参考文献：[＃2368](http://www.sqlalchemy.org/trac/ticket/2368)

-   **[sqlite] [bug]**removed an erroneous “raise” in the SQLite dialect
    when getting table names and view names, where logic is in place to
    fall back to an older version of SQLite that doesn’t have the
    “sqlite\_temp\_master”
    table.[¶](#change-2bdd22a024225bc7479dc1df515c5a4c)

### MSSQL [¶ T0\>](#change-0.7.5-mssql "Permalink to this headline")

-   **[mssql] [bug]**Adjusted the regexp used in the mssql.TIME type to
    ensure only six digits are received for the “microseconds” portion
    of the value, which is expected by Python’s datetime.time().
    请注意，对于发送微秒的支持至少在pyodbc中似乎还没有可能。[¶](#change-cfa986a99df4132f7d3327a8948212a3)

    参考文献：[＃2340](http://www.sqlalchemy.org/trac/ticket/2340)

-   **[mssql]
    [bug]**基于pymssql上的“30个字符”限制，根据报告说它现在做的更好。pymssql没有得到很好的测试，并且由于DBAPI处于不断变化之中，目前还不清楚该驱动程序的状态以及SQLAlchemy的实现应如何适应。[](#change-65bbfc0cbf4ea706329108c2d0689758)

    参考文献：[＃2347](http://www.sqlalchemy.org/trac/ticket/2347)

### 预言[¶ T0\>](#change-0.7.5-oracle "Permalink to this headline")

-   **[oracle]
    [bug]**将ORA-03135添加到oracle“连接丢失”错误永不停止的列表中[¶](#change-b601d2076969dff424f84e83f7e23a3f)

    参考文献：[＃2388](http://www.sqlalchemy.org/trac/ticket/2388)

### 杂项[¶ T0\>](#change-0.7.5-misc "Permalink to this headline")

-   **[feature]
    [examples]**简化版本示例，使用声明性混合以及事件侦听器，而不是元类+
    SessionExtension。[¶](#change-7ea101b9e5ac780313f4ec94a8e11e50)

    参考文献：[＃2313](http://www.sqlalchemy.org/trac/ticket/2313)

-   **[bug] [core]**Changed LRUCache, used by the mapper to cache
    INSERT/UPDATE/DELETE statements, to use an incrementing counter
    instead of a timestamp to track entries, for greater reliability
    versus using time.time(), which can cause test failures on some
    platforms.[¶](#change-8d78c8ac914fdc73f0352b8d86340cc3)

    参考文献：[＃2379](http://www.sqlalchemy.org/trac/ticket/2379)

-   **[bug] [core]**Added a boolean check for the “finalize” function
    within the pool connection proxy’s weakref callback before calling
    it, so that a warning isn’t emitted that this function is None when
    the application is exiting and gc has removed the function from the
    module before the weakref callback was
    invoked.[¶](#change-f11c1ccaa941a5a91a34b9ed4664bc49)

    参考文献：[＃2383](http://www.sqlalchemy.org/trac/ticket/2383)

-   **[bug] [py3k]**Fixed inappropriate usage of util.py3k flag and
    renamed it to util.py3k\_warning, since this flag is intended to
    detect the -3 flag series of import restrictions
    only.[¶](#change-1556c377ef9bf08b1aa03c0a86a85045)

    参考文献：[＃2348](http://www.sqlalchemy.org/trac/ticket/2348)

-   **[bug]
    [examples]**修正large\_collection.py在删除表之前关闭会话。[¶](#change-6152f928a75eb13ceaee66f9f222b9f0)

    参考文献：[＃2346](http://www.sqlalchemy.org/trac/ticket/2346)

0.7.4 [¶ T0\>](#change-0.7.4 "Permalink to this headline")
----------------------------------------------------------

发布时间：2011年12月9日星期五

### ORM [¶ T0\>](#change-0.7.4-orm "Permalink to this headline")

-   **[orm] [feature]** polymorphic\_on现在接受许多新的值：

    > -   未映射的独立表达式
    > -   column\_property()对象
    > -   任何column\_property()的字符串名称或映射列的属性名称

    该文档包含一个使用case()构造的示例，这可能是此处使用的常见构造。和部分

    polymorphic\_on中的独立表达式传播到单表继承子类，以便它们在WHERE /
    JOIN子句中使用，以便像往常一样将行限制到该子类。

    [¶](#change-dc3aefb201de941ad86706e78e661813)

    参考文献：[＃2345](http://www.sqlalchemy.org/trac/ticket/2345)，[＃2238](http://www.sqlalchemy.org/trac/ticket/2238)

-   **[orm] [feature]**在处理Session.dirty等时，IdentitySet支持 -
    操作符与difference()相同。[¶](#change-596c83c399ac6bb626dfd9b5aa932b9c)

    参考文献：[＃2301](http://www.sqlalchemy.org/trac/ticket/2301)

-   **[orm] [feature]**Added new value for Column autoincrement called
    “ignore\_fk”, can be used to force autoincrement on a column that’s
    still part of a ForeignKeyConstraint.
    关系文档中的新示例说明了它的用法。[¶](#change-5c8167d0e62819144052e2a38f39b9ce)

-   **[orm] [bug]**Fixed backref behavior when “popping” the value off
    of a many-to-one in response to a removal from a stale one-to-many -
    the operation is skipped, since the many-to-one has since been
    updated.[¶](#change-31707f56997df996d8e87251b442de49)

    参考文献：[＃2315](http://www.sqlalchemy.org/trac/ticket/2315)

-   **[orm] [bug]**After some years of not doing this, added more
    granularity to the “is X a parent of Y” functionality, which is used
    when determining if the FK on “Y” needs to be “nulled out” as well
    as if “Y” should be deleted with delete-orphan cascade.
    现在测试考虑了父母的Python身份及其身份密钥，以查看Y的最后已知父母是否肯定是X.如果无法做出决定，则会引发StaleDataError。出现此错误的条件相当罕见，要求先前的父项已被垃圾收集，并且以前可能会非常不恰当地更新/删除自从迁移到新父项后的记录，但可能会出现某些情况，即“无声成功”之前发生的这种情况将在模糊不清的情况下出现。到期“Y”会重置“父”跟踪器，这意味着即使X过时，X.remove（Y）也可能会删除Y，但这与之前的行为相同；建议在这种情况下过期X.
    [¶](#change-0597b131afb6950c6095cc7b9d41a22b)

    参考文献：[＃2264](http://www.sqlalchemy.org/trac/ticket/2264)

-   **[orm]
    [bug]**修复了query.get()中布尔上下文中用户映射对象的不恰当评估。也在0.6.9.
    [¶](#change-1c8ec65ea5e475b56844652263a2ae2a)

    参考文献：[＃2310](http://www.sqlalchemy.org/trac/ticket/2310)

-   **[orm]
    [bug]**将缺少的逗号添加到PASSIVE\_RETURN\_NEVER\_SET符号[¶](#change-bd50a6ee2954d91d3f6baec72cde98d0)

    参考文献：[＃2304](http://www.sqlalchemy.org/trac/ticket/2304)

-   **[orm] [bug]** Cls.column.collat​​e（“some
    collat​​ion”）现在可用。也在0.6.9
    [¶](#change-4cdfabe6f7b63319f49ffe1859ae22ef)中

    参考文献：[＃1776](http://www.sqlalchemy.org/trac/ticket/1776)

-   **[orm] [bug]**the value of a composite attribute is now expired
    after an insert or update operation, instead of regenerated in
    place.
    这可确保在使用该值重新生成组合值之前，将先载入在刷新内过期的列值。[¶](#change-7ef516d5f722bd65a4071a3c93af8dcf)

    参考文献：[＃2309](http://www.sqlalchemy.org/trac/ticket/2309)

-   **[orm] [bug]**The fix in also emits the “refresh” event when the
    composite value is loaded on access, even if all column values were
    already present, as is appropriate.
    这修正了依赖于“加载”事件的“可变”扩展，以确保\_parents字典是最新的修复。感谢Scott
    Torborg在这里的测试案例。[¶](#change-05249cc8e387c5a8a616aaae385531e3)

    参考文献：[＃2309](http://www.sqlalchemy.org/trac/ticket/2309)，[＃2308](http://www.sqlalchemy.org/trac/ticket/2308)

-   **[orm] [bug]**Fixed bug whereby a subclass of a subclass using
    concrete inheritance in conjunction with the new ConcreteBase or
    AbstractConcreteBase would fail to apply the subclasses deeper than
    one level to the “polymorphic loader” of each
    base[¶](#change-609fe72c8353d6327b7563d3f1a83b71)

    参考文献：[＃2312](http://www.sqlalchemy.org/trac/ticket/2312)

-   **[orm] [bug]**Fixed bug whereby a subclass of a subclass using the
    new AbstractConcreteBase would fail to acquire the correct
    “base\_mapper” attribute when the “base” mapper was generated,
    thereby causing failures later
    on.[¶](#change-8198da84adbc73e64b436c59dc6a16f3)

    参考文献：[＃2312](http://www.sqlalchemy.org/trac/ticket/2312)

-   **[orm] [bug]**Fixed bug whereby column\_property() created against
    ORM-level column could be treated as a distinct entity when
    producing certain kinds of joined-inh
    joins.[¶](#change-3928c6de9c155292edc1adf1edecb9d3)

    参考文献：[＃2316](http://www.sqlalchemy.org/trac/ticket/2316)

-   **[orm]
    [bug]**修复了元组无意中传递给session.query()时引发的错误格式。也在0.6.9.
    [¶](#change-4a30fc1572fd8ad440dc0246b95e4424)

    参考文献：[＃2297](http://www.sqlalchemy.org/trac/ticket/2297)

-   **[orm]
    [bug]**现在跟踪调用query.join()到单表继承子类，并用于消除额外的WHERE
    ..IN标准通常使用单表继承，因为联接应该适应它。这允许OUTER
    JOIN生成正确的结果，并且在处理单个表继承连接时总体上会产生更少的WHERE标准。[¶](#change-a33290eb16ea6f93b88fc619c1643bec)

    参考文献：[＃2328](http://www.sqlalchemy.org/trac/ticket/2328)

-   **[orm] [bug]** \_\_
    table\_args\_\_现在可以作为空元组以及空字典传递。感谢Fayaz Yusuf
    Khan提供的补丁。[¶](#change-598ef96bfad7670cdec19b24aba4df59)

    参考文献：[＃2339](http://www.sqlalchemy.org/trac/ticket/2339)

-   **[orm] [bug]**Updated warning message when setting delete-orphan
    without delete to no longer refer to 0.6, as we never got around to
    upgrading this to an exception.
    理想情况下，这可能会更好，但这并不是关键。[¶](#change-66ff5c39136a31854eb15d8bb803cb68)

    参考文献：[＃2325](http://www.sqlalchemy.org/trac/ticket/2325)

-   **[orm]
    [bug]**修复了get\_history()引用没有值的复合属性时的错误；为get\_history()添加了关于复合的覆盖范围，否则这只是一个userland函数。[¶](#change-e28cb51839fda175259aa581e046b920)

### 发动机[¶ T0\>](#change-0.7.4-engine "Permalink to this headline")

-   **[engine] [bug]**Fixed bug whereby transaction.rollback() would
    throw an error on an invalidated connection if the transaction were
    a two-phase or savepoint transaction.
    对于普通事务来说，如果连接失效，rollback()是无操作的，所以虽然它不是100％清楚它是否应该是无操作，至少现在该接口是一致的。[T0\>](#change-b0f112949f1f605e403ae19464fd0f72)

    参考文献：[＃2317](http://www.sqlalchemy.org/trac/ticket/2317)

### SQL [¶ T0\>](#change-0.7.4-sql "Permalink to this headline")

-   **[sql] [feature]**The update() construct can now accommodate
    multiple tables in the WHERE clause, which will render an
    “UPDATE..FROM” construct, recognized by Postgresql and MSSQL.
    在MySQL上编译时，将会生成“UPDATE
    t1，t2，..”。如果Column对象用作“values”参数或生成方法中的键，则MySQL还可以在SET子句中针对多个表进行渲染。[¶](#change-16a2053641572c412b6754e5dbf15b08)

    参考文献：[＃2166](http://www.sqlalchemy.org/trac/ticket/2166)，[＃1944](http://www.sqlalchemy.org/trac/ticket/1944)

-   **[sql]
    [feature]**对称为“python\_type”的类型添加访问器，返回特定TypeEngine实例的基本Python类型对象（如果已知），否则引发NotImplementedError
    [¶](#change-7b1b8704940a6df76cfdeaf3ebdaf8bf)

    参考文献：[＃77](http://www.sqlalchemy.org/trac/ticket/77)

-   **[sql] [bug]**related to, made some adjustments to the change from
    regarding the “from” list on a select().
    \_froms集合不再被记忆，因为这简化了各种用例，并且在列已经在表达式中使用之后将列附加到表上时，不需要“警告”
    - select()构造现在将始终生成正确的表达。这里可能没有真实世界的性能。
    select()对象几乎总是临时创建的，希望优化select()的重用的系统将使用“compiled\_cache”特性。调用select.bind时发生的命中已经减少，但绝大多数用户不应该使用“绑定元数据”：）。[¶](#change-93f0d91f5bbe4c6452dfb872bf427219)

    参考文献：[＃2316](http://www.sqlalchemy.org/trac/ticket/2316)，[＃2261](http://www.sqlalchemy.org/trac/ticket/2261)

-   **[sql] [bug]**further tweak to the fix from, so that generative
    methods work a bit better off of cloned (this is almost a non-use
    case though).
    特别是，这允许with\_only\_columns()表现得更加一致。向with\_only\_columns()添加了额外的文档，以阐明预期的行为，这些行为由于。[¶](#change-980730aa57637cb4737a12677e711fb6)

    参考文献：[＃2261](http://www.sqlalchemy.org/trac/ticket/2261)，[＃2319](http://www.sqlalchemy.org/trac/ticket/2319)

### 架构[¶ T0\>](#change-0.7.4-schema "Permalink to this headline")

-   **[schema]
    [feature]**增加了对远程“模式”的新支持：[¶](#change-30eeb63f3664807fb7da0abb1b45863d)

-   **[schema] [feature]**The “extend\_existing” flag on Table now
    allows for the reflection process to take effect for a Table object
    that’s already been defined; when autoload=True and
    extend\_existing=True are both set, the full set of columns will be
    reflected from the Table which will then *overwrite* those columns
    already present, rather than no activity occurring.
    然而，直接存在于自动载入运行中的列将一如既往地使用。[¶](#change-f8b27554125d172552f8afbb264be5ce)

    参考文献：[＃1410](http://www.sqlalchemy.org/trac/ticket/1410)

-   **[schema] [bug]**Fixed bug whereby TypeDecorator would return a
    stale value for \_type\_affinity, when using a TypeDecorator that
    “switches” types, like the CHAR/UUID
    type.[¶](#change-740f1ca9e5f6d1013a43d2f2a3b62e46)

-   **[schema] [bug]**Fixed bug whereby “order\_by=’foreign\_key’”
    option to Inspector.get\_table\_names wasn’t implementing the sort
    properly, replaced with the existing sort
    algorithm[¶](#change-e6f81ac547b821c6e3284e266230443c)

-   **[schema] [bug]**the “name” of a column-level CHECK constraint, if
    present, is now rendered in the CREATE TABLE statement using
    “CONSTRAINT CHECK ”.[¶](#change-d16f46aeda4253c3b9b85c8bbacdeeef)

    参考文献：[＃2305](http://www.sqlalchemy.org/trac/ticket/2305)

-   **[schema]**MetaData() accepts “schema” and “quote\_schema”
    arguments, which will be applied to the same-named arguments of a
    Table or Sequence which leaves these at their default of
    `None`.[¶](#change-82862f893ba8ec9c5f0ee21833ef35a4)

-   **[schema]**
    Sequence接受“quote\_schema”参数[¶](#change-0ee589a6906f82d2282e3743c9ac4052)

-   **[schema]**tometadata() for Table will use the “schema” of the
    incoming MetaData for the new Table if the schema argument is
    explicitly “None”[¶](#change-b47c1358552d546535afa1ac13ce8cc1)

-   **[schema]**添加了CreateSchema和DropSchema DDL结构 -
    它们只接受模式的字符串名称和“quote”标志。[¶](#change-7fbdac893513ac9abb39e64255d2f8b4)

-   **[schema]**When using default “schema” with MetaData, ForeignKey
    will also assume the “default” schema when locating remote table.
    这允许元数据上的“模式”参数应用于任何其他没有“模式”的表对象集合。[¶](#change-efb9e7247339600fac23ba8079daedaa)

-   **[schema]**方言中实现了“has\_schema”方法，但仅适用于Postgresql。礼貌Manlio
    Perillo。[¶](#change-32e0b173bcbaa624549e413ea0c38bda)

    参考文献：[＃1679](http://www.sqlalchemy.org/trac/ticket/1679)

### 的PostgreSQL [¶ T0\>](#change-0.7.4-postgresql "Permalink to this headline")

-   **[postgresql]
    [feature]**向pg.ENUM添加了create\_type构造函数参数。如果为False，则不会执行CREATE
    /
    DROP或检查该类型作为表创建/删除事件的一部分；只有直接调用的create()/
    drop）()方法才能做到这一点。帮助Alembic“离线”脚本。[¶](#change-240e42b2a45d8da58ef70d6352879aa0)

-   **[postgresql] [bug]**
    Postgresql方言记住在创建/删除序列期间处理了特定名称的ENUM。这允许创建/删除序列在没有任何对“checkfirst”的调用的情况下工作，并且也意味着打开“checkfirst”它只需要检查ENUM一次。[¶](#change-fcdadfef6dc24e48c5801555aed80ea6)

    参考文献：[＃2311](http://www.sqlalchemy.org/trac/ticket/2311)

### MySQL的[¶ T0\>](#change-0.7.4-mysql "Permalink to this headline")

-   **[mysql] [bug]** Unicode调整允许最新的pymysql（post 0.4）在Python
    2上传递100％。[¶](#change-87f7d5afd8c8a0001858444e6cd3690a)

### MSSQL [¶ T0\>](#change-0.7.4-mssql "Permalink to this headline")

-   **[mssql] [feature]**解除了SQL
    Server的SAVEPOINT限制。所有测试都通过使用它，但不知道是否有更深层的问题。[¶](#change-a87623bce57b04db403132f2fa33acb1)

    参考文献：[＃822](http://www.sqlalchemy.org/trac/ticket/822)

-   **[mssql] [bug]**repaired the with\_hint() feature which wasn’t
    implemented correctly on MSSQL - usually used for the “WITH
    (NOLOCK)” hint (which you shouldn’t be using anyway !
    改为使用快照隔离:)）[¶](#change-8ce7ab418720d92012440e27a7609754)

    参考文献：[＃2336](http://www.sqlalchemy.org/trac/ticket/2336)

-   **[mssql]
    [bug]**对\_need\_decimal\_fix选项使用新的pyodbc版本检测。[¶](#change-24887a76b4459a4583801f84bf9c9130)

    参考文献：[＃2318](http://www.sqlalchemy.org/trac/ticket/2318)

-   **[mssql] [bug]**不要在SQL Server
    2000上将“表名”转换为NVARCHAR。然而，大多数情况下，黑暗中需要什么咒语才能使PyODBC在FreeTDS
    0.91中完全工作。然而，[](#change-f7f5ed67d9b7d73a8f4cf6aaa054c0c6)

    参考文献：[＃2343](http://www.sqlalchemy.org/trac/ticket/2343)

-   **[mssql]
    [bug]**在检索索引名称列表和索引内的列名称时解码传入值。[¶](#change-426d539458da725fa9abfb7f28580ca7)

    参考文献：[＃2269](http://www.sqlalchemy.org/trac/ticket/2269)

### 杂项[¶ T0\>](#change-0.7.4-misc "Permalink to this headline")

-   **[feature] [ext]**为“变换器”的混合文档添加了一个示例 -
    这是一种混合程序，它将自定义比较器与查询变换可调用结合起来。在调用with\_transformation()的Query上使用新方法。这里的用例是相当实验性的，但仅向Query添加一行代码。[¶](#change-079906bcdf912b0240d809ea2295ab7d)

-   **[bug] [pyodbc]**pyodbc-based dialects now parse the pyodbc
    accurately as far as observed pyodbc strings, including such gems as
    “py3-3.0.1-beta4”[¶](#change-8903fbf1a6a4cb048375458cf67d2ee1)

    参考文献：[＃2318](http://www.sqlalchemy.org/trac/ticket/2318)

-   **[bug]
    [ext]**当没有“default”编译处理程序而不是KeyError时，@compiles修饰器会引发一条信息错误消息。[¶](#change-1ed8ebcf5df5083fc07f342f18c03ac7)

-   **[bug] [examples]**Fixed bug in history\_meta.py example where the
    “unique” flag was not removed from a single-table-inheritance
    subclass which generates columns to put up onto the
    base.[¶](#change-cfcfa2af9f30380f7d1dd29b4b8942c6)

0.7.3 [¶ T0\>](#change-0.7.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2011年10月16日

### 一般[¶ T0\>](#change-0.7.3-general "Permalink to this headline")

-   **[general]**Adjusted the “importlater” mechanism, which is used
    internally to resolve import cycles, such that the usage of
    \_\_import\_\_ is completed when the import of sqlalchemy or
    sqlalchemy.orm is done, thereby avoiding any usage of \_\_import\_\_
    after the application starts new threads, fixes. 也在0.6.9.
    [¶](#change-29ab8f946c75b6324ab4623bb4dbe039)

    参考文献：[＃2279](http://www.sqlalchemy.org/trac/ticket/2279)

### ORM [¶ T0\>](#change-0.7.3-orm "Permalink to this headline")

-   **[orm]**Improved query.join() such that the “left” side can more
    flexibly be a non-ORM selectable, such as a subquery.
    select\_from()中的一个可选项现在将用作左侧，偏向于隐式使用映射实体。如果由于缺少外键而导致加入仍然失败，则错误消息包含此详细信息。感谢IRC上的brianrhude作为测试用例。[¶](#change-ae5b4bf7f08f7c5c83775c1368dad41a)

    参考文献：[＃2298](http://www.sqlalchemy.org/trac/ticket/2298)

-   **[orm]**添加after\_soft\_rollback()会话事件。无论何时发生实际的DBAPI级别回滚，每当调用rollback()时都会无条件触发此事件。此事件专门设计用于在Session.is\_active为True时允许Session进行操作。[¶](#change-6c9416f183df27b183148e9bd94420a1)

    参考文献：[＃2241](http://www.sqlalchemy.org/trac/ticket/2241)

-   **[orm]**在orm.aliased()构造中添加了“adapt\_on\_names”布尔标志。如果名称与实体映射列的名称相同，允许别名()构造将ORM实体链接到包含特定属性的聚合或其他派生形式的可选项。[¶](#change-8cc754ccc2adc294ad252d4bdeb370d0)

-   **[orm]**Added new flag expire\_on\_flush=False to
    column\_property(), marks those properties that would otherwise be
    considered to be “readonly”, i.e. derived from SQL expressions, to
    retain their value after a flush has occurred, including if the
    parent object itself was involved in an
    update.[¶](#change-f10203ba4e7e846b2ba30301f2a94379)

-   **[orm]**Enhanced the instrumentation in the ORM to support Py3K’s
    new argument style of “required kw arguments”, i.e. fn(a, b, \*, c,
    d), fn(a, b, \*args, c, d).
    映射对象的\_\_init\_\_方法的参数签名将被保留，包括所需的kw规则。[¶](#change-dabcd52c3c2100f50821b002f1e3a6a5)

    参考文献：[＃2237](http://www.sqlalchemy.org/trac/ticket/2237)

-   **[orm]**Fixed bug in unit of work whereby detection of “cycles”
    among classes in highly interlinked patterns would not produce a
    deterministic result; thereby sometimes missing some nodes that
    should be considered cycles and causing further issues down the
    road.
    注意这个bug也是0.6；目前不支持。[¶](#change-c4cedeedbd7be98f6ce67dac3e197919)

    参考文献：[＃2282](http://www.sqlalchemy.org/trac/ticket/2282)

-   **[orm]**修复了从0.6开始的各种同义词()相关的回归：

    > -   对同义词做同义词现在起作用。
    > -   针对关系()的同义词可以传递给query.join()，发送给query.options()的选项通过名称传递给query.with\_parent()。

    [¶](#change-01e3a7d2882ae99168675b1632b15b86)

-   **[orm]**Fixed bug whereby mapper.order\_by attribute would be
    ignored in the “inner” query within a subquery eager load. .
    也在0.6.9. [¶](#change-3376d1f0f8fd5692e18be45ec4f9df6d)

    参考文献：[＃2287](http://www.sqlalchemy.org/trac/ticket/2287)

-   **[orm]**身份映射.discard()在内部使用dict.pop（，None）而不是“del”来避免在非确定性gc拆卸期间出现KeyError
    / warning [¶](#change-1eeda31b58b0498795c90858495711b1)

    参考文献：[＃2267](http://www.sqlalchemy.org/trac/ticket/2267)

-   **[orm]**修正了新复合重写中的回归，其中由于缺少导入，deferred =
    True选项失败[¶](#change-b2a626fabeac396bf73fa7b10eaf0786)

    参考文献：[＃2253](http://www.sqlalchemy.org/trac/ticket/2253)

-   **[orm]**复制了“comparator\_factory”参数到composite()，当0.7被释放时被移除。[¶](#change-1cfd554de6fd12bc9bbed36f51379b32)

    参考文献：[＃2248](http://www.sqlalchemy.org/trac/ticket/2248)

-   **[orm]**Fixed bug in query.join() which would occur in a complex
    multiple-overlapping path scenario, where the same table could be
    joined to twice. Thanks *much* to Dave Vitek for the excellent fix
    here.[¶](#change-ecfede670d6323fc4e0c9f2b4c2d4ffa)

    参考文献：[＃2247](http://www.sqlalchemy.org/trac/ticket/2247)

-   **[orm]**当切片为None时，查询会将OFFSET转换为零，以便不调用无用的OFFSET子句。[¶](#change-ca7dab171c5b45294a127e6ae80ee565)

-   **[orm]**修复了边界情况，当新映射器上的关系会在第一个映射器上建立backref时，映射器无法完全更新内部状态。[¶](#change-bfefa86c53e4b97eb19697ef006bac6a)

-   **[orm]**Fixed bug whereby if \_\_eq\_\_() was redefined, a
    relationship many-to-one lazyload would hit the \_\_eq\_\_() and
    fail. 不适用于0.6.9. [¶](#change-35a916ff4e0cd3752176e3645b8e726c)

    参考文献：[＃2260](http://www.sqlalchemy.org/trac/ticket/2260)

-   **[orm]**Calling class\_mapper() and passing in an object that is
    not a “type” (i.e. a class that could potentially be mapped) now
    raises an informative ArgumentError, rather than
    UnmappedClassError.[¶](#change-f3c15c1285778343f7424d1dd8d2dc23)

    参考文献：[＃2196](http://www.sqlalchemy.org/trac/ticket/2196)

-   **[orm]**新的事件挂钩MapperEvents.after\_configured()。在configure()步骤完成并且映射器实际上受到影响后调用。从理论上讲，这个事件在每个应用程序中被调用一次，除非在已经使用现有的映射之后构造新的映射。[¶](#change-f11c11a3ef0b67817b440a0b327c60a3)

-   当一个打开的会话被垃圾回收时，当它们被添加到一个新的会话中时，它所保留的对象将被视为再次被分离出来。**[orm]**这是通过额外的检查来完成的，即前一个“session\_key”实际上并不存在于会话池中。[¶](#change-5c6dee5ef6c553b074703bc9546027b3)

    参考文献：[＃2281](http://www.sqlalchemy.org/trac/ticket/2281)

-   **[orm]**新的声明性功能：

    > -   \_\_declare\_last
    >     \_\_()方法为类方法建立事件侦听器，当映射器通过最后的“configure”步骤完成时将调用该方法。
    > -   \_\_abstract\_\_标志。当这个标记出现在这个类上时，这个类将不会被映射。
    > -   新的帮助类ConcreteBase，AbstractConcreteBase。允许使用声明的具体映射，当调用“configure”映射器步骤时，声明会自动设置“polymorphic\_union”。
    > -   映射器本身具有半私有方法，允许在配置完成后将“with\_polymorphic”分配给映射器。

    [¶](#change-afb3a8e244c8f1d29f26afd5b9a181ba)

    参考文献：[＃2239](http://www.sqlalchemy.org/trac/ticket/2239)

-   **[orm]**Declarative will warn when a subclass’ base uses
    @declared\_attr for a regular column - this attribute does not
    propagate to
    subclasses.[¶](#change-939714d3448edca7f9d13cce0b4ba5cb)

    参考文献：[＃2283](http://www.sqlalchemy.org/trac/ticket/2283)

-   **[orm]**The integer “id” used to link a mapped instance with its
    owning Session is now generated by a sequence generation function
    rather than id(Session), to eliminate the possibility of recycled
    id() values causing an incorrect result, no need to check that
    object actually in the
    session.[¶](#change-a38f4b857777203b02c6fb8320f6ab56)

    参考文献：[＃2280](http://www.sqlalchemy.org/trac/ticket/2280)

-   **[orm]**Behavioral improvement: empty conjunctions such as and\_()
    and or\_() will be flattened in the context of an enclosing
    conjunction, i.e. and\_(x, or\_()) will produce ‘X’ and not ‘X AND
    ()’..[¶](#change-4e682b3609b1baadc8abcfc7bd1a9cfe)

    参考文献：[＃2257](http://www.sqlalchemy.org/trac/ticket/2257)

-   **[orm]**修复了关于计算select()元素的“from”列表的错误。“from”calc现在被延迟，因此如果构造使用尚未附加到表的对象，但稍后与表关联，则它将使用该表作为FROM生成SQL。这种变化深刻影响了FROM列表以及“相关”集合的计算机制，因为一些“子句自适应”方案（这些在ORM中使用非常严重）依赖于这样一个事实，即“froms”通常在适应完成之前缓存集合。返工允许它可以随时清除和重新生成“froms”集合。[¶](#change-9f535715e9461a8906aa9ad3b5766826)

    参考文献：[＃2261](http://www.sqlalchemy.org/trac/ticket/2261)

-   **[orm]**Fixed bug whereby with\_only\_columns() method of Select
    would fail if a selectable were passed.. Also in
    0.6.9.[¶](#change-99995021df97bdd6d7230fd3bf0b14f7)

    参考文献：[＃2270](http://www.sqlalchemy.org/trac/ticket/2270)

### 发动机[¶ T0\>](#change-0.7.3-engine "Permalink to this headline")

-   **[engine]**The recreate() method in all pool classes uses
    self.\_\_class\_\_ to get at the type of pool to produce, in the
    case of subclassing.
    请注意，通常不需要继承池的子类。[¶](#change-fe03967391583f1af44b0523e58c6f32)

    参考文献：[＃2254](http://www.sqlalchemy.org/trac/ticket/2254)

-   **[engine]**Improvement to multi-param statement logging, long lists
    of bound parameter sets will be compressed with an informative
    indicator of the compression taking place.
    异常消息使用相同的改进格式。[¶](#change-c8b58c6c69a06f1d1edd761f2c33f734)

    参考文献：[＃2243](http://www.sqlalchemy.org/trac/ticket/2243)

-   **[engine]**为pool.manage（dbapi）.connect()添加了可选的“sa\_pool\_key”参数，以便不需要序列化args
    [¶](#change-cb1dfd536798db442dde52ee6331cdd4)

-   **[engine]**The entry point resolution supported by create\_engine()
    now supports resolution of individual DBAPI drivers on top of a
    built-in or entry point-resolved dialect, using the standard ‘+’
    notation - it’s converted to a ‘.’ before being resolved as an entry
    point.[¶](#change-81ebdbd8717e73506ce6b46e7f145f52)

    参考文献：[＃2286](http://www.sqlalchemy.org/trac/ticket/2286)

-   **[engine]**为连接中的“return unicode
    detection”步骤添加了一个异常catch
    +警告，允许在NVARCHAR上崩溃的数据库继续初始化，假设没有实现NVARCHAR类型。[¶
    t2 \>](#change-d8e856413f2efc008bfbfc1c10a5421e)

    参考文献：[＃2299](http://www.sqlalchemy.org/trac/ticket/2299)

### 架构[¶ T0\>](#change-0.7.3-schema "Permalink to this headline")

-   修改Column.copy()以使用\_constructor()，默认为self .\_\_
    class\_\_，以便创建新对象。**[schema]**这允许更容易支持Column的子类。[¶](#change-de8c32a6729c83da17177f6a13979717)

    参考文献：[＃2284](http://www.sqlalchemy.org/trac/ticket/2284)

-   **[schema]**Added a slightly nicer \_\_repr\_\_() to SchemaItem
    classes.
    注意这里的repr不能完全支持“repr是构造函数”的想法，因为模式项可以是非常深的嵌套/循环的，有些事情的后期初始化等等。[¶](#change-32308255f47669cee375f30b9c00fd93)

    参考文献：[＃2223](http://www.sqlalchemy.org/trac/ticket/2223)

### 的PostgreSQL [¶ T0\>](#change-0.7.3-postgresql "Permalink to this headline")

-   **[postgresql]**为Index()添加了“postgresql\_using”参数，产生USING子句来指定PG的索引实现。.
    感谢Ryan P.
    Kelly的补丁。[¶](#change-dfbbf7fcd27cee6a40162ad7712796a8)

    参考文献：[＃2290](http://www.sqlalchemy.org/trac/ticket/2290)

-   **[postgresql]**在使用postgresql +
    psycopg2方言时，向create\_engine()添加了client\_encoding参数；使用连接时的值调用psycopg2
    set\_client\_encoding()方法。[¶](#change-ce7825ce219e385bc6db449ec1a37fa4)

    参考文献：[＃1839](http://www.sqlalchemy.org/trac/ticket/1839)

-   **[postgresql]**Fixed bug related to whereby the same modified index
    behavior in PG 9 affected primary key reflection on a renamed
    column.. Also in 0.6.9.[¶](#change-1a2de32673fea06a4118fba7422b3b5e)

    参考文献：[＃2291](http://www.sqlalchemy.org/trac/ticket/2291)，[＃2141](http://www.sqlalchemy.org/trac/ticket/2141)

-   **[postgresql]**
    Table，Sequence的反射函数不再区分大小写。姓名只能在不同的情况下才会有所不同，并且会被正确区分。[¶](#change-a5584939f5bbdeea7e400a4f8440ee72)

    参考文献：[＃2256](http://www.sqlalchemy.org/trac/ticket/2256)

-   **[postgresql]**使用原子计数器作为服务器端游标名称的“随机数”来源；在极少数情况下报道了冲突。[¶](#change-39b479d7d5d6b7bfce6b386c07e71086)

-   **[postgresql]**缩小了在当前搜索路径中反映具有模式的外键引用表时所做的假设；一个显式的模式只有在它实际上与引用表相匹配的时候才会被应用到引用表中，该引用表也有一个明确的模式。以前它假定“当前”模式与完整的search\_path是同义词。[¶](#change-26fee7eb2a113690d6c965d0964e4638)

    参考文献：[＃2249](http://www.sqlalchemy.org/trac/ticket/2249)

### MySQL的[¶ T0\>](#change-0.7.3-mysql "Permalink to this headline")

-   **[mysql]** CREATE
    TABLE会将COLLATE选项放在CHARSET之后，这似乎是MySQL的任意规则的一部分，关于它是否实际工作。也在0.6.9.
    [¶](#change-dd71574d14be141186b7bdcca5c9a7f8)

    参考文献：[＃2225](http://www.sqlalchemy.org/trac/ticket/2225)

-   **[mysql]**为Index构造添加了mysql\_length参数，为索引指定了“length”。[¶](#change-34aeb67581ad7ffc3ae0f6881dd7c33a)

    参考文献：[＃2293](http://www.sqlalchemy.org/trac/ticket/2293)

### 源码[¶ T0\>](#change-0.7.3-sqlite "Permalink to this headline")

-   **[sqlite]**确保从数据库中解析出的非法日期/时间/日期时间字符串引发相同的ValueError，无论C扩展名是否正在使用。[¶](#change-8baaec5ace78d532c085c871572559c6)

### MSSQL [¶ T0\>](#change-0.7.3-mssql "Permalink to this headline")

-   **[mssql]**更改为尝试使用Pyodbc支持FreeTDS
    0.91。这包括当检测到FreeTDS 0.91时字符串绑定以Python
    unicode对象的形式发送，并且CAST（？AS
    NVARCHAR）用于检测表格时。然而，我仍然将Pyodbc + FreeTDS
    0.91行为描述为非常糟糕，但仍有许多查询（如用于反射的查询，这些查询会在Linux上导致核心转储），而且在OSX上它根本不可用，MemoryErrors比比皆是，只是简单的破解unicode支持。[¶](#change-36fa8324de82b137e203587ba0e82d17)

    参考文献：[＃2273](http://www.sqlalchemy.org/trac/ticket/2273)

-   **[mssql]**The behavior of =/!= when comparing a scalar select to a
    value will no longer produce IN/NOT IN as of 0.8; this behavior is a
    little too heavy handed (use in\_() if you want to emit IN) and now
    emits a deprecation warning.
    要立即获得0.8行为并移除警告，可在[http://www.sqlalchemy.org/docs/07/dialects\_mssql.html\#scalar-select-comparisons](http://www.sqlalchemy.org/docs/07/dialects_mssql.html#scalar-select-comparisons)处提供编译器配方以覆盖visit\_binary()的行为。[¶](#change-62130dcfba80f0c29915ea8aabfbe802)

    参考文献：[＃2277](http://www.sqlalchemy.org/trac/ticket/2277)

-   **[mssql]**“0”被接受为limit()的参数，它将产生“TOP
    0”。[¶](#change-b05f07d0da547e8ca3fdddde13481629)

    参考文献：[＃2222](http://www.sqlalchemy.org/trac/ticket/2222)

### 预言[¶ T0\>](#change-0.7.3-oracle "Permalink to this headline")

-   **[oracle]**固定用于zxjdbc方言的ReturningResultProxy
    ..从0.6开始回归。[¶](#change-a7c4980a1f5230b6dddb072ad74b1bcc)

    参考文献：[＃2272](http://www.sqlalchemy.org/trac/ticket/2272)

-   **[oracle]**字符串类型现在在Oracle上生成VARCHAR2，建议将其作为默认VARCHAR。也为Oracle方言添加了显式的VARCHAR2和NVARCHAR2。使用NVARCHAR仍会生成“NVARCHAR2”
    - Oracle上不存在“NVARCHAR” -
    这仍然是“大写字母总是正好给出该”策略的轻微破坏。VARCHAR仍然会根据策略生成“VARCHAR”。如果Oracle将“VARCHAR”定义为他们声称的不同的东西（恕我直言，这种情况永远不会发生），那么类型将可用。[¶](#change-100c2e0f9af568f915d40868c86cd363)

    参考文献：[＃2252](http://www.sqlalchemy.org/trac/ticket/2252)

### 杂项[¶ T0\>](#change-0.7.3-misc "Permalink to this headline")

-   **[types]**超出“precision”和“asdecimal”的浮点类型将被忽略；在此添加弃用警告以及与[¶](#change-b651e9bd5d27c58a581a88d5ae871614)相关的其他文档

    参考文献：[＃2258](http://www.sqlalchemy.org/trac/ticket/2258)

-   **[ext]**
    SQLSoup不会包含在SQLAlchemy的0.8版中；虽然有用，但我们希望保持SQLAlchemy本身专注于一个ORM使用范例。SQLSoup有望很快被第三方项目取代。[¶](#change-94592809a49fc2de7c8eb955f55e91c9)

    参考文献：[＃2262](http://www.sqlalchemy.org/trac/ticket/2262)

-   **[ext]**向AssociationProxy添加了local\_attr，remote\_attr，attr访问器，可以在类级别快速访问代理属性。[¶](#change-0ea049fd6f98a49f4675f411731db74b)

    参考文献：[＃2236](http://www.sqlalchemy.org/trac/ticket/2236)

-   **[ext]**Changed the update() method on association proxy dictionary
    to use a duck typing approach, i.e. checks for “keys”, to discern
    between update({}) and update((a, b)).
    以前，传递一个有元组作为键的字典会被误解为一个序列。[¶](#change-5c74d8048c22d34b8f6e3fea82e57ea5)

    参考文献：[＃2275](http://www.sqlalchemy.org/trac/ticket/2275)

-   **[examples]**调整dictlike-polymorphic.py示例以应用CAST，使其可以在PG，其他数据库上运行。也在0.6.9.
    [¶](#change-6c08f21fbfe0067678dc79a3a4fe76ff)

    参考文献：[＃2266](http://www.sqlalchemy.org/trac/ticket/2266)

0.7.2 [¶ T0\>](#change-0.7.2 "Permalink to this headline")
----------------------------------------------------------

发布于：2011年7月31日

### ORM [¶ T0\>](#change-0.7.2-orm "Permalink to this headline")

-   **[orm]**Feature enhancement: joined and subquery loading will now
    traverse already-present related objects and collections in search
    of unpopulated attributes throughout the scope of the eager load
    being defined, so that the eager loading that is specified via
    mappings or query options unconditionally takes place for the full
    depth, populating whatever is not already populated.
    以前，如果相关的对象或集合已经存在导致不一致的行为（尽管可以节省已加载图形的加载/周期），则此遍历将停止。对于子查询，这意味着子查询发出的附加SELECT语句将无条件地调用，无论现有图的多少已经存在（因此存在争议）。当查询是属性启动的lazyload的结果时，“停止”的先前行为仍然有效，否则当重复遇到相同的相关对象时，“N
    +
    1”风格的集合迭代可能变得不必要地昂贵。还有一个尚未公开的生成查询方法\_with\_invoke\_all\_eagers()，它选择旧/新行为[¶](#change-1739a61f4e8cd25f6b8ab125e4dc5127)

    参考文献：[＃2213](http://www.sqlalchemy.org/trac/ticket/2213)

-   **[orm]**A rework of “replacement traversal” within the ORM as it
    alters selectables to be against aliases of things (i.e. clause
    adaption) includes a fix for multiply-nested any()/has() constructs
    against a joined table
    structure.[¶](#change-a051536230c394b7aa1762379e347b73)

    参考文献：[＃2195](http://www.sqlalchemy.org/trac/ticket/2195)

-   **[orm]**Fixed bug where query.join() + aliased=True from a
    joined-inh structure to itself on relationship() with join condition
    on the child table would convert the lead entity into the joined one
    inappropriately. 也在0.6.9.
    [¶](#change-7cfc8ca67b366824479efed798d288b6)

    参考文献：[＃2234](http://www.sqlalchemy.org/trac/ticket/2234)

-   **[orm]**Fixed regression from 0.6 where Session.add() against an
    object which contained None in a collection would raise an internal
    exception.
    恢复到0.6的行为，即接受None，但显然没有任何东西被持续。理想情况下，带有None或append()的集合至少应该发出一个警告，该警告被认为是0.8.
    [¶](#change-1a864fa03e54fc13755917c5f8b9e4b5)

    参考文献：[＃2205](http://www.sqlalchemy.org/trac/ticket/2205)

-   **[orm]**在无法定位行的对象上加载deferred()属性会引发ObjectDeletedError，而不是稍后失败；改进了ObjectDeletedError中的消息以包含除简单“删除”以外的其他条件。[¶](#change-1bc8115fca741ab8a339a7f655aa525d)

    参考文献：[＃2191](http://www.sqlalchemy.org/trac/ticket/2191)

-   **[orm]**Fixed regression from 0.6 where a get history operation on
    some relationship() based attributes would fail when a lazyload
    would emit; this could trigger within a flush() under certain
    conditions.
    感谢为此提交了良好测试的用户。[¶](#change-f36e6273d56268c70ed5e545bf51c45f)

    参考文献：[＃2224](http://www.sqlalchemy.org/trac/ticket/2224)

-   **[orm]**Fixed bug apparent only in Python 3 whereby sorting of
    persistent + pending objects during flush would produce an illegal
    comparison, if the persistent object primary key is not a single
    integer. 也在0.6.9 [¶](#change-792cce3e71360b029edf5d3c50c4df50)中

    参考文献：[＃2228](http://www.sqlalchemy.org/trac/ticket/2228)

-   **[orm]**Fixed bug whereby the source clause used by query.join()
    would be inconsistent if against a column expression that combined
    multiple entities together. 也在0.6.9
    [¶](#change-2e9b266bc9d8a064d8e2df64b691f537)中

    参考文献：[＃2197](http://www.sqlalchemy.org/trac/ticket/2197)

-   **[orm]**Fixed bug whereby if a mapped class redefined
    \_\_hash\_\_() or \_\_eq\_\_() to something non-standard, which is a
    supported use case as SQLA should never consult these, the methods
    would be consulted if the class was part of a “composite” (i.e.
    non-single-entity) result set. 也在0.6.9.
    [¶](#change-3d44518370e682ece5ea85b6520a24c4)

    参考文献：[＃2215](http://www.sqlalchemy.org/trac/ticket/2215)

-   **[orm]**Added public attribute ”.validators” to Mapper, an
    immutable dictionary view of all attributes that have been decorated
    with the @validates decorator. 礼貌Stefano Fontanelli
    [¶](#change-a3fdfb9e75c58eafef3f473a85141949)

    参考文献：[＃2240](http://www.sqlalchemy.org/trac/ticket/2240)

-   **[orm]**Fixed subtle bug that caused SQL to blow up if:
    column\_property() against subquery + joinedload + LIMIT + order by
    the column property() occurred. . 也在0.6.9
    [¶](#change-c7799003ae3c4017f6c50d5b4174048e)中

    参考文献：[＃2188](http://www.sqlalchemy.org/trac/ticket/2188)

-   **[orm]**
    with\_parent产生的连接条件以及对父代使用“动态”关系时将生成唯一的bindparams，而不是错误地重复相同的bindparam。.
    也在0.6.9. [¶](#change-a26c4de8b069bb0f1d742ca954b24a5a)

    参考文献：[＃2207](http://www.sqlalchemy.org/trac/ticket/2207)

-   **[orm]**在接收到用户参数relationship.order\_by，foreign\_keys，remote\_side等时使用的mapper.polymorphic\_on中添加了相同的“仅列”检查。[¶](#change-6676824fef13b5c985a65ce599197318)

-   **[orm]**Fixed bug whereby comparison of column expression to a
    Query() would not call as\_scalar() on the underlying SELECT
    statement to produce a scalar subquery, in the way that occurs if
    you called it on
    Query().subquery().[¶](#change-13c7fbc21f418ab14248949e4feca96c)

    参考文献：[＃2190](http://www.sqlalchemy.org/trac/ticket/2190)

-   **[orm]**修正了由于在\_decl\_class\_registry中不必要地查找名称而导致从相同名称的超类继承的类失败的声明性错误。[¶](#change-86ea39be50d19682a75bf6d8b6a9d38d)

    参考文献：[＃2194](http://www.sqlalchemy.org/trac/ticket/2194)

-   **[orm]**Repaired the “no statement condition” assertion in Query
    which would attempt to raise if a generative method were called
    after from\_statement() were called.. Also in
    0.6.9.[¶](#change-59cf1b12fed65cf8fec6dc9e7c376536)

    参考文献：[＃2199](http://www.sqlalchemy.org/trac/ticket/2199)

### 发动机[¶ T0\>](#change-0.7.2-engine "Permalink to this headline")

-   **[engine]**如果commit()失败，Connection.begin()提供的上下文管理器将发出rollback()，而不仅仅是发生异常。[¶](#change-0385e1ab6c61e95bc73e698999b3a9d3)

-   **[engine]**Use urllib.parse\_qsl() in Python 2.6 and above, no
    deprecation warning about
    cgi.parse\_qsl()[¶](#change-f04f77f2075dff4e599f01387a3ac100)

    参考文献：[＃1682](http://www.sqlalchemy.org/trac/ticket/1682)

-   **[engine]**添加了mixin类sqlalchemy.ext.DontWrapMixin。用户定义的这种类型的异常在语句执行的上下文中不会包含在StatementException中。[¶](#change-12f69061ac63135f31122ccd030e4137)

-   **[engine]**
    StatementException包装将在消息中显示原始的异常类。[¶](#change-810ad51bfbb5ba21fc145768df376ec8)

-   **[engine]**Failures on connect which raise dbapi.Error will forward
    the error to dialect.is\_disconnect() and set the
    “connection\_invalidated” flag if the dialect knows this to be a
    potentially “retryable” condition. 目前只有Oracle
    ORA-01033被执行。[¶](#change-93add98c10eed840d3b7c907476d4f1c)

    参考文献：[＃2201](http://www.sqlalchemy.org/trac/ticket/2201)

### SQL [¶ T0\>](#change-0.7.2-sql "Permalink to this headline")

-   **[sql]**Fixed two subtle bugs involving column correspondence in a
    selectable, one with the same labeled subquery repeated, the other
    when the label has been “grouped” and loses itself. 影响。[¶
    T0\>](#change-b8a57863c962b6e42184a303176122b6)

    参考文献：[＃2188](http://www.sqlalchemy.org/trac/ticket/2188)

### 架构[¶ T0\>](#change-0.7.2-schema "Permalink to this headline")

-   **[schema]**新特性：所有类型都有with\_variant()方法。产生Variant()的一个实例，这是一种特殊的TypeDecorator，它将根据使用的方言选择不同类型的用法。[¶](#change-401b949c0225e6348b817f4bb541d046)

    参考文献：[＃2187](http://www.sqlalchemy.org/trac/ticket/2187)

-   **[schema]**Added an informative error message when
    ForeignKeyConstraint refers to a column name in the parent that is
    not found. 也在0.6.9. [¶](#change-9bddb9db3d02fbbbb602dbc2e0a8bcad)

-   **[schema]**Fixed bug whereby adaptation of old
    append\_ddl\_listener() function was passing unexpected \*\*kw
    through to the Table event.
    Table没有获取kws，0.6中的MetaData事件会得到“tables =
    somecollection”，这种行为被保留。[¶](#change-fd58411b045a4477dae9c656cd656700)

    参考文献：[＃2206](http://www.sqlalchemy.org/trac/ticket/2206)

-   **[schema]**Fixed bug where “autoincrement” detection on Table would
    fail if the type had no “affinity” value, in particular this would
    occur when using the UUID example on the site that uses TypeEngine
    as the “impl”.[¶](#change-25b1468fb18fd0faf9c058f6fb1f0f70)

-   **[schema]**为TypeEngine对象添加了一个改进的repr()，它将只显示构造函数参数，这些参数是位置或kwargs偏离默认的。[¶](#change-1380c32b42b8ac54c0c0cf0fb67c3e94)

    参考文献：[＃2209](http://www.sqlalchemy.org/trac/ticket/2209)

### 的PostgreSQL [¶ T0\>](#change-0.7.2-postgresql "Permalink to this headline")

-   **[postgresql]**为Index添加了新的“postgresql\_ops”参数，允许为索引列指定PostgreSQL操作符类。Courtesy
    Filip Zyzniewski。[¶](#change-5e7fbb67c30f10c299ecf5f079610643)

    参考文献：[＃2198](http://www.sqlalchemy.org/trac/ticket/2198)

### MySQL的[¶ T0\>](#change-0.7.2-mysql "Permalink to this headline")

-   **[mysql]**修正了OurSQL方言使用ANSI中性引用符号“'”作为XA命令而不是'“'。.
    也在0.6.9. [¶](#change-89bd952e65c8b1c1dd5f09e71b858a1a)

    参考文献：[＃2186](http://www.sqlalchemy.org/trac/ticket/2186)

### 源码[¶ T0\>](#change-0.7.2-sqlite "Permalink to this headline")

-   **[sqlite]**
    SQLite方言不再将反映的默认值的引号剥离，从而允许往返CREATE
    TABLE的工作。这与其他方言也是一致的，这些方言也保持默认的确切形式。[¶](#change-a76d1c5d7fb5742f5907e331f3e060b5)

    参考文献：[＃2189](http://www.sqlalchemy.org/trac/ticket/2189)

### MSSQL [¶ T0\>](#change-0.7.2-mssql "Permalink to this headline")

-   **[mssql]**Adjusted the pyodbc dialect such that bound values are
    passed as bytes and not unicode if the “Easysoft” unix drivers are
    detected. 这与FreeTDS发生的行为相同。如果在某些情况下传递了Python
    unicodes，Easysoft似乎会发生segfault。[¶](#change-600cd2aaea617df4bcb0c1cc8219406a)

### 预言[¶ T0\>](#change-0.7.2-oracle "Permalink to this headline")

-   **[oracle]**添加ORA-00028断开代码，使用cx\_oracle
    \_Error.code获取代码。也在0.6.9.
    [¶](#change-160a70a653da208a38ffb9040ea5726d)

    参考文献：[＃2200](http://www.sqlalchemy.org/trac/ticket/2200)

-   **[oracle]**添加了ORA-01033来断开连接代码，可以在连接事件中捕获代码。[¶](#change-6c87e4c4b4093629e3ba1f02bdf3ab64)

    参考文献：[＃2201](http://www.sqlalchemy.org/trac/ticket/2201)

-   **[oracle]**修复了没有生成正确DDL的oracle.RAW类型。也在0.6.9.
    [¶](#change-03bd66691ff42c3c20f33e7bab730cd1)

    参考文献：[＃2220](http://www.sqlalchemy.org/trac/ticket/2220)

-   **[oracle]**将CURRENT添加到保留字列表中。也在0.6.9.
    [¶](#change-a7992f3b1ebcc0afe915f2e5b81059dc)

    参考文献：[＃2212](http://www.sqlalchemy.org/trac/ticket/2212)

-   **[oracle]**Fixed bug in the mutable extension whereby if the same
    type were used twice in one mapping, the attributes beyond the first
    would not get
    instrumented.[¶](#change-c1007ad607ff9e6ef6af1e934d877593)

-   **[oracle]**修正了可变扩展中的错误，如果设置了None或非对应类型，则会引发错误。现在不接受任何将None分配给所有属性的值，非法值会引发ValueError。[¶](#change-dc447cba87916cdbf0e26b9026b3a710)

### 杂项[¶ T0\>](#change-0.7.2-misc "Permalink to this headline")

-   **[examples]**修复了示例/版本控制测试运行器，不依赖于SQLAlchemy测试库，nosetests必须从examples
    / versioning中运行，以避免setup.cfg打破它。[¶ t2
    \>](#change-4d1214f86691d7af90b6aec2a6000b50)

-   **[examples]**对示例/版本进行调整，以在多级继承情况下选择正确的外键[¶](#change-167aac7d99e8dbb5b0ddd7ea0e5ab0d4)

-   **[examples]**修正属性shard的例子，以0.7风格正确调用绑定参数。[¶](#change-e68d0bc608be6e8845d4b5a7d44194b6)

0.7.1 [¶ T0\>](#change-0.7.1 "Permalink to this headline")
----------------------------------------------------------

发布：2011年6月15日

### 一般[¶ T0\>](#change-0.7.1-general "Permalink to this headline")

-   **[general]**为Python bug
    7511添加了一个解决方法，C扩展构建失败并未在Windows 64位+ VC
    express上引发适当的异常[¶](#change-d964cd2a33f222066a35562de86fea5c)

    参考文献：[＃2184](http://www.sqlalchemy.org/trac/ticket/2184)

### ORM [¶ T0\>](#change-0.7.1-orm "Permalink to this headline")

-   **[orm]**“delete-orphan” cascade is now allowed on self-referential
    relationships - this since SQLA 0.7 no longer enforces “parent with
    no child” at the ORM level; this check is left up to foreign key
    nullability. 与[¶](#change-17de5b36d8997caf117a46a3670a3f8a)有关

    参考文献：[＃1912](http://www.sqlalchemy.org/trac/ticket/1912)

-   **[orm]**修复了新的“可变”扩展以正确地将事件传播给子类；不要为子类创建多个事件侦听器。[¶](#change-92b2af9262983ea532c0f658bfb17f2c)

    参考文献：[＃2180](http://www.sqlalchemy.org/trac/ticket/2180)

-   **[orm]**Modify the text of the message which occurs when the
    “identity” key isn’t detected on flush, to include the common cause
    that the Column isn’t set up to detect auto-increment correctly;.
    也在0.6.8. [¶](#change-c8d8913620eed4ee345ac9d7820ae1a4)

    参考文献：[＃2170](http://www.sqlalchemy.org/trac/ticket/2170)

-   **[orm]**Fixed bug where transaction-level “deleted” collection
    wouldn’t be cleared of expunged states, raising an error if they
    later became transient. 也在0.6.8.
    [¶](#change-83414e0c5ba2231873ec5e6f1f09e4a2)

    参考文献：[＃2182](http://www.sqlalchemy.org/trac/ticket/2182)

### 发动机[¶ T0\>](#change-0.7.1-engine "Permalink to this headline")

-   **[engine]**Deprecate schema/SQL-oriented methods on
    Connection/Engine that were never well known and are redundant:
    reflecttable(), create(), drop(), text(),
    engine.func[¶](#change-efd707a33500efe6db9ee55b32d39216)

-   **[engine]**Adjusted the \_\_contains\_\_() method of a RowProxy
    result row such that no exception throw is generated internally;
    NoSuchColumnError() also will generate its message regardless of
    whether or not the column construct can be coerced to a string..
    Also in 0.6.8.[¶](#change-78e7d60238ce4141107a00fcad3d7fec)

    参考文献：[＃2178](http://www.sqlalchemy.org/trac/ticket/2178)

### SQL [¶ T0\>](#change-0.7.1-sql "Permalink to this headline")

-   **[sql]**Fixed bug whereby metadata.reflect(bind) would close a
    Connection passed as a bind argument.
    从0.6开始的回归。[¶](#change-a536533da35533b9d8846e5ccde035ba)

-   **[sql]**简化选择决定其'.c'集合中的内容的过程。除了传递给select（[]）的原始ClauseList()（它不是一个记录的案例）之外，它的行为是相同的，现在它将被扩展到它的各个列元素中，而不是被忽略。[¶](#change-4f4c4de0d29089abddf8db7cf35a10e6)

### 的PostgreSQL [¶ T0\>](#change-0.7.1-postgresql "Permalink to this headline")

-   **[postgresql]**有关数值数组MATCH运算符的一些单元测试修正。一个潜在的浮点不准确问题已经修复，MATCH运算符的某些测试目前只能在面向EN的语言环境中执行。.
    也在0.6.8. [¶](#change-036a468c7e481fd6d26a23d398c7209b)

    参考文献：[＃2175](http://www.sqlalchemy.org/trac/ticket/2175)

### MySQL的[¶ T0\>](#change-0.7.1-mysql "Permalink to this headline")

-   **[mysql]**单元测试在安装在windows上的MySQL上通过100％。[¶](#change-0cf81608466b1ee490d9df9f2e4eb80c)

-   **[mysql]**删除了在混合大小写名称的窗口上反映MySQL上的表时将失败的“调整大小写”步骤。在对Windows
    MySQL服务器进行了一些实验之后，已经确定这一步并没有真正帮助这种情况。
    MySQL在非Windows平台上不会返回FK名称，并且删除该步骤至少可以让反射的行为更像其他操作系统。这里已经考虑过一个警告，但是它很难确定在什么情况下可以提出这样的警告，所以现在就这么说
    - 增加了一些文档。[¶](#change-766d1ca6ed7112502e017193c6a681e6)

    参考文献：[＃2181](http://www.sqlalchemy.org/trac/ticket/2181)

-   **[mysql]**supports\_sane\_rowcount will be set to False if using
    MySQLdb and the DBAPI doesn’t provide the constants.CLIENT
    module.[¶](#change-b9b78f2fe96924ca3f08b9d15350b202)

### 源码[¶ T0\>](#change-0.7.1-sqlite "Permalink to this headline")

-   **[sqlite]**Accept None from cursor.fetchone() when “PRAGMA
    read\_uncommitted” is called to determine current isolation mode at
    connect time and default to SERIALIZABLE; this to support SQLite
    versions pre-3.3.0 that did not have this
    feature.[¶](#change-8eee0e021de144283ef4bee007693646)

    参考文献：[＃2173](http://www.sqlalchemy.org/trac/ticket/2173)

0.7.0 [¶ T0\>](#change-0.7.0 "Permalink to this headline")
----------------------------------------------------------

发布时间：2011年5月20日

### ORM [¶ T0\>](#change-0.7.0-orm "Permalink to this headline")

-   **[orm]**固定回归在0.7b4（！）中引入由此query.options（someoption（“不存在的名称”））将不会引发错误。此外，还增加了额外的错误捕获功能，以便在该选项尝试构建基于列的元素时进一步修复某些在[¶](#change-dd788f403779ce46f1b284caf86744f1)中定制的错误消息

    参考文献：[＃2069](http://www.sqlalchemy.org/trac/ticket/2069)

-   **[orm]**query.count() emits “count(\*)” instead of
    “count(1)”.[¶](#change-d4667c0cd130250d8c628298a590a146)

    参考文献：[＃2162](http://www.sqlalchemy.org/trac/ticket/2162)

-   **[orm]**Fine tuning of Query clause adaptation when from\_self(),
    union(), or other “select from myself” operation, such that plain
    SQL expression elements added to filter(), order\_by() etc. which
    are present in the nested “from myself” query *will* be adapted in
    the same way an ORM expression element will, since these elements
    are otherwise not easily
    accessible.[¶](#change-eb378c4f08449233f13c8d8f9b93740c)

    参考文献：[＃2155](http://www.sqlalchemy.org/trac/ticket/2155)

-   **[orm]**Fixed bug where determination of “self referential”
    relationship would fail with no workaround for joined-inh subclass
    related to itself, or joined-inh subclass related to a subclass of
    that with no cols in the sub-sub class in the join condition.
    也在0.6.8. [¶](#change-137910b827fa5951d6eaaddedb4ee0fb)

    参考文献：[＃2149](http://www.sqlalchemy.org/trac/ticket/2149)

-   **[orm]**mapper() will ignore non-configured foreign keys to
    unrelated tables when determining inherit condition between parent
    and child class, but will raise as usual for unresolved columns and
    table names regarding the inherited table.
    这是以前已经应用于声明的行为的增强泛化。0.6.8有一个更保守的版本，它并没有从根本上改变连接条件的确定方式。[¶](#change-c391bd5e3f88944f1c0807d34fb45f2b)

    参考文献：[＃2153](http://www.sqlalchemy.org/trac/ticket/2153)

-   **[orm]**当给定实体不是单个完整的类实体或映射器（即列）时调用query.get()是错误的。这是0.6.8中的弃用警告。[¶](#change-1fd991ce05becf2f02fe6b7626ed5533)

    参考文献：[＃2144](http://www.sqlalchemy.org/trac/ticket/2144)

-   **[orm]**Fixed a potential KeyError which under some circumstances
    could occur with the identity map, part
    of[¶](#change-71cf0b71941a427e86274e502d705578)

    参考文献：[＃2148](http://www.sqlalchemy.org/trac/ticket/2148)

-   **[orm]**添加了Query.with\_session()方法，将Query切换为使用不同的会话。[¶](#change-5dbf57f6a88bfe6de8fb836ee68bc8b5)

-   **[orm]**horizontal shard query should use execution options per
    connection as per[¶](#change-faa9884008b31420f7bb380d6ff9fc64)

    参考文献：[＃2131](http://www.sqlalchemy.org/trac/ticket/2131)

-   **[orm]**非主映射器将继承主映射器的\_identity\_class。这样一来，针对通常在继承映射中的类建立的non\_primary将生成与主映射器（也在0.6.8中）的身份映射兼容的结果[¶](#change-b653622696e0f575c1fd2451854ac4cd)

    参考文献：[＃2151](http://www.sqlalchemy.org/trac/ticket/2151)

-   **[orm]**修复了针对“无法为目标列q执行syncrule”发出的错误消息；映射器'X'不映射此列“以引用正确的映射器。.
    也在0.6.8. [¶](#change-4030bddfa4958646441435b3e8495e02)

    参考文献：[＃2163](http://www.sqlalchemy.org/trac/ticket/2163)

-   **[orm]**polymorphic\_union() gets a “cast\_nulls” option, disables
    the usage of CAST when it renders the labeled NULL
    columns.[¶](#change-74b159ca3a99bc5fe6f663d021fbc89e)

    参考文献：[＃1502](http://www.sqlalchemy.org/trac/ticket/1502)

-   **[orm]**polymorphic\_union() renders the columns in their original
    table order, as according to the first table/selectable in the list
    of polymorphic unions in which they appear.
    （除非传递OrderedDict，否则它本身就是无序映射）。[¶](#change-3eb3b816c40c15eed9d6821d323c425a)

-   **[orm]**Fixed bug whereby mapper mapped to an anonymous alias would
    fail if logging were used, due to unescaped % sign in the alias
    name. 也在0.6.8. [¶](#change-9e05f5299c14ba88437debe75cd6021d)

    参考文献：[＃2171](http://www.sqlalchemy.org/trac/ticket/2171)

### SQL [¶ T0\>](#change-0.7.0-sql "Permalink to this headline")

-   **[sql]**Fixed bug whereby nesting a label of a select() with
    another label in it would produce incorrect exported columns.
    除此之外，这会破坏另一个column\_property()的ORM
    column\_property()映射。. 也在0.6.8
    [¶](#change-6969c79eaa9adb98a299ca808a96ba99)中

    参考文献：[＃2167](http://www.sqlalchemy.org/trac/ticket/2167)

-   **[sql]**在确定连接条件时更改了处理，以便仅在两个给定表之间考虑外键错误。也就是说，t1.join（t2）将报告涉及't1'或't2'的FK错误，但涉及't3'的任何错误都将被跳过。这会影响join()，以及ORM关系和继承条件逻辑。[¶](#change-7b39659e3a5787183e7b9f5455b1bf98)

-   **[sql]**当执行过程中的错误处理有一些改进时，确保自动关闭连接在出现异常DBAPI错误时真正关闭。[¶](#change-1abc44fe4928d1fb7b67de993024c975)

-   **[sql]**
    metadata.reflect()和reflection.Inspector()对GC的一些依赖关闭了内部获取的连接，并解决了这个问题。[¶](#change-402e6ed8f3da378e37a1813c62700551)

-   **[sql]**新增显式检查Column
    .name是否被指定为空字符串[¶](#change-a4aa1f5d35bf43355add704f191f639a)

    参考文献：[＃2140](http://www.sqlalchemy.org/trac/ticket/2140)

-   **[sql]**Fixed bug whereby if FetchedValue was passed to column
    server\_onupdate, it would not have its parent “column” assigned,
    added test coverage for all column default assignment patterns.
    也在0.6.8 [¶](#change-adefc09b01691db8adf07315e9824db6)中

    参考文献：[＃2147](http://www.sqlalchemy.org/trac/ticket/2147)

### 的PostgreSQL [¶ T0\>](#change-0.7.0-postgresql "Permalink to this headline")

-   **[postgresql]**修正psycopg2方言中的psycopg2\_version解析。[¶](#change-14212188e4f0bd379551e87f9b85174b)

-   **[postgresql]**修正了影响PG9的错误，因此如果针对名称已更改的列，索引反射将失败。.
    也在0.6.8. [¶](#change-5388cff58c8560a78aca381e346a28c8)

    参考文献：[＃2141](http://www.sqlalchemy.org/trac/ticket/2141)

### MSSQL [¶ T0\>](#change-0.7.0-mssql "Permalink to this headline")

-   **[mssql]**Fixed bug in MSSQL dialect whereby the aliasing applied
    to a schema-qualified table would leak into enclosing select
    statements. 也在0.6.8. [¶](#change-54f2c1f5f537415c50f6115da435a07d)

    参考文献：[＃2169](http://www.sqlalchemy.org/trac/ticket/2169)

### 杂项[¶ T0\>](#change-0.7.0-misc "Permalink to this headline")

-   本节记录了从0.7b4到0.7.0的这些变化。对于什么SQLAlchemy的0.7的新功能的概述，请参阅[http://docs.sqlalchemy.org/en/latest/changelog\_migration\_07.html
    T0\>](http://docs.sqlalchemy.org/en/latest/changelog_migration_07.html)[¶
    T1\>](#change-1d93ec65d8ccdfeddf18f3d0748d91cd)

-   **[documentation]**从ext.mutable文档中删除了“collections.MutableMapping”abc的用法，因为它被错误地使用，并且使得该示例在任何情况下都更难以理解。[¶\<
    / T2\>](#change-1b8c150a713fcfe2bfa9be75de0808d9)

    参考文献：[＃2152](http://www.sqlalchemy.org/trac/ticket/2152)

-   **[examples]**removed the ancient “polymorphic association” examples
    and replaced with an updated set of examples that use declarative
    mixins, “generic\_associations”.
    每个提供一个替代表格布局。[¶](#change-5caeaaa0861dc6502cd2388eece068e4)

-   **[ext]**修复了sqlalchemy.ext.mutable扩展中的错误，其中None没有得到适当的处理，替换事件没有得到适当的处理。[](#change-8cd79396a14e3d4871c28ac127541834)

    参考文献：[＃2143](http://www.sqlalchemy.org/trac/ticket/2143)

0.7.0b4 [¶ T0\>](#change-0.7.0b4 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2011年4月17日

### 一般[¶ T0\>](#change-0.7.0b4-general "Permalink to this headline")

-   **[general]**更改此文件的CHANGES格式。格式更改已应用于0.7版本。[¶](#change-c10e330a6fb6868b79d2f8ea4ca8f2f4)

-   **[general]**现在，“-claclarative”更改将直接列在“-orm”部分下，因为它们密切相关。[¶](#change-568f4ce9f54eaab769ed2bd7d8e4521e)

-   **[general]**
    0.5系列更改已被移至替换CHANGES\_PRE\_05的文件CHANGES\_PRE\_06.
    [¶](#change-33020374149ff987953b51cc27c1d41b)

-   **[general]**
    0.6系列中的0.6.7及更高版本的更新日志现在仅在0.6分支中的CHANGES文件中列出。在0.7的CHANGES文件（即这个文件）中，所有0.6的变化都在它们被应用的0.7节中内联列出（因为所有的0.6变化也都在0.7中）。注意适用于0.6版本的更改，如果存在实现/行为的任何差异。[¶](#change-4b59da9baea961eaaf0893565f87e4a7)

### ORM [¶ T0\>](#change-0.7.0b4-orm "Permalink to this headline")

-   **[orm]**Some fixes to “evaluate” and “fetch” evaluation when
    query.update(), query.delete() are called.
    记录的检索在所有情况下都是在自动刷新之后完成的，并且在发布更新/删除之前，防止未刷新的数据存在以及在评估期间过期的失败对象。[¶](#change-45801dddde8d0c78af04b421301b8307)

    参考文献：[＃2122](http://www.sqlalchemy.org/trac/ticket/2122)

-   **[orm]**重写了在尝试刷新非超类型的子类时发生的异常。[¶](#change-af8e701eaf7ec13322ab104bb650aecb)

    参考文献：[＃2063](http://www.sqlalchemy.org/trac/ticket/2063)

-   **[orm]**当查询选项无法找到目标实体时，还会进行更多措辞调整。解释路径必须来自其中一个根实体。[¶](#change-1fc825ca38aa549debb3965be29f975a)

-   **[orm]**Some fixes to the state handling regarding backrefs,
    typically when autoflush=False, where the back-referenced collection
    wouldn’t properly handle add/removes with no net change. 感谢Richard
    Murri提供的测试案例+补丁。（也在0.6.7）。[¶](#change-1a848298d843da4ca6e3bbb41d8ae1c6)

    参考文献：[＃2123](http://www.sqlalchemy.org/trac/ticket/2123)

-   **[orm]**在UOW中添加了检查，以检测被请求更新或删除包含NULL的主键值的异常情况。[¶](#change-bde26159f4aa960b057cc47bd3c0e866)

    参考文献：[＃2127](http://www.sqlalchemy.org/trac/ticket/2127)

-   **[orm]**一些改进属性历史记录。在0.8版本中可能会有更多的更改，但是现在历史已经被修改，标量历史没有为非现值赋值None的“副作用”。这允许稍微更好地区分None集合和没有实际变化的能力，也影响到它们。[¶](#change-c257d9a6b362baee9ac13f47aada6784)

    参考文献：[＃2127](http://www.sqlalchemy.org/trac/ticket/2127)

-   **[orm]**a “having” clause would be copied from the inside to the
    outside query if from\_self() were used; in particular this would
    break an 0.7 style count() query.
    （也在0.6.7）[¶](#change-99eb10573ae36fd1d9fff5e087a4cfd2)

    参考文献：[＃2130](http://www.sqlalchemy.org/trac/ticket/2130)

-   **[orm]**the Query.execution\_options() method now passes those
    options to the Connection rather than the SELECT statement, so that
    all available options including isolation level and compiled cache
    may be used.[¶](#change-beca9e44abdcdfcfd9daa8cf2d849cf8)

    参考文献：[＃2131](http://www.sqlalchemy.org/trac/ticket/2131)

### 发动机[¶ T0\>](#change-0.7.0b4-engine "Permalink to this headline")

-   **[engine]**如果CPython
    2.x默认启用了C扩展，如果编译失败，它将回退到纯Python。[¶](#change-ab06f7b93d81343ab8080f5e4b808885)

    参考文献：[＃2129](http://www.sqlalchemy.org/trac/ticket/2129)

### SQL [¶ T0\>](#change-0.7.0b4-sql "Permalink to this headline")

-   **[sql]**当传递给SELECT语句而不是Connection时，“compiled\_cache”执行选项现在会引发错误。以前它被完全忽略。我们可能会考虑让这个选项在每个语句级别上工作。[¶](#change-e8fcd9c241670c115a04b0c0a16536b2)

    参考文献：[＃2131](http://www.sqlalchemy.org/trac/ticket/2131)

-   **[sql]**在基础TypeEngine类中还原了“catchall”构造函数，并带有弃用警告。这使得像Integer（11）这样的代码仍然成功。[¶](#change-489c8fdbf96ab63bb53f2a1a861bba4e)

-   **[sql]**Fixed regression whereby MetaData() coming back from
    unpickling did not keep track of new things it keeps track of now,
    i.e. collection of Sequence objects, list of schema
    names.[¶](#change-f00374d634cfacde67965712e5aff348)

    参考文献：[＃2104](http://www.sqlalchemy.org/trac/ticket/2104)

-   **[sql]**The limit/offset keywords to select() as well as the value
    passed to select.limit()/offset() will be coerced to integer.
    （也在0.6.7）[¶](#change-82ab067a38871b8fab4a70169e0ed7ef)

    参考文献：[＃2116](http://www.sqlalchemy.org/trac/ticket/2116)

-   **[sql]**fixed bug where “from” clause gathering from an over()
    clause would be an itertools.chain() and not a list, causing “can
    only concatenate list” TypeError when combined with other
    clauses.[¶](#change-6cf3eb37879e278dcebe3d7eca622bd3)

-   **[sql]**Fixed incorrect usage of ”,” in over() clause being placed
    between the “partition” and “order by”
    clauses.[¶](#change-94181c686d44776e147c618e176fecbb)

    参考文献：[＃2134](http://www.sqlalchemy.org/trac/ticket/2134)

-   **[sql]**在为PrimaryKeyConstraint
    now函数附加事件之前/之后，为所有约束类型的事件之前/之后添加了测试。[¶](#change-d51ca5e1b2cfb62e5942a810d58354f7)

    参考文献：[＃2105](http://www.sqlalchemy.org/trac/ticket/2105)

-   **[sql]**Added explicit true()/false() constructs to expression lib
    - coercion rules will intercept “False”/”True” into these
    constructs.
    在0.6中，构造通常直接转换为字符串，这在0.7中不再被接受。[¶](#change-42aaa6dc1625418edc7375d7ad85c837)

    参考文献：[＃2117](http://www.sqlalchemy.org/trac/ticket/2117)

### 架构[¶ T0\>](#change-0.7.0b4-schema "Permalink to this headline")

-   **[schema]**
    Table上的'useexisting'标志已被新的一对标志'keep\_existing'和'extend\_existing'取代。'extend\_existing'相当于'useexisting'
    -
    返回现有的表，并添加额外的构造函数元素。使用'keep\_existing'，将返回现有表，但不会添加其他构造函数元素
    -
    这些元素仅在新创建表时应用。[¶](#change-631dc3d09fac43240ec00fb355fc6132)

    参考文献：[＃2109](http://www.sqlalchemy.org/trac/ticket/2109)

### 的PostgreSQL [¶ T0\>](#change-0.7.0b4-postgresql "Permalink to this headline")

-   **[postgresql]**现在支持Python 3的Psycopg2.
    [¶](#change-0441092a868aeb0b91d8d24e59c41d75)

-   **[postgresql]**固定支持使用pg8000时的精确数字。[¶](#change-a8605dec5f8e63d728bc927ef61cf975)

    参考文献：[＃2132](http://www.sqlalchemy.org/trac/ticket/2132)

### 源码[¶ T0\>](#change-0.7.0b4-sqlite "Permalink to this headline")

-   **[sqlite]**修正了创建为“REFERENCES
    ”而没有列名的外键反映失败的问题。
    T2\>（也在0.6.7）[¶](#change-3d3d5c73e15d038b45b311224716fa7b)

    参考文献：[＃2115](http://www.sqlalchemy.org/trac/ticket/2115)

### 预言[¶ T0\>](#change-0.7.0b4-oracle "Permalink to this headline")

-   **[oracle]**Using column names that would require quotes for the
    column itself or for a name-generated bind parameter, such as names
    with special characters, underscores, non-ascii characters, now
    properly translate bind parameter keys when talking to cx\_oracle.
    （也在0.6.7）[¶](#change-a04f9e54c60f2a5d5a0591e7e0b563e2)

    参考文献：[＃2100](http://www.sqlalchemy.org/trac/ticket/2100)

-   **[oracle]**Oracle dialect adds use\_binds\_for\_limits=False
    create\_engine() flag, will render the LIMIT/OFFSET values inline
    instead of as binds, reported to modify the execution plan used by
    Oracle. （也在0.6.7）[¶](#change-b3b1ce9d18a4f1b765507ed4c82f7f4d)

    参考文献：[＃2116](http://www.sqlalchemy.org/trac/ticket/2116)

### 杂项[¶ T0\>](#change-0.7.0b4-misc "Permalink to this headline")

-   **[types]** REAL已添加到核心类型。Postgresql，SQL
    Server，MySQL，SQLite支持。请注意，SQL
    Server和MySQL版本中增加了额外的参数，这些方言也可以使用。[¶](#change-57e3cb1dc539a3540bd8469dd0663039)

    参考文献：[＃2081](http://www.sqlalchemy.org/trac/ticket/2081)

-   **[types]**添加@
    event.listens\_for()装饰器，给定目标+事件名称，将装饰函数作为侦听器应用。[¶](#change-d497389785db3672fe86a6119a68b1ab)

    参考文献：[＃2106](http://www.sqlalchemy.org/trac/ticket/2106)

-   现在，AssertionPool存储回溯指示当前检出的连接被获取的位置；
    **[pool]**此回溯报告在第二次并发结账时产生的断言中；礼貌Gunnlaugur
    Briem [¶](#change-af3a34c122e1b93c7637b389b5c8dca8)

    参考文献：[＃2103](http://www.sqlalchemy.org/trac/ticket/2103)

-   **[pool]**The “pool.manage” feature doesn’t use pickle anymore to
    hash the arguments for each
    pool.[¶](#change-0babcdca864d1007baf6c858bdf0377f)

-   **[documentation]**记录的SQLite日期/时间/日期时间类型。（也在0.6.7）[¶](#change-846e0f46d0f5a9d667fe57b1d7c73355)

    参考文献：[＃2029](http://www.sqlalchemy.org/trac/ticket/2029)

-   **[documentation]**修复了可变扩展文档，以显示正确的类型关联方法。[¶](#change-f0da43d53108c83663cf5c8421677f79)

    参考文献：[＃2118](http://www.sqlalchemy.org/trac/ticket/2118)

0.7.0b3 [¶ T0\>](#change-0.7.0b3 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2011年3月20日

### 一般[¶ T0\>](#change-0.7.0b3-general "Permalink to this headline")

-   **[general]**在Pypy下运行时对单元测试有很多修正（礼貌Alex
    Gaynor）。[¶](#change-5612722a30cc5802a707b0c00967f91f)

### ORM [¶ T0\>](#change-0.7.0b3-orm "Permalink to this headline")

-   **[orm]**更改了query.count()的底层方法。query.count()现在在所有情况下都是精确的：

    > 查询。
    > :   from\_self（func.count（literal\_column（“1”）））。标()

    即，“从（）”选择计数（1）“。
    T0\>这会在所有情况下产生子查询，但大大简化了之前尝试执行的所有猜测count()，在许多情况下仍然会失败，特别是当涉及到表连接和其他连接时。如果为其他非常简单的计数生成的子查询确实是个问题，请使用query（func.count()）作为优化。

    [¶](#change-b00ce7472b8519195eaddc530dcd0f9e)

    参考文献：[＃2093](http://www.sqlalchemy.org/trac/ticket/2093)

-   **[orm]**在迭代期间对罕见weakref回调的标识映射进行了一些更改。互斥体已被删除，因为它显然可能导致重入（即在一个线程中）死锁，也许当gc在迭代点收集对象以获得更多内存时。希望“迭代过程中字典发生变化”将非常罕见，因为迭代方法在内部获取单个values()调用中的完整对象列表。注意0.6.7在这里有一个更保守的修复，它仍然保持互斥体。[¶](#change-7d31abf822a2e7e64b102f9796997f9b)

    参考文献：[＃2087](http://www.sqlalchemy.org/trac/ticket/2087)

-   **[orm]**A tweak to the unit of work causes it to order the flush
    along relationship() dependencies even if the given objects don’t
    have any inter-attribute references in memory, which was the
    behavior in 0.5 and earlier, so a flush of Parent/Child with only
    foreign key/primary key set will succeed.
    在保持0.6或更高版本的同时，这不会在flush中产生大量无用的内部依赖性结构，而这些内部依赖性结构并不对应于当前flush中实际的状态。[¶](#change-bfed6815f260e8ac2239597807031e35)

    参考文献：[＃2082](http://www.sqlalchemy.org/trac/ticket/2082)

-   **[orm]**改进了仅当使用加载器选项（通常不正确）查询仅列实体时出现的错误消息，其中父实体不完全存在。[¶
    t2 \>](#change-f888621663e752a17e10e531c6e70078)

    参考文献：[＃2069](http://www.sqlalchemy.org/trac/ticket/2069)

-   **[orm]**Fixed bug in query.options() whereby a path applied to a
    lazyload using string keys could overlap a same named attribute on
    the wrong entity.
    注意0.6.7对此有一个更保守的解决方法。[¶](#change-691e4dcace5092b3faa9e88301875a19)

    参考文献：[＃2098](http://www.sqlalchemy.org/trac/ticket/2098)

### 发动机[¶ T0\>](#change-0.7.0b3-engine "Permalink to this headline")

-   **[engine]**修正了AssertionPool回归bug。[¶](#change-4687c720a53db425d7516c3325af024b)

    参考文献：[＃2097](http://www.sqlalchemy.org/trac/ticket/2097)

-   **[engine]**当指定了无效的方言时，将引发的异常更改为ArgumentError
    [¶](#change-dabd057d91cbbc1025be172472b16366)

    参考文献：[＃2060](http://www.sqlalchemy.org/trac/ticket/2060)

### SQL [¶ T0\>](#change-0.7.0b3-sql "Permalink to this headline")

-   **[sql]**添加了一个完全描述性的错误消息，其中Column是子类，\_make\_proxy()由于构造函数的TypeError而无法复制。在这种情况下，应该实现\_constructor方法。[¶](#change-887e7334d6776bfb4ec1c01f6fb67d4d)

-   **[sql]**为表对象添加了新事件“column\_reflect”。在对象在反射中生成之前接收关于Column的信息字典，并允许修改字典以控制生成的Column的大部分方面，包括键，名称，类型，信息字典。[¶](#change-8a8960a5ec68a2f3af6208fc1b25f4ec)

    参考文献：[＃2095](http://www.sqlalchemy.org/trac/ticket/2095)

-   **[sql]**To help with the “column\_reflect” event being used with
    specific Table objects instead of all instances of Table, listeners
    can be added to a Table object inline with its construction using a
    new argument “listeners”, a list of tuples of the form (, ), which
    are applied to the Table before the reflection process
    begins.[¶](#change-506927bdc1d6192b785d5111a36c591a)

-   **[sql]**Added new generic function “next\_value()”, accepts a
    Sequence object as its argument and renders the appropriate “next
    value” generation string on the target platform, if supported.
    还在Sequence本身提供了“.next\_value()”方法。[¶](#change-fc859aa865a01a4d305dee5ee7edc1ce)

    参考文献：[＃2085](http://www.sqlalchemy.org/trac/ticket/2085)

-   **[sql]**func.next\_value() or other SQL expression can be embedded
    directly into an insert() construct, and if implicit or explicit
    “returning” is used in conjunction with a primary key column, the
    newly generated value will be present in
    result.inserted\_primary\_key.[¶](#change-c53fe13321aabe9b1255beeab83db25c)

    参考文献：[＃2084](http://www.sqlalchemy.org/trac/ticket/2084)

-   **[sql]**为ResultProxy添加访问器“returns\_rows”，“is\_insert”（也在0.6.7中）[¶](#change-5dcae35a30548ea7a895134981194320)

    参考文献：[＃2089](http://www.sqlalchemy.org/trac/ticket/2089)

### 的PostgreSQL [¶ T0\>](#change-0.7.0b3-postgresql "Permalink to this headline")

-   **[postgresql]**为postgresql方言添加了RESERVED\_WORDS。（也在0.6.7）[¶](#change-68e0e1286435ce3f342c12f928e020cb)

    参考文献：[＃2092](http://www.sqlalchemy.org/trac/ticket/2092)

-   **[postgresql]**固定BIT类型以允许“长度”参数，“变化”参数。反思也是固定的。（也在0.6.7）[¶](#change-d2a17779006167796e2a05814a64b40d)

    参考文献：[＃2073](http://www.sqlalchemy.org/trac/ticket/2073)

### MSSQL [¶ T0\>](#change-0.7.0b3-mssql "Permalink to this headline")

-   **[mssql]**Rewrote the query used to get the definition of a view,
    typically when using the Inspector interface, to use
    sys.sql\_modules instead of the information schema, thereby allowing
    views definitions longer than 4000 characters to be fully returned.
    （也在0.6.7）[¶](#change-1310d3a0d8b578fd7875434f5ccac9b5)

    参考文献：[＃2071](http://www.sqlalchemy.org/trac/ticket/2071)

### 火鸟[¶ T0\>](#change-0.7.0b3-firebird "Permalink to this headline")

-   **[firebird]**如果设置为False，create\_engine()上的“implicit\_returning”标志将被接受。（也在0.6.7）[¶](#change-71fef9ae2d4a3fee911550e2dd3956b5)

    参考文献：[＃2083](http://www.sqlalchemy.org/trac/ticket/2083)

### 杂项[¶ T0\>](#change-0.7.0b3-misc "Permalink to this headline")

-   **[declarative]**
    \_\_mapper\_args\_\_中不是“可散列”的参数不会被误认为是可能存在的，可能列参数。（也在0.6.7）[¶](#change-f2aa1ca45ecfe557dbce711ee18b7414)

    参考文献：[＃2091](http://www.sqlalchemy.org/trac/ticket/2091)

-   **[informix]**添加了RESERVED\_WORDS
    informix方言。（也在0.6.7）[¶](#change-048e59b99152e03dc94aece7d4a58bc5)

    参考文献：[＃2092](http://www.sqlalchemy.org/trac/ticket/2092)

-   **[ext]**The horizontal\_shard ShardedSession class accepts the
    common Session argument “query\_cls” as a constructor argument, to
    enable further subclassing of ShardedQuery.
    （也在0.6.7）[¶](#change-0c37ff1205a5698e49e1cd702b6f6aab)

    参考文献：[＃2090](http://www.sqlalchemy.org/trac/ticket/2090)

-   **[examples]**更新了关联，关联代理示例以使用声明式，添加了一个新例子dict\_of\_sets\_with\_default.py，这是一个“推送关联代理”的例子[¶](#change-c9056c5a1b48170ebc2ddf8226ec46b9)

-   **[examples]**烧杯缓存示例允许query\_callable()函数的“query\_cls”参数。（也在0.6.7）[¶](#change-50d97717471ad817c432c80cce080947)

    参考文献：[＃2090](http://www.sqlalchemy.org/trac/ticket/2090)

0.7.0b2 [¶ T0\>](#change-0.7.0b2 "Permalink to this headline")
--------------------------------------------------------------

发布时间：2011年2月19日

### ORM [¶ T0\>](#change-0.7.0b2-orm "Permalink to this headline")

-   **[orm]**Fixed bug whereby Session.merge() would call the load()
    event with one too few
    arguments.[¶](#change-b274fba360c2b009eb105c6c3e69931c)

    参考文献：[＃2053](http://www.sqlalchemy.org/trac/ticket/2053)

-   **[orm]**添加了逻辑，用于防止MapperExtension或SessionExtension中的事件生成为未覆盖的所有方法生成不执行事件。[¶](#change-5f74d0b93a75d1a035e5774a2f3efe4a)

    参考文献：[＃2052](http://www.sqlalchemy.org/trac/ticket/2052)

### SQL [¶ T0\>](#change-0.7.0b2-sql "Permalink to this headline")

-   **[sql]**将EngineEvents事件类重命名为ConnectionEvents。由于这些类永远不会被最终用户代码直接访问，所以这严格地是对最终用户的文档更改。还简化了事件如何链接到内部的引擎和连接。[¶](#change-dc2cf4dea9f417e9de9e08875f99a6e2)

    参考文献：[＃2059](http://www.sqlalchemy.org/trac/ticket/2059)

-   **[sql]**The Sequence() construct, when passed a MetaData() object
    via its ‘metadata’ argument, will be included in CREATE/DROP
    statements within metadata.create\_all() and metadata.drop\_all(),
    including “checkfirst”
    logic.[¶](#change-7299f4b7dbf53dbcd7da7f65a3155088)

    参考文献：[＃2055](http://www.sqlalchemy.org/trac/ticket/2055)

-   **[sql]**如果Column.references()方法有一个外键完全引用给定列，而不仅仅是它的父表，则它返回True。[¶](#change-226a1b45c1480947ae9cd710a9ea6b17)

    参考文献：[＃2064](http://www.sqlalchemy.org/trac/ticket/2064)

### 的PostgreSQL [¶ T0\>](#change-0.7.0b2-postgresql "Permalink to this headline")

-   **[postgresql]**修复了从0.6开始的回归，其中SMALLINT和BIGINT类型都会在整数PK列上生成SERIAL，而不是SMALLINT和BIGSERIAL
    [¶](#change-4b228a39709839285af0e98dcc00a2e5)

    参考文献：[＃2065](http://www.sqlalchemy.org/trac/ticket/2065)

### 杂项[¶ T0\>](#change-0.7.0b2-misc "Permalink to this headline")

-   **[declarative]**固定回归，其中带有内嵌列的对象的composite()将无法初始化。Column对象现在可以与composite()或外部内联，并通过名称或对象引用拉入。[¶](#change-c38fe2e3d383ffe42f0caca46aa19754)

    参考文献：[＃2058](http://www.sqlalchemy.org/trac/ticket/2058)

-   **[declarative]**修复引用旧的@classproperty名称引用@declared\_attr（同样在0.6.7）的错误消息[¶](#change-868f6a352dcb3c48154087013ea5446d)

    参考文献：[＃2061](http://www.sqlalchemy.org/trac/ticket/2061)

-   **[declarative]**
    \_\_table\_args\_\_元组结尾处的字典现在是可选的。[¶](#change-74177071c6a10f9bfc0211cbd13fd13b)

    参考文献：[＃1468](http://www.sqlalchemy.org/trac/ticket/1468)

-   **[ext]**Association proxy now has correct behavior for any(),
    has(), and contains() when proxying a many-to-one scalar attribute
    to a one-to-many collection (i.e. the reverse of the ‘typical’
    association proxy use
    case)[¶](#change-fbab34328d4fe6cc71b895aa96f6e969)

    参考文献：[＃2054](http://www.sqlalchemy.org/trac/ticket/2054)

-   **[examples]**Beaker example now takes into account ‘limit’ and
    ‘offset’, bind params within embedded FROM clauses (like when you
    use union() or from\_self()) when generating a cache
    key.[¶](#change-5f4e8c1c67082ea05fef1c10cf1f5591)

0.7.0b1 [¶ T0\>](#change-0.7.0b1 "Permalink to this headline")
--------------------------------------------------------------

发布时间：2011年2月12日星期六

### 一般[¶ T0\>](#change-0.7.0b1-general "Permalink to this headline")

-   **[general]**新的事件系统，取代所有扩展名，侦听器等。[¶](#change-c4d4e65ccf6d7de7dedaf8e334fd9d16)

    参考文献：[＃1902](http://www.sqlalchemy.org/trac/ticket/1902)

-   **[general]**记录增强[¶](#change-945982ae61324c2ad8e97d0b27c94438)

    参考文献：[＃1926](http://www.sqlalchemy.org/trac/ticket/1926)

-   **[general]**安装程序不再安装鼻插件[¶](#change-f6989c0ecdc122204dd55da78db6a998)

    参考文献：[＃1949](http://www.sqlalchemy.org/trac/ticket/1949)

-   **[general]**
    sys.modules中的“sqlalchemy.exceptions”别名已被删除。基本SQLA例外可通过“from
    sqlalchemy import
    exc”获得。“exc”的“例外”别名现在仍然保留在“sqlalchemy”中，它只是没有修补到sys.modules中。[¶](#change-8789fcdc9fc591ffd61cdf382b03f1bf)

### ORM [¶ T0\>](#change-0.7.0b1-orm "Permalink to this headline")

-   **[orm]**更简洁的query.join形式（target，onclause）[¶](#change-e2528c2304f18c2ce5f5394b38fd2415)

    参考文献：[＃1923](http://www.sqlalchemy.org/trac/ticket/1923)

-   **[orm]**混合属性，implements / supersedes
    synonym()[¶](#change-7ede0cc31794c29e3305ea557cb017ce)

    参考文献：[＃1903](http://www.sqlalchemy.org/trac/ticket/1903)

-   **[orm]**重写组合[¶](#change-5ff099f70239c548b3bc388c7870d61d)

    参考文献：[＃2008](http://www.sqlalchemy.org/trac/ticket/2008)

-   **[orm]**突变事件扩展，取代“mutable = True”

    也可以看看

    [Mutation event extension, supersedes
    “mutable=True”](migration_07.html#migration-mutation-extension)

    [¶](#change-9933b5cedb94b7f32e325d86e65a33ab)

-   **[orm]**默认关闭PickleType和ARRAY可变性[¶](#change-452cd1cadc41336c00209963c1a0efec)

    参考文献：[＃1980](http://www.sqlalchemy.org/trac/ticket/1980)

-   **[orm]**简化的polymorphic\_on赋值[¶](#change-fa249f9f1f872acaf7380e30c7058dfb)

    参考文献：[＃1895](http://www.sqlalchemy.org/trac/ticket/1895)

-   **[orm]**允许没有父母的孤儿进行冲洗[¶](#change-65fcae8bce879fde267e5bc2176105d2)

    参考文献：[＃1912](http://www.sqlalchemy.org/trac/ticket/1912)

-   **[orm]**在autocommit =
    True的情况下提交之前调整的刷新记帐步骤发生。这允许autocommit =
    True与expire\_on\_commit =
    True一起正常工作，并且还允许post-flush会话挂钩在与autocommit =
    False相同的事务上下文中操作。[¶](#change-dd6608b232dab23abed7950caa675c94)

    参考文献：[＃2041](http://www.sqlalchemy.org/trac/ticket/2041)

-   **[orm]**收集成员时产生的警告，标量指示不属于flush
    [¶](#change-586a512ca20f542fb0b3dc90624687c0)

    参考文献：[＃1973](http://www.sqlalchemy.org/trac/ticket/1973)

-   **[orm]**非表 -
    衍生的结构可以映射[¶](#change-de6d90bab81e4535b80a9aaec843aae3)

    参考文献：[＃1876](http://www.sqlalchemy.org/trac/ticket/1876)

-   **[orm]**查询改进[¶](#change-9f98e54eee44096194e20016e063a63f)中的元组标签名称

    参考文献：[＃1942](http://www.sqlalchemy.org/trac/ticket/1942)

-   **[orm]**映​​射列属性首先引用最具体的列[¶](#change-d7e002896ff0028a50064856662321b7)

    参考文献：[＃1892](http://www.sqlalchemy.org/trac/ticket/1892)

-   **[orm]**映​​射到两个或多个同名列的连接需要显式声明[¶](#change-f59d4965cb5e9d7d9ba76a7bae137d5d)

    参考文献：[＃1896](http://www.sqlalchemy.org/trac/ticket/1896)

-   **[orm]**Mapper requires that polymorphic\_on column be present in
    the mapped selectable[¶](#change-13e4c4103063e6adbaaedc9649f9c1fe)

    参考文献：[＃1875](http://www.sqlalchemy.org/trac/ticket/1875)

-   **[orm]**
    compile\_mappers()重命名为configure\_mappers()，简化了配置内部[¶](#change-2dabcc2d64dee7e464a3d9ff742f95b4)

    参考文献：[＃1966](http://www.sqlalchemy.org/trac/ticket/1966)

-   **[orm]**the aliased() function, if passed a SQL FromClause element
    (i.e. not a mapped class), will return element.alias() instead of
    raising an error on
    AliasedClass.[¶](#change-60d1bd5cee4037cb48cb3ee6c86a3435)

    参考文献：[＃2018](http://www.sqlalchemy.org/trac/ticket/2018)

-   **[orm]**Session.merge() will check the version id of the incoming
    state against that of the database, assuming the mapping uses
    version ids and incoming state has a version\_id assigned, and raise
    StaleDataError if they don’t
    match.[¶](#change-dc30e7fb7d7d28808f8ca91367130826)

    参考文献：[＃2027](http://www.sqlalchemy.org/trac/ticket/2027)

-   **[orm]**
    Session.connection()，Session.execute()接受'bind'，以允许执行/连接操作显式地参与引擎的打开事务。[¶
    t2 \>](#change-191d0bb9d2c5b9df0b3ca39410d088ea)

    参考文献：[＃1996](http://www.sqlalchemy.org/trac/ticket/1996)

-   **[orm]**Query.join(), Query.outerjoin(), eagerload(),
    eagerload\_all(), others no longer allow lists of attributes as
    arguments (i.e. option([x, y, z]) form, deprecated since
    0.5)[¶](#change-ed301a804b81ba5c8f397eed63b643a8)

-   **[orm]**删除了ScopedSession.mapper（自0.5开始弃用）。[¶](#change-74d839b75f6ed3070bb2089114ec518d)

-   **[orm]**水平分片查询将'shard\_id'放置在context.attributes中，它可以通过“load()”事件访问。[¶](#change-220a91af357bdbb12a4ddac587ad3bc6)

    参考文献：[＃2031](http://www.sqlalchemy.org/trac/ticket/2031)

-   **[orm]**跨多个实体的单个contains\_eager()调用将指示沿该路径加载的所有集合，而不是每个端点都要求不同的contains\_eager()调用（这从未正确记录过）[¶
    T2\>](#change-1d6862171baa025c434e161124856982)

    参考文献：[＃2032](http://www.sqlalchemy.org/trac/ticket/2032)

-   **[orm]**The “name” field used in orm.aliased() now renders in the
    resulting SQL
    statement.[¶](#change-eb3d1a3aeabd2864f9d545834fcd8608)

-   **[orm]**会话weak\_instance\_dict =
    False已弃用。[¶](#change-0cf6ed342d196434add59c6825ec0e14)

    参考文献：[＃1473](http://www.sqlalchemy.org/trac/ticket/1473)

-   **[orm]**是0.6.6中的一个警告。[¶](#change-1ee59f0d4bd130bb4f4e3b46008c4f81)

    参考文献：[＃2046](http://www.sqlalchemy.org/trac/ticket/2046)

-   **[orm]**Query.distinct() now accepts column expressions as \*args,
    interpreted by the Postgresql dialect as DISTINCT ON
    ().[¶](#change-04563633a2d6f4ae487b736e7b6940fc)

    参考文献：[＃1069](http://www.sqlalchemy.org/trac/ticket/1069)

-   **[orm]**Additional tuning to “many-to-one” relationship loads
    during a flush().
    版本0.6.6（[ticket：2002]）的更改要求在刷新期间可能会发生更多“不必要”的m2o加载。额外的加载模式已被添加，以便在这个特定用例中发出的SQL被修剪回来，同时仍然检索flush所需的信息以避免遗漏任何东西。[](#change-38da3ba0231e5a2247b5a85e512c64af)

    参考文献：[＃2049](http://www.sqlalchemy.org/trac/ticket/2049)

-   **[orm]**传递给attributes.get\_history()的“passive”的值应该是属性包中定义的常量之一。发送True或False不推荐使用。[¶](#change-cd5eacd2ab6529a6aced3f60d15768f1)

-   **[orm]**为Query.subquery()添加了名称参数，以允许将固定名称分配给别名对象。（也在0.6.7）[¶](#change-06edae870b218a7c13eae46fc5fef29d)

    参考文献：[＃2030](http://www.sqlalchemy.org/trac/ticket/2030)

-   **[orm]**当连接表继承映射程序在本地映射表上没有主键（但在超类表上有pks）时，会发出警告。（也在0.6.7）[¶](#change-95089bbf3908e1e43535422631fcd73c)

    参考文献：[＃2019](http://www.sqlalchemy.org/trac/ticket/2019)

-   **[orm]**Fixed bug where “middle” class in a polymorphic hierarchy
    would have no ‘polymorphic\_on’ column if it didn’t also specify a
    ‘polymorphic\_identity’, leading to strange errors upon refresh,
    wrong class loaded when querying from that target.
    在使用单个表继承时也会发出正确的WHERE标准。（也在0.6.7）[¶](#change-92bbd3ad95fb22126cc39a64783f97a8)

    参考文献：[＃2038](http://www.sqlalchemy.org/trac/ticket/2038)

-   **[orm]**Fixed bug where a column with a SQL or server side default
    that was excluded from a mapping with include\_properties or
    exclude\_properties would result in UnmappedColumnError.
    （也在0.6.7）[¶](#change-0734871e34b4de0cfa57a987165f3e25)

    参考文献：[＃1995](http://www.sqlalchemy.org/trac/ticket/1995)

-   **[orm]**在异常情况下发生警告，即在取消引用父对象后发生集合上的附加事件或类似事件，这会阻止父会话在会话中被标记为“脏”
    。这在0.7中是个例外。（也在0.6.7）[¶](#change-c0ff4c4fbb4211eee4b16aa8804e09e1)

    参考文献：[＃2046](http://www.sqlalchemy.org/trac/ticket/2046)

### SQL [¶ T0\>](#change-0.7.0b1-sql "Permalink to this headline")

-   **[sql]**Added over() function, method to FunctionElement classes,
    produces the \_Over() construct which in turn generates “window
    functions”, i.e. “ OVER (PARTITION BY , ORDER BY
    )”.[¶](#change-4eb7f2aa59933bfc4c2322c448c1238f)

    参考文献：[＃1844](http://www.sqlalchemy.org/trac/ticket/1844)

-   **[sql]** LIMIT /
    OFFSET子句现在使用绑定参数[¶](#change-008af6797c834ccbbd51f2ae2c7fba1b)

    参考文献：[＃805](http://www.sqlalchemy.org/trac/ticket/805)

-   **[sql]**select.distinct() now accepts column expressions as \*args,
    interpreted by the Postgresql dialect as DISTINCT ON ().
    请注意，这已通过将列表传递给distinct关键字参数以用于select()。[¶](#change-77f1c98a5680d59107e84241644a0c9e)

    参考文献：[＃1069](http://www.sqlalchemy.org/trac/ticket/1069)

-   **[sql]**select.prefix\_with() accepts multiple expressions (i.e.
    \*expr), ‘prefix’ keyword argument to select() accepts a list or
    tuple.[¶](#change-a0fb484c1222b50996aa723baba384f1)

-   **[sql]**Passing a string to the distinct keyword argument of
    select() for the purpose of emitting special MySQL keywords
    (DISTINCTROW etc.) 已弃用 -
    为此使用prefix\_with()。[¶](#change-df9bfaf8018c8b1539a0b4c8a07550c8)

-   **[sql]**
    TypeDecorator使用主键列[¶](#change-9112c97367c753c162923d518d541ed0)

    参考文献：[＃2006](http://www.sqlalchemy.org/trac/ticket/2006)，[＃2005](http://www.sqlalchemy.org/trac/ticket/2005)

-   **[sql]**
    DDL()构造现在转义百分号[¶](#change-fc71ca433aef5e4ec0d6b0d752fd6b2e)

    参考文献：[＃1897](http://www.sqlalchemy.org/trac/ticket/1897)

-   **[sql]**Table.c / MetaData.tables refined a bit, don’t allow direct
    mutation[¶](#change-f3cb599e9c46745a4bf2b2b7201214bf)

    参考文献：[＃1917](http://www.sqlalchemy.org/trac/ticket/1917)，[＃1893](http://www.sqlalchemy.org/trac/ticket/1893)

-   **[sql]**传递给bindparam()的callables不会被评估[¶](#change-9b51a25af44112e886144cd60fa90f62)

    参考文献：[＃1950](http://www.sqlalchemy.org/trac/ticket/1950)

-   **[sql]** types.type\_map现在是private，types.\_type\_map
    [¶](#change-d22c8592021bf7d745621ed05d7429f1)

    参考文献：[＃1870](http://www.sqlalchemy.org/trac/ticket/1870)

-   **[sql]**强调非公有池方法[¶](#change-1c2d3bb55bfa7910f19563447af291d6)

    参考文献：[＃1982](http://www.sqlalchemy.org/trac/ticket/1982)

-   **[sql]**添加了NULLS FIRST和NULLS
    LAST支持。它作为asc()和desc()运算符的扩展实现，称为nullsfirst()和nullslast()。[¶](#change-192c99cfcb4e50b3886277fbd4c9a212)

    参考文献：[＃723](http://www.sqlalchemy.org/trac/ticket/723)

-   **[sql]**可以使用字符串作为列名内联表创建Index()构造，作为在表外创建索引的替代方法。[T2\>](#change-8a34b5293403955387df1c3e2d0a0a41)

-   **[sql]**execution\_options() on Connection accepts
    “isolation\_level” argument, sets transaction isolation level for
    that connection only until returned to the connection pool, for
    those backends which support it (SQLite,
    Postgresql)[¶](#change-62c7aacfaee859d90d792e30c31ac9bc)

    参考文献：[＃2001](http://www.sqlalchemy.org/trac/ticket/2001)

-   **[sql]**A TypeDecorator of Integer can be used with a primary key
    column, and the “autoincrement” feature of various dialects as well
    as the “sqlite\_autoincrement” flag will honor the underlying
    database type as being
    Integer-based.[¶](#change-f93d9cab78c0153cf9fb0a71c0ea0259)

    参考文献：[＃2005](http://www.sqlalchemy.org/trac/ticket/2005)

-   **[sql]**在Integer
    PK列上存在server\_default时建立一致性。SQLA不会预取这些，也不会返回到cursor.lastrowid（DBAPI）中。确保所有后端在result.inserted\_primary\_key中始终返回无。关于这种情况的反思，除了在我们检测到序列默认值的PG
    SERIAL col的情况下，对server\_default的int PK
    col的反映将“autoincrement”标志设置为False。[¶](#change-4913415ba5d037bab37eccc00e534daa)

    References: [\#2020](http://www.sqlalchemy.org/trac/ticket/2020),
    [\#2021](http://www.sqlalchemy.org/trac/ticket/2021)

-   **[sql]**Result-row processors are applied to pre-executed SQL
    defaults, as well as cursor.lastrowid, when determining the contents
    of
    result.inserted\_primary\_key.[¶](#change-523eaa86a6fb8bbbe523f6ff4320e065)

    参考文献：[＃2006](http://www.sqlalchemy.org/trac/ticket/2006)

-   **[sql]**Bind parameters present in the “columns clause” of a select
    are now auto-labeled like other “anonymous” clauses, which among
    other things allows their “type” to be meaningful when the row is
    fetched, as in result row
    processors.[¶](#change-64b01c67299868c1e98b5a3c2f0c472a)

-   **[sql]**
    TypeDecorator存在于“sqlalchemy”导入空间中。[¶](#change-ecc90be10a16dfffd1ad51bf80e0de25)

-   **[sql]**Non-DBAPI errors which occur in the scope of an execute()
    call are now wrapped in sqlalchemy.exc.StatementError, and the text
    of the SQL statement and repr() of params is included.
    这使得更容易识别在DBAPI涉及之前失败的语句执行。[¶](#change-fb26558eb829e86d5464e9c8f060232b)

    参考文献：[＃2015](http://www.sqlalchemy.org/trac/ticket/2015)

-   **[sql]**The concept of associating a ”.bind” directly with a
    ClauseElement has been explicitly moved to Executable, i.e. the
    mixin that describes ClauseElements which represent
    engine-executable constructs.
    这种改变是对内部组织的改进，不太可能影响任何实际使用。[¶](#change-a66b20fca49c0f8524e0f9b13450df30)

    参考文献：[＃2048](http://www.sqlalchemy.org/trac/ticket/2048)

-   **[sql]**Column.copy(), as used in table.tometadata(), copies the
    ‘doc’ attribute.
    （也在0.6.7）[¶](#change-a466de1bb8545241b6aa4e22314db722)

    参考文献：[＃2028](http://www.sqlalchemy.org/trac/ticket/2028)

-   **[sql]**Added some defs to the resultproxy.c extension so that the
    extension compiles and runs on Python 2.4.
    （也在0.6.7）[¶](#change-e01bc44c0b8683e725b54e07f17b3db8)

    参考文献：[＃2023](http://www.sqlalchemy.org/trac/ticket/2023)

-   **[sql]**The compiler extension now supports overriding the default
    compilation of expression.\_BindParamClause including that the
    auto-generated binds within the VALUES/SET clause of an
    insert()/update() statement will also use the new compilation rules.
    （也在0.6.7）[¶](#change-eb2cc6cfb9f8870e2eec8d687b2b5f2c)

    参考文献：[＃2042](http://www.sqlalchemy.org/trac/ticket/2042)

-   **[sql]**SQLite dialect now uses NullPool for file-based
    databases[¶](#change-4664bca0e88c4aa7baf8649d823fa11e)

    参考文献：[＃1921](http://www.sqlalchemy.org/trac/ticket/1921)

-   **[sql]**The path given as the location of a sqlite database is now
    normalized via os.path.abspath(), so that directory changes within
    the process don’t affect the ultimate location of a relative file
    path.[¶](#change-4afa9ef114e44f1d7f2ee4ab49ea60b0)

    参考文献：[＃2036](http://www.sqlalchemy.org/trac/ticket/2036)

### 的PostgreSQL [¶ T0\>](#change-0.7.0b1-postgresql "Permalink to this headline")

-   **[postgresql]**When explicit sequence execution derives the name of
    the auto-generated sequence of a SERIAL column, which currently only
    occurs if implicit\_returning=False, now accommodates if the table +
    column name is greater than 63 characters using the same logic
    Postgresql uses.
    （也在0.6.7）[¶](#change-b5ada6099a9b9ba39ca6d8b0c0827b92)

    参考文献：[＃1083](http://www.sqlalchemy.org/trac/ticket/1083)

-   **[postgresql]**在“disconnect”异常列表中添加了额外的libpq消息，“无法从服务器接收数据”（同样在0.6.7中）[¶](#change-05134b7490c95da9c06e6ec525e05543)

    参考文献：[＃2044](http://www.sqlalchemy.org/trac/ticket/2044)

### MySQL的[¶ T0\>](#change-0.7.0b1-mysql "Permalink to this headline")

-   **[mysql]**
    pymysql的新的DBAPI支持，它是MySQL-python的纯Python端口。[¶](#change-7d80eda9ae55c5d7135bf452c7420586)

    参考文献：[＃1991](http://www.sqlalchemy.org/trac/ticket/1991)

-   **[mysql]**oursql dialect accepts the same “ssl” arguments in
    create\_engine() as that of MySQLdb.
    （也在0.6.7）[¶](#change-b7f58cb72e13cc5af0d1da04d82b64d3)

    参考文献：[＃2047](http://www.sqlalchemy.org/trac/ticket/2047)

### MSSQL [¶ T0\>](#change-0.7.0b1-mssql "Permalink to this headline")

-   **[mssql]**the String/Unicode types, and their counterparts VARCHAR/
    NVARCHAR, emit “max” as the length when no length is specified, so
    that the default length, normally ‘1’ as per SQL server
    documentation, is instead ‘unbounded’.
    对于VARBINARY类型也会发生这种情况。

    这种行为使得这些类型与Postgresql的VARCHAR类型更紧密的兼容，当没有指定长度时，它类似地是无界的。

    [¶](#change-63bd4273775d5a53a36af9dd8ee5b79b)

    参考文献：[＃1833](http://www.sqlalchemy.org/trac/ticket/1833)

### 火鸟[¶ T0\>](#change-0.7.0b1-firebird "Permalink to this headline")

-   **[firebird]**一些调整，以便支持Interbase。FB /
    Interbase版本标识符被分析为一个结构，例如（8,1,1，'interbase'）或（2,1,588，'firebird'），因此可以区分它们。[¶](#change-432e2525c02e26b7c7853622f71b1123)

    参考文献：[＃1885](http://www.sqlalchemy.org/trac/ticket/1885)

### 杂项[¶ T0\>](#change-0.7.0b1-misc "Permalink to this headline")

-   下面详细介绍每项变更：[http://docs.sqlalchemy.org/en/latest/changelog\_migration\_07.html](http://docs.sqlalchemy.org/en/latest/changelog_migration_07.html)
    [¶](#change-d347d88fe254c05459e964fb7a9d3005)

-   **[declarative]**添加了一个显式检查，用于名称'metadata'用于声明类的列属性的情况。（也在0.6.7）[¶](#change-f4bd4cade780402e38c5ce23e28051cb)

    参考文献：[＃2050](http://www.sqlalchemy.org/trac/ticket/2050)


