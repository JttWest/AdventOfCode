IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

def print_image(pixels, image_width):
  result = ""
  for i in range(0, len(pixels)):
    if i % image_width == 0:
      result += '\n'

    if pixels[i] == '1':
      result += '*'
    else:
      result += ' '

  print(result)

with open('./input.txt') as fp:
  pixels = fp.readline()
  result_image = ['0'] * (IMAGE_WIDTH * IMAGE_HEIGHT)
  pixel_setted = [False] * (IMAGE_WIDTH * IMAGE_HEIGHT)

  for i in range(0, len(pixels)):
    result_image_i = i % (IMAGE_WIDTH * IMAGE_HEIGHT)
    pixel = pixels[i]

    if pixel_setted[result_image_i] or pixel == '2':
      continue

    result_image[result_image_i] = pixel
    pixel_setted[result_image_i] = True

  print_image(result_image, IMAGE_WIDTH)
