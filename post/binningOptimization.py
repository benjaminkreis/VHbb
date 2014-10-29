#!/usr/bin/python

######################################################################
# Script to optimize binning of 2-D templates for hypothesis testing #
# The input histogram needs to have a uniform binning                #
######################################################################
#######################    Sinan Sagir    ############################
#######################  September, 2014  ############################
######################################################################

import ROOT as R
import sys
from array import array
from numpy import linspace

from tdrStyle import *
setTDRStyle()

RFile = R.TFile("plots.root")
hname = "mainBDT_v_VstarMass_bdt_Vtype0_highBoost__totalBackground" # histogram
sname = "globalBoxRebinned/box_"+hname # save name
sname = "test"
stat = 1e6#0.20 # if no statistical uncertainty required, enter a big number; e.g., 1e6

# bools to turn on/off the movement along a direction
goUp    =  0
goDown  =  0
goRight =  0
goLeft  =  0

# change dimensions of rectangle manually 
NbinsXmin =  0 # +/- #bins
NbinsXmax =  0 # +/- #bins
NbinsYmin =  0 # +/- #bins
NbinsYmax =  0 # +/- #bins

# merge the bins at the edges manually
mergeFirstXbin = None #  1 or None
mergeLastXbin  = None # -1 or None
mergeFirstYbin = None #  1 or None
mergeLastYbin  = None # -1 or None

# enter a note to save in the log file if wanted
note = ""

h = RFile.Get(hname).Clone()
h.Draw("COLZ")

canv = R.TCanvas(hname,hname,1000,700)
canv.SetTitle(hname)
h.Draw("COLZ")

Tex = R.TLatex()
Tex.SetNDC()
Tex.SetTextSize(0.04)
Tex.SetTextAlign(31)
Tex.DrawLatex(0.93, 0.92, hname)

# Get the bin with maximum # events
bin0 = h.GetMaximumBin()
binx0, biny0, binz0 = ROOT.Long(), ROOT.Long(), ROOT.Long()
h.GetBinXYZ(bin0, binx0, biny0, binz0)
binxmin, binymin, binxmax, binymax = binx0, biny0, binx0, biny0

# function to find a rectangular area that has no empty bins and statistical uncertainty < stat
# it takes a histogram and four bools to turn on/off movement along a directions and the coordinates
# of starting bin or a rectangular area chosen initially by user
def test(histo,isFinishedxp,isFinishedyp,isFinishedxm,isFinishedym,binxmin,binxmax,binymin,binymax):
	isEmpty=False
	while((not isFinishedxp) or (not isFinishedyp) or (not isFinishedxm) or (not isFinishedym)):
		if not isFinishedxp and histo.GetXaxis().GetBinUpEdge(binxmax)<1200:
			for biny in range(binymin,binymax+1):
				if  (histo.GetBinContent(binxmax+1,biny,binz0)==0): isEmpty=True
				elif (histo.GetBinError(binxmax+1,biny,binz0)/histo.GetBinContent(binxmax+1,biny,binz0)>stat): isEmpty=True
			if(not isEmpty):
				binxmax+=1
				isFinishedxp=False
			if(isEmpty): isFinishedxp=True
			isEmpty=False
		else: isFinishedxp=True 

		if not isFinishedyp and histo.GetYaxis().GetBinUpEdge(binymax)<1:	
			for binx in range(binxmin,binxmax+1):
				if (histo.GetBinContent(binx,binymax+1,binz0)==0): isEmpty=True
				elif (histo.GetBinError(binx,binymax+1,binz0)/histo.GetBinContent(binx,binymax+1,binz0)>stat): isEmpty=True
			if(not isEmpty):
				binymax+=1
				isFinishedyp=False
			if(isEmpty): isFinishedyp=True
			isEmpty=False
		else: isFinishedyp=True 

		if not isFinishedxm and histo.GetXaxis().GetBinLowEdge(binxmin)>0:	
			for biny in range(binymin,binymax+1):
				if (histo.GetBinContent(binxmin-1,biny,binz0)==0): isEmpty=True
				elif (histo.GetBinError(binxmin-1,biny,binz0)/histo.GetBinContent(binxmin-1,biny,binz0)>stat): isEmpty=True
			if(not isEmpty):
				binxmin-=1
				isFinishedxm=False
			if(isEmpty): isFinishedxm=True
			isEmpty=False
		else: isFinishedxm=True 

		if not isFinishedym and histo.GetYaxis().GetBinLowEdge(binymin)>-1:	
			for binx in range(binxmin,binxmax+1):
				if (histo.GetBinContent(binx,binymin-1,binz0)==0): isEmpty=True
				elif (histo.GetBinError(binx,binymin-1,binz0)/histo.GetBinContent(binx,binymin-1,binz0)>stat): isEmpty=True
			if(not isEmpty):
				binymin-=1
				isFinishedym=False
			if(isEmpty): isFinishedym=True
			isEmpty=False
		else: isFinishedym=True 
	return binxmin,binxmax,binymin,binymax

