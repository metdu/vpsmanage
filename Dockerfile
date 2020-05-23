FROM ubuntu:18.04

WORKDIR /var/local
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN apt-get update && \
    apt-get install curl -y && \
    cd / && \
    curl -Ls https://raw.githubusercontent.com/available2099/vpsmanage/master/install.sh > v2-ui.sh

# you can diy it

#  run: docker build -t v2-ui .

#  run: docker run -d  --net=host --privileged --name v2-ui v2-ui  /sbin/init

#  run: docker exec -it v2-ui bash

# run : bash v2-ui.sh