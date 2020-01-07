import regex as re
from math import gcd

class Moon:
  def __init__(self, position, velocity):
    self.position = position
    self.velocity = velocity

def get_osc_interval(position, velocity):
  prev_states = set()

  curr_state = tuple(position) + tuple(velocity)
  intervals = 0
  while curr_state not in prev_states:
    prev_states.add(curr_state)

    # generate new state
    # apply gravity
    for i in range(len(position)):
      for j in [x for x in range(len(position)) if x != i]:
        if position[i] < position[j]:
          velocity[i] += 1
        elif position[i] > position[j]:
          velocity[i] -= 1

    # apply velocity
    for i in range(len(position)):
      position[i] += velocity[i]

    curr_state = tuple(position) + tuple(velocity)

    intervals += 1

  return intervals

def lcm(a, b):
    return a * b // gcd(a, b)

with open('./input.txt') as fp:
  moons = []
  position_regex = re.compile("<x=(.+), y=(.+), z=(.+)>")
  for line in fp:
    re_match = position_regex.match(line)
    x, y, z = int(re_match.group(1)), int(re_match.group(2)), int(re_match.group(3))
    moon = Moon([x,y,z], [0,0,0])
    moons.append(moon)

  interval_x = get_osc_interval([m.position[0] for m in moons], [m.velocity[0] for m in moons])
  interval_y = get_osc_interval([m.position[1] for m in moons], [m.velocity[1] for m in moons])
  interval_z = get_osc_interval([m.position[2] for m in moons], [m.velocity[2] for m in moons])

  steps = lcm(interval_x,lcm(interval_y, interval_z))
  print(steps)
