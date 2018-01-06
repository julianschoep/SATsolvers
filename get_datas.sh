#!/bin/bash

#echo "size 7"
#python3 web-scrapervlinux.py -d 1 -o size7dimacs -n 25 -s 7
#python3 web-scrapervlinux.py -d 2 -o size7dimacs -n 25 -s 7
#echo "size 6"
#python3 web-scrapervlinux.py -d 1 -o size6dimacs -n 25 -s 6
#python3 web-scrapervlinux.py -d 2 -o size6dimacs -n 25 -s 6
#echo "size 5"
#python3 web-scrapervlinux.py -d 1 -o size5dimacs -n 25 -s 5
#python3 web-scrapervlinux.py -d 8 -o size5dimacs -n 25 -s 5
echo "size 4"
#python3 web-scrapervlinux.py -d 7 -o size4dimacs -n 25 -s 4
#python3 web-scrapervlinux.py -d 8 -o size4dimacs -n 25 -s 4
echo "size 3"
#python3 web-scrapervlinux.py -d 8 -o size3dimacs -n 25 -s 3
python3 web-scrapervlinux.py -d 3 -o size6dimacs -n 50 -s 6

echo "Randomizing files..."
#python randomize.py -i size6dimacs
#python randomize.py -i size5dimacse
#python randomize.py -i size4dimacs
#python randomize.py -i size3dimacs

#python web-scraperv2.py -d 5 -o d5s6dimacs -n 30 -s 6
echo "size 7"
#python web-scraperv2.py -d 5 -o d5s7dimacs -n 30 -s 7
echo "Done."
