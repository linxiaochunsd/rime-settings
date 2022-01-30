from fontTools.ttLib import TTFont
import opencc

assistant_map = dict()


def bad_font_filter():
    font = TTFont(file='/System/Library/Fonts/STHeiti Light.ttc', fontNumber=0)
    # print(font['cmap'].__dict__)
    unicode_map = font['cmap'].tables[0].ttFont.getBestCmap()
    glyf_map = font['glyf']
    dic_list = [
        "zrm2000.dict.yaml",
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

    t2s = opencc.OpenCC('t2s.json')
    s2t = opencc.OpenCC('s2t.json')
    for dic in dic_list:
        o = open("output/" + dic + ".tmp", "a")
        with open(dic, "r") as f:
            for line in f.readlines():
                #        print("ok",ok,"bad",bad,"line:",line)
                splits = line.split()
                if len(splits) == 0:
                    o.writelines(line)
                    continue
                words = splits[0]
                isbad = False
                for word in words:
                    if not (ord(word) in unicode_map and len(
                            glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                        print("ok", ok, "bad", bad, "line:", line, words)
                        bad += 1
                        isbad = True
                        break

                if not isbad:
                    words = s2t.convert(words)
                    for word in words:
                        if not (ord(word) in unicode_map and len(
                                glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                            print("ok", ok, "bad", bad, "line:", line, words)
                            bad += 1
                            isbad = True
                            break
                if not isbad:
                    words = t2s.convert(words)
                    for word in words:
                        if not (ord(word) in unicode_map and len(
                                glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                            print("ok", ok, "bad", bad, "line:", line, words)
                            bad += 1
                            isbad = True
                            break
                if not isbad:
                    o.writelines(line)
                    ok += 1


def copy_header(src, dst):
    comment_end = False
    line = True
    while line:
        line = src.readline()
        if line.startswith("#"):
            dst.writelines(line)
            continue
        if not comment_end:
            dst.writelines(line)
        if line.find("...") >= 0:
            comment_end = True
        if comment_end:
            break


def single_char_filter():

    with open("output/zrm2000.dict.yaml.tmp", "r") as src:
        # copy_header(src, dst)
        line = True
        while line:
            line = src.readline()
            if line.find(",,") >= 0 or line.find("..") >= 0:
                continue
            splits = line.split()
            if len(splits) < 2:
                continue
            words = splits[0]
            # print("len(words)",words,len(words))
            if len(words) != 1:
                continue
            code = splits[1]
            if len(code) <= 2 or len(code) > 4:
                continue
            code = code[2:]
            if words in assistant_map:
                assistant_code = assistant_map[words]
                assistant_code.append(code)
            else:
                assistant_code = [code]
            assistant_map[words] = assistant_code
            # print("assistant_map",assistant_map)
            # dst.writelines(line)

    dic_list = [
        # "zrm2000.dict.yaml",
        # "luna_pinyin.chat.dict.yaml",
        # "luna_pinyin.chengyusuyu.dict.yaml",
        # "luna_pinyin.computer.dict.yaml",
        "luna_pinyin.dict.yaml",
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

    t2s = opencc.OpenCC('t2s.json')
    s2t = opencc.OpenCC('s2t.json')
    phrase_dst = open("output/luna_pinyin_phrase.dict.yaml", "a")
    for dic in dic_list:
        multi_char_count = 0
        dst = open("output/" + dic, "a")
        with open(dic, "r") as src:
            copy_header(src, dst)
            line = True
            while line:
                line = src.readline()
                splits = line.split()
                if len(splits) == 0:
                    dst.writelines(line)
                    continue

                words = splits[0]

                if len(words) != 1:
                    multi_char_count +=1
                    phrase_dst.writelines(line)
                    print("multi_char_count",multi_char_count)
                    continue

                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    for ac in assistant_code:
                        char_codes.append(splits[1] + ":" + ac)
                    for char_code in char_codes:
                        newline = line.replace(splits[1], char_code)
                        dst.writelines(newline)
                    continue
                print("char_codes",char_codes)
                words = s2t.convert(words)
                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    for ac in assistant_code:
                        char_codes.append(splits[1] + ":" + ac)
                    for char_code in char_codes:
                        newline = line.replace(splits[1], char_code)
                        dst.writelines(newline)
                    continue
                print("char_codes",char_codes)
                words = t2s.convert(words)
                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    for ac in assistant_code:
                        char_codes.append(splits[1] + ":" + ac)
                    for char_code in char_codes:
                        newline = line.replace(splits[1], char_code)
                        dst.writelines(newline)
                    continue
                print("char_codes",char_codes)
                # dst.writelines(line)

def reverse_lookup():

    with open("output/zrm2000.dict.yaml.tmp", "r") as src:
        # copy_header(src, dst)
        line = True
        while line:
            line = src.readline()
            if line.find(",,") >= 0 or line.find("..") >= 0:
                continue
            splits = line.split()
            if len(splits) < 2:
                continue
            words = splits[0]
            # print("len(words)",words,len(words))
            if len(words) != 1:
                continue
            code = splits[1]
            if len(code) != 4:
                continue
            code = code[2:]
            if words in assistant_map:
                assistant_code = assistant_map[words]
                assistant_code.append(code)
            else:
                assistant_code = [code]
            assistant_map[words] = assistant_code
            # print("assistant_map",assistant_map)
            # dst.writelines(line)

    dic_list = [
        # "zrm2000.dict.yaml",
        # "luna_pinyin.chat.dict.yaml",
        # "luna_pinyin.chengyusuyu.dict.yaml",
        # "luna_pinyin.computer.dict.yaml",
        "luna_pinyin.dict.yaml",
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

    t2s = opencc.OpenCC('t2s.json')
    s2t = opencc.OpenCC('s2t.json')
    # phrase_dst = open("output/luna_pinyin_phrase.dict.yaml", "a")
    for dic in dic_list:
        multi_char_count = 0
        dst = open("output/assistant_reverse.dict.yaml", "a")
        with open(dic, "r") as src:
            copy_header(src, dst)
            line = True
            while line:
                line = src.readline()
                splits = line.split()
                if len(splits) == 0:
                    dst.writelines(line)
                    continue

                words = splits[0]

                if len(words) != 1:
                    multi_char_count +=1
                    # phrase_dst.writelines(line)
                    print("multi_char_count",multi_char_count)
                    continue

                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    quanpin = splits[1]
                    quanpin.replace("iu","q")
                    quanpin.replace("ia","w")
                    quanpin.replace("ua","w")
                    quanpin.replace("uan","r")
                    quanpin.replace("er","r")
                    quanpin.replace("ve","t")
                    quanpin.replace("uai","y")
                    quanpin.replace("v","y")

                    quanpin.replace("uang","d")
                    quanpin.replace("iang","d")

                    for ac in assistant_code:
                        char_codes.append(splits[1] + ":" + ac)
                    for char_code in char_codes:
                        newline = line.replace(splits[1], char_code)
                        dst.writelines(newline)
                    continue
                print("char_codes",char_codes)
                words = s2t.convert(words)
                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    for ac in assistant_code:
                        char_codes.append(splits[1] + ":" + ac)
                    for char_code in char_codes:
                        newline = line.replace(splits[1], char_code)
                        dst.writelines(newline)
                    continue
                print("char_codes",char_codes)
                words = t2s.convert(words)
                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    for ac in assistant_code:
                        char_codes.append(splits[1] + ":" + ac)
                    for char_code in char_codes:
                        newline = line.replace(splits[1], char_code)
                        dst.writelines(newline)
                    continue
                print("char_codes",char_codes)
                # dst.writelines(line)

if __name__ == "__main__":
    # bad_font_filter()
    single_char_filter()
    # reverse_lookup()