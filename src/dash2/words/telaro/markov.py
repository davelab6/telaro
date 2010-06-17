import random

class Markov:

    def __init__(self):
        self.states = {}
        self.state_from_totals = {}

    def printout(self):
        keys = self.states.keys()
        keys.sort()
        for k in keys:
            v = self.states[k]
            print repr(k), repr(v)

    def inc_state_link(self, from_state, to_state):
        if not self.states.has_key(from_state):
            self.states[from_state] = {}
            self.state_from_totals[from_state] = 0
        if not self.states[from_state].has_key(to_state):
            self.states[from_state][to_state] = 0
        self.states[from_state][to_state] += 1
        self.state_from_totals[from_state] += 1

    def prepare(self):
        """ prepare for continuous use of get_next_state
        """
        self.state_probs = {}
        for from_k in self.states.keys():
            self.state_probs[from_k] = []
            count = 0
            for to_k in self.states[from_k].keys():
                count += self.states[from_k][to_k]
                self.state_probs[from_k].append((count, to_k))

    def get_next_state(self, from_state):
        from_d = self.states[from_state]
        from_counts = self.state_probs[from_state]
        if len(from_counts) == 0:
            return None
        (max_count, last_k) = from_counts[-1]
        rand_idx = random.randint(0, max_count)
        # ok this isn't fantastically fast...
        for (count, to_state) in from_counts:
            if count >= rand_idx:
                #print "from_state: %s rand_idx: %d to_state: %s" % (repr(from_state), rand_idx, repr(to_state)), from_counts
                return to_state
        return None
        raise "shouldn't get here"

def get_random_para_starter(starters):
    return starters[random.randint(0, len(starters)-1)]

def get_random_starter(starters, select=None):
    if select is None:
        l = len(starters)
        select = starters.keys()[random.randint(0, l-1)]
    l = len(starters[select])
    return starters[select][random.randint(0, l-1)]

def get_random_state(m):
    l = len(m.states)
    return random.randint(0, l-1)

def random_sentence(m, num_words, starters=None, para_starters=None):
    sentence = []
    if para_starters:
        state = get_random_para_starter(para_starters)
    else:
        state = m.states.keys()[get_random_state(m)]
    for w in range(num_words):
        sentence.append(state)
        prev_state = state
        try:
            state = m.get_next_state(state)
        except:
            state = None
        #print repr(state)
        #if state == '\x00':
        #    print "starter", prev_state
        if state is None:
            # re-kick-start the sentence state.
            if prev_state == '\x00':
                if para_starters:
                    sentence.append(state)
                    state = get_random_para_starter(para_starters)
                    #print "para starter", prev_state, state
                    continue
            else:
                if starters:
                    state = get_random_starter(starters)
                    continue
        if state is None:
            #print "none state"
            state = m.states.keys()[get_random_state(m)]
        else:
            if para_starters and state == '\x00':
                #print "para starter", prev_state
                sentence.append(state)
                state = get_random_para_starter(para_starters)
            #elif starters and starters.has_key(state):
            #    sentence.append(state)
            #    state = get_random_starter(starters, state)
    return sentence
    
def test():
    c = Markov()
    c.inc_state_link("hello", "there")
    c.inc_state_link("there", "friend")
    c.inc_state_link("hello", "friend")
    c.inc_state_link("friend", "of")
    c.inc_state_link("of", "mine")
    c.inc_state_link("mine", ".")
    c.inc_state_link(".", "hello")
    c.inc_state_link("mine", ",")
    c.inc_state_link(",", "how")
    c.inc_state_link("friend", "how")
    c.inc_state_link("friend", ",")
    c.inc_state_link("how", "are")
    c.inc_state_link("are", "you")
    c.inc_state_link("you", "?")
    c.inc_state_link("?", "hello")
    c.prepare()
    state = "hello"
    for i in range(30):
        print state,
        state = c.get_next_state(state)

if __name__ == '__main__':
    test()

