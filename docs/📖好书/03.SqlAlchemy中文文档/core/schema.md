---
title: schema
date: 2021-02-20 22:41:35
permalink: /pages/9365b9/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
模式定义语言[¶](#module-sqlalchemy.schema "Permalink to this headline")
=======================================================================

本节引用描述和检查数据库模式的全面系统SQLAlchemy **模式元数据**。

SQLAlchemy的查询和对象映射操作的核心由*数据库元数据*支持，它由描述表和其他模式级对象的Python对象组成。这些对象是三种主要操作类型的核心
-
发出CREATE和DROP语句（称为*DDL*），构建SQL查询以及表达关于数据库中已存在的结构的信息。

数据库元数据可以通过使用诸如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")，[`ForeignKey`](constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")和[`Sequence`](defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")，所有这些都是从`sqlalchemy.schema`包导入的。它也可以由SQLAlchemy使用名为*reflection*的进程生成，这意味着您从一个对象（如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")）开始，为其指定一个名称，然后指示SQLAlchemy加载与特定发动机源相关的所有附加信息。

SQLAlchemy的数据库元数据结构的一个关键特性是它们被设计成用于与真实DDL非常相似的*声明式*风格。因此，对于那些在创建真正的模式生成脚本方面有一定背景的人来说，他们最直观。

-   [用MetaData描述数据库](metadata.html)
    -   [访问表格和列](metadata.html#accessing-tables-and-columns)
    -   [创建和删除数据库表](metadata.html#creating-and-dropping-database-tables)
    -   [通过迁移更改模式](metadata.html#altering-schemas-through-migrations)
    -   [指定模式名称](metadata.html#specifying-the-schema-name)
    -   [后端特定选项](metadata.html#backend-specific-options)
    -   [Column, Table, MetaData
        API](metadata.html#column-table-metadata-api)
-   [反映数据库对象](reflection.html)
    -   [覆盖反射列](reflection.html#overriding-reflected-columns)
    -   [反映视图](reflection.html#reflecting-views)
    -   [一次反映所有表格](reflection.html#reflecting-all-tables-at-once)
    -   [使用检查器](reflection.html#fine-grained-reflection-with-inspector)进行细粒度反射
    -   [反射的限制](reflection.html#limitations-of-reflection)
-   [Column Insert/Update Defaults](defaults.html)
    -   [标量默认值](defaults.html#scalar-defaults)
    -   [Python执行的函数](defaults.html#python-executed-functions)
    -   [SQL Expressions](defaults.html#sql-expressions)
    -   [服务器端默认值](defaults.html#server-side-defaults)
    -   [触发列](defaults.html#triggered-columns)
    -   [定义序列](defaults.html#defining-sequences)
    -   [默认对象API](defaults.html#default-objects-api)
-   [定义约束和索引](constraints.html)
    -   [定义外键](constraints.html#defining-foreign-keys)
    -   [UNIQUE约束](constraints.html#unique-constraint)
    -   [检查约束](constraints.html#check-constraint)
    -   [PRIMARY KEY
        Constraint](constraints.html#primary-key-constraint)
    -   [在使用声明性ORM扩展](constraints.html#setting-up-constraints-when-using-the-declarative-orm-extension)时设置约束
    -   [配置约束命名约定](constraints.html#configuring-constraint-naming-conventions)
    -   [约束API](constraints.html#constraints-api)
    -   [索引 T0\>](constraints.html#indexes)
    -   [索引API](constraints.html#index-api)
-   [定制DDL](ddl.html)
    -   [自定义DDL](ddl.html#custom-ddl)
    -   [控制DDL序列](ddl.html#controlling-ddl-sequences)
    -   [使用内建的DDLElement
        Classes](ddl.html#using-the-built-in-ddlelement-classes)
    -   [DDL表达式构造API](ddl.html#ddl-expression-constructs-api)

