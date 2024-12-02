# MyNerdFonts

## Fantasque Sans Mono Regular Nerd Font Complete Mono + LXGW WenKai Mono Lite Regular
* 英文：Fantasque Sans Mono Regular Nerd Font Complete Mono.ttf (Nerd Fonts 2.3.3)
* 中文：LXGWWenKaiMonoLite-Regular v1.501 24/10/10

  下载地址：https://github.com/lxgw/LxgwWenKai-Lite/releases/download/v1.501/LXGWWenKaiLite-Regular.ttf

使用[`Warcraft-Font-Merger`](https://github.com/nowar-fonts/Warcraft-Font-Merger)进行合并。

* 优点：比`FantasqueSansMNerdFontMono-Regular.ttf`的行高(line height)要低，能多显示一两行。
* 缺点：Fantasque Sans好久没更新了，Iosevka在持续更新，支持国人。

## FantasqueSansMNerdFontMono + LXGW WenKai Mono Lite Regular
* 英文：FantasqueSansMNerdFontMono-Regular.ttf (Nerd Fonts 3.3.0)

  下载地址：https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/FantasqueSansMono.tar.xz
* 中文：LXGWWenKaiMonoLite-Regular v1.501 24/10/10

使用[`Warcraft-Font-Merger`](https://github.com/nowar-fonts/Warcraft-Font-Merger)进行合并。

## IosevkaTermSS12定制 + LXGW WenKai Mono Lite Regular

* 缺点：和`Fantasque Sans Mono`比起来，显示的行数少了10行左右，行距较大。但是可以调整Iosevka的行距，就和 Fantasque Sans Mono 一样了。

* IosevkaTermSS12 + LXGW WenKai Mono Lite size 16
  + leading=1200, 52行
  + leading=1000，60行，字太挤了。比Fantasque Sans Mono能多显示一行左右，太窄了。
  + leading=1080, 56行，比较合适，已经和FantasqueSansM差不多了。括号需要改小一点，但是好像几个选项都是一个高度，最好不要低于1050。
  + FantasqueSansMono Nerd Font Mono + LXGW WenKai，size 16，不到60行
  + FantasqueSansM Nerd Font Mono + LXGW WenKai Mono Lite，size 16，58行

  ```sh
  vim Iosevka/params/parameters.toml
  leading = 1000
  ```

使用[`Warcraft-Font-Merger`](https://github.com/nowar-fonts/Warcraft-Font-Merger)进行合并。

## IosevkaTermSS12定制 + 更纱黑Term SC

使用`Sarasa-Gothic`进行制作。将`Sarasa-Gothic/sources/IosevkaNTerm/IosevkaNTerm-Regular.ttf`等文件替换成自己定制的`IosevkaTermSS12`字体。

不要用[`Warcraft-Font-Merger`](https://github.com/nowar-fonts/Warcraft-Font-Merger)进行合并，不好控制字符数，建议在生成字体后再用`font-patcher`增加Nerd字体。

```sh
font-patcher --quiet --adjust-line-height --complete --careful your_font.ttf

# e.g.
./font-patcher --quiet --adjust-line-height --complete --careful ../release/IosevkaTermSS12\ +\ LXGW\ WenKai\ Mono\ Lite\ Regular.ttf
```

> 需要用[font-patcher](https://github.com/ryanoasis/nerd-fonts)，增加Nerd Font。如果字符超过65535个，可以去掉一部分`material icon`。

## 说明
1. `Iosevka`目录是定制的Iosevka Term Regular字体。
    在[Iosevka Customer](https://typeof.net/Iosevka/customizer)中，将`Iosevka`目录中的文件贴入，选择喜欢的字符。
    * SS05：FiraCode
    * SS12：UbuntuMono
    其实定制以后，这2个基本是一样的。

2. `Sarasa`目录是更纱黑字体，只build `Term SC Regular`字体，只能build出`Unhinted`的，`autohinted`的字体在build时，分析的时间太长了，跑不出来。

3. shell
  ```sh
  # linux
  TIME_STYLE="+%Y-%m-%d %H:%M%S" ls -ltr
  # macOS
  ls -l -D "%Y-%m-%d %H:%M:%S"
  ls -l -D "%Y-%m-%d %H:%M"
  ```

# 发布的字体

## 2024.12.02
| 大小     | 日期             | 字体                                               | 说明                                                                                                                            |
|----------|------------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| 16791140 | 2024-12-02 19:37 | SarasaTermAlbertSCNerd-Regular-LineHeight-1080.ttf | 推荐指数：`5`。调整Iosevka字体行距为1080，更纱黑在build时是按latin字体的大小来生成字体大小的                                    |
| 14871528 | 2024-12-02 19:41 | SarasaTermSC-FantaqueSans-Nerd_Font-Regular.ttf    | 推荐指数：`3`。中文字体更纱黑合并英文字体FantasqueSans，由于FantasqueSans英文字体的行距过小，光标会覆盖不完部分中文字体，不好看 |

## 2024.12.01
| 大小     | 日期             | 字体                                                               | 说明                                           |
|----------|------------------|--------------------------------------------------------------------|------------------------------------------------|
| 2231612  | 2023-04-03 12:40 | Fantasque Sans Mono Regular Nerd Font Complete Mono.ttf            | 原版英文字体，Nerd Fonts 2.3.3，行距较小       |
| 2172352  | 2024-12-01 21:00 | IosevkaTermSs12-Regular.ttf                                        | 原版英文字体                                   |
| 2379960  | 2024-11-18 08:10 | FantasqueSansMNerdFontMono-Regular.ttf                             | 原版英文字体，Nerd Fonts 3.3.0，行距较大       |
| 14078844 | 2024-11-29 23:54 | FantasqueSansMonoLXGWLite-Regular-20241129.ttf                     | 最早用fontforge手工合并的，中英文对齐有问题    |
| 17658148 | 2024-12-01 13:41 | FantasqueSansMono Nerd Font Mono + LXGW WenKai.ttf                 | 合并文楷字体                                   |
| 11693968 | 2024-12-01 14:03 | LXGWWenKaiMonoLite-Regular.ttf                                     | 未合并英文字体，v1.501 24/10/10                |
| 18029692 | 2024-12-01 10:07 | SarasaTermAlbertSCNerd-Regular.ttf                                 | 推荐指数：3。喜欢更纱黑的选这个                |
| 13444980 | 2024-12-01 17:35 | FantasqueSansMonoNerdFontMono_v2.3.0-LXGWWenKaiMonoLite_v1.501.ttf | 推荐指数：4，行距太小了                        |
| 22914768 | 2024-12-01 21:05 | IosevkaTermSS12+LXGWWenKaiMonoNerdFont-Regular.ttf                 | 推荐指数：4                                    |
| 15357896 | 2024-12-01 20:39 | IosevkaTermSS12+LXGWWenKaiMonoLiteNerdFont-Regular.ttf             | 推荐指数：`4`。行距有点大，字形也很好看        |
| 13639020 | 2024-12-01 14:35 | FantasqueSansNerd_v3.3.0-LXGWLite_v1.501.ttf                       | 推荐指数：`5`。行距大一些，比Iosevka多显示10行 |
