import flask
from flask import Blueprint
from base.models import User
from subscribe.v2ray import V2ray
from util.mysql_util import UserSubscribe, SsNode
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
        NodeList = mysqlsesson.query(SsNode).filter(SsNode.v2_port == User.user_port).all()
        for node in NodeList:
            v2 = V2ray(node.desc, node.server,
                       node.v2_port, node.v2_id, node.v2_alter_id, node.v2_net, node.v2_path)
            shuchu = shuchu + "vmess://" + (base64.b64encode(json.dumps(v2.to_json()).encode('utf-8')).decode('ascii')) + '\n'

    encodestr = base64.b64encode(shuchu.encode('utf-8')).decode('ascii')
    print(str(encodestr, 'utf-8'))
    return str(encodestr, 'utf-8')


@sub_se.route('/quantumultx/<setting_id>', methods=['GET', 'POST'])
def subscribeqx(setting_id):
    shuchu = ''
    Userfirst = mysqlsesson.query(UserSubscribe).filter(UserSubscribe.code == setting_id).first()
    if not Userfirst:
        return '{code":200,"msg":"不存在该订阅}'
    else:
        NodeList = mysqlsesson.query(SsNode).filter(SsNode.v2_port == Userfirst.user_port).all()
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