#!/usr/bin/env /Applications/FontForge.app/Contents/MacOS/FFPython
# coding=utf8

import sys
# import math
# import getopt
import argparse
import logging
from fontTools.ttLib import TTFont, newTable


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def print_table(table):
    print(table, type(table))
    for key,value in table.items():
        print("[%s] = %s" % (key, value))


def print_width(src_file: str):
    font = TTFont(src_file)
    print_table(font["head"].__dict__)
    print_table(font["name"].__dict__)
    # print_table(font["OS/2"].__dict__)
    # print_table(font["OS/2"].panose.__dict__)
    # print_table(font["hmtx"].__dict__)
    # print_table(font["hdmx"].panose.__dict__)
    logging.info("file xAvgCharWidth: %s" % font["OS/2"].xAvgCharWidth)

    font.close()


def fix_width(src_file: str, width: int):
    font = TTFont(src_file, recalcBBoxes=False)

    post = font["post"].__dict__
    post["isFixedPitch"] = 1

    logging.info("%s: change xAvgCharWidth from %d to %d" % (src_file, font["OS/2"].xAvgCharWidth, width))
    font["OS/2"].xAvgCharWidth = width

    font.save(src_file)
    font.close()


def check_char_width(src_file: str):
    """检查每个char的width
    FantasqueSansMNerdFont-Regular.ttf, upm: 2048, width: 1060, 比例 0.518，明显比FiraCode窄，FiraCode不好搭配中文

    gitee上chinese分支的默认宽度是1200，MapleMonoNF-Regular-2048.ttf 1228

    /Users/albert/workspace/FiraCode/distr/ttf/Albert Fira Code/AlbertFiraCode-Regular-LH1670-430.ttf, upm: 1950, width: 1200, 比例 0.615

    /Users/albert/workspace/maple-font/fonts/NF/MapleMono-NF-Regular.ttf 600

    /Users/albert/workspace/maple-font/fonts/NF/MapleMono-NF-Regular.ttf, upm: 1000, width: 600

    LXGWWenKaiLite-Regular.ttf, upm: 1000, width: 1000

    /Users/albert/Downloads/HarmonyOS_Sans_SC_Regular.ttf 原版，upm: 1000, width: 1000

    /Users/albert/workspace/font/SarasaTermSC-FiraCode-Retina-Regular-LH1670-430-w1230.ttf 用sarasa合并后，英文宽度615，中文1000。
      把中文改为1230后，中文太宽了。  
    """

    font = TTFont(src_file)

    print("font[\"hhea\"].advanceWidthMax = %d" % font["hhea"].advanceWidthMax)

    print("%s: xAvgCharWidth = %d" % (src_file, font["OS/2"].xAvgCharWidth))

    for name in font.getGlyphOrder():
        glyph = font["glyf"][name]
        width, lsb = font["hmtx"][name]
        # if width != match_width:
        #     continue
        # if glyph.numberOfContours == 0:
        #     font["hmtx"][name] = (target_width, lsb)
        #     continue

        # delta = round((target_width - width) / 2)
        # glyph.coordinates.translate((delta, 0))
        # glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax = (
        #     glyph.coordinates.calcIntBounds()
        # )
        # font["hmtx"][name] = (target_width, lsb + delta)
        print("[%s], width: %s, lsb: %s" % (name, width, lsb))
    font.close()


# def change_char_width(font: TTFont, match_width: int, target_width: int):
def change_char_width(src_font: str, match_width: int, target_width: int):
    """ 只修改了中文的宽度，为什么中文是固定宽度的？
    if font_config.cn["narrow"]:
        change_char_width(font=font, match_width=1200, target_width=1000)
    """
    font = TTFont(src_font)
    font["hhea"].advanceWidthMax = target_width
    for name in font.getGlyphOrder():
        glyph = font["glyf"][name]
        width, lsb = font["hmtx"][name]

        # print("[%s], width: %s, lsb: %s" % (name, width, lsb))

        if width != match_width:
            continue
        if glyph.numberOfContours == 0:
            font["hmtx"][name] = (target_width, lsb)
            continue

        delta = round((target_width - width) / 2)
        try:
            glyph.coordinates.translate((delta, 0))
            glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax = (
                glyph.coordinates.calcIntBounds()
               )
            font["hmtx"][name] = (target_width, lsb + delta)
            print("--> [%s], width: %s -> %s, lsb: %s -> %s" % (name, width, target_width, lsb, lsb + delta))
        except Exception as e:
            print(e)

    target_font = src_font.split(".")[0] + "-w" + str(target_width) + ".ttf"
    logging.info("target_font: %s" % target_font)
    font.save(target_font)
    font.close()


if __name__ == '__main__':
    # opts, args = getopt.getopt(sys.argv[1:], '-h-c:-m:-v', ['help', 'check=', 'm=', 'version'])
    # print(opts)
    # print(args)

    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-c', '--check', action='store_true', help='check char width')
    parser.add_argument('-m', '--modify', action='store_true', help='modify char width')
    parser.add_argument('-o', '--origin-width', type=int, help='origin char width')
    parser.add_argument('-t', '--target-width', type=int, help='target char width')
    parser.add_argument('-w', '--width', type=int, help='fix avg char width')
    
    parser.add_argument('filename', type=str, help='ttf file name')

    # group.add_argument('-c', '--check', type=str, help='check char width', action='check')
    # group.add_argument('-m', '--modify', type=str, help='modify char width', action='modify')
    # group.add_argument('-o', '--origin-width', type=str, help='origin char width', action='modify')
    # group.add_argument('-t', '--target-width', type=str, help='target char width', action='modify')

    args = parser.parse_args()

    # print(args)

    if args.width is not None:
        fix_width(args.filename, args.width)
        sys.exit(0)

    if args.check:
        # check后直接退出
        check_char_width(args.filename)
        sys.exit(0)

    if args.modify is not None and args.origin_width is not None and args.target_width is not None:
        change_char_width(args.filename, args.origin_width, args.target_width)
        sys.exit(0)

    parser.print_help()
