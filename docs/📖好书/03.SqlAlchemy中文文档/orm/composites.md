---
title: 复合列类型
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/orm/composites/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
复合列类型[¶](#composite-column-types "Permalink to this headline")
===================================================================

一组列可以与单个用户定义的数据类型相关联。ORM 提供了一个单一的属性，它表示使用您提供的类的列组。

在版本 0.7 中更改：复合材料已经过简化，不再“隐藏”基础列的属性。另外，就地突变不再是自动的；请参阅以下关于启用可变性以支持就地更改跟踪的部分。

在版本 0.9 中更改：在面向列的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")构造中使用时，复合材料将返回它们的对象形式，而不是单个列。请参阅[Composite
attributes are now returned as their object form when queried on a
per-attribute
basis](changelog_migration_09.html#migration-2824)查询时，复合属性现在以其对象形式返回。

一个简单的例子表示成对的列作为`Point`对象。`Point`表示如`.x`和`.y`这样的一对：

    class Point(object):plain
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __composite_values__(self):
            return self.x, self.y

        def __repr__(self):
            return "Point(x=%r, y=%r)" % (self.x, self.y)

        def __eq__(self, other):
            return isinstance(other, Point) and \
                other.x == self.x and \
                other.y == self.y

        def __ne__(self, other):
            return not self.__eq__(other)

自定义数据类型类的要求是它有一个构造函数，它接受与其列格式相对应的位置参数，并且还提供了一个方法`__composite_values__()`，它将对象的状态作为列表或元组返回，按照其基于列的属性。它还应提供足够的`__eq__()`和`__ne__()`方法来测试两个实例的相等性。

我们将创建一个映射到一个表`vertices`，它将两个点表示为`x1/y1`和`x2/y2`。这些通常被创建为[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象。然后，[`composite()`](#sqlalchemy.orm.composite "sqlalchemy.orm.composite")函数用于分配新属性，这些新属性将通过`Point`类表示一组列。

    from sqlalchemy import Column, Integerplainplain
    from sqlalchemy.orm import composite
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Vertex(Base):
        __tablename__ = 'vertices'

        id = Column(Integer, primary_key=True)
        x1 = Column(Integer)
        y1 = Column(Integer)
        x2 = Column(Integer)
        y2 = Column(Integer)

        start = composite(Point, x1, y1)
        end = composite(Point, x2, y2)

上面的经典映射会根据现有表定义每个[`composite()`](#sqlalchemy.orm.composite "sqlalchemy.orm.composite")：

    mapper(Vertex, vertices_table, properties={
        'start':composite(Point, vertices_table.c.x1, vertices_table.c.y1),
        'end':composite(Point, vertices_table.c.x2, vertices_table.c.y2),
    })

We can now persist and use `Vertex` instances, as
well as query for them, using the `.start` and
`.end` attributes against ad-hoc `Point` instances:

    >>> v = Vertex(start=Point(3, 4), end=Point(5, 6))plainplainplain
    >>> session.add(v)
    >>> q = session.query(Vertex).filter(Vertex.start == Point(3, 4))
    sql>>> print(q.first().start)
    BEGIN (implicit)
    INSERT INTO vertices (x1, y1, x2, y2) VALUES (?, ?, ?, ?)
    (3, 4, 5, 6)
    SELECT vertices.id AS vertices_id,
            vertices.x1 AS vertices_x1,
            vertices.y1 AS vertices_y1,
            vertices.x2 AS vertices_x2,
            vertices.y2 AS vertices_y2
    FROM vertices
    WHERE vertices.x1 = ? AND vertices.y1 = ?
     LIMIT ? OFFSET ?
    (3, 4, 1, 0)
    Point(x=3, y=4)

 `sqlalchemy.orm.`{.descclassname}`composite`{.descname}(*class\_*, *\*attrs*, *\*\*kwargs*)[¶](#sqlalchemy.orm.composite "Permalink to this definition")
:   返回一个组合的基于列的属性以用于 Mapper。

    完整的使用示例请参见映射文档部分[Composite Columnplain
    Types](#mapper-composite)。

    [`composite()`](#sqlalchemy.orm.composite "sqlalchemy.orm.composite")返回的[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")是[`CompositeProperty`](internals.html#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty")。

    参数：

    -   **class \_** [¶](#sqlalchemy.orm.composite.params.class_) -
        “复合类型”类。
    -   **\* cols** [¶](#sqlalchemy.orm.composite.params.*cols) -
        要映射的列对象列表。
    -   **active\_history = False**
        [¶](#sqlalchemy.orm.composite.params.active_history) -

        当`True`时，表示标量属性的“上一个”值在替换时应加载，如果尚未加载。查看[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")上的同一个标志。

        版本0.7中更改：此标志特别有意义 - 以前它是占位符。

    -   **group**[¶](#sqlalchemy.orm.composite.params.group) – A group
        name for this property when marked as deferred.
    -   **deferred**[¶](#sqlalchemy.orm.composite.params.deferred) –
        When True, the column property is “deferred”, meaning that it
        does not load immediately, and is instead loaded when the
        attribute is first accessed on an instance.
        另见[`deferred()`](loading_columns.html#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")。
    -   **comparator\_factory**[¶](#sqlalchemy.orm.composite.params.comparator_factory)
        – a class which extends [`CompositeProperty.Comparator`](internals.html#sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator "sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator")
        which provides custom SQL clause generation for comparison
        operations.
    -   **doc**[¶](#sqlalchemy.orm.composite.params.doc) – optional
        string that will be applied as the doc on the class-bound
        descriptor.
    -   **info** [¶](#sqlalchemy.orm.composite.params.info) -

        可选数据字典，将填充到此对象的[`MapperProperty.info`](internals.html#MapperProperty.info "MapperProperty.info")属性中。

        0.8版本中的新功能

    -   **extension**[¶](#sqlalchemy.orm.composite.params.extension) –
        an [`AttributeExtension`](deprecated.html#sqlalchemy.orm.interfaces.AttributeExtension "sqlalchemy.orm.interfaces.AttributeExtension")
        instance, or list of extensions, which will be prepended to the
        list of attribute listeners for the resulting descriptor placed
        on the class. **已过时。 T0\>**请参阅[`AttributeEvents`](events.html#sqlalchemy.orm.events.AttributeEvents "sqlalchemy.orm.events.AttributeEvents")。

跟踪复合材料上的原位变异[¶](#tracking-in-place-mutations-on-composites "Permalink to this headline")
----------------------------------------------------------------------------------------------------

不会自动跟踪现有组合值的就地更改。相反，复合类需要显式地将事件提供给其父对象。通过使用[`MutableComposite`](extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")
mixin，该任务在很大程度上是自动化的，它使用事件将每个用户定义的复合对象与所有父关联相关联。请参阅[Establishing
Mutability on
Composites](extensions_mutable.html#mutable-composites)中的示例。

在版本 0.7 中更改：现有合成值的就地更改不再自动进行跟踪；该功能被[`MutableComposite`](extensions_mutable.html#sqlalchemy.ext.mutable.MutableComposite "sqlalchemy.ext.mutable.MutableComposite")类所取代。

重新定义复合材料的比较操作[¶](#redefining-comparison-operations-for-composites "Permalink to this headline")
------------------------------------------------------------------------------------------------------------

默认情况下，“等于”比较操作会产生所有对应列的“与”。This can be changed
using the `comparator_factory` argument to
[`composite()`](#sqlalchemy.orm.composite "sqlalchemy.orm.composite"), where
we specify a custom [`CompositeProperty.Comparator`](internals.html#sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator "sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator")
class to define existing or new operations.
下面我们说明“大于”运算符，实现与“大于”基数相同的表达式：

    from sqlalchemy.orm.properties import CompositePropertyplain
    from sqlalchemy import sql

    class PointComparator(CompositeProperty.Comparator):
        def __gt__(self, other):
            """redefine the 'greater than' operation"""

            return sql.and_(*[a>b for a, b in
                              zip(self.__clause_element__().clauses,
                                  other.__composite_values__())])

    class Vertex(Base):
        ___tablename__ = 'vertices'

        id = Column(Integer, primary_key=True)
        x1 = Column(Integer)
        y1 = Column(Integer)
        x2 = Column(Integer)
        y2 = Column(Integer)

        start = composite(Point, x1, y1,
                            comparator_factory=PointComparator)
        end = composite(Point, x2, y2,
                            comparator_factory=PointComparator)
