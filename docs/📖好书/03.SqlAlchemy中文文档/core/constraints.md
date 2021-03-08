---
title: 定义约束和索引
date: 2021-02-20 22:41:33
permalink: /sqlalchemy/core/constraints/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - core
tags:
  - 
---
定义约束和索引[¶](#defining-constraints-and-indexes "Permalink to this headline")
=================================================================================

本节将讨论SQL
[constraints](glossary.html#term-constraints)和索引。在 SQLAlchemy 中，关键类包括[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")和[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")。

定义外键[¶](#defining-foreign-keys "Permalink to this headline")
----------------------------------------------------------------

SQL中的*外键*是表级结构，限制该表中的一个或多个列，使得值能存在不同列中，通常但不总是位于不同的表。我们调用了约束*外键*列的列和它们被约束到*引用的*列的列。被引用的列几乎总是为他们拥有的表定义主键，但也有例外。外键是将具有相互关系的行对连接在一起的“联合”，SQLAlchemy几乎在其操作的每个区域都非常重视这个概念。

在 SQLAlchemy 以及 DDL 中，可以将外键约束定义为 table 子句中的附加属性，或者对于单列外键，可以在单列的定义内指定外键约束。单列外键更常见，并且在列级别通过构建[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象作为[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的参数来指定：

    user_preference = Table('user_preference', metadata,plain
        Column('pref_id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
        Column('pref_name', String(40), nullable=False),
        Column('pref_value', String(100))
    )

在上面，我们定义了一个新的表`user_preference`，其中每行必须在`user_id`列中包含一个值，该值也存在于`user`表的`user_id`列。

[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")的参数通常是*＆lt；
tablename＆gt；。＆lt； columnname＆gt；＆lt； /
t3＆gt；的形式的字符串，或者对于远程模式中的表或“所有者” form *＆lt；
schemaname＆gt；。＆lt； tablename＆gt；。＆lt；
columnname＆gt；*。*它也可能是一个实际的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，我们稍后会看到它是通过它的`c`集合从现有的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象进行访问的：

    ForeignKey(user.c.user_id)plain

使用字符串的好处在于，仅当第一次需要时才解析`user`和`user_preference`之间的 in-python 链接，以便可以将表对象轻松地分布到多个模块中，按任何顺序定义。

外键也可以使用[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象在表级定义。该对象可以描述单列或多列外键。多列外键称为*复合*外键，并且几乎总是引用具有复合主键的表。下面我们定义一个表`invoice`，它有一个复合主键：

    invoice = Table('invoice', metadata,
        Column('invoice_id', Integer, primary_key=True),
        Column('ref_num', Integer, primary_key=True),
        Column('description', String(60), nullable=False)
    )

然后使用引用`invoice`的复合外键的表`invoice_item`：

    invoice_item = Table('invoice_item', metadata,
        Column('item_id', Integer, primary_key=True),
        Column('item_name', String(60), nullable=False),
        Column('invoice_id', Integer, nullable=False),
        Column('ref_num', Integer, nullable=False),
        ForeignKeyConstraint(['invoice_id', 'ref_num'], ['invoice.invoice_id', 'invoice.ref_num'])
    )

值得注意的是，[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")是定义组合外键的唯一方法。虽然我们也可以在`invoice_item.invoice_id`和`invoice_item.ref_num`列上放置单个[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象，但 SQLAlchemy 不会意识到这两个值应该配对在一起
- 这将是两个单独的外键约束，而不是引用两列的单个组合外键。

### 通过 ALTER 创建/删除外键约束[](#creating-dropping-foreign-key-constraints-via-alter "Permalink to this headline")

我们在教程和其他地方看到的涉及 DDL 外键的行为表明，约束通常在 CREATE
TABLE 语句内呈现为“内联”，如：

    CREATE TABLE addresses (
        id INTEGER NOT NULL,
        user_id INTEGER,
        email_address VARCHAR NOT NULL,
        PRIMARY KEY (id),
        CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users (id)
    )

使用`CONSTRAINT .. FOREIGN KEY在CREATE TABLE定义中“内联”的方式。`The [`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
and [`MetaData.drop_all()`](metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")
methods do this by default, using a topological sort of all the
[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
objects involved such that tables are created and dropped in order of
their foreign key dependency (this sort is also available via the
[`MetaData.sorted_tables`](metadata.html#sqlalchemy.schema.MetaData.sorted_tables "sqlalchemy.schema.MetaData.sorted_tables")
accessor).

这种方法在两个或更多外键约束涉及“依赖周期”的情况下无法工作，其中一组表彼此相互依赖，假设后端强制执行外键（除 SQLite，MySQL
/
MyISAM 数据）。因此，这些方法将在这种循环中将约束分解为单独的 ALTER 语句，而不是支持大多数 ALTER 形式的 SQLite 以外的所有后端。给定一个模式如下：

    node = Table(
        'node', metadata,
        Column('node_id', Integer, primary_key=True),
        Column(
            'primary_element', Integer,
            ForeignKey('element.element_id')
        )
    )

    element = Table(
        'element', metadata,
        Column('element_id', Integer, primary_key=True),
        Column('parent_node_id', Integer),
        ForeignKeyConstraint(
            ['parent_node_id'], ['node.node_id'],
            name='fk_element_parent_node_id'
        )
    )

当我们在后端（如 Postgresql 后端）上调用[`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")时，解析这两个表之间的循环并分别创建约束：

    >>> with engine.connect() as conn:plain
    ...    metadata.create_all(conn, checkfirst=False)
    CREATE TABLE element (
        element_id SERIAL NOT NULL,
        parent_node_id INTEGER,
        PRIMARY KEY (element_id)
    )

    CREATE TABLE node (
        node_id SERIAL NOT NULL,
        primary_element INTEGER,
        PRIMARY KEY (node_id)
    )

    ALTER TABLE element ADD CONSTRAINT fk_element_parent_node_id
        FOREIGN KEY(parent_node_id) REFERENCES node (node_id)
    ALTER TABLE node ADD FOREIGN KEY(primary_element)
        REFERENCES element (element_id)

为了为这些表发出 DROP，应用相同的逻辑，但请注意，在 SQL 中，要发出 DROP
CONSTRAINT，需要该约束具有名称。在上面的`'node'`表中，我们没有命名这个约束；系统将因此尝试仅为那些被命名的约束发出DROP：

    >>> with engine.connect() as conn:
    ...    metadata.drop_all(conn, checkfirst=False)
    ALTER TABLE element DROP CONSTRAINT fk_element_parent_node_id
    DROP TABLE node
    DROP TABLE element

在循环无法解析的情况下，例如，如果我们没有在这里为任一约束应用名称，我们将收到以下错误：

    sqlalchemy.exc.CircularDependencyError: Can't sort tables for DROP;
    an unresolvable foreign key dependency exists between tables:
    element, node.  Please ensure that the ForeignKey and ForeignKeyConstraint
    objects involved in the cycle have names so that they can be dropped
    using DROP CONSTRAINT.

这个错误只适用于DROP情况，因为我们可以在没有名字的CREATE情况下发出“ADD
CONSTRAINT”；数据库通常自动分配一个。

可以使用[`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")和[`ForeignKey.use_alter`](#sqlalchemy.schema.ForeignKey.params.use_alter "sqlalchemy.schema.ForeignKey")关键字参数来手动解决依赖关系周期。我们只能将这个标志添加到`'element'`表中，如下所示：

    element = Table(
        'element', metadata,
        Column('element_id', Integer, primary_key=True),
        Column('parent_node_id', Integer),
        ForeignKeyConstraint(
            ['parent_node_id'], ['node.node_id'],
            use_alter=True, name='fk_element_parent_node_id'
        )
    )

在我们的 CREATE DDL 中，我们将只看到这个约束的 ALTER 语句，而不是另一个：

    >>> with engine.connect() as conn:
    ...    metadata.create_all(conn, checkfirst=False)
    CREATE TABLE element (
        element_id SERIAL NOT NULL,
        parent_node_id INTEGER,
        PRIMARY KEY (element_id)
    )

    CREATE TABLE node (
        node_id SERIAL NOT NULL,
        primary_element INTEGER,
        PRIMARY KEY (node_id),
        FOREIGN KEY(primary_element) REFERENCES element (element_id)
    )

    ALTER TABLE element ADD CONSTRAINT fk_element_parent_node_id
    FOREIGN KEY(parent_node_id) REFERENCES node (node_id)

[`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")
and [`ForeignKey.use_alter`](#sqlalchemy.schema.ForeignKey.params.use_alter "sqlalchemy.schema.ForeignKey"),
when used in conjunction with a drop operation, will require that the
constraint is named, else an error like the following is generated:

    sqlalchemy.exc.CompileError: Can't emit DROP CONSTRAINT for constraint
    ForeignKeyConstraint(...); it has no name

Changed in version 1.0.0: - The DDL system invoked by
[`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
and [`MetaData.drop_all()`](metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")
will now automatically resolve mutually depdendent foreign keys between
tables declared by [`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
and [`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
objects, without the need to explicitly set the
[`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")
flag.

版本1.0.0中已更改： - [`ForeignKeyConstraint.use_alter`(#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")标志可与未命名的约束一起使用；实际调用时，只有DROP操作会发出特定的错误。

也可以看看

[Configuring Constraint Naming
Conventions](#constraint-naming-conventions)

[`sort_tables_and_constraints()`](ddl.html#sqlalchemy.schema.sort_tables_and_constraints "sqlalchemy.schema.sort_tables_and_constraints")

### ON UPDATE 和 ON DELETE [¶](#on-update-and-on-delete "Permalink to this headline")

Most databases support *cascading* of foreign key values, that is the
when a parent row is updated the new value is placed in child rows, or
when the parent row is deleted all corresponding child rows are set to
null or deleted. 在数据定义语言中，这些使用诸如“ON UPDATE CASCADE”，“ON
DELETE CASCADE”和“ON DELETE SET
NULL”之类的短语来指定，这与外键约束对应。“ON UPDATE”或“ON
DELETE”之后的短语也可能允许其他特定于正在使用的数据库的短语。[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")和[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象支持通过`onupdate`和`ondelete`关键字参数生成此子句。该值是在适当的“ON UPDATE”或“ON
DELETE”短语后输出的任何字符串：

    child = Table('child', meta,plain
        Column('id', Integer,
                ForeignKey('parent.id', onupdate="CASCADE", ondelete="CASCADE"),
                primary_key=True
        )
    )

    composite = Table('composite', meta,
        Column('id', Integer, primary_key=True),
        Column('rev_id', Integer),
        Column('note_id', Integer),
        ForeignKeyConstraint(
                    ['rev_id', 'note_id'],
                    ['revisions.id', 'revisions.note_id'],
                    onupdate="CASCADE", ondelete="SET NULL"
        )
    )

请注意，这些子句在SQLite上不受支持，并且在与MySQL一起使用时需要`InnoDB`表。他们也可能不支持其他数据库。

UNIQUE约束[¶](#unique-constraint "Permalink to this headline")
--------------------------------------------------------------

使用[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")上的`unique`关键字，可以在单个列上匿名创建唯一约束。通过[`UniqueConstraint`](#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")表级构造创建明确命名的唯一约束和/或具有多个列的约束。

    from sqlalchemy import UniqueConstraint

    meta = MetaData()
    mytable = Table('mytable', meta,

        # per-column anonymous unique constraint
        Column('col1', Integer, unique=True),

        Column('col2', Integer),
        Column('col3', Integer),

        # explicit/composite unique constraint.  'name' is optional.
        UniqueConstraint('col2', 'col3', name='uix_1')
        )

CHECK约束[¶](#check-constraint "Permalink to this headline")
------------------------------------------------------------

检查约束可以被命名或未命名，可以使用[`CheckConstraint`](#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")结构在列或表级别创建。检查约束的文本直接传递到数据库，因此有限的“数据库无关”行为。列级检查约束通常只应引用它们所在的列，而表级约束可引用表中的任何列。

请注意，有些数据库不支持检查约束，如MySQL。

    from sqlalchemy import CheckConstraint

    meta = MetaData()
    mytable = Table('mytable', meta,

        # per-column CHECK constraint
        Column('col1', Integer, CheckConstraint('col1>5')),

        Column('col2', Integer),
        Column('col3', Integer),

        # table level CHECK constraint.  'name' is optional.
        CheckConstraint('col2 > col3 + 5', name='check1')
        )

    sqlmytable.create(engine)
    CREATE TABLE mytable (
        col1 INTEGER  CHECK (col1>5),
        col2 INTEGER,
        col3 INTEGER,
        CONSTRAINT check1  CHECK (col2 > col3 + 5)
    )

PRIMARY KEY约束[¶](#primary-key-constraint "Permalink to this headline")
------------------------------------------------------------------------

根据用[`Column.primary_key`](metadata.html#sqlalchemy.schema.Column.params.primary_key "sqlalchemy.schema.Column")标志标记的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象，任何[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象的主键约束都是隐式存在的。[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")对象提供对此约束的显式访问，其中包括直接配置的选项：

    from sqlalchemy import PrimaryKeyConstraint

    my_table = Table('mytable', metadata,
                Column('id', Integer),
                Column('version_id', Integer),
                Column('data', String(50)),
                PrimaryKeyConstraint('id', 'version_id', name='mytable_pk')
            )

也可以看看

[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
- detailed API documentation.

使用声明式ORM扩展时设置约束[¶](#setting-up-constraints-when-using-the-declarative-orm-extension "Permalink to this headline")
-----------------------------------------------------------------------------------------------------------------------------

[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")是 SQLAlchemy 核心结构，允许用户定义表格元数据，其中 SQLAlchemy
ORM 可以使用该元数据作为映射类别的目标。The
[Declarative](orm_extensions_declarative_index.html) extension allows
the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
object to be created automatically, given the contents of the table
primarily as a mapping of [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
objects.

要将表级约束对象（如[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")）应用于使用Declarative定义的表，请使用[Table
Configuration](orm_extensions_declarative_table_config.html#declarative-table-args)中介绍的`__table_args__`属性。

配置约束命名约定[¶](#configuring-constraint-naming-conventions "Permalink to this headline")
--------------------------------------------------------------------------------------------

关系数据库通常为所有约束和索引分配显式名称。在通常情况下，使用`CREATE TABLE`创建表，其中 CHECK，UNIQUE 和 PRIMARY
KEY 约束等约束与表定义时，数据库通常会有一个系统，在这个系统中，如果没有另外指定名称，名称会自动分配给这些约束。当使用诸如`ALTER TABLE`的命令在数据库中更改现有数据库表时，此命令通常需要为新约束指定明确的名称以及能够指定要删除或修改的现有约束的名称。

可以使用[`Constraint.name`](#sqlalchemy.schema.Constraint.params.name "sqlalchemy.schema.Constraint")参数明确命名约束，并为索引[`Index.name`](#sqlalchemy.schema.Index.params.name "sqlalchemy.schema.Index")参数指定约束。但是，在约束条件下，该参数是可选的。还有一些使用[`Column.unique`](metadata.html#sqlalchemy.schema.Column.params.unique "sqlalchemy.schema.Column")和[`Column.index`](metadata.html#sqlalchemy.schema.Column.params.index "sqlalchemy.schema.Column")参数来创建[`UniqueConstraint`](#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")和[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")未指定明确名称的对象。

更改现有表和约束的用例可以通过模式迁移工具（如[Alembic](http://alembic.zzzcomputing.com/)）来处理。然而，Alembic 和 SQLAlchemy 目前都没有为其中未指定名称的约束对象创建名称，导致能够更改现有约束的情况意味着必须对关系数据库使用的命名系统进行反向工程以自动分配名称或者必须小心确保所有约束都被命名。

与必须为所有[`Constraint`](#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")和[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象指定显式名称相反，可以使用事件构建自动命名方案。This
approach has the advantage that constraints will get a consistent naming
scheme without the need for explicit name parameters throughout the
code, and also that the convention takes place just as well for those
constraints and indexes produced by the [`Column.unique`(metadata.html#sqlalchemy.schema.Column.params.unique "sqlalchemy.schema.Column")
and [`Column.index`](metadata.html#sqlalchemy.schema.Column.params.index "sqlalchemy.schema.Column")
parameters. 从SQLAlchemy
0.9.2开始，这个基于事件的方法被包含在内，并且可以使用参数[`MetaData.naming_convention`](metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")进行配置。

[`MetaData.naming_convention`](metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")
refers to a dictionary which accepts the [`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
class or individual [`Constraint`](#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")
classes as keys, and Python string templates as values.
它也接受一系列的字符码作为替代键，即`"fk"`，`"pk"`，`"ix"`，`"ck"`，`"uq"`分别为外键，主键，索引，检查和唯一约束。无论何时约束或索引与此[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")对象关联，此字典中的字符串模板都没有给定的现有名称（包括一个现有名称可以进一步修饰的例外情况）。

适用于基本情况的示例命名约定如下所示：

    convention = {
      "ix": 'ix_%(column_0_label)s',
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s"
    }

    metadata = MetaData(naming_convention=convention)

The above convention will establish names for all constraints within the
target [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")
collection. 例如，我们可以观察创建未命名的[`UniqueConstraint`](#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")时产生的名称：

    >>> user_table = Table('user', metadata,plain
    ...                 Column('id', Integer, primary_key=True),
    ...                 Column('name', String(30), nullable=False),
    ...                 UniqueConstraint('name')
    ... )
    >>> list(user_table.constraints)[1].name
    'uq_user_name'

即使我们只使用[`Column.unique`](metadata.html#sqlalchemy.schema.Column.params.unique "sqlalchemy.schema.Column")标志，该功能也会生效：

    >>> user_table = Table('user', metadata,
    ...                  Column('id', Integer, primary_key=True),
    ...                  Column('name', String(30), nullable=False, unique=True)
    ...     )
    >>> list(user_table.constraints)[1].name
    'uq_user_name'

命名约定方法的一个关键优势是名称是在 Python 构建时建立的，而不是在 DDL 发布时。当使用 Alembic 的`--autogenerate`特性时，这种效果是，当生成新的迁移脚本时，命名约定将是显式的：

    def upgrade():
        op.create_unique_constraint("uq_user_name", "user", ["name"])

上面的`"uq_user_name"`字符串是从位于我们的元数据中的[`UniqueConstraint`](#sqlalchemy.schema.UniqueConstraint "sqlalchemy.schema.UniqueConstraint")对象中的`--autogenerate`复制的。

The default value for [`MetaData.naming_convention`(metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")
handles the long-standing SQLAlchemy behavior of assigning a name to a
[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index") object
that is created using the [`Column.index`](metadata.html#sqlalchemy.schema.Column.params.index "sqlalchemy.schema.Column")
parameter:

    >>> from sqlalchemy.sql.schema import DEFAULT_NAMING_CONVENTION
    >>> DEFAULT_NAMING_CONVENTION
    immutabledict({'ix': 'ix_%(column_0_label)s'})

The tokens available include `%(table_name)s`,
`%(referred_table_name)s`,
`%(column_0_name)s`, `%(column_0_label)s`, `%(column_0_key)s`,
`%(referred_column_0_name)s`, and
`%(constraint_name)s`; the documentation for
[`MetaData.naming_convention`](metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")
describes each individually.
通过在naming\_convention 字典中指定一个额外的标记和一个可调用标记，还可以添加新的标记。例如，如果我们想使用 GUID 方案来命名我们的外键约束，我们可以这样做：

    import uuidplain

    def fk_guid(constraint, table):
        str_tokens = [
            table.name,
        ] + [
            element.parent.name for element in constraint.elements
        ] + [
            element.target_fullname for element in constraint.elements
        ]
        guid = uuid.uuid5(uuid.NAMESPACE_OID, "_".join(str_tokens).encode('ascii'))
        return str(guid)

    convention = {
        "fk_guid": fk_guid,
        "ix": 'ix_%(column_0_label)s',
        "fk": "fk_%(fk_guid)s",
    }

上面，当我们创建一个新的[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")时，我们会得到一个名字如下：

    >>> metadata = MetaData(naming_convention=convention)

    >>> user_table = Table('user', metadata,
    ...         Column('id', Integer, primary_key=True),
    ...         Column('version', Integer, primary_key=True),
    ...         Column('data', String(30))
    ...     )
    >>> address_table = Table('address', metadata,
    ...        Column('id', Integer, primary_key=True),
    ...        Column('user_id', Integer),
    ...        Column('user_version_id', Integer)
    ...    )
    >>> fk = ForeignKeyConstraint(['user_id', 'user_version_id'],
    ...                ['user.id', 'user.version'])
    >>> address_table.append_constraint(fk)
    >>> fk.name
    fk_0cd51ab5-8d70-56e8-a83c-86661737766d

也可以看看

[`MetaData.naming_convention`](metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")
- for additional usage details as well as a listing of all available
naming components.

[The Importance of Naming
Constraints](http://alembic.zzzcomputing.com/en/latest/naming.html#tutorial-constraint-names "(in Alembic v0.8.7)")
- 在Alembic文档中。

版本0.9.2新增：添加了[`MetaData.naming_convention`(metadata.html#sqlalchemy.schema.MetaData.params.naming_convention "sqlalchemy.schema.MetaData")参数。

### 命名CHECK约束[¶](#naming-check-constraints "Permalink to this headline")

[`CheckConstraint`](#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")对象是针对任意 SQL 表达式配置的，该表达式可以包含任意数量的列，另外通常使用原始 SQL 字符串进行配置。因此，与[`CheckConstraint`](#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")一起使用的通用约定是我们期望该对象已经拥有一个名称的公约，然后我们使用其他约定元素对其进行了增强。A
typical convention is
`"ck_%(table_name)s_%(constraint_name)s"`:

    metadata = MetaData(plain
        naming_convention={"ck": "ck_%(table_name)s_%(constraint_name)s"}
    )

    Table('foo', metadata,
        Column('value', Integer),
        CheckConstraint('value > 5', name='value_gt_5')
    )

上表将生成名称`ck_foo_value_gt_5`：

    CREATE TABLE foo (
        value INTEGER,
        CONSTRAINT ck_foo_value_gt_5 CHECK (value > 5)
    )

[`CheckConstraint`](#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")还支持`%(columns_0_name)s`标记；我们可以通过确保我们在约束的表达式中使用[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")或[`sql.expression.column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")元素来使用它，或者通过声明与表格分开的约束：

    metadata = MetaData(
        naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"}
    )

    foo = Table('foo', metadata,
        Column('value', Integer)
    )

    CheckConstraint(foo.c.value > 5)

或通过内联使用[`sql.expression.column()`](sqlelement.html#sqlalchemy.sql.expression.column "sqlalchemy.sql.expression.column")：

    from sqlalchemy import column

    metadata = MetaData(
        naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"}
    )

    foo = Table('foo', metadata,
        Column('value', Integer),
        CheckConstraint(column('value') > 5)
    )

两者都会产生名称`ck_foo_value`：

    CREATE TABLE foo (
        value INTEGER,
        CONSTRAINT ck_foo_value CHECK (value > 5)
    )

通过扫描列对象的给定表达式来确定“列零”的名称。如果表达式存在多个列，则扫描确实使用确定性搜索，但表达式的结构将确定将哪个列标记为“列零”。

版本1.0.0新增： [`CheckConstraint`](#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")对象现在支持`column_0_name`命名约定令牌。

### 为布尔型，枚举型和其他架构类型配置命名[¶](#configuring-naming-for-boolean-enum-and-other-schema-types "Permalink to this headline")

[`SchemaType`](type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")类引用类型对象，例如[`Boolean`](type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")和[`Enum`](type_basics.html#sqlalchemy.types.Enum "sqlalchemy.types.Enum")，它们会生成伴随该类型的 CHECK 约束。通过发送“name”参数来最直接地设置约束的名字，例如，
[`Boolean.name`](type_basics.html#sqlalchemy.types.Boolean.params.name "sqlalchemy.types.Boolean")

    Table('foo', metadata,
        Column('flag', Boolean(name='ck_foo_flag'))
    )

命名约定功能也可以与这些类型结合使用，通常通过使用包含`%(constraint_name)s`的约定，然后将名称应用于类型：

    metadata = MetaData(
        naming_convention={"ck": "ck_%(table_name)s_%(constraint_name)s"}
    )

    Table('foo', metadata,
        Column('flag', Boolean(name='flag_bool'))
    )

上表将生成约束名称`ck_foo_flag_bool`：

    CREATE TABLE foo (
        flag BOOL,
        CONSTRAINT ck_foo_flag_bool CHECK (flag IN (0, 1))
    )

[`SchemaType`](type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")类使用特殊的内部符号，因此只能在 DDL 编译时确定命名约定。在 Postgresql 上，有一个本地的 BOOLEAN 类型，所以不需要[`Boolean`](type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")的CHECK约束；我们可以安全地设置一个没有名字的[`Boolean`](type_basics.html#sqlalchemy.types.Boolean "sqlalchemy.types.Boolean")类型，即使检查约束有一个命名约定。如果我们针对没有像 SQLite 或 MySQL 这样的本机 BOOLEAN 类型的数据库运行，只会为 CHECK 约束查阅此约定。

CHECK 约束还可以使用`column_0_name`标记，该标记与[`SchemaType`](type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")很好地配合使用，因为这些约束只有一列：

    metadata = MetaData(plain
        naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"}
    )

    Table('foo', metadata,
        Column('flag', Boolean())
    )

上述模式将产生：

    CREATE TABLE foo (
        flag BOOL,
        CONSTRAINT ck_foo_flag CHECK (flag IN (0, 1))
    )

版本 1.0 更改：不包含`%(constraint_name)s`的约束命名约定再次与[`SchemaType`](type_basics.html#sqlalchemy.types.SchemaType "sqlalchemy.types.SchemaType")约束一起使用。

约束API [¶](#constraints-api "Permalink to this headline")
----------------------------------------------------------

*class* `sqlalchemy.schema。`{.descclassname} `约束`{.descname} （ *name =无*，*可推迟=无*，*开始=无*，*\_create\_rule =无*，*info =无*，*\_type\_bound = False* ，*\*\* dialect\_kw* ） [¶](#sqlalchemy.schema.Constraint "Permalink to this definition")
:   基础：[`sqlalchemy.sql.base.DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")，[`sqlalchemy.schema.SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

    表级SQL约束。

     `__init__`{.descname}(*name=None*, *deferrable=None*, *initially=None*, *\_create\_rule=None*, *info=None*, *\_type\_bound=False*, *\*\*dialect\_kw*)[¶](#sqlalchemy.schema.Constraint.__init__ "Permalink to this definition")
    :   创建一个SQL约束。

        参数：

        -   **name**[¶](#sqlalchemy.schema.Constraint.params.name) –
            Optional, the in-database name of this
            `Constraint`.
        -   **可延迟**
            [¶](#sqlalchemy.schema.Constraint.params.deferrable) -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初** [¶](#sqlalchemy.schema.Constraint.params.initially)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY
            。
        -   **info** [¶](#sqlalchemy.schema.Constraint.params.info) -

            可选数据字典，将填充到此对象的[`SchemaItem.info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")属性中。

            版本1.0.0中的新功能

        -   **\_create\_rule**
            [¶](#sqlalchemy.schema.Constraint.params._create_rule) -

            在编译期间传递DDLCompiler对象的可调用对象。返回True或False以表示此约束的内联生成。

            AddConstraint和DropConstraint
            DDL结构提供DDLElement更全面的“条件DDL”方法，在发布DDL时传递数据库连接。在任何CREATE
            TABLE编译过程中，都可以调用\_create\_rule，在这里可能没有任何事务/连接正在进行。但是，它允许对约束进行条件编译，即使对于不支持通过ALTER
            TABLE添加约束的后端（当前包括SQLite）也是如此。

            \_create\_rule被某些类型用来创建约束。目前，其呼叫签名随时可能发生变化。

        -   **\*\*dialect\_kw**[¶](#sqlalchemy.schema.Constraint.params.**dialect_kw)
            – Additional keyword arguments are dialect specific, and
            passed in the form `<dialectname>_<argname>`.
            有关记录参数的详细信息，请参阅[Dialects](dialects_index.html)中有关单个方言的文档。

*class* `sqlalchemy.schema。`{.descclassname} `ColumnCollectionMixin`{.descname} （ *\*列*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.ColumnCollectionMixin "Permalink to this definition")*
:   `列`{.descname} *=无* [¶](#sqlalchemy.schema.ColumnCollectionMixin.columns "Permalink to this definition")
    :   [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的[`ColumnCollection`](sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")。

        此集合表示此对象引用的列。

*class* `sqlalchemy.schema。`{.descclassname} `ColumnCollectionConstraint`{.descname} （ *\*列*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.ColumnCollectionConstraint "Permalink to this definition")*
:   基础：[`sqlalchemy.schema.ColumnCollectionMixin`](#sqlalchemy.schema.ColumnCollectionMixin "sqlalchemy.schema.ColumnCollectionMixin")，[`sqlalchemy.schema.Constraint`](#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")

    代表ColumnCollection的约束。plain

    `__ init __`{.descname} （ *\*列*，*\*\* kw* ） [T5\>](#sqlalchemy.schema.ColumnCollectionConstraint.__init__ "Permalink to this definition")
    :   参数：
        -   **\*columns**[¶](#sqlalchemy.schema.ColumnCollectionConstraint.params.*columns)
            – A sequence of column names or Column objects.
        -   **name**[¶](#sqlalchemy.schema.ColumnCollectionConstraint.params.name)
            – Optional, the in-database name of this constraint.
        -   **可延迟**
            [¶](#sqlalchemy.schema.ColumnCollectionConstraint.params.deferrable)
            -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初**
            [¶](#sqlalchemy.schema.ColumnCollectionConstraint.params.initially)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY
            。
        -   **\*\*kw**[¶](#sqlalchemy.schema.ColumnCollectionConstraint.params.**kw)
            – other keyword arguments including dialect-specific
            arguments are propagated to the [`Constraint`](#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")
            superclass.

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.ColumnCollectionConstraint.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.ColumnCollectionConstraint.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.ColumnCollectionConstraint.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.ColumnCollectionConstraint.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    ` contains_column  T0> （ T1>  COL  T2> ） T3> ¶ T4>`{.descname}
    :   如果此约束包含给定的列，则返回True。

        请注意，此对象还包含属性`.columns`，它是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的[`ColumnCollection`](sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

 *class*`sqlalchemy.schema.`{.descclassname}`CheckConstraint`{.descname}(*sqltext*, *name=None*, *deferrable=None*, *initially=None*, *table=None*, *info=None*, *\_create\_rule=None*, *\_autoattach=True*, *\_type\_bound=False*)[¶](#sqlalchemy.schema.CheckConstraint "Permalink to this definition")
:   基础：[`sqlalchemy.schema.ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

    表或列级CHECK约束。

    可以包含在表或列的定义中。

     `__init__`{.descname}(*sqltext*, *name=None*, *deferrable=None*, *initially=None*, *table=None*, *info=None*, *\_create\_rule=None*, *\_autoattach=True*, *\_type\_bound=False*)[¶](#sqlalchemy.schema.CheckConstraint.__init__ "Permalink to this definition")
    :   构造一个CHECK约束。

        参数：

        -   **sqltext**
            [¶](#sqlalchemy.schema.CheckConstraint.params.sqltext) -

            包含约束定义的字符串，将逐字使用，或SQL表达式结构。如果以字符串形式给出，则该对象将转换为[`Text`](type_basics.html#sqlalchemy.types.Text "sqlalchemy.types.Text")对象。如果文本字符串包含冒号字符，请使用反斜杠进行转义：

                CheckConstraint(r"foo ~ E'a(?\:b|c)d")

        -   **name**[¶](#sqlalchemy.schema.CheckConstraint.params.name)
            – Optional, the in-database name of the constraint.
        -   **可延迟**
            [¶](#sqlalchemy.schema.CheckConstraint.params.deferrable) -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初**
            [¶](#sqlalchemy.schema.CheckConstraint.params.initially) -
            可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY 。
        -   **info** [¶](#sqlalchemy.schema.CheckConstraint.params.info)
            -

            可选数据字典，将填充到此对象的[`SchemaItem.info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")属性中。

            版本1.0.0中的新功能

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.CheckConstraint.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.CheckConstraint.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.CheckConstraint.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.CheckConstraint.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    ` contains_column  T0> （ T1>  COL  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`contains_column()`](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column "sqlalchemy.schema.ColumnCollectionConstraint.contains_column")
        *method of* [`ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

        如果此约束包含给定的列，则返回True。

        请注意，此对象还包含属性`.columns`，它是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的[`ColumnCollection`](sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

 *class*`sqlalchemy.schema.`{.descclassname}`ForeignKey`{.descname}(*column*, *\_constraint=None*, *use\_alter=False*, *name=None*, *onupdate=None*, *ondelete=None*, *deferrable=None*, *initially=None*, *link\_to\_name=False*, *match=None*, *info=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.schema.ForeignKey "Permalink to this definition")
:   基础：[`sqlalchemy.sql.base.DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")，[`sqlalchemy.schema.SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

    定义两列之间的依赖关系。

    `ForeignKey`被指定为[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的参数，例如：

        t = Table("remote_table", metadata,
            Column("remote_id", ForeignKey("main_table.id"))
        )

    请注意，`ForeignKey`只是一个定义两列之间相关性的标记对象。实际约束在所有情况下都由[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象表示。This
    object will be generated automatically when a `ForeignKey` is associated with a [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    which in turn is associated with a [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").
    Conversely, when [`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
    is applied to a [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
    `ForeignKey` markers are automatically generated
    to be present on each associated [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
    which are also associated with the constraint object.

    请注意，您无法使用`ForeignKey`对象定义“复合”外键约束，该约束是多个父/子列分组之间的约束。要定义此分组，必须使用[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")对象，并将其应用于[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")。关联的`ForeignKey`对象是自动创建的。

    与单个[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象关联的`ForeignKey`对象在该列的foreign\_keys集合中可用。

    外键配置的更多示例在[Defining Foreign
    Keys](#metadata-foreignkeys)中。

     `__init__`{.descname}(*column*, *\_constraint=None*, *use\_alter=False*, *name=None*, *onupdate=None*, *ondelete=None*, *deferrable=None*, *initially=None*, *link\_to\_name=False*, *match=None*, *info=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.schema.ForeignKey.__init__ "Permalink to this definition")
    :   构建一个列级别的FOREIGN KEY。

        The [`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
        object when constructed generates a
        [`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")
        which is associated with the parent [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
        object’s collection of constraints.

        参数：

        -   **列** [¶](#sqlalchemy.schema.ForeignKey.params.column) -

            关键关系的单个目标列。一个[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象或列名称作为字符串：`tablename.columnkey`或`schema.tablename.columnkey`。`columnkey` is the
            `key` which has been assigned to the
            column (defaults to the column name itself), unless
            `link_to_name` is `True` in which case the rendered name of the column is
            used.

            0.7.4版中的新功能：请注意，如果未包含模式名称，并且基础[`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")具有“模式”，则将使用该值。

        -   **名称** [¶](#sqlalchemy.schema.ForeignKey.params.name) -
            可选字符串。没有提供约束时，密钥的数据库内名称。
        -   **onupdate**
            [¶](#sqlalchemy.schema.ForeignKey.params.onupdate) -
            可选字符串。如果设置，则在为此约束发出DDL时发出ON UPDATE 。
            T0\>典型值包括CASCADE，DELETE和RESTRICT。
        -   **ondelete**
            [¶](#sqlalchemy.schema.ForeignKey.params.ondelete) -
            可选字符串。如果设置，则在为此约束发出DDL时发出ON DELETE 。
            T0\>典型值包括CASCADE，DELETE和RESTRICT。
        -   **可延迟**
            [¶](#sqlalchemy.schema.ForeignKey.params.deferrable) -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初** [¶](#sqlalchemy.schema.ForeignKey.params.initially)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY
            。
        -   **link\_to\_name**[¶](#sqlalchemy.schema.ForeignKey.params.link_to_name)
            – if True, the string name given in `column` is the rendered name of the referenced column, not
            its locally assigned `key`.
        -   **use\_alter**
            [¶](#sqlalchemy.schema.ForeignKey.params.use_alter) -

            传递给底层的[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")以指示应该从CREATE
            TABLE / DROP
            TABLE语句向外部生成/删除约束。有关详细说明，请参阅[`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")。

            也可以看看

            [`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")

            [Creating/Dropping Foreign Key Constraints via
            ALTER](#use-alter)创建/删除外键约束

        -   **匹配** [¶](#sqlalchemy.schema.ForeignKey.params.match) -
            可选字符串。如果设置，则在为此约束发出DDL时发出MATCH 。
            T0\>典型值包括SIMPLE，PARTIAL和FULL。
        -   **info** [¶](#sqlalchemy.schema.ForeignKey.params.info) -

            可选数据字典，将填充到此对象的[`SchemaItem.info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")属性中。

            版本1.0.0中的新功能

        -   **\*\* dialect\_kw**
            [¶](#sqlalchemy.schema.ForeignKey.params.**dialect_kw) -

            其他关键字参数是特定于方言的，并以`<dialectname>_<argname>`的形式传递。参数最终由相应的[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")处理。有关记录参数的详细信息，请参阅[Dialects](dialects_index.html)中有关单个方言的文档。

            版本0.9.2中的新功能

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.ForeignKey.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.ForeignKey.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.ForeignKey.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.ForeignKey.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    `列 T0> ¶ T1>`{.descname}
    :   返回由[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")引用的目标[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

        如果没有建立目标列，则会引发异常。

        版本0.9.0中已更改：只要ForeignKey对象和它所引用的远程列都与同一个MetaData对象关联，就立即发生外键目标列解析。

    `复制 T0> （ T1> 架构=无 T2> ） T3> ¶ T4>`{.descname}
    :   生成这个[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")对象的副本。

        新的[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")不会绑定到任何[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

        This method is usually used by the internal copy procedures of
        [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
        [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table"),
        and [`MetaData`](metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData").

        参数：

        **schema**[¶](#sqlalchemy.schema.ForeignKey.copy.params.schema)
        – The returned [`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
        will reference the original table and column name, qualified by
        the given string schema name.

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    ` get_referent  T0> （ T1> 表 T2> ） T3> ¶ T4>`{.descname}
    :   返回此[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")引用的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

        如果[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")没有引用给定的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，则返回None。

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

    `引用 T0> （ T1> 表 T2> ） T3> ¶ T4>`{.descname}
    :   如果给定的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")被此[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")引用，则返回True。

    ` target_fullname  T0> ¶ T1>`{.descname}
    :   为[`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")返回一个基于字符串的'列规范'。

        这通常等同于首先传递给对象构造函数的基于字符串的“tablename.colname”参数。

 *class*`sqlalchemy.schema.`{.descclassname}`ForeignKeyConstraint`{.descname}(*columns*, *refcolumns*, *name=None*, *onupdate=None*, *ondelete=None*, *deferrable=None*, *initially=None*, *use\_alter=False*, *link\_to\_name=False*, *match=None*, *table=None*, *info=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.schema.ForeignKeyConstraint "Permalink to this definition")
:   基础：[`sqlalchemy.schema.ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

    表级别的FOREIGN KEY约束。

    定义单列或复合FOREIGN KEY ... REFERENCES约束。For a no-frills,
    single column foreign key, adding a [`ForeignKey`](#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")
    to the definition of a [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    is a shorthand equivalent for an unnamed, single column
    [`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint").

    外键配置示例位于[Defining Foreign Keys](#metadata-foreignkeys)中。

     `__init__`{.descname}(*columns*, *refcolumns*, *name=None*, *onupdate=None*, *ondelete=None*, *deferrable=None*, *initially=None*, *use\_alter=False*, *link\_to\_name=False*, *match=None*, *table=None*, *info=None*, *\*\*dialect\_kw*)[¶](#sqlalchemy.schema.ForeignKeyConstraint.__init__ "Permalink to this definition")
    :   构建一个支持复合的FOREIGN KEY。

        参数：

        -   **columns**[¶](#sqlalchemy.schema.ForeignKeyConstraint.params.columns)
            – A sequence of local column names.
            指定的列必须定义并出现在父表中。除非`link_to_name`为True，否则这些名称应该与赋予每列的`key`匹配（默认为名称）。
        -   **refcolumns**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.refcolumns)
            - 一系列外部列名或列对象。这些列必须全部位于同一个表内。
        -   **name**[¶](#sqlalchemy.schema.ForeignKeyConstraint.params.name)
            – Optional, the in-database name of the key.
        -   **onupdate**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.onupdate)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出ON UPDATE
            。 T0\>典型值包括CASCADE，DELETE和RESTRICT。
        -   **ondelete**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.ondelete)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出ON DELETE
            。 T0\>典型值包括CASCADE，DELETE和RESTRICT。
        -   **可延迟**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.deferrable)
            -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.initially)
            - 可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY
            。
        -   **link\_to\_name**[¶](#sqlalchemy.schema.ForeignKeyConstraint.params.link_to_name)
            – if True, the string name given in `column` is the rendered name of the referenced column, not
            its locally assigned `key`.
        -   **use\_alter**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter)
            -

            如果为True，则不要将此约束的DDL作为CREATE
            TABLE定义的一部分发出。相反，在创建完整的表集合之后，通过ALTER
            TABLE语句生成它，并在删除整个表集合之前通过ALTER
            TABLE语句删除它。

            The use of [`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")
            is particularly geared towards the case where two or more
            tables are established within a mutually-dependent foreign
            key constraint relationship; however, the
            [`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")
            and [`MetaData.drop_all()`](metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")
            methods will perform this resolution automatically, so the
            flag is normally not needed.

            版本1.0.0中已更改：添加了外键循环的自动解析，无需在典型用例中使用[`ForeignKeyConstraint.use_alter`](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter "sqlalchemy.schema.ForeignKeyConstraint")。

            也可以看看

            [Creating/Dropping Foreign Key Constraints via
            ALTER](#use-alter)创建/删除外键约束

        -   **匹配**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.match) -
            可选字符串。如果设置，则在为此约束发出DDL时发出MATCH 。
            T0\>典型值包括SIMPLE，PARTIAL和FULL。
        -   **info**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.info) -

            可选数据字典，将填充到此对象的[`SchemaItem.info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")属性中。

            版本1.0.0中的新功能

        -   **\*\* dialect\_kw**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.params.**dialect_kw)
            -

            其他关键字参数是特定于方言的，并以`<dialectname>_<argname>`的形式传递。有关记录参数的详细信息，请参阅[Dialects](dialects_index.html)中有关单个方言的文档。

            > 版本0.9.2中的新功能

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.ForeignKeyConstraint.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.ForeignKeyConstraint.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.ForeignKeyConstraint.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    ` column_keys  T0> ¶ T1>`{.descname}
    :   返回表示本[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")中本地列的字符串键列表。

        该列表是发送给[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")的构造函数的原始字符串参数，或者如果约束已使用[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象初始化，则为每个元素的字符串.key。

        版本1.0.0中的新功能

    ` contains_column  T0> （ T1>  COL  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`contains_column()`](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column "sqlalchemy.schema.ColumnCollectionConstraint.contains_column")
        *method of* [`ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

        如果此约束包含给定的列，则返回True。

        请注意，此对象还包含属性`.columns`，它是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的[`ColumnCollection`](sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

    ` referred_table  T0> ¶ T1>`{.descname}
    :   这个[`ForeignKeyConstraint`](#sqlalchemy.schema.ForeignKeyConstraint "sqlalchemy.schema.ForeignKeyConstraint")引用的[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象。

        这是一个动态计算的属性，如果约束和/或父表尚未与包含引用表的元数据集合关联，则该属性可能不可用。

        版本1.0.0中的新功能

*class* `sqlalchemy.schema。`{.descclassname} `PrimaryKeyConstraint`{.descname} （ *\*列*，*\*\*千瓦 T5\> ） T6\> [¶ T7\>](#sqlalchemy.schema.PrimaryKeyConstraint "Permalink to this definition")*
:   基础：[`sqlalchemy.schema.ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

    表级PRIMARY KEY约束。

    The [`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
    object is present automatically on any [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    object; it is assigned a set of [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
    objects corresponding to those marked with the
    [`Column.primary_key`](metadata.html#sqlalchemy.schema.Column.params.primary_key "sqlalchemy.schema.Column")
    flag:

        >>> my_table = Table('mytable', metadata,
        ...                 Column('id', Integer, primary_key=True),
        ...                 Column('version_id', Integer, primary_key=True),
        ...                 Column('data', String(50))
        ...     )
        >>> my_table.primary_key
        PrimaryKeyConstraint(
            Column('id', Integer(), table=<mytable>,
                   primary_key=True, nullable=False),
            Column('version_id', Integer(), table=<mytable>,
                   primary_key=True, nullable=False)
        )

    也可以通过显式使用[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")对象指定[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")的主键；在这种使用模式下，还可以指定约束的“名称”以及可能被方言识别的其他选项：

        my_table = Table('mytable', metadata,
                    Column('id', Integer),
                    Column('version_id', Integer),
                    Column('data', String(50)),
                    PrimaryKeyConstraint('id', 'version_id',
                                         name='mytable_pk')
                )

    一般不应混合两种类型的色谱柱规格。如果[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")中的列与标记为`primary_key=True`的列不符（如果两者都存在），则发出警告；在这种情况下，列严格取自[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")声明，而那些标记为`primary_key=True`的列将被忽略。此行为旨在向后兼容以前的行为。

    版本0.9.2更改：除了标记为`primary_key=True`的列以外，在[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")中使用列的混合现在会发出警告if列表不匹配。忽略那些仅标有标志的列的最终行为目前保持向后兼容；此警告可能会在未来版本中引发异常。

    For the use case where specific options are to be specified on the
    [`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint"),
    but the usual style of using `primary_key=True`
    flags is still desirable, an empty [`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")
    may be specified, which will take on the primary key column
    collection from the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")
    based on the flags:

        my_table = Table('mytable', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('version_id', Integer, primary_key=True),
                    Column('data', String(50)),
                    PrimaryKeyConstraint(name='mytable_pk',
                                         mssql_clustered=True)
                )

    版本0.9.2中的新功能：现在可以指定一个空的[`PrimaryKeyConstraint`](#sqlalchemy.schema.PrimaryKeyConstraint "sqlalchemy.schema.PrimaryKeyConstraint")用于使用约束建立关键字参数，而不管“主键”
    [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")本身；标记为`primary_key=True`的列将被收集到空约束的列集合中。

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.PrimaryKeyConstraint.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.PrimaryKeyConstraint.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.PrimaryKeyConstraint.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.PrimaryKeyConstraint.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    ` contains_column  T0> （ T1>  COL  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`contains_column()`](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column "sqlalchemy.schema.ColumnCollectionConstraint.contains_column")
        *method of* [`ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

        如果此约束包含给定的列，则返回True。

        请注意，此对象还包含属性`.columns`，它是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的[`ColumnCollection`](sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

 *class*`sqlalchemy.schema.`{.descclassname}`UniqueConstraint`{.descname}(*\*columns*, *\*\*kw*)[¶](#sqlalchemy.schema.UniqueConstraint "Permalink to this definition")
:   基础：[`sqlalchemy.schema.ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

    表级UNIQUE约束。

    定义单列或复合UNIQUE约束。对于简单的单列约束，将`unique=True`添加到`Column`定义中是对未命名的单列UniqueConstraint的缩写。

    `__ init __`{.descname} （ *\*列*，*\*\* kw* ） [T5\>](#sqlalchemy.schema.UniqueConstraint.__init__ "Permalink to this definition")
    :   *inherited from the* [`__init__()`](#sqlalchemy.schema.ColumnCollectionConstraint.__init__ "sqlalchemy.schema.ColumnCollectionConstraint.__init__")
        *method of* [`ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")
        参数：
        -   **\*columns**[¶](#sqlalchemy.schema.UniqueConstraint.params.*columns)
            – A sequence of column names or Column objects.
        -   **name**[¶](#sqlalchemy.schema.UniqueConstraint.params.name)
            – Optional, the in-database name of this constraint.
        -   **可延迟**
            [¶](#sqlalchemy.schema.UniqueConstraint.params.deferrable) -
            可选bool。如果设置，则在为此约束发出DDL时发出DEFERRABLE或NOT
            DEFERRABLE。
        -   **最初**
            [¶](#sqlalchemy.schema.UniqueConstraint.params.initially) -
            可选字符串。如果设置，则在为此约束发出DDL时发出INITIALLY 。
        -   **\*\*kw**[¶](#sqlalchemy.schema.UniqueConstraint.params.**kw)
            – other keyword arguments including dialect-specific
            arguments are propagated to the [`Constraint`](#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")
            superclass.

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.UniqueConstraint.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.UniqueConstraint.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.UniqueConstraint.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.UniqueConstraint.argument_for.params.default)
            - 参数的默认值。

        版本0.9.4中的新功能

    ` contains_column  T0> （ T1>  COL  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`contains_column()`](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column "sqlalchemy.schema.ColumnCollectionConstraint.contains_column")
        *method of* [`ColumnCollectionConstraint`](#sqlalchemy.schema.ColumnCollectionConstraint "sqlalchemy.schema.ColumnCollectionConstraint")

        如果此约束包含给定的列，则返回True。

        请注意，此对象还包含属性`.columns`，它是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象的[`ColumnCollection`](sqlelement.html#sqlalchemy.sql.expression.ColumnCollection "sqlalchemy.sql.expression.ColumnCollection")。

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`

 `sqlalchemy.schema.`{.descclassname}`conv`{.descname}(*cls*, *value*, *quote=None*)[¶](#sqlalchemy.schema.conv "Permalink to this definition")
:   标记一个字符串，表明名称已经通过命名约定转换。

    这是一个字符串子类，它指示不应受任何进一步命名约定的名称。

    例如。当我们使用命名约定创建[`Constraint`](#sqlalchemy.schema.Constraint "sqlalchemy.schema.Constraint")时，如下所示：

        m = MetaData(naming_convention={
            "ck": "ck_%(table_name)s_%(constraint_name)s"
        })
        t = Table('t', m, Column('x', Integer),
                        CheckConstraint('x > 5', name='x5'))

    上述约束的名称将呈现为`"ck_t_x5"`。也就是说，现有名称`x5`在命名约定中用作`constraint_name`标记。

    在某些情况下（例如在迁移脚本中），我们可能正在使用已转换的名称呈现上面的[`CheckConstraint`](#sqlalchemy.schema.CheckConstraint "sqlalchemy.schema.CheckConstraint")。为了确保该名称不被重复修改，使用[`schema.conv()`](#sqlalchemy.schema.conv "sqlalchemy.schema.conv")标记来应用新名称。我们可以如下明确地使用它：

        m = MetaData(naming_convention={
            "ck": "ck_%(table_name)s_%(constraint_name)s"
        })
        t = Table('t', m, Column('x', Integer),
                        CheckConstraint('x > 5', name=conv('ck_t_x5')))

    在上面的地方，[`schema.conv()`](#sqlalchemy.schema.conv "sqlalchemy.schema.conv")标记表明这里的约束名称是final的，名称将呈现为`"ck_t_x5"`而不是`"ck_t_ck_t_x5"`

    版本0.9.4中的新功能

    也可以看看

    [Configuring Constraint Naming
    Conventions](#constraint-naming-conventions)

索引[¶ T0\>](#indexes "Permalink to this headline")
---------------------------------------------------

Indexes can be created anonymously (using an auto-generated name
`ix_<column label>`) for a single column using the
inline `index` keyword on [`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
which also modifies the usage of `unique` to apply
the uniqueness to the index itself, instead of adding a separate UNIQUE
constraint.
对于具有特定名称或包含多个列的索引，请使用需要名称的[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")结构。

下面我们举例说明一个[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")，其中有几个[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象关联。“CREATE
INDEX”的DDL在表的create语句之后立即发布：

    meta = MetaData()
    mytable = Table('mytable', meta,
        # an indexed column, with index "ix_mytable_col1"
        Column('col1', Integer, index=True),

        # a uniquely indexed column with index "ix_mytable_col2"
        Column('col2', Integer, index=True, unique=True),

        Column('col3', Integer),
        Column('col4', Integer),

        Column('col5', Integer),
        Column('col6', Integer),
        )

    # place an index on col3, col4
    Index('idx_col34', mytable.c.col3, mytable.c.col4)

    # place a unique index on col5, col6
    Index('myindex', mytable.c.col5, mytable.c.col6, unique=True)

    sqlmytable.create(engine)
    CREATE TABLE mytable (
        col1 INTEGER,
        col2 INTEGER,
        col3 INTEGER,
        col4 INTEGER,
        col5 INTEGER,
        col6 INTEGER
    )
    CREATE INDEX ix_mytable_col1 ON mytable (col1)
    CREATE UNIQUE INDEX ix_mytable_col2 ON mytable (col2)
    CREATE UNIQUE INDEX myindex ON mytable (col5, col6)
    CREATE INDEX idx_col34 ON mytable (col3, col4)

注意在上面的例子中，[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")构造是直接使用[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象在它所对应的表的外部创建的。[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")还支持[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")中的“内联”定义，使用字符串名称来标识列：

    meta = MetaData()plain
    mytable = Table('mytable', meta,
        Column('col1', Integer),

        Column('col2', Integer),

        Column('col3', Integer),
        Column('col4', Integer),

        # place an index on col1, col2
        Index('idx_col12', 'col1', 'col2'),

        # place a unique index on col3, col4
        Index('idx_col34', 'col3', 'col4', unique=True)
    )

0.7 版中的新功能支持[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")中[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")内的“内联”定义。

[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")对象也支持它自己的`create()`方法：

    i = Index('someindex', mytable.c.col5)
    sqli.create(engine)
    CREATE INDEX someindex ON mytable (col5)

### 功能索引[¶](#functional-indexes "Permalink to this headline")

[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")支持目标后端支持的SQL和函数表达式。要使用降序值对列创建索引，可以使用[`ColumnElement.desc()`](sqlelement.html#sqlalchemy.sql.expression.ColumnElement.desc "sqlalchemy.sql.expression.ColumnElement.desc")修饰符：

    from sqlalchemy import Index

    Index('someindex', mytable.c.somecol.desc())

或者使用支持 Postgresql 等函数索引的后端，可以使用`lower()`函数创建“不区分大小写”的索引：

    from sqlalchemy import func, Indexplain

    Index('someindex', func.lower(mytable.c.somecol))

0.8版新增功能： [`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")支持 SQL 表达式和函数以及普通列。

索引API [¶](#index-api "Permalink to this headline")
----------------------------------------------------

 *class*`sqlalchemy.schema.`{.descclassname}`Index`{.descname}(*name*, *\*expressions*, *\*\*kw*)[¶](#sqlalchemy.schema.Index "Permalink to this definition")
:   基础：[`sqlalchemy.sql.base.DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")，[`sqlalchemy.schema.ColumnCollectionMixin`](#sqlalchemy.schema.ColumnCollectionMixin "sqlalchemy.schema.ColumnCollectionMixin")，[`sqlalchemy.schema.SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

    表级索引。plain

    定义一个复合（一个或多个列）INDEX。

    例如。：

        sometable = Table("sometable", metadata,
                        Column("name", String(50)),
                        Column("address", String(100))
                    )

        Index("some_index", sometable.c.name)

    对于简单的单列索引，添加[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")也支持`index=True`：

        sometable = Table("sometable", metadata,
                        Column("name", String(50), index=True)
                    )

    对于组合索引，可以指定多个列：

        Index("some_index", sometable.c.name, sometable.c.address)

    函数索引也受支持，通常通过将[`func`](sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")结构与表结合的[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象结合使用：

        Index("some_index", func.lower(sometable.c.name))

    0.8版本的新功能：支持功能和基于表达式的索引。

    通过内联声明或使用[`Table.append_constraint()`](metadata.html#sqlalchemy.schema.Table.append_constraint "sqlalchemy.schema.Table.append_constraint")，还可以将[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")与[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")手动关联。当使用这种方法时，索引列的名称可以被指定为字符串：

        Table("sometable", metadata,
                        Column("name", String(50)),
                        Column("address", String(100)),
                        Index("some_index", "name", "address")
                )

    为了支持这种形式的基于函数或基于表达式的索引，可以使用[`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")结构：

        from sqlalchemy import text

        Table("sometable", metadata,
                        Column("name", String(50)),
                        Column("address", String(100)),
                        Index("some_index", text("lower(name)"))
                )

    New in version 0.9.5: the [`text()`](sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")
    construct may be used to specify [`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")
    expressions, provided the [`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index") is
    explicitly associated with the [`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table").

    也可以看看

    [Indexes](#schema-indexes) - 有关[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")的一般信息。

    [Postgresql-Specific Index
    Options](dialects_postgresql.html#postgresql-indexes) -
    可用于[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")构造的PostgreSQL特定选项。

    [MySQL Specific Index Options](dialects_mysql.html#mysql-indexes) -
    可用于[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")构造的特定于MySQL的选项。

    [Clustered Index Support](dialects_mssql.html#mssql-indexes) -
    可用于[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")构造的MSSQL特定选项。

     `__init__`{.descname}(*name*, *\*expressions*, *\*\*kw*)[¶](#sqlalchemy.schema.Index.__init__ "Permalink to this definition")
    :   构造一个索引对象。

        参数：

        -   **名称** [¶](#sqlalchemy.schema.Index.params.name) -
            索引的名称
        -   **\*expressions**[¶](#sqlalchemy.schema.Index.params.*expressions)
            – Column expressions to include in the index.
            这些表达式通常是[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的实例，但也可以是最终指向[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")的任意SQL表达式。
        -   **unique = False**
            [¶](#sqlalchemy.schema.Index.params.unique) -
            仅关键字参数；如果为True，则创建唯一索引。
        -   **quote =无 [¶](#sqlalchemy.schema.Index.params.quote) -
            仅关键字参数；是否将引用应用于索引的名称。**以与[`Column.quote`](metadata.html#sqlalchemy.schema.Column.params.quote "sqlalchemy.schema.Column")相同的方式工作。
        -   **info =无** [¶](#sqlalchemy.schema.Index.params.info) -

            可选数据字典，将填充到此对象的[`SchemaItem.info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")属性中。

            版本1.0.0中的新功能

        -   **\*\*kw**[¶](#sqlalchemy.schema.Index.params.**kw) –
            Additional keyword arguments not mentioned above are dialect
            specific, and passed in the form
            `<dialectname>_<argname>`.
            有关记录参数的详细信息，请参阅[Dialects](dialects_index.html)中有关单个方言的文档。

    `argument_for`{.descname} （ *dialect\_name*，*argument\_name*，*默认* ） [¶ T6\>](#sqlalchemy.schema.Index.argument_for "Permalink to this definition")
    :   *inherited from the* [`argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        *method of* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        为此课程添加一种新的特定于方言的关键字参数。

        例如。：

            Index.argument_for("mydialect", "length", None)

            some_index = Index('a', 'b', mydialect_length=5)

        The [`DialectKWArgs.argument_for()`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.argument_for "sqlalchemy.sql.base.DialectKWArgs.argument_for")
        method is a per-argument way adding extra arguments to the
        [`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")
        dictionary.
        这本词典提供了代表方言的各种模式层次结构所接受的参数名称列表。

        新方言通常应该一次性将该字典指定为方言类的数据成员。用于临时添加参数名称的用例通常用于最终用户代码，该代码也使用了使用额外参数的自定义编译方案。

        参数：

        -   **dialect\_name**[¶](#sqlalchemy.schema.Index.argument_for.params.dialect_name)
            – name of a dialect. The dialect must be locatable, else a
            [`NoSuchModuleError`](exceptions.html#sqlalchemy.exc.NoSuchModuleError "sqlalchemy.exc.NoSuchModuleError")
            is raised.
            该方言还必须包含一个现有的[`DefaultDialect.construct_arguments`](internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments "sqlalchemy.engine.default.DefaultDialect.construct_arguments")集合，指示它参与关键字参数验证和默认系统，否则引发[`ArgumentError`](exceptions.html#sqlalchemy.exc.ArgumentError "sqlalchemy.exc.ArgumentError")。如果方言不包括这个集合，那么任何关键字参数都可以代表这个方言指定。所有包含在SQLAlchemy中的方言都包含这个集合，但是对于第三方方言，支持可能会有所不同。
        -   **argument\_name**
            [¶](#sqlalchemy.schema.Index.argument_for.params.argument_name)
            - 参数的名称。
        -   **默认**
            [¶](#sqlalchemy.schema.Index.argument_for.params.default) -
            参数的默认值。

        版本0.9.4中的新功能

    `结合 T0> ¶ T1>`{.descname}
    :   返回与此索引关联的可连接。

    `创建 T0> （ T1> 绑定=无 T2> ） T3> ¶ T4>`{.descname}
    :   使用给定的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")进行连接，为此[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")发出`CREATE`语句。

        也可以看看

        [`MetaData.create_all()`](metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")

    ` dialect_kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这些参数在它们的原始`<dialect>_<kwarg>`格式中呈现。只包括实际通过的论点；不同于[`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")集合，其中包含此方言已知的所有选项，包括默认值。

        该集合也是可写的；键被接受为形式`<dialect>_<kwarg>`，其中值将被组合到选项列表中。

        版本0.9.2中的新功能

        在版本0.9.4中更改： [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")集合现在可写入。

        也可以看看

        [`DialectKWArgs.dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        - nested dictionary form

    ` dialect_options  T0> ¶ T1>`{.descname}
    :   *继承自* [`dialect_options`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options "sqlalchemy.sql.base.DialectKWArgs.dialect_options")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        指定为此构造的方言特定选项的关键字参数的集合。

        这是一个两级嵌套注册表，键入`<dialect_name>`和`<argument_name>`。例如，`postgresql_where`参数可以定位为：

            arg = my_object.dialect_options['postgresql']['where']

        版本0.9.2中的新功能

        也可以看看

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")
        - flat dictionary form

    `降 T0> （ T1> 绑定=无 T2> ） T3> ¶ T4>`{.descname}
    :   使用给定的[`Connectable`](connections.html#sqlalchemy.engine.Connectable "sqlalchemy.engine.Connectable")进行连接，为此[`Index`](#sqlalchemy.schema.Index "sqlalchemy.schema.Index")发出`DROP`语句。

        也可以看看

        [`MetaData.drop_all()`](metadata.html#sqlalchemy.schema.MetaData.drop_all "sqlalchemy.schema.MetaData.drop_all")

    ` get_children  T0> （ T1>  ** kwargs  T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`get_children()`](metadata.html#sqlalchemy.schema.SchemaItem.get_children "sqlalchemy.schema.SchemaItem.get_children")
        *method of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        用于允许SchemaVisitor访问

    `信息 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`info`](metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        与对象关联的信息字典，允许用户定义的数据与这个[`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")关联。

        字典在第一次访问时自动生成。它也可以在一些对象的构造函数中指定，如[`Table`](metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")和[`Column`](metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")。

    ` kwargs  T0> ¶ T1>`{.descname}
    :   *继承自* [`kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.kwargs "sqlalchemy.sql.base.DialectKWArgs.kwargs")
        *属性* [`DialectKWArgs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs "sqlalchemy.sql.base.DialectKWArgs")

        [`DialectKWArgs.dialect_kwargs`](sqlelement.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs "sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs")的同义词。

    `引用 T0> ¶ T1>`{.descname}
    :   *inherited from the* [`quote`](metadata.html#sqlalchemy.schema.SchemaItem.quote "sqlalchemy.schema.SchemaItem.quote")
        *attribute of* [`SchemaItem`](metadata.html#sqlalchemy.schema.SchemaItem "sqlalchemy.schema.SchemaItem")

        对于具有`name`字段的模式项，返回传递给此模式对象的`quote`标志的值。

        从版本0.9开始弃用：使用`<obj>.name.quote`


