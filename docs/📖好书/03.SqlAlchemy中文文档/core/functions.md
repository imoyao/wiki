---
title: SQL 和通用函数
date: 2021-02-20 22:41:34
permalink: /sqlalchemy/core/functions/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
  - 
---
SQL和通用函数[¶](#module-sqlalchemy.sql.expression "Permalink to this headline")
================================================================================

SQLAlchemy 已知的关于数据库特定渲染，返回类型和参数行为的 SQL 函数。通用函数与所有 SQL 函数一样，使用[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")属性进行调用：

    select([func.count()]).select_from(sometable)

请注意，任何不为[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")所知的名称都会按原样生成函数名称
-
对 SQLAlchemy，内置或用户定义的 SQL 函数可以调用，已知或未知的 SQL 函数没有限制。这里的部分只描述了那些 SQLAlchemy 已经知道使用什么参数和返回类型的函数。

SQL 函数 API，工厂和内置函数。

*class* `sqlalchemy.sql.functions。`{.descclassname} `AnsiFunction`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.AnsiFunction "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    `标识符`{.descname} *='AnsiFunction'* [¶](#sqlalchemy.sql.functions.AnsiFunction.identifier "Permalink to this definition")
    :   

    `姓名`{.descname} *='AnsiFunction'* [¶](#sqlalchemy.sql.functions.AnsiFunction.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`Function`{.descname}(*name*, *\*clauses*, *\*\*kw*)[¶](#sqlalchemy.sql.functions.Function "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")

    描述一个命名的SQL函数。

    有关公共方法的描述，请参阅超类[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")。

    也可以看看

    [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")
    - 产生注册或临时[`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")实例的命名空间。

    [`GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")
    - allows creation of registered function types.

     `__init__`{.descname}(*name*, *\*clauses*, *\*\*kw*)[¶](#sqlalchemy.sql.functions.Function.__init__ "Permalink to this definition")
    :   构建一个[`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")。

        [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")结构通常用于构造新的[`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")实例。

 *class*`sqlalchemy.sql.functions.`{.descclassname}`FunctionElement`{.descname}(*\*clauses*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.FunctionElement "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，[`sqlalchemy.sql.expression.ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")，[`sqlalchemy.sql.expression.FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")

    基于SQL函数的构造。

    也可以看看

    [`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")
    - 名为SQL函数。

    [`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")
    - 产生注册或临时[`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")实例的命名空间。

    [`GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")
    - allows creation of registered function types.

    `__ init __`{.descname} （ *\*子句*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.functions.FunctionElement.__init__ "Permalink to this definition")
    :   构造一个[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")。

     `alias`{.descname}(*name=None*, *flat=False*)[¶](#sqlalchemy.sql.functions.FunctionElement.alias "Permalink to this definition")
    :   根据[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")生成[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")结构。

        这个构造将函数包装在一个适用于FROM子句的命名别名中，例如Postgresql接受的样式。

        例如。：

            from sqlalchemy.sql import column

            stmt = select([column('data_view')]).\
                select_from(SomeTable).\
                select_from(func.unnest(SomeTable.data).alias('data_view')
            )

        会产生：

            SELECT data_view
            FROM sometable, unnest(sometable.data) AS data_view

        版本0.9.8新增：现在支持[`FunctionElement.alias()`](#sqlalchemy.sql.functions.FunctionElement.alias "sqlalchemy.sql.functions.FunctionElement.alias")方法。以前，此方法的行为未定义，并且在各个版本中的行为不一致。

    `条款 T0> ¶ T1>`{.descname}
    :   返回包含此[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")参数的基础[`ClauseList`](sqlelement.html#sqlalchemy.sql.expression.ClauseList "sqlalchemy.sql.expression.ClauseList")。

    `列 T0> ¶ T1>`{.descname}
    :   由[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")导出的一组列。

        函数对象当前没有内置的结果列名称；此方法返回一个具有匿名名称列的单元素列集合。

        为函数提供命名列作为FROM子句的临时方法是使用所需的列构建[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")：

            from sqlalchemy.sql import column

            stmt = select([column('x'), column('y')]).                select_from(func.myfunction())

    `执行 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   对嵌入的“绑定”执行[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")。

        这首先调用[`select()`](#sqlalchemy.sql.functions.FunctionElement.select "sqlalchemy.sql.functions.FunctionElement.select")来产生一个SELECT结构。

        请注意，可以将[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")传递给[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")或[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的[`Connectable.execute()`](connections.html#sqlalchemy.engine.Connectable.execute "sqlalchemy.engine.Connectable.execute")方法。

    `过滤 T0> （ T1>  *标准 T2> ） T3> ¶ T4>`{.descname}
    :   针对此功能生成一个FILTER子句。

        用于聚合和窗口函数，用于支持“FILTER”子句的数据库后端。

        表达方式：

            func.count(1).filter(True)

        简写为：

            from sqlalchemy import funcfilter
            funcfilter(func.count(1), True)

        版本1.0.0中的新功能

        也可以看看

        [`FunctionFilter`](sqlelement.html#sqlalchemy.sql.expression.FunctionFilter "sqlalchemy.sql.expression.FunctionFilter")

        [`funcfilter()`](sqlelement.html#sqlalchemy.sql.expression.funcfilter "sqlalchemy.sql.expression.funcfilter")

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   

     `over`{.descname}(*partition\_by=None*, *order\_by=None*, *rows=None*, *range\_=None*)[¶](#sqlalchemy.sql.functions.FunctionElement.over "Permalink to this definition")
    :   针对此功能产生一个OVER子句。

        针对聚合或所谓的“窗口”函数，用于支持窗口函数的数据库后端。

        表达方式：

            func.row_number().over(order_by='x')

        简写为：

            from sqlalchemy import over
            over(func.row_number(), order_by='x')

        有关完整说明，请参见[`over()`](sqlelement.html#sqlalchemy.sql.expression.over "sqlalchemy.sql.expression.over")。

        New in version 0.7.

    `packagenames`{.descname} *=()* [¶](#sqlalchemy.sql.functions.FunctionElement.packagenames "Permalink to this definition")
    :   

    `标量 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   对嵌入的“绑定”执行此[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")并返回标量值。

        这首先调用[`select()`](#sqlalchemy.sql.functions.FunctionElement.select "sqlalchemy.sql.functions.FunctionElement.select")来产生一个SELECT结构。

        请注意，可以将[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")传递给[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")或[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的[`Connectable.scalar()`](connections.html#sqlalchemy.engine.Connectable.scalar "sqlalchemy.engine.Connectable.scalar")方法。

    `选择 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   根据[`FunctionElement`](#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")产生一个[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

        这是简写​​：

            s = select([function_element])

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   

    ` within_group  T0> （ T1>  * ORDER_BY  T2> ） T3> ¶ T4>`{.descname}
    :   根据此函数生成一个WITHIN GROUP（ORDER BY expr）子句。

        针对所谓的“有序集合”和“假设集合”功能，包括[`percentile_cont`](#sqlalchemy.sql.functions.percentile_cont "sqlalchemy.sql.functions.percentile_cont")，[`rank`](#sqlalchemy.sql.functions.rank "sqlalchemy.sql.functions.rank")，[`dense_rank`](#sqlalchemy.sql.functions.dense_rank "sqlalchemy.sql.functions.dense_rank")等。

        有关完整说明，请参见[`within_group()`](sqlelement.html#sqlalchemy.sql.expression.within_group "sqlalchemy.sql.expression.within_group")。

        版本1.1中的新功能

    ` within_group_type  T0> （ T1>  within_group  T2> ） T3> ¶ T4>`{.descname}
    :   对于根据由[`WithinGroup`](sqlelement.html#sqlalchemy.sql.expression.WithinGroup "sqlalchemy.sql.expression.WithinGroup")构造调用的WITHIN
        GROUP（ORDER BY）表达式中的条件定义其返回类型的类型。

        默认返回None，在这种情况下使用函数的普通`.type`。

 *class*`sqlalchemy.sql.functions.`{.descclassname}`GenericFunction`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.GenericFunction "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")

    定义一个“通用”功能。

    通用函数是预先建立的[`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")类，当从[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")属性中按名称调用时，会自动实例化该类。请注意，调用[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")中的任何名称都会导致自动创建新的[`Function`](#sqlalchemy.sql.functions.Function "sqlalchemy.sql.functions.Function")实例，并给定该名称。定义一个[`GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")类的主要用例是这样的，一个特定名称的函数可以被赋予一个固定的返回类型。它还可以包含自定义参数解析方案以及其他方法。

    [`GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")的子类自动注册在类的名字下。例如，用户定义的函数`as_utc()`将立即可用：

        from sqlalchemy.sql.functions import GenericFunction
        from sqlalchemy.types import DateTime

        class as_utc(GenericFunction):
            type = DateTime

        print select([func.as_utc()])

    在定义[`GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")时，通过指定“package”属性可以将用户定义的泛型函数组织成包。包含许多功能的第三方库可能希望使用此功能以避免与其他系统发生名称冲突。例如，如果我们的`as_utc()`函数是包“time”的一部分：

        class as_utc(GenericFunction):
            type = DateTime
            package = "time"

    上面的函数可以从[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")使用包名称`time`获得：

        print select([func.time.as_utc()])

    最后一个选项是允许从[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")中的某个名称访问该函数，但要呈现为不同的名称。`identifier`属性将覆盖从[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")加载的用于访问函数的名称，但会保留`name`作为呈现名称的用法：

        class GeoBuffer(GenericFunction):
            type = Geometry
            package = "geo"
            name = "ST_Buffer"
            identifier = "buffer"

    上述功能将呈现如下：

        >>> print func.geo.buffer()
        ST_Buffer()

    0.8版新增功能： [`GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")现在支持新功能的自动注册以及软件包和自定义命名支持。

    在版本0.8中更改：属性名称`type`用于在类级别指定函数的返回类型。以前，使用名称`__return_type__`。这个名字仍然被认为是向后兼容的。

    `coerce_arguments`{.descname} *= True* [¶](#sqlalchemy.sql.functions.GenericFunction.coerce_arguments "Permalink to this definition")
    :   

    `标识符`{.descname} *='GenericFunction'* [¶](#sqlalchemy.sql.functions.GenericFunction.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='GenericFunction'* [¶](#sqlalchemy.sql.functions.GenericFunction.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`OrderedSetAgg`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.OrderedSetAgg "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    定义一个返回类型基于传递给[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")方法的表达式定义的排序表达式类型的函数。plain

    `array_for_multi_clause`{.descname} *= False* [¶](#sqlalchemy.sql.functions.OrderedSetAgg.array_for_multi_clause "Permalink to this definition")
    :   

    `标识符`{.descname} *='OrderedSetAgg'* [¶](#sqlalchemy.sql.functions.OrderedSetAgg.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='OrderedSetAgg'* [¶](#sqlalchemy.sql.functions.OrderedSetAgg.name "Permalink to this definition")
    :   

    ` within_group_type  T0> （ T1>  within_group  T2> ） T3> ¶ T4>`{.descname}
    :   

*class* `sqlalchemy.sql.functions。`{.descclassname} `ReturnTypeFromArgs`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.ReturnTypeFromArgs "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    定义一个返回类型与其参数相同的函数。plain

    `标识符`{.descname} *='ReturnTypeFromArgs'* [¶](#sqlalchemy.sql.functions.ReturnTypeFromArgs.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='ReturnTypeFromArgs'* [¶](#sqlalchemy.sql.functions.ReturnTypeFromArgs.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`array_agg`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.array_agg "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    支持ARRAY\_AGG功能。

    `func.array_agg(expr)`结构返回[`types.ARRAY`](type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型的表达式。

    例如。：

        stmt = select([func.array_agg(table.c.values)[2:5]])

    版本1.1中的新功能

    也可以看看

    [`postgresql.array_agg()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array_agg "sqlalchemy.dialects.postgresql.array_agg")
    - PostgreSQL特定版本，它返回[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")，其中添加了PG专用操作符。

    `标识符`{.descname} *='array\_agg'* [¶](#sqlalchemy.sql.functions.array_agg.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='array\_agg'* [¶](#sqlalchemy.sql.functions.array_agg.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `ARRAY`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `char_length`{.descname} （ *arg*，*\* \* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.char_length "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    `标识符`{.descname} *='char\_length'* [¶](#sqlalchemy.sql.functions.char_length.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='char\_length'* [¶](#sqlalchemy.sql.functions.char_length.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `Integer`的别名

 *class*`sqlalchemy.sql.functions.`{.descclassname}`coalesce`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.coalesce "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.ReturnTypeFromArgs`](#sqlalchemy.sql.functions.ReturnTypeFromArgs "sqlalchemy.sql.functions.ReturnTypeFromArgs")

    `标识符`{.descname} *='coalesce'* [¶](#sqlalchemy.sql.functions.coalesce.identifier "Permalink to this definition")
    :   

    `姓名`{.descname} *='coalesce'* [¶](#sqlalchemy.sql.functions.coalesce.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`concat`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.concat "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    `标识符`{.descname} *='concat'* [¶](#sqlalchemy.sql.functions.concat.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='concat'* [¶](#sqlalchemy.sql.functions.concat.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `String`的别名

 *class*`sqlalchemy.sql.functions.`{.descclassname}`count`{.descname}(*expression=None*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.count "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    ANSI COUNT聚合函数。没有参数，会发出COUNT \*。

    `标识符`{.descname} *='count'* [¶](#sqlalchemy.sql.functions.count.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='count'* [¶](#sqlalchemy.sql.functions.count.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `Integer`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `cume_dist`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.cume_dist "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    实现`cume_dist`假设集合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    这个函数的返回类型是[`Numeric`](type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")。

    版本1.1中的新功能

    `标识符`{.descname} *='cume\_dist'* [¶](#sqlalchemy.sql.functions.cume_dist.identifier "Permalink to this definition")
    :   

    `姓名`{.descname} *='cume\_dist'* [¶](#sqlalchemy.sql.functions.cume_dist.name "Permalink to this definition")
    :   

    `类型`{.descname} *=数字()* [¶](#sqlalchemy.sql.functions.cume_dist.type "Permalink to this definition")
    :   

*class* `sqlalchemy.sql.functions。`{.descclassname} `current_date`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.current_date "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='当前日期'* [¶](#sqlalchemy.sql.functions.current_date.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='current\_date'* [¶](#sqlalchemy.sql.functions.current_date.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `Date`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `current_time`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.current_time "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='current\_time'* [¶](#sqlalchemy.sql.functions.current_time.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='current\_time'* [¶](#sqlalchemy.sql.functions.current_time.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `Time`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `current_timestamp`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.current_timestamp "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='current\_timestamp'* [¶](#sqlalchemy.sql.functions.current_timestamp.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='current\_timestamp'* [¶](#sqlalchemy.sql.functions.current_timestamp.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `DateTime`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `current_user`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.current_user "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='current\_user'* [¶](#sqlalchemy.sql.functions.current_user.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='current\_user'* [¶](#sqlalchemy.sql.functions.current_user.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `String`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `dense_rank`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.dense_rank "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    实现`dense_rank`假设集合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    这个函数的返回类型是[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")。

    版本1.1中的新功能

    `标识符`{.descname} *='dense\_rank'* [¶](#sqlalchemy.sql.functions.dense_rank.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='dense\_rank'* [¶](#sqlalchemy.sql.functions.dense_rank.name "Permalink to this definition")
    :   

    `type`{.descname} *= Integer()* [¶](#sqlalchemy.sql.functions.dense_rank.type "Permalink to this definition")
    :   

*class* `sqlalchemy.sql.functions。`{.descclassname} `localtime`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.localtime "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='localtime'* [¶](#sqlalchemy.sql.functions.localtime.identifier "Permalink to this definition")plain
    :   

    `name`{.descname} *='localtime'* [¶](#sqlalchemy.sql.functions.localtime.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `DateTime`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `localtimestamp`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.localtimestamp "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='本地时间戳'* [¶](#sqlalchemy.sql.functions.localtimestamp.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='localtimestamp'* [¶](#sqlalchemy.sql.functions.localtimestamp.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `DateTime`的别名

 *class*`sqlalchemy.sql.functions.`{.descclassname}`max`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.max "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.ReturnTypeFromArgs`](#sqlalchemy.sql.functions.ReturnTypeFromArgs "sqlalchemy.sql.functions.ReturnTypeFromArgs")

    `标识符`{.descname} *='max'* [¶](#sqlalchemy.sql.functions.max.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='max'* [¶](#sqlalchemy.sql.functions.max.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`min`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.min "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.ReturnTypeFromArgs`](#sqlalchemy.sql.functions.ReturnTypeFromArgs "sqlalchemy.sql.functions.ReturnTypeFromArgs")

    `identifier`{.descname} *='min'* [¶](#sqlalchemy.sql.functions.min.identifier "Permalink to this definition")
    :   

    `姓名`{.descname} *='分钟'* [¶](#sqlalchemy.sql.functions.min.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`mode`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.mode "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.OrderedSetAgg`](#sqlalchemy.sql.functions.OrderedSetAgg "sqlalchemy.sql.functions.OrderedSetAgg")

    实现`mode`有序集聚合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    该函数的返回类型与排序表达式相同。

    版本1.1中的新功能

    `identifier`{.descname} *='mode'* [¶](#sqlalchemy.sql.functions.mode.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='mode'* [¶](#sqlalchemy.sql.functions.mode.name "Permalink to this definition")
    :   

*class* `sqlalchemy.sql.functions。`{.descclassname} `next_value`{.descname} （ *seq*，*\* \*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.next_value "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    以[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")作为其单个参数，表示'下一个值'。

    编译为每个后端的相应函数，或者如果在不支持序列的后端上使用，则会引发NotImplementedError。

    `标识符`{.descname} *='next\_value'* [¶](#sqlalchemy.sql.functions.next_value.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='next\_value'* [¶](#sqlalchemy.sql.functions.next_value.name "Permalink to this definition")
    :   

    `type`{.descname} *= Integer()* [¶](#sqlalchemy.sql.functions.next_value.type "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`now`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.now "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    `标识符`{.descname} *='现在'* [¶](#sqlalchemy.sql.functions.now.identifier "Permalink to this definition")
    :   

    `姓名`{.descname} *='现在'* [¶](#sqlalchemy.sql.functions.now.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `DateTime`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `percent_rank`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.percent_rank "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    实现`percent_rank`假设集合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    这个函数的返回类型是[`Numeric`](type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")。

    版本1.1中的新功能

    `标识符`{.descname} *='percent\_rank'* [¶](#sqlalchemy.sql.functions.percent_rank.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='percent\_rank'* [¶](#sqlalchemy.sql.functions.percent_rank.name "Permalink to this definition")
    :   

    `类型`{.descname} *=数字()* [¶](#sqlalchemy.sql.functions.percent_rank.type "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`percentile_cont`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.percentile_cont "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.OrderedSetAgg`](#sqlalchemy.sql.functions.OrderedSetAgg "sqlalchemy.sql.functions.OrderedSetAgg")

    实现`percentile_cont`有序集合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    此函数的返回类型与排序表达式相同，或者如果参数是数组，则为排序表达式类型的[`types.ARRAY`](type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")。

    版本1.1中的新功能

    `array_for_multi_clause`{.descname} *= True* [¶](#sqlalchemy.sql.functions.percentile_cont.array_for_multi_clause "Permalink to this definition")
    :   

    `标识符`{.descname} *='percentile\_cont'* [¶](#sqlalchemy.sql.functions.percentile_cont.identifier "Permalink to this definition")
    :   

    `姓名`{.descname} *='percentile\_cont'* [¶](#sqlalchemy.sql.functions.percentile_cont.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`percentile_disc`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.percentile_disc "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.OrderedSetAgg`](#sqlalchemy.sql.functions.OrderedSetAgg "sqlalchemy.sql.functions.OrderedSetAgg")

    实现`percentile_disc`有序集合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    此函数的返回类型与排序表达式相同，或者如果参数是数组，则为排序表达式类型的[`types.ARRAY`](type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")。

    版本1.1中的新功能

    `array_for_multi_clause`{.descname} *= True* [¶](#sqlalchemy.sql.functions.percentile_disc.array_for_multi_clause "Permalink to this definition")
    :   

    `标识符`{.descname} *='percentile\_disc'* [¶](#sqlalchemy.sql.functions.percentile_disc.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='percentile\_disc'* [¶](#sqlalchemy.sql.functions.percentile_disc.name "Permalink to this definition")
    :   

*class* `sqlalchemy.sql.functions。`{.descclassname} `random`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.sql.functions.random "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    `标识符`{.descname} *='随机'* [¶](#sqlalchemy.sql.functions.random.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='随机'* [¶](#sqlalchemy.sql.functions.random.name "Permalink to this definition")
    :   

 *class*`sqlalchemy.sql.functions.`{.descclassname}`rank`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.rank "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    实现`rank`假设集合函数。

    该函数必须与[`FunctionElement.within_group()`](#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")修饰符一起使用，以提供一个排序表达式来进行操作。

    这个函数的返回类型是[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")。

    版本1.1中的新功能

    `标识符`{.descname} *='rank'* [¶](#sqlalchemy.sql.functions.rank.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='rank'* [¶](#sqlalchemy.sql.functions.rank.name "Permalink to this definition")
    :   

    `type`{.descname} *= Integer()* [¶](#sqlalchemy.sql.functions.rank.type "Permalink to this definition")
    :   

 `sqlalchemy.sql.functions.`{.descclassname}`register_function`{.descname}(*identifier*, *fn*, *package='\_default'*)[¶](#sqlalchemy.sql.functions.register_function "Permalink to this definition")
:   将可调用函数与特定的函数关联。名称。

    这通常由\_GenericMeta调用，但也可以自行使用，以便非函数结构可以与[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")访问器关联（即，CAST，EXTRACT）。

*class* `sqlalchemy.sql.functions。`{.descclassname} `session_user`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.session_user "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='session\_user'* [¶](#sqlalchemy.sql.functions.session_user.identifier "Permalink to this definition")plain
    :   

    `name`{.descname} *='session\_user'* [¶](#sqlalchemy.sql.functions.session_user.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `String`的别名

 *class*`sqlalchemy.sql.functions.`{.descclassname}`sum`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.sql.functions.sum "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.ReturnTypeFromArgs`](#sqlalchemy.sql.functions.ReturnTypeFromArgs "sqlalchemy.sql.functions.ReturnTypeFromArgs")

    `标识符`{.descname} *='sum'* [¶](#sqlalchemy.sql.functions.sum.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='sum'* [¶](#sqlalchemy.sql.functions.sum.name "Permalink to this definition")
    :   

*class* `sqlalchemy.sql.functions。`{.descclassname} `sysdate`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.sysdate "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='sysdate'* [¶](#sqlalchemy.sql.functions.sysdate.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='sysdate'* [¶](#sqlalchemy.sql.functions.sysdate.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `DateTime`的别名

*class* `sqlalchemy.sql.functions。`{.descclassname} `user`{.descname} （ *\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.sql.functions.user "Permalink to this definition")
:   基础：[`sqlalchemy.sql.functions.AnsiFunction`](#sqlalchemy.sql.functions.AnsiFunction "sqlalchemy.sql.functions.AnsiFunction")

    `标识符`{.descname} *='user'* [¶](#sqlalchemy.sql.functions.user.identifier "Permalink to this definition")
    :   

    `name`{.descname} *='user'* [¶](#sqlalchemy.sql.functions.user.name "Permalink to this definition")
    :   

    `型 T0> ¶ T1>`{.descname}
    :   `String`的别名


