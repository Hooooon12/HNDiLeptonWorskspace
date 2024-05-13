from ROOT import *
import os,sys,argparse
import mylib
import ctypes
import canvas_margin
import tdrstyle
import CMS_lumi, tdrstyle
from array import array

parser = argparse.ArgumentParser(description='Script for systematics summary')
parser.add_argument('-b', dest='Bkg', type=str)
parser.add_argument('-s', dest='Sig', type=str)
parser.add_argument('-r', dest='Region', type=str)
args = parser.parse_args() # to be used later, for now just run without argument

dataset = os.environ['FLATVERSION']
ENV_PLOT_PATH = os.environ['PLOT_PATH']
Outpath = ENV_PLOT_PATH+"/"+dataset+"/HNL_SignalRegion_Plotter/SystCheck"

# Error printing verbosity
#gErrorIgnoreLevel = kFatal

# Set batch mode
gROOT.SetBatch(True)

#tdrstyle.setTDRStyle()

# TH1 is owned by me (not gDirectory) avoiding unexpected deletion of TH1 object; see https://root.cern/manual/object_ownership/
TH1.AddDirectory(False)

#eras = ["2016preVFP","2016postVFP","2017","2018"]
eras = ["2017"]
#eras = ["2018"]
#channels = ["MuMu","EE","EMu"]
#channels = ["MuMu","EE"]
channels = ["EE"]
expr_channel = {
               'MuMu' : '#mu#mu',
               'EE'   : 'ee',
               'EMu'  : 'e#mu',
              }
#masses = ["M90","M100","M150","M200","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","M1300","M1500","M1700","M2000","M2500","M3000","M5000","M7500","M10000","M15000","M20000"]
masses = ["M100"]
#masses = ["M20000"]
#masses = ["M100","M150","M200","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","M1300","M1500","M1700","M2000","M2500","M3000","M5000","M7500","M10000","M15000","M20000"]
#masses = ["M100","M1000","M10000"]
#tags = ["CRtest_HNL_ULID"]
tags = ["PR48_rateParam_HNL_ULID"]
SystList = [
            "JetRes",
            #"JetMass",
            #"JetMassSmear",
            "JetEn",
            #"MuonEn",
            #"ElectronRes",
            #"ElectronEn",
            "BTagSFHTag",
            #"BTagSFLTag",
            #"METUncl",
            #"Prefire",
            #"PU",
           ]
nSystBin = len(SystList)

SRnameMap = {}
SRnameMap["SR1"] = "sr1"
SRnameMap["SR2"] = "sr2"
SRnameMap["SR3"] = "sr3"
SRnameMap["Combined_SR"] = "sr"

bkgProc = ["zg","conv","wz","zz","ww","wzewk","prompt"] #FIXME might change later?

def FoM(sig, bkg):
  this_sqrt = ((sig+bkg)*log(1+(sig/bkg)) - sig)
  if this_sqrt <= 0.:
    print "[FoM] !!!!WARNING : negative sqrt!!!!"
    print "[FoM] Check out the value :",this_sqrt
    print "[FoM] N_sig :",sig,", N_bkg :",bkg
    if this_sqrt < -0.01:
      print "[FoM] Too low sqrt."
      print "[FoM] Exiting ..."
      sys.exit(1)
    else:
      print "[FoM] Returning 0 ..."
      return 0.
  else:
    print "this bkg :", bkg
    print "this FoM :", sqrt( 2.*((sig+bkg)*log(1+(sig/bkg)) - sig) )
    return sqrt( 2.*((sig+bkg)*log(1+(sig/bkg)) - sig) )

