---
title: 关系配置
date: 2021-02-20 22:41:42
permalink: /sqlalchemy/orm/extensions/declarative/relationships/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
  - extensions
  - declarative
tags:
  - 
---
关系配置[¶](#relationship-configuration "Permalink to this headline")
=====================================================================

本节介绍[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")函数并深入讨论其用法。有关关系的介绍，请从[Object
Relational Tutorial](tutorial.html)开始，然后进入[Building a
Relationship](tutorial.html#orm-tutorial-relationship)。

-   [基本关系模式](basic_relationships.html)
    -   [一对多](basic_relationships.html#one-to-many)
    -   [多对一](basic_relationships.html#many-to-one)
    -   [一对一](basic_relationships.html#one-to-one)
    -   [多对多](basic_relationships.html#many-to-many)
    -   [关联对象](basic_relationships.html#association-object)
-   [Adjacency List Relationships](self_referential.html)
    -   [复合相邻表](self_referential.html#composite-adjacency-lists)
    -   [Self-Referential Query
        Strategies](self_referential.html#self-referential-query-strategies)
    -   [配置自引用预加载](self_referential.html#configuring-self-referential-eager-loading)
-   [将关系与Backref链接](backref.html)
    -   [后退参数](backref.html#backref-arguments)
    -   [单向后退](backref.html#one-way-backrefs)
-   [配置关系连接的方式](join_conditions.html)
    -   [处理多个加入路径](join_conditions.html#handling-multiple-join-paths)
    -   [指定替代联接条件](join_conditions.html#specifying-alternate-join-conditions)
    -   [创建自定义外部条件](join_conditions.html#creating-custom-foreign-conditions)
    -   [在连接条件](join_conditions.html#using-custom-operators-in-join-conditions)中使用自定义运算符
    -   [重叠外键](join_conditions.html#overlapping-foreign-keys)
    -   [Non-relational Comparisons / Materialized
        Path](join_conditions.html#non-relational-comparisons-materialized-path)
    -   [自我引用的多对多关系](join_conditions.html#self-referential-many-to-many-relationship)
    -   [复合“次要”联接](join_conditions.html#composite-secondary-joins)
    -   [与非主要映射器的关系](join_conditions.html#relationship-to-non-primary-mapper)
    -   [构建启用查询的属性](join_conditions.html#building-query-enabled-properties)
-   [收集配置和技巧](collections.html)
    -   [处理大集合](collections.html#working-with-large-collections)
    -   [自定义收集访问](collections.html#customizing-collection-access)
    -   [自定义集合实现](collections.html#custom-collection-implementations)
    -   [收集内部](collections.html#collection-internals)
-   [特殊关系持久性模式](relationship_persistence.html)
    -   [指向自己的行/相互依赖的行](relationship_persistence.html#rows-that-point-to-themselves-mutually-dependent-rows)
    -   [Mutable Primary Keys / Update
        Cascades](relationship_persistence.html#mutable-primary-keys-update-cascades)
-   [关系API](relationship_api.html)

