# A Mockito style mock generator for C


[![Actions Status](https://github.com/BjoernLange/C-Mock-Generator/workflows/CI/badge.svg)](https://github.com/BjoernLange/C-Mock-Generator/actions)

This is a code generator for simple C mocks that can be dropped into a C project without the need for any dependencies. The written test code uses a style similar to that of [Mockito](https://site.mockito.org/).

## Requirements

[Python](https://www.python.org/) is required in at least version 3.6 to run the code generator. The generated test code works only with [Google Test (gtest)](https://github.com/google/googletest).

## Principle

Mocking the C functions is based on the idea of replacing the function call targets at link time. This means that you need to compile and link against the generated versions of header and source files you want to mock.

## Basic usage

Choose a header file you want to mock and generate the mock header and source file:
```bash
> python generate_mock.py -i example.h -oh test/mocks/include/example.h -oc test/mocks/src/example.c
```
Additionally use the argument `-cp include/path` if you need a specific include path in the source file.

By default the generator guesses whether a function parameter is used as input or output. When in doubt it is assumed that the parameter is used as input and output. In this case it is possible to give hints in the documentation:

```c
// complex.h

/**
 * Performs a complex computation.
 * @param[in] input The input value.
 * @param[out] output The output value.
 * @return An error code.
 */
complex_err_t complex_computation(int input, int * output);
```

Assume we want to test this function:
```c
// something.c
#include "something.h"
#include "complex.h"

// Function under test
int do_something(int i) {
    int y = 0;

    if (complex_computation(i, &y) != COMPLEX_ERR_OK) {
        return 0;
    } else {
        return y;
    }
}
```

Then an example test could look like this:
```c
#include "something.h"

#include "complex.h" // Make sure to link against the generated version and compile the generated source file!

#include <gtest/gtest.h>

// ...

TEST(MY_TEST_SUITE_NAME, MyTestName) {
    // given:
    mock_complex_set_up();

    int output = 1;
    when_complex_computation( // expected input parameters
        0 // input
    )
    ->then_provide_output(&output, 1)  // provided output parameter
    ->then_return(COMPLEX_ERR_OK); // return value

    // when:
    int result = do_something(0);

    // then:
    ASSERT_EQ(1, result);

    // finally:
    mock_complex_tear_down();
}
```

This example is taken from our system tests.
