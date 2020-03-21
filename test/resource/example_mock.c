#include "example_header.h"
#include <gtest/gtest.h>

typedef struct ex_init_mocked_call ex_init_mocked_call_t;
struct ex_init_mocked_call {
    bool has_return_value;
    ex_err_t return_value;
    ex_init_mocked_call_t * next;
};

ex_init_mocked_call_t * ex_init_mocked_calls;
ex_init_mocked_call_t * ex_init_ongoing_mocking;

static void ex_init_then_return(ex_err_t);

ex_init_thens_t ex_init_thens = {
    .then_return = &ex_init_then_return,
};

static void ex_init_verify_last_mock_completed(void) {
    if (ex_init_ongoing_mocking != NULL) {
        EXPECT_EQ(true, ex_init_ongoing_mocking->has_return_value);
    }
}

static ex_init_mocked_call_t * ex_init_mocked_call_create(
        ) {
    ex_init_mocked_call_t * mocked_call = (ex_init_mocked_call_t *) malloc(sizeof(ex_init_mocked_call_t));
    EXPECT_TRUE(mocked_call != NULL);

    mocked_call->has_return_value = false;
    mocked_call->next = NULL;

    return mocked_call;
}

static void ex_init_mocked_calls_append(ex_init_mocked_call_t * mocked_call) {
    if (ex_init_mocked_calls == NULL) {
        ex_init_mocked_calls = mocked_call;
    } else {
        ex_init_mocked_call_t * iterator = ex_init_mocked_calls;
        while (iterator->next != NULL ) {
            iterator = iterator->next;
        }
        iterator->next = mocked_call;
    }
}

ex_init_thens_t * when_ex_init(
        ) {
    ex_init_verify_last_mock_completed();

    ex_init_mocked_call_t * mocked_call = ex_init_mocked_call_create(
        );
    ex_init_mocked_calls_append(mocked_call);

    ex_init_ongoing_mocking = mocked_call;

    return &ex_init_thens;
}

static void ex_init_then_return(ex_err_t return_value) {
    ex_init_ongoing_mocking->return_value = return_value;
    ex_init_ongoing_mocking->has_return_value = true;
}

static void ex_init_mocked_calls_free(void) {
    ex_init_mocked_call_t * iterator = ex_init_mocked_calls;
    while (iterator != NULL) {
        ex_init_mocked_call_t * next = iterator->next;
        free(iterator);
        iterator = next;
    }
}

static bool ex_init_mocked_call_matches_input(ex_init_mocked_call_t * mocked_call) {
    return true;
}

static ex_init_mocked_call_t * ex_init_mocked_calls_find_matching(
        ) {
    ex_init_mocked_call_t * iterator = ex_init_mocked_calls;
    while (iterator != NULL) {
        if (ex_init_mocked_call_matches_input(iterator)) {
            return iterator;
        }

        iterator = iterator->next;
    }
    return NULL;
}

ex_err_t ex_init(
        ) {
    ex_init_mocked_call_t * matching_call = ex_init_mocked_calls_find_matching(
        );
    EXPECT_TRUE(matching_call != NULL);
    return matching_call->return_value;
}

typedef struct ex_do_something_mocked_call ex_do_something_mocked_call_t;
struct ex_do_something_mocked_call {
    int i;
    bool has_j
    int j;
    bool has_return_value;
    ex_err_t return_value;
    ex_do_something_mocked_call_t * next;
};

ex_do_something_mocked_call_t * ex_do_something_mocked_calls;
ex_do_something_mocked_call_t * ex_do_something_ongoing_mocking;

static ex_do_something_thens_t * ex_do_something_then_provide_i(int);
static ex_do_something_thens_t * ex_do_something_then_provide_j(int *);
static void ex_do_something_then_return(ex_err_t);

ex_do_something_thens_t ex_do_something_thens = {
    .then_provide_i = &ex_do_something_then_provide_i,
    .then_provide_j = &ex_do_something_then_provide_j,
    .then_return = &ex_do_something_then_return,
};

static void ex_do_something_verify_last_mock_completed(void) {
    if (ex_do_something_ongoing_mocking != NULL) {
        EXPECT_EQ(true, ex_do_something_ongoing_mocking->has_return_value);
    }
}

static ex_do_something_mocked_call_t * ex_do_something_mocked_call_create(
        int i
        ) {
    ex_do_something_mocked_call_t * mocked_call = (ex_do_something_mocked_call_t *) malloc(sizeof(ex_do_something_mocked_call_t));
    EXPECT_TRUE(mocked_call != NULL);

    mocked_call->i = i;
    mocked_call->has_j = false;
    mocked_call->has_return_value = false;
    mocked_call->next = NULL;

    return mocked_call;
}

static void ex_do_something_mocked_calls_append(ex_do_something_mocked_call_t * mocked_call) {
    if (ex_do_something_mocked_calls == NULL) {
        ex_do_something_mocked_calls = mocked_call;
    } else {
        ex_do_something_mocked_call_t * iterator = ex_do_something_mocked_calls;
        while (iterator->next != NULL ) {
            iterator = iterator->next;
        }
        iterator->next = mocked_call;
    }
}

ex_do_something_thens_t * when_ex_do_something(
        int i
        ) {
    ex_do_something_verify_last_mock_completed();

    ex_do_something_mocked_call_t * mocked_call = ex_do_something_mocked_call_create(
        i
        );
    ex_do_something_mocked_calls_append(mocked_call);

    ex_do_something_ongoing_mocking = mocked_call;

    return &ex_do_something_thens;
}

static ex_do_something_thens_t * ex_do_something_then_provide_j(int * j) {
    memcpy(&ex_do_something_ongoing_mocking->j, j, sizeof(int));
    ex_do_something_ongoing_mocking->has_j = true;

    return &ex_do_something_thens;
}

static void ex_do_something_then_return(ex_err_t return_value) {
    ex_do_something_ongoing_mocking->return_value = return_value;
    ex_do_something_ongoing_mocking->has_return_value = true;
}

static void ex_do_something_mocked_calls_free(void) {
    ex_do_something_mocked_call_t * iterator = ex_do_something_mocked_calls;
    while (iterator != NULL) {
        ex_do_something_mocked_call_t * next = iterator->next;
        free(iterator);
        iterator = next;
    }
}

static bool ex_do_something_mocked_call_matches_input(
        ex_do_something_mocked_call_t * mocked_call,
        int i
        ) {
    return
        mocked_call->i == i
        ;
}

static ex_do_something_mocked_call_t * ex_do_something_mocked_calls_find_matching(
        int i
        ) {
    ex_do_something_mocked_call_t * iterator = ex_do_something_mocked_calls;
    while (iterator != NULL) {
        if (ex_do_something_mocked_call_matches_input(iterator,
                i
                )) {
            return iterator;
        }

        iterator = iterator->next;
    }
    return NULL;
}

ex_err_t ex_do_something(
        int i, int * j
        ) {
    ex_do_something_mocked_call_t * matching_call = ex_do_something_mocked_calls_find_matching(
        i
        );
    EXPECT_TRUE(matching_call != NULL);
    if (matching_call->has_j) {
        memcpy(j, &matching_call->j, sizeof(int));
    }
    return matching_call->return_value;
}

void mock_example_header_set_up(void) {
    ex_init_mocked_calls = NULL;
    ex_init_ongoing_mocking = NULL;

    ex_do_something_mocked_calls = NULL;
    ex_do_something_ongoing_mocking = NULL;
}

void mock_example_header_tear_down(void) {
    ex_init_mocked_calls_free();
    ex_do_something_mocked_calls_free();
}