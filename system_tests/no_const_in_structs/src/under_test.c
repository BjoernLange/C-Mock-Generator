#include "under_test.h"
#include "to_mock.h"

int do_something(int value) {
    return to_mock_do(&value);
}