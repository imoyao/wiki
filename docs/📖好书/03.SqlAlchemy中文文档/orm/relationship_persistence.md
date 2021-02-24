---
title: 特殊关系持久性模式
date: 2021-02-20 22:41:45
permalink: /sqlalchemy/orm/relationship_persistence/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
特殊关系持久性模式[¶](#special-relationship-persistence-patterns "Permalink to this headline")
==============================================================================================

指向自己的行/相互依赖的行[¶](#rows-that-point-to-themselves-mutually-dependent-rows "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------

这是一个非常特殊的情况，其中 relationship()必须执行 INSERT 和第二个 UPDATE 才能正确填充行（反之亦然 UPDATE 和 DELETE 才能删除而不违反外键约束）。这两个用例是：

-   一个表包含一个自己的外键，一行将有一个外键值指向自己的主键。
-   每个表包含一个引用另一个表的外键，每个表中的一行引用另一个表。

例如：

              userplainplainplain
    ---------------------------------
    user_id    name   related_user_id
       1       'ed'          1

要么：

                 widget                                                  entryplainplainplainplain
    -------------------------------------------             ---------------------------------
    widget_id     name        favorite_entry_id             entry_id      name      widget_id
       1       'somewidget'          5                         5       'someentry'     1

在第一种情况下，一排指向自己。从技术上讲，使用 PostgreSQL 或 Oracle 等序列的数据库可以使用先前生成的值同时插入行，但依赖于自动增量式主键标识符的数据库不能。[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")总是在刷新过程中假定行数的“父/子”模型，所以除非直接填充主键/外键列，否则[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")需要使用两个语句。

在第二种情况下，必须在引用“条目”行之前插入“小部件”行，但直到生成“条目”行后才能设置该“小部件”行的“favorite\_entry\_id”列。在这种情况下，仅使用两个 INSERT 语句插入“小部件”和“入口”行通常是不可能的；必须执行 UPDATE 以保持实现外键约束。例外情况是，如果外键配置为“延迟到提交”（某些数据库支持的功能），并且手动填充了标识符（本质上绕过[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")）。

为了能够使用补充 UPDATE 语句，我们使用[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的[`post_update`](relationship_api.html#sqlalchemy.orm.relationship.params.post_update "sqlalchemy.orm.relationship")选项。这指定两行之间的链接应该在两行已被 INSERTED 后使用 UPDATE 语句创建；它还会导致在发出 DELETE 之前通过 UPDATE 将行彼此解除关联。The
flag should be placed on just *one* of the relationships, preferably the
many-to-one side.
下面我们举例说明一个完整的例子，包括两个[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")结构：

    from sqlalchemy import Integer, ForeignKey, Columnplainplainplain
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class Entry(Base):
        __tablename__ = 'entry'
        entry_id = Column(Integer, primary_key=True)
        widget_id = Column(Integer, ForeignKey('widget.widget_id'))
        name = Column(String(50))

    class Widget(Base):
        __tablename__ = 'widget'

        widget_id = Column(Integer, primary_key=True)
        favorite_entry_id = Column(Integer,
                                ForeignKey('entry.entry_id',
                                name="fk_favorite_entry"))
        name = Column(String(50))

        entries = relationship(Entry, primaryjoin=
                                        widget_id==Entry.widget_id)
        favorite_entry = relationship(Entry,
                                    primaryjoin=
                                        favorite_entry_id==Entry.entry_id,
                                    post_update=True)

当一个针对上述配置的结构被刷新时，“widget”行将被 INSERT 减去“favorite\_entry\_id”值，然后所有的“entry”行将被 INSERTed 引用父“widget”行，然后将填充 UPDATE 语句“小部件”表的“favorite\_entry\_id”列（暂时为一行）：

    >>> w1 = Widget(name='somewidget')plainplainplainplain
    >>> e1 = Entry(name='someentry')
    >>> w1.favorite_entry = e1
    >>> w1.entries = [e1]
    >>> session.add_all([w1, e1])
    sql>>> session.commit()
    BEGIN (implicit)
    INSERT INTO widget (favorite_entry_id, name) VALUES (?, ?)
    (None, 'somewidget')
    INSERT INTO entry (widget_id, name) VALUES (?, ?)
    (1, 'someentry')
    UPDATE widget SET favorite_entry_id=? WHERE widget.widget_id = ?
    (1, 1)
    COMMIT

我们可以指定的额外配置是在`Widget`上提供更全面的外键约束，这样可以保证`favorite_entry_id`引用`Entry`也指这个`Widget`。我们可以使用复合外键，如下所示：

    from sqlalchemy import Integer, ForeignKey, String, \
            Column, UniqueConstraint, ForeignKeyConstraint
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship

    Base = declarative_base()

    class Entry(Base):
        __tablename__ = 'entry'
        entry_id = Column(Integer, primary_key=True)
        widget_id = Column(Integer, ForeignKey('widget.widget_id'))
        name = Column(String(50))
        __table_args__ = (
            UniqueConstraint("entry_id", "widget_id"),
        )

    class Widget(Base):
        __tablename__ = 'widget'

        widget_id = Column(Integer, autoincrement='ignore_fk', primary_key=True)
        favorite_entry_id = Column(Integer)

        name = Column(String(50))

        __table_args__ = (
            ForeignKeyConstraint(
                ["widget_id", "favorite_entry_id"],
                ["entry.widget_id", "entry.entry_id"],
                name="fk_favorite_entry"
            ),
        )

        entries = relationship(Entry, primaryjoin=
                                        widget_id==Entry.widget_id,
                                        foreign_keys=Entry.widget_id)
        favorite_entry = relationship(Entry,
                                    primaryjoin=
                                        favorite_entry_id==Entry.entry_id,
                                    foreign_keys=favorite_entry_id,
                                    post_update=True)

上面的映射具有桥接`widget_id`和`favorite_entry_id`列的组合[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")。To
ensure that `Widget.widget_id` remains an
“autoincrementing” column we specify [`autoincrement`(core_metadata.html#sqlalchemy.schema.Column.params.autoincrement "sqlalchemy.schema.Column")
to the value `"ignore_fk"` on [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
and additionally on each [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
we must limit those columns considered as part of the foreign key for
the purposes of joining and cross-population.

可变主键/更新级联[¶](#mutable-primary-keys-update-cascades "Permalink to this headline")
----------------------------------------------------------------------------------------

当实体的主键发生变化时，引用主键的相关项目也必须更新。对于强制引用完整性的数据库，最好的策略是使用数据库的 ON
UPDATE CASCADE 功能，以便将主键更改传播到引用的外键 -
这些值在任何时候都不会同步，除非约束被标记为“可延迟”也就是说，在事务完成之前不会强制执行。

It is **highly recommended** that an application which seeks to employ
natural primary keys with mutable values to use the
`ON UPDATE CASCADE` capabilities of the database.
说明这一点的示例映射是：

    class User(Base):plainplainplain
        __tablename__ = 'user'
        __table_args__ = {'mysql_engine': 'InnoDB'}

        username = Column(String(50), primary_key=True)
        fullname = Column(String(100))

        addresses = relationship("Address")


    class Address(Base):
        __tablename__ = 'address'
        __table_args__ = {'mysql_engine': 'InnoDB'}

        email = Column(String(50), primary_key=True)
        username = Column(String(50),
                    ForeignKey('user.username', onupdate="cascade")
                )

Above, we illustrate `onupdate="cascade"` on the
[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
object, and we also illustrate the `mysql_engine='InnoDB'` setting which, on a MySQL backend, ensures that the
`InnoDB` engine supporting referential integrity is
used. 在使用 SQLite 时，应使用[Foreign Key
Support](dialects_sqlite.html#sqlite-foreign-keys)中介绍的配置启用参照完整性。

也可以看看

[Using Passive Deletes](collections.html#passive-deletes) -
支持具有关系的 ON DELETE CASCADE

[`orm.mapper.passive_updates`](mapping_api.html#sqlalchemy.orm.mapper.params.passive_updates "sqlalchemy.orm.mapper")
- [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")

### 模拟有限 ON UPDATE CASCADE，无外键支持[¶](#simulating-limited-on-update-cascade-without-foreign-key-support "Permalink to this headline")

在使用不支持参照完整性的数据库以及具有可变值的自然主键的情况下，SQLAlchemy 提供了一种功能，以允许将主键值传播到已经引用的外键到**通过针对立即引用其值已更改的主键列的外键列发出 UPDATE 语句来限制**范围。当使用`MyISAM`存储引擎时，没有引用完整性功能的主要平台是 MySQL，而`PRAGMA foreign_keys = ON / t2>编译指示不使用。`Oracle 数据库也不支持`ON UPDATE CASCADE`，但由于它仍然强制引用完整性，被标记为可延迟，以便 SQLAlchemy 可以发出 UPDATE 语句。

通过将[`passive_updates`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_updates "sqlalchemy.orm.relationship")标志设置为`False`来启用该功能，最优选为一对多或多对多[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")当“更新”不再是“被动”时，这表明 SQLAlchemy 将针对由具有变化的主键值的父对象引用的集合中引用的对象分别发出 UPDATE 语句。这也意味着集合将被完全加载到内存中（如果尚未本地存在的话）。

我们之前使用`passive_updates=False`的映射如下所示：

    class User(Base):plainplainplain
        __tablename__ = 'user'

        username = Column(String(50), primary_key=True)
        fullname = Column(String(100))

        # passive_updates=False *only* needed if the database
        # does not implement ON UPDATE CASCADE
        addresses = relationship("Address", passive_updates=False)

    class Address(Base):
        __tablename__ = 'address'

        email = Column(String(50), primary_key=True)
        username = Column(String(50), ForeignKey('user.username'))

`passive_updates=False`的主要局限性包括：

-   它比直接数据库 ON UPDATE
    CASCADE 执行得更差，因为它需要使用 SELECT 完全预加载受影响的集合，并且还必须针对这些值发出 UPDATE 语句，它将尝试在“批处理”中运行，但仍然以每次运行在 DBAPI 级别的基础上。
-   该功能不能“级联”多个级别。That is, if mapping X has a foreign key
    which refers to the primary key of mapping Y, but then mapping Y’s
    primary key is itself a foreign key to mapping Z,
    `passive_updates=False` cannot cascade a change
    in primary key value from `Z` to `X`.
-   仅在关系的多对一侧配置`passive_updates=False`不会产生完整效果，因为工作单元仅通过当前标识映射搜索可能引用该对象的对象有一个变异的主键，而不是整个数据库。

As virtually all databases other than Oracle now support
`ON UPDATE CASCADE`, it is highly recommended that
traditional `ON UPDATE CASCADE` support be used in
the case that natural and mutable primary key values are in use.
