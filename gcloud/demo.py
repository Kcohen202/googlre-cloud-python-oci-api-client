# This is demo code, globally disable docstrings.
# pylint: disable=missing-docstring
from code import interact
import itertools
import os.path
import sys
import time


class DemoRunner(object):
    """An interactive runner of demo scripts."""

    KEYPRESS_DELAY = 0.05
    GLOBALS, LOCALS = globals(), locals()
    CODE, COMMENT = 'code', 'comment'

    def __init__(self, fp):
        self.lines = [line.rstrip() for line in fp.readlines()]

    @classmethod
    def from_module(cls, module):
        path = os.path.join(os.path.dirname(module.__file__),
                            'demo', 'demo.py')

        return cls(open(path, 'r'))

    def run(self):
        line_groups = itertools.groupby(self.lines, self.get_line_type)

        for group_type, lines in line_groups:
            if group_type == self.COMMENT:
                self.write(lines)

            elif group_type == self.CODE:
                self.code(lines)

        interact('(Hit CTRL-D to exit...)', local=self.LOCALS)

    @staticmethod
    def wait():
        raw_input()

    @classmethod
    def get_line_type(cls, line):
        if line.startswith('#'):
            return cls.COMMENT
        else:
            return cls.CODE

    @staticmethod
    def get_indent_level(line):
        if not line.strip():
            return None
        return len(line) - len(line.lstrip())

    def write(self, lines):
        print
        print '\n'.join(lines),
        self.wait()

    def code(self, lines):
        code_lines = []

        for line in lines:
            indent = self.get_indent_level(line)

            # If we've completed a block,
            # run whatever code was built up in code_lines.
            if indent == 0:
                self._execute_lines(code_lines)
                code_lines = []

            # Print the prefix for the line depending on the indentation level.
            if indent == 0:
                print '>>> ',
            elif indent > 0:
                print '\n... ',
            elif indent is None:
                continue

            # Break the line into the code section and the comment section.
            if '#' in line:
                code, comment = line.split('#', 2)
            else:
                code, comment = line, None

            # 'Type' out the comment section.
            for char in code.rstrip():
                time.sleep(self.KEYPRESS_DELAY)
                sys.stdout.write(char)
                sys.stdout.flush()

            # Print the comment section (not typed out).
            if comment:
                sys.stdout.write('  # %s' % comment.strip())

            # Add the current line to the list of lines to be run
            # in this block.
            code_lines.append(line)

        # If we had any code built up that wasn't part of a completed block
        # (ie, the lines ended with an indented line),
        # run that code.
        if code_lines:
            self._execute_lines(code_lines)

    def _execute_lines(self, lines):
        if lines:
            self.wait()

            # Yes, this is crazy unsafe... but it's demo code.
            # pylint: disable=exec-used
            exec('\n'.join(lines), self.GLOBALS, self.LOCALS)
            # pylint: enable=exec-used
