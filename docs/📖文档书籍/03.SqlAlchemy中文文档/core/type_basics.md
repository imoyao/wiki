---
title: 列和数据类型
date: 2021-02-20 22:41:37
permalink: /sqlalchemy/core/type_basics/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
列和数据类型[¶](#module-sqlalchemy.types "Permalink to this headline")
======================================================================

SQLAlchemy 为大多数常用数据库数据类型提供了抽象，并提供了一种用于指定自己的自定义数据类型的机制。

类型对象的方法和属性很少直接使用。Type 对象提供给[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")定义，对于数据库驱动程序返回不正确类型的场合，可以作为类型提示提供给 functions。

    >>> users = Table('users', metadata,
    ...               Column('id', Integer, primary_key=True)
    ...               Column('login', String(32))
    ...              )

SQLAlchemy 在发布`CREATE TABLE时将使用Integer`和`String(32)`
t4\>语句，并在从数据库读回行`SELECTed`时再次使用它。接受类型的函数（比如[`Column()`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")）通常会接受一个类型类或实例；
`Integer`相当于`Integer()`，在这种情况下没有构造参数。

泛型类型[¶](#generic-types "Permalink to this headline")
--------------------------------------------------------

泛型类型指定一个可以读取，写入和存储特定类型的 Python 数据的列。发布`CREATE TABLE`语句时，SQLAlchemy 将选择目标数据库上可用的最佳数据库列类型。为了完全控制哪些列类型在`CREATE TABLE`中发出，例如`VARCHAR`，请参阅[\`SQL
Standard Types\`\_](#id1)和本章的其他部分。

*class* `sqlalchemy.types。`{.descclassname} `BigInteger`{.descname} [¶](#sqlalchemy.types.BigInteger "Permalink to this definition")
:   基础：[`sqlalchemy.types.Integer`](#sqlalchemy.types.Integer "sqlalchemy.types.Integer")

    更大的`int`整数的类型。plain

    通常在DDL中生成一个`BIGINT`，否则就像Python端的普通[`Integer`](#sqlalchemy.types.Integer "sqlalchemy.types.Integer")一样。

*class* `sqlalchemy.types。`{.descclassname} `布尔`{.descname} （ *create\_constraint = True*，*名称=无*，*\_create\_events = True ） [¶](#sqlalchemy.types.Boolean "Permalink to this definition")*
:   基础：[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")，[`sqlalchemy.types.SchemaType`](#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")

    一个bool数据类型。plainplain

    布尔值通常在DDL端使用BOOLEAN或SMALLINT，而在Python端则使用`True`或`False`。

    `__ init __`{.descname} （ *create\_constraint = True*，*name =无*，*\_create\_events = True* ） T5\> [¶ T6\>](#sqlalchemy.types.Boolean.__init__ "Permalink to this definition")
    :   构造一个布尔值。

        参数：

        -   **create\_constraint**
            [¶](#sqlalchemy.types.Boolean.params.create_constraint) -
            默认为True。如果布尔值是作为int /
            smallint生成的，那么还要在表上创建CHECK约束，以确保1或0作为值。
        -   **name**[¶](#sqlalchemy.types.Boolean.params.name) – if a
            CHECK constraint is generated, specify the name of the
            constraint.

 *class*`sqlalchemy.types.`{.descclassname}`Date`{.descname}[¶](#sqlalchemy.types.Date "Permalink to this definition")
:   基础：`sqlalchemy.types._DateAffinity`，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    `datetime.date()`对象的类型。plain

*class* `sqlalchemy.types。`{.descclassname} `DateTime`{.descname} （ *timezone = False* / T5\> [¶ T6\>](#sqlalchemy.types.DateTime "Permalink to this definition")
:   基础：`sqlalchemy.types._DateAffinity`，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    `datetime.datetime()`对象的类型。plain

    日期和时间类型从Python `datetime`模块返回对象。大多数DBAPI都支持datetime模块，除了SQLite之外。对于SQLite，日期和时间类型存储为字符串，然后在返回行时将其转换回日期时间对象。

    ` __初始化__  T0> （ T1> 时区=假 T2> ） T3> ¶ T4>`{.descname}
    :   构建一个新的[`DateTime`](#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")。

        参数：

        **时区** [¶](#sqlalchemy.types.DateTime.params.timezone) -
        布尔值。如果为True，并由后端支持，则会产生'TIMESTAMP WITH
        TIMEZONE'。对于不支持时区感知时间戳的后端，不起作用。

*class* `sqlalchemy.types。`{.descclassname} `Enum`{.descname} （ *\* enums*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.types.Enum "Permalink to this definition")*
:   基础：[`sqlalchemy.types.String`](#sqlalchemy.types.String "sqlalchemy.types.String")，[`sqlalchemy.types.SchemaType`](#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")

    通用枚举类型。

    [`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型提供了该列所限制的一组可能的字符串值。

    如果可用的话，[`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型将使用后端的本机“ENUM”类型；否则，它使用VARCHAR数据类型并生成CHECK约束。可以使用[`Enum.native_enum`](#sqlalchemy.types.Enum.params.native_enum "sqlalchemy.types.Enum")标志禁用后端本机枚举类型，并且可以使用[`Enum.create_constraint`](#sqlalchemy.types.Enum.params.create_constraint "sqlalchemy.types.Enum")标志配置CHECK约束的生成。

    [`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型还提供对输入值和数据库返回值的Python验证。对于任何不在可能值的给定列表中的Python值，都会引发`LookupError`。

    在版本1.1中更改：现在，[`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型提供输入值的Python验证以及数据库返回的数据。

    枚举值的来源可能是字符串值列表，或者是符合PEP-435标准的枚举类。对于[`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")数据类型，这个类只需要提供一个`__members__`方法。

    在使用枚举类时，枚举对象既用于输入又用于输出，而不是像普通字符串枚举类型那样使用字符串：

        import enum
        class MyEnum(enum.Enum):
            one = "one"
            two = "two"
            three = "three"


        t = Table(
            'data', MetaData(),
            Column('value', Enum(MyEnum))
        )

        connection.execute(t.insert(), {"value": MyEnum.two})
        assert connection.scalar(t.select()) is MyEnum.two

    版本1.1中的新功能： - 支持PEP-435风格的枚举类。

    也可以看看

    [`ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
    - 特定于PostgreSQL的类型，它具有附加功能。

    `__ init __`{.descname} （ *\* enums*，*\*\* kw* ） [T5\>](#sqlalchemy.types.Enum.__init__ "Permalink to this definition")
    :   构造一个枚举。

        不适用于特定后端的关键字参数将被该后端忽略。

        参数：

        -   **\* enums** [¶](#sqlalchemy.types.Enum.params.*enums) -

            或者只有一个符合PEP-435的枚举类型或一个或多个字符串或unicode枚举标签。如果存在unicode标签，则会自动启用convert\_unicode标志。

            版本1.1中的新功能：可以传递PEP-435风格的枚举类。

        -   **convert\_unicode**[¶](#sqlalchemy.types.Enum.params.convert_unicode)
            – Enable unicode-aware bind parameter and result-set
            processing for this Enum’s data.
            这是根据unicode标签字符串的存在自动设置的。
        -   **create\_constraint**
            [¶](#sqlalchemy.types.Enum.params.create_constraint) -

            默认为True。在创建非本机枚举类型时，还要根据有效值在数据库上构建一个CHECK约束。

            版本1.1中的新增功能： -
            添加了[`Enum.create_constraint`](#sqlalchemy.types.Enum.params.create_constraint "sqlalchemy.types.Enum")，它提供了禁止为非本机枚举类型生成CHECK约束的选项。

        -   **metadata**[¶](#sqlalchemy.types.Enum.params.metadata) –
            Associate this type directly with a `MetaData` object.
            对于作为独立模式构造（Postgresql）存在于目标数据库上的类型，将在`create_all()`和`drop_all()`操作中创建并删除此类型。如果该类型与任何`MetaData`对象关联，则它将自己与其使用的每个`Table`相关联，并且将在创建任何单个表时创建，在检查完成后进行检查。但是，只有当为该`Table`对象的元数据调用`drop_all()`时，才会删除该类型。
        -   **名称** [¶](#sqlalchemy.types.Enum.params.name) -
            此类型的名称。这是Postgresql和任何未来支持的数据库所必需的，这些数据库需要显式命名的类型或显式命名的约束才能生成类型和/或使用它的表。如果使用PEP-435枚举类，则默认使用其名称（转换为小写）。
        -   **native\_enum**[¶](#sqlalchemy.types.Enum.params.native_enum)
            – Use the database’s native ENUM type when available.
            默认为True。False时，对所有后端使用VARCHAR +检查约束。
        -   **模式** [¶](#sqlalchemy.types.Enum.params.schema) -

            此类型的架构名称。对于作为独立模式构造（Postgresql）存在于目标数据库上的类型，此参数指定存在类型的命名模式。

            注意

            [`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")类型的`schema`默认不使用在[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")上建立的`schema`。如果需要这种行为，请将`inherit_schema`标志设置为`True`。

        -   **quote**[¶](#sqlalchemy.types.Enum.params.quote) – Set
            explicit quoting preferences for the type’s name.
        -   **inherit\_schema**[¶](#sqlalchemy.types.Enum.params.inherit_schema)
            – When `True`, the “schema” from the
            owning [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            will be copied to the “schema” attribute of this
            [`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum"),
            replacing whatever value was passed for the
            `schema` attribute.
            这在使用[`Table.tometadata()`](metadata.html#sqlalchemy.schema.Table.tometadata "sqlalchemy.schema.Table.tometadata")操作时也会生效。
        -   **validate\_strings**
            [¶](#sqlalchemy.types.Enum.params.validate_strings) -

            当为真时，无效的字符串值将被验证并且不被允许通过。

            版本1.1.0b2中的新功能

     `create`{.descname}(*bind=None*, *checkfirst=False*)[¶](#sqlalchemy.types.Enum.create "Permalink to this definition")
    :   *inherited from the* [`create()`](#sqlalchemy.types.SchemaType.create "sqlalchemy.types.SchemaType.create")
        *method of* [`SchemaType`](#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")

        为此类型发出CREATE ddl（如果适用）。

     `drop`{.descname}(*bind=None*, *checkfirst=False*)[¶](#sqlalchemy.types.Enum.drop "Permalink to this definition")
    :   *inherited from the* [`drop()`](#sqlalchemy.types.SchemaType.drop "sqlalchemy.types.SchemaType.drop")
        *method of* [`SchemaType`](#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")

        为此类型发布DROP ddl（如果适用）。

*class* `sqlalchemy.types。`{.descclassname} `浮动`{.descname} （ *精度=无*，*asdecimal = False*，*decimal\_return\_scale = None*，*\*\* kwargs* ） [¶](#sqlalchemy.types.Float "Permalink to this definition")
:   基础：[`sqlalchemy.types.Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")

    表示浮点类型的类型，例如`FLOAT`或`REAL`。plain

    除非[`Float.asdecimal`](#sqlalchemy.types.Float.params.asdecimal "sqlalchemy.types.Float")标志设置为True，否则这种类型默认返回Python
    `float`对象，在这种情况下，它们被强制转换为`decimal.Decimal`

    注意

    [`Float`](#sqlalchemy.types.Float "sqlalchemy.types.Float")类型用于接收来自明确已知为浮点类型的数据库类型的数据（例如，`FLOAT`，`REAL`，其他）而不是小数类型（例如`DECIMAL`，`NUMERIC`等）。If the database column
    on the server is in fact a Numeric type, such as `DECIMAL` or `NUMERIC`, use the [`Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")
    type or a subclass, otherwise numeric coercion between
    `float`/`Decimal` may or may
    not function as expected.

     `__init__`{.descname}(*precision=None*, *asdecimal=False*, *decimal\_return\_scale=None*, *\*\*kwargs*)[¶](#sqlalchemy.types.Float.__init__ "Permalink to this definition")
    :   构建一个浮动。

        参数：

        -   **precision**[¶](#sqlalchemy.types.Float.params.precision) –
            the numeric precision for use in DDL
            `CREATE TABLE`.
        -   **asdecimal**[¶](#sqlalchemy.types.Float.params.asdecimal) –
            the same flag as that of [`Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric"),
            but defaults to `False`.
            请注意，将此标志设置为`True`会导致浮点转换。
        -   **decimal\_return\_scale**
            [¶](#sqlalchemy.types.Float.params.decimal_return_scale) -

            从float到Python小数转换时使用的默认缩放比例。由于十进制不准确性，浮点值通常会长得多，并且大多数浮点数据库类型没有“缩放”的概念，所以默认情况下，浮点类型在转换时会查找前十个小数位。指定此值将覆盖该长度。请注意，包含“scale”的MySQL浮点类型将使用“scale”作为decimal\_return\_scale的默认值（如果未另外指定）。

            版本0.9.0中的新功能

        -   **\*\* kwargs** [¶](#sqlalchemy.types.Float.params.**kwargs)
            - 不建议使用。其他参数在这里被默认的[`Float`](#sqlalchemy.types.Float "sqlalchemy.types.Float")类型忽略。对于支持附加参数的特定于数据库的浮点数，请参阅该方言的文档以获取详细信息，例如[`sqlalchemy.dialects.mysql.FLOAT`](dialects_mysql.html#sqlalchemy.dialects.mysql.FLOAT "sqlalchemy.dialects.mysql.FLOAT")。

*class* `sqlalchemy.types。`{.descclassname} `整数`{.descname} [¶](#sqlalchemy.types.Integer "Permalink to this definition")
:   基础：`sqlalchemy.types._DateAffinity`，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    一个用于`int`整数的类型。plainplain

 *class*`sqlalchemy.types.`{.descclassname}`Interval`{.descname}(*native=True*, *second\_precision=None*, *day\_precision=None*)[¶](#sqlalchemy.types.Interval "Permalink to this definition")
:   基础：`sqlalchemy.types._DateAffinity`，[`sqlalchemy.types.TypeDecorator`](custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")

    `datetime.timedelta()`对象的类型。plain

    Interval类型处理`datetime.timedelta`对象。在PostgreSQL中，使用本地`INTERVAL`类型；对于其他人而言，价值被存储为相对于“时代”（1970年1月1日）的日期。

    请注意，`Interval`类型当前不在本机不支持间隔类型的平台上提供日期算术运算。这样的操作通常需要将表达式的两侧（例如，首先将两侧转换为整数时间值）进行转换，该转换当前是手动过程（例如通过[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")）。

    `__ init __`{.descname} （ *native = True*，*second\_precision = None*，*day\_precision = None* ） T5\> [¶ T6\>](#sqlalchemy.types.Interval.__init__ "Permalink to this definition")
    :   构造一个Interval对象。

        参数：

        -   **native**[¶](#sqlalchemy.types.Interval.params.native) –
            when True, use the actual INTERVAL type provided by the
            database, if supported (currently Postgresql, Oracle).
            否则，无论如何将间隔数据表示为历元值。
        -   **second\_precision**[¶](#sqlalchemy.types.Interval.params.second_precision)
            – For native interval types which support a “fractional
            seconds precision” parameter, i.e. Oracle and Postgresql
        -   **day\_precision**[¶](#sqlalchemy.types.Interval.params.day_precision)
            – for native interval types which support a “day precision”
            parameter, i.e. Oracle.

    `coerce_compared_value`{.descname} （ *op*，*值* ） [](#sqlalchemy.types.Interval.coerce_compared_value "Permalink to this definition")
    :   有关说明，请参阅[`TypeEngine.coerce_compared_value()`](type_api.html#sqlalchemy.types.TypeEngine.coerce_compared_value "sqlalchemy.types.TypeEngine.coerce_compared_value")。

    ` IMPL  T0> ¶ T1>`{.descname}
    :   [`DateTime`](#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")的别名

*class* `sqlalchemy.types。`{.descclassname} `LargeBinary`{.descname} （ *length = None* / T5\> [¶ T6\>](#sqlalchemy.types.LargeBinary "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    一种大型二进制字节数据的类型。plain

    The [`LargeBinary`](#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")
    type corresponds to a large and/or unlengthed binary type for the
    target platform, such as BLOB on MySQL and BYTEA for Postgresql.
    它还处理DBAPI的必要转换。

    ` __初始化__  T0> （ T1> 长度=无 T2> ） T3> ¶ T4>`{.descname}
    :   构建一个LargeBinary类型。

        参数：

        **length**[¶](#sqlalchemy.types.LargeBinary.params.length) –
        optional, a length for the column for use in DDL statements, for
        those binary types that accept a length, such as the MySQL BLOB
        type.

*class* `sqlalchemy.types。`{.descclassname} `MatchType`{.descname} （ *create\_constraint = True*，*=无*，*\_create\_events = True ） [¶](#sqlalchemy.types.MatchType "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Boolean`](#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")

    指MATCH运算符的返回类型。plain

    As the [`ColumnOperators.match()`](sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
    is probably the most open-ended operator in generic SQLAlchemy Core,
    we can’t assume the return type at SQL evaluation time, as MySQL
    returns a floating point, not a boolean, and other backends might do
    something different.
    所以这个类型作为一个占位符，当前继承[`Boolean`](#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")。该类型允许方言根据需要注入结果处理功能，并在MySQL上返回浮点值。

    版本1.0.0中的新功能

 *class*`sqlalchemy.types.`{.descclassname}`Numeric`{.descname}(*precision=None*, *scale=None*, *decimal\_return\_scale=None*, *asdecimal=True*)[¶](#sqlalchemy.types.Numeric "Permalink to this definition")
:   基础：`sqlalchemy.types._DateAffinity`，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    用于固定精度数字的类型，例如`NUMERIC`或`DECIMAL`。

    除非[`Numeric.asdecimal`](#sqlalchemy.types.Numeric.params.asdecimal "sqlalchemy.types.Numeric")标志设置为False，否则这种类型默认返回Python
    `decimal.Decimal`对象，在这种情况下，它们被强制为Python `float`

    注意

    [`Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")类型用于从明确知道为十进制类型的数据库类型（例如`DECIMAL`，`NUMERIC`等）接收数据。而不是浮点类型（例如`FLOAT`，`REAL`，其他）。如果服务器上的数据库列实际上是浮点类型类型，如`FLOAT`或`REAL`，则使用[`Float`](#sqlalchemy.types.Float "sqlalchemy.types.Float")类型或a子类，否则`float` / `Decimal`之间的数字强制可能会或可能不会按预期运行。

    注意

    Python `decimal.Decimal`类通常运行缓慢； cPython
    3.3现在已经切换到本地使用[cdecimal](http://pypi.python.org/pypi/cdecimal/)库。对于较老的Python版本，可以将`cdecimal`库修补到任何将完全替换`decimal`库的应用程序中，但是这需要全局应用，并且在任何其他模块已被导入，如下所示：

        import sys
        import cdecimal
        sys.modules["decimal"] = cdecimal

    请注意，`cdecimal`和`decimal`库**彼此不兼容**，因此在全局级别修补`cdecimal`它可以有效地用于硬编码导入`decimal`库的各种DBAPI。

     `__init__`{.descname}(*precision=None*, *scale=None*, *decimal\_return\_scale=None*, *asdecimal=True*)[¶](#sqlalchemy.types.Numeric.__init__ "Permalink to this definition")
    :   构建一个数字。

        参数：

        -   **precision**[¶](#sqlalchemy.types.Numeric.params.precision)
            – the numeric precision for use in DDL
            `CREATE TABLE`.
        -   **scale**[¶](#sqlalchemy.types.Numeric.params.scale) – the
            numeric scale for use in DDL `CREATE TABLE`.
        -   **asdecimal**
            [¶](#sqlalchemy.types.Numeric.params.asdecimal) -
            默认为True。返回值是否应该作为Python
            Decimal对象或浮点数发送。不同的DBAPI根据数据类型发送一个或另一个
            - 数字类型将确保返回值是一致的跨DBAPI的一个或另一个。
        -   **decimal\_return\_scale**
            [¶](#sqlalchemy.types.Numeric.params.decimal_return_scale) -

            从float到Python小数转换时使用的默认缩放比例。由于十进制不准确性，浮点值通常会长得多，并且大多数浮点数据库类型没有“缩放”的概念，所以默认情况下，浮点类型在转换时会查找前十个小数位。指定此值将覆盖该长度。包含明确的“.scale”值的类型（如base
            [`Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")以及MySQL浮点类型）将使用“.scale”的值作为decimal\_return\_scale的默认值，否则指定。

            版本0.9.0中的新功能

        当使用`Numeric`类型时，应注意确保asdecimal设置适用于正在使用的DBAPI -
        当Numeric应用从Decimal-\> float或float-\>
        Decimal的转换时，此转换会发生所有结果列的额外性能开销。

        原生返回Decimal的DBAPI（例如psycopg2）的设置为`True`将具有更高的准确性和更高的性能，因为Decimal的本地转换减少了游戏中浮点问题的数量，而Numeric类型本身不需要应用任何进一步的转换。然而，另一个返回本地*浮动的DBAPI会产生额外的转换开销，并且仍然会受到浮点数据丢失的影响
        - 在这种情况下，`asdecimal=False`至少会移除额外的转换开销。*

 *class*`sqlalchemy.types.`{.descclassname}`PickleType`{.descname}(*protocol=2*, *pickler=None*, *comparator=None*)[¶](#sqlalchemy.types.PickleType "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeDecorator`](custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")

    保存使用pickle序列化的Python对象。

    PickleType建立在二进制类型之上，用于将Python的`pickle.dumps()`应用于传入对象，`pickle.loads()`允许任何可选择的Python对象成为存储为一个序列化的二进制字段。

    要允许ORM更改事件传播与[`PickleType`](#sqlalchemy.types.PickleType "sqlalchemy.types.PickleType")关联的元素，请参阅[Mutation
    Tracking](orm_extensions_mutable.html)。

     `__init__`{.descname}(*protocol=2*, *pickler=None*, *comparator=None*)[¶](#sqlalchemy.types.PickleType.__init__ "Permalink to this definition")
    :   构建一个PickleType。

        参数：

        -   **协议** [¶](#sqlalchemy.types.PickleType.params.protocol) -
            默认为`pickle.HIGHEST_PROTOCOL`。
        -   **pickler** [¶](#sqlalchemy.types.PickleType.params.pickler)
            -
            如果cPickle不可用，则默认为cPickle.pickle或pickle.pickle。可以是任何具有pickle兼容性的对象``` dumps` 和 ``loads ```方法。
        -   **comparator**[¶](#sqlalchemy.types.PickleType.params.comparator)
            – a 2-arg callable predicate used to compare values of this
            type. 如果保留为`None`，则使用Python“equals”运算符来比较值。

    ` IMPL  T0> ¶ T1>`{.descname}
    :   [`LargeBinary`](#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")的别名

*class* `sqlalchemy.types。`{.descclassname} `SchemaType`{.descname} （ *name = None*，*= None*，*metadata = None*，*inherit\_schema = False*，*quote =无*，*\_create\_events = True* ） T10\> [¶ T11\>](#sqlalchemy.types.SchemaType "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.SchemaEventTarget`

    将某个类型标记为可能需要使用架构级别的DDL。plainplain

    支持必须显式创建/删除的类型（即PG
    ENUM类型）以及由表或模式级别约束，触发器和其他规则所赞扬的类型。

    [`SchemaType`](#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    classes can also be targets for the
    [`DDLEvents.before_parent_attach()`](events.html#sqlalchemy.events.DDLEvents.before_parent_attach "sqlalchemy.events.DDLEvents.before_parent_attach")
    and [`DDLEvents.after_parent_attach()`](events.html#sqlalchemy.events.DDLEvents.after_parent_attach "sqlalchemy.events.DDLEvents.after_parent_attach")
    events, where the events fire off surrounding the association of the
    type object with a parent [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column").

    也可以看看

    [`Enum`](#sqlalchemy.types.Enum "sqlalchemy.types.Enum")

    [`Boolean`](#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")

     `adapt`{.descname}(*impltype*, *\*\*kw*)[¶](#sqlalchemy.types.SchemaType.adapt "Permalink to this definition")
    :   

    `结合 T0> ¶ T1>`{.descname}
    :   

    `复制 T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   

     `create`{.descname}(*bind=None*, *checkfirst=False*)[¶](#sqlalchemy.types.SchemaType.create "Permalink to this definition")
    :   为此类型发出CREATE ddl（如果适用）。

     `drop`{.descname}(*bind=None*, *checkfirst=False*)[¶](#sqlalchemy.types.SchemaType.drop "Permalink to this definition")
    :   为此类型发布DROP ddl（如果适用）。

*class* `sqlalchemy.types。`{.descclassname} `SmallInteger`{.descname} [¶](#sqlalchemy.types.SmallInteger "Permalink to this definition")
:   基础：[`sqlalchemy.types.Integer`](#sqlalchemy.types.Integer "sqlalchemy.types.Integer")

    一个更小的`int`整数的类型。

    通常在DDL中生成一个`SMALLINT`，否则就像Python端的普通[`Integer`](#sqlalchemy.types.Integer "sqlalchemy.types.Integer")一样。

*class* `sqlalchemy.types。`{.descclassname} `字符串`{.descname} （ *length =无*，*= None*，*convert\_unicode = False*，*unicode\_error = None*，*\_warn\_on\_bytestring = False ） [¶ T10\>](#sqlalchemy.types.String "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Concatenable`](type_api.html#sqlalchemy.types.Concatenable "sqlalchemy.types.Concatenable")，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    所有字符串和字符类型的基础。plain

    在SQL中，对应于VARCHAR。也可以采用Python
    unicode对象，并在绑定参数中对数据库的编码进行编码（结果集相反）。

    当在CREATE
    TABLE语句中使用String类型时，通常需要长度字段，因为VARCHAR在大多数数据库上需要长度。

     `__init__`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.types.String.__init__ "Permalink to this definition")
    :   创建一个字符串保存类型。

        参数：

        -   **length**[¶](#sqlalchemy.types.String.params.length) –
            optional, a length for the column for use in DDL and CAST
            expressions. 如果没有发布`CREATE TABLE`，可以安全地省略。某些数据库可能需要用于DDL的`length`，并且在`CREATE TABLE`
            DDL时会引发异常如果包含没有长度的`VARCHAR`，则发布。值是否被解释为字节或字符是数据库特定的。
        -   **整理** [¶](#sqlalchemy.types.String.params.collation) -

            可选，用于DDL和CAST表达式的列级别排序规则。使用SQLite，MySQL和Postgresql支持的COLLATE关键字进行呈现。例如。：

                >>> from sqlalchemy import cast, select, String
                >>> print select([cast('some string', String(collation='utf8'))])
                SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1

            0.8版新增：增加了对所有字符串类型的COLLATE支持。

        -   **convert\_unicode**
            [¶](#sqlalchemy.types.String.params.convert_unicode) -

            当设置为`True`时，[`String`](#sqlalchemy.types.String "sqlalchemy.types.String")类型将假定输入将作为Python
            `unicode`对象传递，结果以Python
            `unicode`对象。If the DBAPI in use does
            not support Python unicode (which is fewer and fewer these
            days), SQLAlchemy will encode/decode the value, using the
            value of the `encoding` parameter passed
            to [`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
            as the encoding.

            当使用本地支持Python
            unicode对象的DBAPI时，通常不需要设置此标志。For columns that
            are explicitly intended to store non-ASCII data, the
            [`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
            or [`UnicodeText`](#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")
            types should be used regardless, which feature the same
            behavior of `convert_unicode` but also
            indicate an underlying column type that directly supports
            unicode, such as `NVARCHAR`.

            对于非常罕见的情况，Python `unicode`将由本地支持Python `unicode`的后端由SQLAlchemy编码/解码，值`force`可以在这里传递，这将导致无条件地使用SQLAlchemy的编码/解码服务。

        -   **unicode\_error**
            [¶](#sqlalchemy.types.String.params.unicode_error) -
            可选，一种用于处理Unicode转换错误的方法。行为与标准库的`string.decode()`函数的`errors`关键字参数相同。该标志要求将`convert_unicode`设置为`force` -
            否则，SQLAlchemy不保证处理unicode转换的任务。请注意，此标志为已经返回unicode对象的后端（大多数DBAPI所执行的操作）的后端操作增加了显着的性能开销。此标志只能用作从不同或损坏编码的列中读取字符串的最后手段。

*class* `sqlalchemy.types。`{.descclassname} `Text`{.descname} （ *length = None*，*= None*，*convert\_unicode = False*，*unicode\_error = None*，*\_warn\_on\_bytestring = False ） [¶ T10\>](#sqlalchemy.types.Text "Permalink to this definition")*
:   基础：[`sqlalchemy.types.String`](#sqlalchemy.types.String "sqlalchemy.types.String")

    可变大小的字符串类型。plainplain

    在SQL中，通常对应于CLOB或TEXT。也可以采用Python
    unicode对象，并在绑定参数中对数据库的编码进行编码（结果集相反）。通常，TEXT对象没有长度；而一些数据库在这里会接受一个长度的参数，它会被别人拒绝。

*class* `sqlalchemy.types。`{.descclassname} `Time`{.descname} （ *timezone = False* / T5\> [¶ T6\>](#sqlalchemy.types.Time "Permalink to this definition")
:   基础：`sqlalchemy.types._DateAffinity`，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    `datetime.time()`对象的类型。

*class* `sqlalchemy.types。`{.descclassname} `Unicode`{.descname} （ *length = None*，*\* \* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.types.Unicode "Permalink to this definition")*
:   基础：[`sqlalchemy.types.String`](#sqlalchemy.types.String "sqlalchemy.types.String")

    一个可变长度的Unicode字符串类型。plainplain

    The [`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")
    type is a [`String`](#sqlalchemy.types.String "sqlalchemy.types.String")
    subclass that assumes input and output as Python `unicode` data, and in that regard is equivalent to the usage of the
    `convert_unicode` flag with the [`String`](#sqlalchemy.types.String "sqlalchemy.types.String") type.
    但是，与plain [`String`](#sqlalchemy.types.String "sqlalchemy.types.String")不同，它还意味着一种基本列类型，它明确支持非ASCII数据，例如Oracle和SQL
    Server上的`NVARCHAR`。This can impact the output
    of `CREATE TABLE` statements and
    `CAST` functions at the dialect level, and can
    also affect the handling of bound parameters in some specific DBAPI
    scenarios.

    由[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")类型使用的编码通常由DBAPI本身决定；大多数现代的DBAPI都支持Python
    `unicode`对象作为绑定值和结果集值，编码应该在[Dialects](dialects_index.html)部分的目标DBAPI注释中详细说明。
    。

    对于那些不支持或未配置为直接适应Python `unicode`对象的DBAPI，SQLAlchemy会在DBAPI之外进行编码和解码。此场景中的编码由传递给[`create_engine()`](engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的`encoding`标志确定。

    使用[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")类型时，仅适用于传递Python
    `unicode`对象，而不是`str`。如果在Python 2下传递一个普通的`str`，则会发出警告。如果您注意到您的应用程序发出这些警告，但您不确定它们的来源，请参阅[http://docs.python.org/library/warnings上的Python
    `warnings`过滤器。
    .html](http://docs.python.org/library/warnings.html)可用于将这些警告转化为例外，它将说明堆栈跟踪：

        import warnings
        warnings.simplefilter('error')

    对于希望平等传递字节串和Python `unicode`对象至`Unicode`类型的应用程序，字节串必须先解码为unicode。将[Coercing
    Encoded Strings to
    Unicode](custom_types.html#coerce-to-unicode)的配方说明了这是如何完成的。

    也可以看看：

    > [`UnicodeText`](#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")
    > - 与[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")不相容的文本对应。

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.types.Unicode.__init__ "Permalink to this definition")
    :   创建一个[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")对象。

        参数与[`String`](#sqlalchemy.types.String "sqlalchemy.types.String")的参数相同，不同的是`convert_unicode`默认为`True`。

*class* `sqlalchemy.types。`{.descclassname} `UnicodeText`{.descname} （ *length = None*，*\* \* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.types.UnicodeText "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Text`](#sqlalchemy.types.Text "sqlalchemy.types.Text")

    无限长的Unicode字符串类型。plain

    有关此对象的Unicode特性的详细信息，请参阅[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")。

    像[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")一样，[`UnicodeText`](#sqlalchemy.types.UnicodeText "sqlalchemy.types.UnicodeText")类型的用法意味着在后端使用了能够使用unicode的类型，例如`NCLOB`，`NTEXT`

    `__ init __`{.descname} （ *length = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.types.UnicodeText.__init__ "Permalink to this definition")
    :   创建一个Unicode转换文本类型。

        参数与[`Text`](#sqlalchemy.types.Text "sqlalchemy.types.Text")相同，但`convert_unicode`默认为`True`。

SQL 标准和多个供应商类型[¶](#sql-standard-and-multiple-vendor-types "Permalink to this headline")
------------------------------------------------------------------------------------------------

此类型的类型是指属于 SQL 标准一部分的类型，或可能在数据库后端子集中找到的类型。Unlike
the “generic” types, the SQL standard/multi-vendor types have **no**
guarantee of working on all backends, and will only work on those
backends that explicitly support them by name.
也就是说，类型将始终使用`CREATE TABLE`发布 DDL 中的确切名称。

*class* `sqlalchemy.types。`{.descclassname} `ARRAY`{.descname} （ *item\_type*，*as\_tuple = False dimensions = None，*zero\_indexes = False* ） [¶](#sqlalchemy.types.ARRAY "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Indexable`](type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")，[`sqlalchemy.types.Concatenable`](type_api.html#sqlalchemy.types.Concatenable "sqlalchemy.types.Concatenable")，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示一个SQL数组类型。

    注意

    这种类型是所有ARRAY操作的基础。但是，目前**只有Postgresql后端支持SQLAlchemy**中的SQL数组。建议在使用PostgreSQL的ARRAY类型时直接使用[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型，因为它提供了特定于该后端的其他运算符。

    [`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")是支持各种SQL标准函数（如显式涉及数组的[`array_agg`](functions.html#sqlalchemy.sql.functions.array_agg "sqlalchemy.sql.functions.array_agg")）的Core的一部分；但是，除PostgreSQL后端和可能的某些第三方方言外，其他SQLAlchemy内置方言不支持此类型。

    给定元素的“类型”构造[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型：

        mytable = Table("mytable", metadata,
                Column("data", ARRAY(Integer))
            )

    上面的类型表示一个N维数组，意味着支持的后端（如Postgresql）将自动解释具有任意数量维的值。为了生成一个传入一维整数数组的INSERT构造：

        connection.execute(
                mytable.insert(),
                data=[1,2,3]
        )

    [`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型可以给定固定数量的维度：

        mytable = Table("mytable", metadata,
                Column("data", ARRAY(Integer, dimensions=2))
            )

    发送多个维度是可选的，但建议如果数据类型代表多个维度的数组。这个数字用于：

    -   当向数据库发送类型声明本身时，例如`INTEGER[][]`

    -   在将Python值转换为数据库值时，反之亦然，例如一个[`Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")对象的ARRAY使用此数字来高效地访问数组结构中的字符串值，而无需依靠每行类型检查

    -   当与Python `getitem`访问器一起使用时，维数用于定义`[]`运算符应返回的类型的类型。对于具有两个维度的INTEGER阵列：

            >>> expr = table.c.column[5]  # returns ARRAY(Integer, dimensions=1)
            >>> expr = expr[6]  # returns Integer

    对于一维数组，一个没有维度参数的[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")实例通常会假定为单维行为。

    类型[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")的SQL表达式支持“索引”和“切片”行为。在给定整数索引或切片的情况下，Python
    `[]`运算符正常工作。数组默认为基于1的索引。运算符生成二进制表达式结构，这将为SELECT语句生成适当的SQL：

        select([mytable.c.data[5], mytable.c.data[2:7]])

    以及使用[`Update.values()`](dml.html#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")方法时的UPDATE语句：

        mytable.update().values({
            mytable.c.data[5]: 7,
            mytable.c.data[2:7]: [1, 2, 3]
        })

    [`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型还为运算符[`types.ARRAY.Comparator.any()`](#sqlalchemy.types.ARRAY.Comparator.any "sqlalchemy.types.ARRAY.Comparator.any")和[`types.ARRAY.Comparator.all()`](#sqlalchemy.types.ARRAY.Comparator.all "sqlalchemy.types.ARRAY.Comparator.all")
    。PostgreSQL特定版本的[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")也提供了额外的操作符。

    版本1.1.0中的新功能

    也可以看看

    [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.types.ARRAY.Comparator "Permalink to this definition")
    :   基础：`sqlalchemy.types.Comparator`，`sqlalchemy.types.Comparator`

        定义[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")的比较操作。

        这种类型的方言特定形式提供了更多的运算符。参见[`postgresql.ARRAY.Comparator`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator "sqlalchemy.dialects.postgresql.ARRAY.Comparator")。

        `全部`{.descname} （ *其他*，*运营商=无* ） [t5 \>](#sqlalchemy.types.ARRAY.Comparator.all "Permalink to this definition")
        :   返回`其他 运算符 ALL （数组）`子句。

            参数的地方被切换，因为ALL要求数组表达式在右侧。

            例如。：

                from sqlalchemy.sql import operators

                conn.execute(
                    select([table.c.data]).where(
                            table.c.data.all(7, operator=operators.lt)
                        )
                )

            参数：

            -   **其他**
                [¶](#sqlalchemy.types.ARRAY.Comparator.all.params.other)
                - 要比较的表达式
            -   **operator**[¶](#sqlalchemy.types.ARRAY.Comparator.all.params.operator)
                – an operator object from the
                `sqlalchemy.sql.operators` package, defaults to `operators.eq()`.

            也可以看看

            [`sql.expression.all_()`](sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")

            [`types.ARRAY.Comparator.any()`](#sqlalchemy.types.ARRAY.Comparator.any "sqlalchemy.types.ARRAY.Comparator.any")

        `任何`{.descname} （ *其他*，*运营商=无* ） [t5 \>](#sqlalchemy.types.ARRAY.Comparator.any "Permalink to this definition")
        :   返回`其他 运算符 ANY （数组）`子句。

            参数的位置被切换，因为ANY要求数组表达式在右侧。

            例如。：

                from sqlalchemy.sql import operators

                conn.execute(
                    select([table.c.data]).where(
                            table.c.data.any(7, operator=operators.lt)
                        )
                )

            参数：

            -   **其他**
                [¶](#sqlalchemy.types.ARRAY.Comparator.any.params.other)
                - 要比较的表达式
            -   **operator**[¶](#sqlalchemy.types.ARRAY.Comparator.any.params.operator)
                – an operator object from the
                `sqlalchemy.sql.operators` package, defaults to `operators.eq()`.

            也可以看看

            [`sql.expression.any_()`](sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")

            [`types.ARRAY.Comparator.all()`](#sqlalchemy.types.ARRAY.Comparator.all "sqlalchemy.types.ARRAY.Comparator.all")

    `ARRAY  tt> __ init __`{.descclassname} （ *item\_type*，*as\_tuple = False*，*dimensions =无*，*zero\_indexes = False ） [¶](#sqlalchemy.types.ARRAY.__init__ "Permalink to this definition")*
    :   构建[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")。

        例如。：

            Column('myarray', ARRAY(Integer))

        参数是：

        参数：

        -   **item\_type** [¶](#sqlalchemy.types.ARRAY.params.item_type)
            -
            此数组项目的数据类型。请注意，这里的维数是不相关的，所以像`INTEGER[][]`这样的多维数组被构造为`ARRAY(Integer)`，而不是`ARRAY(ARRAY(Integer))`等等。
        -   **as\_tuple = False**
            [¶](#sqlalchemy.types.ARRAY.params.as_tuple) -
            指定返回结果是否应该从列表转换为元组。由于Python列表很好地对应于SQL数组，因此通常不需要此参数。
        -   **dimensions**[¶](#sqlalchemy.types.ARRAY.params.dimensions)
            – if non-None, the ARRAY will assume a fixed number of
            dimensions.
            这会影响数组在数据库中的声明方式，它如何解释Python和结果值，以及与“getitem”运算符一起工作的表达式行为。有关更多详细信息，请参阅[`types.ARRAY`](#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")中的说明。
        -   **zero\_indexes=False**[¶](#sqlalchemy.types.ARRAY.params.zero_indexes)
            – when True, index values will be converted between Python
            zero-based and SQL one-based indexes, e.g. a value of one
            will be added to all index values before passing to the
            database.

    ` ARRAY。 T0>  comparator_factory  T1> ¶ T2>`{.descclassname}
    :   [`Comparator`](#sqlalchemy.types.ARRAY.Comparator "sqlalchemy.types.ARRAY.Comparator")的别名

    `ARRAY。`{.descclassname} `zero_indexes`{.descname} *= False* [¶](#sqlalchemy.types.ARRAY.zero_indexes "Permalink to this definition")
    :   如果为True，则Python基于零的索引应该在SQL表达式一侧解释为基于一。

*class* `sqlalchemy.types。`{.descclassname} `BIGINT`{.descname} [¶](#sqlalchemy.types.BIGINT "Permalink to this definition")
:   基础：[`sqlalchemy.types.BigInteger`](#sqlalchemy.types.BigInteger "sqlalchemy.types.BigInteger")

    SQL BIGINT类型。plain

*class* `sqlalchemy.types。`{.descclassname} `BINARY`{.descname} （ *length = None* / T5\> [¶ T6\>](#sqlalchemy.types.BINARY "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    SQL BINARY类型。plainplainplain

*class* `sqlalchemy.types。`{.descclassname} `BLOB`{.descname} （ *length = None* / T5\> [¶ T6\>](#sqlalchemy.types.BLOB "Permalink to this definition")
:   基础：[`sqlalchemy.types.LargeBinary`](#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

    SQL BLOB类型。

 *class*`sqlalchemy.types.`{.descclassname}`BOOLEAN`{.descname}(*create\_constraint=True*, *name=None*, *\_create\_events=True*)[¶](#sqlalchemy.types.BOOLEAN "Permalink to this definition")
:   基础：[`sqlalchemy.types.Boolean`](#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")

    SQL BOOLEAN类型。

*class* `sqlalchemy.types。`{.descclassname} `CHAR`{.descname} （ *length = None*，*= None*，*convert\_unicode = False*，*unicode\_error = None*，*\_warn\_on\_bytestring = False ） [¶ T10\>](#sqlalchemy.types.CHAR "Permalink to this definition")*
:   基础：[`sqlalchemy.types.String`](#sqlalchemy.types.String "sqlalchemy.types.String")

    SQL CHAR类型。

*class* `sqlalchemy.types。`{.descclassname} `CLOB`{.descname} （ *length =无*，*= None*，*convert\_unicode = False*，*unicode\_error = None*，*\_warn\_on\_bytestring = False ） [¶ T10\>](#sqlalchemy.types.CLOB "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Text`](#sqlalchemy.types.Text "sqlalchemy.types.Text")

    CLOB类型。plainplain

    这种类型可以在Oracle和Informix中找到。

 *class*`sqlalchemy.types.`{.descclassname}`DATE`{.descname}[¶](#sqlalchemy.types.DATE "Permalink to this definition")
:   基础：[`sqlalchemy.types.Date`](#sqlalchemy.types.Date "sqlalchemy.types.Date")

    SQL DATE类型。plainplainplain

 *class*`sqlalchemy.types.`{.descclassname}`DATETIME`{.descname}(*timezone=False*)[¶](#sqlalchemy.types.DATETIME "Permalink to this definition")
:   基础：[`sqlalchemy.types.DateTime`](#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")

    SQL DATETIME类型。

 *class*`sqlalchemy.types.`{.descclassname}`DECIMAL`{.descname}(*precision=None*, *scale=None*, *decimal\_return\_scale=None*, *asdecimal=True*)[¶](#sqlalchemy.types.DECIMAL "Permalink to this definition")
:   基础：[`sqlalchemy.types.Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")

    SQL DECIMAL类型。plain

 *class*`sqlalchemy.types.`{.descclassname}`FLOAT`{.descname}(*precision=None*, *asdecimal=False*, *decimal\_return\_scale=None*, *\*\*kwargs*)[¶](#sqlalchemy.types.FLOAT "Permalink to this definition")
:   基础：[`sqlalchemy.types.Float`](#sqlalchemy.types.Float "sqlalchemy.types.Float")

    SQL FLOAT类型。plainplain

`sqlalchemy.types。 T0>  INT  T1> ¶ T2>`{.descclassname}
:   [`INTEGER`](#sqlalchemy.types.INTEGER "sqlalchemy.types.INTEGER")的别名

*class* `sqlalchemy.types。`{.descclassname} `JSON`{.descname} （ *none\_as\_null = False* / T5\> [¶ T6\>](#sqlalchemy.types.JSON "Permalink to this definition")
:   基础：[`sqlalchemy.types.Indexable`](type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")，[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示一个SQL JSON类型。plainplainplain

    注意

    [`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")作为特定于供应商的JSON类型的外观提供。由于它支持JSON
    SQL操作，因此它只适用于具有实际JSON类型的后端，目前Postgresql以及某些版本的MySQL。

    [`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")是Core的一部分，以支持原生JSON数据类型日益普及。

    [`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型存储任意的JSON格式数据，例如：

        data_table = Table('data_table', metadata,
            Column('id', Integer, primary_key=True),
            Column('data', JSON)
        )

        with engine.connect() as conn:
            conn.execute(
                data_table.insert(),
                data = {"key1": "value1", "key2": "value2"}
            )

    基础[`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")提供了这两个操作：

    -   键控索引操作：

            data_table.c.data['some key']

    -   整数索引操作：

            data_table.c.data[3]

    -   路径索引操作：

            data_table.c.data[('key_1', 'key_2', 5, ..., 'key_n')]

    额外的操作可以从[`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")特定于方言的版本中找到，如[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")和[`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")，其中每个都可以提供比基本类型更多的操作员。

    索引操作默认返回一个默认类型默认为[`JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")的表达式对象，这样可以根据结果类型调用更多的面向JSON的指令。

    当与SQLAlchemy ORM一起使用时，[`JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型不检测结构的就地突变。为了检测这些，必须使用[`sqlalchemy.ext.mutable`](orm_extensions_mutable.html#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展名。该扩展将允许对数据结构进行“就地”更改以产生将由工作单元检测到的事件。有关字典的简单示例，请参阅[`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")中的示例。

    当使用NULL值时，[`JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型建议使用两个特定常量来区分求值为SQL
    NULL的列，例如没有值，与`"null"`。要插入或选择一个SQL NULL值，请使用常量[`null()`](sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")：

        from sqlalchemy import null
        conn.execute(table.insert(), json_value=null())

    要插入或选择一个值为JSON `"null"`的值，请使用常量[`JSON.NULL`{](#sqlalchemy.types.JSON.NULL "sqlalchemy.types.JSON.NULL")：

        conn.execute(table.insert(), json_value=JSON.NULL)

    [`JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型支持一个标记[`JSON.none_as_null`](#sqlalchemy.types.JSON.params.none_as_null "sqlalchemy.types.JSON")，当设置为True时，将导致Python常量`None`评估为SQL
    NULL的值，并且设置为False时，会导致Python常量`None`求值为JSON `"null"`。为了指示NULL值，Python值`None`可以与[`JSON.NULL`{](#sqlalchemy.types.JSON.NULL "sqlalchemy.types.JSON.NULL")和[`null()`](sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")结合使用，但必须小心在这些情况下取决于[`JSON.none_as_null`](#sqlalchemy.types.JSON.params.none_as_null "sqlalchemy.types.JSON")的值。

    也可以看看

    [`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")

    [`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")

    [`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")

    版本1.1中的新功能

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.types.JSON.Comparator "Permalink to this definition")
    :   基础：`sqlalchemy.types.Comparator`，`sqlalchemy.types.Comparator`

        定义[`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")的比较操作。

    *class* `JSON。`{.descclassname} `JSONIndexType`{.descname} [¶](#sqlalchemy.types.JSON.JSONIndexType "Permalink to this definition")
    :   基础：[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        JSON索引值的数据类型的占位符。

        这允许执行时处理JSON索引值以获取特殊语法。

    *class* `JSON。`{.descclassname} `JSONPathType`{.descname} [¶](#sqlalchemy.types.JSON.JSONPathType "Permalink to this definition")
    :   基础：[`sqlalchemy.types.TypeEngine`](type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

        JSON路径操作的占位符类型。

        这允许将基于路径的索引值执行时处理为特定的SQL语法。

    `JSON。`{.descclassname} `NULL`{.descname} *=符号（'JSON\_NULL'）* [¶](#sqlalchemy.types.JSON.NULL "Permalink to this definition")
    :   描述NULL的json值。

        该值用于强制使用`"null"`的JSON值作为值。根据[`JSON.none_as_null`](#sqlalchemy.types.JSON.params.none_as_null "sqlalchemy.types.JSON")标志的设置，Python
        `None`的值将被识别为SQL NULL或JSON
        `"null"`无论此设置如何，都可以使用[`JSON.NULL`](#sqlalchemy.types.JSON.NULL "sqlalchemy.types.JSON.NULL")常量来解析为JSON
        `"null"`。这与`sql.null()`结构形成对比，该结构始终解析为SQL
        NULL。例如。：

            from sqlalchemy import null
            from sqlalchemy.dialects.postgresql import JSON

            obj1 = MyObject(json_value=null())  # will *always* insert SQL NULL
            obj2 = MyObject(json_value=JSON.NULL)  # will *always* insert JSON string "null"

            session.add_all([obj1, obj2])
            session.commit()

    ` JSON。 T0>  __初始化__  T1> （ T2>  none_as_null =假 T3> ） T4> ¶ T5 >`{.descclassname}
    :   构造一个[`types.JSON`](#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型。

        参数：

        **none\_as\_null = False**
        [¶](#sqlalchemy.types.JSON.params.none_as_null) -

        如果为True，则将值`None`保留为SQL
        NULL值，而不是`null`的JSON编码。请注意，当此标志为False时，[`null()`](sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")结构仍可用于保留NULL值：

            from sqlalchemy import null
            conn.execute(table.insert(), data=null())

        也可以看看

        [`types.JSON.NULL`](#sqlalchemy.types.JSON.NULL "sqlalchemy.types.JSON.NULL")

    ` JSON。 T0>  comparator_factory  T1> ¶ T2>`{.descclassname}
    :   [`Comparator`](#sqlalchemy.types.JSON.Comparator "sqlalchemy.types.JSON.Comparator")的别名

 *class*`sqlalchemy.types.`{.descclassname}`INTEGER`{.descname}[¶](#sqlalchemy.types.INTEGER "Permalink to this definition")
:   基础：[`sqlalchemy.types.Integer`](#sqlalchemy.types.Integer "sqlalchemy.types.Integer")

    SQL INT或INTEGER类型。

*class* `sqlalchemy.types。`{.descclassname} `NCHAR`{.descname} （ *length = None*，*\* \* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.types.NCHAR "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")

    SQL NCHAR类型。plain

*class* `sqlalchemy.types。`{.descclassname} `NVARCHAR`{.descname} （ *length = None*，*\* \* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.types.NVARCHAR "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Unicode`](#sqlalchemy.types.Unicode "sqlalchemy.types.Unicode")

    SQL NVARCHAR类型。plain

 *class*`sqlalchemy.types.`{.descclassname}`NUMERIC`{.descname}(*precision=None*, *scale=None*, *decimal\_return\_scale=None*, *asdecimal=True*)[¶](#sqlalchemy.types.NUMERIC "Permalink to this definition")
:   基础：[`sqlalchemy.types.Numeric`](#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")

    SQL NUMERIC类型。plain

*class* `sqlalchemy.types。`{.descclassname} `REAL`{.descname} （ *precision = None*，*asdecimal = False*，*decimal\_return\_scale = None*，*\*\* kwargs* ） [¶](#sqlalchemy.types.REAL "Permalink to this definition")
:   基础：[`sqlalchemy.types.Float`](#sqlalchemy.types.Float "sqlalchemy.types.Float")

    SQL REAL类型。plainplainplain

*class* `sqlalchemy.types。`{.descclassname} `SMALLINT`{.descname} [¶](#sqlalchemy.types.SMALLINT "Permalink to this definition")
:   基础：[`sqlalchemy.types.SmallInteger`](#sqlalchemy.types.SmallInteger "sqlalchemy.types.SmallInteger")

    SQL SMALLINT类型。

 *class*`sqlalchemy.types.`{.descclassname}`TEXT`{.descname}(*length=None*, *collation=None*, *convert\_unicode=False*, *unicode\_error=None*, *\_warn\_on\_bytestring=False*)[¶](#sqlalchemy.types.TEXT "Permalink to this definition")
:   基础：[`sqlalchemy.types.Text`](#sqlalchemy.types.Text "sqlalchemy.types.Text")

    SQL TEXT类型。plain

 *class*`sqlalchemy.types.`{.descclassname}`TIME`{.descname}(*timezone=False*)[¶](#sqlalchemy.types.TIME "Permalink to this definition")
:   基础：[`sqlalchemy.types.Time`](#sqlalchemy.types.Time "sqlalchemy.types.Time")

    SQL TIME类型。plainplainplainplain

*class* `sqlalchemy.types。`{.descclassname} `TIMESTAMP`{.descname} （ *timezone = False* / T5\> [¶ T6\>](#sqlalchemy.types.TIMESTAMP "Permalink to this definition")
:   基础：[`sqlalchemy.types.DateTime`](#sqlalchemy.types.DateTime "sqlalchemy.types.DateTime")

    SQL TIMESTAMP类型。plain

*class* `sqlalchemy.types。`{.descclassname} `VARBINARY`{.descname} （ *length = None* / T5\> [¶ T6\>](#sqlalchemy.types.VARBINARY "Permalink to this definition")
:   基础：`sqlalchemy.types._Binary`

    SQL VARBINARY类型。plainplainplain

*class* `sqlalchemy.types。`{.descclassname} `VARCHAR`{.descname} （ *length =无*，*= None*，*convert\_unicode = False*，*unicode\_error = None*，*\_warn\_on\_bytestring = False ） [¶ T10\>](#sqlalchemy.types.VARCHAR "Permalink to this definition")*
:   基础：[`sqlalchemy.types.String`](#sqlalchemy.types.String "sqlalchemy.types.String")

    SQL VARCHAR类型。

供应商特定类型[¶](#vendor-specific-types "Permalink to this headline")
----------------------------------------------------------------------

数据库特定类型也可用于从每个数据库的方言模块导入。请参阅您感兴趣的数据库的[Dialects](dialects_index.html)参考。

例如，MySQL 有一个`BIGINT`类型，而 PostgreSQL 有一个`INET`类型。要使用这些，请明确从模块中导入它们：

    from sqlalchemy.dialects import mysqlplain

    table = Table('foo', metadata,
        Column('id', mysql.BIGINT),
        Column('enumerates', mysql.ENUM('a', 'b', 'c'))
    )

或者一些 PostgreSQL 类型：

    from sqlalchemy.dialects import postgresqlplainplain

    table = Table('foo', metadata,
        Column('ipaddress', postgresql.INET),
        Column('elements', postgresql.ARRAY(String))
    )

每个方言在\_\_ all
\_\_集合中提供了该后端支持的完整类型名称集合，因此简单的 import
\*或类似方式将导入为该后端实现的所有受支持类型：

    from sqlalchemy.dialects.postgresql import *plain

    t = Table('mytable', metadata,
               Column('id', INTEGER, primary_key=True),
               Column('name', VARCHAR(300)),
               Column('inetaddr', INET)
    )

如上所述，INTEGER 和 VARCHAR 类型最终来自 sqlalchemy.types，INET 特定于 Postgresql 方言。

某些方言级别类型与 SQL 标准类型具有相同的名称，但也提供了其他参数。例如，MySQL 实现了包括附加参数（如 collat​​ion 和 charset）的所有字符和字符串类型：

    from sqlalchemy.dialects.mysql import VARCHAR, TEXTplain

    table = Table('foo', meta,
        Column('col1', VARCHAR(200, collation='binary')),
        Column('col2', TEXT(charset='latin1'))
    )
