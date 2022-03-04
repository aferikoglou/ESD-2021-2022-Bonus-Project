from random import randint
from annotator import Annotator
import copy
from generators import loop_pragma_generator,array_pragma_generator

class RandomExplorer:
    def __init__(self,annot: Annotator) -> None:
        self.exploration_file = copy.deepcopy(annot)

    def get_random(self):
        II_list = range(64)
        unroll_list = [2**i for i in range(5)]
        partition_list = [2**i for i in range(7)]
        modes = ['block','cyclic']


        for loop in self.exploration_file.optimization_points_loops():
            pipeline = bool(randint(0,1))
            unroll = bool(randint(0,1))
            
            ii = II_list[randint(0,len(II_list)-1)]
            unroll_f = unroll_list[randint(0,len(unroll_list)-1)]
            pragma_list = loop_pragma_generator(pipeline,ii,unroll,unroll_f)

            self.exploration_file.pragma_insertion(loop,'loop',pragma_list)

        for array in list(self.exploration_file.optimization_points_arrays()):
            rand_partition = bool(randint(0,1))

            rand_mode = modes[randint(0,len(modes)-1)]
            rand_factor = partition_list[randint(0,len(partition_list)-1)]
            rand_dim = randint(1,1)
            pragma_list = array_pragma_generator(array,rand_partition,rand_mode,rand_factor,rand_dim)

            self.exploration_file.pragma_insertion(array,'array',pragma_list)

    def get_instance(self):
        self.exploration_file.finalize_code()
        self.exploration_file.print_code('final')




