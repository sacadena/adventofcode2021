import re
from collections import defaultdict
from itertools import product

POSSIBLE_DRAWS = [sum(rolls) for rolls in product(range(1, 4), repeat=3)]

UNIQUE_DRAW_COUNTS = defaultdict(int)
for sum_roll in POSSIBLE_DRAWS:
    UNIQUE_DRAW_COUNTS[sum_roll] += 1


def main():
    with open('data/day21.txt') as h:
        contents = h.read()
    contents = contents.strip().split('\n')
    p1, p2 = list(map(lambda x: int(re.search('\d+', x[10:]).group()),
                    contents))

    roll, scores = practice_game(p1, p2)
    asw1 = roll * min(scores.values())
    print(f'(Puzzle 1) Looser score times dice rolls: {asw1}')


    p1_wins, p2_wins = fast_play((p1, 0), (p2, 0))
    asw2 = (max(p1_wins, p2_wins))
    print(f'(Puzzle 2) Number of universes with most wins: {asw2}')


def practice_game(p1, p2):
    pos, scores = {0: p1, 1: p2}, {0: 0, 1: 0}
    player, roll = 0, 1
    while all([v < 1000 for v in scores.values()]):
        sum_roll = sum([(roll + s) % 100 for s in range(3)])
        pos[player] = (pos[player] + sum_roll - 1) % 10 + 1
        scores[player] += pos[player]
        player = 1 - player
        roll += 3
    return roll-1, scores


def slow_play(player, pos, scores):
    if any([v >= 21 for v in scores.values()]):
        winner = max(scores, key=scores.get)
        return {k: 1 if k == winner else 0 for k in scores}

    other_player = 1 if not(player) else 0
    count_victories = {0: 0, 1:0}
    for sum_rolls in UNIQUE_DRAW_COUNTS:
        positions_here = {k: v for k, v in pos.items()}
        scores_here = {k: v for k, v in scores.items()}
        positions_here[player] = (positions_here[player] + draw - 1) % 10 + 1
        scores_here[player] += positions_here[player]
        this = slow_play(other_player, positions_here, scores_here)
        count_victories = {k: UNIQUE_DRAW_COUNTS[sum_rolls]*this[k] + v for k, v in count_victories.items()}
    return count_victories


def fast_play(x, y, table = dict()):
    if (x, y) in table:  # memoization
        return table[(x, y)]

    posx, scorex = x
    posy, scorey = y

    if scorex >= 21:
        return 1, 0
    if scorey >= 21:
        return 0, 1

    winx, winy = 0, 0

    for sum_rolls in UNIQUE_DRAW_COUNTS:
        posx_new = (posx + sum_rolls - 1) % 10 + 1
        scorex_new = scorex + posx_new
        wy, wx = fast_play(y, (posx_new, scorex_new), table)
        winx += wx * UNIQUE_DRAW_COUNTS[sum_rolls]
        winy += wy * UNIQUE_DRAW_COUNTS[sum_rolls]

    table[(x, y)] = winx, winy
    return winx, winy

if __name__ == '__main__':
    main()
