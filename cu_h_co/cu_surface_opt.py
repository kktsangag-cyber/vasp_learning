import os
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.vasp.inputs import Poscar, Kpoints, Incar

bulk_poscar_path = "cu_h_co/cu_bulk/POSCAR"  # Use CONTCAR if VASP was run
slab_dir = "cu_h_co/cu_110_slab"
os.makedirs(slab_dir, exist_ok=True)

# Load relaxed bulk structure
bulk_struct = Structure.from_file(bulk_poscar_path)

# Slab generation
miller_index = (1, 1, 0)
min_slab_size = 10.0   # Minimum slab thickness in Å (~5-6 atomic layers)
min_vacuum_size = 15.0 # Vacuum layer along Z-axis

slab_gen = SlabGenerator(
    initial_structure=bulk_struct,
    miller_index=miller_index,
    min_slab_size=min_slab_size,
    min_vacuum_size=min_vacuum_size,
    center_slab=True,
    primitive=True  
)

slabs = slab_gen.get_slabs()
cu_slab = slabs[0]

# make a 2x2 Supercell
cu_slab.make_supercell([2, 2, 1])

# add selective dynamics for POSCAR
cu_slab.sort(key=lambda site: site.c)

num_sites = len(cu_slab)
freeze_cutoff = int(num_sites * 0.6)

selective_dynamics = []
for i in range(num_sites):
    if i < 16:
        selective_dynamics.append([False, False, False])
    else:
        selective_dynamics.append([True, True, True])

# write POSCAR
Poscar(cu_slab, selective_dynamics=selective_dynamics).write_file(os.path.join(slab_dir, "POSCAR"))
print("POSCAR with Selective Dynamics generated")

# write KPOINTS
kpts = Kpoints.gamma_automatic(kpts=(5, 5, 1))    # Only one k-point is usually needed along the vacuum direction
kpts.write_file(os.path.join(slab_dir, "KPOINTS"))
print("KPOINTS generated")

# write INCAR
incar_dict = {
    "SYSTEM": "clean Cu(110) surface",

    # Start Parameters
    "ISTART": 0,
    "ISPIN": 1,                 # Cu is non-magnetic
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
    "ISIF": 2,               # Fixed cell shape and volume for surface calculations
    "ISYM": 0,               # Disable symmetry to allow for asymmetric relaxation
    "EDIFFG": -0.02, 
}

Incar.from_dict(incar_dict).write_file(os.path.join(slab_dir, "INCAR"))
print("INCAR generated")

# POTCAR is the same as in the bulk optimization step.