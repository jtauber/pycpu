# 0000
#   0000           @NOP No Operation
# 0001
#   CCCC AAAA AAAA @JCN Jump Condition
# 0010
#   RRR0 DDDD DDDD @FIM Fetch Immediate
#   RRR1           @SRC Send Register Control
# 0011
#   RRR0           @FIN Fetch Indirect
#   RRR1           @JIN Jump Indirect
# 0100
#   AAAA AAAA AAAA @JUN Jump Unconditional
# 0101
#   AAAA AAAA AAAA @JMS Jump to Subroutine
# 0110
#   RRRR           @INC Increment
# 0111
#   RRRR AAAA AAAA @ISZ Increment and Skip
# 1000
#   RRRR            ADD Add
# 1001
#   RRRR            SUB Subtract
# 1010
#   RRRR           @LD  Load
# 1011
#   RRRR           @XCH Exchange
# 1100
#   DDDD           @BBL Branch Back and Load
# 1101
#   DDDD            LDM Load Immediate
# 1110
#   0000           @WRM Write Main Memory
#   0001           @WMP Write RAM Port
#   0010           @WRR Write ROM Port
#   0100           @WR0 Write Status Char 0
#   0101           @WR1 Write Status Char 1
#   0110           @WR2 Write Status Char 2
#   0111           @WR3 Write Status Char 3
#   1000            SBM Subtract Main Memory
#   1001            RDM Read Main Memory
#   1010           @RDR Read ROM Port
#   1011            ADM Add Main Memory
#   1100            RD0 Read Status Char 0
#   1101            RD1 Read Status Char 1
#   1110            RD2 Read Status Char 2
#   1111            RD3 Read Status Char 3
# 1111
#   0000           @CLB Clear Both
#   0001           @CLC Clear Carry
#   0010           @IAC Increment Accumulator
#   0011            CMC Complement Carry
#   0100            CMA Complement
#   0101           @RAL Rotate Left
#   0110            RAR Rotate Right
#   0111            TCC Transfer Carry and Clear
#   1000            DAC Decrement Accumulator
#   1001            TCS Transfer Carry Subtract
#   1010           @STC Set Carry
#   1011            DAA Decimal Adjust Accumulator
#   1100            KBP Keyboard Process
#   1101           @DCL Designate Command Line

ROM = [None] * 256

ROM[0x000:0x03D] = [
    0xE2,           # 0   WRR
    0xCF,           # 1   BBL, 15
    0x2A, 0x41,     # 2   FIM, 5, 4, 1
    0x50, 0xDE,     # 4   JMS (LD MK)
    0x50, 0xE5,     # 6   JMS (CK IDX)
    0x30,           # 8   FIN 0
    0xFE,           # 9   254
    0x50, 0xEE,     # 10  JMS (CK FIN)
    0x50, 0xE5,     # 12  JMS (CK IDX)
    0x50, 0xEE,     # 14  JMS (CK FIN)
    0x50, 0xE5,     # 16  JMS (CK IDX)
    0x2A, 0x42,     # 18  FIM 5, 4, 2
    0x5F, 0xFF,     # 20  JMS 15, 255
    0x57, 0x1A,     # 22  JMS 7, 26
    0x48, 0x24,     # 24  JUN 8, 36
    0x5F, 0xFF,     # 26  JMS 15, 255
    0x53, 0x20,     # 28  JMS 3, 32
    0x4C, 0x18,     # 30  JUN 12, 24
    0x5F, 0xFF,     # 32  JMS 15, 255
    0x4F, 0xFF,     # 34  JUN 15, 255
    0x22, 0xCB,     # 36  FIM 1, 12, 11
    0xF0,           # 38  CLB
    0x2B,           # 39  SRC 5
    0xE1,           # 40  WMP
    0x21,           # 41  SRC 0
    0xE0,           # 42  WRM
    0xF2,           # 43  IAC
    0x71, 0x29,     # 44  ISZ 1, 41
    0xE4,           # 46  WR0
    0xF2,           # 47  IAC
    0xE5,           # 48  WR1
    0xF2,           # 49  IAC
    0xE6,           # 50  WR2
    0xF2,           # 51  IAC
    0xE7,           # 52  WR3
    0x60,           # 53  INC 0
    0x72, 0x29,     # 54  ISZ 2, 41
    0xFA,           # 56  STC
    0x50, 0xF7,     # 57  JMS (CK CDL)
    0x73, 0x39,     # 59  ISZ 3, 57
    0x25,           # 61  SRC 2
    0xFA,           # 62  STC
    0xF5,           # 63  RAL
    0xE1,           # 64  WMP
    0x1A, 0x47,     # 65  JCN C=0, 71
    0x1C, 0x4F,     # 67  JCN A!=0, 79
    0x19, 0x50,     # 69  JCN T=1, 80
    0x12, 0x50,     # 71  JCN C=1, 80
    0x14, 0x52,     # 73  JCN A=0, 82
    0x11, 0x43,     # 75  JCN T=0, 67
    0x40, 0x45,     # 77  JUN 0, 69
    0xF0,           # 79  CLB
    0x40, 0x3F,     # 80  JUN 0, 63
]

