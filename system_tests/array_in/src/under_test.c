#include "under_test.h"
#include "to_mock.h"

int do_something_fixed_size(int i) {
    int y[2] = { i + 2, i + 3 };
    int out = 0;

    if (to_mock_compute_fixed_size(y, &out) != TO_MOCK_ERR_OK) {
        return 0;
    } else {
        return out;
    }
}

int do_something_null_terminated(char first, char second) {
    char y[3] = { first, second, '\0' };
    int out = 0;

    if (to_mock_compute_null_terminated(y, &out) != TO_MOCK_ERR_OK) {
        return 0;
    } else {
        return out;
    }
}

int do_something_null_terminated_twice(char first, int second) {
    char y[2] = { first, '\0' };
    int z[3] = { second, second + 1, '\0' };
    int out = 0;

    if (to_mock_compute_null_terminated_twice(y, z, &out) != TO_MOCK_ERR_OK) {
        return 0;
    } else {
        return out;
    }
}

int do_something_length_described(int first, int second) {
    int z[3] = { second, second + 1, first };
    int out = 0;

    if (to_mock_compute_length_described(z, 3, &out) != TO_MOCK_ERR_OK) {
        return 0;
    } else {
        return out;
    }
}

int do_something_utf8(wchar_t first, wchar_t second) {
    wchar_t z[3] = { first, second, L'\0' };
    int out = 0;

    if (to_mock_compute_utf8(z, &out) != TO_MOCK_ERR_OK) {
        return 0;
    } else {
        return out;
    }
}
