# returns the total direct and indirect orbits starting at planet
def calc_orbits(planet, orbit_map, indirect_orbits):
  result = indirect_orbits
  if planet not in orbit_map:
    return result

  for p in orbit_map[planet]:
    result += calc_orbits(p, orbit_map, indirect_orbits+1)
  return result

with open('./input.txt') as fp:
  orbit_map = {}

  for orbit in fp:
    planets = orbit.strip().split(')')
    p1, p2 = planets[0], planets[1]
    if p1 not in orbit_map:
      orbit_map[p1] = {p2}
    else:
      orbit_map[p1].add(p2)

  print(calc_orbits('COM', orbit_map, 0))