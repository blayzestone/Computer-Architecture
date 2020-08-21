"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.sp = 0xF4
        self.fl = 0b00000000  # 00000LGE
        self.pc = 0
        self.hlt = 1
        self.ldi = 130
        self.prn = 71
        self.mult2print = 160
        self.mul = 162
        self.push = 69
        self.pop = 70
        self.call = 80
        self.jmp = 84
        self.ret = 17
        self.cmp = 167
        self.jeq = 85
        self.jne = 86

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                line = line.strip()
                temp = line.split()

                if len(temp) == 0:
                    continue

                if temp[0][0] == "#":
                    continue

                instruction = int(temp[0], 2)

                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        # elif op == "SUB": etc
        elif op == "CMP":
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = self.fl | 0b00000001
            else:
                self.fl = self.fl & 0b11111110

            if self.registers[reg_a] > self.registers[reg_b]:
                self.fl = self.fl | 0b00000010
            else:
                self.fl = self.fl & 0b11111101

            if self.registers[reg_a] < self.registers[reg_b]:
                self.fl = self.fl | 0b00000100
            else:
                self.fl = self.fl & 0b11111011

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.hlt:
                running = False

            elif ir == self.jmp:
                self.pc = self.registers[operand_a]

            elif ir == self.call:
                self.sp -= 1
                self.ram_write(self.sp, self.pc + 2)

                self.pc = self.registers[operand_a]

            elif ir == self.ret:
                self.pc = self.ram_read(self.sp)
                self.sp += 1

            elif ir == self.ldi:
                self.registers[operand_a] = operand_b
                self.pc += 3

            elif ir == self.mul:
                product = self.registers[operand_a] * self.registers[operand_b]
                self.registers[operand_a] = product

                self.pc += 3

            elif ir == self.mult2print:
                product = self.registers[operand_a] * 2
                self.registers[operand_a] = product

                self.pc += 3

            elif ir == self.prn:
                print(self.registers[operand_a])
                self.pc += 2

            elif ir == self.push:
                self.sp -= 1

                self.ram_write(self.sp, self.registers[operand_a])

                self.pc += 2

            elif ir == self.pop:
                self.registers[operand_a] = self.ram_read(self.sp)
                self.sp += 1
                self.pc += 2

            elif ir == self.cmp:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif ir == self.jeq:
                if self.fl & 0b00000001:
                    self.pc = self.registers[operand_a]
                else:
                    self.pc += 2

            elif ir == self.jne:
                e_flag = self.fl & 0b00000001
                if not e_flag:
                    self.pc = self.registers[operand_a]
                else:
                    self.pc += 2