# call above function to find a local maximum rectangular area
binxmin_loc,binxmax_loc,binymin_loc,binymax_loc=test(h,0,0,0,0,binxmin,binxmax,binymin,binymax)
A_loc = (binxmax_loc-binxmin_loc)*(binymax_loc-binymin_loc)

# draw this local rectangular area on histogram
x1_loc = h.GetXaxis().GetBinLowEdge(binxmin_loc)
x2_loc = h.GetXaxis().GetBinUpEdge(binxmax_loc)
y1_loc = h.GetYaxis().GetBinLowEdge(binymin_loc)
y2_loc = h.GetYaxis().GetBinUpEdge(binymax_loc)
b_loc = R.TBox(x1_loc, y1_loc, x2_loc, y2_loc)
b_loc.SetFillStyle(0)
b_loc.SetLineWidth(3)
b_loc.SetLineColor(R.kYellow)
b_loc.Draw()
print "#####################################################################"
print hname
print "#####################################################################"
print "#####################################################################"
print "Red Box Dimensions (local):"
print "(x1, x2)_loc = (",x1_loc, ",", x2_loc, ") -->", binxmax_loc-binxmin_loc, "bins"
print "(y1, y2)_loc = (",y1_loc, ",", y2_loc, ") -->", binymax_loc-binymin_loc, "bins"
print "Area_loc  [bin^2] = ", A_loc
print "#####################################################################"

binxmin_glob,binxmax_glob,binymin_glob,binymax_glob = binxmin_loc,binxmax_loc,binymin_loc,binymax_loc
A_glob = A_loc
# try to find the global maximum --> guarantied to work most of the time, but not always
for i in range(3):
	for j in range(3):
		for k in range(3):
			for l in range(3):
				if (i and j and k and l): continue
				if not (i or j or k or l): continue
				binxmin_temp,binxmax_temp,binymin_temp,binymax_temp=test(h,i,k,j,l,binxmin_loc+i,binxmax_loc-j,binymin_loc+k,binymax_loc-l)
				A_temp = (binxmax_temp-binxmin_temp)*(binymax_temp-binymin_temp)
				if (A_temp>A_glob): 
					A_glob = A_temp
					binxmin_glob,binxmax_glob,binymin_glob,binymax_glob = binxmin_temp,binxmax_temp,binymin_temp,binymax_temp

# draw this global rectangular area on histogram					
x1_glob = h.GetXaxis().GetBinLowEdge(binxmin_glob)
x2_glob = h.GetXaxis().GetBinUpEdge(binxmax_glob)
y1_glob = h.GetYaxis().GetBinLowEdge(binymin_glob)
y2_glob = h.GetYaxis().GetBinUpEdge(binymax_glob)
b_glob = R.TBox(x1_glob, y1_glob, x2_glob, y2_glob)
b_glob.SetFillStyle(0)
b_glob.SetLineWidth(3)
b_glob.SetLineColor(R.kBlack)
b_glob.Draw()
print "#####################################################################"
print "Black Box Dimensions (global):"
print "(x1, x2)_glob = (",x1_glob, ",", x2_glob, ") -->", binxmax_glob-binxmin_glob, "bins"
print "(y1, y2)_glob = (",y1_glob, ",", y2_glob, ") -->", binymax_glob-binymin_glob, "bins"
print "Area_glob [bin^2] = ", A_glob
print "#####################################################################"

