---
title: migration_05
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/8a8597/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
SQLAlchemy 0.5 有哪些新特性？[¶](#what-s-new-in-sqlalchemy-0-5 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍了 2008 年 10 月 12 日发布的 SQLAlchemy
0.4 版和 2010 年 1 月 16 日发布的 SQLAlchemy 0.5 版之间的变化。

文件日期：2009 年 8 月 4 日

本指南记录了影响用户将他们的应用程序从 0.4 系列 SQLAlchemy 迁移到 0.5 的 API 更改。它也适用于[基本 SQLAlchemy](http://oreilly.com/catalog/9780596516147/)中的工作，它只涵盖了 0.4，并且似乎甚至还有一些旧的 0.3ism。请注意，SQLAlchemy
0.5 删除了许多在 0.4 系列范围内被弃用的行为，并且也弃用了更多特定于 0.4 的行为。

主要文档更改[¶](#major-documentation-changes "Permalink to this headline")
--------------------------------------------------------------------------

文档的某些部分已经完全重写，可以作为新 ORM 功能的介绍。特别是，`Query`和`Session`对象在 API 和行为方面有着明显的区别，从根本上改变了许多基本方式，特别是构建高度自定义的 ORM 查询并处理陈旧的会话状态，提交和回滚。

-   [ORM Tutorial](http://www.sqlalchemy.org/docs/05/ormtutorial.html)
-   [会话记录](http://www.sqlalchemy.org/docs/05/session.html)

弃用来源[¶](#deprecations-source "Permalink to this headline")
--------------------------------------------------------------

另一个信息来源被记录在一系列单元测试中，说明了一些常见的`Query`模式的最新用法；这个文件可以在[source：sqlalchemy / trunk /
test / orm\_test\_deprecations.py]中查看。

需求变更[¶](#requirements-changes "Permalink to this headline")
---------------------------------------------------------------

-   Python 2.4 或更高版本是必需的。SQLAlchemy 0.4 行是 Python
    2.3 支持的最后一个版本。

对象关系映射[¶](#object-relational-mapping "Permalink to this headline")
------------------------------------------------------------------------

-   **查询中的列级表达式** -
    详见[教程](http://www.sqlalchemy.org/docs/05/ormtutorial.html)，`Query`有能力创建特定的 SELECT 语句，而不仅仅是针对整行的那些语句：

        session.query(User.name, func.count(Address.id).label("numaddresses")).join(Address).group_by(User.name)plainplainplainplain

    任何多列/实体查询返回的元组都是*命名的*元组：

        for row in session.query(User.name, func.count(Address.id).label('numaddresses')).join(Address).group_by(User.name):plainplainplain
           print("name", row.name, "number", row.numaddresses)

    `Query` has a `statement`
    accessor, as well as a `subquery()` method which
    allow `Query` to be used to create more complex
    combinations:

        subq = session.query(Keyword.id.label('keyword_id')).filter(Keyword.name.in_(['beans', 'carrots'])).subquery()plainplainplainplainplainplain
        recipes = session.query(Recipe).filter(exists().
           where(Recipe.id==recipe_keywords.c.recipe_id).
           where(recipe_keywords.c.keyword_id==subq.c.keyword_id)
        )

-   **Explicit ORM aliases are recommended for aliased joins** - The
    `aliased()` function produces an “alias” of a
    class, which allows fine-grained control of aliases in conjunction
    with ORM queries. 尽管表级别别名（即`table.alias()`）仍然可用，但 ORM 级别别名保留了 ORM 映射对象的语义，这对于继承映射，选项和其他场景很重要。例如。：

        Friend = aliased(Person)plain
        session.query(Person, Friend).join((Friend, Person.friends)).all()

-   **query.join()大大增强。** -
    您现在可以通过多种方式指定联接的目标和 ON 子句。可以提供单独的目标类，其中 SQLA 将尝试通过与`table.join(someothertable)`相同的方式通过外键形成连接。可以提供一个目标和一个明确的 ON 条件，其中 ON 条件可以是`relation()`名称，实际类描述符或 SQL 表达式。或者只是`relation()`名称或类描述符的旧方法也适用。请参阅包含几个示例的 ORM 教程。

-   **声明式推荐用于不需要（且不喜欢）表和映射器之间的抽象的应用程序。 -
    [/docs/05/reference/ext/declarative.html 声明式]模块，它是用于将`Table`，`mapper()`和用户定义的类对象的表达式组合在一起，因为它简化了应用程序配置，确保“每个类一个映射器”模式，并允许全面的配置可用于不同的`mapper()`调用。**单独的`mapper()`和`Table`用法现在称为“古典 SQLAlchemy 用法”，当然可以自由混合声明。

-   **.c。属性已从类（即`MyClass.c.somecolumn`）中移除**。与 0.4 中的情况一样，类级属性可用作查询元素，即`Class.c.propname`现在被`Class.propname`取代，`c`属性继续保留在`Table`对象上，它们表示存在于表上的`Column`对象的名称空间。

    为了得到映射类的表（如果你没有保留它）：

        table = class_mapper(someclass).mapped_tableplain

    遍历列：

        for col in table.c:plainplainplain
            print(col)

    使用特定列：

        table.c.somecolumnplainplainplain

    类绑定描述符支持完整的 Column 运算符以及文档化的面向关系的运算符，如`has()`，`any()`，`contains()`等

    严重移除`.c.`的原因 is that in 0.5, class-bound
    descriptors carry potentially different meaning, as well as
    information regarding class mappings, versus plain
    `Column` objects - and there are use cases where
    you’d specifically want to use one or the other.
    通常，使用类绑定描述符会调用一组映射/多态感知的转换，而使用表绑定的列则不会。在 0.4 中，这些翻译被全面应用于所有表达式，但是 0.5 与列和映射描述符完全不同，只是将翻译应用于后者。因此，在很多情况下，特别是在处理连接表继承配置以及使用`query(<columns>)`，`Class.propname`和`table.c.colname`不可互换。

    For example, `session.query(users.c.id, users.c.name)` is different versus
    `session.query(User.id, User.name)`; in the
    latter case, the `Query` is aware of the mapper
    in use and further mapper-specific operations like
    `query.join(<propname>)`,
    `query.with_parent()` etc.
    可能会使用，但在前者情况下不能。此外，在多态继承场景中，类绑定描述符引用可用的多态可选列中的列，而不一定是直接对应于描述符的表列。For
    example, a set of classes related by joined-table inheritance to the
    `person` table along the `person_id` column of each table will all have their
    `Class.person_id` attribute mapped to the
    `person_id` column in `person`, and not their subclass table.
    版本 0.4 将自动将此行为映射到表格绑定的`Column`对象。In 0.5, this automatic conversion has been removed,
    so that you in fact *can* use table-bound columns as a means to
    override the translations which occur with polymorphic querying;
    this allows `Query` to be able to create
    optimized selects among joined-table or concrete-table inheritance
    setups, as well as portable subqueries, etc.

-   **Session Now Synchronizes Automatically with
    Transactions.**会话现在默认会自动与事务同步，包括 autoflush 和 autoexpire。除非禁止使用`autocommit`选项，否则交易始终存在。当所有三个标志都设置为默认值时，会话在回滚之后会优雅地恢复，并且很难将陈旧的数据导入会话。有关详细信息，请参阅新的 Session 文档。

-   **隐式订单被移除**。这将影响依赖于 SA 的“隐式排序”行为的 ORM 用户，这些用户声明所有没有`order_by()`的 Query 对象将 ORDER
    BY 的“id”或“oid”列主映射表和所有懒惰/急切加载的集合都会应用类似的排序。在 0.5 中，必须在`mapper()`和`relation()`对象（如果需要）上显式配置自动排序，否则在使用`Query`时自动排序。

    To convert an 0.4 mapping to 0.5, such that its ordering behavior
    will be extremely similar to 0.4 or previous, use the
    `order_by` setting on `mapper()` and `relation()`:

        mapper(User, users, properties={plainplain
            'addresses':relation(Address, order_by=addresses.c.id)
        }, order_by=users.c.id)

    要设置 backref 的顺序，请使用`backref()`函数：

        'keywords':relation(Keyword, secondary=item_keywords,plain
              order_by=keywords.c.name, backref=backref('items', order_by=items.c.id))

    使用声明？To help with the new `order_by`
    requirement, `order_by` and friends can now be
    set using strings which are evaluated in Python later on (this works
    **only** with declarative, not plain mappers):

        class MyClass(MyDeclarativeBase):plainplainplainplainplainplainplainplain
            ...
            'addresses':relation("Address", order_by="Address.id")

    在`relation()s`上设置`order_by`通常是个好主意，因为该顺序不会受到影响。除此之外，最佳做法是使用`Query.order_by()`来控制正在加载的主要实体的排序。

-   **会话现在是 autoflush = True / autoexpire = True / autocommit =
    False。** - 要设置它，只需调用不带参数的`sessionmaker()`即可。名称`transactional=True`现在是`autocommit=False`。Flushes occur
    upon each query issued (disable with `autoflush=False`), within each `commit()` (as always),
    and before each `begin_nested()` (so rolling
    back to the SAVEPOINT is meaningful).
    所有对象都在每个`commit()`之后和每个`rollback()`之后过期。回滚后，挂起的对象被清除，被删除的对象移回到持久性。这些默认值一起工作得非常好，并且实际上不再需要像`clear()`这样的旧技术（它也重新命名为`expunge_all()`）。

    附：：会话现在可以在`rollback()`之后重用。标量和集合属性的变化，添加和删除都回滚。

-   **session.add() replaces session.save(), session.update(),
    session.save\_or\_update().** - the
    `session.add(someitem)` and
    `session.add_all([list of items])` methods
    replace `save()`, `update()`, and `save_or_update()`.
    这些方法将在整个 0.5 中保持不推荐。

-   **backref 配置没有冗长。** - The `backref()`
    function now uses the `primaryjoin` and
    `secondaryjoin` arguments of the forwards-facing
    `relation()` when they are not explicitly
    stated. 不再需要分别在两个方向上指定`primaryjoin` / `secondaryjoin`。

-   **简化的多态选项。** -
    ORM 的“多态负载”行为已被简化。在 0.4 中，mapper()有一个名为`polymorphic_fetch`的参数，可以将其配置为`select`或`deferred`。该选项被删除；现在，映射器只会推迟 SELECT 语句中不存在的任何列。The
    actual SELECT statement used is controlled by the
    `with_polymorphic` mapper argument (which is
    also in 0.4 and replaces `select_table`), as
    well as the `with_polymorphic()` method on
    `Query` (also in 0.4).

    对继承类的延迟加载的一个改进是映射器现在在所有情况下都产生了 SELECT 语句的“优化”版本；也就是说，如果 B 类从 A 继承，并且只有 B 类中存在的几个属性已过期，则刷新操作将只在 SELECT 语句中包含 B 的表，并且不会加入 A.

-   `Session`上的`execute()`方法将普通字符串转换为`text()`结构，以便绑定参数可以全部指定为“：bindname”而不需要明确地调用`text()`。如果需要“原始”SQL，请使用`session.connection()。execute（“raw text”）`。

-   `session.Query().iterate_instances()`已被重命名为`instances()`。返回列表而不是迭代器的旧`instances()`方法不再存在。如果你依赖这种行为，你应该使用`list(your_query.instances())`。

扩展 ORM [¶](#extending-the-orm "Permalink to this headline")
------------------------------------------------------------

在 0.5 中，我们正在采取更多方法来修改和扩展 ORM。下面是一个总结：

-   **MapperExtension。 T0\>** - 这是经典的扩展​​类，它仍然存在。Methods
    which should rarely be needed are `create_instance()` and `populate_instance()`.
    要从数据库加载对象时控制对象的初始化，请使用文档中描述的`reconstruct_instance()`方法或更简单的`@reconstructor`装饰器。
-   **SessionExtension。 T0\>** - 这是一个易于使用的会话事件扩展类。In
    particular, it provides `before_flush()`,
    `after_flush()` and
    `after_flush_postexec()` methods.
    由于在`before_flush()`之内，您可以自由修改会话的刷新计划，因此建议在`MapperExtension.before_XXX`之上使用此用法，而`MapperExtension`
-   **AttributeExtension。 T0\>** -
    这个类现在是公共 API 的一部分，允许拦截属性上的 userland 事件，包括属性设置和删除操作以及集合附加和删除。它还允许修改或设置值。文档中描述的`@validates`装饰器提供了一种将任何映射属性标记为由特定类方法“验证”的快速方法。
-   **属性工具定制。** -
    提供了一个 API，用于完全替代 SQLAlchemy 的属性检测，或者仅仅在某些情况下对其进行扩充。该 API 是为了 Trellis 工具包的目的而生成的，但可作为公共 API 提供。在`/examples/custom_attributes`目录中的分发中提供了一些示例。

模式/类型[¶ T0\>](#schema-types "Permalink to this headline")
-------------------------------------------------------------

-   **没有长度的字符串不会再生成 TEXT，它会生成 VARCHAR** -
    当指定长度时，`String`类型不再奇迹般地转换为`Text`
    。这仅在发出 CREATE
    TABLE 时有效，因为它将发出没有长度参数的`VARCHAR`，这在许多（但不是全部）数据库上都无效。要创建 TEXT（或 CLOB，即无界字符串）列，请使用`Text`类型。

-   **具有 mutable = True 的 PickleType()需要\_\_eq \_\_()方法** -
    `PickleType`类型需要在 mutable =
    True 时比较值。比较`pickle.dumps()`的方法是低效且不可靠的。如果传入的对象没有实现`__eq__()`并且也不是`None`，则使用`dumps()`比较，但会引发警告。对于实现包含所有字典，列表等的`__eq__()`的类型，比较将使用`==`，现在默认情况下可靠。

-   **convert\_bind\_param() and convert\_result\_value() methods of
    TypeEngine/TypeDecorator are removed.** -
    不幸的是，O'Reilly 的书中记录了这些方法，即使它们在 0.3 后被弃用。对于类型为`TypeEngine`的用户定义类型，应该使用`bind_processor()`和`result_processor()`方法进行绑定/结果处理。任何用户定义的类型，无论是扩展`TypeEngine`还是`TypeDecorator`，都可以使用以下适配器轻松适应新样式：

        class AdaptOldConvertMethods(object):plainplainplainplain
            """A mixin which adapts 0.3-style convert_bind_param and
            convert_result_value methods

            """
            def bind_processor(self, dialect):
                def convert(value):
                    return self.convert_bind_param(value, dialect)
                return convert

            def result_processor(self, dialect):
                def convert(value):
                    return self.convert_result_value(value, dialect)
                return convert

            def convert_result_value(self, value, dialect):
                return value

            def convert_bind_param(self, value, dialect):
                return value

    要使用上面的 mixin：

        class MyType(AdaptOldConvertMethods, TypeEngine):plain
           # ...

-   `Column`和`Table`以及`Table`中的`quote_schema`标志上的`quote`默认值是`None`，这意味着让常规引用规则生效。当`True`时，强制引用引用。当`False`时，引用被强制关闭。

-   列`DEFAULT`值 DDL 现在可以通过`Column（...， server_default ='val'）  t2 >，弃用列（...， PassiveDefault（'val'））`。`default=`现在专用于 Python 启动的默认值，并且可以与 server\_default 共存。新的`server_default=FetchedValue()`取代了用于标记列的`PassiveDefault('')`成语受外部触发影响并且没有 DDL 副作用。

-   SQLite 的`DateTime`，`Time`和`Date`类型现在**只接受日期时间对象，而不接受字符串**作为绑定参数输入。如果你想创建自己的“hybrid”类型，它接受字符串并将结果作为日期对象返回（从任何你想要的格式），创建一个`TypeDecorator`，它建立在`String`如果您只需要基于字符串的日期，只需使用`String`即可。

-   此外，当与 SQLite 一起使用时，`DateTime`和`Time`类型现在表示 Python
    `datetime.datetime`对象的“microseconds”字段与`str(datetime)`相同的方式 - 分数秒，而不是微秒数。那是：

        dt = datetime.datetime(2008, 6, 27, 12, 0, 0, 125)  # 125 usecplainplainplain

        # old way
        '2008-06-27 12:00:00.125'

        # new way
        '2008-06-27 12:00:00.000125'

    因此，如果现有的基于 SQLite 文件的数据库打算在 0.4 和 0.5 之间使用，则必须升级日期时间列以存储新格式（请注意：请测试一下，我非常肯定它的正确性）：

        UPDATE mytable SET somedatecol =plain
          substr(somedatecol, 0, 19) || '.' || substr((substr(somedatecol, 21, -1) / 1000000), 3, -1);

    或者，启用“传统”模式，如下所示：

        from sqlalchemy.databases.sqlite import DateTimeMixinplainplain
        DateTimeMixin.__legacy_microseconds__ = True

默认情况下，连接池不再是 threadlocal [¶](#connection-pool-no-longer-threadlocal-by-default "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------

0.4 有一个不幸的默认设置“pool\_threadlocal =
True”，例如，当在单个线程中使用多个会话时会导致意外行为。这个标志现在在 0.5。To
re-enable 0.4’s behavior, specify `pool_threadlocal=True` to `create_engine()`, or alternatively use
the “threadlocal” strategy via `strategy="threadlocal"`.

\* args Accepted，\* args 不再被接受[¶](#args-accepted-args-no-longer-accepted "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------

使用`method(\*args)`与`method([args])`的策略是，如果方法接受表示固定结构的可变长度项集，它需要`\*args`。如果该方法接受数据驱动的可变长度项目集合，则需要`[args]`。

-   The various Query.options() functions `eagerload()`, `eagerload_all()`,
    `lazyload()`, `contains_eager()`, `defer()`, `undefer()` all accept variable-length `\*keys` as
    their argument now, which allows a path to be formulated using
    descriptors, ie. :

        query.options(eagerload_all(User.orders, Order.items, Item.keywords))plainplainplain

    为了向后兼容，仍然接受单个数组参数。

-   Similarly, the `Query.join()` and
    `Query.outerjoin()` methods accept a variable
    length \*args, with a single array accepted for backwards
    compatibility:

        query.join('orders', 'items')plainplainplainplainplain
        query.join(User.orders, Order.items)

-   列和类似的\_()方法中的`in_()`它不再接受`\*args`。

除去[¶ T0\>](#removed "Permalink to this headline")
---------------------------------------------------

-   **entity\_name** -
    此功能始终存在问题并且很少使用。0.5 的更深入充实的用例揭示了导致其被删除的`entity_name`的进一步问题。如果单个类需要不同的映射，请将该类拆分为单独的子类并分别映射它们。一个例子是[wiki：UsageRecipes
    / EntityName]。有关基本原理的更多信息，请参见 http：//groups.google.c
    om / group / sqlalchemy / browse\_thread / thread /
    9e23a0641a88b96d？hl = en。

-   **get()/load() cleanup**

    `load()`方法已被删除。它的功能是任意的，基本上从 Hibernate 中复制，它也不是一个特别有意义的方法。

    要获得同等功能：

        x = session.query(SomeClass).populate_existing().get(7)plainplainplainplain

    `Session.get(cls, id)` and
    `Session.load(cls, id)` have been removed.
    `Session.get()` is redundant vs.
    `session.query(cls).get(id)`.

    `MapperExtension.get()`也被删除（就像`MapperExtension.load()`）。要覆盖`Query.get()`的功能，请使用以下子类：

        class MyQuery(Query):plainplain
            def get(self, ident):
                # ...

        session = sessionmaker(query_cls=MyQuery)()

        ad1 = session.query(Address).get(1)

-   `sqlalchemy.orm.relation()`

    以下已弃用的关键字参数已被删除：

    foreignkey，association，private，attributeext，is\_backref

    特别是，`attributeext`被替换为`extension` -
    `AttributeExtension`类现在处于公共 API 中。

-   `session.Query()`

    以下弃用函数已被删除：

    列表，标量，count\_by，select\_whereclause，get\_by，select\_by，join\_by，selectfirst，selectone，select，execute，select\_statement，select\_text，join\_to，join\_via，selectfirst\_by，selectone\_by，apply\_max，apply\_min，apply\_avg，apply\_sum

    Additionally, the `id` keyword argument to
    `join()`, `outerjoin()`,
    `add_entity()` and `add_column()` has been removed. 要将`Query`中的表别名作为结果列，请使用`aliased`结构：

        from sqlalchemy.orm import aliasedplainplainplainplainplain
        address_alias = aliased(Address)
        print(session.query(User, address_alias).join((address_alias, User.addresses)).all())

-   `sqlalchemy.orm.Mapper`

    -   实例()
    -   get\_session() -
        这个方法不是很明显，但是具有将惰性加载与特定会话相关联的效果，即使父对象完全分离，当扩展名如`scoped_session()`或旧使用`SessionContextExt`。一些依赖此行为的应用程序可能不再按预期工作；但是更好的编程习惯是在需要从属性访问数据库时始终确保对象存在于会话中。
-   `mapper（MyClass， mytable）`

    映射类 no 更长，具有“c”类属性；例如`MyClass.c`

-   `sqlalchemy.orm.collections`

    prepare\_instrumentation 的\_prepare\_instrumentation 别名已被删除。

-   `sqlalchemy.orm`

    删除了`EXT_PASS` `EXT_CONTINUE`的别名。

-   `sqlalchemy.engine`

    从`DefaultDialect.preexecute_sequences`到`.preexecute_pk_sequences`的别名已被删除。

    已弃用的 engine\_descriptors()函数已被删除。

-   `sqlalchemy.ext.activemapper`

    模块已移除。

-   `sqlalchemy.ext.assignmapper`

    模块已移除。

-   `sqlalchemy.ext.associationproxy`

    关键字参数在代理的`.append（item， \ ** kw）`上的传递已被删除，现在简单地`.append(item)`

-   `sqlalchemy.ext.selectresults`，`sqlalchemy.mods.selectresults`

    模块已移除。

-   `sqlalchemy.ext.declarative`

    `declared_synonym()` removed.

-   `sqlalchemy.ext.sessioncontext`

    模块已移除。

-   `sqlalchemy.log`

    已将`sqlalchemy.exc.SADeprecationWarning`的`SADeprecationWarning`别名删除。

-   `sqlalchemy.exc`

    `exc.AssertionError`已被删除，并且使用由内置相同名称的 Python 替换。

-   `sqlalchemy.databases.mysql`

    弃用的`get_version_info`方言方法已被删除。

重命名或移动[¶](#renamed-or-moved "Permalink to this headline")
---------------------------------------------------------------

-   `sqlalchemy.exceptions`现在是`sqlalchemy.exc`

    该模块仍然可以以旧名称导入，直到 0.6。

-   `FlushError`，`ConcurrentModificationError`，`UnmappedColumnError` - \>
    sqlalchemy.orm.exc

    这些异常移至 orm 包。导入'sqlalchemy.orm'将在 sqlalchemy.exc 中安装别名，直到 0.6。

-   `sqlalchemy.logging` - \>
    `sqlalchemy.log`

    此内部模块已重命名。使用 py2app 和类似工具扫描导入时，不再需要特殊的套件。

-   `session.Query().iterate_instances()` - \>
    `session.Query().instances()`。

弃用[¶ T0\>](#deprecated "Permalink to this headline")
------------------------------------------------------

-   `Session.save()`, `Session.update()`, `Session.save_or_update()`

    所有三个都被`Session.add()`取代

-   `sqlalchemy.PassiveDefault`

    使用`Column(server_default=...)`将其转换为 sqlalchemy.DefaultClause()。

-   `session.Query().iterate_instances()`它已被重命名为`instances()`。


