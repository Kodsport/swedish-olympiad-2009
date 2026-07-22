#!/usr/bin/env bash
. ../../../testdata_tools/gen.sh


use_solution joshua.cpp
compile gen_letter_traps.py

samplegroup
sample sample1

group group1 100
include_group sample
tg_manual ../manual_data
tc letter-traps gen_letter_traps n=40000
