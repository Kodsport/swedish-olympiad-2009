#!/usr/bin/env bash
. ../../../testdata_tools/gen.sh


use_solution joshua.cpp

samplegroup
sample janersa0

group group1 30
include_group sample
tc_manual janersa1
tc_manual janersa2

group group2 70
include_group group1
tc_manual janersa3
tc_manual janersa4
tc_manual janersa5
