import pytest

from module_definition import Method
from module_definition.exceptions import MockGeneratorError
from module_definition.parameter import Parameter
from module_definition.parameter_documentation import ParameterDocumentation, \
    ActiveAttributions
from module_definition.type import SimpleType, PointerType


def test_enrich_with_documentation_ensures_parameter_kind_is_set():
    # given:
    method = Method('abc', SimpleType('void'),
                    [Parameter('x', 'abc', SimpleType('int'))])

    # when:
    method.enrich_with_documentation(dict())

    # then:
    assert method.parameters[0].is_input
    assert not method.parameters[0].is_output


def test_enrich_with_documentation_sets_ignored_on_length_descriptors():
    # given:
    pointer_param = Parameter('x', 'abc', PointerType('int', False, 1, False))
    length_descriptor_param = Parameter('size', 'abc', SimpleType('size_t'))
    method = Method('abc', SimpleType('void'),
                    [pointer_param, length_descriptor_param])

    attributions = ActiveAttributions()
    attributions.add_attribution('length-descriptor=size')
    documentation = ParameterDocumentation('x', attributions)

    # when:
    method.enrich_with_documentation({'x': documentation})

    # then:
    assert not pointer_param.is_ignored
    assert pointer_param.is_included
    assert length_descriptor_param.is_ignored
    assert not length_descriptor_param.is_included


def test_error_is_raised_when_length_descriptor_does_not_exist():
    # given:
    pointer_param = Parameter('x', 'abc', PointerType('int', False, 1, False))
    method = Method('abc', SimpleType('void'),
                    [pointer_param])

    attributions = ActiveAttributions()
    attributions.add_attribution('length-descriptor=size')
    documentation = ParameterDocumentation('x', attributions)

    # when:
    try:
        method.enrich_with_documentation({'x': documentation})
    except MockGeneratorError:
        return
    assert False


@pytest.mark.parametrize('return_type,is_not_void', [
    (SimpleType('void'), False),
    (SimpleType('int'), True),
    (PointerType('void', False, 1, False), True),
])
def test_has_not_void_return_type_returns_true_when_return_type_is_not_void(
        return_type, is_not_void):
    # given:
    method = Method('abc', return_type, [])

    # when:
    result = method.has_not_void_return_type

    # then:
    assert result == is_not_void


@pytest.mark.parametrize('return_type,is_void', [
    (SimpleType('void'), True),
    (SimpleType('int'), False),
    (PointerType('void', False, 1, False), False),
])
def test_has_void_return_type_returns_true_when_the_return_type_is_void(
        return_type, is_void):
    # given:
    method = Method('abc', return_type, [])

    # when:
    result = method.has_void_return_type

    # then:
    assert result == is_void
