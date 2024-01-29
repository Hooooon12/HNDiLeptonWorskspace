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
args = parser.parse_args()

# Error printing verbosity
#gErrorIgnoreLevel = kFatal

# Set batch mode
gROOT.SetBatch(True)

#tdrstyle.setTDRStyle()

# TH1 is owned by me (not gDirectory) avoiding unexpected deletion of TH1 object; see https://root.cern/manual/object_ownership/
TH1.AddDirectory(False)

#eras = ["2016preVFP","2016postVFP","2017","2018"]
eras = ["2017"]
channels = ["MuMu","EE","EMu"]
#channels = ["MuMu","EE"]
#channels = ["EMu"]
exp_channel = {
               'MuMu' : '#mu#mu',
               'EE'   : 'ee',
               'EMu'  : 'e#mu',
              }
#masses = ["M90","M100","M150","M200","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","M1300","M1500","M1700","M2000","M2500","M3000","M5000","M7500","M10000","M15000","M20000"]
#masses = ["M100"]
#masses = ["M20000"]
masses = ["M100","M150","M200","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","M1300","M1500","M1700","M2000","M2500","M3000","M5000","M7500","M10000","M15000","M20000"]
tags = ["CRtest_HNL_ULID"]
SystList = [
            "JetRes",
            "JetMass",
            "JetMassSmear",
            "JetEn",
            "MuonEn",
            "ElectronRes",
            "ElectronEn",
            "BTagSFHTag",
            "BTagSFLTag",
            "METUncl",
            "Prefire",
            "PU",
           ]
nSystBin = len(SystList)

def FoM(sig, bkg):
  this_sqrt = ((sig+bkg)*log(1+(sig/bkg)) - sig)
  if this_sqrt <= 0.:
    print "[FoM] !!!!WARNING : negative sqrt!!!!"
    print "[FoM] Check out the value :",this_sqrt
    if abs(this_sqrt) > 0.01:
      print "[FoM] Too much discrepancy."
      print "[FoM] Exiting ..."
      sys.exit(1)
    else:
      print "[FoM] Returning 0 ..."
      return 0.
  else:
    return sqrt( 2.*((sig+bkg)*log(1+(sig/bkg)) - sig) )

def MassScanHist(MassList, SR, era, channel):
  InputPath = "/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/LimitInputs/CRtest_HNL_ULID/"+era

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
    nBinSR1 = 8
    nBinSR2 = 2
    nBinSR3 = nBinSR-10

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
        if this_sig <= 0.:
          print "[WARNING] bin",this_label,"sig_cent :",this_sig
          print "[WARNING] Will skip this bin, but should check."
          continue
        else:
          print "[WARNING] bin",this_label,"sig_cent :",this_sig
          print "[WARNING] changing",this_bkg,"to 1 ..."
          this_bkg = 1.
      FoM_cent += FoM(this_sig,this_bkg)
    h_cent.SetBinContent(i+1,FoM_cent)
    h_cent.GetXaxis().SetBinLabel(i+1,MassList[i])
    yMin = min(yMin,FoM_cent)
    yMax = max(yMax,FoM_cent)

  return h_cent, yMin, yMax

def CheckNevent():
  for tag, era, mass, channel in [[tag, era, mass, channel] for tag in tags for era in eras for mass in masses for channel in channels]:
  
    h_up = TH1D('h_up', '', nSystBin, 0, nSystBin)
    h_down = TH1D('h_down', '', nSystBin, 0, nSystBin)
  
    N_up = []
    N_down = []
  
    os.system('mkdir -p Out/'+tag+'/'+era+'/Nevent')
    InputPath = "/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/LimitInputs/CRtest_HNL_ULID/"+era
    print "Opening...",InputPath+"/"+mass+"_"+channel+"_card_input.root"
    f1 = TFile.Open(InputPath+"/"+mass+"_"+channel+"_card_input.root")
    
    h_Asimov = f1.Get("data_obs")
    N_Tot = h_Asimov.Integral()
    h_Fake = f1.Get("fake")
    N_Fake = h_Fake.Integral()
    if "Mu" in channel:
      N_CF = 0
    else:
      h_CF = f1.Get("cf")
      N_CF = h_CF.Integral()
  
    for syst in SystList:
      h_conv_up     = f1.Get("conv_"+syst+"Up")
      h_prompt_up   = f1.Get("prompt_"+syst+"Up")
      h_conv_down   = f1.Get("conv_"+syst+"Down")
      h_prompt_down = f1.Get("prompt_"+syst+"Down")
  
      N_up.append(h_conv_up.Integral() + h_prompt_up.Integral() + N_Fake + N_CF)
      N_down.append(h_conv_down.Integral() + h_prompt_down.Integral() + N_Fake + N_CF)
    
    for i in range(nSystBin):
      h_up.SetBinContent(i+1,N_up[i]/N_Tot)
      h_up.GetXaxis().SetBinLabel(i+1,SystList[i])
      h_down.SetBinContent(i+1,N_down[i]/N_Tot)
      h_down.GetXaxis().SetBinLabel(i+1,SystList[i])
    
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
    h_up.GetYaxis().SetRangeUser(0.9,1.1)
    h_up.GetYaxis().SetTitle("#frac{Syst. variation}{Nominal}")
    h_up.Draw("hist")
    h_up.Draw("same p")
   
    h_down.SetStats(0)
    h_down.SetLineColor(kBlue)
    h_down.SetMarkerColor(kBlue)
    h_down.SetMarkerStyle(21)
    h_down.Draw("same hist")
    h_down.Draw("same p")
  
    lg = TLegend(0.6, 0.67, 0.95, 0.90)
    lg.SetBorderSize(0)
    lg.SetFillStyle(0)
    lg.SetHeader("#bf{Sum of the Nbkgs}", "c")
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
    latex_channel.DrawLatex(0.2, 0.88, "#splitline{"+exp_channel[channel]+"}{#splitline{"+mass+"}{Combined_SR}}")
  
    c1.SaveAs("Out/"+tag+"/"+era+"/Nevent/"+mass+"_"+channel+"_bkg.png")

