
with open('./input.txt') as fp:
  result = 0
  orbit_map = {}

  for orbit in fp:
    planets = orbit.strip().split(')')
    p1, p2 = planets[1], planets[0]
    orbit_map[p1] = p2

  path_YOU = {}
  dist_YOU = 0
  i = orbit_map['YOU']
  while i in orbit_map:
    path_YOU[i] = dist_YOU
    i = orbit_map[i]
    dist_YOU += 1

  j = orbit_map['SAN']
  dist_SAN = 0
  while j in orbit_map:
    if j in path_YOU:
      result = dist_SAN + path_YOU[j]
      break
    j = orbit_map[j]
    dist_SAN += 1

  print(result)