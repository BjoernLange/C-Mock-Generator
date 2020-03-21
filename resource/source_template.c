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
    bool has_<<<identifier>>>
    <<<ENDIF>>>
    <<<struct_type>>> <<<identifier>>>;
    <<<ENDFORALL>>>
    bool has_return_value;
    <<<return_struct_type>>> return_value;
    <<<identifier>>>_mocked_call_t * next;
};

<<<identifier>>>_mocked_call_t * <<<identifier>>>_mocked_calls;
<<<identifier>>>_mocked_call_t * <<<identifier>>>_ongoing_mocking;

<<<FORALL parameters>>>
static <<<method_identifier>>>_thens_t * <<<method_identifier>>>_then_provide_<<<identifier>>>(<<<type>>>);
<<<ENDFORALL>>>
static void <<<identifier>>>_then_return(<<<return_type>>>);

<<<identifier>>>_thens_t <<<identifier>>>_thens = {
    <<<FORALL parameters>>>
    .then_provide_<<<identifier>>> = &<<<method_identifier>>>_then_provide_<<<identifier>>>,
    <<<ENDFORALL>>>
    .then_return = &<<<identifier>>>_then_return,
};

static void <<<identifier>>>_verify_last_mock_completed(void) {
    if (<<<identifier>>>_ongoing_mocking != NULL) {
        EXPECT_EQ(true, <<<identifier>>>_ongoing_mocking->has_return_value);
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
    mocked_call->has_<<<identifier>>> = false;
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    mocked_call->has_return_value = false;
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
static <<<method_identifier>>>_thens_t * <<<method_identifier>>>_then_provide_<<<identifier>>>(<<<type>>> <<<identifier>>>) {
    memcpy(&<<<method_identifier>>>_ongoing_mocking-><<<identifier>>>, <<<identifier>>>, sizeof(<<<size_type>>>));
    <<<method_identifier>>>_ongoing_mocking->has_<<<identifier>>> = true;

    return &<<<method_identifier>>>_thens;
}

<<<ENDIF>>>
<<<ENDFORALL>>>
static void <<<identifier>>>_then_return(<<<return_type>>> return_value) {
    <<<identifier>>>_ongoing_mocking->return_value = return_value;
    <<<identifier>>>_ongoing_mocking->has_return_value = true;
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
    return
        <<<FORALL parameters JOINING  && >>>
        <<<IF is_input>>>
        mocked_call-><<<identifier>>> == <<<identifier>>>
        <<<ENDIF>>>
        <<<ENDFORALL>>>
        ;
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
        memcpy(<<<identifier>>>, &matching_call-><<<identifier>>>, sizeof(<<<size_type>>>));
    }
    <<<ENDIF>>>
    <<<ENDFORALL>>>
    return matching_call->return_value;
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