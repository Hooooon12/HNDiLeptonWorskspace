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

parser = argparse.ArgumentParser(description='CR plot commands')
parser.add_argument('-c', dest='Category', type=int, default=0)
parser.add_argument('-y', dest='Year', type=int, default=0)
parser.add_argument('-e', dest='Era', type=str, default='NULL')
parser.add_argument('--debug',action='store_true')
parser.add_argument('--ScaleMC', action='store_true')
args = parser.parse_args()

#Analyser='HNL_SignalRegionPlotter'
Analyser='HNL_ControlRegionPlotter' #FIXME analyzer name
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

m.InputDirectory = '/data6/Users/jihkim/SKFlatOutput/'+dataset+"/"+Analyser+"/"+str_Era # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/Analyzer/Era. where the root itput files are stored.

m.DataDirectory = "DATA"
# typical root file name convention --> Analyzer_Skim_SampleName(_suffix).root
m.Filename_prefix = Analyser
m.Filename_suffix = ""
#m.Filename_skim = "_SkimTree_HNMultiLep" #
m.Filename_data_skim = "_SkimTree_HNMultiLepBDT" # use "" if no skim was used

m.OutputDirectoryLocal = ENV_PLOT_PATH+"/"+dataset+"/"+Analyser+"/"+str_Era # HNDiLeptonWorkspace/Output/Plots/Run2UltraLegacy_v3/Analyzer/Era. where the output plots are stored.
os.system('mkdir -p '+ m.OutputDirectoryLocal)
if args.ScaleMC:
  os.system('mkdir -p '+ m.OutputDirectoryLocal+'/ScaleMC/')
  

# check connection to lxplus is open
#check_lxplus_connection() #JH

#set username for lxplus
#m.Lxplus_User = GetFromConfig('LXPLUS_USER')
#m.Lxplus_Dir = GetFromConfig('LXPLUS_Dir')

#print m.Lxplus_User + " " + m.Lxplus_Dir
#exit()



if OutPutOnLxplus:
  m.OutputDirectory = m.Lxplus_Dir
  print "-"*40
  print("ssh "+m.Lxplus_User+"@lxplus.cern.ch 'mkdir -p " + m.OutputDirectory + "'")
  print "-"*40
  os.system("ssh "+m.Lxplus_User+"@lxplus.cern.ch 'mkdir -p " + m.OutputDirectory + "'")


#### Category
m.ScaleMC = args.ScaleMC

#### Systematic
tmp_Systematics = [
  #"Lumi",
  #"GetMCUncertainty",
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
  #"DYNorm",
  #"DYReshapeSyst",
  #"NonPromptNorm",
  #"OthersNorm",
  #"BTagSFHTag",
  #"BTagSFLTag",
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

if args.Category==0: # ?
  #### Define Samples
  if str_Era != 'YearCombined':
    #exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_WZ_%s, SampleGroup_ZZ_%s, SampleGroup_WpWp_%s, SampleGroup_WG_%s, SampleGroup_ZG_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    exec('m.SampleGroups = [SampleGroup_Fake_%s, SampleGroup_VV_%s, SampleGroup_Conv_%s, SampleGroup_WZ_EWK_%s]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SignalsToDraw = [SampleGroup_DY_%s_M100, SampleGroup_DY_%s_M1000, SampleGroup_VBF_%s_M1000, SampleGroup_SSWW_%s_M1000]'%(m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SignalsToDraw = [SampleGroup_DY_%s_M1000, SampleGroup_VBF_%s_M1000, SampleGroup_SSWW_%s_M1000]'%(m.DataEra, m.DataEra, m.DataEra))
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

  #PNs=["MVAUL_LFvsHF"] # parameter name (this is used in hist path)
  PNs=["MVAUL_HNTightV2","MVAUL_HNL_ULID_2017","MVAUL_LFvsHF_HNTightV2","MVAUL_LFvsHF_HNL_ULID_2017"] # parameter name (this is used in hist path)
  #PNs=["MVAUL_HNTightV2"] # parameter name (this is used in hist path)
  #### Define regions
  m.RegionsToDraw = [

    #Region('LimitInput', 'MuonSR', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{LimitInput}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('LimitInputBDT_M100', 'MuonSR', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{LimitInputBDT_M100}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('DiJetSR3', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{DiJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('OneJetSR3', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{OneJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('ZeroJetSR3', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZeroJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('OneJetSR3', 'EE', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{OneJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('ZeroJetSR3', 'EE', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{ee}{ZeroJetSR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('InclusiveSR1', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{Incl. SR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('PassSR2', 'MuMu', PNs[0], '', '', UnblindData=False, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    #Region('HNL_SSPresel_TwoLepton', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR3_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),
    #Region('HNL_SSVBFPresel_TwoLepton', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR3_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),
    #Region('HNL_WZ_ThreeLepton_CR', 'MuMuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu#mu}{WZ_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),
    #Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0], '_ConvMethodPt', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu#mu}{WG_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),
    #Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], '_ConvMethodPt', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu#mu}{ZG_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),
    #Region('HNL_HighMassSR3_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR3_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),
    #Region('HNL_HighMassBJet_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR3_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True),

  ]

  for PN in PNs:
    m.RegionsToDraw.append( Region('HNL_HighMassSR3_TwoLepton_CR', 'MuMu', PN, '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SR3_CR}', CutFlowCaption='', DrawData=True, DrawRatio=True) )

  m.PrintRegions()


#### Define Variables
m.VariablesToDraw = [
  #Variable('', 'Limit input', 'GeV'), #JH
  Variable('Lep_1_pt', 'p_{T} of the leading lepton', 'GeV'),
  Variable('Lep_2_pt', 'p_{T} of the second lepton', 'GeV'),
  #Variable('Lep_3_pt', 'p_{T} of the third lepton', 'GeV'),
  #Variable('Lep_4_pt', 'p_{T} of the fourth lepton', 'GeV'),
  Variable('Lep_1_eta', '#eta of the leading lepton', ''),
  Variable('Lep_2_eta', '#eta of the second lepton', ''),
  #Variable('Lep_3_eta', '#eta of the third lepton', 'GeV'),
  #Variable('Lep_4_eta', '#eta of the fourth lepton', 'GeV'),
  #Variable('Jet_1_pt', 'p_{T} of the leading jet', 'GeV'),
  #Variable('Jet_2_pt', 'p_{T} of the second jet', 'GeV'),
  #Variable('Jet_1_eta', '#eta of the leading jet', 'GeV'),
  #Variable('Jet_2_eta', '#eta of the second jet', 'GeV'),
  Variable('Ev_MET', 'MET', 'GeV'),
  #Variable('Ev_MET2_ST', 'MET^{2}/S_{T}', 'GeV'),
  Variable('N_AK4Jets', 'N_{j}', ''),
  #Variable('N_bjetsM', 'N_{bj}', ''),
  Variable('N_AK8Jets', 'N_{J}', ''),
  #Variable('Lep_3_pt', 'm(ll)','GeV'),
  #Variable('NJets', 'N_{j}',''),
  #Variable('NBJets', 'N_{bj}',''),
  #Variable('nPV', 'N_{pv}',''),
  #Variable('PuppiMETType1XY', '#slash{E}_{T}^{miss} (GeV)', 'GeV'),

]
m.PrintVariables()

#### Draw
m.Draw()
#m.DoSystCheck()
print (str(m.Filename_prefix))

#m.DoCutFlow('NJets')
