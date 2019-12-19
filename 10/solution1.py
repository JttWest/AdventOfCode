class Angle:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return self.x * self.y + self.x + self.y

def calc_angle(origin, dest):
  o_x, o_y = origin
  d_x, d_y = dest

  vector_x = d_x - o_x
  vector_y =  d_y - o_y

  # normalize
  factor = abs(gcd(vector_x, vector_y))
  return Angle(vector_x // factor, vector_y // factor)

def calc_detect_from_index(astroids, index):
  angles = set()
  for i in range(0, len(astroids)):
    if i == index:
      continue
    angles.add(calc_angle(astroids[index], astroids[i]))

  return len(angles)

def gcd(a, b):
  if b == 0:
    return a
  return gcd(b, a % b)

with open('./input.txt') as fp:
  result = 0
  astroids = []
  y = 0
  for line in fp:
    for x in range(0, len(line)):
      if line[x] == '#':
        astroids.append((x, y))
    y += 1

  for i in range(0, len(astroids)):
    result = max(result, calc_detect_from_index(astroids, i))

  print(result)