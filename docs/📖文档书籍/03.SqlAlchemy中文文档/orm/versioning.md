---
title: 配置版本计数器
date: 2021-02-20 22:41:49
permalink: /sqlalchemy/orm/versioning/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
tags:
---
配置版本计数器[¶](#configuring-a-version-counter "Permalink to this headline")
==============================================================================

[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")支持管理一个版本 id 列，它是一个单一表列，每增加一个`UPDATE`映射表发生。每次 ORM 针对该行发出`UPDATE`或`DELETE`时，都会检查该值，以确保内存中保存的值与数据库值匹配。

警告

由于版本控制功能依赖于比较对象的内存记录中的**，该功能仅适用于[`Session.flush()`](session_api.html#sqlalchemy.orm.session.Session.flush "sqlalchemy.orm.session.Session.flush")进程，内存行到数据库。**当使用[`Query.update()`](query.html#sqlalchemy.orm.query.Query.update "sqlalchemy.orm.query.Query.update")或[`Query.delete()`](query.html#sqlalchemy.orm.query.Query.delete "sqlalchemy.orm.query.Query.delete")方法执行多行 UPDATE 或 DELETE 时，**不会**生效，因为这些方法只发出 UPDATE 或 DELETE 语句，否则不能直接访问受影响的行的内容。

此功能的目的是检测两个并发事务何时大致同时修改同一行，或者在系统中提供防止使用“过时”行的警告，该行可能会重复使用来自以前的事务没有刷新（例如，如果使用[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")设置`expire_on_commit=False`，则可以重新使用来自先前事务的数据）。

并发交易更新

当检测到事务中的并发更新时，通常情况下数据库的事务隔离级别低于可重复读取的级别；否则，事务将不会暴露给由与本地更新值冲突的并发更新创建的新行值。在这种情况下，SQLAlchemy 版本控制功能通常对于事务内冲突检测没有用，尽管它仍然可以用于交叉事务过时检测。

执行可重复读取的数据库通常会针对并发更新锁定目标行，或者正在采用某种形式的多版本并发控制，以便在提交事务时发出错误。SQLAlchemy 的 version\_id\_col 是一个替代方案，它允许对事务中的特定表进行版本跟踪，否则可能没有设置此隔离级别。

也可以看看

[可重复读取隔离级别](http://www.postgresql.org/docs/9.1/static/transaction-iso.html#XACT-REPEATABLE-READ)
- Postgresql 的可重复读取实现，包括错误条件的描述。

简单版本计数[¶](#simple-version-counting "Permalink to this headline")
----------------------------------------------------------------------

跟踪版本最直接的方法是在映射表中添加一个整数列，然后在映射器选项中将其建立为`version_id_col`：

    class User(Base):plainplainplainplainplainplain
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        version_id = Column(Integer, nullable=False)
        name = Column(String(50), nullable=False)

        __mapper_args__ = {
            "version_id_col": version_id
        }

以上，`User`映​​射使用列`version_id`跟踪整数版本。当首先刷新`User`类型的对象时，`version_id`列将被赋予值“1”。然后，表中的 UPDATE 将始终以类似于以下的方式发出：

    UPDATE user SET version_id=:version_id, name=:nameplainplainplainplainplain
    WHERE user.id = :user_id AND user.version_id = :user_version_id
    {"name": "new name", "version_id": 2, "user_id": 1, "user_version_id": 1}

The above UPDATE statement is updating the row that not only matches
`user.id = 1`, it also is requiring that
`user.version_id = 1`, where “1” is the last version
identifier we’ve been known to use on this object.
如果某个事务独立修改了该行，则此版本 ID 将不再匹配，并且 UPDATE 语句将报告没有行匹配；这是 SQLAlchemy 测试的条件，只有一行符合我们的 UPDATE（或 DELETE）语句。如果零行匹配，则表明我们的数据版本已过时，并引发[`StaleDataError`](exceptions.html#sqlalchemy.orm.exc.StaleDataError "sqlalchemy.orm.exc.StaleDataError")。

自定义版本计数器/类型[¶](#custom-version-counters-types "Permalink to this headline")
-------------------------------------------------------------------------------------

其他类型的值或计数器可用于版本控制。常见类型包括日期和 GUID。当使用替代类型或计数器方案时，SQLAlchemy 使用`version_id_generator`参数为此方案提供了一个钩子，该参数接受可调用的版本生成。该可调用函数传递当前已知版本的值，并且预计会返回后续版本。

例如，如果我们想使用随机生成的 GUID 跟踪我们的`User`类的版本控制，我们可以做到这一点（请注意，一些后端支持本地 GUID 类型，但我们在这里用一个简单的字符串）：

    import uuidplainplainplainplainplainplainplainplain

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        version_uuid = Column(String(32))
        name = Column(String(50), nullable=False)

        __mapper_args__ = {
            'version_id_col':version_uuid,
            'version_id_generator':lambda version: uuid.uuid4().hex
        }

每当`User`对象受到 INSERT 或 UPDATE 时，持久性引擎将调用`uuid.uuid4()`。在这种情况下，我们的版本生成函数可以忽略`version`的传入值，因为`uuid4()`函数生成没有任何先决条件值的标识符。如果我们使用数字或特殊字符系统等顺序版本方案，我们可以使用给定的`version`来帮助确定后续值。

也可以看看

[Backend-agnostic GUID Type](core_custom_types.html#custom-guid-type)

服务器端版本计数器[¶](#server-side-version-counters "Permalink to this headline")
---------------------------------------------------------------------------------

`version_id_generator`也可以配置为依赖数据库生成的值。在这种情况下，当一行受 INSERT 和 UPDATE 处理时，数据库将需要一些生成新标识符的方法。对于 UPDATE 情况，通常需要更新触发器，除非有问题的数据库支持其他本地版本标识符。Postgresql 数据库特别支持一个称为[xmin](http://www.postgresql.org/docs/9.1/static/ddl-system-columns.html)的系统列，它提供 UPDATE 版本控制。我们可以使用 Postgresql
`xmin`列对我们的`User`类进行版本化，如下所示：

    class User(Base):plainplainplainplainplainplainplainplain
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String(50), nullable=False)
        xmin = Column("xmin", Integer, system=True)

        __mapper_args__ = {
            'version_id_col': xmin,
            'version_id_generator': False
        }

通过上述映射，ORM 将依靠`xmin`列自动提供版本 id 计数器的新值。

创建引用系统列的表

In the above scenario, as `xmin` is a system column
provided by Postgresql, we use the `system=True`
argument to mark it as a system-provided column, omitted from the
`CREATE TABLE` statement.

ORM 通常不会在发出 INSERT 或 UPDATE 时主动获取数据库生成的值的值，而是将这些列保留为“过期”并在下次访问时将其提取出来，除非`eager_defaults` [`mapper()`](mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")标志被设置。但是，当使用服务器端版本列时，ORM 需要主动获取新生成的值。这是为了使版本计数器在之前设置*任何并发事务可以再次更新它。*这个抓取最好在 INSERT 或 UPDATE 语句中使用[RETURNING](glossary.html#term-returning)同时完成，否则如果之后发出 SELECT 语句，仍然存在潜在的竞争条件，版本计数器在获取之前可能会发生变化。

当目标数据库支持 RETURNING 时，我们的`User`类的 INSERT 语句如下所示：

    INSERT INTO "user" (name) VALUES (%(name)s) RETURNING "user".id, "user".xminplainplainplainplain
    {'name': 'ed'}

如上所述，ORM 可以在一个语句中获取任何新生成的主键值以及服务器生成的版本标识符。当后端不支持 RETURNING 时，必须为**每个**
INSERT 和 UPDATE 发出一个额外的 SELECT，效率低得多，并且还引入了错过版本计数器的可能性：

    INSERT INTO "user" (name) VALUES (%(name)s)plainplainplainplain
    {'name': 'ed'}

    SELECT "user".version_id AS user_version_id FROM "user" where
    "user".id = :param_1
    {"param_1": 1}

It is *strongly recommended* that server side version counters only be
used when absolutely necessary and only on backends that support
[RETURNING](glossary.html#term-returning), e.g. Postgresql, Oracle, SQL
Server (though SQL Server has [major
caveats](http://blogs.msdn.com/b/sqlprogrammability/archive/2008/07/11/update-with-output-clause-triggers-and-sqlmoreresults.aspx)
when triggers are used), Firebird.

版本 0.9.0 中的新功能：支持服务器端版本标识符跟踪。

编程或条件版本计数器[¶](#programmatic-or-conditional-version-counters "Permalink to this headline")
---------------------------------------------------------------------------------------------------

当`version_id_generator`设置为 False 时，我们也可以通过编程方式（和有条件地）在我们的对象上设置版本标识符，这与我们分配任何其他映射属性的方式相同。例如，如果我们使用我们的 UUID 示例，但将`version_id_generator`设置为`False`，则可以根据我们的选择设置版本标识符：

    import uuidplainplainplainplain

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        version_uuid = Column(String(32))
        name = Column(String(50), nullable=False)

        __mapper_args__ = {
            'version_id_col':version_uuid,
            'version_id_generator': False
        }

    u1 = User(name='u1', version_uuid=uuid.uuid4())

    session.add(u1)

    session.commit()

    u1.name = 'u2'
    u1.version_uuid = uuid.uuid4()

    session.commit()

我们可以在不增加版本计数器的情况下更新我们的`User`对象；计数器的值将保持不变，并且 UPDATE 语句仍然会检查以前的值。这对于只有某些类别的 UPDATE 对并发性问题敏感的方案可能很有用：

    # will leave version_uuid unchangedplainplainplainplainplainplain
    u1.name = 'u3'
    session.commit()

版本 0.9.0 中的新功能：支持编程式和条件版本标识符跟踪。
