# Cr(110) Surface O2 Adsorption Calculation Workflow

## Directory Structure
- `cr_bulk/`: Geometry optimization of bulk Cr (BCC lattice constant relaxation).
- `cr_110_slab/`: Surface slab creation and relaxation (bottom layers frozen, top layers relaxed).
- `cr_o2_slab/`: O2 molecule placed at on-top site (~1.94 Å) on relaxed Cr(110) surface.

---

## Computational Parameters (VASP)

| Parameter | `cr_bulk` | `cr_110_slab` | `cr_o2_slab` |
| :--- | :--- | :--- | :--- |
| **ENCUT** | 400 eV | 400 eV | 400 eV |
| **ISPIN** | 2 | 2  | 2  |
| **ISYM** | 2 | 0 | 0 |
| **KPOINTS** | 11x11x11 | 9x9x1 | 9x9x1 |
| **ISMEAR / SIGMA** | 1 / 0.2 | 0 / 0.05 | 0 / 0.05 |

---

## Energy Summary & Adsorption Formula

E_ads = E_(slab+O2) - (E_clean_slab + E_O2_gas)

| System | Directory | Total Energy `TOTEN` (eV) | Status |
| :--- | :--- | :--- | :--- |
| **Clean Slab** | `cr_110_slab` | *Pending* | - |
| **O2 Molecule** | `o2_gas` | *Pending* | - |
| **O2 + Slab** | `cr_o2_slab` | *Pending* | - |

**Calculated $E_{\text{ads}}$:** `____ eV`
