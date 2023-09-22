import random

numbers = []
for x in range(1, 11):
    numbers.append(x)

for i in range(9):
    random.shuffle(numbers)
    print(numbers)