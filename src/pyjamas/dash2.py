import pyjd

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.RootPanel import RootPanel

#from letter import Letters
from lettertree import LetterNode

from pyjamas.Canvas.Color import Color
from pyjamas.Canvas.GWTCanvas import GWTCanvas

from pyjamas.Timer import Timer
from pyjamas import DOM
from time import time

def dist(dx, dy):
    return dx*dx + dy*dy

def _check_closest(letter1, letter2, x, y):
    l1_x = letter1.x + letter1.box_width/2
    l1_y = letter1.y + letter1.box_height/2
    l2_x = letter2.x + letter2.box_width/2
    l2_y = letter2.y + letter2.box_height/2
    return (dist(l1_x - x, l1_y - y) < 
           dist(l2_x - x, l2_y - y))

def calc_scale(letter1, letter2, x, y, height):
    l1_x = letter1.x + letter1.box_width/2
    l1_y = letter1.y + letter1.box_height/2
    l2_x = letter2.x + letter2.box_width/2
    l2_y = letter2.y + letter2.box_height/2
    d1 = pow(dist(l1_x - x, l1_y - y), 0.5)
    d2 = pow(dist(l2_x - x, l2_y - y), 0.5)
    if d1 < d2:
        scale_letter = letter1
    else:
        scale_letter = letter2
    min_d = min(height/2, min(d1, d2))
    scale = ((height/2 - min_d) / (height/2))
    print "calc_scale", x, y, d1, d2, min_d, height, scale_letter.box_height, scale
    #return 1.0
    #return 0.5
    max_scale = height / scale_letter.box_height / 2
    return (max_scale - 1.0) * scale + 1.0
    
class Dash:

    def __init__(self):

        self.p = AbsolutePanel(Width="100%", Height="100%",
                               StyleName="dashpanel")
        RootPanel().add(self.p)

        self.cwidth = 700
        self.cheight = 700
        self.canvas = GWTCanvas(self.cwidth, self.cheight)
        self.p.add(self.canvas)
        self.canvas.resize(self.cwidth, self.cheight)
        self.cwidth = 500
        self.cheight = 500
        #self.offset_x = 423.0-233#240.0
        #self.offset_y = 153.0-220#-100.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.move_allowed = False

        w2 = self.cwidth / 2.0
        h2 = self.cheight / 2.0

        test_letters = []
        num_chars = 26
        weight = (1.0 / num_chars)
        for i in range(65, num_chars+65):
            test_letters.append (LetterNode(chr(i), weight) )

        test_letters[25].weight = weight/2
        test_letters[24].weight = weight/2
        test_letters[23].weight = weight/2
        test_letters[22].weight = weight/2
        test_letters[21].weight = weight/2
        test_letters[20].weight = weight/2
        test_letters[8].weight = weight*4

        self.letters = test_letters
        self.cur_time = time()
        self.mouse_pos_x = w2
        self.mouse_pos_y = h2

        test_letters[8].append((LetterNode("a", 0.5) ) )
        test_letters[8].append((LetterNode("b", 0.5) ) )

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

        print self.move_allowed, "%.3f" % diff_time, self.mouse_pos_x, self.mouse_pos_y

        if self.move_allowed:
            w2 = self.cwidth / 2.0
            h2 = self.cheight / 2.0
            scale = diff_time / (self.scale_x)
            x_vel = scale * (self.mouse_pos_x - w2)
            y_vel = scale * (self.mouse_pos_y - h2)

            self.offset_x += x_vel
            self.offset_y += y_vel
            self.draw()

        Timer(50, self)

    def draw(self):

        w2 = self.cwidth / 2.0
        h2 = self.cheight / 2.0

        self.closest = [None, None]

        self.get_closest(0, 0, self.cwidth, self.cheight,
                                self.letters)

        scale = calc_scale(self.closest[0], self.closest[1],
                                  self.offset_x+w2,
                                    self.offset_y+h2,
                                    self.cheight*0.8)
        self.scale_x = scale
        self.scale_y = scale

        print "scale:", scale

        x1 = self.offset_x + (self.cwidth / self.scale_x)
        y1 = self.offset_y + (self.cheight / self.scale_y)

        print "redbox", self.offset_x, self.offset_y, x1, y1

        self.canvas.clear()
        self.canvas.saveContext()

        self.canvas.setFillStyle(Color("#888"))
        self.canvas.setLineWidth(1)
        self.canvas.fillRect(0, 0, self.cwidth, self.cheight)

        #self.canvas.translate(-self.offset_x-(w2/self.scale_x), -self.offset_y-(h2/self.scale_y))
        #self.canvas.scale(self.scale_x, self.scale_y)
        #self.canvas.translate(-self.offset_x/self.scale_x, -self.offset_y/self.scale_y)
        #self.canvas.translate((+w2 / self.scale_x), (+h2 / self.scale_y))
        #self.canvas.translate(165, 165)

        self.display_letters(0, 0, self.cwidth, self.cheight,
                                self.letters, 0)

        #self.canvas.setLineWidth(1)
        #self.canvas.setStrokeStyle(Color("#f00"))
        #self.canvas.strokeRect(self.offset_x, self.offset_y, x1-1, y1-1)

        self.canvas.restoreContext()

        print self.closest

    def sr(self, x, y, w, h):
        #sw = (self.cwidth/2/self.scale_x)
        #sh = (self.cheight/2/self.scale_y)
        sw = self.cwidth/2
        sh = self.cheight/2
        rect = (-sw*self.scale_x+(x+(-self.offset_x+sw/self.scale_x))*self.scale_x,
                -sh*self.scale_y+(y+(-self.offset_y+sh/self.scale_x))*self.scale_y,
                w*self.scale_x,
                h*self.scale_y)
        print "rect", x,y,w,h, rect
        return rect

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

    def get_closest(self, px, py, pwidth, pheight, letters):

        if not letters:
            return

        length = len(letters)
        oy = 0
        for i, letter in enumerate(letters):
            height = letter.weight * pheight
            width  = letter.weight * pwidth
            letter.x = int(px+(pwidth-width))
            letter.y = int(py+oy)
            letter.box_width = width
            letter.box_height = height
            self.get_closest(letter.x, letter.y,
                                 width, height,
                                 letter)
            self.check_closest(letter,
                            self.offset_x + (self.cwidth/2), #* self.scale_x,
                            self.offset_y + (self.cheight/2) )#* self.scale_y)
            oy += height

    def display_letters(self, px, py, pwidth, pheight, letters, colouridx):

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
        self.canvas.fillRect(x, y, w, h)

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
            self.canvas.saveContext()
            self.canvas.setFillStyle(Color("#000"))
            x, y, w, h = self.sr(letter.x, int(py+(oy+height/2+5)), pwidth, pheight)
            self.canvas.fillText(letter.letter, x, y)
            oy += height


if __name__ == '__main__':
    pyjd.setup("./index.html")
    d = Dash()
    pyjd.run()

