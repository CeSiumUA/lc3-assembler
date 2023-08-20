import re
import instructions
from io import TextIOWrapper

class Processor:
    def __init__(self, fd: TextIOWrapper) -> None:
        self.asm_fd = fd
        self.location_counter = {}
        self.pending_label = None

    def parse_line(line: str):
        pass

    def remove_comments(self, line):
        # Regular expression pattern to match semicolons inside double quotes
        pattern = r'"[^"]*"'

        # Replace semicolons inside double quotes with a placeholder
        placeholders = []
        def replace(match):
            placeholders.append(match.group())
            return f'__PLACEHOLDER{len(placeholders) - 1}__'
        line = re.sub(pattern, replace, line)

        # Remove comments (including those outside strings)
        line = re.sub(r';.*', '', line)

        # Put the placeholders back
        def restore(match):
            index = int(match.group(1))
            return placeholders[index]
        line = re.sub(r'__PLACEHOLDER(\d+)__', restore, line)

        return line.strip()

    def sanitize_line(self, line: str):
        line = self.remove_comments(line)
        if line == '':
            return None
        return line

    def first_pass(self):
        linenum = 0
        while True:
            increment_lc = True
            ln = self.asm_fd.readline().strip()
            if ln is None:
                break
            ln = self.sanitize_line(ln)
            if ln is None:
                continue
            tokens = re.findall(r'\w+', ln)

            if not self.__is_opcode(tokens) and not self.__is_directive(tokens) and not self.__is_trap_code(tokens):
                self.__process_label(tokens, linenum)
                if self.pending_label:
                    continue
                tokens = tokens[1:]
            elif self.pending_label:
                self.location_counter[self.pending_label] = linenum
                self.pending_label = None

            if tokens[0] == instructions.LC3_Directive.ORIGIN.value:
                self.origin = self.__get_int(tokens[1])
                continue
            elif tokens[0] == instructions.LC3_Directive.END.value:
                break

            if self.__is_opcode(tokens):
                pass
            elif self.__is_directive(tokens):
                linenum += self.__first_process_directive(tokens, linenum, ln)
                increment_lc = False
            elif self.__is_trap_code(tokens):
                pass
            else:
                raise BaseException('unknown operation', tokens)

            if increment_lc:
                linenum += 1

    def __process_label(self, tokens, linenum):
        if tokens[0] in self.location_counter:
            raise BaseException('Label', tokens[0], 'already exists')
        if self.pending_label:
            raise BaseException('Label', tokens[0], 'already exists')
        if len(tokens) == 1:
            self.pending_label = tokens[0]
        self.location_counter[tokens[0]] = linenum
    
    def __first_process_directive(self, tokens, linenum: int, ln: str) -> int:
        if tokens[0] == instructions.LC3_Directive.BLKW.value:
            return self.__get_int(tokens[1])
        elif tokens[0] == instructions.LC3_Directive.STRINGZ.value:
            delimiter = instructions.LC3_Directive.STRINGZ.value
            idx = ln.find(delimiter)
            str_seg = ln[idx:].replace(delimiter, '', 1).strip().strip('"')
            return len(str_seg) + 1
        elif tokens[0] == instructions.LC3_Directive.FILL.value:
            return 1
        return 0

    def __get_int(self, token: str):
        if token[0] == 'x':
            return int(token[1:], 16)
        elif token[0] == '#':
            return int(token[1:])
        elif token[0] == 'b':
            return int(token[1:], 2)
        else:
            raise BaseException('Invalid number format:', token)

    def __is_directive(self, tokens):
        directives = list(map(lambda c: c.value, instructions.LC3_Directive))
        return tokens[0] in directives
    
    def __is_opcode(self, tokens: list[str]):
        if tokens[0].startswith('BR'):
            return True
        opcodes = list(map(lambda c: c[0].replace('OP_', ''), instructions.LC3_Operation.__members__.items()))
        return tokens[0] in opcodes

    def __is_trap_code(self, tokens):
        traps = list(map(lambda c: Processor.trap_to_str(c), instructions.LC3_Trap_Code))
        return tokens[0] in traps

    def op_to_str(op_code: instructions.LC3_Operation):
        return op_code.name.replace('OP_', '')
    
    def str_to_op(op: str):
        return instructions.LC3_Operation[('OP_' + op)]
    
    def reg_to_str(reg_code: instructions.LC3_Register):
        return reg_code.name.replace('R_', '')
    
    def str_to_reg(reg: str):
        return instructions.LC3_Register[('R_' + reg)]
    
    def trap_to_str(trap_code: instructions.LC3_Trap_Code):
        return trap_code.name.replace('TRAP_', '')
    
    def str_to_trap(trap: str):
        return instructions.LC3_Trap_Code[('TRAP_' + trap)]