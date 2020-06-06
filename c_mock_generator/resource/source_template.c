<<<IF has_include_path>>>
#include "<<<include_path>>>/<<<name>>>.h"
<<<ENDIF>>>
<<<IF has_no_include_path>>>
#include "<<<name>>>.h"
<<<ENDIF>>>
#include <gtest/gtest.h>

<<<FORALL methods>>>
typedef struct <<<identifier>>>_mocked_call <<<identifier>>>_mocked_call_t;
struct <<<identifier>>>_mocked_call {
    <<<FORALL parameters>>>
    <<<IF is_output>>>
    bool has_<<<identifier>>>;
    size_t <<<identifier>>>_length;
    <<<ENDIF>>>
    <<<type>>> <<<identifier>>>;
    <<<ENDFORALL>>>
    bool is_mock_complete;
    <<<IF has_not_void_return_type>>>
    <<<return_struct_type>>> return_value;
    <<<ENDIF>>>
    <<<identifier>>>_mocked_call_t * next;
};

<<<identifier>>>_mocked_call_t * <<<identifier>>>_mocked_calls;
<<<identifier>>>_mocked_call_t * <<<identifier>>>_ongoing_mocking;

<<<FORALL parameters>>>
<<<IF is_output>>>
static <<<method_identifier>>>_thens_t * <<<method_identifier>>>_then_provide_<<<identifier>>>(<<<type>>>, size_t);
<<<ENDIF>>>
<<<ENDFORALL>>>
<<<IF has_void_return_type>>>
static void <<<identifier>>>_then_return(void);
<<<ENDIF>>>
<<<IF has_not_void_return_type>>>
static void <<<identifier>>>_then_return(<<<return_type>>>);
<<<ENDIF>>>

<<<identifier>>>_thens_t <<<identifier>>>_thens = {
    <<<FORALL parameters>>>
    <<<IF is_output>>>
    .then_provide_<<<identifier>>> = &<<<method_identifier>>>_then_provide_<<<identifier>>>,
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    .then_return = &<<<identifier>>>_then_return,
};

static void <<<identifier>>>_verify_last_mock_completed(void) {
    if (<<<identifier>>>_ongoing_mocking != NULL) {
        EXPECT_EQ(true, <<<identifier>>>_ongoing_mocking->is_mock_complete);
    }
}

static <<<identifier>>>_mocked_call_t * <<<identifier>>>_mocked_call_create(
        <<<FORALL parameters JOINING , >>>
        <<<IF is_input>>>
        <<<type>>> <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        ) {
    <<<identifier>>>_mocked_call_t * mocked_call = (<<<identifier>>>_mocked_call_t *) malloc(sizeof(<<<identifier>>>_mocked_call_t));
    EXPECT_TRUE(mocked_call != NULL);

    <<<FORALL parameters>>>
    <<<IF is_input>>>
    mocked_call-><<<identifier>>> = <<<identifier>>>;
    <<<ENDIF>>>
    <<<IF is_output>>>
    mocked_call-><<<identifier>>> = NULL;
    mocked_call->has_<<<identifier>>> = false;
    mocked_call-><<<identifier>>>_length = 0;
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    mocked_call->is_mock_complete = false;
    mocked_call->next = NULL;

    return mocked_call;
}

static void <<<identifier>>>_mocked_calls_append(<<<identifier>>>_mocked_call_t * mocked_call) {
    if (<<<identifier>>>_mocked_calls == NULL) {
        <<<identifier>>>_mocked_calls = mocked_call;
    } else {
        <<<identifier>>>_mocked_call_t * iterator = <<<identifier>>>_mocked_calls;
        while (iterator->next != NULL ) {
            iterator = iterator->next;
        }
        iterator->next = mocked_call;
    }
}

<<<identifier>>>_thens_t * when_<<<identifier>>>(
        <<<FORALL parameters JOINING , >>>
        <<<IF is_input>>>
        <<<type>>> <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        ) {
    <<<identifier>>>_verify_last_mock_completed();

    <<<identifier>>>_mocked_call_t * mocked_call = <<<identifier>>>_mocked_call_create(
        <<<FORALL parameters JOINING , >>>
        <<<IF is_input>>>
        <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        );
    <<<identifier>>>_mocked_calls_append(mocked_call);

    <<<identifier>>>_ongoing_mocking = mocked_call;

    return &<<<identifier>>>_thens;
}

<<<FORALL parameters>>>
<<<IF is_output>>>
static <<<method_identifier>>>_thens_t * <<<method_identifier>>>_then_provide_<<<identifier>>>(<<<type>>> <<<identifier>>>, size_t <<<identifier>>>_length) {
    <<<method_identifier>>>_ongoing_mocking-><<<identifier>>> = <<<identifier>>>;
    <<<method_identifier>>>_ongoing_mocking->has_<<<identifier>>> = true;
    <<<method_identifier>>>_ongoing_mocking-><<<identifier>>>_length = <<<identifier>>>_length;

    return &<<<method_identifier>>>_thens;
}

