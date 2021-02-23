---
title: baked
date: 2021-02-20 22:41:41
permalink: /pages/e0b666/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
  - extensions
tags:
  - 
---
烘焙查询[¶](#module-sqlalchemy.ext.baked "Permalink to this headline")
======================================================================

`baked`为[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象提供了替代的创建模式，可以缓存对象的构造和字符串编译步骤。这意味着对于不止一次使用的特定[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")构建场景，从构建查询的初始构建到生成SQL字符串的所有Python函数调用都将仅发生**一次**，而不是每次查询建立和执行。

The rationale for this system is to greatly reduce Python interpreter
overhead for everything that occurs **before the SQL is emitted**.
“烘焙”系统的缓存以任何方式减少SQL调用或缓存来自数据库的**返回结果**。**不是**。在[Dogpile
Caching](examples.html#examples-caching)中提供了一种演示SQL调用和结果集本身缓存的技术。

版本1.0.0中的新功能

注意

从1.0.0开始，[`sqlalchemy.ext.baked`](#module-sqlalchemy.ext.baked "sqlalchemy.ext.baked")扩展名应该被认为是**实验**。它提供了一个显着不同的查询系统，但尚未得到大规模的证明。

概要[¶ T0\>](#synopsis "Permalink to this headline")
----------------------------------------------------

烘焙系统的使用开始于生成所谓的“面包店”，该面包店代表特定系列查询对象的存储：

    from sqlalchemy.ext import baked

    bakery = baked.bakery()

上述“面包店”将高速缓存的数据存储在默认为200个元素的LRU缓存中，注意到ORM查询通常包含一个ORM查询条目以及一个SQL数据库每个数据库方言条目。

面包店允许我们建立一个[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，方法是将其构造指定为一系列Python可调用对象，通常是lambda表达式。为简洁起见，它会覆盖`+=`运算符，以便典型的查询构建如下所示：

    from sqlalchemy import bindparam

    def search_for_user(session, username, email=None):

        baked_query = bakery(lambda session: session.query(User))
        baked_query += lambda q: q.filter(User.name == bindparam('username'))

        baked_query += lambda q: q.order_by(User.id)

        if email:
            baked_query += lambda q: q.filter(User.email == bindparam('email'))

        result = baked_query(session).params(username=username, email=email).all()

        return result

以下是关于上述代码的一些观察结果：

1.  `baked_query`对象是[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")的一个实例。This
    object is essentially the “builder” for a real orm [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object, but it is not itself the *actual* [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    object.
2.  实际的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象根本不会被构建，直到调用[`Result.all()`](#sqlalchemy.ext.baked.Result.all "sqlalchemy.ext.baked.Result.all")时函数的结尾。
3.  添加到`baked_query`对象的步骤全部表示为Python函数，通常是lambda表达式。赋给[`bakery()`](#sqlalchemy.ext.baked.bakery "sqlalchemy.ext.baked.bakery")函数的第一个lambda表达式接收一个[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")作为它的参数。其余的lambda每个都接收一个[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")作为它们的参数。
4.  In the above code, even though our application may call upon
    `search_for_user()` many times, and even though
    within each invocation we build up an entirely new
    [`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")
    object, *all of the lambdas are only called once*.
    只要这个查询被缓存在面包房中，每个lambda都是**从不**调用的第二次。
5.  通过存储对**lambda对象本身的引用**来实现高速缓存，以便制定高速缓存密钥；也就是说，Python解释器为这些函数分配一个Python内部身份的事实决定了如何在连续运行中识别查询。For
    those invocations of `search_for_user()` where
    the `email` parameter is specified, the callable
    `lambda q: q.filter(User.email == bindparam('email'))` will be part of the cache key that’s retrieved; when
    `email` is `None`, this
    callable is not part of the cache key.
6.  因为lambda只被调用一次，所以必须保证在lambda表达式中**内没有引用可能会改变的变量；相反，假设这些值是绑定到SQL字符串中的，我们使用[`bindparam()`](core_sqlelement.html#sqlalchemy.sql.expression.bindparam "sqlalchemy.sql.expression.bindparam")来构造命名参数，其中我们稍后使用[`Result.params()`](#sqlalchemy.ext.baked.Result.params "sqlalchemy.ext.baked.Result.params")**

性能[¶ T0\>](#performance "Permalink to this headline")
-------------------------------------------------------

烘焙的查询可能看起来有点奇怪，有点尴尬，有点冗长。但是，在应用程序中多次调用的查询所节省的Python性能非常显着。在[Performance](examples.html#examples-performance)中演示的示例套件`short_selects`演示了每个只返回一行的查询的比较，例如以下常规查询：

    session = Session(bind=engine)
    for id_ in random.sample(ids, n):
        session.query(Customer).filter(Customer.id == id_).one()

与同等的“烘焙”查询相比：

    bakery = baked.bakery()
    s = Session(bind=engine)
    for id_ in random.sample(ids, n):
        q = bakery(lambda s: s.query(Customer))
        q += lambda q: q.filter(Customer.id == bindparam('id'))
        q(s).params(id=id_).one()

对每个块调用10000次迭代的Python函数调用计数的区别如下：

    test_baked_query : test a baked query of the full entity.
                       (10000 iterations); total fn calls 1951294

    test_orm_query :   test a straight ORM query of the full entity.
                       (10000 iterations); total fn calls 7900535

就功能强大的笔记本电脑而言，这个数字表示为：

    test_baked_query : test a baked query of the full entity.
                       (10000 iterations); total time 2.174126 sec

    test_orm_query :   test a straight ORM query of the full entity.
                       (10000 iterations); total time 7.958516 sec

请注意，此测试非常有意地使用只返回一行的查询。对于返回很多行的查询，烘焙查询的性能优势将会产生越来越小的影响，与获取行所花费的时间成正比。请记住，**烘焙查询功能仅适用于构建查询本身，而不是结果提取**。使用烘焙的功能绝不能保证更快的应用程序；对于那些被测量为受到这种特定形式的开销影响的应用程序，它只是一个潜在的有用功能。

测量两次，切一次

有关如何配置SQLAlchemy应用程序的背景信息，请参阅[Performance](faq_performance.html#faq-performance)部分。在尝试提高应用程序的性能时，使用性能测量技术是非常重要的。

理[¶ T0\>](#rationale "Permalink to this headline")
---------------------------------------------------

上面的“lambda”方法是更传统的“参数化”方法的超集。假设我们希望构建一个简单的系统，我们只需构建一次[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")，然后将其存储在字典中供重复使用。这可以通过构建查询并通过调用`my_cached_query = query.with_session来移除Session` （无） T6\> T3\>：

    my_simple_cache = {}

    def lookup(session, id_argument):
        if "my_key" not in my_simple_cache:
            query = session.query(Model).filter(Model.id == bindparam('id'))
            my_simple_cache["my_key"] = query.with_session(None)
        else:
            query = my_simple_cache["my_key"].with_session(session)

        return query.params(id=id_argument).all()

上述方法使我们获得了非常小的性能优势。通过重新使用[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")，我们保存了`session.query(Model)`构造函数中的Python工作，并调用`过滤器（Model .id == bindparam（'id'））`，它会跳过我们构建Core表达式以及发送它到[`Query.filter()`](query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")。但是，每次调用[`Query.all()`](query.html#sqlalchemy.orm.query.Query.all "sqlalchemy.orm.query.Query.all")时，该方法仍然会重新生成完整的[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象，并且还会发送此全新的[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")到每次的字符串编译步骤，对于像上面这样的简单情况，这可能是大约70％的开销。

为了减少额外的开销，我们需要一些更专门的逻辑，一些方法来记忆选择对象的构造和SQL的构造。Wiki中有一个例子是[BakedQuery](https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/BakedQuery)，它是该功能的先驱，但是在该系统中，我们没有缓存查询的*构造*。为了消除所有的开销，我们需要缓存查询的构造以及SQL编译。Let’s
assume we adapted the recipe in this way and made ourselves a method
`.bake()` that pre-compiles the SQL for the query,
producing a new object that can be invoked with minimal overhead.
我们的例子变成：

    my_simple_cache = {}

    def lookup(session, id_argument):

        if "my_key" not in my_simple_cache:
            query = session.query(Model).filter(Model.id == bindparam('id'))
            my_simple_cache["my_key"] = query.with_session(None).bake()
        else:
            query = my_simple_cache["my_key"].with_session(session)

        return query.params(id=id_argument).all()

上面，我们已经解决了性能问题，但我们仍然有这个字符串缓存键来处理。

我们可以使用“面包店”的方法来重新构建上述方法，这种方式看起来比“构建lambda”方法更不寻常，更像是对简单的“重用查询”方法的简单改进：

    bakery = baked.bakery()

    def lookup(session, id_argument):
        def create_model_query(session):
            return session.query(Model).filter(Model.id == bindparam('id'))

        parameterized_query = bakery.bake(create_model_query)
        return parameterized_query(session).params(id=id_argument).all()

在上面，我们使用“烘焙”系统，其方式与简单化的“缓存查询”系统非常相似。然而，它使用了少两行代码，不需要制作“my\_key”的缓存键，而且还包含了与我们自定义的“烘焙”功能相同的功能，可以从构建器缓存100％的Python调用工作查询过滤器调用，以生成[`Select`](core_selectable.html#sqlalchemy.sql.expression.Select "sqlalchemy.sql.expression.Select")对象到字符串编译步骤。

从以上所述，如果我们问自己，“如果查询需要对查询结构做出条件性决定会怎样？”，这就是希望变得明显，为什么“烘焙”就是这样。我们可以从*中的任意数量的*函数构建它，而不是从一个函数构建参数化查询（这是我们认为烘焙最初可能工作的方式）。考虑我们的天真示例，如果我们需要在条件基础上在查询中添加附加子句：

    my_simple_cache = {}

    def lookup(session, id_argument, include_frobnizzle=False):
        if include_frobnizzle:
            cache_key = "my_key_with_frobnizzle"
        else:
            cache_key = "my_key_without_frobnizzle"

        if cache_key not in my_simple_cache:
            query = session.query(Model).filter(Model.id == bindparam('id'))
            if include_frobnizzle:
                query = query.filter(Model.frobnizzle == True)

            my_simple_cache[cache_key] = query.with_session(None).bake()
        else:
            query = my_simple_cache[cache_key].with_session(session)

        return query.params(id=id_argument).all()

我们的“简单”参数化系统现在必须负责生成缓存键，这个缓存键考虑了是否传递了“include\_frobnizzle”标志，因为这个标志的存在意味着生成的SQL将完全不同。很明显，随着查询构建的复杂性提高，缓存这些查询的任务变得非常快速。我们可以将上面的例子转换为直接使用“面包店”，如下所示：

    bakery = baked.bakery()

    def lookup(session, id_argument, include_frobnizzle=False):
        def create_model_query(session):
            return session.query(Model).filter(Model.id == bindparam('id'))

        parameterized_query = bakery.bake(create_model_query)

        if include_frobnizzle:
            def include_frobnizzle_in_query(query):
                return query.filter(Model.frobnizzle == True)

            parameterized_query = parameterized_query.with_criteria(
                include_frobnizzle_in_query)

        return parameterized_query(session).params(id=id_argument).all()

在上面，我们不仅缓存查询对象，还缓存为了生成SQL而需要执行的所有工作。我们也不再需要处理确保我们生成一个缓存键，该缓存键准确地考虑了我们所做的所有结构修改；这现在可以自动处理，并且不会出错。

此代码示例比简单示例短几行，无需处理缓存键，并且具有完整的所谓“烘焙”功能的巨大性能优势。但仍然有点冗长！因此，我们采用像[`BakedQuery.add_criteria()`](#sqlalchemy.ext.baked.BakedQuery.add_criteria "sqlalchemy.ext.baked.BakedQuery.add_criteria")和[`BakedQuery.with_criteria()`](#sqlalchemy.ext.baked.BakedQuery.with_criteria "sqlalchemy.ext.baked.BakedQuery.with_criteria")这样的方法并将它们缩短为运算符，并鼓励（尽管肯定不需要！）使用简单的lambda表达式，只是为了减少冗长：

    bakery = baked.bakery()

    def lookup(session, id_argument, include_frobnizzle=False):
        parameterized_query = bakery.bake(
            lambda s: s.query(Model).filter(Model.id == bindparam('id'))
          )

        if include_frobnizzle:
            parameterized_query += lambda q: q.filter(Model.frobnizzle == True)

        return parameterized_query(session).params(id=id_argument).all()

如上所述，该方法实现起来较为简单，代码流与非缓存查询函数看起来更相似，因此使代码更易于移植。

以上描述基本上是用于达到当前“烘焙”方法的设计过程的总结。从“常规”方法开始，需要解决高速缓存密钥构建和管理，删除所有冗余Python执行以及使用条件构建的查询等附加问题，从而形成最终方法。

延迟加载整合[¶](#lazy-loading-integration "Permalink to this headline")
-----------------------------------------------------------------------

已烘焙的查询可以透明地与SQLAlchemy的懒加载程序功能集成。未来版本的SQLAlchemy可能默认启用此功能，因为它在延迟加载中的使用是完全透明的。现在，要为全系统的所有lazyloader启用烘焙加载，请调用[`bake_lazy_loaders()`](#sqlalchemy.ext.baked.bake_lazy_loaders "sqlalchemy.ext.baked.bake_lazy_loaders")函数。这将影响所有使用`lazy='select'`策略的关系以及所有使用[`lazyload()`](loading_relationships.html#sqlalchemy.orm.lazyload "sqlalchemy.orm.lazyload")的每个查询策略。

可以使用`baked_select`加载器策略在每个[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")基础上启用“烘焙”延迟加载：

    class MyClass(Base):
        # ...

        widgets = relationship("Widget", lazy="baked_select")

只要应用程序的任何部分导入了`sqlalchemy.ext.baked`模块，就可以使用`baked_select`策略。此功能使用的“面包房”对于`MyClass`的映射器是本地的。

对于每个查询使用，可以使用[`baked_lazyload()`](#sqlalchemy.ext.baked.baked_lazyload "sqlalchemy.ext.baked.baked_lazyload")策略，该策略与任何其他加载程序选项一样。

### 选择与bake\_queries标志[¶](#opting-out-with-the-bake-queries-flag "Permalink to this headline")

[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构包含一个标志[`relationship.bake_queries`](relationship_api.html#sqlalchemy.orm.relationship.params.bake_queries "sqlalchemy.orm.relationship")，当设置为False时，会导致该关系退出烘焙查询系统，当应用程序范围[`bake_lazy_loaders()`](#sqlalchemy.ext.baked.bake_lazy_loaders "sqlalchemy.ext.baked.bake_lazy_loaders")函数来启用烘焙查询加载器。

API文档[¶](#api-documentation "Permalink to this headline")
-----------------------------------------------------------

 `sqlalchemy.ext.baked.`{.descclassname}`bakery`{.descname}(*cls*, *size=200*)[¶](#sqlalchemy.ext.baked.bakery "Permalink to this definition")
:   建造一个新的面包店。

*class* `sqlalchemy.ext.baked。`{.descclassname} `BakedQuery`{.descname} （ *面包店*，*initial\_fn*，*args =()* ） [¶](#sqlalchemy.ext.baked.BakedQuery "Permalink to this definition")
:   [`query.Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象的构建器对象。

    `add_criteria`{.descname} （ *fn*，*\* args* ） [](#sqlalchemy.ext.baked.BakedQuery.add_criteria "Permalink to this definition")
    :   将标准函数添加到此[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")中。

        这相当于使用`+=`运算符就地修改[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")。

    *classmethod* `面包店`{.descname} （ *size = 200* ） [](#sqlalchemy.ext.baked.BakedQuery.bakery "Permalink to this definition")
    :   建造一个新的面包店。

    ` for_session  T0> （ T1> 会话 T2> ） T3> ¶ T4>`{.descname}
    :   为这个[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")返回一个[`Result`](#sqlalchemy.ext.baked.Result "sqlalchemy.ext.baked.Result")对象。

        这相当于将[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")作为Python可调用对象来调用。
        `结果 = my_baked_query（会话）`。

    `弃土 T0> （ T1> 满=假 T2> ） T3> ¶ T4>`{.descname}
    :   取消将在此BakedQuery对象上发生的任何查询缓存。

        BakedQuery可以继续正常使用，但是其他创建函数不会被缓存；他们将在每次调用时被调用。

        这是为了支持构建烘焙查询的特定步骤使查询无法缓存的情况，例如依赖于某些不可缓存值的变体。

        参数：

        **full**[¶](#sqlalchemy.ext.baked.BakedQuery.spoil.params.full)
        – if False, only functions added to this [`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")
        object subsequent to the spoil step will be non-cached; the
        state of the [`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")
        up until this point will be pulled from the cache.
        如果为True，则每次从头创建整个[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，并在每次调用时调用所有创建函数。

     `with_criteria`{.descname}(*fn*, *\*args*)[¶](#sqlalchemy.ext.baked.BakedQuery.with_criteria "Permalink to this definition")
    :   向这个克隆的[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")添加一个标准函数。

        这相当于使用`+`运算符生成新的带有修改的[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")。

 *class*`sqlalchemy.ext.baked.`{.descclassname}`Result`{.descname}(*bq*, *session*)[¶](#sqlalchemy.ext.baked.Result "Permalink to this definition")
:   针对[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")调用[`BakedQuery`](#sqlalchemy.ext.baked.BakedQuery "sqlalchemy.ext.baked.BakedQuery")。

    [`Result`](#sqlalchemy.ext.baked.Result "sqlalchemy.ext.baked.Result")对象是实际的[`query.Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象被创建或从缓存中检索，针对目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，然后被调用为结果。

    `所有 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回所有行。

        相当于[`Query.all()`](query.html#sqlalchemy.orm.query.Query.all "sqlalchemy.orm.query.Query.all")。

    `第一 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回第一行。

        相当于[`Query.first()`](query.html#sqlalchemy.orm.query.Query.first "sqlalchemy.orm.query.Query.first")。

    `获得 T0> （ T1>  IDENT  T2> ） T3> ¶ T4>`{.descname}
    :   基于身份检索对象。

        相当于[`Query.get()`](query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")。

    `一个 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   只返回一个结果或引发异常。

        等同于[`Query.one()`](query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")。

    ` one_or_none  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回一个或零个结果，或引发多行异常。

        等同于[`Query.one_or_none()`](query.html#sqlalchemy.orm.query.Query.one_or_none "sqlalchemy.orm.query.Query.one_or_none")。

        版本1.0.9中的新功能

    `params`{.descname} （ *\* args*，*\*\* kw* ） [T5\>](#sqlalchemy.ext.baked.Result.params "Permalink to this definition")
    :   指定要替换到字符串SQL语句中的参数。

` sqlalchemy.ext.baked。 T0>  bake_lazy_loaders  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   为全系统的所有lazyloaders启用烘焙查询。

    这个操作对于所有懒惰的加载器应该是安全的，并且会减少这些操作的Python开销。

` sqlalchemy.ext.baked。 T0>  unbake_lazy_loaders  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
:   禁止在系统范围内为所有lazyloaders使用烘焙查询。

    该操作将恢复[`bake_lazy_loaders()`](#sqlalchemy.ext.baked.bake_lazy_loaders "sqlalchemy.ext.baked.bake_lazy_loaders")产生的更改。

` sqlalchemy.ext.baked。 T0>  baked_lazyload  T1> （ T2>  *键 T3> ） T4> ¶  T5>`{.descclassname}
:   指示应该使用加载中使用的“烘焙”查询使用“延迟”加载来加载给定属性。

` sqlalchemy.ext.baked。 T0>  baked_lazyload_all  T1> （ T2>  *键 T3> ） T4> ¶  T5>`{.descclassname}
:   为`orm.baked_lazyload()`生成一个独立的“全部”选项。

    从版本0.9.0开始弃用：“\_all()”样式被方法链接取代，例如：

        session.query(MyClass).options(
            baked_lazyload("someattribute").baked_lazyload("anotherattribute")
        )


