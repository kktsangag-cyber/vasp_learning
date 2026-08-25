# SCF Calculations

POSCAR = CONTCAR from optimisation

KPOINTS and POTCAR remain the same

INCAR = {
    ...
    LAECHG = .TRUE.         # Generate AECCAR0 and AECCAR2 (core and valence energy density)
    LCHARG = .TRUE.

    NSW    = 0              # Disable ionic relaxation
    IBRION = -1             # Optional
    ...
}

# Generate CHGCAR_sum
chgsum.pl AECCAR0 AECCAR2

# Bader partitioning
bader CHGCAR -ref CHGCAR_sum

# Use ACF.dat for charge transfer analysis

The process are the same for those Cu-CO and Cu-H systems.