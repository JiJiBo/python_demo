from fractions import Fraction
import time

x = Fraction(3, 5)
y = Fraction(1, 5)
count = 0
time.sleep(10)
while x < 10:
    print(x)
    time.sleep(0.05)
    x = x * y - 1
    count = count + 1
    if count == 100000:
        break
time.sleep(2)