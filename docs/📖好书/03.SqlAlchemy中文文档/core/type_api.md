---
title: 基本类型 API
date: 2021-02-20 22:41:37
permalink: /sqlalchemy/core/type_api/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
基本类型 API [¶](#base-type-api "Permalink to this headline")
============================================================

*class* `sqlalchemy.types。`{.descclassname} `TypeEngine`{.descname} [¶](#sqlalchemy.types.TypeEngine "Permalink to this definition")
:   基础：`sqlalchemy.sql.visitors.Visitable`

    所有SQL数据类型的最终基类。

    [`TypeEngine`](#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")的通用子类包括[`String`](type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")，[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")和[`Boolean`](type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")。

    有关SQLAlchemy类型系统的概述，请参见[Column and Data
    Types](types.html)。

    也可以看看

    [Column and Data Types](types.html)

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.types.TypeEngine.Comparator "Permalink to this definition")
    :   基础：[`sqlalchemy.sql.operators.ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在类型级别定义的自定义比较操作的基类。请参阅[`TypeEngine.comparator_factory`](#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")。

     `TypeEngine.`{.descclassname}`adapt`{.descname}(*cls*, *\*\*kw*)[¶](#sqlalchemy.types.TypeEngine.adapt "Permalink to this definition")
    :   产生这种类型的“适应”形式，给予一个“impl”类来处理。

        此方法在内部用于将泛型与特定于特定方言的“实现”类型相关联。

    ` TypeEngine。 T0>  bind_expression  T1> （ T2>  bindvalue  T3> ） T4> ¶ T5>`{.descclassname}
    :   “给定一个绑定值（即一个[`BindParameter`](sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")实例），在它的位置返回一个SQL表达式。

        这通常是一个包含语句中现有绑定参数的SQL函数。它用于特殊数据类型，这些数据类型需要文字被封装在某些特殊的数据库函数中，以便将应用程序级别的值强制转换为数据库特定的格式。它是[`TypeEngine.bind_processor()`](#sqlalchemy.types.TypeEngine.bind_processor "sqlalchemy.types.TypeEngine.bind_processor")方法的SQL模拟。

        该方法在语句编译时进行评估，而不是语句构建时间。

        请注意，此方法在实现时应始终返回完全相同的结构，而不使用任何条件逻辑，因为它可用于针对任意数量的绑定参数集的executemany()调用。

        也可以看看：

        [Applying SQL-level Bind/Result
        Processing](custom_types.html#types-sql-value-processing)

    ` TypeEngine。 T0>  bind_processor  T1> （ T2> 方言 T3> ） T4> ¶ T5>`{.descclassname}
    :   返回处理绑定值的转换函数。

        返回一个可调用的对象，它将接收一个绑定参数值作为唯一的位置参数，并返回一个值发送给DB-API。

        如果不需要处理，该方法应该返回`None`。

        参数：

        **dialect**
        [¶](#sqlalchemy.types.TypeEngine.bind_processor.params.dialect)
        - Dialect实例正在使用中。

    `TypeEngine`{.descclassname} `coerce_compared_value`{.descname} （ *op*，*值* ） [¶ T6\>](#sqlalchemy.types.TypeEngine.coerce_compared_value "Permalink to this definition")
    :   为表达式中的'强制'Python值建议类型。

        给定一个运算符和值，给这个类型一个机会返回值应该被强制转换的类型。

        这里的默认行为是保守的；如果右侧已经被强制为一个基于它的Python类型的SQL类型，那么它通常是独立的。

        这里的最终用户功能扩展通常应该通过[`TypeDecorator`](custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")，它提供了更自由的行为，因为它默认将表达式的另一端强制转换为这种类型，从而将特殊的Python转换应用到超出需要的地方由DBAPI向两个ide。它还提供了用于此行为的最终用户定制的公共方法[`TypeDecorator.coerce_compared_value()`](custom_types.html#sqlalchemy.types.TypeDecorator.coerce_compared_value "sqlalchemy.types.TypeDecorator.coerce_compared_value")。

    ` TypeEngine。 T0>  column_expression  T1> （ T2>  colexpr  T3> ） T4> ¶ T5>`{.descclassname}
    :   给定一个SELECT列表达式，返回一个包装SQL表达式。

        这通常是一个SQL函数，它包装列表达式，并将其呈现在SELECT语句的columns子句中。它用于特殊数据类型，这些数据类型需要将列包装在某些特殊的数据库函数中，以便在将值返回给应用程序之前强制值。它是[`TypeEngine.result_processor()`](#sqlalchemy.types.TypeEngine.result_processor "sqlalchemy.types.TypeEngine.result_processor")方法的SQL模拟。

        该方法在语句编译时进行评估，而不是语句构建时间。

        也可以看看：

        [Applying SQL-level Bind/Result
        Processing](custom_types.html#types-sql-value-processing)

    ` TypeEngine。 T0>  comparator_factory  T1> ¶ T2>`{.descclassname}
    :   基础：[`sqlalchemy.sql.operators.ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        一个[`TypeEngine.Comparator`](#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")类，它将应用于拥有[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")对象的操作。

        [`comparator_factory`](#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")属性是在执行列和SQL表达式操作时由核心表达式系统查询的钩子。当[`TypeEngine.Comparator`](#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")类与此属性关联时，它允许自定义所有现有运算符的重新定义，并定义新的运算符。Existing
        operators include those provided by Python operator overloading
        such as [`operators.ColumnOperators.__add__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__add__ "sqlalchemy.sql.operators.ColumnOperators.__add__")
        and [`operators.ColumnOperators.__eq__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__"),
        those provided as standard attributes of
        [`operators.ColumnOperators`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")
        such as [`operators.ColumnOperators.like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
        and [`operators.ColumnOperators.in_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_").

        通过对现有类型进行简单的子类化，或者通过使用[`TypeDecorator`](custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")，可以使用该钩子的基本用法。有关示例，请参阅文档部分[Redefining
        and Creating New Operators](custom_types.html#types-operators)。

        0.8版新增功能：增强了表达式系统，支持按类型级别定制运算符。

        [`Comparator`](#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")的别名

    `TypeEngine`{.descclassname} `compare_against_backend`{.descname} （ *方言*，*conn\_type* ） [¶ T6\>](#sqlalchemy.types.TypeEngine.compare_against_backend "Permalink to this definition")
    :   将此类型与给定的后端类型进行比较。

        此函数目前尚未针对SQLAlchemy类型实现，对于所有内置类型，此函数将返回`None`。但是，它可以通过用户定义的类型实现，可以通过模式比较工具（如Alembic
        autogenerate）使用它。

        未来的SQLAlchemy版本也可能会对这种内置类型的方法产生影响。

        如果此类型与给定类型相同，则该函数应返回True；该类型通常反映在数据库中，因此应该是数据库特定的。使用的方言也通过了。它也可以返回False来声明该类型不相同。

        参数：

        -   **dialect**[¶](#sqlalchemy.types.TypeEngine.compare_against_backend.params.dialect)
            – a [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
            that is involved in the comparison.
        -   **conn\_type**
            [¶](#sqlalchemy.types.TypeEngine.compare_against_backend.params.conn_type)
            - 从后端反射的类型对象。

        版本1.0.3中的新功能

    `TypeEngine`{.descclassname} `compare_values`{.descname} （ *x*，*y* ） [¶ T6\>](#sqlalchemy.types.TypeEngine.compare_values "Permalink to this definition")
    :   比较两个值是否相等。

    ` TypeEngine。 T0> 编译 T1> （ T2> 方言=无 T3> ） T4> ¶ T5 >`{.descclassname}
    :   生成此[`TypeEngine`](#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")的字符串编译形式。

        当不带参数调用时，使用“默认”方言产生字符串结果。

        参数：

        **dialect**
        [¶](#sqlalchemy.types.TypeEngine.compile.params.dialect) - a
        [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")实例。

    ` TypeEngine。 T0>  dialect_impl  T1> （ T2> 方言 T3> ） T4> ¶ T5>`{.descclassname}
    :   返回该[`TypeEngine`](#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")的特定于方言的实现。

    ` TypeEngine。 T0>  evaluates_none  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
    :   返回将[`should_evaluate_none`](#sqlalchemy.types.TypeEngine.should_evaluate_none "sqlalchemy.types.TypeEngine.should_evaluate_none")标志设置为True的此类型的副本。

        例如。：

            Table(
                'some_table', metadata,
                Column(
                    String(50).evaluates_none(),
                    nullable=True,
                    server_default='no value')
            )

        ORM使用此标志来指示在INSERT语句中将`None`的正值传递到列，而不是从INSERT语句中省略列，该列具有触发列级缺省值的效果。它还允许具有与Python
        None值关联的特殊行为的类型指示该值不一定会转换为SQL
        NULL；这是一个JSON类型的主要例子，它可能希望保存JSON值`'null'`。

        在所有情况下，通过在INSERT语句中使用[`null`](sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")
        SQL构造或与ORM映射属性关联，实际的NULL
        SQL值可始终保留在任何列中。

        版本1.1中的新功能

        也可以看看

        [Forcing NULL on a column with a
        default](orm_persistence_techniques.html#session-forcing-null) -
        in the ORM documentation

        [`postgresql.JSON.none_as_null`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.params.none_as_null "sqlalchemy.dialects.postgresql.JSON")
        - Postgresql与此标志的JSON交互。

        [`TypeEngine.should_evaluate_none`](#sqlalchemy.types.TypeEngine.should_evaluate_none "sqlalchemy.types.TypeEngine.should_evaluate_none")
        - class-level flag

    ` TypeEngine。 T0>  get_dbapi_type  T1> （ T2>  DBAPI  T3> ） T4> ¶ T5>`{.descclassname}
    :   如果有的话，从底层DB-API返回相应的类型对​​象。

        > 例如，这可以用于调用`setinputsizes()`。

    `TypeEngine`{.descclassname} `hashable`{.descname} *= True* [¶](#sqlalchemy.types.TypeEngine.hashable "Permalink to this definition")
    :   标志，如果为False，则表示此类型的值不可哈希。

        分配结果列表时由ORM使用。

    ` TypeEngine。 T0>  literal_processor  T1> （ T2> 方言 T3> ） T4> ¶ T5>`{.descclassname}
    :   返回一个转换函数，用于处理不使用绑定直接呈现的文字值。

        当编译器使用通常用于DDL生成的“literal\_binds”标志以及后端不接受绑定参数的某些情况时，会使用此函数。

        版本0.9.0中的新功能

    ` TypeEngine。 T0>  python_type  T1> ¶ T2>`{.descclassname}
    :   如果已知，则返回预期由此类型的实例返回的Python类型对象。

        基本上，对于那些强制执行返回类型的类型，或者在所有常见DBAPI（例如`int`）中都可以这样做的类型，将返回该类型。

        如果未定义返回类型，则引发`NotImplementedError`。

        请注意，任何类型也可以在SQL中容纳NULL，这意味着您在实践中也可以从任何类型获取`None`。

    `TypeEngine。`{.descclassname} `result_processor`{.descname} （ *方言*，*coltype* ） [¶ T6\>](#sqlalchemy.types.TypeEngine.result_processor "Permalink to this definition")
    :   返回处理结果行值的转换函数。

        返回一个可调用对象，它将接收结果行列值作为唯一的位置参数，并返回一个值以返回给用户。

        如果不需要处理，该方法应该返回`None`。

        参数：

        -   **dialect**
            [¶](#sqlalchemy.types.TypeEngine.result_processor.params.dialect)
            - Dialect实例正在使用中。
        -   **coltype**[¶](#sqlalchemy.types.TypeEngine.result_processor.params.coltype)
            – DBAPI coltype argument received in cursor.description.

    `TypeEngine`{.descclassname} `should_evaluate_none`{.descname} *= False* [¶](#sqlalchemy.types.TypeEngine.should_evaluate_none "Permalink to this definition")
    :   如果为True，则Python常量`None`被认为是由此类型明确处理的。

        ORM使用此标志来指示在INSERT语句中将`None`的正值传递到列，而不是从INSERT语句中省略列，该列具有触发列级缺省值的效果。它还允许对Python有特殊行为的类型，例如JSON类型，表示他们想要明确处理None值。

        要在现有类型上设置此标志，请使用[`TypeEngine.evaluates_none()`](#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")方法。

        也可以看看

        [`TypeEngine.evaluates_none()`](#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")

        版本1.1中的新功能

     `TypeEngine.`{.descclassname}`with_variant`{.descname}(*type\_*, *dialect\_name*)[¶](#sqlalchemy.types.TypeEngine.with_variant "Permalink to this definition")
    :   生成一个新的类型对象，将其应用于给定名称的方言时使用给定的类型。

        例如。：

            from sqlalchemy.types import String
            from sqlalchemy.dialects import mysql

            s = String()

            s = s.with_variant(mysql.VARCHAR(collation='foo'), 'mysql')

        [`TypeEngine.with_variant()`](#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")的构造始终是从“fallback”类型到特定于方言的。返回的类型是[`Variant`](#sqlalchemy.types.Variant "sqlalchemy.types.Variant")的一个实例，它本身提供了一个可重复调用的`Variant.with_variant()`。

        参数：

        -   **type\_**[¶](#sqlalchemy.types.TypeEngine.with_variant.params.type_)
            – a [`TypeEngine`](#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
            that will be selected as a variant from the originating
            type, when a dialect of the given name is in use.
        -   **dialect\_name**[¶](#sqlalchemy.types.TypeEngine.with_variant.params.dialect_name)
            – base name of the dialect which uses this type.
            （即`'postgresql'`，`'mysql'`等）

        New in version 0.7.2.

*class* `sqlalchemy.types。`{.descclassname} `可连接`{.descname} [¶](#sqlalchemy.types.Concatenable "Permalink to this definition")
:   mixin 标志着一种类型支持“连接”，通常是字符串。

*class* `sqlalchemy.types。`{.descclassname} `可索引`{.descname} [¶](#sqlalchemy.types.Indexable "Permalink to this definition")
:   mixin 标记类型为支持索引操作，如数组或 JSON 结构。

    版本1.1.0中的新功能plain

*class* `sqlalchemy.types。`{.descclassname} `NullType`{.descname} [¶](#sqlalchemy.types.NullType "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    一个未知的类型。

    [`NullType`](#sqlalchemy.types.NullType "sqlalchemy.types.NullType")
    is used as a default type for those cases where a type cannot be
    determined, including:

    -   在表反射过程中，当[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")不识别列的类型时
    -   使用未知类型的纯Python对象（例如`somecolumn == my_special_object`）构造SQL表达式时，
    -   当创建一个新的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")，并且给定的类型作为`None`传递或根本不传递。

    可以在SQL表达式调用中毫无问题地使用[`NullType`](#sqlalchemy.types.NullType "sqlalchemy.types.NullType")，它只是在表达式构造级别或绑定参数/结果处理级别上没有任何行为。[`NullType`](#sqlalchemy.types.NullType "sqlalchemy.types.NullType")
    will result in a [`CompileError`](exceptions.html#sqlalchemy.exc.CompileError "sqlalchemy.exc.CompileError")
    if the compiler is asked to render the type itself, such as if it is
    used in a [`cast()`](sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")
    operation or within a schema creation operation such as that invoked
    by [`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
    or the [`CreateTable`](ddl.html#sqlalchemy.schema.CreateTable "sqlalchemy.schema.CreateTable")
    construct.

 *class*`sqlalchemy.types.`{.descclassname}`Variant`{.descname}(*base*, *mapping*)[¶](#sqlalchemy.types.Variant "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeDecorator`](custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")

    一种包装类型，可根据使用的方言在各种实现中进行选择。

    [`Variant`](#sqlalchemy.types.Variant "sqlalchemy.types.Variant")类型通常使用[`TypeEngine.with_variant()`](#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")方法构造。

    New in version 0.7.2.

    也可以看看

    [`TypeEngine.with_variant()`](#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
    for an example of use.

    成员：

    with\_variant，\_\_init\_\_


