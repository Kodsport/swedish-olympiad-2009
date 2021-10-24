#!/usr/bin/env bash

. ../../../testdata_tools/gen.sh

use_solution sol.cpp

compile gen_random.py

samplegroup
sample 1

group group1 100
include_group sample
tc c1 gen_random n=100 r=100
tc c2 gen_random n=100 r=2
tc c3 gen_random n=3 r=100
tc c4 gen_random n=1 r=100
