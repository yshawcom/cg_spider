FROM python:3.6-alpine

MAINTAINER yshawcom <yshawcom@163.com>

ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime &&\
    echo $TZ > /etc/timezone

WORKDIR /app

COPY . .

# runtime environment
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENTRYPOINT [ "sh", "start.sh" ]
