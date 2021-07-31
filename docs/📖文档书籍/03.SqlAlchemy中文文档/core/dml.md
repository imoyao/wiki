---
title: dml
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/core/dml/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
插入、更新、删除[¶](#insert-updates-deletes "Permalink to this headline")
=========================================================================

INSERT，UPDATE 和 DELETE 语句建立在从[`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")开始的层次结构上。[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")和[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")构建了基于中间值[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")的构建。

 `sqlalchemy.sql.expression.`{.descclassname}`delete`{.descname}(*table*, *whereclause=None*, *bind=None*, *returning=None*, *prefixes=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.delete "Permalink to this definition")
:   构建[`删除`](#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete")对象.

    类似的功能可以通过[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")上的[`delete()`](selectable.html#sqlalchemy.sql.expression.TableClause.delete "sqlalchemy.sql.expression.TableClause.delete")方法获得。plainplainplainplainplainplain

    参数：

    -   **表** [¶](#sqlalchemy.sql.expression.delete.params.table) -
        从中​​删除行的表。
    -   **whereclause**[¶](#sqlalchemy.sql.expression.delete.params.whereclause)
        – A [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
        describing the `WHERE` condition of the
        `DELETE` statement.
        请注意，可以使用[`where()`](#sqlalchemy.sql.expression.Delete.where "sqlalchemy.sql.expression.Delete.where")生成方法。

    也可以看看

    [Deletes](tutorial.html#deletes) - SQL表达式教程

 `sqlalchemy.sql.expression.`{.descclassname}`insert`{.descname}(*table*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.insert "Permalink to this definition")
:   构建[`插入`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")对象.

    类似的功能可以通过 [`insert()`](selectable.html#sqlalchemy.sql.expression.TableClause.insert "sqlalchemy.sql.expression.TableClause.insert")plainplainplainplainplainplain
    方法 [`得到`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").

    参数：

    -   **table**[¶](#sqlalchemy.sql.expression.insert.params.table) –
        [`TableClause`](selectable.html#sqlalchemy.sql.expression.TableClause "sqlalchemy.sql.expression.TableClause")
        是插入的主题
    -   **values**[¶](#sqlalchemy.sql.expression.insert.params.values) –
        collection of values to be inserted; see
        [`Insert.values()`](#sqlalchemy.sql.expression.Insert.values "sqlalchemy.sql.expression.Insert.values")
        for a description of allowed formats here.
        完全可以省略；根据传递给[`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")的参数，[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")构造也将在执行时动态呈现VALUES子句。
    -   **inline**[¶](#sqlalchemy.sql.expression.insert.params.inline) –
        if True, no attempt will be made to retrieve the SQL-generated
        default values to be provided within the statement; in
        particular, this allows SQL expressions to be rendered ‘inline’
        within the statement without the need to pre-execute them
        beforehand; for backends that support “returning”, this turns
        off the “implicit returning” feature for the statement.

    如果同时存在值和编译时绑定参数，则编译时绑定参数将基于每个键覆盖值中指定的信息。

    值中的键可以是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象或它们的字符串标识符。每个键可以引用以下之一：

    -   文字数据值（即字符串，数字等））；
    -   一个Column对象；
    -   一个SELECT语句。

    如果指定了引用此`INSERT`语句表的`SELECT`语句，则该语句将与`INSERT`语句关联。

    也可以看看

    [Insert Expressions](tutorial.html#coretutorial-insert-expressions)
    - SQL表达式教程

    [Inserts, Updates and Deletes](tutorial.html#inserts-and-updates) -
    SQL表达式教程

 `sqlalchemy.sql.expression.`{.descclassname}`update`{.descname}(*table*, *whereclause=None*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *preserve\_parameter\_order=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.update "Permalink to this definition")
:   构建一个[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")对象。

    例如：plainplainplainplainplainplainplain
    ```python
    from sqlalchemy import update

    stmt = update(users).where(users.c.id==5).\
            values(name='user #5')
    ```
    类似的功能可以通过[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的[`update()`](selectable.html#sqlalchemy.sql.expression.TableClause.update "sqlalchemy.sql.expression.TableClause.update")方法来使用：

        stmt = users.update().\
                    where(users.c.id==5).\
                    values(name='user #5')

    参数：

    -   **table**[¶](#sqlalchemy.sql.expression.update.params.table) – A
        [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        object representing the database table to be updated.
    -   **whereclause**
        [¶](#sqlalchemy.sql.expression.update.params.whereclause) -

        可选SQL表达式，用于描述`UPDATE`语句的`WHERE`条件。现代应用程序可能更喜欢使用生成的[`where()`](#sqlalchemy.sql.expression.Update.where "sqlalchemy.sql.expression.Update.where")方法来指定`WHERE`子句。

        WHERE子句可以引用多个表。对于支持这种情况的数据库，将生成一个`UPDATE FROM`子句，或者在MySQL上执行多表更新。该语句将在不支持多表更新语句的数据库上失败。引用WHERE子句中其他表的SQL标准方法是使用相关子查询：

            users.update().values(name='ed').where(
                    users.c.name==select([addresses.c.email_address]).\
                                where(addresses.c.user_id==users.c.id).\
                                as_scalar()
                    )

        Changed in version 0.7.4: The WHERE clause can refer to multiple
        tables.

    -   **值** [¶](#sqlalchemy.sql.expression.update.params.values) -

        可选字典，它指定`UPDATE`的`SET`条件。如果保留为`None`，则在执行和/或编译语句期间，根据传递给语句的那些参数确定`SET`条件。当没有任何参数的独立编译时，`SET`子句为所有列生成。

        现代应用程序可能更喜欢使用生成的[`Update.values()`](#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")方法来设置UPDATE语句的值。

    -   **inline**[¶](#sqlalchemy.sql.expression.update.params.inline) –
        if True, SQL defaults present on [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects via the `default` keyword will be
        compiled ‘inline’ into the statement and not pre-executed.
        这意味着它们的值在从[`ResultProxy.last_updated_params()`](connections.html#sqlalchemy.engine.ResultProxy.last_updated_params "sqlalchemy.engine.ResultProxy.last_updated_params")返回的字典中不可用。
    -   **preserve\_parameter\_order**
        [¶](#sqlalchemy.sql.expression.update.params.preserve_parameter_order)
        -

        如果为True，则更新语句预期仅通过[`Update.values()`](#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")方法接收**参数**，并且它们必须作为Python
        `list`呈现的UPDATE语句将为维持此顺序的每个引用列发出SET子句。

        版本1.0.10中的新功能

        也可以看看

        [Parameter-Ordered
        Updates](tutorial.html#updates-order-parameters) -
        [`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志的完整示例

    如果`values`和编译时绑定参数均存在，则编译时绑定参数将基于每个键覆盖`values`中指定的信息。

    `values`中的键可以是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象或它们的字符串标识符（特别是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的“键”，通常但不一定等同于其名称”）。通常，这里使用的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象应该是要更新的表的目标[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的一部分。但是，在使用MySQL时，多表UPDATE语句可以引用来自WHERE子句中引用的任何表的列。

    在`values`中引用的值通常是：

    -   文字数据值（即字符串，数字等）
    -   一个SQL表达式，例如相关的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")，一个标量返回的[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")构造等。

    当在[`update()`](#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")结构的values子句中结合[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构时，由[`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")表示的子查询应该是*相关*到父表，即提供将子查询内部的表链接到正在更新的外部表的准则：

        users.update().values(
                name=select([addresses.c.email_address]).\
                        where(addresses.c.user_id==users.c.id).\
                        as_scalar()
            )

    也可以看看

    [Inserts, Updates and Deletes](tutorial.html#inserts-and-updates) -
    SQL表达式语言教程

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Delete`{.descname}(*table*, *whereclause=None*, *bind=None*, *returning=None*, *prefixes=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.Delete "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

    表示一个DELETE构造。plainplainplainplainplainplain

    使用[`delete()`](#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")函数创建[`Delete`](#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete")对象。

     `__init__`{.descname}(*table*, *whereclause=None*, *bind=None*, *returning=None*, *prefixes=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.Delete.__init__ "Permalink to this definition")
    :   构建一个新的[`Delete`](#sqlalchemy.sql.expression.Delete "sqlalchemy.sql.expression.Delete")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`delete()`](#sqlalchemy.sql.expression.delete "sqlalchemy.sql.expression.delete")。

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.sql.expression.Delete.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.Delete.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.sql.expression.Delete.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.sql.expression.Delete.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    `结合 T0> ¶ T1>`{.descname}
    :   *继承自* [`bind`](#sqlalchemy.sql.expression.UpdateBase.bind "sqlalchemy.sql.expression.UpdateBase.bind")
        *属性* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        返回与此[`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")或与之关联的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的“绑定”。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Delete.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Delete.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Delete.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Delete.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Delete.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Delete.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Delete.compile.params.compile_kwargs)
            -

            在所有“访问”方法中将传递给编译器的附加参数的可选字典。例如，这允许将自定义标志传递给自定义编译构造。它也用于传递`literal_binds`标志的情况：

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select([t]).where(t.c.x == 5)

                print s.compile(compile_kwargs={"literal_binds": True})

            版本0.9.0中的新功能

        也可以看看

        [How do I render SQL expressions as strings, possibly with bound
        parameters
        inlined?](faq_sqlexpressions.html#faq-sql-expression-string)

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.Delete.cte "Permalink to this definition")
    :   *继承自* [`cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](selectable.html#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.Delete.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.Delete.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](selectable.html#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.Delete.execution_options "sqlalchemy.sql.expression.Delete.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

     `params`{.descname}(*\*arg*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.Delete.params "Permalink to this definition")
    :   *inherited from the* [`params()`](#sqlalchemy.sql.expression.UpdateBase.params "sqlalchemy.sql.expression.UpdateBase.params")
        *method of* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        设置语句的参数。

        此方法在基类上引发`NotImplementedError`，并由[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")覆盖，以提供UPDATE和INSERT的SET
        / VALUES子句。

    `prefix_with`{.descname} （ *\* expr*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.Delete.prefix_with "Permalink to this definition")
    :   *继承自* [`prefix_with()`](selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with "sqlalchemy.sql.expression.HasPrefixes.prefix_with")
        *方法 [`HasPrefixes`](selectable.html#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")*

        在语句关键字后添加一个或多个表达式，即SELECT，INSERT，UPDATE或DELETE。生成。

        这用于支持后端特定的前缀关键字，例如由MySQL提供的前缀关键字。

        例如。：

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

        可以通过多次调用[`prefix_with()`](#sqlalchemy.sql.expression.Delete.prefix_with "sqlalchemy.sql.expression.Delete.prefix_with")来指定多个前缀。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.Delete.prefix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the INSERT,
            UPDATE, or DELETE keyword.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.Delete.prefix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制将该前缀的呈现仅限于该方言。

    `返回 T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
        *method of* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        在此语句中添加一个[RETURNING](glossary.html#term-returning)或等同的子句。

        例如。：

            stmt = table.update().\
                      where(table.c.data == 'value').\
                      values(status='X').\
                      returning(table.c.server_flag,
                                table.c.updated_timestamp)

            for server_flag, updated_timestamp in connection.execute(stmt):
                print(server_flag, updated_timestamp)

        给定的列表达式集合应该从作为INSERT，UPDATE或DELETE目标的表中派生。虽然[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象是典型的，但元素也可以是表达式：

            stmt = table.insert().returning(
                (table.c.first_name + " " + table.c.last_name).
                label('fullname'))

        编译后，将在语句中呈现RETURNING子句或数据库等效项。对于INSERT和UPDATE，这些值是新插入/更新的值。对于DELETE，这些值是那些被删除的行。

        执行时，要返回的列的值通过结果集可用，并可以使用[`ResultProxy.fetchone()`](connections.html#sqlalchemy.engine.ResultProxy.fetchone "sqlalchemy.engine.ResultProxy.fetchone")和类似的方法进行迭代。对于本身不支持返回值的DBAPI（即cx\_oracle），SQLAlchemy将在结果级接近此行为，以便提供合理的行为中立性。

        请注意，并非所有数据库/
        DBAPI都支持RETURNING。对于不支持的后端，编译和/或执行时会引发异常。对于那些支持它的人来说，后端的功能差异很大，包括对executemany()和其他返回多行的语句的限制。请阅读正在使用的数据库的文档说明，以确定RETURNING的可用性。

        也可以看看

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        -
        针对单个行INSERT或UPDATE的高效获取服务器端默认值和触发器的一种替代方法。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.Delete.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](selectable.html#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.Delete.self_group "sqlalchemy.sql.expression.Delete.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.Delete.self_group "sqlalchemy.sql.expression.Delete.self_group")方法仅返回self。

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Delete.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

    `其中 T0> （ T1>  whereclause  T2> ） T3> ¶ T4>`{.descname}
    :   将给定的WHERE子句添加到新返回的删除结构中。

     `with_hint`{.descname}(*text*, *selectable=None*, *dialect\_name='\*'*)[¶](#sqlalchemy.sql.expression.Delete.with_hint "Permalink to this definition")
    :   *继承自* [`with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        *方法* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        为这个INSERT / UPDATE / DELETE语句添加一个表提示给单个表。

        注意

        [`UpdateBase.with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        currently applies only to Microsoft SQL Server. 对于MySQL INSERT
        / UPDATE / DELETE提示，请使用[`UpdateBase.prefix_with()`](#sqlalchemy.sql.expression.UpdateBase.prefix_with "sqlalchemy.sql.expression.UpdateBase.prefix_with")。

        The text of the hint is rendered in the appropriate location for
        the database backend in use, relative to the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is the subject of this statement, or optionally to that of
        the given [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        passed as the `selectable` argument.

        The `dialect_name` option will limit the
        rendering of a particular hint to a particular backend.
        例如，添加仅对SQL Server有效的提示：

            mytable.insert().with_hint("WITH (PAGLOCK)", dialect_name="mssql")

        New in version 0.7.6.

        参数：

        -   **文本**
            [¶](#sqlalchemy.sql.expression.Delete.with_hint.params.text)
            - 提示的文本。
        -   **selectable**[¶](#sqlalchemy.sql.expression.Delete.with_hint.params.selectable)
            – optional [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            that specifies an element of the FROM clause within an
            UPDATE or DELETE to be the subject of the hint - applies
            only to certain backends.
        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.Delete.with_hint.params.dialect_name)
            – defaults to `*`, if specified as the
            name of a particular dialect, will apply these hints only
            when that dialect is in use.

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Insert`{.descname}(*table*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.Insert "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")

    表示一个INSERT构造。plainplain

    [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")对象是使用[`insert()`](#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")函数创建的。

    也可以看看

    [Insert Expressions](tutorial.html#coretutorial-insert-expressions)

     `__init__`{.descname}(*table*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.Insert.__init__ "Permalink to this definition")
    :   构建一个新的[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`insert()`](#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")。

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.sql.expression.Insert.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.Insert.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.sql.expression.Insert.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.sql.expression.Insert.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    `结合 T0> ¶ T1>`{.descname}
    :   *继承自* [`bind`](#sqlalchemy.sql.expression.UpdateBase.bind "sqlalchemy.sql.expression.UpdateBase.bind")
        *属性* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        返回与此[`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")或与之关联的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的“绑定”。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Insert.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Insert.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Insert.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Insert.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Insert.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Insert.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Insert.compile.params.compile_kwargs)
            -

            在所有“访问”方法中将传递给编译器的附加参数的可选字典。例如，这允许将自定义标志传递给自定义编译构造。它也用于传递`literal_binds`标志的情况：

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select([t]).where(t.c.x == 5)

                print s.compile(compile_kwargs={"literal_binds": True})

            版本0.9.0中的新功能

        也可以看看

        [How do I render SQL expressions as strings, possibly with bound
        parameters
        inlined?](faq_sqlexpressions.html#faq-sql-expression-string)

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.Insert.cte "Permalink to this definition")
    :   *继承自* [`cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](selectable.html#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.Insert.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.Insert.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](selectable.html#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.Insert.execution_options "sqlalchemy.sql.expression.Insert.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

     `from_select`{.descname}(*names*, *select*, *include\_defaults=True*)[¶](#sqlalchemy.sql.expression.Insert.from_select "Permalink to this definition")
    :   返回一个代表`INSERT ... FROM SELECT`语句的新[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")结构。

        例如。：

            sel = select([table1.c.a, table1.c.b]).where(table1.c.c > 5)
            ins = table2.insert().from_select(['a', 'b'], sel)

        参数：

        -   **names**[¶](#sqlalchemy.sql.expression.Insert.from_select.params.names)
            – a sequence of string column names or [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
            objects representing the target columns.
        -   **select**[¶](#sqlalchemy.sql.expression.Insert.from_select.params.select)
            – a [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
            construct, [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause")
            or other construct which resolves into a [`FromClause`](selectable.html#sqlalchemy.sql.expression.FromClause "sqlalchemy.sql.expression.FromClause"),
            such as an ORM [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
            object, etc.
            从此FROM子句返回的列的顺序应与作为`names`参数发送的列顺序相对应；虽然在传递到数据库之前没有检查过，但是如果这些列列表不一致，数据库通常会引发异常。
        -   **include\_defaults**
            [¶](#sqlalchemy.sql.expression.Insert.from_select.params.include_defaults)
            -

            如果为True，则在名称列表中未指定的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象（如[Column
            Insert/Update
            Defaults](defaults.html)中所述）指定的非服务器默认值和SQL表达式将呈现到INSERT和SELECT语句中，以便这些值也包含在要插入的数据中。

            注意

            一个使用Python可调用函数的Python方面的默认值只会在整个语句中调用**一次**，而**不是每行**。

            版本1.0.0中的新增功能： - [`Insert.from_select()`](#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")现在将Python端和SQL表达式列默认值显示为SELECT语句中的列，否则不包含在列表中列名称。

        在版本1.0.0中更改：使用FROM
        SELECT的INSERT意味着[`insert.inline`](#sqlalchemy.sql.expression.insert.params.inline "sqlalchemy.sql.expression.insert")标志设置为True，表示该语句不会尝试获取“最后插入的主键“或其他默认值。该语句处理任意数量的行，因此[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")访问器不适用。

        0.8.3版本中的新功能

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

     `params`{.descname}(*\*arg*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.Insert.params "Permalink to this definition")
    :   *inherited from the* [`params()`](#sqlalchemy.sql.expression.UpdateBase.params "sqlalchemy.sql.expression.UpdateBase.params")
        *method of* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        设置语句的参数。

        此方法在基类上引发`NotImplementedError`，并由[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")覆盖，以提供UPDATE和INSERT的SET
        / VALUES子句。

    `prefix_with`{.descname} （ *\* expr*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.Insert.prefix_with "Permalink to this definition")
    :   *继承自* [`prefix_with()`](selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with "sqlalchemy.sql.expression.HasPrefixes.prefix_with")
        *方法 [`HasPrefixes`](selectable.html#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")*

        在语句关键字后添加一个或多个表达式，即SELECT，INSERT，UPDATE或DELETE。生成。

        这用于支持后端特定的前缀关键字，例如由MySQL提供的前缀关键字。

        例如。：

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

        可以通过多次调用[`prefix_with()`](#sqlalchemy.sql.expression.Insert.prefix_with "sqlalchemy.sql.expression.Insert.prefix_with")来指定多个前缀。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.Insert.prefix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the INSERT,
            UPDATE, or DELETE keyword.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.Insert.prefix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制将该前缀的呈现仅限于该方言。

    ` return_defaults  T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        *方法[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")*

        利用[RETURNING](glossary.html#term-returning)子句获取服务器端表达式和默认值。

        例如。：

            stmt = table.insert().values(data='newdata').return_defaults()

            result = connection.execute(stmt)

            server_created_at = result.returned_defaults['created_at']

        当用于支持RETURNING的后端时，如果不同时使用[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")，则由SQL表达式或server-side-default生成的所有列值将被添加到任何现有的RETURNING子句中。然后，使用[`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")存取器作为字典，结果可以在结果上使用列值，该值指的是键入[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象及其`.key`

        这种方法与[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")不同之处在于：

        1.  [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")仅用于与一行匹配的INSERT或UPDATE语句。尽管一般意义上的RETURNING构造支持多行UPDATE或DELETE语句的多行，或者对于返回多行的INSERT的特殊情况（例如，来自SELECT，多值VALUES子句的INSERT），[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")仅用于“ORM样式”单行INSERT
            / UPDATE语句。当使用[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")时，语句返回的行也会隐式消耗。By
            contrast, [`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
            leaves the RETURNING result-set intact with a collection of
            any number of rows.
        2.  它与现有逻辑兼容，以获取自动生成的主键值，也称为“隐式返回”。支持RETURNING的后端将自动使用RETURNING来获取新生成的主键值；而[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")方法绕过了这种行为，[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")保持不变。
        3.  它可以被称为反对任何后端。不支持RETURNING的后端将跳过功能的使用，而不是引发异常。[`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")的返回值将为`None`

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        is used by the ORM to provide an efficient implementation for
        the `eager_defaults` feature of
        [`mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper").

        参数：

        **cols**[¶](#sqlalchemy.sql.expression.Insert.return_defaults.params.cols)
        – optional list of column key names or [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects.
        如果省略，则服务器上评估的所有列表达式都将添加到返回列表中。

        版本0.9.0中的新功能

        也可以看看

        [`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")

        [`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")

    `返回 T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
        *method of* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        在此语句中添加一个[RETURNING](glossary.html#term-returning)或等同的子句。

        例如。：

            stmt = table.update().\
                      where(table.c.data == 'value').\
                      values(status='X').\
                      returning(table.c.server_flag,
                                table.c.updated_timestamp)

            for server_flag, updated_timestamp in connection.execute(stmt):
                print(server_flag, updated_timestamp)

        给定的列表达式集合应该从作为INSERT，UPDATE或DELETE目标的表中派生。虽然[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象是典型的，但元素也可以是表达式：

            stmt = table.insert().returning(
                (table.c.first_name + " " + table.c.last_name).
                label('fullname'))

        编译后，将在语句中呈现RETURNING子句或数据库等效项。对于INSERT和UPDATE，这些值是新插入/更新的值。对于DELETE，这些值是那些被删除的行。

        执行时，要返回的列的值通过结果集可用，并可以使用[`ResultProxy.fetchone()`](connections.html#sqlalchemy.engine.ResultProxy.fetchone "sqlalchemy.engine.ResultProxy.fetchone")和类似的方法进行迭代。对于本身不支持返回值的DBAPI（即cx\_oracle），SQLAlchemy将在结果级接近此行为，以便提供合理的行为中立性。

        请注意，并非所有数据库/
        DBAPI都支持RETURNING。对于不支持的后端，编译和/或执行时会引发异常。对于那些支持它的人来说，后端的功能差异很大，包括对executemany()和其他返回多行的语句的限制。请阅读正在使用的数据库的文档说明，以确定RETURNING的可用性。

        也可以看看

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        -
        针对单个行INSERT或UPDATE的高效获取服务器端默认值和触发器的一种替代方法。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.Insert.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](selectable.html#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.Insert.self_group "sqlalchemy.sql.expression.Insert.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.Insert.self_group "sqlalchemy.sql.expression.Insert.self_group")方法仅返回self。

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Insert.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

    `值`{.descname} （ *\* args*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Insert.values "Permalink to this definition")
    :   *inherited from the* [`values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")
        *method of* [`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")

        为INSERT语句指定一个固定的VALUES子句，或者为UPDATE指定一个SET子句。

        Note that the [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
        and [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")
        constructs support per-execution time formatting of the VALUES
        and/or SET clauses, based on the arguments passed to
        [`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute").
        但是，可以使用[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")方法将特定的一组参数“修复”到语句中。

        多次调用[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")将产生一个新的结构，每个结构都修改参数列表以包含发送的新参数。在单个参数字典的典型情况下，新传递的键将替换以前构造中的相同键。在基于列表的“多值”结构的情况下，每个新的值列表都被扩展到现有的值列表中。

        参数：

        -   **\*\* kwargs**
            [¶](#sqlalchemy.sql.expression.Insert.values.params.**kwargs)
            -

            键值对表示映射到要呈现到VALUES或SET子句中的值的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的字符串键：

                users.insert().values(name="some name")

                users.update().where(users.c.id==5).values(name="some name")

        -   **\* args**
            [¶](#sqlalchemy.sql.expression.Insert.values.params.*args) -

            作为传递键/值参数的替代方法，字典，元组或字典或元组列表可以作为单个位置参数传递，以形成语句的VALUES或SET子句。接受的表单根据是[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")还是[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构而有所不同。

            对于[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构，可以传递单个字典，其工作方式与kwargs表单相同：

                users.insert().values({"name": "some name"})

                users.update().values({"name": "some new name"})

            对于任何一种形式，但对于[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")构造更典型，也接受包含表中每列的条目的元组：

                users.insert().values((5, "some name"))

            [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")结构还支持传递字典或全表元组列表，这些元组在服务器上将呈现不太常见的“多值”SQL语法
            -
            后端支持此语法，如SQLite，Postgresql，MySQL，但不一定是其他的：

                users.insert().values([
                                    {"name": "some name"},
                                    {"name": "some other name"},
                                    {"name": "yet another name"},
                                ])

            上面的表单将呈现多个VALUES语句，类似于：

                INSERT INTO users (name) VALUES
                                (:name_1),
                                (:name_2),
                                (:name_3)

            It is essential to note that **passing multiple values is
            NOT the same as using traditional executemany() form**.
            上面的语法是不常用的**特殊**语法。要针对多行发出INSERT语句，常规方法是将多个值列表传递给[`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")方法，该方法由所有数据库后端支持，并且通常对于非常高效的大量的参数。

            > 也可以看看
            >
            > [Executing Multiple
            > Statements](tutorial.html#execute-multiple) -
            > 介绍用于INSERT和其他语句的多参数集调用的传统Core方法。
            >
            > 版本1.0.0中已更改：使用多个VALUES子句（即使是长度为1的列表）的INSERT意味着[`Insert.inline`](#sqlalchemy.sql.expression.Insert.params.inline "sqlalchemy.sql.expression.Insert")标志设置为True，表明该语句不会尝试获取“最后插入的主键”或其他默认值。该语句处理任意数量的行，因此[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")访问器不适用。
            >
            > 在1.0.0版本中已更改：多值插入现在支持具有Python侧缺省值和可调参数的列，方式与“executemany”调用方式相同；可调用的是每行调用的。对于其他细节，当使用多值插入时，请参阅[Python-side
            > defaults invoked for each row invidually when using a
            > multivalued insert](changelog_migration_10.html#bug-3288)

            [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构支持一个特殊的形式，它是一个2元组的列表，当提供的时候必须和[`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")参数一起传递。这种形式导致UPDATE语句使用[`Update.values()`](#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")给出的参数顺序来呈现SET子句，而不是[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中给出的列的顺序。

            > 版本1.0.10中的新增功能： -
            > 通过[`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志增加了对参数排序的UPDATE语句的支持。
            >
            > 也可以看看
            >
            > [Parameter-Ordered
            > Updates](tutorial.html#updates-order-parameters) -
            > [`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志的完整示例

        也可以看看

        [Inserts, Updates and
        Deletes](tutorial.html#inserts-and-updates) - SQL表达式语言教程

        [`insert()`](#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")
        - 产生一个`INSERT`语句

        [`update()`](#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")
        - 产生一个`UPDATE`语句

     `with_hint`{.descname}(*text*, *selectable=None*, *dialect\_name='\*'*)[¶](#sqlalchemy.sql.expression.Insert.with_hint "Permalink to this definition")
    :   *继承自* [`with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        *方法* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        为这个INSERT / UPDATE / DELETE语句添加一个表提示给单个表。

        注意

        [`UpdateBase.with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        currently applies only to Microsoft SQL Server. 对于MySQL INSERT
        / UPDATE / DELETE提示，请使用[`UpdateBase.prefix_with()`](#sqlalchemy.sql.expression.UpdateBase.prefix_with "sqlalchemy.sql.expression.UpdateBase.prefix_with")。

        The text of the hint is rendered in the appropriate location for
        the database backend in use, relative to the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is the subject of this statement, or optionally to that of
        the given [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        passed as the `selectable` argument.

        The `dialect_name` option will limit the
        rendering of a particular hint to a particular backend.
        例如，添加仅对SQL Server有效的提示：

            mytable.insert().with_hint("WITH (PAGLOCK)", dialect_name="mssql")

        New in version 0.7.6.

        参数：

        -   **文本**
            [¶](#sqlalchemy.sql.expression.Insert.with_hint.params.text)
            - 提示的文本。
        -   **selectable**[¶](#sqlalchemy.sql.expression.Insert.with_hint.params.selectable)
            – optional [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            that specifies an element of the FROM clause within an
            UPDATE or DELETE to be the subject of the hint - applies
            only to certain backends.
        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.Insert.with_hint.params.dialect_name)
            – defaults to `*`, if specified as the
            name of a particular dialect, will apply these hints only
            when that dialect is in use.

 *class*`sqlalchemy.sql.expression.`{.descclassname}`Update`{.descname}(*table*, *whereclause=None*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *preserve\_parameter\_order=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.Update "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")

    表示更新构造。plainplain

    [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")对象是使用[`update()`](#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")函数创建的。

     `__init__`{.descname}(*table*, *whereclause=None*, *values=None*, *inline=False*, *bind=None*, *prefixes=None*, *returning=None*, *return\_defaults=False*, *preserve\_parameter\_order=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.sql.expression.Update.__init__ "Permalink to this definition")
    :   构建一个新的[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`update()`](#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")。

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.sql.expression.Update.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.Update.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.sql.expression.Update.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.sql.expression.Update.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    `结合 T0> ¶ T1>`{.descname}
    :   *继承自* [`bind`](#sqlalchemy.sql.expression.UpdateBase.bind "sqlalchemy.sql.expression.UpdateBase.bind")
        *属性* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        返回与此[`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")或与之关联的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的“绑定”。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.Update.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.Update.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.Update.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.Update.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.Update.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.Update.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.Update.compile.params.compile_kwargs)
            -

            在所有“访问”方法中将传递给编译器的附加参数的可选字典。例如，这允许将自定义标志传递给自定义编译构造。它也用于传递`literal_binds`标志的情况：

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select([t]).where(t.c.x == 5)

                print s.compile(compile_kwargs={"literal_binds": True})

            版本0.9.0中的新功能

        也可以看看

        [How do I render SQL expressions as strings, possibly with bound
        parameters
        inlined?](faq_sqlexpressions.html#faq-sql-expression-string)

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.Update.cte "Permalink to this definition")
    :   *继承自* [`cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](selectable.html#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.Update.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.Update.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](selectable.html#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.Update.execution_options "sqlalchemy.sql.expression.Update.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

     `params`{.descname}(*\*arg*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.Update.params "Permalink to this definition")
    :   *inherited from the* [`params()`](#sqlalchemy.sql.expression.UpdateBase.params "sqlalchemy.sql.expression.UpdateBase.params")
        *method of* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        设置语句的参数。

        此方法在基类上引发`NotImplementedError`，并由[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")覆盖，以提供UPDATE和INSERT的SET
        / VALUES子句。

    `prefix_with`{.descname} （ *\* expr*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.Update.prefix_with "Permalink to this definition")
    :   *继承自* [`prefix_with()`](selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with "sqlalchemy.sql.expression.HasPrefixes.prefix_with")
        *方法 [`HasPrefixes`](selectable.html#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")*

        在语句关键字后添加一个或多个表达式，即SELECT，INSERT，UPDATE或DELETE。生成。

        这用于支持后端特定的前缀关键字，例如由MySQL提供的前缀关键字。

        例如。：

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

        可以通过多次调用[`prefix_with()`](#sqlalchemy.sql.expression.Update.prefix_with "sqlalchemy.sql.expression.Update.prefix_with")来指定多个前缀。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.Update.prefix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the INSERT,
            UPDATE, or DELETE keyword.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.Update.prefix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制将该前缀的呈现仅限于该方言。

    ` return_defaults  T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        *方法[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")*

        利用[RETURNING](glossary.html#term-returning)子句获取服务器端表达式和默认值。

        例如。：

            stmt = table.insert().values(data='newdata').return_defaults()

            result = connection.execute(stmt)

            server_created_at = result.returned_defaults['created_at']

        当用于支持RETURNING的后端时，如果不同时使用[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")，则由SQL表达式或server-side-default生成的所有列值将被添加到任何现有的RETURNING子句中。然后，使用[`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")存取器作为字典，结果可以在结果上使用列值，该值指的是键入[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象及其`.key`

        这种方法与[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")不同之处在于：

        1.  [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")仅用于与一行匹配的INSERT或UPDATE语句。尽管一般意义上的RETURNING构造支持多行UPDATE或DELETE语句的多行，或者对于返回多行的INSERT的特殊情况（例如，来自SELECT，多值VALUES子句的INSERT），[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")仅用于“ORM样式”单行INSERT
            / UPDATE语句。当使用[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")时，语句返回的行也会隐式消耗。By
            contrast, [`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
            leaves the RETURNING result-set intact with a collection of
            any number of rows.
        2.  它与现有逻辑兼容，以获取自动生成的主键值，也称为“隐式返回”。支持RETURNING的后端将自动使用RETURNING来获取新生成的主键值；而[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")方法绕过了这种行为，[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")保持不变。
        3.  它可以被称为反对任何后端。不支持RETURNING的后端将跳过功能的使用，而不是引发异常。[`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")的返回值将为`None`

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        is used by the ORM to provide an efficient implementation for
        the `eager_defaults` feature of
        [`mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper").

        参数：

        **cols**[¶](#sqlalchemy.sql.expression.Update.return_defaults.params.cols)
        – optional list of column key names or [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects.
        如果省略，则服务器上评估的所有列表达式都将添加到返回列表中。

        版本0.9.0中的新功能

        也可以看看

        [`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")

        [`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")

    `返回 T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
        *method of* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        在此语句中添加一个[RETURNING](glossary.html#term-returning)或等同的子句。

        例如。：

            stmt = table.update().\
                      where(table.c.data == 'value').\
                      values(status='X').\
                      returning(table.c.server_flag,
                                table.c.updated_timestamp)

            for server_flag, updated_timestamp in connection.execute(stmt):
                print(server_flag, updated_timestamp)

        给定的列表达式集合应该从作为INSERT，UPDATE或DELETE目标的表中派生。虽然[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象是典型的，但元素也可以是表达式：

            stmt = table.insert().returning(
                (table.c.first_name + " " + table.c.last_name).
                label('fullname'))

        编译后，将在语句中呈现RETURNING子句或数据库等效项。对于INSERT和UPDATE，这些值是新插入/更新的值。对于DELETE，这些值是那些被删除的行。

        执行时，要返回的列的值通过结果集可用，并可以使用[`ResultProxy.fetchone()`](connections.html#sqlalchemy.engine.ResultProxy.fetchone "sqlalchemy.engine.ResultProxy.fetchone")和类似的方法进行迭代。对于本身不支持返回值的DBAPI（即cx\_oracle），SQLAlchemy将在结果级接近此行为，以便提供合理的行为中立性。

        请注意，并非所有数据库/
        DBAPI都支持RETURNING。对于不支持的后端，编译和/或执行时会引发异常。对于那些支持它的人来说，后端的功能差异很大，包括对executemany()和其他返回多行的语句的限制。请阅读正在使用的数据库的文档说明，以确定RETURNING的可用性。

        也可以看看

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        -
        针对单个行INSERT或UPDATE的高效获取服务器端默认值和触发器的一种替代方法。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.Update.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](selectable.html#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.Update.self_group "sqlalchemy.sql.expression.Update.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.Update.self_group "sqlalchemy.sql.expression.Update.self_group")方法仅返回self。

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Update.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

    `值`{.descname} （ *\* args*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.Update.values "Permalink to this definition")
    :   *inherited from the* [`values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")
        *method of* [`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")

        为INSERT语句指定一个固定的VALUES子句，或者为UPDATE指定一个SET子句。

        Note that the [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
        and [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")
        constructs support per-execution time formatting of the VALUES
        and/or SET clauses, based on the arguments passed to
        [`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute").
        但是，可以使用[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")方法将特定的一组参数“修复”到语句中。

        多次调用[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")将产生一个新的结构，每个结构都修改参数列表以包含发送的新参数。在单个参数字典的典型情况下，新传递的键将替换以前构造中的相同键。在基于列表的“多值”结构的情况下，每个新的值列表都被扩展到现有的值列表中。

        参数：

        -   **\*\* kwargs**
            [¶](#sqlalchemy.sql.expression.Update.values.params.**kwargs)
            -

            键值对表示映射到要呈现到VALUES或SET子句中的值的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的字符串键：

                users.insert().values(name="some name")

                users.update().where(users.c.id==5).values(name="some name")

        -   **\* args**
            [¶](#sqlalchemy.sql.expression.Update.values.params.*args) -

            作为传递键/值参数的替代方法，字典，元组或字典或元组列表可以作为单个位置参数传递，以形成语句的VALUES或SET子句。接受的表单根据是[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")还是[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构而有所不同。

            对于[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构，可以传递单个字典，其工作方式与kwargs表单相同：

                users.insert().values({"name": "some name"})

                users.update().values({"name": "some new name"})

            对于任何一种形式，但对于[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")构造更典型，也接受包含表中每列的条目的元组：

                users.insert().values((5, "some name"))

            [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")结构还支持传递字典或全表元组列表，这些元组在服务器上将呈现不太常见的“多值”SQL语法
            -
            后端支持此语法，如SQLite，Postgresql，MySQL，但不一定是其他的：

                users.insert().values([
                                    {"name": "some name"},
                                    {"name": "some other name"},
                                    {"name": "yet another name"},
                                ])

            上面的表单将呈现多个VALUES语句，类似于：

                INSERT INTO users (name) VALUES
                                (:name_1),
                                (:name_2),
                                (:name_3)

            It is essential to note that **passing multiple values is
            NOT the same as using traditional executemany() form**.
            上面的语法是不常用的**特殊**语法。要针对多行发出INSERT语句，常规方法是将多个值列表传递给[`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")方法，该方法由所有数据库后端支持，并且通常对于非常高效的大量的参数。

            > 也可以看看
            >
            > [Executing Multiple
            > Statements](tutorial.html#execute-multiple) -
            > 介绍用于INSERT和其他语句的多参数集调用的传统Core方法。
            >
            > 版本1.0.0中已更改：使用多个VALUES子句（即使是长度为1的列表）的INSERT意味着[`Insert.inline`](#sqlalchemy.sql.expression.Insert.params.inline "sqlalchemy.sql.expression.Insert")标志设置为True，表明该语句不会尝试获取“最后插入的主键”或其他默认值。该语句处理任意数量的行，因此[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")访问器不适用。
            >
            > 在1.0.0版本中已更改：多值插入现在支持具有Python侧缺省值和可调参数的列，方式与“executemany”调用方式相同；可调用的是每行调用的。对于其他细节，当使用多值插入时，请参阅[Python-side
            > defaults invoked for each row invidually when using a
            > multivalued insert](changelog_migration_10.html#bug-3288)

            [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构支持一个特殊的形式，它是一个2元组的列表，当提供的时候必须和[`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")参数一起传递。这种形式导致UPDATE语句使用[`Update.values()`](#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")给出的参数顺序来呈现SET子句，而不是[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中给出的列的顺序。

            > 版本1.0.10中的新增功能： -
            > 通过[`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志增加了对参数排序的UPDATE语句的支持。
            >
            > 也可以看看
            >
            > [Parameter-Ordered
            > Updates](tutorial.html#updates-order-parameters) -
            > [`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志的完整示例

        也可以看看

        [Inserts, Updates and
        Deletes](tutorial.html#inserts-and-updates) - SQL表达式语言教程

        [`insert()`](#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")
        - 产生一个`INSERT`语句

        [`update()`](#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")
        - 产生一个`UPDATE`语句

    `其中 T0> （ T1>  whereclause  T2> ） T3> ¶ T4>`{.descname}
    :   返回一个新的update()构造，将给定的表达式添加到其WHERE子句中，通过AND连接到现有子句（如果有的话）。

     `with_hint`{.descname}(*text*, *selectable=None*, *dialect\_name='\*'*)[¶](#sqlalchemy.sql.expression.Update.with_hint "Permalink to this definition")
    :   *继承自* [`with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        *方法* [`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

        为这个INSERT / UPDATE / DELETE语句添加一个表提示给单个表。

        注意

        [`UpdateBase.with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        currently applies only to Microsoft SQL Server. 对于MySQL INSERT
        / UPDATE / DELETE提示，请使用[`UpdateBase.prefix_with()`](#sqlalchemy.sql.expression.UpdateBase.prefix_with "sqlalchemy.sql.expression.UpdateBase.prefix_with")。

        The text of the hint is rendered in the appropriate location for
        the database backend in use, relative to the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is the subject of this statement, or optionally to that of
        the given [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        passed as the `selectable` argument.

        The `dialect_name` option will limit the
        rendering of a particular hint to a particular backend.
        例如，添加仅对SQL Server有效的提示：

            mytable.insert().with_hint("WITH (PAGLOCK)", dialect_name="mssql")

        New in version 0.7.6.

        参数：

        -   **文本**
            [¶](#sqlalchemy.sql.expression.Update.with_hint.params.text)
            - 提示的文本。
        -   **selectable**[¶](#sqlalchemy.sql.expression.Update.with_hint.params.selectable)
            – optional [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            that specifies an element of the FROM clause within an
            UPDATE or DELETE to be the subject of the hint - applies
            only to certain backends.
        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.Update.with_hint.params.dialect_name)
            – defaults to `*`, if specified as the
            name of a particular dialect, will apply these hints only
            when that dialect is in use.

*class* `sqlalchemy.sql.expression。`{.descclassname} `UpdateBase`{.descname} [¶](#sqlalchemy.sql.expression.UpdateBase "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.HasCTE`](selectable.html#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")，[`sqlalchemy.sql.base.DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")，[`sqlalchemy.sql.expression.HasPrefixes`](selectable.html#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")，[`sqlalchemy.sql.expression.Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，[`sqlalchemy.sql.expression.ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

    为`INSERT`，`UPDATE`和`DELETE`语句形成基础。plainplainplainplainplainplain

    ` __初始化__  T0> ¶ T1>`{.descname}
    :   *继承自* `__init__`
        *属性* `object`

        x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.sql.expression.UpdateBase.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.UpdateBase.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.sql.expression.UpdateBase.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.sql.expression.UpdateBase.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    `结合 T0> ¶ T1>`{.descname}
    :   返回与此[`UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")或与之关联的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的“绑定”。

    `比较`{.descname} （ *其他*，*\*\* kw* ） [t5 \>](#sqlalchemy.sql.expression.UpdateBase.compare "Permalink to this definition")
    :   *inherited from the* [`compare()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compare "sqlalchemy.sql.expression.ClauseElement.compare")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        将此ClauseElement与给定的ClauseElement进行比较。

        子类应该覆盖默认行为，这是一种直接的身份比较。

        \*\* kw是由subclass
        compare()方法消耗的参数，可用于修改比较条件。（请参阅[`ColumnElement`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")）

    `编译`{.descname} （ *bind = None*，*dialect = None*，*\*\* kw* ） T5\> [¶ T6\>](#sqlalchemy.sql.expression.UpdateBase.compile "Permalink to this definition")
    :   *inherited from the* [`compile()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        编译这个SQL表达式。

        返回值是一个[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象。对返回值调用`str()`或`unicode()`将产生结果的字符串表示形式。[`Compiled`](internals.html#sqlalchemy.engine.interfaces.Compiled "sqlalchemy.engine.interfaces.Compiled")对象还可以使用`params`访问器返回一个绑定参数名称和值的字典。

        参数：

        -   **bind**[¶](#sqlalchemy.sql.expression.UpdateBase.compile.params.bind)
            – An `Engine` or `Connection` from which a `Compiled` will
            be acquired. 这个参数优先于这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎，如果有的话。
        -   **column\_keys**[¶](#sqlalchemy.sql.expression.UpdateBase.compile.params.column_keys)
            – Used for INSERT and UPDATE statements, a list of column
            names which should be present in the VALUES clause of the
            compiled statement. 如果`None`，则呈现目标表格对象中的所有列。
        -   **dialect**[¶](#sqlalchemy.sql.expression.UpdateBase.compile.params.dialect)
            – A `Dialect` instance from which a
            `Compiled` will be acquired.
            该参数优先于bind参数以及[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的绑定引擎（如果有的话）。
        -   **inline**[¶](#sqlalchemy.sql.expression.UpdateBase.compile.params.inline)
            – Used for INSERT statements, for a dialect which does not
            support inline retrieval of newly generated primary key
            columns, will force the expression used to create the new
            primary key value to be rendered inline within the INSERT
            statement’s VALUES clause.
            这通常是指序列执行，但也可能指与主键Column关联的任何服务器端默认生成函数。
        -   **compile\_kwargs**
            [¶](#sqlalchemy.sql.expression.UpdateBase.compile.params.compile_kwargs)
            -

            在所有“访问”方法中将传递给编译器的附加参数的可选字典。例如，这允许将自定义标志传递给自定义编译构造。它也用于传递`literal_binds`标志的情况：

                from sqlalchemy.sql import table, column, select

                t = table('t', column('x'))

                s = select([t]).where(t.c.x == 5)

                print s.compile(compile_kwargs={"literal_binds": True})

            版本0.9.0中的新功能

        也可以看看

        [How do I render SQL expressions as strings, possibly with bound
        parameters
        inlined?](faq_sqlexpressions.html#faq-sql-expression-string)

     `cte`{.descname}(*name=None*, *recursive=False*)[¶](#sqlalchemy.sql.expression.UpdateBase.cte "Permalink to this definition")
    :   *继承自* [`cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")
        *方法* [`HasCTE`](selectable.html#sqlalchemy.sql.expression.HasCTE "sqlalchemy.sql.expression.HasCTE")

        返回一个新的[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")或公共表表达式实例。

        公用表表达式是一种SQL标准，通过使用一个名为“WITH”的子句，SELECT语句可以使用与主语句一起指定的次要语句。有关UNION的特殊语义也可用于允许“递归”查询，其中SELECT语句可以在先前已选择的一组行上进行绘制。

        CTE也可以应用于DML构造对某些数据库的UPDATE，INSERT和DELETE，与RETURNING一起作为CTE行的来源以及CTE行的使用者。

        SQLAlchemy将[`CTE`](selectable.html#sqlalchemy.sql.expression.CTE "sqlalchemy.sql.expression.CTE")对象检测为与[`Alias`](selectable.html#sqlalchemy.sql.expression.Alias "sqlalchemy.sql.expression.Alias")对象类似的对象，作为要传递到语句的FROM子句的特殊元素以及顶部的WITH子句的声明。

        在版本1.1中进行了更改：添加了对CTE，CTE添加到UPDATE / INSERT /
        DELETE的UPDATE / INSERT / DELETE的支持。

        参数：

        -   **name**[¶](#sqlalchemy.sql.expression.UpdateBase.cte.params.name)
            – name given to the common table expression.
            像`_FromClause.alias()`一样，名称可以保留为`None`，在这种情况下，查询编译时将使用匿名符号。
        -   **recursive**[¶](#sqlalchemy.sql.expression.UpdateBase.cte.params.recursive)
            – if `True`, will render
            `WITH RECURSIVE`.
            递归公用表表达式旨在与UNION
            ALL结合使用，以便从已选择的行中派生行。

        以下示例包含两篇来自Postgresql的文档，位于[http://www.postgresql.org/docs/current/static/queries-with.html](http://www.postgresql.org/docs/current/static/queries-with.html)以及其他示例。

        例1，非递归：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            orders = Table('orders', metadata,
                Column('region', String),
                Column('amount', Integer),
                Column('product', String),
                Column('quantity', Integer)
            )

            regional_sales = select([
                                orders.c.region,
                                func.sum(orders.c.amount).label('total_sales')
                            ]).group_by(orders.c.region).cte("regional_sales")


            top_regions = select([regional_sales.c.region]).\
                    where(
                        regional_sales.c.total_sales >
                        select([
                            func.sum(regional_sales.c.total_sales)/10
                        ])
                    ).cte("top_regions")

            statement = select([
                        orders.c.region,
                        orders.c.product,
                        func.sum(orders.c.quantity).label("product_units"),
                        func.sum(orders.c.amount).label("product_sales")
                ]).where(orders.c.region.in_(
                    select([top_regions.c.region])
                )).group_by(orders.c.region, orders.c.product)

            result = conn.execute(statement).fetchall()

        例2，与RECURSIVE：

            from sqlalchemy import (Table, Column, String, Integer,
                                    MetaData, select, func)

            metadata = MetaData()

            parts = Table('parts', metadata,
                Column('part', String),
                Column('sub_part', String),
                Column('quantity', Integer),
            )

            included_parts = select([
                                parts.c.sub_part,
                                parts.c.part,
                                parts.c.quantity]).\
                                where(parts.c.part=='our part').\
                                cte(recursive=True)


            incl_alias = included_parts.alias()
            parts_alias = parts.alias()
            included_parts = included_parts.union_all(
                select([
                    parts_alias.c.sub_part,
                    parts_alias.c.part,
                    parts_alias.c.quantity
                ]).
                    where(parts_alias.c.part==incl_alias.c.sub_part)
            )

            statement = select([
                        included_parts.c.sub_part,
                        func.sum(included_parts.c.quantity).
                          label('total_quantity')
                    ]).\
                    group_by(included_parts.c.sub_part)

            result = conn.execute(statement).fetchall()

        例3，使用带CTE的UPDATE和INSERT的upsert：

            orders = table(
                'orders',
                column('region'),
                column('amount'),
                column('product'),
                column('quantity')
            )

            upsert = (
                orders.update()
                .where(orders.c.region == 'Region1')
                .values(amount=1.0, product='Product1', quantity=1)
                .returning(*(orders.c._all_columns)).cte('upsert'))

            insert = orders.insert().from_select(
                orders.c.keys(),
                select([
                    literal('Region1'), literal(1.0),
                    literal('Product1'), literal(1)
                ).where(exists(upsert.select()))
            )

            connection.execute(insert)

        也可以看看

        [`orm.query.Query.cte()`](orm_query.html#sqlalchemy.orm.query.Query.cte "sqlalchemy.orm.query.Query.cte")
        - [`HasCTE.cte()`](selectable.html#sqlalchemy.sql.expression.HasCTE.cte "sqlalchemy.sql.expression.HasCTE.cte")的ORM版本。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    `执行 tt> （ * multiparams，** params ） T5>`{.descname}
    :   *继承自* [`execute()`](selectable.html#sqlalchemy.sql.expression.Executable.execute "sqlalchemy.sql.expression.Executable.execute")
        *方法* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")。

    ` execution_options  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`execution_options()`](selectable.html#sqlalchemy.sql.expression.Executable.execution_options "sqlalchemy.sql.expression.Executable.execution_options")
        *方法 tt\> [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")*

        为执行期间生效的语句设置非SQL选项。

        执行选项可以在每个语句或每个[`Connection`](connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的基础上设置。此外，[`Engine`](connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")和ORM
        [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供对执行选项的访问，而这些执行选项在连接时进行配置。

        [`execution_options()`](#sqlalchemy.sql.expression.UpdateBase.execution_options "sqlalchemy.sql.expression.UpdateBase.execution_options")方法是生成的。返回此语句的新实例，其中包含以下选项：

            statement = select([table.c.x, table.c.y])
            statement = statement.execution_options(autocommit=True)

        请注意，只有一部分可能的执行选项可以应用于语句 -
        这些选项包括“autocommit”和“stream\_results”，但不包括“isolation\_level”或“c​​ompiled\_cache”。有关可能的选项的完整列表，请参阅[`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")。

        也可以看看

        [`Connection.execution_options()`](connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")

        [`Query.execution_options()`](orm_query.html#sqlalchemy.orm.query.Query.execution_options "sqlalchemy.orm.query.Query.execution_options")

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.get_children "sqlalchemy.sql.expression.ClauseElement.get_children")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的直接子元素。

        这用于访问遍历。

        \*\*
        kwargs可能包含更改返回的集合的标志，例如为了减少更大的遍历而返回项目的子集，或者从不同的上下文返回子项目（例如模式级集合而不是子句-水平）。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

     `params`{.descname}(*\*arg*, *\*\*kw*)[¶](#sqlalchemy.sql.expression.UpdateBase.params "Permalink to this definition")
    :   设置语句的参数。

        此方法在基类上引发`NotImplementedError`，并由[`ValuesBase`](#sqlalchemy.sql.expression.ValuesBase "sqlalchemy.sql.expression.ValuesBase")覆盖，以提供UPDATE和INSERT的SET
        / VALUES子句。

    `prefix_with`{.descname} （ *\* expr*，*\*\* kw* ） [T5\>](#sqlalchemy.sql.expression.UpdateBase.prefix_with "Permalink to this definition")
    :   *继承自* [`prefix_with()`](selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with "sqlalchemy.sql.expression.HasPrefixes.prefix_with")
        *方法 [`HasPrefixes`](selectable.html#sqlalchemy.sql.expression.HasPrefixes "sqlalchemy.sql.expression.HasPrefixes")*

        在语句关键字后添加一个或多个表达式，即SELECT，INSERT，UPDATE或DELETE。生成。

        这用于支持后端特定的前缀关键字，例如由MySQL提供的前缀关键字。

        例如。：

            stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

        可以通过多次调用[`prefix_with()`](#sqlalchemy.sql.expression.UpdateBase.prefix_with "sqlalchemy.sql.expression.UpdateBase.prefix_with")来指定多个前缀。

        参数：

        -   **\*expr**[¶](#sqlalchemy.sql.expression.UpdateBase.prefix_with.params.*expr)
            – textual or [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")
            construct which will be rendered following the INSERT,
            UPDATE, or DELETE keyword.
        -   **\*\* kw**
            [¶](#sqlalchemy.sql.expression.UpdateBase.prefix_with.params.**kw)
            -
            接受单个关键字'dialect'。这是一个可选的字符串方言名称，它将限制将该前缀的呈现仅限于该方言。

    `返回 T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   在此语句中添加一个[RETURNING](glossary.html#term-returning)或等同的子句。

        例如。：

            stmt = table.update().\
                      where(table.c.data == 'value').\
                      values(status='X').\
                      returning(table.c.server_flag,
                                table.c.updated_timestamp)

            for server_flag, updated_timestamp in connection.execute(stmt):
                print(server_flag, updated_timestamp)

        给定的列表达式集合应该从作为INSERT，UPDATE或DELETE目标的表中派生。虽然[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象是典型的，但元素也可以是表达式：

            stmt = table.insert().returning(
                (table.c.first_name + " " + table.c.last_name).
                label('fullname'))

        编译后，将在语句中呈现RETURNING子句或数据库等效项。对于INSERT和UPDATE，这些值是新插入/更新的值。对于DELETE，这些值是那些被删除的行。

        执行时，要返回的列的值通过结果集可用，并可以使用[`ResultProxy.fetchone()`](connections.html#sqlalchemy.engine.ResultProxy.fetchone "sqlalchemy.engine.ResultProxy.fetchone")和类似的方法进行迭代。对于本身不支持返回值的DBAPI（即cx\_oracle），SQLAlchemy将在结果级接近此行为，以便提供合理的行为中立性。

        请注意，并非所有数据库/
        DBAPI都支持RETURNING。对于不支持的后端，编译和/或执行时会引发异常。对于那些支持它的人来说，后端的功能差异很大，包括对executemany()和其他返回多行的语句的限制。请阅读正在使用的数据库的文档说明，以确定RETURNING的可用性。

        也可以看看

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        -
        针对单个行INSERT或UPDATE的高效获取服务器端默认值和触发器的一种替代方法。

    `标量`{.descname} （ *\* multiparams*，*\*\* params* ） [T5\>](#sqlalchemy.sql.expression.UpdateBase.scalar "Permalink to this definition")
    :   *inherited from the* [`scalar()`](selectable.html#sqlalchemy.sql.expression.Executable.scalar "sqlalchemy.sql.expression.Executable.scalar")
        *method of* [`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")

        编译并执行此[`Executable`](selectable.html#sqlalchemy.sql.expression.Executable "sqlalchemy.sql.expression.Executable")，返回结果的标量表示。

    ` self_group  T0> （ T1> 针对=无 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`self_group()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.self_group "sqlalchemy.sql.expression.ClauseElement.self_group")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        对这个[`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")应用“分组”。

        子类重写此方法以返回“分组”结构，即括号。In particular it’s used
        by “binary” expressions to provide a grouping around themselves
        when placed into a larger expression, as well as by
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
        constructs when placed into the FROM clause of another
        [`select()`](selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select").
        （请注意，通常应使用[`Select.alias()`](selectable.html#sqlalchemy.sql.expression.Select.alias "sqlalchemy.sql.expression.Select.alias")方法创建子查询，因为许多平台需要命名嵌套的SELECT语句）。

        由于表达式组合在一起，所以[`self_group()`](#sqlalchemy.sql.expression.UpdateBase.self_group "sqlalchemy.sql.expression.UpdateBase.self_group")的应用程序是自动的
        - 最终用户代码不需要直接使用此方法。Note that SQLAlchemy’s
        clause constructs take operator precedence into account - so
        parenthesis might not be needed, for example, in an expression
        like `x OR (y AND z)` - AND takes precedence
        over OR.

        [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的base
        [`self_group()`](#sqlalchemy.sql.expression.UpdateBase.self_group "sqlalchemy.sql.expression.UpdateBase.self_group")方法仅返回self。

    `unique_params`{.descname} （ *\* optionaldict*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.UpdateBase.unique_params "Permalink to this definition")
    :   *inherited from the* [`unique_params()`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement.unique_params "sqlalchemy.sql.expression.ClauseElement.unique_params")
        *method of* [`ClauseElement`](sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")

        返回带有[`bindparam()`](sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")元素的副本。

        与`params()`功能相同，除了将unique =
        True添加到受影响的绑定参数以便可以使用多个语句。

     `with_hint`{.descname}(*text*, *selectable=None*, *dialect\_name='\*'*)[¶](#sqlalchemy.sql.expression.UpdateBase.with_hint "Permalink to this definition")
    :   为这个INSERT / UPDATE / DELETE语句添加一个表提示给单个表。

        注意

        [`UpdateBase.with_hint()`](#sqlalchemy.sql.expression.UpdateBase.with_hint "sqlalchemy.sql.expression.UpdateBase.with_hint")
        currently applies only to Microsoft SQL Server. 对于MySQL INSERT
        / UPDATE / DELETE提示，请使用[`UpdateBase.prefix_with()`](#sqlalchemy.sql.expression.UpdateBase.prefix_with "sqlalchemy.sql.expression.UpdateBase.prefix_with")。

        The text of the hint is rendered in the appropriate location for
        the database backend in use, relative to the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        that is the subject of this statement, or optionally to that of
        the given [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        passed as the `selectable` argument.

        The `dialect_name` option will limit the
        rendering of a particular hint to a particular backend.
        例如，添加仅对SQL Server有效的提示：

            mytable.insert().with_hint("WITH (PAGLOCK)", dialect_name="mssql")

        New in version 0.7.6.

        参数：

        -   **文本**
            [¶](#sqlalchemy.sql.expression.UpdateBase.with_hint.params.text)
            - 提示的文本。
        -   **selectable**[¶](#sqlalchemy.sql.expression.UpdateBase.with_hint.params.selectable)
            – optional [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
            that specifies an element of the FROM clause within an
            UPDATE or DELETE to be the subject of the hint - applies
            only to certain backends.
        -   **dialect\_name**[¶](#sqlalchemy.sql.expression.UpdateBase.with_hint.params.dialect_name)
            – defaults to `*`, if specified as the
            name of a particular dialect, will apply these hints only
            when that dialect is in use.

 *class*`sqlalchemy.sql.expression.`{.descclassname}`ValuesBase`{.descname}(*table*, *values*, *prefixes*)[¶](#sqlalchemy.sql.expression.ValuesBase "Permalink to this definition")
:   基础：[`sqlalchemy.sql.expression.UpdateBase`](#sqlalchemy.sql.expression.UpdateBase "sqlalchemy.sql.expression.UpdateBase")

    提供对[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")到INSERT和UPDATE结构的支持。plainplainplainplainplain

    ` return_defaults  T0> （ T1>  * COLS  T2> ） T3> ¶ T4>`{.descname}
    :   利用[RETURNING](glossary.html#term-returning)子句获取服务器端表达式和默认值。

        例如。：

            stmt = table.insert().values(data='newdata').return_defaults()

            result = connection.execute(stmt)

            server_created_at = result.returned_defaults['created_at']

        当用于支持RETURNING的后端时，如果不同时使用[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")，则由SQL表达式或server-side-default生成的所有列值将被添加到任何现有的RETURNING子句中。然后，使用[`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")存取器作为字典，结果可以在结果上使用列值，该值指的是键入[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象及其`.key`

        这种方法与[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")不同之处在于：

        1.  [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")仅用于与一行匹配的INSERT或UPDATE语句。尽管一般意义上的RETURNING构造支持多行UPDATE或DELETE语句的多行，或者对于返回多行的INSERT的特殊情况（例如，来自SELECT，多值VALUES子句的INSERT），[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")仅用于“ORM样式”单行INSERT
            / UPDATE语句。当使用[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")时，语句返回的行也会隐式消耗。By
            contrast, [`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")
            leaves the RETURNING result-set intact with a collection of
            any number of rows.
        2.  它与现有逻辑兼容，以获取自动生成的主键值，也称为“隐式返回”。支持RETURNING的后端将自动使用RETURNING来获取新生成的主键值；而[`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")方法绕过了这种行为，[`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")保持不变。
        3.  它可以被称为反对任何后端。不支持RETURNING的后端将跳过功能的使用，而不是引发异常。[`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")的返回值将为`None`

        [`ValuesBase.return_defaults()`](#sqlalchemy.sql.expression.ValuesBase.return_defaults "sqlalchemy.sql.expression.ValuesBase.return_defaults")
        is used by the ORM to provide an efficient implementation for
        the `eager_defaults` feature of
        [`mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper").

        参数：

        **cols**[¶](#sqlalchemy.sql.expression.ValuesBase.return_defaults.params.cols)
        – optional list of column key names or [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
        objects.
        如果省略，则服务器上评估的所有列表达式都将添加到返回列表中。

        版本0.9.0中的新功能

        也可以看看

        [`UpdateBase.returning()`](#sqlalchemy.sql.expression.UpdateBase.returning "sqlalchemy.sql.expression.UpdateBase.returning")

        [`ResultProxy.returned_defaults`](connections.html#sqlalchemy.engine.ResultProxy.returned_defaults "sqlalchemy.engine.ResultProxy.returned_defaults")

    `值`{.descname} （ *\* args*，*\*\* kwargs* ） [T5\>](#sqlalchemy.sql.expression.ValuesBase.values "Permalink to this definition")
    :   为INSERT语句指定一个固定的VALUES子句，或者为UPDATE指定一个SET子句。

        Note that the [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")
        and [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")
        constructs support per-execution time formatting of the VALUES
        and/or SET clauses, based on the arguments passed to
        [`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute").
        但是，可以使用[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")方法将特定的一组参数“修复”到语句中。

        多次调用[`ValuesBase.values()`](#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")将产生一个新的结构，每个结构都修改参数列表以包含发送的新参数。在单个参数字典的典型情况下，新传递的键将替换以前构造中的相同键。在基于列表的“多值”结构的情况下，每个新的值列表都被扩展到现有的值列表中。

        参数：

        -   **\*\* kwargs**
            [¶](#sqlalchemy.sql.expression.ValuesBase.values.params.**kwargs)
            -

            键值对表示映射到要呈现到VALUES或SET子句中的值的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的字符串键：

                users.insert().values(name="some name")

                users.update().where(users.c.id==5).values(name="some name")

        -   **\* args**
            [¶](#sqlalchemy.sql.expression.ValuesBase.values.params.*args)
            -

            作为传递键/值参数的替代方法，字典，元组或字典或元组列表可以作为单个位置参数传递，以形成语句的VALUES或SET子句。接受的表单根据是[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")还是[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构而有所不同。

            对于[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构，可以传递单个字典，其工作方式与kwargs表单相同：

                users.insert().values({"name": "some name"})

                users.update().values({"name": "some new name"})

            对于任何一种形式，但对于[`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")构造更典型，也接受包含表中每列的条目的元组：

                users.insert().values((5, "some name"))

            [`Insert`](#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")结构还支持传递字典或全表元组列表，这些元组在服务器上将呈现不太常见的“多值”SQL语法
            -
            后端支持此语法，如SQLite，Postgresql，MySQL，但不一定是其他的：

                users.insert().values([
                                    {"name": "some name"},
                                    {"name": "some other name"},
                                    {"name": "yet another name"},
                                ])

            上面的表单将呈现多个VALUES语句，类似于：

                INSERT INTO users (name) VALUES
                                (:name_1),
                                (:name_2),
                                (:name_3)

            It is essential to note that **passing multiple values is
            NOT the same as using traditional executemany() form**.
            上面的语法是不常用的**特殊**语法。要针对多行发出INSERT语句，常规方法是将多个值列表传递给[`Connection.execute()`](connections.html#sqlalchemy.engine.Connection.execute "sqlalchemy.engine.Connection.execute")方法，该方法由所有数据库后端支持，并且通常对于非常高效的大量的参数。

            > 也可以看看
            >
            > [Executing Multiple
            > Statements](tutorial.html#execute-multiple) -
            > 介绍用于INSERT和其他语句的多参数集调用的传统Core方法。
            >
            > 版本1.0.0中已更改：使用多个VALUES子句（即使是长度为1的列表）的INSERT意味着[`Insert.inline`](#sqlalchemy.sql.expression.Insert.params.inline "sqlalchemy.sql.expression.Insert")标志设置为True，表明该语句不会尝试获取“最后插入的主键”或其他默认值。该语句处理任意数量的行，因此[`ResultProxy.inserted_primary_key`](connections.html#sqlalchemy.engine.ResultProxy.inserted_primary_key "sqlalchemy.engine.ResultProxy.inserted_primary_key")访问器不适用。
            >
            > 在1.0.0版本中已更改：多值插入现在支持具有Python侧缺省值和可调参数的列，方式与“executemany”调用方式相同；可调用的是每行调用的。对于其他细节，当使用多值插入时，请参阅[Python-side
            > defaults invoked for each row invidually when using a
            > multivalued insert](changelog_migration_10.html#bug-3288)

            [`Update`](#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构支持一个特殊的形式，它是一个2元组的列表，当提供的时候必须和[`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")参数一起传递。这种形式导致UPDATE语句使用[`Update.values()`](#sqlalchemy.sql.expression.Update.values "sqlalchemy.sql.expression.Update.values")给出的参数顺序来呈现SET子句，而不是[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中给出的列的顺序。

            > 版本1.0.10中的新增功能： -
            > 通过[`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志增加了对参数排序的UPDATE语句的支持。
            >
            > 也可以看看
            >
            > [Parameter-Ordered
            > Updates](tutorial.html#updates-order-parameters) -
            > [`preserve_parameter_order`](#sqlalchemy.sql.expression.update.params.preserve_parameter_order "sqlalchemy.sql.expression.update")标志的完整示例

        也可以看看

        [Inserts, Updates and
        Deletes](tutorial.html#inserts-and-updates) - SQL表达式语言教程

        [`insert()`](#sqlalchemy.sql.expression.insert "sqlalchemy.sql.expression.insert")
        - 产生一个`INSERT`语句

        [`update()`](#sqlalchemy.sql.expression.update "sqlalchemy.sql.expression.update")
        - 产生一个`UPDATE`语句


