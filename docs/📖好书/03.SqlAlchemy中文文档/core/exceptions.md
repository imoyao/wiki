---
title: ORM 异常
date: 2021-02-20 22:41:34
permalink: /sqlalchemy/core/exceptions/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
ORM 异常[¶](#module-sqlalchemy.orm.exc "Permalink to this headline")
===================================================================

SQLAlchemy ORM 异常。

`sqlalchemy.orm.exc。 T0>  ConcurrentModificationError  T1> ¶ T2>`{.descclassname}
:   [`StaleDataError`](#sqlalchemy.orm.exc.StaleDataError "sqlalchemy.orm.exc.StaleDataError")的别名

*异常* `sqlalchemy.orm.exc。`{.descclassname} `DetachedInstanceError`{.descname} [¶](#sqlalchemy.orm.exc.DetachedInstanceError "Permalink to this definition")
:   尝试访问分离的映射实例上的卸载属性。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `FlushError`{.descname} [¶](#sqlalchemy.orm.exc.FlushError "Permalink to this definition")
:   flush()期间检测到无效条件。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `MultipleResultsFound`{.descname} [¶](#sqlalchemy.orm.exc.MultipleResultsFound "Permalink to this definition")
:   单个数据库结果是必需的，但不止一个被发现。

 `sqlalchemy.orm.exc.`{.descclassname}`NO_STATE`{.descname}*= (\<type 'exceptions.AttributeError'\>, \<type 'exceptions.KeyError'\>)*[¶](#sqlalchemy.orm.exc.NO_STATE "Permalink to this definition")
:   工具实现可能引发的异常类型。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `NoResultFound`{.descname} [¶](#sqlalchemy.orm.exc.NoResultFound "Permalink to this definition")
:   数据库结果是必需的，但没有找到。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `ObjectDeletedError`{.descname} （ *状态*，*msg =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.exc.ObjectDeletedError "Permalink to this definition")*
:   刷新操作无法检索与对象的已知主键标识相对应的数据库行。

    刷新操作在对象上访问过期属性或使用[`Query.get()`](query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")检索检索到的对象时检测为过期。基于主键为目标行发出SELECT；如果没有行被返回，则引发此异常。plain

    这个异常的真正含义就是，不存在与持久对象关联的主键标识符的行。该行可能已被删除，或者在某些情况下主键已更新为新值，而不在ORM的目标对象管理之外。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `ObjectDereferencedError`{.descname} [¶](#sqlalchemy.orm.exc.ObjectDereferencedError "Permalink to this definition")
:   由于垃圾收集对象，操作无法完成。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `StaleDataError`{.descname} [¶](#sqlalchemy.orm.exc.StaleDataError "Permalink to this definition")
:   遇到数据库状态的操作未被记录。

    导致这种情况发生的条件包括：plain

    -   刷新可能试图更新或删除行，并且在UPDATE或DELETE语句期间意外数量的行被匹配。请注意，当使用version\_id\_col时，UPDATE或DELETE语句中的行也会与当前已知的版本标识符进行匹配。

    -   具有版本\_id\_col的映射对象被刷新，并且从数据库返回的版本号与对象本身的版本号不匹配。

    -   一个对象与其父对象分离，但是该对象先前被附加到了垃圾收集的不同父对象身上，并且如果新父对象实际上是最近的“父对象”，则不能做出决定。

        New in version 0.7.4.

*异常* `sqlalchemy.orm.exc。`{.descclassname} `UnmappedClassError`{.descname} （ *cls*，*msg =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.exc.UnmappedClassError "Permalink to this definition")*
:   为未知类别请求映射操作。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `UnmappedColumnError`{.descname} [¶](#sqlalchemy.orm.exc.UnmappedColumnError "Permalink to this definition")
:   在未知列上请求映射操作。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `UnmappedError`{.descname} [¶](#sqlalchemy.orm.exc.UnmappedError "Permalink to this definition")
:   基础包含预期映射不存在的异常。

*异常* `sqlalchemy.orm.exc。`{.descclassname} `UnmappedInstanceError`{.descname} （ *obj*，*msg =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.exc.UnmappedInstanceError "Permalink to this definition")*
:   为未知实例请求映射操作。


