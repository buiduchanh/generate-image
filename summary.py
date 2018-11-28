# -*- coding: utf-8 -*-
import codecs
import unicodedata


CHAR_DICT = {
    'ぁ': 'あ',
    'ァ': 'ア',
    'ぃ': 'い',
    'ィ': 'イ',
    'ぅ': 'う',
    'ゥ': 'ウ',
    'ぇ': 'え',
    'ェ': 'エ',
    'ぉ': 'お',
    'ォ': 'オ',
    'っ': 'つ',
    'ッ': 'ツ',
    'ゃ': 'や',
    'ャ': 'ヤ',
    'ゅ': 'ゆ',
    'ュ': 'ユ',
    'ょ': 'よ',
    'ョ': 'ヨ',
    'ー': '一',
    '-': '一',
    'ｯ': 'ツ',
    'ヶ': 'ケ',
    '×': 'x',
}


if __name__=='__main__':
    adds = []
    with open('address.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                adds.append(line)

    char_summary = dict()
    for item in adds:
        for char in item:
            char = unicodedata.normalize('NFKC', char)

            if char in CHAR_DICT.keys():
                char = CHAR_DICT[char]

            if char in char_summary.keys():
                char_summary[char] += 1
            else:
                char_summary[char] = 1

    summary_file = codecs.open('char_summary.txt', 'w', encoding='utf8')
    for k, v in char_summary.items():
        summary_file.write(k)
        summary_file.write(': ' + str(v))
        summary_file.write('\n')
    summary_file.close()