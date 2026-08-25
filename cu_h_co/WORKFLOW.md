# Cu(110) Surface Energy, Adsorption, DCD, Bader, and COHP Calculation Workflow

## Directory Structure
- `cu_bulk/`: Geometry optimization of bulk Cu (FCC lattice constant relaxation).
- `cu_110_slab/`: Surface slab creation and relaxation ($2\times2$ supercell, bottom layers frozen, top layers relaxed).
- `h2_gas/`: Isolated $\text{H}_2$ molecule relaxation in a cubic vacuum box ($15\times15\times15\text{ Å}^3$).
- `co_gas/`: Isolated $\text{CO}$ molecule relaxation in a cubic vacuum box ($15\times15\times15\text{ Å}^3$).
- `cu_h_slab/`: $\text{*H}$ atom placed at on-top site on relaxed Cu(110) $2\times2$ surface.
- `cu_co_slab/`: $\text{*CO}$ molecule placed at on-top site on relaxed Cu(110) $2\times2$ surface.
- `cu_in_abs/`: Static run of frozen Cu slab fragment alone (in $2\times2$ supercell for DCD).
- `h_in_abs/`: Static run of frozen $\text{*H}$ adsorbate fragment alone (in $2\times2$ supercell for DCD).
- `co_in_abs/`: Static run of frozen $\text{*CO}$ adsorbate fragment alone (in $2\times2$ supercell for DCD).

---

## Computational Parameters (VASP)

| Parameter | `cu_bulk` | `cu_110_slab` | `h2_gas` | `co_gas` | `cu_h_slab` | `cu_co_slab` | Static Runs (DCD / Bader / COHP) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ENCUT** | 400 eV | 400 eV | 400 eV | 400 eV | 400 eV | 400 eV | 400 eV |
| **ISPIN** | 1 | 1 | 1 | 1 | 2 | 1 | Match relaxed state |
| **ISYM** | 2 | 0 | 2 | 2 | 0 | 0 | -1 (for COHP) / 0 |
| **KPOINTS** | 12x12x12 | 5x5x1 | 1x1x1 | 1x1x1 | 5x5x1 | 5x5x1 | 5x5x1 |
| **ISMEAR / SIGMA** | 0 / 0.05 | 0 / 0.05 | 0 / 0.05 | 0 / 0.05 | 0 / 0.05 | 0 / 0.05 | -5 (Tetrahedron) / 0.05 |
| **LCHARG / LAECHG**| False | False | False | False | False | False | `.TRUE.` (for Bader & DCD) |
| **LWAVE** | False | False | False | False | False | False | `.TRUE.` (for COHP) |
| **NGXF / Y / Z** | Auto | Locked | Auto | Auto | Locked | Locked | **Must be Identical** across fragments |

---

## Energy Summary & Formulas

### 1. Surface Energy ($\gamma$)
$$\gamma = \frac{E_{\text{cu\_110\_slab}} - N_{\text{atoms}} \cdot E_{\text{bulk\_per\_atom}}}{2A}$$

### 2. Adsorption Energies ($E_{\text{ads}}$)
$$E_{\text{ads, H}} = E_{\text{cu\_h\_slab}} - E_{\text{cu\_110\_slab}} - \frac{1}{2} E_{\text{h2\_gas}}$$

$$E_{\text{ads, CO}} = E_{\text{cu\_co\_slab}} - E_{\text{cu\_110\_slab}} - E_{\text{co\_gas}}$$

| System | Directory | Total Energy `TOTEN` (eV) | Status |
| :--- | :--- | :--- | :--- |
| **Bulk Cu (per atom)** | `cu_bulk` | *Pending* | - |
| **Clean Slab ($2\times2$)** | `cu_110_slab` | *Pending* | - |
| **H2 Molecule** | `h2_gas` | *Pending* | - |
| **CO Molecule** | `co_gas` | *Pending* | - |
| **H + Slab** | `cu_h_slab` | *Pending* | - |
| **CO + Slab** | `cu_co_slab` | *Pending* | - |

* **Calculated $\gamma$:** `____ J/m²` (or `eV/Å²`)
* **Calculated $E_{\text{ads, H}}$:** `____ eV`
* **Calculated $E_{\text{ads, CO}}$:** `____ eV`

---

## Post-Processing Analysis Workflows

### 1. Differential Charge Density (DCD)
* **Equation:** $\Delta\rho = \rho_{\text{adsorbed\_slab}} - \rho_{\text{cu\_in\_abs}} - \rho_{\text{adsorbate\_in\_abs}}$
* **Tool:** VASPKIT Option `314`
* **Execution:**
  ```bash
  vaspkit -task 314
  # Inputs: cu_co_slab/CHGCAR cu_in_abs/CHGCAR co_in_abs/CHGCAR