#!/usr/bin/env python

from z80 import Z80, from_twos_comp, to_twos_comp


## two-complment code

assert from_twos_comp(0) == 0
assert from_twos_comp(1) == 1
assert from_twos_comp(127) == 127
assert from_twos_comp(128) == -128
assert from_twos_comp(254) == -2
assert from_twos_comp(255) == -1

assert to_twos_comp(0) == 0
assert to_twos_comp(1) == 1
assert to_twos_comp(127) == 127
assert to_twos_comp(-128) == 128
assert to_twos_comp(-2) == 254
assert to_twos_comp(-1) == 255


z80 = Z80()


## 8-Bit Load Group

# test p101
z80.set_reg_H(0x8A)
z80.set_reg_E(0x10)
z80.memory[0:1] = [
    # LD H,E
    0b01100011,
]
z80.run()
assert z80.get_reg_H() == 0x10
assert z80.get_reg_E() == 0x10

# test p102
z80.memory[0:2] = [
    # LD E,n
    0b00011110,
    0xA5,
]
z80.run()
assert z80.get_reg_E() == 0xA5

# test p103
z80.memory[0:1] = [
    # LD C,(HL)
    0b01001110,
]
z80.memory[0x75A1] = 0x58
z80.set_reg_pair_HL(0x75A1)
z80.run()
assert z80.get_reg_C() == 0x58

# test p104
z80.memory[0:3] = [
    # LD B,(IX+19H)
    0b11011101,
    0b01000110,
    0b00011001,
]
z80.memory[0x25C8] = 0x39
z80.set_reg_IX(0x25AF)
z80.run()
assert z80.get_reg_B() == 0x39

# test p105
z80.memory[0:3] = [
    # LD B,(IY+19H)
    0b11111101,
    0b01000110,
    0b00011001,
]
z80.memory[0x25C8] = 0x39
z80.set_reg_IY(0x25AF)
z80.run()
assert z80.get_reg_B() == 0x39

# test p106
z80.set_reg_pair_HL(0x2146)
z80.set_reg_B(0x29)
z80.memory[0:1] = [
    # LD (HL),B
    0b01110000
]
z80.run()
assert z80.memory[0x2146] == 0x29

# test p107
z80.set_reg_C(0x1C)
z80.set_reg_IX(0x3100)
z80.memory[0:3] = [
    # LD (IX+6H),C
    0b11011101,
    0b01110001,
    0b00000110,
]
z80.run()
assert z80.memory[0x3106] == 0x1C

# test p108
z80.set_reg_C(0x48)
z80.set_reg_IY(0x2A11)
z80.memory[0:3] = [
    # LD (HL),28H # @@@
    0b11111101,
    0b01110001,
    0b00000100,
]
z80.run()
assert z80.memory[0x2A15] == 0x48

# test p109
z80.set_reg_pair_HL(0x4444)
z80.memory[0:2] = [
    # LD (HL),28H # @@@
    0b00110110, # 0x36
    0b00101000, # 0x28
]
z80.run()
assert z80.memory[0x4444] == 0x28

# test p110
z80.set_reg_IX(0x219A)
z80.memory[0:4] = [
    # LD (HL),28H # @@@
    0b11011101,
    0b00110110,
    0b00000101,
    0b01011010,
]
z80.run()
assert z80.memory[0x219F] == 0x5A

# test p111
z80.set_reg_IY(0x940)
z80.memory[0:4] = [
    0b11111101,
    0b00110110, # LD (IY+10H),97AH
    0b00010000,
    0b10010111,
]
z80.run()
assert z80.memory[0x950] == 0x97

# test p112
z80.set_reg_pair_BC(0x4747)
z80.memory[0x4747] = 0x12
z80.memory[0:1] = [
    0b00001010,
]
z80.run()
assert z80.get_reg_A() == 0x12

# test p113
z80.set_reg_pair_DE(0x30A2)
z80.memory[0x30A2] = 0x22
z80.memory[0:1] = [
    0b00011010,
]
z80.run()
assert z80.get_reg_A() == 0x22

