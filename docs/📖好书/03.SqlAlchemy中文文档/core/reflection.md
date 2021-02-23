---
title: reflection
date: 2021-02-20 22:41:35
permalink: /pages/86437b/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
反映数据库对象[¶](#reflecting-database-objects "Permalink to this headline")
============================================================================

可以指示[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象从数据库中已有的相应数据库模式对象加载有关其自身的信息。这个过程被称为*反射*。在最简单的情况下，你只需要指定表名，一个[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象和`autoload=True`标志。如果[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")不是永久绑定的，还要添加`autoload_with`参数：

    >>> messages = Table('messages', meta, autoload=True, autoload_with=engine)
    >>> [c.name for c in messages.columns]
    ['message_id', 'message_name', 'date']

上面的操作将使用给定的引擎来查询数据库中有关`messages`表的信息，然后将生成[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")，[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")和其他与此信息相对应的对象就好像[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象是在Python中手动构造的。

当表被反映时，如果给定的表通过外键引用另一个表，则在表示连接的[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象内创建第二个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。在下面，假设表`shopping_cart_items`引用了一个名为`shopping_carts`的表。反映`shopping_cart_items`表的作用是：`shopping_carts`表也将被加载：

    >>> shopping_cart_items = Table('shopping_cart_items', meta, autoload=True, autoload_with=engine)
    >>> 'shopping_carts' in meta.tables:
    True

The [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
has an interesting “singleton-like” behavior such that if you requested
both tables individually, [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
will ensure that exactly one [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
object is created for each distinct table name.
如果已经存在具有给定名称的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造函数实际返回已存在的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。如下所示，我们可以通过命名它来访问已经生成的`shopping_carts`表：

    shopping_carts = Table('shopping_carts', meta)

当然，无论如何，对上表使用`autoload=True`是个好主意。这是为了如果表格的属性尚未被加载。自动加载操作只发生在表中，如果它尚未加载；一旦加载，具有相同名称的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的新调用将不会重新发出任何反射查询。

覆盖反射列[¶](#overriding-reflected-columns "Permalink to this headline")
-------------------------------------------------------------------------

反映表时，可以使用显式值重写单个列；这对指定自定义数据类型，例如可能未在数据库中配置的主键等约束很方便。:

    >>> mytable = Table('mytable', meta,
    ... Column('id', Integer, primary_key=True),   # override reflected 'id' to have primary key
    ... Column('mydata', Unicode(50)),    # override reflected 'mydata' to be Unicode
    ... autoload=True)

反映意见[¶](#reflecting-views "Permalink to this headline")
-----------------------------------------------------------

反射系统也可以反映意见。基本用法与表格的基本用法相同：

    my_view = Table("some_view", metadata, autoload=True)

Above, `my_view` is a [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
object with [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
objects representing the names and types of each column within the view
“some\_view”.

通常，在反映视图时至少需要一个主键约束，如果不是外键也是如此。视图反射不会推断这些限制。

为此，使用“覆盖”技术，明确指定那些属于主键或具有外键约束的列：

    my_view = Table("some_view", metadata,
                    Column("view_id", Integer, primary_key=True),
                    Column("related_thing", Integer, ForeignKey("othertable.thing_id")),
                    autoload=True
    )

一次反映所有表[¶](#reflecting-all-tables-at-once "Permalink to this headline")
------------------------------------------------------------------------------

The [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
object can also get a listing of tables and reflect the full set.
这是通过使用[`reflect()`](metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")方法实现的。调用它之后，所有定位的表格都存在于[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象的表格字典中：

    meta = MetaData()
    meta.reflect(bind=someengine)
    users_table = meta.tables['users']
    addresses_table = meta.tables['addresses']

`metadata.reflect()` also provides a handy way to
clear or delete all the rows in a database:

    meta = MetaData()
    meta.reflect(bind=someengine)
    for table in reversed(meta.sorted_tables):
        someengine.execute(table.delete())

使用Inspector [¶](#fine-grained-reflection-with-inspector "Permalink to this headline")进行细粒度反射
-----------------------------------------------------------------------------------------------------

还提供一个低级别接口，它提供了从给定数据库加载架构，表，列和约束描述列表的后端不可知系统。这被称为“检查员”：

    from sqlalchemy import create_engine
    from sqlalchemy.engine import reflection
    engine = create_engine('...')
    insp = reflection.Inspector.from_engine(engine)
    print(insp.get_table_names())

 *class*`sqlalchemy.engine.reflection.`{.descclassname}`Inspector`{.descname}(*bind*)[¶](#sqlalchemy.engine.reflection.Inspector "Permalink to this definition")
:   执行数据库模式检查。

    The Inspector acts as a proxy to the reflection methods of the
    [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect"),
    providing a consistent interface as well as caching support for
    previously fetched metadata.

    通常通过[`inspect()`](inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数创建[`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")对象：

        from sqlalchemy import inspect, create_engine
        engine = create_engine('...')
        insp = inspect(engine)

    上述检查方法相当于使用[`Inspector.from_engine()`](#sqlalchemy.engine.reflection.Inspector.from_engine "sqlalchemy.engine.reflection.Inspector.from_engine")方法，即：

        engine = create_engine('...')
        insp = Inspector.from_engine(engine)

    Where above, the [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
    may opt to return an [`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")
    subclass that provides additional methods specific to the dialect’s
    target database.

    ` __初始化__  T0> （ T1> 结合 T2> ） T3> ¶ T4>`{.descname}
    :   初始化一个新的[`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")。

        参数：

        **bind**[¶](#sqlalchemy.engine.reflection.Inspector.params.bind)
        – a [`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable"),
        which is typically an instance of [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
        or [`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection").

        对于[`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")的特定于方言的实例，请参阅[`Inspector.from_engine()`](#sqlalchemy.engine.reflection.Inspector.from_engine "sqlalchemy.engine.reflection.Inspector.from_engine")

    ` default_schema_name  T0> ¶ T1>`{.descname}
    :   返回当前引擎的数据库用户的方言提供的默认模式名称。

        例如。对于SQL Server，这通常是Postgresql和`dbo`的`public`。

     *classmethod*`from_engine`{.descname}(*bind*)[¶](#sqlalchemy.engine.reflection.Inspector.from_engine "Permalink to this definition")
    :   从给定的引擎或连接构造一个新的特定于方言的Inspector对象。

        参数：

        **bind**[¶](#sqlalchemy.engine.reflection.Inspector.from_engine.params.bind)
        – a [`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable"),
        which is typically an instance of [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
        or [`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection").

        此方法不同于直接构造函数调用[`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")，因为[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")有机会提供特定于方言的[`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")实例，它可能会提供其他方法。

        请参阅[`Inspector`](#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")中的示例。

    `get_check_constraints`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_check_constraints "Permalink to this definition")
    :   在table\_name中返回有关检查约束的信息。

        给定一个字符串table\_name和一个可选字符串schema，将检查约束信息返回为带有这些键的字典列表：

        名称
        :   检查约束的名称
        SQLTEXT
        :   检查约束的SQL表达式

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_check_constraints.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_check_constraints.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

        版本1.1.0中的新功能

    `get_columns`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_columns "Permalink to this definition")
    :   返回有关table\_name中列的信息。

        给定一个字符串table\_name和一个可选字符串schema，将列信息返回为带有这些键的字典列表：

        名称
        :   该列的名称
        类型
        :   [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        可空
        :   布尔
        默认
        :   该列的默认值
        ATTRS
        :   包含可选列属性的字典

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_columns.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_columns.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    `get_foreign_keys`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_foreign_keys "Permalink to this definition")
    :   在table\_name中返回有关foreign\_keys的信息。

        给定一个字符串table\_name和一个可选字符串schema，将外键信息作为具有这些键的字典列表返回：

        constrained\_columns
        :   构成外键的列名称列表
        referred\_schema
        :   被引用模式的名称
        referred\_table
        :   被引用表的名称
        referred\_columns
        :   引用表中与constrained\_columns对应的列名称列表
        名称
        :   外键约束的可选名称。

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_foreign_keys.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_foreign_keys.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    `get_indexes`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_indexes "Permalink to this definition")
    :   返回有关table\_name中索引的信息。

        给定一个字符串table\_name和一个可选字符串schema，将索引信息返回为带有这些键的字典列表：

        名称
        :   该索引的名称
        COLUMN\_NAMES
        :   按列顺序排列列表
        独特
        :   布尔
        dialect\_options
        :   方言特定索引选项的字典。所有方言可能不存在。

            版本1.0.0中的新功能

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_indexes.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_indexes.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    `get_pk_constraint`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_pk_constraint "Permalink to this definition")
    :   返回有关table\_name上主键约束的信息。

        给定一个字符串table\_name和一个可选字符串schema，将主键信息作为字典返回以下键：

        constrained\_columns
        :   构成主键的列名称列表
        名称
        :   主键约束的可选名称。

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_pk_constraint.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_pk_constraint.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    `get_primary_keys`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_primary_keys "Permalink to this definition")
    :   返回有关table\_name中主键的信息。

        从版本0.7开始弃用：调用已弃用的方法get\_primary\_keys。改为使用get\_pk\_constraint。

        给定一个字符串table\_name和一个可选字符串schema，以列名称的形式返回主键信息。

    ` get_schema_names  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回所有模式名称。

    ` get_sorted_table_and_fkc_names  T0> （ T1> 架构=无 T2> ） T3> ¶ T4>`{.descname}
    :   返回特定模式中引用的依赖关系排序表和外键约束名称。

        这将产生`（tablename， [（tname， fkname）， （tname， t4）的2元组> fkname）， ...]）`由CREATE顺序中的表名组成，它们与未检测为属于周期的外键约束名称。The
        final element will be
        `(None, [(tname, fkname), (tname, fkname), ..])` which will consist of remaining foreign key constraint
        names that would require a separate CREATE step after-the-fact,
        based on dependencies between tables.

        1.0版本中的新功能

        也可以看看

        [`Inspector.get_table_names()`](#sqlalchemy.engine.reflection.Inspector.get_table_names "sqlalchemy.engine.reflection.Inspector.get_table_names")

        [`sort_tables_and_constraints()`](ddl.html#sqlalchemy.schema.sort_tables_and_constraints "sqlalchemy.schema.sort_tables_and_constraints") - similar method which works
        :   与已经给出的[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")。

     `get_table_names`{.descname}(*schema=None*, *order\_by=None*)[¶](#sqlalchemy.engine.reflection.Inspector.get_table_names "Permalink to this definition")
    :   返回特定模式中引用的所有表名称。

        预计这些名称只是真实的表格，而不是视图。而是使用[`Inspector.get_view_names()`](#sqlalchemy.engine.reflection.Inspector.get_view_names "sqlalchemy.engine.reflection.Inspector.get_view_names")方法返回视图。

        参数：

        -   **架构**
            [¶](#sqlalchemy.engine.reflection.Inspector.get_table_names.params.schema)
            - 架构名称。如果`schema`留在`None`中，则使用数据库的默认模式，否则搜索指定的模式。如果数据库不支持命名模式，那么如果`schema`未作为`None`传递，则行为未定义。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **order\_by**
            [¶](#sqlalchemy.engine.reflection.Inspector.get_table_names.params.order_by)
            -

            可选的，可能是字符串“foreign\_key”对外键依赖项的结果进行排序。不会自动解决循环，并且如果循环存在，将会引发[`CircularDependencyError`](exceptions.html#sqlalchemy.exc.CircularDependencyError "sqlalchemy.exc.CircularDependencyError")。

            从版本1.0.0开始弃用： -
            请参阅[`Inspector.get_sorted_table_and_fkc_names()`](#sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names "sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names")，以便自动解析表之间的外键循环。

            在版本0.8中更改：“foreign\_key”排序按依赖顺序对依赖项进行排序；即按照创建顺序，而不是按降序排列。这是为了与类似的功能保持一致，例如[`MetaData.sorted_tables`](metadata.html#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")和`util.sort_tables()`。

        也可以看看

        [`Inspector.get_sorted_table_and_fkc_names()`](#sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names "sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names")

        [`MetaData.sorted_tables`](metadata.html#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")

    `get_table_options`{.descname} （ *table\_name*，*schema =无*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.get_table_options "Permalink to this definition")
    :   返回创建给定名称的表时指定的选项字典。

        这当前包括一些适用于MySQL表的选项。

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_table_options.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_table_options.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    ` get_temp_table_names  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回当前绑定的临时表名称列表。

        大多数方言都不支持这种方法；目前只有SQLite实现它。

        版本1.0.0中的新功能

    ` get_temp_view_names  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回当前绑定的临时视图名称列表。

        大多数方言都不支持这种方法；目前只有SQLite实现它。

        版本1.0.0中的新功能

    ` get_unique_constraints  T0> （ T1> 表名 T2>，架构=无 T3>， **千瓦 T4> ）  T5> ¶ T6>`{.descname}
    :   返回关于table\_name中的唯一约束的信息。

        给定一个字符串table\_name和一个可选的字符串schema，返回唯一约束信息作为具有这些键的字典列表：

        名称
        :   唯一约束的名称
        COLUMN\_NAMES
        :   按列顺序排列列表

        参数：

        -   **table\_name**[¶](#sqlalchemy.engine.reflection.Inspector.get_unique_constraints.params.table_name)
            – string name of the table.
            对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **架构**
            [](#sqlalchemy.engine.reflection.Inspector.get_unique_constraints.params.schema)
            -
            字符串架构名称；如果省略，则使用数据库连接的默认模式。对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

        0.8.4版本中的新功能

    `get_view_definition`{.descname} （ *view\_name*，*schema =无* ） [t5 \>](#sqlalchemy.engine.reflection.Inspector.get_view_definition "Permalink to this definition")
    :   返回view\_name的定义。

        参数：

        **schema**[¶](#sqlalchemy.engine.reflection.Inspector.get_view_definition.params.schema)
        – Optional, retrieve names from a non-default schema.
        对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    ` get_view_names  T0> （ T1> 架构=无 T2> ） T3> ¶ T4>`{.descname}
    :   返回schema中的所有视图名称。

        参数：

        **schema**[¶](#sqlalchemy.engine.reflection.Inspector.get_view_names.params.schema)
        – Optional, retrieve names from a non-default schema.
        对于特殊引用，请使用[`quoted_name`](sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。

    `可反映`{.descname} （ *表*，*include\_columns*，*exclude\_columns =()* / T5\> [¶ T6\>](#sqlalchemy.engine.reflection.Inspector.reflecttable "Permalink to this definition")
    :   给定一个Table对象，根据内省加载它的内部结构。

        这是大多数方言用来产生表反射的基本方法。直接用法如下所示：

            from sqlalchemy import create_engine, MetaData, Table
            from sqlalchemy.engine import reflection

            engine = create_engine('...')
            meta = MetaData()
            user_table = Table('user', meta)
            insp = Inspector.from_engine(engine)
            insp.reflecttable(user_table, None)

        参数：

        -   **table**[¶](#sqlalchemy.engine.reflection.Inspector.reflecttable.params.table)
            – a [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            instance.
        -   **include\_columns**
            [¶](#sqlalchemy.engine.reflection.Inspector.reflecttable.params.include_columns)
            -
            要包含在反射过程中的字符串列名称的列表。如果`None`，则会反映所有列。

反射的限制[¶](#limitations-of-reflection "Permalink to this headline")
----------------------------------------------------------------------

需要注意的是，反射过程仅使用关系数据库中表示的信息重新创建[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")元数据。按定义，此过程无法还原实际上未存储在数据库中的模式的各个方面。无法反映的国家包括但不限于：

-   客户端默认值是Python函数或使用[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的`default`关键字定义的SQL表达式（注意，这与`server_default`不同，具体是什么可通过反射获得）。
-   列信息，例如可能已放入[`Column.info`{](metadata.html#sqlalchemy.schema.Column.info "sqlalchemy.schema.Column.info")字典中的数据
-   [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的`.quote`设置的值
-   特定[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")与给定[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的关联

关系数据库在很多情况下也以与SQLAlchemy中指定的格式不同的格式报告表格元数据。从反射返回的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象不能始终依赖于生成与原始Python定义的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象相同的DDL。None服务器端的默认值可以通过强制转换指令（通常Postgresql将包含一个`::<type>`强制转换）或不同于最初指定的引用模式返回。

另一类限制包括反射仅部分或尚未定义的模式结构。最近对反思的改进允许反映视图，索引和外键选项等内容。在撰写本文时，不会反映CHECK约束，表格注释和触发器等结构。
