from module_definition import Method
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


def test_value_error_is_raised_when_length_descriptors_does_not_exist():
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
    except ValueError:
        return
    assert False
