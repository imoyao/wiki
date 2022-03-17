---
title: 磁盘模块

tags: 
  - 面试
  - Python
categories: 
  - 💻 工作
  - 存储
date: 2020-05-23 18:21:46
permalink: /pages/fb4a39/
---

## 简介

磁盘模块从功能上来说包含两个部分：磁盘名、磁盘位置、背板等磁盘基本信息获取及磁盘灯设置。

从模块上划分为三部分：

*   **digidiskmap.py** 磁盘名和磁盘位置对应关系模块。
*   **digidiskproduct.py** 背板厂商判定模块，包含背板上磁盘位置和 phyid 对应关系，包含背板磁盘灯和磁盘状态对应关系。
*   **digidisklight.py** 磁盘灯设置模块。

## 设计实现说明

### 磁盘名和磁盘位置对应关系模块 - digidiskmap.py

盘位对应关系获取的原理依据背板上 phyid 的位置不变化（**固件需要一致，因为厂家更新固件时有可能会改变该对应关系**）。

在该原理的前提下，将背板上磁盘位置的顺序也规定下来（**从下到上，从左到右，依次增加**），这样就能生成磁盘位置和 phyid 的对应关系。

背板插入磁盘后，磁盘名称和 phyid 之间也形成对应，这样通过**phyid**的衔接，就能找到磁盘名称和磁盘位置的对应关系。

如下表：
{%raw%}
<table border="1" class="docutils">
<colgroup>
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
<col width="7%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head" colspan="4">Disk Location</th>
<th class="head">&nbsp;</th>
<th class="head" colspan="4">PhyID</th>
<th class="head">&nbsp;</th>
<th class="head" colspan="4">Disk Name</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>21</td>
<td>22</td>
<td>23</td>
<td>24</td>
<td rowspan="6">&nbsp;</td>
<td>0</td>
<td>1</td>
<td>2</td>
<td>3</td>
<td rowspan="6">&nbsp;</td>
<td>sdb</td>
<td>sdc</td>
<td>sdd</td>
<td>sde</td>
</tr>
<tr class="row-odd"><td>17</td>
<td>18</td>
<td>19</td>
<td>20</td>
<td>4</td>
<td>5</td>
<td>6</td>
<td>7</td>
<td>sdf</td>
<td>sdg</td>
<td>sdh</td>
<td>sdi</td>
</tr>
<tr class="row-even"><td>13</td>
<td>14</td>
<td>15</td>
<td>16</td>
<td>8</td>
<td>9</td>
<td>10</td>
<td>11</td>
<td>sdj</td>
<td>sdk</td>
<td>sdl</td>
<td>sdm</td>
</tr>
<tr class="row-odd"><td>9</td>
<td>10</td>
<td>11</td>
<td>12</td>
<td>12</td>
<td>13</td>
<td>14</td>
<td>15</td>
<td>sdn</td>
<td>sdo</td>
<td>sdp</td>
<td>sdq</td>
</tr>
<tr class="row-even"><td>5</td>
<td>6</td>
<td>7</td>
<td>8</td>
<td>16</td>
<td>17</td>
<td>18</td>
<td>19</td>
<td>sdr</td>
<td>sds</td>
<td>sdt</td>
<td>sdu</td>
</tr>
<tr class="row-odd"><td>1</td>
<td>2</td>
<td>3</td>
<td>4</td>
<td>20</td>
<td>21</td>
<td>22</td>
<td>23</td>
<td>sdv</td>
<td>sdw</td>
<td>sdx</td>
<td>sdy</td>
</tr>
</tbody>
</table>
{%endraw%}


#### 磁盘位置和 phyid

