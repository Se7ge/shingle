# -*- coding: utf-8 -*-

from pymorphy import get_morph
morphy = get_morph('dicts')

class Parser:
     
    def parse(self, string):
        if string:
	    string = self.clear_tags(string)
	    words_tuple = self.canonize(string)
        return words_tuple 

    def clear_tags(self, string):
        return string

    def canonize(self, string):
        stop_symbols = self.get_stopsymbols()
	stop_words = self.get_stopwords()
        return ( [x for x in [self.morphy_process(y.strip(stop_symbols)) for y in string.upper().split()] if x and (x not in stop_words)] )

    def get_stopwords(self):
        return (,)

    def get_stopsymbols(self):
        return '.,!?:;-\n\r()'

    def morphy_process(self, string):
        return morphy.normalize(string)
