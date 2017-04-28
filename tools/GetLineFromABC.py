# -*- coding: latin-1 -*-
#
#   运行： python GetLineFromABC.py  Ａ B ... Z
#
#   功能：从文件Z中选出文件A、文件B中没有的行，并输出到stdout
#
#   使用场景：文件Ｚ比较大，而ＡＢ等都是小文件
#

import sys

if len(sys.argv)<3:
    print "invalid arguments!"

dictionary={}
for index in range(1,len(sys.argv)-1):
    for line in open(sys.argv[index],'r'):
        #print "-",line[0:line.find('+')]
        #print "-",line
        dictionary[line[0:line.find('+')]]=0

for line in open(sys.argv[-1],'r'):
    #print line.strip()
    if line.strip() not in dictionary:
        print line.strip()+"+no"
    else:
        #print line
        pass
