# -*- coding: utf-8 -*-
import collections
import binascii

class Keywords:

    @staticmethod
    def get_weights(list):
        res = {}
        collection = collections.Counter(list)
        num_words = len(collection)
        for keyword, number in collection:
            res[keyword]['number'] = number
            res[keyword]['crc32_hash'] = binascii.crc32(keyword)
            res[keyword]['weight'] = number/num_words
        return res
