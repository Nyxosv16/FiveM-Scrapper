@echo off
echo "Start at: %date%:%time%" >> "information/log".txt
title FiveM scrapper v1.5
python main.py
echo "Close at: %date%:%time%" >> "information/log".txt