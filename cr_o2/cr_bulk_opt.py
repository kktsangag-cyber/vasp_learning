import os
from mp_api.client import MPRester
from pymatgen.core.structure import Structure
from pymatgen.io.vasp.inputs import Poscar, Kpoints, Incar

api_key = "TW3zWBKnD7RqAqJwLBHxvCvKiplueTcp"
output_dir = "cr_o2/cr_bulk"
os.makedirs(output_dir, exist_ok=True)

# get Cr
with MPRester(api_key) as mpr:
    res = mpr.get_structure_by_material_id("mp-90")
    struct = res[0] if isinstance(res, list) else res

# write POSCAR
if isinstance(struct, Structure):
    Poscar(struct).write_file(os.path.join(output_dir, "POSCAR"))
    print("POSCAR generated")

# write KPOINTS
kpts = Kpoints.gamma_automatic(kpts=(11, 11, 11))   # Suggested by AI due to Reciprocal Density Rule
kpts.write_file(os.path.join(output_dir, "KPOINTS"))
print("KPOINTS generated")

# write INCAR
incar_dict = {
    "SYSTEM": "Cr Bulk Optimization",

    # Start Parameters
    "ISTART": 0,            # Read existing wavefunction; if there
    "ISPIN": 2,             # Cr is magnetic
    "ICHARG": 2,            # Initial charge density from atomic superposition
    "LWAVE": False,         # Not required in bulk optimization
    "LCHARG": False,        # Not required in bulk optimization

    # Electronic Relaxation
    "ENCUT": 400,           # Greater than the maximum ENMAX in POTCAR
    "ISMEAR": 0,            # For metallic systems, ISMEAR = 0 or 1 is commonly used
    "SIGMA": 0.05,          # For metals, 0.05 and 0.1 eV are commonly used
    "EDIFF": 1e-06,

    # Ionic Relaxation
    "NSW": 30,
    "IBRION": 2,            # Conjugate-gradient ionic relaxation
    "ISIF": 3,              # Geometric optimization
    "ISYM" : 2,             # Fast symmetry mode
    "EDIFFG": -0.02,        # Force convergence criterion in eV/Å
}

Incar.from_dict(incar_dict).write_file(os.path.join(output_dir, "INCAR"))
print("INCAR generated")

# POTCAR generation is not included in this script as it requires specific pseudopotential files that are not part of the pymatgen library.