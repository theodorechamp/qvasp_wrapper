import subprocess
import time
import sys

LowFolder = 2
UpperFolder = 9
Increment = 1
Material = sys.argv[1]

Folder = LowFolder

while Folder <= UpperFolder:
	print('qvasp_kpts_mail 4 24 5 ' + Material + 'KPTStudy'+str(Folder)+'.log, cwd=./'+str(Folder)+'/')
	Folder = Folder + Increment
