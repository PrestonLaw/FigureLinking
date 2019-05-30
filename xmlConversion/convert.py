

import pdb

import argparse
import configparser
import datetime
import glob

from ann_to_json import read_ann

from html import escape, unescape
import math
from Levenshtein import distance as l_distance

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

# Matching strings isn't going to be exact, what with the weird Unicode characters.
# Detects the index of str2 within str1, ASSUMING that len(str1) > len(str2).
def proximity_index(str1, str2):

    if len(str1) < len(str2):
        return -1

    for i in range(len(str1) - len(str2)):
        substr = str1[i:i+len(str2)]

        d = l_distance(substr, str2)

        if d < 10:
            return i

    return -1



def remake_ann(base):

    # Directories: xml noxml oldann newann

    xmlfile = "./xml/" + base + ".xml"
    txtfile = "./noxml/" + base + ".txt"

    raw_xml = []
    notag_xml = []

    with open(xmlfile, 'r') as XML:

        xmlline = XML.readline()

        while xmlline:
            raw_xml.append(xmlline)
            xmlline = XML.readline()

            # The first > and last < mark the XML tags on this line.

            i2 = xmlline.index(">")
            i3 = xmlline.rindex("<")

            if i3 < i2:
                # There is only one tag on this line.
                notag_line = xmlline[:i3] + xmlline[i2+1:]
                notag_xml.append(unescape(notag_line))

            else:

                i1 = xmlline.index("<")
                i4 = xmlline.rindex(">")

                notag_line = xmlline[:i1] + xmlline[i2+1:i3] + xmlline[i4+1:]
                notag_xml.append(unescape(notag_line))

            xmlline = XML.readline()

    txt = []
    running_length = 0
    line_indexes = []

    with open(txtfile, 'r') as TXT:

        txtline = TXT.readline()

        while txtline:
            txt.append(txtline)

            line_indexes.append(running_length)
            running_length += len(txtline)

            txtline = TXT.readline()

    pdb.set_trace()

    #for i in range(len(txt)):
    #    print(xml[i])
    #    print(txt[i])
    #    pdb.set_trace()

    # Brute force.

    xml_ann = read_ann(_args.inann)
    txt_ann = []

    # Step 1: Go through every annotation,
    for ann in xml_ann:
        # Step 2: Get the text of the old annotation,
        ann_text = ann["text"]

        ann_text = unescape(ann_text)

        if len(ann["range"]) > 1:
            print("WARNING: CONNECTED ANNOTATION - " + ann_text)
            pdb.set_trace()

        # Step 3: Compare it to all lines until we find the new starting point of the annotation.
        # Also, we know the length of the new annotation, so when we find a match, we need to
        # get the text of the new annotation here.
        new_text = ""
        position = -1
        for i in range(len(txt)):
            index = proximity_index(txt[i], ann_text)

            if index != -1:
                # Match found.
                position = line_indexes[i] + index
                new_text = txt[position:position + len(ann_text)]
                break

        if position == -1:
            # If there is no match, make a very visible note of it.
            print("NO MATCH: " + ann_text)
            pdb.set_trace()

        # Assuming a match...
        # Step 4: Construct the new annotation object.
        new_ann = ann
        new_ann["text"] = new_text
        new_ann["range"] = [position, position + len(new_text)]
        txt_ann.append(new_ann)

    # Step 5: Write out the new annotation file.
    with open("./newann/" + base + ".txt.ann", 'w') as outfile:
        for ann in txt_ann:
            outfile.write("%s %s %s %s %s"%(ann["ID"],


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
