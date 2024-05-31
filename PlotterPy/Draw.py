### python Draw.py -e 2017

import os,ROOT,sys

WORKING_DIR = os.environ['HNDILEPTONWORKSPACE_DIR']

sys.path.insert(1, WORKING_DIR+'/python')

from Plotter import SampleGroup, Variable, Region, Systematic
from Plotter import Plotter
from IsCorrelated import IsCorrelated

import argparse

ROOT.gROOT.SetBatch(ROOT.kTRUE)

#if not os.path.exists('/tmp/ssh-jalmond@lxplus.cern.ch'):
from GeneralSetup import check_lxplus_connection,GetFromConfig
#check_lxplus_connection() #JH


## Arguments

parser = argparse.ArgumentParser(description='CR, SR plot commands')
parser.add_argument('-c', dest='Category', type=int, default=0)
parser.add_argument('-y', dest='Year', type=int, default=0)
parser.add_argument('-e', dest='Era', type=str, default='NULL')
parser.add_argument('--debug',action='store_true')
parser.add_argument('--ScaleMC', action='store_true')
args = parser.parse_args()

OutPutOnLxplus=False
## Enviroment

dataset = os.environ['FLATVERSION']
ENV_PLOT_PATH = os.environ['PLOT_PATH']

m = Plotter()

m.DoDebug = args.debug

#### In/Out

if args.Year > 0:
  m.DataEra = str(args.Year)
  m.DataYear=str(args.Year)

else:
  
  if not args.Era == "NULL":
    m.DataEra = args.Era
    if "2016" in args.Era:
      m.DataYear = 2016
    else:
      m.DataYear = int(args.Era)
  else:
    m.DataEra = "Run2"
    m.DataYear = "Run2"
      

print ("DataYear Set to " + str(m.DataYear))
print ("DataEra Set to " + str(m.DataEra))


AllowedEras=["2016","2016preVFP","2016postVFP","2017","2018", "Run2"]
if not m.DataEra in AllowedEras:
  print("Era input is incorrect")
  exit()

str_Era=m.DataEra

m.DataDirectory = "DATA"
# typical root file name convention --> Analyzer_Skim_SampleName(_suffix).root

# check connection to lxplus is open
#check_lxplus_connection()

#set username for lxplus
#m.Lxplus_User = GetFromConfig('LXPLUS_USER')
#m.Lxplus_Dir = GetFromConfig('LXPLUS_Dir')

#print m.Lxplus_User + " " + m.Lxplus_Dir
#exit()

#if OutPutOnLxplus:
#  m.OutputDirectory = m.Lxplus_Dir
#  print "-"*40
#  print("ssh "+m.Lxplus_User+"@lxplus.cern.ch 'mkdir -p " + m.OutputDirectory + "'")
#  print "-"*40
#  os.system("ssh "+m.Lxplus_User+"@lxplus.cern.ch 'mkdir -p " + m.OutputDirectory + "'")


#### Category
m.ScaleMC = args.ScaleMC

#### Systematic
tmp_Systematics = [
  #"Lumi",
  "JetRes",
  "JetEn",
  #"JetMass",
  #"JetMassSmear",
  #"MuonEn",
  #"MuonRecoSF",
  #"MuonIDSF",
  #"MuonISOSF",
  #"MuonTriggerSF",
  #"ElectronRecoSF",
  #"ElectronIDSF",
  #"ElectronTriggerSF",
  #"ElectronRes",
  #"ElectronEn",
  #"PU",
  #"Prefire",
  "BTagSFHTag",
  #"BTagSFLTag",
  #"GetMCUncertainty",
  #"DYNorm",
  #"DYReshapeSyst",
  #"NonPromptNorm",
  #"OthersNorm",
]

m.Systematics = [ Systematic(Name="Central", Direction=0, Year=-1) ]
for s in tmp_Systematics:
  isCorr = IsCorrelated(s)
  if isCorr:
    m.Systematics.append( Systematic(Name=s, Direction=+1, Year=-1) )
    m.Systematics.append( Systematic(Name=s, Direction=-1, Year=-1) )
  else:
    if m.DataYear>0:
      m.Systematics.append( Systematic(Name=s, Direction=+1, Year=m.DataYear) )
      m.Systematics.append( Systematic(Name=s, Direction=-1, Year=m.DataYear) )
    else:
      for Y in [2016,2017,2018]:
        m.Systematics.append( Systematic(Name=s, Direction=+1, Year=Y) )
        m.Systematics.append( Systematic(Name=s, Direction=-1, Year=Y) )
