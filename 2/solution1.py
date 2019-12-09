def process_add(pos_1, pos_2, res_pos, program):
  val = program[pos_1] + program[pos_2]
  program[res_pos] = val

def process_multiply(pos_1, pos_2, res_pos, program):
  val = program[pos_1] * program[pos_2]
  program[res_pos] = val

with open('./input.txt') as fp:

  for line in fp:
    codes = [int(c) for c in line.split(',')]
    i = 0
    while codes[i] != 99:
      if codes[i] == 1:
        process_add(codes[i+1], codes[i+2], codes[i+3], codes)
      elif codes[i] == 2:
        process_multiply(codes[i+1], codes[i+2], codes[i+3], codes)
      else:
        print("Unknown opcode: %i".format(codes[i]))
      i += 4

    print(codes[0])
