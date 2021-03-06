#!/usr/bin/env python
""" Telaro
	
	A test text generator for font development, using Markov chains.

	Copyright (C) 2010 Luke Kenneth Casson Leighton <luke.leighton@googlemail.com>

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

	
	telaro.py includes a simple calculator with variables, copied from 
	O'Reilly's "Lex and Yacc," page 63, and a class-based example contributed 
	to PLY by David McNab.
	
	TODO: check this is legal, and explain the file better.
	TODO: en.wikipedia.org/wiki/Markov_blanket has a nice diagram of how it works
	
	./telaro.py -l adhesion -d /usr/share/dict/scowl/british-words.55 < TrainingTexts/adhesion.txt > output.txt
"""

import sys
sys.path.insert(0,"../..")

#import readline
import ply.lex as lex
import ply.yacc as yacc
import os
from getopt import getopt, GetoptError
import sys
from string import strip

from markov import Markov, random_sentence

def print_sentence(sentence, word_filter=None, max_chars=78):
    to_print = ''
    while sentence:
        word = sentence.pop(0)
        if (word not in ' ()=-+.,:;\t?!"\'"' and
           word_filter and not word_filter.has_key(word.lower())):
            continue
        if word == '\x00':
            print to_print
            print
            to_print = ''
            continue
        if len(to_print) + len(word) > max_chars:
            print to_print
            to_print = ''
        if to_print:
            if word in ' ()=-+.,:;\t?!"\'"':
                to_print += word
            else:
                to_print += ' ' + word
        else:
            to_print = word
    if to_print:
        print to_print

class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.sentences = []
        self.markov = Markov()
        self.clause_starter = {}
        self.para_starter = []
        self.words = kw.get('words', None)

        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        s = sys.stdin.read()
        s = s.replace('\n\n', '\x00')
        s = s.replace('\x00\x00', '\x00')
        s = s.replace('\n\n', '')
        s = s.replace('\n', ' ')
        s = s.replace('  ', ' ')
        yacc.parse(s)
        print self.sentences
        self.markov.printout()
        print
        print "clause starters"
        keys = self.clause_starter.keys()
        keys.sort()
        for k in keys:
            v = self.clause_starter[k]
            print "\t", repr(k), v
        print
        print "para starters", self.para_starter
        print
        self.markov.prepare()
        sentence = random_sentence(self.markov, 800,
                                    starters=self.clause_starter,
                                    para_starters=self.para_starter)
        print_sentence(sentence, word_filter=self.words)

    
