import os
import numpy as np
from pymatgen.core.structure import Structure, Molecule
from pymatgen.core.surface import Slab
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.io.vasp.inputs import Poscar, Kpoints, Incar

slab_poscar_path = "cr_o2/cr_110_slab/POSCAR"  # Use CONTCAR if VASP was run
o2_slab_dir = "cr_o2/cr_o2_slab"
os.makedirs(o2_slab_dir, exist_ok=True)

# Slab generation
slab_struct = Structure.from_file(slab_poscar_path)

slab = Slab(
    lattice=slab_struct.lattice,
    species=slab_struct.species,
    coords=slab_struct.frac_coords,
    miller_index=(1, 1, 0),
    oriented_unit_cell=slab_struct,
    shift=0,
    scale_factor=np.eye(3),
    site_properties=slab_struct.site_properties
)

# build O2 molecule
o2_mol = Molecule(["O", "O"], [[0, 0, 0], [0, 0, 1.2075]])

asf = AdsorbateSiteFinder(slab)
ads_sites = asf.find_adsorption_sites()

top_site = ads_sites["ontop"][0]
o2_adsorbed_struct = asf.add_adsorbate(o2_mol, top_site)    # Sum of covalent radii is used automatically

o2_adsorbed_struct.sort(key=lambda site: site.c)

num_sites = len(o2_adsorbed_struct)
freeze_cutoff = int((num_sites - 2) * 0.6)

selective_dynamics = []
for i, site in enumerate(o2_adsorbed_struct):
    if i < freeze_cutoff:
        selective_dynamics.append([False, False, False]) # Freeze
    else:
        selective_dynamics.append([True, True, True])    # Relax (Top Cr + O2)

o2_adsorbed_struct.add_site_property("selective_dynamics", selective_dynamics)

# write POSCAR
Poscar(o2_adsorbed_struct).write_file(os.path.join(o2_slab_dir, "POSCAR"))
print("POSCAR generated")

# 7. write KPOINTS & INCAR
Kpoints.gamma_automatic(kpts=(9, 9, 1)).write_file(os.path.join(o2_slab_dir, "KPOINTS"))

incar_dict = {
    "SYSTEM": "O2 adsorbed on clean Cr(110)",

    # Start Parameters
    "ISTART": 0,
    "ISPIN": 2,  
    "ICHARG": 2,
    "LWAVE": False,
    "LCHARG": False,
    
    # Electronic Relaxation
    "ENCUT": 400,
    "ISMEAR": 0,
    "SIGMA": 0.05,
    "EDIFF": 1e-06,
    
    # Ionic Relaxation
    "NSW": 100,
    "IBRION": 2,          
    "ISIF": 2,              
    "ISYM": 0,               # Disable symmetry to allow for asymmetric relaxation
    "EDIFFG": -0.02, 
}

Incar.from_dict(incar_dict).write_file(os.path.join(o2_slab_dir, "INCAR"))
print("INCAR and KPOINTS generated")

# POTCAR generation is not included in this script as it requires specific pseudopotential files that are not part of the pymatgen library.