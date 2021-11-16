---
title: 性能
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/faq/performance/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - faq
tags:
---
性能[¶ T0\>](#performance "Permalink to this headline")
=======================================================

-   [我如何分析 SQLAlchemy 驱动的应用程序？](#how-can-i-profile-a-sqlalchemy-powered-application)
    -   [查询分析](#query-profiling)
    -   [代码分析](#code-profiling)
    -   [执行缓慢](#execution-slowness)
    -   [结果获取缓慢 - 核心](#result-fetching-slowness-core)
    -   [结果获取缓慢 - ORM](#result-fetching-slowness-orm)
-   [我使用 ORM 插入了 400,000 行，它非常慢！](#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow)

我如何分析 SQLAlchemy 驱动的应用程序？[¶](#how-can-i-profile-a-sqlalchemy-powered-application "Permalink to this headline")
-------------------------------------------------------------------------------------------------------------------------

寻找性能问题通常涉及两个策略。一个是查询分析，另一个是代码分析。

### 查询分析[¶](#query-profiling "Permalink to this headline")

有时，只需简单的 SQL 日志记录（通过 python 的日志记录模块启用，或者通过[`create_engine()`](core_engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")中的`echo=True`参数）就可以了解事情要花多长时间。例如，如果你在 SQL 操作之后记录一些东西，你会在日志中看到类似这样的东西：

    17:37:48,325 INFO  [sqlalchemy.engine.base.Engine.0x...048c] SELECT ...
    17:37:48,326 INFO  [sqlalchemy.engine.base.Engine.0x...048c] {<params>}
    17:37:48,660 DEBUG [myapp.somemessage]

如果您在操作之后立即记录了`myapp.somemessage`，则知道完成 SQL 部分的操作需要 334ms。

记录 SQL 还会说明是否有数十个/数百个查询正在发布，这可能会更好地组织成更少的查询。When
using the SQLAlchemy ORM, the “eager loading” feature is provided to
partially ([`contains_eager()`](orm_loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager"))
or fully ([`joinedload()`](orm_loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload"),
[`subqueryload()`](orm_loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload"))
automate this activity, but without the ORM “eager loading” typically
means to use joins so that results across multiple tables can be loaded
in one result set instead of multiplying numbers of queries as more
depth is added (i.e. `r + r*r2 + r*r2*r3` ...)

要进行更长期的查询分析或实现应用程序端“慢速查询”监视器，可以使用以下配方来使用事件来拦截游标执行：

    from sqlalchemy import eventplain
    from sqlalchemy.engine import Engine
    import time
    import logging

    logging.basicConfig()
    logger = logging.getLogger("myapp.sqltime")
    logger.setLevel(logging.DEBUG)

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement,
                            parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
        logger.debug("Start Query: %s", statement)

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement,
                            parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f", total)

以上，我们使用[`ConnectionEvents.before_cursor_execute()`](core_events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute "sqlalchemy.events.ConnectionEvents.before_cursor_execute")和[`ConnectionEvents.after_cursor_execute()`](core_events.html#sqlalchemy.events.ConnectionEvents.after_cursor_execute "sqlalchemy.events.ConnectionEvents.after_cursor_execute")事件来建立执行语句时的拦截点。我们使用`_ConnectionRecord.info`字典将一个计时器附加到连接上；我们在这里使用一个堆栈来处理游标执行事件可能被嵌套的偶然情况。

### 代码分析[¶](#code-profiling "Permalink to this headline")

如果日志记录显示单个查询花费的时间太长，则需要详细分析处理查询的数据库花了多少时间，通过网络发送结果，由[DBAPI](glossary.html#term-dbapi)处理，以及最后被 SQLAlchemy 的结果集和/或 ORM 层接收。根据具体情况，这些阶段中的每一个都可能会出现各自的瓶颈。

为此，您需要使用[Python 分析模块](https://docs.python.org/2/library/profile.html)。下面是一个简单的配方，用于分析上下文管理器：

    import cProfileplain
    import StringIO
    import pstats
    import contextlib

    @contextlib.contextmanager
    def profiled():
        pr = cProfile.Profile()
        pr.enable()
        yield
        pr.disable()
        s = StringIO.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        # uncomment this to see who's calling what
        # ps.print_callers()
        print(s.getvalue())

要剖析一段代码：

    with profiled():
        Session.query(FooClass).filter(FooClass.somevalue==8).all()

分析的输出结果可用于了解花费时间的想法。剖析输出的一部分如下所示：

    13726 function calls (13042 primitive calls) in 0.014 secondsplain

    Ordered by: cumulative time

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    222/21    0.001    0.000    0.011    0.001 lib/sqlalchemy/faq/orm_loading.py:26(instances)
    220/20    0.002    0.000    0.010    0.001 lib/sqlalchemy/faq/orm_loading.py:327(_instance)
    220/20    0.000    0.000    0.010    0.000 lib/sqlalchemy/faq/orm_loading.py:284(populate_state)
       20    0.000    0.000    0.010    0.000 lib/sqlalchemy/faq/orm_strategies.py:987(load_collection_from_subq)
       20    0.000    0.000    0.009    0.000 lib/sqlalchemy/faq/orm_strategies.py:935(get)
        1    0.000    0.000    0.009    0.009 lib/sqlalchemy/faq/orm_strategies.py:940(_load)
       21    0.000    0.000    0.008    0.000 lib/sqlalchemy/faq/orm_strategies.py:942(<genexpr>)
        2    0.000    0.000    0.004    0.002 lib/sqlalchemy/faq/orm_query.py:2400(__iter__)
        2    0.000    0.000    0.002    0.001 lib/sqlalchemy/faq/orm_query.py:2414(_execute_and_instances)
        2    0.000    0.000    0.002    0.001 lib/sqlalchemy/faq/engine/base.py:659(execute)
        2    0.000    0.000    0.002    0.001 lib/sqlalchemy/faq/sql/elements.py:321(_execute_on_connection)
        2    0.000    0.000    0.002    0.001 lib/sqlalchemy/faq/engine/base.py:788(_execute_clauseelement)

    ...

在上面，我们可以看到`instances()`
SQLAlchemy 函数被调用了 222 次（递归的，从外部的 21 次），总共调用了总共 0.011 秒。

### 执行缓慢[¶](#execution-slowness "Permalink to this headline")

这些电话的具体细节可以告诉我们时间花在哪里。例如，如果您看到时间在`cursor.execute()`之内，例如针对 DBAPI：

    2    0.102    0.102    0.204    0.102 {method 'execute' of 'sqlite3.Cursor' objects}

这将表明数据库需要很长时间才能开始返回结果，这意味着您的查询应该进行优化，可以通过添加索引或重新构建查询和/或基础模式来实现。对于该任务，使用诸如 EXPLAIN，SHOW
PLAN 等的系统来分析查询计划是有保证的。如由数据库后端提供的那样。

### 结果获取缓慢 - 核心[¶](#result-fetching-slowness-core "Permalink to this headline")

另一方面，如果您看到涉及到获取行的数千次调用或对`fetchall()`的非常长的调用，这可能意味着您的查询正在返回比预期更多的行，或者提取行本身很慢。The
ORM itself typically uses `fetchall()` to fetch rows
(or `fetchmany()` if the [`Query.yield_per()`](orm_query.html#sqlalchemy.orm.query.Query.yield_per "sqlalchemy.orm.query.Query.yield_per")
option is used).

在 DBAPI 级别，通过对`fetchall()`进行非常缓慢的调用可以指示过多的行数：

    2    0.300    0.600    0.300    0.600 {method 'fetchall' of 'sqlite3.Cursor' objects}plain

即使最终结果似乎没有多行，意外的大量行也可能是笛卡尔积的结果 -
当多组行合并在一起而没有适当地将表连接在一起时。如果在复杂的查询中使用了错误的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，并引入其他意外的 FROM 子句，那么使用 SQLAlchemy
Core 或 ORM 查询生成此行为通常很容易。

另一方面，在 DBAPI 级别对`fetchall()`执行快速调用，但是当 SQLAlchemy 的[`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")被要求执行`fetchall()`

    # the DBAPI cursor is fast...plain
    2    0.020    0.040    0.020    0.040 {method 'fetchall' of 'sqlite3.Cursor' objects}

    ...

    # but SQLAlchemy's result proxy is slow, this is type-level processing
    2    0.100    0.200    0.100    0.200 lib/sqlalchemy/faq/engine/result.py:778(fetchall)

在某些情况下，后端可能正在进行不需要的类型级处理。更具体地说，在类型 API 中查看缓慢的调用是更好的指标
- 下面是我们使用类似这样的类型时的样子：

    from sqlalchemy import TypeDecorator
    import time

    class Foo(TypeDecorator):
        impl = String

        def process_result_value(self, value, thing):
            # intentionally add slowness for illustration purposes
            time.sleep(.001)
            return value

这种故意缓慢操作的分析输出可以看作是这样的：

    200    0.001    0.000    0.237    0.001 lib/sqlalchemy/faq/sql/type_api.py:911(process)
    200    0.001    0.000    0.236    0.001 test.py:28(process_result_value)
    200    0.235    0.001    0.235    0.001 {time.sleep}

也就是说，我们在`type_api`系统中看到许多昂贵的调用，实际耗时的事情是`time.sleep()`调用。

请务必检查`Dialect 文档`，以获取有关此级别已知性能调整建议的说明，特别是对于像 Oracle 这样的数据库。可能存在与确保数字准确性或字符串处理相关的系统，这些系统在所有情况下可能都不需要。

排队性能受到影响的可能还有更多的低级别点，例如，如果花费的时间似乎集中在像`socket.receive()`这样的调用上，这可能表明除了实际的网络连接，所有事情都很快，并且数据移动花费的时间太多网络。

### 结果获取缓慢 - ORM [¶](#result-fetching-slowness-orm "Permalink to this headline")

为了检测行的 ORM 读取缓慢（这是性能关注的最常见区域），诸如`populate_state()`和`_instance()`的调用将说明单个 ORM 对象群体：

    # the ORM calls _instance for each ORM-loaded row it sees, and
    # populate_state for each ORM-loaded row that results in the population
    # of an object's attributes
    220/20    0.001    0.000    0.010    0.000 lib/sqlalchemy/faq/orm_loading.py:327(_instance)
    220/20    0.000    0.000    0.009    0.000 lib/sqlalchemy/faq/orm_loading.py:284(populate_state)

ORM 将行转换为 ORM 映射对象的速度慢是该操作复杂性与 cPython 开销相结合的产物。减轻这种情况的共同策略包括：

-   获取单个列而不是完整实体，即：

        session.query(User.id, User.name)plain

    代替：

        session.query(User)

-   使用[`Bundle`](orm_query.html#sqlalchemy.orm.query.Bundle "sqlalchemy.orm.query.Bundle")对象来组织基于列的结果：

        u_b = Bundle('user', User.id, User.name)plain
        a_b = Bundle('address', Address.id, Address.email)

        for user, address in session.query(u_b, a_b).join(User.addresses):
            # ...

-   使用结果缓存 - 请参阅[Dogpile
    Caching](orm_examples.html#examples-caching)以获得深入的示例。

-   考虑一下像 Pypy 那样更快的翻译。

配置文件的输出可能有点令人生畏，但经过一些练习后，它们很容易阅读。

也可以看看

[Performance](orm_examples.html#examples-performance) - a suite of
performance demonstrations with bundled profiling capabilities.

我使用 ORM 插入了 400,000 行，它非常慢！[¶](#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------------

在同步对数据库的更改时，SQLAlchemy ORM 使用[unit of
work](glossary.html#term-unit-of-work)模式。这种模式远远超出了简单的“插入”数据。它包括使用属性检测系统接收在对象上分配的属性，该属性检测系统在对象创建时跟踪对象上的更改，包括插入的所有行都在标识映射中进行跟踪，这对于每行 SQLAlchemy 都必须检索其“最后插入的 ID“（如果还没有给出），并且还涉及要插入的行将被扫描并根据需要对其进行排序以获得相关性。对象还需要有相当程度的簿记才能保持所有这些运行，对于大量的行来说，一次可以在大型数据结构上花费过多的时间，因此最好将它们分块。

基本上，工作单元具有很大的自动化程度，可以自动执行将复杂对象图持久化到没有明确持久性代码的关系数据库中的任务，而且这种自动化具有代价。

ORM 基本上不适用于高性能批量插入 -
这是 SQLAlchemy 除了将 ORM 作为第一级组件提供 Core 之外的全部原因。

对于快速批量插入的用例，ORM 构建在其上的 SQL 生成和执行系统是`Core`的一部分。直接使用此系统，我们可以生成一个与直接使用原始数据库 API 相竞争的 INSERT。

或者，SQLAlchemy ORM 提供了[Bulk
Operations](orm_persistence_techniques.html#bulk-operations)方法套件，这些方法提供了工作单元过程的子部分的挂钩，以便发布具有小程度的基于 ORM 的核心级 INSERT 和 UPDATE 结构自动化。

下面的例子说明了插入行的几种不同方法的基于时间的测试，从最自动化到最小化。使用 cPython
2.7，运行时观察到：

    classics-MacBook-Pro:sqlalchemy classic$ python test.py
    SQLAlchemy ORM: Total time for 100000 records 12.0471920967 secs
    SQLAlchemy ORM pk given: Total time for 100000 records 7.06283402443 secs
    SQLAlchemy ORM bulk_save_objects(): Total time for 100000 records 0.856323003769 secs
    SQLAlchemy Core: Total time for 100000 records 0.485800027847 secs
    sqlite3: Total time for 100000 records 0.487842082977 sec

我们可以使用[Pypy](http://pypy.org/)的最新版本将时间缩短三分之一：

    classics-MacBook-Pro:sqlalchemy classic$ /usr/local/src/pypy-2.1-beta2-osx64/bin/pypy test.pyplain
    SQLAlchemy ORM: Total time for 100000 records 5.88369488716 secs
    SQLAlchemy ORM pk given: Total time for 100000 records 3.52294301987 secs
    SQLAlchemy Core: Total time for 100000 records 0.613556146622 secs
    sqlite3: Total time for 100000 records 0.442467927933 sec

脚本：

    import time
    import sqlite3

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String,  create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    Base = declarative_base()
    DBSession = scoped_session(sessionmaker())
    engine = None


    class Customer(Base):
        __tablename__ = "customer"
        id = Column(Integer, primary_key=True)
        name = Column(String(255))


    def init_sqlalchemy(dbname='sqlite:///sqlalchemy.db'):
        global engine
        engine = create_engine(dbname, echo=False)
        DBSession.remove()
        DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


    def test_sqlalchemy_orm(n=100000):
        init_sqlalchemy()
        t0 = time.time()
        for i in xrange(n):
            customer = Customer()
            customer.name = 'NAME ' + str(i)
            DBSession.add(customer)
            if i % 1000 == 0:
                DBSession.flush()
        DBSession.commit()
        print(
            "SQLAlchemy ORM: Total time for " + str(n) +
            " records " + str(time.time() - t0) + " secs")


    def test_sqlalchemy_orm_pk_given(n=100000):
        init_sqlalchemy()
        t0 = time.time()
        for i in xrange(n):
            customer = Customer(id=i+1, name="NAME " + str(i))
            DBSession.add(customer)
            if i % 1000 == 0:
                DBSession.flush()
        DBSession.commit()
        print(
            "SQLAlchemy ORM pk given: Total time for " + str(n) +
            " records " + str(time.time() - t0) + " secs")


    def test_sqlalchemy_orm_bulk_insert(n=100000):
        init_sqlalchemy()
        t0 = time.time()
        n1 = n
        while n1 > 0:
            n1 = n1 - 10000
            DBSession.bulk_insert_mappings(
                Customer,
                [
                    dict(name="NAME " + str(i))
                    for i in xrange(min(10000, n1))
                ]
            )
        DBSession.commit()
        print(
            "SQLAlchemy ORM bulk_save_objects(): Total time for " + str(n) +
            " records " + str(time.time() - t0) + " secs")


    def test_sqlalchemy_core(n=100000):
        init_sqlalchemy()
        t0 = time.time()
        engine.execute(
            Customer.__table__.insert(),
            [{"name": 'NAME ' + str(i)} for i in xrange(n)]
        )
        print(
            "SQLAlchemy Core: Total time for " + str(n) +
            " records " + str(time.time() - t0) + " secs")


    def init_sqlite3(dbname):
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS customer")
        c.execute(
            "CREATE TABLE customer (id INTEGER NOT NULL, "
            "name VARCHAR(255), PRIMARY KEY(id))")
        conn.commit()
        return conn


    def test_sqlite3(n=100000, dbname='sqlite3.db'):
        conn = init_sqlite3(dbname)
        c = conn.cursor()
        t0 = time.time()
        for i in xrange(n):
            row = ('NAME ' + str(i),)
            c.execute("INSERT INTO customer (name) VALUES (?)", row)
        conn.commit()
        print(
            "sqlite3: Total time for " + str(n) +
            " records " + str(time.time() - t0) + " sec")

    if __name__ == '__main__':
        test_sqlalchemy_orm(100000)
        test_sqlalchemy_orm_pk_given(100000)
        test_sqlalchemy_orm_bulk_insert(100000)
        test_sqlalchemy_core(100000)
        test_sqlite3(100000)
