import collections
import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack, TMath, TCanvas, TLegend, TEventList, TDirectory, gObjectTable, TLine, TH2F
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from makeSimpleHtml import writeHTML
from samples import *
from varsdict import *

from optparse import OptionParser, OptionValueError

usage = "usage: python compare.py [--compare: True, False (default: False)] [--CutOpt: True, False (default: False)] [--compareNorm: True, False (default: False)]"
parser = OptionParser(usage)
parser.add_option("-c", "--compare", default=False, action="store_true", help="Use this option to generate comparison plots between signal and background", dest="isCompare")
parser.add_option("-o", "--cutOpt", default=False, action="store_true", help="Use this option to generate scans for cut optimization", dest="isCutOpt")
parser.add_option("-n", "--compareNorm", default=False, action="store_true", help="Use this option to compare the histograms Normalized to 1", dest="isNotNorm")
parser.add_option("-t", "--twoDHist", default=False, action="store_true", help="Use this option to compare two variables and check for correlations using a two-dimensional histogram", dest="is2DHist")


(options, args) = parser.parse_args()

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

#colours = [1, 2, 4, 6, 8, 13, 15]
#styles = [1, 2, 4, 3, 5, 1, 1]
#widths = [3,3,3,3]
#c1 = TCanvas( 'c1', 'canvas', 200, 10, 700, 500 )
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

def comparisonPlots(hists, titles, isLog=False, LogRange=0, pname='sync.pdf', isRatio=True, isLegend=True, isOpt=False, is2D=False):

    display = DisplayManager(pname, isLog, isRatio, LogRange, 0.2, 0.7, isOpt, is2D)
    display.draw_legend = isLegend

    display.Draw(hists, titles, isOpt, is2D)


