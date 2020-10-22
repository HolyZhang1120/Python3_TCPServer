# 使用psutil来判断
import psutil
import os
import struct
import binascii
import signal

py_path = 'TCP_sever.py'


def verification(name):
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == "py.exe" and len(p.cmdline()) > 1 and name+'.py' in p.cmdline()[1]:
        #if p.name() == "py.exe" and len(p.cmdline()) > 1 
            return 1
def restartfunction(name):
	if verification(name) == 1:
		print('running')
	else:
		print('restart')
		os.popen(py_path)
		#os.system(name+'.py')
		#from TCP import *
		#with open(name+'.py','r',encoding='utf-8') as f:
		    #exec(f.read())
try:
	restartfunction(py_path)
except Exception as e:
	raise e




#os.popen(py_path)




