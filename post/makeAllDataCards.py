from DataCard import *
from sys import argv

###############################################################################################
#
# doPostProc.py creates dataCard with 0P and 0M signals by default, for hypothesis testing.
# This script makes separate dataCards for 0P, 0M, and 50/50 mix for simple limit setting.
# Usage: python makeAllDataCards.py <inputDir>
# <inputDir> should contain a 'yields.p' pickle file from which a dataCard can be constructed.
#
###############################################################################################

try: inputDir=argv[1]
except:
    print "No input dir specified"
    exit(1)

try: distribution=argv[2]
except: distribution=None

#            0P signif/excl          0M signif/exlc         fa3 (combo)
signals=    [['Wh_125p6_0P']       ,['Wh_125p6_0M']       ,defaultSignalNames+['Zh_125p6_0P','Zh_125p6_0M','ggZh','ggZhTriangleOnly','ggZhBoxOnly']]
backgrounds=[defaultBackgroundNames,defaultBackgroundNames,[x for x in defaultBackgroundNames if x != 'Zh_125p6_0P' and x != 'ggZh']]
cardNames=  ['dataCard_0P'         ,'dataCard_0M'         ,'dataCard_combo']

for signal,background,cardName in zip(signals,backgrounds,cardNames):

    theCard=DataCard(signalNames=signal, backgroundNames=background)
    theCard.fromPickle(inputDir+'/yields.p')
    if distribution: theCard.distribution=distribution
    theCard.construct()

    theCard.toTxt(inputDir+'/'+cardName+'.txt')

    
