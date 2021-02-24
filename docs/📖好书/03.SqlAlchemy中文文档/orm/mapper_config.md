---
title: 映射器配置
date: 2021-02-20 22:41:43
permalink: /sqlalchemy/orm/mapper_config/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
映射器配置[¶](#mapper-configuration "Permalink to this headline")
=================================================================

本节介绍可用于映射器的各种配置模式。它假定你已经完成了[Object Relational
Tutorial](tutorial.html)并知道如何构建和使用基本的映射器和关系。

-   [映射类型](mapping_styles.html)
    -   [Declarative Mapping](mapping_styles.html#declarative-mapping)
    -   [Classical Mappings](mapping_styles.html#classical-mappings)
    -   [映射，对象的运行时反省](mapping_styles.html#runtime-introspection-of-mappings-objects)
-   [映射列和表达式](scalar_mapping.html)
    -   [映射表列](mapping_columns.html)
    -   [SQL Expressions as Mapped Attributes](mapped_sql_expr.html)
    -   [更改属性行为](mapped_attributes.html)
    -   [复合列类型](composites.html)
-   [映射类继承层次结构](inheritance.html)
    -   [连接表继承](inheritance.html#joined-table-inheritance)
    -   [Single Table
        Inheritance](inheritance.html#single-table-inheritance)
    -   [具体表继承](inheritance.html#concrete-table-inheritance)
    -   [使用与继承关系](inheritance.html#using-relationships-with-inheritance)
    -   [使用继承与声明](inheritance.html#using-inheritance-with-declarative)
-   [非传统映射](nonstandard_mappings.html)
    -   [将一个类映射到多个表](nonstandard_mappings.html#mapping-a-class-against-multiple-tables)
    -   [根据任意选择映射类](nonstandard_mappings.html#mapping-a-class-against-arbitrary-selects)
    -   [一个类的多个映射器](nonstandard_mappings.html#multiple-mappers-for-one-class)
-   [配置版本计数器](versioning.html)
    -   [简单版本计数](versioning.html#simple-version-counting)
    -   [自定义版本计数器/类型](versioning.html#custom-version-counters-types)
    -   [服务器端版本计数器](versioning.html#server-side-version-counters)
    -   [编程或条件版本计数器](versioning.html#programmatic-or-conditional-version-counters)
-   [类映射 API](mapping_api.html)

