---
title: PostgreSQL
date: 2021-02-20 22:41:37
permalink: /sqlalchemy/dialects/postgresql/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - dialects
tags:
  - 
---
PostgreSQL [¶ T0\>](#module-sqlalchemy.dialects.postgresql.base "Permalink to this headline")
===============================================================================================

支持 PostgreSQL 数据库。

DBAPI支持[¶](#dialect-postgresql "Permalink to this headline")
--------------------------------------------------------------

以下dialect / DBAPI选项可用。请参阅各个DBAPI部分的连接信息。

-   [psycopg2 T0\>](#module-sqlalchemy.dialects.postgresql.psycopg2)
-   [pg8000 T0\>](#module-sqlalchemy.dialects.postgresql.pg8000)
-   [psycopg2cffi
    T0\>](#module-sqlalchemy.dialects.postgresql.psycopg2cffi)
-   [PY-的PostgreSQL
    T0\>](#module-sqlalchemy.dialects.postgresql.pypostgresql)
-   [pygresql T0\>](#module-sqlalchemy.dialects.postgresql.pygresql)
-   Jython 的[zxJDBC](#module-sqlalchemy.dialects.postgresql.zxjdbc)

序列/ SERIAL [¶ T0\>](#sequences-serial "Permalink to this headline")
---------------------------------------------------------------------

PostgreSQL 支持序列，SQLAlchemy 使用这些作为为基于整数的主键列创建新的主键值的默认方式。在创建表时，SQLAlchemy 将为基于整数的主键列发布`SERIAL`数据类型，从而生成对应于该列的序列和服务器端默认值。

要指定要用于主键生成的特定命名序列，请使用[`Sequence()`](core_defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")结构：

    Table('sometable', metadata,plain
            Column('id', Integer, Sequence('some_id_seq'), primary_key=True)
        )

当 SQLAlchemy 发出单个 INSERT 语句时，为了履行使“最后一个插入标识符”可用的合同，将一个 RETURNING 子句添加到 INSERT 语句中，该语句指定在语句完成后应该返回主键列。只有在使用 Postgresql
8.2 或更高版本时才会执行 RETURNING 功能。作为后备方法，无论是通过`SERIAL`明确指定还是隐式指定，序列都是事先独立执行的，返回的值将在后续插入中使用。请注意，当使用“executemany”语义执行[`insert()`](core_dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")结构时，“最后插入的标识符”功能不适用；在这种情况下，不会发射 RETURNING 子句，也不会预先执行序列。

要在默认情况下强制使用RETURNING，请将标志`implicit_returning=False`指定为[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")。

事务隔离级别[¶](#transaction-isolation-level "Permalink to this headline")
--------------------------------------------------------------------------

All Postgresql dialects support setting of transaction isolation level
both via a dialect-specific parameter
[`create_engine.isolation_level`](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")
accepted by [`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine"),
as well as the [`Connection.execution_options.isolation_level`(core_connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level "sqlalchemy.engine.Connection.execution_options")
argument as passed to [`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options").
When using a non-psycopg2 dialect, this feature works by issuing the
command
`SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL <level>` for each new connection.
对于特殊的 AUTOCOMMIT 隔离级别，使用了特定于 DBAPI 的技术。

使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")设置隔离级别：

    engine = create_engine(plain
        "postgresql+pg8000://scott:tiger@localhost/test",
        isolation_level="READ UNCOMMITTED"
    )

要设置使用每个连接执行选项：

    connection = engine.connect()plain
    connection = connection.execution_options(
        isolation_level="READ COMMITTED"
    )

`isolation_level`的有效值包括：

-   `READ COMMITTED`
-   `READ UNCOMMITTED`
-   `REPEATABLE READ`
-   `SERIALIZABLE`
-   `AUTOCOMMIT` - on psycopg2 / pg8000 only

也可以看看

[Psycopg2 Transaction Isolation Level](#psycopg2-isolation-level)

[pg8000 Transaction Isolation Level](#pg8000-isolation-level)

Remote-Schema Table Introspection 和 Postgresql search\_path [¶](#remote-schema-table-introspection-and-postgresql-search-path "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------------------------------------------------

Postgresql 方言可以反映来自任何模式的表格。[`Table.schema`(core_metadata.html#sqlalchemy.schema.Table.params.schema "sqlalchemy.schema.Table")参数或者[`MetaData.reflect.schema`](core_metadata.html#sqlalchemy.schema.MetaData.reflect.params.schema "sqlalchemy.schema.MetaData.reflect")参数可确定将为该表搜索哪个模式。反映的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象将在所有情况下保留此`.schema`属性。但是，对于这些[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象通过外键约束引用的表，必须确定`.schema`在这些远程表中的表示方式，该远程模式名称也是当前[Postgresql 搜索路径](http://www.postgresql.org/docs/current/static/ddl-schemas.html#DDL-SCHEMAS-PATH)的成员。

默认情况下，Postgresql 方言模仿 Postgresql 自己的`pg_get_constraintdef()`内置过程鼓励的行为。此函数返回特定外键约束的样本定义，当该名称也位于Postgresql模式搜索路径中时，省略该定义中引用的模式名称。下面的交互说明了这种行为：

    test=> CREATE TABLE test_schema.referred(id INTEGER PRIMARY KEY);
    CREATE TABLE
    test=> CREATE TABLE referring(
    test(>         id INTEGER PRIMARY KEY,
    test(>         referred_id INTEGER REFERENCES test_schema.referred(id));
    CREATE TABLE
    test=> SET search_path TO public, test_schema;
    test=> SELECT pg_catalog.pg_get_constraintdef(r.oid, true) FROM
    test-> pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n
    test-> ON n.oid = c.relnamespace
    test-> JOIN pg_catalog.pg_constraint r  ON c.oid = r.conrelid
    test-> WHERE c.relname='referring' AND r.contype = 'f'
    test-> ;
                   pg_get_constraintdef
    ---------------------------------------------------
     FOREIGN KEY (referred_id) REFERENCES referred(id)
    (1 row)

Above, we created a table `referred` as a member of
the remote schema `test_schema`, however when we
added `test_schema` to the PG
`search_path` and then asked
`pg_get_constraintdef()` for the
`FOREIGN KEY` syntax, `test_schema` was not included in the output of the function.

另一方面，如果我们将搜索路径设置为`public`的典型默认值：

    test=> SET search_path TO public;
    SET

针对`pg_get_constraintdef()`的相同查询现在会为我们返回完全模式限定的名称：

    test=> SELECT pg_catalog.pg_get_constraintdef(r.oid, true) FROMplain
    test-> pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n
    test-> ON n.oid = c.relnamespace
    test-> JOIN pg_catalog.pg_constraint r  ON c.oid = r.conrelid
    test-> WHERE c.relname='referring' AND r.contype = 'f';
                         pg_get_constraintdef
    ---------------------------------------------------------------
     FOREIGN KEY (referred_id) REFERENCES test_schema.referred(id)
    (1 row)

SQLAlchemy将默认使用`pg_get_constraintdef()`的返回值来确定远程模式名称。也就是说，如果我们的`search_path`被设置为包含`test_schema`，并且我们调用了一个表反射过程，如下所示：

    >>> from sqlalchemy import Table, MetaData, create_engine
    >>> engine = create_engine("postgresql://scott:tiger@localhost/test")
    >>> with engine.connect() as conn:
    ...     conn.execute("SET search_path TO test_schema, public")
    ...     meta = MetaData()
    ...     referring = Table('referring', meta,
    ...                       autoload=True, autoload_with=conn)
    ...
    <sqlalchemy.engine.result.ResultProxy object at 0x101612ed0>

The above process would deliver to the [`MetaData.tables`](core_metadata.html#sqlalchemy.schema.MetaData.tables "sqlalchemy.schema.MetaData.tables")
collection `referred` table named **without** the
schema:

    >>> meta.tables['referred'].schema is Noneplainplain
    True

要改变反射的行为，使得不管`search_path`设置如何都维护所引用的模式，请使用`postgresql_ignore_search_path`选项，该选项可以指定为两种语言的特定于方言的参数[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")以及[`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect")：

    >>> with engine.connect() as conn:
    ...     conn.execute("SET search_path TO test_schema, public")
    ...     meta = MetaData()
    ...     referring = Table('referring', meta, autoload=True,
    ...                       autoload_with=conn,
    ...                       postgresql_ignore_search_path=True)
    ...
    <sqlalchemy.engine.result.ResultProxy object at 0x1016126d0>

我们现在将`test_schema.referred`存储为模式限定的：

    >>> meta.tables['test_schema.referred'].schema
    'test_schema'

Postgresql Schema反射的最佳实践

Postgresql 模式反射行为的描述很复杂，并且是多年处理各种用例和用户偏好的产物。但事实上，如果你只是坚持最简单的使用模式，就没有必要了解它：只将`search_path`设置为默认的`public`，绝不会引用名称`public`作为显式模式名称，否则在构建[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象时显式引用所有其他模式名称。这里描述的选项仅适用于那些不能或不愿意遵守这些准则的用户。

请注意，在所有情况下**，“默认”模式总是反映为`None`。**Postgresql 上的“默认”模式是由 Postgresql
`current_schema()`函数返回的模式。在典型的Postgresql安装中，这是`public`的名称。因此，引用`public`（即默认）模式中的另一个表的表将始终将`.schema`属性设置为`None`。

New in version 0.9.2: Added the
`postgresql_ignore_search_path` dialect-level option
accepted by [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
and [`MetaData.reflect()`](core_metadata.html#sqlalchemy.schema.MetaData.reflect "sqlalchemy.schema.MetaData.reflect").

也可以看看

[架构搜索路径](http://www.postgresql.org/docs/9.0/static/ddl-schemas.html#DDL-SCHEMAS-PATH)
- 在 Postgresql 网站上。

INSERT / UPDATE ... RETURNING [¶ T0\>](#insert-update-returning "Permalink to this headline")
---------------------------------------------------------------------------------------------

The dialect supports PG 8.2’s `INSERT..RETURNING`,
`UPDATE..RETURNING` and
`DELETE..RETURNING` syntaxes.
`INSERT..RETURNING` is used by default for
single-row INSERT statements in order to fetch newly generated primary
key identifiers. 要指定明确的`RETURNING`子句，请在每个语句的基础上使用`_UpdateBase.returning()`方法：

    # INSERT..RETURNING
    result = table.insert().returning(table.c.col1, table.c.col2).\
        values(name='foo')
    print result.fetchall()

    # UPDATE..RETURNING
    result = table.update().returning(table.c.col1, table.c.col2).\
        where(table.c.name=='foo').values(name='bar')
    print result.fetchall()

    # DELETE..RETURNING
    result = table.delete().returning(table.c.col1, table.c.col2).\
        where(table.c.name=='foo')
    print result.fetchall()

INSERT ... ON CONFLICT（Upsert）[¶](#insert-on-conflict-upsert "Permalink to this headline")
--------------------------------------------------------------------------------------------

Starting with version 9.5, PostgreSQL allows “upserts” (update or
insert) of rows into a table via the `ON CONFLICT`
clause of the `INSERT` statement.
只有该行不违反任何唯一约束时，才会插入候选行。在违反唯一约束的情况下，可能发生的次要操作可以是“DO
UPDATE”，表示目标行中的数据应该更新，或者“DO
NOTHING”，表示静默跳过此行。

冲突是使用现有的唯一约束和索引来确定的。These constraints may be
identified either using their name as stated in DDL, or they may be
*inferred* by stating the columns and conditions that comprise the
indexes.

SQLAlchemy provides `ON CONFLICT` support via the
Postgresql-specific [`postgresql.dml.insert()`](#sqlalchemy.dialects.postgresql.dml.insert "sqlalchemy.dialects.postgresql.dml.insert")
function, which provides the generative methods
[`on_conflict_do_update()`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")
and [`on_conflict_do_nothing()`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing"):

    from sqlalchemy.dialects.postgresql import insert

    insert_stmt = insert(my_table).values(
        id='some_existing_id',
        data='inserted value')

    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['id']
    )

    conn.execute(do_nothing_stmt)

    do_update_stmt = insert_stmt.on_conflict_do_update(
        constraint='pk_my_table',
        set_=dict(data='updated value')
    )

    conn.execute(do_update_stmt)

两种方法都使用命名约束或列推断来提供冲突的“目标”：

-   The [`Insert.on_conflict_do_update.index_elements`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.index_elements "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")
    argument specifies a sequence containing string column names,
    [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    objects, and/or SQL expression elements, which would identify a
    unique index:

        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'],
            set_=dict(data='updated value')
        )

        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[my_table.c.id],
            set_=dict(data='updated value')
        )

-   当使用[`Insert.on_conflict_do_update.index_elements`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.index_elements "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")推断索引时，可以通过指定使用[`Insert.on_conflict_do_update.index_where`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.index_where "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")参数来推断部分索引：

        from sqlalchemy.dialects.postgresql import insertplain

        stmt = insert(my_table).values(user_email='a@b.com', data='inserted data')
        stmt = stmt.on_conflict_do_update(
            index_elements=[my_table.c.user_email],
            index_where=my_table.c.user_email.like('%@gmail.com'),
            set_=dict(data=stmt.excluded.data)
            )
        conn.execute(stmt)

-   [`Insert.on_conflict_do_update.constraint`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.constraint "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")参数用于直接指定索引而不是推断它。这可以是 UNIQUE 约束，PRIMARY
    KEY 约束或 INDEX 的名称：

        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint='my_table_idx_1',
            set_=dict(data='updated value')
        )

        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint='my_table_pk',
            set_=dict(data='updated value')
        )

-   [`Insert.on_conflict_do_update.constraint`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.constraint "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")参数也可以引用表示约束的SQLAlchemy构造，例如，
    [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")，[`PrimaryKeyConstraint`](core_constraints.html#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")，[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")或[`ExcludeConstraint`](#sqlalchemy.dialects.postgresql.ExcludeConstraint "sqlalchemy.dialects.postgresql.ExcludeConstraint")。在这种使用中，如果约束具有名称，则直接使用它。否则，如果约束未命名，则将使用推理，其中约束的表达式和可选的 WHERE 子句将在结构中拼写出来。使用[`Table.primary_key`](core_metadata.html#sqlalchemy.schema.Table.primary_key "sqlalchemy.schema.Table.primary_key")属性来引用[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的已命名或未命名主键时，此用法特别方便：

        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint=my_table.primary_key,
            set_=dict(data='updated value')
        )

`ON CONFLICT...DO UPDATE` is used to perform an
update of the already existing row, using any combination of new values
as well as values from the proposed insertion.
这些值是使用[`Insert.on_conflict_do_update.set_`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.set_ "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")参数指定的。该参数接受由 UPDATE 的直接值组成的字典：

    from sqlalchemy.dialects.postgresql import insertplainplain

    stmt = insert(my_table).values(id='some_id', data='inserted value')
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=dict(data='updated value')
        )
    conn.execute(do_update_stmt)

警告

[`Insert.on_conflict_do_update()`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")方法不考虑 Python 方面的默认 UPDATE 值或生成函数，例如****。例如那些使用[`Column.onupdate`](core_metadata.html#sqlalchemy.schema.Column.params.onupdate "sqlalchemy.schema.Column")指定的。除非在[`Insert.on_conflict_do_update.set_`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.set_ "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")字典中手动指定这些值，否则这些值不会用于ON
CONFLICT样式的UPDATE。

为了引用建议的插入行，特殊别名[`excluded`](#sqlalchemy.dialects.postgresql.dml.Insert.excluded "sqlalchemy.dialects.postgresql.dml.Insert.excluded")可作为[`postgresql.dml.Insert`](#sqlalchemy.dialects.postgresql.dml.Insert "sqlalchemy.dialects.postgresql.dml.Insert")对象上的属性；这个对象是一个[`ColumnCollection`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")，这个别名包含目标表的所有列：

    from sqlalchemy.dialects.postgresql import insert

    stmt = insert(my_table).values(
        id='some_id',
        data='inserted value',
        author='jlh')
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=dict(data='updated value', author=stmt.excluded.author)
        )
    conn.execute(do_update_stmt)

[`Insert.on_conflict_do_update()`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")方法还使用[`Insert.on_conflict_do_update.where`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.where "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")参数接受WHERE子句，该参数将限制那些接收UPDATE的行：

    from sqlalchemy.dialects.postgresql import insertplain

    stmt = insert(my_table).values(
        id='some_id',
        data='inserted value',
        author='jlh')
    on_update_stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_=dict(data='updated value', author=stmt.excluded.author)
        where=(my_table.c.status == 2)
        )
    conn.execute(on_update_stmt)

`ON CONFLICT` may also be used to skip inserting a
row entirely if any conflict with a unique or exclusion constraint
occurs; below this is illustrated using the
[`on_conflict_do_nothing()`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing")
method:

    from sqlalchemy.dialects.postgresql import insert

    stmt = insert(my_table).values(id='some_id', data='inserted value')
    stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
    conn.execute(stmt)

如果没有指定任何列或约束，则使用`DO NOTHING`，它会跳过INSERT， ：

    from sqlalchemy.dialects.postgresql import insert

    stmt = insert(my_table).values(id='some_id', data='inserted value')
    stmt = stmt.on_conflict_do_nothing()
    conn.execute(stmt)

版本 1.1 中的新增功能增加了对 Postgresql ON CONFLICT 子句的支持

也可以看看

[INSERT .. ON
CONFLICT](http://www.postgresql.org/docs/current/static/sql-insert.html#SQL-ON-CONFLICT)
- 在Postgresql文档中。

全文检索[¶](#full-text-search "Permalink to this headline")
-----------------------------------------------------------

SQLAlchemy makes available the Postgresql `@@`
operator via the [`ColumnElement.match()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.match "sqlalchemy.sql.expression.ColumnElement.match")
method on any textual column expression.
在Postgresql方言中，表达式如下所示：

    select([sometable.c.text.match("search string")])

将发射到数据库：

    SELECT text @@ to_tsquery('search string') FROM table

使用标准的[`func`](core_sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")结构显式使用 Postgresql 文本搜索函数，如`to_tsquery()`和`to_tsvector()`。例如：

    select([
        func.to_tsvector('fat cats ate rats').match('cat & rat')
    ])

发出相当于：

    SELECT to_tsvector('fat cats ate rats') @@ to_tsquery('cat & rat')plain

[`postgresql.TSVECTOR`](#sqlalchemy.dialects.postgresql.TSVECTOR "sqlalchemy.dialects.postgresql.TSVECTOR")类型可以提供显式 CAST：

    from sqlalchemy.dialects.postgresql import TSVECTOR
    from sqlalchemy import select, cast
    select([cast("some text", TSVECTOR)])

产生一个相当于：

    SELECT CAST('some text' AS TSVECTOR) AS anon_1

Postgresql中的全文搜索受以下组合的影响：`default_text_search_config`的 PostgresSQL 设置，用于构建 GIN /
GiST 索引的`regconfig`以及`regconfig`

对具有已经预先计算的 GIN 或 GiST 索引的列执行全文搜索时（全文搜索中常见），可能需要显式传递特定的 PostgresSQL
`regconfig`值以确保查询计划人员利用索引并且不需要重新计算列。

为了提供明确的查询计划或使用不同的搜索策略，`match`方法接受一个`postgresql_regconfig`关键字参数：

    select([mytable.c.id]).where(
        mytable.c.title.match('somestring', postgresql_regconfig='english')
    )

发出相当于：

    SELECT mytable.id FROM mytable
    WHERE mytable.title @@ to_tsquery('english', 'somestring')

还可以将'regconfig'值作为初始参数传递给`to_tsvector()`命令：

    select([mytable.c.id]).where(plain
            func.to_tsvector('english', mytable.c.title )            .match('somestring', postgresql_regconfig='english')
        )

产生一个相当于：

    SELECT mytable.id FROM mytableplain
    WHERE to_tsvector('english', mytable.title) @@
        to_tsquery('english', 'somestring')

建议您使用 PostgresSQL 的`EXPLAIN ANALYZE ...`工具，以确保您使用 SQLAlchemy 生成查询，以充分利用您可能为全文搜索创建的任何索引。

仅从... [¶](#from-only "Permalink to this headline")
----------------------------------------------------

该方言支持 PostgreSQL 的 ONLY 关键字，仅用于定位继承层次结构中的特定表。This
can be used to produce the `SELECT ... FROM ONLY`,
`UPDATE ONLY ...`, and
`DELETE FROM ONLY ...` syntaxes.
它使用SQLAlchemy的提示机制：

    # SELECT ... FROM ONLY ...
    result = table.select().with_hint(table, 'ONLY', 'postgresql')
    print result.fetchall()

    # UPDATE ONLY ...
    table.update(values=dict(foo='bar')).with_hint('ONLY',
                                                   dialect_name='postgresql')

    # DELETE FROM ONLY ...
    table.delete().with_hint('ONLY', dialect_name='postgresql')

Postgresql特定的索引选项[¶](#postgresql-specific-index-options "Permalink to this headline")
--------------------------------------------------------------------------------------------

对于[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构的几个扩展是可用的，特定于 PostgreSQL 方言。

### 部分索引[¶](#partial-indexes "Permalink to this headline")

部分索引为索引定义添加标准，以便将索引应用于行的子集。这些可以使用`postgresql_where`关键字参数在[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")中指定：

    Index('my_index', my_table.c.id, postgresql_where=tbl.c.value > 10)

### 运算符类[¶](#operator-classes "Permalink to this headline")

PostgreSQL 允许为索引的每一列指定一个*操作符类*（参见[http://www.postgresql.org/docs/8.3/interactive/indexes-opclass.html
t1
\>）。](http://www.postgresql.org/docs/8.3/interactive/indexes-opclass.html)[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")构造允许通过`postgresql_ops`关键字参数指定这些构造：

    Index('my_index', my_table.c.id, my_table.c.data,
                            postgresql_ops={
                                'data': 'text_pattern_ops',
                                'id': 'int4_ops'
                            })

版本0.7.2中的新功能： `postgresql_ops`关键字参数指向[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构。

请注意，`postgresql_ops`字典中的键是[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的“键”名称，即用于从`.c`访问它的名称[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的集合，可以将其配置为与数据库中表示的列的实际名称不同。

### 索引类型[¶](#index-types "Permalink to this headline")

PostgreSQL提供了几种索引类型：B-Tree，Hash，GiST和GIN，以及用户创建自己的能力（参见[http://www.postgresql.org/docs/8.3/static/indexes
-types.html
T0\>）。](http://www.postgresql.org/docs/8.3/static/indexes-types.html)可以使用`postgresql_using`关键字参数在[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")中指定这些参数：

    Index('my_index', my_table.c.data, postgresql_using='gin')

The value passed to the keyword argument will be simply passed through
to the underlying CREATE INDEX command, so it *must* be a valid index
type for your version of PostgreSQL.

### 索引存储参数[¶](#index-storage-parameters "Permalink to this headline")

PostgreSQL允许在索引上设置存储参数。可用的存储参数取决于索引使用的索引方法。可以使用`postgresql_with`关键字参数在[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")中指定存储参数：

    Index('my_index', my_table.c.data, postgresql_with={"fillfactor": 50})

版本1.0.6中的新功能

PostgreSQL允许定义要在其中创建索引的表空间。可以使用`postgresql_tablespace`关键字参数在[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")上指定表空间：

    Index('my_index', my_table.c.data, postgresql_tablespace='my_tablespace')plain

版本 1.1 中的新功能

请注意，同样的选项也可以在[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")上使用。

### 与当前[¶](#indexes-with-concurrently "Permalink to this headline")的索引

将 flag `postgresql_concurrently`传递给[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构支持 PostgreSQL 索引选项 CONCURRENTLY：

    tbl = Table('testtbl', m, Column('data', Integer))

    idx1 = Index('test_idx1', tbl.c.data, postgresql_concurrently=True)

假设检测到 Postgresql 8.2 或更高版本或无连接方言，上述索引结构将呈现 DDL
for CREATE INDEX，如下所示：

    CREATE INDEX CONCURRENTLY test_idx1 ON testtbl (data)

对于 DROP INDEX，假设检测到 Postgresql
9.2 或更高版本或者无连接方言，它将发出：

    DROP INDEX CONCURRENTLY test_idx1

版本 1.1 中的新功能：支持 DROP
INDEX 上的 CONCURRENTLY。如果在连接上检测到足够高的 Postgresql 版本（或无连接方言），则只会发出 CONCURRENTLY 关键字。

Postgresql索引反射[¶](#postgresql-index-reflection "Permalink to this headline")
--------------------------------------------------------------------------------

只要使用UNIQUE CONSTRAINT构造，Postgresql数据库就会隐式创建一个UNIQUE
INDEX。When inspecting a table using [`Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector"),
the [`Inspector.get_indexes()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes "sqlalchemy.engine.reflection.Inspector.get_indexes")
and the [`Inspector.get_unique_constraints()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints "sqlalchemy.engine.reflection.Inspector.get_unique_constraints")
will report on these two constructs distinctly; in the case of the
index, the key `duplicates_constraint` will be
present in the index entry if it is detected as mirroring a constraint.
When performing reflection using `Table(..., autoload=True)`, the UNIQUE INDEX is **not** returned in `Table.indexes` when it is detected as mirroring a
[`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
in the `Table.constraints`
collection.

Changed in version 1.0.0: - [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
reflection now includes [`UniqueConstraint`](core_constraints.html#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")
objects present in the `Table.constraints` collection; the Postgresql backend will no longer include a
“mirrored” [`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
construct in `Table.indexes` if
it is detected as corresponding to a unique constraint.

特殊反射选项[¶](#special-reflection-options "Permalink to this headline")
-------------------------------------------------------------------------

用于 Postgresql 后端的[`Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")是[`PGInspector`](#sqlalchemy.dialects.postgresql.base.PGInspector "sqlalchemy.dialects.postgresql.base.PGInspector")的一个实例，它提供了其他方法：

    from sqlalchemy import create_engine, inspect

    engine = create_engine("postgresql+psycopg2://localhost/test")
    insp = inspect(engine)  # will be a PGInspector

    print(insp.get_enums())

*class* `sqlalchemy.dialects.postgresql.base。`{.descclassname} `PGInspector`{.descname} （ *conn* ） T5\> [¶ T6\>](#sqlalchemy.dialects.postgresql.base.PGInspector "Permalink to this definition")
:   基础：[`sqlalchemy.engine.reflection.Inspector`](core_reflection.html#sqlalchemy.engine.reflection.Inspector "sqlalchemy.engine.reflection.Inspector")

    ` get_enums  T0> （ T1> 架构=无 T2> ） T3> ¶ T4>`{.descname}plainplain
    :   返回ENUM对象的列表。

        每个成员都是包含这些字段的字典：

        > -   名称 - 枚举的名称
        > -   模式 - 枚举的模式名称。
        > -   visible - 布尔值，无论此枚举是否在默认搜索路径中可见。
        > -   标签 - 适用于枚举的字符串标签列表。

        参数：

        **架构**
        [¶](#sqlalchemy.dialects.postgresql.base.PGInspector.get_enums.params.schema)
        -
        架构名称。如果没有，则使用默认模式（通常是“公共”）。也可以设置为'\*'来表示所有模式的加载枚举。

        版本1.0.0中的新功能

    ` get_foreign_table_names  T0> （ T1> 架构=无 T2> ） T3> ¶ T4>`{.descname}
    :   返回FOREIGN TABLE名称的列表。

        Behavior is similar to that of
        [`Inspector.get_table_names()`](core_reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names "sqlalchemy.engine.reflection.Inspector.get_table_names"),
        except that the list is limited to those tables tha report a
        `relkind` value of `f`.

        版本1.0.0中的新功能

    `get_table_oid`{.descname} （ *table\_name*，*schema =无* ） [t5 \>](#sqlalchemy.dialects.postgresql.base.PGInspector.get_table_oid "Permalink to this definition")
    :   返回给定表名称的OID。

    `get_view_names`{.descname} （ *schema = None*，*include =（'plain'*，*'materialized' T4\> ） T5\> [¶ T6\>](#sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names "Permalink to this definition")*
    :   返回schema中的所有视图名称。

        参数：

        -   **schema**[¶](#sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names.params.schema)
            – Optional, retrieve names from a non-default schema.
            对于特殊引用，请使用[`quoted_name`](core_sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")。
        -   **include**
            [¶](#sqlalchemy.dialects.postgresql.base.PGInspector.get_view_names.params.include)
            -

            指定要返回哪些类型的视图。作为字符串值（对于单一类型）或元组（对于任意数量的类型）传递。默认为`（'plain'， 'materialized'）`。

            版本1.1中的新功能

PostgreSQL 表选项[¶](#postgresql-table-options "Permalink to this headline")
---------------------------------------------------------------------------

PostgreSQL 方言结合[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")结构直接支持 CREATE
TABLE 的几个选项：

-   `TABLESPACE`

        Table("some_table", metadata, ..., postgresql_tablespace='some_tablespace')plain

    上述选项也可用于[`Index`](core_constraints.html#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构。

-   `ON COMMIT`：

        Table("some_table", metadata, ..., postgresql_on_commit='PRESERVE ROWS')

-   `WITH OIDS`：

        Table("some_table", metadata, ..., postgresql_with_oids=True)plain

-   `WITHOUT OIDS`：

        Table("some_table", metadata, ..., postgresql_with_oids=False)

-   `INHERITS`

        Table("some_table", metadata, ..., postgresql_inherits="some_supertable")plain

        Table("some_table", metadata, ..., postgresql_inherits=("t1", "t2", ...))

版本 1.0.0 中的新功能

也可以看看

[Postgresql CREATE
TABLE选项](http://www.postgresql.org/docs/current/static/sql-createtable.html)

ARRAY 类型[¶](#array-types "Permalink to this headline")
-------------------------------------------------------

Postgresql方言支持数组，既可以是多维列类型也可以是数组文字：

-   [`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
    - ARRAY 数据类型
-   [`postgresql.array`](#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")
    - 数组字面量
-   [`postgresql.array_agg()`](#sqlalchemy.dialects.postgresql.array_agg "sqlalchemy.dialects.postgresql.array_agg")
    - ARRAY\_AGG SQL函数
-   [`postgresql.aggregate_order_by`](#sqlalchemy.dialects.postgresql.aggregate_order_by "sqlalchemy.dialects.postgresql.aggregate_order_by")
    - PG的ORDER BY聚合函数语法的助手。

JSON类型[¶](#json-types "Permalink to this headline")
-----------------------------------------------------

Postgresql 方言支持 JSON 和 JSONB 数据类型，包括 psycopg2 的本地支持和对 Postgresql 所有特殊操作符的支持：

-   [`postgresql.JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")
-   [`postgresql.JSONB`](#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")

HSTORE类型[¶](#hstore-type "Permalink to this headline")
--------------------------------------------------------

支持 Postgresql HSTORE 类型以及 hstore 字面值：

-   [`postgresql.HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")
    - HSTORE 数据类型
-   [`postgresql.hstore`](#sqlalchemy.dialects.postgresql.hstore "sqlalchemy.dialects.postgresql.hstore")
    - hstore文字

ENUM 类型[¶](#enum-types "Permalink to this headline")
-----------------------------------------------------

Postgresql 有一个可独立创建的 TYPE 结构，用于实现枚举类型。这种方法在 SQLAlchemy 方面在这种类型应该是 CREATED 和 DROPPED 的时候引入了很大的复杂性。类型对象也是一个可独立反映的实体。应参考以下部分：

-   [`postgresql.ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
    - DDL 并输入 ENUM 的支持。
-   [`PGInspector.get_enums()`](#sqlalchemy.dialects.postgresql.base.PGInspector.get_enums "sqlalchemy.dialects.postgresql.base.PGInspector.get_enums")
    - 检索当前ENUM类型的列表
-   [`postgresql.ENUM.create()`](#sqlalchemy.dialects.postgresql.ENUM.create "sqlalchemy.dialects.postgresql.ENUM.create")
    , [`postgresql.ENUM.drop()`](#sqlalchemy.dialects.postgresql.ENUM.drop "sqlalchemy.dialects.postgresql.ENUM.drop")
    - individual CREATE and DROP commands for ENUM.

### 使用带 ARRAY 的 ENUM [¶](#using-enum-with-array "Permalink to this headline")

ENUM 和 ARRAY 的组合目前不直接支持后端 DBAPI。为了发送和接收 ENUM 的 ARRAY，请使用以下解决方法类型：

    class ArrayOfEnum(ARRAY):

        def bind_expression(self, bindvalue):
            return sa.cast(bindvalue, self)

        def result_processor(self, dialect, coltype):
            super_rp = super(ArrayOfEnum, self).result_processor(
                dialect, coltype)

            def handle_raw_string(value):
                inner = re.match(r"^{(.*)}$", value).group(1)
                return inner.split(",") if inner else []

            def process(value):
                if value is None:
                    return None
                return super_rp(handle_raw_string(value))
            return process

例如。：

    Table(
        'mydata', metadata,
        Column('id', Integer, primary_key=True),
        Column('data', ArrayOfEnum(ENUM('a', 'b, 'c', name='myenum')))

    )

此类型不作为内置类型包含，因为它将与突然决定直接在新版本中支持 ENUM 的 ARRAY 的 DBAPI 不兼容。

PostgreSQL数据类型[¶](#postgresql-data-types "Permalink to this headline")
--------------------------------------------------------------------------

与所有 SQLAlchemy 方言一样，所有已知可用于 Postgresql 的大写类型都可以从顶级方言导入，无论它们源自[`sqlalchemy.types`](core_type_basics.html#module-sqlalchemy.types "sqlalchemy.types")还是来自本地方言：

    from sqlalchemy.dialects.postgresql import \plain
        ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
        DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
        INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
        TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
        DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR

特定于 PostgreSQL 的类型，或具有特定于 PostgreSQL 的构造参数，如下所示：

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `aggregate_order_by`{.descname} （ *target*，*order\_by T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.postgresql.aggregate_order_by "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.expression.ColumnElement`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")

    用表达式表示Postgresql聚合顺序。plain

    例如。：

        from sqlalchemy.dialects.postgresql import aggregate_order_by
        expr = func.array_agg(aggregate_order_by(table.c.a, table.c.b.desc()))
        stmt = select([expr])

    将代表表达式：

        SELECT array_agg(a ORDER BY b DESC) FROM table;

    同理：

        expr = func.string_agg(
            table.c.a,
            aggregate_order_by(literal_column("','"), table.c.a)
        )
        stmt = select([expr])

    将代表：

        SELECT string_agg(a, ',' ORDER BY a) FROM table;

    版本1.1中的新功能

    也可以看看

    [`array_agg`](core_functions.html#sqlalchemy.sql.functions.array_agg "sqlalchemy.sql.functions.array_agg")

 *class*`sqlalchemy.dialects.postgresql.`{.descclassname}`array`{.descname}(*clauses*, *\*\*kw*)[¶](#sqlalchemy.dialects.postgresql.array "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Tuple`](core_sqlelement.html#sqlalchemy.sql.expression.Tuple "sqlalchemy.sql.expression.Tuple")

    Postgresql ARRAY文字。

    这用于在SQL表达式中生成ARRAY文字，例如：

        from sqlalchemy.dialects.postgresql import array
        from sqlalchemy.dialects import postgresql
        from sqlalchemy import select, func

        stmt = select([
                        array([1,2]) + array([3,4,5])
                    ])

        print stmt.compile(dialect=postgresql.dialect())

    生成SQL：

        SELECT ARRAY[%(param_1)s, %(param_2)s] ||
            ARRAY[%(param_3)s, %(param_4)s, %(param_5)s]) AS anon_1

    [`array`](#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")的实例将始终具有数据类型[`ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")。除非传递了`type_`关键字参数，否则数组的“内部”类型将根据存在的值推断出来：

        array(['foo', 'bar'], type_=CHAR)

    0.8版新增：添加了[`array`](#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")文字类型。

    也可以看看：

    [`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `ARRAY`{.descname} （ *item\_type*，*as\_tuple = False*，*dimensions = None*，*zero\_indexes = False* ） [¶](#sqlalchemy.dialects.postgresql.ARRAY "Permalink to this definition")
:   基础：`sqlalchemy.sql.expression.SchemaEventTarget`，[`sqlalchemy.types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")

    Postgresql ARRAY类型。

    版本1.1中更改： [`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型现在是核心[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型的子类。

    [`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型的构造方式与核心[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型；一个成员类型是必需的，并且如果该类型要用于多个维度，则建议使用多个维度：

        from sqlalchemy.dialects import postgresql

        mytable = Table("mytable", metadata,
                Column("data", postgresql.ARRAY(Integer, dimensions=2))
            )

    [`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型提供在核心[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型上定义的所有操作，包括对“维度”，索引访问和简单匹配（如[`types.ARRAY.Comparator.any()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.any "sqlalchemy.types.ARRAY.Comparator.any")和[`types.ARRAY.Comparator.all()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.all "sqlalchemy.types.ARRAY.Comparator.all")。[`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")
    class also provides PostgreSQL-specific methods for containment
    operations, including
    [`postgresql.ARRAY.Comparator.contains()`](#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contains "sqlalchemy.dialects.postgresql.ARRAY.Comparator.contains")
    [`postgresql.ARRAY.Comparator.contained_by()`](#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contained_by "sqlalchemy.dialects.postgresql.ARRAY.Comparator.contained_by"),
    and [`postgresql.ARRAY.Comparator.overlap()`](#sqlalchemy.dialects.postgresql.ARRAY.Comparator.overlap "sqlalchemy.dialects.postgresql.ARRAY.Comparator.overlap"),
    e.g.:

        mytable.c.data.contains([1, 2])

    所有PostgreSQL DBAPI可能不支持[`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型；目前已知只能在psycopg2上工作。

    此外，[`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")类型不能直接与[`ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")类型结合使用。有关解决方法，请参阅[Using
    ENUM with ARRAY](#postgresql-array-of-enum)中的特殊类型。

    也可以看看

    [`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")
    - 基本数组类型

    [`postgresql.array`](#sqlalchemy.dialects.postgresql.array "sqlalchemy.dialects.postgresql.array")
    - 产生一个文字数组值。

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.dialects.postgresql.ARRAY.Comparator "Permalink to this definition")
    :   基础：`sqlalchemy.types.Comparator`

        定义[`ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")的比较操作。

        请注意，这些操作除了基类[`types.ARRAY.Comparator`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator "sqlalchemy.types.ARRAY.Comparator")类提供的操作外，还包括[`types.ARRAY.Comparator.any()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.any "sqlalchemy.types.ARRAY.Comparator.any")和[`types.ARRAY.Comparator.all()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.all "sqlalchemy.types.ARRAY.Comparator.all")

        ` contained_by  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试元素是否是参数数组表达式元素的适当子集。

        `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contains "Permalink to this definition") \>
        :   布尔表达式。测试元素是否是参数数组表达式元素的超集。

        `重叠 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试数组是否具有与参数数组表达式相同的元素。

    `ARRAY  tt> __ init __`{.descclassname} （ *item\_type*，*as\_tuple = False*，*dimensions =无*，*zero\_indexes = False ） [¶](#sqlalchemy.dialects.postgresql.ARRAY.__init__ "Permalink to this definition")*
    :   构建一个ARRAY。

        例如。：

            Column('myarray', ARRAY(Integer))

        参数是：

        参数：

        -   **item\_type**
            [¶](#sqlalchemy.dialects.postgresql.ARRAY.params.item_type)
            -
            此数组项目的数据类型。请注意，这里的维数是不相关的，所以像`INTEGER[][]`这样的多维数组被构造为`ARRAY(Integer)`，而不是`ARRAY(ARRAY(Integer))`等等。
        -   **as\_tuple = False**
            [¶](#sqlalchemy.dialects.postgresql.ARRAY.params.as_tuple) -
            指定返回结果是否应该从列表转换为元组。诸如psycopg2的DBAPI默认返回列表。当元组返回时，结果是可散列的。
        -   **dimensions**[¶](#sqlalchemy.dialects.postgresql.ARRAY.params.dimensions)
            – if non-None, the ARRAY will assume a fixed number of
            dimensions.
            这将导致为此ARRAY发出的DDL包含确切数量的括号子句`[]`，并且还会优化整体类型的性能。请注意，PG数组总是隐含的“无量纲”，这意味着无论它们如何声明，它们都可以存储任意数量的维度。
        -   **zero\_indexes = False**
            [¶](#sqlalchemy.dialects.postgresql.ARRAY.params.zero_indexes)
            -

            当为True时，索引值将在基于Python的零和基于Postgresql
            one的索引之间转换。在传递给数据库之前，将在所有索引值中添加一个值。

            版本0.9.5中的新功能

 `sqlalchemy.dialects.postgresql.`{.descclassname}`array_agg`{.descname}(*\*arg*, *\*\*kw*)[¶](#sqlalchemy.dialects.postgresql.array_agg "Permalink to this definition")
:   确保返回类型是[`postgresql.ARRAY`](#sqlalchemy.dialects.postgresql.ARRAY "sqlalchemy.dialects.postgresql.ARRAY")，而不是普通的[`types.ARRAY`](core_type_basics.html#sqlalchemy.types.ARRAY "sqlalchemy.types.ARRAY")类型的[`array_agg`](core_functions.html#sqlalchemy.sql.functions.array_agg "sqlalchemy.sql.functions.array_agg")的 Postgresql 特定形式。

    版本1.1中的新功能

 `sqlalchemy.dialects.postgresql.`{.descclassname}`Any`{.descname}(*other*, *arrexpr*, *operator=\<built-in function eq\>*)[¶](#sqlalchemy.dialects.postgresql.Any "Permalink to this definition")
:   [`ARRAY.Comparator.any()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.any "sqlalchemy.types.ARRAY.Comparator.any")方法的同义词。

    这种方法是遗留的，在这里是为了向后兼容。plain

    也可以看看

    [`expression.any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")

 `sqlalchemy.dialects.postgresql.`{.descclassname}`All`{.descname}(*other*, *arrexpr*, *operator=\<built-in function eq\>*)[¶](#sqlalchemy.dialects.postgresql.All "Permalink to this definition")
:   [`ARRAY.Comparator.all()`](core_type_basics.html#sqlalchemy.types.ARRAY.Comparator.all "sqlalchemy.types.ARRAY.Comparator.all")方法的同义词。

    这种方法是遗留的，在这里是为了向后兼容。

    也可以看看

    [`expression.all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `BIT`{.descname} （ *length = None*，*变化=假 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.postgresql.BIT "Permalink to this definition")*
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

 *class*`sqlalchemy.dialects.postgresql.`{.descclassname}`BYTEA`{.descname}(*length=None*)[¶](#sqlalchemy.dialects.postgresql.BYTEA "Permalink to this definition")
:   基础：[`sqlalchemy.types.LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

    ` __初始化__  T0> （ T1> 长度=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.LargeBinary.__init__ "sqlalchemy.types.LargeBinary.__init__")
        *method of* [`LargeBinary`](core_type_basics.html#sqlalchemy.types.LargeBinary "sqlalchemy.types.LargeBinary")

        构建一个LargeBinary类型。

        参数：

        **length**[¶](#sqlalchemy.dialects.postgresql.BYTEA.params.length)
        – optional, a length for the column for use in DDL statements,
        for those binary types that accept a length, such as the MySQL
        BLOB type.

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `CIDR`{.descname} [¶](#sqlalchemy.dialects.postgresql.CIDR "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `DOUBLE_PRECISION`{.descname} （ *precision = None*，*asdecimal = False*，*decimal\_return\_scale = None*，*\*\* kwargs* ） [](#sqlalchemy.dialects.postgresql.DOUBLE_PRECISION "Permalink to this definition")
:   基础：[`sqlalchemy.types.Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")

     `__init__`{.descname}(*precision=None*, *asdecimal=False*, *decimal\_return\_scale=None*, *\*\*kwargs*)[¶](#sqlalchemy.dialects.postgresql.DOUBLE_PRECISION.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.Float.__init__ "sqlalchemy.types.Float.__init__")
        *method of* [`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")

        构建一个浮动。

        参数：

        -   **precision**[¶](#sqlalchemy.dialects.postgresql.DOUBLE_PRECISION.params.precision)
            – the numeric precision for use in DDL
            `CREATE TABLE`.
        -   **asdecimal**[¶](#sqlalchemy.dialects.postgresql.DOUBLE_PRECISION.params.asdecimal)
            – the same flag as that of [`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric"),
            but defaults to `False`.
            请注意，将此标志设置为`True`会导致浮点转换。
        -   **decimal\_return\_scale**
            [¶](#sqlalchemy.dialects.postgresql.DOUBLE_PRECISION.params.decimal_return_scale)
            -

            从float到Python小数转换时使用的默认缩放比例。由于十进制不准确性，浮点值通常会长得多，并且大多数浮点数据库类型没有“缩放”的概念，所以默认情况下，浮点类型在转换时会查找前十个小数位。指定此值将覆盖该长度。请注意，包含“scale”的MySQL浮点类型将使用“scale”作为decimal\_return\_scale的默认值（如果未另外指定）。

            版本0.9.0中的新功能

        -   **\*\* kwargs**
            [¶](#sqlalchemy.dialects.postgresql.DOUBLE_PRECISION.params.**kwargs)
            - 不建议使用。其他参数在这里被默认的[`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")类型忽略。对于支持附加参数的特定于数据库的浮点数，请参阅该方言的文档以获取详细信息，例如[`sqlalchemy.dialects.mysql.FLOAT`](mysql.html#sqlalchemy.dialects.mysql.FLOAT "sqlalchemy.dialects.mysql.FLOAT")。

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `ENUM`{.descname} （ *\* enums*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.postgresql.ENUM "Permalink to this definition")*
:   基础：[`sqlalchemy.types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")

    Postgresql的ENUM类型。

    这是[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")的一个子类，它包含对PG的`CREATE TYPE`和`DROP TYPE`。

    当使用内建类型[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")并且[`Enum.native_enum`](core_type_basics.html#sqlalchemy.types.Enum.params.native_enum "sqlalchemy.types.Enum")标志保留其默认值为True时，Postgresql后端将使用[`postgresql.ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")

    ENUM的创建/删除行为必然错综复杂，因为ENUM类型与父表关系的关系很尴尬，因为它可能仅由单个表“拥有”，或者可能在许多表中共享。

    When using [`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")
    or [`postgresql.ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")
    in an “inline” fashion, the `CREATE TYPE` and
    `DROP TYPE` is emitted corresponding to when the
    [`Table.create()`](core_metadata.html#sqlalchemy.schema.Table.create "sqlalchemy.schema.Table.create")
    and [`Table.drop()`](core_metadata.html#sqlalchemy.schema.Table.drop "sqlalchemy.schema.Table.drop")
    methods are called:

        table = Table('sometable', metadata,
            Column('some_enum', ENUM('a', 'b', 'c', name='myenum'))
        )

        table.create(engine)  # will emit CREATE ENUM and CREATE TABLE
        table.drop(engine)  # will emit DROP TABLE and DROP ENUM

    要在多个表之间使用通用枚举类型，最好的做法是独立声明[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")或[`postgresql.ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")，并将其与[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")

        my_enum = ENUM('a', 'b', 'c', name='myenum', metadata=metadata)

        t1 = Table('sometable_one', metadata,
            Column('some_enum', myenum)
        )

        t2 = Table('sometable_two', metadata,
            Column('some_enum', myenum)
        )

    当使用这种模式时，仍然必须注意各个表格创建的级别。在没有指定`checkfirst=True`的情况下发送CREATE TABLE仍然会导致问题：

        t1.create(engine) # will fail: no such type 'myenum'

    如果我们指定`checkfirst=True`，单独的表级创建操作将检查`ENUM`并创建（如果不存在）：

        # will check if enum exists, and emit CREATE TYPE if not
        t1.create(engine, checkfirst=True)

    当使用元数据级ENUM类型时，如果调用元数据范围的创建/删除操作，则将始终创建并删除类型：

        metadata.create_all(engine)  # will emit CREATE TYPE
        metadata.drop_all(engine)  # will emit DROP TYPE

    该类型也可以直接创建和删除：

        my_enum.create(engine)
        my_enum.drop(engine)

    版本1.0.0更改：现在，Postgresql [`postgresql.ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")类型对于CREATE
    / DROP的行为更为严格。除了`table.create(checkfirst=True)`外，元数据级ENUM类型只会在元数据级创建和删除，而不是表级。The
    `table.drop()` call will now emit a DROP TYPE
    for a table-level enumerated type.

    `__ init __`{.descname} （ *\* enums*，*\*\* kw* ） [T5\>](#sqlalchemy.dialects.postgresql.ENUM.__init__ "Permalink to this definition")
    :   构建一个[`ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")。

        参数与[`types.Enum`](core_type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")的参数相同，但也包括以下参数。

        参数：

        **create\_type**
        [¶](#sqlalchemy.dialects.postgresql.ENUM.params.create_type) -

        默认为True。Indicates that `CREATE TYPE`
        should be emitted, after optionally checking for the presence of
        the type, when the parent table is being created; and
        additionally that `DROP TYPE` is called when
        the table is dropped. When `False`, no check
        will be performed and no `CREATE TYPE` or
        `DROP TYPE` is emitted, unless
        [`create()`](#sqlalchemy.dialects.postgresql.ENUM.create "sqlalchemy.dialects.postgresql.ENUM.create")
        or [`drop()`](#sqlalchemy.dialects.postgresql.ENUM.drop "sqlalchemy.dialects.postgresql.ENUM.drop")
        are called directly. 设置为`False`在创建方案调用SQL文件而不访问实际数据库时很有用 -
        [`create()`](#sqlalchemy.dialects.postgresql.ENUM.create "sqlalchemy.dialects.postgresql.ENUM.create")和[`drop()`](#sqlalchemy.dialects.postgresql.ENUM.drop "sqlalchemy.dialects.postgresql.ENUM.drop")方法可用于将SQL发送到目标绑定。

        New in version 0.7.4.

     `create`{.descname}(*bind=None*, *checkfirst=True*)[¶](#sqlalchemy.dialects.postgresql.ENUM.create "Permalink to this definition")
    :   Emit `CREATE TYPE` for this [`ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM").

        如果底层方言不支持Postgresql CREATE TYPE，则不采取任何操作。

        参数：

        -   **bind**[¶](#sqlalchemy.dialects.postgresql.ENUM.create.params.bind)
            – a connectable [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine"),
            [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"),
            or similar object to emit SQL.
        -   **checkfirst**[¶](#sqlalchemy.dialects.postgresql.ENUM.create.params.checkfirst)
            – if `True`, a query against the PG
            catalog will be first performed to see if the type does not
            exist already before creating.

     `drop`{.descname}(*bind=None*, *checkfirst=True*)[¶](#sqlalchemy.dialects.postgresql.ENUM.drop "Permalink to this definition")
    :   Emit `DROP TYPE` for this [`ENUM`](#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM").

        如果底层方言不支持Postgresql DROP TYPE，则不采取任何操作。

        参数：

        -   **bind**[¶](#sqlalchemy.dialects.postgresql.ENUM.drop.params.bind)
            – a connectable [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine"),
            [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"),
            or similar object to emit SQL.
        -   **checkfirst**[¶](#sqlalchemy.dialects.postgresql.ENUM.drop.params.checkfirst)
            – if `True`, a query against the PG
            catalog will be first performed to see if the type actually
            exists before dropping.

 *class*`sqlalchemy.dialects.postgresql.`{.descclassname}`HSTORE`{.descname}(*text\_type=None*)[¶](#sqlalchemy.dialects.postgresql.HSTORE "Permalink to this definition")
:   基础：[`sqlalchemy.types.Indexable`](core_type_api.html#sqlalchemy.types.Indexable "sqlalchemy.types.Indexable")，[`sqlalchemy.types.Concatenable`](core_type_api.html#sqlalchemy.types.Concatenable "sqlalchemy.types.Concatenable")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql HSTORE类型。

    [`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")类型存储包含字符串的字典，例如：

        data_table = Table('data_table', metadata,
            Column('id', Integer, primary_key=True),
            Column('data', HSTORE)
        )

        with engine.connect() as conn:
            conn.execute(
                data_table.insert(),
                data = {"key1": "value1", "key2": "value2"}
            )

    [`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")
    provides for a wide range of operations, including:

    -   索引操作：

            data_table.c.data['some key'] == 'some value'

    -   遏制行动：

            data_table.c.data.has_key('some key')

            data_table.c.data.has_all(['one', 'two', 'three'])

    -   级联：

            data_table.c.data + {"k1": "v1"}

    有关特殊方法的完整列表，请参阅`HSTORE.comparator_factory`。

    对于与SQLAlchemy ORM一起使用，可能希望将[`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")的用法与[`MutableDict`](orm_extensions_mutable.html#sqlalchemy.ext.mutable.MutableDict "sqlalchemy.ext.mutable.MutableDict")字典现在作为[`sqlalchemy.ext.mutable`](orm_extensions_mutable.html#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")的一部分结合使用延期。该扩展将允许对字典进行“原地”更改，例如，添加新密钥或替换/删除当前字典中的现有密钥，以产生将由工作单元检测到的事件：

        from sqlalchemy.ext.mutable import MutableDict

        class MyClass(Base):
            __tablename__ = 'data_table'

            id = Column(Integer, primary_key=True)
            data = Column(MutableDict.as_mutable(HSTORE))

        my_object = session.query(MyClass).one()

        # in-place mutation, requires Mutable extension
        # in order for the ORM to detect
        my_object.data['some_key'] = 'some value'

        session.commit()

    当不使用[`sqlalchemy.ext.mutable`](orm_extensions_mutable.html#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展名时，除非该字典值被重新分配给HSTORE属性本身，否则ORM将不会被提醒对现有字典的内容进行任何更改，从而产生变化事件。

    0.8版本中的新功能

    也可以看看

    [`hstore`](#sqlalchemy.dialects.postgresql.hstore "sqlalchemy.dialects.postgresql.hstore")
    - 呈现Postgresql `hstore()`函数。

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.dialects.postgresql.HSTORE.Comparator "Permalink to this definition")
    :   基础：`sqlalchemy.types.Comparator`，`sqlalchemy.types.Comparator`

        定义[`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")的比较操作。

        `阵列 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   文本数组表达式。返回交替键和值的数组。

        ` contained_by  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试键是否是参数jsonb表达式的键的真子集。

        `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.dialects.postgresql.HSTORE.Comparator.contains "Permalink to this definition") \>
        :   布尔表达式。测试键（或数组）是否是/包含参数jsonb表达式的键的超集。

        `定义 T0> （ T1> 键 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试密钥是否存在非NULL值。请注意，该密钥可能是SQLA表达式。

        `删除 T0> （ T1> 键 T2> ） T3> ¶ T4>`{.descname}
        :   HStore表达。返回此hstore的内容，并删除给定的密钥。请注意，该密钥可能是SQLA表达式。

        ` has_all  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试jsonb中是否存在所有键

        ` has_any  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试jsonb中是否存在任何密钥

        `对象的has_key  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试密钥的存在。请注意，该密钥可能是SQLA表达式。

        `键 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   文本数组表达式。返回键数组。

        `矩阵 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   文本数组表达式。返回[key，value]对的数组。

        `片 T0> （ T1> 阵列 T2> ） T3> ¶ T4>`{.descname}
        :   HStore表达。返回由key数组定义的hstore的子集。

        `瓦尔斯 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   文本数组表达式。返回值数组。

    ` HSTORE。 T0>  __初始化__  T1> （ T2>  text_type =无 T3> ） T4> ¶ T5 >`{.descclassname}
    :   构建一个新的[`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")。

        参数：

        **text\_type**
        [¶](#sqlalchemy.dialects.postgresql.HSTORE.params.text_type) -

        应该用于索引值的类型。默认为[`types.Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")。

        版本1.1.0中的新功能

    ` HSTORE。 T0>  comparator_factory  T1> ¶ T2>`{.descclassname}
    :   [`Comparator`](#sqlalchemy.dialects.postgresql.HSTORE.Comparator "sqlalchemy.dialects.postgresql.HSTORE.Comparator")的别名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `hstore`{.descname} （ *\* args*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.postgresql.hstore "Permalink to this definition")*
:   基础：[`sqlalchemy.sql.functions.GenericFunction`](core_functions.html#sqlalchemy.sql.functions.GenericFunction "sqlalchemy.sql.functions.GenericFunction")

    使用Postgresql `hstore()`函数在SQL表达式内构建hstore值。

    [`hstore`](#sqlalchemy.dialects.postgresql.hstore "sqlalchemy.dialects.postgresql.hstore")函数接受Postgresql文档中描述的一个或两个参数。

    例如。：

        from sqlalchemy.dialects.postgresql import array, hstore

        select([hstore('key1', 'value1')])

        select([
                hstore(
                    array(['key1', 'key2', 'key3']),
                    array(['value1', 'value2', 'value3'])
                )
            ])

    0.8版本中的新功能

    也可以看看

    [`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")
    - the Postgresql `HSTORE` datatype.

    `型 T0> ¶ T1>`{.descname}
    :   [`HSTORE`](#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")的别名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `INET`{.descname} [¶](#sqlalchemy.dialects.postgresql.INET "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `INTERVAL`{.descname} （ *precision = None* ） T5\> [¶ T6\>](#sqlalchemy.dialects.postgresql.INTERVAL "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    Postgresql INTERVAL类型。

    所有DBAPI可能不支持INTERVAL类型。已知在psycopg2上工作，而不是在pg8000或zxjdbc上工作。

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `JSON`{.descname} （ *none\_as\_null = False*，*astext\_type =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.postgresql.JSON "Permalink to this definition")*
:   基础：[`sqlalchemy.types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")

    表示Postgresql JSON类型。

    这种类型是核心级[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型的特化。请务必阅读[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")的文档以获取有关处理NULL值和ORM使用的重要提示。

    在版本1.1中更改： [`postgresql.JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")现在是新的[`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")类型的Postgresql特定专用。

    由Postgresql版本的[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")提供的运算符包括：

    -   索引操作（`->`运算符）：

            data_table.c.data['some key']

            data_table.c.data[5]

    -   返回文本的索引操作（`->>`运算符）：

            data_table.c.data['some key'].astext == 'some value'

    -   使用CAST进行索引操作（相当于`CAST（col  - >＆gt；>＆lt； / t2> ['some key' t4> AS ＆lt； type＆gt；）`）：

            data_table.c.data['some key'].astext.cast(Integer) == 5

    -   路径索引操作（`#>`运算符）：

            data_table.c.data[('key_1', 'key_2', 5, ..., 'key_n')]

    -   返回文本的路径索引操作（`#>>`运算符）：

            data_table.c.data[('key_1', 'key_2', 5, ..., 'key_n')].astext == 'some value'

    版本1.1中更改： JSON对象上的[`ColumnElement.cast()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")运算符现在要求明确调用[`JSON.Comparator.astext`](#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")修饰符，如果演员只能使用文本字符串。

    索引操作默认返回一个默认类型默认为[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")的表达式对象，这样可以根据结果类型调用更多的面向JSON的指令。

    自定义序列化器和反序列化器在方言级别指定，即使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")。原因在于，在使用psycopg2时，DBAPI只允许在每个游标或每个连接级别使用串行器。例如。：

        engine = create_engine("postgresql://scott:tiger@localhost/test",
                                json_serializer=my_serialize_fn,
                                json_deserializer=my_deserialize_fn
                        )

    使用psycopg2方言时，使用`psycopg2.extras.register_default_json`对数据库注册json\_deserializer。

    也可以看看

    [`types.JSON`](core_type_basics.html#sqlalchemy.types.JSON "sqlalchemy.types.JSON")
    - 核心级JSON类型

    [`JSONB`](#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.dialects.postgresql.JSON.Comparator "Permalink to this definition")
    :   基础：`sqlalchemy.types.Comparator`

        为[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")定义比较操作。

        ` astext  T0> ¶ T1>`{.descname}
        :   在索引表达式中，使用SQL中呈现时的“astext”（例如“ -
            \>\>”）转换。

            例如。：

                select([data_table.c.data['some key'].astext])

            也可以看看

            [`ColumnElement.cast()`](core_sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast "sqlalchemy.sql.expression.ColumnElement.cast")

    `JSON。`{.descclassname} `__ init __`{.descname} （ *none\_as\_null = False*，*astext\_type = None* ） T5\> [¶ T6\>](#sqlalchemy.dialects.postgresql.JSON.__init__ "Permalink to this definition")
    :   构建一个[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")类型。

        参数：

        -   **none\_as\_null**
            [¶](#sqlalchemy.dialects.postgresql.JSON.params.none_as_null)
            -

            如果为True，则将值`None`保留为SQL
            NULL值，而不是`null`的JSON编码。请注意，当此标志为False时，[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")结构仍可用于保留NULL值：

                from sqlalchemy import null
                conn.execute(table.insert(), data=null())

            更改为0.9.8版： - 现在支持`none_as_null`和[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")以保留NULL值。

            也可以看看

            [`JSON.NULL`](core_type_basics.html#sqlalchemy.types.JSON.NULL "sqlalchemy.types.JSON.NULL")

        -   **astext\_type**
            [¶](#sqlalchemy.dialects.postgresql.JSON.params.astext_type)
            -

            在索引属性上用于[`JSON.Comparator.astext`](#sqlalchemy.dialects.postgresql.JSON.Comparator.astext "sqlalchemy.dialects.postgresql.JSON.Comparator.astext")访问器的类型。默认为[`types.Text`](core_type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")。

            版本1.1中的新功能

    ` JSON。 T0>  comparator_factory  T1> ¶ T2>`{.descclassname}
    :   [`Comparator`](#sqlalchemy.dialects.postgresql.JSON.Comparator "sqlalchemy.dialects.postgresql.JSON.Comparator")的别名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `JSONB`{.descname} （ *none\_as\_null = False*，*astext\_type =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.dialects.postgresql.JSONB "Permalink to this definition")*
:   基础：`sqlalchemy.dialects.postgresql.json.JSON`

    表示Postgresql JSONB类型。

    [`JSONB`](#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")类型存储任意的JSONB格式数据，例如：

        data_table = Table('data_table', metadata,
            Column('id', Integer, primary_key=True),
            Column('data', JSONB)
        )

        with engine.connect() as conn:
            conn.execute(
                data_table.insert(),
                data = {"key1": "value1", "key2": "value2"}
            )

    [`JSONB`](#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")类型包含[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")提供的所有操作，包括索引操作的相同行为。It
    also adds additional operators specific to JSONB, including
    [`JSONB.Comparator.has_key()`](#sqlalchemy.dialects.postgresql.JSONB.Comparator.has_key "sqlalchemy.dialects.postgresql.JSONB.Comparator.has_key"),
    [`JSONB.Comparator.has_all()`](#sqlalchemy.dialects.postgresql.JSONB.Comparator.has_all "sqlalchemy.dialects.postgresql.JSONB.Comparator.has_all"),
    [`JSONB.Comparator.has_any()`](#sqlalchemy.dialects.postgresql.JSONB.Comparator.has_any "sqlalchemy.dialects.postgresql.JSONB.Comparator.has_any"),
    [`JSONB.Comparator.contains()`](#sqlalchemy.dialects.postgresql.JSONB.Comparator.contains "sqlalchemy.dialects.postgresql.JSONB.Comparator.contains"),
    and [`JSONB.Comparator.contained_by()`](#sqlalchemy.dialects.postgresql.JSONB.Comparator.contained_by "sqlalchemy.dialects.postgresql.JSONB.Comparator.contained_by").

    与[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")类型类似，当与ORM一起使用时，[`JSONB`](#sqlalchemy.dialects.postgresql.JSONB "sqlalchemy.dialects.postgresql.JSONB")类型不检测就地更改，除非[`sqlalchemy.ext.mutable`](orm_extensions_mutable.html#module-sqlalchemy.ext.mutable "sqlalchemy.ext.mutable")扩展用来。

    自定义序列化器和反序列化器使用`json_serializer`和`json_deserializer`关键字参数与[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")类共享。这些必须使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")在方言级别指定。在使用psycopg2时，序列化程序使用基于每个连接的`psycopg2.extras.register_default_jsonb`与jsonb类型关联，与`psycopg2.extras.register_default_json`相同用于使用json类型注册这些处理程序。

    版本0.9.7中的新功能

    也可以看看

    [`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")

    *class* `比较器`{.descname} （ *expr* ） [¶](#sqlalchemy.dialects.postgresql.JSONB.Comparator "Permalink to this definition")
    :   基础：`sqlalchemy.dialects.postgresql.json.Comparator`

        为[`JSON`](#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")定义比较操作。

        ` contained_by  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试键是否是参数jsonb表达式的键的真子集。

        `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.dialects.postgresql.JSONB.Comparator.contains "Permalink to this definition") \>
        :   布尔表达式。测试键（或数组）是否是/包含参数jsonb表达式的键的超集。

        ` has_all  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试jsonb中是否存在所有键

        ` has_any  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试jsonb中是否存在任何密钥

        `对象的has_key  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。测试密钥的存在。请注意，该密钥可能是SQLA表达式。

    ` JSONB。 T0>  comparator_factory  T1> ¶ T2>`{.descclassname}
    :   [`Comparator`](#sqlalchemy.dialects.postgresql.JSONB.Comparator "sqlalchemy.dialects.postgresql.JSONB.Comparator")的别名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `MACADDR`{.descname} [¶](#sqlalchemy.dialects.postgresql.MACADDR "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `OID`{.descname} [¶](#sqlalchemy.dialects.postgresql.OID "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    提供Postgresql OID类型。

    版本0.9.5中的新功能

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `REAL`{.descname} （ *precision = None*，*asdecimal = False*，*decimal\_return\_scale = None*，*\*\* kwargs* ） [](#sqlalchemy.dialects.postgresql.REAL "Permalink to this definition")
:   基础：[`sqlalchemy.types.Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")

    SQL REAL类型。plain

     `__init__`{.descname}(*precision=None*, *asdecimal=False*, *decimal\_return\_scale=None*, *\*\*kwargs*)[¶](#sqlalchemy.dialects.postgresql.REAL.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](core_type_basics.html#sqlalchemy.types.Float.__init__ "sqlalchemy.types.Float.__init__")
        *method of* [`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")

        构建一个浮动。

        参数：

        -   **precision**[¶](#sqlalchemy.dialects.postgresql.REAL.params.precision)
            – the numeric precision for use in DDL
            `CREATE TABLE`.
        -   **asdecimal**[¶](#sqlalchemy.dialects.postgresql.REAL.params.asdecimal)
            – the same flag as that of [`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric"),
            but defaults to `False`.
            请注意，将此标志设置为`True`会导致浮点转换。
        -   **decimal\_return\_scale**
            [¶](#sqlalchemy.dialects.postgresql.REAL.params.decimal_return_scale)
            -

            从float到Python小数转换时使用的默认缩放比例。由于十进制不准确性，浮点值通常会长得多，并且大多数浮点数据库类型没有“缩放”的概念，所以默认情况下，浮点类型在转换时会查找前十个小数位。指定此值将覆盖该长度。请注意，包含“scale”的MySQL浮点类型将使用“scale”作为decimal\_return\_scale的默认值（如果未另外指定）。

            版本0.9.0中的新功能

        -   **\*\* kwargs**
            [¶](#sqlalchemy.dialects.postgresql.REAL.params.**kwargs) -
            不建议使用。其他参数在这里被默认的[`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")类型忽略。对于支持附加参数的特定于数据库的浮点数，请参阅该方言的文档以获取详细信息，例如[`sqlalchemy.dialects.mysql.FLOAT`](mysql.html#sqlalchemy.dialects.mysql.FLOAT "sqlalchemy.dialects.mysql.FLOAT")。

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `TSVECTOR`{.descname} [¶](#sqlalchemy.dialects.postgresql.TSVECTOR "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    [`postgresql.TSVECTOR`](#sqlalchemy.dialects.postgresql.TSVECTOR "sqlalchemy.dialects.postgresql.TSVECTOR")类型实现了Postgresql文本搜索类型TSVECTOR。plain

    它可以用来对自然语言文档进行全文查询。

    版本0.9.0中的新功能

    也可以看看

    [Full Text Search](#postgresql-match)

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `UUID`{.descname} （ *as\_uuid = False* ） T5\> [¶ T6\>](#sqlalchemy.dialects.postgresql.UUID "Permalink to this definition")
:   基础：[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    Postgresql UUID类型。

    表示UUID列的类型，可以将数据解释为由DBAPI本机返回或作为Python
    uuid对象。

    所有DBAPI可能不支持UUID类型。已知psycopg2而不是pg8000。

    ` __初始化__  T0> （ T1>  as_uuid =假 T2> ） T3> ¶ T4>`{.descname}
    :   构建一个UUID类型。

        参数：

        **as\_uuid=False**[¶](#sqlalchemy.dialects.postgresql.UUID.params.as_uuid)
        – if True, values will be interpreted as Python uuid objects,
        converting to/from string via the DBAPI.

### 范围类型[¶](#range-types "Permalink to this headline")

PostgreSQL 9.2以后的新范围列类型可以通过以下类型来满足：

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `INT4RANGE`{.descname} [¶](#sqlalchemy.dialects.postgresql.INT4RANGE "Permalink to this definition")
:   基础：[`sqlalchemy.dialects.postgresql.ranges.RangeOperators`](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "sqlalchemy.dialects.postgresql.ranges.RangeOperators")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql INT4RANGE类型。plainplain

    0.8.2版本中的新功能

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `INT8RANGE`{.descname} [¶](#sqlalchemy.dialects.postgresql.INT8RANGE "Permalink to this definition")
:   基础：[`sqlalchemy.dialects.postgresql.ranges.RangeOperators`](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "sqlalchemy.dialects.postgresql.ranges.RangeOperators")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql INT8RANGE类型。

    0.8.2版本中的新功能

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `NUMRANGE`{.descname} [¶](#sqlalchemy.dialects.postgresql.NUMRANGE "Permalink to this definition")
:   基础：[`sqlalchemy.dialects.postgresql.ranges.RangeOperators`](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "sqlalchemy.dialects.postgresql.ranges.RangeOperators")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql NUMRANGE类型。plain

    0.8.2版本中的新功能

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `DATERANGE`{.descname} [¶](#sqlalchemy.dialects.postgresql.DATERANGE "Permalink to this definition")
:   基础：[`sqlalchemy.dialects.postgresql.ranges.RangeOperators`](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "sqlalchemy.dialects.postgresql.ranges.RangeOperators")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql DATERANGE类型。

    0.8.2版本中的新功能

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `TSRANGE`{.descname} [¶](#sqlalchemy.dialects.postgresql.TSRANGE "Permalink to this definition")
:   基础：[`sqlalchemy.dialects.postgresql.ranges.RangeOperators`](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "sqlalchemy.dialects.postgresql.ranges.RangeOperators")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql TSRANGE类型。plain

    0.8.2版本中的新功能

*class* `sqlalchemy.dialects.postgresql。`{.descclassname} `TSTZRANGE`{.descname} [¶](#sqlalchemy.dialects.postgresql.TSTZRANGE "Permalink to this definition")
:   基础：[`sqlalchemy.dialects.postgresql.ranges.RangeOperators`](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "sqlalchemy.dialects.postgresql.ranges.RangeOperators")，[`sqlalchemy.types.TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")

    表示Postgresql TSTZRANGE类型。

    0.8.2版本中的新功能

上面的类型通过以下mixin获得大部分功能：

*class* `sqlalchemy.dialects.postgresql.ranges。`{.descclassname} `RangeOperators`{.descname} [¶](#sqlalchemy.dialects.postgresql.ranges.RangeOperators "Permalink to this definition")
:   该混合为范围函数和操作符的[postgres文档](http://www.postgresql.org/docs/devel/static/functions-range.html)的表 9-44 中列出的范围操作符提供了功能。它被`postgres`方言中提供的所有范围类型使用，并可能用于您自己创建的任何范围类型。

    对postgres文档的表9-45中列出的范围函数没有提供额外的支持。对于这些，应该使用正常的[`func()`](core_sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")对象。

    0.8.2版新增功能：支持Postgresql RANGE操作。

    *class* `comparator_factory`{.descname} （ *expr* ） [](#sqlalchemy.dialects.postgresql.ranges.RangeOperators.comparator_factory "Permalink to this definition")
    :   基础：`sqlalchemy.types.Comparator`

        定义范围类型的比较操作。

        ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果两个范围不相等，则返回true

        ` adjacent_to  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列中的范围与操作数中的范围相邻，则返回true。

        ` contained_by  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列包含在右侧操作数中，则返回true。

        `包含`{.descname} （ *其他*，*\*\* kw* ） [¶ t5 \>](#sqlalchemy.dialects.postgresql.ranges.RangeOperators.comparator_factory.contains "Permalink to this definition")
        :   布尔表达式。如果右侧操作数（可以是元素或范围）包含在列中，则返回true。

        ` not_extend_left_of  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列中的范围未扩展到操作数范围的左侧，则返回true。

        ` not_extend_right_of  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列中的范围不扩展到操作数范围的右侧，则返回true。

        `重叠 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列重叠（与右边的操作数有共同点），则返回true。

        ` strictly_left_of  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列严格保留在右侧操作数的左侧，则返回true。

        ` strictly_right_of  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   布尔表达式。如果列严格右侧操作数的右侧，则返回true。

警告

范围类型 DDL 支持应该适用于任何 Postgres
DBAPI 驱动程序，但返回的数据类型可能会有所不同。如果您使用`psycopg2`，建议在使用这些列类型之前升级到版本 2.5 或更高版本。

在实例化使用这些列类型的模型时，您应该传递您为列类型使用的DBAPI驱动程序所期望的任何数据类型。对于[`psycopg2`](http://pythonhosted.org/psycopg2/module.html#module-psycopg2 "(in Psycopg v2.6)")这些是[`NumericRange`](http://pythonhosted.org/psycopg2/extras.html#psycopg2.extras.NumericRange "(in Psycopg v2.6)")，[`DateRange`](http://pythonhosted.org/psycopg2/extras.html#psycopg2.extras.DateRange "(in Psycopg v2.6)")，[`DateTimeRange`](http://pythonhosted.org/psycopg2/extras.html#psycopg2.extras.DateTimeRange "(in Psycopg v2.6)")和[`DateTimeTZRange`](http://pythonhosted.org/psycopg2/extras.html#psycopg2.extras.DateTimeTZRange "(in Psycopg v2.6)")已经通过[`register_range()`](http://pythonhosted.org/psycopg2/extras.html#psycopg2.extras.register_range "(in Psycopg v2.6)")进行了注册。

例如：

    from psycopg2.extras import DateTimeRange
    from sqlalchemy.dialects.postgresql import TSRANGE

    class RoomBooking(Base):

        __tablename__ = 'room_booking'

        room = Column(Integer(), primary_key=True)
        during = Column(TSRANGE())

    booking = RoomBooking(
        room=101,
        during=DateTimeRange(datetime(2013, 3, 23), None)
    )

PostgreSQL 约束类型[¶](#postgresql-constraint-types "Permalink to this headline")
--------------------------------------------------------------------------------

SQLAlchemy通过[`ExcludeConstraint`](#sqlalchemy.dialects.postgresql.ExcludeConstraint "sqlalchemy.dialects.postgresql.ExcludeConstraint")类支持 Postgresql
EXCLUDE 约束：

 *class*`sqlalchemy.dialects.postgresql.`{.descclassname}`ExcludeConstraint`{.descname}(*\*elements*, *\*\*kw*)[¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint "Permalink to this definition")
:   基础：[`sqlalchemy.schema.ColumnCollectionConstraint`](core_constraints.html#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

    表级EXCLUDE约束。

    定义一个EXCLUDE约束，如[postgres文档](http://www.postgresql.org/docs/9.0/static/sql-createtable.html#SQL-CREATETABLE-EXCLUDE)中所述。

     `__init__`{.descname}(*\*elements*, *\*\*kw*)[¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.__init__ "Permalink to this definition")
    :   参数：
        -   **\*elements**[¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.*elements)
            – A sequence of two tuples of the form
            `(column, operator)` where column must
            be a column name or Column object and operator must be a
            string containing the operator to use.
        -   **name**[¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.name)
            – Optional, the in-database name of this constraint.
        -   **可延迟**
            [¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.deferrable)
            -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初**
            [¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.initially)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY
            。
        -   **使用**
            [¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.using)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出USING 。
            T0\>默认为'gist'。
        -   **其中**
            [¶](#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.where)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出WHERE 。

例如：

    from sqlalchemy.dialects.postgresql import ExcludeConstraint, TSRANGEplain

    class RoomBooking(Base):

        __tablename__ = 'room_booking'

        room = Column(Integer(), primary_key=True)
        during = Column(TSRANGE())

        __table_args__ = (
            ExcludeConstraint(('room', '='), ('during', '&&')),
        )

PostgreSQL DML 构造[¶](#postgresql-dml-constructs "Permalink to this headline")
------------------------------------------------------------------------------

 `sqlalchemy.dialects.postgresql.dml.`{.descclassname}`insert`{.descname}(*table*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.dialects.postgresql.dml.insert "Permalink to this definition")
:   构建一个新的[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")对象。

    这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`insert()`](core_dml.html#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")。

 *class*`sqlalchemy.dialects.postgresql.dml.`{.descclassname}`Insert`{.descname}(*table*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.dialects.postgresql.dml.Insert "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")

    INSERT的Postgresql特定实现。

    为特定于PG的语法添加方法，如ON CONFLICT。

    版本1.1中的新功能

    `排除 T0> ¶ T1>`{.descname}
    :   为ON CONFLICT语句提供`excluded`名称空间

        PG的ON
        CONFLICT子句允许引用将被插入的行，称为`excluded`。此属性提供此行中的所有列以供引用。

        也可以看看

        [INSERT...ON CONFLICT (Upsert)](#postgresql-insert-on-conflict)
        - 如何使用[`Insert.excluded`](#sqlalchemy.dialects.postgresql.dml.Insert.excluded "sqlalchemy.dialects.postgresql.dml.Insert.excluded")的示例

    `on_conflict_do_nothing`{.descname} （ *约束=无*，*index\_elements =无*，*index\_where =无* ） T5\> [¶ T6\>](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing "Permalink to this definition")
    :   为ON CONFLICT子句指定DO NOTHING操作。

        `constraint`和`index_elements`参数是可选的，但只能指定其中的一个参数。

        参数：

        **约束**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing.params.constraint)
        -

        表上唯一约束或排除约束的名称，或约束对象本身（如果它具有.name属性）。

        参数：

        **index\_elements**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing.params.index_elements)
        -

        由串列名称，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象或将用于推断目标索引的其他列表达式对象组成的序列。

        参数：

        **index\_where**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_nothing.params.index_where)
        -

        附加的WHERE标准可用于推断条件目标索引。

        版本1.1中的新功能

        也可以看看

        [INSERT...ON CONFLICT (Upsert)](#postgresql-insert-on-conflict)

     `on_conflict_do_update`{.descname}(*constraint=None*, *index\_elements=None*, *index\_where=None*, *set\_=None*, *where=None*)[¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update "Permalink to this definition")
    :   为ON CONFLICT子句指定DO UPDATE SET操作。

        要么使用`constraint`或`index_elements`参数，而只能指定其中的一个参数。

        参数：

        **约束**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.constraint)
        -

        表上唯一约束或排除约束的名称，或约束对象本身（如果它具有.name属性）。

        参数：

        **index\_elements**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.index_elements)
        -

        由串列名称，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象或将用于推断目标索引的其他列表达式对象组成的序列。

        参数：

        **index\_where**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.index_where)
        -

        附加的WHERE标准可用于推断条件目标索引。

        参数：

        **set \_**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.set_)
        -

        必需的参数。字典或其他映射对象，列名称作为键和表达式或文字作为值，指定要采取的`SET`动作。

        警告

        这个字典不考虑Python指定的默认UPDATE值或生成函数，例如****。使用[`Column.onupdate`](core_metadata.html#sqlalchemy.schema.Column.params.onupdate "sqlalchemy.schema.Column")指定的那些。除非在[`Insert.on_conflict_do_update.set_`](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.set_ "sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update")字典中手动指定这些值，否则这些值不会用于ON
        CONFLICT样式的UPDATE。

        参数：

        **其中**
        [¶](#sqlalchemy.dialects.postgresql.dml.Insert.on_conflict_do_update.params.where)
        -

        可选参数。If present, can be a literal SQL string or an
        acceptable expression for a `WHERE` clause
        that restricts the rows affected by `DO UPDATE SET`. 不符合`WHERE`条件的行将不会被更新（对于这些行，实际上是一个`DO NOTHING`）。

        版本1.1中的新功能

        也可以看看

        [INSERT...ON CONFLICT (Upsert)](#postgresql-insert-on-conflict)

psycopg2 [¶ T0\>](#module-sqlalchemy.dialects.postgresql.psycopg2 "Permalink to this headline")
-----------------------------------------------------------------------------------------------

通过 psycopg2 驱动程序支持 PostgreSQL 数据库。

### DBAPI [¶ T0\>](#dialect-postgresql-psycopg2-url "Permalink to this headline")

psycopg2的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/psycopg2/](http://pypi.python.org/pypi/psycopg2/)

### 连接[¶ T0\>](#dialect-postgresql-psycopg2-connect "Permalink to this headline")

连接字符串：

    postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]plain

### psycopg2连接参数[¶](#psycopg2-connect-arguments "Permalink to this headline")

被[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")接受的psycopg2特定的关键字参数是：

-   `server_side_cursors`：为支持此功能的SQL语句启用“服务器端游标”。从psycopg2的观点来看，这实质上意味着光标是使用名称创建的，例如，
    `connection.cursor（'some name'）`，其结果是结果行不会在语句执行后立即被预取并缓冲，而是留在服务器上，只根据需要进行检索。当启用此功能时，SQLAlchemy 的[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")使用特殊的行缓冲行为，从而一次可获取 100 行的组，以减少会话开销。请注意，`stream_results=True`执行选项是以每个执行为基础启用此模式的更有针对性的方式。

-   `use_native_unicode`：为每个连接启用Psycopg2“本地unicode”模式的使用。默认情况下为真。

    也可以看看

    [Disabling Native Unicode](#psycopg2-disable-native-unicode)

-   `isolation_level`：此选项适用于所有 PostgreSQL 方言，包括使用 psycopg2 方言时的`AUTOCOMMIT`隔离级别。

    也可以看看

    [Psycopg2 Transaction Isolation Level](#psycopg2-isolation-level)

-   `client_encoding`：使用 psycopg2 的`set_client_encoding()`方法以 libpq 无关的方式设置客户端编码。

    也可以看看

    [Unicode with Psycopg2](#psycopg2-unicode)

### Unix域连接[¶](#unix-domain-connections "Permalink to this headline")

psycopg2 支持通过 Unix 域连接进行连接。当省略 URL 的`host`部分时，SQLAlchemy 将`None`传递给psycopg2，psycopg2指定了Unix域通信而不是TCP / IP通信：

    create_engine("postgresql+psycopg2://user:password@/dbname")

默认情况下，使用的套接字文件将连接到`/tmp`中的 Unix 域套接字，或者在构建 PostgreSQL 时指定任何套接字目录。通过使用`host`作为附加关键字参数，可以通过将路径名传递给psycopg2来覆盖此值：

    create_engine("postgresql+psycopg2://user:password@/dbname?host=/var/lib/postgresql")plain

也可以看看：

[PQconnectdbParams
T0\>](http://www.postgresql.org/docs/9.1/static/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS)

### 每个语句/连接执行选项[¶](#per-statement-connection-execution-options "Permalink to this headline")

与[`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")，[`Executable.execution_options()`](core_selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")，[`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")一起使用时，以下 DBAPI 特定选项将得到遵守。除了那些不特定于 DBAPI 的：

-   `isolation_level` - 为[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的生命周期设置事务隔离级别（只能在连接上设置，而不能在语句或查询中设置）。请参阅[Psycopg2
    Transaction Isolation Level](#psycopg2-isolation-level)。

-   `stream_results` -
    启用或禁用psycopg2服务器端游标的使用 -
    此功能使用“命名”游标与特殊结果处理方法结合使用，以便结果行不会被完全缓冲。如果`None`或未设置，则使用[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的`server_side_cursors`选项。

-   `max_row_buffer` -
    使用`stream_results`时，是一个整数值，指定一次缓冲的最大行数。这由`BufferedRowResultProxy`解释，如果省略，则缓冲区将增长以最终一次存储 1000 行。

    版本1.0.6中的新功能

### Unicode与Psycopg2 [¶](#unicode-with-psycopg2 "Permalink to this headline")

默认情况下，psycopg2驱动程序使用`psycopg2.extensions.UNICODE`扩展名，以便 DBAPI 直接接收并返回所有字符串作为 Python Unicode 对象
-
SQLAlchemy无需更改即可传递这些值。Psycopg2将根据当前的“客户端编码”设置对字符串值进行编码/解码；默认情况下，这是`postgresql.conf`文件中的值，通常默认为`SQL_ASCII`。通常，这可以更改为`utf8`，作为更有用的默认值：

    # postgresql.conf file

    # client_encoding = sql_ascii # actually, defaults to database
                                 # encoding
    client_encoding = utf8

影响客户端编码的第二种方法是在本地将其设置在 Psycopg2 中。SQLAlchemy 将根据传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的值使用`client_encoding`参数在所有新连接上调用 psycopg2 的[`connection.set_client_encoding()`](http://pythonhosted.org/psycopg2/connection.html#connection.set_client_encoding "(in Psycopg v2.6)")方法：

    # set_client_encoding() setting;
    # works for *all* Postgresql versions
    engine = create_engine("postgresql://user:pass@host/dbname",
                           client_encoding='utf8')

这将覆盖Postgresql客户端配置中指定的编码。When using the parameter in
this way, the psycopg2 driver emits
`SET client_encoding TO 'utf8'` on the connection
explicitly, and works in all Postgresql versions.

请注意，传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的`client_encoding`设置与最近添加的`client_encoding`参数**不一样**现在直接由 libpq 支持。当将`client_encoding`直接传递给`psycopg2.connect()`，并使用[`create_engine.connect_args`](core_engines.html#sqlalchemy.create_engine.params.connect_args "sqlalchemy.create_engine")参数传递 SQLAlchemy 时，

    # libpq direct parameter setting;
    # only works for Postgresql **9.1 and above**
    engine = create_engine("postgresql://user:pass@host/dbname",
                           connect_args={'client_encoding': 'utf8'})

    # using the query string is equivalent
    engine = create_engine("postgresql://user:pass@host/dbname?client_encoding=utf8")

以上参数仅添加到 Postgresql
9.1 版本的 libpq 中，因此使用先前的方法更适合跨版本支持。

#### 禁用本机Unicode [¶](#disabling-native-unicode "Permalink to this headline")

还可以指示 SQLAlchemy 跳过 psycopg2 `UNICODE`扩展名的使用，并使用其自己的 unicode 编码/解码服务，这些服务通常只保留给那些不直接完全支持 unicode 的 DBAPI。将`use_native_unicode=False`传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")将禁止使用`psycopg2.extensions.UNICODE`。SQLAlchemy将使用[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")
`encoding`参数的值将数据本身编码为 Python 字节串，并在返回的过程中使用字节进行强制转换，默认值为`utf-8`由于大多数 DBAPI 现在完全支持 unicode，因此 SQLAlchemy 自己的 unicode 编码/解码功能正逐渐过时。

### 绑定参数样式[¶](#bound-parameter-styles "Permalink to this headline")

psycopg2 方言的默认参数样式是“pyformat”，其中 SQL 使用`%(paramname)s`样式呈现。这种格式的局限性在于它不能适应实际包含百分号或括号符号的参数名称的不寻常情况；因为SQLAlchemy在许多情况下会根据列的名称生成绑定参数名称，所以在列名中出现这些字符会导致问题。

对于[`schema.Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的问题有两种解决方案，它包含名称中的这些字符之一。一种是为具有这种名称的列指定[`schema.Column.key`](core_metadata.html#sqlalchemy.schema.Column.params.key "sqlalchemy.schema.Column")：

    measurement = Table('measurement', metadata,plain
        Column('Size (meters)', Integer, key='size_meters')
    )

Above, an INSERT statement such as `measurement.insert()` will use `size_meters` as the parameter
name, and a SQL expression such as
`measurement.c.size_meters > 10` will derive the
bound parameter name from the `size_meters` key as
well.

版本 1.0.0 更改： -
当 SQL 表达式中创建匿名绑定参数时，SQL 表达式将使用`Column.key`作为命名的来源；此前，此行为仅适用于[`Table.insert()`](core_metadata.html#sqlalchemy.schema.Table.insert "sqlalchemy.schema.Table.insert")和[`Table.update()`](core_metadata.html#sqlalchemy.schema.Table.update "sqlalchemy.schema.Table.update")参数名称。

另一种解决方案是使用位置格式；
psycopg2 允许使用“格式”参数样式，它可以传递给[`create_engine.paramstyle`](core_engines.html#sqlalchemy.create_engine.params.paramstyle "sqlalchemy.create_engine")：

    engine = create_engine(plain
        'postgresql://scott:tiger@localhost:5432/test', paramstyle='format')

用上面的引擎，而不是像这样的陈述：

    INSERT INTO measurement ("Size (meters)") VALUES (%(Size (meters))s)plain
    {'Size (meters)': 1}

我们反而看到：

    INSERT INTO measurement ("Size (meters)") VALUES (%s)plain
    (1, )

如上所述，字典样式被转换成具有位置样式的元组。

### 交易[¶ T0\>](#transactions "Permalink to this headline")

psycopg2方言完全支持SAVEPOINT和两阶段提交操作。

### Psycopg2事务隔离级别[¶](#psycopg2-transaction-isolation-level "Permalink to this headline")

As discussed in [Transaction Isolation
Level](#postgresql-isolation-level), all Postgresql dialects support
setting of transaction isolation level both via the
`isolation_level` parameter passed to
[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine"),
as well as the `isolation_level` argument used by
[`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options").
当使用 psycopg2 方言时，这些选项使用 psycopg2 的`set_isolation_level()`连接方法，而不是发出 Postgresql 指令；这是因为无论如何 psycopg2 的 API 级别设置总是在每个事务开始时发出。

psycopg2方言支持这些常量的隔离级别：

-   `READ COMMITTED`
-   `READ UNCOMMITTED`
-   `REPEATABLE READ`
-   `SERIALIZABLE`
-   `AUTOCOMMIT`

0.8.2 版本中的新功能：在使用 psycopg2 时支持 AUTOCOMMIT 隔离级别。

也可以看看

[Transaction Isolation Level](#postgresql-isolation-level)

[pg8000 Transaction Isolation Level](#pg8000-isolation-level)

### 注意记录[¶](#notice-logging "Permalink to this headline")

psycopg2方言将通过`sqlalchemy.dialects.postgresql`记录器记录Postgresql NOTICE消息：

    import logging
    logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)

### HSTORE类型[¶](#id5 "Permalink to this headline")

`psycopg2`
DBAPI 包含一个本地处理 HSTORE 类型编组的扩展。当使用 psycopg2 版本 2.4 或更高版本时，SQLAlchemy
psycopg2 方言将默认启用此扩展，并且检测到目标数据库已将 HSTORE 类型设置为使用。换句话说，当方言进行第一次连接时，执行如下的一个序列：

1.  使用`psycopg2.extras.HstoreAdapter.get_oids()`请求可用的 HSTORE
    oid。如果这个函数返回一个 HSTORE 标识符列表，然后我们确定存在`HSTORE`扩展名。This function is **skipped** if the version of
    psycopg2 installed is less than version 2.4.
2.  If the `use_native_hstore` flag is at its
    default of `True`, and we’ve detected that
    `HSTORE` oids are available, the
    `psycopg2.extensions.register_hstore()`
    extension is invoked for all connections.

无论 SQL 中的目标列的类型如何，`register_hstore()`扩展名都具有**所有Python字典都被接受为参数的效果**。字典通过这种扩展转换为文本HSTORE表达式。如果不需要此行为，请通过将`use_native_hstore`设置为`False`来禁用hstore扩展的使用，如下所示：

    engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test",
                use_native_hstore=False)

当不使用`psycopg2.extensions.register_hstore()`扩展名时，仍然支持`HSTORE`类型**。**它仅仅意味着 Python 字典和 HSTORE 字符串格式（在参数端和结果端）之间的强制将发生在 SQLAlchemy 自己的编组逻辑中，而不是`psycopg2`，它可能更多高性能。

pg8000 [¶ T0\>](#module-sqlalchemy.dialects.postgresql.pg8000 "Permalink to this headline")
-------------------------------------------------------------------------------------------

通过 pg8000 驱动程序支持 PostgreSQL 数据库。

### DBAPI [¶ T0\>](#dialect-postgresql-pg8000-url "Permalink to this headline")

有关pg8000的文档和下载信息（如果适用），请访问：[https://pythonhosted.org/pg8000/](https://pythonhosted.org/pg8000/)

### 连接[¶ T0\>](#dialect-postgresql-pg8000-connect "Permalink to this headline")

连接字符串：

    postgresql+pg8000://user:password@host:port/dbname[?key=value&key=value...]

### Unicode的[¶ T0\>](#unicode "Permalink to this headline")

pg8000将使用PostgreSQL `client_encoding`参数对它和服务器之间的字符串值进行编码/解码；默认情况下，这是`postgresql.conf`文件中的值，通常默认为`SQL_ASCII`。通常，这可以更改为`utf-8`，作为更有用的默认值：

    #client_encoding = sql_ascii # actually, defaults to database
                                 # encoding
    client_encoding = utf8

通过执行SQL，可以为会话覆盖`client_encoding`：

将CLIENT\_ENCODING 设置为'utf8'；

SQLAlchemy 将基于使用`client_encoding`参数传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")的所有新连接执行此SQL：

    engine = create_engine(plainplainplain
        "postgresql+pg8000://user:pass@host/dbname", client_encoding='utf8')

### pg8000事务隔离级别[¶](#pg8000-transaction-isolation-level "Permalink to this headline")

pg8000 方言提供与[psycopg2](#psycopg2-isolation-level)方言相同的隔离级别设置：

-   `READ COMMITTED`
-   `READ UNCOMMITTED`
-   `REPEATABLE READ`
-   `SERIALIZABLE`
-   `AUTOCOMMIT`

0.9.5 版本中的新功能：支持使用 pg8000 时的 AUTOCOMMIT 隔离级别。

也可以看看

[Transaction Isolation Level](#postgresql-isolation-level)

[Psycopg2 Transaction Isolation Level](#psycopg2-isolation-level)

psycopg2cffi [¶ T0\>](#module-sqlalchemy.dialects.postgresql.psycopg2cffi "Permalink to this headline")
-------------------------------------------------------------------------------------------------------

通过 psycopg2cffi 驱动程序支持 PostgreSQL 数据库。

### DBAPI [¶ T0\>](#dialect-postgresql-psycopg2cffi-url "Permalink to this headline")

psycopg2cffi的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/psycopg2cffi/](http://pypi.python.org/pypi/psycopg2cffi/)

### 连接[¶ T0\>](#dialect-postgresql-psycopg2cffi-connect "Permalink to this headline")

连接字符串：

    postgresql+psycopg2cffi://user:password@host:port/dbname[?key=value&key=value...]plain

`psycopg2cffi` is an adaptation of
`psycopg2`, using CFFI for the C layer.
这使它适用于例如PyPy。文档符合`psycopg2`。

版本 1.0.0 中的新功能

也可以看看

[`sqlalchemy.dialects.postgresql.psycopg2`](#module-sqlalchemy.dialects.postgresql.psycopg2 "sqlalchemy.dialects.postgresql.psycopg2")

PY-的 PostgreSQL [¶ T0\>](#module-sqlalchemy.dialects.postgresql.pypostgresql "Permalink to this headline")
----------------------------------------------------------------------------------------------------------

通过py-postgresql驱动程序支持PostgreSQL数据库。

### DBAPI [¶ T0\>](#dialect-postgresql-pypostgresql-url "Permalink to this headline")

Documentation and download information (if applicable) for py-postgresql
is available at:
[http://python.projects.pgfoundry.org/](http://python.projects.pgfoundry.org/)

### 连接[¶ T0\>](#dialect-postgresql-pypostgresql-connect "Permalink to this headline")

连接字符串：

    postgresql+pypostgresql://user:password@host:port/dbname[?key=value&key=value...]

pygresql [¶ T0\>](#module-sqlalchemy.dialects.postgresql.pygresql "Permalink to this headline")
-----------------------------------------------------------------------------------------------

通过 pygresql 驱动程序支持 PostgreSQL 数据库。

### DBAPI [¶ T0\>](#dialect-postgresql-pygresql-url "Permalink to this headline")

有关 pygresql 的文档和下载信息（如果适用）可在以下网址获得：[http://www.pygresql.org/](http://www.pygresql.org/)

### 连接[¶ T0\>](#dialect-postgresql-pygresql-connect "Permalink to this headline")

连接字符串：

    postgresql+pygresql://user:password@host:port/dbname[?key=value&key=value...]

zxjdbc [¶ T0\>](#module-sqlalchemy.dialects.postgresql.zxjdbc "Permalink to this headline")
-------------------------------------------------------------------------------------------

通过 zxJDBC 为 Jython 驱动程序支持 PostgreSQL 数据库。

### DBAPI [¶ T0\>](#dialect-postgresql-zxjdbc-url "Permalink to this headline")

此数据库的驱动程序可在以下网址找到：[http://jdbc.postgresql.org/](http://jdbc.postgresql.org/)

### 连接[¶ T0\>](#dialect-postgresql-zxjdbc-connect "Permalink to this headline")

连接字符串：

    postgresql+zxjdbc://scott:tiger@localhost/dbplain
