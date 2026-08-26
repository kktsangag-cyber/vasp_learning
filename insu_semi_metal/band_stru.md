# Self-consistent Calculations for Insulators/Semiconductors/Metals

POSCAR = CONTCAR from optimisation

KPOINTS and POTCAR remain the same

INCAR = {
    ...
    LCHARG = .TRUE.             # Get the CHGCAR for band structure calculations
    NSW = 0
    IBRION = -1
    ISMEAR = -5                 # For metallic systems, ISMEAR = 1 ; SIGMA = 0.2
    ...
}

# Non-self-consistent Calculations for Insulators/Semiconductors/Metals

POSCAR = CONTCAR from optimisation

POTCAR remains the same

INCAR = {
    ...
    ICHARG = 11                  # Read the CHGCAR from SCF Calculations
    NSW = 0
    IBRION = -1
    ISMEAR = 0                   # For metallic systems, ISMEAR = 1
    SIGMA = 0.1                  # For metallic systems, SIGMA = 0.2
    LORBIT = 11
    ...
}

A new KPOINT(KPOINTS_PBE_bands, 1D line mode) should be used