class Point:
  def __init__(self):
    self.wires = set()
    self.delay_step1 = 99999999999999
    self.delay_step2 = 99999999999999

  def add_wire(self, wire_index):
    self.wires.add(wire_index)

  def update_delay(self, steps):
    # set the higher of the 2 lengths
    if self.delay_step1 > self.delay_step2:
      self.delay_step1 = min(self.delay_step1, steps)
    else:
      self.delay_step2 = min(self.delay_step2, steps)

  def get_delay(self):
    return self.delay_step1 + self.delay_step2

  def has_intersect(self):
    return len(self.wires) > 1

def record_point(grid, pos, wire_index, steps):
  x, y = pos
  if x not in grid:
    grid[x] = {}

  if y not in grid[x]:
    grid[x][y] = Point()

  point = grid[x][y]
  point.add_wire(wire_index)
  point.update_delay(steps)

def add_wire_seg(pos, grid, seg, wire_index, steps):
  direction = seg[0]
  length = int(seg[1:])
  new_steps = steps

  delta = (0,0)
  if direction == "L":
    delta = (-1, 0)
  elif direction == "R":
    delta = (1, 0)
  elif direction == "D":
    delta = (0, -1)
  elif direction == "U":
    delta = (0, 1)

  x, y = pos
  dx, dy = delta
  end_pos = (x + dx * length, y + dy * length)

  while pos[0] != end_pos[0] or pos[1] != end_pos[1]:
    pos = (pos[0] + delta[0], pos[1] + delta[1])
    new_steps += 1
    record_point(grid, pos, wire_index, new_steps)

  return (end_pos, new_steps)

def add_wire(grid, wire, wire_index):
  pos = (0,0)
  steps = 0
  for seg in wire:
    new_pos, new_steps = add_wire_seg(pos, grid, seg, wire_index, steps)
    pos = new_pos
    steps = new_steps

def closest(grid):
  delay = 999999999999999999999999999
  for x, y_col in grid.items():
    for y, point in y_col.items():
      if point.has_intersect():
        delay = min(delay, point.get_delay())
  return delay

with open('./input.txt') as fp:
  grid = {}
  for i, line in enumerate(fp):
    wire = [c.strip() for c in line.split(',')]
    add_wire(grid, wire, i)

  delay = closest(grid)
  print(delay)