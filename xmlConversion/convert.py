

import pdb

import argparse
import configparser
import datetime
import glob

from ann_to_json import read_ann

import pdb



"""
def parse_args():

    parser = argparse.ArgumentParser()

    #parser.add_argument("--inann", help="Old annotation file for XML file", default="./groundtruth.xml.ann")
    #parser.add_argument("--outann", help="Path to output corrected annotation file", default="./results.xml.ann")
    #parser.add_argument("--xmlfile", help="Path to old data file with XML tags", default="./config.txt")
    #parser.add_argument("--txtfile", help="Path to new data file without XML tags", default="./evaluation.txt")

    parser.add_argument"--base", help="String ID of the file set")

    _args = parser.parse_args()
    return _args
"""


def remake_ann(base):

    # Directories: xml noxml oldann newann

    xmlfile = "./xml/" + base + ".xml"
    txtfile = "./noxml/" + base + ".txt"

    xml = []

    with open(xmlfile, 'r') as XML:

        xmlline = XML.readline()

        while xmlline:
            xml.append(xmlline)
            xmlline = XML.readline()

    txt = []

    with open(txtfile, 'r') as TXT:

        txtline = TXT.readline()

        while txtline:
            txt.append(txtline)
            txtline = TXT.readline()

    running_chars_deleted = 0

    pdb.set_trace()

    for i in range(len(txt)):
        print(xml[i])
        print(txt[i])

        pdb.set_trace()

    # Brute force.

    xml_ann = read_ann(_args.inann)

    # The concept is to go through every annotation, get the text,
    # find the approximate starting location of the text, then execute a search for the text.

    for ann in xml_ann:
        text = ann["text"]



if __name__ == "__main__":

    #_args = parse_args()

    #base = _args.base

    files = glob.glob("./xml/*.xml")

    for file in files:
        base = file[-12:-4]

        remake_ann(base)

    # Part 1: Read in the XML and TXT files and compute a mapping between them.
    # Originally, I wanted an array of booleans, true if the character at that index was removed, and false otherwise.
    # Each line has had characters from the beginning of the line removed up to the first '>'.
    # Each line has had characters from the end of the line removed since the last '<'.
    # But, if index of last '<' is less than index of first '>', I mark it as no characters from end of line.
    # So, I store an array of tuples.
    # Each tuple corresponds to a line.
    # The first element of a tuple is how many characters were removed from the beginning of the line.
    # The second element is how many characters were removed from the end of the line.


    """
    chars_stayed = []

    xml = []

    with open(_args.xmlfile, 'r') as XML:
        # and open(args.txtfile, 'r') as TXT:

        xmlline = XML.readline()
        #txtline = TXT.readline()

        while xmlline:
            # and txtline:

            xml.append(xmlline)

            idx1 = xmlline.index('>')
            idx2 = xmlline.rindex('<')

            if idx2 <= idx1:
                # The only thing on this line is an xml tag.  Or a blank line.  Remove the entire line.

                for index in range(xmlline):
                    chars_stayed.append(False)

            else:
                # Remove the XML tags only.
                # Substring out everything else besides the text.
                tag1 = xmlline[:idx1]
                tag2 = xmlline[idx2:]



            xmlline = XML.readline()



    txt = []

    # Step 2: Load in the text file.
    with open(args.txtfile, 'r') as TXT:

        txtline = TXT.readline()

        while txtline:
            txt.append(txtline)
            txtline = TXT.readline()


    # Now, text searching.

    # First step is to read the .xml.ann file.
    # TODO: Use the .ann file reading function.

    xml_ann = read_ann(_args.inann)

    # The concept is to go through every annotation, get the text,
    # find the approximate starting location of the text, then execute a search for the text.

    for ann in xml_ann:
        text = ann["text"]

    """
