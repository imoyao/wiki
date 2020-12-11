---
title: Python 标准库系列之 tarfile 模块

tags: 
  - 编码
  - 面向对象
top: 12
categories: 
  - 💻 工作
  - 🐍Python
  - 全栈之路
  - 7-标准库
date: 2020-05-23 18:21:46
permalink: /pages/b8a959/
---

The tarfile module makes it possible to read and write tar archives, including those using gzip, bz2 and lzma compression. Use the zipfile module to read or write .zip files, or the higher-level functions in shutil.

官方文档：https://docs.python.org/3.5/library/tarfile.html

打包及重命名文件

```python
>>> import tarfile
# 以w模式创建文件
>>> tar = tarfile.open('tar_file.tar','w')
# 添加一个文件，arcname可以重命名文件
>>> tar.add('/tmp/folder/file.txt', arcname='file.log')
# 添加一个目录
>>> tar.add('/tmp/folder/tmp')                         
# 关闭
>>> tar.close()
```

查看文件列表

```python
>>> tar = tarfile.open('tar_file.tar','r')             
# 获取包内的所有文件列表
>>> tar.getmembers()
[<TarInfo 'file.log' at 0x7f737af2da70>, <TarInfo 'tmp/folder/tmp' at 0x7f737af2dd90>]
```

追加

```python
# 以w模式创建文件
>>> tar = tarfile.open('tar_file.tar','a')
>>> tar.add('/tmp/folder/sc.pyc')
>>> tar.close()
>>> tar = tarfile.open('tar_file.tar','r')
>>> tar.getmembers()
[<TarInfo 'file.log' at 0x7ff8d4fa1110>, <TarInfo 'tmp/folder/tmp' at 0x7ff8d4fa11d8>, <TarInfo 'tmp/folder/sc.pyc' at 0x7ff8d4fa12a0>]
```

解压全部文件

```python
>>> import os
>>> import tarfile
>>> os.system("ls -l")
总用量 12
-rw-rw-r-- 1 ansheng ansheng 10240 5月  26 17:40 tar_file.tar
0
>>> tar = tarfile.open('tar_file.tar','r')
>>> tar.extractall()
>>> tar.close()
>>> os.system("ls -l")
总用量 16
-rw-rw-r-- 1 ansheng ansheng     0 5月  26 16:05 file.log
-rw-rw-r-- 1 ansheng ansheng 10240 5月  26 17:40 tar_file.tar
drwxrwxr-x 3 ansheng ansheng  4096 5月  26 17:48 tmp
0
```

解压单个文件

如果我们的压缩包很大的情况下，就不能够一次性解压了，那样太耗内存了，可以通过下面的方式进行解压，其原理就是一个文件一个文件的解压。

```python
import tarfile
tar = tarfile.open('tar_file.tar','r')
for n in tar.getmembers():
    tar.extract(n,"/tmp")
tar.close()
```