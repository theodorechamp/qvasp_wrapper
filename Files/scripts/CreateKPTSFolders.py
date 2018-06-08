import subprocess
import time
#TODO: Edit KPOINTS files

for i in range(2,10):
	subprocess.Popen('mkdir ./'+str(i)+'/',shell=True)
	time.sleep(1)
	subprocess.Popen('cp -r ./INCAR ./'+str(i)+'/',shell=True)
	subprocess.Popen('cp -r ./POTCAR ./'+str(i)+'/',shell=True)
	subprocess.Popen('cp -r ./KPOINTS ./'+str(i)+'/',shell=True)
	subprocess.Popen('cp -r ./POSCAR ./'+str(i)+'/',shell=True)
	time.sleep(1)
	out = open("./"+str(i)+"/KPOINTS","a")
	out.write(str(i)+' '+str(i)+' '+str(i)+'\n')
	out.close()

