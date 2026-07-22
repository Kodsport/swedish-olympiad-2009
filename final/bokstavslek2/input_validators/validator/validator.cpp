#include "validator.h"

const int MAX_N = 40000;

void run() {
	int n = Int(1, MAX_N);
	Endl();
	
	string last;
	for (int i = 0; i < n; i++) {
		string word = Word();
		Endl();
		assert(word.size() >= 1);
		assert(word.size() <= 20);
		for (char c : word) {
			assert(c >= 'A' && c <= 'Z');
		}
		if (!last.empty()) {
			assert(word > last);
		}
		last = word;
	}
}
