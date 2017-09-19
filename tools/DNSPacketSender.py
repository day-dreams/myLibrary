#! coding:utf-8

"""
    DNS发包机，不处理相应包
"""

from DNS import Lib
from DNS import Type
from DNS import Class
from DNS import Opcode
import random
import socket


def send_dns_packets(ip, qname, num):
    """
        单纯DNS发包,没有回调函数
    """
    tid = random.randint(0, 65535)
    # 端口为53,UDP
    port = 53
    # 操作为查询
    opcode = Opcode.QUERY
    # Tpye类型为A
    qtype = Type.A
    # 查询类，一般为IN
    qclass = Class.IN
    # 期望递归
    rd = 1
    # 建立一个UDP套接字（SOCK_DGRAM，代表UDP，AF_INET表示IPv4）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_port = random.randint(1024, 65535)
    # socket绑定到指定IP地址和接口上
    s.bind(('', source_port))
    for _ in range(0, num):
        server = ip
        m = Lib.Mpacker()
        m.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)
        m.addQuestion(qname, qtype, qclass)
        request = m.getbuf()
        try:
            s.sendto(request, (server, port))
        except socket.error, reason:
            pass
