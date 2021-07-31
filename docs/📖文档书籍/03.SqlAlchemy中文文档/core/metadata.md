---
title: 用 MetaData 描述数据库
date: 2021-02-20 22:41:35
permalink: /sqlalchemy/core/metadata/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
用 MetaData 描述数据库[¶](#module-sqlalchemy.schema "Permalink to this headline")
===============================================================================

本节讨论基本的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")和[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象。

元数据实体的集合存储在一个名为[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")的对象中：

    from sqlalchemy import *plain

    metadata = MetaData()

[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData") is
a container object that keeps together many different features of a
database (or multiple databases) being described.

要表示表，请使用[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")类。它的两个主要参数是表名，然后是它将与之关联的[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象。其余的位置参数大多是描述每列的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象：

    user = Table('user', metadata,plainplainplainplainplain
        Column('user_id', Integer, primary_key=True),
        Column('user_name', String(16), nullable=False),
        Column('email_address', String(60)),
        Column('password', String(20), nullable=False)
    )

以上描述了一个名为`user`的表格，其中包含四列。该表的主键由`user_id`列组成。多列可以分配`primary_key=True`标志，表示多列主键，称为*复合*主键。

还要注意，每列使用对应于泛型类型的对象来描述它的数据类型，比如[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")和[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")。SQLAlchemy 具有数十种不同级别的特异性以及创建自定义类型的能力。关于类型系统的文档可以在[Column
and Data Types](types.html)中找到。

访问表和列[¶](#accessing-tables-and-columns "Permalink to this headline")
-------------------------------------------------------------------------

The [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
object contains all of the schema constructs we’ve associated with it.
它支持访问这些表对象的几种方法，例如按照外键依赖的顺序返回每个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象列表的`sorted_tables`访问器（也就是说，每个表在它引用的所有表之前）：

    >>> for t in metadata.sorted_tables:plainplain
    ...    print(t.name)
    user
    user_preference
    invoice
    invoice_item

在大多数情况下，单个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象已被显式声明，并且这些对象通常作为应用程序中的模块级变量直接访问。一旦定义了[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，它就有一整套访问器，允许检查其属性。给定以下[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")定义：

    employees = Table('employees', metadata,plainplainplainplain
        Column('employee_id', Integer, primary_key=True),
        Column('employee_name', String(60), nullable=False),
        Column('employee_dept', Integer, ForeignKey("departments.department_id"))
    )

请注意此表中使用的[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象
- 此构造定义了对远程表的引用，并在[Defining Foreign
Keys](constraints.html#metadata-foreignkeys)中进行了完整描述。访问关于此表的信息的方法包括：

    # access the column "EMPLOYEE_ID":plainplainplainplain
    employees.columns.employee_id

    # or just
    employees.c.employee_id

    # via string
    employees.c['employee_id']

    # iterate through all columns
    for c in employees.c:
        print(c)

    # get the table's primary key columns
    for primary_key in employees.primary_key:
        print(primary_key)

    # get the table's foreign key objects:
    for fkey in employees.foreign_keys:
        print(fkey)

    # access the table's MetaData:
    employees.metadata

    # access the table's bound Engine or Connection, if its MetaData is bound:
    employees.bind

    # access a column's name, type, nullable, primary key, foreign key
    employees.c.employee_id.name
    employees.c.employee_id.type
    employees.c.employee_id.nullable
    employees.c.employee_id.primary_key
    employees.c.employee_dept.foreign_keys

    # get the "key" of a column, which defaults to its name, but can
    # be any user-defined string:
    employees.c.employee_name.key

    # access a column's table:
    employees.c.employee_id.table is employees

    # get the table related by a foreign key
    list(employees.c.employee_dept.foreign_keys)[0].column.table

创建和删除数据库表[¶](#creating-and-dropping-database-tables "Permalink to this headline")
------------------------------------------------------------------------------------------

Once you’ve defined some [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table") objects,
assuming you’re working with a brand new database one thing you might
want to do is issue CREATE statements for those tables and their related
constructs (as an aside, it’s also quite possible that you *don’t* want
to do this, if you already have some preferred methodology such as tools
included with your database or an existing scripting system - if that’s
the case, feel free to skip this section - SQLAlchemy has no requirement
that it be used to create your tables).

发布 CREATE 的常用方法是在[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象上使用[`create_all()`](#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")。这种方法将发出查询，首先检查每个单独表的存在，如果未找到，将发出 CREATE 语句：

>     engine = create_engine('sqlite:///:memory:')plainplain
>
>     metadata = MetaData()
>
>     user = Table('user', metadata,
>         Column('user_id', Integer, primary_key=True),
>         Column('user_name', String(16), nullable=False),
>         Column('email_address', String(60), key='email'),
>         Column('password', String(20), nullable=False)
>     )
>
>     user_prefs = Table('user_prefs', metadata,
>         Column('pref_id', Integer, primary_key=True),
>         Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
>         Column('pref_name', String(40), nullable=False),
>         Column('pref_value', String(100))
>     )
>
>     sqlmetadata.create_all(engine)
>     PRAGMA table_info(user){}
>     CREATE TABLE user(
>             user_id INTEGER NOT NULL PRIMARY KEY,
>             user_name VARCHAR(16) NOT NULL,
>             email_address VARCHAR(60),
>             password VARCHAR(20) NOT NULL
>     )
>     PRAGMA table_info(user_prefs){}
>     CREATE TABLE user_prefs(
>             pref_id INTEGER NOT NULL PRIMARY KEY,
>             user_id INTEGER NOT NULL REFERENCES user(user_id),
>             pref_name VARCHAR(40) NOT NULL,
>             pref_value VARCHAR(100)
>     )

[`create_all()`](#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
creates foreign key constraints between tables usually inline with the
table definition itself, and for this reason it also generates the
tables in order of their dependency.
有些选项可以改变这种行为，例如使用`ALTER TABLE`。

使用[`drop_all()`](#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")方法类似地实现删除所有表。这个方法与[`create_all()`](#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")完全相反
- 首先检查每个表的存在，并且按照与依赖性相反的顺序删除表。

可以通过[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的`create()`和`drop()`方法创建和删除单个表。这些方法默认发出 CREATE 或 DROP，而不管表是否存在：

    engine = create_engine('sqlite:///:memory:')plainplain

    meta = MetaData()

    employees = Table('employees', meta,
        Column('employee_id', Integer, primary_key=True),
        Column('employee_name', String(60), nullable=False, key='name'),
        Column('employee_dept', Integer, ForeignKey("departments.department_id"))
    )
    sqlemployees.create(engine)
    CREATE TABLE employees(
    employee_id SERIAL NOT NULL PRIMARY KEY,
    employee_name VARCHAR(60) NOT NULL,
    employee_dept INTEGER REFERENCES departments(department_id)
    )
    {}

`drop()`方法：

    sqlemployees.drop(engine)plainplain
    DROP TABLE employees
    {}

要启用“首先检查表存在”逻辑，请将`checkfirst=True`参数添加到`create()`或`drop()`：

    employees.create(engine, checkfirst=True)plain
    employees.drop(engine, checkfirst=False)

通过迁移改变模式[¶](#altering-schemas-through-migrations "Permalink to this headline")
--------------------------------------------------------------------------------------

尽管 SQLAlchemy 直接支持为模式构造发出 CREATE 和 DROP 语句，但通常通过 ALTER 语句以及其他特定于数据库的构造来更改这些构造的能力超出了 SQLAlchemy 本身的范围。虽然很容易通过传递字符串到[`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")或通过使用[`DDL`](ddl.html#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL")构造来手动发出 ALTER 语句和类似事件，但这是常见的做法使用模式迁移工具自动维护与应用程序代码相关的数据库模式。

有两种可用于 SQLAlchemy 的主要迁移工具：

-   [Alembic](http://alembic.zzzcomputing.com) - Written by the author
    of SQLAlchemy, Alembic features a highly customizable environment
    and a minimalistic usage pattern, supporting such features as
    transactional DDL, automatic generation of “candidate” migrations,
    an “offline” mode which generates SQL scripts, and support for
    branch resolution.
-   [SQLAlchemy-Migrate](https://github.com/openstack/sqlalchemy-migrate)
    - The original migration tool for SQLAlchemy, SQLAlchemy-Migrate is
    widely used and continues under active development.
    SQLAlchemy-Migrate 包含 SQL 脚本生成，ORM 类生成，ORM 模型比较以及对 SQLite 迁移的广泛支持等功能。

指定模式名称[¶](#specifying-the-schema-name "Permalink to this headline")
-------------------------------------------------------------------------

一些数据库支持多个模式的概念。一个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")可以通过指定`schema`关键字参数来引用：

    financial_info = Table('financial_info', meta,plain
        Column('id', Integer, primary_key=True),
        Column('value', String(100), nullable=False),
        schema='remote_banks'
    )

在[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")集合中，此表将由`financial_info`和`remote_banks`的组合标识。如果另一个名为`financial_info`的表在没有`remote_banks`模式的情况下被引用，它将引用另一个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
objects can specify references to columns in this table using the form
`remote_banks.financial_info.id`.

`schema`参数应该用于任何所需的名称限定符，包括 Oracle 的“所有者”属性和类似名称。它也可以容纳更长方案的虚线名称：

    schema="dbo.scott"plainplainplain

后端特定选项[¶](#backend-specific-options "Permalink to this headline")
-----------------------------------------------------------------------

[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")支持特定于数据库的选项。例如，MySQL 有不同的表后端类型，包括“MyISAM”和“InnoDB”。这可以用[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")用`mysql_engine`来表示：

    addresses = Table('engine_email_addresses', meta,plainplainplainplain
        Column('address_id', Integer, primary_key=True),
        Column('remote_user_id', Integer, ForeignKey(users.c.user_id)),
        Column('email_address', String(20)),
        mysql_engine='InnoDB'
    )

其他后端也可以支持表级别的选项 -
这些将在每个方言的单个文档部分进行描述。

Column，Table，MetaData API [¶](#column-table-metadata-api "Permalink to this headline")
----------------------------------------------------------------------------------------

`sqlalchemy.schema。 T0>  BLANK_SCHEMA  T1> ¶ T2>`{.descclassname}
:   Symbol indicating that a [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table") or
    [`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")
    should have ‘None’ for its schema, even if the parent
    [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    has specified a schema.

    也可以看看plainplainplainplain

    [`MetaData.schema`](#sqlalchemy.schema.MetaData.params.schema "sqlalchemy.schema.MetaData")

    [`Table.schema`](#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")

    [`Sequence.schema`](defaults.html#sqlalchemy.schema.Sequence.params.schema "sqlalchemy.schema.Sequence")

    版本1.0.14中的新功能

*class* `sqlalchemy.schema。`{.descclassname} `列`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.Column "Permalink to this definition")*
:   基础：[`sqlalchemy.schema.SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")，[`sqlalchemy.sql.expression.ColumnClause`](sqlelement.html#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")

    表示数据库表中的列。plain

    ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`__eq__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实施`==`运算符。

        在列上下文中，生成子句`a = b`。If the target
        is `None`, produces `a IS NULL`.

    `__ init __`{.descname} （ *\* args*，*\*\* kwargs* ） [T5\>](#sqlalchemy.schema.Column.__init__ "Permalink to this definition")
    :   构建一个新的`Column`对象。

        参数：

        -   **名称** [¶](#sqlalchemy.schema.Column.params.name) -

            数据库中表示的该列的名称。该参数可能是第一个位置参数，或通过关键字指定。

            不包含大写字母的名称将被视为不区分大小写的名称，除非是保留字，否则不会被引用。任何数量的大写字符的名称都将被引用并准确发送。请注意，即使对于将大写名称标准化为不区分大小写的数据库（如Oracle），此行为也适用。

            名称字段在构建时可以省略，并在列与[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")关联之前随时应用。这是为了支持[`declarative`](orm_extensions_declarative_api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")扩展中的方便用法。

        -   **type \_** [¶](#sqlalchemy.schema.Column.params.type_) -

            列的类型，使用子类型为[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")的实例指示。如果该类型不需要参数，则类型的类也可以发送，例如：

                # use a type with arguments
                Column('data', String(50))

                # use no arguments
                Column('level', Integer)

            `type`参数可以是第二个位置参数或由关键字指定。

            如果`type`为`None`或省略，它将首先默认为特殊类型[`NullType`](type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")。如果使用[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")和/或[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")使[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")引用另一列，则远程引用列的类型将为复制到此列，此时外键已针对该远程[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象解析。

            版本0.9.0更改：支持从[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象将类型传播到[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")进行了改进，应该更加可靠和及时。

        -   **\*args**[¶](#sqlalchemy.schema.Column.params.*args) –
            Additional positional arguments include various
            [`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")
            derived constructs which will be applied as options to the
            column. 这些包括[`Constraint`](constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")，[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")，[`ColumnDefault`](defaults.html#sqlalchemy.schema.ColumnDefault "sqlalchemy.schema.ColumnDefault")和[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")的实例。在某些情况下，可以使用等效的关键字参数，如`server_default`，`default`和`unique`。
        -   **autoincrement**
            [¶](#sqlalchemy.schema.Column.params.autoincrement) -

            为整数主键列设置“自动增量”语义。缺省值是字符串`"auto"`，它表示没有声明客户端或python端缺省值的INTEGER类型的单列主键应该自动接收自动增量语义；所有其他品种的主键列都不会。这包括在创建表的过程中为这个列发出诸如Postgresql
            SERIAL或MySQL
            AUTO\_INCREMENT之类的[DDL](glossary.html#term-ddl)，以及当INSERT语句调用哪一列时，该列被假定为生成新的整数主键值将由方言检索。

            该标志可以设置为`True`以指示作为组合（例如多列）主键的一部分的列应该具有自动增量语义，尽管注意到主键内只有一列可能具有这个设置。也可以将它设置为`True`以在具有客户端或服务器端默认配置的列上指示自动增量语义，但请注意，并非所有方言都可以将所有默认样式作为“自动增量”。对于具有INTEGER数据类型的单列主键，也可以将其设置为`False`，以禁用该列的自动增量语义。

            在版本1.1中更改：
            autoincrement标志现在默认为`"auto"`，仅指示单列整数主键的默认自动增量语义；对于复合（多列）主键，自动增量永远不会隐式启用；像往常一样，`autoincrement=True`最多只允许其中一列为“自动增量”列。`autoincrement=True`也可以在具有显式客户端或服务器端默认值的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")上设置，但要受到后端数据库和方言的限制。

            仅*设置*对于以下列的列有效：

            -   整数派生（即INT，SMALLINT，BIGINT）。
            -   主键的一部分
            -   除非值指定为`'ignore_fk'`，否则不能通过[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")引用另一列：

                    # turn on autoincrement for this column despite
                    # the ForeignKey()
                    Column('id', ForeignKey('other.id'),
                                primary_key=True, autoincrement='ignore_fk')

                在通过外键引用另一列的列上启用“自动增量”通常是不可取的，因为这样的列需要引用源自其他地方的值。

            该设置对满足上述标准的列有这两个影响：

            -   为该列发布的DDL将包含旨在将此列表示为“自动增量”列的特定于数据库的关键字，如MySQL上的AUTO
                INCREMENT，PostgreSQL上的SERIAL和MS-SQL上的IDENTITY。It
                does *not* issue AUTOINCREMENT for SQLite since this is
                a special SQLite flag that is not required for
                autoincrementing behavior.

                也可以看看

                [SQLite Auto Incrementing
                Behavior](dialects_sqlite.html#sqlite-autoincrement)

            -   该列将被视为可用于使用特定于后端数据库的“autoincrement”方法，例如调用`cursor.lastrowid`，使用INSERT语句中的RETURNING获取序列生成的值，或者使用诸如“SELECT
                scope\_identity()”之类的特殊函数。这些方法对于使用的DBAPI和数据库非常具体，并且差别很大，因此在将`autoincrement=True`与自定义默认生成函数关联时应该小心。

        -   **默认** [¶](#sqlalchemy.schema.Column.params.default) -

            表示此列的*默认值*的标量，Python可调用或[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")表达式，在插入时调用此方法，如果此列在其中的VALUES子句中未指定插。这是使用[`ColumnDefault`](defaults.html#sqlalchemy.schema.ColumnDefault "sqlalchemy.schema.ColumnDefault")作为位置参数的捷径；请参阅该类，以获取关于参数结构的完整细节。

            将此参数与[`Column.server_default`](#sqlalchemy.schema.Column.params.server_default "sqlalchemy.schema.Column")对比，这会在数据库端创建一个默认生成器。

            也可以看看

            [Column Insert/Update Defaults](defaults.html)

        -   **doc**[¶](#sqlalchemy.schema.Column.params.doc) – optional
            String that can be used by the ORM or similar to document
            attributes.
            此属性不会呈现SQL注释（将来的属性“注释”将实现该注释）。
        -   **key**[¶](#sqlalchemy.schema.Column.params.key) – An
            optional string identifier which will identify this
            `Column` object on the [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table").
            当提供密钥时，这是在应用程序中引用`Column`的唯一标识符，包括ORM属性映射； `name`字段仅在呈现SQL时使用。
        -   **index**[¶](#sqlalchemy.schema.Column.params.index) – When
            `True`, indicates that the column is
            indexed. 这是在表上使用[`Index`](constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构的快捷方式。要指定具有显式名称的索引或包含多列的索引，请改用[`Index`](constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构。
        -   **info**[¶](#sqlalchemy.schema.Column.params.info) –
            Optional data dictionary which will be populated into the
            [`SchemaItem.info`](#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
            attribute of this object.
        -   **nullable**[¶](#sqlalchemy.schema.Column.params.nullable) –
            If set to the default of `True`,
            indicates the column will be rendered as allowing NULL, else
            it’s rendered as NOT NULL. 此参数仅在发出CREATE
            TABLE语句时使用。
        -   **onupdate**[¶](#sqlalchemy.schema.Column.params.onupdate) –
            A scalar, Python callable, or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            representing a default value to be applied to the column
            within UPDATE statements, which wil be invoked upon update
            if this column is not present in the SET clause of the
            update. 这是使用[`ColumnDefault`](defaults.html#sqlalchemy.schema.ColumnDefault "sqlalchemy.schema.ColumnDefault")作为`for_update=True`的位置参数的快捷方式。
        -   **primary\_key**[¶](#sqlalchemy.schema.Column.params.primary_key)
            – If `True`, marks this column as a
            primary key column.
            多列可以将此标志设置为指定复合主键。作为替代方案，可以通过明确的[`PrimaryKeyConstraint`](constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")对象指定[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的主键。
        -   **server\_default**
            [¶](#sqlalchemy.schema.Column.params.server_default) -

            表示列的DDL DEFAULT值的[`FetchedValue`](defaults.html#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")实例，str，Unicode或[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构。

            字符串类型将按原样发出，并由单引号括起来：

                Column('x', Text, server_default="val")

                x TEXT DEFAULT 'val'

            一个[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")表达式将按原样呈现，不带引号：

                Column('y', DateTime, server_default=text('NOW()'))

                y DATETIME DEFAULT NOW()

            初始化时，字符串和文本()将被转换为[`DefaultClause`](defaults.html#sqlalchemy.schema.DefaultClause "sqlalchemy.schema.DefaultClause")对象。

            使用[`FetchedValue`](defaults.html#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")来指示已存在的列将在数据库端生成一个默认值，SQLAlchemy将在插入后提供用于后取回的默认值。该构造不指定任何DDL，并且实现留给数据库，例如通过触发器。

            也可以看看

            [Server Side Defaults](defaults.html#server-defaults)

        -   **server\_onupdate**[¶](#sqlalchemy.schema.Column.params.server_onupdate)
            – A [`FetchedValue`](defaults.html#sqlalchemy.schema.FetchedValue "sqlalchemy.schema.FetchedValue")
            instance representing a database-side default generation
            function.
            这向SQLAlchemy表明，在更新后新生成的值将可用。该构造不指定任何DDL，并且实现留给数据库，例如通过触发器。
        -   **quote**[¶](#sqlalchemy.schema.Column.params.quote) – Force
            quoting of this column’s name on or off, corresponding to
            `True` or `False`.
            当它保留默认值`None`时，列标识符将根据名称是否区分大小写（带有至少一个大写字符的标识符视为区分大小写）或者是保留字。该标志仅用于强制引用SQLAlchemy方言未知的保留字。
        -   **unique**[¶](#sqlalchemy.schema.Column.params.unique) –
            When `True`, indicates that this column
            contains a unique constraint, or if `index` is `True` as well, indicates
            that the [`Index`](constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
            should be created with the unique flag.
            要在约束/索引中指定多个列或指定显式名称，请明确使用[`UniqueConstraint`](constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")或[`Index`](constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构。
        -   **系统** [¶](#sqlalchemy.schema.Column.params.system) -

            当`True`时，表示这是一个“系统”列，即数据库自动提供的一列，不应包含在`CREATE列列表中 TABLE`语句。

            有关列应在不同后端有条件呈现的更详细场景，请考虑[`CreateColumn`](ddl.html#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")的自定义编译规则。

            0.8.3版新增：将`system=True`参数添加到[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__le__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__le__ "sqlalchemy.sql.operators.ColumnOperators.__le__")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<=`运算符。

        在列上下文中，生成子句`a <= b`。

    ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__lt__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<`运算符。

        在列上下文中，生成子句`a  b`。

    ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__ne__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__ne__ "sqlalchemy.sql.operators.ColumnOperators.__ne__")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`!=`运算符。

        在列上下文中，生成子句`a ！= b`。If the
        target is `None`, produces
        `a IS NOT NULL`.

    `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`all_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.all_ "sqlalchemy.sql.operators.ColumnOperators.all_")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`all_()`](sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

        版本1.1中的新功能

    ` anon_label  T0> ¶ T1>`{.descname}
    :   *继承自* [`anon_label`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.anon_label "sqlalchemy.sql.expression.ColumnElement.anon_label")
        *属性 tt\>\> [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")*

        为此ColumnElement提供了一个常量“匿名标签”。

        这是一个label()表达式，它将在编译时被命名。每次调用anon\_label时都会返回相同的label()，以便表达式可以多次引用anon\_label，并在编译时生成相同的标签名称。

        编译器在编译时自动使用这个函数来表达已知为“未命名”的表达式，如二进制表达式和函数调用。

    `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`any_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.any_ "sqlalchemy.sql.operators.ColumnOperators.any_")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`any_()`](sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

        版本1.1中的新功能

    ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`asc()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.asc "sqlalchemy.sql.operators.ColumnOperators.asc")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`asc()`](sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

    `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
    :   *inherited from the* [`between()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在()子句之间针对父对象生成[`between()`](sqlelement.html#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

    `铸造 T0> （ T1> 类型_  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`cast()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")
        *method of* [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

        制作一个类型演员，即`CAST（＆lt； expression＆gt； AS ＆lt； type＆gt；）`。

        这是[`cast()`](sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")函数的快捷方式。

        版本1.0.7中的新功能

    `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`collate()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        根据给定的排序字符串，针对父对象生成一个[`collate()`](sqlelement.html#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

     `compare`{.descname}(*other*, *use\_proxies=False*, *equivalents=None*, *\*\*kw*)[¶](#sqlalchemy.schema.Column.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.compare "sqlalchemy.sql.expression.ColumnElement.compare")
        *method of* [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

        将此ColumnElement与另一个进行比较。

        特别理由：

        参数：

        -   **use\_proxies**[¶](#sqlalchemy.schema.Column.compare.params.use_proxies)
            – when True, consider two columns that share a common base
            column as equivalent (i.e. shares\_lineage())
        -   **equivalents**[¶](#sqlalchemy.schema.Column.compare.params.equivalents)
            – a dictionary of columns as keys mapped to sets of columns.
            如果此字典中存在给定的“其他”列，则相应set()中的任何列都会通过比较测试，结果为True。这用于将比较扩展到可能通过外键或其他标准已知等效于此的其他列。

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.schema.Column.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.schema.Column.compile.params.bind) –
            An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.schema.Column.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.schema.Column.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.schema.Column.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.schema.Column.compile.params.compile_kwargs)
            -

            在所有“访问”方法中将传递给编译器的附加参数的可选字典。例如，这允许将自定义标志传递给自定义编译构造。它也用于传递`literal_binds`标志的情况：

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select([t]).where(t.c.x == 5)

                print s.compile(compile_kwargs={"literal_binds": True})

            版本0.9.0中的新功能

        也可以看看

        [How do I render SQL expressions as strings, possibly with bound
        parameters
        inlined?](faq_sqlexpressions.html#faq-sql-expression-string)

    `的concat  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`concat()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现'concat'操作符。

        在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

    `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.schema.Column.contains "Permalink to this definition") \>
    :   *inherited from the* [`contains()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.contains "sqlalchemy.sql.operators.ColumnOperators.contains")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'包含'运算符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；％'`

    `复制 T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   创建此`Column`的单一副本。

        这用于`Table.tometadata`中。

    `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`desc()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.desc "sqlalchemy.sql.operators.ColumnOperators.desc")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`desc()`](sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

    `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`distinct()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.distinct "sqlalchemy.sql.operators.ColumnOperators.distinct")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成一个[`distinct()`](sqlelement.html#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

    `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.schema.Column.endswith "Permalink to this definition")
    :   *inherited from the* [`endswith()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.endswith "sqlalchemy.sql.operators.ColumnOperators.endswith")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'endswith'操作符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

    `表达 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`expression`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.expression "sqlalchemy.sql.expression.ColumnElement.expression")
        *attribute of* [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

        返回一个列表达式。

        检查界面的一部分；回报自我。

    `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.schema.Column.ilike "Permalink to this definition")
    :   *inherited from the* [`ilike()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`ilike`运算符。

        在列上下文中，生成子句`a ILIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.ilike("%foobar%"))

        参数：

        -   **其他** [¶](#sqlalchemy.schema.Column.ilike.params.other) -
            要比较的表达式
        -   **转义** [¶](#sqlalchemy.schema.Column.ilike.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.ilike("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`in_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在运算符中实现`in`

        在列上下文中，生成子句`a IN 其他`。“other”可以是列表达式的元组/列表，或者是[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`is_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS`运算符。

        通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.isnot()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

    ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_distinct_from()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
        *方法 tt\> [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS DISTINCT FROM`运算符。

        在大多数平台上呈现“一个IS DISTINCT FROM
        b”；在一些如SQLite可能会呈现“一个不是b”。

        版本1.1中的新功能

    ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`isnot()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS NOT`运算符。

        Normally, `IS NOT` is generated
        automatically when comparing to a value of `None`, which resolves to `NULL`.
        但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.is_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

    ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`isnot_distinct_from()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS NOT DISTINCT FROM`运算符。

        在大多数平台上呈现“不是从BIND DISTINCT FROM
        b”；在某些例如SQLite上可能会呈现“a IS b”。

        版本1.1中的新功能

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`label()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label")
        *method of* [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

        生成列标签，即`＆lt； columnname＆gt； AS ＆lt； name＆gt；`。

        这是[`label()`](sqlelement.html#sqlalchemy.sql.expression.label "sqlalchemy.sql.expression.label")函数的快捷方式。

        如果'名称'是None，则会生成一个匿名标签名称。

    `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.schema.Column.like "Permalink to this definition")
    :   *inherited from the* [`like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        像运算符一样实现`like`

        在列上下文中，生成子句`a LIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.like("%foobar%"))

        参数：

        -   **其他** [¶](#sqlalchemy.schema.Column.like.params.other) -
            要比较的表达式
        -   **转义** [¶](#sqlalchemy.schema.Column.like.params.escape) -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.like("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.ilike()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.schema.Column.match "Permalink to this definition")
    :   *继承自* [`match()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        *方法 tt\> [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现数据库特定的“匹配”运算符。

        [`match()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        attempts to resolve to a MATCH-like function or operator
        provided by the backend. 例子包括：

        -   Postgresql - 呈现`x @@ to_tsquery（y）`
        -   MySQL - renders
            `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
        -   Oracle - 呈现`CONTAINS（x， y）`
        -   其他后端可能会提供特殊的实现。
        -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

     `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.schema.Column.notilike "Permalink to this definition")
    :   *inherited from the* [`notilike()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT ILIKE`运算符。

        这相当于对[`ColumnOperators.ilike()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.ilike()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`notin_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
        *方法 [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        执行`NOT IN`运算符。

        这相当于对[`ColumnOperators.in_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.in_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

    `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.schema.Column.notlike "Permalink to this definition")
    :   *inherited from the* [`notlike()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT LIKE`运算符。

        这相当于对[`ColumnOperators.like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`nullsfirst()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullsfirst "sqlalchemy.sql.operators.ColumnOperators.nullsfirst")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`nullsfirst()`](sqlelement.html#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

    ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`nullslast()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullslast "sqlalchemy.sql.operators.ColumnOperators.nullslast")
        *[`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`nullslast()`](sqlelement.html#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

    `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.schema.Column.op "Permalink to this definition")
    :   *继承自* [`op()`](sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
        *方法的[`Operators`](sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

        产生通用的操作员功能。

        例如。：

            somecolumn.op("*")(5)

        生产：

            somecolumn * 5

        该函数也可用于使按位运算符明确。例如：

            somecolumn.op('&')(0xff)

        是`somecolumn`中的值的按位与。

        参数：

        -   **operator**[¶](#sqlalchemy.schema.Column.op.params.operator)
            – a string which will be output as the infix operator
            between this element and the expression passed to the
            generated function.
        -   **优先顺序**
            [¶](#sqlalchemy.schema.Column.op.params.precedence) -

            当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

            New in version 0.8: - added the ‘precedence’ argument.

        -   **is\_comparison**
            [¶](#sqlalchemy.schema.Column.op.params.is_comparison) -

            如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
            true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

            版本0.9.2新增： - 添加了[`Operators.op.is_comparison`](sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

        也可以看看

        [Redefining and Creating New
        Operators](custom_types.html#types-operators)

        [Using custom operators in join
        conditions](orm_join_conditions.html#relationship-custom-operator)中使用自定义运算符

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

    `引用 T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   如果此列通过外键引用给定列，则返回True。

    ` shares_lineage  T0> （ T1>  othercolumn  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`shares_lineage()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.shares_lineage "sqlalchemy.sql.expression.ColumnElement.shares_lineage")
        *method of* [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

        如果给定的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")与此[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")具有共同的祖先，则返回True。

    `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.schema.Column.startswith "Permalink to this definition")
    :   *inherited from the* [`startswith()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.startswith "sqlalchemy.sql.operators.ColumnOperators.startswith")
        *method of* [`ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`startwith`运算符。

        在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

 *class*`sqlalchemy.schema.`{.descclassname}`MetaData`{.descname}(*bind=None*, *reflect=False*, *schema=None*, *quote\_schema=None*, *naming\_convention=immutabledict({'ix': 'ix\_%(column\_0\_label)s'})*, *info=None*)[¶](#sqlalchemy.schema.MetaData "Permalink to this definition")
:   基础：[`sqlalchemy.schema.SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

    [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象及其关联的模式结构的集合。plainplain

    保存[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的集合以及对[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的可选绑定。如果绑定，集合中的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象及其列可以参与隐式SQL执行。

    [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象本身存储在[`MetaData.tables`](#sqlalchemy.schema.MetaData.tables "sqlalchemy.schema.MetaData.tables")字典中。

    [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    is a thread-safe object for read operations. 在单个[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象中构建新表格，无论是显式还是反射，都可能不是完全线程安全的。

    也可以看看

    [Describing Databases with MetaData](#metadata-describing) -
    数据库元数据简介

     `__init__`{.descname}(*bind=None*, *reflect=False*, *schema=None*, *quote\_schema=None*, *naming\_convention=immutabledict({'ix': 'ix\_%(column\_0\_label)s'})*, *info=None*)[¶](#sqlalchemy.schema.MetaData.__init__ "Permalink to this definition")
    :   创建一个新的MetaData对象。

        参数：

        -   **bind**[¶](#sqlalchemy.schema.MetaData.params.bind) – An
            Engine or Connection to bind to.
            也可能是一个字符串或URL实例，它们被传递给create\_engine()，并且这个MetaData将被绑定到生成的引擎。
        -   **反映** [¶](#sqlalchemy.schema.MetaData.params.reflect) -

            可选，自动加载绑定数据库中的所有表。默认为False。设置此选项时需要`bind`。

            从版本0.8开始弃用：请使用[`MetaData.reflect()`](#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")方法。

        -   **模式** [¶](#sqlalchemy.schema.MetaData.params.schema) -

            The default schema to use for the [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
            [`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence"),
            and potentially other objects associated with this
            [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData").
            默认为`None`。

            当设置此值时，为schema参数指定`None`的任何[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")将改为定义此模式名称。要为模式构建[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")，即使此参数存在，也要使用`None`，请使用[`BLANK_SCHEMA`](#sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA "sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA")

            也可以看看

            [`Table.schema`](#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")

            [`Sequence.schema`](defaults.html#sqlalchemy.schema.Sequence.params.schema "sqlalchemy.schema.Sequence")

        -   **quote\_schema**[¶](#sqlalchemy.schema.MetaData.params.quote_schema)
            – Sets the `quote_schema` flag for those
            [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
            [`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence"),
            and other objects which make usage of the local
            `schema` name.
        -   **info** [¶](#sqlalchemy.schema.MetaData.params.info) -

            可选数据字典，将填充到此对象的[`SchemaItem.info`](#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")属性中。

            版本1.0.0中的新功能

        -   **naming\_convention**
            [¶](#sqlalchemy.schema.MetaData.params.naming_convention) -

            一个字典引用的值将为[`Constraint`](constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")和[`Index`](constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象建立默认的命名约定，用于那些未明确指定名称的对象。

            这本词典的关键可能是：

            -   约束或索引类，例如[`UniqueConstraint`](constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")，[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")类，[`Index`}](constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")类
            -   a string mnemonic for one of the known constraint
                classes; `"fk"`, `"pk"`, `"ix"`, `"ck"`, `"uq"` for foreign key,
                primary key, index, check, and unique constraint,
                respectively.
            -   用户定义的“记号”的字符串名称，可用于定义新的命名记号。

            与每个“约束类”或“约束助记符”键相关的值是字符串命名模板，如`"uq_%(table_name)s_%(column_0_name)s"`，它们描述名称应该如何组成。与用户定义的“标记”键相关的值应该是`fn（约束， 表）`形式的可召集，它接受约束/索引对象和[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")作为参数，返回一个字符串结果。

            内置名称如下，其中一些可能仅适用于某些类型的约束：

            > -   `%(table_name)s` -
            >     与约束关联的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的名称。
            > -   `%(referred_table_name)s` -](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的名称。
            > -   `%(column_0_name)s` -
            >     约束内索引位置“0”处的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的名称。
            > -   `%(column_0_label)s` -
            >     索引位置“0”处的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的标签，例如`Column.label`
            > -   `%(column_0_key)s` -
            >     索引位置“0”处的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的关键字，例如`Column.key`
            > -   `%(referred_column_0_name)s` -
            >     在[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")引用的索引位置“0”处的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的名称。
            > -   `%(constraint_name)s` -
            >     引用给约束的现有名称的特殊键。当该键存在时，[`Constraint`](constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")对象的现有名称将被替换为由使用此标记的模板字符串组成的名称。当此令牌存在时，要求[`Constraint`](constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")提前提供一个明确的名称。
            > -   用户定义的：任何附加标记都可以通过将其与`fn（约束， 表）`一起传递给naming\_convention字典来实现。

            版本0.9.2中的新功能

            也可以看看

            [Configuring Constraint Naming
            Conventions](constraints.html#constraint-naming-conventions)
            - 有关详细使用示例。

    `append_ddl_listener`{.descname} （ *event\_name*，*听众* ） [](#sqlalchemy.schema.MetaData.append_ddl_listener "Permalink to this definition")
    :   将一个DDL事件监听器追加到`MetaData`中。

        从版本0.7开始弃用：请参阅[`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")。

    `结合 T0> ¶ T1>`{.descname}
    :   An [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
        or [`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
        to which this [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        is bound.

        Typically, a [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
        is assigned to this attribute so that “implicit execution” may
        be used, or alternatively as a means of providing engine binding
        information to an ORM [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        object:

            engine = create_engine("someurl://")
            metadata.bind = engine

        也可以看看

        [Connectionless Execution, Implicit
        Execution](connections.html#dbengine-implicit) - “绑定元数据”

    `明确 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   清除此元数据中的所有表格对象。

    `create_all`{.descname} （ *bind = None*，*tables = None*，*checkfirst = True* ） T5\> [¶ T6\>](#sqlalchemy.schema.MetaData.create_all "Permalink to this definition")
    :   创建存储在这个元数据中的所有表。

        有条件的默认情况下，不会尝试重新创建目标数据库中已存在的表。

        参数：

        -   **bind**[¶](#sqlalchemy.schema.MetaData.create_all.params.bind)
            – A [`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")
            used to access the database; if None, uses the existing bind
            on this `MetaData`, if any.
        -   **tables**[¶](#sqlalchemy.schema.MetaData.create_all.params.tables)
            – Optional list of `Table` objects,
            which is a subset of the total tables in the
            `MetaData` (others are ignored).
        -   **checkfirst**
            [¶](#sqlalchemy.schema.MetaData.create_all.params.checkfirst)
            - 默认为True，不要为已存在于目标数据库中的表发出CREATE。

    `drop_all`{.descname} （ *bind = None*，*tables = None*，*checkfirst = True* ） T5\> [¶ T6\>](#sqlalchemy.schema.MetaData.drop_all "Permalink to this definition")
    :   删除存储在此元数据中的所有表。

        有条件的默认情况下，不会尝试删除目标数据库中不存在的表。

        参数：

        -   **bind**[¶](#sqlalchemy.schema.MetaData.drop_all.params.bind)
            – A [`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")
            used to access the database; if None, uses the existing bind
            on this `MetaData`, if any.
        -   **tables**[¶](#sqlalchemy.schema.MetaData.drop_all.params.tables)
            – Optional list of `Table` objects,
            which is a subset of the total tables in the
            `MetaData` (others are ignored).
        -   **checkfirst**
            [¶](#sqlalchemy.schema.MetaData.drop_all.params.checkfirst)
            - 默认为True，只发布确认存在于目标数据库中的表的DROP。

    ` is_bound  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果此MetaData绑定到引擎或连接，则为true。

     `reflect`{.descname}(*bind=None*, *schema=None*, *views=False*, *only=None*, *extend\_existing=False*, *autoload\_replace=True*, *\*\*dialect\_kwargs*)[¶](#sqlalchemy.schema.MetaData.reflect "Permalink to this definition")
    :   从数据库加载所有可用的表定义。

        在`MetaData`中自动创建`Table`条目，以查找数据库中可用但尚未出现在`MetaData`中的任何表。可能会多次调用以拾取最近添加到数据库中的表，但是如果数据库中不再存在此`MetaData`中的表，则不会执行特殊操作。

        参数：

        -   **bind**[¶](#sqlalchemy.schema.MetaData.reflect.params.bind)
            – A [`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")
            used to access the database; if None, uses the existing bind
            on this `MetaData`, if any.
        -   **schema**[¶](#sqlalchemy.schema.MetaData.reflect.params.schema)
            – Optional, query and reflect tables from an alterate
            schema. 如果没有，则使用与此[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")关联的模式（如果有的话）。
        -   **视图**
            [¶](#sqlalchemy.schema.MetaData.reflect.params.views) -
            如果为True，也反映视图。
        -   **only**
            [¶](#sqlalchemy.schema.MetaData.reflect.params.only) -

            可选的。仅加载可用命名表的子集。可能被指定为一个名称或可调用的序列。

            如果提供了一系列名称，则只会反映这些表。如果请求表但不可用，则会发生错误。已经存在于`MetaData`中的命名表被忽略。

            如果提供了可调用对象，它将用作布尔谓词来过滤潜在表名称的列表。可调用表名和这个`MetaData`实例作为位置参数进行调用，并且应该为任何表反映真实值。

        -   **extend\_existing**
            [¶](#sqlalchemy.schema.MetaData.reflect.params.extend_existing)
            -

            作为[`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")传递给每个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。

            版本0.9.1中的新功能

        -   **autoload\_replace**
            [¶](#sqlalchemy.schema.MetaData.reflect.params.autoload_replace)
            -

            作为[`Table.autoload_replace`](#sqlalchemy.schema.Table.params.autoload_replace "sqlalchemy.schema.Table")传递给每个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。

            版本0.9.1中的新功能

        -   **\*\* dialect\_kwargs**
            [¶](#sqlalchemy.schema.MetaData.reflect.params.**dialect_kwargs)
            -

            上面未提及的其他关键字参数是特定于方言的，并以`<dialectname>_<argname>`的形式传递。有关记录参数的详细信息，请参阅[Dialects](dialects_index.html)中有关单个方言的文档。

            > 版本0.9.2中的新功能： -
            > 添加了[`MetaData.reflect.**dialect_kwargs`](#sqlalchemy.schema.MetaData.reflect.params.**dialect_kwargs "sqlalchemy.schema.MetaData.reflect")以支持反映的所有[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的方言级别反射选项。

    `除去 T0> （ T1> 表 T2> ） T3> ¶ T4>`{.descname}
    :   从这个MetaData中移除给定的Table对象。

    ` sorted_tables  T0> ¶ T1>`{.descname}
    :   返回按照外键依赖关系排序的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象列表。

        The sorting will place [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        objects that have dependencies first, before the dependencies
        themselves, representing the order in which they can be created.
        要获取表格的放置顺序，请使用内置的`reversed()` Python。

        警告

        [`sorted_tables`](#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")访问器本身不能自动解决表间依赖关系循环的自动解析问题，这通常是由相互依赖的外键约束引起的。要解决这些循环，可以将[`ForeignKeyConstraint.use_alter`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")参数应用于这些约束，或者使用[`schema.sort_tables_and_constraints()`](ddl.html#sqlalchemy.schema.sort_tables_and_constraints "sqlalchemy.schema.sort_tables_and_constraints")函数来打破涉及分开循环。

        也可以看看

        [`schema.sort_tables()`](ddl.html#sqlalchemy.schema.sort_tables "sqlalchemy.schema.sort_tables")

        [`schema.sort_tables_and_constraints()`](ddl.html#sqlalchemy.schema.sort_tables_and_constraints "sqlalchemy.schema.sort_tables_and_constraints")

        [`MetaData.tables`](#sqlalchemy.schema.MetaData.tables "sqlalchemy.schema.MetaData.tables")

        [`Inspector.get_table_names()`](reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names "sqlalchemy.engine.reflection.Inspector.get_table_names")

        [`Inspector.get_sorted_table_and_fkc_names()`](reflection.html#sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names "sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names")

    `表格`{.descname} *=无* [¶](#sqlalchemy.schema.MetaData.tables "Permalink to this definition")
    :   一个名为[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的对象名称或“表键”。

        确切的关键是由[`Table.key`](#sqlalchemy.schema.Table.key "sqlalchemy.schema.Table.key")属性确定的；对于没有`Table.schema`属性的表，这与`Table.name`相同。对于具有模式的表格，其格式通常为`schemaname.tablename`。

        也可以看看

        [`MetaData.sorted_tables`](#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")

*class* `sqlalchemy.schema。`{.descclassname} `SchemaItem`{.descname} [¶](#sqlalchemy.schema.SchemaItem "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.SchemaEventTarget`，`sqlalchemy.sql.visitors.Visitable`

    定义数据库模式的项目的基类。plainplainplainplain

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    `引用 T0> ¶ T1>`{.descname}
    :   对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

*class* `sqlalchemy.schema。`{.descclassname} `表`{.descname} （ *\* args*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.Table "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.base.DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")，[`sqlalchemy.schema.SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")，[`sqlalchemy.sql.expression.TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")

    在数据库中表示一个表。plainplain

    例如。：

        mytable = Table("mytable", metadata,
                        Column('mytable_id', Integer, primary_key=True),
                        Column('value', String(50))
                   )

    [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象根据给定的[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象内的名称和可选的模式名称构造自己的唯一实例。第二次调用具有相同名称和相同[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")参数的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造函数将返回*相同*
    [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象 -
    通过这种方式，[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造函数充当注册表函数。

    也可以看看

    [Describing Databases with MetaData](#metadata-describing) -
    数据库元数据简介

    构造函数参数如下：

    参数：

    -   **名称** [¶](#sqlalchemy.schema.Table.params.name) -

        数据库中表示的该表的名称。

        表名与`schema`参数的值一起构成一个关键字，用于唯一标识拥有的[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")集合中的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。对具有相同名称，元数据和模式名​​称的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的其他调用将返回相同的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。

        不包含大写字母的名称将被视为不区分大小写的名称，除非它们是保留字或包含特殊字符，否则不会被引用。具有任意数量大写字符的名称被认为是区分大小写的，并将以引用方式发送。

        要为表名称启用无条件引用，请向构造函数指定标记`quote=True`，或使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")构造指定名称。

    -   **metadata**[¶](#sqlalchemy.schema.Table.params.metadata) – a
        [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        object which will contain this table.
        元数据被用作该表与通过外键引用的其他表的关联点。它也可以用来将该表与特定的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")关联。
    -   **\*args**[¶](#sqlalchemy.schema.Table.params.*args) –
        Additional positional arguments are used primarily to add the
        list of [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects contained within this table. 类似于CREATE
        TABLE语句的样式，可以在这里添加其他[`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")结构，包括[`PrimaryKeyConstraint`](constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")和[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")。
    -   **autoload** [¶](#sqlalchemy.schema.Table.params.autoload) -

        Defaults to False, unless [`Table.autoload_with`](#sqlalchemy.schema.Table.params.autoload_with "sqlalchemy.schema.Table")
        is set in which case it defaults to True; [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects for this table should be reflected from the database,
        possibly augmenting or replacing existing [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects that were expicitly specified.

        版本1.0.0更改：设置[`Table.autoload_with`](#sqlalchemy.schema.Table.params.autoload_with "sqlalchemy.schema.Table")参数意味着[`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")将默认为True。

        也可以看看

        [Reflecting Database Objects](reflection.html)

    -   **autoload\_replace**
        [¶](#sqlalchemy.schema.Table.params.autoload_replace) -

        Defaults to `True`; when using
        [`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")
        in conjunction with [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table"),
        indicates that [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects present in the already-existing [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        object should be replaced with columns of the same name
        retrieved from the autoload process. 当`False`时，已存在于现有名称下的列将从反映过程中省略。

        请注意，此设置不会影响在[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")调用中以编程方式指定的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，该对象也是自动加载的；当[`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")为`True`时，那些[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象将始终替换同名的现有列。

        New in version 0.7.5.

        也可以看看

        [`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")

        [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")

    -   **autoload\_with**
        [¶](#sqlalchemy.schema.Table.params.autoload_with) -

        一个[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象，它将反映这个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象；当设置为非无值时，它意味着[`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")是`True`。如果未设置，但[`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")显式设置为`True`，则自动加载操作将尝试通过查找[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")绑定到底层的[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象。

        也可以看看

        [`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")

    -   **extend\_existing**
        [¶](#sqlalchemy.schema.Table.params.extend_existing) -

        当`True`时，表示如果[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")已经存在于给定的[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")中，则在构造函数中将更多参数应用于现有[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")

        If [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")
        or [`Table.keep_existing`](#sqlalchemy.schema.Table.params.keep_existing "sqlalchemy.schema.Table")
        are not set, and the given name of the new [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        refers to a [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is already present in the target [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        collection, and this [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        specifies additional columns or other constructs or flags that
        modify the table’s state, an error is raised. The purpose of
        these two mutually-exclusive flags is to specify what action
        should be taken when a [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        is specified that matches an existing [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
        yet specifies additional constructs.

        [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")
        will also work in conjunction with [`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")
        to run a new reflection operation against the database, even if
        a [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        of the same name is already present in the target
        [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData");
        newly reflected [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects and other options will be added into the state of the
        [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
        potentially overwriting existing columns and options of the same
        name.

        版本0.7.4更改： [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")将与[`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")设置为True时调用新的反射操作。

        As is always the case with [`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table"),
        [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects can be specified in the same [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        constructor, which will take precedence.
        在下面，现有的表`mytable`将被从数据库反映的[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象以及名为“y”的给定[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

            Table("mytable", metadata,
                        Column('y', Integer),
                        extend_existing=True,
                        autoload=True,
                        autoload_with=engine
                    )

        也可以看看

        [`Table.autoload`](#sqlalchemy.schema.Table.params.autoload "sqlalchemy.schema.Table")

        [`Table.autoload_replace`](#sqlalchemy.schema.Table.params.autoload_replace "sqlalchemy.schema.Table")

        [`Table.keep_existing`](#sqlalchemy.schema.Table.params.keep_existing "sqlalchemy.schema.Table")

    -   **implicit\_returning**[¶](#sqlalchemy.schema.Table.params.implicit_returning)
        – True by default - indicates that RETURNING can be used by
        default to fetch newly inserted primary key values, for backends
        which support this.
        请注意，create\_engine()还提供了隐式返回标志。
    -   **include\_columns**[¶](#sqlalchemy.schema.Table.params.include_columns)
        – A list of strings indicating a subset of columns to be loaded
        via the `autoload` operation; table columns
        who aren’t present in this list will not be represented on the
        resulting `Table` object.
        默认为`None`，表示应该反映所有列。
    -   **info**[¶](#sqlalchemy.schema.Table.params.info) – Optional
        data dictionary which will be populated into the
        [`SchemaItem.info`](#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        attribute of this object.
    -   **keep\_existing**
        [¶](#sqlalchemy.schema.Table.params.keep_existing) -

        当`True`时，表示如果此表已存在于给定的[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")中，则在构造函数内忽略现有[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的其他参数，并返回最初创建的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。这是为了允许一个函数希望在第一次调用时定义一个新的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，但在随后的调用中将返回相同的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，而没有任何声明（特别是约束）再次应用。

        If [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")
        or [`Table.keep_existing`](#sqlalchemy.schema.Table.params.keep_existing "sqlalchemy.schema.Table")
        are not set, and the given name of the new [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        refers to a [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is already present in the target [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        collection, and this [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        specifies additional columns or other constructs or flags that
        modify the table’s state, an error is raised. The purpose of
        these two mutually-exclusive flags is to specify what action
        should be taken when a [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        is specified that matches an existing [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
        yet specifies additional constructs.

        也可以看看

        [`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")

    -   **听众** [¶](#sqlalchemy.schema.Table.params.listeners) -

        A list of tuples of the form `(<eventname>, <fn>)` which will be passed to [`event.listen()`](event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")
        upon construction. 这个对[`event.listen()`](event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")的替代钩子允许在“autoload”过程开始之前建立一个特定于这个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的侦听器函数。对[`DDLEvents.column_reflect()`](events.html#sqlalchemy.events.DDLEvents.column_reflect "sqlalchemy.events.DDLEvents.column_reflect")事件特别有用：

            def listen_for_reflect(table, column_info):
                "handle the column reflection event"
                # ...

            t = Table(
                'sometable',
                autoload=True,
                listeners=[
                    ('column_reflect', listen_for_reflect)
                ])

    -   **mustexist**[¶](#sqlalchemy.schema.Table.params.mustexist) –
        When `True`, indicates that this Table must
        already be present in the given [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        collection, else an exception is raised.
    -   **prefixes**[¶](#sqlalchemy.schema.Table.params.prefixes) – A
        list of strings to insert after CREATE in the CREATE TABLE
        statement. 他们将被空格隔开。
    -   **quote**[¶](#sqlalchemy.schema.Table.params.quote) – Force
        quoting of this table’s name on or off, corresponding to
        `True` or `False`.
        当它保留默认值`None`时，列标识符将根据名称是否区分大小写（带有至少一个大写字符的标识符视为区分大小写）或者是保留字。该标志仅用于强制引用SQLAlchemy方言未知的保留字。
    -   **quote\_schema**[¶](#sqlalchemy.schema.Table.params.quote_schema)
        – same as ‘quote’ but applies to the schema identifier.
    -   **模式** [¶](#sqlalchemy.schema.Table.params.schema) -

        此表的模式名称，如果表驻留在引擎的数据库连接的默认选定模式之外的模式中，则此名称是必需的。默认为`None`。

        If the owning [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        of this [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        specifies its own [`MetaData.schema`](#sqlalchemy.schema.MetaData.params.schema "sqlalchemy.schema.MetaData")
        parameter, then that schema name will be applied to this
        [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        if the schema parameter here is set to `None`. 要在[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")上设置空白模式名称，否则它将使用拥有[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")的模式集，请指定特殊符号[`BLANK_SCHEMA`](#sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA "sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA")。

        版本1.0.14中的新增功能：添加了[`BLANK_SCHEMA`](#sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA "sqlalchemy.schema.sqlalchemy.schema.BLANK_SCHEMA")符号以允许[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")具有空白模式名称，即使当父元素[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")指定[`MetaData.schema`](#sqlalchemy.schema.MetaData.params.schema "sqlalchemy.schema.MetaData")。

        模式名称的引用规则与`name`参数的引用规则相同，因为引用适用于保留字或区分大小写的名称；为模式名称启用无条件引用，为构造函数指定标记`quote_schema=True`，或使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")结构指定名称。

    -   **useexisting** [¶](#sqlalchemy.schema.Table.params.useexisting)
        - 弃用。使用[`Table.extend_existing`](#sqlalchemy.schema.Table.params.extend_existing "sqlalchemy.schema.Table")。
    -   **\*\*kw**[¶](#sqlalchemy.schema.Table.params.**kw) – Additional
        keyword arguments not mentioned above are dialect specific, and
        passed in the form `<dialectname>_<argname>`.
        有关记录参数的详细信息，请参阅[Dialects](dialects_index.html)中有关单个方言的文档。

    `__ init __`{.descname} （ *\* args*，*\*\* kw* ） [T5\>](#sqlalchemy.schema.Table.__init__ "Permalink to this definition")
    :   [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的构造函数。

        这种方法是无操作的。有关构造函数参数，请参阅[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的顶级文档。

    ` add_is_dependent_on  T0> （ T1> 表 T2> ） T3> ¶ T4>`{.descname}
    :   为此表添加一个“依赖关系”。

        这是另一个Table对象，必须在此对象之前先创建，否则将在此对象之后被删除。

        通常，表之间的依赖关系通过ForeignKey对象来确定。但是，对于在外键（规则，继承）之外创建依赖关系的其他情况，此方法可以手动建立这样的链接。

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.schema.Table.alias "Permalink to this definition")
    :   *从* [`alias()`](selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](selectable.html#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` append_column  T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   追加一个[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")到这个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。

        The “key” of the newly added [`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
        i.e. the value of its `.key` attribute, will
        then be available in the `.c` collection of
        this [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
        and the column definition will be included in any CREATE TABLE,
        SELECT, UPDATE, etc. 从[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")结构生成的语句。

        请注意，假设表已经在数据库中创建，那么**不会**更改任何基础数据库中存在的表的定义。关系数据库支持使用SQL
        ALTER命令向现有表添加列，该命令需要针对不包含新添加列的现有表发布。

    ` append_constraint  T0> （ T1> 约束 T2> ） T3> ¶ T4>`{.descname}
    :   追加一个[`Constraint`](constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")到这个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。

        如果特定的DDL创建事件尚未与给定的[`Constraint`](constraints.html#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")对象相关联，则会在将来的CREATE
        TABLE语句中包含约束。

        请注意，对于数据库中已存在的表，**不会**自动在关系数据库中生成约束。要将约束添加到现有的关系数据库表中，必须使用SQL
        ALTER命令。SQLAlchemy还提供了[`AddConstraint`](ddl.html#sqlalchemy.schema.AddConstraint "sqlalchemy.schema.AddConstraint")构造，当它作为可执行子句调用时可以产生此SQL。

    `append_ddl_listener`{.descname} （ *event\_name*，*听众* ） [](#sqlalchemy.schema.Table.append_ddl_listener "Permalink to this definition")
    :   将一个DDL事件监听器追加到`Table`中。

        从版本0.7开始弃用：请参阅[`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")。

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.Table.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.Table.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.Table.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.Table.argument_for.params.default) -
            参数的默认值。

        版本0.9.4中的新功能

    `结合 T0> ¶ T1>`{.descname}
    :   返回与此表关联的可连接。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](selectable.html#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.schema.Table.columns "sqlalchemy.schema.Table.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](selectable.html#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.schema.Table.columns "sqlalchemy.schema.Table.columns")或[`c`](#sqlalchemy.schema.Table.c "sqlalchemy.schema.Table.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.schema.Table.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.schema.Table.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.schema.Table.compile.params.bind) –
            An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.schema.Table.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.schema.Table.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.schema.Table.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.schema.Table.compile.params.compile_kwargs)
            -

            在所有“访问”方法中将传递给编译器的附加参数的可选字典。例如，这允许将自定义标志传递给自定义编译构造。它也用于传递`literal_binds`标志的情况：

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select([t]).where(t.c.x == 5)

                print s.compile(compile_kwargs={"literal_binds": True})

            版本0.9.0中的新功能

        也可以看看

        [How do I render SQL expressions as strings, possibly with bound
        parameters
        inlined?](faq_sqlexpressions.html#faq-sql-expression-string)

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.schema.Table.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](selectable.html#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.schema.Table.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](selectable.html#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](selectable.html#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.schema.Table.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.schema.Table.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.schema.Table.count "Permalink to this definition")
    :   *继承自* [`count()`](selectable.html#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

     `create`{.descname}(*bind=None*, *checkfirst=False*)[¶](#sqlalchemy.schema.Table.create "Permalink to this definition")
    :   使用给定的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")进行连接，为此[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")发出`CREATE`语句。

        也可以看看

        [`MetaData.create_all()`](#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")

    `删除`{.descname} （ *whereclause = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.schema.Table.delete "Permalink to this definition")
    :   *inherited from the* [`delete()`](selectable.html#sqlalchemy.sql.expression.TableClause.delete "sqlalchemy.sql.expression.TableClause.delete")
        *method of* [`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")

        根据这个[`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")生成一个[`delete()`](dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")结构。

        例如。：

            table.delete().where(table.c.id==7)

        有关参数和使用信息，请参阅[`delete()`](dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

     `drop`{.descname}(*bind=None*, *checkfirst=False*)[¶](#sqlalchemy.schema.Table.drop "Permalink to this definition")
    :   使用给定的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")进行连接，为此[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")发出`DROP`语句。

        也可以看看

        [`MetaData.drop_all()`](#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")

    `存在 T0> （ T1> 绑定=无 T2> ） T3> ¶ T4>`{.descname}
    :   如果此表存在，则返回True。

    ` foreign_key_constraints  T0> ¶ T1>`{.descname}
    :   由[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")引用的[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象。

        该列表由当前关联的[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象的集合生成。

        版本1.0.0中的新功能

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](selectable.html#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    `insert`{.descname} （ *values = None*，*inline = False*，*\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.schema.Table.insert "Permalink to this definition")
    :   *inherited from the* [`insert()`](selectable.html#sqlalchemy.sql.expression.TableClause.insert "sqlalchemy.sql.expression.TableClause.insert")
        *method of* [`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")

        针对这个[`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")生成一个[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")结构。

        例如。：

            table.insert().values(name='foo')

        有关参数和使用信息，请参见[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")。

    ` is_derived_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_derived_from()`](selectable.html#sqlalchemy.sql.expression.FromClause.is_derived_from "sqlalchemy.sql.expression.FromClause.is_derived_from")
        *方法* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        如果FromClause从给定的FromClause中“派生”，则返回True。

        一个例子是从表中派生的表的别名。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.schema.Table.join "Permalink to this definition")
    :   *inherited from the* [`join()`](selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个`FromClause`。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确** [¶](#sqlalchemy.schema.Table.join.params.right) -
            连接的右侧；这是任何[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.schema.Table.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.schema.Table.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整** [¶](#sqlalchemy.schema.Table.join.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](selectable.html#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](selectable.html#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `键 T0> ¶ T1>`{.descname}
    :   返回这个[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的'键'。

        该值用作[`MetaData.tables`](#sqlalchemy.schema.MetaData.tables "sqlalchemy.schema.MetaData.tables")集合中的字典键。对于没有`Table.schema`集合的表，它通常与`Table.name`相同；否则它通常是`schemaname.tablename`形式。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](selectable.html#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](selectable.html#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](selectable.html#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.schema.Table.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](selectable.html#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another `FromClause`,
        with the “isouter” flag set to True.

        例如。：

            from sqlalchemy import outerjoin

            j = user_table.outerjoin(address_table,
                            user_table.c.id == address_table.c.user_id)

        以上相当于：

            j = user_table.join(
                address_table,
                user_table.c.id == address_table.c.user_id,
                isouter=True)

        参数：

        -   **正确**
            [¶](#sqlalchemy.schema.Table.outerjoin.params.right) -
            连接的右侧；这是任何[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.schema.Table.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整** [¶](#sqlalchemy.schema.Table.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](selectable.html#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](selectable.html#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

    ` quote_schema  T0> ¶ T1>`{.descname}
    :   返回传递给[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的`quote_schema`标志的值。

        从版本0.9开始弃用：使用`table.schema.quote`

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.schema.Table.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](selectable.html#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.schema.Table.select "Permalink to this definition")
    :   *inherited from the* [`select()`](selectable.html#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.schema.Table.self_group "sqlalchemy.schema.Table.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.schema.Table.self_group "sqlalchemy.schema.Table.self_group")方法仅返回self。

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.schema.Table.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](selectable.html#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](selectable.html#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](selectable.html#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](selectable.html#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `tometadata`{.descname} （ *元数据*，*schema =符号（'retain\_schema'）*，*referenced\_schema\_fn =无 t4 \>，*name = None* ） [¶](#sqlalchemy.schema.Table.tometadata "Permalink to this definition")*
    :   返回与[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")关联的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的副本。

        例如。：

            m1 = MetaData()

            user = Table('user', m1, Column('id', Integer, priamry_key=True))

            m2 = MetaData()
            user_copy = user.tometadata(m2)

        参数：

        -   **metadata**[¶](#sqlalchemy.schema.Table.tometadata.params.metadata)
            – Target [`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
            object, into which the new [`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            object will be created.
        -   **模式**
            [¶](#sqlalchemy.schema.Table.tometadata.params.schema) -

            指示目标模式的可选字符串名称。默认为特殊符号`RETAIN_SCHEMA`，它表示在新的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中不应更改模式名称。如果设置为字符串名称，则新的[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")将具有`.schema`的新名称。如果设置为`None`，则架构将设置为在目标[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")上设置的架构的架构，该架构通常也是`None`，除非明确设置：

                m2 = MetaData(schema='newschema')

                # user_copy_one will have "newschema" as the schema name
                user_copy_one = user.tometadata(m2, schema=None)

                m3 = MetaData()  # schema defaults to None

                # user_copy_two will have None as the schema name
                user_copy_two = user.tometadata(m3, schema=None)

        -   **referenced\_schema\_fn**
            [¶](#sqlalchemy.schema.Table.tometadata.params.referred_schema_fn)
            -

            optional callable which can be supplied in order to provide
            for the schema name that should be assigned to the
            referenced table of a [`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint").
            可调用接受这个父表[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，我们要更改的目标模式，[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象以及该约束的现有“目标模式”。该函数应返回应该应用的字符串模式名称。例如。：

                def referred_schema_fn(table, to_schema,
                                                constraint, referred_schema):
                    if referred_schema == 'base_tables':
                        return referred_schema
                    else:
                        return to_schema

                new_table = table.tometadata(m2, schema="alt_schema",
                                        referred_schema_fn=referred_schema_fn)

            版本0.9.2中的新功能

        -   **名称**
            [¶](#sqlalchemy.schema.Table.tometadata.params.name) -

            可选的字符串名称，表示目标表名称。如果未指定或无，表名将被保留。这允许将[`Table`](#sqlalchemy.schema.Table "sqlalchemy.schema.Table")以新名称复制到同一个[`MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")目标中。

            版本1.0.0中的新功能

     `update`{.descname}(*whereclause=None*, *values=None*, *inline=False*, *\*\*kwargs*)[¶](#sqlalchemy.schema.Table.update "Permalink to this definition")
    :   *继承自* [`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")
        *方法* [`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")

        根据这个[`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")生成一个[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")结构。

        例如。：

            table.update().where(table.c.id==7).values(name='foo')

        有关参数和使用信息，请参阅[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")。

*class* `sqlalchemy.schema。`{.descclassname} `ThreadLocalMetaData`{.descname} [¶](#sqlalchemy.schema.ThreadLocalMetaData "Permalink to this definition")
:   基础：[`sqlalchemy.schema.MetaData`](#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")

    一个MetaData变体，它在每个线程中呈现不同的`bind`。plain

    使MetaData的`bind`属性成为线程本地值，允许将这些表集合绑定到每个线程中的不同`Engine`实现或连接。

    ThreadLocalMetaData开始在每个线程中绑定到None。绑定必须通过分配给`bind`属性或使用`connect()`来显式地进行。您也可以每个线程多次重新绑定，就像普通的`MetaData`一样。

    ` __初始化__  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   构造一个ThreadLocalMetaData。

    `结合 T0> ¶ T1>`{.descname}
    :   此线程绑定的引擎或连接。

        这个属性可以被分配一个引擎或连接，或者分配一个字符串或URL来自动创建一个用`create_engine()`绑定的基本引擎。

    `处置 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在所有线程上下文中处理所有绑定的引擎。

    ` is_bound  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果此线程存在绑定，则为true。


