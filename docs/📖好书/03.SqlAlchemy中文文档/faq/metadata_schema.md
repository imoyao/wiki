---
title: MetaData / Schema
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/faq/metadata_schema/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - faq
tags:
---
MetaData / Schema [¶](#metadata-schema "Permalink to this headline")
====================================================================

-   [当我说`table.drop()` /
    `metadata.drop_all()`](#my-program-is-hanging-when-i-say-table-drop-metadata-drop-all)时，
-   [SQLAlchemy 是否支持 ALTER TABLE，CREATE VIEW，CREATE
    TRIGGER，架构升级功能？](#does-sqlalchemy-support-alter-table-create-view-create-trigger-schema-upgrade-functionality)
-   [我如何按照依赖关系的顺序对 Table 对象进行排序？](#how-can-i-sort-table-objects-in-order-of-their-dependency)
-   [如何将 CREATE TABLE / DROP
    TABLE 输出作为字符串？](#how-can-i-get-the-create-table-drop-table-output-as-a-string)
-   [我如何子类化表/列来提供某些行为/配置？](#how-can-i-subclass-table-column-to-provide-certain-behaviors-configurations)

当我说`table.drop()` / `metadata.drop_all()` [¶](#my-program-is-hanging-when-i-say-table-drop-metadata-drop-all "Permalink to this headline")时
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

这通常对应于两个条件：1.使用对表锁确实严格的 PostgreSQL，以及 2.您的连接仍处于打开状态，其中包含表中的锁，并且与用于 DROP 语句的连接不同。下面是最小版本的模式：

    connection = engine.connect()plainplainplain
    result = connection.execute(mytable.select())

    mytable.drop(engine)

以上，连接池连接仍被检出；此外，上面的结果对象还保持与此连接的链接。如果使用“隐式执行”，则结果将保持此连接处于打开状态，直到结果对象关闭或所有行耗尽。

对`mytable.drop(engine)`的调用会尝试在从[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")采购的第二个连接上发出 DROP
TABLE，该连接将被锁定。

解决方法是在发出 DROP TABLE 之前关闭所有连接：

    connection = engine.connect()plainplainplainplain
    result = connection.execute(mytable.select())

    # fully read result sets
    result.fetchall()

    # close connections
    connection.close()

    # now locks are removed
    mytable.drop(engine)

SQLAlchemy 是否支持 ALTER TABLE，CREATE VIEW，CREATE TRIGGER，架构升级功能？[¶](#does-sqlalchemy-support-alter-table-create-view-create-trigger-schema-upgrade-functionality "Permalink to this headline")
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

一般 ALTER 支持不直接出现在 SQLAlchemy 中。对于特殊的 DDL，可以使用[`DDL`](core_ddl.html#sqlalchemy.schema.DDL "sqlalchemy.schema.DDL")和相关的结构。有关此主题的讨论，请参阅`core_ddl`。

更全面的选择是使用模式迁移工具，例如 Alembic 或 SQLAlchemy-Migrate；请参阅[Altering
Schemas through
Migrations](core_metadata.html#schema-migrations)以便进行讨论。

我如何按照依赖关系的顺序对 Table 对象进行排序？[¶](#how-can-i-sort-table-objects-in-order-of-their-dependency "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------------------

这可以通过[`MetaData.sorted_tables`](core_metadata.html#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")函数使用：

    metadata = MetaData()plainplainplainplainplainplain
    # ... add Table objects to metadata
    ti = metadata.sorted_tables:
    for t in ti:
        print(t)

我怎样才能将 CREATE TABLE / DROP TABLE 输出作为字符串？[¶](#how-can-i-get-the-create-table-drop-table-output-as-a-string "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------------------------------------------

现代 SQLAlchemy 具有代表 DDL 操作的子句结构。这些可以像任何其他 SQL 表达式一样呈现为字符串：

    from sqlalchemy.schema import CreateTable

    print(CreateTable(mytable))

要获取特定于某个引擎的字符串：

    print(CreateTable(mytable).compile(engine))plainplainplain

还有一种特殊的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")形式，可以让您使用以下配方转储整个元数据创建序列：

    def dump(sql, *multiparams, **params):plainplainplainplain
        print(sql.compile(dialect=engine.dialect))
    engine = create_engine('postgresql://', strategy='mock', executor=dump)
    metadata.create_all(engine, checkfirst=False)

[Alembic](https://bitbucket.org/zzzeek/alembic)工具还支持“离线”SQL 生成模式，可将数据库迁移呈现为 SQL 脚本。

我怎么可以继承 Table / Column 来提供某些行为/配置？[¶](#how-can-i-subclass-table-column-to-provide-certain-behaviors-configurations "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------------------------------

[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")不适合直接子类化。但是，有一些简单的方法可以使用创建函数获取构建行为，以及与模式对象之间的关联有关的行为，例如约束约定或使用附件事件的命名约定。在[命名约定](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/NamingConventions)中可以看到许多这些技术的一个例子。
