from solution import _Solution

class Solution(_Solution):
    def __init__(self, i_camera_models = []):
        self.camera_models = i_camera_models
        self.fitness = 0
        self.feasible = True
        #es defineix com la llista dels nodes(codis) qu el nostre TSP(que es el que es a la practica) ha visitat size = k-1
        #en aquest no posem el primer 0
        self.used_code = {}
        #es defineix om la sequencia actual que s'esta provant size = k
        #en aquest posem el primer 0
        self.actual_sequence = {}
        # list equal to actual_secuence but with nodes_id instead of nodes
        self.actual_id_sequence = []
        # list with the distances of the greedy solution
        self.sum_of_codes = []
        self.total_sum = 0
        super().__init__()

    def isFeasible(self):
        return self.feasible

    def makeInfeasible(self):
        self.feasible = False
        self.fitness = float('inf')

    def getFitness(self):
        return self.fitness


    def findFeasibleAssignment(self, node_id):
        feasibleAssignments = []
        for d_id, dist in enumerate(self.distances[node_id]):
            if d_id not in self.actual_sequence:
                if d_id != node_id:
                    feasibleAssignments.append(tuple((dist, d_id)))
            else:
                continue
        return feasibleAssignments

    #afegim un node visitat a les llistes
    def add_node(self, dist, node_id):
        if node_id not in self.used_code:
            self.used_code[node_id] = []
            self.used_code[node_id].append(self.sequence[node_id])
            self.actual_sequence[node_id] = []
            self.actual_sequence[node_id].append(self.sequence[node_id])
            self.actual_id_sequence.append(node_id)
            self.sum_of_codes.append(dist)
            self.total_sum += dist
            return True
        return False

    def remove_node(self, dist, node_id):
        if node_id in self.used_code and dist != 0:
            self.used_code.pop(node_id)
            self.actual_sequence.pop(node_id)
            self.actual_id_sequence.remove(node_id)
            self.sum_of_codes.remove(dist)
            self.total_sum -= dist
            return True
        return False

    def add_starter_node(self, node):
        self.actual_sequence[0] = []
        self.actual_sequence[0].append(node)
        self.actual_id_sequence.append(0)
        return True

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write('OBJECTIVE: ' + str(self.total_sum) + '\n')
        for i, node in enumerate(self.actual_id_sequence):
            if i == 0:
                continue
            else:
                f.write(str(self.actual_id_sequence[i-1]) + ' --> ' + str(node) + '\n')
        f.close()


