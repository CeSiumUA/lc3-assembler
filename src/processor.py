import re
import instructions
from io import TextIOWrapper

class Processor:
    def __init__(self, fd: TextIOWrapper) -> None:
        self.asm_fd = fd

    def parse_line(line: str):
        pass

    def sanitize_line(self, line: str):
        comment_re_rule = r';(.*)'
        line = re.sub(comment_re_rule, '', line)
        if line == '':
            return None

    def first_pass(self):
        while True:
            ln = self.asm_fd.readline().strip()
            if not ln:
                break
            ln = self.sanitize_line(ln)
            if ln is None:
                continue
            


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