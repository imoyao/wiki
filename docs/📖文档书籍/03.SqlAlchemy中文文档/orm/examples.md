---
title: examples
date: 2021-02-20 22:41:40
permalink: /sqlalchemy/orm/examples/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
ORM 示例[¶](#orm-examples "Permalink to this headline")
======================================================

SQLAlchemy 发行版包含各种代码示例，说明一组选择的模式，一些是典型的，一些不太典型。所有都可以运行，可以在发行版的`/examples`目录中找到。所有的描述和源代码可以在这里找到。

额外的 SQLAlchemy 示例（某些用户贡献）可在维基上的[http://www.sqlalchemy.org/trac/wiki/UsageRecipes](http://www.sqlalchemy.org/trac/wiki/UsageRecipes)上获得。

映射食谱[¶](#mapping-recipes "Permalink to this headline")
----------------------------------------------------------

### 邻接列表[¶](#module-examples.adjacency_list "Permalink to this headline")

使用邻接列表模型映射的字典词典结构示例。

例如。：

    node = TreeNode('rootnode')
    node.append('node1')
    node.append('node3')
    session.add(node)
    session.commit()

    dump_tree(node)

文件清单：

-   [adjacency\_list.py
    T0\>](_modules/examples/adjacency_list/adjacency_list.html)

### 协会[¶ T0\>](#module-examples.association "Permalink to this headline")

说明“关联对象”模式的用法的示例，其中中间类调解以多对多模式关联的两个类之间的关系。

文件清单：

-   [proxied\_association.py](_modules/examples/association/proxied_association.html)
    -
    与 basic\_association 相同的示例，在使用[`sqlalchemy.ext.associationproxy`](extensions_associationproxy.html#module-sqlalchemy.ext.associationproxy "sqlalchemy.ext.associationproxy")时添加以明确引用`OrderItem`可选。
-   [basic\_association.py](_modules/examples/association/basic_association.html)
    -
    说明“订单”和“商品”对象集合之间的多对多关系，通过名为“OrderItem”的关联对象将购买价格与每个对象关联起来
-   [dict\_of\_sets\_with\_default.py](_modules/examples/association/dict_of_sets_with_default.html)
    -
    一个高级关联代理示例，它演示了关联代理的嵌套以生成多级 Python 集合，在这种情况下，这是一个包含字符串键和整数集作为值的字典，它隐藏了映射的底层类。

### 有向图[¶](#module-examples.graphs "Permalink to this headline")

有向图结构的持久性示例。该图存储为一组边，每个节都引用一个“下”节点和一个“上”节点。对低层和高层邻居的基本持久性和查询进行了说明：

    n2 = Node(2)
    n5 = Node(5)
    n2.add_neighbor(n5)
    print n2.higher_neighbors()

文件清单：

-   [directed\_graph.py](_modules/examples/graphs/directed_graph.html) -
    有向图示例。

### 作为词典的动态关系[¶](#module-examples.dynamic_dict "Permalink to this headline")

说明如何在“动态”关系之上放置类似字典的外观，以便字典操作（假设简单的字符串键）可以对大集合进行操作，而无需一次加载完整集合。

文件清单：

-   [dynamic\_dict.py
    T0\>](_modules/examples/dynamic_dict/dynamic_dict.html)

### 通用关联[¶](#module-examples.generic_associations "Permalink to this headline")

举例说明将多种父母与特定子对象相关联的各种方法。

这些示例都使用声明性扩展和声明性混合。Each one presents the identical
use case at the end - two classes, `Customer` and
`Supplier`, both subclassing the
`HasAddresses` mixin, which ensures that the parent
class is provided with an `addresses` collection
which contains `Address` objects.

该[discriminator\_on\_association.py
T0\>和](_modules/examples/generic_associations/discriminator_on_association.html)[generic\_fk.py
T1\>脚本现代化在 2007 年的博客文章](_modules/examples/generic_associations/generic_fk.html)[多态关联与 SQLAlchemy 的
T2\>提交食谱版本。](http://techspot.zzzeek.org/2007/05/29/polymorphic-associations-with-sqlalchemy/)

文件清单：

-   [generic\_fk.py](_modules/examples/generic_associations/generic_fk.html)
    -
    以类似于 Django，ROR 等流行框架的方式说明所谓的“通用外键”。这种方法绕过了标准的参照完整性实践，因为“外键”列实际上并没有限制引用任何特定的表；相反，应用程序内部逻辑用于确定引用哪个表。
-   [table\_per\_association.py](_modules/examples/generic_associations/table_per_association.html)
    -
    说明一个混合，它通过为每个父类分别生成的关联表提供一个通用关联。关联的对象本身被保存在所有父母共享的单个表中。
-   [discriminator\_on\_association.py](_modules/examples/generic_associations/discriminator_on_association.html)
    - Illustrates a mixin which provides a generic association using a
    single target table and a single association table, referred to by
    all parent tables.
    关联表包含一个“鉴别器”列，用于确定与关联表中每个特定行关联的父对象的类型。
-   [table\_per\_related.py](_modules/examples/generic_associations/table_per_related.html)
    -
    说明了一个通用关联，它在每个表内保存关联对象，每个关联对象都会生成以代表特定父类持久化这些对象。

### 大集合[¶](#module-examples.large_collection "Permalink to this headline")

大集合的例子。

说明当相关对象列表非常大时，与[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")一起使用的选项，其中包括：

-   “动态”关系查询访问数据切片
-   如何将 ON DELETE CASCADE 与`passive_deletes=True`结合使用，以大大提高相关集合删除的性能。

文件清单：

-   [large\_collection.py
    T0\>](_modules/examples/large_collection/large_collection.html)

### 物化路径[¶](#module-examples.materialized_paths "Permalink to this headline")

使用 SQLAlchemy ORM 演示分层数据的“物化路径”模式。

文件清单：

-   [materialized\_pa​​ths.py](_modules/examples/materialized_paths/materialized_paths.html)
    - 说明了“物化路径”模式。

### 嵌套集[¶](#module-examples.nested_sets "Permalink to this headline")

说明使用 SQLAlchemy ORM 实现分层数据的“嵌套集”模式的基本方法。

文件清单：

-   [nested\_sets.py](_modules/examples/nested_sets/nested_sets.html) -
    Celko 的“嵌套集”树结构。

### 性能[¶ T0\>](#module-examples.performance "Permalink to this headline")

性能分析套件，适用于各种 SQLAlchemy 用例。

每个套件都专注于具有特定性能配置文件和相关含义的特定用例：

-   批量插入
-   个人插入，有或没有交易
-   获取大量的行
-   运行很多简短的查询

所有套件都包含了说明 Core 和 ORM 使用的各种使用模式，并且通常按照性能从最差到最大的顺序进行排序，与 SQLAlchemy 提供的功能数量相反，最大最小（这两种情况通常完全一致）。

在包级别提供了一个命令行工具，可以运行各个套件：

    $ python -m examples.performance --helpplain
    usage: python -m examples.performance [-h] [--test TEST] [--dburl DBURL]
                                          [--num NUM] [--profile] [--dump]
                                          [--runsnake] [--echo]

                                          {bulk_inserts,large_resultsets,single_inserts}

    positional arguments:
      {bulk_inserts,large_resultsets,single_inserts}
                            suite to run

    optional arguments:
      -h, --help            show this help message and exit
      --test TEST           run specific test name
      --dburl DBURL         database URL, default sqlite:///profile.db
      --num NUM             Number of iterations/items/etc for tests; default is 0
                            module-specific
      --profile             run profiling and dump call counts
      --dump                dump full call profile (implies --profile)
      --runsnake            invoke runsnakerun (implies --profile)
      --echo                Echo SQL output

示例运行如下所示：

    $ python -m examples.performance bulk_insertsplain

或者选择：

    $ python -m examples.performance bulk_inserts \plain
        --dburl mysql+mysqldb://scott:tiger@localhost/test \
        --profile --num 1000

也可以看看

[How can I profile a SQLAlchemy powered
application?](faq_performance.html#faq-how-to-profile)

#### 档案清单[¶](#file-listing "Permalink to this headline")

文件清单：

-   [single\_inserts.py](_modules/examples/performance/single_inserts.html)
    -
    在这一系列测试中，我们正在研究一种在独立事务中插入一行的方法，然后返回到基本上“关闭”状态。这将类似于启动数据库连接，插入行，提交和关闭的 API 调用。
-   [short\_selects.py](_modules/examples/performance/short_selects.html)
    - 这一系列测试说明了通过主键选择单个记录的不同方式
-   [bulk\_updates.py](_modules/examples/performance/bulk_updates.html)
    - 这一系列测试说明了批量更新大量行的不同方法。
-   [bulk\_inserts.py](_modules/examples/performance/bulk_inserts.html)
    - 这一系列测试说明了批量插入大量行的不同方法。
-   [large\_resultsets.py](_modules/examples/performance/large_resultsets.html)
    - 在这一系列测试中，我们正在考虑加载大量非常小且简单的行。
-   [\_\_ main \_\_。py](_modules/examples/performance/__main__.html) -
    允许将示例/性能包作为脚本运行。

#### 用时间运行所有测试[¶](#running-all-tests-with-time "Permalink to this headline")

这是运行的默认形式：

    $ python -m examples.performance single_inserts
    Tests to run: test_orm_commit, test_bulk_save,
                  test_bulk_insert_dictionaries, test_core,
                  test_core_query_caching, test_dbapi_raw_w_connect,
                  test_dbapi_raw_w_pool

    test_orm_commit : Individual INSERT/COMMIT pairs via the
        ORM (10000 iterations); total time 13.690218 sec
    test_bulk_save : Individual INSERT/COMMIT pairs using
        the "bulk" API  (10000 iterations); total time 11.290371 sec
    test_bulk_insert_dictionaries : Individual INSERT/COMMIT pairs using
        the "bulk" API with dictionaries (10000 iterations);
        total time 10.814626 sec
    test_core : Individual INSERT/COMMIT pairs using Core.
        (10000 iterations); total time 9.665620 sec
    test_core_query_caching : Individual INSERT/COMMIT pairs using Core
        with query caching (10000 iterations); total time 9.209010 sec
    test_dbapi_raw_w_connect : Individual INSERT/COMMIT pairs w/ DBAPI +
        connection each time (10000 iterations); total time 9.551103 sec
    test_dbapi_raw_w_pool : Individual INSERT/COMMIT pairs w/ DBAPI +
        connection pool (10000 iterations); total time 8.001813 sec

#### 为单个测试转储配置文件[¶](#dumping-profiles-for-individual-tests "Permalink to this headline")

Python 配置文件输出可以转储所有测试，或更常见的单个测试：

    $ python -m examples.performance single_inserts --test test_core --num 1000 --dumpplain
    Tests to run: test_core
    test_core : Individual INSERT/COMMIT pairs using Core. (1000 iterations); total fn calls 186109
             186109 function calls (186102 primitive calls) in 1.089 seconds

       Ordered by: internal time, call count

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1000    0.634    0.001    0.634    0.001 {method 'commit' of 'sqlite3.Connection' objects}
         1000    0.154    0.000    0.154    0.000 {method 'execute' of 'sqlite3.Cursor' objects}
         1000    0.021    0.000    0.074    0.000 /Users/classic/dev/sqlalchemy/orm/lib/sqlalchemy/orm/sql/compiler.py:1950(_get_colparams)
         1000    0.015    0.000    0.034    0.000 /Users/classic/dev/sqlalchemy/orm/lib/sqlalchemy/orm/engine/default.py:503(_init_compiled)
            1    0.012    0.012    1.091    1.091 examples/performance/single_inserts.py:79(test_core)

        ...

#### 使用 RunSnake [¶](#using-runsnake "Permalink to this headline")

该选项需要安装[RunSnake](https://pypi.python.org/pypi/RunSnakeRun)命令行工具：

    $ python -m examples.performance single_inserts --test test_core --num 1000 --runsnake

将显示图形 RunSnake 输出。

#### 编写自己的套房[¶](#writing-your-own-suites "Permalink to this headline")

profiler 套件系统是可扩展的，可以应用于您自己的一套测试。这是一个有价值的技术，用于决定一些性能关键的例程的正确方法。例如，如果我们想分析几种加载之间的差异，我们可以创建一个文件`test_loads.py`，其中包含以下内容：

    from examples.performance import Profiler
    from sqlalchemy import Integer, Column, create_engine, ForeignKey
    from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()
    engine = None
    session = None


    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        children = relationship("Child")


    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))


    # Init with name of file, default number of items
    Profiler.init("test_loads", 1000)


    @Profiler.setup_once
    def setup_once(dburl, echo, num):
        "setup once.  create an engine, insert fixture data"
        global engine
        engine = create_engine(dburl, echo=echo)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        sess = Session(engine)
        sess.add_all([
            Parent(children=[Child() for j in range(100)])
            for i in range(num)
        ])
        sess.commit()


    @Profiler.setup
    def setup(dburl, echo, num):
        "setup per test.  create a new Session."
        global session
        session = Session(engine)
        # pre-connect so this part isn't profiled (if we choose)
        session.connection()


    @Profiler.profile
    def test_lazyload(n):
        "load everything, no eager loading."

        for parent in session.query(Parent):
            parent.children


    @Profiler.profile
    def test_joinedload(n):
        "load everything, joined eager loading."

        for parent in session.query(Parent).options(joinedload("children")):
            parent.children


    @Profiler.profile
    def test_subqueryload(n):
        "load everything, subquery eager loading."

        for parent in session.query(Parent).options(subqueryload("children")):
            parent.children

    if __name__ == '__main__':
        Profiler.main()

我们可以直接运行我们的新脚本：

    $ python test_loads.py  --dburl postgresql+psycopg2://scott:tiger@localhost/testplain
    Running setup once...
    Tests to run: test_lazyload, test_joinedload, test_subqueryload
    test_lazyload : load everything, no eager loading. (1000 iterations); total time 11.971159 sec
    test_joinedload : load everything, joined eager loading. (1000 iterations); total time 2.754592 sec
    test_subqueryload : load everything, subquery eager loading. (1000 iterations); total time 2.977696 sec

以及 RunSnake 输出的个人测试：

    $ python test_loads.py  --num 100 --runsnake --test test_joinedloadplain

### 关系连接条件[¶](#module-examples.join_conditions "Permalink to this headline")

各种[`orm.relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")配置的示例，它们利用`primaryjoin`参数来组合特殊类型的连接条件。

文件清单：

-   [cast.py](_modules/examples/join_conditions/cast.html) -
    说明连接两列的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，其中这些列的类型不同，并且必须在 SQL 端使用 CAST 以便匹配他们。
-   [threeway.py](_modules/examples/join_conditions/threeway.html) -
    Illustrate a “three way join” - where a primary table joins to a
    remote table via an association table, but then the primary table
    also needs to refer to some columns in the remote table directly.

### XML 持久[¶](#module-examples.elementtree "Permalink to this headline")

举例说明了在关系数据库中用 ElementTree 表示的持久化和查询 XML 文档的三种策略。这些技术不直接对 ElementTree 对象应用任何映射，因此与本地 cElementTree 以及 lxml 兼容，并且可以适应任何类型的 DOM 表示系统。也显示了沿类似 xpath 的字符串查询。

例如。：

    # parse an XML file and persist in the database
    doc = ElementTree.parse("test.xml")
    session.add(Document(file, doc))
    session.commit()

    # locate documents with a certain path/attribute structure
    for document in find_document('/somefile/header/field2[@attr=foo]'):
        # dump the XML
        print document

文件清单：

-   [pickle.py](_modules/examples/elementtree/pickle.html) - illustrates
    a quick and dirty way to persist an XML document expressed using
    ElementTree and pickle.
-   [adjacency\_list.py](_modules/examples/elementtree/adjacency_list.html)
    - 说明了使用 ElementTree 保存表示的 XML 文档的明确方式。
-   [optimized\_al.py](_modules/examples/elementtree/optimized_al.html)
    - 使用与`adjacency_list.py`相同的策略，但将每个 DOM 行与其拥有的文档行相关联，以便可以使用 DOM 节点的完整文档加载 O（1）查询
    - 构建“层次结构”是在非递归方式加载之后执行的，并且效率更高。

### 版本控制对象[¶](#versioning-objects "Permalink to this headline")

#### 使用历史记录表进行版本控制[¶](#module-examples.versioned_history "Permalink to this headline")

说明为实体创建版本表的扩展，并为每个更改存储记录。给定的扩展生成一个匿名的“历史”类，它表示目标对象的历史版本。

用法可以通过单元测试模块`test_versioning.py`来说明，它可以通过鼻子运行：

    cd examples/versioning
    nosetests -v

示例用法的片段，使用声明式：

    from history_meta import Versioned, versioned_sessionplain

    Base = declarative_base()

    class SomeClass(Versioned, Base):
        __tablename__ = 'sometable'

        id = Column(Integer, primary_key=True)
        name = Column(String(50))

        def __eq__(self, other):
            assert type(other) is SomeClass and other.id == self.id

    Session = sessionmaker(bind=engine)
    versioned_session(Session)

    sess = Session()
    sc = SomeClass(name='sc1')
    sess.add(sc)
    sess.commit()

    sc.name = 'sc1modified'
    sess.commit()

    assert sc.version == 2

    SomeClassHistory = SomeClass.__history_mapper__.class_

    assert sess.query(SomeClassHistory).\
                filter(SomeClassHistory.version == 1).\
                all() \
                == [SomeClassHistory(version=1, name='sc1')]

`Versioned`
mixin 设计用于声明式。要使用经典映射器的扩展，可以应用`_history_mapper`函数：

    from history_meta import _history_mapper

    m = mapper(SomeClass, sometable)
    _history_mapper(m)

    SomeHistoryClass = SomeClass.__history_mapper__.class_

文件清单：

-   [history\_meta.py](_modules/examples/versioned_history/history_meta.html)
    - 版本化的 mixin 类和其他实用程序。
-   [test\_versioning.py](_modules/examples/versioned_history/test_versioning.html)
    - 说明使用`history_meta.py`模块函数的单元测试。

#### 使用时间行的版本控制[¶](#module-examples.versioned_rows "Permalink to this headline")

说明通过为每个更改存储新行来对数据进行版本升级的扩展；也就是说，通常 UPDATE 变成 INSERT。

文件清单：

-   [versioned\_rows.py](_modules/examples/versioned_rows/versioned_rows.html)
    -
    说明拦截对象更改的方法，将单个行上的 UPDATE 语句转换为 INSERT 语句，以便使用新数据插入新行，使旧行保持不变。
-   [versioned\_map.py](_modules/examples/versioned_rows/versioned_map.html)
    -
    versioned\_rows 示例的变体。在这里，我们存储一个键/值对的字典，以“垂直”方式存储 k
    / v，每个键获得一行。该值被分成两个独立的数据类型，字符串和整数 -
    数据类型存储的范围可以根据个人需求进行调整。

### 垂直属性映射[¶](#module-examples.vertical "Permalink to this headline")

说明“垂直表”映射。

“垂直表”是指将对象的各个属性作为不同的行存储在表中的技术。“垂直表”技术用于持久化可能具有各种属性的对象，代价是简单的查询控制和简洁。它通常存在于内容/文档管理系统中，以便灵活地表示用户创建的结构。

给出了两种不同的方法。在第二行中，每行都引用一个“数据类型”，其中包含有关存储在属性中的信息类型的信息，例如整数，字符串或日期。

例：

    shrew = Animal(u'shrew')
    shrew[u'cuteness'] = 5
    shrew[u'weasel-like'] = False
    shrew[u'poisonous'] = True

    session.add(shrew)
    session.flush()

    q = (session.query(Animal).
         filter(Animal.facts.any(
           and_(AnimalFact.key == u'weasel-like',
                AnimalFact.value == True))))
    print 'weasel-like animals', q.all()

文件清单：

-   [dictlike.py](_modules/examples/vertical/dictlike.html) -
    将垂直表映射为字典。
-   [dictlike-polymorphic.py](_modules/examples/vertical/dictlike-polymorphic.html)
    - 将多态值垂直表映射为字典。

继承映射食谱[¶](#inheritance-mapping-recipes "Permalink to this headline")
--------------------------------------------------------------------------

### 基本继承映射[¶](#module-examples.inheritance "Permalink to this headline")

如 datamapping\_inheritance 中所述的单表，连接表和混凝土表继承的工作示例。

文件清单：

-   [concrete.py](_modules/examples/inheritance/concrete.html) -
    Concrete（table-per-class）继承的例子。
-   [single.py](_modules/examples/inheritance/single.html) -
    单表继承示例。
-   [joined.py](_modules/examples/inheritance/joined.html) -
    联合表（继承的子类）继承示例。

特殊的 API [¶](#special-apis "Permalink to this headline")
---------------------------------------------------------

### 属性工具[¶](#module-examples.custom_attributes "Permalink to this headline")

举例说明对 SQLAlchemy 属性管理系统的修改。

文件清单：

-   [custom\_management.py](_modules/examples/custom_attributes/custom_management.html)
    - 使用[`sqlalchemy.ext.instrumentation`](extensions_instrumentation.html#module-sqlalchemy.ext.instrumentation "sqlalchemy.ext.instrumentation")扩展包说明定制的类工具。
-   [listen\_for\_events.py](_modules/examples/custom_attributes/listen_for_events.html)
    - 说明如何将事件附加到所有已检测的属性并侦听更改事件。
-   [active\_column\_defaults.py](_modules/examples/custom_attributes/active_column_defaults.html)
    - 说明如何使用[`AttributeEvents.init_scalar()`](events.html#sqlalchemy.orm.events.AttributeEvents.init_scalar "sqlalchemy.orm.events.AttributeEvents.init_scalar")事件与 Core 列默认值一起提供 ORM 对象，该对象在未设置时自动生成默认值属性被访问。

### 水平分片[¶](#module-examples.sharding "Permalink to this headline")

使用 SQLAlchemy Sharding
API 的基本示例。分片是指跨多个数据库水平缩放数据。

“分片”映射的基本组件是：

-   多个数据库，每个数据库分配一个'分片 ID'
-   给定要保存的实例的函数，它可以返回单个分片 ID；这被称为“shard\_chooser”
-   一个可以返回适用于特定实例标识符的分片 ID 列表的函数；这被称为“id\_chooser”。如果它返回所有分片 ID，则将搜索所有分片。
-   给定一个特定的查询（“query\_chooser”），该函数可以返回一个分片 ID 列表来尝试。如果它返回所有分片 ID，则将查询所有分片并将结果连接在一起。

在这个例子中，四个 sqlite 数据库将以每个数据库为基础存储关于天气数据的信息。我们提供了示例 shard\_chooser，id\_chooser 和 query\_chooser 函数。query\_chooser 说明了对 SQL 表达式元素的检查，以试图确定被请求的单个分片。

通用分片例程的构建是在多个数据库之间组织实例的问题的一个雄心勃勃的方法。对于一个更为通俗易懂的替代方法，“独立实体”方法是一种以明确的方式将对象分配给不同表（以及潜在的数据库节点）的简单方法
-
在维基上的[EntityName](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/EntityName)中进行了描述。

文件清单：

-   [attribute\_shard.py
    T0\>](_modules/examples/sharding/attribute_shard.html)

扩展 ORM [¶](#extending-the-orm "Permalink to this headline")
------------------------------------------------------------

### Dogpile 缓存[¶](#module-examples.dogpile_caching "Permalink to this headline")

演示如何在[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象中嵌入[dogpile.cache](https://dogpilecache.readthedocs.io/)功能，以允许完全缓存控制以及从长期缓存中拉取“延迟加载”属性的功能。

在版本 0.8 中更改：该示例已更新为使用 dogpile.cache，将 Beaker 替换为正在使用的缓存库。

在这个演示中，说明了以下技术：

-   使用[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")的自定义子类
-   避免查询从自定义缓存源而不是数据库中抽取的基本技术。
-   使用 dogpile.cache 进行基本缓存，使用允许全局控制一组固定配置的“区域”。
-   使用自定义的`MapperOption`对象来配置查询上的选项，包括在发生延迟加载时调用对象图中深层选项的功能。

例如。：

    # query for Person objects, specifying cacheplain
    q = Session.query(Person).options(FromCache("default"))

    # specify that each Person's "addresses" collection comes from
    # cache too
    q = q.options(RelationshipCache(Person.addresses, "default"))

    # query
    print q.all()

要运行，必须安装 SQLAlchemy 和 dogpile.cache，或者在当前的 PYTHONPATH 上运行。演示会为数据文件创建本地目录，插入初始数据并运行。第二次运行该演示将利用已经存在的缓存文件，并且恰好一个针对两个表的 SQL 语句将被发出
- 然而，显示的结果将利用从缓存中拉出的数十个 lazyload。

演示脚本自身，按照复杂性顺序，以 Python 模块的形式运行，以便相对导入工作：

    python -m examples.dogpile_caching.helloworldplain

    python -m examples.dogpile_caching.relationship_caching

    python -m examples.dogpile_caching.advanced

    python -m examples.dogpile_caching.local_session_caching

文件清单：

-   [environment.py](_modules/examples/dogpile_caching/environment.html)
    - 根据需要建立数据/缓存文件路径和配置，引导夹具数据。
-   [caching\_query.py](_modules/examples/dogpile_caching/caching_query.html)
    -
    表示允许在 SQLAlchemy 中使用 Dogpile 缓存的函数和类。引入一个名为 FromCache 的查询选项。
-   [model.py](_modules/examples/dogpile_caching/model.html) -
    数据模型，表示具有多个 Address 对象的 Person，每个对象都有 PostalCode，City，Country。
-   [fixture\_data.py](_modules/examples/dogpile_caching/fixture_data.html)
    -
    安装一些示例数据。在这里，我们有几个美国/加拿大城市的邮政编码。然后，安装 100 个人记录，每个记录都随机选择一个邮政编码。
-   [helloworld.py](_modules/examples/dogpile_caching/helloworld.html) -
    说明如何加载一些数据并缓存结果。
-   [relationship\_caching.py](_modules/examples/dogpile_caching/relationship_caching.html)
    - 说明如何在关系端点上添加缓存选项，以便延迟缓存从缓存中加载。
-   [advanced.py](_modules/examples/dogpile_caching/advanced.html) -
    说明结合使用 FromCache 选项的 Query，包括前端加载，缓存失效和集合缓存。
-   [local\_session\_caching.py](_modules/examples/dogpile_caching/local_session_caching.html)
    -
    到目前为止的一切？本示例创建一个新的 dogpile.cache 后端，该后端将数据保存在当前会话本地的字典中。删除()会话并且缓存消失。

### PostGIS 集成[¶](#module-examples.postgis "Permalink to this headline")

演示帮助嵌入 PostGIS 功能的技巧的天真示例。

这个例子最初是为了将其推广到一个全面的 PostGIS 集成层而开发的。我们很高兴地宣布，这已经成为[GeoAlchemy](http://www.geoalchemy.org/)。

该例子说明：

-   一个允许 CREATE / DROP 与 AddGeometryColumn /
    DropGeometryColumn 一起使用的 DDL 扩展
-   几何类型以及一些子类型，它们将结果行值转换为支持 GIS 的对象，并且还与 DDL 扩展集成。
-   一个支持 GIS 的对象，它存储一个原始几何值并为诸如 AsText()等函数提供一个工厂。
-   一个 ORM 比较器，它可以覆盖映射对象上的标准列方法以生成 GIS 操作员。
-   一个属性事件侦听器，拦截字符串并转换为 GeomFromText()。
-   一个独立的操作员示例。

该实施仅限于公开的，众所周知且易于使用的扩展点。

例如。：

    print session.query(Road).filter(Road.road_geom.intersects(r1.road_geom)).all()plain

文件清单：

-   [postgis.py T0\>](_modules/examples/postgis/postgis.html)

