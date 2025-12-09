import time
from logger import Logger
from problem.instance import Instance
from batman_utils import BatmanUtils


class _Solver(object):
    def __init__(self, config, instance: Instance, i_global_utils: BatmanUtils):
        self.batman_utils = i_global_utils
        self.config = config
        self.instance = instance
        logFields = [
            {'id': 'elapTime', 'name': 'Elap. Time (s)', 'headerformat': '{:>14s}', 'valueformat': '{:>14.20f}'},
            {'id': 'objValue', 'name': 'Obj. Value', 'headerformat': '{:>10s}', 'valueformat': '{:>10.8f}'},
            {'id': 'iterations', 'name': 'Iterations', 'headerformat': '{:>12s}', 'valueformat': '{:>12d}'}
        ]
        self.logger = Logger(fields=logFields)
        if instance is not None and self.config.verbose:
            self.logger.printHeaders()
        self.startTime = 0
        self.elapsedEvalTime = 0
        self.numSolutionsConstructed = 0

    def startTimeMeasure(self):
        self.startTime = time.time()

    def writeLogLine(self, objValue, iterations):
        if not self.config.verbose: return
        logValues = {'elapTime': time.time() - self.startTime, 'objValue': objValue, 'iterations': iterations}
        self.logger.printValues(logValues)

    def solve(self):
        raise NotImplementedError('Abstract method cannot be called')

    def printPerformance(self):
        if not self.config.verbose: return
        avg_evalTimePerCandidate = 0.0
        if self.numSolutionsConstructed != 0:
            avg_evalTimePerCandidate = 1000.0 * self.elapsedEvalTime / float(self.numSolutionsConstructed)

        print('Evaluation Performance:')
        print('  Num. solutions constructed', self.numSolutionsConstructed)
        print('  Total Eval. Time     ', self.elapsedEvalTime, 's')
        print('  Avg. Time / solution', avg_evalTimePerCandidate, 'ms')
