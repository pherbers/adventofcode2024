class ComputationException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class AOC3:
    def __init__(self):
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0
        self.ops = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        self.head = 0
        self.program = []
        self.output = []
    
    def load_program(self, program):
        self.program = program
        self.head = 0
    
    def execute(self):
        while self.head < len(self.program):
            op = self.program[self.head]
            val = self.program[self.head+1]
            self.ops[op](val)
            self.head += 2
            

    def reset(self):
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0
        self.head = 0
        self.output = []

    def print_output(self):
        print(",".join([str(i) for i in self.output]))

    def combo(self, val):
        if val == 0:
            return 0
        elif val == 1:
            return 1
        elif val == 2:
            return 2
        elif val == 3:
            return 3
        elif val == 4:
            return self.reg_a
        elif val == 5:
            return self.reg_b
        elif val == 6:
            return self.reg_c
        elif val == 7:
            raise ComputationException("Combo Value 7 not allowed")

    def adv(self, val):
        self.reg_a = int(self.reg_a / (2**self.combo(val)))

    def bxl(self, val):
        self.reg_b = val ^ self.reg_b

    def bst(self, val):
        self.reg_b = self.combo(val) % 8

    def jnz(self, val):
        if self.reg_a != 0:
            self.head = val - 2
    
    def bxc(self, val):
        self.reg_b = self.reg_b ^ self.reg_c
    
    def out(self, val):
        self.output.append(self.combo(val)%8)

    def bdv(self, val):
        self.reg_b = int(self.reg_a / (2**self.combo(val)))

    def cdv(self, val):
        self.reg_c = int(self.reg_a / (2**self.combo(val)))

def read_from_string(in_str) -> AOC3:
    aoc3 = AOC3()
    for line in in_str.splitlines():
        if line.startswith("Register A: "):
            aoc3.reg_a = int(line.split(":")[1])
        if line.startswith("Register B: "):
            aoc3.reg_b = int(line.split(":")[1])
        if line.startswith("Register C: "):
            aoc3.reg_c = int(line.split(":")[1])
        if line.startswith("Program"):
            ops = line.split(":")[1]
            ops = list([int(o) for o in ops.split(",")])
            aoc3.load_program(ops)
    return aoc3

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

computer = read_from_string(input_text)
computer.reg_a = 601100000
computer.execute()
computer.print_output()

a = 0
while computer.output != computer.program:
    computer.reset()
    computer.reg_a = a
    computer.execute()
    a += 1
    if a % 100000 == 0:
        print(f"Iteration {a:9}")

print(a, computer.program, computer.output)

