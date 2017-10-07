# 常用代码收集库

这里是我的一些常用代码,有些是脚本,有些是复用性很强的工具代码.

目前:

|code|purpose|details|
|-|-|-|
|[GetLineFromABC.py](tools/GetLineFromABC.py)|求文件差集|对文件大小有一定限制|
|[produce-consume-model](./produce-consume-model/ThreadEntry.py)|多线程入库|不支持多重生产-消费模型|
|[GetDomainNS.py](tools/GetDomainNS.py)|获取域名的名字服务器的ip|使用[阿里dns](http://www.alidns.com/),不保证速率;注意不要造成DDOS攻击|
|[calculate.sh](shell-scripts/calculate.sh)|shell脚本中的计算工具|依赖awk|
|[Logger.py](./Logging/Logger.py)|日志类|不依赖标准库logging,线程安全,固定日志格式,可添加handler|
|[AsyncDns.py](tools/AsyncDns.py)|异步的DNS请求类|需要提供qnameGenerator,responseCallback;可以将充分发挥带宽|

todo:
  - [ ] 添加语言和依赖库说明
