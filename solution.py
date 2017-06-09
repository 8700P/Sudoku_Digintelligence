from collections import Counter
import collections

assignments = []


def assign_value(values, box, value):
    if values[box] == value:
        return values
    values[box] = values
    if len(value) == 1:
        assignments.append(values.copy())
    return value


def cross(a, b):
    return [s + t for s in a for t in b]


rows = 'ABCDEFGHI'
cols = '123456789'
digits = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_1 = [a[0] + a[1] for a in zip(rows, cols)]
diagonal_2 = [a[0] + a[1] for a in zip(rows, cols[::-1])]
unitlist = row_units + column_units + square_units + [diagonal_1] + [diagonal_2]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)

"""for s in diagonal1:
    for a in diagonal1:
        peers[s].add(a)
        peers[s].remove(s)


for s in diagonal2:
    for a in diagonal2:
        peers[s].add(a)
        peers[s].remove(s)"""


"""def display(values):
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return"""


def grid_values(grid):
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
            print(solved_values)
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def naked_twins(values):
    twins = False
    while not twins:
        grid_before = values
        for unit in unitlist:
            tw = [values[box] for box in unit if len(values[box]) == 2]
            tp = [v for v, n in collections.Counter(tw).items() if n == 2]
            # print(tw)
            # tws = [box for box in tw if len(tw) >= 2]
            # print(tws)
            # p = [box[0:2] for box in tws if len(tws) == 2]
            # print(p)
            # tp = Counter(p)
            # print(tp)
            nt = [box for box in tp if len(tp) == 1]
            # print(nt)
            for box in nt:
                ntb = box[0] + box[1]
                # print(ntb)
                for peer in unit:
                    if len(values[peer]) >= 2 and ntb != values[peer]:
                        assign_value(values, peer, values[peer].replace(ntb[0], '').replace(ntb[1], ''))
        grid_after = values
        twins = grid_before == grid_after

    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        #values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


'''def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values'''


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
