



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











def rwrite(outfile, text):
    print(text)
    if outfile:
        outfile.write(text)



if __name__ == "__main__":



    # Step 1: Parse the arguments.

    args = parse_args()



    # Step _: Print the output.

    with open(args.evalfile, "w") as of:

        rwrite(of, "FIGURE LINKING EVALUATION\n")



        # Step _.1: Print out the basic parameters the script was run with.

        rwrite(of, "Script run on %s"%(datetime.datetime.now()))
        rwrite(of, "Ground Truth Filename: %s"%(args.gtfile))
        rwrite(of, "Results Filename:      %s"%(args.resultsfile))
        rwrite(of, "Evaluation Filename:   %s"%(args.evalfile))

