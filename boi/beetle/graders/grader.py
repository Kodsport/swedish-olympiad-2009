#!/usr/bin/python3
import sys

if "ignore" in sys.argv:
	print("AC 0")
else:
	the_score = int(sys.argv[1])
	for line in sys.stdin.readlines():
		verdict, score = line.split()
		if verdict != "AC":
			the_score = 0
	print(f"AC {the_score}")
