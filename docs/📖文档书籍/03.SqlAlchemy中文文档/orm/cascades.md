---
title: 级联
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/orm/cascades/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
级联[¶ T0\>](#cascades "Permalink to this headline")
====================================================

映射器支持在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构上配置 cascade 行为的概念。这涉及如何将相对于特定[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的“父”对象执行的操作传播到由该关系引用的项目（例如“子”对象），并且受到[`relationship.cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")选项。

级联的默认行为仅限于所谓的[save-update](#cascade-save-update)和[merge](#cascade-merge)设置的级联。级联的典型“替代”设置是添加[delete](#cascade-delete)和[delete-orphan](#cascade-delete-orphan)选项；这些设置适用于相关对象，只要它们连接到它们的父级，并且以其他方式删除，它们就会存在。

在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")中使用[`cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")选项配置级联行为：

    class Order(Base):
        __tablename__ = 'order'

        items = relationship("Item", cascade="all, delete-orphan")
        customer = relationship("User", cascade="save-update")

要设置 backref 上的级联，同一个标志可以与[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数一起使用，该函数最终将其参数返回给[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")：

    class Item(Base):plain
        __tablename__ = 'item'

        order = relationship("Order",
                        backref=backref("items", cascade="all, delete-orphan")
                    )

级联的起源

SQLAlchemy 对关系级联行为的概念以及配置它们的选项主要来自 Hibernate
ORM 中的类似功能；
Hibernate 在少数地方引用了“级联”，如[示例：父/子](https://docs.jboss.org/hibernate/orm_3.3/reference/en-US/html/example-parentchild.html)。如果级联令人混淆，我们会参考他们的结论，指出“我们刚才介绍的部分可能有点混乱。但是，实际上，这一切都很好。“

[`cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")的默认值是`save-update merge`。此参数的典型替代设置是`all`或更常见的`all， delete-orphan`。The
`all` symbol is a synonym for
`save-update, merge, refresh-expire, expunge, delete`, and using it in conjunction with `delete-orphan` indicates that the child object should follow along with its
parent in all cases, and be deleted once it is no longer associated with
that parent.

以下小节介绍了可以为[`cascade`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade "sqlalchemy.orm.relationship")参数指定的可用值列表。

保存更新[¶ T0\>](#save-update "Permalink to this headline")
-----------------------------------------------------------

`save-update` cascade indicates that when an object
is placed into a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
via [`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add"),
all the objects associated with it via this [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
should also be added to that same [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session").
假设我们有一个包含两个相关对象`address1`，`address2`的对象`user1`：

    >>> user1 = User()
    >>> address1, address2 = Address(), Address()
    >>> user1.addresses = [address1, address2]

If we add `user1` to a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
it will also add `address1`, `address2` implicitly:

    >>> sess = Session()
    >>> sess.add(user1)
    >>> address1 in sess
    True

`save-update`级联还影响已存在于[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中的对象的属性操作。If
we add a third object, `address3` to the
`user1.addresses` collection, it becomes part of the
state of that [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"):

    >>> address3 = Address()
    >>> user1.append(address3)
    >>> address3 in sess
    >>> True

`save-update` has the possibly surprising behavior
which is that persistent objects which were *removed* from a collection
or in some cases a scalar attribute may also be pulled into the
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
of a parent object; this is so that the flush process may handle that
related object appropriately. 这种情况通常只能在从一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中删除一个对象并添加到另一个时才会出现：

    >>> user1 = sess1.query(User).filter_by(id=1).first()
    >>> address1 = user1.addresses[0]
    >>> sess1.close()   # user1, address1 no longer associated with sess1
    >>> user1.addresses.remove(address1)  # address1 no longer associated with user1
    >>> sess2 = Session()
    >>> sess2.add(user1)   # ... but it still gets added to the new session,
    >>> address1 in sess2  # because it's still "pending" for flush
    True

`save-update`级联在默认情况下处于启用状态，通常视为理所当然；它通过对[`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")的单个调用一次性在该[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")内注册对象的整个结构来简化代码。虽然它可以被禁用，但通常不需要这样做。

One case where `save-update` cascade does sometimes
get in the way is in that it takes place in both directions for
bi-directional relationships, e.g. backrefs, meaning that the
association of a child object with a particular parent can have the
effect of the parent object being implicitly associated with that child
object’s [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session");
this pattern, as well as how to modify its behavior using the
[`cascade_backrefs`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade_backrefs "sqlalchemy.orm.relationship")
flag, is discussed in the section [Controlling Cascade on
Backrefs](#backref-cascade).

删除[¶ T0\>](#delete "Permalink to this headline")
--------------------------------------------------

`delete`级联指示当“父”对象被标记为删除时，其相关的“子”对象也应被标记为删除。例如，如果我们有`User.addresses`与`delete`级联关系的配置关系：

    class User(Base):
        # ...

        addresses = relationship("Address", cascade="save-update, merge, delete")

如果使用上述映射，我们有一个`User`对象和两个相关的`Address`对象：

    >>> user1 = sess.query(User).filter_by(id=1).first()
    >>> address1, address2 = user1.addresses

如果我们将`user1`标记为删除，在刷新操作继续之后，`address1`和`address2`也将被删除：

    >>> sess.delete(user1)
    >>> sess.commit()
    DELETE FROM address WHERE address.id = ?
    ((1,), (2,))
    DELETE FROM user WHERE user.id = ?
    (1,)
    COMMIT

Alternatively, if our `User.addresses` relationship
does *not* have `delete` cascade, SQLAlchemy’s
default behavior is to instead de-associate `address1` and `address2` from `user1` by setting their foreign key reference to `NULL`. 使用如下映射：

    class User(Base):plain
        # ...

        addresses = relationship("Address")

在删除父`User`对象时，`address`中的行不会被删除，而是取消关联：

    >>> sess.delete(user1)
    >>> sess.commit()
    UPDATE address SET user_id=? WHERE address.id = ?
    (None, 1)
    UPDATE address SET user_id=? WHERE address.id = ?
    (None, 2)
    DELETE FROM user WHERE user.id = ?
    (1,)
    COMMIT

`delete` cascade is more often than not used in
conjunction with [delete-orphan](#cascade-delete-orphan) cascade, which
will emit a DELETE for the related row if the “child” object is
deassociated from the parent. `delete`和`delete-orphan`级联的组合涵盖了 SQLAlchemy 必须决定将外键列设置为 NULL 还是完全删除行的两种情况。

ORM 级别“删除”级联与 FOREIGN KEY 级别“ON DELETE”级联

The behavior of SQLAlchemy’s “delete” cascade has a lot of overlap with
the `ON DELETE CASCADE` feature of a database
foreign key, as well as with that of the `ON DELETE SET NULL` foreign key setting when “delete” cascade is not specified.
Database level “ON DELETE” cascades are specific to the “FOREIGN KEY”
construct of the relational database; SQLAlchemy allows configuration of
these schema-level constructs at the [DDL](glossary.html#term-ddl) level
using options on [`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
which are described at [ON UPDATE and ON
DELETE](core_constraints.html#on-update-on-delete).

重要的是要注意 ORM 和关系数据库的“级联”概念之间的区别以及它们如何整合：

-   在关系的**多对一**一侧有效配置数据库级`ON DELETE`级联；也就是说，我们将它配置为相对于`FOREIGN KEY`约束，该约束是关系的“许多”方面。在 ORM 级别，**这个方向是颠倒的**。SQLAlchemy
    handles the deletion of “child” objects relative to a “parent” from
    the “parent” side, which means that `delete` and
    `delete-orphan` cascade are configured on the
    **one-to-many** side.

-   Database level foreign keys with no `ON DELETE`
    setting are often used to **prevent** a parent row from being
    removed, as it would necessarily leave an unhandled related row
    present.
    如果在一对多关系中需要此行为，则 SQLAlchemy 将外键设置为`NULL`的默认行为可以通过以下两种方式之一来捕获：

    > -   最简单也是最常见的就是在数据库模式级别将外键保存列设置为`NOT NULL`。SQLAlchemy 将列设置为 NULL 的尝试将失败并出现简单的 NOT
    >     NULL 约束异常。
    > -   另一种更特殊的方式是将[`passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")标志设置为字符串`"all"`。这具有完全禁用 SQLAlchemy 将外键列设置为 NULL 的行为的效果，并且即使子行存在于内存中，也会为父行发出 DELETE，而不会影响子行。在数据库级外键触发（特殊的`ON DELETE`设置或其他情况）需要全部激活的情况下，这可能是需要的父行被删除的情况。

-   Database level `ON DELETE` cascade is **vastly
    more efficient** than that of SQLAlchemy.
    数据库可以一次跨多个关系链接一系列级联操作；例如如果删除行 A，则可以删除表 B 中的所有相关行，并且所有与这些 B 行中的每一行相关的 C 行以及 on 和 on 都在单个 DELETE 语句的范围内。另一方面，SQLAlchemy 为了完全支持级联删除操作，必须单独加载每个相关集合，以便定位所有可能具有更多相关集合的行。也就是说，SQLAlchemy 不够复杂，无法在此上下文中一次为所有相关行发出 DELETE。

-   SQLAlchemy doesn’t **need** to be this sophisticated, as we instead
    provide smooth integration with the database’s own
    `ON DELETE` functionality, by using the
    [`passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")
    option in conjunction with properly configured foreign key
    constraints. 在这种行为下，SQLAlchemy 只会为[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中已存在的行发出 DELETE；对于任何被卸载的集合，它将它们留给数据库来处理，而不是为它们发出 SELECT。[Using
    Passive
    Deletes](collections.html#passive-deletes)部分提供了此用法的示例。

-   虽然数据库级`ON  T1> 删除 T2>  T0>功能只适用于关系的“多”方，SQLAlchemy的的“删除”梯级具有有限还可以在reverse方向上操作，这意味着它可以在“多”侧配置，以删除“一侧”上的对象，当“多”方被删除。`然而，如果有其他对象从“many”引用这个“one”一侧，这很容易导致违反约束，所以它通常只在关系实际上是“一对一”时才有用。应该使用[`single_parent`](relationship_api.html#sqlalchemy.orm.relationship.params.single_parent "sqlalchemy.orm.relationship")标志为这种情况建立一个 Python 内断言。

当使用[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")时，也使用[`secondary`](relationship_api.html#sqlalchemy.orm.relationship.params.secondary "sqlalchemy.orm.relationship")选项包含多对多表，SQLAlchemy 的删除级联会自动处理此多对多表中的行。就像正如[Deleting
Rows from the Many to Many
Table](basic_relationships.html#relationships-many-to-many-deletion)中所描述的那样，从多对多集合中添加或删除对象会导致 INSERT 或 DELETE 行中的 many-当由于父对象删除操作而激活时，`delete`级联会删除“child”表中的行，但也会删除多对多表中的行。

删除-孤儿[¶ T0\>](#delete-orphan "Permalink to this headline")
--------------------------------------------------------------

`delete-orphan`级联会将行为添加到`delete`级联中，以便将子对象从父级中解除关联时标记为删除，而不仅仅是父级被标记为删除。在处理由其父代“拥有”的相关对象时，这是一个常见功能，使用 NOT
NULL 外键，因此从父集合中删除项目会导致其删除。

`delete-orphan` cascade implies that each child
object can only have one parent at a time, so is configured in the vast
majority of cases on a one-to-many relationship.
将其设置为多对一或多对多的关系更为尴尬；对于这个用例，SQLAlchemy 要求使用[`single_parent`](relationship_api.html#sqlalchemy.orm.relationship.params.single_parent "sqlalchemy.orm.relationship")参数配置[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")，建立 Python 端验证，确保该对象仅与一个父对象关联时间。

合并[¶ T0\>](#merge "Permalink to this headline")
-------------------------------------------------

`merge` cascade 指示[`Session.merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")操作应该从作为[`Session.merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")主题的父级传播引用对象。这个级联也是默认的。

刷新-到期[¶ T0\>](#refresh-expire "Permalink to this headline")
---------------------------------------------------------------

`refresh-expire`是一个不常见的选项，表明[`Session.expire()`](session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")操作应该从父级传播到引用的对象。当使用[`Session.refresh()`](session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")时，被引用的对象只会过期，但不会实际刷新。

抹去[¶ T0\>](#expunge "Permalink to this headline")
---------------------------------------------------

`expunge` cascade indicates that when the parent
object is removed from the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
using [`Session.expunge()`](session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge"),
the operation should be propagated down to referred objects.

控制 Backrefs 上的级联[¶](#controlling-cascade-on-backrefs "Permalink to this headline")
--------------------------------------------------------------------------------------

缺省情况下，[save-update](#cascade-save-update)级联发生在从 backrefs 发出的属性更改事件上。这可能是一个令人困惑的陈述，通过示范更容易描述；这意味着，给定一个这样的映射：

    mapper(Order, order_table, properties={
        'items' : relationship(Item, backref='order')
    })

If an `Order` is already in the session, and is
assigned to the `order` attribute of an
`Item`, the backref appends the `Item` to the `items` collection of that
`Order`, resulting in the `save-update` cascade taking place:

    >>> o1 = Order()plain
    >>> session.add(o1)
    >>> o1 in session
    True

    >>> i1 = Item()
    >>> i1.order = o1
    >>> i1 in o1.items
    True
    >>> i1 in session
    True

使用[`cascade_backrefs`](relationship_api.html#sqlalchemy.orm.relationship.params.cascade_backrefs "sqlalchemy.orm.relationship")标志可禁用此行为：

    mapper(Order, order_table, properties={
        'items' : relationship(Item, backref='order',
                                    cascade_backrefs=False)
    })

如上所述，`i1.order = o1`的分配将会附加`i1` `o1`的`items`集合，但不会将`i1`添加到会话中。You can, of course, [`add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")
`i1` to the session at a later point.
此选项可能有助于在对象需要在会话结束之前保持在会话之外的情况，但仍需要将对象关联到目标会话中已经存在的对象。
