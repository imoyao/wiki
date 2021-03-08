---
title: 会话基础
date: 2021-02-20 22:41:47
permalink: /sqlalchemy/orm/session_basics/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
会话基础[¶](#session-basics "Permalink to this headline")
=========================================================

会话是做什么的？[¶](#what-does-the-session-do "Permalink to this headline")
---------------------------------------------------------------------------

从一般意义上说，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")建立与数据库的所有对话，并代表您在其生命周期中加载或关联的所有对象的“保留区”。It
provides the entrypoint to acquire a [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
object, which sends queries to the database using the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
object’s current database connection, populating result rows into
objects that are then stored in the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
inside a structure called the [Identity
Map](http://martinfowler.com/eaaCatalog/identityMap.html) - a data
structure that maintains unique copies of each object, where “unique”
means “only one object with a particular primary key”.

[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")以基本无状态的形式开始。一旦查询被发布或其他对象被持久化，它就会从[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")请求连接资源，该连接资源与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本身或映射的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")正在操作的对象。这个连接代表一个正在进行的事务，它在指示[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")提交或回滚其挂起状态之前一直有效。

All changes to objects maintained by a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
are tracked - before the database is queried again or before the current
transaction is committed, it **flushes** all pending changes to the
database.
这被称为[工作单元](http://martinfowler.com/eaaCatalog/unitOfWork.html)模式。

当使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，重要的是要注意与它关联的对象是由[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")保存的事务的**代理对象**有很多事件会导致对象重新访问数据库以保持同步。可以从[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")中“分离”对象，并继续使用它们，虽然这种做法有其警告。通常情况下，当您想再次使用它们时，您会将分离的对象与另一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")重新关联，以便它们可以恢复表示数据库状态的常规任务。

获得会话[¶](#getting-a-session "Permalink to this headline")
------------------------------------------------------------

[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
is a regular Python class which can be directly instantiated.
但是，为了标准化会话配置和获取方式，[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")类通常用于创建顶级[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")配置，然后可以在整个应用程序中使用，而不需要重复配置参数。

[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")的用法如下所示：

    from sqlalchemy import create_engineplainplain
    from sqlalchemy.orm import sessionmaker

    # an Engine, which the Session will use for connection
    # resources
    some_engine = create_engine('postgresql://scott:tiger@localhost/')

    # create a configured "Session" class
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()

    # work with sess
    myobject = MyObject('foo', 'bar')
    session.add(myobject)
    session.commit()

以上，[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")调用为我们创建了一个工厂，我们将其分配给名为`Session`的名称。这个工厂被调用时，将使用我们给出的配置参数创建一个新的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象。在这种情况下，通常情况下，我们已经配置工厂为连接资源指定特定的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")。

A typical setup will associate the [`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")
with an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine"),
so that each [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
generated will use this [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
to acquire connection resources. 可以使用`bind`参数设置该关联，如上例所示。

在编写应用程序时，将[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")工厂放在全局级别。这个工厂可以被其余的应用程序用作新的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")实例的源，保持[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象在一个地方被构建的配置。

[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")工厂也可以与其他助手一起使用，这些助手将传递用户定义的[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")，然后由助手维护。其中一些帮助程序在[When
do I construct a Session, when do I commit it, and when do I close
it?](#session-faq-whentocreate)。

### 将其他配置添加到现有的 sessionmaker()[¶](#adding-additional-configuration-to-an-existing-sessionmaker "Permalink to this headline")

一个常见的场景是在模块导入时调用[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")，但是要生成一个或多个与[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")关联的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")尚未进行。对于这个用例，[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")结构提供了[`sessionmaker.configure()`](session_api.html#sqlalchemy.orm.session.sessionmaker.configure "sqlalchemy.orm.session.sessionmaker.configure")方法，该方法将其他配置指令放入现有的[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")当构造被调用时发生：

    from sqlalchemy.orm import sessionmakerplainplain
    from sqlalchemy import create_engine

    # configure Session class with desired options
    Session = sessionmaker()

    # later, we create the engine
    engine = create_engine('postgresql://...')

    # associate it with our custom Session class
    Session.configure(bind=engine)

    # work with the session
    session = Session()

### 用替代参数创建特别会话对象[¶](#creating-ad-hoc-session-objects-with-alternate-arguments "Permalink to this headline")

For the use case where an application needs to create a new
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
with special arguments that deviate from what is normally used
throughout the application, such as a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
that binds to an alternate source of connectivity, or a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
that should have other arguments such as `expire_on_commit` established differently from what most of the application
wants, specific arguments can be passed to the [`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")
factory’s [`sessionmaker.__call__()`](session_api.html#sqlalchemy.orm.session.sessionmaker.__call__ "sqlalchemy.orm.session.sessionmaker.__call__")
method.
这些参数将覆盖已经放置的任何配置，比如下面的，其中针对特定[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")构建新的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")：

    # at the module level, the global sessionmaker,plainplain
    # bound to a specific Engine
    Session = sessionmaker(bind=engine)

    # later, some unit of code wants to create a
    # Session that is bound to a specific Connection
    conn = engine.connect()
    session = Session(bind=conn)

将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与特定[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")关联的典型基本原理是维护外部事务的测试夹具
- 参见[Joining a Session into an External Transaction (such as for test
suites)](session_transaction.html#session-external-transaction)为例。

会话常见问题[¶](#session-frequently-asked-questions "Permalink to this headline")
---------------------------------------------------------------------------------

到此为止，许多用户已经对会话有疑问。本节介绍使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时出现的最基本问题的迷你常见问题解答（请注意，我们也有一个[*real
FAQ*](faq_index.html)）。

### 我什么时候制作[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")？[¶](#when-do-i-make-a-sessionmaker "Permalink to this headline")

只有一次，在应用程序的全局范围内。它应该被看作是应用程序配置的一部分。例如，如果您的应用程序在一个包中包含三个.py 文件，则可以将[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")行放入`__init__.py`文件中；从这一点上你的其他模块说“从 mypackage 导入会话”。That
way, everyone else just uses [`Session()`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session"),
and the configuration of that session is controlled by that central
point.

If your application starts up, does imports, but does not know what
database it’s going to be connecting to, you can bind the
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
at the “class” level to the engine later on, using
[`sessionmaker.configure()`](session_api.html#sqlalchemy.orm.session.sessionmaker.configure "sqlalchemy.orm.session.sessionmaker.configure").

在本节的例子中，我们经常会在实际调用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的行的上方创建[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")。但这仅仅是为了例子！实际上，[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")可能位于模块级别的某处。实例化[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的调用将被放置在数据库对话开始的应用程序中。

### 什么时候构建[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，我什么时候提交它，什么时候关闭它？[](#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it "Permalink to this headline")

TL；博士；

1.  As a general rule, keep the lifecycle of the session **separate and
    external** from functions and objects that access and/or manipulate
    database data. 这将大大有助于实现可预测和一致的交易范围。
2.  确保你清楚地知道交易在哪里开始和结束，并保持交易**短**，也就是说，它们以一系列操作结束，而不是无限期地开放。

一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")通常是在逻辑操作开始时建立的，在这个逻辑操作中数据库访问是潜在的预期。

无论何时用于与数据库交谈，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")在开始通信时都会立即开始数据库事务。假设`autocommit`标志保留为建议的`False`缺省值，则此事务将继续进行，直至[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")被回退，落实或关闭。[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")将在上一次交易结束后再次使用时开始新的交易；由此可见，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")能够在多次交易中获得生命周期，但一次只能有一次。我们将这两个概念称为**事务范围**和**会话范围**。

这里的含义是，SQLAlchemy
ORM 鼓励开发人员在他们的应用程序中建立这两个范围，不仅包括范围的开始和结束时间，还包括范围的范围，例如一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

开发人员决定这个范围的负担是 SQLAlchemy
ORM 必须对如何使用数据库有强烈意见的一个领域。[unit of
work](glossary.html#term-unit-of-work)模式具体是随着时间的推移积累变化并周期性地清除它们，保持内存中状态与已知在本地事务中存在的状态同步。这种模式只有在有意义的事务范围到位时才有效。

确定开始和结束[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")范围的最佳点通常不是很难，尽管各种各样的应用程序体系结构可能会引入具有挑战性的情况。

通常的选择是在事务结束的同时拆除[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，这意味着事务和会话范围是相同的。这是一个很好的选择，因为它消除了将会话范围视为与事务范围分开的需要。

虽然关于如何确定事务范围并没有一成不变的建议，但有一些常见模式。特别是如果你正在编写一个 Web 应用程序，那么这个选择已经非常成熟。

Web 应用程序是最简单的情况，因为这样的应用程序已经围绕一个一致的范围构建
-
这是**请求**，它表示来自浏览器的传入请求，处理该请求以制定一个响应，最后将该响应交付给客户。然后，将 Web 应用程序与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")集成是将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")范围与请求范围关联的简单任务。[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以在请求开始时建立，也可以使用延迟初始化模式，该模式在需要时立即建立。然后，请求继续进行，其中一些系统已经到位，应用程序逻辑可以以与访问实际请求对象的方式相关的方式访问当前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。当请求结束时，通常通过使用由 Web 框架提供的事件挂钩，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")也被拆除。The
transaction used by the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
may also be committed at this point, or alternatively the application
may opt for an explicit commit pattern, only committing for those
requests where one is warranted, but still always tearing down the
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
unconditionally at the end.

一些 Web 框架包含基础设施，以协助完成将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的生命周期与 Web 请求的寿命对齐的任务。这包括用于与 Flask
Web 框架结合使用的[Flask-SQLAlchemy](http://packages.python.org/Flask-SQLAlchemy/)等产品，以及通常与 Pyramid 框架一起使用的[Zope-SQLAlchemy](http://pypi.python.org/pypi/zope.sqlalchemy)。SQLAlchemy 建议将这些产品用作可用的。

In those situations where the integration libraries are not provided or
are insufficient, SQLAlchemy includes its own “helper” class known as
[`scoped_session`](contextual.html#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session").
有关该对象使用的教程位于[Contextual/Thread-local
Sessions](contextual.html#unitofwork-contextual)。它提供了将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与当前线程关联的快速方法，以及将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象与其他类型的作用域相关联的模式。

如前所述，对于非 Web 应用程序，没有明确的模式，因为应用程序本身并不只有一种架构模式。最好的策略是尝试划定“操作”，即特定线程开始在一段时间内执行一系列操作的点，这些操作可以在最后执行。一些例子：

-   产生子分叉的后台守护进程会希望为每个子进程创建一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，在该分支的“作业”生命周期中使用该[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")处理，然后在作业完成时将其撕下。
-   对于命令行脚本，应用程序将创建一个在程序开始工作时建立的单个全局[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，并在程序完成其任务时提交。
-   对于 GUI 界面驱动的应用程序，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的范围可能最好在用户生成事件的范围内，例如按钮按钮。或者，范围可以对应于明确的用户交互，诸如用户“打开”一系列记录，然后“保存”它们。

As a general rule, the application should manage the lifecycle of the
session *externally* to functions that deal with specific data.
这是一个关键问题的基本分离，它使得特定于数据的操作不受他们访问和操作数据的上下文的影响。

例如。 **不要这样做**：

    ### this is the **wrong way to do it** ###plain

    class ThingOne(object):
        def go(self):
            session = Session()
            try:
                session.query(FooBar).update({"x": 5})
                session.commit()
            except:
                session.rollback()
                raise

    class ThingTwo(object):
        def go(self):
            session = Session()
            try:
                session.query(Widget).update({"q": 18})
                session.commit()
            except:
                session.rollback()
                raise

    def run_my_program():
        ThingOne().go()
        ThingTwo().go()

保持会话（通常是交易）的生命周期**独立和外部**：

    ### this is a **better** (but not the only) way to do it ###plainplainplainplain

    class ThingOne(object):
        def go(self, session):
            session.query(FooBar).update({"x": 5})

    class ThingTwo(object):
        def go(self, session):
            session.query(Widget).update({"q": 18})

    def run_my_program():
        session = Session()
        try:
            ThingOne().go(session)
            ThingTwo().go(session)

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

高级开发人员将尽量保持会话，事务和异常管理的细节，尽可能避免程序工作的细节。例如，我们可以使用[上下文管理器](http://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)进一步分离关注点：

    ### another way (but again *not the only way*) to do it ###plainplain

    from contextlib import contextmanager

    @contextmanager
    def session_scope():
        """Provide a transactional scope around a series of operations."""
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def run_my_program():
        with session_scope() as session:
            ThingOne().go(session)
            ThingTwo().go(session)

### Session 是缓存吗？[¶](#is-the-session-a-cache "Permalink to this headline")

Yeee ...没有。它有点用作缓存，因为它实现了[identity
map](glossary.html#term-identity-map)模式，并存储了键入其主键的对象。但是，它不会执行任何类型的查询缓存。这意味着，如果你说`session.query(Foo).filter_by(name='bar')`，即使`Foo(name='bar')`在身份地图中，会议不知道这一点。它必须向数据库发出 SQL，取回行，然后当它看到行中的主键时，*然后*它可以查看本地标识映射并查看该对象已经存在。只有当你说`query.get（{some primary key））` [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")

此外，Session 会默认使用弱引用存储对象实例。这也违背了将会话用作缓存的目的。

[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")不是被设计成一个全局对象，每个人都可以作为对象的“注册表”进行咨询。这更像是一个**二级缓存**的工作。SQLAlchemy 使用[dogpile.cache](https://dogpilecache.readthedocs.io/)，通过[Dogpile
Caching](examples.html#examples-caching)示例提供了实现二级缓存的模式。

### 我如何获得某个对象的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")？[¶](#how-can-i-get-the-session-for-a-certain-object "Permalink to this headline")

使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")上的[`object_session()`](session_api.html#sqlalchemy.orm.session.Session.object_session "sqlalchemy.orm.session.Session.object_session")
classmethod：

    session = Session.object_session(someobject)plainplainplain

更新的[Runtime Inspection API](core_inspection.html)系统也可以使用：

    from sqlalchemy import inspectplainplain
    session = inspect(someobject).session

### 会话是线程安全的吗？[¶](#is-the-session-thread-safe "Permalink to this headline")

[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")非常适用于**非并发**方式，这通常意味着一次只有一个线程。

[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")应该以这样一种方式使用，即单个事务中的一系列操作存在一个实例。获得这种效果的一种便捷方法是将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与当前线程相关联（请参阅[Contextual/Thread-local
Sessions](contextual.html#unitofwork-contextual)以了解有关背景信息）。另一种方法是使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")在函数之间传递的模式，否则不与其他线程共享。

更重要的一点是，你不应该*要*使用多个并发线程的会话。这就好比让一家餐厅的每个人都从同一个盘子吃东西。会话是一个本地“工作空间”，您可以使用它来完成一组特定的任务；您不希望或需要与其他正在执行其他任务的线程共享该会话。

确保[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")一次只用于单个并发线程中称为“无共享”方法来实现并发。但实际上，不共享[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")意味着更重要的模式；它不仅意味着[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象本身，而且**与该 Session**关联的所有对象都必须保持在单个并发线程的范围内。与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联的一组映射对象本质上是对通过数据库连接访问的数据库行中的数据的代理，所以就像[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本身一样，整个对象集实际上只是数据库连接（或连接）的大规模代理。最终，它主要是我们远离并发访问的 DBAPI 连接本身；但由于[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")及与其关联的所有对象都是该 DBAPI 连接的所有代理，因此整个图对于并发访问基本上不安全。

If there are in fact multiple threads participating in the same task,
then you may consider sharing the session and its objects between those
threads; however, in this extremely unusual scenario the application
would need to ensure that a proper locking scheme is implemented so that
there isn’t *concurrent* access to the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
or its state.
对这种情况更常见的做法是每个并发线程维护一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，而不是从一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")复制*对象到另一个使用[`Session.merge()`](session_api.html#sqlalchemy.orm.session.Session.merge "sqlalchemy.orm.session.Session.merge")方法将对象的状态复制到不同的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本地的新对象中。*

使用会话的基础[¶](#basics-of-using-a-session "Permalink to this headline")
--------------------------------------------------------------------------

这里介绍最基本的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")使用模式。

### 查询[¶ T0\>](#querying "Permalink to this headline")

[`query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")函数接受一个或多个*实体*并返回一个新的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，该对象将在本会话的上下文中发出映射器查询。实体被定义为映射类，[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象，启用 orm 的*描述符*或`AliasedClass`对象：

    # query from a classplain
    session.query(User).filter_by(name='ed').all()

    # query with multiple classes, returns tuples
    session.query(User, Address).join('addresses').filter_by(name='ed').all()

    # query using orm-enabled descriptors
    session.query(User.name, User.fullname).all()

    # query from a mapper
    user_mapper = class_mapper(User)
    session.query(user_mapper)

当[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")返回结果时，实例化的每个对象都存储在标识映射中。当一行匹配已经存在的对象时，返回相同的对象。In
the latter case, whether or not the row is populated onto an existing
object depends upon whether the attributes of the instance have been
*expired* or not. 默认配置的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")会自动将所有实例沿着事务边界过期，因此对于通常是孤立的事务，应该不存在表示与当前事务相关的陈旧数据的实例的任何问题。

[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象在[Object
Relational
Tutorial](tutorial.html)中有详细介绍，并在 query\_api\_toplevel 中进一步介绍。

### 添加新的或现有的项目[¶](#adding-new-or-existing-items "Permalink to this headline")

[`add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")用于在实例中放置实例。对于*transient*（即全新的）实例，这将在下一次刷新时产生 INSERT 的效果。对于*持久*（即由此会话加载）的实例，它们已经存在并且不需要被添加。*已分离*的实例（即已从会话中删除）可以使用此方法重新与会话相关联：

    user1 = User(name='user1')
    user2 = User(name='user2')
    session.add(user1)
    session.add(user2)

    session.commit()     # write changes to the database

要一次向会话添加项目列表，请使用[`add_all()`](session_api.html#sqlalchemy.orm.session.Session.add_all "sqlalchemy.orm.session.Session.add_all")：

    session.add_all([item1, item2, item3])plainplain

沿`save-update`级联的[`add()`](session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")操作**级联**。欲了解更多详情，请参阅[Cascades](cascades.html#unitofwork-cascades)部分。

### 删除[¶ T0\>](#deleting "Permalink to this headline")

[`delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")方法将一个实例放入要标记为已删除的 Session 对象列表中：

    # mark two objects to be deleted
    session.delete(obj1)
    session.delete(obj2)

    # commit (or flush)
    session.commit()

#### 从集合中删除[¶](#deleting-from-collections "Permalink to this headline")

关于[`delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")出现的常见混淆是当集合的成员对象被删除时。集合成员被标记为从数据库中删除时，这不会影响集合本身在内存中，直到集合过期。下面我们举例说明即使在`Address`对象被标记为删除之后，即使在刷新之后，它仍然存在于与父`User`关联的集合中：

    >>> address = user.addresses[1]plain
    >>> session.delete(address)
    >>> session.flush()
    >>> address in user.addresses
    True

当上述会话提交时，所有属性都已过期。`user.addresses`的下一次访问将重新加载集合，从而显示所需的状态：

    >>> session.commit()plain
    >>> address in user.addresses
    False

删除集合中项目的通常做法是直接使用[`delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete")，而是使用级联行为自从从父集合中删除对象后自动调用删除。`delete-orphan`级联完成了这一点，如下例所示：

    mapper(User, users_table, properties={plainplain
        'addresses':relationship(Address, cascade="all, delete, delete-orphan")
    })
    del user.addresses[1]
    session.flush()

Where above, upon removing the `Address` object from
the `User.addresses` collection, the
`delete-orphan` cascade has the effect of marking
the `Address` object for deletion in the same way as
passing it to [`delete()`](session_api.html#sqlalchemy.orm.session.Session.delete "sqlalchemy.orm.session.Session.delete").

有关级联的详细信息，另请参阅[Cascades](cascades.html#unitofwork-cascades)。

#### 基于过滤条件删除[¶](#deleting-based-on-filter-criterion "Permalink to this headline")

对`Session.delete()`的警告是你需要有一个方便的对象来删除。查询包含一个[`delete()`](query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")方法，该方法根据过滤标准删除：

    session.query(User).filter(User.id==7).delete()plainplainplain

`Query.delete()`方法包含将会话中已存在的符合条件的对象“过期”的功能。然而，它确实有一些注意事项，包括“删除”和“删除孤立”级联不能充分表达已经加载的集合。有关更多详细信息，请参阅[`delete()`](query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")的 API 文档。

### 潮红[¶ T0\>](#flushing "Permalink to this headline")

当[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与其默认配置一起使用时，冲洗步骤几乎总是透明地进行。具体来说，刷新发生在任何单个[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")发布之前，以及在事务提交之前的[`commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")调用中。当使用[`begin_nested()`](session_api.html#sqlalchemy.orm.session.Session.begin_nested "sqlalchemy.orm.session.Session.begin_nested")时，它也发生在发出 SAVEPOINT 之前。

无论自动刷新设置如何，都可以通过发出[`flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")来强制刷新：

    session.flush()

通过使用标志`autoflush=False`构造[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")，可以禁用行为的“flush-on-Query”方面：

    Session = sessionmaker(autoflush=False)plain

另外，可以随时通过设置`autoflush`标志暂时禁用自动刷新：

    mysession = Session()plain
    mysession.autoflush = False

一些禁止自动刷新的配方可在[DisableAutoFlush](http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DisableAutoflush)中找到。

The flush process *always* occurs within a transaction, even if the
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
has been configured with `autocommit=True`, a
setting that disables the session’s persistent transactional state.
如果没有事务存在，[`flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")创建自己的事务并提交它。在刷新期间任何失败都会导致所有交易的回滚。如果会话不处于`autocommit=True`模式，即使基本事务已经被回滚，但在刷新失败后仍需要对[`rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")进行显式调用
- 这样可以保持所谓的“子事务”的整体嵌套模式。

### 犯[¶ T0\>](#committing "Permalink to this headline")

[`commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")
is used to commit the current transaction.
它总是事先发送[`flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")以将任何剩余状态清除到数据库；这与“自动刷新”设置无关。如果没有交易存在，则会引发错误。请注意，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的默认行为是“交易”始终存在；这种行为可以通过设置`autocommit=True`来禁用。在自动提交模式下，可以通过调用[`begin()`](session_api.html#sqlalchemy.orm.session.Session.begin "sqlalchemy.orm.session.Session.begin")方法启动事务。

注意

这里的术语“事务”是指[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")内部的一个事务性构造，它可以维持零个或多个实际数据库（DBAPI）事务。一个单独的 DBAPI 连接开始参与“事务”，因为它首先用于执行 SQL 语句，然后直到会话级别“事务”完成时才存在。有关更多详细信息，请参阅[Managing
Transactions](session_transaction.html#unitofwork-transaction)。

[`commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")的另一个行为是，默认情况下，它会在提交完成后超时所有实例的状态。这样当下次访问实例时，无论是通过属性访问还是通过它们存在于[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")结果集中，它们都会收到最近的状态。要禁用此行为，请使用`expire_on_commit=False`配置[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")。

通常情况下，加载到[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的实例不会被随后的查询改变；假定当前事务是孤立的，所以只要事务继续，最近加载的状态是正确的。由于[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的行为与属性状态完全相同，除了不存在事务外，设置`autocommit=True`在某种程度上对此模型起作用。

### 回滚[¶](#rolling-back "Permalink to this headline")

[`rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")回滚当前事务。使用默认配置的会话时，会话的回滚后状态如下所示：

> -   所有事务回滚并且所有连接返回到连接池，除非 Session 直接绑定到 Connection，在这种情况下，连接仍然保持（但仍然回滚）。
> -   当它们被添加到事务生命周期内的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时，最初处于*挂起*状态的对象被删除，对应于它们的 INSERT 语句被回滚。它们的属性状态保持不变。
> -   在事务生命周期内被标记为*删除*的对象被提升回*持久*状态，对应于它们的 DELETE 语句被回滚。请注意，如果这些对象在事务内第一个*挂起*，则该操作优先。
> -   所有未被清除的对象已经过期。

在了解该状态的情况下，[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")可以在回滚发生后安全地继续使用。

当[`flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")失败时，通常由于主键，外键或“不可空”约束违反等原因而自动发出[`rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")部分故障后可能会继续冲洗）。但是，flush 过程总是使用自己的事务划分器，称为*subsnsaction*，这在[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的文档字符串中有更详细的描述。这意味着即使数据库事务已经回滚，最终用户仍然必须发出[`rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")来完全重置[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的状态。

### 结束[¶ T0\>](#closing "Permalink to this headline")

[`close()`](session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")方法发布[`expunge_all()`](session_api.html#sqlalchemy.orm.session.Session.expunge_all "sqlalchemy.orm.session.Session.expunge_all")，[releases](glossary.html#term-releases)任何事务/连接资源。当连接返回到连接池时，事务状态也会回滚。
