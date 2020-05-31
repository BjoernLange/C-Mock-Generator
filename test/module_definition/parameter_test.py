from typing import Optional
import pytest

from module_definition.exceptions import MockGeneratorError
from module_definition.parameter_documentation import ParameterDocumentation, \
    ActiveAttributions
from module_definition.parameter import Parameter
from module_definition.parameter_kind import ParameterKind
from module_definition.type import SimpleType, PointerType


def create_parameter_documentation(
        identifier: str, parameter_kind: Optional[str] = None,
        fixed_length: Optional[int] = None, null_terminated: bool = False,
        length_descriptor: Optional[str] = None):
    attributions = ActiveAttributions()
    if parameter_kind is not None:
        attributions.add_attribution(parameter_kind)
    if fixed_length is not None:
        attributions.add_attribution('fixed-length={}'.format(fixed_length))
    if null_terminated:
        attributions.add_attribution('null-terminated')
    if length_descriptor is not None:
        attributions.add_attribution(
            'length-descriptor={}'.format(length_descriptor))
    return ParameterDocumentation(identifier, attributions)


def test_enrich_with_documentation_fails_on_impossible_combination():
    # given:
    parameter = Parameter('abc', 'def', SimpleType('int'))
    parameter_documentation = create_parameter_documentation(
        'abc', parameter_kind='out')

    # when:
    try:
        parameter.enrich_with_documentation(parameter_documentation)
    except MockGeneratorError:
        return
    assert False


def test_initial_kind_is_guessed():
    # when:
    parameter = Parameter('abc', 'def', PointerType('int', False, 1, False))

    # then:
    assert parameter.is_input
    assert parameter.is_output


def test_enrich_with_documentation_defaults():
    # given:
    parameter = Parameter('abc', 'def', SimpleType('int'))
    parameter_documentation = create_parameter_documentation('abc')

    # when:
    parameter.enrich_with_documentation(parameter_documentation)

    # then:
    assert parameter.kind == ParameterKind.kind_in()
    assert parameter.is_input
    assert not parameter.is_output
    assert parameter.has_simple_type
    assert not parameter.has_pointer_type
    assert not parameter.is_single_element
    assert not parameter.has_fixed_length
    assert parameter.fixed_length is None
    assert not parameter.is_null_terminated
    assert not parameter.has_length_descriptor
    assert parameter.length_descriptor is None


def test_enrich_with_documentation_sets_fixed_length():
    # given:
    parameter = Parameter('abc', 'def', PointerType('int', False, 1, False))
    parameter_documentation = create_parameter_documentation('abc',
                                                             fixed_length=4)

    # when:
    parameter.enrich_with_documentation(parameter_documentation)

    # then:
    assert parameter.kind == ParameterKind.kind_in_out()
    assert parameter.fixed_length == 4


def test_enrich_with_documentation_defaults_for_pointers():
    # given:
    parameter = Parameter('abc', 'def', PointerType('int', False, 1, False))
    documentation = create_parameter_documentation('abc')

    # when:
    parameter.enrich_with_documentation(documentation)

    # then:
    assert not parameter.has_simple_type
    assert parameter.has_pointer_type
    assert parameter.is_single_element
    assert not parameter.has_fixed_length
    assert parameter.fixed_length is None
    assert not parameter.is_null_terminated
    assert not parameter.has_length_descriptor
    assert parameter.length_descriptor is None


def test_enrich_with_documentation_sets_is_null_terminated():
    # given:
    parameter = Parameter('abc', 'def', PointerType('int', False, 1, False))
    documentation = create_parameter_documentation('abc', null_terminated=True)

    # when:
    parameter.enrich_with_documentation(documentation)

    # then:
    assert parameter.is_null_terminated


def test_enrich_with_documentation_sets_length_descriptor():
    # given:
    parameter = Parameter('abc', 'def', PointerType('int', False, 1, False))
    documentation = create_parameter_documentation(
        'abc', length_descriptor='size')

    # when:
    parameter.enrich_with_documentation(documentation)

    # then:
    assert parameter.has_length_descriptor
    assert parameter.length_descriptor == 'size'


def test_char_pointer_type_is_reported_as_c_string():
    # when:
    parameter = Parameter('abc', 'def', PointerType('char', False, 1, False))

    # then:
    assert parameter.has_c_string_type
    assert not parameter.has_utf8_string_type
    assert not parameter.has_no_string_type


def test_wchar_pointer_type_is_reported_as_utf8_string():
    # when:
    parameter = Parameter('abc', 'def',
                          PointerType('wchar_t', False, 1, False))

    # then:
    assert not parameter.has_c_string_type
    assert parameter.has_utf8_string_type
    assert not parameter.has_no_string_type


@pytest.mark.parametrize('c_type', [
    SimpleType('int'),
    PointerType('int', False, 1, False),
    PointerType('char', False, 2, False),
])
def test_types_not_reported_as_c_string(c_type):
    # when:
    parameter = Parameter('abc', 'def', c_type)

    # then:
    assert not parameter.has_c_string_type
    assert not parameter.has_utf8_string_type
    assert parameter.has_no_string_type
