def process_add(val1, val2, res_pos, program):
  val = val1 + val2
  program[res_pos] = val

def process_multiply(val1, val2, res_pos, program):
  val = val1 * val2
  program[res_pos] = val

def process_input(res_pos, program):
  data = int(input("Input: "))
  program[res_pos] = data

def process_output(val):
  print(val)

class Operation:
  def __init__(self, code):
    self.opcode = code

  def get_opcode(self):
    return self.opcode % 100

  def is_immediate_parameter(self, index):
    positions = self.opcode // 100
    for i in range(0, index):
      positions //= 10
    return positions % 10 == 1

with open('./input.txt') as fp:
  for line in fp:
    codes = [int(c) for c in line.split(',')]
    i = 0
    while i < len(codes):
      op = Operation(codes[i])
      opcode = op.get_opcode()

      if opcode == 1:
        v1 = codes[i+1] if op.is_immediate_parameter(0) else codes[codes[i+1]]
        v2 = codes[i+2] if op.is_immediate_parameter(1) else codes[codes[i+2]]
        process_add(v1, v2, codes[i+3], codes)
        i += 4
      elif opcode == 2:
        v1 = codes[i+1] if op.is_immediate_parameter(0) else codes[codes[i+1]]
        v2 = codes[i+2] if op.is_immediate_parameter(1) else codes[codes[i+2]]
        process_multiply(v1, v2, codes[i+3], codes)
        i += 4
      elif opcode == 3:
        process_input(codes[i+1], codes)
        i += 2
      elif opcode == 4:
        v = codes[i+1] if op.is_immediate_parameter(0) else codes[codes[i+1]]
        process_output(v)
        i += 2
      elif opcode == 99:
        break
      else:
        print("Unknown opcode: %i".format(codes[i]))
