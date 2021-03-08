---
title: 自定义类型
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/orm/custom_types/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
自定义类型[¶](#custom-types "Permalink to this headline")
=========================================================

存在多种方法来重新定义现有类型的行为并提供新的类型。

重写类型编译[¶](#overriding-type-compilation "Permalink to this headline")
--------------------------------------------------------------------------

经常需要强制更改类型的“字符串”版本，即在 CREATE
TABLE 语句或其他 SQL 函数（如 CAST）中呈现的类型。例如，应用程序可能希望强制为所有平台呈现`BINARY`，除了要呈现其中的`BLOB`之外的所有平台。对于大多数使用情况，现有泛型类型（在本例中为[`LargeBinary`](type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")）的使用是首选。但为了更准确地控制类型，每个方言的编译指令可以与任何类型相关联：

    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.types import BINARY

    @compiles(BINARY, "sqlite")
    def compile_binary_sqlite(type_, compiler, **kw):
        return "BLOB"

上面的代码允许使用[`types.BINARY`](type_basics.html#sqlalchemy.types.BINARY "sqlalchemy.types.BINARY")，它将针对除 SQLite 以外的所有后端生成字符串`BINARY`，在这种情况下，它将生成`BLOB`

有关其他示例，请参阅[Changing Compilation of
Types](compiler.html#type-compilation-extension)一节（[Custom SQL
Constructs and Compilation Extension](compiler.html)的小节）。

增加现有类型[¶](#augmenting-existing-types "Permalink to this headline")
------------------------------------------------------------------------

[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")允许创建自定义类型，将绑定参数和结果处理行为添加到现有的类型对象。当需要对数据库进行额外的Python数据封送处理时使用它。

注意

The bind- and result-processing of [`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
is *in addition* to the processing already performed by the hosted type,
which is customized by SQLAlchemy on a per-DBAPI basis to perform
processing specific to that DBAPI.
要更改现有类型的DBAPI级处理，请参阅[Replacing the Bind/Result Processing
of Existing Types](#replacing-processors)部分。

 *class*`sqlalchemy.types.`{.descclassname}`TypeDecorator`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.types.TypeDecorator "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.SchemaEventTarget`，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    允许创建向现有类型添加附加功能的类型。

    此方法优先于指定SQLAlchemy内置类型的子类化，因为它确保所有必需的基础类型功能都保留在原位。

    典型用法：

        import sqlalchemy.types as types

        class MyType(types.TypeDecorator):
            '''Prefixes Unicode values with "PREFIX:" on the way in and
            strips it off on the way out.
            '''

            impl = types.Unicode

            def process_bind_param(self, value, dialect):
                return "PREFIX:" + value

            def process_result_value(self, value, dialect):
                return value[7:]

            def copy(self, **kw):
                return MyType(self.impl.length)

    类级别的“impl”属性是必需的，并且可以引用任何TypeEngine类。或者，可以使用load\_dialect\_impl()方法根据给定的方言提供不同的类型类；在这种情况下，“impl”变量可以引用`TypeEngine`作为占位符。

    接收与所使用的最终类型不相似的Python类型的类型可能需要定义[`TypeDecorator.coerce_compared_value()`](#sqlalchemy.types.TypeDecorator.coerce_compared_value "sqlalchemy.types.TypeDecorator.coerce_compared_value")方法。这用于在将表达式中的Python对象强制为绑定参数时为表达式系统提供提示。考虑这个表达式：

        mytable.c.somecol + datetime.date(2009, 5, 15)

    在上面，如果“somecol”是一个`Integer`变体，那么我们在做日期算术是有意义的，上面的数据通常被数据库解释为给给定日期添加了几天。表达式系统通过不尝试将“date()”值强制为面向整数的绑定参数来做正确的事情。

    但是，在`TypeDecorator`的情况下，我们通常将传入的Python类型更改为新的 -
    `TypeDecorator`默认情况下会“强制”非类型侧是相同的键入本身。如下所示，我们定义一个“纪元”类型，它将日期值存储为整数：

        class MyEpochType(types.TypeDecorator):
            impl = types.Integer

            epoch = datetime.date(1970, 1, 1)

            def process_bind_param(self, value, dialect):
                return (value - self.epoch).days

            def process_result_value(self, value, dialect):
                return self.epoch + timedelta(days=value)

    Our expression of `somecol + date` with the
    above type will coerce the “date” on the right side to also be
    treated as `MyEpochType`.

    此行为可以通过[`coerce_compared_value()`](#sqlalchemy.types.TypeDecorator.coerce_compared_value "sqlalchemy.types.TypeDecorator.coerce_compared_value")方法覆盖，该方法返回应该用于表达式值的类型。下面我们将它设置为整数值将被视为一个`Integer`，并且任何其他值被假定为日期并且将被视为`MyEpochType`：

        def coerce_compared_value(self, op, value):
            if isinstance(value, int):
                return Integer()
            else:
                return self

    警告

    请注意，coerce\_compared\_value的**行为默认不会从基类型**的行为继承。如果[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")增加了某种类型的操作符需要特殊逻辑的类型，则必须重写此方法****。一个关键的例子是装饰[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")和[`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")类型；应该使用[`TypeEngine.coerce_compared_value()`](type_api.html#sqlalchemy.types.TypeEngine.coerce_compared_value "sqlalchemy.types.TypeEngine.coerce_compared_value")的默认规则来处理像索引操作这样的操作符：

        class MyJsonType(TypeDecorator):
            impl = postgresql.JSON

            def coerce_compared_value(self, op, value):
                return self.impl.coerce_compared_value(op, value)

    如果没有上述步骤，像`mycol['foo']`这样的索引操作将导致索引值`'foo'`进行JSON编码。

    `__ init __`{.descname} （ *\* args*，*\*\* kwargs* ） [T5\>](#sqlalchemy.types.TypeDecorator.__init__ "Permalink to this definition")
    :   构建一个[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")。

        Arguments sent here are passed to the constructor of the class
        assigned to the `impl` class level
        attribute, assuming the `impl` is a
        callable, and the resulting object is assigned to the
        `self.impl` instance attribute (thus
        overriding the class attribute of the same name).

        如果类级别`impl`不是可调用的（不寻常的情况），它将被分配给同样的实例属性'as-is'，忽略传递给构造函数的那些参数。

        子类可以覆盖它来完全自定义`self.impl`的生成。

     `adapt`{.descname}(*cls*, *\*\*kw*)[¶](#sqlalchemy.types.TypeDecorator.adapt "Permalink to this definition")
    :   *inherited from the* [`adapt()`](type_api.html#sqlalchemy.types.TypeEngine.adapt "sqlalchemy.types.TypeEngine.adapt")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        产生这种类型的“适应”形式，给予一个“impl”类来处理。

        此方法在内部用于将泛型与特定于特定方言的“实现”类型相关联。

    ` bind_expression  T0> （ T1>  bindvalue  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`bind_expression()`](type_api.html#sqlalchemy.types.TypeEngine.bind_expression "sqlalchemy.types.TypeEngine.bind_expression")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        “给定一个绑定值（即一个[`BindParameter`](sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")实例），在它的位置返回一个SQL表达式。

        这通常是一个包含语句中现有绑定参数的SQL函数。它用于特殊数据类型，这些数据类型需要文字被封装在某些特殊的数据库函数中，以便将应用程序级别的值强制转换为数据库特定的格式。它是[`TypeEngine.bind_processor()`](type_api.html#sqlalchemy.types.TypeEngine.bind_processor "sqlalchemy.types.TypeEngine.bind_processor")方法的SQL模拟。

        该方法在语句编译时进行评估，而不是语句构建时间。

        请注意，此方法在实现时应始终返回完全相同的结构，而不使用任何条件逻辑，因为它可用于针对任意数量的绑定参数集的executemany()调用。

        也可以看看：

        [Applying SQL-level Bind/Result
        Processing](#types-sql-value-processing)

    ` bind_processor  T0> （ T1> 方言 T2> ） T3> ¶ T4>`{.descname}
    :   为给定的[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")提供绑定值处理功能。

        这是实现用于绑定值转换的[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")合同的方法。[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
        will wrap a user-defined implementation of
        [`process_bind_param()`](#sqlalchemy.types.TypeDecorator.process_bind_param "sqlalchemy.types.TypeDecorator.process_bind_param")
        here.

        用户定义的代码可以直接覆盖此方法，尽管它最好使用[`process_bind_param()`](#sqlalchemy.types.TypeDecorator.process_bind_param "sqlalchemy.types.TypeDecorator.process_bind_param")，以保持由`self.impl`提供的处理。

        参数：

        **dialect**
        [¶](#sqlalchemy.types.TypeDecorator.bind_processor.params.dialect)
        - Dialect实例正在使用中。

        此方法与此类的[`result_processor()`](#sqlalchemy.types.TypeDecorator.result_processor "sqlalchemy.types.TypeDecorator.result_processor")方法相反。

    `coerce_compared_value`{.descname} （ *op*，*值* ） [](#sqlalchemy.types.TypeDecorator.coerce_compared_value "Permalink to this definition")
    :   为表达式中的'强制'Python值建议类型。

        默认情况下，返回self。如果使用此类型的对象位于表达式的左侧或右侧，而不是指定了SQLAlchemy类型的普通Python对象，则表达式系统将调用此方法：

            expr = table.c.somecolumn + 35

        Where above, if `somecolumn` uses this type,
        this method will be called with the value
        `operator.add` and `35`.
        返回值是任何SQLAlchemy类型应该用于此特定操作的`35`。

    `coerce_to_is_types`{.descname} *=（＆lt； type'NoneType＆gt；，）* [¶](#sqlalchemy.types.TypeDecorator.coerce_to_is_types "Permalink to this definition")
    :   使用`==`进行比较时指定应该在表达式级别转换为“IS
        ”的Python类型（对于`IS NOT 与!=`结合。

        对于大多数SQLAlchemy类型，这包括`NoneType`以及`bool`。

        [`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
        modifies this list to only include `NoneType`, as typedecorator implementations that deal with
        boolean types are common.

        Custom [`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")类可以覆盖此属性以返回空元组，在这种情况下，不会将值强制为常量。

        ..versionadded :: 0.8.2
        :   添加[`TypeDecorator.coerce_to_is_types`](#sqlalchemy.types.TypeDecorator.coerce_to_is_types "sqlalchemy.types.TypeDecorator.coerce_to_is_types")以便更容易地控制`__eq__()` `__ne__()`操作。

    ` column_expression  T0> （ T1>  colexpr  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`column_expression()`](type_api.html#sqlalchemy.types.TypeEngine.column_expression "sqlalchemy.types.TypeEngine.column_expression")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        给定一个SELECT列表达式，返回一个包装SQL表达式。

        这通常是一个SQL函数，它包装列表达式，并将其呈现在SELECT语句的columns子句中。它用于特殊数据类型，这些数据类型需要将列包装在某些特殊的数据库函数中，以便在将值返回给应用程序之前强制值。它是[`TypeEngine.result_processor()`](type_api.html#sqlalchemy.types.TypeEngine.result_processor "sqlalchemy.types.TypeEngine.result_processor")方法的SQL模拟。

        该方法在语句编译时进行评估，而不是语句构建时间。

        也可以看看：

        [Applying SQL-level Bind/Result
        Processing](#types-sql-value-processing)

    `compare_against_backend`{.descname} （ *dialect*，*conn\_type* ） [¶](#sqlalchemy.types.TypeDecorator.compare_against_backend "Permalink to this definition")
    :   *inherited from the* [`compare_against_backend()`](type_api.html#sqlalchemy.types.TypeEngine.compare_against_backend "sqlalchemy.types.TypeEngine.compare_against_backend")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        将此类型与给定的后端类型进行比较。

        此函数目前尚未针对SQLAlchemy类型实现，对于所有内置类型，此函数将返回`None`。但是，它可以通过用户定义的类型实现，可以通过模式比较工具（如Alembic
        autogenerate）使用它。

        未来的SQLAlchemy版本也可能会对这种内置类型的方法产生影响。

        如果此类型与给定类型相同，则该函数应返回True；该类型通常反映在数据库中，因此应该是数据库特定的。使用的方言也通过了。它也可以返回False来声明该类型不相同。

        参数：

        -   **dialect**[¶](#sqlalchemy.types.TypeDecorator.compare_against_backend.params.dialect)
            – a [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
            that is involved in the comparison.
        -   **conn\_type**
            [¶](#sqlalchemy.types.TypeDecorator.compare_against_backend.params.conn_type)
            - 从后端反射的类型对象。

        版本1.0.3中的新功能

    `比较值`{.descname} （ *x*，*y* ） [¶](#sqlalchemy.types.TypeDecorator.compare_values "Permalink to this definition")
    :   给定两个值，比较他们的平等。

        默认情况下，这会调用基础“impl”的[`TypeEngine.compare_values()`](type_api.html#sqlalchemy.types.TypeEngine.compare_values "sqlalchemy.types.TypeEngine.compare_values")，后者通常使用Python等号运算符`==`。

        ORM使用该函数将原始加载的值与截获的“已更改”值进行比较，以确定是否发生了净更改。

    `编译 T0> （ T1> 方言=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`compile()`](type_api.html#sqlalchemy.types.TypeEngine.compile "sqlalchemy.types.TypeEngine.compile")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        生成此[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")的字符串编译形式。

        当不带参数调用时，使用“默认”方言产生字符串结果。

        参数：

        **dialect**
        [¶](#sqlalchemy.types.TypeDecorator.compile.params.dialect) - a
        [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")实例。

    `复制 T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   生成此[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")实例的副本。

        这是一个浅层副本，用于履行[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")合约的一部分。通常不需要重写，除非用户定义的[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")具有应该被深度复制的本地状态。

    ` dialect_impl  T0> （ T1> 方言 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`dialect_impl()`](type_api.html#sqlalchemy.types.TypeEngine.dialect_impl "sqlalchemy.types.TypeEngine.dialect_impl")
        *[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")*

        返回该[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")的特定于方言的实现。

    ` evaluates_none  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`evaluates_none()`](type_api.html#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        返回将[`should_evaluate_none`](type_api.html#sqlalchemy.types.TypeEngine.should_evaluate_none "sqlalchemy.types.TypeEngine.should_evaluate_none")标志设置为True的此类型的副本。

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

        [`TypeEngine.should_evaluate_none`](type_api.html#sqlalchemy.types.TypeEngine.should_evaluate_none "sqlalchemy.types.TypeEngine.should_evaluate_none")
        - class-level flag

    ` get_dbapi_type  T0> （ T1>  DBAPI  T2> ） T3> ¶ T4>`{.descname}
    :   返回由[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")表示的DBAPI类型对象。

        默认情况下，这会调用基础“impl”的[`TypeEngine.get_dbapi_type()`](type_api.html#sqlalchemy.types.TypeEngine.get_dbapi_type "sqlalchemy.types.TypeEngine.get_dbapi_type")。

    ` literal_processor  T0> （ T1> 方言 T2> ） T3> ¶ T4>`{.descname}
    :   为给定的[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")提供文字处理功能。

        此处的子类通常会覆盖[`TypeDecorator.process_literal_param()`](#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")，而不是直接使用此方法。

        默认情况下，如果实现了该方法，则此方法使用[`TypeDecorator.process_bind_param()`](#sqlalchemy.types.TypeDecorator.process_bind_param "sqlalchemy.types.TypeDecorator.process_bind_param")，其中[`TypeDecorator.process_literal_param()`](#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")不是。The
        rationale here is that [`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
        typically deals with Python conversions of data that are above
        the layer of database presentation. With the value converted by
        [`TypeDecorator.process_bind_param()`](#sqlalchemy.types.TypeDecorator.process_bind_param "sqlalchemy.types.TypeDecorator.process_bind_param"),
        the underlying type will then handle whether it needs to be
        presented to the DBAPI as a bound parameter or to the database
        as an inline SQL value.

        版本0.9.0中的新功能

    ` load_dialect_impl  T0> （ T1> 方言 T2> ） T3> ¶ T4>`{.descname}
    :   返回与方言对应的[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")对象。

        这是一个最终用户覆盖挂钩，可以根据给定的方言用于提供不同的类型。它由[`type_engine()`](#sqlalchemy.types.TypeDecorator.type_engine "sqlalchemy.types.TypeDecorator.type_engine")的[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")实现使用，以帮助确定最终返回给定[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")的类型。

        默认返回`self.impl`。

     `process_bind_param`{.descname}(*value*, *dialect*)[¶](#sqlalchemy.types.TypeDecorator.process_bind_param "Permalink to this definition")
    :   接收要转换的绑定参数值。

        子类重写此方法以返回应传递给底层[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")对象的值，并从那里返回到DBAPI
        `execute()`方法。

        该操作可以是执行自定义行为所需的任何操作，例如转换或序列化数据。这也可以用作验证逻辑的钩子。

        这个操作的设计应考虑到相反的操作，这将是该类的process\_result\_value方法。

        参数：

        -   **value**[¶](#sqlalchemy.types.TypeDecorator.process_bind_param.params.value)
            – Data to operate upon, of any type expected by this method
            in the subclass. 可以是`None`。
        -   **dialect**[¶](#sqlalchemy.types.TypeDecorator.process_bind_param.params.dialect)
            – the [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
            in use.

     `process_literal_param`{.descname}(*value*, *dialect*)[¶](#sqlalchemy.types.TypeDecorator.process_literal_param "Permalink to this definition")
    :   接收要在语句中内联呈现的文字参数值。

        编译器在不使用绑定的情况下呈现文字值时，使用此方法，通常位于DDL中，例如列的“服务器默认值”或CHECK约束内的表达式。

        返回的字符串将被渲染到输出字符串中。

        版本0.9.0中的新功能

     `process_result_value`{.descname}(*value*, *dialect*)[¶](#sqlalchemy.types.TypeDecorator.process_result_value "Permalink to this definition")
    :   接收要转换的结果行列值。

        子类应实现此方法以对从数据库获取的数据进行操作。

        给定一个已由底层[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")对象处理的值，最初来自DBAPI游标方法`fetchone()`

        该操作可以是执行自定义行为所需的任何操作，例如转换或序列化数据。这也可以用作验证逻辑的钩子。

        参数：

        -   **value**[¶](#sqlalchemy.types.TypeDecorator.process_result_value.params.value)
            – Data to operate upon, of any type expected by this method
            in the subclass. 可以是`None`。
        -   **dialect**[¶](#sqlalchemy.types.TypeDecorator.process_result_value.params.dialect)
            – the [`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")
            in use.

        这个操作应该被设计成可以通过这个类的“process\_bind\_param”方法来反转。

    ` python_type  T0> ¶ T1>`{.descname}
    :   *inherited from the* [`python_type`](type_api.html#sqlalchemy.types.TypeEngine.python_type "sqlalchemy.types.TypeEngine.python_type")
        *attribute of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        如果已知，则返回预期由此类型的实例返回的Python类型对象。

        基本上，对于那些强制执行返回类型的类型，或者在所有常见DBAPI（例如`int`）中都可以这样做的类型，将返回该类型。

        如果未定义返回类型，则引发`NotImplementedError`。

        请注意，任何类型也可以在SQL中容纳NULL，这意味着您在实践中也可以从任何类型获取`None`。

    `result_processor`{.descname} （ *dialect*，*coltype* ） [¶](#sqlalchemy.types.TypeDecorator.result_processor "Permalink to this definition")
    :   为给定的[`Dialect`](internals.html#sqlalchemy.engine.interfaces.Dialect "sqlalchemy.engine.interfaces.Dialect")提供结果值处理功能。

        这是实现结果值转换的[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")合同的方法。[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
        will wrap a user-defined implementation of
        [`process_result_value()`](#sqlalchemy.types.TypeDecorator.process_result_value "sqlalchemy.types.TypeDecorator.process_result_value")
        here.

        用户定义的代码可以直接覆盖此方法，尽管它最好使用[`process_result_value()`](#sqlalchemy.types.TypeDecorator.process_result_value "sqlalchemy.types.TypeDecorator.process_result_value")，以保持由`self.impl`提供的处理。

        参数：

        -   **dialect**
            [¶](#sqlalchemy.types.TypeDecorator.result_processor.params.dialect)
            - Dialect实例正在使用中。
        -   **coltype**
            [¶](#sqlalchemy.types.TypeDecorator.result_processor.params.coltype)
            - SQLAlchemy数据类型

        此方法与此类的[`bind_processor()`](#sqlalchemy.types.TypeDecorator.bind_processor "sqlalchemy.types.TypeDecorator.bind_processor")方法相反。

     `type_engine`{.descname}(*dialect*)[¶](#sqlalchemy.types.TypeDecorator.type_engine "Permalink to this definition")
    :   为[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")返回一个特定于方言的[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")实例。

        在大多数情况下，这返回由`self.impl`表示的[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")类型的方言适应形式。使用[`dialect_impl()`](#sqlalchemy.types.TypeDecorator.dialect_impl "sqlalchemy.types.TypeDecorator.dialect_impl")，但也遍历包装的[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")实例。行为可以通过覆盖[`load_dialect_impl()`](#sqlalchemy.types.TypeDecorator.load_dialect_impl "sqlalchemy.types.TypeDecorator.load_dialect_impl")来定制。

    `with_variant`{.descname} （ *type\_*，*dialect\_name* ） [](#sqlalchemy.types.TypeDecorator.with_variant "Permalink to this definition")
    :   *inherited from the* [`with_variant()`](type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
        *method of* [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        生成一个新的类型对象，将其应用于给定名称的方言时使用给定的类型。

        例如。：

            from sqlalchemy.types import String
            from sqlalchemy.dialects import mysql

            s = String()

            s = s.with_variant(mysql.VARCHAR(collation='foo'), 'mysql')

        [`TypeEngine.with_variant()`](type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")的构造始终是从“fallback”类型到特定于方言的。返回的类型是[`Variant`](type_api.html#sqlalchemy.types.Variant "sqlalchemy.types.Variant")的一个实例，它本身提供了一个可重复调用的`Variant.with_variant()`。

        参数：

        -   **type\_**[¶](#sqlalchemy.types.TypeDecorator.with_variant.params.type_)
            – a [`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
            that will be selected as a variant from the originating
            type, when a dialect of the given name is in use.
        -   **dialect\_name**[¶](#sqlalchemy.types.TypeDecorator.with_variant.params.dialect_name)
            – base name of the dialect which uses this type.
            （即`'postgresql'`，`'mysql'`等）

        New in version 0.7.2.

TypeDecorator Recipes [¶](#typedecorator-recipes "Permalink to this headline")
------------------------------------------------------------------------------

接下来几个关键的[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")食谱。

### 将编码字符串强制为Unicode [¶](#coercing-encoded-strings-to-unicode "Permalink to this headline")

A common source of confusion regarding the [`Unicode`](type_basics.html#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
type is that it is intended to deal *only* with Python
`unicode` objects on the Python side, meaning values
passed to it as bind parameters must be of the form
`u'some string'` if using Python 2 and not 3.
它执行的编码/解码功能仅适用于正在使用的DBAPI，并且主要是私有实现细节。

The use case of a type that can safely receive Python bytestrings, that
is strings that contain non-ASCII characters and are not `u''` objects in Python 2, can be achieved using a
[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
which coerces as needed:

    from sqlalchemy.types import TypeDecorator, Unicodeplain

    class CoerceUTF8(TypeDecorator):
        """Safely coerce Python bytestrings to Unicode
        before passing off to the database."""

        impl = Unicode

        def process_bind_param(self, value, dialect):
            if isinstance(value, str):
                value = value.decode('utf-8')
            return value

### 舍入数字[¶](#rounding-numerics "Permalink to this headline")

某些数据库连接器（如 SQL
Server 的数据库连接器）会在小数位数过多的情况下传递 Decimal。这是一个让他们满意的食谱：

    from sqlalchemy.types import TypeDecorator, Numeric
    from decimal import Decimal

    class SafeNumeric(TypeDecorator):
        """Adds quantization to Numeric."""

        impl = Numeric

        def __init__(self, *arg, **kw):
            TypeDecorator.__init__(self, *arg, **kw)
            self.quantize_int = - self.impl.scale
            self.quantize = Decimal(10) ** self.quantize_int

        def process_bind_param(self, value, dialect):
            if isinstance(value, Decimal) and \
                value.as_tuple()[2] < self.quantize_int:
                value = value.quantize(self.quantize)
            return value

### 后端不可知的 GUID 类型[¶](#backend-agnostic-guid-type "Permalink to this headline")

接收并返回 Python
uuid()对象。在其他后端使用 Postgresql，CHAR（32）时使用 PG
UUID 类型，并以字符串化的十六进制格式存储它们。如果需要，可以修改以在 CHAR（16）中存储二进制文件：

    from sqlalchemy.types import TypeDecorator, CHAR
    from sqlalchemy.dialects.postgresql import UUID
    import uuid

    class GUID(TypeDecorator):
        """Platform-independent GUID type.

        Uses Postgresql's UUID type, otherwise uses
        CHAR(32), storing as stringified hex values.

        """
        impl = CHAR

        def load_dialect_impl(self, dialect):
            if dialect.name == 'postgresql':
                return dialect.type_descriptor(UUID())
            else:
                return dialect.type_descriptor(CHAR(32))

        def process_bind_param(self, value, dialect):
            if value is None:
                return value
            elif dialect.name == 'postgresql':
                return str(value)
            else:
                if not isinstance(value, uuid.UUID):
                    return "%.32x" % uuid.UUID(value).int
                else:
                    # hexstring
                    return "%.32x" % value.int

        def process_result_value(self, value, dialect):
            if value is None:
                return value
            else:
                return uuid.UUID(value)

### Marshal JSON字符串[¶](#marshal-json-strings "Permalink to this headline")

这种类型使用`simplejson`将 Python 数据结构封送到/来自 JSON。可以修改为使用 Python 的内置 json 编码器：

    from sqlalchemy.types import TypeDecorator, VARCHAR
    import json

    class JSONEncodedDict(TypeDecorator):
        """Represents an immutable structure as a json-encoded string.

        Usage::

            JSONEncodedDict(255)

        """

        impl = VARCHAR

        def process_bind_param(self, value, dialect):
            if value is not None:
                value = json.dumps(value)

            return value

        def process_result_value(self, value, dialect):
            if value is not None:
                value = json.loads(value)
            return value

请注意，默认情况下，ORM 不会检测到这种类型的“可变性” -
这意味着，就地更改值不会被检测到，也不会被刷新。如果没有进一步的步骤，您需要用每个父对象上的新值替换现有值以检测更改。请注意，这没有什么问题，因为许多应用程序可能不需要一旦创建值就会发生变化。对于那些确实有此要求的用户，最好使用`sqlalchemy.ext.mutable`扩展名应用对可变性的支持 - 请参阅[Mutation
Tracking](orm_extensions_mutable.html)中的示例。

替换现有类型的绑定/结果处理[¶](#replacing-the-bind-result-processing-of-existing-types "Permalink to this headline")
--------------------------------------------------------------------------------------------------------------------

使用[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")实现绑定/结果级别的大部分类型行为增强。对于需要替换由 SQLAlchemy 在 DBAPI 级别应用的特定处理的罕见场景，可以直接对 SQLAlchemy 类型进行子类化，并且`bind_processor()`或`result_processor()`这样做需要重写`adapt()`方法。此方法是 SQLAlchemy 在执行语句期间生成特定于 DBAPI 的类型行为的机制。覆盖它可以使用自定义类型的副本来代替 DBAPI 特定的类型。下面我们将[`types.TIME`](type_basics.html#sqlalchemy.types.TIME "sqlalchemy.types.TIME")类型进行子类化以具有自定义结果处理行为。`process()`函数将直接从 DBAPI 游标接收`value`：

    class MySpecialTime(TIME):plain
        def __init__(self, special_argument):
            super(MySpecialTime, self).__init__()
            self.special_argument = special_argument

        def result_processor(self, dialect, coltype):
            import datetime
            time = datetime.time
            def process(value):
                if value is not None:
                    microseconds = value.microseconds
                    seconds = value.seconds
                    minutes = seconds / 60
                    return time(
                              minutes / 60,
                              minutes % 60,
                              seconds - minutes * 60,
                              microseconds)
                else:
                    return None
            return process

        def adapt(self, impltype):
            return MySpecialTime(self.special_argument)

应用 SQL 级绑定/结果处理[¶](#applying-sql-level-bind-result-processing "Permalink to this headline")
--------------------------------------------------------------------------------------------------

如在[Augmenting Existing Types](#types-typedecorator)和[Replacing the
Bind/Result Processing of Existing
Types](#replacing-processors)部分所见，SQLAlchemy 允许在将参数发送到语句时调用 Python 函数，如以及从数据库加载结果行时，以及在将数据发送到数据库或从数据库发送时对其应用转换。也可以定义 SQL 级别的转换。这里的基本原理是，只有关系数据库包含一系列必要的功能，才能在应用程序和持久性格式之间强制传入和传出数据。例子包括使用数据库定义的加密/解密函数，以及处理地理数据的存储过程。Postgis 对 Postgresql 的扩展包括一系列 SQL 函数，这些函数是将数据强制转换为特定格式所必需的。

任何[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")，[`UserDefinedType`](#sqlalchemy.types.UserDefinedType "sqlalchemy.types.UserDefinedType")或[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")子类都可以包含[`TypeEngine.bind_expression()`](type_api.html#sqlalchemy.types.TypeEngine.bind_expression "sqlalchemy.types.TypeEngine.bind_expression")和/或[`TypeEngine.column_expression()`](type_api.html#sqlalchemy.types.TypeEngine.column_expression "sqlalchemy.types.TypeEngine.column_expression")，当定义为返回非`None`值时，应返回要注入 SQL 语句的[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")表达式，参数或列表达式。例如，要构建将所有传入数据应用于 Postgis 函数`ST_GeomFromText`的所有传出值和函数`ST_AsText`的`Geometry`类型，我们可以创建我们自己的[`UserDefinedType`](#sqlalchemy.types.UserDefinedType "sqlalchemy.types.UserDefinedType")的子类，它提供这些方法与[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")结合使用：

    from sqlalchemy import func
    from sqlalchemy.types import UserDefinedType

    class Geometry(UserDefinedType):
        def get_col_spec(self):
            return "GEOMETRY"

        def bind_expression(self, bindvalue):
            return func.ST_GeomFromText(bindvalue, type_=self)

        def column_expression(self, col):
            return func.ST_AsText(col, type_=self)

我们可以将`Geometry`类型应用到[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")元数据中，并将其用于[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构中：

    geometry = Table('geometry', metadata,
                  Column('geom_id', Integer, primary_key=True),
                  Column('geom_data', Geometry)
                )

    print(select([geometry]).where(
      geometry.c.geom_data == 'LINESTRING(189412 252431,189631 259122)'))

结果 SQL 根据需要嵌入两个函数。`ST_AsText` is applied
to the columns clause so that the return value is run through the
function before passing into a result set, and
`ST_GeomFromText` is run on the bound parameter so
that the passed-in value is converted:

    SELECT geometry.geom_id, ST_AsText(geometry.geom_data) AS geom_data_1
    FROM geometry
    WHERE geometry.geom_data = ST_GeomFromText(:geom_data_2)

The [`TypeEngine.column_expression()`](type_api.html#sqlalchemy.types.TypeEngine.column_expression "sqlalchemy.types.TypeEngine.column_expression")
method interacts with the mechanics of the compiler such that the SQL
expression does not interfere with the labeling of the wrapped
expression. 例如，如果我们针对表达式的[`label()`](sqlelement.html#sqlalchemy.sql.expression.label "sqlalchemy.sql.expression.label")呈现[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")，则将字符串标签移动到包装表达式的外部：

    print(select([geometry.c.geom_data.label('my_data')]))plain

输出：

    SELECT ST_AsText(geometry.geom_data) AS my_dataplain
    FROM geometry

对于直接对内置类型进行子类化的示例，我们继承[`postgresql.BYTEA`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.BYTEA "sqlalchemy.dialects.postgresql.BYTEA")以提供一个`PGPString`，它将利用 Postgresql `pgcrypto`透明地扩展到 encrpyt /解密值：

    from sqlalchemy import create_engine, String, select, func, \plain
            MetaData, Table, Column, type_coerce

    from sqlalchemy.dialects.postgresql import BYTEA

    class PGPString(BYTEA):
        def __init__(self, passphrase, length=None):
            super(PGPString, self).__init__(length)
            self.passphrase = passphrase

        def bind_expression(self, bindvalue):
            # convert the bind's type from PGPString to
            # String, so that it's passed to psycopg2 as is without
            # a dbapi.Binary wrapper
            bindvalue = type_coerce(bindvalue, String)
            return func.pgp_sym_encrypt(bindvalue, self.passphrase)

        def column_expression(self, col):
            return func.pgp_sym_decrypt(col, self.passphrase)

    metadata = MetaData()
    message = Table('message', metadata,
                    Column('username', String(50)),
                    Column('message',
                        PGPString("this is my passphrase", length=1000)),
                )

    engine = create_engine("postgresql://scott:tiger@localhost/test", echo=True)
    with engine.begin() as conn:
        metadata.create_all(conn)

        conn.execute(message.insert(), username="some user",
                                    message="this is my message")

        print(conn.scalar(
                select([message.c.message]).\
                    where(message.c.username == "some user")
            ))

`pgp_sym_encrypt`和`pgp_sym_decrypt`函数应用于 INSERT 和 SELECT 语句：

    INSERT INTO message (username, message)
      VALUES (%(username)s, pgp_sym_encrypt(%(message)s, %(pgp_sym_encrypt_1)s))
      {'username': 'some user', 'message': 'this is my message',
        'pgp_sym_encrypt_1': 'this is my passphrase'}

    SELECT pgp_sym_decrypt(message.message, %(pgp_sym_decrypt_1)s) AS message_1
      FROM message
      WHERE message.username = %(username_1)s
      {'pgp_sym_decrypt_1': 'this is my passphrase', 'username_1': 'some user'}

0.8版新增：添加了[`TypeEngine.bind_expression()`](type_api.html#sqlalchemy.types.TypeEngine.bind_expression "sqlalchemy.types.TypeEngine.bind_expression")和[`TypeEngine.column_expression()`](type_api.html#sqlalchemy.types.TypeEngine.column_expression "sqlalchemy.types.TypeEngine.column_expression")方法。

也可以看看：

[PostGIS Integration](orm_examples.html#examples-postgis)

重新定义和创建新操作符[¶](#redefining-and-creating-new-operators "Permalink to this headline")
----------------------------------------------------------------------------------------------

SQLAlchemy Core 定义了一组可用于所有列表达式的表达式运算符。Some of these
operations have the effect of overloading Python’s built in operators;
examples of such operators include [`ColumnOperators.__eq__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")
(`table.c.somecolumn == 'foo'`),
[`ColumnOperators.__invert__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__invert__ "sqlalchemy.sql.operators.ColumnOperators.__invert__")
(`~table.c.flag`), and
[`ColumnOperators.__add__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__add__ "sqlalchemy.sql.operators.ColumnOperators.__add__")
(`table.c.x + table.c.y`). Other operators are
exposed as explicit methods on column expressions, such as
[`ColumnOperators.in_()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
(`table.c.value.in_(['x', 'y'])`) and
[`ColumnOperators.like()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
(`table.c.value.like('%ed%')`).

在所有情况下，Core表达式结构都会查询表达式的类型，以确定现有运算符的行为，并找出不属于内置集合的其他运算符。The
[`TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
base class defines a root “comparison” implementation
[`TypeEngine.Comparator`](type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator"),
and many specific types provide their own sub-implementations of this
class. 用户定义的[`TypeEngine.Comparator`](type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")实现可以直接构建到特定类型的简单子类中，以覆盖或定义新的操作。下面，我们创建一个覆盖[`ColumnOperators.__add__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__add__ "sqlalchemy.sql.operators.ColumnOperators.__add__")运算符的[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")子类。

    from sqlalchemy import Integerplain

    class MyInt(Integer):
        class comparator_factory(Integer.Comparator):
            def __add__(self, other):
                return self.op("goofy")(other)

上面的配置创建了一个新的类`MyInt`，它将[`TypeEngine.comparator_factory`](type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")属性建立为引用新的类，继承[`TypeEngine.Comparator`](type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")类的子类与[`Integer`](type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")类型相关联。

用法：

    >>> sometable = Table("sometable", metadata, Column("data", MyInt))plain
    >>> print(sometable.c.data + 5)
    sometable.data goofy :data_1

通过将[`TypeEngine.Comparator`](type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")自身实例化为`expr`属性，通过拥有的 SQL 表达式查阅[`ColumnOperators.__add__()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__add__ "sqlalchemy.sql.operators.ColumnOperators.__add__")的实现。表达式系统的机制是这样的，即操作继续递归直到表达式对象产生一个新的 SQL 表达式结构。Above,
we could just as well have said `self.expr.op("goofy")(other)` instead of `self.op("goofy")(other)`.

New methods added to a [`TypeEngine.Comparator`](type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")
are exposed on an owning SQL expression using a `__getattr__` scheme, which exposes methods added to
[`TypeEngine.Comparator`](type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")
onto the owning [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement").
例如，要将`log()`函数添加到整数：

    from sqlalchemy import Integer, funcplain

    class MyInt(Integer):
        class comparator_factory(Integer.Comparator):
            def log(self, other):
                return func.log(self.expr, other)

使用以上类型：

    >>> print(sometable.c.data.log(5))
    log(:log_1, :log_2)

一元操作也是可能的。例如，要添加 Postgresql 阶乘运算符的实现，我们将[`UnaryExpression`](sqlelement.html#sqlalchemy.sql.expression.UnaryExpression "sqlalchemy.sql.expression.UnaryExpression")结构与[`custom_op`](sqlelement.html#sqlalchemy.sql.operators.custom_op "sqlalchemy.sql.operators.custom_op")结合起来以产生阶乘表达式：

    from sqlalchemy import Integerplainplain
    from sqlalchemy.sql.expression import UnaryExpression
    from sqlalchemy.sql import operators

    class MyInteger(Integer):
        class comparator_factory(Integer.Comparator):
            def factorial(self):
                return UnaryExpression(self.expr,
                            modifier=operators.custom_op("!"),
                            type_=MyInteger)

使用以上类型：

    >>> from sqlalchemy.sql import columnplain
    >>> print(column('x', MyInteger).factorial())
    x !

也可以看看：

[`TypeEngine.comparator_factory`](type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")

0.8版新增功能：增强了表达式系统，支持按类型级别定制运算符。

创建新类型[¶](#creating-new-types "Permalink to this headline")
---------------------------------------------------------------

The [`UserDefinedType`](#sqlalchemy.types.UserDefinedType "sqlalchemy.types.UserDefinedType")
class is provided as a simple base class for defining entirely new
database types.
用它来表示 SQLAlchemy 不知道的本地数据库类型。如果只需要 Python 翻译行为，请改用[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")。

*class* `sqlalchemy.types。`{.descclassname} `UserDefinedType`{.descname} [¶](#sqlalchemy.types.UserDefinedType "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    用户定义类型的基础。

    这应该是新类型的基础。请注意，对于大多数情况，[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")可能更合适：

        import sqlalchemy.types as types

        class MyType(types.UserDefinedType):
            def __init__(self, precision = 8):
                self.precision = precision

            def get_col_spec(self, **kw):
                return "MYTYPE(%s)" % self.precision

            def bind_processor(self, dialect):
                def process(value):
                    return value
                return process

            def result_processor(self, dialect, coltype):
                def process(value):
                    return value
                return process

    一旦这个类型被创建，它就可以立即使用：

        table = Table('foo', meta,
            Column('id', Integer, primary_key=True),
            Column('data', MyType(16))
            )

    The `get_col_spec()` method will in most cases
    receive a keyword argument `type_expression`
    which refers to the owning expression of the type as being compiled,
    such as a [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    or [`cast()`](sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")
    construct.
    只有当方法接受其参数签名中的关键字参数（例如`**kw`）时才会发送此关键字；内省是用来检查这个以支持这个功能的遗留形式。

    版本1.0.0新增：拥有的表达式通过关键字参数`type_expression`传递给`get_col_spec()`方法，如果它接收到`**kw`签名。

    `coerce_compared_value`{.descname} （ *op*，*值* ） [](#sqlalchemy.types.UserDefinedType.coerce_compared_value "Permalink to this definition")
    :   为表达式中的'强制'Python值建议类型。

        [`UserDefinedType`](#sqlalchemy.types.UserDefinedType "sqlalchemy.types.UserDefinedType")的默认行为与[`TypeDecorator`](#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")的默认行为相同。默认情况下它会返回`self`，假设比较值应该强制为与此类型相同的类型。有关更多详细信息，请参阅[`TypeDecorator.coerce_compared_value()`](#sqlalchemy.types.TypeDecorator.coerce_compared_value "sqlalchemy.types.TypeDecorator.coerce_compared_value")。

        在版本0.8中改变：
        [`UserDefinedType.coerce_compared_value()`](#sqlalchemy.types.UserDefinedType.coerce_compared_value "sqlalchemy.types.UserDefinedType.coerce_compared_value")现在默认返回`self`，而不是落在[`TypeEngine.coerce_compared_value()`](type_api.html#sqlalchemy.types.TypeEngine.coerce_compared_value "sqlalchemy.types.TypeEngine.coerce_compared_value")


