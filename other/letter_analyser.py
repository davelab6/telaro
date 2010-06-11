#!/usr/bin/env python
""" Character Usage Analyser
	Analyse a text for character statistics - currently just counting

	Copyright (C) 2010 Dave Crossland <dave@understandingfonts.com>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.
	Also add information on how to contact you by electronic and paper mail.

    $ for i in `ls /usr/share/dict/scowl/english*`; do cat $i >> english.max; done
    $ wc -w english.max                         
    628034 english.max
    $ ./letter_analyser.py -t english.max
"""
import sys
from getopt import getopt, GetoptError
from collections import defaultdict

def count(text):
    """Count the chars in a dict"""
    frequencyDict=defaultdict(int)
    for char in text:
        frequencyDict[char]+=1
    return frequencyDict
    
def printCount(frequencyDict):
    """Print the dict's item ready for pasting into spreadsheets"""
    for item in frequencyDict.items():
        print str(item[0]), str(item[1])

if __name__ == '__main__':
    try:
        opts, args = getopt(sys.argv[1:], "t:h",
                ["text=", "help"])
# TODO this is broken...
    except GetoptError, message:
        print "%s: %s" %(sys.argv[0], message)
        usage()
        exit(0)

    for optind, optarg in opts:
        if optind in ("--text", "-t"):
            text = open(optarg).read()
            print "Analysing %s..." % optarg

    frequencyDict = count(text)
    print "Done! Characters and their count: "
    printCount(frequencyDict)
