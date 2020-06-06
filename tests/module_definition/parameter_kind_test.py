from c_mock_generator.module_definition.exceptions import MockGeneratorError
from c_mock_generator.module_definition.parameter_kind import ParameterKind

import pytest


@pytest.mark.parametrize('p_in,p_out', [
    (True, False),
    (True, True),
    (False, True),
])
def test_kind_from_in_out(p_in: bool, p_out: bool):
    # when:
    kind = ParameterKind.from_in_out(p_in, p_out)

    # then:
    assert kind.is_in() == p_in
    assert kind.is_out() == p_out


def test_kind_in_out():
    # when:
    kind = ParameterKind.kind_in_out()

    # then:
    assert kind.is_in()
    assert kind.is_out()


def test_kind_in():
    # when:
    kind = ParameterKind.kind_in()

    # then:
    assert kind.is_in()
    assert not kind.is_out()


def test_kind_out():
    # when:
    kind = ParameterKind.kind_out()

    # then:
    assert not kind.is_in()
    assert kind.is_out()


def test_creation_of_invalid_kind_throws_mock_generator_error():
    # when:
    try:
        ParameterKind.from_in_out(False, False)
    except MockGeneratorError:
        return
    assert False


@pytest.mark.parametrize('identifier,expected_in,expected_out', [
    ('in', True, False),
    ('out', False, True),
    ('inout', True, True),
])
def test_from_string(identifier: str, expected_in: bool, expected_out: bool):
    # when:
    kind = ParameterKind.from_string(identifier)

    # then:
    assert kind.is_in() == expected_in
    assert kind.is_out() == expected_out


def test_from_string_for_illegal_value():
    # when:
    try:
        ParameterKind.from_string('abc')
    except MockGeneratorError:
        return
    assert False
