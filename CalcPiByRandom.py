import random

pi = 3.1415926535897932384626433832795
# Create n number of points on a unit graph.
# Count the number of points inside the unit circle by using a simplified distance formula.
#
def calcPi(n):
    numInside = 0
    numTotal = 0

    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            numInside += 1
    return 4 * (numInside / n)


print(calcPi(10))
print(calcPi(100))
print(calcPi(1000))
print(calcPi(100000))
print(calcPi(1000000))
