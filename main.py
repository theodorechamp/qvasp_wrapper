from SSHClient import SSHClient
from Material import Material
import Operations
import constants as c
from bashcmd import bash


def main():
    Operations.newmaterial("Ti", 72)
    client = SSHClient(c.USERNAME, c.PASSWORD, c.HOST, c.PORT)
    client.connect()
    Operations.kptstudy("Ti", client)


if __name__ == "__main__":
    main()
 #   bash("rm -r ./Files/Ti/")