#include "under_test.h"

#include "to_mock.h"

#include <gtest/gtest.h>

#define UNDER_TEST_TEST_SUITE_NAME UnderTestTest

TEST(UNDER_TEST_TEST_SUITE_NAME, StructPointersCanBeCompared) {
    // given:
    my_struct_t expected = {
        .a = 5,
        .b = 10
    };

    mock_to_mock_set_up();
    when_to_mock_do(&expected)->then_return(15);

    // when:
    int result = do_something(5, 10);

    // then:
    ASSERT_EQ(15, result);

    // finally:
    mock_to_mock_tear_down();
}


TEST(UNDER_TEST_TEST_SUITE_NAME, StructsCanBeCompared) {
    // given:
    my_struct_t expected = {
        .a = 5,
        .b = 10
    };

    mock_to_mock_set_up();
    when_to_mock_do_copy(expected)->then_return(15);

    // when:
    int result = do_something_copy(5, 10);

    // then:
    ASSERT_EQ(15, result);

    // finally:
    mock_to_mock_tear_down();
}