def sproducer(key, ivar, samplekey, sample):

    hist = TH1F('h_' + key, 
                'h_' + key, 
                ivar['nbins'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + '1' + ')'
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    if samplekey is "dataC":
        tree.Draw(key + ' >> ' + hist.GetName(), exp)
    else:
        tree.Draw(key + ' >> ' + hist.GetName(), "weight_pu[0]*"+exp)
    hist.GetXaxis().SetTitle(ivar['xtitle'])
    hist.GetYaxis().SetTitle(ivar['ytitle'])
        
    return copy.deepcopy(hist)
def optsproducer(key, ivar, samplekey, sample, tcut):

    hist = TH1F('h_' + key, 
                'h_' + key, 
                ivar['nbins'], ivar['xmin'], ivar['xmax'])

    exp = '(' + str(WeightCalc(sample['crossxn'], sample['crossxnerr'], sample['file'])[0]) + ')'
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    tree.Draw(key + ' >> ' + hist.GetName(), "weight_pu[0]*"+exp+"*"+tcut)
        
    return copy.deepcopy(hist)
def sproducer2D(key1, key2, var1, var2, samplekey, sample):

    hist = TH2F('h_' + key1 + '_' + key2, 
                'h_' + key1 + '_' + key2, 
                var1['nbins'], var1['xmin'], var1['xmax'],
                var2['nbins'], var2['xmin'], var2['xmax'])

    hist.Sumw2()
    exp = WeightCalc(sample['crossxn'],sample['crossxnerr'],sample['file'])
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    if samplekey is "dataC":
        tree.Draw(key2 + ':' + key1 + ' >> ' + hist.GetName(), '('+str(exp[0])+')')
    else:
        tree.Draw(key2 + ':' + key1  + ' >> ' + hist.GetName(), "weight_pu[0]*("+str(exp[0])+")")
    hist.GetXaxis().SetTitle(var1['xtitle'])
    hist.GetYaxis().SetTitle(var2['xtitle'])
    hist.GetZaxis().SetTitle('events')
    hist.SetTitle(samplekey)
        
    return copy.deepcopy(hist)

directory = '/eos/home-w/wvetens/www/BPH_V5/'
# to add a new variable, add a new entry in 'varsdict.py'. To add a new sample, add a new entry in 'samples.py'.
for varkey, ivar in vardict.iteritems():

    if ivar['HasStackPlot']: 
        addtostack = []
    hists = []
    titles = []
    
    var = varkey
    #print ivar
 
    if var == list(vardict.items()[0])[0]:
        for samplekey, isample in sampledict.iteritems():
            if not options.isNotNorm:
                print samplekey
                print "Weight = ", WeightCalc(isample['crossxn'],0,isample['file'])[0], " +/- ", WeightCalc(0, isample['crossxnerr'], isample['file'])[1]
    #print "Weighted Bc->J/psi+mu+nu evts: ", signal_BcJpsiMuNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,signal_BcJpsiMuNu)[0]
    #print "Weighted Bc->J/psi+tau+nu evts: ", bg_BcJpsiTauNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,bg_BcJpsiTauNu)[0]
    if options.isCompare:
        cdir = directory+'comparisons/'
        plotcdir = cdir+'plots/'
        logscdir = cdir+'logs/'
        ensureDir(plotcdir)
        ensureDir(logscdir)
    
        if ivar['HasStackPlot']:
            stackhist = THStack("stack","stack")
        for samplekey, isample in sampledict.iteritems():
            hist = sproducer(var, ivar, samplekey, isample)
            applyHistStyle(hist, samplekey)
            #hists.append(copy.deepcopy(hist))
            weight = WeightCalc(isample['crossxn'], isample['crossxnerr'], isample['file'])
            if var == list(vardict.items()[0])[0]:
                if samplekey == 'dataC':
                    isample['title'] += ' ['+str(round(isample['file'].Get('cuthist').GetBinContent(1)))+']'
                else:
                    isample['title'] += ' ['+str(round(isample['file'].Get('cuthist').GetBinContent(1)))+':'+str(round(isample['file'].Get('cuthist').GetBinContent(3)*weight[0], isample['digits']))+']'
            titles.append(isample['title'])
            #print samplekey
            #print "Weight = ", weight[0]
            #if ivar['isLegended']:
            #    Legend.AddEntry(hist, isample['title'], 'l')
            if options.isNotNorm:
                if hist.Integral()!=0:
                    hist.Scale(1./hist.Integral()) 
            if samplekey != 'dataC':
                #print "histintegral() ",hist.Integral()
                if not options.isNotNorm:
                    hist.Scale(weight[0])
                #hists.append(hist)
                hists.append(copy.deepcopy(hist))
                if ivar['HasStackPlot']:
                    stackhist.Add(copy.deepcopy(hist))
            else: 
                if not options.isNotNorm:
                    hist.Scale(23)
                #print "histintegral() ",hist.Integral()
                #hists.append(hist)
                hists.append(copy.deepcopy(hist))
    
        if ivar['HasStackPlot']:
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
          
        comparisonPlots(hists, titles, ivar['isLog'], ivar['loglowerlimit'], plotcdir+var+'.pdf', ivar['isRatio'], ivar['isLegended'])
    if options.isCutOpt:
        odir = directory+'cutopt/'
        plotodir = odir+'plots/'
        logsodir = odir+'logs/'
        ensureDir(plotodir)
        ensureDir(logsodir)
        if var not in to_optimize:
            continue
        optparams = to_optimize[var]
        granularity = optparams['granularity']
        igran = int(granularity)
        split = (optparams['xmax']-optparams['xmin'])/granularity
        #coh1name="cutopthist1"+var
        coh2name="cutopthist2"+var
        signame="sig"+var
        bckgname="bckg"+var
        #coh1 = TH1F(coh1name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        #coh1.GetYaxis().SetTitle('a.u.')
        #coh1.GetYaxis().SetTitleFont(12)
        #coh1.GetXaxis().SetTitle(str(ivar['xtitle']))
        coh2 = TH1F(coh2name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        sigh = TH1F(signame, "s", igran, optparams['xmin'], optparams['xmax'])
        bckgh = TH1F(bckgname, "b", igran, optparams['xmin'], optparams['xmax'])
        coh2.GetYaxis().SetTitle('a.u.')
        coh2.GetYaxis().SetTitleFont(12)
        coh2.GetXaxis().SetTitle(str(ivar['xtitle']))
        cut0 = 'JpsiMu_mu3_reliso < 0.25' 
        signal_BcJpsiMuNu.Get('tree').Draw(var+'>>'+signame, '('+cut0+')')
        bg_JpsiX_MuMu_J.Get('tree').Draw(var+'>>'+bckgname, '('+cut0+')')
        bh0 = optsproducer(var, ivar, samplekey, sampledict['bg_JpsiX_MuMu_J'], '('+cut0+')')
        sh0 = optsproducer(var, ivar, samplekey, sampledict['signal_BcJpsiMuNu'], '('+cut0+')')
        b0 = bh0.Integral()
        s0 = sh0.Integral()
        for x in range(1,igran):
            xparam = optparams['xmin']+split*x
            tcut = '('+var+optparams['isgl']+str(xparam)+' && '+cut0+')'
            bh = optsproducer(var, ivar, samplekey, sampledict['bg_JpsiX_MuMu_J'], tcut)
            sh = optsproducer(var, ivar, samplekey, sampledict['signal_BcJpsiMuNu'], tcut)
            b = bh.Integral()
            s = sh.Integral()
            #if (var.find('reliso')>0 or var.find('reldbiso')>0) and x == 1:
            #print "At 0.01, b = ", bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.01))*b_weight 
            #print "s = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.01))*s_weight 
            #print "s/rootb = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.01))*s_weight/TMath.Sqrt(bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.01))*b_weight)
            #print "At 0.05, b = ", bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.05))*b_weight 
            #print "s = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.05))*s_weight 
            #print "s/rootb = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.05))*s_weight/TMath.Sqrt(bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.05))*b_weight)
            #print "At 0.07, b = ", bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.07))*b_weight 
            #print "s = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.07))*s_weight 
            #print "s/rootb = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.07))*s_weight/TMath.Sqrt(bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.07))*b_weight)
            #print "At 0.2, b = ", bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.2))*b_weight 
            #print "s = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.2))*s_weight 
            #print "s/rootb = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.2))*s_weight/TMath.Sqrt(bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.2))*b_weight)
            #print "At 0.5, b = ", bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.5))*b_weight 
            #print "s = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.5))*s_weight 
            #print "s/rootb = ", signal_BcJpsiMuNu.Get('tree').GetEntries(var+optparams['isgl']+str(0.5))*s_weight/TMath.Sqrt(bg_JpsiX_MuMu_J.Get('tree').GetEntries(var+optparams['isgl']+str(0.5))*b_weight)
            if b == 0:
                #coh1.AddBinContent(x+1, 0)
                coh2.AddBinContent(x+1, 0)
            else:
                #coh1.AddBinContent(x+1, s/TMath.Sqrt(s+b))
                coh2.AddBinContent(x+1, s/TMath.Sqrt(b))
        #optcutbin1 = coh1.GetMaximumBin()
        #optcut1 = coh1.GetXaxis().GetBinCenter(optcutbin1)
        #cutline1 = TLine.TLine(optcut1, 0, optcut1, coh1.GetMaximum())
        optcutbin2 = coh2.GetMaximumBin()
        optcut2 = coh2.GetXaxis().GetBinCenter(optcutbin2)
        cutline2 = TLine.TLine(optcut2, 0, optcut2, coh2.GetMaximum())
        histscale = optparams['histscale']
        sigh.SetLineColor(2)
        bckgh.SetLineColor(4)
        #cutline1.SetLineColor(6)
        cutline2.SetLineColor(6)
        #sigh.Scale(histscale * coh1.Integral()/sigh.Integral())
        #bckgh.Scale(histscale * coh1.Integral()/bckgh.Integral())
        #comparisonPlots([coh1, sigh, bckgh, cutline1], ['#frac{s}{#sqrt{s+b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Optimal Cut: ' + var +' '+optparams['isgl']+' '+str(optcut1)+'. #frac{s}{#sqrt{s+b}} = '+str(coh1.GetMaximum())+' vs no cuts: '+str(s0/TMath.Sqrt(s0+b0))], False, False, plotodir+var+'_cutopt1'+'.pdf', False, True, True)
        sigh.Scale(histscale * coh2.Integral()/sigh.Integral())
        bckgh.Scale(histscale * coh2.Integral()/bckgh.Integral())
        comparisonPlots([coh2, sigh, bckgh, cutline2], ['#frac{s}{#sqrt{b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut2)+'.#frac{s}{#sqrt{b}} = '+str(round(coh2.GetMaximum(), 4))+' : '+str(round(s0/TMath.Sqrt(b0), 4))], False, False, plotodir+var+'_cutopt2'+'.pdf', False, True, True)

if options.is2DHist:
    tdir = directory+'2dhists/'
    plottdir = tdir+'plots/'
    logstdir = tdir+'logs/'
    ensureDir(plottdir)
    ensureDir(logstdir)
    for item in corrpairs:
        mmhist1 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'bg_JpsiX_MuMu_J', sampledict['bg_JpsiX_MuMu_J']);
        mmhist2 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu']);
        comparisonPlots([mmhist1], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'bg''.pdf', False, False, False, True)
        comparisonPlots([mmhist2], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'signal'+'.pdf', False, False, False, True)
# This writes to a webpage so you can more easily view all the plots you've created in a web browser, which will display them simultaneously.
# This is optional, you can comment it out if you want to ...
if options.is2DHist:
    writeHTML(tdir, "2-D Histograms")
if options.isCompare:
    writeHTML(cdir, "Comparison Plots")
if options.isCutOpt:
    writeHTML(odir, "Cut Optimization")
