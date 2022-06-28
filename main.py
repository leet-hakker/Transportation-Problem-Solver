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
# through this cycle. This will be euqal to the smallest number in the decreasing cells
# (since you may not have negative units being transported).

# You then adjust the solution to incorporate this improvement.

def stepping_stone(costs, existing_solution):
    pass

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

initial_solution = north_west_corner_method(supply, demand)
shadow_demand, shadow_supply = find_shadow_costs(initial_solution, costs)
improvement_indices = find_improvement_indices(shadow_demand, shadow_supply, initial_solution, costs)

pretty_print_solution(initial_solution)
print(cost(initial_solution, costs))
