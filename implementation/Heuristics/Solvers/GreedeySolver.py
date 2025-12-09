import numpy as np
from Solvers.LocalSearch import LocalSearch
from batman_utils import BatmanUtils
from solver import _Solver
from problem.instance import Instance
from problem.camera import InputCamera, SolutionCamera

class GreedySolver(_Solver):
    def __init__(self, instance: Instance, global_utils: BatmanUtils, local_search: LocalSearch = None):
        self.batman_utils = global_utils
        self.instance = instance
        self.local_search = local_search

    def greedy_solver(self):
        uncovered_matrix = [[1 for day in range(7)] for crossing in range(self.instance.num_crossings)]
        # for i in range(self.N):
        #     for d in range(self.MAX_DAYS):
        #         uncovered.add((i, d))

        solution_cameras = []
        is_crossing_occupied = [False] * self.instance.num_crossings
        
        while self.batman_utils.get_remaining_count(uncovered_matrix) > 0:
            
            best_candidate = None
            best_ratio = float('inf')

            # iterate all possible locations
            for i in range(self.instance.num_crossings):
                if is_crossing_occupied[i]:
                    continue

                # iterate all cam_models
                for cam_model in self.instance.cam_models:
                    spatial_neighbors = self.batman_utils.get_spatial_coverage(i, cam_model.range)
                    # for j in range(self.N):
                    #     if self.M[i][j] <= cam_model['R']:
                    #         spatial_neighbors.append(j)

                    for possible_schedule in range(128): # 2^7 possible schedules

                        binary_schedule = f'{possible_schedule:07b}'
                        schedule = [int(digit) for digit in binary_schedule]

                        if not self.batman_utils.is_valid_schedule(schedule, cam_model.autonomy):
                            continue
                    
                        cost = cam_model.price + (sum(schedule) * cam_model.cost_power)

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

            best_cam = SolutionCamera(
                i_crossing_number=best_candidate['crossing'] + 1,
                i_model_number=best_candidate['cam_model'].id,
                i_schedule=best_candidate['schedule'],
                i_total_cost=best_candidate['cost'])

            solution_cameras.append(best_cam)
            # solution_cameras.append({
            #     'Crossing': , 
            #     'Model_Cam': ,
            #     'Cost': ,
            #     'Schedule': 
            # })

            is_crossing_occupied[best_candidate['crossing']] = True

            c_schedule = best_candidate['schedule']
            for covered_c in best_candidate['spatial']:
                for d in range(7):
                    if c_schedule[d] == 1:
                        uncovered_matrix[covered_c][d] = 0

            print(f"Selected: Crossing {best_candidate['crossing'] + 1}, Camera Model {best_candidate['cam_model'].id}, ")

        # total_cost = sum(c['Cost'] for c in solution_cameras)
        return solution_cameras #, total_cost
    
    def solve(self):
        sol = self.greedy_solver()
        if self.local_search is not None:
            sol = self.local_search.local_search(initial_solution=sol, cam_models=self.cam_models)
        return sol, sum(c.total_cost for c in sol)