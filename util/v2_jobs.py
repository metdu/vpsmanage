import threading

from init import db, mysqlsesson
from util import config, v2_util
from util.schedule_util import schedule_job
from v2ray.models import Inbound
from util.mysql_util import Inbound as InboundMysql, VpsNode, FailedNodeJob
from util.v2_util import get_ip
import requests
from util import server_info
from apscheduler.schedulers.background import BackgroundScheduler

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
        # with __lock:
        v2_config = v2_util.gen_v2_config_from_db()
        v2_util.write_v2_config(v2_config)
        __v2_config_changed = False


def traffic_job():
    print("进入流量统计")
    # with __lock:
    # if not v2_util.is_running():
    #    return
    traffics = v2_util.get_inbounds_traffic()
    if not traffics:
        print("没查到流量")
        return
    for traffic in traffics:
        upload = int(traffic.get('uplink', 0))
        download = int(traffic.get('downlink', 0))
        print("down:" + str(download) + ":up:" + str(upload))
        tag = traffic['tag']
        local_ip = get_ip()
        inbound = Inbound.query.filter_by(tag=tag).first()
        if inbound and download < inbound.down:
            Inbound.query.filter_by(tag=tag).update({'up': Inbound.up + upload, 'down': Inbound.down + download})
        else:
            Inbound.query.filter_by(tag=tag).update({'up': upload, 'down': download})
        # 更新mysql
        inbounding = mysqlsesson.query(InboundMysql).filter(InboundMysql.tag == tag).first()
        if inbounding and download < inbounding.down:
            mysqlsesson.query(InboundMysql).filter(InboundMysql.tag == tag, InboundMysql.server == local_ip).update(
                {InboundMysql.up: InboundMysql.up + upload, InboundMysql.down: InboundMysql.down + download},
                synchronize_session=False)
            mysqlsesson.query(VpsNode).filter(VpsNode.tag == tag, VpsNode.server == local_ip).update(
                {VpsNode.up: VpsNode.up + upload, VpsNode.down: VpsNode.down + download},
                synchronize_session=False)

        else:
            mysqlsesson.query(InboundMysql).filter(InboundMysql.tag == tag, InboundMysql.server == local_ip).update(
                {InboundMysql.up: upload, InboundMysql.down: download},
                synchronize_session=False)
            mysqlsesson.query(VpsNode).filter(VpsNode.tag == tag, VpsNode.server == local_ip).update(
                {VpsNode.up: upload, VpsNode.down: download},
                synchronize_session=False)

    db.session.commit()
    mysqlsesson.commit()


# 创建节点任务
def create_node_job():
    print("进入创建节点")
    # if not v2_util.is_running():
    #    return
    failedNodeJobs = mysqlsesson.query(FailedNodeJob).filter(FailedNodeJob.count < 20, FailedNodeJob.status == 1)
    if not failedNodeJobs:
        return
    for nodejob in failedNodeJobs:
        try:
            requests.post(nodejob.server, nodejob.json, timeout=13)
        except:
            print("Failed http")
            mysqlsesson.query(FailedNodeJob).filter(FailedNodeJob.id == nodejob.id).update(
                {FailedNodeJob.count: nodejob.count + 1})
        else:
            mysqlsesson.query(FailedNodeJob).filter(FailedNodeJob.id == nodejob.id).update(
                {FailedNodeJob.count: nodejob.count + 1, FailedNodeJob.status: 0})
    mysqlsesson.commit()


# 单节点流量统计订阅总流量任务
def check_traffic_job():
    print("进入节点流量统计:")
    # if not v2_util.is_running():
    #   return
    local_ip = get_ip()
    vpsNode = mysqlsesson.query(VpsNode).filter(VpsNode.server == local_ip)
    for node in vpsNode:
        if node.ip + node.down >= node.alllink:
            mysqlsesson.query(VpsNode).filter(VpsNode.tag == node.tag, VpsNode.server == local_ip).update(
                {VpsNode.status: 0, VpsNode.is_subscribe: 0})
            Inbound.query.filter_by(tag=node.tag).update({'enable': False})
    db.session.commit()
    mysqlsesson.commit()


def dojob():
    # 创建调度器：BlockingScheduler
    scheduler = BackgroundScheduler()
    # 添加任务,时间间隔2S
    scheduler.add_job(check_v2_config_job, 'interval', seconds=10, id='test_job1')
    # 添加任务,时间间隔5S
    scheduler.add_job(traffic_job, 'interval', seconds=20, id='test_job2')
    # 添加任务,时间间隔2S
    scheduler.add_job(create_node_job, 'interval', seconds=100, id='test_job3')
    # 添加任务,时间间隔5S
    scheduler.add_job(check_traffic_job, 'interval', seconds=200, id='test_job4')
    # 添加任务,时间间隔5S
    scheduler.add_job(server_info.refresh_status, 'interval', seconds=2, id='test_job5')
    scheduler.start()


def init():
    dojob()
    # schedule_job(check_v2_config_job, config.get_v2_config_check_interval())
    # schedule_job(traffic_job, config.get_traffic_job_interval())
    # schedule_job(create_node_job, 300)
    # schedule_job(check_traffic_job, 300)
