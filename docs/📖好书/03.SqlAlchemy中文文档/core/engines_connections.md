---
title: 引擎和连接使用
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/core/enines_connections/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
引擎和连接使用[¶](#engine-and-connection-use "Permalink to this headline")
==========================================================================

-   [引擎配置](engines.html)
    -   [支持的数据库](engines.html#supported-databases)
    -   [数据库网址](engines.html#database-urls)
    -   [引擎创建 API](engines.html#engine-creation-api)
    -   [池 T0\>](engines.html#pooling)
    -   [自定义 DBAPI 连接()参数](engines.html#custom-dbapi-connect-arguments)
    -   [配置日志记录](engines.html#configuring-logging)
-   [使用引擎和连接](connections.html)
    -   [基本用法](connections.html#basic-usage)
    -   [使用交易](connections.html#using-transactions)
    -   [了解自动提交](connections.html#understanding-autocommit)
    -   [无连接执行，隐式执行](connections.html#connectionless-execution-implicit-execution)
    -   [架构名称的翻译](connections.html#translation-of-schema-names)
    -   [发动机处理](connections.html#engine-disposal)
    -   [使用 Threadlocal 执行策略](connections.html#using-the-threadlocal-execution-strategy)
    -   [使用原始 DBAPI 连接](connections.html#working-with-raw-dbapi-connections)
    -   [注册新方言](connections.html#registering-new-dialects)
    -   [连接/引擎 API](connections.html#connection-engine-api)
-   [连接池](pooling.html)
    -   [连接池配置](pooling.html#connection-pool-configuration)
    -   [切换池实现](pooling.html#switching-pool-implementations)
    -   [使用自定义连接功能](pooling.html#using-a-custom-connection-function)
    -   [构建池](pooling.html#constructing-a-pool)
    -   [池事件](pooling.html#pool-events)
    -   [处理断开连接](pooling.html#dealing-with-disconnects)
    -   [使用连接池和多重处理](pooling.html#using-connection-pools-with-multiprocessing)
    -   [API 文档 -
        可用的池实现](pooling.html#api-documentation-available-pool-implementations)
    -   [Pooling Plain DB-API
        Connections](pooling.html#pooling-plain-db-api-connections)
-   [核心活动](events.html)
    -   [连接池事件](events.html#connection-pool-events)
    -   [SQL Execution and Connection
        Events](events.html#sql-execution-and-connection-events)
    -   [架构事件](events.html#schema-events)

