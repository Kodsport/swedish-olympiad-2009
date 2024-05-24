#!/usr/bin/env bash
. ../../../testdata_tools/gen.sh


use_solution joshua.cpp

samplegroup
sample sample01

group group1 40
tc_manual dsp_j1
tc_manual dsp2

group group2 60
include_group sample
include_group group1
tc_manual dsp1
tc_manual dsp3
tc_manual dsp4
tc_manual dsp5
