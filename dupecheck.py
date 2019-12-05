#!/usr/bin/env python2.7
import os, math, sys, re
from ROOT import TFile, gROOT, TTree, Double, TChain, TMath

gROOT.SetBatch(True)

# inputfile = TFile.Open('/eos/home-w/wvetens/tmp/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018C-17Sep2018-v1/CondorJob_9.root')
inputfile = TFile.Open('/eos/home-w/wvetens/Ntuple_BPH_v0/BJpsiX_MuMu_031019/BJpsiX_MuMu_031019/Btrimu.root')
tree = inputfile.Get('tree')
invars = ['Jpsi_mu1_pt', 'Jpsi_mu1_eta', 'Jpsi_mu1_phi', 'Jpsi_mu2_pt', 'Jpsi_mu2_eta', 'Jpsi_mu2_phi', 'Jpsi_mu3_pt', 'Jpsi_mu3_eta', 'Jpsi_mu3_phi', 'Jpsi_trimu_mass']
tree.SetBranchStatus('*', 0)
for var in invars:     
    tree.SetBranchStatus(var, 1)
Nentries = inputfile.Get('cuthist').GetBinContent(2)
npass=0
nbcand=0
closematch=0

for evt in xrange(int(Nentries)):
#for evt in xrange(100):
    tree.GetEntry(evt)
    #for iJpsi in xrange(tree.Jpsi_mu3_pt.size()):
    iJpsi=0
    nbcand+=1
    dupe = False
    mu1pt = tree.Jpsi_mu1_pt[iJpsi]
    mu1eta = tree.Jpsi_mu1_eta[iJpsi]
    mu1phi = tree.Jpsi_mu1_phi[iJpsi]
    mu2pt = tree.Jpsi_mu2_pt[iJpsi]
    mu2eta = tree.Jpsi_mu2_eta[iJpsi]
    mu2phi = tree.Jpsi_mu2_phi[iJpsi]
    mu3pt = tree.Jpsi_mu3_pt[iJpsi]
    mu3eta = tree.Jpsi_mu3_eta[iJpsi]
    mu3phi = tree.Jpsi_mu3_phi[iJpsi]
    trimumass = tree.Jpsi_trimu_mass[iJpsi]
    #print "Event number: ", evt, " Mu 3 pT: ", mu3pt, " eta: ", mu3eta, " phi: ", mu3phi
    for evt2 in xrange(evt+1, int(Nentries)):
    #for evt2 in xrange(evt+1, 100):
        #print "Checking with event number: ", evt2
        if dupe == False:
            #print "Isn't already a duplicate!"
            tree.GetEntry(evt2)
            #for iJpsi2 in xrange(tree.Jpsi_mu3_pt.size()):
            iJpsi2 = 0
            if tree.Jpsi_mu3_pt[iJpsi2] == mu3pt:
                if tree.Jpsi_mu3_pt[iJpsi2]/mu3pt < 1.001 and tree.Jpsi_mu3_pt[iJpsi2]/mu3pt > 0.999:
                    if tree.Jpsi_mu3_eta[iJpsi2]/mu3eta < 1.001 and tree.Jpsi_mu3_eta[iJpsi2]/mu3eta > 0.999:
                        if tree.Jpsi_trimu_mass[iJpsi2]/trimumass < 1.001 and tree.Jpsi_trimu_mass[iJpsi2]/trimumass > 0.999:
                    #print "Close match between events: ", evt, " and ", evt2
                            closematch+=1
                #print "mu3 pT Match!"
                if tree.Jpsi_mu3_eta[iJpsi2] == mu3eta and tree.Jpsi_mu3_phi[iJpsi2] == mu3phi:
                    #print "mu3 eta and phi match!!"
                    if ( mu2pt == tree.Jpsi_mu2_pt[iJpsi2] and
                         mu2eta == tree.Jpsi_mu2_eta[iJpsi2] and
                         mu2phi == tree.Jpsi_mu2_phi[iJpsi2] and
                         mu1pt == tree.Jpsi_mu1_pt[iJpsi2] and
                         mu1eta == tree.Jpsi_mu1_eta[iJpsi2] and
                         mu1phi == tree.Jpsi_mu1_phi[iJpsi2] ):
                        dupe = True
                        #print "Match! Mu 3 pT for event ", evt2, ": ", tree.Jpsi_mu3_pt[iJpsi2]
    if not dupe: 
        npass+=1
print "Number of Events post-cut: ", Nentries
print "Number of B candidates: ", nbcand
print "Number of B candidates Passed: ", npass
print "Number of close matches between mu3 pt: ", closematch
print "Percentage of B candidates which were duplicates: ", 100-100*npass/nbcand
