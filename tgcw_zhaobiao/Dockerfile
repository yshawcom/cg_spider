FROM python:3.8-alpine

MAINTAINER yshawcom <yshawcom@163.com>

WORKDIR /app

COPY spider .

# runtime environment
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENTRYPOINT [ "sh", "start.sh" ]
