---
title: 自定义 SQL 构造和编译扩展
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/55c1ab/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
自定义 SQL 构造和编译扩展[¶](#module-sqlalchemy.ext.compiler "Permalink to this headline")
========================================================================================

提供用于创建自定义 ClauseElements 和编译器的 API。

概要[¶ T0\>](#synopsis "Permalink to this headline")
----------------------------------------------------

用法涉及创建一个或多个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")子类和一个或多个定义其编译的可调参数：

    from sqlalchemy.ext.compiler import compilesplainplainplainplainplainplainplain
    from sqlalchemy.sql.expression import ColumnClause

    class MyColumn(ColumnClause):
        pass

    @compiles(MyColumn)
    def compile_mycolumn(element, compiler, **kw):
        return "[%s]" % element.name

Above, `MyColumn` extends [`ColumnClause`](sqlelement.html#sqlalchemy.sql.expression.ColumnClause "sqlalchemy.sql.expression.ColumnClause"),
the base expression element for named column objects.
`compiles`修饰符向`MyColumn`类注册自己，以便在对象编译为字符串时调用它：

    from sqlalchemy import selectplainplainplainplainplainplain

    s = select([MyColumn('x'), MyColumn('y')])
    print str(s)

生产：

    SELECT [x], [y]plainplainplainplainplainplainplain

特定于方言的编译规则[¶](#dialect-specific-compilation-rules "Permalink to this headline")
-----------------------------------------------------------------------------------------

编译器也可以制作方言特定的。正在使用的方言将调用适当的编译器：

    from sqlalchemy.schema import DDLElementplainplainplainplainplainplainplainplainplain

    class AlterColumn(DDLElement):

        def __init__(self, column, cmd):
            self.column = column
            self.cmd = cmd

    @compiles(AlterColumn)
    def visit_alter_column(element, compiler, **kw):
        return "ALTER COLUMN %s ..." % element.column.name

    @compiles(AlterColumn, 'postgresql')
    def visit_alter_column(element, compiler, **kw):
        return "ALTER TABLE %s ALTER COLUMN %s ..." % (element.table.name,
                                                       element.column.name)

当使用任何`postgresql`方言时，第二个`visit_alter_table`将被调用。

编译自定义表达式结构[¶](#compiling-sub-elements-of-a-custom-expression-construct "Permalink to this headline")的子元素
----------------------------------------------------------------------------------------------------------------------

`compiler`参数是正在使用的[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。可以检查此对象是否有任何关于正在进行的编译的信息，包括`compiler.dialect`，`compiler.statement`等。[`SQLCompiler`](internals.html#sqlalchemy.sql.compiler.SQLCompiler "sqlalchemy.sql.compiler.SQLCompiler")和[`DDLCompiler`](internals.html#sqlalchemy.sql.compiler.DDLCompiler "sqlalchemy.sql.compiler.DDLCompiler")都包含一个`process()`方法，可用于编译嵌入属性：

    from sqlalchemy.sql.expression import Executable, ClauseElementplainplainplainplain

    class InsertFromSelect(Executable, ClauseElement):
        def __init__(self, table, select):
            self.table = table
            self.select = select

    @compiles(InsertFromSelect)
    def visit_insert_from_select(element, compiler, **kw):
        return "INSERT INTO %s (%s)" % (
            compiler.process(element.table, asfrom=True),
            compiler.process(element.select)
        )

    insert = InsertFromSelect(t1, select([t1]).where(t1.c.x>5))
    print insert

生产：

    "INSERT INTO mytable (SELECT mytable.x, mytable.y, mytable.zplainplainplainplainplainplainplain
                          FROM mytable WHERE mytable.x > :x_1)"

注意

上面的`InsertFromSelect`结构仅仅是一个例子，这个实际的功能已经可以使用[`Insert.from_select()`](dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")方法了。

注意

上面的`InsertFromSelect`构造可能希望启用“autocommit”。有关此步骤，请参阅[Enabling
Autocommit on a Construct](#enabling-compiled-autocommit)。

### 在 SQL 和 DDL 编译器之间交叉编译[¶](#cross-compiling-between-sql-and-ddl-compilers "Permalink to this headline")

SQL 和 DDL 结构分别使用不同的基本编译器 - `SQLCompiler`和`DDLCompiler`进行编译。常见的需求是从 DDL 表达式中访问 SQL 表达式的编译规则。由于这个原因，`DDLCompiler`包含一个访问器`sql_compiler`，比如下面我们生成一个嵌入 SQL 表达式的 CHECK 约束：

    @compiles(MyConstraint)plainplainplainplainplainplain
    def compile_my_constraint(constraint, ddlcompiler, **kw):
        return "CONSTRAINT %s CHECK (%s)" % (
            constraint.name,
            ddlcompiler.sql_compiler.process(
                constraint.expression, literal_binds=True)
        )

上面，我们在`SQLCompiler.process()`（即`literal_binds`）标志调用的过程步骤中添加了一个额外的标志。This indicates that
any SQL expression which refers to a [`BindParameter`](sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")
object or other “literal” object such as those which refer to strings or
integers should be rendered **in-place**, rather than being referred to
as a bound parameter; when emitting DDL, bound parameters are typically
not supported.

在构造上启用自动提交[¶](#enabling-autocommit-on-a-construct "Permalink to this headline")
-----------------------------------------------------------------------------------------

当被要求在没有用户定义事务的情况下执行构造时，回顾[Understanding
Autocommit](connections.html#autocommit)时，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")检测给定构造是否表示 DML 或 DDL，也就是说，数据修改或数据定义语句需要（或者可能需要，在 DDL 的情况下）由 DBAPI 生成的事务被提交（回想起，无论 SQLAlchemy 做什么，DBAPI 总是有一个事务正在进行）。通过检查结构上的“自动提交”执行选项实际上可以完成检查。在构建像 INSERT 派生，新的 DDL 类型或可能改变数据的存储过程的构造时，需要设置“autocommit”选项以使语句在“无连接”执行时运行（如[Connectionless
Execution, Implicit Execution](connections.html#dbengine-implicit)）。

目前，一个快速的方法是将[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")子类化，然后将“autocommit”标志添加到`_execution_options`字典中（注意这是一个“冻结” `union()`方法）：

    from sqlalchemy.sql.expression import Executable, ClauseElementplainplainplainplain

    class MyInsertThing(Executable, ClauseElement):
        _execution_options = \
            Executable._execution_options.union({'autocommit': True})

More succinctly, if the construct is truly similar to an INSERT, UPDATE,
or DELETE, [`UpdateBase`](dml.html#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")
can be used, which already is a subclass of [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable"),
[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
and includes the `autocommit` flag:

    from sqlalchemy.sql.expression import UpdateBaseplainplainplainplain

    class MyInsertThing(UpdateBase):
        def __init__(self, ...):
            ...

子类[`DDLElement`](ddl.html#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")的 DDL 元素已经打开了“autocommit”标志。

更改现有构造的默认编译[¶](#changing-the-default-compilation-of-existing-constructs "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------

编译器扩展也适用于现有的构造。当覆盖内置的 SQL 构造的编译时，@compiles 装饰器将在适当的类上调用（确保使用该类，即`Insert`或`Select`），而不是创建函数，如`insert()`或`select()`）。

在新的编译函数中，为了获得“原始”编译例程，使用适当的 visit\_XXX 方法 -
这是因为 compiler.process()将调用重写例程并导致无限循环。比如，为所有插入语句添加“前缀”：

    from sqlalchemy.sql.expression import Insertplainplainplainplain

    @compiles(Insert)
    def prefix_inserts(insert, compiler, **kw):
        return compiler.visit_insert(insert.prefix_with("some prefix"), **kw)

上面的编译器会在编译时为所有 INSERT 语句加上“some prefix”。

更改类型的编译[¶](#changing-compilation-of-types "Permalink to this headline")
------------------------------------------------------------------------------

`compiler`也适用于类型，例如下面我们为`String` /
`VARCHAR`实现特定于 MS-SQL 的'max'关键字：

    @compiles(String, 'mssql')plain
    @compiles(VARCHAR, 'mssql')
    def compile_varchar(element, compiler, **kw):
        if element.length == 'max':
            return "VARCHAR('max')"
        else:
            return compiler.visit_VARCHAR(element, **kw)

    foo = Table('foo', metadata,
        Column('data', VARCHAR('max'))
    )

子类指南[¶](#subclassing-guidelines "Permalink to this headline")
-----------------------------------------------------------------

使用编译器扩展的很大一部分是对 SQLAlchemy 表达式结构进行子类化。为了使这更容易，表达式和模式包包含一组用于常见任务的“基础”。简介如下：

-   [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
    -
    这是根表达式类。任何 SQL 表达式都可以从此基础派生，并且可能是更长的构造（如专用 INSERT 语句）的最佳选择。

-   [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    -
    所有“列式”元素的根。任何你放在 SELECT 语句的“columns”子句中的东西（以及 order
    by 和 group by）都可以从中得到 - 对象将自动具有 Python 的“比较”行为。

    [`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")
    classes want to have a `type` member which is
    expression’s return type.
    这可以在构造函数的实例级别建立，也可以在类级别建立，如果它通常是常量：

        class timestamp(ColumnElement):plainplainplainplainplainplain
            type = TIMESTAMP()

-   [`FunctionElement`](functions.html#sqlalchemy.sql.functions.FunctionElement "sqlalchemy.sql.functions.FunctionElement")
    - 这是`ColumnElement`和“from 子句”类似对象的混合体，并且表示 SQL 函数或存储过程类型的调用。Since
    most databases support statements along the line of “SELECT FROM ”
    `FunctionElement` adds in the ability to be used
    in the FROM clause of a `select()` construct:

        from sqlalchemy.sql.expression import FunctionElementplainplainplainplainplain

        class coalesce(FunctionElement):
            name = 'coalesce'

        @compiles(coalesce)
        def compile(element, compiler, **kw):
            return "coalesce(%s)" % compiler.process(element.clauses)

        @compiles(coalesce, 'oracle')
        def compile(element, compiler, **kw):
            if len(element.clauses) > 2:
                raise TypeError("coalesce only supports two arguments on Oracle")
            return "nvl(%s)" % compiler.process(element.clauses)

-   [`DDLElement`](ddl.html#sqlalchemy.schema.DDLElement "sqlalchemy.schema.DDLElement")
    - 所有 DDL 表达式的根，例如 CREATE TABLE，ALTER
    TABLE 等。`DDLElement`子类的编译由`DDLCompiler`而不是`SQLCompiler`发布。`DDLElement` also features
    `Table` and `MetaData` event
    hooks via the `execute_at()` method, allowing
    the construct to be invoked during CREATE TABLE and DROP TABLE
    sequences.

-   [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")
    - This is a mixin which should be used with any expression class
    that represents a “standalone” SQL statement that can be passed
    directly to an `execute()` method.
    它已经隐含在`DDLElement`和`FunctionElement`中。

更多示例[¶](#further-examples "Permalink to this headline")
-----------------------------------------------------------

### “UTC 时间戳”功能[¶](#utc-timestamp-function "Permalink to this headline")

一种类似于“CURRENT\_TIMESTAMP”的函数除了应用适当的转换以便时间为 UTC 时间。时间戳最好作为 UTC 存储在关系数据库中，不带时区。UTC，这样您的数据库就不会认为夏令时结束时，时间没有反过来，因为时区就像字符编码一样，没有时区
- 它们最好只应用于应用程序的端点（即在用户输入时转换为 UTC
，在显示时重新应用期望的时区）。

对于 Postgresql 和 Microsoft SQL Server：

    from sqlalchemy.sql import expressionplainplainplainplainplainplainplainplain
    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.types import DateTime

    class utcnow(expression.FunctionElement):
        type = DateTime()

    @compiles(utcnow, 'postgresql')
    def pg_utcnow(element, compiler, **kw):
        return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

    @compiles(utcnow, 'mssql')
    def ms_utcnow(element, compiler, **kw):
        return "GETUTCDATE()"

用法示例：

    from sqlalchemy import (plainplainplainplainplainplainplain
                Table, Column, Integer, String, DateTime, MetaData
            )
    metadata = MetaData()
    event = Table("event", metadata,
        Column("id", Integer, primary_key=True),
        Column("description", String(50), nullable=False),
        Column("timestamp", DateTime, server_default=utcnow())
    )

### “GREATEST”功能[¶](#greatest-function "Permalink to this headline")

“GREATEST”函数被赋予任意数量的参数，并返回最高值的那个 -
它等价于 Python 的`max`函数。SQL 标准版本与基于 CASE 的版本相比，它只适用于两个参数：

    from sqlalchemy.sql import expressionplainplainplainplain
    from sqlalchemy.ext.compiler import compiles
    from sqlalchemy.types import Numeric

    class greatest(expression.FunctionElement):
        type = Numeric()
        name = 'greatest'

    @compiles(greatest)
    def default_greatest(element, compiler, **kw):
        return compiler.visit_function(element)

    @compiles(greatest, 'sqlite')
    @compiles(greatest, 'mssql')
    @compiles(greatest, 'oracle')
    def case_greatest(element, compiler, **kw):
        arg1, arg2 = list(element.clauses)
        return "CASE WHEN %s > %s THEN %s ELSE %s END" % (
            compiler.process(arg1),
            compiler.process(arg2),
            compiler.process(arg1),
            compiler.process(arg2),
        )

用法示例：

    Session.query(Account).\plainplainplainplain
            filter(
                greatest(
                    Account.checking_balance,
                    Account.savings_balance) > 10000
            )

### “false”表达式[¶](#false-expression "Permalink to this headline")

呈现“false”常量表达式，在没有“false”常量的平台上呈现为“0”：

    from sqlalchemy.sql import expressionplainplainplainplainplainplainplainplain
    from sqlalchemy.ext.compiler import compiles

    class sql_false(expression.ColumnElement):
        pass

    @compiles(sql_false)
    def default_false(element, compiler, **kw):
        return "false"

    @compiles(sql_false, 'mssql')
    @compiles(sql_false, 'mysql')
    @compiles(sql_false, 'oracle')
    def int_false(element, compiler, **kw):
        return "0"

用法示例：

    from sqlalchemy import select, union_allplainplainplainplainplain

    exp = union_all(
        select([users.c.name, sql_false().label("enrolled")]),
        select([customers.c.name, customers.c.enrolled])
    )

 `sqlalchemy.ext.compiler.`{.descclassname}`compiles`{.descname}(*class\_*, *\*specs*)[¶](#sqlalchemy.ext.compiler.compiles "Permalink to this definition")
:   为给定的[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")类型注册一个函数作为编译器。

`sqlalchemy.ext.compiler。 T0> 注销 T1> （ T2> 类_  T3> ） T4> ¶< / T5>`{.descclassname}
:   删除与给定[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")类型关联的所有自定义编译器。


