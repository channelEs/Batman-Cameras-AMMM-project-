import os.path

from datParser import DATParser
from problem.instance import Instance
from batman_utils import BatmanUtils
from Solvers.GreedeySolver import GreedySolver
from Solver.LocalSearch import LocalSearch

def prepare_data_set(data_set):
    data_set.P = list(map(int,data_set.P))
    data_set.R = list(map(int,data_set.R))
    data_set.A = list(map(int,data_set.A))
    data_set.C = list(map(int,data_set.C))

    m_lines = []
    for l in data_set.M:
        m_lines.append(list(map(int,l)))
    data_set.M = m_lines
    # print(f'P: {data_set.P[0]} | {len(data_set.P)}')

    cam_models = []
    for i in range(len(data_set.P)):
        # print(f'i {i} leng_pt {len(data_set.P)}')
        model = {
            'id': i + 1,
            'P': data_set.P[i],
            'R': data_set.R[i],
            'A': data_set.A[i],
            'C': data_set.C[i]
        }
        cam_models.append(model)
    return cam_models

if __name__ == "__main__":
    config_file = os.path.join("dat_files","config.dat")
    input_data = DATParser.parse(config_file)
    print(input_data.__dict__)

    data_file = os.path.join("dat_files", input_data.inputFileName)
    data_set = DATParser.parse(data_file)
    print(data_set.__dict__)
    instance = Instance(config=input_data, i_input_data=data_set)

    batman_utils = BatmanUtils(instance=instance)
    
    # cam_models = prepare_data_set(data_set)
    # print(cam_models)
    # print(data_set.__dict__)
    
    solver = None
    local_search = None
    if input_data.local_search:
        local_search = LocalSearch(N=data_set.N, distance_matrix=data_set.M)

    if input_data.solver == "Greedy":
        solver = GreedySolver(global_utils=batman_utils, instance=instance, local_search=local_search)
        
    # if input_data.solver == "GRASP":
    #     solver = GRASPSolver(N=data_set.N, cam_models=cam_models, distance_matrix=data_set.M, local_search=local_search)

    sol, cost = solver.solve()

    for c in sol:
        sched_str = "".join(['✓' if d==1 else '-' for d in c.schedule])
        print(f"Crossing {c.crossing_number} (Model {c.model_number}): {sched_str} | Cost: {c.total_cost}")

    # print("Final Solution:")
    # for s in sol:
    #     print(s)
    print(f"Total Cost: {cost}")