#include "under_test.h"

#include "to_mock.h"

#include <gtest/gtest.h>

#define UNDER_TEST_TEST_SUITE_NAME UnderTestTest

TEST(UNDER_TEST_TEST_SUITE_NAME, ArrayOutputSingleElementTest) {
    // given:
    mock_to_mock_set_up();

    int output = 1;
    when_to_mock_compute(0)->then_provide_result(&output, 1)->then_return();

    // when:
    int result = do_something(0);

    // then:
    ASSERT_EQ(1, result);

    // finally:
    mock_to_mock_tear_down();
}
