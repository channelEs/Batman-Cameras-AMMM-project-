import numpy as np
import random
from batman_utils import BatmanUtils
from Solvers.LocalSearch import LocalSearch
from problem.instance import Instance
from problem.camera import InputCamera, SolutionCamera
from solver import _Solver

class GRASPSolver(_Solver):
    def __init__(self, instance: Instance, global_utils: BatmanUtils, local_search: LocalSearch):
        if local_search is None:
            raise ValueError('local_search NOT SETTED in config')
        self.instance = instance
        self.local_search = local_search
        self.batman_utils = global_utils

    def constructive_phase(self, alpha):
        uncovered_matrix = [[1 for _ in range(7)] for _ in range(self.instance.num_crossings)]
        is_occupied = [False] * self.instance.num_crossings
        solution = []
        
        while BatmanUtils.get_remaining_count(uncovered_matrix) > 0:
            all_candidates = []
            
            for i in range(self.instance.num_crossings):
                if is_occupied[i]: 
                    continue

                for model in self.instance.cam_models:
                    spatial = self.batman_utils.get_spatial_coverage(i, model.range)
                    
                    for sched_int in range(128):
                        bin_str = f"{sched_int:07b}"
                        sched = [int(x) for x in bin_str]
                        
                        if not self.batman_utils.is_valid_schedule(sched, model.autonomy): 
                            continue
                        
                        new_cov = 0
                        for c_idx in spatial:
                            for d_idx in range(7):
                                if sched[d_idx] == 1 and uncovered_matrix[c_idx][d_idx] == 1:
                                    new_cov += 1
                        
                        if new_cov > 0:
                            cost = model.price + (sum(sched) * model.cost_power)
                            ratio = cost / new_cov
                            
                            cand = {
                                'loc': i, 'model': model, 'sched': sched, 
                                'cost': cost, 'sp': spatial, 'ratio': ratio,
                                'cov': new_cov
                            }
                            all_candidates.append(cand)

            if not all_candidates:
                # !!Infeasible. Impossible to cover all spots
                break

            min_ratio = min(c['ratio'] for c in all_candidates)
            max_ratio = max(c['ratio'] for c in all_candidates)
            
            threshold = min_ratio + alpha * (max_ratio - min_ratio)
            rcl = [c for c in all_candidates if c['ratio'] <= threshold]
            
            selected = random.choice(rcl)
            selected_cam = SolutionCamera(
                i_crossing_number=selected['loc'] + 1,
                i_model_number=selected['model'].id,
                i_schedule=selected['sched'],
                i_total_cost=selected['cost'])
            solution.append(selected_cam)
            is_occupied[selected['loc']] = True
            
            # update uncovered!!
            for c_idx in selected['sp']:
                for d_idx in range(7):
                    if selected['sched'][d_idx] == 1:
                        uncovered_matrix[c_idx][d_idx] = 0
                        
        return solution

    def run_grasp(self, max_iterations=10, alpha=0.3):
        current_best_sol = None
        current_best_cost = 100000
        
        print(f"Starting GRASP (Alpha={alpha}, Iterations={max_iterations})...")
        
        for k in range(max_iterations):
            # for each iteration, try the solution and save the best one
            sol = self.constructive_phase(alpha)
            sol = self.local_search.local_search(initial_solution=sol)
            sol_cost = sum(c.total_cost for c in sol) 
            if current_best_cost > sol_cost:
                current_best_sol = sol
                current_best_cost = sol_cost
                print(f"[GRASP it_{k+1}] NEW BEST SOLUTION! current cost = {sol_cost}")

        return current_best_sol
    
    def solve(self):
        sol = self.run_grasp(max_iterations=50, alpha=0.2)
        # if sol is not None:

        return sol, sum(c.total_cost for c in sol) 