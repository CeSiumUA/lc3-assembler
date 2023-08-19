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

    def sanitize_line(self, line: str):
        comment_re_rule = r';(.*)'
        line = re.sub(comment_re_rule, '', line)
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
                linenum += self.__first_process_directive(tokens, linenum)
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
    
    def __first_process_directive(self, tokens, linenum) -> int:
        if tokens[0] == instructions.LC3_Directive.BLKW:
            return self.__get_int(tokens[1])
        if tokens[0] == instructions.LC3_Directive.STRINGZ:
            return len(tokens[1]) + 1
        return 0

    def __get_int(self, token: str):
        if token[0] == 'x':
            return int(token[1:], 16)
        elif token[0] == '#':
            return int(token[1:])
        else:
            raise BaseException('Invalid number format:', token)

    def __is_directive(self, tokens):
        directives = list(map(lambda c: c.value, instructions.LC3_Directive))
        return tokens[0] in directives
    
    def __is_opcode(self, tokens):
        opcodes = list(map(lambda c: Processor.op_to_str(c), instructions.LC3_Operation))
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