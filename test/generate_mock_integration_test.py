import subprocess
import os
import shutil
import pytest


TEMP_DIRECTORY = 'tmp'
TEMP_HEADER = os.path.join(TEMP_DIRECTORY, 'header.h')
TEMP_SOURCE = os.path.join(TEMP_DIRECTORY, 'source.c')


def set_up():
    os.mkdir(TEMP_DIRECTORY)


def tear_down():
    shutil.rmtree(TEMP_DIRECTORY)


@pytest.fixture(autouse=True)
def run_around_tests():
    set_up()
    yield
    tear_down()


def read_file_content(filepath: str) -> str:
    with open(filepath, 'r') as file:
        return file.read()


def test_integration():
    # given:
    input_path = os.path.join('test', 'resource', 'example_header.h')
    expected_header = os.path.join('test', 'resource', 'example_mock.h')
    expected_source = os.path.join('test', 'resource', 'example_mock.c')

    # when:
    subprocess.run([
        'python', 'generate_mock.py',
        '-i', input_path,
        '-oh', TEMP_HEADER,
        '-oc', TEMP_SOURCE], check=True)

    # then:
    assert os.path.isfile(TEMP_HEADER)
    assert os.path.isfile(TEMP_SOURCE)

    assert read_file_content(TEMP_HEADER) == read_file_content(expected_header)
    assert read_file_content(TEMP_SOURCE) == read_file_content(expected_source)
