#include "validator.h"

void run() {
    bool noswitch = Arg("noswitch");

    int h = Int(1, 25); Space();
    int p = Int(1, 200); Endl();
    Eof();

    for (int d = 1;; ++d) {
        double c1 = (d * h + 999) / 1000 * 5 + p * 60 * d * h / 100000.0;
        double c2 = 60 + p * 11 * d * h / 100000.0;
        if (c1 > c2) {
            assert(d * h <= 1000 || !noswitch);
            break;
        }
    }
}
