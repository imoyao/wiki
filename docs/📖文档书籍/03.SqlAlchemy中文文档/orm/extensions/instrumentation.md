---
title: 替代类仪器
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/extensions/instrumentation/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
替代类仪器[¶](#module-sqlalchemy.ext.instrumentation "Permalink to this headline")
==================================================================================

可扩展的类仪器。

[`sqlalchemy.ext.instrumentation`](#module-sqlalchemy.ext.instrumentation "sqlalchemy.ext.instrumentation")包在 ORM 中提供了备用的类工具系统。类工具是指 ORM 如何在维护数据的类上放置属性，并跟踪对该数据的更改，以及安装在类上的事件挂钩。

注意

提供扩展包是为了与其他已经执行自己的仪器的对象管理包集成。它不适用于一般用途。

有关如何使用检测扩展的示例，请参阅示例[Attribute
Instrumentation](examples.html#examples-instrumentation)。

在版本 0.8 中更改： [`sqlalchemy.orm.instrumentation`](events.html#module-sqlalchemy.orm.instrumentation "sqlalchemy.orm.instrumentation")被拆分出来，以便将与非标准检测相关的所有功能移出到[`sqlalchemy.ext.instrumentation`](#module-sqlalchemy.ext.instrumentation "sqlalchemy.ext.instrumentation")导入时，模块将自身安装在[`sqlalchemy.orm.instrumentation`](events.html#module-sqlalchemy.orm.instrumentation "sqlalchemy.orm.instrumentation")中，以便生效，包括识别映射类上的`__sa_instrumentation_manager__`以及[`instrumentation_finders`](#sqlalchemy.ext.instrumentation.instrumentation_finders "sqlalchemy.ext.instrumentation.instrumentation_finders")
\>被用来确定类仪器的分辨率。

API 参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

`sqlalchemy.ext.instrumentation。`{.descclassname} `INSTRUMENTATION_MANAGER`{.descname} *='\_\_sa\_instrumentation\_manager \_\_'* [¶](#sqlalchemy.ext.instrumentation.INSTRUMENTATION_MANAGER "Permalink to this definition")
:   属性，在存在于映射类上时选择自定义检测。

    允许类指定一个稍微或非常不同的技术来跟踪对映射的属性和集合所做的更改。plainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplain

    在给定的对象继承层次结构中只允许使用一个工具实现。

    该属性的值必须是可调用的，并且将传递一个类对象。可调用函数必须返回以下之一：

    > -   InstrumentationManager或子类的实例
    > -   实现InstrumentationManager（TODO）的全部或部分对象，
    > -   一个可玩的字典，实现全部或部分上述（TODO）
    > -   一个ClassManager或子类的实例

    一旦[`sqlalchemy.ext.instrumentation`](#module-sqlalchemy.ext.instrumentation "sqlalchemy.ext.instrumentation")模块被导入后，通过SQLAlchemy工具解析来查询此属性。如果自定义查找器安装在全局instrumentation\_finders列表中，则它们可能会选择或不选择此属性。

*class* `sqlalchemy.orm.instrumentation。`{.descclassname} `InstrumentationFactory`{.descname} [¶](#sqlalchemy.orm.instrumentation.InstrumentationFactory "Permalink to this definition")
:   新的 ClassManager 实例的工厂。

 *class*`sqlalchemy.ext.instrumentation.`{.descclassname}`InstrumentationManager`{.descname}(*class\_*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager "Permalink to this definition")
:   用户定义的类工具扩展。

    [`InstrumentationManager`](#sqlalchemy.ext.instrumentation.InstrumentationManager "sqlalchemy.ext.instrumentation.InstrumentationManager")plainplainplainplainplainplainplainplainplainplainplainplainplainplainplain
    can be subclassed in order to change how class instrumentation
    proceeds.
    此类存在用于与其他对象管理框架集成的目的，这些对象管理框架将完全修改ORM的检测方法，并且不打算用于常规用法。要拦截类工具事件，请参阅[`InstrumentationEvents`](events.html#sqlalchemy.orm.events.InstrumentationEvents "sqlalchemy.orm.events.InstrumentationEvents")。

    这个类的API应该被认为是半稳定的，并且可能会随着新版本的发布而略有变化。

    Changed in version 0.8: [`InstrumentationManager`](#sqlalchemy.ext.instrumentation.InstrumentationManager "sqlalchemy.ext.instrumentation.InstrumentationManager")
    was moved from [`sqlalchemy.orm.instrumentation`](events.html#module-sqlalchemy.orm.instrumentation "sqlalchemy.orm.instrumentation")
    to [`sqlalchemy.ext.instrumentation`](#module-sqlalchemy.ext.instrumentation "sqlalchemy.ext.instrumentation").

    ` dict_getter  T0> （ T1> 类_  T2> ） T3> ¶ T4>`{.descname}
    :   

     `dispose`{.descname}(*class\_*, *manager*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.dispose "Permalink to this definition")
    :   

    `get_instance_dict`{.descname} （ *class\_*，*instance* ） [¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.get_instance_dict "Permalink to this definition")
    :   

     `initialize_instance_dict`{.descname}(*class\_*, *instance*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.initialize_instance_dict "Permalink to this definition")
    :   

     `install_descriptor`{.descname}(*class\_*, *key*, *inst*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.install_descriptor "Permalink to this definition")
    :   

     `install_member`{.descname}(*class\_*, *key*, *implementation*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.install_member "Permalink to this definition")
    :   

    ` install_state  T0> （ T1> 类_  T2>，实例 T3>，状态 T4> ） T5> ¶ T6>`{.descname}
    :   

     `instrument_attribute`{.descname}(*class\_*, *key*, *inst*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.instrument_attribute "Permalink to this definition")
    :   

    `instrument_collection_class`{.descname} （ *class\_*，*key*，*collection\_class* ） [¶ T6\>](#sqlalchemy.ext.instrumentation.InstrumentationManager.instrument_collection_class "Permalink to this definition")
    :   

     `manage`{.descname}(*class\_*, *manager*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.manage "Permalink to this definition")
    :   

    ` manager_getter  T0> （ T1> 类_  T2> ） T3> ¶ T4>`{.descname}
    :   

     `post_configure_attribute`{.descname}(*class\_*, *key*, *inst*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.post_configure_attribute "Permalink to this definition")
    :   

    `remove_state  tt> （ class_，instance ） ¶`{.descname}
    :   

    ` state_getter  T0> （ T1> 类_  T2> ） T3> ¶ T4>`{.descname}
    :   

     `uninstall_descriptor`{.descname}(*class\_*, *key*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.uninstall_descriptor "Permalink to this definition")
    :   

     `uninstall_member`{.descname}(*class\_*, *key*)[¶](#sqlalchemy.ext.instrumentation.InstrumentationManager.uninstall_member "Permalink to this definition")
    :   

`sqlalchemy.ext.instrumentation。`{.descclassname} `instrumentation_finders`{.descname} *= [＆lt；函数 find\_native\_user\_instrumentation\_hook at 0x7f43​​0c541230＆gt；]* [¶](#sqlalchemy.ext.instrumentation.instrumentation_finders "Permalink to this definition")
:   可扩展的可调用序列，返回仪器实现

    当一个类被注册时，每个可调用对象将被传递一个类对象。如果返回None，则会查询序列中的下一个查找器。否则，返回必须是符合sqlalchemy.ext.instrumentation.INSTRUMENTATION\_MANAGER相同准则的检测工厂。plainplainplainplainplainplain

    默认情况下，唯一的查找程序是find\_native\_user\_instrumentation\_hook，它搜索INSTRUMENTATION\_MANAGER。如果所有查找器都返回None，则使用标准的ClassManager工具。

*class* `sqlalchemy.ext.instrumentation。`{.descclassname} `ExtendedInstrumentationRegistry`{.descname} [¶](#sqlalchemy.ext.instrumentation.ExtendedInstrumentationRegistry "Permalink to this definition")
:   基础：[`sqlalchemy.orm.instrumentation.InstrumentationFactory`](#sqlalchemy.orm.instrumentation.InstrumentationFactory "sqlalchemy.orm.instrumentation.InstrumentationFactory")

    扩展[`InstrumentationFactory`](#sqlalchemy.orm.instrumentation.InstrumentationFactory "sqlalchemy.orm.instrumentation.InstrumentationFactory")以增加簿记，以适应多种类别的经理。plainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplainplain


