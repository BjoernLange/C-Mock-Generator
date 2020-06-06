class CodeBuilder:
    def __init__(self):
        self.result = ''

    def append(self, *args):
        for something in args:
            self.result = self.result + str(something)
        return self

    def newline(self):
        self.result = self.result + '\n'
        return self

    def indent(self, level: int):
        self.result = self.result + '    ' * level
        return self

    def __str__(self) -> str:
        return self.result
