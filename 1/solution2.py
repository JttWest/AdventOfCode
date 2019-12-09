def calc_fuel(mass):
  fuel = mass // 3 - 2
  if fuel > 0:
    return fuel + calc_fuel(fuel)
  return 0

with open('./input.txt') as fp:
  result = 0

  for line in fp:
    mass = int(line)
    fuel = calc_fuel(mass)
    result += fuel

  print(result)
