from enum import Enum

class LC3_Directive(Enum):
    ORIGIN = 'ORIG'
    END = 'END'
    BLKW = 'BLKW'
    FILL = 'FILL'
    STRINGZ = 'STRINGZ'

class LC3_Operation(Enum):
    OP_BR = 0
    OP_ADD = 1
    OP_LD = 2
    OP_ST = 3
    OP_JSR = 4
    OP_AND = 5
    OP_LDR = 6
    OP_STR = 7
    OP_RTI = 8
    OP_NOT = 9
    OP_LDI = 10
    OP_STI = 11
    OP_JMP = 12
    OP_RES = 13
    OP_LEA = 14
    OP_TRAP = 15

class LC3_Register(Enum):
    R_R0 = 0
    R_R1 = 1
    R_R2 = 2
    R_R3 = 3
    R_R4 = 4
    R_R5 = 5
    R_R6 = 6
    R_R7 = 7
    R_PC = 8
    R_COND = 9
    R_COUNT = 10

class LC3_Trap_Code(Enum):
    TRAP_GETC = (0x20)
    TRAP_OUT = (0x21)
    TRAP_PUTS = (0x22)
    TRAP_IN = (0x23)
    TRAP_PUTSP = (0x24)
    TRAP_HALT = (0x25)

class LC3_Condition_Flag(Enum):
    FL_POS = (1 << 0)
    FL_ZRO = (1 << 1)
    FL_NEG = (1 << 2)

class LC3_MMR(Enum):
    MR_KBSR = (0xFE00)
    MR_KBDR = (0xFE02)