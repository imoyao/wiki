---
title: 映射列和表达式
date: 2021-02-20 22:41:46
permalink: /sqlalchemy/orm/scalar_mapping/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
映射列和表达式[¶](#mapping-columns-and-expressions "Permalink to this headline")
================================================================================

以下各节讨论如何将表列和SQL表达式映射到单个对象属性。

-   [映射表列](mapping_columns.html)
    -   [命名与属性名称不同的列](mapping_columns.html#naming-columns-distinctly-from-attribute-names)
    -   [自动化来自反映表的列命名方案](mapping_columns.html#automating-column-naming-schemes-from-reflected-tables)
    -   [命名带有前缀](mapping_columns.html#naming-all-columns-with-a-prefix)的所有列
    -   [使用column\_property作为列级选项](mapping_columns.html#using-column-property-for-column-level-options)
    -   [映射表列的子集](mapping_columns.html#mapping-a-subset-of-table-columns)
-   [SQL Expressions as Mapped Attributes](mapped_sql_expr.html)
    -   [使用混合](mapped_sql_expr.html#using-a-hybrid)
    -   [使用column\_property](mapped_sql_expr.html#using-column-property)
    -   [使用普通描述符](mapped_sql_expr.html#using-a-plain-descriptor)
-   [更改属性行为](mapped_attributes.html)
    -   [简单验证器](mapped_attributes.html#simple-validators)
    -   [使用描述符和混合](mapped_attributes.html#using-descriptors-and-hybrids)
    -   [同义词 T0\>](mapped_attributes.html#synonyms)
    -   [运营商自定义](mapped_attributes.html#operator-customization)
-   [复合列类型](composites.html)
    -   [在复合材料上追踪就地变异](composites.html#tracking-in-place-mutations-on-composites)
    -   [重新定义复合材料的比较操作](composites.html#redefining-comparison-operations-for-composites)

