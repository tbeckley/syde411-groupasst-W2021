from dataclasses import dataclass
from queue import LifoQueue

@dataclass
class SolutionSpace:
    is_singular: callable
    is_feasable: callable
    soln_space: dict
    debug_short: callable


def branch_and_bound(orig_soln_space: SolutionSpace, objective_fn: callable, bound: callable, branch: callable, best_soln_val = 0, debug=False):
    soln_queue = LifoQueue()
    soln_queue.put(orig_soln_space)
    best_soln = None

    while not soln_queue.empty():
        test_node: SolutionSpace = soln_queue.get()

        if debug:
            print("Exploring", test_node.debug_short())

        if test_node.is_singular():
            test_node_val = objective_fn(test_node)
            if test_node_val > best_soln_val:
                best_soln = test_node
                best_soln_val = test_node_val

        else:
            new_nodes: list[SolutionSpace] = branch(test_node)

            for new_node in new_nodes:
                if new_node.is_feasable():
                    if new_node.is_singular() or bound(new_node) >= best_soln_val:
                        soln_queue.put(new_node)
                    elif debug:
                        print("Removing {} because bound is too low", new_node.debug_short())
                elif debug:
                    print("Removing {} because infesable", new_node.debug_short())

    return (best_soln, best_soln_val)
