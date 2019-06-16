FROM python:3.6
MAINTAINER yyqq188@foxmail.com
RUN pip install --upgrade pip && pip install requests && pip install redis
COPY ./config.py /config.py
COPY ./main.py /main.py
COPY ./proxy_ip.py /proxy_ip.py
#CMD python /main.py
CMD python /proxy_ip.py