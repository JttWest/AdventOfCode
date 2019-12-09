def process_add(pos_1, pos_2, res_pos, program):
  val = program[pos_1] + program[pos_2]
  program[res_pos] = val

def process_multiply(pos_1, pos_2, res_pos, program):
  val = program[pos_1] * program[pos_2]
  program[res_pos] = val

def is_result(noun, verb, target, program):
  program[1], program[2] = noun, verb

  i = 0
  while program[i] != 99:
    if program[i] == 1:
      process_add(program[i+1], program[i+2], program[i+3], program)
    elif codes[i] == 2:
      process_multiply(program[i+1], program[i+2], program[i+3], program)
    else:
      print("Unknown opcode: %i".format(program[i]))

    if program[0] == target:
      return True

    i += 4

  return False

with open('./input.txt') as fp:
  codes = [int(c) for c in fp.read().split(',')]
  print(codes)

  target = 19690720
  for noun in range(0, 100):
    for verb in range(0, 100):
      if is_result(noun, verb, target, codes[:]):
        print(100*noun+verb)
