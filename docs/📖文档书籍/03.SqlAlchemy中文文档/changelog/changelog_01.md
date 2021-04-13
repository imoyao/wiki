---
title: changelog_01
date: 2021-02-20 22:41:27
permalink: /sqlalchemy/4209a4/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
0.1 Changelog [¶](#changelog "Permalink to this headline")
==========================================================

0.1.7 [¶ T0\>](#change-0.1.7 "Permalink to this headline")
----------------------------------------------------------

发布：2006 年 5 月 5 日星期五

-   对拓扑排序算法[¶](#change-328a512e45ff41563954cf735897ee07)进行了一些修复

-   增加了对 Postgres 的 DISTINCT ON 支持（只提供 distinct = [col1，col2
    ..]）[¶](#change-5325a0bce730c2af7c68b1e8b502c515)

-   在 sql 表达式中添加了\_\_mod\_\_（％运算符）[¶](#change-accc87ebae193a33b61db683b6fec8cc)

-   “order\_by”从继承映射器继承的映射器属性[¶](#change-bc8de29156fa01e13acccf2275546f2c)

-   修复映射器 UPDATES / DELETEs
    [¶](#change-f19ea4a4ac8a900c9dc69f593a0e6900)时使用的列类型

-   with convert\_unicode =
    True，反射失败，已被修复[¶](#change-a83c4b8c4929f00119792aaa1c7eaad0)

-   类型的类型类型！仍然没有工作……必须再次使用 TypeDecorator：（[¶](#change-0ebe95b934b2c9cbf552ea86f570c164)

-   mysql binary type converts array output to buffer, fixes
    PickleType[¶](#change-f786fe476a97d9670225bd23f8ba525c)

-   一次性修复 attributes.py 内存泄漏[¶](#change-521e5583e06309364169c17d38eb7f4c)

-   unittests 根据支持每一个的数据库进行限定[¶](#change-d68c77086376391b4445c79edfb06222)

-   固定的错误，其中列默认会破坏插入对象的 VALUES 子句[¶](#change-242dbb58a59fc700cebb1daa2705e5c3)

-   固定的错误，其中 table def w / schema
    name 会强制引擎连接[¶](#change-c9e53eccf51d7613c97843b27f3a7c82)

-   fix for parenthesis to work correctly with subqueries in
    INSERT/UPDATE[¶](#change-b6a168bf0634a9bcda214e61709a7525)

-   HistoryArraySet gets extend()
    method[¶](#change-de1f7d90ee947b184fd95d1d18936c18)

-   除了=
    [¶](#change-3712b8eaa2628230b682529674bc06c7)之外，还有其他比较运算符的 lazyload 支持

-   lazyload 修复连接条件中的两个比较指向同一列[¶](#change-703437eb9f40d509b86cd1e57be00e21)

-   向映射器添加了“construct\_new”标志，将使用\_\_new\_\_创建实例而不是\_\_init\_\_（0.2 中的标准）[¶](#change-2c543f7f6cc73846553be1de46163f44)

-   将 selectresults.py 添加到 SVN，上次错过了[¶](#change-f9fa9d970a5c396e116d1950c9607944)

-   通过关联表调整以允许从表到它自己的多对多关系[¶](#change-3c36fc2b9bfcd27a4dda5ecb69d6f689)

-   对多态示例[使用的“translate\_row”函数的小修复](#change-7efce648859a52b729d3ce36573a8ea4)

-   create\_engine 使用 cgi.parse\_qsl 读取查询字符串（在 0.2 窗口之外）[¶](#change-0a39188910ba4ac441e56b3f097f808c)

-   调整为 CAST 运算符[¶](#change-cda9b4e506598541c59a57ac145a70cb)

-   固定函数名称 LOCAL\_TIME / LOCAL\_TIMESTAMP - \> LOCALTIME /
    LOCALTIMESTAMP [¶](#change-223883de925fbd8a3a667c76b3a64e02)

-   在编译[中的 ORDER BY /
    HAVING 的固定顺序¶](#change-2a14156f0b25e17fb67f48a17b96f1d8)

0.1.6 [¶ T0\>](#change-0.1.6 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 4 月 12 日

-   support for MS-SQL added courtesy Rick Morrison, Runar
    Petursson[¶](#change-5ba2973cedb4a955806631a79704e24a)

-   J. Ellis
    [¶](#change-11c6b02ceaba6cbd60d96b1201312fbd)中的最新 SQLSoup

-   ActiveMapper has preliminary support for inheritance (Jeff
    Watkins)[¶](#change-b11804c4b34c595ddd5655238d973fd0)

-   使用函数“install\_mods（\*
    modnames）”添加了一个“mods”系统，该系统允许可插入模块修改/增加核心功能。[¶](#change-0c8a7b899b662206ff1d772c2b4f3c32)

-   added the first “mod”, SelectResults, which modifies mapper selects
    to return generators that turn ranges into LIMIT/OFFSET queries
    (Jonas Borgstr?[¶](#change-5165cff42fd7bc0985c9ee41224ef11d)

-   factored out querying capabilities of Mapper into a separate Query
    object which is Session-centric.
    这提高了 mapper.using（session）的性能，并使其他事情成为可能。[¶](#change-149fa05e8a8b6549f870b65a4fb28173)

-   对象存储/会话重构，保存对象的官方方式现在通过 flush()方法。Session 的开始/提交功能被分解到 LegacySession 中，该功能仍然作为默认行为建立，直到 0.2 系列。[¶](#change-a36fb99cd24021ad222613215b456353)

-   类型系统在查询编译时绑定到引擎，而不是架构构建时间。这简化了类型系统以及 ProxyEngine。[¶](#change-a65412891901f69c41b8cdc59c8bb36b)

-   向 mapper 添加了'version\_id'关键字参数。这个关键字应该引用一个 Integer 类型的 Column 对象，最好是不可为空的，这个对象将被用在映射的表上以跟踪版本号。这个数字在每个保存操作时递增，并在 UPDATE
    /
    DELETE 条件中指定，以便将它计入返回的行计数中，如果收到的值不是预期的计数，将导致并发错误。[¶](#change-e26b0f7145354b8b0b48218c57239ae8)

-   在映射器中添加了“entity\_name”关键字参数。映射器现在通过类对象与一个类关联，并且还有一个可选的 entity\_name 参数，该参数是一个默认为 None 的字符串。可以为一个类创建任意数量的主映射器，并由实体名称限定。这些类的实例将通过它们的 entity\_name 限定的映射器发出所有的加载和保存操作，并为其他等价对象在身份映射中维护一个单独的身份。[¶](#change-b20c12e6962a35663f9e7907d3f36082)

-   overhaul to the attributes system.
    代码已被澄清，并且也被固定为支持对象属性的正确多态行为。[¶](#change-ae9d5b1b522edb1aaf5f83ae171fad0c)

-   在选择对象[¶](#change-94d35e9f98ca35211995921004df4b48)中添加了“for\_update”标志

-   针对 backrefs [¶](#change-84dbe2494396013264b0e9418f3a4312)的一些修复

-   修复 postgres1
    DateTime 类型[¶](#change-0118b76318e46eb69356b600e29d3fe4)

-   文档页面主要切换到 Markdown 语法[¶](#change-36e8bef9adbc229c3632abf04f039a3f)

0.1.5 [¶ T0\>](#change-0.1.5 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 3 月 27 日

-   将 SQLSession 概念添加到了 SQLEngine。此对象跟踪从连接池中检索连接以及正在进行的事务。方法 push\_session()和 pop\_session()被添加到 SQLEngine 中，该方法将新的 SQLSession 推入/引出到引擎上，允许在前一个嵌套的第二个连接上进行操作，从而实现嵌套事务。有关 SQLSession 的其他技巧肯定会在后面讨论。[¶](#change-2ca8013d56b6dab07a13fa06df401dc9)

-   将 nest\_on 参数添加到 objectstore.Session。这是一个单独的 SQLEngine 或每次此 Session 成为活动会话时（通过 objectstore.push\_session()或等价物）调用 push\_session()/
    pop\_session()的引擎列表。这允许工作单元 Session 利用嵌套事务特性而不明确地调用引擎上的 push\_session
    / pop\_session。[¶](#change-f4045660fffd963a8410ee98d837ef82)

-   分解对象库/单元工作以将“会话范围”与“非常繁重”分开[¶](#change-5195877eb353a245cb1854f472e25a63)

-   向 MapperExtension 添加了 populate\_instance()方法。允许扩展来修改对象属性的数量。此方法可以调用另一个映射器上的 populate\_instance()方法将属性填充从一个映射器转换为另一个映射器；一些行翻译逻辑也是内置的，以帮助解决这个问题。[¶](#change-4de8a4632f7933b1084adb014d374356)

-   fixed Oracle8-compatibility “use\_ansi” flag which converts JOINs to
    comparisons with the = and (+) operators, passes basic
    unittests[¶](#change-6fdb3140293afd1a90f4b57c169b4faf)

-   调整到 Oracle LIMIT /
    OFFSET 支持[¶](#change-35a4fde8bed4d24e939847f1e5956647)

-   Oracle 反射使用 ALL \_ \*\*视图而不是 USER \_
    \*\*来从[¶](#change-f3dc289f3cbd1248846531a503f99d73)中获取更大的东西列表

-   修复了 Oracle 外键反映[¶](#change-9b3cdcc692c2b2debfc10c3e578f4c8b)

    参考文献：[＃105](http://www.sqlalchemy.org/trac/ticket/105)

-   objectstore.commit(obj1, obj2,...) adds an extra step to seek out
    private relations on properties and delete child objects, even
    though its not a global
    commit[¶](#change-1f061b72173f923556b4eb90801185fc)

-   lots and lots of fixes to mappers which use inheritance,
    strengthened the concept of relations on a mapper being made towards
    the “local” table for that mapper, not the tables it inherits.
    允许更复杂的组合模式与懒惰/渴望加载一起工作。[¶](#change-951f39b628de9b3af7d07279141ef619)

-   增加了对映射器基于同一个表继承的支持，只需指定与父/子映射器相同的表即可。[¶](#change-03ed46790e5851818fe1ba8ca7e8919f)

-   在实例化和填充新对象方面，对属性系统进行了一些小的改进。[¶](#change-956758d0c5a9f020f9b5ea643cfd900f)

-   修正了 MySQL 二进制单元测试[¶](#change-2834e9ac8a3454fdf8a876db8f4a8812)

-   INSERT 可以接收子句元素作为 VALUES 参数，而不仅仅是文字值[¶](#change-877341d248eb486358fba969a82e689f)

-   支持调用多重派生函数，即 schema.mypkg.func()[¶](#change-417b8c0342e2cb2d037d55d3b3f6935b)

-   added J. Ellis’ SQLSoup module to extensions
    package[¶](#change-14b5686246058f8826cfe6748f8e2f4f)

-   添加了“多态”示例，说明从一个映射器加载多个对象类型的方法，其中第二个使用新的 populate\_instance()方法。对映射程序的小改进，UNION 结构可以帮助[¶](#change-e501c9a6894ed384ec9cf53c45384564)中的例子

-   改进/修复 session.refresh()/
    session.expire()（之前可能被称为“invalidate”..）[¶](#change-98a2bd42701dd1dc96285849497a3bdd)

-   添加了 session.expunge()，它完全从当前会话中删除一个对象[¶](#change-247e750522dc1abf187cc9ebe7c07392)

-   添加了\* args，\*\* kwargs pass-thru to
    engine.transaction（func）允许更容易创建事务化装饰器函数[¶](#change-64fa976573f5286cf2c2170f8284a78f)

-   向 ResultProxy 添加了迭代器接口：“for result in
    result：...”[¶](#change-781ae8e0605a3c7c090b6482c29b3a81)

-   将断言添加到 tx = session.begin()； tx.rollback()；
    tx.begin()，即不能在 rollback()[¶](#change-4383a6acbab6661ad2ea81bfac935cee)之后使用它

-   将绑定参数修复日期转换添加到 SQLite，使日期能够与 pysqlite1 一起使用[¶](#change-654f4afac5ca2f8a18cae6ddecd15869)

-   改进子查询以更智能地构造它们的 FROM 子句[¶](#change-f82409dbff86d8cb28b246262e5c7257)

    参考文献：[＃116](http://www.sqlalchemy.org/trac/ticket/116)

-   将 PickleType 添加到类型中。[¶](#change-a2b5d7a407c4983f40c959349c8e29a6)

-   修正了与绑定参数有关的列标签的两个错误：绑定参数键名，它们现在在所有相关情况下从列“标签”生成以利用超出名称长度的规则，并检查与名为与“tablename\_colname”相同的列的特殊冲突添加了[¶](#change-da20f02923aa0e9ce14a56b9dc980596)

-   对工作单元文档，其他文​​档部分进行大修。[¶](#change-e13c93c92e346b4f9dabda454ec44f8c)

-   固定属性错误，如果一个对象被提交，那么它的延迟加载列表如果没有被加载就会被吹走[¶](#change-43809b3535863fd4ce975b2ea873a830)

-   将 unique\_connection()方法添加到引擎，连接池返回不属于线程本地上下文或任何当前事务的连接[¶](#change-7e3df3d4f8a185e894a5aeb68a8ec08c)

-   将 invalidate()函数添加到池连接。将从池中删除连接。仍然需要让引擎自动重新连接到一个陈旧的数据库。[¶](#change-9356a87824679508ce4c592e428336c0)

-   added distinct() function to column elements so you can do
    func.count(mycol.distinct())[¶](#change-fc80d40f50270b028517b3bba2199a42)

-   将“always\_refresh”标志添加到 Mapper 中，创建一个映射器，该映射器将始终刷新其从数据库中获取/选择的对象的属性，并覆盖所做的任何更改。[¶](#change-e5d60d8a3cf463409e92d11d1384f766)

0.1.4 [¶ T0\>](#change-0.1.4 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 3 月 13 日

-   create\_engine()现在使用泛化参数；主机/主机名，db / dbname
    /数据库，密码/密码等。为所有引擎连接。使得引擎 URI 更“普遍”[¶](#change-0ef266ab794fd1853decd9620edf8427)

-   使用标记“scalar =
    True”添加了对嵌入到列子句中的 SELECT 语句的支持[¶](#change-ec2dc23024bd40e1ace566b16a735d09)

-   another overhaul to EagerLoading when used in conjunction with
    mappers that inherit; improvements to eager loads figuring out their
    aliased queries correctly, also relations set up against a mapper
    with inherited mappers will create joins against the table that is
    specific to the mapper itself (i.e. and not any tables that are
    inherited/are further down the inheritance chain), this can be
    overridden by using custom primary/secondary
    joins.[¶](#change-7b51c32cece61a2a7d06a4c224da9443)

-   added J.Ellis patch to mapper.py so that selectone() throws an
    exception if query returns more than one object row, selectfirst()
    to not throw the exception.
    还添加了 selectfirst\_by（与 get\_by 同义）和 selectone\_by
    [¶](#change-8fc4b9aa1cf9744a7669d0be1df63c87)

-   将 onupdate 参数添加到 Column 中，将在更新语句中执行 SQL /
    python.Also 将“for\_update =
    True”添加到所有 DefaultGenerator 子类[¶](#change-6ef2eeb2099404f773c18996c5252732)

-   增加了对 Andrija
    Zaric 贡献的 Oracle 表反射的支持；仍然存在一些关于复合主键/字典选择[¶](#change-0f736b992aafe1dc76f1529c795c4289)的错误

-   在初始的 Firebird 模块中检查，等待测试。[¶](#change-db02019010d352feae175b0ddc9ece30)

-   添加了 sql.ClauseParameters 字典对象作为 compiled.get\_params()的结果，对绑定参数进行了后期处理，以便原始值更易于访问[¶](#change-7d2152ee7c8c6d195f7a1cf43dda5448)

-   索引，列默认值，连接池，引擎构建的更多文档[¶](#change-d46502682e7dca9e36bd65c316e79420)

-   overhaul to the construction of the types system.
    使用更简单的继承模式，以便任何泛型类型都可以很容易地进行子类化，而不需要 TypeDecorator。[¶](#change-885f2250c263e6d9bbd939e640ce6639)

-   将“convert\_unicode =
    False”参数添加到 SQLEngine 中，将导致所有 String 类型执行 unicode 编码/解码（使字符串像 Unicodes 一样）[¶](#change-b8964cd08bf4a630173df252e9bb1acd)

-   在引擎中添加了'encoding
    =“utf8”'参数。给定的编码将用于 Unicode 类型中的所有编码/解码调用以及 convert\_unicode
    = True 时的字符串。[¶](#change-6fd5c8f4796179aa0b657cc3c9a877f8)

-   改进了针对 UNION 映射的支持，增加了 polymorph.py 示例来说明针对 UNION 的多类映射[¶](#change-b7a870e7cbd43542f1e67acfcfd6e1bf)

-   修复 SQLite LIMIT /
    OFFSET 语法[¶](#change-9ed214af739377d4d1a07991af151ccb)

-   修复 Oracle LIMIT 语法[¶](#change-456f1a13c73c2c11c84433cb277ee4dc)

-   添加了 backref()函数，允许反向引用将关键字参数传递给 backref。[¶](#change-b8d7baa9db640a9923d3325eb440d135)

-   Sequences 和 ColumnDefault 对象可以执行 execute()/ scalar()standalone
    [¶](#change-7168d352c4956bf69f8626864e3193c5)

-   SQL functions (i.e. func.foo()) can do execute()/scalar()
    standalone[¶](#change-6b05633188ef87464a8ddb4d1273715f)

-   修复 SQL 函数，以便 ANSI 标准函数（即 current\_timestamp 等）不指定括号。所有其他功能都可以。[¶](#change-0f45a37a74b083bfff321b728c4d1bf5)

-   将 settattr\_clean 和 append\_clean 添加到了 SmartProperty 中，该属性在不触发“脏”事件或任何历史的情况下设置属性。用作：myclass.prop1.setattr\_clean（myobject，'hi'）[¶](#change-d00d8ba1f11adb154262526c7414e593)

-   改进了对映射器使用时对列默认值的支持；映射器将从语句的已执行绑定参数（预转换）中提取预先执行的默认值，以将其填充到已保存的对象的属性中；如果任何 PassiveDefaults 已经启动，将取而代之从数据库中获取行来填充对象。[¶](#change-30d3737ba988bebaa33f655c7900bb01)

-   将'get\_session()。invalidate（\*
    obj）'方法添加到对象库，实例将在下一次访问属性时自动刷新()。[](#change-917a341fe1d89d4b1fff4f7559a2a0f3)

-   包含“engine”关键字参数的 SQL
    func 调用的改进，以便它们可以是 execute()d 或 scalar()ed
    standalone，也可以将 func 访问器添加到 SQLEngine
    [¶](#change-ef790669fa10bf7baaa122ee21865a04)

-   修复了 MySQL4 自定义表引擎，即 TYPE 而不是 ENGINE
    [¶](#change-6516c2f2245e5e1b90117cd2b3a9a482)

-   略有增强的日志记录，包括时间戳记和可配置的格式化系统，以代替全面的日志记录系统[¶](#change-b6ed1a0198df68545ae484c874554bf5)

-   对 TG 组的 ActiveMapper 类的改进，包括多对多关系[¶](#change-5937e5795d6d62109125d68a9a2bca0d)

-   在 mysql
    [¶](#change-5d7bdbcddc8bf662974b56f494fe2cc8)中添加了 Double 和 TinyInt 支持

0.1.3 [¶ T0\>](#change-0.1.3 "Permalink to this headline")
----------------------------------------------------------

发布于：2006 年 3 月 2 日

-   完成“post\_update”功能后，将在插入之前和删除之后添加第二个更新语句，以便协调一个没有创建任何依赖关系的关系；在持续存在两个相互依赖的行时使用[¶](#change-1f5f4367f904484de584c3bb891e66da)

-   完成了 mapper.using（session）函数，本地化的 per-object 会话功能；对象可以作为本地用户定义的 Session
    [¶](#change-0e1e1316e6f3a827735afefe31aac485)来声明和操作

-   使用多个表修复 Oracle“row\_number
    over”子句[¶](#change-766fa5aa35e254d9b460f774da134307)

-   mapper.get() was not selecting multiple-keyed objects if the
    mapper’s table was a join, such as in an inheritance relationship,
    this is fixed.[¶](#change-5a1a16a4b71e3d136d92292a14c57cfd)

-   overhaul to sql/schema packages so that the sql package can run all
    on its own, producing selects, inserts, etc.
    没有任何引擎依赖。基于新的 TableClause /
    ColumnClause 词法对象构建。架构的表/列对象是它们的“物理”子类。简化了 schema
    /
    sql 关系，扩展（如 proxyengine），并大幅提高整体性能。删除困扰 0.1.1 的整个 getattr()行为。[¶](#change-0017cfe2ab4cc37d9c78c82014884f4c)

-   refactoring of how the mapper “synchronizes” data between two
    objects into a separate module, works better with properties
    attached to a mapper that has an additional inheritance relationship
    to one of the related tables, also the same methodology used to
    synchronize parent/child objects now used by mapper to synchronize
    between inherited and inheriting
    mappers.[¶](#change-77a4af6cff5ccb1dc76b81e3a2d1a1f8)

-   使 objectstore“检查非身份映射”更积极，将在对象属性被修改或删除对象时执行检查[¶](#change-25a1b5bf971aeb34c95a82f6515686a1)

-   Index object fully implemented, can be constructed standalone, or
    via “index” and “unique” arguments on
    Columns.[¶](#change-e0e0f804057928ca3c17339825043f53)

-   将“convert\_unicode”标志添加到 SQLEngine 中，将所有的 String /
    CHAR 类型视为 Unicode 类型，并在绑定参数和结果集侧进行 raw-byte /
    utf-8 转换。[T1\>](#change-52570199946b60064a46eee53050539a)

-   postgres 维护一个 ANSI 函数列表，它必须没有圆括号，因此没有参数的函数调用一致地工作[¶](#change-2ca432b76e40ac51ae3326a7cecaaa68)

-   表格可以在没有指定引擎的情况下创建。这会将其引擎默认为一个模块范围的“默认引擎”，它是一个 ProxyEngine。这个引擎可以通过函数“global\_connect”来连接。[¶](#change-02f8ebdd1e633c6e8c28681a25a6f754)

-   将“refresh（\* obj）”方法无条件地添加到 objectstore /
    Session 以重新加载任何对象集合的属性[¶](#change-7aeabde948e2c369ea04d69e2d02699e)

0.1.2 [¶ T0\>](#change-0.1.2 "Permalink to this headline")
----------------------------------------------------------

发布：2006 年 2 月 24 日星期五

-   修复了架构中的递归调用，该架构以某种方式运行了 994 次，然后正常返回。什么都不打破，放慢了一切。感谢 jpellerin 找到它。[¶](#change-de1fc1982f3062522c70b3e35238622d)

0.1.1 [¶ T0\>](#change-0.1.1 "Permalink to this headline")
----------------------------------------------------------

发布日期：2006 年 2 月 23 日

-   对 Function 类进行小修改，以便具有 func.foo()的表达式使用 Function 对象的类型（即左侧）作为布尔表达式的类型，而不是另一侧移动目标（变更集 1020）。[¶](#change-e16c39be323fea2f73db352513a5940b)

-   用 backrefs 创建自引用映射器稍微简单一些（但仍然不那么容易 -
    更改集 1019）[¶](#change-e70d118b07b49de55d82c23d91e9081b)

-   修复了一对一映射（变更集 1015）[¶](#change-5eb55c9b7fb9b46fe9743042c5c197b8)

-   psycopg1 无固定日期/时间问题（变更集 1005）[¶](#change-9d8b445291ec495ae301791eabf26ce9)

-   与 postgres 相关的两个问题，因为不赞成使用 oid，所以不想给你“lastrowid”：

    > -   即使这不是 PassiveDefault 的想法，预先明确执行的主键 col
    >     *do*上的 postgres 数据库端默认值。这是因为列上的序列被反映为 PassiveDefaults，但需要在主键列上显式执行，因此我们知道我们刚插入的内容。
    > -   如果你确实添加了一行有一堆数据库端默认值的行，并且 PassiveDefault 事情是以旧的方式工作的，也就是说他们只是在数据库端执行，那么“无法获取没有 OID 的行”异常发生也不会发生，除非有人（通常是 ORM）明确要求它。

    [¶](#change-e8ec3a2e0e2f56f6655ddcd4de136d35)

-   使用 engine.execute\_compiled 修复了一个小故障，它正在创建第二个 ResultProxy，它被扔掉了。[¶](#change-2c3fc20743a99145b4a0ecf183bce3b5)

-   开始在对象属性中实现更新的逻辑。您现在可以说 myclass.attr.property，它将为您提供与该属性相对应的 PropertyLoader，即 myclass.mapper.props
    ['attr'] [¶](#change-c4c2e167af71097505892fe6c0f9ea0c)

-   急切的加载已经在内部进行彻底检查，以便随时使用别名。现在可以创建更复杂的急切加载链，而不需要明确的“使用别名”类型指令。EagerLoader 代码现在也更加简单。[¶](#change-8b0556e1a808353012875095c53a252b)

-   一个新的有点实验性的标志“use\_update”添加到关系中，表明这个关系应该由第二个 UPDATE 语句处理，无论是在主 INSERT 之后还是在主 DELETE 之前。处理循环行依赖关系。[¶](#change-bb14c5b9872156d48ab505a3a77430f8)

-   添加了异常模块，所有引发的异常（除了一些 KeyError /
    AttributeError 异常）都从这些类下降。[¶](#change-45952d04eaa88500b66049d3f8dc7db2)

-   使用 MySQL 修复日期类型，返回 timedelta 转换为 datetime.time
    [¶](#change-a5536a9bfa01004daf66ff7818a21370)

-   两阶段 objectstore.commit 操作（即 begin /
    commit）现在返回一个事务对象（SessionTrans），以更清楚地指示事务边界。[](#change-3bf53f3d367aba55d5ec4bc69c85692b)

-   具有添加到模式[¶](#change-b54bcb6dbe46538531b8e1d16ddb6123)的创建/删除支持的索引对象

-   修复 postgres，根据正在进行的“我们无法从 postgres 获取插入的行”问题，它会在表中明确预先执行 PassiveDefault（如果它是主键列）问题[¶
    T1\>](#change-3d429f8d0ca014abee1ff15fb990d3ef)

-   更改为获取 postgres 表 defs 的 information\_schema 查询，现在使用显式 JOIN 关键字，因为一个用户使用 8.1
    [¶](#change-b4f51eecebde449095403049763c55a9)

-   修复 engine.process\_defaults，使其可以正确使用具有不同列名/列键的表（changset
    982）[¶](#change-48ba3c876c69946297ad8dd5406e9240)

-   一个列只能附加到一个表中 -
    现在已声明[¶](#change-6a46cd8778aaefd256df83b635921814)

-   postgres 时间类型从时间类型[¶](#change-8d68036be554ddac542f03734315f82f)下降

-   修复所有测试，以便运行类型测试（现在命名为 testtypes）[¶](#change-8eeb4551410be5ee01d94698e94ca5c5)

-   修复 Join 对象，以便正确地导出其外键（cs
    973）[¶](#change-8e34508d624949e6fd5f920ae0e68a91)

-   使用继承固定的映射器创建关系（cs
    973）[¶](#change-fd3d78d00d70c3e12464e5610e3dcb63)


