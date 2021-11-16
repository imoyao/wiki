---
title: ORM 内部
date: 2021-02-20 22:41:35
permalink: /sqlalchemy/core/internals/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - core
tags:
---
ORM 内部[¶](#orm-internals "Permalink to this headline")
=======================================================

此处列出了其他章节未涉及的关键 ORM 结构。

 *class*`sqlalchemy.orm.state.`{.descclassname}`AttributeState`{.descname}(*state*, *key*)[¶](#sqlalchemy.orm.state.AttributeState "Permalink to this definition")
:   提供与特定映射对象上的特定属性相对应的检查界面。

    [`AttributeState`](#sqlalchemy.orm.state.AttributeState "sqlalchemy.orm.state.AttributeState")对象通过特定[`InstanceState`](#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")的[`InstanceState.attrs`](#sqlalchemy.orm.state.InstanceState.attrs "sqlalchemy.orm.state.InstanceState.attrs")集合进行访问：

        from sqlalchemy import inspect

        insp = inspect(some_mapped_object)
        attr_state = insp.attrs.some_attribute

    `历史 T0> ¶ T1>`{.descname}
    :   通过[`History`](session_api.html#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")界面返回此属性的当前预冲刷更改历史记录。

        如果该属性的值被卸载，则此方法**不会**发出加载器可调参数。

        也可以看看

        [`AttributeState.load_history()`](#sqlalchemy.orm.state.AttributeState.load_history "sqlalchemy.orm.state.AttributeState.load_history")
        - 如果值不是本地存在，则使用加载器可调用项检索历史记录。

        [`attributes.get_history()`](session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")
        - 底层函数

    ` load_history  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   通过[`History`](session_api.html#sqlalchemy.orm.attributes.History "sqlalchemy.orm.attributes.History")界面返回此属性的当前预冲刷更改历史记录。

        如果该属性的值被卸载，则此方法**将**发送加载器可调用对象。

        也可以看看

        [`AttributeState.history`](#sqlalchemy.orm.state.AttributeState.history "sqlalchemy.orm.state.AttributeState.history")

        [`attributes.get_history()`](session_api.html#sqlalchemy.orm.attributes.get_history "sqlalchemy.orm.attributes.get_history")
        - 底层函数

        版本0.9.0中的新功能

    ` loaded_value  T0> ¶ T1>`{.descname}
    :   从数据库加载的此属性的当前值。

        如果该值尚未加载，或者没有出现在对象的字典中，则返回NO\_VALUE。

    `值 T0> ¶ T1>`{.descname}
    :   返回此属性的值。

        这个操作等同于直接或通过`getattr()`访问对象的属性，并且如果需要的话将触发任何挂起的加载器可调用。

*class* `sqlalchemy.orm.util。`{.descclassname} `CascadeOptions`{.descname} [¶](#sqlalchemy.orm.util.CascadeOptions "Permalink to this definition")
:   Bases: `__builtin__.frozenset`

    跟踪发送给relationship()。cascade的选项

*类 T0\> `sqlalchemy.orm.instrumentation。 T1>  ClassManager  T2> （ T3> 类_  T4> ）< / T5> ¶ T6>`{.descclassname}*
:   基础：`__builtin__.dict`

    跟踪课堂级别的状态信息。plain

    ` __文件__  T0> ¶ T1>`{.descname}
    :   *inherited from the* `__le__` *attribute of* `dict`

        x .\_\_ le \_\_（y）\<==\> x \<= y\<="" span=""\>

    ` __ LT __  T0> ¶ T1>`{.descname}
    :   *inherited from the* `__lt__` *attribute of* `dict`

        x.\_\_lt\_\_(y) \<==\> x

    ` __ NE __  T0> ¶ T1>`{.descname}
    :   *inherited from the* `__ne__` *attribute of* `dict`

        x .\_\_ ne \_\_（y）\<==\> x！= y

    `清除`{.descname} （ ）→无。删除D. [¶](#sqlalchemy.orm.instrumentation.ClassManager.clear "Permalink to this definition")中的所有项目
    :   *inherited from the* `clear()` *method of* `dict`

    `拷贝`{.descname} （ ）→D [的浅拷贝](#sqlalchemy.orm.instrumentation.ClassManager.copy "Permalink to this definition")
    :   *inherited from the* `copy()` *method of* `dict`

    `处置 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   将这位经理与同班同学分离。

     `fromkeys`{.descname}(*S*[, *v*]) → New dict with keys from S and values equal to v.[¶](#sqlalchemy.orm.instrumentation.ClassManager.fromkeys "Permalink to this definition")
    :   *inherited from the* `fromkeys()` *method of* `dict`

        v默认为None。

     `get`{.descname}(*k*[, *d*]) → D[k] if k in D, else d. d defaults to None.[¶](#sqlalchemy.orm.instrumentation.ClassManager.get "Permalink to this definition")
    :   *继承自* `get()` *方法*
        `dict`

     `has_key`{.descname}(*k*) → True if D has a key k, else False[¶](#sqlalchemy.orm.instrumentation.ClassManager.has_key "Permalink to this definition")
    :   *继承自* `has_key()`
        *方法* `dict`

    `has_parent`{.descname} （ *state*，*key*，*optimistic = False* T5\> [¶ T6\>](#sqlalchemy.orm.instrumentation.ClassManager.has_parent "Permalink to this definition")
    :   去做

    `项`{.descname} （ ）→D（键，值）对的列表，作为2元组[¶](#sqlalchemy.orm.instrumentation.ClassManager.items "Permalink to this definition")
    :   *继承自* `items()` *方法*
        `dict`

     `iteritems`{.descname}() → an iterator over the (key, value) items of D[¶](#sqlalchemy.orm.instrumentation.ClassManager.iteritems "Permalink to this definition")
    :   *inherited from the* `iteritems()` *method of* `dict`

     `iterkeys`{.descname}() → an iterator over the keys of D[¶](#sqlalchemy.orm.instrumentation.ClassManager.iterkeys "Permalink to this definition")
    :   *inherited from the* `iterkeys()` *method of* `dict`

     `itervalues`{.descname}() → an iterator over the values of D[¶](#sqlalchemy.orm.instrumentation.ClassManager.itervalues "Permalink to this definition")
    :   *inherited from the* `itervalues()` *method of* `dict`

    `键`{.descname} （ ）→D键列表[¶](#sqlalchemy.orm.instrumentation.ClassManager.keys "Permalink to this definition")
    :   *inherited from the* `keys()` *method of* `dict`

    `管理 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   将此实例标记为其类的管理器。

    ` original_init  T0> ¶ T1>`{.descname}
    :   x .\_\_ init \_\_（...）初始化x；请参阅帮助（类型（x））进行签名

     `pop`{.descname}(*k*[, *d*]) → v, remove specified key and return the corresponding value.[¶](#sqlalchemy.orm.instrumentation.ClassManager.pop "Permalink to this definition")
    :   *继承自* `pop()` *方法*
        `dict`

        如果未找到密钥，则在返回时返回d，否则引发KeyError

    `popitem`{.descname} （ ）→（k，v），移除并返回一些（key，value）对作为[¶ t3 \>](#sqlalchemy.orm.instrumentation.ClassManager.popitem "Permalink to this definition")
    :   *继承自* `popitem()`
        *方法* `dict`

        2元组；但如果D为空则引发KeyError。

     `setdefault`{.descname}(*k*[, *d*]) → D.get(k,d), also set D[k]=d if k not in D[¶](#sqlalchemy.orm.instrumentation.ClassManager.setdefault "Permalink to this definition")
    :   *继承自* `setdefault()`
        *方法* `dict`

    ` state_getter  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   返回（实例） - \> InstanceState可调用。

        如果不能找到实例的InstanceState，“state
        getter”callables应该引发KeyError或AttributeError。

    `注销 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   删除由该ClassManager建立的所有工具。

     `update`{.descname}([*E*, ]*\*\*F*) → None. 从dict / iterable E和F更新D。[¶](#sqlalchemy.orm.instrumentation.ClassManager.update "Permalink to this definition")
    :   *inherited from the* `update()` *method of* `dict`

        如果E存在且具有.keys()方法，则：对于E中的k：D [k] = E
        [k]如果E存在并且缺少.keys()方法，则：for（k，v）in E： D [k] =
        v在任一情况下，这后面是：对于F中的k：D [k] = F [k]

    `值`{.descname} （ ）→D值列表[¶](#sqlalchemy.orm.instrumentation.ClassManager.values "Permalink to this definition")
    :   *继承自* `values()`
        *方法* `dict`

     `viewitems`{.descname}() → a set-like object providing a view on D's items[¶](#sqlalchemy.orm.instrumentation.ClassManager.viewitems "Permalink to this definition")
    :   *inherited from the* `viewitems()` *method of* `dict`

     `viewkeys`{.descname}() → a set-like object providing a view on D's keys[¶](#sqlalchemy.orm.instrumentation.ClassManager.viewkeys "Permalink to this definition")
    :   *inherited from the* `viewkeys()` *method of* `dict`

    `viewvalues  tt> （ ）→提供D值视图的对象¶`{.descname}
    :   *inherited from the* `viewvalues()` *method of* `dict`

 *class*`sqlalchemy.orm.properties.`{.descclassname}`ColumnProperty`{.descname}(*\*columns*, *\*\*kwargs*)[¶](#sqlalchemy.orm.properties.ColumnProperty "Permalink to this definition")
:   基础：`sqlalchemy.orm.interfaces.StrategizedProperty`

    描述对应于表列的对象属性。

    公共构造函数是[`orm.column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")函数。

    *class* `比较器`{.descname} （ *prop*，*parentmapper*，*adapt\_to\_entity = T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.properties.ColumnProperty.Comparator "Permalink to this definition")*
    :   基础：`sqlalchemy.util.langhelpers.MemoizedSlots`，[`sqlalchemy.orm.interfaces.PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        为[`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")属性生成布尔值，比较和其他运算符。

        有关简要概述，请参阅[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")的文档。

        也可以看看：

        [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        [Redefining and Creating New
        Operators](core_custom_types.html#types-operators)

        [`TypeEngine.comparator_factory`](core_type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")

        ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`__eq__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实施`==`运算符。

            在列上下文中，生成子句`a = b`。If the
            target is `None`, produces
            `a IS NULL`.

        ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`__le__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__le__ "sqlalchemy.sql.operators.ColumnOperators.__le__")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`<=`运算符。

            在列上下文中，生成子句`a <= b`。

        ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`__lt__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`<`运算符。

            在列上下文中，生成子句`a  b`。

        ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`__ne__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__ne__ "sqlalchemy.sql.operators.ColumnOperators.__ne__")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`!=`运算符。

            在列上下文中，生成子句`a ！= b`。If the
            target is `None`, produces
            `a IS NOT NULL`.

        ` adapt_to_entity  T0> （ T1>  adapt_to_entity  T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`adapt_to_entity()`](#sqlalchemy.orm.interfaces.PropComparator.adapt_to_entity "sqlalchemy.orm.interfaces.PropComparator.adapt_to_entity")
            *方法 [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")*

            返回此PropComparator的副本，它将使用给定的[`AliasedInsp`](query.html#sqlalchemy.orm.util.AliasedInsp "sqlalchemy.orm.util.AliasedInsp")生成相应的表达式。

        `适配器 T0> ¶ T1>`{.descname}
        :   *继承自* [`adapter`](#sqlalchemy.orm.interfaces.PropComparator.adapter "sqlalchemy.orm.interfaces.PropComparator.adapter")
            *属性的* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

            生成一个可调用的列，适应列表达式以适应该比较器的别名版本。

        `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`all_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.all_ "sqlalchemy.sql.operators.ColumnOperators.all_")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

            版本1.1中的新功能

        `任何`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.any "Permalink to this definition")
        :   *inherited from the* [`any()`](#sqlalchemy.orm.interfaces.PropComparator.any "sqlalchemy.orm.interfaces.PropComparator.any")
            *method of* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

            如果此集合包含符合给定条件的任何成员，则返回true。

            `any()`的通常实现是[`RelationshipProperty.Comparator.any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")。

            参数：

            -   **criterion**[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.any.params.criterion)
                – an optional ClauseElement formulated against the
                member class’ table or attributes.
            -   **\*\*kwargs**[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.any.params.**kwargs)
                – key/value pairs corresponding to member class
                attribute names which will be compared via equality to
                the corresponding values.

        `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *inherited from the* [`any_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.any_ "sqlalchemy.sql.operators.ColumnOperators.any_")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            针对父对象生成[`any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

            版本1.1中的新功能

        ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`asc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.asc "sqlalchemy.sql.operators.ColumnOperators.asc")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`asc()`](core_sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

        `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
        :   *inherited from the* [`between()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            在()子句之间针对父对象生成[`between()`](core_sqlelement.html#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

        `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            根据给定的排序字符串，针对父对象生成一个[`collate()`](core_sqlelement.html#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

        `的concat  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`concat()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现'concat'操作符。

            在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

        `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.orm.properties.ColumnProperty.Comparator.contains "Permalink to this definition") \>
        :   *inherited from the* [`contains()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.contains "sqlalchemy.sql.operators.ColumnOperators.contains")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现'包含'运算符。

            在列上下文中，生成子句`LIKE '％＆lt； other＆gt；％'`

        `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`desc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.desc "sqlalchemy.sql.operators.ColumnOperators.desc")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`desc()`](core_sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

        `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *inherited from the* [`distinct()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.distinct "sqlalchemy.sql.operators.ColumnOperators.distinct")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            针对父对象生成一个[`distinct()`](core_sqlelement.html#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

        `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.endswith "Permalink to this definition")
        :   *inherited from the* [`endswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.endswith "sqlalchemy.sql.operators.ColumnOperators.endswith")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现'endswith'操作符。

            在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

        `有`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.has "Permalink to this definition")
        :   *inherited from the* [`has()`](#sqlalchemy.orm.interfaces.PropComparator.has "sqlalchemy.orm.interfaces.PropComparator.has")
            *method of* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

            如果此元素引用符合给定条件的成员，则返回true。

            The usual implementation of `has()` is
            [`RelationshipProperty.Comparator.has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has").

            参数：

            -   **criterion**[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.has.params.criterion)
                – an optional ClauseElement formulated against the
                member class’ table or attributes.
            -   **\*\*kwargs**[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.has.params.**kwargs)
                – key/value pairs corresponding to member class
                attribute names which will be compared via equality to
                the corresponding values.

        `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.ilike "Permalink to this definition")
        :   *inherited from the* [`ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`ilike`运算符。

            在列上下文中，生成子句`a ILIKE 其他`。

            例如。：

                select([sometable]).where(sometable.c.column.ilike("%foobar%"))

            参数：

            -   **其他**
                [¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.ilike.params.other)
                - 要比较的表达式
            -   **转义**
                [¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.ilike.params.escape)
                -

                可选的转义字符，呈现`ESCAPE`关键字，例如：

                    somecolumn.ilike("foo/%bar", escape="/")

            也可以看看

            [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

        `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            在运算符中实现`in`

            在列上下文中，生成子句`a IN 其他`。“other”可以是列表达式的元组/列表，或者是[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

        `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`IS`运算符。

            通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

            New in version 0.7.9.

            也可以看看

            [`ColumnOperators.isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

        ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`is_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
            *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现`IS DISTINCT FROM`运算符。

            在大多数平台上呈现“一个IS DISTINCT FROM
            b”；在一些如SQLite可能会呈现“一个不是b”。

            版本1.1中的新功能

        ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`IS NOT`运算符。

            Normally, `IS NOT` is generated
            automatically when comparing to a value of `None`, which resolves to `NULL`.
            但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

            New in version 0.7.9.

            也可以看看

            [`ColumnOperators.is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

        ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`isnot_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现`IS NOT DISTINCT FROM`运算符。

            在大多数平台上呈现“不是从BIND DISTINCT FROM
            b”；在某些例如SQLite上可能会呈现“a IS b”。

            版本1.1中的新功能

        `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.like "Permalink to this definition")
        :   *inherited from the* [`like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            像运算符一样实现`like`

            在列上下文中，生成子句`a LIKE 其他`。

            例如。：

                select([sometable]).where(sometable.c.column.like("%foobar%"))

            参数：

            -   **其他**
                [¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.like.params.other)
                - 要比较的表达式
            -   **转义**
                [¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.like.params.escape)
                -

                可选的转义字符，呈现`ESCAPE`关键字，例如：

                    somecolumn.like("foo/%bar", escape="/")

            也可以看看

            [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

        `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.match "Permalink to this definition")
        :   *继承自* [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
            *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现数据库特定的“匹配”运算符。

            [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
            attempts to resolve to a MATCH-like function or operator
            provided by the backend. 例子包括：

            -   Postgresql - 呈现`x @@ to_tsquery（y）`
            -   MySQL - renders
                `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
            -   Oracle - 呈现`CONTAINS（x， y）`
            -   其他后端可能会提供特殊的实现。
            -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

         `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.notilike "Permalink to this definition")
        :   *inherited from the* [`notilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            执行`NOT ILIKE`运算符。

            这相当于对[`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

            0.8版本中的新功能

            也可以看看

            [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

        ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
            *方法 [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            执行`NOT IN`运算符。

            这相当于对[`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

            0.8版本中的新功能

            也可以看看

            [`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

        `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.notlike "Permalink to this definition")
        :   *inherited from the* [`notlike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            执行`NOT LIKE`运算符。

            这相当于对[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

            0.8版本中的新功能

            也可以看看

            [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

        ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *inherited from the* [`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullsfirst "sqlalchemy.sql.operators.ColumnOperators.nullsfirst")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            针对父对象生成[`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

        ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`nullslast()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullslast "sqlalchemy.sql.operators.ColumnOperators.nullslast")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`nullslast()`](core_sqlelement.html#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

        ` of_type  T0> （ T1> 类_  T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`of_type()`](#sqlalchemy.orm.interfaces.PropComparator.of_type "sqlalchemy.orm.interfaces.PropComparator.of_type")
            *method of* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

            用多态子类重新定义这个对象。

            返回可以从中评估更多标准的新PropComparator。

            例如。：

                query.join(Company.employees.of_type(Engineer)).\
                   filter(Engineer.name=='foo')

            参数：

            **class\_**[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.of_type.params.class_)
            – a class or mapper indicating that criterion will be
            against this specific subclass.

        `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.op "Permalink to this definition")
        :   *继承自* [`op()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
            *方法的[`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

            产生通用的操作员功能。

            例如。：

                somecolumn.op("*")(5)

            生产：

                somecolumn * 5

            该函数也可用于使按位运算符明确。例如：

                somecolumn.op('&')(0xff)

            是`somecolumn`中的值的按位与。

            参数：

            -   **operator**[¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.op.params.operator)
                – a string which will be output as the infix operator
                between this element and the expression passed to the
                generated function.
            -   **优先顺序**
                [¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.op.params.precedence)
                -

                当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

                New in version 0.8: - added the ‘precedence’ argument.

            -   **is\_comparison**
                [¶](#sqlalchemy.orm.properties.ColumnProperty.Comparator.op.params.is_comparison)
                -

                如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
                true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

                版本0.9.2新增： -
                添加了[`Operators.op.is_comparison`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

            也可以看看

            [Redefining and Creating New
            Operators](core_custom_types.html#types-operators)

            [Using custom operators in join
            conditions](join_conditions.html#relationship-custom-operator)中使用自定义运算符

        `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.orm.properties.ColumnProperty.Comparator.startswith "Permalink to this definition")
        :   *inherited from the* [`startswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.startswith "sqlalchemy.sql.operators.ColumnOperators.startswith")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`startwith`运算符。

            在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

    `ColumnProperty。`{.descclassname} `__ init __`{.descname} （ *\*列*，*\*\* kwargs* / T5\> [¶ T6\>](#sqlalchemy.orm.properties.ColumnProperty.__init__ "Permalink to this definition")
    :   构建一个新的[`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property")。

    `ColumnProperty`{.descclassname} `cascade_iterator`{.descname} （ *type*，*状态*，*visited\_instances = / t5\>，*halt\_on = None* ） [¶](#sqlalchemy.orm.properties.ColumnProperty.cascade_iterator "Permalink to this definition")*
    :   *inherited from the* [`cascade_iterator()`](#sqlalchemy.orm.interfaces.MapperProperty.cascade_iterator "sqlalchemy.orm.interfaces.MapperProperty.cascade_iterator")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        从MapperProperty开始，迭代与特定“级联”相关的实例。

        返回一个iterator3-tuples（实例，映射器，状态）。

        请注意，在调用cascade\_iterator之前，此MapperProperty上的'cascade'集合将首先针对给定类型进行检查。

        此方法通常仅适用于RelationshipProperty。

    ` COLUMNPROPERTY。 T0>  class_attribute  T1> ¶ T2>`{.descclassname}
    :   *继承自 [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的*
        [`class_attribute`](#sqlalchemy.orm.interfaces.MapperProperty.class_attribute "sqlalchemy.orm.interfaces.MapperProperty.class_attribute")
        *属性*

        返回与此[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对应的类绑定描述符。

        这基本上是一个`getattr()`调用：

            return getattr(self.parent.class_, self.key)

        即如果这个[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")被命名为`addresses`，并且它映射到的类是`User`，那么这个序列是可能的：

            >>> from sqlalchemy import inspect
            >>> mapper = inspect(User)
            >>> addresses_property = mapper.attrs.addresses
            >>> addresses_property.class_attribute is User.addresses
            True
            >>> User.addresses.property is addresses_property
            True

    ` COLUMNPROPERTY。 T0> 表达 T1> ¶ T2>`{.descclassname}
    :   返回此ColumnProperty的主列或表达式。

    `ColumnProperty。`{.descclassname} `extension_type`{.descname} *=符号（'NOT\_EXTENSION'）* [¶](#sqlalchemy.orm.properties.ColumnProperty.extension_type "Permalink to this definition")
    :   

    ` COLUMNPROPERTY。 T0> 初始化 T1> （ T2> ） T3> ¶ T4>`{.descclassname}
    :   *inherited from the* [`init()`](#sqlalchemy.orm.interfaces.MapperProperty.init "sqlalchemy.orm.interfaces.MapperProperty.init")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        在创建所有映射器以调用映射器之间的关系并执行其他映射器创建初始化步骤后调用。

     `ColumnProperty.`{.descclassname}`set_parent`{.descname}(*parent*, *init*)[¶](#sqlalchemy.orm.properties.ColumnProperty.set_parent "Permalink to this definition")
    :   *inherited from the* [`set_parent()`](#sqlalchemy.orm.interfaces.MapperProperty.set_parent "sqlalchemy.orm.interfaces.MapperProperty.set_parent")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        设置引用此MapperProperty的父映射器。

        当映射器第一次知道时，此方法被一些子类覆盖以执行额外的设置。

*class* `sqlalchemy.orm.properties。`{.descclassname} `ComparableProperty`{.descname} （ *comparator\_factory*，*=无*，*doc =无*，*info =无* ） [¶](#sqlalchemy.orm.properties.ComparableProperty "Permalink to this definition")
:   基础：`sqlalchemy.orm.descriptor_props.DescriptorProperty`

    在查询表达式中使用Python属性。plain

     `__init__`{.descname}(*comparator\_factory*, *descriptor=None*, *doc=None*, *info=None*)[¶](#sqlalchemy.orm.properties.ComparableProperty.__init__ "Permalink to this definition")
    :   构建一个新的[`ComparableProperty`](#sqlalchemy.orm.properties.ComparableProperty "sqlalchemy.orm.properties.ComparableProperty")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅`comparable_property()`。

*class* `sqlalchemy.orm.descriptor_props。`{.descclassname} `CompositeProperty`{.descname} （ *class \_*，*\* attrs*，*\*\* kwargs* ） [¶](#sqlalchemy.orm.descriptor_props.CompositeProperty "Permalink to this definition")
:   基础：`sqlalchemy.orm.descriptor_props.DescriptorProperty`

    定义一个“复合”映射属性，将一组列作为一个属性表示。

    [`CompositeProperty`](#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty")是使用[`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")函数构造的。

    也可以看看

    [Composite Column Types](composites.html#mapper-composite)

    *class* `比较器`{.descname} （ *prop*，*parentmapper*，*adapt\_to\_entity = T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator "Permalink to this definition")*
    :   基础：[`sqlalchemy.orm.interfaces.PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        为[`CompositeProperty`](#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty")属性生成布尔型，比较和其他运算符。

        请参阅[Redefining Comparison Operations for
        Composites](composites.html#composite-operations)中的示例以了解用法概述以及[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")的文档。

        也可以看看：

        [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        [Redefining and Creating New
        Operators](core_custom_types.html#types-operators)

        [`TypeEngine.comparator_factory`](core_type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")

    `CompositeProperty。`{.descclassname} `__ init __`{.descname} （ *class \_*，*\* attrs*，*\*\* kwargs T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.descriptor_props.CompositeProperty.__init__ "Permalink to this definition")*
    :   构建一个新的[`CompositeProperty`](#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")。

    ` CompositeProperty。 T0>  do_init  T1> （ T2> ） T3> ¶ T4>`{.descclassname}
    :   初始化发生在[`CompositeProperty`](#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty")与其父映射器关联之后。

     `CompositeProperty.`{.descclassname}`get_history`{.descname}(*state*, *dict\_*, *passive=symbol('PASSIVE\_OFF')*)[¶](#sqlalchemy.orm.descriptor_props.CompositeProperty.get_history "Permalink to this definition")
    :   为使用attributes.get\_history()的用户级代码提供。

*class* `sqlalchemy.orm.attributes。`{.descclassname} `Event`{.descname} （ *attribute\_impl*，*op T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.attributes.Event "Permalink to this definition")*
:   一个令牌在一系列属性事件中传播。

    作为事件来源的指标，同时也提供了控制属性操作链中传播的手段。plain

    The [`Event`](#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")
    object is sent as the `initiator` argument when
    dealing with the [`AttributeEvents.append()`](events.html#sqlalchemy.orm.events.AttributeEvents.append "sqlalchemy.orm.events.AttributeEvents.append"),
    [`AttributeEvents.set()`](events.html#sqlalchemy.orm.events.AttributeEvents.set "sqlalchemy.orm.events.AttributeEvents.set"),
    and [`AttributeEvents.remove()`](events.html#sqlalchemy.orm.events.AttributeEvents.remove "sqlalchemy.orm.events.AttributeEvents.remove")
    events.

    [`Event`](#sqlalchemy.orm.attributes.Event "sqlalchemy.orm.attributes.Event")对象当前由backref事件处理程序解释，并用于控制跨两个相互依赖的属性的操作传播。

    版本0.9.0中的新功能

    变量：

    -   [**impl**](core_type_basics.html#sqlalchemy.types.Interval.impl "sqlalchemy.types.Interval.impl")
        - `AttributeImpl`它是当前的事件发起者。
    -   [**op**](#sqlalchemy.orm.attributes.QueryableAttribute.op "sqlalchemy.orm.attributes.QueryableAttribute.op")
        - 符号`OP_APPEND`，`OP_REMOVE`或`OP_REPLACE`，指示源操作。

*class* `sqlalchemy.orm.identity。`{.descclassname} `IdentityMap`{.descname} [¶](#sqlalchemy.orm.identity.IdentityMap "Permalink to this definition")
:   `check_modified  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   如果任何 InstanceStates 存在已被标记为“已修改”，则返回 True。

*class* `sqlalchemy.orm.base。`{.descclassname} `InspectionAttr`{.descname} [¶](#sqlalchemy.orm.base.InspectionAttr "Permalink to this definition")
:   基类应用于所有可由[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")函数返回的 ORM 对象。

    这里定义的属性允许使用简单的布尔检查来测试返回对象的基本事实。

    虽然这里的布尔检查与使用Python
    isinstance()函数基本相同，但可以在不需要导入所有这些类的情况下使用此处的标记，还可以使SQLAlchemy类系统更改，同时保持标记处于完整状态为了向前兼容。

    `extension_type`{.descname} *=符号（'NOT\_EXTENSION'）* [¶](#sqlalchemy.orm.base.InspectionAttr.extension_type "Permalink to this definition")
    :   扩展类型，如果有的话。默认为[`interfaces.NOT_EXTENSION`](#sqlalchemy.orm.interfaces.NOT_EXTENSION "sqlalchemy.orm.interfaces.NOT_EXTENSION")

        0.8.0版本中的新功能

        也可以看看

        [`HYBRID_METHOD`](extensions_hybrid.html#sqlalchemy.ext.hybrid.HYBRID_METHOD "sqlalchemy.ext.hybrid.HYBRID_METHOD")

        [`HYBRID_PROPERTY`](extensions_hybrid.html#sqlalchemy.ext.hybrid.HYBRID_PROPERTY "sqlalchemy.ext.hybrid.HYBRID_PROPERTY")

        [`ASSOCIATION_PROXY`](extensions_associationproxy.html#sqlalchemy.ext.associationproxy.ASSOCIATION_PROXY "sqlalchemy.ext.associationproxy.ASSOCIATION_PROXY")

    `is_aliased_class`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_aliased_class "Permalink to this definition")
    :   如果此对象是[`AliasedClass`](query.html#sqlalchemy.orm.util.AliasedClass "sqlalchemy.orm.util.AliasedClass")的实例，则为true。

    `is_attribute`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_attribute "Permalink to this definition")
    :   如果此对象是Python
        [descriptor](glossary.html#term-descriptor)，则为真。

        这可以指许多类型之一。通常是一个[`QueryableAttribute`](#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")，它代表[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")处理属性事件。但也可以是扩展类型，如[`AssociationProxy`](extensions_associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy "sqlalchemy.ext.associationproxy.AssociationProxy")或[`hybrid_property`](extensions_hybrid.html#sqlalchemy.ext.hybrid.hybrid_property "sqlalchemy.ext.hybrid.hybrid_property")。[`InspectionAttr.extension_type`](#sqlalchemy.orm.base.InspectionAttr.extension_type "sqlalchemy.orm.base.InspectionAttr.extension_type")将引用标识特定子类型的常量。

        也可以看看

        [`Mapper.all_orm_descriptors`](mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")

    `is_clause_element`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_clause_element "Permalink to this definition")
    :   如果此对象是[`ClauseElement`](core_sqlelement.html#sqlalchemy.sql.expression.ClauseElement "sqlalchemy.sql.expression.ClauseElement")的实例，则为true。

    `is_instance`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_instance "Permalink to this definition")
    :   如果此对象是[`InstanceState`](#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")的实例，则为true。

    `is_mapper`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_mapper "Permalink to this definition")
    :   如果此对象是[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")的实例，则为true。

    `is_property`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_property "Permalink to this definition")
    :   如果此对象是[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的实例，则为true。

    `is_selectable`{.descname} *= False* [¶](#sqlalchemy.orm.base.InspectionAttr.is_selectable "Permalink to this definition")
    :   如果此对象是[`Selectable`](core_selectable.html#sqlalchemy.sql.expression.Selectable "sqlalchemy.sql.expression.Selectable")的实例，则返回True。

*class* `sqlalchemy.orm.base。`{.descclassname} `InspectionAttrInfo`{.descname} [¶](#sqlalchemy.orm.base.InspectionAttrInfo "Permalink to this definition")
:   基础：[`sqlalchemy.orm.base.InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")

    将`.info`属性添加到[`InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")。

    The rationale for [`InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")
    vs. [`InspectionAttrInfo`](#sqlalchemy.orm.base.InspectionAttrInfo "sqlalchemy.orm.base.InspectionAttrInfo")
    is that the former is compatible as a mixin for classes that specify
    `__slots__`; this is essentially an
    implementation artifact.

    `信息 T0> ¶ T1>`{.descname}
    :   信息字典与对象关联，允许用户定义的数据与这个[`InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")关联。

        字典在第一次访问时生成。Alternatively, it can be specified as a
        constructor argument to the [`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property"),
        [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
        or [`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
        functions.

        0.8版新增功能：增加了对所有[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")子类的.info支持。

        版本1.0.0更改： [`MapperProperty.info`](#MapperProperty.info "MapperProperty.info")也可以通过[`InspectionAttrInfo.info`](#sqlalchemy.orm.base.InspectionAttrInfo.info "sqlalchemy.orm.base.InspectionAttrInfo.info")属性在扩展类型上使用，以便它可以应用于更广泛的ORM和扩展结构。

        也可以看看

        [`QueryableAttribute.info`](#sqlalchemy.orm.attributes.QueryableAttribute.info "sqlalchemy.orm.attributes.QueryableAttribute.info")

        [`SchemaItem.info`](core_metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")

*class* `sqlalchemy.orm.state。`{.descclassname} `InstanceState`{.descname} （ *obj*，*manager T5\> ） T6\> [¶ T7\>](#sqlalchemy.orm.state.InstanceState "Permalink to this definition")*
:   基础：[`sqlalchemy.orm.base.InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")

    跟踪实例级别的状态信息。

    [`InstanceState`](#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")是SQLAlchemy
    ORM使用的关键对象，用于跟踪对象的状态；它是在实例化对象的时刻创建的，通常是SQLAlchemy应用于该类的`__init__()`方法的结果[instrumentation](glossary.html#term-instrumentation)。

    [`InstanceState`](#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")
    is also a semi-public object, available for runtime inspection as to
    the state of a mapped instance, including information such as its
    current status within a particular [`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")
    and details about data on individual attributes.
    为了获取[`InstanceState`](#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")对象的公共API是使用[`inspect()`](core_inspection.html#sqlalchemy.inspection.inspect "sqlalchemy.inspection.inspect")系统：

        >>> from sqlalchemy import inspect
        >>> insp = inspect(some_mapped_object)

    也可以看看

    [Runtime Inspection API](core_inspection.html)

    ` ATTRS  T0> ¶ T1>`{.descname}
    :   返回表示映射对象上每个属性的名称空间，包括其当前值和历史记录。

        返回的对象是[`AttributeState`](#sqlalchemy.orm.state.AttributeState "sqlalchemy.orm.state.AttributeState")的一个实例。该对象允许检查属性中的当前数据以及自上次刷新后的属性历史记录。

    `callables`{.descname} *=()* [¶](#sqlalchemy.orm.state.InstanceState.callables "Permalink to this definition")
    :   每个状态加载器可调用的名称空间可以关联。

        在SQLAlchemy
        1.0中，这仅用于通过查询选项设置的懒加载器/延迟加载器。

        以前，通过在此字典中存储指向InstanceState本身的链接，可调用符号也用于指示过期的属性。此角色现在由expired\_attributes集处理。

    `删除 T0> ¶ T1>`{.descname}
    :   如果对象[deleted](glossary.html#term-deleted)，则返回true。

        处于删除状态的对象保证不在其父节点[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的[`Session.identity_map`](session_api.html#sqlalchemy.orm.session.Session.identity_map "sqlalchemy.orm.session.Session.identity_map")内；但是如果会话的事务回滚，对象将被恢复到持久状态和身份映射。

        注意

        [`InstanceState.deleted`](#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")属性是指在“持久”和“分离”状态之间发生的对象的特定状态；一旦对象[detached](glossary.html#term-detached)，[`InstanceState.deleted`](#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")属性**不再返回True**；为了检测状态是否被删除，无论对象是否与[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")关联，请使用[`InstanceState.was_deleted`](#sqlalchemy.orm.state.InstanceState.was_deleted "sqlalchemy.orm.state.InstanceState.was_deleted")访问器。

        也可以看看

        [Quickie Intro to Object
        States](session_state_management.html#session-object-states)

    `分离 T0> ¶ T1>`{.descname}
    :   如果对象[detached](glossary.html#term-detached)，则返回true。

        也可以看看

        [Quickie Intro to Object
        States](session_state_management.html#session-object-states)

    `字典 T0> ¶ T1>`{.descname}
    :   返回对象使用的实例字典。

        在正常情况下，除非已配置备用仪器系统，否则这总是与映射对象的`__dict__`属性同义。

        在实际对象已被垃圾收集的情况下，这个访问器返回一个空白字典。

    `expired_attributes`{.descname} *=无* [¶](#sqlalchemy.orm.state.InstanceState.expired_attributes "Permalink to this definition")
    :   假设没有待处理的更改，将由管理器的延迟标量加载器加载的'过期'密钥集。

        另请参阅发生刷新操作时与此set相交的`unmodified`集合。

    ` has_identity  T0> ¶ T1>`{.descname}
    :   如果此对象具有标识关键字，则返回`True`。

        这应该始终与表达式`state.persistent 或 state.detached`具有相同的值。

    `身份 T0> ¶ T1>`{.descname}
    :   返回映射对象的映射标识。这是ORM持久保存的主键标识，它总是可以直接传递给[`Query.get()`](query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")。

        如果对象没有主键标识，则返回`None`。

        注意

        即使其属性包含主键值，在[transient](glossary.html#term-transient)或[pending](glossary.html#term-pending)
        **not**的对象上也会有一个映射的标识，直到它被刷新。

    ` identity_key  T0> ¶ T1>`{.descname}
    :   返回映射对象的身份密钥。

        这是用于在[`Session.identity_map`](session_api.html#sqlalchemy.orm.session.Session.identity_map "sqlalchemy.orm.session.Session.identity_map")映​​射中定位对象的关键。它包含由[`identity`](#sqlalchemy.orm.state.InstanceState.identity "sqlalchemy.orm.state.InstanceState.identity")返回的身份。

    `映射器 T0> ¶ T1>`{.descname}
    :   返回用于这个mapepd对象的[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。

    `对象 T0> ¶ T1>`{.descname}
    :   返回由[`InstanceState`](#sqlalchemy.orm.state.InstanceState "sqlalchemy.orm.state.InstanceState")表示的映射对象。

    `未决 T0> ¶ T1>`{.descname}
    :   如果对象[pending](glossary.html#term-pending)，则返回true。

        也可以看看

        [Quickie Intro to Object
        States](session_state_management.html#session-object-states)

    `持久 T0> ¶ T1>`{.descname}
    :   如果对象是[persistent](glossary.html#term-persistent)，则返回true。

        处于持久状态的对象保证位于其父节点[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")的[`Session.identity_map`](session_api.html#sqlalchemy.orm.session.Session.identity_map "sqlalchemy.orm.session.Session.identity_map")内。

        在版本1.1中更改：对于在刷新中“删除”的对象，[`InstanceState.persistent`](#sqlalchemy.orm.state.InstanceState.persistent "sqlalchemy.orm.state.InstanceState.persistent")访问器不再返回True。使用[`InstanceState.deleted`](#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")访问器来检测此状态。这允许“持久”状态保证身份映射中的成员身份。

        也可以看看

        [Quickie Intro to Object
        States](session_state_management.html#session-object-states)

    `会话 T0> ¶ T1>`{.descname}
    :   如果没有可用的，则返回此实例的拥有[`Session`](session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，或返回`None`。

        请注意，这里的结果在某些情况下可能与`obj 在 会话中的不同 T1>；一个被删除的对象会在 session中报告为不是，但是如果事务仍在进行中，该属性仍然会引用该会话。`只有在交易完成后，物品才能在正常情况下完全分离。

    `瞬态 T0> ¶ T1>`{.descname}
    :   如果对象[transient](glossary.html#term-transient)，则返回true。

        也可以看看

        [Quickie Intro to Object
        States](session_state_management.html#session-object-states)

    `卸载 T0> ¶ T1>`{.descname}
    :   返回没有加载值的一组键。

        这包括过期的属性和从未被填充或修改过的任何其他属性。

    `未修饰 T0> ¶ T1>`{.descname}
    :   返回没有未提交更改的密钥集

    ` unmodified_intersection  T0> （ T1> 键 T2> ） T3> ¶ T4>`{.descname}
    :   返回self.unmodified.intersection（键）。

    ` was_deleted  T0> ¶ T1>`{.descname}
    :   如果此对象处于或以前处于“已删除”状态且尚未恢复为持续状态，则返回True。

        一旦对象在flush中被删除，该标志返回True。当显式地或通过事务提交从会话中清除对象并进入“分离”状态时，该标志将继续报告为真。

        版本1.1中的新增功能： - 添加了[`orm.util.was_deleted()`](session_api.html#sqlalchemy.orm.util.was_deleted "sqlalchemy.orm.util.was_deleted")的本地方法形式。

        也可以看看

        [`InstanceState.deleted`](#sqlalchemy.orm.state.InstanceState.deleted "sqlalchemy.orm.state.InstanceState.deleted")
        - 指“已删除”状态

        [`orm.util.was_deleted()`](session_api.html#sqlalchemy.orm.util.was_deleted "sqlalchemy.orm.util.was_deleted")
        - 独立功能

        [Quickie Intro to Object
        States](session_state_management.html#session-object-states)

 *class*`sqlalchemy.orm.attributes.`{.descclassname}`InstrumentedAttribute`{.descname}(*class\_*, *key*, *impl=None*, *comparator=None*, *parententity=None*, *of\_type=None*)[¶](#sqlalchemy.orm.attributes.InstrumentedAttribute "Permalink to this definition")
:   基础：[`sqlalchemy.orm.attributes.QueryableAttribute`](#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")

    添加基本​​[descriptor](glossary.html#term-descriptor)方法的类绑定插装属性。

    有关大多数功能的描述，请参阅[`QueryableAttribute`](#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")。

    ` __删除__  T0> （ T1> 实例 T2> ） T3> ¶ T4>`{.descname}
    :   

     `__get__`{.descname}(*instance*, *owner*)[¶](#sqlalchemy.orm.attributes.InstrumentedAttribute.__get__ "Permalink to this definition")
    :   

     `__set__`{.descname}(*instance*, *value*)[¶](#sqlalchemy.orm.attributes.InstrumentedAttribute.__set__ "Permalink to this definition")
    :   

`sqlalchemy.orm.interfaces。`{.descclassname} `MANYTOONE`{.descname} *= symbol（'MANYTOONE'）* [¶](#sqlalchemy.orm.interfaces.MANYTOONE "Permalink to this definition")
:   指示[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的多对一方向。

    此符号通常由内部使用，但可能会暴露在某些API功能中。

`sqlalchemy.orm.interfaces。`{.descclassname} `MANYTOMANY`{.descname} *= symbol（'MANYTOMANY'）* [¶](#sqlalchemy.orm.interfaces.MANYTOMANY "Permalink to this definition")
:   指示[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的多对多方向。

    此符号通常由内部使用，但可能会暴露在某些API功能中。plain

*class* `sqlalchemy.orm.interfaces。`{.descclassname} `MapperProperty`{.descname} [¶](#sqlalchemy.orm.interfaces.MapperProperty "Permalink to this definition")
:   基础：`sqlalchemy.orm.base._MappedAttribute`，[`sqlalchemy.orm.base.InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")，`sqlalchemy.util.langhelpers.MemoizedSlots`

    表示由[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")映​​射的特定类属性。plain

    最常见的[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")是映射的[`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")，它在映射中表示为[`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")的实例，并且对另一个类的引用由[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")生成，在映射中表示为[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")的实例。

    `信息 T0> ¶ T1>`{.descname}
    :   信息字典与对象关联，允许用户定义的数据与这个[`InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")关联。

        字典在第一次访问时生成。Alternatively, it can be specified as a
        constructor argument to the [`column_property()`](mapping_columns.html#sqlalchemy.orm.column_property "sqlalchemy.orm.column_property"),
        [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship"),
        or [`composite()`](composites.html#sqlalchemy.orm.composite "sqlalchemy.orm.composite")
        functions.

        0.8版新增功能：增加了对所有[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")子类的.info支持。

        版本1.0.0中已更改： `InspectionAttr.info`从[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")移动，以便它可以应用于更广泛的ORM和扩展结构。

        也可以看看

        [`QueryableAttribute.info`](#sqlalchemy.orm.attributes.QueryableAttribute.info "sqlalchemy.orm.attributes.QueryableAttribute.info")

        [`SchemaItem.info`](core_metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")

    `cascade`{.descname} *= frozenset（[]）* [¶](#sqlalchemy.orm.interfaces.MapperProperty.cascade "Permalink to this definition")
    :   'cascade'属性名称的集合。

        在调用“cascade\_iterator”方法之前检查此集合。

        该集合通常仅适用于RelationshipProperty。

     `cascade_iterator`{.descname}(*type\_*, *state*, *visited\_instances=None*, *halt\_on=None*)[¶](#sqlalchemy.orm.interfaces.MapperProperty.cascade_iterator "Permalink to this definition")
    :   从MapperProperty开始，迭代与特定“级联”相关的实例。

        返回一个iterator3-tuples（实例，映射器，状态）。

        请注意，在调用cascade\_iterator之前，此MapperProperty上的'cascade'集合将首先针对给定类型进行检查。

        此方法通常仅适用于RelationshipProperty。

    ` class_attribute  T0> ¶ T1>`{.descname}
    :   返回与此[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对应的类绑定描述符。

        这基本上是一个`getattr()`调用：

            return getattr(self.parent.class_, self.key)

        即如果这个[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")被命名为`addresses`，并且它映射到的类是`User`，那么这个序列是可能的：

            >>> from sqlalchemy import inspect
            >>> mapper = inspect(User)
            >>> addresses_property = mapper.attrs.addresses
            >>> addresses_property.class_attribute is User.addresses
            True
            >>> User.addresses.property is addresses_property
            True

     `create_row_processor`{.descname}(*context*, *path*, *mapper*, *result*, *adapter*, *populators*)[¶](#sqlalchemy.orm.interfaces.MapperProperty.create_row_processor "Permalink to this definition")
    :   生成行处理函数并追加到给定的填充列表集。

    ` do_init  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   执行子类特定的初始化后映射器创建步骤。

        这是一个由`MapperProperty`对象的init()方法调用的模板方法。

    `初始化 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在创建所有映射器以调用映射器之间的关系并执行其他映射器创建初始化步骤后调用。

    ` instrument_class  T0> （ T1> 映射器 T2> ） T3> ¶ T4>`{.descname}
    :   Hook被Mapper调用到该属性，以启动由此MapperProperty管理的类属性的检测。

        这里的MapperProperty通常会调用属性模块来设置InstrumentedAttribute。

        这一步是设置InstrumentedAttribute的两个步骤中的第一步，并且在映射器设置过程的早期调用。

        第二步通常是init\_class\_attribute步骤，通过post\_instrument\_class()钩子从StrategizedProperty调用。这一步为InstrumentedAttribute（特别是“impl”）分配额外的状态，这个状态在MapperProperty确定了它需要做什么样的持久性管理（例如标量，对象，集合等）之后确定。

    `is_property`{.descname} *= True* [¶](#sqlalchemy.orm.interfaces.MapperProperty.is_property "Permalink to this definition")
    :   InspectionAttr接口的一部分；声明这个对象是一个映射器属性。

     `merge`{.descname}(*session*, *source\_state*, *source\_dict*, *dest\_state*, *dest\_dict*, *load*, *\_recursive*, *\_resolve\_conflict\_map*)[¶](#sqlalchemy.orm.interfaces.MapperProperty.merge "Permalink to this definition")
    :   合并由`MapperProperty`表示的属性从源到目标对象。

    ` post_instrument_class  T0> （ T1> 映射器 T2> ） T3> ¶ T4>`{.descname}
    :   执行init()完成后需要进行的仪器调整。

        给定的Mapper是调用操作的Mapper，在继承场景中可能不是与self.parent相同的映射器；但是，Mapper将始终至少成为self.parent的子映射器。

        该方法通常由StrategizedProperty使用，该方法将其委派给LoaderStrategy.init\_class\_attribute()以对类绑定的InstrumentedAttribute执行最终设置。

    `set_parent`{.descname} （ *父*，*init* ） [](#sqlalchemy.orm.interfaces.MapperProperty.set_parent "Permalink to this definition")
    :   设置引用此MapperProperty的父映射器。

        当映射器第一次知道时，此方法被一些子类覆盖以执行额外的设置。

     `setup`{.descname}(*context*, *entity*, *path*, *adapter*, *\*\*kwargs*)[¶](#sqlalchemy.orm.interfaces.MapperProperty.setup "Permalink to this definition")
    :   由Query调用以构造SQL语句。

        与目标映射器关联的每个MapperProperty处理查询上下文引用的语句，并根据需要添加列和/或标准。

`sqlalchemy.orm.interfaces。`{.descclassname} `NOT_EXTENSION`{.descname} *=符号（'NOT\_EXTENSION'）* [¶](#sqlalchemy.orm.interfaces.NOT_EXTENSION "Permalink to this definition")
:   指示不属于 sqlalchemy.ext 的`InspectionAttr`的符号。

    分配给[`InspectionAttr.extension_type`{](#sqlalchemy.orm.base.InspectionAttr.extension_type "sqlalchemy.orm.base.InspectionAttr.extension_type")属性。

`sqlalchemy.orm.interfaces。`{.descclassname} `ONETOMANY`{.descname} *= symbol（'ONETOMANY'）* [¶](#sqlalchemy.orm.interfaces.ONETOMANY "Permalink to this definition")
:   指示[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的一对多方向。

    此符号通常由内部使用，但可能会暴露在某些API功能中。

 *class*`sqlalchemy.orm.interfaces.`{.descclassname}`PropComparator`{.descname}(*prop*, *parentmapper*, *adapt\_to\_entity=None*)[¶](#sqlalchemy.orm.interfaces.PropComparator "Permalink to this definition")
:   基础：[`sqlalchemy.sql.operators.ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

    为[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象定义SQL运算符。plain

    SQLAlchemy允许在Core和ORM级别重新定义运算符。[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")
    is the base class of operator redefinition for ORM-level operations,
    including those of [`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty"),
    [`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty"),
    and [`CompositeProperty`](#sqlalchemy.orm.descriptor_props.CompositeProperty "sqlalchemy.orm.descriptor_props.CompositeProperty").

    注意

    随着SQLAlchemy 0.7中引入的混合属性的出现以及SQLAlchemy
    0.8中的核心级操作符重新定义，用户定义的[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")实例的用例非常罕见。请参阅[Hybrid
    Attributes](extensions_hybrid.html)以及[Redefining and Creating New
    Operators](core_custom_types.html#types-operators)。

    可以创建[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")的用户定义的子类。内置的Python比较和数学运算符方法，如[`operators.ColumnOperators.__eq__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")，[`operators.ColumnOperators.__lt__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")和[`operators.ColumnOperators.__add__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__add__ "sqlalchemy.sql.operators.ColumnOperators.__add__")，可以被覆盖以提供新的操作员行为。自定义[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")通过参数`comparator_factory`传递给[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")实例。在每种情况下，应使用[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")的适当子类：

        # definition of custom PropComparator subclasses

        from sqlalchemy.orm.properties import \
                                ColumnProperty,\
                                CompositeProperty,\
                                RelationshipProperty

        class MyColumnComparator(ColumnProperty.Comparator):
            def __eq__(self, other):
                return self.__clause_element__() == other

        class MyRelationshipComparator(RelationshipProperty.Comparator):
            def any(self, expression):
                "define the 'any' operation"
                # ...

        class MyCompositeComparator(CompositeProperty.Comparator):
            def __gt__(self, other):
                "redefine the 'greater than' operation"

                return sql.and_(*[a>b for a, b in
                                  zip(self.__clause_element__().clauses,
                                      other.__composite_values__())])


        # application of custom PropComparator subclasses

        from sqlalchemy.orm import column_property, relationship, composite
        from sqlalchemy import Column, String

        class SomeMappedClass(Base):
            some_column = column_property(Column("some_column", String),
                                comparator_factory=MyColumnComparator)

            some_relationship = relationship(SomeOtherClass,
                                comparator_factory=MyRelationshipComparator)

            some_composite = composite(
                    Column("a", String), Column("b", String),
                    comparator_factory=MyCompositeComparator
                )

    请注意，对于列级别运算符重新定义，通常使用[`TypeEngine.comparator_factory`](core_type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")属性在核心级别定义运算符更为简单。有关更多详细信息，请参阅[Redefining
    and Creating New
    Operators](core_custom_types.html#types-operators)。

    也可以看看：

    [`ColumnProperty.Comparator`](#sqlalchemy.orm.properties.ColumnProperty.Comparator "sqlalchemy.orm.properties.ColumnProperty.Comparator")

    [`RelationshipProperty.Comparator`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator "sqlalchemy.orm.properties.RelationshipProperty.Comparator")

    [`CompositeProperty.Comparator`](#sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator "sqlalchemy.orm.descriptor_props.CompositeProperty.Comparator")

    [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

    [Redefining and Creating New
    Operators](core_custom_types.html#types-operators)

    [`TypeEngine.comparator_factory`{](core_type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")

    ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`__eq__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实施`==`运算符。

        在列上下文中，生成子句`a = b`。If the target
        is `None`, produces `a IS NULL`.

    ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__le__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__le__ "sqlalchemy.sql.operators.ColumnOperators.__le__")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<=`运算符。

        在列上下文中，生成子句`a <= b`。

    ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__lt__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<`运算符。

        在列上下文中，生成子句`a  b`。

    ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__ne__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__ne__ "sqlalchemy.sql.operators.ColumnOperators.__ne__")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`!=`运算符。

        在列上下文中，生成子句`a ！= b`。If the
        target is `None`, produces
        `a IS NOT NULL`.

    ` adapt_to_entity  T0> （ T1>  adapt_to_entity  T2> ） T3> ¶ T4>`{.descname}
    :   返回此PropComparator的副本，它将使用给定的[`AliasedInsp`](query.html#sqlalchemy.orm.util.AliasedInsp "sqlalchemy.orm.util.AliasedInsp")生成相应的表达式。

    `适配器 T0> ¶ T1>`{.descname}
    :   生成一个可调用的列，适应列表达式以适应该比较器的别名版本。

    `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`all_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.all_ "sqlalchemy.sql.operators.ColumnOperators.all_")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

        版本1.1中的新功能

    `任何`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.interfaces.PropComparator.any "Permalink to this definition")
    :   如果此集合包含符合给定条件的任何成员，则返回true。

        `any()`的通常实现是[`RelationshipProperty.Comparator.any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")。

        参数：

        -   **criterion**[¶](#sqlalchemy.orm.interfaces.PropComparator.any.params.criterion)
            – an optional ClauseElement formulated against the member
            class’ table or attributes.
        -   **\*\*kwargs**[¶](#sqlalchemy.orm.interfaces.PropComparator.any.params.**kwargs)
            – key/value pairs corresponding to member class attribute
            names which will be compared via equality to the
            corresponding values.

    `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`any_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.any_ "sqlalchemy.sql.operators.ColumnOperators.any_")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

        版本1.1中的新功能

    ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`asc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.asc "sqlalchemy.sql.operators.ColumnOperators.asc")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`asc()`](core_sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

    `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
    :   *inherited from the* [`between()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在()子句之间针对父对象生成[`between()`](core_sqlelement.html#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

    `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        根据给定的排序字符串，针对父对象生成一个[`collate()`](core_sqlelement.html#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

    `的concat  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`concat()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现'concat'操作符。

        在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

    `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.orm.interfaces.PropComparator.contains "Permalink to this definition") \>
    :   *inherited from the* [`contains()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.contains "sqlalchemy.sql.operators.ColumnOperators.contains")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'包含'运算符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；％'`

    `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`desc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.desc "sqlalchemy.sql.operators.ColumnOperators.desc")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`desc()`](core_sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

    `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`distinct()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.distinct "sqlalchemy.sql.operators.ColumnOperators.distinct")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成一个[`distinct()`](core_sqlelement.html#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

    `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.interfaces.PropComparator.endswith "Permalink to this definition")
    :   *inherited from the* [`endswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.endswith "sqlalchemy.sql.operators.ColumnOperators.endswith")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'endswith'操作符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

    `有`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.interfaces.PropComparator.has "Permalink to this definition")
    :   如果此元素引用符合给定条件的成员，则返回true。

        The usual implementation of `has()` is
        [`RelationshipProperty.Comparator.has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has").

        参数：

        -   **criterion**[¶](#sqlalchemy.orm.interfaces.PropComparator.has.params.criterion)
            – an optional ClauseElement formulated against the member
            class’ table or attributes.
        -   **\*\*kwargs**[¶](#sqlalchemy.orm.interfaces.PropComparator.has.params.**kwargs)
            – key/value pairs corresponding to member class attribute
            names which will be compared via equality to the
            corresponding values.

    `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.interfaces.PropComparator.ilike "Permalink to this definition")
    :   *inherited from the* [`ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`ilike`运算符。

        在列上下文中，生成子句`a ILIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.ilike("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.ilike.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.ilike.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.ilike("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在运算符中实现`in`

        在列上下文中，生成子句`a IN 其他`。“other”可以是列表达式的元组/列表，或者是[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

    `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS`运算符。

        通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

    ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
        *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS DISTINCT FROM`运算符。

        在大多数平台上呈现“一个IS DISTINCT FROM
        b”；在一些如SQLite可能会呈现“一个不是b”。

        版本1.1中的新功能

    ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS NOT`运算符。

        Normally, `IS NOT` is generated
        automatically when comparing to a value of `None`, which resolves to `NULL`.
        但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

    ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`isnot_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS NOT DISTINCT FROM`运算符。

        在大多数平台上呈现“不是从BIND DISTINCT FROM
        b”；在某些例如SQLite上可能会呈现“a IS b”。

        版本1.1中的新功能

    `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.interfaces.PropComparator.like "Permalink to this definition")
    :   *inherited from the* [`like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        像运算符一样实现`like`

        在列上下文中，生成子句`a LIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.like("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.like.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.like.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.like("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.interfaces.PropComparator.match "Permalink to this definition")
    :   *继承自* [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现数据库特定的“匹配”运算符。

        [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        attempts to resolve to a MATCH-like function or operator
        provided by the backend. 例子包括：

        -   Postgresql - 呈现`x @@ to_tsquery（y）`
        -   MySQL - renders
            `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
        -   Oracle - 呈现`CONTAINS（x， y）`
        -   其他后端可能会提供特殊的实现。
        -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

     `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.orm.interfaces.PropComparator.notilike "Permalink to this definition")
    :   *inherited from the* [`notilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT ILIKE`运算符。

        这相当于对[`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
        *方法 [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        执行`NOT IN`运算符。

        这相当于对[`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

    `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.orm.interfaces.PropComparator.notlike "Permalink to this definition")
    :   *inherited from the* [`notlike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT LIKE`运算符。

        这相当于对[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullsfirst "sqlalchemy.sql.operators.ColumnOperators.nullsfirst")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

    ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`nullslast()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullslast "sqlalchemy.sql.operators.ColumnOperators.nullslast")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`nullslast()`](core_sqlelement.html#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

    ` of_type  T0> （ T1> 类_  T2> ） T3> ¶ T4>`{.descname}
    :   用多态子类重新定义这个对象。

        返回可以从中评估更多标准的新PropComparator。

        例如。：

            query.join(Company.employees.of_type(Engineer)).\
               filter(Engineer.name=='foo')

        参数：

        **class\_**[¶](#sqlalchemy.orm.interfaces.PropComparator.of_type.params.class_)
        – a class or mapper indicating that criterion will be against
        this specific subclass.

    `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.orm.interfaces.PropComparator.op "Permalink to this definition")
    :   *继承自* [`op()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
        *方法的[`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

        产生通用的操作员功能。

        例如。：

            somecolumn.op("*")(5)

        生产：

            somecolumn * 5

        该函数也可用于使按位运算符明确。例如：

            somecolumn.op('&')(0xff)

        是`somecolumn`中的值的按位与。

        参数：

        -   **operator**[¶](#sqlalchemy.orm.interfaces.PropComparator.op.params.operator)
            – a string which will be output as the infix operator
            between this element and the expression passed to the
            generated function.
        -   **优先顺序**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.op.params.precedence)
            -

            当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

            New in version 0.8: - added the ‘precedence’ argument.

        -   **is\_comparison**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.op.params.is_comparison)
            -

            如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
            true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

            版本0.9.2新增： - 添加了[`Operators.op.is_comparison`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

        也可以看看

        [Redefining and Creating New
        Operators](core_custom_types.html#types-operators)

        [Using custom operators in join
        conditions](join_conditions.html#relationship-custom-operator)中使用自定义运算符

    `操作 tt> （ op，*其他，** kwargs / T5> ¶ T6>`{.descname}
    :   *继承自* [`operate()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")
        *方法* [`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

        操作一个参数。

        这是最低级别的操作，缺省情况下会引发`NotImplementedError`。

        在子类上覆盖它可以使普通行为适用于所有操作。例如，覆盖[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")将`func.lower()`应用于左侧和右侧：

            class MyComparator(ColumnOperators):
                def operate(self, op, other):
                    return op(func.lower(self), func.lower(other))

        参数：

        -   **op**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.operate.params.op)
            - 操作员可调用。
        -   **\*其他**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.operate.params.*other)
            -
            操作的“其他”一侧。对于大多数操作来说，这将是一个单一的标量。
        -   **\*\* kwargs**
            [¶](#sqlalchemy.orm.interfaces.PropComparator.operate.params.**kwargs)
            -
            修饰符。这些可以由特殊的操作符传递，如`ColumnOperators.contains()`。

    `reverse_operate`{.descname} （ *op*，*其他*，*\*\* kwargs* T5\> [¶ T6\>](#sqlalchemy.orm.interfaces.PropComparator.reverse_operate "Permalink to this definition")
    :   *inherited from the* [`reverse_operate()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.reverse_operate "sqlalchemy.sql.operators.Operators.reverse_operate")
        *method of* [`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

        对参数进行反向操作。

        用法与`operate()`相同。

    `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.orm.interfaces.PropComparator.startswith "Permalink to this definition")
    :   *inherited from the* [`startswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.startswith "sqlalchemy.sql.operators.ColumnOperators.startswith")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`startwith`运算符。

        在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

 *class*`sqlalchemy.orm.properties.`{.descclassname}`RelationshipProperty`{.descname}(*argument*, *secondary=None*, *primaryjoin=None*, *secondaryjoin=None*, *foreign\_keys=None*, *uselist=None*, *order\_by=False*, *backref=None*, *back\_populates=None*, *post\_update=False*, *cascade=False*, *extension=None*, *viewonly=False*, *lazy=True*, *collection\_class=None*, *passive\_deletes=False*, *passive\_updates=True*, *remote\_side=None*, *enable\_typechecks=True*, *join\_depth=None*, *comparator\_factory=None*, *single\_parent=False*, *innerjoin=False*, *distinct\_target\_key=None*, *doc=None*, *active\_history=False*, *cascade\_backrefs=True*, *load\_on\_pending=False*, *bake\_queries=True*, *strategy\_class=None*, *\_local\_remote\_pairs=None*, *query\_class=None*, *info=None*)[¶](#sqlalchemy.orm.properties.RelationshipProperty "Permalink to this definition")
:   基础：`sqlalchemy.orm.interfaces.StrategizedProperty`

    描述保存与相关数据库表对应的单个项目或项目列表的对象属性。plain

    公共构造函数是[`orm.relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")函数。

    也可以看看：

    [Relationship Configuration](relationships.html)

    *class* `比较器`{.descname} （ *prop*，*parentmapper*，*adapt\_to\_entity = t5\>，*of\_type = None* ） [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator "Permalink to this definition")*
    :   基础：[`sqlalchemy.orm.interfaces.PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        为[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")属性生成布尔型，比较型和其他运算符。

        有关ORM级别操作符定义的简要概述，请参阅[`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")的文档。

        也可以看看：

        [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        [`ColumnProperty.Comparator`](#sqlalchemy.orm.properties.ColumnProperty.Comparator "sqlalchemy.orm.properties.ColumnProperty.Comparator")

        [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        [Redefining and Creating New
        Operators](core_custom_types.html#types-operators)

        [`TypeEngine.comparator_factory`](core_type_api.html#sqlalchemy.types.TypeEngine.comparator_factory "sqlalchemy.types.TypeEngine.comparator_factory")

        ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   实施`==`运算符。

            在多对一的情况下，比如：

                MyClass.some_prop == <some object>

            这通常会产生一个条款，例如：

                mytable.related_id == <some id>

            其中`＆lt； some id＆gt；`是给定对象的主键。

            `==`运算符提供了非多对一比较的部分功能：

            -   不支持与集合的比较。使用[`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")。
            -   与标量一对多比较，将生成一个子句，将父级中的目标列与给定目标进行比较。
            -   与标量多对多相比，关联表的别名也将被渲染，形成查询主体的一部分的自然连接。这不适用于超出简单和比较连接的查询，例如那些使用OR的查询。使用显式连接，外连接或[`has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")来进行更全面的非多对一标量成员测试。
            -   在一对多或多对多的上下文中给出的与`None`的比较产生NOT EXISTS子句。

         `__init__`{.descname}(*prop*, *parentmapper*, *adapt\_to\_entity=None*, *of\_type=None*)[¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.__init__ "Permalink to this definition")
        :   [`RelationshipProperty.Comparator`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator "sqlalchemy.orm.properties.RelationshipProperty.Comparator")的结构是ORM属性结构的内部结构。

        ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`__le__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__le__ "sqlalchemy.sql.operators.ColumnOperators.__le__")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`<=`运算符。

            在列上下文中，生成子句`a <= b`。

        ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`__lt__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`<`运算符。

            在列上下文中，生成子句`a  b`。

        ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   实现`!=`运算符。

            在多对一的情况下，比如：

                MyClass.some_prop != <some object>

            这通常会产生一个条款，例如：

                mytable.related_id != <some id>

            其中`＆lt； some id＆gt；`是给定对象的主键。

            `!=`运算符提供了非多对一比较的部分功能：

            -   不支持与集合的比较。将[`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")与[`not_()`](core_sqlelement.html#sqlalchemy.sql.expression.not_ "sqlalchemy.sql.expression.not_")结合使用。
            -   与标量一对多比较，将生成一个子句，将父级中的目标列与给定目标进行比较。
            -   与标量多对多相比，关联表的别名也将被渲染，形成查询主体的一部分的自然连接。这不适用于超出简单和比较连接的查询，例如那些使用OR的查询。使用显式连接，外连接或[`has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")与[`not_()`](core_sqlelement.html#sqlalchemy.sql.expression.not_ "sqlalchemy.sql.expression.not_")配合使用，以获得更全面的非多对一标量成员资格测试。
            -   在一对多或多对多的上下文中给出的与`None`的比较产生了EXISTS子句。

        `适配器 T0> ¶ T1>`{.descname}
        :   *继承自* [`adapter`](#sqlalchemy.orm.interfaces.PropComparator.adapter "sqlalchemy.orm.interfaces.PropComparator.adapter")
            *属性的* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

            生成一个可调用的列，适应列表达式以适应该比较器的别名版本。

        `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`all_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.all_ "sqlalchemy.sql.operators.ColumnOperators.all_")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

            版本1.1中的新功能

        `任何`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "Permalink to this definition")
        :   根据特定标准生成一个表达式，使用EXISTS测试集合。

            表达式如下：

                session.query(MyClass).filter(
                    MyClass.somereference.any(SomeRelated.x==2)
                )

            将产生如下查询：

                SELECT * FROM my_table WHERE
                EXISTS (SELECT 1 FROM related WHERE related.my_id=my_table.id
                AND related.x=2)

            由于[`any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")使用相关的子查询，因此与大型目标表相比，其性能几乎不如使用连接的性能好。

            [`any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")
            is particularly useful for testing for empty collections:

                session.query(MyClass).filter(
                    ~MyClass.somereference.any()
                )

            会产生：

                SELECT * FROM my_table WHERE
                NOT EXISTS (SELECT 1 FROM related WHERE
                related.my_id=my_table.id)

            [`any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")
            is only valid for collections, i.e. a
            [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
            that has `uselist=True`.
            对于标量引用，请使用[`has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")。

        `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *inherited from the* [`any_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.any_ "sqlalchemy.sql.operators.ColumnOperators.any_")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            针对父对象生成[`any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

            版本1.1中的新功能

        ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`asc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.asc "sqlalchemy.sql.operators.ColumnOperators.asc")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`asc()`](core_sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

        `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
        :   *inherited from the* [`between()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            在()子句之间针对父对象生成[`between()`](core_sqlelement.html#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

        `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            根据给定的排序字符串，针对父对象生成一个[`collate()`](core_sqlelement.html#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

        `的concat  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`concat()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现'concat'操作符。

            在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

        `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "Permalink to this definition") \>
        :   返回一个简单的表达式，用于测试集合是否包含特定的项目。

            [`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")仅对集合有效，即[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")用`uselist=True`

            当在简单的一对多上下文中使用时，表达式如下所示：

                MyClass.contains(other)

            生成一个子句，如：

                mytable.id == <some id>

            Where `<some id>` is the value of the
            foreign key attribute on `other` which
            refers to the primary key of its parent object.
            由此可见，当与简单的一对多操作一起使用时，[`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")非常有用。

            对于多对多操作，[`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")的行为有更多的注意事项。关联表将在语句中呈现，产生“隐式”连接，即在FROM子句中包含多个等同于WHERE子句的表：

                query(MyClass).filter(MyClass.contains(other))

            产生如下查询：

                SELECT * FROM my_table, my_association_table AS
                my_association_table_1 WHERE
                my_table.id = my_association_table_1.parent_id
                AND my_association_table_1.child_id = <some id>

            Where `<some id>` would be the primary
            key of `other`. From the above, it is
            clear that [`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")
            will **not** work with many-to-many collections when used in
            queries that move beyond simple AND conjunctions, such as
            multiple [`contains()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains")
            expressions joined by OR.
            在这种情况下，需要使用子查询或明确的“外连接”。请参阅[`any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")查找使用EXISTS的较低性能替代方法，或参考[`Query.outerjoin()`](query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin")以及[Querying
            with
            Joins](tutorial.html#ormtutorial-joins)有关构建外连接的详细信息。

        `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`desc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.desc "sqlalchemy.sql.operators.ColumnOperators.desc")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`desc()`](core_sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

        `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *inherited from the* [`distinct()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.distinct "sqlalchemy.sql.operators.ColumnOperators.distinct")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            针对父对象生成一个[`distinct()`](core_sqlelement.html#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

        `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.endswith "Permalink to this definition")
        :   *inherited from the* [`endswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.endswith "sqlalchemy.sql.operators.ColumnOperators.endswith")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现'endswith'操作符。

            在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

        `有`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "Permalink to this definition")
        :   使用EXISTS生成一个表达式，该表达式根据特定标准测试标量引用。

            表达式如下：

                session.query(MyClass).filter(
                    MyClass.somereference.has(SomeRelated.x==2)
                )

            将产生如下查询：

                SELECT * FROM my_table WHERE
                EXISTS (SELECT 1 FROM related WHERE
                related.id==my_table.related_id AND related.x=2)

            由于[`has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")使用相关的子查询，因此与大型目标表相比，其性能几乎不如使用连接的性能好。

            [`has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")
            is only valid for scalar references, i.e. a
            [`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")
            that has `uselist=False`.
            对于集合引用，请使用[`any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")。

        `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.ilike "Permalink to this definition")
        :   *inherited from the* [`ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`ilike`运算符。

            在列上下文中，生成子句`a ILIKE 其他`。

            例如。：

                select([sometable]).where(sometable.c.column.ilike("%foobar%"))

            参数：

            -   **其他**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.ilike.params.other)
                - 要比较的表达式
            -   **转义**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.ilike.params.escape)
                -

                可选的转义字符，呈现`ESCAPE`关键字，例如：

                    somecolumn.ilike("foo/%bar", escape="/")

            也可以看看

            [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

        `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   产生一个IN子句 - 目前还没有为[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")实现属性。

        `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`IS`运算符。

            通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

            New in version 0.7.9.

            也可以看看

            [`ColumnOperators.isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

        ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`is_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
            *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现`IS DISTINCT FROM`运算符。

            在大多数平台上呈现“一个IS DISTINCT FROM
            b”；在一些如SQLite可能会呈现“一个不是b”。

            版本1.1中的新功能

        ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *inherited from the* [`isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`IS NOT`运算符。

            Normally, `IS NOT` is generated
            automatically when comparing to a value of `None`, which resolves to `NULL`.
            但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

            New in version 0.7.9.

            也可以看看

            [`ColumnOperators.is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

        ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`isnot_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现`IS NOT DISTINCT FROM`运算符。

            在大多数平台上呈现“不是从BIND DISTINCT FROM
            b”；在某些例如SQLite上可能会呈现“a IS b”。

            版本1.1中的新功能

        `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.like "Permalink to this definition")
        :   *inherited from the* [`like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            像运算符一样实现`like`

            在列上下文中，生成子句`a LIKE 其他`。

            例如。：

                select([sometable]).where(sometable.c.column.like("%foobar%"))

            参数：

            -   **其他**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.like.params.other)
                - 要比较的表达式
            -   **转义**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.like.params.escape)
                -

                可选的转义字符，呈现`ESCAPE`关键字，例如：

                    somecolumn.like("foo/%bar", escape="/")

            也可以看看

            [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

        `映射器 T0> ¶ T1>`{.descname}
        :   由[`RelationshipProperty.Comparator`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator "sqlalchemy.orm.properties.RelationshipProperty.Comparator")引用的目标[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。

            这是[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")的“目标”或“远程”端。

        `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.match "Permalink to this definition")
        :   *继承自* [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
            *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            实现数据库特定的“匹配”运算符。

            [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
            attempts to resolve to a MATCH-like function or operator
            provided by the backend. 例子包括：

            -   Postgresql - 呈现`x @@ to_tsquery（y）`
            -   MySQL - renders
                `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
            -   Oracle - 呈现`CONTAINS（x， y）`
            -   其他后端可能会提供特殊的实现。
            -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

         `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.notilike "Permalink to this definition")
        :   *inherited from the* [`notilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            执行`NOT ILIKE`运算符。

            这相当于对[`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

            0.8版本中的新功能

            也可以看看

            [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

        ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
        :   *继承自* [`notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
            *方法 [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            执行`NOT IN`运算符。

            这相当于对[`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

            0.8版本中的新功能

            也可以看看

            [`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

        `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.notlike "Permalink to this definition")
        :   *inherited from the* [`notlike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            执行`NOT LIKE`运算符。

            这相当于对[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

            0.8版本中的新功能

            也可以看看

            [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

        ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *inherited from the* [`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullsfirst "sqlalchemy.sql.operators.ColumnOperators.nullsfirst")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            针对父对象生成[`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

        ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
        :   *继承自* [`nullslast()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullslast "sqlalchemy.sql.operators.ColumnOperators.nullslast")
            *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

            针对父对象生成一个[`nullslast()`](core_sqlelement.html#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

        ` of_type  T0> （ T1>  CLS  T2> ） T3> ¶ T4>`{.descname}
        :   生成一个表示父类的特定“子类型”属性的构造。

            目前，这可与[`Query.join()`](query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")和[`Query.outerjoin()`](query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin")结合使用。

        `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.op "Permalink to this definition")
        :   *继承自* [`op()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
            *方法的[`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

            产生通用的操作员功能。

            例如。：

                somecolumn.op("*")(5)

            生产：

                somecolumn * 5

            该函数也可用于使按位运算符明确。例如：

                somecolumn.op('&')(0xff)

            是`somecolumn`中的值的按位与。

            参数：

            -   **operator**[¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.op.params.operator)
                – a string which will be output as the infix operator
                between this element and the expression passed to the
                generated function.
            -   **优先顺序**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.op.params.precedence)
                -

                当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

                New in version 0.8: - added the ‘precedence’ argument.

            -   **is\_comparison**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.op.params.is_comparison)
                -

                如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
                true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

                版本0.9.2新增： -
                添加了[`Operators.op.is_comparison`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

            也可以看看

            [Redefining and Creating New
            Operators](core_custom_types.html#types-operators)

            [Using custom operators in join
            conditions](join_conditions.html#relationship-custom-operator)中使用自定义运算符

        `操作 tt> （ op，*其他，** kwargs / T5> ¶ T6>`{.descname}
        :   *继承自* [`operate()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.operate "sqlalchemy.sql.operators.Operators.operate")
            *方法* [`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

            操作一个参数。

            这是最低级别的操作，缺省情况下会引发`NotImplementedError`。

            在子类上覆盖它可以使普通行为适用于所有操作。例如，覆盖[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")将`func.lower()`应用于左侧和右侧：

                class MyComparator(ColumnOperators):
                    def operate(self, op, other):
                        return op(func.lower(self), func.lower(other))

            参数：

            -   **op**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.operate.params.op)
                - 操作员可调用。
            -   **\*其他**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.operate.params.*other)
                -
                操作的“其他”一侧。对于大多数操作来说，这将是一个单一的标量。
            -   **\*\* kwargs**
                [¶](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.operate.params.**kwargs)
                -
                修饰符。这些可以由特殊的操作符传递，如`ColumnOperators.contains()`。

        `reverse_operate`{.descname} （ *op*，*其他*，*\*\* kwargs* T5\> [¶ T6\>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.reverse_operate "Permalink to this definition")
        :   *inherited from the* [`reverse_operate()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.reverse_operate "sqlalchemy.sql.operators.Operators.reverse_operate")
            *method of* [`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")

            对参数进行反向操作。

            用法与`operate()`相同。

        `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.startswith "Permalink to this definition")
        :   *inherited from the* [`startswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.startswith "sqlalchemy.sql.operators.ColumnOperators.startswith")
            *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

            实现`startwith`运算符。

            在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

     `RelationshipProperty.`{.descclassname}`__init__`{.descname}(*argument*, *secondary=None*, *primaryjoin=None*, *secondaryjoin=None*, *foreign\_keys=None*, *uselist=None*, *order\_by=False*, *backref=None*, *back\_populates=None*, *post\_update=False*, *cascade=False*, *extension=None*, *viewonly=False*, *lazy=True*, *collection\_class=None*, *passive\_deletes=False*, *passive\_updates=True*, *remote\_side=None*, *enable\_typechecks=True*, *join\_depth=None*, *comparator\_factory=None*, *single\_parent=False*, *innerjoin=False*, *distinct\_target\_key=None*, *doc=None*, *active\_history=False*, *cascade\_backrefs=True*, *load\_on\_pending=False*, *bake\_queries=True*, *strategy\_class=None*, *\_local\_remote\_pairs=None*, *query\_class=None*, *info=None*)[¶](#sqlalchemy.orm.properties.RelationshipProperty.__init__ "Permalink to this definition")
    :   构建一个新的[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`relationship()`](relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")。

    ` RelationshipProperty。 T0> 级联 T1> ¶ T2>`{.descclassname}
    :   返回该[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")的当前级联设置。

    ` RelationshipProperty。 T0>  class_attribute  T1> ¶ T2>`{.descclassname}
    :   *继承自 [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的*
        [`class_attribute`](#sqlalchemy.orm.interfaces.MapperProperty.class_attribute "sqlalchemy.orm.interfaces.MapperProperty.class_attribute")
        *属性*

        返回与此[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对应的类绑定描述符。

        这基本上是一个`getattr()`调用：

            return getattr(self.parent.class_, self.key)

        即如果这个[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")被命名为`addresses`，并且它映射到的类是`User`，那么这个序列是可能的：

            >>> from sqlalchemy import inspect
            >>> mapper = inspect(User)
            >>> addresses_property = mapper.attrs.addresses
            >>> addresses_property.class_attribute is User.addresses
            True
            >>> User.addresses.property is addresses_property
            True

    `RelationshipProperty`{.descclassname} `extension_type`{.descname} *=符号（'NOT\_EXTENSION'）* [¶](#sqlalchemy.orm.properties.RelationshipProperty.extension_type "Permalink to this definition")
    :   

    ` RelationshipProperty。 T0> 初始化 T1> （ T2> ） T3> ¶ T4>`{.descclassname}
    :   *inherited from the* [`init()`](#sqlalchemy.orm.interfaces.MapperProperty.init "sqlalchemy.orm.interfaces.MapperProperty.init")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        在创建所有映射器以调用映射器之间的关系并执行其他映射器创建初始化步骤后调用。

    ` RelationshipProperty。 T0> 映射器 T1> ¶ T2>`{.descclassname}
    :   返回这个[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")的目标[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")。

        这是一个惰性初始化静态属性。

     `RelationshipProperty.`{.descclassname}`set_parent`{.descname}(*parent*, *init*)[¶](#sqlalchemy.orm.properties.RelationshipProperty.set_parent "Permalink to this definition")
    :   *inherited from the* [`set_parent()`](#sqlalchemy.orm.interfaces.MapperProperty.set_parent "sqlalchemy.orm.interfaces.MapperProperty.set_parent")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        设置引用此MapperProperty的父映射器。

        当映射器第一次知道时，此方法被一些子类覆盖以执行额外的设置。

    ` RelationshipProperty。 T0> 表 T1> ¶ T2>`{.descclassname}
    :   返回链接到[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")对象的目标[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")的可选项。

        从版本0.7开始弃用：使用.target

 *class*`sqlalchemy.orm.descriptor_props.`{.descclassname}`SynonymProperty`{.descname}(*name*, *map\_column=None*, *descriptor=None*, *comparator\_factory=None*, *doc=None*, *info=None*)[¶](#sqlalchemy.orm.descriptor_props.SynonymProperty "Permalink to this definition")
:   基础：`sqlalchemy.orm.descriptor_props.DescriptorProperty`

     `__init__`{.descname}(*name*, *map\_column=None*, *descriptor=None*, *comparator\_factory=None*, *doc=None*, *info=None*)[¶](#sqlalchemy.orm.descriptor_props.SynonymProperty.__init__ "Permalink to this definition")
    :   构建一个新的[`SynonymProperty`](#sqlalchemy.orm.descriptor_props.SynonymProperty "sqlalchemy.orm.descriptor_props.SynonymProperty")对象。

        这个构造函数被镜像为公共API函数；有关完整的用法和参数说明，请参阅[`synonym()`](mapped_attributes.html#sqlalchemy.orm.synonym "sqlalchemy.orm.synonym")。

     `cascade_iterator`{.descname}(*type\_*, *state*, *visited\_instances=None*, *halt\_on=None*)[¶](#sqlalchemy.orm.descriptor_props.SynonymProperty.cascade_iterator "Permalink to this definition")
    :   *inherited from the* [`cascade_iterator()`](#sqlalchemy.orm.interfaces.MapperProperty.cascade_iterator "sqlalchemy.orm.interfaces.MapperProperty.cascade_iterator")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        从MapperProperty开始，迭代与特定“级联”相关的实例。

        返回一个iterator3-tuples（实例，映射器，状态）。

        请注意，在调用cascade\_iterator之前，此MapperProperty上的'cascade'集合将首先针对给定类型进行检查。

        此方法通常仅适用于RelationshipProperty。

    ` class_attribute  T0> ¶ T1>`{.descname}
    :   *继承自 [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的*
        [`class_attribute`](#sqlalchemy.orm.interfaces.MapperProperty.class_attribute "sqlalchemy.orm.interfaces.MapperProperty.class_attribute")
        *属性*

        返回与此[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对应的类绑定描述符。

        这基本上是一个`getattr()`调用：

            return getattr(self.parent.class_, self.key)

        即如果这个[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")被命名为`addresses`，并且它映射到的类是`User`，那么这个序列是可能的：

            >>> from sqlalchemy import inspect
            >>> mapper = inspect(User)
            >>> addresses_property = mapper.attrs.addresses
            >>> addresses_property.class_attribute is User.addresses
            True
            >>> User.addresses.property is addresses_property
            True

     `create_row_processor`{.descname}(*context*, *path*, *mapper*, *result*, *adapter*, *populators*)[¶](#sqlalchemy.orm.descriptor_props.SynonymProperty.create_row_processor "Permalink to this definition")
    :   *inherited from the* [`create_row_processor()`](#sqlalchemy.orm.interfaces.MapperProperty.create_row_processor "sqlalchemy.orm.interfaces.MapperProperty.create_row_processor")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        生成行处理函数并追加到给定的填充列表集。

    ` do_init  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`do_init()`](#sqlalchemy.orm.interfaces.MapperProperty.do_init "sqlalchemy.orm.interfaces.MapperProperty.do_init")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        执行子类特定的初始化后映射器创建步骤。

        这是一个由`MapperProperty`对象的init()方法调用的模板方法。

    `extension_type`{.descname} *=符号（'NOT\_EXTENSION'）* [¶](#sqlalchemy.orm.descriptor_props.SynonymProperty.extension_type "Permalink to this definition")
    :   

    `初始化 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`init()`](#sqlalchemy.orm.interfaces.MapperProperty.init "sqlalchemy.orm.interfaces.MapperProperty.init")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        在创建所有映射器以调用映射器之间的关系并执行其他映射器创建初始化步骤后调用。

     `merge`{.descname}(*session*, *source\_state*, *source\_dict*, *dest\_state*, *dest\_dict*, *load*, *\_recursive*, *\_resolve\_conflict\_map*)[¶](#sqlalchemy.orm.descriptor_props.SynonymProperty.merge "Permalink to this definition")
    :   *继承自* *[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")的
        [`merge()`](#sqlalchemy.orm.interfaces.MapperProperty.merge "sqlalchemy.orm.interfaces.MapperProperty.merge")*

        合并由`MapperProperty`表示的属性从源到目标对象。

    ` post_instrument_class  T0> （ T1> 映射器 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`post_instrument_class()`](#sqlalchemy.orm.interfaces.MapperProperty.post_instrument_class "sqlalchemy.orm.interfaces.MapperProperty.post_instrument_class")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        执行init()完成后需要进行的仪器调整。

        给定的Mapper是调用操作的Mapper，在继承场景中可能不是与self.parent相同的映射器；但是，Mapper将始终至少成为self.parent的子映射器。

        该方法通常由StrategizedProperty使用，该方法将其委派给LoaderStrategy.init\_class\_attribute()以对类绑定的InstrumentedAttribute执行最终设置。

     `setup`{.descname}(*context*, *entity*, *path*, *adapter*, *\*\*kwargs*)[¶](#sqlalchemy.orm.descriptor_props.SynonymProperty.setup "Permalink to this definition")
    :   *inherited from the* [`setup()`](#sqlalchemy.orm.interfaces.MapperProperty.setup "sqlalchemy.orm.interfaces.MapperProperty.setup")
        *method of* [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

        由Query调用以构造SQL语句。

        与目标映射器关联的每个MapperProperty处理查询上下文引用的语句，并根据需要添加列和/或标准。

*class* `sqlalchemy.orm.query。`{.descclassname} `QueryContext`{.descname} （ *query* / T5\> [¶ T6\>](#sqlalchemy.orm.query.QueryContext "Permalink to this definition")
:   

*类 T0\> `sqlalchemy.orm.attributes。 T1>  QueryableAttribute  T2> （ T3> 类_  T4>，键 T5>， IMPL =无 T6>，比较器=无 T7>， parententity =无 T8>， of_type =无 T9> ） T10> ¶ T11>`{.descclassname}*
:   基础：`sqlalchemy.orm.base._MappedAttribute`，[`sqlalchemy.orm.base.InspectionAttr`](#sqlalchemy.orm.base.InspectionAttr "sqlalchemy.orm.base.InspectionAttr")，[`sqlalchemy.orm.interfaces.PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

    [descriptor](glossary.html#term-descriptor)对象的基类，它代表[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")对象拦截属性事件。实际的[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")可以通过[`QueryableAttribute.property`](#sqlalchemy.orm.attributes.QueryableAttribute.property "sqlalchemy.orm.attributes.QueryableAttribute.property")属性进行访问。plain

    也可以看看

    [`InstrumentedAttribute`](#sqlalchemy.orm.attributes.InstrumentedAttribute "sqlalchemy.orm.attributes.InstrumentedAttribute")

    [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")

    [`Mapper.all_orm_descriptors`{](mapping_api.html#sqlalchemy.orm.mapper.Mapper.all_orm_descriptors "sqlalchemy.orm.mapper.Mapper.all_orm_descriptors")

    [`Mapper.attrs`{](mapping_api.html#sqlalchemy.orm.mapper.Mapper.attrs "sqlalchemy.orm.mapper.Mapper.attrs")

    ` __当量__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`__eq__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators.__eq__")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实施`==`运算符。

        在列上下文中，生成子句`a = b`。If the target
        is `None`, produces `a IS NULL`.

    ` __文件__  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__le__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__le__ "sqlalchemy.sql.operators.ColumnOperators.__le__")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<=`运算符。

        在列上下文中，生成子句`a <= b`。

    ` __ LT __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__lt__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__lt__ "sqlalchemy.sql.operators.ColumnOperators.__lt__")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`<`运算符。

        在列上下文中，生成子句`a  b`。

    ` __ NE __  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`__ne__()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__ne__ "sqlalchemy.sql.operators.ColumnOperators.__ne__")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`!=`运算符。

        在列上下文中，生成子句`a ！= b`。If the
        target is `None`, produces
        `a IS NOT NULL`.

    `适配器 T0> ¶ T1>`{.descname}
    :   *继承自* [`adapter`](#sqlalchemy.orm.interfaces.PropComparator.adapter "sqlalchemy.orm.interfaces.PropComparator.adapter")
        *属性的* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        生成一个可调用的列，适应列表达式以适应该比较器的别名版本。

    `所有_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`all_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.all_ "sqlalchemy.sql.operators.ColumnOperators.all_")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`all_()`](core_sqlelement.html#sqlalchemy.sql.expression.all_ "sqlalchemy.sql.expression.all_")子句。

        版本1.1中的新功能

    `任何`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.attributes.QueryableAttribute.any "Permalink to this definition")
    :   *inherited from the* [`any()`](#sqlalchemy.orm.interfaces.PropComparator.any "sqlalchemy.orm.interfaces.PropComparator.any")
        *method of* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        如果此集合包含符合给定条件的任何成员，则返回true。

        `any()`的通常实现是[`RelationshipProperty.Comparator.any()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")。

        参数：

        -   **criterion**[¶](#sqlalchemy.orm.attributes.QueryableAttribute.any.params.criterion)
            – an optional ClauseElement formulated against the member
            class’ table or attributes.
        -   **\*\*kwargs**[¶](#sqlalchemy.orm.attributes.QueryableAttribute.any.params.**kwargs)
            – key/value pairs corresponding to member class attribute
            names which will be compared via equality to the
            corresponding values.

    `任何_  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`any_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.any_ "sqlalchemy.sql.operators.ColumnOperators.any_")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`any_()`](core_sqlelement.html#sqlalchemy.sql.expression.any_ "sqlalchemy.sql.expression.any_")子句。

        版本1.1中的新功能

    ` ASC  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`asc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.asc "sqlalchemy.sql.operators.ColumnOperators.asc")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`asc()`](core_sqlelement.html#sqlalchemy.sql.expression.asc "sqlalchemy.sql.expression.asc")子句。

    `（ cleft，cright，symmetric = False T5> ¶ T6>`{.descname}
    :   *inherited from the* [`between()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.between "sqlalchemy.sql.operators.ColumnOperators.between")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在()子句之间针对父对象生成[`between()`](core_sqlelement.html#sqlalchemy.sql.expression.between "sqlalchemy.sql.expression.between")

    `整理 T0> （ T1> 整理 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`collate()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.collate "sqlalchemy.sql.operators.ColumnOperators.collate")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        根据给定的排序字符串，针对父对象生成一个[`collate()`](core_sqlelement.html#sqlalchemy.sql.expression.collate "sqlalchemy.sql.expression.collate")子句。

    `的concat  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`concat()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.concat "sqlalchemy.sql.operators.ColumnOperators.concat")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现'concat'操作符。

        在列上下文中，生成子句`a || b`，或者使用`concat()`运算符在MySQL上。

    `包含`{.descname} （ *其他*，*\*\* kwargs* ） [](#sqlalchemy.orm.attributes.QueryableAttribute.contains "Permalink to this definition") \>
    :   *inherited from the* [`contains()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.contains "sqlalchemy.sql.operators.ColumnOperators.contains")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'包含'运算符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；％'`

    `递减 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`desc()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.desc "sqlalchemy.sql.operators.ColumnOperators.desc")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`desc()`](core_sqlelement.html#sqlalchemy.sql.expression.desc "sqlalchemy.sql.expression.desc")子句。

    `不同 T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`distinct()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.distinct "sqlalchemy.sql.operators.ColumnOperators.distinct")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成一个[`distinct()`](core_sqlelement.html#sqlalchemy.sql.expression.distinct "sqlalchemy.sql.expression.distinct")子句。

    `endswith`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.attributes.QueryableAttribute.endswith "Permalink to this definition")
    :   *inherited from the* [`endswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.endswith "sqlalchemy.sql.operators.ColumnOperators.endswith")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现'endswith'操作符。

        在列上下文中，生成子句`LIKE '％＆lt； other＆gt；`

    `extension_type`{.descname} *=符号（'NOT\_EXTENSION'）* [¶](#sqlalchemy.orm.attributes.QueryableAttribute.extension_type "Permalink to this definition")
    :   

    `有`{.descname} （ *criterion = None*，*\*\* kwargs* ） [/ T5\>](#sqlalchemy.orm.attributes.QueryableAttribute.has "Permalink to this definition")
    :   *inherited from the* [`has()`](#sqlalchemy.orm.interfaces.PropComparator.has "sqlalchemy.orm.interfaces.PropComparator.has")
        *method of* [`PropComparator`](#sqlalchemy.orm.interfaces.PropComparator "sqlalchemy.orm.interfaces.PropComparator")

        如果此元素引用符合给定条件的成员，则返回true。

        The usual implementation of `has()` is
        [`RelationshipProperty.Comparator.has()`](#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has").

        参数：

        -   **criterion**[¶](#sqlalchemy.orm.attributes.QueryableAttribute.has.params.criterion)
            – an optional ClauseElement formulated against the member
            class’ table or attributes.
        -   **\*\*kwargs**[¶](#sqlalchemy.orm.attributes.QueryableAttribute.has.params.**kwargs)
            – key/value pairs corresponding to member class attribute
            names which will be compared via equality to the
            corresponding values.

    `ilike`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.attributes.QueryableAttribute.ilike "Permalink to this definition")
    :   *inherited from the* [`ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`ilike`运算符。

        在列上下文中，生成子句`a ILIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.ilike("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.orm.attributes.QueryableAttribute.ilike.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.orm.attributes.QueryableAttribute.ilike.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.ilike("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    `在_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        在运算符中实现`in`

        在列上下文中，生成子句`a IN 其他`。“other”可以是列表达式的元组/列表，或者是[`select()`](core_selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select")结构。

    `信息 T0> ¶ T1>`{.descname}
    :   返回底层SQL元素的'info'字典。

        这里的行为如下：

        -   If the attribute is a column-mapped property, i.e.
            [`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty"),
            which is mapped directly to a schema-level [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
            object, this attribute will return the
            [`SchemaItem.info`](core_metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")
            dictionary associated with the core-level [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")
            object.
        -   If the attribute is a [`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")
            but is mapped to any other kind of SQL expression other than
            a [`Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
            the attribute will refer to the [`MapperProperty.info`](#MapperProperty.info "MapperProperty.info")
            dictionary associated directly with the
            [`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty"),
            assuming the SQL expression itself does not have its own
            `.info` attribute (which should be the
            case, unless a user-defined SQL construct has defined one).
        -   If the attribute refers to any other kind of
            [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty"),
            including [`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty"),
            the attribute will refer to the [`MapperProperty.info`](#MapperProperty.info "MapperProperty.info")
            dictionary associated with that [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty").
        -   To access the [`MapperProperty.info`](#MapperProperty.info "MapperProperty.info")
            dictionary of the [`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")
            unconditionally, including for a [`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")
            that’s associated directly with a [`schema.Column`](core_metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column"),
            the attribute can be referred to using
            [`QueryableAttribute.property`](#sqlalchemy.orm.attributes.QueryableAttribute.property "sqlalchemy.orm.attributes.QueryableAttribute.property")
            attribute, as
            `MyClass.someattribute.property.info`.

        0.8.0版本中的新功能

        也可以看看

        [`SchemaItem.info`](core_metadata.html#sqlalchemy.schema.SchemaItem.info "sqlalchemy.schema.SchemaItem.info")

        [`MapperProperty.info`](#MapperProperty.info "MapperProperty.info")

    `是_  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS`运算符。

        通常，当与`None`的值进行比较时，会自动生成`IS`，这会解析为`NULL`。但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")

    ` is_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`is_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_distinct_from "sqlalchemy.sql.operators.ColumnOperators.is_distinct_from")
        *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS DISTINCT FROM`运算符。

        在大多数平台上呈现“一个IS DISTINCT FROM
        b”；在一些如SQLite可能会呈现“一个不是b”。

        版本1.1中的新功能

    ` IsNot运算 T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *inherited from the* [`isnot()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`IS NOT`运算符。

        Normally, `IS NOT` is generated
        automatically when comparing to a value of `None`, which resolves to `NULL`.
        但是，如果与某些平台上的布尔值进行比较，则可能需要明确使用`IS NOT`。

        New in version 0.7.9.

        也可以看看

        [`ColumnOperators.is_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")

    ` isnot_distinct_from  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`isnot_distinct_from()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from "sqlalchemy.sql.operators.ColumnOperators.isnot_distinct_from")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现`IS NOT DISTINCT FROM`运算符。

        在大多数平台上呈现“不是从BIND DISTINCT FROM
        b”；在某些例如SQLite上可能会呈现“a IS b”。

        版本1.1中的新功能

    `像`{.descname} （ *其他*，*escape =无* ） [t5 \>](#sqlalchemy.orm.attributes.QueryableAttribute.like "Permalink to this definition")
    :   *inherited from the* [`like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        像运算符一样实现`like`

        在列上下文中，生成子句`a LIKE 其他`。

        例如。：

            select([sometable]).where(sometable.c.column.like("%foobar%"))

        参数：

        -   **其他**
            [¶](#sqlalchemy.orm.attributes.QueryableAttribute.like.params.other)
            - 要比较的表达式
        -   **转义**
            [¶](#sqlalchemy.orm.attributes.QueryableAttribute.like.params.escape)
            -

            可选的转义字符，呈现`ESCAPE`关键字，例如：

                somecolumn.like("foo/%bar", escape="/")

        也可以看看

        [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    `匹配`{.descname} （ *其他*，*\*\* kwargs* ） [t5 \>](#sqlalchemy.orm.attributes.QueryableAttribute.match "Permalink to this definition")
    :   *继承自* [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        *方法 tt\> [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        实现数据库特定的“匹配”运算符。

        [`match()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")
        attempts to resolve to a MATCH-like function or operator
        provided by the backend. 例子包括：

        -   Postgresql - 呈现`x @@ to_tsquery（y）`
        -   MySQL - renders
            `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
        -   Oracle - 呈现`CONTAINS（x， y）`
        -   其他后端可能会提供特殊的实现。
        -   没有任何特殊实现的后端会将操作符发送为“MATCH”。例如，这与SQlite兼容。

     `notilike`{.descname}(*other*, *escape=None*)[¶](#sqlalchemy.orm.attributes.QueryableAttribute.notilike "Permalink to this definition")
    :   *inherited from the* [`notilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notilike "sqlalchemy.sql.operators.ColumnOperators.notilike")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT ILIKE`运算符。

        这相当于对[`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")使用否定，即`~x.ilike(y)`。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.ilike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")

    ` notin _  T0> （ T1> 其他 T2> ） T3> ¶ T4>`{.descname}
    :   *继承自* [`notin_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")
        *方法 [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        执行`NOT IN`运算符。

        这相当于对[`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")，即`~x.in_(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.in_()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")

    `notlike`{.descname} （ *其他*，*转义=无* ） [t5 \>](#sqlalchemy.orm.attributes.QueryableAttribute.notlike "Permalink to this definition")
    :   *inherited from the* [`notlike()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notlike "sqlalchemy.sql.operators.ColumnOperators.notlike")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        执行`NOT LIKE`运算符。

        这相当于对[`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")，即`~x.like(y)`使用否定。

        0.8版本中的新功能

        也可以看看

        [`ColumnOperators.like()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")

    ` nullsfirst  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *inherited from the* [`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullsfirst "sqlalchemy.sql.operators.ColumnOperators.nullsfirst")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        针对父对象生成[`nullsfirst()`](core_sqlelement.html#sqlalchemy.sql.expression.nullsfirst "sqlalchemy.sql.expression.nullsfirst")子句。

    ` nullslast  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   *继承自* [`nullslast()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.nullslast "sqlalchemy.sql.operators.ColumnOperators.nullslast")
        *[`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")*

        针对父对象生成一个[`nullslast()`](core_sqlelement.html#sqlalchemy.sql.expression.nullslast "sqlalchemy.sql.expression.nullslast")子句。

    `op`{.descname} （ *opstring*，*precedence = 0*，*is\_comparison = False* ） T5\> [¶ T6\>](#sqlalchemy.orm.attributes.QueryableAttribute.op "Permalink to this definition")
    :   *继承自* [`op()`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op "sqlalchemy.sql.operators.Operators.op")
        *方法的[`Operators`](core_sqlelement.html#sqlalchemy.sql.operators.Operators "sqlalchemy.sql.operators.Operators")*

        产生通用的操作员功能。

        例如。：

            somecolumn.op("*")(5)

        生产：

            somecolumn * 5

        该函数也可用于使按位运算符明确。例如：

            somecolumn.op('&')(0xff)

        是`somecolumn`中的值的按位与。

        参数：

        -   **operator**[¶](#sqlalchemy.orm.attributes.QueryableAttribute.op.params.operator)
            – a string which will be output as the infix operator
            between this element and the expression passed to the
            generated function.
        -   **优先顺序**
            [¶](#sqlalchemy.orm.attributes.QueryableAttribute.op.params.precedence)
            -

            当对表达式加括号时，优先级适用于运算符。较低的数字将使表达式在针对具有较高优先级的另一个运算符应用时加括号。除了逗号（`,`）和`AS`运算符以外，`0`的默认值低于所有运算符。100的值将会高于或等于所有操作员，-100将低于或等于所有操作员。

            New in version 0.8: - added the ‘precedence’ argument.

        -   **is\_comparison**
            [¶](#sqlalchemy.orm.attributes.QueryableAttribute.op.params.is_comparison)
            -

            如果为True，那么该运算符将被视为“比较”运算符，即，其计算结果为boolean
            true / false值，如`==`，`>`等。应该设置此标志，以便ORM关系可以确定运算符在自定义连接条件中使用时是比较运算符。

            版本0.9.2新增： - 添加了[`Operators.op.is_comparison`](core_sqlelement.html#sqlalchemy.sql.operators.Operators.op.params.is_comparison "sqlalchemy.sql.operators.Operators.op")标志。

        也可以看看

        [Redefining and Creating New
        Operators](core_custom_types.html#types-operators)

        [Using custom operators in join
        conditions](join_conditions.html#relationship-custom-operator)中使用自定义运算符

    `父 T0> ¶ T1>`{.descname}
    :   返回代表父级的检查实例。

        这将是[`Mapper`](mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")或[`AliasedInsp`](query.html#sqlalchemy.orm.util.AliasedInsp "sqlalchemy.orm.util.AliasedInsp")的实例，具体取决于与此属性关联的父实体的性质。

    `属性 T0> ¶ T1>`{.descname}
    :   返回与此[`QueryableAttribute`](#sqlalchemy.orm.attributes.QueryableAttribute "sqlalchemy.orm.attributes.QueryableAttribute")关联的[`MapperProperty`](#sqlalchemy.orm.interfaces.MapperProperty "sqlalchemy.orm.interfaces.MapperProperty")。

        这里的返回值通常是[`ColumnProperty`](#sqlalchemy.orm.properties.ColumnProperty "sqlalchemy.orm.properties.ColumnProperty")或[`RelationshipProperty`](#sqlalchemy.orm.properties.RelationshipProperty "sqlalchemy.orm.properties.RelationshipProperty")的实例。

    `startswith`{.descname} （ *其他*，*\*\* kwargs* ） [¶ t5 \>](#sqlalchemy.orm.attributes.QueryableAttribute.startswith "Permalink to this definition")
    :   *inherited from the* [`startswith()`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.startswith "sqlalchemy.sql.operators.ColumnOperators.startswith")
        *method of* [`ColumnOperators`](core_sqlelement.html#sqlalchemy.sql.operators.ColumnOperators "sqlalchemy.sql.operators.ColumnOperators")

        实现`startwith`运算符。

        在列上下文中，生成子句`LIKE '＆lt； other＆gt；％'`

 *class*`sqlalchemy.orm.session.`{.descclassname}`UOWTransaction`{.descname}(*session*)[¶](#sqlalchemy.orm.session.UOWTransaction "Permalink to this definition")
:    `filter_states_for_dep`{.descname}(*dep*, *states*)[¶](#sqlalchemy.orm.session.UOWTransaction.filter_states_for_dep "Permalink to this definition")
    :   将 InstanceState 的给定列表筛选为与给定的 DependencyProcessor 相关的列表。

    ` finalize_flush_changes  T0> （ T1> ） T2> ¶ T3>`{.descname}
    :   在成功刷新()后将处理的对象标记为清除/删除。

        在execute()方法成功且事务已提交后，在flush()方法内调用此方法。

     `get_attribute_history`{.descname}(*state*, *key*, *passive=symbol('PASSIVE\_NO\_INITIALIZE')*)[¶](#sqlalchemy.orm.session.UOWTransaction.get_attribute_history "Permalink to this definition")
    :   外观到attributes.get\_state\_history()，包括缓存结果。

    ` IS_DELETED  T0> （ T1> 状态 T2> ） T3> ¶ T4>`{.descname}
    :   如果在此uowtransaction中将给定状态标记为已删除，则返回true。

    ` remove_state_actions  T0> （ T1> 状态 T2> ） T3> ¶ T4>`{.descname}
    :   从uowtransaction中移除一个状态的待处理动作。

    ` was_already_deleted  T0> （ T1> 状态 T2> ） T3> ¶ T4>`{.descname}
    :   如果给定的状态已过期并且之前被删除，则返回true。


