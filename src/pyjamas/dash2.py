import pyjd

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.RootPanel import RootPanel

#from letter import Letters
from lettertree import LetterNode

from pyjamas.Canvas.Color import Color
from pyjamas.Canvas.GWTCanvas import GWTCanvas

class Dash:

    def __init__(self):

        self.p = AbsolutePanel(Width="100%", Height="100%",
                               StyleName="dashpanel")
        RootPanel().add(self.p)

        self.cwidth = 500
        self.cheight = 500
        self.canvas = GWTCanvas(self.cwidth, self.cheight)
        self.p.add(self.canvas)
        self.canvas.resize(self.cwidth, self.cheight)

        test_letters = []
        num_chars = 26
        weight = (1.0 / num_chars)
        for i in range(65, num_chars+65):
            test_letters.append (LetterNode(chr(i), weight) )

        test_letters[25].weight = weight/2
        test_letters[24].weight = weight/2
        test_letters[4].weight = weight*2

        self.letters = test_letters
        self.display_letters(0, 0, self.cwidth, self.cheight,
                                self.letters, 0)

    def display_letters(self, px, py, pwidth, pheight, letters, colouridx):

        self.canvas.saveContext()

        if colouridx == 0:
            col = Color("#ccf")
            altcol = Color("#88f")
        elif colouridx == 1:
            col = Color("#fcc")
            altcol = Color("#f88")
        else:
            col = Color("#cfc")
            altcol = Color("#8f8")

        self.canvas.setLineWidth(1)
        self.canvas.fillRect(px, py, pwidth, pheight)

        if not letters:
            return

        newidx = (colouridx+1) % 3
        length = len(letters)
        oy = 0
        for i, letter in enumerate(letters):
            height = letter.weight * pheight
            width  = letter.weight * pwidth
            if i % 2 == 0:
                self.canvas.setFillStyle(col)
            else:
                self.canvas.setFillStyle(altcol)
            letter_x = int(px+(pwidth-width))
            self.display_letters(letter_x, int(py+oy),
                                 width, height,
                                 letter, newidx)
            self.canvas.saveContext()
            self.canvas.setFillStyle(Color("#000"))
            self.canvas.fillText(letter.letter, letter_x, int(py+(oy+height/2+5)))
            self.canvas.restoreContext()
            oy += height

        self.canvas.restoreContext()

if __name__ == '__main__':
    pyjd.setup("./index.html")
    d = Dash()
    pyjd.run()

