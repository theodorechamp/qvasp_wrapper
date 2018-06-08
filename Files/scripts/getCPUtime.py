import subprocess
import time
import re

#Set to True if KPOINT study, else False
KPOINT = True

#Change these values if performing on an KPOINT study
if KPOINT:
	LOWFOLDER = 2
	UPPERFOLDER = 9
	INCREMENT = 1

#Change these values if performing an ENCUT study
else:
	LOWFOLDER = 400
	UPPERFOLDER = 500
	INCREMENT = 10

#Change value in '' to set where results will be saved
FILENAME = 'TIME.dat'
MATERIAL = 'W'

FOLDER = LOWFOLDER

with open(FILENAME, 'w') as f_obj:
	f_obj.write('MAT\tENCUT\tKPTS\tCPU time (s)\n')
	while FOLDER <= UPPERFOLDER:
		OUTPUT = subprocess.run("grep 'CPU time' OUTCAR", cwd='./'+str(FOLDER)+'/', shell=True, stdout=subprocess.PIPE)
		CPUTime = re.findall(r'\d+', str(OUTPUT.stdout))
		OUTPUT = subprocess.run('grep ENCUT INCAR', cwd='./'+str(FOLDER)+'/', shell=True, stdout=subprocess.PIPE)
		ENCUT = re.findall(r'\d+', str(OUTPUT.stdout))
		OUTPUT = subprocess.run('cat KPOINTS', cwd='./'+str(FOLDER)+'/', shell=True, stdout=subprocess.PIPE)
		KPOINT = re.findall(r'\d+', str(OUTPUT.stdout))
		f_obj.write(MATERIAL  + '\t' + ENCUT[0] + '\t' + KPOINT[6]  + '\t' + CPUTime[0] + '\n') 
		FOLDER = FOLDER + INCREMENT 
