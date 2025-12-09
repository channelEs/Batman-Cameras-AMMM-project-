

class InputCamera():
    def __init__(self):
        self.range = 0
        self.autonomy = 0
        self.cost_power = 0
        self.price = 0

    def init_camera_from_input_config(self, input_data_camera, index):
        self.id = index
        self.price = input_data_camera.P[index] 
        self.range = input_data_camera.R[index] 
        self.autonomy = input_data_camera.A[index] 
        self.cost_power = input_data_camera.C[index] 
        
class SolutionCamera():
    def __init__(self, i_crossing_number = 0, i_model_number = 0, i_total_cost = 0, i_schedule = []):
        self.crossing_number = i_crossing_number
        self.model_number = i_model_number
        self.total_cost = i_total_cost
        self.schedule: list = i_schedule
    