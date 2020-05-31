import pytest

from module_definition.exceptions import MockGeneratorError
from module_definition.parameter_documentation import ParameterDocumentation, \
    ActiveAttributions, parse_param_annotation
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
    assert parameter_documentation.fixed_length is None
    assert not parameter_documentation.null_terminated
    assert parameter_documentation.length_descriptor is None


@pytest.mark.parametrize('text', [
    '@param []',
    '@param [in]',
])
def test_illegal_formatting_fails(text):
    # when:
    try:
        ParameterDocumentation.from_param_string(text)
    except MockGeneratorError:
        return
    assert False


def test_duplicate_in_out_attributions_are_not_allowed():
    # given:
    text = '@param[in, out] test'

    # when:
    try:
        ParameterDocumentation.from_param_string(text)
    except MockGeneratorError:
        return
    assert False


@pytest.mark.parametrize('text', [
    '@param[in, fixed-length=3] test',
    '@param[in,fixed-length=3] test',
    '@param[in,fixed-length =3] test',
    '@param[in,fixed-length= 3] test',
    '@param[in,fixed-length = 3] test',
    '@param[in, fixed-length = 3] test',
])
def test_param_annotation_can_be_parsed_ignoring_whitespace(text):
    # when:
    is_valid_annotation, attribution_values, identifier = \
        parse_param_annotation(text)

    # then:
    assert is_valid_annotation
    assert len(attribution_values) == 2
    assert attribution_values[0] == 'in'
    assert attribution_values[1].startswith('fixed-length')
    assert attribution_values[1].endswith('3')


@pytest.mark.parametrize('text', [
    'fixed-length=3',
    'fixed-length =3',
    'fixed-length= 3',
    'fixed-length = 3',
])
def test_attribution_can_be_parsed_ignoring_additional_whitespace(text):
    # given:
    active_attributions = ActiveAttributions()

    # when:
    active_attributions.add_attribution(text)

    # then:
    assert active_attributions.fixed_length == 3


@pytest.mark.parametrize('text,fixed_length', [
    ('@param[in, fixed-length=3] test', 3),
    ('@param[in, fixed-length=2] test', 2),
])
def test_parse_fixed_length(text, fixed_length):
    # when:
    parameter_documentation = ParameterDocumentation.from_param_string(text)

    # then:
    assert parameter_documentation.identifier == 'test'
    assert parameter_documentation.kind == ParameterKind.kind_in()
    assert parameter_documentation.fixed_length == fixed_length


@pytest.mark.parametrize('text', [
    'fixed-length',
    'fixed-length=abc'
])
def test_illegal_fixed_length(text):
    # given:
    active_attributions = ActiveAttributions()

    # when:
    try:
        active_attributions.add_attribution(text)
    except MockGeneratorError:
        return
    assert False


@pytest.mark.parametrize('text', [
    '@param[in, fixed-length=4, fixed-length=5] test',
    '@param[in, in, fixed-length=5] test',
    '@param[in, null-terminated, null-terminated] value',
])
def test_no_attribution_is_allowed_to_appear_multiple_times(text):
    # when:
    try:
        ParameterDocumentation.from_param_string(text)
    except MockGeneratorError:
        return
    assert False


def test_parse_null_terminated():
    # given:
    text = '@param[in, null-terminated] value'

    # when:
    parameter_documentation = ParameterDocumentation.from_param_string(text)

    # then:
    assert parameter_documentation.identifier == 'value'
    assert parameter_documentation.kind == ParameterKind.kind_in()
    assert parameter_documentation.fixed_length is None
    assert parameter_documentation.null_terminated


@pytest.mark.parametrize('text', [
    '@param[null-terminated, fixed-length=4] x',
    '@param[fixed-length=1, null-terminated] y',
    '@param[fixed-length=4, length-descriptor=a] d',
    '@param[length-descriptor=a, fixed-length=3] d',
    '@param[null-terminated, length-descriptor=a] d',
    '@param[length-descriptor=a, null-terminated] d',
])
def test_conflicting_length_specifiers(text):
    # when:
    try:
        ParameterDocumentation.from_param_string(text)
    except MockGeneratorError:
        return
    assert False


def test_unknown_attribution():
    # given:
    text = '@param[so-what] d'

    # when:
    try:
        ParameterDocumentation.from_param_string(text)
    except MockGeneratorError:
        return
    assert False


@pytest.mark.parametrize(('text', 'expected'), [
    ('@param[length-descriptor=size] a', 'size'),
    ('@param[length-descriptor=length] b', 'length'),
])
def test_length_descriptor_attribution_is_parsed(text, expected):
    # when:
    parameter_documentation = ParameterDocumentation.from_param_string(text)

    # then:
    assert parameter_documentation.length_descriptor == expected