# according to parameters at the beginning, user can modify this global rectangular area
# for example, move one edge of rectangle into, and then let program run algorithm one more time
# to find another rectangle that might work better for the rest of the binning algorithm
binxmin_post,binxmax_post,binymin_post,binymax_post = test(h,not goRight,not goUp,not goLeft,not goDown,binxmin_glob+NbinsXmin,binxmax_glob+NbinsXmax,binymin_glob+NbinsYmin,binymax_glob+NbinsYmax)
A_post = (binxmax_post-binxmin_post)*(binymax_post-binymin_post)
x1_post = h.GetXaxis().GetBinLowEdge(binxmin_post)
x2_post = h.GetXaxis().GetBinUpEdge(binxmax_post)
y1_post = h.GetYaxis().GetBinLowEdge(binymin_post)
y2_post = h.GetYaxis().GetBinUpEdge(binymax_post)
b_post = R.TBox(x1_post, y1_post, x2_post, y2_post)
b_post.SetFillStyle(0)
b_post.SetLineWidth(3)
b_post.SetLineColor(R.kRed)
b_post.Draw()
print "#####################################################################"
print "Red Box Dimensions (post):"
print "(x1, x2)_post = (",x1_post, ",", x2_post, ") -->", binxmax_post-binxmin_post, "bins"
print "(y1, y2)_post = (",y1_post, ",", y2_post, ") -->", binymax_post-binymin_post, "bins"
print "Area_post [bin^2] = ", A_post
print "#####################################################################"

canv.SaveAs(sname+".pdf")
canv.SaveAs(sname+".png")

#xbins0 = [0]+linspace(x1_post,x2_post, binxmax_post-binxmin_post+2).tolist()+[1200]
#ybins0 = [-1]+linspace(y1_post,y2_post, binymax_post-binymin_post+2).tolist()+[1]
xbins0 = [h.GetXaxis().GetBinLowEdge(item) for item in range(1,h.GetXaxis().GetNbins())]+[h.GetXaxis().GetBinUpEdge(h.GetXaxis().GetNbins())]
ybins0 = [h.GetYaxis().GetBinLowEdge(item) for item in range(1,h.GetYaxis().GetNbins())]+[h.GetYaxis().GetBinUpEdge(h.GetYaxis().GetNbins())]
nxbins0 = len(xbins0)-1
nybins0 = len(ybins0)-1
xbins0 = array('f',xbins0)
ybins0 = array('f',ybins0)
hnew0 = R.TH2F("oldrebin0", hname, nxbins0,xbins0,nybins0,ybins0)
hnew0 = RFile.Get(hname).Clone()
xaxis = h.GetXaxis()
yaxis = h.GetYaxis()
for j in range(1,yaxis.GetNbins()+1):
	for i in range(1,xaxis.GetNbins()+1):
		hnew0.Fill(xaxis.GetBinCenter(i),yaxis.GetBinCenter(j),h.GetBinContent(i,j))

canv0 = R.TCanvas(hname+"_0",hname,1000,700)
canv0.SetTitle(hname)
hnew0.GetXaxis().SetTitle(h.GetXaxis().GetTitle())
hnew0.GetYaxis().SetTitle(h.GetYaxis().GetTitle())
hnew0.Draw("COLZ")
b_post.Draw()
Tex.DrawLatex(0.93, 0.92, hname)

