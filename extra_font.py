#!/usr/bin/env /Applications/FontForge.app/Contents/MacOS/FFPython

# coding=utf8
import getopt
import sys

try:
    import fontforge
except ImportError:
    print("未能加载 fontforge 模块，请先安装 fontforge")
    sys.exit(1)


def load_base_char_names(latin_file: str):
    font = fontforge.open(latin_file)
    latin_char_names = []

    for char_name in font:
        latin_char_names.append(char_name)

    font.close()
    return latin_char_names

def generate_extra_font(cn_file: str, latin_file: str):
    """把中文字体中包含的西文字符给去掉，生成一个只包含中文字体的文件"""
    latin_char_names = load_base_char_names(latin_file)
    cn_font = fontforge.open(cn_file)

    for char_name in latin_char_names:
        try:
            glyph = cn_font[char_name]
            glyph.clear()
        except Exception:
            continue

    cn_font.generate("extra_" + cn_file)
    cn_font.close()

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

    generate_extra_font(cn_file, latin_file)
