#ifndef __TO_MOCK_H__
#define __TO_MOCK_H__

#include <stddef.h>

/**
 * Computes something.
 * @param[in] value Some value.
 * @param[out] result Some result.
 * @return length of result.
 */
size_t to_mock_compute(int value, int * result);

#endif