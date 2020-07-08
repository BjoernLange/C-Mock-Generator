#include "under_test.h"

#include "to_mock.h"

#include <gtest/gtest.h>

#define UNDER_TEST_TEST_SUITE_NAME UnderTestTest

TEST(UNDER_TEST_TEST_SUITE_NAME, NoWarningWhenNoMatchableParameterExists) {
    // given:
    mock_to_mock_set_up();
    when_to_mock_get_value()->then_return(2);

    // when:
    int result = do_something(4);

    // then:
    ASSERT_EQ(6, result);

    // finally:
    mock_to_mock_tear_down();
}
