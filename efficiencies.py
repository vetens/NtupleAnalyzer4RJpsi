
import collections
import itertools
import shutil
import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack, TMath, TCanvas, TLegend, TEventList, TDirectory, gObjectTable, TLine, TH2F
from samples import *

from optparse import OptionParser, OptionValueError
import argparse

usage = "usage: python efficiencies.py [--sample: <string with name of sample in samples.py> (default: 'signal_BcJpsiMuNu)] [--nevts: <N_EVTS> ] [--uncert: <Uncertainty in N_EVTS> ] [--cuts: <string with list of cuts> (default: '')]"
parser = OptionParser(usage)
parser.add_option("--sample", default='signal_BcJpsiMuNu', action="store", help="sample to calculate efficiencies or sigma * BR for", dest="sample")
parser.add_option("--nevts", default=0, action="store", help="Number of expected events (to be got from stefanos' fit code)", dest="nevts")
parser.add_option("--uncert", default=0, action="store", help="Uncertainty in Number of expected events (to be got from stefanos' fit code)", dest="uncert")
parser.add_option("--cuts", default='', action="store", help="List of Cuts to apply", dest="cuts")

(options, args) = parser.parse_args()

samplefile = sampledict[options.sample]['file']
tree = samplefile.Get('tree')
cuthist = samplefile.Get('cuthist')
NGenerated = cuthist.GetBinContent(1)
print "Generated events: ", NGenerated
hist = TH1F('h', 'h', 60, 3, 9)
hist.Sumw2()
tree.Draw("JpsiMu_B_mass >> h", options.cuts)
NPassed = hist.Integral()
exA = 0
if NGenerated:
    exA = float(NPassed)/float(NGenerated)
    print "Efficiency x Acceptance = ", exA
else:
    print "There seem to be Zero Generated events..."
if options.nevts:
    if exA:
        sigmaBr = float(options.nevts) / (exA * (lumi / 1000.0))
        if options.uncert:
            uncert_sigmaBr = float(options.uncert) / (exA * (lumi / 1000.0))
        else:
            uncert_sigmaBr = 0
        print "sigma x BR = ", sigmaBr, " +/- ", uncert_sigmaBr, " fb"
    else:
        print "ERROR: efficiency = 0"
