import argparse
import os, errno
import random
import string
import fontconfig

from tqdm import tqdm
from string_generator import (
    create_strings_from_dict,
    create_strings_from_file,
    create_strings_from_wikipedia,
    create_strings_randomly
)
from data_generator import FakeTextDataGenerator
from multiprocessing import Pool

import time
import os
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

FONTS_PATH = '/home/buiduchanh/WorkSpace/Deep_reader/Textco/fonts/japan'
def fonts(fontfiles):
    # with open(os.path.join(DATA_PATH, 'fontlist.txt')) as f:
    #     contents = f.readlines()
    # contents = [x.strip() for x in contents]

    cmaps = {}
    for fontfile in fontfiles:
        # font_path = os.path.join(DATA_PATH, content)
        font = TTFont(fontfile)
        fontfile = os.path.basename(fontfile)
        for cmap in font['cmap'].tables:
            uni_chars = []
            for uni_char in cmap.cmap:
                uni_chars.append(uni_char)
            cmaps[fontfile] = uni_chars
    return cmaps

def get_valid_fonts(strings, fontfiles):
    valid_fonts = []
    for text in strings:
        font_list = fontfiles.copy()
        random.shuffle(font_list)
        get_font = None
        while(len(font_list) > 0):
            fontfile = random.choice(font_list)
            font = fontconfig.FcFont(fontfile)

            check_txt = True
            for char in text:
                if not font.has_char(char):
                    check_txt = False
                    break

            if check_txt:
                get_font = os.path.basename(fontfile)
                break

            font_list.remove(fontfile)

        if get_font is None:
            valid_fonts.append('error')
        else: 
            valid_fonts.append(get_font)

    return valid_fonts

def valid_range(s):
    if len(s.split(',')) > 2:
        raise argparse.ArgumentError("The given range is invalid, please use ?,? format.")
    return tuple([int(i) for i in s.split(',')])

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(description='Generate synthetic text data for text recognition.')
    parser.add_argument(
        "--output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        default="out/",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text",
        default=""
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be fr (French), en (English), es (Spanish), de (German), or cn (Chinese).",
        default="japan"
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",
        help="The number of images to be created.",
        default = 20
    )
    parser.add_argument(
        "-rs",
        "--random_sequences",
        action="store_true",
        help="Use random sequences as the source text for the generation. Set '-let','-num','-sym' to use letters/numbers/symbols. If none specified, using all three.",
        default=False
    )
    parser.add_argument(
        "-let",
        "--include_letters",
        action="store_true",
        help="Define if random sequences should contain letters. Only works with -rs",
        default=False
    )
    parser.add_argument(
        "-num",
        "--include_numbers",
        action="store_true",
        help="Define if random sequences should contain numbers. Only works with -rs",
        default=False
    )
    parser.add_argument(
        "-sym",
        "--include_symbols",
        action="store_true",
        help="Define if random sequences should contain symbols. Only works with -rs",
        default=False
    )
    parser.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",
        help="Define how many words should be included in each generated sample. If the text source is Wikipedia, this is the MINIMUM length",
        default=1
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=False
    )
    parser.add_argument(
        "-f",
        "--format",
        type=int,
        nargs="?",
        help="Define the height of the produced images",
        default=32,
    )
    parser.add_argument(
        "-t",
        "--thread_count",
        type=int,
        nargs="?",
        help="Define the number of thread to use for image generation",
        default=1,
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="jpg",
    )
    parser.add_argument(
        "-k",
        "--skew_angle",
        type=int,
        nargs="?",
        help="Define skewing angle of the generated text. In positive degrees",
        default=0,
    )
    parser.add_argument(
        "-rk",
        "--random_skew",
        action="store_true",
        help="When set, the skew angle will be randomized between the value set with -k and it's opposite",
        default=False,
    )
    parser.add_argument(
        "-wk",
        "--use_wikipedia",
        action="store_true",
        help="Use Wikipedia as the source text for the generation, using this paremeter ignores -r, -n, -s",
        default=False,
    )
    parser.add_argument(
        "-bl",
        "--blur",
        type=int,
        nargs="?",
        help="Apply gaussian blur to the resulting sample. Should be an integer defining the blur radius",
        default=0,
    )
    parser.add_argument(
        "-rbl",
        "--random_blur",
        action="store_true",
        help="When set, the blur radius will be randomized between 0 and -bl.",
        default=False,
    )
    parser.add_argument(
        "-b",
        "--background",
        type=int,
        nargs="?",
        help="Define what kind of background to use. 0: Gaussian Noise, 1: Plain white, 2: Quasicrystal, 3: Pictures",
        default=1,
    )
    parser.add_argument(
        "-hw",
        "--handwritten",
        action="store_true",
        help="Define if the data will be \"handwritten\" by an RNN",
    )
    parser.add_argument(
        "-na",
        "--name_format",
        type=int,
        help="Define how the produced files will be named. 0: [TEXT]_[ID].[EXT], 1: [ID]_[TEXT].[EXT] 2: [ID].[EXT] + one file labels.txt containing id-to-label mappings",
        default=0,
    )
    parser.add_argument(
        "-d",
        "--distorsion",
        type=int,
        nargs="?",
        help="Define a distorsion applied to the resulting image. 0: None (Default), 1: Sine wave, 2: Cosine wave, 3: Random",
        default=0
    )
    parser.add_argument(
        "-do",
        "--distorsion_orientation",
        type=int,
        nargs="?",
        help="Define the distorsion's orientation. Only used if -d is specified. 0: Vertical (Up and down), 1: Horizontal (Left and Right), 2: Both",
        default=0
    )
    parser.add_argument(
        "-wd",
        "--width",
        type=int,
        nargs="?",
        help="Define the width of the resulting image. If not set it will be the width of the text + 10. If the width of the generated text is bigger that number will be used",
        default=-1
    )
    parser.add_argument(
        "-al",
        "--alignment",
        type=int,
        nargs="?",
        help="Define the alignment of the text in the image. Only used if the width parameter is set. 0: left, 1: center, 2: right",
        default=1
    )
    parser.add_argument(
        "-tc",
        "--text_color",
        type=str,
        nargs="?",
        help="Define the text's color, should be either a single hex color or a range in the ?,? format.",
        default='#000000'
    )

    return parser.parse_args()

