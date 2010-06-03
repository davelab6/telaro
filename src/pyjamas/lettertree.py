class LetterNode(list):

    def __init__(self, letter, weight, childnodes=None):
        self.letter = letter
        self.weight = weight
        if childnodes is None:
            childnodes = []
        self.word_ptr = None
        list.__init__(self, childnodes)

    def __repr__(self):
        return "{%f-%f %fx%f}" % (self.x, self.y,
                                  self.box_width, self.box_height)

    def __cmp__(self, l):
        if isinstance(l, LetterNode):
            return cmp(self.letter, l.letter)
        return cmp(self.letter, l)

def pprint_letters(letters, tab=0):
    for l in letters:
        ch = repr(l.letter)[1:-1]
        print "%s %s %.2f" % (" "*tab*2, ch, l.weight)
        pprint_letters(l, tab+1)
