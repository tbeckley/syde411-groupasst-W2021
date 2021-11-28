from common import branch_and_bound
from time import perf_counter_ns

from itertools import permutations

from travellingSalesman import tsp_bound, tsp_branch, tsp_value, TSPSoln
from knapsack_1_0 import knapsack_bound, knapsack_branch, knapsack_value, KnapsackSoln

#region [ Knapsack ]

def knapsack_fast_soln(items: dict, capacity: float):
    sorted_items = sorted(items.values(), key=lambda a: a[1]/a[0], reverse=True)

    running_total = 0
    running_weight = 0

    for item in sorted_items:
        if running_weight + item[0] <= capacity:
            running_total += item[1]
            running_weight += item[0]

    return running_total

def knapsack_exhuastion_solution(items: dict, capacity:float):
    best_soln = 0

    vals = list(items.values()) #[]
    num_items = len(vals)

    for i in range(2**num_items):
        running_total = 0
        running_weight = 0
        for j in range(num_items): 
            if (i>>j & 1) == 1:
                running_weight += vals[j][0]
                running_total += vals[j][1]

            if running_weight > capacity:
                break

        if running_weight <= capacity and running_total > best_soln:
            best_soln = running_total

    return best_soln

def benchmark_knapsack(items: dict, cap: float, case_name: str):
    KnapsackSoln.KNAPSACK_ITEMS = items
    KnapsackSoln.KNAPSACK_MAX_CAPACITY = cap

    print("Running benchmarks...")

    start = perf_counter_ns()
    (_, bnb_soln_val) = branch_and_bound(KnapsackSoln(), knapsack_value, knapsack_bound, knapsack_branch)
    end = perf_counter_ns()
    bnb_time = end-start


    start = perf_counter_ns()
    approx_soln_val = knapsack_fast_soln(items, cap)
    end = perf_counter_ns()
    approx_time = end-start

    start = perf_counter_ns()
    exhaustive_soln_val = knapsack_exhuastion_solution(items, cap)
    end = perf_counter_ns()
    exhaustive_time = end-start

    max_time = max(exhaustive_time, approx_time, bnb_time)

    print("Results for", case_name)
    print("Branch-And-Bound solution: {:8.2f}, time: {:9} us, percent of slowest solution: {:5.1f}".format(bnb_soln_val, int(bnb_time/1_000), bnb_time/max_time*100))
    print("Approximate solution:      {:8.2f}, time: {:9} us, percent of slowest solution: {:5.1f}".format(approx_soln_val, int(approx_time/1_000), approx_time/max_time*100))
    print("Exhaustive solution:       {:8.2f}, time: {:9} us, percent of slowest solution: {:5.1f}".format(exhaustive_soln_val, int(exhaustive_time/1_000), exhaustive_time/max_time*100))

def run_knapsack_benchmarks():
    test_values_1 = {
        1: (6, 50),
        2: (5, 30),
        3: (5, 30)
    }

    test_cap_1 = 10

    test_values_2 = {
        1: (2, 40),
        2: (3.14, 50),
        3: (1.98, 100),
        4: (5, 95),
        5: (3, 30)
    }

    test_cap_2 = 10

    test_values_3 = {1: (1.83, 33.41), 2: (2.1, 13.07), 3: (2.13, 29.55), 4: (4.39, 77.13), 5: (2.22, 48.01), 6: (3.17, 72.84), 7: (1.4700000000000002, 16.29), 8: (3.19, 0.26), 9: (4.7299999999999995, 39.88), 10: (1.02, 11.71), 11: (3.33, 59.2), 12: (3.79, 21.21), 13: (1.82, 3.38), 14: (4.63, 54.85), 15: (2.62, 16.75)}
    test_cap_3 = 20

    test_values_4 = {1: (0.94, 12.58), 2: (2.18, 18.16), 3: (4.909999999999999, 0.76), 4: (1.87, 25.15), 5: (2.8400000000000003, 25.71), 6: (3.99, 61.15), 7: (3.64, 25.29), 8: (0.32, 6.94), 9: (0.36, 2.61), 10: (0.74, 15.24), 11: (2.69, 58.92), 12: (3.92, 73.68), 13: (0.94, 0.28), 14: (1.7200000000000002, 22.75), 15: (4.859999999999999, 120.58), 16: (4.199999999999999, 18.77), 17: (2.16, 12.46), 18: (2.46, 42.55), 19: (2.73, 5.6), 20: (4.659999999999999, 23.39), 21: (4.9799999999999995, 23.53), 22: (2.5700000000000003, 4.65), 23: (0.11, 1.3), 24: (1.6700000000000002, 8.33), 25: (3.35, 44.65) }
    test_cap_4 = 50


    benchmark_knapsack(test_values_1, test_cap_1, "Case 1 - strategically selected edge case")
    benchmark_knapsack(test_values_2, test_cap_2, "Case 2 - example 5-item test case")
    benchmark_knapsack(test_values_3, test_cap_3, "Case 3 - 15 semi-random items")
    benchmark_knapsack(test_values_4, test_cap_4, "Case 4 - 25 semi-random items")

