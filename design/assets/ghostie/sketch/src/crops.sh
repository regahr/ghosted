#!/bin/sh
# 2x crops of every panel (self-check). Run from the sketch folder.
mkdir -p crops
c(){ magick "$1" -crop "$2" +repage -scale 200% "crops/$3.png"; }
c ghostie-sheet.png 460x620+30+120 sheet-front
c ghostie-sheet.png 460x620+490+120 sheet-34
c ghostie-sheet.png 460x620+950+120 sheet-side
c ghostie-sheet.png 460x620+1410+120 sheet-back
c ghostie-sheet.png 600x700+1860+120 sheet-palette-rules
c ghostie-sheet.png 380x470+30+760 sheet-var-tie
c ghostie-sheet.png 380x470+410+760 sheet-var-glasses
c ghostie-sheet.png 380x470+790+760 sheet-var-headset
c ghostie-sheet.png 640x470+1190+760 sheet-wave
c ghostie-sheet.png 420x470+1830+760 sheet-rest
c ghostie-sheet.png 560x380+20+1400 sheet-silhouette
c ghostie-sheet.png 820x380+610+1400 sheet-gamecam
c ghostie-sheet.png 960x480+1630+1400 sheet-tiespec
c body-map.png 1850x330+20+110 bm-A-explore
c body-map.png 1100x1000+20+480 bm-B-front
c body-map.png 1100x700+1150+480 bm-B-notes
c body-map.png 1400x600+20+1280 bm-C-attach
c body-map.png 1060x600+1430+1280 bm-D-gamecam
c tie-options.png 740x620+20+90 tie-ghostie-card
c tie-options.png 740x620+760+90 tie-kit-card
c tie-options.png 1480x440+10+630 tie-closeups-notes
