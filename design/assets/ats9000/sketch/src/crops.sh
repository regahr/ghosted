#!/bin/sh
# 2x crops of every panel for the self-check (run in sketch/). v2 layout.
c() { magick "$1" -crop "$2" +repage -filter point -resize 200% "crops/$3.png"; }
c ats-sheet.png 440x680+40+140 sheet-front
c ats-sheet.png 440x680+460+140 sheet-34
c ats-sheet.png 440x680+880+140 sheet-side
c ats-sheet.png 440x680+1300+140 sheet-back
c ats-sheet.png 900x490+0+960 sheet-scan-stamp
c ats-sheet.png 1300x490+1500+960 sheet-slot-treads
c ats-sheet.png 1300x400+0+1440 sheet-screens
c ats-sheet.png 720x520+0+1840 sheet-silhouette
c ats-sheet.png 1440x620+740+1840 sheet-lineup
c ats-sheet.png 640x760+2180+1840 sheet-gamecam
c ats-sheet.png 900x840+1880+100 sheet-palette
c body-map.png 1680x1000+0+100 bm-front
c body-map.png 900x1000+1700+100 bm-side
c body-map.png 1200x700+0+1100 bm-gamecam
c body-map.png 1400x700+1200+1100 bm-table
