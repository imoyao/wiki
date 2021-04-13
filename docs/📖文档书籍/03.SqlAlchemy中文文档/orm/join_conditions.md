---
title: 配置关系如何连接
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/join_conditions/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
配置关系如何连接[¶](#configuring-how-relationship-joins "Permalink to this headline")
=====================================================================================

[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
will normally create a join between two tables by examining the foreign
key relationship between the two tables to determine which columns
should be compared. 有多种情况需要定制此行为。

处理多个连接路径[¶](#handling-multiple-join-paths "Permalink to this headline")
-------------------------------------------------------------------------------

处理的最常见情况之一是两个表之间有多个外键路径。

考虑一个包含`Address`类的两个外键的`Customer`类：

    from sqlalchemy import Integer, ForeignKey, String, Columnplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class Customer(Base):
        __tablename__ = 'customer'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        billing_address_id = Column(Integer, ForeignKey("address.id"))
        shipping_address_id = Column(Integer, ForeignKey("address.id"))

        billing_address = relationship("Address")
        shipping_address = relationship("Address")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        street = Column(String)
        city = Column(String)
        state = Column(String)
        zip = Column(String)

上面的映射，当我们尝试使用它时，会产生错误：

    sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine joinplainplain
    condition between parent/child tables on relationship
    Customer.billing_address - there are multiple foreign key
    paths linking the tables.  Specify the 'foreign_keys' argument,
    providing a list of those columns which should be
    counted as containing a foreign key reference to the parent table.

上面的消息很长。[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")可以返回很多潜在的消息，这些消息经过精心定制以检测各种常见配置问题；大多数人会建议解决歧义或其他缺失信息所需的额外配置。

在这种情况下，消息希望我们通过指示每个关键字列应该被考虑，来限定每个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，并且适当的格式如下：

    class Customer(Base):plainplainplainplain
        __tablename__ = 'customer'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        billing_address_id = Column(Integer, ForeignKey("address.id"))
        shipping_address_id = Column(Integer, ForeignKey("address.id"))

        billing_address = relationship("Address", foreign_keys=[billing_address_id])
        shipping_address = relationship("Address", foreign_keys=[shipping_address_id])

在上面，我们指定了`foreign_keys`参数，它是[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的列表，指示那些列被视为“外部”换句话说，包含引用父表的值的列。Loading
the `Customer.billing_address` relationship from a
`Customer` object will use the value present in
`billing_address_id` in order to identify the row in
`Address` to be loaded; similarly,
`shipping_address_id` is used for the
`shipping_address` relationship.
两列的联系在持续期间也起着作用；刚刚插入的`Address`对象的新生成的主键将在刷新期间被复制到关联`Customer`对象的相应外键列中。

使用 Declarative 指定`foreign_keys`时，我们也可以使用字符串名称来指定，但是如果使用列表，则**列表是字符串**的一部分，这一点很重要：

    billing_address = relationship("Address", foreign_keys="[Customer.billing_address_id]")plainplain

在这个特定的例子中，因为只有一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")我们需要：

    billing_address = relationship("Address", foreign_keys="Customer.billing_address_id")plainplain

在版本 0.8 中更改： [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")可以单独根据`foreign_keys`参数解决外键目标之间的歧义；在这种情况下，不再需要[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")参数。

指定交替连接条件[¶](#specifying-alternate-join-conditions "Permalink to this headline")
---------------------------------------------------------------------------------------

构造连接时，[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的默认行为是，它将一侧的主键列的值与另一侧的外键引用列的值相等。我们可以将此标准更改为我们希望使用[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")参数的任何内容，以及在使用“辅助”表格的情况下使用[`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")参数。

在下面的示例中，使用`User`类以及存储街道地址的`Address`类，我们创建一个关系`boston_addresses`加载指定城市“波士顿”的`Address`对象：

    from sqlalchemy import Integer, ForeignKey, String, Columnplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        boston_addresses = relationship("Address",
                        primaryjoin="and_(User.id==Address.user_id, "
                            "Address.city=='Boston')")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('user.id'))

        street = Column(String)
        city = Column(String)
        state = Column(String)
        zip = Column(String)

在这个字符串的 SQL 表达式中，我们使用[`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")连接结构为连接条件建立两个不同的谓词
- 连接`User.id`和`Address.user_id`列，并将`Address`中的行限制为`city='Boston'`。使用声明时，像[`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")这样的基本 SQL 函数可以在字符串[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")参数的计算命名空间中自动使用。

我们在[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")中使用的自定义标准通常仅在 SQLAlchemy 呈现 SQL 以加载或表示此关系时才有意义。也就是说，它被用于为了执行每个属性的延迟加载而发出的 SQL 语句中，或者在查询时构建连接（例如通过[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")）或通过急切的“加入”或“子查询”加载样式。当内存中的对象被操作时，我们可以将任何`Address`对象放入`boston_addresses`集合中，而不管`.city`属性是。对象将保留在集合中，直到属性过期并从应用该条件的数据库重新加载。当发生刷新时，无条件刷新`boston_addresses`内部的对象，将主键`user.id`列的值分配到外键持有的`address.user_id`列。`city`条件在这里没有效果，因为 flush 过程只关心将主键值同步到引用外键值中。

创建自定义外部条件[¶](#creating-custom-foreign-conditions "Permalink to this headline")
---------------------------------------------------------------------------------------

主要连接条件的另一个要素是如何确定那些被认为是“外来”的列。通常，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的一些子集将指定[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")，或者以其他方式成为与联接条件相关的[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")的一部分。[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")在它决定应该如何加载和保存这种关系的数据时，会查看这个外键状态。但是，[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")参数可用于创建不涉及任何“模式”级外键的连接条件。我们可以明确地将[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")与[`foreign_keys`](relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")和[`remote_side`](relationship_api.html#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")结合起来，以建立这样的连接。

下面，一个类`HostEntry`连接到它自己，将字符串`content`列等同于`ip_address`列，这是一个名为`INET`我们需要使用[`cast()`](core_sqlelement.html#sqlalchemy.sql.expression.cast "sqlalchemy.sql.expression.cast")来将连接的一边转换为另一边的类型：

    from sqlalchemy import cast, String, Column, Integerplainplain
    from sqlalchemy.orm import relationship
    from sqlalchemy.dialects.postgresql import INET

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class HostEntry(Base):
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

上面的关系会产生一个连接，如：

    SELECT host_entry.id, host_entry.ip_address, host_entry.contentplain
    FROM host_entry JOIN host_entry AS host_entry_1
    ON host_entry_1.ip_address = CAST(host_entry.content AS INET)

An alternative syntax to the above is to use the [`foreign()`](relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")
and [`remote()`](relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")
[annotations](glossary.html#term-annotations), inline within the
[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
expression. 此语法表示[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")通常自身应用于给定[`foreign_keys`](relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")和[`remote_side`](relationship_api.html#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")参数的连接条件的注释。当显式连接条件存在时，这些函数可能更简洁，并且还用于无论该列是多次声明还是在复杂的 SQL 表达式中，都精确地标记“外来”或“远程”列：

    from sqlalchemy.orm import foreign, remote

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

在连接条件[¶](#using-custom-operators-in-join-conditions "Permalink to this headline")中使用自定义运算符
--------------------------------------------------------------------------------------------------------

Another use case for relationships is the use of custom operators, such
as Postgresql’s “is contained within” `<<` operator
when joining with types such as [`postgresql.INET`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.INET "sqlalchemy.dialects.postgresql.INET")
and [`postgresql.CIDR`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.CIDR "sqlalchemy.dialects.postgresql.CIDR").
对于自定义运算符，我们使用[`Operators.op()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")函数：

    inet_column.op("<<")(cidr_column)plain

然而，如果我们使用这个运算符来构造[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")，那么[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")仍然需要更多的信息。This
is because when it examines our primaryjoin condition, it specifically
looks for operators used for **comparisons**, and this is typically a
fixed list containing known comparison operators such as `==`, `<`, etc.
因此，对于我们的自定义操作员参与此系统，我们需要使用[`is_comparison`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")参数将其注册为比较运算符：

    inet_column.op("<<", is_comparison=True)(cidr_column)plainplainplainplain

一个完整的例子：

    class IPA(Base):plainplainplain
        __tablename__ = 'ip_address'

        id = Column(Integer, primary_key=True)
        v4address = Column(INET)

        network = relationship("Network",
                            primaryjoin="IPA.v4address.op('<<', is_comparison=True)"
                                "(foreign(Network.v4representation))",
                            viewonly=True
                        )
    class Network(Base):
        __tablename__ = 'network'

        id = Column(Integer, primary_key=True)
        v4representation = Column(CIDR)

以上，一个查询如：

    session.query(IPA).join(IPA.network)plainplain

将呈现为：

    SELECT ip_address.id AS ip_address_id, ip_address.v4address AS ip_address_v4addressplainplain
    FROM ip_address JOIN network ON ip_address.v4address << network.v4representation

版本 0.9.2 中的新功能： - 添加了[`Operators.op.is_comparison`(core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志来帮助使用自定义运算符创建[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构。

重叠外键[¶](#overlapping-foreign-keys "Permalink to this headline")
-------------------------------------------------------------------

在使用组合外键时会出现一种罕见的情况，例如，一列可能是通过外键约束引用的多列的主题。

Consider an (admittedly complex) mapping such as the
`Magazine` object, referred to both by the
`Writer` object and the `Article` object using a composite primary key scheme that includes
`magazine_id` for both; then to make
`Article` refer to `Writer` as
well, `Article.magazine_id` is involved in two
separate relationships; `Article.magazine` and
`Article.writer`:

    class Magazine(Base):plainplain
        __tablename__ = 'magazine'

        id = Column(Integer, primary_key=True)


    class Article(Base):
        __tablename__ = 'article'

        article_id = Column(Integer)
        magazine_id = Column(ForeignKey('magazine.id'))
        writer_id = Column()

        magazine = relationship("Magazine")
        writer = relationship("Writer")

        __table_args__ = (
            PrimaryKeyConstraint('article_id', 'magazine_id'),
            ForeignKeyConstraint(
                ['writer_id', 'magazine_id'],
                ['writer.id', 'writer.magazine_id']
            ),
        )


    class Writer(Base):
        __tablename__ = 'writer'

        id = Column(Integer, primary_key=True)
        magazine_id = Column(ForeignKey('magazine.id'), primary_key=True)
        magazine = relationship("Magazine")

当上面的映射配置完成后，我们会看到这个警告发出：

    SAWarning: relationship 'Article.writer' will copy columnplain
    writer.magazine_id to column article.magazine_id,
    which conflicts with relationship(s): 'Article.magazine'
    (copies magazine.id to article.magazine_id). Consider applying
    viewonly=True to read-only relationships, or provide a primaryjoin
    condition marking writable columns with the foreign() annotation.

What this refers to originates from the fact that
`Article.magazine_id` is the subject of two
different foreign key constraints; it refers to `Magazine.id` directly as a source column, but also refers to
`Writer.magazine_id` as a source column in the
context of the composite key to `Writer`. If we
associate an `Article` with a particular
`Magazine`, but then associate the
`Article` with a `Writer` that’s
associated with a *different* `Magazine`, the ORM
will overwrite `Article.magazine_id`
non-deterministically, silently changing which magazine we refer
towards; it may also attempt to place NULL into this columnn if we
de-associate a `Writer` from an `Article`. 警告让我们知道这是事实。

为了解决这个问题，我们需要打破`Article`的行为，以包含以下所有三个功能：

1.  `Article` first and foremost writes to
    `Article.magazine_id` based on data persisted in
    the `Article.magazine` relationship only, that
    is a value copied from `Magazine.id`.
2.  `Article` can write to
    `Article.writer_id` on behalf of data persisted
    in the `Article.writer` relationship, but only
    the `Writer.id` column; the
    `Writer.magazine_id` column should not be
    written into `Article.magazine_id` as it
    ultimately is sourced from `Magazine.id`.
3.  `Article` takes `Article.magazine_id` into account when loading `Article.writer`, even though it *doesn’t* write to it on behalf of this
    relationship.

To get just \#1 and \#2, we could specify only
`Article.writer_id` as the “foreign keys” for
`Article.writer`:

    class Article(Base):plainplain
        # ...

        writer = relationship("Writer", foreign_keys='Article.writer_id')

但是，当查询`Writer`时，这会影响`Article.writer`不考虑`Article.magazine_id`：

    SELECT article.article_id AS article_article_id,plainplain
        article.magazine_id AS article_magazine_id,
        article.writer_id AS article_writer_id
    FROM article
    JOIN writer ON writer.id = article.writer_id

因此，为了充分利用＃1，＃2 和＃3，我们通过将[`primaryjoin`(relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")完整地与[`foreign_keys`](relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys "sqlalchemy.orm.relationship")参数，或者通过使用[`foreign()`](relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")进行注释更简洁：

    class Article(Base):plainplain
        # ...

        writer = relationship(
            "Writer",
            primaryjoin="and_(Writer.id == foreign(Article.writer_id), "
                        "Writer.magazine_id == Article.magazine_id)")

版本 1.0.0 中已更改：
ORM 将尝试警告何时将列同时用作来自多个关系的同步目标。

非关系比较/物化路径[¶](#non-relational-comparisons-materialized-path "Permalink to this headline")
--------------------------------------------------------------------------------------------------

警告

本节详细介绍了一个实验功能。

使用自定义表达式意味着我们可以产生不符合常规主/外关键模型的非正统连接条件。一个这样的例子是物化路径模式，在这里我们比较重叠路径令牌的字符串以产生树结构。

通过仔细使用[`foreign()`](relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")和[`remote()`](relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")，我们可以建立一种有效生成基本物化路径系统的关系。基本上，当[`foreign()`](relationship_api.html#sqlalchemy.orm.foreign "sqlalchemy.orm.foreign")和[`remote()`](relationship_api.html#sqlalchemy.orm.remote "sqlalchemy.orm.remote")位于比较表达式的*相同*一侧时，该关系被认为是“one
to 许多”；当他们在*不同*方面时，这种关系被认为是“多对一”。为了比较我们将在这里使用，我们将处理集合，以便将事物配置为“一对多”：

    class Element(Base):plain
        __tablename__ = 'element'

        path = Column(String, primary_key=True)

        descendants = relationship('Element',
                               primaryjoin=
                                    remote(foreign(path)).like(
                                            path.concat('/%')),
                               viewonly=True,
                               order_by=path)

上面，如果给定一个`Element`对象，其路径属性为`"/foo/bar2"`，我们寻找一个`Element.descendants`看起来像：

    SELECT element.path AS element_path
    FROM element
    WHERE element.path LIKE ('/foo/bar2' || '/%') ORDER BY element.path

版本 0.9.5 中的新增功能：已添加支持以允许在 primaryjoin 条件以及使用[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

自我参照多对多关系[¶](#self-referential-many-to-many-relationship "Permalink to this headline")
-----------------------------------------------------------------------------------------------

多对多关系可以由[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")和[`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")中的一个或两个自定义
- 后者对于指定使用[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数。涉及使用[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")和[`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")的常见情况是在建立从类到自身的多对多关系时，如下所示：

    from sqlalchemy import Integer, ForeignKey, String, Column, Table
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    node_to_node = Table("node_to_node", Base.metadata,
        Column("left_node_id", Integer, ForeignKey("node.id"), primary_key=True),
        Column("right_node_id", Integer, ForeignKey("node.id"), primary_key=True)
    )

    class Node(Base):
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        label = Column(String)
        right_nodes = relationship("Node",
                            secondary=node_to_node,
                            primaryjoin=id==node_to_node.c.left_node_id,
                            secondaryjoin=id==node_to_node.c.right_node_id,
                            backref="left_nodes"
        )

如上所述，SQLAlchemy 无法自动知道哪些列应该连接到`right_nodes`和`left_nodes`关系的哪些列。[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")和[`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")参数确定了我们想要如何加入关联表。在上面的声明式表格中，当我们在与`Node`类相对应的 Python 块中声明这些条件时，`id`变量可直接作为[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

Alternatively, we can define the [`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
and [`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")
arguments using strings, which is suitable in the case that our
configuration does not have either the `Node.id`
column object available yet or the `node_to_node`
table perhaps isn’t yet available.
当在一个声明性字符串中引用一个普通的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象时，我们使用该表的字符串名称，因为它存在于[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")中：

    class Node(Base):plainplain
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        label = Column(String)
        right_nodes = relationship("Node",
                            secondary="node_to_node",
                            primaryjoin="Node.id==node_to_node.c.left_node_id",
                            secondaryjoin="Node.id==node_to_node.c.right_node_id",
                            backref="left_nodes"
        )

这里的经典映射情况是类似的，其中`node_to_node`可以连接到`node.c.id`：

    from sqlalchemy import Integer, ForeignKey, String, Column, Table, MetaDataplainplain
    from sqlalchemy.orm import relationship, mapper

    metadata = MetaData()

    node_to_node = Table("node_to_node", metadata,
        Column("left_node_id", Integer, ForeignKey("node.id"), primary_key=True),
        Column("right_node_id", Integer, ForeignKey("node.id"), primary_key=True)
    )

    node = Table("node", metadata,
        Column('id', Integer, primary_key=True),
        Column('label', String)
    )
    class Node(object):
        pass

    mapper(Node, node, properties={
        'right_nodes':relationship(Node,
                            secondary=node_to_node,
                            primaryjoin=node.c.id==node_to_node.c.left_node_id,
                            secondaryjoin=node.c.id==node_to_node.c.right_node_id,
                            backref="left_nodes"
                        )})

请注意，在这两个示例中，[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")关键字指定一个`left_nodes` backref - 当[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")创建反方向的第二个关系时，足以反转[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")和[`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")参数。

复合“次要”加入[¶](#composite-secondary-joins "Permalink to this headline")
--------------------------------------------------------------------------

注意

本节介绍 SQLAlchemy 的一些新增功能和实验功能。

有时，当人们试图在两个表之间建立一个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")时，为了加入它们，需要多于两个或三个表参与。这是[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的一个区域，它试图推动可能的边界，并且通常需要在 SQLAlchemy 邮件列表上敲定这些特殊用例的最终解决方案。

在更新版本的 SQLAlchemy 中，为了提供由多个表组成的复合目标，可以在一些情况下使用[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数。以下是这种连接条件的示例（要求版本 0.9.2 至少按照原样运行）：

    class A(Base):plainplain
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        b_id = Column(ForeignKey('b.id'))

        d = relationship("D",
                    secondary="join(B, D, B.d_id == D.id)."
                                "join(C, C.d_id == D.id)",
                    primaryjoin="and_(A.b_id == B.id, A.id == C.a_id)",
                    secondaryjoin="D.id == B.d_id",
                    uselist=False
                    )

    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)
        d_id = Column(ForeignKey('d.id'))

    class C(Base):
        __tablename__ = 'c'

        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))
        d_id = Column(ForeignKey('d.id'))

    class D(Base):
        __tablename__ = 'd'

        id = Column(Integer, primary_key=True)

In the above example, we provide all three of [`secondary`(relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship"),
[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship"),
and [`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship"),
in the declarative style referring to the named tables `a`, `b`, `c`,
`d` directly. 从`A`到`D`的查询如下所示：

    sess.query(A).join(A.d).all()plain

    SELECT a.id AS a_id, a.b_id AS a_b_id
    FROM a JOIN (
        b AS b_1 JOIN d AS d_1 ON b_1.d_id = d_1.id
            JOIN c AS c_1 ON c_1.d_id = d_1.id)
        ON a.b_id = b_1.id AND a.id = c_1.a_id JOIN d ON d.id = b_1.d_id

在上面的例子中，我们利用能够将多个表填充到“辅助”容器中，以便我们可以跨多个表加入，同时仍然保持[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的“简单”在“左”和“右”方面都有“一张”表；复杂性保持在中间。

版本 0.9.2 中的新功能：支持将[`join()`](core_selectable.html#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")结构直接用作[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数的目标，包括对连接，急切连接和延迟加载的支持，以及在声明式中支持指定复杂条件（如包含类名称作为目标的连接）的支持。

与非主映射器的关系[¶](#relationship-to-non-primary-mapper "Permalink to this headline")
---------------------------------------------------------------------------------------

在上一节中，我们举例说明了一种技术，我们使用[`secondary`(relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")为了在连接条件中放置其他表。有一个复杂的连接案例，即使这种技术是不够的；当我们试图从`A`加入`B`时，可以使用任何数量的`C`，`D`等。在这之间，但是也有`A`和`B` *直接*之间的连接条件。In this case,
the join from `A` to `B` may be
difficult to express with just a complex [`primaryjoin`(relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
condition, as the intermediary tables may need special handling, and it
is also not expressable with a [`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")
object, since the `A->secondary->B` pattern does not
support any references between `A` and `B` directly.
当这个**非常高级的**情况出现时，我们可以求助于创建第二个映射作为关系的目标。这是我们使用[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")的映射，以便映射到包含我们需要的所有附加表的类。为了生成这个映射器作为我们类的“替代”映射，我们使用[`non_primary`](internals.html#sqlalchemy.orm.state.InstanceState.mapper.params.non_primary "sqlalchemy.orm.state.InstanceState.mapper")标志。

下面通过从`A`到`B`的简单连接示出了[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，但是主连接条件增加了两个附加实体`C`和`D`，它们也必须具有与`A`和`B`中的行同时排列的行：

    class A(Base):plainplainplain
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        b_id = Column(ForeignKey('b.id'))

    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)

    class C(Base):
        __tablename__ = 'c'

        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))

    class D(Base):
        __tablename__ = 'd'

        id = Column(Integer, primary_key=True)
        c_id = Column(ForeignKey('c.id'))
        b_id = Column(ForeignKey('b.id'))

    # 1. set up the join() as a variable, so we can refer
    # to it in the mapping multiple times.
    j = join(B, D, D.b_id == B.id).join(C, C.id == D.c_id)

    # 2. Create a new mapper() to B, with non_primary=True.
    # Columns in the join with the same name must be
    # disambiguated within the mapping, using named properties.
    B_viacd = mapper(B, j, non_primary=True, properties={
        "b_id": [j.c.b_id, j.c.d_b_id],
        "d_id": j.c.d_id
        })

    A.b = relationship(B_viacd, primaryjoin=A.b_id == B_viacd.c.b_id)

在上面的例子中，当我们查询时，我们的`B`的非主映射器会发出额外的列；这些可以被忽略：

    sess.query(A).join(A.b).all()plainplainplain

    SELECT a.id AS a_id, a.b_id AS a_b_id
    FROM a JOIN (b JOIN d ON d.b_id = b.id JOIN c ON c.id = d.c_id) ON a.b_id = b.id

构建启用查询的属性[¶](#building-query-enabled-properties "Permalink to this headline")
--------------------------------------------------------------------------------------

非常雄心勃勃的自定义连接条件可能无法直接持久化，并且在某些情况下甚至可能无法正确加载。要移除等式的持久性部分，请在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上使用标记[`viewonly`](relationship_api.html#sqlalchemy.orm.relationship.params.viewonly "sqlalchemy.orm.relationship")，将其建立为只读属性（写入集合的数据将为在 flush()上被忽略）。但是，在极端情况下，请考虑将常规 Python 属性与[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")结合使用，如下所示：

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)

        def _get_addresses(self):
            return object_session(self).query(Address).with_parent(self).filter(...).all()
        addresses = property(_get_addresses)
