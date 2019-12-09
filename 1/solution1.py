with open('./input.txt') as fp:
  result = 0
  
  for line in fp:
    mass = int(line)
    fuel = mass // 3 - 2
    result += fuel

  print(result)
