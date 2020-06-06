from .exceptions import MockGeneratorError


class ParameterKind:
    def __init__(self, is_in: bool, is_out: bool) -> None:
        self.p_in = is_in
        self.p_out = is_out

    def is_in(self) -> bool:
        return self.p_in

    def is_out(self) -> bool:
        return self.p_out

    @classmethod
    def from_string(cls, identifier: str):
        if identifier == 'in':
            return cls.kind_in()
        if identifier == 'out':
            return cls.kind_out()
        if identifier == 'inout':
            return cls.kind_in_out()
        raise MockGeneratorError('{} is not a valid parameter kind.'
                                 .format(identifier))

    @classmethod
    def from_in_out(cls, p_in: bool, p_out: bool):
        if p_in and p_out:
            return cls.kind_in_out()
        if p_in:
            return cls.kind_in()
        if p_out:
            return cls.kind_out()
        raise MockGeneratorError('Parameter needs to be either in or out.')

    @classmethod
    def kind_in_out(cls):
        return PARAMETER_KIND_IN_OUT

    @classmethod
    def kind_in(cls):
        return PARAMETER_KIND_IN

    @classmethod
    def kind_out(cls):
        return PARAMETER_KIND_OUT


PARAMETER_KIND_IN = ParameterKind(True, False)
PARAMETER_KIND_OUT = ParameterKind(False, True)
PARAMETER_KIND_IN_OUT = ParameterKind(True, True)
