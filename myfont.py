# FOR SARASA: build hdmx table
import sys
import math
import getopt
import logging
from fontTools.ttLib import TTFont, newTable


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# 在 macOS 中，注意需要使用 fontforge 自带的 python
# brew install fontforge
# pipenv --site-packages --python=/Applications/FontForge.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3

def print_table(table):
    print(table, type(table))
    # for key,value in table.items():
    #     print("[%s] = %s" % (key, value))

def post_fix(src_file, dst_file):
    dst_font = TTFont(dst_file, recalcBBoxes=False)
    # build_hdmx(dst_font)
    fix_isFixedPitch(dst_font)

    src_font = TTFont(src_file)
    print_table(src_font["head"].__dict__)
    print_table(src_font["name"].__dict__)
    print_table(src_font["OS/2"].__dict__)
    print_table(src_font["OS/2"].panose.__dict__)
    print("src_file xAvgCharWidth: %s" % src_font["OS/2"].xAvgCharWidth)
    # print_table(src_font["hmtx"].__dict__)
    # print_table(src_font["hdmx"].panose.__dict__)

    # dst_font["OS/2"].xAvgCharWidth = src_font["OS/2"].xAvgCharWidth
    src_font.close()

    dst_font.save(dst_file)
    dst_font.close()

def build_hdmx(font):
    headFlagInstructionsMayAlterAdvanceWidth = 0x0010
    sarasaHintPpemMin = 11
    sarasaHintPpemMax = 48

    originalFontHead = font["head"]
    originalFontHmtx = font["hmtx"]

    originalFontHead.flags |= headFlagInstructionsMayAlterAdvanceWidth

    hdmxTable = newTable("hdmx")
    hdmxTable.hdmx = {}

    # build hdmx table for odd and hinted ppems only.
    for ppem in range(
        math.floor(sarasaHintPpemMin / 2) * 2 + 1, sarasaHintPpemMax + 1, 2
    ):
        halfUpm = originalFontHead.unitsPerEm / 2
        halfPpem = math.ceil(ppem / 2)
        hdmxTable.hdmx[ppem] = {
            name: math.ceil(width / halfUpm) * halfPpem
            for name, (width, _) in originalFontHmtx.metrics.items()
        }

    font["hdmx"] = hdmxTable


def fix_pitch(dst_file):
    dst_font = TTFont(dst_file, recalcBBoxes=False)
    fix_isFixedPitch(dst_font)

    # dst_font["OS/2"].xAvgCharWidth = 500

    dst_font.save(dst_file)
    dst_font.close()


def fix_isFixedPitch(font):
    post = font["post"].__dict__
    # print("isFixedPitch:" % post["isFixedPitch"])
    post["isFixedPitch"] = 1

class MyFont():
    '''参考Maple Font的chinese branch, SC/fix.py'''

    def __init__(self, target: str, family_name: str, suffix: str, sub: str):
        self.target = target

        self.family_name = family_name

        '''如SC，NF之类的'''
        self.suffix = suffix

        self.suffix_alt = suffix

        """如：Regular，Light, Retina"""
        self.sub = sub

        self.family_name_trim = family_name.replace(" ", "")

        logging.info("Open file: %s, family name: %s, suffix: %s, sub: %s" % (target, family_name, suffix, sub))
        self.font = TTFont(target)

    def set_name(self, name: str, id: int):
        self.font["name"].setName(name, nameID=id, platformID=3, platEncID=1, langID=0x409)
        self.font["name"].setName(name, nameID=id, platformID=1, platEncID=0, langID=0x0)

    def get_name(self, id: int):
        return self.font["name"].getName(nameID=id, platformID=3, platEncID=1)

    def del_name(self, id: int):
        self.font["name"].removeNames(nameID=id)

    def fix_name(self):
        # correct names
        self.set_name(f"{self.family_name} {self.suffix_alt}", 1)
        self.set_name(self.sub, 2)
        self.set_name(f"{self.family_name} {self.suffix} {self.sub}; {self.get_name(5)}", 3)
        self.set_name(f"{self.family_name} {self.suffix} {self.sub}", 4)
        self.set_name(f"{self.family_name_trim}{self.suffix.replace('-', '')}-{sub}", 6)

    # font.importXML(path.join(ttx_path, f, f + ".O_S_2f_2.ttx"))

    def fix_encoding_and_meta(self):
        # add code page, Latin / Japanese / Simplify Chinese / Traditional Chinese
        # self.font["OS/2"].ulCodePageRange1 = 1 << 0 | 1 << 17 | 1 << 18 | 1 << 20

        # fix meta table, https://learn.microsoft.com/en-us/typography/opentype/spec/meta
        meta = newTable("meta")
        meta.data = {
            "dlng": "Latn, Hans, Hant, Jpan",
            "slng": "Latn, Hans, Hant, Jpan",
        }
        self.font["meta"] = meta

    def fix_isFixedPitch(self):
        """修复字体为等宽字体"""
        post = self.font["post"].__dict__
        logging.debug("isFixedPitch: %d" % post["isFixedPitch"])
        post["isFixedPitch"] = 1

    def save(self):
        print("Save file:", f"{self.family_name} {self.suffix} {self.sub}")
        self.font.save(self.target, reorderTables=False)
        self.font.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("python myfont.py path-to-font family-name suffix sub-name")
        print("e.g.:")
        print("python myfont.py FantasqueSansMNFM_LXGWLite_Regular-fontforge-20241010.ttf \"Albert FantasqueSans LXGWLite\" \"NF\" \"Regular\"")
        sys.exit(1)

    src_font = sys.argv[1]
    family_name = sys.argv[2]
    suffix = sys.argv[3]
    sub = sys.argv[4]
    
    my_font = MyFont(src_font, family_name, suffix, sub)
    my_font.fix_name()
    my_font.fix_encoding_and_meta()
    my_font.fix_isFixedPitch()
    my_font.save()
