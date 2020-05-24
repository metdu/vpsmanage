FROM ubuntu:18.04
#FROM python:3.7
WORKDIR /var/local
COPY requirements.txt ./
RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask tornado
#RUN pip install flask gunicorn gevent

RUN apt-get install -y locales
RUN locale-gen zh_CN
RUN locale-gen zh_CN.utf8
RUN update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 LANGUAGE=zh_CN.UTF-8

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8
COPY . .
RUN apt-get install curl -y && \
    cd / && \
    curl -Ls https://raw.githubusercontent.com/available2099/vpsmanage/master/install.sh > v2-ui.sh
CMD ["/sbin/init && python3  v2-ui.py" ]
#CMD gunicorn -w 4 u2-ui:u2-ui

# you can diy it

#  run: docker build -t v2-ui .

#  run: docker run -d  --net=host --privileged --name v2-ui v2-ui  /sbin/init

#  run: docker exec -it v2-ui bash

# run : bash v2-ui.sh