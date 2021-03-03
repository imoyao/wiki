---
title: 会话 API
date: 2021-02-20 22:41:46
permalink: /sqlalchemy/orm/session_api/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
会话API [¶](#session-api "Permalink to this headline")
======================================================

Session和sessionmaker()[¶](#session-and-sessionmaker "Permalink to this headline")
----------------------------------------------------------------------------------

*class* `sqlalchemy.orm.session。`{.descclassname} `sessionmaker`{.descname} （ *bind = None*，*class \_ =＆lt； class'sqlalchemy.orm.session.Session'＆gt；*，*autoflush = True*，*autocommit = False*，*expire\_on\_commit = True *info = None*，*\*\* kw* ） [¶](#sqlalchemy.orm.session.sessionmaker "Permalink to this definition")*
:   基础：`sqlalchemy.orm.session._SessionClassMethods`

    一个可配置的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")工厂。

    [`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")工厂在调用时生成新的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象，根据此处建立的配置参数创建它们。

    例如。：

        # global scope
        Session = sessionmaker(autoflush=False)

        # later, in a local scope, create and use a session:
        sess = Session()

    发送到构造函数本身的任何关键字参数将覆盖“已配置”关键字：

        Session = sessionmaker()

        # bind an individual session to a connection
        sess = Session(bind=connection)

    该类还包含一个方法[`configure()`](#sqlalchemy.orm.session.sessionmaker.configure "sqlalchemy.orm.session.sessionmaker.configure")，该方法可用于指定工厂的其他关键字参数，该参数将在随后生成的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象中生效。这通常用于在第一次使用之前将一个或多个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")对象与现有的[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")工厂相关联：

        # application starts
        Session = sessionmaker()

        # ... later
        engine = create_engine('sqlite:///foo.db')
        Session.configure(bind=engine)

        sess = Session()

    ` __呼叫__  T0> （ T1>  ** local_kw  T2> ） T3> ¶ T4>`{.descname}
    :   使用此[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")中建立的配置生成新的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象。

        在Python中，当调用与对象相同的方式“调用”时，会在对象上调用`__call__`方法：

            Session = sessionmaker()
            session = Session()  # invokes sessionmaker.__call__()

    `__ init __`{.descname} （ *bind = None*，*class \_ =＆lt； class'sqlalchemy.orm.session.Session'＆gt；* ，*autoflush = True*，*autocommit = False*，*expire\_on\_commit = True*，*info =无*，*\*\*千瓦 T8\> ） T9\> [¶ T10\>](#sqlalchemy.orm.session.sessionmaker.__init__ "Permalink to this definition")*
    :   构建一个新的[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")。

        除了`class_`之外，所有参数都直接对应于由[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")接受的参数。有关参数的更多详细信息，请参阅[`Session.__init__()`](#sqlalchemy.orm.session.Session.__init__ "sqlalchemy.orm.session.Session.__init__")
        docstring。

        参数：

        -   **bind**[¶](#sqlalchemy.orm.session.sessionmaker.params.bind)
            – a [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            or other [`Connectable`](core_connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")
            with which newly created [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            objects will be associated.
        -   **class\_**[¶](#sqlalchemy.orm.session.sessionmaker.params.class_)
            – class to use in order to create new [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            objects. 默认为[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。
        -   **autoflush**[¶](#sqlalchemy.orm.session.sessionmaker.params.autoflush)
            – The autoflush setting to use with newly created
            [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            objects.
        -   **autocommit**[¶](#sqlalchemy.orm.session.sessionmaker.params.autocommit)
            – The autocommit setting to use with newly created
            [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            objects.
        -   **expire\_on\_commit=True**[¶](#sqlalchemy.orm.session.sessionmaker.params.expire_on_commit)
            – the expire\_on\_commit setting to use with newly created
            [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            objects.
        -   **info**
            [¶](#sqlalchemy.orm.session.sessionmaker.params.info) -

            可通过[`Session.info`](#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")获得的可选信息字典。注意，当`info`参数指定给特定[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")施工操作时，该字典*更新*，不会被替换。

            版本0.9.0中的新功能

        -   **\*\*kw**[¶](#sqlalchemy.orm.session.sessionmaker.params.**kw)
            – all other keyword arguments are passed to the constructor
            of newly created [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            objects.

    ` close_all  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* `close_all()` *method of* `_SessionClassMethods`

        Close *all* sessions in memory.

    `配置 T0> （ T1>  ** new_kw  T2> ） T3> ¶ T4>`{.descname}
    :   （重新）配置这个sessionmaker的参数。

        例如。：

            Session = sessionmaker()

            Session.configure(bind=create_engine('sqlite://'))

    ` identity_key  T0> （ T1>  * ARGS  T2>， ** kwargs  T3> ） T4> ¶ T5>`{.descname}
    :   *inherited from the* `identity_key()` *method of* `_SessionClassMethods`

        返回身份密钥。

        这是[`util.identity_key()`](mapping_api.html#sqlalchemy.orm.util.identity_key "sqlalchemy.orm.util.identity_key")的别名。

    ` object_session  T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* `object_session()` *method of* `_SessionClassMethods`

        返回对象所属的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

        这是[`object_session()`](#sqlalchemy.orm.session.object_session "sqlalchemy.orm.session.object_session")的别名。

 *class*`sqlalchemy.orm.session.`{.descclassname}`Session`{.descname}(*bind=None*, *autoflush=True*, *expire\_on\_commit=True*, *\_enable\_transaction\_accounting=True*, *autocommit=False*, *twophase=False*, *weak\_identity\_map=True*, *binds=None*, *extension=None*, *info=None*, *query\_cls=\<class 'sqlalchemy.orm.query.Query'\>*)[¶](#sqlalchemy.orm.session.Session "Permalink to this definition")
:   基础：`sqlalchemy.orm.session._SessionClassMethods`

    管理ORM映射对象的持久性操作。plain

    会话的使用范例在[*Using the Session*](session.html)中描述。

     `__init__`{.descname}(*bind=None*, *autoflush=True*, *expire\_on\_commit=True*, *\_enable\_transaction\_accounting=True*, *autocommit=False*, *twophase=False*, *weak\_identity\_map=True*, *binds=None*, *extension=None*, *info=None*, *query\_cls=\<class 'sqlalchemy.orm.query.Query'\>*)[¶](#sqlalchemy.orm.session.Session.__init__ "Permalink to this definition")
    :   构建一个新的会话。

        另请参阅[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")函数，该函数用于生成具有给定参数集的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")生成可调用对象。

        参数：

        -   **autocommit**
            [¶](#sqlalchemy.orm.session.Session.params.autocommit) -

            警告

            自动提交标志**不用于一般用途**，如果使用它，只应在[`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")
            / [`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")对。在划定的事务之外执行查询是传统的使用模式，并且在某些情况下可能会导致并发连接检出。

            默认为`False`。当`True`时，[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")不会保持持续的事务处于运行状态，并且会根据需要从引擎获取连接，并在使用后立即返回。如果没有交易存在，冲洗将开始并提交（或可能回滚）自己的交易。使用此模式时，[`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法用于显式启动事务。

            也可以看看

            [Autocommit
            Mode](session_transaction.html#session-autocommit)

        -   **autoflush**[¶](#sqlalchemy.orm.session.Session.params.autoflush)
            – When `True`, all query operations will
            issue a [`flush()`](#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")
            call to this `Session` before
            proceeding.
            这是一个方便的功能，因此无需重复调用[`flush()`](#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")以便数据库查询检索结果。通常，`autoflush`与`autocommit=False`结合使用。在这种情况下，很少需要显式调用[`flush()`](#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")；你通常只需要调用[`commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")（刷新）来完成更改。
        -   **bind**[¶](#sqlalchemy.orm.session.Session.params.bind) –
            An optional [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            or [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            to which this `Session` should be bound.
            指定时，此会话执行的所有SQL操作将通过此可连接执行。
        -   **绑定** [¶](#sqlalchemy.orm.session.Session.params.binds) -

            包含更多粒度的可选字典
            :   “绑定”信息比`bind`参数提供的信息。This dictionary can map
                individual :class\`.Table\` instances as well as
                [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
                instances to individual [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
                or [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
                objects. 相对于特定[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")进行的操作将查询此字典中的直接[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")实例以及映射器的`mapped_table`属性，以便找到可连接使用。完整的分辨率在[`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")中描述。用法如下所示：

                    Session = sessionmaker(binds={
                        SomeMappedClass: create_engine('postgresql://engine1'),
                        somemapper: create_engine('postgresql://engine2'),
                        some_table: create_engine('postgresql://engine3'),
                        })

            另请参阅[`Session.bind_mapper()`](#sqlalchemy.orm.session.Session.bind_mapper "sqlalchemy.orm.session.Session.bind_mapper")和[`Session.bind_table()`](#sqlalchemy.orm.session.Session.bind_table "sqlalchemy.orm.session.Session.bind_table")方法。

        -   **class\_**[¶](#sqlalchemy.orm.session.Session.params.class_)
            – Specify an alternate class other than
            `sqlalchemy.orm.session.Session` which
            should be used by the returned class.
            这是[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")函数本地唯一的参数，不会直接发送给`Session`的构造函数。
        -   **\_enable\_transaction\_accounting**
            [¶](#sqlalchemy.orm.session.Session.params._enable_transaction_accounting)
            - 默认为`True`。A legacy-only flag which
            when `False` disables *all* 0.5-style
            object accounting on transaction boundaries, including
            auto-expiry of instances on rollback and commit, maintenance
            of the “new” and “deleted” lists upon rollback, and
            autoflush of pending changes upon [`begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin"),
            all of which are interdependent.
        -   **expire\_on\_commit**
            [¶](#sqlalchemy.orm.session.Session.params.expire_on_commit)
            - 默认为`True`。当`True`时，所有实例将在每个[`commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")后完全过期，以便完成的事务之后的所有属性/对象访问将从最近的数据库状态加载。
        -   **extension**[¶](#sqlalchemy.orm.session.Session.params.extension)
            – An optional [`SessionExtension`](deprecated.html#sqlalchemy.orm.interfaces.SessionExtension "sqlalchemy.orm.interfaces.SessionExtension")
            instance, or a list of such instances, which will receive
            pre- and post- commit and flush events, as well as a
            post-rollback event. **已过时。
            T0\>**请参阅[`SessionEvents`](events.html#sqlalchemy.orm.events.SessionEvents "sqlalchemy.orm.events.SessionEvents")。
        -   **info** [¶](#sqlalchemy.orm.session.Session.params.info) -

            任意数据的可选字典将与此[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联。通过[`Session.info`](#sqlalchemy.orm.session.Session.info "sqlalchemy.orm.session.Session.info")属性可用。请注意，字典在构建时被复制，以便对[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")字典的修改将在本地到[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

            版本0.9.0中的新功能

        -   **query\_cls**[¶](#sqlalchemy.orm.session.Session.params.query_cls)
            – Class which should be used to create new Query objects, as
            returned by the [`query()`](#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")
            method. 默认为[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")。
        -   **twophase**[¶](#sqlalchemy.orm.session.Session.params.twophase)
            – When `True`, all transactions will be
            started as a “two phase” transaction, i.e. using the “two
            phase” semantics of the database in use along with an XID.
            During a [`commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit"),
            after [`flush()`](#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")
            has been issued for all attached databases, the
            [`prepare()`](core_connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare "sqlalchemy.engine.TwoPhaseTransaction.prepare")
            method on each database’s [`TwoPhaseTransaction`](core_connections.html#sqlalchemy.engine.TwoPhaseTransaction "sqlalchemy.engine.TwoPhaseTransaction")
            will be called.
            这允许每个数据库在每个事务提交之前回滚整个事务。
        -   **weak\_identity\_map**[¶](#sqlalchemy.orm.session.Session.params.weak_identity_map)
            – Defaults to `True` - when set to
            `False`, objects placed in the
            [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            will be strongly referenced until explicitly removed or the
            [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            is closed. **弃用** - 强参考身份地图是遗留的。请参阅[Session
            Referencing
            Behavior](session_state_management.html#session-referencing-behavior)中的配方，了解基于事件的方法以维护强壮的身份参考。

    `add`{.descname} （ *instance*，*\_warn = True* ） [t5 \>](#sqlalchemy.orm.session.Session.add "Permalink to this definition")
    :   在`Session`中放置一个对象。

        它的状态将在下一次刷新操作时持续到数据库。

        重复调用`add()`将被忽略。与`add()`相反的是`expunge()`。

    ` add_all  T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   将给定的实例集合添加到此`Session`中。

     `begin`{.descname}(*subtransactions=False*, *nested=False*)[¶](#sqlalchemy.orm.session.Session.begin "Permalink to this definition")
    :   在此[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")上开始交易。

        如果此会话已经在事务中，无论是明文事务还是嵌套事务，都会引发错误，除非指定了`subtransactions=True`或`nested=True`。

        `subtransactions=True`标志指示如果事务已经在进行中，则此[`begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")可以创建子事务。有关子事务的文档，请参阅[Using
        Subtransactions with
        Autocommit](session_transaction.html#session-subtransactions)。

        `nested`标志开始一个SAVEPOINT事务，相当于调用[`begin_nested()`](#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")。有关SAVEPOINT交易的文档，请参阅[Using
        SAVEPOINT](session_transaction.html#session-begin-nested)。

    ` begin_nested  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在此会话上开始一个嵌套事务。

        目标数据库必须支持SQL SAVEPOINT或支持SQLAlchemy的供应商实现。

        有关SAVEPOINT交易的文档，请参阅[Using
        SAVEPOINT](session_transaction.html#session-begin-nested)。

     `bind_mapper`{.descname}(*mapper*, *bind*)[¶](#sqlalchemy.orm.session.Session.bind_mapper "Permalink to this definition")
    :   将[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")与“绑定”相关联，例如一个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")。

        给定的映射器被添加到由[`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")方法使用的查找中。

     `bind_table`{.descname}(*table*, *bind*)[¶](#sqlalchemy.orm.session.Session.bind_table "Permalink to this definition")
    :   将[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")与“绑定”相关联，例如一个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")。

        给定的映射器被添加到由[`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")方法使用的查找中。

     `bulk_insert_mappings`{.descname}(*mapper*, *mappings*, *return\_defaults=False*, *render\_nulls=False*)[¶](#sqlalchemy.orm.session.Session.bulk_insert_mappings "Permalink to this definition")
    :   执行给定映射词典列表的批量插入。

        批量插入功能允许将普通的Python字典用作简单INSERT操作的来源，这些操作可以更容易地组合为更高性能的“执行”操作。使用字典时，没有使用“历史记录”或会话状态管理功能，可以在插入大量简单行时减少延迟。

        在给定映射器映射到的表内组织它们中的值之后，字典中给定的值通常在未修改的情况下传递到Core
        `Insert()`结构中。

        版本1.0.0中的新功能

        警告

        批量插入功能允许以更低延迟的行插入代价来实现大多数其他工作单元功能。Features
        such as object management, relationship handling, and SQL clause
        support are **silently omitted** in favor of raw INSERT of
        records.

        **在使用此方法之前，请阅读** [Bulk
        Operations](persistence_techniques.html#bulk-operations)
        **中的注意事项列表，并完全测试并确认使用这些系统开发的所有代码的功能。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.mapper)
            – a mapped class, or the actual [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            object, representing the single kind of object represented
            within the mapping list.
        -   T0\> **映射 T1\> [¶ T2\> -
            字典的列表，将被插入每一个包含映射行的状态下，在上的属性名称的术语映射类。](#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.mappings)**如果映射涉及多个表（如联合继承映射），则每个字典都必须包含要填充到所有表中的所有键。
        -   **return\_defaults**[¶](#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.return_defaults)
            – when True, rows that are missing values which generate
            defaults, namely integer primary key defaults and sequences,
            will be inserted **one at a time**, so that the primary key
            value is available.
            特别是，这将允许加入继承和其他多表映射正确插入，而不需要提前提供主键值；然而，[`Session.bulk_insert_mappings.return_defaults`](#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.return_defaults "sqlalchemy.orm.session.Session.bulk_insert_mappings")
            **大大降低了整体方法的性能增益。**如果要插入的行仅引用单个表，那么没有理由设置此标志，因为不使用返回的默认信息。
        -   **render\_nulls**
            [¶](#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.render_nulls)
            -

            当为True时，`None`的值将导致INSERT语句中包含NULL值，而不是INSERT中省略的列。这允许所有被插入的行具有相同的一组列，这允许将全部行集合到DBAPI。通常情况下，包含与前一行不同的NULL值组合的每个列集必须从所呈现的INSERT语句中省略不同的一系列列，这意味着它必须作为单独的语句发布。通过传递这个标志，整套行保证可批量化为一个批次；但是费用是由省略列调用的服务器端默认值将被跳过，因此必须小心确保这些不是必需的。

            警告

            设置此标志时，对于插入为NULL的列，**服务器端默认SQL值不会被调用**；
            NULL值将被明确发送。必须注意确保不需要为整个操作调用服务器端默认功能。

            版本1.1中的新功能

        也可以看看

        [Bulk Operations](persistence_techniques.html#bulk-operations)

        [`Session.bulk_save_objects()`](#sqlalchemy.orm.session.Session.bulk_save_objects "sqlalchemy.orm.session.Session.bulk_save_objects")

        [`Session.bulk_update_mappings()`](#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")

    `bulk_save_objects`{.descname} （ *objects*，*return\_defaults = False*，*update\_changed\_only = True* ） T5\> [¶ T6\>](#sqlalchemy.orm.session.Session.bulk_save_objects "Permalink to this definition")
    :   执行给定对象列表的批量保存。

        批量保存功能允许映射对象用作简单INSERT和UPDATE操作的来源，这些操作可以更容易地组合为更高性能的“executemany”操作；从对象中提取数据也使用低延迟进程执行，忽略UPDATE中是否实际修改了属性，还忽略了SQL表达式。

        给定的对象不会添加到会话中，除非还设置了`return_defaults`标志，否则将不会创建其他状态，在这种情况下，将会填充主键属性和服务器端默认值。

        版本1.0.0中的新功能

        警告

        批量保存功能允许以大部分其他工作单元功能为代价实现行延迟更低的INSERT
        / UPDATE。Features such as object management, relationship
        handling, and SQL clause support are **silently omitted** in
        favor of raw INSERT/UPDATES of records.

        **在使用此方法之前，请阅读** [Bulk
        Operations](persistence_techniques.html#bulk-operations)
        **中的注意事项列表，并完全测试并确认使用这些系统开发的所有代码的功能。**

        参数：

        -   **对象**
            [¶](#sqlalchemy.orm.session.Session.bulk_save_objects.params.objects)
            -

            一个映射对象实例的列表。映射的对象保持原样，之后**不**与[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联。

            对于每个对象，对象是否作为INSERT或UPDATE发送取决于传统操作中[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")使用的相同规则；如果对象具有`InstanceState.key`属性集，则该对象被假定为“分离”并且将导致UPDATE。否则，使用INSERT。

            在UPDATE的情况下，语句根据哪些属性发生了变化进行分组，并因此成为每个SET子句的主题。如果`update_changed_only`为False，那么每个对象中的所有属性都会应用到UPDATE语句中，这可能有助于允许将语句组合到一个更大的executemany()中，并且还会减少开销检查属性的历史记录。

        -   **return\_defaults**[¶](#sqlalchemy.orm.session.Session.bulk_save_objects.params.return_defaults)
            – when True, rows that are missing values which generate
            defaults, namely integer primary key defaults and sequences,
            will be inserted **one at a time**, so that the primary key
            value is available.
            特别是，这将允许加入继承和其他多表映射正确插入，而不需要提前提供主键值；然而，[`Session.bulk_save_objects.return_defaults`](#sqlalchemy.orm.session.Session.bulk_save_objects.params.return_defaults "sqlalchemy.orm.session.Session.bulk_save_objects")
            **大大降低了整个方法的性能增益。**
        -   **update\_changed\_only**[¶](#sqlalchemy.orm.session.Session.bulk_save_objects.params.update_changed_only)
            – when True, UPDATE statements are rendered based on those
            attributes in each state that have logged changes.
            如果为False，则所有呈现的属性都将呈现到SET子句中，但主键属性除外。

        也可以看看

        [Bulk Operations](persistence_techniques.html#bulk-operations)

        [`Session.bulk_insert_mappings()`](#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")

        [`Session.bulk_update_mappings()`](#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")

     `bulk_update_mappings`{.descname}(*mapper*, *mappings*)[¶](#sqlalchemy.orm.session.Session.bulk_update_mappings "Permalink to this definition")
    :   对映射字典的给定列表执行批量更新。

        批量更新功能允许将普通Python字典用作简单UPDATE操作的来源，这些操作可以更容易地组合到更高性能的“执行”操作中。使用字典时，没有使用“历史记录”或会话状态管理功能，在更新大量简单行时减少延迟。

        版本1.0.0中的新功能

        警告

        批量更新功能允许以更低的延迟更新行，而牺牲大多数其他工作单元功能。Features
        such as object management, relationship handling, and SQL clause
        support are **silently omitted** in favor of raw UPDATES of
        records.

        **在使用此方法之前，请阅读** [Bulk
        Operations](persistence_techniques.html#bulk-operations)
        **中的注意事项列表，并完全测试并确认使用这些系统开发的所有代码的功能。**

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.session.Session.bulk_update_mappings.params.mapper)
            – a mapped class, or the actual [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            object, representing the single kind of object represented
            within the mapping list.
        -   **mappings**[¶](#sqlalchemy.orm.session.Session.bulk_update_mappings.params.mappings)
            – a list of dictionaries, each one containing the state of
            the mapped row to be updated, in terms of the attribute
            names on the mapped class.
            如果映射涉及多个表（如联合继承映射），则每个字典可能包含与所有表对应的键。所有存在且不是主键一部分的键都应用于UPDATE语句的SET子句；所需的主键值应用于WHERE子句。

        也可以看看

        [Bulk Operations](persistence_techniques.html#bulk-operations)

        [`Session.bulk_insert_mappings()`](#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")

        [`Session.bulk_save_objects()`](#sqlalchemy.orm.session.Session.bulk_save_objects "sqlalchemy.orm.session.Session.bulk_save_objects")

    `靠近 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   关闭本次会议。

        这会清除所有项目并结束正在进行的任何交易。

        如果此会话是使用`autocommit=False`创建的，则立即开始一个新事务。请注意，这个新事务在第一次需要之前不会使用任何连接资源。

    ` close_all  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* `close_all()` *method of* `_SessionClassMethods`

        Close *all* sessions in memory.

    `提交 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   刷新挂起的更改并提交当前事务。

        如果没有事务正在进行，则此方法引发一个[`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")。

        默认情况下，在事务提交后，[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")也会在所有ORM托管的属性上过期加载所有数据库状态。这样可以使后续操作从数据库加载最新的数据。可以使用[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")或[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")构造函数的`expire_on_commit=False`选项禁用此行为。

        如果子事务有效（在多次调用begin()时发生），子事务将被关闭，并且对`commit()`的下一次调用将在封闭事务上运行。

        当在`autocommit=False`的默认模式下使用[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，将在提交后立即开始一个新的事务，但请注意，新开始的事务不会**使用任何连接资源，直到第一个SQL实际发出。

        也可以看看

        [Committing](session_basics.html#session-committing)

     `connection`{.descname}(*mapper=None*, *clause=None*, *bind=None*, *close\_with\_result=False*, *execution\_options=None*, *\*\*kw*)[¶](#sqlalchemy.orm.session.Session.connection "Permalink to this definition")
    :   返回与此[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的事务状态相对应的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象。

        如果[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")配置为`autocommit=False`，则返回与当前事务对应的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")，或者如果没有事务正在进行，一个新的开始并返回[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")（请注意，在发出第一个SQL语句之前，没有与DBAPI建立事务性状态）。

        Alternatively, if this [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        is configured with `autocommit=True`, an
        ad-hoc [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
        is returned using [`Engine.contextual_connect()`](core_connections.html#sqlalchemy.engine.Engine.contextual_connect "sqlalchemy.engine.Engine.contextual_connect")
        on the underlying [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine").

        多重绑定或未绑定的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象中的歧义可以通过任何可选的关键字参数来解决。这最终会使用[`get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")方法进行解析。

        参数：

        -   **bind**[¶](#sqlalchemy.orm.session.Session.connection.params.bind)
            – Optional [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            to be used as the bind.
            如果此引擎已经涉及正在进行的交易，则将使用该连接。此参数优先于`mapper`，`clause`。
        -   **mapper**[¶](#sqlalchemy.orm.session.Session.connection.params.mapper)
            – Optional [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
            mapped class, used to identify the appropriate bind.
            此参数优先于`clause`。
        -   **clause**[¶](#sqlalchemy.orm.session.Session.connection.params.clause)
            – A [`ClauseElement`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            (i.e. [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
            [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text"),
            etc.) 如果绑定不能以其他方式被识别，将用于定位绑定。
        -   **close\_with\_result**[¶](#sqlalchemy.orm.session.Session.connection.params.close_with_result)
            – Passed to [`Engine.connect()`](core_connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect"),
            indicating the [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
            should be considered “single use”, automatically closing
            when the first result set is closed. 如果[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")配置为`autocommit=True`并且尚未执行事务，则此标志仅起作用。
        -   **execution\_options**
            [¶](#sqlalchemy.orm.session.Session.connection.params.execution_options)
            -

            一个执行选项的字典，当连接首次被采购时，它将被传递给[`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")，****。如果连接已经存在于[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中，则发出警告并忽略参数。

            版本0.9.9中的新功能

            也可以看看

            [Setting Transaction Isolation
            Levels](session_transaction.html#session-transaction-isolation)

        -   **\*\*kw**[¶](#sqlalchemy.orm.session.Session.connection.params.**kw)
            – Additional keyword arguments are sent to
            [`get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind"),
            allowing additional arguments to be passed to custom
            implementations of [`get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind").

    `删除 T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   将实例标记为已删除。

        数据库删除操作发生在`flush()`上。

    `删除 T0> ¶ T1>`{.descname}
    :   在`Session`中标记为“已删除”的所有实例的集合

    `脏 T0> ¶ T1>`{.descname}
    :   所有持久实例的集合都被认为是脏的。

        例如。：

            some_mapped_object in session.dirty

        实例在被修改但被删除时被认为是脏的。

        请注意，这种“肮脏”的计算是'乐观'的；大多数属性设置或集合修改操作都会将实例标记为“脏”，并将其置于此集合中，即使属性值没有净更改。在刷新时间，将每个属性的值与之前保存的值进行比较，如果没有净更改，则不会执行SQL操作（这是更昂贵的操作，因此只能在刷新时执行）。

        要检查一个实例是否对其属性进行了可操作的净更改，请使用[`Session.is_modified()`](#sqlalchemy.orm.session.Session.is_modified "sqlalchemy.orm.session.Session.is_modified")方法。

    ` enable_relationship_loading  T0> （ T1>  OBJ  T2> ） T3> ¶ T4>`{.descname}
    :   将对象与此[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")相关联以进行相关的对象加载。

        警告

        [`enable_relationship_loading()`](#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")
        exists to serve special use cases and is not recommended for
        general use.

        使用[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")映​​射的属性访问将尝试使用此[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")作为连接的来源从数据库加载值。这些值将根据此对象上存在的外键值加载
        - 因此，此功能通常仅适用于多对一关系。

        该对象将被附加到该会话中，但**不会**参与任何持久性操作；其几乎所有目的的状态将保持“暂时”或“分离”，除了关系加载的情况。

        另请注意，backrefs通常无法按预期工作。如果有效值是已从外键持有值加载的内容，则在目标对象上更改关系绑定属性可能不会触发backref事件。

        [`Session.enable_relationship_loading()`](#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")方法类似于[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上的`load_on_pending`标志。与该标志不同，[`Session.enable_relationship_loading()`](#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")允许对象保持瞬态，同时仍然能够加载相关项目。

        To make a transient object associated with a [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        via [`Session.enable_relationship_loading()`](#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")
        pending, add it to the [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        using [`Session.add()`](#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")
        normally.

        [`Session.enable_relationship_loading()`](#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")
        does not improve behavior when the ORM is used normally - object
        references should be constructed at the object level, not at the
        foreign key level, so that they are present in an ordinary way
        before flush() proceeds. 此方法不适用于一般用途。

        0.8版本中的新功能

        也可以看看

        `load_on_pending` at [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
        - this flag allows per-relationship loading of many-to-ones on
        items that are pending.

     `execute`{.descname}(*clause*, *params=None*, *mapper=None*, *bind=None*, *\*\*kw*)[¶](#sqlalchemy.orm.session.Session.execute "Permalink to this definition")
    :   在当前事务中执行SQL表达式结构或字符串语句。

        以与[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")相同的方式返回表示语句执行结果的[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")。

        例如。：

            result = session.execute(
                        user_table.select().where(user_table.c.id == 5)
                    )

        [`execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
        accepts any executable clause construct, such as
        [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
        [`insert()`](core_dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert"),
        [`update()`](core_dml.html#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update"),
        [`delete()`](core_dml.html#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete"),
        and [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text").
        普通的SQL字符串也可以被传递，在[`Session.execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")的情况下，它将被解释为与通过[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")构造传递相同。即，以下用法：

            result = session.execute(
                        "SELECT * FROM user WHERE id=:param",
                        {"param":5}
                    )

        相当于：

            from sqlalchemy import text
            result = session.execute(
                        text("SELECT * FROM user WHERE id=:param"),
                        {"param":5}
                    )

        [`Session.execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")的第二个位置参数是一个可选参数集。与[`Connection.execute()`](core_connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")类似，无论是作为单个字典还是字典列表传递，都会确定DBAPI游标的`execute()`或`executemany()`用于执行语句。可以为单个行调用INSERT构造：

            result = session.execute(
                users.insert(), {"id": 7, "name": "somename"})

        或多行：

            result = session.execute(users.insert(), [
                                    {"id": 7, "name": "somename7"},
                                    {"id": 8, "name": "somename8"},
                                    {"id": 9, "name": "somename9"}
                                ])

        该语句在[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的当前事务上下文中执行。用于执行语句的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")也可以通过调用[`Session.connection()`](#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")方法直接获取。这两种方法都使用基于规则的解决方案来确定[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")，它在平均情况下直接来自[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本身的“绑定”，并且在其他情况可以基于传递给该方法的[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")和[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象；请参阅[`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")的文档以获得该方案的完整描述。

        The [`Session.execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
        method does *not* invoke autoflush.

        The [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
        returned by the [`Session.execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
        method is returned with the “close\_with\_result” flag set to
        true; the significance of this flag is that if this
        [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        is autocommitting and does not have a transaction-dedicated
        [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
        available, a temporary [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
        is established for the statement execution, which is closed
        (meaning, returned to the connection pool) when the
        [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
        has consumed all available data. 当[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")配置为autocommit
        = True并且没有事务已启动时，这仅适用于**。

        参数：

        -   **clause**[¶](#sqlalchemy.orm.session.Session.execute.params.clause)
            – An executable statement (i.e. an [`Executable`](core_selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")
            expression such as [`expression.select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"))
            or string SQL statement to be executed.
        -   **params**[¶](#sqlalchemy.orm.session.Session.execute.params.params)
            – Optional dictionary, or list of dictionaries, containing
            bound parameter values.
            如果单个字典发生单行执行；如果一个字典列表，“executemany”将被调用。每个字典中的键必须对应于语句中存在的参数名称。
        -   **mapper**[¶](#sqlalchemy.orm.session.Session.execute.params.mapper)
            – Optional [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
            or mapped class, used to identify the appropriate bind.
            定位绑定时，此参数优先于`clause`。有关更多详细信息，请参阅[`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")。
        -   **bind**[¶](#sqlalchemy.orm.session.Session.execute.params.bind)
            – Optional [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
            to be used as the bind.
            如果此引擎已经涉及正在进行的交易，则将使用该连接。定位绑定时，此参数优先于`mapper`和`clause`。
        -   **\*\*kw**[¶](#sqlalchemy.orm.session.Session.execute.params.**kw)
            – Additional keyword arguments are sent to
            [`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")
            to allow extensibility of “bind” schemes.

        也可以看看

        [SQL Expression Language Tutorial](core_tutorial.html) -
        使用Core SQL结构的教程。

        [Working with Engines and Connections](core_connections.html) -
        有关直接语句执行的更多信息。

        [`Connection.execute()`](core_connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")
        - core level statement execution method, which is
        [`Session.execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
        ultimately uses in order to execute the statement.

    `expire`{.descname} （ *实例*，*attribute\_names =无* ） [t5 \>](#sqlalchemy.orm.session.Session.expire "Permalink to this definition")
    :   过期实例上的属性。

        将实例的属性标记为过时。当下一次访问过期属性时，将向[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的当前事务上下文发出查询，以加载给定实例的所有过期属性。请注意，高度孤立的事务将返回与先前在同一事务中读取的值相同的值，而不考虑该事务之外的数据库状态更改。

        要同时过期[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中的所有对象，请使用[`Session.expire_all()`](#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")。

        [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的默认行为是在每次调用[`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")或[`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")方法时过期所有状态，可以为新事务加载新状态。因此，调用[`Session.expire()`](#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")仅适用于在当前事务中发出非ORM
        SQL语句的特定情况。

        参数：

        -   **instance**[¶](#sqlalchemy.orm.session.Session.expire.params.instance)
            – The instance to be refreshed.
        -   **attribute\_names**[¶](#sqlalchemy.orm.session.Session.expire.params.attribute_names)
            – optional list of string attribute names indicating a
            subset of attributes to be expired.

        也可以看看

        [Refreshing /
        Expiring](session_state_management.html#session-expire) -
        介绍材料

        [`Session.expire()`](#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")

        [`Session.refresh()`](#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")

    ` expire_all  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在此会话中过期所有持久性实例。

        当下一次访问持久实例上的任何属性时，将使用[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的当前事务上下文发出查询，以加载给定实例的所有过期属性。请注意，高度孤立的事务将返回与先前在同一事务中读取的值相同的值，而不考虑该事务之外的数据库状态更改。

        要使这些对象上的单个对象和单个属性过期，请使用[`Session.expire()`](#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")。

        [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的默认行为是在每次调用[`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")或[`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")方法时过期所有状态，可以为新事务加载新状态。因此，假设事务是孤立的，在autocommit
        `False`时不应该需要调用[`Session.expire_all()`](#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")。

        也可以看看

        [Refreshing /
        Expiring](session_state_management.html#session-expire) -
        介绍材料

        [`Session.expire()`](#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")

        [`Session.refresh()`](#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")

    `则清除 T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   从`Session`中删除实例。

        这将释放对实例的所有内部引用。级联将根据*expunge*级联规则应用。

    ` expunge_all  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   从`Session`中删除所有对象实例。

        这相当于在`Session`中的所有对象上调用`expunge(obj)`。

    `冲洗 T0> （ T1> 对象=无 T2> ） T3> ¶ T4>`{.descname}
    :   将所有对象更改刷新到数据库。

        将所有挂起的对象创建，删除和修改写入INSERT，DELETE，UPDATE等操作由会话的工作单元依赖性求解器自动排序。

        数据库操作将在当前的事务上下文中发布，并且不会影响事务的状态，除非发生错误，在这种情况下整个事务将被回滚。您可以在事务中随时刷新()以将更改从Python移动到数据库的事务缓冲区。

        对于没有活动手动事务的`autocommit`会话，flush()将立即创建一个事务，将整个操作集合包含在flush中。

        参数：

        **对象**
        [¶](#sqlalchemy.orm.session.Session.flush.params.objects) -

        可选的；限制刷新操作仅对指定集合中的元素进行操作。

        此功能适用于在完全冲洗()发生之前可能需要对特定对象进行操作的极其狭窄的一组用例。它不适用于一般用途。

    ` get_bind  T0> （ T1> 映射器=无 T2>，子句=无 T3> ） T4> ¶< / T5>`{.descname}
    :   返回该[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")绑定到的“绑定”。

        “绑定”通常是[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的一个实例，除非[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")已直接显式绑定到[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")。

        对于乘法或非约束[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，使用`mapper`或`clause`参数来确定要返回的适当绑定。

        Note that the “mapper” argument is usually present when
        [`Session.get_bind()`](#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")
        is called via an ORM operation such as a
        [`Session.query()`](#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query"),
        each individual INSERT/UPDATE/DELETE operation within a
        [`Session.flush()`](#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush"),
        call, etc.

        解决的顺序是：

        1.  如果存在映射器和session.binds，则根据映射器找到绑定。
        2.  如果存在子句given和session.binds，则根据在session.binds中给出的子句中找到的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象找到一个绑定。
        3.  如果session.bind存在，则返回该值。
        4.  如果给出子句，则尝试返回链接到最终与该子句关联的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")的绑定。
        5.  如果给定了映射器，则尝试返回链接到最终与映射器映射到的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")或其他可选映射关联的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")的绑定。
        6.  无法找到绑定，[`UnboundExecutionError`](core_exceptions.html#sqlalchemy.exc.UnboundExecutionError "sqlalchemy.exc.UnboundExecutionError")。

        参数：

        -   **mapper**[¶](#sqlalchemy.orm.session.Session.get_bind.params.mapper)
            – Optional [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")
            mapped class or instance of [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper").
            The bind can be derived from a [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            first by consulting the “binds” map associated with this
            [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
            and secondly by consulting the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
            associated with the [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            to which the [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
            is mapped for a bind.
        -   **clause**[¶](#sqlalchemy.orm.session.Session.get_bind.params.clause)
            – A [`ClauseElement`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            (i.e. [`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select"),
            [`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text"),
            etc.). If the `mapper` argument is not
            present or could not produce a bind, the given expression
            construct will be searched for a bound element, typically a
            [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            associated with bound [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData").

    ` identity_key  T0> （ T1>  * ARGS  T2>， ** kwargs  T3> ） T4> ¶ T5>`{.descname}
    :   *inherited from the* `identity_key()` *method of* `_SessionClassMethods`

        返回身份密钥。

        这是[`util.identity_key()`](mapping_api.html#sqlalchemy.orm.util.identity_key "sqlalchemy.orm.util.identity_key")的别名。

    `identity_map`{.descname} *=无* [¶](#sqlalchemy.orm.session.Session.identity_map "Permalink to this definition")
    :   将对象标识映射到对象本身。

        迭代通过`Session.identity_map.values()`可以访问当前在会话中的整套持久对象（即具有行标识的持久对象）。

        也可以看看

        [`identity_key()`](mapping_api.html#sqlalchemy.orm.util.identity_key "sqlalchemy.orm.util.identity_key")
        - helper function to produce the keys used in this dictionary.

    `信息 T0> ¶ T1>`{.descname}
    :   用户可修改的字典。

        该字典的初始值可以使用[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")构造函数或[`sessionmaker`](#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")构造函数或工厂方法的`info`参数填充。此处的字典始终是本地[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，并且可以独立于所有其他[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象进行修改。

        版本0.9.0中的新功能

    `无效 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   关闭此会话，使用连接失效。

        这是[`Session.close()`](#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")的一个变体，它还将确保[`Connection.invalidate()`](core_connections.html#sqlalchemy.engine.Connection.invalidate "sqlalchemy.engine.Connection.invalidate")方法在所有[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象上被调用。当知道数据库处于连接不再安全使用的状态时，可以调用它。

        例如。：

            try:
                sess = Session()
                sess.add(User())
                sess.commit()
            except gevent.Timeout:
                sess.invalidate()
                raise
            except:
                sess.rollback()
                raise

        这会清除所有项目并结束正在进行的任何交易。

        如果此会话是使用`autocommit=False`创建的，则立即开始一个新事务。请注意，这个新事务在第一次需要之前不会使用任何连接资源。

        版本0.9.9中的新功能

    ` IS_ACTIVE  T0> ¶ T1>`{.descname}
    :   True if this [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        is in “transaction mode” and is not in “partial rollback” state.

        在`autocommit=False`默认模式下的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本质上总是处于“事务模式”，因为[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")与其关联因为它被实例化。由于回滚，提交或关闭操作，这个[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")一旦被结束立即被新的替换。

        “Transaction mode” does *not* indicate whether or not actual
        database connection resources are in use; the
        [`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")
        object coordinates among zero or more actual database
        transactions, and starts out with none, accumulating individual
        DBAPI connections as different data sources are used within its
        scope. The best way to track when a particular [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        has actually begun to use DBAPI resources is to implement a
        listener using the [`SessionEvents.after_begin()`](events.html#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin")
        method, which will deliver both the [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        as well as the target [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
        to a user-defined event listener.

        “部分回滚”状态是指通常在刷新期间使用的“内部”事务遇到错误并发出DBAPI连接的回滚时。此时，[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")处于“部分回滚”并等待用户调用[`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")，以关闭事务堆栈。正是在这个“部分回滚”期间，[`is_active`](#sqlalchemy.orm.session.Session.is_active "sqlalchemy.orm.session.Session.is_active")标志返回False。After
        the call to [`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback"),
        the [`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")
        is replaced with a new one and [`is_active`](#sqlalchemy.orm.session.Session.is_active "sqlalchemy.orm.session.Session.is_active")
        returns `True` again.

        在`autocommit=True`模式下使用[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")仅在flush调用的范围内实例化，或[`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")被调用。So
        [`is_active`](#sqlalchemy.orm.session.Session.is_active "sqlalchemy.orm.session.Session.is_active")
        will always be `False` outside of a flush or
        [`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")
        block in this mode, and will be `True`
        within the [`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")
        block as long as it doesn’t enter “partial rollback” state.

        从以上所述可以看出，对于这个标志唯一的目的是希望检测的应用程序框架在通用错误处理例程中是必需的，对于[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象在“部分回滚”模式下。在一个典型的集成案例中，这也不是必须的，因为标准做法是无条件地在最外面的异常捕获中发布[`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")。

        To track the transactional state of a [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        fully, use event listeners, primarily the
        [`SessionEvents.after_begin()`](events.html#sqlalchemy.orm.events.SessionEvents.after_begin "sqlalchemy.orm.events.SessionEvents.after_begin"),
        [`SessionEvents.after_commit()`](events.html#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit"),
        [`SessionEvents.after_rollback()`](events.html#sqlalchemy.orm.events.SessionEvents.after_rollback "sqlalchemy.orm.events.SessionEvents.after_rollback")
        and related events.

    `is_modified`{.descname} （ *实例*，*include\_collections = True*，*passive = True* ） T5\> [¶ T6\>](#sqlalchemy.orm.session.Session.is_modified "Permalink to this definition")
    :   如果给定实例具有本地修改的属性，则返回`True`。

        此方法检索实例上每个已插装属性的历史记录，并将当前值与之前提交的值（如果有）进行比较。

        它实际上是检查[`Session.dirty`](#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty")集合中给定实例的更昂贵和准确的版本；对每个属性的“脏”状态进行全面测试。

        例如。：

            return session.is_modified(someobject)

        Changed in version 0.8: When using SQLAlchemy 0.7 and earlier,
        the `passive` flag should **always** be
        explicitly set to `True`, else SQL
        loads/autoflushes may proceed which can affect the modified
        state itself:
        `session.is_modified(someobject, passive=True)`. 在0.8和更高版本中，行为被纠正，并且该标志被忽略。

        这种方法的一些注意事项适用于：

        -   当使用此方法进行测试时，存在于[`Session.dirty`](#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty")集合中的实例可能会报告`False`。这是因为对象可能通过属性突变接收到更改事件，因此将其放置在[`Session.dirty`](#sqlalchemy.orm.session.Session.dirty "sqlalchemy.orm.session.Session.dirty")中，但最终状态与从数据库加载的状态相同，因此在此处没有净更改。

        -   标量属性可能没有记录应用新值的时候以前设置的值，如果在接收新值时该属性未加载或已过期
            -
            在这些情况下，该属性被假定为有变化，即使对数据库值最终没有净变化。在大多数情况下，SQLAlchemy在设置事件发生时不需要“旧”值，因此，如果旧值不存在，则基于假定需要更新标量值，则跳过SQL调用的开销，而在少数情况下，平均成本低于发布防御性SELECT。

            仅当属性容器的`active_history`标志设置为`True`时，才会无条件地获取“旧”值。通常为主键属性和标量对象引用设置此标志，这些参数不是简单的多对一。要为任意映射列设置此标志，请使用[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")的`active_history`参数。

        参数：

        -   **instance**[¶](#sqlalchemy.orm.session.Session.is_modified.params.instance)
            – mapped instance to be tested for pending changes.
        -   **include\_collections**
            [¶](#sqlalchemy.orm.session.Session.is_modified.params.include_collections)
            -
            指示是否应将多值集合包含在操作中。将此设置为`False`是一种仅检测基于本地列的属性（即标量列或多对一外键）的方法，这些属性在刷新时会导致此实例的UPDATE。
        -   **被动**
            [¶](#sqlalchemy.orm.session.Session.is_modified.params.passive)
            -

            Changed in version 0.8: Ignored for backwards compatibility.
            使用SQLAlchemy
            0.7及更早版本时，该标志应始终设置为`True`。

    `merge`{.descname} （ *instance*，*load = True* ） [t5 \>](#sqlalchemy.orm.session.Session.merge "Permalink to this definition")
    :   将给定实例的状态复制到[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")内的相应实例中。

        [`Session.merge()`](#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
        examines the primary key attributes of the source instance, and
        attempts to reconcile it with an instance of the same primary
        key in the session.
        如果没有在本地找到，它将尝试从基于主键的数据库加载对象，如果没有可找到的对象，则创建一个新实例。然后将源实例上的每个属性的状态复制到目标实例。然后由方法返回结果的目标实例；原始源实例保持不变，并且如果尚未与[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联。

        如果关联使用`cascade="merge"`映​​射，则此操作将级联到关联的实例。

        有关合并的详细讨论，请参阅[Merging](session_state_management.html#unitofwork-merging)。

        在版本1.1中更改： - [`Session.merge()`](#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")现在将以与持久性相同的方式协调具有重叠主键的挂起对象。有关讨论，请参阅[Session.merge
        resolves pending conflicts the same as
        persistent](changelog_migration_11.html#change-3601)相同的未决冲突。

        参数：

        -   **instance**[¶](#sqlalchemy.orm.session.Session.merge.params.instance)
            – Instance to be merged.
        -   **载入**
            [¶](#sqlalchemy.orm.session.Session.merge.params.load) -

            Boolean, when False, [`merge()`](#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")
            switches into a “high performance” mode which causes it to
            forego emitting history events as well as all database
            access. 该标志用于将对象图形从二级缓存转移到[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中，或将刚刚加载的对象转移到工作线程拥有的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中或过程而不重新查询数据库。

            `load=False`用例增加了给定对象必须处于“干净”状态的警告，也就是说，没有待处理的更改被刷新
            - 即使传入对象与任何对象分离[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")这样，当合并操作将本地属性和级联填充到相关对象和集合时，可以按原样将这些值“加盖”到目标对象上，而不会生成任何历史记录或属性事件，也不需要协调传入数据与任何现有的相关对象或集合可能不会被加载。来自`load=False`的结果对象总是产生为“干净”的，所以只有给定的对象也应该是“干净”的，否则这表明该方法被错误使用。

    `新的 T0> ¶ T1>`{.descname}
    :   在`Session`中标记为“新”的所有实例的集合。

    ` no_autoflush  T0> ¶ T1>`{.descname}
    :   返回禁用自动刷新的上下文管理器。

        例如。：

            with session.no_autoflush:

                some_object = SomeClass()
                session.add(some_object)
                # won't autoflush
                some_object.related_thing = session.query(SomeRelated).first()

        在`with:`块进行的操作在查询访问时不会发生刷新。这在初始化一系列涉及现有数据库查询的对象时很有用，其中未完成的对象应该尚未刷新。

        New in version 0.7.6.

    ` object_session  T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* `object_session()` *method of* `_SessionClassMethods`

        返回对象所属的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

        这是[`object_session()`](#sqlalchemy.orm.session.object_session "sqlalchemy.orm.session.object_session")的别名。

    `制备 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   准备当前正在进行的两阶段提交事务。

        如果没有事务正在进行，则此方法引发一个[`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")。

        只能准备两阶段会话的根交易。如果当前事务不是这样，则引发一个[`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")。

    `剪枝 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   移除标识映射中缓存的未引用实例。

        从版本0.7开始弃用：不再需要非弱引用标识映射功能。

        请注意，此方法仅在“weak\_identity\_map”设置为False时才有意义。默认的弱身份地图是自我修剪的。

        移除此会话身份地图中未在用户代码中引用，修改，新建或计划删除的任何对象。返回修剪的对象数量。

    `查询`{.descname} （ *\*实体*，*\*\* kwargs* ） [T5\>](#sqlalchemy.orm.session.Session.query "Permalink to this definition")
    :   返回与[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对应的新[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象。

    `refresh`{.descname} （ *instance*，*attribute\_names = None*，*lockmode = None* ） T5\> [¶ T6\>](#sqlalchemy.orm.session.Session.refresh "Permalink to this definition")
    :   过期并刷新给定实例上的属性。

        查询将发布到数据库，所有属性将使用其当前数据库值进行刷新。

        延迟加载的关系属性将保持延迟加载状态，以便实例范围内的刷新操作将立即跟随该属性的延迟加载。

        急切加载的关系属性将在单刷新操作中急切加载。

        请注意，高度隔离的事务将返回与先前在同一事务中读取的值相同的值，而不考虑该事务之外的数据库状态更改
        - 通常只有在非事务时才使用[`refresh()`](#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")正在进行的事务中发出ORM
        SQL语句，或者自动提交模式已打开。

        参数：

        -   **attribute\_names**
            [¶](#sqlalchemy.orm.session.Session.refresh.params.attribute_names)
            - 可选。指示要刷新的属性子集的可迭代字符串属性名称集合。
        -   **lockmode**[¶](#sqlalchemy.orm.session.Session.refresh.params.lockmode)
            – Passed to the [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
            as used by [`with_lockmode()`](query.html#sqlalchemy.orm.query.Query.with_lockmode "sqlalchemy.orm.query.Query.with_lockmode").

        也可以看看

        [Refreshing /
        Expiring](session_state_management.html#session-expire) -
        介绍材料

        [`Session.expire()`](#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")

        [`Session.expire_all()`](#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")

    `回滚 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   回滚正在进行的当前事务。

        如果没有交易正在进行，则此方法是转交。

        此方法回滚当前事务或嵌套事务，而不管子事务是否有效。直到第一次实际交易的所有子交易都关闭。当[`begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")被多次调用时发生子交换。

        也可以看看

        [Rolling Back](session_basics.html#session-rollback)

     `scalar`{.descname}(*clause*, *params=None*, *mapper=None*, *bind=None*, *\*\*kw*)[¶](#sqlalchemy.orm.session.Session.scalar "Permalink to this definition")
    :   像[`execute()`](#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")一样，但返回一个标量结果。

    `交易`{.descname} *=无* [¶](#sqlalchemy.orm.session.Session.transaction "Permalink to this definition")
    :   当前活动或不活动[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")。

*class* `sqlalchemy.orm.session。`{.descclassname} `SessionTransaction`{.descname} （ *session*，*parent = None*，*nested = False* ） [¶](#sqlalchemy.orm.session.SessionTransaction "Permalink to this definition")
:   一个[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")级别的事务。

    [`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")plain
    is a mostly behind-the-scenes object not normally referenced
    directly by application code. 它在多个[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象之间进行协调，为每个对象单独维护一个数据库事务，一次提交或回滚所有对象。它还提供可选的两阶段提交行为，可以增强此协调操作。

    [`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的[`Session.transaction`](#sqlalchemy.orm.session.Session.transaction "sqlalchemy.orm.session.Session.transaction")属性是指当前正在使用的[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")对象（如果有的话）。

    一个[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")在默认的`autocommit=False`模式下与一个[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联，并且没有数据库连接。由于[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")被调用来代表各种[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象发出SQL，因此相应的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")和将关联的[`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")添加到[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")对象内的集合中，成为由[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")维护的连接/事务对之一。

    The lifespan of the [`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")
    ends when the [`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit"),
    [`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")
    or [`Session.close()`](#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")
    methods are called. 此时，[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")删除与其父节点[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的关联。在`autocommit=False`模式下的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")会创建一个新的[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")来立即替换它，而[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")那么在`autocommit=True`模式下，在调用[`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法之前，它将保持不存在[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")

    [`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")行为的另一个细节是它能够“嵌套”。这意味着可以在存在[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")时调用[`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法，产生一个新的[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")来临时替换父[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")。当[`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")产生为嵌套时，它将自己分配给[`Session.transaction`](#sqlalchemy.orm.session.Session.transaction "sqlalchemy.orm.session.Session.transaction")属性。When
    it is ended via [`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
    or [`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback"),
    it restores its parent [`SessionTransaction`](#sqlalchemy.orm.session.SessionTransaction "sqlalchemy.orm.session.SessionTransaction")
    back onto the [`Session.transaction`{](#sqlalchemy.orm.session.Session.transaction "sqlalchemy.orm.session.Session.transaction")
    attribute. 行为实际上是一个堆栈，其中[`Session.transaction`](#sqlalchemy.orm.session.Session.transaction "sqlalchemy.orm.session.Session.transaction")指向当前堆栈的头部。

    The purpose of this stack is to allow nesting of
    [`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")
    or [`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
    calls in context with various flavors of [`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin").
    此嵌套行为适用于[`Session.begin_nested()`](#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")用于发出SAVEPOINT事务的情况，也用于产生所谓的“子事务”，该子事务允许一段代码使用开始/回滚/提交序列，而不管其封闭代码块是否已开始事务。无论是否显式调用或通过autoflush调用，[`flush()`](#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")方法都是“子事务”功能的主要使用者，因为它希望保证它在事务块内工作，而不管是否在调用方法时，[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")处于事务模式。

    也可以看看：

    [`Session.rollback()`](#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")

    [`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")

    [`Session.begin()`](#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")

    [`Session.begin_nested()`](#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")

    [`Session.is_active`{](#sqlalchemy.orm.session.Session.is_active "sqlalchemy.orm.session.Session.is_active")

    [`SessionEvents.after_commit()`](events.html#sqlalchemy.orm.events.SessionEvents.after_commit "sqlalchemy.orm.events.SessionEvents.after_commit")

    [`SessionEvents.after_rollback()`](events.html#sqlalchemy.orm.events.SessionEvents.after_rollback "sqlalchemy.orm.events.SessionEvents.after_rollback")

    [`SessionEvents.after_soft_rollback()`](events.html#sqlalchemy.orm.events.SessionEvents.after_soft_rollback "sqlalchemy.orm.events.SessionEvents.after_soft_rollback")

会话实用程序[¶](#session-utilites "Permalink to this headline")
---------------------------------------------------------------

` sqlalchemy.orm.session。 T0>  make_transient  T1> （ T2> 实例 T3> ） T4> ¶< / T5>`{.descclassname}
:   改变给定实例的状态，使其[transient](glossary.html#term-transient)。

    注意

    [`make_transient()`](#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")仅是高级用例的特例函数。

    假定给定的映射实例处于[persistent](glossary.html#term-persistent)或[detached](glossary.html#term-detached)状态。该函数将删除其与任何[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")及其[`InstanceState.identity`](internals.html#sqlalchemy.orm.state.InstanceState.identity "sqlalchemy.orm.state.InstanceState.identity")的关联。其效果是该对象的行为就像它是新构建的，除了保留在调用时加载的任何属性/集合值。如果由于使用[`Session.delete()`](#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")而删除了此对象，则[`InstanceState.deleted`](internals.html#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")标志也会重置。

    警告

    [`make_transient()`](#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")
    does **not** “unexpire” or otherwise eagerly load ORM-mapped
    attributes that are not currently loaded at the time the function is
    called. 这包括以下属性：

    -   通过[`Session.expire()`](#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")过期
    -   作为提交会话事务的自然效果，例如， [`Session.commit()`](#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
    -   通常是[lazy
        loaded](glossary.html#term-lazy-loaded)，但目前未加载
    -   是通过[Deferred Column
        Loading](loading_columns.html#deferred)“延期”，并且尚未加载
    -   在加载这个对象的查询中不存在，例如在连接表继承和其他场景中常见的那个。

    在调用[`make_transient()`](#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")之后，如上所述的卸载属性在访问时通常会解析为值`None`，或者面向集合的属性为空集合。由于对象是暂时的并且与任何数据库标识无关，因此将不再检索这些值。

    也可以看看

    [`make_transient_to_detached()`](#sqlalchemy.orm.session.make_transient_to_detached "sqlalchemy.orm.session.make_transient_to_detached")

` sqlalchemy.orm.session。 T0>  make_transient_to_detached  T1> （ T2> 实例 T3> ） T4> ¶< / T5>`{.descclassname}
:   使给定的瞬态实例[detached](glossary.html#term-detached)。

    注意

    [`make_transient_to_detached()`](#sqlalchemy.orm.session.make_transient_to_detached "sqlalchemy.orm.session.make_transient_to_detached")仅是高级用例的一种特例函数。

    给定实例上的所有属性历史记录将被重置，就像该实例是从查询中新加载的一样。缺少的属性将被标记为过期。需要的对象的主键属性将被设置为实例的“关键”。

    然后可以将该对象添加到会话中，也可以使用load =
    False标志进行合并，此时它看起来好像是以这种方式加载的，而不发出SQL。

    这是一个特殊的用例函数，它不同于对[`Session.merge()`](#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")的正常调用，因为给定的持久状态可以在没有任何SQL调用的情况下生成。

    版本0.9.5中的新功能

    也可以看看

    [`make_transient()`](#sqlalchemy.orm.session.make_transient "sqlalchemy.orm.session.make_transient")

`sqlalchemy.orm.session。 T0>  object_session  T1> （ T2> 实例 T3> ） T4> ¶< / T5>`{.descclassname}
:   返回给定实例所属的[`Session`](#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

    这与[`InstanceState.session`{](internals.html#sqlalchemy.orm.state.InstanceState.session "sqlalchemy.orm.state.InstanceState.session")访问器基本相同。详情请参阅该属性。

` sqlalchemy.orm.util。 T0>  was_deleted  T1> （ T2> 对象 T3> ） T4> ¶< / T5>`{.descclassname}
:   如果给定对象在会话刷新中被删除，则返回True。

    这与对象是否持久或分离无关。

    0.8.0版本中的新功能

    也可以看看

    [`InstanceState.was_deleted`{](internals.html#sqlalchemy.orm.state.InstanceState.was_deleted "sqlalchemy.orm.state.InstanceState.was_deleted")

属性和状态管理实用程序[¶](#attribute-and-state-management-utilities "Permalink to this headline")
-------------------------------------------------------------------------------------------------

这些函数由 SQLAlchemy 属性检测 API 提供，以提供处理实例，属性值和历史记录的详细界面。它们中的一些在构建事件监听器函数时很有用，比如[*ORM
Events*](events.html)中描述的那些函数。

`sqlalchemy.orm.util。 T0>  object_state  T1> （ T2> 实例 T3> ） T4> ¶< / T5>`{.descclassname}
:   给定一个对象，返回与该对象关联的[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")。

    如果未配置映射，则引发[`sqlalchemy.orm.exc.UnmappedInstanceError`](exceptions.html#sqlalchemy.orm.exc.UnmappedInstanceError "sqlalchemy.orm.exc.UnmappedInstanceError")。

    等效功能可通过[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数使用：

        inspect(instance)

    如果实例不是映射的一部分，则使用检查系统将引发[`sqlalchemy.exc.NoInspectionAvailable`](core_exceptions.html#sqlalchemy.exc.NoInspectionAvailable "sqlalchemy.exc.NoInspectionAvailable")。

 `sqlalchemy.orm.attributes.`{.descclassname}`del_attribute`{.descname}(*instance*, *key*)[¶](#sqlalchemy.orm.attributes.del_attribute "Permalink to this definition")
:   删除属性的值，激发历史事件。

    无论直接应用于该类的仪器如何，都可以使用该函数，即不需要描述符。自定义属性管理方案需要使用此方法来建立SQLAlchemy所理解的属性状态。

`sqlalchemy.orm.attributes。`{.descclassname} `get_attribute`{.descname} （ *实例*，*键* ） T5\> [¶ T6\>](#sqlalchemy.orm.attributes.get_attribute "Permalink to this definition")
:   获取属性的值，触发所需的可调用对象。

    无论直接应用于该类的仪器如何，都可以使用该函数，即不需要描述符。自定义属性管理方案需要使用此方法来使用SQLAlchemy所理解的属性状态。

 `sqlalchemy.orm.attributes.`{.descclassname}`get_history`{.descname}(*obj*, *key*, *passive=symbol('PASSIVE\_OFF')*)[¶](#sqlalchemy.orm.attributes.get_history "Permalink to this definition")
:   返回给定对象和属性键的[`History`](#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")记录。

    参数：

    -   **obj**[¶](#sqlalchemy.orm.attributes.get_history.params.obj) –
        an object whose class is instrumented by the attributes package.
    -   **键** [¶](#sqlalchemy.orm.attributes.get_history.params.key) -
        字符串属性名称。
    -   **passive**[¶](#sqlalchemy.orm.attributes.get_history.params.passive)
        – indicates loading behavior for the attribute if the value is
        not already present.
        这是一个bitflag属性，默认为符号`PASSIVE_OFF`，表示应发出所有必需的SQL。

 `sqlalchemy.orm.attributes.`{.descclassname}`init_collection`{.descname}(*obj*, *key*)[¶](#sqlalchemy.orm.attributes.init_collection "Permalink to this definition")
:   初始化集合属性并返回集合适配器。

    此函数用于提供直接访问以前卸载的属性的集合内部信息。例如。：

        collection_adapter = init_collection(someobject, 'elements')
        for elem in values:
            collection_adapter.append_without_event(elem)

    要获得更简单的方法，请参阅[`set_committed_value()`](#sqlalchemy.orm.attributes.set_committed_value "sqlalchemy.orm.attributes.set_committed_value")。

    obj是一个检测对象实例。为了向后兼容，直接接受InstanceState，但不推荐使用此用法。

`sqlalchemy.orm.attributes。`{.descclassname} `flag_modified`{.descname} （ *实例*，*键* ） T5\> [¶ T6\>](#sqlalchemy.orm.attributes.flag_modified "Permalink to this definition")
:   将实例上的属性标记为“已修改”。

    这将在实例上设置'修改'标志并为给定属性建立无条件更改事件。

` sqlalchemy.orm.attributes。 T0>  instance_state  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   为给定的映射对象返回[`InstanceState`](internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")。

    该函数是[`object_state()`](#sqlalchemy.orm.util.object_state "sqlalchemy.orm.util.object_state")的内部版本。[`object_state()`](#sqlalchemy.orm.util.object_state "sqlalchemy.orm.util.object_state")和/或[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数在这里是首选的，因为如果给定的对象未被映射，它们每个都会发出信息异常。

 `sqlalchemy.orm.instrumentation.`{.descclassname}`is_instrumented`{.descname}(*instance*, *key*)[¶](#sqlalchemy.orm.instrumentation.is_instrumented "Permalink to this definition")
:   如果给定实例的给定属性由属性包进行检测，则返回True。

    无论直接应用于该类的仪器如何，都可以使用该函数，即不需要描述符。plain

 `sqlalchemy.orm.attributes.`{.descclassname}`set_attribute`{.descname}(*instance*, *key*, *value*)[¶](#sqlalchemy.orm.attributes.set_attribute "Permalink to this definition")
:   设置属性的值，触发历史事件。

    无论直接应用于该类的仪器如何，都可以使用该函数，即不需要描述符。自定义属性管理方案需要使用此方法来建立SQLAlchemy所理解的属性状态。plain

 `sqlalchemy.orm.attributes.`{.descclassname}`set_committed_value`{.descname}(*instance*, *key*, *value*)[¶](#sqlalchemy.orm.attributes.set_committed_value "Permalink to this definition")
:   设置没有历史事件的属性的值。

    取消任何以前的历史记录。该值应该是标量保持属性的标量值，或者任何集合保持属性的迭代值。

    这与懒惰加载器关闭并从数据库加载其他数据时使用的基础方法相同。特别是，这种方法可以被应用程序代码使用，该代码通过单独的查询加载了附加属性或集合，然后可以将其附加到实例，就像它是其原始加载状态的一部分一样。

*class* `sqlalchemy.orm.attributes。`{.descclassname} `历史记录`{.descname} [¶](#sqlalchemy.orm.attributes.History "Permalink to this definition")
:   基础：[`sqlalchemy.orm.attributes.History`](#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")

    已添加，未更改和已删除值的三元组，表示在已检测属性上发生的更改。plain

    为对象的特定属性获取[`History`](#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")对象的最简单方法是使用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数：

        from sqlalchemy import inspect

        hist = inspect(myobject).attrs.myattribute.history

    每个元组成员都是一个可迭代的序列：

    -   `added` -
        添加到属性（第一个元组元素）的项目集合。
    -   `unchanged` -
        属性（第二个元组元素）上没有改变的项目的集合。
    -   `deleted` -
        已从属性（第三个元组元素）中删除的项的集合。

    `空 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果[`History`](#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")没有更改并且没有现有的未更改状态，则返回True。

    ` has_changes  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果[`History`](#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")发生变化，则返回True。

    ` non_added  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回未更改+删除的集合。

    ` non_deleted  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回添加的+的集合不变。

    `总和 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回添加的+不变+删除的集合。


