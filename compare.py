import collections
import itertools
import shutil
import copy, math, os, collections, sys
import numpy as np
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack, TMath, TCanvas, TLegend, TEventList, TDirectory, gObjectTable, TLine, TH2F, TAxis
from ROOT import TH2I
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from makeSimpleHtml import writeHTML
from samples import *
from varsdict import *

from optparse import OptionParser, OptionValueError

usage = "usage: python compare.py [--compare: True, False (default: False)] [--CutOpt: True, False (default: False)] [--compareNorm: True, False (default: False)] [--twoDHist: True, False (default: False)] [--rmrf: True, False (default: False)] [--outdir: <Directory For Outgoing Files> (default: /eos/home-w/wvetens/www/BPH_V5/)] [--precut: <Precuts in TCut string format> (default: '')]"
parser = OptionParser(usage)
parser.add_option("-c", "--compare", default=False, action="store_true", help="Use this option to generate comparison plots between signal and background", dest="isCompare")
parser.add_option("-o", "--cutOpt", default=False, action="store_true", help="Use this option to generate scans for cut optimization", dest="isCutOpt")
parser.add_option("-n", "--compareNorm", default=False, action="store_true", help="Use this option to compare the histograms Normalized to 1", dest="isNorm")
parser.add_option("-t", "--twoDHist", default=False, action="store_true", help="Use this option to compare two variables and check for correlations using a two-dimensional histogram", dest="is2DHist")
parser.add_option("-f", "--rmrf", default=False, action="store_true", help="Forcefully overwrite the output directories to remove old outputs", dest="isrmrf")
parser.add_option("-g", "--gen", default=False, action="store_true", help="with this flag true, will analyze gen level info from MC files", dest="isgen")
parser.add_option("--outdir", default='/eos/home-w/wvetens/www/geninfo/', action="store", help="Output Directory for plots", dest="outdir")
parser.add_option("--precut", default='', action="store", help="List of Cuts to apply before plotting", dest="precut")


(options, args) = parser.parse_args()

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptStat(0)

directory = options.outdir
cut0 = options.precut
#colours = [1, 2, 4, 6, 8, 13, 15]
#styles = [1, 2, 4, 3, 5, 1, 1]
#widths = [3,3,3,3]
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

def WeightCalc(crossxn, crossxnerr, Tfile):
    nevts = Tfile.Get('cuthist').GetBinContent(1)
    wgt = lumi * crossxn / nevts
    wgterr = lumi * crossxnerr / nevts
    return [wgt, wgterr, nevts]

def comparisonPlots(hists, titles, isLog=False, LogRange=0, pname='sync.pdf', isRatio=True, isLegend=True, isOpt=False, is2D=False, isLogX=False):

    display = DisplayManager(pname, isLog, isRatio, LogRange, 0.2, 0.7, isOpt, is2D, isLogX)
    display.draw_legend = isLegend

    display.Draw(hists, titles, isOpt, is2D)

def BinLogX(xmin, xmax, bins):
    width = (float(xmax) - float(xmin)) / float(bins)
    new_bins = []
    for i in xrange(bins):
        new_bins += [10.0 ** (xmin + i * width)]
    return new_bins

def sproducer(key, ivar, samplekey, sample, cut0='', title='', isLogX=False):

    if isLogX:
        bins = BinLogX(ivar['xmin'], ivar['xmax'], ivar['nbins'])
        hist = TH1F('h_' + key, 'h_' + key, ivar['nbins'], np.array(bins, dtype='int64'))
    else:
        hist = TH1F('h_' + key, 'h_' + key, ivar['nbins'], ivar['xmin'], ivar['xmax'])
    hist.Sumw2()
    if title is not '':
        hist.SetTitle(title)
    if samplekey is "dataC":
        wgt = '23'
    else:
        wgt = str(WeightCalc(sample['crossxn'],sample['crossxnerr'],sample['file'])[0]) 
    if cut0 == '':
        exp = '('+wgt+')'
    else:
        exp = wgt+'*(' + cut0 + ')'
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    if samplekey is "dataC":
        tree.Draw(key + ' >> ' + hist.GetName(), exp)
    else:
        tree.Draw(key + ' >> ' + hist.GetName(), 'weight_pu[0]*'+exp)
    hist.GetXaxis().SetTitle(ivar['xtitle'])
    hist.GetYaxis().SetTitle(ivar['ytitle'])
        
    return copy.deepcopy(hist)
def IDsproducer(key, xlist, cut, title, sample='bg_JpsiX_MuMu_J'):

    hist = TH1F('h_' + key, 
                title, 
                len(xlist), 1, len(xlist)+1)

    rootfile = sampledict[sample]['file']
    if cut == '':
        exp = '(1)'
    else:
        exp = '(' + cut + ')'
        
    tree = rootfile.Get('tree')
    for binnum in xrange(len(xlist)):
       hist.GetXaxis().SetBinLabel(binnum+1, xlist[binnum]) 

    tree.Draw(key + ' >> ' + hist.GetName(), 'weight_pu[0]*'+exp)
    hist.GetXaxis().SetTitle(vardict[key]['xtitle'])
    if key == 'sister_type':
        hist.GetXaxis().SetLabelSize(0.03)
    hist.GetYaxis().SetTitle(vardict[key]['ytitle'])
        
    return copy.deepcopy(hist)

