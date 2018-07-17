from SSHClient import SSHClient
from Material import Material
import Operations
import constants as c
from bashcmd import bash
from crawler import Crawler

import os


def main():
	client = SSHClient(c.USERNAME, c.PASSWORD, c.HOST, c.PORT)
	client.connect()
	crawler = Crawler(client)
	crawler.crawl(c.PROJECT)
	crawler.write("timedata.csv")


if __name__ == "__main__":
    main()
#    bash("rm -r ./Files/Ti/")
