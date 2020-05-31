import argparse
import os
from typing import Iterable, Tuple, List, Optional

from module_definition import Module, Method, ParameterDocumentation
from module_definition.exceptions import MockGeneratorError
from util import CodeBuilder, TemplateFormatter, read_lines


def line_starts_with_documentation(line: str) -> bool:
    return line.lstrip().startswith('/**')


class LineIterator(Iterable):
    def __init__(self, lines: Iterable[str]) -> None:
        self.iterator = iter(lines)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)

    def parse_method(self):
        documentation = self.read_until('*/')
        parameter_documentation = \
            ParameterDocumentation.multiple_from_documentation(documentation)
        method_definition = self.read_until(';').rstrip()
        method = Method.from_method_definition(method_definition)
        method.enrich_with_documentation(parameter_documentation)
        return method

    def read_until(self, terminator: str) -> str:
        result = ''
        line = next(self.iterator)
        while not line.rstrip().endswith(terminator):
            result = result + line
            line = next(self.iterator)
        return result + line


class MockHeaderCodeGenerator:
    def __init__(self, module_name: str, source_include_path: Optional[str],
                 lines: Iterable[str]) -> None:
        self.module_name = module_name
        self.source_include_path = source_include_path
        self.line_it = LineIterator(lines)
        self.header_builder = CodeBuilder()
        self.ifdef_level = 0
        self.methods: List[Method] = []
        self.set_up_tear_down_generated = False

    def generate_header_code(self) -> None:
        line_number = 1
        try:
            for line in self.line_it:
                self.track_ifdef_level(line)

                if self.should_generate_set_up_and_tear_down_declarations():
                    self.append_set_up_tear_down_declaration()

                if line_starts_with_documentation(line):
                    method = self.line_it.parse_method()
                    self.register_method(method)
                else:
                    self.append_line(line)
                self.append_newline()
                line_number = line_number + 1
        except MockGeneratorError as error:
            print('Parsing error at line {}: {}'
                  .format(line_number, str(error)))
            exit(1)

    @property
    def module(self) -> Module:
        return Module(self.source_include_path, self.module_name, self.methods)

    @property
    def header_code(self) -> str:
        return str(self.header_builder)

    def append_newline(self) -> None:
        self.header_builder.newline()

    def append_line(self, line: str) -> None:
        self.header_builder.append(line.rstrip())

    def should_generate_set_up_and_tear_down_declarations(self) -> bool:
        return not self.set_up_tear_down_generated and self.ifdef_level == 0

    def register_method(self, method: Method) -> None:
        self.header_builder.append(method.generate_header_content())
        self.methods.append(method)

    def track_ifdef_level(self, line: str) -> None:
        if line.lstrip().startswith('#if'):
            self.ifdef_level = self.ifdef_level + 1
        elif line.lstrip().startswith('#endif'):
            self.ifdef_level = self.ifdef_level - 1

    def append_set_up_tear_down_declaration(self) -> None:
        self.set_up_tear_down_generated = True
        self.header_builder.append('void mock_', self.module_name,
                                   '_set_up(void);').newline()
        self.header_builder.append('void mock_', self.module_name,
                                   '_tear_down(void);').newline().newline()


def generate_mock_header_code(
        module_name: str, source_include_path: Optional[str],
        lines: Iterable[str]) -> Tuple[str, Module]:
    generator = MockHeaderCodeGenerator(
        module_name, source_include_path, lines)
    generator.generate_header_code()
    return generator.header_code, generator.module


def generate_mock_source_code(module: Module):
    return '\n'.join(TemplateFormatter(
        read_lines('resource/source_template.c')).format(module))


def generate_mock_code_for_lines(
        module_name: str, source_include_path: Optional[str],
        lines: Iterable[str]) -> Tuple[str, str]:
    header_code, module = generate_mock_header_code(
        module_name, source_include_path, lines)
    source_code = generate_mock_source_code(module)
    return header_code, source_code


def are_args_valid(args) -> bool:
    if not args.input.endswith('.h') or \
            not os.path.isfile(args.input):
        print('Input needs to be a C header file.')
        return False

    if not args.output_header.endswith('.h') or \
            os.path.isfile(args.output_header):
        print('Output header needs to be a C header file name and '
              'must not exist.')
        return False

    if not args.output_source.endswith('.c') or \
            os.path.isfile(args.output_source):
        print('Output source needs to be a C source file name and '
              'must not exist.')
        return False

    return True


def generate_mock_code(args) -> None:
    if not are_args_valid(args):
        return

    with open(args.input) as file:
        module_name = os.path.basename(args.input)[:-2]
        source_include_path = args.source_include_path
        lines = (x for x in file)
        header, source = generate_mock_code_for_lines(
            module_name, source_include_path, lines)

    with open(args.output_header, 'w') as file:
        file.write(header)
    with open(args.output_source, 'w') as file:
        file.write(source)


def main() -> None:
    parser = argparse.ArgumentParser()
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-i', '--input', required=True)
    required_named.add_argument('-oh', '--output-header', required=True)
    required_named.add_argument('-oc', '--output-source', required=True)
    parser.add_argument('-cp', '--source-include-path')
    generate_mock_code(parser.parse_args())


if __name__ == '__main__':
    main()
