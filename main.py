from collections import deque, defaultdict
from fractions import Fraction

tolerance = 0
maximum_dice = 9
valid_dice = [4, 6, 8, 12, 20]

polynomial_lookup = [
    {i + 1: 1 for i in range(dice)}
    for dice in valid_dice
]

def multiply_polynomials(a, b):
    result = defaultdict(int)
    for apow, aco in a.items():
        for bpow, bco in b.items():
            result[apow + bpow] += aco * bco
    return result

def probability_valid(probability_map, target):
    running_sum = 0
    small = min(probability_map.keys())
    big = max(probability_map.keys())
    all_possible = sum(probability_map.values())
    sorted_items = sorted(probability_map.items())
    for key, value in sorted_items:
        running_sum += value
        if abs(target - Fraction(running_sum, all_possible)) <= tolerance:
            return True, [key, big - (key - small)]

    return False, None

def find_dice(target):
    queue = deque([(0, tuple(), {0: 1}, 0)])

    while queue:
        dice_count, breadcrumb, probabilities, highest_dice = queue.popleft()

        success, threshold = probability_valid(probabilities, target)
        if success:
            return breadcrumb, threshold

        if dice_count < maximum_dice:
            for i, dice_type in enumerate(valid_dice[highest_dice:]):
                queue.append((
                    dice_count + 1,
                    breadcrumb + tuple([dice_type]),
                    multiply_polynomials(probabilities, polynomial_lookup[highest_dice + i]),
                    highest_dice + i
                ))

    return None, ()

def farey_sequence(order):
    farey_pairs = [(0, 1), (1, 1)]

    a, b = 0, 1
    c, d = 1, order

    while c <= order:
        k = (order + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        farey_pairs.append((a, b))

    return farey_pairs

for a, b in farey_sequence(9):
    dice, threshold = find_dice(Fraction(a, b))
    print(Fraction(a, b), dice, threshold)
