When designing a typeface, a short word such as "adhesion" or "shoplift" can be used to prototype the key features of the typeface. To transform this from lettering to typeface design, the letterforms must be typeset with a long text for reading.

The most simple way to approximate this is to randomly typeset the letters for one page. This can be improved by analysing a source text for letter frequencies; Fontforge's font.randomText() provides this functionality.

But random letters are not words. Thus the next level of approximating real text is to search a dictionary for all the words that can be written using only the given letters, and typeset these words randomly for 1 page of text (say, 800 words). [Telaro will provide this](http://code.google.com/p/telaro/issues/detail?id=3) but for now the proprietary www.adhesiontext.com web service provides this functionality.

But random words are not sentences. If you prepare a text file containing sentences using only words from such a subset, Telaro will amplify the number of sentences you have written. So you can write a few dozen sentences, and get a whole page of text.

Telaro does this by processing your text file into markov chains. This technique is used for "chat bots" such as [NIALL](http://www.lab6.com/old/niall.html), and many other Markov text generators have been published as free software, such as the python [Parody Generator](http://utilitymill.com/edit/Markov_Chain_Parody_Text_Generator).

Downloading the source code and run Telaro from the command line. You'll need Python and Mercurial installed.

```
$ hg clone https://telaro.googlecode.com/hg/ telaro 
$ cd telaro
$ ./telaro.py < TrainingTexts/adhesion.txt > output.txt
```