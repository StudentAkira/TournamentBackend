import time

d = {
    'a': 1000,
    'b': 2,
    'c': 3,
    'd': 4
}

max_value = -1000
second_max_value = -1000

for k in d.keys():
    if d[k] > second_max_value:
        second_max_value = d[k]
    if d[k] > max_value:
        second_max_value = max_value
        max_value = d[k]

print(max_value)
print(second_max_value)