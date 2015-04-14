import random

def mark_v_shaney(text, size):
    assert size > 0
    link, term = build_links(text)
    assert size < len(term)
    mark = build_chain(size, link, term)
    return mark

def build_links(text):
    words = text.split()
    link = {}
    term = []
    for index in range(len(words) - 2):
        a, b, c = words[index:index+3]
        key = a, b
        if key in link:
            value = link[key]
            if c not in value:
                value.append(c)
        else:
            link[key] = [c]
        if b[-1] in list('.?!'):
            if key not in term:
                term.append(key)
    if c[-1] in list('.?!'):
        key = b, c
        if key not in term:
            term.append(key)
    return link, term

def build_chain(size, link, term):
    key = random.choice(term)
    cache = []
    buffer = []
    while True:
        if key in link:
            word = random.choice(link[key])
            buffer.append(word)
            key = key[1], word
            if key in term:
                sentence = ' '.join(buffer)
                if sentence not in cache:
                    cache.append(sentence)
                    if len(cache) == size:
                        return ' '.join(cache)
                buffer = []
        else:
            key = random.choice(term)

TEXT = open("GPL-3").read()
COUNT = 10

if __name__ == '__main__':
    import textwrap
    print (textwrap.fill(mark_v_shaney(TEXT,int(COUNT)), 80))
