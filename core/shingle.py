# -*- coding: utf-8 -*-
import binascii
from settings import SHINGLE_LENGTH

class Shingles:

    @staticmethod
    def generate(source):
        out = []
        for i in range(len(source)-(SHINGLE_LENGTH-1)):
            out.append(binascii.crc32(' '.join( [x for x in source[i:i+SHINGLE_LENGTH]] ).encode('utf-8')))

        return out

    def compare (self, source1, source2):
        same = 0
        for i in range(len(source1)):
            if source1[i] in source2:
                same = same + 1

        return same*2/float(len(source1) + len(source2))*100