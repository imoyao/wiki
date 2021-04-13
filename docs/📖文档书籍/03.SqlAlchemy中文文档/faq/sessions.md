---
title: 会话/查询
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/faq/sessions/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - faq
tags:
---
会话/查询[¶](#sessions-queries "Permalink to this headline")
============================================================

-   [我正在使用我的会话重新加载数据，但没有看到我在别处提交的更改](#i-m-re-loading-data-with-my-session-but-it-isn-t-seeing-changes-that-i-committed-elsewhere)
-   [“此会话的事务由于刷新期间的先前异常而回滚。”（或类似的）](#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar)
    -   [但为什么 flush()坚持发布 ROLLBACK？](#but-why-does-flush-insist-on-issuing-a-rollback)
    -   [但为什么自动调用 ROLLBACK 不够？为什么我必须再次 ROLLBACK？](#but-why-isn-t-the-one-automatic-call-to-rollback-enough-why-must-i-rollback-again)
-   [我如何进行查询，以便每次查询都添加特定的过滤器？](#how-do-i-make-a-query-that-always-adds-a-certain-filter-to-every-query)
-   [我创建了一个针对外部联接的映射，并且在查询返回行时，不返回对象。为什么不呢？](#i-ve-created-a-mapping-against-an-outer-join-and-while-the-query-returns-rows-no-objects-are-returned-why-not)
-   [我使用`joinedload()`或`lazy=False`创建 JOIN / OUTER
    JOIN，并且在尝试添加 WHERE 时 SQLAlchemy 未构造正确的查询，ORDER
    BY，LIMIT 等（依赖于（OUTER）JOIN）](#i-m-using-joinedload-or-lazy-false-to-create-a-join-outer-join-and-sqlalchemy-is-not-constructing-the-correct-query-when-i-try-to-add-a-where-order-by-limit-etc-which-relies-upon-the-outer-join)
-   [查询没有`__len__()`，为什么不能？](#query-has-no-len-why-not)
-   [如何使用带有 ORM 查询的文本 SQL？](#how-do-i-use-textual-sql-with-orm-queries)
-   [我在调用`Session.delete(myobject)`，并且它不会从父集合中移除！](#i-m-calling-session-delete-myobject-and-it-isn-t-removed-from-the-parent-collection)
-   [当我加载对象时为什么不调用`__init__()`？](#why-isn-t-my-init-called-when-i-load-objects)
-   [如何在 SA 的 ORM 中使用 ON DELETE
    CASCADE？](#how-do-i-use-on-delete-cascade-with-sa-s-orm)
-   [我将实例中的“foo\_id”属性设置为“7”，但“foo”属性仍然是`None` - 不应该使用 id＃7 加载 Foo 吗？ t0
    \>](#i-set-the-foo-id-attribute-on-my-instance-to-7-but-the-foo-attribute-is-still-none-shouldn-t-it-have-loaded-foo-with-id-7)
-   [我如何走路与给定对象相关的所有对象？](#how-do-i-walk-all-objects-that-are-related-to-a-given-object)
-   [有没有一种方法可以在不查询关键字并获取包含该关键字的行的引用的情况下仅自动获取唯一关键字（或其他类型的对象）？](#is-there-a-way-to-automagically-have-only-unique-keywords-or-other-kinds-of-objects-without-doing-a-query-for-the-keyword-and-getting-a-reference-to-the-row-containing-that-keyword)

我正在使用会话重新加载数据，但没有看到我在其他地方提交的更改[¶](#i-m-re-loading-data-with-my-session-but-it-isn-t-seeing-changes-that-i-committed-elsewhere "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

关于这种行为的主要问题是，即使事务处于*可序列化*隔离状态，即使事务不是（通常不是），该事务也会像事务一样进行。实际上，这意味着会话不会更改已在事务范围内读取的任何数据。

如果术语“隔离级别”不熟悉，那么您首先需要阅读以下链接：

[隔离级别](https://en.wikipedia.org/wiki/Isolation_%28database_systems%29)

简而言之，可序列化的隔离级别通常意味着，一旦在事务中选择了一系列行，每次重新发出该 SELECT 时都会得到*相同的数据*。如果您处于隔离级别较低的“可重复读取”级别，则会看到新添加的行（不再看到已删除的行），但对于已加载**的行，您将不会看到任何变化。只有在较低的隔离级别时，例如“读取提交”，是否有可能看到一行数据改变其价值。

有关使用 SQLAlchemy ORM 时控制隔离级别的信息，请参阅[Setting Transaction
Isolation
Levels](orm_session_transaction.html#session-transaction-isolation)。

为了大大简化事情，[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本身按照完全独立的事务工作，并且不会覆盖已经读取的任何映射属性，除非您告诉它。尝试重新读取正在进行的事务中加载的数据的用例是一种*罕见*用例，在很多情况下这种用例不起作用，所以这被认为是例外，而不是规范；为了在这个异常中工作，提供了几种方法来允许在正在进行的事务的上下文中重新加载特定的数据。

当我们谈论[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，要理解“交易”的含义，您的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")仅用于交易。这是对[Managing
Transactions](orm_session_transaction.html#unitofwork-transaction)的概述。

一旦我们发现了隔离级别，并且我们认为隔离级别设置的足够低，这样如果我们重新选择一行，我们应该在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

从最普通到最不重要的三种方式：

1.  We simply end our transaction and start a new one on next access
    with our [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    by calling [`Session.commit()`](orm_session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
    (note that if the [`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    is in the lesser-used “autocommit” mode, there would be a call to
    [`Session.begin()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")
    as well).
    绝大多数的应用程序和用例没有任何问题，无法在其他事务中“看见”数据，因为他们坚持这种模式，这是**短期交易的最佳实践的核心\<
    T0\>。**请参阅[When do I construct a Session, when do I commit it,
    and when do I close
    it?](orm_session_basics.html#session-faq-whentocreate)对此有一些想法。
2.  我们告诉我们的[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")重新读取它已经读取的行，当我们使用[`Session.expire_all()`](orm_session_api.html#sqlalchemy.orm.session.Session.expire_all "sqlalchemy.orm.session.Session.expire_all")或[`Session.expire()`](orm_session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")，或使用`Session.refresh`立即在对象上。有关详细信息，请参阅[Refreshing /
    Expiring](orm_session_state_management.html#session-expire)。
3.  我们可以运行整个查询，同时将它们设置为在使用[`Query.populate_existing()`](orm_query.html#sqlalchemy.orm.query.Query.populate_existing "sqlalchemy.orm.query.Query.populate_existing")读取行时明确覆盖已加载的对象。

But remember, **the ORM cannot see changes in rows if our isolation
level is repeatable read or higher, unless we start a new transaction**.

“此会话的事务由于刷新期间的先前异常而回滚。”（或类似的）[¶](#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This is an error that occurs when a [`Session.flush()`](orm_session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")
raises an exception, rolls back the transaction, but further commands
upon the Session are called without an explicit call to
[`Session.rollback()`](orm_session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")
or [`Session.close()`](orm_session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close").

它通常对应于捕获[`Session.flush()`](orm_session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")或[`Session.commit()`](orm_session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")中的异常并且没有正确处理异常的应用程序。例如：

    from sqlalchemy import create_engine, Column, Integerplainplainplainplainplainplainplainplain
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base(create_engine('sqlite://'))

    class Foo(Base):
        __tablename__ = 'foo'
        id = Column(Integer, primary_key=True)

    Base.metadata.create_all()

    session = sessionmaker()()

    # constraint violation
    session.add_all([Foo(id=1), Foo(id=1)])

    try:
        session.commit()
    except:
        # ignore error
        pass

    # continue using session without rolling back
    session.commit()

[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的用法应该符合类似于以下的结构：

    try:plainplainplainplainplain
        <use session>
        session.commit()
    except:
       session.rollback()
       raise
    finally:
       session.close()  # optional, depends on use case

许多事情可能导致尝试/除了冲刷除外失败。您应始终对会话操作进行某种“构架”，以便连接和事务资源具有确定的边界，否则应用程序并未真正控制其资源的使用。这并不是说你需要在应用程序中放置 try
/
except 块，相反，这将是一个可怕的想法。您应该构建您的应用程序，以便在会话操作周围有一个（或几个）“框架”点。

有关如何组织[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")使用情况的详细讨论，请参阅[When
do I construct a Session, when do I commit it, and when do I close
it?](orm_session_basics.html#session-faq-whentocreate)。

### 但为什么 flush()坚持发布 ROLLBACK？[¶](#but-why-does-flush-insist-on-issuing-a-rollback "Permalink to this headline")

如果[`Session.flush()`](orm_session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")可以部分完成然后不回滚会很好，但是这超出了它当前的能力，因为它的内部簿记必须被修改，以便它可以在任何时候被暂停时间，并与已刷新到数据库的内容完全一致。虽然这在理论上是可行的，但是由于许多数据库操作在任何情况下都需要 ROLLBACK，所以增强的有用性大大降低了。特别是 Postgres 有一些操作，一旦失败，交易不允许继续：

    test=> create table foo(id integer primary key);plainplainplainplainplain
    NOTICE:  CREATE TABLE / PRIMARY KEY will create implicit index "foo_pkey" for table "foo"
    CREATE TABLE
    test=> begin;
    BEGIN
    test=> insert into foo values(1);
    INSERT 0 1
    test=> commit;
    COMMIT
    test=> begin;
    BEGIN
    test=> insert into foo values(1);
    ERROR:  duplicate key value violates unique constraint "foo_pkey"
    test=> insert into foo values(2);
    ERROR:  current transaction is aborted, commands ignored until end of transaction block

SQLAlchemy 提供的解决这两个问题的方法是通过[`Session.begin_nested()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")支持 SAVEPOINT。通过使用[`Session.begin_nested()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")，您可以构建一个可能在事务内失败的操作，然后在保持封闭事务的同时“回滚”到失败前的点。

### 但为什么不是自动调用 ROLLBACK 足够？为什么我必须再次 ROLLBACK？[¶](#but-why-isn-t-the-one-automatic-call-to-rollback-enough-why-must-i-rollback-again "Permalink to this headline")

这也是[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")提供了一个一致的接口并拒绝猜测它正在使用的上下文的问题。例如，[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")支持多个级别内的“成帧”。比如，假设你有一个装饰器`@with_session()`，它这样做了：

    def with_session(fn):plainplainplainplainplainplain
       def go(*args, **kw):
           session.begin(subtransactions=True)
           try:
               ret = fn(*args, **kw)
               session.commit()
               return ret
           except:
               session.rollback()
               raise
       return go

如果上面的装饰器已经不存在，则开始一个事务，然后提交它，如果它是创建者。“subtransactions”标志表示如果[`Session.begin()`](orm_session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")已被封闭函数调用，除了计数器递增外，什么都不会发生
- 当[`Session.commit()`](orm_session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")它允许这种使用模式：

    @with_session
    def one():
       # do stuffplainplainplain
       two()


    @with_sessionplainplainplain
    def two():
       # etc.

    one()

    two()

`one()`可以调用`two()`，或`two()`可以自行调用，`@with_session`正如你所看到的，如果`two()`调用引发异常然后发出`rollback()`的`flush()`，那么*always*是装饰器执行的第二个`rollback()`，可能还有第三个对应于两个装饰器级别。如果`flush()`将`rollback()`推到栈顶，然后我们说所有剩下的`rollback()`写得不好的封闭方法可能会抑制异常，然后在没有错误的情况下调用`commit()`，然后您有一个无提示失败条件。人们得到这个错误的主要原因实际上是因为他们没有编写干净的“框架”代码，而且他们还会遇到其他问题。

If you think the above use case is a little exotic, the same kind of
thing comes into play if you want to SAVEPOINT- you might call
`begin_nested()` several times, and the
`commit()`/`rollback()` calls
each resolve the most recent `begin_nested()`. The
meaning of `rollback()` or `commit()` is dependent upon which enclosing block it is called, and you
might have any sequence of `rollback()`/`commit()` in any order, and its the level
of nesting that determines their behavior.

在上述两种情况下，如果`flush()`违反了事务块的嵌套，则根据情况，行为将从“魔术”到无声失败到公然中断代码流。

`flush()` makes its own “subtransaction”, so that a
transaction is started up regardless of the external transactional
state, and when complete it calls `commit()`, or
`rollback()` upon failure - but that
`rollback()` corresponds to its own subtransaction -
it doesn’t want to guess how you’d like to handle the external “framing”
of the transaction, which could be nested many levels with any
combination of subtransactions and real SAVEPOINTs.
开始/结束“帧”的工作与`flush()`外部的代码保持一致，并且我们决定这是最一致的方法。

我如何做一个总是为每个查询添加特定过滤器的查询？[¶](#how-do-i-make-a-query-that-always-adds-a-certain-filter-to-every-query "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------------------------

请参阅[PreFilteredQuery](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/PreFilteredQuery)中的配方。

我已经创建了一个针对外部连接的映射，并且在查询返回行时，不会返回任何对象。为什么不呢？[¶](#i-ve-created-a-mapping-against-an-outer-join-and-while-the-query-returns-rows-no-objects-are-returned-why-not "Permalink to this headline")
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

由外部联接返回的行可能包含 NULL 作为主键的一部分，因为主键是两个表的组合。[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象会忽略没有可接受主键的传入行。Based
on the setting of the `allow_partial_pks` flag on
[`mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper"),
a primary key is accepted if the value has at least one non-NULL value,
or alternatively if the value has no NULL values.
请参阅[`mapper()`](orm_mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")中的`allow_partial_pks`。

I’m using `joinedload()` or `lazy=False` to create a JOIN/OUTER JOIN and SQLAlchemy is not constructing the correct query when I try to add a WHERE, ORDER BY, LIMIT, etc. （依赖于（OUTER）JOIN）[¶](#i-m-using-joinedload-or-lazy-false-to-create-a-join-outer-join-and-sqlalchemy-is-not-constructing-the-correct-query-when-i-try-to-add-a-where-order-by-limit-etc-which-relies-upon-the-outer-join "Permalink to this headline")
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

通过加入的预先加载生成的连接仅用于完全加载相关集合，并且设计为不会影响查询的主要结果。由于它们是匿名别名，因此不能直接引用它们。

有关此行为的详细信息，请参阅[The Zen of Eager
Loading](orm_loading_relationships.html#zen-of-eager-loading)。

查询没有`__len__()`，为什么不呢？[¶](#query-has-no-len-why-not "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------

应用于对象的 Python `__len__()`魔术方法允许使用`len()`内建来确定集合的长度。It’s intuitive that a SQL query object
would link `__len__()` to the [`Query.count()`](orm_query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")
method, which emits a SELECT COUNT.
这是不可能的原因是因为评估查询作为列表会导致两个 SQL 调用，而不是一个：

    class Iterates(object):plainplainplainplain
        def __len__(self):
            print("LEN!")
            return 5

        def __iter__(self):
            print("ITER!")
            return iter([1, 2, 3, 4, 5])

    list(Iterates())

输出：

    ITER!plainplain
    LEN!

如何在 ORM 查询中使用文本 SQL？[¶](#how-do-i-use-textual-sql-with-orm-queries "Permalink to this headline")
--------------------------------------------------------------------------------------------------------

看到：

-   [Using Textual SQL](orm_tutorial.html#orm-tutorial-literal-sql) -
    具有[`Query`](orm_query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")的特设文本块
-   [Using SQL Expressions with
    Sessions](orm_persistence_techniques.html#session-sql-expressions) -
    直接在文本 SQL 中使用[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

我打电话给`Session.delete(myobject)`，它不会从父集合中移除！[¶](#i-m-calling-session-delete-myobject-and-it-isn-t-removed-from-the-parent-collection "Permalink to this headline")
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

有关此行为的描述，请参阅[Deleting from
Collections](orm_session_basics.html#session-deleting-from-collections)。

为什么当我加载对象时不调用`__init__()`？[¶](#why-isn-t-my-init-called-when-i-load-objects "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------------------------

有关此行为的描述，请参阅[Constructors and Object
Initialization](orm_constructors.html#mapping-constructors)。

如何在 SA 的 ORM 中使用 ON DELETE CASCADE？[¶](#how-do-i-use-on-delete-cascade-with-sa-s-orm "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------

SQLAlchemy 将始终为当前加载在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中的相关行发布 UPDATE 或 DELETE 语句。对于未加载的行，默认情况下，它会发出 SELECT 语句来加载这些行并将其删除/删除；换句话说，它假定没有配置 ON
DELETE CASCADE。要将 SQLAlchemy 配置为与 ON DELETE
CASCADE 配合使用，请参阅[Using Passive
Deletes](orm_collections.html#passive-deletes)。

我将我的实例的“foo\_id”属性设置为“7”，但“foo”属性仍然是`None` - 它不应该使用 id＃7 加载 Foo 吗？[T2\>](#i-set-the-foo-id-attribute-on-my-instance-to-7-but-the-foo-attribute-is-still-none-shouldn-t-it-have-loaded-foo-with-id-7 "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ORM 的构造方式不是支持从外键属性更改驱动的即时关系群体 -
而是设计为以相反方式工作 -
外键属性由 ORM 在幕后处理，最终用户自然建立对象关系。因此，设置`o.foo`的推荐方法就是这样做 - 设置它！:

    foo = Session.query(Foo).get(7)plainplainplainplain
    o.foo = foo
    Session.commit()

操纵外键属性当然是完全合法的。但是，将外键属性设置为新值目前不会触发它所涉及的[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的“过期”事件。这意味着对于以下顺序：

    o = Session.query(SomeClass).first()plainplainplainplainplainplain
    assert o.foo is None  # accessing an un-set attribute sets it to None
    o.foo_id = 7

`o.foo` is initialized to `None`
when we first accessed it. 设置`o.foo_id = 7`的值为“7” - 所以`o.foo`仍然是`None`：

    # attribute is already set to None, has not beenplainplainplainplainplainplainplain
    # reconciled with o.foo_id = 7 yet
    assert o.foo is None

对于基于外键变异的`o.foo`加载通常会在 commit 后自然实现，它们都会刷新新的外键值并过期所有状态：

    Session.commit()  # expires all attributesplainplainplainplainplain

    foo_7 = Session.query(Foo).get(7)

    assert o.foo is foo_7  # o.foo lazyloads on access

更简单的操作是单独使用属性 - 这可以使用[`Session.expire()`](orm_session_api.html#sqlalchemy.orm.session.Session.expire "sqlalchemy.orm.session.Session.expire")对任何[persistent](glossary.html#term-persistent)对象执行：

    o = Session.query(SomeClass).first()plainplainplainplain
    o.foo_id = 7
    Session.expire(o, ['foo'])  # object must be persistent for this

    foo_7 = Session.query(Foo).get(7)

    assert o.foo is foo_7  # o.foo lazyloads on access

请注意，如果对象不是持久对象，而是出现在[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中，则称为[pending](glossary.html#term-pending)。这意味着该对象的行尚未被插入到数据库中。对于这样的对象，在插入行之前设置`foo_id`没有意义。否则还没有行：

    new_obj = SomeClass()plainplainplainplainplainplainplain
    new_obj.foo_id = 7

    Session.add(new_obj)

    # accessing an un-set attribute sets it to None
    assert new_obj.foo is None

    Session.flush()  # emits INSERT

    # expire this because we already set .foo to None
    Session.expire(o, ['foo'])

    assert new_obj.foo is foo_7  # now it loads

非持久对象的属性加载

上面的“等待”行为的一个变体是如果我们在[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")上使用 flag
`load_on_pending`。当这个标志被设置时，懒惰的加载器将在 INSERT 进行之前为`new_obj.foo`发出；这种方法的另一个变体是使用[`Session.enable_relationship_loading()`](orm_session_api.html#sqlalchemy.orm.session.Session.enable_relationship_loading "sqlalchemy.orm.session.Session.enable_relationship_loading")方法，该方法可以将对象“附加”到[`Session`](orm_session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，使得多对一关系根据外键属性加载，而不管对象处于任何特定状态。Both
techniques are **not recommended for general use**; they were added to
suit specific programming scenarios encountered by users which involve
the repurposing of the ORM’s usual object states.

配方[ExpireRelationshipOnFKChange](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/ExpireRelationshipOnFKChange)具有使用 SQLAlchemy 事件的示例，以便将外键属性的设置与多对一关系进行协调。

我如何走遍与给定对象相关的所有对象？[¶](#how-do-i-walk-all-objects-that-are-related-to-a-given-object "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------------

具有与其相关的其他对象的对象将对应于映射器之间设置的[`relationship()`](orm_relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构。这个代码片段会迭代所有的对象，并修正周期：

    from sqlalchemy import inspectplainplainplainplainplain


    def walk(obj):
        deque = [obj]

        seen = set()

        while deque:
            obj = deque.pop(0)
            if obj in seen:
                continue
            else:
                seen.add(obj)
                yield obj
            insp = inspect(obj)
            for relationship in insp.mapper.relationships:
                related = getattr(obj, relationship.key)
                if relationship.uselist:
                    deque.extend(related)
                elif related is not None:
                    deque.append(related)

该功能可以演示如下：

    Base = declarative_base()plainplainplainplainplainplainplainplain


    class A(Base):
        __tablename__ = 'a'
        id = Column(Integer, primary_key=True)
        bs = relationship("B", backref="a")


    class B(Base):
        __tablename__ = 'b'
        id = Column(Integer, primary_key=True)
        a_id = Column(ForeignKey('a.id'))
        c_id = Column(ForeignKey('c.id'))
        c = relationship("C", backref="bs")


    class C(Base):
        __tablename__ = 'c'
        id = Column(Integer, primary_key=True)


    a1 = A(bs=[B(), B(c=C())])


    for obj in walk(a1):
        print(obj)

输出：

    <__main__.A object at 0x10303b190>plainplainplainplainplainplain
    <__main__.B object at 0x103025210>
    <__main__.B object at 0x10303b0d0>
    <__main__.C object at 0x103025490>

有没有一种方法可以在不查询关键字并获取对包含该关键字的行的引用的情况下仅自动生成唯一关键字（或其他类型的对象）？[¶](#is-there-a-way-to-automagically-have-only-unique-keywords-or-other-kinds-of-objects-without-doing-a-query-for-the-keyword-and-getting-a-reference-to-the-row-containing-that-keyword "Permalink to this headline")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

当人们阅读文档中的多对多示例时，他们会遇到这样的事实：如果您创建两次相同的`Keyword`，它将被放入数据库两次。这有点不方便。

这个[UniqueObject](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/UniqueObject)配方是为了解决这个问题而创建的。
