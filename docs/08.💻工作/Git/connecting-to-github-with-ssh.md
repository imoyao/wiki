---
title: 使用 SSH 连接到 GitHub
date: 2020-12-06 10:16:16
tags: 
  - GitHub
  - Git
  - SSH
  - ssh_agent
  - ssh_key
categories: 
  - U0001F4BB 工作
  - Git
permalink: /pages/db03c4/
---
## 前言
终于厌烦了每一次往远程仓库推送代码时都要手动输入用户名和密码验证个人信息，所以配置了一下 SSH 认证。

## [关于 SSH](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/about-ssh)

{% note info %}

SSH 为 Secure Shell 的缩写，由 IETF 的网络小组（Network Working Group）所制定；SSH 为建立在应用层基础上的安全协议。

{% endnote %}

使用 SSH 协议可以连接远程服务器和服务并向它们验证。 利用 SSH 密钥可以连接 GitHub，而无需在每次访问时都提供用户名和个人访问令牌。


## [检查现有 SSH 密钥→](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/checking-for-existing-ssh-keys)

在生成 SSH 密钥之前，您可以检查是否有任何现有的 SSH 密钥。

## [生成新 SSH 密钥并添加到 ssh-agent→](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

检查现有 SSH 密钥后，您可以生成新 SSH 密钥以用于身份验证，然后将其添加到 ssh-agent。

## [新增 SSH 密钥到 GitHub 帐户→](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account)

要配置 GitHub 帐户使用新的（或现有）SSH 密钥，您还需要将其添加到 GitHub 帐户。

## [测试 SSH 连接→](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/testing-your-ssh-connection)

设置 SSH 密钥并将其添加到您的 GitHub 帐户后，您可以测试连接。

## [使用 SSH 密钥密码→](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/working-with-ssh-key-passphrases)

您可以保护 SSH 密钥并配置身份验证代理，这样您就不必在每次使用 SSH 密钥时重新输入密码。

## 其他

### 之前使用 https 克隆

对于已经克隆到本地的 https 类型仓库，我们可以通过修改 git 配置的方式实现 SSH 连接到远程仓库。
```plain
vim .git/config
```
像下面改 url
```plain
[remote "origin"]
url = git@github.com:hpcpp/hello-world.git
```

### Permission denied
```bash
ssh -T git@github.com
git@github.com: Permission denied (publickey).
```
直接添加刚才新增的 key
```bash
ssh-add ~/.ssh/id_imoyao  # 替换成你自己的 key
```

### Could not open a connection to your authentication agent
```bash
ssh-agent bash
```
### 每次开机自启动 ssh_agent

**Windows** 上 **自动启动 git-agent** 以及 **自动加载 SSH Key** 的方法

这里的 **自动** 指的是，每次启动 **Git Bash** 这个客户端时

1. 新建文件 `~/.profile` ，即 `/c/Users/XXX/profile` ，然后写入如下内容

```bash
env=~/.ssh/agent.env  
  
agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }  
  
agent_start () {  
 (umask 077; ssh-agent >| "$env")  
 . "$env" >| /dev/null ; }  
  
agent_load_env  
  
# agent_run_state: 0=agent running w/ key; 1=agent w/o key; 2= agent not running  
agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)  
  
if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then  
 agent_start  
 ssh-add  
 ssh-add ~/.ssh/github  # 如果自定义了 key 的名字或者路径，则需要写在这里  
 ssh-add ~/.ssh/coding  
elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then  
 ssh-add  
 ssh-add ~/.ssh/github  # 如果自定义了 key 的名字或者路径，则需要写在这里  
 ssh-add ~/.ssh/coding  
fi  
  
unset env  
```
2. 在新开 **Git Bash** 时，如果看到如下信息，表示 **ssh-agent** 打开成功，**SSH Key** 加载成功。

```plain
Identity added: /c/Users/XXX/.ssh/id_rsa (/c/Users/XXX/.ssh/id_rsa)  
Identity added: /c/Users/XXX/.ssh/github (/c/Users/XXX/.ssh/github)  
Identity added: /c/Users/XXX/.ssh/coding (/c/Users/XXX/.ssh/coding)  
```
3. 然后，可以通过 `ssh -T` 命令才测试一下，看到如下信息表示添加测试通过。

```bash
$ ssh -T git@github.com  
Hi XXX! You've successfully authenticated, but GitHub does not provide shell access.  

$ ssh -T git@git.coding.net  
Warning: Permanently added the RSA host key for IP address '123.XX.XX.XX' to the list of known hosts.  
Coding 提示: Hello XXX, You've connected to Coding.net via SSH. This is a personal key.  
```
XXX，你好，你已经通过 SSH 协议认证 Coding.net 服务，这是一个个人公钥

## 参考链接
[使用 SSH 连接到 GitHub - GitHub Docs](https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh)
[GitHub 教程 SSH keys 配置_LolitaSian-CSDN 博客](https://blog.csdn.net/qq_36667170/article/details/79094257)
[通过 SSH 操作 Git 终极教程 | zcdll's Blog](https://zcdll.github.io/2018/01/10/git-ssh/)
