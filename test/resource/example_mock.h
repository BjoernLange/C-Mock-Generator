#ifndef __EXAMPLE_HEADER_H__
#define __EXAMPLE_HEADER_H__

#include "another_example.h"

typedef enum {
    EX_ERR_OK = 0,
    EX_ERR_FAIL,
} ex_err_t;

typedef struct mock_ex_init_call {
    ex_err_t provided_return_value;
} mock_ex_init_call_t;

typedef struct ex_init_thens ex_init_thens_t;

typedef void (*ex_init_then_return_func)(ex_err_t);
typedef ex_init_then_return_func ex_init_then_return_func_t;

struct ex_init_thens {
    ex_init_then_return_func_t then_return;
};

ex_init_thens_t * when_ex_init(void);

ex_err_t ex_init(void);

typedef struct mock_ex_do_something_call {
    int expected_i;
    int * provided_j;
    ex_err_t provided_return_value;
} mock_ex_do_something_call_t;

typedef struct ex_do_something_thens ex_do_something_thens_t;

typedef ex_do_something_thens_t * (*ex_do_something_then_provide_j_func)(int *);
typedef ex_do_something_then_provide_j_func ex_do_something_then_provide_j_func_t;
typedef void (*ex_do_something_then_return_func)(ex_err_t);
typedef ex_do_something_then_return_func ex_do_something_then_return_func_t;

struct ex_do_something_thens {
    ex_do_something_then_provide_j_func_t then_provide_j;
    ex_do_something_then_return_func_t then_return;
};

ex_do_something_thens_t * when_ex_do_something(
    int i
    );

ex_err_t ex_do_something(
    int i, int * j
    );

void mock_example_header_set_up(void);
void mock_example_header_tear_down(void);

#endif
