import os
import numpy as np
from pymatgen.core.structure import Structure, Molecule
from pymatgen.core.surface import Slab
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.io.vasp.inputs import Poscar, Kpoints, Incar

slab_poscar_path = "cu_h_co/cu_110_slab/POSCAR"  # Use CONTCAR if VASP was run
co_slab_dir = "cu_h_co/cu_co_slab"
os.makedirs(co_slab_dir, exist_ok=True)

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

# make a 2x2 Supercell to prevent artificial CO-CO image interactions (0.25 ML coverage)
slab.make_supercell([2, 2, 1])

# build CO molecule
co_mol = Molecule(["C", "O"], [[0, 0, 0], [0, 0, 1.13]])

asf = AdsorbateSiteFinder(slab)
ads_sites = asf.find_adsorption_sites()

top_site = ads_sites["ontop"][0]
co_adsorbed_struct = asf.add_adsorbate(co_mol, top_site)    # Sum of covalent radii is used automatically

co_adsorbed_struct.sort(key=lambda site: site.z)

selective_dynamics = []
for i in range(len(co_adsorbed_struct)):
    if i < 16:
        selective_dynamics.append([False, False, False])  # Freeze bottom 4 Cu layers
    else:
        selective_dynamics.append([True, True, True])     # Relax top Cu layer + CO

# write POSCAR
poscar = Poscar(co_adsorbed_struct, selective_dynamics=selective_dynamics)
poscar.write_file(os.path.join(co_slab_dir, "POSCAR"))

# write KPOINTS & INCAR
Kpoints.gamma_automatic(kpts=(5, 5, 1)).write_file(os.path.join(co_slab_dir, "KPOINTS"))

incar_dict = {
    "SYSTEM": "CO adsorbed on Cu(110) 2x2",

    # Start Parameters
    "ISTART": 0,
    "ISPIN": 1,  
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

Incar.from_dict(incar_dict).write_file(os.path.join(co_slab_dir, "INCAR"))
print("INCAR and KPOINTS generated")

# POTCAR is the combined POTCAR in the bulk and gas optimization step.