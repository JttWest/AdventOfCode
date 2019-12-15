def process_add(v1, v2, res_pos, program):
  val = v1 + v2
  program[res_pos] = val

def process_multiply(v1, v2, res_pos, program):
  val = v1 * v2
  program[res_pos] = val

def process_input(inp, res_pos, program):
  program[res_pos] = inp

def process_output(val):
  return val

def process_less_than(v1, v2, res_pos, program):
  if v1 < v2:
    program[res_pos] = 1
  else:
    program[res_pos] = 0

def process_equal(v1, v2, res_pos, program):
  if v1 == v2:
    program[res_pos] = 1
  else:
    program[res_pos] = 0

class Operation:
  def __init__(self, code):
    self.opcode = code

  def get_opcode(self):
    return self.opcode % 100

  def is_immediate_parameter(self, index):
    positions = self.opcode // 100
    for _ in range(0, index):
      positions //= 10
    return positions % 10 == 1

class Amplfier:
  def __init__(self, codes):
    self.codes = codes
    self.instr_ptr = 0
    self.has_inputted_phase_setting = False
    self.terminated = False
  
  def compute_amp_signal(self, phase_setting, input_signal):
    codes = self.codes
    while self.instr_ptr < len(codes) and not self.terminated:
      op = Operation(codes[self.instr_ptr])
      opcode = op.get_opcode()

      if opcode == 1:
        v1 = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        v2 = codes[self.instr_ptr+2] if op.is_immediate_parameter(1) else codes[codes[self.instr_ptr+2]]
        process_add(v1, v2, codes[self.instr_ptr+3], codes)
        self.instr_ptr += 4
      elif opcode == 2:
        v1 = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        v2 = codes[self.instr_ptr+2] if op.is_immediate_parameter(1) else codes[codes[self.instr_ptr+2]]
        process_multiply(v1, v2, codes[self.instr_ptr+3], codes)
        self.instr_ptr += 4
      elif opcode == 3:
        if self.has_inputted_phase_setting:
          v = input_signal
        else:
          v = phase_setting
          self.has_inputted_phase_setting = True
        process_input(v, codes[self.instr_ptr+1], codes)
        self.instr_ptr += 2
      elif opcode == 4:
        v = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        self.instr_ptr += 2
        return process_output(v)
      elif opcode == 5: # JUMP_IF_TRUE
        v1 = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        v2 = codes[self.instr_ptr+2] if op.is_immediate_parameter(1) else codes[codes[self.instr_ptr+2]]
        if v1 != 0:
          self.instr_ptr = v2
        else:
          self.instr_ptr += 3
      elif opcode == 6: # JUMP_IF_FALSE
        v1 = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        v2 = codes[self.instr_ptr+2] if op.is_immediate_parameter(1) else codes[codes[self.instr_ptr+2]]
        if v1 == 0:
          self.instr_ptr = v2
        else:
          self.instr_ptr += 3
      elif opcode == 7:
        v1 = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        v2 = codes[self.instr_ptr+2] if op.is_immediate_parameter(1) else codes[codes[self.instr_ptr+2]]
        process_less_than(v1, v2, codes[self.instr_ptr+3], codes)
        self.instr_ptr += 4
      elif opcode == 8:
        v1 = codes[self.instr_ptr+1] if op.is_immediate_parameter(0) else codes[codes[self.instr_ptr+1]]
        v2 = codes[self.instr_ptr+2] if op.is_immediate_parameter(1) else codes[codes[self.instr_ptr+2]]
        process_equal(v1, v2, codes[self.instr_ptr+3], codes)
        self.instr_ptr += 4
      elif opcode == 99:
        self.terminated = True
        return None
      else:
        print(f"Unknown opcode: {codes[self.instr_ptr]}")

def compute_thruster_signal(codes, phase_settings, num_amps):
  input_signal = 0
  amps = [Amplfier(codes[:]) for _ in range(0, num_amps)]
  curr_amp_i = 0
  
  while True:
    amp = amps[curr_amp_i]
    output_signal = amp.compute_amp_signal(phase_settings[curr_amp_i], input_signal)
    if output_signal is None:
      break
    else:
      input_signal = output_signal

    curr_amp_i = (curr_amp_i + 1) % num_amps

  return input_signal

def calc_max_signal(phase_settings, i, codes):
  res = 0
  if i >= len(phase_settings):
    res = compute_thruster_signal(codes[:], phase_settings[:], 5)
  else:
    for j in range(i, len(phase_settings)):
      phase_settings[i], phase_settings[j] = phase_settings[j], phase_settings[i]
      res = max(res, calc_max_signal(phase_settings, i+1, codes))
      phase_settings[i], phase_settings[j] = phase_settings[j], phase_settings[i]
  return res

with open('./input.txt') as fp:
  codes = [int(c) for c in fp.readline().split(',')]
  print(calc_max_signal([5,6,7,8,9], 0, codes))
