from module_definition.parameter_documentation import ParameterDocumentation
from module_definition.parameter_kind import ParameterKind
from module_definition.type import Type


class Parameter:
    def __init__(self, identifier: str, method_identifier: str,
                 param_type: Type) -> None:
        self.identifier = identifier
        self.method_identifier = method_identifier
        self.type = param_type
        self.kind = ParameterKind.from_in_out(
            True, param_type.can_be_output_parameter_type())

    @property
    def is_input(self):
        return self.kind.is_in()

    @property
    def is_output(self):
        return self.kind.is_out()

    @property
    def struct_type(self):
        return self.type.decrease_pointer_count().strip_const()

    @property
    def size_type(self):
        return self.type.decrease_pointer_count().strip_const()

    def enrich_with_documentation(self, documentation: ParameterDocumentation)\
            -> None:
        if documentation.identifier != self.identifier:
            return

        if documentation.kind is None:
            self.kind = ParameterKind.from_in_out(
                True, self.type.can_be_output_parameter_type())
        elif documentation.kind.is_out() \
                and not self.type.can_be_output_parameter_type():
            raise ValueError('Parameter {} is declared as output but type '
                             'cannot be used as output'.format(self))
        else:
            self.kind = documentation.kind

    def __str__(self) -> str:
        return '{} {}'.format(self.type, self.identifier)

    @classmethod
    def from_parameter_list(cls, parameter_list: str, method_identifier: str):
        parameter_list = parameter_list.strip()
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
