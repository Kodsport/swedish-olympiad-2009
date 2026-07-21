#!/usr/bin/env bash

PPATH=$(realpath ..)
. ../../../testdata_tools/gen.sh

#ulimit -s unlimited

use_solution exact.cpp

compile gen_rand.py

samplegroup
limits noswitch=0
sample 1

group group1 33
limits noswitch=1
tc_manual ../manual_tests/t2.in
tc_manual ../manual_tests/t4.in
for i in {1..3}; do
    tc g1-$i gen_rand mode=noswitch
done

group group2 67
limits noswitch=0
include_group sample group1
tc_manual ../manual_tests/t1.in
tc_manual ../manual_tests/t3.in
tc_manual ../manual_tests/t5.in
tc_manual ../manual_tests/t6.in
for i in {1..7}; do
    tc g2-$i gen_rand mode=random
done
