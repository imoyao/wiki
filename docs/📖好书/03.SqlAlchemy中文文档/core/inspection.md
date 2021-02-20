---
title: inspection
date: 2021-02-20 22:41:35
permalink: /pages/e748ea/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
运行时检测API [¶](#module-sqlalchemy.inspection "Permalink to this headline")
=============================================================================

检查模块提供了[`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数，该函数在Core和ORM中传递有关各种SQLAlchemy对象的运行时信息。

[`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数是SQLAlchemy的公共API的入口点，用于查看内存中对象的配置和构造。根据传递给[`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")的对象的类型，返回值可以是提供已知接口的相关对象，或者在许多情况下它将返回对象本身。

[`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")的基本原理是双重的。One
is that it replaces the need to be aware of a large variety of
“information getting” functions in SQLAlchemy, such as
[`Inspector.from_engine()`](reflection.html#sqlalchemy.engine.reflection.Inspector.from_engine "sqlalchemy.engine.reflection.Inspector.from_engine"),
[`orm.attributes.instance_state()`](orm_session_api.html#sqlalchemy.orm.attributes.instance_state "sqlalchemy.orm.attributes.instance_state"),
[`orm.class_mapper()`](orm_mapping_api.html#sqlalchemy.orm.class_mapper "sqlalchemy.orm.class_mapper"),
and others. 另一个原因是，[`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")的返回值保证服从一个记录的API，因此允许构建在SQLAlchemy配置之上的第三方工具以前向兼容的方式构建。

0.8版中的新功能从版本0.8开始引入[`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")系统。

 `sqlalchemy.inspection.`{.descclassname}`inspect`{.descname}(*subject*, *raiseerr=True*)[¶](#sqlalchemy.inspection.inspect "Permalink to this definition")
:   为给定的目标生成检查对象。

    在某些情况下，返回的值可能与给定的对象相同，例如传递[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象。在其他情况下，它将是给定对象的注册检查类型的实例，例如，如果传递[`engine.Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，则返回一个[`Inspector`](reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")对象。

    参数：

    -   **subject**[¶](#sqlalchemy.inspection.inspect.params.subject) –
        the subject to be inspected.
    -   **raiseerr**[¶](#sqlalchemy.inspection.inspect.params.raiseerr)
        – When `True`, if the given subject does not
        correspond to a known SQLAlchemy inspected type,
        [`sqlalchemy.exc.NoInspectionAvailable`{.xref .py .py-class
        .docutils
        .literal}](exceptions.html#sqlalchemy.exc.NoInspectionAvailable "sqlalchemy.exc.NoInspectionAvailable")
        is raised. 如果`False`{.docutils
        .literal}，则返回`None`。

可用的检查目标[¶](#available-inspection-targets "Permalink to this headline")
-----------------------------------------------------------------------------

以下列出了许多最常见的检查目标。

-   [`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")（即[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")）
    - 返回一个[`Inspector`](reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")对象。
-   [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
    - all SQL expression components, including [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
    [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
    serve as their own inspection objects, meaning any of these objects
    passed to [`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")
    return themselves.
-   `object` - 给定的对象将由ORM检查映射 -
    如果是，则返回表示对象映射状态的[`InstanceState`](orm_internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")。[`InstanceState`](orm_internals.html#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")还通过[`AttributeState`](orm_internals.html#sqlalchemy.orm.state.AttributeState "sqlalchemy.orm.state.AttributeState")接口提供对每个属性状态的访问，以及通过[`History`](orm_session_api.html#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")访问任何属性的每次刷新“历史记录”目的。
-   `type`（即类） - 给定的类将由ORM检查映射 -
    如果是，则返回该类的[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。
-   mapped attribute - passing a mapped attribute to [`inspect()`](#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect"),
    such as `inspect(MyClass.some_attribute)`,
    returns a [`QueryableAttribute`](orm_internals.html#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")
    object, which is the [descriptor](glossary.html#term-descriptor)
    associated with a mapped class. This descriptor refers to a
    [`MapperProperty`](orm_internals.html#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty"),
    which is usually an instance of [`ColumnProperty`](orm_internals.html#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")
    or [`RelationshipProperty`](orm_internals.html#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty"),
    via its [`QueryableAttribute.property`{](orm_internals.html#sqlalchemy.orm.attributes.QueryableAttribute.property "sqlalchemy.orm.attributes.QueryableAttribute.property")
    attribute.
-   [`AliasedClass`](orm_query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")
    - 返回一个[`AliasedInsp`](orm_query.html#sqlalchemy.orm.util.AliasedInsp "sqlalchemy.orm.util.AliasedInsp")对象。

