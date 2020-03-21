from util.code_builder import CodeBuilder


def test_append():
    # given:
    builder = CodeBuilder()

    # when:
    builder.append('xyz')

    # then:
    assert str(builder) == 'xyz'


def test_multi_append():
    # given:
    builder = CodeBuilder()

    # when:
    builder.append('xyz', 'abc')

    # then:
    assert str(builder) == 'xyzabc'
