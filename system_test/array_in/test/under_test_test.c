#include "under_test.h"

#include "to_mock.h"

#include <gtest/gtest.h>

#define UNDER_TEST_TEST_SUITE_NAME UnderTestTest

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputFixedSizeTest) {
    // given:
    mock_to_mock_set_up();

    int input[2] = {2, 3};
    int output = 1;
    when_to_mock_compute_fixed_size( // expected input parameters
        input // input
    )
    ->then_provide_output(&output, 1)  // provided output parameter
    ->then_return(TO_MOCK_ERR_OK); // return value

    // when:
    int result = do_something_fixed_size(0);

    // then:
    ASSERT_EQ(1, result);

    // finally:
    mock_to_mock_tear_down();
}

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputNullTerminatedTest) {
    // given:
    mock_to_mock_set_up();

    char input_to_ignore[3] = {'a', 'c', '\0'};
    int output_to_ignore = 5;
    when_to_mock_compute_null_terminated( // expected input parameters
        input_to_ignore // input
    )
    ->then_provide_output(&output_to_ignore, 1)  // provided output parameter
    ->then_return(TO_MOCK_ERR_OK); // return value

    char input_to_ignore2[2] = {'a', '\0'};
    int output_to_ignore2 = 6;
    when_to_mock_compute_null_terminated( // expected input parameters
        input_to_ignore2 // input
    )
    ->then_provide_output(&output_to_ignore2, 1)  // provided output parameter
    ->then_return(TO_MOCK_ERR_OK); // return value

    char input[3] = {'a', 'b', '\0'};
    int output = 2;
    when_to_mock_compute_null_terminated( // expected input parameters
        input // input
    )
    ->then_provide_output(&output, 1)  // provided output parameter
    ->then_return(TO_MOCK_ERR_OK); // return value

    // when:
    int result = do_something_null_terminated('a', 'b');

    // then:
    ASSERT_EQ(2, result);

    // finally:
    mock_to_mock_tear_down();
}

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputNullTerminatedTwiceTest) {
    // given:
    mock_to_mock_set_up();

    char input1[2] = {'a', '\0'};
    int input2[3] = {5, 6, 0};
    int output = 2;
    when_to_mock_compute_null_terminated_twice(
        input1,
        input2
    )
    ->then_provide_output(&output, 1)
    ->then_return(TO_MOCK_ERR_OK);

    // when:
    int result = do_something_null_terminated_twice('a', 5);

    // then:
    ASSERT_EQ(2, result);

    // finally:
    mock_to_mock_tear_down();
}

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputLengthDescribedTest) {
    // given:
    mock_to_mock_set_up();

    int input[3] = {5, 6, 0};
    int output = 7;
    when_to_mock_compute_length_described(
        input,
        3
    )
    ->then_provide_output(&output, 1)
    ->then_return(TO_MOCK_ERR_OK);

    // when:
    int result = do_something_length_described(0, 5);

    // then:
    ASSERT_EQ(7, result);

    // finally:
    mock_to_mock_tear_down();
}

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputLengthDescribedMatchCorrectByContentTest) {
    // given:
    mock_to_mock_set_up();

    int alt_input[3] = {1, 2, 3};
    int alt_output = 4;
    when_to_mock_compute_length_described(
        alt_input,
        3
    )
    ->then_provide_output(&alt_output, 1)
    ->then_return(TO_MOCK_ERR_OK);

    int input[3] = {5, 6, 0};
    int output = 7;
    when_to_mock_compute_length_described(
        input,
        3
    )
    ->then_provide_output(&output, 1)
    ->then_return(TO_MOCK_ERR_OK);

    // when:
    int result = do_something_length_described(0, 5);

    // then:
    ASSERT_EQ(7, result);

    // finally:
    mock_to_mock_tear_down();
}

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputLengthDescribedMatchCorrectByLengthTest) {
    // given:
    mock_to_mock_set_up();

    int input_to_ignore[2] = {5, 6};
    int output_to_ignore = 4;
    when_to_mock_compute_length_described(
        input_to_ignore,
        2
    )
    ->then_provide_output(&output_to_ignore, 1)
    ->then_return(TO_MOCK_ERR_OK);

    int input[3] = {5, 6, 0};
    int output = 7;
    when_to_mock_compute_length_described(
        input,
        3
    )
    ->then_provide_output(&output, 1)
    ->then_return(TO_MOCK_ERR_OK);

    // when:
    int result = do_something_length_described(0, 5);

    // then:
    ASSERT_EQ(7, result);

    // finally:
    mock_to_mock_tear_down();
}

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayInputUtf8StringComparisonTest) {
    // given:
    mock_to_mock_set_up();

    wchar_t input[3] = L"ab";
    int output = 7;
    when_to_mock_compute_utf8(
        input
    )
    ->then_provide_output(&output, 1)
    ->then_return(TO_MOCK_ERR_OK);

    // when:
    int result = do_something_utf8(L'a', L'b');

    // then:
    ASSERT_EQ(7, result);

    // finally:
    mock_to_mock_tear_down();
}
