#include "validator.h"

const int MAX_N = 255;
const int MAX_VAL = 255;
const int MAX_STEPS = 1e5;

const vector<string> NAMES = {"CONST", "ADD", "SUB", "JNZ", "INPUT", "OUTPUT", "HALT"};
const vector<int> ARITY     = {2,       2,     2,     2,     1,       1,        0};
enum { CONST, ADD, SUB, JNZ, INPUT, OUTPUT, HALT };

void run() {
	bool noJnz = Arg("no_jnz", 0);

	int n = Int(1, MAX_N); Endl();

	vector<int> op(n), parX(n), parY(n);
	for (int i = 0; i < n; i++) {
		string name = Word();
		int j = (int)(find(NAMES.begin(), NAMES.end(), name) - NAMES.begin());
		if (j == (int)NAMES.size()) die_line("unknown instruction \"" + name + "\"");
		if (j == JNZ && noJnz) die_line("JNZ is not allowed in this group");
		op[i] = j;
		if (ARITY[j] >= 1) { Space(); parX[i] = Int(0, MAX_VAL); }
		if (ARITY[j] >= 2) { Space(); parY[i] = Int(0, MAX_VAL); }
		Endl();
	}

	vector<int> data;
	while (_peek1() != -1) {
		data.push_back(Int(0, MAX_VAL));
		Endl();
	}

	// Instruction N-1 must be HALT or a JNZ to an earlier instruction.
	if (!(op[n - 1] == HALT || (op[n - 1] == JNZ && parY[n - 1] < n - 1)))
		die("instruction N-1 is neither HALT nor a JNZ to an earlier instruction");

	// Simulate to check the remaining statement guarantees.
	vector<int> reg(256, 0);
	int pc = 0, steps = 0;
	size_t inptr = 0;
	while (op[pc] != HALT) {
		if (++steps > MAX_STEPS) die("program executes more than 10^5 instructions");
		int x = parX[pc], y = parY[pc];
		switch (op[pc]) {
			case CONST:
				reg[y] = x;
				break;
			case ADD:
				reg[y] += reg[x];
				if (reg[y] > MAX_VAL) die("ADD at instruction " + to_string(pc) + " gives sum > 255");
				break;
			case SUB:
				reg[y] -= reg[x];
				if (reg[y] < 0) die("SUB at instruction " + to_string(pc) + " gives result < 0");
				break;
			case JNZ:
				if (reg[x] != 0) {
					pc = y;
					if (pc >= n) die("JNZ jumps to instruction " + to_string(y) + " >= N");
					continue;
				}
				break;
			case INPUT:
				if (inptr == data.size()) die("program runs out of DSP input data");
				reg[x] = data[inptr++];
				break;
			case OUTPUT:
				break;
		}
		pc++;
		if (pc >= n) die("program runs past instruction N-1 without halting");
	}
}
