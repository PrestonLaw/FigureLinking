



# Imports

import pdb

import argparse
import configparser
import datetime






# Using the argparse library to read in up to four optional arguments.
# --gtfile: The file containing the groundtruth entities.
# --resultsfile: The file containing the non-groundtruth entities.
# --config: The file containing the configuration parameters.
# --evalfile: The file to which the output will be written.  Default: evaluation.txt
def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--gtfile", help="Path to groundtruth '.xml.ann' file", default="./groundtruth.xml.ann")
    parser.add_argument("--resultsfile", help="Path to non-groundtruth '.xml.ann' file", default="./results.xml.ann")
    parser.add_argument("--config", help="Path to configuration file", default="./config.txt")
    parser.add_argument("--evalfile", help="Path to output file", default="./evaluation.txt")

    args = parser.parse_args()
    return args



# We define this global variable so that we know what EntityTypes there are.
# It will be appended to whenever we come across an Entity with a new EntityType.
EntityTypes = []



# Reading in a BRAT .ann file.
def read_ann(filename, config):

    ann_list = []

    #pdb.set_trace()

    annot_count = 0

    # Opening the file.
    with open(filename, 'r') as f:
        line = f.readline()
        # Parsing every line in the file individually.
        while line:
            tokens = line.split()
            # We know a line is to be ignored if it starts with "#".
            if tokens[0][0] == "#":
                line = f.readline()
                continue

            # Here's the tricky bit. I need to resume reading lines until I stop getting
            # attribute lines.  I then need to use those attributes to load the character
            # range for this particular annotation into a specific dictionary, based on
            # what the Type and Num are.
            if tokens[0][0] == "T":
                # Begin reading in the annotation.
                # First, get the character range.

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

                # This must either be "Reference" or "Caption".
                entitytype = tokens[1]

                # Now that I have the character range, start reading in attribute lines.
                line = f.readline()
                type = ""
                num = 0
                reftype = "Caption"
                while line and line[0] != "T":
                    if line[0] == "#":
                        line = f.readline()
                        continue
                    # Now that I have an attribute line, parse it.
                    tokens = line.split()

                    if tokens[1] == "Num":
                        num = int(tokens[3])
                        #print("Adding character range for figure number %d."%num)
                    elif tokens[1] == "Type":
                        type = tokens[3]
                        #print("Adding character range for figure with type '%s'."%type)
                    elif tokens[1] == "RefType":
                        reftype = tokens[3]

                    line = f.readline()

                # The attributes of the annotationg have been read in.  Store it directly.

                annot_count += 1
                #print("Annotation %d: %s, %s, %d"%(annot_count, reftype, type, num))

                ann_dict = {}
                ann_dict["range"] = char_range
                ann_dict["EntityType"] = entitytype
                ann_dict["RefType"] = reftype
                ann_dict["Type"] = type
                ann_dict["Num"] = num
                ann_dict["Text"] = text

                if config["Allowed REFTYPES"][reftype] != 'true' or config["Allowed TYPES"][type] != 'true':
                    continue

                ann_list.append(ann_dict)

    return ann_list



# Necessary member function.  Cannot hash lists.
def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d



def PR(overlap, gt, ex):
    P = 1.0
    R = 1.0
    if gt != 0:
        R = float(overlap) / gt
    if ex != 0:
        P = float(overlap) / ex
    return (P, R)



def range_within_category(config, ann_list):

    total = 0

    cap_range_total = 0.0
    ref_range_total = 0.0
    cap_count_total = 0
    ref_count_total = 0

    #pdb.set_trace()

    for i in range(len(ann_list)):

        #pdb.set_trace()

        # We should only add the length of an annotation to total_gt or total_ex if it's within category.

        #if ann_list[i]["RefType"] in include_reftype and ann_list[i]["Type"] in include_type:
        if config["Allowed REFTYPES"][ann_list[i]["RefType"]] == "true" and \
           config["Allowed TYPES"][ann_list[i]["Type"]] == "true":
            if ann_list[i]["EntityType"] == "Caption":
                cap_range_total += len(ann_list[i]["range"])
                cap_count_total += 1
            else:
                ref_range_total += len(ann_list[i]["range"])
                ref_count_total += 1

    return (cap_range_total, cap_count_total, ref_range_total, ref_count_total)



