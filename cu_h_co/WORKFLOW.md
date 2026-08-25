# Cu(110) Surface Energy, Adsorption, DCD, Bader, and COHP Calculation Workflow

## Directory Structure
- `cu_bulk/`: Geometry optimization of bulk Cu (FCC lattice constant relaxation).
- `cu_110_slab/`: Surface slab creation and relaxation ($2\times2$ supercell, bottom layers frozen, top layers relaxed).
- `h2_gas/`: Isolated $\text{H}_2$ molecule relaxation in a cubic vacuum box ($15\times15\times15\text{ Å}^3$).
- `co_gas/`: Isolated $\text{CO}$ molecule relaxation in a cubic vacuum box ($15\times15\times15\text{ Å}^3$).
- `cu_h_slab/`: $\text{*H}$ atom placed at on-top site on relaxed Cu(110) $2\times2$ surface.
- `cu_co_slab/`: $\text{*CO}$ molecule placed at on-top site on relaxed Cu(110) $2\times2$ surface.
- `cu_in_cuco_abs/`: Static run of frozen Cu slab fragment alone from Cu-CO system (in $2\times2$ supercell for DCD).
- `cu_in_cuh_abs/`: Static run of frozen Cu slab fragment alone from Cu-H system (in $2\times2$ supercell for DCD).
- `h_in_cuh_abs/`: Static run of frozen $\text{*H}$ adsorbate fragment alone (in $2\times2$ supercell for DCD).
- `co_in_cuco_abs/`: Static run of frozen $\text{*CO}$ adsorbate fragment alone (in $2\times2$ supercell for DCD).

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
$$\gamma = \frac{E_{\text{cu(110) slab}} - N_{\text{atoms}} \cdot E_{\text{bulk per atom}}}{2A}$$

### 2. Adsorption Energies ($E_{\text{ads}}$)
$$E_{\text{ads, H}} = E_{\text{cu-h slab}} - E_{\text{cu(110)slab}} - \frac{1}{2} E_{\text{h2 gas}}$$

$$E_{\text{ads, CO}} = E_{\text{cu-co slab}} - E_{\text{cu(110) slab}} - E_{\text{co gas}}$$

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

## 1. Charge-Density Difference (DCD) Analysis

### 1.1 Mathematical Formulation
$$\Delta\rho = \rho_{\text{adsorbed slab}} - \rho_{\text{clean slab}} - \rho_{\text{adsorbate}}$$

* **$\Delta\rho > 0$ (Yellow isosurface):** Electron accumulation / charge redistribution.
* **$\Delta\rho < 0$ (Cyan/Blue isosurface):** Electron depletion.

### 1.2 Execution via VASPKIT
1. Ensure all 3 static calculations share **identical unit cell boundaries, KPOINTS, and hardcoded FFT grids (`NGXF`, `NGYF`, `NGZF`)**.
2. Run VASPKIT task `314` in terminal:

VASPKIT outputs **`CHGDIFF.vasp`**, which can be loaded directly into VESTA for 3D visualization.

---

## 2. Bader Charge Analysis

### 2.1 Quantities & Formulas
Charge transfer ($\Delta q$) for an atom with $Z$ valence electrons is calculated as:
$$\Delta q = Z - q_{\text{Bader}}$$

* **$Z$:** Valence electron count of the neutral pseudopotential (e.g., $Z_{\text{Cu}} = 11$, $Z_{\text{C}} = 4$, $Z_{\text{O}} = 6$).
* **$q_{\text{Bader}}$:** Integrated electron population read from column `CHARGE` in **`ACF.dat`**.

### 2.2 Physical Interpretation
* **$\Delta q > 0$:** Electron depletion (atom acts as electron donor).
* **$\Delta q < 0$:** Electron accumulation (atom acts as electron acceptor).
* **Adsorption Delta:** Comparing $q_{\text{Bader}}$ of isolated molecules vs. adsorbed species yields net interfacial charge transfer.

---

## 3. COHP & ICOHP Analysis (LOBSTER)

### 3.1 Data Extraction & File Structure (`COHPCAR.lobster`)
Run `lobster` to produce `COHPCAR.lobster`. 
1. **Verify Bond Counting**
   * The number of bonds included in the COHP analysis must match the number of bonds identified in `distance.dat`.
2. **Structure of `COHPCAR.lobster`**

| Column | Description |
| :--- | :--- |
| **Col 1** | Energy ($E - E_{\text{F}}$ in eV) |
| **Col 2** | Average COHP |
| **Col 3** | Average ICOHP |
| **Col 4 / 5** | COHP / ICOHP of Pair 1 |
| **Col 6 / 7** | COHP / ICOHP of Pair 2 |
| ... | ... |

### 3.2 Plotting & Interpretation Principles
1. **Energy–COHP Plotting:** 
   * **X-axis:** Column 1 ($E - E_{\text{F}}$).
   * **Y-axis:** Column 2 (or $-\text{COHP}$ depending on software convention).
   * **Interpretation:** States below $E_{\text{F}}$ ($E < 0$) with positive COHP represent occupied bonding states; states with negative COHP represent occupied antibonding states.
2. **Energy–ICOHP (Bond Strength):**
   * **X-axis:** Column 1 ($E - E_{\text{F}}$).
   * **Y-axis:** Column 3 (Average ICOHP).
   * **Interpretation:** Evaluated at $E_{\text{F}} = 0.00\text{ eV}$. **More negative ICOHP values indicate stronger chemical bonding interactions.**