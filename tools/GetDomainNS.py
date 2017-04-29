#! coding:utf-8

"""
    获取域名的名字服务器的ip(s)
"""

import DNS
import sys

def get_domain_ip(domain,cache={}):
    """
        内部设置缓存
    """
    if domain in cache.keys():
        return cache[domain]
    else:
        req=DNS.Request(domain,qtype=DNS.Type.A,server='223.6.6.6',timeout=5)
        res=req.req()
        ips=[]
        for rr in res.answers:
            ips.append(rr['data'])
        cache[domain]=ips
        return ips

def get_ns_ips(domain):
    req=DNS.Request(domain,qtype=DNS.Type.NS,server='223.6.6.6',timeout=5)
    response=req.req()
    ips=[]
    for ns in response.answers:
        temp=get_domain_ip(ns['data'])
        for item in temp:
            ips.append(item)
    return ips

if __name__=="__main__":
    for domain in sys.argv[1:]:
        try:
            print domain,get_ns_ips(domain)
        except Exception,e:
            raise
