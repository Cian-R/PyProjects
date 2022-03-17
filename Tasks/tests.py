# COMP1730/6730 S2 2021 - Homework 5
# Submission is due 11:55pm, Friday the 1st of October, 2021.

# YOUR ANU ID: uNNNNNNN
# YOUR NAME:

# Implement the function average_rank below.
# (The statement "pass" is just a placeholder that does nothing: you
# should replace it.)
# You can define other functions if it helps you decompose the problem
# and write a better organised and/or more readable solution.

import collections


def average_rank(table):
    for row in table:
        row = mappify(row)

    result = []
    for person_index in range(len(table[0])):
        ranks = []
        for row in table:
            ranks.append(row[person_index])
        result.append(sum(ranks)/len(table))
    return result


def mappify(test):
    map = {}
    index = 0
    for result in test:
        map[result] = index
        index += 1

    orderedMap = dict(reversed(sorted(map.items())))  # Create ordered dictionary in form {testscore: index}
    keyList = list(orderedMap.keys())

    for i in orderedMap:
        test[orderedMap.get(i)] = keyList.index(i) + 1

    return test


def test_average_rank_set1():
    '''
    This function runs a number of tests of the average_rank function.
    If it works ok, you will just see the output ("all set 1 tests passed")
    at the end when you call this function; if some test fails, there will
    be an error message.

    This function runs the first (simplest) set of tests; function
    test_set_2 below runs some more complicated tests.
    '''

    # two simple tests with three columns and three rows
    T1 = [[2,4,6], [1,4,9], [3,6,9]]
    assert allclose(average_rank(T1), [3,2,1])
    T2 = [[2,4,6], [4,6,2], [6,2,4]]
    assert allclose(average_rank(T2), [2,2,2])
    # more rows
    T3 = [[2,4,6], [-1,0,1], [4,6,2], [0,-1,1], [6,2,4]]
    assert allclose(average_rank(T3), [(1+3+2+2+3)/5,(2+2+3+3+1)/5,(3+1+1+1+2)/5])
    # floating point values:
    import math
    T4 = [[math.pi/4,math.pi/2,math.pi], [math.pi/2,math.pi,math.pi/4],
          [3*math.pi,math.pi,2*math.pi]]
    assert allclose(average_rank(T4), [2,2,2])
    # if there are no columns, returned list should be empty
    assert average_rank([[]]) == []
    print("all set 1 tests passed")

def test_average_rank_set2():
    '''
    This function runs a number of tests of the average_rank function.
    If it works ok, you will just see the output ("all set 1 tests passed")
    at the end when you call this function; if some test fails, there will
    be an error message.

    This function runs the second (more complex) set of tests.
    '''
    # some examples with ties
    T1 = [[2,2,6,6], [4,4,4,4]]
    assert allclose(average_rank(T1), [3,3,2,2])
    T2 = [[0,0,0,0], [1,1,1,1], [1.5,1.5,1.5,1.5]]
    assert allclose(average_rank(T2), [2.5,2.5,2.5,2.5])
    T3 = [[0,0,0,0], [1,1,1,1], [1.5,1.6,1.5,1.5]]
    assert allclose(average_rank(T3), [8/3,2,8/3,8/3])
    # example from the data science lecture:
    model_data = [[40,571,353,9,95,41,1428,350],
                  [16,200,108,2,495,434,88,0],
                  [7,352,216,9,1201,1897,9,0],
                  [10,187,202,280,704,215,47,0],
                  [52,616,204,2,47,17,122,5],
                  [4,147,146,0,3646,536,0,0],
                  [80,914,373,4,45,2,161,60],
                  [67,406,778,1,9,2,3,30],
                  [52,635,303,1,5,0,5,860],
                  [121,712,595,0,19,0,1,53],
                  [51,1914,449,0,29,18,4,50]]
    flipped = [[row[c] for row in model_data] for c in range(len(model_data[0]))]
    assert allclose(average_rank(flipped), [4.1875, 6.75, 5.75, 6.3125, 5.75, 8.1875, 4.0625, 6.5, 6.4375, 6.1875, 5.875])

def allclose(s1, s2):
    '''
    Compare two numeric sequences of equal length, and return True
    iff they are sufficiently close (< 10^-6 difference) in each
    position.
    '''
    assert len(s1) == len(s2)
    return all([abs(s1[i] - s2[i]) < 1e-6 for i in range(len(s1))])


# mappify([40,571,353,9,95,41,1428,350])

print(average_rank([[2,4,6], [1,4,9], [3,6,9]]))
