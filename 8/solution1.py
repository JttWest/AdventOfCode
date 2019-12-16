IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

def parse_image(pixels, start_i, end_i):
  num_0 = 0
  num_1 = 0
  num_2 = 0
  for i in range(start_i, end_i):
    d = pixels[i]
    if d == '0':
      num_0 += 1
    elif d == '1':
      num_1 += 1
    elif d == '2':
      num_2 += 1

  return (num_0, num_1, num_2)

with open('./input.txt') as fp:
  layer = (float('Inf'), 0, 0)
  pixels = fp.readline()

  i = 0
  while i < len(pixels):
    layer_res = parse_image(pixels, i, i + (IMAGE_WIDTH * IMAGE_HEIGHT))
    if layer_res[0] < layer[0]:
      layer = layer_res 

    i += IMAGE_WIDTH * IMAGE_HEIGHT

  print(layer[1]*layer[2])