#!/bin/sh
# 2x crops of every panel for the self-check (run in sketch/).
c() { magick "$1" -crop "$2" +repage -filter point -resize 200% "crops/$3.png"; }
c ats-sheet.png 440x700+40+140 sheet-front
c ats-sheet.png 440x700+460+140 sheet-34
c ats-sheet.png 440x700+880+140 sheet-side
c ats-sheet.png 440x700+1300+140 sheet-back
c ats-sheet.png 900x480+0+940 sheet-scan-stamp
c ats-sheet.png 1300x480+1500+940 sheet-hopper-treads
c ats-sheet.png 1300x480+0+1420 sheet-screens
c ats-sheet.png 720x520+0+1830 sheet-silhouette
c ats-sheet.png 1440x620+740+1830 sheet-lineup
c ats-sheet.png 640x700+2180+1830 sheet-gamecam
c ats-sheet.png 900x800+1880+100 sheet-palette
c body-map.png 1680x900+0+100 bm-front
c body-map.png 900x900+1700+100 bm-side
c body-map.png 1200x700+0+1000 bm-gamecam
c body-map.png 1400x700+1200+1000 bm-table
c explore.png 2600x620+0+500 ex-thumbs
c explore.png 2600x700+0+1180 ex-directions
