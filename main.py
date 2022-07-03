# Create a table, with one row for every source and one column for every destination. Each cell
# represents a route from a source to a destination. Each destination's demand is given at the
# foot of each column and each source's stock is given at the end of each row. Enter numbers
# in each cell to show how many units are to be sent along that route

# Begin with the top left-hand corner. Allocate the maximum available quantity to meet the demand
# at this destination, whilst not exceeding the stock at this source.

# As each stock is emptied, move on square down and allocate as many units as possible from the
# next source until the demand of the destination is met. As each demand is met, move one square
# to the right and again allocate as many units as possible.

# When all stock is assigned, and all the demands are met, stop.

def add_array(one, other):
    if len(one) != len(other):
        raise "Arrays not the same size"
    if len(one[0]) != len(other[0]):
        raise "Arrays not the same size"

    new_array = [[0 for j in one[0]] for i in one]
    for i in range(len(one)):
        for j in range(len(one)):
            new_array[i][j] = one[i][j] + other[i][j]

    return new_array

def mul_array(one, other):
    if isinstance(other, list):
        if len(one) != len(other):
            raise "Arrays not the same size"
        if len(one[0]) != len(other[0]):
            raise "Arrays not the same size"

        new_array = [[0 for j in one[0]] for i in one]
        for i in range(len(one)):
            for j in range(len(one[i])):
                new_array[i][j] = one[i][j] * other[i][j]

    else:
        new_array = [[0 for j in one[0]] for i in one]
        for i in range(len(one)):
            for j in range(len(one[i])):
                new_array[i][j] = one[i][j] * other

    return new_array

