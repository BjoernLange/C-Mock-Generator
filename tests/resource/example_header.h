#ifndef __EXAMPLE_HEADER_H__
#define __EXAMPLE_HEADER_H__

#include "another_example.h"

typedef enum {
    EX_ERR_OK = 0,
    EX_ERR_FAIL,
} ex_err_t;

/**
 * Initializes the example.
 * @return {@code EX_ERR_OK} if successful. Otherwise {@code EX_ERR_FAIL}.
 */
ex_err_t ex_init(void);

/**
 * Does something with ints.
 * @param i Some input parameter.
 * @param[out] j Some output parameter.
 * @return {@code EX_ERR_OK} if no error occurred.
 *         Otherwise {@code EX_ERR_FAIL}.
 */
ex_err_t ex_do_something(int i, int* j);

#endif