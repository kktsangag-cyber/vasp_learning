# VASP Learning Folder

## Overview
This repository contains the input files for different VASP calculations.

## What I have learnt
* Foundational quantum mechanical concepts in atomic and electronic structures.
* Formatting and parameter tuning for standard VASP input files: `INCAR`, `POSCAR`, and `KPOINTS`.

Preparing INPUT files for
* Geometric Optimisation (Surface and Absorption Energy Calculations)
* SCF Calculations (Differential Charge Density, Bader and COHP Calculations)
* NSCF Calculations (Band Structures, DOS and Phonon Spectra)

* General understanding of workflow of NEB method, Frequency Analysis and basic molecular-dynamics workflow

## Files
There are three folders: cr_o2, cu_h_co, insu_semi_metal.
Only INPUT files (without POTCAR) for VASP are contained.

**cr_o2**:
* Optimisation of Cr bulk, Cr surface and O2 gas
* Absorption Energy Calculations of Cr-O2 system

**cu_h_co**:
* Surface energy of Cu slab and the adsorption energies of *H and *CO
* Differential Charge Density Calculations
* Baber Calculations
* COHP Analysis

**insu_semi_metal**:
* Band Structure Calculations (KPOINTS for NSCF (k-lines) is not prepared)
* Density of States Calculations (KPOINTS Convergence Test is not performed so KPOINTS is omitted)
* Phonon Calculations (only Diamond POSCAR is treated by Phononpy)
