# tgcw_zhaobiao

## 天工e招（天工开物电子招投标交易平台）

[地址](http://zhaobiao.tgcw.net.cn/cms/index.htm)

### 业务公告

* [招标公告](http://zhaobiao.tgcw.net.cn/cms/channel/xmgg/index.htm)

* [中标候选人公示](http://zhaobiao.tgcw.net.cn/cms/channel/bidzbgs/index.htm)

* [中标结果公告](http://zhaobiao.tgcw.net.cn/cms/channel/bidzbgg/index.htm)

## Docker 部署

### 构造镜像

```shell
cp /usr/share/zoneinfo/Asia/Shanghai . \
  && docker build -t cg/spider-tgcw-zhaobiao:v1 .
```

### 启动容器

```shell
docker run -d \
  --name spider-tgcw-zhaobiao \
  -e PROXY_POOL_URL=http://192.168.50.6:5010/get/ \
  -e MYSQL_HOSTNAME=192.168.50.6 \
  -v /root/spider/log:/app/log \
  cg/spider-tgcw-zhaobiao:v1
```

### 环境变量

| 变量 | 说明 | 默认值 | 
| --- | --- | --- | 
| `REQUEST_RETRY_TIME` | 请求重试次数 | 3 | 
| `REQUEST_RETRY_INTERVAL` | 请求重试间隔(s) | 3 | 
| `REQUEST_TIMEOUT` | 请求超时(s) | 10 | 
| `NEED_PROXY` | 是否需要IP代理 | `True` | 
| `PROXY_POOL_URL` | 代理IP池url | `http://127.0.0.1:5010/get/` | 
| `INTERVAL_DAYS` | 每次执行爬取数据天数 | 20 | 
| `MYSQL_HOSTNAME` | MySQL数据库连接hostname | `localhost` | 
| `MYSQL_PORT` | MySQL数据库连接port | 3306 | 
| `MYSQL_USERNAME` | MySQL数据库连接username | `root` | 
| `MYSQL_PASSWORD` | MySQL数据库连接password | `123456` | 
| `MYSQL_SCHEMA` | MySQL数据库连接schema | `cg_spider` | 
| `LOG_LEVEL` | 日志级别 | `DEBUG` | 
| `LOG_BACKUP_COUNT` | 日志文件保留数量 | 3 | 