ROM[0x0DE:] = [
    # LD MK
    0x2B,           # 222 SRC 5
    0xAB,           # 223 LD 11
    0xF1,           # 224 CLC
    0xE1,           # 225 WMP
    0xF5,           # 226 RAL
    0xBB,           # 227 XCH 11
    0xC0,           # 228 BBL, 0
    # CK IDX
    0x21,           # 229 SRC 0
    0x23,           # 230 SRC 1
    0x25,           # 231 SRC 2
    0x27,           # 232 SRC 3
    0x29,           # 233 SRC 4
    0x2B,           # 234 SRC 5
    0x2D,           # 235 SRC 6
    0x2F,           # 236 SRC 7
    0xC0,           # 237 BBL, 0
    # CK FIN
    0x32,           # 238 FIN 1
    0x34,           # 239 FIN 2
    0x36,           # 240 FIN 3
    0x38,           # 241 FIN 4
    0x3A,           # 242 FIN 5
    0x3C,           # 243 FIN 6
    0x3E,           # 244 FIN 7
    0x30,           # 245 FIN 0
    0xC0,           # 246 BBL, 0
    # CK CDL
    0xA4,           # 247 LD 4
    0xF5,           # 248 RAL
    0xFD,           # 249 DCL
    0xB4,           # 250 XCH 4
    0xEA,           # 251 RDR
    0xC0,           # 252 BBL, 0

    0x00,           # 253
    0xFF,           # 254
    0x00,           # 255
]


