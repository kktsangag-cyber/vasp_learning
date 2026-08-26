# Self-consistent Calculations for Insulators/Semiconductors/Metals

POSCAR = CONTCAR from optimisation

KPOINTS and POTCAR remain the same

INCAR = {
    ...
    LCHARG = .TRUE.             # Get the CHGCAR for DOS calculations
    LWAVE = .TRUE.              # Get the WAVECAR for DOS calculations
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
    ISTART = 1                  # Read the WAVECAR from SCF Calculations
    ICHARG = 11                 # Read the CHGCAR from SCF Calculations
    NSW = 0
    IBRION = -1
    ISMEAR = 0                  # For insulators and semiconductors, ISMEAR = -5
    SIGMA = 0.02                # For metals, ISMEAR = 1 ; SIGMA = 0.05
    # ISMEAR = 0 ; SIGMA = 0.02 is used for gases

    LORBIT = 11
    NEDOS  = 6000
    ...
}

Usually, a new KPOINT with desnser k-point mesh should be used

# DOS Analysis
[zjb@op 3-nscf]$ split_dos
-> get DOS0(total DOS), DOS1(projected DOS of first atom) and DOS2(projected DOS of second atom)

# Plot graph
dosplot.pl DOS0 

For spin-polarized calculations (ISPIN = 2), the DOS files contain separate spin-up and spin-down contributions.