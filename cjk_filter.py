from fontTools.ttLib import TTFont

font = TTFont(file='/System/Library/Fonts/STHeiti Light.ttc',fontNumber=1)
# print(font['cmap'].__dict__)
unicode_map = font['cmap'].tables[0].ttFont.getBestCmap()
glyf_map = font['glyf']
dic_list = [
    "essay.txt",
    # "luna_pinyin.chat.dict.yaml",
    # "luna_pinyin.chengyusuyu.dict.yaml",
    # "luna_pinyin.computer.dict.yaml",
    # "luna_pinyin.dict.yaml",
    # "luna_pinyin.extended.dict.yaml",
    # "luna_pinyin.kaifa.dict.yaml",
    # "luna_pinyin.mingxing.dict.yaml",
    # "luna_pinyin.place.dict.yaml",
    # "luna_pinyin.poetry.dict.yaml",
    # "luna_pinyin.popular.dict.yaml",
    # "luna_pinyin.website.dict.yaml",
    # "luna_pinyin.xiandaihanyu.dict.yaml",
    # "zhwiki.dict.yaml",
]
ok = 0
bad = 0
import opencc
t2s = opencc.OpenCC('t2s.json')
s2t = opencc.OpenCC('s2t.json')
for dic in dic_list:
    o = open("output/"+dic,"a")
    comment_end=False
    with open(dic,"r") as f:
        for line in f.readlines():
    #        print("ok",ok,"bad",bad,"line:",line)
            splits = line.split()
            if len(splits) == 0:
                o.writelines(line)
                continue
            words = splits[0]
            isbad = False
            for word in words:
                if not (ord(word) in unicode_map and len(glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                    print("ok",ok,"bad",bad,"line:",line, words)
                    bad += 1
                    isbad = True
                    break

            if not isbad:
                words = t2s.convert(words)
                for word in words:
                    if not (ord(word) in unicode_map and len(glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                        print("ok",ok,"bad",bad,"line:",line, words)
                        bad += 1
                        isbad = True
                        break
            if not isbad:
                words = s2t.convert(words)
                for word in words:
                    if not (ord(word) in unicode_map and                                len(glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                        print("ok",ok,"bad",bad,"line:",line, words)
                        bad += 1
                        isbad = True
                        break
            if not isbad:
                o.writelines(line)
                ok += 1
