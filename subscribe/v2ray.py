import json
import base64


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

    def v2link(self):
        json_dict = {
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
            "tls": ""
        }
        json_data = json.dumps(json_dict)
        result_link = "vmess://{}".format(bytes.decode(base64.b64encode(bytes(json_data, 'utf-8'))))
        return result_link

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
            "tls": ""

        }