def IDsproducer2D(keyx, xlist, keyy, ylist, cut, title):

    hist = TH2I('h_' + keyx + keyy, 
                title, 
                len(xlist), 1, len(xlist)+1, len(ylist), 1, len(ylist)+1)
    rootfile = sampledict['bg_JpsiX_MuMu_J']['file']

    if cut == '':
        exp = '(1)'
    else:
        exp = '(' + cut + ')'
        
    tree = rootfile.Get('tree')
    for binnum in xrange(len(xlist)):
       hist.GetXaxis().SetBinLabel(binnum+1, xlist[binnum]) 
    for binnum in xrange(len(ylist)):
       hist.GetYaxis().SetBinLabel(binnum+1, ylist[binnum]) 

    tree.Draw(keyy + ':' + keyx + ' >> ' + hist.GetName(), 'weight_pu[0]*'+exp)
    hist.GetXaxis().SetTitle(vardict[keyx]['xtitle'])
    if keyx == 'sister_type':
        hist.GetXaxis().SetLabelSize(0.03)
    hist.GetYaxis().SetTitle(vardict[keyy]['xtitle'])
    if keyy == 'sister_type':
        hist.GetYaxis().SetLabelSize(0.02)
        
    return copy.deepcopy(hist)
def optsproducer(key, ivar, samplekey, sample, tcut):

    hist = TH1F('h_' + key, 
                'h_' + key, 
                ivar['nbins'], ivar['xmin'], ivar['xmax'])

    wgt =  str(WeightCalc(sample['crossxn'], sample['crossxnerr'], sample['file'])[0])
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')
    hist.GetYaxis().SetTitleOffset(2.5)

    if tcut == '':
        tree.Draw(key + ' >> ' + hist.GetName(), '('+'weight_pu[0]*'+wgt+')')
    else:
        tree.Draw(key + ' >> ' + hist.GetName(), 'weight_pu[0]*'+wgt+'*'+tcut)
        
    return copy.deepcopy(hist)
def sproducer2D(key1, key2, var1, var2, samplekey, sample, cut0=''):

    hist = TH2F('h_' + key1 + '_' + key2, 
                samplekey+';'+var1['xtitle']+';'+var2['xtitle']+';events', 
                var1['nbins'], var1['xmin'], var1['xmax'],
                var2['nbins'], var2['xmin'], var2['xmax'])

    hist.Sumw2()
    if samplekey is "dataC":
        wgt = '1'
    else:
        wgt = str(WeightCalc(sample['crossxn'],sample['crossxnerr'],sample['file'])[0]) 
    if cut0 == '':
        exp = '('+wgt+')'
    else:
        exp = wgt+'*(' + cut0 + ')'
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    if samplekey is "dataC":
        tree.Draw(key2 + ':' + key1 + ' >> ' + hist.GetName(), exp)
    else:
        tree.Draw(key2 + ':' + key1  + ' >> ' + hist.GetName(), 'weight_pu[0]*'+exp)
    hist.GetXaxis().SetTitleOffset(1)
    hist.GetYaxis().SetTitleOffset(1.7)
    hist.GetZaxis().SetTitleOffset(1.7)
    #hist.SetFontSize(14)
        
    return copy.deepcopy(hist)

if options.isgen:
    gdir = directory+'gen/'
    plotgdir = gdir+'plots/'
    logsgdir = gdir+'logs/'
    if options.isrmrf:
        if os.path.exists(gdir):
            shutil.rmtree(gdir)
    ensureDir(plotgdir)
    ensureDir(logsgdir)
if options.is2DHist:
    tdir = directory+'2dhists/'
    plottdir = tdir+'plots/'
    logstdir = tdir+'logs/'
    if options.isrmrf:
        if os.path.exists(tdir):
            shutil.rmtree(tdir)
    ensureDir(plottdir)
    ensureDir(logstdir)
if options.isCompare:
    cdir = directory+'comparisons/'
    plotcdir = cdir+'plots/'
    logscdir = cdir+'logs/'
    if options.isrmrf:
        if os.path.exists(cdir):
            shutil.rmtree(cdir)
    ensureDir(plotcdir)
    ensureDir(logscdir)
if options.isCutOpt:
    odir = directory+'cutopt/'
    plotodir = odir+'plots/'
    logsodir = odir+'logs/'
    if options.isrmrf:
        if os.path.exists(odir):
            shutil.rmtree(odir)
    ensureDir(plotodir)
    ensureDir(logsodir)
    odir2 = directory+'reject_cutopt/'
    plotodir2 = odir2+'plots/'
    logsodir2 = odir2+'logs/'
    if options.isrmrf:
        if os.path.exists(odir2):
            shutil.rmtree(odir2)
    ensureDir(plotodir2)
    ensureDir(logsodir2)


