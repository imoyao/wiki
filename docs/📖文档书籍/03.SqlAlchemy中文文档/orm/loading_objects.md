---
title: 加载对象
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/loading_objects/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
加载对象[¶](#loading-objects "Permalink to this headline")
==========================================================

有关映射对象的一般加载的注释和功能。

有关查询 SQLAlchemy ORM 的深入介绍，请参阅[Object Relational
Tutorial](tutorial.html)。

-   [加载列](loading_columns.html)
    -   [延期的列载入](loading_columns.html#deferred-column-loading)
    -   [列包](loading_columns.html#column-bundles)
-   [Relationship Loading Techniques](loading_relationships.html)
    -   [使用 Loader 策略：延迟加载，急切加载](loading_relationships.html#using-loader-strategies-lazy-loading-eager-loading)
    -   [订购的重要性](loading_relationships.html#the-importance-of-ordering)
    -   [沿路径加载](loading_relationships.html#loading-along-paths)
    -   [默认加载策略](loading_relationships.html#default-loading-strategies)
    -   [每个实体的默认加载策略](loading_relationships.html#per-entity-default-loading-strategies)
    -   [渴望加载的禅宗](loading_relationships.html#the-zen-of-eager-loading)
    -   [要使用什么类型的装载](loading_relationships.html#what-kind-of-loading-to-use)
    -   [将显式连接/语句路由到预先加载的集合](loading_relationships.html#routing-explicit-joins-statements-into-eagerly-loaded-collections)
    -   [创建自定义加载规则](loading_relationships.html#creating-custom-load-rules)
    -   [Relationship Loader
        API](loading_relationships.html#relationship-loader-api)
-   [构造函数和对象初始化](constructors.html)
-   [查询 API](query.html)
    -   [查询对象](query.html#the-query-object)
    -   [ORM-Specific Query
        Constructs](query.html#orm-specific-query-constructs)

