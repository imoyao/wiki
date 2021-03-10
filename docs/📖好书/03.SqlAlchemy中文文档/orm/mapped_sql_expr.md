---
title: SQL 表达式作为映射的属性
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/mapped_sql_expr/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
SQL 表达式作为映射的属性[¶](#sql-expressions-as-mapped-attributes "Permalink to this headline")
==============================================================================================

映射类的属性可以链接到可用于查询的 SQL 表达式。

使用混合[¶](#using-a-hybrid "Permalink to this headline")
---------------------------------------------------------

将相对简单的 SQL 表达式链接到类的最简单和最灵活的方法是使用所谓的“混合属性”，如[Hybrid
Attributes](extensions_hybrid.html)部分中所述。该混合提供了一种既适用于 Python 级别又适用于 SQL 表达级别的表达式。例如，下面我们映射一个类`User`，它包含属性`firstname`和`lastname`，并且包含一个混合，它将为我们提供`fullname`，这是两个字符串的连接：

    from sqlalchemy.ext.hybrid import hybrid_property

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        firstname = Column(String(50))
        lastname = Column(String(50))

        @hybrid_property
        def fullname(self):
            return self.firstname + " " + self.lastname

上面，`fullname`属性在实例和类级别都被解释，以便它可以从实例中获得：

    some_user = session.query(User).first()
    print(some_user.fullname)

以及在查询中可用：

    some_user = session.query(User).filter(User.fullname == "John Smith").first()plain

字符串连接的例子很简单，Python 表达式可以在实例和类级别双重使用。通常，必须将 SQL 表达式与 Python 表达式区分开来，这可以使用[`hybrid_property.expression()`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property.expression "sqlalchemy.ext.hybrid.hybrid_property.expression")来实现。下面我们通过 Python 中的`if`语句和 SQL 表达式的[`sql.expression.case()`](core_sqlelement.html#sqlalchemy.sql.expression.case "sqlalchemy.sql.expression.case")构造来说明条件需要存在于混合内部的情况：

    from sqlalchemy.ext.hybrid import hybrid_propertyplain
    from sqlalchemy.sql import case

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        firstname = Column(String(50))
        lastname = Column(String(50))

        @hybrid_property
        def fullname(self):
            if self.firstname is not None:
                return self.firstname + " " + self.lastname
            else:
                return self.lastname

        @fullname.expression
        def fullname(cls):
            return case([
                (cls.firstname != None, cls.firstname + " " + cls.lastname),
            ], else_ = cls.lastname)

使用 column\_property [¶](#using-column-property "Permalink to this headline")
-----------------------------------------------------------------------------

[`orm.column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")函数可用于以类似于定期映射的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的方式映射 SQL 表达式。使用这种技术，该属性在加载时与所有其他列映射属性一起加载。这在某些情况下比混合使用更有优势，因为该值可以与对象的父行同时加载，特别是当表达式链接到其他表时（通常作为相关子查询）来访问通常不会在已经加载的对象上可用的数据。

Disadvantages to using [`orm.column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")
for SQL expressions include that the expression must be compatible with
the SELECT statement emitted for the class as a whole, and there are
also some configurational quirks which can occur when using
[`orm.column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")
from declarative mixins.

我们的“全名”示例可以使用[`orm.column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")表示如下：

    from sqlalchemy.orm import column_propertyplain

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        firstname = Column(String(50))
        lastname = Column(String(50))
        fullname = column_property(firstname + " " + lastname)

相关的子查询也可以使用。下面我们使用[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造创建一个 SELECT，它将特定`User`可用的`Address`对象的计数链接在一起：

    from sqlalchemy.orm import column_propertyplain
    from sqlalchemy import select, func
    from sqlalchemy import Column, Integer, String, ForeignKey

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('user.id'))

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        address_count = column_property(
            select([func.count(Address.id)]).\
                where(Address.user_id==id).\
                correlate_except(Address)
        )

在上面的例子中，我们定义了如下所示的[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构：

    select([func.count(Address.id)]).\
        where(Address.user_id==id).\
        correlate_except(Address)

The meaning of the above statement is, select the count of
`Address.id` rows where the
`Address.user_id` column is equated to
`id`, which in the context of the `User` class is the [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
named `id` (note that `id` is
also the name of a Python built in function, which is not what we want
to use here - if we were outside of the `User` class
definition, we’d use `User.id`).

`select.correlate_except()`指示表明可以从 FROM 列表中省略此[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")的 FROM 子句中的每个元素（即，与封闭的 SELECT 针对`User`的声明）除了与`Address`对应的声明之外。This
isn’t strictly necessary, but prevents `Address`
from being inadvertently omitted from the FROM list in the case of a
long string of joins between `User` and
`Address` tables where SELECT statements against
`Address` are nested.

如果导入问题阻止[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")与该类内联定义，则可以在两者都配置后将其分配给类。在 Declarative 中，这具有调用[`Mapper.add_property()`](mapping_api.html#sqlalchemy.orm.mapper.Mapper.add_property "sqlalchemy.orm.mapper.Mapper.add_property")在事实之后添加其他属性的效果：

    User.address_count = column_property(plain
            select([func.count(Address.id)]).\
                where(Address.user_id==User.id)
        )

对于多对多关系，使用[`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")将关联表的字段连接到关系中的两个表，这里用经典映射来说明：

    from sqlalchemy import and_

    mapper(Author, authors, properties={
        'book_count': column_property(
                            select([func.count(books.c.id)],
                                and_(
                                    book_authors.c.author_id==authors.c.id,
                                    book_authors.c.book_id==books.c.id
                                )))
        })

使用普通描述符[¶](#using-a-plain-descriptor "Permalink to this headline")
-------------------------------------------------------------------------

如果 SQL 查询比[`orm.column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")或[`hybrid_property`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")可以提供的更精细，则可以使用作为属性访问的常规 Python 函数，假设该表达式只需要在已经加载的实例上可用。该函数使用 Python 自己的`@property`修饰器进行修饰，以将其标记为只读属性。Within the function,
[`object_session()`](session_api.html#sqlalchemy.orm.session.object_session "sqlalchemy.orm.session.object_session")
is used to locate the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
corresponding to the current object, which is then used to emit a query:

    from sqlalchemy.orm import object_session
    from sqlalchemy import select, func

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        firstname = Column(String(50))
        lastname = Column(String(50))

        @property
        def address_count(self):
            return object_session(self).\
                scalar(
                    select([func.count(Address.id)]).\
                        where(Address.user_id==self.id)
                )

普通描述符方法作为最后的手段是有用的，但在通常情况下，混合性和列属性方法的性能较差，因为它需要在每次访问时发出 SQL 查询。
