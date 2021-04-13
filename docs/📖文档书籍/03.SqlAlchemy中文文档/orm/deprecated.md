---
title: 不推荐使用的 ORM 事件接口
date: 2021-02-20 22:41:40
permalink: /sqlalchemy/orm/deprecated/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
不推荐使用的 ORM 事件接口[¶](#module-sqlalchemy.orm.interfaces "Permalink to this headline")
==========================================================================================

本节描述了最初存在于 SQLAlchemy
0.1 中的基于类的 ORM 事件接口，该接口在 SQLAlchemy
0.5 之前有更多类型的事件。非 ORM 模拟在[Deprecated Event
Interfaces](core_interfaces.html)中描述。

从版本 0.7 开始弃用：从 SQLAlchemy
0.7 开始，[Events](core_event.html)中描述的新事件系统取代了扩展/代理/侦听器系统，为所有不需要的事件提供一致的接口用于子类化。

Mapper 事件[¶](#mapper-events "Permalink to this headline")
----------------------------------------------------------

*class* `sqlalchemy.orm.interfaces。`{.descclassname} `MapperExtension`{.descname} [¶](#sqlalchemy.orm.interfaces.MapperExtension "Permalink to this definition")
:   [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")事件挂钩的基本实现。

    注意plainplainplainplainplainplainplainplain

    [`MapperExtension`](#sqlalchemy.orm.interfaces.MapperExtension "sqlalchemy.orm.interfaces.MapperExtension")已弃用。请参阅[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")以及[`MapperEvents`](events.html#sqlalchemy.orm.events.MapperEvents "sqlalchemy.orm.events.MapperEvents")。

    新的扩展类是[`MapperExtension`](#sqlalchemy.orm.interfaces.MapperExtension "sqlalchemy.orm.interfaces.MapperExtension")的子类，它是使用`extension` mapper()参数指定的，该参数是一个[`MapperExtension`](#sqlalchemy.orm.interfaces.MapperExtension "sqlalchemy.orm.interfaces.MapperExtension")

        from sqlalchemy.orm.interfaces import MapperExtension

        class MyExtension(MapperExtension):
            def before_insert(self, mapper, connection, instance):
                print "instance %s before insert !" % instance

        m = mapper(User, users_table, extension=MyExtension())

    一个映射器可以维护`MapperExtension`对象链。当发生特定的映射事件时，每个`MapperExtension`上的相应方法被串行调用，并且每种方法都有能力阻止链进一步处理：

        m = mapper(User, users_table, extension=[ext1, ext2, ext3])

    每个`MapperExtension`方法默认返回符号EXT\_CONTINUE。这个符号通常意味着“移动到下一个`MapperExtension`进行处理”。对于返回像翻译行或新对象实例这样的对象的方法，EXT\_CONTINUE表示方法的结果应该被忽略。在某些情况下，需要执行默认的映射器活动，例如将新实例添加到结果列表中。

    符号EXT\_STOP在`MapperExtension`对象链中具有重要意义，即返回此符号时链将被停止。与EXT\_CONTINUE类似，在某些情况下，默认的映射器活动将不会执行，这也有其他重要意义。

    `after_delete`{.descname} （ *mapper*，*connection*，*instance* ） [¶ T6\>](#sqlalchemy.orm.interfaces.MapperExtension.after_delete "Permalink to this definition")
    :   在该实例被删除后接收对象实例。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

     `after_insert`{.descname}(*mapper*, *connection*, *instance*)[¶](#sqlalchemy.orm.interfaces.MapperExtension.after_insert "Permalink to this definition")
    :   在插入实例后接收对象实例。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

    `after_update`{.descname} （ *mapper*，*连接*，*实例* ） [¶ T6\>](#sqlalchemy.orm.interfaces.MapperExtension.after_update "Permalink to this definition")
    :   在实例更新后接收对象实例。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

     `before_delete`{.descname}(*mapper*, *connection*, *instance*)[¶](#sqlalchemy.orm.interfaces.MapperExtension.before_delete "Permalink to this definition")
    :   在该实例被删除之前接收一个对象实例。

        请注意，可以在此处设置*no*更改整体刷新计划；并且对`Session`的操纵不会产生预期的效果。要操作扩展中的`Session`，请使用`SessionExtension`。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

    `before_insert`{.descname} （ *mapper*，*连接*，*实例* ） [¶ T6\>](#sqlalchemy.orm.interfaces.MapperExtension.before_insert "Permalink to this definition")
    :   在该实例插入其表中之前接收一个对象实例。

        这是设置主键值以及不以其他方式处理的好地方。

        可以在此方法内修改基于列的属性，这将导致插入新值。However *no*
        changes to the overall flush plan can be made, and manipulation
        of the `Session` will not have the desired
        effect. 要操作扩展中的`Session`，请使用`SessionExtension`。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

    `before_update`{.descname} （ *mapper*，*connection*，*instance* ） [¶ T6\>](#sqlalchemy.orm.interfaces.MapperExtension.before_update "Permalink to this definition")
    :   在实例更新之前接收对象实例。

        请注意，为所有标记为“脏”的实例调用此方法，即使这些实例没有对其基于列的属性进行净更改。当一个对象的任何基于列的属性有一个被调用的“set
        attribute”操作或当它的任何集合被修改时，这个对象被标记为脏。如果在更新时没有基于列的属性有任何净更改，则不会发布UPDATE语句。这意味着发送到before\_update的实例*不是*保证会发出UPDATE语句（尽管您可以在此处影响结果）。

        要检测对象上的基于列的属性是否具有净更改，并因此会生成UPDATE语句，请使用`object_session（instance）.is_modified（instance， include_collections = False）  T2>  T0>。`

        可以在此方法中修改基于列的属性，这将导致更新新值。However *no*
        changes to the overall flush plan can be made, and manipulation
        of the `Session` will not have the desired
        effect. 要操作扩展中的`Session`，请使用`SessionExtension`。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

    `init_failed`{.descname} （ *mapper*，*class \_*，*oldinit*，*实例 t5 \>，*args*，*kwargs* ） [¶](#sqlalchemy.orm.interfaces.MapperExtension.init_failed "Permalink to this definition")*
    :   当它的构造函数被调用时接收一个实例，并引发异常。

        该方法仅在对象的用户区构造期间被调用。从数据库加载对象时不会调用它。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

     `init_instance`{.descname}(*mapper*, *class\_*, *oldinit*, *instance*, *args*, *kwargs*)[¶](#sqlalchemy.orm.interfaces.MapperExtension.init_instance "Permalink to this definition")
    :   当它的构造函数被调用时接收一个实例。

        该方法仅在对象的用户区构造期间被调用。从数据库加载对象时不会调用它。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

     `instrument_class`{.descname}(*mapper*, *class\_*)[¶](#sqlalchemy.orm.interfaces.MapperExtension.instrument_class "Permalink to this definition")
    :   首次构建映射器时接收类，并将映射应用到映射类。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

     `reconstruct_instance`{.descname}(*mapper*, *instance*)[¶](#sqlalchemy.orm.interfaces.MapperExtension.reconstruct_instance "Permalink to this definition")
    :   通过`__new__`创建对象实例后，并在初始属性填充发生后接收对象实例。

        这通常在基于传入结果行创建实例时发生，并且在该实例的生存期中仅调用一次。

        请注意，在结果行加载期间，在为此实例接收的第一行调用此方法。请注意，根据结果行中的内容，某些属性和集合可能被加载，甚至可能不被加载或甚至被初始化。

        返回值仅在`MapperExtension`链中有效；父映射器的行为不会被此方法修改。

会话事件[¶](#session-events "Permalink to this headline")
---------------------------------------------------------

*class* `sqlalchemy.orm.interfaces。`{.descclassname} `SessionExtension`{.descname} [¶](#sqlalchemy.orm.interfaces.SessionExtension "Permalink to this definition")
:   [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")事件挂钩的基本实现。

    注意plainplainplainplainplainplainplainplainplainplainplain

    [`SessionExtension`](#sqlalchemy.orm.interfaces.SessionExtension "sqlalchemy.orm.interfaces.SessionExtension")
    is deprecated. 请参阅[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")以及[`SessionEvents`](events.html#sqlalchemy.orm.events.SessionEvents "sqlalchemy.orm.events.SessionEvents")。

    可以使用`extension`关键字参数将子类安装到[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")（或[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")）中：

        from sqlalchemy.orm.interfaces import SessionExtension

        class MySessionExtension(SessionExtension):
            def before_commit(self, session):
                print "before commit!"

        Session = sessionmaker(extension=MySessionExtension())

    同一个[`SessionExtension`](#sqlalchemy.orm.interfaces.SessionExtension "sqlalchemy.orm.interfaces.SessionExtension")实例可以用于任意数量的会话。

    `after_attach`{.descname} （ *session*，*instance* ） [¶](#sqlalchemy.orm.interfaces.SessionExtension.after_attach "Permalink to this definition")
    :   在实例连接到会话后执行。

        这是在添加，删除或合并之后调用的。

     `after_begin`{.descname}(*session*, *transaction*, *connection*)[¶](#sqlalchemy.orm.interfaces.SessionExtension.after_begin "Permalink to this definition")
    :   在连接开始事务后执行

        transaction is the SessionTransaction.
        在连接上启动引擎级事务之后调用此方法。

    `after_bulk_delete`{.descname} （ *会话*，*查询*，*query\_context*，*结果 t5 \> ） T6\> [¶ T7\>](#sqlalchemy.orm.interfaces.SessionExtension.after_bulk_delete "Permalink to this definition")*
    :   对会话进行批量删除操作后执行。

        这是在session.query（...）。delete()之后调用的。

        query是调用此删除操作的查询对象。query\_context was the query
        context object. 结果是批量操作返回的结果对象。

    `after_bulk_update`{.descname} （ *会话*，*查询*，*query\_context*，*结果 t5 \> ） T6\> [¶ T7\>](#sqlalchemy.orm.interfaces.SessionExtension.after_bulk_update "Permalink to this definition")*
    :   在批量更新操作后执行会话。

        这是在session.query（...）。update()之后调用的。

        query是调用此更新操作的查询对象。query\_context was the query
        context object. 结果是批量操作返回的结果对象。

    ` after_commit  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   在提交发生后执行。

        请注意，如果长时间运行的事务正在进行，这可能不是每次刷新。

    `after_flush`{.descname} （ *session*，*flush\_context* ） [¶](#sqlalchemy.orm.interfaces.SessionExtension.after_flush "Permalink to this definition")
    :   刷新完成后执行，但在调用提交之前执行。

        请注意，会话的状态仍处于预先刷新状态，即“新建”，“脏”和“已删除”列表仍显示预刷新状态以及实例属性的历史记录设置。

    `after_flush_postexec`{.descname} （ *session*，*flush\_context* ） [](#sqlalchemy.orm.interfaces.SessionExtension.after_flush_postexec "Permalink to this definition")
    :   刷新完成后以及执行后状态发生后执行。

        这将是'新'，'脏'和'删除'列表处于最终状态的时候。实际提交()可能发生也可能没有发生，具体取决于flush是否开始自己的事务或参与更大的事务。

    ` after_rollback  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   发生回滚后执行。

        请注意，如果长时间运行的事务正在进行，这可能不是每次刷新。

    ` before_commit  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   在调用commit之前执行。

        请注意，如果长时间运行的事务正在进行，这可能不是每次刷新。

    ` before_flush  T0> （ T1> 会话 T2>， flush_context  T3>，实例 T4> ） T5> ¶ T6>`{.descname}
    :   在刷新过程开始之前执行。

        实例是传递给`flush()`方法的对象的可选列表。

属性事件[¶](#attribute-events "Permalink to this headline")
-----------------------------------------------------------

*class* `sqlalchemy.orm.interfaces。`{.descclassname} `AttributeExtension`{.descname} [¶](#sqlalchemy.orm.interfaces.AttributeExtension "Permalink to this definition")
:   `AttributeImpl`事件挂钩的基本实现，这是在用户代码中引发属性突变时触发的事件。

    注意plainplainplainplainplainplain

    [`AttributeExtension`](#sqlalchemy.orm.interfaces.AttributeExtension "sqlalchemy.orm.interfaces.AttributeExtension")已弃用。请参阅[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")以及[`AttributeEvents`](events.html#sqlalchemy.orm.events.AttributeEvents "sqlalchemy.orm.events.AttributeEvents")。

    [`AttributeExtension`](#sqlalchemy.orm.interfaces.AttributeExtension "sqlalchemy.orm.interfaces.AttributeExtension")用于侦听设置，删除和追加单个映射属性上的事件。它使用[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")，[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")和其他的扩展参数在单独的映射属性上建立：

        from sqlalchemy.orm.interfaces import AttributeExtension
        from sqlalchemy.orm import mapper, relationship, column_property

        class MyAttrExt(AttributeExtension):
            def append(self, state, value, initiator):
                print "append event !"
                return value

            def set(self, state, value, oldvalue, initiator):
                print "set event !"
                return value

        mapper(SomeClass, sometable, properties={
            'foo':column_property(sometable.c.foo, extension=MyAttrExt()),
            'bar':relationship(Bar, extension=MyAttrExt())
        })

    请注意，[`AttributeExtension`](#sqlalchemy.orm.interfaces.AttributeExtension "sqlalchemy.orm.interfaces.AttributeExtension")方法[`append()`](#sqlalchemy.orm.interfaces.AttributeExtension.append "sqlalchemy.orm.interfaces.AttributeExtension.append")和[`set()`](#sqlalchemy.orm.interfaces.AttributeExtension.set "sqlalchemy.orm.interfaces.AttributeExtension.set")需要返回`value`参数。返回值用作有效值，并允许扩展改变最终持续的内容。

    AttributeExtension在与映射类关联的描述符中组装。

    `active_history`{.descname} *= True* [¶](#sqlalchemy.orm.interfaces.AttributeExtension.active_history "Permalink to this definition")
    :   表明set()方法想要接收'旧'值，即使它意味着释放懒惰的可调参数。

        请注意，`active_history`也可以直接通过[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")和[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")设置。

     `append`{.descname}(*state*, *value*, *initiator*)[¶](#sqlalchemy.orm.interfaces.AttributeExtension.append "Permalink to this definition")
    :   收到追加追加事件。

        返回值将被用作要追加的实际值。

    `删除`{.descname} （ *状态*，*值*，*发起人* ） [¶ T6\>](#sqlalchemy.orm.interfaces.AttributeExtension.remove "Permalink to this definition")
    :   收到移除事件。

        没有定义返回值。

     `set`{.descname}(*state*, *value*, *oldvalue*, *initiator*)[¶](#sqlalchemy.orm.interfaces.AttributeExtension.set "Permalink to this definition")
    :   收到设定的事件。

        返回的值将用作要设置的实际值。


