import random

arms = []
arm_count = []


def bandit(testNum, armIdx, pullVal):
    global arms, arm_count
    epsilon = .05
    if testNum == 0:
        arms = [0 for x in range(armIdx)]
        arm_count = [0 for x in range(armIdx)]
        return 0
    elif testNum > 0:
        arm_count[armIdx] += 1
        arms[armIdx] = ((arms[armIdx] * (arm_count[armIdx] - 1)) + pullVal) / arm_count[armIdx]
        p = random.random()
        if p < epsilon:
            return random.randint(0, len(arms) - 1)
        else:
            max_value = max(arms)
            return arms.index(max_value)

"""
def main():
    print()


if __name__ == "__main__":
    main()
"""

# Aditya Kak 3 2022