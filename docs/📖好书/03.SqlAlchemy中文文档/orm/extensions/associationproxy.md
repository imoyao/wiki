---
title: associationproxy
date: 2021-02-20 22:41:41
permalink: /pages/4ec584/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
  - extensions
tags:
  - 
---
关联代理[¶](#module-sqlalchemy.ext.associationproxy "Permalink to this headline")
=================================================================================

`associationproxy` is used to create a read/write
view of a target attribute across a relationship.
它本质上隐藏了两个端点之间的“中间”属性的用法，可用于从相关对象集合中挑选字段或减少使用关联对象模式的详细程度。创造性地应用，关联代理允许构建几乎任何几何图形的复杂集合和字典视图，并使用标准的，透明配置的关系模式持久化到数据库。

简化标量集合[¶](#simplifying-scalar-collections "Permalink to this headline")
-----------------------------------------------------------------------------

考虑两个类（`User`和`Keyword`）之间的多对多映射。每个`User`可以包含任意数量的`Keyword`对象，反之亦然（多对多模式在[Many To
Many](basic_relationships.html#relationships-many-to-many)中描述） ：

    from sqlalchemy import Column, Integer, String, ForeignKey, Table
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(64))
        kw = relationship("Keyword", secondary=lambda: userkeywords_table)

        def __init__(self, name):
            self.name = name

    class Keyword(Base):
        __tablename__ = 'keyword'
        id = Column(Integer, primary_key=True)
        keyword = Column('keyword', String(64))

        def __init__(self, keyword):
            self.keyword = keyword

    userkeywords_table = Table('userkeywords', Base.metadata,
        Column('user_id', Integer, ForeignKey("user.id"),
               primary_key=True),
        Column('keyword_id', Integer, ForeignKey("keyword.id"),
               primary_key=True)
    )

读取和操作与`User`关联的“关键字”字符串的集合需要从每个集合元素遍历`.keyword`属性，这可能会很棘手：

    >>> user = User('jek')
    >>> user.kw.append(Keyword('cheese inspector'))
    >>> print(user.kw)
    [<__main__.Keyword object at 0x12bf830>]
    >>> print(user.kw[0].keyword)
    cheese inspector
    >>> print([keyword.keyword for keyword in user.kw])
    ['cheese inspector']

对`User`类应用`association_proxy`以产生`kw`关系的“视图”，该关系仅显示字符串值`.keyword`与每个`Keyword`对象关联：

    from sqlalchemy.ext.associationproxy import association_proxy

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(64))
        kw = relationship("Keyword", secondary=lambda: userkeywords_table)

        def __init__(self, name):
            self.name = name

        # proxy the 'keyword' attribute from the 'kw' relationship
        keywords = association_proxy('kw', 'keyword')

我们现在可以将`.keywords`集合引用为可读写的字符串列表。新的`Keyword`对象是透明地为我们创建的：

    >>> user = User('jek')
    >>> user.keywords.append('cheese inspector')
    >>> user.keywords
    ['cheese inspector']
    >>> user.keywords.append('snack ninja')
    >>> user.kw
    [<__main__.Keyword object at 0x12cdd30>, <__main__.Keyword object at 0x12cde30>]

由[`association_proxy()`](#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")函数产生的[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")对象是[Python描述符](http://docs.python.org/howto/descriptor.html)的实例。无论使用通过[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数的声明映射还是经典映射，都始终声明用户定义类正在映射。

代理通过对底层映射属性或集合进行操作来响应操作，并且通过代理进行的更改在映射属性中立即显现，反之亦然。底层属性保持完全可访问。

首次访问时，关联代理会对目标集合执行自检操作，以使其行为正确对应。例如，如果本地代理属性是集合（通常是）或标量引用，以及集合是否像集合，列表或字典一样起作用，则会考虑这些细节，以便代理应该像基础收集或属性确实。

创造新价值[¶](#creation-of-new-values "Permalink to this headline")
-------------------------------------------------------------------

当列表append()事件（或set add()，dictionary \_\_setitem
\_\_()或标量赋值事件）被关联代理拦截时，它使用其构造函数实例化“中间”对象的新实例，作为单个论证给定的价值。在我们上面的例子中，一个操作如下：

    user.keywords.append('cheese inspector')

由协会代理翻译成操作：

    user.kw.append(Keyword('cheese inspector'))

这个例子在这里工作，因为我们设计了`Keyword`的构造函数来接受一个位置参数`keyword`。对于单参数构造函数不可行的情况，可以使用`creator`参数来定制关联代理的创建行为，该参数引用可调用的函数（即Python函数），该函数将产生一个新的对象实例给出单数论证。下面我们用典型的lambda来说明这一点：

    class User(Base):
        # ...

        # use Keyword(keyword=kw) on append() events
        keywords = association_proxy('kw', 'keyword',
                        creator=lambda kw: Keyword(keyword=kw))

`creator`函数在基于列表或集合的集合或标量属性的情况下接受单个参数。在基于字典的集合中，它接受两个参数“key”和“value”。下面的例子是[Proxying
to Dictionary Based Collections](#proxying-dictionaries)。

简化关联对象[¶](#simplifying-association-objects "Permalink to this headline")
------------------------------------------------------------------------------

“关联对象”模式是多对多关系的扩展形式，并在[Association
Object](basic_relationships.html#association-pattern)中进行了描述。关联代理对于在常规使用中保留“关联对象”非常有用。

假设我们上面的`userkeywords`表有额外的列，我们希望明确映射，但是在大多数情况下我们不需要直接访问这些属性。下面我们举例说明一个新的映射，它引入了映射到前面说明的`userkeywords`表的`UserKeyword`类。这个类增加了一个额外的列`special_key`，这是我们偶尔想要访问的值，但通常情况下不会。我们在`User`类中创建了一个名为`keywords`的关联代理，它将与`User`的`user_keywords`
\>到每个`UserKeyword`中存在的`.keyword`属性：

    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship, backref

    from sqlalchemy.ext.associationproxy import association_proxy
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(64))

        # association proxy of "user_keywords" collection
        # to "keyword" attribute
        keywords = association_proxy('user_keywords', 'keyword')

        def __init__(self, name):
            self.name = name

    class UserKeyword(Base):
        __tablename__ = 'user_keyword'
        user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
        keyword_id = Column(Integer, ForeignKey('keyword.id'), primary_key=True)
        special_key = Column(String(50))

        # bidirectional attribute/collection of "user"/"user_keywords"
        user = relationship(User,
                    backref=backref("user_keywords",
                                    cascade="all, delete-orphan")
                )

        # reference to the "Keyword" object
        keyword = relationship("Keyword")

        def __init__(self, keyword=None, user=None, special_key=None):
            self.user = user
            self.keyword = keyword
            self.special_key = special_key

    class Keyword(Base):
        __tablename__ = 'keyword'
        id = Column(Integer, primary_key=True)
        keyword = Column('keyword', String(64))

        def __init__(self, keyword):
            self.keyword = keyword

        def __repr__(self):
            return 'Keyword(%s)' % repr(self.keyword)

通过上述配置，我们可以对每个`User`对象的`.keywords`集合进行操作，并且隐藏`UserKeyword`的用法：

    >>> user = User('log')
    >>> for kw in (Keyword('new_from_blammo'), Keyword('its_big')):
    ...     user.keywords.append(kw)
    ...
    >>> print(user.keywords)
    [Keyword('new_from_blammo'), Keyword('its_big')]

在上面，每个`.keywords.append()`操作相当于：

    >>> user.user_keywords.append(UserKeyword(Keyword('its_heavy')))

这个`UserKeyword`关联对象在这里有两个属性被填充；作为第一个参数传递`Keyword`对象的结果，直接填充`.keyword`属性。当`UserKeyword`对象附加到`User.user_keywords`集合时，`.user`参数被分配，其中`User.user_keywords`和`UserKeyword.user`会导致`UserKeyword.user`属性的填充。上面的`special_key`参数保留默认值`None`。

对于那些我们希望`special_key`具有值的情况，我们显式创建`UserKeyword`对象。下面我们分配所有三个属性，其中`.user`的赋值将`UserKeyword`的作用附加到`User.user_keywords`集合中：

    >>> UserKeyword(Keyword('its_wood'), user, special_key='my special key')

关联代理向我们返回由所有这些操作表示的`Keyword`对象的集合：

    >>> user.keywords
    [Keyword('new_from_blammo'), Keyword('its_big'), Keyword('its_heavy'), Keyword('its_wood')]

代理基于字典的集合[¶](#proxying-to-dictionary-based-collections "Permalink to this headline")
---------------------------------------------------------------------------------------------

关联代理也可以代理基于字典的集合。SQLAlchemy映射通常使用[`attribute_mapped_collection()`](collections.html#sqlalchemy.orm.collections.attribute_mapped_collection "sqlalchemy.orm.collections.attribute_mapped_collection")集合类型来创建字典集合，以及[Custom
Dictionary-Based Collections](collections.html#id1)中描述的扩展技术。

关联代理在检测到基于字典的集合的使用时调整其行为。将新值添加到字典时，关联代理通过将两个参数传递给创建函数而不是一个参数（键和值）来实例化中间对象。与往常一样，此创建函数默认为中介类的构造函数，并可使用`creator`参数进行自定义。

下面，我们修改我们的`UserKeyword`示例，使得`User.user_keywords`集合现在将使用字典进行映射，其中`UserKeyword.special_key`参数将会被用作字典的关键字。然后，我们将`creator`参数应用于`User.keywords`代理，以便在将新元素添加到字典时适当地分配这些值：

    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.ext.associationproxy import association_proxy
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm.collections import attribute_mapped_collection

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(64))

        # proxy to 'user_keywords', instantiating UserKeyword
        # assigning the new key to 'special_key', values to
        # 'keyword'.
        keywords = association_proxy('user_keywords', 'keyword',
                        creator=lambda k, v:
                                    UserKeyword(special_key=k, keyword=v)
                    )

        def __init__(self, name):
            self.name = name

    class UserKeyword(Base):
        __tablename__ = 'user_keyword'
        user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
        keyword_id = Column(Integer, ForeignKey('keyword.id'), primary_key=True)
        special_key = Column(String)

        # bidirectional user/user_keywords relationships, mapping
        # user_keywords with a dictionary against "special_key" as key.
        user = relationship(User, backref=backref(
                        "user_keywords",
                        collection_class=attribute_mapped_collection("special_key"),
                        cascade="all, delete-orphan"
                        )
                    )
        keyword = relationship("Keyword")

    class Keyword(Base):
        __tablename__ = 'keyword'
        id = Column(Integer, primary_key=True)
        keyword = Column('keyword', String(64))

        def __init__(self, keyword):
            self.keyword = keyword

        def __repr__(self):
            return 'Keyword(%s)' % repr(self.keyword)

我们将`.keywords`集合说明为字典，将`UserKeyword.string_key`值映射到`Keyword`对象：

    >>> user = User('log')

    >>> user.keywords['sk1'] = Keyword('kw1')
    >>> user.keywords['sk2'] = Keyword('kw2')

    >>> print(user.keywords)
    {'sk1': Keyword('kw1'), 'sk2': Keyword('kw2')}

复合关联代理[¶](#composite-association-proxies "Permalink to this headline")
----------------------------------------------------------------------------

考虑到我们之前从关系到标量属性，代理跨越关联对象以及代理字典的代理示例，我们可以将所有三种技术组合在一起以给出`User` a `keywords`字典严格处理映射到字符串`keyword`的`special_key`的字符串值。`UserKeyword`和`Keyword`类都完全隐藏。这是通过在`User`上建立一个关联代理实现的，该代理引用`UserKeyword`上存在的关联代理：

    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship, backref

    from sqlalchemy.ext.associationproxy import association_proxy
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm.collections import attribute_mapped_collection

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(64))

        # the same 'user_keywords'->'keyword' proxy as in
        # the basic dictionary example
        keywords = association_proxy(
                    'user_keywords',
                    'keyword',
                    creator=lambda k, v:
                                UserKeyword(special_key=k, keyword=v)
                    )

        def __init__(self, name):
            self.name = name

    class UserKeyword(Base):
        __tablename__ = 'user_keyword'
        user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
        keyword_id = Column(Integer, ForeignKey('keyword.id'),
                                                        primary_key=True)
        special_key = Column(String)
        user = relationship(User, backref=backref(
                "user_keywords",
                collection_class=attribute_mapped_collection("special_key"),
                cascade="all, delete-orphan"
                )
            )

        # the relationship to Keyword is now called
        # 'kw'
        kw = relationship("Keyword")

        # 'keyword' is changed to be a proxy to the
        # 'keyword' attribute of 'Keyword'
        keyword = association_proxy('kw', 'keyword')

    class Keyword(Base):
        __tablename__ = 'keyword'
        id = Column(Integer, primary_key=True)
        keyword = Column('keyword', String(64))

        def __init__(self, keyword):
            self.keyword = keyword

`User.keywords` is now a dictionary of string to
string, where `UserKeyword` and `Keyword` objects are created and removed for us transparently using the
association proxy.
在下面的例子中，我们举例说明了赋值运算符的用法，也可以由关联代理进行适当处理，以便将字典值同时应用于集合：

    >>> user = User('log')
    >>> user.keywords = {
    ...     'sk1':'kw1',
    ...     'sk2':'kw2'
    ... }
    >>> print(user.keywords)
    {'sk1': 'kw1', 'sk2': 'kw2'}

    >>> user.keywords['sk3'] = 'kw3'
    >>> del user.keywords['sk2']
    >>> print(user.keywords)
    {'sk1': 'kw1', 'sk3': 'kw3'}

    >>> # illustrate un-proxied usage
    ... print(user.user_keywords['sk3'].kw)
    <__main__.Keyword object at 0x12ceb90>

上面我们的示例的一个警告是，因为为每个字典集操作创建了`Keyword`对象，所以该示例未能保持其字符串名称上`Keyword`对象的唯一性，即这是一种标签场景的典型要求。对于这种用例，建议使用配方[UniqueObject](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/UniqueObject)或类似的创建策略，这将对`Keyword`类的构造函数应用“首先查找，然后创建”策略，因此如果给定的名称已经存在，则返回已经存在的`Keyword`。

查询关联代理[¶](#querying-with-association-proxies "Permalink to this headline")
--------------------------------------------------------------------------------

[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")具有简单的SQL构造功能，这些功能与使用中的基础[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")）以及目标属性相关。例如，[`RelationshipProperty.Comparator.any()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")和[`RelationshipProperty.Comparator.has()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")操作是可用的，并且会产生一个“嵌套的”EXISTS子句，如in我们的基本关联对象示例：

    >>> print(session.query(User).filter(User.keywords.any(keyword='jek')))
    SELECT user.id AS user_id, user.name AS user_name
    FROM user
    WHERE EXISTS (SELECT 1
    FROM user_keyword
    WHERE user.id = user_keyword.user_id AND (EXISTS (SELECT 1
    FROM keyword
    WHERE keyword.id = user_keyword.keyword_id AND keyword.keyword = :keyword_1)))

对于标量属性的代理，支持`__eq__()`：

    >>> print(session.query(UserKeyword).filter(UserKeyword.keyword == 'jek'))
    SELECT user_keyword.*
    FROM user_keyword
    WHERE EXISTS (SELECT 1
        FROM keyword
        WHERE keyword.id = user_keyword.keyword_id AND keyword.keyword = :keyword_1)

和`.contains()`可用于标量集合的代理：

    >>> print(session.query(User).filter(User.keywords.contains('jek')))
    SELECT user.*
    FROM user
    WHERE EXISTS (SELECT 1
    FROM userkeywords, keyword
    WHERE user.id = userkeywords.user_id
        AND keyword.id = userkeywords.keyword_id
        AND keyword.keyword = :keyword_1)

[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")
can be used with [`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
somewhat manually using the [`attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.attr "sqlalchemy.ext.associationproxy.AssociationProxy.attr")
attribute in a star-args context:

    q = session.query(User).join(*User.keywords.attr)

版本0.7.3中的新增内容： [`attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.attr "sqlalchemy.ext.associationproxy.AssociationProxy.attr")属性在star-args上下文中。

[`attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.attr "sqlalchemy.ext.associationproxy.AssociationProxy.attr")由[`AssociationProxy.local_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.local_attr "sqlalchemy.ext.associationproxy.AssociationProxy.local_attr")和[`AssociationProxy.remote_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr "sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr")组成，它们只是实际代理属性的同义词，也可用于查询：

    uka = aliased(UserKeyword)
    ka = aliased(Keyword)
    q = session.query(User).\
            join(uka, User.keywords.local_attr).\
            join(ka, User.keywords.remote_attr)

New in version 0.7.3: [`AssociationProxy.local_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.local_attr "sqlalchemy.ext.associationproxy.AssociationProxy.local_attr")
and [`AssociationProxy.remote_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr "sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr"),
synonyms for the actual proxied attributes, and usable for querying.

API文档[¶](#api-documentation "Permalink to this headline")
-----------------------------------------------------------

 `sqlalchemy.ext.associationproxy.`{.descclassname}`association_proxy`{.descname}(*target\_collection*, *attr*, *\*\*kw*)[¶](#sqlalchemy.ext.associationproxy.association_proxy "Permalink to this definition")
:   返回实现目标属性视图的Python属性，该属性引用目标成员上的属性。

    返回的值是[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")的一个实例。

    将一个表示关系的Python属性实现为一组简单值或一个标量值。被代理的属性将模仿目标（列表，字典或集合）的集合类型，或者在一对一关系的情况下，它是一个简单的标量值。

    参数：

    -   **target\_collection**
        [¶](#sqlalchemy.ext.associationproxy.association_proxy.params.target_collection)
        - 我们将代理的属性的名称。该属性通常由[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")映​​射以链接到目标集合，但也可以是多对一或非标量关系。
    -   **attr**
        [¶](#sqlalchemy.ext.associationproxy.association_proxy.params.attr)
        -

        我们将代理的关联实例或实例的属性。

        例如，给定[obj1，obj2]的目标集合，由此代理属性创建的列表看起来像[getattr（obj1，*attr*），getattr（obj2，*attr
        t1 \>）]*

        如果关系是一对一关系，或者使用list =
        False，那么简单地说：getattr（obj，*attr*）

    -   **创作者**
        [¶](#sqlalchemy.ext.associationproxy.association_proxy.params.creator)
        -

        可选的。

        将新项目添加到此代理集合时，将创建由目标集合收集的类的新实例。对于列表和集合集合，将使用新值的“值”来调用目标类构造函数。对于字典类型，传递了两个参数：键和值。

        如果您想以不同方式构造实例，请提供一个*creator*函数，该函数接受上面的参数并返回实例。

        对于标量关系，如果目标是None，creator()将被调用。如果目标存在，set操作被代理到关联对象上的setattr()。

        如果您的关联对象具有多个属性，则可以设置多个关联代理映射到不同的属性。请参阅单元测试的示例，以及有关如何使用creator()函数在此情况下构建按需标量关系的示例。

    -   **\*\*kw**[¶](#sqlalchemy.ext.associationproxy.association_proxy.params.**kw)
        – Passes along any other keyword arguments to
        [`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy").

 *class*`sqlalchemy.ext.associationproxy.`{.descclassname}`AssociationProxy`{.descname}(*target\_collection*, *attr*, *creator=None*, *getset\_factory=None*, *proxy\_factory=None*, *proxy\_bulk\_set=None*, *info=None*)[¶](#sqlalchemy.ext.associationproxy.AssociationProxy "Permalink to this definition")
:   基础：[`sqlalchemy.orm.base.InspectionAttrInfo`](internals.html#sqlalchemy.orm.base.InspectionAttrInfo "sqlalchemy.orm.base.InspectionAttrInfo")

    呈现对象属性的读/写视图的描述符。

     `__init__`{.descname}(*target\_collection*, *attr*, *creator=None*, *getset\_factory=None*, *proxy\_factory=None*, *proxy\_bulk\_set=None*, *info=None*)[¶](#sqlalchemy.ext.associationproxy.AssociationProxy.__init__ "Permalink to this definition")
    :   构建一个新的[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")。

        [`association_proxy()`](#sqlalchemy.ext.associationproxy.association_proxy "sqlalchemy.ext.associationproxy.association_proxy")函数在这里作为通常的入口点提供，尽管[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")可以直接实例化和/或子类化。

        参数：

        -   **target\_collection**[¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.target_collection)
            – Name of the collection we’ll proxy to, usually created
            with [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship").
        -   **attr**[¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.attr)
            – Attribute on the collected instances we’ll proxy for.
            例如，给定[obj1，obj2]的目标集合，由此代理属性创建的列表将看起来像[getattr（obj1，attr），getattr（obj2，attr）]
        -   **创作者**
            [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.creator)
            -

            可选的。将新项目添加到此代理集合时，将创建由目标集合收集的类的新实例。对于列表和集合集合，将使用新值的“值”来调用目标类构造函数。对于字典类型，传递了两个参数：键和值。

            如果您想以不同方式构造实例，请提供一个“创建者”函数，该函数接受上述参数并返回实例。

        -   **getset\_factory**
            [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.getset_factory)
            -

            可选的。Proxied属性访问由例程自动处理，例程根据此代理的attr参数获取和设置值。

            如果你想自定义这种行为，你可以提供一个getset\_factory可调用，它产生一个getter和setter函数的元组。工厂被调用两个参数，底层集合的抽象类型和此代理实例。

        -   **proxy\_factory**
            [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.proxy_factory)
            -
            可选。要仿真的集合类型是通过嗅探目标集合来确定的。如果您的集合类型不能通过鸭子输入来确定，或者您想使用不同的集合实现，则可以提供工厂函数来生成这些集合。只适用于非标量关系。
        -   **proxy\_bulk\_set**
            [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.proxy_bulk_set)
            -
            可选，与proxy\_factory一起使用。有关详细信息，请参阅\_set()方法。
        -   **info**
            [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.params.info)
            -

            可选的，将被分配给[`AssociationProxy.info`](#sqlalchemy.ext.associationproxy.AssociationProxy.info "sqlalchemy.ext.associationproxy.AssociationProxy.info")（如果存在）。

            版本1.0.9中的新功能

    `任何`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.ext.associationproxy.AssociationProxy.any "Permalink to this definition")
    :   使用EXISTS生成代理的“any”表达式。

        该表达式将是一个使用基础代理属性的[`RelationshipProperty.Comparator.any()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")和/或[`RelationshipProperty.Comparator.has()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")运算符的组合产品。

    ` ATTR  T0> ¶ T1>`{.descname}
    :   返回`（local_attr， remote_attr）`的元组。

        在跨两个关系使用[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")指定连接时，该属性很方便：

            sess.query(Parent).join(*Parent.proxied.attr)

        New in version 0.7.3.

        也可以看看：

        [`AssociationProxy.local_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.local_attr "sqlalchemy.ext.associationproxy.AssociationProxy.local_attr")

        [`AssociationProxy.remote_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr "sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr")

    `包含 T0> （ T1>  OBJ  T2> ） T3> ¶ T4>`{.descname}
    :   使用EXISTS生成代理的“包含”表达式。

        这个表达式将是一个使用[`RelationshipProperty.Comparator.any()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")，[`RelationshipProperty.Comparator.has()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")和/或[`RelationshipProperty.Comparator.contains()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")运算符的底层代理属性。

    `extension_type`{.descname} *=符号（'ASSOCIATION\_PROXY'）* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.extension_type "Permalink to this definition")
    :   

    `有`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.ext.associationproxy.AssociationProxy.has "Permalink to this definition")
    :   使用EXISTS生成代理“有”表达式。

        该表达式将是一个使用基础代理属性的[`RelationshipProperty.Comparator.any()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")和/或[`RelationshipProperty.Comparator.has()`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")运算符的组合产品。

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](internals.html#sqlalchemy.orm.base.InspectionAttrInfo.info "sqlalchemy.orm.base.InspectionAttrInfo.info")
        *attribute of* [`InspectionAttrInfo`](internals.html#sqlalchemy.orm.base.InspectionAttrInfo "sqlalchemy.orm.base.InspectionAttrInfo")

        信息字典与对象关联，允许用户定义的数据与这个[`InspectionAttr`](internals.html#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")关联。

        字典在第一次访问时生成。Alternatively, it can be specified as a
        constructor argument to the [`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property"),
        [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
        or [`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
        functions.

        0.8版新增功能：增加了对所有[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")子类的.info支持。

        版本1.0.0更改： [`MapperProperty.info`](internals.html#MapperProperty.info "MapperProperty.info")也可以通过[`InspectionAttrInfo.info`](internals.html#sqlalchemy.orm.base.InspectionAttrInfo.info "sqlalchemy.orm.base.InspectionAttrInfo.info")属性在扩展类型上使用，以便它可以应用于更广泛的ORM和扩展结构。

        也可以看看

        [`QueryableAttribute.info`](internals.html#sqlalchemy.orm.attributes.QueryableAttribute.info "sqlalchemy.orm.attributes.QueryableAttribute.info")

        [`SchemaItem.info`](core_metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")

    `is_aliased_class`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_aliased_class "Permalink to this definition")
    :   

    `is_attribute`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_attribute "Permalink to this definition")
    :   

    `is_clause_element`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_clause_element "Permalink to this definition")
    :   

    `is_instance`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_instance "Permalink to this definition")
    :   

    `is_mapper`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_mapper "Permalink to this definition")
    :   

    `is_property`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_property "Permalink to this definition")
    :   

    `is_selectable`{.descname} *= False* [¶](#sqlalchemy.ext.associationproxy.AssociationProxy.is_selectable "Permalink to this definition")
    :   

    ` local_attr  T0> ¶ T1>`{.descname}
    :   由[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")引用的'local'[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")。

        New in version 0.7.3.

        也可以看看：

        [`AssociationProxy.attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.attr "sqlalchemy.ext.associationproxy.AssociationProxy.attr")

        [`AssociationProxy.remote_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr "sqlalchemy.ext.associationproxy.AssociationProxy.remote_attr")

    ` remote_attr  T0> ¶ T1>`{.descname}
    :   这个[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")引用的'remote'[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")。

        New in version 0.7.3.

        也可以看看：

        [`AssociationProxy.attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.attr "sqlalchemy.ext.associationproxy.AssociationProxy.attr")

        [`AssociationProxy.local_attr`](#sqlalchemy.ext.associationproxy.AssociationProxy.local_attr "sqlalchemy.ext.associationproxy.AssociationProxy.local_attr")

    `标量 T0> ¶ T1>`{.descname}
    :   如果[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")代表本地方的标量关系，则返回`True`。

    ` target_class  T0> ¶ T1>`{.descname}
    :   由[`AssociationProxy`](#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")处理的中介类。

        截获的append / set / assignment事件将导致产生这个类的新实例。

`sqlalchemy.ext.associationproxy。`{.descclassname} `ASSOCIATION_PROXY`{.descname} *=符号（'ASSOCIATION\_PROXY'）* [¶](#sqlalchemy.ext.associationproxy.ASSOCIATION_PROXY "Permalink to this definition")
:   

