from pyjamas.ui.TextArea import TextArea 
from pyjamas.ui import KeyboardListener
from pyjamas.log import writebr
from pyjamas import DOM

KEY_MAP = { '.': 190,
            ',': [44, 188]
          }

class T9TextArea(TextArea):

    def __init__(self, available_keys, **kwargs):
        TextArea.__init__(self, **kwargs)
        self.available_keys = []
        for k in available_keys:
            k = KEY_MAP.get(k, ord(k))
            if isinstance(k, list):
                self.available_keys += k
            else:
                self.available_keys.append(k)

        self.available_keys.append(44)
        self.addChangeListener(self)
        self.addKeyboardListener(self)

    def onChange(self, sender):
        pass

    def checkKey(self, sender, keycode, modifiers):
        if int(keycode) in KeyboardListener.KEYS:
            print "nope", keycode, KeyboardListener.KEYS
            return
        print type(keycode), type(self.available_keys[0])
        if int(keycode) not in self.available_keys:
            print "stop", keycode, self.available_keys
            event = DOM.eventGetCurrentEvent()
            DOM.eventPreventDefault(event)
        
    def onKeyPress(self, sender, keycode, modifiers = None):
        self.checkKey(sender, keycode, modifiers)
        
    def onKeyDown(self, sender, keycode, modifiers = None):
        self.checkKey(sender, keycode, modifiers)

    def onKeyUp(self, sender, keycode, modifiers = None):
        pass
        #self.checkKey(sender, keycode, modifiers)

