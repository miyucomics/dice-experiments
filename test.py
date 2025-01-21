from collections import Counter, deque
from fractions import Fraction

maximum_dice = 4
valid_dice = [6]
polynomial_lookup = [{i + 1: 1 for i in range(dice)} for dice in valid_dice]

def multiply_polynomials(a, b):
    result = Counter()
    for apow, aco in a.items():
        for bpow, bco in b.items():
            result[apow + bpow] += aco * bco
    return result

def farey_sequence(order):
    a, b, c, d = 0, 1, 1, order
    yield Fraction(a, b)
    while c <= order:
        k = (order + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield Fraction(a, b)

best_match_so_far = {term: (tuple(), tuple(), 1) for term in farey_sequence(100) if term >= 0.5}
perfect_matches = {}

def update_dictionaries(breadcrumbs, probability_map):
    running_sum = 0
    sorted_terms = sorted(probability_map.items())
    denominator = sum(probability_map.values())
    small = min(probability_map.keys())
    big = max(probability_map.keys())
    for number, ways in sorted_terms:
        running_sum += ways
        for target in list(best_match_so_far.keys()):
            _, _, error = best_match_so_far[target]
            distance = abs(target - Fraction(running_sum, denominator))
            if distance == 0:
                best_match_so_far.pop(target)
                perfect_matches[target] = (breadcrumbs, (number, big - (number - small)), distance)
                perfect_matches[1 - target] = (breadcrumbs, (big - (number - small), number), distance)
            if distance < error:
                best_match_so_far[target] = (breadcrumbs, (number, big - (number - small)), distance)

queue = deque([(0, tuple(), {0: 1}, 0)])

while queue:
    dice_count, breadcrumbs, probabilities, highest_dice = queue.popleft()
    update_dictionaries(breadcrumbs, probabilities)

    if dice_count < maximum_dice:
        for i, dice_type in enumerate(valid_dice[highest_dice:]):
            queue.append((
                dice_count + 1,
                breadcrumbs + tuple([dice_type]),
                multiply_polynomials(probabilities, polynomial_lookup[highest_dice + i]),
                highest_dice + i
            ))

for target, data in sorted(perfect_matches.items(), key=lambda x: x[1][2]):
    print(target, data)
