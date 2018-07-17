from pymatgen import *
import os
import sys

a = MPRester("dh6VviweGRaAUItf")
struct = a.get_structures(sys.argv[1])
if len(sys.argv) == 3:
    struct[0].make_supercell([sys.argv[2],sys.argv[2],sys.argv[2]])
else:
    struct[0].make_supercell([3,3,3])
struct[0].to("poscar", os.path.dirname(os.path.realpath(__file__))+'/POSCAR')