m.PrintSystematics()

SetBinningPerEra=False

if not SetBinningPerEra:
  #### Binning infos
  m.SetBinningFilepath(
    WORKING_DIR+'/data/'+dataset+'/YearCombined/Rebins.txt',
    WORKING_DIR+'/data/'+dataset+'/YearCombined/Xaxis.txt',
    WORKING_DIR+'/data/'+dataset+'/YearCombined/CR_yaxis.txt',
  )
else: # binning per era
  m.SetBinningFilepath(
    WORKING_DIR+'/data/'+dataset+'/'+str_Era+'/CR_rebins.txt',
    WORKING_DIR+'/data/'+dataset+'/'+str_Era+'/CR_xaxis.txt',
    WORKING_DIR+'/data/'+dataset+'/'+str_Era+'/CR_yaxis.txt',
  )


#### Predef samples
from PredefinedSamples import *

#TODO make SampleGroups dependent on each regions to draw

if args.Category==0: # ?
  #### Define Samples
  if str_Era != 'Run2':
    ############## samples for SS_CR, VBF_CR, LLL_VR ##############
    #exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_Conv_%s, SampleGroup_MC_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_Conv_others_%s, SampleGroup_ZG_%s, SampleGroup_DYJets_MG_%s, SampleGroup_WZ_%s, SampleGroup_ZZ_%s, SampleGroup_VVV_%s, SampleGroup_ttV_%s, SampleGroup_TTXX_%s, SampleGroup_tZq_%s, SampleGroup_Higgs_%s, SampleGroup_VBFHiggs_%s, SampleGroup_WW_%s, SampleGroup_WZ_EWK_%s, SampleGroup_ggH_%s, SampleGroup_ggZZ_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_Conv_others_%s, SampleGroup_ZG_%s, SampleGroup_DYJets_MiNNLO_EE_%s, SampleGroup_DYJets_MiNNLO_MuMu_%s, SampleGroup_DYJets_MiNNLO_TauTau_%s, SampleGroup_WZ_%s, SampleGroup_ZZ_%s, SampleGroup_VVV_%s, SampleGroup_ttV_%s, SampleGroup_TTXX_%s, SampleGroup_tZq_%s, SampleGroup_Higgs_%s, SampleGroup_VBFHiggs_%s, SampleGroup_WW_%s, SampleGroup_WZ_EWK_%s, SampleGroup_ggH_%s, SampleGroup_ggZZ_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    ############## samples for OS_VR #######################
    #exec('m.SampleGroups = [SampleGroup_DY_%s, SampleGroup_DYtau_%s, SampleGroup_WJets_MG_OS_%s, SampleGroup_WG_OS_%s, SampleGroup_ZG_OS_%s, SampleGroup_TTLL_%s, SampleGroup_VV_OS_%s, SampleGroup_tW_%s, SampleGroup_FakeOS_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    ############## samples for SRs #######################
    #exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_Conv_%s, SampleGroup_MC_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    exec('m.SignalsToDraw = [SampleGroup_DYTypeI_%s_M1000, SampleGroup_VBFTypeI_%s_M1000, SampleGroup_SSWWTypeI_%s_M1000]'%(m.DataEra, m.DataEra, m.DataEra))
  else:
    m.SampleGroups = [
      SampleGroup_Fake_Run2,SampleGroup_CF_Run2,SampleGroup_Conv_Run2,SampleGroup_Prompt_Run2
    ]
    m.SignalsToDraw = [SampleGroup_DYTypeI_Run2_M1000, SampleGroup_VBFTypeI_Run2_M1000, SampleGroup_SSWWTypeI_Run2_M1000]

  #### Signals
  #### Print
  m.PrintSamples()

  #PNs=["MVAUL_PtCone_HNTightV2","MVAUL_HNTightV2","MVAUL_HNL_ULID_2017","MVAUL_LFvsHF_cut0_HNTightV2","MVAUL_LFvsHF_cut0_HNL_ULID_2017","MVAUL_LFvsHF_cut0p8_HNTightV2","MVAUL_LFvsHF_cut0p8_HNL_ULID_2017","MVAUL_TriLep_HNL_ULID_2017"] # parameter name (this is used in hist path)
  #PNs=["HNL_ULID_HNL_ULID_FO_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv2_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv3_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv4_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv5_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv6_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FO_BDTFlavour_PtCorr_NoPR"] # parameter name (this is used in hist path)
  #PNs=["HNL_ULID_HNL_ULID_FO_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv2_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv3_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv4_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv5_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv6_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FO_BDTFlavour_PtParton_NoPR"] # parameter name (this is used in hist path)
  #PNs=["HNL_ULID", "HNTightV2"] # parameter name (this is used in hist path)
  PNs=["HNL_ULID"] # parameter name (this is used in hist path)

  RegionNames = {
                 ### VBF_CR ##
                 #"HNL_WpWp_TwoLepton_CR1" : "WpWp_CR1",
                 #"HNL_WpWp_TwoLepton_CR2" : "WpWp_CR2",
                 #"HNL_WpWpNP_TwoLepton_CR" : "WpWpNP_CR",
                 #"HNL_WpWpNP2_TwoLepton_CR" : "WpWpNP2_CR",
                 #"HNL_WpWpNP3_TwoLepton_CR" : "WpWpNP3_CR",
                 ### SS_CR ##
                 #"HNL_SSPresel_TwoLepton" : "SSPresel",
                 #"HNL_HighMassSR1_TwoLepton_CR" : "SR1_CR",
                 #"HNL_HighMassSR2_TwoLepton_CR" : "SR2_CR",
                 #"HNL_HighMassSR3_TwoLepton_CR" : "SR3_CR",
                 #"HNL_HighMassSR3_2J_TwoLepton_CR" : "SR3_2Jet_CR",
                 #"HNL_HighMassSSZPeak_TwoLepton_CR" : "SSZpeak_CR",
                 #"HNL_HighMassSSZPeak_AK8_TwoLepton_CR" : "SSZpeak_AK8_CR",
                 #"HNL_HighMass1Jet_TwoLepton_CR" : "1Jet_CR",
                 #"HNL_HighMassBJet_TwoLepton_CR" : "BJet_CR",
                 #"HNL_HighMassNP_TwoLepton_CR" : "0Jet_CR",
                 ### LLL_VR ###
                 #"HNL_WZ_SR1_ThreeLepton_CR" : "WZ_SR1_CR",
                 #"HNL_WZVBF_ThreeLepton_CR" : "WZVBF_CR",
                 #"HNL_WZVBF2_ThreeLepton_CR" : "WZVBF2_CR",
                 #"HNL_WZB_ThreeLepton_CR" : "WZB_CR",
                 #"HNL_WZ_SR3_ThreeLepton_CR" : "WZ_SR3_CR",
                 #"HNL_ZZ_FourLepton_CR"  : "ZZ_CR",
                 #"HNL_ZG_ThreeLepton_CR" : "ZG_CR",
                 #"HNL_ZNPEl_ThreeLepton_CR" : "ZNPel_CR",
                 #"HNL_ZNPMu_ThreeLepton_CR" : "ZNPmu_CR",
                 #"HNL_WG_ThreeLepton_CR" : "WG_CR",
                 #"HNL_WZ2_ThreeLepton_CR" : "WZ2_CR",
                 #"HNL_WZB_ThreeLepton_CR" : "WZb_CR",
                 #"HNL_ZZLoose_FourLepton_CR"  : "ZZloose_CR",
                 #"HNL_TopNP_ThreeLepton_CR" : "TopNP_CR",
                 ## OS_VR ##
                 #"HNL_OS_Z_TwoLepton_CR"      : "Z_CR",
                 #"HNL_OS_Top_TwoLepton_CR"    : "Top_CR",
                 #"HNL_OS_Top2b_TwoLepton_CR"  : "Top2b_CR",
                 #"HNL_OS_ZAK8_TwoLepton_CR"   : "ZAK8_CR",
                 #"HNL_OS_TopAK8_TwoLepton_CR" : "TopAK8_CR",
                 ## SR ##
                 "LimitBins" : "Limit Input (Cut-based)",
                 #"LimitBinsBDT_M100" : "Limit Input (M100)",
                 #"LimitBinsBDT_M200" : "Limit Input (M200)",
                 #"LimitBinsBDT_M300" : "Limit Input (M300)",
                 #"LimitBinsBDT_M400" : "Limit Input (M400)",
                 #"LimitBinsBDT_M500" : "Limit Input (M500)",
                 #"PassSR1" : "SR1 w/o M(llJ)",
                 #"LimitShape_SR1" : "SR1 (MN1 binned)",
                 #"DiJetSR3" : "DiJetSR3",
                 #"InclusiveSR1" : "InclusiveSR1",
                 #"FinalSR1" : "FinalSR1",
                }

  RegionChannels = {
                    "FourLepton"  : {
                                     "MuMuMuMu" : "#mu#mu#mu#mu",
                                     "EEEE"     : "eeee",
                                     "EMuLL"    : "e#mu+ll",
                                     "LLLL"     : "llll",
                                    },
                    "ThreeLepton" : {
                                     "MuMuMu" : "#mu#mu#mu",
                                     "EEE"    : "eee",
                                     "EMuL"   : "e#mu+l",
                                     "LLL"    : "lll",
                                    },
                    "TwoLepton"   : {
                                     "MuMu" : "#mu#mu",
                                     "EE"   : "ee",
                                     "EMu"  : "e#mu",
                                     "LL"   : "ll",
                                    },
                   }

  UnblindData = {
                 'HNL_ControlRegion_Plotter' : True,
                 'HNL_SignalRegion_Plotter' : False,
                }

  DrawData = {
              'HNL_ControlRegion_Plotter' : True,
              'HNL_SignalRegion_Plotter' : False,
             }

  #### Define regions
  m.RegionsToDraw = []

  for RegionName, RegionLatex in RegionNames.items():

    # Analyser, Input files now depend on which region to draw.
    if ("CR" in RegionName) or ("Presel" in RegionName):
      Analyser='HNL_ControlRegion_Plotter'
    else:
      Analyser='HNL_SignalRegion_Plotter'

    m.Filename_prefix = Analyser
    m.Filename_suffix = ""
    m.OutputDirectoryLocal = ENV_PLOT_PATH+"/"+dataset+"/"+Analyser+"/"+str_Era # HNDiLeptonWorkspace/Output/Plots/Run2UltraLegacy_v3/Analyzer/Era. where the output plots will be stored.
    os.system('mkdir -p '+ m.OutputDirectoryLocal)
    if args.ScaleMC:
      os.system('mkdir -p '+ m.OutputDirectoryLocal+'/ScaleMC/')

    # Define input directory depending on the region name.
    if Analyser == 'HNL_ControlRegion_Plotter':
      if "ThreeLepton" in RegionName or "FourLepton" in RegionName:
        InputDirectory = '/data6/Users/jihkim/SKFlatOutput/'+dataset+"/"+Analyser+"/"+str_Era+"/LLL_VR__" # where the root itput files are stored.
      elif "TwoLepton" in RegionName and ("CR" in RegionName and "WpWp" in RegionName):
        InputDirectory = '/data6/Users/jihkim/SKFlatOutput/'+dataset+"/"+Analyser+"/"+str_Era+"/VBF_CR__" # where the root itput files are stored.
      elif "TwoLepton" in RegionName and (("CR" in RegionName and not "OS" in RegionName) or ("SSPresel" in RegionName)):
        InputDirectory = '/data6/Users/jihkim/SKFlatOutput/'+dataset+"/"+Analyser+"/"+str_Era+"/SS_CR__" # where the root itput files are stored.
      elif "TwoLepton" in RegionName and ("CR" in RegionName and "OS" in RegionName):
        InputDirectory = '/data6/Users/jihkim/SKFlatOutput/'+dataset+"/"+Analyser+"/"+str_Era+"/OS_VR__" # where the root itput files are stored.
    else:
      InputDirectory = '/data6/Users/jihkim/SKFlatOutput/'+dataset+"/"+Analyser+"/"+str_Era+"/"

    # Define data skim following the region
    if "OS_VR" in InputDirectory:
      m.Filename_data_skim = "_SkimTree_DileptonBDT" # use "" if no skim was used
    else:
      m.Filename_data_skim = "_SkimTree_HNMultiLepBDT" # use "" if no skim was used

    for PN in PNs:

      for RegionChannel, Channels in RegionChannels.items():
        if RegionChannel is "FourLepton" or RegionChannel is "ThreeLepton":
          if not RegionChannel in RegionName: continue #The ThreeLepton, FourLepton must be included in the Region Name. If not, TwoLepton is assumed.
        for Channel, ChannelLatex in Channels.items():
          m.RegionsToDraw.append( Region(RegionName, Channel, PN, InputDirectory, '', '', UnblindData[Analyser], Logy=0, TLatexAlias='#splitline{'+ChannelLatex+'}{'+RegionLatex+'}', CutFlowCaption='', DrawData=DrawData[Analyser], DrawRatio=True) )
          #m.RegionsToDraw.append( Region(RegionName, Channel, PN, InputDirectory, '', 'MiNNLO', UnblindData[Analyser], Logy=0, TLatexAlias='#splitline{'+ChannelLatex+'}{'+RegionLatex+'}', CutFlowCaption='', DrawData=True, DrawRatio=True) )


  #m.PrintRegions()


