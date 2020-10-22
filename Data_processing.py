#!/usr/bin/python3
# -*-coding:utf-8 -*-

import binascii
import time
import struct
from file import ReadFile
from file import ReadFileSize
from crc32 import crc2hex 
from crc32 import crc32 
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import os

Send_num = 5*1024
Flag = 1

def ini_data(i,data_loc,data,size): #i=1,读，i=0,写;data_loc:文件指针位置；data：数据；size:读文件字节
    save_path = 'Storage.ini'
    with open(save_path,"rb+") as f:
        f.seek(data_loc,0)
        if i == 0:
            data = binascii.a2b_hex(data)
            f.write(data) # img_bin里面保存着 以二进制方式读取的图片内容,当前目录会生成一张img.jpg的图片
        elif i == 1:
            return f.read(size)

def upgrade_function(data,size,BUFSIZ):
  msg = '00'
  if (data[2] == 'a') & (data[3] == 'b') :    #0xAB  请求升级
     Send_num1 = str(data)[4:6]   #保留
     Send_num1 = int(Send_num1,16)  #保留
     crc11 = str(data)[6:int(size)]
     data1 = str(data)[0:6]
     data1 = crc2hex(data1)
     if data1 == crc11 :   #下发升级包大小
        if Flag == 1:
            msg1 = b'\xAA\xAB'
        else: msg1 = b'\xAA\xAD' #获取结构化事件戳
        msg1 = str(binascii.b2a_hex(msg1))[2:-1]
        msg2 = ReadFileSize(BUFSIZ)
        #print(msg2)
        msg2 = struct.pack('>i',msg2).hex()    #数据大小
        msg3 = crc32(BUFSIZ)
        msg2 = '%s%s%s' % (msg1,msg2,msg3)
        msg4 = crc2hex(msg2)   #crc32校验和
        msg = '%s%s' % (msg2,msg4)
         #else:print("服务端返回的内容:%s" % (data_i)) 
      #else:print("服务端返回的内容:%s" % (data_i)) 
  elif (data[2] == 'a') & (data[3] == 'c') :    #0xAC 请求包号
      data_i = str(data)[4:6]
      data_i = int(data_i,16)
      crc11 = str(data)[6:int(size)]
      data1 = str(data)[0:6]
      data1 = crc2hex(data1)
      print("服务端返回的内容:%s" % (data1)) 
      print("服务端返回的内容:%s" % (crc11)) 
      if data1 == crc11:   #下发升级包大小
          print("服务端返回的内容:%s" % (data_i)) 
          msg = ReadFile(data_i-1,Send_num,BUFSIZ)
  else:msg = '00'
  return msg
