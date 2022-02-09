import re

from fontTools.ttLib import TTFont
import opencc

assistant_map = dict()
sep = ":"

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

    t2s = opencc.OpenCC('t2s')
    s2t = opencc.OpenCC('s2t')
    for dic in dic_list:
        o = open("output/" + dic , "w")
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

                # if not isbad:
                #     words = s2t.convert(words)
                #     for word in words:
                #         if not (ord(word) in unicode_map and len(
                #                 glyf_map[unicode_map[ord(word)]].getCoordinates(0)[0]) > 0):
                #             print("ok", ok, "bad", bad, "line:", line, words)
                #             bad += 1
                #             isbad = True
                #             break
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
                    # simp = t2s.convert(splits[0])
                    # line = line.replace(splits[0],simp)
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


def ms_zrm_assistant():

    shengmu = ["","b","p","m","f","d","t","n","l","g","k","h","j","q","x","z","c","s","zh","ch","sh","r","x","y","w"]
    yunmu = ["a","o","e","i","u","v","ai","ei","ui","ao","ou","iu","ie","ve","er","an","en","in","un","vn","ang","eng","ing","ong","ia","iao","ian","iang","iong","ua","ue","uai","uan","uang","uo"]

    quanpin_ms_shuangpin_mapping = dict()
    for s in shengmu:
        for y in yunmu:
            pinyin = s + y
            shuangpin = shuangpin_replace(pinyin)
            print(pinyin,shuangpin)
            quanpin_ms_shuangpin_mapping[pinyin] = shuangpin
    # exit(0)
    with open("output/zrm2000.dict.yaml", "r") as src:
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
            if len(code) <=3:
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

    t2s = opencc.OpenCC('t2s')
    s2t = opencc.OpenCC('s2t')
    # phrase_dst = open("output/luna_pinyin_phrase.dict.yaml", "a")
    for dic in dic_list:
        multi_char_count = 0
        dst = open("output/luna_pinyin_assistant.dict.yaml", "w")
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
                    # print("multi_char_count",multi_char_count)
                    continue

                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    quanpin = splits[1]
                    if quanpin not in quanpin_ms_shuangpin_mapping:
                        print("quanpin not in map",quanpin,line)
                        continue
                    shuangpin = quanpin_ms_shuangpin_mapping[quanpin]
                    for sp in shuangpin:
                        for ac in assistant_code:
                            char_codes.append(sp + sep + ac)
                        for char_code in char_codes:
                            newline = line.replace(splits[1], char_code)
                            dst.writelines(newline)
                    print("char_codes",char_codes)
                    continue


                words = s2t.convert(words)
                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    quanpin = splits[1]
                    if quanpin not in quanpin_ms_shuangpin_mapping:
                        print("quanpin not in map",quanpin,line)
                        continue
                    shuangpin = quanpin_ms_shuangpin_mapping[quanpin]
                    for sp in shuangpin:
                        for ac in assistant_code:
                            char_codes.append(sp + sep + ac)
                        for char_code in char_codes:
                            newline = line.replace(splits[1], char_code)
                            dst.writelines(newline)
                    print("char_codes",char_codes)
                    continue


                words = t2s.convert(words)
                if words in assistant_map:
                    assistant_code = assistant_map[words]
                    char_codes = []
                    quanpin = splits[1]
                    if quanpin not in quanpin_ms_shuangpin_mapping:
                        print("quanpin not in map",quanpin,line)
                        continue
                    shuangpin = quanpin_ms_shuangpin_mapping[quanpin]
                    for sp in shuangpin:
                        for ac in assistant_code:
                            char_codes.append(sp + sep + ac)
                        for char_code in char_codes:
                            newline = line.replace(splits[1], char_code)
                            dst.writelines(newline)
                    print("char_codes",char_codes)
                    continue

                # dst.writelines(line)
def shuangpin_replace(input):
    reg_str_list = [
        "xform/^([aoe].*)$/o$1/",
        "xform/^([ae])(.*)$/$1$1$2/",
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
    res = [input]
    for r in  reg_str_list:
        for i in range(len(res)):
            splits = r.split("/")
            mode = splits[0]
            pat = splits[1]
            rep_str = splits[2].replace("$","\\")
            # reRes = re.search(pat,res[i])
            # print("reRes",reRes)

            new_str = re.sub(pat,rep_str,res[i])
            if new_str == res[i]:
                continue
            # print(res[i],mode, pat,rep_str,new_str)
            if r.startswith("derive"):
                res.append(new_str)
            elif r.startswith("xform"):
                res[i] = new_str
    for i in range(len(res)):
        res[i] = res[i].lower()
    return res

if __name__ == "__main__":
    # bad_font_filter()
    # single_char_filter()
    ms_zrm_assistant()


