import flask
from flask import Blueprint
from base.models import User
from subscribe.v2ray import V2ray
from util.mysql_util import UserSubscribe, VpsNode
from init import mysqlsesson
import base64
import json

sub_se = Blueprint('', __name__)


@sub_se.route('/netlify/<setting_id>', methods=['GET', 'POST'])
def subscribe(setting_id):
    shuchu = ''
    User = mysqlsesson.query(UserSubscribe).filter(UserSubscribe.code == setting_id).first()
    if not User:
        return '{code":200,"msg":"不存在该订阅}'
    else:
        expire_time = V2ray("nextTime:"+str(User.expire_time), "8.8.8.8",
                       9999,"b5a811d6-c13e-4000-9204-0c45b47e586a", "22","ws", "").v2link()
        genery = mysqlsesson.query(UserSubscribe).filter(UserSubscribe.code == 'ZGVtbwxx').first()

        NodeList = mysqlsesson.query(VpsNode).filter(VpsNode.v2_port == User.user_port).all()
        for node in NodeList:
            v2 = V2ray(node.desc, node.server,
                       node.v2_port, node.v2_id, node.v2_alter_id, node.v2_net, node.v2_path).v2link()
            shuchu = shuchu +v2 + '\n'
        shuchu = shuchu + genery.fq_text + '\n'
    encodestr = base64.b64encode(shuchu.encode('utf-8'))
    print(encodestr)
    return encodestr


@sub_se.route('/quantumultx/<setting_id>', methods=['GET', 'POST'])
def subscribeqx(setting_id):
    shuchu = ''
    Userfirst = mysqlsesson.query(UserSubscribe).filter(UserSubscribe.code == setting_id).first()
    if not Userfirst:
        return '{code":200,"msg":"不存在该订阅}'
    else:
        expire_time =  V2ray("nextTime:"+str(Userfirst.expire_time), "8.8.8.8",
                       9999,"b5a811d6-c13e-4000-9204-0c45b47e586a", "22","ws", "")
        openurl = "vmess=" + expire_time.add + ":" + str(expire_time.port) + ", method=chacha20-ietf-poly1305, password=" \
                  + expire_time.id + ", obfs=" + expire_time.net + ", obfs-uri=" + expire_time.path \
                  + ",fast-open=false, udp-relay=false, tag=" + expire_time.ps
        shuchu = shuchu + openurl + "\n"
        NodeList = mysqlsesson.query(VpsNode).filter(VpsNode.v2_port == Userfirst.user_port).all()
        for node in NodeList:
            v2 = V2ray(node.desc, node.server,
                       node.v2_port, node.v2_id, node.v2_alter_id, node.v2_net, node.v2_path)
            openurl = "vmess=" + v2.add + ":" + str(v2.port) + ", method=chacha20-ietf-poly1305, password=" \
                      + v2.id + ", obfs=" + v2.net + ", obfs-uri=" + v2.path \
                      + ",fast-open=false, udp-relay=false, tag=" + v2.ps
            shuchu = shuchu + openurl + "\n"
    encodestr = base64.b64encode(shuchu.encode('utf-8'))
    print(str(encodestr, 'utf-8'))
    return str(encodestr, 'utf-8')
@sub_se.route('/commitlogs/log', methods=['GET', 'POST'])
def getcommitlogs():
    file_object = open('/var/local/gitlog', "rt")
    # 不要把open放在try中，以防止打开失败，那么就不用关闭了
    try:
        file_context = file_object.read().splitlines()
        # file_context是一个string，读取完后，就失去了对test.txt的文件引用
        #  file_context = open(file).read().splitlines()
        # file_context是一个list，每行文本内容是list中的一个元素
    finally:
        file_object.close()
    # 除了以上方法，也可用with、contextlib都可以打开文件，且自动关闭文件，
    # 以防止打开的文件对象未关闭而占用内存
    logs = ""
    for tx in file_context:
        logs = logs + tx + "\n"
    return logs

@sub_se.route('/<setting_id>', methods=['GET', 'POST'])
def subscriberoot(setting_id):
    Usertest = mysqlsesson.query(UserSubscribe).filter(UserSubscribe.code == setting_id).first()
    shuchu = ''
    if not Usertest:
        return '{code":200,"msg":"订阅不存在}'
    else:
        shuchu = Usertest.fq_text
    encodestr = base64.b64encode(shuchu.encode('utf-8'))
    print(str(encodestr, 'utf-8'))
    return str(encodestr, 'utf-8')
