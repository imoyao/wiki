---
title: Docker 实践手册
tags: 
  - Docker
  - 容器化
  - 容器
top_img: /images/logos/Docker-Logo-White-RGB_Horizontal.png
cover: /images/logos/Docker-logo.png
categories: 
  - 💻 工作
  - Docker
date: 2020-05-07 14:42:38
permalink: /pages/9eabb8/
---
## 什么是 Docker
Docker 是针对程序开发人员和系统管理员来**开发、部署、运行**应用的一个虚拟化平台。
使用容器部署应用程序称为容器化。更多参考：[What is a Container? | App Containerization | Docker](https://www.docker.com/resources/what-container)
### 容器化的优势
灵活：即使最复杂的应用程序也可以容器化。
轻量级：容器利用并共享了主机内核，在系统资源方面比虚拟机更加有效。
可移植：您可以在本地构建，部署到云上并在任何地方运行。
解耦：容器是高度自给自足并封装的容器，使您可以在不破坏其他容器的情况下更换或升级它们。
可扩展：您可以在数据中心内增加并自动分布容器副本。
安全：容器将积极的约束和隔离应用于流程，而无需用户方面的任何配置。
### 镜像和容器
从根本上讲，一个容器不过是一个正在运行的进程，并对其应用了一些附加的封装功能，以使其与主机和其他容器隔离. 容器隔离的最重要方面之一是每个容器都与自己的专用文件系统进行交互. 该文件系统由 Docker 镜像提供。映像包括运行应用程序所需的一切——代码或二进制文件，运行时刻（runtime），依赖项以及所需的任何其他文件系统对象.
### 容器和虚拟机
容器（Linux Containers，缩写为 LXC）在 Linux 上本地运行 ，并与其他容器共享主机的内核。它运行一个隔离的进程，不占用任何其他可执行文件更多的内存，从而使其轻量化。

虚拟机（virtual machine）就是带环境安装的一种解决方案。它可以在一种操作系统里面运行另一种操作系统，比如在 Windows 系统里面运行 Linux 系统。应用程序对此毫无感知，因为虚拟机看上去跟真实系统一模一样，而对于底层系统来说，虚拟机就是一个普通文件，不需要了就删掉，对其他部分毫无影响。

虽然用户可以通过虚拟机还原软件的原始环境。但是，这个方案有几个缺点：
1. 资源占用多
虚拟机会独占一部分内存和硬盘空间。它运行的时候，其他程序就不能使用这些资源了。哪怕虚拟机里面的应用程序实际使用的内存只有 1MB，虚拟机本身依然需要几百 MB 的内存才能运行。
2. 冗余步骤多
虚拟机是完整的操作系统，一些系统级别的操作步骤，往往无法跳过，比如用户登录。
3. 启动慢
启动操作系统需要多久，启动虚拟机就需要多久。可能要等几分钟，应用程序才能真正运行。
![](/images/docker-vs-VM.png)

## Docker 架构
[Docker architecture](https://docs.docker.com/get-started/overview/#docker-architecture)
{% raw %}

<table class="reference">
 <tbody>
<tr><th width="20%">概念</th><th>说明</th></tr>
  <tr>
   <td><p>Docker 镜像(Images)</p></td>
   <td><p>Docker 镜像是用于创建 Docker 容器的模板，比如 Ubuntu 系统。 </p></td>
  </tr>
  <tr>
   <td><p>Docker 容器(Container)</p></td>
   <td><p>容器是独立运行的一个或一组应用，是镜像运行时的实体。</p></td>
  </tr>
  <tr>
   <td><p>Docker 客户端(Client)</p></td>
   <td><p>
Docker 客户端通过命令行或者其他工具使用 Docker SDK (<a href="https://docs.docker.com/develop/sdk/" target="_blank" rel="noopener noreferrer">https://docs.docker.com/develop/sdk/</a>) 与 Docker 的守护进程通信。</p></td>
  </tr>
  <tr>
   <td><p>Docker 主机(Host)</p></td>
   <td><p>一个物理或者虚拟的机器用于执行 Docker  守护进程和容器。</p></td>
  </tr>
  <tr>
   <td><p>Docker Registry</p></td>
   <td><p>Docker 仓库用来保存镜像，可以理解为代码控制中的代码仓库。</p>
<p>Docker Hub(<a href="https://hub.docker.com" target="_blank" rel="noopener noreferrer">https://hub.docker.com</a>) 提供了庞大的镜像集合供使用。</p>
  <p>一个 Docker Registry 中可以包含多个仓库（Repository）；每个仓库可以包含多个标签（Tag）；每个标签对应一个镜像。</p>

<p>通常，一个仓库会包含同一个软件不同版本的镜像，而标签就常用于对应该软件的各个版本。我们可以通过 <span class="marked">&lt;仓库名&gt;:&lt;标签&gt;</span> 的格式来指定具体是这个软件哪个版本的镜像。如果不给出标签，将以 <strong>latest</strong> 作为默认标签。</p></td>
  </tr>
  <tr>
   <td><p>Docker Machine</p></td>
   <td><p>Docker Machine是一个简化Docker安装的命令行工具，通过一个简单的命令行即可在相应的平台上安装Docker，比如VirtualBox、 Digital Ocean、Microsoft Azure。</p></td>
  </tr>
 </tbody>
</table>

{% endraw %}

## docker 环境安装
 参考[Install Docker Engine on CentOS | Docker Documentation](https://docs.docker.com/engine/install/centos/)
### 安装校验
- 状态测试
```shell
systemctl status docker
```
```plain
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2020-05-06 18:14:52 CST; 22h ago
     Docs: http://docs.docker.com
# too long no show
Hint: Some lines were ellipsized, use -l to show in full.
```
- 版本检查
```shell
docker --version
```
```plain
Docker version 1.13.1, build 7f2769b/1.13.1
```
- 功能测试
```plain
[root@cephnode1 ~]# docker run hello-world
```
此命令会直接从 image 文件生成正在运行的容器实例，如果镜像不存在，则会自动使用`docker image pull`去仓库抓取。
```plain
WARNING: IPv4 forwarding is disabled. Networking will not work.

Hello from Docker!
This message shows that your installation appears to be working correctly.

# too long no show

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

## 命令
执行`docker --help`可以看到所有支持的指令如下：

```plain
Usage:	docker COMMAND

A self-sufficient runtime for containers

Options:
      --config string      Location of client config files (default "/root/.docker")
  -D, --debug              Enable debug mode
      --help               Print usage
  -H, --host list          Daemon socket(s) to connect to (default [])
  -l, --log-level string   Set the logging level ("debug", "info", "warn", "error", "fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/root/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/root/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/root/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Management Commands:
  container   Manage containers
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  volume      Manage volumes

Commands:
  attach      Attach to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes

Run 'docker COMMAND --help' for more information on a command.

```
更多参考：
- [Docker Command Cheat Sheet - 简书](https://www.jianshu.com/p/b3f42bc85ec3)
- [Docker Free CheatSheet – CheatSheet](https://cheatsheet.dennyzhang.com/cheatsheet-docker-A4)
- [Docker CheatSheet | Docker 配置与实践清单_慕课手记](http://www.imooc.com/article/79968)
- [awesome-cheatsheets/docker.sh at master · LeCoupa/awesome-cheatsheets](https://github.com/LeCoupa/awesome-cheatsheets/blob/master/tools/docker.sh)
- [Docker 命令大全 | 菜鸟教程](https://www.runoob.com/docker/docker-command-manual.html)

## 构建并运行自己的 image

我们可以拉取镜像来运行，但是要制作自己的 image，就需要编写 Dockerfile。它是一个文本文件。Docker 根据改文件生成 image 文件。
以官网的 [例子](https://docs.docker.com/get-started/part2/) 看一下如何构建 image：

1. 首先克隆应用：
```shell
git clone https://github.com/dockersamples/node-bulletin-board
cd node-bulletin-board/bulletin-board-app
```
2. 之后打开 dockerfile，查看里面的内容
```plain
# 使用官方镜像（node:current-slim）作为父级image，冒号表示标签
FROM node:current-slim
# 设置工作目录，此处目录是你的镜像文件系统，而不是主机文件系统
WORKDIR /usr/src/app
# 将文件从主机拷贝到本地，即拷贝到/usr/src/app/package.json
COPY package.json .
# 运行npm install 安装依赖，所有依赖会打包进 image 文件
RUN npm install
# 暴露端口8080，允许外部连接
EXPOSE 8080
# CMD 指令：执行npm start 启动服务
CMD [ "npm", "start" ]
# 将源码从主机拷贝进你的文件系统中
COPY . .
```
这些步骤和在主机上进行部署安装的步骤大致相同，但是，将他们捕获为 dockerfile 可以是我们在可移植的、独立的 docker 镜像中执行相同的步骤。更多指令参考 [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

#### `RUN`指令与`CMD`指令的区别在哪里
简单说，RUN 命令在 image 文件的构建阶段执行，执行结果都会打包进入 image 文件；CMD 命令则是在容器启动后执行。另外，一个 Dockerfile 可以包含多个 RUN 命令，但是只能有一个 CMD 命令。

### 创建并测试 image
确保工作目录：
```shell
[root@cephnode1 bulletin-board-app]# pwd
```
```plain
/root/node-bulletin-board/bulletin-board-app
```
执行命令
```shell
docker build --tag bulletinboard:1.0 .
```
之后就会去拉取 image
```plain
Sending build context to Docker daemon 45.57 kB
Step 1/7 : FROM node:current-slim
Trying to pull repository docker.io/library/node ... 
current-slim: Pulling from docker.io/library/node
b248fa9f6d2a: Pull complete 
dffc92453adc: Pull complete 
fe328043d349: Pull complete 
4f10197c89ca: Pull complete 
ea536aa94bcb: Pull complete 
Digest: sha256:082cbbeb6144e6bc7757f8f18a3486b52297179332254e6b6053c7c1b1e6ee5a
Status: Downloaded newer image for docker.io/node:current-slim
 ---> b91e80125d03
Step 2/7 : WORKDIR /usr/src/app
 ---> 953dba16ff6c
Removing intermediate container b0ec527a8a85
Step 3/7 : COPY package.json .
 ---> 37223c9f96f0
Removing intermediate container 5210827d4f6a
Step 4/7 : RUN npm install
 ---> Running in b0636bf7b2a0

> ejs@2.7.4 postinstall /usr/src/app/node_modules/ejs
> node ./postinstall.js

Thank you for installing EJS: built with the Jake JavaScript build tool (https://jakejs.com/)

npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN vue-event-bulletin@1.0.0 No repository field.
npm WARN The package morgan is included as both a dev and production dependency.

added 91 packages from 168 contributors and audited 221 packages in 16.522s
found 0 vulnerabilities

 ---> 34a58294222e
Removing intermediate container b0636bf7b2a0
Step 5/7 : EXPOSE 8080
 ---> Running in 3d26cdf56f1e
 ---> 58a0de628db8
Removing intermediate container 3d26cdf56f1e
Step 6/7 : CMD npm start
 ---> Running in 23b066d14e0b
 ---> 08fe8f2ddf74
Removing intermediate container 23b066d14e0b
Step 7/7 : COPY . .
 ---> 6bee22fc7e1d
Removing intermediate container 3368c01c7cbc
Successfully built 6bee22fc7e1d
```
### 查看 images
```shell
[root@cephnode1 bulletin-board-app]# docker images
```
返回结果
```plain
REPOSITORY                                  TAG                 IMAGE ID            CREATED             SIZE
bulletinboard                               1.0                 6bee22fc7e1d        5 minutes ago       181 MB  # 刚才我们创建的镜像
docker.io/ceph/daemon                       latest              dc553e10e530        4 days ago          1.18 GB
docker.io/node                              current-slim        b91e80125d03        4 days ago          165 MB
docker.io/hello-world                       latest              bf756fb1ae65        4 months ago        13.3 kB
docker.io/jolmomar/ansible_runner_service   latest              b27d3f6bf8a6        8 months ago        658 MB

```
### 将你的 image 作为容器运行
1. 基于新生成的 image 启动容器
    ```shell
    docker run --publish 8000:8080 --detach --name bb bulletinboard:1.0
    ```
    上面指令的标识：
    - `--publish` 要求 Docker 将主机端口 8000 上传入的流量转发到容器端口 8080。容器有自己的专用端口集，因此如果要从网络访问某个端口，必须以这种方式将通信量转发给它。否则，以默认的安全组配置，防火墙规则将阻止所有网络流量到达容器。
    - `--detach`要求 Docker 在后台运行此容器。
    - `--name`指定一个名称，在随后的命令中可以使用该名称引用容器，在本例中为`bb`。
    另外，我们没有指定要运行容器的进程。因为在构建 Dockerfile 时使用了 CMD 指令； 因此，Docker 知道在启动时会自动在容器内运行 `npm start` 进程。
    此外，可以使用
    ```shell
    docker container run -p 8000:8080 -it 6bee22fc7e1d # image id
    # or
    docker container run -p 8000:8080 -it bulletinboard:1.0 # image名称和标签
    ```
    会打开一个类似 dev 模式的容器，也可以正常访问。
    ```plain
    > vue-event-bulletin@1.0.0 start /usr/src/app
    > node server.js
    
    Magic happens on port 8080...
    ```
    - `-p` 容器的 8080 映射到本机 8000 端口
    - `it` 容器 shell 映射到本机 shell，之后你在本机窗口输入的指令会传入到容器中
    
2. 通过主机 8000 端口使用浏览器访问应用
 ![](/images/Snipaste_2020-05-11_15-10-44.png)
3. 之后可以使用指令停止容器
    ```shell
    docker stop bb
    ```
    然后再去访问，应用已经停止服务了。当然，你还可以使用`docker rm --force bb`强制删除容器。
    删除容器还可以使用下面的指令：
    1. 查询容器 ID
    ```shell
    docker container ls -all
    # 或者使用 ps 查看全部容器
    docker ps -a
    ```  
    返回结果
    ```plain
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS               NAMES
    d60c45afdc10        bulletinboard:1.0   "docker-entrypoint..."   7 minutes ago       Exited (0) 2 minutes ago                       hopeful_mcclintock
    ```
    2. 删除容器
    ```shell
    docker container rm [containerID]
    ```
    
### 常用指令
- docker container start
`docker container run`命令是新建容器，每运行一次，就会新建一个容器。同样的命令运行两次，就会生成两个一模一样的容器文件。如果希望重复使用容器，就要使用`docker container start`命令，它用来启动已经生成、已经停止运行的容器文件。
```shell
docker container start [containerID]
```
- docker container stop
`docker container kill`命令终止容器运行，相当于向容器里面的主进程发出 SIGKILL 信号。而`docker container stop`命令也是用来终止容器运行，相当于向容器里面的主进程发出 SIGTERM 信号，然后过一段时间再发出 SIGKILL 信号。
```shell
docker container stop [containerID]
```
这两个信号的差别是：应用程序收到 SIGTERM 信号以后，可以自行进行收尾清理工作，但也可以不理会这个信号。如果收到 SIGKILL 信号，就会强行立即终止，那些正在进行中的操作会全部丢失。
- docker container logs
`docker container logs`命令用来查看 docker 容器的输出，即容器里面 Shell 的标准输出。如果`docker run`命令运行容器的时候没有使用`-it`参数，就要用这个命令查看输出。
```shell
$ docker container logs [containerID]
```
- docker container exec
`docker container exec`命令用于进入一个正在运行的 docker 容器。如果`docker run`命令运行容器的时候，没有使用`-it`参数，就要用这个命令进入容器。一旦进入了容器，就可以在容器的 Shell 执行命令了。
```shell
$ docker container exec -it [containerID] /bin/bash
```
- docker container cp
`docker container cp`命令用于从正在运行的 Docker 容器里面，将文件拷贝到本机。下面是拷贝到当前目录的写法。
```bash
$ docker container cp [containID]:[/path/to/file] .
```

## 参考资料
- [Orientation and setup | Docker Documentation](https://docs.docker.com/get-started/)
- [Docker 入门教程 - 阮一峰的网络日志](https://www.ruanyifeng.com/blog/2018/02/docker-tutorial.html)
- [什么是 Docker? - Docker 入门教程 - docker 中文社区](http://www.docker.org.cn/book/docker/what-is-docker-16.html)
- [Docker 教程 | 菜鸟教程](https://www.runoob.com/docker/docker-tutorial.html)
- [Docker 中文文档 Docker 概述-DockerInfo](http://www.dockerinfo.net/document)
- [Docker 学习新手笔记：从入门到放弃 - Joe’s Blog](https://hijiangtao.github.io/2018/04/17/Docker-in-Action/)