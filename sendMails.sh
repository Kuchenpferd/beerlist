#!/bin/bash

cd ~/beerlist/Tools
nohup python3.6 sendMails.py "$@" > ../mail.log
