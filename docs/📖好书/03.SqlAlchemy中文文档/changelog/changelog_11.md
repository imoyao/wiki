---
title: changelog_11
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/602fe0/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - changelog
tags:
  - 
---
1.1更新日志[¶](#changelog "Permalink to this headline")
=======================================================

1.1.0b2 [¶ T0\>](#change-1.1.0b2 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2016年7月1日

### SQL [¶ T0\>](#change-1.1.0b2-sql "Permalink to this headline")

-   **[sql] [bug]**Fixed issue in SQL math negation operator where the
    type of the expression would no longer be the numeric type of the
    original.
    这会导致类型确定结果集行为的问题。[¶](#change-7006ffe86a58284eda862bbc60b8bc4b)

    这个改变也被**backported**改为：1.0.14

    参考文献：[＃3735](http://www.sqlalchemy.org/trac/ticket/3735)

-   **[sql] [bug]**Fixed bug whereby the `__getstate__` / `__setstate__` methods for
    sqlalchemy.util.Properties were non-working due to the transition in
    the 1.0 series to `__slots__`.
    该问题可能会影响某些第三方应用程序。Pull请求Pieter
    Mulder提供。[¶](#change-5699ea1e56391cae80ed2aa84bf2c6e2)

    这个改变也被**backported**改为：1.0.14

    参考文献：[＃3728](http://www.sqlalchemy.org/trac/ticket/3728)

-   **[sql]
    [bug]**在纯Python和C-extensions版本之间，只有特征整数类型的后端[`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")数据类型所执行的处理已经变得一致，
    C-extension版本将接受来自数据库的任何整数值作为布尔值，而不仅仅是零和一；另外，发送到数据库的非布尔整型值被强制为0或1，而不是作为原始整数值传递。

    也可以看看

    [Non-native boolean integer values coerced to zero/one/None in all
    cases](migration_11.html#change-3730)

    [¶](#change-f3088aa888b7e3a90f1814ce21c0b220)

    参考文献：[＃3730](http://www.sqlalchemy.org/trac/ticket/3730)

-   **[sql] [bug]**回滚[`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")中的验证规则以允许未知字符串值通过，除非标志`validate_string=True`While the immediate use is to allow comparisons to enums
    with LIKE, the fact that this use exists indicates there may be more
    unknown-string-comparsion use cases than we expected, which hints
    that perhaps there are some unknown string-INSERT cases
    too.[¶](#change-61ec601e4af58a2d337d455e2abcc9da)

    参考文献：[＃3725](http://www.sqlalchemy.org/trac/ticket/3725)

### 的PostgreSQL [¶ T0\>](#change-1.1.0b2-postgresql "Permalink to this headline")

-   **[postgresql] [bug] [ext]**Made a slight behavioral change in the
    `sqlalchemy.ext.compiler` extension, whereby the
    existing compilation schemes for an established construct would be
    removed if that construct was itself didn’t already have its own
    dedicated `__visit_name__`.
    这在1.0中很少见，但在1.1 [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")子类`sqltypes.ARRAY`中有此现象。因此，为另一种方言（如SQLite）设置编译处理程序会使主[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")对象不再可编译。[](#change-a5fce71fb2e30fdf321b95c31697aa26)

    参考文献：[＃3732](http://www.sqlalchemy.org/trac/ticket/3732)

### MySQL的[¶ T0\>](#change-1.1.0b2-mysql "Permalink to this headline")

-   **[mysql] [bug]**在[No more generation of an implicit KEY for
    composite primary key w/
    AUTO\_INCREMENT](migration_11.html#change-mysql-3216)生成隐式键有一点，所以如果明确定义了[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")，那么列的顺序就会被精确地保留下来，以便在必要时控制这种行为。[¶](#change-8e0948ee4b6cb64315abc0156aeb1fd6)

    参考文献：[＃3726](http://www.sqlalchemy.org/trac/ticket/3726)

1.1.0b1 [¶ T0\>](#change-1.1.0b1 "Permalink to this headline")
--------------------------------------------------------------

发布日期：2016年6月16日

### ORM [¶ T0\>](#change-1.1.0b1-orm "Permalink to this headline")

-   **[orm] [feature] [ext]**A new ORM extension
    [Indexable](orm_extensions_indexable.html) is added, which allows
    construction of Python attributes which refer to specific elements
    of “indexed” structures such as arrays and JSON fields. 请求Jeong
    YunWon提供的请求。

    也可以看看

    [New Indexable ORM extension](migration_11.html#feature-indexable)

    [¶](#change-b3c884910b59a35c1b5267eca4bbe2b5)

-   **[orm] [feature]**Added new flag
    [`Session.bulk_insert_mappings.render_nulls`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.render_nulls "sqlalchemy.orm.session.Session.bulk_insert_mappings")
    which allows an ORM bulk INSERT to occur with NULL values rendered;
    this bypasses server side defaults, however allows all statements to
    be formed with the same set of columns, allowing them to be batched.
    请求礼拜Tobias
    Sauerwein。[¶](#change-5acfb1b58ae42f608a8630f796d96e7e)

-   **[orm]
    [feature]**添加了新事件[`AttributeEvents.init_scalar()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.init_scalar "sqlalchemy.orm.events.AttributeEvents.init_scalar")，以及一个说明其用法的新示例套件。在持久对象之前，可以使用此事件向Python端属性提供Core生成的默认值。

    也可以看看

    [New init\_scalar() event intercepts default values at ORM
    level](migration_11.html#change-1311)

    [¶](#change-532ef99ecd1dd5bb8ee5ee6a8a2401db)

    参考文献：[＃1311](http://www.sqlalchemy.org/trac/ticket/1311)

-   **[orm] [feature]**将[`AutomapBase.prepare.schema`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase.prepare.params.schema "sqlalchemy.ext.automap.AutomapBase.prepare")添加到[`AutomapBase.prepare()`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")方法中，以指示应反映哪些模式表如果不是默认模式。拉请求由Josh
    Marlow提供。[¶](#change-6b828691a60c4907d089b06e95f44234)

    参考文献：[pull request
    github：237](https://github.com/zzzeek/sqlalchemy/pull/237)

-   **[orm] [feature]**将新参数[`orm.mapper.passive_deletes`](orm_mapping_api.html#sqlalchemy.orm.mapper.params.passive_deletes "sqlalchemy.orm.mapper")添加到可用的映射器选项。这允许DELETE进行仅针对基表的连接表继承映射，同时允许ON
    DELETE CASCADE处理从子类表中删除行。

    也可以看看

    [passive\_deletes feature for joined-inheritance
    mappings](migration_11.html#change-2349)的passive\_deletes功能

    [¶](#change-ebaee83acc1f8f12b712ab57c6ce231d)

    参考文献：[＃2349](http://www.sqlalchemy.org/trac/ticket/2349)

-   **[orm] [feature]**Calling str() on a core SQL construct has been
    made more “friendly”, when the construct contains non-standard SQL
    elements such as RETURNING, array index operations, or
    dialect-specific or custom datatypes.
    现在在这些情况下返回一个字符串，以表示该构造的近似值（通常是Postgresql风格的版本），而不是引发错误。

    也可以看看

    [“Friendly” stringification of Core SQL constructs without a
    dialect](migration_11.html#change-3631)

    [¶](#change-678ae60d4035b7177656f7d144cea811)

    参考文献：[＃3631](http://www.sqlalchemy.org/trac/ticket/3631)

-   **[orm] [feature]**The `str()` call for
    [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    will now take into account the [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    to which the [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    is bound, when generating the string form of the SQL, so that the
    actual SQL that would be emitted to the database is shown, if
    possible. Previously, only the engine associated with the
    [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
    to which the mappings are associated would be used, if present.
    如果没有绑定可以位于映射关联的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")或[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")上，那么“默认”方言用于呈现SQL，就像以前的情况。

    也可以看看

    [Stringify of Query will consult the Session for the correct
    dialect](migration_11.html#change-3081)

    [¶](#change-b748efc9574b29a2ea49e7c0333742a1)

    参考文献：[＃3081](http://www.sqlalchemy.org/trac/ticket/3081)

-   **[orm] [feature]**The [`SessionEvents`](orm_events.html#sqlalchemy.orm.events.SessionEvents "sqlalchemy.orm.events.SessionEvents")
    suite now includes events to allow unambiguous tracking of all
    object lifecycle state transitions in terms of the [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    itself, e.g. pending, transient, persistent, detached.
    每个事件中对象的状态也被定义。

    也可以看看

    [New Session lifecycle events](migration_11.html#change-2677)

    [¶](#change-d5cf16064aa92922d05395b09c928698)

    参考文献：[＃2677](http://www.sqlalchemy.org/trac/ticket/2677)

-   **[orm]
    [feature]**添加了一个新的会话生命周期状态[deleted](glossary.html#term-deleted)。这个新的状态代表一个从[persistent](glossary.html#term-persistent)状态中被删除的对象，并且一旦事务被提交就会移动到[detached](glossary.html#term-detached)状态。这解决了长期存在的问题，即被删除的对象存在于灰色区域中的持久对象和分离对象之间。The
    [`InstanceState.persistent`{](orm_internals.html#sqlalchemy.orm.state.InstanceState.persistent "sqlalchemy.orm.state.InstanceState.persistent")
    accessor will **no longer** report on a deleted object as
    persistent; the [`InstanceState.deleted`](orm_internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")
    accessor will instead be True for these objects, until they become
    detached.

    也可以看看

    [New Session lifecycle events](migration_11.html#change-2677)

    [¶](#change-df3d7ca7a278488ea611b03405eb14fd)

    参考文献：[＃2677](http://www.sqlalchemy.org/trac/ticket/2677)

-   **[orm]
    [feature]**为将映射类或映射实例传递到解释为SQL绑定参数的上下文中的常见错误情况添加了新的检查；为此提出了一个新的例外。

    也可以看看

    [Specific checks added for passing mapped classes, instances as SQL
    literals](migration_11.html#change-3321)

    [¶](#change-09452835bc692d53fcd69eaae680cdf6)

    参考文献：[＃3321](http://www.sqlalchemy.org/trac/ticket/3321)

-   **[orm] [feature]**Added new relationship loading strategy
    [`orm.raiseload()`](orm_loading_relationships.html#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload")
    (also accessible via `lazy='raise'`).
    这种策略的行为几乎与[`orm.noload()`](orm_loading_relationships.html#sqlalchemy.orm.noload "sqlalchemy.orm.noload")类似，但不是返回`None`，而是引发一个InvalidRequestError。拉请求阿德里安Moennich礼貌。

    也可以看看

    [New “raise” loader strategy](migration_11.html#change-3512)

    [¶](#change-ceee86d0abb726cd008560b25849fd6d)

    参考文献：[＃3512](http://www.sqlalchemy.org/trac/ticket/3512)，[请求github：193](https://github.com/zzzeek/sqlalchemy/pull/193)

-   **[orm]
    [bug]**修复了将对象从一个父对象多对一地更改为另一个对象时与外键属性的未刷新修改结合使用时可能不一致的问题。属性移动现在考虑外键的数据库提交值，以便找到要移动的对象的“上一个”父对象。这允许事件正确启动，包括backref事件。以前，这些事件并不总是会发生。可能依赖于先前破坏行为的应用程序可能会受到影响。

    也可以看看

    [Fix involving many-to-one object moves with user-initiated foriegn
    key manipulations](migration_11.html#change-3708)

    [¶](#change-9093c4c590e858f7a6341c361cd97105)

    参考文献：[＃3708](http://www.sqlalchemy.org/trac/ticket/3708)

-   **[orm] [bug]**Fixed bug where deferred columns would inadvertently
    be set up for database load on the next object-wide unexpire, when
    the object were merged into the session with
    `session.merge(obj, load=False)`.[¶](#change-649f635edb55d8224f0ebeb39df69dd6)

    参考文献：[＃3488](http://www.sqlalchemy.org/trac/ticket/3488)

-   **[orm] [bug]
    [mysql]**进一步继续讨论[＃2696](http://www.sqlalchemy.org/trac/ticket/2696)中首先覆盖的保存点的常见MySQL异常情况，其中[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")放置在SAVEPOINT在回滚已改进之前消失，以允许[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")在该保存点之外仍然起作用。假定保存点操作失败并被取消。

    也可以看看

    [Improved Session state when a SAVEPOINT is cancelled by the
    database](migration_11.html#change-3680)取消SAVEPOINT时改进了会话状态

    [¶](#change-f28176c3e7691799da5b2674680209c0)

    参考文献：[＃3680](http://www.sqlalchemy.org/trac/ticket/3680)

-   **[orm] [bug]**Fixed bug where a newly inserted instance that is
    rolled back would still potentially cause persistence conflicts on
    the next transaction, because the instance would not be checked that
    it was expired.
    此修复程序将解决大量导致“身份X与持久实例Y冲突的新实例”错误的大类病例。

    也可以看看

    [Erroneous “new instance X conflicts with persistent instance Y”
    flush errors fixed](migration_11.html#change-3677)

    [¶](#change-8a920447463b0b57def835f194bc947f)

    参考文献：[＃3677](http://www.sqlalchemy.org/trac/ticket/3677)

-   **[orm] [bug]**An improvement to the workings of
    [`Query.correlate()`](orm_query.html#sqlalchemy.orm.query.Query.correlate "sqlalchemy.orm.query.Query.correlate")
    such that when a “polymorphic” entity is used which represents a
    straight join of several tables, the statement will ensure that all
    the tables within the join are part of what’s correlating.

    也可以看看

    [Improvements to the Query.correlate method with polymoprhic
    entities](migration_11.html#change-3662)改进Query.correlate方法

    [¶](#change-8d8169201233ee410bfb943fcbd64e8f)

    参考文献：[＃3662](http://www.sqlalchemy.org/trac/ticket/3662)

-   **[orm] [bug]**Fixed bug which would cause an eagerly loaded
    many-to-one attribute to not be loaded, if the joined eager load
    were from a row where the same entity were present multiple times,
    some calling for the attribute to be eagerly loaded and others not.
    尽管不同的加载程序路径已经处理父实体，但修改此处的逻辑以接受属性。

    也可以看看

    [Joined eager loading where the same entity is present multiple
    times in one row](migration_11.html#change-3431)

    [¶](#change-4654a27da3f75152d9bb46cdb7469e40)

    参考文献：[＃3431](http://www.sqlalchemy.org/trac/ticket/3431)

-   **[orm] [bug]**A refinement to the logic which adds columns to the
    resulting SQL when [`Query.distinct()`](orm_query.html#sqlalchemy.orm.query.Query.distinct "sqlalchemy.orm.query.Query.distinct")
    is combined with [`Query.order_by()`](orm_query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")
    such that columns which are already present will not be added a
    second time, even if they are labeled with a different name.
    无论如何改变，添加到SQL中的额外列从未在最终结果中返回，因此此更改仅影响语句的字符串形式以及在Core执行上下文中使用时的行为。此外，使用DISTINCT
    ON格式时不再添加列，只要由于加入了预先加载而不将查询包装在子查询中。

    也可以看看

    [Columns no longer added redundantly with DISTINCT + ORDER
    BY](migration_11.html#change-3641)添加列

    [¶](#change-3e46993e39e8cecdbbf5cb968b80c4eb)

    参考文献：[＃3641](http://www.sqlalchemy.org/trac/ticket/3641)

-   **[orm] [bug]**Fixed issue where two same-named relationships that
    refer to a base class and a concrete-inherited subclass would raise
    an error if those relationships were set up using “backref”, while
    setting up the identical configuration using relationship() instead
    with the conflicting names would succeed, as is allowed in the case
    of a concrete mapping.

    也可以看看

    [Same-named backrefs will not raise an error when applied to
    concrete inheritance
    subclasses](migration_11.html#change-3630)时，相同名称的backrefs不会引发错误

    [¶](#change-89b5808175cb646ca27aee96edc8813f)

    参考文献：[＃3630](http://www.sqlalchemy.org/trac/ticket/3630)

-   **[orm] [bug]**The [`Session.merge()`](orm_session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
    method now tracks pending objects by primary key before emitting an
    INSERT, and merges distinct objects with duplicate primary keys
    together as they are encountered, which is essentially
    semi-deterministic at best. 此行为与持久对象已发生的情况相匹配。

    也可以看看

    [Session.merge resolves pending conflicts the same as
    persistent](migration_11.html#change-3601)

    [¶](#change-ac6144457b07a73e68843f65fff61adb)

    参考文献：[＃3601](http://www.sqlalchemy.org/trac/ticket/3601)

-   **[orm] [bug]**Fixed bug where the “single table inheritance”
    criteria would be added onto the end of a query in some
    inappropriate situations, such as when querying from an exists() of
    a single-inheritance subclass.

    也可以看看

    [Further Fixes to single-table inheritance
    querying](migration_11.html#change-3582)

    [¶](#change-dd65aebe5daa65ac33d96732d8c19890)

    参考文献：[＃3582](http://www.sqlalchemy.org/trac/ticket/3582)

-   **[orm] [bug]**Added a new type-level modifier
    [`TypeEngine.evaluates_none()`](core_type_api.html#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")
    which indicates to the ORM that a positive set of None should be
    persisted as the value NULL, instead of omitting the column from the
    INSERT statement.
    此功能既可用作[＃3514](http://www.sqlalchemy.org/trac/ticket/3514)实现的一部分，也可用于任何类型的独立功能。

    也可以看看

    [New options allowing explicit persistence of NULL over a
    default](migration_11.html#change-3250)上显式持久化NULL的新选项

    [¶](#change-ad8a491013281436a5ec669721de6d99)

    参考文献：[＃3250](http://www.sqlalchemy.org/trac/ticket/3250)

-   **[orm] [bug]**Internal calls to “bookkeeping” functions within
    [`Session.bulk_save_objects()`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects "sqlalchemy.orm.session.Session.bulk_save_objects")
    and related bulk methods have been scaled back to the extent that
    this functionality is not currently used, e.g. checks for column
    default values to be fetched after an INSERT or UPDATE
    statement.[¶](#change-48c47319c947b658d154aa9c012b32e3)

    参考文献：[＃3526](http://www.sqlalchemy.org/trac/ticket/3526)

-   **[orm] [bug] [postgresql]**结合Postgresql [`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")类型对`None`的值进行了修补。当[`JSON.none_as_null`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON.params.none_as_null "sqlalchemy.dialects.mysql.JSON")标志的默认值为`False`时，ORM现在可以正确插入Json“'null'”字符串到列中ORM对象被设置为值`None`，或者当`None`值与[`Session.bulk_insert_mappings()`](orm_session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")一起使用时，**t12\>如果列上有默认或服务器默认值。**

    也可以看看

    [JSON “null” is inserted as expected with ORM operations, regardless
    of column default present](migration_11.html#change-3514)

    [New options allowing explicit persistence of NULL over a
    default](migration_11.html#change-3250)上显式持久化NULL的新选项

    [¶](#change-1b66765ab8f05691258b629037065a6e)

    参考文献：[＃3514](http://www.sqlalchemy.org/trac/ticket/3514)

-   **[orm] [change]**不推荐使用[`Mapper.order_by`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.params.order_by "sqlalchemy.orm.mapper.Mapper")参数。这是一个旧参数，不再与SQLAlchemy的工作方式有关，一旦Query对象被引入。通过贬低它，我们确定我们不支持非工作用例，并鼓励应用程序退出使用此参数。

    也可以看看

    [Mapper.order\_by is deprecated](migration_11.html#change-3394)

    [¶](#change-09669497f855398505a14d647f0b239c)

    参考文献：[＃3394](http://www.sqlalchemy.org/trac/ticket/3394)

-   **[orm] [change]**不推荐使用[`Session.weak_identity_map`](orm_session_api.html#sqlalchemy.orm.session.Session.params.weak_identity_map "sqlalchemy.orm.session.Session")参数。请参阅[Session
    Referencing
    Behavior](orm_session_state_management.html#session-referencing-behavior)中的新配方，了解基于事件的方法来维护强身份图行为。

    也可以看看

    [New Session lifecycle events](migration_11.html#change-2677)

    [¶](#change-32d6229592346b5ad6b2e70e7d6a902d)

    参考文献：[＃2677](http://www.sqlalchemy.org/trac/ticket/2677)

### 发动机[¶ T0\>](#change-1.1.0b1-engine "Permalink to this headline")

-   **[engine] [feature]**Added connection pool events
    `ConnectionEvents.close()`,
    `ConnectionEvents.detach()`,
    `ConnectionEvents.close_detached()`.[¶](#change-a6533a6047f760f9f9ccee7003a447c2)

-   **[engine] [feature]**用于日志记录，异常和`repr()`目的的绑定参数集和结果行的所有字符串格式现在会截断每个集合中非常大的标量值，包括“N个字符截断”符号，类似于大型多参数集的显示如何被截断。

    也可以看看

    [Large parameter and row values are now truncated in logging and
    exception
    displays](migration_11.html#change-2837)中，大参数和行值现在被截断

    [¶](#change-d0cb65da9fa15d19af196aad7ff5623e)

    参考文献：[＃2837](http://www.sqlalchemy.org/trac/ticket/2837)

-   **[engine] [feature]**添加了[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的多租户模式转换。这支持在许多模式中使用同一组[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的应用程序的用例，例如schema-per-user。添加新的执行选项[`Connection.execution_options.schema_translate_map`](core_connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map "sqlalchemy.engine.Connection.execution_options")。

    也可以看看

    [Multi-Tenancy Schema Translation for Table
    objects](migration_11.html#change-2685)

    [¶](#change-b54566e0a3f779d77ce78d1bb4807399)

    参考文献：[＃2685](http://www.sqlalchemy.org/trac/ticket/2685)

-   **[engine]
    [feature]**为引擎添加了一个新的入口点系统，以允许在URL的查询字符串中声明“插件”。可以编写自定义插件，预先给予机会改变和/或使用引擎的URL和关键字参数，然后在引擎创建时将给引擎本身以允许进行额外的修改或事件注册。插件被编写为[`CreateEnginePlugin`](core_connections.html#sqlalchemy.engine.CreateEnginePlugin "sqlalchemy.engine.CreateEnginePlugin")的子类；详情请参见该课程。[¶](#change-1afaa182eadbbcdb22dd3e0761a0950f)

    参考文献：[＃3536](http://www.sqlalchemy.org/trac/ticket/3536)

### SQL [¶ T0\>](#change-1.1.0b1-sql "Permalink to this headline")

-   **[sql] [feature]**通过新的[`FromClause.tablesample()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.tablesample "sqlalchemy.sql.expression.FromClause.tablesample")方法和独立函数添加了TABLESAMPLE支持。拉尔请求IljaEverilä礼貌。

    也可以看看

    [Support for TABLESAMPLE](migration_11.html#change-3718)

    [¶](#change-360a40aabf1019e2f12d467220dd3e37)

    参考文献：[＃3718](http://www.sqlalchemy.org/trac/ticket/3718)

-   **[sql] [feature]**使用[`expression.over.range_`](core_sqlelement.html#sqlalchemy.sql.expression.over.params.range_ "sqlalchemy.sql.expression.over")和[`expression.over.rows`](core_sqlelement.html#sqlalchemy.sql.expression.over.params.rows "sqlalchemy.sql.expression.over")参数增加了对窗口函数范围的支持。

    也可以看看

    [Support for RANGE and ROWS specification within window
    functions](migration_11.html#change-3049)

    [¶](#change-0fea1bc883b8c90b2f54079c0440f160)

    参考文献：[＃3049](http://www.sqlalchemy.org/trac/ticket/3049)

-   **[sql] [feature]**Implemented reflection of CHECK constraints for
    SQLite and Postgresql.
    这可以通过新的检查器方法[`Inspector.get_check_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints "sqlalchemy.engine.reflection.Inspector.get_check_constraints")以及以[`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")对象的形式反映[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")约束收集。拉格请求礼貌AlexGrönholm。[¶](#change-9c0058e414df17a6d151e9268e00fc34)

    参考：[请求位桶：80](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/80)

-   **[sql] [feature]**New [`ColumnOperators.is_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
    and [`ColumnOperators.isnot_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
    operators; pull request courtesy Sebastian Bank.

    也可以看看

    [Support for IS DISTINCT FROM and IS NOT DISTINCT
    FROM](migration_11.html#change-is-distinct-from)

    [¶](#change-47ebc8c173b02b3858f2a91e5c4bc3d4)

-   **[sql] [feature]**在`DDLCompiler.visit_create_table()`中添加了名为`DDLCompiler.create_table_suffix()`的钩子，允许自定义方言在添加关键字之后“CREATE
    TABLE”子句。拉马克桑丹要求礼貌。[¶](#change-852081e60156f45afd19aa6656b45262)

    参考文献：[请求github：275](https://github.com/zzzeek/sqlalchemy/pull/275)

-   **[sql] [feature]**现在，可以从[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")返回的行容纳负整数索引。请求礼貌Emanuele
    Gaifas。

    也可以看看

    [Negative integer indexes accommodated by Core result
    rows](migration_11.html#change-gh-231)

    [¶](#change-0746e16f1e36084f02c6d55a068046a0)

    参考文献：[请求github：231](https://github.com/zzzeek/sqlalchemy/pull/231)

-   **[sql] [feature]**Added [`Select.lateral()`](core_selectable.html#sqlalchemy.sql.expression.Select.lateral "sqlalchemy.sql.expression.Select.lateral")
    and related constructs to allow for the SQL standard LATERAL
    keyword, currently only supported by Postgresql.

    也可以看看

    [Support for the SQL LATERAL keyword](migration_11.html#change-2857)

    [¶](#change-b96a97734ea3e708037e4856542e8e74)

    参考文献：[＃2857](http://www.sqlalchemy.org/trac/ticket/2857)

-   **[sql] [feature]**增加了对“Core Full”和ORM渲染“FULL OUTER
    JOIN”的支持。拉提请求Stefan Urbanek提供。

    也可以看看

    [Core and ORM support for FULL OUTER
    JOIN](migration_11.html#change-1957)

    [¶](#change-a91f9625fbd8a65e11808cecf7088895)

    参考文献：[＃1957](http://www.sqlalchemy.org/trac/ticket/1957)，[请求github：209](https://github.com/zzzeek/sqlalchemy/pull/209)

-   **[sql] [feature]**CTE functionality has been expanded to support
    all DML, allowing INSERT, UPDATE, and DELETE statements to both
    specify their own WITH clause, as well as for these statements
    themselves to be CTE expressions when they include a RETURNING
    clause.

    也可以看看

    [CTE Support for INSERT, UPDATE,
    DELETE](migration_11.html#change-2551)

    [¶](#change-2e0fda4bfd6e2b5255952d61f70e148f)

    参考文献：[＃2551](http://www.sqlalchemy.org/trac/ticket/2551)

-   **[sql] [feature]**添加了对PEP-435型枚举类的支持，即Python
    3的`enum.Enum`类，但也包括兼容的枚举库，支持[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")数据类型。[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")数据类型现在还执行输入值的Python验证，并添加一个选项以放弃创建CHECK约束[`Enum.create_constraint`](core_type_basics.html#sqlalchemy.types.Enum.params.create_constraint "sqlalchemy.types.Enum")。拉格请求礼貌AlexGrönholm。

    也可以看看

    [Support for Python’s native enum type and compatible
    forms](migration_11.html#change-3292)

    [The Enum type now does in-Python validation of
    values](migration_11.html#change-3095)

    [¶](#change-9d6d98d7acabc8564b8eebb11c28a624)

    参考文献：[＃3292](http://www.sqlalchemy.org/trac/ticket/3292)，[＃3095](http://www.sqlalchemy.org/trac/ticket/3095)

-   **[sql] [feature]**A deep improvement to the recently added
    [`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")
    method, and its interaction with result-row processing, now allows
    the columns passed to the method to be positionally matched with the
    result columns in the statement, rather than matching on name alone.
    这样做的好处包括，在将文本SQL语句链接到ORM或Core表模型时，不需要为公共列名称添加标签或重复数据删除系统，这也意味着无需担心标签名称如何匹配ORM列等等。In
    addition, the [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
    has been further enhanced to map column and string keys to a row
    with greater precision in some cases.

    也可以看看

    [ResultSet column matching enhancements; positional column setup for
    textual SQL](migration_11.html#change-3501) - feature overview

    [TextClause.columns() will match columns positionally, not by name,
    when passed positionally](migration_11.html#behavior-change-3501) -
    backwards compatibility remarks

    [¶](#change-62a0a934a2b0bba2ce629ca376fa5890)

    参考文献：[＃3501](http://www.sqlalchemy.org/trac/ticket/3501)

-   **[sql] [feature]**为核心[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")添加了一个新类型。This
    is the base of the PostgreSQL [`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
    type as well as that of the new [`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")
    type, so that a PG/MySQL-agnostic JSON column may be used.
    该类型具有基本索引和路径搜索支持。

    也可以看看

    [JSON support added to Core](migration_11.html#change-3619)

    [¶](#change-17c3b4f058ed555d27ca96a245bdde91)

    参考文献：[＃3619](http://www.sqlalchemy.org/trac/ticket/3619)

-   **[sql]
    [feature]**增加了对`＆lt； t2＆gt； WITHIN 形式的“集合” GROUP （ORDER  tt>> BY >）`，使用[`FunctionElement.within_group()`](core_functions.html#sqlalchemy.sql.functions.FunctionElement.within_group "sqlalchemy.sql.functions.FunctionElement.within_group")已经添加了一系列具有从该集合派生的返回类型的常见集合集合函数。这包括[`percentile_cont`](core_functions.html#sqlalchemy.sql.functions.percentile_cont "sqlalchemy.sql.functions.percentile_cont")，[`dense_rank`](core_functions.html#sqlalchemy.sql.functions.dense_rank "sqlalchemy.sql.functions.dense_rank")等功能。

    也可以看看

    [New Function features, “WITHIN GROUP”, array\_agg and set aggregate
    functions](migration_11.html#change-3132)

    [¶](#change-f1a5b143ac2614a44c4d4be425086e5e)

    参考文献：[＃1370](http://www.sqlalchemy.org/trac/ticket/1370)

-   **[sql] [feature]
    [postgresql]**增加了对SQL标准函数[`array_agg`](core_functions.html#sqlalchemy.sql.functions.array_agg "sqlalchemy.sql.functions.array_agg")的支持，该函数会自动返回正确的[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")键入和支持索引/切片操作，以及[`postgresql.array_agg()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array_agg "sqlalchemy.dialects.postgresql.array_agg")，它会返回一个带有附加比较特征的[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")。由于目前只有Postgresql支持数组，所以实际上只能在Postgresql上运行。还添加了一个新的构造[`postgresql.aggregate_order_by`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by "sqlalchemy.dialects.postgresql.aggregate_order_by")，以支持PG的“ORDER
    BY”扩展。

    也可以看看

    [New Function features, “WITHIN GROUP”, array\_agg and set aggregate
    functions](migration_11.html#change-3132)

    [¶](#change-1765f3641a6e264a7fe24088c46a4b59)

    参考文献：[＃3132](http://www.sqlalchemy.org/trac/ticket/3132)

-   **[sql] [feature]**为核心[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")添加了一个新类型。这是PostgreSQL
    [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型的基础，现在成为Core的一部分，开始支持各种支持SQL标准数组的支持功能，包括一些功能和最终支持其他数据库上的本地数组一个“数组”的概念，比如DB2或Oracle。此外，还添加了新的运算符[`expression.any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")和[`expression.all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")。这些不仅支持Postgresql上的数组构造，还支持在MySQL上可用的子查询（但可惜不在Postgresql上）。

    也可以看看

    [Array support added to Core; new ANY and ALL
    operators](migration_11.html#change-3516)

    [¶](#change-073de265914ed4fee6ddbc41fb452906)

    参考文献：[＃3516](http://www.sqlalchemy.org/trac/ticket/3516)

-   **[sql] [bug]** [`FromClause.count()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.count "sqlalchemy.sql.expression.FromClause.count")已弃用。该函数使用表中的任意列并且不可靠；对于核心用途，应该首选`func.count()`。[¶](#change-33f3b50c7e87df7564c217803f642cf6)

    参考文献：[＃3724](http://www.sqlalchemy.org/trac/ticket/3724)

-   **[sql] [bug]**Fixed an assertion that would raise somewhat
    inappropriately if a [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    were associated with a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    that is associated with a lower-case-t [`TableClause`](core_selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause");
    the association should be ignored for the purposes of associating
    the index with a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").[¶](#change-0555461d7e299c51372dcc39d1516f29)

    参考文献：[＃3616](http://www.sqlalchemy.org/trac/ticket/3616)

-   **[sql] [bug]**The [`type_coerce()`](core_sqlelement.html#sqlalchemy.sql.expression.type_coerce "sqlalchemy.sql.expression.type_coerce")
    construct is now a fully fledged Core expression element which is
    late-evaluated at compile time.
    以前，函数只是一个转换函数，它可以通过返回一个面向列的表达式或一个给定的[`BindParameter`](core_sqlelement.html#sqlalchemy.sql.expression.BindParameter "sqlalchemy.sql.expression.BindParameter")对象的副本的[`Label`](core_sqlelement.html#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")来处理不同的表达式输入，特别是当ORM级表达式转换将列转换为绑定参数时（例如，用于延迟加载）时，操作无法在逻辑上维护。

    也可以看看

    [The type\_coerce function is now a persistent SQL
    element](migration_11.html#change-3531)

    [¶](#change-4c12275c79c42b62d1c375f76c771599)

    参考文献：[＃3531](http://www.sqlalchemy.org/trac/ticket/3531)

-   **[sql] [bug]**The [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
    type extender will now work in conjunction with a
    [`SchemaType`](core_type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")
    implementation, typically [`Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    or [`Boolean`](core_type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")
    with regards to ensuring that the per-table events are propagated
    from the implementation type to the outer type.
    这些事件用于确保约束或Postgresql类型（例如ENUM）与父表一起正确创建（并可能被删除）。

    也可以看看

    [TypeDecorator now works with Enum, Boolean, “schema” types
    automatically](migration_11.html#change-2919)

    [¶](#change-6f4cf479ea625f2b2f5aa2a4e952959b)

    参考文献：[＃2919](http://www.sqlalchemy.org/trac/ticket/2919)

-   **[sql] [bug]**The behavior of the [`union()`](core_selectable.html#sqlalchemy.sql.expression.union "sqlalchemy.sql.expression.union")
    construct and related constructs such as [`Query.union()`](orm_query.html#sqlalchemy.orm.query.Query.union "sqlalchemy.orm.query.Query.union")
    now handle the case where the embedded SELECT statements need to be
    parenthesized due to the fact that they include LIMIT, OFFSET and/or
    ORDER BY.
    这些查询**在SQLite**上不起作用，并且会像以前那样在后端上失败，但现在应该在所有其他后端上运行。

    也可以看看

    [A UNION or similar of SELECTs with LIMIT/OFFSET/ORDER BY now
    parenthesizes the embedded selects](migration_11.html#change-2528)

    [¶](#change-e9e0e04652a369370f2eae50538498c9)

    参考文献：[＃2528](http://www.sqlalchemy.org/trac/ticket/2528)

-   **[sql] [mysql] [change]**The system by which a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    considers itself to be an “auto increment” column has been changed,
    such that autoincrement is no longer implicitly enabled for a
    [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    that has a composite primary key.
    为了适应能够为复合PK成员列启用自动增量功能，同时保持SQLAlchemy为单个整数主键启用隐式自动增量的长期行为，第三个状态已添加到[`Column.autoincrement`](core_metadata.html#sqlalchemy.schema.Column.params.autoincrement "sqlalchemy.schema.Column")参数`"auto"`，现在是默认值。

    也可以看看

    [The .autoincrement directive is no longer implicitly enabled for a
    composite primary key column](migration_11.html#change-3216)

    [No more generation of an implicit KEY for composite primary key w/
    AUTO\_INCREMENT](migration_11.html#change-mysql-3216)的组合主键生成隐式KEY

    [¶](#change-6d7175b6067e4d63a84c6dccbbda213f)

    参考文献：[＃3216](http://www.sqlalchemy.org/trac/ticket/3216)

### 架构[¶ T0\>](#change-1.1.0b1-schema "Permalink to this headline")

-   **[schema] [enhancement]**传递给[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的默认生成函数现在通过“update\_wrapper”运行，或者在传递可调用非函数时通过等效函数运行内省工具保留了包装函数的名称和文档字符串。请求礼貌hsum。[¶](#change-c7382e5258b1fe48e537f64ed89e23f6)

    参考文献：[请求github：204](https://github.com/zzzeek/sqlalchemy/pull/204)

### 的PostgreSQL [¶ T0\>](#change-1.1.0b1-postgresql "Permalink to this headline")

-   **[postgresql]
    [feature]**使用新的Postgresql特定的[`postgresql.dml.Insert`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.Insert "sqlalchemy.dialects.postgresql.dml.Insert")对象添加了对Postgresql的INSERT..ON
    CONFLICT的支持。拉宾的请求和广泛的努力由罗宾托马斯。

    也可以看看

    [Support for INSERT..ON CONFLICT (DO UPDATE | DO
    NOTHING)](migration_11.html#change-3529)

    [¶](#change-b5af3aea27f2ddfa949adb65b413e64a)

    参考文献：[＃3529](http://www.sqlalchemy.org/trac/ticket/3529)

-   **[postgresql] [feature]**如果在[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")上设置了`postgresql_concurrently`标志，且DROP
    INDEX的DDL将发出“CONCURRENTLY”在使用中被检测为Postgresql
    9.2或更高版本。对于CREATE
    INDEX，还添加了数据库版本检测，如果PG版本小于8.2，则会删除该子句。请求礼物Iuri
    de Silvio。[¶](#change-5d11b5a42524d1e67d0cff645c9823dc)

    参考文献：[pull request
    bitbucket：84](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/84)

-   **[postgresql]
    [feature]**增加了新的参数[`PGInspector.get_view_names.include`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names.params.include "sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names")，允许指定应返回哪种视图。目前包括“简单”和“物化”视图。请求Sebastian
    Bank提供。[¶](#change-28b7f4677e511cd22a9dd16745eed45d)

    参考文献：[＃3588](http://www.sqlalchemy.org/trac/ticket/3588)

-   **[postgresql] [feature]**添加`postgresql_tablespace`作为[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")的参数，以允许为Postgresql中的索引指定TABLESPACE。补充[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")上的同名参数。请求礼貌Benjamin
    Bertrand。[¶](#change-a00e0127e1725a49a0b06bb28f6955d7)

    参考文献：[＃3720](http://www.sqlalchemy.org/trac/ticket/3720)

-   **[postgresql] [feature]**Added new parameter
    [`GenerativeSelect.with_for_update.key_share`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.key_share "sqlalchemy.sql.expression.GenerativeSelect.with_for_update"),
    which will render the `FOR NO KEY UPDATE`
    version of `FOR UPDATE` and
    `FOR KEY SHARE` instead of `FOR SHARE` on the Postgresql backend.
    请求谢谢Skopin。[¶](#change-649a821a56db1d45186876e467cf2875)

    参考文献：[请求github：297](https://github.com/zzzeek/sqlalchemy/pull/297)

-   **[postgresql] [feature] [oracle]**Added new parameter
    [`GenerativeSelect.with_for_update.skip_locked`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update.params.skip_locked "sqlalchemy.sql.expression.GenerativeSelect.with_for_update"),
    which will render the `SKIP LOCKED` phrase for a
    `FOR UPDATE` or `FOR SHARE`
    lock on the Postgresql and Oracle backends. 拉请求Jack
    Zhou提供。[¶](#change-36718d0ab64a4cacea7a24fad8df0070)

    参考文献：[pull request
    bitbucket：86](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/86)

-   **[postgresql] [feature]**为PyGreSQL
    Postgresql方言增加了一种新的方言。感谢Christoph Zwerschke和Kaolin
    Imago Fire的努力。[¶](#change-41c7633e830699e83927635c357dbb4c)

-   **[postgresql]
    [feature]**增加了一个新的常量`postgresql.JSON.NULL`，表示无论其他设置如何，都应该使用JSON
    NULL值作为值。

    也可以看看

    [New JSON.NULL Constant
    Added](migration_11.html#change-3514-jsonnull)

    [¶](#change-19aa6de2dd87b7d89df8d37af407d32c)

    参考文献：[＃3514](http://www.sqlalchemy.org/trac/ticket/3514)

-   **[postgresql]
    [bug]**新增支持将物化视图的来源反映到[`Inspector.get_view_definition()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_definition "sqlalchemy.engine.reflection.Inspector.get_view_definition")方法的Postgresql版本。[¶](#change-5df5fd63f9f8615d9db6cdf04a4daeef)

    参考文献：[＃3587](http://www.sqlalchemy.org/trac/ticket/3587)

-   **[postgresql] [bug]**The use of a [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
    object that refers to a [`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    or [`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
    subtype will now emit the expected “CREATE TYPE” and “DROP TYPE” DDL
    when the type is used within a “CREATE TABLE” or “DROP TABLE”.

    也可以看看

    [ARRAY with ENUM will now emit CREATE TYPE for the
    ENUM](migration_11.html#change-2729)

    [¶](#change-47dd8bf4fad0416dfd0377b613df9e99)

    参考文献：[＃2729](http://www.sqlalchemy.org/trac/ticket/2729)

-   **[postgresql] [bug]**特殊数据类型（如[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")，[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")和[`postgresql.HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")现在设置为False，这允许这些类型可以在包含行内实体的ORM查询中获取。

    也可以看看

    [Changes regarding “unhashable”
    types](migration_11.html#change-3499)

    [ARRAY and JSON types now correctly specify
    “unhashable”](migration_11.html#change-3499-postgresql)

    [¶](#change-de38578e28bc8265d15f20fa71a4ac1b)

    参考文献：[＃3499](http://www.sqlalchemy.org/trac/ticket/3499)

-   **[postgresql] [bug]**The Postgresql [`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
    type now supports multidimensional indexed access, e.g. expressions
    such as `somecol[5][6]` without any need for
    explicit casts or type coercions, provided that the
    [`postgresql.ARRAY.dimensions`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.params.dimensions "sqlalchemy.dialects.postgresql.ARRAY")
    parameter is set to the desired number of dimensions.

    也可以看看

    [Correct SQL Types are Established from Indexed Access of ARRAY,
    JSON, HSTORE](migration_11.html#change-3503)

    [¶](#change-67a74d635741c7b8299e75c637f764fa)

    参考文献：[＃3487](http://www.sqlalchemy.org/trac/ticket/3487)

-   **[postgresql] [bug]**使用索引访问时，[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")和[`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")的返回类型已得到修复，例如Postgresql本身，并返回一个表达式，该表达式本身是[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")或[`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")类型。之前，访问器将返回[`NullType`](core_type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")，这将禁止使用后续的类JSON运算符。

    也可以看看

    [Correct SQL Types are Established from Indexed Access of ARRAY,
    JSON, HSTORE](migration_11.html#change-3503)

    [¶](#change-7250d82c6e54b03841a530346c262638)

    参考文献：[＃3503](http://www.sqlalchemy.org/trac/ticket/3503)

-   **[postgresql] [bug]**The [`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON"),
    [`postgresql.JSONB`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")
    and [`postgresql.HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")
    datatypes now allow full control over the return type from an
    indexed textual access operation, either
    `column[someindex].astext` for a JSON type or
    `column[someindex]` for an HSTORE type, via the
    [`postgresql.JSON.astext_type`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.params.astext_type "sqlalchemy.dialects.postgresql.JSON")
    and [`postgresql.HSTORE.text_type`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE.params.text_type "sqlalchemy.dialects.postgresql.HSTORE")
    parameters.

    也可以看看

    [Correct SQL Types are Established from Indexed Access of ARRAY,
    JSON, HSTORE](migration_11.html#change-3503)

    [¶](#change-e131ab33b04196b6d2081a5e820d4974)

    参考文献：[＃3503](http://www.sqlalchemy.org/trac/ticket/3503)

-   **[postgresql] [bug]**The [`postgresql.JSON.Comparator.astext`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")
    modifier no longer calls upon [`ColumnElement.cast()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")
    implicitly, as PG’s JSON/JSONB types allow cross-casting between
    each other as well.
    在JSON索引访问中使用[`ColumnElement.cast()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")的代码，例如需要修改`col[someindex].cast(Integer)`，以显式调用[`postgresql.JSON.Comparator.astext`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")。

    也可以看看

    [The JSON cast() operation now requires .astext is called
    explicitly](migration_11.html#change-3503-cast)

    [¶](#change-6dfedfbab62807e6296ba6410d21fa16)

    参考文献：[＃3503](http://www.sqlalchemy.org/trac/ticket/3503)

-   **[postgresql]
    [change]**已过时弃用`sqlalchemy.dialects.postgres`模块；这已经发出了许多年的警告，并且项目应该调用`sqlalchemy.dialects.postgresql`。然而，`postgres://`形式的引擎网址仍然会继续运作。[¶](#change-6330dccd9f95ad0cf2168ee7ac940254)

### MySQL的[¶ T0\>](#change-1.1.0b1-mysql "Permalink to this headline")

-   **[mysql]
    [feature]**通过AUTOCOMMIT隔离级别设置增加了对MySQL驱动程序的“autocommit”的支持。请求Roman
    Romania礼貌的请求。

    也可以看看

    [Added support for AUTOCOMMIT “isolation
    level”](migration_11.html#change-3332)

    [¶](#change-9205bf2037f2de73d4da5d5c4ede6d18)

    参考文献：[＃3332](http://www.sqlalchemy.org/trac/ticket/3332)

-   **[mysql] [feature]**为MySQL 5.7添加了[`mysql.JSON`](dialects_mysql.html#sqlalchemy.dialects.mysql.JSON "sqlalchemy.dialects.mysql.JSON")。JSON类型提供了MySQL中的JSON值的持久性以及“getitem”和“getpath”的基本运算符支持，利用`JSON_EXTRACT`函数引用JSON结构中的各个路径。

    也可以看看

    [MySQL JSON Support](migration_11.html#change-3547)

    [¶](#change-1f91faadfeca6a6deca2362e7f770a4c)

    参考文献：[＃3547](http://www.sqlalchemy.org/trac/ticket/3547)

-   **[mysql] [change]**The MySQL dialect no longer generates an extra
    “KEY” directive when generating CREATE TABLE DDL for a table using
    InnoDB with a composite primary key with AUTO\_INCREMENT on a column
    that isn’t the first column; to overcome InnoDB’s limitation here,
    the PRIMARY KEY constraint is now generated with the AUTO\_INCREMENT
    column placed first in the list of columns.

    也可以看看

    [No more generation of an implicit KEY for composite primary key w/
    AUTO\_INCREMENT](migration_11.html#change-mysql-3216)的组合主键生成隐式KEY

    [The .autoincrement directive is no longer implicitly enabled for a
    composite primary key column](migration_11.html#change-3216)

    [¶](#change-d2790f0772bca4a21e0a612e8157501c)

    参考文献：[＃3216](http://www.sqlalchemy.org/trac/ticket/3216)

### 源码[¶ T0\>](#change-1.1.0b1-sqlite "Permalink to this headline")

-   **[sqlite] [feature]**现在，SQLite方言反映了ON UPDATE和ON
    DELETE短语在外键约束内。请求礼貌Michal
    Petrucha。[¶](#change-4b6e53e3c72102adbc3539e8d0687737)

    参考文献：[请求github：244](https://github.com/zzzeek/sqlalchemy/pull/244)

-   **[sqlite] [feature]**
    SQLite方言现在反映了主键约束的名称。拉请求戴安娜克拉克礼貌。

    也可以看看

    [Reflection of the name of PRIMARY KEY
    constraints](migration_11.html#change-3629)

    [¶](#change-49d30a6da6539d0de1fe5e50170ffa98)

    参考文献：[＃3629](http://www.sqlalchemy.org/trac/ticket/3629)

-   **[sqlite] [bug]**The workaround for right-nested joins on SQLite,
    where they are rewritten as subqueries in order to work around
    SQLite’s lack of support for this syntax, is lifted when SQLite
    version 3.7.16 or greater is detected.

    也可以看看

    [Right-nested join workaround lifted for SQLite version
    3.7.16](migration_11.html#change-3634)

    [¶](#change-ff629759d993d58e82fc77a32e11282f)

    参考文献：[＃3634](http://www.sqlalchemy.org/trac/ticket/3634)

-   **[sqlite] [bug]**The workaround for SQLite’s unexpected delivery of
    column names as `tablename.columnname` for some
    kinds of queries is now disabled when SQLite version 3.10.0 or
    greater is detected.

    也可以看看

    [Dotted column names workaround lifted for SQLite version
    3.10.0](migration_11.html#change-3633)

    [¶](#change-63298ba6c855aa8516743d99d0319ba1)

    参考文献：[＃3633](http://www.sqlalchemy.org/trac/ticket/3633)

-   **[sqlite]
    [change]**增加了对用于SQLite的[`Inspector.get_schema_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_schema_names "sqlalchemy.engine.reflection.Inspector.get_schema_names")方法的SQLite方言的支持；拉请求礼貌Brian
    Van
    Klaveren。还修复了对使用模式创建索引的支持以及模式绑定表中对外键约束的反映。

    也可以看看

    [Improved Support for Remote
    Schemas](migration_11.html#change-sqlite-schemas)

    [¶](#change-b5448aba0a3a84361c2f1ee75c597bfa)

    参考文献：[pull request
    github：198](https://github.com/zzzeek/sqlalchemy/pull/198)

### MSSQL [¶ T0\>](#change-1.1.0b1-mssql "Permalink to this headline")

-   **[mssql] [feature]**The `mssql_clustered` flag
    available on [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint"),
    [`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint"),
    [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    now defaults to `None`, and can be set to False
    which will render the NONCLUSTERED keyword in particular for a
    primary key, allowing a different index to be used as “clustered”.
    请求礼貌SauliusŽemaitaitis。[¶](#change-be8b6149c59334d05c96e5207d84cfa2)

-   **[mssql] [feature]**通过[`create_engine.isolation_level`](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")和[`Connection.execution_options.isolation_level`](core_connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")参数为SQL
    Server方言添加了基本的隔离级别支持。

    也可以看看

    [Added transaction isolation level support for SQL
    Server](migration_11.html#change-3534)

    [¶](#change-83bc6226d745f264990c3f697a8bec64)

    参考文献：[＃3534](http://www.sqlalchemy.org/trac/ticket/3534)

-   **[mssql] [bug]**根据`VARBINARY`数据类型适当调整mxODBC方言以使用`BinaryNull`符号。拉拉请求礼貌艾伦。[¶](#change-b04c14877b76f5d17f0cd07b715c468a)

    参考文献：[pull request
    bitbucket：58](https://bitbucket.org/zzzeek/sqlalchemy/pull-request/58)

-   修复了SQL Server方言通过将令牌`"max"`分配给具有无限长度的字符串长度或其他可变长度列类型来解决问题的问题。**[mssql]
    [bug]**字符串的长度属性。虽然显式使用`"max"`标记受SQL
    Server方言支持，但它不是基本字符串类型的常规协定的一部分，而是应将其长度保留为None。现在该方言将该长度指定为无，以反映该类型，以便该类型在其他上下文中正常运行。

    也可以看看

    [String / varlength types no longer represent “max” explicitly on
    reflection](migration_11.html#change-3504)

    [¶](#change-2101980fac60807a3d347737bfff6a29)

    参考文献：[＃3504](http://www.sqlalchemy.org/trac/ticket/3504)

-   **[mssql] [change]**The `legacy_schema_aliasing`
    flag, introduced in version 1.0.5 as part of
    [\#3424](http://www.sqlalchemy.org/trac/ticket/3424) to allow
    disabling of the MSSQL dialect’s attempts to create aliases for
    schema-qualified tables, now defaults to False; the old behavior is
    now disabled unless explicitly turned on.

    也可以看看

    [The legacy\_schema\_aliasing flag is now set to
    False](migration_11.html#change-3434)

    [¶](#change-88e689d9f43877db618ab1091101ab1a)

    参考文献：[＃3434](http://www.sqlalchemy.org/trac/ticket/3434)

### 杂项[¶ T0\>](#change-1.1.0b1-misc "Permalink to this headline")

-   **[feature] [ext]**将[`MutableSet`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableSet "sqlalchemy.ext.mutable.MutableSet")和[`MutableList`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableList "sqlalchemy.ext.mutable.MutableList")辅助类添加到[Mutation
    Tracking](orm_extensions_mutable.html)扩展中。请求Jeong
    YunWon提供。[¶](#change-d682fc46bfa49ace6fb8b8b9f4b09a5e)

    参考文献：[＃3297](http://www.sqlalchemy.org/trac/ticket/3297)

-   **[bug] [ext]**The docstring specified on a hybrid property or
    method is now honored at the class level, allowing it to work with
    tools like Sphinx autodoc.
    这里的机制必然涉及混合属性的表达式的一些包装，这可能导致它们使用内省而出现不同。

    也可以看看

    [Hybrid properties and methods now propagate the docstring as well
    as .info](migration_11.html#change-3653)

    [¶](#change-a2c32a48b7c0700784bb0b7a87dd1f3f)

    参考文献：[＃3653](http://www.sqlalchemy.org/trac/ticket/3653)

-   **[bug]
    [sybase]**尝试编译包含“offset”的查询时，不支持的Sybase方言现在引发`NotImplementedError`；
    Sybase没有直接的“偏移”功能。[¶](#change-44d4eaf2aee417980d71eddb977888cb)

    参考文献：[＃2278](http://www.sqlalchemy.org/trac/ticket/2278)


