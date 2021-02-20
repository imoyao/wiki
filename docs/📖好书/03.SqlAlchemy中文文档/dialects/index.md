---
title: index
date: 2021-02-20 23:10:52
permalink: /pages/32a1d7/
categories:
  - 📖好书
  - SqlAlchemy中文文档
  - dialects
tags:
  - 
---
方言[¶ T0\>](#dialects "Permalink to this headline")
====================================================

**方言**是SQLAlchemy用来与各种类型的[DBAPI](glossary.html#term-dbapi)实现和数据库进行通信的系统。以下部分包含参考文档和特定于每个后端用法的注释，以及各种DBAPI的注释。

所有方言都要求安装适当的DBAPI驱动程序。

包含的方言[¶](#included-dialects "Permalink to this headline")
--------------------------------------------------------------

-   [火鸟 T0\>](firebird.html)
-   [Microsoft SQL Server](mssql.html)
-   [的MySQL T0\>](mysql.html)
-   [甲骨文 T0\>](oracle.html)
-   [的PostgreSQL T0\>](postgresql.html)
-   [SQLite的 T0\>](sqlite.html)
-   [的Sybase T0\>](sybase.html)

外部方言[¶](#external-dialects "Permalink to this headline")
------------------------------------------------------------

在版本0.8中更改：从SQLAlchemy
0.8开始，几种方言已移至外部项目，新数据库的方言也将作为外部项目发布。这里的基本原理是保持基本的SQLAlchemy安装和测试套件的增长非常大。

诸如SQLite，MySQL，Postgresql，Oracle，SQL
Server和Firebird等“经典”方言目前仍将保留在Core中。

在版本1.0中更改： Drizzle方言已被移入第三方系统。

当前SQLAlchemy的外部方言项目包括：

### 生产就绪[¶](#production-ready "Permalink to this headline")

-   [ibm\_db\_sa](http://code.google.com/p/ibm-db/wiki/README) - driver
    for IBM DB2 and Informix, developed jointly by IBM and SQLAlchemy
    developers.
-   [sqlalchemy-redshift](https://pypi.python.org/pypi/sqlalchemy-redshift)
    - driver for Amazon Redshift, adapts the existing
    Postgresql/psycopg2 driver.
-   [sqlalchemy\_exasol](https://github.com/blue-yonder/sqlalchemy_exasol)
    - EXASolution的驱动程序。
-   [sqlalchemy-sqlany](https://github.com/sqlanywhere/sqlalchemy-sqlany)
    - 由SAP开发的SAP Sybase SQL Anywhere驱动程序。
-   [sqlalchemy-monetdb](https://github.com/gijzelaerr/sqlalchemy-monetdb)
    - MonetDB的驱动程序。

### 实验/不完整[¶](#experimental-incomplete "Permalink to this headline")

处于不完整状态或被认为有点实验性的方言。

-   [CALCHIPAN](https://bitbucket.org/zzzeek/calchipan/) -
    使[Pandas](http://pandas.pydata.org/)数据框适应SQLAlchemy。
-   [sqlalchemy-cubrid](https://bitbucket.org/zzzeek/sqlalchemy-cubrid)
    - CUBRID数据库的驱动程序。

### 阁楼[¶ T0\>](#attic "Permalink to this headline")

“阁楼”中的方言是早些时候为SQLAlchemy贡献的，但自那时以来很少受到关注或需求，现在迁移到自己的仓库中，最多只是半工作状态。对这些方言感兴趣的社区成员应该可以自由选择他们当前的代码库，并转入工作库。

-   [sqlalchemy-access](https://bitbucket.org/zzzeek/sqlalchemy-access)
    - Microsoft Access的驱动程序。
-   [sqlalchemy-drizzle](https://bitbucket.org/zzzeek/sqlalchemy-drizzle)
    - Drizzle MySQL变体的驱动程序。
-   [sqlalchemy-informixdb](https://bitbucket.org/zzzeek/sqlalchemy-informixdb)
    - informixdb DBAPI的驱动程序。
-   [sqlalchemy-maxdb](https://bitbucket.org/zzzeek/sqlalchemy-maxdb) -
    MaxDB数据库的驱动程序

