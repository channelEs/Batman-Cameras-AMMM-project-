import os.path
import csv
import os
import time
from datParser import DATParser
from problem.instance import Instance
from batman_utils import BatmanUtils
from Solvers.GreedeySolver import GreedySolver
from Solvers.LocalSearch import LocalSearch
from Solvers.GRASPSolver import GRASPSolver

def save_execution_to_csv(in_filename:str, out_filename, N, K, time, solver, solution, total_cost, alpha=None):
    fieldnames = ['in_filename', 'N', 'K', 'total_cost', 'time', 'solver', 'num_cameras', 'alpha', 'Configuration_Details']
    file_exists = os.path.isfile(out_filename)
    config_details = []
    for c in solution:
        loc = c.crossing_number
        mod = c.model_number
        sched = "".join(['1' if d==1 else '0' for d in c.schedule])
            
        config_details.append(f"Loc{loc}:M{mod}:S[{sched}]")
    
    config_str = " | ".join(config_details)
    with open(out_filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'in_filename': in_filename.split('/')[-1],
            'N': N,
            'K': K,
            'total_cost': total_cost,
            'time': time,
            'solver': solver,
            'num_cameras': len(solution),
            'alpha': 'NO_a' if alpha is None else alpha,
            'Configuration_Details': config_str
        })
        
    print(f"-> Result saved to {out_filename}")

if __name__ == "__main__":
    config_file = os.path.join("config","config.dat")
    input_data = DATParser.parse(config_file)
    print(input_data.__dict__)

    print(f'EXECUTING instance filename: {input_data.inputFileName}')
    data_file = os.path.join(input_data.inputFileName)
    data_set = DATParser.parse(data_file)
    print(data_set.__dict__)
    instance = Instance(config=input_data, i_input_data=data_set)

    batman_utils = BatmanUtils(instance=instance)
    
    solver = None
    local_search = None
    start = time.time() 
    if input_data.local_search:
        local_search = LocalSearch(global_utils=batman_utils, instance=instance)

    if input_data.solver == "Greedy":
        solver = GreedySolver(global_utils=batman_utils, instance=instance, local_search=local_search)
        
    if input_data.solver == "GRASP":
        solver = GRASPSolver(global_utils=batman_utils, instance=instance, local_search=local_search, alpha=input_data.alpha)

    sol, cost = solver.solve()

    output_file = os.path.join("solutions",input_data.inputFileName)
    end = time.time()
    save_execution_to_csv(in_filename=data_file, out_filename=input_data.solutionFile,N=instance.num_crossings, K=len(instance.cam_models), time=end-start, solver=input_data.solver, solution=sol, total_cost=cost, alpha=input_data.alpha)

    for c in sol:
        sched_str = "".join(['✓' if d==1 else '-' for d in c.schedule])
        print(f"Crossing {c.crossing_number} (Model {c.model_number}): {sched_str} | Cost: {c.total_cost}")

    # print("Final Solution:")
    # for s in sol:
    #     print(s)
    print(f"Total Cost: {cost}")