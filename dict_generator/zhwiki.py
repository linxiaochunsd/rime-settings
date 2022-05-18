import itertools
import os
import time
import re

from fontTools.ttLib import TTFont
import opencc
from pypinyin import Style
from pypinyin import pinyin as Pinyin
from pypinyin_dict.pinyin_data import zdic

zdic.load()

def returnEmpty(chars):
    return [""]


phrase_frequent_map = dict()

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
    "derive/T$/V/",
    "xform/(.)ou$/$1B/",
    "xform/in$/N/",
    "xform/ing$/;/",
]

sep = ":"

font_list = [
    ('/System/Library/Fonts/STHeiti Light.ttc', 2),
    #          '/System/Library/Fonts/STHeiti Light.ttc',
    ('/System/Library/Fonts/PingFang.ttc', 36)
    # '/System/Library/Fonts/Hiragino Sans GB.ttc',
    # '/System/Library/Fonts/AppleSDGothicNeo.ttc',

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


class Pronunciation(object):
    def __init__(self, p):
        self.p = p
        self.stats = 0
        self.phrases = dict()

    def add_phrase(self, phrase, stats, pinyins):

        if phrase in self.phrases:
            return
        self.phrases[phrase] = pinyins
        self.stats += stats


class Char(object):

    def __init__(self, char, stats):
        self.char = char
        self.stats = stats
        self.pinyins = dict()
        self.assis_codes = {}

    def new_pinyin(self, pinyin):
        if pinyin in self.pinyins:
            return
        else:
            self.pinyins[pinyin] = Pronunciation(pinyin)

    def set_stats(self, stats):
        if self.stats < stats:
            self.stats = stats

    def add_phrase(self, pinyin, phrase, stats, pinyins):
        if pinyin not in self.pinyins:
            self.pinyins[pinyin] = Pronunciation(pinyin)
        self.pinyins[pinyin].add_phrase(phrase, stats, pinyins)

    def add_ass_code(self, assis_code):
        self.assis_codes[assis_code] = True

    def double_pinyins(self):
        ds = []
        for pinyin in self.pinyins:
            ds.append(converter(pinyin))
        return ds

    def output(self, rarely_used=False):
        # print(self.char,self.pinyins.items(),self.assis_codes.items())
        total_num = 0
        rarely_limit = 10
        doubles_res = []
        double_assists_res = []
        fix_phrases = []

        # if rarely_used and self.stats > rarely_limit:
        #     return doubles_res, double_assists_res
        # if (not rarely_used) and self.stats <= rarely_limit:
        #     return doubles_res, double_assists_res
        for pinyin in self.pinyins:
            total_num += self.pinyins[pinyin].stats

        for pinyin in self.pinyins:

            freq = ""
            if len(self.pinyins) > 1:
                if total_num == 0:
                    freq = "\t%.2f%%" % (1 / len(self.pinyins) * 100)
                else:
                    freq_ratio = self.pinyins[pinyin].stats / total_num
                    if freq_ratio < 0.1:
                        for phrase in self.pinyins[pinyin].phrases:
                            dss = phrase_converter(self.pinyins[pinyin].phrases[phrase])
                            for ds in dss:
                                phrase_double = " ".join(ds)
                                fix_phrases.append(phrase +"\t"+phrase_double + "\n")
                    freq = "\t%.2f%%" % (self.pinyins[pinyin].stats / total_num * 100)
            doubles = converter(pinyin)
            for double in doubles:
                if len(double) != 2:
                    continue
                line = self.char + "\t" + double
                doubles_res.append(line + freq + "\n")
                for ac in self.assis_codes:
                    double_assists_res.append(line + ":" + ac.upper() + "\t-1" + "\n")

        return doubles_res, double_assists_res,fix_phrases


T2S = opencc.OpenCC('t2s')


class FontFilter(object):

    def __init__(self, font_file_list):
        self.font_file_list = font_file_list
        self.unicode_map = dict()
        for font_file,count in font_file_list:
            for i in range(count):
                font = TTFont(file=font_file, fontNumber=i)
                unicode_map = font['cmap'].tables[0].ttFont.getBestCmap()
                if unicode_map is not None:
                    self.unicode_map.update(unicode_map)
                print(font_file, len(self.unicode_map))
            # if "glyf" in self.font:
            #     self.glyf_map = self.font['glyf']

    def miss_font(self, chars):
        for char in chars:
            if ord(char) not in self.unicode_map:
                print(chars, "not in font")  # todo
                return True
            # if hasattr(self, 'glyf_map') and len(self.glyf_map[self.unicode_map[ord(char)]].getCoordinates(0)[0]) == 0:
            #     # print(chars, "not in font", self.font_file)  # todo
            #     return True
        return False


UnionFontFilter = FontFilter(font_list)


def miss_font(phrase):
    if UnionFontFilter.miss_font(phrase):
        return True
    return False



def scan_dict_with_pinyin(dict_file):
    res = []
    with open(dict_file, "r") as src:
        while True:
            line = src.readline()
            if not line:
                break
            if is_header(line):
                res.append(line)
                continue
            splits = line.split("\t")
            if len(splits) < 2:
                continue

            ori_phrase = splits[0]
            phrase = T2S.convert(ori_phrase)
            if miss_font(phrase):
                continue

            pinyins = splits[1].split(" ")
            doubles = phrase_converter(pinyins)

            res.append(phrase+ "\t" + doubles)
    return res




def is_header(line):
    if line.startswith("#"):
        return True
    if line.startswith("..."):
        return True
    if line.startswith("---"):
        return True
    if line.startswith("name"):
        return True
    if line.startswith("version"):
        return True
    if line.startswith("sort"):
        return True
    if line.startswith("use_preset_vocabulary"):
        return True
    if line.startswith("vocabulary"):
        return True

    return False


def output(phrase_map,dict_name):
    with open(dict_name + ".dict.yaml", "w") as dict_f:

        for phrase in phrase_map:

            dict_f.writelines(phrase)


if __name__ == "__main__":


    phrases = scan_dict_with_pinyin("zhwiki-20220416.dict.yaml")

    output(phrases,"zhwiki")
    # charset.output("my_own_rarely_used", rarelay_used=True)
    # nie="聂"
    # out = FontFilter(font_file)(nie)
    # print("out",out)
