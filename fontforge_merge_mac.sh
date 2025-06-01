FUSION_NAME="IosevkaNFM + LXGW WenKai Mono Lite"
FUSION_ID="IosevkaNFM+LXGWWenKaiMonoLite"
# FUSION_DESCRIPTION: The free and open-source font fused with JetBrains Mono & Maple Mono
# FUSION_DEVELOPER: Space Time
# FUSION_URL: ${{ github.server_url }}/${{ github.repository }}
# FUSION_COPYRIGHT: Copyright 2025 Space Time (${{ github.server_url }}/${{ github.repository }})
# FUSION_LICENSE: "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org"


# for STYLE in "Thin" "ThinItalic" "ExtraLight" "ExtraLightItalic" "Light" "LightItalic" "Regular" "Italic" "Medium" "MediumItalic" "SemiBold" "SemiBoldItalic" "Bold" "BoldItalic" "ExtraBold" "ExtraBoldItalic"; do
for STYLE in "Regular"; do
    /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge "fuse_fonts.ff" \
              "release/LXGWWenKaiMonoLite-Regular-v1.511-20250325.ttf" \
              "release/IosevkaTermSS05NerdFontMono-Regular.ttf" \
              "$FUSION_ID-$STYLE" \
              "$FUSION_NAME" \
              "$FUSION_NAME $STYLE" \
              "$STYLE" \
              "$FUSION_ID-${STYLE}.ttf"
done

./width.py -f 520 -a 1040 IosevkaNFM+LXGWWenKaiMonoLite-Regular.ttf
./width.py -m IosevkaNFM+LXGWWenKaiMonoLite-Regular.ttf -o 1000 -t 1040
./width.py -m IosevkaNFM+LXGWWenKaiMonoLite-Regular-w1040.ttf -o 500 -t 520
rm IosevkaNFM+LXGWWenKaiMonoLite-Regular-w1040.ttf
mv IosevkaNFM+LXGWWenKaiMonoLite-Regular-w1040-w520.ttf IosevkaNFM+LXGWWenKaiMonoLite-Regular.ttf
timetag=`date "+%Y%m%d-%H-%M-%S"`
target="IosevkaNFM+LXGWWenKaiMonoLite-Regular-${timetag}.ttf"
mv IosevkaNFM+LXGWWenKaiMonoLite-Regular.ttf $target
./width.py -c $target
