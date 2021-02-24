---
title: Sybase 特有的
date: 2021-02-20 22:41:38
permalink: /sqlalchemy/dialects/sybase/
categories:
  - 📖好书
  - SqlAlchemy 中文文档
  - dialects
tags:
---
的 Sybase [¶ T0\>](#module-sqlalchemy.dialects.sybase.base "Permalink to this headline")
=======================================================================================

支持 Sybase 数据库。

DBAPI 支持[¶](#dialect-sybase "Permalink to this headline")
----------------------------------------------------------

以下 dialect / DBAPI 选项可用。请参阅各个 DBAPI 部分的连接信息。

-   [Python 的的 Sybase T0\>](#module-sqlalchemy.dialects.sybase.pysybase)
-   [PyODBC T0\>](#module-sqlalchemy.dialects.sybase.pyodbc)
-   [mxODBC T0\>](#module-sqlalchemy.dialects.sybase.mxodbc)

注意

Sybase 方言在当前的 SQLAlchemy 版本上运行，但没有经常测试，并且可能有许多问题和警告，目前尚未处理。

蟒-SYBASE [¶ T0\>](#module-sqlalchemy.dialects.sybase.pysybase "Permalink to this headline")
--------------------------------------------------------------------------------------------

通过 Python-Sybase 驱动程序支持 Sybase 数据库。

### DBAPI [¶ T0\>](#dialect-sybase-pysybase-url "Permalink to this headline")

Documentation and download information (if applicable) for Python-Sybase
is available at:
[http://python-sybase.sourceforge.net/](http://python-sybase.sourceforge.net/)

### 连接[¶ T0\>](#dialect-sybase-pysybase-connect "Permalink to this headline")

连接字符串：

    sybase+pysybase://<username>:<password>@<dsn>/[database name]plainplainplain

### Unicode 支持[¶](#unicode-support "Permalink to this headline")

python-sybase 驱动程序目前似乎不支持任何类型的非 ASCII 字符串。

pyodbc [¶ T0\>](#module-sqlalchemy.dialects.sybase.pyodbc "Permalink to this headline")
---------------------------------------------------------------------------------------

通过 PyODBC 驱动程序支持 Sybase 数据库。

### DBAPI [¶ T0\>](#dialect-sybase-pyodbc-url "Permalink to this headline")

PyODBC 的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/pyodbc/](http://pypi.python.org/pypi/pyodbc/)

### 连接[¶ T0\>](#dialect-sybase-pyodbc-connect "Permalink to this headline")

连接字符串：

    sybase+pyodbc://<username>:<password>@<dsnname>[/<database>]plain

### Unicode 支持[¶](#id1 "Permalink to this headline")

pyodbc 驱动程序当前支持使用 Unicode 或多字节字符串的这些 Sybase 类型：

    CHARplainplainplainplainplain
    NCHAR
    NVARCHAR
    TEXT
    VARCHAR

目前*不支持*的是：

    UNICHARplainplainplainplainplainplainplain
    UNITEXT
    UNIVARCHAR

mxodbc [¶ T0\>](#module-sqlalchemy.dialects.sybase.mxodbc "Permalink to this headline")
---------------------------------------------------------------------------------------

通过 mxODBC 驱动程序支持 Sybase 数据库。

### DBAPI [¶ T0\>](#dialect-sybase-mxodbc-url "Permalink to this headline")

mxODBC 的文档和下载信息（如果适用）可在以下网址获得：[http://www.egenix.com/](http://www.egenix.com/)

### 连接[¶ T0\>](#dialect-sybase-mxodbc-connect "Permalink to this headline")

连接字符串：

    sybase+mxodbc://<username>:<password>@<dsnname>plainplainplainplain

注意

这种方言只是一个存根，目前可能不起作用。
