from S08_asm_tools import constants

START_FILE = 'firmware.asm'


class Operands(object):
    """A list of operands modifying an instruction."""
    def __init__(self, raw_input: str):
        self.raw_input = raw_input
        self.operands = [op.strip() for op in self.raw_input.split(',') if op.strip()]

    def __format__(self, *args, **kwargs):
        return ", ".join(self.operands).__format__(*args, **kwargs)


class Instruction(object):
    """An S08 ASM instruction."""
    def __init__(self, token: str):
        self.token = token

    def __format__(self, *args, **kwargs):
        return self.token.__format__(*args, **kwargs)

    def __repr__(self):
        return f'S08 instruction {self.token}: {self.name}'

    @property
    def name(self):
        return constants.instruction.get(self.token, '')


class Line(object):
    """One line of ASM source code."""

    def __init__(self, line_number: int = 0, source_line: str = ''):
        self.line_number = line_number
        self.source_line = source_line
        self.clean_line = None
        self.label = None
        self.instruction = None
        self.operands = None
        self.comment = None

        self._replacements()
        wip_line = self._separate_comment()
        wip_line = self._separate_label(wip_line=wip_line)
        self._separate_operands(wip_line=wip_line)

    def __str__(self):
        if not self.label and not self.instruction.token and not self.operands:
            return f'{self.comment}'
        else:
            return (
                f'{self.label:15}{self.instruction:10} {self.operands:30} '
                f'; {self.instruction.name}{self.comment}'
            )

    def _replacements(self):
        """ Clean out unwanted tabs and colons. """
        self.clean_line = self.source_line.replace('\t', ' ')
        # The colon in the next three items interferes with parsing
        self.clean_line = self.clean_line.replace('TICKEDG:', 'TICKEDG')
        self.clean_line = self.clean_line.replace('TICKIE:', 'TICKIE')
        self.clean_line = self.clean_line.replace('TICKACK:', 'TICKACK')

    def _separate_comment(self) -> str:
        """ Separate any comments (beginning with a semicolon) from the rest of the line. """
        comment_marker_position = self.clean_line.find(';')  # equals -1 if no semicolon
        comment = self.clean_line[comment_marker_position:] if comment_marker_position >= 0 else ''
        self.comment = comment.strip()
        return self.clean_line[:comment_marker_position].strip()

    def _separate_label(self, wip_line: str) -> str:
        """ Check if there is a label and pull it out of the line. """
        colon_position = wip_line.find(':')
        self.label = wip_line[:colon_position] if colon_position >= 0 else ''
        return wip_line[len(self.label) + 1:].strip() if self.label else wip_line

    def _separate_operands(self, wip_line: str) -> [str]:
        """ Separate the operator and the list of comma-delimited operands. """
        space_position = wip_line.find(' ')
        token = wip_line[:space_position] if space_position >= 0 else wip_line
        self.instruction = Instruction(token=token)
        self.operands = Operands(raw_input=wip_line[len(token) + 1:]) if token else ''


def main():
    with open('formatted_' + START_FILE, 'w') as fout:
        for number, line in enumerate(open(START_FILE, 'r')):
            fout.write(str(Line(line_number=number, source_line=line)) + '\n')



if __name__ == '__main__':
    main()
