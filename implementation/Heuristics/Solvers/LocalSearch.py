import numpy as np
from batman_utils import BatmanUtils
from solver import _Solver
from problem.instance import Instance
from problem.camera import InputCamera, SolutionCamera

class LocalSearch(_Solver):
    def __init__(self, instance: Instance, global_utils: BatmanUtils):
        self.batman_utils = global_utils
        self.instance = instance

    def local_search(self, initial_solution):
        current_solution: list[SolutionCamera] = initial_solution
        improved = True

        while(improved):
            improved = False
            count_matrix = [[0 for day in range(7)] for corssing in range(self.instance.num_crossings)]

            for sol_camera in initial_solution:
                # print(f'looking into {sol_camera}')
                crossing = sol_camera.crossing_number - 1
                model_cam = next(m for m in self.instance.cam_models if m.id == sol_camera.model_number)
                spatial_covered = self.batman_utils.get_spatial_coverage(crossing, model_cam.range)

                for crossing_i in spatial_covered:
                    for d in range(7):
                        if sol_camera.schedule[d] == 1:
                            count_matrix[crossing_i][d] += 1
            
            # REMOVE ussles cameras
            # if there is a cell in count_matrix with value > 1, we can search if it is possible to remove some camera
            camera_to_remove = -1
            for i, camera in enumerate(current_solution):
                crossing = camera.crossing_number - 1
                model_cam = next(m for m in self.instance.cam_models if m.id == camera.model_number)
                spatial_covered = self.batman_utils.get_spatial_coverage(crossing, model_cam.range)

                is_useless = True
                for crossing_i in spatial_covered:
                    for d in range(7):
                        if camera.schedule[d] == 1:
                            if count_matrix[crossing_i][d] <= 1:
                                is_useless = False
                                break
                    if not is_useless:
                        break
                
                if is_useless:
                    camera_to_remove = i
                    break

            if camera_to_remove != -1:
                print(f'REMOVING camera at crossing {current_solution[camera_to_remove].crossing_number}')
                del current_solution[camera_to_remove]
                improved = True
                continue # re build matrix count
        
            # SWAP cameras
            # look to swap cameras which have lower cost

            best_swap_saving = 0
            best_swap_candidate = None

            for i, camera in enumerate(current_solution):
                crossing = camera.crossing_number - 1
                model_cam = next(m for m in self.instance.cam_models if m.id == camera.model_number)
                spatial_covered = self.batman_utils.get_spatial_coverage(crossing, model_cam.range)

                single_camera_crossings = []
                for crossing_i in spatial_covered:
                    for d in range(7):
                        if camera.schedule[d] == 1:
                            if count_matrix[crossing_i][d] == 1:
                                single_camera_crossings.append((crossing_i, d))

                current_cost = camera.total_cost

                for candidate_model in self.instance.cam_models:
                
                    for possible_schedule in range(128):
                        binary_schedule = f'{possible_schedule:07b}'
                        schedule = [int(digit) for digit in binary_schedule]

                        if not BatmanUtils.is_valid_schedule(schedule, candidate_model.autonomy):
                            continue
                    
                        cost = candidate_model.price + (sum(schedule) * candidate_model.cost_power)

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
                                new_camera_entry = SolutionCamera(
                                    i_crossing_number=crossing_i + 1,
                                    i_model_number=candidate_model.id,
                                    i_schedule=schedule,
                                    i_total_cost=cost)
                                best_swap_candidate = (i, new_camera_entry)

            if best_swap_candidate:
                idx_to_swap, new_cam = best_swap_candidate
                print(f"LS: Swapped Cam at {new_cam.crossing_number} for cheaper Model_Cam {new_cam.model_number}. Saving: {best_swap_saving}")
                
                current_solution[idx_to_swap] = new_cam
                improved = True
                continue

        print(f"Local Search Final Cost: {sum(c.total_cost for c in current_solution)}")
        return current_solution