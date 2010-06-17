""" turn words into a LetterNode tree.
"""

from lettertree import LetterNode, pprint_letters

words = "fifish fill fillip filo filths fist fists fit fits flop flosh floss foil foils foolship foothill foothills foots footstools fop fops fopship fplot hi hills hilltop hilts hip hippolith his hiss hit hits holloos hoofs hoopoo hoopoos hoops hop hops hot hotfoot hotfoots if ills is islot it lill liposis lips lit lithophthisis lithosols loft lift lifts loo loot lost lot lots loth lotto of off offshoot oh oil oilish olio oof ooh ooliths ophiophilist opposit ostitis otolith otoliths ototoi phi phillippi phillis philophilosophos philosophist phoss photolith photolitho phots pip pipit piss pit pithos plops plot plots polit polloi polo poloist poof pooh poohpoohist poops pops posh posthitis postil postposit pot potoo potshoot psiloi psilosis psoitis sfoot shilloo shools shop shoplift shoplifts sifflot silo sip sips sis sit slipslop slipsloppish sloops sloosh slop slopshop slot so soffits solipsists solist soosoo sooths sootish sop sophists sophs sos sot sotol sots spiff spill spiss spit split spoil spoilt spoof spoofish stiffish stills stilts stoop stoot stop this thistlish thitsiol thlipsis tholli tiff til tilt tip tipi tiptoppish tiptops tis titlists tits to too tool toolsi toot tooth top topoi tops topsl tosspot tots".split(" ")

words.sort()

#words = "golf fred frederick fried".split(" ")

def assign_equal_weight(letters):
    length = len(letters)
    if length == 0:
        return
    weight = 1.0 / length
    for l in letters:
        l.weight = weight
        assign_equal_weight(l)

def recurse_sort(letters):
    letters.sort()
    for l in letters:
        recurse_sort(l)

def get_test_words():
    global words
    return words

def get_letter_chain(words):
    res = []
    for w in words:
        p = res
        for l in w:
            found = False
            for idx, pl in enumerate(p):
                if l == pl.letter:
                    p = pl
                    found = True
                    break
            if not found:
                ln = LetterNode(l, 0.0, parent=p)
                p.append(ln)
                p = ln
        comma = LetterNode(",", 0.0, parent=p)
        dot = LetterNode(".", 0.0, parent=p)
        space = LetterNode(" ", 0.0, parent=p)
        p.append(space)
        p.append(dot)
        p.append(comma)
        dot.append(LetterNode(" ", 0.0, parent=p))
        comma.append(LetterNode(" ", 0.0, parent=p))

    assign_equal_weight(res)
    recurse_sort(res)

    return res

if __name__ == '__main__':
    l = get_test_letters(get_test_words())
    pprint_letters(l)