def load_dict(lang):
    """
        Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(os.path.join('dicts', lang + '.txt'), 'r', encoding="utf8", errors='ignore') as d:
        lang_dict = d.readlines()
    return lang_dict

def load_fonts(lang):
    """
        Load all fonts in the fonts directories
    """

    if lang == 'cn':
        return [os.path.join('fonts/cn', font) for font in os.listdir('fonts/cn')]
    elif lang == 'japan':
        return [os.path.join('fonts/japan', font) for font in os.listdir('fonts/japan')]
    else:
        return [os.path.join('fonts/latin', font) for font in os.listdir('fonts/latin')]

def main():
    """
        Description: Main function
    """

    # Argument parsing
    args = parse_arguments()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    lang_dict = load_dict(args.language)

    # Create font (path) list
    fontfiles = load_fonts(args.language)

    # cmaps = fonts(fontfiles)
    # print(cmaps['SNsanafonyu.ttf'])
    # exit()
    # 'SNsanafonyu.ttf'
  
    # Creating synthetic sentences (or word)
    strings = []

    if args.use_wikipedia:
        strings = create_strings_from_wikipedia(args.length, args.count, args.language)
    elif args.input_file != '':
        strings = create_strings_from_file(args.input_file, args.count)
    elif args.random_sequences:
        strings = create_strings_randomly(args.length, args.random, args.count,
                                          args.include_letters, args.include_numbers, args.include_symbols, args.language)
        # Set a name format compatible with special characters automatically if they are used
        if args.include_symbols or True not in (args.include_letters, args.include_numbers, args.include_symbols):
            args.name_format = 2
    else:
        strings = create_strings_from_dict(args.length, args.random, args.count, lang_dict)


    string_count = len(strings)
    # print('count',string_count)
    p = Pool(args.thread_count)
    # realfont = []
    # for text_ in strings:
        # #print('text',text_)
        # getfont = []
        # random.shuffle(fontfiles)
        # for fontfile in fontfiles:
            # #print(fontfile)
            # check_txt = True

            # fontfile = fontfile.split('/')[-1]
            # for char in text_:
                # #print('char',char)
                # if ord(char) not in cmaps[fontfile]:
                    # #print(cmaps[fontfile])
                    # check_txt = False
                    # break
            # if check_txt:
                # getfont.append(fontfile)
                # break
        # if not getfont:
            # realfont.append('error')
        # else: 
            # realfont.append(getfont[0])
   
    #realfont = get_valid_fonts(strings, fontfiles)
    with open ('texts/valid_font.txt') as fonts_:
        allfont = fonts_.readlines()
    realfont = [xfont.strip() for xfont in allfont]
    print('len font',len(realfont))
    
    names = ['address_201081129_%07d.jpg' % i for i in range (string_count)]

    #print(len(realfont))
    #for i in range(len(realfont)):
        #print('%d: %s' % (i, realfont[i]))

    #with open ('texts/valid_font.txt', 'a') as f_:
    #    for font in realfont:
    #        f_.writelines(font + '\n')
    #    f_.close()
        
    for _ in tqdm(p.imap_unordered(
        FakeTextDataGenerator.generate_from_tuple,
        zip(
            [i for i in range(0, string_count)],
            names,
            strings,
            # [fonts[random.randrange(0, len(fonts))] for _ in range(0, string_count)],
            [os.path.join(FONTS_PATH, _ ) for _ in realfont],
            [args.output_dir] * string_count,
            [args.format] * string_count,
            [args.extension] * string_count,
            [args.skew_angle] * string_count,
            [args.random_skew] * string_count,
            [args.blur] * string_count,
            [args.random_blur] * string_count,
            [args.background] * string_count,
            [args.distorsion] * string_count,
            [args.distorsion_orientation] * string_count,
            [args.handwritten] * string_count,
            [args.name_format] * string_count,
            [args.width] * string_count,
            [args.alignment] * string_count,
            [args.text_color] * string_count
        )
    ), total=args.count):
        pass
    p.terminate()

    if args.name_format == 2:
        # Create file with filename-to-label connections
        with open(os.path.join(args.output_dir, "labels.txt"), 'w', encoding="utf8") as f:
            for i in range(string_count):
                file_name = str(i) + "." + args.extension
                f.write("{} {}\n".format(file_name, strings[i]))

if __name__ == '__main__':
    main()