class I4004:
    def __init__(self):
        self.accumulator = 0x0
        self.registers = [0x0] * 16
        self.pc_stack = [0x000]
        self.rom_port = 0x0
        self.ram_port = [0x0] * 4
        self.ram_address = 0x00
        self.carry = 0
        self.rom = ROM
        self.ram = [0x0] * 1024
        self.ram_status = [0x0] * 64
        self.ram_bank = 0
        self.test = 0

    def next(self):
        return self.rom[self.pc_stack[0]]

    def increment_pc(self):
        self.pc_stack[0] += 1
        self.pc_stack[0] &= 0xFF  # @@@ just for exerciser

    def run(self):
        while True:
            print self.pc_stack
            op = self.next()
            if op is None:
                print "registers =", self.registers
                print "accumulator =", self.accumulator
                print "unknown op", op
                break
            if op >> 4 == 0x0:
                if op % 0x10 == 0:
                    self.NOP()
                else:
                    self.unimplemented_op()
            elif op >> 4 == 0x1:
                self.JCN(op % 0x10)
            elif op >> 4 == 0x2:
                if op % 2 == 0:
                    self.FIM(op % 0x10)
                else:
                    self.SRC((op % 0x10) - 1)
            elif op >> 4 == 0x3:
                if op % 2 == 0:
                    self.FIN(op % 0x10)
                else:
                    self.JIN((op % 0x10) - 1)
            elif op >> 4 == 0x4:
                self.JUN(op % 0x10)
            elif op >> 4 == 0x5:
                self.JMS(op % 0x10)
            elif op >> 4 == 0x6:
                self.INC(op % 0x10)
            elif op >> 4 == 0x7:
                self.ISZ(op % 0x10)
            elif op >> 4 == 0xA:
                self.LD(op % 0x10)
            elif op >> 4 == 0xB:
                self.XCH(op % 0x10)
            elif op >> 4 == 0xC:
                self.BBL(op % 0x10)
            elif op == 0xE0:
                self.WRM()
            elif op == 0xE1:
                self.WMP()
            elif op == 0xE2:
                self.WRR()
            elif op == 0xE4:  # |
                self.WRx(0)   # |
            elif op == 0xE5:  # |
                self.WRx(1)   # combine
            elif op == 0xE6:  # |
                self.WRx(2)   # |
            elif op == 0xE7:  # |
                self.WRx(3)   # |
            elif op == 0xEA:
                self.RDR()
            elif op == 0xF0:
                self.CLB()
            elif op == 0xF1:
                self.CLC()
            elif op == 0xF2:
                self.IAC()
            elif op == 0xF5:
                self.RAL()
            elif op == 0xFA:
                self.STC()
            elif op == 0xFD:
                self.DCL()
            elif op == 0xFE:
                self.unimplemented_op()
            else:
                print "registers =", self.registers
                print "accumulator =", self.accumulator
                print "unknown op %02X" % op
                break

    def unimplemented_op(self):
        self.increment_pc()

    def BBL(self, data):
        self.increment_pc()
        print "BBL", data
        if len(self.pc_stack) > 1:
            self.pc_stack = self.pc_stack[1:]
            self.accumulator = data

    def CLB(self):
        self.increment_pc()
        print "CLB"
        self.carry = 0
        self.accumulator = 0

    def CLC(self):
        self.increment_pc()
        print "CLC"
        self.carry = 0

    def DCL(self):
        self.increment_pc()
        self.ram_bank = {
            0: 0, 1: 1, 2: 2, 4: 3,
            3: 4, 5: 5, 6: 6, 7: 7,
        }[self.accumulator & 0x7]

    def FIM(self, pair):
        self.increment_pc()
        self.registers[pair: pair + 2] = divmod(self.next(), 0x10)
        print "FIM", pair >> 1, self.registers[pair: pair + 2]
        self.increment_pc()

    def FIN(self, pair):
        self.increment_pc()
        address = (self.pc_stack[0] & 0xF00) + (self.registers[0] << 4) + self.registers[1]
        data = self.rom[address]
        self.registers[pair: pair + 2] = divmod(data, 0x10)
        print "FIN", pair >> 1, self.registers[pair: pair + 2]

    def IAC(self):
        self.increment_pc()
        self.carry, self.accumulator = divmod(self.accumulator + 1, 0x10)
        print "IAC", self.accumulator

    def INC(self, register):
        self.increment_pc()
        self.registers[register] = (self.registers[register] + 1) & 0xF
        print "INC", register, self.registers[register]

    def ISZ(self, register):
        self.increment_pc()
        address = self.next()
        self.increment_pc()
        self.registers[register] = (self.registers[register] + 1) & 0xF
        print "ISZ", register, self.registers[register], address
        if self.registers[register] != 0:
            self.pc_stack[0] = address

    def JCN(self, condition):
        self.increment_pc()
        address = self.next()
        self.increment_pc()

        c1 = ((condition & 0x8) == 0x8)
        c2 = ((condition & 0x4) == 0x3)
        c3 = ((condition & 0x2) == 0x2)
        c4 = ((condition & 0x1) == 0x1)

        c = (c2 and self.accumulator == 0) or (c3 and self.carry == 1) or (c4 and self.test == 1)

        if c ^ c1:
            self.pc_stack[0] = address

        print "JCN", condition, c, c1, c2, c3, c4

    # def JIN(self, pair):
    #     self.increment_pc()
    #     address = (self.pc_stack[0] & 0xF00) + (self.registers[pair] << 4) + self.registers[pair + 1]
    #     self.pc_stack[0] = address
    #     print "JIN", pair >> 1, address

    def JMS(self, a3):
        self.increment_pc()
        address = (a3 << 8) + self.next()
        address &= 0xFF  # @@@ just for exerciser
        print "JMS", address
        self.increment_pc()
        self.pc_stack.insert(0, address)

    def JUN(self, a3):
        self.increment_pc()
        address = (a3 << 8) + self.next()
        address &= 0xFF  # @@@ just for exerciser
        print "JUN", address
        self.pc_stack[0] = address

    def LD(self, register):
        self.increment_pc()
        self.accumulator = self.registers[register]
        print "LD", self.accumulator

    def NOP(self):
        self.increment_pc()

    def RAL(self):
        self.increment_pc()
        old_acc = self.accumulator
        self.carry, self.accumulator = divmod((self.accumulator << 1) + self.carry, 0x10)
        print "RAL", old_acc, self.accumulator, self.carry

    def RDR(self):
        self.increment_pc()
        # @@@ no selection of ROM chip considered, nor I/O distinction
        print "RDR", self.rom_port
        self.accumulator = self.rom_port

    def SRC(self, pair):
        self.increment_pc()
        self.ram_address = (self.registers[pair] << 4) + self.registers[pair + 1]
        print "SRC", pair >> 1, self.ram_address

    def STC(self):
        self.increment_pc()
        print "STC"
        self.carry = 1

    def WMP(self):
        self.increment_pc()
        print "WMP", self.ram_address >> 6, self.accumulator
        self.ram_port[self.ram_address >> 6] = self.accumulator

    def WRM(self):
        self.increment_pc()
        print "WRM", self.ram_address, self.accumulator
        self.ram[self.ram_address] = self.accumulator

    def WRR(self):
        self.increment_pc()
        print "WRR", self.accumulator
        # @@@ no selection of ROM chip considered, nor I/O distinction
        self.rom_port = self.accumulator

    def WRx(self, status):
        self.increment_pc()
        print "WR", self.ram_address >> 4, status
        self.ram_status[((self.ram_address >> 4) << 2) + status] = self.accumulator

    def XCH(self, register):
        self.increment_pc()
        acc_buffer = self.accumulator
        self.accumulator = self.registers[register]
        self.registers[register] = acc_buffer
        print "XCH", register, self.accumulator, acc_buffer


i4004 = I4004()
i4004.run()
