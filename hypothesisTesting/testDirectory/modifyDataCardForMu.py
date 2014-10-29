#!/usr/bin/python

from utils import printTable
from numpy import linspace
from sys import argv
import os

if not os.path.exists('dataCard_original.txt'): os.system('mv dataCard.txt dataCard_original.txt')

mu = argv[1]

def modifyfile(filename):
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()
    data = []
    for line in lines:
		if line.startswith("imax"):
			data.append(line.strip().split())
			imax = int(line.strip().split()[1])
			ColumnsToModify = linspace(2,(imax-1)*8+2,imax)
		elif line.startswith("rate"):
			rateList = ['rate','']
			i=1
			for item in line.strip().split()[1:]:
				if i in ColumnsToModify:
					itemtemp = float(mu)*float(item)
					rateList.append(str(itemtemp))
				else:
					rateList.append(item)
				i+=1
			data.append(rateList)
		elif line.startswith("----"): data.append(['break'])
		elif (line.startswith("Observation") or line.startswith("shapes")): data.append([line.strip().split()[0],'','','']+line.strip().split()[1:])
		elif (line.startswith("bin") or line.startswith("process")): data.append([line.strip().split()[0],'']+line.strip().split()[1:])
		else: data.append(line.strip().split())
    out=open('dataCard.txt','w')
    printTable(data,out)
				
modifyfile('dataCard_original.txt')
