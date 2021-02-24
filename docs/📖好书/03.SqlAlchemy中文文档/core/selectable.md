---
title: selectable
date: 2021-02-20 22:41:36
permalink: /sqlalchemy/core/selectable/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
Selectables，Tables，FROM objects [¶](#selectables-tables-from-objects "Permalink to this headline")
====================================================================================================

The term “selectable” refers to any object that rows can be selected
from; in SQLAlchemy, these objects descend from [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
and their distinguishing feature is their [`FromClause.c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
attribute, which is a namespace of all the columns contained within the
FROM clause (these elements are themselves [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
subclasses).

 `sqlalchemy.sql.expression.`{.descclassname}`alias`{.descname}(*selectable*, *name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.alias "Permalink to this definition")
:   返回一个[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象。

    An [`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
    represents any [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    with an alternate name assigned within SQL, typically using the
    `AS` clause when generated, e.g.
    `SELECT * FROM table AS aliasname`.

    类似的功能可以通过所有[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")子类上的[`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")方法使用。

    当从[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象创建[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")时，这会使表格呈现为`tablename AS < / t8> aliasname`。

    For [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    objects, the effect is that of creating a named subquery, i.e.
    `(select ...) AS aliasname`.

    `name`参数是可选的，并提供在呈现的SQL中使用的名称。如果为空，则会在编译时确定性地生成“匿名”名称。确定性意味着该名称对于在同一语句中使用的其他构造是唯一的，并且对于同一个语句对象的每个连续编译也将是相同的名称。

    参数：

    -   **selectable**[¶](#sqlalchemy.sql.expression.alias.params.selectable)
        – any [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        subclass, such as a table, select statement, etc.
    -   **name**[¶](#sqlalchemy.sql.expression.alias.params.name) –
        string name to be assigned as the alias. 如果`None`，则会在编译时确定性地生成名称。
    -   **flat** [¶](#sqlalchemy.sql.expression.alias.params.flat) -

        如果给定的selectable是[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")的实例，请参阅[`Join.alias()`](#sqlalchemy.sql.expression.Join.alias "sqlalchemy.sql.expression.Join.alias")以获取详细信息。

        版本0.9.0中的新功能

 `sqlalchemy.sql.expression.`{.descclassname}`except_`{.descname}(*\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.except_ "Permalink to this definition")
:   返回多个可选项的`EXCEPT`。

    返回的对象是[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的一个实例。plain

    \*选择
    :   [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")实例列表。
    \*\* kwargs
    :   可用的关键字参数与[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")相同。

 `sqlalchemy.sql.expression.`{.descclassname}`except_all`{.descname}(*\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.except_all "Permalink to this definition")
:   返回多个可选项的`EXCEPT ALL`。

    返回的对象是[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的一个实例。

    \*选择
    :   [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")实例列表。
    \*\* kwargs
    :   可用的关键字参数与[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")相同。

 `sqlalchemy.sql.expression.`{.descclassname}`exists`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.exists "Permalink to this definition")
:   针对现有的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象构建新的`Exists`。

    调用样式具有以下形式：

        # use on an existing select()
        s = select([table.c.col1]).where(table.c.col2==5)
        s = exists(s)

        # construct a select() at once
        exists(['*'], **select_arguments).where(criterion)

        # columns argument is optional, generates "EXISTS (SELECT *)"
        # by default.
        exists().where(table.c.col2==5)

 `sqlalchemy.sql.expression.`{.descclassname}`intersect`{.descname}(*\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.intersect "Permalink to this definition")
:   Return an `INTERSECT` of multiple selectables.

    返回的对象是[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的一个实例。

    \*选择
    :   [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")实例列表。
    \*\* kwargs
    :   可用的关键字参数与[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")相同。

 `sqlalchemy.sql.expression.`{.descclassname}`intersect_all`{.descname}(*\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.intersect_all "Permalink to this definition")
:   返回多个可选项的`INTERSECT ALL`。

    返回的对象是[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的一个实例。

    \*选择
    :   [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")实例列表。
    \*\* kwargs
    :   可用的关键字参数与[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")相同。

 `sqlalchemy.sql.expression.`{.descclassname}`join`{.descname}(*left*, *right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.join "Permalink to this definition")
:   给定两个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")表达式，产生一个[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")对象。

    例如。：

        j = join(user_table, address_table,
                 user_table.c.id == address_table.c.user_id)
        stmt = select([user_table]).select_from(j)

    会沿着以下几行发出SQL：

        SELECT user.id, user.name FROM user
        JOIN address ON user.id = address.user_id

    Similar functionality is available given any [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    object (e.g. such as a [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"))
    using the [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
    method.

    参数：

    -   **left** [¶](#sqlalchemy.sql.expression.join.params.left) -
        连接的左侧。
    -   **正确** [¶](#sqlalchemy.sql.expression.join.params.right) -
        连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
    -   **onclause**[¶](#sqlalchemy.sql.expression.join.params.onclause)
        – a SQL expression representing the ON clause of the join.
        如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
    -   **isouter**[¶](#sqlalchemy.sql.expression.join.params.isouter) –
        if True, render a LEFT OUTER JOIN, instead of JOIN.
    -   **完整** [¶](#sqlalchemy.sql.expression.join.params.full) -

        如果为True，则渲染一个FULL OUTER JOIN，而不是JOIN。

        版本1.1中的新功能

    也可以看看

    [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
    - method form, based on a given left side

    [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
    - 生成的对象的类型

 `sqlalchemy.sql.expression.`{.descclassname}`lateral`{.descname}(*selectable*, *name=None*)[¶](#sqlalchemy.sql.expression.lateral "Permalink to this definition")
:   返回一个[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")对象。

    [`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")是一个[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")子类，它表示应用了LATERAL关键字的子查询。

    LATERAL子查询的特殊行为是它出现在封闭SELECT的FROM子句中，但可能与该SELECT的其他FROM子句相关。这是子查询的一种特殊情况，只有少数后端支持，现在是更新的Postgresql版本。

    版本1.1中的新功能

    也可以看看

    [LATERAL correlation](tutorial.html#lateral-selects) - overview of
    usage.

 `sqlalchemy.sql.expression.`{.descclassname}`outerjoin`{.descname}(*left*, *right*, *onclause=None*, *full=False*)[¶](#sqlalchemy.sql.expression.outerjoin "Permalink to this definition")
:   返回一个`OUTER JOIN`子句元素。

    返回的对象是[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")的实例。

    类似的功能也可以通过任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")上的[`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")方法使用。

    参数：

    -   **left** [¶](#sqlalchemy.sql.expression.outerjoin.params.left) -
        连接的左侧。
    -   **右** [¶](#sqlalchemy.sql.expression.outerjoin.params.right) -
        连接的右侧。
    -   **onclause**[¶](#sqlalchemy.sql.expression.outerjoin.params.onclause)
        – Optional criterion for the `ON` clause, is
        derived from foreign key relationships established between left
        and right otherwise.

    要将连接链接在一起，请在生成的[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")对象上使用[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")或[`FromClause.outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")方法。

 `sqlalchemy.sql.expression.`{.descclassname}`select`{.descname}(*columns=None*, *whereclause=None*, *from\_obj=None*, *distinct=False*, *having=None*, *correlate=True*, *prefixes=None*, *suffixes=None*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.select "Permalink to this definition")
:   构建一个新的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")。

    通过任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")上的[`FromClause.select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")方法也可以获得类似的功能。

    接受[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")参数的所有参数也接受字符串参数，这些参数将根据需要转换为[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")或[`literal_column()`](sqlelement.html#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")结构。

    也可以看看

    [Selecting](tutorial.html#coretutorial-selecting) -
    [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的核心教程描述。

    参数：

    -   **列** [¶](#sqlalchemy.sql.expression.select.params.columns) -

        [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")或[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象的列表，这些对象将形成结果语句的列子句。For
        those objects that are instances of [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        (typically [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        or [`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
        objects), the [`FromClause.c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        collection is extracted to form a collection of
        [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
        objects.

        该参数还将接受给定的[`Text`](type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")结构，以及ORM映射的类。

        注意

        [`select.columns`](#sqlalchemy.sql.expression.select.params.columns "sqlalchemy.sql.expression.select")参数在[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的方法形式中不可用，例如，
        [`FromClause.select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")

        也可以看看

        [`Select.column()`](#sqlalchemy.sql.expression.Select.column "sqlalchemy.sql.expression.Select.column")

        [`Select.with_only_columns()`](#sqlalchemy.sql.expression.Select.with_only_columns "sqlalchemy.sql.expression.Select.with_only_columns")

    -   **whereclause**
        [¶](#sqlalchemy.sql.expression.select.params.whereclause) -

        将用于形成`WHERE`子句的[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")表达式。通常最好将WHERE标准添加到与[`Select.where()`](#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")链接的现有[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")使用方法中。

        也可以看看

        [`Select.where()`](#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")

    -   **from\_obj**
        [¶](#sqlalchemy.sql.expression.select.params.from_obj) -

        将被添加到结果语句的`FROM`子句中的[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")对象的列表。这相当于在现有的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象上使用方法链接调用[`Select.select_from()`](#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")。

        也可以看看

        [`Select.select_from()`](#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")
        - full description of explicit FROM clause specification.

    -   **autocommit**
        [¶](#sqlalchemy.sql.expression.select.params.autocommit) -

        已过时。使用`.execution_options(autocommit=<True|False>)`来设置自动提交选项。

        也可以看看

        [`Executable.execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")

    -   **bind=None**[¶](#sqlalchemy.sql.expression.select.params.bind)
        – an [`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
        or [`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
        instance to which the resulting [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")
        object will be bound. 否则[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象将自动绑定到`Connectable`实例可以位于其包含的[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")成员中的任何位置。
    -   **correlate = True**
        [¶](#sqlalchemy.sql.expression.select.params.correlate) -

        表明这个[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象应该包含[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")元素与一个封闭的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象“相关”。通常最好使用[`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")指定现有[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")构造上的相关性。

        也可以看看

        [`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")
        - full description of correlation.

    -   **distinct = False**
        [¶](#sqlalchemy.sql.expression.select.params.distinct) -

        当`True`时，将`DISTINCT`限定符应用于结果语句的columns子句。

        布尔参数也可以是列表达式或列表达式的列表 -
        这是一种特殊的调用形式，Postgresql方言可以理解为`DISTINCT ON （＆lt； columns＆gt；）`语法。

        通过[`distinct()`](#sqlalchemy.sql.expression.Select.distinct "sqlalchemy.sql.expression.Select.distinct")方法，现有的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象也可以使用`distinct`。

        也可以看看

        [`Select.distinct()`](#sqlalchemy.sql.expression.Select.distinct "sqlalchemy.sql.expression.Select.distinct")

    -   **for\_update = False**
        [¶](#sqlalchemy.sql.expression.select.params.for_update) -

        > 当`True`时，将`FOR UPDATE`应用到结果语句的末尾。
        >
        > Deprecated since version 0.9.0: - use
        > [`Select.with_for_update()`](#sqlalchemy.sql.expression.Select.with_for_update "sqlalchemy.sql.expression.Select.with_for_update")
        > to specify the structure of the `FOR UPDATE` clause.
        >
        > `for_update`接受由特定后端解释的各种字符串值，包括：
        >
        > -   `"read"` - on MySQL, translates to
        >     `LOCK IN SHARE MODE`; on Postgresql,
        >     translates to `FOR SHARE`.
        > -   `"nowait"` - on Postgresql and Oracle,
        >     translates to `FOR UPDATE NOWAIT`.
        > -   `"read_nowait"` - on Postgresql,
        >     translates to `FOR SHARE NOWAIT`.

        也可以看看

        [`Select.with_for_update()`](#sqlalchemy.sql.expression.Select.with_for_update "sqlalchemy.sql.expression.Select.with_for_update")
        - improved API for specifying the `FOR UPDATE` clause.

    -   **group\_by**
        [¶](#sqlalchemy.sql.expression.select.params.group_by) -

        将包含结果选择的`GROUP BY`子句的[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")对象的列表。This
        parameter is typically specified more naturally using the
        [`Select.group_by()`](#sqlalchemy.sql.expression.Select.group_by "sqlalchemy.sql.expression.Select.group_by")
        method on an existing [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select").

        也可以看看

        [`Select.group_by()`](#sqlalchemy.sql.expression.Select.group_by "sqlalchemy.sql.expression.Select.group_by")

    -   **有** [¶](#sqlalchemy.sql.expression.select.params.having) -

        当`GROUP BY`时，[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")将包含结果选择的`HAVING`用来。此参数通常在现有[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")中使用[`Select.having()`](#sqlalchemy.sql.expression.Select.having "sqlalchemy.sql.expression.Select.having")方法更自然地指定。

        也可以看看

        [`Select.having()`](#sqlalchemy.sql.expression.Select.having "sqlalchemy.sql.expression.Select.having")

    -   **限制=无** [¶](#sqlalchemy.sql.expression.select.params.limit)
        -

        一个数值，通常在结果选择中呈现为`LIMIT`表达式。不支持`LIMIT`的后端将尝试提供类似的功能。此参数通常在现有的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")中使用[`Select.limit()`](#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")方法来更自然地指定。

        也可以看看

        [`Select.limit()`](#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")

    -   **偏移量=无**
        [¶](#sqlalchemy.sql.expression.select.params.offset) -

        a numeric value which usually renders as an `OFFSET` expression in the resulting select.
        不支持`OFFSET`的后端将尝试提供类似的功能。此参数通常在现有[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")中使用[`Select.offset()`](#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")方法更自然地指定。

        也可以看看

        [`Select.offset()`](#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")

    -   **order\_by**
        [¶](#sqlalchemy.sql.expression.select.params.order_by) -

        一个标量或[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")对象的列表，它们将包含结果select的`ORDER BY`子句。此参数通常在现有的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")中使用[`Select.order_by()`](#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")方法更自然地指定。

        也可以看看

        [`Select.order_by()`](#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")

    -   **use\_labels = False**
        [¶](#sqlalchemy.sql.expression.select.params.use_labels) -

        当`True`时，将使用columns子句中每列的标签生成该语句，该列使用其父表的名称（或别名）限定每个列，以便不同表中的列之间的名称冲突不会发生。标签的格式是\_
        。 T1\> T0\>生成的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象的“c”集合也将使用这些名称来定位列成员。

        也可以使用[`Select.apply_labels()`](#sqlalchemy.sql.expression.Select.apply_labels "sqlalchemy.sql.expression.Select.apply_labels")方法在现有的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象上指定此参数。

        也可以看看

        [`Select.apply_labels()`](#sqlalchemy.sql.expression.Select.apply_labels "sqlalchemy.sql.expression.Select.apply_labels")

`sqlalchemy.sql.expression。`{.descclassname} `子查询 tt> （ 别名，* args， ** kwargs  T5> ） T6> ¶ T7>`{.descname}
:   返回从[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")派生的[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象。

    名称
    :   别名

    \* args，\*\* kwargs

    > 所有其他参数传递给[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")函数。

 `sqlalchemy.sql.expression.`{.descclassname}`table`{.descname}(*name*, *\*columns*)[¶](#sqlalchemy.sql.expression.table "Permalink to this definition")
:   产生一个新的[`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")。

    返回的对象是一个[`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")实例，它表示模式级别[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的“语法”部分。它可能被用来构造轻量级的表格结构。

    Changed in version 1.0.0: [`expression.table()`](#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")
    can now be imported from the plain `sqlalchemy`
    namespace like any other SQL element.

    参数：

    -   **名称** [¶](#sqlalchemy.sql.expression.table.params.name) -
        表格的名称。
    -   **columns**[¶](#sqlalchemy.sql.expression.table.params.columns)
        – A collection of [`expression.column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
        constructs.

 `sqlalchemy.sql.expression.`{.descclassname}`tablesample`{.descname}(*selectable*, *sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.tablesample "Permalink to this definition")
:   返回一个[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")对象。

    [`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")
    is an [`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")
    subclass that represents a table with the TABLESAMPLE clause applied
    to it. [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
    is also available from the [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    class via the [`FromClause.tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
    method.

    TABLESAMPLE子句允许从表中选择一个随机选择的近似百分比的行。它支持多种采样方法，最常见的是BERNOULLI和SYSTEM。

    例如。：

        from sqlalchemy import func

        selectable = people.tablesample(
                    func.bernoulli(1),
                    name='alias',
                    seed=func.random())
        stmt = select([selectable.c.people_id])

    假设`people`具有列`people_id`，则上述语句将呈现为：

        SELECT alias.people_id FROM
        people AS alias TABLESAMPLE bernoulli(:bernoulli_1)
        REPEATABLE (random())

    版本1.1中的新功能

    参数：

    -   **sampling**[¶](#sqlalchemy.sql.expression.tablesample.params.sampling)
        – a `float` percentage between 0 and 100 or
        [`functions.Function`](functions.html#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function").
    -   **名称** [¶](#sqlalchemy.sql.expression.tablesample.params.name)
        - 可选的别名
    -   **seed**[¶](#sqlalchemy.sql.expression.tablesample.params.seed)
        – any real-valued SQL expression.
        指定时，也会呈现REPEATABLE子句。

 `sqlalchemy.sql.expression.`{.descclassname}`union`{.descname}(*\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.union "Permalink to this definition")
:   返回多个可选择的`UNION`。

    返回的对象是[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的一个实例。

    所有[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")子类都有一个类似的[`union()`](#sqlalchemy.sql.expression.union "sqlalchemy.sql.expression.union")方法。

    \*选择
    :   [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")实例列表。
    \*\* kwargs
    :   可用的关键字参数与[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")相同。

 `sqlalchemy.sql.expression.`{.descclassname}`union_all`{.descname}(*\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.union_all "Permalink to this definition")
:   返回多个可选项的`UNION ALL`。

    返回的对象是[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的一个实例。

    所有[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")子类中都有一个类似的[`union_all()`](#sqlalchemy.sql.expression.union_all "sqlalchemy.sql.expression.union_all")方法。

    \*选择
    :   [`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")实例列表。
    \*\* kwargs
    :   可用的关键字参数与[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")相同。

*class* `sqlalchemy.sql.expression。`{.descclassname} `别名`{.descname} （ *可选*，*名称=无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.expression.Alias "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.expression.FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

    表示一个表或可选别名（AS）。

    使用`AS`关键字（或在某些数据库（例如Oracle）上没有关键字），通常应用于SQL语句内的任何表或子选择，表示别名。

    This object is constructed from the [`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")
    module level function as well as the [`FromClause.alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
    method available on all [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    subclasses.

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.Alias.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.Alias.columns "sqlalchemy.sql.expression.Alias.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.Alias.columns "sqlalchemy.sql.expression.Alias.columns")或[`c`](#sqlalchemy.sql.expression.Alias.c "sqlalchemy.sql.expression.Alias.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Alias.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Alias.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Alias.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Alias.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Alias.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Alias.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Alias.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.Alias.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.Alias.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.Alias.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.Alias.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Alias.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.Alias.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.Alias.join.params.right) -
            连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Alias.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.Alias.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Alias.join.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Alias.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.Alias.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Alias.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Alias.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Alias.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.Alias.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Alias.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.Alias.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Alias.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`CompoundSelect`{.descname}(*keyword*, *\*selects*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.CompoundSelect "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

    Forms the basis of `UNION`, `UNION ALL`, and other
    :   基于SELECT的集合操作。

    也可以看看

    [`union()`](#sqlalchemy.sql.expression.union "sqlalchemy.sql.expression.union")

    [`union_all()`](#sqlalchemy.sql.expression.union_all "sqlalchemy.sql.expression.union_all")

    [`intersect()`](#sqlalchemy.sql.expression.intersect "sqlalchemy.sql.expression.intersect")

    [`intersect_all()`](#sqlalchemy.sql.expression.intersect_all "sqlalchemy.sql.expression.intersect_all")

    `except()`

    [`except_all()`](#sqlalchemy.sql.expression.except_all "sqlalchemy.sql.expression.except_all")

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.CompoundSelect.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` append_group_by  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`append_group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.append_group_by "sqlalchemy.sql.expression.GenerativeSelect.append_group_by")
        *方法* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        追加应用于此可选项的给定GROUP BY标准。

        该标准将被附加到任何预先存在的GROUP BY标准。

        这是一种**in-place**突变方法； [`group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.group_by "sqlalchemy.sql.expression.GenerativeSelect.group_by")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_order_by  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`append_order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.append_order_by "sqlalchemy.sql.expression.GenerativeSelect.append_order_by")
        *方法* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        附加给定的ORDER BY标准应用于此可选项。

        该标准将被附加到任何预先存在的ORDER BY标准。

        这是一种**in-place**突变方法； [`order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.order_by "sqlalchemy.sql.expression.GenerativeSelect.order_by")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` apply_labels  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`apply_labels()`](#sqlalchemy.sql.expression.GenerativeSelect.apply_labels "sqlalchemy.sql.expression.GenerativeSelect.apply_labels")
        *方法* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        返回一个新的可选项，并将'use\_labels'标志设置为True。

        这将导致使用标签对其表名称生成列表达式，例如“SELECT somecolumn
        AS
        tablename\_somecolumn”。这允许包含多个FROM子句的可选项生成一组唯一的列名称，而不考虑各个FROM子句之间的名称冲突。

    ` as_scalar  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选项的'标量'表示，它可以用作列表达式。

        通常，在其子列中只有一列的select语句可以用作标量表达式。

        返回的对象是[`ScalarSelect`](#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")的一个实例。

    `自动提交 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`autocommit()`](#sqlalchemy.sql.expression.SelectBase.autocommit "sqlalchemy.sql.expression.SelectBase.autocommit")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        将'autocommit'标志设置为True返回一个新的可选项。

        从版本0.6开始弃用： `autocommit()`已弃用。使用带有'autocommit'标志的[`Executable.execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.CompoundSelect.columns "sqlalchemy.sql.expression.CompoundSelect.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.CompoundSelect.columns "sqlalchemy.sql.expression.CompoundSelect.columns")或[`c`](#sqlalchemy.sql.expression.CompoundSelect.c "sqlalchemy.sql.expression.CompoundSelect.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.CompoundSelect.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.CompoundSelect.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.CompoundSelect.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.CompoundSelect.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.CompoundSelect.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.CompoundSelect.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.CompoundSelect.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.CompoundSelect.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.CompoundSelect.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.CompoundSelect.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.CompoundSelect.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.CompoundSelect.cte "Permalink to this definition")
    :   *继承自* [`cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.CompoundSelect.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.CompoundSelect.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    `描述 T0> ¶ T1>`{.descname}
    :   *从* [`description`](#sqlalchemy.sql.expression.FromClause.description "sqlalchemy.sql.expression.FromClause.description")
        *继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        这个FromClause的简要描述。

        主要用于错误消息格式。

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.CompoundSelect.execution_options "sqlalchemy.sql.expression.CompoundSelect.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` FOR_UPDATE  T0> ¶ T1>`{.descname}
    :   *继承自* [`for_update`](#sqlalchemy.sql.expression.GenerativeSelect.for_update "sqlalchemy.sql.expression.GenerativeSelect.for_update")
        *属性* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        为`for_update`属性提供传统方言支持。

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

    ` GROUP_BY  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   从 [`group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.group_by "sqlalchemy.sql.expression.GenerativeSelect.group_by")
        *方法继承的*[`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")**

        返回一个新的可选项，其中应用了GROUP BY标准的给定列表。

        该标准将被附加到任何预先存在的GROUP BY标准。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.CompoundSelect.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.join.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.CompoundSelect.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.CompoundSelect.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.join.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`label()`](#sqlalchemy.sql.expression.SelectBase.label "sqlalchemy.sql.expression.SelectBase.label")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选择的“标量”表示，嵌入为带有标签的子查询。

        也可以看看

        [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `限制 T0> （ T1> 限制 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`limit()`](#sqlalchemy.sql.expression.GenerativeSelect.limit "sqlalchemy.sql.expression.GenerativeSelect.limit")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        返回一个新的可选择的给定LIMIT标准。

        这是一个数值，通常在结果选择中呈现为`LIMIT`表达式。不支持`LIMIT`的后端将尝试提供类似的功能。

        版本1.0.0更改： - [`Select.limit()`](#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")现在可以接受任意SQL表达式以及整数值。

        参数：

        **limit**[¶](#sqlalchemy.sql.expression.CompoundSelect.limit.params.limit)
        – an integer LIMIT parameter, or a SQL expression that provides
        an integer result.

    `偏移 T0> （ T1> 偏移 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`offset()`](#sqlalchemy.sql.expression.GenerativeSelect.offset "sqlalchemy.sql.expression.GenerativeSelect.offset")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        使用给定的OFFSET标准返回一个新的可选项。

        This is a numeric value which usually renders as an
        `OFFSET` expression in the resulting select.
        不支持`OFFSET`的后端将尝试提供类似的功能。

        版本1.0.0更改： - [`Select.offset()`](#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")现在可以接受任意SQL表达式以及整数值。

        参数：

        **offset**[¶](#sqlalchemy.sql.expression.CompoundSelect.offset.params.offset)
        – an integer OFFSET parameter, or a SQL expression that provides
        an integer result.

    ` ORDER_BY  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.order_by "sqlalchemy.sql.expression.GenerativeSelect.order_by")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        返回一个新的可选项，其中应用了ORDER BY标准的给定列表。

        该标准将被附加到任何预先存在的ORDER BY标准。

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.CompoundSelect.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.CompoundSelect.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.CompoundSelect.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.CompoundSelect.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.CompoundSelect.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.CompoundSelect.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.CompoundSelect.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.CompoundSelect.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.CompoundSelect.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

     `with_for_update`{.descname}(*nowait=False*, *read=False*, *of=None*, *skip\_locked=False*, *key\_share=False*)[¶](#sqlalchemy.sql.expression.CompoundSelect.with_for_update "Permalink to this definition")
    :   *inherited from the* [`with_for_update()`](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        为[`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")指定一个`FOR UPDATE`子句。

        例如。：

            stmt = select([table]).with_for_update(nowait=True)

        在像Postgresql或Oracle这样的数据库上，上面的代码会显示如下的语句：

            SELECT table.a, table.b FROM table FOR UPDATE NOWAIT

        在其他后端，`nowait`选项被忽略，而是产生：

            SELECT table.a, table.b FROM table FOR UPDATE

        当不带任何参数调用时，语句将以后缀`FOR UPDATE`进行呈现。然后可以提供其他参数，这些参数允许使用通用数据库特定的变体。

        参数：

        -   **nowait**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.with_for_update.params.nowait)
            -
            boolean；将在Oracle和Postgresql方言中呈现`FOR  tt> UPDATE NOWAIT`
        -   **读**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.with_for_update.params.read)
            - boolean；将在MySQL上呈现`LOCK IN SHARE 模式`，`在Postgresql上共享 共享`。On
            Postgresql, when combined with `nowait`,
            will render `FOR SHARE NOWAIT`.
        -   **of**[¶](#sqlalchemy.sql.expression.CompoundSelect.with_for_update.params.of)
            – SQL expression or list of SQL expression elements
            (typically [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
            objects or a compatible expression) which will render into a
            `FOR UPDATE OF` clause; supported by
            PostgreSQL and Oracle. 可以根据后端呈现为表格或列。
        -   **skip\_locked**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.with_for_update.params.skip_locked)
            -

            boolean, will render `FOR UPDATE SKIP LOCKED` on Oracle and Postgresql dialects or
            `FOR SHARE SKIP LOCKED` if
            `read=True` is also specified.

            版本1.1.0中的新功能

        -   **key\_share**
            [¶](#sqlalchemy.sql.expression.CompoundSelect.with_for_update.params.key_share)
            -

            boolean, will render `FOR NO KEY UPDATE`, or if combined with `read=True` will render `FOR KEY SHARE`,
            on the Postgresql dialect.

            版本1.1.0中的新功能

 *class*`sqlalchemy.sql.expression.`{.descclassname}`CTE`{.descname}(*selectable*, *name=None*, *recursive=False*, *\_cte\_alias=None*, *\_restates=frozenset([])*, *\_suffixes=None*)[¶](#sqlalchemy.sql.expression.CTE "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.Generative`，[`sqlalchemy.sql.expression.HasSuffixes`](#sqlalchemy.sql.expression.HasSuffixes "sqlalchemy.sql.expression.HasSuffixes")，[`sqlalchemy.sql.expression.Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")

    代表通用表达式。

    [`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象是使用任何可选择的`SelectBase.cte()`方法获得的。查看完整示例的方法。

    New in version 0.7.6.

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.CTE.columns "sqlalchemy.sql.expression.CTE.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.CTE.columns "sqlalchemy.sql.expression.CTE.columns")或[`c`](#sqlalchemy.sql.expression.CTE.c "sqlalchemy.sql.expression.CTE.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.CTE.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.CTE.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.CTE.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.CTE.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.CTE.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.CTE.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.CTE.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.CTE.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.CTE.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.CTE.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.CTE.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.CTE.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.CTE.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.CTE.join.params.right) -
            连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.CTE.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.CTE.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.CTE.join.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.CTE.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.CTE.outerjoin.params.right) -
            连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.CTE.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.CTE.outerjoin.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.CTE.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.CTE.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.CTE.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

    `后缀 tt> （ * expr，** kw ） T5>`{.descname}
    :   *inherited from the* [`suffix_with()`](#sqlalchemy.sql.expression.HasSuffixes.suffix_with "sqlalchemy.sql.expression.HasSuffixes.suffix_with")
        *method of* [`HasSuffixes`](#sqlalchemy.sql.expression.HasSuffixes "sqlalchemy.sql.expression.HasSuffixes")

        在整个语句后添加一个或多个表达式。

        这用于在特定结构上支持后端特定的后缀关键字。

        例如。：

            stmt = select([col1, col2]).cte().suffix_with(
                "cycle empno set y_cycle to 1 default 0", dialect="oracle")

        多个后缀可以通过多次调用[`suffix_with()`](#sqlalchemy.sql.expression.CTE.suffix_with "sqlalchemy.sql.expression.CTE.suffix_with")来指定。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.CTE.suffix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the target
            clause.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.CTE.suffix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制仅将该后缀渲染为该方言。

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.CTE.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.CTE.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

*class* `sqlalchemy.sql.expression。`{.descclassname} `可执行文件`{.descname} [¶](#sqlalchemy.sql.expression.Executable "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.Generative`

    将一个ClauseElement标记为支持执行。

    [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")
    is a superclass for all “statement” types of objects, including
    [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
    [`delete()`](dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete"),
    [`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update"),
    [`insert()`](dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert"),
    [`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text").

    `结合 T0> ¶ T1>`{.descname}
    :   返回此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")绑定到的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")；如果没有找到，则返回None。

        这是遍历，在本地进行检查，然后检查关联对象的“from”子句，直到找到绑定的引擎或连接。

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   编译并执行[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.Executable.scalar "Permalink to this definition")
    :   编译并执行此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

*class* `sqlalchemy.sql.expression。`{.descclassname} `FromClause`{.descname} [¶](#sqlalchemy.sql.expression.FromClause "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")

    表示可以在`SELECT`语句的`FROM`子句中使用的元素。plain

    最常见的[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")形式是[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。所有[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象共有的主要特征包括：

    -   一个[`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")集合，它提供对[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象集合的每个名称的访问。
    -   一个[`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")属性，它是指示`primary_key`标志的所有[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的集合。
    -   Methods to generate various derivations of a “from” clause,
        including [`FromClause.alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias"),
        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join"),
        [`FromClause.select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select").

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.FromClause.alias "Permalink to this definition")
    :   返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` C  T0> ¶ T1>`{.descname}
    :   [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")或[`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "Permalink to this definition")
    :   返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.FromClause.corresponding_column "Permalink to this definition")
    :   给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.FromClause.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.FromClause.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.FromClause.count "Permalink to this definition")
    :   返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    `描述 T0> ¶ T1>`{.descname}
    :   这个FromClause的简要描述。

        主要用于错误消息格式。

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   返回FromClause引用的ForeignKey对象的集合。

    ` is_derived_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   如果FromClause从给定的FromClause中“派生”，则返回True。

        一个例子是从表中派生的表的别名。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.FromClause.join "Permalink to this definition")
    :   从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.FromClause.join.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.FromClause.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.FromClause.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.FromClause.join.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.FromClause.outerjoin "Permalink to this definition")
    :   Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.FromClause.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.FromClause.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.FromClause.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    ` primary_key  T0> ¶ T1>`{.descname}
    :   返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.FromClause.replace_selectable "Permalink to this definition")
    :   用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `架构`{.descname} *=无* [¶](#sqlalchemy.sql.expression.FromClause.schema "Permalink to this definition")
    :   为[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")定义'schema'属性。

        除[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")以外的大多数对象，这通常是`None`，它被视为[`Table.schema`](metadata.html#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")参数的值。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.FromClause.select "Permalink to this definition")
    :   返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.FromClause.tablesample "Permalink to this definition")
    :   返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

 *class*`sqlalchemy.sql.expression.`{.descclassname}`GenerativeSelect`{.descname}(*use\_labels=False*, *for\_update=False*, *limit=None*, *offset=None*, *order\_by=None*, *group\_by=None*, *bind=None*, *autocommit=None*)[¶](#sqlalchemy.sql.expression.GenerativeSelect "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

    可以添加其他元素的SELECT语句的基类。

    这可以作为[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")和[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的基础，其中可以添加ORDER
    BY，GROUP BY等元素，并且可以控制列呈现。与[`TextAsFrom`](#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")相比，它虽然它的子类为[`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")，并且也是一个SELECT构造，它表示一个固定的文本字符串，不能在此级别进行更改，只能打包为子查询。

    版本0.9.0新增： [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")用于提供特定于[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")和[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")的功能，同时允许[`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")用于其他类似SELECT的对象，例如[`TextAsFrom`](#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.GenerativeSelect.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` append_group_by  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   追加应用于此可选项的给定GROUP BY标准。

        该标准将被附加到任何预先存在的GROUP BY标准。

        这是一种**in-place**突变方法； [`group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.group_by "sqlalchemy.sql.expression.GenerativeSelect.group_by")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_order_by  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   附加给定的ORDER BY标准应用于此可选项。

        该标准将被附加到任何预先存在的ORDER BY标准。

        这是一种**in-place**突变方法； [`order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.order_by "sqlalchemy.sql.expression.GenerativeSelect.order_by")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` apply_labels  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回一个新的可选项，并将'use\_labels'标志设置为True。

        这将导致使用标签对其表名称生成列表达式，例如“SELECT somecolumn
        AS
        tablename\_somecolumn”。这允许包含多个FROM子句的可选项生成一组唯一的列名称，而不考虑各个FROM子句之间的名称冲突。

    ` as_scalar  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选项的'标量'表示，它可以用作列表达式。

        通常，在其子列中只有一列的select语句可以用作标量表达式。

        返回的对象是[`ScalarSelect`](#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")的一个实例。

    `自动提交 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`autocommit()`](#sqlalchemy.sql.expression.SelectBase.autocommit "sqlalchemy.sql.expression.SelectBase.autocommit")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        将'autocommit'标志设置为True返回一个新的可选项。

        从版本0.6开始弃用： `autocommit()`已弃用。使用带有'autocommit'标志的[`Executable.execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")。

    `结合 T0> ¶ T1>`{.descname}
    :   *继承自* [`bind`](#sqlalchemy.sql.expression.Executable.bind "sqlalchemy.sql.expression.Executable.bind")
        *属性* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        返回此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")绑定到的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")；如果没有找到，则返回None。

        这是遍历，在本地进行检查，然后检查关联对象的“from”子句，直到找到绑定的引擎或连接。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.GenerativeSelect.columns "sqlalchemy.sql.expression.GenerativeSelect.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.GenerativeSelect.columns "sqlalchemy.sql.expression.GenerativeSelect.columns")或[`c`](#sqlalchemy.sql.expression.GenerativeSelect.c "sqlalchemy.sql.expression.GenerativeSelect.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.GenerativeSelect.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.GenerativeSelect.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.GenerativeSelect.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.GenerativeSelect.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.GenerativeSelect.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.GenerativeSelect.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.GenerativeSelect.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.GenerativeSelect.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.GenerativeSelect.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.GenerativeSelect.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.GenerativeSelect.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.GenerativeSelect.cte "Permalink to this definition")
    :   *继承自* [`cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.GenerativeSelect.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.GenerativeSelect.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    `描述 T0> ¶ T1>`{.descname}
    :   *从* [`description`](#sqlalchemy.sql.expression.FromClause.description "sqlalchemy.sql.expression.FromClause.description")
        *继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        这个FromClause的简要描述。

        主要用于错误消息格式。

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.GenerativeSelect.execution_options "sqlalchemy.sql.expression.GenerativeSelect.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` FOR_UPDATE  T0> ¶ T1>`{.descname}
    :   为`for_update`属性提供传统方言支持。

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.get_children "sqlalchemy.sql.expression.ClauseElement.get_children")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的直接子元素。

        这用于访问遍历。

        \*\*
        kwargs可能包含更改返回的集合的标志，例如为了减少更大的遍历而返回项目的子集，或者从不同的上下文返回子项目（例如模式级集合而不是子句-水平）。

    ` GROUP_BY  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的可选项，其中应用了GROUP BY标准的给定列表。

        该标准将被附加到任何预先存在的GROUP BY标准。

    ` is_derived_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_derived_from()`](#sqlalchemy.sql.expression.FromClause.is_derived_from "sqlalchemy.sql.expression.FromClause.is_derived_from")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        如果FromClause从给定的FromClause中“派生”，则返回True。

        一个例子是从表中派生的表的别名。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.GenerativeSelect.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.join.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.GenerativeSelect.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.GenerativeSelect.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.join.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`label()`](#sqlalchemy.sql.expression.SelectBase.label "sqlalchemy.sql.expression.SelectBase.label")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选择的“标量”表示，嵌入为带有标签的子查询。

        也可以看看

        [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `限制 T0> （ T1> 限制 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的可选择的给定LIMIT标准。

        这是一个数值，通常在结果选择中呈现为`LIMIT`表达式。不支持`LIMIT`的后端将尝试提供类似的功能。

        版本1.0.0更改： - [`Select.limit()`](#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")现在可以接受任意SQL表达式以及整数值。

        参数：

        **limit**[¶](#sqlalchemy.sql.expression.GenerativeSelect.limit.params.limit)
        – an integer LIMIT parameter, or a SQL expression that provides
        an integer result.

    `偏移 T0> （ T1> 偏移 T2> ） T3> ¶ T4>`{.descname}
    :   使用给定的OFFSET标准返回一个新的可选项。

        This is a numeric value which usually renders as an
        `OFFSET` expression in the resulting select.
        不支持`OFFSET`的后端将尝试提供类似的功能。

        版本1.0.0更改： - [`Select.offset()`](#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")现在可以接受任意SQL表达式以及整数值。

        参数：

        **offset**[¶](#sqlalchemy.sql.expression.GenerativeSelect.offset.params.offset)
        – an integer OFFSET parameter, or a SQL expression that provides
        an integer result.

    ` ORDER_BY  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的可选项，其中应用了ORDER BY标准的给定列表。

        该标准将被附加到任何预先存在的ORDER BY标准。

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.GenerativeSelect.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.GenerativeSelect.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.GenerativeSelect.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.GenerativeSelect.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.GenerativeSelect.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.GenerativeSelect.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.GenerativeSelect.self_group "sqlalchemy.sql.expression.GenerativeSelect.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.GenerativeSelect.self_group "sqlalchemy.sql.expression.GenerativeSelect.self_group")方法仅返回self。

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.GenerativeSelect.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.GenerativeSelect.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

     `with_for_update`{.descname}(*nowait=False*, *read=False*, *of=None*, *skip\_locked=False*, *key\_share=False*)[¶](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update "Permalink to this definition")
    :   为[`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")指定一个`FOR UPDATE`子句。

        例如。：

            stmt = select([table]).with_for_update(nowait=True)

        在像Postgresql或Oracle这样的数据库上，上面的代码会显示如下的语句：

            SELECT table.a, table.b FROM table FOR UPDATE NOWAIT

        在其他后端，`nowait`选项被忽略，而是产生：

            SELECT table.a, table.b FROM table FOR UPDATE

        当不带任何参数调用时，语句将以后缀`FOR UPDATE`进行呈现。然后可以提供其他参数，这些参数允许使用通用数据库特定的变体。

        参数：

        -   **nowait**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.nowait)
            -
            boolean；将在Oracle和Postgresql方言中呈现`FOR  tt> UPDATE NOWAIT`
        -   **读**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.read)
            - boolean；将在MySQL上呈现`LOCK IN SHARE 模式`，`在Postgresql上共享 共享`。On
            Postgresql, when combined with `nowait`,
            will render `FOR SHARE NOWAIT`.
        -   **of**[¶](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.of)
            – SQL expression or list of SQL expression elements
            (typically [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
            objects or a compatible expression) which will render into a
            `FOR UPDATE OF` clause; supported by
            PostgreSQL and Oracle. 可以根据后端呈现为表格或列。
        -   **skip\_locked**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked)
            -

            boolean, will render `FOR UPDATE SKIP LOCKED` on Oracle and Postgresql dialects or
            `FOR SHARE SKIP LOCKED` if
            `read=True` is also specified.

            版本1.1.0中的新功能

        -   **key\_share**
            [¶](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.key_share)
            -

            boolean, will render `FOR NO KEY UPDATE`, or if combined with `read=True` will render `FOR KEY SHARE`,
            on the Postgresql dialect.

            版本1.1.0中的新功能

*class* `sqlalchemy.sql.expression。`{.descclassname} `HasCTE`{.descname} [¶](#sqlalchemy.sql.expression.HasCTE "Permalink to this definition")
:   Mixin声明一个类包含CTE支持。

    版本1.1中的新功能

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.HasCTE.cte "Permalink to this definition")
    :   返回一个新的[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.HasCTE.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.HasCTE.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

*class* `sqlalchemy.sql.expression。`{.descclassname} `HasPrefixes`{.descname} [¶](#sqlalchemy.sql.expression.HasPrefixes "Permalink to this definition")
:   `prefix_with`{.descname} （ *\* expr*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.HasPrefixes.prefix_with "Permalink to this definition")
    :   在语句关键字后添加一个或多个表达式，即SELECT，INSERT，UPDATE或DELETE。生成。

        这用于支持后端特定的前缀关键字，例如由MySQL提供的前缀关键字。

        例如。：

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

        可以通过多次调用[`prefix_with()`](#sqlalchemy.sql.expression.HasPrefixes.prefix_with "sqlalchemy.sql.expression.HasPrefixes.prefix_with")来指定多个前缀。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.HasPrefixes.prefix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the INSERT,
            UPDATE, or DELETE keyword.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.HasPrefixes.prefix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制将该前缀的呈现仅限于该方言。

*class* `sqlalchemy.sql.expression。`{.descclassname} `HasSuffixes`{.descname} [¶](#sqlalchemy.sql.expression.HasSuffixes "Permalink to this definition")
:   `后缀 tt> （ * expr，** kw ） T5>`{.descname}
    :   在整个语句后添加一个或多个表达式。

        这用于在特定结构上支持后端特定的后缀关键字。

        例如。：

            stmt = select([col1, col2]).cte().suffix_with(
                "cycle empno set y_cycle to 1 default 0", dialect="oracle")

        多个后缀可以通过多次调用[`suffix_with()`](#sqlalchemy.sql.expression.HasSuffixes.suffix_with "sqlalchemy.sql.expression.HasSuffixes.suffix_with")来指定。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.HasSuffixes.suffix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the target
            clause.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.HasSuffixes.suffix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制仅将该后缀渲染为该方言。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Join`{.descname}(*left*, *right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.Join "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

    represent a `JOIN` construct between two
    [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    elements.

    The public constructor function for [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
    is the module-level [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
    function, as well as the [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
    method of any [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    (e.g. such as [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")).

    也可以看看

    [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")

    [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

     `__init__`{.descname}(*left*, *right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.Join.__init__ "Permalink to this definition")
    :   构建一个新的[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")。

        这里通常的入口点是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象的[`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")函数或[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")方法。

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.Join.alias "Permalink to this definition")
    :   返回此[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")的别名。

        这里的默认行为是首先从[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")生成一个SELECT构造，然后从中产生一个[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")。所以给了一个形式的加入：

            j = table_a.join(table_b, table_a.c.id == table_b.c.a_id)

        本身的JOIN看起来像：

            table_a JOIN table_b ON table_a.id = table_b.a_id

        Whereas the alias of the above, `j.alias()`,
        would in a SELECT context look like:

            (SELECT table_a.id AS table_a_id, table_b.id AS table_b_id,
                table_b.a_id AS table_b_a_id
                FROM table_a
                JOIN table_b ON table_a.id = table_b.a_id) AS anon_1

        给定一个[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")对象`j`，等价的长手形式是：

            from sqlalchemy import select, alias
            j = alias(
                select([j.left, j.right]).\
                    select_from(j).\
                    with_labels(True).\
                    correlate(False),
                name=name
            )

        由[`Join.alias()`](#sqlalchemy.sql.expression.Join.alias "sqlalchemy.sql.expression.Join.alias")生成的可选择列与以单个名称显示的两个单独可选列的列相同
        - 各列为“自动标记”，即`.c.`所得到的[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")的集合使用`<tablename>_<columname>`方案表示各个列的名称：

            j.c.table_a_id
            j.c.table_b_a_id

        [`Join.alias()`](#sqlalchemy.sql.expression.Join.alias "sqlalchemy.sql.expression.Join.alias")还具有替代选项，用于别名联接，不会产生封闭的SELECT，并且通常不会将标签应用于列名称。`flat=True`选项将分别针对左侧和右侧调用[`FromClause.alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")。使用这个选项，不会产生新的`SELECT`；我们相反，从一个构造如下：

            j = table_a.join(table_b, table_a.c.id == table_b.c.a_id)
            j = j.alias(flat=True)

        我们得到如下结果：

            table_a AS table_a_1 JOIN table_b AS table_b_1 ON
            table_a_1.id = table_b_1.a_id

        `flat=True`参数也会传播到包含的selectables，以便组合连接如：

            j = table_a.join(
                    table_b.join(table_c,
                            table_b.c.id == table_c.c.b_id),
                    table_b.c.a_id == table_a.c.id
                ).alias(flat=True)

        会产生如下表达式：

            table_a AS table_a_1 JOIN (
                    table_b AS table_b_1 JOIN table_c AS table_c_1
                    ON table_b_1.id = table_c_1.b_id
            ) ON table_a_1.id = table_b_1.a_id

        独立的[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")函数以及基础的[`FromClause.alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")方法也支持`flat=True`参数作为无操作，以便参数可以传递给任何可选择的`alias()`方法。

        版本0.9.0新增：增加了`flat=True`选项来创建连接的“别名”，而不用在SELECT子查询内部进行封闭。

        参数：

        -   **名称**
            [¶](#sqlalchemy.sql.expression.Join.alias.params.name) -
            给予别名的名称。
        -   **flat**
            [¶](#sqlalchemy.sql.expression.Join.alias.params.flat) -

            如果为True，则生成此[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")的左侧和右侧的别名，并返回这两个可选项的联接。这会生成不包含封闭SELECT的连接表达式。

            版本0.9.0中的新功能

        也可以看看

        [`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.Join.columns "sqlalchemy.sql.expression.Join.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.Join.columns "sqlalchemy.sql.expression.Join.columns")或[`c`](#sqlalchemy.sql.expression.Join.c "sqlalchemy.sql.expression.Join.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Join.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Join.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Join.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Join.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Join.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Join.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Join.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.Join.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.Join.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.Join.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.Join.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Join.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.Join.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.Join.join.params.right) -
            连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Join.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.Join.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Join.join.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Join.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.Join.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Join.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Join.outerjoin.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Join.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.Join.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.sql.expression.Join.select "Permalink to this definition")
    :   从[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")中创建一个[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")。

        给定一个[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")对象`j`，等价的长手形式是：

            from sqlalchemy import select
            j = select([j.left, j.right], **kw).\
                        where(whereclause).\
                        select_from(j)

        参数：

        -   **whereclause**[¶](#sqlalchemy.sql.expression.Join.select.params.whereclause)
            – the WHERE criterion that will be sent to the
            [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
            function
        -   **\*\*kwargs**[¶](#sqlalchemy.sql.expression.Join.select.params.**kwargs)
            – all other kwargs are sent to the underlying
            [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
            function.

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.Join.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Join.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Lateral`{.descname}(*selectable*, *name=None*)[¶](#sqlalchemy.sql.expression.Lateral "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")

    表示一个LATERAL子查询。

    This object is constructed from the [`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")
    module level function as well as the [`FromClause.lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
    method available on all [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
    subclasses.

    尽管LATERAL是SQL标准的一部分，但只有更新的Postgresql版本才支持此关键字。

    版本1.1中的新功能

    也可以看看

    [LATERAL correlation](tutorial.html#lateral-selects) - overview of
    usage.

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.Lateral.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.Lateral.columns "sqlalchemy.sql.expression.Lateral.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.Lateral.columns "sqlalchemy.sql.expression.Lateral.columns")或[`c`](#sqlalchemy.sql.expression.Lateral.c "sqlalchemy.sql.expression.Lateral.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Lateral.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Lateral.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Lateral.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Lateral.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Lateral.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Lateral.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Lateral.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.Lateral.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.Lateral.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.Lateral.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.Lateral.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Lateral.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.Lateral.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.Lateral.join.params.right) -
            连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Lateral.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.Lateral.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Lateral.join.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Lateral.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.Lateral.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Lateral.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Lateral.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Lateral.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.Lateral.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Lateral.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.Lateral.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Lateral.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`ScalarSelect`{.descname}(*element*)[¶](#sqlalchemy.sql.expression.ScalarSelect "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.Generative`，`sqlalchemy.sql.expression.Grouping`

    `其中 T0> （ T1> 暴 T2> ） T3> ¶ T4>`{.descname}
    :   对此[`ScalarSelect`](#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")引用的SELECT语句应用WHERE子句。

*class* `sqlalchemy.sql.expression。`{.descclassname} `选择`{.descname} （ *columns =无*，*whereclause = None*，*from\_obj = None*，*distinct = False*，*具有=无*，*correlate = t9\>，*前缀=无*，*后缀=无*，*\*\* kwargs* ） [](#sqlalchemy.sql.expression.Select "Permalink to this definition") \>*
:   基础：[`sqlalchemy.sql.expression.HasPrefixes`](#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")，[`sqlalchemy.sql.expression.HasSuffixes`](#sqlalchemy.sql.expression.HasSuffixes "sqlalchemy.sql.expression.HasSuffixes")，[`sqlalchemy.sql.expression.GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

    代表一个`SELECT`语句。plain

     `__init__`{.descname}(*columns=None*, *whereclause=None*, *from\_obj=None*, *distinct=False*, *having=None*, *correlate=True*, *prefixes=None*, *suffixes=None*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.Select.__init__ "Permalink to this definition")
    :   构建一个新的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")。

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.Select.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` append_column  T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   将给定的列表达式追加到此select()构造的columns子句中。

        这是一种**in-place**突变方法； [`column()`](#sqlalchemy.sql.expression.Select.column "sqlalchemy.sql.expression.Select.column")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_correlation  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   将给定的相关表达式附加到这个select()结构中。

        这是一种**in-place**突变方法； [`correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   将给定的FromClause表达式附加到这个select()构造的FROM子句中。

        这是一种**in-place**突变方法； [`select_from()`](#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_group_by  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`append_group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.append_group_by "sqlalchemy.sql.expression.GenerativeSelect.append_group_by")
        *方法* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        追加应用于此可选项的给定GROUP BY标准。

        该标准将被附加到任何预先存在的GROUP BY标准。

        这是一种**in-place**突变方法； [`group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.group_by "sqlalchemy.sql.expression.GenerativeSelect.group_by")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_having  T0> （ T1> 具有 T2> ） T3> ¶ T4>`{.descname}
    :   将给定的表达式追加到这个select()构造的HAVING标准中。

        该表达式将通过AND连接到现有的HAVING标准。

        This is an **in-place** mutation method; the [`having()`](#sqlalchemy.sql.expression.Select.having "sqlalchemy.sql.expression.Select.having")
        method is preferred, as it provides standard [method
        chaining](glossary.html#term-method-chaining).

    ` append_order_by  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`append_order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.append_order_by "sqlalchemy.sql.expression.GenerativeSelect.append_order_by")
        *方法* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        附加给定的ORDER BY标准应用于此可选项。

        该标准将被附加到任何预先存在的ORDER BY标准。

        这是一种**in-place**突变方法； [`order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.order_by "sqlalchemy.sql.expression.GenerativeSelect.order_by")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_prefix  T0> （ T1> 子句 T2> ） T3> ¶ T4>`{.descname}
    :   将给定的列子句前缀表达式附加到此select()构造。

        这是一种**in-place**突变方法； [`prefix_with()`](#sqlalchemy.sql.expression.Select.prefix_with "sqlalchemy.sql.expression.Select.prefix_with")方法是首选，因为它提供了标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` append_whereclause  T0> （ T1>  whereclause  T2> ） T3> ¶ T4>`{.descname}
    :   将给定的表达式追加到这个select()构造的WHERE标准中。

        该表达式将通过AND连接到现有的WHERE标准。

        这是一种**in-place**突变方法； [`where()`](#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")方法是首选，因为它提供标准的[method
        chaining](glossary.html#term-method-chaining)。

    ` apply_labels  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`apply_labels()`](#sqlalchemy.sql.expression.GenerativeSelect.apply_labels "sqlalchemy.sql.expression.GenerativeSelect.apply_labels")
        *方法* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        返回一个新的可选项，并将'use\_labels'标志设置为True。

        这将导致使用标签对其表名称生成列表达式，例如“SELECT somecolumn
        AS
        tablename\_somecolumn”。这允许包含多个FROM子句的可选项生成一组唯一的列名称，而不考虑各个FROM子句之间的名称冲突。

    ` as_scalar  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选项的'标量'表示，它可以用作列表达式。

        通常，在其子列中只有一列的select语句可以用作标量表达式。

        返回的对象是[`ScalarSelect`](#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")的一个实例。

    `自动提交 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`autocommit()`](#sqlalchemy.sql.expression.SelectBase.autocommit "sqlalchemy.sql.expression.SelectBase.autocommit")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        将'autocommit'标志设置为True返回一个新的可选项。

        从版本0.6开始弃用： `autocommit()`已弃用。使用带有'autocommit'标志的[`Executable.execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.Select.columns "sqlalchemy.sql.expression.Select.columns")属性的别名。

    `列 T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的select()构造，并将给定的列表达式添加到它的columns子句中。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.Select.columns "sqlalchemy.sql.expression.Select.columns")或[`c`](#sqlalchemy.sql.expression.Select.c "sqlalchemy.sql.expression.Select.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Select.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Select.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Select.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Select.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Select.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Select.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Select.compile.params.compile_kwargs)
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

    `归属关系 T0> （ T1>  * fromclauses  T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")，它将给定的FROM子句与一个包含[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")的FROM子句关联起来。

        调用此方法会关闭[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象的“自动关联”的默认行为。通常，出现在[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")中的FROM元素将通过它的[WHERE
        clause](glossary.html#term-where-clause)，ORDER
        BY，HAVING或[columns
        clause](glossary.html#term-columns-clause)这个[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象的[FROM
        clause](glossary.html#term-from-clause)。使用[`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")方法设置显式相关集合，可以提供一个固定的FROM对象列表，这些对象可能会在此过程中发生。

        当使用[`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")应用特定的FROM子句进行关联时，无论此[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象相对于将[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")。这与“自动关联”的行为形成鲜明对比，该行为仅与立即包含[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")相关。多级关联确保封闭和封闭[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")之间的链接始终通过至少一个WHERE
        / ORDER BY / HAVING / columns子句进行关联。

        如果传递`None`，则[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象不会关联任何FROM条目，并且所有对象都将无条件地呈现在本地FROM子句中。

        参数：

        **\* fromclauses**
        [¶](#sqlalchemy.sql.expression.Select.correlate.params.*fromclauses)
        -

        a list of one or more [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        constructs, or other compatible constructs (i.e. ORM-mapped
        classes) to become part of the correlate collection.

        在版本0.8.0中更改： ORM映射类被[`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")接受。

        版本0.8.0中已更改： [`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")方法不再无条件地从FROM子句中删除条目；相反，候选FROM条目还必须与位于封闭[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")中的FROM条目匹配，该条目最终包含在WHERE子句，ORDER
        BY子句，HAVING子句或columns子句中一个封闭的`Select()`。

        在版本0.8.2中更改：显式关联通过[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象的任何级别嵌套进行；在以前的0.8版本中，相关只会发生在相对于立即封闭的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")结构中。

        也可以看看

        [`Select.correlate_except()`](#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")

        [Correlated Subqueries](tutorial.html#correlated-subqueries)

    ` correlate_except  T0> （ T1>  * fromclauses  T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")，它将从自动关联过程中省略给定的FROM子句。

        调用[`Select.correlate_except()`](#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")会关闭给定FROM元素的[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象的“自动关联”默认行为。此处指定的元素将无条件出现在FROM列表中，而所有其他FROM元素仍保持正常的自动关联行为。

        在0.8.2版本中进行了更改：对[`Select.correlate_except()`](#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")方法进行了改进，以完全防止此处指定的FROM子句从此[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")

        如果传递`None`，则[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象将关联其所有FROM条目。

        版本0.8.2更改：调用`correlate_except(None)`将正确地自动关联所有FROM子句。

        参数：

        **\*fromclauses**[¶](#sqlalchemy.sql.expression.Select.correlate_except.params.*fromclauses)
        – a list of one or more [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        constructs, or other compatible constructs (i.e. ORM-mapped
        classes) to become part of the correlate-exception collection.

        也可以看看

        [`Select.correlate()`](#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")

        [Correlated Subqueries](tutorial.html#correlated-subqueries)

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.Select.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.Select.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.Select.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.Select.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Select.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.Select.cte "Permalink to this definition")
    :   *继承自* [`cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.Select.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.Select.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    `描述 T0> ¶ T1>`{.descname}
    :   *从* [`description`](#sqlalchemy.sql.expression.FromClause.description "sqlalchemy.sql.expression.FromClause.description")
        *继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        这个FromClause的简要描述。

        主要用于错误消息格式。

    `不同 T0> （ T1>  * EXPR  T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的select()构造，它将DISTINCT应用到它的columns子句。

        参数：

        **\* expr**
        [¶](#sqlalchemy.sql.expression.Select.distinct.params.*expr) -
        可选的列表达式。当存在时，Postgresql方言将呈现`DISTINCT ON （＆lt；表达式＆gt；）`结构。

     `except_`{.descname}(*other*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.Select.except_ "Permalink to this definition")
    :   针对给定的selectable返回此select()构造的SQL EXCEPT。

    `except_all`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.expression.Select.except_all "Permalink to this definition")
    :   根据给定的selectable返回SQL EXCEPT ALL的所有select()构造。

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.Select.execution_options "sqlalchemy.sql.expression.Select.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` FOR_UPDATE  T0> ¶ T1>`{.descname}
    :   *继承自* [`for_update`](#sqlalchemy.sql.expression.GenerativeSelect.for_update "sqlalchemy.sql.expression.GenerativeSelect.for_update")
        *属性* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        为`for_update`属性提供传统方言支持。

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

    ` 320交织 T0> ¶ T1>`{.descname}
    :   返回FromClause元素的显示列表。

    `get_children`{.descname} （ *column\_collections = True*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.sql.expression.Select.get_children "Permalink to this definition")
    :   按照ClauseElement规范返回子元素。

    ` GROUP_BY  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   从 [`group_by()`](#sqlalchemy.sql.expression.GenerativeSelect.group_by "sqlalchemy.sql.expression.GenerativeSelect.group_by")
        *方法继承的*[`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")**

        返回一个新的可选项，其中应用了GROUP BY标准的给定列表。

        该标准将被附加到任何预先存在的GROUP BY标准。

    `具有 T0> （ T1> 具有 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的select()构造，将给定的表达式添加到它的HAVING子句中，通过AND连接到现有子句（如果有的话）。

    ` inner_columns  T0> ¶ T1>`{.descname}
    :   所有ColumnElement表达式的迭代器，这些表达式将被渲染到结果SELECT语句的columns子句中。

    `相交 T0> （ T1> 其他 T2>， ** kwargs  T3> ） T4> ¶ T5 >`{.descname}
    :   根据给定的selectable返回此select()构造的SQL INTERSECT。

    `intersect_all`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.expression.Select.intersect_all "Permalink to this definition")
    :   根据给定的selectable返回一个SQL INTERSECT ALL这个select()构造。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.Select.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.Select.join.params.right) -
            连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Select.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.Select.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Select.join.params.full) -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`label()`](#sqlalchemy.sql.expression.SelectBase.label "sqlalchemy.sql.expression.SelectBase.label")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选择的“标量”表示，嵌入为带有标签的子查询。

        也可以看看

        [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `限制 T0> （ T1> 限制 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`limit()`](#sqlalchemy.sql.expression.GenerativeSelect.limit "sqlalchemy.sql.expression.GenerativeSelect.limit")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        返回一个新的可选择的给定LIMIT标准。

        这是一个数值，通常在结果选择中呈现为`LIMIT`表达式。不支持`LIMIT`的后端将尝试提供类似的功能。

        版本1.0.0更改： - [`Select.limit()`](#sqlalchemy.sql.expression.Select.limit "sqlalchemy.sql.expression.Select.limit")现在可以接受任意SQL表达式以及整数值。

        参数：

        **limit**[¶](#sqlalchemy.sql.expression.Select.limit.params.limit)
        – an integer LIMIT parameter, or a SQL expression that provides
        an integer result.

     `locate_all_froms`{.descname}(*\*args*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.Select.locate_all_froms "Permalink to this definition")
    :   返回此Select所引用的所有FromClause元素的集合。

        这个集合是由`froms`属性返回的超集，这个属性专门用于那些实际将被渲染的FromClause元素。

    `偏移 T0> （ T1> 偏移 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`offset()`](#sqlalchemy.sql.expression.GenerativeSelect.offset "sqlalchemy.sql.expression.GenerativeSelect.offset")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        使用给定的OFFSET标准返回一个新的可选项。

        This is a numeric value which usually renders as an
        `OFFSET` expression in the resulting select.
        不支持`OFFSET`的后端将尝试提供类似的功能。

        版本1.0.0更改： - [`Select.offset()`](#sqlalchemy.sql.expression.Select.offset "sqlalchemy.sql.expression.Select.offset")现在可以接受任意SQL表达式以及整数值。

        参数：

        **offset**[¶](#sqlalchemy.sql.expression.Select.offset.params.offset)
        – an integer OFFSET parameter, or a SQL expression that provides
        an integer result.

    ` ORDER_BY  T0> （ T1>  *条款 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`order_by()`](#sqlalchemy.sql.expression.GenerativeSelect.order_by "sqlalchemy.sql.expression.GenerativeSelect.order_by")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        返回一个新的可选项，其中应用了ORDER BY标准的给定列表。

        该标准将被附加到任何预先存在的ORDER BY标准。

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Select.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.Select.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.Select.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.Select.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Select.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    `prefix_with`{.descname} （ *\* expr*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.Select.prefix_with "Permalink to this definition")
    :   *继承自* [`prefix_with()`](#sqlalchemy.sql.expression.HasPrefixes.prefix_with "sqlalchemy.sql.expression.HasPrefixes.prefix_with")
        *方法 [`HasPrefixes`](#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")*

        在语句关键字后添加一个或多个表达式，即SELECT，INSERT，UPDATE或DELETE。生成。

        这用于支持后端特定的前缀关键字，例如由MySQL提供的前缀关键字。

        例如。：

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

        可以通过多次调用[`prefix_with()`](#sqlalchemy.sql.expression.Select.prefix_with "sqlalchemy.sql.expression.Select.prefix_with")来指定多个前缀。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.Select.prefix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the INSERT,
            UPDATE, or DELETE keyword.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.Select.prefix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制将该前缀的呈现仅限于该方言。

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

    ` reduce_columns  T0> （ T1>  only_synonyms =真 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的：func\`.select\`构造，其中包含从列子句中删除的冗余命名的等价值列。

        这里的“冗余”表示两列中的一列是基于外键引用另一列，或者通过语句的WHERE子句中的简单相等比较来引用。The
        primary purpose of this method is to automatically construct a
        select statement with all uniquely-named columns, without the
        need to use table-qualified labels as [`apply_labels()`](#sqlalchemy.sql.expression.Select.apply_labels "sqlalchemy.sql.expression.Select.apply_labels")
        does.

        当根据外键省略列时，被引用的列是保留的列。当基于WHERE
        eqivalence省略列时，columns子句中的第一列是保留的列。

        参数：

        **only\_synonyms**[¶](#sqlalchemy.sql.expression.Select.reduce_columns.params.only_synonyms)
        – when True, limit the removal of columns to those which have
        the same name as the equivalent.
        否则，将删除所有与另一个等效的列。

        0.8版本中的新功能

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.Select.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.Select.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.Select.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

    ` select_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构，并将给定的FROM表达式合并到它的FROM对象列表中。

        例如。：

            table1 = table('t1', column('a'))
            table2 = table('t2', column('b'))
            s = select([table1.c.a]).\
                select_from(
                    table1.join(table2, table1.c.a==table2.c.b)
                )

        “from”列表是每个元素身份的唯一集合，因此添加一个已经存在的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或其他可选项将不起作用。传递引用已存在的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或其他可选项的[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")将会在呈现的FROM列表中隐藏作为单个元素可选择的存在，而不是呈现它变成一个JOIN子句。

        尽管[`Select.select_from()`](#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")的典型用途是用连接替换默认的派生FROM子句，但如果需要，也可以使用单个表元素多次调用它，如果需要的话FROM子句不能从columns子句中完全派生：

            select([func.count('*')]).select_from(table1)

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   按照ClauseElement规范返回“分组”结构。

        这产生了一个可以嵌入到表达式中的元素。请注意，在构建表达式时，会根据需要自动调用此方法，并且不需要明确使用。

    `后缀 tt> （ * expr，** kw ） T5>`{.descname}
    :   *inherited from the* [`suffix_with()`](#sqlalchemy.sql.expression.HasSuffixes.suffix_with "sqlalchemy.sql.expression.HasSuffixes.suffix_with")
        *method of* [`HasSuffixes`](#sqlalchemy.sql.expression.HasSuffixes "sqlalchemy.sql.expression.HasSuffixes")

        在整个语句后添加一个或多个表达式。

        这用于在特定结构上支持后端特定的后缀关键字。

        例如。：

            stmt = select([col1, col2]).cte().suffix_with(
                "cycle empno set y_cycle to 1 default 0", dialect="oracle")

        多个后缀可以通过多次调用[`suffix_with()`](#sqlalchemy.sql.expression.Select.suffix_with "sqlalchemy.sql.expression.Select.suffix_with")来指定。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.Select.suffix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the target
            clause.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.Select.suffix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制仅将该后缀渲染为该方言。

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.Select.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `union`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.expression.Select.union "Permalink to this definition")
    :   根据给定的selectable返回此select()构造的SQL UNION。

    `union_all`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.expression.Select.union_all "Permalink to this definition")
    :   针对给定的selectable返回此select()构造的SQL UNION ALL。

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Select.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

    `其中 T0> （ T1>  whereclause  T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的select()构造，将给定的表达式添加到其WHERE子句中，通过AND连接到现有子句（如果有的话）。

     `with_for_update`{.descname}(*nowait=False*, *read=False*, *of=None*, *skip\_locked=False*, *key\_share=False*)[¶](#sqlalchemy.sql.expression.Select.with_for_update "Permalink to this definition")
    :   *inherited from the* [`with_for_update()`](#sqlalchemy.sql.expression.GenerativeSelect.with_for_update "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")
        *method of* [`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")

        为[`GenerativeSelect`](#sqlalchemy.sql.expression.GenerativeSelect "sqlalchemy.sql.expression.GenerativeSelect")指定一个`FOR UPDATE`子句。

        例如。：

            stmt = select([table]).with_for_update(nowait=True)

        在像Postgresql或Oracle这样的数据库上，上面的代码会显示如下的语句：

            SELECT table.a, table.b FROM table FOR UPDATE NOWAIT

        在其他后端，`nowait`选项被忽略，而是产生：

            SELECT table.a, table.b FROM table FOR UPDATE

        当不带任何参数调用时，语句将以后缀`FOR UPDATE`进行呈现。然后可以提供其他参数，这些参数允许使用通用数据库特定的变体。

        参数：

        -   **nowait**
            [¶](#sqlalchemy.sql.expression.Select.with_for_update.params.nowait)
            -
            boolean；将在Oracle和Postgresql方言中呈现`FOR  tt> UPDATE NOWAIT`
        -   **读**
            [¶](#sqlalchemy.sql.expression.Select.with_for_update.params.read)
            - boolean；将在MySQL上呈现`LOCK IN SHARE 模式`，`在Postgresql上共享 共享`。On
            Postgresql, when combined with `nowait`,
            will render `FOR SHARE NOWAIT`.
        -   **of**[¶](#sqlalchemy.sql.expression.Select.with_for_update.params.of)
            – SQL expression or list of SQL expression elements
            (typically [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
            objects or a compatible expression) which will render into a
            `FOR UPDATE OF` clause; supported by
            PostgreSQL and Oracle. 可以根据后端呈现为表格或列。
        -   **skip\_locked**
            [¶](#sqlalchemy.sql.expression.Select.with_for_update.params.skip_locked)
            -

            boolean, will render `FOR UPDATE SKIP LOCKED` on Oracle and Postgresql dialects or
            `FOR SHARE SKIP LOCKED` if
            `read=True` is also specified.

            版本1.1.0中的新功能

        -   **key\_share**
            [¶](#sqlalchemy.sql.expression.Select.with_for_update.params.key_share)
            -

            boolean, will render `FOR NO KEY UPDATE`, or if combined with `read=True` will render `FOR KEY SHARE`,
            on the Postgresql dialect.

            版本1.1.0中的新功能

     `with_hint`{.descname}(*selectable*, *text*, *dialect\_name='\*'*)[¶](#sqlalchemy.sql.expression.Select.with_hint "Permalink to this definition")
    :   给这个[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")添加一个索引或其他执行上下文提示。

        相对于给定的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")作为`selectable`传递，提示文本呈现在正在使用的数据库后端的适当位置。论据。方言实现通常使用Python字符串替换语法和令牌`%(name)s`来呈现表或别名的名称。例如。在使用Oracle时，需要：

            select([mytable]).\
                with_hint(mytable, "index(%(name)s ix_mytable)")

        将SQL呈现为：

            select /*+ index(mytable ix_mytable) */ ... from mytable

        The `dialect_name` option will limit the
        rendering of a particular hint to a particular backend.
        例如，同时为Oracle和Sybase添加提示：

            select([mytable]).\
                with_hint(mytable, "index(%(name)s ix_mytable)", 'oracle').\
                with_hint(mytable, "WITH INDEX ix_mytable", 'sybase')

        也可以看看

        [`Select.with_statement_hint()`](#sqlalchemy.sql.expression.Select.with_statement_hint "sqlalchemy.sql.expression.Select.with_statement_hint")

    ` with_only_columns  T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构，其中的columns子句替换为给定的列。

        版本0.7.3更改：由于错误修复，此方法在版本0.7.3中有轻微的行为改变。在版本0.7.3之前，已经预先计算了[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的FROM子句，并添加了新列；在0.7.3及更高版本中，它是在编译时计算的，解决了将列与父表后期绑定的问题。这改变了[`Select.with_only_columns()`](#sqlalchemy.sql.expression.Select.with_only_columns "sqlalchemy.sql.expression.Select.with_only_columns")的行为，因为删除了不再在新列表中表示的FROM子句，但是这种行为更一致，因为FROM子句始终从当前列子句派生。这种方法的最初意图是允许修剪现有列列表的列数比原来存在的列数少；在完全不同的列表中替换列表的用例在0.7.3发布之前一直没有预料到；下面的使用指南说明了这应该如何完成。

        这个方法与使用给定的columns子句调用原始的[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")完全等价。即一份声明：

            s = select([table1.c.a, table1.c.b])
            s = s.with_only_columns([table1.c.b])

        应该完全等同于：

            s = select([table1.c.b])

        这意味着只有从列列表派生的FROM子句将被丢弃，如果新列列表不再包含该FROM：

            >>> table1 = table('t1', column('a'), column('b'))
            >>> table2 = table('t2', column('a'), column('b'))
            >>> s1 = select([table1.c.a, table2.c.b])
            >>> print s1
            SELECT t1.a, t2.b FROM t1, t2
            >>> s2 = s1.with_only_columns([table2.c.b])
            >>> print s2
            SELECT t2.b FROM t1

        在构造中维护特定FROM子句的首选方法，假设它不会在其他地方表示（即不在WHERE子句中等）是使用[`Select.select_from()`](#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from")来设置它：

            >>> s1 = select([table1.c.a, table2.c.b]).\
            ...         select_from(table1.join(table2,
            ...                 table1.c.a==table2.c.a))
            >>> s2 = s1.with_only_columns([table2.c.b])
            >>> print s2
            SELECT t2.b FROM t1 JOIN t2 ON t1.a=t2.a

        还应注意使用传递给[`Select.with_only_columns()`](#sqlalchemy.sql.expression.Select.with_only_columns "sqlalchemy.sql.expression.Select.with_only_columns")的正确的一组列对象。由于该方法基本上等效于首先用给定列调用[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造，传递给[`Select.with_only_columns()`](#sqlalchemy.sql.expression.Select.with_only_columns "sqlalchemy.sql.expression.Select.with_only_columns")的列通常应该是一个子集传递给[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造的那些，而不是那些可从[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的`.c`集合中获得的构造。那是：

            s = select([table1.c.a, table1.c.b]).select_from(table1)
            s = s.with_only_columns([table1.c.b])

        和**不是**：

            # usually incorrect
            s = s.with_only_columns([s.c.b])

        后者将生成SQL：

            SELECT b
            FROM (SELECT t1.a AS a, t1.b AS b
            FROM t1), t1

        由于[`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造基本上被要求从`table1`以及其自身中选择。

     `with_statement_hint`{.descname}(*text*, *dialect\_name='\*'*)[¶](#sqlalchemy.sql.expression.Select.with_statement_hint "Permalink to this definition")
    :   向此[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")添加语句提示。

        该方法类似于[`Select.with_hint()`](#sqlalchemy.sql.expression.Select.with_hint "sqlalchemy.sql.expression.Select.with_hint")，不同之处在于它不需要单独的表格，而是作为整体应用于该语句。

        此处的提示仅针对后端数据库，并可能包含隔离级别，文件指令，提取指令等指令。

        版本1.0.0中的新功能

        也可以看看

        [`Select.with_hint()`](#sqlalchemy.sql.expression.Select.with_hint "sqlalchemy.sql.expression.Select.with_hint")

*class* `sqlalchemy.sql.expression。`{.descclassname} `可选`{.descname} [¶](#sqlalchemy.sql.expression.Selectable "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

    将课程标记为可选

*class* `sqlalchemy.sql.expression。`{.descclassname} `SelectBase`{.descname} [¶](#sqlalchemy.sql.expression.SelectBase "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.HasCTE`](#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")，[`sqlalchemy.sql.expression.Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，[`sqlalchemy.sql.expression.FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

    SELECT语句的基类。

    这包括[`Select`](#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")，[`CompoundSelect`](#sqlalchemy.sql.expression.CompoundSelect "sqlalchemy.sql.expression.CompoundSelect")和[`TextAsFrom`](#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")。

    ` as_scalar  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回这个可选项的'标量'表示，它可以用作列表达式。

        通常，在其子列中只有一列的select语句可以用作标量表达式。

        返回的对象是[`ScalarSelect`](#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")的一个实例。

    `自动提交 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   将'autocommit'标志设置为True返回一个新的可选项。

        从版本0.6开始弃用： `autocommit()`已弃用。使用带有'autocommit'标志的[`Executable.execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")。

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   返回这个可选择的“标量”表示，嵌入为带有标签的子查询。

        也可以看看

        [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")

*class* `sqlalchemy.sql.expression。`{.descclassname} `TableClause`{.descname} （ *name*，*\*列 T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.expression.TableClause "Permalink to this definition")*
:   基础：`sqlalchemy.sql.expression.Immutable`，[`sqlalchemy.sql.expression.FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

    代表最小的“表”结构。

    这是一个轻量级的表格对象，它只有一个名称和一个列集合，通常由[`expression.column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")函数生成：

        from sqlalchemy import table, column

        user = table("user",
                column("id"),
                column("name"),
                column("description"),
        )

    [`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")结构可作为更常用的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的基础，提供常见的[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")服务集合，包括`.c.`收集和声明生成方法。

    It does **not** provide all the additional schema-level services of
    [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
    including constraints, references to other tables, or support for
    [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")-level
    services. 当一个更完全的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")不在手边时，它可以作为一个临时构造用于生成快速SQL语句。

    `__ init __`{.descname} （ *name*，*\*列* ） [](#sqlalchemy.sql.expression.TableClause.__init__ "Permalink to this definition")
    :   构建一个新的[`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`table()`](#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")。

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.TableClause.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.TableClause.columns "sqlalchemy.sql.expression.TableClause.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.TableClause.columns "sqlalchemy.sql.expression.TableClause.columns")或[`c`](#sqlalchemy.sql.expression.TableClause.c "sqlalchemy.sql.expression.TableClause.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.TableClause.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TableClause.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.TableClause.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.TableClause.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.TableClause.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.TableClause.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.TableClause.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.TableClause.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.TableClause.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.TableClause.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.TableClause.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.TableClause.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    `删除`{.descname} （ *whereclause = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.sql.expression.TableClause.delete "Permalink to this definition")
    :   根据这个[`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")生成一个[`delete()`](dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")结构。

        例如。：

            table.delete().where(table.c.id==7)

        有关参数和使用信息，请参阅[`delete()`](dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")。

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

    `implicit_returning`{.descname} *= False* [¶](#sqlalchemy.sql.expression.TableClause.implicit_returning "Permalink to this definition")
    :   [`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")
        doesn’t support having a primary key or column -level defaults,
        so implicit returning doesn’t apply.

    `insert`{.descname} （ *values = None*，*inline = False*，*\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TableClause.insert "Permalink to this definition")
    :   针对这个[`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")生成一个[`insert()`](dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")结构。

        例如。：

            table.insert().values(name='foo')

        有关参数和使用信息，请参见[`insert()`](dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")。

    ` is_derived_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_derived_from()`](#sqlalchemy.sql.expression.FromClause.is_derived_from "sqlalchemy.sql.expression.FromClause.is_derived_from")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        如果FromClause从给定的FromClause中“派生”，则返回True。

        一个例子是从表中派生的表的别名。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.TableClause.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.TableClause.join.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.TableClause.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.TableClause.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.TableClause.join.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TableClause.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.TableClause.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.TableClause.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.TableClause.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.TableClause.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.TableClause.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.TableClause.self_group "sqlalchemy.sql.expression.TableClause.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.TableClause.self_group "sqlalchemy.sql.expression.TableClause.self_group")方法仅返回self。

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.TableClause.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

     `update`{.descname}(*whereclause=None*, *values=None*, *inline=False*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.TableClause.update "Permalink to this definition")
    :   根据这个[`TableClause`](#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")生成一个[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")结构。

        例如。：

            table.update().where(table.c.id==7).values(name='foo')

        有关参数和使用信息，请参阅[`update()`](dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`TableSample`{.descname}(*selectable*, *sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.TableSample "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")

    表示一个TABLESAMPLE子句。

    该对象由所有[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")子类上的[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")模块级函数以及[`FromClause.tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")方法构造而成。

    版本1.1中的新功能

    也可以看看

    [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.TableSample.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.TableSample.columns "sqlalchemy.sql.expression.TableSample.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.TableSample.columns "sqlalchemy.sql.expression.TableSample.columns")或[`c`](#sqlalchemy.sql.expression.TableSample.c "sqlalchemy.sql.expression.TableSample.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.TableSample.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TableSample.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.TableSample.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.TableSample.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.TableSample.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.TableSample.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.TableSample.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.TableSample.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.TableSample.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.TableSample.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.TableSample.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.TableSample.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.TableSample.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.TableSample.join.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.TableSample.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.TableSample.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.TableSample.join.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TableSample.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.TableSample.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.TableSample.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.TableSample.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.TableSample.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.TableSample.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.TableSample.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.TableSample.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.TableSample.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

*class* `sqlalchemy.sql.expression。`{.descclassname} `TextAsFrom`{.descname} （ *text*，*columns*，*positions = False* ） [¶](#sqlalchemy.sql.expression.TextAsFrom "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

    在[`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")界面中包装[`TextClause`](sqlelement.html#sqlalchemy.sql.expression.TextClause "sqlalchemy.sql.expression.TextClause")结构。

    This allows the [`TextClause`](sqlelement.html#sqlalchemy.sql.expression.TextClause "sqlalchemy.sql.expression.TextClause")
    object to gain a `.c` collection and other
    FROM-like capabilities such as [`FromClause.alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias"),
    `SelectBase.cte()`, etc.

    [`TextAsFrom`](#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")结构是通过[`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法生成的
    - 请参阅该方法以获取详细信息。

    版本0.9.0中的新功能

    也可以看看

    [`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")

    [`TextClause.columns()`](sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.expression.TextAsFrom.alias "Permalink to this definition")
    :   *从* [`alias()`](#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的别名。

        这是调用的简写：

            from sqlalchemy import alias
            a = alias(self, name=name)

        有关详细信息，请参阅[`alias()`](#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")。

    ` as_scalar  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选项的'标量'表示，它可以用作列表达式。

        通常，在其子列中只有一列的select语句可以用作标量表达式。

        返回的对象是[`ScalarSelect`](#sqlalchemy.sql.expression.ScalarSelect "sqlalchemy.sql.expression.ScalarSelect")的一个实例。

    `自动提交 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`autocommit()`](#sqlalchemy.sql.expression.SelectBase.autocommit "sqlalchemy.sql.expression.SelectBase.autocommit")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        将'autocommit'标志设置为True返回一个新的可选项。

        从版本0.6开始弃用： `autocommit()`已弃用。使用带有'autocommit'标志的[`Executable.execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")。

    `结合 T0> ¶ T1>`{.descname}
    :   *继承自* [`bind`](#sqlalchemy.sql.expression.Executable.bind "sqlalchemy.sql.expression.Executable.bind")
        *属性* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        返回此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")绑定到的[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")；如果没有找到，则返回None。

        这是遍历，在本地进行检查，然后检查关联对象的“from”子句，直到找到绑定的引擎或连接。

    ` C  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`c`](#sqlalchemy.sql.expression.FromClause.c "sqlalchemy.sql.expression.FromClause.c")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        [`columns`](#sqlalchemy.sql.expression.TextAsFrom.columns "sqlalchemy.sql.expression.TextAsFrom.columns")属性的别名。

    `列 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`columns`](#sqlalchemy.sql.expression.FromClause.columns "sqlalchemy.sql.expression.FromClause.columns")
        *attribute of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        由[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")维护的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的基于命名的集合。

        [`columns`](#sqlalchemy.sql.expression.TextAsFrom.columns "sqlalchemy.sql.expression.TextAsFrom.columns")或[`c`](#sqlalchemy.sql.expression.TextAsFrom.c "sqlalchemy.sql.expression.TextAsFrom.c")集合是使用表绑定或其他可选绑定列构建SQL表达式的入口：

            select([mytable]).where(mytable.c.somecolumn == 5)

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.TextAsFrom.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TextAsFrom.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.TextAsFrom.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.TextAsFrom.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.TextAsFrom.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.TextAsFrom.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.TextAsFrom.compile.params.compile_kwargs)
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

    `对等元等于`{.descname} （ *列*，*等值* ） [](#sqlalchemy.sql.expression.TextAsFrom.correspond_on_equivalents "Permalink to this definition")
    :   *inherited from the* [`correspond_on_equivalents()`](#sqlalchemy.sql.expression.FromClause.correspond_on_equivalents "sqlalchemy.sql.expression.FromClause.correspond_on_equivalents")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回给定列的相应列，或者如果None搜索给定字典中的匹配项。

    `对应列`{.descname} （ *列*，*require\_embedded = False* ） [t5 \>](#sqlalchemy.sql.expression.TextAsFrom.corresponding_column "Permalink to this definition")
    :   *继承自* [`corresponding_column()`](#sqlalchemy.sql.expression.FromClause.corresponding_column "sqlalchemy.sql.expression.FromClause.corresponding_column")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        给定一个[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，从这个[`Selectable`](#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")对象的原始[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")通过共同的祖先返回导出的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")柱。

        参数：

        -   **column**[¶](#sqlalchemy.sql.expression.TextAsFrom.corresponding_column.params.column)
            – the target [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            to be matched
        -   **require\_embedded**[¶](#sqlalchemy.sql.expression.TextAsFrom.corresponding_column.params.require_embedded)
            – only return corresponding columns for the given
            [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement"),
            if the given [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
            is actually present within a sub-element of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").
            Normally the column will match if it merely shares a common
            ancestor with one of the exported columns of this
            [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause").

    `count`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.TextAsFrom.count "Permalink to this definition")
    :   *继承自* [`count()`](#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回一个根据[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")生成的SELECT
        COUNT。

        从版本1.1开始弃用： `FromClause.count()`已弃用。对行进行计数需要正确的列表达式和联接，DISTINCT等。必须提出，否则结果可能不是预期的结果。请直接使用适当的`func.count()`表达式。

        该函数针对表的主键中的第一列或整个表中的第一列生成COUNT。显式使用`func.count()`应该是首选的：

            row_count = conn.scalar(
                select([func.count('*')]).select_from(table)
            )

        也可以看看

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.TextAsFrom.cte "Permalink to this definition")
    :   *继承自* [`cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.TextAsFrom.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.TextAsFrom.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    `描述 T0> ¶ T1>`{.descname}
    :   *从* [`description`](#sqlalchemy.sql.expression.FromClause.description "sqlalchemy.sql.expression.FromClause.description")
        *继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        这个FromClause的简要描述。

        主要用于错误消息格式。

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.TextAsFrom.execution_options "sqlalchemy.sql.expression.TextAsFrom.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` foreign_keys  T0> ¶ T1>`{.descname}
    :   *继承自* [`foreign_keys`](#sqlalchemy.sql.expression.FromClause.foreign_keys "sqlalchemy.sql.expression.FromClause.foreign_keys")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回FromClause引用的ForeignKey对象的集合。

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.get_children "sqlalchemy.sql.expression.ClauseElement.get_children")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的直接子元素。

        这用于访问遍历。

        \*\*
        kwargs可能包含更改返回的集合的标志，例如为了减少更大的遍历而返回项目的子集，或者从不同的上下文返回子项目（例如模式级集合而不是子句-水平）。

    ` is_derived_from  T0> （ T1>  fromclause  T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_derived_from()`](#sqlalchemy.sql.expression.FromClause.is_derived_from "sqlalchemy.sql.expression.FromClause.is_derived_from")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        如果FromClause从给定的FromClause中“派生”，则返回True。

        一个例子是从表中派生的表的别名。

     `join`{.descname}(*right*, *onclause=None*, *isouter=False*, *full=False*)[¶](#sqlalchemy.sql.expression.TextAsFrom.join "Permalink to this definition")
    :   *inherited from the* [`join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        从[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")返回[`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")到另一个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")。

        例如。：

            from sqlalchemy import join

            j = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
            stmt = select([user_table]).select_from(j)

        会沿着以下几行发出SQL：

            SELECT user.id, user.name FROM user
            JOIN address ON user.id = address.user_id

        参数：

        -   **正确**
            [¶](#sqlalchemy.sql.expression.TextAsFrom.join.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.TextAsFrom.join.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **isouter**[¶](#sqlalchemy.sql.expression.TextAsFrom.join.params.isouter)
            – if True, render a LEFT OUTER JOIN, instead of JOIN.
        -   **完整**
            [¶](#sqlalchemy.sql.expression.TextAsFrom.join.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。意味着[`FromClause.join.isouter`](#sqlalchemy.sql.expression.FromClause.join.params.isouter "sqlalchemy.sql.expression.FromClause.join")。

            版本1.1中的新功能

        也可以看看

        [`join()`](#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")
        - 独立功能

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        - 生成的对象的类型

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`label()`](#sqlalchemy.sql.expression.SelectBase.label "sqlalchemy.sql.expression.SelectBase.label")
        *方法* [`SelectBase`](#sqlalchemy.sql.expression.SelectBase "sqlalchemy.sql.expression.SelectBase")

        返回这个可选择的“标量”表示，嵌入为带有标签的子查询。

        也可以看看

        [`as_scalar()`](#sqlalchemy.sql.expression.SelectBase.as_scalar "sqlalchemy.sql.expression.SelectBase.as_scalar")

    `横向 T0> （ T1> 名=无 T2> ） T3> ¶ T4>`{.descname}
    :   *从* [`lateral()`](#sqlalchemy.sql.expression.FromClause.lateral "sqlalchemy.sql.expression.FromClause.lateral")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的LATERAL别名。

        返回值是由顶层[`lateral()`](#sqlalchemy.sql.expression.lateral "sqlalchemy.sql.expression.lateral")函数提供的[`Lateral`](#sqlalchemy.sql.expression.Lateral "sqlalchemy.sql.expression.Lateral")结构。

        版本1.1中的新功能

        也可以看看

        [LATERAL correlation](tutorial.html#lateral-selects) - overview
        of usage.

    `外连接`{.descname} （ *右*，*onclause =无*，*full = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.TextAsFrom.outerjoin "Permalink to this definition")
    :   *从* [`outerjoin()`](#sqlalchemy.sql.expression.FromClause.outerjoin "sqlalchemy.sql.expression.FromClause.outerjoin")
        *方法继承* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        Return a [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")
        from this [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
        to another [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
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
            [¶](#sqlalchemy.sql.expression.TextAsFrom.outerjoin.params.right)
            - 连接的右侧；这是任何[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")对象，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，也可以是可选择兼容的对象，例如ORM映射类。
        -   **onclause**[¶](#sqlalchemy.sql.expression.TextAsFrom.outerjoin.params.onclause)
            – a SQL expression representing the ON clause of the join.
            如果留在`None`，则[`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")将尝试基于外键关系来连接两个表。
        -   **完整**
            [¶](#sqlalchemy.sql.expression.TextAsFrom.outerjoin.params.full)
            -

            如果为True，则渲染一个FULL OUTER JOIN，而不是LEFT OUTER
            JOIN。

            版本1.1中的新功能

        也可以看看

        [`FromClause.join()`](#sqlalchemy.sql.expression.FromClause.join "sqlalchemy.sql.expression.FromClause.join")

        [`Join`](#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.TextAsFrom.params "Permalink to this definition")
    :   *inherited from the* [`params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` primary_key  T0> ¶ T1>`{.descname}
    :   *继承自* [`primary_key`](#sqlalchemy.sql.expression.FromClause.primary_key "sqlalchemy.sql.expression.FromClause.primary_key")
        *属性* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回构成此FromClause主键的Column对象的集合。

     `replace_selectable`{.descname}(*old*, *alias*)[¶](#sqlalchemy.sql.expression.TextAsFrom.replace_selectable "Permalink to this definition")
    :   *继承自* [`replace_selectable()`](#sqlalchemy.sql.expression.FromClause.replace_selectable "sqlalchemy.sql.expression.FromClause.replace_selectable")
        *方法* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        用给定的Alias对象替换所有出现的FromClause'old'，并返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的副本。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.TextAsFrom.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    `选择`{.descname} （ *whereclause = None*，*\*\* params* ） [/ T5\>](#sqlalchemy.sql.expression.TextAsFrom.select "Permalink to this definition")
    :   *inherited from the* [`select()`](#sqlalchemy.sql.expression.FromClause.select "sqlalchemy.sql.expression.FromClause.select")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回这个[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的SELECT。

        也可以看看

        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        - general purpose method which allows for arbitrary column
        lists.

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.TextAsFrom.self_group "sqlalchemy.sql.expression.TextAsFrom.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.TextAsFrom.self_group "sqlalchemy.sql.expression.TextAsFrom.self_group")方法仅返回self。

     `tablesample`{.descname}(*sampling*, *name=None*, *seed=None*)[¶](#sqlalchemy.sql.expression.TextAsFrom.tablesample "Permalink to this definition")
    :   *inherited from the* [`tablesample()`](#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")
        *method of* [`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

        返回此[`FromClause`](#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")的TABLESAMPLE别名。

        返回值是顶级[`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")函数也提供的[`TableSample`](#sqlalchemy.sql.expression.TableSample "sqlalchemy.sql.expression.TableSample")结构。

        版本1.1中的新功能

        也可以看看

        [`tablesample()`](#sqlalchemy.sql.expression.tablesample "sqlalchemy.sql.expression.tablesample")
        - 使用指南和参数

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.TextAsFrom.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。


