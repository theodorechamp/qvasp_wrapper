from time import sleep
from subprocess import Popen


def bash(cmd, echo=False):
    # type: (string, Boolean) -> object
    Popen(cmd, shell=True)
    if echo:
        print(cmd)
    sleep(0.01)
