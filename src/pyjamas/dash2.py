import pyjd
import math

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Label import Label

#from letter import Letters
from lettertree import LetterNode, pprint_letters
from words import get_test_letters

from pyjamas.Canvas.Color import Color
from pyjamas.Canvas.GWTCanvas import GWTCanvas

from pyjamas.Timer import Timer
from pyjamas import DOM
from time import time

def dist(dx, dy):
    return dx*dx + dy*dy

def _check_closest(letter1, letter2, x, y):
    l1_x = letter1.x #+ letter1.box_width/2
    l1_y = letter1.y + letter1.box_height/2
    l2_x = letter2.x #+ letter2.box_width/2
    l2_y = letter2.y + letter2.box_height/2
    return (dist(l1_x - x, l1_y - y) < 
           dist(l2_x - x, l2_y - y))

def _inside(letter, x, y):
    if x < letter.x:
        return False
    if y < letter.y:
        return False
    if x > letter.x + letter.box_width:
        return False
    if y > letter.y + letter.box_height:
        return False
    return True
    
def calc_scale(letter1, letter2, x, y, height):
    l1_x = letter1.x #+ letter1.box_width/2
    l1_y = letter1.y + letter1.box_height/2
    l2_x = letter2.x #+ letter2.box_width/2
    l2_y = letter2.y + letter2.box_height/2
    d1 = pow(dist(l1_x - x, l1_y - y), 0.5)
    d2 = pow(dist(l2_x - x, l2_y - y), 0.5)
    min_d1 = min(height/2, d1)
    min_d2 = min(height/2, d2)

    # divide by 8, seems to work.  no idea why.
    max_scale1 = height / letter1.box_height / 8
    max_scale2 = height / letter2.box_height / 8

    # ok.  complicated.  the closer the cursor is, the more "relevant"
    # the scaling.  d1 or d2 equal to zero means _spot_ on cursor.

    max_scale = min(max_scale1, max_scale2) # start with min, add rest in a mo
    scale_diff = max(max_scale1, max_scale2) - max_scale

    if d1 < d2:
        proportion = ((d2-d1)/d2)
    else:
        proportion = ((d1-d2)/d1)

    max_scale += scale_diff * proportion

    return max_scale

