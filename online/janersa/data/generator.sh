#!/usr/bin/env bash
. ../../../testdata_tools/gen.sh


use_solution joshua.cpp

compile gen_strong.py

samplegroup
sample janersa0

group group1 30
limits n=25 m=75
include_group sample
tc g1-random gen_strong mode=random n=25 m=75
tc g1-banded gen_strong mode=banded n=25 m=75
tc g1-antisweep gen_strong mode=antisweep n=24 m=24
tc g1-tiny gen_strong mode=random n=2 m=1
tg_manual ../manual_data/g1

group group2 70
include_group group1
tc g2-random-a gen_strong mode=random n=700 m=2000
tc g2-random-b gen_strong mode=random n=700 m=2000
tc g2-banded gen_strong mode=banded n=700 m=2000
tc g2-clustered gen_strong mode=clustered n=700 m=2000
tc g2-antisweep-a gen_strong mode=antisweep n=700 m=700
tc g2-antisweep-b gen_strong mode=antisweep n=700 m=700
tc g2-path gen_strong mode=path n=700 m=699
tg_manual ../manual_data/g2
