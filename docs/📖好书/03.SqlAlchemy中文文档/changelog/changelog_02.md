---
title: changelog_02
date: 2021-02-20 22:41:27
permalink: /sqlalchemy/83b36d/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
0.2 Changelog [¶](#changelog "Permalink to this headline")
==========================================================

0.2.8 [¶ T0\>](#change-0.2.8 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 9 月 5 日

-   清理连接方法+文档。在查询字符串中指定的自定义 DBAPI 参数，'create\_engine'的'connect\_args'参数或通过'creator'函数创建自定义创建函数到'create\_engine'。[¶](#change-3bbadb0e14ad8a356003b9897cb91e87)

-   在池中添加了“recycle”参数，在 create\_engine 上是“pool\_recycle”，默认为 3600 秒；在这个年龄段之后的连接将被关闭并替换为新的，以处理自动关闭陈旧连接的 db
    [¶](#change-74b02ececd1ed7dfe95d6a425751c152)

    参考文献：[＃274](http://www.sqlalchemy.org/trac/ticket/274)

-   用连接池改变了“无效”语义；将指示底层连接记录在下次调用时重新连接。如果在对 connection.cursor()的底层调用中发生任何错误，“invalidate”也将自动被调用。这将有望允许连接池重新连接到已停止并启动而不重新启动连接应用程序的数据库[¶](#change-891655bb143a645ffda95f976413f7e4)

    参考文献：[＃121](http://www.sqlalchemy.org/trac/ticket/121)

-   eesh！教程 doctest 已经打破了一段时间。[¶](#change-210fa589aa63e27cbcd167e3d413bd4a)

-   add\_property() method on mapper does a “compile all mappers” step
    in case the given property references a non-compiled mapper (as it
    did in the case of the tutorial
    !)[¶](#change-0689db83c9414012f77d5ac5be7dad82)

-   在创建[¶](#change-6dd4134b65e78d4e47e987a1214fc28a)之前检查已存在的 pg 序列

    参考文献：[＃277](http://www.sqlalchemy.org/trac/ticket/277)

-   if a contextual session is established via
    MapperExtension.get\_session (as it is using the sessioncontext
    plugin, etc), a lazy load operation will use that session by default
    if the parent object is not persistent with a session
    already.[¶](#change-d42420b8e77c60ee21356f414d9890fd)

-   对于没有数据库标识的对象，惰性加载不会触发（为什么？请参阅[http://www.sqlalchemy.org/trac/wiki/WhyDontForeignKeysLoadData](http://www.sqlalchemy.org/trac/wiki/WhyDontForeignKeysLoadData)）[¶](#change-14d08d0b2284b0d741b1607953a9c6cb)

-   工作单元可更好地检查属于“删除孤儿”级联的“孤儿”对象，对于父级不可级联的某些情况，[¶
    T1\>](#change-721c4061d19ede0ca96b182b60e5d466)

-   mappers can tell if one of their objects is an “orphan” based on
    interactions with the attribute package.
    这个检查是基于当对象彼此连接和分离时为每个关系维护的状态标志。[¶](#change-fac2a3b6748371c68b935a45f19d6e6a)

-   现在使用“delete-orphan”声明一个自引用关系是无效的（因为上述检查会使它们无法保存）[¶](#change-031952863e78271a6465312378851202)

-   当工作单元试图将它们作为关系的一部分 flush()时，改进了对作为会话一部分的对象的检查。[¶](#change-b95860b65d50a5e16644a3a7090677c9)

-   语句执行支持在表达式中多次使用相同的 BindParam 对象；简化位置参数的处理。Bill
    Noon 很好地理解了基本思想。[¶](#change-aa5e5306b0d71cd750994e09e8191826)

    参考文献：[＃280](http://www.sqlalchemy.org/trac/ticket/280)

-   使用 pg\_schema 表移动 postgres 反射，可以用 use\_information\_schema =
    create\_engine 的真实参数覆盖。[¶](#change-0be4a1e8c04f9408aad86c3b03efb039)

    References: [\#60](http://www.sqlalchemy.org/trac/ticket/60),
    [\#71](http://www.sqlalchemy.org/trac/ticket/71)

-   添加了 MetaData，Table，Column 的 case\_sensitive 参数，根据父模式项是否具有标志的非 None 设置自动确定自身，如果不是，则标识符名称是全部小写还是不。当设置为 True 时，引用应用于具有混合或大写标识符的标识符。引用也会在所有情况下自动应用于已知为保留字或包含其他非标准字符的标识符。各种数据库方言可以覆盖所有这些行为，但是目前他们都使用默认行为。用 postgres，mysql，sqlite，oracle 进行测试。需要使用 firebird，ms-sql 进行更多测试。与[¶](#change-18aeba9b6838ec86beda042ba1d8ebd1)正在进行的工作的一部分

    参考文献：[＃155](http://www.sqlalchemy.org/trac/ticket/155)

-   单元测试更新为在没有安装任何 pysqlite 的情况下运行；池测试使用模拟 DBAPI
    [¶](#change-6890864b32d49c0993860a394a3ca922)

-   网址支持密码[¶](#change-5d0ce32e4eab9c49742272a0546562b9)中的转义字符

    参考文献：[＃281](http://www.sqlalchemy.org/trac/ticket/281)

-   在 UNION 查询中添加了限制/偏移量（尽管尚未在 oracle 中）[¶](#change-69829bd44736e35b59f6af5eb1bc3824)

-   在 DateTime 和 Time 类型中添加了“timezone =
    True”标志。到目前为止，postgres 会将其转换为“TIME [STAMP]（WITH |
    WITHOUT）TIME
    ZONE”，以便对时区存在的控制更加可控（psycopg2 返回带有 tzinfo 的日期时间（如果可用的话，这可能会导致对日期时间的混淆）
    [¶ T0\>](#change-76b257b9178528b6903fdfbacb5deb90)

-   使用 query.count()修复使用不同的，具有 SelectResults 的\*\* kwargs
    count()[¶](#change-4c9c98073c450c62d75b6c9e1c6be295)

    参考文献：[＃287](http://www.sqlalchemy.org/trac/ticket/287)

-   自动加载失败时，从元数据中取消注册 Table；
    [¶](#change-cbd4157fde09c2e29b1106f3ba99d5bb)

    参考文献：[＃289](http://www.sqlalchemy.org/trac/ticket/289)

-   导入 py2.5s sqlite3 [¶](#change-c628d36cd3ecb839d688028cc3c07f4a)

    参考文献：[＃293](http://www.sqlalchemy.org/trac/ticket/293)

-   unicode 修复 startswith()/
    endswith()[¶](#change-675e2de9dc96db028d1fad889acfe61c)

    参考文献：[＃296](http://www.sqlalchemy.org/trac/ticket/296)

0.2.7 [¶ T0\>](#change-0.2.7 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 8 月 12 日星期六

-   设置的引用工具，以便在所有查询/创建/删除中使用针对单个表，模式和列标识符的特定于数据库的引用。通过 Table 或 Column 中的“quote
    = True”以及 Table 中的“quote\_schema = True”启用。感谢 Aaron
    Spike 的出色努力。[¶](#change-f68d31c5108f5178cd9ca5ed2f52188e)

-   assignmapper was setting is\_primary=True, causing all sorts of
    mayhem by not raising an error when redundant mappers were set up,
    fixed[¶](#change-28022343f9e0c1b8eec8a5cfa8770f0c)

-   在映射器中添加了 allow\_null\_pks 选项，允许某些主键列为空的行（即映射到外部连接等时）[¶](#change-f2160b22aae40f4e15a130ce0c1744d8)

-   modifcation to unitofwork to not maintain ordering within the “new”
    list or within the UOWTask “objects” list; instead, new objects are
    tagged with an ordering identifier as they are registered as new
    with the session, and the INSERT statements are then sorted within
    the mapper save\_obj.
    INSERT 顺序基本上一直推到 flush 周期的末尾。这样，在 UOWTask 中发生的各种排序和组织（特别是循环任务排序）不必担心维护顺序（它们不是无论如何）[¶](#change-5cbf0cc0fe21a05f64a43cb5418713a8)

-   固定反映外键以自动加载引用表，如果它尚未加载[¶](#change-b48fef6da67e2ecf70da2c57a64e38de)

-   

    -   将 URL 查询字符串参数传递给 connect()函数

    [¶](#change-455463b280eb3132e92fe54f7734d6f5)

    参考文献：[＃256](http://www.sqlalchemy.org/trac/ticket/256)

-   

    -   oracle 布尔类型

    [¶](#change-3e931a2ab54c0feecb7e62a15a1ed310)

    参考文献：[＃257](http://www.sqlalchemy.org/trac/ticket/257)

-   默认情况下，关系*中的自定义主要/辅助连接条件将*传播到 backrefs。指定 backref()将覆盖此行为。[¶](#change-81bfd9246d95eb794f4c8bfbecf65ba2)

-   better check for ambiguous join conditions in sql.Join; propagates
    to a better error message in PropertyLoader (i.e.
    relation()/backref()) for when the join condition can’t be
    reasonably determined.[¶](#change-ab95309b460511ad583b25a5609ca143)

-   sqlite 在表反射时正确创建 ForeignKeyConstraint 对象。[¶](#change-6e9df47b5d985faac8a19aba9ac31d0e)

-   由于所做的更改而导致的池调整。溢出计数器只应在连接实际成功时递减。添加了一个测试脚本来尝试测试。[¶](#change-b83f55045895c513f494d037e3676755)

    参考文献：[＃224](http://www.sqlalchemy.org/trac/ticket/224)

-   固定 mysql 的默认值反射为 PassiveDefault
    [¶](#change-6639f317c4e35284c4e7434c92765c69)

-   在 MS-SQL 中添加了'tinyint'，'mediumint'类型。[¶](#change-2dd28b0bca11a936a2a7c39234817f58)

    参考文献：[＃263](http://www.sqlalchemy.org/trac/ticket/263)，[＃264](http://www.sqlalchemy.org/trac/ticket/264)

-   SingletonThreadPool 有一个大小并执行一个清理过程，因此只有给定数量的线程本地连接保留（对于集体处理线程的 sqlite 应用程序是必需的）[¶](#change-bbbc83a81584527d32666718a578efdd)

-   使用懒惰加载程序修复小泡菜 bug
    [¶](#change-5420b64df06d75a52fbf5648918bfea5)

    参考文献：[＃267](http://www.sqlalchemy.org/trac/ticket/267)，[＃265](http://www.sqlalchemy.org/trac/ticket/265)

-   修正了 mysql 反射中可能出现的错误，其中某些版本为 SHOW CREATE
    TABLE 调用返回一个数组而不是字符串[¶](#change-cd224ce5fcbe2a9f3baabaca462adb1a)

-   在映射到连接时修复延迟加载[¶](#change-bc6d5f6159746979ffec371aca55f56f)

    参考文献：[＃1770](http://www.sqlalchemy.org/trac/ticket/1770)

-   all create()/drop() calls have a keyword argument of “connectable”.
    “引擎”已被弃用。[¶](#change-f6a82444b216aaf6d5a5f5d28f86e206)

-   修正了 ms-sql connect()与 adodbapi
    [¶](#change-69a4eb2afb9e5e132d1f0946f576a722)

-   在 Select()[¶](#change-a68b1295306f4992d0aacdefb2690416)中添加了“nowait”标志

-   inheritance check uses issubclass() instead of direct \_\_mro\_\_
    check to make sure class A inherits from B, allowing mapper
    inheritance to more flexibly correspond to class
    inheritance[¶](#change-5fb6ec3bc3afd934a7d137242f6bf080)

    参考文献：[＃271](http://www.sqlalchemy.org/trac/ticket/271)

-   在调用聚合时（即 max，min 等），SelectResults 将使用子选择符。在具有 ORDER
    BY 子句的 SelectResults
    [¶](#change-8e0c5881a8bd4d0dcd278f5d50e67358)上

    参考文献：[＃252](http://www.sqlalchemy.org/trac/ticket/252)

-   修复了类型，以便更容易使用特定于数据库的类型；修复了 mysql 文本类型以使用该方法[¶](#change-ed310693d7a6e356cb2bdd490308eccc)

    参考文献：[＃269](http://www.sqlalchemy.org/trac/ticket/269)

-   对 sqlite 日期类型组织[¶](#change-82615419630b2ffbd6f9ce7d4f12932d)的一些修复

-   将 MSTinyInteger 添加到 MS-SQL
    [¶](#change-b5319ee829a2a90ef9a71fea9b6ad83b)

    参考文献：[＃263](http://www.sqlalchemy.org/trac/ticket/263)

0.2.6 [¶ T0\>](#change-0.2.6 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 7 月 20 日

-   big overhaul to schema to allow truly composite primary and foreign
    key constraints, via new ForeignKeyConstraint and
    PrimaryKeyConstraint objects.
    主键/外键创建的现有方法尚未更改，但在幕后使用这些新对象。表格创建和反射现在更多地面向表格而不是列面向。[¶](#change-f8f62c879ce023c4b5a34014b6a07e0e)

    参考文献：[＃76](http://www.sqlalchemy.org/trac/ticket/76)

-   对 MapperExtension 调用方案进行了大修，之前的工作并不完善[¶](#change-77fcf46249de1df2311dcc5841a81672)

-   调整为 ActiveMapper，支持自引用关系[¶](#change-3e7930f4e1f7db2df2614a03b648a0d4)

-   稍微重新安排到 objectstore（在 activemapper /
    threadlocal 中），以便 SessionContext 被'.context'引用而不是直接子类化。[¶](#change-88865e828653eacf13fd80f9f9c2699e)

-   activemapper will use threadlocal’s objectstore if the mod is
    activated when activemapper is
    imported[¶](#change-88eda57ebf8024f3f435fb8ec29d769a)

-   对 URL 正则表达式的小修复，允许在其中包含'@'的文件名[¶](#change-9e2123c55cfece3d0453cd0f4facf76f)

-   修复 Session expunge / update / etc
    ...需要更多的清理[¶](#change-b249794857f4ffef83824b29eb577243)

-   select\_table 映射器*静态*并不总是编译[¶](#change-1e0443db2dd1ddadf93ed4e1637c9100)

-   修正了布尔数据类型[¶](#change-6110d6d0c21f6d8574611b4a3931fedb)

-   added count()/count\_by() to list of methods proxied by
    assignmapper; this also adds them to
    activemapper[¶](#change-ee2c3e4930941f8e1b65654539428565)

-   封装在 DBAPIError
    [¶](#change-4df52daf5a58fc301e4a1e627b125995)中的连接异常

-   ActiveMapper now supports autoloading column definitions from the
    database if you supply a \_\_autoload\_\_ = True attribute in your
    mapping inner-class.
    目前这不支持反映任何关系。[¶](#change-bf375e7b928b6b2fa4a0c42c22c38c70)

-   在某些情况下，延迟的列负载可能会在 flush()中搞乱连接状态，这是固定的[¶](#change-7594a508ec44d989e4dc22ca9c08cf72)

-   expunge()不适用于 cascade，fixed。[¶](#change-df8c878cc9c3bc4bc30c295a7d73f671)

-   固定级联操作中潜在的无限循环[¶](#change-288343a3c32f10a42628139244fbe8f1)

-   added “synonym()” function, applied to properties to have a propname
    the same as another, for the purposes of overriding props and
    allowing the original propname to be accessible in
    select\_by().[¶](#change-07327ed0a795f6353c3c638aeed5975d)

-   修复了在子句结构中的输入，它特别有助于与 polymorphic\_union 类型相关的问题（CAST
    /
    ColumnClause 将其类型传播到代理列）[¶](#change-2a08703fcdc6dab5940f3e16b74754a9)

-   mapper compilation work ongoing, someday it’ll work……moved around
    the initialization of MapperProperty objects to be after all mappers
    are created to better handle circular compilations.
    现在所有的属性都会调用 do\_init()方法，如果这样的话，它们更能意识到它们的“继承”状态。[¶](#change-95665b34b7c34a6ed0c412d09c6f8b5a)

-   显式加载显式禁止自引用关系或与继承映射器（也是自引用）的关系[¶](#change-089e0f59d1470ea7c96c1170212b9e0d)

-   在 query.\_get 中减少绑定参数的大小以安抚挑剔的 oracle
    [¶](#change-309f20e1cd0b0511d7f17353f217004a)

    参考文献：[＃244](http://www.sqlalchemy.org/trac/ticket/244)

-   在 table.create()/
    table.drop()以及 table.exists()方法中添加了'checkfirst'参数[¶](#change-8cf76d441e1c43db7d944b29dd3957c7)

    参考文献：[＃234](http://www.sqlalchemy.org/trac/ticket/234)

-   继承[¶](#change-0227275efbac00a91adbe472de048594)的其他一些正在进行的修复

    参考文献：[＃245](http://www.sqlalchemy.org/trac/ticket/245)

-   属性/ backref / orphan /历史跟踪调整像往常一样...
    [¶](#change-920a89b86f9399735f51a77600c9cf8b)

0.2.5 [¶ T0\>](#change-0.2.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 7 月 08 日

-   fixed endless loop bug in select\_by(), if the traversal hit two
    mappers that referenced each
    other[¶](#change-6c5bbff7b5e3d9af04c26c7cf472a488)

-   升级了所有的 unittests 以将'./lib/'插入 sys.path，解决了新的 setuptools
    PYTHONPATH - 查杀行为[¶](#change-59e2b6515f9cf90eab511b44b21c6c21)

-   进一步修复属性/依赖关系/ etc ……
    [¶](#change-a635a07bb0755421e364596ccc416ed3)

-   改进了 DynamicMetaData 未连接时的错误处理[¶](#change-0f308612c0441691991056a9ab1577b2)

-   很大程度上支持 MS-SQL（用 pymssql 测试）[¶](#change-d449f97ddbe9cb671592e5b7821d2555)

-   组中的 UPDATE 和 DELETE 语句的排序现在按照主键值的顺序排列，用于更多的确定性排序[¶](#change-10cb588f38e3ba8028e1fa3d9eda66aa)

-   after\_insert / delete /
    update 现在称为每个对象的映射器扩展，而不是每个对象每个表[¶](#change-736e4b3a6aa7ac48bbd1ed840f55abde)

-   进一步修复/重构映射器编译[¶](#change-efafc61951a6e94fc868a8288241c457)

0.2.4 [¶ T0\>](#change-0.2.4 "Permalink to this headline")
----------------------------------------------------------

发布于：2006 年 6 月 27 日

-   try/except when the mapper sets init.\_\_name\_\_ on a mapped class,
    supports python 2.3[¶](#change-ad79406bdf9ff4dd50cc4712d7ef6ede)

-   固定的错误，其中 threadlocal 引擎仍会自动提交，尽管事务正在进行中[¶](#change-62bf207102cbb650c0a7f8df8bfafa8f)

-   延迟加载和延迟加载操作要求父对象在 Session 中进行操作；而在操作刚刚返回一个空白列表或 None 之前，它现在会引发一个异常。[¶](#change-240cbf4e4d00720bad97b00f9418461a)

-   Session.update() is slightly more lenient if the session to which
    the given object was formerly attached to was garbage collected;
    otherwise still requires you explicitly remove the instance from the
    previous Session.[¶](#change-07be64fc9973f6dd2e46c0d537b52c0a)

-   修复了映射器编译，检查更多错误条件[¶](#change-51b9869ab9d4cf9e77da66d618a94802)

-   小的修复程序加上订购/限制/偏移[¶](#change-03a4cc85caf469f1dc0aff0590a1863a)

-   utterly remarkable: added a single space between ‘CREATE TABLE’ and
    ‘(’ since *that’s how MySQL indicates a non- reserved word…………
……
…………
    tablename.....*[¶](#change-1afa0092b73a4311513258de8d1bfe61)

g/trac/ticket/206)
plainplainplainplainplain
-   更多修复了继承问题，与多对多关系正确地保存[¶](#change-4aadd1394222f4244ef7c8cba4717753)

-   fixed bug when specifying explicit module to mysql
    dialect[¶](#change-8988c487400090a1e553b717bab0ebe8)

-   when QueuePool times out it raises a TimeoutError instead of
    erroneously making another
    connection[¶](#change-343c6000dc8252a15f438367a548099c)

-   Queue.Queue usage in pool has been replaced with a locally modified
    version (works in py2.3/2.4!)
    它使用一个线程.Lock 来进行互斥。这是为了解决在 Queue 的 get()方法中调用 ConnectionFairy 的\_\_del
    \_\_()方法，然后通过 put()方法将其连接返回到 Queue 的报告情况，导致可重入的挂起，除非使用线程.lock。
    [¶ T0\>](#change-90b6ad1a4b48a77cb1587a668db4f7ef)

-   postgres will not place SERIAL keyword on a primary key column if it
    has a foreign key
    constraint[¶](#change-b4f10360f1d0891a0962f3f9c2768aca)

-   cursor() method on ConnectionFairy allows db-specific extension
    arguments to be
    propagated[¶](#change-adea3d7d82966c7931857cae6dd60450)

    参考文献：[＃221](http://www.sqlalchemy.org/trac/ticket/221)

-   延迟加载绑定参数正确地传播列类型[¶](#change-6c1fbbe4abd643ebc8f3ffb21a9af71e)

    参考文献：[＃225](http://www.sqlalchemy.org/trac/ticket/225)

-   新的 MySQL 类型：MSEnum，MSTinyText，MSMediumText，MSLongText 等更多支持 MS 特定长度/精度参数的数值类型补丁 Mike
    Bernson [¶](#change-22f10061c7f8be06b4bdcb04c8b9df8d)

-   修正连接池 invalidate()[¶](#change-352e899ebdf1244cadff3555b1420e2b)

    参考文献：[＃224](http://www.sqlalchemy.org/trac/ticket/224)

0.2.3 [¶ T0\>](#change-0.2.3 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 6 月 17 日星期六

-   overhaul to mapper compilation to be deferred.
    这允许映射器以任何顺序构造，并且当映射器第一次使用时编译它们之间的关系。[¶](#change-8291e03c8c5f2701838ae5d2f8be31c3)

-   修复了级联行为中的一个非常大的速度瓶颈，特别是当 backrefs 正在使用时[¶](#change-9b32bca1789e60d5e16e1edc3a21a32e)

-   属性检测模块已被完全重写；现在它的程度更简单，更清晰，速度更快。属性的“历史”不再是每次更改的微观管理，而是第一次加载实例时创建的“CommittedState”对象的一部分。HistoryArraySet 消失后，列表属性的行为现在更加开放式（即它们不再是集合）。[¶](#change-1c0e73f78920f1f97d78a0e02b7db01f)

-   在内部使用的 py2.4“set”结构，回退到 sets.Set 何时“set”不可用/需要排序[¶](#change-c64bb0af937cfa88844e4ab96b6733fd)

-   修复事务控制，以便重复的 rollback()调用不会失败（当 flush()会在更大的 try
    / except 事务块中引发异常时，会非常糟糕）[¶\< /
    T1\>](#change-8de15dabb0ded4dfee956d664aef38e4)

-   “foreignkey” argument to relation() can also be a list.
    固定的自动外键检测[¶](#change-34c175944f8e671890f062d720dda4b5)

    参考文献：[＃151](http://www.sqlalchemy.org/trac/ticket/151)

-   固定的错误，其中含有模式名称的表没有正确获取 MetaData 对象的索引[¶](#change-c720f31d6d377648e95acdd146d1ed90)

-   固定错误，其中带有重定义的“key”属性的 Column 没有在 ResultProxy
    [中发生类型转换¶](#change-5f5ca83d1dd3a0599d44cfd324640ae3)

    参考文献：[＃207](http://www.sqlalchemy.org/trac/ticket/207)

-   URL 的固定'port'属性是一个整数（如果存在）[¶](#change-ecc83114559345f0a9a3eaa6df5bb4b9)

-   修复了旧 bug，如果多对多映射为“次要”的表有额外的列，删除操作无效[¶](#change-7b441f457cf77d508db40bebef05589b)

-   针对 UNION 查询映射的错误修正[¶](#change-de389a34b53d442e9d0b3b965217ab28)

-   修正不存在 DB 驱动程序[¶](#change-8f30bc9cbea047626bdc2a9439e7b5d9)时抛出的不正确的异常类

-   在反映不存在的表时添加了 NonExistentTable 异常[¶](#change-f46f46103387cad34879ec24046fcf1e)

    参考文献：[＃138](http://www.sqlalchemy.org/trac/ticket/138)

-   针对 ActiveMapper 的一对一后向引用，其他重构的小修复[¶](#change-aafc1f39ed388e24a34c35773df53c20)

-   映​​射类中的重载构造函数从原始类获取\_\_name\_\_和\_\_doc\_\_
    [¶](#change-bb50a7f88718f169a72b62a811969d9f)

-   fixed small bug in selectresult.py regarding mapper
    extension[¶](#change-63471dc1ed02b7737a4624ed9f337f79)

    参考文献：[＃200](http://www.sqlalchemy.org/trac/ticket/200)

-   对 cascade\_mappers 的小调整，目前不是很强大的支持函数[¶](#change-63c68a2ab8ee24aabc39666ea967de89)

-   some fixes to between(), column.between() to propagate typing
    information better[¶](#change-d5c489545664e97beb313f16da2784e8)

    参考文献：[＃202](http://www.sqlalchemy.org/trac/ticket/202)

-   如果一个对象构造失败，不会被添加到会话中[¶](#change-8c5324bac2a3c16712cfe35d35c030fb)

    参考文献：[＃203](http://www.sqlalchemy.org/trac/ticket/203)

-   CAST 函数已经在 ansicompiler 中用自己的编译函数编写成自己的子句对象；允许 MySQL 默默地忽略大多数 CAST 调用，因为 MySQL 似乎只支持带 Date 类型的标准 CAST 语法。与 MySQL 兼容的 CAST 支持字符串，整数等一个 TODO
    [¶](#change-d71618f02787ee9db4cb33bd9b9eb692)

0.2.2 [¶ T0\>](#change-0.2.2 "Permalink to this headline")
----------------------------------------------------------

发行日期：2006 年 6 月 5 日

-   多态继承行为的重大改进，使其能够与邻接列表表结构一起工作[¶](#change-bd742cfd65f6050597926dae4390d9e1)

    参考文献：[＃190](http://www.sqlalchemy.org/trac/ticket/190)

-   主要修复和重构对整体继承关系，更多的单元测试[¶](#change-379544c91d5eb4c6c05ac1b9457687e4)

-   在 create\_engine()[¶](#change-5721b63173344cabdf45367267f595c2)上固定了“echo\_pool”标志

-   修复文档，删除了不正确的信息，close()与 threadlocal 策略一起使用是不安全的（它完全安全！）[¶](#change-c4f0077420c5dcf5a3897967a07a0157)

-   create\_engine()可以将 URL 作为字符串或 unicode
    [¶](#change-388830402ad051c6cdc28d707c1eb34d)

    参考文献：[＃188](http://www.sqlalchemy.org/trac/ticket/188)

-   firebird support partially completed; thanks to James Ralston and
    Brad Clements for their
    efforts.[¶](#change-9b0f96f37a1fed6d2bb5f20ab572737a)

-   Oracle url translation was broken, fixed, will feed host/port/sid
    into cx\_oracle makedsn() if ‘database’ field is present, else uses
    straight TNS name from the ‘host’
    field[¶](#change-615b40df2b68e4c59eab279554f94f0f)

-   使用 unicode 标准修复 query.get()/
    query.load()[¶](#change-3b0a8d2e0dcba1cba0638fd178df5af8)

-   count() function on selectables now uses table primary key or first
    column instead of “1” for criterion, also uses label “rowcount”
    instead of “count”.[¶](#change-8d66948e4fce771b72c1b176af8458dd)

-   获得了基本的“映射到多个表”功能清理，更正确地记录[¶](#change-3e0af16f5eb71a64848fe32af5739cc7)

-   恢复了 global\_connect()函数，并附加到名为“default\_metadata”的 DynamicMetaData 实例。将 MetaData
    arg 保留为 Table
    out 将使用默认元数据。[¶](#change-1258190627b876b0ffe8295ecdd5ffb8)

-   修复了会话级联行为，entity\_name propigation
    [¶](#change-a8160ae0fe8661326e73d97cfa1a5918)

-   将 unittests 重新组织为子目录[¶](#change-8341e0a7cda1491806850d425a74bb8c)

-   更多修正了 threadlocal 连接嵌套模式[¶](#change-0f6562e42a0e8a9b74b9302ca568a13d)

0.2.1 [¶ T0\>](#change-0.2.1 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 5 月 29 日

-   “pool” argument to create\_engine() properly
    propagates[¶](#change-26b387ee2747217a96f6982738dc82ac)

-   修复了 URL，如果不解析，会引发异常，不会传递空白字段到数据库连接字符串（一个字符串，如 user：host
    @ /
    db 在 postgres 上破解）[T1\>](#change-bfd7ab5d5c9af9f46885a6f856400645)

-   当 Mapper 插入并尝试获取新的主键值时对其进行小修改[¶](#change-05ae6d2f0e41b25c9aefe7a65ffb0b98)

-   重写了 TLEngine 的一半，与'strategy
    =“threadlocal”'一起使用了 ComposedSQLEngine。它现在正确地实现了 engine.begin()/
    engine.commit()，它完全嵌套在 connection.begin()/
    trans.commit()中。增加了大约六个单元测试。[¶](#change-9cf0fdd64a8448f403279ba717187a9f)

-   major “duh” in pool.Pool, forgot to put back the
    WeakValueDictionary.
    本来应该检查这个的单元测试也默默地想念它。固定 unittest 以确保 ConnectionFairy 正确地超出范围。[¶](#change-d9a9007ac13e6499a26f44a500fa7c5d)

-   添加到 SingletonThreadPool 的占位符 dispose()方法，不会执行任何操作[¶](#change-d110ae3a45ebc503ac45c8483c5bfc3d)

-   当引发异常时，会自动调用 rollback()，但只有在进程中没有事务时才会自动调用（即，更像自动提交）。[¶](#change-25946e86814860e1bc890e293c2ab638)

-   如果没有 sqlite 模块存在，修复 sqlite 中的异常[¶](#change-7d94f3def3f5ff26407726dd433da955)

-   为关联对象 doc
    [¶](#change-8abad0d2f2c6c44e00ac58e5c17cadb4)添加了额外的示例细节

-   连接添加了已经关闭的检查[¶](#change-bec5627771341c1349121e09bd06b71e)

0.2.0 [¶ T0\>](#change-0.2.0 "Permalink to this headline")
----------------------------------------------------------

发布时间：2006 年 5 月 27 日星期六

-   overhaul to Engine system so that what was formerly the SQLEngine is
    now a ComposedSQLEngine which consists of a variety of components,
    including a Dialect, ConnectionProvider, etc.
    这影响了所有的 db 模块以及 Session 和 Mapper。[¶](#change-eb84c383fb66582cc54c697758830e55)

-   create\_engine now takes only RFC-1738-style strings:
    driver://user:password@host:port/database[¶](#change-89db6fc8f97249a357036010f230d383)

-   total rewrite of connection-scoping methodology, Connection objects
    can now execute clause elements directly, added explicit “close” as
    well as support throughout Engine/ORM to handle closing properly, no
    longer relying upon \_\_del\_\_ internally to return connections to
    the pool.[¶](#change-c962e5efdda3519cd260a842cfbf1633)

    参考文献：[＃152](http://www.sqlalchemy.org/trac/ticket/152)

-   overhaul to Session interface and scoping.
    使用 hibernate 风格的方法，包括 query（class），save()，save\_or\_update()等。默认情况下不安装 threadlocal 作用域。为特定的引擎和/或连接提供绑定接口，以便底层架构对象不需要绑定到引擎。增加了一个基本的 SessionTransaction 对象，可以简化多个引擎之间的事务处理。[¶](#change-258687fe610d04ccd25d09e8b41156a7)

-   overhaul to mapper’s dependency and “cascade” behavior; dependency
    logic factored out of properties.py into a separate module
    “dependency.py”.
    “级联”行为现在可以明确控制，适当执行“删除”，“删除孤儿”等。依赖关系系统现在可以在刷新时间确定子对象是否具有父项，以便更好地决定该子项如何在数据库中进行删除操作。[¶](#change-78e49d8a0a13ccbb005df73ef3366953)

-   overhaul to Schema to build upon MetaData object instead of an
    Engine. 整个 SQL /
    Schema 系统可以在没有任何引擎的情况下使用，仅由显式连接对象执行。“绑定”方法通过模式对象的 BoundMetaData 存在。ProxyEngine 通常不再需要，并由 DynamicMetaData 取代。[¶](#change-485af54d0f5397c314da6e88136207a1)

-   实现了真正的多态行为，修复[¶](#change-3630275017278ecdd227d14ffa6548c8)

    参考文献：[＃167](http://www.sqlalchemy.org/trac/ticket/167)

-   “oid” system has been totally moved into compile-time behavior; if
    they are used in an order\_by where they are not available, the
    order\_by doesn’t get compiled,
    fixes[¶](#change-3d8b1afa02b15535632392487a516dde)

    参考文献：[＃147](http://www.sqlalchemy.org/trac/ticket/147)

-   overhaul to packaging; “mapping” is now “orm”, “objectstore” is now
    “session”, the old “objectstore” namespace gets loaded in via the
    “threadlocal” mod if
    used[¶](#change-8bf8612ef556f0bf755fe718681e6980)

-   现在通过“import ”调用 mods。
    T1\>扩展模式在 mods 中的优势在于 mods 是全局性的 - monkeypatching
    [¶](#change-ffb12a0fc7cadef5121724285bb70b4e)

-   修复 add\_property，使其传播属性以继承 mappers
    [¶](#change-8d8c686814c344c1621cc615bb1d45e8)

    参考文献：[＃154](http://www.sqlalchemy.org/trac/ticket/154)

-   backrefs create themselves against primary mapper of its originating
    property, priamry/secondary join arguments can be specified to
    override.
    帮助他们使用多态映射器[¶](#change-2d36f63ccaebe536de04bc7fecaee573)

-   “表存在”函数已经实现[¶](#change-4ba29fdbbc8becb660237815d53b83e4)

    参考文献：[＃31](http://www.sqlalchemy.org/trac/ticket/31)

-   将“create\_all /
    drop\_all”添加到 MetaData 对象[¶](#change-30c09019de225b41f95bdc0851e58dc7)

    参考文献：[＃98](http://www.sqlalchemy.org/trac/ticket/98)

-   拓扑排序算法的改进和修复，以及更多的单元测试[¶](#change-d7d3b18ab1260ef31dc840caf70b800a)

-   教程页面添加到文档中，也可以使用自定义 doctest 运行器来运行以确保其正常工作。docs 通常会被彻底检查以处理新的代码模式[¶](#change-01b8d39163627d26378163c4770488fd)

-   更多的修复，重构。[¶](#change-3afbbfc302967cb3d9fab98edf0a3603)

-   迁移指南可在维基上的[http://www.sqlalchemy.org/trac/wiki/02Migration](http://www.sqlalchemy.org/trac/wiki/02Migration)
    [¶](#change-16e332fa3928256dced17d268bfd6be4)


