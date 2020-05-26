#include "under_test.h"
#include "to_mock.h"

int do_something(int value) {
    int result = 0;
    to_mock_compute(value, &result);
    return result;
}