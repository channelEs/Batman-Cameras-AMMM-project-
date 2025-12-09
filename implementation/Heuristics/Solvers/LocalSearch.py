import numpy as np
from batman_utils import BatmanUtils
from solver import _Solver

class LocalSearch(_Solver):
    def __init__(self, instance: Instance, global_utils: BatmanUtils):
        self.batman_utils = global_utils
        self.instance = instance

    def local_search(self, initial_solution, cam_models):
        current_solution = initial_solution
        improved = True

        while(improved):
            improved = False
            count_matrix = [[0 for day in range(7)] for corssing in range(self.N)]

            for camera in current_solution:
                crossing = camera['Crossing'] - 1
                model_cam = next(m for m in cam_models if m['id'] == camera['Model_Cam'])
                spatial_covered = BatmanUtils.get_spatial_coverage(self.N, self.M, crossing, model_cam['R'])

                for crossing_i in spatial_covered:
                    for d in range(7):
                        if camera['Schedule'][d] == 1:
                            count_matrix[crossing_i][d] += 1
            
            # REMOVE ussles cameras
            # if there is a cell in count_matrix with value > 1, we can search if it is possible to remove some camera
            camera_to_remove = -1
            for i, camera in enumerate(current_solution):
                crossing = camera['Crossing'] - 1
                model_cam = next(m for m in cam_models if m['id'] == camera['Model_Cam'])
                spatial_covered = BatmanUtils.get_spatial_coverage(self.N, self.M, crossing, model_cam['R'])

                is_useless = True
                for crossing_i in spatial_covered:
                    for d in range(7):
                        if camera['Schedule'][d] == 1:
                            if count_matrix[crossing_i][d] <= 1:
                                is_useless = False
                                break
                    if not is_useless:
                        break
                
                if is_useless:
                    camera_to_remove = i
                    break

            if camera_to_remove != -1:
                print(f'REMOVING camera at crossing {current_solution[camera_to_remove]["Crossing"]}')
                del current_solution[camera_to_remove]
                improved = True
                continue # re build matrix count
        
            # SWAP cameras
            # look to swap cameras which have lower cost

            best_swap_saving = 0
            best_swap_candidate = None

            for i, camera in enumerate(current_solution):
                crossing = camera['Crossing'] - 1
                model_cam = next(m for m in cam_models if m['id'] == camera['Model_Cam'])
                spatial_covered = BatmanUtils.get_spatial_coverage(self.N, self.M, crossing, model_cam['R'])

                single_camera_crossings = []
                for crossing_i in spatial_covered:
                    for d in range(7):
                        if camera['Schedule'][d] == 1:
                            if count_matrix[crossing_i][d] == 1:
                                single_camera_crossings.append((crossing_i, d))

                current_cost = camera['Cost']

                for candidate_model in cam_models:
                
                    for possible_schedule in range(128):
                        binary_schedule = f'{possible_schedule:07b}'
                        schedule = [int(digit) for digit in binary_schedule]

                        if not BatmanUtils.is_valid_schedule(schedule, candidate_model['A']):
                            continue
                    
                        cost = candidate_model['P'] + (sum(schedule) * candidate_model['C'])

                        if cost >= current_cost:
                            continue

                        cover_single_camera_crossings = True
                        for (crossing, day) in single_camera_crossings:
                            if schedule[day] == 0:
                                cover_single_camera_crossings = False
                                break

                        if cover_single_camera_crossings:
                            saving = current_cost - cost
                            if saving > best_swap_saving:
                                best_swap_saving = saving
                                new_camera_entry = {
                                    'Crossing': crossing_i + 1,
                                    'Model_Cam': candidate_model['id'],
                                    'Schedule': schedule,
                                    'Cost': cost
                                }
                                best_swap_candidate = (i, new_camera_entry)

            if best_swap_candidate:
                idx_to_swap, new_cam = best_swap_candidate
                print(f"LS: Swapped Cam at {new_cam['Crossing']} for cheaper Model_Cam {new_cam['Model_Cam']}. Saving: {best_swap_saving}")
                current_solution[idx_to_swap] = new_cam
                improved = True
                continue

        print(f"Local Search Final Cost: {sum(c['Cost'] for c in current_solution)}")
        return current_solution