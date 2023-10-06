#!/bin/bash -l
#PBS -N 3f
#PBS -j eo
#PBS -q gpu
#PBS -l nodes=1:ppn=1:gpus=1
#PBS -l walltime=72:00:00

cd $PBS_O_WORKDIR

##############################################################################################

pmemd.cuda -O -i $PWD/min1.in -o min1.out -p com_solv.top -c com_solv.crd  -r min1.rst -ref com_solv.crd
pmemd.cuda -O -i $PWD/min2.in -o min2.out -p com_solv.top -c min1.rst -r min2.rst 
pmemd.cuda -O -i $PWD/heat.in  -o heat.out  -p com_solv.top -c min2.rst -r heat.rst  -ref min2.rst -x heat.nc
pmemd.cuda -O -i $PWD/equil.in  -o equil.out  -p com_solv.top -c heat.rst  -r equil.rst -ref heat.rst -x equil.nc
pmemd.cuda -O -i $PWD/prod.in  -o prod.out  -p com_solv.top -c equil.rst  -r prod.rst  -x prod.nc

###############################################################################

