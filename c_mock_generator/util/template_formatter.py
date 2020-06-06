from typing import List, Iterable
import itertools


class MissingAttrException(Exception):
    pass


def get_attribute(object_tree, attribute_name: str):
    try:
        return getattr(object_tree, attribute_name)
    except AttributeError:
        raise MissingAttrException('{} has no attribute named {}'
                                   .format(object_tree, attribute_name))


class CodeLinesIterator:
    def __init__(self, iterable: Iterable):
        self.__iterator = iter(iterable)
        self.__top_element = None
        self.__finished = False

    @property
    def top(self):
        if self.__top_element is None:
            self.pop()
        if self.__finished:
            raise StopIteration()
        return self.__top_element

    def pop(self):
        try:
            self.__top_element = next(self.__iterator)
        except StopIteration:
            self.__top_element = None
            self.__finished = True

    def replace_placeholders_in_top(self, object_tree):
        while self.__top_contains_placeholder():
            self.__replace_first_placeholder_in_top(object_tree)

    def __top_contains_placeholder(self) -> bool:
        return '<<<' in self.top and '>>>' in self.top

    def __replace_first_placeholder_in_top(self, object_tree):
        placeholder = self.__get_first_placeholder_in_top()
        self.__top_element = placeholder.replace_in_text(self.top, object_tree)

    def __get_first_placeholder_in_top(self):
        name = self.top[self.top.index('<<<') + 3:self.top.index('>>>')]
        return Placeholder(name)

    def is_top_for_all_statement(self) -> bool:
        return self.top.strip().startswith('<<<FORALL')

    def is_top_end_for_all_statement(self) -> bool:
        return self.top.strip() == '<<<ENDFORALL>>>'

    def parse_for_all_section(self):
        if ' JOINING ' not in self.top:
            attribute_name = self.top.strip()[10:-3]
            separator = '\n'
        else:
            text = self.top.strip()
            attribute_name = text[10:text.index(' JOINING ')]
            separator = text[text.index(' JOINING ') + 9:-3]
            while '<newline>' in separator:
                separator = separator.replace('<newline>', '\n')
        self.pop()
        content = self.__retrieve_till_end_line_is_reached(
            self.is_top_for_all_statement, self.is_top_end_for_all_statement)
        return ForAll(attribute_name, separator, content)

    def __retrieve_till_end_line_is_reached(self, is_top_start_line,
                                            is_top_end_line) -> List[str]:
        level = 1
        lines = []
        while True:
            if is_top_end_line():
                if level == 1:
                    self.pop()
                    break
                level = level - 1

            if is_top_start_line():
                level = level + 1

            lines.append(self.top)
            self.pop()
        return lines

    def is_top_if_statement(self) -> bool:
        return self.top.strip().startswith('<<<IF')

    def is_top_end_if_statement(self) -> bool:
        return self.top.strip() == '<<<ENDIF>>>'

    def parse_if_section(self):
        attr_name = self.top.strip()[6:-3]
        self.pop()
        lines = self.__retrieve_till_end_line_is_reached(
            self.is_top_if_statement, self.is_top_end_if_statement)
        return If(attr_name, lines)


class Placeholder:
    def __init__(self, name: str):
        self.name = name

    @property
    def raw_name(self) -> str:
        return '<<<' + self.name + '>>>'

    def replace_in_text(self, text: str, object_tree) -> str:
        return text.replace(self.raw_name,
                            str(get_attribute(object_tree, self.name)))


class FormattedCodeBlocks:
    def __init__(self, formatted: List[List[str]]):
        self.formatted = formatted

    def is_empty(self):
        return not self.formatted

    def join_multi_line_blocks(self) -> List[str]:
        return ['\n'.join(x) for x in self.formatted]


class ForAll:
    def __init__(self, attribute_name: str, separator: str,
                 content: List[str]):
        self.attribute_name = attribute_name
        self.separator = separator
        self.content = content

    def format(self, object_tree) -> List[str]:
        children = self.get_attribute(object_tree)
        code_blocks = TemplateFormatter(self.content).format_multiple(children)
        return self.post_process(code_blocks)

    def get_attribute(self, object_tree):
        return get_attribute(object_tree, self.attribute_name)

    def post_process(self, code_blocks: FormattedCodeBlocks) -> List[str]:
        if code_blocks.is_empty():
            return []

        lines = code_blocks.join_multi_line_blocks()
        if '\n' not in self.separator:
            lines = self.strip_whitespaces_for_formatting(lines)
        joined = [self.separator.join(lines)]
        return list(itertools.chain(*[x.split('\n') for x in joined]))

    def strip_whitespaces_for_formatting(self, formatted: List[str]) \
            -> List[str]:
        formatted[0] = formatted[0].rstrip()
        for i in range(1, len(formatted)):
            formatted[i] = formatted[i].strip()
        return formatted


class If:
    def __init__(self, attribute_name: str, content: List[str]):
        self.attribute_name = attribute_name
        self.content = content


class TemplateFormatter:
    def __init__(self, template_code_lines: Iterable[str]) -> None:
        self.template_code_lines = template_code_lines
        self.lines_it = CodeLinesIterator([])

    def format(self, object_tree) -> Iterable[str]:
        self.lines_it = CodeLinesIterator(self.template_code_lines)
        result = []
        try:
            while True:
                result.extend(self.format_chunk_of_lines(object_tree))
        except StopIteration:
            pass
        return result

    def format_multiple(self, object_trees: List) -> FormattedCodeBlocks:
        result = []
        for object_tree in object_trees:
            formatted = list(self.format(object_tree))
            if formatted:
                result.append(formatted)
        return FormattedCodeBlocks(result)

    def format_chunk_of_lines(self, object_tree) -> List[str]:
        if self.lines_it.is_top_for_all_statement():
            return self.format_for_all(object_tree)
        if self.lines_it.is_top_if_statement():
            return self.format_if(object_tree)
        return self.format_single_line(object_tree)

    def format_single_line(self, object_tree) -> List[str]:
        self.lines_it.replace_placeholders_in_top(object_tree)
        result = [self.lines_it.top]
        self.lines_it.pop()
        return result

    def format_for_all(self, object_tree) -> List[str]:
        return self.lines_it.parse_for_all_section().format(object_tree)

    def format_if(self, object_tree) -> List[str]:
        if_statement = self.lines_it.parse_if_section()
        attr_value = get_attribute(object_tree, if_statement.attribute_name)
        if not attr_value:
            return []

        formatter = TemplateFormatter(if_statement.content)
        return list(formatter.format(object_tree))
