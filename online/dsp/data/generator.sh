#!/usr/bin/env bash
. ../../../testdata_tools/gen.sh


use_solution joshua.cpp

compile maxdsp.py pypy

samplegroup
sample sample01

group group1 40
limits no_jnz=1
tg_manual ../manual_data/g1
tc max-straightline maxdsp mode=g1

group group2 60
include_group sample
include_group group1
tg_manual ../manual_data/g2
tc max-steps maxdsp mode=steps
tc max-output maxdsp mode=output
tc max-input maxdsp mode=input