#endregion [ Knapsack ]

#region [ Travelling Salesman ]

def ts_approx_soln(matrix: list):
    soln = [1]
    running_total = 0

    while(len(soln) < len(matrix)):
        min_city_no = -1
        min_city_val = 9999999999

        for idx, val in enumerate(matrix[soln[-1]-1]):
            if not (idx+1) in soln and val < min_city_val:
                min_city_no = idx+1
                min_city_val = val
        
        soln.append(min_city_no)
        running_total += min_city_val

    running_total += matrix[soln[-1]-1][0]
    soln.append(1)
    return (soln, running_total)

def ts_exhaustive_soln(matrix: list):
    num_cities = len(matrix)

    cities = list(range(1, num_cities))

    best_soln = None
    best_soln_val = 9999999

    for r in permutations(cities):
        route = [0] + list(r) + [0]
        
        running_soln_val = 0

        for i in range(num_cities):
            running_soln_val += matrix[route[i]][route[i+1]]

        if running_soln_val < best_soln_val:
            best_soln_val = running_soln_val
            best_soln = route

    return ([i+1 for i in best_soln], best_soln_val)

def benchmark_ts(matrix: list, case_name: str):
    TSPSoln.TSP_MATRIX = matrix


    print("Running benchmarks...")

    start = perf_counter_ns()
    (bnb_soln_rough, bnb_val_rough) = branch_and_bound(TSPSoln(), tsp_value, tsp_bound, tsp_branch, -99999999999)
    end = perf_counter_ns()
    bnb_time = end-start
    bnb_soln = bnb_soln_rough.debug_short() + [1]
    bnb_val = -bnb_val_rough

    start = perf_counter_ns()
    (approx_sln, approx_val) =(ts_approx_soln(matrix))
    end = perf_counter_ns()
    approx_time = end-start

    start = perf_counter_ns()
    (exhaustive_soln, exhaustive_val) = (ts_exhaustive_soln(matrix))
    end = perf_counter_ns()
    exhaustive_time = end-start

    max_time = max(exhaustive_time, approx_time, bnb_time)

    print("Results for", case_name)
    print("Branch-And-Bound solution: {:8.2f}, time: {:9} us, percent of slowest solution: {:5.1f}".format(bnb_val, int(bnb_time/1_000), bnb_time/max_time*100))
    print("Approximate solution:      {:8.2f}, time: {:9} us, percent of slowest solution: {:5.1f}".format(approx_val, int(approx_time/1_000), approx_time/max_time*100))
    print("Exhaustive solution:       {:8.2f}, time: {:9} us, percent of slowest solution: {:5.1f}".format(exhaustive_val, int(exhaustive_time/1_000), exhaustive_time/max_time*100))
    print()

