---
title: migration_10
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/63d953/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
SQLAlchemy 1.0有哪些新特性？[¶](#what-s-new-in-sqlalchemy-1-0 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍了 2014 年 5 月发布的 SQLAlchemy
0.9 版本，以及 2015 年 4 月发布的 SQLAlchemy 1.0 版本之间的变化。

文件最后更新日期：2015 年 6 月 9 日

引言[¶ T0\>](#introduction "Permalink to this headline")
--------------------------------------------------------

本指南介绍了 SQLAlchemy
1.0 版中的新功能，并介绍了影响用户将其应用程序从 0.9 系列 SQLAlchemy 迁移到 1.0 的更改。

请仔细阅读关于行为变化的章节，以了解行为中潜在的向后不兼容的变化。

新功能和改进 - ORM [¶](#new-features-and-improvements-orm "Permalink to this headline")
---------------------------------------------------------------------------------------

### 新会话批量INSERT / UPDATE API [¶](#new-session-bulk-insert-update-api "Permalink to this headline")

已经创建了一系列新的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")方法，它们将工作单元直接提供给工作单位以发出 INSERT 和 UPDATE 语句。如果使用正确，这个面向专家的系统可以允许 ORM 映射用于生成批量插入和更新语句，批量插入到 executemany 组中，从而允许语句以与直接使用 Core 相媲美的速度进行。

也可以看看

[Bulk Operations](orm_persistence_techniques.html#bulk-operations) -
introduction and full documentation

[＃3100 T0\>](http://www.sqlalchemy.org/trac/ticket/3100)

### 新的性能示例套件[¶](#new-performance-example-suite "Permalink to this headline")

受到针对[Bulk
Operations](orm_persistence_techniques.html#bulk-operations)功能以及[How
can I profile a SQLAlchemy powered
application?](faq_performance.html#faq-how-to-profile)常见问题解答部分，增加了一个新的示例部分，其中有几个脚本，旨在说明各种核心和 ORM 技术的相对性能概况。这些脚本被组织到用例中，并被封装在一个单一的控制台界面下，从而可以运行演示的任意组合，抛出时间，Python 配置文件结果和/或 RunSnake 配置文件显示。

也可以看看

[Performance](orm_examples.html#examples-performance)

### “烘焙”查询[¶](#baked-queries "Permalink to this headline")

“烘焙”查询功能是一种不寻常的新方法，它允许直接构建使用缓存来调用[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，后续调用功能大大减少了Python函数调用开销（超过75％）。通过将一个[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象指定为一系列仅调用一次的lambda表达式，作为预编译单元的查询开始变得可行：

    from sqlalchemy.ext import baked
    from sqlalchemy import bindparam

    bakery = baked.bakery()

    def search_for_user(session, username, email=None):

        baked_query = bakery(lambda session: session.query(User))
        baked_query += lambda q: q.filter(User.name == bindparam('username'))

        baked_query += lambda q: q.order_by(User.id)

        if email:
            baked_query += lambda q: q.filter(User.email == bindparam('email'))

        result = baked_query(session).params(username=username, email=email).all()

        return result

也可以看看

[Baked Queries](orm_extensions_baked.html)

[＃3054 T0\>](http://www.sqlalchemy.org/trac/ticket/3054)

### 声明性混合，`@declared_attr`和相关特性的改进[¶](#improvements-to-declarative-mixins-declared-attr-and-related-features "Permalink to this headline")

与[`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")结合的声明性系统已经过大修，以支持新功能。

用[`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")装饰的函数现在只在之后被调用**所有基于混色的列副本生成。**这意味着该函数可以调用混入建立的列，并且会接收到正确的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的引用：

    class HasFooBar(object):
        foobar = Column(Integer)

        @declared_attr
        def foobar_prop(cls):
            return column_property('foobar: ' + cls.foobar)

    class SomeClass(HasFooBar, Base):
        __tablename__ = 'some_table'
        id = Column(Integer, primary_key=True)

Above, `SomeClass.foobar_prop` will be invoked
against `SomeClass`, and
`SomeClass.foobar` will be the final [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
object that is to be mapped to `SomeClass`, as
opposed to the non-copied object present directly on
`HasFooBar`, even though the columns aren’t mapped
yet.

The [`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")
function now **memoizes** the value that’s returned on a per-class
basis, so that repeated calls to the same attribute will return the same
value. 我们可以改变这个例子来说明这一点：

    class HasFooBar(object):plain
        @declared_attr
        def foobar(cls):
            return Column(Integer)

        @declared_attr
        def foobar_prop(cls):
            return column_property('foobar: ' + cls.foobar)

    class SomeClass(HasFooBar, Base):
        __tablename__ = 'some_table'
        id = Column(Integer, primary_key=True)

以前，`SomeClass`将通过调用`foobar`映射到`foobar`列的一个特定副本，但是`foobar_prop`第二次会产生不同的列。在声明性设置时间内，`SomeClass.foobar`的值现在被记忆，所以即使在映射器映射该属性之前，无论[`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")被调用。

上面的两种行为应该对许多类型的映射器属性的声明性定义有很大的帮助，这些属性派生自其他属性，其中[`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")函数从本地存在的其他[`declared_attr`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")函数该类实际上是映射的。

对于希望构建一个为每个子类创建不同列的声明性混合的漂亮边缘情况，将添加新的修饰符[`declared_attr.cascading`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr.cascading "sqlalchemy.ext.declarative.declared_attr.cascading")。使用此修饰符，将为映射的继承层次结构中的每个类单独调用修饰的函数。虽然这已经是针对特殊属性（如`__table_args__`和`__mapper_args__`）的行为，但对于列和其他属性，缺省行为假定该属性仅附加到基类，并且只是从子类继承而来。通过[`declared_attr.cascading`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.declared_attr.cascading "sqlalchemy.ext.declarative.declared_attr.cascading")，可以应用单个行为：

    class HasSomeAttribute(object):
        @declared_attr.cascading
        def some_id(cls):
            if has_inherited_table(cls):
                return Column(ForeignKey('myclass.id'), primary_key=True)
            else:
                return Column(Integer, primary_key=True)

            return Column('id', Integer, primary_key=True)

    class MyClass(HasSomeAttribute, Base):
        ""
        # ...

    class MySubClass(MyClass):
        ""
        # ...

也可以看看

[Mixing in Columns in Inheritance
Scenarios](orm_extensions_declarative_mixins.html#mixin-inheritance-columns)

最后，[`AbstractConcreteBase`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")类已被重写，以便可以在抽象基础上内联设置关系或其他映射器属性：

    from sqlalchemy import Column, Integer, ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import (declarative_base, declared_attr,
        AbstractConcreteBase)

    Base = declarative_base()

    class Something(Base):
        __tablename__ = u'something'
        id = Column(Integer, primary_key=True)


    class Abstract(AbstractConcreteBase, Base):
        id = Column(Integer, primary_key=True)

        @declared_attr
        def something_id(cls):
            return Column(ForeignKey(Something.id))

        @declared_attr
        def something(cls):
            return relationship(Something)


    class Concrete(Abstract):
        __tablename__ = u'cca'
        __mapper_args__ = {'polymorphic_identity': 'cca', 'concrete': True}

The above mapping will set up a table `cca` with
both an `id` and a `something_id` column, and `Concrete` will also have a
relationship `something`.
新功能是`Abstract`也将具有一个独立配置的关系`something`，该关系针对基础的多态联合进行构建。

[＃3150](http://www.sqlalchemy.org/trac/ticket/3150)
[＃2670](http://www.sqlalchemy.org/trac/ticket/2670)
[＃3149](http://www.sqlalchemy.org/trac/ticket/3149)
[＃2952](http://www.sqlalchemy.org/trac/ticket/2952)
[＃3050](http://www.sqlalchemy.org/trac/ticket/3050)

### ORM全部对象的读取速度提高了25％[¶](#orm-full-object-fetches-25-faster "Permalink to this headline")

`loading.py`模块的机制以及标识映射经过了内联，重构和修剪的几个过程，因此现在的行加载大约比基于OR​​M的对象快大约25％
。假设有一个1M行表，类似下面的脚本说明了最受改善的负载类型：

    import time
    from sqlalchemy import Integer, Column, create_engine, Table
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Foo(Base):
        __table__ = Table(
            'foo', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('a', Integer(), nullable=False),
            Column('b', Integer(), nullable=False),
            Column('c', Integer(), nullable=False),
        )

    engine = create_engine(
        'mysql+mysqldb://scott:tiger@localhost/test', echo=True)

    sess = Session(engine)

    now = time.time()

    # avoid using all() so that we don't have the overhead of building
    # a large list of full objects in memory
    for obj in sess.query(Foo).yield_per(100).limit(1000000):
        pass

    print("Total time: %d" % (time.time() - now))

本地 MacBookPro 的结果从 0.9 秒的 19 秒降至 1.0 的 14 秒。在批量处理大量行时，[`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")调用总是一个好主意，因为它可以防止Python解释器不得不一次为所有对象及其工具分配大量内存。如果没有[`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")，MacBookPro 上面的脚本在 0.9 上是 31 秒，在 1.0 上是 26 秒，因此需要花费额外的时间来设置非常大的内存缓冲区。

### New KeyedTuple实现显着加快[¶](#new-keyedtuple-implementation-dramatically-faster "Permalink to this headline")

我们看了一下[`KeyedTuple`](orm_query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")实现，希望改进像这样的查询：

    rows = sess.query(Foo.a, Foo.b, Foo.c).all()plain

使用[`KeyedTuple`](orm_query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")类而不是Python的`collections.namedtuple()`，因为后者有一个非常复杂的类型创建例程，其基准测试比[`KeyedTuple`](orm_query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")但是，当获取成千上万行时，`collections.namedtuple()`快速超过[`KeyedTuple`](orm_query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")，随着实例调用的增加，它变得非常慢。该怎么办？两种方法之间进行对冲的新类型。基于哪种情况，新的“轻量级键控元组”要么针对“大小”（返回的行数）和“num”（针对不同查询的数量），要么优于两者，要么滞后于较快的对象。在“甜蜜点”中，我们既创建了大量新类型，又获取了很多行，轻量级对象完全吸引了名为 tuple 和 KeyedTuple：

    -----------------
    size=10 num=10000                 # few rows, lots of queries
    namedtuple: 3.60302400589         # namedtuple falls over
    keyedtuple: 0.255059957504        # KeyedTuple very fast
    lw keyed tuple: 0.582715034485    # lw keyed trails right on KeyedTuple
    -----------------
    size=100 num=1000                 # <--- sweet spot
    namedtuple: 0.365247011185
    keyedtuple: 0.24896979332
    lw keyed tuple: 0.0889317989349   # lw keyed blows both away!
    -----------------
    size=10000 num=100
    namedtuple: 0.572599887848
    keyedtuple: 2.54251694679
    lw keyed tuple: 0.613876104355
    -----------------
    size=1000000 num=10               # few queries, lots of rows
    namedtuple: 5.79669594765         # namedtuple very fast
    keyedtuple: 28.856498003          # KeyedTuple falls over
    lw keyed tuple: 6.74346804619     # lw keyed trails right on namedtuple

[＃3176 T0\>](http://www.sqlalchemy.org/trac/ticket/3176)

### 结构性内存使用的重大改进[¶](#significant-improvements-in-structural-memory-use "Permalink to this headline")

通过对许多内部对象使用`__slots__`，结构性内存的使用得到了改进。此优化特别适用于具有大量表和列的大型应用程序的基本内存大小，并可减少各种高容量对象（包括事件监听内部件，比较对象以及ORM属性和加载器策略系统的某些部分）的内存大小。

利用 heapy 测量 Nova 的启动大小的一个工作台说明了在基本导入“nova.db.”的过程中，SQLAlchemy 的对象，相关字典以及弱引用占用了大约 3.7 个 megs 或 46％的差异，即 46％。
sqlalchemy.models”：

    # reported by heapy, summation of SQLAlchemy objects +plain
    # associated dicts + weakref-related objects with core of Nova imported:

        Before: total count 26477 total bytes 7975712
        After: total count 18181 total bytes 4236456

    # reported for the Python module space overall with the
    # core of Nova imported:

        Before: Partition of a set of 355558 objects. Total size = 61661760 bytes.
        After: Partition of a set of 346034 objects. Total size = 57808016 bytes.

### UPDATE 语句现在在 flush [¶](#update-statements-are-now-batched-with-executemany-in-a-flush "Permalink to this headline")中与executemany()一起进行批处理

UPDATE 语句现在可以在一个 ORM
flush 内批处理为更高性能的 executemany()调用，类似于 INSERT 语句可以批处理的方式；这将在基于以下标准的 flush 内被调用：

-   按顺序的两个或多个 UPDATE 语句涉及要修改的相同的一组列。
-   该语句在SET子句中没有嵌入式SQL表达式。
-   映射不使用[`version_id_col`](orm_mapping_api.html#sqlalchemy.orm.mapper.params.version_id_col "sqlalchemy.orm.mapper")，或者后端dialect支持executemany()操作的“理智”行计数；大多数DBAPI现在都能正确支持这一点。

### Session.get\_bind()处理更广泛的继承场景[¶](#session-get-bind-handles-a-wider-variety-of-inheritance-scenarios "Permalink to this headline")

只要查询或工作单元清理过程试图找到与特定类相对应的数据库引擎，就会调用[`Session.get_bind()`](orm_session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")方法。该方法已得到改进，可处理各种面向继承的场景，其中包括：

-   绑定到Mixin或抽象类：

        class MyClass(SomeMixin, Base):
            __tablename__ = 'my_table'
            # ...

        session = Session(binds={SomeMixin: some_engine})

-   基于表单独绑定到继承的具体子类：

        class BaseClass(Base):
            __tablename__ = 'base'

            # ...

        class ConcreteSubClass(BaseClass):
            __tablename__ = 'concrete'

            # ...

            __mapper_args__ = {'concrete': True}


        session = Session(binds={plain
            base_table: some_engine,
            concrete_table: some_other_engine
        })

[＃3035 T0\>](http://www.sqlalchemy.org/trac/ticket/3035)

### Session.get\_bind()将在所有相关的查询案例中接收映射器[¶](#session-get-bind-will-receive-the-mapper-in-all-relevant-query-cases "Permalink to this headline")

A series of issues were repaired where the [`Session.get_bind()`](orm_session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")
would not receive the primary [`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
of the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query"),
even though this mapper was readily available (the primary mapper is the
single mapper, or alternatively the first mapper, that is associated
with a [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
object).

The [`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
object, when passed to [`Session.get_bind()`](orm_session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind"),
is typically used by sessions that make use of the
[`Session.binds`](orm_session_api.html#sqlalchemy.orm.session.Session.params.binds "sqlalchemy.orm.session.Session")
parameter to associate mappers with a series of engines (although in
this use case, things frequently “worked” in most cases anyway as the
bind would be located via the mapped table object), or more specifically
implement a user-defined [`Session.get_bind()`](orm_session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")
method that provies some pattern of selecting engines based on mappers,
such as horizontal sharding or a so-called “routing” session that routes
queries to different backends.

这些情景包括：

-   [`Query.count()`](orm_query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")

        session.query(User).count()

-   [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")和[`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")，用于UPDATE
    / DELETE语句以及“fetch”策略使用的SELECT：

        session.query(User).filter(User.id == 15).update(
                {"name": "foob"}, synchronize_session='fetch')

        session.query(User).filter(User.id == 15).delete(
                synchronize_session='fetch')

-   针对单个列的查询：

        session.query(User.id, User.name).all()

-   SQL函数和其他针对间接映射的表达式，如[`column_property`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")：

        class User(Base):plain
            # ...

            score = column_property(func.coalesce(self.tables.users.c.name, None)))

        session.query(func.max(User.score)).scalar()

[＃3227](http://www.sqlalchemy.org/trac/ticket/3227)
[＃3242](http://www.sqlalchemy.org/trac/ticket/3242)
[＃1326](http://www.sqlalchemy.org/trac/ticket/1326)

### .info 字典改进[¶](#info-dictionary-improvements "Permalink to this headline")

`InspectionAttr.info`集合现在可用于从[`Mapper.all_orm_descriptors`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")集合中检索的每种对象。这包括[`hybrid_property`](orm_extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")和[`association_proxy()`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")。但是，由于这些对象是类绑定描述符，因此必须从它们所连接的类中分别访问**，以便获取该属性。**下面是使用[`Mapper.all_orm_descriptors`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")名称空间的示例：

    class SomeObject(Base):
        # ...

        @hybrid_property
        def some_prop(self):
            return self.value + 5


    inspect(SomeObject).all_orm_descriptors.some_prop.info['foo'] = 'bar'

它也可作为所有[`SchemaItem`](core_metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")对象（例如[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")，[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")等）的构造函数参数使用。以及其余的 ORM 结构，如[`orm.synonym()`](orm_mapped_attributes.html#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")。

[＃2971 T0\>](http://www.sqlalchemy.org/trac/ticket/2971)

[＃2963 T0\>](http://www.sqlalchemy.org/trac/ticket/2963)

### 使用别名order\_by [¶](#columnproperty-constructs-work-a-lot-better-with-aliases-order-by "Permalink to this headline")，ColumnProperty 构造可以更好地工作

有关[`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")的各种问题已得到修复，特别是针对[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")构造以及0.9中引入的“按标号排序”逻辑请参阅[Label
constructs can now render as their name alone in an ORDER
BY](migration_09.html#migration-1068)中单独呈现其名称）。

给定如下映射：

    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)

    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))


    A.b = column_property(
            select([func.max(B.id)]).where(B.a_id == A.id).correlate(A)
        )

包含“A.b”两次的简单场景将无法正确呈现：

    print(sess.query(A, a1).order_by(a1.b))

这将按错误的列排序：

    SELECT a.id AS a_id, (SELECT max(b.id) AS max_1 FROM b
    WHERE b.a_id = a.id) AS anon_1, a_1.id AS a_1_id,
    (SELECT max(b.id) AS max_2
    FROM b WHERE b.a_id = a_1.id) AS anon_2
    FROM a, a AS a_1 ORDER BY anon_1

新产出：

    SELECT a.id AS a_id, (SELECT max(b.id) AS max_1
    FROM b WHERE b.a_id = a.id) AS anon_1, a_1.id AS a_1_id,
    (SELECT max(b.id) AS max_2
    FROM b WHERE b.a_id = a_1.id) AS anon_2
    FROM a, a AS a_1 ORDER BY anon_2

也有许多情况下，“按顺序排列”逻辑将无法按标签排序，例如，如果映射是“多态”：

    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        type = Column(String)

        __mapper_args__ = {'polymorphic_on': type, 'with_polymorphic': '*'}

order\_by将无法使用标签，因为它会因多态加载而被匿名化：

    SELECT a.id AS a_id, a.type AS a_type, (SELECT max(b.id) AS max_1
    FROM b WHERE b.a_id = a.id) AS anon_1
    FROM a ORDER BY (SELECT max(b.id) AS max_2
    FROM b WHERE b.a_id = a.id)

现在标签的顺序跟踪匿名标签，现在可以使用：

    SELECT a.id AS a_id, a.type AS a_type, (SELECT max(b.id) AS max_1
    FROM b WHERE b.a_id = a.id) AS anon_1
    FROM a ORDER BY anon_1

这些修复包括各种可能破坏`aliased()`结构状态的heisenbugs，这样标签逻辑将再次失败；这些也已被修复。

[＃3148](http://www.sqlalchemy.org/trac/ticket/3148)
[＃3188](http://www.sqlalchemy.org/trac/ticket/3188)

新功能和改进 - 核心[¶](#new-features-and-improvements-core "Permalink to this headline")
----------------------------------------------------------------------------------------

### 选择/查询 LIMIT / OFFSET 可以被指定为任意的 SQL 表达式[¶](#select-query-limit-offset-may-be-specified-as-an-arbitrary-sql-expression "Permalink to this headline")

除了整数值之外，[`Select.limit()`](core_selectable.html#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")和[`Select.offset()`](core_selectable.html#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")方法现在接受任何SQL表达式作为参数。ORM
[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象也会将任何表达式传递给底层的[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象。通常，这用于允许传递一个绑定参数，以后可以用一个值替换它：

    sel = select([table]).limit(bindparam('mylimit')).offset(bindparam('myoffset'))

不支持非整数LIMIT或OFFSET表达式的方言可能会继续不支持此行为；第三方方言也可能需要修改才能利用新的行为。当前使用`._limit`或`._offset`属性的方言将继续适用于极限/偏移被指定为简单整数值的情况。但是，当指定SQL表达式时，这两个属性将在访问时引发[`CompileError`](core_exceptions.html#sqlalchemy.exc.CompileError "sqlalchemy.exc.CompileError")。希望支持新功能的第三方方言现在应该调用`._limit_clause`和`._offset_clause`属性来接收完整的 SQL 表达式，而不是整数值。

### `ForeignKeyConstraint`上的`use_alter`标志（通常）不再需要[¶](#the-use-alter-flag-on-foreignkeyconstraint-is-usually-no-longer-needed "Permalink to this headline")

The [`MetaData.create_all()`](core_metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
and [`MetaData.drop_all()`](core_metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")
methods will now make use of a system that automatically renders an
ALTER statement for foreign key constraints that are involved in
mutually-dependent cycles between tables, without the need to specify
[`ForeignKeyConstraint.use_alter`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint").
此外，外键约束不再需要有一个名称才能通过 ALTER 创建；只有 DROP 操作需要名称。在 DROP 的情况下，该功能将确保只有具有明确名称的约束实际上包含在 ALTER 语句中。如果 DROP 无法解决，则系统现在发出一个简洁明了的错误信息，如果 DROP 无法继续进行。

[`ForeignKeyConstraint.use_alter`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")和[`ForeignKey.use_alter`](core_constraints.html#sqlalchemy.schema.ForeignKey.params.use_alter "sqlalchemy.schema.ForeignKey")标志保持不变，并且在CREATE
/ DROP场景中继续具有建立那些需要ALTER的约束的效果。

从版本 1.0.1 开始，如果 SQLite 不支持 ALTER，那么在 DROP 期间，给定的表有一个无法解析的周期；在这种情况下会发出警告，并且按照**no**顺序删除这些表，除非启用约束，否则这通常在 SQLite 上可以正常工作。要解决警告并继续至少对 SQLite 数据库进行部分排序，特别是在启用了约束的情况下，将“use\_alter”标志重新应用于这些[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")和[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")应该明确地从这种排序中删除的对象。

也可以看看

[Creating/Dropping Foreign Key Constraints via
ALTER](core_constraints.html#use-alter) - 新行为的完整描述。

[＃3282 T0\>](http://www.sqlalchemy.org/trac/ticket/3282)

### ResultProxy“自动关闭”现在是一个“软”关闭[¶](#resultproxy-auto-close-is-now-a-soft-close "Permalink to this headline")

对于许多发行版本，[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")对象总是在所有结果行被提取的地方自动关闭。这是为了允许使用该对象而不需要明确地调用[`ResultProxy.close()`](core_connections.html#sqlalchemy.engine.ResultProxy.close "sqlalchemy.engine.ResultProxy.close")；由于所有 DBAPI 资源都已被释放，因此该对象可以放弃。但是，该对象保持严格的“关闭”行为，这意味着后续对[`ResultProxy.fetchone()`](core_connections.html#sqlalchemy.engine.ResultProxy.fetchone "sqlalchemy.engine.ResultProxy.fetchone")，[`ResultProxy.fetchmany()`](core_connections.html#sqlalchemy.engine.ResultProxy.fetchmany "sqlalchemy.engine.ResultProxy.fetchmany")或[`ResultProxy.fetchall()`](core_connections.html#sqlalchemy.engine.ResultProxy.fetchall "sqlalchemy.engine.ResultProxy.fetchall")现在会引发一个[`ResourceClosedError`](core_exceptions.html#sqlalchemy.exc.ResourceClosedError "sqlalchemy.exc.ResourceClosedError")：

    >>> result = connection.execute(stmt)
    >>> result.fetchone()
    (1, 'x')
    >>> result.fetchone()
    None  # indicates no more rows
    >>> result.fetchone()
    exception: ResourceClosedError

这种行为与 pep-249 的状态不一致，即在结果耗尽后，您可以重复调用 fetch 方法。它还会干扰结果代理的某些实现的行为，例如 cx\_oracle方言对某些数据类型使用的`BufferedColumnResultProxy`。

To solve this, the “closed” state of the [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
has been broken into two states; a “soft close” which does the majority
of what “close” does, in that it releases the DBAPI cursor and in the
case of a “close with result” object will also release the connection,
and a “closed” state which is everything included by “soft close” as
well as establishing the fetch methods as “closed”.
[`ResultProxy.close()`](core_connections.html#sqlalchemy.engine.ResultProxy.close "sqlalchemy.engine.ResultProxy.close")方法现在从不隐式调用，只有[`ResultProxy._soft_close()`](core_connections.html#sqlalchemy.engine.ResultProxy._soft_close "sqlalchemy.engine.ResultProxy._soft_close")方法非公开：

    >>> result = connection.execute(stmt)
    >>> result.fetchone()
    (1, 'x')
    >>> result.fetchone()
    None  # indicates no more rows
    >>> result.fetchone()
    None  # still None
    >>> result.fetchall()
    []
    >>> result.close()
    >>> result.fetchone()
    exception: ResourceClosedError  # *now* it raises

[＃3330](http://www.sqlalchemy.org/trac/ticket/3330)
[＃3329](http://www.sqlalchemy.org/trac/ticket/3329)

### CHECK Constraints现在支持命名约定中的`%(column_0_name)s`标记[¶](#check-constraints-now-support-the-column-0-name-s-token-in-naming-conventions "Permalink to this headline")

`%(column_0_name)s`将从在[`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")的表达式中找到的第一列派生：

    metadata = MetaData(
        naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"}
    )

    foo = Table('foo', metadata,
        Column('value', Integer),
    )

    CheckConstraint(foo.c.value > 5)

将呈现：

    CREATE TABLE foo (plainplain
        value INTEGER,
        CONSTRAINT ck_foo_value CHECK (value > 5)
    )

命名约定与由[`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")（如[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")或[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")）生成的约束的组合现在也将使用所有 CHECK 约束约定。

也可以看看

[Naming CHECK
Constraints](core_constraints.html#naming-check-constraints)

[Configuring Naming for Boolean, Enum, and other schema
types](core_constraints.html#naming-schematypes)配置命名

[＃3299 T0\>](http://www.sqlalchemy.org/trac/ticket/3299)

### 引用未附加列的约束可以在连接其引用列时自动附加到表上[¶](#constraints-referring-to-unattached-columns-can-auto-attach-to-the-table-when-their-referred-columns-are-attached "Permalink to this headline")

由于至少有0.8版本，一个[`Constraint`](core_constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")有能力根据传递的表格附加列自动附加到[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")：

    from sqlalchemy import Table, Column, MetaData, Integer, UniqueConstraint

    m = MetaData()

    t = Table('t', m,
        Column('a', Integer),
        Column('b', Integer)
    )

    uq = UniqueConstraint(t.c.a, t.c.b)  # will auto-attach to Table

    assert uq in t.constraints

为了协助某些倾向于使用声明的情况，即使[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象尚未与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")关联，此相同的自动附件逻辑现在也可以运行；额外的事件被建立，当那些[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象关联时，[`Constraint`](core_constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")也被添加：

    from sqlalchemy import Table, Column, MetaData, Integer, UniqueConstraint

    m = MetaData()

    a = Column('a', Integer)
    b = Column('b', Integer)

    uq = UniqueConstraint(a, b)

    t = Table('t', m, a, b)

    assert uq in t.constraints  # constraint auto-attached

上述功能是版本1.0.0b3后期添加的。对于[＃3411](http://www.sqlalchemy.org/trac/ticket/3411)，版本 1.0.4 的修订确保了如果[`Constraint`](core_constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")引用[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的混合并且字符串列名称；因为我们还没有跟踪名称添加到[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的情况：

    from sqlalchemy import Table, Column, MetaData, Integer, UniqueConstraint

    m = MetaData()

    a = Column('a', Integer)
    b = Column('b', Integer)

    uq = UniqueConstraint(a, 'b')

    t = Table('t', m, a, b)

    # constraint *not* auto-attached, as we do not have tracking
    # to locate when a name 'b' becomes available on the table
    assert uq not in t.constraints

以上，列“a”到表“t”的附件事件将在附加列“b”之前触发（因为“a”在“b”之前的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造函数中声明），并且如果要尝试附件，约束将无法找到“b”。为了一致性，如果约束引用任何字符串名称，则会跳过自动附加列连接逻辑。

当[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")已经包含构造[`Constraint`](core_constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")时的所有目标[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象时，原始自动附加逻辑当然会保持原位：

    from sqlalchemy import Table, Column, MetaData, Integer, UniqueConstraintplain

    m = MetaData()

    a = Column('a', Integer)
    b = Column('b', Integer)


    t = Table('t', m, a, b)

    uq = UniqueConstraint(a, 'b')

    # constraint auto-attached normally as in older versions
    assert uq in t.constraints

[＃3341](http://www.sqlalchemy.org/trac/ticket/3341)
[＃3411](http://www.sqlalchemy.org/trac/ticket/3411)

### INSERT FROM SELECT 现在包含 Python 和 SQL 表达式默认值[¶](#insert-from-select-now-includes-python-and-sql-expression-defaults "Permalink to this headline")

[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
now includes Python and SQL-expression defaults if otherwise
unspecified; the limitation where non-server column defaults aren’t
included in an INSERT FROM SELECT is now lifted and these expressions
are rendered as constants into the SELECT statement:

    from sqlalchemy import Table, Column, MetaData, Integer, select, func

    m = MetaData()

    t = Table(
        't', m,
        Column('x', Integer),
        Column('y', Integer, default=func.somefunction()))

    stmt = select([t.c.x])
    print(t.insert().from_select(['x'], stmt))

将呈现：

    INSERT INTO t (x, y) SELECT t.x, somefunction() AS somefunction_1
    FROM t

该功能可以使用[`Insert.from_select.include_defaults`(core_dml.html#sqlalchemy.sql.expression.Insert.from_select.params.include_defaults "sqlalchemy.sql.expression.Insert.from_select")禁用。

### 列服务器默认值现在呈现文字值[¶](#column-server-defaults-now-render-literal-values "Permalink to this headline")

当由[`Column.server_default`](core_metadata.html#sqlalchemy.schema.Column.params.server_default "sqlalchemy.schema.Column")设置的[`DefaultClause`](core_defaults.html#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")作为要编译的 SQL 表达式存在时，“literal
bindings”编译器标志将打开。这允许嵌入在 SQL 中的文字正确呈现，例如：

    from sqlalchemy import Table, Column, MetaData, Textplain
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects.postgresql import ARRAY, array
    from sqlalchemy.dialects import postgresql

    metadata = MetaData()

    tbl = Table("derp", metadata,
        Column("arr", ARRAY(Text),
                    server_default=array(["foo", "bar", "baz"])),
    )

    print(CreateTable(tbl).compile(dialect=postgresql.dialect()))

现在呈现：

    CREATE TABLE derp (
        arr TEXT[] DEFAULT ARRAY['foo', 'bar', 'baz']
    )

在此之前，文字值`“foo”， “bar”， “baz”`这在DDL中是无用的。

[＃3087 T0\>](http://www.sqlalchemy.org/trac/ticket/3087)

### UniqueConstraint现在是表反射过程的一部分[¶](#uniqueconstraint-is-now-part-of-the-table-reflection-process "Permalink to this headline")

使用`autoload=True`填充的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象现在将包含[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")结构以及[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构。这个逻辑对于 Postgresql 和 Mysql 有一些注意事项：

#### 的PostgreSQL [¶ T0\>](#postgresql "Permalink to this headline")

Postgresql 具有这样的行为，当创建 UNIQUE 约束时，它隐式地创建与该约束相对应的 UNIQUE
INDEX。[`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")和[`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")方法将继续**这两个**清楚地返回这些条目，其中[`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")在索引条目中包含一个标记`duplicates_constraint`，用于指示检测到的相应约束。However, when performing full table
reflection using `Table(..., autoload=True)`, the
[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
construct is detected as being linked to the [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint"),
and is **not** present within the `Table.indexes` collection; only the [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
will be present in the `Table.constraints` collection. 重复数据删除逻辑通过在查询`pg_index`时加入到`pg_constraint`表来查看两个结构是否已链接。

#### MySQL 的[¶ T0\>](#mysql "Permalink to this headline")

MySQL 对于 UNIQUE
INDEX 和 UNIQUE 约束没有单独的概念。虽然它在创建表和索引时支持两种语法，但它们不会以任何不同的方式存储它们。The
[`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")
and the [`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")
methods will continue to **both** return an entry for a UNIQUE index in
MySQL, where [`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")
features a new token `duplicates_index` within the
constraint entry indicating that this is a dupe entry corresponding to
that index. However, when performing full table reflection using
`Table(..., autoload=True)`, the
[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
construct is **not** part of the fully reflected [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
construct under any circumstances; this construct is always represented
by a [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
with the `unique=True` setting present in the
`Table.indexes` collection.

也可以看看

[Postgresql Index
Reflection](dialects_postgresql.html#postgresql-index-reflection)

[MySQL Unique Constraints and
Reflection](dialects_mysql.html#mysql-unique-constraints)

[＃3184 T0\>](http://www.sqlalchemy.org/trac/ticket/3184)

### 新系统安全地发出参数化警告[¶](#new-systems-to-safely-emit-parameterized-warnings "Permalink to this headline")

很长一段时间，警告消息不能引用数据元素，这样一个特定的函数可能会发出无数个独特的警告。发生这种情况的关键在于`Unicode 类型 收到 tt> 非unicode / t5> 参数 值`警告。在这个消息中放置数据值将意味着该模块的Python
`__warningregistry__`，或者在某些情况下，Python全局`warnings.onceregistry`将变得无界限，如同大多数警告情况下，这两个集合中的一个会填充每条不同的警告消息。

The change here is that by using a special `string`
type that purposely changes how the string is hashed, we can control
that a large number of parameterized messages are hashed only on a small
set of possible hash values, such that a warning such as
`Unicode type received non-unicode bind param value`
can be tailored to be emitted only a specific number of times; beyond
that, the Python warnings registry will begin recording them as
duplicates.

为了说明，以下测试脚本将只显示 10 个参数集中的 10 个警告，总数为 1000：

    from sqlalchemy import create_engine, Unicode, select, cast
    import random
    import warnings

    e = create_engine("sqlite://")

    # Use the "once" filter (which is also the default for Python
    # warnings).  Exactly ten of these warnings will
    # be emitted; beyond that, the Python warnings registry will accumulate
    # new values as dupes of one of the ten existing.
    warnings.filterwarnings("once")

    for i in range(1000):
        e.execute(select([cast(
            ('foo_%d' % random.randint(0, 1000000)).encode('ascii'), Unicode)]))

这里的警告格式是：

    /path/lib/sqlalchemy/sql/sqltypes.py:186: SAWarning: Unicode type received
      non-unicode bind param value 'foo_4852'. (this warning may be
      suppressed after 10 occurrences)

[＃3178 T0\>](http://www.sqlalchemy.org/trac/ticket/3178)

关键行为改变 - ORM [¶](#key-behavioral-changes-orm "Permalink to this headline")
--------------------------------------------------------------------------------

### query.update()现在将字符串名称解析为映射的属性名称[¶](#query-update-now-resolves-string-names-into-mapped-attribute-names "Permalink to this headline")

[`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")的文档声明给定的`values`字典是“属性名称为键的字典”，暗示这些是映射的属性名称。不幸的是，该函数设计得更加注重接收属性和SQL表达式，而不是太多的字符串；当字符串被传递时，这些字符串将直接传递到核心更新语句而没有任何解决方案，就这些名称在映射类中的表示方式而言，这意味着名称必须完全与表列匹配，而不是如何该名称的属性被映射到类上。

字符串名称现在被认真解析为属性名称：

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column('user_name', String(50))

在上面，列`user_name`被映射为`name`。之前，调用传递字符串的[`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")将不得不按如下方式调用：

    session.query(User).update({'user_name': 'moonbeam'})

给定的字符串现在是针对实体解析的：

    session.query(User).update({'name': 'moonbeam'})plain

通常最好直接使用该属性，以避免任何含糊之处：

    session.query(User).update({User.name: 'moonbeam'})

该更改还表示同义词和混合属性也可以通过字符串名称引用：

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column('user_name', String(50))

        @hybrid_property
        def fullname(self):
            return self.name

    session.query(User).update({'fullname': 'moonbeam'})

[＃3228 T0\>](http://www.sqlalchemy.org/trac/ticket/3228)

### 将对象与无值与[¶](#warnings-emitted-when-comparing-objects-with-none-values-to-relationships "Permalink to this headline")关系进行比较时发出警告

这个变化在1.0.1中是新的。一些用户正在执行基本上是这种形式的查询：

    session.query(Address).filter(Address.user == User(id=None))plain

SQLAlchemy目前不支持此模式。对于所有版本，它发出的SQL类似于：

    SELECT address.id AS address_id, address.user_id AS address_user_id,
    address.email_address AS address_email_address
    FROM address WHERE ? = address.user_id
    (None,)

请注意，有一个比较`WHERE ？ = address.user_id`绑定值`?`在SQL中接收`None`或`NULL`。**这总是会在SQL中返回False**。这里的比较理论上会生成SQL，如下所示：

    SELECT address.id AS address_id, address.user_id AS address_user_id,
    address.email_address AS address_email_address
    FROM address WHERE address.user_id IS NULL

但现在，**它没有**。依靠“NULL =
NULL”在所有情况下都会产生 False 这一事实的应用程序有可能会冒着某种程度上的风险，SQLAlchemy 可能会解决此问题以生成“IS
NULL”，然后查询会产生不同的结果。因此，通过这种操作，您将看到一个警告：

    SAWarning: Got None for value of column user.id; this is unsupported
    for a relationship comparison and will not currently produce an
    IS comparison (but may in a future release)

请注意，这种模式在大多数情况下在 1.0.0 版本中被打破，包括所有的 beta；会产生像`SYMBOL('NEVER_SET')`这样的值。此问题已得到解决，但通过识别此模式，现在发出了警告，以便我们可以在将来的版本中更安全地修复此损坏的行为（现在在[＃3373](http://www.sqlalchemy.org/trac/ticket/3373)中捕获）。

[＃3371 T0\>](http://www.sqlalchemy.org/trac/ticket/3371)

### “否定包含或等于”关系比较将使用属性的当前值，而不是数据库值[¶](#a-negated-contains-or-equals-relationship-comparison-will-use-the-current-value-of-attributes-not-the-database-value "Permalink to this headline")

这个变化在 1.0.1 是新的；虽然我们希望这是 1.0.0，但它只是由于[＃3371](http://www.sqlalchemy.org/trac/ticket/3371)而变得明显。

给定映射：

    class A(Base):plain
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)

    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))
        a = relationship("A")

给定`A`，主键为 7，但我们更改为 10 而无需刷新：

    s = Session(autoflush=False)plain
    a1 = A(id=7)
    s.add(a1)
    s.commit()

    a1.id = 10

针对与此对象作为目标的多对一关系的查询将在绑定参数中使用值 10：

    s.query(B).filter(B.a == a1)

生产：

    SELECT b.id AS b_id, b.a_id AS b_a_idplainplain
    FROM b
    WHERE ? = b.a_id
    (10,)

However, before this change, the negation of this criteria would **not**
use 10, it would use 7, unless the object were flushed first:

    s.query(B).filter(B.a != a1)

产生（0.9 以及 1.0.1 之前的所有版本）：

    SELECT b.id AS b_id, b.a_id AS b_a_id
    FROM b
    WHERE b.a_id != ? OR b.a_id IS NULL
    (7,)

对于瞬态对象，它会产生一个破坏的查询：

    SELECT b.id, b.a_id
    FROM b
    WHERE b.a_id != :a_id_1 OR b.a_id IS NULL
    {u'a_id_1': symbol('NEVER_SET')}

这种不一致性已被修复，并且在所有查询中，现在将使用当前属性值，在本例中`10`。

[＃3374 T0\>](http://www.sqlalchemy.org/trac/ticket/3374)

### 属性事件和其他与没有预先存在的值的属性有关的操作的变化[¶](#changes-to-attribute-events-and-other-operations-regarding-attributes-that-have-no-pre-existing-value "Permalink to this headline")

在此更改中，访问对象时的默认返回值`None`现在在每次访问时动态返回，而不是在第一次访问时用特殊的“set”操作隐式设置该属性的状态。The
visible result of this change is that `obj.__dict__`
is not implicitly modified on get, and there are also some minor
behavioral changes for [`attributes.get_history()`](orm_session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")
and related functions.

给定一个没有状态的对象：

    >>> obj = Foo()

它总是SQLAlchemy的行为，如果我们访问一个从未设置过的标量属性或多对一属性，它将返回为`None`：

    >>> obj.someattr
    None

这个`None`的值实际上现在是`obj`状态的一部分，并且与我们已经明确设置了该属性的情况不同。
`obj.someattr = 无`。然而，这里的“set on
get”在历史和事件方面会有不同的表现。它不会发射任何属性事件，而且如果我们查看历史记录，我们可以看到：

    >>> inspect(obj).attrs.someattr.historyplain
    History(added=(), unchanged=[None], deleted=())   # 0.9 and below

也就是说，就好像该属性始终是`None`，并且从未更改过。这与我们先设置属性的情况明显不同：

    >>> obj = Foo()
    >>> obj.someattr = None
    >>> inspect(obj).attrs.someattr.history
    History(added=[None], unchanged=(), deleted=())  # all versions

以上意味着我们的“设置”操作的行为可能会被之前通过“get”访问的值所破坏。在 1.0 中，这种不一致性已经解决了，当使用默认的“getter”时，不再实际设置任何东西。

    >>> obj = Foo()
    >>> obj.someattr
    None
    >>> inspect(obj).attrs.someattr.history
    History(added=(), unchanged=(), deleted=())  # 1.0
    >>> obj.someattr = None
    >>> inspect(obj).attrs.someattr.history
    History(added=[None], unchanged=(), deleted=())

上述行为没有太大影响的原因是因为关系数据库中的 INSERT 语句在大多数情况下认为缺失值与 NULL 相同。SQLAlchemy 是否收到一个设置为 None 的特定属性的历史事件通常无关紧要；因为发送 None
/
NULL 与否之间的差异不会产生影响。然而，正如[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)（在[Priority
of attribute changes on relationship-bound attributes vs. FK-bound may
appear to
change](#migration-3060)）说明了一些很少的边缘情况实际上我们确实希望设置`None`。此外，在这里允许属性事件意味着现在可以为 ORM 映射属性创建“默认值”函数。

作为这种变化的一部分，隐含的“无”的生成现在在过去发生的其他情况下被禁用；这包括何时收到多对一的属性集操作；以前，如果没有设置其他值，“旧”值将为“无”；它现在将发送`orm.attributes.NEVER_SET`值，该值现在可以发送给属性侦听器。调用 Mapper 实用程序函数（如[`Mapper.primary_key_from_instance()`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.primary_key_from_instance "sqlalchemy.orm.mapper.Mapper.primary_key_from_instance")；）时也可能会收到此符号。如果主键属性根本没有设置，而之前的值为`None`，它现在将成为`orm.attributes.NEVER_SET`符号，并且不会更改对象的状态发生。

[＃3061 T0\>](http://www.sqlalchemy.org/trac/ticket/3061)

### 关系绑定属性与FK绑定属性变化的优先级可能会改变[¶](#priority-of-attribute-changes-on-relationship-bound-attributes-vs-fk-bound-may-appear-to-change "Permalink to this headline")

作为[＃3060](http://www.sqlalchemy.org/trac/ticket/3060)的一个副作用，将关系绑定属性设置为`None`现在是一个跟踪的历史事件，它涉及持续存在的意图`None`因为设置关系绑定属性的情况总是会直接分配给外键属性，所以在分配 None 时可以看到行为更改。给定映射：

    class A(Base):plain
        __tablename__ = 'table_a'

        id = Column(Integer, primary_key=True)

    class B(Base):
        __tablename__ = 'table_b'

        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('table_a.id'))
        a = relationship(A)

在 1.0 中，在所有情况下，关系绑定属性优先于 FK 绑定属性，无论我们分配的值是对`A`对象的引用还是`None`在 0.9 中，行为是不一致的，只有赋值时才会生效；不考虑：

    a1 = A(id=1)plain
    a2 = A(id=2)
    session.add_all([a1, a2])
    session.flush()

    b1 = B()
    b1.a = a1   # we expect a_id to be '1'; takes precedence in 0.9 and 1.0

    b2 = B()
    b2.a = None  # we expect a_id to be None; takes precedence only in 1.0

    b1.a_id = 2
    b2.a_id = 2

    session.add_all([b1, b2])
    session.commit()

    assert b1.a is a1  # passes in both 0.9 and 1.0
    assert b2.a is None  # passes in 1.0, in 0.9 it's a2

[＃3060 T0\>](http://www.sqlalchemy.org/trac/ticket/3060)

### session.expunge()将完全分离已被删除的对象[¶](#session-expunge-will-fully-detach-an-object-that-s-been-deleted "Permalink to this headline")

[`Session.expunge()`](orm_session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")的行为存在导致关于已删除对象的行为不一致的错误。在清除之后，[`object_session()`](orm_session_api.html#sqlalchemy.orm.session.object_session "sqlalchemy.orm.session.object_session")函数以及[`InstanceState.session`](orm_internals.html#sqlalchemy.orm.state.InstanceState.session "sqlalchemy.orm.state.InstanceState.session")属性仍然会将对象报告为属于[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

    u1 = sess.query(User).first()
    sess.delete(u1)

    sess.flush()

    assert u1 not in sess
    assert inspect(u1).session is sess  # this is normal before commit

    sess.expunge(u1)

    assert u1 not in sess
    assert inspect(u1).session is None  # would fail

Note that it is normal for `u1 not in sess` to be
True while `inspect(u1).session` still refers to the
session, while the transaction is ongoing subsequent to the delete
operation and [`Session.expunge()`](orm_session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")
has not been called; the full detachment normally completes once the
transaction is committed.
这个问题也会影响依赖于[`Session.expunge()`](orm_session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")的函数，比如[`make_transient()`](orm_session_api.html#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")。

[＃3139 T0\>](http://www.sqlalchemy.org/trac/ticket/3139)

### 通过yield\_per [¶](#joined-subquery-eager-loading-explicitly-disallowed-with-yield-per "Permalink to this headline")显式禁止加入/子查询加载加载

为了使[`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")方法更易于使用，当使用 yield\_per 时，如果任何子查询渴望加载器或加入的将使用集合的渴望加载器都要生效，因为它们目前与 yield-per 不兼容（然而，理论上子查询加载可能）。发生此错误时，可以使用星号发送[`lazyload()`](orm_loading_relationships.html#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")选项：

    q = sess.query(Object).options(lazyload('*')).yield_per(100)plain

或使用[`Query.enable_eagerloads()`](orm_query.html#sqlalchemy.orm.query.Query.enable_eagerloads "sqlalchemy.orm.query.Query.enable_eagerloads")：

    q = sess.query(Object).enable_eagerloads(False).yield_per(100)

[`lazyload()`](orm_loading_relationships.html#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")选项的优点是，仍然可以使用额外的多对一连接的加载器选项：

    q = sess.query(Object).options(
        lazyload('*'), joinedload("some_manytoone")).yield_per(100)

### 处理重复连接目标[¶](#changes-and-fixes-in-handling-of-duplicate-join-targets "Permalink to this headline")时的更改和修复

此处的更改包括在某些情况下发生意外和不一致行为时发生的错误，这些错误包括两次连接到实体或多个单表实体针对同一个表，而不使用基于关系的 ON 子句以及连接多次以相同的目标关系。

以映射开始：

    from sqlalchemy import Integer, Column, String, ForeignKey
    from sqlalchemy.orm import Session, relationship
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        bs = relationship("B")

    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))

连接到`A.bs`两次的查询：

    print(s.query(A).join(A.bs).join(A.bs))

将呈现：

    SELECT a.id AS a_id
    FROM a JOIN b ON a.id = b.a_id

该查询会重复删除多余的`A.bs`，因为它试图支持如下所示的情况：

    s.query(A).join(A.bs).\
        filter(B.foo == 'bar').\
        reset_joinpoint().join(A.bs, B.cs).filter(C.bar == 'bat')

That is, the `A.bs` is part of a “path”.
作为[＃3367](http://www.sqlalchemy.org/trac/ticket/3367)的一部分，两次到达相同的端点而不是大路径的一部分现在将发出警告：

    SAWarning: Pathed join target A.bs has already been joined to; skipping

当加入实体而不使用关系路径时，更大的变化涉及到。如果我们加入`B`两次：

    print(s.query(A).join(B, B.a_id == A.id).join(B, B.a_id == A.id))

在0.9中，这将呈现如下：

    SELECT a.id AS a_idplain
    FROM a JOIN b ON b.a_id = a.id JOIN b AS b_1 ON b_1.a_id = a.id

这是有问题的，因为别名是隐含的，并且在不同的ON子句的情况下会导致不可预知的结果。

在1.0中，没有应用自动别名，我们得到：

    SELECT a.id AS a_idplainplain
    FROM a JOIN b ON b.a_id = a.id JOIN b ON b.a_id = a.id

这会引发数据库错误。虽然如果我们加入冗余关系和基于冗余非关系的目标，如果“重复连接目标”的行为相同，那么现在我们只是在更严重的情况下改变行为，在这种情况下，先前会出现隐式锯齿，并且只会在关系案例中发出警告。最终，两次加入相同的事物而没有任何混淆消除歧义的行为会在所有情况下产生错误。

此更改还会影响单表继承目标。使用如下映射：

    from sqlalchemy import Integer, Column, String, ForeignKeyplain
    from sqlalchemy.orm import Session, relationship
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class A(Base):
        __tablename__ = "a"

        id = Column(Integer, primary_key=True)
        type = Column(String)

        __mapper_args__ = {'polymorphic_on': type, 'polymorphic_identity': 'a'}


    class ASub1(A):
        __mapper_args__ = {'polymorphic_identity': 'asub1'}


    class ASub2(A):
        __mapper_args__ = {'polymorphic_identity': 'asub2'}


    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)

        a_id = Column(Integer, ForeignKey("a.id"))

        a = relationship("A", primaryjoin="B.a_id == A.id", backref='b')

    s = Session()

    print(s.query(ASub1).join(B, ASub1.b).join(ASub2, B.a))

    print(s.query(ASub1).join(B, ASub1.b).join(ASub2, ASub2.id == B.a_id))

底部的两个查询是等价的，并且都应该呈现相同的SQL：

    SELECT a.id AS a_id, a.type AS a_type
    FROM a JOIN b ON b.a_id = a.id JOIN a ON b.a_id = a.id AND a.type IN (:type_1)
    WHERE a.type IN (:type_2)

上面的 SQL 是无效的，因为它在 FROM 列表中呈现两次“a”。但是，只有第二个查询会出现隐式别名错误，并将其渲染为：

    SELECT a.id AS a_id, a.type AS a_type
    FROM a JOIN b ON b.a_id = a.id JOIN a AS a_1
    ON a_1.id = b.a_id AND a_1.type IN (:type_1)
    WHERE a_1.type IN (:type_2)

在上面，第二次加入“a”是别名。虽然这看起来很方便，但它并不是单一继承查询的一般工作方式，而且具有误导性和不一致性。

最终结果是依赖于这个错误的应用程序现在会有数据库引发的错误。解决方案是使用预期的形式。在查询中引用单一继承实体的多个子类时，必须手动使用别名来消除表的歧义，因为所有子类通常引用同一个表：

    asub2_alias = aliased(ASub2)

    print(s.query(ASub1).join(B, ASub1.b).join(asub2_alias, B.a.of_type(asub2_alias)))

[＃3233](http://www.sqlalchemy.org/trac/ticket/3233)
[＃3367](http://www.sqlalchemy.org/trac/ticket/3367)

### 延迟列不再隐式不延迟[¶](#deferred-columns-no-longer-implicitly-undefer "Permalink to this headline")

标记为延迟但没有显式未延迟的映射属性现在将保持“延迟”状态，即使它们的列以某种方式存在于结果集中。这是一种性能增强，因为当获得结果集时，ORM加载不再花费时间搜索每个延迟列。但是，对于依赖于此的应用程序，现在应该使用明确的[`undefer()`](orm_loading_columns.html#sqlalchemy.orm.undefer "sqlalchemy.orm.undefer")或类似选项，以防止在访问属性时发出SELECT。

### 已弃用的 ORM 事件挂钩已删除[¶](#deprecated-orm-event-hooks-removed "Permalink to this headline")

以下 ORM 事件挂钩（其中一些已从 0.5 开始已弃用）已被删除：`translate_row`，`populate_instance`，`append_result`，`create_instance`这些钩子的用例起源于早期的 0.1 /
0.2 系列 SQLAlchemy，并且早已不必要了。特别是钩子在很大程度上无法使用，因为这些事件中的行为契约与周围的内部组件紧密相关，例如需要如何创建和初始化实例以及如何在 ORM 生成的行内定位列。删除这些钩子大大简化了 ORM 对象加载的机制。

### 使用自定义行加载程序时对新Bundle功能的API更改[¶](#api-change-for-new-bundle-feature-when-custom-row-loaders-are-used "Permalink to this headline")

当`create_row_processor()`方法在自定义类上被覆盖时，0.9的新[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")对象在 API 中有一个小的改变。以前，示例代码如下所示：

    from sqlalchemy.orm import Bundle

    class DictBundle(Bundle):
        def create_row_processor(self, query, procs, labels):
            """Override create_row_processor to return values as dictionaries"""
            def proc(row, result):
                return dict(
                            zip(labels, (proc(row, result) for proc in procs))
                        )
            return proc

未使用的`result`成员现在被删除：

    from sqlalchemy.orm import Bundleplain

    class DictBundle(Bundle):
        def create_row_processor(self, query, procs, labels):
            """Override create_row_processor to return values as dictionaries"""
            def proc(row):
                return dict(
                            zip(labels, (proc(row) for proc in procs))
                        )
            return proc

也可以看看

[Column Bundles](orm_loading_columns.html#bundles)

### 右内部连接嵌套现在是 innerjoin = True [¶](#right-inner-join-nesting-now-the-default-for-joinedload-with-innerjoin-true "Permalink to this headline")的已加入连接的默认值

[`joinedload.innerjoin`](orm_loading_relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")以及[`relationship.innerjoin`](orm_relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin "sqlalchemy.orm.relationship")的行为现在使用“嵌套”内部联接，即右嵌套，作为内部联接加入加入的急切加载被链接到外部加入急切加载。为了获得将外部连接存在时将所有连接的紧急加载链接为外部连接的旧行为，请使用`innerjoin="unnested"`。

As introduced in [Right-nested inner joins available in joined eager
loads](migration_09.html#feature-2976) from version 0.9, the behavior of
`innerjoin="nested"` is that an inner join eager
load chained to an outer join eager load will use a right-nested join.
`"nested"` is now implied when using
`innerjoin=True`:

    query(User).options(plain
        joinedload("orders", innerjoin=False).joinedload("items", innerjoin=True))

使用新的默认值，这将以下面的形式呈现 FROM 子句：

    FROM users LEFT OUTER JOIN (orders JOIN items ON <onclause>) ON <onclause>

也就是说，对INNER连接使用右嵌套连接，以便可以返回`users`的完整结果。INNER 连接的使用比使用 OUTER 连接更有效，并允许[`joinedload.innerjoin`](orm_loading_relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")优化参数在所有情况下都生效。

要获得较旧的行为，请使用`innerjoin="unnested"`：

    query(User).options(
        joinedload("orders", innerjoin=False).joinedload("items", innerjoin="unnested"))

这将避免右嵌套连接，并尽管使用 innerjoin 指令使用所有 OUTER 连接将连接链接在一起：

    FROM users LEFT OUTER JOIN orders ON <onclause> LEFT OUTER JOIN items ON <onclause>

正如 0.9 注释中指出的那样，右嵌套连接有困难的唯一数据库后端是 SQLite；从 0.9 版开始，SQLAlchemy 将右嵌套连接转换为子查询，作为 SQLite 上的连接目标。

也可以看看

[Right-nested inner joins available in joined eager
loads](migration_09.html#feature-2976) - 0.9.4 中介绍的特征描述。

[＃3008 T0\>](http://www.sqlalchemy.org/trac/ticket/3008)

### 子查询不再应用于使用list = False加入的预载[¶](#subqueries-no-longer-applied-to-uselist-false-joined-eager-loads "Permalink to this headline")

给定如下所示的加入的热切加载：

    class A(Base):plain
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        b = relationship("B", uselist=False)


    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))

    s = Session()
    print(s.query(A).options(joinedload(A.b)).limit(5))

SQLAlchemy considers the relationship `A.b` to be a
“one to many, loaded as a single value”, which is essentially a “one to
one” relationship.
但是，加入的预加载一直将上述情况视为主查询需要位于子查询中的情况，正如通常在主查询应用 LIMIT 时收集 B 对象所需的情况：

    SELECT anon_1.a_id AS anon_1_a_id, b_1.id AS b_1_id, b_1.a_id AS b_1_a_id
    FROM (SELECT a.id AS a_id
    FROM a LIMIT :param_1) AS anon_1
    LEFT OUTER JOIN b AS b_1 ON anon_1.a_id = b_1.a_id

然而，由于内部查询的到外层一个上的关系是至多只有一排在`uselist=False`

    SELECT a.id AS a_id, b_1.id AS b_1_id, b_1.a_id AS b_1_a_idplain
    FROM a LEFT OUTER JOIN b AS b_1 ON a.id = b_1.a_id
    LIMIT :param_1

在 LEFT OUTER
JOIN 返回多于一行的情况下，ORM 总是在这里发出警告并忽略`uselist=False`的附加结果，因此在该错误情况下的结果不应改变。

[＃3249 T0\>](http://www.sqlalchemy.org/trac/ticket/3249)

### 如果与join()，select\_from()，from\_self()一起使用，query.update()/ query.delete()会引发[¶](#query-update-query-delete-raises-if-used-with-join-select-from-from-self "Permalink to this headline")

A warning is emitted in SQLAlchemy 0.9.10 (not yet released as of June
9, 2015) when the [`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")
or [`Query.delete()`](orm_query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")
methods are invoked against a query which has also called upon
[`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join"),
[`Query.outerjoin()`](orm_query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin"),
[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
or [`Query.from_self()`](orm_query.html#sqlalchemy.orm.query.Query.from_self "sqlalchemy.orm.query.Query.from_self").
这些不支持的用例在 0.9 系列中默默无效，直到发出警告为止。在 1.0 中，这些情况引发了一个例外。

[＃3349 T0\>](http://www.sqlalchemy.org/trac/ticket/3349)

### query.update()with `synchronize_session='evaluate'`引发多表更新[¶](#query-update-with-synchronize-session-evaluate-raises-on-multi-table-update "Permalink to this headline")

[`Query.update()`](orm_query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")的“评估程序”不适用于多表更新，需要设置为`synchronize_session=False`或`synchronize_session='fetch'`。新的行为是，现在引发了一个明确的异常，并带有一条消息来更改同步设置。这是从 0.9.7 发出的警告升级而来的。

[＃3117 T0\>](http://www.sqlalchemy.org/trac/ticket/3117)

### 复活事件已被删除[¶](#resurrect-event-has-been-removed "Permalink to this headline")

“复活”ORM 事件已被完全删除。从 0.8 版本开始，该事件不再具有任何功能，从工作单元中删除旧的“可变”系统。

### 使用from\_self()，count()[时，更改为单表继承条件](#change-to-single-table-inheritance-criteria-when-using-from-self-count "Permalink to this headline")

给定一个单表继承映射，如：

    class Widget(Base):
        __table__ = 'widget_table'

    class FooWidget(Widget):
        pass

对子类使用[`Query.from_self()`](orm_query.html#sqlalchemy.orm.query.Query.from_self "sqlalchemy.orm.query.Query.from_self")或[`Query.count()`](orm_query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")会产生子查询，但是将子类型的“WHERE”标准添加到外部：

    sess.query(FooWidget).from_self().all()

渲染：

    SELECT
        anon_1.widgets_id AS anon_1_widgets_id,
        anon_1.widgets_type AS anon_1_widgets_type
    FROM (SELECT widgets.id AS widgets_id, widgets.type AS widgets_type,
    FROM widgets) AS anon_1
    WHERE anon_1.widgets_type IN (?)

问题在于，如果内部查询没有指定所有列，那么我们不能在外部添加WHERE子句（它实际上会尝试并产生错误的查询）。这个决定显然回到了0.6.5，注释“可能需要对此做出更多调整”。那么，这些调整已经到来！所以现在上面的查询会呈现：

    SELECT
        anon_1.widgets_id AS anon_1_widgets_id,
        anon_1.widgets_type AS anon_1_widgets_type
    FROM (SELECT widgets.id AS widgets_id, widgets.type AS widgets_type,
    FROM widgets
    WHERE widgets.type IN (?)) AS anon_1

所以那些不包含“type”的查询仍然可以工作！:

    sess.query(FooWidget.id).count()

呈现：

    SELECT count(*) AS count_1
    FROM (SELECT widgets.id AS widgets_id
    FROM widgets
    WHERE widgets.type IN (?)) AS anon_1

[＃3177 T0\>](http://www.sqlalchemy.org/trac/ticket/3177)

### 单表继承条件无条件地添加到所有 ON 子句[¶](#single-table-inheritance-criteria-added-to-all-on-clauses-unconditionally "Permalink to this headline")

当连接到单表继承子类目标时，ORM在加入关系时总是添加“单表标准”。给定映射为：

    class Widget(Base):
        __tablename__ = 'widget'
        id = Column(Integer, primary_key=True)
        type = Column(String)
        related_id = Column(ForeignKey('related.id'))
        related = relationship("Related", backref="widget")
        __mapper_args__ = {'polymorphic_on': type}


    class FooWidget(Widget):
        __mapper_args__ = {'polymorphic_identity': 'foo'}


    class Related(Base):
        __tablename__ = 'related'
        id = Column(Integer, primary_key=True)

一段时间以来，关系的加入会为该类型提供一个“单一继承”子句：

    s.query(Related).join(FooWidget, Related.widget).all()

SQL 输出：

    SELECT related.id AS related_id
    FROM related JOIN widget ON related.id = widget.related_id AND widget.type IN (:type_1)

Above, because we joined to a subclass `FooWidget`,
[`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
knew to add the `AND widget.type IN ('foo')`
criteria to the ON clause.

这里的变化是，`AND widget.type IN()`条件现在附加到*任何*
ON子句，不只是从关系中产生的那些，包括一个明确说明的关系：

    # ON clause will now render as
    # related.id = widget.related_id AND widget.type IN (:type_1)
    s.query(Related).join(FooWidget, FooWidget.related_id == Related.id).all()

当没有任何类型的ON子句被声明时，以及“隐式”连接：

    # ON clause will now render as
    # related.id = widget.related_id AND widget.type IN (:type_1)
    s.query(Related).join(FooWidget).all()

以前，这些ON子句不包含单继承条件。已经添加此标准以解决此问题的应用程序将希望删除其显式使用，但如果标准在此期间发生两次，它应该继续正常工作。

也可以看看

[Changes and fixes in handling of duplicate join targets](#bug-3233)

[＃3222 T0\>](http://www.sqlalchemy.org/trac/ticket/3222)

关键行为改变 - 核心[¶](#key-behavioral-changes-core "Permalink to this headline")
---------------------------------------------------------------------------------

### 将完整的 SQL 片段强制转换为 text()[¶](#warnings-emitted-when-coercing-full-sql-fragments-into-text "Permalink to this headline")时发出警告

自从SQLAlchemy开始以来，一直强调不妨碍纯文本的使用。The Core and ORM
expression systems were intended to allow any number of points at which
the user can just use plain text SQL expressions, not just in the sense
that you can send a full SQL string to [`Connection.execute()`](core_connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute"),
but that you can send strings with SQL expressions into many functions,
such as [`Select.where()`](core_selectable.html#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where"),
[`Query.filter()`](orm_query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter"),
and [`Select.order_by()`](core_selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by").

Note that by “SQL expressions” we mean a **full fragment of a SQL
string**, such as:

    # the argument sent to where() is a full SQL expression
    stmt = select([sometable]).where("somecolumn = 'value'")

and we are **not talking about string arguments**, that is, the normal
behavior of passing string values that become parameterized:

    # This is a normal Core expression with a string argument -
    # we aren't talking about this!!
    stmt = select([sometable]).where(sometable.c.somecolumn == 'value')

Core教程一直以来都使用这种技术，使用[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造，其中几乎所有组件都被指定为直线。然而，尽管这种长期存在的行为和示例，用户显然对这种行为存在感到惊讶，并且在询问社区时，我无法找到任何实际上*没有感到惊讶的用户，您可以将完整的字符串发送到像[`Query.filter()`](orm_query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")这样的方法中。*

所以这里的改变是鼓励用户在编写部分或全部由文本片段组成的 SQL 时限定文本字符串。在撰写选择时如下所示：

    stmt = select(["a", "b"]).where("a = b").select_from("sometable")

声明是正常建立的，与以前一样强制执行。但是，您会看到以下警告消息：

    SAWarning: Textual column expression 'a' should be explicitly declared
    with text('a'), or use column('a') for more specificity
    (this warning may be suppressed after 10 occurrences)

    SAWarning: Textual column expression 'b' should be explicitly declared
    with text('b'), or use column('b') for more specificity
    (this warning may be suppressed after 10 occurrences)

    SAWarning: Textual SQL expression 'a = b' should be explicitly declared
    as text('a = b') (this warning may be suppressed after 10 occurrences)

    SAWarning: Textual SQL FROM expression 'sometable' should be explicitly
    declared as text('sometable'), or use table('sometable') for more
    specificity (this warning may be suppressed after 10 occurrences)

这些警告试图通过显示参数以及接收字符串的位置来准确显示问题的出处。警告使用[Session.get\_bind()
handles a wider variety of inheritance
scenarios](#feature-3178)，以便可以安全地发出参数化警告而不会耗尽内存，并且如果希望警告是例外情况，应该使用[Python
Warnings Filter](https://docs.python.org/2/library/warnings.html)：

    import warnings
    warnings.simplefilter("error")   # all warnings raise an exception

鉴于上述警告，我们的声明工作得很好，但为了摆脱警告，我们将重写我们的声明如下：

    from sqlalchemy import select, textplain
    stmt = select([
            text("a"),
            text("b")
        ]).where(text("a = b")).select_from(text("sometable"))

正如警告所暗示的，如果我们使用[`column()`](core_sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")和[`table()`](core_selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")，我们可以更具体地说明文本。

    from sqlalchemy import select, text, column, tableplain

    stmt = select([column("a"), column("b")]).\
        where(text("a = b")).select_from(table("sometable"))

还要注意，现在可以从“sqlalchemy”中导入[`table()`](core_selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")和[`column()`](core_sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")，而不使用“sql”部分。

The behavior here applies to [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
as well as to key methods on [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query"),
including [`Query.filter()`](orm_query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter"),
[`Query.from_statement()`](orm_query.html#sqlalchemy.orm.query.Query.from_statement "sqlalchemy.orm.query.Query.from_statement")
and [`Query.having()`](orm_query.html#sqlalchemy.orm.query.Query.having "sqlalchemy.orm.query.Query.having").

#### ORDER BY和GROUP BY是特殊情况[¶](#order-by-and-group-by-are-special-cases "Permalink to this headline")

有一种情况使用字符串具有特殊含义，并且作为此更改的一部分，我们已增强其功能。当我们有一个引用某个列名或命名标签的[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")或[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")时，我们可能想要 GROUP
BY 和/或 ORDER BY 已知列或标签：

    stmt = select([plain
        user.c.name,
        func.count(user.c.id).label("id_count")
    ]).group_by("name").order_by("id_count")

在上面的语句中，我们希望看到“ORDER BY
id\_count”，而不是函数的重新声明。The string argument given is actively
matched to an entry in the columns clause during compilation, so the
above statement would produce as we expect, without warnings (though
note that the `"name"` expression has been resolved
to `users.name`! ）：

    SELECT users.name, count(users.id) AS id_count
    FROM users GROUP BY users.name ORDER BY id_count

但是，如果我们引用无法找到的名称，则我们再次收到警告，如下所示：

    stmt = select([
            user.c.name,
            func.count(user.c.id).label("id_count")
        ]).order_by("some_label")

输出符合我们的说法，但它又一次警告我们：

    SAWarning: Can't resolve label reference 'some_label'; converting toplain
    text() (this warning may be suppressed after 10 occurrences)

    SELECT users.name, count(users.id) AS id_count
    FROM users ORDER BY some_label

上述行为适用于我们可能想要参考所谓的“标签参考”的所有地方； ORDER
BY 和 GROUP BY，但也包含在 OVER 子句中，以及引用列的 DISTINCT
ON 子句（例如 Postgresql 语法）。

我们仍然可以使用[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")为 ORDER
BY 或其他表达式指定任意表达式：

    stmt = select([users]).order_by(text("some special expression"))

整个变化的结果是SQLAlchemy现在希望我们在发送字符串时告诉它该字符串显式为[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")构造，或者列，表等，并且if我们使用它作为标签名称，按照group
by或其他表达式进行排序，SQLAlchemy预期字符串会解析为已知的内容，否则应该再次使用[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")或类似方法进行限定。

[＃2992 T0\>](http://www.sqlalchemy.org/trac/ticket/2992)

### 在使用多值插入时，为每行调用 Python 方默认值[¶](#python-side-defaults-invoked-for-each-row-invidually-when-using-a-multivalued-insert "Permalink to this headline")

当使用多值版本的[`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")时，支持 Python 端列的默认设置基本上未实现，并且只能在特定情况下“偶然”工作，当使用的方言是使用非定位（例如命名）风格的绑定参数，以及何时不需要为每一行调用 Python 端可调用。

该功能已经过大修，因此其功能与“executemany”风格的调用类似：

    import itertoolsplainplain

    counter = itertools.count(1)
    t = Table(
        'my_table', metadata,
        Column('id', Integer, default=lambda: next(counter)),
        Column('data', String)
    )

    conn.execute(t.insert().values([
        {"data": "d1"},
        {"data": "d2"},
        {"data": "d3"},
    ]))

上面的例子将会像预期的那样分别为每一行调用`next(counter)`：

    INSERT INTO my_table (id, data) VALUES (?, ?), (?, ?), (?, ?)plain
    (1, 'd1', 2, 'd2', 3, 'd3')

以前，位置方言会失败，因为不会为其他位置生成绑定：

    Incorrect number of bindings supplied. The current statement uses 6,plain
    and there are 4 supplied.
    [SQL: u'INSERT INTO my_table (id, data) VALUES (?, ?), (?, ?), (?, ?)']
    [parameters: (1, 'd1', 'd2', 'd3')]

并且使用“named”方言，“id”的相同值将在每一行中重复使用（因此，此更改与依赖此的系统反向不兼容）：

    INSERT INTO my_table (id, data) VALUES (:id, :data_0), (:id, :data_1), (:id, :data_2)
    {u'data_2': 'd3', u'data_1': 'd2', u'data_0': 'd1', 'id': 1}

系统也会拒绝将“服务器端”默认值作为内联呈现的 SQL 调用，因为无法保证服务器端默认值与此兼容。如果 VALUES 子句为特定列呈现，则需要 Python 端值；如果省略的值仅指服务器端的默认值，则会引发异常：

    t = Table(
        'my_table', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', String, server_default='some default')
    )

    conn.execute(t.insert().values([
        {"data": "d1"},
        {"data": "d2"},
        {},
    ]))

会提高：

    sqlalchemy.exc.CompileError: INSERT value for column my_table.data isplain
    explicitly rendered as a boundparameter in the VALUES clause; a
    Python-side value or SQL expression is required

以前，值“d1”将被复制到第三行的值（但是只能使用命名格式！）：

    INSERT INTO my_table (data) VALUES (:data_0), (:data_1), (:data_0)
    {u'data_1': 'd2', u'data_0': 'd1'}

[＃3288 T0\>](http://www.sqlalchemy.org/trac/ticket/3288)

### 事件侦听器不能在该事件的运行器[¶](#event-listeners-can-not-be-added-or-removed-from-within-that-event-s-runner "Permalink to this headline")中添加或删除

从同一事件本身中删除事件侦听器会在迭代过程中修改列表的元素，这将导致静态连接的事件侦听器无法启动。为了在保持性能的同时避免这种情况发生，列表已被替换为`collections.deque()`，它不允许在迭代过程中进行任何添加或删除操作，而是引发`RuntimeError`。

[＃3163 T0\>](http://www.sqlalchemy.org/trac/ticket/3163)

### INSERT ... FROM SELECT结构现在意味着`inline=True` [¶](#the-insert-from-select-construct-now-implies-inline-true "Permalink to this headline")

现在使用[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")意味着`inline=True`在[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")上。这有助于修复 INSERT
... FROM
SELECT 构造无意中编译为支持后端的“隐式返回”的错误，这会在插入零行的 INSERT 情况下导致破坏（因为隐式返回期望行）
，以及在插入多行的 INSERT 情况下的任意返回数据（例如，只有很多行的第一行）。一个类似的更改也适用于具有多个参数集的 INSERT..VALUES；隐含的 RETURNING 将不再为此语句发出。由于这两个构造都处理可变数量的行，所以[`ResultProxy.inserted_primary_key`](core_connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")访问器不适用。以前，有一个文档说明，有人可能更喜欢带有INSERT..FROM
SELECT的`inline=True`，因为有些数据库不支持返回，因此不能做“隐式”返回，但没有任何理由INSERT
... FROM
SELECT需要在任何情况下隐式返回。如果需要插入数据，则应使用常规显式[`Insert.returning()`](core_dml.html#sqlalchemy.sql.expression.Insert.returning "sqlalchemy.sql.expression.Insert.returning")返回可变数目的结果行。

[＃3169 T0\>](http://www.sqlalchemy.org/trac/ticket/3169)

### `autoload_with`现在意味着`autoload=True` [¶](#autoload-with-now-implies-autoload-true "Permalink to this headline")

通过单独传递[`Table.autoload_with`](core_metadata.html#sqlalchemy.schema.Table.params.autoload_with "sqlalchemy.schema.Table")，可以设置[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")进行反射：

    my_table = Table('my_table', metadata, autoload_with=some_engine)plain

[＃3027 T0\>](http://www.sqlalchemy.org/trac/ticket/3027)

### DBAPI 异常包装和 handle\_error()事件改进[¶](#dbapi-exception-wrapping-and-handle-error-event-improvements "Permalink to this headline")

在[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象失效，然后尝试重新连接并遇到错误的情况下，SQLAlchemy 的包装 DBAPI 异常不会发生；这已经解决了。

此外，最近添加的[`ConnectionEvents.handle_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.handle_error "sqlalchemy.events.ConnectionEvents.handle_error")事件现在将针对初始连接时发生的错误，重新连接时以及在使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")时给定自定义连接通过[`create_engine.creator`](core_engines.html#sqlalchemy.create_engine.params.creator "sqlalchemy.create_engine")执行功能。

The [`ExceptionContext`](core_connections.html#sqlalchemy.engine.ExceptionContext "sqlalchemy.engine.ExceptionContext")
object has a new datamember [`ExceptionContext.engine`](core_connections.html#sqlalchemy.engine.ExceptionContext.engine "sqlalchemy.engine.ExceptionContext.engine")
that will always refer to the [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
in use, in those cases when the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
object is not available (e.g. on initial connect).

[＃3266 T0\>](http://www.sqlalchemy.org/trac/ticket/3266)

### ForeignKeyConstraint.columns 现在是一个 ColumnCollection [¶](#foreignkeyconstraint-columns-is-now-a-columncollection "Permalink to this headline")

`ForeignKeyConstraint.columns`
was previously a plain list containing either strings or [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
objects, depending on how the [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
was constructed and whether it was associated with a table.
该集合现在是[`ColumnCollection`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")，并且仅在[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")与[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")关联后才被初始化。A
new accessor [`ForeignKeyConstraint.column_keys`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.column_keys "sqlalchemy.schema.ForeignKeyConstraint.column_keys")
is added to unconditionally return string keys for the local set of
columns regardless of how the object was constructed or its current
state.

### MetaData.sorted\_tables访问器是“确定性的”[¶](#metadata-sorted-tables-accessor-is-deterministic "Permalink to this headline")

The sorting of tables resulting from the [`MetaData.sorted_tables`](core_metadata.html#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")
accessor is “deterministic”; the ordering should be the same in all
cases regardless of Python hashing.
这是通过首先按名称对表格进行排序，然后将它们传递给拓扑算法，该拓扑算法在迭代时保持排序。

Note that this change does **not** yet apply to the ordering applied
when emitting [`MetaData.create_all()`](core_metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
or [`MetaData.drop_all()`](core_metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all").

[＃3084 T0\>](http://www.sqlalchemy.org/trac/ticket/3084)

### null()，false()和true()常量不再是单身人士[¶](#null-false-and-true-constants-are-no-longer-singletons "Permalink to this headline")

这三个常量被更改为返回 0.9 中的“单例”值；不幸的是，这会导致像下面这样的查询不能按预期呈现：

    select([null(), null()])

rendering only `SELECT NULL AS anon_1`, because the
two [`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")
constructs would come out as the same `NULL` object,
and SQLAlchemy’s Core model is based on object identity in order to
determine lexical significance.
除了希望节省物体开销之外，0.9中的变化并不重要；一般来说，一个未命名的构造需要保持词汇上的独特性，以便得到唯一的标记。

[＃3170 T0\>](http://www.sqlalchemy.org/trac/ticket/3170)

### SQLite / Oracle具有不同的临时表/视图名称报告方法[¶](#sqlite-oracle-have-distinct-methods-for-temporary-table-view-name-reporting "Permalink to this headline")

在 SQLite / Oracle 的情况下，[`Inspector.get_table_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names "sqlalchemy.engine.reflection.Inspector.get_table_names")和[`Inspector.get_view_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names "sqlalchemy.engine.reflection.Inspector.get_view_names")方法也会返回临时表和视图的名称，任何其他方言（在 MySQL 的情况下，至少它是不可能的）。This
logic has been moved out to two new methods
[`Inspector.get_temp_table_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_temp_table_names "sqlalchemy.engine.reflection.Inspector.get_temp_table_names")
and [`Inspector.get_temp_view_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_temp_view_names "sqlalchemy.engine.reflection.Inspector.get_temp_view_names").

Note that reflection of a specific named temporary table or temporary
view, either by `Table('name', autoload=True)` or
via methods like [`Inspector.get_columns()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns "sqlalchemy.engine.reflection.Inspector.get_columns")
continues to function for most if not all dialects.
特别是对于SQLite，还有一个针对临时表的UNIQUE约束反射的错误修复，它是[＃3203](http://www.sqlalchemy.org/trac/ticket/3203)。

[＃3204 T0\>](http://www.sqlalchemy.org/trac/ticket/3204)

方言的改进和变化 - Postgresql [¶](#dialect-improvements-and-changes-postgresql "Permalink to this headline")
------------------------------------------------------------------------------------------------------------

### ENUM类型创建/删除规则的大修[¶](#overhaul-of-enum-type-create-drop-rules "Permalink to this headline")

对于创建和删除TYPE，Postgresql [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")的规则更为严格。

An [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
that is created **without** being explicitly associated with a
[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
object will be created *and* dropped corresponding to
[`Table.create()`](core_metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create")
and [`Table.drop()`](core_metadata.html#sqlalchemy.schema.Table.drop "sqlalchemy.schema.Table.drop"):

    table = Table('sometable', metadata,
        Column('some_enum', ENUM('a', 'b', 'c', name='myenum'))
    )

    table.create(engine)  # will emit CREATE TYPE and CREATE TABLE
    table.drop(engine)  # will emit DROP TABLE and DROP TYPE - new for 1.0

这意味着如果第二个表也有一个名为'myenum'的枚举，那么上面的 DROP 操作现在将失败。为了适应普通共享枚举类型的用例，元数据关联枚举的行为已得到增强。

An [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
that is created **with** being explicitly associated with a
[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
object will *not* be created *or* dropped corresponding to
[`Table.create()`](core_metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create")
and [`Table.drop()`](core_metadata.html#sqlalchemy.schema.Table.drop "sqlalchemy.schema.Table.drop"),
with the exception of [`Table.create()`](core_metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create")
called with the `checkfirst=True` flag:

    my_enum = ENUM('a', 'b', 'c', name='myenum', metadata=metadata)

    table = Table('sometable', metadata,
        Column('some_enum', my_enum)
    )

    # will fail: ENUM 'my_enum' does not exist
    table.create(engine)

    # will check for enum and emit CREATE TYPE
    table.create(engine, checkfirst=True)

    table.drop(engine)  # will emit DROP TABLE, *not* DROP TYPE

    metadata.drop_all(engine) # will emit DROP TYPE

    metadata.create_all(engine) # will emit CREATE TYPE

[＃3319 T0\>](http://www.sqlalchemy.org/trac/ticket/3319)

### 新的Postgresql表选项[¶](#new-postgresql-table-options "Permalink to this headline")

当通过[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造渲染 DDL 时，增加了对 PG 表格选项 TABLESPACE，ON
COMMIT，WITH（OUT）OIDS 和 INHERITS 的支持。

也可以看看

[PostgreSQL Table
Options](dialects_postgresql.html#postgresql-table-options)

[＃2051 T0\>](http://www.sqlalchemy.org/trac/ticket/2051)

### 使用Postgresql Dialect [¶](#new-get-enums-method-with-postgresql-dialect "Permalink to this headline")的新get\_enums()方法

在 Postgresql 中，[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")方法返回一个[`PGInspector`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector "sqlalchemy.dialects.postgresql.base.PGInspector")对象，其中包含一个新的[`PGInspector.get_enums()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_enums "sqlalchemy.dialects.postgresql.base.PGInspector.get_enums")方法，该方法返回所有可用的`ENUM`类型：

    from sqlalchemy import inspect, create_engine

    engine = create_engine("postgresql+psycopg2://host/dbname")
    insp = inspect(engine)
    print(insp.get_enums())

也可以看看

[`PGInspector.get_enums()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_enums "sqlalchemy.dialects.postgresql.base.PGInspector.get_enums")

### Postgresql Dialect反映了物化视图，外部表[¶](#postgresql-dialect-reflects-materialized-views-foreign-tables "Permalink to this headline")

变化如下：

-   带有`autoload=True`的`Table`结构现在将匹配存在于数据库中的名称作为物化视图或外部表。
-   [`Inspector.get_view_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names "sqlalchemy.engine.reflection.Inspector.get_view_names")
    will return plain and materialized view names.
-   [`Inspector.get_table_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names "sqlalchemy.engine.reflection.Inspector.get_table_names")
    does **not** change for Postgresql, it continues to return only the
    names of plain tables.
-   添加了一个新方法[`PGInspector.get_foreign_table_names()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_foreign_table_names "sqlalchemy.dialects.postgresql.base.PGInspector.get_foreign_table_names")，它将返回Postgresql模式表中明确标记为“外部”的表的名称。

对反射的改变包括将`'m'`和`'f'`添加到我们在查询`pg_class.relkind`时使用的限定符列表中，但是此更改在1.0.0中是新的，以避免那些在生产中运行0.9的人出现任何向后不兼容的意外。

[＃2891 T0\>](http://www.sqlalchemy.org/trac/ticket/2891)

### Postgresql `has_table()`现在可用于临时表[¶](#postgresql-has-table-now-works-for-temporary-tables "Permalink to this headline")

这是一个简单的修复，现在可以使用临时表的“有表”，以便可以继续执行以下代码：

    from sqlalchemy import *

    metadata = MetaData()
    user_tmp = Table(
        "user_tmp", metadata,
        Column("id", INT, primary_key=True),
        Column('name', VARCHAR(50)),
        prefixes=['TEMPORARY']
    )

    e = create_engine("postgresql://scott:tiger@localhost/test", echo='debug')
    with e.begin() as conn:
        user_tmp.create(conn, checkfirst=True)

        # checkfirst will succeed
        user_tmp.create(conn, checkfirst=True)

这种行为会导致非失败应用程序的行为不同，这是非常不可能的，因为 Postgresql 允许非临时表以静默方式覆盖临时表。因此，像下面这样的代码现在将完全不同，不再在临时表之后创建真实表：

    from sqlalchemy import *plain

    metadata = MetaData()
    user_tmp = Table(
        "user_tmp", metadata,
        Column("id", INT, primary_key=True),
        Column('name', VARCHAR(50)),
        prefixes=['TEMPORARY']
    )

    e = create_engine("postgresql://scott:tiger@localhost/test", echo='debug')
    with e.begin() as conn:
        user_tmp.create(conn, checkfirst=True)

        m2 = MetaData()
        user = Table(
            "user_tmp", m2,
            Column("id", INT, primary_key=True),
            Column('name', VARCHAR(50)),
        )

        # in 0.9, *will create* the new table, overwriting the old one.
        # in 1.0, *will not create* the new table
        user.create(conn, checkfirst=True)

[＃3264 T0\>](http://www.sqlalchemy.org/trac/ticket/3264)

### Postgresql FILTER 关键字[¶](#postgresql-filter-keyword "Permalink to this headline")

Postgresql 现在支持 9.4 的集合函数的 SQL 标准 FILTER 关键字。SQLAlchemy 允许使用[`FunctionElement.filter()`](core_functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")：

    func.count(1).filter(True)

也可以看看

[`FunctionElement.filter()`](core_functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")

[`FunctionFilter`](core_sqlelement.html#sqlalchemy.sql.expression.FunctionFilter "sqlalchemy.sql.expression.FunctionFilter")

### PG8000 方言支持客户端编码[¶](#pg8000-dialect-supports-client-side-encoding "Permalink to this headline")

[`create_engine.encoding`](core_engines.html#sqlalchemy.create_engine.params.encoding "sqlalchemy.create_engine")参数现在可以通过pg8000方言使用连接处理程序，它可以发出`SET CLIENT_ENCODING`匹配所选的编码。

### PG8000 本机 JSONB 支持[¶](#pg8000-native-jsonb-support "Permalink to this headline")

已经添加了对 PG8000 版本大于 1.10.1 的支持，其中原生支持 JSONB。

### 支持pypy [¶](#support-for-psycopg2cffi-dialect-on-pypy "Permalink to this headline")上的psycopg2cffi Dialect

增加了对pypy psycopg2cffi方言的支持。

也可以看看

[`sqlalchemy.dialects.postgresql.psycopg2cffi`](dialects_postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2cffi "sqlalchemy.dialects.postgresql.psycopg2cffi")

方言的改进和改变 - MySQL [¶](#dialect-improvements-and-changes-mysql "Permalink to this headline")
--------------------------------------------------------------------------------------------------

### 在所有情况下，MySQL TIMESTAMP类型现在都会呈现NULL / NOT NULL [¶](#mysql-timestamp-type-now-renders-null-not-null-in-all-cases "Permalink to this headline")

如果使用`nullable=True`设置列，则 MySQL 方言一直通过为这种类型发送 NULL 来解决 MySQL 的与 TIMESTAMP 列相关的隐式 NOT
NULL 默认值。但是，MySQL
5.6.6 及更高版本提供了一个新标记[explicit\_defaults\_for\_timestamp](http://dev.mysql.com/doc/refman/5.6/en/server-system-variables.html#sysvar_explicit_defaults_for_timestamp)，它修复了 MySQL 的非标准行为，使其表现得像其他类型一样；为了适应这种情况，SQLAlchemy 现在无条件地为所有 TIMESTAMP 列发出 NULL
/ NOT NULL。

也可以看看

[TIMESTAMP Columns and NULL](dialects_mysql.html#mysql-timestamp-null)

[＃3155 T0\>](http://www.sqlalchemy.org/trac/ticket/3155)

### MySQL SET Type大写，支持空集，unicode，空值处理[¶](#mysql-set-type-overhauled-to-support-empty-sets-unicode-blank-value-handling "Permalink to this headline")

[`mysql.SET`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET "sqlalchemy.dialects.mysql.SET")类型历史上不包括分别处理空白集和空值的系统；因为不同的驱动程序在处理空字符串和空字符集表示方面有不同的行为，所以SET类型只试图在这些行为之间进行对冲，选择将空集作为`set([''])`这里的部分原因是，否则实际上不可能在MySQL
SET中存储一个空字符串，因为驱动程序给我们返回的字符串无法区分`set([''])`和`set()`用户确定是否`set([''])`实际上表示“空集”。

新行为将空字符串的用例（这是一个甚至在MySQL文档中没有记录的异常情况）移动到一个特殊情况，现在[`mysql.SET`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET "sqlalchemy.dialects.mysql.SET")的默认行为是：

-   将 MySQL-python 返回的空字符串`''`处理为空set
    `set()`；
-   将MySQL-Connector-Python返回的单空值集合`set([''])`转换为空set `set()`；
-   为了处理实际希望在其可能值列表中包含空值`''`的集合类型的情况，实现了一个新特性（在这个用例中是必需的），从而设置值被持久化并且作为一个按位整数值加载；添加标志[`mysql.SET.retrieve_as_bitwise`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise "sqlalchemy.dialects.mysql.SET")以启用此功能。

通过使用[`mysql.SET.retrieve_as_bitwise`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise "sqlalchemy.dialects.mysql.SET")标志，可以保持集合的持久性，并且检索时不会出现任何含糊不清的值。理论上这个标志可以在任何情况下被打开，只要该类型的给定值列表与数据库中声明的顺序完全匹配即可。它只会使 SQL
echo 输出更加不寻常。

[`mysql.SET`](dialects_mysql.html#sqlalchemy.dialects.mysql.SET "sqlalchemy.dialects.mysql.SET")的默认行为保持不变，使用字符串往返传值。基于字符串的行为现在支持unicode完全包含use\_unicode
= 0的MySQL-python。

[＃3283 T0\>](http://www.sqlalchemy.org/trac/ticket/3283)

### MySQL内部“没有这样的表”异常不会传递给事件处理程序[¶](#mysql-internal-no-such-table-exceptions-not-passed-to-event-handlers "Permalink to this headline")

现在，MySQL方言将禁止[`ConnectionEvents.handle_error()`](core_events.html#sqlalchemy.events.ConnectionEvents.handle_error "sqlalchemy.events.ConnectionEvents.handle_error")事件触发它在内部使用的用于检测表是否存在的语句。这是通过使用执行选项`skip_user_error_events`来实现的，该选项为该执行的范围禁用句柄错误事件。通过这种方式，重写异常的用户代码不需要担心偶尔需要捕获 SQLAlchemy 特定异常的 MySQL 方言或其他方言。

### 为MySQL连接器更改了`raise_on_warnings`的默认值[¶](#changed-the-default-value-of-raise-on-warnings-for-mysql-connector "Permalink to this headline")

MySQL-Connector将“raise\_on\_warnings”的默认值更改为 False。由于某种原因，这被设置为 True。不幸的是，“缓冲”标志必须保持为 True，因为 MySQL 连接器不允许游标关闭，除非所有结果都被完全获取。

[＃2515 T0\>](http://www.sqlalchemy.org/trac/ticket/2515)

### MySQL布尔符号“true”，“false”再次工作[¶](#mysql-boolean-symbols-true-false-work-again "Permalink to this headline")

对 IS / IS
NOT 运算符进行 0.9 版本的修改以及[＃2682](http://www.sqlalchemy.org/trac/ticket/2682)中的布尔类型不允许 MySQL 方言在“IS”的上下文中使用“true”和“false”
/ “不是”。显然，即使 MySQL 没有“boolean”类型，即使这些符号与“1”和“0”（和 IS
/ IS）是同义的，它仍然支持 IS / IS NOT。不是不适用于数字）。

因此，这里的变化是 MySQL 方言仍然是“非本地布尔”，但是[`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")和[`false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")符号再次产生关键字“true”和“false
“，这样像`column.is_(true())`这样的表达式再次适用于MySQL。

[＃3186 T0\>](http://www.sqlalchemy.org/trac/ticket/3186)

### match()运算符现在返回与MySQL的浮点返回值兼容的不可知的MatchType [¶](#the-match-operator-now-returns-an-agnostic-matchtype-compatible-with-mysql-s-floating-point-return-value "Permalink to this headline")

一个[`ColumnOperators.match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")表达式的返回类型现在是一个名为[`MatchType`](core_type_basics.html#sqlalchemy.types.MatchType "sqlalchemy.types.MatchType")的新类型。这是[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")的一个子类，可以通过方言拦截，以便在 SQL 执行时产生不同的结果类型。

像下面这样的代码现在可以正常工作并返回MySQL上的浮点数：

    >>> connection.execute(
    ...    select([
    ...        matchtable.c.title.match('Agile Ruby Programming').label('ruby'),
    ...        matchtable.c.title.match('Dive Python').label('python'),
    ...        matchtable.c.title
    ...    ]).order_by(matchtable.c.id)
    ... )
    [
        (2.0, 0.0, 'Agile Web Development with Ruby On Rails'),
        (0.0, 2.0, 'Dive Into Python'),
        (2.0, 0.0, "Programming Matz's Ruby"),
        (0.0, 0.0, 'The Definitive Guide to Django'),
        (0.0, 1.0, 'Python in a Nutshell')
    ]

[＃3263 T0\>](http://www.sqlalchemy.org/trac/ticket/3263)

### 细雨方言现在是一种外语[¶](#drizzle-dialect-is-now-an-external-dialect "Permalink to this headline")

The dialect for [Drizzle](http://www.drizzle.org/) is now an external
dialect, available at
[https://bitbucket.org/zzzeek/sqlalchemy-drizzle](https://bitbucket.org/zzzeek/sqlalchemy-drizzle).
在 SQLAlchemy 能够适应第三方方言之前，这种方言被添加到了 SQLAlchemy 中；未来，所有不属于“无所不在”类别的数据库都是第三方方言。方言的实现没有改变，仍然基于 SQLAlchemy 中的 MySQL
+
MySQLdb方言。方言尚未发布，处于“阁楼”地位；但是它通过了大部分测试，并且一般都处于体面的工作状态，如果有人想要接受抛光。

方言的改进和改变 - SQLite [¶](#dialect-improvements-and-changes-sqlite "Permalink to this headline")
----------------------------------------------------------------------------------------------------

### SQLite 命名和未命名的 UNIQUE 和 FOREIGN KEY 约束将检查和反映[¶](#sqlite-named-and-unnamed-unique-and-foreign-key-constraints-will-inspect-and-reflect "Permalink to this headline")

UNIQUE 和 FOREIGN
KEY 约束现在完全反映在 SQLite 中，无论是否带有名称。以前，外键名称被忽略，未命名的唯一约束被忽略。特别是这将有助于 Alembic 的新 SQLite 迁移功能。

为了实现这一点，对于外键和唯一约束，PRAGMA
foreign\_keys，index\_list 和 index\_info 的结果与 CREATE
TABLE 语句的正则表达式解析相结合，以形成约束名称的完整图片，以及区分 UNIQUE 作为 UNIQUE 与未命名的 INDEX 创建的约束。

[＃3244 T0\>](http://www.sqlalchemy.org/trac/ticket/3244)

[＃3261 T0\>](http://www.sqlalchemy.org/trac/ticket/3261)

方言的改进和改变 - SQL Server [¶](#dialect-improvements-and-changes-sql-server "Permalink to this headline")
------------------------------------------------------------------------------------------------------------

### 基于主机名的 SQL Server 连接需要 PyODBC 驱动程序名称[¶](#pyodbc-driver-name-is-required-with-hostname-based-sql-server-connections "Permalink to this headline")

使用无 DSN 连接的 PyODBC 连接到 SQL
Server，例如使用明确的主机名，现在需要一个驱动程序名 -
SQLAlchemy 将不再尝试猜测默认值：

    engine = create_engine("mssql+pyodbc://scott:tiger@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0")plain

SQLAlchemy 以前硬编码的默认“SQL
Server”在 Windows 上已过时，并且 SQLAlchemy 不能根据操作系统/驱动程序检测猜测最佳驱动程序。使用 ODBC 完全避免此问题时，始终首选使用 DSN。

[＃3182 T0\>](http://www.sqlalchemy.org/trac/ticket/3182)

### SQL Server 2012 大型文本/二进制类型呈现为 VARCHAR，NVARCHAR，VARBINARY [¶](#sql-server-2012-large-text-binary-types-render-as-varchar-nvarchar-varbinary "Permalink to this headline")

对于 SQL Server 2012 及更高版本，[`Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")，[`UnicodeText`](core_type_basics.html#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")和[`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")类型的呈现已更改，并具有完全控制行为的选项，基于微软的弃用准则。有关详细信息，请参阅[Large
Text/Binary Type
Deprecation](dialects_mssql.html#mssql-large-type-deprecation)。

方言的改进和改变 - Oracle [¶](#dialect-improvements-and-changes-oracle "Permalink to this headline")
----------------------------------------------------------------------------------------------------

### 在 Oracle [¶](#improved-support-for-ctes-in-oracle "Permalink to this headline")中改进了对CTE的支持

CTE 对 Oracle 的支持已经得到了修复，并且还有一个新特性`CTE.with_suffixes()`可以帮助 Oracle 的特殊指令：

    included_parts = select([plain
        part.c.sub_part, part.c.part, part.c.quantity
    ]).where(part.c.part == "p1").\
        cte(name="included_parts", recursive=True).\
        suffix_with(
            "search depth first by part set ord1",
            "cycle part set y_cycle to 1 default 0", dialect='oracle')

[＃3220 T0\>](http://www.sqlalchemy.org/trac/ticket/3220)

### DDL 的新 Oracle 关键字[¶](#new-oracle-keywords-for-ddl "Permalink to this headline")

关键字如COMPRESS，ON COMMIT，BITMAP：

[Oracle Table Options](dialects_oracle.html#oracle-table-options)

[Oracle Specific Index
Options](dialects_oracle.html#oracle-index-options)
