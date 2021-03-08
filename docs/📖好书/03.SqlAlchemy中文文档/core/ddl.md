---
title: 定制 DDL
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/core/ddl/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
定制 DDL [¶](#customizing-ddl "Permalink to this headline")
==========================================================

In the preceding sections we’ve discussed a variety of schema constructs
including [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint"),
[`CheckConstraint`](constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint"),
and [`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence").
Throughout, we’ve relied upon the `create()` and
[`create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
methods of [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
and [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
in order to issue data definition language (DDL) for all constructs.
在发布时，调用预定义的操作顺序，并且创建每个表的 DDL 被无条件地创建，包括与其相关联的所有约束和其他对象。对于需要特定于数据库的 DDL 的更复杂场景，SQLAlchemy 提供了两种技术，可用于根据任何条件添加任何 DDL，可以伴随标准的表生成或自身。

自定义 DDL [¶](#custom-ddl "Permalink to this headline")
-------------------------------------------------------

使用[`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL")结构最容易实现自定义 DDL 短语。这个构造像所有其他的 DDL 元素一样工作，除了它接受一个字符串，它是要发射的文本：

    event.listen(plain
        metadata,
        "after_create",
        DDL("ALTER TABLE users ADD CONSTRAINT "
            "cst_user_name_length "
            " CHECK (length(user_name) >= 8)")
    )

创建 DDL 结构库的更全面的方法是使用自定义编译 -
有关详细信息，请参阅[Custom SQL Constructs and Compilation
Extension](compiler.html)。

控制 DDL 序列[¶](#controlling-ddl-sequences "Permalink to this headline")
-----------------------------------------------------------------------

先前引入的[`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL")构造也具有基于对数据库的检查有条件调用的能力。该功能可以使用[`DDLElement.execute_if()`](#sqlalchemy.schema.DDLElement.execute_if "sqlalchemy.schema.DDLElement.execute_if")方法。例如，如果我们想创建一个触发器，但只能在 Postgresql 后端上，我们可以这样调用它：

    mytable = Table(
        'mytable', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', String(50))
    )

    trigger = DDL(
        "CREATE TRIGGER dt_ins BEFORE INSERT ON mytable "
        "FOR EACH ROW BEGIN SET NEW.data='ins'; END"
    )

    event.listen(
        mytable,
        'after_create',
        trigger.execute_if(dialect='postgresql')
    )

[`DDLElement.execute_if.dialect`](#sqlalchemy.schema.DDLElement.execute_if.params.dialect "sqlalchemy.schema.DDLElement.execute_if")关键字也接受字符串方言名称的元组：

    event.listen(plainplain
        mytable,
        "after_create",
        trigger.execute_if(dialect=('postgresql', 'mysql'))
    )
    event.listen(
        mytable,
        "before_drop",
        trigger.execute_if(dialect=('postgresql', 'mysql'))
    )

[`DDLElement.execute_if()`](#sqlalchemy.schema.DDLElement.execute_if "sqlalchemy.schema.DDLElement.execute_if")方法也可以用于可接收数据库连接的可调用函数。在下面的例子中，我们使用它来有条件地创建 CHECK 约束，首先在 Postgresql 目录中查看它是否存在：

    def should_create(ddl, target, connection, **kw):plainplain
        row = connection.execute(
            "select conname from pg_constraint where conname='%s'" %
            ddl.element.name).scalar()
        return not bool(row)

    def should_drop(ddl, target, connection, **kw):
        return not should_create(ddl, target, connection, **kw)

    event.listen(
        users,
        "after_create",
        DDL(
            "ALTER TABLE users ADD CONSTRAINT "
            "cst_user_name_length CHECK (length(user_name) >= 8)"
        ).execute_if(callable_=should_create)
    )
    event.listen(
        users,
        "before_drop",
        DDL(
            "ALTER TABLE users DROP CONSTRAINT cst_user_name_length"
        ).execute_if(callable_=should_drop)
    )

    sqlusers.create(engine)
    CREATE TABLE users (
        user_id SERIAL NOT NULL,
        user_name VARCHAR(40) NOT NULL,
        PRIMARY KEY (user_id)
    )

    select conname from pg_constraint where conname='cst_user_name_length'
    ALTER TABLE users ADD CONSTRAINT cst_user_name_length  CHECK (length(user_name) >= 8)
    sqlusers.drop(engine)
    select conname from pg_constraint where conname='cst_user_name_length'
    ALTER TABLE users DROP CONSTRAINT cst_user_name_length
    DROP TABLE users

使用内置的 DDLElement 类[¶](#using-the-built-in-ddlelement-classes "Permalink to this headline")
----------------------------------------------------------------------------------------------

`sqlalchemy.schema`包包含提供 DDL 表达式的 SQL 表达式结构。例如，要产生一个`CREATE TABLE`语句：

    from sqlalchemy.schema import CreateTable
    sqlengine.execute(CreateTable(mytable))
    CREATE TABLE mytable (
        col1 INTEGER,
        col2 INTEGER,
        col3 INTEGER,
        col4 INTEGER,
        col5 INTEGER,
        col6 INTEGER
    )

在上面，[`CreateTable`](#sqlalchemy.schema.CreateTable "sqlalchemy.schema.CreateTable")构造像任何其他表达式构造一样工作（如`select()`，`table.insert()`等）。所有 SQLAlchemy 的面向 DDL 的构造都是[`DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")基类的子类；这是对应于 CREATE 和 DROP 以及 ALTER 的所有对象的基础，不仅在 SQLAlchemy 中，而且在 Alembic
Migrations 中也是如此。可用构造的完整引用位于[DDL Expression Constructs
API](#schema-api-ddl)中。

用户定义的 DDL 结构也可以创建为[`DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")本身的子类。[Custom
SQL Constructs and Compilation
Extension](compiler.html)中的文档有几个例子。

上一节[Controlling DDL
Sequences](#schema-ddl-sequences)中描述的事件驱动的 DDL 系统也可以与其他[`DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")对象一起使用。However,
when dealing with the built-in constructs such as [`CreateIndex`](#sqlalchemy.schema.CreateIndex "sqlalchemy.schema.CreateIndex"),
[`CreateSequence`](#sqlalchemy.schema.CreateSequence "sqlalchemy.schema.CreateSequence"),
etc, the event system is of **limited** use, as methods like
[`Table.create()`](metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create")
and [`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
will invoke these constructs unconditionally.
在未来的 SQLAlchemy 发行版中，包含条件执行的 DDL 事件系统将考虑目前在所有情况下调用的内置构造。

我们可以用[`AddConstraint`](#sqlalchemy.schema.AddConstraint "sqlalchemy.schema.AddConstraint")和[`DropConstraint`](#sqlalchemy.schema.DropConstraint "sqlalchemy.schema.DropConstraint")结构来说明一个事件驱动的例子，因为事件驱动系统可以用于 CHECK 和 UNIQUE 约束，像我们在[`DDLElement.execute_if()`](#sqlalchemy.schema.DDLElement.execute_if "sqlalchemy.schema.DDLElement.execute_if")的前一个例子：

    def should_create(ddl, target, connection, **kw):plainplain
        row = connection.execute(
            "select conname from pg_constraint where conname='%s'" %
            ddl.element.name).scalar()
        return not bool(row)

    def should_drop(ddl, target, connection, **kw):
        return not should_create(ddl, target, connection, **kw)

    event.listen(
        users,
        "after_create",
        AddConstraint(constraint).execute_if(callable_=should_create)
    )
    event.listen(
        users,
        "before_drop",
        DropConstraint(constraint).execute_if(callable_=should_drop)
    )

    sqlusers.create(engine)
    CREATE TABLE users (
        user_id SERIAL NOT NULL,
        user_name VARCHAR(40) NOT NULL,
        PRIMARY KEY (user_id)
    )

    select conname from pg_constraint where conname='cst_user_name_length'
    ALTER TABLE users ADD CONSTRAINT cst_user_name_length  CHECK (length(user_name) >= 8)
    sqlusers.drop(engine)
    select conname from pg_constraint where conname='cst_user_name_length'
    ALTER TABLE users DROP CONSTRAINT cst_user_name_length
    DROP TABLE users

While the above example is against the built-in [`AddConstraint`](#sqlalchemy.schema.AddConstraint "sqlalchemy.schema.AddConstraint")
and [`DropConstraint`](#sqlalchemy.schema.DropConstraint "sqlalchemy.schema.DropConstraint")
objects, the main usefulness of DDL events for now remains focused on
the use of the [`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL") construct
itself, as well as with user-defined subclasses of [`DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")
that aren’t already part of the [`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all"),
[`Table.create()`](metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create"),
and corresponding “drop” processes.

DDL 表达式构造 API [¶](#ddl-expression-constructs-api "Permalink to this headline")
---------------------------------------------------------------------------------

 `sqlalchemy.schema.`{.descclassname}`sort_tables`{.descname}(*tables*, *skip\_fn=None*, *extra\_dependencies=None*)[¶](#sqlalchemy.schema.sort_tables "Permalink to this definition")
:   根据依赖关系排序[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的集合。

    这是一个依赖排序的排序，它将发射[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，以便它们将遵循其依赖的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。根据[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象的存在以及[`Table.add_is_dependent_on()`](metadata.html#sqlalchemy.schema.Table.add_is_dependent_on "sqlalchemy.schema.Table.add_is_dependent_on")添加的显式依赖关系，表依赖于另一个表。plain

    警告

    The [`sort_tables()`](#sqlalchemy.schema.sort_tables "sqlalchemy.schema.sort_tables")
    function cannot by itself accommodate automatic resolution of
    dependency cycles between tables, which are usually caused by
    mutually dependent foreign key constraints.
    要解决这些循环，可以将[`ForeignKeyConstraint.use_alter`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")参数应用于这些约束，或者使用`sql.sort_tables_and_constraints()`函数来打破涉及分开循环。

    参数：

    -   **tables**[¶](#sqlalchemy.schema.sort_tables.params.tables) – a
        sequence of [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        objects.
    -   **skip\_fn**[¶](#sqlalchemy.schema.sort_tables.params.skip_fn) –
        optional callable which will be passed a [`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
        object; if it returns True, this constraint will not be
        considered as a dependency. Note this is **different** from the
        same parameter in [`sort_tables_and_constraints()`](#sqlalchemy.schema.sort_tables_and_constraints "sqlalchemy.schema.sort_tables_and_constraints"),
        which is instead passed the owning [`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
        object.
    -   **extra\_dependencies**
        [¶](#sqlalchemy.schema.sort_tables.params.extra_dependencies) -
        表格的2元组序列，也将被视为相互依赖。

    也可以看看

    [`sort_tables_and_constraints()`](#sqlalchemy.schema.sort_tables_and_constraints "sqlalchemy.schema.sort_tables_and_constraints")

    `MetaData.sorted_tables()` -
    uses this function to sort

 `sqlalchemy.schema.`{.descclassname}`sort_tables_and_constraints`{.descname}(*tables*, *filter\_fn=None*, *extra\_dependencies=None*)[¶](#sqlalchemy.schema.sort_tables_and_constraints "Permalink to this definition")
:   对[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    / [`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象的集合进行排序。

    这是一个依赖排序的排序，它将发出`（Table， [ForeignKeyConstraint， ...]）  t0的元组>使得每个Table`遵循其依赖的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。Remaining
    [`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    objects that are separate due to dependency rules not satisifed by
    the sort are emitted afterwards as
    `(None, [ForeignKeyConstraint ...])`.

    Tables are dependent on another based on the presence of
    [`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    objects, explicit dependencies added by
    [`Table.add_is_dependent_on()`](metadata.html#sqlalchemy.schema.Table.add_is_dependent_on "sqlalchemy.schema.Table.add_is_dependent_on"),
    as well as dependencies stated here using the [`skip_fn`](#sqlalchemy.schema.sort_tables_and_constraints.params.skip_fn "sqlalchemy.schema.sort_tables_and_constraints")
    and/or [`extra_dependencies`](#sqlalchemy.schema.sort_tables_and_constraints.params.extra_dependencies "sqlalchemy.schema.sort_tables_and_constraints")
    parameters.

    参数：

    -   **tables**[¶](#sqlalchemy.schema.sort_tables_and_constraints.params.tables)
        – a sequence of [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        objects.
    -   **filter\_fn**[¶](#sqlalchemy.schema.sort_tables_and_constraints.params.filter_fn)
        – optional callable which will be passed a
        [`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
        object, and returns a value based on whether this constraint
        should definitely be included or excluded as an inline
        constraint, or neither.
        如果它返回False，那么这个约束肯定会被包含作为一个不受ALTER约束的依赖；如果为True，则仅在**结尾处包含**作为ALTER结果。返回无意味着约束被包含在基于表格的结果中，除非它被检测为依赖周期的一部分。
    -   **extra\_dependencies**
        [¶](#sqlalchemy.schema.sort_tables_and_constraints.params.extra_dependencies)
        - 表格的2元组序列，也将被视为相互依赖。

    版本1.0.0中的新功能

    也可以看看

    [`sort_tables()`](#sqlalchemy.schema.sort_tables "sqlalchemy.schema.sort_tables")

*class* `sqlalchemy.schema。`{.descclassname} `DDLElement`{.descname} [¶](#sqlalchemy.schema.DDLElement "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，`sqlalchemy.schema._DDLCompiles`

    DDL表达式构造的基类。plainplainplain

    This class is the base for the general purpose [`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL") class, as
    well as the various create/drop clause constructs such as
    [`CreateTable`](#sqlalchemy.schema.CreateTable "sqlalchemy.schema.CreateTable"),
    [`DropTable`](#sqlalchemy.schema.DropTable "sqlalchemy.schema.DropTable"),
    [`AddConstraint`](#sqlalchemy.schema.AddConstraint "sqlalchemy.schema.AddConstraint"),
    etc.

    [`DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")与[Events](event.html)中介绍的SQLAlchemy事件紧密集成。一个实例本身就是一个接收可调用的事件：

        event.listen(
            users,
            'after_create',
            AddConstraint(constraint).execute_if(dialect='postgresql')
        )

    也可以看看

    [`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL")

    [`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")

    [Events](event.html)

    [Controlling DDL Sequences](#schema-ddl-sequences)

    `__ call __`{.descname} （ *target*，*bind*，*\*\* kw* T5\> [¶ T6\>](#sqlalchemy.schema.DDLElement.__call__ "Permalink to this definition")
    :   以ddl\_listener的身份执行DDL。

    `针对 T0> （ T1> 靶 T2> ） T3> ¶ T4>`{.descname}
    :   针对特定模式项目返回此DDL的副本。

    `结合 T0> ¶ T1>`{.descname}
    :   

    `callable _`{.descname} *=无* [¶](#sqlalchemy.schema.DDLElement.callable_ "Permalink to this definition")
    :   

    `方言`{.descname} *=无* [¶](#sqlalchemy.schema.DDLElement.dialect "Permalink to this definition")
    :   

     `execute`{.descname}(*bind=None*, *target=None*)[¶](#sqlalchemy.schema.DDLElement.execute "Permalink to this definition")
    :   立即执行此DDL。

        如果未提供，则使用分配给`.bind`属性的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")或[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")执行DDL语句。如果DDL在标准上有条件的`on`

        参数：

        -   **bind**[¶](#sqlalchemy.schema.DDLElement.execute.params.bind)
            – Optional, an `Engine` or
            `Connection`.
            如果未提供，则必须在`.bind`属性中存在有效的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")。
        -   **target**
            [¶](#sqlalchemy.schema.DDLElement.execute.params.target) -
            可选，默认为None。执行调用的目标SchemaItem。将被传递给`on`
            callable（如果有），并且还可以为该语句提供字符串扩展数据。有关更多信息，请参阅`execute_at`。

     `execute_at`{.descname}(*event\_name*, *target*)[¶](#sqlalchemy.schema.DDLElement.execute_at "Permalink to this definition")
    :   将此DDL的执行链接到SchemaItem的DDL生命周期。

        从版本0.7开始弃用：请参阅[`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")以及[`DDLElement.execute_if()`](#sqlalchemy.schema.DDLElement.execute_if "sqlalchemy.schema.DDLElement.execute_if")。

        将此`DDLElement`链接到`Table`或`MetaData`实例，并在该架构项创建或删除时执行该实例。DDL语句将使用与表创建/删除本身相同的连接和事务上下文来执行。该语句的`.bind`属性被忽略。

        参数：

        -   **event**[¶](#sqlalchemy.schema.DDLElement.execute_at.params.event)
            – One of the events defined in the schema item’s
            `.ddl_events`; e.g. ‘before-create’,
            ‘after-create’, ‘before-drop’ or ‘after-drop’
        -   **target**[¶](#sqlalchemy.schema.DDLElement.execute_at.params.target)
            – The Table or MetaData instance for which this DDLElement
            will be associated with.

        DDLElement实例可以链接到任意数量的模式项目。

        `execute_at`建立在[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")和[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的`append_ddl_listener`接口上。

        警告：创建或删除独立的表也会触发任何DDL设置为`execute_at`表的元数据。这可能会在未来的版本中发生变化。

    `execute_if`{.descname} （ *dialect = None*，*callable\_ = None*，*state = None* ） T5\> [¶ T6\>](#sqlalchemy.schema.DDLElement.execute_if "Permalink to this definition")
    :   返回可执行此DDLElement的可调用对象。

        用于提供事件监听的包装：

            event.listen(
                        metadata,
                        'before_create',
                        DDL("my_ddl").execute_if(dialect='postgresql')
                    )

        参数：

        -   **dialect**
            [¶](#sqlalchemy.schema.DDLElement.execute_if.params.dialect)
            -

            可能是一个字符串，元组或可调用谓词。如果是字符串，则会将其与正在执行的数据库方言的名称进行比较：

                DDL('something').execute_if(dialect='postgresql')

            如果一个元组指定多个方言名称：

                DDL('something').execute_if(dialect=('postgresql', 'mysql'))

        -   **callable \_**
            [¶](#sqlalchemy.schema.DDLElement.execute_if.params.callable_)
            -

            一个可调用的对象，它将被调用四个位置参数以及可选的关键字参数：

            > DDL：
            > 这个DDL元素。
            > 目标：
            > [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象是此事件的目标。如果DDL是明确执行的，可能是None。
            > 绑定：
            > 用于DDL执行的[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            > 表：
            > 可选关键字参数 -
            > 要在MetaData.create\_all()或drop\_all()方法调用中创建/删除的Table对象的列表。
            > 州：
            > 可选的关键字参数 - 将成为传递给此函数的`state`参数。
            > checkfirst：
            > Keyword argument, will be True if the ‘checkfirst’ flag
            > was set during the call to `create()`,
            > `create_all()`, `drop()`, `drop_all()`.

            如果callable返回一个真值，则会执行DDL语句。

        -   **state**[¶](#sqlalchemy.schema.DDLElement.execute_if.params.state)
            – any value which will be passed to the callable\_ as the
            `state` keyword argument.

        也可以看看

        [`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")

        [Events](event.html)

    `on`{.descname} *=无* [¶](#sqlalchemy.schema.DDLElement.on "Permalink to this definition")
    :   

    `目标`{.descname} *=无* [¶](#sqlalchemy.schema.DDLElement.target "Permalink to this definition")
    :   

*class* `sqlalchemy.schema。`{.descclassname} `DDL`{.descname} （ *语句*，*on =无 context = None，*bind = None* ） [¶](#sqlalchemy.schema.DDL "Permalink to this definition")*
:   基础：[`sqlalchemy.schema.DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")

    一个文字DDL语句。

    指定要由数据库执行的文字SQL
    DDL。DDL对象充当DDL事件侦听器，可以使用[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象作为目标来订阅[`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")中列出的事件。基本模板支持允许单个DDL实例处理多个表的重复任务。

    例子：

        from sqlalchemy import event, DDL

        tbl = Table('users', metadata, Column('uid', Integer))
        event.listen(tbl, 'before_create', DDL('DROP TRIGGER users_trigger'))

        spow = DDL('ALTER TABLE %(table)s SET secretpowers TRUE')
        event.listen(tbl, 'after_create', spow.execute_if(dialect='somedb'))

        drop_spow = DDL('ALTER TABLE users SET secretpowers FALSE')
        connection.execute(drop_spow)

    在Table事件上进行操作时，可以使用以下`statement`字符串替换：

        %(table)s  - the Table name, with any required quoting applied
        %(schema)s - the schema name, with any required quoting applied
        %(fullname)s - the Table name including schema, quoted if needed

    DDL的“上下文”（如果有的话）将与上述标准替换结合使用。上下文中出现的键将覆盖标准替换。

     `__init__`{.descname}(*statement*, *on=None*, *context=None*, *bind=None*)[¶](#sqlalchemy.schema.DDL.__init__ "Permalink to this definition")
    :   创建一个DDL语句。

        参数：

        -   **语句** [¶](#sqlalchemy.schema.DDL.params.statement) -

            要执行的字符串或unicode字符串。语句将用Python的字符串格式化操作符处理。请参阅`context`参数和`execute_at`方法。

            语句中的文字'％'必须转义为'%%'。

            SQL绑定参数在DDL语句中不可用。

        -   **on** [¶](#sqlalchemy.schema.DDL.params.on) -

            从版本0.7开始弃用：请参阅[`DDLElement.execute_if()`](#sqlalchemy.schema.DDLElement.execute_if "sqlalchemy.schema.DDLElement.execute_if")。

            可选的过滤标准。可能是一个字符串，元组或可调用谓词。如果是字符串，则会将其与正在执行的数据库方言的名称进行比较：

                DDL('something', on='postgresql')

            如果一个元组指定多个方言名称：

                DDL('something', on=('postgresql', 'mysql'))

            如果是可调用的，则会调用四个位置参数以及可选的关键字参数：

            > DDL：
            > 这个DDL元素。
            > 事件：
            > 触发此DDL的事件的名称，例如'after-create'如果显式执行DDL，则为None。
            > 目标：
            > `Table`或`MetaData`对象是此事件的目标。如果DDL是明确执行的，可能是None。
            > 连接：
            > 用于DDL执行的`Connection`
            > 表：
            > 可选关键字参数 -
            > 要在MetaData.create\_all()或drop\_all()方法调用中创建/删除的Table对象的列表。

            如果callable返回一个真值，则会执行DDL语句。

        -   **上下文** [¶](#sqlalchemy.schema.DDL.params.context) -
            可选字典，默认为None。这些值将可用于DDL语句中的字符串替换。
        -   **绑定** [¶](#sqlalchemy.schema.DDL.params.bind) -
            可选。一个[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")，当`execute()`没有绑定参数时被调用时默认使用。

        也可以看看

        [`DDLEvents`](events.html#sqlalchemy.events.DDLEvents "sqlalchemy.events.DDLEvents")

        [Events](event.html)

 *class*`sqlalchemy.schema.`{.descclassname}`_CreateDropBase`{.descname}(*element*, *on=None*, *bind=None*)[¶](#sqlalchemy.schema._CreateDropBase "Permalink to this definition")
:   基础：[`sqlalchemy.schema.DDLElement`](#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")

    表示CREATE和DROP或等价物的DDL结构的基类。plainplain

    \_CreateDropBase的常见主题是单个`element`属性，它指向要创建或删除的元素。

 *class*`sqlalchemy.schema.`{.descclassname}`CreateTable`{.descname}(*element*, *on=None*, *bind=None*, *include\_foreign\_key\_constraints=None*)[¶](#sqlalchemy.schema.CreateTable "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示一个CREATE TABLE语句。plain

     `__init__`{.descname}(*element*, *on=None*, *bind=None*, *include\_foreign\_key\_constraints=None*)[¶](#sqlalchemy.schema.CreateTable.__init__ "Permalink to this definition")
    :   创建一个[`CreateTable`](#sqlalchemy.schema.CreateTable "sqlalchemy.schema.CreateTable")结构。

        参数：

        -   **element**[¶](#sqlalchemy.schema.CreateTable.params.element)
            – a [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            that’s the subject of the CREATE
        -   **on**[¶](#sqlalchemy.schema.CreateTable.params.on) – See
            the description for ‘on’ in [`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL").
        -   **bind**[¶](#sqlalchemy.schema.CreateTable.params.bind) –
            See the description for ‘bind’ in [`DDL`](#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL").
        -   **include\_foreign\_key\_constraints**
            [¶](#sqlalchemy.schema.CreateTable.params.include_foreign_key_constraints)
            -

            将被包含在CREATE结构内的[`ForeignKeyConstraint`](constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象的可选序列；如果省略，则包含所有未指定use\_alter
            = True的外键约束。

            版本1.0.0中的新功能

 *class*`sqlalchemy.schema.`{.descclassname}`DropTable`{.descname}(*element*, *on=None*, *bind=None*)[¶](#sqlalchemy.schema.DropTable "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示DROP TABLE语句。

*class* `sqlalchemy.schema。`{.descclassname} `CreateColumn`{.descname} （ *元素* ） t5 \> [¶ T6\>](#sqlalchemy.schema.CreateColumn "Permalink to this definition")
:   基础：`sqlalchemy.schema._DDLCompiles`

    将[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")表示为通过[`CreateTable`](#sqlalchemy.schema.CreateTable "sqlalchemy.schema.CreateTable")结构呈现在CREATE
    TABLE语句中。

    通过使用[Custom SQL Constructs and Compilation
    Extension](compiler.html)中介绍的编译器扩展来扩展[`CreateColumn`](#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")，可以在CREATE
    TABLE语句的生成过程中支持自定义列DDL。

    典型的集成是检查传入的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，并在找到特定标志或条件时重定向编译：

        from sqlalchemy import schema
        from sqlalchemy.ext.compiler import compiles

        @compiles(schema.CreateColumn)
        def compile(element, compiler, **kw):
            column = element.element

            if "special" not in column.info:
                return compiler.visit_create_column(element, **kw)

            text = "%s SPECIAL DIRECTIVE %s" % (
                    column.name,
                    compiler.type_compiler.process(column.type)
                )
            default = compiler.get_column_default_string(column)
            if default is not None:
                text += " DEFAULT " + default

            if not column.nullable:
                text += " NOT NULL"

            if column.constraints:
                text += " ".join(
                            compiler.process(const)
                            for const in column.constraints)
            return text

    上述构造可以应用于[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，如下所示：

        from sqlalchemy import Table, Metadata, Column, Integer, String
        from sqlalchemy import schema

        metadata = MetaData()

        table = Table('mytable', MetaData(),
                Column('x', Integer, info={"special":True}, primary_key=True),
                Column('y', String(50)),
                Column('z', String(20), info={"special":True})
            )

        metadata.create_all(conn)

    以上，我们添加到[`Column.info`{](metadata.html#sqlalchemy.schema.Column.info "sqlalchemy.schema.Column.info")集合的指令将被我们的自定义编译方案检测到：

        CREATE TABLE mytable (
                x SPECIAL DIRECTIVE INTEGER NOT NULL,
                y VARCHAR(50),
                z SPECIAL DIRECTIVE VARCHAR(20),
            PRIMARY KEY (x)
        )

    当生成`CREATE TABLE`时，[`CreateColumn`](#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")结构也可用于跳过某些列。这是通过创建有条件地返回`None`的编译规则来完成的。这基本上是如何产生与在[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")上使用`system=True`参数相同的效果，它将列标记为隐式存在的“系统”列。

    例如，假设我们希望产生一个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，该表跳过Postgresql后端对Postgresql
    `xmin`列的渲染，但是在其他后端确实呈现它，预期触发规则。条件编译规则可以仅在Postgresql上跳过此名称：

        from sqlalchemy.schema import CreateColumn

        @compiles(CreateColumn, "postgresql")
        def skip_xmin(element, compiler, **kw):
            if element.element.name == 'xmin':
                return None
            else:
                return compiler.visit_create_column(element, **kw)


        my_table = Table('mytable', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('xmin', Integer)
                )

    以上，一个[`CreateTable`](#sqlalchemy.schema.CreateTable "sqlalchemy.schema.CreateTable")结构将产生一个`CREATE TABLE`，其中只包含`id`字符串中的列；
    `xmin`列将被省略，但仅针对Postgresql后端。

    0.8.3版中的新功能 [`CreateColumn`](#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")构造支持通过从自定义编译规则返回`None`跳过列。

    0.8版新增：添加了[`CreateColumn`](#sqlalchemy.schema.CreateColumn "sqlalchemy.schema.CreateColumn")结构以支持自定义列创建样式。

 *class*`sqlalchemy.schema.`{.descclassname}`CreateSequence`{.descname}(*element*, *on=None*, *bind=None*)[¶](#sqlalchemy.schema.CreateSequence "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示一个CREATE SEQUENCE语句。

 *class*`sqlalchemy.schema.`{.descclassname}`DropSequence`{.descname}(*element*, *on=None*, *bind=None*)[¶](#sqlalchemy.schema.DropSequence "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示DROP SEQUENCE语句。plain

 *class*`sqlalchemy.schema.`{.descclassname}`CreateIndex`{.descname}(*element*, *on=None*, *bind=None*)[¶](#sqlalchemy.schema.CreateIndex "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示CREATE INDEX语句。plain

 *class*`sqlalchemy.schema.`{.descclassname}`DropIndex`{.descname}(*element*, *on=None*, *bind=None*)[¶](#sqlalchemy.schema.DropIndex "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    代表DROP INDEX语句。plain

*class* `sqlalchemy.schema。`{.descclassname} `AddConstraint`{.descname} （ *元素*，*/ t5\>，*\*\* kw* ） [¶](#sqlalchemy.schema.AddConstraint "Permalink to this definition")*
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示ALTER TABLE ADD CONSTRAINT语句。

*class* `sqlalchemy.schema。`{.descclassname} `DropConstraint`{.descname} （ *元素*，*cascade = False*，*\*\* kw* ） [¶](#sqlalchemy.schema.DropConstraint "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示一个ALTER TABLE DROP CONSTRAINT语句。plain

*class* `sqlalchemy.schema。`{.descclassname} `CreateSchema`{.descname} （ *name*，*quote =无*，*\*\* kw* ） [¶](#sqlalchemy.schema.CreateSchema "Permalink to this definition")
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    表示CREATE SCHEMA语句。

    New in version 0.7.4.

    这里的参数是模式的字符串名称。

    `__ init __`{.descname} （ *name*，*quote =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.schema.CreateSchema.__init__ "Permalink to this definition")
    :   创建一个新的[`CreateSchema`](#sqlalchemy.schema.CreateSchema "sqlalchemy.schema.CreateSchema")结构。

*class* `sqlalchemy.schema。`{.descclassname} `DropSchema`{.descname} （ *name*，*quote =无cascade = False，*\*\* kw* ） [¶](#sqlalchemy.schema.DropSchema "Permalink to this definition")*
:   基础：[`sqlalchemy.schema._CreateDropBase`](#sqlalchemy.schema._CreateDropBase "sqlalchemy.schema._CreateDropBase")

    代表DROP SCHEMA语句。

    这里的参数是模式的字符串名称。

    New in version 0.7.4.

     `__init__`{.descname}(*name*, *quote=None*, *cascade=False*, *\*\*kw*)[¶](#sqlalchemy.schema.DropSchema.__init__ "Permalink to this definition")
    :   创建一个新的[`DropSchema`](#sqlalchemy.schema.DropSchema "sqlalchemy.schema.DropSchema")结构。


