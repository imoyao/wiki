---
title: 订购清单
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/extensions/orderinglist/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
订购清单[¶](#module-sqlalchemy.ext.orderinglist "Permalink to this headline")
=============================================================================

管理包含元素的索引/位置信息的自定义列表。

作者：Jason Kirtland

`orderinglist` is a helper for mutable ordered
relationships. 它将拦截在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")管理的集合上执行的列表操作，并自动将列表位置中的更改同步到目标标量属性上。

示例：一个`slide`表，其中每一行引用相关`bullet`表中的零个或多个条目。幻灯片中的项目符号将根据`bullet`表中的`position`列的值依次显示。当条目在内存中重新排序时，`position`属性的值应该更新以反映新的排序顺序：

    Base = declarative_base()plainplainplainplainplainplainplainplainplain

    class Slide(Base):
        __tablename__ = 'slide'

        id = Column(Integer, primary_key=True)
        name = Column(String)

        bullets = relationship("Bullet", order_by="Bullet.position")

    class Bullet(Base):
        __tablename__ = 'bullet'
        id = Column(Integer, primary_key=True)
        slide_id = Column(Integer, ForeignKey('slide.id'))
        position = Column(Integer)
        text = Column(String)

标准关系映射将在包含所有相关的`Bullet`对象的每个`Slide`上产生一个类似列表的属性，但不会自动处理排序中的更改。当将`Bullet`附加到`Slide.bullets`时，`Bullet.position`属性将保持未设置状态，直到手动分配。当`Bullet`插入列表中间时，以下`Bullet`对象也需要重新编号。

[`OrderingList`](#sqlalchemy.ext.orderinglist.OrderingList "sqlalchemy.ext.orderinglist.OrderingList")对象自动执行此任务，管理集合中所有`Bullet`对象上的`position`属性。它是使用[`ordering_list()`](#sqlalchemy.ext.orderinglist.ordering_list "sqlalchemy.ext.orderinglist.ordering_list")工厂构造的：

    from sqlalchemy.ext.orderinglist import ordering_listplainplainplainplainplain

    Base = declarative_base()

    class Slide(Base):
        __tablename__ = 'slide'

        id = Column(Integer, primary_key=True)
        name = Column(String)

        bullets = relationship("Bullet", order_by="Bullet.position",
                                collection_class=ordering_list('position'))

    class Bullet(Base):
        __tablename__ = 'bullet'
        id = Column(Integer, primary_key=True)
        slide_id = Column(Integer, ForeignKey('slide.id'))
        position = Column(Integer)
        text = Column(String)

通过上面的映射，管理`Bullet.position`属性：

    s = Slide()plainplainplainplainplainplainplainplain
    s.bullets.append(Bullet())
    s.bullets.append(Bullet())
    s.bullets[1].position
    >>> 1
    s.bullets.insert(1, Bullet())
    s.bullets[2].position
    >>> 2

[`OrderingList`](#sqlalchemy.ext.orderinglist.OrderingList "sqlalchemy.ext.orderinglist.OrderingList")构造仅适用于集合中的**更改**，而不是数据库中的初始加载，并且要求列表在加载时排序。因此，请务必在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上针对目标排序属性指定`order_by`，以便在首次加载时排序正确。

警告

[`OrderingList`](#sqlalchemy.ext.orderinglist.OrderingList "sqlalchemy.ext.orderinglist.OrderingList")
only provides limited functionality when a primary key column or unique
column is the target of the sort. 不支持或存在问题的操作包括：

> -   两个条目必须交换价值。这在主键或唯一约束的情况下不直接支持，因为这意味着至少需要先暂时删除一行，或者在交换机发生时将其更改为第三个中性值。
> -   必须删除一个条目才能为新条目腾出空间。SQLAlchemy 的工作单元在单次刷新内的 DELETE 之前执行所有 INSERT。在主键的情况下，它将交易 UPDATE 语句的同一主键的 INSERT
>     /
>     DELETE，以减少此限制的影响，但这不会发生在 UNIQUE 列上。未来的功能将允许“DELETE
>     before
>     INSERT”行为成为可能，以缓解这一限制，虽然此功能要求在映射器级别对要以这种方式处理的列组进行显式配置。

[`ordering_list()`](#sqlalchemy.ext.orderinglist.ordering_list "sqlalchemy.ext.orderinglist.ordering_list")
takes the name of the related object’s ordering attribute as an
argument. 默认情况下，[`ordering_list()`](#sqlalchemy.ext.orderinglist.ordering_list "sqlalchemy.ext.orderinglist.ordering_list")中对象位置的从零开始的整数索引与排序属性同步：索引 0 将获得位置 0，索引 1 位置 1 等。要开始以 1 或其他整数进行编号，请提供`count_from=1`。

API 参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

 `sqlalchemy.ext.orderinglist.`{.descclassname}`ordering_list`{.descname}(*attr*, *count\_from=None*, *\*\*kw*)[¶](#sqlalchemy.ext.orderinglist.ordering_list "Permalink to this definition")
:   准备一个用于映射器定义的[`OrderingList`](#sqlalchemy.ext.orderinglist.OrderingList "sqlalchemy.ext.orderinglist.OrderingList")工厂。

    返回适合用作Mapper关系的`collection_class`选项参数的对象。例如。：plainplain

        from sqlalchemy.ext.orderinglist import ordering_list

        class Slide(Base):
            __tablename__ = 'slide'

            id = Column(Integer, primary_key=True)
            name = Column(String)

            bullets = relationship("Bullet", order_by="Bullet.position",
                                    collection_class=ordering_list('position'))

    参数：

    -   **attr**[¶](#sqlalchemy.ext.orderinglist.ordering_list.params.attr)
        – Name of the mapped attribute to use for storage and retrieval
        of ordering information
    -   **count\_from**[¶](#sqlalchemy.ext.orderinglist.ordering_list.params.count_from)
        – Set up an integer-based ordering, starting at
        `count_from`.
        例如，`orders_list（'pos'， count_from = 1）`会在SQL中创建一个基于1的列表，将值存储在'
        pos'栏。如果提供`ordering_func`，则忽略。

    其他参数传递给[`OrderingList`](#sqlalchemy.ext.orderinglist.OrderingList "sqlalchemy.ext.orderinglist.OrderingList")构造函数。

`sqlalchemy.ext.orderinglist。`{.descclassname} `count_from_0`{.descname} （ *index*，*collection* ） T5\> [¶ T6\>](#sqlalchemy.ext.orderinglist.count_from_0 "Permalink to this definition")
:   编号功能：从 0 开始的连续整数。

`sqlalchemy.ext.orderinglist。`{.descclassname} `count_from_1`{.descname} （ *index*，*collection* ） T5\> [¶ T6\>](#sqlalchemy.ext.orderinglist.count_from_1 "Permalink to this definition")
:   编号功能：从 1 开始的连续整数。

`sqlalchemy.ext.orderinglist。 T0>  count_from_n_factory  T1> （ T2> 启动 T3> ） T4> ¶< / T5>`{.descclassname}
:   编号功能：从任意启动开始的连续整数。

 *class*`sqlalchemy.ext.orderinglist.`{.descclassname}`OrderingList`{.descname}(*ordering\_attr=None*, *ordering\_func=None*, *reorder\_on\_append=False*)[¶](#sqlalchemy.ext.orderinglist.OrderingList "Permalink to this definition")
:   基础：`__builtin__.list`

    管理其子女的位置信息的自定义列表。plainplainplainplainplainplainplainplainplainplainplainplain

    [`OrderingList`](#sqlalchemy.ext.orderinglist.OrderingList "sqlalchemy.ext.orderinglist.OrderingList")对象通常使用[`ordering_list()`](#sqlalchemy.ext.orderinglist.ordering_list "sqlalchemy.ext.orderinglist.ordering_list")工厂函数设置，与[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")函数结合使用。

    `__ init __`{.descname} （ *ordering\_attr = None*，*ordering\_func = None*，*reorder\_on\_append = False* ） T5\> [¶ T6\>](#sqlalchemy.ext.orderinglist.OrderingList.__init__ "Permalink to this definition")
    :   管理其子女的位置信息的自定义列表。

        `OrderingList` is a
        `collection_class` list implementation that
        syncs position in a Python list with a position attribute on the
        mapped objects.

        这个实现依赖于以正确的顺序开始的列表，所以**确定**在你的关系上放置一个`order_by`。

        参数：

        -   **ordering\_attr**
            [¶](#sqlalchemy.ext.orderinglist.OrderingList.params.ordering_attr)
            - 关系中存储对象顺序的属性的名称。
        -   **ordering\_func**
            [¶](#sqlalchemy.ext.orderinglist.OrderingList.params.ordering_func)
            -

            可选的。将Python列表中的位置映射到要存储在`ordering_attr`中的值的函数。返回的值通常是（但不一定是！）整数。

            使用两个位置参数调用`ordering_func`：列表中元素的索引和列表本身。

            如果省略，则Python列表索引用于属性值。该模块提供了两种基本的预置编号功能：`count_from_0`和`count_from_1`。更多奇异的例子，如步进编号，字母和斐波那契编号，请参阅单元测试。

        -   **reorder\_on\_append**
            [¶](#sqlalchemy.ext.orderinglist.OrderingList.params.reorder_on_append)
            -

            默认为False。当附加一个具有现有（非无）排序值的对象时，除非`reorder_on_append`为真，否则该值将保持不变。这是一种优化，可以避免各种危险的意外数据库写入。

            当你的对象加载时，SQLAlchemy会通过append()将实例添加到列表中。如果由于某种原因，数据库中的结果集跳过了排序步骤（比如说，行'1'丢失，但您得到'2'，'3'和'4'），reorder\_on\_append
            =
            True会立即重新编号项目到'1'，'2'，'3'。如果您有多个会话进行更改，其中任何一个会偶尔加载此集合，但所有会话都会尝试“清除”其提交中的编号，可能会导致除一个之外的所有会话都发生并发修改错误。

            建议使用False默认值，如果您正在对之前已排序的实例执行`append()`操作，或者在手动执行sql之后执行一些内务操作，则只需调用`reorder()`操作。

    `追加 T0> （ T1> 实体 T2> ） T3> ¶ T4>`{.descname}
    :   L.append（object） - 追加对象结束

    `插入`{.descname} （ *索引*，*实体* ） [¶](#sqlalchemy.ext.orderinglist.OrderingList.insert "Permalink to this definition")
    :   L.insert（index，object） - 在索引之前插入对象

     `pop`{.descname}([*index*]) → item -- remove and return item at index (default last).[¶](#sqlalchemy.ext.orderinglist.OrderingList.pop "Permalink to this definition")
    :   如果列表为空或索引超出范围，则引发IndexError。

    `除去 T0> （ T1> 实体 T2> ） T3> ¶ T4>`{.descname}
    :   L.remove（价值） -
        删除第一次出现的价值。如果值不存在，则引发ValueError。

    `重排序 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   同步整个集合的排序。

        扫描列表并确保每个对象都有准确的订购信息集。


