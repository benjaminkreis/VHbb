#!/usr/bin/env python

'''
Re-created from:
'''
'''
Add statistical shape errors (aka Barlow Beeston) to a shape .root file

Author: Evan K. Friis, UW Madison
'''
from utils import printTable
from numpy import linspace
import fnmatch
import logging
import ROOT
import sys
import os

cut = "bdt"
none = "-"
one = "1"

log = logging.getLogger('stat_shapes')

def readOldDataCard(filename):
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()
    data = []
    bin = []
    process = []
    for line in lines:
    	if line.startswith("----"): data.append(['break'])
    	elif (line.startswith("Observation") or line.startswith("shapes")): data.append([line.strip().split()[0],'','','']+line.strip().split()[1:])
    	elif (line.startswith("bin") or line.startswith("process") or line.startswith("rate")): 
    		data.append([line.strip().split()[0],'']+line.strip().split()[1:])
    		if line.startswith("bin"): bin=line.strip().split()
    		if (line.startswith("process") and line.strip().split()[1].startswith("Wh")): process=line.strip().split()
    	elif line.startswith("stat_"): continue
    	else: data.append(line.strip().split())
    return data, bin, process

def walk_and_copy(inputdir, outputdir, threshold, thresholdBG, binList, processList):
    ''' Recursive function which copies from inputdir to outputdir '''
    data = []
    for key in inputdir.GetListOfKeys():
        # Keep track of stuff we find in this directory
        directories = []
        histos = []
        name = key.GetName()
        classname = key.GetClassName()
        if classname.startswith('TDirectory'):
            directories.append(name)
        elif isinstance(inputdir.Get(name), ROOT.TH1):
            histos.append(name)
        # Copy all histograms from input -> output directory
        for histo in histos:
            th1 = inputdir.Get(histo)
            th1totBG = inputdir.Get(histo[:histo.find("__")+2]+'totalBackground')
            outputdir.cd()
            th1.Write()
            
            do_shapes = histo.endswith("0P") or histo.endswith("0M") or histo.endswith("W_light") or histo.endswith("W_b") or histo.endswith("W_bb") or histo.endswith("ZJets") or histo.endswith("ttbar") or histo.endswith("singleTop") or histo.endswith("VZ") or histo.endswith("VV")
            if do_shapes:
                # check all bins to see if they need to be shape-errored
                log.info("Building stat shapes for %s", histo)
                for ibin in range(1, th1.GetNbinsX()+1):
                    if th1.GetBinContent(ibin): 
                        error = th1.GetBinError(ibin)
                        val = th1.GetBinContent(ibin)
                        valtotBG = th1totBG.GetBinContent(ibin)
                        # Check if we are above threshold
                        if (error/val > threshold/100 and error/valtotBG > thresholdBG/100):
                            vtype = histo[histo.find(cut)+4:histo.find(cut)+10]
                            boost = histo[histo.find(cut)+11:histo.find("__")]
                            process0 = histo[histo.find("__")+2:]
                            process = process0
                            if (process0 == "Wh_125p6_0P"): process = "0P"
                            if (process0 == "Wh_125p6_0M"): process = "0M"
                            err_up = th1.Clone(
                                th1.GetName() + '_' + vtype + '_' + boost + '_' + process + "_ss_bin_%iUp" % ibin)
                            err_down = th1.Clone(
                                th1.GetName() + '_' + vtype + '_' + boost + '_' + process + "_ss_bin_%iDown" % ibin)
                            err_up.SetBinContent(ibin, val + error)
                            err_down.SetBinContent(ibin, val - error)
                            liste = [vtype + '_' + boost +  '_' + process + "_ss_bin_%i" % ibin,'shape']
                            for i in range(len(binList)-1):
                            	if ((vtype+'_'+boost==binList[i+1]) and (process0==processList[i+1])): liste.append(one)
                            	else: liste.append(none)
                            data.append(liste)
                            outputdir.cd()
                            err_up.Write()
                            err_down.Write()
                            log.info("==> built shape for %s bin %i", histo, ibin)
        # Now copy and recurse into subdirectories
        for subdir in directories:
            output_subdir = outputdir.mkdir(subdir)
            # Recurse
            walk_and_copy(
                inputdir.Get(subdir), output_subdir, 
                threshold, thresholdBG, binList, processList)
    return data

def main(inputRfilename, outputRfilename, inputDCfilename, outputDCfilename, threshold, thresholdBG):
    input = ROOT.TFile(inputRfilename, 'READ')
    output = ROOT.TFile(outputRfilename, 'RECREATE')
    data = []
    olddata, binList, processList = readOldDataCard(inputDCfilename)
    data += olddata
    newdata = walk_and_copy(input, output, threshold, thresholdBG, binList, processList)
    data += newdata
    out=open(outputDCfilename,'w')
    printTable(data,out)

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    threshold = 0 # cut on binError/binContent in %
    thresholdBG = 0 # cut on binError/binContent_TotalBackground in %
    prefix = "/uscms_data/d3/ssagir/VHbbAnalysis/CMSSW_5_3_3_patch2/src/VHbb/post/plots"
    prefix += "/BDT_nominalprime/"
    inputRfile = prefix+"plots.root"
    outputRfile = prefix+"plots_statUnc%(threshold)s_bg%(thresholdBG)s.root" %locals()
    inputDataCard = prefix+"dataCard.txt"
    outputDataCard = prefix+"dataCard_statUnc%(threshold)s_bg%(thresholdBG)s.txt" %locals()

    log.info("Building shape systematics. input: %s output: %s",
             inputRfile, outputRfile)
    main(inputRfile, outputRfile, inputDataCard, outputDataCard, float(threshold), float(thresholdBG))
