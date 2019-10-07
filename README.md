# FigureLinking

##Evaluation

Main files: evaluate.py evaluate_summary.py



evaluate.py is a Python 2.7 script intended to compare exactly one pair of annotation files.

Requires a ground truth annotation file, a non-ground truth annotation file, a config file, and an output path.

Optional flag: --json

Tells the script to use .json files in place of .ann files as arguments.  NOTE: JSON object structure not finalized; functionality incomplete.

Run "python evaluate.py --help" for more information on the individual flags.



evaluate_summary.py runs the evaluation script on all pairs of ground truth and non-ground truth files within a folder that follow a specific naming convention.

Requires a directory containing all annotation files and a directory to contain outputs.

The naming convention is as follows:

- Ground truth annotation files must be named "gt*.ann", where the asterisk represents an arbitrary sequence of characters.
- Non-ground truth annotation files must be named "res*.ann", where the asterisk represents an arbitrary sequence of characters.

NOTE: For evaluation to be run on a pair of files, the arbitrary sequences of characters used in each filename must be identical.  Otherwise, the files will be discarded.




