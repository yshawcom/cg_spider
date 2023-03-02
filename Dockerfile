FROM python:3.6-alpine

MAINTAINER yshawcom <yshawcom@163.com>

# apk repository, timezone
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update  \
    && apk add -U tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY . .

# runtime environment
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "sh", "start.sh" ]
