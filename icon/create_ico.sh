#!/bin/bash

#convert to png
inkscape --without-gui --export-png=mmg-icon_64x64.png --export-dpi=72 --export-background=rgb\(255,255,255\) --export-width=64 --export-height=64 mmg-icon.svg &> /dev/null
inkscape --without-gui --export-png=mmg-icon_48x48.png --export-dpi=72 --export-background=rgb\(255,255,255\) --export-width=48 --export-height=48 mmg-icon.svg &> /dev/null
inkscape --without-gui --export-png=mmg-icon_32x32.png --export-dpi=72 --export-background=rgb\(255,255,255\) --export-width=32 --export-height=32 mmg-icon.svg &> /dev/null
inkscape --without-gui --export-png=mmg-icon_16x16.png --export-dpi=72 --export-background=rgb\(255,255,255\) --export-width=16 --export-height=16 mmg-icon.svg &> /dev/null


#convert to xpm
#convert mmg-icon_32x32.png mmg-icon.xpm

#create ico
icotool -c -o mmg-icon.ico mmg-icon_64x64.png mmg-icon_48x48.png mmg-icon_32x32.png mmg-icon_16x16.png
