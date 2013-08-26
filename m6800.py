
# accumulator A (8-bit)
# accumulator B (8-bit)
# index register (16-bit)
# program counter (16-bit)
# stack pointer (16-bit)
# condition codes register (6-bit) HINZVC


# addressing modes:
# - inherent
# - immediate
# - direct (zero-page)
# - extended
# - relative (signed)
# - indexed


class A:
    def __init__(self, cpu):
        self.cpu = cpu
    def get(self):
        return self.cpu.accumulator_a
    def set(self, value):
        self.cpu.accumulator_a = value


class B:
    def __init__(self, cpu):
        self.cpu = cpu
    def get(self):
        return self.cpu.accumulator_b
    def set(self, value):
        self.cpu.accumulator_b = value


class CPU:
    
    def __init__(self, memory):
        self.memory = memory
        
        self.accumulator_a = 0x00
        self.accumulator_b = 0x00
        self.index_register = 0x0000
        self.program_counter = 0x0000
        self.stack_point = 0x0000
        
        self.flag_H = 0
        self.flag_I = 0
        self.flag_N = 0
        self.flag_Z = 0
        self.flag_V = 0
        self.flag_C = 0
    
    ####
    
    # @@@ shared
    def get_pc(self, inc=1):
        pc = self.program_counter
        self.program_counter += inc
        return pc
    
    # @@@
    def read_byte(self, address):
        return self.memory.read_byte(address)
    
    # def read_word(self, address):
    #     return self.memory.read_word(address)
    
    # @@@ shared
    def read_pc_byte(self):
        return self.read_byte(self.get_pc())
    
    # def read_pc_word(self):
    #     return self.read_word(self.get_pc(2))

    # def write_byte(self, address, value):
    #     self.memory.write_byte(address, value)
    
    def test_run(self, start, end):
        self.program_counter = start
        while True:
            if self.program_counter == end:
                break
            self.op(self.read_pc_byte())
    
    ####
    
    def op(self, opcode):
        if opcode & 0x80: # 1.......
            return [
                "SUB", "CMP", "SBC", None ,
                "AND", "BIT", self.LDA, "STA",
                "EOR", "ADC", "ORA", self.ADD,
                "CPX/!", "BSR/HCF/JSR/JSR/!", "LDS/LDX", "STS/STX",
            ][opcode & 0x0F](
                [A, B][(opcode & 0x40) >> 6](self),
                [self.immediate, "D", "X", "E"][(opcode & 0x30) >> 4]()
            )
        else: # 0.......
            if opcode & 0x40: # 01......
                return [
                    "NEG", None , None , "COM",
                    "LSR", None , "ROR", "ASR",
                    "ASL", "ROL", "DEC", None ,
                    "INC", "TST", "JMP", self.CLR,
                ][opcode & 0x0F](
                    [A, B, "M", "E"][(opcode & 0x30) >> 4](self)
                )
            else: # 00......
                if opcode & 0x20: # 001.....
                    if opcode & 0x10: # 0011....
                        if opcode & 0x08: # 00111...
                            operation = opcode & 0x07
                            return [
                                None , "RTS", None , "RTI",
                                None , None , "WAI", "SWI",
                            ][operation]
                        else: # 00110...
                            operation = opcode & 0x07
                            return [
                                "TSX", "INS", "PUL:A", "PUL:B",
                                "DES", "TXS", "PSH:A", "PSH:B",
                            ][operation]
                    else: # 0010....
                        operation = opcode & 0x0F
                        return [
                            "BRA", None , "BHI", "BLS",
                            "BCC", "BCS", "BNE", "BEQ",
                            "BVC", "BVS", "BPL", "BMI",
                            "BGE", "BLT", "BGT", "BLE",
                        ][operation]
                else: # 000.....
                    if opcode & 0x10: # 0001....
                        return [
                            "SBA", "CBA", None , None ,
                            "NBA", None , "TAB", "TBA",
                            None , "DAA", None , self.ABA,
                            None , None , None , None ,
                        ][opcode & 0x0F]()
                    else: # 0000....
                        if opcode & 0x08: # 00001...
                            operation = opcode & 0x07
                            return [
                                "INX", "DEX", "CLV", "SEV",
                                "CLC", "SEC", "CLI", "SEI",
                            ][operation]
                        else: # 00000...
                            operation = opcode & 0x07
                            return [
                                None , "NOP", None , None ,
                                None , None , "TAP", "TPA",
                            ][operation]
        
        raise Exception("0x{:02X}".format(opcode))
    
    ####
    
    # @@@ shared
    def update_nz(self, value):
        value = value % 0x100
        self.flag_Z = 1 if (value == 0) else 0
        self.flag_N = 1 if ((value & 0x80) != 0) else 0
        return value
    
    # @@@ shared
    def update_nzc(self, value):
        self.flag_C = 1 if (value > 0xFF) else 0
        return self.update_nz(value)
    
    ####
    
    # @@@ shared
    def immediate(self):
        return self.get_pc()
    
    ####
    
    def ABA(self):
        self.accumulator_a = self.update_nzc(self.accumulator_a + self.accumulator_b)
        # @@@ overflow flag
        # @@@ half-carry flag
    
    def ADD(self, accumulator, operand_address):
        accumulator.set(self.update_nzc(accumulator.get() + self.read_byte(operand_address)))
        # @@@ overflow flag
        # @@@ half-carry flag
    
    def CLR(self, what):
        what.set(0x00)
        self.flag_N = 0
        self.flag_Z = 1
        self.flag_V = 0
        self.flag_C = 0
    
    def LDA(self, accumulator, operand_address):
        accumulator.set(self.update_nz(self.read_byte(operand_address)))        
        self.flag_V = 0


class TestMemory:
    def __init__(self, data):
        self.data = data
    
    def read_byte(self, address):
        return self.data[address]


class test_cpu(object):
    def __init__(self, *program):
        self.program = program
        
    def __enter__(self):
        cpu = CPU(TestMemory(self.program))
        cpu.test_run(0, len(self.program))
        return cpu
    
    def __exit__(self, type, value, traceback):
        pass


# LDAA immediate
with test_cpu(0x86, 0x01) as cpu:
    assert cpu.accumulator_a == 0x01

# LDAB immediate
with test_cpu(0xC6, 0x02) as cpu:
    assert cpu.accumulator_b == 0x02

# ABA
with test_cpu(0x86, 0x03, 0xC6, 0x04, 0x1B) as cpu:
    assert cpu.accumulator_a == 0x07

# CLRA
with test_cpu(0x86, 0x01, 0x4F) as cpu:
    assert cpu.accumulator_a == 0x00

# CLRB
with test_cpu(0xC6, 0x02, 0x5F) as cpu:
    assert cpu.accumulator_b == 0x00

# ADDA immediate
with test_cpu(0x86, 0x01, 0x8B, 0x05) as cpu:
    assert cpu.accumulator_a == 0x06

# ADDB immediate
with test_cpu(0xC6, 0x02, 0xCB, 0x05) as cpu:
    assert cpu.accumulator_b == 0x07
