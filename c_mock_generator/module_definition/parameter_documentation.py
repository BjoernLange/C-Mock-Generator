from abc import ABC
from typing import Dict, Set, List, Tuple, Optional, cast

from .exceptions import MockGeneratorError
from .parameter_kind import ParameterKind


ATTRIBUTION_FACTORIES = {
    'in':
        lambda v: KeywordAttribution(
            'in', conflicting_identifiers={'out', 'inout'}),
    'out':
        lambda v: KeywordAttribution(
            'out', conflicting_identifiers={'in', 'inout'}),
    'inout':
        lambda v: KeywordAttribution(
            'inout', conflicting_identifiers={'in', 'out'}),

    'fixed-length':
        lambda v:
        PositiveIntAttribution(
            'fixed-length', v,
            conflicting_identifiers={'null-terminated', 'length-descriptor'}),
    'null-terminated':
        lambda v:
        KeywordAttribution(
            'null-terminated',
            conflicting_identifiers={'fixed-length', 'length-descriptor'}),
    'length-descriptor':
        lambda v:
        StringAttribution(
            'length-descriptor', v,
            conflicting_identifiers={'fixed-length', 'null-terminated'}),
}


def create_attribution(identifier: str, value: Optional[str]):
    if identifier not in ATTRIBUTION_FACTORIES:
        raise MockGeneratorError('Unknown attribution: {}'.format(identifier))

    return ATTRIBUTION_FACTORIES[identifier](value)


def parse_param_annotation(param_annotation: str) -> \
        Tuple[bool, List[str], str]:
    is_valid_annotation = param_annotation.startswith('@param')
    param_annotation = param_annotation[6:].lstrip()

    attribution_values: List[str] = []
    if param_annotation.startswith('['):
        all_attribution_values = \
            param_annotation[1:param_annotation.index(']')]
        param_annotation = \
            param_annotation[param_annotation.index(']') + 1:].lstrip()

        attribution_values = \
            [x.strip()
             for x in all_attribution_values.split(',')
             if x.strip()]

    if ' ' in param_annotation:
        identifier = param_annotation[:param_annotation.index(' ')]
    else:
        identifier = param_annotation

    if identifier.strip() == '':
        raise MockGeneratorError('Missing parameter identifier')

    return is_valid_annotation, attribution_values, identifier


class ActiveAttributions:
    def __init__(self) -> None:
        self.active: Dict[str, Attribution] = {}

    def add_attribution(self, attribution_value: str) -> None:
        identifier, value = \
            ActiveAttributions.__parse_identifier_and_value(attribution_value)

        if identifier in self.active:
            raise MockGeneratorError('Duplicate {} attribution'
                                     .format(identifier))

        attribution = create_attribution(identifier, value)
        self.check_for_conflicts(attribution)
        self.active[attribution.identifier] = attribution

    def check_for_conflicts(self, attribution):
        for active in self.active.values():
            if active.conflicts_with(attribution.identifier):
                raise MockGeneratorError(
                    '{} and {} attributions cannot be used simultaneously'
                    .format(active.identifier, attribution.identifier))

    @classmethod
    def __parse_identifier_and_value(cls, attribution_value: str) -> \
            Tuple[str, Optional[str]]:
        value: Optional[str] = None
        if '=' in attribution_value:
            identifier = \
                attribution_value[:attribution_value.index('=')].rstrip()
            value = \
                attribution_value[attribution_value.index('=') + 1:]
        else:
            identifier = attribution_value
        return identifier, value

    @property
    def kind(self) -> Optional[ParameterKind]:
        if 'in' in self.active:
            return ParameterKind.kind_in()
        elif 'out' in self.active:
            return ParameterKind.kind_out()
        elif 'inout' in self.active:
            return ParameterKind.kind_in_out()
        return None

    @property
    def fixed_length(self) -> Optional[int]:
        if 'fixed-length' not in self.active:
            return None

        attribution = cast(PositiveIntAttribution, self.active['fixed-length'])
        return attribution.value

    @property
    def null_terminated(self) -> bool:
        return 'null-terminated' in self.active

    @property
    def length_descriptor(self) -> Optional[str]:
        if 'length-descriptor' not in self.active:
            return None

        attribution = cast(StringAttribution, self.active['length-descriptor'])
        return attribution.value


class ParameterDocumentation:
    def __init__(self, identifier: str, attributions: ActiveAttributions) \
            -> None:
        self.identifier = identifier
        self.kind = attributions.kind
        self.fixed_length = attributions.fixed_length
        self.null_terminated = attributions.null_terminated
        self.length_descriptor = attributions.length_descriptor

    @classmethod
    def from_param_string(cls, string: str):
        is_valid_annotation, attribution_values, identifier = \
            parse_param_annotation(string)
        if not is_valid_annotation:
            return None

        active_attributions = ActiveAttributions()
        for attribution_value in attribution_values:
            active_attributions.add_attribution(attribution_value)

        return ParameterDocumentation(identifier, active_attributions)

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


class Attribution(ABC):
    def __init__(self, identifier: str,
                 conflicting_identifiers: Optional[Set[str]]) -> None:
        self.identifier = identifier
        self.conflicting_identifiers = \
            conflicting_identifiers \
            if conflicting_identifiers is not None \
            else frozenset()

    def conflicts_with(self, identifier: str) -> bool:
        return identifier in self.conflicting_identifiers


class KeywordAttribution(Attribution):
    def __init__(self, identifier: str,
                 conflicting_identifiers: Optional[Set[str]] = None):
        super().__init__(identifier, conflicting_identifiers)


class PositiveIntAttribution(Attribution):
    def __init__(self, identifier: str, value: Optional[str],
                 conflicting_identifiers: Optional[Set[str]] = None):
        super().__init__(identifier, conflicting_identifiers)
        if value is None:
            raise MockGeneratorError(
                '{} attribution requires a value (pass with =x)'
                .format(self.identifier))
        try:
            self.value = int(value)
        except ValueError:
            self.raise_illegal_value()

        if self.value <= 0:
            self.raise_illegal_value()

    def raise_illegal_value(self) -> None:
        raise MockGeneratorError(
            'The value of the {} attribution needs to be a positive integer '
            '(>0)'.format(self.identifier))


class StringAttribution(Attribution):
    def __init__(self, identifier: str, value: Optional[str],
                 conflicting_identifiers: Optional[Set[str]] = None):
        super().__init__(identifier, conflicting_identifiers)
        if value is None:
            raise MockGeneratorError(
                '{} attribution requires a value (pass with =x)'
                .format(self.identifier))
        self.value = value
