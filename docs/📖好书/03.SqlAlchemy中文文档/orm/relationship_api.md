---
title: relationship_api
date: 2021-02-20 22:41:45
permalink: /pages/9f27b1/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
关系API [¶](#relationships-api "Permalink to this headline")
============================================================

 `sqlalchemy.orm.`{.descclassname}`relationship`{.descname}(*argument*, *secondary=None*, *primaryjoin=None*, *secondaryjoin=None*, *foreign\_keys=None*, *uselist=None*, *order\_by=False*, *backref=None*, *back\_populates=None*, *post\_update=False*, *cascade=False*, *extension=None*, *viewonly=False*, *lazy=True*, *collection\_class=None*, *passive\_deletes=False*, *passive\_updates=True*, *remote\_side=None*, *enable\_typechecks=True*, *join\_depth=None*, *comparator\_factory=None*, *single\_parent=False*, *innerjoin=False*, *distinct\_target\_key=None*, *doc=None*, *active\_history=False*, *cascade\_backrefs=True*, *load\_on\_pending=False*, *bake\_queries=True*, *strategy\_class=None*, *\_local\_remote\_pairs=None*, *query\_class=None*, *info=None*)[¶](#sqlalchemy.orm.relationship "Permalink to this definition")
:   提供两个映射类之间的关系。

    这对应于父子关系或关联表关系。构造的类是[`RelationshipProperty`](internals.html#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")的一个实例。

    典型的[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，用于经典映射中：

        mapper(Parent, properties={
          'children': relationship(Child)
        })

    [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")接受的一些参数可选地接受一个可调用的函数，该函数在被调用时会产生所需的值。The
    callable is invoked by the parent [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
    at “mapper initialization” time, which happens only when mappers are
    first used, and is assumed to be after all mappings have been
    constructed.
    这可以用于解决声明顺序和其他依赖性问题，例如，如果`Child`在`Parent`中声明在同一个文件中：

        mapper(Parent, properties={
            "children":relationship(lambda: Child,
                                order_by=lambda: Child.id)
        })

    当使用[Declarative](extensions_declarative_index.html)扩展名时，Declarative初始化程序允许将字符串参数传递给[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")。这些字符串参数被转换为可以将字符串评估为Python代码的可调参数，使用Declarative类注册表作为命名空间。这允许相关类的查找通过它们的字符串名称自动进行，并且无需将相关类根本导入到本地模块空间中：

        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()

        class Parent(Base):
            __tablename__ = 'parent'
            id = Column(Integer, primary_key=True)
            children = relationship("Child", order_by="Child.id")

    也可以看看

    [Relationship Configuration](relationships.html) -
    [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的完整介绍性和参考文档。

    [Building a Relationship](tutorial.html#orm-tutorial-relationship) -
    ORM教程介绍。

    参数：

    -   **参数** [¶](#sqlalchemy.orm.relationship.params.argument) -

        映射类或实际的[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")实例，表示关系的目标。

        [`argument`](#sqlalchemy.orm.relationship.params.argument "sqlalchemy.orm.relationship")也可以作为可调用函数传递，它在映射器初始化时计算，并且在使用Declarative时可以作为Python可评估的字符串传递。

        也可以看看

        [Configuring
        Relationships](extensions_declarative_relationships.html#declarative-configuring-relationships)
        - 使用Declarative时关系配置的更多细节。

    -   **辅助** [¶](#sqlalchemy.orm.relationship.params.secondary) -

        对于多对多关系，指定中间表，并且通常是[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的实例。在不常见的情况下，参数也可以被指定为[`Alias`](core_selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")结构，甚至可以指定为[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")结构。

        [`secondary`](#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")也可以作为可映射函数在映射器初始化时进行评估。When
        using Declarative, it may also be a string argument noting the
        name of a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is present in the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        collection associated with the parent-mapped [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").

        The [`secondary`](#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")
        keyword argument is typically applied in the case where the
        intermediary [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        is not otherwise expressed in any direct class mapping.
        如果“辅助”表也被明确地映射到其他地方（例如在[Association
        Object](basic_relationships.html#association-pattern)中），应该考虑应用[`viewonly`](#sqlalchemy.orm.relationship.params.viewonly "sqlalchemy.orm.relationship")标志，以便[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")

        也可以看看

        [Many To
        Many](basic_relationships.html#relationships-many-to-many) -
        “多对多”的参考例子。

        [Building a Many To Many
        Relationship](tutorial.html#orm-tutorial-many-to-many) -
        ORM教程介绍多对多关系。

        [Self-Referential Many-to-Many
        Relationship](join_conditions.html#self-referential-many-to-many)
        - 在自引用情况下使用多对多的细节。

        [Configuring Many-to-Many
        Relationships](extensions_declarative_relationships.html#declarative-many-to-many)
        - 使用声明式时的其他选项。

        [Association
        Object](basic_relationships.html#association-pattern) -
        在组合关联表关系时替代[`secondary`](#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")，允许在关联表上指定其他属性。

        [Composite “Secondary”
        Joins](join_conditions.html#composite-secondary-join) -
        一种较少使用的模式，在某些情况下可以启用复杂的[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        SQL条件。

        版本0.9.2中的新功能： [`secondary`](#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")在引用[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")实例时更有效。

    -   T0\> **active\_history =假 T1\> [¶ T2\> - 当`True`](#sqlalchemy.orm.relationship.params.active_history)**通常情况下，简单多对一的历史追踪逻辑只需要知道“新”值就可以执行刷新。该标志可用于使用[`attributes.get_history()`](session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")的应用程序，该应用程序还需要知道该属性的“上一个”值。
    -   **backref** [¶](#sqlalchemy.orm.relationship.params.backref) -

        indicates the string name of a property to be placed on the
        related mapper’s class that will handle this relationship in the
        other
        direction.其他属性将在配置映射器时自动创建。也可以作为[`backref()`](#sqlalchemy.orm.backref "sqlalchemy.orm.backref")对象传递以控制新关系的配置。

        也可以看看

        [Linking Relationships with
        Backref](backref.html#relationships-backref) -
        介绍性文档和示例。

        [`back_populates`](#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")
        - alternative form of backref specification.

        [`backref()`](#sqlalchemy.orm.backref "sqlalchemy.orm.backref") -
        allows control over [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        configuration when using [`backref`](#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship").

    -   **back\_populates**
        [¶](#sqlalchemy.orm.relationship.params.back_populates) -

        一个字符串名称，作用与[`backref`](#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")相同，除了补充属性**不是**自动创建，而是必须在其他映射器上显式配置。补充属性还应该指示[`back_populates`](#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")到此关系，以确保正常运行。

        也可以看看

        [Linking Relationships with
        Backref](backref.html#relationships-backref) -
        介绍性文档和示例。

        [`backref`](#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")
        - alternative form of backref specification.

    -   **bake\_queries = True**
        [¶](#sqlalchemy.orm.relationship.params.bake_queries) -

        当首先调用[`bake_lazy_loaders()`](extensions_baked.html#sqlalchemy.ext.baked.bake_lazy_loaders "sqlalchemy.ext.baked.bake_lazy_loaders")函数时，使用[`BakedQuery`](extensions_baked.html#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")缓存来缓存惰性加载中使用的SQL的构造。默认为True，当烘焙查询缓存系统正在使用时，它旨在为每个关系提供“退出”标志。

        警告

        当调用应用程序范围的[`bake_lazy_loaders()`](extensions_baked.html#sqlalchemy.ext.baked.bake_lazy_loaders "sqlalchemy.ext.baked.bake_lazy_loaders")函数时，仅**标志**有效。它默认为True，因此是“退出”标志。

        如果烘焙查询在其他情况下正在使用，则将此标志设置为False可能会减少此[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的ORM内存使用量，或解决在烘焙查询缓存系统中观察到的未解决的稳定性问题。

        版本1.0.0中的新功能

        也可以看看

        [Baked Queries](extensions_baked.html)

    -   **cascade** [¶](#sqlalchemy.orm.relationship.params.cascade) -

        一个逗号分隔的级联规则列表，确定会话操作应该如何从父级到子级“级联”。这默认为`False`，这意味着应该使用默认级联 -
        这个默认级联是`“save-update， 合并” < / T2>。`

        The available cascades are `save-update`,
        `merge`, `expunge`,
        `delete`, `delete-orphan`, and `refresh-expire`. An
        additional option, `all` indicates shorthand
        for
        `"save-update, merge, refresh-expire, expunge, delete"`, and is often used as in
        `"all, delete-orphan"` to indicate that
        related objects should follow along with the parent object in
        all cases, and be deleted when de-associated.

        也可以看看

        [Cascades](cascades.html#unitofwork-cascades) -
        每个可用级联选项的详细信息。

        [Configuring delete/delete-orphan
        Cascade](tutorial.html#tutorial-delete-cascade) -
        描述删除级联的教程示例。

    -   **cascade\_backrefs = True**
        [¶](#sqlalchemy.orm.relationship.params.cascade_backrefs) -

        一个布尔值，用于指示`save-update`级联应该沿着backref截取的赋值事件操作。当设置为`False`时，如果通过backref接收事件，则由此关系管理的属性不会将传入的瞬态对象级联到永久父级的会话中。

        也可以看看

        [Controlling Cascade on Backrefs](cascades.html#backref-cascade)
        - 有关如何使用[`cascade_backrefs`](#sqlalchemy.orm.relationship.params.cascade_backrefs "sqlalchemy.orm.relationship")选项的完整讨论和示例。

    -   **collection\_class**
        [¶](#sqlalchemy.orm.relationship.params.collection_class) -

        一个返回新的列表持有对象的类或可调用对象。将用来代替存储元素的普通列表。

        也可以看看

        [Customizing Collection
        Access](collections.html#custom-collections) -
        介绍性文档和示例。

    -   **comparator\_factory**
        [¶](#sqlalchemy.orm.relationship.params.comparator_factory) -

        一个扩展[`RelationshipProperty.Comparator`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator "sqlalchemy.orm.properties.RelationshipProperty.Comparator")的类，它为比较操作提供自定义的SQL子句生成。

        也可以看看

        [`PropComparator`](internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")
        - some detail on redefining comparators at this level.

        [Operator
        Customization](mapped_attributes.html#custom-comparators) -
        简要介绍此功能。

    -   **distinct\_target\_key = None**
        [¶](#sqlalchemy.orm.relationship.params.distinct_target_key) -

        指示“子查询”渴望加载是否应将DISTINCT关键字应用于最内层的SELECT语句。当作为`None`离开时，在目标列不包含目标表的完整主键的情况下，将应用DISTINCT关键字。当设置为`True`时，DISTINCT关键字无条件地应用于最内层的SELECT。

        当DISTINCT将最内层子查询的性能降低到超出最内层行可能导致的性能时，可能需要将此标志设置为False。

        0.8.3版中的新功能： - [`distinct_target_key`](#sqlalchemy.orm.relationship.params.distinct_target_key "sqlalchemy.orm.relationship")允许子查询eager加载器将DISTINCT修饰符应用于最内层的SELECT。

        版本0.9.0更改： - [`distinct_target_key`](#sqlalchemy.orm.relationship.params.distinct_target_key "sqlalchemy.orm.relationship")现在默认为`None`，因此该功能会自动为其中最内层查询目标一个非唯一的密钥。

        也可以看看

        [Relationship Loading Techniques](loading_relationships.html) -
        包含对子查询渴望加载的介绍。

    -   **doc**[¶](#sqlalchemy.orm.relationship.params.doc) – docstring
        which will be applied to the resulting descriptor.
    -   **扩展名** [¶](#sqlalchemy.orm.relationship.params.extension) -

        一个[`AttributeExtension`](deprecated.html#sqlalchemy.orm.interfaces.AttributeExtension "sqlalchemy.orm.interfaces.AttributeExtension")实例或扩展名列表，它们将被放置在放置在该类上的结果描述符的属性侦听器列表中。

        从版本0.7开始弃用：请参阅[`AttributeEvents`](events.html#sqlalchemy.orm.events.AttributeEvents "sqlalchemy.orm.events.AttributeEvents")。

    -   **foreign\_keys**
        [¶](#sqlalchemy.orm.relationship.params.foreign_keys) -

        在[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")对象的[`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")That
        is, if the [`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
        condition of this [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        is `a.id == b.a_id`, and the values in
        `b.a_id` are required to be present in
        `a.id`, then the “foreign key” column of
        this [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        is `b.a_id`.

        In normal cases, the [`foreign_keys`](#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")
        parameter is **not required.** [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        will automatically determine which columns in the
        [`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
        conditition are to be considered “foreign key” columns based on
        those [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects that specify [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey"),
        or are otherwise listed as referencing columns in a
        [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
        construct.
        只有在以下情况下才需要foreign\_keys：[`foreign_keys`](#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")

        > 1.  由于存在多个外键引用，因此从本地表到远程表构建联接的方式不止一种。设置`foreign_keys`将限制[`relationship()`{.xref .py .py-func
        >     .docutils
        >     .literal}](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")将这些列指定为“foreign”。
        >
        >     在版本0.8中更改：通过单独设置[`foreign_keys`{.xref .py
        >     .py-paramref .docutils
        >     .literal}](#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")参数可以解决多外键加入歧义，而无需明确设置[`primaryjoin`{.xref
        >     .py .py-paramref .docutils
        >     .literal}](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")以及。
        >
        > 2.  被映射的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")实际上并不存在[`ForeignKey`{.xref
        >     .py .py-class .docutils
        >     .literal}](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")或[`ForeignKeyConstraint`{.xref
        >     .py .py-class .docutils
        >     .literal}](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")结构，这通常是因为该表是从不支持外键的数据库反射（MySQL
        >     MyISAM）。
        > 3.  [`primaryjoin`{.xref .py .py-paramref .docutils
        >     .literal}](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")参数用于构造非标准连接条件，该条件使用通常不引用其“父”列的列或表达式，例如由复杂比较表示的连接条件使用SQL函数。

        [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构会引发信息错误消息，提示在出现模糊条件时使用[`foreign_keys`](#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")参数。在典型情况下，如果[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")不引发任何异常，通常不需要[`foreign_keys`](#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")参数。

        [`foreign_keys`](#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")
        may also be passed as a callable function which is evaluated at
        mapper initialization time, and may be passed as a
        Python-evaluable string when using Declarative.

        也可以看看

        [Handling Multiple Join
        Paths](join_conditions.html#relationship-foreign-keys)

        [Creating Custom Foreign
        Conditions](join_conditions.html#relationship-custom-foreign)

        [`foreign()`](#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign") -
        允许直接注释[`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")条件中的“外部”列。

        0.8版中的新功能 [`foreign()`](#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")注释也可以直接应用于[`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")表达式，该表达式是一种替代的，更具体的描述特定[`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")中的哪些列应被视为“外来”。

    -   **info** [¶](#sqlalchemy.orm.relationship.params.info) -

        可选数据字典，将填充到此对象的[`MapperProperty.info`](internals.html#MapperProperty.info "MapperProperty.info")属性中。

        0.8版本中的新功能

    -   **innerjoin = False**
        [¶](#sqlalchemy.orm.relationship.params.innerjoin) -

        当`True`时，加入的紧急加载将使用内部联接来加入相关表而不是外部联接。此选项的用途通常是性能之一，因为内部联接通常比外部联接执行得更好。

        当关系通过使用不可为空的局部外键多对一地引用一个对象时，或者当引用是一对一或集合是一对一的时候，该标志可以设置为`True`保证有一个或至少一个条目。

        该选项支持与[`joinedload.innerjoin`](loading_relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")相同的“嵌套”和“非嵌入”选项。有关嵌套/未引入行为的详细信息，请参阅该标志。

        也可以看看

        [`joinedload.innerjoin`](loading_relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")
        - 由loader选项指定的选项，包括嵌套行为的详细信息。

        [What Kind of Loading to Use
        ?](loading_relationships.html#what-kind-of-loading) -
        讨论各种装载机选项的一些细节。

    -   **join\_depth**
        [¶](#sqlalchemy.orm.relationship.params.join_depth) -

        当非`None`时，指示深度“渴望”加载器应该加入自我引用或循环关系的级别的整数值。该数字表示同一个映射器在特定连接分支的加载条件下应出现多少次。当缺省值为`None`时，渴望的加载器在遇到链中已经更高的相同目标映射器时将停止链接。该选项适用于加入和子查询的加载器。

        也可以看看

        [Configuring Self-Referential Eager
        Loading](self_referential.html#self-referential-eager-loading) -
        介绍性文档和示例。

    -   **lazy ='select'** [¶](#sqlalchemy.orm.relationship.params.lazy)
        -

        指定应该如何加载相关项目。默认值是`select`。价值观包括：

        -   `select` - items should be loaded lazily
            when the property is first accessed, using a separate SELECT
            statement, or identity map fetch for simple many-to-one
            references.
        -   `immediate` - items should be loaded as
            the parents are loaded, using a separate SELECT statement,
            or identity map fetch for simple many-to-one references.
        -   `joined` - 应该使用JOIN或LEFT OUTER
            JOIN“加热”与父项相同的查询。连接是否为“外部”取决于[`innerjoin`](#sqlalchemy.orm.relationship.params.innerjoin "sqlalchemy.orm.relationship")参数。
        -   `subquery` - items should be loaded
            “eagerly” as the parents are loaded, using one additional
            SQL statement, which issues a JOIN to a subquery of the
            original statement, for each collection requested.
        -   `noload` -
            任何时候都不应该发生加载。这是为了支持“只写”属性或以某种特定于应用程序的方式填充的属性。
        -   `raise` -
            不允许延迟加载；访问该属性，如果其值尚未通过预加载加载，则会引发[`InvalidRequestError`{.xref
            .py .py-exc .docutils
            .literal}](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")。

            版本1.1中的新功能

        -   `dynamic` -
            该属性将为所有读取操作返回一个预配置的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，在迭代结果之前，可以对其应用进一步的过滤操作。有关更多详细信息，请参阅[Dynamic
            Relationship
            Loaders](collections.html#dynamic-relationship)部分。
        -   真 - “选择”的同义词
        -   假 - “加入”的同义词
        -   无 - “noload”的同义词

        也可以看看

        [*Relationship Loading Techniques*](loading_relationships.html)
        - 完整的关系加载器配置文档。

        [Dynamic Relationship
        Loaders](collections.html#dynamic-relationship) -
        `dynamic`选项的详细信息。

        [Setting Noload,
        RaiseLoad](collections.html#collections-noload-raiseload) -
        关于“noload”和“raise”的注释

    -   **load\_on\_pending = False**
        [¶](#sqlalchemy.orm.relationship.params.load_on_pending) -

        指示暂时或挂起的父对象的加载行为。

        设置为`True`时，会导致lazy-loader为不持久的父对象发出查询，这意味着它从未被刷新过。当禁用自动刷新或暂挂对象已被“附加”到[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")但不属于其暂挂集合的一部分时，这可能对未决对象有效。

        当正常使用ORM时，[`load_on_pending`](#sqlalchemy.orm.relationship.params.load_on_pending "sqlalchemy.orm.relationship")标志不会改善行为
        -
        对象引用应该在对象级而不是在外键级构建，以便它们以普通方式存在于flush收益。该标志不适用于一般用途。

        也可以看看

        [`Session.enable_relationship_loading()`](session_api.html#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")
        -
        此方法为整个对象建立“加载挂起”行为，并允许加载保持暂时或分离的对象。

    -   **order\_by** [¶](#sqlalchemy.orm.relationship.params.order_by)
        -

        指示加载这些项目时应该应用的顺序。[`order_by`](#sqlalchemy.orm.relationship.params.order_by "sqlalchemy.orm.relationship")
        is expected to refer to one of the [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects to which the target class is mapped, or the attribute
        itself bound to the target class which refers to the column.

        [`order_by`](#sqlalchemy.orm.relationship.params.order_by "sqlalchemy.orm.relationship")也可以作为一个可调用函数传递，该函数在映射器初始化时计算，并且可以在使用Declarative时作为Python可评估字符串传递。

    -   **passive\_deletes = False**
        [¶](#sqlalchemy.orm.relationship.params.passive_deletes) -

        指示删除操作期间的加载行为。

        True值表示在父级删除操作期间不应加载卸载的子项。通常，当删除父项时，将加载所有子项，以便它们可以标记为已删除，或者将其父项的外键设置为NULL。Marking
        this flag as True usually implies an ON DELETE rule is in place
        which will handle updating/deleting child rows on the database
        side.

        另外，如果没有启用删除或删除孤立级联，则将该标志设置为字符串值“all”将禁用子级外键的“空出”。这通常用于数据库端的触发或错误引发场景。请注意，冲突发生后，会话中子对象的外键属性不会更改，因此这是非常特殊的用例设置。

        也可以看看

        [Using Passive Deletes](collections.html#passive-deletes) -
        介绍性文档和示例。

    -   **passive\_updates = True**
        [¶](#sqlalchemy.orm.relationship.params.passive_updates) -

        指示引用的主键值发生更改时要执行的持久性行为，指示引用的外键列也将需要更改其值。

        如果为True，则假定在数据库的外键上配置了`ON UPDATE CASCADE`数据库将处理UPDATE从源列到相关行的传播。当False时，SQLAlchemy
        [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构将尝试发出自己的UPDATE语句来修改相关的目标。但是请注意，SQLAlchemy
        **不能**为多个级联发出UPDATE。另外，在数据库实际上实施参照完整性的情况下，将此标志设置为False是不兼容的，除非这些限制是明确“延迟”的，如果目标后端支持它的话。

        强烈建议使用可变主键的应用程序将`passive_updates`设置为True，而是使用数据库本身的参照完整性功能来高效完整地处理更改。

        也可以看看

        [Mutable Primary Keys / Update
        Cascades](relationship_persistence.html#passive-updates) -
        Introductory documentation and examples.

        [`mapper.passive_updates`](mapping_api.html#sqlalchemy.orm.mapper.params.passive_updates "sqlalchemy.orm.mapper")
        - 一个对连接表继承映射有效的类似标志。

    -   **post\_update**
        [¶](#sqlalchemy.orm.relationship.params.post_update) -

        这表示该关系应该在INSERT之后或DELETE之前由第二个UPDATE语句处理。目前，它也会在实例更新后发出UPDATE，尽管这在技术上应该得到改进。该标志用于处理保存两个单独行之间的双向依赖关系（即，每行都引用另一行），否则将无法完全插入或删除两行，因为一行存在于另一行之前。当一个特定的映射安排会产生两个相互依赖的行时使用这个标志，例如一个与一组子行有一对多关系的表，还有一个引用单个子行的列在该列表中（即两个表都包含彼此的外键）。如果刷新操作返回检测到“循环依赖”的错误，则这是一个提示，您可能希望使用[`post_update`](#sqlalchemy.orm.relationship.params.post_update "sqlalchemy.orm.relationship")来“中断”该循环。

        也可以看看

        [Rows that point to themselves / Mutually Dependent
        Rows](relationship_persistence.html#post-update) -
        介绍性文档和示例。

    -   **primaryjoin**
        [¶](#sqlalchemy.orm.relationship.params.primaryjoin) -

        一个将用作此子对象与父对象的主连接的SQL表达式，或者以多对多关系形式表示主对象与关联表的连接。默认情况下，根据父表和子表（或关联表）的外键关系计算此值。

        [`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
        may also be passed as a callable function which is evaluated at
        mapper initialization time, and may be passed as a
        Python-evaluable string when using Declarative.

        也可以看看

        [Specifying Alternate Join
        Conditions](join_conditions.html#relationship-primaryjoin)

    -   **remote\_side**
        [¶](#sqlalchemy.orm.relationship.params.remote_side) -

        用于自我指涉关系，表示构成关系“远程端”的列或列的列表。

        [`relationship.remote_side`](#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")也可以作为一个可调用的函数传递，它在映射器初始化时计算，并且在使用Declarative时可以作为Python可评估的字符串传递。

        版本0.8中的更改： [`remote()`](#sqlalchemy.orm.remote "sqlalchemy.orm.remote")注释也可以直接应用于`primaryjoin`表达式，该表达式是一个替代的，更具体的描述特定`primaryjoin`中的哪些列应被视为“远程”。

        也可以看看

        [Adjacency List
        Relationships](self_referential.html#self-referential) -
        深入解释如何使用[`remote_side`](#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")来配置自我参照关系。

        [`remote()`](#sqlalchemy.orm.remote "sqlalchemy.orm.remote") -
        通常在使用自定义[`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")条件时实现与[`remote_side`](#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")相同目的的注释功能。

    -   **query\_class**
        [¶](#sqlalchemy.orm.relationship.params.query_class) -

        将被用作由“动态”关系返回的“appender查询”的基础的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")子类，即指定`lazy="dynamic"`或者使用[`orm.dynamic_loader()`](#sqlalchemy.orm.dynamic_loader "sqlalchemy.orm.dynamic_loader")函数以其他方式构造。

        也可以看看

        [Dynamic Relationship
        Loaders](collections.html#dynamic-relationship) -
        “动态”关系加载器介绍。

    -   **secondaryjoin**
        [¶](#sqlalchemy.orm.relationship.params.secondaryjoin) -

        一个SQL表达式，将用作关联表与子对象的连接。默认情况下，根据关联表和子表的外键关系计算此值。

        [`secondaryjoin`](#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")
        may also be passed as a callable function which is evaluated at
        mapper initialization time, and may be passed as a
        Python-evaluable string when using Declarative.

        也可以看看

        [Specifying Alternate Join
        Conditions](join_conditions.html#relationship-primaryjoin)

    -   **single\_parent**
        [¶](#sqlalchemy.orm.relationship.params.single_parent) -

        如果为True，则安装一个验证器，该验证器可以防止对象一次与多个父对象关联。这用于多对一或多对多关系，应该将其视为一对一或一对多关系。它的用法是可选的，除了[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构是多对一或多对多的，并且还指定了`delete-orphan`级联选项。[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构本身会引发错误，指示何时需要此选项。

        也可以看看

        [Cascades](cascades.html#unitofwork-cascades) -
        包含[`single_parent`](#sqlalchemy.orm.relationship.params.single_parent "sqlalchemy.orm.relationship")标志何时适用的详细信息。

    -   **uselist** [¶](#sqlalchemy.orm.relationship.params.uselist) -

        指示该属性是否应该作为列表或标量加载的布尔值。在大多数情况下，根据关系的类型和方向，这个值由映射器配置时的[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")自动确定
        -
        一对多形成一个列表，多对一形成一个标量，许多到很多是一个列表。如果通常需要一个标量（如双向一对一关系），则将[`uselist`](#sqlalchemy.orm.relationship.params.uselist "sqlalchemy.orm.relationship")设置为False。

        [`uselist`](#sqlalchemy.orm.relationship.params.uselist "sqlalchemy.orm.relationship")标志在现有[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构中也可用作只读属性，可用于确定[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")

            >>> User.addresses.property.uselist
            True

        也可以看看

        [One To One](basic_relationships.html#relationships-one-to-one)
        - Introduction to the “one to one” relationship pattern, which
        is typically when the [`uselist`](#sqlalchemy.orm.relationship.params.uselist "sqlalchemy.orm.relationship")
        flag is needed.

    -   **viewonly=False**[¶](#sqlalchemy.orm.relationship.params.viewonly)
        – when set to True, the relationship is used only for loading
        objects, and not for any persistence operation.
        指定[`viewonly`](#sqlalchemy.orm.relationship.params.viewonly "sqlalchemy.orm.relationship")的[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")可以在[`primaryjoin`](#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")条件中使用更广泛的SQL操作，包括使用各种比较运算符以及SQL函数（如[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")）。The
        [`viewonly`](#sqlalchemy.orm.relationship.params.viewonly "sqlalchemy.orm.relationship")
        flag is also of general use when defining any kind of
        [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        that doesn’t represent the full set of related objects, to
        prevent modifications of the collection from resulting in
        persistence operations.

 `sqlalchemy.orm.`{.descclassname}`backref`{.descname}(*name*, *\*\*kwargs*)[¶](#sqlalchemy.orm.backref "Permalink to this definition")
:   使用显式关键字参数创建一个后端引用，这些参数是可以发送到[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的相同参数。

    与[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的`backref`关键字参数一起使用以代替字符串参数，例如：

        'items':relationship(
            SomeItem, backref=backref('parent', lazy='subquery'))

    也可以看看

    [Linking Relationships with
    Backref](backref.html#relationships-backref)

 `sqlalchemy.orm.`{.descclassname}`relation`{.descname}(*\*arg*, *\*\*kw*)[¶](#sqlalchemy.orm.relation "Permalink to this definition")
:   [`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的同义词。

 `sqlalchemy.orm.`{.descclassname}`dynamic_loader`{.descname}(*argument*, *\*\*kw*)[¶](#sqlalchemy.orm.dynamic_loader "Permalink to this definition")
:   构建一个动态加载映射器属性。

    这与使用[`relationship()`](#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")中的`lazy='dynamic'`参数基本相同：

        dynamic_loader(SomeClass)

        # is the same as

        relationship(SomeClass, lazy="dynamic")

    有关动态加载的更多详细信息，请参见[Dynamic Relationship
    Loaders](collections.html#dynamic-relationship)部分。

` sqlalchemy.orm。 T0> 外国 T1> （ T2>  EXPR  T3> ） T4> ¶ T5 >`{.descclassname}
:   使用“外部”注释标注一个primaryjoin表达式的一部分。

    有关使用说明，请参阅[Creating Custom Foreign
    Conditions](join_conditions.html#relationship-custom-foreign)部分。

    0.8版本中的新功能

    也可以看看

    [Creating Custom Foreign
    Conditions](join_conditions.html#relationship-custom-foreign)

    [`remote()`](#sqlalchemy.orm.remote "sqlalchemy.orm.remote")

` sqlalchemy.orm。 T0> 远程 T1> （ T2>  EXPR  T3> ） T4> ¶ T5 >`{.descclassname}
:   使用'远程'注释标注一个primaryjoin表达式的一部分。

    有关使用说明，请参阅[Creating Custom Foreign
    Conditions](join_conditions.html#relationship-custom-foreign)部分。

    0.8版本中的新功能

    也可以看看

    [Creating Custom Foreign
    Conditions](join_conditions.html#relationship-custom-foreign)

    [`foreign()`](#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")