# highlight the bins that are not satisfying the conditions on the original histogram
# i.e., show the bins that are empty or above statistical uncertainty threshold
b_temp = {}
for j in range(1,h.GetYaxis().GetNbins()+1):
	for i in range(1,h.GetXaxis().GetNbins()+1):
		if(h.GetBinContent(i,j)==0): 
			x1_temp = hnew0.GetXaxis().GetBinLowEdge(i)
			x2_temp = hnew0.GetXaxis().GetBinUpEdge(i)
			y1_temp = hnew0.GetYaxis().GetBinLowEdge(j)
			y2_temp = hnew0.GetYaxis().GetBinUpEdge(j)
			b_temp[str(i)+str(j)+str(j)] = R.TBox(x1_temp, y1_temp, x2_temp, y2_temp)
			b_temp[str(i)+str(j)+str(j)].SetFillStyle(0)
			b_temp[str(i)+str(j)+str(j)].SetLineWidth(3)
			b_temp[str(i)+str(j)+str(j)].SetLineColor(R.kBlack)
			b_temp[str(i)+str(j)+str(j)].Draw()
		elif(h.GetBinError(i,j)/h.GetBinContent(i,j)>stat): 
			x1_temp = hnew0.GetXaxis().GetBinLowEdge(i)
			x2_temp = hnew0.GetXaxis().GetBinUpEdge(i)
			y1_temp = hnew0.GetYaxis().GetBinLowEdge(j)
			y2_temp = hnew0.GetYaxis().GetBinUpEdge(j)
			b_temp[str(i)+str(j)+str(j)] = R.TBox(x1_temp, y1_temp, x2_temp, y2_temp)
			b_temp[str(i)+str(j)+str(j)].SetFillStyle(0)
			b_temp[str(i)+str(j)+str(j)].SetLineWidth(3)
			b_temp[str(i)+str(j)+str(j)].SetLineColor(R.kBlack)
			b_temp[str(i)+str(j)+str(j)].Draw()
canv0.SaveAs(sname+"_rebinned0.pdf")
canv0.SaveAs(sname+"_rebinned0.png")

#####################################################
# REBINNING EXTERIOR REGION OF THE RECTANGLE STARTS #
#####################################################

# moving to the right, merging bins as moved until all the bins to the right of the box 
# satisfy conditions altogether. This preserves the binning along the y-axis 
reBinContent = 0
reBinError = 0
isOK = True
reBinsXP = []
reBinContent = {}
reBinError = {}
for i in range (h.GetXaxis().GetNbins()): 
	reBinContent[i]=0
	reBinError[i]=0
for binxp in range(binxmax_post,h.GetXaxis().GetNbins()):
	for biny in range(binymin_post,binymax_post+1):
		reBinContent[biny] += h.GetBinContent(binxp,biny,binz0)
		reBinError[biny] += h.GetBinError(binxp,biny,binz0)*h.GetBinError(binxp,biny,binz0)
		if  (reBinContent[biny]==0): isOK=False
		elif (R.TMath.Sqrt(reBinError[biny])/reBinContent[biny]>stat): isOK=False
		#print reBinContent, reBinError,R.TMath.Sqrt(reBinError)/reBinContent
	if(isOK):
		reBinsXP.append(h.GetXaxis().GetBinUpEdge(binxp))
		#print binxmax_post, binxp
		for i in range (h.GetXaxis().GetNbins()): 
			reBinContent[i]=0
			reBinError[i]=0
	isOK=True
if(len(reBinsXP)>0):
	if(reBinsXP[-1]==h.GetXaxis().GetXmax()): reBinsXP = reBinsXP[:-1]
	if(not len(reBinsXP)==0):
		if(reBinsXP[0]==h.GetXaxis().GetBinUpEdge(binxmax_post)): reBinsXP = reBinsXP[1:]
#print reBinsXP, h.GetXaxis().GetNbins()

# moving to the left, merging bins as moved until all the bins to the left of the box 
# satisfy conditions altogether. This preserves the binning along the y-axis 
reBinContent = 0
reBinError = 0
isOK = True
reBinsXM = []
reBinContent = {}
reBinError = {}
for i in range (h.GetXaxis().GetNbins()): 
	reBinContent[i]=0
	reBinError[i]=0
