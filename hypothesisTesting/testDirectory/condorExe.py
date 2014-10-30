#!/usr/bin/python

import os
from sys import argv

dir=argv[1]
command=' '.join(argv[2:])

os.chdir(dir)
os.system('source '+dir+'/condor.env')
os.system(command)


