assignments = []

# A flag that control whether imposing diagonal Sudoku constraint
solve_diagonal = True

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Add the additional diagonal units
diagonal_units_1 = [[rows[i]+cols[i] for i in range(len(rows))]]
diagonal_units_2 = [[rows[-i-1]+cols[i] for i in range(len(rows))]]

if solve_diagonal:
    unitlist = row_units + column_units + square_units + diagonal_units_1 + diagonal_units_2
else:
    unitlist = row_units + column_units + square_units
    
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Extract any unsolved keys that has length == 2
    possible_twins = [box for box in values.keys() if len(values[box]) == 2]
     
    naked_twins = []
    # Two boxes are naked twins if they have same values and belong to each other peers
    # The computed list may have duplicate naked twins, but it doesn't affect the ultimate result   
    for box1 in possible_twins:
        identical_box = [box2 for box2 in possible_twins if values[box1]==values[box2] and box2 in peers[box1]]
        for box2 in identical_box:
            naked_twins.append([box1, box2])

    # For each naked twin's peers, eliminate the possible vaulues
    for twins in naked_twins:
        for peer in (peers[twins[0]] & peers[twins[1]]):
            for digit in values[twins[0]]:
                #values[peer] = values[peer].replace(digit,'')
                assign_value(values, peer, values[peer].replace(digit,''))
    
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Extract all keys that have been solved
    solved_keys = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_keys:
        # Get the value of the solved key
        digit = values[box]
        # For all its peers, eliminate the solved key's value (by replacing with '')
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # Go through all units (i.e. each rows, colums and 9x9 units)
    for unit in unitlist:
        for digit in '123456789':
            # For each digit, get the boxes that contains that digit
            dplaces = [box for box in unit if digit in values[box]]
            # If it is the only box that contain that digit, replace the box's value with the digit
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
               
    return values

def reduce_puzzle(values):
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
        
        # Use the Naked Twins Strategy
        values = naked_twins(values)      
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values) 
    
    if values is False:
        return False ## Failed to find a solution
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    grid_1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    grid_2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    values = solve(diag_sudoku_grid)
    
    if values == False:
        print('The sudoku is unsolvable')
    else:
        display(values)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
