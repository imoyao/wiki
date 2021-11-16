---
title: 上下文/线程本地会话
date: 2021-02-20 22:41:40
permalink: /sqlalchemy/orm/contextual/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
上下文/线程本地会话[¶](#contextual-thread-local-sessions "Permalink to this headline")
======================================================================================

回想一下[When do I construct a Session, when do I commit it, and when do
I close
it?](session_basics.html#session-faq-whentocreate)，引入了“session
scopes”的概念，重点放在 web 应用程序和练习将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的作用域与 Web 请求的作用域相关联。大多数现代 Web 框架都包含集成工具，因此可以自动管理[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的范围，并且应该尽可能使用这些工具。

SQLAlchemy 包括其自己的帮助对象，这有助于建立用户定义的[`会话`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")范围。它也被第三方集成系统用来帮助构建他们的集成方案。

该对象是[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")对象，它表示[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的**注册表**。如果您不熟悉注册表模式，可以在[企业架构模式](http://martinfowler.com/eaaCatalog/registry.html)中找到一个很好的介绍。

注意

[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")对象是许多 SQLAlchemy 应用程序使用的非常流行和有用的对象。然而，重要的是要注意，它只向[`会话`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")管理的问题提出**一种方法**。如果您是 SQLAlchemy 的新手，特别是如果术语“线程局部变量”对您来说看起来很陌生，我们建议您尽可能先熟悉一个现成的集成系统，例如[Flask-SQLAlchemy
\< /
t0\>或](http://packages.python.org/Flask-SQLAlchemy/)[zope.sqlalchemy](http://pypi.python.org/pypi/zope.sqlalchemy)。

通过调用它来构造一个[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")，传递一个**工厂**，可以创建新的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象。一个工厂只是在调用时产生一个新的对象，而在 Session 的情况下，最常见的工厂就是本节前面介绍的 sessionmaker。
[](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")[](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")下面我们来说明这个用法：

    >>> from sqlalchemy.orm import scoped_session
    >>> from sqlalchemy.orm import sessionmaker

    >>> session_factory = sessionmaker(bind=some_engine)
    >>> Session = scoped_session(session_factory)

当我们“调用”注册表时，我们创建的[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")对象现在将调用[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")

    >>> some_session = Session()plain

以上，`some_session`是[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的一个实例，我们现在可以使用它来与数据库通信。同样的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")也出现在我们创建的[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")注册表中。如果我们再次调用注册表，我们会返回**相同的**
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")：

    >>> some_other_session = Session()
    >>> some_session is some_other_session
    True

该模式允许应用程序的不同部分调用全局[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")，以便所有这些区域可能共享相同的会话，而无需明确地传递。我们在注册表中建立的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")将保持，直到我们通过调用[`scoped_session.remove()`](#sqlalchemy.orm.scoping.scoped_session.remove "sqlalchemy.orm.scoping.scoped_session.remove")明确告诉我们的注册表处理它：

    >>> Session.remove()

[`scoped_session.remove()`](#sqlalchemy.orm.scoping.scoped_session.remove "sqlalchemy.orm.scoping.scoped_session.remove")方法首先在当前的[`会话`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")上调用[`Session.close()`](session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")，这样可以释放任何连接/事务首先由[`会话`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")拥有的资源，然后丢弃[`会话`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")本身。这里的“释放”意味着连接将返回到其连接池，并且任何事务状态都将回滚，最终使用底层 DBAPI 连接的`rollback()`方法。

此时，[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")对象为“空”，并在再次调用时创建**新**
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。如下图所示，这与我们之前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")不一样：

    >>> new_session = Session()plain
    >>> new_session is some_session
    False

上述一系列步骤简要说明了“注册表”模式的概念。有了这个基本想法，我们可以讨论这种模式如何进行的一些细节。

隐式方法访问[¶](#implicit-method-access "Permalink to this headline")
---------------------------------------------------------------------

[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")的工作很简单；为所有需要的人保留一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。作为对这个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")产生更多透明访问的手段，[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")还包含**代理行为**，这意味着注册表本身可以被视为类似直接[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")；当在这个对象上调用方法时，它们被**代理**到由注册表维护的基础[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")：

    Session = scoped_session(some_factory)plain

    # equivalent to:
    #
    # session = Session()
    # print(session.query(MyClass).all())
    #
    print(Session.query(MyClass).all())

上面的代码通过调用注册表来完成与获取当前[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")相同的任务，然后使用该[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

线程本地作用域[¶](#thread-local-scope "Permalink to this headline")
-------------------------------------------------------------------

熟悉多线程编程的用户会注意到，将任何东西表示为全局变量通常是一个坏主意，因为它意味着全局对象将被许多线程同时访问。[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象完全被设计为以**非并发**方式使用，就多线程而言意味着“一次只能在一个线程中”。So
our above example of [`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")
usage, where the same [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
object is maintained across multiple calls, suggests that some process
needs to be in place such that mutltiple calls across many threads don’t
actually get a handle to the same session.
我们称之为**线程本地存储**，这意味着将使用一个特殊的对象来维护每个应用程序线程的独特对象。Python 通过[threading.local()](http://docs.python.org/library/threading.html#threading.local)结构提供了这个功能。The
[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")
object by default uses this object as storage, so that a single
[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
is maintained for all who call upon the [`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")
registry, but only within the scope of a single thread.
在另一个线程中调用注册表的调用者将获得该另一个线程本地的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")实例。

使用这种技术，[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")提供了一个快速且相对简单的方法（如果人们熟悉线程本地存储），在应用程序中提供单个全局对象的方式可以安全地从多个线程。

与往常一样，[`scoped_session.remove()`](#sqlalchemy.orm.scoping.scoped_session.remove "sqlalchemy.orm.scoping.scoped_session.remove")方法会移除与该线程关联的当前[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")（如果有的话）。但是，`threading.local()`对象的一个​​优点是，如果应用程序线程本身结束，那么该线程的“存储”也会被垃圾收集。因此，使用线程本地作用域和一个生成并拆除线程的应用程序实际上是“安全的”，而不需要调用[`scoped_session.remove()`](#sqlalchemy.orm.scoping.scoped_session.remove "sqlalchemy.orm.scoping.scoped_session.remove")。然而，事务本身的范围，即通过[`Session.commit()`](session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")或[`Session.rollback()`](session_api.html#sqlalchemy.orm.session.Session.rollback "sqlalchemy.orm.session.Session.rollback")结束它们通常仍然是必须明确安排在适当的时间，除非应用程序实际上将线程的生命周期与事务的生命周期相关联。

在 Web 应用程序中使用线程本地作用域[¶](#using-thread-local-scope-with-web-applications "Permalink to this headline")
------------------------------------------------------------------------------------------------------------------

正如在[When do I construct a Session, when do I commit it, and when do I
close
it?](session_basics.html#session-faq-whentocreate)，Web 应用程序围绕**Web 请求的概念构建
t2\>，并且将这样的应用程序与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")集成通常意味着[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")将与该请求相关联。**事实证明，大多数 Python
Web 框架（异常框架 Twisted 和 Tornado 等显着异常）都以简单的方式使用线程，以便在一个*工作线程*。当请求结束时，工作线程被释放到可用于处理另一请求的工作者池中。

Web 请求和线程的这种简单对应意味着将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与线程相关联意味着它也与该线程内运行的 Web 请求相关联，反之亦然，前提是[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")因此，使用[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")作为将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与 Web 应用程序集成的快速方法是一种常见做法。下面的序列图说明了这个流程：

    Web Server          Web Framework        SQLAlchemy ORM Code
    --------------      --------------       ------------------------------
    startup        ->   Web framework        # Session registry is established
                        initializes          Session = scoped_session(sessionmaker())

    incoming
    web request    ->   web request     ->   # The registry is *optionally*
                        starts               # called upon explicitly to create
                                             # a Session local to the thread and/or request
                                             Session()

                                             # the Session registry can otherwise
                                             # be used at any time, creating the
                                             # request-local Session() if not present,
                                             # or returning the existing one
                                             Session.query(MyClass) # ...

                                             Session.add(some_object) # ...

                                             # if data was modified, commit the
                                             # transaction
                                             Session.commit()

                        web request ends  -> # the registry is instructed to
                                             # remove the Session
                                             Session.remove()

                        sends output      <-
    outgoing web    <-
    response

使用上述流程，将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与 Web 应用程序集成的过程有两个要求：

1.  首次启动 Web 应用程序时，创建一个[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")注册表，确保该对象可由应用程序的其余部分访问。
2.  确保在 Web 请求结束时调用[`scoped_session.remove()`](#sqlalchemy.orm.scoping.scoped_session.remove "sqlalchemy.orm.scoping.scoped_session.remove")，通常通过与 Web 框架的事件系统集成以建立“请求结束”事件。

As noted earlier, the above pattern is **just one potential way** to
integrate a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
with a web framework, one which in particular makes the significant
assumption that the **web framework associates web requests with
application threads**. It is however **strongly recommended that the
integration tools provided with the web framework itself be used, if
available**, instead of [`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session").

In particular, while using a thread local can be convenient, it is
preferable that the [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
be associated **directly with the request**, rather than with the
current thread.
自定义作用域的下一部分详细介绍了一种更高级的配置，它可以将[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")的用法与基于直接请求的作用域或任何类型的作用域相结合。

使用自定义创建的范围[¶](#using-custom-created-scopes "Permalink to this headline")
----------------------------------------------------------------------------------

[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")对象的“线程本地”范围的默认行为只是“范围”[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的众多选项之一。自定义范围可以基于任何现有的“我们正在处理的事物”的系统来定义。

假设一个 web 框架定义了一个库函数`get_current_request()`。使用此框架构建的应用程序可以随时调用此函数，并且结果将是表示当前正在处理的请求的某种`Request`对象。如果`Request`对象是可散列的，那么这个函数可以很容易地与[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")集成以将[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")与请求相关联。下面我们结合 Web 框架`on_request_end`提供的假设事件标记来说明这一点，该请求允许在请求结束时调用代码：

    from my_web_framework import get_current_request, on_request_endplain
    from sqlalchemy.orm import scoped_session, sessionmaker

    Session = scoped_session(sessionmaker(bind=some_engine), scopefunc=get_current_request)

    @on_request_end
    def remove_session(req):
        Session.remove()

在上面，我们以通常的方式实例化[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")，不同之处在于我们将我们的请求返回函数作为“scopefunc”传递。这指示[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")在调用注册表返回当前[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")时使用此函数生成字典密钥。在这种情况下，我们确保实施可靠的“删除”系统尤为重要，因为本字典不能自行管理。

上下文会话 API [¶](#contextual-session-api "Permalink to this headline")
-----------------------------------------------------------------------

*class* `sqlalchemy.orm.scoping。`{.descclassname} `scoped_session`{.descname} （ *session\_factory*，*scopefunc =无 T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.scoping.scoped_session "Permalink to this definition")*
:   提供[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象的范围管理。

    有关教程，请参阅[Contextual/Thread-local
    Sessions](#unitofwork-contextual)。

    ` __呼叫__  T0> （ T1>  **千瓦 T2> ） T3> ¶ T4>`{.descname}
    :   返回当前[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，如果不存在，则使用[`scoped_session.session_factory`](#sqlalchemy.orm.scoping.scoped_session.session_factory "sqlalchemy.orm.scoping.scoped_session.session_factory")创建它。

        参数：

        **\*\*kw**[¶](#sqlalchemy.orm.scoping.scoped_session.__call__.params.**kw)
        – Keyword arguments will be passed to the
        [`scoped_session.session_factory`](#sqlalchemy.orm.scoping.scoped_session.session_factory "sqlalchemy.orm.scoping.scoped_session.session_factory")
        callable, if an existing [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
        is not present. 如果存在[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")并且关键字参数已被传递，则引发[`InvalidRequestError`](core_exceptions.html#sqlalchemy.exc.InvalidRequestError "sqlalchemy.exc.InvalidRequestError")。

    `__ init __`{.descname} （ *session\_factory*，*scopefunc = None* ） [t5 \>](#sqlalchemy.orm.scoping.scoped_session.__init__ "Permalink to this definition")
    :   构建一个新的[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")。

        参数：

        -   **session\_factory**[¶](#sqlalchemy.orm.scoping.scoped_session.params.session_factory)
            – a factory to create new [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
            instances. 这通常但不一定是[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")的一个实例。
        -   **scopefunc**
            [¶](#sqlalchemy.orm.scoping.scoped_session.params.scopefunc)
            -
            定义当前范围的可选函数。如果不通过，[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")对象将采用“线程本地”作用域，并将使用Python
            `threading.local()`来维护当前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")如果通过，函数应该返回一个可哈希标记；此标记将用作字典中的键以存储和检索当前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

    `配置 T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   重新配置这个[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")使用的[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")。

        参见[`sessionmaker.configure()`](session_api.html#sqlalchemy.orm.session.sessionmaker.configure "sqlalchemy.orm.session.sessionmaker.configure")。

    ` query_property  T0> （ T1>  query_cls =无 T2> ） T3> ¶ T4>`{.descname}
    :   返回一个类属性，它在调用时针对类和当前[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")生成一个[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象。

        例如。：

            Session = scoped_session(sessionmaker())

            class MyClass(object):
                query = Session.query_property()

            # after mappers are defined
            result = MyClass.query.filter(MyClass.name=='foo').all()

        默认生成会话配置的查询类的实例。要覆盖和使用自定义实现，请提供一个`query_cls`可调用。可调用对象将作为位置参数和会话关键字参数与类的映射器一起调用。

        放置在类上的查询属性的数量没有限制。

    `除去 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果存在，则丢弃当前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。

        这将首先在当前的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")上调用[`Session.close()`](session_api.html#sqlalchemy.orm.session.Session.close "sqlalchemy.orm.session.Session.close")方法，该方法释放仍然保存的任何现有的事务/连接资源；交易具体回滚。然后[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")被丢弃。在相同范围内的下一次使用时，[`scoped_session`](#sqlalchemy.orm.scoping.scoped_session "sqlalchemy.orm.scoping.scoped_session")将生成一个新的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象。

    `session_factory`{.descname} *=无* [¶](#sqlalchemy.orm.scoping.scoped_session.session_factory "Permalink to this definition")
    :   提供给\_\_ init
        \_\_的session\_factory存储在此属性中，并可以在稍后访问。当需要新的非范围[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")到数据库时，这非常有用。

 *class*`sqlalchemy.util.`{.descclassname}`ScopedRegistry`{.descname}(*createfunc*, *scopefunc*)[¶](#sqlalchemy.util.ScopedRegistry "Permalink to this definition")
:   基于“范围”功能可以存储单个类的一个或多个实例的注册表。

    该对象将`__call__`实现为“getter”，因此通过调用`myregistry()`，将为当前范围返回包含的对象。plain

    参数：

    -   **createfunc**[¶](#sqlalchemy.util.ScopedRegistry.params.createfunc)
        – a callable that returns a new object to be placed in the
        registry
    -   **scopefunc**[¶](#sqlalchemy.util.ScopedRegistry.params.scopefunc)
        – a callable that will return a key to store/retrieve an object.

    `__ init __`{.descname} （ *createfunc*，*scopefunc* ） [](#sqlalchemy.util.ScopedRegistry.__init__ "Permalink to this definition")
    :   构建一个新的[`ScopedRegistry`](#sqlalchemy.util.ScopedRegistry "sqlalchemy.util.ScopedRegistry")。

        参数：

        -   **createfunc**[¶](#sqlalchemy.util.ScopedRegistry.params.createfunc)
            – A creation function that will generate a new value for the
            current scope, if none is present.
        -   **scopefunc**[¶](#sqlalchemy.util.ScopedRegistry.params.scopefunc)
            – A function that returns a hashable token representing the
            current scope (such as, current thread identifier).

    `明确 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   清除当前的范围，如果有的话。

    `具有 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果当前范围中存在对象，则返回True。

    `设置 T0> （ T1>  OBJ  T2> ） T3> ¶ T4>`{.descname}
    :   设置当前范围的值。

*class* `sqlalchemy.util。`{.descclassname} `ThreadLocalRegistry`{.descname} （ *createfunc* ） t5 \> [¶ T6\>](#sqlalchemy.util.ThreadLocalRegistry "Permalink to this definition")
:   基础：`sqlalchemy.util._collections.ScopedRegistry`

    一个使用`threading.local()`变量进行存储的[`ScopedRegistry`](#sqlalchemy.util.ScopedRegistry "sqlalchemy.util.ScopedRegistry")。


