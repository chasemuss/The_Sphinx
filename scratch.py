from random import random
from math import ceil


def roll_dice(num_dice: int, dice_sides: int) -> int:
    results = [ceil(random() * dice_sides) for x in range(num_dice)]
    results.sort()
    return f'You rolled {num_dice}d{dice_sides} and got a {sum(results)}\nYour rolls were {', '.join([str(x) for x in results])}'


print(roll_dice(20, 6))