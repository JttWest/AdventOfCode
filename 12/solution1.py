import regex as re

class Moon:
  def __init__(self, position, velocity):
    self.position = position
    self.velocity = velocity

  def get_potential_energy(self):
    x, y, z = self.position
    return abs(x) + abs(y) + abs(z)

  def get_kinetic_energy(self):
    x, y, z = self.velocity
    return abs(x) + abs(y) + abs(z)

def get_moon_pairs(moons):
  res = []
  for i in range(0, len(moons)):
    for j in range(i+1, len(moons)):
      pair = (moons[i], moons[j])
      res.append(pair)
  return res

def apply_gravity_on_axis(dimension_index, moon_pair):
  moon_1, moon_2 = pair
  pos_1 = moon_1.position[dimension_index]
  pos_2 = moon_2.position[dimension_index]

  if pos_1 > pos_2:
    moon_1.velocity[dimension_index] -= 1
    moon_2.velocity[dimension_index] += 1
  elif pos_2 > pos_1:
    moon_1.velocity[dimension_index] += 1
    moon_2.velocity[dimension_index] -= 1

def apply_velocity_on_axis(dimension_index, moon):
  vel = moon.velocity[dimension_index]
  moon.position[dimension_index] += vel

with open('./input.txt') as fp:
  steps = 1000

  moons = []
  position_regex = re.compile("<x=(.+), y=(.+), z=(.+)>")
  for line in fp:
    re_match = position_regex.match(line)
    x, y, z = int(re_match.group(1)), int(re_match.group(2)), int(re_match.group(3))
    moon = Moon([x,y,z], [0,0,0])
    moons.append(moon)

  moon_pairs = get_moon_pairs(moons)
  for _ in range(0, steps):
    # apply gravity
    for pair in moon_pairs:
      for dimension in range(0, 3):
        apply_gravity_on_axis(dimension, pair)

    # apply velocity
    for moon in moons:
      for dimension in range(0, 3):
        apply_velocity_on_axis(dimension, moon)

  total_energy = 0
  for moon in moons:
    total_energy += moon.get_kinetic_energy() * moon.get_potential_energy()

  print(total_energy)
