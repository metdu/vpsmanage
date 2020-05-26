# coding: utf-8
from sqlalchemy import CHAR, Column, Date, DateTime, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FqUrl(Base):
    __tablename__ = 'fq_url'

    id = Column(BIGINT(20), primary_key=True)
    describe = Column(String(50), nullable=False, server_default=text("''"), comment='vps_名字')
    url_status = Column(String(10), nullable=False, server_default=text("''"), comment='用户付费状态')
    url = Column(String(4000), nullable=False, server_default=text("''"), comment='链接')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class FqUser(Base):
    __tablename__ = 'fq_users'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(20), nullable=False, server_default=text("''"), comment='名字')
    user_wx = Column(String(100), nullable=False, server_default=text("''"), comment='用户微信')
    user_type = Column(String(10), nullable=False, server_default=text("''"), comment='用户付费类型')
    user_status = Column(String(10), nullable=False, server_default=text("''"), comment='用户付费状态')
    user_url = Column(String(200), nullable=False, server_default=text("''"), comment='用户短连接base64')
    user_price = Column(String(10), nullable=False, server_default=text("''"), comment='用户价格')
    fq_text = Column(Text)
    yjl_user = Column(String(100))
    yjl_pwd = Column(String(100))
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class Inbound(Base):
    __tablename__ = 'inbound'

    id = Column(INTEGER(11), primary_key=True)
    port = Column(INTEGER(11), nullable=False, unique=True)
    listen = Column(String(50))
    protocol = Column(String(50), nullable=False)
    settings = Column(String(500), nullable=False)
    stream_settings = Column(String(500), nullable=False)
    tag = Column(String(255), nullable=False, unique=True)
    sniffing = Column(String(200))
    remark = Column(String(255), nullable=False)
    up = Column(BIGINT(20), nullable=False)
    down = Column(BIGINT(20), nullable=False)
    enable = Column(INTEGER(11), nullable=False)


class SsNode(Base):
    __tablename__ = 'ss_node'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    type = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='服务类型：1-SS、2-V2ray')
    name = Column(String(128), nullable=False, server_default=text("''"), comment='名称')
    group_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='所属分组')
    country_code = Column(CHAR(5), nullable=False, server_default=text("'un'"), comment='国家代码')
    server = Column(String(128), server_default=text("''"), comment='服务器域名地址')
    desc = Column(String(255), server_default=text("''"), comment='节点简单描述')
    is_subscribe = Column(TINYINT(4), server_default=text("'1'"), comment='是否允许用户订阅该节点：0-否、1-是')
    sort = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序值，值越大越靠前显示')
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-维护、1-正常')
    up = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已上传流量，单位字节')
    down = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已下载流量，单位字节')
    v2_alter_id = Column(INTEGER(11), nullable=False, server_default=text("'16'"), comment='V2ray额外ID')
    v2_port = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='V2ray端口')
    v2_method = Column(String(32), nullable=False, server_default=text("'aes-128-gcm'"), comment='V2ray加密方式')
    v2_net = Column(String(16), nullable=False, server_default=text("'tcp'"), comment='V2ray传输协议')
    v2_type = Column(String(32), nullable=False, server_default=text("'none'"), comment='V2ray伪装类型')
    v2_host = Column(String(255), nullable=False, server_default=text("''"), comment='V2ray伪装的域名')
    v2_path = Column(String(255), nullable=False, server_default=text("''"), comment='V2ray WS/H2路径')
    v2_tls = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='V2ray底层传输安全 0 未开启 1 开启')
    v2_insider_port = Column(INTEGER(11), nullable=False, server_default=text("'10550'"), comment='V2ray内部端口（内部监听），v2_port为0时有效')
    v2_outsider_port = Column(INTEGER(11), nullable=False, server_default=text("'443'"), comment='V2ray外部端口（外部覆盖），v2_port为0时有效')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class UserSubscribe(Base):
    __tablename__ = 'user_subscribe'
    __table_args__ = (
        Index('user_id', 'user_id', 'status'),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='用户ID')
    username = Column(String(128, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"), comment='用户名')
    password = Column(String(64, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"), comment='密码')
    code = Column(CHAR(5), index=True, server_default=text("''"), comment='订阅地址唯一识别码')
    transfer_enable = Column(BIGINT(20), nullable=False, server_default=text("'1099511627776'"), comment='可用流量，单位字节，默认1TiB')
    up = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已上传流量，单位字节')
    down = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='已下载流量，单位字节')
    times = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='地址请求次数')
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-禁用、1-启用')
    ban_desc = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"), comment='封禁理由')
    wechat = Column(String(30, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='微信')
    qq = Column(String(20, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='QQ')
    usage = Column(String(10, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'4'"), comment='用途：1-手机、2-电脑、3-路由器、4-其他')
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


class VpsDevice(Base):
    __tablename__ = 'vps_device'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='设备名称')
    level = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='类型：0,1,2,3,4普通到VIP4')
    country_code = Column(CHAR(5, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'un'"), comment='国家代码')
    server = Column(String(128, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='服务器域名地址')
    ip = Column(CHAR(15, 'utf8mb4_unicode_ci'), server_default=text("''"), comment='服务器IPV4地址')
    status = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='状态：0-不可用、1-可用')
