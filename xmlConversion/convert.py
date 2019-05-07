

import pdb

import argparse
import configparser
import datetime








def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--inann", help="Old annotation file for XML file", default="./groundtruth.xml.ann")
    parser.add_argument("--outann", help="Path to output corrected annotation file", default="./results.xml.ann")
    parser.add_argument("--xmlfile", help="Path to old data file with XML tags", default="./config.txt")
    parser.add_argument("--txtfile", help="Path to new data file without XML tags", default="./evaluation.txt")

    _args = parser.parse_args()
    return _args




if __name__ == "__main__":

    _args = parse_args()

    # Part 1: Read in the XML and TXT files and compute a mapping between them.
    # Originally, I wanted an array of booleans, true if the character at that index was removed, and false otherwise.
    # Each line has had characters from the beginning of the line removed up to the first '>'.
    # Each line has had characters from the end of the line removed since the last '<'.
    # But, if index of last '<' is less than index of first '>', I mark it as no characters from end of line.
    # So, I store an array of tuples.
    # Each tuple corresponds to a line.
    # The first element of a tuple is how many characters were removed from the beginning of the line.
    # The second element is how many characters were removed from the end of the line.


    map = []

    with open(_args.xmlfile, 'r') as XML and open(args.txtfile, 'r') as TXT:

        xmlline = XML.readline()
        txtline = TXT.readline()

        while xmlline and txtline:

            idx1 = xmlline.index('>')
            idx2 = xmlline.rindex('<')
