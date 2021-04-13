---
title: 类映射 API
date: 2021-02-20 22:41:45
permalink: /sqlalchemy/orm/mapping_api/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
类映射 API [¶](#class-mapping-api "Permalink to this headline")
==============================================================

 `sqlalchemy.orm.`{.descclassname}`mapper`{.descname}(*class\_*, *local\_table=None*, *properties=None*, *primary\_key=None*, *non\_primary=False*, *inherits=None*, *inherit\_condition=None*, *inherit\_foreign\_keys=None*, *extension=None*, *order\_by=False*, *always\_refresh=False*, *version\_id\_col=None*, *version\_id\_generator=None*, *polymorphic\_on=None*, *\_polymorphic\_map=None*, *polymorphic\_identity=None*, *concrete=False*, *with\_polymorphic=None*, *allow\_partial\_pks=True*, *batch=True*, *column\_prefix=None*, *include\_properties=None*, *exclude\_properties=None*, *passive\_updates=True*, *passive\_deletes=False*, *confirm\_deleted\_rows=True*, *eager\_defaults=False*, *legacy\_is\_orphan=False*, *\_compiled\_cache\_size=100*)[¶](#sqlalchemy.orm.mapper "Permalink to this definition")
:   返回一个新的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象。

    该功能通常通过声明扩展在幕后使用。当使用Declarative时，许多通常的[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")参数由Declarative扩展本身处理，包括`class_`，`local_table`，`properties`，`inherits`。其他选项使用`__mapper_args__`类变量传递给[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")：plainplain

        class MyClass(Base):
            __tablename__ = 'my_table'
            id = Column(Integer, primary_key=True)
            type = Column(String(50))
            alt = Column("some_alt", Integer)

            __mapper_args__ = {
                'polymorphic_on' : type
            }

    显式使用[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")通常被称为*经典映射*。上面的声明性示例在经典形式上等同于：

        my_table = Table("my_table", metadata,
            Column('id', Integer, primary_key=True),
            Column('type', String(50)),
            Column("some_alt", Integer)
        )

        class MyClass(object):
            pass

        mapper(MyClass, my_table,
            polymorphic_on=my_table.c.type,
            properties={
                'alt':my_table.c.some_alt
            })

    也可以看看

    [Classical Mappings](mapping_styles.html#classical-mapping) -
    讨论直接使用[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")

    参数：

    -   **class \_** [¶](#sqlalchemy.orm.mapper.params.class_) -
        要映射的类。当使用Declarative时，这个参数会自动作为声明的类本身传递。
    -   **local\_table**[¶](#sqlalchemy.orm.mapper.params.local_table) –
        The [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        or other selectable to which the class is mapped.
        如果此映射器使用单表继承从另一个映射器继承，则可能为`None`。When using Declarative, this argument is
        automatically passed by the extension, based on what is
        configured via the `__table__` argument or
        via the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        produced as a result of the `__tablename__`
        and [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        arguments present.
    -   **always\_refresh**[¶](#sqlalchemy.orm.mapper.params.always_refresh)
        – If True, all query operations for this mapped class will
        overwrite all data within object instances that already exist
        within the session, erasing any in-memory changes with whatever
        information was loaded from the database.
        高度不鼓励使用这个标志；作为替代方法，请参阅方法[`Query.populate_existing()`](query.html#sqlalchemy.orm.query.Query.populate_existing "sqlalchemy.orm.query.Query.populate_existing")。
    -   **allow\_partial\_pks**
        [¶](#sqlalchemy.orm.mapper.params.allow_partial_pks) -
        默认为True。指示具有一些NULL值的组合主键应被视为可能存在于数据库中。This
        affects whether a mapper will assign an incoming row to an
        existing identity, as well as if [`Session.merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
        will check the database first for a particular primary key
        value. 例如，如果已映射到​​OUTER JOIN，则可能发生“部分主键”。
    -   **batch**[¶](#sqlalchemy.orm.mapper.params.batch) – Defaults to
        `True`, indicating that save operations of
        multiple entities can be batched together for efficiency.
        设置为False表示在保存下一个实例之前，实例将完全保存。这是极少数情况下使用的，即[`MapperEvents`](events.html#sqlalchemy.orm.events.MapperEvents "sqlalchemy.orm.events.MapperEvents")侦听器需要在各个行持久性操作之间调用。
    -   **column\_prefix**
        [¶](#sqlalchemy.orm.mapper.params.column_prefix) -

        当[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象被自动指定为映射类的属性时，该字符串将被映射到映射属性名称的前面。不会影响显式指定的基于列的属性。

        示例中的[Naming All Columns with a
        Prefix](mapping_columns.html#column-prefix)部分。

    -   **具体** [¶](#sqlalchemy.orm.mapper.params.concrete) -

        如果为True，则表示此映射器应该使用其父映射器的具体表继承。

        例如，请参阅[Concrete Table
        Inheritance](inheritance.html#concrete-inheritance)部分。

    -   **confirm\_deleted\_rows**
        [¶](#sqlalchemy.orm.mapper.params.confirm_deleted_rows) -

        默认为True；当基于特定主键的DELETE出现多一行时，如果匹配的行数不等于期望的行数，则会发出警告。可以将此参数设置为False来处理数据库ON
        DELETE
        CASCADE规则可能会自动删除其中某些行的情况。警告可能会更改为未来版本中的例外情况。

        版本0.9.4中的新增功能： -
        添加了[`mapper.confirm_deleted_rows`](#sqlalchemy.orm.mapper.params.confirm_deleted_rows "sqlalchemy.orm.mapper")以及条件匹配的行删除检查。

    -   **eager\_defaults**
        [¶](#sqlalchemy.orm.mapper.params.eager_defaults) -

        如果为True，ORM将在INSERT或UPDATE后立即获取服务器生成的默认值的值，而不是在下次访问时将它们保留为过期值。这可以用于在flush完成之前立即需要服务器生成的值的事件方案。默认情况下，该方案将在插入或更新的每行中发出单独的`SELECT`语句，该注释可能会增加显着的性能开销。但是，如果目标数据库支持[RETURNING](glossary.html#term-returning)，则默认值将以INSERT或UPDATE语句内联返回，这可以极大地提高需要频繁访问刚刚生成的服务器默认值的应用程序的性能。

        在版本0.9.0中更改： `eager_defaults`选项现在可以使用[RETURNING](glossary.html#term-returning)作为支持它的后端。

    -   **exclude\_properties**
        [¶](#sqlalchemy.orm.mapper.params.exclude_properties) -

        要从映射中排除的列表或一组字符串列名称。

        例如，请参阅[Mapping a Subset of Table
        Columns](mapping_columns.html#include-exclude-cols)。

    -   **extension**[¶](#sqlalchemy.orm.mapper.params.extension) – A
        [`MapperExtension`](deprecated.html#sqlalchemy.orm.interfaces.MapperExtension "sqlalchemy.orm.interfaces.MapperExtension")
        instance or list of [`MapperExtension`](deprecated.html#sqlalchemy.orm.interfaces.MapperExtension "sqlalchemy.orm.interfaces.MapperExtension")
        instances which will be applied to all operations by this
        [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper").
        **已过时。 T0\>**请参阅[`MapperEvents`](events.html#sqlalchemy.orm.events.MapperEvents "sqlalchemy.orm.events.MapperEvents")。
    -   **include\_properties**
        [¶](#sqlalchemy.orm.mapper.params.include_properties) -

        一个包含列表或一组要包含的字符串列名。

        例如，请参阅[Mapping a Subset of Table
        Columns](mapping_columns.html#include-exclude-cols)。

    -   **继承** [¶](#sqlalchemy.orm.mapper.params.inherits) -

        一个映射类或相应的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，表示该[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")应该*继承*的超类。这里映射的类必须是其他映射器类的子类。当使用Declarative时，由于声明的类的自然类层次结构而自动传递此参数。

        也可以看看

        [Mapping Class Inheritance Hierarchies](inheritance.html)

    -   **inherit\_condition**[¶](#sqlalchemy.orm.mapper.params.inherit_condition)
        – For joined table inheritance, a SQL expression which will
        define how the two tables are joined; defaults to a natural join
        between the two tables.
    -   **inherit\_foreign\_keys**[¶](#sqlalchemy.orm.mapper.params.inherit_foreign_keys)
        – When `inherit_condition` is used and the
        columns present are missing a [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
        configuration, this parameter can be used to specify which
        columns are “foreign”.
        在大多数情况下，可以保留为`None`。
    -   **legacy\_is\_orphan**
        [¶](#sqlalchemy.orm.mapper.params.legacy_is_orphan) -

        布尔值，默认为`False`。当`True`时，指定将“遗留”孤儿考虑应用于由此映射器映射的对象，这意味着挂起（即非持久）对象从拥有[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，只有当它从*全部*父母指定一个`delete-orphan`级联到此映射器时，才会关联。新的默认行为是，当该对象与指定`delete-orphan`级联的*其父母的任何*关联时，该对象会自动清除。这种行为与持久化对象的行为更加一致，并且允许行为在更多场景中保持一致，而与是否已经刷新了可签发对象无关。

        请参阅[The consideration of a “pending” object as an “orphan”
        has been made more
        aggressive](changelog_migration_08.html#legacy-is-orphan-addition)。

        0.8版新增功能： -
        将待处理对象视为“孤立对象”的修改已被修改为与持久对象的行为更加接近，即对象从[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，只要它从任何孤立启用的父母中解除关联。以前，挂起的对象只有在与所有孤立启用的父母关联时才会被清除。新标志`legacy_is_orphan`被添加到[`orm.mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")中，以重新建立传统行为。

    -   **non\_primary** [¶](#sqlalchemy.orm.mapper.params.non_primary)
        -

        指定该[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")是“主”映射程序的补充，即用于持久化的映射程序。这里创建的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")可用于类的临时映射到备选可选项，仅用于加载。

        [`Mapper.non_primary`](#sqlalchemy.orm.mapper.Mapper.params.non_primary "sqlalchemy.orm.mapper.Mapper")不是一个经常使用的选项，但在某些特定的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")情况下很有用。

        也可以看看

        [Relationship to Non Primary
        Mapper](join_conditions.html#relationship-non-primary-mapper)

    -   **order\_by** [¶](#sqlalchemy.orm.mapper.params.order_by) -

        一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象列表，选择操作应将其用作实体的默认排序。默认情况下，映射器没有预定义的顺序。

        从版本1.1开始弃用：不推荐使用[`Mapper.order_by`](#sqlalchemy.orm.mapper.Mapper.params.order_by "sqlalchemy.orm.mapper.Mapper")参数。使用[`Query.order_by()`](query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")确定结果集的排序。

    -   **passive\_deletes**
        [¶](#sqlalchemy.orm.mapper.params.passive_deletes) -

        指示删除连接表继承实体时，外键列的DELETE行为。对于基本映射器，默认为`False`；对于继承映射器，默认为`False`，除非超类映射器上的值设置为`True`。

        当`True`时，假定ON DELETE
        CASCADE配置在将此映射器表与其超类表关联的外键关系上，以便当工作单元试图删除实体时，它只需要为超类表发出DELETE语句，而不是此表。

        当`False`时，会为此映射器的表单独发出DELETE语句。如果这个表的本地主键属性被卸载，那么必须发出一个SELECT来验证这些属性；请注意，连接表子类的主键列不是整个对象的“主键”的一部分。

        请注意，`True`的值始终是**强制到子类映射器上；也就是说，超类无法指定passive\_deletes，而这对所有子类映射器都不起作用。**

        版本1.1中的新功能

        也可以看看

        [Using Passive Deletes](collections.html#passive-deletes) -
        与[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")一起使用的相似功能的描述

        [`mapper.passive_updates`](#sqlalchemy.orm.mapper.params.passive_updates "sqlalchemy.orm.mapper")
        - 支持连接表继承映射器的ON UPDATE CASCADE

    -   **passive\_updates**
        [¶](#sqlalchemy.orm.mapper.params.passive_updates) -

        指示主键列在连接表继承映射上发生更改时外键列的UPDATE行为。默认为`True`。

        如果为True，则假定在数据库的外键上配置了ON UPDATE
        CASCADE，并且数据库将处理UPDATE从源列传播到连接表行上的从属列。

        如果为False，则假定数据库不强制执行参照完整性，并且不会为更新发布自己的CASCADE操作。工作单元过程将在主键更改期间为从属列发出UPDATE语句。

        也可以看看

        [Mutable Primary Keys / Update
        Cascades](relationship_persistence.html#passive-updates) -
        与[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")一起使用的相似特征的描述

        [`mapper.passive_deletes`](#sqlalchemy.orm.mapper.params.passive_deletes "sqlalchemy.orm.mapper")
        - 为连接表继承映射器支持ON DELETE CASCADE

    -   **polymorphic\_on**
        [¶](#sqlalchemy.orm.mapper.params.polymorphic_on) -

        当存在继承类时，指定用于确定传入行的目标类的列，属性或SQL表达式。

        该值通常是存在于映射的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象：

            class Employee(Base):
                __tablename__ = 'employee'

                id = Column(Integer, primary_key=True)
                discriminator = Column(String(50))

                __mapper_args__ = {
                    "polymorphic_on":discriminator,
                    "polymorphic_identity":"employee"
                }

        它也可以被指定为一个SQL表达式，就像在这个例子中我们使用[`case()`](core_sqlelement.html#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")结构来提供一个条件方法：

            class Employee(Base):
                __tablename__ = 'employee'

                id = Column(Integer, primary_key=True)
                discriminator = Column(String(50))

                __mapper_args__ = {
                    "polymorphic_on":case([
                        (discriminator == "EN", "engineer"),
                        (discriminator == "MA", "manager"),
                    ], else_="employee"),
                    "polymorphic_identity":"employee"
                }

        它也可以引用用[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")配置的任何属性，或者指向一个字符串名称的属性：

            class Employee(Base):
                __tablename__ = 'employee'

                id = Column(Integer, primary_key=True)
                discriminator = Column(String(50))
                employee_type = column_property(
                    case([
                        (discriminator == "EN", "engineer"),
                        (discriminator == "MA", "manager"),
                    ], else_="employee")
                )

                __mapper_args__ = {
                    "polymorphic_on":employee_type,
                    "polymorphic_identity":"employee"
                }

        在版本0.7.4中进行了更改： `polymorphic_on`可以指定为SQL表达式，或者参考使用[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")配置的任何属性，一个字符串的名称。

        当设置`polymorphic_on`引用本地映射的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中不存在的属性或表达式时，鉴别器的值应该持久保存到数据库中，鉴别器的值不会自动设置在新实例上；这必须由用户通过手动方式或通过事件监听器来处理。建立这样一个听众的典型方法如下所示：

            from sqlalchemy import event
            from sqlalchemy.orm import object_mapper

            @event.listens_for(Employee, "init", propagate=True)
            def set_identity(instance, *arg, **kw):
                mapper = object_mapper(instance)
                instance.discriminator = mapper.polymorphic_identity

        如上所述，我们将映射类的`polymorphic_identity`的值赋给`discriminator`属性，从而将值保存到数据库中的`discriminator`列。

        警告

        目前，**只能设置一个鉴别器列**，通常位于层次结构中最底层的类。“级联”多态列还不被支持。

        也可以看看

        [Mapping Class Inheritance Hierarchies](inheritance.html)

    -   **polymorphic\_identity**[¶](#sqlalchemy.orm.mapper.params.polymorphic_identity)
        – Specifies the value which identifies this particular class as
        returned by the column expression referred to by the
        `polymorphic_on` setting.
        在接收到行时，将与`polymorphic_on`列表达式相对应的值与此值进行比较，指示哪个子类应该用于新重建的对象。
    -   **properties**[¶](#sqlalchemy.orm.mapper.params.properties) – A
        dictionary mapping the string names of object attributes to
        [`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")
        instances, which define the persistence behavior of that
        attribute. 请注意，映射后的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中存在的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象会自动放入`ColumnProperty`实例中，除非被覆盖。当使用Declarative时，基于所声明的类体中声明的所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")实例自动传递此参数。
    -   **primary\_key**[¶](#sqlalchemy.orm.mapper.params.primary_key) –
        A list of [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects which define the primary key to be used against this
        mapper’s selectable unit. 这通常只是`local_table`的主键，但可以在此处重写。
    -   **version\_id\_col**
        [¶](#sqlalchemy.orm.mapper.params.version_id_col) -

        一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")，用于保留表中行的正在运行的版本标识。这用于检测并发更新或在刷新中存在陈旧数据。该方法是检测UPDATE语句是否与最后一个已知版本ID不匹配，引发[`StaleDataError`](exceptions.html#sqlalchemy.orm.exc.StaleDataError "sqlalchemy.orm.exc.StaleDataError")异常。默认情况下，除非`version_id_generator`指定了替代版本生成器，否则该列必须为[`Integer`](core_type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")类型。

        也可以看看

        [Configuring a Version
        Counter](versioning.html#mapper-version-counter) -
        讨论版本计数和基本原理。

    -   **version\_id\_generator**
        [¶](#sqlalchemy.orm.mapper.params.version_id_generator) -

        定义应该如何生成新版本的ID。默认为`None`，这表示使用简单的整数计数方案。要提供自定义版本控制方案，请提供表单的可调用函数：

            def generate_version(version):
                return next_version

        另外，通过指定值`False`，可以使用服务器端版本控制功能，例如触发器或版本ID生成器以外的程序版本控制方案。使用此选项时，请参阅[Server
        Side Version
        Counters](versioning.html#server-side-version-counter)以了解重要的一点。

        版本0.9.0新增： `version_id_generator`支持服务器端版本号的生成。

        也可以看看

        [Custom Version Counters /
        Types](versioning.html#custom-version-counter)

        [Server Side Version
        Counters](versioning.html#server-side-version-counter)

    -   **with\_polymorphic**
        [¶](#sqlalchemy.orm.mapper.params.with_polymorphic) -

        指示“多态”加载的默认样式的`（＆lt； classes＆gt；， ＆lt； selectable＆gt；）`形式的元组，哪些表一次被查询。是映射器和/或类的任何单个或列表，指示应该一次加载的继承类。
        T0\>特殊值`'*'`可用于指示所有降序类应立即加载。第二个元组参数表示将用于查询多个类的可选项。

        也可以看看

        [Basic Control of Which Tables are
        Queried](inheritance.html#with-polymorphic) - 讨论多态查询技术。

`sqlalchemy.orm。 T0>  object_mapper  T1> （ T2> 实例 T3> ） T4> ¶ T5 >`{.descclassname}
:   给定一个对象，返回与对象实例关联的主映射器。

    如果未配置映射，则引发[`sqlalchemy.orm.exc.UnmappedInstanceError`](exceptions.html#sqlalchemy.orm.exc.UnmappedInstanceError "sqlalchemy.orm.exc.UnmappedInstanceError")。plainplain

    该功能可通过检查系统获得：

        inspect(instance).mapper

    如果实例不是映射的一部分，则使用检查系统将引发[`sqlalchemy.exc.NoInspectionAvailable`](core_exceptions.html#sqlalchemy.exc.NoInspectionAvailable "sqlalchemy.exc.NoInspectionAvailable")。

 `sqlalchemy.orm.`{.descclassname}`class_mapper`{.descname}(*class\_*, *configure=True*)[¶](#sqlalchemy.orm.class_mapper "Permalink to this definition")
:   给定一个类，返回与密钥关联的主要[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。

    如果给定类没有配置映射，则引发[`UnmappedClassError`](exceptions.html#sqlalchemy.orm.exc.UnmappedClassError "sqlalchemy.orm.exc.UnmappedClassError")；如果传递了非类对象，则引发[`ArgumentError`](core_exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。plainplainplainplain

    等效功能可通过[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数使用：

        inspect(some_mapped_class)

    如果该类未映射，则使用检查系统将引发[`sqlalchemy.exc.NoInspectionAvailable`](core_exceptions.html#sqlalchemy.exc.NoInspectionAvailable "sqlalchemy.exc.NoInspectionAvailable")。

`sqlalchemy.orm。 T0>  configure_mappers  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   初始化到目前为止已经构建的所有映射器的映射器间关系。

    这个函数可以调用任意次数，但在大多数情况下会自动调用，使用第一次映射，以及每当使用映射和额外尚未配置的映射器已经构建。plainplainplain

    出现这种情况的要点包括何时将映射类实例化为实例，以及何时使用[`Session.query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")方法。

    [`configure_mappers()`](#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")函数提供了几个可用于扩充其功能的事件挂钩。这些方法包括：

    -   [`MapperEvents.before_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")
        - called once before [`configure_mappers()`](#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
        does any work; this can be used to establish additional options,
        properties, or related mappings before the operation proceeds.
    -   [`MapperEvents.mapper_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")
        - called as each indivudal [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
        is configured within the process; will include all mapper state
        except for backrefs set up by other mappers that are still to be
        configured.
    -   [`MapperEvents.after_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")
        - called once after [`configure_mappers()`](#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
        is complete; at this stage, all [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
        objects that are known to SQLAlchemy will be fully configured.
        请注意，调用应用程序可能还有其他尚未生成的映射，例如，如果它们尚处于未导入模块中。

`sqlalchemy.orm。 T0>  clear_mappers  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   从所有类中移除所有映射器。

    这个函数从类中移除所有的工具并处理它们相关的映射器。一旦被调用，这些类就会被取消映射，并可以在以后用新的映射器重新映射。plainplainplainplainplainplain

    [`clear_mappers()`](#sqlalchemy.orm.clear_mappers "sqlalchemy.orm.clear_mappers")
    is *not* for normal use, as there is literally no valid usage for it
    outside of very specific testing scenarios.
    通常，映射器是用户定义类的永久性结构组件，并且不会独立于类而丢弃它。如果一个映射类本身被垃圾收集，它的映射器也会自动处理。因此，[`clear_mappers()`](#sqlalchemy.orm.clear_mappers "sqlalchemy.orm.clear_mappers")仅用于测试套件中，该测试套件将重复使用具有不同映射的相同类，这本身就是极其罕见的用例
    -
    唯一的这种用例实际上是SQLAlchemy自己的测试套件以及可能的其他ORM扩展库的测试套件，这些扩展库打算根据固定的一组类来测试映射器构造的各种组合。

 `sqlalchemy.orm.util.`{.descclassname}`identity_key`{.descname}(*\*args*, *\*\*kwargs*)[¶](#sqlalchemy.orm.util.identity_key "Permalink to this definition")
:   生成“身份密钥”元组，就像在[`Session.identity_map`](session_api.html#sqlalchemy.orm.session.Session.identity_map "sqlalchemy.orm.session.Session.identity_map")字典中用作键一样。

    这个函数有几种调用方式：

    -   `identity_key（class， ident）`

        该表单接收映射类和主键标量或元组作为参数。

        例如。：

            >>> identity_key(MyClass, (1, 2))
            (<class '__main__.MyClass'>, (1, 2))

        参数类：

        映射类（必须是位置参数）

        参数标识：

        主键，可能是标量或元组参数。

    -   `identity_key(instance=instance)`

        此表单将为给定实例生成身份密钥。该实例不必是持久性的，只需要填充其主键属性（否则对于那些缺失值，键将包含`None`）。

        例如。：

            >>> instance = MyClass(1, 2)
            >>> identity_key(instance=instance)
            (<class '__main__.MyClass'>, (1, 2))

        在这种形式下，给定实例最终通过[`Mapper.identity_key_from_instance()`](#sqlalchemy.orm.mapper.Mapper.identity_key_from_instance "sqlalchemy.orm.mapper.Mapper.identity_key_from_instance")运行，如果对象已过期，将会对相应的行执行数据库检查。

        参数实例：

        对象实例（必须作为关键字arg提供）

    -   `identity_key（class， row = row）`

        除了将一个数据库结果行作为[`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")对象传递外，此表单与类/元组表单类似。

        例如。：

            >>> row = engine.execute("select * from table where a=1 and b=2").first()
            >>> identity_key(MyClass, row=row)
            (<class '__main__.MyClass'>, (1, 2))

        参数类：

        映射类（必须是位置参数）

        参数行：

        [`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")
        row returned by a [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
        (must be given as a keyword arg)

 `sqlalchemy.orm.util.`{.descclassname}`polymorphic_union`{.descname}(*table\_map*, *typecolname*, *aliasname='p\_union'*, *cast\_nulls=True*)[¶](#sqlalchemy.orm.util.polymorphic_union "Permalink to this definition")
:   创建一个由多态映射器使用的`UNION`语句。

    有关如何使用它的示例，请参阅[Concrete Tableplainplainplainplainplain
    Inheritance](inheritance.html#concrete-inheritance)。

    参数：

    -   **table\_map**[¶](#sqlalchemy.orm.util.polymorphic_union.params.table_map)
        – mapping of polymorphic identities to [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        objects.
    -   **typecolname**[¶](#sqlalchemy.orm.util.polymorphic_union.params.typecolname)
        – string name of a “discriminator” column, which will be derived
        from the query, producing the polymorphic identity for each row.
        如果`None`，则不会生成多态鉴别符。
    -   **aliasname**[¶](#sqlalchemy.orm.util.polymorphic_union.params.aliasname)
        – name of the [`alias()`](core_selectable.html#sqlalchemy.sql.expression.alias "sqlalchemy.sql.expression.alias")
        construct generated.
    -   **cast\_nulls**[¶](#sqlalchemy.orm.util.polymorphic_union.params.cast_nulls)
        – if True, non-existent columns, which are represented as
        labeled NULLs, will be passed into CAST.
        这是一个遗留问题，在Oracle的一些后端存在问题 -
        在这种情况下，它可以设置为False。

 *class*`sqlalchemy.orm.mapper.`{.descclassname}`Mapper`{.descname}(*class\_*, *local\_table=None*, *properties=None*, *primary\_key=None*, *non\_primary=False*, *inherits=None*, *inherit\_condition=None*, *inherit\_foreign\_keys=None*, *extension=None*, *order\_by=False*, *always\_refresh=False*, *version\_id\_col=None*, *version\_id\_generator=None*, *polymorphic\_on=None*, *\_polymorphic\_map=None*, *polymorphic\_identity=None*, *concrete=False*, *with\_polymorphic=None*, *allow\_partial\_pks=True*, *batch=True*, *column\_prefix=None*, *include\_properties=None*, *exclude\_properties=None*, *passive\_updates=True*, *passive\_deletes=False*, *confirm\_deleted\_rows=True*, *eager\_defaults=False*, *legacy\_is\_orphan=False*, *\_compiled\_cache\_size=100*)[¶](#sqlalchemy.orm.mapper.Mapper "Permalink to this definition")
:   基础：[`sqlalchemy.orm.base.InspectionAttr`](internals.html#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")

    定义类属性与数据库表列的关联。plainplainplainplain

    [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象使用[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数实例化。有关实例化新的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象的信息，请参阅该函数的文档。

    当[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")明确用于链接用户定义的类和表元数据时，这被称为*经典映射*。现代SQLAlchemy用法倾向于支持类配置的[`sqlalchemy.ext.declarative`](extensions_declarative_api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")扩展，这使得在后台使用[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")。

    给定一个已知由ORM映射的类，可以使用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数获取维护它的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")：

        from sqlalchemy import inspect

        mapper = inspect(MyClass)

    由[`sqlalchemy.ext.declarative`](extensions_declarative_api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")扩展名映射的类也将通过`__mapper__`属性使其映射器可用。

     `__init__`{.descname}(*class\_*, *local\_table=None*, *properties=None*, *primary\_key=None*, *non\_primary=False*, *inherits=None*, *inherit\_condition=None*, *inherit\_foreign\_keys=None*, *extension=None*, *order\_by=False*, *always\_refresh=False*, *version\_id\_col=None*, *version\_id\_generator=None*, *polymorphic\_on=None*, *\_polymorphic\_map=None*, *polymorphic\_identity=None*, *concrete=False*, *with\_polymorphic=None*, *allow\_partial\_pks=True*, *batch=True*, *column\_prefix=None*, *include\_properties=None*, *exclude\_properties=None*, *passive\_updates=True*, *passive\_deletes=False*, *confirm\_deleted\_rows=True*, *eager\_defaults=False*, *legacy\_is\_orphan=False*, *\_compiled\_cache\_size=100*)[¶](#sqlalchemy.orm.mapper.Mapper.__init__ "Permalink to this definition")
    :   构建一个新的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数描述，请参阅[`mapper()`](#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")。

    ` add_properties  T0> （ T1>  dict_of_properties  T2> ） T3> ¶ T4>`{.descname}
    :   使用add\_property将给定的属性字典添加到此映射器中。

     `add_property`{.descname}(*key*, *prop*)[¶](#sqlalchemy.orm.mapper.Mapper.add_property "Permalink to this definition")
    :   添加一个单独的MapperProperty到这个映射器。

        如果映射器尚未配置，只需将该属性添加到发送给构造函数的初始属性字典中即可。如果这个Mapper已经配置完毕，那么给定的MapperProperty会立即配置。

    ` all_orm_descriptors  T0> ¶ T1>`{.descname}
    :   与映射类关联的所有[`InspectionAttr`](internals.html#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")属性的名称空间。

        这些属性在所有情况下都是与映射类或其超类关联的Python
        [descriptors](glossary.html#term-descriptors)。

        该名称空间包括映射到该类的属性以及由扩展模块声明的属性。它包含从[`InspectionAttr`](internals.html#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")继承的任何Python描述符类型。这包括[`QueryableAttribute`](internals.html#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")以及扩展类型，例如[`hybrid_property`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")，[`hybrid_method`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_method "sqlalchemy.ext.hybrid.hybrid_method")和[`AssociationProxy`](extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")。

        为了区分映射属性和扩展属性，属性[`InspectionAttr.extension_type`](internals.html#sqlalchemy.orm.base.InspectionAttr.extension_type "sqlalchemy.orm.base.InspectionAttr.extension_type")将引用区分不同扩展类型的常量。

        在处理[`QueryableAttribute`](internals.html#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")时，[`QueryableAttribute.property`](internals.html#sqlalchemy.orm.attributes.QueryableAttribute.property "sqlalchemy.orm.attributes.QueryableAttribute.property")属性指向[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")属性，这是您在引用映射集合时获得的通过[`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")的属性。

        警告

        [`Mapper.all_orm_descriptors`](#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")访问器名称空间是`OrderedProperties`的一个实例。这是一个类似字典的对象，它包含少量的命名方法，如`OrderedProperties.items()`和`OrderedProperties.values()`。When accessing attributes dynamically,
        favor using the dict-access scheme, e.g.
        `mapper.all_orm_descriptors[somename]` over
        `getattr(mapper.all_orm_descriptors, somename)` to avoid name collisions.

        0.8.0版本中的新功能

        也可以看看

        [`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")

    ` ATTRS  T0> ¶ T1>`{.descname}
    :   所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象的名称空间都与此映射器关联。

        这是一个基于其关键名称提供每个属性的对象。例如，具有`User.name`属性的`User`类的映射器将提供`mapper.attrs.name`，它将是[`ColumnProperty`](internals.html#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")表示`name`列。命名空间对象也可以迭代，这会产生每个[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")。

        [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
        has several pre-filtered views of this attribute which limit the
        types of properties returned, inclding [`synonyms`](#sqlalchemy.orm.mapper.Mapper.synonyms "sqlalchemy.orm.mapper.Mapper.synonyms"),
        [`column_attrs`](#sqlalchemy.orm.mapper.Mapper.column_attrs "sqlalchemy.orm.mapper.Mapper.column_attrs"),
        [`relationships`](#sqlalchemy.orm.mapper.Mapper.relationships "sqlalchemy.orm.mapper.Mapper.relationships"),
        and [`composites`](#sqlalchemy.orm.mapper.Mapper.composites "sqlalchemy.orm.mapper.Mapper.composites").

        警告

        [`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")访问器名称空间是`OrderedProperties`的实例。这是一个类似字典的对象，它包含少量的命名方法，如`OrderedProperties.items()`和`OrderedProperties.values()`。When accessing attributes dynamically,
        favor using the dict-access scheme, e.g.
        `mapper.attrs[somename]` over
        `getattr(mapper.attrs, somename)` to avoid
        name collisions.

        也可以看看

        [`Mapper.all_orm_descriptors`](#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")

    `base_mapper`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.base_mapper "Permalink to this definition")
    :   继承链中最基本的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。

        在非继承场景中，该属性将始终是[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。在继承场景中，它引用了[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，它是继承链中所有其他[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象的父对象。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `c`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.c "Permalink to this definition")
    :   [`columns`](#sqlalchemy.orm.mapper.Mapper.columns "sqlalchemy.orm.mapper.Mapper.columns")。

     `cascade_iterator`{.descname}(*type\_*, *state*, *halt\_on=None*)[¶](#sqlalchemy.orm.mapper.Mapper.cascade_iterator "Permalink to this definition")
    :   迭代对象图中的每个元素及其映射器，以满足给定级联规则的所有关系。

        参数：

        -   **type \_**
            [¶](#sqlalchemy.orm.mapper.Mapper.cascade_iterator.params.type_)
            -

            级联规则的名称（即`"save-update"`，`"delete"`等。）。

            注意

            这里不接受`"all"`级联。对于通用对象遍历函数，请参阅[How do I walk
            all objects that are related to a given
            object?](faq_sessions.html#faq-walk-objects)。

        -   **状态**
            [¶](#sqlalchemy.orm.mapper.Mapper.cascade_iterator.params.state)
            -
            领导InstanceState。子项目将根据为该对象的映射器定义的关系进行处理。

        返回：

        该方法产生单独的对象实例。

        也可以看看

        [Cascades](cascades.html#unitofwork-cascades)

        [How do I walk all objects that are related to a given
        object?](faq_sessions.html#faq-walk-objects) -
        说明了不依赖级联而遍历所有对象的通用函数。

    `class _`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.class_ "Permalink to this definition")
    :   这个[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")映​​射的Python类。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `class_manager`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.class_manager "Permalink to this definition")
    :   [`ClassManager`](internals.html#sqlalchemy.orm.instrumentation.ClassManager "sqlalchemy.orm.instrumentation.ClassManager")，它为这个[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")维护事件侦听器和类绑定描述符。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    ` column_attrs  T0> ¶ T1>`{.descname}
    :   返回由[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")维护的所有[`ColumnProperty`](internals.html#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")属性的命名空间。

        也可以看看

        [`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")
        - 所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象的命名空间。

    `列`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.columns "Permalink to this definition")
    :   由[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")维护的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或其他标量表达式对象的集合。

        该集合的行为与任何[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的`c`属性的行为相同，区别仅在于此映射中包含的那些列存在，并且基于属性名称在映射中定义，不一定是[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")本身的`key`属性。另外，这里还存在由[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")映​​射的标量表达式。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    ` common_parent  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   如果给定的映射器与此映射器共享共同的继承父项，则返回true。

    `复合材料 T0> ¶ T1>`{.descname}
    :   返回由[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")维护的所有[`CompositeProperty`](internals.html#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty")属性的命名空间。

        也可以看看

        [`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")
        - 所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象的命名空间。

    `具体`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.concrete "Permalink to this definition")
    :   如果[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")是一个具体的继承映射器，则表示`True`。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `已配置`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.configured "Permalink to this definition")
    :   如果已经配置[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，则表示`True`。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

        也可以看看

        [`configure_mappers()`](#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")

    `实体 T0> ¶ T1>`{.descname}
    :   检查API的一部分。

        返回self.class\_。

    `get_property`{.descname} （ *key*，*\_configure\_mappers = True* ） [t5 \>](#sqlalchemy.orm.mapper.Mapper.get_property "Permalink to this definition")
    :   返回与给定键相关联的MapperProperty。

    ` get_property_by_column  T0> （ T1> 列 T2> ） T3> ¶ T4>`{.descname}
    :   给定一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，返回映射此列的[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")。

    ` identity_key_from_instance  T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   根据主键属性返回给定实例的身份关键字。

        如果实例的状态已过期，则调用此方法将导致数据库检查以查看该对象是否已被删除。如果该行不再存在，则引发[`ObjectDeletedError`](exceptions.html#sqlalchemy.orm.exc.ObjectDeletedError "sqlalchemy.orm.exc.ObjectDeletedError")。

        该值通常也可以在属性名称键下的实例状态中找到。

    ` identity_key_from_primary_key  T0> （ T1>  primary_key  T2> ） T3> ¶ T4>`{.descname}
    :   返回身份地图密钥以用于存储/检索身份地图中的项目。

        参数：

        **primary\_key**
        [¶](#sqlalchemy.orm.mapper.Mapper.identity_key_from_primary_key.params.primary_key)
        - 指示标识符的值列表。

    `identity_key_from_row`{.descname} （ *row*，*adapter = None* ） [t5 \>](#sqlalchemy.orm.mapper.Mapper.identity_key_from_row "Permalink to this definition")
    :   返回身份地图密钥，用于从身份地图中存储/检索项目。

        参数：

        **row**[¶](#sqlalchemy.orm.mapper.Mapper.identity_key_from_row.params.row)
        – A [`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")
        instance. The columns which are mapped by this [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
        should be locatable in the row, preferably via the
        [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        object directly (as is the case when a [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        construct is executed), or via string names of the form
        `<tablename>_<colname>`.

    `继承`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.inherits "Permalink to this definition")
    :   引用这个[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")继承的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，如果有的话。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `is_mapper`{.descname} *= True* [¶](#sqlalchemy.orm.mapper.Mapper.is_mapper "Permalink to this definition")
    :   检查API的一部分。

    `赛 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   如果此映射器从给定的映射器继承，则返回True。

    ` iterate_properties  T0> ¶ T1>`{.descname}
    :   返回所有MapperProperty对象的迭代器。

    `local_table`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.local_table "Permalink to this definition")
    :   这个[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")管理的[`Selectable`](core_selectable.html#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")。

        通常是[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或[`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")的实例。也可以是`None`。

        “本地”表是[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")直接负责从属性访问和刷新角度管理的可选项。对于非继承映射器，本地表与“映射”表相同。对于连接表继承映射器，local\_table将是这个[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")所代表的整体“连接”的特定子表。如果这个映射器是一个单表继承映射器，local\_table将是`None`。

        也可以看看

        [`mapped_table`](#sqlalchemy.orm.mapper.Mapper.mapped_table "sqlalchemy.orm.mapper.Mapper.mapped_table")

    `mapped_table`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.mapped_table "Permalink to this definition")
    :   [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")映射到的[`Selectable`](core_selectable.html#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")。

        通常是[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")或[`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")的实例。

        “映射”表是映射器在查询期间选择的可选项。对于非继承映射器，映射表与“本地”表相同。对于连接表继承映射器，mapped\_table引用表示此特定子类的完整行的完整[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")。对于单表继承映射器，mapped\_table引用基表。

        也可以看看

        [`local_table`](#sqlalchemy.orm.mapper.Mapper.local_table "sqlalchemy.orm.mapper.Mapper.local_table")

    `映射器 T0> ¶ T1>`{.descname}
    :   检查API的一部分。

        返回自我。

    `non_primary`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.non_primary "Permalink to this definition")
    :   如果[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")是一个“非主要”映射器，则表示`True`。一个仅用于分隔行但不用于持久性管理的映射器。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `polymorphic_identity`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.polymorphic_identity "Permalink to this definition")
    :   表示结果行加载过程中与[`polymorphic_on`](#sqlalchemy.orm.mapper.Mapper.polymorphic_on "sqlalchemy.orm.mapper.Mapper.polymorphic_on")列匹配的标识符。

        仅用于继承，此对象可以是任何类型，与[`polymorphic_on`](#sqlalchemy.orm.mapper.Mapper.polymorphic_on "sqlalchemy.orm.mapper.Mapper.polymorphic_on")表示的列的类型相当。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    ` polymorphic_iterator  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   遍历包含该映射器和所有后代映射器的集合。

        这不仅包括立即继承的映射器，还包括它们的所有继承映射器。

        要遍历整个层次结构，请使用`mapper.base_mapper.polymorphic_iterator()`。

    `polymorphic_map`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.polymorphic_map "Permalink to this definition")
    :   在继承场景中映射到[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")实例的“多态身份”标识符的映射。

        标识符可以是任何类型，与[`polymorphic_on`](#sqlalchemy.orm.mapper.Mapper.polymorphic_on "sqlalchemy.orm.mapper.Mapper.polymorphic_on")表示的列的类型相当。

        映射器的继承链将全部引用相同的多态映射对象。该对象用于将传入结果行关联到目标映射器。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `polymorphic_on`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.polymorphic_on "Permalink to this definition")
    :   在继承方案中，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或SQL表达式被指定为该[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")的`polymorphic_on`参数。

        该属性通常是一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")实例，但也可能是一个表达式，例如从[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")派生的表达式。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `primary_key`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.primary_key "Permalink to this definition")
    :   从[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")的角度来看，一个迭代器包含[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的集合，该对象构成映射表的“主键”。

        该列表与[`mapped_table`](#sqlalchemy.orm.mapper.Mapper.mapped_table "sqlalchemy.orm.mapper.Mapper.mapped_table")中的可选列表相反。在继承映射器的情况下，某些列可能由超类映射器管理。例如，对于[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")，主键由[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")引用的所有表中的所有主键列确定。

        该列表也不一定与与基础表关联的主键列集合相同； [`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")具有`primary_key`参数，可以覆盖[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")认为的主键列。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    ` primary_key_from_instance  T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   返回给定实例的主键值列表。

        如果实例的状态已过期，则调用此方法将导致数据库检查以查看该对象是否已被删除。如果该行不再存在，则引发[`ObjectDeletedError`](exceptions.html#sqlalchemy.orm.exc.ObjectDeletedError "sqlalchemy.orm.exc.ObjectDeletedError")。

    ` primary_mapper  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回与此映射器的类关键字（类）相对应的主映射器。

    `关系 T0> ¶ T1>`{.descname}
    :   由[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")维护的所有[`RelationshipProperty`](internals.html#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")属性的命名空间。

        警告

        [`Mapper.relationships`](#sqlalchemy.orm.mapper.Mapper.relationships "sqlalchemy.orm.mapper.Mapper.relationships")存取器名称空间是`OrderedProperties`的一个实例。这是一个类似字典的对象，它包含少量的命名方法，如`OrderedProperties.items()`和`OrderedProperties.values()`。When accessing attributes dynamically,
        favor using the dict-access scheme, e.g.
        `mapper.relationships[somename]` over
        `getattr(mapper.relationships, somename)` to
        avoid name collisions.

        也可以看看

        [`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")
        - 所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象的命名空间。

    `可选 T0> ¶ T1>`{.descname}
    :   这个[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")构造的[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造默认选择。

        通常情况下，这相当于[`mapped_table`](#sqlalchemy.orm.mapper.Mapper.mapped_table "sqlalchemy.orm.mapper.Mapper.mapped_table")，除非使用`with_polymorphic`功能，在这种情况下，将返回完整的“多态”选择。

    ` self_and_descendants  T0> ¶ T1>`{.descname}
    :   包含这个映射器和所有后代映射器的集合。

        这不仅包括立即继承的映射器，还包括它们的所有继承映射器。

    `单`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.single "Permalink to this definition")
    :   如果[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")是单表继承映射器，则表示`True`。

        [`local_table`](#sqlalchemy.orm.mapper.Mapper.local_table "sqlalchemy.orm.mapper.Mapper.local_table")
        will be `None` if this flag is set.

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `同义词 T0> ¶ T1>`{.descname}
    :   返回由[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")维护的所有[`SynonymProperty`](internals.html#sqlalchemy.orm.descriptor_props.SynonymProperty "sqlalchemy.orm.descriptor_props.SynonymProperty")属性的名称空间。

        也可以看看

        [`Mapper.attrs`](#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")
        - 所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象的命名空间。

    `表格`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.tables "Permalink to this definition")
    :   一个迭代器，包含[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")所知的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的集合。

        如果映射器映射到[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")或[`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")表示[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")，则包含[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象完整的构造将在这里呈现。

        这是在映射器构建期间确定的*只读*属性。如果直接修改，行为是未定义的。

    `验证器`{.descname} *=无* [¶](#sqlalchemy.orm.mapper.Mapper.validators "Permalink to this definition")
    :   使用[`validates()`](mapped_attributes.html#sqlalchemy.orm.validates "sqlalchemy.orm.validates")装饰器修饰过的属性的不可变字典。

        该字典包含字符串属性名称作为映射到实际验证方法的键。

    ` with_polymorphic_mappers  T0> ¶ T1>`{.descname}
    :   包含在默认“多态”查询中的[`Mapper`](#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象列表。