# In order to write simultaneously to the terminal and to an output file without duplicating code.
def rwrite(outfile, text):
    print(text)
    if outfile:
        outfile.write(text + "\n")



if __name__ == "__main__":



    # Step 1: Parse the arguments.

    args = parse_args()



    # Step 2: Parse the config file.

    config = configparser.ConfigParser()
    config.optionxform=str
    config.read(args.config)

    pdb.set_trace()



    # Step 3: Parse the grountruth and non-groundtruth files into

# Part 3: Count how many Caption and Reference entities there are in the Groundtruth and NonGroundtruth files.

    entity_statistics = {
        'gt_ref': 0,
        'gt_cap': 0,
        'ex_ref': 0,
        'ex_cap': 0
    }

    for ann in list_gt:
        if ann["EntityType"] == "Caption":
            entity_statistics["gt_cap"] += 1
        else:
            entity_statistics["gt_ref"] += 1
    for ann in list_ex:
        if ann["EntityType"] == "Caption":
            entity_statistics["ex_cap"] += 1
        else:
            entity_statistics["ex_ref"] += 1



    # Part 4: Find both character length count and number of entities within the configuration parameters for
    # the four categories delineated by Caption versus Reference entitytype and Groundtruth versus NonGroundtruth file.

    cap_range_total_gt, cap_count_total_gt, ref_range_total_gt, ref_count_total_gt = range_within_category(config, list_gt)
    cap_range_total_ex, cap_count_total_ex, ref_range_total_ex, ref_count_total_ex = range_within_category(config, list_ex)



    # Part 5: Find all preliminary match pairs, pairs that match without regard to configuration parameters
    # and only by the minimum requirement of having at least one character overlap.

    match_dict = {}

    for i in range(len(list_gt)):

        ann_gt = list_gt[i]

        for j in range(len(list_ex)):

            ann_ex = list_ex[j]

            overlap = len(set(ann_gt["range"]).intersection(set(ann_ex["range"])))

            if overlap > 0:
                #pdb.set_trace()

                f_key = (freeze(ann_gt), freeze(ann_ex))

                match_dict[f_key] = overlap



    # Part 6: Define some variables to be kept track of for the final writing of results.

    match_counts = {
        'Caption': {
            "TP": 0,
            "FN": 0,
            "FP": 0
        },
        'Reference': {
            "TP": 0,
            "FN": 0,
            "FP": 0
        }
    }

    match_overlaps = {
        "Caption": 0.0,
        "Reference": 0.0
    }

    reqs = config["Match Requirements"]

    TP_matches = []

    TP_match_pairs = []
    FP_match_pairs = []
    FN_matches = []



    # Part 7: Iterate over each preliminary match pair.

    for (f_gt, f_ex) in match_dict.keys():

        gt = dict(f_gt)
        ex = dict(f_ex)

        overlap = match_dict[(f_gt, f_ex)]
        threshold = config["Match Requirements"]["Overlap Threshold"]

        len_gt = len(gt["range"])
        len_ex = len(ex["range"])

        if threshold:
            threshold = float(threshold)
        else:
            threshold = 0.0



        # Part 7.1: If a preliminary match pair fails the configuration requirements,
        # it is considered a false positive match.

        if (reqs["ENTITYTYPE Match Required"] == 'true' and gt["EntityType"] != ex["EntityType"]) or \
           (reqs["REFTYPE Match Required"] == 'true' and gt["RefType"] != ex["RefType"]) or \
           (reqs["TYPE Match Required"] == 'true' and gt["Type"] != ex["Type"]) or \
           (reqs["NUM Match Required"] == 'true' and gt["Num"] != ex["Num"]) or \
           len_gt * threshold > overlap or len_ex * threshold > overlap:
            FP_match_pairs.append((f_gt, f_ex))
            if gt["EntityType"] == "Caption":
                match_counts["Caption"]["FP"] += 1
            else:
                match_counts["Reference"]["FP"] += 1
            continue



        # Part 7.2: Otherwise, the preliminary match pair is a true match pair,
        # and is considered a true positive match.

        if gt["EntityType"] == "Caption":
            match_counts["Caption"]["TP"] += 1
            match_overlaps["Caption"] += overlap
        else:
            match_counts["Reference"]["TP"] += 1
            match_overlaps["Reference"] += overlap



        # Part 7.3: We need to keep track of which GT entities are true matched outside of the loop.

        TP_matches.append(f_gt)
        TP_match_pairs.append((f_gt, f_ex))



    # Part 8: Count up the number of falsely unmatched entities within each category, using the variable
    # kept track of in part 7.3.

    #pdb.set_trace()

    for gt in list_gt:
        if freeze(gt) not in TP_matches:
            FN_matches.append(freeze(gt))
            if gt["EntityType"] == "Caption":
                match_counts["Caption"]["FN"] += 1
            else:
                match_counts["Reference"]["FN"] += 1



    # Step _: Print the output.

    with open(args.evalfile, "w") as of:

        rwrite(of, "FIGURE LINKING EVALUATION\n")



        # Step _.1: Print out the basic parameters the script was run with.

        rwrite(of, "Script run on %s"%(datetime.datetime.now()))
        rwrite(of, "Ground Truth Filename: %s"%(args.gtfile))
        rwrite(of, "Results Filename:      %s"%(args.resultsfile))
        rwrite(of, "Evaluation Filename:   %s\n"%(args.evalfile))



        # Step _.2: Print out the parameters given via the config file.

        rwrite(of, "-"*50)
        rwrite(of, "CONFIGURATION PARAMETERS\n")

        rwrite(of, "Span Overlap Threshold: %d
        rwrite(of, "Span Overlap Threshold: %s"%config["Match Requirements"]["Overlap Threshold"])
        rwrite(of, "REFTYPE Categories Tested:")
        for key in config["Allowed REFTYPES"].keys():
            rwrite(of, "    %s - %s"%(key, config["Allowed REFTYPES"][key]))
        rwrite(of, "TYPE Categories Tested:")
        for key in config["Allowed TYPES"].keys():
            rwrite(of, "    %s - %s"%(key, config["Allowed TYPES"][key]))
        rwrite(of, "ENTITYTYPE Match Required: %s"%config["Match Requirements"]["ENTITYTYPE Match Required"])
        rwrite(of, "REFTYPE Match Required:    %s"%config["Match Requirements"]["REFTYPE Match Required"])
        rwrite(of, "TYPE Match Required:       %s"%config["Match Requirements"]["TYPE Match Required"])
        rwrite(of, "NUM Match Required:        %s\n"%config["Match Requirements"]["NUM Match Required"])



        # Part 9.3: The number of Caption and Reference entities in each of the GT and non-GT files.

        rwrite(of, "ENTITY STATISTICS")
        rwrite(of, "Ground Truth")
        rwrite(of, "    # of 'Caption':   %d"%(entity_statistics['gt_cap']))
        rwrite(of, "    # of 'Reference': %d"%(entity_statistics['gt_ref']))
        rwrite(of, "Results")
        rwrite(of, "    # of 'Caption':   %d"%(entity_statistics['ex_cap']))
        rwrite(of, "    # of 'Reference': %d\n"%(entity_statistics['ex_ref']))



        # Part 9.4: The number of true positive, false positive, and false negative matches on the GT entities.

        rwrite(of, "EVALUATION RESULTS")
        rwrite(of, "Match Counts")
        rwrite(of, "    Overall (all ENTITYTYPES):")
        rwrite(of, "        # of Correct Matches:        %d"%(match_counts["Caption"]["TP"] + match_counts["Reference"]["TP"]))
        rwrite(of, "        # of False Negative Matches: %d"%(match_counts["Caption"]["FN"] + match_counts["Reference"]["FN"]))
        rwrite(of, "        # of False Positive Matches: %d"%(match_counts["Caption"]["FP"] + match_counts["Reference"]["FP"]))
        rwrite(of, "    'Caption' ENTITYTYPE Only:")
        rwrite(of, "        # of Correct Matches:        %d"%(match_counts["Caption"]["TP"]))
        rwrite(of, "        # of False Negative Matches: %d"%(match_counts["Caption"]["FN"]))
        rwrite(of, "        # of False Positive Matches: %d"%(match_counts["Caption"]["FP"]))
        rwrite(of, "    'Reference' ENTITYTYPE Only:")
        rwrite(of, "        # of Correct Matches:        %d"%(match_counts["Reference"]["TP"]))
        rwrite(of, "        # of False Negative Matches: %d"%(match_counts["Reference"]["FN"]))
        rwrite(of, "        # of False Positive Matches: %d"%(match_counts["Reference"]["FP"]))



        # Part 9.5a: The precision and recall on the match accuracy, as determined by the absolute count of true matches.
        # Part 9.5b: The precision and recall on the match accuracy, as determined by the number of overlapping characters
        #            summed up over all true matches.

        # Part 9.5.1: Over all entity types.

        rwrite(of, "Match Metrics")
        rwrite(of, "    Overall (all ENTITYTYPES):")
        rwrite(of, "        Overlap (computed on overlap between text spans):")
        P,R = PR(match_overlaps["Caption"] + match_overlaps["Reference"],
                 cap_range_total_gt + ref_range_total_gt,
                 cap_range_total_ex + ref_range_total_ex)
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))
        rwrite(of, "        Count (computed on # of correct/incorrect matches):")
        P,R = PR(match_counts["Caption"]["TP"] + match_counts["Reference"]["TP"],
                 cap_count_total_gt + ref_count_total_gt,
                 cap_count_total_ex + ref_count_total_ex)
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))



        # Part 9.5.2: Individually over the Caption and Reference entity types.
        # Note: Precision is defined as the proportion of non-GT entities that have GT entities matching them.
        #       Recall is defined as the proportion of GT entities that have non-GT entities matching them.

        rwrite(of, "    'Caption' ENTITYTYPE Only:")
        rwrite(of, "        Overlap (computed on overlap between text spans):")
        P,R = PR(match_overlaps["Caption"], cap_range_total_gt, cap_range_total_ex)
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))
        rwrite(of, "        Count (computed on # of correct/incorrect matches):")
        P,R = PR(match_counts["Caption"]["TP"], cap_count_total_gt, cap_count_total_ex)
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))

        rwrite(of, "    'Reference' ENTITYTYPE Only:")
        rwrite(of, "        Overlap (computed on overlap between text spans):")
        P,R = PR(match_overlaps["Reference"], ref_range_total_gt, ref_range_total_ex)
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))
        rwrite(of, "        Count (computed on # of correct/incorrect matches):")
        P,R = PR(match_counts["Reference"]["TP"], ref_count_total_gt, ref_count_total_ex)
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))



        # Part 9.5.3: Print out all true matches.
        rwrite(of, "")
        rwrite(of, "Match Contents")
        rwrite(of, "CORRECT MATCHES")
        count = 0
        for (f_gt, f_ex) in TP_match_pairs:

            gt = dict(f_gt)
            ex = dict(f_ex)

            overlap = match_dict[(f_gt, f_ex)]
            threshold = config["Match Requirements"]["Overlap Threshold"]

            len_gt = len(gt["range"])
            len_ex = len(ex["range"])

            count += 1

            rwrite(of, "Match %d:"%(count))
            rwrite(of, "    ENTITYTYPES: %s, %s"%(gt["EntityType"], ex["EntityType"]))
            rwrite(of, "    REFTYPES: %s, %s"%(gt["RefType"], ex["RefType"]))
            rwrite(of, "    TYPES: %s, %s"%(gt["Type"], ex["Type"]))
            rwrite(of, "    NUMS: %d, %d"%(gt["Num"], ex["Num"]))
            rwrite(of, "    Text of GT / non-GT entities:")
            rwrite(of, "%s"%(gt["Text"]))
            rwrite(of, "%s\n"%(ex["Text"]))

        rwrite(of, "FALSE POSITIVE MATCHES")
        count = 0
        for (f_gt, f_ex) in FP_match_pairs:

            gt = dict(f_gt)
            ex = dict(f_ex)

            overlap = match_dict[(f_gt, f_ex)]
            threshold = config["Match Requirements"]["Overlap Threshold"]

            len_gt = len(gt["range"])
            len_ex = len(ex["range"])

            count += 1

            rwrite(of, "Match %d:"%(count))
            rwrite(of, "    ENTITYTYPES: %s, %s"%(gt["EntityType"], ex["EntityType"]))
            rwrite(of, "    REFTYPES: %s, %s"%(gt["RefType"], ex["RefType"]))
            rwrite(of, "    TYPES: %s, %s"%(gt["Type"], ex["Type"]))
            rwrite(of, "    NUMS: %d, %d"%(gt["Num"], ex["Num"]))
            rwrite(of, "    Text of GT / non-GT entities:")
            rwrite(of, "%s"%(gt["Text"]))
            rwrite(of, "%s\n"%(ex["Text"]))

