from pyjamas.ui.Label import Label

class Letter(Label):

    def __init__(self, panel, char, x, y, width, height, **kwargs):
        Label.__init__(self, text=char, Width=width, Height=height,
                            **kwargs)
        self.panel = panel
        self.panel.add(self, x, y)

class Letters:

    def __init__(self, panel, letter_dict):
        self.panel = panel
        self.letter_dict = letter_dict
        self.labels = {}
        y = 0
        for l in letter_dict.keys():
            self.labels[l] = Letter(self.panel, l, 500, y, 20, 20)
            y += 20