def none_to_zeros(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == None:
                array[i][j] = 0

    return array

def zeros_to_none(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 0:
                array[i][j] = None

    return array

def north_west_corner_method(supply, demand):
    solution = [[None for j in supply] for i in demand]

    i = 0
    j = 0
    while (j+i)<len(supply)+len(demand)-1:
        if demand[i] >= supply[j]:
            solution[i][j] = supply[j]
            demand[i] -= supply[j]
            supply[j] = 0
            j += 1
        else:
            solution[i][j] = demand[i]
            supply[j] -= demand[i]
            demand[i] = 0
            i += 1  

    return solution


# Start with the north-west corner, and set the cost linked with its source to zero

# Move along the row to any other non-empty squares. Set the cost linked with these
# destinations equal to the total transportation cost for that route (since the source
# cost for the row is 0)

# When all possible destination costs for that row have been established, go to the
# start of the next row.

# Move along this row to any non-empty squares and use the destination costs found
# earlier, to establish the source cost for the row. Once that has been done, find
# any further unknown destination costs.

# Repeat steps 3 and 4 until all source and destination costs have been found

def find_shadow_costs(solution, costs):
    shadow_costs_demand = [None for i in range(len(solution))]
    shadow_costs_supply = [None for i in range(len(solution[0]))]

    shadow_costs_supply[0] = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if solution[i][j] != None:
                if shadow_costs_supply[j] != None:
                    shadow_costs_demand[i] = costs[i][j] - shadow_costs_supply[j]
                else:
                    shadow_costs_supply[j] = costs[i][j] - shadow_costs_demand[i]

    return shadow_costs_demand, shadow_costs_supply


def find_improvement_indices(shadow_demand, shadow_supply, solution, costs):
    indices = [[0 for j in i] for i in solution]

    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if solution[i][j] == None:
                indices[i][j] = costs[i][j] - (shadow_demand[i] + shadow_supply[j])

    return indices

def is_optimal(indices):
    return min(flatten(indices)) >= 0

# Create a cycle of adjustents. The two basic rules are:
#   a) Within any row and column there can only be one increasing cell and one
#   decreasing cell
#   b) Apart from the entering cell, adjustments are only made to non-empty cells.

# Once the cycle of adjustments has been found you transfer the maximum number of units
# through this cycle. This will be equal to the smallest number in the decreasing cells
# (since you may not have negative units being transported).

# You then adjust the solution to incorporate this improvement.

def check_horizontal(solution, modifications, current_cell):
    print("checking horizontal")
    width = len(solution)
    left = [i for i in range(width)][:current_cell[1]]
    if current_cell[1] in left:
        left.remove(current_cell[1])
    right = [i for i in range(width)][current_cell[1]:]
    if current_cell[1] in right:
        right.remove(current_cell[1])

    for i in left:
        if (modifications[current_cell[0]][i] == 0) and solution[current_cell[0]][i]:
            print(f"Found: {(current_cell[0], i)}")
            return (current_cell[0], i)

    for i in right:
        if (modifications[current_cell[0]][i] == 0) and solution[current_cell[0]][i]:
            print(f"Found: {(current_cell[0], i)}")
            return (current_cell[0], i)

    return False


def check_vertical(solution, modifications, current_cell):
    print("checking vertical")
    height = len(solution[0])
    top = [i for i in range(height)][:current_cell[0]]
    if current_cell[0] in top:
        top.remove(current_cell[0])
    bottom = [i for i in range(height)][current_cell[0]:]
    if current_cell[0] in bottom:
        bottom.remove(current_cell[0])

    for i in top:
        if (modifications[i][current_cell[1]] == 0) and solution[i][current_cell[1]]:
            print(f"Found: {(i, current_cell[1])}")
            return (i, current_cell[1])

    for i in bottom:
        if (modifications[i][current_cell[1]] == 0) and solution[i][current_cell[1]]:
            print(f"Found: {(i, current_cell[1])}")
            return (i, current_cell[1])

    return False

def stepping_stone(supply, demand, costs, existing_solution, entering_cell):
    modifications = [[0 for i in supply] for j in demand]
#    print(entering_cell)
    sign = 1
    while True:
        pretty_print_solution(modifications)
        modifications[entering_cell[0]][entering_cell[1]] = 1*sign
        sign *= -1
        num_changes = 0

        # Make rest of row invalid if the row now contains two changes
        for i in range(len(modifications)):
#            print(modifications[i][entering_cell[1]], end=", ")
            if modifications[i][entering_cell[1]] != 0:
                num_changes += 1
#        print()
#        print(num_changes)
        if num_changes >= 2:
            for i in range(len(modifications)):
                if modifications[i][entering_cell[1]] == 0:
                    modifications[i][entering_cell[1]] = 2
#        print(', '.join([str(modifications[i][entering_cell[1]]) for i in range(len(modifications))]))
        new_entering_cell = check_horizontal(existing_solution, modifications, entering_cell)
        if not new_entering_cell:
            new_entering_cell = check_vertical(existing_solution, modifications, entering_cell)
        entering_cell = new_entering_cell
        if not entering_cell:
            break


    ## Get theta value

    # Separate all negative modifications
    negative_mods = [[0 for j in range(len(modifications[0]))] for i in modifications]
    for i in range(len(modifications)):
        for j in range(len(modifications[i])):
            if modifications[i][j] < 0:
                negative_mods[i][j] = -1

    # Iterate through and find the lowest cell with negative modification
    # Set theta equal to that value
    theta = 0
    for i in range(len(negative_mods)):
        for j in range(len(negative_mods[i])):
            if negative_mods[i][j] == -1:
                if existing_solution[i][j] < theta:
                    theta = existing_solution[i][j]


    ## Modify existing solution
    # new_solution = existing_solution + (modifications * theta)

    existing_solution = none_to_zeros(existing_solution)

    new_solution = add_array(existing_solution, mul_array(modifications, theta))

    new_solution = zeros_to_none(new_solution)

    return new_solution


def flatten(xss):
    return [x for xs in xss for x in xs]

def pretty_print_solution(solution):
    print_str = ""
    supplier_names = [chr(65 + i) for i in range(len(solution[0]))]
    stocker_names = [chr(90 - i) for i in range(len(solution))][::-1]
    print_str += "   "
    for stocker in stocker_names:
        print_str += f"{stocker}   "
    print_str += "\n"

    for i in range(len(supplier_names)):
        row = ""
        for j in range(len(solution)):
            row += "  "
            if solution[i][j] != None:
                row += str(solution[i][j])
            else:
                row += "-"
        print_str += f"{supplier_names[i]}{row}\n"

    print(print_str)

costs = [
        [150, 175, 188], 
        [213, 204, 198],
        [222, 218, 246]
        ]
supply = [32, 44, 34]
demand = [28, 45, 37]

def cost(solution, costs):
    total_cost = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if not solution[i][j]: solution[i][j] = 0
            total_cost += solution[i][j] * costs[i][j]

    return total_cost

def find_optimal_solution(costs, supply, demand):
    initial = north_west_corner_method(supply, demand)
    shadow_demand, shadow_supply = find_shadow_costs(initial, costs)
    indices = find_improvement_indices(shadow_demand, shadow_supply, initial, costs)

    if is_optimal(improvement_indices):
        return initial, cost(initial, costs)
    else:
        solution = stepping_stone()
        return solution, cost(solution, costs)

def index_minimum(array):
    min = array[0][0]
    index = (0, 0)
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] < min:
                min = array[i][j]
                index = (i, j)
    return index

initial_solution = north_west_corner_method(supply, demand)
shadow_demand, shadow_supply = find_shadow_costs(initial_solution, costs)
improvement_indices = find_improvement_indices(shadow_demand, shadow_supply, initial_solution, costs)
entering_cell = index_minimum(improvement_indices)

solution = stepping_stone(supply, demand, costs, initial_solution, entering_cell)

pretty_print_solution(solution)
print(cost(initial_solution, costs))
