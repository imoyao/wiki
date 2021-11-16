---
title: 收集配置和技术
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/faq/collections/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - faq
tags:
---
收集配置和技术[¶](#collection-configuration-and-techniques "Permalink to this headline")
========================================================================================

[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")函数定义两个类之间的链接。当链接定义了一对多或多对多的关系时，当对象被加载和操作时，它被表示为一个 Python 集合。本节介绍有关收集配置和技术的其他信息。

使用大集合[¶](#working-with-large-collections "Permalink to this headline")
---------------------------------------------------------------------------

根据关系的加载策略，[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的默认行为是完全加载项目集合。另外，默认情况下，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")只知道如何删除会话中实际存在的对象。当一个父实例被标记为删除和刷新时，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")加载其子项的完整列表，以便它们可以被删除，或者将其外键值设置为空；这是为了避免违反约束。对于大量子项目，有几种策略可以在加载时间和删除时间内绕过子项目的全部加载。

### 动态关系加载器[¶](#dynamic-relationship-loaders "Permalink to this headline")

实现大型集合管理的关键特征是所谓的“动态”关系。这是[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的一种可选形式，它在访问时返回一个[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象来代替集合。[`filter()`](query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")
criterion may be applied as well as limits and offsets, either
explicitly or via array slices:

    class User(Base):
        __tablename__ = 'user'

        posts = relationship(Post, lazy="dynamic")

    jack = session.query(User).get(id)

    # filter Jack's blog posts
    posts = jack.posts.filter(Post.headline=='this is a post')

    # apply array slices
    posts = jack.posts[5:20]

动态关系通过`append()`和`remove()`方法支持有限的写入操作：

    oldpost = jack.posts.filter(Post.headline=='old post').one()plain
    jack.posts.remove(oldpost)

    jack.posts.append(Post('new post'))

由于动态关系的读取端总是查询数据库，因此在对数据进行刷新之前，对基础集合的更改将不可见。但是，只要在使用中的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")上启用了“autoflush”，每次集合即将发出查询时都会自动发生。

要在后端参考上放置一个动态关系，请将[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")函数与`lazy='dynamic'`结合使用：

    class Post(Base):
        __table__ = posts_table

        user = relationship(User,
                    backref=backref('posts', lazy='dynamic')
                )

请注意，此时，无法将动态/延迟加载选项与动态关系结合使用。

注意

[`dynamic_loader()`](relationship_api.html#sqlalchemy.orm.dynamic_loader "sqlalchemy.orm.dynamic_loader")函数与指定`lazy='dynamic'`参数时的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")基本相同。

警告

“动态”加载器仅适用于**集合**。使用具有多对一，一对一或 uselist =
False 关系的“动态”加载器是无效的。在这些情况下，较新版本的 SQLAlchemy 会发出警告或异常。

### 设置 Noload，RaiseLoad [¶](#setting-noload-raiseload "Permalink to this headline")

即使访问，“noload”关系也不会从数据库加载。它使用`lazy='noload'`配置：

    class MyClass(Base):plain
        __tablename__ = 'some_table'

        children = relationship(MyOtherClass, lazy='noload')

在上面，`children`集合是完全可写的，并且对它的更改将被持久保存到数据库以及本地可用于在添加时读取。但是，当`MyClass`实例刚从数据库加载时，`children`集合保持为空。noload 策略也可以使用[`orm.noload()`](loading_relationships.html#sqlalchemy.orm.noload "sqlalchemy.orm.noload")加载程序选项以查询选项为基础。

或者，“加载”加载关系会引发一个[`InvalidRequestError`{.xref .py .py-exc
.docutils
.literal}](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")，其中属性通常会发出延迟加载：

    class MyClass(Base):plain
        __tablename__ = 'some_table'

        children = relationship(MyOtherClass, lazy='raise')

以上，`children`集合上的属性访问将会引发异常，如果它以前没有被预先加载。这包括读取权限，但对于集合也会影响写入权限，因为集合不能在没有先加载的情况下进行突变。其基本原理是确保应用程序在特定上下文中不发出任何意外的延迟加载。与其不必通过 SQL 日志来确定所有必要的属性已被加载，“提升”策略将导致卸载的属性在被访问时立即引发。通过使用[`orm.raiseload()`](loading_relationships.html#sqlalchemy.orm.raiseload "sqlalchemy.orm.raiseload")加载器选项，查询选项也可以使用提升策略。

版本 1.1 中的新增功能：添加了“引导”加载器策略。

### 使用被动删除[¶](#using-passive-deletes "Permalink to this headline")

使用[`passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")禁用 DELETE 操作上的子对象加载，并结合数据库上的“ON
DELETE（CASCADE | SET NULL）”来自动级联删除子对象：

    class MyClass(Base):plain
        __tablename__ = 'mytable'
        id = Column(Integer, primary_key=True)
        children = relationship("MyOtherClass",
                        cascade="all, delete-orphan",
                        passive_deletes=True)

    class MyOtherClass(Base):
        __tablename__ = 'myothertable'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer,
                    ForeignKey('mytable.id', ondelete='CASCADE')
                        )

注意

要使用“ON DELETE CASCADE”，底层数据库引擎必须支持外键。

-   使用 MySQL 时，必须选择适当的存储引擎。有关详细信息，请参阅[CREATE
    TABLE arguments including Storage
    Engines](dialects_mysql.html#mysql-storage-engines)。
-   在使用 SQLite 时，必须明确启用外键支持。有关详细信息，请参见[Foreign
    Key Support](dialects_sqlite.html#sqlite-foreign-keys)。

当应用[`passive_deletes`](relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes "sqlalchemy.orm.relationship")时，当`MyClass`的实例标记为删除时，`children`关系不会被加载到内存中。The
`cascade="all, delete-orphan"` *will* take effect
for instances of `MyOtherClass` which are currently
present in the session; however for instances of
`MyOtherClass` which are not loaded, SQLAlchemy
assumes that “ON DELETE CASCADE” rules will ensure that those rows are
deleted by the database.

也可以看看

[`orm.mapper.passive_deletes`](mapping_api.html#sqlalchemy.orm.mapper.params.passive_deletes "sqlalchemy.orm.mapper")
- [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")上的类似功能

自定义集合访问[¶](#customizing-collection-access "Permalink to this headline")
------------------------------------------------------------------------------

映射一对多或多对多关系会导致通过父实例上的属性访问值的集合。默认情况下，这个集合是一个`list`：

    class Parent(Base):
        __tablename__ = 'parent'
        parent_id = Column(Integer, primary_key=True)

        children = relationship(Child)

    parent = Parent()
    parent.children.append(Child())
    print(parent.children[0])

集合不限于列表。通过在[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")中指定[`collection_class`](relationship_api.html#sqlalchemy.orm.relationship.params.collection_class "sqlalchemy.orm.relationship")选项，可以使用集合，可变序列和几乎任何其他可充当容器的 Python 对象来代替默认列表：

    class Parent(Base):
        __tablename__ = 'parent'
        parent_id = Column(Integer, primary_key=True)

        # use a set
        children = relationship(Child, collection_class=set)

    parent = Parent()
    child = Child()
    parent.children.add(child)
    assert child in parent.children

### 词典集合[¶](#dictionary-collections "Permalink to this headline")

将字典用作集合时需要一些额外的细节。这是因为对象总是作为列表从数据库加载，并且必须提供密钥生成策略才能正确填充字典。[`attribute_mapped_collection()`](#sqlalchemy.orm.collections.attribute_mapped_collection "sqlalchemy.orm.collections.attribute_mapped_collection")函数是实现简单字典集合的最常见方法。它生成一个字典类，它将映射类的特定属性作为关键字。Below
we map an `Item` class containing a dictionary of
`Note` items keyed to the `Note.keyword` attribute:

    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy.orm.collections import attribute_mapped_collection
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        notes = relationship("Note",
                    collection_class=attribute_mapped_collection('keyword'),
                    cascade="all, delete-orphan")

    class Note(Base):
        __tablename__ = 'note'
        id = Column(Integer, primary_key=True)
        item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
        keyword = Column(String)
        text = Column(String)

        def __init__(self, keyword, text):
            self.keyword = keyword
            self.text = text

`Item.notes` is then a dictionary:

    >>> item = Item()
    >>> item.notes['a'] = Note('a', 'atext')
    >>> item.notes.items()
    {'a': <__main__.Note object at 0x2eaaf0>}

[`attribute_mapped_collection()`](#sqlalchemy.orm.collections.attribute_mapped_collection "sqlalchemy.orm.collections.attribute_mapped_collection")将确保每个`Note`的`.keyword`属性符合字典中的键。例如，当分配给`Item.notes`时，我们提供的字典键必须与实际的`Note`对象匹配：

    item = Item()
    item.notes = {
                'a': Note('a', 'atext'),
                'b': Note('b', 'btext')
            }

[`attribute_mapped_collection()`](#sqlalchemy.orm.collections.attribute_mapped_collection "sqlalchemy.orm.collections.attribute_mapped_collection")用作键的属性根本不需要映射！Using
a regular Python `@property` allows virtually any
detail or combination of details about the object to be used as the key,
as below when we establish it as a tuple of `Note.keyword` and the first ten letters of the `Note.text` field:

    class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        notes = relationship("Note",
                    collection_class=attribute_mapped_collection('note_key'),
                    backref="item",
                    cascade="all, delete-orphan")

    class Note(Base):
        __tablename__ = 'note'
        id = Column(Integer, primary_key=True)
        item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
        keyword = Column(String)
        text = Column(String)

        @property
        def note_key(self):
            return (self.keyword, self.text[0:10])

        def __init__(self, keyword, text):
            self.keyword = keyword
            self.text = text

上面我们添加了一个`Note.item`
backref。指定这种反向关系时，`Note`被添加到`Item.notes`字典中，并且会自动为我们生成密钥：

    >>> item = Item()
    >>> n1 = Note("a", "atext")
    >>> n1.item = item
    >>> item.notes
    {('a', 'atext'): <__main__.Note object at 0x2eaaf0>}

其他内置的字典类型包括[`column_mapped_collection()`](#sqlalchemy.orm.collections.column_mapped_collection "sqlalchemy.orm.collections.column_mapped_collection")，它几乎像[`attribute_mapped_collection()`](#sqlalchemy.orm.collections.attribute_mapped_collection "sqlalchemy.orm.collections.attribute_mapped_collection")，直接给定[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")

    from sqlalchemy.orm.collections import column_mapped_collectionplain

    class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        notes = relationship("Note",
                    collection_class=column_mapped_collection(Note.__table__.c.keyword),
                    cascade="all, delete-orphan")

以及传递任何可调用函数的[`mapped_collection()`](#sqlalchemy.orm.collections.mapped_collection "sqlalchemy.orm.collections.mapped_collection")。请注意，如前所述，使用[`attribute_mapped_collection()`](#sqlalchemy.orm.collections.attribute_mapped_collection "sqlalchemy.orm.collections.attribute_mapped_collection")以及`@property`通常更容易：

    from sqlalchemy.orm.collections import mapped_collectionplain

    class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        notes = relationship("Note",
                    collection_class=mapped_collection(lambda note: note.text[0:10]),
                    cascade="all, delete-orphan")

字典映射通常与“关联代理”扩展结合使用，以产生流线化的字典视图。有关示例，请参见[Proxying
to Dictionary Based
Collections](extensions_associationproxy.html#proxying-dictionaries)和[Composite
Association
Proxies](extensions_associationproxy.html#composite-association-proxy)。

`sqlalchemy.orm.collections。 T0>  attribute_mapped_collection  T1> （ T2>  attr_name  T3> ） T4> ¶< / T5>`{.descclassname}
:   基于属性的键控的基于字典的集合类型。

    使用基于集合中实体的'attr\_name'属性的键值返回[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")工厂，其中`attr_name`是属性的字符串名称。plain

    关键值在对象的生命周期中必须是不可变的。例如，如果这些键值在会话期间发生更改（例如，会话刷新后从无到数据库分配的整数），则无法映射外键值。

`sqlalchemy.orm.collections。 T0>  column_mapped_collection  T1> （ T2>  mapping_spec  T3> ） T4> ¶< / T5>`{.descclassname}
:   基于列的键控的基于字典的集合类型。

    使用从mapping\_spec生成的键控函数返回一个[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")工厂，该工具可能是一列或一列列。plain

    关键值在对象的生命周期中必须是不可变的。例如，如果这些键值在会话期间发生更改（例如，会话刷新后从无到数据库分配的整数），则无法映射外键值。

`sqlalchemy.orm.collections。 T0>  mapped_collection  T1> （ T2>  keyfunc  T3> ） T4> ¶< / T5>`{.descclassname}
:   基于字典的具有任意键控的集合类型。

    返回带有从keyfunc生成的键控函数的[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")工厂，这是一个可调用的实体，它返回一个实体并返回一个键值。

    关键值在对象的生命周期中必须是不可变的。例如，如果这些键值在会话期间发生更改（例如，会话刷新后从无到数据库分配的整数），则无法映射外键值。

自定义集合实现[¶](#custom-collection-implementations "Permalink to this headline")
----------------------------------------------------------------------------------

您也可以将自己的类型用于收藏。在简单情况下，从`list`或`set`进行插入，添加自定义行为是所有必需的。在其他情况下，需要特殊的装饰器来告诉 SQLAlchemy 有关集合如何操作的更多细节。

我需要一个自定义集合实现吗？

在大多数情况下，根本不是！“自定义”集合的最常见用例是将传入值验证或编组为新的表单，例如成为类实例的字符串，或者以某种方式在内部代表数据的字符串，在不同形式的外部呈现该数据的“视图”。

对于第一个用例，[`orm.validates()`](mapped_attributes.html#sqlalchemy.orm.validates "sqlalchemy.orm.validates")装饰器是迄今为止在所有情况下为验证和简单编组而截取传入值的最简单方法。有关此示例，请参阅[Simple
Validators](mapped_attributes.html#simple-validators)。

For the second use case, the [Association
Proxy](extensions_associationproxy.html) extension is a well-tested,
widely used system that provides a read/write “view” of a collection in
terms of some attribute present on the target object.
由于目标属性可以是返回几乎任何东西的`@property`，因此只需几个函数就可以构建一个集合的一系列“替代”视图。这种方法使底层映射集合不受影响，并且避免了在逐个方法的基础上仔细调整集合行为的需要。

当集合需要在访问或变异操作时具有特殊行为时，自定义集合非常有用，否则这些操作无法在集合的外部进行建模。他们当然可以结合上述两种方法。

SQLAlchemy 中的集合是透明的*检测*。仪表意味着对集合上的正常操作进行跟踪，并导致在刷新时刻将更改写入数据库。此外，收集操作可以触发*事件*，这表明必须进行一些辅助操作。辅助操作的例子包括将子项保存在父节点的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中（即`save-update`级联），以及同步双向关系的状态（即[`backref()`](relationship_api.html#sqlalchemy.orm.backref "sqlalchemy.orm.backref")）。

集合包理解列表，集合和字典的基本接口，并将自动将检测应用于这些内置类型及其子类。实现基本集合接口的对象派生类型通过鸭式输入进行检测和检测：

    class ListLike(object):
        def __init__(self):
            self.data = []
        def append(self, item):
            self.data.append(item)
        def remove(self, item):
            self.data.remove(item)
        def extend(self, items):
            self.data.extend(items)
        def __iter__(self):
            return iter(self.data)
        def foo(self):
            return 'foo'

`append`，`remove`和`extend`是已知的类列表方法，并将自动进行检测。`__iter__`不是一个增变器方法，不会被检测，而且`foo`也不会。

当然，鸭子输入（即猜测）并不稳定，所以你可以通过提供一个`__emulates__` class 属性来明确你正在实现的接口：

    class SetLike(object):plain
        __emulates__ = set

        def __init__(self):
            self.data = set()
        def append(self, item):
            self.data.add(item)
        def remove(self, item):
            self.data.remove(item)
        def __iter__(self):
            return iter(self.data)

由于`append`，这个类看起来像列表一样，但是`__emulates__`强制它设置为类似的。`remove`已知是设置界面的一部分，并将进行检测。

但是这个类还不行：需要一点点粘合剂才能适应 SQLAlchemy 的使用。ORM 需要知道使用哪些方法来追加，删除和迭代集合的成员。当使用像`list`或`set`这样的类型时，适当的方法是众所周知的，并在出现时自动使用。这个集合类没有提供预期的`add`方法，因此我们必须通过装饰器为 ORM 提供显式映射。

### 通过装饰器注释自定义集合[¶](#annotating-custom-collections-via-decorators "Permalink to this headline")

装饰器可用于标记 ORM 管理集合所需的各种方法。当你的课堂并不完全满足其容器类型的常规界面，或者你想用另一种方法完成工作时使用它们。

    from sqlalchemy.orm.collections import collection

    class SetLike(object):
        __emulates__ = set

        def __init__(self):
            self.data = set()

        @collection.appender
        def append(self, item):
            self.data.add(item)

        def remove(self, item):
            self.data.remove(item)

        def __iter__(self):
            return iter(self.data)

这就是完成这个例子所需要的一切。SQLAlchemy 将通过`append`方法添加实例。`remove`和`__iter__`是集合的默认方法，将用于删除和迭代。缺省方法也可以更改：

    from sqlalchemy.orm.collections import collectionplain

    class MyList(list):
        @collection.remover
        def zark(self, item):
            # do something special...

        @collection.iterator
        def hey_use_this_instead_for_iteration(self):
            # ...

没有要求成为名单，或者根本不需要设置。集合类可以是任何形状，只要它们具有标记为 SQLAlchemy 使用的 append，remove 和 iterate 接口即可。将使用映射实体作为单个参数调用 Append 和 Remove 方法，并且不带任何参数调用迭代器方法，并且必须返回一个迭代器。

*class* `sqlalchemy.orm.collections。`{.descclassname} `集合`{.descname} [¶](#sqlalchemy.orm.collections.collection "Permalink to this definition")
:   实体集合类的装饰器。

    装饰者分为两组：注释和截取食谱。

    注释装饰器（appender，remover，iterator，linker，converter，inward\_instrumented）表示方法的用途并且不带任何参数。他们不是与parens写的：

        @collection.appender
        def append(self, append): ...

    配方装饰器都需要parens，即使那些没有参数的配置：

        @collection.adds('entity')
        def insert(self, position, entity): ...

        @collection.removes_return()
        def popitem(self): ...

    *静态 tt\> `增加`{.descname} （ *arg* ） [](#sqlalchemy.orm.collections.collection.adds "Permalink to this definition")*
    :   将该方法标记为将实体添加到集合中。

        向该方法添加“添加到集合”处理。decorator参数指示哪个方法参数保存与SQLAlchemy相关的值。参数可以在位置上指定（即整数）或按名称指定：

            @collection.adds(1)
            def push(self, item): ...

            @collection.adds('entity')
            def do_stuff(self, thing, entity=None): ...

    *静态 tt\> `appender`{.descname} （ *fn* ） [](#sqlalchemy.orm.collections.collection.appender "Permalink to this definition")*
    :   将该方法标记为收集appender。

        使用一个位置参数调用appender方法：要附加的值。如果尚未装饰，该方法将自动用'adds（1）'装饰：

            @collection.appender
            def add(self, append): ...

            # or, equivalently
            @collection.appender
            @collection.adds(1)
            def add(self, append): ...

            # for mapping type, an 'append' may kick out a previous value
            # that occupies that slot.  consider d['a'] = 'foo'- any previous
            # value in d['a'] is discarded.
            @collection.appender
            @collection.replaces(1)
            def add(self, entity):
                key = some_key_func(entity)
                previous = None
                if key in self:
                    previous = self[key]
                self[key] = entity
                return previous

        如果集合中不允许附加值，则可能引发异常。需要记住的是appender将被数据库查询映射的每个对象调用。如果数据库包含违反集合语义的行，则需要有创意才能解决该问题，因为通过集合进行访问将不起作用。

        如果appender方法在内部进行检测，则还必须接收关键字参数'\_sa\_initiator'并确保将其颁发给收集事件。

     *static*`converter`{.descname}(*fn*)[¶](#sqlalchemy.orm.collections.collection.converter "Permalink to this definition")
    :   将方法标记为收集转换器。

        当一个集合被完全替换时，这个可选方法将被调用，如下所示：

            myobj.acollection = [newvalue1, newvalue2]

        转换器方法将接收正在分配的对象，并且应该返回一个适用于`appender`方法的可迭代值。转换器不得分配值或改变集合，它唯一的工作就是将用户提供的值调整为ORM使用的可迭代值。

        默认的转换器实现将使用鸭子键入进行转换。类似dict的集合将被转换为字典值的迭代，而其他类型将被简单地迭代：

            @collection.converter
            def convert(self, other): ...

        如果对象的鸭式键入与此集合的类型不匹配，则会引发TypeError。

        如果要扩展可以批量分配的可能类型的范围或对要分配的值执行验证，请提供此方法的实现。

    *static* `within_instrumented`{.descname} （ *fn* ） [](#sqlalchemy.orm.collections.collection.internally_instrumented "Permalink to this definition")
    :   按照仪器标记方法。

        这个标签将防止任何装饰被应用于该方法。如果您正在使用基本的SQLAlchemy接口方法之一编排您自己对`collection_adapter()`的调用，或者阻止自动的ABC方法修饰封装您的实现，请使用此方法：

            # normally an 'extend' method on a list-like class would be
            # automatically intercepted and re-implemented in terms of
            # SQLAlchemy events and append().  your implementation will
            # never be called, unless:
            @collection.internally_instrumented
            def extend(self, items): ...

    *静态 tt\> `迭代器`{.descname} （ *fn* ） [¶](#sqlalchemy.orm.collections.collection.iterator "Permalink to this definition")*
    :   将方法标记为收集卸妆。

        迭代器方法被调用时没有参数。预计会返回所有集合成员的迭代器：

            @collection.iterator
            def __iter__(self): ...

    *静态 tt\> `链接`{.descname} （ *fn* ） [¶](#sqlalchemy.orm.collections.collection.link "Permalink to this definition")*
    :   弃用； [`collection.linker()`](#sqlalchemy.orm.collections.collection.linker "sqlalchemy.orm.collections.collection.linker")的同义词。

    *静态 tt\> `链接器`{.descname} （ *fn* ） [](#sqlalchemy.orm.collections.collection.linker "Permalink to this definition")*
    :   将该方法标记为“链接到属性”事件处理程序。

        当集合类与InstrumentedAttribute链接或断开链接时，将调用此可选事件处理程序。它在实例上设置'\_sa\_adapter'属性后立即调用。传递一个参数：链接的集合适配器；如果解除链接，则返回None。

        从版本1.0.0开始弃用： - [`collection.linker()`](#sqlalchemy.orm.collections.collection.linker "sqlalchemy.orm.collections.collection.linker")处理程序被[`AttributeEvents.init_collection()`](events.html#sqlalchemy.orm.events.AttributeEvents.init_collection "sqlalchemy.orm.events.AttributeEvents.init_collection")和[`AttributeEvents.dispose_collection()`](events.html#sqlalchemy.orm.events.AttributeEvents.dispose_collection "sqlalchemy.orm.events.AttributeEvents.dispose_collection")处理程序。

    *静态 T0\> `卸妆 T1> （ T2>  FN  T3> ） T4> ¶ T5>`{.descname}*
    :   将方法标记为收集卸妆。

        使用一个位置参数调用移除方法：要移除的值。如果尚未装饰，该方法将自动用[`removes_return()`](#sqlalchemy.orm.collections.collection.removes_return "sqlalchemy.orm.collections.collection.removes_return")进行修饰：

            @collection.remover
            def zap(self, entity): ...

            # or, equivalently
            @collection.remover
            @collection.removes_return()
            def zap(self, ): ...

        如果要删除的值在集合中不存在，则可以引发异常或返回无以忽略该错误。

        如果remove方法在内部进行检测，则还必须接收关键字参数'\_sa\_initiator'并确保将其颁发给收集事件。

    *static* `移除`{.descname} （ *arg* ） [¶](#sqlalchemy.orm.collections.collection.removes "Permalink to this definition")
    :   将该方法标记为删除集合中的实体。

        向方法添加“从集合中删除”处理。decorator参数指示哪个方法参数保存要删除的与SQLAlchemy相关的值。参数可以在位置上指定（即整数）或按名称指定：

            @collection.removes(1)
            def zap(self, item): ...

        对于在调用时未知移除值的方法，请使用collection.removes\_return。

    *static* `removed_return`{.descname} （ ） [¶](#sqlalchemy.orm.collections.collection.removes_return "Permalink to this definition")
    :   将该方法标记为删除集合中的实体。

        向方法添加“从集合中删除”处理。该方法的返回值（如果有的话）被视为要删除的值。方法参数未被检查：

            @collection.removes_return()
            def pop(self): ...

        对于在调用时已知移除值的方法，请使用collection.remove。

    *静态 tt\> `替换 tt> （ arg ） `{.descname}*
    :   将方法标记为替换集合中的实体。

        向该方法添加“添加到集合”和“从集合中删除”处理。decorator参数指示哪个方法参数保存要添加的SQLAlchemy相关值，以及返回值（如果有的话将被视为要删除的值）。

        参数可以在位置上指定（即整数）或按名称指定：

            @collection.replaces(2)
            def __setitem__(self, index, item): ...

### 自定义基于字典的集合[¶](#custom-dictionary-based-collections "Permalink to this headline")

[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")类可以用作自定义类型的基类，也可以作为混合来快速将`dict`集合支持添加到其他类中。它使用键控功能委托给`__setitem__`和`__delitem__`：

    from sqlalchemy.util import OrderedDictplain
    from sqlalchemy.orm.collections import MappedCollection

    class NodeMap(OrderedDict, MappedCollection):
        """Holds 'Node' objects, keyed by the 'name' attribute with insert order maintained."""

        def __init__(self, *args, **kw):
            MappedCollection.__init__(self, keyfunc=lambda node: node.name)
            OrderedDict.__init__(self, *args, **kw)

When subclassing [`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection"),
user-defined versions of `__setitem__()` or
`__delitem__()` should be decorated with
[`collection.internally_instrumented()`](#sqlalchemy.orm.collections.collection.internally_instrumented "sqlalchemy.orm.collections.collection.internally_instrumented"),
**if** they call down to those same methods on [`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection").
这是因为[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")上的方法已经被检测到
-
在一个已经检测到的调用中调用它们可能会导致重复触发事件或不恰当地触发事件，从而在极少数情况下导致内部状态损坏：

    from sqlalchemy.orm.collections import MappedCollection,\
                                        collection

    class MyMappedCollection(MappedCollection):
        """Use @internally_instrumented when your methods
        call down to already-instrumented methods.

        """

        @collection.internally_instrumented
        def __setitem__(self, key, value, _sa_initiator=None):
            # do something with key, value
            super(MyMappedCollection, self).__setitem__(key, value, _sa_initiator)

        @collection.internally_instrumented
        def __delitem__(self, key, _sa_initiator=None):
            # do something with key
            super(MyMappedCollection, self).__delitem__(key, _sa_initiator)

ORM 理解`dict`接口就像列表和集合一样，如果您选择继承`dict`或在类中提供字典集合行为，它将自动处理所有类字典方法鸭子类。但是，必须修饰 appender 和 remover 方法
-
默认情况下，SQLAlchemy 基本字典接口中没有兼容方法。迭代将经过`itervalues()`，除非另有修饰。

注意

由于版本 0.7.6 之前的 MappedCollection 中存在一个错误，通常需要在使用[`collection.internally_instrumented()`](#sqlalchemy.orm.collections.collection.internally_instrumented "sqlalchemy.orm.collections.collection.internally_instrumented")的自定义[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")子类之前调用​​此解决方法：

    from sqlalchemy.orm.collections import _instrument_class, MappedCollectionplain
    _instrument_class(MappedCollection)

这将确保[`MappedCollection`](#sqlalchemy.orm.collections.MappedCollection "sqlalchemy.orm.collections.MappedCollection")在自定义子类中使用之前，已使用自定义`__setitem__()`和`__delitem__()`方法正确初始化。

*class* `sqlalchemy.orm.collections。`{.descclassname} `MappedCollection`{.descname} （ *keyfunc* ）\< / T5\> [¶ T6\>](#sqlalchemy.orm.collections.MappedCollection "Permalink to this definition")
:   基础：`__builtin__.dict`

    基本的基于字典的集合类。plain

    使用集合类需要的最小包语义扩展字典。`set`和`remove`是通过键控函数实现的：任何可调用的方法都需要一个对象并返回一个用作字典键的对象。

    ` __初始化__  T0> （ T1>  keyfunc  T2> ） T3> ¶ T4>`{.descname}
    :   用keyfunc提供的键控创建一个新的集合。

        keyfunc可以是接受对象并返回一个对象用作字典键的任何可调用对象。

        每次ORM需要按值添加成员（例如从数据库加载实例时）或删除成员时，都会调用keyfunc。关于字典键控应用的通常警告
        - `keyfunc(object)`在集合的生命周期中应该返回相同的输出。基于可变属性的键控会导致集合中的“无法访问”实例“丢失”。

    `清除`{.descname} （ ）→无。删除D. [¶](#sqlalchemy.orm.collections.MappedCollection.clear "Permalink to this definition")中的所有项目
    :   

     `pop`{.descname}(*k*[, *d*]) → v, remove specified key and return the corresponding value.[¶](#sqlalchemy.orm.collections.MappedCollection.pop "Permalink to this definition")
    :   如果未找到密钥，则在返回时返回d，否则引发KeyError

    `popitem`{.descname} （ ）→（k，v），移除并返回一些（key，value）对作为[¶ t3 \>](#sqlalchemy.orm.collections.MappedCollection.popitem "Permalink to this definition")
    :   2元组；但如果D为空则引发KeyError。

    `除去 T0> （ T1> 值 T2>， _sa_initiator =无 T3> ） T4> ¶ T5 >`{.descname}
    :   按值删除一个项目，查询该项的keyfunc。

    `set`{.descname} （ *value*，*\_sa\_initiator = None* ） [t5 \>](#sqlalchemy.orm.collections.MappedCollection.set "Permalink to this definition")
    :   按值添加项目，查询密钥的keyfunc。

     `setdefault`{.descname}(*k*[, *d*]) → D.get(k,d), also set D[k]=d if k not in D[¶](#sqlalchemy.orm.collections.MappedCollection.setdefault "Permalink to this definition")
    :   

     `update`{.descname}([*E*, ]*\*\*F*) → None. 从dict / iterable E和F更新D。[¶](#sqlalchemy.orm.collections.MappedCollection.update "Permalink to this definition")
    :   如果E存在且具有.keys()方法，则：对于E中的k：D [k] = E
        [k]如果E存在并且缺少.keys()方法，则：for（k，v）in E： D [k] =
        v在任一情况下，这后面是：对于F中的k：D [k] = F [k]

### 仪表和自定义类型[¶](#instrumentation-and-custom-types "Permalink to this headline")

许多自定义类型和现有库类可以作为实体集合类型使用。但是，需要注意的是，检测过程会修改类型，并自动在方法中添加装饰器。

这些装饰在关系之外是轻量级且无操作的，但是在其他地方触发时它们确实增加了不必要的开销。当使用库类作为集合时，最好使用“平凡的子类”技巧来限制装饰，使其仅用于关系中的使用。例如：

    class MyAwesomeList(some.great.library.AwesomeList):plain
        pass

    # ... relationship(..., collection_class=MyAwesomeList)

ORM 将这种方法用于内置插件，当`list`，`set`或`dict`被直接使用时，静静地替换一个普通的子类。

集合内部[¶](#collection-internals "Permalink to this headline")
---------------------------------------------------------------

各种内部方法。

 `sqlalchemy.orm.collections.`{.descclassname}`bulk_replace`{.descname}(*values*, *existing\_adapter*, *new\_adapter*)[¶](#sqlalchemy.orm.collections.bulk_replace "Permalink to this definition")
:   加载一个新的集合，根据之前的类似成员资格触发事件。

    将`values`中的实例附加到`new_adapter`上。对于`existing_adapter`中不存在的任何实例，都会触发事件。`values`中不存在的`existing_adapter`中的任何实例都将移除在它们上面触发的事件。

    参数：

    -   **values**[¶](#sqlalchemy.orm.collections.bulk_replace.params.values)
        – An iterable of collection member instances
    -   **existing\_adapter**[¶](#sqlalchemy.orm.collections.bulk_replace.params.existing_adapter)
        – A [`CollectionAdapter`](#sqlalchemy.orm.collections.CollectionAdapter "sqlalchemy.orm.collections.CollectionAdapter")
        of instances to be replaced
    -   **new\_adapter**[¶](#sqlalchemy.orm.collections.bulk_replace.params.new_adapter)
        – An empty [`CollectionAdapter`](#sqlalchemy.orm.collections.CollectionAdapter "sqlalchemy.orm.collections.CollectionAdapter")
        to load with `values`

*class* `sqlalchemy.orm.collections。`{.descclassname} `集合`{.descname}
:   实体集合类的装饰器。

    装饰者分为两组：注释和截取食谱。plain

    注释装饰器（appender，remover，iterator，linker，converter，inward\_instrumented）表示方法的用途并且不带任何参数。他们不是与parens写的：

        @collection.appender
        def append(self, append): ...

    配方装饰器都需要parens，即使那些没有参数的配置：

        @collection.adds('entity')
        def insert(self, position, entity): ...

        @collection.removes_return()
        def popitem(self): ...

`sqlalchemy.orm.collections。`{.descclassname} `collection_adapter`{.descname} *=＆lt； operator.attrgetter object＆gt；* [¶](#sqlalchemy.orm.collections.collection_adapter "Permalink to this definition")
:   获取集合的[`CollectionAdapter`](#sqlalchemy.orm.collections.CollectionAdapter "sqlalchemy.orm.collections.CollectionAdapter")。

 *class*`sqlalchemy.orm.collections.`{.descclassname}`CollectionAdapter`{.descname}(*attr*, *owner\_state*, *data*)[¶](#sqlalchemy.orm.collections.CollectionAdapter "Permalink to this definition")
:   ORM 和任意 Python 集合之间的桥梁。

    代理基本级集合操作（​​追加，删除，迭代）到基础Python集合，并为进入或离开集合的实体发出添加/删除事件。

    ORM仅使用[`CollectionAdapter`](#sqlalchemy.orm.collections.CollectionAdapter "sqlalchemy.orm.collections.CollectionAdapter")来与实体集合进行交互。

*class* `sqlalchemy.orm.collections。`{.descclassname} `InstrumentedDict`{.descname} [¶](#sqlalchemy.orm.collections.InstrumentedDict "Permalink to this definition")
:   基础：`__builtin__.dict`

    内置字典的工具版本。plain

*class* `sqlalchemy.orm.collections。`{.descclassname} `InstrumentedList`{.descname} [¶](#sqlalchemy.orm.collections.InstrumentedList "Permalink to this definition")
:   基础：`__builtin__.list`

    内置列表的检测版本。plain

*class* `sqlalchemy.orm.collections。`{.descclassname} `InstrumentedSet`{.descname} [¶](#sqlalchemy.orm.collections.InstrumentedSet "Permalink to this definition")
:   基础：`__builtin__.set`

    内置集合的插装版本。plain

`sqlalchemy.orm.collections。 T0>  prepare_instrumentation  T1> （ T2> 工厂 T3> ） T4> ¶< / T5>`{.descclassname}
:   为将来使用作为集合类工厂准备一个可调用的函数。

    给定一个集合类工厂（无论类型还是无参数），返回另一个工厂，在调用时将生成兼容的实例。plain

    该函数负责将collection\_class = list转换为collection\_class =
    InstrumentedList的运行时行为。


