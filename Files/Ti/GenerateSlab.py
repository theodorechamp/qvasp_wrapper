# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:42:37 2017

@author: Sarah
"""
import sys, os
from pymatgen import *
m = MPRester("CWqrbiQxDVUza5Xk")
if len(sys.argv) > 1:
    mpid = "mp-" + str(sys.argv[1])

else:
    mpid = "mp-27953"
struct = m.get_structure_by_material_id(mpid)
if len(sys.argv) > 1:
    struct.make_supercell([sys.argv[2],sys.argv[2],sys.argv[2]])
else:
    struct.make_supercell([3,3,3])
struct.to("poscar",os.getcwd()+'/POSCAR')

from pymatgen.core.surface import *
#min_slab_size= 12
#min_vacuum_size= 13
#lll_reduce=True
#center_slab=False
#primitive=True
#
#max_miller=1
#tol=0.1
#bonds=None
#max_broken_bonds=0
#symmetrize=True
#
#
#
#allslabs=generate_all_slabs(struct,max_miller,min_slab_size,min_vacuum_size,bonds,tol,max_broken_bonds,lll_reduce,center_slab,primitive)
#print(len(allslabs))
#allslabs
#from pprint import pprint
#pprint([ slab.miller_index for slab in allslabs ])
#
#for slab in allslabs:
#    miller=slab.miller_index
#    gen = SlabGenerator(struct, miller, min_slab_size, min_vacuum_size, lll_reduce,center_slab, primitive)
#    slabs=gen.get_slabs()
#    print(len(slabs))
#    print(slabs[0])
#    slabs[0].to("poscar",os.getcwd()+'/POSCAR-'+struct.formula.replace(" ", "")+'-slab'+str(miller))

#MIs = ['(0, 0, 1)','(1, 0, 0)','(1, 0, 1)','(1, 1, -1)','(1, 1, 0)','(1, 1, 1)']
#MIs = ['(1, 0, -1)', '(1, 1, -1)','(1, 1, 0)','(1, 1, 1)']
##MIs = ['(1, 0, -1)', '(1, 1, 0)','(1, 1, 1)']
#for x in MIs:
#    #struct = Structure.from_file("POSCAR-Mo32N16-Slab"+str(x))
#    struct = Structure.from_file("POSCAR-W27N27-Slab"+str(x))
#    struct.make_supercell([2,2,1])
#    #struct.to("poscar",os.getcwd()+'/POSCAR-MoN-Slab'+str(x))
#    struct.to("poscar",os.getcwd()+'/POSCAR-WN-Slab'+str(x))
#    struct = Structure.from_file("WN_CONTCAR"+str(x))
#    m = struct.lattice.matrix
#    print(np.linalg.norm(np.cross(m[0], m[1])))


#MIs = ['111','110','11-1','101','100','001']
#for x in MIs:
#    struct = Structure.from_file("CONTCAR-"+str(x)+'slab')
#    m = struct.lattice.matrix
#    print(np.linalg.norm(np.cross(m[0], m[1])))
#
#    def add_adsorbate_atom(self, indices, specie, distance):
#        """
#        Gets the structure of single atom adsorption.
#        slab structure from the Slab class(in [0, 0, 1])
#
#        Args:
#            indices ([int]): Indices of sites on which to put the absorbate.
#                Absorbed atom will be displaced relative to the center of
#                these sites.
#            specie (Specie/Element/str): adsorbed atom species
#            distance (float): between centers of the adsorbed atom and the
#                given site in Angstroms.
#        """
#        # Let's do the work in cartesian coords
#        center = np.sum([self[i].coords for i in indices], axis=0) / len(
#            indices)
#
#        coords = center + self.normal * distance / np.linalg.norm(self.normal)
#
#        self.append(specie, coords, coords_are_cartesian=True)
#
#
#add_adsorbate_atom(struct, [1, 1, 1], 1, 0.05016)


#elements = ['MoN']
#dirs = ['001','100','101','11-1','110','111']
#
#for x in elements:
#    change_to_el = x
#    name = 'MoN'
#    os.makedirs(name)
#    for y in dirs:
#        subdirectory = name + "/" + y + "/"
#        os.makedirs(subdirectory)
