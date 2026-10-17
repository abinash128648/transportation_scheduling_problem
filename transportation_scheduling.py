import math
from OTTools import TransportationProblem
print("transportation or scheduling (1/2)?")
input_type = input()
if input_type == "1":
    print("Transportation selected.")
    # Add transportation-related code here
    print("Enter the number of Demands:")
    num_demands = int(input())
    print("Enter the number of Supplies:")
    num_supplies = int(input())

    transportation_matrix = []
    for i in range(num_demands):
        transportation_matix_row = []
        for j in range(num_supplies):
            print(f"Enter the cost for demand {i+1} and supply {j+1}:")
            demand_value = float(input())
            transportation_matix_row.append(demand_value)
        transportation_matrix.append(transportation_matix_row)
    print("Transportation matrix:")
    for row in transportation_matrix:
        for value in row:
            print(value, end=" ")
        print()

    print("Enter the demands for each demand point:")
    demands = []
    for i in range(num_demands):
        print(f"Enter demand for demand point {i + 1}:")
        demand = int(input())
        demands.append(demand)
    print("Demands:", demands)
    print("Enter the supplies for each supply point:")
    supplies = []
    for j in range(num_supplies):
        print(f"Enter supply for supply point {j + 1}:")
        supply = int(input())
        supplies.append(supply)
    print("Supplies:", supplies)
    total_demand = sum(demands)
    total_supply = sum(supplies)
    if total_demand != total_supply:
        print("Total demand and total supply are not equal. Please check your inputs.")
        exit()
    print("method for problem solving (1/2/3/4)?")
    print("1. Northwest method")
    print("2. Least cost method")
    print("3. Vogel's approximation method")
    print("4. optimal solution")
    method = input()
    transportation_problem = TransportationProblem(transportation_matrix, demands, supplies)
    if method == "1":
        print("Northwest method selected.")

        NW_solution = transportation_problem.solve(method="NWCR")
        print("Northwest method solution:", NW_solution)

        total_cost = sum(
            transportation_matrix[i][j] * NW_solution[i][j]
            for i in range(num_demands)
            for j in range(num_supplies)
    )
        print("Total transportation cost (Northwest):", total_cost)

    elif method == "2":
        print("Least cost method selected.")

        LC_solution = transportation_problem.solve(method="LCM")
        print("Least cost method solution:", LC_solution)

        total_cost = sum(
            transportation_matrix[i][j] * LC_solution[i][j]
            for i in range(num_demands)
            for j in range(num_supplies)
    )
        print("Total transportation cost (Least Cost):", total_cost)

    elif method == "3":
        print("Vogel's approximation method selected.")

        VG_solution = transportation_problem.solve(method="VAM")
        print("Vogel's approximation method solution:", VG_solution)

        total_cost = sum(
            transportation_matrix[i][j] * VG_solution[i][j]
            for i in range(num_demands)
            for j in range(num_supplies)
        )
        print("Total transportation cost (VAM):", total_cost)

    elif method == "4":
        print("Comparing transportation methods.")

        NW_solution = transportation_problem.solve(method="NWCR")
        LC_solution = transportation_problem.solve(method="LCM")
        VG_solution = transportation_problem.solve(method="VAM")

    # Calculate total cost for each method
        NW_cost = sum(
        transportation_matrix[i][j] * NW_solution[i][j]
        for i in range(num_demands)
        for j in range(num_supplies)
    )

        LC_cost = sum(
        transportation_matrix[i][j] * LC_solution[i][j]
        for i in range(num_demands)
        for j in range(num_supplies)
    )

        VG_cost = sum(
        transportation_matrix[i][j] * VG_solution[i][j]
        for i in range(num_demands)
        for j in range(num_supplies)
    )

        print("Northwest method total cost:", NW_cost)
        print("Least cost method total cost:", LC_cost)
        print("Vogel's approximation method total cost:", VG_cost)

    # Select the solution with the lowest cost
        costs = {
        "Northwest": (NW_cost, NW_solution),
        "Least Cost": (LC_cost, LC_solution),
        "VAM": (VG_cost, VG_solution)
    }

        best_method = min(costs, key=lambda method_name: costs[method_name][0])
        OPT_cost, OPT_solution = costs[best_method]

        print("Lowest-cost method:", best_method)
        print("Lowest transportation cost:", OPT_cost)
        print("Corresponding allocation:", OPT_solution)

elif input_type == "2":
    import numpy as np
    from scipy.optimize import linear_sum_assignment

    print("Scheduling selected.")


    num_jobs = int(input("Enter the number of jobs: "))
    num_machines = int(input("Enter the number of machines: "))

    if num_jobs <= 0 or num_machines <= 0:
        print("Number of jobs and machines must be positive.")
        exit()


    cost_matrix = []

    for i in range(num_jobs):
        row = []
        for j in range(num_machines):
            cost = float(input(
                f"Enter cost for Job {i + 1} on Machine {j + 1}: "
            ))
            row.append(cost)
        cost_matrix.append(row)

    cost_matrix = np.array(cost_matrix, dtype=float)

    print("\nOriginal cost matrix:")
    print(cost_matrix)

    rows, cols = cost_matrix.shape
    size = max(rows, cols)

    padded_matrix = np.zeros((size, size))
    padded_matrix[:rows, :cols] = cost_matrix


    row_minima = padded_matrix.min(axis=1)
    row_reduced = padded_matrix - row_minima[:, np.newaxis]

    print("\nAfter row reduction:")
    print(row_reduced)


    col_minima = row_reduced.min(axis=0)
    reduced_matrix = row_reduced - col_minima[np.newaxis, :]

    print("\nAfter column reduction:")
    print(reduced_matrix)


    assigned_rows, assigned_cols = linear_sum_assignment(
        padded_matrix
    )

    print("\nOptimal assignment:")
    total_cost = 0

    for r, c in zip(assigned_rows, assigned_cols):
        if r < rows and c < cols:
            print(
                f"Job {r + 1} -> Machine {c + 1}, "
                f"Cost = {cost_matrix[r, c]:g}"
            )
            total_cost += cost_matrix[r, c]
        elif r < rows:
            print(f"Job {r + 1} -> Dummy machine (unassigned)")
        elif c < cols:
            print(f"Dummy job -> Machine {c + 1} (unassigned)")

    print("\nMinimum total assignment cost:", total_cost)
