from typing import List, Dict
import os

from .exceptions import MockGeneratorError
from .parameter import Parameter
from .parameter_documentation import ParameterDocumentation
from .type import Type
from c_mock_generator.util import TemplateFormatter, read_lines


class Method:
    def __init__(self, identifier: str, return_type: Type,
                 parameters: List[Parameter]) -> None:
        self.identifier = identifier
        self.return_type = return_type
        self.parameters = parameters

    @property
    def return_struct_type(self):
        return str(self.return_type.decrease_pointer_count())

    @property
    def has_void_return_type(self):
        return self.return_type.is_void()

    @property
    def has_not_void_return_type(self):
        return not self.has_void_return_type

    @property
    def has_input_parameters(self):
        return [x for x in self.parameters if x.is_input]

    @property
    def has_no_input_parameters(self):
        return not self.has_input_parameters

    @property
    def has_parameters(self):
        return self.parameters

    @property
    def has_no_parameters(self):
        return not self.has_parameters

    def enrich_with_documentation(
            self, parameter_documentation: Dict[str, ParameterDocumentation]) \
            -> None:
        self.enrich_parameters_with_documentation(parameter_documentation)
        self.mark_length_descriptors_as_ignored()

    def enrich_parameters_with_documentation(
            self, parameter_documentation: Dict[str, ParameterDocumentation]):
        for parameter in self.parameters:
            if parameter.identifier in parameter_documentation:
                parameter.enrich_with_documentation(
                    parameter_documentation[parameter.identifier])

    def mark_length_descriptors_as_ignored(self):
        for parameter in self.parameters:
            if parameter.has_length_descriptor:
                try:
                    length_descriptor = next(
                        (x for x in self.parameters
                         if x.identifier == parameter.length_descriptor))
                except StopIteration:
                    raise MockGeneratorError(
                        'Cannot use {} as length descriptor for {} because it '
                        'does not exist'.format(
                            parameter.length_descriptor, parameter.identifier))

                length_descriptor.is_ignored = True

    def __str__(self) -> str:
        return '{} {}({})'.format(self.return_type, self.identifier,
                                  ', '.join([str(x) for x in self.parameters]))

    @classmethod
    def from_method_definition(cls, method_definition: str):
        parts = method_definition.split('(')
        ret_id_part = parts[0]
        return_type = ret_id_part[:ret_id_part.rindex(' ')].strip()
        identifier = ret_id_part[ret_id_part.rindex(' ') + 1:].strip()

        return Method(identifier, Type.from_type_string(return_type),
                      Parameter.from_parameter_list(parts[1][:-2], identifier))

    def generate_header_content(self) -> str:
        header_template = os.path.join(os.path.dirname(__file__), '..',
                                       'resource', 'header_template.h')
        return '\n'.join(
            TemplateFormatter(read_lines(header_template)).format(self))
