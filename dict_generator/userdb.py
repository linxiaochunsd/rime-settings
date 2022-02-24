import itertools
import os
import time
import re

from fontTools.ttLib import TTFont
import opencc

rules = [
    "xform/^([aoe].*)$/o$1/",
    # "xform/^([ae])(.*)$/$1$1$2/",
    "xform/iu$/Q/",
    "xform/[iu]a$/W/",
    "xform/er$|[uv]an$/R/",
    "xform/[uv]e$/T/",
    "xform/v$|uai$/Y/",
    "xform/^sh/U/",
    "xform/^ch/I/",
    "xform/^zh/V/",
    "xform/uo$/O/",
    "xform/[uv]n$/P/",
    "xform/i?ong$/S/",
    "xform/[iu]ang$/D/",
    "xform/(.)en$/$1F/",
    "xform/(.)eng$/$1G/",
    "xform/(.)ang$/$1H/",
    "xform/ian$/M/",
    "xform/(.)an$/$1J/",
    "xform/iao$/C/",
    "xform/(.)ao$/$1K/",
    "xform/(.)ai$/$1L/",
    "xform/(.)ei$/$1Z/",
    "xform/ie$/X/",
    "xform/ui$/V/",
    # "derive/T$/V/",
    "xform/(.)ou$/$1B/",
    "xform/in$/N/",
    "xform/ing$/;/",
]


class DoublePinyinConverter(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    mapping = dict()

    def __init__(self, rules):
        self.rules = rules

    def __call__(self, pinyin):
        if pinyin in self.mapping:
            return self.mapping[pinyin]
        res = [pinyin]
        for r in self.rules:
            for i in range(len(res)):
                splits = r.split("/")
                pat = splits[1]
                rep_str = splits[2].replace("$", "\\")

                new_str = re.sub(pat, rep_str, res[i])
                if new_str == res[i]:
                    continue
                # print(res[i],mode, pat,rep_str,new_str)
                if r.startswith("derive"):
                    res.append(new_str)
                elif r.startswith("xform"):
                    res[i] = new_str
        for i in range(len(res)):
            res[i] = res[i].lower()
        self.mapping[pinyin] = res
        return res


converter = DoublePinyinConverter(rules)
def phrase_converter(pinyins):
    dss = []
    for p in pinyins:
        dss.append(converter(p)[0])
    return " ".join(dss)



def scan_dict(dict_file):
    res = []
    with open(dict_file, "r") as src:
        while True:
            line = src.readline()
            if not line:
                break
            line = line.strip()

            splits = line.split("\t")
            if len(splits) < 1:
                continue

            phrase = splits[0]
            if len(phrase) <= 1:
                continue
            pinyins = splits[1].split(" ")
            doubles = phrase_converter(pinyins)
            res.append(doubles+"\t"+phrase+"\tc=1 d=0.5 t=1470")

    return res



def output(phrase_map,dict_name):
    with open(dict_name + ".dict.yaml", "w") as dict_f:

        for phrase in phrase_map:

            dict_f.writelines(phrase + "\n")



if __name__ == "__main__":
    # test()

    phrases = scan_dict("bd_input_dict")
    output(phrases,"userdb")