from SSHClient import SSHClient
from Material import Material
import Operations
import constants as c
import subprocess


def main():
    Operations.newmaterial("Ti", 72)
    client = SSHClient(c.USERNAME, c.PASSWORD, c.HOST, c.PORT)
    client.connect()
    Operations.kptstudy("Ti", client)


if __name__ == "__main__":
    main()
    subprocess.Popen("rm -r ./Files/Ti/", shell=True)