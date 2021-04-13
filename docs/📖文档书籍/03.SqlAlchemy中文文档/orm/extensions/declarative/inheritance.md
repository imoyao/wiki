---
title: 映射类继承层次结构
date: 2021-02-20 22:41:41
permalink: /sqlalchemy/orm/extensions/declarative/inheritance/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - orm
  - extensions
  - declarative
tags:
---
映射类继承层次结构[¶](#mapping-class-inheritance-hierarchies "Permalink to this headline")
==========================================================================================

SQLAlchemy 支持三种继承形式：**单表继承**，其中几种类由单个表表示，**具体表继承**，其中每种类都由独立表示表和**连接表继承**，其中类层次结构在相关表中分解，每个类由其自己的表示，其中只包含那些属于该类的属性。

最常见的继承形式是单一表和连接表，而具体继承呈现更多配置挑战。

当映射器在继承关系中配置时，SQLAlchemy 能够加载元素[polymorphically](glossary.html#term-polymorphically)，这意味着单个查询可以返回多种类型的对象。

连接表继承[¶](#joined-table-inheritance "Permalink to this headline")
---------------------------------------------------------------------

在连接的表继承中，沿着父类的特定类列表的每个类都由唯一的表来表示。特定实例的全部属性集合表示为沿其继承路径中所有表的连接。在这里，我们首先定义`Employee`类。该表将包含主键列（或多个列），以及由`Employee`表示的每个属性的列。在这种情况下，它只是`name`：

    class Employee(Base):plainplain
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        type = Column(String(50))

        __mapper_args__ = {
            'polymorphic_identity':'employee',
            'polymorphic_on':type
        }

映射表还有一个名为`type`的列。该列的作用是作为**鉴别符**，并存储一个值，该值指示行内表示的对象的类型。该列可以是任何数据类型，尽管字符串和整数是最常见的。

警告

目前，**只能设置一个鉴别器列**，通常位于层次结构中最底层的类。“级联”多态列还不被支持。

只有在需要多态加载时才需要鉴别器列，正如通常情况一样。它不是直接存在于基本映射表上，而是可以在查询类时使用的派生 select 语句上定义；但是，这是一个更复杂的配置方案。

该映射通过`__mapper_args__`字典接收附加参数。在这里，`type`列明确表示为鉴别器列，`employee`的**多态性标识**也被给出；这是将存储在该类的实例的多态鉴别器列中的值。

接下来我们定义`Employee`的`Engineer`和`Manager`子类。每个都包含表示它们表示的子类唯一的属性的列。每个表还必须包含一个主键列（或多个列），并且在大多数情况下还需要对父表的外键引用：

    class Engineer(Employee):plain
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        engineer_name = Column(String(30))

        __mapper_args__ = {
            'polymorphic_identity':'engineer',
        }

    class Manager(Employee):
        __tablename__ = 'manager'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        manager_name = Column(String(30))

        __mapper_args__ = {
            'polymorphic_identity':'manager',
        }

标准做法是将同一列用于主键的角色以及父表的外键，并且该列的名称也与父表的名称相同。但是，这两种做法都是可选的。单独的列可用于主键和父
-
关系，列的名称可能与父代的名称不同，甚至可以在父表和子表之间指定自定义连接条件，而不是使用外键。

加入继承主键

连接表继承配置的一个自然结果是任何映射对象的标识都可以完全从基表中确定。这具有明显的优势，因此 SQLAlchemy 始终将已连接继承类的主键列视为基表的唯一键列。In
other words, the `id` columns of both the
`engineer` and `manager` tables
are not used to locate `Engineer` or
`Manager` objects - only the value in
`employee.id` is considered. `engineer.id` and `manager.id` are still of course
critical to the proper operation of the pattern overall as they are used
to locate the joined row, once the parent row has been determined within
a statement.

完成联合继承映射后，查询`Employee`将返回`Employee`，`Engineer`和`Manager`对象的组合。Newly saved
`Engineer`, `Manager`, and
`Employee` objects will automatically populate the
`employee.type` column with `engineer`, `manager`, or `employee`, as appropriate.

### 查询哪些表的基本控制[¶](#basic-control-of-which-tables-are-queried "Permalink to this headline")

[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")函数和[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")的[`with_polymorphic()`](query.html#sqlalchemy.orm.query.Query.with_polymorphic "sqlalchemy.orm.query.Query.with_polymorphic")方法会影响[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")从中选择。通常，像这样的查询：

    session.query(Employee).all()plainplain

...仅从`employee`表中选择。从数据库加载新鲜数据时，我们的连接表设置将仅使用如下所示的 SQL 从父表进行查询：

    SELECT employee.id AS employee_id,
        employee.name AS employee_name, employee.type AS employee_type
    FROM employee
    []

As attributes are requested from those `Employee`
objects which are represented in either the `engineer` or `manager` child tables, a second load
is issued for the columns in that related row, if the data was not
already loaded.
因此，在访问这些对象之后，您会看到更多的 SQL 按以下方式发布：

    SELECT manager.id AS manager_id,plainplainplain
        manager.manager_data AS manager_manager_data
    FROM manager
    WHERE ? = manager.id
    [5]
    SELECT engineer.id AS engineer_id,
        engineer.engineer_info AS engineer_engineer_info
    FROM engineer
    WHERE ? = engineer.id
    [2]

在发布少量项目的搜索时（例如使用[`Query.get()`](query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")时），这种行为可以很好地工作，因为连接表的全部范围不会不必要地引入到 SQL 语句中。但是当查询大量已知类型很多的行时，可能需要主动加入部分或全部连接的表。`with_polymorphic`功能提供了此功能。

告诉我们的查询需要多态加载`Engineer`和`Manager`对象，我们可以使用[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")函数创建一个新的别名类与每个继承表的外连接相结合的基表的选择：

    from sqlalchemy.orm import with_polymorphicplain

    eng_plus_manager = with_polymorphic(Employee, [Engineer, Manager])

    query = session.query(eng_plus_manager)

上面产生一个查询，它将`employee`表连接到`engineer`和`manager`表，如下所示：

    query.all()plainplain

    SELECT employee.id AS employee_id,
        engineer.id AS engineer_id,
        manager.id AS manager_id,
        employee.name AS employee_name,
        employee.type AS employee_type,
        engineer.engineer_info AS engineer_engineer_info,
        manager.manager_data AS manager_manager_data
    FROM employee
        LEFT OUTER JOIN engineer
        ON employee.id = engineer.id
        LEFT OUTER JOIN manager
        ON employee.id = manager.id
    []

由[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")返回的实体是一个[`AliasedClass`](query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")对象，它可以像任何其他别名一样在[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")中使用，包括命名属性对于`Employee`类中的这些属性。在我们的例子中，`eng_plus_manager`成为我们用于引用上面三向外连接的实体。它还包括在类列表中命名的每个类的名称空间，以便可以调用特定于这些子类的属性。以下示例说明如何根据`eng_plus_manager`调用特定于`Engineer`以及`Manager`的属性：

    eng_plus_manager = with_polymorphic(Employee, [Engineer, Manager])plainplainplainplain
    query = session.query(eng_plus_manager).filter(
                    or_(
                        eng_plus_manager.Engineer.engineer_info=='x',
                        eng_plus_manager.Manager.manager_data=='y'
                    )
                )

[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")
accepts a single class or mapper, a list of classes/mappers, or the
string `'*'` to indicate all subclasses:

    # join to the engineer table
    entity = with_polymorphic(Employee, Engineer)

    # join to the engineer and manager tables
    entity = with_polymorphic(Employee, [Engineer, Manager])

    # join to all subclass tables
    entity = with_polymorphic(Employee, '*')

    # use the 'entity' with a Query object
    session.query(entity).all()

它还接受第三个参数`selectable`，它取代了自动连接创建，并直接从可选给定中进行选择。这个特性通常与后面描述的“具体”继承一起使用，但是可以与任何类型的继承设置一起使用，以便专用 SQL 用于多态加载：

    # custom selectable
    employee = Employee.__table__
    manager = Manager.__table__
    engineer = Engineer.__table__
    entity = with_polymorphic(
                Employee,
                [Engineer, Manager],
                employee.outerjoin(manager).outerjoin(engineer)
            )

    # use the 'entity' with a Query object
    session.query(entity).all()

请注意，如果您只需要加载一个子类型，比如`Engineer`对象，则不需要[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")，因为您可以针对`Engineer`类。

[`Query.with_polymorphic()`](query.html#sqlalchemy.orm.query.Query.with_polymorphic "sqlalchemy.orm.query.Query.with_polymorphic")与[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")具有相同的用途，但在使用模式中不如其灵活，因为它仅适用于第一个完整映射，然后影响[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")中该类或目标子类的所有事件。对于简单的情况，可以认为它更简洁：

    session.query(Employee).with_polymorphic([Engineer, Manager]).\plainplainplain
        filter(or_(Engineer.engineer_info=='w', Manager.manager_data=='q'))

版本 0.8 中的新功能： [`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")，是[`Query.with_polymorphic()`](query.html#sqlalchemy.orm.query.Query.with_polymorphic "sqlalchemy.orm.query.Query.with_polymorphic")方法的改进版本。

该映射器还接受`with_polymorphic`作为配置参数，以便自动发布连接样式的加载。这个参数可能是字符串`'*'`，一个类的列表，或者是一个元组，或者是一个元组，后面跟着一个可选的：

    class Employee(Base):plainplain
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        type = Column(String(20))

        __mapper_args__ = {
            'polymorphic_on':type,
            'polymorphic_identity':'employee',
            'with_polymorphic':'*'
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        __mapper_args__ = {'polymorphic_identity':'engineer'}

    class Manager(Employee):
        __tablename__ = 'manager'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        __mapper_args__ = {'polymorphic_identity':'manager'}

对于`Employee`对象的每个查询，上述映射将产生一个类似于`with_polymorphic('*')`的查询。

使用[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")或[`Query.with_polymorphic()`](query.html#sqlalchemy.orm.query.Query.with_polymorphic "sqlalchemy.orm.query.Query.with_polymorphic")将覆盖映射器级别`with_polymorphic`设置。

 `sqlalchemy.orm.`{.descclassname}`with_polymorphic`{.descname}(*base*, *classes*, *selectable=False*, *flat=False*, *polymorphic\_on=None*, *aliased=False*, *innerjoin=False*, *\_use\_mapper\_path=False*, *\_existing\_alias=None*)[¶](#sqlalchemy.orm.with_polymorphic "Permalink to this definition")
:   生成一个[`AliasedClass`](query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")构造，它为给定基底的后代映射器指定列。

    New in version 0.8: [`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")
    is in addition to the existing [`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")
    method [`Query.with_polymorphic()`](query.html#sqlalchemy.orm.query.Query.with_polymorphic "sqlalchemy.orm.query.Query.with_polymorphic"),
    which has the same purpose but is not as flexible in its usage.

    使用此方法将确保每个后代映射程序的表都包含在FROM子句中，并且将允许针对这些表使用filter()标准。结果的实例也会有这些列已经加载，所以不需要这些列的“post
    fetch”。

    请参阅[Basic Control of Which Tables are
    Queried](#with-polymorphic)中的示例。

    参数：

    -   **基** [¶](#sqlalchemy.orm.with_polymorphic.params.base) -
        基类为别名。
    -   **classes**[¶](#sqlalchemy.orm.with_polymorphic.params.classes)
        – a single class or mapper, or list of class/mappers, which
        inherit from the base class.
        或者，它也可以是字符串`'*'`，在这种情况下，所有降序映射类将被添加到FROM子句中。
    -   **aliased**[¶](#sqlalchemy.orm.with_polymorphic.params.aliased)
        – when True, the selectable will be wrapped in an alias, that is
        `(SELECT * FROM <fromclauses>) AS anon_1`.
        当使用with\_polymorphic()在不支持括号连接的后端创建JOIN的目标（如SQLite和旧版本的MySQL）时，这可能很重要。
    -   **flat** [¶](#sqlalchemy.orm.with_polymorphic.params.flat) -

        布尔，将通过传递给
        :   [`FromClause.alias()`](core_selectable.html#sqlalchemy.sql.expression.FromClause.alias "sqlalchemy.sql.expression.FromClause.alias")调用，以便[`Join`](core_selectable.html#sqlalchemy.sql.expression.Join "sqlalchemy.sql.expression.Join")对象的别名不包含封闭的SELECT。这可以在许多情况下导致更高效的查询。针对嵌套JOIN的JOIN将被重写为针对不支持此语法的后端上的别名SELECT子查询的JOIN。

        将`flat`设置为`True`意味着`aliased`标志也是`True`。

        版本0.9.0中的新功能

        也可以看看

        [`Join.alias()`](core_selectable.html#sqlalchemy.sql.expression.Join.alias "sqlalchemy.sql.expression.Join.alias")

    -   **selectable**[¶](#sqlalchemy.orm.with_polymorphic.params.selectable)
        – a table or select() statement that will be used in place of
        the generated FROM clause.
        如果任何期望的类使用具体的表继承，则此参数是必需的，因为SQLAlchemy目前无法自动在表之间生成UNION。如果使用，`selectable`参数必须表示由每个映射类映射的全部表和列集。否则，未记录的映射列将导致它们的表直接附加到FROM子句中，这通常会导致错误的结果。
    -   **polymorphic\_on**
        [¶](#sqlalchemy.orm.with_polymorphic.params.polymorphic_on) -
        用作给定可选项的“鉴别器”列的列。如果没有给定，将使用基类映射器的polymorphic\_on属性（如果有的话）。这对默认情况下没有多态加载行为的映射很有用。
    -   **innerjoin**[¶](#sqlalchemy.orm.with_polymorphic.params.innerjoin)
        – if True, an INNER JOIN will be used.
        这应该仅在查询一个特定子类型时才被指定

### 高级控制哪些表被查询[¶](#advanced-control-of-which-tables-are-queried "Permalink to this headline")

`with_polymorphic`函数适用于简单场景。但是，需要对表格渲染进行直接控制，例如当只想渲染子类表而不渲染父表时。

这个用例可以直接使用映射的[`Table`](core_metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象来实现。例如，要查询具有特定标准的员工姓名：

    engineer = Engineer.__table__plain
    manager = Manager.__table__

    session.query(Employee.name).\
        outerjoin((engineer, engineer.c.employee_id==Employee.employee_id)).\
        outerjoin((manager, manager.c.employee_id==Employee.employee_id)).\
        filter(or_(Engineer.engineer_info=='w', Manager.manager_data=='q'))

基表，在这种情况下，“雇员”表，并不总是必要的。使用更少的连接，SQL 查询总是更高效。在这里，如果我们只想加载特定于管理员或工程师的信息，我们可以指示[`Query`](query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")仅使用那些表。`FROM`子句由[`Session.query()`](session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")，[`Query.filter()`](query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")或[`Query.select_from()`](query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")方法：

    session.query(Manager.manager_data).select_from(manager)plainplain

    session.query(engineer.c.id).\
            filter(engineer.c.engineer_info==manager.c.manager_data)

### 创建连接到特定的子类型[¶](#creating-joins-to-specific-subtypes "Permalink to this headline")

[`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")方法是一个帮助器，它允许沿着[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")路径构建连接，同时将标准缩小到特定的子类。假设`employees`表代表与`Company`对象关联的员工集合。我们将在`employees`表和一个新表`companies`中添加一个`company_id`列：

    class Company(Base):plainplain
        __tablename__ = 'company'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        employees = relationship("Employee",
                        backref='company',
                        cascade='all, delete-orphan')

    class Employee(Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        type = Column(String(20))
        company_id = Column(Integer, ForeignKey('company.id'))
        __mapper_args__ = {
            'polymorphic_on':type,
            'polymorphic_identity':'employee',
            'with_polymorphic':'*'
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        engineer_info = Column(String(50))
        __mapper_args__ = {'polymorphic_identity':'engineer'}

    class Manager(Employee):
        __tablename__ = 'manager'
        id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
        manager_data = Column(String(50))
        __mapper_args__ = {'polymorphic_identity':'manager'}

When querying from `Company` onto the
`Employee` relationship, the `join()` method as well as the `any()` and
`has()` operators will create a join from
`company` to `employee`, without
including `engineer` or `manager` in the mix. 如果我们希望具有专门针对`Engineer`类的标准，那么我们可以使用[`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")运算符告诉那些方法连接或子查询表示子类的连接表：

    session.query(Company).\plain
        join(Company.employees.of_type(Engineer)).\
        filter(Engineer.engineer_info=='someinfo')

这样的一个长效版本将涉及到在 2 元组中可选的完整目标：

    employee = Employee.__table__plain
    engineer = Engineer.__table__

    session.query(Company).\
        join((employee.join(engineer), Company.employees)).\
        filter(Engineer.engineer_info=='someinfo')

[`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")接受一个类参数。通过连接到上面的显式连接，或者使用[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")函数创建一个多态可选：

    manager_and_engineer = with_polymorphic(plainplain
                                Employee, [Manager, Engineer],
                                aliased=True)

    session.query(Company).\
        join(manager_and_engineer, Company.employees).\
        filter(
            or_(manager_and_engineer.Engineer.engineer_info=='someinfo',
                manager_and_engineer.Manager.manager_data=='somedata')
        )

在上面，我们在`orm.with_polymorhpic()`中使用了`aliased=True`参数，这样`Company`和`manager_and_engineer`转换为别名子查询。某些后端（如 SQLite 和旧版本的 MySQL）无法处理以下格式的 FROM 子句：

    FROM x JOIN (y JOIN z ON <onclause>) ON <onclause>plain

使用`aliased=True`而不是将其呈现为：

    FROM x JOIN (SELECT * FROM y JOIN z ON <onclause>) AS anon_1 ON <onclause>plainplain

上面的连接也可以通过将`of_type()`与多态结构相结合来更简洁地表达：

    manager_and_engineer = with_polymorphic(plain
                                Employee, [Manager, Engineer],
                                aliased=True)

    session.query(Company).\
        join(Company.employees.of_type(manager_and_engineer)).\
        filter(
            or_(manager_and_engineer.Engineer.engineer_info=='someinfo',
                manager_and_engineer.Manager.manager_data=='somedata')
        )

当嵌入式标准根据子类时，`any()`和`has()`运算符也可以与[`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")一起使用：

    session.query(Company).\plain
            filter(
                Company.employees.of_type(Engineer).
                    any(Engineer.engineer_info=='someinfo')
                ).all()

请注意，`any()`和`has()`都是相关 EXISTS 查询的简写。用手建立一个看起来像：

    session.query(Company).filter(plain
        exists([1],
            and_(Engineer.engineer_info=='someinfo',
                employees.c.company_id==companies.c.company_id),
            from_obj=employees.join(engineers)
        )
    ).all()

上面的 EXISTS 子查询从`employees`到`engineers`的连接中进行选择，并且还指定将 EXISTS 子选择与父`companies`表关联的标准。

New in version 0.8: [`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")
accepts [`orm.aliased()`](query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")
and [`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")
constructs in conjunction with [`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join"),
`any()` and `has()`.

### 急切加载特定或多形的子类型[¶](#eager-loading-of-specific-or-polymorphic-subtypes "Permalink to this headline")

[`joinedload()`](loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")，[`subqueryload()`](loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")，[`contains_eager()`](loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")和其他负载相关选项也支持使用[`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")下面我们加载`Company`行，同时热切地加载相关的`Engineer`对象，同时查询`employee`和`engineer`

    session.query(Company).\plainplain
        options(
            subqueryload(Company.employees.of_type(Engineer)).
            subqueryload("machines")
            )
        )

与[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")的情况一样，`of_type()`也可以用于加载和[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")同时，可以加载所有引用子类型的所有子属性：

    manager_and_engineer = with_polymorphic(
                                Employee, [Manager, Engineer],
                                aliased=True)

    session.query(Company).\
        options(
            joinedload(Company.employees.of_type(manager_and_engineer))
            )
        )

New in version 0.8: [`joinedload()`](loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload"),
[`subqueryload()`](loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload"),
[`contains_eager()`](loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")
and related loader options support paths that are qualified with
[`of_type()`](internals.html#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type"),
supporting single target types as well as
[`orm.with_polymorphic()`](#sqlalchemy.orm.with_polymorphic "sqlalchemy.orm.with_polymorphic")
targets.

上述查询的另一个选项是分别声明两个子类型； [`joinedload()`](loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")指令应该检测到这一点，并自动创建上面的`with_polymorphic`结构：

    session.query(Company).\plainplainplain
        options(
            joinedload(Company.employees.of_type(Manager)),
            joinedload(Company.employees.of_type(Engineer)),
            )
        )

版本 1.0 中的新特性当多重重叠的`of_type()`指令遇到时，像[`joinedload()`](loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")这样的热切加载器将创建一个多态实体。

单表继承[¶](#single-table-inheritance "Permalink to this headline")
-------------------------------------------------------------------

单表继承是基类的属性以及所有子类在单个表中表示的位置。表中列出了每个映射到基类和所有子类的属性；对应于单个子类的列是可空的。除了只有一个表以外，这个配置看起来很像连接表继承。在这种情况下，需要一个`type`列，因为没有其他方式可以区分类。该表仅在基本映射器中指定；对于继承类，将它们的`table`参数留空：

    class Employee(Base):plain
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        manager_data = Column(String(50))
        engineer_info = Column(String(50))
        type = Column(String(20))

        __mapper_args__ = {
            'polymorphic_on':type,
            'polymorphic_identity':'employee'
        }

    class Manager(Employee):
        __mapper_args__ = {
            'polymorphic_identity':'manager'
        }

    class Engineer(Employee):
        __mapper_args__ = {
            'polymorphic_identity':'engineer'
        }

请注意，派生类 Manager 和 Engineer 的映射器省略了`__tablename__`，表示它们没有自己的映射表。

具体表继承[¶](#concrete-table-inheritance "Permalink to this headline")
-----------------------------------------------------------------------

这种继承形式将每个类映射到不同的表。由于具体继承有更多的概念开销，首先我们将说明这些表看起来像 Core 表元数据：

    employees_table = Table(
        'employee', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
    )

    managers_table = Table(
        'manager', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('manager_data', String(50)),
    )

    engineers_table = Table(
        'engineer', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('engineer_info', String(50)),
    )

注意在这种情况下没有`type`列；对于多态加载，为了在查询过程中“制造”这些信息，需要额外的步骤。

使用经典映射，我们可以独立映射我们的三个类，而不需要任何关系；
`Engineer`和`Manager`从`Employee`继承的事实对经典映射没有任何影响：

    class Employee(object):plain
        pass

    class Manager(Employee):
        pass

    class Engineer(Employee):
        pass

    mapper(Employee, employees_table)
    mapper(Manager, managers_table)
    mapper(Engineer, engineers_table)

但是，当使用 Declarative 时，Declarative 假定类之间有继承映射，因为它们已经处于继承关系中。因此，为了以声明方式映射我们的三个类，我们必须在`__mapper_args__`中包含[`orm.mapper.concrete`](mapping_api.html#sqlalchemy.orm.mapper.params.concrete "sqlalchemy.orm.mapper")参数：

    class Employee(Base):plain
        __tablename__ = 'employee'

        id = Column(Integer, primary_key=True)
        name = Column(String(50))

    class Manager(Employee):
        __tablename__ = 'manager'

        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        manager_data = Column(String(50))

        __mapper_args__ = {
            'concrete': True
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'

        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        engineer_info = Column(String(50))

        __mapper_args__ = {
            'concrete': True
        }

应该指出两个关键点：

-   We must **define all columns explicitly** on each subclass, even
    those of the same name. 像`Employee.name`这样的列在这里不会被**复制到`Manager`或`Engineer`映射的表格中。**
-   while the `Engineer` and `Manager` classes are mapped in an inheritance relationship with
    `Employee`, they still **do not include
    polymorphic loading**.

### 具体多态加载[¶](#concrete-polymorphic-loading "Permalink to this headline")

要多态加载，需要使用[`orm.mapper.with_polymorphic`(mapping_api.html#sqlalchemy.orm.mapper.params.with_polymorphic "sqlalchemy.orm.mapper")参数，以及可选的指示如何加载行。多态加载对于具体继承来说效率最低，所以如果我们确实寻求这种加载方式，虽然可能不太推荐。在具体继承的情况下，这意味着我们必须构建所有三个表的联合。

首先用经典映射来说明这一点，SQLAlchemy 包含一个辅助函数来创建这个名为[`polymorphic_union()`](mapping_api.html#sqlalchemy.orm.util.polymorphic_union "sqlalchemy.orm.util.polymorphic_union")的 UNION，它将把所有不同的列映射到具有相同数字和列名的选择结构中，还为每个子查询生成一个虚拟的`type`列。在所有三个表都被声明之后，该函数被称为**，然后与映射器结合使用：**

    from sqlalchemy.orm import polymorphic_unionplainplain

    pjoin = polymorphic_union({
        'employee': employees_table,
        'manager': managers_table,
        'engineer': engineers_table
    }, 'type', 'pjoin')

    employee_mapper = mapper(Employee, employees_table,
                                        with_polymorphic=('*', pjoin),
                                        polymorphic_on=pjoin.c.type,
                                        polymorphic_identity='employee')
    manager_mapper = mapper(Manager, managers_table,
                                        inherits=employee_mapper,
                                        concrete=True,
                                        polymorphic_identity='manager')
    engineer_mapper = mapper(Engineer, engineers_table,
                                        inherits=employee_mapper,
                                        concrete=True,
                                        polymorphic_identity='engineer')

选择后，多态联合产生一个像这样的查询：

    session.query(Employee).all()plain

    SELECT
        pjoin.id AS pjoin_id,
        pjoin.name AS pjoin_name,
        pjoin.type AS pjoin_type,
        pjoin.manager_data AS pjoin_manager_data,
        pjoin.engineer_info AS pjoin_engineer_info
    FROM (
        SELECT
            employee.id AS id,
            employee.name AS name,
            CAST(NULL AS VARCHAR(50)) AS manager_data,
            CAST(NULL AS VARCHAR(50)) AS engineer_info,
            'employee' AS type
        FROM employee
        UNION ALL
        SELECT
            manager.id AS id,
            manager.name AS name,
            manager.manager_data AS manager_data,
            CAST(NULL AS VARCHAR(50)) AS engineer_info,
            'manager' AS type
        FROM manager
        UNION ALL
        SELECT
            engineer.id AS id,
            engineer.name AS name,
            CAST(NULL AS VARCHAR(50)) AS manager_data,
            engineer.engineer_info AS engineer_info,
            'engineer' AS type
        FROM engineer
    ) AS pjoin

上面的 UNION 查询需要为每个子表生成“NULL”列，以适应那些不属于映射的列。

为了使用 Declarative 映射具体继承和多态加载，挑战在于在映射创建时准备好多态联合。实现此目的的一种方法是继续在实际映射类之前定义表元数据，并使用`__table__`将它们指定给每个类：

    class Employee(Base):
        __table__ = employee_table
        __mapper_args__ = {
            'polymorphic_on':pjoin.c.type,
            'with_polymorphic': ('*', pjoin),
            'polymorphic_identity':'employee'
        }

    class Engineer(Employee):
        __table__ = engineer_table
        __mapper_args__ = {'polymorphic_identity':'engineer', 'concrete':True}

    class Manager(Employee):
        __table__ = manager_table
        __mapper_args__ = {'polymorphic_identity':'manager', 'concrete':True}

### 使用声明式助手类[¶](#using-the-declarative-helper-classes "Permalink to this headline")

另一种方法是使用一个特殊的帮助类，它承担推迟生成[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象的相当复杂的任务，直到收集到所有表元数据为止，并且映射器将与之关联的多态联合将能得到的。这可以通过[`AbstractConcreteBase`](extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")和[`ConcreteBase`](extensions_declarative_api.html#sqlalchemy.ext.declarative.ConcreteBase "sqlalchemy.ext.declarative.ConcreteBase")类获得。就我们这里的例子而言，我们使用“混凝土”基础，例如一个`Employee`行本身可以存在，不是`Engineer`或`Manager`。映射将如下所示：

    from sqlalchemy.ext.declarative import ConcreteBaseplainplainplain

    class Employee(ConcreteBase, Base):
        __tablename__ = 'employee'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))

        __mapper_args__ = {
            'polymorphic_identity':'employee',
            'concrete':True
        }

    class Manager(Employee):
        __tablename__ = 'manager'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        manager_data = Column(String(40))

        __mapper_args__ = {
            'polymorphic_identity':'manager',
            'concrete':True
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        engineer_info = Column(String(40))

        __mapper_args__ = {
            'polymorphic_identity':'engineer',
            'concrete':True
        }

也可以选择使用所谓的“抽象”基础；我们实际上不会有`employee`表，而只会有`manager`和`engineer`表。The `Employee` class will never be
instantiated directly.
这里的变化是基本映射器直接映射到可选的“多态联合”，它不再包含`employee`表。在经典的映射中，这是：

    from sqlalchemy.orm import polymorphic_union

    pjoin = polymorphic_union({
        'manager': managers_table,
        'engineer': engineers_table
    }, 'type', 'pjoin')

    employee_mapper = mapper(Employee, pjoin,
                                        with_polymorphic=('*', pjoin),
                                        polymorphic_on=pjoin.c.type)
    manager_mapper = mapper(Manager, managers_table,
                                        inherits=employee_mapper,
                                        concrete=True,
                                        polymorphic_identity='manager')
    engineer_mapper = mapper(Engineer, engineers_table,
                                        inherits=employee_mapper,
                                        concrete=True,
                                        polymorphic_identity='engineer')

使用声明助手，[`AbstractConcreteBase`](extensions_declarative_api.html#sqlalchemy.ext.declarative.AbstractConcreteBase "sqlalchemy.ext.declarative.AbstractConcreteBase")助手可以产生这个；该映射将是：

    from sqlalchemy.ext.declarative import AbstractConcreteBaseplain

    class Employee(AbstractConcreteBase, Base):
        pass

    class Manager(Employee):
        __tablename__ = 'manager'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        manager_data = Column(String(40))

        __mapper_args__ = {
            'polymorphic_identity':'manager',
            'concrete':True
        }

    class Engineer(Employee):
        __tablename__ = 'engineer'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        engineer_info = Column(String(40))

        __mapper_args__ = {
            'polymorphic_identity':'engineer',
            'concrete':True
        }

也可以看看

[Concrete Table
Inheritance](extensions_declarative_inheritance.html#declarative-concrete-table)
- 在声明性参考文档中

使用与继承的关系[¶](#using-relationships-with-inheritance "Permalink to this headline")
---------------------------------------------------------------------------------------

连接表和单表继承场景都产生可用于[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")函数的映射；也就是说，可以将父对象映射到多态的子对象。同样，继承映射器可以在任何级别都有[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")对象，它们继承到每个子类。关系的唯一要求是父母与子女之间存在表格关系。一个例子是对连接表继承例子的以下修改，它在`Employee`和`Company`之间设置了一个双向关系：

    employees_table = Table('employees', metadata,plainplain
        Column('employee_id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('company_id', Integer, ForeignKey('companies.company_id'))
    )

    companies = Table('companies', metadata,
       Column('company_id', Integer, primary_key=True),
       Column('name', String(50)))

    class Company(object):
        pass

    mapper(Company, companies, properties={
       'employees': relationship(Employee, backref='company')
    })

### 与具体继承的关系[¶](#relationships-with-concrete-inheritance "Permalink to this headline")

在具体的继承场景中，映射关系更具挑战性，因为不同的类不共享表。在这种情况下，如果每个子表中包含父项的外键，那么如果可以从父项到子项构建联接条件，则*可以*建立从父项到子项的关系：

    companies = Table('companies', metadata,plain
       Column('id', Integer, primary_key=True),
       Column('name', String(50)))

    employees_table = Table('employees', metadata,
        Column('employee_id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('company_id', Integer, ForeignKey('companies.id'))
    )

    managers_table = Table('managers', metadata,
        Column('employee_id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('manager_data', String(50)),
        Column('company_id', Integer, ForeignKey('companies.id'))
    )

    engineers_table = Table('engineers', metadata,
        Column('employee_id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('engineer_info', String(50)),
        Column('company_id', Integer, ForeignKey('companies.id'))
    )

    mapper(Employee, employees_table,
                    with_polymorphic=('*', pjoin),
                    polymorphic_on=pjoin.c.type,
                    polymorphic_identity='employee')

    mapper(Manager, managers_table,
                    inherits=employee_mapper,
                    concrete=True,
                    polymorphic_identity='manager')

    mapper(Engineer, engineers_table,
                    inherits=employee_mapper,
                    concrete=True,
                    polymorphic_identity='engineer')

    mapper(Company, companies, properties={
        'employees': relationship(Employee)
    })

The big limitation with concrete table inheritance is that
[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
objects placed on each concrete mapper do **not** propagate to child
mappers. 如果您想要在所有具体映射器上设置相同的[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")对象，则必须手动配置它们。To
configure back references in such a configuration the
`back_populates` keyword may be used instead of
`backref`, such as below where both
`A(object)` and `B(A)`
bidirectionally reference `C`:

    ajoin = polymorphic_union({
            'a':a_table,
            'b':b_table
        }, 'type', 'ajoin')

    mapper(A, a_table, with_polymorphic=('*', ajoin),
        polymorphic_on=ajoin.c.type, polymorphic_identity='a',
        properties={
            'some_c':relationship(C, back_populates='many_a')
    })
    mapper(B, b_table,inherits=A, concrete=True,
        polymorphic_identity='b',
        properties={
            'some_c':relationship(C, back_populates='many_a')
    })
    mapper(C, c_table, properties={
        'many_a':relationship(A, collection_class=set,
                                    back_populates='some_c'),
    })

在声明式[¶](#using-inheritance-with-declarative "Permalink to this headline")中使用继承
---------------------------------------------------------------------------------------

声明使得继承配置更直观。请参阅[Inheritance
Configuration](extensions_declarative_inheritance.html#declarative-inheritance)上的文档。
