# -*- coding: utf-8 -*-
import codecs
import unicodedata
import csv 

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
    flag  = False
    adds = []
    charac = []
    list_address = []
    with open('texts/data_add.txt', 'r', encoding='utf-8') as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line:
                adds.append(line)
    adds = list(set(adds))
    # print(adds)
    with open('texts/char_address.csv', 'r', encoding ='utf-8' ) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            charac.append(row[0])
    print(len(adds))
    
    newadds = []
    for idx, item in enumerate(adds):
        # print(item)
        newitem  = ''
        for numchar, char in enumerate(item):

            char = unicodedata.normalize('NFKC', char)

            if len(char) != 1:
                for id_ , ca_ in enumerate(char):
                    if ca_ not in charac:
                        char.replace(ca_,"")

            if char in CHAR_DICT.keys():
                char = CHAR_DICT[char]
            
            if char not in charac:
                continue
            newitem += char

        print('a',newitem)
        newadds.append(newitem)
    
    print(len(newadds))

    with open ('texts/final_add.txt' , 'w') as finadd:
        for itm in newadds:
            finadd.write(''.join(itm) + '\n')
        finadd.close()





    