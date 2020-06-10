import json

from flask import Blueprint, render_template, jsonify, request
from flask_babel import gettext
from sqlalchemy import and_

from base.models import Msg
from init import db
from util import config, server_info
from util.v2_jobs import v2_config_change
from v2ray.models import Inbound
# from v2ray.modelsmysql import InboundMysql
from init import mysqlsesson
from util.mysql_util import Inbound as InboundMysql, VpsNode, UserSubscribe, VpsDevice
from util.v2_util import random_email, get_ip
import base64
import requests

v2ray_bp = Blueprint('v2ray', __name__, url_prefix='/v2ray')

__check_interval = config.get_v2_config_check_interval()


@v2ray_bp.route('/', methods=['GET'])
def index():
    from init import common_context
    status = json.dumps(server_info.get_status(), ensure_ascii=False)
    return render_template('v2ray/index.html', **common_context, status=status)


@v2ray_bp.route('/accounts/', methods=['GET'])
def accounts():
    from init import common_context
    inbs = Inbound.query.all()
    inbs = '[' + ','.join([json.dumps(inb.to_json(), ensure_ascii=False) for inb in inbs]) + ']'
    return render_template('v2ray/accounts.html', **common_context, inbounds=inbs)


@v2ray_bp.route('/clients/', methods=['GET'])
def clients():
    from init import common_context
    return render_template('v2ray/clients.html', **common_context)


@v2ray_bp.route('/setting/', methods=['GET'])
def setting():
    from init import common_context
    settings = config.all_settings()
    settings = '[' + ','.join([json.dumps(s.to_json(), ensure_ascii=False) for s in settings]) + ']'
    return render_template('v2ray/setting.html', **common_context, settings=settings)


@v2ray_bp.route('/tutorial/', methods=['GET'])
def tutorial():
    from init import common_context
    return render_template('v2ray/tutorial.html', **common_context)


@v2ray_bp.route('/donate/', methods=['GET'])
def donate():
    from init import common_context
    return render_template('v2ray/donate.html', **common_context)


@v2ray_bp.route('/inbounds', methods=['GET'])
def inbounds():
    return jsonify([inb.to_json() for inb in Inbound.query.all()])


@v2ray_bp.route('inbound/add', methods=['POST'])
@v2_config_change
def add_inbound():
    port = int(request.form['port'])
    print("进来了")
    if Inbound.query.filter_by(port=port).count() > 0:
        return jsonify(Msg(False, gettext('port exists')))
    listen = request.form['listen']
    protocol = request.form['protocol']
    settings = request.form['settings']
    email = random_email()
    remail = '"email":"' + email + '",'
    str_list = list(settings)
    str_list.insert(13, remail)  # 插入堆积
    newsettings = ''.join(str_list)
    stream_settings = request.form['stream_settings']
    sniffing = request.form['sniffing']
    remark = request.form['remark']
    # 当前用户等级
    user_level = request.form['level']
    # 是否更新所有服务器
    allvps = request.form['allvps']
    inbound = Inbound(port, listen, protocol, newsettings, stream_settings, sniffing, remark, user_level)
    db.session.add(inbound)
    db.session.commit()
    local_ip = get_ip()
    if allvps == 'true':
        print("更新所有vps")
        devices = mysqlsesson.query(VpsDevice).filter(VpsDevice.level <= int(user_level), VpsDevice.status == 1).all()
        inbound.allvps = 'false'
        for device in devices:
            if local_ip != device.ip:
                requests.post("http://" + device.ip + ":65432/v2ray/inbound/add", inbound.to_json_vps(), timeout=13)
                # requests.post("http://127.0.0.1:5000/v2ray/inbound/add", inbound.to_json_vps(), timeout=3)
        # 插入mysql 用户表,生成订阅
        userSubscribe = UserSubscribe(base64.b64encode(email.encode('utf-8')), port, user_level, 1)
        mysqlsesson.add(userSubscribe)

    # 插入mysql inbound
    inboundMysql = InboundMysql(local_ip, port, listen, protocol, newsettings, stream_settings, sniffing, remark)
    mysqlsesson.add(inboundMysql)
    # 插入mysql 节点表
    Node = VpsNode(protocol, local_ip, json.loads(settings)['clients'][0]['id'],
                   json.loads(settings)['clients'][0]['alterId'], port,
                   json.loads(stream_settings)['wsSettings']['path'], remark, json.loads(stream_settings)['network'])
    mysqlsesson.add(Node)
    mysqlsesson.commit()
    return jsonify(
        Msg(True,
            gettext(u'Successfully added, will take effect within %(seconds)d seconds', seconds=__check_interval)
            )
    )


