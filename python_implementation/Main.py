import os.path

from datParser import DATParser
from GreedeySolver import GreedySolver
from LocalSearch import LocalSearch
from GRASPSolver import GRASPSolver

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
    
    solver = None
    data_file = os.path.join("dat_files", input_data.inputFileName)
    data_set = DATParser.parse(data_file)
    print(data_set.__dict__)
    
    cam_models = prepare_data_set(data_set)
    print(cam_models)
    print(data_set.__dict__)
    
    local_search = None
    if input_data.local_search:
        local_search = LocalSearch(N=data_set.N, distance_matrix=data_set.M)

    if input_data.solver == "Greedy":
        solver = GreedySolver(num_crossings=data_set.N, cam_models=cam_models, distance_matrix=data_set.M, local_search=local_search)
        
    if input_data.solver == "GRASP":
        solver = GRASPSolver(N=data_set.N, cam_models=cam_models, distance_matrix=data_set.M, local_search=local_search)

    sol, cost = solver.solve()

    for c in sol:
        sched_str = "".join(['✓' if d==1 else '-' for d in c['Schedule']])
        print(f"Crossing {c['Crossing']} (Model {c['Model_Cam']}): {sched_str} | Cost: {c['Cost']}")

    # print("Final Solution:")
    # for s in sol:
    #     print(s)
    print(f"Total Cost: {cost}")