# test p114
z80.memory[0x8832] = 0x04
z80.memory[0:3] = [
    0b00111010,
    0x32,
    0x88,
]
z80.run()
assert z80.get_reg_A() == 0x04

# test p115
z80.set_reg_pair_BC(0x1212)
z80.set_reg_A(0x7A)
z80.memory[0:1] = [
    0b00000010,
]
z80.run()
assert z80.memory[0x1212] == 0x7A

# test p116
z80.set_reg_pair_DE(0x1128)
z80.set_reg_A(0xA0)
z80.memory[0:1] = [
    0b00010010,
]
z80.run()
assert z80.memory[0x1128] == 0xA0

# test p117
z80.set_reg_A(0xD7)
z80.memory[0:3] = [
    0b00110010,
    0x41,
    0x31,
]
z80.run()
assert z80.memory[0x3141] == 0xD7

# test p118
# @@@

# test p119
# @@@

# test p120
# @@@

# test p121
# @@@


## 16-Bit Load Group

# test p122
z80.memory[0:3] = [
    # LD HL,5000H
    0b00100001, # 0x21
    0x00,
    0x50,
]
z80.run()
assert z80.get_reg_pair_HL() == 0x5000

# test p123
z80.memory[0:4] = [
    0b11011101,
    0b00100001,
    0xA2,
    0x45,
]
z80.run()
assert z80.get_reg_IX() == 0x45A2

# test p124
z80.memory[0:4] = [
    0b11111101,
    0b00100001,
    0x33,
    0x77,
]
z80.run()
assert z80.get_reg_IY() == 0x7733

# test p125
z80.memory[0x4545] = 0x37
z80.memory[0x4546] = 0xA1
z80.memory[0:3] = [
    # LD HL,(4545H)
    0b00101010, # 0x2A
    0x45,
    0x45,
]
z80.run()
assert z80.get_reg_pair_HL() == 0xA137

# test p126
z80.memory[0x2130] = 0x65
z80.memory[0x2131] = 0x78
z80.memory[0:4] = [
    0b11101101,
    0b01001011,
    0x30,
    0x21,
]
z80.run()
assert z80.get_reg_pair_BC() == 0x7865

# test p127
z80.memory[0x6666] = 0x92
z80.memory[0x6667] = 0xDA
z80.memory[0:4] = [
    0b11011101,
    0b00101010,
    0x66,
    0x66
]
z80.run()
assert z80.get_reg_IX() == 0xDA92

# test p128
z80.memory[0x6666] = 0x92
z80.memory[0x6667] = 0xDA
z80.memory[0:4] = [
    0b11111101,
    0b00101010,
    0x66,
    0x66
]
z80.run()
assert z80.get_reg_IY() == 0xDA92

# test p129
z80.set_reg_pair_HL(0x483A)
z80.memory[0:3] = [
    0b00100010,
    0x29,
    0xB2,
]
z80.run()
assert z80.memory[0xB229] == 0x3A
assert z80.memory[0xB22A] == 0x48

# test p130
z80.set_reg_pair_BC(0x4644)
z80.memory[0:4] = [
    0b11101101,
    0b01000011,
    0x00,
    0x10,
]
z80.run()
assert z80.memory[0x1000] == 0x44
assert z80.memory[0x1001] == 0x46

# test p131
z80.set_reg_IX(0x5A30)
z80.memory[0:4] = [
    # LD (4392H),IX
    0b11011101, # 0xDD
    0b00100010, # 0x22
    0x92,
    0x43,
]
z80.run()
assert z80.memory[0x4392] == 0x30
assert z80.memory[0x4393] == 0x5A

# test p132
z80.set_reg_IY(0x4174)
z80.memory[0:4] = [
    # LD (8838H),IY
    0b11111101, # 0xFD
    0b00100010, # 0x22
    0x38,
    0x88,
]
z80.run()
assert z80.memory[0x8838] == 0x74
assert z80.memory[0x8839] == 0x41

