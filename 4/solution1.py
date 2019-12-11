# def get_lowest_valid(low):
#   num = [int(i) for i in str(low)]
#   first_dec_i = 1
#   for i in range(1, len(num)):
#     if num[i] < num[i-1]:
#       break
#     first_dec_i += 1

#   # pad the rest
#   pad_val = num[first_dec_i-1]
#   while first_dec_i < len(num):
#     num[first_dec_i] = pad_val
#     first_dec_i += 1
#   return num

def contains_dup(num_str):
  for i in range(1, len(num_str)):
    if num_str[i] == num_str[i-1]:
      return True

  return False

def is_incr(num_str):
  for i in range(1, len(num_str)):
    if num_str[i] < num_str[i-1]:
      return False

  return True


def solution(low, high):
  count = 0
  for i in range(low, high+1):
    num_str = str(i)
    if contains_dup(num_str) and is_incr(num_str):
      count += 1
  return count

print(solution(108457, 562041))