class Text(Parser):

    tokens = (
        'NAME',#'NUMBER',
        'FULLSTOP',
        'NULL',
        #'LBRACK',
        #'QUOTE',
        #'RBRACK',
        'COLON','SEMICOLON', 
        'EXCLAMATION','QUESTIONMARK', 
        'NEWLINE',
        'TAB',
        'SLASH',
        'COMMA',
        )

    # Tokens

    t_NULL  = r'\x00'
    t_FULLSTOP  = r'\.'
    #t_SPACE     = r'\ '
    t_COLON     = r':'
    t_SEMICOLON = r';'
    t_NEWLINE = r'\n'
    t_EXCLAMATION = r'!'
    #t_QUOTE      = r'[\'"]'
    #t_LBRACK      = r'\('
    #t_RBRACK      = r'\)'
    t_QUESTIONMARK = r'\?'
    t_TAB       = r'\t'
    t_COMMA     = r','
    t_SLASH     = r'/'
    t_NAME      = r'[a-zA-Z0-9_][\'`a-zA-Z0-9_]*'

    def _t_FLOAT(self, t):
        r'\d+[\.]\d*'
        try:
            t.value = float(t.value)
        except ValueError:
            print "Integer value too large", t.value
            t.value = 0
        print "parsed number %s" % repr(t.value)
        return t

    def _t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print "Integer value too large", t.value
            t.value = 0
        print "parsed number %s" % repr(t.value)
        return t

    t_ignore = " "

    def _t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
        print "Illegal character '%s'" % repr(t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    #precedence = (
    #    ('left','PLUS','MINUS'),
    #    ('left','TIMES','DIVIDE'),
    #    ('left', 'EXP'),
    #    ('right','UMINUS'),
    #    )

    def p_text_para(self, p):
        'text : paragraph'
        self.sentences.append(p[1])
        self.para_starter.append(p[1][0])
        p[0] = [p[1]]

    def p_text_paras(self, p):
        'text : text NULL paragraph'
        self.markov.inc_state_link(p[1][-1][-1], p[2])
        self.markov.inc_state_link(p[2], p[3][0])
        self.sentences.append(p[3])
        self.para_starter.append(p[3][0])
        p[0] = p[1] + [p[3]]
        #print "join", repr(p[-1][-1][-1]), repr(p[2]), repr(p[3][0])

    def p_paragraph_assign(self, p):
        'paragraph : sentences'
        #self.sentences.append(p[1])
        #self.markov.inc_state_link(p[1][-1], p[2])
        p[0] = p[1] #+ [p[2]]

    def p_sentences_ended(self, p):
        """sentence : sentence clausedivider
        """
        #if p[2] != '\n' or p[1][-1] in ':;,. \n':
        self.markov.inc_state_link(p[1][-1], p[2])
        p[0] = p[1] + [p[2]]

    #def p_paradivider_expr(self, p):
    #    """paradivider : FULLSTOP NEWLINE
    #    """
    #    self.markov.inc_state_link(p[1], p[2])
    #    p[0] = [p[1], p[2]]

    def p_sentenceending_prefixedtwice(self, p):
        """sentenceending : clausedivider clausedivider sentence
        """
        #if p[1] != '\n' or p[2][0] in ':;,. \n':
        self.markov.inc_state_link(p[1], p[2])
        self.markov.inc_state_link(p[2], p[3][0])
        if not self.clause_starter.has_key(p[2]):
            self.clause_starter[p[2]] = []
        self.clause_starter[p[2]].append(p[3][0])
        if p[2] in '.?! \n':
            self.para_starter.append(p[3][0])
        p[0] = [p[1], p[2]] + p[3]

    def p_sentenceending_prefixed(self, p):
        """sentenceending : clausedivider sentence
        """
        #if p[1] != '\n' or p[2][0] in ':;,. \n':
        self.markov.inc_state_link(p[1], p[2][0])
        if not self.clause_starter.has_key(p[1]):
            self.clause_starter[p[1]] = []
        self.clause_starter[p[1]].append(p[2][0])
        if p[1] in '.?! \n':
            self.para_starter.append(p[2][0])
        p[0] = [p[1]] + p[2]

    def p_sentences_divided(self, p):
        """sentence : sentence sentenceending
        """
        #if p[2][0] != '\n' or p[1][-1] in '\n.':
        self.markov.inc_state_link(p[1][-1], p[2][0])
        p[0] = p[1] + p[2]

    def p_sentences_single(self, p):
        """sentences : sentence
        """
        #print "single sentence", p[1]
        p[0] = p[1]
        
    def p_clausedivider_expr(self, p):
        """clausedivider : FULLSTOP
                         | COLON
                         | SEMICOLON
                         | TAB
                         | SLASH
                         | COMMA
                         | EXCLAMATION
                         | QUESTIONMARK
        """
        p[0] = p[1]

    def p_sentence_namesorlinks(self, p):
        """sentence : sentence NAME
        """
        #print "sentence names", p[1], p[2]
        self.markov.inc_state_link(p[1][-1], p[2])
        p[0] = p[1] + [p[2]]

    #def p_hyperlink_expr1(self, p):
    #    """hyperlink : NAME COLON SLASH SLASH namedots
    #    """
    #    p[0] = p[1]+"://"+p[5]
    #    print "hyperlink", p[0]

    #def p_namedots_expr(self, p):
    #    """namedots : NAME FULLSTOP namedots
    #    """
    #    p[0] = p[1]+"."+p[3]

    #def p_namedots_name(self, p):
    #    """namedots : NAME
    #    """
    #    p[0] = p[1]

    def p_sentence_name(self, p):
        """sentence : NAME
        """
        p[0] = [p[1]]

    #def p_nameorhyp_exp(self, p):
    #    """nameorhyp : NAME
    #                | hyperlink"""
    #    p[0] = p[1]

    def p_error(self, p):
        if p:
            print "Syntax error at '%s'" % repr(p.value)
        else:
            print "Syntax error at EOF"

def check_all_letters_in(letters, word):
    for w in word:
        if w.lower() not in letters and w.upper() not in letters:
            return False
    return True

if __name__ == '__main__':

    use_words = False
    words_file = "/usr/share/dict/words"
    letters = map(chr, range(65+32, 65+26+32)) + ["'`"]

    try:
        opts, args = getopt(sys.argv[1:], "l:d:h",
                ["letters=", "dictionary=", "help"])
    except GetoptError, message:
        print "%s: %s" %(sys.argv[0], message)
        usage()
        exit(0)

    for optind, optarg in opts:
        if optind in ("--dictionary", "-d"):
            use_words = True
            words_file = optarg
        elif optind in ("--letters", "-l"):
            letters = []
            for l in optarg:
                letters.append(l)

    words = None
    if use_words:
        words = {}
        for w in open(words_file).readlines():
            w = w.strip()
            if not letters:
                words[w.lower()] = 1
            else:
                if check_all_letters_in(letters, w):
                    words[w.lower()] = 1

    calc = Text(words=words)
    calc.run()
