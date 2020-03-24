#ifndef __COMPLEX_H__
#define __COMPLEX_H__

#include <stddef.h>

typedef enum {
    COMPLEX_ERR_OK = 0,
    COMPLEX_ERR_FAIL,
} complex_err_t;

/**
 * Performs a complex computation.
 * @param[in] input The input value.
 * @param[out] output count outputs.
 * @return An error code.
 */
complex_err_t complex_computation(int input, int * output);

#endif