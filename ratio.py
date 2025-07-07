#!/usr/bin/env /Applications/FontForge.app/Contents/MacOS/FFPython
# coding=utf8

# https://github.com/tonsky/FiraCode/issues/1204 Font height option?
#
# ./ratio.py ~/Library/Fonts/FiraCode-Regular.ttf
# ./ratio.py ~/Library/Fonts/InputMonoNarrow-Regular.ttf
# ./ratio.py "~/Library/Fonts/MonoLisa Regular NF.ttf"
# ./ratio.py ~/Library/Fonts/PragmataPro_Mono_R_0822.ttf
# ./ratio.py '~/Library/Fonts/Ubuntu Mono Nerd Font Complete.ttf'
#
# ./ratio.py ~/Library/Fonts/IosevkaTermSS05NFM+LXGWWenKaiMonoLite-Regular-20250629.ttf
# 我修改后的Iosevka字体，E: 48% -> 57%, z: 71% -> 80%
#

import sys
import fontforge


def analyze_z_dimensions(font_path):
    font = fontforge.open(font_path)
    
    # 检查字体中是否包含字母'z'
    if 'z' not in font:
        print("错误：字体中不包含字母'z'")
        return
    
    # 获取字母'z'的glyph
    z_glyph = font['z']
    
    # 获取glyph的边界框 (xmin, ymin, xmax, ymax)
    bbox = z_glyph.boundingBox()
    
    # 计算宽度和高度
    width = bbox[2] - bbox[0]  # xmax - xmin
    height = bbox[3] - bbox[1]  # ymax - ymin
    
    # 计算宽高比例
    if height != 0:
        ratio = width / height
    else:
        ratio = float('inf')  # 避免除以零
    
    # 打印结果
    print(f"字体文件: {font_path}")
    print(f"字母'z'的边界框: {bbox}")
    print(f"宽度: {width} 单位")
    print(f"高度: {height} 单位")
    print(f"宽高比例: {ratio:.2f}")
    
    # 关闭字体文件
    font.close()


def analyze_glyph_dimensions(font, letter):
    # 检查字体中是否包含字母
    if letter not in font:
        print("错误：字体中不包含字母'%s'" % letter)
        return
    
    # 获取字母'z'的glyph
    glyph = font[letter]
    
    # 获取glyph的边界框 (xmin, ymin, xmax, ymax)
    bbox = glyph.boundingBox()
    
    # 计算宽度和高度
    width = bbox[2] - bbox[0]  # xmax - xmin
    height = bbox[3] - bbox[1]  # ymax - ymin
    
    # 计算宽高比例
    if height != 0:
        ratio = width / height
    else:
        ratio = float('inf')  # 避免除以零
    
    # print(f"字体文件: {font}")
    print(f"字母'{letter}'的边界框: {bbox}")
    print(f"宽度: {width} 单位")
    print(f"高度: {height} 单位")
    print(f"宽高比例: {ratio:.2f}")
    

if __name__ == "__main__":
    # font_file = input("请输入字体文件路径: ")
    # analyze_z_dimensions(font_file)
    font_file = sys.argv[1]

    print(f"字体文件: {font_file}")
    font = fontforge.open(font_file)
    analyze_glyph_dimensions(font, 'E')
    analyze_glyph_dimensions(font, 'z')
    font.close()
