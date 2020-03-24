#include "something.h"
#include "complex.h"

int do_something(int i) {
    int y = 0;

    if (complex_computation(i, &y) != COMPLEX_ERR_OK) {
        return 0;
    } else {
        return y;
    }
}