#### Define Variables
m.VariablesToDraw = [
  #Variable('MuonCR', 'Inclusive SR', ''),
  #Variable('ElectronCR', 'Inclusive SR', ''),
  #Variable('ElectronMuonCR', 'Inclusive SR', ''),
  #Variable('MuonCRBDT', 'Inclusive SR', ''),
  #Variable('ElectronCRBDT', 'Inclusive SR', ''),
  #Variable('ElectronMuonCRBDT', 'Inclusive SR', ''),
  #Variable('MuonSR', 'Inclusive SR', ''),
  #Variable('ElectronSR', 'Inclusive SR', ''),
  #Variable('ElectronMuonSR', 'Inclusive SR', ''),
  Variable('MuonSR1', 'SR1', ''),
  Variable('ElectronSR1', 'SR1', ''),
  Variable('ElectronMuonSR1', 'SR1', ''),
  Variable('MuonSR2', 'SR2', ''),
  Variable('ElectronSR2', 'SR2', ''),
  Variable('ElectronMuonSR2', 'SR2', ''),
  Variable('MuonSR3', 'SR3', ''),
  Variable('ElectronSR3', 'SR3', ''),
  Variable('ElectronMuonSR3', 'SR3', ''),
  #Variable('MuonSR3BDT', 'SR3BDT', ''),
  #Variable('ElectronSR3BDT', 'SR3BDT', ''),
  #Variable('ElectronMuonSR3BDT', 'SR3BDT', ''),
  #Variable('MuonSRBDT', 'Inclusive SR', ''),
  #Variable('ElectronSRBDT', 'Inclusive SR', ''),
  #Variable('ElectronMuonSRBDT', 'Inclusive SR', ''),
  #Variable('N1Mass_Central', 'M_{N1}', 'GeV'),
  #Variable('AK8J_Mass/llJ', 'M_{llJ}', 'GeV'),
  #Variable('Lep_1_pt', 'p_{T} of the leading lepton', 'GeV'),
  #Variable('Lep_2_pt', 'p_{T} of the second lepton', 'GeV'),
  #Variable('Lep_1_eta', '#eta of the leading lepton', ''),
  #Variable('Lep_2_eta', '#eta of the second lepton', ''),
  #Variable('Lep_3_pt', 'p_{T} of the third lepton', 'GeV'),
  #Variable('Lep_4_pt', 'p_{T} of the fourth lepton', 'GeV'),
  #Variable('Lep_3_eta', '#eta of the third lepton', ''),
  #Variable('Lep_4_eta', '#eta of the fourth lepton', ''),
  #Variable('Jet_1_pt', 'p_{T} of the leading jet', 'GeV'),
  #Variable('Jet_2_pt', 'p_{T} of the second jet', 'GeV'),
  #Variable('Jet_1_eta', '#eta of the leading jet', 'GeV'),
  #Variable('Jet_2_eta', '#eta of the second jet', 'GeV'),
  #Variable('M_ll', 'M_{ll}', 'GeV'),
  #Variable('DiJet_M_lljj', 'M_{lljj}', 'GeV'),
  #Variable('DiJet_M_l1jj', 'M_{l1jj}', 'GeV'),
  #Variable('Ev_MET', 'MET', 'GeV'),
  #Variable('Ev_MET2_ST', 'MET^{2}/S_{T}', 'GeV'),
  #Variable('N_BJet', 'N_{bj}',''),
  #Variable('N_AK4J', 'N_{j}', ''),
  #Variable('N_Mu', 'N_{#mu}', ''),
  #Variable('N_El', 'N_{e}', ''),

]
m.PrintVariables()

#### Draw
m.DoSystCheck()

#m.DoCutFlow('NJets')
