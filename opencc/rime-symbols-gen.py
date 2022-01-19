#!/usr/bin/env python
#-*- encoding:utf-8 -*-

# https://www.unicode.org/charts/charindex.html

import json
import opencc
s2t = opencc.OpenCC('s2t.json')


def strSpaceRange_1(start, end):
    return ' '.join(map(chr,range(start, end + 1)))

def genTextTypeCategory(name, ranges):
    t_name = s2t.convert(name)

    text = ''

    # 繁体一遍
    if name != t_name:
        text += t_name + '\t' + t_name + ' '
        for r in ranges:
            text += strSpaceRange_1(r[0], r[1])
        text += '\n'

    # 简体一遍
    text += name + '\t' + name + ' '
    for r in ranges:
        text += strSpaceRange_1(r[0], r[1])
    text += '\n'

    return text

def genTextTypeWord(name, char):
    t_name = s2t.convert(name)

    text = ''

    # 繁体一遍
    if name != t_name:
        text += t_name + '\t' + t_name + ' ' + char + '\n'

    # 简体一遍
    text += name + '\t' + name + ' ' + char + '\n'
    return text

def genSymbolCategory(file_name):
    text = ''

    # 音符
    # https://www.unicode.org/charts/PDF/U2600.pdf
    text += genTextTypeCategory('音乐符号', (
        (0x2669, 0x266F),
        ))

    # 几何图形
    # https://www.unicode.org/charts/PDF/U25A0.pdf
    # https://www.unicode.org/charts/PDF/U1F780.pdf
    text += genTextTypeCategory('几何图形', (
        (0x25A0, 0x25FF),
        # (0x1F780, 0x1F7D8),
        (0x1F7E0, 0x1F7EB),
        ))

    # 箭头符号
    # https://www.unicode.org/charts/PDF/U2190.pdf
    # https://www.unicode.org/charts/PDF/U2B00.pdf
    text += genTextTypeCategory('箭头符号', (
        (0x2190, 0x21FF),
        # (0x2B00, 0x2B73),
        ))

    # 数学符号
    # https://www.unicode.org/charts/PDF/U2200.pdf
    text += genTextTypeCategory('数学符号', (
        (0x2200, 0x22FF),
        ))

    # 罗马数字
    # https://www.unicode.org/charts/PDF/U2150.pdf
    text += genTextTypeCategory('罗马数字', (
        (0x2160, 0x2183),
        ))

    # 希腊字母
    # https://www.unicode.org/charts/PDF/U0370.pdf
    text += genTextTypeCategory('希腊字母', (
        (0x03B1, 0x03C9),
        (0x0391, 0x03A1),
        (0x03A3, 0x03A9),
        ))


    open(file_name, 'w', encoding = 'utf-8').write(text)

