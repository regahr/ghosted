#!/bin/sh
# 2x crops of every panel for the self-check (run in sketch/).
c() { magick "$1" -crop "$2" +repage -filter point -resize 200% "crops/$3.png"; }
c ricky-sheet.png 380x760+60+140 sheet-front
c ricky-sheet.png 380x760+460+140 sheet-34
c ricky-sheet.png 380x760+860+140 sheet-side
c ricky-sheet.png 380x760+1260+140 sheet-back
c ricky-sheet.png 1240x560+20+960 sheet-drain
c ricky-sheet.png 720x560+1320+960 sheet-phone
c ricky-sheet.png 720x560+2080+960 sheet-hop
c ricky-sheet.png 660x420+20+1630 sheet-silhouette
c ricky-sheet.png 1480x440+710+1630 sheet-lineup
c ricky-sheet.png 560x580+2220+1630 sheet-gamecam
c ricky-sheet.png 800x700+1980+100 sheet-palette
c body-map.png 1600x900+20+100 bm-front-side
c body-map.png 980x420+1610+860 bm-gamecam
c body-map.png 2560x900+20+1000 bm-drain-map
c explore.png 2600x620+0+520 ex-thumbs
c explore.png 2600x600+0+1150 ex-directions
