import os
import numpy as np
from pymatgen.core.structure import Molecule
from pymatgen.io.vasp.inputs import Poscar, Incar, Kpoints

h2_gas_dir = "cu_h_co/h2_gas"
os.makedirs(h2_gas_dir, exist_ok=True)

# build h2 in cubic cell
h2_mol = Molecule(
    species=["H", "H"],
    coords=[
        [0.0, 0.0, -0.37],
        [0.0, 0.0, 0.37]
    ]
)

h2_box = h2_mol.get_boxed_structure(15.0, 15.0, 15.0)

# write POSCAR
Poscar(h2_box).write_file(os.path.join(h2_gas_dir, "POSCAR"))

# write INCAR
incar_dict = {
    "SYSTEM": "h2 gas molecule",

    # Start Parameters
    "ISTART": 0,
    "ISPIN": 1,                 # H2 is non-magnetic
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
Incar.from_dict(incar_dict).write_file(os.path.join(h2_gas_dir, "INCAR"))

# 5. Write KPOINTS (Gamma-point only for isolated gas phase)
kpoints = Kpoints.gamma_automatic(kpts=(1, 1, 1))
kpoints.write_file(os.path.join(h2_gas_dir, "KPOINTS"))

print("Input files generated")

# POTCAR generation is not included in this script as it requires specific pseudopotential files that are not part of the pymatgen library.