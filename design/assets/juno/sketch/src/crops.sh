#!/bin/sh
# 2x crops of every panel for the self-check (run in sketch/).
mkdir -p crops
c() { magick "$1" -crop "$2" +repage -filter point -resize 200% "crops/$3.png"; }
c juno-sheet.png 400x770+50+140 sheet-front
c juno-sheet.png 400x770+450+140 sheet-34
c juno-sheet.png 400x770+850+140 sheet-side
c juno-sheet.png 400x770+1250+140 sheet-back
c juno-sheet.png 900x740+1980+100 sheet-palette
c juno-sheet.png 740x640+10+975 sheet-handover
c juno-sheet.png 740x640+750+975 sheet-wave
c juno-sheet.png 780x640+1490+975 sheet-write
c juno-sheet.png 620x600+2280+975 sheet-expressions
c juno-sheet.png 660x460+20+1670 sheet-silhouette
c juno-sheet.png 660x420+20+2150 sheet-cup-size
c juno-sheet.png 2200x900+690+1670 sheet-lineups
c juno-sheet.png 1500x620+20+2550 sheet-gamecam
c juno-sheet.png 1100x420+1750+2550 sheet-facecheck
c body-map.png 1700x960+20+110 bm-front-side-back
c body-map.png 1000x420+1610+960 bm-holds
c body-map.png 1300x700+20+1090 bm-gamecam
c body-map.png 1000x900+1620+130 bm-notes
c explore.png 2700x500+0+110 ex-refs
c explore.png 2700x660+0+520 ex-thumbs
c explore.png 2700x680+0+1190 ex-directions
