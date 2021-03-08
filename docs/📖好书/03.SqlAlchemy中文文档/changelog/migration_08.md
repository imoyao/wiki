---
title: migration_08
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/1557ad/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
SQLAlchemy 0.8 有哪些新特性？[¶](#what-s-new-in-sqlalchemy-0-8 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍了截至 2012 年 10 月发布的 SQLAlchemy 版本 0.7，以及预计 2013 年初发布的 SQLAlchemy 版本 0.8 之间的变化。

文件日期：2012 年 10 月 25 日更新日期：2013 年 3 月 9 日

引言[¶ T0\>](#introduction "Permalink to this headline")
--------------------------------------------------------

本指南介绍了 SQLAlchemy
0.8 版中的新增功能，并介绍了影响用户将其应用程序从 0.7 系列 SQLAlchemy 迁移到 0.8 的更改。

SQLAlchemy 版本将在 1.0 版中关闭，而 0.5 版以后的每个新版本都会减少主要的使用更改。大部分应用现代 0.7 模式的应用程序应该可以移动到 0.8 而无需更改。使用 0.6 甚至 0.5 模式的应用程序也应该直接迁移到 0.8，尽管更大的应用程序可能需要使用每个临时版本进行测试。

平台支持[¶](#platform-support "Permalink to this headline")
-----------------------------------------------------------

### 针对 Python 2.5 及更高版本[¶](#targeting-python-2-5-and-up-now "Permalink to this headline")

SQLAlchemy 0.8 将针对 Python 2.5 并转发； Python 2.4 的兼容性正在被丢弃。

The internals will be able to make usage of Python ternaries (that is,
`x if y else z`) which will improve things versus
the usage of `y and x or z`, which naturally has
been the source of some bugs, as well as context managers (that is,
`with:`) and perhaps in some cases
`try:/except:/else:` blocks which will help with
code readability.

SQLAlchemy 最终也会减少 2.5 的支持 -
当 2.6 达到基线时，SQLAlchemy 将转而使用 2.6 /
3.3 原地兼容性，去掉`2to3`工具的使用并维护一个源代码库与 Python 2 和 3 同时工作。

新的 ORM 功能[¶](#new-orm-features "Permalink to this headline")
--------------------------------------------------------------

### 重写[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构[¶](#rewritten-relationship-mechanics "Permalink to this headline")

0.8 特性是一个关于如何[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")确定如何在两个实体之间进行连接的改进且功能强大的系统。新系统包含以下功能：

-   The `primaryjoin` argument is **no longer
    needed** when constructing a [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    against a class that has multiple foreign key paths to the target.
    只需要`foreign_keys`参数来指定应包含的列：

        class Parent(Base):
            __tablename__ = 'parent'
            id = Column(Integer, primary_key=True)
            child_id_one = Column(Integer, ForeignKey('child.id'))
            child_id_two = Column(Integer, ForeignKey('child.id'))

            child_one = relationship("Child", foreign_keys=child_id_one)
            child_two = relationship("Child", foreign_keys=child_id_two)

        class Child(Base):
            __tablename__ = 'child'
            id = Column(Integer, primary_key=True)

-   与自引用关系的关系，现在支持**列指向自身**的复合外键。规范情况如下：

        class Folder(Base):
            __tablename__ = 'folder'
            __table_args__ = (
              ForeignKeyConstraint(
                  ['account_id', 'parent_id'],
                  ['folder.account_id', 'folder.folder_id']),
            )

            account_id = Column(Integer, primary_key=True)
            folder_id = Column(Integer, primary_key=True)
            parent_id = Column(Integer)
            name = Column(String)

            parent_folder = relationship("Folder",
                                backref="child_folders",
                                remote_side=[account_id, folder_id]
                          )

    Above, the `Folder` refers to its parent
    `Folder` joining from `account_id` to itself, and `parent_id` to
    `folder_id`.
    当 SQLAlchemy 构造一个自动连接时，它不再可以假设“远程”一侧的所有列都是别名，而“本地”一侧的所有列都不是这样
    - `account_id`列是**两边**。所以内部关系机制被完全重写以支持完全不同的系统，由此生成两个`account_id`副本，每个副本包含不同的*注释*以确定它们在语句中的角色。请注意基本热切负载中的连接条件：

        SELECT
            folder.account_id AS folder_account_id,
            folder.folder_id AS folder_folder_id,
            folder.parent_id AS folder_parent_id,
            folder.name AS folder_name,
            folder_1.account_id AS folder_1_account_id,
            folder_1.folder_id AS folder_1_folder_id,
            folder_1.parent_id AS folder_1_parent_id,
            folder_1.name AS folder_1_name
        FROM folder
            LEFT OUTER JOIN folder AS folder_1
            ON
                folder_1.account_id = folder.account_id
                AND folder.folder_id = folder_1.parent_id

        WHERE folder.folder_id = ? AND folder.account_id = ?

-   以前很难的自定义连接条件，如涉及函数和/或 CASTing 类型的连接条件，现在在大多数情况下会按预期运行：

        class HostEntry(Base):plainplain
            __tablename__ = 'host_entry'

            id = Column(Integer, primary_key=True)
            ip_address = Column(INET)
            content = Column(String(50))

            # relationship() using explicit foreign_keys, remote_side
            parent_host = relationship("HostEntry",
                                primaryjoin=ip_address == cast(content, INET),
                                foreign_keys=content,
                                remote_side=ip_address
                            )

    新的[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")机制利用了被称为[annotations](glossary.html#term-annotations)的 SQLAlchemy 概念。这些注释也可以通过[`foreign()`](orm_relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")和[`remote()`](orm_relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")函数显式地提供给应用程序代码，作为提高高级配置可读性或直接注入精确度配置，绕过通常的加入检查试探法：

        from sqlalchemy.orm import foreign, remoteplainplain

        class HostEntry(Base):
            __tablename__ = 'host_entry'

            id = Column(Integer, primary_key=True)
            ip_address = Column(INET)
            content = Column(String(50))

            # relationship() using explicit foreign() and remote() annotations
            # in lieu of separate arguments
            parent_host = relationship("HostEntry",
                                primaryjoin=remote(ip_address) == \
                                        cast(foreign(content), INET),
                            )

也可以看看

[Configuring how Relationship
Joins](orm_join_conditions.html#relationship-configure-joins) -
关于[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的新修订部分，详细介绍了定制相关属性和集合访问的最新技术。

[＃1401](http://www.sqlalchemy.org/trac/ticket/1401)
[＃610](http://www.sqlalchemy.org/trac/ticket/610)

### 新类/对象检查系统[¶](#new-class-object-inspection-system "Permalink to this headline")

许多 SQLAlchemy 用户正在编写需要检查映射类属性的系统，包括能够获取主键列，对象关系，普通属性等等，通常用于构建数据编组系统，如 JSON
/ XML 转换方案，当然还有形式库丰富。

最初，[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")模型是最初的检查点，它们具有良好的文件记录系统。虽然 SQLAlchemy
ORM 模型也完全可以反映内容，但这从来就不是一个完全稳定和支持的功能，用户往往不清楚如何获取这些信息。

现在，0.8 为此提供了一致，稳定且完全记录的 API，其中包括一个用于映射类，实例，属性和其他 Core 和 ORM 构造的检查系统。该系统的入口点是核心级别的[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数。在大多数情况下，被检查的对象已经是 SQLAlchemy 系统的一部分，比如[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，[`InstanceState`](orm_internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")，[`Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")。在某些情况下，添加新对象的工作是在特定上下文中提供检查 API，例如[`AliasedInsp`](orm_query.html#sqlalchemy.orm.util.AliasedInsp "sqlalchemy.orm.util.AliasedInsp")和[`AttributeState`](orm_internals.html#sqlalchemy.orm.state.AttributeState "sqlalchemy.orm.state.AttributeState")。

一些关键功能的演练如下：

    >>> class User(Base):plain
    ...     __tablename__ = 'user'
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(String)
    ...     name_syn = synonym(name)
    ...     addresses = relationship("Address")
    ...

    >>> # universal entry point is inspect()
    >>> b = inspect(User)

    >>> # b in this case is the Mapper
    >>> b
    <Mapper at 0x101521950; User>

    >>> # Column namespace
    >>> b.columns.id
    Column('id', Integer(), table=<user>, primary_key=True, nullable=False)

    >>> # mapper's perspective of the primary key
    >>> b.primary_key
    (Column('id', Integer(), table=<user>, primary_key=True, nullable=False),)

    >>> # MapperProperties available from .attrs
    >>> b.attrs.keys()
    ['name_syn', 'addresses', 'id', 'name']

    >>> # .column_attrs, .relationships, etc. filter this collection
    >>> b.column_attrs.keys()
    ['id', 'name']

    >>> list(b.relationships)
    [<sqlalchemy.orm.properties.RelationshipProperty object at 0x1015212d0>]

    >>> # they are also namespaces
    >>> b.column_attrs.id
    <sqlalchemy.orm.properties.ColumnProperty object at 0x101525090>

    >>> b.relationships.addresses
    <sqlalchemy.orm.properties.RelationshipProperty object at 0x1015212d0>

    >>> # point inspect() at a mapped, class level attribute,
    >>> # returns the attribute itself
    >>> b = inspect(User.addresses)
    >>> b
    <sqlalchemy.orm.attributes.InstrumentedAttribute object at 0x101521fd0>

    >>> # From here we can get the mapper:
    >>> b.mapper
    <Mapper at 0x101525810; Address>

    >>> # the parent inspector, in this case a mapper
    >>> b.parent
    <Mapper at 0x101521950; User>

    >>> # an expression
    >>> print(b.expression)
    "user".id = address.user_id

    >>> # inspect works on instances
    >>> u1 = User(id=3, name='x')
    >>> b = inspect(u1)

    >>> # it returns the InstanceState
    >>> b
    <sqlalchemy.orm.state.InstanceState object at 0x10152bed0>

    >>> # similar attrs accessor refers to the
    >>> b.attrs.keys()
    ['id', 'name_syn', 'addresses', 'name']

    >>> # attribute interface - from attrs, you get a state object
    >>> b.attrs.id
    <sqlalchemy.orm.state.AttributeState object at 0x10152bf90>

    >>> # this object can give you, current value...
    >>> b.attrs.id.value
    3

    >>> # ... current history
    >>> b.attrs.id.history
    History(added=[3], unchanged=(), deleted=())

    >>> # InstanceState can also provide session state information
    >>> # lets assume the object is persistent
    >>> s = Session()
    >>> s.add(u1)
    >>> s.commit()

    >>> # now we can get primary key identity, always
    >>> # works in query.get()
    >>> b.identity
    (3,)

    >>> # the mapper level key
    >>> b.identity_key
    (<class '__main__.User'>, (3,))

    >>> # state within the session
    >>> b.persistent, b.transient, b.deleted, b.detached
    (True, False, False, False)

    >>> # owning session
    >>> b.session
    <sqlalchemy.orm.session.Session object at 0x101701150>

也可以看看

[Runtime Inspection API](core_inspection.html)

[＃2208 T0\>](http://www.sqlalchemy.org/trac/ticket/2208)

### 新的 with\_polymorphic()功能可用于任何地方[¶](#new-with-polymorphic-feature-can-be-used-anywhere "Permalink to this headline")

The [`Query.with_polymorphic()`](orm_query.html#sqlalchemy.orm.query.Query.with_polymorphic "sqlalchemy.orm.query.Query.with_polymorphic")
method allows the user to specify which tables should be present when
querying against a joined-table entity.
不幸的是，这个方法很笨拙，只适用于列表中的第一个实体，否则在内部使用和内部使用都会有尴尬的行为。已添加名为[`with_polymorphic()`](orm_inheritance.html#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")的对[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")结构的新增强，允许将任何实体“别名”为其自身的“多态”版本，可自由使用任何地方：

    from sqlalchemy.orm import with_polymorphic
    palias = with_polymorphic(Person, [Engineer, Manager])
    session.query(Company).\
                join(palias, Company.employees).\
                filter(or_(Engineer.language=='java', Manager.hair=='pointy'))

也可以看看

[Basic Control of Which Tables are
Queried](orm_inheritance.html#with-polymorphic) -
用于多态加载控制的新更新文档。

[＃2333 T0\>](http://www.sqlalchemy.org/trac/ticket/2333)

### of\_type() works with alias(), with\_polymorphic(), any(), has(), joinedload(), subqueryload(), contains\_eager()[¶](#of-type-works-with-alias-with-polymorphic-any-has-joinedload-subqueryload-contains-eager "Permalink to this headline")

The [`PropComparator.of_type()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")
method is used to specify a specific subtype to use when constructing
SQL expressions along a [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
that has a [polymorphic](glossary.html#term-polymorphic) mapping as its
target. This method can now be used to target *any number* of target
subtypes, by combining it with the new [`with_polymorphic()`](orm_inheritance.html#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")
function:

    # use eager loading in conjunction with with_polymorphic targetsplain
    Job_P = with_polymorphic(Job, [SubJob, ExtraJob], aliased=True)
    q = s.query(DataContainer).\
                join(DataContainer.jobs.of_type(Job_P)).\
                    options(contains_eager(DataContainer.jobs.of_type(Job_P)))

The method now works equally well in most places a regular relationship
attribute is accepted, including with loader functions like
[`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload"),
[`subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload"),
[`contains_eager()`](orm_loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager"),
and comparison methods like [`PropComparator.any()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.any "sqlalchemy.orm.interfaces.PropComparator.any")
and [`PropComparator.has()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.has "sqlalchemy.orm.interfaces.PropComparator.has"):

    # use eager loading in conjunction with with_polymorphic targets
    Job_P = with_polymorphic(Job, [SubJob, ExtraJob], aliased=True)
    q = s.query(DataContainer).\
                join(DataContainer.jobs.of_type(Job_P)).\
                    options(contains_eager(DataContainer.jobs.of_type(Job_P)))

    # pass subclasses to eager loads (implicitly applies with_polymorphic)
    q = s.query(ParentThing).\
                    options(
                        joinedload_all(
                            ParentThing.container,
                            DataContainer.jobs.of_type(SubJob)
                    ))

    # control self-referential aliasing with any()/has()
    Job_A = aliased(Job)
    q = s.query(Job).join(DataContainer.jobs).\
                    filter(
                        DataContainer.jobs.of_type(Job_A).\
                            any(and_(Job_A.id < Job.id, Job_A.type=='fred')
                        )
                    )

也可以看看

[Creating Joins to Specific Subtypes](orm_inheritance.html#of-type)

[＃2438](http://www.sqlalchemy.org/trac/ticket/2438)
[＃1106](http://www.sqlalchemy.org/trac/ticket/1106)

### 事件可以应用于未映射的超类[¶](#events-can-be-applied-to-unmapped-superclasses "Permalink to this headline")

Mapper 和实例事件现在可以与一个未映射的超类相关联，其中这些事件将被映射到这些子类时传播到子类。应该使用`propagate=True`标志。此功能允许将事件与声明性基类关联：

    from sqlalchemy.ext.declarative import declarative_baseplain

    Base = declarative_base()

    @event.listens_for("load", Base, propagate=True)
    def on_load(target, context):
        print("New instance loaded:", target)

    # on_load() will be applied to SomeClass
    class SomeClass(Base):
        __tablename__ = 'sometable'

        # ...

[＃2585 T0\>](http://www.sqlalchemy.org/trac/ticket/2585)

### 声明区分模块/包[¶](#declarative-distinguishes-between-modules-packages "Permalink to this headline")

Declarative 的一个关键特性是能够使用其字符串名称引用其他映射类。类名注册表现在对给定类的拥有模块和包是敏感的。类可以通过表达式中的虚线名称引用：

    class Snack(Base):plain
        # ...

        peanuts = relationship("nuts.Peanut",
                primaryjoin="nuts.Peanut.snack_id == Snack.id")

该解决方案允许使用任何完整或部分消除歧义的软件包名称。如果特定类的路径仍不明确，则会引发错误。

[＃2338 T0\>](http://www.sqlalchemy.org/trac/ticket/2338)

### 声明式[¶](#new-deferredreflection-feature-in-declarative "Permalink to this headline")中的新 DeferredReflection 特性

“延迟反射”示例已移至声明中的支持功能。这个特性允许只用占位符`Table`元数据构造声明式映射类，直到`prepare()`步骤被调用，给定一个`Engine`充分反映所有表格并建立实际映射。系统支持重写列，单个和联合继承，以及不同的每个引擎基数。现在可以根据在引擎创建时在一个步骤中汇编的现有表创建完整的声明性配置：

    class ReflectedOne(DeferredReflection, Base):
        __abstract__ = True

    class ReflectedTwo(DeferredReflection, Base):
        __abstract__ = True

    class MyClass(ReflectedOne):
        __tablename__ = 'mytable'

    class MyOtherClass(ReflectedOne):
        __tablename__ = 'myothertable'

    class YetAnotherClass(ReflectedTwo):
        __tablename__ = 'yetanothertable'

    ReflectedOne.prepare(engine_one)
    ReflectedTwo.prepare(engine_two)

也可以看看

[`DeferredReflection`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")

[＃2485 T0\>](http://www.sqlalchemy.org/trac/ticket/2485)

### ORM 类现在被核心构造接受[¶](#orm-classes-now-accepted-by-core-constructs "Permalink to this headline")

While the SQL expressions used with [`Query.filter()`](orm_query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter"),
such as `User.id == 5`, have always been compatible
for use with core constructs such as [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
the mapped class itself would not be recognized when passed to
[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
[`Select.select_from()`](core_selectable.html#sqlalchemy.sql.expression.Select.select_from "sqlalchemy.sql.expression.Select.select_from"),
or [`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate").
新的 SQL 注册系统允许映射类在核心内被接受为 FROM 子句：

    from sqlalchemy import select

    stmt = select([User]).where(User.id == 5)

以上，映射的`User`类将展开到映射`User`的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。

[＃2245 T0\>](http://www.sqlalchemy.org/trac/ticket/2245)

### Query.update()支持 UPDATE..FROM [¶](#query-update-supports-update-from "Permalink to this headline")

新的 UPDATE..FROM 机制在 query.update()中工作。下面，我们针对`SomeEntity`发出 UPDATE，并针对`SomeOtherEntity`添加了一个 FROM 子句（或等价物，具体取决于后端）：

    query(SomeEntity).\
        filter(SomeEntity.id==SomeOtherEntity.id).\
        filter(SomeOtherEntity.foo=='bar').\
        update({"data":"x"})

特别是，对已加入继承实体的更新是受支持的，前提是 UPDATE 的目标对要过滤的表是本地的，或者如果父表和子表混合在一起，则它们将显式连接到查询中。下面，给出`Engineer`作为`Person`的联合子类：

    query(Engineer).\plain
            filter(Person.id==Engineer.id).\
            filter(Person.name=='dilbert').\
            update({"engineer_data":"java"})

会产生：

    UPDATE engineer SET engineer_data='java' FROM person
    WHERE person.id=engineer.id AND person.name='dilbert'

[＃2365 T0\>](http://www.sqlalchemy.org/trac/ticket/2365)

### rollback()只会从 begin\_nested()[¶](#rollback-will-only-roll-back-dirty-objects-from-a-begin-nested "Permalink to this headline")回滚“脏”对象

通过`Session.begin_nested()` -
在`rollback()`上改变使用 SAVEPOINT 的用户的行为改变时，只有那些自上次刷新后变脏的对象才会有效过期时，`Session`的其余部分保持不变。这是因为对 SAVEPOINT 的 ROLLBACK 不会终止包含事务的隔离，所以不需要过期，除非那些在当前事务中没有刷新的更改。

[＃2452 T0\>](http://www.sqlalchemy.org/trac/ticket/2452)

### 缓存示例现在使用 dogpile.cache [¶](#caching-example-now-uses-dogpile-cache "Permalink to this headline")

缓存示例现在使用[dogpile.cache](https://dogpilecache.readthedocs.io/)。Dogpile.cache 是​​Beaker 缓存部分的重写，具有极其简单和快速的操作，并支持分布式锁定。

请注意，Dogpile 示例以及之前的 Beaker 示例所使用的 SQLAlchemy
API 已稍有变化，特别是如 Beaker 示例所示，需要进行此更改：

    --- examples/beaker_caching/caching_query.py
    +++ examples/beaker_caching/caching_query.py
    @@ -222,7 +222,8 @@

             """
             if query._current_path:
    -            mapper, key = query._current_path[-2:]
    +            mapper, prop = query._current_path[-2:]
    +            key = prop.key

                 for cls in mapper.class_.__mro__:
                     if (cls, key) in self._relationship_options:

也可以看看

`dogpile_caching`

[＃2589 T0\>](http://www.sqlalchemy.org/trac/ticket/2589)

新的核心功能[¶](#new-core-features "Permalink to this headline")
----------------------------------------------------------------

### Core [¶](#fully-extensible-type-level-operator-support-in-core "Permalink to this headline")中完全可扩展的类型级别操作符支持

核心迄今从来没有任何系统为 Column 和其他表达式结构添加对新 SQL 运算符的支持，除了[`ColumnOperators.op()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.op "sqlalchemy.sql.operators.ColumnOperators.op")方法，它足以让事情发挥作用。Core 从来没有任何系统可以让现有操作员的行为被覆盖。到目前为止，操作符可以被灵活地重新定义的唯一方法是在 ORM 层中，使用[`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")给出一个`comparator_factory`参数。因此，像 GeoAlchemy 这样的第三方库不得不以 ORM 为中心，并依靠一系列黑客来应用新的操作，并让它们正确传播。

Core中的新操作系统添加了一直缺少的钩子，它将新的和重载的操作符与*类型*关联。毕竟，它不是真正的列，CAST 运算符或 SQL 函数，它们真正驱动出现的操作类型，它是表达式的*类型*。实现细节是最小的
- 只有一些额外的方法被添加到核心[`ColumnElement`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")类型中，以便为可选的运算符集咨询它的[`TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")对象。新的或修改的操作可以通过使用[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")或“全局全面”通过附加新的[`TypeEngine.Comparator`](core_type_api.html#sqlalchemy.types.TypeEngine.Comparator "sqlalchemy.types.TypeEngine.Comparator")

例如，要将对数支持添加到[`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")类型中：

    from sqlalchemy.types import Numericplainplain
    from sqlalchemy.sql import func

    class CustomNumeric(Numeric):
        class comparator_factory(Numeric.Comparator):
            def log(self, other):
                return func.log(self.expr, other)

新的类型可以像任何其他类型一样使用：

    data = Table('data', metadata,plain
              Column('id', Integer, primary_key=True),
              Column('x', CustomNumeric(10, 5)),
              Column('y', CustomNumeric(10, 5))
         )

    stmt = select([data.c.x.log(data.c.y)]).where(data.c.x.log(2) < value)
    print(conn.execute(stmt).fetchall())

由此产生的新功能立即包括对 Postgresql 的 HSTORE 类型的支持，以及与 Postgresql 的 ARRAY 类型相关的新操作。它还为现有类型获取更多特定于这些类型的运算符（比如更多字符串，整数和日期运算符）铺平了道路。

也可以看看

[Redefining and Creating New
Operators](core_custom_types.html#types-operators)

[`HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")

[＃2547 T0\>](http://www.sqlalchemy.org/trac/ticket/2547)

### 对插入[¶](#multiple-values-support-for-insert "Permalink to this headline")的多值支持

The [`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")
method now supports a list of dictionaries, which will render a
multi-VALUES statement such as
`VALUES (<row1>), (<row2>), ...`.
这只与支持这种语法的后端相关，包括 Postgresql，SQLite 和 MySQL。它与通常的`executemany()`风格的 INSERT 不同，它保持不变：

    users.insert().values([plain
                        {"name": "some name"},
                        {"name": "some other name"},
                        {"name": "yet another name"},
                    ])

也可以看看

[`Insert.values()`](core_dml.html#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")

[＃2623 T0\>](http://www.sqlalchemy.org/trac/ticket/2623)

### 输入表达式[¶](#type-expressions "Permalink to this headline")

SQL 表达式现在可以与类型相关联。Historically, [`TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
has always allowed Python-side functions which receive both bound
parameters as well as result row values, passing them through a Python
side conversion function on the way to/back from the database.
新功能允许类似的功能，除了在数据库方面：

    from sqlalchemy.types import String
    from sqlalchemy import func, Table, Column, MetaData

    class LowerString(String):
        def bind_expression(self, bindvalue):
            return func.lower(bindvalue)

        def column_expression(self, col):
            return func.lower(col)

    metadata = MetaData()
    test_table = Table(
            'test_table',
            metadata,
            Column('data', LowerString)
    )

上面，`LowerString`类型定义了一个 SQL 表达式，只要在 SELECT 语句的 columns 子句中呈现`test_table.c.data`列时就会发出该表达式：

    >>> print(select([test_table]).where(test_table.c.data == 'HI'))
    SELECT lower(test_table.data) AS data
    FROM test_table
    WHERE test_table.data = lower(:data_1)

GeoAlchemy 的新版本也大量使用了该功能，以便根据类型规则在 SQL 中内联嵌入 PostGIS 表达式。

也可以看看

[Applying SQL-level Bind/Result
Processing](core_custom_types.html#types-sql-value-processing)

[＃1534 T0\>](http://www.sqlalchemy.org/trac/ticket/1534)

### 核心检查系统[¶](#core-inspection-system "Permalink to this headline")

[New Class/Object Inspection
System](#feature-orminspection-08)中引入的[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数也适用于核心。应用于[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")时，它会生成一个[`Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")对象：

    from sqlalchemy import inspectplain
    from sqlalchemy import create_engine

    engine = create_engine("postgresql://scott:tiger@localhost/test")
    insp = inspect(engine)
    print(insp.get_table_names())

It can also be applied to any [`ClauseElement`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement"),
which returns the [`ClauseElement`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
itself, such as [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select"),
etc. 这使它可以在 Core 和 ORM 结构之间流畅地工作。

### 新方法[`Select.correlate_except()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except") [¶](#new-method-select-correlate-except "Permalink to this headline")

[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
now has a method [`Select.correlate_except()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")
which specifies “correlate on all FROM clauses except those specified”.
它可用于映射相关子查询应正常关联的场景，除了可选的特定目标：

    class SnortEvent(Base):plain
        __tablename__ = "event"

        id = Column(Integer, primary_key=True)
        signature = Column(Integer, ForeignKey("signature.id"))

        signatures = relationship("Signature", lazy=False)

    class Signature(Base):
        __tablename__ = "signature"

        id = Column(Integer, primary_key=True)

        sig_count = column_property(
                        select([func.count('*')]).\
                            where(SnortEvent.signature == id).
                            correlate_except(SnortEvent)
                    )

也可以看看

[`Select.correlate_except()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate_except "sqlalchemy.sql.expression.Select.correlate_except")

### Postgresql HSTORE类型[¶](#postgresql-hstore-type "Permalink to this headline")

对 Postgresql 的`HSTORE`类型的支持现在可用作[`postgresql.HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")。This
type makes great usage of the new operator system to provide a full
range of operators for HSTORE types, including index access,
concatenation, and containment methods such as `has_key()`, `has_any()`, and `matrix()`:

    from sqlalchemy.dialects.postgresql import HSTORE

    data = Table('data_table', metadata,
            Column('id', Integer, primary_key=True),
            Column('hstore_data', HSTORE)
        )

    engine.execute(
        select([data.c.hstore_data['some_key']])
    ).scalar()

    engine.execute(
        select([data.c.hstore_data.matrix()])
    ).scalar()

也可以看看

[`postgresql.HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")

[`postgresql.hstore`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.hstore "sqlalchemy.dialects.postgresql.hstore")

[＃2606 T0\>](http://www.sqlalchemy.org/trac/ticket/2606)

### 增强的 Postgresql ARRAY 类型[¶](#enhanced-postgresql-array-type "Permalink to this headline")

[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型将接受可选的“维度”参数，将其固定为固定数量的维度，并在检索结果时大大提高效率：

    # old way, still works since PG supports N-dimensions per row:plainplain
    Column("my_array", postgresql.ARRAY(Integer))

    # new way, will render ARRAY with correct number of [] in DDL,
    # will process binds and results more efficiently as we don't need
    # to guess how many levels deep to go
    Column("my_array", postgresql.ARRAY(Integer, dimensions=2))

该类型还引入了新的运算符，使用新的类型特定的运算符框架。新的操作包括索引访问：

    result = conn.execute(plain
        select([mytable.c.arraycol[2]])
    )

在 SELECT 中切片访问：

    result = conn.execute(plain
        select([mytable.c.arraycol[2:4]])
    )

在更新中切片更新：

    conn.execute(
        mytable.update().values({mytable.c.arraycol[2:3]: [7, 8]})
    )

独立阵列文字：

    >>> from sqlalchemy.dialects import postgresqlplain
    >>> conn.scalar(
    ...    select([
    ...        postgresql.array([1, 2]) + postgresql.array([3, 4, 5])
    ...    ])
    ...  )
    [1, 2, 3, 4, 5]

数组串联，其中右侧`[4， 5， 6>`）被强制转换为数组文字：

    select([mytable.c.arraycol + [4, 5, 6]])

也可以看看

[`postgresql.ARRAY`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")

[`postgresql.array`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")

[＃2441 T0\>](http://www.sqlalchemy.org/trac/ticket/2441)

### SQLite [¶](#new-configurable-date-time-types-for-sqlite "Permalink to this headline")的新的，可配置的 DATE，TIME 类型

SQLite 没有内置的 DATE，TIME 或 DATETIME 类型，而是提供了一些支持将日期和时间值存储为字符串或整数。SQLite 的日期和时间类型在 0.8 中得到了增强，可以针对特定格式进行更多的配置，包括“微秒”部分是可选的，以及其他几乎所有的部分。

    Column('sometimestamp', sqlite.DATETIME(truncate_microseconds=True))plain
    Column('sometimestamp', sqlite.DATETIME(
                        storage_format=(
                                    "%(year)04d%(month)02d%(day)02d"
                                    "%(hour)02d%(minute)02d%(second)02d%(microsecond)06d"
                        ),
                        regexp="(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{6})"
                        )
                )
    Column('somedate', sqlite.DATE(
                        storage_format="%(month)02d/%(day)02d/%(year)04d",
                        regexp="(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)",
                    )
                )

非常感谢 Nate Dub 在 Pycon 2012 上的冲刺。

也可以看看

[`sqlite.DATETIME`](dialects_sqlite.html#sqlalchemy.dialects.sqlite.DATETIME "sqlalchemy.dialects.sqlite.DATETIME")

[`sqlite.DATE`](dialects_sqlite.html#sqlalchemy.dialects.sqlite.DATE "sqlalchemy.dialects.sqlite.DATE")

[`sqlite.TIME`](dialects_sqlite.html#sqlalchemy.dialects.sqlite.TIME "sqlalchemy.dialects.sqlite.TIME")

[＃2363 T0\>](http://www.sqlalchemy.org/trac/ticket/2363)

### 所有方言都支持“COLLATE”；特别是 MySQL，Postgresql，SQLite [¶](#collate-supported-across-all-dialects-in-particular-mysql-postgresql-sqlite "Permalink to this headline")

The “collate” keyword, long accepted by the MySQL dialect, is now
established on all [`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")
types and will render on any backend, including when features such as
[`MetaData.create_all()`](core_metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
and [`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")
is used:

    >>> stmt = select([cast(sometable.c.somechar, String(20, collation='utf8'))])
    >>> print(stmt)
    SELECT CAST(sometable.somechar AS VARCHAR(20) COLLATE "utf8") AS anon_1
    FROM sometable

也可以看看

[`String`](core_type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")

[＃2276 T0\>](http://www.sqlalchemy.org/trac/ticket/2276)

### “前缀”现在支持[`update()`](core_dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")，[`delete()`](core_dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete") [¶](#prefixes-now-supported-for-update-delete "Permalink to this headline")

面向 MySQL，可以在任何这些结构中呈现“前缀”。例如。：

    stmt = table.delete().prefix_with("LOW_PRIORITY", dialect="mysql")


    stmt = table.update().prefix_with("LOW_PRIORITY", dialect="mysql")

除了那些已经存在于[`insert()`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")，[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")和[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")上的方法之外，该方法是新增的。

也可以看看

[`Update.prefix_with()`](core_dml.html#sqlalchemy.sql.expression.Update.prefix_with "sqlalchemy.sql.expression.Update.prefix_with")

[`Delete.prefix_with()`](core_dml.html#sqlalchemy.sql.expression.Delete.prefix_with "sqlalchemy.sql.expression.Delete.prefix_with")

[`Insert.prefix_with()`](core_dml.html#sqlalchemy.sql.expression.Insert.prefix_with "sqlalchemy.sql.expression.Insert.prefix_with")

[`Select.prefix_with()`](core_selectable.html#sqlalchemy.sql.expression.Select.prefix_with "sqlalchemy.sql.expression.Select.prefix_with")

[`Query.prefix_with()`](orm_query.html#sqlalchemy.orm.query.Query.prefix_with "sqlalchemy.orm.query.Query.prefix_with")

[＃2431 T0\>](http://www.sqlalchemy.org/trac/ticket/2431)

行为改变[¶](#behavioral-changes "Permalink to this headline")
-------------------------------------------------------------

### “待决”对象作为“孤儿”的考虑已经变得更加激进[¶](#the-consideration-of-a-pending-object-as-an-orphan-has-been-made-more-aggressive "Permalink to this headline")

这是 0.8 系列的后期增加，但希望新的行为在更广泛的各种情况下通常更加一致和直观。The
ORM has since at least version 0.4 included behavior such that an object
that’s “pending”, meaning that it’s associated with a [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
but hasn’t been inserted into the database yet, is automatically
expunged from the [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
when it becomes an “orphan”, which means it has been de-associated with
a parent object that refers to it with `delete-orphan` cascade on the configured [`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship").
此行为旨在大致反映持久性（即已插入）对象的行为，其中 ORM 将针对基于拦截事件的孤立成为孤立对象的这些对象发出 DELETE。

对于由多种父项引用的对象（每个对象指定了`delete-orphan`），行为变化都会发挥作用。典型的例子是一个[association
object](orm_basic_relationships.html#association-pattern)，它以多对多的模式连接两种其他类型的对象。以前，行为是这样的，只有在与其父母的*all*关联时，待处理对象才会被清除。随着行为的变化，一旦从*与之前关联的父母的任何*去相关联，待处理对象就被清除。此行为旨在更加紧密地匹配持久对象的行为，持久对象与父对象关联后立即删除。

旧版行为的基本原理至少可以追溯到版本 0.4，并且基本上是一个防御性的决定，当一个对象仍在为 INSERT 构建时，试图减轻混淆。但事实是，只要在任何情况下将对象连接到任何新的父对象，对象就会与[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

如果对象不是首先与那些父母关联，或者如果它已被清除，但随后重新与[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")通过后续的附件事件，但仍未完全关联。在这种情况下，预计数据库会发出完整性错误，因为可能有 NOT
NULL 外键列未被填充。ORM 决定让这些 INSERT 尝试发生，这是基于判断一个对象只是部分与其所需的父对象关联，但与其中一些对象有活动关联的对象，通常不是用户错误，而是故意忽略，应该默默跳过
- 在这里默默地跳过 INSERT 会导致这种性质的用户错误非常难以调试。

通过将 flag `legacy_is_orphan`指定为映射器选项，可以重新为任何[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")启用可能依赖它的应用程序的旧行为。

新的行为允许以下测试用例的工作：

    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(64))

    class UserKeyword(Base):
        __tablename__ = 'user_keyword'
        user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
        keyword_id = Column(Integer, ForeignKey('keyword.id'), primary_key=True)

        user = relationship(User,
                    backref=backref("user_keywords",
                                    cascade="all, delete-orphan")
                )

        keyword = relationship("Keyword",
                    backref=backref("user_keywords",
                                    cascade="all, delete-orphan")
                )

        # uncomment this to enable the old behavior
        # __mapper_args__ = {"legacy_is_orphan": True}

    class Keyword(Base):
        __tablename__ = 'keyword'
        id = Column(Integer, primary_key=True)
        keyword = Column('keyword', String(64))

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    # note we're using Postgresql to ensure that referential integrity
    # is enforced, for demonstration purposes.
    e = create_engine("postgresql://scott:tiger@localhost/test", echo=True)

    Base.metadata.drop_all(e)
    Base.metadata.create_all(e)

    session = Session(e)

    u1 = User(name="u1")
    k1 = Keyword(keyword="k1")

    session.add_all([u1, k1])

    uk1 = UserKeyword(keyword=k1, user=u1)

    # previously, if session.flush() were called here,
    # this operation would succeed, but if session.flush()
    # were not called here, the operation fails with an
    # integrity error.
    # session.flush()
    del u1.user_keywords[0]

    session.commit()

[＃2655 T0\>](http://www.sqlalchemy.org/trac/ticket/2655)

### after\_attach 事件在与会话相关联而不是之前触发后触发； before\_attach添加[¶](#the-after-attach-event-fires-after-the-item-is-associated-with-the-session-instead-of-before-before-attach-added "Permalink to this headline")

使用 after\_attach的事件处理程序现在可以假定给定实例与给定会话关联：

    @event.listens_for(Session, "after_attach")plain
    def after_attach(session, instance):
        assert instance in session

一些用例要求它以这种方式工作。但是，其他用例要求该项目*不是*，而不是会话的一部分，例如，用于加载实例所需状态的查询首先发出自动刷新，否则会过早刷新目标目的。这些用例应该使用新的“before\_attach”事件：

    @event.listens_for(Session, "before_attach")
    def before_attach(session, instance):
        instance.some_necessary_attribute = session.query(Widget).\
                                                filter_by(instance.widget_name).\
                                                first()

[＃2464 T0\>](http://www.sqlalchemy.org/trac/ticket/2464)

### 现在查询自动关联，就像 select()做[¶](#query-now-auto-correlates-like-a-select-does "Permalink to this headline")

以前有必要调用[`Query.correlate()`](orm_query.html#sqlalchemy.orm.query.Query.correlate "sqlalchemy.orm.query.Query.correlate")以使列或 WHERE 子查询与父项相关联：

    subq = session.query(Entity.value).\plainplain
                    filter(Entity.id==Parent.entity_id).\
                    correlate(Parent).\
                    as_scalar()
    session.query(Parent).filter(subq=="some value")

这是一个普通的`select()`构造的相反行为，默认情况下会采用自动关联。0.8 中的上述语句将自动关联：

    subq = session.query(Entity.value).\plain
                    filter(Entity.id==Parent.entity_id).\
                    as_scalar()
    session.query(Parent).filter(subq=="some value")

例如在`select()`中，可以通过调用`query.correlate(None)`来禁用关联，或者通过传递实体`query.correlate(someentity)`

[＃2179 T0\>](http://www.sqlalchemy.org/trac/ticket/2179)

### 相关性现在始终是特定于上下文的[¶](#correlation-is-now-always-context-specific "Permalink to this headline")

To allow a wider variety of correlation scenarios, the behavior of
[`Select.correlate()`](core_selectable.html#sqlalchemy.sql.expression.Select.correlate "sqlalchemy.sql.expression.Select.correlate")
and [`Query.correlate()`](orm_query.html#sqlalchemy.orm.query.Query.correlate "sqlalchemy.orm.query.Query.correlate")
has changed slightly such that the SELECT statement will omit the
“correlated” target from the FROM clause only if the statement is
actually used in that context.
另外，在封闭的 SELECT 语句中作为 FROM 放置的 SELECT 语句不再可能“关联”（即省略）FROM 子句。

这种改变只会使渲染 SQL 变得更好，因为在相对于所选内容的 FROM 对象不足的情况下，不再可能渲染非法 SQL：

    from sqlalchemy.sql import table, column, selectplain

    t1 = table('t1', column('x'))
    t2 = table('t2', column('y'))
    s = select([t1, t2]).correlate(t1)

    print(s)

在此更改之前，上述内容将返回：

    SELECT t1.x, t2.y FROM t2plain

这是无效的 SQL，因为“t1”在任何 FROM 子句中都没有引用。

现在，在没有包含 SELECT 的情况下，它会返回：

    SELECT t1.x, t2.y FROM t1, t2

在 SELECT 中，相关按预期生效：

    s2 = select([t1, t2]).where(t1.c.x == t2.c.y).where(t1.c.x == s)

    print(s2)

    SELECT t1.x, t2.y FROM t1, t2
    WHERE t1.x = t2.y AND t1.x =
        (SELECT t1.x, t2.y FROM t2)

预期此更改不会影响任何现有的应用程序，因为相关行为对于正确构建的表达式而言仍然相同。只有在测试场景中依赖于非相关上下文中使用的相关 SELECT 的无效字符串输出的应用程序才会看到任何更改。

[＃2668 T0\>](http://www.sqlalchemy.org/trac/ticket/2668)

### 现在，create\_all()和 drop\_all()将授予一个空列表[¶](#create-all-and-drop-all-will-now-honor-an-empty-list-as-such "Permalink to this headline")

现在，方法[`MetaData.create_all()`](core_metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")和[`MetaData.drop_all()`](core_metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")将接受[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的列表，这些对象是空的，并且不会发出任何 CREATE 或 DROP 语句。以前，一个空的列表与为集合传递`None`相同，并且无条件地为所有项目发出 CREATE / DROP。

这是一个错误修复，但某些应用程序可能依赖于以前的行为。

[＃2664 T0\>](http://www.sqlalchemy.org/trac/ticket/2664)

### 修复了[`InstrumentationEvents`](orm_events.html#sqlalchemy.orm.events.InstrumentationEvents "sqlalchemy.orm.events.InstrumentationEvents") [¶](#repaired-the-event-targeting-of-instrumentationevents "Permalink to this headline")

The [`InstrumentationEvents`](orm_events.html#sqlalchemy.orm.events.InstrumentationEvents "sqlalchemy.orm.events.InstrumentationEvents")
series of event targets have documented that the events will only be
fired off according to the actual class passed as a target.
通过 0.7，情况并非如此，任何适用于[`InstrumentationEvents`](orm_events.html#sqlalchemy.orm.events.InstrumentationEvents "sqlalchemy.orm.events.InstrumentationEvents")的事件侦听器都将被映射的所有类调用。在0.8中，增加了额外的逻辑，以便事件只会调用那些发送的类。默认情况下，`propagate`标志默认设置为`True`，因为类工具事件通常用于拦截尚未创建的类。

[＃2590 T0\>](http://www.sqlalchemy.org/trac/ticket/2590)

### 与 MS-SQL 中的子查询进行比较时，不再需要对 IN 进行“=”的魔术强化[¶](#no-more-magic-coercion-of-to-in-when-comparing-to-subquery-in-ms-sql "Permalink to this headline")

我们在 MSSQL 方言中发现了一个非常古老的行为，它会在尝试像这样做时尝试从用户身上抢救用户：

    scalar_subq = select([someothertable.c.id]).where(someothertable.c.data=='foo')
    select([sometable]).where(sometable.c.id==scalar_subq)

SQL Server 不允许与标量 SELECT 进行等同比较，即“x =（SELECT
something）”。MSSQL 方言会将其转换为 IN。然而，像“（SELECT something）=
x”这样的比较会发生同样的事情，总的来说，这种猜测级别超出了 SQLAlchemy 的通常范围，因此行为被删除。

[＃2277 T0\>](http://www.sqlalchemy.org/trac/ticket/2277)

### 修正了[`Session.is_modified()`](orm_session_api.html#sqlalchemy.orm.session.Session.is_modified "sqlalchemy.orm.session.Session.is_modified") [¶](#fixed-the-behavior-of-session-is-modified "Permalink to this headline")

[`Session.is_modified()`](orm_session_api.html#sqlalchemy.orm.session.Session.is_modified "sqlalchemy.orm.session.Session.is_modified")方法接受一个参数`passive`，这基本上不是必须的，参数在所有情况下都应该是`True`当它保留默认的`False`时，它会触及数据库，并经常触发 autoflush，它本身会改变结果。在 0.8 中，`passive`参数将不起作用，并且未加载的属性将永远不会被检查历史记录，因为根据定义，未加载的属性可能没有挂起的状态更改。

也可以看看

[`Session.is_modified()`](orm_session_api.html#sqlalchemy.orm.session.Session.is_modified "sqlalchemy.orm.session.Session.is_modified")

[＃2320 T0\>](http://www.sqlalchemy.org/trac/ticket/2320)

### `Column.key` is honored in the [`Select.c`](core_selectable.html#sqlalchemy.sql.expression.Select.c "sqlalchemy.sql.expression.Select.c") attribute of [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select") with [`Select.apply_labels()`](core_selectable.html#sqlalchemy.sql.expression.Select.apply_labels "sqlalchemy.sql.expression.Select.apply_labels")[¶](#column-key-is-honored-in-the-select-c-attribute-of-select-with-select-apply-labels "Permalink to this headline")

表达式系统的用户知道[`Select.apply_labels()`](core_selectable.html#sqlalchemy.sql.expression.Select.apply_labels "sqlalchemy.sql.expression.Select.apply_labels")为每个列名添加表名，影响[`Select.c`](core_selectable.html#sqlalchemy.sql.expression.Select.c "sqlalchemy.sql.expression.Select.c")中可用的名称：

    s = select([table1]).apply_labels()plain
    s.c.table1_col1
    s.c.table1_col2

在 0.8 之前，如果[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")具有不同的`Column.key`，则此键将被忽略，与[`Select.apply_labels()`](core_selectable.html#sqlalchemy.sql.expression.Select.apply_labels "sqlalchemy.sql.expression.Select.apply_labels")不一致用过的：

    # before 0.8
    table1 = Table('t1', metadata,
        Column('col1', Integer, key='column_one')
    )
    s = select([table1])
    s.c.column_one # would be accessible like this
    s.c.col1 # would raise AttributeError

    s = select([table1]).apply_labels()
    s.c.table1_column_one # would raise AttributeError
    s.c.table1_col1 # would be accessible like this

In 0.8, `Column.key` is honored
in both cases:

    # with 0.8plain
    table1 = Table('t1', metadata,
        Column('col1', Integer, key='column_one')
    )
    s = select([table1])
    s.c.column_one # works
    s.c.col1 # AttributeError

    s = select([table1]).apply_labels()
    s.c.table1_column_one # works
    s.c.table1_col1 # AttributeError

关于“name”和“key”的所有其他行为是相同的，包括呈现的 SQL 仍将使用`<tablename>_<colname>`形式 - 这里强调了防止`Column.key`内容被呈现到`SELECT`语句中，因此`Column.key`中使用的特殊/非 ascii 字符没有问题。

[＃2397 T0\>](http://www.sqlalchemy.org/trac/ticket/2397)

### single\_parent 警告现在是一个错误[¶](#single-parent-warning-is-now-an-error "Permalink to this headline")

一个[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")是多对一或多对多的，并且指定了“cascade
='all，delete-orphan'”，这是一个尴尬但仍然受支持的用例（限制）如果关系没有指定`single_parent=True`选项，现在会引发错误。以前它只会发出警告，但在任何情况下都会在属性系统中立即出现故障。

[＃2405 T0\>](http://www.sqlalchemy.org/trac/ticket/2405)

### 将`inspector`参数添加到`column_reflect`事件[¶](#adding-the-inspector-argument-to-the-column-reflect-event "Permalink to this headline")

0.7 添加了一个名为`column_reflect`的新事件，这样可以反映出列的反射，因为每个列都反映出来。我们得到这个事件有点不对，因为事件没有办法获取用于反射的当前`Inspector`和`Connection`，在来自数据库的附加信息的情况下是必要的。由于这是一个尚未广泛使用的新事件，因此我们将直接向其中添加`inspector`参数：

    @event.listens_for(Table, "column_reflect")plain
    def listen_for_col(inspector, table, column_info):
        # ...

[＃2418 T0\>](http://www.sqlalchemy.org/trac/ticket/2418)

### 禁用排序规则的自动检测，MySQL 的套管[¶](#disabling-auto-detect-of-collations-casing-for-mysql "Permalink to this headline")

MySQL 方言执行两个调用，一个是非常昂贵的，用于从数据库加载所有可能的排序规则以及第一次`Engine`连接时的套管信息。这些集合都不用于任何 SQLAlchemy 函数，因此这些调用将被更改为不再自动发射。可能依赖这些集合的应用程序存在于`engine.dialect`上，需要直接调用`_detect_collations()`和`_detect_casing()`。

[＃2404 T0\>](http://www.sqlalchemy.org/trac/ticket/2404)

### “Unconsumed column names” warning becomes an exception[¶](#unconsumed-column-names-warning-becomes-an-exception "Permalink to this headline")

引用`insert()`或`update()`构造中不存在的列会引发错误而不是警告：

    t1 = table('t1', column('x'))plainplainplain
    t1.insert().values(x=5, z=5) # raises "Unconsumed column names: z"

[＃2415 T0\>](http://www.sqlalchemy.org/trac/ticket/2415)

### Inspector.get\_primary\_keys()已弃用，请使用 Inspector.get\_pk\_constraint [¶](#inspector-get-primary-keys-is-deprecated-use-inspector-get-pk-constraint "Permalink to this headline")

`Inspector`上的这两个方法是多余的，其中`get_primary_keys()`将返回与`get_pk_constraint()`相同的信息减去约束的名称：

    >>> insp.get_primary_keys()
    ["a", "b"]

    >>> insp.get_pk_constraint()
    {"name":"pk_constraint", "constrained_columns":["a", "b"]}

[＃2422 T0\>](http://www.sqlalchemy.org/trac/ticket/2422)

### 在大多数情况下，不区分大小写的结果行名称将被禁用[¶](#case-insensitive-result-row-names-will-be-disabled-in-most-cases "Permalink to this headline")

一个非常古老的行为，`RowProxy`中的列名始终不区分大小写：

    >>> row = result.fetchone()plain
    >>> row['foo'] == row['FOO'] == row['Foo']
    True

这是为了一些早期需要的方言的好处，如 Oracle 和 Firebird，但在现代用法中，我们有更准确的方法来处理这两个平台的不区分大小写的行为。

展望未来，只有通过将标志`case_sensitive=False`传递给`create_engine()`，此行为才可用，但否则必须从行中请求列名尽可能匹配套管。

[＃2423 T0\>](http://www.sqlalchemy.org/trac/ticket/2423)

### `InstrumentationManager` and alternate class instrumentation is now an extension[¶](#instrumentationmanager-and-alternate-class-instrumentation-is-now-an-extension "Permalink to this headline")

`sqlalchemy.orm.interfaces.InstrumentationManager`类将移至`sqlalchemy.ext.instrumentation.InstrumentationManager`。“替代仪表”系统是为了需要与现有或不寻常的类仪器系统一起工作的极少数安装而建立的，并且通常很少使用。该系统的复杂性已被导出到`ext.`模块。It remains unused until once imported, typically when a
third party library imports `InstrumentationManager`, at which point it is injected back into
`sqlalchemy.orm` by replacing the default
`InstrumentationFactory` with
`ExtendedInstrumentationRegistry`.

除去[¶ T0\>](#removed "Permalink to this headline")
---------------------------------------------------

### SQLSoup [¶ T0\>](#sqlsoup "Permalink to this headline")

SQLSoup 是一个方便的包，它在 SQLAlchemy
ORM 之上提供了一个替代接口。SQLSoup 现在被移植到自己的项目中，并单独记录/发布；请参阅[https://bitbucket.org/zzzeek/sqlsoup](https://bitbucket.org/zzzeek/sqlsoup)。

SQLSoup 是一个非常简单的工具，可以从对其使用风格感兴趣的贡献者中受益。

[＃2262 T0\>](http://www.sqlalchemy.org/trac/ticket/2262)

### MutableType [¶ T0\>](#mutabletype "Permalink to this headline")

SQLAlchemy ORM 中旧的“可变”系统已被删除。这指的是`MutableType`接口，该接口已应用于`PickleType`等类型并有条件地应用于`TypeDecorator`，并且由于很早的 SQLAlchemy 版本提供了一种方式为 ORM 检测所谓的“可变”数据结构（如 JSON 结构和腌渍对象）的变化。然而，实施从来都不合理，并且迫使工作单元使用效率非常低的模式，这导致在冲洗期间对所有对象进行昂贵的扫描。在 0.7 中引入了[sqlalchemy.ext.mutable](http://docs.sqlalchemy.org/en/latest/orm_extensions_mutable.html)扩展，以便在发生更改时用户定义的数据类型可以将事件适当地发送到工作单元。

今天，`MutableType`的使用量预计会很低，因为其效率低下已经有几年了。

[＃2442 T0\>](http://www.sqlalchemy.org/trac/ticket/2442)

### sqlalchemy.exceptions（多年来一直是 sqlalchemy.exc）[¶](#sqlalchemy-exceptions-has-been-sqlalchemy-exc-for-years "Permalink to this headline")

我们留下了一个别名`sqlalchemy.exceptions`，试图使一些尚未升级到使用`sqlalchemy.exc`的非常旧的库变得更容易一些。但有些用户仍然对它感到困惑，所以在 0.8 版本中，我们正在彻底消除这种混淆。

[＃2433 T0\>](http://www.sqlalchemy.org/trac/ticket/2433)
