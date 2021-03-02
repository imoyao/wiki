---
title: ORM 配置
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/faq/ormconfiguration/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - faq
tags:
---
ORM 配置[¶](#orm-configuration "Permalink to this headline")
===========================================================

-   [我如何映射一个没有主键的表？](#how-do-i-map-a-table-that-has-no-primary-key)
-   [如何配置一个 Python 保留字或类似的列？](#how-do-i-configure-a-column-that-is-a-python-reserved-word-or-similar)
-   [给定一个映射类，如何获得所有列，关系，映射属性等的列表？](#how-do-i-get-a-list-of-all-columns-relationships-mapped-attributes-etc-given-a-mapped-class)
-   [我收到关于“在属性 Y 下隐式合并列 X”的警告或错误](#i-m-getting-a-warning-or-error-about-implicitly-combining-column-x-under-attribute-y)
-   [我正在使用 Declarative 并使用`and_()`或`or_()`设置 primaryjoin /
    secondaryjoin，并且收到有关外键的错误消息。
    T0\>](#i-m-using-declarative-and-setting-primaryjoin-secondaryjoin-using-an-and-or-or-and-i-am-getting-an-error-message-about-foreign-keys)
-   [Why is `ORDER BY` required with
    `LIMIT` (especially with
    `subqueryload()`)?](#why-is-order-by-required-with-limit-especially-with-subqueryload)

我如何映射一个没有主键的表？[¶](#how-do-i-map-a-table-that-has-no-primary-key "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------

SQLAlchemy
ORM 为了映射到一个特定的表，需要至少有一列表示为主键列；多列即合成主键当然也完全可行。这些列**不是**需要被数据库实际称为主键列，尽管它们是一个好主意。仅作为主键的*行为*是必要的，例如，作为一行的唯一且不可空的标识符。

大多数 ORM 需要对象具有某种主键，因为内存中的对象必须对应于数据库表中唯一可识别的行；至少，这允许对象可以作为 UPDATE 和 DELETE 语句的目标，这些语句只会影响该对象的行，而不会影响其他行。然而，主要关键的重要性远不止于此。在 SQLAlchemy 中，所有 ORM 映射对象总是在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中唯一地使用称为[identity
map](glossary.html#term-identity-map)的模式链接到其特定的数据库行，该模式是 SQLAlchemy 使用的工作单元系统，也是 ORM 使用最常见（也不常见）模式的关键。

注意

需要注意的是，我们只是在谈论 SQLAlchemy
ORM；一个构建在 Core 上的应用程序，它仅处理[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象，[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造等，**不需要任何主键以任何方式呈现在表格上或与其关联（尽管如此，在 SQL 中，所有表格都应该具有某种主键，以免需要实际更新或删除特定的行）。**

几乎在所有情况下，表都有一个所谓的[candidate
key](glossary.html#term-candidate-key)，它是一列或一系列唯一标识一行的列。如果一个表真的没有这个，并且实际上有完全重复的行，那么这个表就不对应于[第一范式](http://en.wikipedia.org/wiki/First_normal_form)，并且不能被映射。否则，可以直接将任何包含最佳候选键的列应用于映射器：

    class SomeClass(Base):plainplainplainplainplainplain
        __table__ = some_table_with_no_pk
        __mapper_args__ = {
            'primary_key':[some_table_with_no_pk.c.uid, some_table_with_no_pk.c.bar]
        }

更好的是，当使用完全声明的表元数据时，在这些列上使用`primary_key=True`标志：

    class SomeClass(Base):plainplainplainplainplainplain
        __tablename__ = "some_table_with_no_pk"

        uid = Column(Integer, primary_key=True)
        bar = Column(String, primary_key=True)

关系数据库中的所有表都应该有主键。即使是多对多关联表 -
主键也是两个关联列的组合：

    CREATE TABLE my_association (plainplainplain
      user_id INTEGER REFERENCES user(id),
      account_id INTEGER REFERENCES account(id),
      PRIMARY KEY (user_id, account_id)
    )

如何配置一个 Python 保留字或类似的列？[¶](#how-do-i-configure-a-column-that-is-a-python-reserved-word-or-similar "Permalink to this headline")
--------------------------------------------------------------------------------------------------------------------------------------------

在基于列的属性中可以给出映射中所需的任何名称。请参阅[Naming Columns
Distinctly from Attribute
Names](orm_mapping_columns.html#mapper-column-distinct-names)。

如何获得所有列，关系，映射属性等的列表给定一个映射类？[¶](#how-do-i-get-a-list-of-all-columns-relationships-mapped-attributes-etc-given-a-mapped-class "Permalink to this headline")
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

这些信息都可以从[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象中找到。

要获取特定映射类的[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")，请在其上调用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数：

    from sqlalchemy import inspectplain

    mapper = inspect(MyClass)

从那里，所有有关该类的信息都可以通过以下属性访问：

-   [`Mapper.attrs`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")
    - 所有映射属性的命名空间。属性本身是[`MapperProperty`](orm_internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的实例，它们包含可导致映射的 SQL 表达式或列的附加属性（如果适用）。
-   [`Mapper.column_attrs`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.column_attrs "sqlalchemy.orm.mapper.Mapper.column_attrs")
    -
    映射的属性名称空间限于列和 SQL 表达式属性。您可能希望使用[`Mapper.columns`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.columns "sqlalchemy.orm.mapper.Mapper.columns")直接访问[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象。
-   [`Mapper.relationships`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.relationships "sqlalchemy.orm.mapper.Mapper.relationships")
    - 所有[`RelationshipProperty`](orm_internals.html#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")属性的命名空间。
-   [`Mapper.all_orm_descriptors`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")
    - namespace of all mapped attributes, plus user-defined attributes
    defined using systems such as [`hybrid_property`](orm_extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property"),
    [`AssociationProxy`](orm_extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")
    and others.
-   [`Mapper.columns`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.columns "sqlalchemy.orm.mapper.Mapper.columns")
    - 与映射关联的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象和其他命名 SQL 表达式的命名空间。
-   [`Mapper.mapped_table`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.mapped_table "sqlalchemy.orm.mapper.Mapper.mapped_table")
    - 此映射器映射到的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或其他可选项。
-   [`Mapper.local_table`{](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.local_table "sqlalchemy.orm.mapper.Mapper.local_table")
    - 该映射器为“本地”的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")这与[`Mapper.mapped_table`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper.mapped_table "sqlalchemy.orm.mapper.Mapper.mapped_table")的不同之处在于，映射器使用继承映射到组合选择。

我收到了一条警告或错误消息：“隐式地将列 X 属性 Y 组合在一起”[¶](#i-m-getting-a-warning-or-error-about-implicitly-combining-column-x-under-attribute-y "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

这种情况是指当映射包含两个由于名称而被映射到相同属性名称的列时，但没有任何迹象表明这是故意的。映射类需要为每个要存储独立值的属性显式名称；当两列具有相同的名称并且没有歧义时，它们属于同一个属性，结果是一列中的值被**复制到另一列中，根据哪列被分配给属性第一。**

这种行为通常是可取的，并且在两个列通过继承映射内的外键关系链接在一起的情况下，可以不发出警告。当发生警告或异常时，可以通过将列分配给命名不同的属性，或者如果希望将它们组合在一起来解决问题，可以使用[`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")使其明确。

给出如下的例子：

    from sqlalchemy import Integer, Column, ForeignKeyplainplain
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)

    class B(A):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)
        a_id = Column(Integer, ForeignKey('a.id'))

从 SQLAlchemy 0.9.5 版开始，检测到上述情况，并会警告`A`和`B`的`id`列正在合并同名命名属性`id`，这是一个严重的问题，因为它意味着一个`B`对象的主键总是与它的`A` 。

解决此问题的映射如下所示：

    class A(Base):plainplainplain
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)

    class B(A):
        __tablename__ = 'b'

        b_id = Column('id', Integer, primary_key=True)
        a_id = Column(Integer, ForeignKey('a.id'))

Suppose we did want `A.id` and `B.id` to be mirrors of each other, despite the fact that
`B.a_id` is where `A.id` is
related. 我们可以使用[`column_property()`](orm_mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")将它们结合在一起：

    class A(Base):plainplainplain
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)

    class B(A):
        __tablename__ = 'b'

        # probably not what you want, but this is a demonstration
        id = column_property(Column(Integer, primary_key=True), A.id)
        a_id = Column(Integer, ForeignKey('a.id'))

我正在使用 Declarative 并使用`and_()`或`or_()`设置primaryjoin / secondaryjoin，并且收到有关外键的错误消息。[/ T4\>](#i-m-using-declarative-and-setting-primaryjoin-secondaryjoin-using-an-and-or-or-and-i-am-getting-an-error-message-about-foreign-keys "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

你在做这个吗？:

    class MyClass(Base):plainplainplain
        # ....

        foo = relationship("Dest", primaryjoin=and_("MyClass.id==Dest.foo_id", "MyClass.foo==Dest.bar"))

这是两个字符串表达式的`and_()`，SQLAlchemy 不能应用任何映射。Declarative 允许[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")参数指定为字符串，并使用`eval()`转换为表达式对象。但是这不会发生在`and_()`表达式内部 -
这是一种特殊的操作，声明式只适用于传递给 primaryjoin 或其他参数的字符串的*整体*

    class MyClass(Base):
        # ....

        foo = relationship("Dest", primaryjoin="and_(MyClass.id==Dest.foo_id, MyClass.foo==Dest.bar)")

或者，如果您需要的对象已经可用，请跳过字符串：

    class MyClass(Base):plain
        # ....

        foo = relationship(Dest, primaryjoin=and_(MyClass.id==Dest.foo_id, MyClass.foo==Dest.bar))

同样的想法适用于所有其他参数，如`foreign_keys`：

    # wrong !plainplainplainplainplain
    foo = relationship(Dest, foreign_keys=["Dest.foo_id", "Dest.bar_id"])

    # correct !
    foo = relationship(Dest, foreign_keys="[Dest.foo_id, Dest.bar_id]")

    # also correct !
    foo = relationship(Dest, foreign_keys=[Dest.foo_id, Dest.bar_id])

    # if you're using columns from the class that you're inside of, just use the column objects !
    class MyClass(Base):
        foo_id = Column(...)
        bar_id = Column(...)
        # ...

        foo = relationship(Dest, foreign_keys=[foo_id, bar_id])

为什么`LIMIT`需要`ORDER BY`（特别是`subqueryload()`）？ [¶ T7\>](#why-is-order-by-required-with-limit-especially-with-subqueryload "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

当没有设置显式排序时，关系数据库可以以任意顺序返回行。虽然这种排序通常对应于表内行的自然顺序，但并非所有数据库和所有查询都是这种情况。这样做的结果是，任何使用`LIMIT`或`OFFSET`限制行的查询应始终**指定`ORDER  t6 > BY`。**否则，实际返回哪些行是不确定的。

当我们使用 SQLAlchemy 方法（如[`Query.first()`](orm_query.html#sqlalchemy.orm.query.Query.first "sqlalchemy.orm.query.Query.first")）时，实际上我们在查询中应用了一个`LIMIT`，所以没有明确的排序，它不是确定性的我们真的回来了。虽然我们可能没有注意到对通常以自然顺序返回行的数据库的简单查询，但如果我们还使用[`orm.subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")加载相关集合，则会变得更加棘手，而我们可能无法按预期加载收藏。

SQLAlchemy通过发出一个单独的查询来实现[`orm.subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")，其结果与第一个查询的结果相匹配。我们看到这样发出两个查询：

    >>> session.query(User).options(subqueryload(User.addresses)).all()plainplain
    -- the "main" query
    SELECT users.id AS users_id
    FROM users
    -- the "load" query issued by subqueryload
    SELECT addresses.id AS addresses_id,
           addresses.user_id AS addresses_user_id,
           anon_1.users_id AS anon_1_users_id
    FROM (SELECT users.id AS users_id FROM users) AS anon_1
    JOIN addresses ON anon_1.users_id = addresses.user_id
    ORDER BY anon_1.users_id

第二个查询嵌入第一个查询作为行的来源。当内部查询使用`OFFSET`和/或`LIMIT`时没有排序，这两个查询可能看不到相同的结果：

    >>> user = session.query(User).options(subqueryload(User.addresses)).first()plainplain
    -- the "main" query
    SELECT users.id AS users_id
    FROM users
     LIMIT 1
    -- the "load" query issued by subqueryload
    SELECT addresses.id AS addresses_id,
           addresses.user_id AS addresses_user_id,
           anon_1.users_id AS anon_1_users_id
    FROM (SELECT users.id AS users_id FROM users LIMIT 1) AS anon_1
    JOIN addresses ON anon_1.users_id = addresses.user_id
    ORDER BY anon_1.users_id

根据数据库的具体情况，我们可能会得到如下两个查询的结果：

    -- query #1
    +--------+
    |users_id|
    +--------+
    |       1|
    +--------+

    -- query #2
    +------------+-----------------+---------------+
    |addresses_id|addresses_user_id|anon_1_users_id|
    +------------+-----------------+---------------+
    |           3|                2|              2|
    +------------+-----------------+---------------+
    |           4|                2|              2|
    +------------+-----------------+---------------+

以上，我们收到 2 个`user.id`的`addresses`行，其中 1 个没有。我们浪费了两行，但实际上并未加载收集。这是一个阴险的错误，因为没有查看 SQL 和结果，ORM 将不会显示出任何问题；如果我们访问`User`的`addresses`，它将为集合发出延迟加载，并且我们不会看到任何实际发生错误的地方。

此问题的解决方案是始终指定确定性的排序顺序，以便主查询始终返回相同的一组行。这通常意味着您应该在表上的唯一列上使用[`Query.order_by()`](orm_query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")。主键是一个很好的选择：

    session.query(User).options(subqueryload(User.addresses)).order_by(User.id).first()plainplainplain

请注意，[`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")不会遇到同样的问题，因为只发出一个查询，所以加载查询不能与主查询不同。

也可以看看

[The Importance of
Ordering](orm_loading_relationships.html#subqueryload-ordering)
