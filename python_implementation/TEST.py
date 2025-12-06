import numpy as np
import copy

def solve_batman_full():
    # --- 1. Input Data ---
    N = 4
    models = [
        {'id': 1, 'P': 20, 'R': 1, 'A': 2, 'C': 5},
        {'id': 2, 'P': 21, 'R': 1, 'A': 3, 'C': 5}
    ]
    M = [
        [0,  1, 1, 50],
        [1,  0, 1,  1],
        [1,  1, 0,  1],
        [50, 1, 1,  0]
    ]

    # --- Helper: Validity Check ---
    def is_valid_schedule(schedule, Ak):
        if sum(schedule) == 0: return False
        doubled = schedule + schedule
        # Min 2 consecutive
        for k in range(1, 13):
            if doubled[k-1]==0 and doubled[k]==1 and doubled[k+1]==0:
                return False
        # Max Autonomy
        current_run = 0
        max_run = 0
        for val in doubled:
            if val == 1: current_run += 1
            else: current_run = 0
            if current_run > max_run: max_run = current_run
        return max_run <= Ak

    # --- Helper: Get Spatial Neighbors ---
    def get_spatial(loc_idx, range_val):
        return [j for j in range(N) if M[loc_idx][j] <= range_val]

    # ==========================================
    # PART 1: GREEDY (Array Based)
    # ==========================================
    def run_greedy():
        uncovered_matrix = [[1 for _ in range(7)] for _ in range(N)]
        is_occupied = [False] * N
        solution = []
        
        def count_rem(mat): return sum(sum(r) for r in mat)

        print(f"--- Greedy Start ---")
        
        while count_rem(uncovered_matrix) > 0:
            best_cand = None
            best_ratio = float('inf')

            for i in range(N):
                if is_occupied[i]: continue
                
                for model in models:
                    spatial = get_spatial(i, model['R'])
                    
                    for sched_int in range(128):
                        bin_str = f"{sched_int:07b}"
                        sched = [int(x) for x in bin_str]
                        
                        if not is_valid_schedule(sched, model['A']): continue
                        
                        cost = model['P'] + (sum(sched) * model['C'])
                        
                        new_cov = 0
                        for c_idx in spatial:
                            for d_idx in range(7):
                                if sched[d_idx] == 1 and uncovered_matrix[c_idx][d_idx] == 1:
                                    new_cov += 1
                        
                        if new_cov > 0:
                            ratio = cost / new_cov
                            if ratio < best_ratio:
                                best_ratio = ratio
                                best_cand = {'loc': i, 'mod': model, 'sched': sched, 'cost': cost, 'sp': spatial}

            if not best_cand:
                print("Greedy stuck!")
                return None
            
            # Commit
            solution.append({
                'Crossing': best_cand['loc'] + 1,
                'Model': best_cand['mod']['id'],
                'Schedule': best_cand['sched'],
                'Cost': best_cand['cost']
            })
            is_occupied[best_cand['loc']] = True
            
            for c_idx in best_cand['sp']:
                for d_idx in range(7):
                    if best_cand['sched'][d_idx] == 1:
                        uncovered_matrix[c_idx][d_idx] = 0
                        
        print(f"Greedy Cost: {sum(c['Cost'] for c in solution)}")
        return solution

    # ==========================================
    # PART 2: LOCAL SEARCH (New Array Implementation)
    # ==========================================
    def run_local_search(initial_solution):
        current_sol = copy.deepcopy(initial_solution)
        improved = True
        
        print(f"\n--- Local Search Start ---")
        
        while improved:
            improved = False
            
            # 1. Build Coverage Count Matrix (The Integer Grid)
            # Rows: Crossings, Cols: Days. Value: How many cams cover this spot.
            count_matrix = [[0 for _ in range(7)] for _ in range(N)]
            
            for cam in current_sol:
                loc = cam['Crossing'] - 1
                model = next(m for m in models if m['id'] == cam['Model'])
                spatial = get_spatial(loc, model['R'])
                
                for c_idx in spatial:
                    for d in range(7):
                        if cam['Schedule'][d] == 1:
                            count_matrix[c_idx][d] += 1

            # -----------------------------
            # MOVE A: Pruning (Drop Redundant)
            # -----------------------------
            cam_to_remove = -1
            for idx, cam in enumerate(current_sol):
                loc = cam['Crossing'] - 1
                model = next(m for m in models if m['id'] == cam['Model'])
                spatial = get_spatial(loc, model['R'])
                
                is_redundant = True
                # Check if every slot covered by this cam has count > 1
                for c_idx in spatial:
                    for d in range(7):
                        if cam['Schedule'][d] == 1:
                            if count_matrix[c_idx][d] <= 1:
                                is_redundant = False
                                break # Not redundant
                    if not is_redundant: break
                
                if is_redundant:
                    cam_to_remove = idx
                    break # Found one, stop searching
            
            if cam_to_remove != -1:
                print(f"LS: Pruned redundant camera at Crossing {current_sol[cam_to_remove]['Crossing']}")
                del current_sol[cam_to_remove]
                improved = True
                continue # Restart loop to rebuild count matrix
            
            # -----------------------------
            # MOVE B: Swap (Replace with Cheaper)
            # -----------------------------
            # We look for a camera that can be replaced by a cheaper one
            # WITHOUT losing coverage on its "Critical Slots" (where count == 1)
            
            best_swap_saving = 0
            best_swap_cand = None # (index_to_replace, new_cam_dict)
            
            for idx, cam in enumerate(current_sol):
                # Identify Critical Slots for this camera
                loc = cam['Crossing'] - 1
                model = next(m for m in models if m['id'] == cam['Model'])
                spatial = get_spatial(loc, model['R'])
                
                critical_slots = [] # List of tuples (c_idx, day)
                for c_idx in spatial:
                    for d in range(7):
                        if cam['Schedule'][d] == 1:
                            if count_matrix[c_idx][d] == 1:
                                critical_slots.append((c_idx, d))
                
                # Try to find a cheaper configuration at the SAME location
                # (You could expand this to other empty locations if you want)
                current_cost = cam['Cost']
                
                for cand_model in models:
                    # Quick check: Does this model even have the range to cover the critical crossings?
                    # The set of crossings in critical_slots must be visible to cand_model
                    cand_spatial = get_spatial(loc, cand_model['R'])
                    
                    # Convert lists to check subset
                    needed_crossings = set(s[0] for s in critical_slots)
                    if not needed_crossings.issubset(set(cand_spatial)):
                        continue # This model is too weak range-wise
                    
                    # Try schedules
                    for sched_int in range(128):
                        bin_str = f"{sched_int:07b}"
                        cand_sched = [int(x) for x in bin_str]
                        
                        if not is_valid_schedule(cand_sched, cand_model['A']): continue
                        
                        cand_cost = cand_model['P'] + (sum(cand_sched) * cand_model['C'])
                        
                        if cand_cost >= current_cost: continue # Not cheaper
                        
                        # Check Coverage of Critical Slots
                        covers_all_critical = True
                        for (req_c, req_d) in critical_slots:
                            # We know req_c is in cand_spatial (checked above)
                            # We just need to check if the day is ON
                            if cand_sched[req_d] == 0:
                                covers_all_critical = False
                                break
                        
                        if covers_all_critical:
                            # We found a valid swap!
                            saving = current_cost - cand_cost
                            if saving > best_swap_saving:
                                best_swap_saving = saving
                                new_cam_entry = {
                                    'Crossing': loc + 1,
                                    'Model': cand_model['id'],
                                    'Schedule': cand_sched,
                                    'Cost': cand_cost
                                }
                                best_swap_cand = (idx, new_cam_entry)

            if best_swap_cand:
                idx_to_swap, new_cam = best_swap_cand
                print(f"LS: Swapped Cam at {new_cam['Crossing']} for cheaper Model {new_cam['Model']}. Saving: {best_swap_saving}")
                current_sol[idx_to_swap] = new_cam
                improved = True
                continue

        print(f"Local Search Final Cost: {sum(c['Cost'] for c in current_sol)}")
        return current_sol

    # --- Execution ---
    greedy_sol = run_greedy()
    final_sol = run_local_search(greedy_sol)
    
    # Visualization
    print("\n--- Final Configuration ---")
    for c in final_sol:
        sched_viz = "".join(["1" if d==1 else "." for d in c['Schedule']])
        print(f"Loc {c['Crossing']} | Mod {c['Model']} | Cost {c['Cost']} | {sched_viz}")

solve_batman_full()