# test p133
z80.set_reg_pair_HL(0x442E)
z80.memory[0:1] = [
    # LD SP,HL
    0xF9,
]
z80.run()
assert z80.get_reg_SP() == 0x442E

# test p134
z80.set_reg_IX(0x98DA)
z80.memory[0:2] = [
    # LD SP,IX
    0xDD,
    0xF9,
]
z80.run()
assert z80.get_reg_SP() == 0x98DA

# test p135
z80.set_reg_IY(0xA227)
z80.memory[0:2] = [
    # LD SP,IY
    0xFD,
    0xF9,
]
z80.run()
assert z80.get_reg_SP() == 0xA227

# test p136
z80.set_reg_pair_AF(0x2233)
z80.set_reg_SP(0x1007)
z80.memory[0:1] = [
    # PUSH AF
    0b11110101, # F5
]
z80.run()
assert z80.memory[0x1006] == 0x22
assert z80.memory[0x1005] == 0x33
assert z80.get_reg_SP() == 0x1005

# test p137
z80.set_reg_IX(0x2234)
z80.set_reg_SP(0x1007)
z80.memory[0:2] = [
    # PUSH IX
    0xDD,
    0xE5,
]
z80.run()
assert z80.memory[0x1006] == 0x22
assert z80.memory[0x1005] == 0x34

# test p138
z80.set_reg_IY(0x2235)
z80.set_reg_SP(0x1007)
z80.memory[0:2] = [
    # PUSH IY
    0xFD,
    0xE5,
]
z80.run()
assert z80.memory[0x1006] == 0x22
assert z80.memory[0x1005] == 0x35

# test p139
z80.set_reg_SP(0x1000)
z80.memory[0x1000] = 0x55
z80.memory[0x1001] = 0x33
z80.memory[0:1] = [
    # POP HL
    0b11100001,
]
z80.run()
assert z80.get_reg_pair_HL() == 0x3355
assert z80.get_reg_SP() == 0x1002

# test p140
z80.set_reg_SP(0x1000)
z80.memory[0x1000] = 0x55
z80.memory[0x1001] = 0x33
z80.memory[0:2] = [
    # POP IX
    0b11011101, # 0xDD
    0b11100001, # 0xE1
]
z80.run()
assert z80.get_reg_IX() == 0x3355
assert z80.get_reg_SP() == 0x1002

# test p141 (typo in doc)
z80.set_reg_SP(0x1000)
z80.memory[0x1000] = 0x55
z80.memory[0x1001] = 0x33
z80.memory[0:2] = [
    # POP IY
    0b11111101, # 0xFD
    0b11100001, # 0xE1
]
z80.run()
assert z80.get_reg_IY() == 0x3355
assert z80.get_reg_SP() == 0x1002

# test p142
z80.set_reg_pair_DE(0x2822)
z80.set_reg_pair_HL(0x499A)
z80.memory[0:1] = [
    # EX DE,HL
    0b11101011, # 0xEB
]
z80.run()
assert z80.get_reg_pair_DE() == 0x499A
assert z80.get_reg_pair_HL() == 0x2822

# test p143
z80.set_reg_pair_AF(0x9900)
assert z80.get_reg_pair_AF() == 0x9900
z80.memory[0:1] = [
    0b00001000, # 0x08
]
z80.run()
z80.set_reg_pair_AF(0x5944)
assert z80.get_reg_pair_AF() == 0x5944
z80.memory[0:1] = [
    0b00001000, # 0x08
]
z80.run()
assert z80.get_reg_pair_AF() == 0x9900
z80.memory[0:1] = [
    0b00001000, # 0x08
]
z80.run()
assert z80.get_reg_pair_AF() == 0x5944

