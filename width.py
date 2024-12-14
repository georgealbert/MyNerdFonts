#!/usr/bin/env /Applications/FontForge.app/Contents/MacOS/FFPython
# coding=utf8

import sys
import argparse
import logging
from fontTools.ttLib import TTFont


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def fix_width(src_file: str, width: int, line_position=0, line_thickness=0):
    """修改AvgCharWidth和isFixedPitch，让程序能正确的识别是等宽字体，并且能以等宽字体来显示"""
    src_font = TTFont(src_file, recalcBBoxes=False)

    post = src_font["post"].__dict__

    # 改为1后，vimr就能在等宽字体中找到了
    post["isFixedPitch"] = 1

    logging.info("Fix xAvgCharWidth, %d -> %d" % (src_font["OS/2"].xAvgCharWidth, width))

    # 设置为西文字体的宽度，设置后emacs可以中英文对齐了
    src_font["OS/2"].xAvgCharWidth = width

    old_position = post["underlinePosition"]
    old_thickness = post["underlineThickness"]

    if line_position != 0:
        post["underlinePosition"] = line_position
        print("fix post[\"underlinePosition\"], %d -> %d" % (old_position, post["underlinePosition"]))

    if line_thickness != 0:
        post["underlineThickness"] = line_thickness
        print("fix post[\"underlineThickness\"] %d -> %d" % (old_thickness,post["underlineThickness"]))

    src_font.save(src_file)
    src_font.close()


def check_char_width(src_file: str, is_verbose: bool):
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

    print("font[\"OS/2\"].xAvgCharWidth = %d" % font["OS/2"].xAvgCharWidth)

    # fonttools/blob/main/Lib/fontTools/cffLib/__init__.py
    post = font["post"].__dict__
    print("post[\"underlinePosition\"] = %d" % post["underlinePosition"])
    print("post[\"underlineThickness\"] = %d" % post["underlineThickness"])
    print("post[\"isFixedPitch\"] = %d" % post["isFixedPitch"])

    chars = {}
    
    for name in font.getGlyphOrder():
        glyph = font["glyf"][name]
        width, lsb = font["hmtx"][name]

        chars[str(width)] = chars.get(str(width), 0) + 1
        if is_verbose:
            print("[%s], width: %s, lsb: %s" % (name, width, lsb))

    sorted_values = sorted(chars.items(), key=lambda x: x[1])

    # for key, value in sorted_values.items():
    print("[char width]\t[count]")
    for key, value in sorted_values:
        print("%s\t\t%s" % (key, value))

    font.close()


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
    font.save(target_font)
    font.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group(required=True)
    # parser.add_argument('-c', '--check', type=str, help='check char width')
    parser.add_argument('-c', '--check', action='store_true', help='check char width')
    parser.add_argument('-v', '--verbose', action='store_true', help='whether show char detail when check char width')
    parser.add_argument('-m', '--modify', action='store_true', help='modify char width')
    parser.add_argument('-o', '--origin-width', type=int, help='origin char width')
    parser.add_argument('-t', '--target-width', type=int, help='target char width')
    parser.add_argument('-f', '--fix-width', type=int, help='fix ["OS/2"].xAvgCharWidth')
    parser.add_argument('-l', '--line-position', type=int, help='fix ["OS/2"].underlinePosition')
    parser.add_argument('-n', '--line-thickness', type=int, help='fix ["OS/2"].underlineThickness')

    parser.add_argument('filename', type=str, help='filename of a ttf file')

    # group.add_argument('-c', '--check', type=str, help='check char width', action='check')
    # group.add_argument('-m', '--modify', type=str, help='modify char width', action='modify')
    # group.add_argument('-o', '--origin-width', type=str, help='origin char width', action='modify')
    # group.add_argument('-t', '--target-width', type=str, help='target char width', action='modify')

    args = parser.parse_args()

    # print("%s, filename: %s" % (args, args.filename))

    if args.fix_width and args.line_position and args.line_thickness:
        fix_width(args.filename, args.fix_width, args.line_position, args.line_thickness)
        sys.exit(0)

    if args.check:
        # check后直接退出
        check_char_width(args.filename, args.verbose)
        sys.exit(0)

    if args.filename is not None and args.modify is not None and args.origin_width is not None and args.target_width is not None:
        change_char_width(args.filename, args.origin_width, args.target_width)
        sys.exit(0)

    parser.print_help()
