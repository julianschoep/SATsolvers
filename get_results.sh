#!/bin/bash

echo "Creating randomizations"


echo "get results size 3"
python3 aut_parser.py -i size6dimacs -s 6 -a dis-2LW
python3 aut_parser.py -i size6dimacs -s 6


