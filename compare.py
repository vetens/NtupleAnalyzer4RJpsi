import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle
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


def comparisonPlots(hists, titles, isLog=False, LogRange=0, pname='sync.pdf', isRatio=True, isLegend=True, isStack=False):

    display = DisplayManager(pname, isLog, isRatio, LogRange, 0.2, 0.7, isStack)
    display.draw_legend = isLegend

    display.Draw(hists, titles, isStack)


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

comparevars = ['Jpsi_trimu_mass', 'Jpsi_trimu_fl3d', 'Jpsi_trimu_lip', 'Jpsi_trimu_maxdoca', 'Jpsi_maxdoca']
comparextitles = ['m(#mu#mu#mu) inv mass [Gev]', 'B_{c} Flight Length 3D', 'B_{c} Longitudinal Impact Parameter', 'B_{c} max doca', 'J/#psi max doca']
comparenbins = [100, 100, 100, 100, 100]
comparexmin = [3, 0, -5, 0, 0]
comparexmax = [9, 10, 5, 0.5, 0.5]
compareytitles = ['', '', '', '', '']
compareislog = [False, True, True, True, True]
compareisratio = [False, False, False, False, False]
compareislegend = [False, False, False, False, False]
compareisstack = [False, False, False, False, False]
logrange = [1., 3.6, 4.3, 3.7, 5.8]

nvars = len(comparevars)
for i in range(nvars):
    vardict = collections.OrderedDict() 

    hists = []
    titles = []
    
    var = comparevars[i]
    nbin = comparenbins[i] 
    xmin = comparexmin[i]
    xmax = comparexmax[i]
    xtitle = comparextitles[i]
    ytitle = compareytitles[i]
    
    vardict['background'] = {'file':bgfile, 'tree':'tree', 'var':var , 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B->J/#psi+x'}
    vardict['data'] = {'file':datfile, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'Data'}
    vardict['signal'] = {'file':sigfile, 'tree':'tree', 'var':var, 'nbin':nbin, 'xmin':xmin, 'xmax':xmax, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'B_{c}->J/#psi#mu#nu'}
    
    for vkey, ivar in vardict.iteritems():
    
        print vkey
    
        hist = sproducer(vkey, ivar['file'], vkey, ivar)
        hists.append(copy.deepcopy(hist))
        titles.append(ivar['title'])
    
       
    for ii, ihist in enumerate(hists):
        applyHistStyle(ihist, ii)
        ihist.Scale(1./ihist.GetSumOfWeights())
        ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.3)
            
    comparisonPlots(hists, titles, compareislog[i], logrange[i], 'Plots/'+var+'.pdf', compareisratio[i], compareislegend[i], compareisstack[i])

# nbin = 100
# x_min = -4.
# x_max = 4.
# xtitle = 'selected vtx_{z} - gen. vtx_{z} (cm)'
# ytitle = 'a.u.'

# vardict['PV'] = {'file':datfile, 'tree':'tree', 'var':'Jpsi_PV_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'PV'}
# vardict['JPVZ'] = {'file':datfile, 'tree':'tree', 'var':'Jpsi_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'min. #Deltaz(J/#psi SV vz)'}
# vardict['bbPV'] = {'file':datfile, 'tree':'tree', 'var':'Jpsi_bbPV_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'min. #Deltaz(J/#psi ext. back to beamline)'}
# vardict['pvipPV'] = {'file':bgfile, 'tree':'tree', 'var':'Jpsi_bbPV_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'min. doc (J/#psi ext. back to beamline)'}

#for vkey, ivar in vardict.iteritems():
#
#    print vkey
#
#    hist = sproducer(vkey, datfile, vkey, ivar)
#    hists.append(copy.deepcopy(hist))
#    titles.append(ivar['title'])
#
#   
#for ii, ihist in enumerate(hists):
#    applyHistStyle(ihist, ii)
##    ihist.Scale(1./ihist.GetSumOfWeights())
#    ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)
#        
#comparisonPlots(hists, titles, False, 'Plots/pvchoice.pdf', False)
#comparisonPlots(hists, titles, True, 'Plots/pvchoice_log.pdf', False)
#
