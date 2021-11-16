---
title: SQL 表达式语言教程
date: 2021-02-20 22:41:36
permalink: /sqlalchemy/core/tutorial/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
SQL 表达式语言教程[¶](#sql-expression-language-tutorial "Permalink to this headline")
====================================================================================

SQLAlchemy 表达式语言提供了一个使用 Python 结构表示关系数据库结构和表达式的系统。这些结构被模拟为尽可能接近底层数据库的结构，同时提供数据库后端之间各种实现差异的一些抽象。虽然构造尝试用一致的结构来表示后端之间的等价概念，但它们并不隐藏对特定后端子集而言唯一的有用概念。因此，表达式语言提供了一种编写后端中立的 SQL 表达式的方法，但并不试图强制该表达式是后端中立的。

表达式语言与对象关系映射器形成对比，对象关系映射器是一种建立在表达式语言之上的独特 API。而在[Object
Relational
Tutorial](orm_tutorial.html)中引入的 ORM 呈现高层次和抽象的使用模式，这本身就是表达式语言的应用使用的一个例子，表达式语言提供了一个表示基元关系数据库的构造直接没有意见。

虽然 ORM 和表达式语言的使用模式之间存在重叠，但它们的相似之处却比最初出现时更为肤浅。一个从用户定义的[域模型](http://en.wikipedia.org/wiki/Domain_model)的角度接近数据的结构和内容，该模型透明地从其底层存储模型中持久保留并刷新。另一种方法从文字模式和 SQL 表达式表达式的角度来看，它们被显式地组合成数据库单独消费的消息。

虽然应用程序需要定义自己的系统，将应用程序概念转换为单独的数据库消息和单个数据库结果集，但是可以使用表达式语言专门构建成功的应用程序。或者，使用 ORM 构建的应用程序可以在高级方案中直接在需要特定数据库交互的特定区域中偶尔使用表达式语言。

The following tutorial is in doctest format, meaning each
`>>>` line represents something you can type at a
Python command prompt, and the following text represents the expected
return value.本教程没有先决条件。

版本检查[¶](#version-check "Permalink to this headline")
--------------------------------------------------------

快速检查以确认我们至少处于 SQLAlchemy 的**版本 1.1**：

    >>> import sqlalchemy
    >>> sqlalchemy.__version__  # doctest: +SKIP
    1.1.0

连接[¶ T0\>](#connecting "Permalink to this headline")
------------------------------------------------------

对于本教程，我们将使用一个仅内存的 SQLite 数据库。这是一种简单的测试方法，无需在任何地方定义实际的数据库。要连接，我们使用[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")：

    >>> from sqlalchemy import create_engineplain
    >>> engine = create_engine('sqlite:///:memory:', echo=True)

`echo`标志是设置 SQLAlchemy 日志记录的快捷方式，它是通过 Python 的标准`日志`模块完成的。启用它，我们将看到生成的所有 SQL。如果您正在学习本教程并希望产生更少的输出，请将其设置为`False`。本教程将把 SQL 格式化为一个弹出窗口，所以它不会妨碍我们；只需点击“SQL”链接即可查看正在生成的内容。

[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的返回值是[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的一个实例，它表示数据库的核心接口，通过处理方言数据库和[DBAPI](glossary.html#term-dbapi)的使用细节。在这种情况下，SQLite 方言将向 Python 内置的`sqlite3`模块解释指令。

懒惰连接

当[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")首次返回时，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")尚未尝试连接到数据库；这只会在第一次被要求对数据库执行任务时发生。

The first time a method like [`Engine.execute()`](connections.html#sqlalchemy.engine.Engine.execute "sqlalchemy.engine.Engine.execute")
or [`Engine.connect()`](connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect")
is called, the [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
establishes a real [DBAPI](glossary.html#term-dbapi) connection to the
database, which is then used to emit the SQL.

也可以看看

[Database Urls](engines.html#database-urls) -
包含连接到多种数据库的[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")示例，其中包含更多信息的链接。

定义和创建表格[¶](#define-and-create-tables "Permalink to this headline")
-------------------------------------------------------------------------

SQL 表达式语言在大多数情况下针对表列构造表达式。在 SQLAlchemy 中，一个列通常由一个名为[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的对象表示，并且在所有情况下，一个[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")都与一个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")关联。[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象及其关联的子对象的集合称为**数据库元数据**。在本教程中，我们将明确地列出几个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，但是请注意，SA 还可以从现有数据库中自动“导入”整个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象集合（此过程称为**表反射**）。

我们使用[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")结构将所有表定义在名为[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")的目录中，类似于常规的 SQL
CREATE
TABLE 语句。我们将创建两个表，其中一个表示应用程序中的“用户”，另一个表示“users”表中每行的零个或多个“电子邮件地址”：

    >>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    >>> metadata = MetaData()
    >>> users = Table('users', metadata,
    ...     Column('id', Integer, primary_key=True),
    ...     Column('name', String),
    ...     Column('fullname', String),
    ... )

    >>> addresses = Table('addresses', metadata,
    ...   Column('id', Integer, primary_key=True),
    ...   Column('user_id', None, ForeignKey('users.id')),
    ...   Column('email_address', String, nullable=False)
    ...  )

所有关于如何定义[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象以及如何从现有数据库自动创建它们的描述在[Describing
Databases with MetaData](metadata.html)中描述。

接下来，为了告诉[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")，我们实际上希望在 SQLite 数据库中创建真实的表格选择，我们使用[`create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")，并将`engine`实例指向我们的数据库。这将在创建之前检查每个表的存在情况，因此可以安全地调用多次：

    sql>>> metadata.create_all(engine)
    SE...
    CREATE TABLE users (
        id INTEGER NOT NULL,
        name VARCHAR,
        fullname VARCHAR,
        PRIMARY KEY (id)
    )
    ()
    COMMIT
    CREATE TABLE addresses (
        id INTEGER NOT NULL,
        user_id INTEGER,
        email_address VARCHAR NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
    )
    ()
    COMMIT

注意

熟悉 CREATE
TABLE 语法的用户可能注意到 VARCHAR 列的生成没有长度；在 SQLite 和 Postgresql 上，这是一个有效的数据类型，但是在其他情况下，它是不允许的。因此，如果在其中一个数据库上运行本教程，并且希望使用 SQLAlchemy 发出 CREATE
TABLE，则可以为[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")类型提供“length”，如下所示：

    Column('name', String(50))plain

[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")上的长度字段以及[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")，[`Numeric`](type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")等可用的类似精度/缩放字段。除了创建表格时，不会被 SQLAlchemy 引用。

此外，Firebird 和 Oracle 需要序列来生成新的主键标识符，并且 SQLAlchemy 不会在未经指示的情况下生成或采用这些标识符。为此，您可以使用[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")结构：

    from sqlalchemy import Sequence
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True)

一个完整的，万无一失的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")是：

    users = Table('users', metadata,
       Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
       Column('name', String(50)),
       Column('fullname', String(50)),
       Column('password', String(12))
    )

我们分别包含这个更详细的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造，以突出显示主要针对 Python 内使用的最小构造与将用于在特定的后端上发出 CREATE
TABLE 语句的构造之间的区别更严格的要求。

插入表达式[¶](#insert-expressions "Permalink to this headline")
---------------------------------------------------------------

我们要创建的第一个 SQL 表达式是[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")结构，它表示一个 INSERT 语句。这通常是相对于其目标表创建的：

    >>> ins = users.insert()

要查看此构造产生的 SQL 样本，​​请使用`str()`函数：

    >>> str(ins)
    'INSERT INTO users (id, name, fullname) VALUES (:id, :name, :fullname)'

请注意，INSERT 语句为`users`表中的每个列命名。这可以通过使用`values()`方法来限制，该方法显式地建立 INSERT 的 VALUES 子句：

    >>> ins = users.insert().values(name='jack', fullname='Jack Jones')plain
    >>> str(ins)
    'INSERT INTO users (name, fullname) VALUES (:name, :fullname)'

上面，虽然`values`方法将 VALUES 子句限制为两列，但我们放置在`values`中的实际数据未呈现到字符串中；相反，我们得到了命名绑定参数As it
turns out, our data *is* stored within our [`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
construct, but it typically only comes out when the statement is
actually executed; since the data consists of literal values, SQLAlchemy
automatically generates bind parameters for them.
我们现在可以通过查看声明的编译形式来查看这些数据：

    >>> ins.compile().paramsplain
    {'fullname': 'Jack Jones', 'name': 'jack'}

执行[¶ T0\>](#executing "Permalink to this headline")
-----------------------------------------------------

[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")的有趣部分正在执行它。在本教程中，我们将主要关注执行 SQL 构造的最明确的方法，并稍后介绍一些“快捷方式”。我们创建的`engine`对象是一个能够向数据库发出 SQL 的数据库连接的存储库。要获取连接，我们使用`connect()`方法：

    >>> conn = engine.connect()plain
    >>> conn
    <sqlalchemy.engine.base.Connection object at 0x...>

[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象表示主动检出的 DBAPI 连接资源。让我们将[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")对象并看看会发生什么：

    >>> result = conn.execute(ins)
    INSERT INTO users (name, fullname) VALUES (?, ?)
    ('jack', 'Jack Jones')
    COMMIT

所以 INSERT 语句现在发布到数据库中。尽管我们在输出中获得了位置“qmark”绑定参数，而不是“命名的”绑定参数。怎么来的
？因为执行时，[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")使用 SQLite
**方言**来帮助生成语句；当我们使用`str()`函数时，语句不知道这个方言，并回到使用命名参数的默认值。我们可以手动查看，如下所示：

    >>> ins.bind = engineplain
    >>> str(ins)
    'INSERT INTO users (name, fullname) VALUES (?, ?)'

当我们调用`execute()`时，我们得到的`result`变量​​怎么样？由于 SQLAlchemy [`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象引用了 DBAPI 连接，因此称为[`ResultProxy`](connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")对象的结果与 DBAPI 游标对象类似。在 INSERT 的情况下，我们可以从中获取重要信息，例如使用[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")从我们的语句中生成的主键值：

    >>> result.inserted_primary_key
    [1]

SQLite 自动生成`1`的值，但仅仅是因为我们没有在我们的[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")语句中指定`id`列；否则，我们的显性价值将被使用。In either case, SQLAlchemy
always knows how to get at a newly generated primary key value, even
though the method of generating them is different across different
databases; each database’s [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
knows the specific steps needed to determine the correct value (or
values; note that [`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")
returns a list so that it supports composite primary keys).
这里的方法包括使用`cursor.lastrowid`，从数据库特定的函数中选择，使用`INSERT..RETURNING`语法；这一切都是透明的。

执行多个语句[¶](#executing-multiple-statements "Permalink to this headline")
----------------------------------------------------------------------------

我们上面的插入示例是故意稍微画出来展示一些表达式语言结构的各种行为。在通常情况下，通常根据发送给[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上的`execute()`方法的参数编译[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")语句，以便不需要在[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")中使用`values`关键字。让我们再次创建一个通用的[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")语句并以“正常”的方式使用它：

    >>> ins = users.insert()plain
    >>> conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')
    INSERT INTO users (id, name, fullname) VALUES (?, ?, ?)
    (2, 'wendy', 'Wendy Williams')
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

上面，因为我们在`execute()`方法中指定了所有三列，所以编译的[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")包含了所有三列。根据我们指定的参数，[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")语句在执行时编译；如果我们指定的参数较少，那么[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")在其 VALUES 子句中的条目较少。

要使用 DBAPI 的`executemany()`方法发出很多插入，我们可以发送一个字典列表，每个字典包含一组不同的要插入的参数，就像我们在这里添加一些电子邮件地址一样：

    >>> conn.execute(addresses.insert(), [plain
    ...    {'user_id': 1, 'email_address' : 'jack@yahoo.com'},
    ...    {'user_id': 1, 'email_address' : 'jack@msn.com'},
    ...    {'user_id': 2, 'email_address' : 'www@www.org'},
    ...    {'user_id': 2, 'email_address' : 'wendy@aol.com'},
    ... ])
    INSERT INTO addresses (user_id, email_address) VALUES (?, ?)
    ((1, 'jack@yahoo.com'), (1, 'jack@msn.com'), (2, 'www@www.org'), (2, 'wendy@aol.com'))
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

上面，我们再次依赖 SQLite 为每个`addresses`行自动生成主键标识符。

当执行多组参数时，每个字典必须有**相同的**组键；即你在一些字典中的键比其他键少。这是因为[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")语句是针对列表中的**第一个**字典编译的，并且假定所有后续的参数字典都与该语句兼容。

每个[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")，[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")和[`delete()`](dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")结构都可以使用“executemany”风格的调用。

选择[¶ T0\>](#selecting "Permalink to this headline")
-----------------------------------------------------

我们从插入开始，以便我们的测试数据库中包含一些数据。数据中更有趣的部分是选择它！稍后我们将介绍 UPDATE 和 DELETE 语句。用于生成 SELECT 语句的主要结构是[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")函数：

    >>> from sqlalchemy.sql import selectplain
    >>> s = select([users])
    >>> result = conn.execute(s)
    SELECT users.id, users.name, users.fullname
    FROM users
    ()

在上面，我们发出了一个基本的[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")调用，将`users`表放置在 select 的 COLUMNS 子句中，然后执行。SQLAlchemy 将`users`表扩展为每个列的集合，并为我们生成了一个 FROM 子句。The result
returned is again a [`ResultProxy`](connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
object, which acts much like a DBAPI cursor, including methods such as
[`fetchone()`](connections.html#sqlalchemy.engine.ResultProxy.fetchone "sqlalchemy.engine.ResultProxy.fetchone")
and [`fetchall()`](connections.html#sqlalchemy.engine.ResultProxy.fetchall "sqlalchemy.engine.ResultProxy.fetchall").
从中获取行的最简单方法是迭代：

    >>> for row in result:plain
    ...     print(row)
    (1, u'jack', u'Jack Jones')
    (2, u'wendy', u'Wendy Williams')

上面，我们看到打印每一行产生了一个简单的元组结果。我们有更多的选择来访问每一行中的数据。一种非常常见的方式是通过字典访问，使用字符串名称的列：

    sql>>> result = conn.execute(s)
    SELECT users.id, users.name, users.fullname
    FROM users
    ()

    >>> row = result.fetchone()
    >>> print("name:", row['name'], "; fullname:", row['fullname'])
    name: jack ; fullname: Jack Jones

整数索引也适用：

    >>> row = result.fetchone()plain
    >>> print("name:", row[1], "; fullname:", row[2])
    name: wendy ; fullname: Wendy Williams

但另一种方式，其用处稍后将变得明显，就是直接将[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象用作关键字：

    sql>>> for row in conn.execute(s):
    ...     print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])
    SELECT users.id, users.name, users.fullname
    FROM users
    ()
    name: jack ; fullname: Jack Jones
    name: wendy ; fullname: Wendy Williams

剩余待处理行的结果集应在丢弃前显式关闭。当对象被垃圾收集时，由[`ResultProxy`](connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")引用的游标和连接资源将分别关闭并返回到连接缓冲池，但最好将其明确化，因为某些数据库 API 对这些事情非常挑剔：

    >>> result.close()plain

如果我们想更仔细地控制放置在 select 的 COLUMNS 子句中的列，我们引用来自[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的单个[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象。它们可以作为[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的`c`属性的命名属性使用：

    >>> s = select([users.c.name, users.c.fullname])
    sql>>> result = conn.execute(s)
    SELECT users.name, users.fullname
    FROM users
    ()
    >>> for row in result:
    ...     print(row)
    (u'jack', u'Jack Jones')
    (u'wendy', u'Wendy Williams')

让我们观察关于 FROM 子句的一些有趣的事情。尽管生成的语句包含两个不同的部分，即“SELECT 列”部分和“FROM 表”部分，但我们的[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构只包含一个包含列的列表。这个怎么用
？让我们尝试将*两个*表放入我们的[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")语句中：

    sql>>> for row in conn.execute(select([users, addresses])):
    ...     print(row)
    SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address
    FROM users, addresses
    ()
    (1, u'jack', u'Jack Jones', 1, 1, u'jack@yahoo.com')
    (1, u'jack', u'Jack Jones', 2, 1, u'jack@msn.com')
    (1, u'jack', u'Jack Jones', 3, 2, u'www@www.org')
    (1, u'jack', u'Jack Jones', 4, 2, u'wendy@aol.com')
    (2, u'wendy', u'Wendy Williams', 1, 1, u'jack@yahoo.com')
    (2, u'wendy', u'Wendy Williams', 2, 1, u'jack@msn.com')
    (2, u'wendy', u'Wendy Williams', 3, 2, u'www@www.org')
    (2, u'wendy', u'Wendy Williams', 4, 2, u'wendy@aol.com')

它将**两个**表放入 FROM 子句中。但是，它也是一团糟。那些熟悉 SQL 连接的人知道这是一个**笛卡尔积**；来自`users`表的每行都是根据`addresses`表中的每行生成的。所以为了使这个陈述有一些理智，我们需要一个 WHERE 子句。我们使用[`Select.where()`](selectable.html#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")来做到这一点：

    >>> s = select([users, addresses]).where(users.c.id == addresses.c.user_id)plain
    sql>>> for row in conn.execute(s):
    ...     print(row)
    SELECT users.id, users.name, users.fullname, addresses.id,
       addresses.user_id, addresses.email_address
    FROM users, addresses
    WHERE users.id = addresses.user_id
    ()
    (1, u'jack', u'Jack Jones', 1, 1, u'jack@yahoo.com')
    (1, u'jack', u'Jack Jones', 2, 1, u'jack@msn.com')
    (2, u'wendy', u'Wendy Williams', 3, 2, u'www@www.org')
    (2, u'wendy', u'Wendy Williams', 4, 2, u'wendy@aol.com')

So that looks a lot better, we added an expression to our
[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
which had the effect of adding
`WHERE users.id = addresses.user_id` to our
statement, and our results were managed down so that the join of
`users` and `addresses` rows
made sense. 但让我们看看那个表达？它只是在两个不同的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象之间使用 Python 等号运算符。应该清楚，有些事情已经到来。Saying
`1 == 1` produces `True`, and
`1 == 2` produces `False`, not a
WHERE clause. 因此，让我们看看到底表达的是什么：

    >>> users.c.id == addresses.c.user_id
    <sqlalchemy.sql.elements.BinaryExpression object at 0x...>

哇，惊喜！这既不是`True`也不是`False`。那么它是什么？

    >>> str(users.c.id == addresses.c.user_id)
    'users.id = addresses.user_id'

正如你所看到的，`==`运算符产生的对象非常类似于我们制作的[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")和[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")对象到目前为止，这要归功于 Python 的`__eq__()`内置；你可以调用`str()`并产生 SQL。到现在为止，我们可以看到，我们正在使用的所有东西最终都是同一类型的对象。SQLAlchemy 将所有这些表达式的基类称为[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")。

算[¶ T0\>](#operators "Permalink to this headline")
---------------------------------------------------

由于我们偶然发现了 SQLAlchemy 的操作符范例，让我们来看看它的一些功能。我们已经看到如何将两列彼此等同起来：

    >>> print(users.c.id == addresses.c.user_id)
    users.id = addresses.user_id

如果我们使用一个字面值（一个字面意思，而不是一个 SQLAlchemy 子句对象），我们得到一个绑定参数：

    >>> print(users.c.id == 7)plain
    users.id = :id_1

`7`文字嵌入了生成的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")；我们可以使用与[`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")对象相同的技巧来查看它：

    >>> (users.c.id == 7).compile().params
    {u'id_1': 7}

事实证明，大多数 Python 操作符在这里生成一个 SQL 表达式，如 equals，not
equals 等。:

    >>> print(users.c.id != 7)
    users.id != :id_1

    >>> # None converts to IS NULL
    >>> print(users.c.name == None)
    users.name IS NULL

    >>> # reverse works too
    >>> print('fred' > users.c.name)
    users.name < :name_1

如果我们将两个整数列加在一起，我们得到一个加法表达式：

    >>> print(users.c.id + addresses.c.id)plain
    users.id + addresses.id

有趣的是，[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的类型很重要！如果我们在两个基于字符串的列上使用`+`（回想一下，我们在[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象中放置了[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")和[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

    >>> print(users.c.name + users.c.fullname)
    users.name || users.fullname

其中`||`是大多数数据库上使用的字符串连接运算符。但不是全部。MySQL 用户，不要害怕：

    >>> print((users.c.name + users.c.fullname).plain
    ...      compile(bind=create_engine('mysql://'))) # doctest: +SKIP
    concat(users.name, users.fullname)

以上说明了为连接到 MySQL 数据库的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")生成的 SQL；
`||`运算符现在编译为 MySQL 的`concat()`函数。

如果遇到真正不可用的操作符，可以始终使用[`ColumnOperators.op()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.op "sqlalchemy.sql.operators.ColumnOperators.op")方法；这会产生你需要的任何操作符：

    >>> print(users.c.name.op('tiddlywinks')('foo'))
    users.name tiddlywinks :name_1

该函数也可用于使按位运算符明确。例如：

    somecolumn.op('&')(0xff)plain

是 somecolumn 中的值的按位与。

### 操作员定制[¶](#operator-customization "Permalink to this headline")

While [`ColumnOperators.op()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.op "sqlalchemy.sql.operators.ColumnOperators.op")
is handy to get at a custom operator in a hurry, the Core supports
fundamental customization and extension of the operator system at the
type level.
现有操作符的行为可以在每个类型的基础上进行修改，并且可以定义新的操作，这些操作可用于属于该特定类型的所有列表达式。有关说明，请参阅[Redefining
and Creating New Operators](custom_types.html#types-operators)部分。

连词[¶ T0\>](#conjunctions "Permalink to this headline")
--------------------------------------------------------

我们希望在[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构中展示一些我们的运算符。但是我们需要把它们再加一点，所以我们先来介绍一些连词。连词是 AND 和 OR 这些小词汇，它们把事物放在一起。我们也会碰到 NOT。[`and_()`](sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")，[`or_()`](sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")和[`not_()`](sqlelement.html#sqlalchemy.sql.expression.not_ "sqlalchemy.sql.expression.not_")可以从 SQLAlchemy 提供的相应函数中工作（注意，我们也会在[`like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    >>> from sqlalchemy.sql import and_, or_, not_
    >>> print(and_(
    ...         users.c.name.like('j%'),
    ...         users.c.id == addresses.c.user_id,
    ...         or_(
    ...              addresses.c.email_address == 'wendy@aol.com',
    ...              addresses.c.email_address == 'jack@yahoo.com'
    ...         ),
    ...         not_(users.c.id > 5)
    ...       )
    ...  )
    users.name LIKE :name_1 AND users.id = addresses.user_id AND
    (addresses.email_address = :email_address_1
       OR addresses.email_address = :email_address_2)
    AND users.id <= :id_1

你也可以使用重新依存的 AND，OR 和 NOT 运算符，尽管由于 Python 运算符的优先级，你必须注意括号：

    >>> print(users.c.name.like('j%') & (users.c.id == addresses.c.user_id) &plain
    ...     (
    ...       (addresses.c.email_address == 'wendy@aol.com') | \
    ...       (addresses.c.email_address == 'jack@yahoo.com')
    ...     ) \
    ...     & ~(users.c.id>5)
    ... )
    users.name LIKE :name_1 AND users.id = addresses.user_id AND
    (addresses.email_address = :email_address_1
        OR addresses.email_address = :email_address_2)
    AND users.id <= :id_1

因此，对于所有这些词汇表，我们选择在 AOL 或 MSN 上有电子邮件地址的所有用户，其名称以“m”和“z”之间的字母开头，我们还会生成一个包含全名的列他们的电邮地址。We
will add two new constructs to this statement, [`between()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
and [`label()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label").
[`between()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
produces a BETWEEN clause, and [`label()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label")
is used in a column expression to produce labels using the
`AS` keyword; it’s recommended when selecting from
expressions that otherwise would not have a name:

    >>> s = select([(users.c.fullname +
    ...               ", " + addresses.c.email_address).
    ...                label('title')]).\
    ...        where(
    ...           and_(
    ...               users.c.id == addresses.c.user_id,
    ...               users.c.name.between('m', 'z'),
    ...               or_(
    ...                  addresses.c.email_address.like('%@aol.com'),
    ...                  addresses.c.email_address.like('%@msn.com')
    ...               )
    ...           )
    ...        )
    >>> conn.execute(s).fetchall()
    SELECT users.fullname || ? || addresses.email_address AS title
    FROM users, addresses
    WHERE users.id = addresses.user_id AND users.name BETWEEN ? AND ? AND
    (addresses.email_address LIKE ? OR addresses.email_address LIKE ?)
    (', ', 'm', 'z', '%@aol.com', '%@msn.com')
    [(u'Wendy Williams, wendy@aol.com',)]

SQLAlchemy 再一次为我们的语句找出了 FROM 子句。实际上，它会根据所有其他位决定 FROM 子句；
column 子句，where 子句，还有一些我们还没有涉及的元素，包括 ORDER BY，GROUP
BY 和 HAVING。

使用[`and_()`](sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")的快捷方式是将多个[`where()`](selectable.html#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")子句链接在一起。以上内容也可以写成：

    >>> s = select([(users.c.fullname +
    ...               ", " + addresses.c.email_address).
    ...                label('title')]).\
    ...        where(users.c.id == addresses.c.user_id).\
    ...        where(users.c.name.between('m', 'z')).\
    ...        where(
    ...               or_(
    ...                  addresses.c.email_address.like('%@aol.com'),
    ...                  addresses.c.email_address.like('%@msn.com')
    ...               )
    ...        )
    >>> conn.execute(s).fetchall()
    SELECT users.fullname || ? || addresses.email_address AS title
    FROM users, addresses
    WHERE users.id = addresses.user_id AND users.name BETWEEN ? AND ? AND
    (addresses.email_address LIKE ? OR addresses.email_address LIKE ?)
    (', ', 'm', 'z', '%@aol.com', '%@msn.com')
    [(u'Wendy Williams, wendy@aol.com',)]

我们可以通过连续的方法调用建立[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构的方式称为[method
chaining](glossary.html#term-method-chaining)。

使用文本 SQL [¶](#using-textual-sql "Permalink to this headline")
----------------------------------------------------------------

我们的最后一个例子确实成为了一小部分。从一个人所理解的文本 SQL 表达式变成一个 Python 构造，它将程序化风格中的组件组合在一起可能很难。这就是为什么 SQLAlchemy 只允许你使用字符串的原因，对于那些 SQL 已经知道并且没有强烈需要支持动态特性的语句的情况。[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构用于组成一个大部分不变的传递给数据库的文本语句。下面，我们创建一个[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")对象并执行它：

    >>> from sqlalchemy.sql import text
    >>> s = text(
    ...     "SELECT users.fullname || ', ' || addresses.email_address AS title "
    ...         "FROM users, addresses "
    ...         "WHERE users.id = addresses.user_id "
    ...         "AND users.name BETWEEN :x AND :y "
    ...         "AND (addresses.email_address LIKE :e1 "
    ...             "OR addresses.email_address LIKE :e2)")
    sql>>> conn.execute(s, x='m', y='z', e1='%@aol.com', e2='%@msn.com').fetchall()
    SELECT users.fullname || ', ' || addresses.email_address AS title
    FROM users, addresses
    WHERE users.id = addresses.user_id AND users.name BETWEEN ? AND ? AND
    (addresses.email_address LIKE ? OR addresses.email_address LIKE ?)
    ('m', 'z', '%@aol.com', '%@msn.com')
    [(u'Wendy Williams, wendy@aol.com',)]

在上面，我们可以看到使用命名的冒号格式在[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")中指定了绑定参数；不管数据库后端如何，这种格式都是一致的。为了发送参数值，我们将它们作为附加参数传递给[`execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")方法。

### 指定绑定参数行为[¶](#specifying-bound-parameter-behaviors "Permalink to this headline")

[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构使用[`TextClause.bindparams()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")方法支持预先建立的绑定值：

    stmt = text("SELECT * FROM users WHERE users.name BETWEEN :x AND :y")
    stmt = stmt.bindparams(x="m", y="z")

参数也可以显式输入：

    stmt = stmt.bindparams(bindparam("x", String), bindparam("y", String))plain
    result = conn.execute(stmt, {"x": "m", "y": "z"})

当类型需要数据类型提供的 Python 端或特殊的 SQL 端处理时，键入绑定参数是必要的。

也可以看看

[`TextClause.bindparams()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")
- full method description

### 指定结果列行为[¶](#specifying-result-column-behaviors "Permalink to this headline")

我们也可以使用[`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法指定关于结果列的信息；此方法可用于根据名称指定返回类型：

    stmt = stmt.columns(id=Integer, name=String)

或者可以在位置上传递完整的列表达式，无论是键入还是未定义。在这种情况下，最好在我们的文本 SQL 中明确列出列，因为我们的列表达式与 SQL 的相关性将在位置上完成：

    stmt = text("SELECT id, name FROM users")plain
    stmt = stmt.columns(users.c.id, users.c.name)

当我们调用[`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法时，我们得到一个[`TextAsFrom`](selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")对象，该对象支持完整的[`TextAsFrom.c`](selectable.html#sqlalchemy.sql.expression.TextAsFrom.c "sqlalchemy.sql.expression.TextAsFrom.c")和其他“可选“操作：

    j = stmt.join(addresses, stmt.c.id == addresses.c.user_id)

    new_stmt = select([stmt.c.id, addresses.c.id]).\
        select_from(j).where(stmt.c.name == 'x')

当将文本 SQL 与现有的 Core 或 ORM 模型相关联时，[`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")的位置形式特别有用，因为我们可以直接使用列表达式，而不必担心名称冲突或其他结果列名称问题在文本 SQL 中：

    >>> stmt = text("SELECT users.id, addresses.id, users.id, "
    ...     "users.name, addresses.email_address AS email "
    ...     "FROM users JOIN addresses ON users.id=addresses.user_id "
    ...     "WHERE users.id = 1").columns(
    ...        users.c.id,
    ...        addresses.c.id,
    ...        addresses.c.user_id,
    ...        users.c.name,
    ...        addresses.c.email_address
    ...     )
    sql>>> result = conn.execute(stmt)
    SELECT users.id, addresses.id, users.id, users.name,
        addresses.email_address AS email
    FROM users JOIN addresses ON users.id=addresses.user_id WHERE users.id = 1
    ()

上面的结果中有三列名为“id”，但由于我们已经在列表表达式中定位了这些列，因此当使用实际列对象作为关键字获取结果列时，名称不是问题。获取`email_address`列将是：

    >>> row = result.fetchone()plain
    >>> row[addresses.c.email_address]
    'jack@yahoo.com'

另一方面，如果我们使用了一个字符串列键，通常的基于名称的匹配规则仍然适用，并且我们会为`id`值得到一个模糊的列错误：

    >>> row["id"]
    Traceback (most recent call last):
    ...
    InvalidRequestError: Ambiguous column name 'id' in result set column descriptions

It’s important to note that while accessing columns from a result set
using [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
objects may seem unusual, it is in fact the only system used by the ORM,
which occurs transparently beneath the facade of the [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
object; in this way, the [`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
method is typically very applicable to textual statements to be used in
an ORM context. [Using Textual
SQL](orm_tutorial.html#orm-tutorial-literal-sql)中的示例说明了一个简单的用法。

版本 1.1 中的新功能： [`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法现在接受列表达式，这些列表达式将在位置上与纯文本 SQL 结果集相匹配，从而不需要列名匹配或甚至在将表元数据或 ORM 模型与文本 SQL 匹配时在 SQL 语句中是唯一的。

也可以看看

[`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
- full method description

[Using Textual SQL](orm_tutorial.html#orm-tutorial-literal-sql) -
将 ORM 级查询与[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")相集成

### 在较大的语句中使用 text()片段[¶](#using-text-fragments-inside-bigger-statements "Permalink to this headline")

[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")也可用于生成可在[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")对象中自由运行的 SQL 片段，该对象接受[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")对象作为其建设者职能的大部分参数。下面，我们结合[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")对象中[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")的用法。[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构提供了语句的“几何结构”，而[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构提供了此表单中的文本内容。我们可以建立一个声明，而无需参考任何预先建立的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")元数据：

    >>> s = select([plain
    ...        text("users.fullname || ', ' || addresses.email_address AS title")
    ...     ]).\
    ...         where(
    ...             and_(
    ...                 text("users.id = addresses.user_id"),
    ...                 text("users.name BETWEEN 'm' AND 'z'"),
    ...                 text(
    ...                     "(addresses.email_address LIKE :x "
    ...                     "OR addresses.email_address LIKE :y)")
    ...             )
    ...         ).select_from(text('users, addresses'))
    sql>>> conn.execute(s, x='%@aol.com', y='%@msn.com').fetchall()
    SELECT users.fullname || ', ' || addresses.email_address AS title
    FROM users, addresses
    WHERE users.id = addresses.user_id AND users.name BETWEEN 'm' AND 'z'
    AND (addresses.email_address LIKE ? OR addresses.email_address LIKE ?)
    ('%@aol.com', '%@msn.com')
    [(u'Wendy Williams, wendy@aol.com',)]

Changed in version 1.0.0: The [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
construct emits warnings when string SQL fragments are coerced to
[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text"),
and [`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
should be used explicitly. 请参阅[Warnings emitted when coercing full
SQL fragments into
text()](changelog_migration_10.html#migration-2992)作为背景。

### [`table()`](selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")，[`literal_column()`](sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")和[`column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column") [使用更具体的文本](#using-more-specific-text-with-table-literal-column-and-column "Permalink to this headline")

我们可以通过使用[`column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")，[`literal_column()`](sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")和[`table()`](selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")来将我们的结构级别向另一个方向移回我们声明的一些关键要素。Using
these constructs, we can get some more expression capabilities than if
we used [`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
directly, as they provide to the Core more information about how the
strings they store are to be used, but still without the need to get
into full [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
based metadata. 在下面，我们还为key [`literal_column()`](sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")对象中的两个指定了[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")数据类型，以便特定于字符串的连接运算符变为可用。我们还使用[`literal_column()`](sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")来使用限定表的表达式，例如`users.fullname`，将按原样呈现；使用[`column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")表示可能引用的单个列名称：

    >>> from sqlalchemy import select, and_, text, String
    >>> from sqlalchemy.sql import table, literal_column
    >>> s = select([
    ...    literal_column("users.fullname", String) +
    ...    ', ' +
    ...    literal_column("addresses.email_address").label("title")
    ... ]).\
    ...    where(
    ...        and_(
    ...            literal_column("users.id") == literal_column("addresses.user_id"),
    ...            text("users.name BETWEEN 'm' AND 'z'"),
    ...            text(
    ...                "(addresses.email_address LIKE :x OR "
    ...                "addresses.email_address LIKE :y)")
    ...        )
    ...    ).select_from(table('users')).select_from(table('addresses'))

    sql>>> conn.execute(s, x='%@aol.com', y='%@msn.com').fetchall()
    SELECT users.fullname || ? || addresses.email_address AS anon_1
    FROM users, addresses
    WHERE users.id = addresses.user_id
    AND users.name BETWEEN 'm' AND 'z'
    AND (addresses.email_address LIKE ? OR addresses.email_address LIKE ?)
    (', ', '%@aol.com', '%@msn.com')
    [(u'Wendy Williams, wendy@aol.com',)]

### 按标签排序或分组[¶](#ordering-or-grouping-by-a-label "Permalink to this headline")

我们有时希望使用字符串作为快捷方式的一个地方是，当我们的语句有一些我们想要在诸如“ORDER
BY”或“GROUP
BY”子句的地方引用的标签列元素时；其他候选人包括“OVER”或“DISTINCT”条款中的字段。如果我们的[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构中有这样的标签，我们可以直接通过将字符串直接传递给`select.order_by()`或`select.group_by()`等等。这将引用指定的标签并防止表达式被渲染两次：

    >>> from sqlalchemy import func
    >>> stmt = select([
    ...         addresses.c.user_id,
    ...         func.count(addresses.c.id).label('num_addresses')]).\
    ...         order_by("num_addresses")

    sql>>> conn.execute(stmt).fetchall()
    SELECT addresses.user_id, count(addresses.id) AS num_addresses
    FROM addresses ORDER BY num_addresses
    ()
    [(2, 4)]

通过传递字符串名称，我们可以使用[`asc()`](sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")或[`desc()`](sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")等修饰符：

    >>> from sqlalchemy import func, desc
    >>> stmt = select([
    ...         addresses.c.user_id,
    ...         func.count(addresses.c.id).label('num_addresses')]).\
    ...         order_by(desc("num_addresses"))

    sql>>> conn.execute(stmt).fetchall()
    SELECT addresses.user_id, count(addresses.id) AS num_addresses
    FROM addresses ORDER BY num_addresses DESC
    ()
    [(2, 4)]

请注意，此处的字符串功能非常适合于我们已经使用[`label()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label")方法创建特定命名标签的情况。在其他情况下，我们总是希望直接引用[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象，以便表达式系统可以为渲染提供最有效的选择。下面，我们将说明如何使用[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")消除我们想要按多次出现的列名进行排序时的不明确性：

    >>> u1a, u1b = users.alias(), users.alias()
    >>> stmt = select([u1a, u1b]).\
    ...             where(u1a.c.name > u1b.c.name).\
    ...             order_by(u1a.c.name)  # using "name" here would be ambiguous

    sql>>> conn.execute(stmt).fetchall()
    SELECT users_1.id, users_1.name, users_1.fullname, users_2.id,
    users_2.name, users_2.fullname
    FROM users AS users_1, users AS users_2
    WHERE users_1.name > users_2.name ORDER BY users_1.name
    ()
    [(2, u'wendy', u'Wendy Williams', 1, u'jack', u'Jack Jones')]

使用别名[¶](#using-aliases "Permalink to this headline")
--------------------------------------------------------

SQL 中的别名对应于表或 SELECT 语句的“重命名”版本，只要您说“SELECT .. FROM
sometable AS someothername”就会发生这种情况。`AS`为表格创建一个新名称。别名是一个关键结构，因为它们允许通过唯一名称引用任何表或子查询。在表格的情况下，这允许多次在 FROM 子句中命名相同的表格。在 SELECT 语句的情况下，它为由语句表示的列提供父名称，从而允许它们相对于该名称被引用。

In SQLAlchemy, any [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
construct, or other selectable can be turned into an alias using the
[`FromClause.alias()`](selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
method, which produces a [`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
construct. 举一个例子，假设我们知道我们的用户`jack`有两个特定的电子邮件地址。我们如何根据这两个地址的组合来定位插孔？为了达到这个目的，我们使用`addresses`表的一个连接，每个地址一次。我们根据`addresses`创建两个[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")结构，然后在[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构中使用它们：

    >>> a1 = addresses.alias()
    >>> a2 = addresses.alias()
    >>> s = select([users]).\
    ...        where(and_(
    ...            users.c.id == a1.c.user_id,
    ...            users.c.id == a2.c.user_id,
    ...            a1.c.email_address == 'jack@msn.com',
    ...            a2.c.email_address == 'jack@yahoo.com'
    ...        ))
    sql>>> conn.execute(s).fetchall()
    SELECT users.id, users.name, users.fullname
    FROM users, addresses AS addresses_1, addresses AS addresses_2
    WHERE users.id = addresses_1.user_id
        AND users.id = addresses_2.user_id
        AND addresses_1.email_address = ?
        AND addresses_2.email_address = ?
    ('jack@msn.com', 'jack@yahoo.com')
    [(1, u'jack', u'Jack Jones')]

请注意，[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")结构在最终的 SQL 结果中生成了名称`addresses_1`和`addresses_2`。这些名称的生成由结构在语句中的位置决定。如果我们仅使用第二个`a2`别名创建查询，则名称将以`addresses_1`出现。The generation of the names is also *deterministic*,
meaning the same SQLAlchemy statement construct will produce the
identical SQL string each time it is rendered for a particular dialect.

由于在外部，我们使用[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")构造本身来引用别名，所以我们不需要关心生成的名称。但是，出于调试的目的，可以通过将字符串名称传递给[`FromClause.alias()`](selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")方法来指定它：

    >>> a1 = addresses.alias('a1')

别名当然可以用于您可以从中进行选择的任何内容，包括 SELECT 语句本身。我们可以通过制作整个语句的别名，将`users`表自回归到我们创建的[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")。`correlate(None)`指令是为了避免 SQLAlchemy 试图将内部`users`表与外部表相关联：

    >>> a1 = s.correlate(None).alias()
    >>> s = select([users.c.name]).where(users.c.id == a1.c.id)
    sql>>> conn.execute(s).fetchall()
    SELECT users.name
    FROM users,
        (SELECT users.id AS id, users.name AS name, users.fullname AS fullname
            FROM users, addresses AS addresses_1, addresses AS addresses_2
            WHERE users.id = addresses_1.user_id AND users.id = addresses_2.user_id
            AND addresses_1.email_address = ?
            AND addresses_2.email_address = ?) AS anon_1
    WHERE users.id = anon_1.id
    ('jack@msn.com', 'jack@yahoo.com')
    [(u'jack',)]

使用连接[¶](#using-joins "Permalink to this headline")
------------------------------------------------------

我们已经能够构建任何 SELECT 表达式了。SELECT 的下一个基石是 JOIN 表达式。我们已经在我们的示例中进行了连接，只需将两个表放入[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造的 columns 子句或 where 子句中即可。但是，如果我们想要创建一个真正的“JOIN”或“OUTERJOIN”构造，我们使用[`join()`](selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")和[`outerjoin()`](selectable.html#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")方法，这些方法通常从左表访问在加入：

    >>> print(users.join(addresses))plain
    users JOIN addresses ON users.id = addresses.user_id

警报读者会看到更多惊喜；
SQLAlchemy 想出了如何加入两个表！这个连接的 ON 条件是根据我们在本教程开始的`addresses`表格路上放置的[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象自动生成的。已经`join()`结构看起来好像是连接表的更好方法。

当然，您可以加入任何您想要的表达方式，例如，如果我们想加入所有在其电子邮件地址中使用相同名称的用户名作为用户名：

    >>> print(users.join(addresses,
    ...                 addresses.c.email_address.like(users.c.name + '%')
    ...             )
    ...  )
    users JOIN addresses ON addresses.email_address LIKE (users.name || :name_1)

当我们创建一个[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造时，SQLAlchemy 会查看我们提到的表，然后将它们放在语句的 FROM 子句中。但是，当我们使用 JOIN 时，我们知道我们需要什么 FROM 子句，所以我们在这里使用[`select_from()`](selectable.html#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")方法：

    >>> s = select([users.c.fullname]).select_from(
    ...    users.join(addresses,
    ...             addresses.c.email_address.like(users.c.name + '%'))
    ...    )
    sql>>> conn.execute(s).fetchall()
    SELECT users.fullname
    FROM users JOIN addresses ON addresses.email_address LIKE (users.name || ?)
    ('%',)
    [(u'Jack Jones',), (u'Jack Jones',), (u'Wendy Williams',)]

The [`outerjoin()`](selectable.html#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
method creates `LEFT OUTER JOIN` constructs, and is
used in the same way as [`join()`](selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join"):

    >>> s = select([users.c.fullname]).select_from(users.outerjoin(addresses))
    >>> print(s)
    SELECT users.fullname
        FROM users
        LEFT OUTER JOIN addresses ON users.id = addresses.user_id

这就是输出`outerjoin()`产生的结果，当然，除非你在第 9 版之前使用 Oracle 停留在一个 gig 中，并且你已经设置了引擎（可以使用`OracleDialect`）使用 Oracle 特定的 SQL：

    >>> from sqlalchemy.dialects.oracle import dialect as OracleDialectplain
    >>> print(s.compile(dialect=OracleDialect(use_ansi=False)))
    SELECT users.fullname
    FROM users, addresses
    WHERE users.id = addresses.user_id(+)

如果您不知道 SQL 的含义，请不要担心！Oracle
DBA 的秘密部落不希望他们发现黑魔法；）。

也可以看看

[`expression.join()`](selectable.html#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")

[`expression.outerjoin()`](selectable.html#sqlalchemy.sql.expression.outerjoin "sqlalchemy.sql.expression.outerjoin")

[`Join`](selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

其他的东西[¶](#everything-else "Permalink to this headline")
------------------------------------------------------------

引入了创建 SQL 表达式的概念。剩下的是相同主题的更多变体。所以现在我们将列出我们需要知道的其他重要事情。

### 绑定参数对象[¶](#bind-parameter-objects "Permalink to this headline")

在所有这些例子中，无论文字表达式出现在哪里，SQLAlchemy 都忙于创建绑定参数。您也可以使用自己的名称指定自己的绑定参数，并重复使用相同的语句。[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构用于产生具有给定名称的绑定参数。尽管 SQLAlchemy 总是在 API 端通过名称引用绑定参数，但数据库方言在执行时会转换为适当的名称或位置样式，因为在这里它将转换为 SQLite 的位置：

    >>> from sqlalchemy.sql import bindparam
    >>> s = users.select(users.c.name == bindparam('username'))
    sql>>> conn.execute(s, username='wendy').fetchall()
    SELECT users.id, users.name, users.fullname
    FROM users
    WHERE users.name = ?
    ('wendy',)
    [(2, u'wendy', u'Wendy Williams')]

[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")的另一个重要方面是它可以被分配一个类型。bind 参数的类型将决定它在表达式中的行为，以及绑定到它的数据在被发送到数据库之前如何处理：

    >>> s = users.select(users.c.name.like(bindparam('username', type_=String) + text("'%'")))
    sql>>> conn.execute(s, username='wendy').fetchall()
    SELECT users.id, users.name, users.fullname
    FROM users
    WHERE users.name LIKE (? || '%')
    ('wendy',)
    [(2, u'wendy', u'Wendy Williams')]

[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构也可以多次使用，其中 execute 参数中只需要一个命名值：

    >>> s = select([users, addresses]).\plain
    ...     where(
    ...        or_(
    ...          users.c.name.like(
    ...                 bindparam('name', type_=String) + text("'%'")),
    ...          addresses.c.email_address.like(
    ...                 bindparam('name', type_=String) + text("'@%'"))
    ...        )
    ...     ).\
    ...     select_from(users.outerjoin(addresses)).\
    ...     order_by(addresses.c.id)
    sql>>> conn.execute(s, name='jack').fetchall()
    SELECT users.id, users.name, users.fullname, addresses.id,
        addresses.user_id, addresses.email_address
    FROM users LEFT OUTER JOIN addresses ON users.id = addresses.user_id
    WHERE users.name LIKE (? || '%') OR addresses.email_address LIKE (? || '@%')
    ORDER BY addresses.id
    ('jack', 'jack')
    [(1, u'jack', u'Jack Jones', 1, 1, u'jack@yahoo.com'), (1, u'jack', u'Jack Jones', 2, 1, u'jack@msn.com')]

也可以看看

[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")

### 功能[¶ T0\>](#functions "Permalink to this headline")

SQL 函数使用[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")关键字创建，该关键字使用属性访问生成函数：

    >>> from sqlalchemy.sql import func
    >>> print(func.now())
    now()

    >>> print(func.concat('x', 'y'))
    concat(:concat_1, :concat_2)

By “generates”, we mean that **any** SQL function is created based on
the word you choose:

    >>> print(func.xyz_my_goofy_function())
    xyz_my_goofy_function()

某些函数名由 SQLAlchemy 知道，允许应用特殊的行为规则。一些例如是“ANSI”函数，这意味着它们不会在它们后面添加括号，例如 CURRENT\_TIMESTAMP：

    >>> print(func.current_timestamp())plain
    CURRENT_TIMESTAMP

函数通常用在 select 语句的 columns 子句中，也可以标记以及给定类型。建议标记函数，以便可以根据字符串名称将结果定位到结果行中，并且在需要执行结果集处理（例如 Unicode 转换和日期转换）时需要为其分配类型。下面，我们使用结果函数`scalar()`来读取第一行的第一列，然后关闭结果；即使存在，标签在这种情况下并不重要：

    >>> conn.execute(
    ...     select([
    ...            func.max(addresses.c.email_address, type_=String).
    ...                label('maxemail')
    ...           ])
    ...     ).scalar()
    SELECT max(addresses.email_address) AS maxemail
    FROM addresses
    ()
    u'www@www.org'

支持返回整个结果集的函数的 PostgreSQL 和 Oracle 等数据库可以组合成可选单位，可用于语句中。Such
as, a database function `calculate()` which takes
the parameters `x` and `y`, and
returns three columns which we’d like to name `q`,
`z` and `r`, we can construct
using “lexical” column objects as well as bind parameters:

    >>> from sqlalchemy.sql import columnplain
    >>> calculate = select([column('q'), column('z'), column('r')]).\
    ...        select_from(
    ...             func.calculate(
    ...                    bindparam('x'),
    ...                    bindparam('y')
    ...                )
    ...             )
    >>> calc = calculate.alias()
    >>> print(select([users]).where(users.c.id > calc.c.z))
    SELECT users.id, users.name, users.fullname
    FROM users, (SELECT q, z, r
    FROM calculate(:x, :y)) AS anon_1
    WHERE users.id > anon_1.z

如果我们想要用不同的绑定参数两次使用我们的`calculate`语句，[`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")函数将为我们创建副本，并将绑定参数标记为“unique”相互冲突的名字是孤立的。请注意，我们也可以选择两个单独的别名：

    >>> calc1 = calculate.alias('c1').unique_params(x=17, y=45)
    >>> calc2 = calculate.alias('c2').unique_params(x=5, y=12)
    >>> s = select([users]).\
    ...         where(users.c.id.between(calc1.c.z, calc2.c.z))
    >>> print(s)
    SELECT users.id, users.name, users.fullname
    FROM users,
        (SELECT q, z, r FROM calculate(:x_1, :y_1)) AS c1,
        (SELECT q, z, r FROM calculate(:x_2, :y_2)) AS c2
    WHERE users.id BETWEEN c1.z AND c2.z

    >>> s.compile().params # doctest: +SKIP
    {u'x_2': 5, u'y_2': 12, u'y_1': 45, u'x_1': 17}

也可以看看

[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

### 窗口函数[¶](#window-functions "Permalink to this headline")

任何[`FunctionElement`](functions.html#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")，包括由[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")生成的函数都可以转换成一个“窗口函数”，即 OVER 子句，使用[`FunctionElement.over()`](functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over")

    >>> s = select([
    ...         users.c.id,
    ...         func.row_number().over(order_by=users.c.name)
    ...     ])
    >>> print(s)
    SELECT users.id, row_number() OVER (ORDER BY users.name) AS anon_1
    FROM users

[`FunctionElement.over()`](functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over")还支持使用[`expression.over.rows`](sqlelement.html#sqlalchemy.sql.expression.over.params.rows "sqlalchemy.sql.expression.over")或[`expression.over.range`](sqlelement.html#sqlalchemy.sql.expression.over.params.range "sqlalchemy.sql.expression.over")参数进行范围规定：

    >>> s = select([
    ...         users.c.id,
    ...         func.row_number().over(
    ...                 order_by=users.c.name,
    ...                 rows=(-2, None))
    ...     ])
    >>> print(s)
    SELECT users.id, row_number() OVER
    (ORDER BY users.name ROWS BETWEEN :param_1 PRECEDING AND UNBOUNDED FOLLOWING) AS anon_1
    FROM users

[`expression.over.rows`](sqlelement.html#sqlalchemy.sql.expression.over.params.rows "sqlalchemy.sql.expression.over")和[`expression.over.range`](sqlelement.html#sqlalchemy.sql.expression.over.params.range "sqlalchemy.sql.expression.over")均接受一个二元组，其中包含范围的负整数和正整数的组合，零表示“CURRENT
ROW”和`None`以指示“UNBOUNDED”。有关更多详细信息，请参阅[`over()`](sqlelement.html#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")上的示例。

版本 1.1 中的新功能：支持窗口函数的“行”和“范围”规范

也可以看看

[`over()`](sqlelement.html#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")

[`FunctionElement.over()`](functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over")

### 联合和其他集合操作[¶](#unions-and-other-set-operations "Permalink to this headline")

联合体有两种风格，UNION 和 UNION
ALL，它们可以通过模块级函数[`union()`](selectable.html#sqlalchemy.sql.expression.union "sqlalchemy.sql.expression.union")和[`union_all()`](selectable.html#sqlalchemy.sql.expression.union_all "sqlalchemy.sql.expression.union_all")使用：

    >>> from sqlalchemy.sql import union
    >>> u = union(
    ...     addresses.select().
    ...             where(addresses.c.email_address == 'foo@bar.com'),
    ...    addresses.select().
    ...             where(addresses.c.email_address.like('%@yahoo.com')),
    ... ).order_by(addresses.c.email_address)

    sql>>> conn.execute(u).fetchall()
    SELECT addresses.id, addresses.user_id, addresses.email_address
    FROM addresses
    WHERE addresses.email_address = ?
    UNION
    SELECT addresses.id, addresses.user_id, addresses.email_address
    FROM addresses
    WHERE addresses.email_address LIKE ? ORDER BY addresses.email_address
    ('foo@bar.com', '%@yahoo.com')
    [(1, 1, u'jack@yahoo.com')]

Also available, though not supported on all databases, are
[`intersect()`](selectable.html#sqlalchemy.sql.expression.intersect "sqlalchemy.sql.expression.intersect"),
[`intersect_all()`](selectable.html#sqlalchemy.sql.expression.intersect_all "sqlalchemy.sql.expression.intersect_all"),
[`except_()`](selectable.html#sqlalchemy.sql.expression.except_ "sqlalchemy.sql.expression.except_"),
and [`except_all()`](selectable.html#sqlalchemy.sql.expression.except_all "sqlalchemy.sql.expression.except_all"):

    >>> from sqlalchemy.sql import except_
    >>> u = except_(
    ...    addresses.select().
    ...             where(addresses.c.email_address.like('%@%.com')),
    ...    addresses.select().
    ...             where(addresses.c.email_address.like('%@msn.com'))
    ... )

    sql>>> conn.execute(u).fetchall()
    SELECT addresses.id, addresses.user_id, addresses.email_address
    FROM addresses
    WHERE addresses.email_address LIKE ?
    EXCEPT
    SELECT addresses.id, addresses.user_id, addresses.email_address
    FROM addresses
    WHERE addresses.email_address LIKE ?
    ('%@%.com', '%@msn.com')
    [(1, 1, u'jack@yahoo.com'), (4, 2, u'wendy@aol.com')]

所谓的“复合”可选项的一个常见问题是由于它们与括号嵌套的事实而产生的。特别是 SQLite 不喜欢以括号开头的语句。因此，在“化合物”中嵌套“化合物”时，如果该化合物也是化合物，通常需要将`.alias().select()`应用于最外层化合物的第一个元素。例如，要在“except\_”中嵌套“union”和“select”，SQLite 会希望将“union”声明为子查询：

    >>> u = except_(
    ...    union(
    ...         addresses.select().
    ...             where(addresses.c.email_address.like('%@yahoo.com')),
    ...         addresses.select().
    ...             where(addresses.c.email_address.like('%@msn.com'))
    ...     ).alias().select(),   # apply subquery here
    ...    addresses.select(addresses.c.email_address.like('%@msn.com'))
    ... )
    sql>>> conn.execute(u).fetchall()
    SELECT anon_1.id, anon_1.user_id, anon_1.email_address
    FROM (SELECT addresses.id AS id, addresses.user_id AS user_id,
        addresses.email_address AS email_address
        FROM addresses
        WHERE addresses.email_address LIKE ?
        UNION
        SELECT addresses.id AS id,
            addresses.user_id AS user_id,
            addresses.email_address AS email_address
        FROM addresses
        WHERE addresses.email_address LIKE ?) AS anon_1
    EXCEPT
    SELECT addresses.id, addresses.user_id, addresses.email_address
    FROM addresses
    WHERE addresses.email_address LIKE ?
    ('%@yahoo.com', '%@msn.com', '%@msn.com')
    [(1, 1, u'jack@yahoo.com')]

也可以看看

[`union()`](selectable.html#sqlalchemy.sql.expression.union "sqlalchemy.sql.expression.union")

[`union_all()`](selectable.html#sqlalchemy.sql.expression.union_all "sqlalchemy.sql.expression.union_all")

[`intersect()`](selectable.html#sqlalchemy.sql.expression.intersect "sqlalchemy.sql.expression.intersect")

[`intersect_all()`](selectable.html#sqlalchemy.sql.expression.intersect_all "sqlalchemy.sql.expression.intersect_all")

[`except_()`](selectable.html#sqlalchemy.sql.expression.except_ "sqlalchemy.sql.expression.except_")

[`except_all()`](selectable.html#sqlalchemy.sql.expression.except_all "sqlalchemy.sql.expression.except_all")

### 标量选择[¶](#scalar-selects "Permalink to this headline")

标量选择是一个只返回一行和一列的 SELECT。然后它可以用作列表达式。A scalar
select is often a [correlated
subquery](glossary.html#term-correlated-subquery), which relies upon the
enclosing SELECT statement in order to acquire at least one of its FROM
clauses.

通过调用[`as_scalar()`](selectable.html#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")或[`label()`](selectable.html#sqlalchemy.sql.expression.SelectBase.label "sqlalchemy.sql.expression.SelectBase.label")方法，可以修改[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构以充当列表达式：

    >>> stmt = select([func.count(addresses.c.id)]).\
    ...             where(users.c.id == addresses.c.user_id).\
    ...             as_scalar()

The above construct is now a [`ScalarSelect`](selectable.html#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")
object, and is no longer part of the [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
hierarchy; it instead is within the [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
family of expression constructs.
我们可以将这个结构放在另一个列的另一个列中。[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")：

    >>> conn.execute(select([users.c.name, stmt])).fetchall()plain
    SELECT users.name, (SELECT count(addresses.id) AS count_1
    FROM addresses
    WHERE users.id = addresses.user_id) AS anon_1
    FROM users
    ()
    [(u'jack', 2), (u'wendy', 2)]

要将非匿名列名应用于我们的标量选择，我们使用[`SelectBase.label()`](selectable.html#sqlalchemy.sql.expression.SelectBase.label "sqlalchemy.sql.expression.SelectBase.label")来创建它：

    >>> stmt = select([func.count(addresses.c.id)]).\plain
    ...             where(users.c.id == addresses.c.user_id).\
    ...             label("address_count")
    >>> conn.execute(select([users.c.name, stmt])).fetchall()
    SELECT users.name, (SELECT count(addresses.id) AS count_1
    FROM addresses
    WHERE users.id = addresses.user_id) AS address_count
    FROM users
    ()
    [(u'jack', 2), (u'wendy', 2)]

也可以看看

[`Select.as_scalar()`](selectable.html#sqlalchemy.sql.expression.Select.as_scalar "sqlalchemy.sql.expression.Select.as_scalar")

[`Select.label()`](selectable.html#sqlalchemy.sql.expression.Select.label "sqlalchemy.sql.expression.Select.label")

### 相关子查询[¶](#correlated-subqueries "Permalink to this headline")

请注意，在[Scalar
Selects](#scalar-selects)的示例中，每个嵌入式选择的 FROM 子句在其 FROM 子句中都不包含`users`表。这是因为 SQLAlchemy 自动将[correlates](glossary.html#term-correlates)例如：

    >>> stmt = select([addresses.c.user_id]).\
    ...             where(addresses.c.user_id == users.c.id).\
    ...             where(addresses.c.email_address == 'jack@yahoo.com')
    >>> enclosing_stmt = select([users.c.name]).where(users.c.id == stmt)
    >>> conn.execute(enclosing_stmt).fetchall()
    SELECT users.name
    FROM users
    WHERE users.id = (SELECT addresses.user_id
        FROM addresses
        WHERE addresses.user_id = users.id
        AND addresses.email_address = ?)
    ('jack@yahoo.com',)
    [(u'jack',)]

自动关联通常会做预期的事情，但它也可以被控制。例如，如果我们想要一条语句只关联`addresses`表而不关联`users`表，即使两者都出现在封闭的 SELECT 中，我们也使用[`correlate()`](selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")方法来指定那些可能相关的 FROM 子句：

    >>> stmt = select([users.c.id]).\
    ...             where(users.c.id == addresses.c.user_id).\
    ...             where(users.c.name == 'jack').\
    ...             correlate(addresses)
    >>> enclosing_stmt = select(
    ...         [users.c.name, addresses.c.email_address]).\
    ...     select_from(users.join(addresses)).\
    ...     where(users.c.id == stmt)
    >>> conn.execute(enclosing_stmt).fetchall()
    SELECT users.name, addresses.email_address
     FROM users JOIN addresses ON users.id = addresses.user_id
     WHERE users.id = (SELECT users.id
     FROM users
     WHERE users.id = addresses.user_id AND users.name = ?)
     ('jack',)
     [(u'jack', u'jack@yahoo.com'), (u'jack', u'jack@msn.com')]

要完全禁用相关的语句，我们可以传递`None`作为参数：

    >>> stmt = select([users.c.id]).\
    ...             where(users.c.name == 'wendy').\
    ...             correlate(None)
    >>> enclosing_stmt = select([users.c.name]).\
    ...     where(users.c.id == stmt)
    >>> conn.execute(enclosing_stmt).fetchall()
    SELECT users.name
     FROM users
     WHERE users.id = (SELECT users.id
      FROM users
      WHERE users.name = ?)
    ('wendy',)
    [(u'wendy',)]

我们还可以使用[`Select.correlate_except()`](selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")方法通过排除来控制关联。比如，我们可以通过告诉它关联除`users`之外的所有 FROM 子句来为`users`表写入我们的SELECT：

    >>> stmt = select([users.c.id]).\
    ...             where(users.c.id == addresses.c.user_id).\
    ...             where(users.c.name == 'jack').\
    ...             correlate_except(users)
    >>> enclosing_stmt = select(
    ...         [users.c.name, addresses.c.email_address]).\
    ...     select_from(users.join(addresses)).\
    ...     where(users.c.id == stmt)
    >>> conn.execute(enclosing_stmt).fetchall()
    SELECT users.name, addresses.email_address
     FROM users JOIN addresses ON users.id = addresses.user_id
     WHERE users.id = (SELECT users.id
     FROM users
     WHERE users.id = addresses.user_id AND users.name = ?)
     ('jack',)
     [(u'jack', u'jack@yahoo.com'), (u'jack', u'jack@msn.com')]

#### 横向关联[¶](#lateral-correlation "Permalink to this headline")

LATERAL 关联是 SQL 关联的一个特殊子类别，它允许可选单元在单个 FROM 子句中引用另一个可选单元。这是一个非常特殊的用例，虽然它是 SQL 标准的一部分，但只有最新版本的 Postgresql 才支持它。

Normally, if a SELECT statement refers to
`table1 JOIN (some SELECT) AS subquery` in its FROM
clause, the subquery on the right side may not refer to the “table1”
expression from the left side; correlation may only refer to a table
that is part of another SELECT that entirely encloses this SELECT.
LATERAL 关键字允许我们绕过这种行为，允许表达式如下：

    SELECT people.people_id, people.age, people.name
    FROM people JOIN LATERAL (SELECT books.book_id AS book_id
    FROM books WHERE books.owner_id = people.people_id)
    AS book_subq ON true

在上面，JOIN 的右侧包含一个子查询，它不仅引用“books”表，而且还引用“JOIN”左侧的“people”表。SQLAlchemy
Core 支持使用[`Select.lateral()`](selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")方法的上述语句，如下所示：

    >>> from sqlalchemy import table, column, select, true
    >>> people = table('people', column('people_id'), column('age'), column('name'))
    >>> books = table('books', column('book_id'), column('owner_id'))
    >>> subq = select([books.c.book_id]).\
    ...      where(books.c.owner_id == people.c.people_id).lateral("book_subq")
    >>> print(select([people]).select_from(people.join(subq, true())))
    SELECT people.people_id, people.age, people.name
    FROM people JOIN LATERAL (SELECT books.book_id AS book_id
    FROM books WHERE books.owner_id = people.people_id)
    AS book_subq ON true

在上面，我们可以看到[`Select.lateral()`](selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")方法与[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法非常相似，包括我们可以指定一个可选名称。然而，构造是[`Lateral`](selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")构造而不是[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")，它提供了 LATERAL 关键字以及特殊的指令，以允许从包含语句的 FROM 子句中进行关联。

[`Select.lateral()`](selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")方法通常与[`Select.correlate()`](selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")和[`Select.correlate_except()`](selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")方法交互，除了相关规则也适用于包含语句的 FROM 子句中的任何其他表。如果表被指定为[`Select.correlate()`](selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")，并且对除[`Select.correlate_except()`](selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")

版本 1.1 中的新功能：支持 LATERAL 关键字和横向关联。

也可以看看

[`Lateral`](selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")

[`Select.lateral()`](selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")

### 订购，分组，限制，偏移…… [¶](#ordering-grouping-limiting-offset-ing "Permalink to this headline")

通过将列表达式传递给`order_by()`方法来完成排序：

    >>> stmt = select([users.c.name]).order_by(users.c.name)plain
    >>> conn.execute(stmt).fetchall()
    SELECT users.name
    FROM users ORDER BY users.name
    ()
    [(u'jack',), (u'wendy',)]

可以使用[`asc()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.asc "sqlalchemy.sql.expression.ColumnElement.asc")和[`desc()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.desc "sqlalchemy.sql.expression.ColumnElement.desc")修饰符来控制升序或降序：

    >>> stmt = select([users.c.name]).order_by(users.c.name.desc())
    >>> conn.execute(stmt).fetchall()
    SELECT users.name
    FROM users ORDER BY users.name DESC
    ()
    [(u'wendy',), (u'jack',)]

分组是指 GROUP
BY 子句，通常与聚合函数结合使用以建立要聚合的行组。这是通过`group_by()`方法提供的：

    >>> stmt = select([users.c.name, func.count(addresses.c.id)]).\
    ...             select_from(users.join(addresses)).\
    ...             group_by(users.c.name)
    >>> conn.execute(stmt).fetchall()
    SELECT users.name, count(addresses.id) AS count_1
    FROM users JOIN addresses
        ON users.id = addresses.user_id
    GROUP BY users.name
    ()
    [(u'jack', 2), (u'wendy', 2)]

在应用 GROUP
BY 之后，可以使用 HAVING 过滤聚合值上的结果。它可以通过[`having()`](selectable.html#sqlalchemy.sql.expression.Select.having "sqlalchemy.sql.expression.Select.having")方法获得：

    >>> stmt = select([users.c.name, func.count(addresses.c.id)]).\
    ...             select_from(users.join(addresses)).\
    ...             group_by(users.c.name).\
    ...             having(func.length(users.c.name) > 4)
    >>> conn.execute(stmt).fetchall()
    SELECT users.name, count(addresses.id) AS count_1
    FROM users JOIN addresses
        ON users.id = addresses.user_id
    GROUP BY users.name
    HAVING length(users.name) > ?
    (4,)
    [(u'wendy', 2)]

在组合的 SELECT 语句中处理重复的常见系统是 DISTINCT 修饰符。可以使用[`Select.distinct()`](selectable.html#sqlalchemy.sql.expression.Select.distinct "sqlalchemy.sql.expression.Select.distinct")方法添加一个简单的 DISTINCT 子句：

    >>> stmt = select([users.c.name]).\
    ...             where(addresses.c.email_address.
    ...                    contains(users.c.name)).\
    ...             distinct()
    >>> conn.execute(stmt).fetchall()
    SELECT DISTINCT users.name
    FROM users, addresses
    WHERE (addresses.email_address LIKE '%%' || users.name || '%%')
    ()
    [(u'jack',), (u'wendy',)]

大多数数据库后端支持限制返回行数的系统，大多数数据库后端还具有在给定“偏移量”之后开始返回行的方法。尽管 Postgresql，MySQL 和 SQLite 等公共后端支持 LIMIT 和 OFFSET 关键字，但其他后端需要引用更多深奥的功能，例如“窗口函数”和行 ID 以达到相同的效果。[`limit()`](selectable.html#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")和[`offset()`](selectable.html#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")方法为当前后端的方法提供了一个简单的抽象：

    >>> stmt = select([users.c.name, addresses.c.email_address]).\
    ...             select_from(users.join(addresses)).\
    ...             limit(1).offset(1)
    >>> conn.execute(stmt).fetchall()
    SELECT users.name, addresses.email_address
    FROM users JOIN addresses ON users.id = addresses.user_id
     LIMIT ? OFFSET ?
    (1, 1)
    [(u'jack', u'jack@msn.com')]

插入，更新和删除[¶](#inserts-updates-and-deletes "Permalink to this headline")
------------------------------------------------------------------------------

我们已经看到本教程前面介绍的[`insert()`](selectable.html#sqlalchemy.sql.expression.TableClause.insert "sqlalchemy.sql.expression.TableClause.insert")。其中[`insert()`](selectable.html#sqlalchemy.sql.expression.TableClause.insert "sqlalchemy.sql.expression.TableClause.insert")产生INSERT，[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")方法产生 UPDATE。这两种结构都有一个名为[`values()`](dml.html#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")的方法，它指定语句的 VALUES 或 SET 子句。

[`values()`](dml.html#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")方法容纳任何列表达式作为值：

    >>> stmt = users.update().\
    ...             values(fullname="Fullname: " + users.c.name)
    >>> conn.execute(stmt)
    UPDATE users SET fullname=(? || users.name)
    ('Fullname: ',)
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

在“execute many”上下文中使用[`insert()`](selectable.html#sqlalchemy.sql.expression.TableClause.insert "sqlalchemy.sql.expression.TableClause.insert")或[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")时，我们可能还想指定在参数列表中可以引用的命名绑定参数。这两个构造会自动为执行时发送给[`execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")的字典中传递的任何列名生成绑定占位符。但是，如果我们希望使用组合表达式的显式目标命名参数，则需要使用[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构。当将[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")与[`insert()`](selectable.html#sqlalchemy.sql.expression.TableClause.insert "sqlalchemy.sql.expression.TableClause.insert")或[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")结合使用时，表格列的名称本身为“自动”绑定名称。我们可以结合使用隐式可用的绑定名称和明确命名的参数，如下例所示：

    >>> stmt = users.insert().\
    ...         values(name=bindparam('_name') + " .. name")
    >>> conn.execute(stmt, [
    ...        {'id':4, '_name':'name1'},
    ...        {'id':5, '_name':'name2'},
    ...        {'id':6, '_name':'name3'},
    ...     ])
    INSERT INTO users (id, name) VALUES (?, (? || ?))
    ((4, 'name1', ' .. name'), (5, 'name2', ' .. name'), (6, 'name3', ' .. name'))
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

使用[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")结构发出 UPDATE 语句。这很像 INSERT，除了可以指定一个额外的 WHERE 子句：

    >>> stmt = users.update().\
    ...             where(users.c.name == 'jack').\
    ...             values(name='ed')

    >>> conn.execute(stmt)
    UPDATE users SET name=? WHERE users.name = ?
    ('ed', 'jack')
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

在“executemany”上下文中使用[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")时，我们可能希望在 WHERE 子句中使用显式命名的绑定参数。同样，[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")是用于实现此目的的构造：

    >>> stmt = users.update().\
    ...             where(users.c.name == bindparam('oldname')).\
    ...             values(name=bindparam('newname'))
    >>> conn.execute(stmt, [
    ...     {'oldname':'jack', 'newname':'ed'},
    ...     {'oldname':'wendy', 'newname':'mary'},
    ...     {'oldname':'jim', 'newname':'jake'},
    ...     ])
    UPDATE users SET name=? WHERE users.name = ?
    (('ed', 'jack'), ('mary', 'wendy'), ('jake', 'jim'))
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

### 相关更新[¶](#correlated-updates "Permalink to this headline")

通过关联的更新，您可以使用另一个表或同一个表中的选择来更新表：

    >>> stmt = select([addresses.c.email_address]).\
    ...             where(addresses.c.user_id == users.c.id).\
    ...             limit(1)
    >>> conn.execute(users.update().values(fullname=stmt))
    UPDATE users SET fullname=(SELECT addresses.email_address
        FROM addresses
        WHERE addresses.user_id = users.id
        LIMIT ? OFFSET ?)
    (1, 0)
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

### 多表更新[¶](#multiple-table-updates "Permalink to this headline")

New in version 0.7.4.

Postgresql，Microsoft SQL
Server 和 MySQL 后端都支持引用多个表的 UPDATE 语句。对于 PG 和 MSSQL，这是“UPDATE
FROM”语法，它一次更新一个表，但可以在额外的“FROM”子句中引用附加表，然后可以直接在 WHERE 子句中引用该子句。在 MySQL 上，可以将多个表嵌入到由逗号分隔的单个 UPDATE 语句中。通过在 WHERE 子句中指定多个表，SQLAlchemy
[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")构造隐式支持这两种模式：

    stmt = users.update().\
            values(name='ed wood').\
            where(users.c.id == addresses.c.id).\
            where(addresses.c.email_address.startswith('ed%'))
    conn.execute(stmt)

来自上述语句的结果 SQL 将呈现为：

    UPDATE users SET name=:name FROM addressesplain
    WHERE users.id = addresses.id AND
    addresses.email_address LIKE :email_address_1 || '%%'

使用 MySQL 时，可以使用传递给[`Update.values()`](dml.html#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")的字典形式，直接在 SET 子句中为每个表分配列：

    stmt = users.update().\
            values({
                users.c.name:'ed wood',
                addresses.c.email_address:'ed.wood@foo.com'
            }).\
            where(users.c.id == addresses.c.id).\
            where(addresses.c.email_address.startswith('ed%'))

这些表在 SET 子句中显式引用：

    UPDATE users, addresses SET addresses.email_address=%s,
            users.name=%s WHERE users.id = addresses.id
            AND addresses.email_address LIKE concat(%s, '%%')

当这些结构用于不支持的数据库时，SQLAlchemy 不会做任何特殊的事情。当存在多个表时，默认情况下会生成`UPDATE FROM`语法，如果不支持此语法，则该语句将被数据库拒绝。

### 参数有序更新[¶](#parameter-ordered-updates "Permalink to this headline")

呈现 SET 子句时，[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")构造的默认行为是使用原始[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象中给出的列顺序来呈现它们。这是一个重要的行为，因为它意味着具有特定列的特定 UPDATE 语句的呈现每次都会呈现相同，这会对依赖于语句形式的查询缓存系统产生影响，客户端或服务器侧。由于参数本身作为 Python 字典键传递给[`Update.values()`](dml.html#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")方法，因此没有其他可用的固定排序。

但是，在某些情况下，UPDATE 语句的 SET 子句中呈现的参数顺序可能很重要。这个的主要例子是使用 MySQL 并提供基于其他列值的列值的更新。以下声明的最终结果：

    UPDATE some_table SET x = y + 10, y = 20plain

将有不同的结果比：

    UPDATE some_table SET y = 20, x = y + 10plain

这是因为在 MySQL 上，单独的 SET 子句在每个值的基础上被完全评估，而不是基于每行，并且每个 SET 子句被评估，嵌入在该行中的值都在变化。

为了适应这个特定的用例，可以使用[`preserve_parameter_order`(dml.html#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志。当使用这个标志时，我们为[`Update.values()`](dml.html#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")方法提供一个**2 元组的 Python 列表**作为参数。

    stmt = some_table.update(preserve_parameter_order=True).\plain
        values([(some_table.c.y, 20), (some_table.c.x, some_table.c.y + 10)])

除了它被排序之外，2 元组列表本质上与 Python 字典结构相同。使用上面的表格，我们确信，“y”列的 SET 子句将首先呈现，然后是“x”列的 SET 子句。

版本 1.0.10 中的新增功能：使用[`preserve_parameter_order`(dml.html#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志增加了对显式排序 UPDATE 参数的支持。

### 删除[¶ T0\>](#deletes "Permalink to this headline")

最后，删除。这很容易使用[`delete()`](selectable.html#sqlalchemy.sql.expression.TableClause.delete "sqlalchemy.sql.expression.TableClause.delete")结构完成：

    >>> conn.execute(addresses.delete())
    DELETE FROM addresses
    ()
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

    >>> conn.execute(users.delete().where(users.c.name > 'm'))
    DELETE FROM users WHERE users.name > ?
    ('m',)
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

### 匹配行计数[¶](#matched-row-counts "Permalink to this headline")

[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")和[`delete()`](selectable.html#sqlalchemy.sql.expression.TableClause.delete "sqlalchemy.sql.expression.TableClause.delete")都与*匹配行计数*关联。这是一个数字，表示 WHERE 子句匹配的行数。请注意，通过“匹配”，这包括没有实际发生 UPDATE 的行。该值可用于[`rowcount`](connections.html#sqlalchemy.engine.ResultProxy.rowcount "sqlalchemy.engine.ResultProxy.rowcount")：

    >>> result = conn.execute(users.delete())
    DELETE FROM users
    ()
    COMMIT
    >>> result.rowcount
    1

进一步参考[¶](#further-reference "Permalink to this headline")
--------------------------------------------------------------

表达式语言参考：[SQL Statements and Expressions
API](expression_api.html)

数据库元数据参考：[Describing Databases with MetaData](metadata.html)

引擎参考：[*Engine Configuration*](engines.html)

连接参考：[Working with Engines and Connections](connections.html)

类型参考：[Column and Data Types](types.html)
