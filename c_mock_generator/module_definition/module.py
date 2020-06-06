from typing import List, Union

from c_mock_generator.module_definition import Method


class Module:
    def __init__(self, include_path: Union[str, None],
                 name: str, methods: List[Method]):
        self.include_path = include_path
        self.name = name
        self.methods = methods

    @property
    def has_include_path(self):
        return self.include_path is not None

    @property
    def has_no_include_path(self):
        return not self.has_include_path
