import os
import numpy as np
from pymatgen.core.structure import Molecule
from pymatgen.io.vasp.inputs import Poscar, Incar, Kpoints

o2_gas_dir = "cr_o2/o2_gas"
os.makedirs(o2_gas_dir, exist_ok=True)

# build o2 in cubic cell
o2_mol = Molecule(
    species=["O", "O"],
    coords=[
        [0.0, 0.0, -0.605],
        [0.0, 0.0, 0.605]
    ]
)

o2_box = o2_mol.get_boxed_structure(15.0, 15.0, 15.0)

# write POSCAR
Poscar(o2_box).write_file(os.path.join(o2_gas_dir, "POSCAR"))

# write INCAR
incar_dict = {
    "SYSTEM": "clean Cr(110) surface",

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
    "NSW": 30,
    "IBRION": 2,          
    "ISIF": 2,                       
    "EDIFFG": -0.02, 
}
Incar.from_dict(incar_dict).write_file(os.path.join(o2_gas_dir, "INCAR"))

# 5. Write KPOINTS (Gamma-point only for isolated gas phase)
kpoints = Kpoints.gamma_automatic(kpts=(1, 1, 1))
kpoints.write_file(os.path.join(o2_gas_dir, "KPOINTS"))

print("✓ Input files generated successfully in ./cr_o2_gas/")