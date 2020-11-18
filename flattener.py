import collections
import itertools
import shutil
import math, os, sys
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, Double, TChain, TMath
import numpy as num

from optparse import OptionParser, OptionValueError

from samples import *

usage = "usage: python flattener.py [--odir: <OUTPUT DIRECTORY> (default : '')]"
parser = OptionParser(usage)

parser.add_option("-o", "--odir", default='', type ="string", help="output directory", dest="odir")
parser.add_option("-d", "--debug", default=False, action="store_true", help="debug mode", dest="debug")
parser.add_option("-g", "--genlevel", default=False, action="store_true", help="are you doing gen level?", dest="isGen")

(options, args) = parser.parse_args()

if options.odir:
    whereIsItSaved = options.odir
else:
    whereIsItSaved = "DEFAULT"

print 'Output Directory: ', whereIsItSaved

gROOT.SetBatch(True)
flattenedLocations = open("flatsamples.py", "w")

for samplekey, sample in sampledict.iteritems():
    infile = sample['file']
    lowpt_eff_ID_file = TFile('MuonReferenceEfficiencies/EfficienciesStudies/2018/Jpsi/rootfiles/RunABCD_SF_ID.root')
    #Eta is y axis pT is x axis
    # Eta goes from 0 to 2.4, pT goes from 0 to 40 GeV
    lowpt_eff_ID_hist = lowpt_eff_ID_file.Get('NUM_TightID_DEN_genTracks_pt_abseta')
    #lowpt_eff_ISO_file = TFile('MuonReferenceEfficiencies/EfficienciesStudies/2018/Jpsi/rootfiles/RunABCD_SF_ISO.root')
    print "Processing Sample: ", samplekey
    intree = infile.Get('tree')
    flattenedLocations.write("sampledict['"+str(samplekey)+"']['flatfile'] = TFile('"+options.odir+"' + 'flatTuple_' + '"+samplekey+"' + '.root')\n")
    flatfile = options.odir + 'flatTuple_' + samplekey + '.root'
    outputfile = TFile(flatfile, 'recreate')
    intree.SetBranchStatus('*', 1)
    otree = TTree('tree', 'tree')
    Ninit = infile.Get('cuthist').GetBinContent(1)
    print "initial number of events", Ninit

    Nevts = num.zeros(1, dtype=int)
    otree.Branch('Nevts', Nevts, 'Nevts/I')
    PV_N = num.zeros(1, dtype=int)
    otree.Branch('PV_N', PV_N, 'PV_N/I')

    JpsiMu_mu1_pt = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu1_pt', JpsiMu_mu1_pt, 'JpsiMu_mu1_pt/D')
    JpsiMu_mu1_eta = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu1_eta', JpsiMu_mu1_eta, 'JpsiMu_mu1_eta/D')
    JpsiMu_mu1_phi = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu1_phi', JpsiMu_mu1_phi, 'JpsiMu_mu1_phi/D')
    JpsiMu_mu1_isLoose = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu1_isLoose', JpsiMu_mu1_isLoose, 'JpsiMu_mu1_isLoose/B')
    JpsiMu_mu1_isTight = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu1_isTight', JpsiMu_mu1_isTight, 'JpsiMu_mu1_isTight/B')
    JpsiMu_mu1_isPF = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu1_isPF', JpsiMu_mu1_isPF, 'JpsiMu_mu1_isPF/B')
    JpsiMu_mu1_isGlobal = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu1_isGlobal', JpsiMu_mu1_isGlobal, 'JpsiMu_mu1_isGlobal/B')
    JpsiMu_mu1_isTracker = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu1_isTracker', JpsiMu_mu1_isTracker, 'JpsiMu_mu1_isTracker/B')
    JpsiMu_mu1_isSoft = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu1_isSoft', JpsiMu_mu1_isSoft, 'JpsiMu_mu1_isSoft/B')
    JpsiMu_mu1_dbiso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu1_dbiso', JpsiMu_mu1_dbiso, 'JpsiMu_mu1_dbiso/D')

    JpsiMu_mu2_pt = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu2_pt', JpsiMu_mu2_pt, 'JpsiMu_mu2_pt/D')
    JpsiMu_mu2_eta = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu2_eta', JpsiMu_mu2_eta, 'JpsiMu_mu2_eta/D')
    JpsiMu_mu2_phi = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu2_phi', JpsiMu_mu2_phi, 'JpsiMu_mu2_phi/D')
    JpsiMu_mu2_isLoose = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu2_isLoose', JpsiMu_mu2_isLoose, 'JpsiMu_mu2_isLoose/B')
    JpsiMu_mu2_isTight = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu2_isTight', JpsiMu_mu2_isTight, 'JpsiMu_mu2_isTight/B')
    JpsiMu_mu2_isPF = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu2_isPF', JpsiMu_mu2_isPF, 'JpsiMu_mu2_isPF/B')
    JpsiMu_mu2_isGlobal = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu2_isGlobal', JpsiMu_mu2_isGlobal, 'JpsiMu_mu2_isGlobal/B')
    JpsiMu_mu2_isTracker = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu2_isTracker', JpsiMu_mu2_isTracker, 'JpsiMu_mu2_isTracker/B')
    JpsiMu_mu2_isSoft = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu2_isSoft', JpsiMu_mu2_isSoft, 'JpsiMu_mu2_isSoft/B')
    JpsiMu_mu2_dbiso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu2_dbiso', JpsiMu_mu2_dbiso, 'JpsiMu_mu2_dbiso/D')

    JpsiMu_mu3_pt = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu3_pt', JpsiMu_mu3_pt, 'JpsiMu_mu3_pt/D')
    JpsiMu_mu3_eta = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu3_eta', JpsiMu_mu3_eta, 'JpsiMu_mu3_eta/D')
    JpsiMu_mu3_phi = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu3_phi', JpsiMu_mu3_phi, 'JpsiMu_mu3_phi/D')
    JpsiMu_mu3_isLoose = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu3_isLoose', JpsiMu_mu3_isLoose, 'JpsiMu_mu3_isLoose/B')
    JpsiMu_mu3_isTight = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu3_isTight', JpsiMu_mu3_isTight, 'JpsiMu_mu3_isTight/B')
    JpsiMu_mu3_isPF = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu3_isPF', JpsiMu_mu3_isPF, 'JpsiMu_mu3_isPF/B')
    JpsiMu_mu3_isGlobal = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu3_isGlobal', JpsiMu_mu3_isGlobal, 'JpsiMu_mu3_isGlobal/B')
    JpsiMu_mu3_isTracker = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu3_isTracker', JpsiMu_mu3_isTracker, 'JpsiMu_mu3_isTracker/B')
    JpsiMu_mu3_isSoft = num.zeros(1, dtype=bool)
    otree.Branch('JpsiMu_mu3_isSoft', JpsiMu_mu3_isSoft, 'JpsiMu_mu3_isSoft/B')
    JpsiMu_mu3_dbiso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu3_dbiso', JpsiMu_mu3_dbiso, 'JpsiMu_mu3_dbiso/D')

    JpsiMu_Jpsi_pt = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_pt', JpsiMu_Jpsi_pt, 'JpsiMu_Jpsi_pt/D')
    JpsiMu_Jpsi_eta = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_eta', JpsiMu_Jpsi_eta, 'JpsiMu_Jpsi_eta/D')
    JpsiMu_Jpsi_phi = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_phi', JpsiMu_Jpsi_phi, 'JpsiMu_Jpsi_phi/D')
    JpsiMu_Jpsi_vprob = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_vprob', JpsiMu_Jpsi_vprob, 'JpsiMu_Jpsi_vprob/D')
    JpsiMu_Jpsi_lip = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_lip', JpsiMu_Jpsi_lip, 'JpsiMu_Jpsi_lip/D')
    JpsiMu_Jpsi_lips = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_lips', JpsiMu_Jpsi_lips, 'JpsiMu_Jpsi_lips/D')
    JpsiMu_Jpsi_pvip = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_pvip', JpsiMu_Jpsi_pvip, 'JpsiMu_Jpsi_pvip/D')
    JpsiMu_Jpsi_pvips = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_pvips', JpsiMu_Jpsi_pvips, 'JpsiMu_Jpsi_pvips/D')
    JpsiMu_Jpsi_fl3d = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_fl3d', JpsiMu_Jpsi_fl3d, 'JpsiMu_Jpsi_fl3d/D')
    JpsiMu_Jpsi_fls3d = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_fls3d', JpsiMu_Jpsi_fls3d, 'JpsiMu_Jpsi_fls3d/D')
    JpsiMu_Jpsi_alpha = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_alpha', JpsiMu_Jpsi_alpha, 'JpsiMu_Jpsi_alpha/D')
    JpsiMu_Jpsi_maxdoca = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_maxdoca', JpsiMu_Jpsi_maxdoca, 'JpsiMu_Jpsi_maxdoca/D')
    JpsiMu_Jpsi_mindoca = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_mindoca', JpsiMu_Jpsi_mindoca, 'JpsiMu_Jpsi_mindoca/D')
    JpsiMu_Jpsi_unfit_mass = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_Jpsi_unfit_mass', JpsiMu_Jpsi_unfit_mass, 'JpsiMu_Jpsi_unfit_mass/D')

    JpsiMu_B_pt = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_pt', JpsiMu_B_pt, 'JpsiMu_B_pt/D')
    JpsiMu_B_eta = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_eta', JpsiMu_B_eta, 'JpsiMu_B_eta/D')
    JpsiMu_B_phi = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_phi', JpsiMu_B_phi, 'JpsiMu_B_phi/D')
    JpsiMu_B_vprob = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_vprob', JpsiMu_B_vprob, 'JpsiMu_B_vprob/D')
    JpsiMu_B_lip = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_lip', JpsiMu_B_lip, 'JpsiMu_B_lip/D')
    JpsiMu_B_lips = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_lips', JpsiMu_B_lips, 'JpsiMu_B_lips/D')
    JpsiMu_B_pvip = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_pvip', JpsiMu_B_pvip, 'JpsiMu_B_pvip/D')
    JpsiMu_B_pvips = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_pvips', JpsiMu_B_pvips, 'JpsiMu_B_pvips/D')
    JpsiMu_B_fl3d = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_fl3d', JpsiMu_B_fl3d, 'JpsiMu_B_fl3d/D')
    JpsiMu_B_fls3d = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_fls3d', JpsiMu_B_fls3d, 'JpsiMu_B_fls3d/D')
    JpsiMu_B_alpha = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_alpha', JpsiMu_B_alpha, 'JpsiMu_B_alpha/D')
    JpsiMu_B_maxdoca = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_maxdoca', JpsiMu_B_maxdoca, 'JpsiMu_B_maxdoca/D')
    JpsiMu_B_mindoca = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_mindoca', JpsiMu_B_mindoca, 'JpsiMu_B_mindoca/D')
    JpsiMu_B_mass = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_mass', JpsiMu_B_mass, 'JpsiMu_B_mass/D')
    JpsiMu_B_iso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_iso', JpsiMu_B_iso, 'JpsiMu_B_iso/D')
    JpsiMu_B_iso_ntracks = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_iso_ntracks', JpsiMu_B_iso_ntracks, 'JpsiMu_B_iso_ntracks/D')
    JpsiMu_B_iso_mindoca = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_iso_mindoca', JpsiMu_B_iso_mindoca, 'JpsiMu_B_iso_mindoca/D')

    JpsiMu_B_mcorr = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_mcorr', JpsiMu_B_mcorr, 'JpsiMu_B_mcorr/D')
    JpsiMu_B_reliso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_B_reliso', JpsiMu_B_reliso, 'JpsiMu_B_reliso/D')
    JpsiMu_mu1_reldbiso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu1_reldbiso', JpsiMu_mu1_reldbiso, 'JpsiMu_mu1_reldbiso/D')
    JpsiMu_mu2_reldbiso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu2_relidbso', JpsiMu_mu2_reldbiso, 'JpsiMu_mu2_reldbiso/D')
    JpsiMu_mu3_reldbiso = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_mu3_reldbiso', JpsiMu_mu3_reldbiso, 'JpsiMu_mu3_reldbiso/D')
    JpsiMu_dphi_mu2_mu3 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_dphi_mu2_mu3', JpsiMu_dphi_mu2_mu3, 'JpsiMu_dphi_mu2_mu3/D')
    JpsiMu_cosdphi_mu2_mu3 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_cosdphi_mu2_mu3', JpsiMu_cosdphi_mu2_mu3, 'JpsiMu_cosdphi_mu2_mu3/D')
    JpsiMu_dR_mu2_mu3 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_dR_mu2_mu3', JpsiMu_dR_mu2_mu3, 'JpsiMu_dR_mu2_mu3/D')
    JpsiMu_dphi_mu1_mu3 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_dphi_mu1_mu3', JpsiMu_dphi_mu1_mu3, 'JpsiMu_dphi_mu1_mu3/D')
    JpsiMu_cosdphi_mu1_mu3 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_cosdphi_mu1_mu3', JpsiMu_cosdphi_mu1_mu3, 'JpsiMu_cosdphi_mu1_mu3/D')
    JpsiMu_dR_mu1_mu3 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_dR_mu1_mu3', JpsiMu_dR_mu1_mu3, 'JpsiMu_dR_mu1_mu3/D')
    JpsiMu_dphi_mu1_mu2 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_dphi_mu1_mu2', JpsiMu_dphi_mu1_mu2, 'JpsiMu_dphi_mu1_mu2/D')
    JpsiMu_cosdphi_mu1_mu2 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_cosdphi_mu1_mu2', JpsiMu_cosdphi_mu1_mu2, 'JpsiMu_cosdphi_mu1_mu2/D')
    JpsiMu_dR_mu1_mu2 = num.zeros(1, dtype=float)
    otree.Branch('JpsiMu_dR_mu1_mu2', JpsiMu_dR_mu1_mu2, 'JpsiMu_dR_mu1_mu2/D')

    if "Dat" not in samplekey and 'dat' not in samplekey:
        if options.isGen and "Tau" not in samplekey and "OniaAndX" not in samplekey:
            genParticle_pt = num.zeros(1, dtype=float)
            otree.Branch('genParticle_pt', genParticle_pt, 'genParticle_pt/D')
            genParticle_eta = num.zeros(1, dtype=float)
            otree.Branch('genParticle_eta', genParticle_eta, 'genParticle_eta/D')
            genParticle_phi = num.zeros(1, dtype=float)
            otree.Branch('genParticle_phi', genParticle_phi, 'genParticle_phi/D')
            genParticle_pdgId = num.zeros(1, dtype=int)
            otree.Branch('genParticle_pdgId', genParticle_pdgId, 'genParticle_pdgId/I')
            genParticle_status = num.zeros(1, dtype=int)
            otree.Branch('genParticle_status', genParticle_status, 'genParticle_status/I')
            JpsiGen = num.zeros(1, dtype=bool)
            otree.Branch('JpsiGen', JpsiGen, 'JpsiGen/B')
            genBc_pt= num.zeros(1, dtype=float)
            otree.Branch('genBc_pt', genBc_pt, 'genBc_pt/D')

        nPuVtxTrue = num.zeros(1, dtype=int)
        otree.Branch('nPuVtxTrue', nPuVtxTrue, 'nPuVtxTrue/I')
        bX = num.zeros(1, dtype=int)
        otree.Branch('bX', bX, 'bX/I')

        weight_pu = num.zeros(1, dtype=float)
        otree.Branch('weight_pu', weight_pu, 'weight_pu/D')

        weight_total = num.zeros(1, dtype=float)
        otree.Branch('weight_total', weight_total, 'weight_total/D')

        weight_total_up = num.zeros(1, dtype=float)
        otree.Branch('weight_total_up', weight_total_up, 'weight_total_up/D')

        weight_total_down = num.zeros(1, dtype=float)
        otree.Branch('weight_total_down', weight_total_down, 'weight_total_down/D')

        weight_SF_ID = num.zeros(1, dtype=float)
        otree.Branch('weight_SF_ID', weight_SF_ID, 'weight_SF_ID/D')

        weight_SF_ID_up = num.zeros(1, dtype=float)
        otree.Branch('weight_SF_ID_up', weight_SF_ID_up, 'weight_SF_ID_up/D')

        weight_SF_ID_down = num.zeros(1, dtype=float)
        otree.Branch('weight_SF_ID_down', weight_SF_ID_down, 'weight_SF_ID_down/D')

        weight_crossec = num.zeros(1, dtype=float)
        otree.Branch('weight_crossec', weight_crossec, 'weight_crossec/D')

        #weight_crossec_up = num.zeros(1, dtype=float)
        #otree.Branch('weight_crossec_up', weight_crossec_up, 'weight_crossec_up/D')

        #weight_crossec_down = num.zeros(1, dtype=float)
        #otree.Branch('weight_crossec_down', weight_crossec_down, 'weight_crossec_down/D')
        if "OniaAndX" in samplekey and options.isGen:
            isBplusJpsiKplus = num.zeros(1, dtype=bool)
            otree.Branch('isBplusJpsiKplus', isBplusJpsiKplus, 'isBplusJpsiKplus/B')
            isBplusJpsiPiplus = num.zeros(1, dtype=bool)
            otree.Branch('isBplusJpsiPiplus', isBplusJpsiPiplus, 'isBplusJpsiPiplus/B')
            isBplusJpsiKPiPiplus = num.zeros(1, dtype=bool)
            otree.Branch('isBplusJpsiKPiPiplus', isBplusJpsiKPiPiplus, 'isBplusJpsiKPiPiplus/B')
            isBplusJpsi3Kplus = num.zeros(1, dtype=bool)
            otree.Branch('isBplusJpsi3Kplus', isBplusJpsi3Kplus, 'isBplusJpsi3Kplus/B')
            isBplusJpsiPhiKplus = num.zeros(1, dtype=bool)
            otree.Branch('isBplusJpsiPhiKplus', isBplusJpsiPhiKplus, 'isBplusJpsiPhiKplus/B')
            isBplusJpsiK0Piplus = num.zeros(1, dtype=bool)
            otree.Branch('isBplusJpsiK0Piplus', isBplusJpsiK0Piplus, 'isBplusJpsiK0Piplus/B')

    Nevt = intree.GetEntries()
    if Nevt == Ninit:
        print "tree->GetEntries() gives pre-selection events"
    else:
        print "tree->GetEntries() only gives post-selection events"
    evtid = 0
    for evt in xrange(Nevt):
        intree.GetEntry(evt)
        if evt%100000==0: print '{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '%processed'
        #if evt == 1000:
        #    break

        # Optimized Cuts: mu3 Tight, pT > 10 GeV, iso < 0.2, B iso < 0.2, B vprob > 0.1
        #if not intree.JpsiMu_mu3_isTight[0]: continue
        #if intree.JpsiMu_mu3_reldbiso > 0.2: continue
        #if intree.JpsiMu_mu3_pt[0] < 10: continue
        #if intree.JpsiMu_B_reliso > 0.2: continue
        #if intree.JpsiMu_B_vprob < 0.1: continue
        

        Nevts[0]                                = Ninit
        PV_N[0]                                 = intree.PV_N
        JpsiMu_mu1_pt[0]                        = intree.JpsiMu_mu1_pt[0]
        JpsiMu_mu1_eta[0]                       = intree.JpsiMu_mu1_eta[0]
        JpsiMu_mu1_phi[0]                       = intree.JpsiMu_mu1_phi[0]
        JpsiMu_mu1_isLoose[0]                   = intree.JpsiMu_mu1_isLoose[0]
        JpsiMu_mu1_isTight[0]                   = intree.JpsiMu_mu1_isTight[0]
        JpsiMu_mu1_isPF[0]                      = intree.JpsiMu_mu1_isPF[0]
        JpsiMu_mu1_isGlobal[0]                  = intree.JpsiMu_mu1_isGlobal[0]
        JpsiMu_mu1_isTracker[0]                 = intree.JpsiMu_mu1_isTracker[0]
        JpsiMu_mu1_isSoft[0]                    = intree.JpsiMu_mu1_isSoft[0]
        JpsiMu_mu1_dbiso[0]                     = intree.JpsiMu_mu1_dbiso[0]
        JpsiMu_mu1_reldbiso[0]                  = intree.JpsiMu_mu1_reldbiso
        JpsiMu_mu2_pt[0]                        = intree.JpsiMu_mu2_pt[0]
        JpsiMu_mu2_eta[0]                       = intree.JpsiMu_mu2_eta[0]
        JpsiMu_mu2_phi[0]                       = intree.JpsiMu_mu2_phi[0]
        JpsiMu_mu2_isLoose[0]                   = intree.JpsiMu_mu2_isLoose[0]
        JpsiMu_mu2_isTight[0]                   = intree.JpsiMu_mu2_isTight[0]
        JpsiMu_mu2_isPF[0]                      = intree.JpsiMu_mu2_isPF[0]
        JpsiMu_mu2_isGlobal[0]                  = intree.JpsiMu_mu2_isGlobal[0]
        JpsiMu_mu2_isTracker[0]                 = intree.JpsiMu_mu2_isTracker[0]
        JpsiMu_mu2_isSoft[0]                    = intree.JpsiMu_mu2_isSoft[0]
        JpsiMu_mu2_dbiso[0]                     = intree.JpsiMu_mu2_dbiso[0]
        JpsiMu_mu2_reldbiso[0]                  = intree.JpsiMu_mu2_reldbiso
        JpsiMu_mu3_pt[0]                        = intree.JpsiMu_mu3_pt[0]
        JpsiMu_mu3_eta[0]                       = intree.JpsiMu_mu3_eta[0]
        JpsiMu_mu3_phi[0]                       = intree.JpsiMu_mu3_phi[0]
        JpsiMu_mu3_isLoose[0]                   = intree.JpsiMu_mu3_isLoose[0]
        JpsiMu_mu3_isTight[0]                   = intree.JpsiMu_mu3_isTight[0]
        JpsiMu_mu3_isPF[0]                      = intree.JpsiMu_mu3_isPF[0]
        JpsiMu_mu3_isGlobal[0]                  = intree.JpsiMu_mu3_isGlobal[0]
        JpsiMu_mu3_isTracker[0]                 = intree.JpsiMu_mu3_isTracker[0]
        JpsiMu_mu3_isSoft[0]                    = intree.JpsiMu_mu3_isSoft[0]
        JpsiMu_mu3_dbiso[0]                     = intree.JpsiMu_mu3_dbiso[0]
        JpsiMu_mu3_reldbiso[0]                  = intree.JpsiMu_mu3_reldbiso
        JpsiMu_Jpsi_pt[0]                       = intree.JpsiMu_Jpsi_pt[0]
        JpsiMu_Jpsi_eta[0]                      = intree.JpsiMu_Jpsi_eta[0]
        JpsiMu_Jpsi_phi[0]                      = intree.JpsiMu_Jpsi_phi[0]
        JpsiMu_Jpsi_vprob[0]                    = intree.JpsiMu_Jpsi_vprob[0]
        JpsiMu_Jpsi_lip[0]                      = intree.JpsiMu_Jpsi_lip[0]
        JpsiMu_Jpsi_lips[0]                     = intree.JpsiMu_Jpsi_lips[0]
        JpsiMu_Jpsi_pvip[0]                     = intree.JpsiMu_Jpsi_pvip[0]
        JpsiMu_Jpsi_pvips[0]                    = intree.JpsiMu_Jpsi_pvips[0]
        JpsiMu_Jpsi_fl3d[0]                     = intree.JpsiMu_Jpsi_fl3d[0]
        JpsiMu_Jpsi_fls3d[0]                    = intree.JpsiMu_Jpsi_fls3d[0]
        JpsiMu_Jpsi_alpha[0]                    = intree.JpsiMu_Jpsi_alpha[0]
        JpsiMu_Jpsi_maxdoca[0]                  = intree.JpsiMu_Jpsi_maxdoca[0]
        JpsiMu_Jpsi_mindoca[0]                  = intree.JpsiMu_Jpsi_mindoca[0]
        JpsiMu_Jpsi_unfit_mass[0]               = intree.JpsiMu_Jpsi_unfit_mass[0]
        JpsiMu_B_pt[0]                          = intree.JpsiMu_B_pt[0]
        JpsiMu_B_eta[0]                         = intree.JpsiMu_B_eta[0]
        JpsiMu_B_phi[0]                         = intree.JpsiMu_B_phi[0]
        JpsiMu_B_vprob[0]                       = intree.JpsiMu_B_vprob[0]
        JpsiMu_B_lip[0]                         = intree.JpsiMu_B_lip[0]
        JpsiMu_B_lips[0]                        = intree.JpsiMu_B_lips[0]
        JpsiMu_B_pvip[0]                        = intree.JpsiMu_B_pvip[0]
        JpsiMu_B_pvips[0]                       = intree.JpsiMu_B_pvips[0]
        JpsiMu_B_fl3d[0]                        = intree.JpsiMu_B_fl3d[0]
        JpsiMu_B_fls3d[0]                       = intree.JpsiMu_B_fls3d[0]
        JpsiMu_B_alpha[0]                       = intree.JpsiMu_B_alpha[0]
        JpsiMu_B_maxdoca[0]                     = intree.JpsiMu_B_maxdoca[0]
        JpsiMu_B_mindoca[0]                     = intree.JpsiMu_B_mindoca[0]
        JpsiMu_B_mass[0]                        = intree.JpsiMu_B_mass[0]
        JpsiMu_B_iso[0]                         = intree.JpsiMu_B_iso[0]
        JpsiMu_B_iso_ntracks[0]                 = intree.JpsiMu_B_iso_ntracks[0]
        JpsiMu_B_iso_mindoca[0]                 = intree.JpsiMu_B_iso_mindoca[0]
        JpsiMu_B_mcorr[0]                       = intree.JpsiMu_B_mcorr
        JpsiMu_B_reliso[0]                      = intree.JpsiMu_B_reliso
        JpsiMu_dphi_mu2_mu3[0]                  = intree.dphi_mu2_mu3
        JpsiMu_cosdphi_mu2_mu3[0]               = intree.cosdphi_mu2_mu3
        JpsiMu_dR_mu2_mu3[0]                    = intree.dR_mu2_mu3
        JpsiMu_dphi_mu1_mu2[0]                  = intree.dphi_mu1_mu2
        JpsiMu_cosdphi_mu1_mu2[0]               = intree.cosdphi_mu1_mu2
        JpsiMu_dR_mu1_mu2[0]                    = intree.dR_mu1_mu2
        JpsiMu_dphi_mu1_mu3[0]                  = intree.dphi_mu1_mu3
        JpsiMu_cosdphi_mu1_mu3[0]               = intree.cosdphi_mu1_mu3
        JpsiMu_dR_mu1_mu3[0]                    = intree.dR_mu1_mu3
        if "Dat" not in samplekey and 'dat' not in samplekey:
            nPuVtxTrue[0]                       = intree.nPuVtxTrue[0]
            weight_pu[0]                        = intree.weight_pu
            bX[0]                               = intree.bX[0]
            #Eta is y axis pT is x axis
            # Eta goes from 0 to 2.4, pT goes from 0 to 40 GeV

            # Print all individual scale factors and uncerts, to check if errors are symmetric. 
            # Print all components of total weight calculation for one or two evts including lumi, crossexn, and nevts
            # Camilla says errors should be exactly symmetric
            ID_SF_mu1 = lowpt_eff_ID_hist.GetBinContent(lowpt_eff_ID_hist.FindBin(JpsiMu_mu1_pt[0], abs(JpsiMu_mu1_eta[0])))
            ID_SF_err_stat_mu1 = lowpt_eff_ID_hist.GetBinError(lowpt_eff_ID_hist.FindBin(JpsiMu_mu1_pt[0], abs(JpsiMu_mu1_eta[0])))
            
            ID_SF_mu2 = lowpt_eff_ID_hist.GetBinContent(lowpt_eff_ID_hist.FindBin(JpsiMu_mu2_pt[0], abs(JpsiMu_mu2_eta[0])))
            ID_SF_err_stat_mu2 = lowpt_eff_ID_hist.GetBinError(lowpt_eff_ID_hist.FindBin(JpsiMu_mu2_pt[0], abs(JpsiMu_mu2_eta[0])))

            ID_SF_mu3 = lowpt_eff_ID_hist.GetBinContent(lowpt_eff_ID_hist.FindBin(JpsiMu_mu3_pt[0], abs(JpsiMu_mu3_eta[0])))
            ID_SF_err_stat_mu3 = lowpt_eff_ID_hist.GetBinError(lowpt_eff_ID_hist.FindBin(JpsiMu_mu3_pt[0], abs(JpsiMu_mu3_eta[0])))


            err_stat_sf = TMath.Sqrt((ID_SF_err_stat_mu1 * ID_SF_mu2 * ID_SF_mu3)**2 + (ID_SF_mu1 * ID_SF_err_stat_mu2 * ID_SF_mu3)**2 + (ID_SF_mu1 * ID_SF_mu2 * ID_SF_err_stat_mu3)**2)

            if options.debug and ID_SF_mu1 !=0 and ID_SF_mu2 !=0 and ID_SF_mu3 != 0:
                print "mu1 sf", ID_SF_mu1, "+/-", ID_SF_err_stat_mu1/ID_SF_mu1 * 100, "%"
                print "mu2 sf", ID_SF_mu2, "+/-", ID_SF_err_stat_mu2/ID_SF_mu2 * 100, "%"
                print "mu3 sf", ID_SF_mu3, "+/-", ID_SF_err_stat_mu3/ID_SF_mu3 * 100, "%"
                print "event SF error", err_stat_sf
                print "lumi", lumi
                print "cross section", sample['crossxn']
                print "Nevts", Nevts[0]
                print "Pileup Weight", weight_pu[0]

            weight_crossec[0] = lumi * sample['crossxn'] / Nevts[0]
            #weight_crossec_up[0] = weight_crossec[0] + lumi * sample['crossxnerr'] / Nevts[0]
            #weight_crossec_down[0] = weight_crossec[0] - lumi * sample['crossxnerr'] / Nevts[0] 
            weight_SF_ID[0] = ID_SF_mu1 * ID_SF_mu2 * ID_SF_mu3
            weight_SF_ID_up[0] = weight_SF_ID[0] + err_stat_sf
            weight_SF_ID_down[0] = weight_SF_ID[0] - err_stat_sf
            weight_total[0] = weight_pu[0] * weight_crossec[0] * weight_SF_ID[0]
            weight_total_up[0] = weight_pu[0] * weight_SF_ID_up[0] * weight_crossec[0] 
            weight_total_down[0] = weight_pu[0] * weight_SF_ID_down[0] * weight_crossec[0] 
            if options.debug:
                print "event ID scale factor ", weight_SF_ID[0], " +", 100 * (weight_SF_ID_up[0] - weight_SF_ID[0])/weight_SF_ID[0], "% / -", 100 * (weight_SF_ID[0] - weight_SF_ID_down[0])/weight_SF_ID[0],"%"
                print "total weight ", weight_total[0], " +", 100 * (weight_total_up[0] - weight_total[0])/weight_total[0], "% / -", 100 * (weight_total[0] - weight_total_down[0])/weight_total[0], "%"
            #if evt == 1000 and options.debug:
            #    break

            if options.isGen and "Tau" not in samplekey and "OniaAndX" not in samplekey:
                genParticle_pt[0]                   = intree.genParticle_pt[0]
                genParticle_eta[0]                  = intree.genParticle_eta[0]
                genParticle_phi[0]                  = intree.genParticle_phi[0]
                genParticle_pdgId[0]                = intree.genParticle_pdgId[0]
                genParticle_status[0]               = intree.genParticle_status[0]
                JpsiGen[0]                          = intree.JpsiGen
                genBc_pt[0]                         = intree.genBc_pt

            if "OniaAndX" in samplekey and options.isGen:
                isBplusJpsiKplus[0]             = intree.isBplusJpsiKplus
                isBplusJpsiPiplus[0]            = intree.isBplusJpsiPiplus
                isBplusJpsiKPiPiplus[0]         = intree.isBplusJpsiKPiPiplus
                isBplusJpsi3Kplus[0]            = intree.isBplusJpsi3Kplus
                isBplusJpsiPhiKplus[0]          = intree.isBplusJpsiPhiKplus
                isBplusJpsiK0Piplus[0]          = intree.isBplusJpsiK0Piplus

        evtid +=1
        otree.Fill()
    otree.Write()
    outputfile.Close()
