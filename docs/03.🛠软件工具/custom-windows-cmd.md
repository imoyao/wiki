---
title: 自定义 Windows10 终端工具配置
tags: 
  - 工具
categories: 
  - 🛠 工具
date: 2020-04-21 23:19:29

permalink: /pages/638cfb/
---
前言
--

经历了数天的磨难，终于把 OpenWrt 编译成功了 ，为了表达成功的喜悦放了张图，没想到引起了小伙伴们的骚动。于是我决定写一篇关于我现在在 Windows 10 下使用的终端方案的配置教程。

![](https://ximg.now.sh/post/20190814040213.png#vwid=1376&vhei=739)

WSL
---

适用于 Linux 的 Windows 子系统（英语：Windows Subsystem for Linux，简称 WSL）是一个为在 Windows 10 和 Windows Server 2019 上能够原生运行 Linux 二进制可执行文件（ELF 格式）的兼容层。[维基百科](https://p3terx.com/go/aHR0cHM6Ly96aC53aWtpcGVkaWEub3JnL3dpa2kvJUU5JTgwJTgyJUU3JTk0JUE4JUU0JUJBJThFX0xpbnV4XyVFNyU5QSU4NF9XaW5kb3dzXyVFNSVBRCU5MCVFNyVCMyVCQiVFNyVCQiU5Rg==)

强行翻译：**Windows 10 是最好的 Linux 发行版**

### 安装 WSL

如果你没有使用过 WSL ，那么可以按照[微软官方教程](https://p3terx.com/go/aHR0cHM6Ly9kb2NzLm1pY3Jvc29mdC5jb20vemgtY24vd2luZG93cy93c2wvaW5zdGFsbC13aW4xMA==) 来操作。

以管理员身份运行 PowerShell (WIN+X , A)，输入下面的命令，并重启。
```plain
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```
然后去应用商店下载自己喜欢的 Linux 发行版。

![](https://ximg.now.sh/post/20190814190607.png#vwid=1222&vhei=730)
下载好后打开，会提示输入用户名和密码。到这里 WSL 就算安装完成了。

![](https://ximg.now.sh/post/20190814235435.png#vwid=586&vhei=407)

[Terminus](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL0V1Z2VueS90ZXJtaW51cw==)
----------------------------------------------------------------------------------

Terminus 是一个高度可配置的终端模拟器，适用于 Windows、macOS 和 Linux。官方称它是 Windows 标准终端（conhost），PowerShell ISE，PuTTY 或 iTerm 的替代品。

官方宣传图长这样，于是我被吸引了。但其实我的第一反应是又拿 Mac 的图片来骗我，因为之前见过太多软件在 Windows 和 Mac 上的外观差距了。

![](https://ximg.now.sh/post/20190818173825.jpg#vwid=1796&vhei=1351)

[下载](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL0V1Z2VueS90ZXJtaW51cy9yZWxlYXNlcw==)并安装完长这样，跟官方图比有种淘宝卖家秀和买家秀的感觉。

![](https://ximg.now.sh/post/20190814205646.png#vwid=927&vhei=600)

点击右上角的齿轮打开设置，首先看到的是主题外观设置的选项。打开 `Acrylic background` 选项可以开启透明模糊效果。然后会出现 `Background type` 选项，`Fluent` 效果更好，有官方图的感觉了，但拖动窗口时不跟手。“Fluent” 翻译成中文是 “流畅”，而 “Blur” 是 “模糊”，然而效果恰恰相反，这就有点讽刺了。（注：此处的 “Fluent” 应该是指的微软的 [Fluent Design](https://p3terx.com/go/aHR0cHM6Ly93d3cubWljcm9zb2Z0LmNvbS9kZXNpZ24vZmx1ZW50) ，感谢评论区大佬 [@XYenon](https://p3terx.com/archives/the-strongest-terminal-solution-under-windows-10.html/comment-page-1) 指正）

![](https://ximg.now.sh/post/20190814211830.png#vwid=1206&vhei=740)

接着打开 `Shell` 设置，在 `Profile` 选择 `WSL/Ubantu`，这样默认新建的窗口就是 WSL 了。

![](https://ximg.now.sh/post/20190814212650.png#vwid=1206&vhei=740)

[Oh My Zsh](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3JvYmJ5cnVzc2VsbC9vaC1teS16c2g=)
-------------------------------------------------------------------------------------------

> **Oh My Zsh will not make you a 10x developer...but you may feel like one.**

上面那句话来自 [Oh My Zsh README](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3JvYmJ5cnVzc2VsbC9vaC1teS16c2gvYmxvYi9tYXN0ZXIvUkVBRE1FLm1k) ，意思是 “装逼是第一生产力”。(大雾

我使用 Oh My Zsh 倒不是为把终端搞得花里胡哨去装逼，作为一个实用主义者，我非常喜欢自动建议、补全和代码高亮功能，这极大的提高了终端的输入效率。

### 安装 zsh
```plain
    apt update && apt install -y zsh
```
### 安装 Oh My Zsh

使用 curl 下载安装
```plain
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
使用 wget 下载安装
```plain
    sh -c "$(wget -O- https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
Oh My Zsh 安装完成后会提示你设置 zsh 为默认 sehll 。如果没有提示，输入下面的命令进行设置：
```plain
    chsh -s $(which zsh)
```
### 修改 Oh My Zsh 主题

Oh My Zsh 有很多[内置主题](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3JvYmJ5cnVzc2VsbC9vaC1teS16c2gvd2lraS90aGVtZXM=) ，只需要修改配置文件即可启用。也可以选择安装 [外置主题](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3JvYmJ5cnVzc2VsbC9vaC1teS16c2gvd2lraS9FeHRlcm5hbC10aGVtZXM=) ，比如 [Powerlevel10k](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3JvbWthdHYvcG93ZXJsZXZlbDEwaw==) 。

我使用的主题是 [ys](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3JvYmJ5cnVzc2VsbC9vaC1teS16c2gvd2lraS90aGVtZXMjeXM=) ，简单实用，不花里胡哨。使用 `sed` 命令一键修改：
```plain
    sed -i '/^ZSH_THEME=/c\ZSH_THEME="ys"' ~/.zshrc
```
修改后输入下面的命令刷新配置就可以看到效果：
```plain
    source ~/.zshrc
```
### 安装 Oh My Zsh 插件

安装 [zsh-syntax-highlighting](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3pzaC11c2Vycy96c2gtc3ludGF4LWhpZ2hsaWdodGluZw==) （代码高亮）
```plain
    git clone https://github.com/zsh-users/zsh-syntax-highlighting $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```
安装 [zsh-autosuggestions](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3pzaC11c2Vycy96c2gtYXV0b3N1Z2dlc3Rpb25z) （自动建议）
```plain
    git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```
安装 [zsh-completions](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL3pzaC11c2Vycy96c2gtY29tcGxldGlvbnM=) （自动补全）
```plain
    git clone https://github.com/zsh-users/zsh-completions $ZSH_CUSTOM/plugins/zsh-completions
```
zsh-completions 插件还需把 `autoload -U compinit && compinit` 添加到`.zshrc`。输入命令可一键添加：
```plain
    [ -z "`grep "autoload -U compinit && compinit" ~/.zshrc`" ] && echo "autoload -U compinit && compinit" >> ~/.zshrc
```
把需要启用的插件写入到配置文件中，使用 `sed` 命令一键操作：
```plain
    sed -i '/^plugins=/c\plugins=(git sudo z zsh-syntax-highlighting zsh-autosuggestions zsh-completions)' ~/.zshrc
```
> 如果你有自己想添加的插件，写在括号内即可，插件名称用空格隔开。

最后应用配置
```plain
    source ~/.zshrc
```
[The Fuck](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL252Ym4vdGhlZnVjaw==)
------------------------------------------------------------------------------

当你想在终端里启动一个程序，并潇洒自信的输入了一个命令时，却发现指令貌似出错了，但找了半天又不知道错在哪里。

此时自然会血压飙升，一句 “What the fuck ？！” 就挂在嘴边，快要喷口而出了！

有了 [The Fuck](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL252Ym4vdGhlZnVjaw==) ，你就不会需要 WTF 这句芬芳之语。

你只需要再在终端里输入一个 `fuck`，这个软件就能帮你迅速的找出指令的错误在哪里了。

![](https://ximg.now.sh/post/20190814175904.gif#vwid=686&vhei=379)

（文案来自于[差评](https://p3terx.com/go/aHR0cHM6Ly9tcC53ZWl4aW4ucXEuY29tL3MvVllCb0I2dGF5QnJyNFc3VjVfUTB1UQ==) ，写得太好了，所以我也没必要自己水了。图片来自官方 [README](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL252Ym4vdGhlZnVjaw==) )

### 安装 The Fuck

我的 WSL 使用的是 Ubuntu ，按照[官方教程](https://p3terx.com/go/aHR0cHM6Ly9naXRodWIuY29tL252Ym4vdGhlZnVjayNpbnN0YWxsYXRpb24=) 输入以下命令进行安装
```plain
    sudo apt update
    sudo apt install python3-dev python3-pip python3-setuptools
    sudo pip3 install thefuck
```
安装完后输入 `fuck` 会提示将 `eval $(thefuck --alias)` 添加到 `~/.zshrc` 中。此时你只需要再输入一次 `fuck`，就会自动进行添加，这也算你第一次成功体验到 The Fuck 的功能了。

![](https://ximg.now.sh/post/20190815030056.png#vwid=929&vhei=268)

最后应用配置
```plain
    source ~/.zshrc
```
尾巴
--

以上就是这套 “最强终端” 方案的配置方法。其实做出来完全是无心插柳，因为觉得 Xshell 不好用，就想找替代品，结果阴差阳错的在 GitHub 的 Terminal 话题下找到了 Terminus 这款终端软件，最后经过瞎 JB 折腾，搞了这套方案。

Terminus 在 SSH 的功能体验远远比不上 Xshell ，而且因为软件还处于测试阶段，bug 还挺很多的，就比如模糊透明效果在我的另一台设备上使用就出现了问题，偶尔还会卡死，没有滚动条等问题。由于是基于 Electron 打造的，内存占用很感人，打开就有 200M+。再看看 Xshell 才 10M+。虽然目前它还不能取代 Xhsell 作为 SSH 工具来使用，但这套方案替代了我在 Git Bash 和部分 Linux 虚拟机上的使用场景，而且截图时也能拿来装装 X，算是没有白费力气。也希望开发者们加油，把 Terminus 做得更好。



## 本文链接

[打造 Windows 10 下最强终端方案：WSL + Terminus + Oh My Zsh + The Fuck](https://p3terx.com/archives/the-strongest-terminal-solution-under-windows-10.html) 