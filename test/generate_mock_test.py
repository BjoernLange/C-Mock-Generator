from generate_mock import MockHeaderCodeGenerator

EXPECTED_HEADER_CODE = \
    '''#ifndef __DEMO_H__
#define __DEMO_H__
void mock_demo_set_up(void);
void mock_demo_tear_down(void);

#endif
#if ABC
#endif
'''


def test_set_up_tear_down_is_not_generated_twice():
    # given:
    generator = MockHeaderCodeGenerator('demo', None, [
        '#ifndef __DEMO_H__',
        '#define __DEMO_H__',
        '#endif',
        '#if ABC',
        '#endif',
    ])

    # when:
    generator.generate_header_code()

    # then
    assert generator.header_code == EXPECTED_HEADER_CODE
