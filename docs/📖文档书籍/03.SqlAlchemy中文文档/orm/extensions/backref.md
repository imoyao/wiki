---
title: 将关系与 Backref 关联
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/orm/extensions/backref/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
将关系与 Backref 关联[¶](#linking-relationships-with-backref "Permalink to this headline")
========================================================================================

[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")关键字参数最初是在[Object
Relational
Tutorial](tutorial.html)中引入的，在这里的许多示例中都提到过。它实际上做了什么？让我们从规范的`User`和`Address`场景开始：

    from sqlalchemy import Integer, ForeignKey, String, Columnplainplainplainplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        addresses = relationship("Address", backref="user")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey('user.id'))

上面的配置在`User`上建立了一个名为`User.addresses`的`Address`对象的集合。它还在`Address`上建立一个`.user`属性，它将引用父对象`User`。

实际上，[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")关键字只是在`地址`映射中放置第二个[`关系()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的常见快捷方式，包括建立一个事件两侧的侦听器将镜像两个方向的属性操作。以上配置相当于：

    from sqlalchemy import Integer, ForeignKey, String, Columnplainplainplainplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        addresses = relationship("Address", back_populates="user")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey('user.id'))

        user = relationship("User", back_populates="addresses")

上面，我们明确地向`Address`添加了一个`.user`关系。On both
relationships, the [`back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")
directive tells each relationship about the other one, indicating that
they should establish “bidirectional” behavior between each other.
这种配置的主要作用是关系将事件处理程序添加到两个属性中，这两个属性的行为是“当发生附加或设置事件时，使用这个特定属性名称将自己设置为传入属性”。行为如下所示。从`User`和`Address`实例开始。`.addresses`集合为空，`.user`属性为`None`：

    >>> u1 = User()plainplainplainplainplainplainplain
    >>> a1 = Address()
    >>> u1.addresses
    []
    >>> print(a1.user)
    None

但是，一旦将`Address`追加到`u1.addresses`集合中，集合和标量属性都将被填充：

    >>> u1.addresses.append(a1)plainplainplainplainplainplainplainplainplain
    >>> u1.addresses
    [<__main__.Address object at 0x12a6ed0>]
    >>> a1.user
    <__main__.User object at 0x12a6590>

这种行为当然也适用于移除操作，以及双方的等效操作。例如，当`.user`再次设置为`None`时，`Address`对象将从反向集合中删除：

    >>> a1.user = Noneplainplainplainplainplain
    >>> u1.addresses
    []

对`.addresses`集合和`.user`属性的操作完全在 Python 中进行，没有与 SQL 数据库进行任何交互。如果没有这种行为，一旦数据被刷新到数据库，并且在提交或到期操作发生后重新加载，适当的状态就会显现在两端。[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")
/ [`back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")行为具有以下优点：常见的双向操作可以反映正确的状态，而无需数据库往返。

请记住，当在单个关系上使用[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")关键字时，就好像上面的两个关系是分别使用[`back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")创建的。

Backref 参数[¶](#backref-arguments "Permalink to this headline")
---------------------------------------------------------------

我们已经确定，[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")关键字仅仅是构建彼此引用的两个单独[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构的快捷方式。这种快捷方式的一部分行为是，应用于[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的某些配置参数也将应用于其他方向
- 即描述模式级关系的参数，并且不太可能在相反的方向上是不同的。The usual
case here is a many-to-many [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
that has a [`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")
argument, or a one-to-many or many-to-one which has a
[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
argument (the [`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
argument is discussed in [Specifying Alternate Join
Conditions](join_conditions.html#relationship-primaryjoin)).
例如，如果我们将`Address`对象的列表限制为以“tony”开头的列表：

    from sqlalchemy import Integer, ForeignKey, String, Columnplainplainplainplainplainplainplainplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        addresses = relationship("Address",
                        primaryjoin="and_(User.id==Address.user_id, "
                            "Address.email.startswith('tony'))",
                        backref="user")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey('user.id'))

我们可以通过检查所得到的财产来观察，双方的关系是否适用了这种连接条件：

    >>> print(User.addresses.property.primaryjoin)plainplainplainplainplainplain
    "user".id = address.user_id AND address.email LIKE :email_1 || '%%'
    >>>
    >>> print(Address.user.property.primaryjoin)
    "user".id = address.user_id AND address.email LIKE :email_1 || '%%'
    >>>

This reuse of arguments should pretty much do the “right thing” - it
uses only arguments that are applicable, and in the case of a many-to-
many relationship, will reverse the usage of [`primaryjoin`(relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")
and [`secondaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin "sqlalchemy.orm.relationship")
to correspond to the other direction (see the example in
[Self-Referential Many-to-Many
Relationship](join_conditions.html#self-referential-many-to-many) for
this).

然而，我们常常会指定参数，这些参数仅适用于我们碰巧放置“backref”的那一边。This
includes [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
arguments like [`lazy`](relationship_api.html#sqlalchemy.orm.relationship.params.lazy "sqlalchemy.orm.relationship"),
[`remote_side`](relationship_api.html#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship"),
[`cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")
and [`cascade_backrefs`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade_backrefs "sqlalchemy.orm.relationship").
对于这种情况，我们使用[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数代替字符串：

    # <other imports>plainplainplainplainplainplain
    from sqlalchemy.orm import backref

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)

        addresses = relationship("Address",
                        backref=backref("user", lazy="joined"))

在上面的例子中，我们只在`Address.user`一侧放置了一个`lazy="joined"`指令，表明当对`Address`进行查询时，应自动创建一个到`User`实体的连接，它将填充每个返回的`Address`的`.user`属性。[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数将我们给它的参数格式化为一个由接收[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")解释的形式，作为应用于它创建的新关系的附加参数。

单向后退[¶](#one-way-backrefs "Permalink to this headline")
-----------------------------------------------------------

一种不寻常的情况是“单向后退”。这是 backref 的“back-populating”行为只在一个方向上需要的地方。一个例子是包含一个过滤[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")条件的集合。我们希望根据需要将项追加到此集合中，并让它们在传入对象上填充“父”对象。但是，我们还想拥有不属于集合的项目，但仍具有相同的“父母”关联
- 这些项目不应该在集合中。

以我们前面的例子为例，我们建立了[`primaryjoin`](relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin "sqlalchemy.orm.relationship")，该集合仅限于`Address`对象的电子邮件地址以`tony`开头，通常 backref 行为是所有项目都在两个方向上填充。我们不希望出现类似以下情况的此行为：

    >>> u1 = User()plainplainplainplainplainplainplainplain
    >>> a1 = Address(email='mary')
    >>> a1.user = u1
    >>> u1.addresses
    [<__main__.Address object at 0x1411910>]

以上，`Address`对象与`u1`的`addresses`集合中的条件不匹配。在刷新这些对象之后，提交的事务及其属性在重新加载时到期，`addresses`集合将在下次访问时触发数据库，​​并且不再具有此`Address`对象目前，由于过滤条件。但是，我们可以通过使用两个单独的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构，仅在一侧放置[`back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")来消除 Python 端“backref”行为的这一不需要的一方：

    from sqlalchemy import Integer, ForeignKey, String, Columnplainplainplainplainplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        addresses = relationship("Address",
                        primaryjoin="and_(User.id==Address.user_id, "
                            "Address.email.startswith('tony'))",
                        back_populates="user")

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship("User")

在上面的场景中，将`Address`对象附加到`User`的`.addresses`集合将始终建立`.user`
\>属性在`Address`上：

    >>> u1 = User()plainplainplainplainplainplainplainplainplainplainplainplain
    >>> a1 = Address(email='tony')
    >>> u1.addresses.append(a1)
    >>> a1.user
    <__main__.User object at 0x1411850>

但是，将`User`应用于`Address`的`.user`属性不会将`Address`对象附加到采集：

    >>> a2 = Address(email='mary')plainplainplainplainplainplain
    >>> a2.user = u1
    >>> a2 in u1.addresses
    False

Of course, we’ve disabled some of the usefulness of [`backref`(relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")
here, in that when we do append an `Address` that
corresponds to the criteria of `email.startswith('tony')`, it won’t show up in the `User.addresses`
collection until the session is flushed, and the attributes reloaded
after a commit or expire operation.
虽然我们可以考虑一个在 Python 中检查这个标准的属性事件，但它开始跨越 Python 中复制太多 SQL 行为的路线。backref 行为本身只是对这种哲学的轻微超越
- SQLAlchemy 试图将这些原则保持在最低水平。