# test p144
z80.set_reg_pair_BC(0x445A)
z80.set_reg_pair_DE(0x3DA2)
z80.set_reg_pair_HL(0x8859)
assert z80.get_reg_pair_BC() == 0x445A
assert z80.get_reg_pair_DE() == 0x3DA2
assert z80.get_reg_pair_HL() == 0x8859
z80.memory[0:1] = [
    0b11011001, # 0xD9
]
z80.run()
z80.set_reg_pair_BC(0x0988)
z80.set_reg_pair_DE(0x9300)
z80.set_reg_pair_HL(0x00E7)
assert z80.get_reg_pair_BC() == 0x0988
assert z80.get_reg_pair_DE() == 0x9300
assert z80.get_reg_pair_HL() == 0x00E7
z80.memory[0:1] = [
    0b11011001, # 0xD9
]
z80.run()
assert z80.get_reg_pair_BC() == 0x445A
assert z80.get_reg_pair_DE() == 0x3DA2
assert z80.get_reg_pair_HL() == 0x8859
z80.memory[0:1] = [
    0b11011001, # 0xD9
]
z80.run()
assert z80.get_reg_pair_BC() == 0x0988
assert z80.get_reg_pair_DE() == 0x9300
assert z80.get_reg_pair_HL() == 0x00E7

# test p145
z80.set_reg_pair_HL(0x7012)
z80.set_reg_SP(0x8856)
z80.memory[0x8856] = 0x11
z80.memory[0x8857] = 0x22
z80.memory[0:1] = [
    # EX (SP),HL
    0b11100011, # 0xE3
]
z80.run()
assert z80.get_reg_pair_HL() == 0x2211
assert z80.memory[0x8856] == 0x12
assert z80.memory[0x8857] == 0x70
assert z80.get_reg_SP() == 0x8856

# test p146
z80.set_reg_IX(0x3988)
z80.set_reg_SP(0x0100)
z80.memory[0x0100] = 0x90
z80.memory[0x0101] = 0x48
z80.memory[0:2] = [
    # EX (SP),IX
    0b11011101, # 0xDD
    0b11100011, # 0xE3
]
z80.run()
assert z80.get_reg_IX() == 0x4890
assert z80.memory[0x0100] == 0x88
assert z80.memory[0x0101] == 0x39
assert z80.get_reg_SP() == 0x0100

# test p147
z80.set_reg_IY(0x3988)
z80.set_reg_SP(0x0100)
z80.memory[0x0100] = 0x90
z80.memory[0x0101] = 0x48
z80.memory[0:2] = [
    # EX (SP),IY
    0b11111101, # 0xFD
    0b11100011, # 0xE3
]
z80.run()
assert z80.get_reg_IY() == 0x4890
assert z80.memory[0x0100] == 0x88
assert z80.memory[0x0101] == 0x39
assert z80.get_reg_SP() == 0x0100

# test p148
z80.set_reg_pair_HL(0x1111)
z80.memory[0x1111] = 0x88
z80.set_reg_pair_DE(0x2222)
z80.memory[0x2222] = 0x66
z80.set_reg_pair_BC(0x7)
z80.memory[0:2] = [
    # LDI
    0b11101101, # ED
    0b10100000, # A0
]
z80.run()
assert z80.get_reg_pair_HL() == 0x1112
assert z80.memory[0x1111] == 0x88
assert z80.get_reg_pair_DE() == 0x2223
assert z80.memory[0x2222] == 0x88
assert z80.get_reg_pair_BC() == 0x6

# test p149-150
z80.set_reg_pair_HL(0x1111)
z80.set_reg_pair_DE(0x2222)
z80.set_reg_pair_BC(0x0003)
z80.memory[0x1111:0x1114] = [0x88, 0x36, 0xA5]
z80.memory[0x2222:0x2225] = [0x66, 0x59, 0xC5]
z80.memory[0:2] = [
    # LDIR
    0b11101101, # ED
    0b10110000, # B0
]
z80.run()
assert z80.get_reg_pair_HL() == 0x1114
assert z80.get_reg_pair_DE() == 0x2225
assert z80.get_reg_pair_BC() == 0x0000
assert z80.memory[0x1111:0x1114] == [0x88, 0x36, 0xA5]
assert z80.memory[0x2222:0x2225] == [0x88, 0x36, 0xA5]

