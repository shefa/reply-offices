class TabuSearch:
	def __init__(
			self,
            rng,
            neighbourhood_function,
            cost_function,
            branching_factor,
            tabu_list_size,
            num_non_improve,
            better_solution_function):
		self.rng = rng
        self.neighbourhood_function = neighbourhood_function
        self.cost_function = cost_function
        self.branching_factor = branching_factor
        self.tabu_list_size = tabu_list_size
        self.num_non_improve = num_non_improve
        self.better_solution_function = better_solution_function


	def run(self, initial_solution):
        iterations_since_last_improvement = 0

        current_solution = initial_solution.copy()
        current_solution_cost = self.cost_function(initial_solution)

        best_solution = current_solution.copy()
        best_solution_cost = current_solution_cost

        tabuList = set()

        while iterations_since_last_improvement < self.num_non_improve:

        	best_neighbour = current_solution.copy()
        	best_neighbour_cost = current_solution_cost

        	for _ in range(self.branching_factor):
	        	neighbour = self.neighbourhood_function(current_solution)
	        	if neighbour in tabuList:
	        		continue

	            neighbour_solution_cost = self.cost_function(neighbour)

	            if neighbour_solution_cost > best_neighbour_cost:
	            	best_neighbour_cost = neighbour_solution_cost
	            	best_neighbour = neighbour

	        delta_cost = best_neighbour_cost - current_solution_cost
	        tabuList.add(neighbour)

	        if delta_cost >= 0:
	         	current_solution = best_neighbour
	          	current_solution_cost = best_neighbour_cost

		        if current_solution_cost > best_solution_cost:
	                self.better_solution_function(current_solution_cost,current_solution)
	                best_solution = current_solution[:]
	                best_solution_cost = current_solution_cost
	                iterations_since_last_improvement = 0
	            else:
	                iterations_since_last_improvement += 1