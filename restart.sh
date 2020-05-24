#!/bin/bash
#首先删掉文件,替换文件,然后运行命令
#运行指令 sh ./restart.sh
# AUTHOR  demo

#删除容器
docker rm -f $(docker ps -a | grep v2-ui | awk '{print $1}')
#删除镜像
docker rmi v2-ui
#打包镜像
docker build -t v2-ui .
#启动容器
docker run -d  --net=host  --name v2-ui v2-ui  /sbin/init
#docker run -d --net=host --privileged --name v2-ui v2-ui /sbin/init
#进入容器
docker exec -it v2-ui bash