for i in range(1,binxmin_post):
	binxm = binxmin_post-i
	for biny in range(binymin_post,binymax_post+1):
		reBinContent[biny] += h.GetBinContent(binxm,biny,binz0)
		reBinError[biny] += h.GetBinError(binxm,biny,binz0)*h.GetBinError(binxm,biny,binz0)
		if  (reBinContent[biny]==0): isOK=False
		elif (R.TMath.Sqrt(reBinError[biny])/reBinContent[biny]>stat): isOK=False
		#print reBinContent, reBinError,R.TMath.Sqrt(reBinError)/reBinContent
	if(isOK):
		reBinsXM.append(h.GetXaxis().GetBinLowEdge(binxm))
		#print binxmin_post, binxm
		for i in range (h.GetXaxis().GetNbins()): 
			reBinContent[i]=0
			reBinError[i]=0
	isOK=True
reBinsXM=reBinsXM[::-1]
if(len(reBinsXM)>0):
	if(reBinsXM[0]==h.GetXaxis().GetXmin()): reBinsXM = reBinsXM[1:]
	if(not len(reBinsXM)==0):
		if(reBinsXM[-1]==h.GetXaxis().GetBinLowEdge(binxmin_post)): reBinsXM = reBinsXM[:-1]
#print reBinsXM, h.GetXaxis().GetNbins()

# moving to up, merging bins as moved until all the bins to the top of the box 
# satisfy conditions altogether. This preserves the binning along the x-axis 
reBinContent = 0
reBinError = 0
isOK = True
reBinsYP = []
reBinContent = {}
reBinError = {}
for i in range (h.GetXaxis().GetNbins()): 
	reBinContent[i]=0
	reBinError[i]=0
for binyp in range(binymax_post,h.GetYaxis().GetNbins()):
	for binx in range(binxmin_post,binxmax_post+1):
		reBinContent[binx] += h.GetBinContent(binx,binyp,binz0)
		reBinError[binx] += h.GetBinError(binx,binyp,binz0)*h.GetBinError(binx,binyp,binz0)
		if  (reBinContent[binx]==0): isOK=False
		elif (R.TMath.Sqrt(reBinError[binx])/reBinContent[binx]>stat): isOK=False
	if(isOK):
		reBinsYP.append(h.GetYaxis().GetBinUpEdge(binyp))
		#print binymax_post, binyp
		for i in range (h.GetXaxis().GetNbins()): 
			reBinContent[i]=0
			reBinError[i]=0
	isOK=True
if(len(reBinsYP)>0):
	if(reBinsYP[-1]==h.GetYaxis().GetXmax()): reBinsYP = reBinsYP[:-1]
	if(not len(reBinsYP)==0):
		if(reBinsYP[0]==h.GetYaxis().GetBinUpEdge(binymax_post)): reBinsYP = reBinsYP[1:]
#print reBinsYP, h.GetYaxis().GetNbins()

# finally moving to down, merging bins as moved until all the bins to the bottom of the box 
# satisfy conditions altogether. This preserves the binning along the x-axis
reBinContent = 0
reBinError = 0
isOK = True
reBinsYM = []
reBinContent = {}
reBinError = {}
for i in range (h.GetXaxis().GetNbins()): 
	reBinContent[i]=0
	reBinError[i]=0
for i in range(1,binymin_post):
	binym = binymin_post-i
	for binx in range(binxmin_post,binxmax_post+1):
		reBinContent[binx] += h.GetBinContent(binx,binym,binz0)
		reBinError[binx] += h.GetBinError(binx,binym,binz0)*h.GetBinError(binx,binym,binz0)
		if  (reBinContent[binx]==0): isOK=False
		elif (R.TMath.Sqrt(reBinError[binx])/reBinContent[binx]>stat): isOK=False
		#print reBinContent, reBinError,R.TMath.Sqrt(reBinError)/reBinContent
	if(isOK):
		reBinsYM.append(h.GetYaxis().GetBinLowEdge(binym))
		#print binymin_post, binym
		for i in range (h.GetXaxis().GetNbins()): 
			reBinContent[i]=0
			reBinError[i]=0
	isOK=True
