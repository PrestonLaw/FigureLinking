

import pdb

import argparse
import configparser
import datetime
import json





def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--annfile", help="Path to '.xml.ann' file", default="./groundtruth.xml.ann")
    parser.add_argument("--outfile", help="Path to output json file", default="./results.xml.ann")
    #parser.add_argument("--config", help="Path to configuration file", default="./config.txt")
    #parser.add_argument("--evalfile", help="Path to output file", default="./evaluation.txt")

    _args = parser.parse_args()
    return _args



# We define this global variable so that we know what EntityTypes there are.
# It will be appended to whenever we come across an Entity with a new EntityType.
EntityTypes = ["Caption", "Reference"]

# We should also define the configuration parameters as a global variable as well.
args = None
#config = None



# Reading in a BRAT .ann file.
def read_ann(filename):

    #ann_list = []

    ann_dict = {}

    conn_map = {}

    #pdb.set_trace()

    annot_count = 0

    # Opening the file.
    with open(filename, 'r') as f:
        line = f.readline()
        # Parsing every line in the file individually.
        while line:
            tokens = line.split()
            # We know a line is to be ignored if it starts with "#".
            #if tokens[0][0] == "#":
            #    line = f.readline()
            #    continue

            # Here's the tricky bit. I need to resume reading lines until I stop getting
            # attribute lines.  I then need to use those attributes to load the character
            # range for this particular annotation into a specific dictionary, based on
            # what the Type and Num are.
            if tokens[0][0] == "T":
                # Read in the annotation.

                # Step 1: Get the character range.
                char_range = []
                start_ann = int(tokens[2])
                index = 3
                while ";" in tokens[index]:
                    i = tokens[index].split(";")
                    ann_list += range(start_ann, int(i[0]))
                    start_ann = int(i[1])
                    index += 1
                char_range += range(start_ann, int(tokens[index]))

                # The rest of the tokens make up the text covered by the entity.
                text = " ".join(tokens[index+1:])

                # Step 2: Handle the EntityType.  This can be "Reference" or "Caption" or something else.
                entitytype = tokens[1]

                # Maintaining the list of EntityTypes.
                if entitytype not in EntityTypes:
                    EntityTypes.append(entitytype)
                    # New EntityTypes are included by default, and must be explicitly disallowed in the config file.
                    #config["Allowed ENTITYTYPES"][entitytype] = "true"

                # Step 3: Using the ID of the entity as a key in a dictionary to enable future attribute modification.
                id = tokens[0]

                ann_dict[id] = {
                    "ID": id,
                    "EntityType": entitytype,
                    "RefType": None,
                    "Type": None,
                    "Num": None,
                    "range": char_range
                }

            # Each line that begins with "A" is an attribute that needs to be set.
            if tokens[0][0] == "A":

                # The ID of the entity the attribute belongs to.
                e_id = tokens[2]
                # The attribute name we're overwriting.  Can be "RefType", "Type", or "Num".
                a_type = tokens[1]
                # The value of the attribute we're overwriting.
                a_val = tokens[3]

                # Special case: If We're overwriting a Num attribute, the value needs to be an integer.
                if a_type == "Num":
                    a_val = int(a_val)

                # Overwriting the attribute field.
                ann_dict[e_id][a_type] = a_val

            # Lines that begin with "R" are relations / continuations.
            if tokens[0][0] == "R":

                fromID = tokens[2][5:]
                toID = tokens[3][5:]

                conn_map[toID] = fromID

                while fromID in conn_map.keys():
                    fromID = conn_map[fromID]

                #fromEntity = ann_dict[fromID]
                #toEntity = ann_dict[toID]

                # Append the ranges together.
                ann_dict[fromID]["range"] += ann_dict[toID]["range"]

                # Since we are treating this as a single annotation, delete the 'to' entity.
                del ann_dict[toID]



            # Reading in the new line to continue the loop.
            line = f.readline()

    ann_dict["Connected"] = conn_map

    return ann_dict

    # Now that the dictionary of annotations is complete, we check each one against the configuration file.
    # We only want to include those with appropriate EntityTypes, RefTypes, and Types.

    #pdb.set_trace()

    #for key in ann_dict.keys():
    #    ann = ann_dict[key]
        #if config["Allowed ENTITYTYPES"][ann["EntityType"]] != "true" or \
        #   (ann["RefType"] is not None and config["Allowed REFTYPES"][ann["RefType"]] != "true") or \
        #   (ann["Type"] is not None and config["Allowed TYPES"][ann["Type"]] != "true"):
        #    continue

        # If it does not violate the configuration parameters, append it to the list of returned entities.
    #    ann_list.append(ann)

    #return ann_list






if __name__ == "__main__":



    # Part 1: Parse the arguments.

    _args = parse_args()



    ann_dict = read_ann(_args.annfile)

    with open(_args.outfile, 'w') as of:
        json.dump(ann_dict, of)
