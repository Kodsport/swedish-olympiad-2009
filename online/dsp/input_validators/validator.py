#!/usr/bin/python3
import re
import sys

int_pat = "(0|[1-9][0-9]*)"
inp1_re = "^"+int_pat+"$"
inp2_re = "^\S+( \S+)*$"

commands = {
		"CONST": 2,
		"ADD": 2,
		"SUB": 2,
		"JNZ": 2,
		"INPUT": 1,
		"OUTPUT": 1,
		"HALT": 0
}

line = sys.stdin.readline()
assert re.match(inp1_re, line)
n = int(line)
assert 0 < n < 256

for i in range(n):
	line = sys.stdin.readline()
	assert re.match(inp2_re, line)
	cmds = line.split()
	assert cmds[0] in commands
	params = commands[cmds[0]]
	assert len(cmds) == params + 1
	for j in range(params):
		assert re.match(int_pat, cmds[j+1])
		d = int(cmds[j+1])
		assert 0 <= d <= 255

while True:
	line = sys.stdin.readline()
	if len(line) == 0:
		break
	assert re.match(int_pat, line)
	d = int(line)
	assert 0 <= d <= 255
sys.exit(42)
