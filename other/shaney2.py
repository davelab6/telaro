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
"""

import random
#import os
import sys
from string import strip
#import string
from getopt import getopt, GetoptError

def mark_v_shaney(text, size):
    assert size > 0
    link, term = build_links(text)
    assert size < len(term)
    mark = build_chain(size, link, term)
    return mark

def build_links(text):
    words = text.split()
    link = {}
    term = []
    for index in range(len(words) - 2):
        a, b, c = words[index:index+3]
        key = a, b
        if key in link:
            value = link[key]
            if c not in value:
                value.append(c)
        else:
            link[key] = [c]
        if b[-1] in list('.?!'):
            if key not in term:
                term.append(key)
    if c[-1] in list('.?!'):
        key = b, c
        if key not in term:
            term.append(key)
    return link, term

def build_chain(size, link, term):
    key = random.choice(term)
    cache = []
    buffer = []
    while True:
        if key in link:
            word = random.choice(link[key])
            buffer.append(word)
            key = key[1], word
            if key in term:
                sentence = ' '.join(buffer)
                if sentence not in cache:
                    cache.append(sentence)
                    if len(cache) == size:
                        return ' '.join(cache)
                buffer = []
        else:
            key = random.choice(term)

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

    print (textwrap.fill(mark_v_shaney(trainingtext,int(count)), 80))
