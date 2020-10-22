import struct
import os
import binascii
from crc32 import crc2hex 

def ReadFile(i,j,filepath): #i:第几包，j：每包的字节数
    binfile = open(filepath, 'rb') #打开二进制文件
    size = ReadFileSize(filepath) #获得文件大小
    print(size)
    if size/j%1 :
        size1 = int(size/j)+1
    else: size1 = int(size/j)
    if i == (size1-1):
        size2 = size-(j*i)
    else: size2 = j
    
    print(size2)
    binfile.seek(j*i,0)
    data = binfile.read(j) #每次输出j个字节
    data = str(binascii.b2a_hex(data))[2:-1]
    msg = b'\xAA\xAC' #获取结构化事件戳
    msg = str(binascii.b2a_hex(msg))[2:-1]
    msg1 = struct.pack('B',i).hex()         #包数
    msg2 = struct.pack('>i',size2).hex()    #数据大小
    #print(msg2)
    data = '%s%s%s%s' % (msg,msg1,msg2,data)
    data1 = crc2hex(data)   #crc32校验和
    data = '%s%s' % (data,data1)
    #print(data)
    binfile.close()
    del i,j
    return data
def ReadFileSize(filepath):
    size = os.path.getsize(filepath) #获得文件大小
    return size


    