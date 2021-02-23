---
title: SQL表达式
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/faq/sqlexpressions/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - faq
tags:
  - 
---
SQL表达式[¶](#sql-expressions "Permalink to this headline")
===========================================================

-   [如何将SQL表达式呈现为字符串，可能绑定的参数内联？](#how-do-i-render-sql-expressions-as-strings-possibly-with-bound-parameters-inlined)
-   [Why does `.col.in_([])` Produce
    `col != col`? Why not `1=0`?](#why-does-col-in-produce-col-col-why-not-1-0)

如何将SQL表达式呈现为字符串，可能内联了绑定参数？[¶](#how-do-i-render-sql-expressions-as-strings-possibly-with-bound-parameters-inlined "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

在绝大多数情况下，SQLAlchemy语句或Query的“字符串化”非常简单：

    print(str(statement))

这适用于ORM [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")以及任何[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")或其他语句。此外，要将语句编译为特定的方言或引擎，如果语句本身尚未绑定到某个语句，您可以将它传递给[`ClauseElement.compile()`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")：

    print(statement.compile(someengine))

或者没有[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")：

    from sqlalchemy.dialects import postgresql
    print(statement.compile(dialect=postgresql.dialect()))

当给定ORM [`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象时，为了获得[`ClauseElement.compile()`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement.compile "sqlalchemy.sql.expression.ClauseElement.compile")方法，我们只需要首先访问[`statement`](orm_query.html#sqlalchemy.orm.query.Query.statement "sqlalchemy.orm.query.Query.statement")访问器：

    statement = query.statement
    print(statement.compile(someengine))

上述表单将在传递给Python
[DBAPI](glossary.html#term-dbapi)时呈现SQL语句，其中包括绑定参数不以内联方式呈现。SQLAlchemy通常不绑定绑定参数，因为这是由Python
DBAPI适当地处理的，更不用说绕过绑定参数可能是现代Web应用程序中使用最广泛的安全漏洞。SQLAlchemy在某些情况下（例如发出DDL）的能力有限。为了访问这个功能，可以使用传递给`compile_kwargs`的`literal_binds`标志：

    from sqlalchemy.sql import table, column, select

    t = table('t', column('x'))

    s = select([t]).where(t.c.x == 5)

    print(s.compile(compile_kwargs={"literal_binds": True}))

上面的方法有一点要注意，它只支持基本类型，例如整数和字符串，而且如果直接使用没有预设值的[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")，它将不会能够将其串联起来。

要支持对不支持类型的内联文字渲染，请为包含[`TypeDecorator.process_literal_param()`](core_custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")方法的目标类型实现一个[`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")：

    from sqlalchemy import TypeDecorator, Integer


    class MyFancyType(TypeDecorator):
        impl = Integer

        def process_literal_param(self, value, dialect):
            return "my_fancy_formatting(%s)" % value

    from sqlalchemy import Table, Column, MetaData

    tab = Table('mytable', MetaData(), Column('x', MyFancyType()))

    print(
        tab.select().where(tab.c.x > 5).compile(
            compile_kwargs={"literal_binds": True})
    )

产出如下产出：

    SELECT mytable.x
    FROM mytable
    WHERE mytable.x > my_fancy_formatting(5)

为什么`.col.in_([])`产生`col ！= col` ？为什么不`1=0`？[¶](#why-does-col-in-produce-col-col-why-not-1-0 "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

关于这个问题的一点介绍。SQL中的IN运算符给出了要与列进行比较的元素列表，但通常不会接受空列表，即可以这样说：

    column IN (1, 2, 3)

这是无效的说：

    column IN ()

SQLAlchemy的`Operators.in_()`运算符在给出一个空列表时产生这个表达式：

    column != column

从版本0.6开始，它也会产生一个警告，指出将会呈现效率较低的比较操作。这个表达式是唯一一个既是数据库不可知的，又能产生正确结果的表达式。

例如，“通过比较1 = 0或1！=
1来评估为假”的幼稚方法不能正确处理空值。表达式如下：

    NOT column != column

当“列”为空时不会返回一行，但是不考虑列的表达式：

    NOT 1=0

将。

更接近该商标的是以下CASE表达式：

    CASE WHEN column IS NOT NULL THEN 1=0 ELSE NULL END

我们不使用这个表达式，因为它的冗长，而且在WHERE子句中它也不被Oracle接受
- 取决于你如何说出它，你会得到“ORA-00905：missing keyword”或者“ORA-00920
：无效的关系运算符“。它的效率还不如完全没有子句的情况下渲染SQL（或者根本不发布SQL，如果语句只是简单的搜索）。

因此，最好的方法是在零长度的参数列表中避免使用IN。相反，如果不应返回行，请不要首先发出查询。警告最好使用Python警告过滤器提升为完全错误状态（请参阅[http://docs.python.org/library/warnings.html](http://docs.python.org/library/warnings.html)）。
