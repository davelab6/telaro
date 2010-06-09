from pyjamas.ui.Button import Button
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.FocusListener import FocusHandler
from pyjamas.ui.Focus import FocusMixin
from pyjamas.ui import Focus 

from pyjamas import log

rows = ["'`1234567890-=",
        "qwertyuiop[]",
        "asdfghjkl;'#",
        "\zxcvbnm,./",
        " "]

class Qwerty(FlexTable, FocusHandler, FocusMixin):

    def __init__(self,  **kwargs):
        FlexTable.__init__(self, **kwargs)
        FocusHandler.__init__(self)
        self.buttons = {}
        fmt = self.getFlexCellFormatter()
        for i, row in enumerate(rows):
            for j, letter in enumerate(row):
                if letter == ' ':
                    l = '&nbsp;'
                else:
                    l = letter
                button = Button(l, self, StyleName="kbdbutton")
                self.buttons[letter] = button
                self.setWidget(i, j, button)
                if letter == ' ':
                    fmt.setColSpan(i, j, 5)
                    button.addStyleName("kbdbuttonspace")

    def onClick(self, button):
        log.writebr(button.getHTML())

    def activate(self, selection):
        for (letter, button) in self.buttons.items():
            active = letter in selection
            button.setEnabled(active)
            if active:
                button.removeStyleName("kbdbuttondisabled")
                button.addStyleName("kbdbuttonenabled")
            else:
                button.removeStyleName("kbdbuttonenabled")
                button.addStyleName("kbdbuttondisabled")