def MassScanHist(MassList, SR, tag, era, channel):
  InputPath = "/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegion_Plotter/LimitExtraction/"+tag+"/"+era+"/"+SRnameMap[SR]

  nMassBin = len(MassList)

  h_cent = TH1D('h_cent', '', nMassBin, 0, nMassBin)
  yMin = 100000.
  yMax = 0.
  for i in range(nMassBin):

    print "Opening...",InputPath+"/"+MassList[i]+"_"+channel+"_card_input.root"
    f1 = TFile.Open(InputPath+"/"+MassList[i]+"_"+channel+"_card_input.root")

    h_Asimov = f1.Get("data_obs")
    h_DYVBF = f1.Get("signalDYVBF")
    h_SSWW = f1.Get("signalSSWW")
    nBinSR = h_Asimov.GetNbinsX()
    nBinSR1 = 6 #FIXME
    nBinSR2 = 2
    nBinRange = {
                 'SR1' : range(nBinSR1),
                 'SR2' : range(nBinSR1,nBinSR1+nBinSR2),
                 'SR3' : range(nBinSR1+nBinSR2,nBinSR),
                 'Combined_SR' : range(nBinSR),
                }

    FoM_cent = 0.
    for j in nBinRange[SR]:
      this_sig = 0.
      this_bkg = h_Asimov.GetBinContent(j+1)
      this_label = h_Asimov.GetXaxis().GetLabels().At(j).GetName() #At starts with 0: https://root.cern/doc/master/classTList.html#ae03bdf13ec16e76796e83c18eeae06d0
      try:
        this_sig += h_DYVBF.GetBinContent(j+1)
      except AttributeError:
        pass
      try:
        this_sig += h_SSWW.GetBinContent(j+1)
      except AttributeError:
        pass

      if this_bkg <= 0.:
        print "============While counting nominal in",SR,"...============="
        print "[WARNING] bin",this_label,"bkg_cent :",this_bkg
        print "[WARNING] bin",this_label,"sig_cent :",this_sig
        if this_sig <= 0.:
          print "[WARNING] Will skip this bin, but should check."
          continue
        else:
          print "[WARNING] changing",this_bkg,"to 0.1 ..."
          this_bkg = 0.1
      FoM_cent += FoM(this_sig,this_bkg)
    h_cent.SetBinContent(i+1,FoM_cent)
    h_cent.GetXaxis().SetBinLabel(i+1,MassList[i])
    yMin = min(yMin,FoM_cent)
    yMax = max(yMax,FoM_cent)

  return h_cent, yMin, yMax

