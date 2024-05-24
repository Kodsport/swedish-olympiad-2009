#!/usr/bin/env bash
. ../../../testdata_tools/gen.sh


use_solution joshua.cpp

samplegroup
sample sample1

group group1 100
include_group sample
tc_manual secret1
tc_manual secret2
tc_manual secret3
tc_manual secret4
tc_manual secret5
