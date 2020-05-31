class V2ray:
    def __init__(self, ps=None, add=None,
                 port=None, id=None, aid=None, net=None, path=None):
        self.v = '2'
        self.ps = ps
        self.add = add
        self.port = port
        self.id = id
        self.aid = aid
        self.net = net
        self.type = 'none'
        self.host = ''
        self.path = path
        self.tls = 'none'

    def to_json(self):
        return {
                "v": "2",
                "ps": self.ps,
                "add": self.add,
                "port": self.port,
                "id": self.id,
                "aid": self.aid,
                "net": self.net,
                "type": "none",
                "host": "",
                "path": self.path,
                "tls": "none"

        }
