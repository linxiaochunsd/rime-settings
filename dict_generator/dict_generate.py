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


# font_list = []
# g = os.walk("/Users/linxiaochun/Downloads/简体中文")
#
#
# for path, dir_list, file_list in g:
#     for file_name in file_list:
#         if file_name.endswith("ttc") or file_name.endswith("ttf"):
#             font_list.append(os.path.join(path, file_name))
# print(font_list)
#
# phonetic_symbol = {
#     "ā": "a1",
#     "á": "a2",
#     "ǎ": "a3",
#     "à": "a4",
#
#     "ē": "e1",
#     "é": "e2",
#     "ě": "e3",
#     "è": "e4",
#
#     "ō": "o1",
#     "ó": "o2",
#     "ǒ": "o3",
#     "ò": "o4",
#
#     "ī": "i1",
#     "í": "i2",
#     "ǐ": "i3",
#     "ì": "i4",
#
#     "ū": "u1",
#     "ú": "u2",
#     "ǔ": "u3",
#     "ù": "u4",
#
#     # üe
#     "ü": "v",
#     "ǖ": "v1",
#     "ǘ": "v2",
#     "ǚ": "v3",
#     "ǜ": "v4",
#
#     "ń": "n2",
#     "ň": "n3",
#     "ǹ": "n4",
#
#     "m̄": "m1",  # len('m̄') == 2
#     "ḿ": "m2",
#     "m̀": "m4",  # len("m̀") == 2
#
#     "ê̄": "ê1",  # len('ê̄') == 2
#     "ế": "ê2",
#     "ê̌": "ê3",  # len('ê̌') == 2
#     "ề": "ê4",
# }

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


class Pronunciation(object):
    def __init__(self, p):
        self.p = p
        self.stats = 0
        self.phrases = dict()

    def add_phrase(self, phrase, stats):
        if phrase in self.phrases:
            return
        self.phrases[phrase] = True
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

    def add_phrase(self, pinyin, phrase, stats):
        if pinyin not in self.pinyins:
            self.pinyins[pinyin] = Pronunciation(pinyin)
        self.pinyins[pinyin].add_phrase(phrase, stats)

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
                    freq = "\t%.2f%%" % (self.pinyins[pinyin].stats / total_num * 100)
            doubles = converter(pinyin)
            for double in doubles:
                if len(double) != 2:
                    continue
                line = self.char + "\t" + double
                doubles_res.append(line + freq + "\n")
                for ac in self.assis_codes:
                    double_assists_res.append(line + ":" + ac.upper() + "\t-1" + "\n")

        return doubles_res, double_assists_res


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


def get_pinyin(phrase):
    pinyins = Pinyin(phrase, heteronym=False, style=Style.NORMAL, errors=returnEmpty)
    for pinyin in pinyins:
        for i in range(len(pinyin)):
            #有些拼音有问题, 需要修正一下
            if re.compile("[^\w]+").search(pinyin[i]) is not None:
                pinyin[i] = re.sub("[^\w]+", "", pinyin[i])
                print(phrase, pinyin)

    return pinyins


