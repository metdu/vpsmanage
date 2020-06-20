from sqlalchemy.orm import sessionmaker
from sqlalchemy import CHAR, Column, Date, DateTime, Index, String, TIMESTAMP, Text, text, create_engine
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER, TINYINT,LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import time

# 创建对象的基类:
Base = declarative_base()

class FailedNodeJob(Base):
    __tablename__ = 'failed_node_jobs'
    __table_args__ = {'comment': '失败任务'}

    id = Column(BIGINT(20), primary_key=True)
    create_ip = Column(String(128, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='创建任务ip')
    destnation_ip = Column(String(128, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='需要执行任务服务器域名地址')
    server = Column(String(128, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='请求服务器域名地址')
    json = Column(String(1000), nullable=False)
    count = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='job执行次数')
    failed_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-删除、1-待执行')
    def __init__(self, create_ip=None, destnation_ip=None, server=None, json=None):
        self.server = server
        self.create_ip = create_ip
        self.destnation_ip = destnation_ip
        self.server = server
        self.json = json
        self.count = 0
        self.failed_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.status = 1

class Inbound(Base):
    __tablename__ = 'inbound'

    id = Column(INTEGER(11), primary_key=True)
    server = Column(String(128), server_default=text("''"), comment='服务器域名地址')
    port = Column(INTEGER(11), nullable=False)
    listen = Column(String(50))
    protocol = Column(String(50), nullable=False)
    settings = Column(String(500), nullable=False)
    stream_settings = Column(String(500), nullable=False)
    tag = Column(String(255), nullable=False)
    sniffing = Column(String(200))
    remark = Column(String(255), nullable=False)
    up = Column(BIGINT(20), nullable=False)
    down = Column(BIGINT(20), nullable=False)
    enable = Column(INTEGER(11), nullable=False)

    def __init__(self, server=None, port=None, listen=None, protocol=None,
                 settings=None, stream_settings=None, sniffing=None, remark=None):
        self.server = server
        self.port = port
        self.listen = listen
        self.protocol = protocol
        self.settings = settings
        self.stream_settings = stream_settings
        self.tag = 'inbound-%d' % self.port
        self.sniffing = sniffing
        self.remark = remark
        self.up = 0
        self.down = 0
        self.enable = True


class VpsNode(Base):
    __tablename__ = 'vps_node'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    type = Column(String(8), nullable=False, server_default=text("'V2ray'"), comment='服务类型：SS、V2ray')
    name = Column(String(128), nullable=False, server_default=text("''"), comment='名称')
    group_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='所属分组')
    country_code = Column(CHAR(5), nullable=False, server_default=text("'un'"), comment='国家代码')
    server = Column(String(128), server_default=text("''"), comment='服务器域名地址')
    tag = Column(String(255), nullable=False, server_default=text("''"), comment='端口tag')
    is_subscribe = Column(TINYINT(4), server_default=text("'1'"), comment='是否允许用户订阅该节点：0-否、1-是')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序值，值越大越靠前显示')
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-维护、1-正常')
    up = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已上传流量，单位字节')
    down = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已下载流量，单位字节')
    alllink = Column(BIGINT(20), nullable=False, server_default=text("'107374182400'"), comment='总流量，单位字节')
    desc = Column(String(255), server_default=text("''"), comment='节点简单描述')
    v2_id = Column(String(255), nullable=False, server_default=text("''"), comment='V2ray id密码')
    v2_alter_id = Column(INTEGER(11), nullable=False, server_default=text("'16'"), comment='V2ray额外ID')
    v2_port = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='V2ray端口')
    v2_method = Column(String(32), nullable=False, server_default=text("'aes-128-gcm'"), comment='V2ray加密方式')
    v2_net = Column(String(16), nullable=False, server_default=text("'tcp'"), comment='V2ray传输协议')
    v2_type = Column(String(32), nullable=False, server_default=text("'none'"), comment='V2ray伪装类型')
    v2_host = Column(String(255), nullable=False, server_default=text("''"), comment='V2ray伪装的域名')
    v2_path = Column(String(255), nullable=False, server_default=text("''"), comment='V2ray WS/H2路径')
    v2_tls = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='V2ray底层传输安全 0 未开启 1 开启')
    v2_insider_port = Column(INTEGER(11), nullable=False, server_default=text("'10550'"),
                             comment='V2ray内部端口（内部监听），v2_port为0时有效')
    v2_outsider_port = Column(INTEGER(11), nullable=False, server_default=text("'443'"),
                              comment='V2ray外部端口（外部覆盖），v2_port为0时有效')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, type=None, server=None, v2_id=None, v2_alter_id=None,
                 v2_port=None, v2_path=None, desc=None, v2_net=None):
        self.type = type
        self.server = server
        self.v2_id = v2_id
        self.v2_alter_id = v2_alter_id
        self.v2_port = v2_port
        self.v2_method = 'auto'
        self.v2_host = server
        self.desc = desc
        self.v2_path = v2_path
        self.v2_net = v2_net
        self.tag = 'inbound-%d' % self.v2_port
        self.created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class UserSubscribe(Base):
    __tablename__ = 'user_subscribe'
    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    username = Column(String(128, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"), comment='用户名')
    password = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"), comment='密码')
    code = Column(String(200), nullable=False, server_default=text("''"), comment='订阅地址唯一识别码')
    user_port = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户使用的V2ray端口')
    fq_text = Column(Text)
    transfer_enable = Column(BIGINT(20), nullable=False, server_default=text("'1099511627776'"),
                             comment='可用流量，单位字节，默认1TiB')
    up = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已上传流量，单位字节')
    down = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已下载流量，单位字节')
    alllink = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='总流量，单位字节')
    times = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='地址请求次数')
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-禁用、1-启用')
    ban_desc = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"), comment='封禁理由')
    wechat = Column(String(30, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='微信')
    qq = Column(String(20, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='QQ')
    usage = Column(String(10, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'4'"),
                   comment='用途：1-手机、2-电脑、3-路由器、4-其他')
    pay_way = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='付费方式：0-免费、1-季付、2-月付、3-半年付、4-年付')
    balance = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='余额，单位分')
    enable_time = Column(Date, comment='开通日期')
    expire_time = Column(Date, nullable=False, server_default=text("'2099-01-01'"), comment='过期时间')
    remark = Column(Text(collation='utf8mb4_unicode_ci'), comment='备注')
    level = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='等级：可定义名称')
    is_admin = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='是否管理员：0-否、1-是')
    traffic_reset_day = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='流量自动重置日，0表示不重置')
    created_at = Column(DateTime, comment='创建时间')
    updated_at = Column(DateTime, comment='最后更新时间')

    def __init__(self, code=None, user_port=None, level=None, is_admin=None):
        self.code = code
        self.user_port = user_port
        self.level = level
        self.is_admin = is_admin
        self.created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.updated_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class VpsDevice(Base):
    __tablename__ = 'vps_device'
    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='设备名称')
    level = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='类型：0,1,2,3,4普通到VIP4')
    country_code = Column(CHAR(5), nullable=False, server_default=text("'un'"), comment='国家代码')
    server = Column(String(128, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='服务器域名地址')
    ip = Column(CHAR(15), server_default=text("''"), comment='服务器IPV4地址')
    alllink = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='总流量，单位字节')
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-不可用、1-可用')

    def __init__(self, name=None, level=None, country_code=None, server=None, alllink=None):
        self.name = name
        self.level = level
        self.country_code = country_code
        self.server = server
        self.alllink = alllink


# 初始化数据库连接:
def conn_mysql():
    #engine = create_engine('mysql+pymysql://root:nihao123@67.230.168.201:4306/demo')
    engine = create_engine('mysql+pymysql://lihao:lihao123@149.129.84.249:3306/lihao')
    Base.metadata.create_all(engine)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


'''
user = session.query(User).filter(User.id=='6').one()
# 打印类型和对象的name属性:
print('type:', type(user))
print('name:', user.name)
print('name:', user.source)
# 关闭Session:
session.close()
'''


def con_mysql(sql):
    import pymysql
    conn = pymysql.connect(host="67.230.168.201", user='root', password='nihao123', db='demo', charset='utf8',
                           port=4306)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return res
