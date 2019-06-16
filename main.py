import redis
import requests
import time
import datetime
import json
from config import settings
class Process():
    def __init__(self):
        self.pool = redis.ConnectionPool(host=settings["host"],port=settings["port"])
        self.r = redis.Redis(connection_pool=self.pool)

    def _get_timestamp(self):
        last_208_time = datetime.datetime.now() - datetime.timedelta(hours=208)
        return str(int(time.mktime(last_208_time.timetuple())))

    def _get_HistoryTop5(self,history_top5_domain_url,proxy_ip):

        history_data = requests.post(history_top5_domain_url+"?" + "jsonPost=1&t="+self._get_timestamp(),proxies=proxy_ip)
        return history_data.text
    def _get_lmcl_data(self,lmcl_domain_url,proxy_ip):
        lmcl_data = requests.post(lmcl_domain_url + "?" + "jsonPost=1&t=" + self._get_timestamp(),proxies = proxy_ip)
        return lmcl_data.text

    def insert(self,channel_name,data):
        self.r.publish(channel_name,message=data)


    def get_proxy_ip(self):
        proxy_data = self.r.rpop("proxy_ip")
        if proxy_data:
            proxy_ip_data = json.loads(proxy_data)
            type = proxy_ip_data['type']
            host = proxy_ip_data['host']
            port = proxy_ip_data['port']
            # country = proxy_ip_data['country']
            # print(country)
            # if "CN" in country and country:
            if "https" not in type:
                return {type:type+"://"+host+":"+str(port)}
            else:
                self.get_proxy_ip()
            # else:
            #     self.get_proxy_ip()

if __name__ == "__main__":
    channel_name = "loti"
    history_top5_domain_url = "https://www.xpj338888.com/NewLottery2/HistoryTop5/幸运飞艇"
    lmcl_domain_url = "https://www.xpj338888.com/NewLottery2/lmcl/幸运飞艇"
    #
    p = Process()




    while True:
        proxy_ip = p.get_proxy_ip()
        if proxy_ip:
            num = 1
            while True:

                time.sleep(5)
                print(proxy_ip)
                # print(type(proxy_ip))
                history_data = p._get_HistoryTop5(history_top5_domain_url,proxy_ip)
                print(history_data)
                p.insert(channel_name, history_data)
                time.sleep(5)
                lmcl_data = p._get_lmcl_data(lmcl_domain_url,proxy_ip)
                print(lmcl_data)
                p.insert(channel_name, lmcl_data)
                num += 1

                if num == 4:
                    break


