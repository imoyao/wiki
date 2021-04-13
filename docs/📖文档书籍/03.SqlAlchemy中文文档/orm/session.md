---
title: 使用会话
date: 2021-02-20 22:41:46
permalink: /sqlalchemy/orm/session/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
使用会话[¶](#module-sqlalchemy.orm.session "Permalink to this headline")
========================================================================

[`orm.mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数和[`declarative`](extensions_declarative_api.html#module-sqlalchemy.ext.declarative "sqlalchemy.ext.declarative")扩展是 ORM 的主要配置接口。一旦配置了映射，持久化操作的主要用法界面就是[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

-   [会话基础](session_basics.html)
    -   [会话是做什么的？](session_basics.html#what-does-the-session-do)
    -   [获得会话](session_basics.html#getting-a-session)
    -   [会话常见问题](session_basics.html#session-frequently-asked-questions)
    -   [使用会话的基础](session_basics.html#basics-of-using-a-session)
-   [状态管理](session_state_management.html)
    -   [Quickie 介绍对象状态](session_state_management.html#quickie-intro-to-object-states)
    -   [会话属性](session_state_management.html#session-attributes)
    -   [会话参照行为](session_state_management.html#session-referencing-behavior)
    -   [合并 T0\>](session_state_management.html#merging)
    -   [清除日期 T0\>](session_state_management.html#expunging)
    -   [刷新/过期](session_state_management.html#refreshing-expiring)
-   [级联 T0\>](cascades.html)
    -   [保存更新 T0\>](cascades.html#save-update)
    -   [删除 T0\>](cascades.html#delete)
    -   [删除-孤儿 T0\>](cascades.html#delete-orphan)
    -   [合并 T0\>](cascades.html#merge)
    -   [刷新-到期 T0\>](cascades.html#refresh-expire)
    -   [则清除 T0\>](cascades.html#expunge)
    -   [在 Backrefs 上控制级联](cascades.html#controlling-cascade-on-backrefs)
-   [Transactions and Connection Management](session_transaction.html)
    -   [管理交易](session_transaction.html#managing-transactions)
    -   [将会话加入外部事务（例如测试套件）](session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
-   [Additional Persistence Techniques](persistence_techniques.html)
    -   [将 SQL 插入/更新表达式嵌入到](persistence_techniques.html#embedding-sql-insert-update-expressions-into-a-flush)中
    -   [在会话中使用 SQL 表达式](persistence_techniques.html#using-sql-expressions-with-sessions)
    -   [在具有默认](persistence_techniques.html#forcing-null-on-a-column-with-a-default)的列上强制 NULL
    -   [分区策略](persistence_techniques.html#partitioning-strategies)
    -   [Bulk Operations](persistence_techniques.html#bulk-operations)
-   [上下文/线程本地会话](contextual.html)
    -   [隐式方法访问](contextual.html#implicit-method-access)
    -   [线程本地作用域](contextual.html#thread-local-scope)
    -   [在 Web 应用程序中使用线程本地作用域](contextual.html#using-thread-local-scope-with-web-applications)
    -   [使用自定义创建的范围](contextual.html#using-custom-created-scopes)
    -   [Contextual Session API](contextual.html#contextual-session-api)
-   [使用事件跟踪对象和会话更改](session_events.html)
    -   [持久性事件](session_events.html#persistence-events)
    -   [对象生命周期事件](session_events.html#object-lifecycle-events)
    -   [交易事件](session_events.html#transaction-events)
    -   [属性更改事件](session_events.html#attribute-change-events)
-   [会话 API](session_api.html)
    -   [Session and
        sessionmaker()](session_api.html#session-and-sessionmaker)
    -   [会话实用程序](session_api.html#session-utilites)
    -   [属性和状态管理实用程序](session_api.html#attribute-and-state-management-utilities)

