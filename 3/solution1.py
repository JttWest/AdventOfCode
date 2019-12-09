def record_point(grid, pos, wire_index):
  x, y = pos
  if x not in grid:
    grid[x] = {}

  if y not in grid[x]:
    grid[x][y] = set()

  grid[x][y].add(wire_index)

def add_wire_seg(pos, grid, seg, wire_index):
  direction = seg[0]
  length = int(seg[1:])

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
    record_point(grid, pos, wire_index)

  return end_pos

def add_wire(grid, wire, wire_index):
  pos = (0,0)
  for seg in wire:
    new_pos = add_wire_seg(pos, grid, seg, wire_index)
    pos = new_pos

def closest(grid):
  dist = 999999999999999999999999999
  for x, y_col in grid.items():
    for y, s in y_col.items():
      if len(s) > 1 and abs(x) + abs(y) < dist:
        dist = abs(x) + abs(y)

  return dist

with open('./input.txt') as fp:
  grid = {}
  for i, line in enumerate(fp):
    wire = [c.strip() for c in line.split(',')]
    add_wire(grid, wire, i)

  dist = closest(grid)
  print(dist)
