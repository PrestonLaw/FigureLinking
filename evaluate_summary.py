

import glob
import argparse
import os
import pdb
import datetime

from evaluate import evaluate, PR, rwrite

#from types import SimpleNamespace



class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]



def parse_args():

    parser = argparse.ArgumentParser()

    #parser.add_argument("--gtpath", help="Path to groundtruth '.xml.ann' file", default="./groundtruth.xml.ann")
    #parser.add_argument("--respath", help="Path to non-groundtruth '.xml.ann' file", default="./results.xml.ann")
    parser.add_argument("--anndir", help="Path to annotation file folder", default="./test_ann/")
    parser.add_argument("--config", help="Path to configuration file", default="./config.txt")
    parser.add_argument("--evaldir", help="Path to output file folder", default="./output/")

    _args = parser.parse_args()
    return _args





if __name__ == "__main__":

    _args = parse_args()

    filepairs = []

    for file in glob.glob(_args.anndir + "*.xml.ann"):
        tokens = file.split("/")

        filename = tokens[-1]

        if filename[0:2] == "gt":
            id = filename[2:-8]
        elif filename[0:3] == "res":
            id = filename[3:-8]

        if id not in filepairs:
            filepairs.append(id)

    #pdb.set_trace()

    # Recording all the output variables for each evaluation.  Intensive, but I don't see a better solution.

    _EntityTypes = set([])
    _entity_statistics = []
    _match_counts = []
    _match_overlaps = []
    _gt_ranges = []
    _gt_counts = []
    _ex_ranges = []
    _ex_counts = []

    for id in filepairs:

        sub_args = {"gtfile": _args.anndir + "gt" + id + ".xml.ann",
                    "resfile": _args.anndir + "res" + id + ".xml.ann",
                    "config": _args.config,
                    "evalfile": _args.evaldir + "test" + id + ".txt"
        }

        [EntityTypes,
         entity_statistics,
         match_counts,
         match_overlaps,
         gt_ranges,
         gt_counts,
         ex_ranges,
         ex_counts] = evaluate(Map(sub_args))

        _EntityTypes = _EntityTypes.union(set(EntityTypes))
        _entity_statistics.append(entity_statistics)
        _match_counts.append(match_counts)
        _match_overlaps.append(match_overlaps)
        _gt_ranges.append(gt_ranges)
        _gt_counts.append(gt_counts)
        _ex_ranges.append(ex_ranges)
        _ex_counts.append(ex_counts)

        print("\n"*5)



    # Redefining the variables to combine all of them into one.

    EntityTypes = _EntityTypes


    entity_statistics = {
        ET: {'gt': 0, 'ex': 0}
        for ET in EntityTypes
    }

    for es in _entity_statistics:
        for ET in es.keys():
            entity_statistics[ET]['gt'] += es[ET]['gt']
            entity_statistics[ET]['ex'] += es[ET]['ex']


    match_counts = {
        ET: {
            "TM": 0,
            "FM": 0,
            "FE": 0,
            "ME": 0
        } for ET in EntityTypes
    }

    for mc in _match_counts:
        for ET in mc.keys():
            match_counts[ET]["TM"] += mc[ET]["TM"]
            match_counts[ET]["FM"] += mc[ET]["FM"]
            match_counts[ET]["FE"] += mc[ET]["FE"]
            match_counts[ET]["ME"] += mc[ET]["ME"]


    match_overlaps = {
        ET: 0.0 for ET in EntityTypes
    }

    for mo in _match_overlaps:
        for ET in mo.keys():
            match_overlaps[ET] += mo[ET]


    gt_ranges = {ET: 0.0 for ET in EntityTypes}
    for r in _gt_ranges:
        for ET in r.keys():
            gt_ranges[ET] += r[ET]


    ex_ranges = {ET: 0.0 for ET in EntityTypes}
    for r in _ex_ranges:
        for ET in r.keys():
            ex_ranges[ET] += r[ET]


    gt_counts = {ET: 0 for ET in EntityTypes}
    for r in _gt_counts:
        for ET in r.keys():
            gt_counts[ET] += r[ET]


    ex_counts = {ET: 0 for ET in EntityTypes}
    for r in _ex_counts:
        for ET in r.keys():
            ex_counts[ET] += r[ET]



    # Now that we have unified variables, we can perform the exact same sort of output as we do for individual files.

    with open("./summary.txt", "w") as of:

        rwrite(of, "FIGURE LINKING EVALUATION SUMMARY\n")



        # Step 9.1: Print out the basic parameters the script was run with.

        rwrite(of, "Script run on %s"%(datetime.datetime.now()))



        # Part 9.3: The number of Caption and Reference entities in each of the GT and non-GT files.

        rwrite(of, "-"*50)
        rwrite(of, "ENTITY STATISTICS\n")
        rwrite(of, "Ground Truth")
        for ET in EntityTypes:
            rwrite(of, "    # of '%s': %d"%(ET, entity_statistics[ET]["gt"]))

        rwrite(of, "Results")
        for ET in EntityTypes:
             rwrite(of, "    # of '%s': %d"%(ET, entity_statistics[ET]["ex"]))

        rwrite(of, "\n" + "-" * 50)



        # Part 9.4: The number of true positive, false positive, and false negative matches on the GT entities.

        rwrite(of, "EVALUATION RESULTS\n")
        rwrite(of, "Match Counts")
        rwrite(of, "    Overall (all ENTITYTYPES):")
        rwrite(of, "        # of True Matches:    %d"%(sum([match_counts[ET]["TM"] for ET in EntityTypes])))
        rwrite(of, "        # of False Matches:   %d"%(sum([match_counts[ET]["FM"] for ET in EntityTypes])))
        rwrite(of, "        # of False Entities:  %d"%(sum([match_counts[ET]["FE"] for ET in EntityTypes])))
        rwrite(of, "        # of Missed Entities: %d"%(sum([match_counts[ET]["ME"] for ET in EntityTypes])))
        for ET in EntityTypes:
            rwrite(of, "    '%s' ENTITYTYPE Only:"%(ET))
            rwrite(of, "        # of True Matches:    %d"%(match_counts[ET]["TM"]))
            rwrite(of, "        # of False Matches:   %d"%(match_counts[ET]["FM"]))
            rwrite(of, "        # of False Entities:  %d"%(match_counts[ET]["FE"]))
            rwrite(of, "        # of Missed Entities: %d"%(match_counts[ET]["ME"]))



        # Part 9.5a: The precision and recall on the match accuracy, as determined by the absolute count of true matches.
        # Part 9.5b: The precision and recall on the match accuracy, as determined by the number of overlapping characters
        #            summed up over all true matches.

        # Part 9.5.1: Over all entity types.

        #pdb.set_trace()

        rwrite(of, "Match Metrics")
        rwrite(of, "    Overall (all ENTITYTYPES):")
        rwrite(of, "        Overlap (computed on overlap between text spans):")
        P,R = PR(sum(match_overlaps.values()), sum(gt_ranges.values()), sum(ex_ranges.values()))
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))
        rwrite(of, "        Count (computed on # of correct/incorrect matches):")
        P,R = PR(sum([match_counts[ET]["TM"] for ET in EntityTypes]), sum(gt_counts.values()), sum(ex_counts.values()))
        rwrite(of, "            Precision = %f, Recall = %f"%(P,R))



        # Part 9.5.2: Individually over the Caption and Reference entity types.
        # Note: Precision is defined as the proportion of non-GT entities that have GT entities matching them.
        #       Recall is defined as the proportion of GT entities that have non-GT entities matching them.

        for ET in EntityTypes:
            rwrite(of, "    '%s' ENTITYTYPE Only:"%(ET))
            rwrite(of, "        Overlap (computed on overlap between next spans):")
            P,R = PR(match_overlaps[ET], gt_ranges[ET], ex_ranges[ET])
            rwrite(of, "            Precision = %f, Recall = %f"%(P,R))
            rwrite(of, "        Count (computed on # of correct/incorrect matches):")
            P,R = PR(match_counts[ET]["TM"], gt_counts[ET], ex_counts[ET])
            rwrite(of, "            Precision = %f, Recall = %f"%(P,R))












