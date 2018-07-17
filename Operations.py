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

def newmaterial(materialname):
    # Generate Poscar, expand it, place in correct folder
    bash('mkdir ' + os.getcwd() + c.FILESLOCATION + materialname)
    bash('cp ' + os.getcwd() + c.FILESLOCATION + 'scripts/GenerateSlab.py ' + os.getcwd() + c.FILESLOCATION + materialname)
    bash('python ' + os.getcwd() + c.FILESLOCATION + materialname + '/GenerateSlab.py ' + str(materialname) + ' ' + str(CELLSIZE))
    bash('cd Files/Ti; ls')

def kptstudysetup(materialname, client):
    # Making folders, uploading POSCAR file and POTCAR file
    client.cd(c.SCRATCH)
    client.command("mkdir " + materialname)
    client.command("mkdir " + c.SCRATCH + materialname + "/" + c.KPOINTFOLDER)
    time.sleep(10)
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'POSCAR', os.getcwd()+c.FILESLOCATION+materialname + '/POSCAR')
    client.cd('/' + materialname + '/'+ c.KPOINTFOLDER, relative=True)
    client.command('makepot ' + materialname)

    # Finding reasonable ENCUT value
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

    # Set up KPointStudy
    print("Setting up KPoints...")
    client.command("python CreateKPTSFolders.py")
    time.sleep(2)

    # Queuing jobs
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'queuejobsKPTS.py',
                     os.getcwd() + c.FILESLOCATION + 'scripts/queuejobsKPTS.py')
    client.command("python queuejobsKPTS.py " + materialname, echo=True)


def kptstudyanalysis(materialname, client):
    # Upload geteneKPT.py file
    client.cd(c.SCRATCH)
    client.cd(materialname, relative=True)
    client.cd(c.KPOINTFOLDER, relative=True)
    client.uploadFTP(c.SCRATCH + materialname + c.KPOINTFOLDER + 'geteneKPT.py',
                     os.getcwd() + c.FILESLOCATION + 'scripts/geteneKPT.py')
    # Run geteneKPT.py
    client.command("python geteneKPT.py")
    time.sleep(10)

    # Get contents of ENEResults.txt
    results = client.command("cat " + c.ENERESULTSFILE).splitlines()
    energy_wo_entropy = []
    energy_w_entropy = []
    for x in results:
        values = re.findall(r'\d+.\d+', x)
        energy_wo_entropy.append(values[0])
        energy_w_entropy.append(values[1])
    ionnumber = getionnumber(client.command("cat POSCAR"))
    energy_wo_entropy_per_atom = []
    for x in energy_wo_entropy:
        energy_wo_entropy_per_atom.append(float(x) / float(ionnumber))
    energy_w_entropy_per_atom = []
    for x in energy_w_entropy:
        energy_w_entropy_per_atom.append(float(x) / float(ionnumber))

    # Choosing appropriate KPTS

def encutstudysetup(materialname, client):
    # Creating ENCUTStudy folder
    client.cd(c.SCRATCH)
    client.cd(materialname, relative=True)
    client.command("mkdir " + c.ENCUTFOLDER)
    # Copying


def getionnumber(output):
    array = output.splitlines()
    number = array[6]
    numbers = re.findall(r'\d+', number)
    total = 0
    for x in numbers:
        total += int(x)
    return total



