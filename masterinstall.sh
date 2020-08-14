#!/usr/bin/env bash

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

cur_dir=$(pwd)

# check root
[[ $EUID -ne 0 ]] && echo -e "${red}错误：${plain} 必须使用root用户运行此脚本！\n" && exit 1

# check os
if [[ -f /etc/redhat-release ]]; then
    release="centos"
elif cat /etc/issue | grep -Eqi "debian"; then
    release="debian"
elif cat /etc/issue | grep -Eqi "ubuntu"; then
    release="ubuntu"
elif cat /etc/issue | grep -Eqi "centos|red hat|redhat"; then
    release="centos"
elif cat /proc/version | grep -Eqi "debian"; then
    release="debian"
elif cat /proc/version | grep -Eqi "ubuntu"; then
    release="ubuntu"
elif cat /proc/version | grep -Eqi "centos|red hat|redhat"; then
    release="centos"
else
    echo -e "${red}未检测到系统版本，请联系脚本作者！${plain}\n" && exit 1
fi

if [ $(getconf WORD_BIT) != '32' ] && [ $(getconf LONG_BIT) != '64' ] ; then
    echo "本软件不支持 32 位系统(x86)，请使用 64 位系统(x86_64)，如果检测有误，请联系作者"
    exit -1
fi

os_version=""

# os version
if [[ -f /etc/os-release ]]; then
    os_version=$(awk -F'[= ."]' '/VERSION_ID/{print $3}' /etc/os-release)
fi
if [[ -z "$os_version" && -f /etc/lsb-release ]]; then
    os_version=$(awk -F'[= ."]+' '/DISTRIB_RELEASE/{print $2}' /etc/lsb-release)
fi

if [[ x"${release}" == x"centos" ]]; then

    if [[ ${os_version} -le 6 ]]; then
        echo -e "${red}请使用 CentOS 7 或更高版本的系统！${plain}\n" && exit 1
    fi
elif [[ x"${release}" == x"ubuntu" ]]; then
    if [[ ${os_version} -lt 16 ]]; then
        echo -e "${red}请使用 Ubuntu 16 或更高版本的系统！${plain}\n" && exit 1
    fi
elif [[ x"${release}" == x"debian" ]]; then

    if [[ ${os_version} -lt 8 ]]; then
        echo -e "${red}请使用 Debian 8 或更高版本的系统！${plain}\n" && exit 1
    fi
fi
install_python(){
  yum -y install wget zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel epel-release gcc
    wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz
    tar zxvf Python-3.7.5.tgz
    cd Python-3.7.5
    ./configure --with-ssl
    make && make install
    cd ..
    yum -y install python3-pip

    # 删除软链接，建立新的软连接
    rm -rf /usr/bin/pip3
    rm -rf /usr/bin/python3
    ln -s /usr/local/bin/python3.7 /usr/bin/python3
    ln -s /usr/local/bin/pip3.7 /usr/bin/pip3
    #其他版本： https://www.python.org/downloads/source/

     apt  install -y wget zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel epel-release gcc
    wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz
    tar zxvf Python-3.7.5.tgz
    cd Python-3.7.5
    ./configure --with-ssl
    make && make install
    cd ..
    apt  install -y python3-pip

    # 删除软链接，建立新的软连接
    rm -rf /usr/bin/pip3
    rm -rf /usr/bin/python3
    ln -s /usr/local/bin/python3.7 /usr/bin/python3
    ln -s /usr/local/bin/pip3.7 /usr/bin/pip3
}


install_base() {
    if [[ x"${release}" == x"centos" ]]; then
        yum install wget curl tar unzip -y
    else
        apt install wget curl tar unzip -y
    fi
}

