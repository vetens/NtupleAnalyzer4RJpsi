import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack, TMath
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from makeSimpleHtml import writeHTML

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]
widths = [3,3,3,3]

def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(widths[i])
    h.SetStats(False)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def comparisonPlots(hists, titles, isLog=False, LogRange=0, pname='sync.pdf', isRatio=True, isLegend=True):

    display = DisplayManager(pname, isLog, isRatio, LogRange, 0.2, 0.7)
    display.draw_legend = isLegend

    display.Draw(hists, titles)


def sproducer(key, rootfile, name, isample):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                isample['nbin'], isample['xmin'], isample['xmax'])

    hist.Sumw2()
    exp = '(' + isample['sel'] + ')'
        
    tree = rootfile.Get(isample['tree'])

    print isample['var'] + ' >> ' + hist.GetName(), exp
    
    tree.Draw(isample['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(isample['xtitle'])
    hist.GetYaxis().SetTitle(isample['ytitle'])
        
    return copy.deepcopy(hist)

ensureDir('/eos/home-w/wvetens/www/BPH_V0/plots/')
ensureDir('/eos/home-w/wvetens/www/BPH_V0/logs/')

datfile = TFile('/eos/home-w/wvetens/plottest/Charmonium.root')
bgfile = TFile('/eos/home-w/wvetens/plottest/BJpsiX.root')
sigfile = TFile('/eos/home-w/wvetens/plottest/BcJpsiMuNu.root')
lumi = 6.894770971
# Signal Cross section estimated by multiplying the ratio of efficiencies of muon to pion at 7.5 GeV, 
# the number of observed Bc in the Full run 2 analysis divided by the Integrated Luminosity of the 
# full Run 2 Analysis, multiplied by the branching ratio of Bc->J/psi+munu / Bc->J/psi+pi+
# see: https://indico.cern.ch/event/857555/contributions/3614074/attachments/1931729/3199637/rjpsi_23_10_2019.pdf
# for method and efficiency ratio, see the PDG for the branching ratio,
# and see https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.122.132001 for Run 2 Bc production
# errors just added in quadrature
crossxns = [5.588 * 10**12, 2.0 * 7629.0/140.0 *1/4.69 * 10 ** (-2)]
crossxnerrs = [1.243 * 10**11, TMath.Sqrt( (2.0*225/140.0*1/4.69* 10 ** (-2))**2 +(2.0*7629.0/140.0 * 0.28/ (4.69) **2 * 10 ** (-2))**2 +(2.0*7629.0/140.0 * 0.46/ (4.69) ** 2 * 10 ** (-2))**2 )]
nevts = [bgfile.Get('cuthist').GetBinContent(1), sigfile.Get('cuthist').GetBinContent(1)] 
effwgts = []
effwgterrs = []
for i in range(len(crossxns)):
    effwgts.append(lumi*crossxns[i]/nevts[i])
    effwgterrs.append(lumi*crossxnerrs[i]/nevts[i])
# to add a new variable, add a new entry in the ordered dictionary 'vardict'. To add a new sample, add a new entry in the ordered dictionary 'sampledict'.
# the 'loglowerlimit' parameter is only taken into account for variables which will be plotted on a Log scale, i.e. when 'isLog' is True.
# When the graph is shown in Log-scale, 'loglowerlimit' is the negative of the minimum power of ten shown, i.e. -4.5 corresponds to 
# 10^(-4.5)

vardict = collections.OrderedDict()

vardict['mcorr'] = {'xtitle': 'corrected m(#mu#mu#mu) inv mass [Gev]', 'nbins': 60, 'xmin': 3, 'xmax': 9, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': True, 'loglowerlimit': 1} 
vardict['Jpsi_trimu_mass'] = {'xtitle': 'm(#mu#mu#mu) inv mass [Gev]', 'nbins': 60, 'xmin': 3, 'xmax': 9, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': True, 'loglowerlimit': 1} 
vardict['Jpsi_trimu_fl3d'] = {'xtitle': 'B_{c} Flight Length 3D', 'nbins': 60, 'xmin': 0, 'xmax': 10, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 3.6} 
vardict['Jpsi_trimu_lip'] = {'xtitle': 'B_{c} Longitudinal Impact Parameter', 'nbins': 60, 'xmin': -5, 'xmax': 5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 4.3} 
vardict['Jpsi_trimu_maxdoca'] = {'xtitle': 'B_{c} max doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 3.7} 
vardict['Jpsi_maxdoca'] = {'xtitle': 'J/#psi max doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 5.8} 
vardict['cosdphi_Jpsi_mu3'] = {'xtitle': 'Cos(#Delta#phi_{J/#psi,#mu_{3}})', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 5} 
vardict['Jpsi_pt'] = {'xtitle': 'p_{T} of the J/#psi (GeV)', 'nbins': 60, 'xmin': 8, 'xmax': 14, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['Jpsi_mu3_pt'] = {'xtitle': 'p_{T} of the #mu_{3} (GeV)', 'nbins': 60, 'xmin': 5, 'xmax': 11, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['dR_Jpsi_mu3'] = {'xtitle': '#Delta R_{J/#psi,#mu_{3}}', 'nbins': 60, 'xmin': 0, 'xmax': 0.8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['Jpsi_vprob'] = {'xtitle': 'J/#psi Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['Jpsi_trimu_vprob'] = {'xtitle': 'Trimuon Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 5} 
vardict['Jpsi_unfitvprob'] = {'xtitle': 'Unfit J/#psi Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['Jpsi_trimu_unfitvprob'] = {'xtitle': 'Unfit Trimuon Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': 5} 

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
    ytitle = ivar['ytitle']
    
    sampledict['data'] = {'file':datfile, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'Data', 'wgt': 1, 'wgterr': 0}
    sampledict['background'] = {'file':bgfile, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B->J/#psi+x', 'wgt': effwgts[0], 'wgterr': effwgterrs[0]}
    sampledict['signal'] = {'file':sigfile, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->J/#psi#mu#nu', 'wgt': effwgts[1], 'wgterr': effwgterrs[1]}
    
    if ivar['HasStackPlot']:
        stackhist = THStack()
    for samplekey, isample in sampledict.iteritems():
    
        print samplekey
        hist = sproducer(samplekey, isample['file'], samplekey, isample)
        hists.append(copy.deepcopy(hist))
        titles.append(isample['title'])
        if ivar['HasStackPlot'] and samplekey == 'data':
            addtostack.append(False)
        elif ivar['HasStackPlot']:
            addtostack.append(True)
       
    for ii, ihist in enumerate(hists):
        applyHistStyle(ihist, ii)
        if not ivar['HasStackPlot']:
            ihist.Scale(1./ihist.Integral())
        else:
            ihist.Scale(isample['wgt'])
        ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.3)
        if ivar['HasStackPlot'] and addtostack[ii]:
            stackhist.Add(ihist)
    if ivar['HasStackPlot']:
        hists.append(stackhist)
        titles.append("Stack")
            
    comparisonPlots(hists, titles, ivar['isLog'], ivar['loglowerlimit'], '/eos/home-w/wvetens/www/BPH_V0/plots/'+var+'.pdf', ivar['isRatio'], ivar['isLegended'])
# This writes to a webpage so you can more easily view all the plots you've created in a web browser, which will display them simultaneously.
# This is optional, you can comment it out if you want to ...
    writeHTML('/eos/home-w/wvetens/www/BPH_V0', titles[ii])

