---
title: 基本关系模式
date: 2021-02-20 22:41:39
permalink: /pages/002fd5/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - relationships
---
基本关系模式[¶](#basic-relationship-patterns "Permalink to this headline")
==========================================================================

快速预览基本关系模式。

用于以下各节的导入如下：

    from sqlalchemy import Table, Column, Integer, ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

一对多[¶](#one-to-many "Permalink to this headline")
----------------------------------------------------

一对多关系中，在引用parent表的child表中配置一个外键。[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
指定parent表,作为代表child表的项目集合的引用

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        children = relationship("Child")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))

为了在一对多中建立双向关系，其中“反向”侧（child表）是多对一,
指定附加[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
和用 [`relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")
参数连接俩个表:

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        children = relationship("Child", back_populates="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))
        parent = relationship("Parent", back_populates="children")

`child`将获得具有多对一语义的`parent`属性。

或者，可以在单个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上使用[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")选项，而不使用[`back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")。

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        children = relationship("Child", backref="parent")

多对一[¶](#many-to-one "Permalink to this headline")
----------------------------------------------------

多对一中，在引用child表的parent表中放置外键。[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
在paren表上声明，将创建一个新的标量保持属性：

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)

在俩边通过增加第二个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
并应用 [`relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")
参数 来达到双向行为

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", back_populates="parents")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parents = relationship("Parent", back_populates="child")

或者，可以在单个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上使用[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")参数，例如`Parent.child`。

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", backref="parents")

一对一[¶](#one-to-one "Permalink to this headline")
---------------------------------------------------

一对一本质上是在两边都是标量属性的双向关系。为了实现这一点，放置指示标量属性的[`uselist`](relationship_api.html#sqlalchemy.orm.relationship.params.uselist "sqlalchemy.orm.relationship")标志，来代替“多”侧关系的集合。来将一对多转换为一对一：

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child = relationship("Child", uselist=False, back_populates="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))
        parent = relationship("Parent", back_populates="child")

或者多对一：

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", back_populates="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent = relationship("Parent", back_populates="child", uselist=False)

总之，可以使用[`relationship.backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")和[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数来代替[`relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")方法；要在反向引用上指定`uselist`，请使用[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数：

    from sqlalchemy.orm import backref

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", backref=backref("parent", uselist=False))

多对多[¶](#many-to-many "Permalink to this headline")
-----------------------------------------------------

在“多对多”中，需要在两个类之间添加了一个关联表。关联表由[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数指示。通常，[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")使用与声明性基类关联的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象，以便[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")指令可以定位要链接的远程表：

    association_table = Table('association', Base.metadata,
        Column('left_id', Integer, ForeignKey('left.id')),
        Column('right_id', Integer, ForeignKey('right.id'))
    )

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Child",
                        secondary=association_table)

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)

对于双向关系，关系的两侧都包含集合。使用[`relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")指定，并为每个[`关系()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")指定公共关联表：

    association_table = Table('association', Base.metadata,
        Column('left_id', Integer, ForeignKey('left.id')),
        Column('right_id', Integer, ForeignKey('right.id'))
    )

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship(
            "Child",
            secondary=association_table,
            back_populates="parents")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)
        parents = relationship(
            "Parent",
            secondary=association_table,
            back_populates="children")

当使用[`backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")参数而不是[`relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")时，反向引用将自动对反向关系使用相同的[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数：

    association_table = Table('association', Base.metadata,
        Column('left_id', Integer, ForeignKey('left.id')),
        Column('right_id', Integer, ForeignKey('right.id'))
    )

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Child",
                        secondary=association_table,
                        backref="parents")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)

[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数也接受一个可返回最终参数的callable，只有在首次使用mappers时才会计算。.使用它，稍后我们可以定义`association_table`，只要在所有模块初始化完成后便可调用。

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Child",
                        secondary=lambda: association_table,
                        backref="parents")

使用声明式扩展，传统的“表的字符串名称”也被接受，与存储在`Base.metadata.tables`中的表的名称匹配：

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Child",
                        secondary="association",
                        backref="parents")

### 从多对多表中删除行[¶](#deleting-rows-from-the-many-to-many-table "Permalink to this headline")

对于[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数唯一的行为是指定这里的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")自动受限于INSERT和DELETE语句，因为对象从集合中添加或删除。这里**不需要手动从此表中删除**。从集合中删除记录的操作将影响正在删除的行：

    # row will be deleted from the "secondary" table
    # automatically
    myparent.children.remove(somechild)

经常出现的一个问题是，当子对象直接传递给[`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")时，“secondary”表中的行是如何删除的：

    session.delete(somechild)

这里有几种可能性：

-   如果从`parent`到`child`有[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，但**没有**反向关系对于连接特定的`Child`和每个`Parent`，SQLAlchemy将不会有任何意识到在删除此特定`Child`对象时，它需要维护“secondary”表格，将其链接到`Parent`。将不会删除“secondary”表
-   如果存在将特定 `Child`链接到每个`Parent`的关系，假设它被称为`Child.parents`，SQLAlchemy将默认加载`Child.parents`集合以定位所有`Parent`对象，并从建立此链接的“secondary”表中删除每一行。注意，这种关系不需要是正式的。
    SQLAlchemy严格地关注与正在删除的`Child`对象相关联的每个[`关系()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")。
-   这里更高性能的选择是使用ON DELETE
    CASCADE指令与数据库使用的外键。假设数据库支持此功能，则可以使数据库本身自动删除“辅助”表中的行，作为引用“child”中的行将被删除。可以指示SQLAlchemy使用[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上的[`passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")指令，在`Child.parents`集合中放弃主动加载；有关详细信息，请参阅[使用被动删除](collections.html#passive-deletes)。

再次注意，这些行为 **仅** 与[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")中使用的[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")选项相关。如果处理显式地映射且在相关[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")
选项中 *不* 存在的关联表，可以使用级联规则来自动删除对正在删除的相关实体作出反应的实体——有关此功能的信息，请参阅[Cascades](cascades.html#unitofwork-cascades)。

参阅：
- [在多对多关系中使用级联删除](cascades.html#cascade-delete-many-to-many)
- [在多对多关系中使用外键的 ON DELETE](cascades.html#passive-deletes-many-to-many)

关联对象[¶](#association-object "Permalink to this headline")
-------------------------------------------------------------

关联对象模式是多对多的变体：当关联表包含除左表和右表外键之外的其他列时使用。而不是使用[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")参数，将一个新类直接映射到关联表。关系的左侧通过一对多引用关联对象，关联类通过多对一引用右侧。下面我们示出映射到`Association`类的关联表，这包括被称为`extra_data`的列，它是一个储存在相互关联`Parent`和
`Child`中的string值。

    class Association(Base):
        __tablename__ = 'association'
        left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
        right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
        extra_data = Column(String(50))
        child = relationship("Child")

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Association")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)

一如既往，双向关系使用[`relationship.back_populates`(relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")或[`relationship.backref`](relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")：

    class Association(Base):
        __tablename__ = 'association'
        left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
        right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
        extra_data = Column(String(50))
        child = relationship("Child", back_populates="parents")
        parent = relationship("Parent", back_populates="children")

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Association", back_populates="parent")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)
        parents = relationship("Association", back_populates="child")

以直接形式使用关联模式要求子对象在关联到关联实例之前附加到父对象；类似地，从parent到child的访问通过关联对象：

    # create parent, append a child via association
    p = Parent()
    a = Association(extra_data="some data")
    a.child = Child()
    p.children.append(a)

    # iterate through child objects via association, including association
    # attributes
    for assoc in p.children:
        print(assoc.extra_data)
        print(assoc.child)

为了增强关联对象模式，以便直接访问`Association`对象是可选的，SQLAlchemy提供[（Association
Proxy）关联代理](extensions_associationproxy.html)扩展。此扩展允许配置属性，这些属性将通过单个访问访问两个“hops”，一个hop”到关联的对象，第二个访问目标属性。

警告

关联对象模式**不以将关联表映射为 “secondary”**的单独关系来协调变化。

以下，对`Parent.children`所做的更改不会与在Python中对`Parent.child_associations`或`Child.parent_associations`所做的更改协调；而所有这些关系将自己继续正常工作，在[`会话`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")过期之前，在一个上的更改不会显示在另一个中，通常发生在[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit"):

    class Association(Base):
        __tablename__ = 'association'

        left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
        right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
        extra_data = Column(String(50))

        child = relationship("Child", back_populates="parent_associations")
        parent = relationship("Parent", back_populates="child_associations")

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)

        children = relationship("Child", secondary="association")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)

此外，正如一个关系的更改不会自动反映在其他关系中一样，将相同的数据写入这两个关系也会导致冲突的INSERT或DELETE语句，例如下面的示例中，我们在`Parent`和`Child`对象建立两次相同的关系：

    p1 = Parent()
    c1 = Child()
    p1.children.append(c1)

    # redundant, will cause a duplicate INSERT on Association
    p1.parent_associations.append(Association(child=c1))

如果你知道你在做什么，那么使用上面的映射是很好的，尽管将`viewonly = True`参数应用到“secondary”关系可能是个好主意，以避免冗余更改被记录。然而，为了获得一个万能模式，允许一个简单的两个对象`Parent->Child`关系，同时仍然使用关联对象模式，请使用关联代理扩展，如[Association
Proxy](extensions_associationproxy.html)所述。
