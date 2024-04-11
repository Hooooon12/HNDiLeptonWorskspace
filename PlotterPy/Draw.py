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
    m.DataEra = "YearCombined"
    m.DataYear = -1
      

print ("DataYear Set to " + str(m.DataYear))
print ("DataEra Set to " + str(m.DataEra))


AllowedEras=["2016","2016preVFP","2016postVFP","2017","2018", "YearCombined"]
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
  #"JetRes",
  #"JetEn",
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
  #"BTagSFHTag",
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
  if str_Era != 'YearCombined':
    ############## samples for SS CRs ##############
    #exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_VV_%s, SampleGroup_Conv_%s, SampleGroup_WZ_EWK_%s, SampleGroup_WpWp_%s, SampleGroup_Others_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_Conv_%s, SampleGroup_MC_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    ############## samples for OS CRs #######################
    #exec('m.SampleGroups = [SampleGroup_DY_%s, SampleGroup_DYtau_%s, SampleGroup_WJets_MG_%s, SampleGroup_TTLL_%s, SampleGroup_VV_%s, SampleGroup_tW_%s, SampleGroup_FakeOS_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    ############## samples for SRs #######################
    #exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_CF_%s, SampleGroup_Conv_%s, SampleGroup_MC_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SignalsToDraw = [SampleGroup_DYTypeI_%s_M1000, SampleGroup_VBFTypeI_%s_M1000, SampleGroup_SSWWTypeI_%s_M1000]'%(m.DataEra, m.DataEra, m.DataEra))
  else:
    m.SampleGroups = [
      SampleGroup_TTLL_2016preVFP,SampleGroup_TTLL_2016postVFP,SampleGroup_TTLL_2017,SampleGroup_TTLL_2018,
      SampleGroup_TW_2016preVFP,SampleGroup_TW_2016postVFP,SampleGroup_TW_2017,SampleGroup_TW_2018,
      SampleGroup_VV_incl_2016preVFP, SampleGroup_VV_incl_2016postVFP, SampleGroup_VV_incl_2017, SampleGroup_VV_incl_2018,
      SampleGroup_DY_2016preVFP, SampleGroup_DY_2016postVFP, SampleGroup_DY_2017, SampleGroup_DY_2018,
    ]

  #### Signals
  #### Print
  m.PrintSamples()

  #PNs=["MVAUL_PtCone_HNTightV2","MVAUL_HNTightV2","MVAUL_HNL_ULID_2017","MVAUL_LFvsHF_cut0_HNTightV2","MVAUL_LFvsHF_cut0_HNL_ULID_2017","MVAUL_LFvsHF_cut0p8_HNTightV2","MVAUL_LFvsHF_cut0p8_HNL_ULID_2017","MVAUL_TriLep_HNL_ULID_2017"] # parameter name (this is used in hist path)
  #PNs=["HNL_ULID_HNL_ULID_FO_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv2_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv3_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv4_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv5_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FOv6_Standard_PtCorr_NoPR","HNL_ULID_HNL_ULID_FO_BDTFlavour_PtCorr_NoPR"] # parameter name (this is used in hist path)
  #PNs=["HNL_ULID_HNL_ULID_FO_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv2_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv3_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv4_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv5_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FOv6_Standard_PtParton_NoPR","HNL_ULID_HNL_ULID_FO_BDTFlavour_PtParton_NoPR"] # parameter name (this is used in hist path)
  #PNs=["HNL_ULID", "HNTightV2"] # parameter name (this is used in hist path)
  PNs=["HNL_ULID"] # parameter name (this is used in hist path)

  RegionNames = {
                 "HNL_SSPresel_TwoLepton" : "SSPresel",
                 #"HNL_HighMassSR1_TwoLepton_CR" : "SR1_CR",
                 #"HNL_HighMassCR2_TwoLepton_CR" : "SR2_CR", #FIXME later to SR2
                 #"HNL_HighMassSR3_TwoLepton_CR" : "SR3_CR",
                 #"HNL_HighMassSR3LowJet_TwoLepton_CR" : "SR3_01Jet_CR",
                 #"HNL_HighMassSR3_2J_TwoLepton_CR" : "SR3_2Jet_CR",
                 #"HNL_HighMass1Jet_TwoLepton_CR" : "1Jet_CR",
                 #"HNL_HighMassBJet_TwoLepton_CR" : "BJet_CR",
                 #"HNL_HighMassNP_TwoLepton_CR" : "0Jet_CR",
                 #"HNL_WZ_ThreeLepton_CR" : "WZ_CR",
                 #"HNL_ZZ_FourLepton_CR"  : "ZZ_CR",
                 #"HNL_ZG_ThreeLepton_CR" : "ZG_CR",
                 #"HNL_WG_ThreeLepton_CR" : "WG_CR",
                 #"HNL_OS_Z_TwoLepton_CR"      : "Z_CR",
                 #"HNL_OS_Top_TwoLepton_CR"    : "Top_CR",
                 #"HNL_OS_Top2b_TwoLepton_CR"  : "Top2b_CR",
                 #"HNL_OS_ZAK8_TwoLepton_CR"   : "ZAK8_CR",
                 #"HNL_OS_TopAK8_TwoLepton_CR" : "TopAK8_CR",
                 #"LimitInput" : "Limit Input (Cut-based)",
                 #"LimitInputBDT_M100" : "Limit Input (M100)",
                 #"DiJetSR3" : "DiJetSR3",
                 #"InclusiveSR1" : "InclusiveSR1",
                 #"FinalSR1" : "FinalSR1",
                }

  RegionChannels = {
                    "FourLepton"  : {
                                     "MuMuMuMu" : "#mu#mu#mu#mu",
                                     "EEEE"     : "eeee",
                                     "EMuLL"    : "e#mu+ll",
                                    },
                    "ThreeLepton" : {
                                     "MuMuMu" : "#mu#mu#mu",
                                     "EEE"    : "eee",
                                     "EMuL"   : "e#mu+l",
                                    },
                    "TwoLepton"   : {
                                     "MuMu" : "#mu#mu",
                                     "EE"   : "ee",
                                     "EMu"  : "e#mu",
                                    },
                   }

  UnblindData = {
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
          m.RegionsToDraw.append( Region(RegionName, Channel, PN, InputDirectory, '', '', UnblindData[Analyser], Logy=0, TLatexAlias='#splitline{'+ChannelLatex+'}{'+RegionLatex+'}', CutFlowCaption='', DrawData=True, DrawRatio=True) )


    #SRs
    #m.RegionsToDraw.append( Region('LimitInput', 'MuonSR', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{LimitInput}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #Region('LimitInputBDT_M100', 'MuonSR', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{LimitInputBDT_M100}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #m.RegionsToDraw.append( Region('DiJetSR3', 'MuMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{DiJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR1', 'MuMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{InclusiveSR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR2', 'MuMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{InclusiveSR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR3', 'MuMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{InclusiveSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('DiJetSR3', 'EE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{DiJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR1', 'EE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{InclusiveSR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR2', 'EE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{InclusiveSR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR3', 'EE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{InclusiveSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('DiJetSR3', 'EMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{e#mu}{DiJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR1', 'EMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{e#mu}{InclusiveSR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR2', 'EMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{e#mu}{InclusiveSR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR3', 'EMu', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{e#mu}{InclusiveSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('DiJetSR3', 'MuE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mue}{DiJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR1', 'MuE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mue}{InclusiveSR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR2', 'MuE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mue}{InclusiveSR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #m.RegionsToDraw.append( Region('InclusiveSR3', 'MuE', PN, 'Leptons', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mue}{InclusiveSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied') )
    #Region('OneJetSR3', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{OneJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('ZeroJetSR3', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZeroJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('OneJetSR3', 'EE', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{OneJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('ZeroJetSR3', 'EE', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{ZeroJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('InclusiveSR1', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{Incl. SR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('PassSR2', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),



  #m.PrintRegions()


#### Define Variables
m.VariablesToDraw = [
  #Variable('MuonCR', '', ''),
  #Variable('ElectronCR', '', ''),
  #Variable('ElectronMuonCR', '', ''),
  #Variable('MuonSR', '', ''),
  #Variable('ElectronSR', '', ''),
  #Variable('ElectronMuonSR', '', ''),
  #Variable('Lep_1_mva', 'MVA', ''),
  #Variable('Lep_2_mva', 'MVA', ''),
  #Variable('Lep_1_LFvsHF', 'LFvsHF', ''),
  #Variable('Lep_2_LFvsHF', 'LFvsHF', ''),
  Variable('Lep_1_pt', 'p_{T} of the leading lepton', 'GeV'),
  Variable('Lep_2_pt', 'p_{T} of the second lepton', 'GeV'),
  Variable('Lep_1_eta', '#eta of the leading lepton', ''),
  Variable('Lep_2_eta', '#eta of the second lepton', ''),
  #Variable('Leps_pt',  'p_{T} of all leptons', 'GeV'),
  #Variable('Lep_3_pt', 'p_{T} of the third lepton', 'GeV'),
  #Variable('Lep_4_pt', 'p_{T} of the fourth lepton', 'GeV'),
  #Variable('Lep_1_ptcone', 'p_{T}^{cone} of the leading lepton', 'GeV'),
  #Variable('Lep_2_ptcone', 'p_{T}^{cone} of the second lepton', 'GeV'),
  #Variable('Lep_3_ptcone', 'p_{T}^{cone} of the third lepton', 'GeV'),
  #Variable('Lep_4_ptcone', 'p_{T}^{cone} of the fourth lepton', 'GeV'),
  #Variable('Leps_eta',  '#eta of all leptons', ''),
  #Variable('Lep_3_eta', '#eta of the third lepton', ''),
  #Variable('Lep_4_eta', '#eta of the fourth lepton', ''),
  #Variable('DiJet_M_llW', 'M_{llW}', 'GeV'),
  #Variable('Jet_1_pt', 'p_{T} of the leading jet', 'GeV'),
  #Variable('Jet_2_pt', 'p_{T} of the second jet', 'GeV'),
  #Variable('Jet_1_eta', '#eta of the leading jet', 'GeV'),
  #Variable('Jet_2_eta', '#eta of the second jet', 'GeV'),
  #Variable('N_AK8Jets', 'N_{J}', ''),
  #Variable('N_bjetsM', 'N_{bj}', ''),
  #Variable('Lep_3_pt', 'm(ll)','GeV'),
  #Variable('NJets', 'N_{j}',''),
  #Variable('NBJets', 'N_{bj}',''),
  #Variable('nPV', 'N_{pv}',''),
  #Variable('PuppiMETType1XY', '#slash{E}_{T}^{miss} (GeV)', 'GeV'),
  #Variable('M_ll', 'M_{ll}', 'GeV'),
  #Variable('Ev_MET', 'MET', 'GeV'),
  #Variable('Ev_MET2_ST', 'MET^{2}/S_{T}', 'GeV'),
  #Variable('N_AK4J', 'N_{j}', ''),
  #Variable('N_Mu', 'N_{#mu}', ''),
  #Variable('N_El', 'N_{e}', ''),

]
m.PrintVariables()

#### Draw
m.DoSystCheck()

#m.DoCutFlow('NJets')
