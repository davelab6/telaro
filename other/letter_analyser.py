#!/usr/bin/env python
""" Markov Chain Parody Text Generator 
	A text generator, using Markov chains.

	Copyright (C) 2009, 2010 Various Contributors From
	http://utilitymill.com/edit/Markov_Chain_Parody_Text_Generator 

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
	
	./letter_analyser.py -t TrainingTexts/adhesion.txt
"""

from cStringIO import StringIO
from getopt import getopt, GetoptError
import sys

std_key_size = 0

keyboard_mapping={
#position, size, iscap
'a': ((145,222),std_key_size,False),
'b': ((385,272),std_key_size,False),
'c': ((278,272),std_key_size,False),
'd': ((253,222),std_key_size,False),
'e': ((239,170),std_key_size,False),
'f': ((305,222),std_key_size,False),
'g': ((358,222),std_key_size,False),
'h': ((412,222),std_key_size,False),
'i': ((508,170),std_key_size,False),
'j': ((467,222),std_key_size,False),
'k': ((520,222),std_key_size,False),
'l': ((574,222),std_key_size,False),
'm': ((493,272),std_key_size,False),
'n': ((438,272),std_key_size,False),
'o': ((560,170),std_key_size,False),
'p': ((615,170),std_key_size,False),
'q': ((131,170),std_key_size,False),
'r': ((294,170),std_key_size,False),
's': ((200,222),std_key_size,False),
't': ((346,170),std_key_size,False),
'u': ((454,170),std_key_size,False),
'v': ((332,272),std_key_size,False),
'w': ((186,170),std_key_size,False),
'x': ((224,272),std_key_size,False),
'y': ((400,170),std_key_size,False),
'z': ((171,272),std_key_size,False),
'0': ((590,118),std_key_size,False),
'1': ((102,118),std_key_size,False),
'2': ((157,118),std_key_size,False),
'3': ((213,118),std_key_size,False),
'4': ((265,118),std_key_size,False),
'5': ((320,118),std_key_size,False),
'6': ((374,118),std_key_size,False),
'7': ((427,118),std_key_size,False),
'8': ((480,118),std_key_size,False),
'9': ((535,118),std_key_size,False),
')': ((590,118),std_key_size,True),
'!': ((102,118),std_key_size,True),
'@': ((157,118),std_key_size,True),
'#': ((213,118),std_key_size,True),
'$': ((265,118),std_key_size,True),
'%': ((320,118),std_key_size,True),
'^': ((374,118),std_key_size,True),
'&': ((427,118),std_key_size,True),
'*': ((480,118),std_key_size,True),
'(': ((535,118),std_key_size,True),
'`': ((51,118),std_key_size,False),
'~': ((51,118),std_key_size,True),
'-': ((643,118),std_key_size,False),
'_': ((643,118),std_key_size,True),
'=': ((695,118),std_key_size,False),
'+': ((695,118),std_key_size,True),
'|': ((777,170),(65,38),True),
'\\': ((777,170),(65,38),False),
'[': ((670,170),std_key_size,False),
']': ((722,170),std_key_size,False),
'{': ((670,170),std_key_size,True),
'}': ((722,170),std_key_size,True),
';': ((627,222),std_key_size,False),
':': ((627,222),std_key_size,True),
"'": ((681,222),std_key_size,False),
'"': ((681,222),std_key_size,True),
'/': ((654,272),std_key_size,False),
'?': ((654,272),std_key_size,True),
'>': ((600,272),std_key_size,True),
'<': ((547,272),std_key_size,True),
',': ((547,272),std_key_size,False),
'.': ((600,272),std_key_size,False),
'\n': ((735,222),(106,38),False),
'\t': ((47,170),(70,38),False),
'shift1': ((47,272),(112,38),False),
'shift2': ((708,272),(112,38),False),
' ': ((280,326),(334,43),False),
}

def char_freq(text):
    from collections import defaultdict
    freq=defaultdict(int) # when key is not found, inserts 0
    for char in text:
        freq[char]+=1
        #Handle keys that can be two chars, eg 9 and (
        if char in keyboard_mapping:
            position=keyboard_mapping[char][0]
            for key,(key_position,size,isupper) in keyboard_mapping.items():
                if key_position==position and key!=char:
                    freq[key]+=1
        #Handle counting hits of shift key
        if char.isupper():
            freq['shift1']+=1
            freq['shift2']+=1
        elif char in keyboard_mapping and keyboard_mapping[char][2]:
            freq['shift1']+=1
            freq['shift2']+=1
    return freq


def heatmap(text):
    freq=char_freq(text)
    import pprint
    pprint.pprint(freq)
#   turn into percents
    total=float(sum(freq.values()))
    for char in freq:
        freq[char]=(freq[char]/total)*100
    pprint.pprint(freq)


def main(text, space2tab, heat_map):
    keyboard_im = Image.open(StringIO(keyboard_im_file))
    
    if space2tab:
        text = text.replace(' ' * space2tab, '\t')
    if heat_map:
        final_im = heatmap(text, keyboard_im)
        key_im = Image.open(StringIO(key_im_file))
        final_im = add_key(final_im, key_im)
    else:
        final_im = keyhit_plot(text, keyboard_im)
    
    tmp = StringIO()
    final_im.save(tmp, "JPEG")
    tmp.seek(0)
    return tmp

if __name__ == '__main__':
    import textwrap
    count = 10

    try:
        opts, args = getopt(sys.argv[1:], "c:t:h",
                ["count=", "trainingtext=", "help"])
# TODO this is broken...
    except GetoptError, message:
        print "%s: %s" %(sys.argv[0], message)
        usage()
        exit(0)

    for optind, optarg in opts:
        if optind in ("--count", "-c"):
            count = optarg
        elif optind in ("--trainingtext", "-t"):
            trainingtext = open(optarg).read()

    heatmap(trainingtext)
