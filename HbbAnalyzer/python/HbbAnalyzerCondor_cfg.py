import FWCore.ParameterSet.Config as cms
import sys, os, subprocess
from subprocess import call
import ConfigParser
from optparse import OptionParser
import glob

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")


def usage():
    """ Usage: HbbAnalyzer [options] outputFile inputFiles ( --hh for options)

    """
    pass


class JobPar:
    def __init__(self):
        getJobopt(self)

def getJobopt(self):


    parser = OptionParser(usage=usage.__doc__)
    parser.add_option("-n", "--nevts", dest="nevts", default=-1, type="int",
                      help="number of events to process (default=-1 (all))")
    parser.add_option("--hh", action="store_true", dest="help",default=False,
                      help="print help")

    (options, args) = parser.parse_args()

    narg=len(args)

    if options.help:
        parser.print_help()
        sys.exit(0)

    if narg < 3 :
        print usage.__doc__
        parser.print_help()
        sys.exit(1)


    self.outFile       = args[1]
    self.inputFiles    = args[2]
    self.nevts         = options.nevts


jobpar=JobPar()

print jobpar.outFile
print jobpar.inputFiles
print jobpar.nevts
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(jobpar.nevts) )

allfiles = glob.glob(jobpar.inputFiles + "*/Hbb*.root")
#print "allfiles ", allfiles
infiles = []
for f in allfiles:
    infiles.append('file:' + f)

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        infiles
    )
)

process.load('VHbb.HbbAnalyzer.HbbAnalyzer_cfi')

#process.demo = cms.EDAnalyzer('HbbAnalyzer'
#)

process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)

process.load('CommonTools.UtilAlgos.TFileService_cfi')
#process.TFileService.fileName=cms.string('HbbAna.root')
process.TFileService.fileName=cms.string(jobpar.outFile)
#process.out = cms.OutputModule("PoolOutputModule",
#                               fileName = cms.untracked.string('HbbAna.root'),
#                               outputCommands = cms.untracked.vstring(['keep *_HbbAnalyzer_*_*',
#                                                                       ])
#)

#process.end = cms.EndPath(process.out)
process.p = cms.Path(process.HbbAnalyzer)
