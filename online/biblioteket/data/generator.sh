#!/usr/bin/env bash

PPATH=$(realpath ..)
. ../../../testdata_tools/gen.sh

ulimit -s unlimited

use_solution gemini.py

compile gen_edge.py

samplegroup
sample sample01

group group1 30
limits maxk=1
tg_manual ../manual/kone
tc g1-allpos gen_edge mode=onesided sign=pos n=100 k=1
tc g1-allneg gen_edge mode=onesided sign=neg n=100 k=1
tc g1-zeros gen_edge mode=zeros n=100 nzero=60 k=1
tc g1-single gen_edge mode=minimal v=-1000 k=1

group group2 70
include_group sample group1
tg_manual ../manual/full
tc g2-allpos gen_edge mode=onesided sign=pos n=100 k=7
tc g2-allneg gen_edge mode=onesided sign=neg n=100 k=3
tc g2-onetrip-side gen_edge mode=onesided sign=pos n=100 k=100
tc g2-antinearest-pos gen_edge mode=antinearest npos=43 nneg=36 k=7 farside=pos
tc g2-antinearest-neg gen_edge mode=antinearest npos=29 nneg=22 k=5 farside=neg
tc g2-singletrip gen_edge mode=singletrip n=9 k=100
tc g2-zeros gen_edge mode=zeros n=100 nzero=50 k=4
tc g2-single gen_edge mode=minimal v=1000 k=100