def run_ts_benchmarks(): 
    test_case_1 = [[0, 12, 29, 22, 13, 24], [12, 0, 19, 3, 25, 6], [29, 19, 0, 21, 23, 28], [22, 3, 21, 0, 4, 5],  [13, 25, 23, 4, 0, 16], [24, 6, 28, 5, 16, 0]]
    test_case_2 = [[0, 24, 77, 91, 31, 88, 45, 37, 59], [24, 0, 72, 82, 6, 44, 88, 13, 68], [77, 72, 0, 91, 98, 9, 24, 13, 62], [91, 82, 91, 0, 42, 64, 41, 12, 23], [31, 6, 98, 42, 0, 5, 38, 67, 7], [88, 44, 9, 64, 5, 0, 10, 93, 52], [45, 88, 24, 41, 38, 10, 0, 38, 95], [37, 13, 13, 12, 67, 93, 38, 0, 17], [59, 68, 62, 23, 7, 52, 95, 17, 0]]
    test_case_3 = [[0, 9, 52, 48, 58, 47, 66, 77, 76, 91, 59, 70], [9, 0, 8, 66, 69, 65, 2, 2, 27, 98, 74, 86], [52, 8, 0, 21, 16, 46, 66, 3, 67, 7, 22, 55], [48, 66, 21, 0, 18, 24, 6, 66, 88, 72, 78, 63], [58, 69, 16, 18, 0, 73, 77, 32, 28, 62, 72, 23], [47, 65, 46, 24, 73, 0, 66, 49, 94, 45, 73, 22], [66, 2, 66, 6, 77, 66, 0, 32, 81, 86, 99, 67], [77, 2, 3, 66, 32, 49, 32, 0, 21, 16, 42, 64], [76, 27, 67, 88, 28, 94, 81, 21, 0, 52, 49, 83], [91, 98, 7, 72, 62, 45, 86, 16, 52, 0, 3, 22], [59, 74, 22, 78, 72, 73, 99, 42, 49, 3, 0, 3], [70, 86, 55, 63, 23, 22, 67, 64, 83, 22, 3, 0]]
    test_case_4 = [[0, 52, 71, 70, 78, 86, 41, 23, 22, 43, 19, 63, 78, 89], [52, 0, 23, 76, 76, 64, 83, 40, 11, 98, 56, 23, 35, 62], [71, 23, 0, 78, 65, 75, 75, 58, 59, 12, 99, 43, 9, 34], [70, 76, 78, 0, 89, 42, 25, 52, 10, 61, 38, 14, 18, 89], [78, 76, 65, 89, 0, 11, 28, 44, 4, 24, 21, 80, 99, 66], [86, 64, 75, 42, 11, 0, 57, 21, 36, 42, 16, 28, 59, 95], [41, 83, 75, 25, 28, 57, 0, 60, 77, 68, 61, 76, 79, 59], [23, 40, 58, 52, 44, 21, 60, 0, 96, 6, 40, 87, 84, 80], [22, 11, 59, 10, 4, 36, 77, 96, 0, 6, 40, 85, 23, 42], [43, 98, 12, 61, 24, 42, 68, 6, 6, 0, 71, 61, 35, 1], [19, 56, 99, 38, 21, 16, 61, 40, 40, 71, 0, 40, 98, 44], [63, 23, 43, 14, 80, 28, 76, 87, 85, 61, 40, 0, 12, 76], [78, 35, 9, 18, 99, 59, 79, 84, 23, 35, 98, 12, 0, 18], [89, 62, 34, 89, 66, 95, 59, 80, 42, 1, 44, 76, 18, 0]]

    benchmark_ts(test_case_1, "Test Case 1, {} items".format(len(test_case_1)))

    benchmark_ts(test_case_2, "Test Case 2, {} items".format(len(test_case_2)))

    benchmark_ts(test_case_3, "Test Case 3, {} items".format(len(test_case_3)))

    benchmark_ts(test_case_4, "Test Case 4, {} items".format(len(test_case_4)))
# endregion [Travelling Salesman]

if __name__ == "__main__":
    run_ts_benchmarks()