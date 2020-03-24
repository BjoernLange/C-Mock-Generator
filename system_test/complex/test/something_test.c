#include "something.h"

#include "complex.h"

#include <gtest/gtest.h>

#define SOMETHING_TEST_SUITE_NAME SomethingTest

TEST(SOMETHING_TEST_SUITE_NAME, ExampleTest) {
    // given:
    mock_complex_set_up();

    int output = 1;
    when_complex_computation( // expected input parameters
        0 // input
    )
    ->then_provide_output(&output)  // provided output parameter
    ->then_return(COMPLEX_ERR_OK); // return value

    // when:
    int result = do_something(0);

    // then:
    ASSERT_EQ(1, result);

    // finally:
    mock_complex_tear_down();
}

