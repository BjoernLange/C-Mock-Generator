#ifndef __TO_MOCK_H__
#define __TO_MOCK_H__

#include <stddef.h>

typedef enum {
    TO_MOCK_ERR_OK = 0,
    TO_MOCK_ERR_FAIL,
} to_mock_err_t;

/**
 * Performs a computation.
 * @param[in, fixed-length=2] input 2 input values.
 * @param[out] output The output.
 * @return An error code.
 */
to_mock_err_t to_mock_compute_fixed_size(int * input, int * output);

/**
 * Performs a computation.
 * @param[in, null-terminated] input Input values.
 * @param[out] output The output.
 * @return An error code.
 */
to_mock_err_t to_mock_compute_null_terminated(char * input, int * output);

/**
 * Performs a computation.
 * @param[in, null-terminated] input1 Input values.
 * @param[in, null-terminated] input2 More input values.
 * @param[out] output The output.
 * @return An error code.
 */
to_mock_err_t to_mock_compute_null_terminated_twice(char * input1, int * input2, int * output);

/**
 * Performs a computation.
 * @param[in, length-descriptor=size] input Input values.
 * @param[in] size Size of input.
 * @param[out] output The output.
 * @return An error code.
 */
to_mock_err_t to_mock_compute_length_described(int * input, size_t size, int * output);

/**
 * Performs a computation.
 * @param[in, null-terminated] input Input values.
 * @param[out] output The output.
 * @return An error code.
 */
to_mock_err_t to_mock_compute_utf8(wchar_t * input, int * output);

#endif