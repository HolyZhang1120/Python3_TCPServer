
import binascii
import zlib
#https://www.cnblogs.com/kerndev/p/5537379.html
#https://stackoverflow.com/questions/5557214/crc32-checksum-in-python-with-hex-input
def crc32asii(v):
    return '0x%8x' % (binascii.crc32(v) & 0xffffffff)
 
 
def crc2hex(crc): 
    return '%08x' % (binascii.crc32(binascii.a2b_hex(crc)) & 0xffffffff) 
 
 
#s='11'
#b = bytes(s, encoding='utf-8')
#print(crc32asii(b))
 
#1234567890的16进制为499602D2
#d='3131'
#print(crc2hex(d))

def crc32hex1(k):
    """
    计算文件 crc32 hash 值
    """
    hash = 0
    hash = zlib.crc32(k, hash)
    return "%08X" % (hash & 0xFFFFFFFF)


def crc32(file_path):
    """
    计算文件 crc32 hash 值
    """
    with open(file_path, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65535)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

#msg2 = crc32('pic/20201016221608.jpg')
#print("服务端返回的内容:%s" % (msg2)) 
 