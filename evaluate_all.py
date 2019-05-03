

import glob
import argparse
import os
import pdb

from evaluate import evaluate

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

    for id in filepairs:

        sub_args = {"gtfile": _args.anndir + "gt" + id + ".xml.ann",
                    "resfile": _args.anndir + "res" + id + ".xml.ann",
                    "config": _args.config,
                    "evalfile": _args.evaldir + "test" + id + ".txt"
        }

        evaluate(Map(sub_args))

        print("\n"*5)
