import pyjd
import math

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HTML import HTML

#from letter import Letters
from lettertree import LetterNode, pprint_letters
from words import get_test_letters

from keyboard import Qwerty
from textbox import T9TextArea

from pyjamas.Timer import Timer
from pyjamas import DOM
from pyjamas import log
from time import time


class Dash:

    def __init__(self):

        self.p = VerticalPanel(Width="700px", Height="700px",
                               StyleName="dashpanel")
        RootPanel().add(self.p)
        self.log = HTML("log", Width="500px", Height="100px")

        self.kbd = Qwerty()
        self.tb = T9TextArea(self, '')
        self.p.add(self.tb)
        self.p.add(self.kbd)
        self.p.add(self.log)

        self.word_chain = get_test_letters()
        # TODO: make a fake "top level" LetterNode, which these are added to
        self.letters = self.get_more_letters()
        self.root_node = self.letters

        self.cur_time = time()

        self.redraw_required = True
        #self.draw()

        self.tb.setFocus(True)
        self.tb.addChangeListener(self)
        self.tb.addClickListener(self)
        self.old_text = None
        self.old_pos = None
        self.textNotify('')

    def textNotify(self, text):
        """ determine text position, next letters, pass them to on-screen
            keyboard
        """
        pos = self.tb.getCursorPos()
        if text == self.old_text and pos == self.old_pos:
            return
        self.old_text = text
        self.old_pos = pos

        # first, hunt through the letters-tree.
        node = self.letters
        log.writebr("pos %d %s" % (pos, text))
        for i, t in enumerate(text):
            if i == pos:
                break
            #log.writebr("checking %s" % t)
            next_node = None
            for l in node:
                #log.writebr("\tagainst %s" % l.letter)
                if len(l) == 0:
                    more = self.get_more_letters(l)
                    for m in more:
                        l.append(m)
                if t == l.letter:
                    next_node = l
                    break
            if not next_node:
                self.tb.setSelectionRange(i, len(self.tb.getText()))
                return
            node = next_node
        
        available_keys = ''
        for l in node:
            letter = l.letter
            ul = letter.upper()
            available_keys += letter
            if ul != letter:
                available_keys += ul
        self.kbd.activate(available_keys)
        self.tb.setAvailableKeys(available_keys)

    def execute(self):
        self.onChange(self.tb)

    def onClick(self, sender):
        print "click"
        text = self.tb.getText()
        self.textNotify(text)

    def onChange(self, sender):
        text = sender.getText()
        self.textNotify(text)

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

    def draw(self):

        self.canvas.resize(self.cwidth, self.cheight)
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

        self.log_txt += "scale: %f<br/>" % self.scale
        self.log_txt += "targetscale: %f<br/>" % self.target_scale

        #print "scale:", self.scale, self.target_scale

        x1 = self.offset_x + (self.cwidth / self.scale)
        y1 = self.offset_y + (self.cheight / self.scale)

        #print "redbox", self.offset_x, self.offset_y, x1, y1

        self.canvas.saveContext()
        self.canvas.clear()

        #self.canvas.setFillStyle(Color("#888"))
        #self.canvas.setLineWidth(1)
        #self.canvas.fillRect(0, 0, self.cwidth, self.cheight)

        self.display_letters(None, 0.0, 0.0, self.cwidth, self.cheight,
                                self.root_node, 0)

        self.canvas.restoreContext()

        #print self.closest

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
    pyjd.setup("./public/t9.html")
    d = Dash()
    pyjd.run()

