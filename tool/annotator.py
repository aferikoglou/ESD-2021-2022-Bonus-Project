import re
import token 


class Annotator:
    
    def __init__(self,FOR=True,PARTITION=True) -> None:
        self.FOR = FOR
        self.PARTITION = PARTITION
        self.loop_counter = 0
        self.array_counter = 0
        self.optimization_dictionary_loops = {}
        self.optimized_code = []
        self.datatype_capture = []
        self.optimization_dictionary_arrays = {}

    def read_code(self,code):
        self.code = code.readlines()

    def print_code(self,print_file='annotated'):
        if print_file == 'final':
            for line in self.optimized_code:
                print(line,end='')
        else:
            for line in self.code:
                print(line,end='')
        print()

    def capture_datatypes(self,type_list):
        self.datatype_capture = type_list

    def annotate_loops(self):
        for i in range(len(self.code)):
            tokens = self.code[i].split()
            for t in tokens:
                if t[:4] == 'for(' or t ==  'for':
                    self.code[i] = f"LOOP_{self.loop_counter}: {self.code[i]}"
                    self.code.insert(i+1,f'@@@LOOP_{self.loop_counter}\n')
                    self.optimization_dictionary_loops[f"LOOP_{self.loop_counter}"] = []
                    self.loop_counter += 1
                    break

    def optimization_points_loops(self):
        return self.optimization_dictionary_loops

    def optimization_points_arrays(self):
        return self.optimization_dictionary_arrays

    
    def annotate_arrays(self):
        for i in range(len(self.code)):
            tokens = self.code[i].split()
            if len(tokens) > 0 and tokens[0] in self.datatype_capture:
                arrays = re.split(r'[;,\s+]',self.code[i])
                for item in arrays:
                    if len(item) > 0 and item not in self.datatype_capture:
                        item_name = item.split('[')[0]
                        self.optimization_dictionary_arrays[f'{item_name}'] = {'dims': item.count('['), 'optimizations':[]}
                        self.code.insert(i+1,f'@@@ARRAY_{item_name}\n')
                    


    def pragma_insertion(self,tag,type,pragma_list):
        if type == 'loop':
            self.optimization_dictionary_loops[tag] = pragma_list
        elif type == 'array':
            self.optimization_dictionary_arrays[tag]['optimizations'] = pragma_list

    def finalize_code(self):
        self.optimized_code = list(self.code)
        
        for key in self.optimization_dictionary_loops:
            pragma_location = self.optimized_code.index(f"@@@{key}\n")
            for pragma in self.optimization_dictionary_loops[key]:
                self.optimized_code.insert(pragma_location+1,f"{pragma}\n")

        for key in self.optimization_dictionary_arrays:
            pragma_location = self.optimized_code.index(f"@@@ARRAY_{key}\n")
            print(key)
            op_list = self.optimization_dictionary_arrays[key]
            print(op_list)
            for pragma in op_list['optimizations']:
                self.optimized_code.insert(pragma_location+1,f"{pragma}\n")

        temp = []
        for line in self.optimized_code:
            if line[:3] != '@@@':
                temp.append(line)
        self.optimized_code = temp

            



            

            

        


        
            
