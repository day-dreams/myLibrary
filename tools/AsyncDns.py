#! coding:utf-8

"""
    DNS发包机，不处理相应包
"""

import select
import random
import socket
from DNS import Lib
from DNS import Type
from DNS import Class
from DNS import Opcode


class QheaderGenerateHandle:
    """
        生成qheader的工具类,需指定qypte,recursive;默认qclass为IN
    """

    def __init__(self,  recursive=True):
        self.recursive = recursive

    def add_qheader(self, packer):
        """
            生成DNS请求的头部,并添加到packer中
        """
        tid = random.randint(0, 65535)
        # 操作为查询
        opcode = Opcode.QUERY
        # 期望递归
        if self.recursive:
            rd = 1
        else:
            rd = 0
        packer.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)


class AsyncDnsSender:
    """
        异步发包机器
    """

    def __init__(self, qname_generator_handle, response_handle, qtype=Type.A, recursive=True):
        """
            qname_generator_handle: 根据ip生成qname并返回
            qtype:查询类型
            recursive:是否要求递归
            response_handle:处理响应包的回调函数
        """
        self.generate_qname_callback = qname_generator_handle
        self.response_callback = response_handle
        self.qtype = qtype
        self.qclass = Class.IN
        self.port = 53
        self.generate_qheader_callback = QheaderGenerateHandle(recursive)
        pass

    def async_send(self, ips):
        """
            异步发送请求.
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        source_port = random.randint(1024, 65535)

        for ip in ips:
            m = Lib.Mpacker()
            self.generate_qheader_callback.add_qheader(m)
            qname = self.generate_qname_callback(ip)
            m.addQuestion(qname, self.qtype, self.qclass)
            request = m.getbuf()

            try:
                self.socket.sendto(request, (ip, self.port))
            except socket.error, reason:
                pass

    def async_recv(self):
        """
            接受所有响应包,并调用回调函数
        """
        s = self.socket
        while True:
            rsocket, wsocket, errsocket = select.select([s], [], [], 1)
            if len(rsocket) == 0:
                break
            (response_buffer, address) = s.recvfrom(65535)
            u = Lib.Munpacker(response_buffer)
            r = Lib.DnsResult(u, {})
            self.response_callback(r)


def test():
    """
        AsyncSender使用示例
    """
    def responseCallback(response):
        print ""
        print response.header
        print response.answers
        print response.authority
        print response.additional

    def qnameGenerator(ip):
        return "baidu.com"

    sender = AsyncDnsSender(qnameGenerator, responseCallback)

    _ips = ['1.2.4.8', '8.8.8.8', '114.114.114.114', '223.6.6.6', '223.5.5.5']
    ips = []
    for _ in range(1000):
        ips += _ips

    sender.async_send(ips)
    sender.async_recv()


if __name__ == "__main__":
    test()
