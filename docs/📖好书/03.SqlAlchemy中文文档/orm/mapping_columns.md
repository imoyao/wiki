---
title: 映射表列
date: 2021-02-20 22:41:45
permalink: /sqlalchemy/orm/mapping_columns/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
映射表列[¶](#mapping-table-columns "Permalink to this headline")
================================================================

[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")的默认行为是将映射的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的所有列汇编为映射对象属性，每个列都根据列本身的名称进行命名特别是[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的`key`属性）。这种行为可以通过几种方式进行修改。

命名与属性名称明显不同的列[¶](#naming-columns-distinctly-from-attribute-names "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------

默认情况下，映射与[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")共享与映射属性相同的名称
- 具体而言，它匹配[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")上的`Column.key`属性，默认情况下它与`Column.name`相同。

分配给映射到[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的 Python 属性的名称可以与`Column.name`或`Column.key`不同，只需通过指定正如我们在声明性映射中所说明的那样：

    class User(Base):plain
        __tablename__ = 'user'
        id = Column('user_id', Integer, primary_key=True)
        name = Column('user_name', String(50))

Where above `User.id` resolves to a column named
`user_id` and `User.name`
resolves to a column named `user_name`.

映射到现有表格时，可以直接引用[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象：

    class User(Base):plainplainplainplain
        __table__ = user_table
        id = user_table.c.user_id
        name = user_table.c.user_name

或者在经典的映射中，使用所需的键将其放置在`properties`字典中：

    mapper(User, user_table, properties={plainplainplainplain
       'id': user_table.c.user_id,
       'name': user_table.c.user_name,
    })

在下一节中，我们将更仔细地检查`.key`的用法。

自动化来自反射表的列命名方案[¶](#automating-column-naming-schemes-from-reflected-tables "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------

在上一节[Naming Columns Distinctly from Attribute
Names](#mapper-column-distinct-names)中，我们展示了显式映射到类的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")如何可以具有与该列不同的属性名称。但是，如果我们没有明确列出[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，而是使用反射自动生成[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象（例如，如[Reflecting
Database
Objects](core_reflection.html)在这种情况下，我们可以利用[`DDLEvents.column_reflect()`](core_events.html#sqlalchemy.events.DDLEvents.column_reflect "sqlalchemy.events.DDLEvents.column_reflect")事件来拦截[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的生成并为它们提供`Column.key`

    @event.listens_for(Table, "column_reflect")
    def column_reflect(inspector, table, column_info):
        # set column.key = "attr_<lower_case_name>"
        column_info['key'] = "attr_%s" % column_info['name'].lower()

通过上述事件，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的反射将被我们的事件拦截，该事件添加了一个新的“.key”元素，如下图所示：

    class MyClass(Base):
        __table__ = Table("some_table", Base.metadata,
                    autoload=True, autoload_with=some_engine)

如果我们想限定事件只对上面的特定[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象作出反应，我们可以在我们的事件中检查它：

    @event.listens_for(Table, "column_reflect")
    def column_reflect(inspector, table, column_info):
        if table.metadata is Base.metadata:
            # set column.key = "attr_<lower_case_name>"
            column_info['key'] = "attr_%s" % column_info['name'].lower()

用前缀[命名所有列¶](#naming-all-columns-with-a-prefix "Permalink to this headline")
-----------------------------------------------------------------------------------

通常在映射到现有的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象时使用`column_prefix`作为列名前缀的快速方法：

    class User(Base):plainplain
        __table__ = user_table
        __mapper_args__ = {'column_prefix':'_'}

以上将放置诸如`_user_id`，`_user_name`，`_password`等属性名称。在映射的`User`类上。

这种方法在现代用法中不常见。为了处理反映表，更灵活的方法是使用[Automating
Column Naming Schemes from Reflected
Tables](#mapper-automated-reflection-schemes)中描述的方法。

将 column\_property 用于列级选项[¶](#using-column-property-for-column-level-options "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------

使用[`column_property()`](#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")函数映射[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")时可以指定选项。该函数明确地创建[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")用于跟踪[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的[`ColumnProperty`](internals.html#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")；通常，[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")会自动创建它。使用[`column_property()`](#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")，我们可以传递关于如何映射[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的额外参数。下面，我们传递一个选项`active_history`，该选项指定对此列值的更改应导致先前加载的值为前者：

    from sqlalchemy.orm import column_propertyplainplainplainplain

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = column_property(Column(String(50)), active_history=True)

[`column_property()`](#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")
is also used to map a single attribute to multiple columns.
这个用例映射到一个[`join()`](core_selectable.html#sqlalchemy.sql.expression.join "sqlalchemy.sql.expression.join")，它具有彼此相等的属性：

    class User(Base):plainplain
        __table__ = user.join(address)

        # assign "user.id", "address.user_id" to the
        # "id" attribute
        id = column_property(user_table.c.id, address_table.c.user_id)

有关此用法的更多示例，请参阅[Mapping a Class against Multiple
Tables](nonstandard_mappings.html#maptojoin)。

需要[`column_property()`](#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")的另一个地方是将 SQL 表达式指定为映射属性，比如下面我们创建的属性`fullname`，即`firstname`和`lastname`列：

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        firstname = Column(String(50))
        lastname = Column(String(50))
        fullname = column_property(firstname + " " + lastname)

在[SQL Expressions as Mapped
Attributes](mapped_sql_expr.html#mapper-sql-expressions)中查看此用法的示例。

 `sqlalchemy.orm.`{.descclassname}`column_property`{.descname}(*\*columns*, *\*\*kwargs*)[¶](#sqlalchemy.orm.column_property "Permalink to this definition")
:   提供用于 Mapper 的列级属性。

    通常可以直接使用[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")元素将基于列的属性应用于映射器的`properties`字典。当给定的列不直接存在于映射器的可选择范围内时使用此函数；示例包括SQL表达式，函数和标量SELECT查询。plain

    不存在于映射器可选择的列将不会被映射器持久化并且是有效的“只读”属性。

    参数：

    -   **\* cols** [¶](#sqlalchemy.orm.column_property.params.*cols) -
        要映射的列对象的列表。
    -   **active\_history = False**
        [¶](#sqlalchemy.orm.column_property.params.active_history) -

        当`True`时，表示标量属性的“上一个”值在替换时应加载，如果尚未加载。通常，简单的非主键标量值的历史跟踪逻辑只需要知道“新”值就可以执行刷新。此标志可用于使用[`attributes.get_history()`](session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")或[`Session.is_modified()`](session_api.html#sqlalchemy.orm.session.Session.is_modified "sqlalchemy.orm.session.Session.is_modified")的应用程序，该应用程序还需要知道属性的“上一个”值。

        New in version 0.6.6.

    -   **comparator\_factory**[¶](#sqlalchemy.orm.column_property.params.comparator_factory)
        – a class which extends [`ColumnProperty.Comparator`](internals.html#sqlalchemy.orm.properties.ColumnProperty.Comparator "sqlalchemy.orm.properties.ColumnProperty.Comparator")
        which provides custom SQL clause generation for comparison
        operations.
    -   **group**[¶](#sqlalchemy.orm.column_property.params.group) – a
        group name for this property when marked as deferred.
    -   **deferred**[¶](#sqlalchemy.orm.column_property.params.deferred)
        – when True, the column property is “deferred”, meaning that it
        does not load immediately, and is instead loaded when the
        attribute is first accessed on an instance.
        另见[`deferred()`](loading_columns.html#sqlalchemy.orm.deferred "sqlalchemy.orm.deferred")。
    -   **doc**[¶](#sqlalchemy.orm.column_property.params.doc) –
        optional string that will be applied as the doc on the
        class-bound descriptor.
    -   **expire\_on\_flush = True**
        [¶](#sqlalchemy.orm.column_property.params.expire_on_flush) -

        在刷新时禁用过期。引用SQL表达式（而不是单个表绑定列）的column\_property()被认为是“只读”属性；填充它对数据状态没有影响，它只能返回数据库状态。出于这个原因，只要父对象涉及到刷新，即在刷新中有任何种类的“脏”状态，column\_property()的值就会过期。将该参数设置为`False`将产生在刷新过程结束后保留​​现有值的效果。但请注意，具有默认到期设置的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")仍会在[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")调用之后过期所有属性。

        New in version 0.7.3.

    -   **info** [¶](#sqlalchemy.orm.column_property.params.info) -

        可选数据字典，将填充到此对象的[`MapperProperty.info`](internals.html#MapperProperty.info "MapperProperty.info")属性中。

        0.8版本中的新功能

    -   **extension**[¶](#sqlalchemy.orm.column_property.params.extension)
        – an [`AttributeExtension`](deprecated.html#sqlalchemy.orm.interfaces.AttributeExtension "sqlalchemy.orm.interfaces.AttributeExtension")
        instance, or list of extensions, which will be prepended to the
        list of attribute listeners for the resulting descriptor placed
        on the class. **已过时。 T0\>**请参阅[`AttributeEvents`](events.html#sqlalchemy.orm.events.AttributeEvents "sqlalchemy.orm.events.AttributeEvents")。

映射表列的子集[¶](#mapping-a-subset-of-table-columns "Permalink to this headline")
----------------------------------------------------------------------------------

有时，使用[Reflecting Database
Objects](core_reflection.html#metadata-reflection)中描述的反映过程来使[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象可用于从数据库加载表结构。对于有很多不需要在应用程序中引用的列的表，可以使用`include_properties`或`exclude_properties`参数指定只有列的子集应该是映射。例如：

    class User(Base):plainplainplainplain
        __table__ = user_table
        __mapper_args__ = {
            'include_properties' :['user_id', 'user_name']
        }

...将`User`类映射到`user_table`表，仅包括`user_id`和`user_name`列 - 其余未被引用。同理：

    class Address(Base):plainplain
        __table__ = address_table
        __mapper_args__ = {
            'exclude_properties' : ['street', 'city', 'state', 'zip']
        }

...将`Address`类映射到`address_table`表，其中包括除`street`，`city`之外的所有列。 `state`和`zip`。

使用此映射时，未包含的列将不会在由[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")发出的任何 SELECT 语句中引用，也不会在表示该列的映射类上存在任何映射属性；分配该名称的属性将不会超出正常 Python 属性分配的作用。

在某些情况下，多个列可能具有相同的名称，例如映射到共享某个列名的两个或多个表的连接时。`include_properties`和`exclude_properties`也可以容纳[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象来更准确地描述应该包含或排除哪些列：

    class UserAddress(Base):plain
        __table__ = user_table.join(addresses_table)
        __mapper_args__ = {
            'exclude_properties' :[address_table.c.id],
            'primary_key' : [user_table.c.id]
        }

注意

insert and update defaults configured on individual [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
objects, i.e. those described at [Column Insert/Update
Defaults](core_defaults.html#metadata-defaults) including those
configured by the `default`, `update`, `server_default` and
`server_onupdate` arguments, will continue to
function normally even if those [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
objects are not mapped. 这是因为在`default`和`update`的情况下，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象仍然存在于[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中，从而允许默认函数在 ORM 发出 INSERT 或 UPDATE 时发生，而在`server_default`和`server_onupdate`的情况下，关系数据库本身维护这些函数。
