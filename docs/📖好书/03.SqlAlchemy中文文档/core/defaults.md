---
title: 列插入/更新默认值
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/core/defaults/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
---
列插入/更新默认值[¶](#column-insert-update-defaults "Permalink to this headline")
=================================================================================

SQLAlchemy 针对在 INSERT 和 UPDATE 语句期间发生的列级事件提供了非常丰富的功能集。选项包括：

-   在 INSERT 和 UPDATE 操作期间用作默认值的标量值
-   在 INSERT 和 UPDATE 操作时执行的 Python 函数
-   INSERT 语句中嵌入的 SQL 表达式（或者在某些情况下预先执行）
-   嵌入在 UPDATE 语句中的 SQL 表达式
-   在INSERT期间使用的服务器端默认值
-   在 UPDATE 期间使用服务器端触发器的标记

所有插入/更新默认值的一般规则是，只有当特定列的值不作为`execute()`参数传递时才会生效。否则，使用给定的值。

标量默认值[¶](#scalar-defaults "Permalink to this headline")
------------------------------------------------------------

最简单的默认值是一个用作列默认值的标量值：

    Table("mytable", meta,
        Column("somecolumn", Integer, default=12)
    )

上面，如果没有提供其他值，则在INSERT期间将值“12”绑定为列值。

标量值也可能与 UPDATE 语句相关联，尽管这不是很常见（因为 UPDATE 语句通常在寻找动态默认值）：

    Table("mytable", meta,
        Column("somecolumn", Integer, onupdate=25)
    )

Python 执行的函数[¶](#python-executed-functions "Permalink to this headline")
----------------------------------------------------------------------------

[`Column.default`](metadata.html#sqlalchemy.schema.Column.params.default "sqlalchemy.schema.Column")和[`Column.onupdate`](metadata.html#sqlalchemy.schema.Column.params.onupdate "sqlalchemy.schema.Column")关键字参数也接受 Python 函数。如果没有提供该列的其他值，则在插入或更新时调用这些函数，并将返回的值用于该列的值。下面举例说明了一个粗略的“序列”，它将一个递增计数器分配给主键列：

    # a function which counts upwardsplain
    i = 0
    def mydefault():
        global i
        i += 1
        return i

    t = Table("mytable", meta,
        Column('id', Integer, primary_key=True, default=mydefault),
    )

应该注意的是，对于真正的“递增序列”行为，通常应该使用数据库的内置功能，这可能包括序列对象或其他自动增量功能。对于主键列，SQLAlchemy在大多数情况下会自动使用这些功能。有关[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的API文档，包括[`Column.autoincrement`](metadata.html#sqlalchemy.schema.Column.params.autoincrement "sqlalchemy.schema.Column")标志以及本章后面[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")中有关标准主要背景的部分密钥生成技术。

To illustrate onupdate, we assign the Python `datetime` function `now` to the
[`Column.onupdate`](metadata.html#sqlalchemy.schema.Column.params.onupdate "sqlalchemy.schema.Column")
attribute:

    import datetime

    t = Table("mytable", meta,
        Column('id', Integer, primary_key=True),

        # define 'last_updated' to be populated with datetime.now()
        Column('last_updated', DateTime, onupdate=datetime.datetime.now),
    )

当 update 语句执行并且没有为`last_updated`传递值时，将执行`datetime.datetime.now()`
Python函数并将其返回值用作`last_updated`请注意，我们现在`now`作为函数本身而不调用它（即没有下面的括号） -
SQLAlchemy将在语句执行时执行该函数。

### 上下文相关的默认函数[¶](#context-sensitive-default-functions "Permalink to this headline")

由[`Column.default`](metadata.html#sqlalchemy.schema.Column.params.default "sqlalchemy.schema.Column")和[`Column.onupdate`](metadata.html#sqlalchemy.schema.Column.params.onupdate "sqlalchemy.schema.Column")使用的 Python 函数也可以使用当前语句的上下文来确定一个值。语句的 context 是一个内部 SQLAlchemy 对象，它包含有关正在执行的语句的所有信息，包括其源表达式，与其关联的参数以及游标。与默认生成有关的上下文的典型用例是访问在该行上插入或更新的其他值。要访问上下文，请提供一个接受单个`context`参数的函数：

    def mydefault(context):plainplainplain
        return context.current_parameters['counter'] + 12

    t = Table('mytable', meta,
        Column('counter', Integer),
        Column('counter_plus_twelve', Integer, default=mydefault, onupdate=mydefault)
    )

上面我们举例说明了一个默认函数，它将为所有的 INSERT 和 UPDATE 语句执行，其中`counter_plus_twelve`的值没有被提供，并且该值将是执行`counter`列，加上数字 12。

虽然传递给默认函数的上下文对象具有许多属性，但`current_parameters`成员是仅在执行默认函数时才提供的特殊成员，用于从其现有值中派生默认值。For
a single statement that is executing many sets of bind parameters, the
user-defined function is called for each set of parameters, and
`current_parameters` will be provided with each
individual parameter set for each execution.

SQL 表达式[¶](#sql-expressions "Permalink to this headline")
-----------------------------------------------------------

“default”和“onupdate”关键字也可以通过 SQL 表达式，包括 select 语句或直接函数调用：

    t = Table("mytable", meta,
        Column('id', Integer, primary_key=True),

        # define 'create_date' to default to now()
        Column('create_date', DateTime, default=func.now()),

        # define 'key' to pull its default from the 'keyvalues' table
        Column('key', String(20), default=keyvalues.select(keyvalues.c.type='type1', limit=1)),

        # define 'last_modified' to use the current_timestamp SQL function on update
        Column('last_modified', DateTime, onupdate=func.utc_timestamp())
        )

Above, the `create_date` column will be populated
with the result of the `now()` SQL function (which,
depending on backend, compiles into `NOW()` or
`CURRENT_TIMESTAMP` in most cases) during an INSERT
statement, and the `key` column with the result of a
SELECT subquery from another table.
当为此表发出UPDATE语句时，`last_modified`列将填充`UTC_TIMESTAMP()`的值，该函数是 MySQL 特有的函数。

请注意，当使用`func`函数时，与使用 Python
datetime 函数不同，我们*do*调用函数，即括号“()” -
这是因为我们在这种情况下需要的是函数的返回值，它是将被呈现到 INSERT 或 UPDATE 语句中的 SQL 表达式结构。

上述 SQL 函数通常在执行 INSERT 或 UPDATE 语句时“inline”执行，也就是说，执行一条语句，将给定的表达式或子查询嵌入到语句的 VALUES 或 SET 子句中。尽管在某些情况下，函数在事先 SELECT 语句中“预执行”。当以下所有情况都属实时，会发生这种情况：

-   该列是主键列
-   数据库方言不支持可用的`cursor.lastrowid`存取器（或等价物）；目前包括 PostgreSQL，Oracle 和 Firebird，以及一些 MySQL 方言。
-   该方言不支持“RETURNING”子句或类似方法，或者将`implicit_returning`标志设置为`False`。支持 RETURNING 的方言目前包括 Postgresql，Oracle，Firebird 和 MS-SQL。
-   该声明是单个执行，即仅提供一组参数，并且不使用“executemany”行为
-   在[`Insert()`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update()`](dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构中未设置`inline=True`标志，并且该语句没有定义明确的 returns()子句。

除非出于性能考虑，否则默认生成子句“预执行”不是通常需要考虑的事项。

当使用一组参数执行语句（即，它不是“executemany”样式执行）时，返回的[`ResultProxy`](connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")将包含可通过[`ResultProxy.postfetch_cols()`](connections.html#sqlalchemy.engine.ResultProxy.postfetch_cols "sqlalchemy.engine.ResultProxy.postfetch_cols")其中包含具有内联执行的缺省值的所有[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的列表。Similarly,
all parameters which were bound to the statement, including all Python
and SQL expressions which were pre-executed, are present in the
[`ResultProxy.last_inserted_params()`](connections.html#sqlalchemy.engine.ResultProxy.last_inserted_params "sqlalchemy.engine.ResultProxy.last_inserted_params")
or [`ResultProxy.last_updated_params()`](connections.html#sqlalchemy.engine.ResultProxy.last_updated_params "sqlalchemy.engine.ResultProxy.last_updated_params")
collections on [`ResultProxy`](connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy").
[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")集合包含插入行的主键值列表（列表使得单列和组合列主键以相同的格式表示）。

服务器端默认值[¶](#server-side-defaults "Permalink to this headline")
---------------------------------------------------------------------

SQL 表达式默认的变体是[`Column.server_default`](metadata.html#sqlalchemy.schema.Column.params.server_default "sqlalchemy.schema.Column")，它在[`Table.create()`](metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create")操作期间被放置在 CREATE
TABLE 语句中：

    t = Table('test', meta,
        Column('abc', String(20), server_default='abc'),
        Column('created_at', DateTime, server_default=text("sysdate"))
    )

创建上述表格的调用将产生：

    CREATE TABLE test (plain
        abc varchar(20) default 'abc',
        created_at datetime default sysdate
    )

[`Column.server_default`](metadata.html#sqlalchemy.schema.Column.params.server_default "sqlalchemy.schema.Column")的行为类似于常规 SQL 默认行为；如果它放在数据库的主键列上，但没有“后取”ID 的方法，并且该语句不是“内联”的，则 SQL 表达式将被预先执行；否则，SQLAlchemy 会让数据库端的默认值正常启动。

触发列[¶](#triggered-columns "Permalink to this headline")
----------------------------------------------------------

可以使用[`FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")作为标记来调出具有由数据库触发器或其他外部过程设置的值的列：

    t = Table('test', meta,plain
        Column('abc', String(20), server_default=FetchedValue()),
        Column('def', String(20), server_onupdate=FetchedValue())
    )

更改为0.8.0b2,0.7.10版本： [`FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")上的`for_update`参数在指定为`server_onupdate`如果使用旧版本，请将上面的onupdate指定为`server_onupdate=FetchedValue(for_update=True)`。

这些标记在创建表时不会发出“default”子句，但是它们将静态的`server_default`子句设置为相同的内部标志，为高级工具提供了一个提示：“post-fetch
“应在插入或更新后执行这些行。

注意

将[`FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")与主键列结合使用通常是不恰当的，特别是在使用ORM或需要[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")属性的任何其他场景时。这是因为“post-fetch”操作要求主键值已经可用，以便可以在主键上选择该行。

对于服务器生成的主键值，所有数据库都提供特殊的访问器或其他技术来获取表的“最后插入的主键”列。这些机制不受[`FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")的影响。对于使用触发器生成主键值的特殊情况，并且正在使用的数据库不支持`RETURNING`子句，可能需要放弃使用触发器，而是应用SQL表达式或用作“预执行”表达式：

    t = Table('test', meta,
            Column('abc', MyType, default=func.generate_new_value(), primary_key=True)
    )

Where above, when [`Table.insert()`](metadata.html#sqlalchemy.schema.Table.insert "sqlalchemy.schema.Table.insert")
is used, the `func.generate_new_value()` expression
will be pre-executed in the context of a scalar `SELECT` statement, and the new value will be applied to the subsequent
`INSERT`, while at the same time being made
available to the [`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")
attribute.

定义序列[¶](#defining-sequences "Permalink to this headline")
-------------------------------------------------------------

SQLAlchemy 使用[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象表示数据库序列，这被认为是“列缺省”的特例。它只对数据库有明确的支持，这些数据库目前包括 Postgresql，Oracle 和 Firebird。[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象被忽略。

[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")可以作为 INSERT 操作期间使用的“默认”生成器放置在任何列上，也可以配置为在 UPDATE 操作期间根据需要触发。它通常与单个整数主键列结合使用：

    table = Table("cartitems", meta,plain
        Column("cart_id", Integer, Sequence('cart_id_seq'), primary_key=True),
        Column("description", String(40)),
        Column("createdate", DateTime())
    )

在上面，表“cartitems”与名为“cart\_id\_seq”的序列相关联。当针对“cartitems”发生 INSERT 语句并且没有为“cart\_id”列传递值时，将使用“cart\_id\_seq”序列来生成一个值。

当[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")与表关联时，为该表颁发的 CREATE 和 DROP 语句也将为该序列对象发出 CREATE
/ DROP，从而将序列对象与其父表“捆绑”。

[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象还实现了特殊的功能以适应 Postgresql 的 SERIAL 数据类型。PG 中的 SERIAL 类型自动生成一个在插入过程中隐式使用的序列。这意味着如果一个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象在其主键列上定义了一个[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")，以便它可以与Oracle和Firebird一起使用，那么[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")将进入 PG 通常使用的“隐式”序列的方式。对于这个用例，将标志`optional=True`添加到[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象
- 这表明仅当数据库提供时才应使用[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")没有其他选项可用于生成主键标识符。

[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象也可以像SQL表达式那样独立执行，具有调用其“下一个值”功能的效果：

    seq = Sequence('some_sequence')plainplain
    nextid = connection.execute(seq)

### 将序列关联到服务器端默认[¶](#associating-a-sequence-as-the-server-side-default "Permalink to this headline")

当我们如上所述将[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")与[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")相关联时，此关联仅为**in-Python
only**关联。将为我们的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")生成的 CREATE
TABLE 不会引用此序列。如果我们希望将序列用作服务器端缺省值，即使我们从 SQL 命令行向表中发出 INSERT 命令，也可以使用[`Column.server_default`](metadata.html#sqlalchemy.schema.Column.params.server_default "sqlalchemy.schema.Column")参数与序列的值生成函数一起使用，可以从[`Sequence.next_value()`](#sqlalchemy.schema.Sequence.next_value "sqlalchemy.schema.Sequence.next_value")方法获得：

    cart_id_seq = Sequence('cart_id_seq')
    table = Table("cartitems", meta,
        Column(
            "cart_id", Integer, cart_id_seq,
            server_default=cart_id_seq.next_value(), primary_key=True),
        Column("description", String(40)),
        Column("createdate", DateTime())
    )

上面的元数据将在 Postgresql 上生成一个 CREATE TABLE 语句，如下所示：

    CREATE TABLE cartitems (
        cart_id INTEGER DEFAULT nextval('cart_id_seq') NOT NULL,
        description VARCHAR(40),
        createdate TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (cart_id)
    )

我们把[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")也作为Python的默认值放在上面，也就是说，它在[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")定义中提到了两次。根据所使用的后端，这可能不是严格必要的，例如在 Postgresql 后端，Core 将使用`RETURNING`访问新生成的主键值。However, for the best compatibility,
[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence") was
originally intended to be a Python-side directive first and foremost so
it’s probably a good idea to specify it in this way as well.

默认对象API [¶](#default-objects-api "Permalink to this headline")
------------------------------------------------------------------

*class* `sqlalchemy.schema。`{.descclassname} `ColumnDefault`{.descname} （ *arg*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.ColumnDefault "Permalink to this definition")*
:   基础：[`sqlalchemy.schema.DefaultGenerator`](#sqlalchemy.schema.DefaultGenerator "sqlalchemy.schema.DefaultGenerator")

    列上的普通默认值。

    这可以对应于常量，可调用函数或SQL子句。

    [`ColumnDefault`](#sqlalchemy.schema.ColumnDefault "sqlalchemy.schema.ColumnDefault")
    is generated automatically whenever the `default`, `onupdate` arguments of
    [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    are used. 一个[`ColumnDefault`](#sqlalchemy.schema.ColumnDefault "sqlalchemy.schema.ColumnDefault")也可以在位置上传递。

    例如，以下内容：

        Column('foo', Integer, default=50)

    相当于：

        Column('foo', Integer, ColumnDefault(50))

 *class*`sqlalchemy.schema.`{.descclassname}`DefaultClause`{.descname}(*arg*, *for\_update=False*, *\_reflected=False*)[¶](#sqlalchemy.schema.DefaultClause "Permalink to this definition")
:   基础：[`sqlalchemy.schema.FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")

    DDL指定的DEFAULT列值。plain

    [`DefaultClause`](#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")
    is a [`FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")
    that also generates a “DEFAULT” clause when “CREATE TABLE” is
    emitted.

    [`DefaultClause`](#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")
    is generated automatically whenever the `server_default`, `server_onupdate` arguments of
    [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    are used. 一个[`DefaultClause`](#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")也可以在位置上传递。

    例如，以下内容：

        Column('foo', Integer, server_default="50")

    相当于：

        Column('foo', Integer, DefaultClause("50"))

*class* `sqlalchemy.schema。`{.descclassname} `DefaultGenerator`{.descname} （ *for\_update = False* / T5\> [¶ T6\>](#sqlalchemy.schema.DefaultGenerator "Permalink to this definition")
:   基础：`sqlalchemy.schema._NotAColumnExpr`，[`sqlalchemy.schema.SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

    列*默认*值的基类。

*类 T0\> `sqlalchemy.schema。 T1>  FetchedValue  T2> （ T3>  FOR_UPDATE =假 T4> ）< / T5> ¶ T6>`{.descclassname}*
:   基础：`sqlalchemy.schema._NotAColumnExpr`，`sqlalchemy.sql.expression.SchemaEventTarget`

    透明数据库默认的标记。plain

    当数据库配置为为列提供一些自动默认值时，使用[`FetchedValue`](#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")。

    例如。：

        Column('foo', Integer, FetchedValue())

    将指出某个触发器或默认生成器将在INSERT期间为`foo`列创建新值。

    也可以看看

    [Triggered Columns](#triggered-columns)

*class* `sqlalchemy.schema。`{.descclassname} `PassiveDefault`{.descname} （ *\* arg*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.PassiveDefault "Permalink to this definition")*
:   基础：[`sqlalchemy.schema.DefaultClause`](#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")

    DDL指定的DEFAULT列值。

    从版本0.6开始弃用： [`PassiveDefault`](#sqlalchemy.schema.PassiveDefault "sqlalchemy.schema.PassiveDefault")已弃用。使用[`DefaultClause`](#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")。

 *class*`sqlalchemy.schema.`{.descclassname}`Sequence`{.descname}(*name*, *start=None*, *increment=None*, *minvalue=None*, *maxvalue=None*, *nominvalue=None*, *nomaxvalue=None*, *cycle=None*, *schema=None*, *optional=False*, *quote=None*, *metadata=None*, *quote\_schema=None*, *for\_update=False*)[¶](#sqlalchemy.schema.Sequence "Permalink to this definition")
:   基础：[`sqlalchemy.schema.DefaultGenerator`](#sqlalchemy.schema.DefaultGenerator "sqlalchemy.schema.DefaultGenerator")

    表示一个命名的数据库序列。

    [`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象表示数据库序列的名称和配置参数。它还表示一个可以由SQLAlchemy
    [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")执行的构造，为目标数据库呈现适当的“下一个值”函数并返回结果。

    [`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")通常与主键列关联：

        some_table = Table(
            'some_table', metadata,
            Column('id', Integer, Sequence('some_table_seq'),
            primary_key=True)
        )

    当针对上述[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")发出CREATE
    TABLE时，如果目标平台支持序列，则也会发出CREATE
    SEQUENCE语句。对于不支持序列的平台，忽略[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")结构。

    也可以看看

    [`CreateSequence`](ddl.html#sqlalchemy.schema.CreateSequence "sqlalchemy.schema.CreateSequence")

    [`DropSequence`](ddl.html#sqlalchemy.schema.DropSequence "sqlalchemy.schema.DropSequence")

     `__init__`{.descname}(*name*, *start=None*, *increment=None*, *minvalue=None*, *maxvalue=None*, *nominvalue=None*, *nomaxvalue=None*, *cycle=None*, *schema=None*, *optional=False*, *quote=None*, *metadata=None*, *quote\_schema=None*, *for\_update=False*)[¶](#sqlalchemy.schema.Sequence.__init__ "Permalink to this definition")
    :   构建一个[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")对象。

        参数：

        -   **名称** [¶](#sqlalchemy.schema.Sequence.params.name) -
            序列的名称。
        -   **开始** [¶](#sqlalchemy.schema.Sequence.params.start) -
            序列的起始索引。当CREATE SEQUENCE命令作为“START
            WITH”子句的值发送到数据库时使用此值。如果`None`，则省略该子句，在大多数平台上该子句指示起始值为1。
        -   **增量** [¶](#sqlalchemy.schema.Sequence.params.increment) -
            序列的增量值。当CREATE SEQUENCE命令作为“INCREMENT
            BY”子句的值发送到数据库时使用此值。如果`None`，则该子句被省略，在大多数平台上该子句指示增量为1。
        -   **minvalue**
            [¶](#sqlalchemy.schema.Sequence.params.minvalue) -

            序列的最小值。当CREATE
            SEQUENCE命令作为“MINVALUE”子句的值发送到数据库时使用此值。如果`None`，则该子句被省略，在大多数平台上该子句分别指示升序和降序序列的最小值为1和-2
            \^ 63-1。

            版本1.0.7中的新功能

        -   **maxvalue**
            [¶](#sqlalchemy.schema.Sequence.params.maxvalue) -

            序列的最大值。当CREATE
            SEQUENCE命令作为“MAXVALUE”子句的值发送到数据库时使用此值。如果`None`，则省略该子句，它在大多数平台上分别指示升序和降序序列的最大值为2
            \^ 63-1和-1。

            版本1.0.7中的新功能

        -   **nominvalue**
            [¶](#sqlalchemy.schema.Sequence.params.nominvalue) -

            没有最小值的序列。当CREATE SEQUENCE命令作为“NO
            MINVALUE”子句的值发送到数据库时使用此值。如果`None`，则该子句被省略，在大多数平台上该子句分别指示升序和降序序列的最小值为1和-2
            \^ 63-1。

            版本1.0.7中的新功能

        -   **nomaxvalue**
            [¶](#sqlalchemy.schema.Sequence.params.nomaxvalue) -

            没有最大值的序列。当将CREATE SEQUENCE命令作为“NO
            MAXVALUE”子句的值发送到数据库时使用此值。如果`None`，则省略该子句，它在大多数平台上分别指示升序和降序序列的最大值为2
            \^ 63-1和-1。

            版本1.0.7中的新功能

        -   **循环** [¶](#sqlalchemy.schema.Sequence.params.cycle) -

            允许序列在分别以升序或降序达到最大值或最小值时回绕。当CREATE
            SEQUENCE命令作为“CYCLE”子句发送到数据库时使用此值。如果达到限制，则生成的下一个数字将分别为minvalue或maxvalue。如果cycle
            =
            False（默认值），则在序列达到其最大值后对nextval的任何调用将返回一个错误。

            版本1.0.7中的新功能

        -   **schema**[¶](#sqlalchemy.schema.Sequence.params.schema) –
            Optional schema name for the sequence, if located in a
            schema other than the default. 当[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")出现时选择模式名称的规则与[`Table.schema`](metadata.html#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")的规则相同。
        -   **optional**[¶](#sqlalchemy.schema.Sequence.params.optional)
            – boolean value, when `True`, indicates
            that this [`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")
            object only needs to be explicitly generated on backends
            that don’t provide another way to generate primary key
            identifiers.
            目前，它基本上意味着“不要在Postgresql后端创建这个序列，SERIAL关键字会自动为我们创建一个序列”。
        -   **quote**[¶](#sqlalchemy.schema.Sequence.params.quote) –
            boolean value, when `True` or
            `False`, explicitly forces quoting of
            the schema name on or off. 如果保留为`None`的默认值，则会发生基于大括号和保留字的正常引用规则。
        -   **quote\_schema**[¶](#sqlalchemy.schema.Sequence.params.quote_schema)
            – set the quoting preferences for the `schema` name.
        -   **元数据** [¶](#sqlalchemy.schema.Sequence.params.metadata)
            -

            可选的[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象，它将与此[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")关联。A
            [`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")
            that is associated with a [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
            gains access to the `bind` of that
            [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData"),
            meaning the [`Sequence.create()`](#sqlalchemy.schema.Sequence.create "sqlalchemy.schema.Sequence.create")
            and [`Sequence.drop()`](#sqlalchemy.schema.Sequence.drop "sqlalchemy.schema.Sequence.drop")
            methods will make usage of that engine automatically.

            版本0.7更改：此外，当[`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")时，相应的[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")将会发出相应的CREATE
            SEQUENCE / DROP SEQUENCE
            DDL命令和[`MetaData.drop_all()`](metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")被调用。

            请注意，当一个[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")应用于[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")时，[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")会自动与该元素的[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象关联列的父[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，当该关联时。The
            [`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")
            will then be subject to automatic CREATE SEQUENCE/DROP
            SEQUENCE corresponding to when the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            object itself is created or dropped, rather than that of the
            [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
            object overall.

        -   **for\_update**[¶](#sqlalchemy.schema.Sequence.params.for_update)
            – Indicates this [`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence"),
            when associated with a [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
            should be invoked for UPDATE statements on that column’s
            table, rather than for INSERT statements, when no value is
            otherwise present for that column in the statement.

     `create`{.descname}(*bind=None*, *checkfirst=True*)[¶](#sqlalchemy.schema.Sequence.create "Permalink to this definition")
    :   在数据库中创建这个序列。

     `drop`{.descname}(*bind=None*, *checkfirst=True*)[¶](#sqlalchemy.schema.Sequence.drop "Permalink to this definition")
    :   从数据库中删除这个序列。

    ` next_value  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回一个[`next_value`](functions.html#sqlalchemy.sql.functions.next_value "sqlalchemy.sql.functions.next_value")函数元素，该元素将为任何SQL表达式中的[`Sequence`](#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")提供适当的增量函数。


