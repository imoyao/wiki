---
title: Sybase特有的
date: 2021-02-20 22:41:38
permalink: /sqlalchemy/dialects/sybase/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - dialects
tags:
  - 
---
的Sybase [¶ T0\>](#module-sqlalchemy.dialects.sybase.base "Permalink to this headline")
=======================================================================================

支持Sybase数据库。

DBAPI支持[¶](#dialect-sybase "Permalink to this headline")
----------------------------------------------------------

以下dialect / DBAPI选项可用。请参阅各个DBAPI部分的连接信息。

-   [Python的的Sybase T0\>](#module-sqlalchemy.dialects.sybase.pysybase)
-   [PyODBC T0\>](#module-sqlalchemy.dialects.sybase.pyodbc)
-   [mxODBC T0\>](#module-sqlalchemy.dialects.sybase.mxodbc)

注意

Sybase方言在当前的SQLAlchemy版本上运行，但没有经常测试，并且可能有许多问题和警告，目前尚未处理。

蟒-SYBASE [¶ T0\>](#module-sqlalchemy.dialects.sybase.pysybase "Permalink to this headline")
--------------------------------------------------------------------------------------------

通过Python-Sybase驱动程序支持Sybase数据库。

### DBAPI [¶ T0\>](#dialect-sybase-pysybase-url "Permalink to this headline")

Documentation and download information (if applicable) for Python-Sybase
is available at:
[http://python-sybase.sourceforge.net/](http://python-sybase.sourceforge.net/)

### 连接[¶ T0\>](#dialect-sybase-pysybase-connect "Permalink to this headline")

连接字符串：

    sybase+pysybase://<username>:<password>@<dsn>/[database name]

### Unicode支持[¶](#unicode-support "Permalink to this headline")

python-sybase驱动程序目前似乎不支持任何类型的非ASCII字符串。

pyodbc [¶ T0\>](#module-sqlalchemy.dialects.sybase.pyodbc "Permalink to this headline")
---------------------------------------------------------------------------------------

通过PyODBC驱动程序支持Sybase数据库。

### DBAPI [¶ T0\>](#dialect-sybase-pyodbc-url "Permalink to this headline")

PyODBC的文档和下载信息（如果适用）可在以下网址获得：[http://pypi.python.org/pypi/pyodbc/](http://pypi.python.org/pypi/pyodbc/)

### 连接[¶ T0\>](#dialect-sybase-pyodbc-connect "Permalink to this headline")

连接字符串：

    sybase+pyodbc://<username>:<password>@<dsnname>[/<database>]

### Unicode支持[¶](#id1 "Permalink to this headline")

pyodbc驱动程序当前支持使用Unicode或多字节字符串的这些Sybase类型：

    CHAR
    NCHAR
    NVARCHAR
    TEXT
    VARCHAR

目前*不支持*的是：

    UNICHAR
    UNITEXT
    UNIVARCHAR

mxodbc [¶ T0\>](#module-sqlalchemy.dialects.sybase.mxodbc "Permalink to this headline")
---------------------------------------------------------------------------------------

通过mxODBC驱动程序支持Sybase数据库。

### DBAPI [¶ T0\>](#dialect-sybase-mxodbc-url "Permalink to this headline")

mxODBC的文档和下载信息（如果适用）可在以下网址获得：[http://www.egenix.com/](http://www.egenix.com/)

### 连接[¶ T0\>](#dialect-sybase-mxodbc-connect "Permalink to this headline")

连接字符串：

    sybase+mxodbc://<username>:<password>@<dsnname>

注意

这种方言只是一个存根，目前可能不起作用。
