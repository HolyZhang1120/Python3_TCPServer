#!/usr/bin/python3
# -*-coding:utf-8 -*-

import socket#获取计算机名称

def getIP():
    hostname=socket.gethostname()#获取本机IP
    IP=socket.gethostbyname(hostname)
    return IP
print (getIP())
