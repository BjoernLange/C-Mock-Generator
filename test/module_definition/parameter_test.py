from module_definition.parameter_documentation import ParameterDocumentation
from module_definition.parameter import Parameter
from module_definition.parameter_kind import ParameterKind
from module_definition.type import SimpleType, PointerType


def test_enrich_with_documentation():
    # given:
    parameter = Parameter('abc', 'def', SimpleType('int'))
    parameter_documentation = ParameterDocumentation('abc', None)

    # when:
    parameter.enrich_with_documentation(parameter_documentation)

    # then:
    assert parameter.kind == ParameterKind.kind_in()


def test_enrich_with_documentation_fails_on_impossible_combination():
    # given:
    parameter = Parameter('abc', 'def', SimpleType('int'))
    parameter_documentation = ParameterDocumentation(
        'abc', ParameterKind.kind_out())

    # when:
    try:
        parameter.enrich_with_documentation(parameter_documentation)
    except ValueError:
        return
    assert False


def test_initial_kind_is_guessed():
    # when:
    parameter = Parameter('abc', 'def', PointerType('int', False, 1, False))

    # then:
    assert parameter.is_input
    assert parameter.is_output
