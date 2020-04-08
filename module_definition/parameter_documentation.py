from typing import Union, Dict

from module_definition.parameter_kind import ParameterKind


class ParameterDocumentation:
    def __init__(self, identifier: str,
                 kind: Union[None, ParameterKind]) -> None:
        self.identifier = identifier
        self.kind = kind

    @classmethod
    def from_param_string(cls, string: str):
        if not string.startswith('@param'):
            return None
        string = string[6:].lstrip()

        kind = None
        if string.startswith('['):
            parameter_kind_id = string[1:string.index(']')]
            kind = ParameterKind.from_string(parameter_kind_id)
            string = string[string.index(']') + 1:].lstrip()

        if ' ' in string:
            identifier = string[:string.index(' ')]
        else:
            identifier = string

        if identifier.strip() == '':
            raise ValueError('Missing parameter name')

        return ParameterDocumentation(identifier, kind)

    @classmethod
    def multiple_from_documentation(cls, documentation: str) -> Dict:
        result = {}
        for line in documentation.splitlines():
            line = line.lstrip()
            if line.startswith('*'):
                line = line[1:].lstrip()
            if not line.startswith('@param'):
                continue

            doc = ParameterDocumentation.from_param_string(line)
            result[doc.identifier] = doc
        return result
