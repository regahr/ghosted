#!/bin/sh
# 2x crops of every panel for the self-check (run in sketch/).
c() { magick "$1" -crop "$2" +repage -filter point -resize 200% "crops/$3.png"; }
c brett-sheet.png 400x770+50+140 sheet-front
c brett-sheet.png 400x770+450+140 sheet-34
c brett-sheet.png 400x770+850+140 sheet-side
c brett-sheet.png 400x770+1250+140 sheet-back
c brett-sheet.png 900x740+1980+100 sheet-palette
c brett-sheet.png 740x640+10+975 sheet-idle
c brett-sheet.png 800x640+750+975 sheet-like
c brett-sheet.png 740x640+1550+975 sheet-bullets
c brett-sheet.png 610x600+2280+975 sheet-expressions
c brett-sheet.png 660x460+20+1670 sheet-silhouette
c brett-sheet.png 1400x930+690+1670 sheet-lineup
c brett-sheet.png 780x1010+2110+1670 sheet-gamecam
c body-map.png 1600x960+20+110 bm-front-side
c body-map.png 940x420+1610+940 bm-hands
c body-map.png 1300x700+20+1090 bm-gamecam
c body-map.png 1000x1000+1620+130 bm-notes
c explore.png 2700x500+0+110 ex-refs
c explore.png 2700x660+0+520 ex-thumbs
c explore.png 2700x680+0+1190 ex-directions
