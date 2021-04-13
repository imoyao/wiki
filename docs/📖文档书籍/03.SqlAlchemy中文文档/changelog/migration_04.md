---
title: migration_04
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/a5cdb7/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
  - 
---
SQLAlchemy 0.4 有哪些新特性？[¶](#what-s-new-in-sqlalchemy-0-4 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍了 2008 年 10 月 14 日发布的 SQLAlchemy
0.3 版和 2007 年 10 月 12 日发布的 SQLAlchemy 0.4 版之间的变化。

文件日期：2008 年 3 月 21 日

第一件事第一件[¶](#first-things-first "Permalink to this headline")
-------------------------------------------------------------------

如果您使用任何 ORM 功能，请确保从`sqlalchemy.orm`导入：

    from sqlalchemy import *plain
    from sqlalchemy.orm import *

Secondly, anywhere you used to say `engine=`,
`connectable=`, `bind_to=`,
`something.engine`, `metadata.connect()`, use `bind`:

    myengine = create_engine('sqlite://')

    meta = MetaData(myengine)

    meta2 = MetaData()
    meta2.bind = myengine

    session = create_session(bind=myengine)

    statement = select([table], bind=myengine)

有这些？好！你现在（95％）0.4 兼容。如果您使用 0.3.10，则可以立即进行这些更改；他们也会在那里工作。

模块导入[¶](#module-imports "Permalink to this headline")
---------------------------------------------------------

In 0.3, “`from sqlachemy import *`” would import all
of sqlachemy’s sub-modules into your namespace.
版本 0.4 不再将子模块导入名称空间。这可能意味着您需要在代码中添加额外的导入。

在 0.3 中，此代码起作用：

    from sqlalchemy import *plainplain

    class UTCDateTime(types.TypeDecorator):
        pass

在 0.4 中，必须这样做：

    from sqlalchemy import *plain
    from sqlalchemy import types

    class UTCDateTime(types.TypeDecorator):
        pass

对象关系映射[¶](#object-relational-mapping "Permalink to this headline")
------------------------------------------------------------------------

### 查询[¶ T0\>](#querying "Permalink to this headline")

#### 新的查询 API [¶](#new-query-api "Permalink to this headline")

查询在生成界面上是标准化的（旧界面仍然存在，仅此而已）。虽然大多数生成接口的可用性为 0.3，但 0.4
Query 具有与外部生成匹配的内在胆量，并且有更多技巧。所有结果缩小都通过`filter()`和`filter_by()`，限制/偏移可以通过数组切片或`limit()` /
`offset()`，加入是通过`join()`和`outerjoin()`（或者更手动地通过`select_from()`作为手动形成的标准）。

为避免弃用警告，您必须对您的 03 代码进行一些更改

User.query.get\_by（\*\* kwargs）

    User.query.filter_by(**kwargs).first()plainplain

User.query.select\_by（\*\* kwargs）

    User.query.filter_by(**kwargs).all()plainplainplainplainplain

User.query.select()

    User.query.filter(xxx).all()plainplain

#### 新的基于属性的表达式构造[¶](#new-property-based-expression-constructs "Permalink to this headline")

到目前为止，ORM 中最明显的差异是，您现在可以直接使用基于类的属性构建查询条件。使用映射类时，不再需要“.c。”前缀：

    session.query(User).filter(and_(User.name == 'fred', User.id > 17))plainplainplain

尽管简单的基于列的比较没有什么大不了，但类属性有一些新的“更高级别”结构可用，包括以前仅在`filter_by()`中可用的结构：

    # comparison of scalar relations to an instanceplain
    filter(Address.user == user)

    # return all users who contain a particular address
    filter(User.addresses.contains(address))

    # return all users who *dont* contain the address
    filter(~User.address.contains(address))

    # return all users who contain a particular address with
    # the email_address like '%foo%'
    filter(User.addresses.any(Address.email_address.like('%foo%')))

    # same, email address equals 'foo@bar.com'.  can fall back to keyword
    # args for simple comparisons
    filter(User.addresses.any(email_address = 'foo@bar.com'))

    # return all Addresses whose user attribute has the username 'ed'
    filter(Address.user.has(name='ed'))

    # return all Addresses whose user attribute has the username 'ed'
    # and an id > 5 (mixing clauses with kwargs)
    filter(Address.user.has(User.id > 5, name='ed'))

`Column`集合在`.c`属性中的映射类上仍然可用。请注意，基于属性的表达式仅适用于映射类的映射属性。`.c`仍然用于访问常规表中的列和 SQL 表达式生成的可选对象。

#### 自动连接别名[¶](#automatic-join-aliasing "Permalink to this headline")

我们现在有一段时间 join()和 outerjoin()：

    session.query(Order).join('items')...plain

现在你可以别名了：

    session.query(Order).join('items', aliased=True).plain
       filter(Item.name='item 1').join('items', aliased=True).filter(Item.name=='item 3')

以上将使用别名从订单 -
\>项目创建两个连接。每个后面的`filter()`调用都会将其表格标准调整为别名标准。要获取`Item`对象，请使用`add_entity()`并使用`id`定位每个连接：

    session.query(Order).join('items', id='j1', aliased=True).
    filter(Item.name == 'item 1').join('items', aliased=True, id='j2').
    filter(Item.name == 'item 3').add_entity(Item, id='j1').add_entity(Item, id='j2')

以下面的形式返回元组：`（Order， Item， Item）`。

#### 自我引用查询[¶](#self-referential-queries "Permalink to this headline")

所以 query.join()现在可以生成别名。这给了我们什么？自引用查询！连接可以在没有任何`Alias`对象的情况下完成：

    # standard self-referential TreeNode mapper with backrefplainplainplain
    mapper(TreeNode, tree_nodes, properties={
        'children':relation(TreeNode, backref=backref('parent', remote_side=tree_nodes.id))
    })

    # query for node with child containing "bar" two levels deep
    session.query(TreeNode).join(["children", "children"], aliased=True).filter_by(name='bar')

要为别名中的每个表添加条件标准，可以使用`from_joinpoint`继续加入同一行别名：

    # search for the treenode along the path "n1/n12/n122"plainplain

    # first find a Node with name="n122"
    q = sess.query(Node).filter_by(name='n122')

    # then join to parent with "n12"
    q = q.join('parent', aliased=True).filter_by(name='n12')

    # join again to the next parent with 'n1'.  use 'from_joinpoint'
    # so we join from the previous point, instead of joining off the
    # root table
    q = q.join('parent', aliased=True, from_joinpoint=True).filter_by(name='n1')

    node = q.first()

#### `query.populate_existing()`[¶](#query-populate-existing "Permalink to this headline")

`query.load()`（或`session.refresh()`）的热切版本。如果已经存在于会话中，则从查询加载的每个实例（包括所有急切加载的项目）都会立即刷新：

    session.query(Blah).populate_existing().all()plainplain

### 关系[¶ T0\>](#relations "Permalink to this headline")

#### 嵌入到更新/插入中的 SQL 子句[¶](#sql-clauses-embedded-in-updates-inserts "Permalink to this headline")

对于在`flush()`期间嵌入式执行 SQL 子句，直接嵌入 UPDATE 或 INSERT 中：

    myobject.foo = mytable.c.value + 1

    user.pwhash = func.md5(password)

    order.hash = text("select hash from hashing_table")

在操作之后，使用延迟加载器设置 column-attribute，以便在下次访问时发出 SQL 以加载新值。

#### 自引用和周期性快速加载[¶](#self-referential-and-cyclical-eager-loading "Permalink to this headline")

由于我们的 alias-fu 已经改进，所以`relation()`可以沿同一个表加入\*任意次数\*；你告诉它你想走多深。让我们更清楚地显示自引用的`TreeNode`：

    nodes = Table('nodes', metadata,plain
         Column('id', Integer, primary_key=True),
         Column('parent_id', Integer, ForeignKey('nodes.id')),
         Column('name', String(30)))

    class TreeNode(object):
        pass

    mapper(TreeNode, nodes, properties={
        'children':relation(TreeNode, lazy=False, join_depth=3)
    })

那么当我们说：

    create_session().query(TreeNode).all()

? 沿着别名进行连接，从父母那里深入三级：

    SELECTplain
    nodes_3.id AS nodes_3_id, nodes_3.parent_id AS nodes_3_parent_id, nodes_3.name AS nodes_3_name,
    nodes_2.id AS nodes_2_id, nodes_2.parent_id AS nodes_2_parent_id, nodes_2.name AS nodes_2_name,
    nodes_1.id AS nodes_1_id, nodes_1.parent_id AS nodes_1_parent_id, nodes_1.name AS nodes_1_name,
    nodes.id AS nodes_id, nodes.parent_id AS nodes_parent_id, nodes.name AS nodes_name
    FROM nodes LEFT OUTER JOIN nodes AS nodes_1 ON nodes.id = nodes_1.parent_id
    LEFT OUTER JOIN nodes AS nodes_2 ON nodes_1.id = nodes_2.parent_id
    LEFT OUTER JOIN nodes AS nodes_3 ON nodes_2.id = nodes_3.parent_id
    ORDER BY nodes.oid, nodes_1.oid, nodes_2.oid, nodes_3.oid

注意干净的别名。加入并不关心它是否违背同一个直接表或其他对象，然后循环回到开始。当指定`join_depth`时，任何类型的热切加载链都可以循环回自身。当不存在时，急切加载在碰到一个循环时自动停止。

#### 复合类型[¶](#composite-types "Permalink to this headline")

这是 Hibernate 阵营的一员。复合类型允许您定义一个由多个列（或者一列，如果需要）组成的自定义数据类型。让我们定义一个新的类型，`Point`。存储 x / y 坐标：

    class Point(object):plain
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __composite_values__(self):
            return self.x, self.y
        def __eq__(self, other):
            return other.x == self.x and other.y == self.y
        def __ne__(self, other):
            return not self.__eq__(other)

定义`Point`对象的方式特定于自定义类型；构造函数接受一个参数列表，并且`__composite_values__()`方法产生这些参数的序列。顺序将与我们的映射器相匹配，我们稍后会看到。

我们来创建一个顶点表，每行存储两个点：

    vertices = Table('vertices', metadata,
        Column('id', Integer, primary_key=True),
        Column('x1', Integer),
        Column('y1', Integer),
        Column('x2', Integer),
        Column('y2', Integer),
        )

然后，映射它！我们将创建一个存储两个`Point`对象的`Vertex`对象：

    class Vertex(object):plain
        def __init__(self, start, end):
            self.start = start
            self.end = end

    mapper(Vertex, vertices, properties={
        'start':composite(Point, vertices.c.x1, vertices.c.y1),
        'end':composite(Point, vertices.c.x2, vertices.c.y2)
    })

一旦你设置了你的复合类型，它就像其他任何类型一样可用：

    v = Vertex(Point(3, 4), Point(26,15))plain
    session.save(v)
    session.flush()

    # works in queries too
    q = session.query(Vertex).filter(Vertex.start == Point(3, 4))

如果您想定义映射属性在表达式中使用时生成 SQL 子句的方式，请创建您自己的`sqlalchemy.orm.PropComparator`子类，定义任何常用运算符（如`__eq__()`，`__le__()`等），并将它发送到`composite()`。复合类型也可以作为主键，并可用于`query.get()`中：

    # a Document class which uses a composite Versionplainplain
    # object as primary key
    document = query.get(Version(1, 'a'))

#### `dynamic_loader()`关系[¶](#dynamic-loader-relations "Permalink to this headline")

一个`relation()`，它为所有读取操作返回一个实时`Query`对象。写操作仅限于`append()`和`remove()`，集合的更改在刷新会话之前不可见。此功能特别适用于在每次查询之前刷新的“自动刷新”会话。

    mapper(Foo, foo_table, properties={plain
        'bars':dynamic_loader(Bar, backref='foo', <other relation() opts>)
    })

    session = create_session(autoflush=True)
    foo = session.query(Foo).first()

    foo.bars.append(Bar(name='lala'))

    for bar in foo.bars.filter(Bar.name=='lala'):
        print(bar)

    session.commit()

#### 新选项：`undefer_group()`，`eagerload_all()` [¶](#new-options-undefer-group-eagerload-all "Permalink to this headline")

一些方便的查询选项。`undefer_group()`将一组“延迟”列标记为 undeferred：

    mapper(Class, table, properties={plainplainplainplainplainplain
        'foo' : deferred(table.c.foo, group='group1'),
        'bar' : deferred(table.c.bar, group='group1'),
        'bat' : deferred(table.c.bat, group='group1'),
    )

    session.query(Class).options(undefer_group('group1')).filter(...).all()

和`eagerload_all()`设置一个属性链，以便在一次传递中保持渴望：

    mapper(Foo, foo_table, properties={plainplain
       'bar':relation(Bar)
    })
    mapper(Bar, bar_table, properties={
       'bat':relation(Bat)
    })
    mapper(Bat, bat_table)

    # eager load bar and bat
    session.query(Foo).options(eagerload_all('bar.bat')).filter(...).all()

#### 新集合 API [¶](#new-collection-api "Permalink to this headline")

集合不再由 InstrumentedList 代理代理，并且对成员，方法和属性的访问是直接的。装饰者现在拦截进入和离开集合的对象，现在可以轻松地编写管理自己的成员资格的自定义集合类。灵活的装饰器也可以替换 0.3 中定制集合的命名方法接口，从而使任何类都可以很容易地作为集合容器使用。

基于字典的集合现在更容易使用，并且完全像`dict`一样。Changing `__iter__` is no longer
needed for `dict``s, and new built-in ``dict`
types cover many needs:

    # use a dictionary relation keyed by a columnplainplainplain
    relation(Item, collection_class=column_mapped_collection(items.c.keyword))
    # or named attribute
    relation(Item, collection_class=attribute_mapped_collection('keyword'))
    # or any function you like
    relation(Item, collection_class=mapped_collection(lambda entity: entity.a + entity.b))

需要为新 API 更新现有的 0.3 `dict`样和自由格式的对象派生集合类。在大多数情况下，这只是将一些装饰器添加到类定义中的问题。

#### 从外部表/子查询映射关系[¶](#mapped-relations-from-external-tables-subqueries "Permalink to this headline")

这个特性静静地出现在 0.3 中，但在 0.4 下得到了改进，这要归功于能够将子查询转换为表的子查询转换为针对该表的别名的子查询。这对于急切加载，查询中的别名加入等是关键的。当您只需要添加一些额外的列或子查询时，它可以减少对 select 语句创建映射器的需要：

    mapper(User, users, properties={plainplain
           'fullname': column_property((users.c.firstname + users.c.lastname).label('fullname')),
           'numposts': column_property(
                select([func.count(1)], users.c.id==posts.c.user_id).correlate(users).label('posts')
           )
        })

一个典型的查询如下所示：

    SELECT (SELECT count(1) FROM posts WHERE users.id = posts.user_id) AS count,plainplainplain
    users.firstname || users.lastname AS fullname,
    users.id AS users_id, users.firstname AS users_firstname, users.lastname AS users_lastname
    FROM users ORDER BY users.oid

### 水平缩放（分片）API [¶](#horizontal-scaling-sharding-api "Permalink to this headline")

[browser：/ sqlalchemy / trunk / examples / sharding / attribute\_shard
.py]

### 会话[¶ T0\>](#sessions "Permalink to this headline")

#### 新会话创建范式； SessionContext，assignmapper 已弃用[¶](#new-session-create-paradigm-sessioncontext-assignmapper-deprecated "Permalink to this headline")

没错，整个 shebang 被两个配置函数取代。使用它们将产生自 0.1 以来我们已经具有的最多 0.1sh 的感觉（即，最少量的打字）。

在您定义`engine`（或任何地方）的位置配置您自己的`Session`类：

    from sqlalchemy import create_engineplainplain
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('myengine://')
    Session = sessionmaker(bind=engine, autoflush=True, transactional=True)

    # use the new Session() freely
    sess = Session()
    sess.save(someobject)
    sess.flush()

如果您需要后期配置会话，请使用引擎进行配置，稍后使用`configure()`添加它：

    Session.configure(bind=create_engine(...))plainplainplainplainplain

All the behaviors of `SessionContext` and the
`query` and `__init__` methods
of `assignmapper` are moved into the new
`scoped_session()` function, which is compatible
with both `sessionmaker` as well as
`create_session()`:

    from sqlalchemy.orm import scoped_session, sessionmakerplainplainplainplain

    Session = scoped_session(sessionmaker(autoflush=True, transactional=True))
    Session.configure(bind=engine)

    u = User(name='wendy')

    sess = Session()
    sess.save(u)
    sess.commit()

    # Session constructor is thread-locally scoped.  Everyone gets the same
    # Session in the thread when scope="thread".
    sess2 = Session()
    assert sess is sess2

当使用线程本地的`Session`时，返回的类将所有`Session's`接口实现为 classmethods，并且“assignmapper”的功能可以使用`mapper`就像旧的`objectstore`天……

    # "assignmapper"-like functionality available via ScopedSession.mapperplain
    Session.mapper(User, users_table)

    u = User(name='wendy')

    Session.commit()

#### 会话再次默认为弱引用[¶](#sessions-are-again-weak-referencing-by-default "Permalink to this headline")

默认情况下，Session 中的 weak\_identity\_map 标志现在设置为`True`。自动从会话中删除外部推断和超出范围的实例。但是，存在“脏”变化的项目将保持强引用状态，直到这些变化被刷新为止，此时对象将恢复为弱引用（这对'可变'类型也适用，如可选属性）。将 weak\_identity\_map 设置为`False`为使用会话的用户恢复旧的强引用行为，如缓存。

#### 自动事务会话[¶](#auto-transactional-sessions "Permalink to this headline")

正如您可能已经注意到的那样，我们正在`Session`上调用`commit()`。标志`transactional=True`表示`Session`总是在事务中，`commit()`永久保存。

#### 自动刷新会话[¶](#auto-flushing-sessions "Permalink to this headline")

Also, `autoflush=True` means the `Session` will `flush()` before each
`query` as well as when you call `flush()` or `commit()`. 所以现在这将工作：

    Session = sessionmaker(bind=engine, autoflush=True, transactional=True)plainplainplainplain

    u = User(name='wendy')

    sess = Session()
    sess.save(u)

    # wendy is flushed, comes right back from a query
    wendy = sess.query(User).filter_by(name='wendy').one()

#### 事务方法已移至会话[¶](#transactional-methods-moved-onto-sessions "Permalink to this headline")

`commit()`和`rollback()`，以及`begin()`现在直接在`Session`上。不需要为任何事情使用`SessionTransaction`（它仍然在后台）。

    Session = sessionmaker(autoflush=True, transactional=False)plainplainplain

    sess = Session()
    sess.begin()

    # use the session

    sess.commit() # commit transaction

与封闭的引擎级别（即非 ORM）事务共享`Session`非常简单：

    Session = sessionmaker(autoflush=True, transactional=False)plain

    conn = engine.connect()
    trans = conn.begin()
    sess = Session(bind=conn)

    # ... session is transactional

    # commit the outermost transaction
    trans.commit()

#### 使用 SAVEPOINT [¶](#nested-session-transactions-with-savepoint "Permalink to this headline")嵌套会话事务

在引擎和 ORM 级别可用。ORM 文档到目前为止：

[http://www.sqlalchemy.org/docs/04/session.html\#unitofwork\_ma](http://www.sqlalchemy.org/docs/04/session.html#unitofwork_ma)
naging

#### 两阶段提交会话[¶](#two-phase-commit-sessions "Permalink to this headline")

在引擎和 ORM 级别可用。ORM 文档到目前为止：

[http://www.sqlalchemy.org/docs/04/session.html\#unitofwork\_ma](http://www.sqlalchemy.org/docs/04/session.html#unitofwork_ma)
naging

### 继承[¶ T0\>](#inheritance "Permalink to this headline")

#### 无连接或联合的多态继承[¶](#polymorphic-inheritance-with-no-joins-or-unions "Permalink to this headline")

新的继承文档：[http://www.sqlalchemy.org/docs/04](http://www.sqlalchemy.org/docs/04)
/mappers.html\#advdatamapping\_mapper\_inheritance\_joined

#### 使用`get()` [¶](#better-polymorphic-behavior-with-get "Permalink to this headline")更好地进行多态行为

连接表继承层次结构中的所有类都使用基类获取`_instance_key`，即`（BaseClass， （1， ）， 无）`。通过这种方式，当您针对基类调用`get()` a
`Query`时，可以在当前标识映射中查找子类实例，而无需查询数据库。

### 类型[¶ T0\>](#types "Permalink to this headline")

#### `sqlalchemy.types.TypeDecorator` [¶](#custom-subclasses-of-sqlalchemy-types-typedecorator "Permalink to this headline")

有一个用于子类化 TypeDecorator 的[新 API](http://www.sqlalchemy.org/docs/04/types.html#types_custom)。在某些情况下使用 0.3
API 会导致编译错误。

SQL 表达式[¶](#sql-expressions "Permalink to this headline")
-----------------------------------------------------------

### 全新，确定性标签/别名生成[¶](#all-new-deterministic-label-alias-generation "Permalink to this headline")

所有“匿名”标签和别名现在都使用简单的\_ 格式。 T1\>
T0\>SQL 更容易阅读，并与计划优化器缓存兼容。请查看教程中的一些示例：[http://www.sqlalchemy.org/docs/04/ormtutorial.html](http://www.sqlalchemy.org/docs/04/ormtutorial.html)
[http://www.sqlalchemy.org/docs/ 04 / sqlexpression.html
T1\>](http://www.sqlalchemy.org/docs/04/sqlexpression.html)

### 生成 select()构造[¶](#generative-select-constructs "Permalink to this headline")

这绝对是通过`select()`进行的。请参阅 htt
p：//www.sqlalchemy.org/docs/04/sqlexpression.html\#sql\_transf orm。

### 新的操作员系统[¶](#new-operator-system "Permalink to this headline")

SQL 运算符和或多或少每个 SQL 关键字都被抽象到编译器层。他们现在可以智能地操作，并且可以识别类型/后端，请参阅：[http：//www.sq](http://www.sq)
lalchemy.org/docs/04/sqlexpression.html\#sql\_operators

### 所有`type`关键字参数重命名为`type_` [¶](#all-type-keyword-arguments-renamed-to-type "Permalink to this headline")

就像它说的那样：

    b = bindparam('foo', type_=String)plain

### in\_函数更改为接受序列或可选[¶](#in-function-changed-to-accept-sequence-or-selectable "Permalink to this headline")

in\_函数现在将一系列值或可选值作为其唯一参数。以前传入值作为位置参数的 API 仍然有效，但现在已被弃用。这意味着

    my_table.select(my_table.c.id.in_(1,2,3)plain
    my_table.select(my_table.c.id.in_(*listOfIds)

应改为

    my_table.select(my_table.c.id.in_([1,2,3])plainplain
    my_table.select(my_table.c.id.in_(listOfIds)

架构和反思[¶](#schema-and-reflection "Permalink to this headline")
------------------------------------------------------------------

### `MetaData`, `BoundMetaData`, `DynamicMetaData`...[¶](#metadata-boundmetadata-dynamicmetadata "Permalink to this headline")

在 0.3.x 系列中，不赞成使用`MetaData`和`ThreadLocalMetaData`的`BoundMetaData`和`DynamicMetaData`。0.4 的旧名称已被删除。更新很简单：

    +-------------------------------------+-------------------------+plain
    |If You Had                           | Now Use                 |
    +=====================================+=========================+
    | ``MetaData``                        | ``MetaData``            |
    +-------------------------------------+-------------------------+
    | ``BoundMetaData``                   | ``MetaData``            |
    +-------------------------------------+-------------------------+
    | ``DynamicMetaData`` (with one       | ``MetaData``            |
    | engine or threadlocal=False)        |                         |
    +-------------------------------------+-------------------------+
    | ``DynamicMetaData``                 | ``ThreadLocalMetaData`` |
    | (with different engines per thread) |                         |
    +-------------------------------------+-------------------------+

`MetaData`类型的很少使用的`name`参数已被删除。`ThreadLocalMetaData`构造函数现在不带任何参数。现在这两种类型都可以绑定到`Engine`或单个`Connection`。

### 一步多表反射[¶](#one-step-multi-table-reflection "Permalink to this headline")

您现在可以加载表定义，并通过一次传递从整个数据库或模式自动创建`Table`对象：

    >>> metadata = MetaData(myengine, reflect=True)plain
    >>> metadata.tables.keys()
    ['table_a', 'table_b', 'table_c', '...']

`MetaData` also gains a `.reflect()` method enabling finer control over the loading process,
including specification of a subset of available tables to load.

SQL 执行[¶](#sql-execution "Permalink to this headline")
-------------------------------------------------------

### `engine`, `connectable`, and `bind_to` are all now `bind`[¶](#engine-connectable-and-bind-to-are-all-now-bind "Permalink to this headline")

### `Transactions`，`NestedTransactions`和`TwoPhaseTransactions` [¶](#transactions-nestedtransactions-and-twophasetransactions "Permalink to this headline")

### 连接池事件[¶](#connection-pool-events "Permalink to this headline")

连接池现在会在创建新的 DB-API 连接时触发事件，检出并检入池中。例如，您可以使用它们在新连接上执行会话范围的 SQL 安装语句。

### Oracle 引擎已修复[¶](#oracle-engine-fixed "Permalink to this headline")

在 0.3.11 中，Oracle 引擎中存在关于如何处理主键的错误。这些错误可能会导致在其他引擎（如 sqlite）中正常工作的程序在使用 Oracle 引擎时失败。在 0.4 版本中，Oracle 引擎已经过修改，修复了这些主键问题。

### Oracle 的输出参数[¶](#out-parameters-for-oracle "Permalink to this headline")

    result = engine.execute(text("begin foo(:x, :y, :z); end;", bindparams=[bindparam('x', Numeric), outparam('y', Numeric), outparam('z', Numeric)]), x=5)plainplainplain
    assert result.out_parameters == {'y':10, 'z':75}

### 连接绑定`MetaData`，`Sessions` [¶](#connection-bound-metadata-sessions "Permalink to this headline")

`MetaData` and `Session` can be
explicitly bound to a connection:

    conn = engine.connect()plainplain
    sess = create_session(bind=conn)

### 更快，更安全`ResultProxy`对象[¶](#faster-more-foolproof-resultproxy-objects "Permalink to this headline")
