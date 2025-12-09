from problem.solution import Solution
from problem.camera import InputCamera

class Instance(object):
    def __init__(self, config, i_input_data):
        print('READING INPUT')
        self.config = config
        self.inputData = i_input_data
        self.num_crossings = i_input_data.N
        m_lines = []
        for value in i_input_data.M:
            m_lines.append(list(map(int,value)))
        self.min_range_crossing_matrix = m_lines

        print(f'M: {self.min_range_crossing_matrix}')

        i_input_data.P = list(map(int,i_input_data.P))
        i_input_data.R = list(map(int,i_input_data.R))
        i_input_data.A = list(map(int,i_input_data.A))
        i_input_data.C = list(map(int,i_input_data.C))

        self.cam_models = []
        for i in range(len(i_input_data.P)):
            # print(f'i {i} leng_pt {len(i_input_data.P)}')
            cam = InputCamera()
            cam.init_camera_from_input_config(input_data_camera=i_input_data, index=i)
            self.cam_models.append(cam)
            # model = {
            #     'id': i + 1,
            #     'P': i_input_data.P[i],
            #     'R': i_input_data.R[i],
            #     'A': i_input_data.A[i],
            #     'C': i_input_data.C[i]
            # }
            # self.cam_models.append(model)

        print(f'CAM_MODELS: {self.cam_models}')

    # def getSizeCode(self):
    #     # Returns length of each code (m parameter)
    #     return self.sizeCode

    # def getnumCodes(self):
    #     # Returns the number of codes in S
    #     return self.numCodes

    # def getNode(self, index):
    #     # Returns the code of S[index]
    #     return self.sequence[index]

    # def getDistances(self):
    #     # Returns the distance matrix of S
    #     return self.distances

    # def getSequence(self):
    #     # Returns matrix S of the input instance
    #     return self.sequence

    # def createSolution(self):
    #     solution = Solution(self.sequence, self.distances)
    #     solution.setVerbose(self.config.verbose)
    #     solution.add_starter_node(self.getNode(0))
    #     return solution

    def checkInstance(self):
        return True
