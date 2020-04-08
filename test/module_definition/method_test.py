from module_definition import Method
from module_definition.parameter import Parameter
from module_definition.type import SimpleType


def test_enrich_with_documentation_ensures_parameter_kind_is_set():
    # given:
    method = Method('abc', SimpleType('void'),
                    [Parameter('x', 'abc', SimpleType('int'))])

    # when:
    method.enrich_with_documentation(dict())

    # then:
    assert method.parameters[0].is_input
    assert not method.parameters[0].is_output
