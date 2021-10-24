#!/usr/bin/env bash

PPATH=$(realpath ..)
REQUIRE_SAMPLE_REUSE=0
. ../../../../testdata_tools/gen.sh

ulimit -s unlimited

use_solution biblioteket.cpp

samplegroup
sample sample01

group group1 30
limits maxk=1
tc_manual ../manual/kone1.in
tc_manual ../manual/kone2.in
tc_manual ../manual/kone3.in
tc_manual ../manual/kone4.in
tc_manual ../manual/kone5.in

group group2 70
include_group sample
include_group group1
tc_manual ../manual/biblioteket1.in
tc_manual ../manual/biblioteket2.in
tc_manual ../manual/biblioteket3.in
tc_manual ../manual/biblioteket4.in
tc_manual ../manual/biblioteket5.in
