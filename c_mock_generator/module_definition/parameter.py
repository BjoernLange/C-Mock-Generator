from typing import Optional

from .exceptions import MockGeneratorError
from .parameter_documentation import ParameterDocumentation
from .parameter_kind import ParameterKind
from .type import Type


class Parameter:
    def __init__(self, identifier: str, method_identifier: str,
                 param_type: Type) -> None:
        self.identifier = identifier
        self.method_identifier = method_identifier
        self.type = param_type
        self.kind = ParameterKind.from_in_out(
            True, param_type.can_be_output_parameter_type())
        self.fixed_length: Optional[int] = None
        self.is_null_terminated = False
        self.length_descriptor: Optional[str] = None
        self.is_ignored = False

    @property
    def is_input(self) -> bool:
        return self.kind.is_in()

    @property
    def is_output(self) -> bool:
        return self.kind.is_out()

    @property
    def size_type(self) -> Type:
        return self.type.decrease_pointer_count().strip_const()

    @property
    def has_simple_type(self) -> bool:
        return not self.has_pointer_type

    @property
    def has_pointer_type(self) -> bool:
        return self.type.is_pointer()

    @property
    def is_single_element(self) -> bool:
        return self.has_pointer_type and \
               not self.has_fixed_length and \
               not self.is_null_terminated and \
               not self.has_length_descriptor

    @property
    def has_fixed_length(self) -> bool:
        return self.fixed_length is not None

    @property
    def has_length_descriptor(self) -> bool:
        return self.length_descriptor is not None

    @property
    def is_included(self) -> bool:
        return not self.is_ignored

    @property
    def has_c_string_type(self) -> bool:
        return self.type.is_c_string()

    @property
    def has_utf8_string_type(self) -> bool:
        return self.type.is_utf8_string()

    @property
    def has_no_string_type(self) -> bool:
        return not self.has_c_string_type and not self.has_utf8_string_type

    def enrich_with_documentation(self, documentation: ParameterDocumentation)\
            -> None:
        if documentation.identifier != self.identifier:
            return

        if documentation.kind is None:
            self.kind = ParameterKind.from_in_out(
                True, self.type.can_be_output_parameter_type())
        elif documentation.kind.is_out() \
                and not self.type.can_be_output_parameter_type():
            raise MockGeneratorError(
                'Parameter {} is declared as output but type cannot be used '
                'as output'.format(self))
        else:
            self.kind = documentation.kind

        self.fixed_length = documentation.fixed_length
        self.is_null_terminated = documentation.null_terminated
        self.length_descriptor = documentation.length_descriptor

    def __str__(self) -> str:
        return '{} {}'.format(self.type, self.identifier)

    @classmethod
    def from_parameter_list(cls, parameter_list: str, method_identifier: str):
        parameter_list = parameter_list.strip()
        if not parameter_list:
            raise MockGeneratorError(
                'Method {} has an unspecified number of arguments '
                '(pre-prototype). Use "void" if you want a method without '
                'parameters.'.format(method_identifier))
        if parameter_list == 'void':
            return []

        params = parameter_list.split(',')
        result = []
        for definition in params:
            definition = definition.strip()
            param_type = definition[:definition.rindex(' ')].strip()
            identifier = definition[definition.rindex(' ') + 1:].strip()
            result.append(Parameter(identifier,
                                    method_identifier,
                                    Type.from_type_string(param_type)))
        return result