def CheckNevent(SR, Type): # Type : "DYVBF", "SSWW", "bkg"
  for tag, era, mass, channel in [[tag, era, mass, channel] for tag in tags for era in eras for mass in masses for channel in channels]:

    os.system('mkdir -p '+Outpath+'/'+tag+'/'+era+'/Nevent/'+Type+'/'+SR)
    InputPath = "/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegion_Plotter/LimitExtraction/"+tag+"/"+era+"/"+SRnameMap[SR]
    print "Opening...",InputPath+"/"+mass+"_"+channel+"_card_input.root"
    f1 = TFile.Open(InputPath+"/"+mass+"_"+channel+"_card_input.root")

    # hists to draw
    h_up = TH1D('h_up', '', nSystBin, 0, nSystBin)
    h_down = TH1D('h_down', '', nSystBin, 0, nSystBin)

    # numbers to calculate
    N_up = []
    N_down = []

    # Mapping Type to the input hist name
    Type_hist = {}
    Type_hist["bkg"] = "data_obs"
    Type_hist["DYVBF"] = "signalDYVBF"
    Type_hist["SSWW"]  = "signalSSWW"

    h_Tot = f1.Get(Type_hist[Type])
    try:
      nBinSR = h_Tot.GetNbinsX()
    except AttributeError:
      print "[!!WARNING!!] There is no hist named "+Type_hist[Type]+" in "+InputPath+"/"+mass+"_"+channel+"_card_input.root"+" ."
      print "Skipping",Type_hist[Type],"..."
      continue
    #nBinSR1 = 6 #FIXME
    #nBinSR2 = 2
    #nBinRange = {
    #             'SR1' : [1,nBinSR1],
    #             'SR2' : [nBinSR1+1,nBinSR1+nBinSR2],
    #             'SR3' : [nBinSR1+nBinSR2+1,nBinSR],
    #             'Combined_SR' : [1,nBinSR],
    #            }
    #N_Tot = h_Tot.Integral(nBinRange[SR][0],nBinRange[SR][-1])
    N_Tot = h_Tot.Integral()

    h_Fake = f1.Get("fake")
    #N_Fake = h_Fake.Integral(nBinRange[SR][0],nBinRange[SR][-1])
    N_Fake = h_Fake.Integral()
    if "Mu" in channel:
      N_CF = 0
    else:
      h_CF = f1.Get("cf")
      #N_CF = h_CF.Integral(nBinRange[SR][0],nBinRange[SR][-1])
      N_CF = h_CF.Integral()

    for syst in SystList:
      thisSyst_N_up   = 0.
      thisSyst_N_down = 0.
      for bkg in bkgProc:
        this_h_up   = f1.Get(bkg+"_"+syst+"Up")
        this_h_down = f1.Get(bkg+"_"+syst+"Down")
        try:
          #this_N_up   = this_h_up.Integral(nBinRange[SR][0],nBinRange[SR][-1])
          #this_N_down = this_h_down.Integral(nBinRange[SR][0],nBinRange[SR][-1])
          this_N_up   = this_h_up.Integral()
          this_N_down = this_h_down.Integral()
        except AttributeError:
          print "[!!WARNING!!] There is no hist named "+bkg+"_"+syst+" in "+InputPath+"/"+mass+"_"+channel+"_card_input.root"+" ."
          print "Skipping",bkg,syst,"..."
          continue
        else:
          thisSyst_N_up   += this_N_up
          thisSyst_N_down += this_N_down

      h_sig_up      = f1.Get(Type_hist[Type]+"_"+syst+"Up")
      h_sig_down    = f1.Get(Type_hist[Type]+"_"+syst+"Down")

      if "bkg" in Type:
        N_up.append(thisSyst_N_up + N_Fake + N_CF)
        N_down.append(thisSyst_N_down + N_Fake + N_CF)
      else:
        #N_up.append(h_sig_up.Integral(nBinRange[SR][0],nBinRange[SR][-1]))
        #N_down.append(h_sig_down.Integral(nBinRange[SR][0],nBinRange[SR][-1]))
        N_up.append(h_sig_up.Integral())
        N_down.append(h_sig_down.Integral())

    yMax = 0.
    for i in range(nSystBin):
      #print N_Tot
      h_up.SetBinContent(i+1,N_up[i]/N_Tot)
      h_up.GetXaxis().SetBinLabel(i+1,SystList[i])
      h_down.SetBinContent(i+1,N_down[i]/N_Tot)
      h_down.GetXaxis().SetBinLabel(i+1,SystList[i])
      yMax = max( yMax, abs((N_up[i]/N_Tot)-1.), abs((N_down[i]/N_Tot)-1.) ) # max difference from 1
    yMax *= 1.2
    yMin = 1.-yMax
    yMax += 1.

    # print out the details
    print "!! Discrepancy > 10% !!"
    for i in range(nSystBin):
      if abs(N_up[i]/N_Tot-1.) >= 0.1 or abs(N_down[i]/N_Tot-1.) >= 0.1:
        print "=================================================="
        print "in",mass,channel,SR,Type,h_up.GetXaxis().GetLabels().At(i).GetName(),";"
        print "up :",N_up[i]/N_Tot,", down :",N_down[i]/N_Tot
        print "N_Tot :",N_Tot,", N_up :",N_up[i],", N_down :",N_down[i]
        print "=================================================="

    ## CANVAS
    c1 = TCanvas('c1', '', 1000, 800)
    c1.Draw()
    c1.cd()

    c1_up = TPad("c1_up", "", 0, 0, 1, 1)
    c1_up.SetTopMargin( 0.052 )
    c1_up.SetBottomMargin( 0.13 )
    c1_up.SetRightMargin( 0.032 )
    c1_up.SetLeftMargin( 0.15 )
    c1_up.Draw()
    c1_up.cd()
    #c1_up.SetLogy()

    h_up.SetStats(0)
    h_up.SetLineColor(kRed)
    h_up.SetMarkerColor(kRed)
    h_up.SetMarkerStyle(21)
    h_up.GetYaxis().SetRangeUser(yMin,yMax)
    h_up.GetYaxis().SetTitle("#frac{Syst. variation}{Nominal}")
    h_up.Draw("hist")
    h_up.Draw("same p")
 
    h_down.SetStats(0)
    h_down.SetLineColor(kBlue)
    h_down.SetMarkerColor(kBlue)
    h_down.SetMarkerStyle(21)
    h_down.Draw("same hist")
    h_down.Draw("same p")

    LineAt1 = TLine(0,1,12,1)
    LineAt1.SetLineStyle(7) # dashed line
    LineAt1.Draw("same")

    lg = TLegend(0.6, 0.67, 0.95, 0.90)
    lg.SetBorderSize(0)
    lg.SetFillStyle(0)
    lg.SetHeader("#bf{Sum of the N_"+Type+"}", "c")
    lg.AddEntry(h_up, "syst up", "lp")
    lg.AddEntry(h_down, "syst down", "lp")
    lg.Draw()

    latex_CMSPriliminary = TLatex()
    latex_CMSPriliminary.SetNDC()
    latex_CMSPriliminary.SetTextSize(0.035)
    latex_CMSPriliminary.DrawLatex(0.15, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")

    latex_Lumi = TLatex()
    latex_Lumi.SetNDC()
    latex_Lumi.SetTextSize(0.035)
    latex_Lumi.SetTextFont(42)
    latex_Lumi.SetTextAlign(31)
    latex_Lumi.DrawLatex(0.97, 0.96, mylib.TotalLumiByEra(era)+" fb^{-1} (13 TeV)")

    latex_channel = TLatex()
    latex_channel.SetNDC()
    latex_channel.SetTextSize(0.037)
    latex_channel.DrawLatex(0.2, 0.88, "#splitline{"+expr_channel[channel]+"}{#splitline{"+mass+"}{"+SR+"}}")

    c1.SaveAs(Outpath+"/"+tag+"/"+era+"/Nevent/"+Type+"/"+SR+"/"+mass+"_"+channel+"_"+SR+"_"+Type+".png")

def CheckFoM(SR, SP): # SignalRegion, SignalProcess (TBC)
  for tag, era, mass, channel in [[tag, era, mass, channel] for tag in tags for era in eras for mass in masses for channel in channels]:

    h_up = TH1D('h_up', '', nSystBin, 0, nSystBin)
    h_down = TH1D('h_down', '', nSystBin, 0, nSystBin)

    FoM_up = []
    FoM_down = []

    os.system('mkdir -p '+Outpath+'/'+tag+'/'+era+'/FoM/'+SR)
    InputPath = "/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegion_Plotter/LimitExtraction/"+tag+"/"+era+"/"+SRnameMap[SR]
    print "Opening...",InputPath+"/"+mass+"_"+channel+"_card_input.root"
    f1 = TFile.Open(InputPath+"/"+mass+"_"+channel+"_card_input.root")
    
    h_Asimov = f1.Get("data_obs")
    h_DYVBF = f1.Get("signalDYVBF")
    h_SSWW = f1.Get("signalSSWW")
    nBinSR = h_Asimov.GetNbinsX()
    nBinSR1 = 6 #FIXME
    nBinSR2 = 2
    nBinRange = {
                 'SR1' : range(nBinSR1),
                 'SR2' : range(nBinSR1,nBinSR1+nBinSR2),
                 'SR3' : range(nBinSR1+nBinSR2,nBinSR),
                 'Combined_SR' : range(nBinSR),
                }

    NegBkgBins = []
    FoM_cent = 0.
    print "In Central,"
    for i in nBinRange[SR]:
      this_sig = 0.
      this_bkg = h_Asimov.GetBinContent(i+1)
      this_label = h_Asimov.GetXaxis().GetLabels().At(i).GetName() #At starts with 0: https://root.cern/doc/master/classTList.html#ae03bdf13ec16e76796e83c18eeae06d0
      try:
        this_sig += h_DYVBF.GetBinContent(i+1)
      except AttributeError:
        pass
      try:
        this_sig += h_SSWW.GetBinContent(i+1)
      except AttributeError:
        pass

      if this_bkg <= 0.:
        print "============While counting nominal in",SR,"...============="
        print "[WARNING] bin",this_label,"bkg_cent :",this_bkg
        print "[WARNING] bin",this_label,"sig_cent :",this_sig
        if this_sig <= 0.:
          print "[WARNING] Will skip this bin, but should check."
          continue
        else:
          #print "[WARNING] Adding 0.1 to",this_bkg,"..."
          #this_bkg += 0.1
          print "[WARNING] Adding 1. to",this_bkg,"..."
          this_bkg += 1.
          NegBkgBins.append(i)
      print i+1,"th bin:"
      FoM_cent += FoM(this_sig,this_bkg)

    h_Fake = f1.Get("fake")
    h_CF = f1.Get("cf")

    for syst in SystList:
      print "In", syst+","
      h_conv_up     = f1.Get("conv_"+syst+"Up")
      h_prompt_up   = f1.Get("prompt_"+syst+"Up")
      h_DYVBF_up    = f1.Get("signalDYVBF_"+syst+"Up")
      h_SSWW_up     = f1.Get("signalSSWW_"+syst+"Up")
      h_conv_down   = f1.Get("conv_"+syst+"Down")
      h_prompt_down = f1.Get("prompt_"+syst+"Down")
      h_DYVBF_down  = f1.Get("signalDYVBF_"+syst+"Down")
      h_SSWW_down   = f1.Get("signalSSWW_"+syst+"Down")
 
      this_FoM_up = 0.
      this_FoM_down = 0.
      for i in nBinRange[SR]:
        this_sig_up = 0.
        this_sig_down = 0.
        this_label = h_Asimov.GetXaxis().GetLabels().At(i).GetName() #At starts with 0: https://root.cern/doc/master/classTList.html#ae03bdf13ec16e76796e83c18eeae06d0
        try:
          this_sig_up += h_DYVBF_up.GetBinContent(i+1)
          this_sig_down += h_DYVBF_down.GetBinContent(i+1)
        except AttributeError:
          pass
        try:
          this_sig_up += h_SSWW_up.GetBinContent(i+1)
          this_sig_down += h_SSWW_down.GetBinContent(i+1)
        except AttributeError:
          pass

        this_bkg_up = h_conv_up.GetBinContent(i+1) + h_prompt_up.GetBinContent(i+1) + h_Fake.GetBinContent(i+1)
        this_bkg_down = h_conv_down.GetBinContent(i+1) + h_prompt_down.GetBinContent(i+1) + h_Fake.GetBinContent(i+1)
        try:
          this_bkg_up += h_CF.GetBinContent(i+1)
          this_bkg_down += h_CF.GetBinContent(i+1)
        except AttributeError:
          pass

        if i in NegBkgBins:
          #print "[WARNING] Adding 0.1 to",this_bkg,"..."
          #this_bkg_up += 0.1
          #this_bkg_down += 0.1
          print "[WARNING]",i+1,"th bin was negative in the central;"
          print "[WARNING] Adding 1. to",this_bkg,"..."
          this_bkg_up += 1.
          this_bkg_down += 1.

        if this_bkg_up <= 0. or this_bkg_down <= 0.:
          print "============While counting",syst,"in",SR,"...============="
          print "[WARNING] bin",this_label,"bkg_up :",this_bkg_up
          print "[WARNING] bin",this_label,"bkg_down :",this_bkg_down
          print "[WARNING] bin",this_label,"sig_up :",this_sig_up
          print "[WARNING] bin",this_label,"sig_down :",this_sig_down
          if this_sig_up <= 0. or this_sig_down <= 0.:
            print "[WARNING] Will skip this bin, but should check."
            continue
          else:
            if this_bkg_up <= 0.:
              print "[WARNING] this_bkg_up is negative :",this_bkg_up,"--> skipping ..."
              continue
            if this_bkg_down <= 0.:
              print "[WARNING] this_bkg_down is negative :",this_bkg_down,"--> skipping ..."
              continue

        print i+1,"th Up:"
        this_FoM_up += FoM(this_sig_up,this_bkg_up)
        print i+1,"th Down:"
        this_FoM_down += FoM(this_sig_down,this_bkg_down)

      #print syst,"FoM_up :",this_FoM_up,", FoM_down :",this_FoM_down
      FoM_up.append(this_FoM_up)
      FoM_down.append(this_FoM_down)

    yMax = 0.
    for i in range(nSystBin):
      h_up.SetBinContent(i+1,FoM_up[i]/FoM_cent)
      h_up.GetXaxis().SetBinLabel(i+1,SystList[i])
      h_down.SetBinContent(i+1,FoM_down[i]/FoM_cent)
      h_down.GetXaxis().SetBinLabel(i+1,SystList[i])
      yMax = max( yMax, abs((FoM_up[i]/FoM_cent)-1.), abs((FoM_down[i]/FoM_cent)-1.) ) # max difference from 1
    yMax *= 1.2
    yMin = 1.-yMax
    yMax += 1.

    ## CANVAS
    c1 = TCanvas('c1', '', 1000, 800)
    c1.Draw()
    c1.cd()

    c1_up = TPad("c1_up", "", 0, 0, 1, 1)
    c1_up.SetTopMargin( 0.052 )
    c1_up.SetBottomMargin( 0.13 )
    c1_up.SetRightMargin( 0.032 )
    c1_up.SetLeftMargin( 0.15 )
    c1_up.Draw()
    c1_up.cd()
    #c1_up.SetLogy()

    h_up.SetStats(0)
    h_up.SetLineColor(kRed)
    h_up.SetMarkerColor(kRed)
    h_up.SetMarkerStyle(21)
    h_up.GetYaxis().SetRangeUser(yMin,yMax)
    h_up.GetYaxis().SetTitle("#frac{Syst. variation}{Nominal}")
    h_up.Draw("hist")
    h_up.Draw("same p")
 
    h_down.SetStats(0)
    h_down.SetLineColor(kBlue)
    h_down.SetMarkerColor(kBlue)
    h_down.SetMarkerStyle(21)
    h_down.Draw("same hist")
    h_down.Draw("same p")

    LineAt1 = TLine(0,1,12,1)
    LineAt1.SetLineStyle(7) # dashed line
    LineAt1.Draw("same")

    lg = TLegend(0.6, 0.67, 0.95, 0.88)
    lg.SetBorderSize(0)
    lg.SetFillStyle(0)
    lg.SetHeader("#bf{Figure of Merit}", "c")
    lg.AddEntry(h_up, "syst up", "lp")
    lg.AddEntry(h_down, "syst down", "lp")
    lg.Draw()

    latex_CMSPriliminary = TLatex()
    latex_CMSPriliminary.SetNDC()
    latex_CMSPriliminary.SetTextSize(0.035)
    latex_CMSPriliminary.DrawLatex(0.15, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")

    latex_Lumi = TLatex()
    latex_Lumi.SetNDC()
    latex_Lumi.SetTextSize(0.035)
    latex_Lumi.SetTextFont(42)
    latex_Lumi.SetTextAlign(31)
    latex_Lumi.DrawLatex(0.97, 0.96, mylib.TotalLumiByEra(era)+" fb^{-1} (13 TeV)")

    latex_channel = TLatex()
    latex_channel.SetNDC()
    latex_channel.SetTextSize(0.037)
    latex_channel.DrawLatex(0.2, 0.88, "#splitline{"+expr_channel[channel]+"}{#splitline{"+mass+"}{"+SR+"}}")

    c1.SaveAs(Outpath+"/"+tag+"/"+era+"/FoM/"+SR+"/"+mass+"_"+channel+".png")

def FoMScan(SR, SP): # SignalRegion, SignalProcess(TBA). FoM scan wrt signal mass

  FullMass = ["M100","M150","M200","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","M1300","M1500","M1700","M2000","M2500","M3000","M5000","M7500","M10000","M15000","M20000"]
  nMassBin = len(FullMass)

  for tag, era, channel in [[tag, era, channel] for tag in tags for era in eras for channel in channels]:
    os.system('mkdir -p '+Outpath+'/'+tag+'/'+era+'/FoM/'+SR)

    h_cent, yMin_cent, yMax_cent = MassScanHist(FullMass, SR, tag, era, channel)

    yMin = yMin_cent*0.1
    yMax = yMax_cent*10.
    
    ## CANVAS
    c1 = TCanvas('c1', '', 1000, 800)
    c1.Draw()
    c1.cd()
    
    c1_up = TPad("c1_up", "", 0, 0, 1, 1)
    c1_up.SetTopMargin( 0.052 )
    c1_up.SetBottomMargin( 0.13 )
    c1_up.SetRightMargin( 0.052 )
    c1_up.SetLeftMargin( 0.1 )
    c1_up.Draw()
    c1_up.cd()
    c1_up.SetLogy()

    h_cent.SetStats(0)
    h_cent.SetLineColor(9)
    h_cent.SetLineWidth(3)
    h_cent.SetMarkerColor(9)
    h_cent.SetMarkerStyle(21)
    h_cent.GetYaxis().SetRangeUser(yMin,yMax)
    h_cent.GetYaxis().SetTitle("Figure of Merit")
    h_cent.Draw("lp")

    if "Combined" in SR: 
      h_cent.SetLineColor(kBlack)
      h_cent.SetLineWidth(2)
      h_cent.SetMarkerColor(kBlack)

      h_cent_SR1, yMin_SR1, yMax_SR1 = MassScanHist(FullMass, "SR1", tag, era, channel)
      h_cent_SR2, yMin_SR2, yMax_SR2 = MassScanHist(FullMass, "SR2", tag, era, channel)
      h_cent_SR3, yMin_SR3, yMax_SR3 = MassScanHist(FullMass, "SR3", tag, era, channel)

      yMin = min(yMin_cent,yMin_SR1,yMin_SR2,yMin_SR3)
      yMax = max(yMax_cent,yMax_SR1,yMax_SR2,yMax_SR3)
      yMin *= 0.1
      yMax *= 10.

      h_cent.GetYaxis().SetRangeUser(yMin,yMax)

      color_code = {
                    'SR1' : kRed,
                    'SR2' : kOrange+6,
                    'SR3' : kBlue,
                   }

      marker_code = {
                     'SR1' : 20,
                     'SR2' : 22,
                     'SR3' : 34,
                    }

      SRhist_dir = {
                    'SR1' : h_cent_SR1,
                    'SR2' : h_cent_SR2,
                    'SR3' : h_cent_SR3,
                   }

      for this_SR in SRhist_dir.keys():
        SRhist_dir[this_SR].SetLineColor(color_code[this_SR])
        SRhist_dir[this_SR].SetLineWidth(2)
        SRhist_dir[this_SR].SetMarkerColor(color_code[this_SR])
        SRhist_dir[this_SR].SetMarkerStyle(marker_code[this_SR])
        SRhist_dir[this_SR].GetYaxis().SetRangeUser(yMin,yMax)
        SRhist_dir[this_SR].GetYaxis().SetTitle("Figure of Merit")
        SRhist_dir[this_SR].Draw("same lp")

      lg = TLegend(0.6, 0.67, 0.95, 0.88)
      lg.SetBorderSize(0)
      lg.SetFillStyle(0)
      lg.SetHeader("#bf{Figure of Merit}", "c")
      lg.AddEntry(h_cent, "Combined", "lp")
      lg.AddEntry(h_cent_SR1, "SR1", "lp")
      lg.AddEntry(h_cent_SR2, "SR2", "lp")
      lg.AddEntry(h_cent_SR3, "SR3", "lp")
      lg.Draw()

    latex_CMSPriliminary = TLatex()
    latex_CMSPriliminary.SetNDC()
    latex_CMSPriliminary.SetTextSize(0.035)
    latex_CMSPriliminary.DrawLatex(0.15, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")
    
    latex_Lumi = TLatex()
    latex_Lumi.SetNDC()
    latex_Lumi.SetTextSize(0.035)
    latex_Lumi.SetTextFont(42)
    latex_Lumi.SetTextAlign(31)
    latex_Lumi.DrawLatex(0.95, 0.96, mylib.TotalLumiByEra(era)+" fb^{-1} (13 TeV)")

    latex_channel = TLatex()
    latex_channel.SetNDC()
    latex_channel.SetTextSize(0.037)
    latex_channel.DrawLatex(0.15, 0.88, "#splitline{"+expr_channel[channel]+"}{"+SR+"}")

    c1.SaveAs(Outpath+"/"+tag+"/"+era+"/FoM/"+SR+"/Scan_"+channel+".png")



#SRlist = ["SR1","SR2","SR3","Combined_SR"]
#SRlist = ["Combined_SR"]
SRlist = ["SR2"]
#Typelist = ["bkg","DYVBF","SSWW"]
#Typelist = ["DYVBF"]
Typelist = ["bkg"]

for sr, tp in [[sr, tp] for sr in SRlist for tp in Typelist]:
  CheckNevent(sr,tp)

#for sr in SRlist:
#  CheckFoM(sr,"")
#  #FoMScan(sr,"")

#CheckFoM('Combined_SR',"")
#CheckFoM('SR1',"")
#CheckFoM('SR2',"")
#CheckFoM('SR3',"")
#FoMScan('Combined_SR',"")
#FoMScan('SR1',"")
#FoMScan('SR2',"")
#FoMScan('SR3',"")
