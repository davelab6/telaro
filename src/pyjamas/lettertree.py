class LetterNode(list):

    def __init__(self, letter, weight, childnodes=None):
        self.letter = letter
        self.weight = weight
        if childnodes is None:
            childnodes = []
        list.__init__(self, childnodes)

    def __repr__(self):
        return "%f %f" % (self.x, self.y)

