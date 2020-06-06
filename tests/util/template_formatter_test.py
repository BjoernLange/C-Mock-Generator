from c_mock_generator.util import TemplateFormatter
from c_mock_generator.util.template_formatter import MissingAttrException

import pytest


@pytest.mark.parametrize('data', [
    'static void setUp();',
    'static void tearDown();'
])
def test_no_replacement(data):
    # given:
    formatter = TemplateFormatter([data])

    # when:
    result = formatter.format(None)

    # then:
    assert '\n'.join(result) == data


class Module:
    def __init__(self, name, rel_path, methods=[]) -> None:
        self.name = name
        self.rel_path = rel_path
        self.methods = methods


class Method:
    def __init__(self, name, parameters=[]):
        self.name = name
        self.parameters = parameters


class Parameter:
    def __init__(self, type_name, name, inout=True):
        self.type_name = type_name
        self.name = name
        self.inout = inout


@pytest.mark.parametrize('template_code_lines,object_tree,resulting_code', [
    (['static void <<<name>>>_set_up();'], Module('mod', 'hal/mod.h'),
     ['static void mod_set_up();']),
    (['#include "<<<rel_path>>>"'], Module('mod', 'hal/mod.h'),
     ['#include "hal/mod.h"']),
    (['#include "<<<name>>>.h"'], Module('hal', 'hal/mod.h'),
     ['#include "hal.h"']),
    (['#include "<<<rel_path>>>"'], Module('hal', 'hal.h'),
     ['#include "hal.h"']),
    (['// Test', '#include "<<<rel_path>>>"'], Module('hal', 'hal.h'),
     ['// Test', '#include "hal.h"']),
])
def test_simple_replacement(template_code_lines, object_tree, resulting_code):
    # given:
    formatter = TemplateFormatter(template_code_lines)

    # when:
    result = formatter.format(object_tree)

    # then:
    assert list(result) == resulting_code


def test_replacing_with_missing_attribute():
    # given:
    formatter = TemplateFormatter(['<<<abc>>>'])

    # when:
    try:
        formatter.format(Module('abc', ''))
    except MissingAttrException:
        return

    assert False


@pytest.mark.parametrize('template_code_lines,object_tree,resulting_code', [
    (['<<<FORALL methods>>>',
      'static void <<<name>>>();',
      '<<<ENDFORALL>>>'
      ], Module('test', 'test.h'), []),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>();',
      '<<<ENDFORALL>>>',
      'static void shutDown();'
      ], Module('test', 'test.h'),
     ['static void shutDown();']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>();',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it')]),
     ['static void do_it();']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>();',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it'), Method('do_it2')]),
     ['static void do_it();',
      'static void do_it2();']),
    (['   <<<FORALL methods>>>',
      'static void <<<name>>>();',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it')]),
     ['static void do_it();']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>();',
      '    <<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it')]),
     ['static void do_it();']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>(',
      '    <<<FORALL parameters>>>',
      '    <<<type_name>>> <<<name>>>,',
      '    <<<ENDFORALL>>>',
      '    int x);',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it')]),
     ['static void do_it(',
      '    int x);']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>(',
      '    <<<FORALL parameters>>>',
      '    <<<type_name>>> <<<name>>>,',
      '    <<<ENDFORALL>>>',
      '    int x);',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it', [Parameter('char', 'b')])]),
     ['static void do_it(',
      '    char b,',
      '    int x);']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>(',
      '    <<<FORALL parameters JOINING , >>>',
      '    <<<type_name>>> <<<name>>>',
      '    <<<ENDFORALL>>>',
      '    );',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it', [Parameter('char', 'b')])]),
     ['static void do_it(',
      '    char b',
      '    );']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>(',
      '    <<<FORALL parameters JOINING , >>>',
      '    <<<type_name>>> <<<name>>>',
      '    <<<ENDFORALL>>>',
      '    );',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it', [Parameter('char', 'b'),
                                                Parameter('int', 'x')])]),
     ['static void do_it(',
      '    char b, int x',
      '    );']),
    (['<<<FORALL methods>>>',
      'static void <<<name>>>(',
      '    <<<FORALL parameters JOINING , >>>',
      '    <<<type_name>>> <<<name>>>',
      '    <<<ENDFORALL>>>',
      '    );',
      '<<<ENDFORALL>>>'
      ],
     Module('test', 'test.h', [Method('do_it')]),
     ['static void do_it(',
      '    );']),
    (['<<<FORALL methods JOINING <newline><newline>>>>',
      'void <<<name>>>(void);',
      '<<<ENDFORALL>>>'],
     Module('persistency', 'hal', [Method('abc'), Method('def')]),
     ['void abc(void);', '', 'void def(void);']),
    (['<<<FORALL methods JOINING <newline><newline>>>>',
      'void <<<name>>>(void);',
      'void <<<name>>>2(void);',
      '<<<ENDFORALL>>>'],
     Module('persistency', 'hal', [Method('abc'), Method('def')]),
     ['void abc(void);',
      'void abc2(void);',
      '',
      'void def(void);',
      'void def2(void);']),
    (['<<<FORALL methods JOINING <newline><newline>>>>',
      '    void <<<name>>>(void);',
      '    void <<<name>>>2(void);',
      '<<<ENDFORALL>>>'],
     Module('persistency', 'hal', [Method('abc'), Method('def')]),
     ['    void abc(void);',
      '    void abc2(void);',
      '',
      '    void def(void);',
      '    void def2(void);']),
    (['<<<FORALL parameters JOINING , >>>',
      '<<<IF inout>>>',
      '<<<type_name>>> <<<name>>>',
      '<<<ENDIF>>>',
      '<<<ENDFORALL>>>'],
     Method('abc', [Parameter('int', 'a', inout=False),
                    Parameter('int', 'b', inout=True)]),
     ['int b']),
])
def test_forall_replacement(template_code_lines, object_tree, resulting_code):
    # given:
    formatter = TemplateFormatter(template_code_lines)

    # when:
    result = formatter.format(object_tree)

    # then:
    assert list(result) == resulting_code


class Conditional:
    def __init__(self, is_in: bool):
        self.is_in = is_in


@pytest.mark.parametrize('template_code_lines,object_tree,resulting_code', [
    ([
        '<<<IF is_in>>>',
        'in',
        '<<<ENDIF>>>'
    ],
     Conditional(False),
     []),
    ([
        '<<<IF is_in>>>',
        'in',
        '<<<ENDIF>>>'
    ],
     Conditional(True),
     ['in']),
    ([
         '    <<<IF is_in>>>',
         '    in',
         '    <<<ENDIF>>>'
     ],
     Conditional(True),
     ['    in']),
    ([
         '<<<IF is_in>>>',
         '    <<<IF is_in>>>',
         'in',
         '    <<<ENDIF>>>',
         '<<<ENDIF>>>'
     ],
     Conditional(True),
     ['in']),
])
def test_if_replacement(template_code_lines, object_tree, resulting_code):
    # given:
    formatter = TemplateFormatter(template_code_lines)

    # when:
    result = formatter.format(object_tree)

    # then:
    assert list(result) == resulting_code


class Format:
    def __init__(self):
        self.value = True


def test_attribute_string_conversion():
    # given:
    object_tree = Format()
    formatter = TemplateFormatter(['<<<value>>>'])

    # when:
    result = formatter.format(object_tree)

    # then:
    assert list(result) == ['True']
