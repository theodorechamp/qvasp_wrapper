from __future__ import print_function
import re
import os
import constants as c
from StructureIdentify import Structure


class DataContainer:
	def __init__(self, time, ENMAX, ENCUT, KPTS, ions, number, hydrogen, lattype):
		self.time = time
		self.ENCUT = ENCUT
		self.KPTS = KPTS
		self.ions = ions
		self.number = number
		self.hydrogen = hydrogen
		self.lattype = lattype
		self.ENMAX = ENMAX

	def print(self):
		for x in self.ions:
			print(x[0] + " " + str(x[1]) + " ", end="")
		print("\n")
		print("Time to run: " + str(self.time))
		print("ENCUT: " + str(self.ENCUT))
		print("KPTS: " + str(self.KPTS))


class Crawler:
	def __init__(self, c):
		self.client = c
		self.materials = []

	def crawl(self, path):
		self.crawlrec(path)

	def crawlrec(self, path):
		self.client.cd(path)

		response = self.client.command("grep 'reached required' OUTCAR")
		if len(response) > 1:
			print(path)
			if "final" in path or "initial" in path:
				print("This is dumbobo")
			elif "NEB" in path:
				print("NEB")
			elif "DIMER" in path:
				print("Dimer")
			else:
				response = self.client.command("grep 'CPU time' OUTCAR")
				time = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", response)
				response = self.client.command("grep '<i name=\"ENCUT\">' vasprun.xml")
				ENCUT = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", response)
				response = self.client.command("grep '<v type=\"int\" name=\"divisions\">' vasprun.xml ")
				KPTS = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", response)

				response = self.client.command("grep ENMAX POTCAR")
				ENMAX = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", response)[0]

				response = self.client.command("cat POSCAR")
				struct = Structure(response)
				lattype = struct.identifystruct()
				responsesplit = response.split("\n")
				molesandnum = responsesplit[0]
				temp = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", molesandnum)
				number = 0
				for x in temp:
					number += int(x)
				molecule = ""
				for x in molesandnum:
					if x != " ":

						if x.isalpha():
							molecule += x

				if "Hydrogen" in path:
					hydrogen = True
				else:
					hydrogen = False
				if hydrogen:
					hdist = struct.hydrogendistance()
				else:
					hdist = 0.0

				data = DataContainer(time, ENMAX, ENCUT, KPTS, molecule.rstrip(), number, hdist, lattype)
				self.materials.append(data)

		folders = self.client.command("echo */").split(" ")
		if len(folders) > 1:
			for x in folders:
				x = re.sub('\n', '', x)
				self.crawlrec(path + x)

	def write(self, fn):
		f = open(os.getcwd() + c.OUTPUTLOCATION + fn, "w")
		f.write("ions,number,hydrogen,lattice type,KPTS,ENCUT,ENMAX,time\n")
		for x in self.materials:
			f.write(x.ions + "," + str(x.number) + "," + str(x.hydrogen) + "," + str(x.lattype) + "," + str(x.KPTS[0]) + "," + str(x.ENCUT[0]) + "," + str(x.ENMAX) + ","+ str(x.time[0]) +"\n")

		f.close()
		print("done!")