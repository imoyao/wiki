---
title: 列元素和表达式
date: 2021-02-20 22:41:36
permalink: /sqlalchemy/core/sqlelement/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
列元素和表达式[¶](#module-sqlalchemy.sql.expression "Permalink to this headline")
=================================================================================

SQL表达式API最基本的部分是“列元素”，它允许基本的SQL表达式支持。所有SQL表达式结构的核心是[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")，它是几个子分支的基础。[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")类是用于构造任何类型的SQL表达式的基本单位。

` sqlalchemy.sql.expression。 T0> 所有_  T1> （ T2>  EXPR  T3> ） T4> ¶< / T5>`{.descclassname}
:   产生一个ALL表达式。

    这可能适用于某些方言的数组类型（例如postgresql），或适用于其他方面的子查询（例如mysql）。例如。：

        # postgresql '5 = ALL (somearray)'
        expr = 5 == all_(mytable.c.somearray)

        # mysql '5 = ALL (SELECT value FROM table)'
        expr = 5 == all_(select([table.c.value]))

    版本1.1中的新功能

    也可以看看

    [`expression.any_()`](#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")

` sqlalchemy.sql.expression。 T0> 和_  T1> （ T2>  *条款 T3> ） T4> ¶  T5>`{.descclassname}
:   Produce a conjunction of expressions joined by `AND`.

    例如。：

        from sqlalchemy import and_

        stmt = select([users_table]).where(
                        and_(
                            users_table.c.name == 'wendy',
                            users_table.c.enrolled == True
                        )
                    )

    使用Python `&`运算符也可以使用[`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")连接符（但要注意复合表达式需要用括号括起来才能用Python运算符优先级行为来运行）：

        stmt = select([users_table]).where(
                        (users_table.c.name == 'wendy') &
                        (users_table.c.enrolled == True)
                    )

    在某些情况下，[`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")操作也是隐含的；例如，可以针对一个语句多次调用[`Select.where()`](selectable.html#sqlalchemy.sql.expression.Select.where "sqlalchemy.sql.expression.Select.where")方法，这会影响每个子句使用[`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")进行组合：

        stmt = select([users_table]).\
                    where(users_table.c.name == 'wendy').\
                    where(users_table.c.enrolled == True)

    也可以看看

    [`or_()`](#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")

` sqlalchemy.sql.expression。 T0> 任何_  T1> （ T2>  EXPR  T3> ） T4> ¶< / T5>`{.descclassname}
:   产生一个ANY表达式。

    这可能适用于某些方言的数组类型（例如postgresql），或适用于其他方面的子查询（例如mysql）。例如。：

        # postgresql '5 = ANY (somearray)'
        expr = 5 == any_(mytable.c.somearray)

        # mysql '5 = ANY (SELECT value FROM table)'
        expr = 5 == any_(select([table.c.value]))

    版本1.1中的新功能

    也可以看看

    [`expression.all_()`](#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")

` sqlalchemy.sql.expression。 T0>  ASC  T1> （ T2> 列 T3> ） T4> ¶< / T5>`{.descclassname}
:   产生一个升序`ORDER BY`子句元素。

    例如。：

        from sqlalchemy import asc
        stmt = select([users_table]).order_by(asc(users_table.c.name))

    将生成SQL为：

        SELECT id, name FROM user ORDER BY name ASC

    [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")函数是所有SQL表达式上可用的[`ColumnElement.asc()`](#sqlalchemy.sql.expression.ColumnElement.asc "sqlalchemy.sql.expression.ColumnElement.asc")方法的独立版本，例如：

        stmt = select([users_table]).order_by(users_table.c.name.asc())

    参数：

    **column**[¶](#sqlalchemy.sql.expression.asc.params.column) – A
    [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    (e.g. scalar SQL expression) with which to apply the [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")
    operation.

    也可以看看

    [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")

    [`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")

    [`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")

    [`Select.order_by()`](selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")

 `sqlalchemy.sql.expression.`{.descclassname}`between`{.descname}(*expr*, *lower\_bound*, *upper\_bound*, *symmetric=False*)[¶](#sqlalchemy.sql.expression.between "Permalink to this definition")
:   产生一个`BETWEEN`谓词子句。

    例如。：

        from sqlalchemy import between
        stmt = select([users_table]).where(between(users_table.c.id, 5, 7))

    会产生类似于以下的SQL：

        SELECT id, name FROM user WHERE id BETWEEN :id_1 AND :id_2

    The [`between()`](#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")
    function is a standalone version of the
    [`ColumnElement.between()`](#sqlalchemy.sql.expression.ColumnElement.between "sqlalchemy.sql.expression.ColumnElement.between")
    method available on all SQL expressions, as in:

        stmt = select([users_table]).where(users_table.c.id.between(5, 7))

    如果值不是[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")子类，则所有传递给()之间传递给[`between()`](#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")例如，可以比较三个固定值，如下所示：

        print(between(5, 3, 7))

    这会产生：

        :param_1 BETWEEN :param_2 AND :param_3

    参数：

    -   **expr**[¶](#sqlalchemy.sql.expression.between.params.expr) – a
        column expression, typically a [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
        instance or alternatively a Python scalar expression to be
        coerced into a column expression, serving as the left side of
        the `BETWEEN` expression.
    -   **lower\_bound**[¶](#sqlalchemy.sql.expression.between.params.lower_bound)
        – a column or Python scalar expression serving as the lower
        bound of the right side of the `BETWEEN`
        expression.
    -   **upper\_bound**[¶](#sqlalchemy.sql.expression.between.params.upper_bound)
        – a column or Python scalar expression serving as the upper
        bound of the right side of the `BETWEEN`
        expression.
    -   **symmetric**
        [¶](#sqlalchemy.sql.expression.between.params.symmetric) -

        如果为True，则呈现“BETWEEN
        SYMMETRIC”。请注意，并非所有数据库都支持此语法。

        版本0.9.5中的新功能

    也可以看看

    [`ColumnElement.between()`](#sqlalchemy.sql.expression.ColumnElement.between "sqlalchemy.sql.expression.ColumnElement.between")

 `sqlalchemy.sql.expression.`{.descclassname}`bindparam`{.descname}(*key*, *value=symbol('NO\_ARG')*, *type\_=None*, *unique=False*, *required=symbol('NO\_ARG')*, *quote=None*, *callable\_=None*, *isoutparam=False*, *\_compared\_to\_operator=None*, *\_compared\_to\_type=None*)[¶](#sqlalchemy.sql.expression.bindparam "Permalink to this definition")
:   产生一个“约束表达”。

    返回值是[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")的一个实例；这是一个[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")子类，它表示SQL表达式中所谓的“占位符”值，其值是在针对数据库连接执行的语句处提供的。

    在SQLAlchemy中，[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")构造能够携带将在表达时最终使用的实际值。通过这种方式，它不仅可以作为最终人口的“占位符”，还可以作为表示不应直接在SQL语句中呈现的所谓“不安全”值的手段，而应该传递给[DBAPI](glossary.html#term-dbapi)作为需要正确转义并可能为了类型安全性而处理的值。

    明确使用[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")时，用例通常是传统延迟参数之一；
    [`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构接受一个名称，然后可以在执行时引用它：

        from sqlalchemy import bindparam

        stmt = select([users_table]).\
                    where(users_table.c.name == bindparam('username'))

    上述语句在呈现时会产生类似于以下内容的SQL：

        SELECT id, name FROM user WHERE name = :username

    为了填充上面的`:username`的值，该值通常会在执行时应用于像[`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")这样的方法：

        result = connection.execute(stmt, username='wendy')

    显式使用[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")在生成要多次调用的UPDATE或DELETE语句时也很常见，其中语句的WHERE标准将在每次调用时更改，例如：

        stmt = (users_table.update().
                where(user_table.c.name == bindparam('username')).
                values(fullname=bindparam('fullname'))
                )

        connection.execute(
            stmt, [{"username": "wendy", "fullname": "Wendy Smith"},
                   {"username": "jack", "fullname": "Jack Jones"},
                   ]
        )

    SQLAlchemy的Core表达式系统以隐含的意义广泛使用[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")。通常传递给几乎所有SQL表达式函数的Python文本值被强制转换为固定的[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构。例如，给定一个比较操作，例如：

        expr = users_table.c.name == 'Wendy'

    The above expression will produce a [`BinaryExpression`](#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")
    construct, where the left side is the [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object representing the `name` column, and the
    right side is a [`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
    representing the literal value:

        print(repr(expr.right))
        BindParameter('%(4327771088 name)s', 'Wendy', type_=String())

    上面的表达式将呈现SQL，如：

        user.name = :name_1

    其中`:name_1`参数名称是匿名名称。实际的字符串`Wendy`不在呈现的字符串中，而是随后在语句执行中使用它。如果我们调用如下的语句：

        stmt = select([users_table]).where(users_table.c.name == 'Wendy')
        result = connection.execute(stmt)

    我们将看到SQL日志输出为：

        SELECT "user".id, "user".name
        FROM "user"
        WHERE "user".name = %(name_1)s
        {'name_1': 'Wendy'}

    在上面，我们看到`Wendy`作为参数传递给数据库，占位符`:name_1`以目标数据库的适当形式呈现，在这种情况下，Postgresql数据库。

    同样，就“VALUES”部分而言，在使用[CRUD](glossary.html#term-crud)语句时，会自动调用[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")。[`insert()`](dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")结构会产生一个`INSERT`表达式，该表达式在语句执行时将根据传递的参数生成绑定占位符，如下所示：

        stmt = users_table.insert()
        result = connection.execute(stmt, name='Wendy')

    以上将生成SQL输出为：

        INSERT INTO "user" (name) VALUES (%(name)s)
        {'name': 'Wendy'}

    The [`Insert`](dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
    construct, at compilation/execution time, rendered a single
    [`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
    mirroring the column name `name` as a result of
    the single `name` parameter we passed to the
    [`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")
    method.

    参数：

    -   **key**[¶](#sqlalchemy.sql.expression.bindparam.params.key) –
        the key (e.g. the name) for this bind param.
        将在生成的SQL语句中用于使用命名参数的方言。如果其他[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")对象存在于同一个关键字中，或者其长度过长并且需要截断，则可能会修改此值。
    -   **value**[¶](#sqlalchemy.sql.expression.bindparam.params.value)
        – Initial value for this bind param.
        如果没有其他值针对此特定参数名称的语句执行方法指示，则将在语句执行时间用作传递给DBAPI的此参数的值。默认为`None`。
    -   **callable \_**
        [¶](#sqlalchemy.sql.expression.bindparam.params.callable_) -
        代替“value”的可调用函数。该函数将在语句执行时调用以确定最终值。用于在创建子句结构时无法确定实际绑定值的场景，但嵌入式绑定值仍然是可取的。
    -   **type \_**
        [¶](#sqlalchemy.sql.expression.bindparam.params.type_) -

        [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")类或实例表示此[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")的可选数据类型。如果没有通过，基于给定的值可以自动确定绑定的类型；例如，诸如`str`，`int`，`bool`等普通Python类型可能会导致[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")，[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")或[`Boolean`](type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")

        [`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")的类型特别重要，因为类型将在将值传递到数据库之前对值进行预处理。例如，引用datetime值并指定为保存[`DateTime`](type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")类型的[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")可以将所需的转换应用于该值（例如SQLite上的字符串化）在将值传递给数据库之前。

    -   **unique**[¶](#sqlalchemy.sql.expression.bindparam.params.unique)
        – if True, the key name of this [`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
        will be modified if another [`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
        of the same name already has been located within the containing
        expression.
        当生成所谓的“匿名”绑定表达式时，这个标志一般由内部使用，它通常不适用于显式命名的[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构。
    -   **必填**
        [¶](#sqlalchemy.sql.expression.bindparam.params.required) -

        如果`True`，则在执行时需要一个值。如果没有通过，如果[`bindparam.value`](#sqlalchemy.sql.expression.bindparam.params.value "sqlalchemy.sql.expression.bindparam")或[`bindparam.callable`](#sqlalchemy.sql.expression.bindparam.params.callable "sqlalchemy.sql.expression.bindparam")都没有通过，则默认为`True`。如果其中任何一个参数存在，那么[`bindparam.required`](#sqlalchemy.sql.expression.bindparam.params.required "sqlalchemy.sql.expression.bindparam")默认为`False`。

        在0.8版中更改：如果未指定`required`标志，它将自动设置为`True`或`False`取决于是否指定了`value`或`callable`参数。

    -   **quote**[¶](#sqlalchemy.sql.expression.bindparam.params.quote)
        – True if this parameter name requires quoting and is not
        currently known as a SQLAlchemy reserved word; this currently
        only applies to the Oracle backend, where bound names must
        sometimes be quoted.
    -   **isoutparam**[¶](#sqlalchemy.sql.expression.bindparam.params.isoutparam)
        – if True, the parameter should be treated like a stored
        procedure “OUT” parameter. 这适用于支持OUT参数的后端，如Oracle。

    也可以看看

    [Bind Parameter Objects](tutorial.html#coretutorial-bind-param)

    [Insert Expressions](tutorial.html#coretutorial-insert-expressions)

    [`outparam()`](#sqlalchemy.sql.expression.outparam "sqlalchemy.sql.expression.outparam")

 `sqlalchemy.sql.expression.`{.descclassname}`case`{.descname}(*whens*, *value=None*, *else\_=None*)[¶](#sqlalchemy.sql.expression.case "Permalink to this definition")
:   产生一个`CASE`表达式。

    SQL中的`CASE`构造是一个条件对象，其行为有点类似于其他语言中的“if /
    then”构造。它返回一个[`Case`](#sqlalchemy.sql.expression.Case "sqlalchemy.sql.expression.Case")的实例。

    [`case()`](#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")
    in its usual form is passed a list of “when” constructs, that is, a
    list of conditions and results as tuples:

        from sqlalchemy import case

        stmt = select([users_table]).\
                    where(
                        case(
                            [
                                (users_table.c.name == 'wendy', 'W'),
                                (users_table.c.name == 'jack', 'J')
                            ],
                            else_='E'
                        )
                    )

    上述语句将生成类似于以下的SQL：

        SELECT id, name FROM user
        WHERE CASE
            WHEN (name = :name_1) THEN :param_1
            WHEN (name = :name_2) THEN :param_2
            ELSE :param_3
        END

    When simple equality expressions of several values against a single
    parent column are needed, [`case()`](#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")
    also has a “shorthand” format used via the [`case.value`](#sqlalchemy.sql.expression.case.params.value "sqlalchemy.sql.expression.case")
    parameter, which is passed a column expression to be compared.
    在这种形式下，[`case.whens`](#sqlalchemy.sql.expression.case.params.whens "sqlalchemy.sql.expression.case")参数作为字典传递，其中包含要与键入结果表达式进行比较的表达式。以下声明等同于上述声明：

        stmt = select([users_table]).\
                    where(
                        case(
                            {"wendy": "W", "jack": "J"},
                            value=users_table.c.name,
                            else_='E'
                        )
                    )

    在[`case.whens`](#sqlalchemy.sql.expression.case.params.whens "sqlalchemy.sql.expression.case")以及[`case.else_`](#sqlalchemy.sql.expression.case.params.else_ "sqlalchemy.sql.expression.case")中被接受为结果值的值从Python文字转换为[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")构造。SQL表达式，例如[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")结构也被接受。要将文字字符串表达式强制转换为内联呈现的常量表达式，请使用[`literal_column()`](#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")结构，如下所示：

        from sqlalchemy import case, literal_column

        case(
            [
                (
                    orderline.c.qty > 100,
                    literal_column("'greaterthan100'")
                ),
                (
                    orderline.c.qty > 10,
                    literal_column("'greaterthan10'")
                )
            ],
            else_=literal_column("'lessthan10'")
        )

    以上将渲染给定的常量而不使用结果值的绑定参数（但仍然用于比较值），如下所示：

        CASE
            WHEN (orderline.qty > :qty_1) THEN 'greaterthan100'
            WHEN (orderline.qty > :qty_2) THEN 'greaterthan10'
            ELSE 'lessthan10'
        END

    参数：

    -   **whens** [¶](#sqlalchemy.sql.expression.case.params.whens) -

        The criteria to be compared against, [`case.whens`](#sqlalchemy.sql.expression.case.params.whens "sqlalchemy.sql.expression.case")
        accepts two different forms, based on whether or not
        [`case.value`](#sqlalchemy.sql.expression.case.params.value "sqlalchemy.sql.expression.case")
        is used.

        In the first form, it accepts a list of 2-tuples; each 2-tuple
        consists of `(<sql expression>, <value>)`,
        where the SQL expression is a boolean expression and “value” is
        a resulting value, e.g.:

            case([
                (users_table.c.name == 'wendy', 'W'),
                (users_table.c.name == 'jack', 'J')
            ])

        在第二种形式中，它接受映射到结果值的比较值的Python字典；这种形式要求[`case.value`](#sqlalchemy.sql.expression.case.params.value "sqlalchemy.sql.expression.case")存在，并且值将使用`==`运算符进行比较，例如：

            case(
                {"wendy": "W", "jack": "J"},
                value=users_table.c.name
            )

    -   **value**[¶](#sqlalchemy.sql.expression.case.params.value) – An
        optional SQL expression which will be used as a fixed
        “comparison point” for candidate values within a dictionary
        passed to [`case.whens`](#sqlalchemy.sql.expression.case.params.whens "sqlalchemy.sql.expression.case").
    -   **else\_**[¶](#sqlalchemy.sql.expression.case.params.else_) – An
        optional SQL expression which will be the evaluated result of
        the `CASE` construct if all expressions
        within [`case.whens`](#sqlalchemy.sql.expression.case.params.whens "sqlalchemy.sql.expression.case")
        evaluate to false.
        省略时，如果没有“when”表达式评估为true，大多数数据库将产生NULL结果。

 `sqlalchemy.sql.expression.`{.descclassname}`cast`{.descname}(*expression*, *type\_*)[¶](#sqlalchemy.sql.expression.cast "Permalink to this definition")
:   产生一个`CAST`表达式。

    [`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")返回[`Cast`](#sqlalchemy.sql.expression.Cast "sqlalchemy.sql.expression.Cast")的实例。

    例如。：

        from sqlalchemy import cast, Numeric

        stmt = select([
                    cast(product_table.c.unit_price, Numeric(10, 4))
                ])

    上述语句将生成类似于以下的SQL：

        SELECT CAST(unit_price AS NUMERIC(10, 4)) FROM product

    [`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")函数在使用时执行两个不同的函数。首先是它在结果SQL字符串中呈现`CAST`表达式。The second is that it associates the given type
    (e.g. [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
    class or instance) with the column expression on the Python side,
    which means the expression will take on the expression operator
    behavior associated with that type, as well as the bound-value
    handling and result-row-handling behavior of the type.

    版本0.9.0更改： [`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")现在将给定类型应用于表达式，以使其对边界值生效。除了结果处理之外，Python到数据库的方向也是如此。数据库到Python，方向。

    [`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")的替代方法是[`type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")函数。此函数执行将表达式与特定类型关联的第二个任务，但不会在SQL中呈现`CAST`表达式。

    参数：

    -   **expression**[¶](#sqlalchemy.sql.expression.cast.params.expression)
        – A SQL expression, such as a [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
        expression or a Python string which will be coerced into a bound
        literal value.
    -   **type\_**[¶](#sqlalchemy.sql.expression.cast.params.type_) – A
        [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        class or instance indicating the type to which the
        `CAST` should apply.

    也可以看看

    [`type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")
    - 没有发射CAST的Python端类型强制。

 `sqlalchemy.sql.expression.`{.descclassname}`column`{.descname}(*text*, *type\_=None*, *is\_literal=False*, *\_selectable=None*)[¶](#sqlalchemy.sql.expression.column "Permalink to this definition")
:   生成一个[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")对象。

    [`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")类的轻量级模拟。[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")函数可以仅用一个名字来调用，如下所示：

        from sqlalchemy import column

        id, name = column("id"), column("name")
        stmt = select([id, name]).select_from("user")

    上面的语句会产生如下的SQL：

        SELECT id, name FROM user

    Once constructed, [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    may be used like any other SQL expression element such as within
    [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
    constructs:

        from sqlalchemy.sql import column

        id, name = column("id"), column("name")
        stmt = select([id, name]).select_from("user")

    假设由[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")处理的文本像数据库列的名称一样处理；如果字符串包含混合大小写，特殊字符或匹配目标后端上的已知保留字，则列表达式将使用由后端确定的引用行为进行呈现。要生成一个完全不带引号的文本SQL表达式，请改为使用[`literal_column()`](#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")，或将`True`作为[`column.is_literal`](#sqlalchemy.sql.expression.column.params.is_literal "sqlalchemy.sql.expression.column")此外，完整的SQL语句最好使用[`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构进行处理。

    [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    can be used in a table-like fashion by combining it with the
    [`table()`](selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")
    function (which is the lightweight analogue to [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"))
    to produce a working table construct with minimal boilerplate:

        from sqlalchemy import table, column, select

        user = table("user",
                column("id"),
                column("name"),
                column("description"),
        )

        stmt = select([user.c.description]).where(user.c.name == 'wendy')

    A [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    / [`table()`](selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")
    construct like that illustrated above can be created in an ad-hoc
    fashion and is not associated with any [`schema.MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData"),
    DDL, or events, unlike its [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    counterpart.

    Changed in version 1.0.0: [`expression.column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    can now be imported from the plain `sqlalchemy`
    namespace like any other SQL element.

    参数：

    -   **文本** [¶](#sqlalchemy.sql.expression.column.params.text) -
        元素的文本。
    -   **type**[¶](#sqlalchemy.sql.expression.column.params.type) –
        [`types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        object which can associate this [`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")
        with a type.
    -   **is\_literal**[¶](#sqlalchemy.sql.expression.column.params.is_literal)
        – if True, the [`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")
        is assumed to be an exact expression that will be delivered to
        the output with no quoting rules applied regardless of case
        sensitive settings. the [`literal_column()`](#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")
        function essentially invokes [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
        while passing `is_literal=True`.

    也可以看看

    [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

    [`literal_column()`](#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")

    [`table()`](selectable.html#sqlalchemy.sql.expression.table "sqlalchemy.sql.expression.table")

    [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")

    [Using More Specific Text with table(), literal\_column(), and
    column()](tutorial.html#sqlexpression-literal-column)中使用更多特定文本

`sqlalchemy.sql.expression。`{.descclassname} `整理`{.descname} （ *表达式*，*整理* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.collate "Permalink to this definition")
:   返回子句`表达式 COLLATE 整理`。

    例如。：

        collate(mycolumn, 'utf8_bin')

    生产：

        mycolumn COLLATE utf8_bin

` sqlalchemy.sql.expression。 T0> 递减 T1> （ T2> 列 T3> ） T4> ¶< / T5>`{.descclassname}
:   产生一个降序`ORDER BY`子句元素。

    例如。：

        from sqlalchemy import desc

        stmt = select([users_table]).order_by(desc(users_table.c.name))

    将生成SQL为：

        SELECT id, name FROM user ORDER BY name DESC

    [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")函数是所有SQL表达式上可用的[`ColumnElement.desc()`](#sqlalchemy.sql.expression.ColumnElement.desc "sqlalchemy.sql.expression.ColumnElement.desc")方法的独立版本，例如：

        stmt = select([users_table]).order_by(users_table.c.name.desc())

    参数：

    **column**[¶](#sqlalchemy.sql.expression.desc.params.column) – A
    [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    (e.g. scalar SQL expression) with which to apply the [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")
    operation.

    也可以看看

    [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")

    [`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")

    [`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")

    [`Select.order_by()`](selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")

` sqlalchemy.sql.expression。 T0> 不同 T1> （ T2>  EXPR  T3> ） T4> ¶< / T5>`{.descclassname}
:   生成列表达式级别的一元`DISTINCT`子句。

    这将`DISTINCT`关键字应用于单个列表达式，并且通常包含在聚合函数中，如下所示：

        from sqlalchemy import distinct, func
        stmt = select([func.count(distinct(users_table.c.name))])

    以上将产生一个表达式，类似于：

        SELECT COUNT(DISTINCT name) FROM user

    The [`distinct()`](#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")
    function is also available as a column-level method, e.g.
    [`ColumnElement.distinct()`](#sqlalchemy.sql.expression.ColumnElement.distinct "sqlalchemy.sql.expression.ColumnElement.distinct"),
    as in:

        stmt = select([func.count(users_table.c.name.distinct())])

    [`distinct()`](#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")运算符与[`Select`](selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")的[`Select.distinct()`](selectable.html#sqlalchemy.sql.expression.Select.distinct "sqlalchemy.sql.expression.Select.distinct")方法不同，后者会生成`SELECT`将`DISTINCT`语句作为一个整体应用于结果集，例如一个`SELECT DISTINCT`表达式。请参阅该方法以获取更多信息。

    也可以看看

    [`ColumnElement.distinct()`](#sqlalchemy.sql.expression.ColumnElement.distinct "sqlalchemy.sql.expression.ColumnElement.distinct")

    [`Select.distinct()`](selectable.html#sqlalchemy.sql.expression.Select.distinct "sqlalchemy.sql.expression.Select.distinct")

    [`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

 `sqlalchemy.sql.expression.`{.descclassname}`extract`{.descname}(*field*, *expr*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.extract "Permalink to this definition")
:   返回一个[`Extract`](#sqlalchemy.sql.expression.Extract "sqlalchemy.sql.expression.Extract")结构。

    这通常可以从[`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")命名空间中以[`extract()`](#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")和`func.extract`的形式获得。

` sqlalchemy.sql.expression。 T0> 假 T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   返回一个[`False_`](#sqlalchemy.sql.elements.False_ "sqlalchemy.sql.elements.False_")结构。

    例如。：

        >>> from sqlalchemy import false
        >>> print select([t.c.x]).where(false())
        SELECT x FROM t WHERE false

    不支持真/假常量的后端将呈现为针对1或0的表达式：

        >>> print select([t.c.x]).where(false())
        SELECT x FROM t WHERE 0 = 1

    The [`true()`](#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
    and [`false()`](#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")
    constants also feature “short circuit” operation within an
    [`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
    or [`or_()`](#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")
    conjunction:

        >>> print select([t.c.x]).where(or_(t.c.x > 5, true()))
        SELECT x FROM t WHERE true

        >>> print select([t.c.x]).where(and_(t.c.x > 5, false()))
        SELECT x FROM t WHERE false

    在版本0.9中更改： [`true()`](#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")和[`false()`](#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")具有在不支持真/假的连接词和方言中更好的集成行为常量。

    也可以看看

    [`true()`](#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")

`sqlalchemy.sql.expression。`{.descclassname} `func`{.descname} *=＆lt； sqlalchemy.sql.functions.\_FunctionGenerator对象＆gt；* [¶](#sqlalchemy.sql.expression.func "Permalink to this definition")
:   生成SQL函数表达式。

    [`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")是一个特殊的对象实例，它基于基于名称的属性生成SQL函数，例如：

        >>> print(func.count(1))
        count(:param_1)

    该元素是一个像任何其他列一样的SQL元素，并且以这种方式使用：

        >>> print(select([func.count(table.c.id)]))
        SELECT count(sometable.id) FROM sometable

    任何名字都可以给予[`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")。如果函数名称对SQLAlchemy是未知的，它将完全按照原样呈现。对于SQLAlchemy知道的常用SQL函数，名称可能被解释为一个*通用函数*，它将被正确编译到目标数据库：

        >>> print(func.current_timestamp())
        CURRENT_TIMESTAMP

    要调用点分隔包中存在的函数，请按照相同的方式指定它们：

        >>> print(func.stats.yield_curve(5, 10))
        stats.yield_curve(:yield_curve_1, :yield_curve_2)

    可以使SQLAlchemy知道函数的返回类型，以启用特定于类型的词法和基于结果的行为。例如，要确保基于字符串的函数返回Unicode值并在表达式中将其类似地视为字符串，请将[`Unicode`](type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")指定为类型：

        >>> print(func.my_string(u'hi', type_=Unicode) + ' ' +
        ...       func.my_string(u'there', type_=Unicode))
        my_string(:my_string_1) || :my_string_2 || my_string(:my_string_3)

    由[`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")调用返回的对象通常是[`Function`](functions.html#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")的一个实例。此对象符合“列”界面，包括比较和标注功能。该对象还可以传递给[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")或[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的[`execute()`](connections.html#sqlalchemy.engine.Connectable.execute "sqlalchemy.engine.Connectable.execute")方法，在那里它首先被包装在SELECT语句中：

        print(connection.execute(func.current_timestamp()).scalar())

    在一些例外情况下，[`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")访问器将把名称重定向到内置表达式，例如[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")或[`extract()`](#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")因为这些名称具有众所周知的含义，但与SQLAlchemy透视图中的“函数”不完全相同。

    版本0.8中的新功能 [`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")可以返回常用准功能名称的非函数表达式结构，如[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")和[`extract()`](#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")

    被解释为“通用”函数的函数知道如何自动计算它们的返回类型。有关已知泛型函数的列表，请参阅[SQL
    and Generic Functions](functions.html#generic-functions)。

    注意

    [`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")构造仅有限地支持调用独立的“存储过程”，特别是那些有特殊参数化问题的构件。

    有关如何将DBAPI级`callproc()`方法用于完全传统存储过程的详细信息，请参阅[Calling Stored
    Procedures](connections.html#stored-procedures)部分。

 `sqlalchemy.sql.expression.`{.descclassname}`funcfilter`{.descname}(*func*, *\*criterion*)[¶](#sqlalchemy.sql.expression.funcfilter "Permalink to this definition")
:   针对一个函数产生一个[`FunctionFilter`](#sqlalchemy.sql.expression.FunctionFilter "sqlalchemy.sql.expression.FunctionFilter")对象。

    用于聚合和窗口函数，用于支持“FILTER”子句的数据库后端。

    例如。：

        from sqlalchemy import funcfilter
        funcfilter(func.count(1), MyClass.name == 'some name')

    会产生“COUNT（1）FILTER（WHERE myclass.name ='某个名字'）”。

    该函数也可以通过[`FunctionElement.filter()`](functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")方法从[`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")构造本身使用。

    版本1.0.0中的新功能

    也可以看看

    [`FunctionElement.filter()`](functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")

 `sqlalchemy.sql.expression.`{.descclassname}`label`{.descname}(*name*, *element*, *type\_=None*)[¶](#sqlalchemy.sql.expression.label "Permalink to this definition")
:   为给定的[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")返回一个[`Label`](#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")对象。

    标签通常通过`AS` SQL关键字更改`SELECT`语句的columns子句中元素的名称。

    通过[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")上的[`ColumnElement.label()`](#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label")方法可以更方便地使用此功能。

    参数：

    -   **名称** [¶](#sqlalchemy.sql.expression.label.params.name) -
        标签名称
    -   **obj**[¶](#sqlalchemy.sql.expression.label.params.obj) – a
        [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement").

 `sqlalchemy.sql.expression.`{.descclassname}`literal`{.descname}(*value*, *type\_=None*)[¶](#sqlalchemy.sql.expression.literal "Permalink to this definition")
:   返回绑定到绑定参数的文字子句。

    当非[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")对象（例如字符串，整数，日期等）时，将自动创建文本子句。用于与[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")子类的比较操作，例如[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象。使用此函数强制生成一个文字子句，该子句将被创建为具有绑定值的[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")。

    参数：

    -   **value**[¶](#sqlalchemy.sql.expression.literal.params.value) –
        the value to be bound.
        可以是底层DB-API支持的任何Python对象，也可以通过给定的类型参数进行翻译。
    -   **type\_**[¶](#sqlalchemy.sql.expression.literal.params.type_) –
        an optional [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        which will provide bind-parameter translation for this literal.

 `sqlalchemy.sql.expression.`{.descclassname}`literal_column`{.descname}(*text*, *type\_=None*)[¶](#sqlalchemy.sql.expression.literal_column "Permalink to this definition")
:   生成[`column.is_literal`](#sqlalchemy.sql.expression.column.params.is_literal "sqlalchemy.sql.expression.column")标志设置为True的[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")对象。

    [`literal_column()`](#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")
    is similar to [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column"),
    except that it is more often used as a “standalone” column
    expression that renders exactly as stated; while [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    stores a string name that will be assumed to be part of a table and
    may be quoted as such, [`literal_column()`](#sqlalchemy.sql.expression.literal_column "sqlalchemy.sql.expression.literal_column")
    can be that, or any other arbitrary column-oriented expression.

    参数：

    -   **文本**
        [¶](#sqlalchemy.sql.expression.literal_column.params.text) -
        表达式的文本；可以是任何SQL表达式。引用规则将不适用。要指定应受引用规则约束的列名称表达式，请使用[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")函数。
    -   **type\_**[¶](#sqlalchemy.sql.expression.literal_column.params.type_)
        – an optional [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        object which will provide result-set translation and additional
        expression semantics for this column.
        如果保留为None，那么类型将是NullType。

    也可以看看

    [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")

    [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")

    [Using More Specific Text with table(), literal\_column(), and
    column()](tutorial.html#sqlexpression-literal-column)中使用更多特定文本

` sqlalchemy.sql.expression。 T0> 不_  T1> （ T2> 子句 T3> ） T4> ¶< / T5>`{.descclassname}
:   返回给定子句的否定，即`NOT(clause)`。

    所有[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")子类中的`~`运算符也被重载，以产生相同的结果。

` sqlalchemy.sql.expression。 T0> 空 T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   返回一个常量[`Null`](#sqlalchemy.sql.elements.Null "sqlalchemy.sql.elements.Null")结构。

` sqlalchemy.sql.expression。 T0>  nullsfirst  T1> （ T2> 列 T3> ） T4> ¶< / T5>`{.descclassname}
:   为`ORDER BY  t3生成NULLS FIRST` \>表达。

    [`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")
    is intended to modify the expression produced by [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")
    or [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc"),
    and indicates how NULL values should be handled when they are
    encountered during ordering:

        from sqlalchemy import desc, nullsfirst

        stmt = select([users_table]).\
                    order_by(nullsfirst(desc(users_table.c.name)))

    上面的SQL表达式类似于：

        SELECT id, name FROM user ORDER BY name DESC NULLS FIRST

    Like [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")
    and [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc"),
    [`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")
    is typically invoked from the column expression itself using
    [`ColumnElement.nullsfirst()`](#sqlalchemy.sql.expression.ColumnElement.nullsfirst "sqlalchemy.sql.expression.ColumnElement.nullsfirst"),
    rather than as its standalone function version, as in:

        stmt = (select([users_table]).
                order_by(users_table.c.name.desc().nullsfirst())
                )

    也可以看看

    [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")

    [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")

    [`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")

    [`Select.order_by()`](selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")

` sqlalchemy.sql.expression。 T0>  nullslast  T1> （ T2> 列 T3> ） T4> ¶< / T5>`{.descclassname}
:   为`ORDER BY  t3生成NULLS LAST` \>表达。

    [`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")
    is intended to modify the expression produced by [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")
    or [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc"),
    and indicates how NULL values should be handled when they are
    encountered during ordering:

        from sqlalchemy import desc, nullslast

        stmt = select([users_table]).\
                    order_by(nullslast(desc(users_table.c.name)))

    上面的SQL表达式类似于：

        SELECT id, name FROM user ORDER BY name DESC NULLS LAST

    Like [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")
    and [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc"),
    [`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")
    is typically invoked from the column expression itself using
    [`ColumnElement.nullslast()`](#sqlalchemy.sql.expression.ColumnElement.nullslast "sqlalchemy.sql.expression.ColumnElement.nullslast"),
    rather than as its standalone function version, as in:

        stmt = select([users_table]).\
                    order_by(users_table.c.name.desc().nullslast())

    也可以看看

    [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")

    [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")

    [`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")

    [`Select.order_by()`](selectable.html#sqlalchemy.sql.expression.Select.order_by "sqlalchemy.sql.expression.Select.order_by")

` sqlalchemy.sql.expression。 T0> 或_  T1> （ T2>  *条款 T3> ） T4> ¶  T5>`{.descclassname}
:   生成由`OR`连接的表达式的连接。

    例如。：

        from sqlalchemy import or_

        stmt = select([users_table]).where(
                        or_(
                            users_table.c.name == 'wendy',
                            users_table.c.name == 'jack'
                        )
                    )

    使用Python `|`运算符也可以使用[`or_()`](#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")连接符（尽管注意复合表达式需要用括号括起来才能用Python运算符优先级行为来运行）：

        stmt = select([users_table]).where(
                        (users_table.c.name == 'wendy') |
                        (users_table.c.name == 'jack')
                    )

    也可以看看

    [`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")

 `sqlalchemy.sql.expression.`{.descclassname}`outparam`{.descname}(*key*, *type\_=None*)[¶](#sqlalchemy.sql.expression.outparam "Permalink to this definition")
:   创建一个'OUT'参数用于函数（存储过程），用于支持它们的数据库。

    `outparam`可以像常规函数参数一样使用。“output”值将通过其`out_parameters`属性从[`ResultProxy`](connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")对象中提供，该属性返回包含这些值的字典。

 `sqlalchemy.sql.expression.`{.descclassname}`over`{.descname}(*element*, *partition\_by=None*, *order\_by=None*, *range\_=None*, *rows=None*)[¶](#sqlalchemy.sql.expression.over "Permalink to this definition")
:   针对函数生成[`Over`](#sqlalchemy.sql.expression.Over "sqlalchemy.sql.expression.Over")对象。

    针对聚合或所谓的“窗口”函数，用于支持窗口函数的数据库后端。

    [`over()`](#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")
    is usually called using the [`FunctionElement.over()`](functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over")
    method, e.g.:

        func.row_number().over(order_by=mytable.c.some_column)

    会产生：

        ROW_NUMBER() OVER(ORDER BY some_column)

    范围也可以使用[`expression.over.range_`](#sqlalchemy.sql.expression.over.params.range_ "sqlalchemy.sql.expression.over")和[`expression.over.rows`](#sqlalchemy.sql.expression.over.params.rows "sqlalchemy.sql.expression.over")参数。这些互斥参数都接受一个2元组，它包含整数和None的组合：

        func.row_number().over(order_by=my_table.c.some_column, range_=(None, 0))

    以上将产生：

        ROW_NUMBER() OVER(ORDER BY some_column RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

    值None表示“无界限”，值为零表示“当前行”，负/正整数表示“之前”和“跟随”：

    -   5个上一个和下列10个之间的范围：

            func.row_number().over(order_by='x', range_=(-5, 10))

    -   无界上行和当前行之间的行数：

            func.row_number().over(order_by='x', rows=(None, 0))

    -   2个前置和未定界之间的范围如下：

            func.row_number().over(order_by='x', range_=(-2, None))

    版本1.1中的新功能：支持窗口内的RANGE / ROWS

    参数：

    -   **element**[¶](#sqlalchemy.sql.expression.over.params.element) –
        a [`FunctionElement`](functions.html#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement"),
        [`WithinGroup`](#sqlalchemy.sql.expression.WithinGroup "sqlalchemy.sql.expression.WithinGroup"),
        or other compatible construct.
    -   **partition\_by**[¶](#sqlalchemy.sql.expression.over.params.partition_by)
        – a column element or string, or a list of such, that will be
        used as the PARTITION BY clause of the OVER construct.
    -   **order\_by**[¶](#sqlalchemy.sql.expression.over.params.order_by)
        – a column element or string, or a list of such, that will be
        used as the ORDER BY clause of the OVER construct.
    -   **范围\_** [¶](#sqlalchemy.sql.expression.over.params.range_) -

        窗口的可选范围子句。这是一个元组值，它可以包含整数值或无，并将呈现一个RANGE
        BETWEEN PRECEDING / FOLLOWING子句

        版本1.1中的新功能

    -   **行** [¶](#sqlalchemy.sql.expression.over.params.rows) -

        窗口的可选行子句。这是一个元组值，可以包含整数值或无，并将呈现ROWS
        BETWEEN PRECEDING / FOLLOWING子句。

        版本1.1中的新功能

    该函数也可以通过[`FunctionElement.over()`](functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over")方法从[`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")构造本身使用。

    也可以看看

    [`expression.func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    [`expression.within_group()`](#sqlalchemy.sql.expression.within_group "sqlalchemy.sql.expression.within_group")

 `sqlalchemy.sql.expression.`{.descclassname}`text`{.descname}(*text*, *bind=None*, *bindparams=None*, *typemap=None*, *autocommit=None*)[¶](#sqlalchemy.sql.expression.text "Permalink to this definition")
:   构造一个新的[`TextClause`](#sqlalchemy.sql.expression.TextClause "sqlalchemy.sql.expression.TextClause")子句，直接表示文本SQL字符串。

    例如。：

        from sqlalchemy import text

        t = text("SELECT * FROM users")
        result = connection.execute(t)

    通过纯字符串提供的优点[`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")提供了对绑定参数，每个语句执行选项以及绑定参数和结果列的键入行为的后端中立支持，允许使用SQLAlchemy类型构造执行按字面指定的语句时的角色。该构造还可以提供一个`.c`列元素集合，允许将其作为子查询嵌入到其他SQL表达式结构中。

    绑定参数由名称指定，格式为`:name`。例如。：

        t = text("SELECT * FROM users WHERE id=:user_id")
        result = connection.execute(t, user_id=12)

    对于需要逐字逐句冒号的SQL语句，如在内联字符串中，使用反斜杠进行转义：

        t = text("SELECT * FROM users WHERE name='\:username'")

    [`TextClause`](#sqlalchemy.sql.expression.TextClause "sqlalchemy.sql.expression.TextClause")结构包含的方法可以提供有关绑定参数的信息，以及从文本语句中返回的列值（假设它是可执行的SELECT类型的语句）。[`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")方法用于提供绑定参数的详细信息，并且[`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法允许指定返回列，包括名称和类型：

        t = text("SELECT * FROM users WHERE id=:user_id").\
                bindparams(user_id=7).\
                columns(id=Integer, name=String)

        for id, name in connection.execute(t):
            print(id, name)

    当文本字符串SQL片段被指定为较大查询的一部分时（例如SELECT语句的WHERE子句），将使用[`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构：

        s = select([users.c.id, users.c.name]).where(text("id=:user_id"))
        result = connection.execute(s, user_id=12)

    [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")也用于使用纯文本构造完整的独立语句。因此，SQLAlchemy将其引用为[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")对象，并支持[`Executable.execution_options()`](selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")方法。例如，可以使用[`Connection.execution_options.autocommit`](connections.html#sqlalchemy.engine.Connection.execution_options.params.autocommit "sqlalchemy.engine.Connection.execution_options")选项显式设置应该服从“autocommit”的[`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构：

        t = text("EXEC my_procedural_thing()").\
                execution_options(autocommit=True)

    Note that SQLAlchemy’s usual “autocommit” behavior applies to
    [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    constructs implicitly - that is, statements which begin with a
    phrase such as `INSERT`, `UPDATE`, `DELETE`, or a variety of other
    phrases specific to certain backends, will be eligible for
    autocommit if no transaction is in progress.

    参数：

    -   **text** [¶](#sqlalchemy.sql.expression.text.params.text) -
        要创建的SQL语句的文本。使用`:<param>`指定绑定参数；它们将被编译为其引擎特定的格式。
    -   **autocommit**
        [¶](#sqlalchemy.sql.expression.text.params.autocommit) -
        弃用。Use .execution\_options(autocommit=) to set the autocommit
        option.
    -   **bind**[¶](#sqlalchemy.sql.expression.text.params.bind) – an
        optional connection or engine to be used for this text query.
    -   **bindparams**
        [¶](#sqlalchemy.sql.expression.text.params.bindparams) -

        已过时。[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")实例的列表，用于提供有关嵌入语句中的参数的信息。该参数现在在返回之前调用构造上的[`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")方法。例如。：

            stmt = text("SELECT * FROM table WHERE id=:id",
                      bindparams=[bindparam('id', value=5, type_=Integer)])

        相当于：

            stmt = text("SELECT * FROM table WHERE id=:id").\
                      bindparams(bindparam('id', value=5, type_=Integer))

        Deprecated since version 0.9.0: the
        [`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")
        method supersedes the `bindparams` argument
        to [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text").

    -   **typemap** [¶](#sqlalchemy.sql.expression.text.params.typemap)
        -

        已过时。一个字典，它将`SELECT`语句的columns子句中表示的列的名称映射到类型对象，这些对象将用于对结果集中的列执行后处理。此参数现在调用[`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法，该方法返回一个获取`.c`集合的[`TextAsFrom`](selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")结构，并且可以嵌入其他表达式。例如。：

            stmt = text("SELECT * FROM table",
                          typemap={'id': Integer, 'name': String},
                      )

        相当于：

            stmt = text("SELECT * FROM table").columns(id=Integer,
                                                       name=String)

        或者：

            from sqlalchemy.sql import column
            stmt = text("SELECT * FROM table").columns(
                                  column('id', Integer),
                                  column('name', String)
                              )

        Deprecated since version 0.9.0: the
        [`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
        method supersedes the `typemap` argument to
        [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text").

    也可以看看

    [Using Textual SQL](tutorial.html#sqlexpression-text) - 在Core教程中

    [Using Textual SQL](orm_tutorial.html#orm-tutorial-literal-sql) - in
    the ORM tutorial

` sqlalchemy.sql.expression。 T0> 真 T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   返回一个常量[`True_`](#sqlalchemy.sql.elements.True_ "sqlalchemy.sql.elements.True_")结构。

    例如。：

        >>> from sqlalchemy import true
        >>> print select([t.c.x]).where(true())
        SELECT x FROM t WHERE true

    不支持真/假常量的后端将呈现为针对1或0的表达式：

        >>> print select([t.c.x]).where(true())
        SELECT x FROM t WHERE 1 = 1

    The [`true()`](#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
    and [`false()`](#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")
    constants also feature “short circuit” operation within an
    [`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
    or [`or_()`](#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")
    conjunction:

        >>> print select([t.c.x]).where(or_(t.c.x > 5, true()))
        SELECT x FROM t WHERE true

        >>> print select([t.c.x]).where(and_(t.c.x > 5, false()))
        SELECT x FROM t WHERE false

    在版本0.9中更改： [`true()`](#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")和[`false()`](#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")具有在不支持真/假的连接词和方言中更好的集成行为常量。

    也可以看看

    [`false()`](#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")

 `sqlalchemy.sql.expression.`{.descclassname}`tuple_`{.descname}(*\*clauses*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.tuple_ "Permalink to this definition")
:   返回一个[`Tuple`](#sqlalchemy.sql.expression.Tuple "sqlalchemy.sql.expression.Tuple")。

    主要用途是生成一个复合IN构造：

        from sqlalchemy import tuple_

        tuple_(table.c.col1, table.c.col2).in_(
            [(1, 2), (5, 12), (10, 19)]
        )

    警告

    所有后端都不支持组合IN构造，目前已知可在Postgresql和MySQL上使用，但不支持SQLite。当这种表达式被调用时，不支持的后端会引发[`DBAPIError`](exceptions.html#sqlalchemy.exc.DBAPIError "sqlalchemy.exc.DBAPIError")的子类。

`sqlalchemy.sql.expression。`{.descclassname} `type_coerce`{.descname} （ *表达式*，*类型\_* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.type_coerce "Permalink to this definition")
:   将SQL表达式与特定类型关联，而不呈现`CAST`。

    例如。：

        from sqlalchemy import type_coerce

        stmt = select([
            type_coerce(log_table.date_string, StringDateTime())
        ])

    上面的结构将产生一个[`TypeCoerce`](#sqlalchemy.sql.expression.TypeCoerce "sqlalchemy.sql.expression.TypeCoerce")对象，该对象呈现给表达式添加标签的SQL，但是不会修改它在SQL端的值：

        SELECT date_string AS anon_1 FROM log

    当结果行被提取时，`StringDateTime`类型将代表`date_string`列应用于结果行。“anon\_1”标签的基本原理是，类型强制列在结果列的列表中与目标列的其他强制类型或直接值保持分离。为了为表达式提供一个命名标签，使用[`ColumnElement.label()`](#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label")：

        stmt = select([
            type_coerce(
                log_table.date_string, StringDateTime()).label('date')
        ])

    当文字值或[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构作为目标传递给[`type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")时，具有绑定值处理功能的类型也会生效。例如，如果一个类型实现[`TypeEngine.bind_expression()`](type_api.html#sqlalchemy.types.TypeEngine.bind_expression "sqlalchemy.types.TypeEngine.bind_expression")方法或[`TypeEngine.bind_processor()`](type_api.html#sqlalchemy.types.TypeEngine.bind_processor "sqlalchemy.types.TypeEngine.bind_processor")方法或同等方法，则这些函数将在语句编译/执行时生效一个文字值被传递，如下所示：

        # bound-value handling of MyStringType will be applied to the
        # literal value "some string"
        stmt = select([type_coerce("some string", MyStringType)])

    [`type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")类似于[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")函数，只是它不会在结果语句中呈现`CAST`表达式。

    参数：

    -   **expression**[¶](#sqlalchemy.sql.expression.type_coerce.params.expression)
        – A SQL expression, such as a [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
        expression or a Python string which will be coerced into a bound
        literal value.
    -   **type\_**[¶](#sqlalchemy.sql.expression.type_coerce.params.type_)
        – A [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        class or instance indicating the type to which the expression is
        coerced.

    也可以看看

    [`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")

 `sqlalchemy.sql.expression.`{.descclassname}`within_group`{.descname}(*element*, *\*order\_by*)[¶](#sqlalchemy.sql.expression.within_group "Permalink to this definition")
:   根据函数生成一个[`WithinGroup`](#sqlalchemy.sql.expression.WithinGroup "sqlalchemy.sql.expression.WithinGroup")对象。

    针对所谓的“有序集合”和“假设集合”功能，包括[`percentile_cont`](functions.html#sqlalchemy.sql.functions.percentile_cont "sqlalchemy.sql.functions.percentile_cont")，[`rank`](functions.html#sqlalchemy.sql.functions.rank "sqlalchemy.sql.functions.rank")，[`dense_rank`](functions.html#sqlalchemy.sql.functions.dense_rank "sqlalchemy.sql.functions.dense_rank")等。

    [`within_group()`](#sqlalchemy.sql.expression.within_group "sqlalchemy.sql.expression.within_group")
    is usually called using the [`FunctionElement.within_group()`](functions.html#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")
    method, e.g.:

        from sqlalchemy import within_group
        stmt = select([
            department.c.id,
            func.percentile_cont(0.5).within_group(
                department.c.salary.desc()
            )
        ])

    The above statement would produce SQL similar to
    `SELECT department.id, percentile_cont(0.5) WITHIN GROUP (ORDER BY department.salary DESC)`.

    参数：

    -   **element**[¶](#sqlalchemy.sql.expression.within_group.params.element)
        – a [`FunctionElement`](functions.html#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")
        construct, typically generated by [`func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func").
    -   **\*order\_by**[¶](#sqlalchemy.sql.expression.within_group.params.*order_by)
        – one or more column elements that will be used as the ORDER BY
        clause of the WITHIN GROUP construct.

    版本1.1中的新功能

    也可以看看

    [`expression.func`](#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")

    [`expression.over()`](#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")

 *class*`sqlalchemy.sql.expression.`{.descclassname}`BinaryExpression`{.descname}(*left*, *right*, *operator*, *type\_=None*, *negate=None*, *modifiers=None*)[¶](#sqlalchemy.sql.expression.BinaryExpression "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个`LEFT ＆lt；运算符＆gt； RIGHT`的表达式。

    每当在Python二进制表达式中使用两个列表达式时，会自动生成[`BinaryExpression`](#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")：

        >>> from sqlalchemy.sql import column
        >>> column('a') + column('b')
        <sqlalchemy.sql.expression.BinaryExpression object at 0x101029dd0>
        >>> print column('a') + column('b')
        a + b

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.BinaryExpression.compare "Permalink to this definition")
    :   根据给定的[`BinaryExpression`](#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")比较这个[`BinaryExpression`](#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")。

*class* `sqlalchemy.sql.expression。`{.descclassname} `BindParameter`{.descname} （ *key*，*value =符号（'NO\_ARG'）*，*type\_ = None*，*unique = False*，*required =符号（'NO\_ARG'）* *quote = None*，*callable\_ = None*，*isoutparam = False*，*\_compared\_to\_operator = None*，*\_compared\_to\_type = None T13\> ） T14\> [¶ T15\>](#sqlalchemy.sql.expression.BindParameter "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    代表“绑定表达”。

    [`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
    is invoked explicitly using the [`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
    function, as in:

        from sqlalchemy import bindparam

        stmt = select([users_table]).\
                    where(users_table.c.name == bindparam('username'))

    关于如何使用[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")的详细讨论位于[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")处。

    也可以看看

    [`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")

    `__ init __`{.descname} （ *键*，*value =符号（'NO\_ARG'）*，*type\_ =无 t4 \>，*unique = False*，*required = symbol（'NO\_ARG'）*，*quote = None*，*callable\_ = None* ，*isoutparam = False*，*\_compared\_to\_operator = None*，*\_compared\_to\_type = None* ） [](#sqlalchemy.sql.expression.BindParameter.__init__ "Permalink to this definition")*
    :   构建一个新的[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.BindParameter.compare "Permalink to this definition")
    :   将这个[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")与给定的子句进行比较。

    ` effective_value  T0> ¶ T1>`{.descname}
    :   考虑是否设置了`callable`参数，返回此绑定参数的值。

        The `callable` value will be evaluated and
        returned if present, else `value`.

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Case`{.descname}(*whens*, *value=None*, *else\_=None*)[¶](#sqlalchemy.sql.expression.Case "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    代表一个`CASE`表达式。

    [`Case`](#sqlalchemy.sql.expression.Case "sqlalchemy.sql.expression.Case")是使用[`case()`](#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")工厂函数生成的，如下所示：

        from sqlalchemy import case

        stmt = select([users_table]).\
                    where(
                        case(
                            [
                                (users_table.c.name == 'wendy', 'W'),
                                (users_table.c.name == 'jack', 'J')
                            ],
                            else_='E'
                        )
                    )

    [`Case`](#sqlalchemy.sql.expression.Case "sqlalchemy.sql.expression.Case")用法的详细信息位于[`case()`](#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")处。

    也可以看看

    [`case()`](#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")

    `__ init__`{.descname} （ *whens*，*value = None*，*else\_ = None* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Case.__init__ "Permalink to this definition")
    :   构建一个新的[`Case`](#sqlalchemy.sql.expression.Case "sqlalchemy.sql.expression.Case")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`case()`](#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Cast`{.descname}(*expression*, *type\_*)[¶](#sqlalchemy.sql.expression.Cast "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个`CAST`表达式。

    [`Cast`](#sqlalchemy.sql.expression.Cast "sqlalchemy.sql.expression.Cast")是使用[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")工厂函数生成的，如下所示：

        from sqlalchemy import cast, Numeric

        stmt = select([
                    cast(product_table.c.unit_price, Numeric(10, 4))
                ])

    [`Cast`](#sqlalchemy.sql.expression.Cast "sqlalchemy.sql.expression.Cast")用法的详细信息位于[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")处。

    也可以看看

    [`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")

     `__init__`{.descname}(*expression*, *type\_*)[¶](#sqlalchemy.sql.expression.Cast.__init__ "Permalink to this definition")
    :   构建一个新的[`Cast`](#sqlalchemy.sql.expression.Cast "sqlalchemy.sql.expression.Cast")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")。

*class* `sqlalchemy.sql.expression。`{.descclassname} `ClauseElement`{.descname} [¶](#sqlalchemy.sql.expression.ClauseElement "Permalink to this definition")
:   基础：`sqlalchemy.sql.visitors.Visitable`

    以编程方式构造的SQL表达式的元素的基类。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.ClauseElement.compare "Permalink to this definition")
    :   将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.ClauseElement.compile "Permalink to this definition")
    :   编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.ClauseElement.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.ClauseElement.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.ClauseElement.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.ClauseElement.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.ClauseElement.compile.params.compile_kwargs)
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

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   返回这个[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的直接子元素。

        这用于访问遍历。

        \*\*
        kwargs可能包含更改返回的集合的标志，例如为了减少更大的遍历而返回项目的子集，或者从不同的上下文返回子项目（例如模式级集合而不是子句-水平）。

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.ClauseElement.params "Permalink to this definition")
    :   返回带有[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   对这个[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")方法仅返回self。

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.ClauseElement.unique_params "Permalink to this definition")
    :   返回带有[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`ClauseList`{.descname}(*\*clauses*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.ClauseList "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

    描述由操作员分隔的子句列表。

    默认情况下，以逗号分隔，例如列列表。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.ClauseList.compare "Permalink to this definition")
    :   将这个[`ClauseList`](#sqlalchemy.sql.expression.ClauseList "sqlalchemy.sql.expression.ClauseList")与给定的[`ClauseList`](#sqlalchemy.sql.expression.ClauseList "sqlalchemy.sql.expression.ClauseList")进行比较，包括所有子句项的比较。

*class* `sqlalchemy.sql.expression。`{.descclassname} `ColumnClause`{.descname} （ *text*，*type\_ =无*，*is\_literal = False*，*\_selectable =无* ） [¶](#sqlalchemy.sql.expression.ColumnClause "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.Immutable`，[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示来自任何文本字符串的列表达式。

    The [`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause"),
    a lightweight analogue to the [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    class, is typically invoked using the [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")
    function, as in:

        from sqlalchemy import column

        id, name = column("id"), column("name")
        stmt = select([id, name]).select_from("user")

    上面的语句会产生如下的SQL：

        SELECT id, name FROM user

    [`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")
    is the immediate superclass of the schema-specific [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object. 尽管[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")类具有与[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")完全相同的功能，但在行为需求仅限于简单的情况下，[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")类本身可以使用SQL表达式生成。该对象与模式级别的元数据或与[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")所执行的执行时间行为没有任何关联，因此从这个意义上来说是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的“轻量级”版本。

    有关[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")用法的详细信息位于[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")处。

    也可以看看

    [`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")

    [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

     `__init__`{.descname}(*text*, *type\_=None*, *is\_literal=False*, *\_selectable=None*)[¶](#sqlalchemy.sql.expression.ColumnClause.__init__ "Permalink to this definition")
    :   构建一个新的[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`ColumnCollection`{.descname}(*\*columns*)[¶](#sqlalchemy.sql.expression.ColumnCollection "Permalink to this definition")
:   基础：`sqlalchemy.util._collections.OrderedProperties`

    存储ColumnElement实例列表的有序字典。

    覆盖`__eq__()`方法以在相关列集之间生成SQL子句。

    `添加 T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   在此集合中添加一列。

        该列的关键属性将用作此字典的散列键。

    `替换 T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   将给定的列添加到此集合中，删除此列的未认证版本以及具有相同密钥的现有列。

        > 例如。：
        >
        >     t = Table('sometable', metadata, Column('col1', Integer))
        >     t.columns.replace(Column('col1', Integer, key='columnone'))
        >
        > 将从集合中删除原来的'col1'，并在名称'columnname'下添加新列。

        由schema.Column用于在表反射期间覆盖列。

*class* `sqlalchemy.sql.expression。`{.descclassname} `ColumnElement`{.descname} [¶](#sqlalchemy.sql.expression.ColumnElement "Permalink to this definition")
:   基础：[`sqlalchemy.sql.operators.ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")，[`sqlalchemy.sql.expression.ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

    表示适用于“列”子句，WHERE子句等的面向列的SQL表达式的声明。

    While the most familiar kind of [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    is the [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    object, [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    serves as the basis for any unit that may be present in a SQL
    expression, including the expressions themselves, SQL functions,
    bound parameters, literal expressions, keywords such as
    `NULL`, etc. [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    is the ultimate base class for all such elements.

    各种各样的SQLAlchemy
    Core函数在SQL表达式级别工作，并且打算接受[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")的实例作为参数。这些函数通常会记录他们接受“SQL表达式”作为参数。这对于SQLAlchemy来说意味着什么，通常是指一个输入，它既可以是一个[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象，也可以是一个可以被**强制**为一个的值。关于SQL表达式的大部分（但不是全部）SQLAlchemy核心函数遵循的强制规则如下所示：

    > -   a literal Python value, such as a string, integer or floating
    >     point value, boolean, datetime, `Decimal`
    >     object, or virtually any other Python object, will be coerced
    >     into a “literal bound value”. This generally means that a
    >     [`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
    >     will be produced featuring the given value embedded into the
    >     construct; the resulting [`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
    >     object is an instance of [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement").
    >     在SQLAlchemy特定于类型的转换器（例如，Python）之后，Python的值最终会在执行时作为`execute()`或`executemany()`方法的参数化参数发送给DBAPI。由任何关联的[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")对象提供的值）应用于该值。
    > -   任何特殊的对象值，通常是ORM级别的构造，它们具有称为`__clause_element__()`的方法。当一个未知类型的对象被传递给一个将参数强制为一个[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")表达式的函数时，Core表达式系统查找这个方法。`__clause_element__()`方法（如果存在）应该返回一个[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")实例。The
    >     primary use of `__clause_element__()`
    >     within SQLAlchemy is that of class-bound attributes on
    >     ORM-mapped classes; a `User` class which
    >     contains a mapped attribute named `.name`
    >     will have a method `User.name.__clause_element__()` which when invoked returns the [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    >     called `name` associated with the mapped
    >     table.
    > -   Python `None`值通常被解释为`NULL`，它在SQLAlchemy Core中生成[`null()`](#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")的实例。

    一个[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")提供了使用Python表达式生成新的[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的能力。This
    means that Python operators such as `==`,
    `!=` and `<` are overloaded
    to mimic SQL operations, and allow the instantiation of further
    [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    instances which are composed from other, more fundamental
    [`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    objects. 例如，可以将两个[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")对象与加法运算符`+`一起添加以产生[`BinaryExpression`](#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")。[`ColumnClause`](#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause")和[`BinaryExpression`](#sqlalchemy.sql.expression.BinaryExpression "sqlalchemy.sql.expression.BinaryExpression")都是[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")的子类：

        >>> from sqlalchemy.sql import column
        >>> column('a') + column('b')
        <sqlalchemy.sql.expression.BinaryExpression object at 0x101029dd0>
        >>> print column('a') + column('b')
        a + b

    也可以看看

    [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

    [`expression.column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")

    ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`__eq__()`](#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实施`==`运算符。

        在列上下文中，生成子句`a = b`。If the target
        is `None`, produces `a IS NULL`.

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

    ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__le__()`](#sqlalchemy.sql.operators.ColumnOperators.__le__ "sqlalchemy.sql.operators.ColumnOperators.__le__")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<=`运算符。

        在列上下文中，生成子句`a <= b`。

    ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__lt__()`](#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<`运算符。

        在列上下文中，生成子句`a  b`。

    ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__ne__()`](#sqlalchemy.sql.operators.ColumnOperators.__ne__ "sqlalchemy.sql.operators.ColumnOperators.__ne__")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`!=`运算符。

        在列上下文中，生成子句`a ！= b`。If the
        target is `None`, produces
        `a IS NOT NULL`.

    `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`all_()`](#sqlalchemy.sql.operators.ColumnOperators.all_ "sqlalchemy.sql.operators.ColumnOperators.all_")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`all_()`](#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

        版本1.1中的新功能

    ` anon_label  T0> ¶ T1>`{.descname}
    :   为此ColumnElement提供了一个常量“匿名标签”。

        这是一个label()表达式，它将在编译时被命名。每次调用anon\_label时都会返回相同的label()，以便表达式可以多次引用anon\_label，并在编译时生成相同的标签名称。

        编译器在编译时自动使用这个函数来表达已知为“未命名”的表达式，如二进制表达式和函数调用。

    `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`any_()`](#sqlalchemy.sql.operators.ColumnOperators.any_ "sqlalchemy.sql.operators.ColumnOperators.any_")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`any_()`](#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

        版本1.1中的新功能

    ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`asc()`](#sqlalchemy.sql.operators.ColumnOperators.asc "sqlalchemy.sql.operators.ColumnOperators.asc")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

    ` base_columns  T0> ¶ T1>`{.descname}
    :   

    `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
    :   *inherited from the* [`between()`](#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在()子句之间针对父对象生成[`between()`](#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

    `绑定`{.descname} *=无* [¶](#sqlalchemy.sql.expression.ColumnElement.bind "Permalink to this definition")
    :   

    `铸造 T0> （ T1> 类型_  T2> ） T3> ¶ T4>`{.descname}
    :   制作一个类型演员，即`CAST（＆lt； expression＆gt； AS ＆lt； type＆gt；）`。

        这是[`cast()`](#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")函数的快捷方式。

        版本1.0.7中的新功能

    `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`collate()`](#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        根据给定的排序字符串，针对父对象生成一个[`collate()`](#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

    `比较 T0> ¶ T1>`{.descname}
    :   

     `compare`{.descname}(*other*, *use\_proxies=False*, *equivalents=None*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.ColumnElement.compare "Permalink to this definition")
    :   将此ColumnElement与另一个进行比较。

        特别理由：

        参数：

        -   **use\_proxies**[¶](#sqlalchemy.sql.expression.ColumnElement.compare.params.use_proxies)
            – when True, consider two columns that share a common base
            column as equivalent (i.e. shares\_lineage())
        -   **equivalents**[¶](#sqlalchemy.sql.expression.ColumnElement.compare.params.equivalents)
            – a dictionary of columns as keys mapped to sets of columns.
            如果此字典中存在给定的“其他”列，则相应set()中的任何列都会通过比较测试，结果为True。这用于将比较扩展到可能通过外键或其他标准已知等效于此的其他列。

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.ColumnElement.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.ColumnElement.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.ColumnElement.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.ColumnElement.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.ColumnElement.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.ColumnElement.compile.params.compile_kwargs)
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
    :   *继承自* [`concat()`](#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现'concat'操作符。

        在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

    `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.sql.expression.ColumnElement.contains "Permalink to this definition") \>
    :   *inherited from the* [`contains()`](#sqlalchemy.sql.operators.ColumnOperators.contains "sqlalchemy.sql.operators.ColumnOperators.contains")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'包含'运算符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；％'`

    `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`desc()`](#sqlalchemy.sql.operators.ColumnOperators.desc "sqlalchemy.sql.operators.ColumnOperators.desc")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

    `说明`{.descname} *=无* [¶](#sqlalchemy.sql.expression.ColumnElement.description "Permalink to this definition")
    :   

    `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`distinct()`](#sqlalchemy.sql.operators.ColumnOperators.distinct "sqlalchemy.sql.operators.ColumnOperators.distinct")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成一个[`distinct()`](#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

    `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.expression.ColumnElement.endswith "Permalink to this definition")
    :   *inherited from the* [`endswith()`](#sqlalchemy.sql.operators.ColumnOperators.endswith "sqlalchemy.sql.operators.ColumnOperators.endswith")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'endswith'操作符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

    `表达 T0> ¶ T1>`{.descname}
    :   返回一个列表达式。

        检查界面的一部分；回报自我。

    `foreign_keys`{.descname} *= []* [¶](#sqlalchemy.sql.expression.ColumnElement.foreign_keys "Permalink to this definition")
    :   

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](#sqlalchemy.sql.expression.ClauseElement.get_children "sqlalchemy.sql.expression.ClauseElement.get_children")
        *method of* [`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回这个[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的直接子元素。

        这用于访问遍历。

        \*\*
        kwargs可能包含更改返回的集合的标志，例如为了减少更大的遍历而返回项目的子集，或者从不同的上下文返回子项目（例如模式级集合而不是子句-水平）。

    `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.sql.expression.ColumnElement.ilike "Permalink to this definition")
    :   *inherited from the* [`ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`ilike`运算符。

        在列上下文中，生成子句`a ILIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.ilike("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.sql.expression.ColumnElement.ilike.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.sql.expression.ColumnElement.ilike.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.ilike("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`in_()`](#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在运算符中实现`in`

        在列上下文中，生成子句`a IN 其他`。“other”可以是列表达式的元组/列表，或者是[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

    `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`is_()`](#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS`运算符。

        通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.isnot()`](#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

    `is_clause_element`{.descname} *= True* [¶](#sqlalchemy.sql.expression.ColumnElement.is_clause_element "Permalink to this definition")
    :   

    ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_distinct_from()`](#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
        *方法 tt\> [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS DISTINCT FROM`运算符。

        在大多数平台上呈现“一个IS DISTINCT FROM
        b”；在一些如SQLite可能会呈现“一个不是b”。

        版本1.1中的新功能

    `is_selectable`{.descname} *= False* [¶](#sqlalchemy.sql.expression.ColumnElement.is_selectable "Permalink to this definition")
    :   

    ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`isnot()`](#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS NOT`运算符。

        Normally, `IS NOT` is generated
        automatically when comparing to a value of `None`, which resolves to `NULL`.
        但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.is_()`](#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

    ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`isnot_distinct_from()`](#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS NOT DISTINCT FROM`运算符。

        在大多数平台上呈现“不是从BIND DISTINCT FROM
        b”；在某些例如SQLite上可能会呈现“a IS b”。

        版本1.1中的新功能

    `键`{.descname} *=无* [¶](#sqlalchemy.sql.expression.ColumnElement.key "Permalink to this definition")
    :   在某些情况下在Python命名空间中引用该对象的'关键'。

        这典型地指的是存在于可选择的例如`.c`集合中的列的“关键字”。 sometable.c
        [“somekey”]会返回一个带有“somekey”.key的Column。

    `标签 T0> （ T1> 名称 T2> ） T3> ¶ T4>`{.descname}
    :   生成列标签，即`＆lt； columnname＆gt； AS ＆lt； name＆gt；`。

        这是[`label()`](#sqlalchemy.sql.expression.label "sqlalchemy.sql.expression.label")函数的快捷方式。

        如果'名称'是None，则会生成一个匿名标签名称。

    `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.sql.expression.ColumnElement.like "Permalink to this definition")
    :   *inherited from the* [`like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        像运算符一样实现`like`

        在列上下文中，生成子句`a LIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.like("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.sql.expression.ColumnElement.like.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.sql.expression.ColumnElement.like.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.like("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.expression.ColumnElement.match "Permalink to this definition")
    :   *继承自* [`match()`](#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        *方法 tt\> [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现数据库特定的“匹配”运算符。

        [`match()`](#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        attempts to resolve to a MATCH-like function or operator
        provided by the backend. 例子包括：

        -   Postgresql - 呈现`x @@ to_tsquery（y）`
        -   MySQL - renders
            `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
        -   Oracle - 呈现`CONTAINS（x， y）`
        -   其他后端可能会提供特殊的实现。
        -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

     `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.sql.expression.ColumnElement.notilike "Permalink to this definition")
    :   *inherited from the* [`notilike()`](#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT ILIKE`运算符。

        这相当于对[`ColumnOperators.ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`notin_()`](#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
        *方法 [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        执行`NOT IN`运算符。

        这相当于对[`ColumnOperators.in_()`](#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.in_()`](#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

    `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.sql.expression.ColumnElement.notlike "Permalink to this definition")
    :   *inherited from the* [`notlike()`](#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT LIKE`运算符。

        这相当于对[`ColumnOperators.like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`nullsfirst()`](#sqlalchemy.sql.operators.ColumnOperators.nullsfirst "sqlalchemy.sql.operators.ColumnOperators.nullsfirst")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

    ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`nullslast()`](#sqlalchemy.sql.operators.ColumnOperators.nullslast "sqlalchemy.sql.operators.ColumnOperators.nullslast")
        *[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

    `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.ColumnElement.op "Permalink to this definition")
    :   *继承自* [`op()`](#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
        *方法的[`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

        产生通用的操作员功能。

        例如。：

            somecolumn.op("*")(5)

        生产：

            somecolumn * 5

        该函数也可用于使按位运算符明确。例如：

            somecolumn.op('&')(0xff)

        是`somecolumn`中的值的按位与。

        参数：

        -   **operator**[¶](#sqlalchemy.sql.expression.ColumnElement.op.params.operator)
            – a string which will be output as the infix operator
            between this element and the expression passed to the
            generated function.
        -   **优先顺序**
            [¶](#sqlalchemy.sql.expression.ColumnElement.op.params.precedence)
            -

            当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

            New in version 0.8: - added the ‘precedence’ argument.

        -   **is\_comparison**
            [¶](#sqlalchemy.sql.expression.ColumnElement.op.params.is_comparison)
            -

            如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
            true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

            版本0.9.2新增： - 添加了[`Operators.op.is_comparison`](#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

        也可以看看

        [Redefining and Creating New
        Operators](custom_types.html#types-operators)

        [Using custom operators in join
        conditions](orm_join_conditions.html#relationship-custom-operator)中使用自定义运算符

    `操作 tt> （ op，*其他，** kwargs / T5> ¶ T6>`{.descname}
    :   

    `params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.ColumnElement.params "Permalink to this definition")
    :   *inherited from the* [`params()`](#sqlalchemy.sql.expression.ClauseElement.params "sqlalchemy.sql.expression.ClauseElement.params")
        *method of* [`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        返回此ClauseElement的一个副本，其中[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素替换为从给定字典中取得的值：

            >>> clause = column('x') + bindparam('foo')
            >>> print clause.compile().params
            {'foo':None}
            >>> print clause.params({'foo':7}).compile().params
            {'foo':7}

    `primary_key`{.descname} *= False* [¶](#sqlalchemy.sql.expression.ColumnElement.primary_key "Permalink to this definition")
    :   

    ` proxy_set  T0> ¶ T1>`{.descname}
    :   

    `reverse_operate`{.descname} （ *op*，*其他*，*\*\* kwargs* T5\> [¶ T6\>](#sqlalchemy.sql.expression.ColumnElement.reverse_operate "Permalink to this definition")
    :   

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   

    ` shares_lineage  T0> （ T1>  othercolumn  T2> ） T3> ¶ T4>`{.descname}
    :   如果给定的[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")与此[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")具有共同的祖先，则返回True。

    `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.sql.expression.ColumnElement.startswith "Permalink to this definition")
    :   *inherited from the* [`startswith()`](#sqlalchemy.sql.operators.ColumnOperators.startswith "sqlalchemy.sql.operators.ColumnOperators.startswith")
        *method of* [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`startwith`运算符。

        在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

    `supports_execution`{.descname} *= False* [¶](#sqlalchemy.sql.expression.ColumnElement.supports_execution "Permalink to this definition")
    :   

    `timetuple`{.descname} *=无* [¶](#sqlalchemy.sql.expression.ColumnElement.timetuple "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.ColumnElement.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

*class* `sqlalchemy.sql.operators。`{.descclassname} `ColumnOperators`{.descname} [¶](#sqlalchemy.sql.operators.ColumnOperators "Permalink to this definition")
:   基础：[`sqlalchemy.sql.operators.Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

    为[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")表达式定义布尔型，比较型和其他运算符。

    默认情况下，所有方法调用[`operate()`](#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")或[`reverse_operate()`](#sqlalchemy.sql.expression.ColumnElement.reverse_operate "sqlalchemy.sql.expression.ColumnElement.reverse_operate")，从Python内置`operator`模块传递相应的运算符函数或来自`sqlalchemy.expression.operators`的SQLAlchemy特定操作符函数。例如`__eq__`函数：

        def __eq__(self, other):
            return self.operate(operators.eq, other)

    其中`operators.eq`基本上是：

        def eq(a, b):
            return a == b

    核心列表达式单元[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")覆盖[`Operators.operate()`](#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")等等，以进一步返回[`ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")结构，以便`==`

    也可以看看：

    [Redefining and Creating New
    Operators](custom_types.html#types-operators)

    [`TypeEngine.comparator_factory`{](type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")

    [`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

    [`PropComparator`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

    ` __添加__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`+`运算符。

        在列上下文中，如果父对象具有非字符串亲和性，则会生成子句`a + b`。If the parent object has a string affinity, produces
        the concatenation operator, `a || b` - see
        [`ColumnOperators.concat()`](#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat").

    ` __和__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自 [`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")的*
        [`__and__()`](#sqlalchemy.sql.operators.Operators.__and__ "sqlalchemy.sql.operators.Operators.__and__")
        **

        实施`&`运算符。

        与SQL表达式一起使用时，会产生AND操作，等同于[`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")，即：

            a & b

        相当于：

            from sqlalchemy import and_
            and_(a, b)

        在使用`&`时应注意操作符的优先级；
        `&`运算符的优先级最高。如果操作数包含更多的子表达式，则应将其括在括号中：

            (a == 2) & (b == 4)

    ` __ delattr __  T0> ¶ T1>`{.descname}
    :   *继承自* `__delattr__`
        *属性* `object`

        x .\_\_ delattr \_\_（'name'）\<==\> del x.name

    ` __ DIV __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`/`运算符。

        在列上下文中，生成子句`a / b`。

    ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`==`运算符。

        在列上下文中，生成子句`a = b`。If the target
        is `None`, produces `a IS NULL`.

    ` __格式__  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* `__format__()`
        ** `object`

        默认对象格式化程序

    ` __ GE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`>=`运算符。

        在列上下文中，生成子句`a ＆gt； = b`。

    ` __的getAttribute __  T0> ¶ T1>`{.descname}
    :   *继承自* `__getattribute__` *属性* `object`

        x .\_\_ getattribute \_\_（'name'）\<==\> x.name

    ` __的GetItem __  T0> （ T1> 索引 T2> ） T3> ¶ T4>`{.descname}
    :   实现[]运算符。

        这可以被一些特定于数据库的类型使用，例如Postgresql
        ARRAY和HSTORE。

    ` __ GT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`>`运算符。

        在列上下文中，生成子句`a ＆gt； b`。

    ` __散列__  T0> ¶ T1>`{.descname}
    :   

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

    ` __反相__  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`__invert__()`](#sqlalchemy.sql.operators.Operators.__invert__ "sqlalchemy.sql.operators.Operators.__invert__")
        *method of* [`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

        实施`~`运算符。

        与SQL表达式一起使用时，结果为NOT操作，相当于[`not_()`](#sqlalchemy.sql.expression.not_ "sqlalchemy.sql.expression.not_")，即：

            ~a

        相当于：

            from sqlalchemy import not_
            not_(a)

    ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`<=`运算符。

        在列上下文中，生成子句`a <= b`。

    ` __ LSHIFT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   执行\<

        没有被SQLAlchemy核心使用，这是为想要使用\<

    ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`<`运算符。

        在列上下文中，生成子句`a  b`。

    ` __ MOD __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`%`运算符。

        在列上下文中，生成子句`a ％ b`。

    ` __ MUL __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`*`运算符。

        在列上下文中，生成子句`a * b`。

    ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`!=`运算符。

        在列上下文中，生成子句`a ！= b`。If the
        target is `None`, produces
        `a IS NOT NULL`.

    ` __ NEG __  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   实施`-`运算符。

        在列上下文中，生成子句`-a`。

     `__new__`{.descname}(*S*, *...*) → a new object with type S, a subtype of T[¶](#sqlalchemy.sql.operators.ColumnOperators.__new__ "Permalink to this definition")
    :   *inherited from the* `__new__()` *method of* `object`

    ` __或__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自 [`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")的*
        [`__or__()`](#sqlalchemy.sql.operators.Operators.__or__ "sqlalchemy.sql.operators.Operators.__or__")
        **

        实施`|`运算符。

        与SQL表达式一起使用时，会产生OR操作，等同于[`or_()`](#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")，即：

            a | b

        相当于：

            from sqlalchemy import or_
            or_(a, b)

        在使用`|`时应注意运营商的优先级；
        `|`运算符的优先级最高。如果操作数包含更多的子表达式，则应将其括在括号中：

            (a == 2) | (b == 4)

    ` __ RADD __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   反向实施`+`运算符。

        参见[`ColumnOperators.__add__()`](#sqlalchemy.sql.operators.ColumnOperators.__add__ "sqlalchemy.sql.operators.ColumnOperators.__add__")。

    ` __ RDIV __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   反向实施`/`运算符。

        请参阅[`ColumnOperators.__div__()`](#sqlalchemy.sql.operators.ColumnOperators.__div__ "sqlalchemy.sql.operators.ColumnOperators.__div__")。

    ` __减少__  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* `object`的
        `__reduce__()` *方法*

        腌菜的帮手

    ` __ reduce_ex __  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* `__reduce_ex__()` *method of* `object`

        腌菜的帮手

    ` __再版__  T0> ¶ T1>`{.descname}
    :   *继承自* `__repr__`
        *属性* `object`

    ` __ RMOD __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   反过来实施`%`运算符。

        参见[`ColumnOperators.__mod__()`](#sqlalchemy.sql.operators.ColumnOperators.__mod__ "sqlalchemy.sql.operators.ColumnOperators.__mod__")。

    ` __ RMUL __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   反向实施`*`运算符。

        参见[`ColumnOperators.__mul__()`](#sqlalchemy.sql.operators.ColumnOperators.__mul__ "sqlalchemy.sql.operators.ColumnOperators.__mul__")。

    ` __ RSHIFT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   执行\>\>操作符。

        SQLAlchemy核心不使用它，这是为想要使用\>\>作为扩展点的自定义操作系统提供的。

    ` __ RSUB __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   反过来实施`-`运算符。

        参见[`ColumnOperators.__sub__()`](#sqlalchemy.sql.operators.ColumnOperators.__sub__ "sqlalchemy.sql.operators.ColumnOperators.__sub__")。

    ` __ rtruediv __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   反向实施`//`运算符。

        参见[`ColumnOperators.__truediv__()`](#sqlalchemy.sql.operators.ColumnOperators.__truediv__ "sqlalchemy.sql.operators.ColumnOperators.__truediv__")。

    ` __ SETATTR __  T0> ¶ T1>`{.descname}
    :   *继承自* `__setattr__`
        *属性* `object`

        x .\_\_ setattr \_\_（'name'，value）\<==\> x.name = value

    `__ sizeof __`{.descname} （ ）→int [¶](#sqlalchemy.sql.operators.ColumnOperators.__sizeof__ "Permalink to this definition")
    :   *继承自 `object`的*
        `__sizeof__()` *方法*

        内存中对象的大小，以字节为单位

    ` __ STR __  T0> ¶ T1>`{.descname}
    :   *继承 `object`的*
        `__str__` *属性*

    ` __子__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`-`运算符。

        在列上下文中，生成子句`a  -  b`。

    ` __ subclasshook __  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* `__subclasshook__()` *方法* `object`

        抽象类可以覆盖它来自定义issubclass()。

        这是由abc.ABCMeta
        .\_\_子类检查\_\_()在早期调用的。它应该返回True，False或NotImplemented。如果它返回NotImplemented，则使用正常算法。否则，它会覆盖正常的算法（并且结果被缓存）。

    ` __ truediv __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`//`运算符。

        在列上下文中，生成子句`a / b`。

    `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成一个[`all_()`](#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

        版本1.1中的新功能

    `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成[`any_()`](#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

        版本1.1中的新功能

    ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成一个[`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

    `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
    :   在()子句之间针对父对象生成[`between()`](#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

    `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
    :   根据给定的排序字符串，针对父对象生成一个[`collate()`](#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

    `的concat  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现'concat'操作符。

        在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

    `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.sql.operators.ColumnOperators.contains "Permalink to this definition") \>
    :   实现'包含'运算符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；％'`

    `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成一个[`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

    `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成一个[`distinct()`](#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

    `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.operators.ColumnOperators.endswith "Permalink to this definition")
    :   实现'endswith'操作符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

    `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.sql.operators.ColumnOperators.ilike "Permalink to this definition")
    :   实现`ilike`运算符。

        在列上下文中，生成子句`a ILIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.ilike("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.ilike.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.ilike.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.ilike("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   在运算符中实现`in`

        在列上下文中，生成子句`a IN 其他`。“other”可以是列表达式的元组/列表，或者是[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

    `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`IS`运算符。

        通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.isnot()`](#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

    ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`IS DISTINCT FROM`运算符。

        在大多数平台上呈现“一个IS DISTINCT FROM
        b”；在一些如SQLite可能会呈现“一个不是b”。

        版本1.1中的新功能

    ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`IS NOT`运算符。

        Normally, `IS NOT` is generated
        automatically when comparing to a value of `None`, which resolves to `NULL`.
        但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.is_()`](#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

    ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实现`IS NOT DISTINCT FROM`运算符。

        在大多数平台上呈现“不是从BIND DISTINCT FROM
        b”；在某些例如SQLite上可能会呈现“a IS b”。

        版本1.1中的新功能

    `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.sql.operators.ColumnOperators.like "Permalink to this definition")
    :   像运算符一样实现`like`

        在列上下文中，生成子句`a LIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.like("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.like.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.like.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.like("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.sql.operators.ColumnOperators.match "Permalink to this definition")
    :   实现数据库特定的“匹配”运算符。

        [`match()`](#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        attempts to resolve to a MATCH-like function or operator
        provided by the backend. 例子包括：

        -   Postgresql - 呈现`x @@ to_tsquery（y）`
        -   MySQL - renders
            `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
        -   Oracle - 呈现`CONTAINS（x， y）`
        -   其他后端可能会提供特殊的实现。
        -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

     `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.sql.operators.ColumnOperators.notilike "Permalink to this definition")
    :   执行`NOT ILIKE`运算符。

        这相当于对[`ColumnOperators.ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.ilike()`](#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   执行`NOT IN`运算符。

        这相当于对[`ColumnOperators.in_()`](#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.in_()`](#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

    `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.sql.operators.ColumnOperators.notlike "Permalink to this definition")
    :   执行`NOT LIKE`运算符。

        这相当于对[`ColumnOperators.like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.like()`](#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成[`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

    ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   针对父对象生成一个[`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

    `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.operators.ColumnOperators.op "Permalink to this definition")
    :   *继承自* [`op()`](#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
        *方法的[`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

        产生通用的操作员功能。

        例如。：

            somecolumn.op("*")(5)

        生产：

            somecolumn * 5

        该函数也可用于使按位运算符明确。例如：

            somecolumn.op('&')(0xff)

        是`somecolumn`中的值的按位与。

        参数：

        -   **operator**[¶](#sqlalchemy.sql.operators.ColumnOperators.op.params.operator)
            – a string which will be output as the infix operator
            between this element and the expression passed to the
            generated function.
        -   **优先顺序**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.op.params.precedence)
            -

            当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

            New in version 0.8: - added the ‘precedence’ argument.

        -   **is\_comparison**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.op.params.is_comparison)
            -

            如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
            true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

            版本0.9.2新增： - 添加了[`Operators.op.is_comparison`](#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

        也可以看看

        [Redefining and Creating New
        Operators](custom_types.html#types-operators)

        [Using custom operators in join
        conditions](orm_join_conditions.html#relationship-custom-operator)中使用自定义运算符

    `操作 tt> （ op，*其他，** kwargs / T5> ¶ T6>`{.descname}
    :   *继承自* [`operate()`](#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")
        *方法* [`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

        操作一个参数。

        这是最低级别的操作，缺省情况下会引发`NotImplementedError`。

        在子类上覆盖它可以使普通行为适用于所有操作。例如，覆盖[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")将`func.lower()`应用于左侧和右侧：

            class MyComparator(ColumnOperators):
                def operate(self, op, other):
                    return op(func.lower(self), func.lower(other))

        参数：

        -   **op**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.operate.params.op)
            - 操作员可调用。
        -   **\*其他**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.operate.params.*other)
            -
            操作的“其他”一侧。对于大多数操作来说，这将是一个单一的标量。
        -   **\*\* kwargs**
            [¶](#sqlalchemy.sql.operators.ColumnOperators.operate.params.**kwargs)
            -
            修饰符。这些可以由特殊的操作符传递，如`ColumnOperators.contains()`。

    `reverse_operate`{.descname} （ *op*，*其他*，*\*\* kwargs* T5\> [¶ T6\>](#sqlalchemy.sql.operators.ColumnOperators.reverse_operate "Permalink to this definition")
    :   *inherited from the* [`reverse_operate()`](#sqlalchemy.sql.operators.Operators.reverse_operate "sqlalchemy.sql.operators.Operators.reverse_operate")
        *method of* [`Operators`](#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

        对参数进行反向操作。

        用法与`operate()`相同。

    `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.sql.operators.ColumnOperators.startswith "Permalink to this definition")
    :   实现`startwith`运算符。

        在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

    `timetuple`{.descname} *=无* [¶](#sqlalchemy.sql.operators.ColumnOperators.timetuple "Permalink to this definition")
    :   Hack，允许在LHS上比较日期时间对象。

*class* `sqlalchemy.sql.base。`{.descclassname} `DialectKWArgs`{.descname} [¶](#sqlalchemy.sql.base.DialectKWArgs "Permalink to this definition")
:   建立一个具有缺省和构造函数验证的特定方言参数的类的能力。

    The [`DialectKWArgs`](#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")
    interacts with the [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
    present on a dialect.

    也可以看看

    [`DefaultDialect.construct_arguments`{](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")

     *classmethod*`argument_for`{.descname}(*dialect\_name*, *argument\_name*, *default*)[¶](#sqlalchemy.sql.base.DialectKWArgs.argument_for "Permalink to this definition")
    :   为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.sql.base.DialectKWArgs.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.sql.base.DialectKWArgs.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.sql.base.DialectKWArgs.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` kwargs  T0> ¶ T1>`{.descname}
    :   [`DialectKWArgs.dialect_kwargs`](#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Extract`{.descname}(*field*, *expr*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.Extract "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个SQL EXTRACT子句，`提取（field FROM expr）`。

     `__init__`{.descname}(*field*, *expr*, *\*\*kwargs*)[¶](#sqlalchemy.sql.expression.Extract.__init__ "Permalink to this definition")
    :   构建一个新的[`Extract`](#sqlalchemy.sql.expression.Extract "sqlalchemy.sql.expression.Extract")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`extract()`](#sqlalchemy.sql.expression.extract "sqlalchemy.sql.expression.extract")。

*class* `sqlalchemy.sql.elements。`{.descclassname} `False _`{.descname} [¶](#sqlalchemy.sql.elements.False_ "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    在SQL语句中表示`false`关键字或等效项。

    [`False_`](#sqlalchemy.sql.elements.False_ "sqlalchemy.sql.elements.False_")通过[`false()`](#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")函数作为常量访问。

*class* `sqlalchemy.sql.expression。`{.descclassname} `FunctionFilter`{.descname} （ *func*，*\*标准 T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.expression.FunctionFilter "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个函数FILTER子句。

    这是一个针对聚集和窗口函数的特殊操作符，它控制将哪些行传递给它。它仅受特定数据库后端支持。

    通过[`FunctionElement.filter()`](functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")调用[`FunctionFilter`](#sqlalchemy.sql.expression.FunctionFilter "sqlalchemy.sql.expression.FunctionFilter")：

        func.count(1).filter(True)

    版本1.0.0中的新功能

    也可以看看

    [`FunctionElement.filter()`](functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")

     `__init__`{.descname}(*func*, *\*criterion*)[¶](#sqlalchemy.sql.expression.FunctionFilter.__init__ "Permalink to this definition")
    :   构造一个新的[`FunctionFilter`](#sqlalchemy.sql.expression.FunctionFilter "sqlalchemy.sql.expression.FunctionFilter")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`funcfilter()`](#sqlalchemy.sql.expression.funcfilter "sqlalchemy.sql.expression.funcfilter")。

    `过滤 T0> （ T1>  *标准 T2> ） T3> ¶ T4>`{.descname}
    :   针对该功能生成额外的FILTER。

        此方法将附加条件添加到由[`FunctionElement.filter()`](functions.html#sqlalchemy.sql.functions.FunctionElement.filter "sqlalchemy.sql.functions.FunctionElement.filter")设置的初始条件中。

        多个标准通过`AND`在SQL呈现时间连接在一起。

     `over`{.descname}(*partition\_by=None*, *order\_by=None*)[¶](#sqlalchemy.sql.expression.FunctionFilter.over "Permalink to this definition")
    :   针对此过滤功能产生一个OVER子句。

        针对聚合或所谓的“窗口”函数，用于支持窗口函数的数据库后端。

        表达方式：

            func.rank().filter(MyClass.y > 5).over(order_by='x')

        简写为：

            from sqlalchemy import over, funcfilter
            over(funcfilter(func.rank(), MyClass.y > 5), order_by='x')

        有关完整说明，请参见[`over()`](#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Label`{.descname}(*name*, *element*, *type\_=None*)[¶](#sqlalchemy.sql.expression.Label "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个列标签（AS）。

    使用`AS`
    sql关键字通常应用于任何列级元素来表示标签。

     `__init__`{.descname}(*name*, *element*, *type\_=None*)[¶](#sqlalchemy.sql.expression.Label.__init__ "Permalink to this definition")
    :   构建一个新的[`Label`](#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`label()`](#sqlalchemy.sql.expression.label "sqlalchemy.sql.expression.label")。

*class* `sqlalchemy.sql.elements。`{.descclassname} `空`{.descname} [¶](#sqlalchemy.sql.elements.Null "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    在SQL语句中表示NULL关键字。

    [`Null`](#sqlalchemy.sql.elements.Null "sqlalchemy.sql.elements.Null")通过[`null()`](#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")函数作为常量访问。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Over`{.descname}(*element*, *partition\_by=None*, *order\_by=None*, *range\_=None*, *rows=None*)[¶](#sqlalchemy.sql.expression.Over "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    代表OVER子句。

    这是一个针对所谓的“窗口”函数的特殊操作符，以及任何聚合函数，它会产生相对于结果集本身的结果。它仅受特定数据库后端支持。

     `__init__`{.descname}(*element*, *partition\_by=None*, *order\_by=None*, *range\_=None*, *rows=None*)[¶](#sqlalchemy.sql.expression.Over.__init__ "Permalink to this definition")
    :   构建一个新的[`Over`](#sqlalchemy.sql.expression.Over "sqlalchemy.sql.expression.Over")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`over()`](#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")。

    ` FUNC  T0> ¶ T1>`{.descname}
    :   由[`Over`](#sqlalchemy.sql.expression.Over "sqlalchemy.sql.expression.Over")子句引用的元素。

        从版本1.1开始弃用： `func`元素已被重命名为`.element`。虽然`.func`是只读的，但这两个属性是同义词。

*class* `sqlalchemy.sql.expression。`{.descclassname} `TextClause`{.descname} （ *text*，*=无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.expression.TextClause "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.expression.Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，[`sqlalchemy.sql.expression.ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

    表示一个文字SQL文本片段。

    例如。：

        from sqlalchemy import text

        t = text("SELECT * FROM users")
        result = connection.execute(t)

    [`Text`](type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")结构是使用[`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")函数生成的；请参阅该函数以获取完整文档。

    也可以看看

    [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")

    `bindparams`{.descname} （ *\* binds*，*\*\* names\_to\_values* ） [T5\>](#sqlalchemy.sql.expression.TextClause.bindparams "Permalink to this definition")
    :   在[`TextClause`](#sqlalchemy.sql.expression.TextClause "sqlalchemy.sql.expression.TextClause")结构中建立绑定参数的值和/或类型。

        给定一个文本构造如：

            from sqlalchemy import text
            stmt = text("SELECT id, name FROM user WHERE name=:name "
                        "AND timestamp=:timestamp")

        通过使用简单的关键字参数，可以使用[`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")方法建立`:name`和`:timestamp`的初始值：

            stmt = stmt.bindparams(name='jack',
                        timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5))

        Where above, new [`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
        objects will be generated with the names `name` and `timestamp`, and values of
        `jack` and
        `datetime.datetime(2012, 10, 8, 15, 12, 5)`,
        respectively.
        类型将根据给出的值推断，在这种情况下[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")和[`DateTime`](type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")。

        当需要特定的键入行为时，可以使用位置`*binds`参数来直接指定[`bindparam()`](#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构。这些结构必须至少包含`key`参数，然后是可选值和类型：

            from sqlalchemy import bindparam
            stmt = stmt.bindparams(
                            bindparam('name', value='jack', type_=String),
                            bindparam('timestamp', type_=DateTime)
                        )

        在上面，我们为`timestamp`绑定指定了[`DateTime`](type_basics.html#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")的类型，`name`绑定的[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")的类型。在`name`的情况下，我们还设置`"jack"`的默认值。

        额外的绑定参数可以在语句执行时提供，例如：

            result = connection.execute(stmt,
                        timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5))

        可以重复调用[`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")方法，在该方法中它将重新使用现有的[`BindParameter`](#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")对象添加新信息。例如，我们可以首先用键入信息来调用[`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")，然后再用值信息再次调用它，它将被合并：

            stmt = text("SELECT id, name FROM user WHERE name=:name "
                        "AND timestamp=:timestamp")
            stmt = stmt.bindparams(
                bindparam('name', type_=String),
                bindparam('timestamp', type_=DateTime)
            )
            stmt = stmt.bindparams(
                name='jack',
                timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5)
            )

        New in version 0.9.0: The [`TextClause.bindparams()`](#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")
        method supersedes the argument `bindparams`
        passed to [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text").

    `列`{.descname} （ *\* cols*，*\*\*类型* ） [T5\>](#sqlalchemy.sql.expression.TextClause.columns "Permalink to this definition")
    :   将此[`TextClause`](#sqlalchemy.sql.expression.TextClause "sqlalchemy.sql.expression.TextClause")对象转换为可以嵌入到另一个语句中的[`TextAsFrom`](selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")对象。

        这个函数基本上弥补了完全文本的SELECT语句和“可选择”的SQL表达式语言概念之间的差距：

            from sqlalchemy.sql import column, text

            stmt = text("SELECT id, name FROM some_table")
            stmt = stmt.columns(column('id'), column('name')).alias('st')

            stmt = select([mytable]).\
                    select_from(
                        mytable.join(stmt, mytable.c.name == stmt.c.name)
                    ).where(stmt.c.id > 5)

        上面，我们将一系列[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")元素在位置上传递给[`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法。这些[`column()`](#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")元素现在成为[`TextAsFrom.c`](selectable.html#sqlalchemy.sql.expression.TextAsFrom.c "sqlalchemy.sql.expression.TextAsFrom.c")列集合中的第一个类元素，就像任何其他可选元素一样。

        The column expressions we pass to [`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
        may also be typed; when we do so, these [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
        objects become the effective return type of the column, so that
        SQLAlchemy’s result-set-processing systems may be used on the
        return values.
        对于类型（如日期或布尔类型）以及某些方言配置上的unicode处理，通常需要这样做：

            stmt = text("SELECT id, name, timestamp FROM some_table")
            stmt = stmt.columns(
                        column('id', Integer),
                        column('name', Unicode),
                        column('timestamp', DateTime)
                    )

            for id, name, timestamp in connection.execute(stmt):
                print(id, name, timestamp)

        作为上述语法的捷径，如果仅需要进行类型转换，则可以使用仅引用类型的关键字参数：

            stmt = text("SELECT id, name, timestamp FROM some_table")
            stmt = stmt.columns(
                        id=Integer,
                        name=Unicode,
                        timestamp=DateTime
                    )

            for id, name, timestamp in connection.execute(stmt):
                print(id, name, timestamp)

        [`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")的位置形式还提供了**位置列定位**的独特功能，这在使用带有复杂文本查询的ORM时特别有用。如果我们将模型中的列指定为[`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")，则结果集将在位置上与这些列匹配，这意味着文本SQL中列的名称或来源无关紧要：

            stmt = text("SELECT users.id, addresses.id, users.id, "
                 "users.name, addresses.email_address AS email "
                 "FROM users JOIN addresses ON users.id=addresses.user_id "
                 "WHERE users.id = 1").columns(
                    User.id,
                    Address.id,
                    Address.user_id,
                    User.name,
                    Address.email_address
                 )

            query = session.query(User).from_statement(stmt).options(
                contains_eager(User.addresses))

        版本1.1中的新功能当纯粹在位置上传递列表达式时，[`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法现在可在结果集中提供位置列定位。

        [`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法提供了直接调用[`FromClause.alias()`](selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")以及`SelectBase.cte()` SELECT语句：

            stmt = stmt.columns(id=Integer, name=String).cte('st')

            stmt = select([sometable]).where(sometable.c.id == stmt.c.id)

        New in version 0.9.0: [`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
        can now be converted into a fully featured “selectable”
        construct using the [`TextClause.columns()`](#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
        method. 此方法取代[`text()`](#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")的`typemap`参数。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Tuple`{.descname}(*\*clauses*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.Tuple "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ClauseList`](#sqlalchemy.sql.expression.ClauseList "sqlalchemy.sql.expression.ClauseList")，[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个SQL元组。

    `__ init __`{.descname} （ *\*子句*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.Tuple.__init__ "Permalink to this definition")
    :   构建一个新的[`Tuple`](#sqlalchemy.sql.expression.Tuple "sqlalchemy.sql.expression.Tuple")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`tuple_()`](#sqlalchemy.sql.expression.tuple_ "sqlalchemy.sql.expression.tuple_")。

 *class*`sqlalchemy.sql.expression.`{.descclassname}`WithinGroup`{.descname}(*element*, *\*order\_by*)[¶](#sqlalchemy.sql.expression.WithinGroup "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    代表一个WITHIN GROUP（ORDER BY）子句。

    这是针对所谓的“有序集合”和“假设集合”函数的特殊运算符，包括`percentile_cont()`，`rank()`，`dense_rank()`等。

    它仅受特定数据库后端支持，如PostgreSQL，Oracle和MS SQL Server。

    [`WithinGroup`](#sqlalchemy.sql.expression.WithinGroup "sqlalchemy.sql.expression.WithinGroup")构造从方法[`FunctionElement.within_group_type()`](functions.html#sqlalchemy.sql.functions.FunctionElement.within_group_type "sqlalchemy.sql.functions.FunctionElement.within_group_type")中提取它的类型。如果返回`None`，则使用函数的`.type`。

    `__ init __`{.descname} （ *元素*，*\* order\_by* ） [](#sqlalchemy.sql.expression.WithinGroup.__init__ "Permalink to this definition")
    :   构建一个新的[`WithinGroup`](#sqlalchemy.sql.expression.WithinGroup "sqlalchemy.sql.expression.WithinGroup")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参见[`within_group()`](#sqlalchemy.sql.expression.within_group "sqlalchemy.sql.expression.within_group")。

     `over`{.descname}(*partition\_by=None*, *order\_by=None*)[¶](#sqlalchemy.sql.expression.WithinGroup.over "Permalink to this definition")
    :   根据[`WithinGroup`](#sqlalchemy.sql.expression.WithinGroup "sqlalchemy.sql.expression.WithinGroup")结构产生一个OVER子句。

        该函数具有与[`FunctionElement.over()`](functions.html#sqlalchemy.sql.functions.FunctionElement.over "sqlalchemy.sql.functions.FunctionElement.over")相同的签名。

*class* `sqlalchemy.sql.elements。`{.descclassname} `True _`{.descname} [¶](#sqlalchemy.sql.elements.True_ "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    在SQL语句中表示`true`关键字或等效项。

    [`True_`](#sqlalchemy.sql.elements.True_ "sqlalchemy.sql.elements.True_")
    is accessed as a constant via the [`true()`](#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
    function.

 *class*`sqlalchemy.sql.expression.`{.descclassname}`TypeCoerce`{.descname}(*expression*, *type\_*)[¶](#sqlalchemy.sql.expression.TypeCoerce "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    表示一个Python端的类型强制包装器。

    [`TypeCoerce`](#sqlalchemy.sql.expression.TypeCoerce "sqlalchemy.sql.expression.TypeCoerce")
    supplies the [`expression.type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")
    function; see that function for usage details.

    在版本1.1中更改： [`type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")函数现在生成一个持久化的[`TypeCoerce`](#sqlalchemy.sql.expression.TypeCoerce "sqlalchemy.sql.expression.TypeCoerce")包装器对象，而不是将给定的对象就地转换。

    也可以看看

    [`expression.type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")

     `__init__`{.descname}(*expression*, *type\_*)[¶](#sqlalchemy.sql.expression.TypeCoerce.__init__ "Permalink to this definition")
    :   构建一个新的[`TypeCoerce`](#sqlalchemy.sql.expression.TypeCoerce "sqlalchemy.sql.expression.TypeCoerce")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`type_coerce()`](#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")。

*class* `sqlalchemy.sql.operators。`{.descclassname} `custom_op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False*，*natural\_self\_precedent = False* ） [¶](#sqlalchemy.sql.operators.custom_op "Permalink to this definition")
:   代表一个'自定义'操作符。

    当使用[`ColumnOperators.op()`](#sqlalchemy.sql.operators.ColumnOperators.op "sqlalchemy.sql.operators.ColumnOperators.op")方法创建自定义操作符可调用时，[`custom_op`](#sqlalchemy.sql.operators.custom_op "sqlalchemy.sql.operators.custom_op")通常是即时创建的。当以编程方式构造表达式时，该类也可以直接使用。例如。代表“阶乘”操作：

        from sqlalchemy.sql import UnaryExpression
        from sqlalchemy.sql import operators
        from sqlalchemy import Numeric

        unary = UnaryExpression(table.c.somecolumn,
                modifier=operators.custom_op("!"),
                type_=Numeric)

*class* `sqlalchemy.sql.operators。`{.descclassname} `运算符`{.descname} [¶](#sqlalchemy.sql.operators.Operators "Permalink to this definition")
:   比较基础和逻辑运算符。

    Implements base methods [`operate()`](#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")
    and [`reverse_operate()`](#sqlalchemy.sql.operators.Operators.reverse_operate "sqlalchemy.sql.operators.Operators.reverse_operate"),
    as well as [`__and__()`](#sqlalchemy.sql.operators.Operators.__and__ "sqlalchemy.sql.operators.Operators.__and__"),
    [`__or__()`](#sqlalchemy.sql.operators.Operators.__or__ "sqlalchemy.sql.operators.Operators.__or__"),
    [`__invert__()`](#sqlalchemy.sql.operators.Operators.__invert__ "sqlalchemy.sql.operators.Operators.__invert__").

    通常通过其最常见的子类[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")使用。

    ` __和__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`&`运算符。

        与SQL表达式一起使用时，会产生AND操作，等同于[`and_()`](#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")，即：

            a & b

        相当于：

            from sqlalchemy import and_
            and_(a, b)

        在使用`&`时应注意操作符的优先级；
        `&`运算符的优先级最高。如果操作数包含更多的子表达式，则应将其括在括号中：

            (a == 2) & (b == 4)

    ` __反相__  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   实施`~`运算符。

        与SQL表达式一起使用时，结果为NOT操作，相当于[`not_()`](#sqlalchemy.sql.expression.not_ "sqlalchemy.sql.expression.not_")，即：

            ~a

        相当于：

            from sqlalchemy import not_
            not_(a)

    ` __或__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   实施`|`运算符。

        与SQL表达式一起使用时，会产生OR操作，等同于[`or_()`](#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")，即：

            a | b

        相当于：

            from sqlalchemy import or_
            or_(a, b)

        在使用`|`时应注意运营商的优先级；
        `|`运算符的优先级最高。如果操作数包含更多的子表达式，则应将其括在括号中：

            (a == 2) | (b == 4)

    `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.sql.operators.Operators.op "Permalink to this definition")
    :   产生通用的操作员功能。

        例如。：

            somecolumn.op("*")(5)

        生产：

            somecolumn * 5

        该函数也可用于使按位运算符明确。例如：

            somecolumn.op('&')(0xff)

        是`somecolumn`中的值的按位与。

        参数：

        -   **operator**[¶](#sqlalchemy.sql.operators.Operators.op.params.operator)
            – a string which will be output as the infix operator
            between this element and the expression passed to the
            generated function.
        -   **优先顺序**
            [¶](#sqlalchemy.sql.operators.Operators.op.params.precedence)
            -

            当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

            New in version 0.8: - added the ‘precedence’ argument.

        -   **is\_comparison**
            [¶](#sqlalchemy.sql.operators.Operators.op.params.is_comparison)
            -

            如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
            true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

            版本0.9.2新增： - 添加了[`Operators.op.is_comparison`](#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

        也可以看看

        [Redefining and Creating New
        Operators](custom_types.html#types-operators)

        [Using custom operators in join
        conditions](orm_join_conditions.html#relationship-custom-operator)中使用自定义运算符

    `操作 tt> （ op，*其他，** kwargs / T5> ¶ T6>`{.descname}
    :   操作一个参数。

        这是最低级别的操作，缺省情况下会引发`NotImplementedError`。

        在子类上覆盖它可以使普通行为适用于所有操作。例如，覆盖[`ColumnOperators`](#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")将`func.lower()`应用于左侧和右侧：

            class MyComparator(ColumnOperators):
                def operate(self, op, other):
                    return op(func.lower(self), func.lower(other))

        参数：

        -   **op**
            [¶](#sqlalchemy.sql.operators.Operators.operate.params.op) -
            操作员可调用。
        -   **\*其他**
            [¶](#sqlalchemy.sql.operators.Operators.operate.params.*other)
            -
            操作的“其他”一侧。对于大多数操作来说，这将是一个单一的标量。
        -   **\*\* kwargs**
            [¶](#sqlalchemy.sql.operators.Operators.operate.params.**kwargs)
            -
            修饰符。这些可以由特殊的操作符传递，如`ColumnOperators.contains()`。

    `reverse_operate`{.descname} （ *op*，*其他*，*\*\* kwargs* T5\> [¶ T6\>](#sqlalchemy.sql.operators.Operators.reverse_operate "Permalink to this definition")
    :   对参数进行反向操作。

        用法与`operate()`相同。

*class* `sqlalchemy.sql.elements。`{.descclassname} `quoted_name`{.descname} [¶](#sqlalchemy.sql.elements.quoted_name "Permalink to this definition")
:   基础：`sqlalchemy.util.langhelpers.MemoizedSlots`，`__builtin__.unicode`

    用一个引用首选项来表示一个SQL标识符。

    [`quoted_name`](#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")是一个Python
    unicode / str子类，它表示一个特定的标识符名称和一个`quote`标志。当设置为`True`或`False`时，`quote`标志会覆盖此标识符的自动引用行为，以便无条件引用或不引用名称。如果保留默认值`None`，则基于对令牌本身的检查，将引用行为应用于每个后端基础上的标识符。

    `quote=True`的[`quoted_name`](#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")对象也可以防止在所谓的“name
    normalize”选项中被修改。某些数据库后端（如Oracle，Firebird和DB2）将大小写不区分大小写的名称“归一化”。这些后端的SQLAlchemy方言可以从SQLAlchemy的小写方式不敏感约定转换为这些后端的大小写不敏感约定。这里的`quote=True`标志将阻止这种转换发生，以支持被标记为全部小写字母的标识符。

    指定[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")等关键架构结构的名称时，通常会自动创建[`quoted_name`](#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")对象。该类也可以显式作为名称传递给接收可引用名称的任何函数。如使用具有无条件引用名称的[`Engine.has_table()`](connections.html#sqlalchemy.engine.Engine.has_table "sqlalchemy.engine.Engine.has_table")方法：

        from sqlaclchemy import create_engine
        from sqlalchemy.sql.elements import quoted_name

        engine = create_engine("oracle+cx_oracle://some_dsn")
        engine.has_table(quoted_name("some_table", True))

    上述逻辑将针对Oracle后端运行“has
    table”逻辑，并将名称完全传递为`"some_table"`，而不会转换为大写。

    版本0.9.0中的新功能

*class* `sqlalchemy.sql.expression。`{.descclassname} `UnaryExpression`{.descname} （ *元素*，*运算符=无*，*修饰符=无*，*type\_ =无*，*negate =无*，*wraps\_column\_expression = False* ） T10\> [¶ T11\>](#sqlalchemy.sql.expression.UnaryExpression "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    定义一个“一元”表达式。

    一元表达式具有单列表达式和运算符。运算符可以放置在列表达式的左侧（称为“运算符”）或右侧（称为“修饰符”）。

    [`UnaryExpression`](#sqlalchemy.sql.expression.UnaryExpression "sqlalchemy.sql.expression.UnaryExpression")
    is the basis for several unary operators including those used by
    [`desc()`](#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc"),
    [`asc()`](#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc"),
    [`distinct()`](#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct"),
    [`nullsfirst()`](#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")
    and [`nullslast()`](#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast").

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.UnaryExpression.compare "Permalink to this definition")
    :   将此[`UnaryExpression`](#sqlalchemy.sql.expression.UnaryExpression "sqlalchemy.sql.expression.UnaryExpression")与给定的[`ClauseElement`](#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")进行比较。