# test p151
z80.set_reg_pair_HL(0x1111)
z80.memory[0x1111] = 0x88
z80.set_reg_pair_DE(0x2222)
z80.memory[0x2222] = 0x66
z80.set_reg_pair_BC(0x7)
z80.memory[0:2] = [
    # LDD
    0b11101101, # ED
    0b10101000, # A8
]
z80.run()
assert z80.get_reg_pair_HL() == 0x1110
assert z80.memory[0x1111] == 0x88
assert z80.get_reg_pair_DE() == 0x2221
assert z80.memory[0x2222] == 0x88
assert z80.get_reg_pair_BC() == 0x6

# test p152-153
z80.set_reg_pair_HL(0x1114)
z80.set_reg_pair_DE(0x2225)
z80.set_reg_pair_BC(0x0003)
z80.memory[0x1112:0x1115] = [0x88, 0x36, 0xA5]
z80.memory[0x2223:0x2226] = [0x66, 0x59, 0xC5]
z80.memory[0:2] = [
    # LDDR
    0b11101101, # ED
    0b10111000, # B8
]
z80.run()
assert z80.get_reg_pair_HL() == 0x1111
assert z80.get_reg_pair_DE() == 0x2222
assert z80.get_reg_pair_BC() == 0x0000
assert z80.memory[0x1112:0x1115] == [0x88, 0x36, 0xA5]
assert z80.memory[0x2223:0x2226] == [0x88, 0x36, 0xA5]

# test p154
z80.set_reg_pair_HL(0x1111)
z80.memory[0x1111] = 0x3B
z80.set_reg_A(0x3B)
z80.set_reg_pair_BC(0x001)
z80.memory[0:2] = [
    # CPI
    0b11101101, # 0xED
    0b10100001, # 0xA1
]
z80.run()
assert z80.get_reg_pair_BC() == 0x0000
assert z80.get_reg_pair_HL() == 0x1112
assert z80.flag_Z == 1
assert z80.flag_PV == 0
assert z80.get_reg_A() == 0x3B
assert z80.memory[0x1111] == 0x3B

# test p155-156
z80.set_reg_pair_HL(0x1111)
z80.set_reg_A(0xF3)
z80.set_reg_pair_BC(0x7)
z80.memory[0x1111:0x1114] = [0x52, 0x00, 0xF3]
z80.memory[0:2] = [
    # CPIR
    0b11101101, # 0xED
    0b10110001, # 0xB1
]
z80.run()
assert z80.get_reg_pair_HL() == 0x1114
assert z80.get_reg_pair_BC() == 0x0004
assert z80.flag_PV == 1
assert z80.flag_Z == 1

# test p157
z80.set_reg_pair_HL(0x1111)
z80.memory[0x1111] = 0x3B
z80.set_reg_A(0x3B)
z80.set_reg_pair_BC(0x0001)
z80.memory[0:2] = [
    # CPD
    0b11101101, # 0xED
    0b10101001, # 0xA9
]
z80.run()
assert z80.get_reg_pair_BC() == 0x0000
assert z80.get_reg_pair_HL() == 0x1110
assert z80.flag_Z == 1
assert z80.flag_PV == 0
assert z80.get_reg_A() == 0x3B
assert z80.memory[0x1111] == 0x3B

# test p158-159
z80.set_reg_pair_HL(0x1118)
z80.set_reg_A(0xF3)
z80.set_reg_pair_BC(0x7)
z80.memory[0x1116:0x1119] = [0xF3, 0x00, 0x52]
z80.memory[0:2] = [
    # CPDR
    0b11101101, # 0xED
    0b10111001, # 0xB9
]
z80.run()
assert z80.get_reg_pair_HL() == 0x1115
assert z80.get_reg_pair_BC() == 0x0004
assert z80.flag_PV == 1
assert z80.flag_Z == 1


## 8-Bit Arithmetic Group

