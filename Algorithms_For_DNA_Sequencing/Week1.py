list = ['a','b','c','d']

string = "".join(list)

import random

print(random.choice('ACGT'))

seq = ""

for _ in range(10):
    seq += random.choice('ACGT')

print(seq)

""" String formatting """
price = 59
txt = f"The price is {price:,} dollars."
print(txt)

