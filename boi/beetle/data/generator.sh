#!/usr/bin/env bash

PPATH=$(realpath ..)
. ../../../testdata_tools/gen.sh

#ulimit -s unlimited

use_solution joshua.cpp

compile gen_rand.py
compile gen_kill_cheese.py

samplegroup
sample 1


group group1 5
limits nonnegative=1
tc g1-1 gen_rand n=300 m=1000000 mode=positive
tc g1-2 gen_rand n=300 m=1000000 mode=positive zero=1

group group2 10
limits maxn=20 maxm=100
include_group sample
tg_manual ../manual_data/n20
tc g2-1 gen_rand n=5 m=3 mode=random
tc g2-2 gen_rand n=20 m=100 mode=random
tc g2-3 gen_rand n=20 m=100 mode=random
tc g2-4 gen_rand n=20 m=100 mode=random
tc g2-5 gen_rand n=20 m=100 mode=random

group group3 35
limits maxn=100 maxm=100
include_group group2
tg_manual ../manual_data/m100
# tc g1-1 gen_rand n=5 m=3 mode=random
# tc g1-2 gen_rand n=20 m=1000 mode=random
# tc g1-3 gen_rand n=20 m=1000 mode=random
# tc g1-4 gen_rand n=20 m=1000 mode=random
# tc g1-5 gen_rand n=20 m=1000 mode=random


group group4 30
limits maxn=100
include_group group3
tg_manual ../manual_data/n100
tc g4-kill-cheese-1 gen_kill_cheese n=100 m=1000000 mode=kill_cheese_hard seed=1
tc g4-kill-cheese-2 gen_kill_cheese n=100 m=1000000 mode=kill_cheese_hard seed=2
tc g4-kill-cheese-3 gen_kill_cheese n=100 m=1000000 mode=kill_cheese_hard seed=3

group group5 20
include_group group1 group4
tg_manual ../manual_data/n300
tc g5-kill-cheese-1 gen_kill_cheese n=300 m=1000000 near=60 far_start=500 far_step=100 mode=kill_cheese
tc g5-kill-cheese-2 gen_kill_cheese n=300 m=1000000 near=50 far_start=1000 far_step=100 mode=kill_cheese
tc g5-kill-cheese-3 gen_kill_cheese n=300 m=1000000 near=75 far_start=500 far_step=50 mode=kill_cheese

