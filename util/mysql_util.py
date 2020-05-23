from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
from sqlalchemy.ext.declarative import declarative_base
import json

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'student'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    source = Column(String(20))


from sqlalchemy import Column, Integer, String, BIGINT, Boolean



class InboundMysql(Base):
    __tablename__ = 'inbound'
    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, unique=True, nullable=False)
    listen = Column(String(50), default='0.0.0.0')
    protocol = Column(String(50), nullable=False)
    settings = Column(String(500), nullable=False)
    stream_settings = Column(String(500), nullable=False)
    tag = Column(String(255), default='', unique=True, nullable=False)
    sniffing = Column(String(200), default='{"enabled":true,"destOverride":["http","tls"]}')
    remark = Column(String(255), default='', nullable=False)
    up = Column(BIGINT, default=0, nullable=False)
    down = Column(BIGINT, default=0, nullable=False)
    enable = Column(Integer, default=1, nullable=False)


    def __init__(self, port=None, listen=None, protocol=None,
                 settings=None, stream_settings=None, sniffing=None, remark=None):
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
        self.enable = 1

    def to_json(self):
        return {
            'id': self.id,
            'port': self.port,
            'listen': self.listen,
            'protocol': self.protocol,
            'settings': json.loads(self.settings, encoding='utf-8'),
            'stream_settings': json.loads(self.stream_settings, encoding='utf-8'),
            'sniffing': json.loads(self.sniffing, encoding='utf-8'),
            'remark': self.remark,
            'up': self.up,
            'down': self.down,
            'enable': self.enable,
        }

    def to_v2_json(self):
        return {
            'port': self.port,
            'listen': self.listen,
            'protocol': self.protocol,
            'settings': json.loads(self.settings, encoding='utf-8'),
            'streamSettings': json.loads(self.stream_settings, encoding='utf-8'),
            'sniffing': json.loads(self.sniffing, encoding='utf-8'),
            'tag': self.tag,
        }

    def to_v2_str(self):
        return json.dumps(self.to_v2_json(), indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)

# 初始化数据库连接:
def conn_mysql():
    engine = create_engine('mysql+pymysql://lihao:lihao123@149.129.84.249:3306/lihao')
    Base.metadata.create_all(engine)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
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
    conn = pymysql.connect(host="149.129.84.249",user ='lihao',password ='lihao123',db='lihao',charset='utf8',port=3306)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return res