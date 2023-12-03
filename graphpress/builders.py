import csv
import os
import math
import gzip


def mergeDictionary(dict_1, dict_2):
    """
    Merges two dictionaries
    dict1   {0: [2,4], 1: [5]}
    dict2   {0: [3], 2: [5]}
    ret     {0: [2,4,3], 1: [5], 2: [5]}
    """
    dict_3 = {**dict_1, **dict_2}
    for key, value in dict_3.items():
        if key in dict_1 and key in dict_2:
            dict_3[key] = value + dict_1[key]
    return dict_3

def format_line (line):
    """
    Converts from correct format [num, {}] to line for .gz file
    line    [0, {0: [2,3,4], 1: [5]}]
    ret     "0 0.2.3.4 1.5\n".encode()
    """
    id_line_local = line[0]
    answer = [str(id_line_local)]
    for edge in line[1].keys():
        nums_string = list(map (lambda x: str(x), line[1][edge]))
        nums_join = '.'.join([str(edge)] + nums_string)
        answer.append(nums_join)
    last = ' '.join(answer) + '\n'
    return last.encode()

def line_convert (line):
    """
    Converts a text line to correct format [num, {}]
    line    "0 0.2.3.4 1.5"
    ret     [0, {0: [2,3,4], 1: [5]}]
    """
    line_to = []
    if line != '':
        line_to = line.split(' ')
        id_line = int(line_to[0])
        rs = {}
        for val in line_to[1:]:
            val_split = list(map(lambda x: int(x),val.split('.')))
            rs[val_split[0]] = val_split[1:]
        line_to = [id_line,rs]
    return line_to

def structToText(key, value):
	"""
	Converts a structure {1 : [2,3]} to a list that will be written after
	key		1
	value	[2,3]
	ret		[1, '2.3']
	"""
	groups = list(map(lambda x: '.'.join( list(map(lambda y: str(y),x)) ),value))
	return [key] + groups

class Builder():

    def __init__(self, reader, parser, partition_folder, output_file, max_lines_readed_per_file=10000):
        self.reader = reader
        self.parser = parser
        self.partition_folder = partition_folder
        self.output_file = output_file
        self.max_lines_readed_per_file = max_lines_readed_per_file
        

    def make_partitions(self, debug=False):
        rel = {}
        act_readed_lines = 0
        act_part = 0
        line_counter = 0

        for line in self.reader.readline():
            subj, pred, obj = self.parser.parse_line(line)
            if subj in rel:
                done = False

                for relation in rel[subj]:
                    if relation[0] == pred:
                        relation.append(obj)
                        done = True
                        break
                if not done:
                    rel[subj].append([pred,obj])
            else:
                rel[subj] = [[pred,obj]]

            # If node obj is in rel
            if obj in rel:
                done = False

                for relation in rel[obj]:
                    if relation[0] == pred * -1:
                        relation.append(subj)
                        done = True
                        break

                if not done:
                    rel[obj].append([pred * -1,subj])

            else:
                rel[obj] = [[pred * -1,subj]]

            act_readed_lines += 1
            line_counter += 1

            # If max lines readed, write file
            if act_readed_lines > self.max_lines_readed_per_file:
                file_open = open(f"{self.partition_folder}/part_{act_part}.csv",'w',newline='')
                file_writer = writer = csv.writer(file_open,delimiter=' ', quotechar='|')

                for data in sorted(rel.keys()):
                    result = structToText(data,rel[data])
                    file_writer.writerow(result)
                
                # Restart variables
                file_open.close()
                rel = {}
                act_readed_lines = 0
                act_part += 1

        # If some lines left, write last file
        if act_readed_lines > 0:
            file_open = open(f"{self.partition_folder}/part_{act_part}.csv",'w',newline='')
            file_writer = writer = csv.writer(file_open,delimiter=' ', quotechar='|')

            for data in sorted(rel.keys()):
                result = structToText(data,rel[data])
                file_writer.writerow(result)

            file_open.close()
            rel = {}
            act_part += 1

        if debug: print(f"Readed lines: {line_counter}")


    def merge_partitions(self):
        
        comp_file = gzip.open(self.output_file,"wb")

        parts = os.listdir(self.partition_folder)
        files = []
        for filename in parts:
            files.append(open(f'{self.partition_folder}/{filename}',"r"))

        lines = []
        for x in files:
            line_to = x.readline().replace('\n','')
            line_f = line_convert(line_to)
            lines.append(line_f)

        act_line = []           # Line that will be written
        last_id = math.inf      # Lower id of the lines
        write_line = False      # Has to write the line

        while True:

            # Checks loaded lines
            i = 0
            done_files = True           # End condition
            for i in range(len(lines)):
                if lines[i] != []:
                    done_files = False
                    continue
                line_to = files[i].readline().replace('\n','')
                line_f = line_convert(line_to)
                lines[i] = line_f


            # All files are done
            if done_files:
                # Write file
                line_write = format_line(act_line)
                comp_file.write(line_write)
                #new_node += 1
                
                # Ends
                #print("\n")
                #print(f"Total nodes: {new_node}")
                #print(f"Max ID: {act_line[0]}")
                #print("\n")
                return

        
            index = 0           # Index of the line
            write_line = True   # Has to write actual line

            # Candidate values
            local_last_id = math.inf
            local_index = 0
            local_act_line = []


            # Merge
            while index < len(lines):
                
                # Load a line if it is empty
                if lines[index] == []:
                    line_to = files[index].readline().replace('\n','')
                    lines[index] = line_convert(line_to)
                
                # If stills empty, continue
                if lines[index] == []:
                    index += 1
                    continue
                
                # Get values
                line_id = lines[index][0]
                line_con = lines[index][1]

                # If same id, merge
                if line_id == last_id:
                    act_line[1] = mergeDictionary(line_con, act_line[1])
                    line_to = files[index].readline().replace('\n','')
                    lines[index] = line_convert(line_to)
                    write_line = False
                    break
                
                # Check if is the new candidate
                elif line_id < local_last_id:
                    local_last_id = line_id
                    local_act_line = lines[index]
                    local_index = index

                index += 1

            # Write line
            if write_line:
                if act_line != []:
                    line_write = format_line(act_line)
                    comp_file.write(line_write)
                    #new_node += 1
                act_line = local_act_line
                last_id = local_last_id
                line_to = files[local_index].readline().replace('\n','')
                lines[local_index] = line_convert(line_to)
            















