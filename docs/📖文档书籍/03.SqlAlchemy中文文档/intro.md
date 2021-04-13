---
title: intro
date: 2021-02-20 22:41:39
permalink: /sqlalchemy/intro/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
tags:
---
概述[¶ T0\>](#overview "Permalink to this headline")
====================================================

SQLAlchemy 的 SQL 工具包和 ORM 是一套 python 数据库操作的综合工具包。它有多个不同领域的功能，可以单独使用或组合使用。其主要组件如下图所示，包含组件层次上的依赖关系。

![](http://sqlalchemy.readthedocs.io/en/latest/_images/sqla_arch_small.png)

如上图所示，SQLAlchemy 最重要的两个部分是 **ORM** 和 **SQL
表达式语言**。SQL 表达式可以独立于 ORM 使用。使用 ORM 时，SQL
表达式语言仍然是公开 API 的一部分，因为它在对象关系配置和查询中使用。

文档概述[¶](#documentation-overview "Permalink to this headline")
-----------------------------------------------------------------

文档分为三个部分: [SQLAlchemy ORM](orm_index.html)、[SQLAlchemy
核心](core_index.html)和 [方言（Dialects）](dialects_index.html).

在 [SQLAlchemy ORM](orm_index.html)中,
对象关系映射被充分引入和描述。新用户可以从[对象关系教程](orm_tutorial.html)开始。如果你想要了解自动构建高级 SQL 以及管理 Python 对象，推荐阅读此教程。

在 [SQLAlchemy Core](core_index.html) 中，主要介绍了 SQLAlchemy 的
SQL、数据库集成和描述服务， 这部分的核心是 SQL 表达语言。SQL
表达式是独立于 ORM 包的一套自成一体的工具集， 它可以用来创建易于使用的
SQ 表达式，该 SQL 表达式可通过编程创建、修改和执行，返回游标结果集。对比
ORM 使用域为中心的方式，表达语言提供模式为中心的架构。新用户请从 [SQL
表达式教程](core_tutorial.html)开始。SQLAlchemy
引擎，链接和池服务同样在[SQLAlchemy Core](core_index.html)中有描述。

[Dialects](dialects_index.html)介绍了所有 SQLAlchemy 支持的数据库和
DBAPI 后端。

代码示例[¶](#code-examples "Permalink to this headline")
--------------------------------------------------------

主要关于 ORM 的工作代码示例包含在 SQLAlchemy 发行版中.所有包含的示例应用程序的描述在[ORM
Examples](orm_examples.html).中。

还有各种各样的示例涉及核心 SQLAlchemy 构造以及维基上的 ORM, 参见[Theatrum
Chemicum](http://www.sqlalchemy.org/trac/wiki/UsageRecipes)。

安装指南[¶](#installation-guide "Permalink to this headline")
-------------------------------------------------------------

### 支持的平台[¶](#supported-platforms "Permalink to this headline")

SQLAlchemy 已经针对以下平台进行了测试：

-   cPython 自 2.6 版开始，通过 2.xx 系列
-   cPython 版本 3，贯穿所有 3.xx 系列
-   [Pypy](http://pypy.org/) 2.1 or greater

在 0.9 版本中更改： Python 2.6 现在是支持的最小 Python 版本。

目前不支持的平台包括 Jython，IronPython。曾经已经支持
Jython，并且可能会在将来的版本中支持，这取决于 Jython 本身的状态。

### 支持的安装方法[¶](#supported-installation-methods "Permalink to this headline")

SQLAlchemy 安装是通过基于[setuptools](http://pypi.python.org/pypi/setuptools/)的标准 Python 方法，通过直接引用`setup.py`或通过使用[pip](http://pypi.python.org/pypi/pip/)或其他 setuptools，兼容的方法。

在版本 1.1 中更改：
setup.py 文件现在需要 setuptools；不再支持简单的 distutils 安装。

### 通过 pip 安装[¶](#install-via-pip "Permalink to this headline")

当`pip`可用时，可以从 Pypi 下载并在一个步骤中安装该分发：

    pip install SQLAlchemyplainplainplainplainplainplainplainplainplainplain

该命令将从[Python Cheese
Shop](http://pypi.python.org/pypi/SQLAlchemy)下载最新的**发布的**版 SQLAlchemy 并将其安装到您的系统中。

为了安装最新的**prerelease**版本，比如`1.1.0b1`，pip 要求使用`--pre`标志：

    pip install --pre SQLAlchemyplainplainplainplain

如上所述，如果最新版本是预发行版本，则将安装它而不是最新发布的版本。

### 使用 setup.py [¶](#installing-using-setup-py "Permalink to this headline")进行安装

否则，您可以使用`setup.py`脚本从分发安装：

    python setup.py installplainplainplainplainplainplainplainplainplainplainplain

### 安装 C 扩展[¶](#installing-the-c-extensions "Permalink to this headline")

SQLAlchemy 包含 C 扩展，它提供了额外的速度提升来处理结果集。这些扩展在 cPython 的 2.xx 和 3.xx 系列上均受支持。

`setup.py` will automatically build the extensions
if an appropriate platform is detected.
如果 C 扩展的构建失败，由于缺少编译器或其他问题，安装过程将输出警告消息，并在完成报告最终状态时重新运行没有 C 扩展的构建。

要运行构建/安装而不尝试编译 C 扩展，可以指定`DISABLE_SQLALCHEMY_CEXT`环境变量。对于这种情况的用例要么是针对特殊的测试环境，要么是通常的“重建”机制无法解决的罕见情况下的兼容性/构建问题：

    export DISABLE_SQLALCHEMY_CEXT=1; python setup.py installplainplainplainplainplainplainplainplainplainplain

在版本 1.1 中更改：遗留的--without-cextensions 标志已从安装程序中删除，因为它依赖于 setuptools 的不推荐使用的功能。

### 在 Python 3 上安装[¶](#installing-on-python-3 "Permalink to this headline")

SQLAlchemy 直接在 Python 2 或 Python
3 上运行，并且可以在任何环境中安装，无需任何调整或代码转换。

### 安装数据库 API [¶](#installing-a-database-api "Permalink to this headline")

SQLAlchemy 旨在与针对特定数据库构建的[DBAPI](glossary.html#term-dbapi)实现一起运行，并包含对最流行数据库的支持。The
individual database sections in [*Dialects*](dialects_index.html)
enumerate the available DBAPIs for each database, including external
links.

### 检查安装的 SQLAlchemy 版本[¶](#checking-the-installed-sqlalchemy-version "Permalink to this headline")

本文档涵盖了 SQLAlchemy 版本 1.1。如果您正在使用已安装 SQLAlchemy 的系统，请从您的 Python 提示符中检查版本，如下所示：

    >>> import sqlalchemyplainplainplainplainplainplainplainplain
    >>> sqlalchemy.__version__ # doctest: +SKIP
    1.1.0

1.0 到 1.1 迁移[¶](#to-1-1-migration "Permalink to this headline")
---------------------------------------------------------------

Notes on what’s changed from 1.0 to 1.1 is available here at [*What’s
New in SQLAlchemy 1.1?*](changelog_migration_11.html).
