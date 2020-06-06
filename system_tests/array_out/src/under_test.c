#include "under_test.h"
#include "to_mock.h"

int do_something(int value) {
    int result[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    size_t length = to_mock_compute(value, result);
    int sum = 0;
    for (size_t i = 0; i < length; i++) {
        sum += result[i];
    }
    return sum;
}