from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.HTML import HTML
from pyjamas import DOM

class WordBox(ScrollPanel):

    def __init__(self, **kwargs):
        Width = kwargs.get("Width")
        self.table = FlowPanel(Width=Width, StyleName="wordpanel")
        ScrollPanel.__init__(self, self.table, **kwargs)
    
    def setWords(self, words):
        self.words = words
        self.createBoxes()

    def createBoxes(self):
        while self.table.getWidgetCount():
            self.table.remove(0)
        for w in self.words:
            el = DOM.createDiv()
            DOM.setStyleAttribute(el, "float", "left")
            wid = HTML(w, Element=el, 
                        StyleName="flowpanelword")
            self.table.add(wid)

    def markWords(self, wordstarter):
        for box in self.table:
            box.removeStyleName("flowpanelwordhighlight")
        for box in self.table:
            txt = box.getHTML()
            if txt.startswith(wordstarter):
                box.addStyleName("flowpanelwordhighlight")

