---
title: 其他持久性技术
date: 2021-02-20 22:41:45
permalink: /sqlalchemy/orm/persistence_techniques/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - orm
tags:
  - 
---
其他持久性技术[¶](#additional-persistence-techniques "Permalink to this headline")
==================================================================================

将SQL插入/更新表达式嵌入到[¶](#embedding-sql-insert-update-expressions-into-a-flush "Permalink to this headline")中
-------------------------------------------------------------------------------------------------------------------

此功能允许将数据库列的值设置为SQL表达式而不是文字值。它对原子更新，调用存储过程等等特别有用。你所做的就是将一个表达式分配给一个属性：

    class SomeClass(object):
        pass
    mapper(SomeClass, some_table)

    someobject = session.query(SomeClass).get(5)

    # set 'value' attribute to a SQL expression adding one
    someobject.value = some_table.c.value + 1

    # issues "UPDATE some_table SET value=value+1"
    session.commit()

这种技术适用于INSERT和UPDATE语句。在flush /
commit操作之后，上面`someobject`中的`value`属性已过期，以便下次访问时，新生成的值将从数据库加载。

在会话中使用SQL表达式[¶](#using-sql-expressions-with-sessions "Permalink to this headline")
-------------------------------------------------------------------------------------------

SQL表达式和字符串可以通过事务上下文中的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")执行。This
is most easily accomplished using the [`execute()`](session_api.html#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
method, which returns a [`ResultProxy`](core_connections.html#sqlalchemy.engine.ResultProxy "sqlalchemy.engine.ResultProxy")
in the same manner as an [`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")
or [`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection"):

    Session = sessionmaker(bind=engine)
    session = Session()

    # execute a string statement
    result = session.execute("select * from table where id=:id", {'id':7})

    # execute a SQL expression construct
    result = session.execute(select([mytable]).where(mytable.c.id==7))

可以使用[`connection()`](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")方法访问由[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")保存的当前[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")

    connection = session.connection()

上面的例子处理了绑定到单个[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")或[`Connection`](core_connections.html#sqlalchemy.engine.Connection "sqlalchemy.engine.Connection")的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。To
execute statements using a [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
which is bound either to multiple engines, or none at all (i.e. relies
upon bound metadata), both [`execute()`](session_api.html#sqlalchemy.orm.session.Session.execute "sqlalchemy.orm.session.Session.execute")
and [`connection()`](session_api.html#sqlalchemy.orm.session.Session.connection "sqlalchemy.orm.session.Session.connection")
accept a `mapper` keyword argument, which is passed
a mapped class or [`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")
instance, which is used to locate the proper context for the desired
engine:

    Session = sessionmaker()
    session = Session()

    # need to specify mapper or class when executing
    result = session.execute("select * from table where id=:id", {'id':7}, mapper=MyMappedClass)

    result = session.execute(select([mytable], mytable.c.id==7), mapper=MyMappedClass)

    connection = session.connection(MyMappedClass)

在具有默认[¶](#forcing-null-on-a-column-with-a-default "Permalink to this headline")的列上强制NULL
--------------------------------------------------------------------------------------------------

ORM将任何从未在对象上设置的属性视为“默认”情况；该属性将从INSERT语句中省略：

    class MyObject(Base):
        __tablename__ = 'my_table'
        id = Column(Integer, primary_key=True)
        data = Column(String(50), nullable=True)

    obj = MyObject(id=1)
    session.add(obj)
    session.commit()  # INSERT with the 'data' column omitted; the database
                      # itself will persist this as the NULL value

Omitting a column from the INSERT means that the column will have the
NULL value set, *unless* the column has a default set up, in which case
the default value will be persisted.
这既适用于从服务器端默认的纯SQL透视角度，也适用于SQLAlchemy插入行为的客户端和服务器端默认行为：

    class MyObject(Base):
        __tablename__ = 'my_table'
        id = Column(Integer, primary_key=True)
        data = Column(String(50), nullable=True, server_default="default")

    obj = MyObject(id=1)
    session.add(obj)
    session.commit()  # INSERT with the 'data' column omitted; the database
                      # itself will persist this as the value 'default'

但是，在ORM中，即使将Python值`None`显式指定给对象，也会将该值视为**相同**，就好像该值从未分配过一样：

    class MyObject(Base):
        __tablename__ = 'my_table'
        id = Column(Integer, primary_key=True)
        data = Column(String(50), nullable=True, server_default="default")

    obj = MyObject(id=1, data=None)
    session.add(obj)
    session.commit()  # INSERT with the 'data' column explicitly set to None;
                      # the ORM still omits it from the statement and the
                      # database will still persist this as the value 'default'

即使传递了`None`，上面的操作仍会保留在`data`列的`"default"`的服务器默认值中，而不是SQL
NULL。这是ORM的一个长期存在的行为，许多应用程序都将其作为假设。

那么，如果我们想实际上将NULL放入此列，即使该列具有默认值，该怎么办呢？有两种方法。一个是在每个实例级别上，我们使用[`null`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")
SQL结构分配属性：

    from sqlalchemy import null

    obj = MyObject(id=1, data=null())
    session.add(obj)
    session.commit()  # INSERT with the 'data' column explicitly set as null();
                      # the ORM uses this directly, bypassing all client-
                      # and server-side defaults, and the database will
                      # persist this as the NULL value

[`null`](core_sqlelement.html#sqlalchemy.sql.expression.null "sqlalchemy.sql.expression.null")
SQL构造始终转换为直接存在于目标INSERT语句中的SQL NULL值。

If we’d like to be able to use the Python value `None` and have this also be persisted as NULL despite the presence
of column defaults, we can configure this for the ORM using a Core-level
modifier [`TypeEngine.evaluates_none()`](core_type_api.html#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none"),
which indicates a type where the ORM should treat the value
`None` the same as any other value and pass it
through, rather than omitting it as a “missing” value:

    class MyObject(Base):
        __tablename__ = 'my_table'
        id = Column(Integer, primary_key=True)
        data = Column(
          String(50).evaluates_none(),  # indicate that None should always be passed
          nullable=True, server_default="default")

    obj = MyObject(id=1, data=None)
    session.add(obj)
    session.commit()  # INSERT with the 'data' column explicitly set to None;
                      # the ORM uses this directly, bypassing all client-
                      # and server-side defaults, and the database will
                      # persist this as the NULL value

评估无

[`TypeEngine.evaluates_none()`](core_type_api.html#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")修饰符主要用于指示Python值“无”显着的类型，主要示例是可能要保留JSON的JSON类型`null`我们在这里略微重新调整它，以便向ORM发出信号，即使没有为其分配特殊的类型级别的行为，我们仍然希望将`None`传递到类型中。

版本1.1中的新增功能：添加了[`TypeEngine.evaluates_none()`](core_type_api.html#sqlalchemy.types.TypeEngine.evaluates_none "sqlalchemy.types.TypeEngine.evaluates_none")方法，以表明应将“无”值视为重要。

分区策略[¶](#partitioning-strategies "Permalink to this headline")
------------------------------------------------------------------

### 简单垂直分区[¶](#simple-vertical-partitioning "Permalink to this headline")

垂直分区在多个数据库中放置不同种类的对象或不同的表格：

    engine1 = create_engine('postgresql://db1')
    engine2 = create_engine('postgresql://db2')

    Session = sessionmaker(twophase=True)

    # bind User operations to engine 1, Account operations to engine 2
    Session.configure(binds={User:engine1, Account:engine2})

    session = Session()

以上，针对任何一类的操作都会使用链接到该类的[`Engine`](core_connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")。在刷新操作后，将执行类似的规则以确保将每个类写入正确的数据库。

如果底层后端支持它，则多个数据库之间的事务可以通过两阶段提交进行协调。举例来说，请参阅[Enabling
Two-Phase Commit](session_transaction.html#session-twophase)。

### 自定义垂直分区[¶](#custom-vertical-partitioning "Permalink to this headline")

通过覆盖[`Session.get_bind()`](session_api.html#sqlalchemy.orm.session.Session.get_bind "sqlalchemy.orm.session.Session.get_bind")方法可以构建更全面的基于规则的类级别分区。下面我们举例说明一个自定义的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，它提供了以下规则：

1.  刷新操作交付给名为`master`的引擎。
2.  对`MyOtherClass`子类的对象的操作都发生在`other`引擎上。
3.  Read operations for all other classes occur on a random choice of
    the `slave1` or `slave2`
    database.

<!-- -->

    engines = {
        'master':create_engine("sqlite:///master.db"),
        'other':create_engine("sqlite:///other.db"),
        'slave1':create_engine("sqlite:///slave1.db"),
        'slave2':create_engine("sqlite:///slave2.db"),
    }

    from sqlalchemy.orm import Session, sessionmaker
    import random

    class RoutingSession(Session):
        def get_bind(self, mapper=None, clause=None):
            if mapper and issubclass(mapper.class_, MyOtherClass):
                return engines['other']
            elif self._flushing:
                return engines['master']
            else:
                return engines[
                    random.choice(['slave1','slave2'])
                ]

上面的[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")类使用`class_`参数插入到[`sessionmaker`](session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker")中：

    Session = sessionmaker(class_=RoutingSession)

这种方法可以与多个[`MetaData`](core_metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象结合使用，例如使用[\_\_abstract\_\_](extensions_declarative_api.html#declarative-abstract)中描述的声明性`__abstract__`关键字的方法。

### 水平分区[¶](#horizontal-partitioning "Permalink to this headline")

水平分区跨多个数据库分割单个表（或一组表）。

请参阅“分片”示例：[Horizontal
Sharding](examples.html#examples-sharding)。

批量操作[¶](#bulk-operations "Permalink to this headline")
----------------------------------------------------------

注意

批量操作模式是在[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象上提供的一系列新操作，用于调用INSERT和UPDATE语句，大大减少了Python的开销，代价是功能少，自动化和错误检查。从SQLAlchemy
1.0开始，这些功能应该被视为“测试版”，另外还适用于高级用户。

版本1.0.0中的新功能

对[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的批量操作包括[`Session.bulk_save_objects()`](session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects "sqlalchemy.orm.session.Session.bulk_save_objects")，[`Session.bulk_insert_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")和[`Session.bulk_update_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")这些方法的目的是直接暴露工作单位系统的内部元素，这样可以单独利用发出给予字典或对象状态的INSERT和UPDATE语句的设施，绕过正常的工作状态机制，关系和属性管理。这种方法的优点严格限制了Python的开销之一：

-   flush()过程包括所有对象的调查，状态，级联状态，通过[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")关联的所有对象的状态，以及要执行的所有操作的拓扑排序完全被绕过。这减少了大量的Python开销。
-   即使操作完成，给定的对象与目标[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")之间也没有定义关系，这意味着根据标识映射或会话在连接它们或管理它们的状态时没有任何开销。
-   [`Session.bulk_insert_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")和[`Session.bulk_update_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")方法接受普通Python字典的列表，而不是对象；这进一步减少了与实例化映射对象以及为它们分配状态相关的大量开销，这通常还要以每个属性为基础对历史进行昂贵的跟踪。
-   在INSERT之后获取主键的过程也被默认禁用。当正确执行时，INSERT语句现在可以更容易地被工作单元批处理成`executemany()`块，它比单独的语句调用执行得更好。
-   UPDATE语句可以类似地进行定制，使所有属性无条件地服从SET语句，同样可以使用`executemany()`块。

应该使用[Performance](examples.html#examples-performance)示例套件研究批量例程的性能行为。这是一系列示例脚本，它们演示了各种场景下的Python调用计数，包括批量插入和更新场景。

也可以看看

[Performance](examples.html#examples-performance) - includes detailed
examples of bulk operations contrasted against traditional Core and ORM
methods, including performance metrics.

### 用法[¶ T0\>](#usage "Permalink to this headline")

每个方法都在[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")对象事务的上下文中工作，就像任何其他方法一样：

    s = Session()
    objects = [
        User(name="u1"),
        User(name="u2"),
        User(name="u3")
    ]
    s.bulk_save_objects(objects)

对于[`Session.bulk_insert_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")和[`Session.bulk_update_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")，传递字典：

    s.bulk_insert_mappings(User,
      [dict(name="u1"), dict(name="u2"), dict(name="u3")]
    )

也可以看看

[`Session.bulk_save_objects()`](session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects "sqlalchemy.orm.session.Session.bulk_save_objects")

[`Session.bulk_insert_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings "sqlalchemy.orm.session.Session.bulk_insert_mappings")

[`Session.bulk_update_mappings()`](session_api.html#sqlalchemy.orm.session.Session.bulk_update_mappings "sqlalchemy.orm.session.Session.bulk_update_mappings")

### 与核心插入/更新构造比较[¶](#comparison-to-core-insert-update-constructs "Permalink to this headline")

批量方法提供的性能在特定情况下可以接近在“executemany”上下文中使用核心[`Insert`](core_dml.html#sqlalchemy.sql.expression.Insert "sqlalchemy.sql.expression.Insert")和[`Update`](core_dml.html#sqlalchemy.sql.expression.Update "sqlalchemy.sql.expression.Update")结构的性能（有关“executemany”
，请参阅Core教程中的[Executing Multiple
Statements](core_tutorial.html#execute-multiple)）。为了实现这一点，应禁用[`Session.bulk_insert_mappings.return_defaults`](session_api.html#sqlalchemy.orm.session.Session.bulk_insert_mappings.params.return_defaults "sqlalchemy.orm.session.Session.bulk_insert_mappings")标志，以便可以将行组合在一起。应仔细研究[Performance](examples.html#examples-performance)中的示例套件，以便熟悉可以实现批量性能的快速程度。

### ORM兼容性[¶](#orm-compatibility "Permalink to this headline")

与传统的ORM使用相比，批量插入/更新方法失去了大量的功能。以下是使用这些方法时**不可用**的功能列表：

-   沿着[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")链接持久化
-   依赖性顺序排序行；行将按照它们传递给方法的顺序直接插入或更新
-   对给定对象的会话管理，包括对会话的附件，身份映射管理。
-   与主键突变，ON UPDATE级联有关的功能
-   SQL表达式插入/更新（例如[Embedding SQL Insert/Update Expressions
    into a Flush](#flush-embedded-sql-expressions)中）
-   ORM事件，如[`MapperEvents.before_insert()`](events.html#sqlalchemy.orm.events.MapperEvents.before_insert "sqlalchemy.orm.events.MapperEvents.before_insert")等。批量会话方法没有事件支持。

**可用的功能**包括：

-   映射对象的INSERT和UPDATE
-   版本标识符支持
-   多表映射（如连接继承） -
    但是，要插入多个表的对象要么提前完全填充主键标识符，否则[`Session.bulk_save_objects.return_defaults`](session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects.params.return_defaults "sqlalchemy.orm.session.Session.bulk_save_objects")标志必须被使用，这将大大降低性能的好处

