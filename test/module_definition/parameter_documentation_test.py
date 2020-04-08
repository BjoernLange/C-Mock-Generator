import pytest

from module_definition.parameter_documentation import ParameterDocumentation
from module_definition.parameter_kind import ParameterKind


@pytest.mark.parametrize('text,identifier,kind', [
    ('@param abc', 'abc', None),
    ('@param abc The ABC', 'abc', None),
    ('@param[in] abc The ABC', 'abc', ParameterKind.kind_in()),
    ('@param[out] abc The ABC', 'abc', ParameterKind.kind_out()),
    ('@param[inout] abc The ABC', 'abc', ParameterKind.kind_in_out()),
])
def test_from_param_string(text, identifier, kind):
    # when:
    parameter_documentation = ParameterDocumentation.from_param_string(text)

    # then:
    assert parameter_documentation.identifier == identifier
    if kind is None:
        assert parameter_documentation.kind is None
    else:
        assert parameter_documentation.kind == kind


@pytest.mark.parametrize('text', [
    '@param []',
    '@param [in]',
])
def test_illegal_formatting_fails(text):
    # when:
    try:
        ParameterDocumentation.from_param_string(text)
    except ValueError:
        return
    assert False
