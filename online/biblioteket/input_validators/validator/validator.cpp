#include "validator.h"

void run() {
    int maxk = Arg("maxk", 100);
	int n = Int(1, 100);
	Space();
	int k = Int(1, maxk);
	Endl();

	for (int i = 0; i < n; i++) {
        Int(-1000, 1000); Endl();
	}
}