# test p160-161
z80.set_reg_A(0x44)
z80.set_reg_C(0x11)
z80.memory[0:1] = [
    # ADD A,C
    0b10000001,
]
z80.run()
assert z80.get_reg_A() == 0x55

# test p162
z80.set_reg_A(0x23)
z80.memory[0:2] = [
    # ADD A,33H
    0b11000110, # 0xC6
    0x33,
]
z80.run()
assert z80.get_reg_A() == 0x56

# test p163
z80.set_reg_A(0xA0)
z80.set_reg_pair_HL(0x2323)
z80.memory[0:1] = [
    # ADD A,(HL)
    0b10000110, # 0x86
]
z80.memory[0x2323] = 0x08
z80.run()
assert z80.get_reg_A() == 0xA8

# test p164
z80.set_reg_A(0x11)
z80.set_reg_IX(0x1000)
z80.memory[0x1005] = 0x22
z80.memory[0:3] = [
    # ADD A,(IX+5H)
    0b11011101, # 0xDD
    0b10000110, # 0x86
    0x05,
]
z80.run()
assert z80.get_reg_A() == 0x33

# test p165
z80.set_reg_A(0x11)
z80.set_reg_IY(0x2000)
z80.memory[0x2005] = 0x33
z80.memory[0:3] = [
    # ADD A,(IY+5H)
    0b11111101, # 0xFD
    0b10000110, # 0x86
    0x05,
]
z80.run()
assert z80.get_reg_A() == 0x44

# test p166-167
z80.set_reg_A(0x16)
z80.flag_C = 1
z80.set_reg_pair_HL(0x6666)
z80.memory[0x6666] = 0x10
z80.memory[0:1] = [
    # ADC A,(HL)
    0b10001110, # 0x8E
]
z80.run()
assert z80.get_reg_A() == 0x27

# own test
z80.set_reg_A(0x16)
z80.flag_C = 1
z80.memory[0:2] = [
    # ADC A,10H
    0b11001110, # 0xCE
    0x10,
]
z80.run()
assert z80.get_reg_A() == 0x27

# test p168-169
z80.set_reg_A(0x29)
z80.set_reg_D(0x11)
z80.memory[0:1] = [
    # SUB D
    0b10010010,
]
z80.run()
assert z80.get_reg_A() == 0x18

# test p170-171
z80.set_reg_A(0x16)
z80.flag_C = 1
z80.set_reg_pair_HL(0x3433)
z80.memory[0x3433] = 0x05
z80.memory[0:1] = [
    # SBC A,(HL)
    0b10011110, # 0x9E
]
z80.run()
assert z80.get_reg_A() == 0x10

# test p172-173
z80.set_reg_B(0x7B)
z80.set_reg_A(0xC3)
z80.memory[0:1] = [
    # AND B
    0b10100000,
]
z80.run()
assert z80.get_reg_A() == 0x43

# test p174-175
z80.set_reg_H(0x48)
z80.set_reg_A(0x12)
z80.memory[0:1] = [
    # OR H
    0b10110100,
]
z80.run()
assert z80.get_reg_A() == 0x5A

# test p176-177
z80.set_reg_A(0x96)
z80.memory[0:2] = [
    # XOR 5DH
    0b11101110, # 0xEE
    0x5D,
]
z80.run()
assert z80.get_reg_A() == 0xCB

# test p178-179
z80.set_reg_A(0x63)
z80.set_reg_pair_HL(0x6000)
z80.memory[0x6000] = 0x60
z80.memory[0:1] = [
    # CP (HL)
    0b10111110, # 0xBE
]
assert z80.flag_S == 0 # @@@
assert z80.flag_Z == 0 # @@@
assert z80.flag_H == 1 # @@@
assert z80.flag_PV == 0 # @@@
assert z80.flag_N == 1 # @@@
assert z80.flag_C == 1 # @@@

### OPCODE COVERAGE

# for i in range(0x100):
#     print hex(i),
#     z80 = Z80()
#     z80.memory[0] = i

#     try:
#         z80.run()
#         print "*** PASS ***"
#     except Exception, e:
#         print e
