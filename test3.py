import math


def findTwinFactors(n):
    middle_val = math.sqrt(n)
    if middle_val.is_integer():
        middle_val = int(middle_val)
        print(f"Factors of {n} are {middle_val} and {middle_val}")
        return [middle_val, middle_val]
    else:
        middle_val = int(middle_val)
        for i in range(n // 2):
            if (n % (middle_val + i)) == 0:
                print(f"Factors of {n} are {middle_val + i} and {int(n / (middle_val + i))}")
                return [middle_val + i, int(n / (middle_val + i))]
            elif (n % (middle_val - i)) == 0:
                print(f"Factors of {n} are {middle_val - i} and {int(n / (middle_val - i))}")
                return [middle_val - i, int(n / (middle_val - i))]


findTwinFactors(64)
findTwinFactors(55)
findTwinFactors(100)
findTwinFactors(45)
findTwinFactors(2450)
