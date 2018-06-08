from time import sleep
from subprocess import Popen


def bash(cmd):
    Popen(cmd, shell=True)
    sleep(0.001)
