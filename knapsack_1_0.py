from dataclasses import dataclass
from common import SolutionSpace
import copy
from typing import List




@dataclass
class KnapsackSoln(SolutionSpace):

    soln_space: dict # { 1: True, 2: None, 3: False, etc.... }
    num_variables: int

    # sorted by best value/weight
    remaining_items: list #  [(id, weight, value), (id, weight, value)] #

    KNAPSACK_ITEMS = {}
    KNAPSACK_MAX_CAPACITY = None


    def __init__(self):
        if not KnapsackSoln.KNAPSACK_ITEMS:
            raise ValueError("No items set")

        if not KnapsackSoln.KNAPSACK_MAX_CAPACITY:
            raise ValueError("No Max Capacity")

        self.num_variables = len(KnapsackSoln.KNAPSACK_ITEMS)

        self.remaining_items = []

        self.soln_space = {}

        for i in range(1,self.num_variables + 1):
            self.soln_space[i] = None

        for item_id, item_info in KnapsackSoln.KNAPSACK_ITEMS.items():
            self.remaining_items.append((item_id, item_info[0], item_info[1]))

        self.remaining_items.sort(key=lambda a: a[2]/a[1], reverse=True)

    def is_singular(self):
        for i in range(1, self.num_variables+1):
            if not self.soln_space[i] in [True, False]:
                return False

        return True

    def debug(self):
        print("Solution space description: ")
        for i in range(1, self.num_variables+1):
            if self.soln_space[i] is True:
                print("  Item {} is in!".format(i))
            elif self.soln_space[i] is False:
                print("  Item {} is out!".format(i))
            else:
                print("  Item {} is undecided!".format(i))

        print("Remaining items: {}", self.remaining_items)

    def debug_short(self):
        strs = []
        for i in range(1, self.num_variables+1):
            if self.soln_space[i] is True:
                strs.append("{} IN".format(i))
            elif self.soln_space[i] is False:
                strs.append("{} OUT".format(i))

        return "({})".format(', '.join(strs))

    def is_feasable(self):
        running_sum = 0

        for i in range(1, self.num_variables+1):
            if self.soln_space[i] is True:
                running_sum += KnapsackSoln.KNAPSACK_ITEMS[i][0]

        return (running_sum <= KnapsackSoln.KNAPSACK_MAX_CAPACITY)

def knapsack_branch(soln_space: KnapsackSoln) -> List[KnapsackSoln]:
    new_soln_in: KnapsackSoln = copy.deepcopy(soln_space)

    next_item_id = new_soln_in.remaining_items.pop(0)[0]
    new_soln_in.soln_space[next_item_id] = True

    new_soln_out = copy.deepcopy(new_soln_in)
    new_soln_out.soln_space[next_item_id] = False

    return [new_soln_out, new_soln_in]

def knapsack_bound(soln: KnapsackSoln) -> float:
    running_val = 0
    occupied_weight = 0

    for i in range(1, soln.num_variables + 1):
        if(soln.soln_space[i] is True):
            occupied_weight += KnapsackSoln.KNAPSACK_ITEMS[i][0]
            running_val += KnapsackSoln.KNAPSACK_ITEMS[i][1]

    # assume non-singular solution...
    next_best_item = soln.remaining_items[0]
    next_best_value = next_best_item[2]/next_best_item[1]

    return running_val + (KnapsackSoln.KNAPSACK_MAX_CAPACITY-occupied_weight)*next_best_value

def knapsack_value(soln: KnapsackSoln) -> float:
    running_val = 0
    for i in range(1, soln.num_variables + 1):
        if(soln.soln_space[i] is True):
            running_val += KnapsackSoln.KNAPSACK_ITEMS[i][1]

    return running_val

