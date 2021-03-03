---
title: 混合、自定义实体公共类
date: 2021-02-20 22:41:41
permalink: /sqlalchemy/orm/extensions/declarative/mixins/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
  - declarative
tags:
---
混合、自定义实体公共类[¶](#mixin-and-custom-base-classes "Permalink to this headline")
======================================================================================

使用[`declarative`](api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")时的一个常见需求是跨多个类共享某些功能，例如一组公共列，一些常用表选项或其他映射属性。标准的 Python 成语就是让这些类从包含这些常用特征的基础继承而来。

使用[`declarative`](api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")时，通过使用自定义声明式基类以及除主基础之外还继承的“mixin”类，可以使用该惯用法。声明包括几个帮助器功能，以便如何声明映射。下面是一些常用的混合成语的例子：

    from sqlalchemy.ext.declarative import declared_attrplain

    class MyMixin(object):

        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

        __table_args__ = {'mysql_engine': 'InnoDB'}
        __mapper_args__= {'always_refresh': True}

        id =  Column(Integer, primary_key=True)

    class MyModel(MyMixin, Base):
        name = Column(String(1000))

Where above, the class `MyModel` will contain an
“id” column as the primary key, a `__tablename__`
attribute that derives from the name of the class itself, as well as
`__table_args__` and `__mapper_args__` defined by the `MyMixin` mixin class.

There’s no fixed convention over whether `MyMixin`
precedes `Base` or not.
正常的 Python 方法解决规则适用，上面的例子也适用于：

    class MyModel(Base, MyMixin):
        name = Column(String(1000))

这是有效的，因为`Base`在这里没有定义`MyMixin`定义的任何变量，即`__tablename__`，`__table_args__` `id`等如果`Base`确实定义了一个具有相同名称的属性，则首先放置在继承列表中的类将确定在新定义的类上使用哪个属性。

通过传参来定制化 Base 基类[¶](#augmenting-the-base "Permalink to this headline")
------------------------------------------------------------------------------

除了使用 MixIn 类这种方法外，上文提到的技术也是完全可以使用到 Base 基类本身的，实现方法就是通过给[`declarative_base()`](api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")
参数传一个 `cls` 参数

    from sqlalchemy.ext.declarative import declared_attr

    class Base(object):
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

        __table_args__ = {'mysql_engine': 'InnoDB'}

        id =  Column(Integer, primary_key=True)

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base(cls=Base)

    class MyModel(Base):
        name = Column(String(1000))

如上，`MyModel`以及其他继承自`Base`的实体类就会拥有从类名（`id`主键列）派生的表名，“巴拉巴拉”的

在列中混合[¶](#mixing-in-columns "Permalink to this headline")
--------------------------------------------------------------

在 mixin 上指定列的最基本方法是通过简单的声明：

    class TimestampMixin(object):plain
        created_at = Column(DateTime, default=func.now())

    class MyModel(TimestampMixin, Base):
        __tablename__ = 'test'

        id =  Column(Integer, primary_key=True)
        name = Column(String(1000))

Where above, all declarative classes that include
`TimestampMixin` will also have a column
`created_at` that applies a timestamp to all row
insertions.

熟悉 SQLAlchemy 表达式语言的人知道 id(object
identity)唯一标识了一个对象实例在一张表（schema）中的身份两个`Table`对象`a`和`b`可能都有一个名为`id`的列，但这些区别的方式是`a.c.id`和`b.c.id`是两个不同的 Python 对象，分别引用它们的父表`a`和`b`。

对于 mixin 列，似乎只有一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象被显式创建，但上面的最终`created_at`列必须作为每个独立目标的独立 Python 对象存在类。为了达到这个目的，声明性扩展创建了一个被检测为 mixin 的类上遇到的每个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的**copy**。

此复制机制仅限于没有外键的简单列，因为[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")本身包含对在此级别无法正确重新创建的列的引用。对于具有外键的列以及需要目标显式上下文的各种映射级构造，提供了[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")修饰符，以便可以将许多类通用的模式定义为可调用对象：

    from sqlalchemy.ext.declarative import declared_attr

    class ReferenceAddressMixin(object):
        @declared_attr
        def address_id(cls):
            return Column(Integer, ForeignKey('address.id'))

    class User(ReferenceAddressMixin, Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)

在上面，`address_id`类级可调用在构造`User`类的位置执行，并且声明性扩展可以使用得到的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

在版本 0.6.5 中更改：将`sqlalchemy.util.classproperty`重命名为[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")。

Columns generated by [`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")
can also be referenced by `__mapper_args__` to a
limited degree, currently by `polymorphic_on` and
`version_id_col`; the declarative extension will
resolve them at class construction time:

    class MyMixin:plain
        @declared_attr
        def type_(cls):
            return Column(String(50))

        __mapper_args__= {'polymorphic_on':type_}

    class MyModel(MyMixin, Base):
        __tablename__='test'
        id =  Column(Integer, primary_key=True)

在关系中混合[¶](#mixing-in-relationships "Permalink to this headline")
----------------------------------------------------------------------

Relationships created by [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
are provided with declarative mixin classes exclusively using the
[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")
approach, eliminating any ambiguity which could arise when copying a
relationship and its possibly column-bound contents.
下面是一个结合外键列和关系的例子，这样两个类`Foo`和`Bar`都可以配置为通过多对一引用共同的目标类：

    class RefTargetMixin(object):plain
        @declared_attr
        def target_id(cls):
            return Column('target_id', ForeignKey('target.id'))

        @declared_attr
        def target(cls):
            return relationship("Target")

    class Foo(RefTargetMixin, Base):
        __tablename__ = 'foo'
        id = Column(Integer, primary_key=True)

    class Bar(RefTargetMixin, Base):
        __tablename__ = 'bar'
        id = Column(Integer, primary_key=True)

    class Target(Base):
        __tablename__ = 'target'
        id = Column(Integer, primary_key=True)

### 使用高级关系参数（例如`primaryjoin`等）[¶](#using-advanced-relationship-arguments-e-g-primaryjoin-etc "Permalink to this headline")

[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")定义需要显式的主要连接，order\_by 等除了最简单的情况外，所有表达式都应该使用**后缀**形式表示这些参数，即使用字符串形式或 lambda 表达式。这是因为要使用`@declared_attr`配置的相关[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象不可用于其他`@declared_attr`属性；虽然这些方法将工作并返回新的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，但这些对象并不是 Declarative 将在使用它自己调用方法时使用的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，因此使用*不同的*
[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象。

规范的例子是依赖于另一个混合列的主连接条件：

    class RefTargetMixin(object):
        @declared_attr
        def target_id(cls):
            return Column('target_id', ForeignKey('target.id'))

        @declared_attr
        def target(cls):
            return relationship(Target,
                primaryjoin=Target.id==cls.target_id   # this is *incorrect*
            )

使用上面的 mixin 映射一个类，我们会得到如下错误：

    sqlalchemy.exc.InvalidRequestError: this ForeignKey's parent column is notplain
    yet associated with a Table.

这是因为我们在`target()`方法中调用的`target_id` [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")与[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")该声明实际上是要映射到我们的表。

上面的条件使用 lambda 来解决：

    class RefTargetMixin(object):
        @declared_attr
        def target_id(cls):
            return Column('target_id', ForeignKey('target.id'))

        @declared_attr
        def target(cls):
            return relationship(Target,
                primaryjoin=lambda: Target.id==cls.target_id
            )

或者可选地，字符串形式（其最终生成拉姆达）：

    class RefTargetMixin(object):
        @declared_attr
        def target_id(cls):
            return Column('target_id', ForeignKey('target.id'))

        @declared_attr
        def target(cls):
            return relationship("Target",
                primaryjoin="Target.id==%s.target_id" % cls.__name__
            )

在 deferred()，column\_property()和其他 MapperProperty 类中混合[¶](#mixing-in-deferred-column-property-and-other-mapperproperty-classes "Permalink to this headline")
------------------------------------------------------------------------------------------------------------------------------------------------------------------

Like [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
all [`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")
subclasses such as [`deferred()`](loading_columns.html#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred"),
[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property"),
etc.
最终涉及对列的引用，因此在与声明性 mixin 一起使用时，必须具有[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")要求，以便不需要依赖复制：

    class SomethingMixin(object):

        @declared_attr
        def dprop(cls):
            return deferred(Column(Integer))

    class Something(SomethingMixin, Base):
        __tablename__ = "something"

[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")或其他构造可以引用来自 mixin 的其他列。在[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")被调用之前，它们被提前复制：

    class SomethingMixin(object):
        x = Column(Integer)

        y = Column(Integer)

        @declared_attr
        def x_plus_y(cls):
            return column_property(cls.x + cls.y)

版本 1.0.0 中已更改：将 mixin 列复制到最终映射类，以便[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")方法可以访问将要映射的实际列。

在关联代理和其他属性中混合[¶](#mixing-in-association-proxy-and-other-attributes "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------

Mixins 可以指定用户定义的属性以及其他扩展单元，如[`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")。在属性必须专门针对目标子类定制的情况下，[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")的用法是必需的。一个示例是构建多个[`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")属性，每个属性都针对不同类型的子对象。下面是一个[`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")
/ mixin 示例，它为实现类提供了字符串值的标量列表：

    from sqlalchemy import Column, Integer, ForeignKey, Stringplain
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.associationproxy import association_proxy
    from sqlalchemy.ext.declarative import declarative_base, declared_attr

    Base = declarative_base()

    class HasStringCollection(object):
        @declared_attr
        def _strings(cls):
            class StringAttribute(Base):
                __tablename__ = cls.string_table_name
                id = Column(Integer, primary_key=True)
                value = Column(String(50), nullable=False)
                parent_id = Column(Integer,
                                ForeignKey('%s.id' % cls.__tablename__),
                                nullable=False)
                def __init__(self, value):
                    self.value = value

            return relationship(StringAttribute)

        @declared_attr
        def strings(cls):
            return association_proxy('_strings', 'value')

    class TypeA(HasStringCollection, Base):
        __tablename__ = 'type_a'
        string_table_name = 'type_a_strings'
        id = Column(Integer(), primary_key=True)

    class TypeB(HasStringCollection, Base):
        __tablename__ = 'type_b'
        string_table_name = 'type_b_strings'
        id = Column(Integer(), primary_key=True)

在上面，`HasStringCollection`
mixin 产生了一个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，它引用了一个新生成的名为`StringAttribute`的类。`StringAttribute`类使用自己的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")定义生成，该定义对使用`HasStringCollection` mixin 的父类是本地的。它还生成一个[`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")对象，该对象将对`strings`属性的引用代理到每个`StringAttribute`的`value`实例。

`TypeA` or `TypeB` can be
instantiated given the constructor argument `strings`, a list of strings:

    ta = TypeA(strings=['foo', 'bar'])
    tb = TypeA(strings=['bat', 'bar'])

该列表将生成`StringAttribute`对象的集合，该对象保存到`type_a_strings`或`type_b_strings`表的本地表中：

    >>> print(ta._strings)
    [<__main__.StringAttribute object at 0x10151cd90>,
        <__main__.StringAttribute object at 0x10151ce10>]

When constructing the [`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy"),
the [`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")
decorator must be used so that a distinct [`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")
object is created for each of the `TypeA` and
`TypeB` classes.

版本 0.8 中的新功能 [`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")可用于非映射属性，包括用户定义的属性以及[`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")。

通过 mixins 控制表继承[¶](#controlling-table-inheritance-with-mixins "Permalink to this headline")
------------------------------------------------------------------------------------------------

`__tablename__`属性可用于提供一个函数，该函数将确定继承层次结构中每个类所用表的名称，以及某个类是否具有其自己的不同表。

这是通过使用[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")指标和名为`__tablename__()`的方法实现的。对于每个映射的类，声明式将始终为特殊名称`__tablename__`，`__mapper_args__`和`__table_args__`函数**调用[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")在层次结构**中。因此，该功能需要单独接收每个班级，并为每个班级提供正确的答案。

例如，要创建一个 mixin，为每个类提供一个基于类名的简单表名：

    from sqlalchemy.ext.declarative import declared_attr

    class Tablename:
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

    class Person(Tablename, Base):
        id = Column(Integer, primary_key=True)
        discriminator = Column('type', String(50))
        __mapper_args__ = {'polymorphic_on': discriminator}

    class Engineer(Person):
        __tablename__ = None
        __mapper_args__ = {'polymorphic_identity': 'engineer'}
        primary_language = Column(String(50))

或者，我们可以使用[`has_inherited_table()`](api.html#sqlalchemy.ext.declarative.has_inherited_table "sqlalchemy.ext.declarative.has_inherited_table")修改我们的`__tablename__`函数为子类返回`None`。这具有将这些子类映射为父表单继承的效果：

    from sqlalchemy.ext.declarative import declared_attrplain
    from sqlalchemy.ext.declarative import has_inherited_table

    class Tablename(object):
        @declared_attr
        def __tablename__(cls):
            if has_inherited_table(cls):
                return None
            return cls.__name__.lower()

    class Person(Tablename, Base):
        id = Column(Integer, primary_key=True)
        discriminator = Column('type', String(50))
        __mapper_args__ = {'polymorphic_on': discriminator}

    class Engineer(Person):
        primary_language = Column(String(50))
        __mapper_args__ = {'polymorphic_identity': 'engineer'}

在继承方案中的列中混合[¶](#mixing-in-columns-in-inheritance-scenarios "Permalink to this headline")
---------------------------------------------------------------------------------------------------

与[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")结合使用时，如何处理`__tablename__`和其他特殊名称，当我们混合使用列和属性时（例如关系，列属性等）），该函数仅针对层次结构中的**基类**调用。下面，只有`Person`类会收到一个名为`id`的列。
`Engineer`中的映射将失败，该工程没有给出主键：

    class HasId(object):plain
        @declared_attr
        def id(cls):
            return Column('id', Integer, primary_key=True)

    class Person(HasId, Base):
        __tablename__ = 'person'
        discriminator = Column('type', String(50))
        __mapper_args__ = {'polymorphic_on': discriminator}

    class Engineer(Person):
        __tablename__ = 'engineer'
        primary_language = Column(String(50))
        __mapper_args__ = {'polymorphic_identity': 'engineer'}

在连接表继承中，我们通常希望每个子类都有明确命名的列。但是在这种情况下，我们可能希望在每个表上都有一个`id`列，并让它们通过外键相互引用。We can achieve this as a mixin by
using the [`declared_attr.cascading`](api.html#sqlalchemy.ext.declarative.declared_attr.cascading "sqlalchemy.ext.declarative.declared_attr.cascading")
modifier, which indicates that the function should be invoked **for each
class in the hierarchy**, just like it does for
`__tablename__`:

    class HasId(object):plain
        @declared_attr.cascading
        def id(cls):
            if has_inherited_table(cls):
                return Column('id',
                              Integer,
                              ForeignKey('person.id'), primary_key=True)
            else:
                return Column('id', Integer, primary_key=True)

    class Person(HasId, Base):
        __tablename__ = 'person'
        discriminator = Column('type', String(50))
        __mapper_args__ = {'polymorphic_on': discriminator}

    class Engineer(Person):
        __tablename__ = 'engineer'
        primary_language = Column(String(50))
        __mapper_args__ = {'polymorphic_identity': 'engineer'}

版本 1.0.0 新增：新增[`declared_attr.cascading`](api.html#sqlalchemy.ext.declarative.declared_attr.cascading "sqlalchemy.ext.declarative.declared_attr.cascading")。

结合来自多个 Mixin 的 Table / Mapper 参数[¶](#combining-table-mapper-arguments-from-multiple-mixins "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------

在声明性 mixin 指定的`__table_args__`或`__mapper_args__`的情况下，您可能希望将几个 mixin 的一些参数与您希望在类 iteself 上定义的参数结合起来。这里可以使用[`declared_attr`](api.html#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")装饰器来创建从多个集合中抽取的用户定义的整理例程：

    from sqlalchemy.ext.declarative import declared_attrplain

    class MySQLSettings(object):
        __table_args__ = {'mysql_engine':'InnoDB'}

    class MyOtherMixin(object):
        __table_args__ = {'info':'foo'}

    class MyModel(MySQLSettings, MyOtherMixin, Base):
        __tablename__='my_model'

        @declared_attr
        def __table_args__(cls):
            args = dict()
            args.update(MySQLSettings.__table_args__)
            args.update(MyOtherMixin.__table_args__)
            return args

        id =  Column(Integer, primary_key=True)

用 Mixins 创建索引[¶](#creating-indexes-with-mixins "Permalink to this headline")
-------------------------------------------------------------------------------

要定义适用于从 mixin 派生的所有表的命名的可能多列[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")，请使用[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")的“inline”形式，并将它建立为`__table_args__`

    class MyMixin(object):
        a =  Column(Integer)
        b =  Column(Integer)

        @declared_attr
        def __table_args__(cls):
            return (Index('test_idx_%s' % cls.__tablename__, 'a', 'b'),)

    class MyModel(MyMixin, Base):
        __tablename__ = 'atable'
        c =  Column(Integer,primary_key=True)