# to add a new variable, add a new entry in 'varsdict.py'. To add a new sample, add a new entry in 'samples.py'.
GoodCuts = []
for varkey, ivar in vardict.iteritems():

    if ivar['HasStackPlot']: 
        addtostack = []
    hists = []
    titles = []
    
    var = varkey
    #print ivar
 
    if var == list(vardict.items()[0])[0]:
        for samplekey, isample in sampledict.iteritems():
            if not options.isNorm:
                print samplekey
                print "Non-PU Weight = ", WeightCalc(isample['crossxn'],0,isample['file'])[0], " +/- ", WeightCalc(0, isample['crossxnerr'], isample['file'])[1]
    #print "Weighted Bc->J/psi+mu+nu evts: ", signal_BcJpsiMuNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,signal_BcJpsiMuNu)[0]
    #print "Weighted Bc->J/psi+tau+nu evts: ", bg_BcJpsiTauNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,bg_BcJpsiTauNu)[0]
    if options.isCompare:
        gStyle.SetOptTitle(0)
        if ivar['HasStackPlot']:
            stackhist = THStack("stack","stack")
        for samplekey, isample in sampledict.iteritems():
            hist = sproducer(var, ivar, samplekey, isample)
            applyHistStyle(hist, samplekey)
            weight = WeightCalc(isample['crossxn'], isample['crossxnerr'], isample['file'])
            # Add number of initial and final events to title (only want to do this once)
            if var == list(vardict.items()[0])[0]:
                if samplekey == 'dataC':
                    isample['title'] += ' ['+str(round(isample['file'].Get('cuthist').GetBinContent(1)))+':'+str(round(hist.Integral()))+']'
                else:
                    isample['title'] += ' ['+str(round(isample['file'].Get('cuthist').GetBinContent(1)))+':'+str(round(hist.Integral(), isample['digits']))+']'
            # add histogram to stack hist if it isn't data and normalize histograms
            if options.isNorm:
                if hist.Integral()!=0:
                    hist.Scale(1./hist.Integral()) 
            if samplekey != 'dataC':
                if ivar['HasStackPlot']:
                    stackhist.Add(copy.deepcopy(hist))
            hists.append(copy.deepcopy(hist))
            titles.append(isample['title'])
    
        if ivar['HasStackPlot']:
            hists.append(stackhist)
            titles.append("stack")
    
        comparisonPlots(hists, titles, ivar['isLog'], ivar['loglowerlimit'], plotcdir+var+'.pdf', ivar['isRatio'], ivar['isLegended'])
    if options.isCutOpt:
        gStyle.SetOptTitle(0)
        if var not in to_optimize:
            continue
        optparams = to_optimize[var]
        granularity = optparams['granularity']
        igran = int(granularity)
        split = (optparams['xmax']-optparams['xmin'])/granularity
        #coh1name="cutopthist1"+var
        coh2name="cutopthist2"+var
        coh3name="cutopthist3"+var
        signame="sig"+var
        bckgname="bckg"+var
        #coh1 = TH1F(coh1name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        #coh1.GetYaxis().SetTitle('a.u.')
        #coh1.GetYaxis().SetTitleFont(12)
        #coh1.GetXaxis().SetTitle(str(ivar['xtitle']))
        coh2 = TH1F(coh2name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        coh2.GetYaxis().SetTitle('a.u.')
        coh2.GetYaxis().SetTitleFont(12)
        coh2.GetXaxis().SetTitle(str(ivar['xtitle']))
        coh3 = TH1F(coh3name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        coh3.GetYaxis().SetTitle('a.u.')
        coh3.GetYaxis().SetTitleFont(12)
        coh3.GetXaxis().SetTitle(str(ivar['xtitle']))
        sigh = TH1F(signame, "s", igran, optparams['xmin'], optparams['xmax'])
        bckgh = TH1F(bckgname, "b", igran, optparams['xmin'], optparams['xmax'])
        if cut0 == '':
            signal_BcJpsiMuNu.Get('tree').Draw(var+'>>'+signame)
            bg_JpsiX_MuMu_J.Get('tree').Draw(var+'>>'+bckgname)
            bh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['bg_JpsiX_MuMu_J'], '')
            sh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['signal_BcJpsiMuNu'], '')
        else:
            signal_BcJpsiMuNu.Get('tree').Draw(var+'>>'+signame, '('+cut0+')')
            bg_JpsiX_MuMu_J.Get('tree').Draw(var+'>>'+bckgname, '('+cut0+')')
            bh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['bg_JpsiX_MuMu_J'], '('+cut0+')')
            sh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['signal_BcJpsiMuNu'], '('+cut0+')')
        b0 = bh0.Integral()
        s0 = sh0.Integral()
        if not cut0 == '':
            icut = ' && ('+cut0+')'
        else:
            icut = ''
        for x in range(1,igran):
            xparam = optparams['xmin']+split*x
            tcut = '('+var+optparams['isgl']+str(xparam)+icut+')'
            bh = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['bg_JpsiX_MuMu_J'], tcut)
            sh = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['signal_BcJpsiMuNu'], tcut)
            b = bh.Integral()
            s = sh.Integral()
            if b == 0:
                #coh1.AddBinContent(x+1, 0)
                coh2.AddBinContent(x+1, 0)
                coh3.AddBinContent(x+1, 0)
            else:
                #coh1.AddBinContent(x+1, s/TMath.Sqrt(s+b))
                coh2.AddBinContent(x+1, s/TMath.Sqrt(b))
                coh3.AddBinContent(x+1, s/b)
        #optcutbin1 = coh1.GetMaximumBin()
        #optcut1 = coh1.GetBin(optcutbin1)
        #optcut1 = optparams['xmin'] + optcutbin1 * split
        #cutline1 = TLine.TLine(optcut1, 0, optcut1, coh1.GetMaximum())
        optcutbin2 = coh2.GetMaximumBin()
        optcut2 = optparams['xmin'] + optcutbin2 * split
        cutline2 = TLine.TLine(optcut2, 0, optcut2, coh2.GetMaximum())
        optcutbin3 = coh3.GetMaximumBin()
        optcut3 = coh3.GetBin(optcutbin3)
        optcut3 = optparams['xmin'] + optcutbin3 * split
        cutline3 = TLine.TLine(optcut3, 0, optcut3, coh3.GetMaximum())
        histscale = optparams['histscale']
        sigh.SetLineColor(2)
        bckgh.SetLineColor(4)
        #cutline1.SetLineColor(6)
        cutline2.SetLineColor(6)
        cutline3.SetLineColor(6)
        opt_signif = coh2.GetMaximum()
        if opt_signif >= 0.0022:
            GoodCuts += [var]
            #sigh.Scale(histscale * coh1.Integral()/sigh.Integral())
            #bckgh.Scale(histscale * coh1.Integral()/bckgh.Integral())
            #comparisonPlots([coh1, sigh, bckgh, cutline1], ['#frac{s}{#sqrt{s+b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Optimal Cut: ' + var +' '+optparams['isgl']+' '+str(optcut1)+'. #frac{s}{#sqrt{s+b}} = '+str(coh1.GetMaximum())+' vs no cuts: '+str(s0/TMath.Sqrt(s0+b0))], False, False, plotodir+var+'_cutopt1'+'.pdf', False, True, True)

            sigh.Scale(histscale * coh2.Integral()/sigh.Integral())
            bckgh.Scale(histscale * coh2.Integral()/bckgh.Integral())
            comparisonPlots([coh2, sigh, bckgh, cutline2], ['#frac{s}{#sqrt{b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut2)+'.#frac{s}{#sqrt{b}} = '+str(round(coh2.GetMaximum(), 4))+' : '+str(round(s0/TMath.Sqrt(b0), 4))], False, False, plotodir+var+'_cutopt2'+'.pdf', False, True, True)

            sigh.Scale(histscale * coh3.Integral()/sigh.Integral())
            bckgh.Scale(histscale * coh3.Integral()/bckgh.Integral())
            comparisonPlots([coh3, sigh, bckgh, cutline3], ['#frac{s}{b}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut3)+'.#frac{s}{b} = '+str(round(coh3.GetMaximum(), 8))+' : '+str(round(s0/b0, 8))], False, False, plotodir+var+'_cutopt3'+'.pdf', False, True, True)

        else:
            #sigh.Scale(histscale * coh1.Integral()/sigh.Integral())
            #bckgh.Scale(histscale * coh1.Integral()/bckgh.Integral())
            #comparisonPlots([coh1, sigh, bckgh, cutline1], ['#frac{s}{#sqrt{s+b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Optimal Cut: ' + var +' '+optparams['isgl']+' '+str(optcut1)+'. #frac{s}{#sqrt{s+b}} = '+str(coh1.GetMaximum())+' vs no cuts: '+str(s0/TMath.Sqrt(s0+b0))], False, False, plotodir2+var+'_cutopt1'+'.pdf', False, True, True)

            sigh.Scale(histscale * coh2.Integral()/sigh.Integral())
            bckgh.Scale(histscale * coh2.Integral()/bckgh.Integral())
            comparisonPlots([coh2, sigh, bckgh, cutline2], ['#frac{s}{#sqrt{b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut2)+'.#frac{s}{#sqrt{b}} = '+str(round(coh2.GetMaximum(), 4))+' : '+str(round(s0/TMath.Sqrt(b0), 4))], False, False, plotodir2+var+'_cutopt2'+'.pdf', False, True, True)

            sigh.Scale(histscale * coh3.Integral()/sigh.Integral())
            bckgh.Scale(histscale * coh3.Integral()/bckgh.Integral())
            comparisonPlots([coh3, sigh, bckgh, cutline3], ['#frac{s}{b}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut3)+'.#frac{s}{b} = '+str(round(coh3.GetMaximum(), 8))+' : '+str(round(s0/b0, 8))], False, False, plotodir2+var+'_cutopt3'+'.pdf', False, True, True)

if options.is2DHist:
    gStyle.SetOptTitle(1)
    gStyle.SetTitleX(.5)
    if options.isCutOpt:
        nGoodCuts = len(GoodCuts)
        for i in range(nGoodCuts):
            for j in range(nGoodCuts):
                if j>i:
                    mmhist1 = sproducer2D(GoodCuts[i], GoodCuts[j], vardict[GoodCuts[i]], vardict[GoodCuts[j]], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J']);
                    mmhist2 = sproducer2D(GoodCuts[i], GoodCuts[j], vardict[GoodCuts[i]], vardict[GoodCuts[j]], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu']);
                    mmhist3 = sproducer2D(GoodCuts[i], GoodCuts[j], vardict[GoodCuts[i]], vardict[GoodCuts[j]], 'dataC', sampledict['dataC']);
                    comparisonPlots([mmhist1], [""], False, False, plottdir+GoodCuts[i]+'_'+GoodCuts[j]+'_'+'bg''.pdf', False, False, False, True)
                    comparisonPlots([mmhist2], [""], False, False, plottdir+GoodCuts[i]+'_'+GoodCuts[j]+'_'+'signal'+'.pdf', False, False, False, True)
                    comparisonPlots([mmhist3], [""], False, False, plottdir+GoodCuts[i]+'_'+GoodCuts[j]+'_'+'data'+'.pdf', False, False, False, True)
                    
    for item in corrpairs:
        mmhist1 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J']);
        mmhist2 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu']);
        mmhist3 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'dataC', sampledict['dataC']);
        comparisonPlots([mmhist1], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'bg''.pdf', False, False, False, True)
        comparisonPlots([mmhist2], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'signal'+'.pdf', False, False, False, True)
        comparisonPlots([mmhist3], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'dataC'+'.pdf', False, False, False, True)
if options.isgen:
# The B and X types in their own separate 1D histograms and together in 2D histograms
    Xbin = ['#mu^{#pm}', '#pi^{#pm}','K^{+}', 'p', '#gamma', 'K^{0}_{s}','Other']

    vardict['X_type'] = {'xtitle': 'What sort of X produced in J/#psi+X', 'nbins': len(Xbin), 'xmin': 0, 'xmax': len(Xbin) -1, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3}
    idhist = IDsproducer('X_type', Xbin, ' JpsiMu_B_reliso < 0.2', 'X isolated') 
    if idhist.Integral()!=0:
        idhist.Scale(1/idhist.Integral())
    idhists = [idhist]
    idtitles = [idhist.GetTitle()]
    comparisonPlots(idhists, idtitles, vardict['X_type']['isLog'],vardict['X_type']['loglowerlimit'], plotgdir+'X_type.pdf', vardict['X_type']['isRatio'], vardict['X_type']['isLegended'])

    idhist2 = IDsproducer('X_type', Xbin, ' JpsiMu_B_reliso > 0.2', 'X unisolated') 
    if idhist2.Integral()!=0:
        idhist2.Scale(1/idhist2.Integral())
    idhists2 = [idhist2]
    idtitles2 = [idhist2.GetTitle()]
    comparisonPlots(idhists2, idtitles2, vardict['X_type']['isLog'],vardict['X_type']['loglowerlimit'], plotgdir+'X_type2.pdf', vardict['X_type']['isRatio'], vardict['X_type']['isLegended'])

    idhist3 = IDsproducer('X_type', Xbin, '', 'Signal', 'signal_BcJpsiMuNu')
    if idhist3.Integral()!=0:
        idhist3.Scale(1/idhist3.Integral())
    idhists3 = [idhist3]
    idtitles3 = [idhist3.GetTitle()]
    comparisonPlots(idhists3, idtitles3, vardict['X_type']['isLog'],vardict['X_type']['loglowerlimit'], plotgdir+'X_type3.pdf', vardict['X_type']['isRatio'], vardict['X_type']['isLegended'])

    vardict['X_pdgId'] = {'xtitle': 'PDGID of X classified as \'Other\'', 'nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3, 'isLogX': True}
    Xidhist = sproducer('X_pdgId', vardict['X_pdgId'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' JpsiMu_B_reliso < 0.2 && X_type == ' + str(len(Xbin)), 'X isolated', True) 
    if Xidhist.Integral()!=0:
        Xidhist.Scale(1/Xidhist.Integral())
    Xidhists = [Xidhist]
    Xidtitles = [Xidhist.GetTitle()]
    comparisonPlots(Xidhists, Xidtitles, vardict['X_pdgId']['isLog'],vardict['X_pdgId']['loglowerlimit'], plotgdir+'X_pdgId.pdf', vardict['X_pdgId']['isRatio'], vardict['X_pdgId']['isLegended'], False, False, True)

    Xidhist2 = sproducer('X_pdgId', vardict['X_pdgId'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' JpsiMu_B_reliso > 0.2 && X_type == ' + str(len(Xbin)), 'X unisolated', True) 
    if Xidhist2.Integral()!=0:
        Xidhist2.Scale(1/Xidhist2.Integral())
    Xidhists2 = [Xidhist2]
    Xidtitles2 = [Xidhist2.GetTitle()]
    comparisonPlots(Xidhists2, Xidtitles2, vardict['X_pdgId']['isLog'],vardict['X_pdgId']['loglowerlimit'], plotgdir+'X_pdgId2.pdf', vardict['X_pdgId']['isRatio'], vardict['X_pdgId']['isLegended'], False, False, True)

    sisterbin = ['#mu^{#pm}', '#pi^{0}', '#pi^{#pm}', '#rho^{+}', '#eta', '#omega', 'K^{0}', 'K^{+}', 'K^{*0}', 'K^{*+}', 'D^{+}', 'D^{0}', 'J/#psi', '#psi(2S)', '#gamma', 'K^{0}_{s}', 'D^{*+}', '#chi_{c1}', 'e', '#Lambda_{c}^{+}', 'D^{*+}_{s}', 'D^{*0}', 'B^{0}', 'K^{0}', '#Xi^{+}_{c}', 'D_{1}^{+}', 'D_{0}^{*+}', '#Lambda_{b}^{0}', 'D_{2}^{*+}', 'n', 'D_{s2}^{*+}', 'D_{s0}^{*+}', 'D_{1}^{0}', 'K^{0}', 'D_{s}^{+}', 'K^{0}_{L}', 'Other']
    vardict['sister_type'] = {'xtitle': 'Gen Level ID of X\'s Sister(s)', 'nbins': len(sisterbin), 'xmin': 0, 'xmax': len(sisterbin) -1, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3}
    sishist = IDsproducer('sister_type', sisterbin, ' JpsiMu_B_reliso < 0.2', 'X isolated') 
    if sishist.Integral()!=0:
        sishist.Scale(1/sishist.Integral())
    sishists = [sishist]
    sistitles = [sishist.GetTitle()]
    comparisonPlots(sishists, sistitles, vardict['sister_type']['isLog'],vardict['sister_type']['loglowerlimit'], plotgdir+'sister_type.pdf', vardict['sister_type']['isRatio'], vardict['sister_type']['isLegended'])

    sishist2 = IDsproducer('sister_type', sisterbin, ' JpsiMu_B_reliso > 0.2', 'X unisolated') 
    if sishist2.Integral()!=0:
        sishist2.Scale(1/sishist2.Integral())
    sishists2 = [sishist2]
    sistitles2 = [sishist2.GetTitle()]
    comparisonPlots(sishists2, sistitles2, vardict['sister_type']['isLog'],vardict['sister_type']['loglowerlimit'], plotgdir+'sister_type2.pdf', vardict['sister_type']['isRatio'], vardict['sister_type']['isLegended'])

    sishist3 = IDsproducer('sister_type', sisterbin, '', 'Signal', 'signal_BcJpsiMuNu')
    if sishist3.Integral()!=0:
        sishist3.Scale(1/sishist3.Integral())
    sishists3 = [sishist3]
    sistitles3 = [sishist3.GetTitle()]
    comparisonPlots(sishists3, sistitles3, vardict['sister_type']['isLog'],vardict['sister_type']['loglowerlimit'], plotgdir+'sister_type3.pdf', vardict['sister_type']['isRatio'], vardict['sister_type']['isLegended'])

#    vardict['genParticle_sister_pdgId'] = {'xtitle': 'PDGID of X Sisters classified as \'Other\'', 'nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3, 'isLogX': True}
#    sisidhist = sproducer('genParticle_sister_pdgId', vardict['genParticle_sister_pdgId'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' JpsiMu_B_reliso < 0.2 && sister_type == ' + str(len(sisterbin)), 'X isolated', True) 
#    if sisidhist.Integral()!=0:
#        sisidhist.Scale(1/sisidhist.Integral())
#    sisidhists = [sisidhist]
#    sisidtitles = [sisidhist.GetTitle()]
#    comparisonPlots(sisidhists, sisidtitles, vardict['genParticle_sister_pdgId']['isLog'],vardict['genParticle_sister_pdgId']['loglowerlimit'], plotgdir+'genParticle_sister_pdgId.pdf', vardict['genParticle_sister_pdgId']['isRatio'], vardict['genParticle_sister_pdgId']['isLegended'], False, False, True)
#
#    sisidhist2 = sproducer('genParticle_sister_pdgId', vardict['genParticle_sister_pdgId'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' JpsiMu_B_reliso > 0.2 && sister_type == ' + str(len(sisterbin)), 'X unisolated', True) 
#    if sisidhist2.Integral()!=0:
#        sisidhist2.Scale(1/sisidhist2.Integral())
#    sisidhists2 = [sisidhist2]
#    sisidtitles2 = [sisidhist2.GetTitle()]
#    comparisonPlots(sisidhists2, sisidtitles2, vardict['genParticle_sister_pdgId']['isLog'],vardict['genParticle_sister_pdgId']['loglowerlimit'], plotgdir+'genParticle_sister_pdgId2.pdf', vardict['genParticle_sister_pdgId']['isRatio'], vardict['genParticle_sister_pdgId']['isLegended'], False, False, True)

    Bbin = ['B^{0}','B^{+}', 'B_{s}^{0}', 'B_{c}^{+}', 'J/#psi', 'D^{0}', 'D^{+}', '#tau', '#Xi^{0}_{b}', '#psi(2S)', 'other']
    vardict['B_type'] = {'xtitle': 'Type of B', 'nbins': len(Bbin), 'xmin': 0, 'xmax': len(Bbin), 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3}
    Bidhist = IDsproducer('B_type', Bbin, ' JpsiMu_B_reliso < 0.2', 'X isolated')
    if Bidhist.Integral()!=0:
        Bidhist.Scale(1/Bidhist.Integral())
    Bidhists = [Bidhist]
    Bidtitles = [Bidhist.GetTitle()]
    comparisonPlots(Bidhists, Bidtitles, vardict['B_type']['isLog'],vardict['B_type']['loglowerlimit'], plotgdir+'B_type.pdf', vardict['B_type']['isRatio'], vardict['B_type']['isLegended'])

    Bidhist2 = IDsproducer('B_type', Bbin, ' JpsiMu_B_reliso > 0.2', 'X unisolated')
    if Bidhist2.Integral()!=0:
        Bidhist2.Scale(1/Bidhist2.Integral())
    Bidhists2 = [Bidhist2]
    Bidtitles2 = [Bidhist2.GetTitle()]
    comparisonPlots(Bidhists2, Bidtitles2, vardict['B_type']['isLog'],vardict['B_type']['loglowerlimit'], plotgdir+'B_type2.pdf', vardict['B_type']['isRatio'], vardict['B_type']['isLegended'])

    Bidhist3 = IDsproducer('B_type', Bbin, '', 'Signal', 'signal_BcJpsiMuNu')
    if Bidhist3.Integral()!=0:
        Bidhist3.Scale(1/Bidhist3.Integral())
    Bidhists3 = [Bidhist3]
    Bidtitles3 = [Bidhist3.GetTitle()]
    comparisonPlots(Bidhists3, Bidtitles3, vardict['B_type']['isLog'],vardict['B_type']['loglowerlimit'], plotgdir+'B_type3.pdf', vardict['B_type']['isRatio'], vardict['B_type']['isLegended'])

#    vardict['X_Mother_pdgId'] = {'xtitle': 'PDGID of Mothers of X classified as \'Other\'', 'nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3, 'isLogX': True}
#    momidhist = sproducer('X_Mother_pdgId', vardict['X_Mother_pdgId'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' JpsiMu_B_reliso < 0.2 && B_type == ' + str(len(sisterbin)), 'X isolated', True) 
#    if momidhist.Integral()!=0:
#        momidhist.Scale(1/momidhist.Integral())
#    momidhists = [momidhist]
#    momidtitles = [momidhist.GetTitle()]
#    comparisonPlots(momidhists, momidtitles, vardict['X_Mother_pdgId']['isLog'],vardict['X_Mother_pdgId']['loglowerlimit'], plotgdir+'X_Mother_pdgId.pdf', vardict['X_Mother_pdgId']['isRatio'], vardict['X_Mother_pdgId']['isLegended'], False, False, True)
#
#    momidhist2 = sproducer('X_Mother_pdgId', vardict['X_Mother_pdgId'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' JpsiMu_B_reliso > 0.2 && B_type == ' + str(len(sisterbin)), 'X unisolated', True) 
#    if momidhist2.Integral()!=0:
#        momidhist2.Scale(1/momidhist2.Integral())
#    momidhists2 = [momidhist2]
#    momidtitles2 = [momidhist2.GetTitle()]
#    comparisonPlots(momidhists2, momidtitles2, vardict['X_Mother_pdgId']['isLog'],vardict['X_Mother_pdgId']['loglowerlimit'], plotgdir+'X_Mother_pdgId2.pdf', vardict['X_Mother_pdgId']['isRatio'], vardict['X_Mother_pdgId']['isLegended'], False, False, True)
#
#
#    momidhist3 = sproducer('X_Mother_pdgId', vardict['X_Mother_pdgId'], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu'], ' JpsiMu_B_reliso > 0.2 && B_type == ' + str(len(sisterbin)), 'Signal', True) 
#    if momidhist3.Integral()!=0:
#        momidhist3.Scale(1/momidhist3.Integral())
#    momidhists3 = [momidhist3]
#    momidtitles3 = [momidhist3.GetTitle()]
#    comparisonPlots(momidhists3, momidtitles3, vardict['X_Mother_pdgId']['isLog'],vardict['X_Mother_pdgId']['loglowerlimit'], plotgdir+'X_Mother_pdgId3.pdf', vardict['X_Mother_pdgId']['isRatio'], vardict['X_Mother_pdgId']['isLegended'], False, False, True)
#
## Where are the photons as X coming from?
#
#    vardict['Photon_mother'] = {'xtitle': 'Mother of #gamma Tagged as X', 'nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': False, 'HasStackPlot': False, 'loglowerlimit': -3, 'isLogX': True}
#
#    photonhist = sproducer('Photon_mother', vardict['Photon_mother'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'], ' X_type == 19', '', True) 
#    comparisonPlots([photonhist], [photonhist.GetTitle()], vardict['Photon_mother']['isLog'],vardict['Photon_mother']['loglowerlimit'], plotgdir+'Photon_mother.pdf', vardict['Photon_mother']['isRatio'], vardict['Photon_mother']['isLegended'], False, False, True)

# now for the 2D histograms, splitting into first and second mother particles

    isoBX = IDsproducer2D('X_type', Xbin, 'B_type', Bbin, ' JpsiMu_B_reliso < 0.2', 'X isolated')
    comparisonPlots([isoBX], [""], False, False, plotgdir+'B_type'+'_'+'X_type'+'_'+'iso'+'.pdf', False, False, False, True)

    unisoBX = IDsproducer2D('X_type', Xbin, 'B_type', Bbin, ' JpsiMu_B_reliso > 0.2', 'X unisolated')
    comparisonPlots([unisoBX], [""], False, False, plotgdir+'B_type'+'_'+'X_type'+'_'+'uniso'+'.pdf', False, False, False, True)

    isoBsis = IDsproducer2D('sister_type', sisterbin, 'B_type', Bbin, ' JpsiMu_B_reliso < 0.2', 'X isolated')
    comparisonPlots([isoBsis], [""], False, False, plotgdir+'B_type'+'_'+'sister_type'+'_'+'iso'+'.pdf', False, False, False, True)

    unisoBsis = IDsproducer2D('sister_type', sisterbin, 'B_type', Bbin, ' JpsiMu_B_reliso > 0.2', 'X unisolated')
    comparisonPlots([unisoBsis], [""], False, False, plotgdir+'B_type'+'_'+'sister_type'+'_'+'uniso'+'.pdf', False, False, False, True)

    isosisX = IDsproducer2D('X_type', Xbin, 'sister_type', sisterbin, ' JpsiMu_B_reliso < 0.2', 'X isolated')
    comparisonPlots([isosisX], [""], False, False, plotgdir+'sister_type'+'_'+'X_type'+'_'+'iso'+'.pdf', False, False, False, True)

    unisosisX = IDsproducer2D('X_type', Xbin, 'sister_type', sisterbin, ' JpsiMu_B_reliso > 0.2', 'X unisolated')
    comparisonPlots([unisosisX], [""], False, False, plotgdir+'sister_type'+'_'+'X_type'+'_'+'uniso'+'.pdf', False, False, False, True)

# min dR between mu3 and its sister particles

    vardict['genParticle_Bdau_dRmin'] = {'xtitle': 'Min #Delta R between all gen B daughters', 'nbins': 60, 'xmin': 0, 'xmax': 3, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3}
    Bdau_dR_hist_bg =  sproducer('genParticle_Bdau_dRmin', vardict['genParticle_Bdau_dRmin'], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J'])
    bgtitle = sampledict['bg_JpsiX_MuMu_J']['title']
    sampledict['bg_JpsiX_MuMu_J']['title'] += ' [ #Delta R < 0.4 / total = '+str(round(Bdau_dR_hist_bg.Integral(1,Bdau_dR_hist_bg.GetXaxis().FindBin(0.4))/(Bdau_dR_hist_bg.Integral()+Bdau_dR_hist_bg.GetBinContent(61)), 3))+']'
    if Bdau_dR_hist_bg.Integral()!=0:
        Bdau_dR_hist_bg.Scale(1./Bdau_dR_hist_bg.Integral())
    applyHistStyle(Bdau_dR_hist_bg, 'bg_JpsiX_MuMu_J')
    Bdau_dR_hist_sig =  sproducer('genParticle_Bdau_dRmin', vardict['genParticle_Bdau_dRmin'], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu'])
    sigtitle = sampledict['signal_BcJpsiMuNu']['title']
    sampledict['signal_BcJpsiMuNu']['title'] += ' [ #Delta R < 0.4 / total = '+str(round(Bdau_dR_hist_sig.Integral(1,Bdau_dR_hist_sig.GetXaxis().FindBin(0.4))/(Bdau_dR_hist_sig.Integral()+Bdau_dR_hist_sig.GetBinContent(61)), 3))+']'
    if Bdau_dR_hist_sig.Integral()!=0:
        Bdau_dR_hist_sig.Scale(1./Bdau_dR_hist_sig.Integral())
    applyHistStyle(Bdau_dR_hist_sig, 'signal_BcJpsiMuNu')
    comparisonPlots([Bdau_dR_hist_bg, Bdau_dR_hist_sig], [sampledict['bg_JpsiX_MuMu_J']['title'], sampledict['signal_BcJpsiMuNu']['title']], vardict['genParticle_Bdau_dRmin']['isLog'], vardict['genParticle_Bdau_dRmin']['loglowerlimit'], plotgdir+'genParticle_Bdau_dRmin.pdf', vardict['genParticle_Bdau_dRmin']['isRatio'], vardict['genParticle_Bdau_dRmin']['isLegended'])

    sampledict['signal_BcJpsiMuNu']['title'] = sigtitle
    sampledict['bg_JpsiX_MuMu_J']['title'] = bgtitle

    fullhist = sproducer('genParticle_Bdau_dRmin', vardict['genParticle_Bdau_dRmin'], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu'], '', 'All X')
    
    xfrombchist = sproducer('genParticle_Bdau_dRmin', vardict['genParticle_Bdau_dRmin'], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu'], 'B_type == 4', 'X from Bc')

    xnotfrombchist = sproducer('genParticle_Bdau_dRmin', vardict['genParticle_Bdau_dRmin'], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu'], 'B_type != 4', 'X not from Bc')
    applyHistStyle(Bdau_dR_hist_sig, 'signal_BcJpsiMuNu')
    applyHistStyle(xfrombchist, 'bg_JpsiX_MuMu_J')
    applyHistStyle(xnotfrombchist, 'dataC')
    print "Number of X", fullhist.Integral()
    print "Number of X from Bc", xfrombchist.Integral()
    print "Number of X not from Bc", xnotfrombchist.Integral()
    print "Percent not from Bc:", xnotfrombchist.Integral()/fullhist.Integral()

    comparisonPlots([Bdau_dR_hist_sig, xfrombchist, xnotfrombchist], ['All X','X from Bc','X not from Bc'], vardict['genParticle_Bdau_dRmin']['isLog'], 5, plotgdir+'WheresXFromInSignal.pdf', False, True)
    
# Min gen level dR between mu3 and daughters of the other B produced in the evt (signal only)

    vardict['genParticle_Bdau_OtherB_dRmin'] = {'xtitle': 'Min #DeltaR(#mu_{3} & daugh other B)', 'nbins': 60, 'xmin': 0, 'xmax': 5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3}
    Bdau_otherB_dR_hist =  sproducer('genParticle_Bdau_OtherB_dRmin', vardict['genParticle_Bdau_OtherB_dRmin'], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu'])
    sampledict['signal_BcJpsiMuNu']['title'] += ' [ #Delta R < 0.4 / total = '+str(round(Bdau_otherB_dR_hist.Integral(1,Bdau_otherB_dR_hist.GetXaxis().FindBin(0.4))/(Bdau_otherB_dR_hist.Integral()+Bdau_otherB_dR_hist.GetBinContent(61)), 3))+']'
    applyHistStyle(Bdau_otherB_dR_hist, 'signal_BcJpsiMuNu')
    comparisonPlots([Bdau_otherB_dR_hist], [sampledict['signal_BcJpsiMuNu']['title']], vardict['genParticle_Bdau_OtherB_dRmin']['isLog'], vardict['genParticle_Bdau_OtherB_dRmin']['loglowerlimit'],  plotgdir+'genParticle_Bdau_OtherB_dRmin.pdf', vardict['genParticle_Bdau_OtherB_dRmin']['isRatio'],  vardict['genParticle_Bdau_OtherB_dRmin']['isLegended'])

vardict['mismatched_mu1'] = {'xtitle': 'PDGID of #mu_{1} in event of bad match', '  nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True  , 'HasStackPlot': False, 'loglowerlimit': 3}
vardict['mismatched_mu2'] = {'xtitle': 'PDGID of #mu_{2} in event of bad match', '  nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True  , 'HasStackPlot': False, 'loglowerlimit': 3}
vardict['mismatched_mu3'] = {'xtitle': 'PDGID of #mu_{3} in event of bad match', '  nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True  , 'HasStackPlot': False, 'loglowerlimit': 3}
vardict['mismatched_B'] = {'xtitle': 'PDGID of B in event of bad match', '  nbins': 100, 'xmin': 0, 'xmax': 6, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True  , 'HasStackPlot': False, 'loglowerlimit': 3}
    
# This writes to a webpage so you can more easily view all the plots you've created in a web browser, which will display them simultaneously.
# This is optional, you can comment it out if you want to ...
if options.isgen:
    writeHTML(gdir, "Gen Info")
if options.is2DHist:
    writeHTML(tdir, "2-D Histograms")
if options.isCompare:
    writeHTML(cdir, "Comparison Plots")
if options.isCutOpt:
    writeHTML(odir, "Cut Optimization")
    writeHTML(odir2, "Cut Optimization pt 2")
