#!/usr/bin/env bash

PPATH=$(realpath ..)
. ../../../testdata_tools/gen.sh

#ulimit -s unlimited

use_solution joshua.cpp

compile gen_rand.py
compile gen_kill_cheese.py
compile gen_kill_2n.py
compile gen_kill_js_gemini2.py

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
tc g2-2 gen_rand n=20 m=100 mode=random max_coord=200
tc g2-3 gen_rand n=20 m=100 mode=random max_coord=200
tc g2-4 gen_rand n=20 m=100 mode=random max_coord=200
tc g2-5 gen_rand n=20 m=100 mode=random max_coord=200

group group3 35
limits maxn=100 maxm=100
include_group group2
tg_manual ../manual_data/m100
tc g3-1 gen_rand n=100 m=100 mode=random max_coord=200
tc g3-2 gen_rand n=100 m=100 mode=random max_coord=200 mode=positive
tc g3-3 gen_rand n=100 m=100 mode=random max_coord=200 zero=1
tc g3-4 gen_rand n=100 m=100 mode=random max_coord=300 zero=1


group group4 30
limits maxn=100
include_group group3
tg_manual ../manual_data/n100
tc g4-rand-1 gen_rand n=100 m=100 mode=random
tc g4-rand-2 gen_rand n=100 m=100 mode=random
tc g4-rand-3 gen_rand n=100 m=1000000 mode=random
tc g4-rand-4 gen_rand n=100 m=1000000 mode=random
tc g4-kill-cheese-1 gen_kill_cheese n=100 m=1000000 mode=kill_cheese_hard seed=1
tc g4-kill-cheese-2 gen_kill_cheese n=100 m=1000000 mode=kill_cheese_hard seed=2
tc g4-kill-cheese-3 gen_kill_cheese n=100 m=1000000 mode=kill_cheese_hard seed=3
tc g4-kill-2n-1 gen_kill_2n n=100 m=1000000
tc g4-kill-2n-2 gen_kill_2n n=100 m=500000
tc g4-kill-2n-3 gen_kill_2n n=100 m=1000000
tc g4-kill-bjs-1 gen_kill_js_gemini2 n=100 m=1000000 mode=kill_bjs seed=1
tc g4-kill-bjs-2 gen_kill_js_gemini2 n=100 m=1000000 mode=kill_bjs seed=2
tc g4-kill-bjs-3 gen_kill_js_gemini2 n=100 m=1000000 mode=kill_bjs seed=3

group group5 20
include_group group1 group4
tg_manual ../manual_data/n300
tc g5-kill-cheese-1 gen_kill_cheese n=300 m=1000000 near=60 far_start=500 far_step=100 mode=kill_cheese
tc g5-kill-cheese-2 gen_kill_cheese n=300 m=1000000 near=50 far_start=1000 far_step=100 mode=kill_cheese
tc g5-kill-cheese-3 gen_kill_cheese n=300 m=1000000 near=75 far_start=500 far_step=50 mode=kill_cheese
tc g5-kill-gemini2-1 gen_kill_js_gemini2 n=300 m=1000000 mode=kill_gemini2 base=1.04 seed=1
tc g5-kill-gemini2-2 gen_kill_js_gemini2 n=300 m=1000000 mode=kill_gemini2 base=1.04 seed=2
tc g5-kill-gemini2-3 gen_kill_js_gemini2 n=300 m=1000000 mode=kill_gemini2 base=1.04 seed=3

