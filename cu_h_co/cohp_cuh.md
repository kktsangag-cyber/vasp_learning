# Static Calculations

POSCAR = CONTCAR from optimisation

KPOINTS and POTCAR remain the same

INCAR = {
    ISTART  = 0
    ICHARG  = 2

    ISYM    = -1          # Must be -1 or 0

    ENCUT   = xxxx        # Determined from convergence tests
    PREC    = Accurate

    ISMEAR  = -5
    NELM    = 100
    NELMIN  = 2
    EDIFF   = 1E-8

    IBRION  = -1
    ISIF    = 0
    NSW     = 0           # Static calculations

    ISPIN   = 2          

    LREAL   = .FALSE.

    NBANDS  = 200         # Use sufficiently large NBANDS

    LWAVE   = .TRUE.      # Required for COHP Analysis

    NPAR    = 4

    NEDOS   = 2000
    LORBIT  = 12
}

# get_bond_total.py
distance.dat generated using POSCAR(before relaxation)
(CONTCAR->POSCAR(relaxed) should be used if VASP)

# get_cohpfile.py [initial_energy] [final_energy] [element1] [element2] [min_distance] [max_distance]

Cu_H_1.9_2.1
get_cohpfile.py -e -20 10 \
-s Cu H \
-z Cu:3d,4s H:1s \              # match with POTCAR
-d 1.9 2.1 \                    # minimum in distance.dat +- 0.1
-m 5

# Run LOBSTER using lobsterin

# Result Analysis