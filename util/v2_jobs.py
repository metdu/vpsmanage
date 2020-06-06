import threading

from init import db, mysqlsesson
from util import config, v2_util
from util.schedule_util import schedule_job
from v2ray.models import Inbound
from util.mysql_util import Inbound as InboundMysql

__lock = threading.Lock()
__v2_config_changed = True


def v2_config_change(func):
    def inner(*args, **kwargs):
        global __v2_config_changed
        result = func(*args, **kwargs)
        __v2_config_changed = True
        return result

    inner.__name__ = func.__name__
    return inner


def check_v2_config_job():
    global __v2_config_changed
    if __v2_config_changed:
        with __lock:
            v2_config = v2_util.gen_v2_config_from_db()
            v2_util.write_v2_config(v2_config)
            __v2_config_changed = False


def traffic_job():
    with __lock:
        if not v2_util.is_running():
            return
        traffics = v2_util.get_inbounds_traffic()
        if not traffics:
            return
        for traffic in traffics:
            upload = int(traffic.get('uplink', 0))
            download = int(traffic.get('downlink', 0))
            tag = traffic['tag']
            inbound = Inbound.query.filter_by(tag=tag)
            print("upload:"+upload)
            print("upload:"+download)
            print("uploadquery:"+inbound['down'])
            if inbound and download < inbound['down']:
                Inbound.query.filter_by(tag=tag).update({'up': Inbound.up + upload, 'down': Inbound.down + download})
            else:
                Inbound.query.filter_by(tag=tag).update({'up': upload, 'down': download})
            # 更新mysql
            inbounding = mysqlsesson.query(InboundMysql).filter(InboundMysql.tag == tag)
            print("mqquery:"+inbounding['down'])
            if inbounding and download < inbounding['down']:
                mysqlsesson.query(InboundMysql).filter(InboundMysql.tag == tag).update(
                    {InboundMysql.up: InboundMysql.up + upload, InboundMysql.down: InboundMysql.down + download},
                    synchronize_session=False)
            else:
                mysqlsesson.query(InboundMysql).filter(InboundMysql.tag == tag).update(
                    {InboundMysql.up: upload, InboundMysql.down: download})
        db.session.commit()
        mysqlsesson.commit()


def init():
    schedule_job(check_v2_config_job, config.get_v2_config_check_interval())
    schedule_job(traffic_job, config.get_traffic_job_interval())
