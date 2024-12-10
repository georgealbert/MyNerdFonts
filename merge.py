# coding=utf8
import getopt
import sys

# ### !/usr/bin/env
# /Applications/FontForge.app/Contents/MacOS/FFPython

from fontTools.merge import Merger

# try:
#     import fontforge
# except ImportError:
#     print("未能加载 fontforge 模块，请先安装 fontforge")
#     sys.exit(1)


def merge_font(sc, nf):
    """把中文字体sc合并到英文字体nf(Nerd Font)中，合并前调整中文字体大小
    FontForge -> 元素 -> 字体信息 -> 通用 -> M全字大小(E)
    如把 LXGW Lite 从1000调整到2048
    """
    sc_font = fontforge.open(sc)
    latin_font = fontforge.open(nf)

    for item in sc_font.glyphs():
        if item.unicode == -1:
            continue
        sc_font.selection.select(("more", None), item.unicode)
        latin_font.selection.select(("more", None), item.unicode)

    sc_font.copy()
    latin_font.paste()

    latin_font.generate(nf + ".merge.ttf")
    sc_font.close()
    latin_font.close()


def build_cn(latin: str, cn: str ):
    merger = Merger()
    font = merger.merge(
        [
            cn,
            latin,
            # joinPaths(cn),
            # joinPaths(latin),
        ]
    )

    # font["OS/2"].xAvgCharWidth = 600


    # add code page, Latin / Japanese / Simplify Chinese / Traditional Chinese
    font["OS/2"].ulCodePageRange1 = 1 << 0 | 1 << 17 | 1 << 18 | 1 << 20

    # fix meta table, https://learn.microsoft.com/en-us/typography/opentype/spec/meta
    meta = newTable("meta")
    meta.data = {
        "dlng": "Latn, Hans, Hant, Jpan",
        "slng": "Latn, Hans, Hant, Jpan",
    }
    font["meta"] = meta

    font.save(latin + cn)
    font.close()


def usage():
    print("usage:\n--cnfile 中文字体文件 --latinfile 英文字体文件")

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '-h-c:-l:-v', ['help', 'cnfile=', 'latinfile=', 'version'])
    # print(opts)
    # print(args)

    cn_file = ""
    latin_file = ""
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            usage()
            sys.exit(0)

        if opt_name in ('-c', '--cnfile'):
            cn_file = opt_value
            
        if opt_name in ('-l', '--latinfile'):
            latin_file = opt_value

    if cn_file == "" or latin_file == "":
        usage()
        sys.exit(0)

    build_cn(cn_file, latin_file)

    # if len(sys.argv) != 3:
    #     print("中文字体 英文字体")
    #     sys.exit(1)
    # else:
    #     sc = sys.argv[1]
    #     nf = sys.argv[2]
        
        # merge_font(sc, nf)
