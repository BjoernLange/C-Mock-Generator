#include "under_test.h"
#include "to_mock.h"

int do_something(int a, short b) {
    my_struct_t x = {
        .a = a,
        .b = b
    };

    return to_mock_do(&x);
}


int do_something_copy(int a, short b) {
    my_struct_t x = {
        .a = a,
        .b = b
    };

    return to_mock_do_copy(x);
}
