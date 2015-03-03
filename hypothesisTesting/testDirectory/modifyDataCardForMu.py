#!/usr/bin/python

from utils import printTable
from numpy import linspace
from sys import argv
import os

#if not os.path.exists('dataCard_original.txt'): os.system('mv dataCard.txt dataCard_original.txt')

mu = float(argv[1])
process=argv[2]
if len(argv)>3: input=argv[3]
else:           input='dataCard.txt'
if len(argv)>4: output=argv[4]
else:           output='dataCardWMu.txt'



def modifyfile(filename):
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()
    data = []
    processes=[]
    for line in lines:
		if line.startswith("imax"):
			data.append(line.strip().split())
			imax = int(line.strip().split()[1])
		elif line.startswith("rate"):
			rateList = ['rate','']
			nprocess = len(line.strip().split()[1:])/imax
			#ColumnsToModify = linspace(2,(imax-1)*nprocess+2,imax)
                        ColumnsToModify=[]
                        for i in range(len(processes)):
                                       if process in processes[i]: ColumnsToModify.append(i+1)
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
		elif (line.startswith("bin") or line.startswith("process")):
                    data.append([line.strip().split()[0],'']+line.strip().split()[1:])
                    if line.startswith("process") and not processes:
                        processes=line.strip().split()[1:]
		else: data.append(line.strip().split())
    out=open(output,'w')
    printTable(data,out)
				
modifyfile(input)
