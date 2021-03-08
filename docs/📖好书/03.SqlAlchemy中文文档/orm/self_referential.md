---
title: 邻接列表关系
date: 2021-02-20 22:41:46
permalink: /sqlalchemy/orm/self_referential/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
邻接列表关系[¶](#adjacency-list-relationships "Permalink to this headline")
===========================================================================

**邻接列表**模式是一种常见的关系模式，表中包含对其自身的外键引用。这是在平坦表格中表示分层数据的最常见方式。其他方法包括**嵌套集合**，有时称为“修改前序”，以及**物化路径**。尽管修改前序在 SQL 查询中对其流畅性进行评估时具有吸引力，但由于并发性，复杂性以及修改后的前序几乎没有优势，所以邻接列表模型可能是大多数分层存储需求最合适的模式通过可以将子树完全加载到应用程序空间的应用程序。

在这个例子中，我们将使用一个名为`Node`的映射类来表示一个树结构：

    class Node(Base):plain
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        data = Column(String(50))
        children = relationship("Node")

有了这个结构，一个图形如下：

    root --+---> child1plainplain
           +---> child2 --+--> subchild1
           |              +--> subchild2
           +---> child3

将用以下数据表示：

    id       parent_id     dataplainplainplainplain
    ---      -------       ----
    1        NULL          root
    2        1             child1
    3        1             child2
    4        3             subchild1
    5        3             subchild2
    6        1             child3

这里[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")配置与“正常”一对多关系的工作方式相同，除了“方向”，即关系是一对多还是一对多多对一，默认情况下假定为一对多。为了建立多对一的关系，额外的指令被称为[`remote_side`](relationship_api.html#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")，它是[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的集合表明那些应该被认为是“遥远”的那些：

    class Node(Base):plainplainplain
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        data = Column(String(50))
        parent = relationship("Node", remote_side=[id])

在上面的情况中，`id`列作为`parent` [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的[`remote_side`](relationship_api.html#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")应用，从而建立`parent_id`作为“本地”一方，然后该关系表现为多对一。

与往常一样，可以使用[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数将两个方向组合为双向关系：

    class Node(Base):plainplain
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        data = Column(String(50))
        children = relationship("Node",
                    backref=backref('parent', remote_side=[id])
                )

SQLAlchemy 中包含几个例子来说明自我指涉策略；这些包括[Adjacency
List](examples.html#examples-adjacencylist)和[XML
Persistence](examples.html#examples-xmlpersistence)。

复合邻接表[¶](#composite-adjacency-lists "Permalink to this headline")
----------------------------------------------------------------------

邻接列表关系的子类别是连接条件的“本地”和“远程”两侧都存在特定列的罕见情况。一个例子是下面的`Folder`类；使用复合主键，`account_id`列引用自身，以指示与父文件位于同一帐户内的子文件夹；而`folder_id`指的是该帐户中的特定文件夹：

    class Folder(Base):plain
        __tablename__ = 'folder'
        __table_args__ = (
          ForeignKeyConstraint(
              ['account_id', 'parent_id'],
              ['folder.account_id', 'folder.folder_id']),
        )

        account_id = Column(Integer, primary_key=True)
        folder_id = Column(Integer, primary_key=True)
        parent_id = Column(Integer)
        name = Column(String)

        parent_folder = relationship("Folder",
                            backref="child_folders",
                            remote_side=[account_id, folder_id]
                      )

上面，我们将`account_id`传递到[`remote_side`](relationship_api.html#sqlalchemy.orm.relationship.params.remote_side "sqlalchemy.orm.relationship")列表中。[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")识别这里的`account_id`列位于两侧，并将“remote”列与`folder_id`列对齐，承认在“远程”方面是唯一存在的。

0.8 版新增功能：支持[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")中的自引用组合键，其中列指向自身。

自引用查询策略[¶](#self-referential-query-strategies "Permalink to this headline")
----------------------------------------------------------------------------------

查询自引用结构的工作方式与其他查询类似：

    # get all nodes named 'child2'plain
    session.query(Node).filter(Node.data=='child2')

但是，当试图沿着外键从树的一级连接到下一级时，需要格外小心。在 SQL 中，从表到它自身的连接要求表达式的至少一侧是“别名”，以便可以毫不含糊地引用它。

回顾 ORM 教程中的[Using
Aliases](tutorial.html#ormtutorial-aliases)，[`orm.aliased()`](query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")构造通常用于提供 ORM 实体的“别名”。使用这种技术从`Node`加入自己的过程如下所示：

    from sqlalchemy.orm import aliasedplainplainplain

    nodealias = aliased(Node)
    sqlsession.query(Node).filter(Node.data=='subchild1').\
                    join(nodealias, Node.parent).\
                    filter(nodealias.data=="child2").\
                    all()
    SELECT node.id AS node_id,
            node.parent_id AS node_parent_id,
            node.data AS node_data
    FROM node JOIN node AS node_1
        ON node.parent_id = node_1.id
    WHERE node.data = ?
        AND node_1.data = ?
    ['subchild1', 'child2']

[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
also includes a feature known as [`Query.join.aliased`(query.html#sqlalchemy.orm.query.Query.join.params.aliased "sqlalchemy.orm.query.Query.join")
that can shorten the verbosity self- referential joins, at the expense
of query flexibility.
此功能执行与上述相似的“别名”步骤，而不需要明确的实体。调用[`Query.filter()`](query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")以及在别名连接之后的类似操作将**将`Node`实体修改为别名的实体：**

    sqlsession.query(Node).filter(Node.data=='subchild1').\plainplain
            join(Node.parent, aliased=True).\
            filter(Node.data=='child2').\
            all()
    SELECT node.id AS node_id,
            node.parent_id AS node_parent_id,
            node.data AS node_data
    FROM node
        JOIN node AS node_1 ON node_1.id = node.parent_id
    WHERE node.data = ? AND node_1.data = ?
    ['subchild1', 'child2']

要将标准添加到更长连接的多个点，请将[`Query.join.from_joinpoint`](query.html#sqlalchemy.orm.query.Query.join.params.from_joinpoint "sqlalchemy.orm.query.Query.join")添加到其他[`join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")调用中：

    # get all nodes named 'subchild1' with aplain
    # parent named 'child2' and a grandparent 'root'
    sqlsession.query(Node).\
            filter(Node.data=='subchild1').\
            join(Node.parent, aliased=True).\
            filter(Node.data=='child2').\
            join(Node.parent, aliased=True, from_joinpoint=True).\
            filter(Node.data=='root').\
            all()
    SELECT node.id AS node_id,
            node.parent_id AS node_parent_id,
            node.data AS node_data
    FROM node
        JOIN node AS node_1 ON node_1.id = node.parent_id
        JOIN node AS node_2 ON node_2.id = node_1.parent_id
    WHERE node.data = ?
        AND node_1.data = ?
        AND node_2.data = ?
    ['subchild1', 'child2', 'root']

[`Query.reset_joinpoint()`](query.html#sqlalchemy.orm.query.Query.reset_joinpoint "sqlalchemy.orm.query.Query.reset_joinpoint")也会从过滤调用中移除“别名”：

    session.query(Node).\plainplainplain
            join(Node.children, aliased=True).\
            filter(Node.data == 'foo').\
            reset_joinpoint().\
            filter(Node.data == 'bar')

有关使用[`Query.join.aliased`](query.html#sqlalchemy.orm.query.Query.join.params.aliased "sqlalchemy.orm.query.Query.join")沿自连参考节点链任意连接的示例，请参阅[XML
Persistence](examples.html#examples-xmlpersistence)。

配置自引用预加载[¶](#configuring-self-referential-eager-loading "Permalink to this headline")
---------------------------------------------------------------------------------------------

在正常的查询操作期间，使用从父表到子表的连接或外连接进行预先加载关系，从而可以从单个 SQL 语句填充父代及其直接子集合或引用，或者可以为所有直接子集合填充第二个语句。在加入相关项目时，SQLAlchemy 的联接和子查询预加载在所有情况下使用别名表，因此与自引用加入兼容。但是，为了使用自引用关系进行加载，需要告诉 SQLAlchemy 应该加入和/或查询多少层；否则急切的负载将不会发生。该深度设置通过[`join_depth`](mapping_api.html#sqlalchemy.orm.mapper.Mapper.relationships.params.join_depth "sqlalchemy.orm.mapper.Mapper.relationships")进行配置：

    class Node(Base):plain
        __tablename__ = 'node'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        data = Column(String(50))
        children = relationship("Node",
                        lazy="joined",
                        join_depth=2)

    sqlsession.query(Node).all()
    SELECT node_1.id AS node_1_id,
            node_1.parent_id AS node_1_parent_id,
            node_1.data AS node_1_data,
            node_2.id AS node_2_id,
            node_2.parent_id AS node_2_parent_id,
            node_2.data AS node_2_data,
            node.id AS node_id,
            node.parent_id AS node_parent_id,
            node.data AS node_data
    FROM node
        LEFT OUTER JOIN node AS node_2
            ON node.id = node_2.parent_id
        LEFT OUTER JOIN node AS node_1
            ON node_2.id = node_1.parent_id
    []
