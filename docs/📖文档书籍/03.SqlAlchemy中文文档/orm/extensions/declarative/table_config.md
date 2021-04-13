---
title: 表格配置
date: 2021-02-20 22:41:42
permalink: /sqlalchemy/orm/extensions/declarative/table_config/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
  - declarative
tags:
---
表格配置[¶](#table-configuration "Permalink to this headline")
==============================================================

除了名称，元数据和映射列参数之外的表参数是使用`__table_args__`类属性指定的。该属性包含通常发送到[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造函数的位置和关键字参数。该属性可以用两种形式之一来指定。一个是字典：

    class MyClass(Base):plainplainplainplainplainplainplainplainplainplain
        __tablename__ = 'sometable'
        __table_args__ = {'mysql_engine':'InnoDB'}

另一个是元组，每个参数都是位置的（通常是约束条件）：

    class MyClass(Base):plainplainplainplainplainplainplainplainplainplain
        __tablename__ = 'sometable'
        __table_args__ = (
                ForeignKeyConstraint(['id'], ['remote_table.id']),
                UniqueConstraint('foo'),
                )

通过将最后一个参数指定为字典，可以使用上述形式指定关键字参数：

    class MyClass(Base):plainplainplainplainplainplainplainplainplainplain
        __tablename__ = 'sometable'
        __table_args__ = (
                ForeignKeyConstraint(['id'], ['remote_table.id']),
                UniqueConstraint('foo'),
                {'autoload':True}
                )

使用\_\_table \_\_ [¶](#using-a-hybrid-approach-with-table "Permalink to this headline")的混合方法
--------------------------------------------------------------------------------------------------

作为`__tablename__`的替代方案，可以使用直接的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")结构。在这种情况下需要名称的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象将被添加到映射中，就像正常映射到表一样：

    class MyClass(Base):plainplainplainplainplainplainplainplainplainplainplainplainplainplain
        __table__ = Table('my_table', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50))
        )

`__table__` provides a more focused point of control
for establishing table metadata, while still getting most of the
benefits of using declarative.
使用反射的应用程序可能希望在其他地方加载表元数据并将其传递给声明性类：

    from sqlalchemy.ext.declarative import declarative_baseplainplainplainplainplainplain

    Base = declarative_base()
    Base.metadata.reflect(some_engine)

    class User(Base):
        __table__ = metadata.tables['user']

    class Address(Base):
        __table__ = metadata.tables['address']

一些配置方案可能会发现使用`__table__`更合适，例如那些已经利用[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的数据驱动性质来自定义和/或自动化模式定义的配置方案。

请注意，当使用`__table__`方法时，该对象可立即用作类声明主体本身内的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，因为 Python 类只是另一个语法块。在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的`primaryjoin`条件中使用`id`列来说明以下情况：

    class MyClass(Base):plainplainplainplainplainplainplainplainplainplainplainplain
        __table__ = Table('my_table', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50))
        )

        widgets = relationship(Widget,
                    primaryjoin=Widget.myclass_id==__table__.c.id)

类似地，引用`__table__`的映射属性可以内联放置，如下我们将`name`列分配给属性`_name`，生成同义词对于`name`：

    from sqlalchemy.ext.declarative import synonym_forplainplainplainplainplainplainplainplainplain

    class MyClass(Base):
        __table__ = Table('my_table', Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50))
        )

        _name = __table__.c.name

        @synonym_for("_name")
        def name(self):
            return "Name: %s" % _name

用声明[¶](#using-reflection-with-declarative "Permalink to this headline")使用反射
----------------------------------------------------------------------------------

将`autoload=True`与映射类结合使用的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")很容易：

    class MyClass(Base):plainplainplainplainplainplainplainplainplainplainplainplain
        __table__ = Table('mytable', Base.metadata,
                        autoload=True, autoload_with=some_engine)

然而，这里可以做出的一个改进是在首次声明类时不要求[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")可用。为了达到这个目的，使用[`DeferredReflection`](api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")
mixin，它只有在调用一个特殊的`prepare(engine)`步骤后才能设置映射：

    from sqlalchemy.ext.declarative import declarative_base, DeferredReflectionplainplainplain

    Base = declarative_base(cls=DeferredReflection)

    class Foo(Base):
        __tablename__ = 'foo'
        bars = relationship("Bar")

    class Bar(Base):
        __tablename__ = 'bar'

        # illustrate overriding of "bar.foo_id" to have
        # a foreign key constraint otherwise not
        # reflected, such as when using MySQL
        foo_id = Column(Integer, ForeignKey('foo.id'))

    Base.prepare(e)

版本 0.8 新增：新增[`DeferredReflection`](api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")。
