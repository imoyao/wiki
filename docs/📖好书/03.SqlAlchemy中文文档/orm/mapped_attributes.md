---
title: mapped_attributes
date: 2021-02-20 22:41:43
permalink: /pages/99b767/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
更改属性行为[¶](#changing-attribute-behavior "Permalink to this headline")
==========================================================================

简单验证器[¶](#simple-validators "Permalink to this headline")
--------------------------------------------------------------

向属性添加“验证”例程的一种快速方法是使用[`validates()`](#sqlalchemy.orm.validates "sqlalchemy.orm.validates")装饰器。属性验证器可以引发异常，停止变更属性值的过程，或者可以将给定值更改为不同的值。与所有属性扩展一样，验证器只能由普通的用户级代码调用；当ORM填充对象时它们不会被发出：

    from sqlalchemy.orm import validates

    class EmailAddress(Base):
        __tablename__ = 'address'

        id = Column(Integer, primary_key=True)
        email = Column(String)

        @validates('email')
        def validate_email(self, key, address):
            assert '@' in address
            return address

版本1.0.0中已更改： -
当刷新主键列的新提取值以及一些python或服务器端默认值时，验证器不再在刷新过程中触发。在1.0之前，验证器也可能在这些情况下被触发。

当项目添加到集合时，验证程序还会收到追加追加事件：

    from sqlalchemy.orm import validates

    class User(Base):
        # ...

        addresses = relationship("Address")

        @validates('addresses')
        def validate_address(self, key, address):
            assert '@' in address.email
            return address

缺省情况下，验证功能不会针对集合删除事件发出，因为典型的期望是被丢弃的值不需要验证。However,
[`validates()`](#sqlalchemy.orm.validates "sqlalchemy.orm.validates")
supports reception of these events by specifying
`include_removes=True` to the decorator.
当设置此标志时，验证函数必须接收一个额外的布尔参数，如果`True`表明该操作是删除：

    from sqlalchemy.orm import validates

    class User(Base):
        # ...

        addresses = relationship("Address")

        @validates('addresses', include_removes=True)
        def validate_address(self, key, address, is_remove):
            if is_remove:
                raise ValueError(
                        "not allowed to remove items from the collection")
            else:
                assert '@' in address.email
                return address

使用`include_backrefs=False`选项也可以定制相互依赖的验证器通过backref链接的情况；当设置为`False`时，此选项可防止发生验证功能，如果事件是由于backref引起的：

    from sqlalchemy.orm import validates

    class User(Base):
        # ...

        addresses = relationship("Address", backref='user')

        @validates('addresses', include_backrefs=False)
        def validate_address(self, key, address):
            assert '@' in address.email
            return address

Above, if we were to assign to `Address.user` as in
`some_address.user = some_user`, the
`validate_address()` function would *not* be
emitted, even though an append occurs to `some_user.addresses` - the event is caused by a backref.

请注意，[`validates()`](#sqlalchemy.orm.validates "sqlalchemy.orm.validates")装饰器是建立在属性事件之上的便利函数。需要更多控制属性更改行为配置的应用程序可以使用此系统，如[`AttributeEvents`](events.html#sqlalchemy.orm.events.AttributeEvents "sqlalchemy.orm.events.AttributeEvents")所述。

 `sqlalchemy.orm.`{.descclassname}`validates`{.descname}(*\*names*, *\*\*kw*)[¶](#sqlalchemy.orm.validates "Permalink to this definition")
:   装饰一个方法作为一个或多个命名属性的“验证器”。

    将方法指定为验证程序，该方法接收属性的名称以及要分配的值，或者在集合的情况下，将要添加到集合的值。然后该函数可以引发验证异常，以阻止进程继续进行（Python内置的`ValueError`和`AssertionError`异常是合理的选择），或者可以修改或替换之前的值诉讼。函数应返回给定的值。

    请注意，集合**的验证程序不能**在验证例程中发出该集合的加载 -
    此用法引发一个断言以避免递归溢出。这是一个不支持的重入条件。

    参数：

    -   **\*名称** [¶](#sqlalchemy.orm.validates.params.*names) -
        要验证的属性名称列表。
    -   **include\_removes**
        [¶](#sqlalchemy.orm.validates.params.include_removes) -

        如果为True，“remove”事件也将被发送 -
        验证函数必须接受一个额外的参数“is\_remove”，它将是一个布尔值。

        New in version 0.7.7.

    -   **include\_backrefs**
        [¶](#sqlalchemy.orm.validates.params.include_backrefs) -

        默认为`True`；如果`False`{.docutils
        .literal}，如果始发者是通过backref相关的属性事件，则验证函数不会发出。这可以用于双向[`validates()`{.xref
        .py .py-func .docutils
        .literal}](#sqlalchemy.orm.validates "sqlalchemy.orm.validates")用法，其中每个属性操作只有一个验证器应该发出。

        版本0.9.0中的新功能

    也可以看看

    [Simple Validators](#simple-validators) - [`validates()`](#sqlalchemy.orm.validates "sqlalchemy.orm.validates")

使用描述符和混合[¶](#using-descriptors-and-hybrids "Permalink to this headline")
--------------------------------------------------------------------------------

为属性生成修改后行为的更全面的方法是使用[descriptors](glossary.html#term-descriptors)。这些通常在Python中使用`property()`函数使用。描述符的标准SQLAlchemy技术是创建一个简单的描述符，并使其从具有不同名称的映射属性读取/写入。下面我们使用Python
2.6样式的属性来说明这一点：

    class EmailAddress(Base):
        __tablename__ = 'email_address'

        id = Column(Integer, primary_key=True)

        # name the attribute with an underscore,
        # different from the column name
        _email = Column("email", String)

        # then create an ".email" attribute
        # to get/set "._email"
        @property
        def email(self):
            return self._email

        @email.setter
        def email(self, email):
            self._email = email

上述方法可行，但我们可以添加更多内容。While our `EmailAddress` object will shuttle the value through the `email` descriptor and into the `_email` mapped
attribute, the class level `EmailAddress.email`
attribute does not have the usual expression semantics usable with
[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query").
为了提供这些，我们改用如下的[`hybrid`](extensions_hybrid.html#module-sqlalchemy.ext.hybrid "sqlalchemy.ext.hybrid")扩展名：

    from sqlalchemy.ext.hybrid import hybrid_property

    class EmailAddress(Base):
        __tablename__ = 'email_address'

        id = Column(Integer, primary_key=True)

        _email = Column("email", String)

        @hybrid_property
        def email(self):
            return self._email

        @email.setter
        def email(self, email):
            self._email = email

`.email`属性除了在我们拥有`EmailAddress`实例时提供getter /
setter行为外，还在类级别使用时提供了SQL表达式，也就是说，直接从`EmailAddress`类：

    from sqlalchemy.orm import Session
    session = Session()

    sqladdress = session.query(EmailAddress).\
                     filter(EmailAddress.email == 'address@example.com').\
                     one()
    SELECT address.email AS address_email, address.id AS address_id
    FROM address
    WHERE address.email = ?
    ('address@example.com',)

    address.email = 'otheraddress@example.com'
    sqlsession.commit()
    UPDATE address SET email=? WHERE address.id = ?
    ('otheraddress@example.com', 1)
    COMMIT

[`hybrid_property`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")还允许我们改变属性的行为，包括定义在实例级别与类/表达级别访问属性时使用[`hybrid_property.expression()`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property.expression "sqlalchemy.ext.hybrid.hybrid_property.expression")修饰符。比如，如果我们想自动添加一个主机名，我们可以定义两组字符串操作逻辑：

    class EmailAddress(Base):
        __tablename__ = 'email_address'

        id = Column(Integer, primary_key=True)

        _email = Column("email", String)

        @hybrid_property
        def email(self):
            """Return the value of _email up until the last twelve
            characters."""

            return self._email[:-12]

        @email.setter
        def email(self, email):
            """Set the value of _email, tacking on the twelve character
            value @example.com."""

            self._email = email + "@example.com"

        @email.expression
        def email(cls):
            """Produce a SQL expression that represents the value
            of the _email column, minus the last twelve characters."""

            return func.substr(cls._email, 0, func.length(cls._email) - 12)

以上，访问`EmailAddress`实例的`email`属性将返回`_email`属性的值，删除或添加主机名`@example.com`中的值。当我们查询`email`属性时，会呈现一个SQL函数，它会产生相同的效果：

    sqladdress = session.query(EmailAddress).filter(EmailAddress.email == 'address').one()
    SELECT address.email AS address_email, address.id AS address_id
    FROM address
    WHERE substr(address.email, ?, length(address.email) - ?) = ?
    (0, 12, 'address')

在[Hybrid
Attributes](extensions_hybrid.html)中了解更多关于混合动力的信息。

同义词[¶ T0\>](#synonyms "Permalink to this headline")
------------------------------------------------------

同义词是映射级别的结构，它允许类的任何属性“镜像”映射的另一个属性。

从最基本的意义上说，同义词是通过附加名称提供某个特定属性的简单方法：

    class MyClass(Base):
        __tablename__ = 'my_table'

        id = Column(Integer, primary_key=True)
        job_status = Column(String(50))

        status = synonym("job_status")

上面的类`MyClass`具有两个属性，即`.job_status`和`.status`，它们在表达式级别上表现为一个属性：

    >>> print(MyClass.job_status == 'some_status')
    my_table.job_status = :job_status_1

    >>> print(MyClass.status == 'some_status')
    my_table.job_status = :job_status_1

并在实例级别：

    >>> m1 = MyClass(status='x')
    >>> m1.status, m1.job_status
    ('x', 'x')

    >>> m1.job_status = 'y'
    >>> m1.status, m1.job_status
    ('y', 'y')

[`synonym()`](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")可以用于任何类型的映射属性，该属性的子类为[`MapperProperty`](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")，包括映射列和关系以及同义词本身。

除了简单的镜像之外，也可以使用[`synonym()`](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")来引用用户定义的[descriptor](glossary.html#term-descriptor)。我们可以用`@property`提供我们的`status`同义词：

    class MyClass(Base):
        __tablename__ = 'my_table'

        id = Column(Integer, primary_key=True)
        status = Column(String(50))

        @property
        def job_status(self):
            return "Status: " + self.status

        job_status = synonym("status", descriptor=job_status)

当使用Declarative时，可以使用[`synonym_for()`](extensions_declarative_api.html#sqlalchemy.ext.declarative.synonym_for "sqlalchemy.ext.declarative.synonym_for")装饰器更简洁地表达上述模式：

    from sqlalchemy.ext.declarative import synonym_for

    class MyClass(Base):
        __tablename__ = 'my_table'

        id = Column(Integer, primary_key=True)
        status = Column(String(50))

        @synonym_for("status")
        @property
        def job_status(self):
            return "Status: " + self.status

虽然[`synonym()`](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")对于简单镜像很有用，但使用[hybrid
attribute](#mapper-hybrids)特性更好地处理了在描述符中增强属性行为的用例，朝向Python描述符。从技术上讲，一个[`synonym()`](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")可以完成[`hybrid_property`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")所能做的所有事情，因为它还支持注入自定义SQL功能，但混合使用更为简单的情况。

 `sqlalchemy.orm.`{.descclassname}`synonym`{.descname}(*name*, *map\_column=None*, *descriptor=None*, *comparator\_factory=None*, *doc=None*, *info=None*)[¶](#sqlalchemy.orm.synonym "Permalink to this definition")
:   将属性名称表示为映射属性的同义词，因为该属性将镜像另一个属性的值和表达式行为。

    参数：

    -   **名称** [¶](#sqlalchemy.orm.synonym.params.name) -
        现有映射属性的名称。这可以引用该类上配置的任何[`MapperProperty`{.xref
        .py .py-class .docutils
        .literal}](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的字符串名称，包括列绑定的属性和关系。
    -   **descriptor**[¶](#sqlalchemy.orm.synonym.params.descriptor) – a
        Python [descriptor](glossary.html#term-descriptor) that will be
        used as a getter (and potentially a setter) when this attribute
        is accessed at the instance level.
    -   **map\_column** [¶](#sqlalchemy.orm.synonym.params.map_column) -

        if `True`, the [`synonym()`{.xref .py
        .py-func .docutils
        .literal}](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")
        construct will locate the existing named [`MapperProperty`{.xref
        .py .py-class .docutils
        .literal}](internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")
        based on the attribute name of this [`synonym()`{.xref .py
        .py-func .docutils
        .literal}](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym"),
        and assign it to a new attribute linked to the name of this
        [`synonym()`](#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym").
        也就是说，给定一个映射如下：

            class MyClass(Base):
                __tablename__ = 'my_table'

                id = Column(Integer, primary_key=True)
                job_status = Column(String(50))

                job_status = synonym("_job_status", map_column=True)

        The above class `MyClass` will now have the
        `job_status` [`Column`{.xref .py .py-class
        .docutils
        .literal}](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        object mapped to the attribute named `_job_status`{.docutils
        .literal}, and the attribute named `job_status`{.docutils
        .literal} will refer to the synonym itself.
        此功能通常与`descriptor`{.docutils
        .literal}参数结合使用，以便将用户定义的描述符作为现有列的“包装器”链接。

    -   **info** [¶](#sqlalchemy.orm.synonym.params.info) -

        可选数据字典，将填充到此对象的`InspectionAttr.info`{.xref .py
        .py-attr .docutils .literal}属性中。

        版本1.0.0中的新功能

    -   **comparator\_factory**
        [¶](#sqlalchemy.orm.synonym.params.comparator_factory) -

        [`PropComparator`](internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")的子类，将在SQL表达式级别提供自定义比较行为。

        注意

        对于提供重新定义属性的Python级别和SQL表达级别行为的属性的用例，请参阅[Using
        Descriptors and
        Hybrids](#mapper-hybrids)中介绍的Hybrid属性以获得更有效的技术。

    也可以看看

    [Synonyms](#synonyms) - 功能的例子。

    [Using Descriptors and Hybrids](#mapper-hybrids) -
    与同义词相比，混合为更复杂的属性包装方案提供了更好的方法。

操作员定制[¶](#operator-customization "Permalink to this headline")
-------------------------------------------------------------------

SQLAlchemy
ORM和Core表达式语言使用的“操作符”是完全可定制的。例如，比较表达式`User.name == 'ed'`使用Python内置的运算符本身称为`operator.eq`
-
可修改SQLAlchemy与此类运算符关联的实际SQL构造。新操作也可以与列表达式相关联。发生在列表达式上的运算符在类型级别上被直接重新定义
- 请参阅[Redefining and Creating New
Operators](core_custom_types.html#types-operators)部分的描述。

ORM level functions like [`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property"),
[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
and [`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
also provide for operator redefinition at the ORM level, by passing a
[`PropComparator`](internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")
subclass to the `comparator_factory` argument of
each function.
在这个级别定制运营商是一种罕见的用例。请参阅[`PropComparator`](internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")中的文档以获取概述。
