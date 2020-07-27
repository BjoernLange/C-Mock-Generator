#ifndef __TO_MOCK_H__
#define __TO_MOCK_H__

#include <stddef.h>

typedef struct my_struct {
    int a;
    short b;
} my_struct_t;

/**
 * Gets a value.
 */
int to_mock_do(my_struct_t * y);

/**
 * Gets a value with copy.
 */
int to_mock_do_copy(my_struct_t y);

#endif