'''
TODO: Improve makepot functionality, delete POSCAR somehow

'''

import os
from SSHClient import SSHClient
import constants as c
from bashcmd import bash
import re
import math
import time

CELLSIZE = 4


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def newmaterial(materialname, materialID):
    # Generate Poscar, expand it, place in correct folder
    bash('mkdir ' + os.getcwd() + c.FILESLOCATION + materialname)
    bash('cp ' + os.getcwd() + c.FILESLOCATION + 'scripts/GenerateSlab.py ' + os.getcwd() + c.FILESLOCATION + materialname)
    bash('python ' + os.getcwd() + c.FILESLOCATION + materialname + '/GenerateSlab.py ' + str(materialID) + ' ' + str(CELLSIZE))
    bash('cd Files/Ti; ls')

def kptstudy(materialname, client):
    # Making folders, uploading POSCAR file and POTCAR file
    client.cd(c.SCRATCH)
    client.command("mkdir " + materialname)
    client.command("mkdir " + c.SCRATCH + materialname + "/" + c.KPOINTFOLDER)
    time.sleep(10)
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'POSCAR', os.getcwd()+c.FILESLOCATION+materialname + '/POSCAR')
    client.cd('/' + materialname + '/'+ c.KPOINTFOLDER, relative=True)
    client.command('makepot ' + materialname)

    #Finding reasonable ENCUT value
    response = client.command('grep ENMAX POTCAR')
    ENMAX = float(re.findall(r'\d+', response)[0])
    ENCUT = ENMAX * 1.5
    ENCUT = roundup(ENCUT)

    # Setting up INCAR
    bash('cp ' + os.getcwd() + c.INPUTLOCATION + 'INCAR ' + os.getcwd() + c.FILESLOCATION + materialname)
    bash('cp ' + os.getcwd() + c.INPUTLOCATION + 'KPOINTS ' + os.getcwd() + c.FILESLOCATION + materialname)
    out1 = open(os.getcwd() + c.FILESLOCATION +materialname + '/INCAR', 'a')
    out1.write('ENCUT = ' + str(ENCUT) + '\n')
    out2 = open(os.getcwd() + c.FILESLOCATION + materialname + '/POSCAR', 'r')
    numofions = getionnumber(out2.read())
    out2.close()
    out1.write('MAGMOM = ' + str(numofions) + '*1.0')
    out1.close()

    # Uploading INCAR and KPOINT Files
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'INCAR',
                     os.getcwd() + c.FILESLOCATION + materialname + '/INCAR')
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'KPOINTS',
                     os.getcwd() + c.FILESLOCATION + materialname + '/KPOINTS')
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'CreateKPTSFolders.py',
                     os.getcwd() + c.FILESLOCATION + 'scripts/CreateKPTSFolders.py')

    #Set up KPointStudy
    print("Setting up KPoints...")
    client.command("python CreateKPTSFolders.py")
    time.sleep(2)


def getionnumber(output):
    array = output.splitlines()
    number = array[6]
    numbers = re.findall(r'\d+', number)
    total = 0
    for x in numbers:
        total += int(x)
    return total



