---
title: nonstandard_mappings
date: 2021-02-20 22:41:45
permalink: /pages/64bb62/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
非传统映射[¶](#non-traditional-mappings "Permalink to this headline")
=====================================================================

根据多个表映射类[¶](#mapping-a-class-against-multiple-tables "Permalink to this headline")
------------------------------------------------------------------------------------------

除了普通表以外，映射器还可以针对任意关系单元（称为*selectables*）构建。例如，[`join()`](core_selectable.html#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")函数创建一个由多个表组成的可选单元，其中包含自己的复合主键，可以像[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
：

    from sqlalchemy import Table, Column, Integer, \
            String, MetaData, join, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import column_property

    metadata = MetaData()

    # define two Table objects
    user_table = Table('user', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
            )

    address_table = Table('address', metadata,
                Column('id', Integer, primary_key=True),
                Column('user_id', Integer, ForeignKey('user.id')),
                Column('email_address', String)
                )

    # define a join between them.  This
    # takes place across the user.id and address.user_id
    # columns.
    user_address_join = join(user_table, address_table)

    Base = declarative_base()

    # map to it
    class AddressUser(Base):
        __table__ = user_address_join

        id = column_property(user_table.c.id, address_table.c.user_id)
        address_id = address_table.c.id

在上面的示例中，联接表示`user`和`address`表的列。`user.id`和`address.user_id`列由外键等同，所以在映射中它们被定义为一个属性，`AddressUser.id` ，使用[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")来指示专门的列映射。根据这部分配置，映射将在发生刷新时将`user.id`中的新主键值复制到`address.user_id`列中。

此外，`address.id`列显式映射到名为`address_id`的属性。This is
to **disambiguate** the mapping of the `address.id`
column from the same-named `AddressUser.id`
attribute, which here has been assigned to refer to the `user` table combined with the `address.user_id`
foreign key.

上述映射的自然主键是`（user.id， address.id）`的组合，因为它们是主键列将`user`和`address`表合并在一起。The identity of an
`AddressUser` object will be in terms of these two
values, and is represented from an `AddressUser`
object as `(AddressUser.id, AddressUser.address_id)`.

根据任意选择映射类[¶](#mapping-a-class-against-arbitrary-selects "Permalink to this headline")
----------------------------------------------------------------------------------------------

类似于对连接的映射，普通的[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")对象也可以与映射器一起使用。下面的示例片段举例说明了将名为`Customer`的类映射到包含对子查询的连接的[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")：

    from sqlalchemy import select, func

    subq = select([
                func.count(orders.c.id).label('order_count'),
                func.max(orders.c.price).label('highest_order'),
                orders.c.customer_id
                ]).group_by(orders.c.customer_id).alias()

    customer_select = select([customers, subq]).\
                select_from(
                    join(customers, subq,
                            customers.c.id == subq.c.customer_id)
                ).alias()

    class Customer(Base):
        __table__ = customer_select

Above, the full row represented by `customer_select`
will be all the columns of the `customers` table, in
addition to those columns exposed by the `subq`
subquery, which are `order_count`,
`highest_order`, and `customer_id`. 将`Customer`类映射到此可选项然后创建一个包含这些属性的类。

当ORM持续`Customer`的新实例时，只有`customers`表将实际接收到INSERT。这是因为`orders`表的主关键字未在映射中表示；
ORM将仅向其映射主键的表发出INSERT。

注意

几乎从不需要映射到任意SELECT语句的做法，尤其是复杂的SELECT语句；它往往会产生复杂的查询，这些查询的效率往往低于通过直接查询构建产生的查询的效率。The
practice is to some degree based on the very early history of SQLAlchemy
where the [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
construct was meant to represent the primary querying interface; in
modern usage, the [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
object can be used to construct virtually any SELECT statement,
including complex composites, and should be favored over the
“map-to-selectable” approach.

一个类的多个映射器[¶](#multiple-mappers-for-one-class "Permalink to this headline")
-----------------------------------------------------------------------------------

在现代的SQLAlchemy中，一个特定的类一次只能映射一个所谓的**primary**映​​射器。该映射器涉及三个主要功能领域：映射类的查询，持久性和检测。主要映射器的基本原理与[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")修改类本身的事实有关，不仅将它持久化为特定的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，而且[instrumenting](glossary.html#term-instrumenting)无法将多个映射器同等级地与一个类相关联，因为只有一个映射器可以真正对这个类进行测试。

然而，有一类称为**非主映射器的映射器允许附加的映射器与类关联，但是使用范围有限。**此范围通常适用于能够从备用表或可选单元加载行，但仍会生成最终使用主映射持久化的类。非主映射器是使用古典风格的映射创建的，该映射对已使用主映射器映射的类进行映射，并涉及使用[`non_primary`{.xref
.py .py-paramref .docutils
.literal}](mapping_api.html#sqlalchemy.orm.mapper.params.non_primary "sqlalchemy.orm.mapper")标志。

现代SQLAlchemy中非主要映射器的使用非常有限，因为可以直接使用[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象来完成从子查询或其他复合语句加载类的任务。

对于非主映射器，实际上只有一个用例，那就是我们希望为这样一个映射器建立[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")；这在罕见和高级的情况下非常有用，我们的关系试图通过使用许多表和/或连接来连接两个类。这种模式的一个例子是[Relationship
to Non Primary
Mapper](join_conditions.html#relationship-non-primary-mapper)的关系。

至于实际上可以在不同场景下完全坚持不同表的类的用例，早期版本的SQLAlchemy提供了一个适用于Hibernate的特性，称为“实体名称”特性。但是，一旦映射类本身成为SQL表达式构造的源，此用例在SQLAlchemy中就变得不可行了；也就是说，类的属性本身直接链接到映射的表列。该功能已被删除，取而代之的是一种简单的面向配方的方法来完成此任务，没有任何工具的歧义
-
创建新的子类，每个子类分别映射。此模式现在可在[实体名称](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/EntityName)中作为配方使用。
