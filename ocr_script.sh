#!/bin/bash

for f in fighting300_cp/*.pdf
do

  FILE_NAME="${f%%.*}"

  convert -density 300 $FILE_NAME.pdf -depth 8 $FILE_NAME.tiff

  textcleaner -g -e stretch -f 25 -o 5 -s 1 -t 5 $FILE_NAME.tiff $FILE_NAME.tiff

  tesseract -l eng -psm 1 $FILE_NAME.tiff $FILE_NAME

done

echo "Done"