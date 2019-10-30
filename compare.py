import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack
from DisplayManager import DisplayManager
from officialStyle import officialStyle

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


def sproducer(key, rootfile, name, ivar):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['nbin'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + ivar['sel'] + ')'
        
    tree = rootfile.Get(ivar['tree'])

    print ivar['var'] + ' >> ' + hist.GetName(), exp
    
    tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(ivar['xtitle'])
    hist.GetYaxis().SetTitle(ivar['ytitle'])
        
    return copy.deepcopy(hist)

ensureDir('Plots/')

datfile = TFile('/eos/user/w/wvetens/data/Charmonium_2018_runC.root')
bgfile = TFile('/eos/user/w/wvetens/MC/BJpsiX_MC.root')
sigfile = TFile('/eos/user/w/wvetens/signalmc/BcJpsiMuNu_MC.root')
lumi = 6.894770971
crossxns = [5.588 * 10**12, 1]
crossxnerrs = [1.243 * 10**11, 1]
nevts = [1, 1]
effwgts = []
effwgterrs = []
for i in range(len(crossxns)):
    effwgts.append(lumi*crossxns[i]/nevts[i])
    effwgterrs.append(lumi*crossxnerrs[i]/nevts[i])

comparevars = ['Jpsi_trimu_mass', 'Jpsi_trimu_fl3d', 'Jpsi_trimu_lip', 'Jpsi_trimu_maxdoca', 'Jpsi_maxdoca']
comparextitles = ['m(#mu#mu#mu) inv mass [Gev]', 'B_{c} Flight Length 3D', 'B_{c} Longitudinal Impact Parameter', 'B_{c} max doca', 'J/#psi max doca']
comparenbins = [100, 100, 100, 100, 100]
comparexmin = [3, 0, -5, 0, 0]
comparexmax = [9, 10, 5, 0.5, 0.5]
compareytitles = ['', '', '', '', '']
comparelog = [False, True, True, True, True]
compareratio = [False, False, False, False, False]
comparelegend = [False, False, False, False, False]
comparestack = [True, False, False, False, False]
logrange = [1., 3.6, 4.3, 3.7, 5.8]

nvars = len(comparevars)
for i in range(nvars):
    vardict = collections.OrderedDict() 

    if comparestack[i]: 
        addtostack = []
    hists = []
    titles = []
    
    var = comparevars[i]
    nbin = comparenbins[i] 
    xmin = comparexmin[i]
    xmax = comparexmax[i]
    xtitle = comparextitles[i]
    ytitle = compareytitles[i]
    
    vardict['background'] = {'file':bgfile, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B->J/#psi+x', 'wgt': effwgts[0], 'wgterr': effwgterrs[0]}
    vardict['data'] = {'file':datfile, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'Data', 'wgt': 1}
    vardict['signal'] = {'file':sigfile, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->J/#psi#mu#nu', 'wgt': effwgts[1], 'wgterr': effwgterrs[1]}
    

    stackhist = THStack()
    for vkey, ivar in vardict.iteritems():
    
        print vkey
        hist = sproducer(vkey, ivar['file'], vkey, ivar)
        hists.append(copy.deepcopy(hist))
        titles.append(ivar['title'])
        if comparestack[i] and vkey == 'data':
            addtostack.append(False)
        elif comparestack[i]:
            addtostack.append(True)
       
    for ii, ihist in enumerate(hists):
        applyHistStyle(ihist, ii)
        if not comparestack[i]:
            ihist.Scale(1./ihist.GetSumOfWeights())
        else:
            ihist.Scale(ivar['wgt'])
        ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.3)
        if comparestack[i] and addtostack[ii]:
            stackhist.Add(ihist)
            
    comparisonPlots(hists, titles, comparelog[i], logrange[i], 'Plots/'+var+'.pdf', compareratio[i], comparelegend[i])
