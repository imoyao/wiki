---
title: 声明式 API
date: 2021-02-20 22:41:41
permalink: /sqlalchemy/orm/extensions/declarative/api/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
  - declarative
tags:
  - 
---
声明式 API [¶](#declarative-api "Permalink to this headline")
============================================================

API 参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

 `sqlalchemy.ext.declarative.`{.descclassname}`declarative_base`{.descname}(*bind=None*, *metadata=None*, *mapper=None*, *cls=\<type 'object'\>*, *name='Base'*, *constructor=\<function \_\_init\_\_\>*, *class\_registry=None*, *metaclass=\<class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'\>*)[¶](#sqlalchemy.ext.declarative.declarative_base "Permalink to this definition")
:   为声明性类定义构造一个基类。

    新的基类将被赋予一个元类，该元类生成适当的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，并根据在类中声明提供的信息以及该类的任何子类进行相应的[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")调用类。

    参数：

    -   **bind**[¶](#sqlalchemy.ext.declarative.declarative_base.params.bind)
        – An optional [`Connectable`](core_connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable"),
        will be assigned the `bind` attribute on the
        [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        instance.
    -   **metadata**[¶](#sqlalchemy.ext.declarative.declarative_base.params.metadata)
        – An optional [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        instance. 所有由基类的子类隐式声明的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象将共享此元数据。如果没有提供MetaData实例，则会创建一个MetaData实例。The
        [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
        instance will be available via the metadata attribute of the
        generated declarative base class.
    -   **mapper**[¶](#sqlalchemy.ext.declarative.declarative_base.params.mapper)
        – An optional callable, defaults to [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper").
        将用于将子类映射到其表。
    -   **cls**
        [¶](#sqlalchemy.ext.declarative.declarative_base.params.cls) -
        默认为`object`。一种用作生成的声明式基类的基础的类型。可能是类或类的元组。
    -   **名称**
        [¶](#sqlalchemy.ext.declarative.declarative_base.params.name) -
        默认为`Base`。生成的类的显示名称。自定义这不是必需的，但可以提高回溯和调试的清晰度。
    -   **constructor**[¶](#sqlalchemy.ext.declarative.declarative_base.params.constructor)
        – Defaults to `_declarative_constructor()`, an \_\_init\_\_ implementation that assigns
        \*\*kwargs for declared fields and relationships to an instance.
        如果提供`None`，则不会提供\_\_init\_\_，并且构造会通过正常的Python语义回退到cls
        .\_\_ init\_\_。
    -   **class\_registry**[¶](#sqlalchemy.ext.declarative.declarative_base.params.class_registry)
        – optional dictionary that will serve as the registry of class
        names-\> mapped classes when string names are used to identify
        classes inside of [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        and others.
        允许两个或更多声明性基类共享相同的类名称注册表以简化基础间关系。
    -   **元类**
        [¶](#sqlalchemy.ext.declarative.declarative_base.params.metaclass)
        - 默认为`DeclarativeMeta`。元类或\_\_metaclass\_\_兼容的callable用作生成的声明基类的元类型。

    也可以看看

    [`as_declarative()`](#sqlalchemy.ext.declarative.as_declarative "sqlalchemy.ext.declarative.as_declarative")

` sqlalchemy.ext.declarative。 T0>  as_declarative  T1> （ T2>  **千瓦 T3> ） T4>  ¶ T5>`{.descclassname}
:   [`declarative_base()`](#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")的类装饰器。

    为发送给[`declarative_base()`](#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")的`cls`参数提供语法快捷方式，允许将基类就地转换为“声明式”基础：

        from sqlalchemy.ext.declarative import as_declarative

        @as_declarative()
        class Base(object):
            @declared_attr
            def __tablename__(cls):
                return cls.__name__.lower()
            id = Column(Integer, primary_key=True)

        class MyMappedClass(Base):
            # ...

    传递给[`as_declarative()`](#sqlalchemy.ext.declarative.as_declarative "sqlalchemy.ext.declarative.as_declarative")的所有关键字参数都传递给[`declarative_base()`](#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")。

    0.8.3版本中的新功能

    也可以看看

    [`declarative_base()`](#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")

*类 T0\> `sqlalchemy.ext.declarative。 T1>  declared_attr  T2> （ T3>  fget  T4>，级联=假 T5> ） T6> ¶ T7>`{.descclassname}*
:   基础：`sqlalchemy.orm.base._MappedAttribute`，`__builtin__.property`

    将类级方法标记为表示映射属性或特殊声明性成员名称的定义。

    @declared\_attr将属性转换为可以从未被实例化的类调用的类标量属性。声明式将特别标记为@declared\_attr的属性视为返回特定于映射或声明式表配置的构造。属性的名称是该属性的非动态版本的名称。

    @declared\_attr通常不适用于mixin，以定义要应用于该类的不同实现者的关系：

        class ProvidesUser(object):
            "A mixin that adds a 'user' relationship to classes."

            @declared_attr
            def user(self):
                return relationship("User")

    它也可以应用于映射类，例如为继承提供“多态”方案：

        class Employee(Base):
            id = Column(Integer, primary_key=True)
            type = Column(String(50), nullable=False)

            @declared_attr
            def __tablename__(cls):
                return cls.__name__.lower()

            @declared_attr
            def __mapper_args__(cls):
                if cls.__name__ == 'Employee':
                    return {
                            "polymorphic_on":cls.type,
                            "polymorphic_identity":"Employee"
                    }
                else:
                    return {"polymorphic_identity":cls.__name__}

    版本0.8中的更改 [`declared_attr`](#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")可以与非ORM或扩展属性（例如用户定义的属性或[`association_proxy()`](associationproxy.html#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")将在课堂上课时分配给班级。

    `级联 T0> ¶ T1>`{.descname}
    :   将[`declared_attr`](#sqlalchemy.ext.declarative.declared_attr "sqlalchemy.ext.declarative.declared_attr")标记为级联。

        这是一个特殊用途修饰符，它指示基于列或MapperProperty的声明属性应该在映射继承方案内针对每个映射的子类明确配置。

        下面，MyClass和MySubClass都将建立一个独立的`id` Column对象：

            class HasSomeAttribute(object):
                @declared_attr.cascading
                def some_id(cls):
                    if has_inherited_table(cls):
                        return Column(
                            ForeignKey('myclass.id'), primary_key=True)
                    else:
                        return Column(Integer, primary_key=True)

                    return Column('id', Integer, primary_key=True)

            class MyClass(HasSomeAttribute, Base):
                ""
                # ...

            class MySubClass(MyClass):
                ""
                # ...

        The behavior of the above configuration is that
        `MySubClass` will refer to both its own
        `id` column as well as that of
        `MyClass` underneath the attribute named
        `some_id`.

        也可以看看

        [Inheritance
        Configuration](inheritance.html#declarative-inheritance)

        [Mixing in Columns in Inheritance
        Scenarios](mixins.html#mixin-inheritance-columns)

`sqlalchemy.ext.declarative.api。`{.descclassname} `_declarative_constructor`{.descname} （ *self*，*\*\* kwargs* ） T5\> [¶ T6\>](#sqlalchemy.ext.declarative.api._declarative_constructor "Permalink to this definition")
:   一个简单的构造函数，允许从 kwargs 初始化。

    使用`kwargs`中的名称和值在构造的实例上设置属性。

    只有作为实例类的属性存在的键才被允许。例如，这些可以是任何映射的列或关系。

` sqlalchemy.ext.declarative。 T0>  has_inherited_table  T1> （ T2>  CLS  T3> ） T4> ¶< / T5>`{.descclassname}
:   给定一个类，如果它继承的任何类有一个映射表，则返回 True，否则返回 False。

 `sqlalchemy.ext.declarative.`{.descclassname}`synonym_for`{.descname}(*name*, *map\_column=False*)[¶](#sqlalchemy.ext.declarative.synonym_for "Permalink to this definition")
:   装饰者，使 Python @property 成为列的查询同义词。

    [`synonym()`](mapped_attributes.html#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")的装饰版本。正在装饰的函数是'descriptor'，否则将它的参数传递给synonym()：

        @synonym_for('col')
        @property
        def prop(self):
            return 'special sauce'

    常规的`synonym()`也可以在声明性设置中直接使用，并且可以方便读/写属性：

        prop = synonym('col', descriptor=property(_read_prop, _write_prop))

`sqlalchemy.ext.declarative。 T0>  comparable_using  T1> （ T2>  comparator_factory  T3> ） T4> ¶< / T5>`{.descclassname}
:   装饰者，允许在查询标准中使用 Python @property。

    这是通过comparator\_factory和正在装饰的函数的`comparable_property()`的装饰器前端：

        @comparable_using(MyComparatorType)
        @property
        def prop(self):
            return 'special sauce'

    常规的`comparable_property()`也可以在声明性设置中直接使用，并且可以方便读/写属性：

        prop = comparable_property(MyComparatorType)

 `sqlalchemy.ext.declarative.`{.descclassname}`instrument_declarative`{.descname}(*cls*, *registry*, *metadata*)[¶](#sqlalchemy.ext.declarative.instrument_declarative "Permalink to this definition")
:   给定一个类，使用给定的注册表（声明可以是任何字典和 MetaData 对象）声明性地配置类。

*class* `sqlalchemy.ext.declarative。`{.descclassname} `AbstractConcreteBase`{.descname} [¶](#sqlalchemy.ext.declarative.AbstractConcreteBase "Permalink to this definition")
:   基础：`sqlalchemy.ext.declarative.api.ConcreteBase`

    “具体”声明映射的助手类。

    [`AbstractConcreteBase`](#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    will use the [`polymorphic_union()`](mapping_api.html#sqlalchemy.orm.util.polymorphic_union "sqlalchemy.orm.util.polymorphic_union")
    function automatically, against all tables mapped as a subclass to
    this class. 该函数通过`__declare_last__()`函数调用，该函数本质上是[`after_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")事件的钩子。

    [`AbstractConcreteBase`](#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")
    does produce a mapped class for the base class, however it is not
    persisted to any table; it is instead mapped directly to the
    “polymorphic” selectable directly and is only used for selecting.
    与[`ConcreteBase`](#sqlalchemy.ext.declarative.ConcreteBase "sqlalchemy.ext.declarative.ConcreteBase")比较，它为基类创建一个持久表。

    例：

        from sqlalchemy.ext.declarative import AbstractConcreteBase

        class Employee(AbstractConcreteBase, Base):
            pass

        class Manager(Employee):
            __tablename__ = 'manager'
            employee_id = Column(Integer, primary_key=True)
            name = Column(String(50))
            manager_data = Column(String(40))

            __mapper_args__ = {
                'polymorphic_identity':'manager',
                'concrete':True}

    抽象基类通过声明以特殊方式处理；在类配置时，它的行为就像是一个声明式混合或一个`__abstract__`基类。一旦配置了类并且生成了映射，它就会自己映射，但是在它的所有后继之后。这是在其他SQLAlchemy系统中找不到的独特映射系统。

    使用这种方法，我们可以按照我们通常在[Mixin and Custom Base
    Classes](mixins.html#declarative-mixins)中执行的方式指定将在映射的子类上进行的列和属性：

        class Company(Base):
            __tablename__ = 'company'
            id = Column(Integer, primary_key=True)

        class Employee(AbstractConcreteBase, Base):
            employee_id = Column(Integer, primary_key=True)

            @declared_attr
            def company_id(cls):
                return Column(ForeignKey('company.id'))

            @declared_attr
            def company(cls):
                return relationship("Company")

        class Manager(Employee):
            __tablename__ = 'manager'

            name = Column(String(50))
            manager_data = Column(String(40))

            __mapper_args__ = {
                'polymorphic_identity':'manager',
                'concrete':True}

    但是，当我们使用我们的映射时，`Manager`和`Employee`将具有可独立使用的`.company`属性：

        session.query(Employee).filter(Employee.company.has(id=5))

    在版本1.0.0中进行了更改： - [`AbstractConcreteBase`](#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")的机制已经过修改，以支持直接在抽象基础上建立的关系，而无需任何特殊的配置步骤。

    也可以看看

    [`ConcreteBase`](#sqlalchemy.ext.declarative.ConcreteBase "sqlalchemy.ext.declarative.ConcreteBase")

    [Concrete Table Inheritance](inheritance.html#concrete-inheritance)

    [Using the Declarative Helper
    Classes](inheritance.html#inheritance-concrete-helpers)

*class* `sqlalchemy.ext.declarative。`{.descclassname} `ConcreteBase`{.descname} [¶](#sqlalchemy.ext.declarative.ConcreteBase "Permalink to this definition")
:   “具体”声明映射的助手类。

    [`ConcreteBase`](#sqlalchemy.ext.declarative.ConcreteBase "sqlalchemy.ext.declarative.ConcreteBase")
    will use the [`polymorphic_union()`](mapping_api.html#sqlalchemy.orm.util.polymorphic_union "sqlalchemy.orm.util.polymorphic_union")
    function automatically, against all tables mapped as a subclass to
    this class. 该函数通过`__declare_last__()`函数调用，该函数本质上是[`after_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")事件的钩子。

    [`ConcreteBase`](#sqlalchemy.ext.declarative.ConcreteBase "sqlalchemy.ext.declarative.ConcreteBase")
    produces a mapped table for the class itself.
    与[`AbstractConcreteBase`](#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")比较，不是。

    例：

        from sqlalchemy.ext.declarative import ConcreteBase

        class Employee(ConcreteBase, Base):
            __tablename__ = 'employee'
            employee_id = Column(Integer, primary_key=True)
            name = Column(String(50))
            __mapper_args__ = {
                            'polymorphic_identity':'employee',
                            'concrete':True}

        class Manager(Employee):
            __tablename__ = 'manager'
            employee_id = Column(Integer, primary_key=True)
            name = Column(String(50))
            manager_data = Column(String(40))
            __mapper_args__ = {
                            'polymorphic_identity':'manager',
                            'concrete':True}

    也可以看看

    [`AbstractConcreteBase`](#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")

    [Concrete Table Inheritance](inheritance.html#concrete-inheritance)

    [Using the Declarative Helper
    Classes](inheritance.html#inheritance-concrete-helpers)

*class* `sqlalchemy.ext.declarative。`{.descclassname} `DeferredReflection`{.descname} [¶](#sqlalchemy.ext.declarative.DeferredReflection "Permalink to this definition")
:   基于延迟反射步骤构建映射的辅助类。

    通常，通过在声明式类中使用autoload = True将[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象设置为`__table__`属性，可以在声明中使用声明式命令。The caveat is that theplain
    [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    must be fully reflected, or at the very least have a primary key
    column, at the point at which a normal declarative mapping is
    constructed, meaning the [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
    must be available at class declaration time.

    在一个特定的方法被调用后，[`DeferredReflection`](#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")
    mixin将映射器的构造移动到稍后的点，该方法首先反映了迄今为止创建的所有[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。类可以这样定义它：

        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.ext.declarative import DeferredReflection
        Base = declarative_base()

        class MyClass(DeferredReflection, Base):
            __tablename__ = 'mytable'

    Above, `MyClass` is not yet mapped.
    在以上述方式定义了一系列类之后，所有表都可以被映射，并且使用[`prepare()`](#sqlalchemy.ext.declarative.DeferredReflection.prepare "sqlalchemy.ext.declarative.DeferredReflection.prepare")创建映射：

        engine = create_engine("someengine://...")
        DeferredReflection.prepare(engine)

    [`DeferredReflection`](#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")
    mixin可以应用于各个类，用作声明性基本本身的基础，或者用于自定义抽象类。使用抽象基础允许为特定准备步骤准备只有一部分类，这对于使用多个引擎的应用程序是必需的。例如，如果应用程序有两个引擎，则可以使用两个基础，并分别进行准备，例如：

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

        # ... etc.

    以上，可以分别配置`ReflectedOne`和`ReflectedTwo`的类层次结构：

        ReflectedOne.prepare(engine_one)
        ReflectedTwo.prepare(engine_two)

    0.8版本中的新功能

     *classmethod*`prepare`{.descname}(*engine*)[¶](#sqlalchemy.ext.declarative.DeferredReflection.prepare "Permalink to this definition")
    :   为所有当前的[`DeferredReflection`](#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")子类反映所有[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象

### 特殊指令[¶](#special-directives "Permalink to this headline")

#### `__declare_last__()`[¶](#declare-last "Permalink to this headline")

`__declare_last__()`钩子允许定义由[`MapperEvents.after_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")事件自动调用的类级别函数，该映射假定映射已完成，并且'configure'步骤已经完成：

    class MyClass(Base):plain
        @classmethod
        def __declare_last__(cls):
            ""
            # do something with mappings

New in version 0.7.3.

#### `__declare_first__()`[¶](#declare-first "Permalink to this headline")

像`__declare_last__()`，但是在映射器配置开始时通过[`MapperEvents.before_configured()`](events.html#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")事件调用：

    class MyClass(Base):plain
        @classmethod
        def __declare_first__(cls):
            ""
            # do something before mappings are configured

版本 0.9.3 中的新功能

#### `__abstract__`[¶](#abstract "Permalink to this headline")

`__abstract__`会导致声明性完全跳过为该类生成表或映射器。一个类可以像mixin一样添加到层次结构中（参见[Mixin
and Custom Base
Classes](mixins.html#declarative-mixins)），允许子类仅从特殊类扩展：

    class SomeAbstractBase(Base):plain
        __abstract__ = True

        def some_helpful_method(self):
            ""

        @declared_attr
        def __mapper_args__(cls):
            return {"helpful mapper arguments":True}

    class MyMappedClass(SomeAbstractBase):
        ""

`__abstract__`的一个可能用途是对不同的基础使用不同的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")：

    Base = declarative_base()plain

    class DefaultBase(Base):
        __abstract__ = True
        metadata = MetaData()

    class OtherBase(Base):
        __abstract__ = True
        metadata = MetaData()

以上，从`DefaultBase`继承的类将使用一个[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")作为表的注册表，而那些从`OtherBase`继承的类将使用不同的表。表格本身可以在不同的数据库中创建：

    DefaultBase.metadata.create_all(some_engine)plain
    OtherBase.metadata_create_all(some_other_engine)

New in version 0.7.3.
