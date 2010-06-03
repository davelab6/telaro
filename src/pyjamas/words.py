""" turn words into a LetterNode tree.
"""

from lettertree import LetterNode, pprint_letters

words = "fifish fill fillip filo filths fist fists fit fits flop flosh foil foolship foothill foothills foots footstools fop fops fopship fplot hi hills hilltop hilts hip hippolith his hiss hit hits holloos hoofs hoopoo hoopoos hoops hop hops hot hotfoot hotfoots if ills is islot it lill liposis lips lit lithophthisis lithosols loft loo loot lost lot loth lotto of off offshoot oh oil oilish olio oof ooh ooliths ophiophilist opposit ostitis otolith otoliths ototoi phi phillippi phillis philophilosophos philosophist phoss photolith photolitho phots pip pipit piss pit pithos plops plot plots polit polloi polo poloist poof pooh poohpoohist poops pops posh posthitis postil postposit pot potoo potshoot psiloi psilosis psoitis sfoot shilloo shools shop shoplift shoplifts sifflot silo sip sips sis sit slipslop slipsloppish sloops sloosh slop slopshop slot so soffits solipsists solist soosoo sooths sootish sop sophists sophs sos sot sotol sots spiff spill spiss spit split spoil spoilt spoof spoofish stiffish stills stilts stoop stoot stop this thistlish thitsiol thlipsis tholli tiff til tilt tip tipi tiptoppish tiptops tis titlists tits to too tool toolsi toot tooth top topoi tops topsl tosspot tots".split(" ")

#words = "fred frederick fried".split(" ")

def assign_equal_weight(letters):
    length = len(letters)
    if length == 0:
        return
    weight = 1.0 / length
    for l in letters:
        l.weight = weight
        assign_equal_weight(l)

def get_test_letters():
    res = []
    for w in words:
        p = res
        for l in w:
            try:
                idx = p.index(l)
                p = p[idx]
            except ValueError:
                ln = LetterNode(l, 0.0)
                p.append(ln)
                p = ln
        p.append(LetterNode(" ", 0.0))
        p.append(LetterNode(",", 0.0))
        p.append(LetterNode(".", 0.0))

    assign_equal_weight(res)

    return res

if __name__ == '__main__':
    l = get_test_letters()
    pprint_letters(l)
