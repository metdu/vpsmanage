import requests

class HttpUtil:

    def requestget(self, url,params):
        res = requests.get(url, params)
        return res.text

    def requestpost(self,url,params):
        res = requests.get(url, params)
        return res.text



if __name__ == "__main__":

    url = "http://127.0.0.1:81/hello/add"
    http = HttpUtil()

    params = {'name': 'ccc'}
    res = http.requestget("http://127.0.0.1:81/hello/add",params)
    print (res)


    params = {'name': 'fff'}
    res = http.requestpost(url, params)
    print (res)
