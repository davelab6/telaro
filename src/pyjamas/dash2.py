import pyjd

from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.RootPanel import RootPanel

from letter import Letters

class Dash:

    def __init__(self):

        self.p = AbsolutePanel(Width="100%", Height="100%",
                               StyleName="dashpanel")
        RootPanel().add(self.p)

        test_letters = {}
        num_chars = 26
        for i in range(65, num_chars+65):
            test_letters[chr(i)] = (1.0 / num_chars)

        self.letters = Letters(self.p, test_letters)

if __name__ == '__main__':
    pyjd.setup("./index.html")
    d = Dash()
    pyjd.run()

