#include "validator.h"

const int MAX_N = 100;
const int MAX_K = 100;
const int MAX_COORD = 1000;

void run() {
	int n = Int(1, MAX_N);
	Space();
	int k = Int(1, Arg("maxk", MAX_K));
	Endl();

	for (int i = 0; i < n; i++) {
        Int(-MAX_COORD, MAX_COORD);
		Endl();
	}
}
