# -*- coding: utf-8 -*-

def levenshtein(seq1, seq2):
    """Adapted from
    <http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python>
    and is licensed under <http://creativecommons.org/licenses/by-sa/3.0/> license.
    """
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]
