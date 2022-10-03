import random
import math

arms = []
arm_count = []
total = 0


def bandit(testNum, armIdx, pullVal):
    global arms, arm_count, total
    if testNum == 0:
        arms = [0 for x in range(armIdx)]
        arm_count = [0 for x in range(armIdx)]
        total = 0
        return 0
    else:
        total += 1
        arm_count[armIdx] += 1
        arms[armIdx] = ((arms[armIdx] * (arm_count[armIdx] - 1)) + pullVal) / arm_count[armIdx]
        if testNum <= 9:
            return testNum
        else:
            calculate = [arms[x] + math.sqrt(((.5 * math.log(total)) / arm_count[x])) for x in range(10)]
            max_value = max(calculate)
            return calculate.index(max_value)
# Aditya Kak 3 2022