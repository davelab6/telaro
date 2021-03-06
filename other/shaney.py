# 2010-07-07 Dave Crosslan downloaded this from 
# http://web.archive.org/web/20000818101532/www.strout.net/python/shaney.py
# after seeing it on www.utilitymill.com 
#
#	shaney.py              by Greg McFarlane
#	                       some editing by Joe Strout
#
#	search for "Mark V.  Shaney" on the WWW for more info!

import sys
import rand
import string

def run(filename=''):
	if filename=='':
		file = open( raw_input('Enter name of a textfile to read: '), 'r')
	else:
		file = open( filename, 'r')
	
	text = file.read()
	file.close()
	words = string.split(text)
	
	end_sentence = []
	dict = {}
	prev1 = ''
	prev2 = ''
	for word in words:
	  if prev1 != '' and prev2 != '':
	    key = (prev2, prev1)
	    if dict.has_key(key):
	      dict[key].append(word)
	    else:
	      dict[key] = [word]
	      if prev1[-1:] == '.':
	        end_sentence.append(key)
	  prev2 = prev1
	  prev1 = word
	
	if end_sentence == []:
	  print 'Sorry, there are no sentences in the text.'
	  return
	
	key = ()
	count = 10
	
	while 1:
	  if dict.has_key(key):
	    word = rand.choice(dict[key])
	    print word,
	    key = (key[1], word)
	    if key in end_sentence:
	      print
	      count = count - 1
	      if count <= 0:
		break
	  else:
	    key = rand.choice(end_sentence)
	
# end of run() function

# immediate-mode commands, for drag-and-drop or execfile() execution
if __name__ == '__main__':
	if len(sys.argv) == 2:
		run(sys.argv[1])		# accept a command-line filename
	else:
		run()
	print
	raw_input("press Return>")
else:
	print "Module shaney imported."
	print "To run, type: shaney.run()"
	print "To reload after changes to the source, type: reload(shaney)"

# end of shaney.py