class Dash:

    def __init__(self):

        self.p = AbsolutePanel(Width="100%", Height="100%",
                               StyleName="dashpanel")
        RootPanel().add(self.p)
        self.log = Label("log")

        self.cwidth = 700.0
        self.cheight = 700.0
        self.canvas = GWTCanvas(self.cwidth, self.cheight)
        self.p.add(self.canvas, 0, 0)
        self.p.add(self.log, self.cwidth+10, 0)
        self.canvas.resize(self.cwidth, self.cheight)
        self.cwidth = 700.0
        self.cheight = 700.0
        #self.offset_x = 423.0-233#240.0
        #self.offset_y = 153.0-220#-100.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale = 1.0
        self.target_scale = 1.0
        self.move_allowed = False

        w2 = self.cwidth / 2.0
        h2 = self.cheight / 2.0

        self.word_chain = get_test_letters()
        # TODO: make a fake "top level" LetterNode, which these are added to
        self.letters = self.get_more_letters()
        self.root_node = self.letters

        self.cur_time = time()
        self.mouse_pos_x = w2
        self.mouse_pos_y = h2

        self.draw()

        Timer(50, self)

        self.canvas.addMouseListener(self)

    def new_mouse_pos(self, x, y):
        el = self.canvas.getElement()
        self.mouse_pos_x = x - DOM.getAbsoluteLeft(el)
        self.mouse_pos_y = y - DOM.getAbsoluteTop(el)

    def onMouseDown(self, sender, x, y):
        self.move_allowed = True
        self.new_mouse_pos(x, y)

    def onMouseUp(self, sender, x, y):
        self.move_allowed = False
        self.new_mouse_pos(x, y)

    def onMouseMove(self, sender, x, y):
        self.new_mouse_pos(x, y)

    def onMouseEnter(self, sender):
        pass

    def onMouseLeave(self, sender):
        self.move_allowed = False

    def onTimer(self, timer):
        
        new_time = time()
        diff_time = new_time - self.cur_time
        self.cur_time = new_time

        self.log.setText("time: %.2f" % self.cur_time)

        scale = diff_time / (self.scale)

        #print self.move_allowed, "%.3f" % diff_time, self.mouse_pos_x, self.mouse_pos_y

        scale_diff = math.log10(self.target_scale) - math.log10(self.scale)
        scale_diff = scale_diff * diff_time * 2
        self.scale = math.pow(10, math.log10(self.scale) + scale_diff)

        if self.move_allowed:
            w2 = self.cwidth / 2.0
            h2 = self.cheight / 2.0
            x_vel = scale * (self.mouse_pos_x - w2)
            y_vel = scale * (self.mouse_pos_y - h2)

            self.offset_x += x_vel
            self.offset_y += y_vel
            self.redraw_required = True

        elif abs(scale_diff) > 1e-15:
            self.redraw_required = True

        if self.redraw_required:
            self.draw()

        Timer(50, self)

    def draw(self):

        self.redraw_required = False

        w2 = self.cwidth / 2.0
        h2 = self.cheight / 2.0

        self.closest = [None, None]

        self.get_closest(0.0, 0.0, self.cwidth, self.cheight,
                                self.root_node)

        #print self.closest

        scale = calc_scale(self.closest[0], self.closest[1],
                                  self.offset_x,
                                    self.offset_y+h2,
                                    self.cheight)
        self.target_scale = scale

        #print "scale:", self.scale, self.target_scale

        x1 = self.offset_x + (self.cwidth / self.scale)
        y1 = self.offset_y + (self.cheight / self.scale)

        #print "redbox", self.offset_x, self.offset_y, x1, y1

        self.canvas.clear()
        self.canvas.saveContext()

        self.canvas.setFillStyle(Color("#888"))
        self.canvas.setLineWidth(1)
        self.canvas.fillRect(0, 0, self.cwidth, self.cheight)

        self.display_letters(None, 0.0, 0.0, self.cwidth, self.cheight,
                                self.root_node, 0)

        self.canvas.restoreContext()

        #print self.closest

    def sr(self, x, y, w, h):
        #sw = (self.cwidth/2/self.scale)
        #sh = (self.cheight/2/self.scale)
        sw = self.cwidth/2.0
        sh = self.cheight/2.0
        rect = (-sw*self.scale+(x+(-self.offset_x+sw/self.scale))*self.scale,
                -sh*self.scale+(y+(-self.offset_y+sh/self.scale))*self.scale,
                w*self.scale,
                h*self.scale)
        #print "rect", x,y,w,h, rect
        return rect

    def check_closest(self, letter, x, y):
        """ this function gets the two closest letters to the current cursor.
        """
        #print self.closest
        if self.closest[0] is None:
            #print "none"
            self.closest[0] = letter
        else:
            #print x, y, letter.x, letter.y
            if _check_closest(self.closest[0], letter, x, y):
                return
            self.closest[1] = self.closest[0]
            self.closest[0] = letter

    def get_closest(self, px, py, pwidth, pheight, letters):

        if not letters:
            return

        length = len(letters)
        amount_use = 1.0
        oy = 0.0 # pheight * (1.0-amount_use) / 2.0
        for i, letter in enumerate(letters):
            height = letter.weight * pheight 
            width  = letter.weight * pwidth
            letter.x = px+(pwidth - width) #+ height * 0.1
            letter.y = py+oy
            letter.box_width = width
            letter.box_height = height * amount_use

            cursor_x = self.offset_x + (self.cwidth/2.0)
            cursor_y = self.offset_y + (self.cheight/2.0)

            if _inside(letter, cursor_x, cursor_y):
                self.inside_letter = letter

            self.get_closest(letter.x, letter.y,
                                 letter.box_width, letter.box_height,
                                 letter)
            self.check_closest(letter, cursor_x, cursor_y)

            oy += letter.box_height

    def get_more_letters(self, letter=None):
        res = []
        if letter is None or letter.word_ptr is None or \
           len(letter.word_ptr) == 0:
            chain = self.word_chain
        else:
            chain = letter.word_ptr
        for l in chain:
            ln = LetterNode(l.letter, l.weight, parent=l.parent)
            ln.word_ptr = l
            res.append(ln)
        #print "letter", letter
        #pprint_letters(res)
        return res

    def display_letters(self, ch, px, py, pwidth, pheight, letters, colouridx):

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
        x, y, w, h = self.sr(px, py, pwidth, pheight)

        if y + h < 0:
            return
        if y > self.cheight:
            return
        if x + w < 0:
            return
        if x > self.cwidth:
            return

        self.canvas.fillRect(x, y, w, h)

        if ch:
            self.canvas.setFillStyle(Color("#000"))
            self.canvas.fillText(ch, x, y + h)

        if h < 20:
            return

        if not letters:
            more = self.get_more_letters(letters)
            self.redraw_required = True
            return more

        if not letters:
            return

        newidx = (colouridx+1) % 3
        length = len(letters)
        oy = 0
        for i, letter in enumerate(letters):
            height = letter.box_width
            width  = letter.box_height
            if i % 2 == 0:
                self.canvas.setFillStyle(col)
            else:
                self.canvas.setFillStyle(altcol)
            more = self.display_letters(letter.letter, letter.x, letter.y,
                                 width, height,
                                 letter, newidx)
            if more:
                for l in more:
                    letter.append(l)
            oy += height


if __name__ == '__main__':
    pyjd.setup("./public/dash2.html")
    d = Dash()
    pyjd.run()

