import subprocess
import os
import time
from SSHClient import SSHClient
import constants as c

CELLSIZE = 4


def newmaterial(materialname, materialID):
    # Generate Poscar, expand it, place in correct folder
    subprocess.Popen('mkdir ' + os.getcwd() + c.FILESLOCATION + materialname, shell=True)
    time.sleep(0.25)
    subprocess.Popen('cp ' + os.getcwd() + c.FILESLOCATION + 'scripts/GenerateSlab.py ' + os.getcwd() + c.FILESLOCATION + materialname, shell=True)
    subprocess.Popen('python ' + os.getcwd() + c.FILESLOCATION + materialname + '/GenerateSlab.py ' + str(materialID) + ' ' + str(CELLSIZE), shell=True)
    subprocess.Popen('cp ' + os.getcwd() + '/POSCAR ' + os.getcwd() + c.FILESLOCATION + materialname + '/', shell = True)
    print('rm ' + os.getcwd() + '/POSCAR')
    subprocess.Popen('rm ' + os.getcwd() + '/POSCAR')
    time.sleep(1)


def kptstudy(materialname, client):
    client.cd(c.SCRATCH)
    client.command("mkdir " + materialname)
    client.cd(c.SCRATCH + materialname, relative=True)
    client.command("mkdir " + c.KPOINTFOLDER)
    client.uploadFTP(c.SCRATCH + materialname + '/' + c.KPOINTFOLDER + '/POSCAR',
                     os.getcwd()+c.FILESLOCATION+materialname + '/POSCAR')
    client.cd(materialname + '/' + c.KPOINTFOLDER)
    client.showcwd()