def genSymbolWord(file_name):
    text = ''

    text += genTextTypeWord('左', '←')
    text += genTextTypeWord('上', '↑')
    text += genTextTypeWord('右', '→')
    text += genTextTypeWord('下', '↓')
    text += genTextTypeWord('左上', '↖')
    text += genTextTypeWord('右上', '↗')
    text += genTextTypeWord('右下', '↘')
    text += genTextTypeWord('左下', '↙')

    text += genTextTypeWord('负', '−')
    text += genTextTypeWord('根号', '√')
    text += genTextTypeWord('三次根号', '∛')
    text += genTextTypeWord('四次根号', '∜')
    text += genTextTypeWord('正比于', '∝')
    text += genTextTypeWord('无穷大', '∞')
    text += genTextTypeWord('角', '∠')
    text += genTextTypeWord('平行于', '∥')
    text += genTextTypeWord('交集', '∩')
    text += genTextTypeWord('并集', '∪')
    text += genTextTypeWord('积分', '∫')
    text += genTextTypeWord('双重积分', '∬')
    text += genTextTypeWord('二重积分', '∬')
    text += genTextTypeWord('三重积分', '∭')
    text += genTextTypeWord('所以', '∴')
    text += genTextTypeWord('因为', '∵')
    text += genTextTypeWord('相似于', '∽')
    text += genTextTypeWord('全等于', '≌')
    text += genTextTypeWord('垂直于', '⊥')
    text += genTextTypeWord('约等于', '≈')
    text += genTextTypeWord('不等于', '≠')
    text += genTextTypeWord('包含于', '⊂')
    text += genTextTypeWord('小于等于', '≤')
    text += genTextTypeWord('大于等于', '≥')
    text += genTextTypeWord('异或', '⊕')

    text += genTextTypeWord('零次方', '⁰')
    text += genTextTypeWord('一次方', '¹')
    text += genTextTypeWord('二次方', '²')
    text += genTextTypeWord('平方', '²')
    text += genTextTypeWord('三次方', '³')
    text += genTextTypeWord('立方', '³')
    text += genTextTypeWord('四次方', '⁴')
    text += genTextTypeWord('五次方', '⁵')
    text += genTextTypeWord('六次方', '⁶')
    text += genTextTypeWord('七次方', '⁷')
    text += genTextTypeWord('八次方', '⁸')
    text += genTextTypeWord('九次方', '⁹')

    text += genTextTypeWord('摄氏度', '℃')
    text += genTextTypeWord('华氏度', '℉')
    text += genTextTypeWord('百分号', '％')
    text += genTextTypeWord('千分号', '‰')
    text += genTextTypeWord('万分号', '‱')
    text += genTextTypeWord('度', '°')
    text += genTextTypeWord('欧姆', 'Ω')


    text += genTextTypeWord('皮安', '㎀')
    text += genTextTypeWord('纳安', '㎁')
    text += genTextTypeWord('微安', '㎂')
    text += genTextTypeWord('毫安', '㎃')
    text += genTextTypeWord('千安培', '㎄')
    text += genTextTypeWord('千字节', '㎅')
    text += genTextTypeWord('兆字节', '㎆')
    text += genTextTypeWord('吉字节', '㎇')
    text += genTextTypeWord('卡路里', '㎈')
    text += genTextTypeWord('卡', '㎈')
    text += genTextTypeWord('千卡', '㎉')
    text += genTextTypeWord('皮法', '㎊')
    text += genTextTypeWord('纳法', '㎋')
    text += genTextTypeWord('微法', '㎌')
    text += genTextTypeWord('微克', '㎍')
    text += genTextTypeWord('毫克', '㎎')
    text += genTextTypeWord('千克', '㎏')
    text += genTextTypeWord('赫', '㎐')
    text += genTextTypeWord('赫兹', '㎐')
    text += genTextTypeWord('千赫', '㎑')
    text += genTextTypeWord('千赫兹', '㎑')
    text += genTextTypeWord('兆赫', '㎒')
    text += genTextTypeWord('兆赫兹', '㎒')
    text += genTextTypeWord('吉赫', '㎓')
    text += genTextTypeWord('吉赫兹', '㎓')
    text += genTextTypeWord('太赫', '㎔')
    text += genTextTypeWord('太赫兹', '㎔')

    text += genTextTypeWord('费米', '㎙')
    text += genTextTypeWord('纳米', '㎚')
    text += genTextTypeWord('微米', '㎛')
    text += genTextTypeWord('毫米', '㎜')
    text += genTextTypeWord('厘米', '㎝')
    text += genTextTypeWord('千米', '㎞')
    text += genTextTypeWord('平方毫米', '㎟')
    text += genTextTypeWord('平方厘米', '㎠')
    text += genTextTypeWord('平方米', '㎡')
    text += genTextTypeWord('平方千米', '㎢')
    text += genTextTypeWord('立方毫米', '㎣')
    text += genTextTypeWord('立方厘米', '㎤')
    text += genTextTypeWord('立方米', '㎥')
    text += genTextTypeWord('立方千米', '㎦')
    text += genTextTypeWord('米每秒', '㎧')
    text += genTextTypeWord('米每平方秒', '㎨')
    text += genTextTypeWord('帕', '㎩')
    text += genTextTypeWord('千帕', '㎪')
    text += genTextTypeWord('兆帕', '㎫')
    text += genTextTypeWord('吉帕', '㎬')
    text += genTextTypeWord('弧度', '㎭')
    text += genTextTypeWord('弧度每秒', '㎮')
    text += genTextTypeWord('每平方秒弧度', '㎯')
    text += genTextTypeWord('皮秒', '㎰')
    text += genTextTypeWord('纳秒', '㎱')
    text += genTextTypeWord('微秒', '㎲')
    text += genTextTypeWord('毫秒', '㎳')
    text += genTextTypeWord('皮伏', '㎴')
    text += genTextTypeWord('纳伏', '㎵')
    text += genTextTypeWord('微伏', '㎶')
    text += genTextTypeWord('毫伏', '㎷')
    text += genTextTypeWord('千伏', '㎸')
    text += genTextTypeWord('兆伏', '㎹')
    text += genTextTypeWord('皮瓦', '㎺')
    text += genTextTypeWord('纳瓦', '㎻')
    text += genTextTypeWord('微瓦', '㎼')
    text += genTextTypeWord('毫瓦', '㎽')
    text += genTextTypeWord('千瓦', '㎾')
    text += genTextTypeWord('兆瓦', '㎿')
    text += genTextTypeWord('微欧', '㏀')
    text += genTextTypeWord('兆欧', '㏁')
    text += genTextTypeWord('上午', '㏂')
    text += genTextTypeWord('贝可', '㏃')
    text += genTextTypeWord('立方厘米', '㏄')
    text += genTextTypeWord('坎', '㏅')
    text += genTextTypeWord('坎德拉', '㏅')
    text += genTextTypeWord('库伦每千克', '㏆')
    #text += genTextTypeWord('', '㏇')
    text += genTextTypeWord('分贝', '㏈')
    text += genTextTypeWord('戈瑞', '㏉')
    text += genTextTypeWord('公顷', '㏊')
    text += genTextTypeWord('马力', '㏋')
    text += genTextTypeWord('英寸', '㏌')
    # text += genTextTypeWord('', '㏍')
    # text += genTextTypeWord('', '㏎')
    text += genTextTypeWord('节', '㏏')
    text += genTextTypeWord('流明', '㏐')
    #text += genTextTypeWord('', '㏑')
    #text += genTextTypeWord('', '㏒')
    text += genTextTypeWord('勒克斯', '㏓')
    #text += genTextTypeWord('', '㏔')
    text += genTextTypeWord('密耳', '㏕')
    text += genTextTypeWord('摩尔', '㏖')
    #text += genTextTypeWord('', '㏗')
    text += genTextTypeWord('下午', '㏘')
    text += genTextTypeWord('百万分比浓度', '㏙')
    #text += genTextTypeWord('', '㏚')
    text += genTextTypeWord('球面度', '㏛')
    text += genTextTypeWord('希沃特', '㏜')
    text += genTextTypeWord('韦伯', '㏝')
    text += genTextTypeWord('牛顿每库仑', '㏞')
    text += genTextTypeWord('安每米', '㏟')
    text += genTextTypeWord('安培每米', '㏟')

    text += genTextTypeWord('四分之一', '¼')
    text += genTextTypeWord('二分之一', '½')
    text += genTextTypeWord('四分之三', '¾')

    text += genTextTypeWord('七分之一', '⅐')
    text += genTextTypeWord('九分之一', '⅑')
    text += genTextTypeWord('十分之一', '⅒')
    text += genTextTypeWord('三分之一', '⅓')
    text += genTextTypeWord('三分之二', '⅔')
    text += genTextTypeWord('五分之一', '⅕')
    text += genTextTypeWord('五分之二', '⅖')
    text += genTextTypeWord('五分之三', '⅗')
    text += genTextTypeWord('五分之四', '⅘')
    text += genTextTypeWord('六分之一', '⅙')
    text += genTextTypeWord('六分之五', '⅚')
    text += genTextTypeWord('八分之一', '⅛')
    text += genTextTypeWord('八分之三', '⅜')
    text += genTextTypeWord('八分之五', '⅝')
    text += genTextTypeWord('八分之七', '⅞')
    #text += genTextTypeWord('', '⅟')

    text += genTextTypeWord('阿尔法', 'α')
    text += genTextTypeWord('贝塔', 'β')
    text += genTextTypeWord('伽玛', 'γ')
    text += genTextTypeWord('德尔塔', 'δ')
    text += genTextTypeWord('艾普西龙', 'ε')
    text += genTextTypeWord('捷塔', 'ζ')
    text += genTextTypeWord('依塔', 'η')
    text += genTextTypeWord('西塔', 'θ')
    text += genTextTypeWord('缪', 'μ')
    text += genTextTypeWord('派', 'π')
    text += genTextTypeWord('套', 'τ')
    text += genTextTypeWord('普赛', 'ψ')
    text += genTextTypeWord('欧米伽', 'ω')

    text += genTextTypeWord('人民币', '¥')
    text += genTextTypeWord('元', '¥')
    text += genTextTypeWord('日元', '￥')
    text += genTextTypeWord('美分', '￠')
    text += genTextTypeWord('美元', '＄')
    text += genTextTypeWord('英镑', '￡')
    text += genTextTypeWord('欧元', '€')
    text += genTextTypeWord('朝鲜元', '₩')
    text += genTextTypeWord('韩元', '₩')

    text += genTextTypeWord('点', '丶')
    text += genTextTypeWord('横', '一')
    text += genTextTypeWord('竖', '丨')
    text += genTextTypeWord('撇', '丿')
    text += genTextTypeWord('捺', '㇏')
    text += genTextTypeWord('提', '㇀')

    text += genTextTypeWord('横折', '㇕')
    text += genTextTypeWord('横撇', 'フ')
    text += genTextTypeWord('横钩', '乛')
    text += genTextTypeWord('横折钩', '')
    text += genTextTypeWord('横折提', '㇊')
    text += genTextTypeWord('横折弯', '㇍')
    text += genTextTypeWord('横折折', '㇅')
    text += genTextTypeWord('横斜钩', '⺄')
    text += genTextTypeWord('横折弯钩', '㇈')
    text += genTextTypeWord('横撇弯钩', '㇌')
    text += genTextTypeWord('横折折撇', '㇋')
    text += genTextTypeWord('横折折折钩', '𠄎')
    text += genTextTypeWord('横折折折', '㇎')
    text += genTextTypeWord('竖提', '𠄌')
    text += genTextTypeWord('竖折', '𠃊')
    text += genTextTypeWord('竖钩', '亅')
    text += genTextTypeWord('竖弯', '㇄')
    text += genTextTypeWord('竖弯钩', '乚')
    text += genTextTypeWord('竖折撇', 'ㄣ')
    text += genTextTypeWord('竖折折', '𠃑')
    text += genTextTypeWord('竖折折钩', '㇉')
    text += genTextTypeWord('撇点', '𡿨')
    text += genTextTypeWord('撇折', '𠃋')
    text += genTextTypeWord('斜钩', '㇂')
    text += genTextTypeWord('弯钩', '㇁')
    text += genTextTypeWord('卧钩', '㇃')

    open(file_name, 'w', encoding = 'utf-8').write(text)

def genOpenccJson(name, file_name, category, word):
    text_json = {
      "name": name,
      "segmentation": {
        "type": "mmseg",
        "dict": {
          "type": "text",
          "file": word
        }
      },
      "conversion_chain": [{
        "dict": {
          "type": "group",
          "dicts": [{
            "type": "text",
            "file": word
          }, {
            "type": "text",
            "file": category
          }]
        }
      }]
    }
    json.dump(text_json, open(file_name, 'w'))

def main():
    category = 'symbol_category.txt'
    word = 'symbol_word.txt'
    genSymbolCategory(category)
    genSymbolWord(word)
    genOpenccJson('Chinese to Symbol', 'symbol.json', category, word)


if __name__ == '__main__':
    exit(main())
