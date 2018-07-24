import re

class Structure:

	def __init__(self, file):
		self.file = file.split("\n")

	def distance(self, str1, str2):
		str1s = str1.split(" ")
		str2s = str2.split(" ")
		if len(str2s) < 3:
			return 0
		str1s = [x for x in str1s if x != '']
		str2s = [x for x in str2s if x != '']
		return self.distancesplit(str1s, str2s)

	def distancesplit(self, p1, p2):
		d1 = abs((float(p1[0])-float(p2[0])))
		if d1 > .5:
			d1 = 1 - d1
		d2 = abs((float(p1[1])-float(p2[1])))
		if d2 > .5:
			d2 = 1 - d2
		d3 = abs((float(p1[2])-float(p2[2])))
		if d3 > .5:
			d3 = 1 - d3
		return (d1**2+d2**2+d3**2)**.5
		'''d1 = (float(p1[0])*float(p2[0]))**2
		if d1 > .5:
			d1 = 1 - d1
		d2 = (float(p1[1])*float(p2[1]))**2
		if d2 > .5:
			d2 = 1 - d2
		d3 = (float(p1[2])*float(p2[2]))**2
		if d3 > .5:
			d3 = 1 - d3
		return (d1+d2+d3)'''

	def calculatemidpoint(self, l1, l2, l3, l4):
		m = [(float(l1[0])+float(l2[0])+float(l3[0])+float(l4[0]))/4, (float(l1[1])+float(l2[1])+float(l3[1])+float(l4[1]))/4, (float(l1[2])+float(l2[2])+float(l3[2])+float(l4[2]))/4]
		return m;

	def hydrogendistance(self):
		ions = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", self.file[6])[0]
		hloc = self.file[6+int(ions)]
		hlocs = hloc.split(" ")
		hlocs = [x for x in hlocs if x != '']
		distances = []
		i = 8
		for x in self.file[8:]:
			d = [self.distance(hloc, x), i]
			if d[0] > 0.005:
				distances.append(d)
			i += 1
		distances.sort()
		p1 = self.file[distances[0][1]].split(" ")
		p1 = [x for x in p1 if x != '']
		p2 = self.file[distances[1][1]].split(" ")
		p2 = [x for x in p2 if x != '']
		p3 = self.file[distances[2][1]].split(" ")
		p3 = [x for x in p3 if x != '']
		p4 = self.file[distances[3][1]].split(" ")
		p4 = [x for x in p4 if x != '']
		mp = self.calculatemidpoint(p1, p2, p3, p4)
		return self.distancesplit(hlocs, mp)

	def identifystruct(self):
		iline = self.file[len(self.file)/2]
		distances = []
		for x in self.file[8:]:
			d = self.distance(iline, x)
			if d > 0.1:
				distances.append(d)
		distances.sort()
		error = 0.05
		while True:
			count = 1
			for i in range(1, len(distances) - 1):
				if abs(distances[0] - distances[i]) < error:
					count += 1
				else:
					break
			print(count)
			if count == 4:
				return 4
			elif count == 6:
				return 6
			elif count == 8:
				return 8
			elif error <= 0:
				return 0
			elif count > 8:
				print("Here")
				error = error - 0.01
			else:
				return 0
