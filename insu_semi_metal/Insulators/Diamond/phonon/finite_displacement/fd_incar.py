import os
from pymatgen.io.vasp.inputs import Incar

phonon_dir = "phonon/finite_displacement"
os.makedirs(phonon_dir, exist_ok=True)


incar_dict = {
   "SYSTEM": "Phonon",

    "PREC": "Accurate",
    "ENCUT": 500,

    "ISTART": 0,
    "ICHARG": 2,
    "ISPIN": 1,

    "NELM": 60,
    "NELMIN": 4,
    "NELMDL": -3,
    "EDIFF": 1E-7,

    "IALGO": 38,
    "ADDGRID": "TRUE",
    "LREAL": "FALSE",

    "NSW": 0,       
    "IBRION": -1,

    "EDIFFG": -1E-7,

    "ISMEAR": 0,
    "SIGMA": 0.01
}

Incar.from_dict(incar_dict).write_file(os.path.join(phonon_dir, "INCAR"))
print("INCAR generated")