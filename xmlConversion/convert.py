

import pdb

import argparse
import configparser
import datetime
import glob

from ann_to_json import read_ann

from html import escape, unescape
import math
#from Levenshtein import distance as l_distance
import string
import os.path
from os import path
import re

import pdb



# Note: This will not work on all ann files in the future, and in fact, currently has two crash conditions.

printable = set(string.printable)

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def edit_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]



# Matching strings isn't going to be exact, what with the weird Unicode characters.
# Detects the index of str2 within str1, ASSUMING that len(str1) > len(str2).
# If there is no exact match, this function returns the smallest distance.
def proximity_index_and_match(str1, str2):

    #if len(str1) < len(str2):
    #    return -1

    min_dist = 100
    min_index = -1

    for i in range(len(str1) - len(str2)):
        substr = str1[i:i+len(str2)]

        d = edit_distance(substr, str2)

        if d < min_dist:
            min_dist = d
            min_index = i

        if d == 0:
            return (i, 0)

    return (min_index, min_dist)



def remake_ann(base):

    # Directories: xml noxml oldann newann

    #xmlfile = "./xml/" + base + ".xml"
    txtfile = "./noxml/" + base + ".txt"

    #raw_xml = []

    #pdb.set_trace()

    #txt = []
    txt = ""
    running_length = 0
    line_indexes = []

    print("\nReading file %s..."%txtfile)

    with open(txtfile, 'r') as TXT:

        txtline = TXT.readline()

        while txtline:
            #txt.append(txtline)
            txt += txtline

            line_indexes.append(running_length)
            running_length += len(txtline)

            txtline = TXT.readline()

    #pdb.set_trace()

    #for i in range(len(txt)):
    #    print(xml[i])
    #    print(txt[i])
    #    pdb.set_trace()

    # Brute force.

    #unfound_anns = []

    ann_file = "./oldann/" + base + ".xml.ann"
    print("Reading file %s...\n"%ann_file)
    xml_ann, continuations = read_ann(ann_file)
    txt_ann = []

    # Step 1: Go through every annotation.
    for key in xml_ann:
        # Step 2: Get the text of the old annotation.
        ann = xml_ann[key]
        ann_text = ann["text"]

        ann_text = unescape(ann_text)

        ann_text = cleanhtml(ann_text)

        ann_text = ''.join(i for i in ann_text if ord(i)<128)

        #if len(ann["range"]) > 1:
        #    print("WARNING: CONNECTED ANNOTATION - " + ann_text)
        #    #unfound_anns.append(ann_text)
        #    #continue
        #    pdb.set_trace()
        #    continue

        print("Searching for text: %s"%ann_text)

        index, dist = proximity_index_and_match(txt, ann_text)

        if dist > 1:
            print("Closest match text: %s"%txt[index:index + len(ann_text)])

        # Assuming a match...
        # Step 4: Construct the new annotation object.
        new_ann = ann
        new_ann["text"] = txt[index:index + len(ann_text)]
        new_ann["range"] = [index, index + len(ann_text)]
        #pdb.set_trace()
        txt_ann.append(new_ann)

        """

        # Step 3: Compare it to all lines until we find the new starting point of the annotation.
        # Also, we know the length of the new annotation, so when we find a match, we need to
        # get the text of the new annotation here.
        best_dist = 100
        best_index = 0
        best_line = 0
        # Iterate over every line in the txt file.
        for i in range(len(txt)):
            # index is the character index within txt[i].
            # Find the closest match to ann_text within txt[i].
            index, dist = proximity_index_and_match(txt[i], ann_text)

            if dist < best_dist:
                best_dist = dist
                best_index = index
                best_line = i

            if dist == 0:
                # Exact match found.
                break

        if best_dist > 1:
            # If there is no match, make a very visible note of it.
            print("NO EXACT MATCH: " + ann_text)
            #unfound_anns.append(ann_text)
            #continue
            #pdb.set_trace()

        # Assuming a match...
        # Step 4: Construct the new annotation object.
        new_ann = ann
        new_ann["text"] = txt[best_line][index:index + len(ann_text)]
        position = line_indexes[best_line] + index
        new_ann["range"] = [position, position + len(ann_text)]
        #pdb.set_trace()
        txt_ann.append(new_ann)
        """

    # Step 5: Write out the new annotation file.
    inc_id = 1
    txt_ann_file = "./newann/" + base + ".txt.ann"
    print("Writing file %s..."%txt_ann_file)

    with open(txt_ann_file, 'w+') as outfile:
        for ann in txt_ann:
            #pdb.set_trace()
            outfile.write("%s %s %d %d %s\n"%(ann["ID"], ann["EntityType"], ann["range"][0], ann["range"][1], ann["text"]))
            if "RefType" in ann.keys() and ann["RefType"] is not None:
                outfile.write("A%d RefType %s %s\n"%(inc_id, ann["ID"], ann["RefType"]))
                inc_id += 1
            outfile.write("A%d Type %s %s\n"%(inc_id, ann["ID"], ann["Type"]))
            inc_id += 1
            if ann["Num"] is None:
                ann["Num"] = 0
            outfile.write("A%d Num %s %d\n"%(inc_id, ann["ID"], ann["Num"]))
            inc_id += 1
        outfile.write(continuations)

    #return unfound_anns


if __name__ == "__main__":

    #_args = parse_args()

    #base = _args.base

    files = glob.glob("./xml/*.xml")

    #unfound_anns = {}

    for file in files:
        base = file[-12:-4]

        if path.exists("./newann/" + base + ".txt.ann"):
            continue

        #pdb.set_trace()

        #unfound_anns[base] = remake_ann(base)
        remake_ann(base)

    #print("FINAL REPORT")
    #for base in unfound_anns:
    #    print("Missed annotations in " + base + ":")
    #    print(unfound_anns[base])

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
