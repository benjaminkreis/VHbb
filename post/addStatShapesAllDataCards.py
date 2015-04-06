#!/usr/bin/env python

from utils import printTable

def readDataCard(filename):
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()
    data = []
    for line in lines:
    	if line.startswith("----"): data.append(['break'])
    	elif (line.startswith("Observation") or line.startswith("shapes")): data.append([line.strip().split()[0],'','','']+line.strip().split()[1:])
    	elif (line.startswith("bin") or line.startswith("process") or line.startswith("rate")): 
    		data.append([line.strip().split()[0],'']+line.strip().split()[1:])
    		if line.startswith("bin"): dict1=line.strip().split()[1:]
    		if (line.startswith("process") and line.strip().split()[1].startswith("Zh")): dict2=line.strip().split()[1:]
    	elif line.startswith("stat_"): continue
    	else: data.append(line.strip().split())
    dict = [item1+'_'+item2 for item1,item2 in zip(dict1,dict2)]
    return data, dict

def addStatShapes(filename, dictOld):
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()
    for line in lines[:50]:
    	if line.startswith("bin"): dict1=line.strip().split()[1:]
    	elif (line.startswith("process") and line.strip().split()[1].startswith("Zh")): dict2=line.strip().split()[1:]
    	else: continue
    dict = [item1+'_'+item2 for item1,item2 in zip(dict1,dict2)]
    data = []
    start = False
    for line in lines:
    	if line.startswith("ttbarShape_ZH"): 
    		start = True
    		continue
    	if start:
			dictTemp = {}
			count = 2
			for key in dict: 
				dictTemp[key] = line.strip().split()[count]
				count += 1
			datatemp = line.strip().split()[:2]
			for key in dictOld:
				datatemp += [dictTemp[key]]
			data.append(datatemp)
    return data

def main(inputDCfile, inputDCfile0P, outputDCfile0P, inputDCfile0M, outputDCfile0M):
	data0P = []
	dataOld0P, dictOld0P = readDataCard(inputDCfile0P)
	data0P += dataOld0P
	dataNew0P = addStatShapes(inputDCfile, dictOld0P)
	data0P += dataNew0P
	out0P=open(outputDCfile0P,'w')
	printTable(data0P,out0P)

	data0M = []
	dataOld0M, dictOld0M = readDataCard(inputDCfile0M)
	data0M += dataOld0M
	dataNew0M = addStatShapes(inputDCfile, dictOld0M)
	data0M += dataNew0M
	out0M=open(outputDCfile0M,'w')
	printTable(data0M,out0M)

if __name__ == "__main__":
	prefix = "/uscms_data/d3/ssagir/ZllHbbAnalysis/CMSSW_5_3_6/src/VHbb/post/plots"
	prefix += "/BDT_hypoTestBinning_official_unblinded_022715/"
	inputDCfile = prefix+"dataCard_statUnc15_bg7.txt"
	inputDCfile0P = prefix+"dataCard_0P.txt"
	inputDCfile0M = prefix+"dataCard_0M.txt"
	outputDCfile0P = prefix+"dataCard_0P"+inputDCfile.split('/')[-1][8:]
	outputDCfile0M = prefix+"dataCard_0M"+inputDCfile.split('/')[-1][8:]
	main(inputDCfile, inputDCfile0P, outputDCfile0P, inputDCfile0M, outputDCfile0M)
