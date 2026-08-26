import os
from mp_api.client import MPRester
from pymatgen.core.structure import Structure
from pymatgen.io.vasp.inputs import Poscar, Kpoints

api_key = os.environ.get("MP_API_KEY", "TW3zWBKnD7RqAqJwLBHxvCvKiplueTcp")
output_dir = "insu_semi_metal"

material_categories = {
    "Insulators": {
        "Diamond": "mp-66",
        "NaCl": "mp-22862",
        "MgO": "mp-1265",
        "BN": "mp-1639",
        "LiF": "mp-1138"
    },
    "Semiconductors": {
        "Si": "mp-149",
        "GaAs": "mp-2534",
        "SiC": "mp-8062",
        "GaN": "mp-830",
        "AlP": "mp-1550"
    },
    "Metals": {
        "Al": "mp-134",
        "Fe": "mp-13",
        "Ag": "mp-124",
        "Au": "mp-81",
        "Pt": "mp-126"
    }
}

base_geo_incar = {
    # Start Parameters
    "ISTART": 0,
    "ICHARG": 2,
    "LWAVE": False,
    "LCHARG": False,
    
    # Electronic Relaxation
    "EDIFF": 1e-06,
    
    # Ionic Relaxation
    "NSW": 60,         
    "IBRION": 2,          
    "ISIF": 3,                 
    "EDIFFG": -0.02, 
}

with MPRester(api_key) as mpr:
    for category, mats in material_categories.items():
        for mat_name, mp_id in mats.items():
            
            struct = mpr.get_structure_by_material_id(mp_id, conventional_unit_cell=False)
            
            geo_dir = os.path.join(output_dir, category, mat_name, "01_geo_opt")
            os.makedirs(geo_dir, exist_ok=True)

            # write POSCAR
            if isinstance(struct, Structure):
                Poscar(struct).write_file(os.path.join(geo_dir, "POSCAR"))
            
            geo_incar = base_geo_incar.copy()
            geo_incar["SYSTEM"] = f"{mat_name} Optimisation"
            
            if category == "Metals":
                geo_incar["ISMEAR"] = 1
                geo_incar["SIGMA"] = 0.2
                geo_incar["ENCUT"] = 450 if mat_name == "Fe" else 400
                k_mesh = (12, 12, 12)
                if mat_name == "Fe":
                    geo_incar["ISPIN"] = 2  # Fe is magnetic 
                    num_atoms = len(struct) if isinstance(struct, Structure) else 1
                    geo_incar["MAGMOM"] = " ".join(["3.0"] * num_atoms)
            else:
                geo_incar["ISMEAR"] = 0
                geo_incar["SIGMA"] = 0.05
                geo_incar["ENCUT"] = 550 if mat_name == "Diamond" else 450
                k_mesh = (6, 6, 6)  
                
            # write INCAR
            with open(os.path.join(geo_dir, "INCAR"), "w") as f:
                for k, v in geo_incar.items(): 
                    f.write(f"{k} = {v}\n")
            
            # write KPOINTS
            Kpoints.gamma_automatic(kpts=k_mesh).write_file(os.path.join(geo_dir, "KPOINTS"))

print("Input generation complete.")