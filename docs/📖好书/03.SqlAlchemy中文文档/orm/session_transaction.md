---
title: session_transaction
date: 2021-02-20 22:41:49
permalink: /pages/916274/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
事务和连接管理[¶](#transactions-and-connection-management "Permalink to this headline")
=======================================================================================

管理交易[¶](#managing-transactions "Permalink to this headline")
----------------------------------------------------------------

可以说新构建的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")处于“开始”状态。在此状态下，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")尚未与任何可能与其关联的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")对象建立任何连接或事务状态。

然后[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")接收请求以操作数据库连接。Typically,
this means it is called upon to execute SQL statements using a
particular [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine"),
which may be via [`Session.query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query"),
[`Session.execute()`](session_api.html#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute"),
or within a flush operation of pending data, which occurs when such
state exists and [`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
or [`Session.flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")
is called.

当收到这些请求时，遇到的每个新[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")都与由[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")维护的正在进行的事务状态相关联。当操作第一个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")时，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以说已经离开“开始”状态并进入“事务性”状态。对于遇到的每个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，都有一个[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")与它关联，它通过[`Engine.contextual_connect()`](core_connections.html#sqlalchemy.engine.Engine.contextual_connect "sqlalchemy.engine.Engine.contextual_connect")方法获取。如果[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")直接与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")相关联（请参阅[Joining
a Session into an External Transaction (such as for test
suites)](#session-external-transaction)这个），它被直接添加到事务状态。

对于每个[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")还维护一个[`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")对象，该对象通过调用[`Connection.begin()`](core_connections.html#sqlalchemy.engine.Connection.begin "sqlalchemy.engine.Connection.begin")在每个[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上，或者如果已经使用标记`twophase=True`建立了[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象，则[`TwoPhaseTransaction`](core_connections.html#sqlalchemy.engine.TwoPhaseTransaction "sqlalchemy.engine.TwoPhaseTransaction")对象通过[`Connection.begin_twophase()`](core_connections.html#sqlalchemy.engine.Connection.begin_twophase "sqlalchemy.engine.Connection.begin_twophase")获取。这些事务全部被提交或回滚，对应于[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")和[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")方法的调用。如果适用，提交操作还会对所有事务调用[`TwoPhaseTransaction.prepare()`](core_connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare "sqlalchemy.engine.TwoPhaseTransaction.prepare")方法。

When the transactional state is completed after a rollback or commit,
the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
[releases](glossary.html#term-releases) all [`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")
and [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
resources, and goes back to the “begin” state, which will again invoke
new [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
and [`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")
objects as new requests to emit SQL statements are received.

下面的例子说明了这个生命周期：

    engine = create_engine("...")
    Session = sessionmaker(bind=engine)

    # new session.   no connections are in use.
    session = Session()
    try:
        # first query.  a Connection is acquired
        # from the Engine, and a Transaction
        # started.
        item1 = session.query(Item).get(1)

        # second query.  the same Connection/Transaction
        # are used.
        item2 = session.query(Item).get(2)

        # pending changes are created.
        item1.foo = 'bar'
        item2.bar = 'foo'

        # commit.  The pending changes above
        # are flushed via flush(), the Transaction
        # is committed, the Connection object closed
        # and discarded, the underlying DBAPI connection
        # returned to the connection pool.
        session.commit()
    except:
        # on rollback, the same closure of state
        # as that of commit proceeds.
        session.rollback()
        raise

### 使用SAVEPOINT [¶](#using-savepoint "Permalink to this headline")

如果底层引擎支持SAVEPOINT事务，可以使用[`begin_nested()`{.xref .py
.py-meth .docutils
.literal}](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")方法描述：

    Session = sessionmaker()
    session = Session()
    session.add(u1)
    session.add(u2)

    session.begin_nested() # establish a savepoint
    session.add(u3)
    session.rollback()  # rolls back u3, keeps u1 and u2

    session.commit() # commits u1 and u2

[`begin_nested()`](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")
may be called any number of times, which will issue a new SAVEPOINT with
a unique identifier for each call. 对于每个[`begin_nested()`{.xref .py
.py-meth .docutils
.literal}](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")调用，必须发出相应的[`rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")或[`commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")。（但是请注意，如果返回值用作上下文管理器，即在with-statement中，则此退回/提交由上下文管理器在退出上下文时发出，因此不应显式添加。）

当调用[`begin_nested()`](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")时，将无条件发布[`flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")（不管`autoflush`设置如何）。这是为了当发生[`rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")时，会话的完整状态已过期，从而导致所有后续的属性/实例访问都引用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的完整状态在[`begin_nested()`](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")之前被调用。

[`begin_nested()`](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested"),
in the same manner as the less often used [`begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")
method, returns a transactional object which also works as a context
manager. 它可以简洁地用于单个记录插入，以便捕获唯一约束例外等情况：

    for record in records:
        try:
            with session.begin_nested():
                session.merge(record)
        except:
            print("Skipped record %s" % record)
    session.commit()

### 自动提交模式[¶](#autocommit-mode "Permalink to this headline")

The example of [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
transaction lifecycle illustrated at the start of [Managing
Transactions](#unitofwork-transaction) applies to a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
configured in the default mode of `autocommit=False`. Constructing a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
with `autocommit=True` produces a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
placed into “autocommit” mode, where each SQL statement invoked by a
[`Session.query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")
or [`Session.execute()`](session_api.html#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
occurs using a new connection from the connection pool, discarding it
after results have been iterated. [`Session.flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")操作仍然发生在单个事务的范围内，尽管此事务在[`Session.flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")操作完成后关闭。

警告

“autocommit” mode should **not be considered for general use**.
如果使用，它应该总是与[`Session.begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")和[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")的用法相结合，以确保事务划分。

在划定的事务之外执行查询是传统的使用模式，并且在某些情况下可能会导致并发连接检出。

在没有划分的事务时，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")无法就自动屏蔽何时发生以及何时应该发生自动过期做出适当的决定，因此应使用`autoflush =假， expire_on_commit =假`。

“自动提交”的现代用法适用于需要在“开始”状态发生时专门控制的框架集成。可以使用[`Session.begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法将`autocommit=True`配置的会话置于“开始”状态。After the cycle completes upon
[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
or [`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback"),
connection and transaction resources are
[released](glossary.html#term-released) and the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
goes back into “autocommit” mode, until [`Session.begin()`{.xref .py
.py-meth .docutils
.literal}](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")
is called again:

    Session = sessionmaker(bind=engine, autocommit=True)
    session = Session()
    session.begin()
    try:
        item1 = session.query(Item).get(1)
        item2 = session.query(Item).get(2)
        item1.foo = 'bar'
        item2.bar = 'foo'
        session.commit()
    except:
        session.rollback()
        raise

[`Session.begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法还返回一个事务标记，该标记与Python
2.6 `with`语句兼容：

    Session = sessionmaker(bind=engine, autocommit=True)
    session = Session()
    with session.begin():
        item1 = session.query(Item).get(1)
        item2 = session.query(Item).get(2)
        item1.foo = 'bar'
        item2.bar = 'foo'

#### 对自动提交使用Subtransactions [¶](#using-subtransactions-with-autocommit "Permalink to this headline")

子事务表示[`Session.begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法与`subtransactions=True`标志的结合使用。这产生了一个非事务性的分隔结构，允许将调用嵌套到[`begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")和[`commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")。它的目的是允许构建可以在事务内运行的代码，而不依赖于任何启动事务的外部代码，以及在已经划定事务的块内。

`subtransactions=True` is generally only useful in
conjunction with autocommit, and is equivalent to the pattern described
at [Nesting of Transaction
Blocks](core_connections.html#connections-nested-transactions), where
any number of functions can call [`Connection.begin()`{.xref .py
.py-meth .docutils
.literal}](core_connections.html#sqlalchemy.engine.Connection.begin "sqlalchemy.engine.Connection.begin")
and [`Transaction.commit()`](core_connections.html#sqlalchemy.engine.Transaction.commit "sqlalchemy.engine.Transaction.commit")
as though they are the initiator of the transaction, but in fact may be
participating in an already ongoing transaction:

    # method_a starts a transaction and calls method_b
    def method_a(session):
        session.begin(subtransactions=True)
        try:
            method_b(session)
            session.commit()  # transaction is committed here
        except:
            session.rollback() # rolls back the transaction
            raise

    # method_b also starts a transaction, but when
    # called from method_a participates in the ongoing
    # transaction.
    def method_b(session):
        session.begin(subtransactions=True)
        try:
            session.add(SomeObject('bat', 'lala'))
            session.commit()  # transaction is not committed yet
        except:
            session.rollback() # rolls back the transaction, in this case
                               # the one that was initiated in method_a().
            raise

    # create a Session and call method_a
    session = Session(autocommit=True)
    method_a(session)
    session.close()

子进程使用[`Session.flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")进程来确保刷新操作发生在事务中，而不管自动提交。当自动提交被禁用时，它仍然有用，因为它强制[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")进入“挂起回滚”状态，因为失败的刷新无法在操作中恢复，最终用户仍然维持“整个交易的范围“。

### 启用两阶段提交[¶](#enabling-two-phase-commit "Permalink to this headline")

对于支持两阶段操作的后端（当前MySQL和PostgreSQL），可以指示会话使用两阶段提交语义。这将协调跨数据库的事务提交，以便在所有数据库中提交或回滚事务。您还可以[`prepare()`](session_api.html#sqlalchemy.orm.session.Session.prepare "sqlalchemy.orm.session.Session.prepare")会话以与未由SQLAlchemy管理的交易进行交互。要使用两阶段事务，请在会话中设置标志`twophase=True`：

    engine1 = create_engine('postgresql://db1')
    engine2 = create_engine('postgresql://db2')

    Session = sessionmaker(twophase=True)

    # bind User operations to engine 1, Account operations to engine 2
    Session.configure(binds={User:engine1, Account:engine2})

    session = Session()

    # .... work with accounts and users

    # commit.  session will issue a flush to all DBs, and a prepare step to all DBs,
    # before committing both transactions
    session.commit()

### 设置事务隔离级别[¶](#setting-transaction-isolation-levels "Permalink to this headline")

[Isolation](glossary.html#term-isolation) refers to the behavior of the
transaction at the database level in relation to other transactions
occurring concurrently. 有四种众所周知的隔离模式，通常Python
DBAPI允许通过明确的API或通过特定于数据库的调用来基于每个连接来设置这些模式。

SQLAlchemy的方言在每个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或per
[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")基础上支持可设置的隔离模式，在[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")在[`Connection.execution_options()`](core_connections.html#sqlalchemy.engine.Connection.execution_options "sqlalchemy.engine.Connection.execution_options")级别。

当使用ORM [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，它充当引擎和连接的*外观*，但不直接暴露事务隔离。因此，为了影响事务隔离级别，我们需要根据情况对[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")执行操作。

也可以看看

[`create_engine.isolation_level`](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")

[SQLite Transaction
Isolation](dialects_sqlite.html#sqlite-isolation-level)

[Postgresql Isolation
Level](dialects_postgresql.html#postgresql-isolation-level)

[MySQL Isolation Level](dialects_mysql.html#mysql-isolation-level)

#### 设置隔离引擎范围[¶](#setting-isolation-engine-wide "Permalink to this headline")

要在全局范围内设置具有特定隔离级别的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")或[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")，请使用[`create_engine.isolation_level`{.xref
.py .py-paramref .docutils
.literal}](core_engines.html#sqlalchemy.create_engine.params.isolation_level "sqlalchemy.create_engine")参数：

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    eng = create_engine(
        "postgresql://scott:tiger@localhost/test",
        isolation_level='REPEATABLE_READ')

    maker = sessionmaker(bind=eng)

    session = maker()

#### 为单个会话设置隔离[¶](#setting-isolation-for-individual-sessions "Permalink to this headline")

当我们创建一个新的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，无论是直接使用构造函数，还是当我们调用[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")生成的可调用对象时，我们都可以通过`bind`直接参数，覆盖已有的绑定。我们可以将其与[`Engine.execution_options()`](core_connections.html#sqlalchemy.engine.Engine.execution_options "sqlalchemy.engine.Engine.execution_options")方法结合使用，以生成原始[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")的副本，以添加此选项：

    session = maker(
        bind=engine.execution_options(isolation_level='SERIALIZABLE'))

对于[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")或[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")配置了多个“绑定”的情况，我们可以完全重新指定`binds`参数，或者if我们只想替换特定的绑定，我们可以使用[`Session.bind_mapper()`](session_api.html#sqlalchemy.orm.session.Session.bind_mapper "sqlalchemy.orm.session.Session.bind_mapper")或[`Session.bind_table()`](session_api.html#sqlalchemy.orm.session.Session.bind_table "sqlalchemy.orm.session.Session.bind_table")方法：

    session = maker()
    session.bind_mapper(
        User, user_engine.execution_options(isolation_level='SERIALIZABLE'))

我们也可以使用下面的单个交易方法。

#### 设置单个事务的隔离[¶](#setting-isolation-for-individual-transactions "Permalink to this headline")

关于隔离级别的一个关键警告是该设置无法在事务已经开始的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")上安全地修改。数据库无法更改正在进行的事务的隔离级别，并且某些DBAPI和SQLAlchemy方言在此区域中具有不一致的行为。有些可能会隐式地发出ROLLBACK，有些可能隐式地发出COMMIT，有些可能会在下一个事务之前忽略该设置。因此，如果在事务已经在使用时设置此选项，则SQLAlchemy会发出警告。[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象不为我们提供用于事务尚未开始的事务中的[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")。So
here, we need to pass execution options to the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
at the start of a transaction by passing
[`Session.connection.execution_options`](session_api.html#sqlalchemy.orm.session.Session.connection.params.execution_options "sqlalchemy.orm.session.Session.connection")
provided by the [`Session.connection()`](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")
method:

    from sqlalchemy.orm import Session

    sess = Session(bind=engine)
    sess.connection(execution_options={'isolation_level': 'SERIALIZABLE'})

    # work with session

    # commit transaction.  the connection is released
    # and reverted to its previous isolation level.
    sess.commit()

以上，我们首先使用构造函数或[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")生成[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。然后我们通过调用[`Session.connection()`](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")明确地设置一个事务的开始，它提供了在事务开始之前传递给连接的执行选项。If
we are working with a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
that has multiple binds or some other custom scheme for
[`Session.get_bind()`](session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind"),
we can pass additional arguments to [`Session.connection()`{.xref .py
.py-meth .docutils
.literal}](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")
in order to affect how the bind is procured:

    sess = my_sesssionmaker()

    # set up a transaction for the bind associated with
    # the User mapper
    sess.connection(
        mapper=User,
        execution_options={'isolation_level': 'SERIALIZABLE'})

    # work with session

    # commit transaction.  the connection is released
    # and reverted to its previous isolation level.
    sess.commit()

[`Session.connection.execution_options`](session_api.html#sqlalchemy.orm.session.Session.connection.params.execution_options "sqlalchemy.orm.session.Session.connection")参数仅在针对事务中特定绑定的**第一次**调用[`Session.connection()`](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")时才被接受。如果事务已经在目标连接上开始，则会发出警告：

    >>> session = Session(eng)
    >>> session.execute("select 1")
    <sqlalchemy.engine.result.ResultProxy object at 0x1017a6c50>
    >>> session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
    sqlalchemy/orm_session.py:310: SAWarning: Connection is already established
    for the given bind; execution_options ignored

版本0.9.9新增：将[`Session.connection.execution_options`{.xref .py
.py-paramref .docutils
.literal}](session_api.html#sqlalchemy.orm.session.Session.connection.params.execution_options "sqlalchemy.orm.session.Session.connection")参数添加到[`Session.connection()`](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")。

### 使用事件跟踪事务状态[¶](#tracking-transaction-state-with-events "Permalink to this headline")

有关会话事务状态更改的可用事件挂钩的概述，请参阅[Transaction
Events](session_events.html#session-transaction-events)部分。

将会话加入外部事务（例如测试套件）[¶](#joining-a-session-into-an-external-transaction-such-as-for-test-suites "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------------------------

If a [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")
is being used which is already in a transactional state (i.e. has a
[`Transaction`](core_connections.html#sqlalchemy.engine.Transaction "sqlalchemy.engine.Transaction")
established), a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
can be made to participate within that transaction by just binding the
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
to that [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection").
通常的基本原理是测试套件允许ORM代码使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")自由运行，包括调用[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")的能力，其中整个数据库交互被回滚：

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from unittest import TestCase

    # global application scope.  create Session class, engine
    Session = sessionmaker()

    engine = create_engine('postgresql://...')

    class SomeTest(TestCase):
        def setUp(self):
            # connect to the database
            self.connection = engine.connect()

            # begin a non-ORM transaction
            self.trans = self.connection.begin()

            # bind an individual Session to the connection
            self.session = Session(bind=self.connection)

        def test_something(self):
            # use the session in tests.

            self.session.add(Foo())
            self.session.commit()

        def tearDown(self):
            self.session.close()

            # rollback - everything that happened with the
            # Session above (including calls to commit())
            # is rolled back.
            self.trans.rollback()

            # return connection to the Engine
            self.connection.close()

在上面，我们发布了[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")以及[`Transaction.rollback()`](core_connections.html#sqlalchemy.engine.Transaction.rollback "sqlalchemy.engine.Transaction.rollback")。这是一个例子，我们可以利用[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")对象维护*subtransactions*的能力，或嵌套的begin
/ commit-or-rollback对，其中只有最外面的begin /
commit对实际上提交事务，或者如果最外面的块回滚，则所有内容都回滚。

支持回滚测试

除了需要在测试本身范围内实际调用[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")的测试外，上述配方适用于任何类型的数据库启用测试。上面的配方可以扩展，使得[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")总是运行在每个事务开始时建立的SAVEPOINT范围内的所有操作，以便测试还可以将“事务”回滚为同时仍然保留在从未犯下的较大“交易”的范围内，并使用两个额外事件：

    from sqlalchemy import event


    class SomeTest(TestCase):

        def setUp(self):
            # connect to the database
            self.connection = engine.connect()

            # begin a non-ORM transaction
            self.trans = connection.begin()

            # bind an individual Session to the connection
            self.session = Session(bind=self.connection)

            # start the session in a SAVEPOINT...
            self.session.begin_nested()

            # then each time that SAVEPOINT ends, reopen it
            @event.listens_for(self.session, "after_transaction_end")
            def restart_savepoint(session, transaction):
                if transaction.nested and not transaction._parent.nested:

                    # ensure that state is expired the way
                    # session.commit() at the top level normally does
                    # (optional step)
                    session.expire_all()

                    session.begin_nested()

        # ... the tearDown() method stays the same
