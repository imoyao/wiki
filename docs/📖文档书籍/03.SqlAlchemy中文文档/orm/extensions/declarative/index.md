---
title: 声明
date: 2021-02-20 23:15:26
permalink: /sqlalchemy/orm/extensions/declarative/index/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
  - declarative
tags:
---
声明[¶ T0\>](#declarative "Permalink to this headline")
=======================================================

声明性系统是 SQLAlchemy
ORM 提供的通常使用的系统，用于定义映射到关系数据库表的类。但是，正如[Classical
Mappings](mapping_styles.html#classical-mapping)所述，Declarative 实际上是一系列在 SQLAlchemy
[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")结构之上的扩展。

虽然文档通常提到了大多数示例的声明，但以下各节将提供有关声明 API 如何与基本[`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")和 Core
[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")系统交互的详细信息，如以及如何使用 mixin 等系统构建复杂模式。

-   [基本使用](basic_use.html)
    -   [定义属性](basic_use.html#defining-attributes)
    -   [访问 MetaData](basic_use.html#accessing-the-metadata)
    -   [类构造函数](basic_use.html#class-constructor)
    -   [映射器配置](basic_use.html#mapper-configuration)
    -   [定义 SQL 表达式](basic_use.html#defining-sql-expressions)
-   [配置关系](relationships.html)
    -   [配置多对多关系](relationships.html#configuring-many-to-many-relationships)
-   [表格配置](table_config.html)
    -   [使用\_\_table
        \_\_](table_config.html#using-a-hybrid-approach-with-table)的混合方法
    -   [通过声明](table_config.html#using-reflection-with-declarative)使用反射
-   [继承配置](inheritance.html)
    -   [连接表继承](inheritance.html#joined-table-inheritance)
    -   [Single Table
        Inheritance](inheritance.html#single-table-inheritance)
    -   [具体表继承](inheritance.html#concrete-table-inheritance)
-   [Mixin and Custom Base Classes](mixins.html)
    -   [增加基础](mixins.html#augmenting-the-base)
    -   [在列中混合](mixins.html#mixing-in-columns)
    -   [在关系中混合](mixins.html#mixing-in-relationships)
    -   [在 deferred()，column\_property()和其他 MapperProperty 类中混合](mixins.html#mixing-in-deferred-column-property-and-other-mapperproperty-classes)
    -   [在关联代理和其他属性中混合](mixins.html#mixing-in-association-proxy-and-other-attributes)
    -   [用 mixins 控制表继承](mixins.html#controlling-table-inheritance-with-mixins)
    -   [在继承方案中的列中混合](mixins.html#mixing-in-columns-in-inheritance-scenarios)
    -   [结合来自多个 Mixin 的表/映射器参数](mixins.html#combining-table-mapper-arguments-from-multiple-mixins)
    -   [用 Mixin 创建索引](mixins.html#creating-indexes-with-mixins)
-   [Declarative API](api.html)
    -   [API 参考](api.html#api-reference)

