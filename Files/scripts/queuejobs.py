import subprocess
import time

LowFolder = 400
UpperFolder = 520
Increment = 5
Material = "TiN"

Folder = LowFolder

while Folder <= UpperFolder:
	subprocess.Popen('qvasp_kpts_mail 4 24 5 ' + Material + 'ENCUTStudy'+str(Folder)+'.log',cwd='./'+str(Folder)+'/' , shell=True)
	Folder = Folder + Increment
