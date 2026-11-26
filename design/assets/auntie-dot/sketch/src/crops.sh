#!/bin/sh
# 2x crops of every panel for the self-check (run in sketch/).
c() { magick "$1" -crop "$2" +repage -filter point -resize 200% "crops/$3.png"; }
c dot-sheet.png 400x760+50+140 sheet-front
c dot-sheet.png 400x760+450+140 sheet-34
c dot-sheet.png 400x760+850+140 sheet-side
c dot-sheet.png 400x760+1250+140 sheet-back
c dot-sheet.png 900x620+1980+100 sheet-palette
c dot-sheet.png 790x560+20+940 sheet-sway
c dot-sheet.png 800x560+810+940 sheet-talk
c dot-sheet.png 640x560+1630+940 sheet-card
c dot-sheet.png 640x360+2260+940 sheet-expressions
c dot-sheet.png 660x420+20+1610 sheet-silhouette
c dot-sheet.png 1400x780+690+1610 sheet-lineup
c dot-sheet.png 780x900+2110+1610 sheet-gamecam
c body-map.png 1600x900+20+100 bm-front-side
c body-map.png 700x520+1580+940 bm-top
c body-map.png 1100x760+20+1040 bm-gamecam
c body-map.png 1000x760+1600+130 bm-notes
c explore.png 2700x620+0+110 ex-refs
c explore.png 2700x620+0+520 ex-thumbs
c explore.png 2700x620+0+1150 ex-directions
