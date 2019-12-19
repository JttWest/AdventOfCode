import math
from functools import reduce

class Direction:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return self.x * self.y + self.x + self.y

class Astroid:
  def __init__(self, location):
    self.location = location
    self.laser_precedence = 0

  def __lt__(self, other):
    return self.laser_precedence < other.laser_precedence

  def calc_direction(self, origin):
    o_x, o_y = origin.location
    d_x, d_y = self.location

    vector_x = d_x - o_x
    vector_y =  o_y - d_y

    # normalize
    factor = abs(gcd(vector_x, vector_y))
    return Direction(vector_x // factor, vector_y // factor)

  def calc_distance(self, origin):
    o_x, o_y = origin.location
    d_x, d_y = self.location

    return abs(d_x - o_y) + abs(d_y - o_y)

  def set_laser_precedence(self, precedence):
    self.laser_precedence = precedence

def generate_astroid_directions(astroids, reference):
  directions = {}
  for ast in astroids:
    if ast == reference:
      continue

    direction = ast.calc_direction(reference)
    if direction in directions:
      # insert astroid by ascending distance
      dist = ast.calc_distance(reference)
      same_direction_astroids = directions[direction]
      insertion_i = 0
      for i in range(0, len(same_direction_astroids)):
        insertion_i = i
        if same_direction_astroids[i].calc_distance(reference) > dist:
          break

      same_direction_astroids.insert(insertion_i, ast)
    else:
      directions[direction] = [ast]

  return directions

def calc_radian(origin, dest):
  o_x, o_y = origin
  d_x, d_y = dest
  vector_x = d_x - o_x
  vector_y =  -(d_y - o_y)
  v1_theta = math.atan2(1, 0)
  v2_theta = math.atan2(vector_y, vector_x)
  angle = (v1_theta - v2_theta)
  # convert from [-PI, PI] to [0, 2PI]
  angle = angle if angle >= 0 else angle + 2 * math.pi
  return angle

def gcd(a, b):
  if b == 0:
    return a
  return gcd(b, a % b)

def find_astroid_to_place_laser(astroids):
  astroid = None
  num_planets = 0
  for i in range(0, len(astroids)):
    directions = generate_astroid_directions(astroids, astroids[i])
    if len(directions) > num_planets:
      astroid = astroids[i]
      num_planets = len(directions)
  return astroid

with open('./input.txt') as fp:
  astroids = []
  y = 0
  for line in fp:
    for x in range(0, len(line)):
      if line[x] == '#':
        astroids.append(Astroid((x, y)))
    y += 1

  laser_on_astroid = find_astroid_to_place_laser(astroids)
  directions = generate_astroid_directions(astroids, laser_on_astroid)

  astroids_to_sort = []
  for same_path_astroids in directions.values():
    for i in range(0, len(same_path_astroids)):
      ast = same_path_astroids[i]
      rad = calc_radian(laser_on_astroid.location, ast.location)
      laser_precedence = rad if i == 0 else 10**i + rad
      ast.set_laser_precedence(laser_precedence)
      astroids_to_sort.append(ast)

  astroids_to_sort.sort()
  x, y = astroids_to_sort[199].location
  print(x * 100 + y)
