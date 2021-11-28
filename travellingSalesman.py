from common import SolutionSpace
from typing import List
from dataclasses import dataclass
import copy


@dataclass
class TSPSoln(SolutionSpace):
    TSP_MATRIX = [[0, 12, 29, 22, 13, 24],
       [12, 0, 19, 3, 25, 6],
       [29, 19, 0, 21, 23, 28],
       [22, 3, 21, 0, 4, 5], 
       [13, 25, 23, 4, 0, 16], 
       [24, 6, 28, 5, 16, 0]]
    
    soln_space: List  # [1, 4, 3, 2]
    num_variables: int
    curr_bound: int
    curr_weight: int

    def __init__(self):
        self.num_variables = len(TSPSoln.TSP_MATRIX)
        self.soln_space = [1]
        self.curr_bound = 0

        for i in range(self.num_variables):
            self.curr_bound += (firstMin(TSPSoln.TSP_MATRIX, i, self) + 
                        secondMin(TSPSoln.TSP_MATRIX, i, self))
                    
        self.curr_weight = 0


    def is_singular(self):
        if len(self.soln_space) != self.num_variables:
            return False

        return True


    def debug(self):
        return self.soln_space


    def debug_short(self):
        return self.soln_space


    def is_feasable(self):
        return True

# Function to find the minimum edge cost 
# having an end at the vertex i
def firstMin(adj, i, soln_space: TSPSoln):
    min = float('inf')
    for k in range(soln_space.num_variables):
        if adj[i - 1][k] < min and i != k:
            min = adj[i - 1][k]

    return min

# function to find the second minimum edge 
# cost having an end at the vertex i
def secondMin(adj, i, soln_space: TSPSoln):
    first, second = float('inf'), float('inf')
    for j in range(soln_space.num_variables):
        if i == j:
            continue
        if adj[i - 1][j] <= first:
            second = first
            first = adj[i - 1][j]

        elif(adj[i - 1][j] <= second and 
            adj[i - 1][j] != first):
            second = adj[i - 1][j]

    return second

def tsp_branch(soln_space: TSPSoln) -> List[TSPSoln]:
    arr = []

    for i in range(1, soln_space.num_variables + 1):
        if i not in soln_space.soln_space:
            temp = copy.deepcopy(soln_space)
            temp.soln_space.append(i)
            temp.curr_weight += TSPSoln.TSP_MATRIX[temp.soln_space[-2] - 1][temp.soln_space[-1] - 1]
            arr.append(temp)
    return arr

def tsp_bound(soln: TSPSoln) -> float:  
    if len(soln.soln_space) == 1:
        soln.curr_bound -= ((firstMin(TSPSoln.TSP_MATRIX, soln.soln_space[len(soln.soln_space) - 1], soln) + 
                        firstMin(TSPSoln.TSP_MATRIX, soln.soln_space[-1], soln)) / 2)
    else:
        soln.curr_bound -= ((secondMin(TSPSoln.TSP_MATRIX, soln.soln_space[len(soln.soln_space) - 1], soln) +
                            firstMin(TSPSoln.TSP_MATRIX, soln.soln_space[-1], soln)) / 2)

    res =  (soln.curr_bound + soln.curr_weight)*-1

    # Since compared values include the cost to return to the first node,
    # we must adjust the bound DOWN (towards zero) to viable more solutions since the default bound calculation 
    # does not include the return home cost. The bound should be adjusted by the maximum possible 
    # return-home cost, the largest value in row 0 that we have not already visited 
    res += max(val for (key, val) in enumerate(soln.TSP_MATRIX[0]) if key-1 not in soln.soln_space) # Add return home penalty

    return res

def tsp_value(soln: TSPSoln) -> float:
    running_val = 0
    for i in range(1, soln.num_variables):
        running_val += TSPSoln.TSP_MATRIX[soln.soln_space[i-1]-1][soln.soln_space[i]-1]

    return (running_val + TSPSoln.TSP_MATRIX[soln.soln_space[i]-1][0])*-1