<<<ENDIF>>>
<<<ENDFORALL>>>
<<<IF has_void_return_type>>>
static void <<<identifier>>>_then_return(void) {
<<<ENDIF>>>
<<<IF has_not_void_return_type>>>
static void <<<identifier>>>_then_return(<<<return_type>>> return_value) {
    <<<identifier>>>_ongoing_mocking->return_value = return_value;
<<<ENDIF>>>
    <<<identifier>>>_ongoing_mocking->is_mock_complete = true;
}

static void <<<identifier>>>_mocked_calls_free(void) {
    <<<identifier>>>_mocked_call_t * iterator = <<<identifier>>>_mocked_calls;
    while (iterator != NULL) {
        <<<identifier>>>_mocked_call_t * next = iterator->next;
        free(iterator);
        iterator = next;
    }
}

<<<IF has_input_parameters>>>
static bool <<<identifier>>>_mocked_call_matches_input(
        <<<identifier>>>_mocked_call_t * mocked_call,
        <<<FORALL parameters JOINING , >>>
        <<<IF is_input>>>
        <<<type>>> <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        ) {
    <<<FORALL parameters>>>
    <<<IF is_input>>>
    <<<IF is_included>>>
    <<<IF has_simple_type>>>
    if (mocked_call-><<<identifier>>> != <<<identifier>>>) {
        return false;
    }
    <<<ENDIF>>>
    <<<IF has_pointer_type>>>
    <<<IF is_single_element>>>
    if (*(mocked_call-><<<identifier>>>) != *(<<<identifier>>>)) {
        return false;
    }
    <<<ENDIF>>>
    <<<IF has_fixed_length>>>
    if (memcmp(mocked_call-><<<identifier>>>, <<<identifier>>>, <<<fixed_length>>>)) {
        return false;
    }
    <<<ENDIF>>>
    <<<IF is_null_terminated>>>
    <<<IF has_c_string_type>>>
    if (strcmp(mocked_call-><<<identifier>>>, <<<identifier>>>)) {
        return false;
    }
    <<<ENDIF>>>
    <<<IF has_utf8_string_type>>>
    if (wcscmp(mocked_call-><<<identifier>>>, <<<identifier>>>)) {
        return false;
    }
    <<<ENDIF>>>
    <<<IF has_no_string_type>>>
    {
        uint mocked_length = 0;
        for (; mocked_call-><<<identifier>>>[mocked_length] != '\0'; mocked_length++);
        uint param_length = 0;
        for (; <<<identifier>>>[param_length] != '\0'; param_length++);
        if (mocked_length != param_length) {
            return false;
        }

        if (memcmp(mocked_call-><<<identifier>>>, <<<identifier>>>, mocked_length)) {
            return false;
        }
    }
    <<<ENDIF>>>
    <<<ENDIF>>>
    <<<IF has_length_descriptor>>>
    if (mocked_call-><<<length_descriptor>>> != <<<length_descriptor>>>) {
        return false;
    }
    if (memcmp(mocked_call-><<<identifier>>>, <<<identifier>>>, <<<length_descriptor>>>)) {
        return false;
    }
    <<<ENDIF>>>
    <<<ENDIF>>>
    <<<ENDIF>>>
    <<<ENDIF>>>
    <<<ENDFORALL>>>

    return true;
}
<<<ENDIF>>>
<<<IF has_no_input_parameters>>>
static bool <<<identifier>>>_mocked_call_matches_input(<<<identifier>>>_mocked_call_t * mocked_call) {
    return true;
}
<<<ENDIF>>>

static <<<identifier>>>_mocked_call_t * <<<identifier>>>_mocked_calls_find_matching(
        <<<FORALL parameters JOINING , >>>
        <<<IF is_input>>>
        <<<type>>> <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        ) {
    <<<identifier>>>_mocked_call_t * iterator = <<<identifier>>>_mocked_calls;
    while (iterator != NULL) {
        <<<IF has_input_parameters>>>
        if (<<<identifier>>>_mocked_call_matches_input(iterator,
                <<<FORALL parameters JOINING , >>>
                <<<IF is_input>>>
                <<<identifier>>>
                <<<ENDIF>>>
                <<<ENDFORALL>>>
                )) {
            return iterator;
        }
        <<<ENDIF>>>
        <<<IF has_no_input_parameters>>>
        if (<<<identifier>>>_mocked_call_matches_input(iterator)) {
            return iterator;
        }
        <<<ENDIF>>>

        iterator = iterator->next;
    }
    return NULL;
}

<<<return_type>>> <<<identifier>>>(
        <<<FORALL parameters JOINING , >>>
        <<<type>>> <<<identifier>>>
        <<<ENDFORALL>>>
        ) {
    <<<identifier>>>_mocked_call_t * matching_call = <<<identifier>>>_mocked_calls_find_matching(
        <<<FORALL parameters JOINING , >>>
        <<<IF is_input>>>
        <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        );
    EXPECT_TRUE(matching_call != NULL);
    <<<FORALL parameters>>>
    <<<IF is_output>>>
    if (matching_call->has_<<<identifier>>>) {
        memcpy(<<<identifier>>>, matching_call-><<<identifier>>>, sizeof(<<<size_type>>>) * matching_call-><<<identifier>>>_length);
    }
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    <<<IF has_not_void_return_type>>>
    return matching_call->return_value;
    <<<ENDIF>>>
}

<<<ENDFORALL>>>
void mock_<<<name>>>_set_up(void) {
    <<<FORALL methods JOINING <newline><newline>>>>
    <<<identifier>>>_mocked_calls = NULL;
    <<<identifier>>>_ongoing_mocking = NULL;
    <<<ENDFORALL>>>
}

void mock_<<<name>>>_tear_down(void) {
    <<<FORALL methods>>>
    <<<identifier>>>_mocked_calls_free();
    <<<ENDFORALL>>>
}