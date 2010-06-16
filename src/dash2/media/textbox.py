from pyjamas.ui.TextArea import TextArea 
from pyjamas.ui import KeyboardListener
from pyjamas.log import writebr
from pyjamas import DOM
from pyjamas import DeferredCommand

KEY_MAP = { '.': 190,
            ',': [44, 188]
          }

class T9TextArea(TextArea):

    def __init__(self, sink, available_keys, **kwargs):
        TextArea.__init__(self, **kwargs)
        self.addKeyboardListener(self)
        self.setAvailableKeys(available_keys)
        self.sink = sink

    def setAvailableKeys(self, available_keys):
        self.available_keys = []
        for k in available_keys:
            k = KEY_MAP.get(k, ord(k))
            if isinstance(k, list):
                self.available_keys += k
            else:
                self.available_keys.append(k)

    def checkKey(self, sender, keycode, modifiers):
        DeferredCommand.add(self.sink)
        if int(keycode) in KeyboardListener.KEYS:
            #print "nope", keycode, KeyboardListener.KEYS
            return
        #print type(keycode), type(self.available_keys[0])
        if int(keycode) not in self.available_keys:
            #print "stop", keycode, self.available_keys
            event = DOM.eventGetCurrentEvent()
            DOM.eventPreventDefault(event)
            return

    def onKeyPress(self, sender, keycode, modifiers = None):
        self.checkKey(sender, keycode, modifiers)
        
    def onKeyDown(self, sender, keycode, modifiers = None):
        self.checkKey(sender, keycode, modifiers)

    def onKeyUp(self, sender, keycode, modifiers = None):
        pass

