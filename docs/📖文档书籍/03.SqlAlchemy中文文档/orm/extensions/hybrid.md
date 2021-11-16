---
title: 混合属性
date: 2021-02-20 22:41:42
permalink: /sqlalchemy/orm/extensions/hybrid/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
tags:
---
混合属性[¶](#module-sqlalchemy.ext.hybrid "Permalink to this headline")
=======================================================================

在具有“混合”行为的 ORM 映射类上定义属性。

“混合”意味着属性在类级和实例级定义了不同的行为。

[`hybrid`](#module-sqlalchemy.ext.hybrid "sqlalchemy.ext.hybrid")扩展提供了特殊形式的方法装饰器，大约有 50 行代码，并且几乎不依赖于 SQLAlchemy 的其余部分。理论上，它可以与任何基于描述符的表达系统一起工作。

考虑映射`Interval`，表示整数`start`和`end`值。我们可以在映射类上定义更高级别的函数，这些类可以在类级别生成 SQL 表达式，也可以在实例级别上进行 Python 表达式评估。下面，用[`hybrid_method`](#sqlalchemy.ext.hybrid.hybrid_method "sqlalchemy.ext.hybrid.hybrid_method")或[`hybrid_property`](#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")装饰的每个函数都可以接收`self`作为类的实例，或者作为类本身：

    from sqlalchemy import Column, Integer
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import Session, aliased
    from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

    Base = declarative_base()

    class Interval(Base):
        __tablename__ = 'interval'

        id = Column(Integer, primary_key=True)
        start = Column(Integer, nullable=False)
        end = Column(Integer, nullable=False)

        def __init__(self, start, end):
            self.start = start
            self.end = end

        @hybrid_property
        def length(self):
            return self.end - self.start

        @hybrid_method
        def contains(self, point):
            return (self.start <= point) & (point <= self.end)

        @hybrid_method
        def intersects(self, other):
            return self.contains(other.start) | self.contains(other.end)

以上，`length`属性返回`end`和`start`属性之间的差异。使用`Interval`的实例，使用正常的 Python 描述符机制，在 Python 中进行相减：

    >>> i1 = Interval(5, 10)plain
    >>> i1.length
    5

当处理`Interval`类本身时，[`hybrid_property`](#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")描述符将给定`Interval`类的函数体评估为参数，当使用 SQLAlchemy 表达式机制返回一个新的 SQL 表达式：

    >>> print Interval.length
    interval."end" - interval.start

    >>> print Session().query(Interval).filter(Interval.length > 10)
    SELECT interval.id AS interval_id, interval.start AS interval_start,
    interval."end" AS interval_end
    FROM interval
    WHERE interval."end" - interval.start > :param_1

ORM methods such as [`filter_by()`](query.html#sqlalchemy.orm.query.Query.filter_by "sqlalchemy.orm.query.Query.filter_by")
generally use `getattr()` to locate attributes, so
can also be used with hybrid attributes:

    >>> print Session().query(Interval).filter_by(length=5)
    SELECT interval.id AS interval_id, interval.start AS interval_start,
    interval."end" AS interval_end
    FROM interval
    WHERE interval."end" - interval.start = :param_1

`Interval`类示例还演示了`contains()`和`intersects()`两种方法，用[`hybrid_method`](#sqlalchemy.ext.hybrid.hybrid_method "sqlalchemy.ext.hybrid.hybrid_method")修饰。该装饰器将相同的想法应用于[`hybrid_property`](#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")应用于属性的方法。这些方法返回布尔值，并利用 Python
`|`和`&`位运算符来产生等效的实例级和 SQL 表达式级布尔行为：

    >>> i1.contains(6)
    True
    >>> i1.contains(15)
    False
    >>> i1.intersects(Interval(7, 18))
    True
    >>> i1.intersects(Interval(25, 29))
    False

    >>> print Session().query(Interval).filter(Interval.contains(15))
    SELECT interval.id AS interval_id, interval.start AS interval_start,
    interval."end" AS interval_end
    FROM interval
    WHERE interval.start <= :start_1 AND interval."end" > :end_1

    >>> ia = aliased(Interval)
    >>> print Session().query(Interval, ia).filter(Interval.intersects(ia))
    SELECT interval.id AS interval_id, interval.start AS interval_start,
    interval."end" AS interval_end, interval_1.id AS interval_1_id,
    interval_1.start AS interval_1_start, interval_1."end" AS interval_1_end
    FROM interval, interval AS interval_1
    WHERE interval.start <= interval_1.start
        AND interval."end" > interval_1.start
        OR interval.start <= interval_1."end"
        AND interval."end" > interval_1."end"

定义与属性行为不同的表达行为[¶](#defining-expression-behavior-distinct-from-attribute-behavior "Permalink to this headline")
----------------------------------------------------------------------------------------------------------------------------

我们使用上面的`&`和`|`位运算符是幸运的，考虑到我们的函数对两个布尔值进行操作以返回新函数。在许多情况下，Python 内函数和 SQLAlchemy
SQL 表达式的构造有足够的区别，应该定义两个单独的 Python 表达式。[`hybrid`](#module-sqlalchemy.ext.hybrid "sqlalchemy.ext.hybrid")装饰器为此定义了[`hybrid_property.expression()`](#sqlalchemy.ext.hybrid.hybrid_property.expression "sqlalchemy.ext.hybrid.hybrid_property.expression")修饰符。作为一个例子，我们将定义间隔的半径，这需要使用绝对值函数：

    from sqlalchemy import func

    class Interval(object):
        # ...

        @hybrid_property
        def radius(self):
            return abs(self.length) / 2

        @radius.expression
        def radius(cls):
            return func.abs(cls.length) / 2

Python 函数`abs()`用于实例级操作，SQL 函数`ABS()`通过[`func`](core_sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")对象用于类级表达式：

    >>> i1.radius
    2

    >>> print Session().query(Interval).filter(Interval.radius > 5)
    SELECT interval.id AS interval_id, interval.start AS interval_start,
        interval."end" AS interval_end
    FROM interval
    WHERE abs(interval."end" - interval.start) / :abs_1 > :param_1

定义 Setters [¶](#defining-setters "Permalink to this headline")
---------------------------------------------------------------

混合属性也可以定义 setter 方法。如果我们想在上面设置`length`，那么在修改端点值时：

    class Interval(object):
        # ...

        @hybrid_property
        def length(self):
            return self.end - self.start

        @length.setter
        def length(self, value):
            self.end = self.start + value

现在在 set 中调用`长度（self， value）`方法：

    >>> i1 = Interval(5, 10)plain
    >>> i1.length
    5
    >>> i1.length = 12
    >>> i1.end
    17

处理关系[¶](#working-with-relationships "Permalink to this headline")
---------------------------------------------------------------------

创建与相关对象（而不是基于列的数据）相结合的混合体时，没有本质区别。对不同表情的需求往往更大。我们将要说明的两个变体是“连接依赖”混合体和“相关子查询”混合体。

### 加入 - 从属关系混合[¶](#join-dependent-relationship-hybrid "Permalink to this headline")

考虑以下将`User`与`SavingsAccount`关联的声明性映射：

    from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.ext.hybrid import hybrid_property

    Base = declarative_base()

    class SavingsAccount(Base):
        __tablename__ = 'account'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
        balance = Column(Numeric(15, 5))

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)

        accounts = relationship("SavingsAccount", backref="owner")

        @hybrid_property
        def balance(self):
            if self.accounts:
                return self.accounts[0].balance
            else:
                return None

        @balance.setter
        def balance(self, value):
            if not self.accounts:
                account = Account(owner=self)
            else:
                account = self.accounts[0]
            account.balance = value

        @balance.expression
        def balance(cls):
            return SavingsAccount.balance

上述混合属性`balance`与此用户的帐户列表中的第一个`SavingsAccount`条目配合使用。Python 中的 getter /
setter 方法可以将`accounts`视为`self`上可用的 Python 列表。

但是，在表达级别上，预计`User`类将在适当的上下文中使用，以便存在对`SavingsAccount`的适当连接：

    >>> print Session().query(User, User.balance).\plain
    ...     join(User.accounts).filter(User.balance > 5000)
    SELECT "user".id AS user_id, "user".name AS user_name,
    account.balance AS account_balance
    FROM "user" JOIN account ON "user".id = account.user_id
    WHERE account.balance > :balance_1

但是请注意，虽然实例级访问器需要担心是否存在`self.accounts`，但这个问题在 SQL 表达式级别表达不同，我们基本上会使用外连接：

    >>> from sqlalchemy import or_plain
    >>> print (Session().query(User, User.balance).outerjoin(User.accounts).
    ...         filter(or_(User.balance < 5000, User.balance == None)))
    SELECT "user".id AS user_id, "user".name AS user_name,
    account.balance AS account_balance
    FROM "user" LEFT OUTER JOIN account ON "user".id = account.user_id
    WHERE account.balance <  :balance_1 OR account.balance IS NULL

### 相关子查询关系混合[¶](#correlated-subquery-relationship-hybrid "Permalink to this headline")

当然，我们可以放弃依赖封闭查询的连接用法，而支持相关的子查询，它可以被移植到单个列表达式中。相关的子查询更具可移植性，但通常在 SQL 级别执行得更差。使用在[Using
column\_property](mapped_sql_expr.html#mapper-column-property-sql-expressions)中说明的相同技术，我们可以调整我们的`SavingsAccount`示例以汇总*所有*个帐户的余额，并使用相关子查询列表达式：

    from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.ext.hybrid import hybrid_property
    from sqlalchemy import select, func

    Base = declarative_base()

    class SavingsAccount(Base):
        __tablename__ = 'account'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
        balance = Column(Numeric(15, 5))

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)

        accounts = relationship("SavingsAccount", backref="owner")

        @hybrid_property
        def balance(self):
            return sum(acc.balance for acc in self.accounts)

        @balance.expression
        def balance(cls):
            return select([func.sum(SavingsAccount.balance)]).\
                    where(SavingsAccount.user_id==cls.id).\
                    label('total_balance')

上面的配方会给我们提供一个相关的 SELECT 的`balance`列：

    >>> print s.query(User).filter(User.balance > 400)plain
    SELECT "user".id AS user_id, "user".name AS user_name
    FROM "user"
    WHERE (SELECT sum(account.balance) AS sum_1
    FROM account
    WHERE account.user_id = "user".id) > :param_1

构建自定义比较器[¶](#building-custom-comparators "Permalink to this headline")
------------------------------------------------------------------------------

混合财产还包括允许建造定制比较器的帮手。一个比较器对象允许您自定义每个 SQLAlchemy 表达式运算符的行为。当创建在 SQL 端具有一些高度特异性行为的自定义类型时，它们非常有用。

下面的示例类允许对名为`word_insensitive`的属性进行不区分大小写的比较：

    from sqlalchemy.ext.hybrid import Comparator, hybrid_propertyplain
    from sqlalchemy import func, Column, Integer, String
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class CaseInsensitiveComparator(Comparator):
        def __eq__(self, other):
            return func.lower(self.__clause_element__()) == func.lower(other)

    class SearchWord(Base):
        __tablename__ = 'searchword'
        id = Column(Integer, primary_key=True)
        word = Column(String(255), nullable=False)

        @hybrid_property
        def word_insensitive(self):
            return self.word.lower()

        @word_insensitive.comparator
        def word_insensitive(cls):
            return CaseInsensitiveComparator(cls.word)

以上，针对`word_insensitive`的 SQL 表达式会将`LOWER()`
SQL 函数应用于双方：

    >>> print Session().query(SearchWord).filter_by(word_insensitive="Trucks")
    SELECT searchword.id AS searchword_id, searchword.word AS searchword_word
    FROM searchword
    WHERE lower(searchword.word) = lower(:lower_1)

上面的`CaseInsensitiveComparator`实现了[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")接口的一部分。可以对所有比较操作（即，`eq`，`lt`，`gt`等）应用“强制”使用[`Operators.operate()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")：

    class CaseInsensitiveComparator(Comparator):
        def operate(self, op, other):
            return op(func.lower(self.__clause_element__()), func.lower(other))

混合价值对象[¶](#hybrid-value-objects "Permalink to this headline")
-------------------------------------------------------------------

在前面的例子中，如果我们要将`SearchWord`实例的`word_insensitive`属性与纯 Python 字符串进行比较，那么纯 Python 字符串不会被强制为小写字母
- 我们构建的`CaseInsensitiveComparator`，由`@word_insensitive.comparator`返回，仅适用于 SQL 方面。

自定义比较器的更全面的形式是构造*混合值对象*。该技术将目标值或表达式应用于值对象，然后在所有情况下由访问器返回值对象。值对象允许控制值的所有操作以及如何处理比较值，无论是在 SQL 表达式还是 Python 值方面。用新的`CaseInsensitiveWord`类替换以前的`CaseInsensitiveComparator`类：

    class CaseInsensitiveWord(Comparator):
        "Hybrid value representing a lower case representation of a word."

        def __init__(self, word):
            if isinstance(word, basestring):
                self.word = word.lower()
            elif isinstance(word, CaseInsensitiveWord):
                self.word = word.word
            else:
                self.word = func.lower(word)

        def operate(self, op, other):
            if not isinstance(other, CaseInsensitiveWord):
                other = CaseInsensitiveWord(other)
            return op(self.word, other.word)

        def __clause_element__(self):
            return self.word

        def __str__(self):
            return self.word

        key = 'word'
        "Label to apply to Query tuple results"

Above, the `CaseInsensitiveWord` object represents
`self.word`, which may be a SQL function, or may be
a Python native. 通过重写`operate()`和`__clause_element__()`以根据`self.word`工作，所有比较操作都将针对“转换后” `word`，无论是 SQL 端还是 Python 端。我们的`SearchWord`类现在可以无条件地从单个混合调用中提供`CaseInsensitiveWord`对象：

    class SearchWord(Base):
        __tablename__ = 'searchword'
        id = Column(Integer, primary_key=True)
        word = Column(String(255), nullable=False)

        @hybrid_property
        def word_insensitive(self):
            return CaseInsensitiveWord(self.word)

`word_insensitive`属性现在普遍具有不区分大小写的比较行为，包括 SQL 表达式与 Python 表达式（请注意，Python 值在此处转换为小写）：

    >>> print Session().query(SearchWord).filter_by(word_insensitive="Trucks")
    SELECT searchword.id AS searchword_id, searchword.word AS searchword_word
    FROM searchword
    WHERE lower(searchword.word) = :lower_1

SQL 表达式与 SQL 表达式：

    >>> sw1 = aliased(SearchWord)
    >>> sw2 = aliased(SearchWord)
    >>> print Session().query(
    ...                    sw1.word_insensitive,
    ...                    sw2.word_insensitive).\
    ...                        filter(
    ...                            sw1.word_insensitive > sw2.word_insensitive
    ...                        )
    SELECT lower(searchword_1.word) AS lower_1,
    lower(searchword_2.word) AS lower_2
    FROM searchword AS searchword_1, searchword AS searchword_2
    WHERE lower(searchword_1.word) > lower(searchword_2.word)

仅 Python 表达式：

    >>> ws1 = SearchWord(word="SomeWord")plain
    >>> ws1.word_insensitive == "sOmEwOrD"
    True
    >>> ws1.word_insensitive == "XOmEwOrX"
    False
    >>> print ws1.word_insensitive
    someword

对于任何可能具有多种表示形式（例如时间戳，时间差，测量单位，货币和加密密码）的值，“混合值”模式都非常有用。

也可以看看

[杂种和价值不可知类型](http://techspot.zzzeek.org/2011/10/21/hybrids-and-value-agnostic-types/)
- 在 techspot.zzzeek.org 博客上

[价值不可知论类型，第二部分](http://techspot.zzzeek.org/2011/10/29/value-agnostic-types-part-ii/)
- 在 techspot.zzzeek.org 博客上

建立变形金刚[¶](#building-transformers "Permalink to this headline")
--------------------------------------------------------------------

一个*转换器*是一个可以接收[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象并返回一个新对象的对象。[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象包含一个方法[`with_transformation()`](query.html#sqlalchemy.orm.query.Query.with_transformation "sqlalchemy.orm.query.Query.with_transformation")，该方法返回由给定函数转换的新的[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")。

我们可以将它和[`Comparator`](#sqlalchemy.ext.hybrid.Comparator "sqlalchemy.ext.hybrid.Comparator")类结合起来，生成一种类型的配方，既可以设置查询的 FROM 子句，也可以指定过滤条件。

考虑一个映射的类`Node`，它将使用邻接表进行汇编成一个分层树形模式：

    from sqlalchemy import Column, Integer, ForeignKey
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    class Node(Base):
        __tablename__ = 'node'
        id =Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        parent = relationship("Node", remote_side=id)

Suppose we wanted to add an accessor `grandparent`.
这将返回`Node.parent`的`parent`。当我们有一个`Node`的实例时，这很简单：

    from sqlalchemy.ext.hybrid import hybrid_property

    class Node(Base):
        # ...

        @hybrid_property
        def grandparent(self):
            return self.parent.parent

对于表达，事情并不清楚。We’d need to construct a [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
where we [`join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")
twice along `Node.parent` to get to the
`grandparent`.
我们可以返回一个转换可调用对象，我们将与[`Comparator`](#sqlalchemy.ext.hybrid.Comparator "sqlalchemy.ext.hybrid.Comparator")类结合使用来接收任何[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象，并返回一个与`Node.parent`属性，并根据给定的标准进行过滤：

    from sqlalchemy.ext.hybrid import Comparator

    class GrandparentTransformer(Comparator):
        def operate(self, op, other):
            def transform(q):
                cls = self.__clause_element__()
                parent_alias = aliased(cls)
                return q.join(parent_alias, cls.parent).\
                            filter(op(parent_alias.parent, other))
            return transform

    Base = declarative_base()

    class Node(Base):
        __tablename__ = 'node'
        id =Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('node.id'))
        parent = relationship("Node", remote_side=id)

        @hybrid_property
        def grandparent(self):
            return self.parent.parent

        @grandparent.comparator
        def grandparent(cls):
            return GrandparentTransformer(cls)

`GrandparentTransformer`覆盖[`Comparator`](#sqlalchemy.ext.hybrid.Comparator "sqlalchemy.ext.hybrid.Comparator")层次结构的核心[`Operators.operate()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")方法以返回查询转换可调用，然后运行在特定情况下给定的比较操作。Such
as, in the example above, the `operate` method is
called, given the `Operators.eq`
callable as well as the right side of the comparison
`Node(id=5)`. 然后返回一个函数`transform`，它将首先转换[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")以加入到`Node.parent`，然后比较`parent_alias`
\>在左侧和右侧使用`Operators.eq`，传入`Query.filter`：

    >>> from sqlalchemy.orm import Session
    >>> session = Session()
    sql>>> session.query(Node).\
    ...        with_transformation(Node.grandparent==Node(id=5)).\
    ...        all()
    SELECT node.id AS node_id, node.parent_id AS node_parent_id
    FROM node JOIN node AS node_1 ON node_1.id = node.parent_id
    WHERE :param_1 = node_1.parent_id

我们可以通过从“过滤器”步骤中分离“连接”步骤来修改模式，使其更加冗长但灵活。The
tricky part here is ensuring that successive instances of
`GrandparentTransformer` use the same
[`AliasedClass`](query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")
object against `Node`.
下面我们使用一个简单的记忆方法，将一个`GrandparentTransformer`与每个类关联起来：

    class Node(Base):plain

        # ...

        @grandparent.comparator
        def grandparent(cls):
            # memoize a GrandparentTransformer
            # per class
            if '_gp' not in cls.__dict__:
                cls._gp = GrandparentTransformer(cls)
            return cls._gp

    class GrandparentTransformer(Comparator):

        def __init__(self, cls):
            self.parent_alias = aliased(cls)

        @property
        def join(self):
            def go(q):
                return q.join(self.parent_alias, Node.parent)
            return go

        def operate(self, op, other):
            return op(self.parent_alias.parent, other)

    sql>>> session.query(Node).\
    ...            with_transformation(Node.grandparent.join).\
    ...            filter(Node.grandparent==Node(id=5))
    SELECT node.id AS node_id, node.parent_id AS node_parent_id
    FROM node JOIN node AS node_1 ON node_1.id = node.parent_id
    WHERE :param_1 = node_1.parent_id

“变压器”模式是一种开始使用一些功能性编程范例的实验模式。虽然它只推荐给高级和/或耐心的开发人员，但它可能有很多令人惊奇的事情可用。

API 参考[¶](#api-reference "Permalink to this headline")
-------------------------------------------------------

 *class*`sqlalchemy.ext.hybrid.`{.descclassname}`hybrid_method`{.descname}(*func*, *expr=None*)[¶](#sqlalchemy.ext.hybrid.hybrid_method "Permalink to this definition")
:   基础：[`sqlalchemy.orm.base.InspectionAttrInfo`](internals.html#sqlalchemy.orm.base.InspectionAttrInfo "sqlalchemy.orm.base.InspectionAttrInfo")

    一个装饰器，允许定义具有实例级和类级行为的Python对象方法。

    `__ init __`{.descname} （ *func*，*expr = None* ） [t5 \>](#sqlalchemy.ext.hybrid.hybrid_method.__init__ "Permalink to this definition")
    :   创建一个新的[`hybrid_method`](#sqlalchemy.ext.hybrid.hybrid_method "sqlalchemy.ext.hybrid.hybrid_method")。

        用法通常是通过装饰器：

            from sqlalchemy.ext.hybrid import hybrid_method

            class SomeClass(object):
                @hybrid_method
                def value(self, x, y):
                    return self._value + x + y

                @value.expression
                def value(self, x, y):
                    return func.some_function(self._value, x, y)

    `表达 T0> （ T1>  EXPR  T2> ） T3> ¶ T4>`{.descname}
    :   提供定义SQL表达式生成方法的修改装饰器。

*类 T0\> `sqlalchemy.ext.hybrid。 T1>  hybrid_property  T2> （ T3>  fget  T4>， FSET = None，fdel = None，expr = None ） ¶`{.descclassname}*
:   基础：[`sqlalchemy.orm.base.InspectionAttrInfo`](internals.html#sqlalchemy.orm.base.InspectionAttrInfo "sqlalchemy.orm.base.InspectionAttrInfo")

    一个装饰器，允许定义具有实例级别和类级别行为的Python描述符。

     `__init__`{.descname}(*fget*, *fset=None*, *fdel=None*, *expr=None*)[¶](#sqlalchemy.ext.hybrid.hybrid_property.__init__ "Permalink to this definition")
    :   创建一个新的[`hybrid_property`](#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")。

        用法通常是通过装饰器：

            from sqlalchemy.ext.hybrid import hybrid_property

            class SomeClass(object):
                @hybrid_property
                def value(self):
                    return self._value

                @value.setter
                def value(self, value):
                    self._value = value

    `比较 T0> （ T1> 比较 T2> ） T3> ¶ T4>`{.descname}
    :   提供定义自定义比较器生成方法的修改装饰器。

        装饰方法的返回值应该是[`Comparator`](#sqlalchemy.ext.hybrid.Comparator "sqlalchemy.ext.hybrid.Comparator")的一个实例。

    `删除器 T0> （ T1>  FDEL  T2> ） T3> ¶ T4>`{.descname}
    :   提供定义值删除方法的修改装饰器。

    `表达 T0> （ T1>  EXPR  T2> ） T3> ¶ T4>`{.descname}
    :   提供定义SQL表达式生成方法的修改装饰器。

    `设定器 T0> （ T1>  FSET  T2> ） T3> ¶ T4>`{.descname}
    :   提供一个定义值设置器方法的修改装饰器。

 *class*`sqlalchemy.ext.hybrid.`{.descclassname}`Comparator`{.descname}(*expression*)[¶](#sqlalchemy.ext.hybrid.Comparator "Permalink to this definition")
:   基础：[`sqlalchemy.orm.interfaces.PropComparator`](internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

    一个辅助类，允许轻松构建用于混合使用的自定义[`PropComparator`](internals.html#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")类。

`sqlalchemy.ext.hybrid。`{.descclassname} `HYBRID_METHOD`{.descname} *=符号（'HYBRID\_METHOD'）* [¶](#sqlalchemy.ext.hybrid.HYBRID_METHOD "Permalink to this definition")
:   

`sqlalchemy.ext.hybrid。`{.descclassname} `HYBRID_PROPERTY`{.descname} *=符号（'HYBRID\_PROPERTY'）* [¶](#sqlalchemy.ext.hybrid.HYBRID_PROPERTY "Permalink to this definition")
:   

