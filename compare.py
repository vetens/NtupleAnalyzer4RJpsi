import collections
import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack, TMath, TCanvas, TLegend, TEventList, TDirectory, gObjectTable
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from makeSimpleHtml import writeHTML

from optparse import OptionParser, OptionValueError

usage = "usage: python compare.py [--compare: True, False (default: False)] [--CutOpt: True, False (default: False)] [--compareNorm: True, False (default: False)]"
parser = OptionParser(usage)
parser.add_option("-c", "--compare", default=False, action="store_true", help="Use this option to generate comparison plots between signal and background", dest="isCompare")
parser.add_option("-o", "--cutOpt", default=False, action="store_true", help="Use this option to generate scans for cut optimization", dest="isCutOpt")
parser.add_option("-n", "--compareNorm", default=False, action="store_true", help="Use this option to compare the histograms Normalized to 1", dest="isNorm")


(options, args) = parser.parse_args()

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

#colours = [1, 2, 4, 6, 8, 13, 15]
#styles = [1, 2, 4, 3, 5, 1, 1]
#widths = [3,3,3,3]
#c1 = TCanvas( 'c1', 'canvas', 200, 10, 700, 500 )
colours = {"dataC":1, "bg_BJpsiX_MuMu":2, "bg_BcChic1MuNu":3, "bg_BcJpsiTauNu":4, "bg_BcPsi2STauNu":5, "bg_BJpsiX_MuMu_J": 6, "bg_JpsiX_MuMu_J":7, "bg_BcPsi2SMuNu":8, "signal_BcJpsiMuNu":9}
styles ={"dataC":1, "bg_BJpsiX_MuMu":2, "bg_BcChic1MuNu":4, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":5, "bg_BJpsiX_MuMu_J": 7, "bg_JpsiX_MuMu_J":8, "bg_BcPsi2SMuNu":10, "signal_BcJpsiMuNu":1}
widths = {"dataC":3, "bg_BJpsiX_MuMu":3, "bg_BcChic1MuNu":3, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":3, "bg_BJpsiX_MuMu_J": 3, "bg_JpsiX_MuMu_J":3, "bg_BcPsi2SMuNu":3, "signal_BcJpsiMuNu":3}

def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    if i =='data':
        h.SetMarkerSize(1)
    else:
        h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(widths[i])
    h.SetStats(False)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def comparisonPlots(hists, titles, isLog=False, LogRange=0, pname='sync.pdf', isRatio=True, isLegend=True, isErr=True):

    display = DisplayManager(pname, isLog, isRatio, LogRange, 0.2, 0.7, isErr)
    display.draw_legend = isLegend

    display.Draw(hists, titles, isErr)


def sproducer(key, rootfile, name, isample):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                isample['nbin'], isample['xmin'], isample['xmax'])

    hist.Sumw2()
    exp = '(' + isample['sel'] + ')'
        
    tree = rootfile.Get(isample['tree'])

    #print isample['var'] + ' >> ' + hist.GetName(), exp
    if key is "dataC":
        tree.Draw(isample['var'] + ' >> ' + hist.GetName(), exp)
    else:
        tree.Draw(isample['var'] + ' >> ' + hist.GetName(), "weight_pu[0]*("+exp+")")
    hist.GetXaxis().SetTitle(isample['xtitle'])
    hist.GetYaxis().SetTitle(isample['ytitle'])
        
    return copy.deepcopy(hist)

# ensureDir('/eos/home-c/cgalloni/www/BPH_V0/plots/')
# ensureDir('/eos/home-c/cgalloni/www/BPH_V0/logs/')
directory = '/eos/home-w/wvetens/www/BPH_V5/'
plotdir = directory+'plots/'
logsdir = directory+'logs/'
ensureDir(plotdir)
ensureDir(logsdir)

# datfile = TFile('/afs/cern.ch/user/w/wvetens/public/4Camilla/Charmonium.root')
# bgfile = TFile('/afs/cern.ch/user/w/wvetens/public/4Camilla/BJpsiX.root')
# sigfile = TFile('/afs/cern.ch/user/w/wvetens/public/4Camilla/BcJpsiMuNu.root')
datfileC = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/Charmonium/Charmonium_Run2018C-17Sep2018-v1/Btrimu.root')
bg_BcChic1MuNu = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BcChic1MuNu_211019/BcChic1MuNu_211019/Btrimu.root')
bg_BcJpsiTauNu = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BcJpsiTauNu_020519/BcJpsiTauNu_020519/Btrimu.root')
bg_BcPsi2STauNu = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BcPsi2STauNu_051019/BcPsi2STauNu_051019/Btrimu.root')
bg_BJpsiX_MuMu_J = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BJpsiX_MuMu_J_211119/BJpsiX_MuMu_J_211119/Btrimu.root')
bg_JpsiX_MuMu_J = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/JpsiX_MuMu_J_211119/JpsiX_MuMu_J_211119/Btrimu.root')
bg_BcPsi2SMuNu = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BcPsi2SMuNu_091019/BcPsi2SMuNu_091019/Btrimu.root')
bg_BJpsiX_MuMu = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BJpsiX_MuMu_031019/BJpsiX_MuMu_031019/Btrimu.root')
signal_BcJpsiMuNu = TFile('/eos/home-w/wvetens/Ntuple_BPH_v5_multipleCand/BcJpsiMuNu_020519/BcJpsiMuNu_020519/Btrimu.root')
lumi = 6.894770971
#######################################################################################################################
# OUTDATED                                                                                                            #
#######################################################################################################################
# Signal Cross section estimated by multiplying the ratio of efficiencies of muon to pion at 7.5 GeV (0.01672),       #
# the number of observed Bc in the Full run 2 analysis (7629) divided by the Integrated Luminosity (140 fb^-1) of the #
# full Run 2 Analysis, multiplied by the branching ratio of Bc->J/psi+munu / Bc->J/psi+pi+ (20)                       #
# see: https://indico.cern.ch/event/857555/contributions/3614074/attachments/1931729/3199637/rjpsi_23_10_2019.pdf     #
# for method and efficiency ratio, see the PDG for the branching ratio,                                               #
# and see https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.122.132001 for Run 2 Bc production                     #
# errors just added in quadrature                                                                                     #
# sigma_Bc->Jpsi+mu+nu = 1.822*10^(-2) pb \pm 2.755*10^(-5)                                                           #
#######################################################################################################################
# New sigma calculation method: http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2019_046_v6.pdf
# sigma=Nproduced/L = Nobs/(e_reco L), all values taken from above source
# Using this, we get 90 \pm 10 pb for our cross section
def WeightCalc(crossxn, crossxnerr, Tfile):
    nevts = Tfile.Get('cuthist').GetBinContent(1)
    wgt = lumi * crossxn / nevts
    wgterr = lumi * crossxnerr / nevts
    return [wgt, wgterr, nevts]
#crossxns = [2.063*10**8 ,  7629.0/140.0 *20* 0.01672]
#crossxnerrs = [1.243 * 10**11, TMath.Sqrt( (2.0*225/140.0*1/4.69* 10 ** (-2))**2 +(2.0*7629.0/140.0 * 0.28/ (4.69) **2 * 10 ** (-2))**2 +(2.0*7629.0/140.0 * 0.46/ (4.69) ** 2 * 10 ** (-2))**2 )]
#nevts = [datfileC.Get('cuthist').GetBinContent(1), datfileC.Get('cuthist').GetBinContent(1)] 
#effwgts = []
#effwgterrs = []
#for i in range(len(crossxns)):
#    effwgts.append(lumi*crossxns[i]/nevts[i])
#    print " file %s, effwgt %s, nevts %s"   %(i,lumi*crossxns[i]/nevts[i],nevts[i])
#    effwgterrs.append(lumi*crossxnerrs[i]/nevts[i])

# to add a new variable, add a new entry in the ordered dictionary 'vardict'. To add a new sample, add a new entry in the ordered dictionary 'sampledict'.
# the 'loglowerlimit' parameter is only taken into account for variables which will be plotted on a Log scale, i.e. when 'isLog' is True.
# When the graph is shown in Log-scale, 'loglowerlimit' is the negative of the minimum power of ten shown, i.e. -4.5 corresponds to 
# 10^(-4.5)


vardict = collections.OrderedDict()

vardict['mcorr'] = {'xtitle': 'corrected m(#mu#mu#mu) inv mass [Gev]', 'nbins': 60, 'xmin': 3, 'xmax': 9, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_B_mass'] = {'xtitle': 'm(#mu#mu#mu) inv mass [Gev]', 'nbins': 60, 'xmin': 3, 'xmax': 9, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
#vardict['MET_corrPx'] = {'xtitle': 'MET_corrPx', 'nbins': 60, 'xmin': -30, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2} 
#vardict['MET_corrPy'] = {'xtitle': 'MET_corrPy', 'nbins': 60, 'xmin': -30, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2} 
vardict['MET_et'] = {'xtitle': 'MET_et (GeV)', 'nbins': 60, 'xmin': 0, 'xmax': 10, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
#vardict['MET_sumEt'] = {'xtitle': 'MET_sumEt (GeV)', 'nbins': 60, 'xmin': 0, 'xmax': 3500, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
##vardict['MET_significance'] = {'xtitle': 'MET_significance', 'nbins': 60, 'xmin': 0, 'xmax': 14, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_mu1_iso'] = {'xtitle': '#mu_{1} isolation', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_mu2_iso'] = {'xtitle': '#mu_{2} isolation', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_mu3_iso'] = {'xtitle': '#mu_{3} isolation', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_mu1_dbiso'] = {'xtitle': 'Jpsi_mu1_dbiso', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_mu2_dbiso'] = {'xtitle': 'Jpsi_mu2_dbiso', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_mu3_dbiso'] = {'xtitle': 'Jpsi_mu3_dbiso', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_B_pt'] = {'xtitle': 'p_{T} of the trimuon (GeV)', 'nbins': 60, 'xmin': 8, 'xmax': 14, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_mu3_pt'] = {'xtitle': 'p_{T} of the #mu_{3} (GeV)', 'nbins': 60, 'xmin': 5, 'xmax': 11, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_B_fl3d'] = {'xtitle': 'B_{c} Flight Length 3D', 'nbins': 60, 'xmin': 0, 'xmax': 10, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_fls3d'] = {'xtitle': 'B_{c} Flight Length 3D Significance', 'nbins': 60, 'xmin': 0, 'xmax': 90, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_iso'] = {'xtitle': 'B_{c} isolation', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_lip'] = {'xtitle': 'B_{c} Longitudinal Impact Parameter', 'nbins': 60, 'xmin': -5, 'xmax': 5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_maxdoca'] = {'xtitle': 'B_{c} max doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_mindoca'] = {'xtitle': 'B_{c} min doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.02, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_maxdoca'] = {'xtitle': 'J/#psi max doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 6} 
vardict['JpsiMu_Jpsi_mindoca'] = {'xtitle': 'J/#psi min doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.02, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_JpsiMu_mu3'] = {'xtitle': 'Cos(#Delta#phi_{J/#psi,#mu_{3}})', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_JpsiMu_MET'] = {'xtitle': 'Cos(#Delta#phi_{J/#psi,MET})', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_mu3_MET'] = {'xtitle': 'Cos(#Delta#phi_{#mu_{3},MET})', 'nbins': 61, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['dR_JpsiMu_mu3'] = {'xtitle': '#Delta R_{J/#psi,#mu_{3}}', 'nbins': 60, 'xmin': 0, 'xmax': 0.8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['JpsiMu_Jpsi_vprob'] = {'xtitle': 'J/#psi Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2} 
vardict['JpsiMu_B_vprob'] = {'xtitle': 'Trimuon Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_Jpsi_alpha'] = {'xtitle': 'J/#psi #alpha', 'nbins': 60, 'xmin': -1, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3.7} 
vardict['JpsiMu_B_alpha'] = {'xtitle': 'B_{c} #alpha', 'nbins': 60, 'xmin': -1, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3.7} 
for varkey, ivar in vardict.iteritems():
    print varkey
    sampledict = collections.OrderedDict() 

    if ivar['HasStackPlot']: 
        addtostack = []
    hists = []
    titles = []
    
    var = varkey
    nbin = ivar['nbins']
    xmin = ivar['xmin']
    xmax = ivar['xmax']
    xtitle = ivar['xtitle']
    ytitle = 'events'#ivar['ytitle']
    
    sampledict['dataC'] = {'file':datfileC, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'Data (Charmonium Run2018C)'+' ['+str(round(datfileC.Get('cuthist').GetBinContent(1)))+':'+str(round(datfileC.Get('cuthist').GetBinContent(2)*23, 1))+']', 'crossxn': 1, 'crossxnerr': 0}
    sampledict['bg_BJpsiX_MuMu'] = {'file':bg_BJpsiX_MuMu, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B->J/#psi + X'+' ['+str(round(bg_BJpsiX_MuMu.Get('cuthist').GetBinContent(1)))+':'+str(round(bg_BJpsiX_MuMu.Get('cuthist').GetBinContent(3)*WeightCalc(5.588*10**8,0,bg_BJpsiX_MuMu)[0], 1))+']', 'crossxn': 5.588*10**8, 'crossxnerr': 3.951*10**8}
#    sampledict['bg_BcChic1MuNu'] = {'file':bg_BcChic1MuNu, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->#chi_{c}^{1} + #mu + #nu'+' ['+str(round(bg_BcChic1MuNu.Get('cuthist').GetBinContent(1)))+':'+str(round(bg_BcChic1MuNu.Get('cuthist').GetBinContent(3)*WeightCalc(1,0,bg_BcChic1MuNu)[0], 1))+']', 'crossxn': 1, 'crossxnerr': 0}
    sampledict['bg_BcJpsiTauNu'] = {'file':bg_BcJpsiTauNu, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->J/#psi + #tau + #nu'+' ['+str(round(bg_BcJpsiTauNu.Get('cuthist').GetBinContent(1)))+':'+str(round(bg_BcJpsiTauNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,bg_BcJpsiTauNu)[0], 1))+']', 'crossxn': 90, 'crossxnerr': 10}
#    sampledict['bg_BcPsi2STauNu'] = {'file':bg_BcPsi2STauNu, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->#psi(2S) + #tau + #nu'+' ['+str(round(bg_BcPsi2STauNu.Get('cuthist').GetBinContent(1), 2))+':'+str(round(bg_BcPsi2STauNu.Get('cuthist').GetBinContent(3)*WeightCalc(1,0,bg_BcPsi2STauNu)[0], 2))+']', 'crossxn': 1, 'crossxnerr': 0}
    sampledict['bg_BJpsiX_MuMu_J'] = {'file':bg_BJpsiX_MuMu_J, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B->J/#psi + X with relaxed gen filter cuts'+' ['+str(round(bg_BJpsiX_MuMu_J.Get('cuthist').GetBinContent(1)))+':'+str(round(bg_BJpsiX_MuMu_J.Get('cuthist').GetBinContent(3)*WeightCalc(1.080 * 10 ** 9,0,bg_BJpsiX_MuMu_J)[0], 1))+']', 'crossxn': 1.080 * 10 ** 9, 'crossxnerr': 1.730 *10**8}
    sampledict['bg_JpsiX_MuMu_J'] = {'file':bg_JpsiX_MuMu_J, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'pp->J/#psi+X'+' ['+str(round(bg_JpsiX_MuMu_J.Get('cuthist').GetBinContent(1)))+':'+str(round(bg_JpsiX_MuMu_J.Get('cuthist').GetBinContent(3)*WeightCalc(1.957*10**8,0,bg_BcPsi2SMuNu)[0], 1))+']', 'crossxn': 1.384*10**9, 'crossxnerr': 1.957*10**8}
#    sampledict['bg_BcPsi2SMuNu'] = {'file':bg_BcPsi2SMuNu, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->#psi(2S) + #mu + #nu'+' ['+str(round(bg_BcPsi2SMuNu.Get('cuthist').GetBinContent(1)))+':'+str(round(bg_BcPsi2SMuNu.Get('cuthist').GetBinContent(3)*WeightCalc(2.612*10**10,0,bg_BcPsi2SMuNu)[0], 1))+']', 'crossxn': 2.612*10**10, 'crossxnerr': 2.347*10**5}
    sampledict['signal_BcJpsiMuNu'] = {'file':signal_BcJpsiMuNu, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->J/#psi + #mu + #nu'+' ['+str(round(signal_BcJpsiMuNu.Get('cuthist').GetBinContent(1)))+':'+str(round(signal_BcJpsiMuNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,signal_BcJpsiMuNu)[0], 1))+']', 'crossxn': 90, 'crossxnerr': 10}
 
    for samplekey, isample in sampledict.iteritems():
        print samplekey
        print "Weight = ", WeightCalc(isample['crossxn'],0,isample['file'])[0], " +/- ", WeightCalc(0, isample['crossxnerr'], isample['file'])[1]
    if not options.isCompare:
        break
    #print "Weighted Bc->J/psi+mu+nu evts: ", signal_BcJpsiMuNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,signal_BcJpsiMuNu)[0]
    #print "Weighted Bc->J/psi+tau+nu evts: ", bg_BcJpsiTauNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,bg_BcJpsiTauNu)[0]
    if options.isCompare:
    
        if ivar['HasStackPlot']:
            stackhist = THStack("stack","stack")
        for samplekey, isample in sampledict.iteritems():
            hist = sproducer(samplekey, isample['file'], samplekey, isample)
            applyHistStyle(hist, samplekey)
            #hists.append(copy.deepcopy(hist))
            titles.append(isample['title'])
            weight = WeightCalc(isample['crossxn'], isample['crossxnerr'], isample['file'])
            #print samplekey
            #print "Weight = ", weight[0]
            #if ivar['isLegended']:
            #    Legend.AddEntry(hist, isample['title'], 'l')
            if options.isNorm:
                if hist.Integral()!=0:
                    hist.Scale(1./hist.Integral()) 
            if samplekey != 'dataC':
                #print "histintegral() ",hist.Integral()
                hist.Scale(weight[0])
                #hists.append(hist)
                hists.append(copy.deepcopy(hist))
                if ivar['HasStackPlot']:
                    stackhist.Add(copy.deepcopy(hist))
            else: 
                hist.Scale(23)
                #print "histintegral() ",hist.Integral()
                #hists.append(hist)
                hists.append(copy.deepcopy(hist))
    
           
    
        if ivar['HasStackPlot']:
            #stackhist.SetFillColor(kGreen+3);
            hists.append(stackhist)
            titles.append("stack")
    
        #for ii, ihist in enumerate(hists):
            ##print " ihist.Integral() ", ihist.Integral()
            #cv_samples = TCanvas('plots/'+ihist.GetTitle(), 'plots/'+ihist.GetTitle() , 10, 10, 700, 600)   
            #cv_samples .cd()
            #ihist.Draw()
            #cv_samples.Print('plots/'+ihist.GetTitle()+".pdf")
            #del cv_samples 
       
        #for ii, ihist in enumerate(hists):
        #    applyHistStyle(ihist, ii)
        #    if not ivar['HasStackPlot'] :
        #        ihist.Scale(1./ihist.Integral())
        #    else:
        #        print "multiplying a weight of isample['wgt'] %s for sample %s " %(isample['wgt'], samplekey)
        #        ihist.Scale(isample['wgt'])
        #    ihist.SetMaximum(ihist.GetMaximum()*1.3)
        #    if ivar['HasStackPlot'] and addtostack[ii]:
        #        stackhist.Add(ihist)
        #if ivar['HasStackPlot']:
        #    hists.append(stackhist)
        #    titles.append("Stack")
          
        comparisonPlots(hists, titles, ivar['isLog'], ivar['loglowerlimit'], plotdir+var+'.pdf', ivar['isRatio'], ivar['isLegended'])

if options.isCutOpt:
    bg_JpsiX_MuMu_J.Get('tree').SetBranchStatus('*', 0)
    bg_JpsiX_MuMu_J.Get('tree').SetBranchStatus('JpsiMu_B_fls3d', 1)
    signal_BcJpsiMuNu.Get('tree').SetBranchStatus('*', 0)
    signal_BcJpsiMuNu.Get('tree').SetBranchStatus('JpsiMu_B_fls3d', 1)
    var = vardict['JpsiMu_B_fls3d']
    granularity = 1000.0
    split = (var['xmax']-var['xmin'])/granularity
    cutopthist1 = TH1F("cutopthist1", "Cut Optimization for "+str(var['xtitle']), int(granularity), var['xmin'], var['xmax'])
    cutopthist1.GetYaxis().SetTitle('#frac{s}{#sqrt{s+b}}')
    cutopthist1.GetYaxis().SetTitleFont(12)
    cutopthist1.GetYaxis().SetTitleOffset(0.6)
    cutopthist1.GetXaxis().SetTitle(str(var['xtitle']))
    cutopthist2 = TH1F("cutopthist2", "Cut Optimization for "+str(var['xtitle']), int(granularity), var['xmin'], var['xmax'])
    cutopthist2.GetYaxis().SetTitle('#frac{s}{#sqrt{b}}')
    cutopthist2.GetYaxis().SetTitleFont(12)
    cutopthist2.GetYaxis().SetTitleOffset(0.6)
    cutopthist2.GetXaxis().SetTitle(str(var['xtitle']))
    #print var['xmax']
    #print var['xmin']
    #print split
    for x in range(0,int(granularity)):
        xparam = var['xmin']+split*x
        b = bg_JpsiX_MuMu_J.Get('tree').GetEntries('JpsiMu_B_fls3d'+'>'+str(xparam))
        s = signal_BcJpsiMuNu.Get('tree').GetEntries('JpsiMu_B_fls3d'+'>'+str(xparam))
        cutopthist1.AddBinContent(x+1, s/TMath.Sqrt(s+b))
        cutopthist2.AddBinContent(x+1, s/TMath.Sqrt(b))
    comparisonPlots([cutopthist1], ['#frac{s}{#sqrt{s+b}}'], False, False, plotdir+'JpsiMu_B_fls3d_cutopt1'+'.pdf', False, False, False)
    comparisonPlots([cutopthist2], ['#frac{s}{#sqrt{b}}'], False, False, plotdir+'JpsiMu_B_fls3d_cutopt2'+'.pdf', False, False, False)
# This writes to a webpage so you can more easily view all the plots you've created in a web browser, which will display them simultaneously.
# This is optional, you can comment it out if you want to ...
writeHTML(directory, "Comparison Plots")
