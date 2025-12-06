import numpy as np
from LocalSearch import LocalSearch
from batman_utils import BatmanUtils

class GreedySolver:
    def __init__(self, num_crossings, cam_models, distance_matrix, local_search: LocalSearch = None):
        self.N = num_crossings
        self.cam_models = cam_models
        self.M = np.array(distance_matrix)
        self.local_search = local_search

    def greedy_solver(self):
        uncovered_matrix = [[1 for day in range(7)] for crossing in range(self.N)]
        # for i in range(self.N):
        #     for d in range(self.MAX_DAYS):
        #         uncovered.add((i, d))

        solution_cameras = []
        is_crossing_occupied = [False] * self.N
        
        while BatmanUtils.get_remaining_count(uncovered_matrix) > 0:
            
            best_candidate = None
            best_ratio = float('inf')

            # iterate all possible locations
            for i in range(self.N):
                if is_crossing_occupied[i]:
                    continue

                # iterate all cam_models
                for cam_model in self.cam_models:
                    spatial_neighbors = BatmanUtils.get_spatial_coverage(self.N, self.M, i, cam_model['R'])
                    # for j in range(self.N):
                    #     if self.M[i][j] <= cam_model['R']:
                    #         spatial_neighbors.append(j)

                    for possible_schedule in range(128): # 2^7 possible schedules

                        binary_schedule = f'{possible_schedule:07b}'
                        schedule = [int(digit) for digit in binary_schedule]

                        if not BatmanUtils.is_valid_schedule(schedule, cam_model['A']):
                            continue
                    
                        cost = cam_model['P'] + (sum(schedule) * cam_model['C'])

                        new_covered_count = 0
                        for c_idx in spatial_neighbors:
                            for d_idx in range(7):
                                if schedule[d_idx] == 1 and uncovered_matrix[c_idx][d_idx] == 1:
                                    new_covered_count += 1
                        
                        if new_covered_count > 0:
                            ratio = cost / new_covered_count
                            if ratio < best_ratio:
                                best_ratio = ratio
                                best_candidate = {
                                    'crossing': i,
                                    'cam_model': cam_model,
                                    'schedule': schedule,
                                    'cost': cost,
                                    'covered_count': new_covered_count,
                                    'spatial': spatial_neighbors
                                }
            
            if best_candidate is None:
                print("Stopping: No valid candidate found to cover remaining slots.")
                break

            solution_cameras.append({
                'Crossing': best_candidate['crossing'] + 1, 
                'Model_Cam': best_candidate['cam_model']['id'],
                'Cost': best_candidate['cost'],
                'Schedule': best_candidate['schedule']
            })

            is_crossing_occupied[best_candidate['crossing']] = True

            c_schedule = best_candidate['schedule']
            for covered_c in best_candidate['spatial']:
                for d in range(7):
                    if c_schedule[d] == 1:
                        uncovered_matrix[covered_c][d] = 0

            print(f"Selected: Crossing {best_candidate['crossing'] + 1}, Camera Model {best_candidate['cam_model']['id']}, ")

        # total_cost = sum(c['Cost'] for c in solution_cameras)
        return solution_cameras #, total_cost
    
    def solve(self):
        sol = self.greedy_solver()
        if self.local_search is not None:
            sol = self.local_search.local_search(initial_solution=sol, cam_models=self.cam_models)
        return sol, sum(c['Cost'] for c in sol)