reBinsYM=reBinsYM[::-1]
if(len(reBinsYM)>0):
	if(reBinsYM[0]==h.GetYaxis().GetXmin()): reBinsYM = reBinsYM[1:]
	if(not len(reBinsYM)==0):
		if(reBinsYM[-1]==h.GetYaxis().GetBinLowEdge(binymin_post)): reBinsYM = reBinsYM[:-1]
#print reBinsYM, h.GetYaxis().GetNbins()

###################################################
# REBINNING EXTERIOR REGION OF THE RECTANGLE ENDS #
###################################################

# Rebinning the histogram with the results found
xEdgeMin, xEdgeMax, yEdgeMin, yEdgeMax = [], [], [],[]
if not x1_post==h.GetXaxis().GetXmin():xEdgeMin=[h.GetXaxis().GetXmin()]
if not x2_post==h.GetXaxis().GetXmax():xEdgeMax=[h.GetXaxis().GetXmax()]
if not y1_post==h.GetYaxis().GetXmin():yEdgeMin=[h.GetYaxis().GetXmin()]
if not y2_post==h.GetYaxis().GetXmax():yEdgeMax=[h.GetYaxis().GetXmax()]
xbins1List = xEdgeMin+reBinsXM[mergeFirstXbin:]+linspace(x1_post,x2_post, binxmax_post-binxmin_post+2).tolist()+reBinsXP[:mergeLastXbin]+xEdgeMax
ybins1List = yEdgeMin+reBinsYM[mergeFirstYbin:]+linspace(y1_post,y2_post, binymax_post-binymin_post+2).tolist()+reBinsYP[:mergeLastYbin]+yEdgeMax
nxbins1 = len(xbins1List)-1
nybins1 = len(ybins1List)-1
xbins1 = array('f',xbins1List)
ybins1 = array('f',ybins1List)
hnew1 = R.TH2F("oldrebin1", hname, nxbins1, xbins1, nybins1, ybins1)
"""
xbins1List = linspace(0,1200,50).tolist()
ybins1List = linspace(-1,1,50).tolist()
nxbins1 = len(xbins1List)-1
nybins1 = len(ybins1List)-1
xbins1 = array('f',xbins1List)
ybins1 = array('f',ybins1List)
hnew1 = R.TH2F("oldrebin1", hname, nxbins1, xbins1, nybins1, ybins1)
"""
# first fill the histogram with new binning
for j in range(1,yaxis.GetNbins()+1):
	for i in range(1,xaxis.GetNbins()+1):
		hnew1.Fill(xaxis.GetBinCenter(i),yaxis.GetBinCenter(j),h.GetBinContent(i,j))

# calculate and set the new errors of the bins
xBin1ErrorList=[]
yBin1ErrorList=[]
for jold in range(1,yaxis.GetNbins()+1):
	for jnew in range(1,nybins1+1):
		if(abs(h.GetYaxis().GetBinUpEdge(jold)-hnew1.GetYaxis().GetBinUpEdge(jnew))<1e-4):
			yBin1ErrorList.append(jold)
			break
for iold in range(1,xaxis.GetNbins()+1):
	for inew in range(1,nxbins1+1):
		if(abs(h.GetXaxis().GetBinUpEdge(iold)-hnew1.GetXaxis().GetBinUpEdge(inew))<1e-4):
			xBin1ErrorList.append(iold)
			break
print xbins1List, ybins1List
print xBin1ErrorList, yBin1ErrorList
print len(xBin1ErrorList), len(yBin1ErrorList), nxbins1, nybins1
for j in range(1,nybins1+1):
	for i in range(1,nxbins1+1):
		startX=1
		if(i>1):startX=xBin1ErrorList[i-2]+1
		startY=1
		if(j>1):startY=yBin1ErrorList[j-2]+1
		endX=xBin1ErrorList[i-1]+1
		endY=yBin1ErrorList[j-1]+1
		errorTemp=0
		#print startX,endX
		#print startY,endY
		for k in range(startX,endX):
			for l in range(startY,endY):
				errorTemp+=h.GetBinError(k,l,binz0)*h.GetBinError(k,l,binz0)
		hnew1.SetBinError(i,j,R.TMath.Sqrt(errorTemp))
		#print R.TMath.Sqrt(errorTemp)/hnew1.GetBinContent(i,j,binz0)

