import requests
import telnetlib
import json
import redis
from config import settings
proxy_url = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
pool = redis.ConnectionPool(host=settings['host'], port=settings['port'])
r = redis.Redis(connection_pool=pool)


def verify(ip, port, type_,country):
    proxies = {}
    try:
        telnetlib.Telnet(ip, port, timeout=5)
    except:
        print("unconnection")
    else:
        print("connected successful")
        proxies['host'] = ip
        proxies['port'] = port
        proxies['type'] = type_
        proxies['country'] = country
        proxies_json = json.dumps(proxies)
        r.lpush('proxy_ip', str(proxies_json))


def getProxy(proxy_url):
    response = requests.get(proxy_url)
    proxies_list = response.text.splitlines()
    lens = len(proxies_list)
    for i in range(lens):
        proxy_str = proxies_list[i]
        proxy_json = json.loads(proxy_str)
        host = proxy_json['host']
        port = proxy_json['port']
        type_ = proxy_json['type']
        country = proxy_json['country']
        verify(host, port, type_,country)
        if i == lens - 1:
            getProxy(proxy_url)


if __name__ == "__main__":
    getProxy(proxy_url)
