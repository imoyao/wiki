---
title: migration_09
date: 2021-02-20 22:41:31
permalink: /sqlalchemy/cac9ed/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - changelog
tags:
---
SQLAlchemy 0.9 有哪些新特性？[¶](#what-s-new-in-sqlalchemy-0-9 "Permalink to this headline")
===========================================================================================

关于本文档

本文档介绍了 2013 年 5 月发布的 SQLAlchemy 版本 0.8 和 2013 年 12 月 30 日发布的 SQLAlchemy
0.9 版本之间的更改。

文件最后更新日期：2015 年 6 月 10 日

引言[¶ T0\>](#introduction "Permalink to this headline")
--------------------------------------------------------

本指南介绍了 SQLAlchemy
0.9 版中的新增功能，并介绍了影响用户将其应用程序从 0.8 系列 SQLAlchemy 迁移到 0.9 的更改。

请仔细查看[Behavioral Changes -
ORM](#behavioral-changes-orm-09)和[Behavioral Changes -
Core](#behavioral-changes-core-09)以了解潜在的向后不兼容变更。

平台支持[¶](#platform-support "Permalink to this headline")
-----------------------------------------------------------

### 针对 Python 2.6 及更高版本，Python 3 无 2to3 [¶](#targeting-python-2-6-and-up-now-python-3-without-2to3 "Permalink to this headline")

0.9 版本的第一个成就是消除了对 Python
3 兼容性的 2to3 工具的依赖。为了更简单明了，现在最低版本的 Python 版本是 2.6，它具有与 Python
3 的广泛兼容性。现在所有的 SQLAlchemy 模块和单元测试都可以用 2.6 前向版的任何 Python 解释器解释，包括 3.1 和 3.2 解释器。

[＃2671 T0\>](http://www.sqlalchemy.org/trac/ticket/2671)

### Python 3 支持的 C 扩展[¶](#c-extensions-supported-on-python-3 "Permalink to this headline")

C 扩展已经移植到支持 Python 3，现在可以在 Python 2 和 Python 3 环境中构建。

[＃2161 T0\>](http://www.sqlalchemy.org/trac/ticket/2161)

行为改变 - ORM [¶](#behavioral-changes-orm "Permalink to this headline")
------------------------------------------------------------------------

### 当以每个属性为基础查询时，复合属性现在以其对象形式返回[¶](#composite-attributes-are-now-returned-as-their-object-form-when-queried-on-a-per-attribute-basis "Permalink to this headline")

将[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")与复合属性结合使用现在返回由该复合物维护的对象类型，而不是分解为单独的列。在[Composite
Column Types](orm_composites.html#mapper-composite)中使用映射设置：

    >>> session.query(Vertex.start, Vertex.end).\
    ...     filter(Vertex.start == Point(3, 4)).all()
    [(Point(x=3, y=4), Point(x=5, y=6))]

此更改与代码中的后向不兼容，该代码需要将单个属性扩展为单个列。要获得该行为，请使用`.clauses`访问器：

    >>> session.query(Vertex.start.clauses, Vertex.end.clauses).\
    ...     filter(Vertex.start == Point(3, 4)).all()
    [(3, 4, 5, 6)]

也可以看看

[Column Bundles for ORM queries](#change-2824)

[＃2824 T0\>](http://www.sqlalchemy.org/trac/ticket/2824)

### [`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")不再将该子句应用于相应的实体[¶](#query-select-from-no-longer-applies-the-clause-to-corresponding-entities "Permalink to this headline")

在最近的版本中，[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")方法作为控制[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象“从中选择”的第一件事的手段已经普及，通常用于控制JOIN将如何呈现。

根据通常的`User`映​​射考虑以下示例：

    select_stmt = select([User]).where(User.id == 7).alias()

    q = session.query(User).\
               join(select_stmt, User.id == select_stmt.c.id).\
               filter(User.name == 'ed')

上面的语句可预测地呈现如下的 SQL：

    SELECT "user".id AS user_id, "user".name AS user_name
    FROM "user" JOIN (SELECT "user".id AS id, "user".name AS name
    FROM "user"
    WHERE "user".id = :id_1) AS anon_1 ON "user".id = anon_1.id
    WHERE "user".name = :name_1

如果我们想要颠倒 JOIN 的左侧和右侧元素的顺序，文档将导致我们相信我们可以使用[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")来执行此操作：

    q = session.query(User).\plain
            select_from(select_stmt).\
            join(User, User.id == select_stmt.c.id).\
            filter(User.name == 'ed')

However, in version 0.8 and earlier, the above use of
[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")
would apply the `select_stmt` to **replace** the
`User` entity, as it selects from the
`user` table which is compatible with
`User`:

    -- SQLAlchemy 0.8 and earlier...plain
    SELECT anon_1.id AS anon_1_id, anon_1.name AS anon_1_name
    FROM (SELECT "user".id AS id, "user".name AS name
    FROM "user"
    WHERE "user".id = :id_1) AS anon_1 JOIN "user" ON anon_1.id = anon_1.id
    WHERE anon_1.name = :name_1

The above statement is a mess, the ON clause refers
`anon_1.id = anon_1.id`, our WHERE clause has been
replaced with `anon_1` as well.

这种行为是非常有意的，但是与[`Query.select_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")流行的用例有不同的用例。上述行为现在可以通过称为[`Query.select_entity_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_entity_from "sqlalchemy.orm.query.Query.select_entity_from")的新方法使用。这是一种较少使用的行为，在现代SQLAlchemy中大致等价于从定制的[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")结构中进行选择：

    select_stmt = select([User]).where(User.id == 7)plain
    user_from_stmt = aliased(User, select_stmt.alias())

    q = session.query(user_from_stmt).filter(user_from_stmt.name == 'ed')

因此，对于 SQLAlchemy 0.9，我们从`select_stmt`中选择的查询产生了我们期望的 SQL：

    -- SQLAlchemy 0.9plain
    SELECT "user".id AS user_id, "user".name AS user_name
    FROM (SELECT "user".id AS id, "user".name AS name
    FROM "user"
    WHERE "user".id = :id_1) AS anon_1 JOIN "user" ON "user".id = id
    WHERE "user".name = :name_1

The [`Query.select_entity_from()`](orm_query.html#sqlalchemy.orm.query.Query.select_entity_from "sqlalchemy.orm.query.Query.select_entity_from")
method will be available in SQLAlchemy **0.8.2**, so applications which
rely on the old behavior can transition to this method first, ensure all
tests continue to function, then upgrade to 0.9 without issue.

[＃2736 T0\>](http://www.sqlalchemy.org/trac/ticket/2736)

### `viewonly=True` on `relationship()` prevents history from taking effect[¶](#viewonly-true-on-relationship-prevents-history-from-taking-effect "Permalink to this headline")

[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上的`viewonly`标志用于防止更改目标属性在刷新过程中产生任何效果。这是通过消除刷新期间的属性来实现的。但是，直到现在，对该属性的更改仍然会将父对象注册为“脏”并触发潜在的刷新。现在的变化是，`viewonly`标志现在也禁止为目标属性设置历史记录。像backrefs和用户定义事件的属性事件仍然可以继续正常运行。

更改说明如下：

    from sqlalchemy import Column, Integer, ForeignKey, create_engine
    from sqlalchemy.orm import backref, relationship, Session
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import inspect

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)

    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)
        a_id = Column(Integer, ForeignKey('a.id'))
        a = relationship("A", backref=backref("bs", viewonly=True))

    e = create_engine("sqlite://")
    Base.metadata.create_all(e)

    a = A()
    b = B()

    sess = Session(e)
    sess.add_all([a, b])
    sess.commit()

    b.a = a

    assert b in sess.dirty

    # before 0.9.0
    # assert a in sess.dirty
    # assert inspect(a).attrs.bs.history.has_changes()

    # after 0.9.0
    assert a not in sess.dirty
    assert not inspect(a).attrs.bs.history.has_changes()

[＃2833 T0\>](http://www.sqlalchemy.org/trac/ticket/2833)

### 关联代理 SQL 表达式改进和修复[¶](#association-proxy-sql-expression-improvements-and-fixes "Permalink to this headline")

由引用标量关系上的标量值的关联代理实现的`==`和`!=`运算符现在生成更完整的 SQL 表达式，旨在考虑当比较是针对`None`时，“关联”行是否存在。

考虑这个映射：

    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)

        b_id = Column(Integer, ForeignKey('b.id'), primary_key=True)
        b = relationship("B")
        b_value = association_proxy("b", "value")

    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)
        value = Column(String)

通过 0.8，查询如下：

    s.query(A).filter(A.b_value == None).all()plain

会产生：

    SELECT a.id AS a_id, a.b_id AS a_b_id
    FROM a
    WHERE EXISTS (SELECT 1
    FROM b
    WHERE b.id = a.b_id AND b.value IS NULL)

在 0.9 中，它现在产生：

    SELECT a.id AS a_id, a.b_id AS a_b_idplain
    FROM a
    WHERE (EXISTS (SELECT 1
    FROM b
    WHERE b.id = a.b_id AND b.value IS NULL)) OR a.b_id IS NULL

不同之处在于，它不仅检查`b.value`，还检查`a`是否根本不指向`b`行。这将返回与先前版本不同的结果，对于使用此类比较的系统，其中某些父行没有关联行。

更关键的是，为`A.b_value ！= 无`发出正确的表达式。在 0.8 中，对于没有`b`的`A`行，这将返回`True`：

    SELECT a.id AS a_id, a.b_id AS a_b_id
    FROM a
    WHERE NOT (EXISTS (SELECT 1
    FROM b
    WHERE b.id = a.b_id AND b.value IS NULL))

现在在 0.9 中，检查已被重新编译，以确保 A.b\_id 行存在，除了`B.value`为非 NULL：

    SELECT a.id AS a_id, a.b_id AS a_b_idplain
    FROM a
    WHERE EXISTS (SELECT 1
    FROM b
    WHERE b.id = a.b_id AND b.value IS NOT NULL)

此外，还增强了`has()`运算符，以便您可以在不使用标准的情况下将其称为标量列值，并且它会生成检查存在或不存在的关联行的条件：

    s.query(A).filter(A.b_value.has()).all()plainplain

输出：

    SELECT a.id AS a_id, a.b_id AS a_b_id
    FROM a
    WHERE EXISTS (SELECT 1
    FROM b
    WHERE b.id = a.b_id)

这相当于`A.b.has()`，但允许直接对`b_value`进行查询。

[＃2751 T0\>](http://www.sqlalchemy.org/trac/ticket/2751)

### 关联代理丢失标量返回无[¶](#association-proxy-missing-scalar-returns-none "Permalink to this headline")

如果代理对象不存在，则从标量属性到标量的关联代理现在将返回`None`。这与在 SQLAlchemy 中缺少多对一返回 None 的事实一致，所以应该使用代理值。例如。：

    from sqlalchemy import *plain
    from sqlalchemy.orm import *
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.ext.associationproxy import association_proxy

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        b = relationship("B", uselist=False)

        bname = association_proxy("b", "name")

    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)
        a_id = Column(Integer, ForeignKey('a.id'))
        name = Column(String)

    a1 = A()

    # this is how m2o's always have worked
    assert a1.b is None

    # but prior to 0.9, this would raise AttributeError,
    # now returns None just like the proxied value.
    assert a1.bname is None

[＃2810 T0\>](http://www.sqlalchemy.org/trac/ticket/2810)

### 如果值不存在，attributes.get\_history()将默认从数据库中查询[¶](#attributes-get-history-will-query-from-the-db-by-default-if-value-not-present "Permalink to this headline")

A bugfix regarding [`attributes.get_history()`](orm_session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")
allows a column-based attribute to query out to the database for an
unloaded value, assuming the `passive` flag is left
at its default of `PASSIVE_OFF`.
以前，这个标志不会被兑现。此外，添加了一个新方法[`AttributeState.load_history()`](orm_internals.html#sqlalchemy.orm.state.AttributeState.load_history "sqlalchemy.orm.state.AttributeState.load_history")以补充[`AttributeState.history`](orm_internals.html#sqlalchemy.orm.state.AttributeState.history "sqlalchemy.orm.state.AttributeState.history")属性，该属性将为未加载属性发出加载器可调用对象。

这是一个小小的变化，演示如下：

    from sqlalchemy import Column, Integer, String, create_engine, inspectplain
    from sqlalchemy.orm import Session, attributes
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        data = Column(String)

    e = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(e)

    sess = Session(e)

    a1 = A(data='a1')
    sess.add(a1)
    sess.commit()  # a1 is now expired

    # history doesn't emit loader callables
    assert inspect(a1).attrs.data.history == (None, None, None)

    # in 0.8, this would fail to load the unloaded state.
    assert attributes.get_history(a1, 'data') == ((), ['a1',], ())

    # load_history() is now equiavlent to get_history() with
    # passive=PASSIVE_OFF ^ INIT_OK
    assert inspect(a1).attrs.data.load_history() == ((), ['a1',], ())

[＃2787 T0\>](http://www.sqlalchemy.org/trac/ticket/2787)

行为改变 - 核心[¶](#behavioral-changes-core "Permalink to this headline")
-------------------------------------------------------------------------

### 类型对象不再接受被忽略的关键字参数[¶](#type-objects-no-longer-accept-ignored-keyword-arguments "Permalink to this headline")

通过 0.8 系列，大多数类型的对象接受了被默默忽略的任意关键字参数：

    from sqlalchemy import Date, Integer

    # storage_format argument here has no effect on any backend;
    # it needs to be on the SQLite-specific type
    d = Date(storage_format="%(day)02d.%(month)02d.%(year)04d")

    # display_width argument here has no effect on any backend;
    # it needs to be on the MySQL-specific type
    i = Integer(display_width=5)

这是一个非常古老的 bug，为 0.8 系列添加了弃用警告，但因为没有人用“-W”标志运行 Python，所以大部分都没有看到：

    $ python -W always::DeprecationWarning ~/dev/sqlalchemy/test.pyplain
    /Users/classic/dev/sqlalchemy/test.py:5: SADeprecationWarning: Passing arguments to
    type object constructor <class 'sqlalchemy.types.Date'> is deprecated
      d = Date(storage_format="%(day)02d.%(month)02d.%(year)04d")
    /Users/classic/dev/sqlalchemy/test.py:9: SADeprecationWarning: Passing arguments to
    type object constructor <class 'sqlalchemy.types.Integer'> is deprecated
      i = Integer(display_width=5)

从 0.9 系列开始，“catch all”构造函数从[`TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")中移除，并且这些无意义的参数不再被接受。

使用特定于方言的参数（如`storage_format`和`display_width`）的正确方法是使用适当的方言特定类型：

    from sqlalchemy.dialects.sqlite import DATEplainplain
    from sqlalchemy.dialects.mysql import INTEGER

    d = DATE(storage_format="%(day)02d.%(month)02d.%(year)04d")

    i = INTEGER(display_width=5)

那么我们想要方言不可知类型的情况呢？我们使用[`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")方法：

    from sqlalchemy import Date, Integer
    from sqlalchemy.dialects.sqlite import DATE
    from sqlalchemy.dialects.mysql import INTEGER

    d = Date().with_variant(
            DATE(storage_format="%(day)02d.%(month)02d.%(year)04d"),
            "sqlite"
        )

    i = Integer().with_variant(
            INTEGER(display_width=5),
            "mysql"
        )

[`TypeEngine.with_variant()`](core_type_api.html#sqlalchemy.types.TypeEngine.with_variant "sqlalchemy.types.TypeEngine.with_variant")
isn’t new, it was added in SQLAlchemy 0.7.2.
因此，在 0.8 系列上运行的代码可以更正为在升级到 0.9 之前使用此方法并进行测试。

### `None`不能再用作“部分 AND”构造函数[¶](#none-can-no-longer-be-used-as-a-partial-and-constructor "Permalink to this headline")

`None` can no longer be used as the “backstop” to
form an AND condition piecemeal.
即使某些 SQLAlchemy 内部函数使用了它，该模式也不是文档模式：

    condition = Noneplainplain

    for cond in conditions:
        condition = condition & cond

    if condition is not None:
        stmt = stmt.where(condition)

当`conditions`非空时，上述序列将在 0.9 产生`SELECT .. WHERE ＆lt； condition＆gt； AND NULL`。`None`不再被隐式忽略，而是与`None`在其他上下文中解释时一致。

对于 0.8 和 0.9，正确的代码应为：

    from sqlalchemy.sql import and_plain

    if conditions:
        stmt = stmt.where(and_(*conditions))

另一个适用于所有后端的变种 0.9，但在 0.8 上只适用于支持布尔常量的后端：

    from sqlalchemy.sql import trueplain

    condition = true()

    for cond in conditions:
        condition = cond & condition

    stmt = stmt.where(condition)

在 0.8 上，这将产生一个 SELECT 语句，该语句在 WHERE 子句中总是有`AND true`，而后者不会被接受支持布尔常量（MySQL，MSSQL）。在 0.9 上，`true`常量将被放在`and_()`连接符中。

也可以看看

[Improved rendering of Boolean constants, NULL constants,
conjunctions](#migration-2804)的渲染

### `create_engine()`的“密码”部分不再将`+`标记视为编码空间[¶](#the-password-portion-of-a-create-engine-no-longer-considers-the-sign-as-an-encoded-space "Permalink to this headline")

无论出于何种原因，Python 函数`unquote_plus()`都应用于 URL 的“password”字段，这是[RFC
1738](http://www.ietf.org/rfc/rfc1738.txt)中描述的编码规则的错误应用。它作为加号逃脱了空间。现在 URL 的字符串只对“：​​”，“@”或“/”进行编码，并且现在也应用于`username`和`password`字段以前它只适用于密码）。在解析时，编码字符被转换，但加号和空格按原样传递：

    # password: "pass word + other:words"plain
    dbtype://user:pass word + other%3Awords@host/dbname

    # password: "apples/oranges"
    dbtype://username:apples%2Foranges@hostspec/database

    # password: "apples@oranges@@"
    dbtype://username:apples%40oranges%40%40@hostspec/database

    # password: '', username is "username@"
    dbtype://username%40:@hostspec/database

[＃2873 T0\>](http://www.sqlalchemy.org/trac/ticket/2873)

### COLLATE的优先规则已被更改[¶](#the-precedence-rules-for-collate-have-been-changed "Permalink to this headline")

以前，像下面这样的表达式：

    print((column('x') == 'somevalue').collate("en_EN"))plain

会产生这样的表达式：

    -- 0.8 behavior
    (x = :x_1) COLLATE en_EN

上述内容被 MSSQL 误解，通常不是针对任何数据库建议的语法。该表达式现在将生成大多数数据库文档所说明的语法：

    -- 0.9 behaviorplain
    x = :x_1 COLLATE en_EN

如果将[`collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")运算符应用于右列，则可能出现向后不兼容的更改，如下所示：

    print(column('x') == literal('somevalue').collate("en_EN"))

在 0.8 中，这产生：

    x = :param_1 COLLATE en_EN

然而在 0.9 中，现在会产生更准确但可能不是你想要的形式：

    x = (:param_1 COLLATE en_EN)

The [`ColumnOperators.collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
operator now works more appropriately within an `ORDER BY` expression as well, as a specific precedence has been given to
the `ASC` and `DESC` operators
which will again ensure no parentheses are generated:

    >>> # 0.8plain
    >>> print(column('x').collate('en_EN').desc())
    (x COLLATE en_EN) DESC

    >>> # 0.9
    >>> print(column('x').collate('en_EN').desc())
    x COLLATE en_EN DESC

[＃2879 T0\>](http://www.sqlalchemy.org/trac/ticket/2879)

### Postgresql CREATE TYPE AS ENUM现在将引用应用于值[¶](#postgresql-create-type-x-as-enum-now-applies-quoting-to-values "Permalink to this headline")

现在，[`postgresql.ENUM`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.ENUM "sqlalchemy.dialects.postgresql.ENUM")类型将对枚举值中的单引号进行转义：

    >>> from sqlalchemy.dialects import postgresql
    >>> type = postgresql.ENUM('one', 'two', "three's", name="myenum")
    >>> from sqlalchemy.dialects.postgresql import base
    >>> print(base.CreateEnumType(type).compile(dialect=postgresql.dialect()))
    CREATE TYPE myenum AS ENUM ('one','two','three''s')

现有的解决方法已经逃脱了单引号，需要修改，否则他们现在会双重逃脱。

[＃2878 T0\>](http://www.sqlalchemy.org/trac/ticket/2878)

新功能[¶](#new-features "Permalink to this headline")
-----------------------------------------------------

### 事件清除 API [¶](#event-removal-api "Permalink to this headline")

现在可以使用新的[`event.remove()`](core_event.html#sqlalchemy.event.remove "sqlalchemy.event.remove")函数删除使用[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")或[`event.listens_for()`](core_event.html#sqlalchemy.event.listens_for "sqlalchemy.event.listens_for")建立的事件。发送到[`event.remove()`](core_event.html#sqlalchemy.event.remove "sqlalchemy.event.remove")的`target`，`identifier`和`fn`参数需要与发送的参数完全匹配聆听，并将该事件从所有已建立的地点删除：

    @event.listens_for(MyClass, "before_insert", propagate=True)plain
    def my_before_insert(mapper, connection, target):
        """listen for before_insert"""
        # ...

    event.remove(MyClass, "before_insert", my_before_insert)

在上面的例子中，设置了`propagate=True`标志。这意味着`my_before_insert()`被建立为`MyClass`以及`MyClass`的所有子类的侦听器。The system tracks everywhere that the
`my_before_insert()` listener function had been
placed as a result of this call and removes it as a result of calling
[`event.remove()`](core_event.html#sqlalchemy.event.remove "sqlalchemy.event.remove").

删除系统使用注册表将传递给[`event.listen()`](core_event.html#sqlalchemy.event.listen "sqlalchemy.event.listen")的参数与事件侦听器的集合关联，事件侦听器在很多情况下都是原始用户提供的函数的封装版本。此注册表大量使用弱引用，以便允许所有包含的内容（如侦听器目标）在超出范围时进行垃圾回收。

[＃2268 T0\>](http://www.sqlalchemy.org/trac/ticket/2268)

### 新的查询选项 API； `load_only()`选项[¶](#new-query-options-api-load-only-option "Permalink to this headline")

The system of loader options such as [`orm.joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload"),
[`orm.subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload"),
[`orm.lazyload()`](orm_loading_relationships.html#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload"),
[`orm.defer()`](orm_loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer"),
etc. 全部基于称为[`Load`](orm_query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")的新系统。[`Load`](orm_query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")提供了一种“方法链接”（a.k.a.[generative](glossary.html#term-generative)）加载器选项的方法，以便不使用点或多个属性名称将长路径连接在一起，而是为每个路径指定一个明确的加载器样式。

虽然新方法略为冗长，但理解起来更简单一点，就是哪些选项适用于哪些路径没有含糊不清之处；它简化了选项的方法签名并提供了更大的灵活性，特别是对于基于列的选项。旧系统也会无限期地保持功能，所有样式都可以混合使用。

**旧方式**

要在多元素路径中的每个链接上设置特定的加载样式，必须使用`_all()`选项：

    query(User).options(joinedload_all("orders.items.keywords"))plain

**新途径**

Loader 选项现在是可链接的，所以同样的`joinedload(x)`方法同样适用于每个链接，无需在[`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")和[`joinedload_all()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload_all "sqlalchemy.orm.joinedload_all")

    query(User).options(joinedload("orders").joinedload("items").joinedload("keywords"))

**旧方式**

在基于子类的路径上设置选项要求将路径中的所有链接拼写为类绑定属性，因为需要调用[`PropComparator.of_type()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")方法：

    session.query(Company).\plain
        options(
            subqueryload_all(
                Company.employees.of_type(Engineer),
                Engineer.machines
            )
        )

**新途径**

只有路径中实际需要[`PropComparator.of_type()`](orm_internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")的元素需要设置为类绑定属性，之后才能恢复基于字符串的名称：

    session.query(Company).\plain
        options(
            subqueryload(Company.employees.of_type(Engineer)).
            subqueryload("machines")
            )
        )

**旧方式**

在长路径中的最后一个链接上设置加载器选项使用的语法看起来很像它应该为路径中的所有链接设置选项，导致混淆：

    query(User).options(subqueryload("orders.items.keywords"))plain

**新途径**

现在可以使用[`defaultload()`](orm_loading_relationships.html#sqlalchemy.orm.defaultload "sqlalchemy.orm.defaultload")来为现有加载程序样式应该保持不变的路径中的条目拼写出路径。更详细，但意图更清晰：

    query(User).options(defaultload("orders").defaultload("items").subqueryload("keywords"))plainplain

虚线样式仍然可以利用，特别是在跳过多个路径元素的情况下：

    query(User).options(defaultload("orders.items").subqueryload("keywords"))plain

**旧方式**

需要使用每个列的完整路径拼写路径上的[`defer()`](orm_loading_columns.html#sqlalchemy.orm.defer "sqlalchemy.orm.defer")选项：

    query(User).options(defer("orders.description"), defer("orders.isopen"))

**新途径**

到达目标路径的单个[`Load`](orm_query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")对象可以[`Load.defer()`](orm_query.html#sqlalchemy.orm.strategy_options.Load.defer "sqlalchemy.orm.strategy_options.Load.defer")重复调用它：

    query(User).options(defaultload("orders").defer("description").defer("isopen"))

#### 加载类[¶](#the-load-class "Permalink to this headline")

可以直接使用[`Load`](orm_query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")类来提供“绑定”目标，特别是当存在多个父实体时：

    from sqlalchemy.orm import Load

    query(User, Address).options(Load(Address).joinedload("entries"))

#### 仅加载[¶](#load-only "Permalink to this headline")

一个新的选项[`load_only()`](orm_loading_columns.html#sqlalchemy.orm.load_only "sqlalchemy.orm.load_only")实现了“推迟一切，但是”的加载方式，只加载给定的列并推迟其余部分：

    from sqlalchemy.orm import load_only

    query(User).options(load_only("name", "fullname"))

    # specify explicit parent entity
    query(User, Address).options(Load(User).load_only("name", "fullname"))

    # specify path
    query(User).options(joinedload(User.addresses).load_only("email_address"))

#### 特定于类的通配符[¶](#class-specific-wildcards "Permalink to this headline")

使用[`Load`](orm_query.html#sqlalchemy.orm.strategy_options.Load "sqlalchemy.orm.strategy_options.Load")，可以使用通配符为给定实体上的所有关系（或可能是列）设置加载，而不会影响其他任何关系：

    # lazyload all User relationships
    query(User).options(Load(User).lazyload("*"))

    # undefer all User columns
    query(User).options(Load(User).undefer("*"))

    # lazyload all Address relationships
    query(User).options(defaultload(User.addresses).lazyload("*"))

    # undefer all Address columns
    query(User).options(defaultload(User.addresses).undefer("*"))

[＃1418 T0\>](http://www.sqlalchemy.org/trac/ticket/1418)

### 新`text()`功能[¶](#new-text-capabilities "Permalink to this headline")

[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构获得新方法：

-   [`TextClause.bindparams()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.bindparams "sqlalchemy.sql.expression.TextClause.bindparams")
    allows bound parameter types and values to be set flexibly:

        # setup valuesplain
        stmt = text("SELECT id, name FROM user "
              "WHERE name=:name AND timestamp=:timestamp").\
              bindparams(name="ed", timestamp=datetime(2012, 11, 10, 15, 12, 35))

        # setup types and/or values
        stmt = text("SELECT id, name FROM user "
              "WHERE name=:name AND timestamp=:timestamp").\
              bindparams(
                  bindparam("name", value="ed"),
                  bindparam("timestamp", type_=DateTime()
              ).bindparam(timestamp=datetime(2012, 11, 10, 15, 12, 35))

-   [`TextClause.columns()`](core_sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")取代[`text()`](core_sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")的`typemap`选项，返回一个新的结构[`TextAsFrom`](core_selectable.html#sqlalchemy.sql.expression.TextAsFrom "sqlalchemy.sql.expression.TextAsFrom")：

        # turn a text() into an alias(), with a .c. collection:plain
        stmt = text("SELECT id, name FROM user").columns(id=Integer, name=String)
        stmt = stmt.alias()

        stmt = select([addresses]).select_from(
                      addresses.join(stmt), addresses.c.user_id == stmt.c.id)


        # or into a cte():
        stmt = text("SELECT id, name FROM user").columns(id=Integer, name=String)
        stmt = stmt.cte("x")

        stmt = select([addresses]).select_from(
                      addresses.join(stmt), addresses.c.user_id == stmt.c.id)

[＃2877 T0\>](http://www.sqlalchemy.org/trac/ticket/2877)

### 从SELECT [¶](#insert-from-select "Permalink to this headline")插入

经过几年毫无意义的拖延之后，这个相对较小的语法特征已被添加，并且也被支持到 0.8.3，所以在技术上 0.9 不是“新”。A
[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")
construct or other compatible construct can be passed to the new method
[`Insert.from_select()`](core_dml.html#sqlalchemy.sql.expression.Insert.from_select "sqlalchemy.sql.expression.Insert.from_select")
where it will be used to render an `INSERT .. SELECT` construct:

    >>> from sqlalchemy.sql import table, column
    >>> t1 = table('t1', column('a'), column('b'))
    >>> t2 = table('t2', column('x'), column('y'))
    >>> print(t1.insert().from_select(['a', 'b'], t2.select().where(t2.c.y == 5)))
    INSERT INTO t1 (a, b) SELECT t2.x, t2.y
    FROM t2
    WHERE t2.y = :y_1

该构造足够智能，可以容纳诸如类和[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象的 ORM 对象：

    s = Session()plainplain
    q = s.query(User.id, User.name).filter_by(name='ed')
    ins = insert(Address).from_select((Address.id, Address.email_address), q)

渲染：

    INSERT INTO addresses (id, email_address)
    SELECT users.id AS users_id, users.name AS users_name
    FROM users WHERE users.name = :name_1

[＃722 T0\>](http://www.sqlalchemy.org/trac/ticket/722)

### 新的 FOR UPDATE 支持在`select()`，`Query()` [¶](#new-for-update-support-on-select-query "Permalink to this headline")

An attempt is made to simplify the specification of the
`FOR UPDATE` clause on `SELECT`
statements made within Core and ORM, and support is added for the
`FOR UPDATE OF` SQL supported by Postgresql and
Oracle.

使用核心[`GenerativeSelect.with_for_update()`](core_selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update "sqlalchemy.sql.expression.GenerativeSelect.with_for_update")，诸如`FOR SHARE`和`NOWAIT`可以单独指定，而不是链接到任意字符串代码：

    stmt = select([table]).with_for_update(read=True, nowait=True, of=table)

在 Posgtresql 上面的语句可能呈现如下：

    SELECT table.a, table.b FROM table FOR SHARE OF table NOWAITplainplain

[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象获得了类似的方法[`Query.with_for_update()`](orm_query.html#sqlalchemy.orm.query.Query.with_for_update "sqlalchemy.orm.query.Query.with_for_update")，其行为方式相同。此方法取代了使用不同系统翻译`FOR UPDATE`子句的现有[`Query.with_lockmode()`](orm_query.html#sqlalchemy.orm.query.Query.with_lockmode "sqlalchemy.orm.query.Query.with_lockmode")方法。目前，“lockmode”字符串参数仍然被[`Session.refresh()`](orm_session_api.html#sqlalchemy.orm.session.Session.refresh "sqlalchemy.orm.session.Session.refresh")方法接受。

### 浮点数字符串转换精度可配置为本地浮点类型[¶](#floating-point-string-conversion-precision-configurable-for-native-floating-point-types "Permalink to this headline")

无论何时 DBAPI 返回要转换为 Python `Decimal()`的 Python 浮点类型，SQLAlchemy 都会执行的转换必然涉及将浮点值转换为字符串的中间步骤。用于此字符串转换的比例先前已硬编码为 10，现在可配置。该设置可以在[`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")以及[`Float`](core_type_basics.html#sqlalchemy.types.Float "sqlalchemy.types.Float")类型以及所有 SQL 和特定于方言的后代类型上使用参数`decimal_return_scale`If the type supports a `.scale` parameter,
as is the case with [`Numeric`](core_type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")
and some float types such as [`mysql.DOUBLE`](dialects_mysql.html#sqlalchemy.dialects.mysql.DOUBLE "sqlalchemy.dialects.mysql.DOUBLE"),
the value of `.scale` is used as the default for
`.decimal_return_scale` if it is not otherwise
specified. 如果`.scale`和`.decimal_return_scale`都不存在，则默认值为 10。例如。：

    from sqlalchemy.dialects.mysql import DOUBLEplain
    import decimal

    data = Table('data', metadata,
        Column('double_value',
                    mysql.DOUBLE(decimal_return_scale=12, asdecimal=True))
    )

    conn.execute(
        data.insert(),
        double_value=45.768392065789,
    )
    result = conn.scalar(select([data.c.double_value]))

    # previously, this would typically be Decimal("45.7683920658"),
    # e.g. trimmed to 10 decimal places

    # now we get 12, as requested, as MySQL can support this
    # much precision for DOUBLE
    assert result == decimal.Decimal("45.768392065789")

[＃2867 T0\>](http://www.sqlalchemy.org/trac/ticket/2867)

### 用于 ORM 查询的列包[¶](#column-bundles-for-orm-queries "Permalink to this headline")

[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")允许查询一组列，然后在查询返回的元组下面将这些列组合成一个名称。[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")的初始目的是 1.允许将“合成”ORM 列作为基于列的结果集中的单个值返回，而不是将它们展开到单个列中，并且 2.允许在 ORM 中创建自定义结果集构造，使用专门的列和返回类型，而不涉及映射类的更重量级的机制。

也可以看看

[Composite attributes are now returned as their object form when queried
on a per-attribute
basis](#migration-2824)查询时，复合属性现在以其对象形式返回

[Column Bundles](orm_loading_columns.html#bundles)

[＃2824 T0\>](http://www.sqlalchemy.org/trac/ticket/2824)

### 服务器端版本计数[¶](#server-side-version-counting "Permalink to this headline")

ORM的版本控制功能（现在也在[Configuring a Version
Counter](orm_versioning.html#mapper-version-counter)中有记录）现在可以使用服务器端版本计数方案（例如由触发器或数据库系统列生成的版本计数方案）以及条件编程方案在 version\_id\_counter 函数本身之外。通过为`version_id_generator`参数提供`False`值，ORM 将使用已设置的版本标识符，或者同时从每行中获取版本标识符 INSERT 或发布 UPDATE。当使用服务器生成的版本标识符时，强烈建议仅在具有强大 RETURNING 支持的后端使用此功能（Postgresql，SQL
Server；
Oracle 也支持 RETURNING，但 cx\_oracle 驱动程序只有有限的支持），否则额外的 SELECT 报表将会增加显着的性能开销。在[Server
Side Version
Counters](orm_versioning.html#server-side-version-counter)中提供的示例说明了Postgresql
`xmin`系统列的使用情况，以便将其与 ORM 的版本控制功能集成在一起。

也可以看看

[Server Side Version
Counters](orm_versioning.html#server-side-version-counter)

[＃2793 T0\>](http://www.sqlalchemy.org/trac/ticket/2793)

### `include_backrefs=False`选项用于`@validates` [¶](#include-backrefs-false-option-for-validates "Permalink to this headline")

[`validates()`](orm_mapped_attributes.html#sqlalchemy.orm.validates "sqlalchemy.orm.validates")函数现在接受一个选项`include_backrefs=True`，该选项将绕过针对事件从 backref：

    from sqlalchemy import Column, Integer, ForeignKey
    from sqlalchemy.orm import relationship, validates
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class A(Base):
        __tablename__ = 'a'

        id = Column(Integer, primary_key=True)
        bs = relationship("B", backref="a")

        @validates("bs")
        def validate_bs(self, key, item):
            print("A.bs validator")
            return item

    class B(Base):
        __tablename__ = 'b'

        id = Column(Integer, primary_key=True)
        a_id = Column(Integer, ForeignKey('a.id'))

        @validates("a", include_backrefs=False)
        def validate_a(self, key, item):
            print("B.a validator")
            return item

    a1 = A()
    a1.bs.append(B())  # prints only "A.bs validator"

[＃1535 T0\>](http://www.sqlalchemy.org/trac/ticket/1535)

### Postgresql JSON 类型[¶](#postgresql-json-type "Permalink to this headline")

Postgresql 方言现在使用[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")类型来补充[`postgresql.HSTORE`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.HSTORE "sqlalchemy.dialects.postgresql.HSTORE")类型。

也可以看看

[`postgresql.JSON`](dialects_postgresql.html#sqlalchemy.dialects.postgresql.JSON "sqlalchemy.dialects.postgresql.JSON")

[＃2581 T0\>](http://www.sqlalchemy.org/trac/ticket/2581)

### Automap Extension [¶](#automap-extension "Permalink to this headline")

在**0.9.1**中添加了一个新扩展，称为[`sqlalchemy.ext.automap`](orm_extensions_automap.html#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")。This
is an **experimental** extension which expands upon the functionality of
Declarative as well as the [`DeferredReflection`](orm_extensions_declarative_api.html#sqlalchemy.ext.declarative.DeferredReflection "sqlalchemy.ext.declarative.DeferredReflection")
class. Essentially, the extension provides a base class
[`AutomapBase`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
which automatically generates mapped classes and relationships between
them based on given table metadata.

通常使用的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")可能通过反射产生，但不要求使用反射。最基本的用法说明[`sqlalchemy.ext.automap`](orm_extensions_automap.html#module-sqlalchemy.ext.automap "sqlalchemy.ext.automap")如何基于反射的模式传递映射类，包括关系：

    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine

    Base = automap_base()

    # engine, suppose it has two tables 'user' and 'address' set up
    engine = create_engine("sqlite:///mydatabase.db")

    # reflect the tables
    Base.prepare(engine, reflect=True)

    # mapped classes are now created with names matching that of the table
    # name.
    User = Base.classes.user
    Address = Base.classes.address

    session = Session(engine)

    # rudimentary relationships are produced
    session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
    session.commit()

    # collection-based relationships are by default named "<classname>_collection"
    print(u1.address_collection)

除此之外，[`AutomapBase`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")类是声明性基础，并且支持所有声明性功能。“自动映射”功能可以与现有的显式声明的模式一起使用，以仅生成关系和丢失的类。命名方案和关系生产例程可以使用可调用函数来放弃。

It is hoped that the [`AutomapBase`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
system provides a quick and modernized solution to the problem that the
very famous [SQLSoup](https://sqlsoup.readthedocs.io/en/latest/) also
tries to solve, that of generating a quick and rudimentary object model
from an existing database on the fly. By addressing the issue strictly
at the mapper configuration level, and integrating fully with existing
Declarative class techniques, [`AutomapBase`](orm_extensions_automap.html#sqlalchemy.ext.automap.AutomapBase "sqlalchemy.ext.automap.AutomapBase")
seeks to provide a well-integrated approach to the issue of expediently
auto-generating ad-hoc mappings.

也可以看看

[Automap](orm_extensions_automap.html)

行为改进[¶](#behavioral-improvements "Permalink to this headline")
------------------------------------------------------------------

除非出现非常罕见和不寻常的假设情况，否则应该不会产生兼容性问题，但如果出现意外问题，则需要注意这些问题。

### 许多 JOIN 和 LEFT OUTER JOIN 表达式将不再被包含（SELECT \* FROM ..）AS ANON\_1 [¶](#many-join-and-left-outer-join-expressions-will-no-longer-be-wrapped-in-select-from-as-anon-1 "Permalink to this headline")

多年以来，SQLAlchemy ORM 一直被阻止在现有 JOIN 的右侧（通常是 LEFT OUTER
JOIN，因为 INNER JOIN 总是被压平）嵌套 JOIN。

    SELECT a.*, b.*, c.* FROM a LEFT OUTER JOIN (b JOIN c ON b.id = c.id) ON a.id

这是因为直到版本**3.7.16**的 SQLite 无法解析上述格式的语句：

    SQLite version 3.7.15.2 2013-01-09 11:53:05plain
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> create table a(id integer);
    sqlite> create table b(id integer);
    sqlite> create table c(id integer);
    sqlite> select a.id, b.id, c.id from a left outer join (b join c on b.id=c.id) on b.id=a.id;
    Error: no such column: b.id

右外连接当然是解决右括号的另一种方法；这将会非常复杂并且在视觉上很难实现，但幸运的是 SQLite 不支持 RIGHT
OUTER JOIN :)：

    sqlite> select a.id, b.id, c.id from b join c on b.id=c.id
       ...> right outer join a on b.id=a.id;
    Error: RIGHT and FULL OUTER JOINs are not currently supported

早在 2005 年，目前还不清楚其他数据库是否存在这种形式的问题，但今天似乎很清楚，除了 SQLite 之外，每一个测试数据库都能够支持它（Oracle
8 是一个非常古老的数据库，根本不支持 JOIN 关键字，但对于 Oracle 的语法，SQLAlchemy 总是有一个简单的重写方案）。更糟糕的是，应用 SELECT 的 SQLAlchemy 通常的解决方法通常会降低 Postgresql 和 MySQL 等平台的性能：

    SELECT a.*, anon_1.* FROM a LEFT OUTER JOIN (
                    SELECT b.id AS b_id, c.id AS c_id
                    FROM b JOIN c ON b.id = c.id
                ) AS anon_1 ON a.id=anon_1.b_id

使用连接表继承结构时，像以上形式的 JOIN 常见；任何时候[`Query.join()`](orm_query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")用于从某个父节点连接到一个连接表子类，或者当类似地使用[`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")时，SQLAlchemy 的 ORM 将始终确保为避免查询无法在 SQLite 上运行，嵌套的 JOIN 永远不会呈现。尽管 Core 一直支持更加紧凑的形式，但 ORM 必须避免它。

在 ON 子句中存在特殊标准的多对多关系中产生连接时，会出现另外一个问题。考虑像下面这样的热切加载连接：

    session.query(Order).outerjoin(Order.items)

假设从`Order`到`Item`的多对多实际上指的是像`Subitem`这样的子类，上述的 SQL 将如下所示：

    SELECT order.id, order.name
    FROM order LEFT OUTER JOIN order_item ON order.id = order_item.order_id
    LEFT OUTER JOIN item ON order_item.item_id = item.id AND item.type = 'subitem'

上述查询有什么问题？基本上，它会加载很多`order` /
`order_item`行，其中`item.type ==  t6 > '子项'`不正确。

从 SQLAlchemy
0.9 开始，我们采用了一种全新的方法。ORM 不再担心在封闭 JOIN 的右侧嵌套 JOIN，现在它将尽可能经常地渲染这些，同时仍然返回正确的结果。当传递 SQL 语句进行编译时，如果已知该后端不支持右嵌套 JOIN，则**dialect 编译器**将**重写连接**以适应目标后端（目前只有 SQLite
- 如果其他后端有这个问题，请让我们知道！）。

所以一个普通的`query(Parent).join(Subclass)`现在通常会产生一个更简单的表达式：

    SELECT parent.id AS parent_idplain
    FROM parent JOIN (
            base_table JOIN subclass_table
            ON base_table.id = subclass_table.id) ON parent.id = base_table.parent_id

加入像`query(Parent).options(joinedload(Parent.subclasses))`这样的预先加载将替换个别表而不是包装在`ANON_1`中：

    SELECT parent.*, base_table_1.*, subclass_table_1.* FROM parent
        LEFT OUTER JOIN (
            base_table AS base_table_1 JOIN subclass_table AS subclass_table_1
            ON base_table_1.id = subclass_table_1.id)
            ON parent.id = base_table_1.parent_id

多对多连接和 eagerloads 将嵌套“次”和“右”表：

    SELECT order.id, order.nameplain
    FROM order LEFT OUTER JOIN
    (order_item JOIN item ON order_item.item_id = item.id AND item.type = 'subitem')
    ON order_item.order_id = order.id

所有这些连接在使用特别指定`use_labels=True`的[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")语句进行呈现时（对于 ORM 发出的所有查询都是如此），这些连接都是“连接重写”
，这是将所有这些右嵌套连接重写为嵌套 SELECT 语句的过程，同时保持由[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")使用的相同标签。因此 SQLite 即使在 2013 年也不支持这种非常常见的 SQL 语法的一个数据库本身就具有额外的复杂性，上面的查询被重写为：

    -- sqlite only!
    SELECT parent.id AS parent_id
        FROM parent JOIN (
            SELECT base_table.id AS base_table_id,
                    base_table.parent_id AS base_table_parent_id,
                    subclass_table.id AS subclass_table_id
            FROM base_table JOIN subclass_table ON base_table.id = subclass_table.id
        ) AS anon_1 ON parent.id = anon_1.base_table_parent_id

    -- sqlite only!
    SELECT parent.id AS parent_id, anon_1.subclass_table_1_id AS subclass_table_1_id,
            anon_1.base_table_1_id AS base_table_1_id,
            anon_1.base_table_1_parent_id AS base_table_1_parent_id
    FROM parent LEFT OUTER JOIN (
        SELECT base_table_1.id AS base_table_1_id,
            base_table_1.parent_id AS base_table_1_parent_id,
            subclass_table_1.id AS subclass_table_1_id
        FROM base_table AS base_table_1
        JOIN subclass_table AS subclass_table_1 ON base_table_1.id = subclass_table_1.id
    ) AS anon_1 ON parent.id = anon_1.base_table_1_parent_id

    -- sqlite only!
    SELECT "order".id AS order_id
    FROM "order" LEFT OUTER JOIN (
            SELECT order_item_1.order_id AS order_item_1_order_id,
                order_item_1.item_id AS order_item_1_item_id,
                item.id AS item_id, item.type AS item_type
    FROM order_item AS order_item_1
        JOIN item ON item.id = order_item_1.item_id AND item.type IN (?)
    ) AS anon_1 ON "order".id = anon_1.order_item_1_order_id

注意

从 SQLAlchemy
1.1 开始，当 SQLite 版本**3.7.16**或更高版本被检测到时，SQLite 此功能中的变通方法将自动禁用，因为 SQLite 修复了对右嵌套连接的支持。

现在，[`Join.alias()`](core_selectable.html#sqlalchemy.sql.expression.Join.alias "sqlalchemy.sql.expression.Join.alias")，[`aliased()`](orm_query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")和[`with_polymorphic()`](orm_inheritance.html#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")函数支持一个新参数`flat=True`此标志默认情况下不会启用，以帮助实现向后兼容性 -
但现在，可选择的“polymorhpic”可作为目标而不生成任何子查询：

    employee_alias = with_polymorphic(Person, [Engineer, Manager], flat=True)plainplain

    session.query(Company).join(
                        Company.employees.of_type(employee_alias)
                    ).filter(
                        or_(
                            Engineer.primary_language == 'python',
                            Manager.manager_name == 'dilbert'
                        )
                    )

生成（除了 SQLite 以外）：

    SELECT companies.company_id AS companies_company_id, companies.name AS companies_nameplain
    FROM companies JOIN (
        people AS people_1
        LEFT OUTER JOIN engineers AS engineers_1 ON people_1.person_id = engineers_1.person_id
        LEFT OUTER JOIN managers AS managers_1 ON people_1.person_id = managers_1.person_id
    ) ON companies.company_id = people_1.company_id
    WHERE engineers.primary_language = %(primary_language_1)s
        OR managers.manager_name = %(manager_name_1)s

[＃2369](http://www.sqlalchemy.org/trac/ticket/2369)
[＃2587](http://www.sqlalchemy.org/trac/ticket/2587)

### 右连接的内部连接可用于连接的预先加载[¶](#right-nested-inner-joins-available-in-joined-eager-loads "Permalink to this headline")

从版本 0.9.4 开始，上面提到的右嵌套连接可以在加入的热切加载情况下启用，其中“外部”连接与右侧的“内部”连接。

通常情况下，加入一个像以下这样的热切加载链：

    query(User).options(joinedload("orders", innerjoin=False).joinedload("items", innerjoin=True))

不会产生内连接；由于来自用户 - \>订单的LEFT OUTER
JOIN，所以加入的预加载无法使用来自order-\>
items 的 INNER 连接，而无需更改返回的用户行，而是忽略“链接”`innerjoin=True`0.9.0 应该如何实现这将是，而不是：

    FROM users LEFT OUTER JOIN orders ON <onclause> LEFT OUTER JOIN items ON <onclause>plain

新的“右嵌套连接是好的”逻辑会启动，我们会得到：

    FROM users LEFT OUTER JOIN (orders JOIN items ON <onclause>) ON <onclause>

由于我们错过了这一点，为了避免进一步的回归，我们通过指定字符串`"nested"`到[`joinedload.innerjoin`](orm_loading_relationships.html#sqlalchemy.orm.joinedload.params.innerjoin "sqlalchemy.orm.joinedload")添加了上述功能：

    query(User).options(joinedload("orders", innerjoin=False).joinedload("items", innerjoin="nested"))plain

这个特性在 0.9.4 中是新的。

[＃2976 T0\>](http://www.sqlalchemy.org/trac/ticket/2976)

### ORM 可以使用 RETURNING [¶](#orm-can-efficiently-fetch-just-generated-insert-update-defaults-using-returning "Permalink to this headline")高效地获取刚生成的 INSERT / UPDATE 默认值

[`Mapper`](orm_mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")长期以来支持一个名为`eager_defaults=True`的未公开标志。此标志的作用是，当 INSERT 或 UPDATE 进行时，并且该行已知具有服务器生成的默认值时，SELECT 会立即跟随它，以便“热切”地加载这些新值。通常，服务器生成的列在对象上被标记为“过期”，因此除非应用程序在刷新后实际访问这些列，否则不会产生开销。因此，`eager_defaults`标志没有多大用处，因为它只能降低性能，并且仅用于支持异常事件方案，用户需要在刷新过程中立即使用默认值。

在 0.9 版本中，由于版本 ID 增强，现在`eager_defaults`可以为这些值发出 RETURNING 子句，因此在具有强大的 RETURNING 支持特别是 Postgresql 的后端上，ORM 可以获取新生成的默认值 SQL 表达式值与 INSERT 或 UPDATE 内联。`eager_defaults`, when enabled, makes use of RETURNING automatically when the
target backend and [`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
supports “implicit returning”.

### 子查询 Eager Loading 将对某些查询的最内层 SELECT 应用 DISTINCT [¶](#subquery-eager-loading-will-apply-distinct-to-the-innermost-select-for-some-queries "Permalink to this headline")

为了减少在涉及多对一关系时通过子查询预加载可以生成的重复行的数量，当连接将目标列指定为不包含多对一关系的列时，DISTINCT 关键字将应用于最内层的 SELECT 主键，就像在多对一时加载一样。

也就是说，当从 A-\> B进行多对一的子查询加载时：

    SELECT b.id AS b_id, b.name AS b_name, anon_1.b_id AS a_b_id
    FROM (SELECT DISTINCT a_b_id FROM a) AS anon_1
    JOIN b ON b.id = anon_1.a_b_id

由于`a.b_id`是非不同的外键，所以应用 DISTINCT 以消除多余的`a.b_id`。可以使用 flag `distinct_target_key`为特定的[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")无条件地打开或关闭行为，将值设置为`True`以无条件开启， `False`表示无条件关闭，而`None`表示当目标 SELECT 针对不包含完整主键的列时，此功能才会生效。在 0.9 中，`None`是默认值。

该选项也被反向移植到0.8，其中`distinct_target_key`选项默认为`False`。

虽然此功能旨在通过消除重复行来提高性能，但 SQL 本身中的`DISTINCT`关键字可能会对性能产生负面影响。如果 SELECT 中的列未被索引，那么`DISTINCT`可能会在行集上执行`ORDER BY`昂贵。通过保持功能仅限于希望在任何情况下索引的外键，预计新的默认值是合理的。

该功能也不能消除每一个可能的重复行为情况；如果在连接链的其他地方存在多对一的情况，则可能仍会出现重复行。

[＃2836 T0\>](http://www.sqlalchemy.org/trac/ticket/2836)

### Backref 处理程序现在可以传播多个层次[¶](#backref-handlers-can-now-propagate-more-than-one-level-deep "Permalink to this headline")

属性事件沿其“发起者”传递的机制，即与事件开始相关联的对象已被更改；而不是传递`AttributeImpl`，而是传递一个新对象[`attributes.Event`](orm_internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")；此对象引用`AttributeImpl`以及“操作令牌”，表示操作是附加，删除或替换操作。

属性事件系统不再查看此“启动器”对象以停止一系列递归属性事件。相反，由于相互依赖的 backref 处理程序而阻止无限递归的系统已被移至 ORM
backref 事件处理程序，该处理程序现在接管确保一系列相互依赖的事件（例如追加到集合 A 的角色）的角色。
bs，在响应中设置多对一的属性 Ba）并没有进入无穷无尽的递归流。这里的基本原理是，如果给定更多的事件传播的细节和控制权，backref 系统最终可以允许发生多于一个级别的操作；典型的情况是集合追加会导致多对一的替换操作，而这又会导致将项目从以前的集合中删除：

    class Parent(Base):
        __tablename__ = 'parent'

        id = Column(Integer, primary_key=True)
        children = relationship("Child", backref="parent")

    class Child(Base):
        __tablename__ = 'child'

        id = Column(Integer, primary_key=True)
        parent_id = Column(ForeignKey('parent.id'))

    p1 = Parent()
    p2 = Parent()
    c1 = Child()

    p1.children.append(c1)

    assert c1.parent is p1  # backref event establishes c1.parent as p1

    p2.children.append(c1)

    assert c1.parent is p2  # backref event establishes c1.parent as p2
    assert c1 not in p1.children  # second backref event removes c1 from p1.children

Above, prior to this change, the `c1` object would
still have been present in `p1.children`, even
though it is also present in `p2.children` at the
same time; the backref handlers would have stopped at replacing
`c1.parent` with `p2` instead of
`p1`. In 0.9, using the more detailed [`Event`](orm_internals.html#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")
object as well as letting the backref handlers make more detailed
decisions about these objects, the propagation can continue onto
removing `c1` from `p1.children`
while maintaining a check against the propagation from going into an
endless recursive loop.

最终用户代码是哪一个。使用[`AttributeEvents.set()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.set "sqlalchemy.orm.events.AttributeEvents.set")，[`AttributeEvents.append()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.append "sqlalchemy.orm.events.AttributeEvents.append")或[`AttributeEvents.remove()`](orm_events.html#sqlalchemy.orm.events.AttributeEvents.remove "sqlalchemy.orm.events.AttributeEvents.remove")事件，以及 b。由于这些事件可能需要修改以防止递归循环，所以启动进一步的属性修改操作，因为属性系统不再阻止事件链在没有 backref 事件处理程序的情况下无限传播。此外，取决于`initiator`值的代码需要根据新的 API 进行调整，并且必须准备好`initiator`的值以从其原始值因为 backref 处理程序现在可以为某些操作交换新的`initiator`值。

[＃2789 T0\>](http://www.sqlalchemy.org/trac/ticket/2789)

### 输入系统现在处理呈现“文字绑定”值的任务[¶](#the-typing-system-now-handles-the-task-of-rendering-literal-bind-values "Permalink to this headline")

A new method is added to [`TypeEngine`](core_type_api.html#sqlalchemy.types.TypeEngine "sqlalchemy.types.TypeEngine")
[`TypeEngine.literal_processor()`](core_type_api.html#sqlalchemy.types.TypeEngine.literal_processor "sqlalchemy.types.TypeEngine.literal_processor")
as well as [`TypeDecorator.process_literal_param()`](core_custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")
for [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
which take on the task of rendering so-called “inline literal paramters”
- parameters that normally render as “bound” values, but are instead
being rendered inline into the SQL statement due to the compiler
configuration. 当为诸如[`CheckConstraint`](core_constraints.html#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")的结构生成DDL时，以及在使用诸如`op.inline_literal()`的结构时由 Alembic 使用此功能。之前，检查了一些简单的“isinstance”检查了一些基本类型，并且无条件地使用了“绑定处理器”，从而导致字符串被过早编码为 utf-8 等问题。

Custom types written with [`TypeDecorator`](core_custom_types.html#sqlalchemy.types.TypeDecorator "sqlalchemy.types.TypeDecorator")
should continue to work in “inline literal” scenarios, as the
[`TypeDecorator.process_literal_param()`](core_custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")
falls back to [`TypeDecorator.process_bind_param()`](core_custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param "sqlalchemy.types.TypeDecorator.process_bind_param")
by default, as these methods usually handle a data manipulation, not as
much how the data is presented to the database.
[`TypeDecorator.process_literal_param()`](core_custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param "sqlalchemy.types.TypeDecorator.process_literal_param")
can be specified to specifically produce a string representing how a
value should be rendered into an inline DDL statement.

[＃2838 T0\>](http://www.sqlalchemy.org/trac/ticket/2838)

### 模式标识符现在携带自己的引用信息[¶](#schema-identifiers-now-carry-along-their-own-quoting-information "Permalink to this headline")

这种改变简化了 Core 对所谓“quote”标志的使用，例如传递给[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的`quote`标志。该标志现在已内化在字符串名称本身内，现在它表示为字符串子类[`quoted_name`](core_sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")的一个实例。现在，[`IdentifierPreparer`](core_internals.html#sqlalchemy.sql.compiler.IdentifierPreparer "sqlalchemy.sql.compiler.IdentifierPreparer")完全依赖于由[`quoted_name`](core_sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")对象报告的引用首选项，而不是在大多数情况下检查任何显式的`quote`标志。这里解决的问题包括各种区分大小写的方法（如[`Engine.has_table()`](core_connections.html#sqlalchemy.engine.Engine.has_table "sqlalchemy.engine.Engine.has_table")）以及方言中的类似方法现在可以使用明确引用的名称，而不需要复杂化或引入向后不兼容的更改到那些 API（其中许多是第三方），并带有引用标志的详细信息
-
特别是更广泛的标识符现在可以与 Oracle，Firebird 和 DB2 等所谓的“大写字母”后端正常工作（后端存储和根据不区分大小写的名称使用全部大写报告表和列名称）。

[`quoted_name`](core_sqlelement.html#sqlalchemy.sql.elements.quoted_name "sqlalchemy.sql.elements.quoted_name")对象在内部根据需要使用；但是，如果其他关键字需要固定的引用偏好，则该类可公开使用。

[＃2812 T0\>](http://www.sqlalchemy.org/trac/ticket/2812)

### 改进了布尔常量，NULL 常量，连词的渲染[¶](#improved-rendering-of-boolean-constants-null-constants-conjunctions "Permalink to this headline")

新功能已添加到[`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")和[`false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")常量中，特别是与[`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")和[`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")函数以及 WHERE
/ HAVING 子句与这些类型，整体布尔类型以及[`null()`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")常量的行为。

从这样的表格开始：

    from sqlalchemy import Table, Boolean, Integer, Column, MetaData

    t1 = Table('t', MetaData(), Column('x', Boolean()), Column('y', Integer))

select 结构现在将布尔列作为二进制表达式在不具有`true`
/ `false`常量 beahvior 的后端渲染：

    >>> from sqlalchemy import select, and_, false, true
    >>> from sqlalchemy.dialects import mysql, postgresql

    >>> print(select([t1]).where(t1.c.x).compile(dialect=mysql.dialect()))
    SELECT t.x, t.y  FROM t WHERE t.x = 1

The [`and_()`](core_sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")
and [`or_()`](core_sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")
constructs will now exhibit quasi “short circuit” behavior, that is
truncating a rendered expression, when a [`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
or [`false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")
constant is present:

    >>> print(select([t1]).where(and_(t1.c.y > 5, false())).compile(plain
    ...     dialect=postgresql.dialect()))
    SELECT t.x, t.y FROM t WHERE false

[`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")可以用作构建表达式的基础：

    >>> expr = true()plain
    >>> expr = expr & (t1.c.y > 5)
    >>> print(select([t1]).where(expr))
    SELECT t.x, t.y FROM t WHERE t.y > :y_1

The boolean constants [`true()`](core_sqlelement.html#sqlalchemy.sql.expression.true "sqlalchemy.sql.expression.true")
and [`false()`](core_sqlelement.html#sqlalchemy.sql.expression.false "sqlalchemy.sql.expression.false")
themselves render as `0 = 1` and `1 = 1` for a backend with no boolean constants:

    >>> print(select([t1]).where(and_(t1.c.y > 5, false())).compile(
    ...     dialect=mysql.dialect()))
    SELECT t.x, t.y FROM t WHERE 0 = 1

对`None`的解释至少在现在是一致的，而不是特别有效的 SQL：

    >>> print(select([t1.c.x]).where(None))plain
    SELECT t.x FROM t WHERE NULL

    >>> print(select([t1.c.x]).where(None).where(None))
    SELECT t.x FROM t WHERE NULL AND NULL

    >>> print(select([t1.c.x]).where(and_(None, None)))
    SELECT t.x FROM t WHERE NULL AND NULL

[＃2804 T0\>](http://www.sqlalchemy.org/trac/ticket/2804)

### 现在，标签构造可以在 ORDER BY [¶](#label-constructs-can-now-render-as-their-name-alone-in-an-order-by "Permalink to this headline")中作为其名称单独渲染

对于在 column 子句和 SELECT 的 ORDER BY 子句中都使用[`Label`](core_sqlelement.html#sqlalchemy.sql.expression.Label "sqlalchemy.sql.expression.Label")的情况，标签将在 ORDER
BY 子句中呈现为它的名称，假设底层方言报告支持此功能。

例如。例如：

    from sqlalchemy.sql import table, column, select, func

    t = table('t', column('c1'), column('c2'))
    expr = (func.foo(t.c.c1) + t.c.c2).label("expr")

    stmt = select([expr]).order_by(expr)

    print(stmt)

0.9 之前会呈现为：

    SELECT foo(t.c1) + t.c2 AS exprplain
    FROM t ORDER BY foo(t.c1) + t.c2

现在呈现为：

    SELECT foo(t.c1) + t.c2 AS exprplainplain
    FROM t ORDER BY expr

如果标签没有进一步嵌入到 ORDER BY 中的表达式中，ORDER
BY 只呈现标签，而不是简单的`ASC`或`DESC`。

上述格式适用于所有测试过的数据库，但可能与旧数据库版本（MySQL 4？Oracle
8？等等。）。根据用户报告，我们可以添加将禁用基于数据库版本检测的功能的规则。

[＃1068 T0\>](http://www.sqlalchemy.org/trac/ticket/1068)

### `RowProxy` now has tuple-sorting behavior[¶](#rowproxy-now-has-tuple-sorting-behavior "Permalink to this headline")

[`RowProxy`](core_connections.html#sqlalchemy.engine.RowProxy "sqlalchemy.engine.RowProxy")对象的行为很像一个元组，但直到现在，如果使用`sorted()`对它们进行排序，则它们不会排序为元组。`__eq__()`方法现在将两边都作为元组进行比较，并且还添加了`__lt__()`方法：

    users.insert().execute(
            dict(user_id=1, user_name='foo'),
            dict(user_id=2, user_name='bar'),
            dict(user_id=3, user_name='def'),
        )

    rows = users.select().order_by(users.c.user_name).execute().fetchall()

    eq_(rows, [(2, 'bar'), (3, 'def'), (1, 'foo')])

    eq_(sorted(rows), [(1, 'foo'), (2, 'bar'), (3, 'def')])

[＃2848 T0\>](http://www.sqlalchemy.org/trac/ticket/2848)

### 当类型可用时，不带类型的 bindparam()构造会通过复制进行升级[¶](#a-bindparam-construct-with-no-type-gets-upgraded-via-copy-when-a-type-is-available "Permalink to this headline")

“升级”一个[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")结构以承担封闭表达式的类型的逻辑已经通过两种方式得到了改进。First,
the [`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
object is **copied** before the new type is assigned, so that the given
[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")
is not mutated in place. 其次，在编译[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构时，同样的操作发生在关于通过[`ValuesBase.values()`](core_dml.html#sqlalchemy.sql.expression.ValuesBase.values "sqlalchemy.sql.expression.ValuesBase.values")方法。

如果给定一个无类型的[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")：

    bp = bindparam("some_col")

如果我们使用这个参数如下：

    expr = mytable.c.col == bp

The type for `bp` remains as `NullType`, however if `mytable.c.col` is of type
`String`, then `expr.right`,
that is the right side of the binary expression, will take on the
`String` type. 以前，`bp`本身会被更改为`String`作为其类型。

同样，此操作发生在[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")中：

    stmt = mytable.update().values(col=bp)plain

上面，`bp`保持不变，但执行语句时将使用`String`类型，我们可以通过检查`binds`字典来看到：

    >>> compiled = stmt.compile()
    >>> compiled.binds['some_col'].type
    String

该功能允许自定义类型在 INSERT /
UPDATE 语句中发挥其预期效果，而无需在每个[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")表达式中明确指定这些类型。

潜在的向后兼容变化涉及两个不太可能的情况。由于绑定参数是**克隆**，用户不应该依赖一旦创建就对[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")构造进行就地更改。另外，在[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")或[`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")语句中使用[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")的代码依赖于[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")

[＃2850 T0\>](http://www.sqlalchemy.org/trac/ticket/2850)

### 列可以可靠地从通过 ForeignKey [¶](#columns-can-reliably-get-their-type-from-a-column-referred-to-via-foreignkey "Permalink to this headline")引用的列中获取它们的类型

有一个长期以来的行为，说[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")可以在没有类型的情况下声明，只要[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")由[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")引用，并且引用列中的类型将被复制到该列中。问题是这个功能从来没有很好的工作，并没有被维护。The
core issue was that the [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
object doesn’t know what target [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
it refers to until it is asked, typically the first time the foreign key
is used to construct a [`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join").
因此，直到那个时候，父[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")不会有类型，或者更具体地说，它将具有默认类型的[`NullType`](core_type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")。

虽然需要很长时间，但重新组织[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象初始化的工作已完成，因此该功能最终可以接受。At
the core of the change is that the [`ForeignKey.column`](core_constraints.html#sqlalchemy.schema.ForeignKey.column "sqlalchemy.schema.ForeignKey.column")
attribute no longer lazily initializes the location of the target
[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column");
the issue with this system was that the owning [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
would be stuck with [`NullType`](core_type_api.html#sqlalchemy.types.NullType "sqlalchemy.types.NullType")
as its type until the [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
happened to be used.

In the new version, the [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
coordinates with the eventual [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
it will refer to using internal attachment events, so that the moment
the referencing [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
is associated with the [`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData"),
all [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
objects that refer to it will be sent a message that they need to
initialize their parent column.
这个系统比较复杂，但工作更加扎实；作为奖励，现在有各种各样的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
/ [`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")配置场景的测试，并且错误消息已被改进为非常特定于不少于 7 个不同的错误条件。

现在可以正常工作的情景包括：

1.  只要目标[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")与相同的[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")关联，[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")中的类型立即出现。无论首先配置哪一侧，这都可以工作：

        >>> from sqlalchemy import Table, MetaData, Column, Integer, ForeignKeyplain
        >>> metadata = MetaData()
        >>> t2 = Table('t2', metadata, Column('t1id', ForeignKey('t1.id')))
        >>> t2.c.t1id.type
        NullType()
        >>> t1 = Table('t1', metadata, Column('id', Integer, primary_key=True))
        >>> t2.c.t1id.type
        Integer()

2.  系统现在也可以使用[`ForeignKeyConstraint`](core_constraints.html#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")：

        >>> from sqlalchemy import Table, MetaData, Column, Integer, ForeignKeyConstraintplain
        >>> metadata = MetaData()
        >>> t2 = Table('t2', metadata,
        ...     Column('t1a'), Column('t1b'),
        ...     ForeignKeyConstraint(['t1a', 't1b'], ['t1.a', 't1.b']))
        >>> t2.c.t1a.type
        NullType()
        >>> t2.c.t1b.type
        NullType()
        >>> t1 = Table('t1', metadata,
        ...     Column('a', Integer, primary_key=True),
        ...     Column('b', Integer, primary_key=True))
        >>> t2.c.t1a.type
        Integer()
        >>> t2.c.t1b.type
        Integer()

3.  它甚至适用于“多跳” - 也就是说，引用另一个[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的引用[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的[`ForeignKey`](core_constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")：

        >>> from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey
        >>> metadata = MetaData()
        >>> t2 = Table('t2', metadata, Column('t1id', ForeignKey('t1.id')))
        >>> t3 = Table('t3', metadata, Column('t2t1id', ForeignKey('t2.t1id')))
        >>> t2.c.t1id.type
        NullType()
        >>> t3.c.t2t1id.type
        NullType()
        >>> t1 = Table('t1', metadata, Column('id', Integer, primary_key=True))
        >>> t2.c.t1id.type
        Integer()
        >>> t3.c.t2t1id.type
        Integer()

[＃1765 T0\>](http://www.sqlalchemy.org/trac/ticket/1765)

方言改变[¶](#dialect-changes "Permalink to this headline")
----------------------------------------------------------

### Firebird `fdb`现在是默认的 Firebird 方言。[¶](#firebird-fdb-is-now-the-default-firebird-dialect "Permalink to this headline")

如果创建的引擎没有方言说明符，即`firebird://`，则现在使用`fdb`方言。`fdb` is a `kinterbasdb` compatible DBAPI which
per the Firebird project is now their official Python driver.

[＃2504 T0\>](http://www.sqlalchemy.org/trac/ticket/2504)

### Firebird `fdb`和`kinterbasdb` set `retaining=False`默认[¶](#firebird-fdb-and-kinterbasdb-set-retaining-false-by-default "Permalink to this headline")

Both the `fdb` and `kinterbasdb`
DBAPIs support a flag `retaining=True` which can be
passed to the `commit()` and `rollback()` methods of its connection.
此标志的记录基本原理是为了提高性能，DBAPI 可以为后续事务重新使用内部事务状态。However,
newer documentation refers to analyses of Firebird’s “garbage
collection” which expresses that this flag can have a negative effect on
the database’s ability to process cleanup tasks, and has been reported
as *lowering* performance as a result.

鉴于这些信息，该标记如何实际使用尚不清楚，而且由于它似乎只是一种性能增强功能，现在默认为`False`。可以通过将标志`retaining=True`传递给[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")调用来控制该值。这是一个新标志，从 0.8.2 开始添加，因此 0.8.2 上的应用程序可以根据需要开始将其设置为`True`或`False`。

也可以看看

[`sqlalchemy.dialects.firebird.fdb`](dialects_firebird.html#module-sqlalchemy.dialects.firebird.fdb "sqlalchemy.dialects.firebird.fdb")

[`sqlalchemy.dialects.firebird.kinterbasdb`](dialects_firebird.html#module-sqlalchemy.dialects.firebird.kinterbasdb "sqlalchemy.dialects.firebird.kinterbasdb")

[http://pythonhosted.org/fdb/usage-guide.html\#retaining-transactions](http://pythonhosted.org/fdb/usage-guide.html#retaining-transactions)
- 有关“保留”标志的信息。

[＃2763 T0\>](http://www.sqlalchemy.org/trac/ticket/2763)