@v2ray_bp.route('inbound/update/<int:in_id>', methods=['POST'])
@v2_config_change
def update_inbound(in_id):
    update = {}
    port = request.form.get('port')
    add_if_not_none(update, 'port', port)
    if port:
        if Inbound.query.filter(Inbound.port == port).count() > 1:
            return jsonify(Msg(False, gettext('port exists')))
        add_if_not_none(update, 'tag', 'inbound-' + port)
    add_if_not_none(update, 'listen', request.form.get('listen'))
    add_if_not_none(update, 'protocol', request.form.get('protocol'))
    add_if_not_none(update, 'settings', request.form.get('settings'))
    add_if_not_none(update, 'stream_settings', request.form.get('stream_settings'))
    add_if_not_none(update, 'sniffing', request.form.get('sniffing'))
    add_if_not_none(update, 'remark', request.form.get('remark'))
    add_if_not_none(update, 'enable', request.form.get('enable') == 'true')
    add_if_not_none(update, 'level', request.form.get('level'))

    listen = request.form['listen']
    protocol = request.form['protocol']
    settings = request.form['settings']
    email = random_email()
    remail = '"email":"' + email + '",'
    str_list = list(settings)
    str_list.insert(13, remail)  # 插入堆积
    newsettings = ''.join(str_list)
    stream_settings = request.form['stream_settings']
    sniffing = request.form['sniffing']
    remark = request.form['remark']
    # 当前用户等级
    user_level = request.form['level']
    # 是否更新所有服务器
    allvps = request.form['allvps']
    local_ip = get_ip()
    if allvps == "true":
        inbound = Inbound(int(port), listen, protocol, newsettings, stream_settings, sniffing, remark, user_level)
        inbound.allvps = 'false'
        devices = mysqlsesson.query(VpsDevice).filter(VpsDevice.level <= int(user_level), VpsDevice.status == 1).all()
        for device in devices:
            if local_ip != device.ip:
                requests.post("http://" + device.ip + ":65432/v2ray/inbound/update/" + str(in_id), inbound.to_json_vps(),
                              timeout=3)
                # requests.post("http://127.0.0.1:5000/v2ray/inbound/add", inbound.to_json_vps(), timeout=3)
    print("vps更新")
    Inbound.query.filter_by(port=in_id).update(update)
    db.session.commit()
    return jsonify(
        Msg(True,
            gettext(u'Successfully updated, will take effect within %(seconds)d seconds', seconds=__check_interval)
            )
    )


@v2ray_bp.route('inbound/del/<int:in_id>', methods=['POST'])
@v2_config_change
def del_inbound(in_id):
    Inbound.query.filter_by(id=in_id).delete()
    db.session.commit()
    return jsonify(
        Msg(True,
            gettext(u'Successfully deleted, will take effect within %(seconds)d seconds', seconds=__check_interval)
            )
    )


@v2ray_bp.route('reset_traffic/<int:in_id>', methods=['POST'])
def reset_traffic(in_id):
    Inbound.query.filter_by(id=in_id).update({'up': 0, 'down': 0})
    db.session.commit()
    return jsonify(Msg(True, gettext('Reset traffic successfully')))


@v2ray_bp.route('reset_all_traffic', methods=['POST'])
def reset_all_traffic():
    Inbound.query.update({'up': 0, 'down': 0})
    db.session.commit()
    return jsonify(Msg(True, gettext('Reset add traffic successfully')))


def add_if_not_none(d, key, value):
    if value is not None:
        d[key] = value
