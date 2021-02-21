---
title: migration_06
date: 2021-02-20 22:41:31
permalink: /pages/9ef190/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
SQLAlchemy 0.6中有什么新东西？[¶](#what-s-new-in-sqlalchemy-0-6 "Permalink to this headline")
=============================================================================================

关于本文档

本文档介绍了2012年5月5日发布的SQLAlchemy版本0.5（2010年1月16日发布）和SQLAlchemy
0.6版本之间的更改。

文件日期：2010年6月6日

本指南记录了影响用户将他们的应用程序从0.5系列SQLAlchemy迁移到0.6的API更改。请注意，SQLAlchemy
0.6会删除在0.5系列范围内不推荐使用的一些行为，并且会弃用更多特定于0.5的行为。

平台支持[¶](#platform-support "Permalink to this headline")
-----------------------------------------------------------

-   整个2.xx系列的cPython 2.4以上版本
-   Jython 2.5.1 - 使用Jython中包含的zxJDBC DBAPI。
-   cPython 3.x - 参见[source：sqlalchemy / trunk /
    README.py3k]了解如何为python3构建信息。

新的方言系统[¶](#new-dialect-system "Permalink to this headline")
-----------------------------------------------------------------

现在，方言模块在单个数据库后端的范围内分解为不同的子组件。方言实现现在位于`sqlalchemy.dialects`包中。`sqlalchemy.databases`包依然以占位符的形式存在，为简单的导入提供一定程度的后向兼容性。

对于每个受支持的数据库，在包含多个文件的`sqlalchemy.dialects`中存在一个子包。每个软件包都包含一个称为`base.py`的模块，该模块定义该数据库使用的特定SQL方言。它还包含一个或多个“驱动程序”模块，每个模块对应于特定的DBAPI
- 这些文件被命名为与DBAPI本身相对应，如`pysqlite`，`cx_oracle`或`pyodbc`SQLAlchemy方言使用的类首先在`base.py`模块中声明，定义数据库定义的所有行为特征。这些包括能力映射，如“支持序列”，“支持返回”等，类型定义和SQL编译规则。每个“驱动程序”模块依次提供这些类的子类，以覆盖默认行为以适应该DBAPI的附加功能，行为和怪癖。对于支持多个后端（pyodbc，zxJDBC，mxODBC）的DBAPI，方言模块将使用来自`sqlalchemy.connectors`包的mixins，它提供了所有后端通用的DBAPI功能，通常涉及connect参数。这意味着使用pyodbc，zxJDBC或mxODBC进行连接（实现时）在支持的后端之间非常一致。

由`create_engine()`使用的URL格式已得到增强，可以使用受JDBC启发的方案来处理特定后端的任意数量的DBAPI。以前的格式仍然有效，并且会选择一个“默认的”DBAPI实现，比如下面的Postgresql
URL，它将使用psycopg2：

    create_engine('postgresql://scott:tiger@localhost/test')

但是，要指定特定的DBAPI后端（例如pg8000），请使用加号“+”将其添加到URL的“协议”部分中：

    create_engine('postgresql+pg8000://scott:tiger@localhost/test')

重要的方言链接：

-   关于连接参数的文档：[http://www.sqlalchemy.org/docs/06/dbengine.html\#create](http://www.sqlalchemy.org/docs/06/dbengine.html#create)
    - engine-url-arguments。
-   单个方言的参考文件：[http：// ww](http://ww)
    w.sqlalchemy.org/docs/06/reference/dialects\_index.html
-   DatabaseNotes的提示和技巧。

有关方言的其他说明：

-   在SQLAlchemy
    0.6中，类型系统发生了巨大变化。这对所有有关命名约定，行为和实现的方言都有影响。请参阅下面的“类型”部分。
-   the `ResultProxy` object now offers a 2x speed
    improvement in some cases thanks to some refactorings.
-   the `RowProxy`, i.e. individual result row
    object, is now directly pickleable.
-   用于定位外部方言的setuptools入口点现在称为`sqlalchemy.dialects`。用0.4或0.5写的外部方言在任何情况下都需要修改为0.6，所以这种改变不会增加任何额外的困难。
-   方言现在在初始连接上收到initialize()事件以确定连接属性。
-   编译器生成的函数和运算符现在使用形式为“visit\_ ”和“visit\_
    \_fn”的（几乎）常规调度函数来提供定制的处理。 T1\>
    T0\>这代替了用直观的访问者方法复制编译器子类中的“函数”和“操作符”字典的需要，并且还允许编译器子类完全控制渲染，因为完整的\_Function或\_BinaryExpression对象被传入。

### Dialect Imports [¶](#dialect-imports "Permalink to this headline")

方言的进口结构发生了变化。每种方言现在通过`sqlalchemy.dialects.<name>`导出其基本“方言”类以及该方言支持的全套SQL类型。例如，要导入一组PG类型：

    from sqlalchemy.dialects.postgresql import INTEGER, BIGINT, SMALLINT,\
                                                VARCHAR, MACADDR, DATE, BYTEA

在上面，`INTEGER`实际上是`sqlalchemy.types`中普通的`INTEGER`类型，但是PG方言使它可以以与那些类型相同的方式是特定于PG的，如`BYTEA`和`MACADDR`。

表达式语言变化[¶](#expression-language-changes "Permalink to this headline")
----------------------------------------------------------------------------

### 重要的表达语言Gotcha [¶](#an-important-expression-language-gotcha "Permalink to this headline")

对于可能影响某些应用程序的表达式语言，有一个非常重要的行为变化。Python布尔表达式的布尔值，即`==`，`!=`以及类似的，现在可以精确地评估正在比较的两个子对象。

我们知道，将一个`ClauseElement`与任何其他对象进行比较都会返回另一个`ClauseElement`：

    >>> from sqlalchemy.sql import column
    >>> column('foo') == 5
    <sqlalchemy.sql.expression._BinaryExpression object at 0x1252490>

这样一来，Python表达式在转换为字符串时就会生成SQL表达式：

    >>> str(column('foo') == 5)
    'foo = :foo_1'

但是如果我们这样说会发生什么？

    >>> if column('foo') == 5:
    ...     print("yes")
    ...

在先前版本的SQLAlchemy中，返回的`_BinaryExpression`是一个普通的Python对象，其计算结果为`True`。现在，它计算实际的`ClauseElement`是否应该与正在比较的哈希值相同。含义：

    >>> bool(column('foo') == 5)
    False
    >>> bool(column('foo') == column('foo'))
    False
    >>> c = column('foo')
    >>> bool(c == c)
    True
    >>>

这意味着代码如下：

    if expression:
        print("the expression is:", expression)

如果`expression`是二进制子句，则不会评估。由于不应该使用上述模式，因此如果在布尔上下文中调用，基`ClauseElement`现在会引发异常：

    >>> bool(c)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      ...
        raise TypeError("Boolean value of this clause is not defined")
    TypeError: Boolean value of this clause is not defined

相反，想要检查`ClauseElement`表达式的代码应该如下所示：

    if expression is not None:
        print("the expression is:", expression)

请记住，**这也适用于Table和Column对象**。

改变的理由是双重的：

-   Comparisons of the form `if c1 == c2: <do something>` can actually be written now
-   支持`ClauseElement`对象的正确散列现在可用于其他平台，即Jython。直到此时，SQLAlchemy严重依赖于cPython在这方面的具体行为（并且偶尔还存在问题）。

### 更严格的“executemany”行为[¶](#stricter-executemany-behavior "Permalink to this headline")

SQLAlchemy中的“executemany”对应于对`execute()`的调用，传递一组绑定参数集：

    connection.execute(table.insert(), {'data':'row1'}, {'data':'row2'}, {'data':'row3'})

当`Connection`对象发送给定的用于编译的`insert()`结构时，它将传递给第一组绑定的键名传递给编译器，以确定该语句的VALUES子句。熟悉这个构造的用户会知道其余字典中存在的其他键没有任何影响。What’s
different now is that all subsequent dictionaries need to include at
least *every* key that is present in the first dictionary.
这意味着这样的调用不再有效：

    connection.execute(table.insert(),
                            {'timestamp':today, 'data':'row1'},
                            {'timestamp':today, 'data':'row2'},
                            {'data':'row3'})

因为第三行没有指定'timestamp'列。以前版本的SQLAlchemy只会为这些缺失的列插入NULL。但是，如果上面示例中的`timestamp`列包含Python方面的默认值或函数，则不会使用**。这是因为“executemany”操作已针对大量参数集的最大性能进行了优化，并且不会尝试评估那些缺少的键的Python方面的默认值。由于缺省值通常是作为与INSERT语句嵌入的SQL表达式实现的，或者是基于INSERT字符串结构触发的服务器端表达式，而INSERT字符串根据定义不能根据每个参数集有条件地触发，对于Python方面的默认行为与SQL
/服务器方面的默认行为是不一致的。（基于SQL表达式的默认值是嵌入到0.5系列中的，同样是为了尽量减少大量参数集的影响）。

SQLAlchemy
0.6因此通过禁止任何后续参数集将任何字段留空来建立可预测的一致性。这样，Python方面的默认值和函数就不再发生沉默的失败，并且允许在其行为与SQL和服务器端默认值之间保持一致。

### UNION和其他“复合”构造一致括号[¶](#union-and-other-compound-constructs-parenthesize-consistently "Permalink to this headline")

A rule that was designed to help SQLite has been removed, that of the
first compound element within another compound (such as, a
`union()` inside of an `except_()`) wouldn’t be parenthesized.
这是不一致的，并且在Postgresql上产生了错误的结果，PostgreSQL具有关于INTERSECTION的优先规则，并且它通常是一个惊喜。当在SQLite中使用复杂的组合时，现在需要将第一个元素转换为子查询（它也与PG兼容）。一个新的例子是在[[http://www.sqlalchemy.org/docs/06/sqlexpression.html](http://www.sqlalchemy.org/docs/06/sqlexpression.html)＃union-and-other-set-operations]结尾处的SQL表达式教程中。有关更多背景信息，请参阅[＃1665](http://www.sqlalchemy.org/trac/ticket/1665)和r6690。

C用于结果获取的扩展[¶](#c-extensions-for-result-fetching "Permalink to this headline")
--------------------------------------------------------------------------------------

The `ResultProxy` and related elements, including
most common “row processing” functions such as unicode conversion,
numerical/boolean conversions and date parsing, have been re-implemented
as optional C extensions for the purposes of performance.
这代表了SQLAlchemy通往“黑暗面”的路径的开始，我们希望通过重新实现C中的关键部分来继续提高性能。扩展可以通过指定`--with-cextensions`来构建，即` python setup.py  -  with  -  cextensions install` 。

The extensions have the most dramatic impact on result fetching using
direct `ResultProxy` access, i.e. that which is
returned by `engine.execute()`,
`connection.execute()`, or
`session.execute()`. 在由ORM `Query`对象返回的结果中，结果提取的开销比例不高，因此ORM性能稍微提高了一些，主要是提取大型结果集。性能改进高度依赖于正在使用的dbapi以及用于访问每行的列的语法（例如，`row['name']`比`row.name`当前的扩展对插入/更新/删除的速度没有影响，也没有改善SQL执行的延迟，也就是说，花费大部分时间执行很多结果集很少的语句的应用程序看不到太多的改进。

无论延期如何，性能在0.6和0.5之间都有所提高。A quick overview of what
connecting and fetching 50,000 rows looks like with SQLite, using mostly
direct SQLite access, a `ResultProxy`, and a simple
mapped ORM object:

    sqlite select/native: 0.260s

    0.6 / C extension

    sqlalchemy.sql select: 0.360s
    sqlalchemy.orm fetch: 2.500s

    0.6 / Pure Python

    sqlalchemy.sql select: 0.600s
    sqlalchemy.orm fetch: 3.000s

    0.5 / Pure Python

    sqlalchemy.sql select: 0.790s
    sqlalchemy.orm fetch: 4.030s

在上面，由于Python中的性能增强，ORM的读取速度比0.5快33％。有了C扩展，我们又得到了20％。However,
`ResultProxy` fetches improve by 67% with the C
extension versus not.
其他测试报告对于某些情况（例如发生大量字符串转换的情况）速度提高了200％。

新的模式功能[¶](#new-schema-capabilities "Permalink to this headline")
----------------------------------------------------------------------

`sqlalchemy.schema`包得到了一些长期需要的关注。最明显的变化是新扩展的DDL系统。在SQLAlchemy中，从版本0.5开始可以创建自定义的DDL字符串，并将它们与表或元数据对象关联：

    from sqlalchemy.schema import DDL

    DDL('CREATE TRIGGER users_trigger ...').execute_at('after-create', metadata)

现在，全套的DDL结构在相同的系统下可用，包括CREATE TABLE，ADD
CONSTRAINT等。:

    from sqlalchemy.schema import Constraint, AddConstraint

    AddContraint(CheckConstraint("value > 5")).execute_at('after-create', mytable)

此外，所有的DDL对象现在都是普通的`ClauseElement`对象，就像任何其他SQLAlchemy表达式对象一样：

    from sqlalchemy.schema import CreateTable

    create = CreateTable(mytable)

    # dumps the CREATE TABLE as a string
    print(create)

    # executes the CREATE TABLE statement
    engine.execute(create)

并使用`sqlalchemy.ext.compiler`扩展名，您可以创建自己的：

    from sqlalchemy.schema import DDLElement
    from sqlalchemy.ext.compiler import compiles

    class AlterColumn(DDLElement):

        def __init__(self, column, cmd):
            self.column = column
            self.cmd = cmd

    @compiles(AlterColumn)
    def visit_alter_column(element, compiler, **kw):
        return "ALTER TABLE %s ALTER COLUMN %s %s ..." % (
            element.column.table.name,
            element.column.name,
            element.cmd
        )

    engine.execute(AlterColumn(table.c.mycolumn, "SET DEFAULT 'test'"))

### 已弃用/已删除模式元素[¶](#deprecated-removed-schema-elements "Permalink to this headline")

模式包也大大简化了。许多在0.5中被弃用的选项和方法已被删除。其他鲜为人知的访问器和方法也被删除。

-   “所有者”关键字参数将从`Table`中删除。使用“模式”来表示任何名称空间要预先添加到表名中。
-   不推荐使用`MetaData.connect()`和`ThreadLocalMetaData.connect()` -
    发送“绑定”属性来绑定元数据。
-   不推荐使用metadata.table\_iterator()方法（使用sorted\_tables）
-   “元数据”参数从`DefaultGenerator`和子类中移除，但保持本地存在于`Sequence`上，这是DDL中的独立构造。
-   不推荐使用`PassiveDefault` -
    使用`DefaultClause`。
-   从`Index`和`Constraint`对象中删除了公共可变性：
    -   `ForeignKeyConstraint.append_element()`
    -   `Index.append_column()`
    -   `UniqueConstraint.append_column()`
    -   `PrimaryKeyConstraint.add()`
    -   `PrimaryKeyConstraint.remove()`

这些应该以声明方式构建（即在一个构造中）。

-   其他删除的东西：
    -   `Table.key`（不知道这是什么）
    -   `Column.bind`（通过column.table.bind获取）
    -   `Column.metadata`（通过column.table.metadata获取）
    -   `Column.sequence`（使用column.default）

### 其他行为改变[¶](#other-behavioral-changes "Permalink to this headline")

-   `UniqueConstraint`, `Index`,
    `PrimaryKeyConstraint` all accept lists of
    column names or column objects as arguments.
-   `ForeignKey`上的`use_alter`标志现在是可以使用`DDL()`事件系统手动构建的操作的快捷选项。A side effect of this
    refactor is that `ForeignKeyConstraint` objects
    with `use_alter=True` will *not* be emitted on
    SQLite, which does not support ALTER for foreign keys.
    这对SQLite的行为没有影响，因为SQLite实际上没有兑现FOREIGN KEY约束。
-   `Table.primary_key`不可分配 -
    使用`table.append_constraint(PrimaryKeyConstraint(...))`
-   带有`ForeignKey`的`Column`定义，并且没有类型，例如`Column(name, ForeignKey(sometable.c.somecol))` used to get the type of the referenced column.
    现在对该自动类型推断的支持是部分的，可能不适用于所有情况。

记录打开了[¶](#logging-opened-up "Permalink to this headline")
--------------------------------------------------------------

在这里和那里需要额外的方法调用，您可以在创建引擎，池或映射器后设置INFO和DEBUG的日志级别，并开始记录。The
`isEnabledFor(INFO)` method is now called
per-`Connection` and `isEnabledFor(DEBUG)` per-`ResultProxy` if already enabled on
the parent connection. 池日志记录发送到`log.info()`和`log.debug()` - 没有检查 -
请注意池检出/检入通常是每个事务一次。

反射/督察API [¶](#reflection-inspector-api "Permalink to this headline")
------------------------------------------------------------------------

反射系统允许通过`Table（'sometable'， 元数据， autoload = True）反映表格列。  t0 >已经被开放到它自己的细粒度API中，它允许直接检查数据库元素，如表，列，约束，索引等。`此API将返回值表示为字符串，字典和`TypeEngine`对象的简单列表。现在，`autoload=True`的内部建立在这个系统上，原始数据库信息到`sqlalchemy.schema`结构的转换是集中的，大大简化了个别方言的契约减少不同后端之间的错误和不一致性。

要使用检查员：

    from sqlalchemy.engine.reflection import Inspector
    insp = Inspector.from_engine(my_engine)

    print(insp.get_schema_names())

`from_engine()`方法在某些情况下会为后端特定的检查器提供额外的功能，例如提供`get_table_oid()`方法的Postgresql：

    my_engine = create_engine('postgresql://...')
    pg_insp = Inspector.from_engine(my_engine)

    print(pg_insp.get_table_oid('my_table'))

返回支持[¶](#returning-support "Permalink to this headline")
------------------------------------------------------------

现在，`insert()`，`update()`和`delete()`结构支持`returning()`方法，对应于由Postgresql，Oracle，MS-SQL和Firebird支持的SQL
RETURNING子句。目前不支持任何其他后端。

以与`select()`结构相同的方式给出列表达式的列表，这些列的值将作为常规结果集返回：

    result = connection.execute(
                table.insert().values(data='some data').returning(table.c.id, table.c.timestamp)
            )
    row = result.first()
    print("ID:", row['id'], "Timestamp:", row['timestamp'])

在四个受支持的后端之间执行RETURNING的方式各不相同，在Oracle需要复杂地使用OUT参数的情况下，这些参数被重新路由到“模拟”结果集中，而MS-SQL使用尴尬的SQL语法。RETURNING的使用受到限制：

-   它不适用于任何“executemany()”执行风格。这是所有支持的DBAPI的限制。
-   一些后端（如Oracle）仅支持返回单行的RETURNING -
    这包括UPDATE和DELETE语句，这意味着update()或delete()构造必须仅匹配单行，否则会引发错误（由Oracle提供，而不是SQLAlchemy的）。

RETURNING也被SQLAlchemy自动使用（当可用时以及未通过明确的`returning()`调用指定）时，为单行INSERT语句获取新生成的主键值。这意味着对于需要主键值的插入语句，不再需要“SELECT
nextval（sequence）”预执行。真相被告知，隐式RETURNING特性比旧的“select
nextval()”系统带来更多的方法开销，该系统使用快速和肮脏的cursor.execute()来获取序列值，并且在Oracle需要额外绑定的输出参数。因此，如果方法/协议开销比其他数据库往返行程更昂贵，则可以通过将`implicit_returning=False`指定为`create_engine()`来禁用该功能。

输入系统更改[¶](#type-system-changes "Permalink to this headline")
------------------------------------------------------------------

### 新Archicture [¶](#new-archicture "Permalink to this headline")

该类型系统已经在幕后完全重新编制，以提供两个目标：

-   从类型本身的SQL规范中分离对绑定参数和结果行值（通常是DBAPI要求）的处理，这是数据库要求。这与将数据库SQL行为与DBAPI分离的整体方言重构是一致的。
-   根据`TypeEngine`对象生成DDL并根据列反射构建`TypeEngine`对象，从而建立清晰一致的契约。

这些变化的重点包括：

-   方言内部类型的建设已经彻底改变。方言现在将公开可用的类型定义为大写名称，而内部实现类型使用下划线标识符（即私有）。用SQL和DDL表示类型的系统已被移至编译器系统。这具有大部分方言中的类型对象少得多的效果。关于这种方言作者的体系结构的详细文档在[source：/
    lib / sqlalc hemy / dialects\_type\_migration\_guidelines.txt]中。
-   类型的反射现在返回types.py中的确切类型，如果类型不是标准的SQL类型，则返回方言本身的UPPERCASE类型。这意味着现在反射会返回关于反射类型的更准确信息。
-   用户定义的类型继承`TypeEngine`并希望提供`get_col_spec()`现在应该是`UserDefinedType`的子类。
-   所有类型的`result_processor()`方法现在接受一个附加参数`coltype`。这是附加到cursor.description的DBAPI类型对象，应该在适用时使用，以便更好地决定应返回哪种结果处理可调用。理想情况下，处理器功能永远不需要使用`isinstance()`，这在这个级别上是一个昂贵的调用。

### 本机Unicode模式[¶](#native-unicode-mode "Permalink to this headline")

由于更多的DBAPI支持直接返回Python
unicode对象，因此现在基础语言会对第一个连接执行检查，该连接将确定DBAPI是否返回Python
unicode对象，以用于基本选择VARCHAR值。如果是这样，`String`类型和所有子类（即`Text`，`Unicode`等）将在收到结果行时跳过“unicode”检查/转换步骤。这为大型结果集提供了显着的性能提升。目前已知“unicode模式”适用于：

-   sqlite3 / pysqlite
-   psycopg2 - SQLA
    0.6现在在每个psycopg2连接对象上默认使用“UNICODE”类型扩展
-   pg8000
-   cx\_oracle（我们使用输出处理器 - 很好的功能！）

其他类型可以根据需要选择禁用unicode处理，例如与MS-SQL一起使用时的`NVARCHAR`类型。

特别是，如果基于先前返回非Unicode字符串的DBAPI移植应用程序，则“本地unicode”模式具有明显不同的默认行为
- 声明为`String`或`VARCHAR`现在默认返回unicode，而他们之前会返回字符串。这可能会破坏需要非Unicode字符串的代码。通过将`use_native_unicode=False`传递给`create_engine()`，可以禁用psycopg2“native unicode”模式。

对于明确不需要unicode对象的字符串列更通用的解决方案是使用将unicode转换回utf-8或任何所需的`TypeDecorator`：

    class UTF8Encoded(TypeDecorator):
        """Unicode type which coerces to utf-8."""

        impl = sa.VARCHAR

        def process_result_value(self, value, dialect):
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            return value

请注意，`assert_unicode`标志现在已被弃用。SQLAlchemy允许DBAPI和后端数据库在可用时处理Unicode参数，并且不会通过检查传入类型来增加操作开销；像sqlite和Postgresql这样的现代系统如果传递了无效的数据，将会在它们的末尾产生编码错误。在SQLAlchemy确实需要将Python
Unicode绑定参数强制转换为编码字符串，或者明确使用Unicode类型的情况下，如果对象是字符串，则会引发警告。可以使用Python警告过滤器来记录此警告，或将其转换为异常：[http://docs.python.org/library/warnings.html](http://docs.python.org/library/warnings.html)

### 通用枚举类型[¶](#generic-enum-type "Permalink to this headline")

我们现在在`types`模块中有一个`Enum`。这是一个字符串类型，它被赋予了一系列“标签”，这些标签约束了赋予这些标签的可能值。默认情况下，此类型使用最大标签的大小生成`VARCHAR`，并将CREATE约束应用于CREATE
TABLE语句中的表。当使用MySQL时，默认情况下类型使用MySQL的ENUM类型，并且在使用Postgresql时，类型将使用`CREATE TYPE ＆lt； mytype＆gt； AS ENUM`。为了使用Postgresql创建类型，必须为构造函数指定`name`参数。该类型还接受`native_enum=False`选项，该选项将为所有数据库发出VARCHAR /
CHECK策略。请注意，Postgresql ENUM类型目前不适用于pg8000或zxjdbc。

### 反射返回方言特定类型[¶](#reflection-returns-dialect-specific-types "Permalink to this headline")

反射现在返回数据库中可能的最具体类型。也就是说，如果您使用`String`创建表，然后将其反映回来，则反映的列可能会是`VARCHAR`。对于支持更具体形式的方言，这就是你会得到的。所以一个`Text`类型会在Oracle上返回为`oracle.CLOB`，一个`LargeBinary`可能是一个`mysql.MEDIUMBLOB`等等这里的明显优势是反射保留了数据库必须说明的尽可能多的信息。

一些在表格元数据中大量使用的应用程序可能希望在反映的表格和/或未反映的表格中比较类型。在`TypeEngine`上有一个名为`_type_affinity`和相关联的比较帮助器`_compare_type_affinity`的半私人访问器。该访问器返回类型对应的“generic”`types`类：

    >>> String(50)._compare_type_affinity(postgresql.VARCHAR(50))
    True
    >>> Integer()._compare_type_affinity(mysql.REAL)
    False

### 其他API更改[¶](#miscellaneous-api-changes "Permalink to this headline")

通常的“通用”类型仍然是使用中的一般系统，即`String`，`Float`，`DateTime`。这里有一些变化：

-   类型不再对默认参数进行猜测。In particular, `Numeric`, `Float`, as well as subclasses
    NUMERIC, FLOAT, DECIMAL don’t generate any length or scale unless
    specified. 这也继续包括有争议的`String`和`VARCHAR`类型（尽管当MySQL被要求渲染VARCHAR的时候，方言会先发制人）。假定没有默认值，并且如果在CREATE
    TABLE语句中使用它们，则如果底层数据库不允许这些类型的非延长版本，则会引发错误。
-   对于BLOB / BYTEA /类似的类型，`Binary`类型已重命名为`LargeBinary`。对于`BINARY`和`VARBINARY`，它们直接存在于`types.BINARY`，`types.VARBINARY`中，以及MySQL和MS-SQL方言。
-   `PickleType` now uses == for comparison of
    values when mutable=True, unless the “comparator” argument with a
    comparison function is specified to the type.
    如果您正在酸洗自定义对象，则应实施`__eq__()`方法，以便基于值的比较准确无误。
-   Numeric和Float的默认“precision”和“scale”参数已被删除，现在默认为None。除非提供这些值，否则默认情况下NUMERIC和FLOAT将不带数字参数呈现。
-   SQLite上的DATE，TIME和DATETIME类型现在可以采用可选的“storage\_format”和“regexp”参数。“storage\_format”可用于使用自定义字符串格式存储这些类型。“regexp”允许使用自定义正则表达式来匹配数据库中的字符串值。
-   不再支持SQLite `Time`和`DateTime`类型的`__legacy_microseconds__`类型。您应该使用新的“storage\_format”参数。
-   `DateTime` types on SQLite now use by a default
    a stricter regular expression to match strings from the database.
    如果您使用以旧格式存储的数据，请使用新的“regexp”参数。

ORM更改[¶](#orm-changes "Permalink to this headline")
-----------------------------------------------------

将ORM应用程序从0.5升级到0.6应该几乎不需要更改，因为ORM的行为几乎完全相同。有一些默认参数和名称更改，并且一些加载行为已得到改进。

### 新工作单元[¶](#new-unit-of-work "Permalink to this headline")

工作单元的内部结构，主要是`topological.py`和`unitofwork.py`，已经完全重写并大大简化。这应该对使用没有任何影响，因为在刷新过程中所有现有行为都完全保持（或者至少在我们的测试套件和少量生产环境经过严格测试的情况下）。flush()的性能现在使用少20-30％的方法调用，并且应该使用更少的内存。现在应该相当容易地遵循源代码的意图和流程，并且在这一点上flush的架构相当开放，为潜在的复杂领域创造空间。刷新过程不再依赖于递归，因此可以刷新任意大小和复杂度的刷新计划。此外，映射程序的“保存”过程发出INSERT和UPDATE语句，现在缓存两个语句的“编译”形式，以便通过非常大的刷新进一步显着减少callcounts。

使用flush或早期版本的0.6或0.5观察到的任何行为变化都应尽快报告给我们 -
我们将确保没有功能丢失。

### 对`query.update()`和`query.delete()` [的更改](#changes-to-query-update-and-query-delete "Permalink to this headline")

-   query.update()的'expire'选项已被重命名为'fetch'，因此与query.delete()的匹配。
-   `query.update()` and `query.delete()` both default to ‘evaluate’ for the synchronize strategy.
-   update()和delete()的“同步”策略会在失败时产生错误。没有隐含的回退到“获取”。评估失败是基于标准的结构，所以成功/失败是基于代码结构的确定性。

### `relation()`被正式命名为`relationship()` [¶](#relation-is-officially-named-relationship "Permalink to this headline")

这解决了长期存在的问题，即“关系”是指关系代数术语中的“表或派生表”。`relation()`这个名字很少打字，在可预见的未来将继续存在，所以这种改变应该完全没有问题。

### 子查询加载[¶](#subquery-eager-loading "Permalink to this headline")

一种新型的热切加载被称为“子查询”加载。这是一个负载，在首次加载第一个查询中所有父项的完整集合后，立即发出第二个SQL查询，并使用INNER
JOIN向上连接到父项。Subquery loading is used simlarly to the current
joined-eager loading, using the ``` `subqueryload()`` ``` and ``` ``subqueryload_all()`` ``` options
as well as the ``` ``lazy='subquery'`` ``` setting
on ``` ``relationship()` ```.
子查询加载通常会更加高效地加载许多较大的集合，因为它无条件地使用INNER
JOIN，并且不会重新加载父行。

### ``` `eagerload()`` ```, ``` ``eagerload_all()`` ``` is now ``` ``joinedload()`` ```, ``` ``joinedload_all()` ```[¶](#eagerload-eagerload-all-is-now-joinedload-joinedload-all "Permalink to this headline")

To make room for the new subquery load feature, the existing
``` `eagerload()`` ```/``` ``eagerload_all()`` ``` options are
now superseded by ``` ``joinedload()`` ``` and
``` ``joinedload_all()`` ```.
就像``` ``relation()` ```一样，旧名字在可预见的未来将继续存在。

### ``` `lazy=False|None|True|'dynamic'`` ``` now accepts ``` ``lazy='noload'|'joined'|'subquery'|'select'|'dynamic'` ```[¶](#lazy-false-none-true-dynamic-now-accepts-lazy-noload-joined-subquery-select-dynamic "Permalink to this headline")

Continuing on the theme of loader strategies opened up, the standard
keywords for the ``` `lazy`` ``` option on
``` ``relationship()`` ``` are now
``` ``select`` ``` for lazy loading (via a SELECT
issued on attribute access), ``` ``joined`` ``` for
joined-eager loading, ``` ``subquery`` ``` for
subquery-eager loading, ``` ``noload`` ``` for no
loading should occur, and ``` ``dynamic`` ``` for a
“dynamic” relationship. 旧的``` ``True`` ```，``` ``False`` ```，``` ``None` ```参数仍被接受，其行为与以前一样。

### innerjoin =关于关系的True，joinedload [¶](#innerjoin-true-on-relation-joinedload "Permalink to this headline")

现在可以指示联合加载的标量和集合使用INNER JOIN而不是OUTER
JOIN。在Postgresql上，据观察，在某些查询中提供了300-600％的加速比。将此标志设置为任何多对一的不可空外键，对于任何保证相关项目存在的集合也是如此。

在mapper级别：

    mapper(Child, child)
    mapper(Parent, parent, properties={
        'child':relationship(Child, lazy='joined', innerjoin=True)
    })

在查询时间级别：

    session.query(Parent).options(joinedload(Parent.child, innerjoin=True)).all()

`relationship()`级别的`innerjoin=True`标志也将对任何不覆盖该值的`joinedload()`选项生效。

### 多对一的增强功能[¶](#many-to-one-enhancements "Permalink to this headline")

-   多对一的关系现在会在更少的情况下触发延迟加载，包括在大多数情况下不会在更换新代码时获取“旧”值。

-   与连接表子类的多对一关系现在使用get()作为简单加载（称为“use\_get”条件），即`Related` - \>“Sub（Base）
    ，而不需要根据基表重新定义主连接条件。[票：1186]

-   指定具有声明列的外键，即`ForeignKey(MyRelatedClass.id)`不会破坏发生的“use\_get”条件[ticket：1492]

-   relationship()，joinedload()和joinedload\_all()现在具有一个名为“innerjoin”的选项。指定`True`或`False`来控制是否将渴望连接构造为INNER或OUTER连接。与往常一样，默认为`False`。映射器选项将覆盖关系()中指定的任何设置。通常应该设置为多对一，而不是可空的外键关系，以提高连接性能。[票：1544]

-   当LIMIT /
    OFFSET出现时，加入的预加载的行为使得主查询被包装在子查询中，现在对于所有紧急加载是多对一连接的情况都是例外。在这种情况下，由于多对一连接不会将行添加到结果中，所以急切连接与限制/偏移一起直接与父表对齐，而无需额外的子查询开销。

    例如，在0.5这个查询中：

        session.query(Address).options(eagerload(Address.user)).limit(10)

    会产生如下的SQL：

        SELECT * FROM
          (SELECT * FROM addresses LIMIT 10) AS anon_1
          LEFT OUTER JOIN users AS users_1 ON users_1.id = anon_1.addresses_user_id

    这是因为任何渴望加载器的存在表明它们中的一些或全部可能涉及多行集合，这将需要在子查询内包装任何种类的行计数敏感修饰符，如LIMIT。

    在0.6中，该逻辑更加敏感，并且可以检测所有渴望的加载器是否表示多对一，在这种情况下，渴望加入不会影响rowcount：

        SELECT * FROM addresses LEFT OUTER JOIN users AS users_1 ON users_1.id = addresses.user_id LIMIT 10

### 加入表继承的可变主键[¶](#mutable-primary-keys-with-joined-table-inheritance "Permalink to this headline")

一个连接表继承配置，其中子表具有PK，现在可以在支持CASCADE的数据库（如Postgresql）上更新父PK的外键。`mapper()`现在有一个选项`passive_updates=True`，表示这个外键会自动更新。如果在像SQLite或MySQL /
MyISAM这样的非级联数据库上，将该标志设置为`False`。未来的功能增强将尝试使此标志根据使用的方言/表格样式进行自动配置。

### 烧杯缓存[¶](#beaker-caching "Permalink to this headline")

Beaker集成的一个有希望的新例子是在`examples/beaker_caching`中。这是一个直接的方法，它在`Query`的结果生成引擎中应用Beaker缓存。缓存参数通过`query.options()`提供，并允许完全控制缓存的内容。SQLAlchemy
0.6包含对`Session.merge()`方法的改进以支持此类和类似的配方，并在大多数情况下提供显着改进的性能。

### 其他更改[¶](#other-changes "Permalink to this headline")

-   当选择多个列/实体时，由`Query`返回的“行元组”对象现在可以被选择以及更高的性能。
-   `query.join()`已被重新设计，以提供更一致的行为和更多的灵活性（包括[ticket：1537]）
-   `query.select_from()` accepts multiple clauses
    to produce multiple comma separated entries within the FROM clause.
    从多宿主连接()子句中选择时很有用。
-   `Session.merge()`上的“dont\_load =
    True”标志已弃用，现在为“load = False”。
-   添加了“make\_transient()”辅助函数，该函数将持久性/分离性实例转换为临时性实例（即，删除instance\_key并从任何会话中删除）。[票：1052]
-   mapper()上的allow\_null\_pks标志已弃用，并已重命名为allow\_partial\_pks。它默认打开。这意味着对于任何主键列都有一个非空值的行将被视为一个标识。通常只有在映射到外部联接时才需要此方案。当设置为False时，其中包含NULL的PK不会被视为主键
    -
    特别是这意味着结果行将返回为无（或未填充到集合中），0.6中的新值也表示会话.merge()不会针对这样的PK值向数据库进行往返。[票：1680]
-   “backref”的机制已完全合并到更细粒度的“back\_populates”系统中，并完全发生在`RelationProperty`的`_generate_backref()`方法中。这使得`RelationProperty`的初始化过程更加简单，并且可以更轻松地将设置（例如`RelationProperty`的子类）传播到反向引用中。内部`BackRef()`消失，`backref()`返回`RelationProperty`可理解的普通元组。
-   the keys attribute of `ResultProxy` is now a
    method, so references to it (`result.keys`) must
    be changed to method invocations (`result.keys()`)
-   `ResultProxy.last_inserted_ids` is now
    deprecated, use `ResultProxy.inserted_primary_key` instead.

### 已弃用/已删除ORM元素[¶](#deprecated-removed-orm-elements "Permalink to this headline")

大多数在整个0.5版本中被弃用的元素和提出的弃用警告已被删除（有一些例外）。所有标记为“等待折旧”的元素现在都被弃用，并会在使用后引发警告。

-   sessionmaker()上的'transactional'标志被删除。使用'autocommit =
    True'来表示'transactional = False'。
-   mapper()上的'polymorphic\_fetch'参数被删除。加载可以使用'with\_polymorphic'选项进行控制。
-   mapper()上的'select\_table'参数被删除。为此功能使用'with\_polymorphic
    =（“\*”，）'。
-   同义词()的'代理'参数被删除。这个标志在整个0.5中没有做任何事情，因为“代理生成”行为现在是自动的。
-   不推荐将单个元素列表传递给joinedload()，joinedload\_all()，contains\_eager()，lazyload()，defer()和undefer()而不是多个位置\*参数。
-   将单个元素列表传递给query.order\_by()，query.group\_by()，query.join()或query.outerjoin()而不是多个位置\*参数已弃用。
-   `query.iterate_instances()`被删除。使用`query.instances()`。
-   `Query.query_from_parent()`被删除。Use the
    sqlalchemy.orm.with\_parent() function to produce a “parent” clause,
    or alternatively `query.with_parent()`.
-   `query._from_self()`被删除，改为使用`query.from_self()`。
-   composite()的“comparator”参数被删除。使用“comparator\_factory”。
-   `RelationProperty._get_join()` is removed.
-   Session上的'echo\_uow'标志被删除。在“sqlalchemy.orm.unitofwork”名称上使用日志记录。
-   `session.clear()` is removed.
    使用`session.expunge_all()`。
-   `session.save()`, `session.update()`, `session.save_or_update()` are
    removed. 使用`session.add()`和`session.add_all()`。
-   session.flush()上的“objects”标志仍然被弃用。
-   session.merge()中的“dont\_load = True”标志不赞成使用“load = False”。
-   `ScopedSession.mapper` remains deprecated.
    请参阅[http://www.sqlalchemy.org/trac/wiki/Usag](http://www.sqlalchemy.org/trac/wiki/Usag)
    eRecipes / SessionAwareMapper中的使用配方
-   将`InstanceState`（内部SQLAlchemy状态对象）传递给`attributes.init_collection()`或`attributes.get_history()`已弃用。这些函数是公共API，通常需要一个常规的映射对象实例。
-   `declarative_base()`的'engine'参数被删除。使用'bind'关键字参数。

扩展程序[¶ T0\>](#extensions "Permalink to this headline")
----------------------------------------------------------

### SQLSoup [¶ T0\>](#sqlsoup "Permalink to this headline")

SQLSoup已经过现代化和更新，以反映0.5 /
0.6的常见功能，包括定义明确的会话集成。请阅读[[http：//www.sqlalc](http://www.sqlalc)
hemy.org/docs/06/reference/ext/sqlsoup.html]上的新文档。

### 声明[¶ T0\>](#declarative "Permalink to this headline")

`DeclarativeMeta`（`declarative_base`的默认元类）先前允许子类修改`dict_`以添加类属性（例如列）。这不再起作用，`DeclarativeMeta`构造函数现在忽略`dict_`。相反，类属性应该直接分配，例如，应该使用`cls.id=Column(...)`，或者[MixIn
class](http://www.sqlalchemy.org/docs/reference/ext/declarative.html#mix-in-classes)方法来代替元类方法。
