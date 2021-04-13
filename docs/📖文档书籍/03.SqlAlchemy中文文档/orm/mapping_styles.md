---
title: 映射类型
date: 2021-02-20 22:41:45
permalink: /sqlalchemy/orm/mapping_styles/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
映射类型[¶](#types-of-mappings "Permalink to this headline")
============================================================

现代 SQLAlchemy 具有两种不同的映射器配置样式。“古典”风格是 SQLAlchemy 的原始映射 API，而“声明式”则是建立在“古典”之上的更丰富，更简洁的系统。Both
styles may be used interchangeably, as the end result of each is exactly
the same - a user-defined class mapped by the [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
function onto a selectable unit, typically a [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").

声明性映射[¶](#declarative-mapping "Permalink to this headline")
----------------------------------------------------------------

*声明性映射*是在现代 SQLAlchemy 中构建映射的典型方式。利用[Declarative](extensions_declarative_index.html)系统，可以立即定义用户定义类的组件以及该类映射到的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")元数据：

    from sqlalchemy.ext.declarative import declarative_baseplainplainplainplain
    from sqlalchemy import Column, Integer, String, ForeignKey

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)

以上是四列的基本单表映射。其他属性，例如与其他映射类的关系，也在类定义中内联声明：

    class User(Base):plainplainplainplain
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)

        addresses = relationship("Address", backref="user", order_by="Address.id")

    class Address(Base):
        __tablename__ = 'address'

        id = Column(Integer, primary_key=True)
        user_id = Column(ForeignKey('user.id'))
        email_address = Column(String)

声明性映射系统在[Object Relational
Tutorial](tutorial.html)中引入。有关此系统如何工作的更多详细信息，请参见[Declarative](extensions_declarative_index.html)。

古典映射[¶](#classical-mappings "Permalink to this headline")
-------------------------------------------------------------

A *经典映射*指的是使用[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数对映射类进行配置，而不使用 Declarative 系统。这是 SQLAlchemy 的原始类映射 API，它仍然是 ORM 提供的基本映射系统。

在“古典”形式中，表格元数据是通过[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")结构单独创建的，然后通过[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数与`User` ：

    from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKeyplainplainplainplain
    from sqlalchemy.orm import mapper

    metadata = MetaData()

    user = Table('user', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(50)),
                Column('fullname', String(50)),
                Column('password', String(12))
            )

    class User(object):
        def __init__(self, name, fullname, password):
            self.name = name
            self.fullname = fullname
            self.password = password

    mapper(User, user)

有关映射属性的信息（例如与其他类的关系）通过`properties`字典提供。The example below illustrates a second [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
object, mapped to a class called `Address`, then
linked to `User` via [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"):

    address = Table('address', metadata,plainplainplainplain
                Column('id', Integer, primary_key=True),
                Column('user_id', Integer, ForeignKey('user.id')),
                Column('email_address', String(50))
                )

    mapper(User, user, properties={
        'addresses' : relationship(Address, backref='user', order_by=address.c.id)
    })

    mapper(Address, address)

在使用经典映射时，必须直接提供类，而没有 Declarative 提供的“字符串查找”系统的好处。SQL 表达式通常以[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的形式指定，即`Address`关系的`address.c.id`，而不是`Address.id`，因为`Address`可能尚未链接到表元数据，我们也不能在此处指定字符串。

文档中的一些示例仍然使用经典方法，但请注意经典和声明式方法**完全可互换**。两个系统最终都会创建相同的配置，由[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，用户定义的类组成，它们与[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")链接在一起。当我们谈论“[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")的行为”时，这也包括在使用 Declarative 系统时
- 它仍然在幕后使用。

对映射，对象的运行时反省[¶](#runtime-introspection-of-mappings-objects "Permalink to this headline")
----------------------------------------------------------------------------------------------------

使用[Runtime Inspection
API](core_inspection.html)系统，无论使用何种方法，[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象都可以从任何映射类中获得。使用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数，可以从映射类获取[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")：

    >>> from sqlalchemy import inspectplainplainplainplainplain
    >>> insp = inspect(User)

详细信息包括[`Mapper.columns`](mapping_api.html#sqlalchemy.orm.mapper.Mapper.columns "sqlalchemy.orm.mapper.Mapper.columns")：

    >>> insp.columnsplainplainplainplain
    <sqlalchemy.util._collections.OrderedProperties object at 0x102f407f8>

这是一个可以以列表格式或通过个人名称查看的名称空间：

    >>> list(insp.columns)plainplainplainplain
    [Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('name', String(length=50), table=<user>), Column('fullname', String(length=50), table=<user>), Column('password', String(length=12), table=<user>)]
    >>> insp.columns.name
    Column('name', String(length=50), table=<user>)

其他名称空间包括[`Mapper.all_orm_descriptors`](mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")，其中包含所有映射的属性以及混合，关联代理：

    >>> insp.all_orm_descriptorsplainplainplain
    <sqlalchemy.util._collections.ImmutableProperties object at 0x1040e2c68>
    >>> insp.all_orm_descriptors.keys()
    ['fullname', 'password', 'name', 'id']

以及[`Mapper.column_attrs`](mapping_api.html#sqlalchemy.orm.mapper.Mapper.column_attrs "sqlalchemy.orm.mapper.Mapper.column_attrs")：

    >>> list(insp.column_attrs)plainplainplainplainplainplainplainplainplainplainplain
    [<ColumnProperty at 0x10403fde0; id>, <ColumnProperty at 0x10403fce8; name>, <ColumnProperty at 0x1040e9050; fullname>, <ColumnProperty at 0x1040e9148; password>]
    >>> insp.column_attrs.name
    <ColumnProperty at 0x10403fce8; name>
    >>> insp.column_attrs.name.expression
    Column('name', String(length=50), table=<user>)

也可以看看

[Runtime Inspection API](core_inspection.html)

[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")

[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")
