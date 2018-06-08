import subprocess
import time

LowFolder = 1
UpperFolder = 4
Increment = 1

Folder = LowFolder

while Folder <= UpperFolder:
	subprocess.Popen('qvasp_kpts_mail 4 24 5 NbiHydrogen'+str(Folder)+'.log',cwd='./'+str(Folder)+'i/' , shell=True)
	subprocess.Popen('qvasp_kpts_mail 4 24 5 NbfHydrogen'+str(Folder)+'.log',cwd='./'+str(Folder)+'f/' , shell=True)	
	Folder = Folder + Increment
