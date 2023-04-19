import os

class Master:

    def __init__(self, input_location, n_mappers, n_reducers, output_location):
        self.input_location = input_location #ex: input\\wordCount
        self.n_mappers = n_mappers
        self.n_reducers = n_reducers
        self.output_location = output_location

    def input_split(self):
        files = os.listdir(self.input_location)
        print("input files: ", files)
        n_input_files = len(files)
        mapper_to_files_mapping = {}  # dict of the form {mapper_number: [input1.txt]}
        chunk_size = n_input_files // self.n_mappers
        mapper_i = 1
        file_i = 0

        # first assigning chunk size number of files to each mapper
        while(mapper_i <= self.n_mappers):
            end = file_i + chunk_size
            file_list = []
            while(file_i<end):
                file_list.append(files[file_i])
                file_i = file_i + 1
            mapper_to_files_mapping[mapper_i] = file_list
            mapper_i  = mapper_i + 1

        # assignig remaining files (1 to each mapper)
        mapper_i = 1
        while(file_i < n_input_files):
            mapper_to_files_mapping[mapper_i].append(files[file_i])
            file_i = file_i + 1
            mapper_i = mapper_i + 1
        return mapper_to_files_mapping
    

if __name__== "__main__":

    input_location = input("Enter input data location(folder name example: 'input\\wordCount'): ")
    output_location = input("Enter output data location(folder name example: 'output\\wordCount'): ")
    n_mappers = int(input("Enter M (no of mappers): "))
    n_reducers = int(input("Enter R (no of reducers): "))

    master = Master(input_location, n_mappers, n_reducers, output_location)
    mapper_to_files_mapping = master.input_split()
    print(mapper_to_files_mapping)

