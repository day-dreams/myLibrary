#! coding:utf-8

"""
    异步DNS类
"""

import select
import random
import socket
from DNS import Lib
from DNS import Type
from DNS import Class
from DNS import Opcode


class AsyncRequest(object):
    def __init__(self, sock_recv_buffer_size=1024 * 1024 * 3):
        """
            默认socket的recv buffer为3MiB
        """
        self.sock_recv_buffer_size = sock_recv_buffer_size

        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # 这个选项需要命令支持：sysctl -w net.core.rmem_max=10485760
        self.sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, self.sock_recv_buffer_size)

    def refresh_socket(self):
        """
            使用一个新的socket
        """
        self.sock = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, self.sock_recv_buffer_size)

    def _add_qheader(self, packer, recursive):
        """
            生成DNS请求的头部,并添加到packer中
        """
        tid = random.randint(0, 65535)
        # 操作为查询
        opcode = Opcode.QUERY
        # 期望递归
        if recursive:
            rd = 1
        else:
            rd = 0
        packer.addHeader(tid, 0, opcode, 0, 0, rd, 0, 0, 0, 1, 0, 0, 0)

    def send(self, server, qname, qtype=Type.A, recursive=True, qclass=Class.IN, port=53):
        """
            发送请求数据包，不返回任何响应
        """
        packer = Lib.Mpacker()
        self._add_qheader(packer, recursive)
        packer.addQuestion(qname, qtype, qclass)
        request_data = packer.getbuf()
        self.sock.sendto(request_data, (server, port))

    def recv(self, timeout=3):
        """
            返回一个生成器，用于迭代socket在timeout内接受到的响应包
        """
        while True:
            rsocket, wsocket, errsocket = select.select(
                [self.sock], [], [], timeout)
            if len(rsocket) == 0:
                return
            (response_buffer, address) = self.sock.recvfrom(65535)
            u = Lib.Munpacker(response_buffer)
            r = Lib.DnsResult(u, {})
            yield (r, address[0])


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

    sender = AsyncRequest()

    ips = ['202.102.154.3']

    for i in range(1, 100):
        a, b = 0, 0

        for _ in range(i * 100):
            for ip in ips:
                sender.send(ip, "www.hitwh.edu.cn")
                a += 1

        for data in sender.recv():
            b += 1

            res = data[0]
            ip = data[1]
            # print res.header, ip
            # print res.answers
            # print res.authority
            # print res.additional

        sender.refresh_socket()

        print "send:%d,recv:%d,pkt_loss_rate:%f" % (a, b, 1 - float(b) / a)


if __name__ == "__main__":
    test()
