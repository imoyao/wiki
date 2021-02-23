---
title: migration_07
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/aec63a/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
SQLAlchemy 0.7有哪些新特性？[¶](#what-s-new-in-sqlalchemy-0-7 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍了2012年5月5日发布的SQLAlchemy版本0.6和2012年10月发布的SQLAlchemy版本0.7之间的更改。

文件日期：2011年7月27日

引言[¶ T0\>](#introduction "Permalink to this headline")
--------------------------------------------------------

本指南介绍了SQLAlchemy
0.7版中的新增功能，并介绍了影响用户将其应用程序从0.6系列SQLAlchemy迁移到0.7的更改。

在尽可能高的程度上，进行更改的方式不会中断与为0.6构建的应用程序的兼容性。这些必须不是向后兼容的更改很少，除了一个之外，对可变属性默认值的更改都会影响应用程序的极小部分
- 许多更改都涉及非公共API和某些用户可能已无记录的黑客攻击试图使用。

还记录了第二类甚至更小的非向后兼容更改。这类更改将至少从0.5版本开始被弃用的那些功能和行为视为已弃用，并且自从弃用以来一直提出警告。这些更改只会影响仍在使用0.4或早期0.5样式API的应用程序。随着项目的成熟，我们对0.x级别版本的这些变化越来越少，这是我们API的产品具有越来越少的特性，这些特性对于他们要解决的用例而言并不理想。

SQLAlchemy
0.7中已经取代了一系列现有功能。“被取代”和“不推荐”这两个术语之间没有太大区别，只是前者对旧功能的建议太弱了。在0.7中，像`synonym`和`comparable_property`以及所有`Extension`和其他事件类的功能已被取代。但是这些“被取代”的功能已经被重新实现，因此它们的实现大部分都是在核心ORM代码之外生存，所以它们继续“徘徊”不会影响SQLAlchemy进一步精简和优化其内部的能力，我们希望它们保持不变在可预见的未来API内。

新功能[¶](#new-features "Permalink to this headline")
-----------------------------------------------------

### 新事件系统[¶](#new-event-system "Permalink to this headline")

SQLAlchemy很早就开始使用`MapperExtension`类，该类提供了映射器持久化周期的钩子。随着SQLAlchemy迅速变得更加组件化，将映射器推进到更加关注的配置角色中，弹出了更多的“扩展”，“侦听器”和“代理”类，以特殊方式解决各种活动拦截用例。Part
of this was driven by the divergence of activities;
`ConnectionProxy` objects wanted to provide a system
of rewriting statements and parameters; `AttributeExtension` provided a system of replacing incoming values, and
`DDL` objects had events that could be switched off
of dialect-sensitive callables.

0.7使用全新的统一方法重新实现了所有这些插件点，该方法保留了不同系统的所有功能，提供了更大的灵活性和更少的样板，性能更好，并且无需为每个事件子系统学习截然不同的API
。The pre-existing classes `MapperExtension`,
`SessionExtension`, `AttributeExtension`, `ConnectionProxy`,
`PoolListener` as well as the
`DDLElement.execute_at` method are deprecated and
now implemented in terms of the new system - these APIs remain fully
functional and are expected to remain in place for the foreseeable
future.

新方法使用命名事件和用户定义的可调参数将活动与事件相关联。API的外观和感觉受到JQuery，Blinker和Hibernate等多种来源的驱动，并且在与几十个用户在Twitter上的会议期间进行了几次进一步修改，这些用户似乎比邮件列表的响应率高得多这样的问题。

它还具有目标规范的开放式系统，允许将事件与API类相关联，例如所有`Session`或`Engine`对象与API类的特定实例，比如针对特定的`Pool`或`Mapper`，以及相关对象（如映射的用户定义类），或者特定于特定属性映射父类的特定子类。单独的监听器子系统可以将包装应用到传入的用户定义的监听器函数中，这些函数修改了它们的调用方式
-
映射器事件可以接收正在被操作的对象的实例或其底层的`InstanceState`对象。属性事件可以选择是否有返回新值的责任。

现在有几个系统基于新的事件API，包括新的“可变属性”API以及复合属性。对事件的强调也导致了一些新的事件的引入，包括属性到期和刷新操作，酸洗加载/转储操作，完成的映射器构建操作。

也可以看看

[Events](core_event.html)

[＃1902 T0\>](http://www.sqlalchemy.org/trac/ticket/1902)

### Hybrid属性，implements / supersedes同义词()，comparable\_property()[¶](#hybrid-attributes-implements-supersedes-synonym-comparable-property "Permalink to this headline")

“派生属性”示例现在已经变成官方扩展。`synonym()`的典型用例是提供对映射列的描述符访问；
`comparable_property()`的用例应该能够从任何描述符中返回一个`PropComparator`。在实践中，“派生”的方法更容易使用，更具可扩展性，在几十行纯Python中实现，几乎不需要导入，并且不需要ORM内核甚至不需要知道它。该功能现在称为“混合属性”扩展。

`synonym()` and `comparable_property()` are still part of the ORM, though their implementations have
been moved outwards, building on an approach that is similar to that of
the hybrid extension, so that the core ORM mapper/query/property modules
aren’t really aware of them otherwise.

也可以看看

[Hybrid Attributes](orm_extensions_hybrid.html)

[＃1903 T0\>](http://www.sqlalchemy.org/trac/ticket/1903)

### 速度增强[¶](#speed-enhancements "Permalink to this headline")

按照所有主要SQLA版本的习惯，通过内部广泛传递来减少开销和呼叫计数，这进一步减少了常见场景中所需的工作。此版本的亮点包括：

-   对于主键已经存在的行，刷新过程现在将INSERT语句捆绑到提供给`cursor.executemany()`的批处理中。特别是，这通常适用于连接表继承配置上的“子”表，这意味着对于连接表对象的大批量插入，对`cursor.execute`的调用次数可以减半，允许对传递给`cursor.executemany()`的语句进行本地DBAPI优化（例如重新使用预准备语句）。
-   在访问已加载的相关对象的多对一引用时调用的代码路径已大大简化。直接检查身份映射而不需要首先生成新的`Query`对象，这在需要访问的数千个内存中的多对一的情况下是昂贵的。构造的每个调用“加载器”对象的用法也不再用于大多数惰性属性加载。
-   当映射器内部访问flush中的映射属性时，组合的重写允许更短的代码路径。
-   当“保存更新”和其他级联操作需要在与属性关联的数据成员的全部范围内级联时，新的内联属性访问功能取代了之前“历史”的用法。这可以降低为此速度关键操作生成新的`History`对象的开销。
-   内联的`ExecutionContext`，与语句执行相对应的对象已被内联和简化。
-   现在缓存每个语句执行的类型生成的`bind_processor()`和`result_processor()`可调集（仔细地避免ad-hoc类型和方言的内存泄漏）为了这种类型的生命周期，进一步减少了每个语句的调用开销。
-   语句的特定`Compiled`实例的“绑定处理器”集合也缓存在`Compiled`对象上，进一步利用了flush的“编译缓存”进程重新使用INSERT，UPDATE，DELETE语句的相同编译形式。

包含样本基准测试脚本的callcount简化示例位于[http://techspot.zzzeek.org/2010/12/12/a-tale-of-three](http://techspot.zzzeek.org/2010/12/12/a-tale-of-three)
- 配置文件/

### 复写重写[¶](#composites-rewritten "Permalink to this headline")

“复合”功能已被重写，如`synonym()`和`comparable_property()`，以使用基于描述符和事件的更轻量级实现，而不是构建到ORM内部。这允许从映射器/工作单元的内部消除一些延迟，并且简化了组合的工作。复合属性现在不再隐藏它构建的基础列，现在它们仍然是常规属性。复合材料也可以作为`relationship()`以及`Column()`属性的代理。

主要的向后不兼容的复合变化是他们不再使用`mutable=True`系统来检测原位突变。请使用[突变跟踪](http://www.sqlalchemy.org/docs/07/orm_extensions_mutable.html)扩展名来为现有的组合使用情况建立就地更改事件。

也可以看看

[Composite Column Types](orm_composites.html#mapper-composite)

[Mutation Tracking](orm_extensions_mutable.html)

[＃2008](http://www.sqlalchemy.org/trac/ticket/2008)
[＃2024](http://www.sqlalchemy.org/trac/ticket/2024)

### query.join（target，onclause）[¶](#more-succinct-form-of-query-join-target-onclause "Permalink to this headline")的更简洁的形式

现在使用显式语句向目标发布`query.join()`的默认方法是：

    query.join(SomeClass, SomeClass.id==ParentClass.some_id)

在0.6中，这个用法被认为是一个错误，因为`join()`接受多个对应于多个JOIN子句的参数 -
两个参数形式需要在一个元组中以消除单参数和双参数连接目标。在0.6的中间，我们为这种特定的调用风格增加了检测和错误消息，因为它很常见。在0.7中，由于我们无论如何都在检测确切的模式，并且由于不必理由地键入元组是非常烦人的，所以非元组方法现在变成了“正常”的方式。与单连接情况相比，“多JOIN”用例非常罕见，并且通过多次调用`join()`可以更清楚地表示多个连接。

元组表单将保持向后兼容。

请注意，`query.join()`的所有其他形式保持不变：

    query.join(MyClass.somerelation)
    query.join("somerelation")
    query.join(MyTarget)
    # ... etc

[使用连接查询](http://www.sqlalchemy.org/docs/07/orm_tutorial.html#querying-with-joins)

[＃1923 T0\>](http://www.sqlalchemy.org/trac/ticket/1923)

### 突变事件扩展，取代“mutable = True”[¶](#mutation-event-extension-supersedes-mutable-true "Permalink to this headline")

一个新的扩展[Mutation
Tracking](orm_extensions_mutable.html)提供了一种机制，通过该机制，用户定义的数据类型可以将改变事件提供给拥有的父母或父母。The
extension includes an approach for scalar database values, such as those
managed by [`PickleType`](core_type_basics.html#sqlalchemy.types.PickleType "sqlalchemy.types.PickleType"),
`postgresql.ARRAY`, or other custom
`MutableType` classes, as well as an approach for
ORM “composites”, those configured using [`composite()`](orm_composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite").

也可以看看

[Mutation Tracking](orm_extensions_mutable.html)

### NULLS FIRST / NULLS LAST运算符[¶](#nulls-first-nulls-last-operators "Permalink to this headline")

这些被实现为`asc()`和`desc()`运算符的扩展，称为`nullsfirst()`和`nullslast()`

也可以看看

[`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")

[`nullslast()`](core_sqlelement.html#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")

[＃723 T0\>](http://www.sqlalchemy.org/trac/ticket/723)

### select.distinct()，query.distinct()接受PostgreSQL的\* args DISTINCT ON [¶](#select-distinct-query-distinct-accepts-args-for-postgresql-distinct-on "Permalink to this headline")

This was already available by passing a list of expressions to the
`distinct` keyword argument of `select()`, the `distinct()` method of
`select()` and `Query` now
accept positional arguments which are rendered as DISTINCT ON when a
Postgresql backend is used.

[不同()
T0\>](http://www.sqlalchemy.org/docs/07/core_expression_api.html#sqlalchemy.sql.expression.Select.distinct)

[Query.distinct()
T0\>](http://www.sqlalchemy.org/docs/07/orm_query.html#sqlalchemy.orm.query.Query.distinct)

[＃1069 T0\>](http://www.sqlalchemy.org/trac/ticket/1069)

### `Index()`可以在`Table`，`__table_args__` [¶](#index-can-be-placed-inline-inside-of-table-table-args "Permalink to this headline")

Index()构造可以与表定义一起内联创建，使用字符串作为列名，作为在表外创建索引的替代方法。那是：

    Table('mytable', metadata,
            Column('id',Integer, primary_key=True),
            Column('name', String(50), nullable=False),
            Index('idx_name', 'name')
    )

这里的主要基本原理是为了声明`__table_args__`的好处，特别是在与mixin一起使用时：

    class HasNameMixin(object):
        name = Column('name', String(50), nullable=False)
        @declared_attr
        def __table_args__(cls):
            return (Index('name'), {})

    class User(HasNameMixin, Base):
        __tablename__ = 'user'
        id = Column('id', Integer, primary_key=True)

[索引 T0\>](http://www.sqlalchemy.org/docs/07/core_schema.html#indexes)

### 窗口函数SQL构造[¶](#window-function-sql-construct "Permalink to this headline")

“窗口函数”在结果集生成时提供有关结果集的信息。这允许针对诸如“行号”，“等级”等各种事物的标准。已知它们至少由Postgresql，SQL
Server和Oracle支持，可能还有其他支持。

对窗口函数的最佳介绍在Postgresql的站点上，从8.4版开始支持窗口函数：

[http://www.postgresql.org/docs/9.0/static/tutorial](http://www.postgresql.org/docs/9.0/static/tutorial)
- window.html

SQLAlchemy使用`over()`方法提供一个通常通过现有函数子句调用的简单结构，该方法接受`order_by`和`partition_by`关键字参数。下面我们复制PG教程中的第一个例子：

    from sqlalchemy.sql import table, column, select, func

    empsalary = table('empsalary',
                    column('depname'),
                    column('empno'),
                    column('salary'))

    s = select([
            empsalary,
            func.avg(empsalary.c.salary).
                  over(partition_by=empsalary.c.depname).
                  label('avg')
        ])

    print(s)

SQL：

    SELECT empsalary.depname, empsalary.empno, empsalary.salary,
    avg(empsalary.salary) OVER (PARTITION BY empsalary.depname) AS avg
    FROM empsalary

[sqlalchemy.sql.expression.over
T0\>](http://www.sqlalchemy.org/docs/07/core_expression_api.html#sqlalchemy.sql.expression.over)

[＃1844 T0\>](http://www.sqlalchemy.org/trac/ticket/1844)

### Connection上的execution\_options()接受“isolation\_level”参数[¶](#execution-options-on-connection-accepts-isolation-level-argument "Permalink to this headline")

这为单个`Connection`设置事务隔离级别，直到`Connection`关闭，并且其基础DBAPI资源返回到连接池，隔离级别重置为连接池默认。默认隔离级别是使用`create_engine()`的`isolation_level`参数设置的。

事务隔离支持目前仅支持Postgresql和SQLite后端。

[execution\_options()
T0\>](http://www.sqlalchemy.org/docs/07/core_connections.html#sqlalchemy.engine.base.Connection.execution_options)

[＃2001 T0\>](http://www.sqlalchemy.org/trac/ticket/2001)

### `TypeDecorator`使用整数主键列[¶](#typedecorator-works-with-integer-primary-key-columns "Permalink to this headline")

扩展`Integer`行为的`TypeDecorator`可以与主键列一起使用。`Column`的“自动增量”功能现在将认识到底层数据库列仍然是一个整数，以便拉斯特瓦尔德机制继续发挥作用。`TypeDecorator`本身将其结果值处理器应用于新生成的主键，包括由DBAPI
`cursor.lastrowid`访问器接收的主键。

[＃2005](http://www.sqlalchemy.org/trac/ticket/2005)
[＃2006](http://www.sqlalchemy.org/trac/ticket/2006)

### `TypeDecorator`存在于“sqlalchemy”导入空间中[¶](#typedecorator-is-present-in-the-sqlalchemy-import-space "Permalink to this headline")

不再需要从`sqlalchemy.types`中导入它，它现在镜像在`sqlalchemy`中。

### 新方言[¶](#new-dialects "Permalink to this headline")

方言已被添加：

-   Drizzle数据库的MySQLdb驱动程序：

    [细雨 T0\>](http://www.sqlalchemy.org/docs/07/dialects_drizzle.html)

-   支持pymysql DBAPI：

    [pymsql注释](http://www.sqlalchemy.org/docs/07/dialects_mysql.html#module-sqlalchemy.dialects.mysql.pymysql)

-   psycopg2现在可以与Python 3一起使用

行为改变（向后兼容）[¶](#behavioral-changes-backwards-compatible "Permalink to this headline")
----------------------------------------------------------------------------------------------

### C扩展默认生成[¶](#c-extensions-build-by-default "Permalink to this headline")

这是0.7b4。如果检测到cPython
2.xx，Exts将生成。如果构建失败，例如在Windows安装中，则捕获该条件并继续进行非C安装。如果使用Python
3或Pypy，C exts将不会生成。

### Query.count()简化后，应该始终工作[¶](#query-count-simplified-should-work-virtually-always "Permalink to this headline")

在`Query.count()`中发生的非常古老的猜测已经现代化以使用`.from_self()`。That is, `query.count()` is now
equivalent to:

    query.from_self(func.count(literal_column('1'))).scalar()

以前，内部逻辑试图重写查询本身的列子句，并且在检测到“子查询”条件（例如可能包含聚合的列查询或具有DISTINCT的查询）时，会经历复杂重写列子句的过程。这种逻辑在复杂条件下失败了，特别是那些涉及到连接表继承的逻辑，并且由于更全面的`.from_self()`调用已经过时了。

由`query.count()`发出的SQL现在总是如下形式：

    SELECT count(1) AS count_1 FROM (
        SELECT user.id AS user_id, user.name AS user_name from user
    ) AS anon_1

也就是说，原始查询完全保留在子查询中，不再猜测应该如何应用计数。

[＃2093 T0\>](http://www.sqlalchemy.org/trac/ticket/2093)

#### 发出一个非子查询形式的count()[¶](#to-emit-a-non-subquery-form-of-count "Permalink to this headline")

MySQL用户已经报道过，MyISAM引擎不会因为这个简单的改变而完全落空。请注意，对于针对无法处理简单子查询的DB进行优化的简单`count()`，应该使用`func.count()`：

    from sqlalchemy import func
    session.query(func.count(MyClass.id)).scalar()

或者用于`count(*)`：

    from sqlalchemy import func, literal_column
    session.query(func.count(literal_column('*'))).select_from(MyClass).scalar()

### LIMIT / OFFSET子句现在使用绑定参数[¶](#limit-offset-clauses-now-use-bind-parameters "Permalink to this headline")

LIMIT和OFFSET子句或其后端等价物（即TOP，ROW NUMBER
OVER等），为实际值使用绑定参数，支持它的所有后端（除了Sybase以外）。这允许更好的查询优化器性能，因为具有不同LIMIT
/ OFFSET的多个语句的文本字符串现在是相同的。

[＃805 T0\>](http://www.sqlalchemy.org/trac/ticket/805)

### 日志记录增强功能[¶](#logging-enhancements "Permalink to this headline")

Vinay
Sajip为我们的日志记录系统提供了一个补丁，使得不再需要嵌入到引擎和池的日志语句中的“十六进制字符串”以允许`echo`标志正常工作。一个使用过滤记录对象的新系统允许我们保持我们当前的行为`echo`对于单个引擎是本地的，而不需要对这些引擎局部的附加标识字符串。

[＃1926 T0\>](http://www.sqlalchemy.org/trac/ticket/1926)

### 简化的polymorphic\_on分配[¶](#simplified-polymorphic-on-assignment "Permalink to this headline")

当在继承场景中使用时，`polymorphic_on`列映射属性的总体现在在对象构造时发生，即使用init事件调用其`__init__`方法。该属性的行为与任何其他列映射属性相同。以前，特殊逻辑会在刷新期间触发以填充此列，从而阻止任何用户代码修改其行为。新方法通过三种方式改进了这一点：1.多态身份现在就在其构建的对象上出现；
2.多态身份可以通过用户代码进行更改，而不会与任何其他列映射属性有所不同；
3.刷新过程中映射器的内部被简化，不再需要对此列进行特殊检查。

[＃1895 T0\>](http://www.sqlalchemy.org/trac/ticket/1895)

### contains\_eager()连接多个路径（即“all()”）[¶](#contains-eager-chains-across-multiple-paths-i-e-all "Permalink to this headline")

现在，``` `contains_eager()`` ```修饰符将自行链接一段更长的路径，而不需要发出单独的``` ``contains_eager()` ```调用。代替：

    session.query(A).options(contains_eager(A.b), contains_eager(A.b, B.c))

你可以说：

    session.query(A).options(contains_eager(A.b, B.c))

[＃2032 T0\>](http://www.sqlalchemy.org/trac/ticket/2032)

### 禁止没有父母的孤儿被允许[¶](#flushing-of-orphans-that-have-no-parent-is-allowed "Permalink to this headline")

我们有一个长期存在的行为，在flush期间检查所谓的“孤立”，即与`relationship()`关联的一个对象，该对象指定了“delete-orphan”级联，已被新增加到INSERT的会话中，并且没有建立父母关系。这项检查是在几年前添加的，以适应测试孤儿行为的一致性的一些测试案例。在现代SQLA中，这一检查在Python方面不再需要。通过使对象的父行的外键引用NOT
NULL来完成“孤立检查”的等效行为，其中数据库以与SQLA允许大多数其他操作一样的方式建立数据一致性的工作。如果对象的父外键可为空，则可以插入该行。当对象与特定的父对象持久化时，将会运行“孤儿”行为，然后与该父对象关联，导致为其发出DELETE语句。

[＃1912 T0\>](http://www.sqlalchemy.org/trac/ticket/1912)

### 收集成员时产生的警告，标量指示不属于flush [¶](#warnings-generated-when-collection-members-scalar-referents-not-part-of-the-flush "Permalink to this headline")的一部分

当标记为“脏”的父对象上通过加载的`relationship()`引用的相关对象在当前`Session`中不存在时，现在会发出警告。

当对象添加到`Session`时，或者当对象首先与父对象关联时，`save-update`级联会生效，因此通常与对象相关的对象全部出现在同一个`Session`中。但是，如果针对特定`relationship()`禁用`save-update`级联，则不会发生此行为，而刷新进程不会尝试更正它，而是与配置的级联行为保持一致。以前，当在冲洗过程中检测到这些物体时，它们被无声地跳过。新的行为是发出警告，目的是为了提醒那些经常出现意外行为的情况。

[＃1973 T0\>](http://www.sqlalchemy.org/trac/ticket/1973)

### 安装程序不再安装鼻插件[¶](#setup-no-longer-installs-a-nose-plugin "Permalink to this headline")

由于我们转向鼻子，我们使用了一个通过setuptools安装的插件，所以`nosetests`脚本会自动运行SQLA的插件代码，这是我们测试拥有完整环境所必需的。在0.6的中间，我们意识到这里的导入模式意味着Nose的“coverage”插件将会中断，因为“coverage”要求在导入任何覆盖模块之前启动该插件。所以在0.6的中间，我们通过在构建中添加一个单独的`sqlalchemy-nose`包来解决这个问题，从而使情况变得更糟。

In 0.7 we’ve done away with trying to get `nosetests` to work automatically, since the SQLAlchemy module would
produce a large number of nose configuration options for all usages of
`nosetests`, not just the SQLAlchemy unit tests
themselves, and the additional `sqlalchemy-nose`
install was an even worse idea, producing an extra package in Python
environments. 0.7中的`sqla_nose.py`脚本现在是用鼻子运行测试的唯一方法。

[＃1949 T0\>](http://www.sqlalchemy.org/trac/ticket/1949)

### 非`Table`衍生的结构可以映射[¶](#non-table-derived-constructs-can-be-mapped "Permalink to this headline")

完全不反对任何`Table`的构造，就像一个函数一样，可以被映射。

    from sqlalchemy import select, func
    from sqlalchemy.orm import mapper

    class Subset(object):
        pass
    selectable = select(["x", "y", "z"]).select_from(func.some_db_function()).alias()
    mapper(Subset, selectable, primary_key=[selectable.c.x])

[＃1876 T0\>](http://www.sqlalchemy.org/trac/ticket/1876)

### aliased()接受`FromClause`元素[¶](#aliased-accepts-fromclause-elements "Permalink to this headline")

This is a convenience helper such that in the case a plain
`FromClause`, such as a `select`, `Table` or `join` is
passed to the `orm.aliased()` construct, it passes
through to the `.alias()` method of that from
construct rather than constructing an ORM level `AliasedClass`.

[＃2018 T0\>](http://www.sqlalchemy.org/trac/ticket/2018)

### Session.connection()，Session.execute()接受'bind'[¶](#session-connection-session-execute-accept-bind "Permalink to this headline")

这是为了允许执行/连接操作明确地参与引擎的公开事务。它还允许`Session`的自定义子类实现它们自己的`get_bind()`方法和参数，以将这些自定义参数与`execute()`和`connection()`方法。

[Session.connection](http://www.sqlalchemy.org/docs/07/orm_session.html#sqlalchemy.orm.session.Session.connection)
[Session.execute](http://www.sqlalchemy.org/docs/07/orm_session.html#sqlalchemy.orm.session.Session.execute)

[＃1996 T0\>](http://www.sqlalchemy.org/trac/ticket/1996)

### 独立地绑定column子句中的参数auto-labeled。[¶](#standalone-bind-parameters-in-columns-clause-auto-labeled "Permalink to this headline")

现在在一个select的“columns子句”中出现的绑定参数现在被自动标记为像其他“匿名”子句一样，除了别的以外，在取出该行时允许它们的“类型”有意义，就像在结果行处理器中一样。

### SQLite - relative file paths are normalized through os.path.abspath()[¶](#sqlite-relative-file-paths-are-normalized-through-os-path-abspath "Permalink to this headline")

这样，一个改变当前目录的脚本将继续定位到相同的位置，因为后续的SQLite连接已经建立。

[＃2036 T0\>](http://www.sqlalchemy.org/trac/ticket/2036)

### MS-SQL - `String` / `Unicode` / `VARCHAR` / `NVARCHAR` / `VARBINARY`最大“为没有长度[¶](#ms-sql-string-unicode-varchar-nvarchar-varbinary-emit-max-for-no-length "Permalink to this headline")

在MS-SQL后端，当没有指定长度时，String / Unicode类型及其对应的VARCHAR /
NVARCHAR以及VARBINARY（[＃1833](http://www.sqlalchemy.org/trac/ticket/1833)）会发出“max”作为长度。这使得它与Postgresql的VARCHAR类型更兼容，当没有指定长度时它类似地是无界的。当没有指定长度时，SQL
Server将这些类型的长度默认为'1'。

行为改变（向后不相容）[¶](#behavioral-changes-backwards-incompatible "Permalink to this headline")
--------------------------------------------------------------------------------------------------

再次注意，除了默认的可变性更改外，大多数这些更改都是\*非常小的，并且不会影响大多数用户。

### `PickleType`和ARRAY可变性关闭[¶](#pickletype-and-array-mutability-turned-off-by-default "Permalink to this headline")

当映射具有`PickleType`或`postgresql.ARRAY`数据类型的列时，此更改引用ORM的默认行为。`mutable`标志现在默认设置为`False`。如果现有的应用程序使用这些类型，并且依赖于检测到就地突变，则必须使用`mutable=True`构造类型对象以恢复0.6行为：

    Table('mytable', metadata,
        # ....

        Column('pickled_data', PickleType(mutable=True))
    )

`mutable=True`标志正在逐步淘汰，以支持新的[突变跟踪](http://www.sqlalchemy.org/docs/07/orm_extensions_mutable.html)扩展。此扩展提供了一种机制，通过该机制，用户定义的数据类型可以将更改事件提供给拥有的父级或父级。

以前使用`mutable=True`的方法不提供更改事件 -
相反，ORM必须扫描会话中存在的所有可变值，并将它们与原始值进行比较，以便每次`flush()`被调用，这是一个非常耗时的事件。这是从SQLAlchemy最初的时候开始的，当`flush()`不是自动的，并且历史跟踪系统不像现在那样复杂时。

Existing applications which use `PickleType`,
`postgresql.ARRAY` or other `MutableType` subclasses, and require in-place mutation detection, should
migrate to the new mutation tracking system, as `mutable=True` is likely to be deprecated in the future.

[＃1980 T0\>](http://www.sqlalchemy.org/trac/ticket/1980)

### `composite()`的可变性检测需要突变跟踪扩展[¶](#mutability-detection-of-composite-requires-the-mutation-tracking-extension "Permalink to this headline")

所谓的“复合”映射属性，即那些使用[复合列类型](http://www.sqlalchemy.org/docs/07/orm_mapper_config.html#composite-column-types)中描述的技术配置的属性，已被重新实现，使得ORM内部不再意识到它们（导致更短，更高效关键部分的代码路径）。虽然复合类型通常被视为不可变的值对象，但从未强制执行。对于使用具有可变性的组合的应用程序，[Mutation
Tracking](http://www.sqlalchemy.org/docs/07/orm_extensions_mutable.html)扩展提供了一个基类，它建立了用户定义的组合类型将更改事件消息发送回每个对象的所属父项或父项的机制。

使用复合类型并依赖这些对象的原位变异检测的应用程序应该迁移到“突变追踪”扩展，或者更改复合类型的用法，以免不再需要就地更改（即对待它们作为不可变的值对象）。

### SQLite - SQLite方言现在对基于文件的数据库使用`NullPool` [¶](#sqlite-the-sqlite-dialect-now-uses-nullpool-for-file-based-databases "Permalink to this headline")

This change is **99.999% backwards compatible**, unless you are using
temporary tables across connection pool connections.

基于文件的SQLite连接速度非常快，使用`NullPool`意味着每次调用`Engine.connect`都会创建一个新的pysqlite连接。

以前，使用`SingletonThreadPool`，这意味着线程中某个引擎的所有连接都是相同的连接。这意味着新方法更直观，特别是在使用多个连接时。

`SingletonThreadPool` is still the default engine
when a `:memory:` database is used.

请注意，由于SQLite处理临时表的方式，此更改**会中断跨Session提交使用的临时表**。如果需要超出一个池连接范围的临时表，请参见[http://www.sqlalchemy.org/docs/dialects\_sqlite.html\#using](http://www.sqlalchemy.org/docs/dialects_sqlite.html#using)
- temporary-tables-with-sqlite中的注释。

[＃1921 T0\>](http://www.sqlalchemy.org/trac/ticket/1921)

### `Session.merge()`检查版本映射器的版本id [¶](#session-merge-checks-version-ids-for-versioned-mappers "Permalink to this headline")

Session.merge()将检查传入状态的版本ID与数据库的版本ID，假设映射使用版本ID并且传入状态具有分配的版本ID，并且如果它们不匹配则引发StaleDataError。这是正确的行为，因为如果传入状态包含陈旧的版本ID，则应该假定状态为陈旧。

如果将数据合并到版本化状态，则版本ID属性可能未定义，并且不会进行版本检查。

这个检查通过检查Hibernate是做什么来确认的 - `merge()`和版本控制功能最初都是从Hibernate调整的。

[＃2027 T0\>](http://www.sqlalchemy.org/trac/ticket/2027)

### 查询改进[¶](#tuple-label-names-in-query-improved "Permalink to this headline")中的元组标签名称

对于依赖旧行为的应用程序来说，这种改进可能略微向后兼容。

给定两个映射类`Foo`和`Bar`，每个类都有一个列`spam`：

    qa = session.query(Foo.spam)
    qb = session.query(Bar.spam)

    qu = qa.union(qb)

由`qu`产生的单列名称将是`spam`。由于`union`会组合事物的方式，因此之前它会像`foo_spam`类似，这与`spam`名称不一致非联合查询。

[＃1942 T0\>](http://www.sqlalchemy.org/trac/ticket/1942)

### 映射列属性首先引用最具体的列[¶](#mapped-column-attributes-reference-the-most-specific-column-first "Permalink to this headline")

这是对映射列属性引用多个列时涉及的行为的更改，特别是在处理与超类上的属性具有相同名称的连接表子类上的属性时。

使用声明式，场景是这样的：

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)

    class Child(Parent):
       __tablename__ = 'child'
        id = Column(Integer, ForeignKey('parent.id'), primary_key=True)

以上，属性`Child.id`指向`child.id`列和`parent.id` -
这是由于属性。如果它在类上命名不同，如`Child.child_id`，则它将明确地映射到`child.id`，并且`Child.id`为与`Parent.id`具有相同的属性。

当`id`属性用于引用`parent.id`和`child.id`时，它将它们存储在有序列表中。像`Child.id`这样的表达式在渲染时仅引用这些列的*一个*。直到0.6，这个列将是`parent.id`。In 0.7, it is the less surprising `child.id`.

这种行为的遗留问题涉及到不再适用的ORM的行为和限制；所需要的只是扭转秩序。

这种方法的主要优点是，现在可以更轻松地构建引用本地列的`primaryjoin`表达式：

    class Child(Parent):
       __tablename__ = 'child'
        id = Column(Integer, ForeignKey('parent.id'), primary_key=True)
        some_related = relationship("SomeRelated",
                        primaryjoin="Child.id==SomeRelated.child_id")

    class SomeRelated(Base):
       __tablename__ = 'some_related'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))

在0.7之前，`Child.id`表达式将引用`Parent.id`，并且有必要将`child.id`映射到不同的属性。

这也意味着像这样的查询会改变它的行为：

    session.query(Parent).filter(Child.id > 7)

在0.6中，这会使得：

    SELECT parent.id AS parent_id
    FROM parent
    WHERE parent.id > :id_1

在0.7中，你会得到：

    SELECT parent.id AS parent_id
    FROM parent, child
    WHERE child.id > :id_1

你会注意到它是一个笛卡尔积 - 这个行为现在等同于`Child`本地的任何其他属性的行为。使用`with_polymorphic()`方法或显式连接底层`Table`对象的类似策略来针对所有`Parent`对象呈现查询按照与0.5和0.6相同的方式对`Child`进行标准化：

    print(s.query(Parent).with_polymorphic([Child]).filter(Child.id > 7))

0.6和0.7中的哪一个呈现：

    SELECT parent.id AS parent_id, child.id AS child_id
    FROM parent LEFT OUTER JOIN child ON parent.id = child.id
    WHERE child.id > :id_1

此更改的另一个影响是跨两个表的连接继承负载将从子表的值中填充，而不是父表的值。一个不常见的情况是，使用`with_polymorphic="*"`针对“父”进行的查询针对“父”发出查询，并将LEFT OUTER
JOIN改为“child”。该行位于“Parent”中，看到多态身份对应于“Child”，但假设“child”中的实际行已被*删除*。由于这种损坏，该行出现与“child”设置为NULL的所有列
- 这是现在填充的值，而不是父表中的值。

[＃1892 T0\>](http://www.sqlalchemy.org/trac/ticket/1892)

### 映射到两个或多个同名列的连接需要显式声明[¶](#mapping-to-joins-with-two-or-more-same-named-columns-requires-explicit-declaration "Permalink to this headline")

这与[＃1892](http://www.sqlalchemy.org/trac/ticket/1892)中的前一个更改有些相关。在映射到连接时，同名列必须显式链接到映射属性，即如[根据多个表映射类](http://www.sqlalchemy.org/docs/07/orm_mapper_config.html#mapping-a-class-against-multiple-tables)中所述。

给定两个表`foo`和`bar`，每个表具有主键列`id`，现在会产生一个错误：

    foobar = foo.join(bar, foo.c.id==bar.c.foo_id)
    mapper(FooBar, foobar)

This because the `mapper()` refuses to guess what
column is the primary representation of `FooBar.id`
- is it `foo.c.id` or is it `bar.c.id` ? 该属性必须是明确的：

    foobar = foo.join(bar, foo.c.id==bar.c.foo_id)
    mapper(FooBar, foobar, properties={
        'id':[foo.c.id, bar.c.id]
    })

[＃1896 T0\>](http://www.sqlalchemy.org/trac/ticket/1896)

### Mapper要求polymorphic\_on列存在于映射的可选[¶](#mapper-requires-that-polymorphic-on-column-be-present-in-the-mapped-selectable "Permalink to this headline")中

这是0.6的警告，现在0.7的错误。为`polymorphic_on`提供的列必须位于映射可选项中。这可以防止一些偶然的用户错误，例如：

    mapper(SomeClass, sometable, polymorphic_on=some_lookup_table.c.id)

其中polymorphic\_on必须位于`sometable`列上，在这种情况下可能是`sometable.c.some_lookup_id`。还有一些“多态联合”情景，其中有时会出现类似的错误。

这样的配置错误一直是“错误的”，并且上面的映射不能像指定的那样工作 -
该列将被忽略。然而，在罕见的情况下，应用程序在不知不觉中依赖于这种行为，它可能会向后兼容。

[＃1875 T0\>](http://www.sqlalchemy.org/trac/ticket/1875)

### `DDL()`构造现在转义百分号[¶](#ddl-constructs-now-escape-percent-signs "Permalink to this headline")

以前，对于那些接受`pyformat`的DBAPI，根据DBAPI，`DDL()`字符串中的百分号必须转义，即`%%`或`format`绑定（即psycopg2，mysql-python），这与`text()`构造不一致。对于`text()`，现在对`DDL()`发生同样的转义。

[＃1897 T0\>](http://www.sqlalchemy.org/trac/ticket/1897)

### `Table.c` / `MetaData.tables`细化了一下，不允许直接变异[¶](#table-c-metadata-tables-refined-a-bit-don-t-allow-direct-mutation "Permalink to this headline")

Another area where some users were tinkering around in such a way that
doesn’t actually work as expected, but still left an exceedingly small
chance that some application was relying upon this behavior, the
construct returned by the `.c` attribute on
`Table` and the `.tables`
attribute on `MetaData` is explicitly non-mutable.
该构造的“可变”版本现在是私人的。Adding columns to `.c` involves using the `append_column()`
method of `Table`, which ensures things are
associated with the parent `Table` in the
appropriate way; similarly, `MetaData.tables` has a
contract with the `Table` objects stored in this
dictionary, as well as a little bit of new bookkeeping in that a
`set()` of all schema names is tracked, which is
satisfied only by using the public `Table`
constructor as well as `Table.tometadata()`.

当然有可能这些属性所咨询的`ColumnCollection`和`dict`集合有一天会在其所有的突变方法上实现事件，这样恰当的簿记就发生在但是直到有人有动机去实现所有这些以及几十个新的单元测试，缩小这些集合的变异路径将确保没有应用程序试图依赖目前不被支持的用法。

[＃1893](http://www.sqlalchemy.org/trac/ticket/1893)
[＃1917](http://www.sqlalchemy.org/trac/ticket/1917)

### 对于所有inserted\_primary\_key值，server\_default始终返回None [¶](#server-default-consistently-returns-none-for-all-inserted-primary-key-values "Permalink to this headline")

在Integer
PK列上存在server\_default时建立一致性。SQLA不会预取这些，也不会返回到cursor.lastrowid（DBAPI）中。确保所有后端始终在result.inserted\_primary\_key中返回None，这些后端可能先前已返回一个值。在主键列上使用server\_default是非常不寻常的。如果使用特殊函数或SQL表达式来生成主键默认值，则应该将其设置为Python端“default”而不是server\_default。

关于这种情况的反思，除了在我们检测到序列默认值的PG SERIAL
col的情况下，对server\_default的int PK
col的反映将“autoincrement”标志设置为False。

[\#2020](http://www.sqlalchemy.org/trac/ticket/2020)
[\#2021](http://www.sqlalchemy.org/trac/ticket/2021)

### sys.modules中的`sqlalchemy.exceptions`别名已被移除[¶](#the-sqlalchemy-exceptions-alias-in-sys-modules-is-removed "Permalink to this headline")

For a few years we’ve added the string `sqlalchemy.exceptions` to `sys.modules`, so that a statement like
“`import sqlalchemy.exceptions`” would work.
很久以来，核心例外模块的名称一直是`exc`，因此建议为此模块导入：

    from sqlalchemy import exc

The `exceptions` name is still present in
“`sqlalchemy`” for applications which might have
said `from sqlalchemy import exceptions`, but they
should also start using the `exc` name.

### 查询计时配方更改[¶](#query-timing-recipe-changes "Permalink to this headline")

虽然不是SQLAlchemy本身的一部分，但值得一提的是，将`ConnectionProxy`重新加入到新事件系统中意味着它不再适合“Timing all
Queries”配方。请调整查询计时器以使用`before_cursor_execute()`和`after_cursor_execute()`事件，并在更新配方UsageRecipes / Profiling中进行演示。

弃用的API [¶](#deprecated-api "Permalink to this headline")
-----------------------------------------------------------

### 类型上的默认构造函数不会接受参数[¶](#default-constructor-on-types-will-not-accept-arguments "Permalink to this headline")

简单类型，如`Integer`，`Date`等在核心类型模块中不接受参数。The default constructor that
accepts/ignores a catchall `\*args, \**kwargs` is
restored as of 0.7b4/0.7.0, but emits a deprecation warning.

如果参数与核心类型（如`Integer`）一起使用，可能是因为您打算使用特定于方言的类型，如`sqlalchemy.dialects.mysql.INTEGER`例如接受一个“display\_width”参数。

### compile\_mappers()重命名为configure\_mappers()，简化了配置内部结构[¶](#compile-mappers-renamed-configure-mappers-simplified-configuration-internals "Permalink to this headline")

这个系统慢慢地从小的东西变成了东西，从本地实现到了单个的映射器，并且很少被命名为更具全局性的“注册表”级功能，而且命名得不好，所以我们通过将实现移出`Mapper`并将其重命名为`configure_mappers()`。当一个应用程序通过属性或查询访问需要映射时，通常不需要调用`configure_mappers()`，因为此过程是按照需要发生的。

[＃1966 T0\>](http://www.sqlalchemy.org/trac/ticket/1966)

### 核心侦听器/代理被事件侦听器取代[¶](#core-listener-proxy-superseded-by-event-listeners "Permalink to this headline")

`PoolListener`, `ConnectionProxy`, `DDLElement.execute_at` are superseded by
`event.listen()`, using the `PoolEvents`, `EngineEvents`, `DDLEvents` dispatch targets, respectively.

### ORM扩展取代了事件监听器[¶](#orm-extensions-superseded-by-event-listeners "Permalink to this headline")

`MapperExtension`, `AttributeExtension`, `SessionExtension` are superseded by
`event.listen()`, using the `MapperEvents`/`InstanceEvents`,
`AttributeEvents`, `SessionEvents`, dispatch targets, respectively.

### 在select()中为MySQL发送字符串'distinct'应该通过前缀来完成[¶](#sending-a-string-to-distinct-in-select-for-mysql-should-be-done-via-prefixes "Permalink to this headline")

这个模糊的特性允许这种模式与MySQL后端：

    select([mytable], distinct='ALL', prefixes=['HIGH_PRIORITY'])

`prefixes`关键字或`prefix_with()`方法应该用于非标准或不常用的前缀：

    select([mytable]).prefix_with('HIGH_PRIORITY', 'ALL')

### `useexisting`取代`extend_existing`和`keep_existing` [¶](#useexisting-superseded-by-extend-existing-and-keep-existing "Permalink to this headline")

表中的`useexisting`标志已被一对新的标志`keep_existing`和`extend_existing`所取代。`extend_existing`相当于`useexisting` -
返回现有的表，并添加其他构造函数元素。使用`keep_existing`，将返回现有表格，但不会添加其他构造函数元素 -
仅在新创建表格时应用这些元素。

向后不兼容的API更改[¶](#backwards-incompatible-api-changes "Permalink to this headline")
----------------------------------------------------------------------------------------

### 传递给`bindparam()`的可加密标签不会被评估 - 影响Beaker示例[¶](#callables-passed-to-bindparam-don-t-get-evaluated-affects-the-beaker-example "Permalink to this headline")

[＃1950 T0\>](http://www.sqlalchemy.org/trac/ticket/1950)

请注意，这会影响Beaker缓存示例，其中`_params_from_query()`函数的工作需要稍作调整。如果您使用Beaker示例中的代码，则应该应用此更改。

### types.type\_map现在是private，types.\_type\_map [¶](#types-type-map-is-now-private-types-type-map "Permalink to this headline")

我们注意到一些用户使用`sqlalchemy.types`中的这个字典作为将Python类型与SQL类型关联的快捷方式。我们无法保证此字典的内容或格式，另外，以一对一的方式关联Python类型的业务有一些灰色区域，应由各个应用程序最好决定，因此我们强调了此属性。

[＃1870 T0\>](http://www.sqlalchemy.org/trac/ticket/1870)

### 将独立`alias()`函数的`alias`关键字arg重命名为`name` [¶](#renamed-the-alias-keyword-arg-of-standalone-alias-function-to-name "Permalink to this headline")

This so that the keyword argument `name` matches
that of the `alias()` methods on all
`FromClause` objects as well as the `name` argument on `Query.subquery()`.

只有使用独立`alias()`函数而不是方法绑定函数并使用显式关键字名称`alias`传递别名的代码才会需要这里修改。

### 非公开的`Pool`方法强调[¶](#non-public-pool-methods-underscored "Permalink to this headline")

所有不适合公开使用的`Pool`和子类的方法都已用下划线重新命名。他们以前没有这样命名是一个错误。

现在强调或删除了合并方法：

`Pool.create_connection()` - \>
`Pool._create_connection()`

`Pool.do_get()` - \> `Pool._do_get()`

`Pool.do_return_conn()` - \>
`Pool._do_return_conn()`

`Pool.do_return_invalid()` - \>已删除，未使用

`Pool.return_conn()` - \>
`Pool._return_conn()`

`Pool.get()` - \> `Pool._get()`，公共API为`Pool.connect()`

`SingletonThreadPool.cleanup()` - \>
`_cleanup()`

`SingletonThreadPool.dispose_local()` -
\>已移除，请使用`conn.invalidate()`

[＃1982 T0\>](http://www.sqlalchemy.org/trac/ticket/1982)

先前已弃用，现已删除[¶](#previously-deprecated-now-removed "Permalink to this headline")
----------------------------------------------------------------------------------------

### Query.join()，Query.outerjoin()，eagerload()，eagerload\_all()等不再允许属性列表作为参数[¶](#query-join-query-outerjoin-eagerload-eagerload-all-others-no-longer-allow-lists-of-attributes-as-arguments "Permalink to this headline")

将属性或属性名称的列表传递给`Query.join`，`eagerload()`

    # old way, deprecated since 0.5
    session.query(Houses).join([Houses.rooms, Room.closets])
    session.query(Houses).options(eagerload_all([Houses.rooms, Room.closets]))

这些方法都可以接受0.5系列的\*参数：

    # current way, in place since 0.5
    session.query(Houses).join(Houses.rooms, Room.closets)
    session.query(Houses).options(eagerload_all(Houses.rooms, Room.closets))

### `ScopedSession.mapper`被删除[¶](#scopedsession-mapper-is-removed "Permalink to this headline")

此功能提供了一个映射器扩展，它将基于类的功能与特定的`ScopedSession`相链接，特别是提供了新对象实例将自动与该会话关联的行为。该功能被教程和框架过度使用，由于其隐含的行为导致用户很大的困惑，并在0.5.5中被弃用。复制其功能的技术在[wiki：UsageRecipes
/ SessionAwareMapper]