磁盘位置和 phyid 对应关系的获取，目前是通过 [sg3_utils](http://www.linuxfromscratch.org/blfs/view/svn/general/sg3_utils.html) 工具包里的 sg_ses 命令来实现。

执行如下命令，将指定的 phyid 对应的 led 灯点亮，获取磁盘位置和 phyid 之间的对应。
```shell
sg_ses --set=fault --index=phyid sg 设备
```
*   –set=fault 将 phyid 对应位置的 led 灯设置为 fault 状态（红色常亮状态）
*   –index=phyid 指定要设置的 phyid。一般来说，phyid 的索引从 0 开始，如果背板有 24 盘位，那么背板的 phyid 就是 0~23。
*   sg 设备 背板对应的设备，可以通过多种方式获取，最简单的方式是通过 sg3_utils 工具包里的 sg_map 命令获取，没有磁盘对应的 sg 设备就是背板的 sg 设备。如下例，/dev/sg4 就是背板的 sg 设备。
```bash
[root@Storage ~]# sg_map
/dev/sg0  /dev/sda
/dev/sg1  /dev/sdb
/dev/sg2  /dev/sdc
/dev/sg3  /dev/sdd
/dev/sg4
```
#### 磁盘名称和 phyid

磁盘名称和 phyid 之间的对应关系，是通过目录的遍历来完成（/sys/class/sas_device/），先找到插到背板上所有的磁盘。
```bash
[root@Storage ~]# ls -1d /sys/class/sas_device/expander-0:0/device/phy-*/port/end_device-*/target*/*/block/*
/sys/class/sas_device/expander-0:0/device/phy-0:0:13/port/end_device-0:0:0/target0:0:0/0:0:0:0/block/sdb
/sys/class/sas_device/expander-0:0/device/phy-0:0:17/port/end_device-0:0:1/target0:0:1/0:0:1:0/block/sdc
/sys/class/sas_device/expander-0:0/device/phy-0:0:21/port/end_device-0:0:2/target0:0:2/0:0:2:0/block/sdd
```
依次处理：

1.  每行记录截取到/port/之前的位置，比如”/sys/class/sas_device/expander-0:0/device/phy-0:0:13/port/end_device-0:0:0/target0:0:0/0:0:0:0/block/sdb”，截取的路径为”/sys/class/sas_device/expander-0:0/device/phy-0:0:13”。
2.  进入截取目录位置，找到子目录”sas_phy”。
3.  进入”sas_phy”目录，找到以字符”phy-“开始的子目录，一般和第一步截取后目录名相同，这里就是”phy-0:0:13”。
4.  进入”phy-0:0:13”，读取该目录下的”phy_identifier”文件，获取到的值即为磁盘对应的 phyid。

则磁盘”sdb”对应的 phyid 文件全路径为”/sys/class/sas_device/expander-0:0/device/phy-0:0:13/sas_phy/phy-0:0:13/phy_identifier”，对应的 phyid 为”13”。

### 背板厂商判定模块 - digidiskproduct.py

背板厂商判定模块其实是 Phyid 和磁盘位置关系的固化，当某个固件的背板把 Phyid 和磁盘位置关系找出来以后，在固件不发生大的改变的情况下，这种对应关系是稳定的，为了避免重复性工作，需要将这种关系固化下来。

这样就又需要一种关系映射，也就是需要一个标示、关键字，python 里讲就是需要一个 key，因为这种关系是同背板固件相关，所以就想着从背板上获取这个标示，最后选择根据背板的 product_id（/sys/class/sas_expander/expander-X/product_id）来判断。

还有一个状态会体现在这个 key 里，背板上的插槽数量，也就是这个背板是多少盘位的（8、12、16 还是 24）。

**注意**：这里 key 没有直接使用 product_id 的值，因为可读性太差，根据不同的 product_id，生成一个厂家和盘位的组合，这个组合被用来当做 key。

比如 product_id 为 80H10341807A0，根据适配的过程，可以知道这是一款勤诚的 24 盘位的背板，那么 key 就是 **CHENBROPHYIDMAP24** ，**CHENBRO** 表示勤诚，**PHYIDMAP** 表示这是通过 phyid 找位置的映射（phyid 是 key，位置是 value），**24** 表示 24 盘位。
```plain
CHENBROPHYIDMAP24 = {
    '20' : '21','21' : '22','22' : '23','23' : '24',
    '16' : '17','17' : '18','18' : '19','19' : '20',
    '12' : '13','13' : '14','14' : '15','15' : '16',
    '8'  : '9',  '9' : '10','10' : '11','11' : '12',
    '4'  : '5',  '5' : '6',  '6' : '7',  '7' : '8',
    '0'  : '1',  '1' : '2',  '2' : '3',  '3' : '4'
}
```
### 磁盘灯设置模块 - digidisklight.py

磁盘灯设置也是使用 sg3_utils 工具包里的 sg_ses 命令来实现（和获取磁盘位置和 phyid 对应关系方法一样）。

模块在通过 phyid 设置 led 灯的基础上进行了扩展，允许通过磁盘位置和磁盘名称来设置 led 灯（对应关系固化前提下）。

sg_ses 命令功能很强大，查看它的帮助信息，可以看到如下：
```bash
[root@Storage ~]# sg_ses --help
Usage: sg_ses [--byte1=B1] [--clear=STR] [--control] [--data=H,H...]
              [--descriptor=DN] [--enumerate] [--filter] [--get=STR]
              [--help] [--hex] [--index=IIA | --index=TIA,II]
              [--inner-hex] [--join] [--list] [--nickname=SEN]
              [--nickid=SEID] [--page=PG] [--raw] [--set=STR]
              [--status] [--verbose] [--version] DEVICE
```
我们只使用了其中的 led 灯点亮/熄灭功能。

设置磁盘灯命令如下：
```bash
sg_ses --set=STR --index=TIA,II DEVICE
```
清除磁盘灯命令如下：
```bash
sg_ses --clear=STR --index=TIA,II DEVICE
```
通过控制背板的 led 灯闪烁的频率或是常亮，我们可以实现不同的组合，对每个组合进行定义，就能表达我们想要的内容。（由于每个背板固件对 led 灯控制的支持不尽相同，所以实际效果是有出入的，需要保证的一点是 **损坏** 状态一定要明确的表现出来，以便于坏盘的更换。）

和 phyid 和磁盘位置关系的固化一样，这里也是通过背板厂家来区分不同背板 led 灯对应不同的状态，目前已支持的状态如下：

- 鲸鲨背板
```plain
{
    '1' : '',           #使用中
    '2' : 'missing',    #未使用
    '3' : '',           #热备
    '4' : '',           #重构
    '-2': 'fault',      #损坏
    '-1': 'active'      #未激活
}
```
- 迎广背板：
```plain
{
    '1' : '',           #使用中
    '2' : 'ok',         #未使用
    '3' : 'hotspare',   #热备
    '4' : 'active',     #重构
    '-2': 'fault',      #损坏
    '-1': 'rsvddevice'  #未激活
}
```
- 勤诚背板：
```plain
{
    '1' : '',           #使用中
    '2' : '',           #未使用
    '3' : '',           #热备
    '4' : '',           #重构
    '-2': 'fault',      #损坏
    '-1': ''            #未激活
}
```
### 使用方法

磁盘模块使用时主要是调用磁盘名和磁盘位置对应关系模块（digidiskmap.py）和磁盘灯设置模块（digidisklight.py），digidiskproduct.py 基本是常量模块，只有在新的背板适配时才会修改。

### 磁盘名和磁盘位置对应关系模块 - digidiskmap.py

该模块会获取所有的背板和磁盘信息，从固化的磁盘位置和 phyid 映射中查找，匹配成功会返回磁盘和盘位的对应关系，磁盘和 phyid 的对应关系，背板信息。
 
{%raw%}
<table class="docutils field-list" frame="void" rules="none">
<colgroup><col class="field-name">
<col class="field-body">
</colgroup><tbody valign="top">
<tr class="field-odd field"><th class="field-name">作用:</th><td class="field-body"><p class="first">获取当前设备的 <strong>磁盘名:磁盘位置</strong> 对应关系、<strong>磁盘名:phyid</strong> 对应关系、<strong>背板信息</strong></p>
</td>
</tr>
<tr class="field-even field"><th class="field-name">输入:</th><td class="field-body"><p class="first">jsonformat</p>
<table border="1" class="docutils">
<colgroup>
<col width="25%">
<col width="25%">
<col width="25%">
<col width="25%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">参数</th>
<th class="head">值</th>
<th class="head">类型</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>jsonformat</td>
<td>True|False</td>
<td>bool</td>
<td>是否以JSON字符串格式返回</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">输出:</th><td class="field-body"><p class="first">[disknamemap,disknamephymap,expanders]</p>
<table border="1" class="docutils">
<colgroup>
<col width="25%">
<col width="25%">
<col width="25%">
<col width="25%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">参数</th>
<th class="head">值</th>
<th class="head">类型</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>disknamemap</td>
<td>{磁盘名称:磁盘位置}</td>
<td>dict</td>
<td>磁盘和盘位对应关系</td>
</tr>
<tr class="row-odd"><td>disknamephymap</td>
<td>{磁盘名称:phyid}</td>
<td>dict</td>
<td>磁盘和盘位对应关系</td>
</tr>
<tr class="row-even"><td>expanders</td>
<td>{背板编号:{背板信息}}</td>
<td>dict</td>
<td>背板信息</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-even field"><th class="field-name">示例:</th><td class="field-body"><div class="first last highlight-python"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">digidisk</span> <span class="kn">import</span> <span class="n">digidiskmap</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">digidiskmap</span><span class="o">.</span><span class="n">get_diskmap</span><span class="p">(</span><span class="bp">False</span><span class="p">)</span>
<span class="go">[</span>
<span class="go">   {'sdd': '0-22', 'sdb': '0-14', 'sdc': '0-18'},</span>
<span class="go">   {'sdd': '21', 'sdb': '13', 'sdc': '17'},</span>
<span class="go">   {'0':</span>
<span class="go">       {</span>
<span class="go">           'id': '0',</span>
<span class="go">           'name': 'expander-0:0',</span>
<span class="go">           'count': '24',</span>
<span class="go">           'product': 'CHENBRO',</span>
<span class="go">           'smpdevice': 'sg4',</span>
<span class="go">           'model': '80H10341807A0',</span>
<span class="go">           'sasaddress': '0x5001c45001d099bf',</span>
<span class="go">           'hard': False</span>
<span class="go">       }</span>
<span class="go">   }</span>
<span class="go">]</span>
</pre></div>
</div>
</td>
</tr>
</tbody>
</table>
{%endraw%}

### 磁盘灯设置模块 - digidisklight.py

该模块会根据用户传入的 phyid、磁盘位置、磁盘名称，状态等参数，设置或清除对应位置的 led 灯状态。

传入的状态可以为具体的状态值（string），也可以预定义的状态值对应的数字。

磁盘状态
{%raw%}
<table border="1" class="colwidths-given docutils" id="id10">
<caption><span class="caption-text">磁盘状态</span><a class="headerlink" href="#id10" title="永久链接至表格">¶</a></caption>
<colgroup>
<col width="25%">
<col width="38%">
<col width="38%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">数字</th>
<th class="head">对应的状态</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>1</td>
<td>inuse</td>
<td>使用中</td>
</tr>
<tr class="row-odd"><td>2</td>
<td>unuse</td>
<td>未使用</td>
</tr>
<tr class="row-even"><td>3</td>
<td>spare</td>
<td>热备</td>
</tr>
<tr class="row-odd"><td>4</td>
<td>rebuild</td>
<td>重构</td>
</tr>
<tr class="row-even"><td>-1</td>
<td>inactive</td>
<td>未激活</td>
</tr>
<tr class="row-odd"><td>-2</td>
<td>broken</td>
<td>损坏</td>
</tr>
</tbody>
</table>
{%endraw%}

#### 设置磁盘灯状态

`setdisklight`(_**kwargs_)[¶](# "永久链接至目标")
{%raw%}
<table class="docutils field-list" frame="void" rules="none">
<colgroup><col class="field-name">
<col class="field-body">
</colgroup><tbody valign="top">
<tr class="field-odd field"><th class="field-name">作用:</th><td class="field-body"><p class="first">设置 <strong>指定位置</strong> 或 <strong>整个背板</strong> 的 <strong>磁盘灯</strong> 为 <strong>指定状态</strong></p>
</td>
</tr>
<tr class="field-even field"><th class="field-name">说明:</th><td class="field-body"><ol class="first arabic simple">
<li>dpid、dlid和dname中的任意一个参数都对应背板上一个固定位置。使用dpid和dlid时，如果未体现背板信息（如：0-X），就需要通过eid或esg等参数来补充。</li>
<li>未指定dpid、dlid、dname等定位参数但指定esg、eid等背板参数时，设置整个背板。</li>
</ol>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">输入:</th><td class="field-body"><p class="first">键值对</p>
<table border="1" class="docutils">
<colgroup>
<col width="25%">
<col width="25%">
<col width="25%">
<col width="25%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">参数</th>
<th class="head">值</th>
<th class="head">类型</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>dpid</td>
<td>X-X|X，X为数字</td>
<td>string</td>
<td>磁盘对应的phy_identifier编号。格式为0-0，表示expanderid:phyid，如果格式为0，则需要指定eid或esg。</td>
</tr>
<tr class="row-odd"><td>dlid</td>
<td>X-X|X，X为数字</td>
<td>string</td>
<td>磁盘对应的位置编号。格式为0-1，表示expanderid:locateid；如果格式为1，则需要指定eid或esg。</td>
</tr>
<tr class="row-even"><td>dname</td>
<td>sdX。</td>
<td>string</td>
<td>磁盘名称。如果指定esg或eid，在对应背板上搜索磁盘；未指定时需遍历所有背板。</td>
</tr>
<tr class="row-odd"><td>esg</td>
<td>/dev/sgX，X为数字</td>
<td>string</td>
<td>背板对应的sg设备</td>
</tr>
<tr class="row-even"><td>eid</td>
<td>X，X为数字</td>
<td>string</td>
<td>背板对应的编号</td>
</tr>
<tr class="row-odd"><td>eproduct</td>
<td>INWIN|CHENBRO|ESTOR</td>
<td>string</td>
<td>背板厂商。和ecount组合，在只提供dlid的时候获取phy_identifier编号。</td>
</tr>
<tr class="row-even"><td>ecount</td>
<td>8|12|16|24</td>
<td>string</td>
<td>背板盘位</td>
</tr>
<tr class="row-odd"><td>light</td>
<td>1|2|3|4|-1|-2
inuse|unuse|spare|rebuild|inactive|fault
missing|fault|active|locate|hotspare|rsvddevice</td>
<td>string</td>
<td>磁盘灯状态。参考 <a class="reference internal" href="#tb-diskstatus"><span class="std std-ref">磁盘状态</span></a>。</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-even field"><th class="field-name">输出:</th><td class="field-body"><p class="first">数字</p>
<table border="1" class="docutils">
<colgroup>
<col width="25%">
<col width="25%">
<col width="25%">
<col width="25%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">参数</th>
<th class="head">值</th>
<th class="head">类型</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>retcode</td>
<td>0|-1|-2|-3|-4</td>
<td>int</td>
<td>设置磁盘灯结果</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">释义:</th><td class="field-body"><table border="1" class="first docutils">
<colgroup>
<col width="50%">
<col width="50%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">值</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>0</td>
<td>成功</td>
</tr>
<tr class="row-odd"><td>-1</td>
<td>参数不足</td>
</tr>
<tr class="row-even"><td>-2</td>
<td>错误的磁盘灯</td>
</tr>
<tr class="row-odd"><td>-3</td>
<td>未适配背板灯</td>
</tr>
<tr class="row-even"><td>-4</td>
<td>未适配背板盘位</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-even field"><th class="field-name">示例:</th><td class="field-body"><div class="first last highlight-python"><div class="highlight"><pre><span></span><span class="c1">#设置phyid为22的位置状态为'-2'(broken)</span>
<span class="o">&gt;&gt;&gt;</span> <span class="kn">from</span> <span class="nn">digidisk</span> <span class="kn">import</span> <span class="n">digidisklight</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">setdisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dpid'</span><span class="p">:</span><span class="s1">'22'</span><span class="p">,</span><span class="s1">'esg'</span><span class="p">:</span><span class="s1">'sg4'</span><span class="p">,</span><span class="s1">'light'</span><span class="p">:</span><span class="s1">'-2'</span><span class="p">})</span>
<span class="mi">0</span>
<span class="c1">#设置磁盘位置为12的状态为broken</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">setdisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dlid'</span><span class="p">:</span><span class="s1">'0-12'</span><span class="p">,</span><span class="s1">'light'</span><span class="p">:</span><span class="s1">'broken'</span><span class="p">})</span>
<span class="mi">0</span>
<span class="c1">#设置phyid为22的位置状态为broken</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">setdisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dpid'</span><span class="p">:</span><span class="s1">'0-22'</span><span class="p">,</span><span class="s1">'light'</span><span class="p">:</span><span class="s1">'broken'</span><span class="p">})</span>
<span class="mi">0</span>
<span class="c1">#设置磁盘sdb状态为broken</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">setdisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dname'</span><span class="p">:</span><span class="s1">'sdb'</span><span class="p">,</span><span class="s1">'light'</span><span class="p">:</span><span class="s1">'broken'</span><span class="p">})</span>
<span class="mi">0</span>
</pre></div>
</div>
</td>
</tr>
</tbody>
</table>
{%endraw%}

#### 清除磁盘灯状态

`cleardisklight`(_**kwargs_)[¶](# "永久链接至目标")

{%raw%}
<table class="docutils field-list" frame="void" rules="none">
<colgroup><col class="field-name">
<col class="field-body">
</colgroup><tbody valign="top">
<tr class="field-odd field"><th class="field-name">作用:</th><td class="field-body"><p class="first">清除 指定位置 或 整个背板 的 磁盘灯 的 指定状态 或 全部状态</p>
</td>
</tr>
<tr class="field-even field"><th class="field-name">说明:</th><td class="field-body"><ol class="first arabic simple">
<li>指定磁盘灯状态时只清除该状态，不指定磁盘灯状态时清除所有状态。</li>
<li>未指定dpid、dlid、dname等定位磁盘参数但指定esg、eid等背板参数时，清除整个背板。</li>
<li>需要注意的是，因为背板固件支持的不同，不是所有磁盘状态都有表现在磁盘灯上，这里只能保证 <strong>磁盘损坏</strong> 时的磁盘灯状态。</li>
</ol>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">输入:</th><td class="field-body"><p class="first">键值对</p>
<table border="1" class="docutils">
<colgroup>
<col width="25%">
<col width="25%">
<col width="25%">
<col width="25%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">参数</th>
<th class="head">值</th>
<th class="head">类型</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>dpid</td>
<td>X-X|X，X为数字</td>
<td>string</td>
<td>磁盘对应的phy_identifier编号。格式为0-0，表示expanderid:phyid，如果格式为0，则需要指定eid或esg。</td>
</tr>
<tr class="row-odd"><td>dlid</td>
<td>X-X|X，X为数字</td>
<td>string</td>
<td>磁盘对应的位置编号。格式为0-1，表示expanderid:locateid；如果格式为1，则需要指定eid或esg。</td>
</tr>
<tr class="row-even"><td>dname</td>
<td>sdX。</td>
<td>string</td>
<td>磁盘名称。如果指定esg或eid，在对应背板上搜索磁盘；未指定时需遍历所有背板。</td>
</tr>
<tr class="row-odd"><td>esg</td>
<td>/dev/sgX，X为数字</td>
<td>string</td>
<td>背板对应的sg设备</td>
</tr>
<tr class="row-even"><td>eid</td>
<td>X，X为数字</td>
<td>string</td>
<td>背板对应的编号</td>
</tr>
<tr class="row-odd"><td>eproduct</td>
<td>INWIN|CHENBRO|ESTOR</td>
<td>string</td>
<td>背板厂商。和ecount组合，在只提供dlid的时候获取phy_identifier编号。</td>
</tr>
<tr class="row-even"><td>ecount</td>
<td>8|12|16|24</td>
<td>string</td>
<td>背板盘位</td>
</tr>
<tr class="row-odd"><td>light</td>
<td>1|2|3|4|-1|-2
inuse|unuse|spare|rebuild|inactive|fault
missing|fault|active|locate|hotspare|rsvddevice</td>
<td>string</td>
<td>磁盘灯状态。参考 <a class="reference internal" href="#tb-diskstatus"><span class="std std-ref">磁盘状态</span></a>。</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-even field"><th class="field-name">输出:</th><td class="field-body"><p class="first">数字</p>
<table border="1" class="docutils">
<colgroup>
<col width="25%">
<col width="25%">
<col width="25%">
<col width="25%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">参数</th>
<th class="head">值</th>
<th class="head">类型</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>retcode</td>
<td>0|-1|-2|-3|-4</td>
<td>int</td>
<td>清除磁盘灯结果</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-odd field"><th class="field-name">释义:</th><td class="field-body"><table border="1" class="first docutils">
<colgroup>
<col width="50%">
<col width="50%">
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">值</th>
<th class="head">释义</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>0</td>
<td>成功</td>
</tr>
<tr class="row-odd"><td>-1</td>
<td>参数不足</td>
</tr>
<tr class="row-even"><td>-2</td>
<td>错误的磁盘灯</td>
</tr>
<tr class="row-odd"><td>-3</td>
<td>未适配背板灯</td>
</tr>
<tr class="row-even"><td>-4</td>
<td>未适配背板盘位</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr class="field-even field"><th class="field-name">示例:</th><td class="field-body"><div class="first last highlight-python"><div class="highlight"><pre><span></span><span class="c1">#清除编号为0的背板上所有位置所有状态</span>
<span class="o">&gt;&gt;&gt;</span> <span class="kn">from</span> <span class="nn">digidisk</span> <span class="kn">import</span> <span class="n">digidisklight</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">cleardisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'eid'</span><span class="p">:</span><span class="s1">'0'</span><span class="p">})</span>
<span class="mi">0</span>
<span class="c1">#清除编号为0的背板上phyid为22位置的所有状态</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">cleardisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dpid'</span><span class="p">:</span><span class="s1">'0-22'</span><span class="p">})</span>
<span class="mi">0</span>
<span class="c1">#phyid不包含背板信息时，需要单独指定eid或esg。</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">cleardisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dpid'</span><span class="p">:</span><span class="s1">'22'</span><span class="p">,</span><span class="s1">'eid'</span><span class="p">:</span><span class="s1">'0'</span><span class="p">})</span>
<span class="mi">0</span>
<span class="c1">#清除磁盘sdb状态broken</span>
<span class="o">&gt;&gt;&gt;</span> <span class="n">digidisklight</span><span class="o">.</span><span class="n">cleardisklight</span><span class="p">(</span><span class="o">**</span><span class="p">{</span><span class="s1">'dname'</span><span class="p">:</span><span class="s1">'sdb'</span><span class="p">,</span><span class="s1">'light'</span><span class="p">:</span><span class="s1">'broken'</span><span class="p">})</span>
<span class="mi">0</span>
</pre></div>
</div>
</td>
</tr>
</tbody>
</table>
{%endraw%}