import pyjd

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.RootPanel import RootPanel

#from letter import Letters
from lettertree import LetterNode

from pyjamas.Canvas.Color import Color
from pyjamas.Canvas.GWTCanvas import GWTCanvas

def dist(dx, dy):
    return dx*dx + dy*dy

def _check_closest(letter1, letter2, x, y):
    return (dist(letter1.x - x, letter1.y - y) < 
           dist(letter2.x - x, letter2.y - y))

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
        self.offset_x = 0
        self.offset_y = 0
        self.scale_x = 1.0
        self.scale_y = 1.0

        test_letters = []
        num_chars = 26
        weight = (1.0 / num_chars)
        for i in range(65, num_chars+65):
            test_letters.append (LetterNode(chr(i), weight) )

        test_letters[25].weight = weight/2
        test_letters[24].weight = weight/2
        test_letters[4].weight = weight*2

        self.letters = test_letters
        self.closest = [None, None]
        self.display_letters(0, 0, self.cwidth, self.cheight,
                                self.letters, 0)
        print self.closest

    def check_closest(self, letter, x, y):
        """ this function gets the two closest letters to the current cursor.
        """
        print self.closest
        if self.closest[0] is None:
            print "none"
            self.closest[0] = letter
        else:
            print x, y, letter.x, letter.y
            if _check_closest(self.closest[0], letter, x, y):
                return
            self.closest[1] = self.closest[0]
            self.closest[0] = letter

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
            letter.x = int(px+(pwidth-width))
            letter.y = int(py+oy)
            letter.box_width = width
            letter.box_height = height
            self.display_letters(letter.x, letter.y,
                                 width, height,
                                 letter, newidx)
            self.check_closest(letter,
                            self.offset_x + (self.cwidth/2) * self.scale_x,
                            self.offset_y + (self.cheight/2) * self.scale_y)
            self.canvas.saveContext()
            self.canvas.setFillStyle(Color("#000"))
            self.canvas.fillText(letter.letter, letter.x, int(py+(oy+height/2+5)))
            self.canvas.restoreContext()
            oy += height

        self.canvas.restoreContext()

if __name__ == '__main__':
    pyjd.setup("./index.html")
    d = Dash()
    pyjd.run()

