import numpy as np

class ParetoOptimizer:

    def __init__(self,vector_list,optimizing_direction):
        self.vector_list = vector_list
        self.optimizing_direction = optimizing_direction
        
    def worse(elem1,elem2,optimizing_vector):
        result = (np.array(elem1) - np.array(elem2)) * np.array(optimizing_vector)
        #print(np.max(result))
     
        if np.max(result) < 0.00000000000001:
            return True
        return False

    def optimal_points(self):
        result_list = []
        for element in self.vector_list:
            #print(element)
            pareto_optimal = True
            for x in self.vector_list:
                if x != element:
                    if ParetoOptimizer.worse(element[:-1],x[:-1],self.optimizing_direction):
                        pareto_optimal = False
                        break
            if pareto_optimal:
                result_list.append(element)
        return result_list