class CharSet(object):
    mapping = dict()

    def __init__(self):
        pass

    def add_single_char(self, char, pinyin, stats):
        # if char == "聂":
        #     print(char,pinyin,stats)
        if pinyin == "":
            return
        if char not in self.mapping:
            self.mapping[char] = Char(char, stats)
        else:
            self.mapping[char].set_stats(stats)
        self.mapping[char].new_pinyin(pinyin)

    def add_phrase_char(self, char, pinyin, phrase, stats):
        # if char == "聂":
        #     print(char,pinyin,stats)
        if pinyin == "":
            return
        if char not in self.mapping:
            self.mapping[char] = Char(char, 0)

        self.mapping[char].add_phrase(pinyin, phrase, stats)

    def add_ass_code(self, char, assis_code):
        if char in self.mapping:
            self.mapping[char].add_ass_code(assis_code)

    def find(self, char):
        if char not in self.mapping:
            return None

        doubles, double_assists = self.mapping[char].output()
        print(self.mapping[char].char, self.mapping[char].stats)
        for pinyin in self.mapping[char].pinyins:
            print(pinyin, self.mapping[char].pinyins[pinyin].stats, self.mapping[char].pinyins[pinyin].phrases.items())
        print(self.mapping[char].assis_codes.items())

        return doubles, double_assists

    def output(self, dict_name, rarelay_used=False):
        version = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        doubles_f = open("../"+dict_name + ".dict.yaml", "w")
        header = f"""---
name: {dict_name}
version: {version}
sort: by_weight
use_preset_vocabulary: false
...
"""
        doubles_f.write(header)

        dict_name += ".assist"
        double_assists_f = open("../"+dict_name + ".dict.yaml", "w")
        header = f"""---
name: {dict_name}
version: {version}
sort: by_weight
use_preset_vocabulary: false
...
"""
        double_assists_f.write(header)

        for c in self.mapping:
            # print(c,self.mapping[c])
            doubles, double_assists = self.mapping[c].output(rarelay_used)
            doubles_f.writelines(doubles)
            double_assists_f.writelines(double_assists)

    def scan_essay(self, dict_file):
        with open(dict_file, "r") as src:
            while True:
                line = src.readline()
                if not line:
                    break
                # if is_header(line):
                #     continue
                splits = line.split()
                if len(splits) < 2:
                    continue
                ori_phrase = splits[0]
                phrase = T2S.convert(ori_phrase)
                if miss_font(phrase):
                    continue
                stats = int(splits[1])
                if len(phrase) == 1:  # 单字
                    char = phrase
                    pinyins = get_pinyin(char)[0]

                    for pinyin in pinyins:
                        self.add_single_char(char, pinyin, stats)
                    continue

                pinyins = get_pinyin(phrase)

                for i in range(len(phrase)):
                    char = phrase[i]
                    char_pinyins = pinyins[i]
                    for char_pinyin in char_pinyins:
                        self.add_phrase_char(char, char_pinyin, phrase, stats)

    def scan_dict(self, dict_file):
        with open(dict_file, "r") as src:
            while True:
                line = src.readline()
                if not line:
                    break
                if is_header(line):
                    continue
                splits = line.split()
                if len(splits) < 2:
                    continue

                ori_phrase = splits[0]
                phrase = T2S.convert(ori_phrase)
                if miss_font(phrase):
                    continue
                stats = 0
                if len(phrase) == 1:  # 单字
                    char = phrase
                    pinyins = get_pinyin(char)[0]

                    for pinyin in pinyins:
                        self.add_single_char(char, pinyin, stats)
                    continue

                pinyins = get_pinyin(phrase)

                for i in range(len(phrase)):
                    char = phrase[i]
                    char_pinyins = pinyins[i]
                    for char_pinyin in char_pinyins:
                        self.add_phrase_char(char, char_pinyin, phrase, stats)

    def add_all_assis_codes(self, dict_file):
        with open(dict_file, "r") as src:
            while True:

                line = src.readline()
                if not line:
                    break
                if is_header(line):
                    continue
                splits = line.split()
                if len(splits) < 2:
                    continue

                ori_phrase = splits[0]
                phrase = T2S.convert(ori_phrase)
                if miss_font(phrase):
                    continue

                if len(phrase) == 1:  # 单字
                    char = phrase
                    double_assist = splits[1]
                    assist_code = double_assist[2:]
                    if len(assist_code) < 2:  # 只区全码
                        continue
                    if char == "聂":
                        print("聂", line)
                    self.add_ass_code(char, assist_code)
                    continue


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


def test():
    font = TTFont('/System/Library/Fonts/PingFang.ttc')
    print("font", font)
    exit(0)


if __name__ == "__main__":
    # test()
    test = ".test"
    test = ""
    essay_file = "../essay-zh-hans.txt" + test
    dict_file = "luna_pinyin.dict.yaml" + test
    zrm_file = "zrm2000.dict.yaml" + test

    # print(FontFilter(font_file)("𩽾𩾌"))
    # exit(0)

    charset = CharSet()
    charset.scan_essay(essay_file)
    charset.scan_dict(dict_file)
    charset.add_all_assis_codes(zrm_file)

    print(charset.find("聂"))
    print(charset.find("乤"))
    print(charset.find("𩽾"))
    # print(charset.find("家"))
    # print(charset.find("大"))

    charset.output("my_own")
    # charset.output("my_own_rarely_used", rarelay_used=True)
    # nie="聂"
    # out = FontFilter(font_file)(nie)
    # print("out",out)