def CheckFoM(SR, SP): # SignalRegion, SignalProcess (TBC)
  for tag, era, mass, channel in [[tag, era, mass, channel] for tag in tags for era in eras for mass in masses for channel in channels]:
  
    h_up = TH1D('h_up', '', nSystBin, 0, nSystBin)
    h_down = TH1D('h_down', '', nSystBin, 0, nSystBin)
  
    FoM_up = []
    FoM_down = []
  
    os.system('mkdir -p Out/'+tag+'/'+era+'/FoM/'+SR)
    InputPath = "/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/LimitInputs/CRtest_HNL_ULID/"+era
    print "Opening...",InputPath+"/"+mass+"_"+channel+"_card_input.root"
    f1 = TFile.Open(InputPath+"/"+mass+"_"+channel+"_card_input.root")
    
    h_Asimov = f1.Get("data_obs")
    h_DYVBF = f1.Get("signalDYVBF")
    h_SSWW = f1.Get("signalSSWW")
    nBinSR = h_Asimov.GetNbinsX()
    nBinSR1 = 8
    nBinSR2 = 2
    nBinSR3 = nBinSR-10

    nBinRange = {
                 'SR1' : range(nBinSR1),
                 'SR2' : range(nBinSR1,nBinSR1+nBinSR2),
                 'SR3' : range(nBinSR1+nBinSR2,nBinSR),
                 'Combined_SR' : range(nBinSR),
                }

    FoM_cent = 0.
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
        if this_sig <= 0.:
          print "[WARNING] bin",this_label,"sig_cent :",this_sig
          print "[WARNING] Will skip this bin, but should check."
          continue
        else:
          print "[WARNING] bin",this_label,"sig_cent :",this_sig
          print "[WARNING] changing",this_bkg,"to 1 ..."
          this_bkg = 1.
      FoM_cent += FoM(this_sig,this_bkg)

    h_Fake = f1.Get("fake")
    h_CF = f1.Get("cf")
  
    for syst in SystList:
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

        if this_bkg_up <= 0. or this_bkg_down <= 0.:
          print "============While counting",syst,"...============="
          print "[WARNING] bin",this_label,"bkg_up :",this_bkg_up
          print "[WARNING] bin",this_label,"bkg_down :",this_bkg_down
          if this_sig_up <= 0. or this_sig_down <= 0.:
            print "[WARNING] bin",this_label,"sig_up :",this_sig_up
            print "[WARNING] bin",this_label,"sig_down :",this_sig_down
            print "[WARNING] Will skip this bin, but should check."
            continue
          else:
            print "[WARNING] bin",this_label,"sig_up :",this_sig_up
            print "[WARNING] bin",this_label,"sig_down :",this_sig_down
            print "[WARNING] changing",this_bkg_up,"to 1 ..."
            print "[WARNING] changing",this_bkg_down,"to 1 ..."
            this_bkg_up = 1.
            this_bkg_down = 1.

        this_FoM_up += FoM(this_sig_up,this_bkg_up)
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
    latex_channel.DrawLatex(0.2, 0.88, "#splitline{"+exp_channel[channel]+"}{#splitline{"+mass+"}{"+SR+"}}")
  
    c1.SaveAs("Out/"+tag+"/"+era+"/FoM/"+SR+"/"+mass+"_"+channel+".png")

def FoMScan(SR, SP): # SignalRegion, SignalProcess (TBC)

  FullMass = ["M100","M150","M200","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","M1300","M1500","M1700","M2000","M2500","M3000","M5000","M7500","M10000","M15000","M20000"]
  nMassBin = len(FullMass)

  for tag, era, channel in [[tag, era, channel] for tag in tags for era in eras for channel in channels]:
    os.system('mkdir -p Out/'+tag+'/'+era+'/FoM/'+SR)

    h_cent, yMin_cent, yMax_cent = MassScanHist(FullMass, SR, era, channel)

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

      h_cent_SR1, yMin_SR1, yMax_SR1 = MassScanHist(FullMass, "SR1", era, channel)
      h_cent_SR2, yMin_SR2, yMax_SR2 = MassScanHist(FullMass, "SR2", era, channel)
      h_cent_SR3, yMin_SR3, yMax_SR3 = MassScanHist(FullMass, "SR3", era, channel)

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
    latex_channel.DrawLatex(0.15, 0.88, "#splitline{"+exp_channel[channel]+"}{"+SR+"}")
  
    c1.SaveAs("Out/"+tag+"/"+era+"/FoM/"+SR+"/Scan_"+channel+".png")






CheckNevent()
CheckFoM('Combined_SR',"")
CheckFoM('SR1',"")
CheckFoM('SR2',"")
CheckFoM('SR3',"")
FoMScan('Combined_SR',"")
FoMScan('SR1',"")
FoMScan('SR2',"")
FoMScan('SR3',"")

