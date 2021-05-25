
# 使用psutil来判断
import psutil
import os
import struct
import binascii
import signal

name = 'TCP_sever'


def verification(name):
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == "python3.exe" and len(p.cmdline()) > 1 and name+'.py' in p.cmdline()[1]:
        #if p.name() == "py.exe" and len(p.cmdline()) > 1 
            return 1
def restartfunction(name):
	if verification(name) == 1:
		print('running')
	else:
		print('restart')
		#os.popen(name+'.py')
		#os.system(name+'.py')
		import TCP_sever
		#with open(name+'.py','r',encoding='utf-8') as f:
		    #exec(f.read())
try:
	restartfunction(name)
except Exception as e:
	raise e







