# Generate the supercell
phonopy-init -d --dim="5 5 1" -c POSCAR         # CONTCAR should be used
-> SPOSCAR / POSCAR-001, POSCAR-002, ...

# Method 1: Density Functional Perturbation Theory (DFPT)
INCAR = {
    SYSTEM = Phonon

    PREC = Accurate
    ENCUT = 500

    ISTART = 0
    ICHARG = 2
    ISPIN = 1

    NELM = 60
    NELMIN = 4
    NELMDL = -3
    EDIFF = 1E-7

    IALGO = 38
    ADDGRID = .TRUE.
    LREAL = .FALSE.

    NSW = 1                         # DFPT requires 1 ionic step
    IBRION = 8                      # Activates the DFPT phonon calculation

    EDIFFG = -1E-7

    ISMEAR = 0
    SIGMA = 0.01

    SYMPREC = 1E-6
}

Convergence tests for ENCUT, PREC, EDIFF, KPOINTS, and parallelization parameters (e.g., NCORE) are recommended
SYMPREC = 1E-6 is recommended to avoid symmetry-related errors

KPOINTS: The k-point mesh should be tested for convergence. Higher-density meshes (e.g., 3×3×1 or 4×4×1) generally improve accuracy if computational resources permit.

## Run VASP

## Prepare band.conf

## Generate Force Constants and Phonon Dispersion
phonopy --fc vasprun.xml
phonopy --dim="5 5 1" -c POSCAR-unitcell band.conf
phonopy-bandplot --gnuplot > 551.dat
-> FORCE_CONSTANTS(second-order force constant matrix), 551.dat(phonon dispersion data)

# Method 2: Finite Displacement Method
For every generated displacement structure (POSCAR-00*), create an independent calculation directory and copy the file.
Rename it as POSCAR.
INCAR, POSCAR, KPOINTS and POTCAR should be included.

INCAR = {
    SYSTEM = Phonon

    PREC = Accurate
    ENCUT = 500

    ISTART = 0
    ICHARG = 2
    ISPIN = 1

    NELM = 60
    NELMIN = 4
    NELMDL = -3
    EDIFF = 1E-7

    IALGO = 38
    ADDGRID = .TRUE.
    LREAL = .FALSE.

    NSW = 0                         # No ionic step for this method
    IBRION = -1

    EDIFFG = -1E-7

    ISMEAR = 0
    SIGMA = 0.01
}

Remove non-ASCII characters and inline comments from the input files to avoid parsing errors.

KPOINTS: A denser mesh (e.g., 2×2×1) can be used if computational resources allow. The same k-point mesh should be maintained ***consistently*** in subsequent force-constant calculations.

## Run All Displacement Calculations
Copy each vasprun.xml into the parent directory and rename them as vasprun.xml-001, vasprun.xml-002, ...

## Prepare band.conf
extra line: FORCE_CONSTANTS = WRITE

## Generate Force Constants and Phonon Dispersion
phonopy --fc vasprun.xml
phonopy --dim="5 5 1" -c POSCAR-unitcell band.conf
phonopy-bandplot --gnuplot > 551.dat
-> FORCE_CONSTANTS(second-order force constant matrix), 551.dat(phonon dispersion data)

# Recommendations
Density Functional Perturbation Theory (DFPT) (recommended for small systems)
Finite Displacement Method (recommended for large systems and compatible with most post-processing workflows)

Verify convergence with respect to:
supercell size,
plane-wave cutoff (ENCUT),
k-point sampling,
electronic convergence (EDIFF)