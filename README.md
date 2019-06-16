执行main.py ,每10秒中请求网站的接口并返回数据到redis的channel中
proxy_ip.py是另一个进程，用于产生并校验ip代理，供main.py 所用。
两个是独立的进程。
已经分别打成docker镜像