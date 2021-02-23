---
title: events
date: 2021-02-20 22:41:34
permalink: /pages/5aeacd/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
ORM事件[¶](#orm-events "Permalink to this headline")
====================================================

ORM包含各种可用于订阅的挂钩。

有关最常用的ORM事件的介绍，请参见[Tracking Object and Session Changes
with
Events](session_events.html)部分。一般的事件系统在[Events](core_event.html)讨论。非ORM事件（如关于连接和低级语句执行的事件）在[Core
Events](core_events.html)中描述。

属性事件[¶](#attribute-events "Permalink to this headline")
-----------------------------------------------------------

*class* `sqlalchemy.orm.events。`{.descclassname} `AttributeEvents`{.descname} [¶](#sqlalchemy.orm.events.AttributeEvents "Permalink to this definition")
:   基础：[`sqlalchemy.event.base.Events`](core_events.html#sqlalchemy.event.base.Events "sqlalchemy.event.base.Events")

    定义对象属性的事件。

    这些通常在目标类的类绑定描述符上定义。

    例如。：

        from sqlalchemy import event

        def my_append_listener(target, value, initiator):
            print "received append event for target: %s" % target

        event.listen(MyClass.collection, 'append', my_append_listener)

    当`retval=True`标志传递给[`listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")时，监听器可以选择返回值的可能修改版本：

        def validate_phone(target, value, oldvalue, initiator):
            "Strip non-numeric characters from a phone number"

            return re.sub(r'(?![0-9])', '', value)

        # setup listener on UserContact.phone attribute, instructing
        # it to use the return value
        listen(UserContact.phone, 'set', validate_phone, retval=True)

    类似上面的验证函数也会引发异常，例如`ValueError`来暂停操作。

    [`listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")函数可以使用几个修饰符。

    参数：

    -   **active\_history=False**[¶](#sqlalchemy.orm.events.AttributeEvents.params.active_history)
        – When True, indicates that the “set” event would like to
        receive the “old” value being replaced unconditionally, even if
        this requires firing off database loads.
        请注意，`active_history`也可以直接通过[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")和[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")设置。
    -   **propagate=False**[¶](#sqlalchemy.orm.events.AttributeEvents.params.propagate)
        – When True, the listener function will be established not just
        for the class attribute given, but for attributes of the same
        name on all current subclasses of that class, as well as all
        future subclasses of that class, using an additional listener
        that listens for instrumentation events.
    -   **raw=False**[¶](#sqlalchemy.orm.events.AttributeEvents.params.raw)
        – When True, the “target” argument to the event will be the
        [`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")
        management object, rather than the mapped instance itself.
    -   **retval=False**[¶](#sqlalchemy.orm.events.AttributeEvents.params.retval)
        – when True, the user-defined event listening must return the
        “value” argument from the function.
        这使得监听功能有机会改变最终用于“设置”或“追加”事件的值。

    `append`{.descname} （ *target*，*值*，*发起人* ） [¶ T6\>](#sqlalchemy.orm.events.AttributeEvents.append "Permalink to this definition")
    :   收到追加追加事件。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass.some_attribute, 'append')
            def receive_append(target, value, initiator):
                "listen for the 'append' event"

                # ... (event handling logic) ...

        参数：

        -   **target**[¶](#sqlalchemy.orm.events.AttributeEvents.append.params.target)
            – the object instance receiving the event.
            如果侦听器使用`raw=True`进行注册，则这将是[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")对象。
        -   **value**[¶](#sqlalchemy.orm.events.AttributeEvents.append.params.value)
            – the value being appended.
            如果此侦听器使用`retval=True`进行注册，那么侦听器函数必须返回此值或替换它的新值。
        -   **发起人**
            [¶](#sqlalchemy.orm.events.AttributeEvents.append.params.initiator)
            -

            表示事件启动的[`attributes.Event`](internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")实例。可以通过backref处理程序从其原始值进行修改，以控制链式事件传播。

            在版本0.9.0中更改： `initiator`参数现在作为[`attributes.Event`](internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")对象传递，并且可以通过一个backref处理程序反向链接事件链。

        返回：

        如果事件使用`retval=True`注册，则应返回给定值或新的有效值。

     `dispose_collection`{.descname}(*target*, *collection*, *collection\_adpater*)[¶](#sqlalchemy.orm.events.AttributeEvents.dispose_collection "Permalink to this definition")
    :   收到“收集处理”事件。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass.some_attribute, 'dispose_collection')
            def receive_dispose_collection(target, collection, collection_adpater):
                "listen for the 'dispose_collection' event"

                # ... (event handling logic) ...

        当集合被替换时，此事件会触发基于集合的属性，即：

            u1.addresses.append(a1)

            u1.addresses = [a2, a3]  # <- old collection is disposed

        事件的机制通常包括给定的集合是空的，即使它在被替换时存储对象。

        版本1.0.0新增： [`AttributeEvents.init_collection()`](#sqlalchemy.orm.events.AttributeEvents.init_collection "sqlalchemy.orm.events.AttributeEvents.init_collection")和[`AttributeEvents.dispose_collection()`](#sqlalchemy.orm.events.AttributeEvents.dispose_collection "sqlalchemy.orm.events.AttributeEvents.dispose_collection")事件取代`collection.linker`

    `init_collection`{.descname} （ *target*，*collection*，*collection\_adapter* ） [¶ T6\>](#sqlalchemy.orm.events.AttributeEvents.init_collection "Permalink to this definition")
    :   接收'collection init'事件。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass.some_attribute, 'init_collection')
            def receive_init_collection(target, collection, collection_adapter):
                "listen for the 'init_collection' event"

                # ... (event handling logic) ...

        当为空白属性首次生成初始“空集合”时，以及集合被替换为新集合时（例如通过设置事件），此事件将触发基于集合的属性。

        例如，假设`User.addresses`是一个基于关系的集合，事件在这里触发：

            u1 = User()
            u1.addresses.append(a1)  #  <- new collection

        并且在更换操作期间：

            u1.addresses = [a2, a3]  #  <- new collection

        参数：

        -   **target**[¶](#sqlalchemy.orm.events.AttributeEvents.init_collection.params.target)
            – the object instance receiving the event.
            如果侦听器使用`raw=True`进行注册，则这将是[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")对象。
        -   **集合**
            [¶](#sqlalchemy.orm.events.AttributeEvents.init_collection.params.collection)
            -
            新集合。这将始终由指定为[`RelationshipProperty.collection_class`](internals.html#sqlalchemy.orm.properties.RelationshipProperty.params.collection_class "sqlalchemy.orm.properties.RelationshipProperty")的内容生成，并且将始终为空。
        -   **collection\_adpater**[¶](#sqlalchemy.orm.events.AttributeEvents.init_collection.params.collection_adpater)
            – the [`CollectionAdapter`](collections.html#sqlalchemy.orm.collections.CollectionAdapter "sqlalchemy.orm.collections.CollectionAdapter")
            that will mediate internal access to the collection.

        版本1.0.0新增： [`AttributeEvents.init_collection()`](#sqlalchemy.orm.events.AttributeEvents.init_collection "sqlalchemy.orm.events.AttributeEvents.init_collection")和[`AttributeEvents.dispose_collection()`](#sqlalchemy.orm.events.AttributeEvents.dispose_collection "sqlalchemy.orm.events.AttributeEvents.dispose_collection")事件取代`collection.linker`

     `init_scalar`{.descname}(*target*, *value*, *dict\_*)[¶](#sqlalchemy.orm.events.AttributeEvents.init_scalar "Permalink to this definition")
    :   接收标量“init”事件。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass.some_attribute, 'init_scalar')
            def receive_init_scalar(target, value, dict_):
                "listen for the 'init_scalar' event"

                # ... (event handling logic) ...

        当访问未初始化的，未执行的标量属性时，将调用此事件。在这种情况下通常会返回`None`的值；对对象的状态不做任何更改。

        事件处理程序可以通过两种方式来改变这种行为。一种是可以返回`None`以外的值。另一个原因是该值可能被建立为对象状态的一部分，这也会产生持续的效果。

        典型用途是在访问时建立属性的特定默认值：

            SOME_CONSTANT = 3.1415926

            @event.listens_for(
                MyClass.some_attribute, "init_scalar",
                retval=True, propagate=True)
            def _init_some_attribute(target, dict_, value):
                dict_['some_attribute'] = SOME_CONSTANT
                return SOME_CONSTANT

        上面，我们将属性`MyClass.some_attribute`初始化为`SOME_CONSTANT`的值。以上代码包含以下功能：

        -   通过在给定的`dict_`中设置值`SOME_CONSTANT`，我们表明该值将被持久化到数据库。**如果我们明确地将它与对象**关联，那么给定的值只能保存到数据库中。给定的`dict_`是映射对象的`__dict__`元素，假定默认的属性检测系统就位。
        -   通过建立`retval=True`标志，我们从函数返回的值将由属性getter返回。没有这个标志，事件被认为是一个被动的观察者，我们的函数的返回值被忽略。
        -   如果映射类包含继承子类，那么`propagate=True`标志是有意义的，它也会使用此事件侦听器。没有这个标志，继承的子类将不会使用我们的事件处理程序。

        当我们在给定字典中建立值时，该值将用于由工作单元建立的INSERT语句中。通常，`None`的默认返回值不是作为对象的一部分建立的，以避免响应正常被动的“get”操作而发生对象变化的问题，并避免出现问题是否在属性访问操作期间不应该触发[`AttributeEvents.set()`](#sqlalchemy.orm.events.AttributeEvents.set "sqlalchemy.orm.events.AttributeEvents.set")事件。这不会影响INSERT操作，因为`None`值与任何情况下进入数据库的`NULL`的值匹配；请注意，在INSERT期间跳过了`None`，以确保列和SQL级别的默认功能可以触发。

        当我们应用我们的值时，属性设置事件[`AttributeEvents.set()`](#sqlalchemy.orm.events.AttributeEvents.set "sqlalchemy.orm.events.AttributeEvents.set")以及由[`orm.validates`](mapped_attributes.html#sqlalchemy.orm.validates "sqlalchemy.orm.validates")提供的相关验证功能****到给定的`dict_`。要使这些事件响应我们新生成的值而调用，请将该值作为普通属性集操作应用于给定对象：

            SOME_CONSTANT = 3.1415926

            @event.listens_for(
                MyClass.some_attribute, "init_scalar",
                retval=True, propagate=True)
            def _init_some_attribute(target, dict_, value):
                # will also fire off attribute set events
                target.some_attribute = SOME_CONSTANT
                return SOME_CONSTANT

        当设置多个侦听器时，通过将指定`retval=True`的前一个侦听器返回的值作为`value`

        [`AttributeEvents.init_scalar()`](#sqlalchemy.orm.events.AttributeEvents.init_scalar "sqlalchemy.orm.events.AttributeEvents.init_scalar")事件可用于从映射的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象上建立的默认值和/或可调用值中提取值。有关此示例，请参阅[Attribute
        Instrumentation](examples.html#examples-instrumentation)中的“有效列默认值”示例。

        版本1.1中的新功能

        参数：

        -   **target**[¶](#sqlalchemy.orm.events.AttributeEvents.init_scalar.params.target)
            – the object instance receiving the event.
            如果侦听器使用`raw=True`进行注册，则这将是[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")对象。
        -   **value**[¶](#sqlalchemy.orm.events.AttributeEvents.init_scalar.params.value)
            – the value that is to be returned before this event
            listener were invoked. 该值以`None`值开始，但如果存在多个侦听器，则该值将成为先前事件处理函数的返回值。
        -   **dict \_**
            [¶](#sqlalchemy.orm.events.AttributeEvents.init_scalar.params.dict_)
            - 此映射对象的属性字典。这通常是对象的`__dict__`，但在任何情况下都代表属性系统用于获取此属性实际值的目标。在此字典中放置值会影响该值将在由工作单元生成的INSERT语句中使用。

        也可以看看

        [Attribute
        Instrumentation](examples.html#examples-instrumentation) -
        请参阅`active_column_defaults.py`示例。

    `删除`{.descname} （ *target*，*值*，*发起人* ） [¶ T6\>](#sqlalchemy.orm.events.AttributeEvents.remove "Permalink to this definition")
    :   接收收集移除事件。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass.some_attribute, 'remove')
            def receive_remove(target, value, initiator):
                "listen for the 'remove' event"

                # ... (event handling logic) ...

        参数：

        -   **target**[¶](#sqlalchemy.orm.events.AttributeEvents.remove.params.target)
            – the object instance receiving the event.
            如果侦听器使用`raw=True`进行注册，则这将是[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")对象。
        -   **值**
            [¶](#sqlalchemy.orm.events.AttributeEvents.remove.params.value)
            - 被删除的值。
        -   **发起人**
            [¶](#sqlalchemy.orm.events.AttributeEvents.remove.params.initiator)
            -

            表示事件启动的[`attributes.Event`](internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")实例。可以通过backref处理程序从其原始值进行修改，以控制链式事件传播。

            在版本0.9.0中更改： `initiator`参数现在作为[`attributes.Event`](internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")对象传递，并且可以通过一个backref处理程序反向链接事件链。

        返回：

        没有为此事件定义返回值。

     `set`{.descname}(*target*, *value*, *oldvalue*, *initiator*)[¶](#sqlalchemy.orm.events.AttributeEvents.set "Permalink to this definition")
    :   接收标量设置事件。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass.some_attribute, 'set')
            def receive_set(target, value, oldvalue, initiator):
                "listen for the 'set' event"

                # ... (event handling logic) ...

            # named argument style (new in 0.9)
            @event.listens_for(SomeClass.some_attribute, 'set', named=True)
            def receive_set(**kw):
                "listen for the 'set' event"
                target = kw['target']
                value = kw['value']

                # ... (event handling logic) ...

        参数：

        -   **target**[¶](#sqlalchemy.orm.events.AttributeEvents.set.params.target)
            – the object instance receiving the event.
            如果侦听器使用`raw=True`进行注册，则这将是[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")对象。
        -   **值**
            [¶](#sqlalchemy.orm.events.AttributeEvents.set.params.value)
            - 正在设置的值。如果此侦听器使用`retval=True`进行注册，那么侦听器函数必须返回此值或替换它的新值。
        -   **oldvalue**
            [¶](#sqlalchemy.orm.events.AttributeEvents.set.params.oldvalue)
            - 之前的值被替换。这也可能是`NEVER_SET`或`NO_VALUE`的符号。如果侦听器使用`active_history=True`进行注册，则如果现有值当前已卸载或过期，则将从数据库加载该属性的先前值。
        -   **发起人**
            [¶](#sqlalchemy.orm.events.AttributeEvents.set.params.initiator)
            -

            表示事件启动的[`attributes.Event`](internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")实例。可以通过backref处理程序从其原始值进行修改，以控制链式事件传播。

            在版本0.9.0中更改： `initiator`参数现在作为[`attributes.Event`](internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")对象传递，并且可以通过一个backref处理程序反向链接事件链。

        返回：

        如果事件使用`retval=True`注册，则应返回给定值或新的有效值。

Mapper事件[¶](#mapper-events "Permalink to this headline")
----------------------------------------------------------

*class* `sqlalchemy.orm.events。`{.descclassname} `MapperEvents`{.descname} [¶](#sqlalchemy.orm.events.MapperEvents "Permalink to this definition")
:   基础：[`sqlalchemy.event.base.Events`](core_events.html#sqlalchemy.event.base.Events "sqlalchemy.event.base.Events")

    定义特定于映射的事件。

    例如。：

        from sqlalchemy import event

        def my_before_insert_listener(mapper, connection, target):
            # execute a stored procedure upon INSERT,
            # apply the value to the row to be inserted
            target.calculated_value = connection.scalar(
                                        "select my_special_function(%d)"
                                        % target.special_number)

        # associate the listener function with SomeClass,
        # to execute during the "before_insert" hook
        event.listen(
            SomeClass, 'before_insert', my_before_insert_listener)

    可用目标包括：

    -   映射类
    -   未映射的映射或待映射类的超类（使用`propagate=True`标志）
    -   [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象
    -   [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")类本身和[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数指示侦听所有映射器。

    在版本0.8.0中更改：映​​射器事件可以与映射类的未映射超类相关联。

    Mapper事件提供了映射器关键部分的钩子，包括与对象检测，对象加载和对象持久性相关的部分。In
    particular, the persistence methods [`before_insert()`](#sqlalchemy.orm.events.MapperEvents.before_insert "sqlalchemy.orm.events.MapperEvents.before_insert"),
    and [`before_update()`](#sqlalchemy.orm.events.MapperEvents.before_update "sqlalchemy.orm.events.MapperEvents.before_update")
    are popular places to augment the state being persisted - however,
    these methods operate with several significant restrictions.
    鼓励用户评估[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")和[`SessionEvents.after_flush()`](#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")方法作为更灵活和用户友好的钩子，以便在其中应用额外的数据库状态齐平。

    当使用[`MapperEvents`](#sqlalchemy.orm.events.MapperEvents "sqlalchemy.orm.events.MapperEvents")时，[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")函数可以使用几个修饰符。

    参数：

    -   **propagate=False**[¶](#sqlalchemy.orm.events.MapperEvents.params.propagate)
        – When True, the event listener should be applied to all
        inheriting mappers and/or the mappers of inheriting classes, as
        well as any mapper which is the target of this listener.
    -   **raw=False**[¶](#sqlalchemy.orm.events.MapperEvents.params.raw)
        – When True, the “target” argument passed to applicable event
        listener functions will be the instance’s [`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")
        management object, rather than the mapped instance itself.
    -   **retval = False**
        [¶](#sqlalchemy.orm.events.MapperEvents.params.retval) -

        当为True时，用户定义的事件函数必须具有返回值，其目的是控制后续事件传播，或者以其他方式更改映射器正在进行的操作。可能的返回值是：

        -   `sqlalchemy.orm.interfaces.EXT_CONTINUE`
            - 继续正常处理事件。
        -   `sqlalchemy.orm.interfaces.EXT_STOP` -
            取消链中的所有后续事件处理程序。
        -   其他值 - 由特定侦听器指定的返回值。

    ` after_configured  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在配置了一系列映射器之后调用。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'after_configured')
            def receive_after_configured():
                "listen for the 'after_configured' event"

                # ... (event handling logic) ...

        在函数完成其工作后，每次调用[`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")函数时都会调用[`MapperEvents.after_configured()`](#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")事件。[`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
        is typically invoked automatically as mappings are first used,
        as well as each time new mappers have been made available and
        new mapper use is detected.

        将此事件与[`MapperEvents.mapper_configured()`](#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")事件进行比较，该事件在配置操作继续时以每个映射器为基础调用；与该事件不同，当调用此事件时，所有交叉配置（例如backrefs）也将可用于任何挂起的映射器。也可以与[`MapperEvents.before_configured()`](#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")相对照，该映射在配置一系列映射器之前调用。

        This event can **only** be applied to the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
        class or [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
        function, and not to individual mappings or mapped classes.
        它仅针对整个映射进行调用：

            from sqlalchemy.orm import mapper

            @event.listens_for(mapper, "after_configured")
            def go():
                # ...

        理论上这个事件在每个应用程序中被调用一次，但实际上在任何时候调用新的映射器都会受到[`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")调用的影响。如果在已经使用现有映射的情况下构建新的映射，则可能再次调用该事件。为了确保一个特定的事件只被调用一次而不再进行，可以应用`once=True`参数（0.9.4中的新值）：

            from sqlalchemy.orm import mapper

            @event.listens_for(mapper, "after_configured", once=True)
            def go():
                # ...

        也可以看看

        [`MapperEvents.mapper_configured()`](#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")

        [`MapperEvents.before_configured()`](#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")

    `after_delete`{.descname} （ *mapper*，*connection*，*target* ） [¶ T6\>](#sqlalchemy.orm.events.MapperEvents.after_delete "Permalink to this definition")
    :   在发出与该实例相对应的DELETE语句之后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'after_delete')
            def receive_after_delete(mapper, connection, target):
                "listen for the 'after_delete' event"

                # ... (event handling logic) ...

        此事件用于在给定连接上发出其他SQL语句，以及执行与删除事件相关的应用程序特定簿记。

        在上一步中，它们的DELETE语句同时发出后，该事件通常被称为同一类的一批对象。

        警告

        Mapper级别的刷新事件只允许**非常有限的操作**，仅对本地行的属性进行操作，并允许在给定的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发出任何SQL。**请完整阅读[Mapper-level
        Events](session_events.html#session-persistence-mapper)中的注释以获取使用这些方法的指导原则；通常，[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")方法对于一般的冲洗更改应该是首选。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.after_delete.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **connection**[¶](#sqlalchemy.orm.events.MapperEvents.after_delete.params.connection)
            – the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            being used to emit DELETE statements for this instance.
            这为特定于此实例的目标数据库上的当前事务提供了一个句柄。
        -   **target**
            [¶](#sqlalchemy.orm.events.MapperEvents.after_delete.params.target)
            - 被删除的映射实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。

        返回：

        此事件不支持返回值。

        也可以看看

        [Persistence
        Events](session_events.html#session-persistence-events)

     `after_insert`{.descname}(*mapper*, *connection*, *target*)[¶](#sqlalchemy.orm.events.MapperEvents.after_insert "Permalink to this definition")
    :   在对应于该实例的INSERT语句发出后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'after_insert')
            def receive_after_insert(mapper, connection, target):
                "listen for the 'after_insert' event"

                # ... (event handling logic) ...

        在发生INSERT之后，此事件用于修改实例中的纯Python内部状态，以及在给定连接上发出其他SQL语句。

        在先前步骤中一次发出INSERT语句后，通常会调用该事件的一批对象。在极不常见的情况下，可以使用`batch=False`配置[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")，这将导致批次实例被分解为单个和更差的表现）事件
        - \>持续 - \>事件步骤。

        警告

        Mapper级别的刷新事件只允许**非常有限的操作**，仅对本地行的属性进行操作，并允许在给定的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发出任何SQL。**请完整阅读[Mapper-level
        Events](session_events.html#session-persistence-mapper)中的注释以获取使用这些方法的指导原则；通常，[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")方法对于一般的冲洗更改应该是首选。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.after_insert.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **connection**[¶](#sqlalchemy.orm.events.MapperEvents.after_insert.params.connection)
            – the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            being used to emit INSERT statements for this instance.
            这为特定于此实例的目标数据库上的当前事务提供了一个句柄。
        -   **target**[¶](#sqlalchemy.orm.events.MapperEvents.after_insert.params.target)
            – the mapped instance being persisted.
            如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。

        返回：

        此事件不支持返回值。

        也可以看看

        [Persistence
        Events](session_events.html#session-persistence-events)

     `after_update`{.descname}(*mapper*, *connection*, *target*)[¶](#sqlalchemy.orm.events.MapperEvents.after_update "Permalink to this definition")
    :   在对应于该实例的UPDATE语句发出后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'after_update')
            def receive_after_update(mapper, connection, target):
                "listen for the 'after_update' event"

                # ... (event handling logic) ...

        在发生UPDATE之后，此事件用于修改实例中的纯Python内部状态，以及在给定连接上发出其他SQL语句。

        This method is called for all instances that are marked as
        “dirty”, *even those which have no net changes to their
        column-based attributes*, and for which no UPDATE statement has
        proceeded. 当一个对象的任何基于列的属性有一个被调用的“set
        attribute”操作或当它的任何集合被修改时，这个对象被标记为脏。如果在更新时没有基于列的属性有任何净更改，则不会发布UPDATE语句。这意味着发送到[`after_update()`](#sqlalchemy.orm.events.MapperEvents.after_update "sqlalchemy.orm.events.MapperEvents.after_update")的实例*不是*保证已发布UPDATE语句。

        要检测对象上的基于列的属性是否具有净更改并因此生成UPDATE语句，请使用`object_session（instance）.is_modified（instance， include_collections = False）  T2>  T0>。`

        在上一步中，它们的UPDATE语句一次被发出后，该事件通常被称为同一类的一批对象。在极不常见的情况下，可以使用`batch=False`配置[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")，这将导致批次实例被分解为单个和更差的表现）事件
        - \>持续 - \>事件步骤。

        警告

        Mapper级别的刷新事件只允许**非常有限的操作**，仅对本地行的属性进行操作，并允许在给定的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发出任何SQL。**请完整阅读[Mapper-level
        Events](session_events.html#session-persistence-mapper)中的注释以获取使用这些方法的指导原则；通常，[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")方法对于一般的冲洗更改应该是首选。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.after_update.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **connection**[¶](#sqlalchemy.orm.events.MapperEvents.after_update.params.connection)
            – the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            being used to emit UPDATE statements for this instance.
            这为特定于此实例的目标数据库上的当前事务提供了一个句柄。
        -   **target**[¶](#sqlalchemy.orm.events.MapperEvents.after_update.params.target)
            – the mapped instance being persisted.
            如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。

        返回：

        此事件不支持返回值。

        也可以看看

        [Persistence
        Events](session_events.html#session-persistence-events)

    ` before_configured  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在一系列映射器配置之前调用。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'before_configured')
            def receive_before_configured():
                "listen for the 'before_configured' event"

                # ... (event handling logic) ...

        The [`MapperEvents.before_configured()`](#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")
        event is invoked each time the [`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
        function is invoked, before the function has done any of its
        work. [`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
        is typically invoked automatically as mappings are first used,
        as well as each time new mappers have been made available and
        new mapper use is detected.

        This event can **only** be applied to the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
        class or [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
        function, and not to individual mappings or mapped classes.
        它仅针对整个映射进行调用：

            from sqlalchemy.orm import mapper

            @event.listens_for(mapper, "before_configured")
            def go():
                # ...

        将此事件与[`MapperEvents.after_configured()`](#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")约束在配置一系列映射器之后调用，以及[`MapperEvents.mapper_configured()`](#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")尽可能地配置每个映射器。

        理论上这个事件在每个应用程序中被调用一次，但实际上在任何时候调用新的映射器都会受到[`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")调用的影响。如果在已经使用现有映射的情况下构建新的映射，则可能再次调用该事件。为了确保一个特定的事件只被调用一次而不再进行，可以应用`once=True`参数（0.9.4中的新值）：

            from sqlalchemy.orm import mapper

            @event.listens_for(mapper, "before_configured", once=True)
            def go():
                # ...

        版本0.9.3中的新功能

        也可以看看

        [`MapperEvents.mapper_configured()`](#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")

        [`MapperEvents.after_configured()`](#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")

     `before_delete`{.descname}(*mapper*, *connection*, *target*)[¶](#sqlalchemy.orm.events.MapperEvents.before_delete "Permalink to this definition")
    :   在与该实例相对应的DELETE语句发出之前接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'before_delete')
            def receive_before_delete(mapper, connection, target):
                "listen for the 'before_delete' event"

                # ... (event handling logic) ...

        此事件用于在给定连接上发出其他SQL语句，以及执行与删除事件相关的应用程序特定簿记。

        在稍后的步骤中一次发出DELETE语句之前，通常会调用该事件的一批对象。

        警告

        Mapper级别的刷新事件只允许**非常有限的操作**，仅对本地行的属性进行操作，并允许在给定的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发出任何SQL。**请完整阅读[Mapper-level
        Events](session_events.html#session-persistence-mapper)中的注释以获取使用这些方法的指导原则；通常，[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")方法对于一般的冲洗更改应该是首选。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.before_delete.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **connection**[¶](#sqlalchemy.orm.events.MapperEvents.before_delete.params.connection)
            – the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            being used to emit DELETE statements for this instance.
            这为特定于此实例的目标数据库上的当前事务提供了一个句柄。
        -   **target**
            [¶](#sqlalchemy.orm.events.MapperEvents.before_delete.params.target)
            - 被删除的映射实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。

        返回：

        此事件不支持返回值。

        也可以看看

        [Persistence
        Events](session_events.html#session-persistence-events)

    `before_insert`{.descname} （ *mapper*，*connection*，*target* ） [¶ T6\>](#sqlalchemy.orm.events.MapperEvents.before_insert "Permalink to this definition")
    :   在对应于该实例的INSERT语句发出之前接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'before_insert')
            def receive_before_insert(mapper, connection, target):
                "listen for the 'before_insert' event"

                # ... (event handling logic) ...

        在发生INSERT之前，此事件用于修改实例上的本地非对象相关属性，以及在给定连接上发出其他SQL语句。

        在稍后的步骤中一次发出INSERT语句之前，通常会调用该事件的一批对象。在极不常见的情况下，可以使用`batch=False`配置[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")，这将导致批次实例被分解为单个和更差的表现）事件
        - \>持续 - \>事件步骤。

        警告

        Mapper级别的刷新事件只允许**非常有限的操作**，仅对本地行的属性进行操作，并允许在给定的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发出任何SQL。**请完整阅读[Mapper-level
        Events](session_events.html#session-persistence-mapper)中的注释以获取使用这些方法的指导原则；通常，[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")方法对于一般的冲洗更改应该是首选。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.before_insert.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **connection**[¶](#sqlalchemy.orm.events.MapperEvents.before_insert.params.connection)
            – the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            being used to emit INSERT statements for this instance.
            这为特定于此实例的目标数据库上的当前事务提供了一个句柄。
        -   **target**[¶](#sqlalchemy.orm.events.MapperEvents.before_insert.params.target)
            – the mapped instance being persisted.
            如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。

        返回：

        此事件不支持返回值。

        也可以看看

        [Persistence
        Events](session_events.html#session-persistence-events)

     `before_update`{.descname}(*mapper*, *connection*, *target*)[¶](#sqlalchemy.orm.events.MapperEvents.before_update "Permalink to this definition")
    :   在对应于该实例的UPDATE语句发出之前接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'before_update')
            def receive_before_update(mapper, connection, target):
                "listen for the 'before_update' event"

                # ... (event handling logic) ...

        此事件用于在发生UPDATE之前修改实例上的本地非对象相关属性，以及在给定连接上发出其他SQL语句。

        This method is called for all instances that are marked as
        “dirty”, *even those which have no net changes to their
        column-based attributes*.
        当一个对象的任何基于列的属性有一个被调用的“set
        attribute”操作或当它的任何集合被修改时，这个对象被标记为脏。如果在更新时没有基于列的属性有任何净更改，则不会发布UPDATE语句。This
        means that an instance being sent to [`before_update()`](#sqlalchemy.orm.events.MapperEvents.before_update "sqlalchemy.orm.events.MapperEvents.before_update")
        is *not* a guarantee that an UPDATE statement will be issued,
        although you can affect the outcome here by modifying attributes
        so that a net change in value does exist.

        要检测对象上的基于列的属性是否具有净更改，并因此会生成UPDATE语句，请使用`object_session（instance）.is_modified（instance， include_collections = False）  T2>  T0>。`

        在稍后的步骤中同时发出UPDATE语句之前，通常会调用该事件的一批对象。在极不常见的情况下，可以使用`batch=False`配置[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")，这将导致批次实例被分解为单个和更差的表现）事件
        - \>持续 - \>事件步骤。

        警告

        Mapper级别的刷新事件只允许**非常有限的操作**，仅对本地行的属性进行操作，并允许在给定的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上发出任何SQL。**请完整阅读[Mapper-level
        Events](session_events.html#session-persistence-mapper)中的注释以获取使用这些方法的指导原则；通常，[`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")方法对于一般的冲洗更改应该是首选。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.before_update.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **connection**[¶](#sqlalchemy.orm.events.MapperEvents.before_update.params.connection)
            – the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            being used to emit UPDATE statements for this instance.
            这为特定于此实例的目标数据库上的当前事务提供了一个句柄。
        -   **target**[¶](#sqlalchemy.orm.events.MapperEvents.before_update.params.target)
            – the mapped instance being persisted.
            如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。

        返回：

        此事件不支持返回值。

        也可以看看

        [Persistence
        Events](session_events.html#session-persistence-events)

     `instrument_class`{.descname}(*mapper*, *class\_*)[¶](#sqlalchemy.orm.events.MapperEvents.instrument_class "Permalink to this definition")
    :   在仪表应用于映射类之前，首先构造映射器时接收类。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'instrument_class')
            def receive_instrument_class(mapper, class_):
                "listen for the 'instrument_class' event"

                # ... (event handling logic) ...

        这个事件是mapper构建的最早阶段。映射器的大多数属性尚未初始化。

        这个监听器既可以应用于整个[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")类，也可以应用于任何未映射的类，它将作为映射类的基础（使用`propagate=True`旗）：

            Base = declarative_base()

            @event.listens_for(Base, "instrument_class", propagate=True)
            def on_new_class(mapper, cls_):
                " ... "

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.instrument_class.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **class \_**
            [¶](#sqlalchemy.orm.events.MapperEvents.instrument_class.params.class_)
            - 映射的类。

     `mapper_configured`{.descname}(*mapper*, *class\_*)[¶](#sqlalchemy.orm.events.MapperEvents.mapper_configured "Permalink to this definition")
    :   当特定映射器在[`configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")调用的范围内完成自己的配置时调用。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'mapper_configured')
            def receive_mapper_configured(mapper, class_):
                "listen for the 'mapper_configured' event"

                # ... (event handling logic) ...

        当[`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")函数继续执行尚未配置的映射器的当前列表时，会为每个映射器调用[`MapperEvents.mapper_configured()`](#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")事件。[`orm.configure_mappers()`](mapping_api.html#sqlalchemy.orm.configure_mappers "sqlalchemy.orm.configure_mappers")
        is typically invoked automatically as mappings are first used,
        as well as each time new mappers have been made available and
        new mapper use is detected.

        当事件被调用时，映射器应该处于最终状态，但是**不包括可能从其他映射器调用的backrefs**；它们可能仍然在配置操作中处于挂起状态。由[`orm.relationship.back_populates`](relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")参数*替代配置的双向关系将*完全可用，因为此类关系不依赖于其他可能未配置的映射器知道它们存在。

        对于确保**所有**映​​射器准备就绪的事件（包括仅在其他映射中定义的backrefs），请使用[`MapperEvents.after_configured()`](#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")事件；只有在完全配置了所有已知的映射后，此事件才会调用。

        The [`MapperEvents.mapper_configured()`](#sqlalchemy.orm.events.MapperEvents.mapper_configured "sqlalchemy.orm.events.MapperEvents.mapper_configured")
        event, unlike [`MapperEvents.before_configured()`](#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")
        or [`MapperEvents.after_configured()`](#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured"),
        is called for each mapper/class individually, and the mapper is
        passed to the event itself.
        它也被称为一次特定的映射器。因此，该事件对于配置步骤非常有用，该配置步骤只能在特定的映射器基础上调用一次，因此不需要“backref”配置必须准备就绪。

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.events.MapperEvents.mapper_configured.params.mapper)
            – the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            which is the target of this event.
        -   **class \_**
            [¶](#sqlalchemy.orm.events.MapperEvents.mapper_configured.params.class_)
            - 映射的类。

        也可以看看

        [`MapperEvents.before_configured()`](#sqlalchemy.orm.events.MapperEvents.before_configured "sqlalchemy.orm.events.MapperEvents.before_configured")

        [`MapperEvents.after_configured()`](#sqlalchemy.orm.events.MapperEvents.after_configured "sqlalchemy.orm.events.MapperEvents.after_configured")

实例事件[¶](#instance-events "Permalink to this headline")
----------------------------------------------------------

*class* `sqlalchemy.orm.events。`{.descclassname} `InstanceEvents`{.descname} [¶](#sqlalchemy.orm.events.InstanceEvents "Permalink to this definition")
:   基础：[`sqlalchemy.event.base.Events`](core_events.html#sqlalchemy.event.base.Events "sqlalchemy.event.base.Events")

    定义特定于对象生命周期的事件。

    例如。：

        from sqlalchemy import event

        def my_load_listener(target, context):
            print "on load!"

        event.listen(SomeClass, 'load', my_load_listener)

    可用目标包括：

    -   映射类
    -   未映射的映射或待映射类的超类（使用`propagate=True`标志）
    -   [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象
    -   [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")类本身和[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数指示侦听所有映射器。

    在版本0.8.0中更改：实例事件可以与映射类的未映射超类相关联。

    实例事件与映射器事件密切相关，但对于实例及其工具更具体，而不是其持久性系统。

    当使用[`InstanceEvents`](#sqlalchemy.orm.events.InstanceEvents "sqlalchemy.orm.events.InstanceEvents")时，[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")函数可以使用几个修饰符。

    参数：

    -   **propagate=False**[¶](#sqlalchemy.orm.events.InstanceEvents.params.propagate)
        – When True, the event listener should be applied to all
        inheriting classes as well as the class which is the target of
        this listener.
    -   **raw=False**[¶](#sqlalchemy.orm.events.InstanceEvents.params.raw)
        – When True, the “target” argument passed to applicable event
        listener functions will be the instance’s [`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")
        management object, rather than the mapped instance itself.

    `expire`{.descname} （ *target*，*attrs* ） [¶](#sqlalchemy.orm.events.InstanceEvents.expire "Permalink to this definition")
    :   在其属性或某个子集已过期后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'expire')
            def receive_expire(target, attrs):
                "listen for the 'expire' event"

                # ... (event handling logic) ...

        'keys'是属性名称的列表。如果没有，则整个州都过期了。

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.expire.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **attrs**[¶](#sqlalchemy.orm.events.InstanceEvents.expire.params.attrs)
            – sequence of attribute names which were expired, or None if
            all attributes were expired.

     `first_init`{.descname}(*manager*, *cls*)[¶](#sqlalchemy.orm.events.InstanceEvents.first_init "Permalink to this definition")
    :   当调用特定映射的第一个实例时调用。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'first_init')
            def receive_first_init(manager, cls):
                "listen for the 'first_init' event"

                # ... (event handling logic) ...

        当某个类的`__init__`方法被称为该特定类的第一次时，将调用此事件。在调用[`InstanceEvents.init()`](#sqlalchemy.orm.events.InstanceEvents.init "sqlalchemy.orm.events.InstanceEvents.init")事件之前，事件在`__init__`实际进行之前调用事件。

    `init`{.descname} （ *target*，*args*，*kwargs* ） [¶ T6\>](#sqlalchemy.orm.events.InstanceEvents.init "Permalink to this definition")
    :   当它的构造函数被调用时接收一个实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'init')
            def receive_init(target, args, kwargs):
                "listen for the 'init' event"

                # ... (event handling logic) ...

        该方法仅在对象的用户区构造期间结合对象的构造器（例如，它的`__init__`方法。从数据库加载对象时不调用它；请参阅[`InstanceEvents.load()`](#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")事件以拦截数据库负载。

        在调用该对象的实际`__init__`构造函数之前调用该事件。可以就地修改`kwargs`字典，以影响传递给`__init__`的内容。

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.init.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **args**[¶](#sqlalchemy.orm.events.InstanceEvents.init.params.args)
            – positional arguments passed to the `__init__` method. 这是作为一个元组传递的，目前是不可变的。
        -   **kwargs**[¶](#sqlalchemy.orm.events.InstanceEvents.init.params.kwargs)
            – keyword arguments passed to the `__init__` method. 这个结构*可以被修改。*

        也可以看看

        [`InstanceEvents.init_failure()`](#sqlalchemy.orm.events.InstanceEvents.init_failure "sqlalchemy.orm.events.InstanceEvents.init_failure")

        [`InstanceEvents.load()`](#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")

    `init_failure`{.descname} （ *target*，*args*，*kwargs* ） [¶ T6\>](#sqlalchemy.orm.events.InstanceEvents.init_failure "Permalink to this definition")
    :   当它的构造函数被调用时接收一个实例，并引发异常。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'init_failure')
            def receive_init_failure(target, args, kwargs):
                "listen for the 'init_failure' event"

                # ... (event handling logic) ...

        该方法仅在对象的用户区构造期间结合对象的构造器（例如，它的`__init__`方法。从数据库加载对象时不会调用它。

        事件在`__init__`方法引发的异常被捕获后调用。事件被调用后，原来的异常被重新向外提升，这样对象的构造仍然会引发异常。引发的实际异常和堆栈跟踪应存在于`sys.exc_info()`中。

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.init_failure.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **args**[¶](#sqlalchemy.orm.events.InstanceEvents.init_failure.params.args)
            – positional arguments that were passed to the
            `__init__` method.
        -   **kwargs**
            [¶](#sqlalchemy.orm.events.InstanceEvents.init_failure.params.kwargs)
            - 传递给`__init__`方法的关键字参数。

        也可以看看

        [`InstanceEvents.init()`](#sqlalchemy.orm.events.InstanceEvents.init "sqlalchemy.orm.events.InstanceEvents.init")

        [`InstanceEvents.load()`](#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")

     `load`{.descname}(*target*, *context*)[¶](#sqlalchemy.orm.events.InstanceEvents.load "Permalink to this definition")
    :   通过`__new__`创建对象实例后，并在初始属性填充发生后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'load')
            def receive_load(target, context):
                "listen for the 'load' event"

                # ... (event handling logic) ...

        这通常在基于传入结果行创建实例时发生，并且在该实例的生存期中仅调用一次。

        请注意，在结果行加载期间，在为此实例接收的第一行调用此方法。请注意，根据结果行中的内容，某些属性和集合可能被加载，甚至可能不被加载或甚至被初始化。

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.load.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **context**[¶](#sqlalchemy.orm.events.InstanceEvents.load.params.context)
            – the [`QueryContext`](internals.html#sqlalchemy.orm.query.QueryContext "sqlalchemy.orm.query.QueryContext")
            corresponding to the current [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
            in progress. 例如，在[`Session.merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")期间，如果加载不对应于[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")，则此参数可能为`None`。

        也可以看看

        [`InstanceEvents.init()`](#sqlalchemy.orm.events.InstanceEvents.init "sqlalchemy.orm.events.InstanceEvents.init")

        [`InstanceEvents.refresh()`](#sqlalchemy.orm.events.InstanceEvents.refresh "sqlalchemy.orm.events.InstanceEvents.refresh")

        [`SessionEvents.loaded_as_persistent()`](#sqlalchemy.orm.events.SessionEvents.loaded_as_persistent "sqlalchemy.orm.events.SessionEvents.loaded_as_persistent")

     `pickle`{.descname}(*target*, *state\_dict*)[¶](#sqlalchemy.orm.events.InstanceEvents.pickle "Permalink to this definition")
    :   在其关联状态正在进行酸洗时接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'pickle')
            def receive_pickle(target, state_dict):
                "listen for the 'pickle' event"

                # ... (event handling logic) ...

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.pickle.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **state\_dict**[¶](#sqlalchemy.orm.events.InstanceEvents.pickle.params.state_dict)
            – the dictionary returned by
            `InstanceState.__getstate__`, containing the state to be pickled.

     `refresh`{.descname}(*target*, *context*, *attrs*)[¶](#sqlalchemy.orm.events.InstanceEvents.refresh "Permalink to this definition")
    :   在查询中刷新了一个或多个属性后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'refresh')
            def receive_refresh(target, context, attrs):
                "listen for the 'refresh' event"

                # ... (event handling logic) ...

        将它与[`InstanceEvents.load()`](#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")方法进行对比，该方法在首次从查询加载对象时调用。

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.refresh.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **context**[¶](#sqlalchemy.orm.events.InstanceEvents.refresh.params.context)
            – the [`QueryContext`](internals.html#sqlalchemy.orm.query.QueryContext "sqlalchemy.orm.query.QueryContext")
            corresponding to the current [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
            in progress.
        -   **attrs**[¶](#sqlalchemy.orm.events.InstanceEvents.refresh.params.attrs)
            – sequence of attribute names which were populated, or None
            if all column-mapped, non-deferred attributes were
            populated.

        也可以看看

        [`InstanceEvents.load()`](#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")

    `refresh_flush  tt> （ target，flush_context，attrs ） ¶ T6>`{.descname}
    :   在对象的持久性内刷新一个或多个属性后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'refresh_flush')
            def receive_refresh_flush(target, flush_context, attrs):
                "listen for the 'refresh_flush' event"

                # ... (event handling logic) ...

        这个事件与[`InstanceEvents.refresh()`](#sqlalchemy.orm.events.InstanceEvents.refresh "sqlalchemy.orm.events.InstanceEvents.refresh")相同，除了它在工作单元flush过程中调用，并且这里的值通常来自处理INSERT或UPDATE的过程，例如通过RETURNING子句或从Python方面的默认值。

        版本1.0.5中的新功能

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.refresh_flush.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **flush\_context**[¶](#sqlalchemy.orm.events.InstanceEvents.refresh_flush.params.flush_context)
            – Internal [`UOWTransaction`](internals.html#sqlalchemy.orm.session.UOWTransaction "sqlalchemy.orm.session.UOWTransaction")
            object which handles the details of the flush.
        -   **attrs**[¶](#sqlalchemy.orm.events.InstanceEvents.refresh_flush.params.attrs)
            – sequence of attribute names which were populated.

    `unpickle`{.descname} （ *target*，*state\_dict* ） [¶](#sqlalchemy.orm.events.InstanceEvents.unpickle "Permalink to this definition")
    :   在其关联状态已取消之后接收对象实例。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeClass, 'unpickle')
            def receive_unpickle(target, state_dict):
                "listen for the 'unpickle' event"

                # ... (event handling logic) ...

        参数：

        -   **target**
            [¶](#sqlalchemy.orm.events.InstanceEvents.unpickle.params.target)
            - 映射的实例。如果事件配置为`raw=True`，则这将改为与该实例关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")状态管理对象。
        -   **state\_dict**[¶](#sqlalchemy.orm.events.InstanceEvents.unpickle.params.state_dict)
            – the dictionary sent to `InstanceState.__setstate__`, containing the state
            dictionary which was pickled.

会话事件[¶](#session-events "Permalink to this headline")
---------------------------------------------------------

*class* `sqlalchemy.orm.events。`{.descclassname} `SessionEvents`{.descname} [¶](#sqlalchemy.orm.events.SessionEvents "Permalink to this definition")
:   基础：[`sqlalchemy.event.base.Events`](core_events.html#sqlalchemy.event.base.Events "sqlalchemy.event.base.Events")

    定义特定于[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")生命周期的事件。

    例如。：

        from sqlalchemy import event
        from sqlalchemy.orm import sessionmaker

        def my_before_commit(session):
            print "before commit!"

        Session = sessionmaker()

        event.listen(Session, "before_commit", my_before_commit)

    [`listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")函数将接受[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象以及[`sessionmaker()`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")和[`scoped_session()`](contextual.html#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")

    此外，它还接受[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")类，它将侦听器全局应用于所有[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")实例。

    `after_attach`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.events.SessionEvents.after_attach "Permalink to this definition")
    :   在实例连接到会话后执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_attach')
            def receive_after_attach(session, instance):
                "listen for the 'after_attach' event"

                # ... (event handling logic) ...

        这是在添加，删除或合并之后调用的。

        注意

        从0.8开始，此事件在项目与会话完全关联之后触发*，这与以前的版本不同。*对于需要对象尚未成为会话状态一部分的事件处理程序（例如可能在目标对象尚未完成时自动刷新的处理程序），请考虑新的[`before_attach()`](#sqlalchemy.orm.events.SessionEvents.before_attach "sqlalchemy.orm.events.SessionEvents.before_attach")事件。

        也可以看看

        [`before_attach()`](#sqlalchemy.orm.events.SessionEvents.before_attach "sqlalchemy.orm.events.SessionEvents.before_attach")

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

     `after_begin`{.descname}(*session*, *transaction*, *connection*)[¶](#sqlalchemy.orm.events.SessionEvents.after_begin "Permalink to this definition")
    :   在连接开始事务后执行

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_begin')
            def receive_after_begin(session, transaction, connection):
                "listen for the 'after_begin' event"

                # ... (event handling logic) ...

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.after_begin.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **transaction**[¶](#sqlalchemy.orm.events.SessionEvents.after_begin.params.transaction)
            – The [`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction").
        -   **connection**[¶](#sqlalchemy.orm.events.SessionEvents.after_begin.params.connection)
            – The [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            object which will be used for SQL statements.

        也可以看看

        [`before_commit()`](#sqlalchemy.orm.events.SessionEvents.before_commit "sqlalchemy.orm.events.SessionEvents.before_commit")

        [`after_commit()`](#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit")

        [`after_transaction_create()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_create "sqlalchemy.orm.events.SessionEvents.after_transaction_create")

        [`after_transaction_end()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_end "sqlalchemy.orm.events.SessionEvents.after_transaction_end")

    ` after_bulk_delete  T0> （ T1>  delete_context  T2> ） T3> ¶ T4>`{.descname}
    :   对会话进行批量删除操作后执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style (arguments as of 0.9)
            @event.listens_for(SomeSessionOrFactory, 'after_bulk_delete')
            def receive_after_bulk_delete(delete_context):
                "listen for the 'after_bulk_delete' event"

                # ... (event handling logic) ...

            # legacy calling style (pre-0.9)
            @event.listens_for(SomeSessionOrFactory, 'after_bulk_delete')
            def receive_after_bulk_delete(session, query, query_context, result):
                "listen for the 'after_bulk_delete' event"

                # ... (event handling logic) ...

        版本0.9已更改： `after_bulk_delete`事件现在接受参数`delete_context`。接受上面列出的先前参数签名的听众函数将自动适应新签名。

        这被称为[`Query.delete()`](query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")方法的结果。

        参数：

        **delete\_context**
        [¶](#sqlalchemy.orm.events.SessionEvents.after_bulk_delete.params.delete_context)
        -

        一个“删除上下文”对象，其中包含有关更新的详细信息，包括这些属性：

        > -   `session` - 涉及[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        > -   `query` - [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象是否调用了此更新操作。
        > -   `context` [`QueryContext`](internals.html#sqlalchemy.orm.query.QueryContext "sqlalchemy.orm.query.QueryContext")对象，对应于调用ORM查询。
        > -   `result` the [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
        >     returned as a result of the bulk DELETE operation.

    ` after_bulk_update  T0> （ T1>  update_context  T2> ） T3> ¶ T4>`{.descname}
    :   在批量更新操作后执行会话。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style (arguments as of 0.9)
            @event.listens_for(SomeSessionOrFactory, 'after_bulk_update')
            def receive_after_bulk_update(update_context):
                "listen for the 'after_bulk_update' event"

                # ... (event handling logic) ...

            # legacy calling style (pre-0.9)
            @event.listens_for(SomeSessionOrFactory, 'after_bulk_update')
            def receive_after_bulk_update(session, query, query_context, result):
                "listen for the 'after_bulk_update' event"

                # ... (event handling logic) ...

        版本0.9已更改： `after_bulk_update`现在接受参数`update_context`。接受上面列出的先前参数签名的听众函数将自动适应新签名。

        这被称为[`Query.update()`](query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")方法的结果。

        参数：

        **update\_context**
        [¶](#sqlalchemy.orm.events.SessionEvents.after_bulk_update.params.update_context)
        -

        一个“更新上下文”对象，其中包含有关更新的详细信息，包括这些属性：

        > -   `session` - 涉及[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        > -   `query` - [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象是否调用了此更新操作。
        > -   `context` [`QueryContext`](internals.html#sqlalchemy.orm.query.QueryContext "sqlalchemy.orm.query.QueryContext")对象，对应于调用ORM查询。
        > -   `result`由于批量UPDATE操作返回的[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")。

    ` after_commit  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   在提交发生后执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_commit')
            def receive_after_commit(session):
                "listen for the 'after_commit' event"

                # ... (event handling logic) ...

        注意

        [`after_commit()`](#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit")钩子不是每次刷新的*，也就是说，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以将SQL发送到数据库多次交易。*要拦截这些事件，请使用[`before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")，[`after_flush()`](#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")或[`after_flush_postexec()`](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")事件。

        注意

        当调用[`after_commit()`](#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit")事件时，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")不处于活动事务中，因此无法发出SQL。要发出对应于每个事务的SQL，请使用[`before_commit()`](#sqlalchemy.orm.events.SessionEvents.before_commit "sqlalchemy.orm.events.SessionEvents.before_commit")事件。

        参数：

        tt\> **会话**
        [¶](#sqlalchemy.orm.events.SessionEvents.after_commit.params.session)
        - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

        也可以看看

        [`before_commit()`](#sqlalchemy.orm.events.SessionEvents.before_commit "sqlalchemy.orm.events.SessionEvents.before_commit")

        [`after_begin()`](#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin")

        [`after_transaction_create()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_create "sqlalchemy.orm.events.SessionEvents.after_transaction_create")

        [`after_transaction_end()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_end "sqlalchemy.orm.events.SessionEvents.after_transaction_end")

    `after_flush`{.descname} （ *session*，*flush\_context* ） [¶](#sqlalchemy.orm.events.SessionEvents.after_flush "Permalink to this definition")
    :   刷新完成后执行，但在调用提交之前执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_flush')
            def receive_after_flush(session, flush_context):
                "listen for the 'after_flush' event"

                # ... (event handling logic) ...

        请注意，会话的状态仍处于预先刷新状态，即“新建”，“脏”和“已删除”列表仍显示预刷新状态以及实例属性的历史记录设置。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.after_flush.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **flush\_context**[¶](#sqlalchemy.orm.events.SessionEvents.after_flush.params.flush_context)
            – Internal [`UOWTransaction`](internals.html#sqlalchemy.orm.session.UOWTransaction "sqlalchemy.orm.session.UOWTransaction")
            object which handles the details of the flush.

        也可以看看

        [`before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")

        [`after_flush_postexec()`](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")

        [Persistence
        Events](session_events.html#session-persistence-events)

    `after_flush_postexec`{.descname} （ *session*，*flush\_context* ） [](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "Permalink to this definition")
    :   刷新完成后以及执行后状态发生后执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_flush_postexec')
            def receive_after_flush_postexec(session, flush_context):
                "listen for the 'after_flush_postexec' event"

                # ... (event handling logic) ...

        这将是'新'，'脏'和'删除'列表处于最终状态的时候。实际提交()可能发生也可能没有发生，具体取决于flush是否开始自己的事务或参与更大的事务。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **flush\_context**[¶](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec.params.flush_context)
            – Internal [`UOWTransaction`](internals.html#sqlalchemy.orm.session.UOWTransaction "sqlalchemy.orm.session.UOWTransaction")
            object which handles the details of the flush.

        也可以看看

        [`before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")

        [`after_flush()`](#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")

        [Persistence
        Events](session_events.html#session-persistence-events)

    ` after_rollback  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   在发生真正的DBAPI回滚后执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_rollback')
            def receive_after_rollback(session):
                "listen for the 'after_rollback' event"

                # ... (event handling logic) ...

        请注意，只有当针对数据库的*实际*回滚发生时才会触发此事件 -
        每次[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法触发时，都会触发*而不是*如果底层的DBAPI事务已经被回滚，则称为“在很多情况下，由于当前事务无效，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")在此事件期间不会处于“活动”状态。要获取在最后一个回滚进行之后处于活动状态的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，请使用[`SessionEvents.after_soft_rollback()`](#sqlalchemy.orm.events.SessionEvents.after_soft_rollback "sqlalchemy.orm.events.SessionEvents.after_soft_rollback")事件，检查[`Session.is_active`](session_api.html#sqlalchemy.orm.session.Session.is_active "sqlalchemy.orm.session.Session.is_active")标志。

        参数：

        tt\> **会话**
        [¶](#sqlalchemy.orm.events.SessionEvents.after_rollback.params.session)
        - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

     `after_soft_rollback`{.descname}(*session*, *previous\_transaction*)[¶](#sqlalchemy.orm.events.SessionEvents.after_soft_rollback "Permalink to this definition")
    :   在发生任何回滚之后执行，包括实际上不会在DBAPI级别发出的“软”回滚。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_soft_rollback')
            def receive_after_soft_rollback(session, previous_transaction):
                "listen for the 'after_soft_rollback' event"

                # ... (event handling logic) ...

        这对应于嵌套和外部回滚，即调用DBAPI的rollback()方法的最内部回滚，以及只从事务堆栈中自行弹出的封闭回滚调用。

        通过首先检查[`Session.is_active`](session_api.html#sqlalchemy.orm.session.Session.is_active "sqlalchemy.orm.session.Session.is_active")标志，给定的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可用于在最外侧回滚之后调用SQL和[`Session.query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")

            @event.listens_for(Session, "after_soft_rollback")
            def do_something(session, previous_transaction):
                if session.is_active:
                    session.execute("select * from some_table")

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.after_soft_rollback.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **previous\_transaction**[¶](#sqlalchemy.orm.events.SessionEvents.after_soft_rollback.params.previous_transaction)
            – The [`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")
            transactional marker object which was just closed.
            给定[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的当前[`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")可以通过[`Session.transaction`](session_api.html#sqlalchemy.orm.session.Session.transaction "sqlalchemy.orm.session.Session.transaction")属性获得。

        New in version 0.7.3.

    `after_transaction_create`{.descname} （ *session*，*transaction* ） [¶](#sqlalchemy.orm.events.SessionEvents.after_transaction_create "Permalink to this definition")
    :   当创建新的[`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")时执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_transaction_create')
            def receive_after_transaction_create(session, transaction):
                "listen for the 'after_transaction_create' event"

                # ... (event handling logic) ...

        这个事件与[`after_begin()`](#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin")不同，它发生在每个[`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")整体上，而不是在单个数据库连接上开始事务。它也被嵌套事务和子事务调用，并且总是与相应的[`after_transaction_end()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_end "sqlalchemy.orm.events.SessionEvents.after_transaction_end")事件匹配（假设[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")正常运行）。

        参数：

        -   **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.after_transaction_create.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **transaction**[¶](#sqlalchemy.orm.events.SessionEvents.after_transaction_create.params.transaction)
            – the target [`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction").

        0.8版本中的新功能

        也可以看看

        [`after_transaction_end()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_end "sqlalchemy.orm.events.SessionEvents.after_transaction_end")

    `after_transaction_end`{.descname} （ *session*，*transaction* ） [¶](#sqlalchemy.orm.events.SessionEvents.after_transaction_end "Permalink to this definition")
    :   当[`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")的跨度结束时执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'after_transaction_end')
            def receive_after_transaction_end(session, transaction):
                "listen for the 'after_transaction_end' event"

                # ... (event handling logic) ...

        这个事件与[`after_commit()`](#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit")的不同之处在于它对应于所有正在使用的[`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")对象，包括嵌套事务和子事务的对象，并且总是与相应的[`after_transaction_create()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_create "sqlalchemy.orm.events.SessionEvents.after_transaction_create")事件。

        参数：

        -   **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.after_transaction_end.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **transaction**[¶](#sqlalchemy.orm.events.SessionEvents.after_transaction_end.params.transaction)
            – the target [`SessionTransaction`](session_api.html#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction").

        0.8版本中的新功能

        也可以看看

        [`after_transaction_create()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_create "sqlalchemy.orm.events.SessionEvents.after_transaction_create")

    `before_attach`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.events.SessionEvents.before_attach "Permalink to this definition")
    :   在实例连接到会话之前执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'before_attach')
            def receive_before_attach(session, instance):
                "listen for the 'before_attach' event"

                # ... (event handling logic) ...

        这在添加，删除或合并之前调用会导致对象成为会话的一部分。

        New in version 0.8.: Note that [`after_attach()`](#sqlalchemy.orm.events.SessionEvents.after_attach "sqlalchemy.orm.events.SessionEvents.after_attach")
        now fires off after the item is part of the session.
        [`before_attach()`](#sqlalchemy.orm.events.SessionEvents.before_attach "sqlalchemy.orm.events.SessionEvents.before_attach")
        is provided for those cases where the item should not yet be
        part of the session state.

        也可以看看

        [`after_attach()`](#sqlalchemy.orm.events.SessionEvents.after_attach "sqlalchemy.orm.events.SessionEvents.after_attach")

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    ` before_commit  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   在调用提交之前执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'before_commit')
            def receive_before_commit(session):
                "listen for the 'before_commit' event"

                # ... (event handling logic) ...

        注意

        [`before_commit()`](#sqlalchemy.orm.events.SessionEvents.before_commit "sqlalchemy.orm.events.SessionEvents.before_commit")钩子是*不是*每次刷新，也就是说，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以将SQL发送到数据库多次交易。要拦截这些事件，请使用[`before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")，[`after_flush()`](#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")或[`after_flush_postexec()`](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")事件。

        参数：

        tt\> **会话**
        [¶](#sqlalchemy.orm.events.SessionEvents.before_commit.params.session)
        - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

        也可以看看

        [`after_commit()`](#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit")

        [`after_begin()`](#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin")

        [`after_transaction_create()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_create "sqlalchemy.orm.events.SessionEvents.after_transaction_create")

        [`after_transaction_end()`](#sqlalchemy.orm.events.SessionEvents.after_transaction_end "sqlalchemy.orm.events.SessionEvents.after_transaction_end")

    ` before_flush  T0> （ T1> 会话 T2>， flush_context  T3>，实例 T4> ） T5> ¶ T6>`{.descname}
    :   在刷新过程开始之前执行。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'before_flush')
            def receive_before_flush(session, flush_context, instances):
                "listen for the 'before_flush' event"

                # ... (event handling logic) ...

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.before_flush.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **flush\_context**[¶](#sqlalchemy.orm.events.SessionEvents.before_flush.params.flush_context)
            – Internal [`UOWTransaction`](internals.html#sqlalchemy.orm.session.UOWTransaction "sqlalchemy.orm.session.UOWTransaction")
            object which handles the details of the flush.
        -   **instances**[¶](#sqlalchemy.orm.events.SessionEvents.before_flush.params.instances)
            – Usually `None`, this is the collection
            of objects which can be passed to the
            [`Session.flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")
            method (note this usage is deprecated).

        也可以看看

        [`after_flush()`](#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")

        [`after_flush_postexec()`](#sqlalchemy.orm.events.SessionEvents.after_flush_postexec "sqlalchemy.orm.events.SessionEvents.after_flush_postexec")

        [Persistence
        Events](session_events.html#session-persistence-events)

    `deleted_to_detached`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.events.SessionEvents.deleted_to_detached "Permalink to this definition")
    :   截取特定对象的“已删除到已分离”过渡。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'deleted_to_detached')
            def receive_deleted_to_detached(session, instance):
                "listen for the 'deleted_to_detached' event"

                # ... (event handling logic) ...

        当从会话中删除已删除的对象时，将调用此事件。发生这种情况的典型情况是，当对象被删除的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的事务被提交时；该对象从删除状态移至分离状态。

        当调用[`Session.expunge_all()`](session_api.html#sqlalchemy.orm.session.Session.expunge_all "sqlalchemy.orm.session.Session.expunge_all")或[`Session.close()`](session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")事件时，也会调用在flush中被删除的对象，以及对象是通过[`Session.expunge()`](session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")单独从删除状态中删除。

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `deleted_to_persistent`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.events.SessionEvents.deleted_to_persistent "Permalink to this definition")
    :   截取特定对象的“已删除到永久”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'deleted_to_persistent')
            def receive_deleted_to_persistent(session, instance):
                "listen for the 'deleted_to_persistent' event"

                # ... (event handling logic) ...

        只有当由于调用[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")而在刷新中成功删除的对象被恢复时，才会发生此转换。在任何其他情况下不会调用该事件。

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `detached_to_persistent`{.descname} （ *会话*，*实例* ） [](#sqlalchemy.orm.events.SessionEvents.detached_to_persistent "Permalink to this definition")
    :   截取特定对象的“分离到持续”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'detached_to_persistent')
            def receive_detached_to_persistent(session, instance):
                "listen for the 'detached_to_persistent' event"

                # ... (event handling logic) ...

        这个事件是[`SessionEvents.after_attach()`](#sqlalchemy.orm.events.SessionEvents.after_attach "sqlalchemy.orm.events.SessionEvents.after_attach")事件的一个特例，它只为这个特定的转换调用。它通常在[`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")调用期间以及在[`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")调用期间调用，前提是对象之前未与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")（请注意，标记为“已删除”的对象将保持“持久”状态，直到刷新结束）。

        注意

        如果该对象作为对[`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")的调用的一部分而持久化，则在调用此事件时，该对象**不是**，但标记为已删除。To
        detect deleted objects, check the `deleted`
        flag sent to the [`SessionEvents.persistent_to_detached()`](#sqlalchemy.orm.events.SessionEvents.persistent_to_detached "sqlalchemy.orm.events.SessionEvents.persistent_to_detached")
        to event after the flush proceeds, or check the
        [`Session.deleted`](session_api.html#sqlalchemy.orm.session.Session.deleted "sqlalchemy.orm.session.Session.deleted")
        collection within the [`SessionEvents.before_flush()`](#sqlalchemy.orm.events.SessionEvents.before_flush "sqlalchemy.orm.events.SessionEvents.before_flush")
        event if deleted objects need to be intercepted before the
        flush.

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.detached_to_persistent.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.detached_to_persistent.params.instance)
            – the ORM-mapped instance being operated upon.

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `loaded_as_persistent`{.descname} （ *会话*，*实例* ） [](#sqlalchemy.orm.events.SessionEvents.loaded_as_persistent "Permalink to this definition")
    :   拦截特定对象的“加载作为永久”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'loaded_as_persistent')
            def receive_loaded_as_persistent(session, instance):
                "listen for the 'loaded_as_persistent' event"

                # ... (event handling logic) ...

        该事件在ORM加载过程中被调用，并且与[`InstanceEvents.load()`](#sqlalchemy.orm.events.InstanceEvents.load "sqlalchemy.orm.events.InstanceEvents.load")事件非常类似地被调用。但是，此处的事件可以链接到[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")类或实例，而不是映射器或类层次结构，并且可以顺利地与其他会话生命周期事件集成。当该事件被调用时，该对象保证出现在会话的身份映射中。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.loaded_as_persistent.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.loaded_as_persistent.params.instance)
            – the ORM-mapped instance being operated upon.

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `pending_to_persistent`{.descname} （ *会话*，*实例* ） [¶](#sqlalchemy.orm.events.SessionEvents.pending_to_persistent "Permalink to this definition")
    :   截取特定对象的“挂起到持续”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'pending_to_persistent')
            def receive_pending_to_persistent(session, instance):
                "listen for the 'pending_to_persistent' event"

                # ... (event handling logic) ...

        该事件在刷新过程中被调用，类似于在[`SessionEvents.after_flush()`](#sqlalchemy.orm.events.SessionEvents.after_flush "sqlalchemy.orm.events.SessionEvents.after_flush")事件中扫描[`Session.new`](session_api.html#sqlalchemy.orm.session.Session.new "sqlalchemy.orm.session.Session.new")集合。但是，在这种情况下，当事件被调用时，对象已经移至持久状态。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.pending_to_persistent.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.pending_to_persistent.params.instance)
            – the ORM-mapped instance being operated upon.

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `pending_to_transient`{.descname} （ *会话*，*实例* ） [](#sqlalchemy.orm.events.SessionEvents.pending_to_transient "Permalink to this definition")
    :   截取特定对象的“等待到瞬态”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'pending_to_transient')
            def receive_pending_to_transient(session, instance):
                "listen for the 'pending_to_transient' event"

                # ... (event handling logic) ...

        当没有被刷新的待处理对象被从会话中逐出时，发生这种不太常见的转换；当[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法回退事务或使用[`Session.expunge()`](session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")方法时，会发生这种情况。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.pending_to_transient.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.pending_to_transient.params.instance)
            – the ORM-mapped instance being operated upon.

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `persistent_to_deleted`{.descname} （ *session*，*instance* ） [](#sqlalchemy.orm.events.SessionEvents.persistent_to_deleted "Permalink to this definition")
    :   截取特定对象的“永久删除”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'persistent_to_deleted')
            def receive_persistent_to_deleted(session, instance):
                "listen for the 'persistent_to_deleted' event"

                # ... (event handling logic) ...

        当一个持久化对象的标识从flush中的数据库中被删除时，该事件被调用，但是该对象在事务完成之前仍然与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联。

        如果事务回滚，则对象再次移至持久状态，并调用[`SessionEvents.deleted_to_persistent()`](#sqlalchemy.orm.events.SessionEvents.deleted_to_persistent "sqlalchemy.orm.events.SessionEvents.deleted_to_persistent")事件。如果事务已提交，则该对象将分离，这将发出[`SessionEvents.deleted_to_detached()`](#sqlalchemy.orm.events.SessionEvents.deleted_to_detached "sqlalchemy.orm.events.SessionEvents.deleted_to_detached")事件。

        请注意，虽然[`Session.delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")方法是将对象标记为已删除的主要公共接口，但由于级联规则而导致许多对象被删除，直到刷新时间才会确定该对象。因此，在清除进行之前，没有办法捕获每个将被删除的对象。因此，[`SessionEvents.persistent_to_deleted()`](#sqlalchemy.orm.events.SessionEvents.persistent_to_deleted "sqlalchemy.orm.events.SessionEvents.persistent_to_deleted")事件在刷新结束时被调用。

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `persistent_to_detached`{.descname} （ *会话*，*实例* ） [¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_detached "Permalink to this definition")
    :   截取特定对象的“持续到分离”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'persistent_to_detached')
            def receive_persistent_to_detached(session, instance):
                "listen for the 'persistent_to_detached' event"

                # ... (event handling logic) ...

        当持久对象从会话中被驱逐时，会调用此事件。导致这种情况发生的条件很多，包括：

        -   使用诸如[`Session.expunge()`](session_api.html#sqlalchemy.orm.session.Session.expunge "sqlalchemy.orm.session.Session.expunge")或[`Session.close()`](session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")等方法
        -   当对象是该会话事务的INSERT语句的一部分时，调用[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_detached.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_detached.params.instance)
            – the ORM-mapped instance being operated upon.
        -   **已删除**
            [¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_detached.params.deleted)
            -
            布尔值。如果为True，则表示此对象已移至分离状态，因为它已标记为已删除并已刷新。

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `persistent_to_transient`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_transient "Permalink to this definition")
    :   截取特定对象的“持久到瞬态”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'persistent_to_transient')
            def receive_persistent_to_transient(session, instance):
                "listen for the 'persistent_to_transient' event"

                # ... (event handling logic) ...

        当已经刷新的待处理对象被从会话中逐出时，发生这种不太常见的转换；当[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法回退事务时可能发生这种情况。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_transient.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.persistent_to_transient.params.instance)
            – the ORM-mapped instance being operated upon.

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

    `transient_to_pending`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.events.SessionEvents.transient_to_pending "Permalink to this definition")
    :   截取特定对象的“暂态到暂挂”转换。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeSessionOrFactory, 'transient_to_pending')
            def receive_transient_to_pending(session, instance):
                "listen for the 'transient_to_pending' event"

                # ... (event handling logic) ...

        这个事件是[`SessionEvents.after_attach()`](#sqlalchemy.orm.events.SessionEvents.after_attach "sqlalchemy.orm.events.SessionEvents.after_attach")事件的一个特例，它只为这个特定的转换调用。它通常在[`Session.add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")调用期间调用。

        参数：

        -   tt\> **会话**
            [¶](#sqlalchemy.orm.events.SessionEvents.transient_to_pending.params.session)
            - 目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        -   **instance**[¶](#sqlalchemy.orm.events.SessionEvents.transient_to_pending.params.instance)
            – the ORM-mapped instance being operated upon.

        版本1.1中的新功能

        也可以看看

        [Object Lifecycle
        Events](session_events.html#session-lifecycle-events)

查询事件[¶](#query-events "Permalink to this headline")
-------------------------------------------------------

*class* `sqlalchemy.orm.events。`{.descclassname} `QueryEvents`{.descname} [¶](#sqlalchemy.orm.events.QueryEvents "Permalink to this definition")
:   基础：[`sqlalchemy.event.base.Events`](core_events.html#sqlalchemy.event.base.Events "sqlalchemy.event.base.Events")

    表示构建[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象内的事件。

    此处的事件旨在用于[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")的尚未发布的检查系统。现在可以进行一些非常基本的操作，但检查系统旨在使复杂的查询操作自动化。

    版本1.0.0中的新功能

    ` before_compile  T0> （ T1> 查询 T2> ） T3> ¶ T4>`{.descname}
    :   在将[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象组成核心[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象之前接收该对象。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeQuery, 'before_compile')
            def receive_before_compile(query):
                "listen for the 'before_compile' event"

                # ... (event handling logic) ...

        此事件旨在允许更改给出的查询：

            @event.listens_for(Query, "before_compile", retval=True)
            def no_deleted(query):
                for desc in query.column_descriptions:
                    if desc['type'] is User:
                        entity = desc['entity']
                        query = query.filter(entity.deleted == False)
                return query

        通常应该使用`retval=True`参数集来监听事件，以便可以返回修改后的查询。

仪器事件[¶](#module-sqlalchemy.orm.instrumentation "Permalink to this headline")
--------------------------------------------------------------------------------

定义SQLAlchemy的类检测系统。

该模块通常对用户应用程序不直接可见，但定义了ORM交互性的很大一部分。

instrumentation.py处理最终用户类的状态跟踪注册。它与分别建立per-instance和per-class-attribute工具的state.py和attributes.py紧密交互。

类工具系统可以使用[`sqlalchemy.ext.instrumentation`](extensions_instrumentation.html#module-sqlalchemy.ext.instrumentation "sqlalchemy.ext.instrumentation")模块在每个类或全局基础上定制，该模块提供了构建和指定替代工具形式的方法。

*class* `sqlalchemy.orm.events。`{.descclassname} `InstrumentationEvents`{.descname} [¶](#sqlalchemy.orm.events.InstrumentationEvents "Permalink to this definition")
:   基础：[`sqlalchemy.event.base.Events`](core_events.html#sqlalchemy.event.base.Events "sqlalchemy.event.base.Events")

    与类仪器事件相关的事件。

    这里的监听器支持针对任何新的样式类建立对象，即任何属于“类型”的子类的对象。然后，事件将被针对该类别的事件解雇。如果“propagate
    = True”标志被传递给event.listen()，那么该事件也将触发该类的子类。

    Python `type`内置函数也被接受为目标，它在使用时具有为所有类发出事件的效果。

    请注意，此处的“传播”标志默认为`True`，与默认为`False`的其他类级别事件不同。这意味着当一个监听器建立在超类上时，新的子类也将成为这些事件的主题。

    在版本0.8中更改： -
    这里的事件将根据传入类与传递给[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")的类的类型进行比较来发出。以前，尽管文件中有相反的规定，但事件将无条件地为任何班级开火，无论哪个班级被发送聆听。

     `attribute_instrument`{.descname}(*cls*, *key*, *inst*)[¶](#sqlalchemy.orm.events.InstrumentationEvents.attribute_instrument "Permalink to this definition")
    :   示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeBaseClass, 'attribute_instrument')
            def receive_attribute_instrument(cls, key, inst):
                "listen for the 'attribute_instrument' event"

                # ... (event handling logic) ...

        在检测属性时调用。

    ` class_instrument  T0> （ T1>  CLS  T2> ） T3> ¶ T4>`{.descname}
    :   在给定的课程安装后调用。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeBaseClass, 'class_instrument')
            def receive_class_instrument(cls):
                "listen for the 'class_instrument' event"

                # ... (event handling logic) ...

        要获取[`ClassManager`](internals.html#sqlalchemy.orm.instrumentation.ClassManager "sqlalchemy.orm.instrumentation.ClassManager")，请使用`manager_of_class()`。

    ` class_uninstrument  T0> （ T1>  CLS  T2> ） T3> ¶ T4>`{.descname}
    :   在给定的班级未被打开之前调用。

        示例参数表单：

            from sqlalchemy import event

            # standard decorator style
            @event.listens_for(SomeBaseClass, 'class_uninstrument')
            def receive_class_uninstrument(cls):
                "listen for the 'class_uninstrument' event"

                # ... (event handling logic) ...

        要获取[`ClassManager`](internals.html#sqlalchemy.orm.instrumentation.ClassManager "sqlalchemy.orm.instrumentation.ClassManager")，请使用`manager_of_class()`。


