# Geometric Optimisation

INCAR = {
    ...
    NGXF    = 150         (FFT grid mesh density for nice charge/potential plots)
    NGYF    = 150         (FFT grid mesh density for nice charge/potential plots)
    NGZF    = 180         (FFT grid mesh density for nice charge/potential plots)
    ...
}

FFT mesh parameters should be added in INCAR to ensure identical FFT grids for all subsequent charge-density calculations

# Static Calculations for Absorped Cu-CO system

POSCAR = CONTCAR from optimisation

KPOINTS and POTCAR remain the same

INCAR = {
    ...
    LCHARG = .TRUE.
    NSW = 0
    IBRION = -1
    ...
}

# Static Calculations for Isolated Cu-CO system

[zjb@op cu_co_slab]$ cp INCAR POSCAR POTCAR KPOINTS ../cu_in_cuco_abs/
[zjb@op cu_co_slab]$ cp INCAR POSCAR POTCAR KPOINTS ../co_in_cuco_abs/
remove CO in cu_in_cuco_abs/POSCAR and cu_in_cuco_abs/POTCAR 
remove Cu in co_in_cuco_abs/POSCAR and co_in_cuco_abs/POTCAR

# Use VASPKIT or chgsum.pl for Charge-Density Difference Calculation