FROM python:3.6-alpine

MAINTAINER yshawcom <yshawcom@163.com>

RUN mkdir /usr/share/zoneinfo \
    && mkdir /usr/share/zoneinfo/Asia \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone

COPY Shanghai /usr/share/zoneinfo/Asia

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENTRYPOINT [ "sh", "start.sh" ]
