#!/usr/bin/python3
# coding:utf-8
from socket import *
from Data_processing import *
import binascii
import time
import struct
from GetIP import getIP
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from crc32 import crc2hex 
from crc32 import crc32 
import os

COD = 'utf-8'
HOST = '192.168.2.100' # 主机ip
PORT = 25052 # 软件端口号
BUFSIZ = 1024*2
BUFSIZ1 = BUFSIZ*3
SIZE =10
filepath='RTCNew.bin'
ADDR = (HOST, PORT)
print (ADDR)
tcpS = socket(AF_INET, SOCK_STREAM) # 创建socket对象
tcpS.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #加入socket配置，重用ip和端口
tcpS.bind(ADDR) # 绑定ip端口号
tcpS.listen(SIZE)  # 设置最大链接数
while True:
    print("服务器启动，监听客户端链接")
    conn, addr = tcpS.accept() 
    conn.settimeout(10)
    print("链接的客户端", addr)

    while True:
        try:
            #ata= conn.recv(BUFSIZ1)
            had_received = 0     
            data = bytes() 
            flag = 0 
            while had_received < BUFSIZ1:
                part_body= conn.recv(BUFSIZ1 - had_received)
                data111 = str(binascii.b2a_hex(part_body))[2:-1]
                if (data111[0] == 'b') & (data111[1] == 'b') & (data111[2] == 'a') & (data111[3] == 'c') :
                    data_pack_size = str(data111)[6:14]
                    data_pack_size = int(data_pack_size,16)
                    flag = 1
                    #print('flag', flag)
                if flag == 1:
                    data +=  part_body
                    part_body_length = len(part_body)
                    #print('part_body_length', part_body_length)
                    had_received += part_body_length
                    if had_received >= data_pack_size:
                        break
                elif flag == 0 : 
                    data  =  part_body
                    break
        except Exception:
            print("断开的客户端", addr)
            break
        if not data:
            break

        data = str(binascii.b2a_hex(data))[2:-1]
        size = len(data)


        print("客户端发送的内容:%s" % (data))
        global msg_data
        msg_data = '00'
        print("11")
        #print("客户端发送的内容:%s" % (data))
        try:
            if (data[0] == 'a') & (data[1] == 'a') :    #0xAA
                msg_data = upgrade_function(data,size,filepath)                                            
            if (data[0] == 'b') & (data[1] == 'b') :    #0xAB
                msg_data = picture_function(data,size,BUFSIZ) 
            
        except Exception as e:
            print('the Exception is:',e)
            break
        data_hui = '\r\n'

        conn.send(bytes.fromhex(msg_data)) #发送消息给已链接客户端
        conn.send(data_hui.encode(COD)) #发送消息给已链接客户端
        print("服务端返回的内容:%s" % (msg_data)) 
    conn.close() #关闭客户端链接
tcpS.closel()




