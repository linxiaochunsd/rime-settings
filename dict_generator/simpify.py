import os
import time
import re

from fontTools.ttLib import TTFont
import opencc

global_phrase_map = dict()

font_list = [
    ('/System/Library/Fonts/STHeiti Light.ttc', 2),
    #          '/System/Library/Fonts/STHeiti Light.ttc',
    ('/System/Library/Fonts/PingFang.ttc', 36)
    # '/System/Library/Fonts/Hiragino Sans GB.ttc',
    # '/System/Library/Fonts/AppleSDGothicNeo.ttc',
]



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



def scan_dict(dict_file):
    phrase_map = dict()
    with open(dict_file, "r") as src:
        while True:
            line = src.readline()
            if not line:
                break
            line = line.strip()
            if is_header(line):
                continue
            splits = line.split()
            if len(splits) < 1:
                continue

            ori_phrase = splits[0]

            if len(ori_phrase) <= 1:
                continue
            phrase = T2S.convert(ori_phrase)
            if miss_font(phrase):
                continue
            if phrase in global_phrase_map:
                continue
            phrase_map[phrase] = True
            global_phrase_map[phrase] = True


    return phrase_map


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
    version = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    with open("../"+dict_name + ".dict.yaml", "w") as dict_f:
        header = f"""---
name: {dict_name}
version: {version}
sort: by_weight
use_preset_vocabulary: false
...
"""
        dict_f.write(header)


        for phrase in phrase_map:

            dict_f.writelines(phrase + "\n")



if __name__ == "__main__":
    # test()

    independent_dict_files = [
        "luna_pinyin.place.dict.yaml",
        "luna_pinyin.poetry.dict.yaml",
        "luna_pinyin.chengyusuyu.dict.yaml",
    ]

    phrases = scan_dict("../essay-zh-hans.txt")
    for dict_file in independent_dict_files:
        phrases = scan_dict(dict_file)
        file_name_splits = dict_file.split('.')
        if len(file_name_splits) == 4:
            name = file_name_splits[1]
        else:
            name = file_name_splits[0]
        output(phrases,name)


    popular_dict_files = [
        "luna_pinyin.xiandaihanyu.dict.yaml",
        "luna_pinyin.popular.dict.yaml",
        "luna_pinyin.mingxing.dict.yaml",
        "luna_pinyin.dict.yaml",
        "luna_pinyin.chat.dict.yaml",

    ]
    popular_dict = dict()
    for dict_file in popular_dict_files:
        phrases = scan_dict(dict_file)
        popular_dict.update(phrases)
    output(popular_dict,"popular")


    it_dict_files=[
        "luna_pinyin.computer.dict.yaml",
        "luna_pinyin.website.dict.yaml",
        "luna_pinyin.kaifa.dict.yaml",
    ]
    it_dict = dict()
    for dict_file in it_dict_files:
        phrases = scan_dict(dict_file)
        it_dict.update(phrases)
    output(it_dict,"it")