def picture_function(data,size,BUFSIZ):
  msg = '00'
  if (data[2] == 'a') & (data[3] == 'b') :    #0xAB  请求升级
     pic_size = str(data)[4:12]
     pic_size1 = int(pic_size,16)
     crc11 = str(data)[12:int(size)]
     data1 = str(data)[0:12]
     data1 = crc2hex(data1)
     if data1 == crc11 :   #下发升级包大小
        msg1 = b'\xBB\xAB'
        ini_flag = b'\xF6\x00'
        ini_flag = str(binascii.b2a_hex(ini_flag))[2:-1]
        msg1 = str(binascii.b2a_hex(msg1))[2:-1]
        msg2 = BUFSIZ
        msg2 = struct.pack('>i',msg2).hex()    #数据大小
        msg2 = '%s%s' % (msg1,msg2)
        msg3 = crc2hex(msg2)   #crc32校验和
        msg = '%s%s' % (msg2,msg3)
        name = time.strftime("%Y%m%d%H%M%S") #获取结构化事件戳
        ini_data(0,0,ini_flag,0) #存储图片
        ini_data(0,2,pic_size,0) #存储图片大小
        ini_data(0,6,name,0) #存储图片名称
        print("1")
        print(pic_size1)
  elif (data[2] == 'a') & (data[3] == 'c') :    #0xAC 请求包号
      print("22")
      ini_flag1 = ini_data(1,0,0,1)
      ini_flag1 = str(binascii.b2a_hex(ini_flag1))[2:-1]
      if ini_flag1 == 'f6':
          data_pack = str(data)[4:6]
          #data_pack1 = int(data_pack,16)
          crc11 = str(data)[(int(size)-8):int(size)]
          data1 = str(data)[0:(int(size)-8)]
          data1 = crc2hex(data1)
          print("1")
          print(data1)
          print(crc11)
          if data1 == crc11:   #下发升级包大小
              pic_pack = ini_data(1,1,0,1)
              pic_pack = str(binascii.b2a_hex(pic_pack))[2:-1]
              print(pic_pack)
              print(data_pack)
              if pic_pack == data_pack:

                  print("2")
                  msg1 = b'\xBB\xAC'
                  msg1 = str(binascii.b2a_hex(msg1))[2:-1]
                  msg2 = data_pack
                  #msg2 = struct.pack('B',msg2).hex()
                  msg2 = '%s%s' % (msg1,msg2)
                  msg3 = crc2hex(msg2)   #crc32校验和
                  msg = '%s%s' % (msg2,msg3)
                  pic_pack1 = int(pic_pack,16)+1
                  print(pic_pack1-1)
                  pic_pack1 = "%0.2x" % (pic_pack1)
                  #pic_pack1 = str.encode(hex(pic_pack1))
                  #pic_pack1=pic_pack1.HexstrToBytes(1,'little')
                  #pic_pack1 = str(pic_pack1)[4:-1]
                  ini_data(0,1,pic_pack1,0) #存储图片
                  pic_data = str(data)[14:(int(size)-8)]
                  pic_data = binascii.a2b_hex(pic_data)
                  name =  ini_data(1,6,0,7)
                  name = str(binascii.b2a_hex(name))[2:-1]
                  name_path = 'pic/'+name+'.jpg'
                  with open(name_path,"ab") as f:
                    f.write(pic_data) # img_bin里面保存着 以二进制方式读取的图片内容,当前目录会生成一张img.jpg的图片 
                    print("3")
  elif (data[2] == 'a') & (data[3] == 'd') :    #0xAC 请求包号
      pic_crc_client = str(data)[4:12]
      print("pic_crc_client:%s" % (pic_crc_client))
      crc11 = str(data)[12:int(size)]
      data1 = str(data)[0:12]
      data1 = crc2hex(data1)
      if data1 == crc11:   #下发升级包大小
          name =  ini_data(1,6,0,7)
          name = str(binascii.b2a_hex(name))[2:-1]
          name_path = 'pic/'+name+'.jpg'
          #name_path = 'pic/20201017114938.jpg'
          pic_crc = crc32(name_path)
          pic_crc = pic_crc.lower() #大写转换成小写
          pic_size = ini_data(1,2,0,4)
          pic_size = str(binascii.b2a_hex(pic_size))[2:-1]
          pic_size = int(pic_size,16)
          pic_size_read = os.path.getsize(name_path) #获得文件大小
          print("pic_crc_client:%s" % (pic_crc))
          print("pic_crc_client:%s" % (pic_size))
          print("pic_crc_client:%s" % (pic_size_read))
          if (pic_crc == pic_crc_client) and (pic_size == pic_size_read):
              msg1 = b'\xBB\xAD\xAA'
              msg1 = str(binascii.b2a_hex(msg1))[2:-1]
              msg2 = crc2hex(msg1)   #crc32校验和
              msg = '%s%s' % (msg1,msg2)
              ini_flag = b'\xFF\x00'
              ini_flag = str(binascii.b2a_hex(ini_flag))[2:-1]
              ini_data(0,0,ini_flag,0) #完成图片存储
              print("3")
              #lena = mpimg.imread(name_path) # 读取和代码处于同一目录下的 lena.png
              # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
              #lena.shape #(512, 512, 3)

              #plt.imshow(lena) # 显示图片
              #plt.axis('off') # 不显示坐标轴
              #plt.show()
  return msg
