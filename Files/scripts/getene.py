import subprocess
import time

#Set to True if KPOINT study, else False
KPOINT = False

#Change these values if performing on KPOINT study
if KPOINT:
	LOWFOLDER = 2
	UPPERFOLDER = 9
	INCREMENT = 1

#Change these values if performing on ENCUT study
else:
	LOWFOLDER = 400
	UPPERFOLDER = 520
	INCREMENT = 5

#Change value in '' to set where results will be saved
FILENAME = 'ENEResults.txt'

FOLDER = LOWFOLDER

with open(FILENAME, 'w') as f_obj:
	while FOLDER <= UPPERFOLDER:
		OUTPUT = subprocess.run('ene',cwd='./'+str(FOLDER)+'/',shell=True,stdout=subprocess.PIPE)
		strOUTPUT = str(OUTPUT.stdout)
		energies = [strOUTPUT[103:116], strOUTPUT[141:154]]  	
		f_obj.write(str(FOLDER) + '\t' + energies[0] + '\t' + energies[1]+'\n')
		FOLDER = FOLDER + INCREMENT
		time.sleep(1)
