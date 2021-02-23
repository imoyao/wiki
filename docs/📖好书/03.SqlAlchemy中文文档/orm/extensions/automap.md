---
title: automap
date: 2021-02-20 22:41:41
permalink: /pages/0b473a/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
  - extensions
tags:
  - 
---
自动地图[¶ T0\>](#module-sqlalchemy.ext.automap "Permalink to this headline")
=============================================================================

定义对[`sqlalchemy.ext.declarative`](declarative_api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")系统的扩展，该系统自动从数据库模式生成映射类和关系，但通常不一定反映出来。

版本0.9.1新增：添加了[`sqlalchemy.ext.automap`](#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")。

It is hoped that the [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
system provides a quick and modernized solution to the problem that the
very famous [SQLSoup](https://sqlsoup.readthedocs.io/en/latest/) also
tries to solve, that of generating a quick and rudimentary object model
from an existing database on the fly. By addressing the issue strictly
at the mapper configuration level, and integrating fully with existing
Declarative class techniques, [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
seeks to provide a well-integrated approach to the issue of expediently
auto-generating ad-hoc mappings.

基本使用[¶](#basic-use "Permalink to this headline")
----------------------------------------------------

最简单的用法是将现有数据库反映到新模型中。我们使用[`automap_base()`](#sqlalchemy.ext.automap.automap_base "sqlalchemy.ext.automap.automap_base")创建一个新的[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")类，类似于我们如何创建声明性基类。然后，我们在生成的基类上调用[`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")，要求它反映模式并生成映射：

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine

    Base = automap_base()

    # engine, suppose it has two tables 'user' and 'address' set up
    engine = create_engine("sqlite:///mydatabase.db")

    # reflect the tables
    Base.prepare(engine, reflect=True)

    # mapped classes are now created with names by default
    # matching that of the table name.
    User = Base.classes.user
    Address = Base.classes.address

    session = Session(engine)

    # rudimentary relationships are produced
    session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
    session.commit()

    # collection-based relationships are by default named
    # "<classname>_collection"
    print (u1.address_collection)

Above, calling [`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")
while passing along the [`AutomapBase.prepare.reflect`(#sqlalchemy.ext.automap.AutomapBase.prepare.params.reflect "sqlalchemy.ext.automap.AutomapBase.prepare")
parameter indicates that the [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
method will be called on this declarative base classes’
[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
collection; then, each **viable** [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
within the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
will get a new mapped class generated automatically.
将各种表链接在一起的[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象将用于在类之间生成新的，双向的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")对象。类和关系沿着我们可以定制的默认命名方案进行。此时，由相关的`User`和`Address`类组成的基本映射已准备好以传统方式使用。

注意

通过**可行**，我们的意思是，对于要映射的表，它必须指定一个主键。此外，如果该表被检测为两个其他表之间的纯关联表，则该表不会被直接映射，而是会被配置为两个引用表的映射之间的多对多表。

从现有元数据生成映射[¶](#generating-mappings-from-an-existing-metadata "Permalink to this headline")
----------------------------------------------------------------------------------------------------

我们可以将预先声明的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象传递给[`automap_base()`](#sqlalchemy.ext.automap.automap_base "sqlalchemy.ext.automap.automap_base")。这个对象可以以任何方式构造，包括以编程方式，从序列化的文件中，或从使用[`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")反映的本身。下面我们举例说明反射和显式表声明的组合：

    from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
    engine = create_engine("sqlite:///mydatabase.db")

    # produce our own MetaData object
    metadata = MetaData()

    # we can reflect it ourselves from a database, using options
    # such as 'only' to limit what tables we look at...
    metadata.reflect(engine, only=['user', 'address'])

    # ... or just define our own Table objects with it (or combine both)
    Table('user_order', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('user_id', ForeignKey('user.id'))
                )

    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare()

    # mapped classes are ready
    User, Address, Order = Base.classes.user, Base.classes.address,        Base.classes.user_order

明确指定类[¶](#specifying-classes-explicitly "Permalink to this headline")
--------------------------------------------------------------------------

[`sqlalchemy.ext.automap`](#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")扩展允许类以类似于[`DeferredReflection`](declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")类的方式显式定义。从[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")扩展的类与常规声明类相似，但在构建之后不会立即映射，而是在调用[`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")时映射。The
[`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")
method will make use of the classes we’ve established based on the table
name we use. 如果我们的模式包含表`user`和`address`，我们可以定义一个或两个要使用的类：

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    # automap base
    Base = automap_base()

    # pre-declare User for the 'user' table
    class User(Base):
        __tablename__ = 'user'

        # override schema elements like Columns
        user_name = Column('name', String)

        # override relationships too, if desired.
        # we must use the same name that automap would use for the
        # relationship, and also must refer to the class name that automap will
        # generate for "address"
        address_collection = relationship("address", collection_class=set)

    # reflect
    engine = create_engine("sqlite:///mydatabase.db")
    Base.prepare(engine, reflect=True)

    # we still have Address generated from the tablename "address",
    # but User is the same as Base.classes.User now

    Address = Base.classes.address

    u1 = session.query(User).first()
    print (u1.address_collection)

    # the backref is still there:
    a1 = session.query(Address).first()
    print (a1.user)

以上，其中一个更复杂的细节是，我们说明了覆盖automap将创建的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")对象之一。为此，我们需要确保名称与automap通常会生成的名称相匹配，因为从automap的角度来看，关系名称将是`User.address_collection`和引用的类名称，被称为`address`，即使我们在我们使用这个类时将它称为`Address`。

重写命名方案[¶](#overriding-naming-schemes "Permalink to this headline")
------------------------------------------------------------------------

[`sqlalchemy.ext.automap`](#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap") is
tasked with producing mapped classes and relationship names based on a
schema, which means it has decision points in how these names are
determined. These three decision points are provided using functions
which can be passed to the [`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")
method, and are known as [`classname_for_table()`](#sqlalchemy.ext.automap.classname_for_table "sqlalchemy.ext.automap.classname_for_table"),
[`name_for_scalar_relationship()`](#sqlalchemy.ext.automap.name_for_scalar_relationship "sqlalchemy.ext.automap.name_for_scalar_relationship"),
and [`name_for_collection_relationship()`](#sqlalchemy.ext.automap.name_for_collection_relationship "sqlalchemy.ext.automap.name_for_collection_relationship").
这些函数中的任何一个或所有函数都是在下面的例子中提供的，我们使用[Inflect](https://pypi.python.org/pypi/inflect)包使用类名的“camel
case”方案和集合名称的“pluralizer”：

    import re
    import inflect

    def camelize_classname(base, tablename, table):
        "Produce a 'camelized' class name, e.g. "
        "'words_and_underscores' -> 'WordsAndUnderscores'"

        return str(tablename[0].upper() + \
                re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))

    _pluralizer = inflect.engine()
    def pluralize_collection(base, local_cls, referred_cls, constraint):
        "Produce an 'uncamelized', 'pluralized' class name, e.g. "
        "'SomeTerm' -> 'some_terms'"

        referred_name = referred_cls.__name__
        uncamelized = re.sub(r'[A-Z]',
                             lambda m: "_%s" % m.group(0).lower(),
                             referred_name)[1:]
        pluralized = _pluralizer.plural(uncamelized)
        return pluralized

    from sqlalchemy.ext.automap import automap_base

    Base = automap_base()

    engine = create_engine("sqlite:///mydatabase.db")

    Base.prepare(engine, reflect=True,
                classname_for_table=camelize_classname,
                name_for_collection_relationship=pluralize_collection
        )

从上面的映射中，我们现在将有`User`和`Address`的类，其中`User`到`Address`的集合是称为`User.addresses`：

    User, Address = Base.classes.User, Base.classes.Address

    u1 = User(addresses=[Address(email="foo@bar.com")])

关系检测[¶](#relationship-detection "Permalink to this headline")
-----------------------------------------------------------------

绝大多数automap完成的是基于外键的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构的生成。这对于多对一和一对多关系有效的机制如下：

1.  已知映射到特定类的给定[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")会针对[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象进行检查。

2.  从每个[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")，存在的远程[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象与其映射到的类匹配（如果有的话），否则它将被跳过。

3.  正如我们正在检查的[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对应于来自直接映射类的引用，该关系将被设置为指向所引用的类的多对一；将在涉及这个类的引用类上创建相应的一对多后向参考。

4.  If any of the columns that are part of the
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    are not nullable (e.g. `nullable=False`), a
    [`cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")
    keyword argument of `all, delete-orphan` will be
    added to the keyword arguments to be passed to the relationship or
    backref. If the [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    reports that [`ForeignKeyConstraint.ondelete`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.ondelete "sqlalchemy.schema.ForeignKeyConstraint")
    is set to `CASCADE` for a not null or
    `SET NULL` for a nullable set of columns, the
    option [`passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")
    flag is set to `True` in the set of relationship
    keyword arguments. 请注意，并非所有后端都支持ON DELETE的反射。

    版本1.0.0中的新功能： -
    当生成一对多关系并建立默认级联`all时，automap将检测不可为空的外键约束， t2 > delete-orphan`如果是的话；此外，如果约束指定`CASCADE`的[`ForeignKeyConstraint.ondelete`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.ondelete "sqlalchemy.schema.ForeignKeyConstraint")为非空或`SET  tt> NULL / t9>表示可空列，还添加passive_deletes=True`选项。

5.  关系的名称是使用[`AutomapBase.prepare.name_for_scalar_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_scalar_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")和[`AutomapBase.prepare.name_for_collection_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_collection_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")可调用函数确定的。需要注意的是，默认关系命名从**实际类名称**派生名称。如果您通过声明某个特定类的明确名称，或者指定了一个备用类命名方案，那么这就是从中派生关系名称的名称。

6.  检查这些类是否存在与这些名称匹配的现有映射属性。If one is detected
    on one side, but none on the other side, [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
    attempts to create a relationship on the missing side, then uses the
    [`relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")
    parameter in order to point the new relationship to the other side.

7.  In the usual case where no relationship is on either side,
    [`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")
    produces a [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    on the “many-to-one” side and matches it to the other using the
    [`relationship.backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")
    parameter.

8.  Production of the [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    and optionally the [`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")
    is handed off to the
    [`AutomapBase.prepare.generate_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")
    function, which can be supplied by the end-user in order to augment
    the arguments passed to [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    or [`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")
    or to make use of custom implementations of these functions.

### 自定义关系参数[¶](#custom-relationship-arguments "Permalink to this headline")

[`AutomapBase.prepare.generate_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")挂钩可用于向关系添加参数。在大多数情况下，我们可以使用现有的[`automap.generate_relationship()`](#sqlalchemy.ext.automap.generate_relationship "sqlalchemy.ext.automap.generate_relationship")函数在用给定的关键字字典增加自己的参数后返回对象。

下面是如何将[`relationship.cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")和[`relationship.passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")选项发送到所有一对多关系的说明：

    from sqlalchemy.ext.automap import generate_relationship

    def _gen_relationship(base, direction, return_fn,
                                    attrname, local_cls, referred_cls, **kw):
        if direction is interfaces.ONETOMANY:
            kw['cascade'] = 'all, delete-orphan'
            kw['passive_deletes'] = True
        # make use of the built-in function to actually return
        # the result.
        return generate_relationship(base, direction, return_fn,
                                     attrname, local_cls, referred_cls, **kw)

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    # automap base
    Base = automap_base()

    engine = create_engine("sqlite:///mydatabase.db")
    Base.prepare(engine, reflect=True,
                generate_relationship=_gen_relationship)

### 多对多关系[¶](#many-to-many-relationships "Permalink to this headline")

[`sqlalchemy.ext.automap`](#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap") will
generate many-to-many relationships, e.g. those which contain a
`secondary` argument. 生产这些产品的过程如下：

1.  在任何已映射的类已被分配给它之前，为[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象检查给定的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。
2.  If the table contains two and exactly two
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    objects, and all columns within this table are members of these two
    [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    objects, the table is assumed to be a “secondary” table, and will
    **not be mapped directly**.
3.  如果有的话，[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")指向的两个（或一个，用于自引用）外部表与它们将要映射到的类相匹配。
4.  如果两侧的映射类已经定位，则在这两个类之间创建一个多对多双向[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
    / [`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")对。
5.  多对多的覆盖逻辑与一对多/多对一的覆盖逻辑相同；将调用[`generate_relationship()`](#sqlalchemy.ext.automap.generate_relationship "sqlalchemy.ext.automap.generate_relationship")函数来生成结构，并保留现有的属性。

### 与继承的关系[¶](#relationships-with-inheritance "Permalink to this headline")

[`sqlalchemy.ext.automap`](#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")不会在两个处于继承关系的类之间生成任何关系。也就是说，有两个等级给出如下：

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        type = Column(String(50))
        __mapper_args__ = {
             'polymorphic_identity':'employee', 'polymorphic_on': type
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        __mapper_args__ = {
            'polymorphic_identity':'engineer',
        }

从`Engineer`到`Employee`的外键不是用于关系，而是用于在两个类之间建立连接的继承。

请注意，这意味着automap不会为从子类链接到超类的外键生成*任何*关系。如果映射具有从子类到超类的实际关系，那么这些映射需要是明确的。下面，我们有两个独立的从`Engineer`到`Employee`的外键，我们需要设置我们想要的关系以及`inherit_condition` ，因为这些不是SQLAlchemy可以猜测的东西：

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        type = Column(String(50))

        __mapper_args__ = {
            'polymorphic_identity':'employee', 'polymorphic_on':type
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        favorite_employee_id = Column(Integer, ForeignKey('employee.id'))

        favorite_employee = relationship(Employee,
                                         foreign_keys=favorite_employee_id)

        __mapper_args__ = {
            'polymorphic_identity':'engineer',
            'inherit_condition': id == Employee.id
        }

### 处理简单的命名冲突[¶](#handling-simple-naming-conflicts "Permalink to this headline")

在映射过程中命名冲突的情况下，根据需要覆盖[`classname_for_table()`](#sqlalchemy.ext.automap.classname_for_table "sqlalchemy.ext.automap.classname_for_table")，[`name_for_scalar_relationship()`](#sqlalchemy.ext.automap.name_for_scalar_relationship "sqlalchemy.ext.automap.name_for_scalar_relationship")和[`name_for_collection_relationship()`](#sqlalchemy.ext.automap.name_for_collection_relationship "sqlalchemy.ext.automap.name_for_collection_relationship")中的任何一个。例如，如果automap试图命名与现有列相同的多对一关系，则可以有条件地选择替代约定。给定一个模式：

    CREATE TABLE table_a (
        id INTEGER PRIMARY KEY
    );

    CREATE TABLE table_b (
        id INTEGER PRIMARY KEY,
        table_a INTEGER,
        FOREIGN KEY(table_a) REFERENCES table_a(id)
    );

上述模式将首先将`table_a`表自动映射为名为`table_a`的类；它会自动将关系映射到`table_b`的类上，其名称与此相关的类相同。 `table_a`该关系名称与映射列`table_b.table_a`冲突，并且将在映射时发出错误。

我们可以通过使用下划线来解决这个冲突，如下所示：

    def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
        name = referred_cls.__name__.lower()
        local_table = local_cls.__table__
        if name in local_table.columns:
            newname = name + "_"
            warnings.warn(
                "Already detected name %s present.  using %s" %
                (name, newname))
            return newname
        return name


    Base.prepare(engine, reflect=True,
        name_for_scalar_relationship=name_for_scalar_relationship)

或者，我们可以更改列侧的名称。被映射的列可以使用[Naming Columns
Distinctly from Attribute
Names](mapping_columns.html#mapper-column-distinct-names)区别命名列的方法修改，通过将列明确分配给新名称：

    Base = automap_base()

    class TableB(Base):
        __tablename__ = 'table_b'
        _table_a = Column('table_a', ForeignKey('table_a.id'))

    Base.prepare(engine, reflect=True)

将Automap与显式声明一起使用[¶](#using-automap-with-explicit-declarations "Permalink to this headline")
------------------------------------------------------------------------------------------------------

如前所述，automap不依赖于反射，并且可以使用[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")集合中任何[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的集合。由此可见，automap也可以用于生成缺失的关系，给出一个完全定义表元数据的完整模型：

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import Column, Integer, String, ForeignKey

    Base = automap_base()

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String)

    class Address(Base):
        __tablename__ = 'address'

        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(ForeignKey('user.id'))

    # produce relationships
    Base.prepare()

    # mapping is complete, with "address_collection" and
    # "user" relationships
    a1 = Address(email='u1')
    a2 = Address(email='u2')
    u1 = User(address_collection=[a1, a2])
    assert a1.user is u1

Above, given mostly complete `User` and
`Address` mappings, the [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
which we defined on `Address.user_id` allowed a
bidirectional relationship pair `Address.user` and
`User.address_collection` to be generated on the
mapped classes.

请注意，当继承[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")时，需要使用[`AutomapBase.prepare()`](#sqlalchemy.ext.automap.AutomapBase.prepare "sqlalchemy.ext.automap.AutomapBase.prepare")方法；如果未调用，则我们声明的类处于未映射状态。

API参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

 `sqlalchemy.ext.automap.`{.descclassname}`automap_base`{.descname}(*declarative\_base=None*, *\*\*kw*)[¶](#sqlalchemy.ext.automap.automap_base "Permalink to this definition")
:   生成声明式自动映射基础。

    该函数生成一个新的基类，它是[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")类的产物，也是[`declarative.declarative_base()`](declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")生成的声明基。

    除`declarative_base`以外的所有参数都是直接传递给[`declarative.declarative_base()`](declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")函数的关键字参数。

    参数：

    -   **declarative\_base**[¶](#sqlalchemy.ext.automap.automap_base.params.declarative_base)
        – an existing class produced by
        [`declarative.declarative_base()`](declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base").
        当它被传递时，函数本身不再调用[`declarative.declarative_base()`](declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")，所有其他关键字参数都被忽略。
    -   **\*\*kw**[¶](#sqlalchemy.ext.automap.automap_base.params.**kw)
        – keyword arguments are passed along to
        [`declarative.declarative_base()`](declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base").

*class* `sqlalchemy.ext.automap。`{.descclassname} `AutomapBase`{.descname} [¶](#sqlalchemy.ext.automap.AutomapBase "Permalink to this definition")
:   “自动映射”模式的基类。

    可以将[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")类与由[`declarative.declarative_base()`](declarative_api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")函数生成的“声明性基本”类进行比较。在实践中，[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")类总是作为一个mixin与一个实际的声明基础一起使用。

    通常使用[`automap_base()`](#sqlalchemy.ext.automap.automap_base "sqlalchemy.ext.automap.automap_base")函数即时创建一个新的子类化的[`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")。

    也可以看看

    [Automap](#)

    `类`{.descname} *=无* [¶](#sqlalchemy.ext.automap.AutomapBase.classes "Permalink to this definition")
    :   包含类的`util.Properties`的实例。

        该对象的行为与表上的`.c`集合非常相似。类以它们的名称存在，例如：

            Base = automap_base()
            Base.prepare(engine=some_engine, reflect=True)

            User, Address = Base.classes.User, Base.classes.Address

     *classmethod*`prepare`{.descname}(*engine=None*, *reflect=False*, *schema=None*, *classname\_for\_table=\<function classname\_for\_table\>*, *collection\_class=\<type 'list'\>*, *name\_for\_scalar\_relationship=\<function name\_for\_scalar\_relationship\>*, *name\_for\_collection\_relationship=\<function name\_for\_collection\_relationship\>*, *generate\_relationship=\<function generate\_relationship\>*)[¶](#sqlalchemy.ext.automap.AutomapBase.prepare "Permalink to this definition")
    :   从[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")中提取映射的类和关系并执行映射。

        参数：

        -   **engine**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.engine)
            – an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            or [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            with which to perform schema reflection, if specified.
            如果[`AutomapBase.prepare.reflect`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.reflect "sqlalchemy.ext.automap.AutomapBase.prepare")参数为False，则不使用此对象。
        -   **reflect**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.reflect)
            – if True, the [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")
            method is called on the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
            associated with this [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase").
            The [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            passed via [`AutomapBase.prepare.engine`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.engine "sqlalchemy.ext.automap.AutomapBase.prepare")
            will be used to perform the reflection if present; else, the
            [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
            should already be bound to some engine else the operation
            will fail.
        -   **classname\_for\_table**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.classname_for_table)
            – callable function which will be used to produce new class
            names, given a table name.
            默认为[`classname_for_table()`](#sqlalchemy.ext.automap.classname_for_table "sqlalchemy.ext.automap.classname_for_table")。
        -   **name\_for\_scalar\_relationship**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_scalar_relationship)
            – callable function which will be used to produce
            relationship names for scalar relationships.
            默认为[`name_for_scalar_relationship()`](#sqlalchemy.ext.automap.name_for_scalar_relationship "sqlalchemy.ext.automap.name_for_scalar_relationship")。
        -   **name\_for\_collection\_relationship**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_collection_relationship)
            – callable function which will be used to produce
            relationship names for collection-oriented relationships.
            默认为[`name_for_collection_relationship()`](#sqlalchemy.ext.automap.name_for_collection_relationship "sqlalchemy.ext.automap.name_for_collection_relationship")。
        -   **generate\_relationship**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship)
            – callable function which will be used to actually generate
            [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
            and [`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")
            constructs. 默认为[`generate_relationship()`](#sqlalchemy.ext.automap.generate_relationship "sqlalchemy.ext.automap.generate_relationship")。
        -   **collection\_class**[¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.collection_class)
            – the Python collection class that will be used when a new
            [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
            object is created that represents a collection.
            默认为`list`。
        -   **模式**
            [¶](#sqlalchemy.ext.automap.AutomapBase.prepare.params.schema)
            -

            当与[`AutomapBase.prepare.reflect`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.reflect "sqlalchemy.ext.automap.AutomapBase.prepare")标志一起出现时，将传递给[`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")以指示表应该从哪里反映出来的主模式。省略时，将使用由数据库连接使用的默认模式。

            版本1.1中的新功能

 `sqlalchemy.ext.automap.`{.descclassname}`classname_for_table`{.descname}(*base*, *tablename*, *table*)[¶](#sqlalchemy.ext.automap.classname_for_table "Permalink to this definition")
:   给定表名称，返回应该使用的类名称。

    默认的实现是：

        return str(tablename)

    可以使用[`AutomapBase.prepare.classname_for_table`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.classname_for_table "sqlalchemy.ext.automap.AutomapBase.prepare")参数指定替代实现。

    参数：

    -   **base**[¶](#sqlalchemy.ext.automap.classname_for_table.params.base)
        – the [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
        class doing the prepare.
    -   **tablename**[¶](#sqlalchemy.ext.automap.classname_for_table.params.tablename)
        – string name of the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").
    -   **table**[¶](#sqlalchemy.ext.automap.classname_for_table.params.table)
        – the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        object itself.

    返回：

    一个字符串类的名字。

    注意

    在Python
    2中，用于类名**的字符串必须是**非Unicode对象，例如一个`str()`对象。[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的`.name`属性通常是一个Python
    unicode子类，所以在计算后应该将`str()`函数应用于该名称任何非ASCII字符。

 `sqlalchemy.ext.automap.`{.descclassname}`name_for_scalar_relationship`{.descname}(*base*, *local\_cls*, *referred\_cls*, *constraint*)[¶](#sqlalchemy.ext.automap.name_for_scalar_relationship "Permalink to this definition")
:   对于标量对象引用，返回应该用于从一个类引用到另一个类的属性名称。

    默认的实现是：

        return referred_cls.__name__.lower()

    可以使用[`AutomapBase.prepare.name_for_scalar_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_scalar_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")参数指定替代实现。

    参数：

    -   **base**[¶](#sqlalchemy.ext.automap.name_for_scalar_relationship.params.base)
        – the [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
        class doing the prepare.
    -   **local\_cls**
        [¶](#sqlalchemy.ext.automap.name_for_scalar_relationship.params.local_cls)
        - 要在本地映射的类。
    -   **referenced\_cls**
        [¶](#sqlalchemy.ext.automap.name_for_scalar_relationship.params.referred_cls)
        - 要在引用端映射的类。
    -   **constraint**[¶](#sqlalchemy.ext.automap.name_for_scalar_relationship.params.constraint)
        – the [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
        that is being inspected to produce this relationship.

 `sqlalchemy.ext.automap.`{.descclassname}`name_for_collection_relationship`{.descname}(*base*, *local\_cls*, *referred\_cls*, *constraint*)[¶](#sqlalchemy.ext.automap.name_for_collection_relationship "Permalink to this definition")
:   返回应该用于从一个类引用到另一个类的属性名称作为集合引用。

    默认的实现是：

        return referred_cls.__name__.lower() + "_collection"

    可以使用[`AutomapBase.prepare.name_for_collection_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_collection_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")参数指定替代实现。

    参数：

    -   **base**[¶](#sqlalchemy.ext.automap.name_for_collection_relationship.params.base)
        – the [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
        class doing the prepare.
    -   **local\_cls**
        [¶](#sqlalchemy.ext.automap.name_for_collection_relationship.params.local_cls)
        - 要在本地映射的类。
    -   **referenced\_cls**
        [¶](#sqlalchemy.ext.automap.name_for_collection_relationship.params.referred_cls)
        - 要在引用端映射的类。
    -   **constraint**[¶](#sqlalchemy.ext.automap.name_for_collection_relationship.params.constraint)
        – the [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
        that is being inspected to produce this relationship.

` sqlalchemy.ext.automap。 T0>  generate_relationship  T1> （ T2> 碱 T3>，方向 T4>， return_fn  T5>， attrname  T6>， local_cls  T7>， referred_cls  T8>， **千瓦 T9> ） T10 > ¶ T11>`{.descclassname}
:   代表两个映射类生成[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")或[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")。

    该函数的一个替代实现可以使用[`AutomapBase.prepare.generate_relationship`](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship "sqlalchemy.ext.automap.AutomapBase.prepare")参数指定。

    这个函数的默认实现如下：

        if return_fn is backref:
            return return_fn(attrname, **kw)
        elif return_fn is relationship:
            return return_fn(referred_cls, **kw)
        else:
            raise TypeError("Unknown relationship function: %s" % return_fn)

    参数：

    -   **base**[¶](#sqlalchemy.ext.automap.generate_relationship.params.base)
        – the [`AutomapBase`](#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
        class doing the prepare.
    -   **direction**[¶](#sqlalchemy.ext.automap.generate_relationship.params.direction)
        – indicate the “direction” of the relationship; this will be one
        of [`ONETOMANY`](internals.html#sqlalchemy.orm.interfaces.ONETOMANY "sqlalchemy.orm.interfaces.ONETOMANY"),
        [`MANYTOONE`](internals.html#sqlalchemy.orm.interfaces.MANYTOONE "sqlalchemy.orm.interfaces.MANYTOONE"),
        [`MANYTOMANY`](internals.html#sqlalchemy.orm.interfaces.MANYTOMANY "sqlalchemy.orm.interfaces.MANYTOMANY").
    -   **return\_fn**
        [¶](#sqlalchemy.ext.automap.generate_relationship.params.return_fn)
        - 默认用于创建关系的功能。这将是[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")或[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")。在第二步中，将使用[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数的结果产生新的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，所以用户定义的实现正确区分这两个函数，如果使用自定义关系函数。
    -   **local\_cls**[¶](#sqlalchemy.ext.automap.generate_relationship.params.local_cls)
        – the “local” class to which this relationship or backref will
        be locally present.
    -   **referred\_cls**[¶](#sqlalchemy.ext.automap.generate_relationship.params.referred_cls)
        – the “referred” class to which the relationship or backref
        refers to.
    -   **\*\* kw**
        [¶](#sqlalchemy.ext.automap.generate_relationship.params.**kw) -
        所有其他关键字参数都传递给该函数。

    Attrname：

    该关系被分配到的属性名称。如果[`generate_relationship.return_fn`](#sqlalchemy.ext.automap.generate_relationship.params.return_fn "sqlalchemy.ext.automap.generate_relationship")的值是[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数，那么这个名称是分配给后端参考的名称。

    返回：

    [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")或[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")结构，如[`generate_relationship.return_fn`](#sqlalchemy.ext.automap.generate_relationship.params.return_fn "sqlalchemy.ext.automap.generate_relationship")参数指定的。


