---
title: 关系加载技术
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/loading_relationships/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
关系加载技术[¶](#relationship-loading-techniques "Permalink to this headline")
==============================================================================

SQLAlchemy 的很大一部分是对查询中相关对象加载的方式提供了广泛的控制。这个行为可以在映射器构造时使用[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")函数的`lazy`参数进行配置，也可以使用[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")目的。

使用 Loader 策略：延迟加载，预先加载[¶](#using-loader-strategies-lazy-loading-eager-loading "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------

默认情况下，所有的对象间关系都是**延迟加载**。与[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")关联的标量或集合属性包含一个触发器，该属性首次被访问时触发。除了一种情况外，该触发器在访问点发出 SQL 调用以加载相关对象或对象：

    sql>>> jack.addressesplain
    SELECT addresses.id AS addresses_id, addresses.email_address AS addresses_email_address,
    addresses.user_id AS addresses_user_id
    FROM addresses
    WHERE ? = addresses.user_id
    [5]
    [<Address(u'jack@google.com')>, <Address(u'j25@yahoo.com')>]

在没有发出 SQL 的情况下，对于简单的多对一关系，只能通过其主键标识相关对象，并且该对象已存在于当前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中。

“load upon attribute access”的默认行为称为“lazy”或“select”加载 -
名称“select”，因为通常在首次访问属性时会发出“SELECT”语句。

在[Object Relational Tutorial](tutorial.html)中，我们引入了**Eager
Loading**的概念。我们将`option`与[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象结合使用，以表示在单个 SQL 查询中应该与父对象同时加载关系。这个被称为[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")的选项将一个 JOIN（缺省为 LEFT
OUTER join）连接到该语句，并从与父类相同的结果集中填充标量/集合：

    sql>>> jack = session.query(User).\
    ... options(joinedload('addresses')).\
    ... filter_by(name='jack').all() #doctest: +NORMALIZE_WHITESPACE
    SELECT addresses_1.id AS addresses_1_id, addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id, users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname, users.password AS users_password
    FROM users LEFT OUTER JOIN addresses AS addresses_1 ON users.id = addresses_1.user_id
    WHERE users.name = ?
    ['jack']

除了“加入急切加载”之外，还有第二种急切加载选项，称为“子查询加载”。这种热切的加载为请求的每个集合都发出额外的 SQL 语句，并聚合到所有父对象中：

    sql>>> jack = session.query(User).\plain
    ... options(subqueryload('addresses')).\
    ... filter_by(name='jack').all()
    SELECT users.id AS users_id, users.name AS users_name, users.fullname AS users_fullname,
    users.password AS users_password
    FROM users
    WHERE users.name = ?
    ('jack',)
    SELECT addresses.id AS addresses_id, addresses.email_address AS addresses_email_address,
    addresses.user_id AS addresses_user_id, anon_1.users_id AS anon_1_users_id
    FROM (SELECT users.id AS users_id
    FROM users
    WHERE users.name = ?) AS anon_1 JOIN addresses ON anon_1.users_id = addresses.user_id
    ORDER BY anon_1.users_id, addresses.id
    ('jack',)

任何[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的默认**加载器策略**由`lazy`关键字参数配置，该参数默认为`select`这表示一个“选择”语句。下面我们将它设置为`joined`，以便使用 JOIN 加载`children`关系：

    # load the 'children' collection using LEFT OUTER JOIN
    class Parent(Base):
        __tablename__ = 'parent'

        id = Column(Integer, primary_key=True)
        children = relationship("Child", lazy='joined')

我们还可以使用`subquery`将其设置为对所有集合使用第二个查询进行热切加载：

    # load the 'children' collection using a second query which
    # JOINS to a subquery of the original
    class Parent(Base):
        __tablename__ = 'parent'

        id = Column(Integer, primary_key=True)
        children = relationship("Child", lazy='subquery')

查询时，使用[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")，[`subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")和[`lazyload()`](#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")

    # set children to load lazily
    session.query(Parent).options(lazyload('children')).all()

    # set children to load eagerly with a join
    session.query(Parent).options(joinedload('children')).all()

    # set children to load eagerly with a second statement
    session.query(Parent).options(subqueryload('children')).all()

订购的重要性[¶](#the-importance-of-ordering "Permalink to this headline")
-------------------------------------------------------------------------

A query which makes use of [`subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")
in conjunction with a limiting modifier such as [`Query.first()`](query.html#sqlalchemy.orm.query.Query.first "sqlalchemy.orm.query.Query.first"),
[`Query.limit()`](query.html#sqlalchemy.orm.query.Query.limit "sqlalchemy.orm.query.Query.limit"),
or [`Query.offset()`](query.html#sqlalchemy.orm.query.Query.offset "sqlalchemy.orm.query.Query.offset")
should **always** include [`Query.order_by()`](query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")
against unique column(s) such as the primary key, so that the additional
queries emitted by [`subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")
include the same ordering as used by the parent query.
没有它，内部查询可能会返回错误的行：

    # incorrect, no ORDER BYplain
    session.query(User).options(subqueryload(User.addresses)).first()

    # incorrect if User.name is not unique
    session.query(User).options(subqueryload(User.addresses)).order_by(User.name).first()

    # correct
    session.query(User).options(subqueryload(User.addresses)).order_by(User.name, User.id).first()

也可以看看

[Why is ORDER BY required with LIMIT (especially with
subqueryload())?](faq_ormconfiguration.html#faq-subqueryload-limit-sort)
- 详细的例子

沿路径加载[¶](#loading-along-paths "Permalink to this headline")
----------------------------------------------------------------

要引用比一个层次更深的关系，可以使用方法链接。所有加载器选项返回的对象是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")类的一个实例，它提供了一个所谓的“生成”接口：

    session.query(Parent).options(
                                joinedload('foo').
                                    joinedload('bar').
                                    joinedload('bat')
                                ).all()

使用方法链接，明确声明路径中每个链接的装入程序样式。要沿路径导航而不改变特定属性的现有装入程序样式，可以使用[`defaultload()`](#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")方法/函数：

    session.query(A).options(
                        defaultload("atob").joinedload("btoc")
                    ).all()

在版本 0.9.0 中进行了更改：之前在加载器选项中指定点分隔路径的方法已被[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")对象和相关方法的模糊方法所取代。使用这个系统，用户明确指定链中每个链接的加载样式，而不是在诸如`joinedload()`和`joinedload_all()`之类的选项之间进行猜测。提供[`orm.defaultload()`](#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")以允许在不修改现有加载程序选项的情况下进行路径导航。点分离路径系统以及`_all()`函数将无限期地保持向后兼容。

默认加载策略[¶](#default-loading-strategies "Permalink to this headline")
-------------------------------------------------------------------------

New in version 0.7.5: Default loader strategies as a new feature.

Each of [`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload"),
[`subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload"),
[`lazyload()`](#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload"),
[`noload()`](#sqlalchemy.orm.noload "sqlalchemy.orm.noload"), and
[`raiseload()`](#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload") can be
used to set the default style of [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
loading for a particular query, affecting all [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
-mapped attributes not otherwise specified in the [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query").
通过将字符串`'*'`作为参数传递给以下任何选项，可以使用此功能：

    session.query(MyClass).options(lazyload('*'))

在上面，`lazyload('*')`选项将取代用于该查询的所有[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构的`lazy`设置，那些使用`'dynamic'`风格的加载。例如，如果某些关系指定了`lazy='joined'`或`lazy='subquery'`，则使用`lazyload('*')`所有这些关系使用`'select'`加载，例如在访问每个属性时发出一条 SELECT 语句。

该选项不会取代查询中声明的加载器选项，如[`eagerload()`](#sqlalchemy.orm.eagerload "sqlalchemy.orm.eagerload")，[`subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")等。下面的查询仍将使用`widget`关系的连接加载：

    session.query(MyClass).options(
                                lazyload('*'),
                                joinedload(MyClass.widget)
                            )

如果传递多个`'*'`选项，则最后一个覆盖先前传递的选项。

每个实体的默认加载策略[¶](#per-entity-default-loading-strategies "Permalink to this headline")
----------------------------------------------------------------------------------------------

版本 0.9.0 中的新功能：每个实体的默认加载器策略。

默认加载器策略的一个变体是能够以每个实体为基础设置策略。例如，如果查询`User`和`Address`，我们可以指示`Address`上的所有关系仅使用延迟加载，方法是首先应用[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")对象，然后将`*`指定为链接选项：

    session.query(User, Address).options(Load(Address).lazyload('*'))

以上，`Address`上的所有关系都将设置为延迟加载。

渴望的载入中的载入[¶](#the-zen-of-eager-loading "Permalink to this headline")
-----------------------------------------------------------------------------

The philosophy behind loader strategies is that any set of loading
schemes can be applied to a particular query, and *the results don’t
change* - only the number of SQL statements required to fully load
related objects and collections changes.
一个特定的查询可能会开始使用所有延迟加载。在上下文中使用它之后，可能会发现总是访问特定的属性或集合，并且更改这些的加载器策略会更有效。该策略可以在没有对查询进行其他修改的情况下进行更改，结果将保持不变，但会发出更少的 SQL 语句。在理论上（并且在实践中），对于[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")可以做的任何事情都不会让它根据加载器策略的变化加载一组不同的主要或相关对象。

特别是[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")如何实现不影响以任何方式返回的实体行的结果是它创建了它添加到查询中的连接的匿名别名，以便它们不能被引用查询的其他部分。For
example, the query below uses [`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload") to
create a LEFT OUTER JOIN from `users` to
`addresses`, however the `ORDER BY` added against `Address.email_address` is
not valid - the `Address` entity is not named in the
query:

    >>> jack = session.query(User).\
    ... options(joinedload(User.addresses)).\
    ... filter(User.name=='jack').\
    ... order_by(Address.email_address).all()
    SELECT addresses_1.id AS addresses_1_id, addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id, users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname, users.password AS users_password
    FROM users LEFT OUTER JOIN addresses AS addresses_1 ON users.id = addresses_1.user_id
    WHERE users.name = ? ORDER BY addresses.email_address   <-- this part is wrong !
    ['jack']

Above, `ORDER BY addresses.email_address` is not
valid since `addresses` is not in the FROM list.
加载`User`通过电子邮件地址记录和订购的正确方法是使用[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")：

    >>> jack = session.query(User).\
    ... join(User.addresses).\
    ... filter(User.name=='jack').\
    ... order_by(Address.email_address).all()

    SELECT users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname, users.password AS users_password
    FROM users JOIN addresses ON users.id = addresses.user_id
    WHERE users.name = ? ORDER BY addresses.email_address
    ['jack']

上述声明当然与前一个声明不同，因为`addresses`中的列根本不包含在结果中。我们可以添加[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")，以便有两个连接
- 一个是我们要订购的，另一个是匿名使用来加载`User.addresses`

    >>> jack = session.query(User).\
    ... join(User.addresses).\
    ... options(joinedload(User.addresses)).\
    ... filter(User.name=='jack').\
    ... order_by(Address.email_address).all()
    SELECT addresses_1.id AS addresses_1_id, addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id, users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname, users.password AS users_password
    FROM users JOIN addresses ON users.id = addresses.user_id
    LEFT OUTER JOIN addresses AS addresses_1 ON users.id = addresses_1.user_id
    WHERE users.name = ? ORDER BY addresses.email_address
    ['jack']

What we see above is that our usage of [`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
is to supply JOIN clauses we’d like to use in subsequent query
criterion, whereas our usage of [`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload") only
concerns itself with the loading of the `User.addresses` collection, for each `User` in the result.
在这种情况下，这两个连接可能看起来多余 - 它们是多少。If we wanted to use
just one JOIN for collection loading as well as ordering, we use the
[`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")
option, described in [Routing Explicit Joins/Statements into Eagerly
Loaded Collections](#contains-eager) below. But to see why
[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload") does
what it does, consider if we were **filtering** on a particular
`Address`:

    >>> jack = session.query(User).\
    ... join(User.addresses).\
    ... options(joinedload(User.addresses)).\
    ... filter(User.name=='jack').\
    ... filter(Address.email_address=='someaddress@foo.com').\
    ... all()
    SELECT addresses_1.id AS addresses_1_id, addresses_1.email_address AS addresses_1_email_address,
    addresses_1.user_id AS addresses_1_user_id, users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname, users.password AS users_password
    FROM users JOIN addresses ON users.id = addresses.user_id
    LEFT OUTER JOIN addresses AS addresses_1 ON users.id = addresses_1.user_id
    WHERE users.name = ? AND addresses.email_address = ?
    ['jack', 'someaddress@foo.com']

在上面，我们可以看到两个 JOIN 具有非常不同的角色。一个将匹配`User`和`Address`的其中一个行，即`Address.email_address=='someaddress@foo.com'`的连接。The other LEFT OUTER JOIN will match *all*
`Address` rows related to `User`, and is only used to populate the `User.addresses` collection, for those `User` objects that
are returned.

通过将[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")的使用更改为另一种加载类型，我们可以更改集合的加载方式，完全独立于用于检索我们想要的实际`User`行的 SQL。下面我们将[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")改成[`subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")：

    >>> jack = session.query(User).\
    ... join(User.addresses).\
    ... options(subqueryload(User.addresses)).\
    ... filter(User.name=='jack').\
    ... filter(Address.email_address=='someaddress@foo.com').\
    ... all()
    SELECT users.id AS users_id, users.name AS users_name,
    users.fullname AS users_fullname, users.password AS users_password
    FROM users JOIN addresses ON users.id = addresses.user_id
    WHERE users.name = ? AND addresses.email_address = ?
    ['jack', 'someaddress@foo.com']

    # ... subqueryload() emits a SELECT in order
    # to load all address records ...

当使用连接的预先加载时，如果查询包含影响外部返回到连接的行的修饰符，例如在使用 DISTINCT，LIMIT，OFFSET 或等效项时，完成的语句首先被包装在子查询中，并且专用于连接加入的急切加载应用于子查询。无论查询的格式是什么，SQLAlchemy 的加入的加载都会花费更多的时间，然后再增加 10 英里，以确保它不会影响查询的最终结果，只会加载集合和相关对象的方式。

使用什么样的装载？[¶](#what-kind-of-loading-to-use "Permalink to this headline")
--------------------------------------------------------------------------------

通常使用哪种类型的加载通常归结为优化 SQL 执行次数，发出的 SQL 的复杂性以及获取的数据量之间的折衷。让我们举两个例子：引用集合的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")和引用标量多对一引用的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")。

-   一对多收藏

> -   当使用默认的延迟加载时，如果加载 100 个对象，然后访问每个对象的集合，则会发出总共 101 条 SQL 语句，尽管每条语句通常都是一个没有任何连接的简单 SELECT。
> -   在使用连接的加载时，100 个对象及其集合的加载只会发出一条 SQL 语句。但是，获取的行的总数将等于所有集合的大小之和，再加上一个具有空集合的每个父对象的额外行。每行还将包含由父项表示的全部列，对每个集合项重复
>     -
>     SQLAlchemy 不会重新获取除主键以外的这些列，但大多数 DBAPI（有一些例外）将传输完整数据在任何情况下，每个父母通过电线连接到客户端连接。因此，只有当收集的大小相对较小时，加入的急切加载才有意义。与 INNER 加入相比，LEFT
>     OUTER JOIN 也可以是性能密集型的。
> -   使用子查询加载时，100 个对象的加载将发出两个 SQL 语句。第二条语句将获取等于所有集合大小总和的行数。使用 INNER
>     JOIN，并且请求最少的父列，只有主键。因此，当集合较大时，子查询负载才有意义。
> -   当连接或子查询加载使用多级深度时，加载集合中的集合将乘以以笛卡尔方式获取的行的总数。两种形式的急切加载总是从原始父类加入。

-   多对一参考

> -   当使用默认的延迟加载时，在收集的情况下，100 个对象的负载会发出多达 101 个 SQL 语句。然而
>     -
>     这是一个明显的例外，因为如果多对一引用是对目标主键的简单外键引用，那么将使用[`Query.get()`](query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")因此，在这里，如果对象集合引用相对较小的目标对象集合，或者完整的可能目标对象集合已被加载到会话中并被强引用，则使用默认的 lazy
>     ='select'\< / t0\>是迄今为止最有效的方法。
> -   使用连接加载时，100 个对象的加载只会发出一条 SQL 语句。连接将是一个 LEFT
>     OUTER
>     JOIN，在所有情况下总行数将等于 100。如果你知道每个父对象都有一个子对象（即外键引用不是 NULL），那么可以将[`innerjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin "sqlalchemy.orm.relationship")设置为`True`在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")中指定。对于有很多可能的目标引用可能尚未加载的对象加载，使用 INNER
>     JOIN 加载加载非常有效。
> -   子查询加载将为所有子对象发出第二次加载，因此对于 100 个对象的加载，将会发出两条 SQL 语句。然而，除了可能在所有情况下子查询加载都可以使用 INNER
>     JOIN，而连接加载要求外键不是 NULL，这里可能没有太多优势。

将显式连接/语句路由到预先加载的集合[¶](#routing-explicit-joins-statements-into-eagerly-loaded-collections "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------

[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")的行为是这样的：自动创建连接，使用匿名别名作为目标，其结果被路由到加载对象的集合和标量引用。通常情况下，查询已经包含了代表特定集合或标量引用的必要连接，并且由连接的加载特性添加的连接是多余的
- 但您仍然希望集合/引用被填充。

为此 SQLAlchemy 提供[`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")选项。该选项的使用方式与[`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")选项相同，只是假定[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")将显式指定适当的连接。下面，我们指定`User`和`Address`之间的连接，并将其作为加载`User.addresses`的基础：

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        addresses = relationship("Address")

    class Address(Base):
        __tablename__ = 'address'

        # ...

    q = session.query(User).join(User.addresses).\
                options(contains_eager(User.addresses))

如果语句的“热切”部分是“别名”，则可以使用[`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")的`alias`关键字参数指示它。这是作为对[`aliased()`](query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")或[`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")结构的引用发送的：

    # use an alias of the Address entityplain
    adalias = aliased(Address)

    # construct a Query object which expects the "addresses" results
    query = session.query(User).\
        outerjoin(adalias, User.addresses).\
        options(contains_eager(User.addresses, alias=adalias))

    # get results normally
    sqlr = query.all()
    SELECT users.user_id AS users_user_id, users.user_name AS users_user_name, adalias.address_id AS adalias_address_id,
    adalias.user_id AS adalias_user_id, adalias.email_address AS adalias_email_address, (...other columns...)
    FROM users LEFT OUTER JOIN email_addresses AS email_addresses_1 ON users.user_id = email_addresses_1.user_id

The path given as the argument to [`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")
needs to be a full path from the starting entity.
例如，如果我们正在加载`Users->orders->Order->items->Item`，那么字符串版本将如下所示：

    query(User).options(contains_eager('orders').contains_eager('items'))

或者使用类绑定描述符：

    query(User).options(contains_eager(User.orders).contains_eager(Order.items))

### 使用 contains\_eager()加载自定义过滤的收集结果[¶](#using-contains-eager-to-load-a-custom-filtered-collection-result "Permalink to this headline")

当我们使用[`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")时，*我们*正在构建将用于填充集合的 SQL。由此看来，我们可以选择**修改**集合要存储的值，方法是编写我们的 SQL 来为集合或标量属性加载元素的子集。

作为一个例子，我们可以加载一个`User`对象，并通过过滤仅仅将特定的地址加载到它的`.addresses`集合中：

    q = session.query(User).join(User.addresses).\
                filter(Address.email.like('%ed%')).\
                options(contains_eager(User.addresses))

The above query will load only `User` objects which
contain at least `Address` object that contains the
substring `'ed'` in its `email`
field; the `User.addresses` collection will contain
**only** these `Address` entries, and *not* any
other `Address` entries that are in fact associated
with the collection.

警告

请记住，当我们只将对象的子集加载到集合中时，该集合不再代表数据库中的实际内容。如果我们试图向这个集合添加条目，我们可能会发现自己与已经在数据库中但未在本地加载的条目冲突。

另外，一旦对象或属性过期，**集合将完全重新加载正常**。This expiration
occurs whenever the [`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit"),
[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")
methods are used assuming default session settings, or the
[`Session.expire_all()`](session_api.html#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")
or [`Session.expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")
methods are used.

由于这些原因，当需要一个对象加上一组自定义的相关对象时，更愿意在元组中返回单独的字段而不是人为改变集合：

    q = session.query(User, Address).join(User.addresses).\
                filter(Address.email.like('%ed%'))

### 任意语句的高级用法[¶](#advanced-usage-with-arbitrary-statements "Permalink to this headline")

可以更加创造性地使用`alias`参数，因为它可以表示任何一组任意名称以匹配到一个语句中。在它下面链接到一个将一组列对象链接到一个字符串 SQL 语句的[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")：

    # label the columns of the addresses table
    eager_columns = select([
                        addresses.c.address_id.label('a1'),
                        addresses.c.email_address.label('a2'),
                        addresses.c.user_id.label('a3')])

    # select from a raw SQL statement which uses those label names for the
    # addresses table.  contains_eager() matches them up.
    query = session.query(User).\
        from_statement("select users.*, addresses.address_id as a1, "
                "addresses.email_address as a2, addresses.user_id as a3 "
                "from users left outer join addresses on users.user_id=addresses.user_id").\
        options(contains_eager(User.addresses, alias=eager_columns))

创建自定义加载规则[¶](#creating-custom-load-rules "Permalink to this headline")
-------------------------------------------------------------------------------

警告

这是一项先进的技术！应该使用非常小心和测试。

ORM 具有各种边界情况，其中属性的值在本地可用，但是 ORM 本身并不知晓这一点。还有一些情况是需要用户定义的加载属性系统。为了支持用户定义的加载系统的用例，提供了一个关键函数[`attributes.set_committed_value()`](session_api.html#sqlalchemy.orm.attributes.set_committed_value "sqlalchemy.orm.attributes.set_committed_value")。这个函数基本上等同于 Python 自己的`setattr()`函数，除了应用于目标对象时，用于确定刷新时间更改的 SQLAlchemy 的“属性历史记录”系统被绕过；该属性的分配方式与 ORM 从数据库中加载该属性的方式相同。

使用[`attributes.set_committed_value()`](session_api.html#sqlalchemy.orm.attributes.set_committed_value "sqlalchemy.orm.attributes.set_committed_value")可以与另一个称为[`InstanceEvents.load()`](events.html#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")的关键事件组合，以在加载对象时生成属性填充行为。一个这样的例子是双向的“一对一”情况，其中加载一对一的“多对一”一方也应该暗示“一对多”方的价值。SQLAlchemy
ORM 在加载相关对象时不会考虑 backrefs，它将“一对一”视为另一个“一对多”，而这恰好是一行。

鉴于以下映射：

    from sqlalchemy import Integer, ForeignKey, Columnplain
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()


    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        b_id = Column(ForeignKey('b.id'))
        b = relationship("B", backref=backref("a", uselist=False), lazy='joined')


    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)

如果我们查询一个`A`行，然后询问`a.b.a`，我们将得到一个额外的SELECT：

    >>> a1.b.aplain
    SELECT a.id AS a_id, a.b_id AS a_b_id
    FROM a
    WHERE ? = a.b_id

由于`b.a`与`a1`的值相同，因此该 SELECT 是多余的。我们可以创建一个有效规则来为我们填充这个：

    from sqlalchemy import eventplain
    from sqlalchemy.orm import attributes

    @event.listens_for(A, "load")
    def load_b(target, context):
        if 'b' in target.__dict__:
            attributes.set_committed_value(target.b, 'a', target)

现在当我们查询`A`时，我们将从我们的事件中获得`A.b`来自加入的预先加载和`A.b.a`

    sqla1 = s.query(A).first()plain
    SELECT a.id AS a_id, a.b_id AS a_b_id, b_1.id AS b_1_id
    FROM a LEFT OUTER JOIN b AS b_1 ON b_1.id = a.b_id
     LIMIT ? OFFSET ?
    (1, 0)
    assert a1.b.a is a1

Relationship Loader API [¶](#relationship-loader-api "Permalink to this headline")
----------------------------------------------------------------------------------

`sqlalchemy.orm。 T0>  contains_alias  T1> （ T2> 别名 T3> ） T4> ¶ T5 >`{.descclassname}
:   返回将向[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")指示主表已被别名的`MapperOption`。

    这是一个很少用的选项，以适应[`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")与使用别名父表的用户定义SELECT语句结合使用的情况。例如。：

        # define an aliased UNION called 'ulist'
        ulist = users.select(users.c.user_id==7).\
                        union(users.select(users.c.user_id>7)).\
                        alias('ulist')

        # add on an eager load of "addresses"
        statement = ulist.outerjoin(addresses).\
                        select().apply_labels()

        # create query, indicating "ulist" will be an
        # alias for the main table, "addresses"
        # property should be eager loaded
        query = session.query(User).options(
                                contains_alias(ulist),
                                contains_eager(User.addresses))

        # then get results via the statement
        results = query.from_statement(statement).all()

    参数：

    **alias**[¶](#sqlalchemy.orm.contains_alias.params.alias) – is the
    string name of an alias, or a [`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
    object representing the alias.

 `sqlalchemy.orm.`{.descclassname}`contains_eager`{.descname}(*\*keys*, *\*\*kw*)[¶](#sqlalchemy.orm.contains_eager "Permalink to this definition")
:   指示应该从查询中手动指定的列中急切加载给定属性。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。plain

    该选项与加载所需行的显式连接一起使用，即：

        sess.query(Order).\
                join(Order.user).\
                options(contains_eager(Order.user))

    上面的查询将从`Order`实体连接到其相关的`User`实体，并且返回的`Order`对象将具有`Order.user`属性预填充。

    [`contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")还接受一个别名参数，该参数是别名的字符串名称，[`alias()`](core_selectable.html#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")结构或[`aliased()`](query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")结构。当急切加载的行来自别名表时，请使用它：

        user_alias = aliased(User)
        sess.query(Order).\
                join((user_alias, Order.user)).\
                options(contains_eager(Order.user, alias=user_alias))

    也可以看看

    [Routing Explicit Joins/Statements into Eagerly Loaded
    Collections](#contains-eager)

`sqlalchemy.orm。 T0>  defaultload  T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   指示应使用其默认加载程序样式加载的属性。

    此方法用于链接到其他加载器选项，例如在链接到正在加载的父类的关系的类上设置[`orm.defer()`](loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")选项。[`orm.defaultload()`](#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")来导航此路径而不更改关系的加载样式：

        session.query(MyClass).options(defaultload("someattr").defer("some_column"))

    也可以看看

    [`orm.defer()`](loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")

    [`orm.undefer()`](loading_columns.html#sqlalchemy.orm.undefer "sqlalchemy.orm.undefer")

`sqlalchemy.orm。`{.descclassname} `eagerload`{.descname} （ *\* args*，*\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.orm.eagerload "Permalink to this definition")
:   [`joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")的同义词。

`sqlalchemy.orm。`{.descclassname} `eagerload_all`{.descname} （ *\* args*，*\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.orm.eagerload_all "Permalink to this definition")
:   [`joinedload_all()`](#sqlalchemy.orm.joinedload_all "sqlalchemy.orm.joinedload_all")的同义词

`sqlalchemy.orm。 T0>  immediateload  T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   指示应该使用带有每个属性的 SELECT 语句的立即加载来加载给定的属性。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。

    也可以看看

    [Relationship Loading Techniques](#)

    [`orm.joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")

    [`orm.lazyload()`](#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")

    [`relationship.lazy`](relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship")

 `sqlalchemy.orm.`{.descclassname}`joinedload`{.descname}(*\*keys*, *\*\*kw*)[¶](#sqlalchemy.orm.joinedload "Permalink to this definition")
:   表明给定的属性应该使用连接的预加载加载。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。plain

    例子：

        # joined-load the "orders" collection on "User"
        query(User).options(joinedload(User.orders))

        # joined-load Order.items and then Item.keywords
        query(Order).options(joinedload(Order.items).joinedload(Item.keywords))

        # lazily load Order.items, but when Items are loaded,
        # joined-load the keywords collection
        query(Order).options(lazyload(Order.items).joinedload(Item.keywords))

    参数：

    **innerjoin** [¶](#sqlalchemy.orm.joinedload.params.innerjoin) -

    如果`True`，则表示加入的预先加载应该使用内部联接而不是左侧外部联接的默认加载：

        query(Order).options(joinedload(Order.user, innerjoin=True))

    为了将多个渴望连接链接在一起，其中一些可能是OUTER和其他INNER，右嵌套连接用于链接它们：

        query(A).options(
            joinedload(A.bs, innerjoin=False).
                joinedload(B.cs, innerjoin=True)
        )

    上面的查询通过“外部”连接链接A.bs，并通过“内部”连接链接B.cs会将连接呈现为“左侧外部连接（b
    JOIN
    c）”。当使用SQLite时，这种形式的JOIN被转换为使用完整的子查询，否则不直接支持该语法。

    `innerjoin`标志也可以用术语`"unnested"`来表示。这将防止连接成为右嵌套，并且会绕过“内部”连接而将“innerjoin”预紧装置连接到“outerjoin”预紧装置。使用这个表格如下：

        query(A).options(
            joinedload(A.bs, innerjoin=False).
                joinedload(B.cs, innerjoin="unnested")
        )

    连接将呈现为“左外连接b左外连接c”，以便所有“a”匹配，而不是被不包含“c”的“b”不正确地限制。

    注意

    The “unnested” flag does **not** affect the JOIN rendered from a
    many-to-many association table, e.g. a table configured as
    [`relationship.secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship"),
    to the target table; for correctness of results, these joins are
    always INNER and are therefore right-nested if linked to an OUTER
    join.

    版本0.9.4中的新功能：增加了对嵌套的渴望“内部”连接的支持。请参阅[Right-nested
    inner joins available in joined eager
    loads](changelog_migration_09.html#feature-2976)中可用的右嵌套内连接。

    版本1.0.0更改： `innerjoin=True`现在意味着`innerjoin="nested"`，而在0.9中暗示`innerjoin="unnested"`为了实现1.0之前的“unnested”内部联接行为，请使用值`innerjoin="unnested"`。请参见[Right inner join nesting now the default for
    joinedload with
    innerjoin=True](changelog_migration_10.html#migration-3008)的joinedload的缺省值。

    注意

    由[`orm.joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")生成的连接是**匿名别名**。连接进行的标准无法修改，[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")也不能以任何方式引用这些连接，包括排序。

    要生成明确可用的特定SQL JOIN，请使用[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")。要将显式JOIN与急切加载的集合结合使用，请使用[`orm.contains_eager()`](#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")；请参见[Routing
    Explicit Joins/Statements into Eagerly Loaded
    Collections](#contains-eager)。

    也可以看看

    [Relationship Loading Techniques](#)

    [Routing Explicit Joins/Statements into Eagerly Loaded
    Collections](#contains-eager)

    [`orm.subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")

    [`orm.lazyload()`](#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")

    [`relationship.lazy`](relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship")

    [`relationship.innerjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin "sqlalchemy.orm.relationship")
    - [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")-level
    version of the [`joinedload.innerjoin`](#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")
    option.

 `sqlalchemy.orm.`{.descclassname}`joinedload_all`{.descname}(*\*keys*, *\*\*kw*)[¶](#sqlalchemy.orm.joinedload_all "Permalink to this definition")
:   为[`orm.joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")生成一个独立的“全部”选项。

    从版本0.9.0开始弃用：“\_all()”样式被方法链接取代，例如：plain

        session.query(MyClass).options(
            joinedload("someattribute").joinedload("anotherattribute")
        )

`sqlalchemy.orm。 T0>  lazyload  T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   指示应该使用“懒惰”加载来加载给定的属性。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。plain

    也可以看看

    [`relationship.lazy`](relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship")

`sqlalchemy.orm。 T0> 空载 T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   指示给定的关系属性应该保持卸载状态。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。plain

    [`orm.noload()`](#sqlalchemy.orm.noload "sqlalchemy.orm.noload")适用于[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")属性；对于基于列的属性，请参阅[`orm.defer()`](loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")。

`sqlalchemy.orm。 T0>  raiseload  T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   指示给定的关系属性应该禁止延迟加载。

    使用[`orm.raiseload()`](#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload")配置的关系属性将在访问时引发[`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")。这是有用的典型方式是当应用程序试图确保在特定上下文中访问的所有关系属性已经通过预先加载加载时。与其不必通过SQL日志来确保延迟加载不会发生，这种策略会立即引发它们。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。

    [`orm.raiseload()`](#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload")仅适用于[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")属性。

    版本1.1中的新功能

`sqlalchemy.orm。 T0>  subqueryload  T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   指示应该使用子查询预加载来加载给定的属性。

    该函数是[`Load`](query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")接口的一部分，并支持方法链接和独立操作。

    例子：

        # subquery-load the "orders" collection on "User"
        query(User).options(subqueryload(User.orders))

        # subquery-load Order.items and then Item.keywords
        query(Order).options(subqueryload(Order.items).subqueryload(Item.keywords))

        # lazily load Order.items, but when Items are loaded,
        # subquery-load the keywords collection
        query(Order).options(lazyload(Order.items).subqueryload(Item.keywords))

    也可以看看

    [Relationship Loading Techniques](#)

    [`orm.joinedload()`](#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")

    [`orm.lazyload()`](#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")

    [`relationship.lazy`](relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship")

`sqlalchemy.orm。 T0>  subqueryload_all  T1> （ T2>  *键 T3> ） T4> ¶ T5>`{.descclassname}
:   为[`orm.subqueryload()`](#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")生成一个独立的“全部”选项。

    从版本0.9.0开始弃用：“\_all()”样式被方法链接取代，例如：

        session.query(MyClass).options(
            subqueryload("someattribute").subqueryload("anotherattribute")
        )


