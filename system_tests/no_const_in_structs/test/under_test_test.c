#include "under_test.h"

#include "to_mock.h"

#include <gtest/gtest.h>

#define UNDER_TEST_TEST_SUITE_NAME UnderTestTest

TEST(UNDER_TEST_TEST_SUITE_NAME, ConstPointerParametersCompile) {
    // given:
    int value = 4;
    mock_to_mock_set_up();
    when_to_mock_do(&value)->then_return(2);

    // when:
    int result = do_something(value);

    // then:
    ASSERT_EQ(2, result);

    // finally:
    mock_to_mock_tear_down();
}
