def from_twos_comp(val):
    assert 0x00 <= val <= 0xFF
    return -((0xFF ^ val) + 1) if val >= 0x80 else val


def to_twos_comp(val):
    assert -128 <= val <= 127
    return 0xFF ^ -(val + 1) if val < 0 else val


class Z80:

    def __init__(self):
        self.memory = [0] * 0x10000
        self.reg_A = 0x00
        self.reg_B = 0x00
        self.reg_C = 0x00
        self.reg_D = 0x00
        self.reg_E = 0x00
        self.reg_H = 0x00
        self.reg_L = 0x00
        self.reg_A_shadow = 0x00
        self.reg_F_shadow = 0x00
        self.reg_B_shadow = 0x00
        self.reg_C_shadow = 0x00
        self.reg_D_shadow = 0x00
        self.reg_E_shadow = 0x00
        self.reg_H_shadow = 0x00
        self.reg_L_shadow = 0x00
        self.flag_S = 0
        self.flag_Z = 0
        self.flag_X5 = 0
        self.flag_H = 0
        self.flag_X3 = 0
        self.flag_PV = 0
        self.flag_N = 0
        self.flag_C = 0
        self.reg_IX = 0
        self.reg_IY = 0
        self.reg_SP = 0  # @@@

    def read_mem16(self, addr):
        lo = self.memory[addr]
        hi = self.memory[addr + 1]
        return (hi << 8) + lo

    def write_mem16(self, addr, val):
        hi, lo = divmod(val, 0x100)
        self.memory[addr] = lo
        self.memory[addr + 1] = hi

    def get_PC(self):
        addr = self.PC
        self.PC += 1  # 16-bit overflow @@@
        return addr

    def read_PC(self):
        return self.memory[self.get_PC()]

    def read16_PC(self):
        lo = self.read_PC()
        hi = self.read_PC()
        return (hi << 8) + lo

    def push16(self, val):
        hi, lo = divmod(val, 0x100)
        self.reg_SP -= 1
        self.memory[self.reg_SP] = hi
        self.reg_SP -= 1
        self.memory[self.reg_SP] = lo

    def pop16(self):
        lo = self.memory[self.reg_SP]
        self.reg_SP += 1
        hi = self.memory[self.reg_SP]
        self.reg_SP += 1
        return (hi << 8) + lo

    def get_reg_A(self):
        return self.reg_A

    def get_reg_F(self):
        f = (self.flag_S << 7) + \
            (self.flag_Z << 6) + \
            (self.flag_X5 << 5) + \
            (self.flag_H << 4) + \
            (self.flag_X3 << 3) + \
            (self.flag_PV << 2) + \
            (self.flag_N << 1) + \
            (self.flag_C << 0)
        return f

    def get_reg_B(self):
        return self.reg_B

    def get_reg_C(self):
        return self.reg_C

    def get_reg_D(self):
        return self.reg_D

    def get_reg_E(self):
        return self.reg_E

    def get_reg_H(self):
        return self.reg_H

    def get_reg_L(self):
        return self.reg_L

    def get_reg_pair_AF(self):
        return (self.reg_A << 8) + self.get_reg_F()

    def get_reg_pair_AF_shadow(self):
        return (self.reg_A_shadow << 8) + self.reg_F_shadow

    def get_reg_pair_BC(self):
        return (self.reg_B << 8) + self.reg_C

    def get_reg_pair_BC_shadow(self):
        return (self.reg_B_shadow << 8) + self.reg_C_shadow

    def get_reg_pair_DE(self):
        return (self.reg_D << 8) + self.reg_E

    def get_reg_pair_DE_shadow(self):
        return (self.reg_D_shadow << 8) + self.reg_E_shadow

    def get_reg_pair_HL(self):
        return (self.reg_H << 8) + self.reg_L

    def get_reg_pair_HL_shadow(self):
        return (self.reg_H_shadow << 8) + self.reg_L_shadow

    def get_indirect_HL(self):
        return self.memory[self.get_reg_pair_HL()]

    def get_reg_IX(self):
        return self.reg_IX

    def get_reg_IY(self):
        return self.reg_IY

    def get_reg_SP(self):
        return self.reg_SP

    def set_reg_A(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_A = val

    def set_reg_F(self, val):
        assert 0x00 <= val <= 0xFF
        self.flag_S = (0b10000000 & val) >> 7
        self.flag_Z = (0b01000000 & val) >> 6
        self.flag_X5 = (0b00100000 & val) >> 5
        self.flag_H = (0b00010000 & val) >> 4
        self.flag_X3 = (0b00001000 & val) >> 3
        self.flag_PV = (0b00000100 & val) >> 2
        self.flag_N = (0b00000010 & val) >> 1
        self.flag_C = (0b00000001 & val) >> 0
        assert val == self.get_reg_F()

    def set_reg_B(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_B = val

    def set_reg_C(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_C = val

    def set_reg_D(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_D = val

    def set_reg_E(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_E = val

    def set_reg_H(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_H = val

    def set_reg_L(self, val):
        assert 0x00 <= val <= 0xFF
        self.reg_L = val

    def set_reg_pair_AF(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_A, f = divmod(val, 0x100)
        self.set_reg_F(f)

    def set_reg_pair_AF_shadow(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_A_shadow, self.reg_F_shadow = divmod(val, 0x100)

    def set_reg_pair_BC(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_B, self.reg_C = divmod(val, 0x100)

    def set_reg_pair_BC_shadow(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_B_shadow, self.reg_C_shadow = divmod(val, 0x100)

    def set_reg_pair_DE(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_D, self.reg_E = divmod(val, 0x100)

    def set_reg_pair_DE_shadow(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_D_shadow, self.reg_E_shadow = divmod(val, 0x100)

    def set_reg_pair_HL(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_H, self.reg_L = divmod(val, 0x100)

    def set_reg_pair_HL_shadow(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_H_shadow, self.reg_L_shadow = divmod(val, 0x100)

    def set_indirect_HL(self, val):
        assert 0x00 <= val <= 0xFF
        self.memory[self.get_reg_pair_HL()] = val

    def set_reg_IX(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_IX = val

    def set_reg_IY(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_IY = val

    def set_reg_SP(self, val):
        assert 0x00 <= val <= 0xFFFF
        self.reg_SP = val

    def reg_getter(self, bitcode):
        return [
            self.get_reg_B, self.get_reg_C, self.get_reg_D, self.get_reg_E,
            self.get_reg_H, self.get_reg_L, self.get_indirect_HL, self.get_reg_A][bitcode]

    def reg_setter(self, bitcode):
        return [
            self.set_reg_B, self.set_reg_C, self.set_reg_D, self.set_reg_E,
            self.set_reg_H, self.set_reg_L, self.set_indirect_HL, self.set_reg_A][bitcode]

    def reg_pair_getter(self, bitcode):
        return [
            self.get_reg_pair_BC, self.get_reg_pair_DE, self.get_reg_pair_HL,
            self.get_reg_SP][bitcode]

    def reg_pair_getter2(self, bitcode):
        return [
            self.get_reg_pair_BC, self.get_reg_pair_DE, self.get_reg_pair_HL,
            self.get_reg_pair_AF][bitcode]

    def reg_pair_setter(self, bitcode):
        return [
            self.set_reg_pair_BC, self.set_reg_pair_DE, self.set_reg_pair_HL,
            self.set_reg_SP][bitcode]

    def mem_setter(self, addr):
        def set_mem(val):
            self.memory[addr] = val
        return set_mem

    def mem_getter(self, addr):
        def get_mem():
            return self.memory[addr]
        return get_mem

    def LDI(self):
        self.memory[self.get_reg_pair_DE()] = self.memory[self.get_reg_pair_HL()]
        self.set_reg_pair_DE(self.get_reg_pair_DE() + 1)
        self.set_reg_pair_HL(self.get_reg_pair_HL() + 1)
        self.set_reg_pair_BC(self.get_reg_pair_BC() - 1)
        # @@@ should flags go before inc/dec?
        self.flag_H = 0
        self.flag_PV = 1 if self.get_reg_pair_BC() - 1 != 0 else 0
        self.flag_N = 0

    def LDD(self):
        self.memory[self.get_reg_pair_DE()] = self.memory[self.get_reg_pair_HL()]
        self.set_reg_pair_DE(self.get_reg_pair_DE() - 1)
        self.set_reg_pair_HL(self.get_reg_pair_HL() - 1)
        self.set_reg_pair_BC(self.get_reg_pair_BC() - 1)
        # @@@ should flags go before inc/dec?
        self.flag_H = 0
        self.flag_PV = 1 if self.get_reg_pair_BC() - 1 != 0 else 0
        self.flag_N = 0

    def CPI(self):
        tmp1 = self.memory[self.get_reg_pair_HL()]
        tmp2 = self.get_reg_A()
        self.flag_S = 1 if tmp2 > tmp1 else 0
        self.flag_Z = 1 if tmp2 == tmp1 else 0
        self.flag_H = 0  # @@@
        self.flag_PV = 1 if self.get_reg_pair_BC() - 1 != 0 else 0
        self.flag_N = 1
        self.set_reg_pair_HL(self.get_reg_pair_HL() + 1)
        self.set_reg_pair_BC(self.get_reg_pair_BC() - 1)

    def CPD(self):
        tmp1 = self.memory[self.get_reg_pair_HL()]
        tmp2 = self.get_reg_A()
        self.flag_S = 1 if tmp2 > tmp1 else 0
        self.flag_Z = 1 if tmp2 == tmp1 else 0
        self.flag_H = 0  # @@@
        self.flag_PV = 1 if self.get_reg_pair_BC() - 1 != 0 else 0
        self.flag_N = 1
        self.set_reg_pair_HL(self.get_reg_pair_HL() - 1)
        self.set_reg_pair_BC(self.get_reg_pair_BC() - 1)

    def ADD(self, augend):
        val = from_twos_comp(self.get_reg_A()) + from_twos_comp(augend)
        self.flag_S = 1 if val < 0 else 0
        self.flag_Z = 1 if val == 0 else 0
        self.flag_H = 1 if True else 0  # @@@
        self.flag_PV = 0 if -128 <= val <= 127 else 1
        self.flag_N = 0
        self.flag_C = 1 if True else 0  # @@@
        self.set_reg_A(to_twos_comp(val))

    def ADC(self, augend):
        assert self.flag_C in [0, 1]
        self.ADD(augend + self.flag_C)

    def SUB(self, subtrahend):
        val = from_twos_comp(self.get_reg_A()) - from_twos_comp(subtrahend)
        self.flag_S = 1 if val < 0 else 0
        self.flag_Z = 1 if val == 0 else 0
        self.flag_H = 1 if True else 0  # @@@
        self.flag_PV = 0 if -128 <= val <= 127 else 1
        self.flag_N = 1
        self.flag_C = 1 if True else 0  # @@@
        self.set_reg_A(to_twos_comp(val))

    def SBC(self, subtrahend):
        assert self.flag_C in [0, 1]
        self.SUB(subtrahend + self.flag_C)

    def AND(self, operand):
        val = self.get_reg_A() & operand
        # @@@ flags
        self.set_reg_A(val)

    def OR(self, operand):
        val = self.get_reg_A() | operand
        # @@@ flags
        self.set_reg_A(val)

    def XOR(self, operand):
        val = self.get_reg_A() ^ operand
        # @@@ flags
        self.set_reg_A(val)

    def CP(self, operand):
        val = from_twos_comp(self.get_reg_A()) - from_twos_comp(operand)
        self.flag_S = 1 if val < 0 else 0
        self.flag_Z = 1 if val == 0 else 0
        self.flag_H = 1 if True else 0  # @@@
        self.flag_PV = 0 if -128 <= val <= 127 else 1
        self.flag_N = 1
        self.flag_C = 1 if True else 0  # @@@

    def run(self):
        self.PC = 0x0000

        op = self.read_PC()

        prefix = None

        if op == 0xDD:
            prefix = 0xDD
            op = self.read_PC()
        elif op == 0xFD:
            prefix = 0xFD
            op = self.read_PC()
        elif op == 0xED:
            prefix = 0xED
            op = self.read_PC()

        op_x = (0b11000000 & op) >> 6
        op_p = (0b00110000 & op) >> 4
        op_y = (0b00111000 & op) >> 3
        op_q = (0b00001111 & op)
        op_z = (0b00000111 & op)

        if op_x == 0b00:
            if op == 0b00000010:  # 0x02
                addr = self.get_reg_pair_BC()
                self.memory[addr] = self.get_reg_A()
            elif op == 0b00001000:  # 0x08
                # EX AF,AF'
                tmp = self.get_reg_pair_AF_shadow()
                self.set_reg_pair_AF_shadow(self.get_reg_pair_AF())
                self.set_reg_pair_AF(tmp)
            elif op == 0b00001010:  # 0x0A
                addr = self.get_reg_pair_BC()
                self.set_reg_A(self.memory[addr])
            elif op == 0b00010010:  # 0x12
                addr = self.get_reg_pair_DE()
                self.memory[addr] = self.get_reg_A()
            elif op == 0b00011010:  # 0x1A
                addr = self.get_reg_pair_DE()
                self.set_reg_A(self.memory[addr])
            elif op == 0b00100001:  # 0x21
                if prefix == 0xDD:
                    setter = self.set_reg_IX
                elif prefix == 0xFD:
                    setter = self.set_reg_IY
                else:
                    setter = self.set_reg_pair_HL
                setter(self.read16_PC())
            elif op == 0b00100010:  # 0x22
                if prefix == 0xDD:
                    getter = self.get_reg_IX
                elif prefix == 0xFD:
                    getter = self.get_reg_IY
                else:
                    getter = self.get_reg_pair_HL
                addr = self.read16_PC()
                self.write_mem16(addr, getter())
            elif op == 0b00101010:  # 0x2A
                if prefix == 0xDD:
                    setter = self.set_reg_IX
                elif prefix == 0xFD:
                    setter = self.set_reg_IY
                else:
                    setter = self.set_reg_pair_HL
                addr = self.read16_PC()
                setter(self.read_mem16(addr))
            elif op == 0b00110010:  # 0x32
                addr = self.read16_PC()
                self.memory[addr] = self.get_reg_A()
            elif op == 0b00110110:  # 0x36
                if prefix == 0xDD:
                    addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                elif prefix == 0xFD:
                    addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                else:
                    addr = self.get_reg_pair_HL()
                self.memory[addr] = self.read_PC()
            elif op == 0b00111010:  # 0x3A
                addr = self.read16_PC()
                self.set_reg_A(self.memory[addr])
            elif op_q == 0b0001:  # LD rr,nn
                self.reg_pair_setter(op_p)(self.read16_PC())
            elif op_z == 0b100:  # INC m
                # @@@ can this be reused:
                if prefix == 0xDD or prefix == 0xFD:
                    if prefix == 0xDD:
                        addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                    elif prefix == 0xFD:
                        addr = self.get_reg_IY() + from_twos_comp(self.read_PC())

                    getter = self.mem_getter(addr)
                    setter = self.mem_setter(addr)
                else:
                    getter = self.reg_getter(op_y)
                    setter = self.reg_setter(op_y)
                # @@@ ???
                prev_val = getter()
                val = prev_val + 1  # @@@ handle overflow
                setter(val)
                self.flag_S = 1 if val < 0 else 0  # @@@
                self.flag_Z = 1 if val == 0 else 0
                self.flag_H = 1 if True else 0  # @@@
                self.flag_PV = 1 if prev_val == 0x7F else 0
                self.flag_N = 0
                # flag_C not affected
            elif op_z == 0b101:  # DEC m
                # @@@ can this be reused:
                if prefix == 0xDD or prefix == 0xFD:
                    if prefix == 0xDD:
                        addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                    elif prefix == 0xFD:
                        addr = self.get_reg_IY() + from_twos_comp(self.read_PC())

                    getter = self.mem_getter(addr)
                    setter = self.mem_setter(addr)
                else:
                    getter = self.reg_getter(op_y)
                    setter = self.reg_setter(op_y)
                # @@@ ???
                prev_val = getter()
                val = prev_val - 1  # @@@ handle overflow
                setter(val)
                self.flag_S = 1 if val < 0 else 0  # @@@
                self.flag_Z = 1 if val == 0 else 0
                self.flag_H = 1 if True else 0  # @@@
                self.flag_PV = 1 if prev_val == 0x80 else 0
                self.flag_N = 0
                # flag_C not affected
            elif op_z == 0b110:  # LD r,n
                self.reg_setter(op_y)(self.read_PC())
            else:
                raise Exception("unknown operand")

        elif op_x == 0b01:  # LD r,r
            if prefix == 0xED:
                if op_q == 0b0011:  # LD (nn),dd
                    addr = self.read16_PC()
                    self.write_mem16(addr, self.reg_pair_getter(op_p)())
                elif op_q == 0b1011:  # LD dd,(nn)
                    addr = self.read16_PC()
                    self.reg_pair_setter(op_p)(self.read_mem16(addr))
                else:
                    raise Exception("unknown operand")
            else:
                set_code = op_y
                get_code = op_z

                if prefix == 0xDD or prefix == 0xFD:
                    if prefix == 0xDD:
                        addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                    elif prefix == 0xFD:
                        addr = self.get_reg_IY() + from_twos_comp(self.read_PC())

                    if get_code == 0b110:
                        setter = self.reg_setter(set_code)(self.mem_getter(addr)())
                    elif set_code == 0b110:
                        setter = self.mem_setter(addr)(self.reg_getter(get_code)())
                    else:
                        raise Exception("unknown operand")
                else:
                    setter = self.reg_setter(set_code)(self.reg_getter(get_code)())

        elif op_x == 0b10:
            if prefix == 0xED:
                if op == 0b10100000:  # 0xA0
                    # LDI
                    self.LDI()
                elif op == 0b10100001:  # 0xA1
                    # CPI
                    self.CPI()
                elif op == 0b10101000:  # 0xA8
                    # LDD
                    self.LDD()
                elif op == 0b10101001:  # 0xA9
                    # CPD
                    self.CPD()
                elif op == 0b10110000:  # 0xB0
                    while True:
                        self.LDI()
                        if self.get_reg_pair_BC() == 0x00:
                            break
                        else:
                            pass  # @@@ PC decrement?
                elif op == 0b10110001:  # 0bB1
                    while True:
                        self.CPI()
                        if self.get_reg_pair_BC() == 0x00 or self.flag_Z == 1:
                            break
                        else:
                            pass  # @@@ PC decrement?
                elif op == 0b10111000:  # 0xB8
                    while True:
                        self.LDD()
                        if self.get_reg_pair_BC() == 0:
                            break
                        else:
                            pass  # @@@ PC decrement?
                elif op == 0b10111001:  # 0xB9
                    while True:
                        self.CPD()
                        if self.get_reg_pair_BC() == 0x00 or self.flag_Z == 1:
                            break
                        else:
                            pass  # @@@ PC decrement?
                else:
                    raise Exception("unknown operand")
            else:
                if op_y == 0b000:
                    if prefix == 0xDD:
                        if op_z == 0b110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            augend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op_z == 0b110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            augend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:  # ADD A,r
                        augend = self.reg_getter(op_z)()

                    self.ADD(augend)

                elif op_y == 0b001:
                    if prefix == 0xDD:
                        if op_z == 0b110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            augend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op_z == 0b110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            augend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:
                        augend = self.reg_getter(op_z)()

                    self.ADC(augend)

                elif op_y == 0b010:  # how can this be merged with ADD? @@@
                    if prefix == 0xDD:
                        if op_z == 0x110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            subtrahend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op_z == 0x110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            subtrahend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:
                        subtrahend = self.reg_getter(op_z)()

                    self.SUB(subtrahend)

                elif op_y == 0b011:  # how can this be merged with ADD? @@@
                    if prefix == 0xDD:
                        if op == 0x110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            subtrahend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op == 0x110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            subtrahend = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:
                        subtrahend = self.reg_getter(op_z)()

                    self.SBC(subtrahend)

                elif op_y == 0b100:  # how can this be merged with ADD? @@@
                    if prefix == 0xDD:
                        if op == 0x110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            val = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op == 0x110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            val = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:
                        val = self.reg_getter(op_z)()

                    self.AND(val)

                elif op_y == 0b101:  # how can this be merged with ADD? @@@
                    if prefix == 0xDD:
                        if op == 0x110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            val = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op == 0x110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            val = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:
                        val = self.reg_getter(op_z)()

                    self.XOR(val)

                elif op_y == 0b110:  # how can this be merged with ADD? @@@
                    if prefix == 0xDD:
                        if op == 0x110:
                            addr = self.get_reg_IX() + from_twos_comp(self.read_PC())
                            val = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    elif prefix == 0xFD:
                        if op == 0x110:
                            addr = self.get_reg_IY() + from_twos_comp(self.read_PC())
                            val = self.memory[addr]
                        else:
                            raise Exception("unknown operand")
                    else:
                        val = self.reg_getter(op_z)()

                    self.OR(val)

                else:
                    raise Exception("unknown operand")

        elif op_x == 0b11:

            if op_q == 0b0001:  # POP
                if prefix == 0xDD:
                    if op == 0b11100001:  # 0xE1
                        setter = self.set_reg_IX
                    else:
                        raise Exception("unknown operand")
                elif prefix == 0xFD:
                    if op == 0b11100001:  # 0xE1
                        setter = self.set_reg_IY
                    else:
                        raise Exception("unknown operand")
                else:
                    setter = self.reg_pair_setter(op_p)

                setter(self.pop16())

            elif op_q == 0b0101:  # PUSH
                if prefix == 0xDD:
                    if op == 0b11100101:  # 0xE5
                        getter = self.get_reg_IX
                    else:
                        raise Exception("unknown operand")
                elif prefix == 0xFD:
                    if op == 0b11100101:  # 0xE5
                        getter = self.get_reg_IY
                    else:
                        raise Exception("unknown operand")
                else:
                    getter = self.reg_pair_getter2(op_p)

                self.push16(getter())

            elif op == 0xC6:  # ADD A,n
                self.ADD(self.read_PC())  #
            elif op == 0xCE:  # ADC A,n   # how to tie these in with 86/8E? @@@
                self.ADC(self.read_PC())  #
            elif op == 0xD6:  # SUB n
                self.SUB(self.read_PC())
            elif op == 0xDE:  # SBC n
                self.SBC(self.read_PC())
            elif op == 0xD9:
                # EXX
                BC_tmp = self.get_reg_pair_BC()
                DE_tmp = self.get_reg_pair_DE()
                HL_tmp = self.get_reg_pair_HL()
                self.set_reg_pair_BC(self.get_reg_pair_BC_shadow())
                self.set_reg_pair_DE(self.get_reg_pair_DE_shadow())
                self.set_reg_pair_HL(self.get_reg_pair_HL_shadow())
                self.set_reg_pair_BC_shadow(BC_tmp)
                self.set_reg_pair_DE_shadow(DE_tmp)
                self.set_reg_pair_HL_shadow(HL_tmp)
            elif op == 0xE3:
                if prefix == 0xDD:
                    getter = self.get_reg_IX
                    setter = self.set_reg_IX
                elif prefix == 0xFD:
                    getter = self.get_reg_IY
                    setter = self.set_reg_IY
                else:
                    getter = self.get_reg_pair_HL
                    setter = self.set_reg_pair_HL

                tmp = self.read_mem16(self.get_reg_SP())
                self.write_mem16(self.get_reg_SP(), getter())
                setter(tmp)
            elif op == 0xE6:  # AND n
                self.AND(self.read_PC())
            elif op == 0xEB:
                # EX DE,HL
                tmp = self.get_reg_pair_HL()
                self.set_reg_pair_HL(self.get_reg_pair_DE())
                self.set_reg_pair_DE(tmp)
            elif op == 0xEE:  # XOR n
                self.XOR(self.read_PC())
            elif op == 0xF6:  # OR n
                self.OR(self.read_PC())
            elif op == 0xF9:
                if prefix == 0xDD:
                    getter = self.get_reg_IX
                elif prefix == 0xFD:
                    getter = self.get_reg_IY
                else:
                    getter = self.get_reg_pair_HL

                self.set_reg_SP(getter())

            elif op == 0xFE:  # CP n
                self.CP(self.read_PC())
            else:
                raise Exception("unknown operand")
        else:
            raise Exception("unknown operand")
