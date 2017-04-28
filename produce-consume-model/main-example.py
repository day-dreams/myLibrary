#!coding:utf-8

"""
    模型使用实例
"""

import time
import ThreadEntry

def produce(num):
    while True:
        time.sleep(num)
        print "---"

def consume(num):
    while True:
        time.sleep(num)
        print "***"

def main():
    p=lambda :produce(1)
    c=lambda :consume(2)
    model=ThreadEntry.ProduceConsumerModel(p,c)
    model.prepare()
    model.run()

if __name__=="__main__":
    main()
