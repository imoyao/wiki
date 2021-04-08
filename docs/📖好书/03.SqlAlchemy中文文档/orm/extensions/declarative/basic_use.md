---
title: 基本使用
date: 2021-02-20 22:41:41
permalink: /sqlalchemy/orm/extensions/declarative/basic_use/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
  - declarative
tags:
---
基本使用[¶](#basic-use "Permalink to this headline")
====================================================

SQLAlchemy 对象关系配置涉及[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")和类对象的组合以定义映射类。[`declarative`](api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")
allows all three to be expressed at once within the class declaration.
尽可能使用常规 SQLAlchemy 模式和 ORM 结构，因此“古典”ORM 使用和声明性之间的配置保持高度相似。

举一个简单的例子：

    from sqlalchemy.ext.declarative import declarative_baseplainplainplain

    Base = declarative_base()

    class SomeClass(Base):
        __tablename__ = 'some_table'
        id = Column(Integer, primary_key=True)
        name =  Column(String(50))

在上面，`declarative_base()`可调用返回一个新的基类，所有映射类都应该继承它。当类定义完成时，将会生成一个新的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")。

生成的表和映射器可以通过`SomeClass`类中的`__table__`和`__mapper__`属性访问：

    # access the mapped Table
    SomeClass.__table__

    # access the Mapper
    SomeClass.__mapper__

定义属性[¶](#defining-attributes "Permalink to this headline")
--------------------------------------------------------------

在前面的示例中，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象会自动使用它们所分配的属性的名称进行命名。

要使用与其映射属性不同的名称明确命名列，只需为该列命名即可。Below,
column “some\_table\_id” is mapped to the “id” attribute of SomeClass,
but in SQL will be represented as “some\_table\_id”:

    class SomeClass(Base):plainplain
        __tablename__ = 'some_table'
        id = Column("some_table_id", Integer, primary_key=True)

属性可以在其构造后添加到类中，并将它们根据需要添加到基础[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")定义中：

    SomeClass.data = Column('data', Unicode)plainplainplain
    SomeClass.related = relationship(RelatedInfo)

使用声明式构造的类可以与使用[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")显式映射的类自由交互。

尽管不是必需的，但建议所有表共享相同的底层[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象，以便可以毫无问题地解决字符串配置的[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")引用。

访问 MetaData [¶](#accessing-the-metadata "Permalink to this headline")
----------------------------------------------------------------------

`declarative_base()`基类包含一个[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象，其中收集了新定义的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。此对象旨在直接访问[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")特定的操作。例如，为所有表发出 CREATE 语句：

    engine = create_engine('sqlite://')plainplainplainplain
    Base.metadata.create_all(engine)

`declarative_base()` can also
receive a pre-existing [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
object, which allows a declarative setup to be associated with an
already existing traditional collection of [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
objects:

    mymetadata = MetaData()plainplainplainplain
    Base = declarative_base(metadata=mymetadata)

类构造函数[¶](#class-constructor "Permalink to this headline")
--------------------------------------------------------------

作为一个方便的功能，`declarative_base()`在接受关键字参数的类上设置一个默认构造函数，并将它们分配给指定的属性：

    e = Engineer(primary_language='python')plainplainplainplain

映射器配置[¶](#mapper-configuration "Permalink to this headline")
-----------------------------------------------------------------

声明在内部创建映射到声明表时使用[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数。[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")的选项直接通过`__mapper_args__`类属性传递。与往常一样，引用局部映射列的参数可以直接从类声明中引用它们：

    from datetime import datetimeplainplainplainplainplainplain

    class Widget(Base):
        __tablename__ = 'widgets'

        id = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, nullable=False)

        __mapper_args__ = {
                        'version_id_col': timestamp,
                        'version_id_generator': lambda v:datetime.now()
                    }

定义 SQL 表达式[¶](#defining-sql-expressions "Permalink to this headline")
------------------------------------------------------------------------

有关将属性声明性映射到 SQL 表达式的示例，请参阅[SQL Expressions as Mapped
Attributes](mapped_sql_expr.html#mapper-sql-expressions)。