canv1 = R.TCanvas(hname+"_1",hname,1000,700)
canv1.SetTitle(hname)
hnew1.GetXaxis().SetTitle(h.GetXaxis().GetTitle())
hnew1.GetYaxis().SetTitle(h.GetYaxis().GetTitle())
hnew1.Draw("COLZ")
b_post.Draw()

# show the bins that are not satisfying conditions after all!
b_temp = {}
ii = 0
jj = 0
for j in range(1,hnew1.GetYaxis().GetNbins()+1):
	for i in range(1,hnew1.GetXaxis().GetNbins()+1):
		if(hnew1.GetBinContent(i,j)==0): 
			x1_temp = hnew1.GetXaxis().GetBinLowEdge(i)
			x2_temp = hnew1.GetXaxis().GetBinUpEdge(i)
			y1_temp = hnew1.GetYaxis().GetBinLowEdge(j)
			y2_temp = hnew1.GetYaxis().GetBinUpEdge(j)
			b_temp[str(i)+str(j)+str(j)] = R.TBox(x1_temp, y1_temp, x2_temp, y2_temp)
			b_temp[str(i)+str(j)+str(j)].SetFillStyle(1)
			b_temp[str(i)+str(j)+str(j)].SetLineWidth(3)
			b_temp[str(i)+str(j)+str(j)].SetLineColor(R.kBlack)
			b_temp[str(i)+str(j)+str(j)].Draw()
		elif(hnew1.GetBinError(i,j)/hnew1.GetBinContent(i,j)>stat): 
			x1_temp = hnew1.GetXaxis().GetBinLowEdge(i)
			x2_temp = hnew1.GetXaxis().GetBinUpEdge(i)
			y1_temp = hnew1.GetYaxis().GetBinLowEdge(j)
			y2_temp = hnew1.GetYaxis().GetBinUpEdge(j)
			b_temp[str(i)+str(j)+str(j)] = R.TBox(x1_temp, y1_temp, x2_temp, y2_temp)
			b_temp[str(i)+str(j)+str(j)].SetFillStyle(0)#3004
			b_temp[str(i)+str(j)+str(j)].SetFillColor(R.kBlack)
			b_temp[str(i)+str(j)+str(j)].SetLineWidth(3)
			b_temp[str(i)+str(j)+str(j)].SetLineColor(R.kBlack)
			b_temp[str(i)+str(j)+str(j)].Draw()

canv1.SaveAs(sname+"_rebinned1.pdf")
canv1.SaveAs(sname+"_rebinned1.png")

print "#####################################################################"
print hname
print "#####################################################################"
print "#####################################################################"
print "New Bins to be used in doPostProc.py :"
print "#####################################################################"
print "xbins = ", xbins1List, nxbins1
print "ybins = ", ybins1List, nybins1
print "#####################################################################"
logFile = open(sname + '_rebinned1.txt','a')
sys.stdout = logFile
print hname
print "******************************************"
print "Configuration Parameters :"
print "******************************************"
print "goUp    = ",goUp
print "goDown  = ",goDown
print "goRight = ",goRight
print "goLeft  = ",goLeft
print " "
print "NbinsXmin = ",NbinsXmin
print "NbinsXmax = ",NbinsXmax
print "NbinsYmin = ",NbinsYmin
print "NbinsYmax = ",NbinsYmax
print " "
print "mergeFirstXbin = ",mergeFirstXbin
print "mergeLastXbin  = ",mergeLastXbin
print "mergeFirstYbin = ",mergeFirstYbin
print "mergeLastYbin  = ",mergeLastYbin
print " "
print "Note : ", note
print "******************************************"
print "New Bins to be used in doPostProc.py :"
print "******************************************"
print "Nxbins = ", nxbins1
print "xbins = ", xbins1List
print "ybins = ", nybins1
print "ybins = ", ybins1List
print "******************************************"
logFile.close()
