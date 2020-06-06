from abc import ABC, abstractmethod


class Type(ABC):
    @abstractmethod
    def can_be_output_parameter_type(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def decrease_pointer_count(self):
        raise NotImplementedError()

    @abstractmethod
    def strip_const(self):
        raise NotImplementedError()

    @abstractmethod
    def is_pointer(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_c_string(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_utf8_string(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_void(self) -> bool:
        raise NotImplementedError()

    @classmethod
    def from_type_string(cls, type_string: str):
        if '*' in type_string:
            return PointerType.from_type_string(type_string)
        return SimpleType.from_type_string(type_string)


class SimpleType(Type):
    def __init__(self, type_identifier: str):
        self.type = type_identifier

    def can_be_output_parameter_type(self) -> bool:
        return False

    def decrease_pointer_count(self):
        return self

    def strip_const(self):
        return self

    def is_pointer(self) -> bool:
        return False

    def is_c_string(self) -> bool:
        return False

    def is_utf8_string(self) -> bool:
        return False

    def is_void(self) -> bool:
        return self.type == 'void'

    def __str__(self) -> str:
        return self.type

    @classmethod
    def from_type_string(cls, type_string: str):
        return SimpleType(type_string.strip())


class PointerType(Type):
    def __init__(self, type_identifier: str, value_const: bool,
                 pointer_count: int, pointer_const: bool):
        self.type = type_identifier
        self.value_const = value_const
        self.pointer_count = pointer_count
        self.pointer_const = pointer_const

    def can_be_output_parameter_type(self) -> bool:
        return not self.value_const

    def decrease_pointer_count(self):
        if self.pointer_count == 1:
            return SimpleType(self.type)

        return PointerType(self.type, self.value_const,
                           self.pointer_count - 1, self.pointer_const)

    def strip_const(self):
        return PointerType(self.type, False, self.pointer_count, False)

    def is_pointer(self) -> bool:
        return True

    def is_c_string(self) -> bool:
        return self.type == 'char' and self.pointer_count == 1

    def is_utf8_string(self) -> bool:
        return self.type == 'wchar_t' and self.pointer_count == 1

    def is_void(self) -> bool:
        return False

    def __str__(self) -> str:
        v_const = ' const' if self.value_const else ''
        p_const = ' const' if self.pointer_const else ''
        return self.type + v_const + ' ' + '*' * self.pointer_count + p_const

    @classmethod
    def from_type_string(cls, type_string: str):
        type_string = type_string.strip()

        pointer_const = False
        if type_string.endswith(' const') or type_string.endswith('*const'):
            pointer_const = True
            type_string = type_string[:-5].rstrip()

        pointer_count = type_string.count('*')
        type_string = type_string.replace('*', '').rstrip()

        value_const = False
        if type_string.endswith(' const'):
            value_const = True
            type_string = type_string[:-5].rstrip()

        return PointerType(type_string, value_const,
                           pointer_count, pointer_const)
