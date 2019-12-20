from enum import Enum


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
  ParameterMode = Enum('ParameterMode', 'POSITION IMMEDIATE RELATIVE')

  def __init__(self, code):
    self.opcode = code

  def get_opcode(self):
    return self.opcode % 100

  def get_parameter_mode(self, index):
    positions = self.opcode // 100
    for _ in range(0, index):
      positions //= 10
    parameter_val = positions % 10
    if parameter_val == 0:
      return self.ParameterMode.POSITION
    elif parameter_val == 1:
      return self.ParameterMode.IMMEDIATE
    else:
      return self.ParameterMode.RELATIVE


class IntcodeComputer:
  def __init__(self, codes):
    self.codes = codes
    self.instr_ptr = 0
    self.terminated = False
    self.relative_base = 0

  def get_program_value(self, index):
    return self.codes.get(index, 0)

  def get_program_value_from_instr_ptr(self, index):
    val_index = self.instr_ptr + index
    return self.codes.get(val_index, 0)

  def get_parameter_value(self, operation, parameter_index, instr_ptr_value):
    parameter_mode = operation.get_parameter_mode(parameter_index)
    program_value = self.get_program_value(instr_ptr_value)
    if parameter_mode == Operation.ParameterMode.POSITION:
      return self.get_program_value(program_value)
    elif parameter_mode == Operation.ParameterMode.IMMEDIATE:
      return program_value
    else:
      return self.get_program_value(self.relative_base + program_value)

  def get_result_pos(self, operation, parameter_index, memory_position):
    parameter_mode = operation.get_parameter_mode(parameter_index)
    program_value = self.get_program_value(memory_position)
    if parameter_mode == Operation.ParameterMode.POSITION:
      return program_value
    else:  # relative mode
      return self.relative_base + program_value

  def excute(self, input_v=None):
    codes = self.codes
    while not self.terminated:
      op = Operation(self.get_program_value_from_instr_ptr(0))
      opcode = op.get_opcode()

      if opcode == 1:
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        v2 = self.get_parameter_value(op, 1, self.instr_ptr+2)
        res_pos = self.get_result_pos(op, 2, self.instr_ptr+3)
        process_add(v1, v2, res_pos, codes)
        self.instr_ptr += 4
      elif opcode == 2:
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        v2 = self.get_parameter_value(op, 1, self.instr_ptr+2)
        res_pos = self.get_result_pos(op, 2, self.instr_ptr+3)
        process_multiply(v1, v2, res_pos, codes)
        self.instr_ptr += 4
      elif opcode == 3:
        res_pos = self.get_result_pos(op, 0, self.instr_ptr+1)
        v = input_v
        process_input(v, res_pos, codes)
        self.instr_ptr += 2
      elif opcode == 4:
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        self.instr_ptr += 2
        return process_output(v1)
      elif opcode == 5:  # JUMP_IF_TRUE
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        v2 = self.get_parameter_value(op, 1, self.instr_ptr+2)
        if v1 != 0:
          self.instr_ptr = v2
        else:
          self.instr_ptr += 3
      elif opcode == 6:  # JUMP_IF_FALSE
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        v2 = self.get_parameter_value(op, 1, self.instr_ptr+2)
        if v1 == 0:
          self.instr_ptr = v2
        else:
          self.instr_ptr += 3
      elif opcode == 7:
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        v2 = self.get_parameter_value(op, 1, self.instr_ptr+2)
        res_pos = self.get_result_pos(op, 2, self.instr_ptr+3)
        process_less_than(v1, v2, res_pos, codes)
        self.instr_ptr += 4
      elif opcode == 8:
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        v2 = self.get_parameter_value(op, 1, self.instr_ptr+2)
        res_pos = self.get_result_pos(op, 2, self.instr_ptr+3)
        process_equal(v1, v2, res_pos, codes)
        self.instr_ptr += 4
      elif opcode == 9:
        v1 = self.get_parameter_value(op, 0, self.instr_ptr+1)
        self.relative_base += v1
        self.instr_ptr += 2
      elif opcode == 99:
        self.terminated = True
        print('Program terminated!')
        return None
      else:
        print(f"Unknown opcode: {opcode}")
        return None


# Facing[Turn_direction] : (Coord_diff, New_direction)
MOVEMENT = {
            'UP': {'TURN_LEFT': ((-1, 0), 'LEFT'), 'TURN_RIGHT': ((1, 0), 'RIGHT')},
            'DOWN': {'TURN_LEFT': ((1, 0), 'RIGHT'), 'TURN_RIGHT': ((-1, 0), 'LEFT')},
            'LEFT': {'TURN_LEFT': ((0, -1), 'DOWN'), 'TURN_RIGHT': ((0, 1), 'UP')},
            'RIGHT': {'TURN_LEFT': ((0, 1), 'UP'), 'TURN_RIGHT': ((0, -1), 'DOWN')},
        }


def coord(x, y):
  return f'{x},{y}'


with open('./input.txt') as fp:
  codes = {i: int(c) for i, c in enumerate(fp.readline().split(','))}
  program = IntcodeComputer(codes)

  paint_panels = set()
  panels_map = {}
  curr_face = 'UP'
  curr_coord = (0, 0)
  panels_map[0] = {0: 1}
  while not program.terminated:
    curr_x, curr_y = curr_coord
    panel_color = panels_map.get(curr_x, {}).get(curr_y, 0)
    paint_color = program.excute(panel_color)
    if paint_color is None:
      break
    direction = program.excute()
    direction_key = 'TURN_LEFT' if direction == 0 else 'TURN_RIGHT'

    paint_panels.add(coord(curr_x, curr_y))
    if curr_x not in panels_map:
      panels_map[curr_x] = {}
    panels_map[curr_x][curr_y] = paint_color

    movement_diff, new_face = MOVEMENT[curr_face][direction_key]
    new_coord = (curr_x + movement_diff[0], curr_y + movement_diff[1])
    curr_coord = new_coord
    curr_face = new_face

  min_x, max_x = min(panels_map.keys()), max(panels_map.keys())
  min_y, max_y = min(map(min, *panels_map.values())), max(map(max, *panels_map.values()))
  print(min_x, max_x, min_y, max_y)
  print(len(paint_panels))

  for y in range(max_y+10, min_y-10, -1):
    line = ''
    for x in range(min_x-10, max_x+10):
      panel_color = panels_map.get(x, {}).get(y, 0)
      if panel_color == 1:
        line += '*'
      elif panel_color == 0:
        line += ' '
      else:
        print(f'Invalid panel color {panel_color}')
    print(line)
