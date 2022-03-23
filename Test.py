import itertools


def SimpleBrute(numbers):
    permutations = list(itertools.permutations(list(numbers)))
    signs = ["+", "-", "/", "*", "**"]

    for version in permutations:
        for sign1 in signs:
            for sign2 in signs:
                for sign3 in signs:
                    equation = version[0] + sign1 + version[1] + sign2 + version[2] + sign3 + version[3]
                    if eval(equation) == 10:
                        return equation

    return "That's a no for simple bodmas combinations"


print(SimpleBrute("2321"))