install_v2ray() {
    echo -e "${green}开始安装or升级v2ray${plain}"
    bash <(curl -L -s https://install.direct/go.sh)
    if [[ $? -ne 0 ]]; then
        echo -e "${red}v2ray安装或升级失败，请检查错误信息${plain}"
        echo -e "${yellow}大多数原因可能是因为你当前服务器所在的地区无法下载 v2ray 安装包导致的，这在国内的机器上较常见，解决方式是手动安装 v2ray，具体原因还是请看上面的错误信息${plain}"
        exit 1
    fi
    systemctl enable v2ray
    systemctl start v2ray
#    service  v2ray start
}

close_firewall() {
    if [[ x"${release}" == x"centos" ]]; then
        systemctl stop firewalld
        systemctl disable firewalld
    elif [[ x"${release}" == x"ubuntu" ]]; then
        ufw disable
    elif [[ x"${release}" == x"debian" ]]; then
        iptables -P INPUT ACCEPT
        iptables -P OUTPUT ACCEPT
        iptables -P FORWARD ACCEPT
        iptables -F
    fi
}
docker_install()
{
	echo "检查Docker......"
	docker -v
    if [ $? -eq  0 ]; then
        echo "检查到Docker已安装!"
    else
    	echo "安装docker环境..."
         apt-get update\
          && apt-get -y install vim curl sudo inotify-tools\
          && curl -fsSL https://get.docker.com/ | sh || apt-get -y install docker.io
        echo "安装docker环境...安装完成!"
    fi
    # 创建公用网络==bridge模式
    #docker network create share_network
}
install_docker(){
docker_install
  cd /var/local
  mkdir v2master
  cd v2master
  git init
  git pull  https://github.com/available2099/vpsmanage.git
  git remote add upstream https://github.com/available2099/vpsmanage.git
  git fetch upstream
  chmod -R 777 /var/local/v2master
  #删除容器
  docker rm -f $(docker ps -a | grep v2-ui | awk '{print $1}')
#删除镜像
  docker rmi v2-ui
  #打包镜像
  docker build -t v2-ui .
  #启动容器
  docker run -d --net=host -v /etc/v2ray:/etc/v2ray  --restart=always  --name v2-ui v2-ui
   cp -f inotifyconf.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable inotifyconf
    systemctl start inotifyconf
    echo -e "${green}v2master 安装完成，面板已启动，"
    echo -e "如果是全新安装，默认网页端口为 ${green}8085${plain}，用户名和密码默认都是 ${green}admin${plain}"
    echo -e "请自行确保此端口没有被其他程序占用，${yellow}并且确保 8085 端口已放行${plain}"
}

install_master(){
  if [[ x"${release}" == x"centos" ]]; then
       #systemctl stop startv2m
		python_version=$(python3 --version| awk -F " " '{print $NF}'| awk -F "." '{print $NF}')
        if [ $python_version -gt 2 ];then
          echo "已安装Python3"
          yum install -y  vim python3-pip git
          pip3 install --upgrade pip
          pip install flask tornado
          cd /var/local
          mkdir v2master
          cd v2master
          git init
          git pull  https://github.com/available2099/vpsmanage.git
          git remote add upstream https://github.com/available2099/vpsmanage.git
          git fetch upstream
          pip install --no-cache-dir -r requirements.txt
          chmod +x /var/local/v2master/startv2m.sh
          cp -f startv2m.service /etc/systemd/system/
          systemctl daemon-reload
          systemctl enable startv2m
          systemctl start startv2m
          echo -e "${green}v2master 安装完成，面板已启动，"
          echo -e "如果是全新安装，默认网页端口为 ${green}8085${plain}，用户名和密码默认都是 ${green}admin${plain}"
          echo -e "请自行确保此端口没有被其他程序占用，${yellow}并且确保 8085 端口已放行${plain}"
          echo -e "若想将 8085 修改为其它端口，输入 v2-ui 命令进行修改，同样也要确保你修改的端口也是放行的"
        fi
elif [[ x"${release}" == x"ubuntu" ]]; then
    #systemctl stop startv2m
    python_version=$(python3 --version| awk -F " " '{print $NF}'| awk -F "." '{print $NF}')
    if [ $python_version -gt 2 ];then
      echo "已安装Python3"
      apt-get update -y
      apt-get install -y  vim python3-pip git
      pip3 install --upgrade pip
      pip install flask tornado
      cd /var/local
      mkdir v2master
      cd v2master
      git init
      git pull  https://github.com/available2099/vpsmanage.git
      git remote add upstream https://github.com/available2099/vpsmanage.git
      git fetch upstream
      pip install --no-cache-dir -r requirements.txt
      chmod +x /var/local/v2master/startv2m.sh
      cp -f startv2m.service /etc/systemd/system/
        systemctl daemon-reload
        systemctl enable startv2m
        systemctl start startv2m
        echo -e "${green}v2master 安装完成，面板已启动，"
        echo -e "如果是全新安装，默认网页端口为 ${green}8085${plain}，用户名和密码默认都是 ${green}admin${plain}"
        echo -e "请自行确保此端口没有被其他程序占用，${yellow}并且确保 8085 端口已放行${plain}"
        echo -e "若想将 8085 修改为其它端口，输入 v2-ui 命令进行修改，同样也要确保你修改的端口也是放行的"
    fi
elif [[ x"${release}" == x"debian" ]]; then
  #systemctl stop startv2m
  python_version=$(python3 --version| awk -F " " '{print $NF}'| awk -F "." '{print $NF}')
  if [ $python_version -gt 2 ];then
    echo "已安装Python3"
    apt-get update -y
    apt-get install -y  vim python3-pip git
    pip3 install --upgrade pip
    pip install flask tornado
    cd /var/local
    mkdir v2master
    cd v2master
    git init
    git pull  https://github.com/available2099/vpsmanage.git
    git remote add upstream https://github.com/available2099/vpsmanage.git
    git fetch upstream
    pip install --no-cache-dir -r requirements.txt
    chmod +x /var/local/v2master/startv2m.sh
    cp -f startv2m.service /etc/systemd/system/
      systemctl daemon-reload
      systemctl enable startv2m
      systemctl start startv2m
      echo -e "${green}v2master 安装完成，面板已启动，"
      echo -e "如果是全新安装，默认网页端口为 ${green}8085${plain}，用户名和密码默认都是 ${green}admin${plain}"
      echo -e "请自行确保此端口没有被其他程序占用，${yellow}并且确保 8085 端口已放行${plain}"
      echo -e "若想将 8085 修改为其它端口，输入 v2-ui 命令进行修改，同样也要确保你修改的端口也是放行的"
   fi
fi
}

echo -e "${green}开始安装${plain}"
install_base
install_v2ray
#install_docker
install_master
close_firewall
#install_v2-uidocker
#install_v2-ui
