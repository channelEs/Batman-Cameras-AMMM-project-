from problem.instance import Instance

class BatmanUtils(object):
    def __init__(self, instance: Instance):
        self.instance = instance

    @staticmethod
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
    
    def get_spatial_coverage(self, crossing_idx, range_val):
        covered = []
        for j in range(self.instance.num_crossings):
            if self.instance.min_range_crossing_matrix[crossing_idx][j] <= range_val:
                covered.append(j)
        return covered

    @staticmethod
    def count_matrix_remaining(mat):
        return sum(sum(r) for r in mat)
    
    @staticmethod
    def get_remaining_count(matrix):
        total = 0
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == 1:
                    total += 1
        return total