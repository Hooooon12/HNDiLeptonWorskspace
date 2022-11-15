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

Analyser='HNL_ControlRegionPlotter'
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


m.InputDirectory = WORKING_DIR+'/InputFiles/MergedFiles/'+dataset+"/"+Analyser+"/"

str_Era=m.DataEra

m.DataDirectory = str_Era
m.Filename_prefix = Analyser
m.Filename_suffix = ""
m.Filename_skim = "_SkimTree_HNMultiLep"
m.Filename_data_skim = "_SkimTree_HNMultiLep"

m.OutputDirectoryLocal = ENV_PLOT_PATH+"/"+dataset+"/"+Analyser+"/"+str_Era+"/"
os.system('mkdir -p '+ m.OutputDirectoryLocal)
if args.ScaleMC:
  os.system('mkdir -p '+ m.OutputDirectoryLocal+'/ScaleMC/')
  

# check connection to lxplus is open
#check_lxplus_connection() #JH

#set username for lxplus
m.Lxplus_User = GetFromConfig('LXPLUS_USER')
m.Lxplus_Dir = GetFromConfig('LXPLUS_Dir')

print m.Lxplus_User + " " + m.Lxplus_Dir
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
  #"MuonRecoSF",
  #"MuonEn",
  #"MuonIDSF",
  #"MuonISOSF",
  #"MuonTriggerSF",
  #"ElectronRecoSF",
  #"ElectronRes",
  #"ElectronEn",
  #"ElectronIDSF",
  #"ElectronTriggerSF",
  #"PU",
  #"Prefire",
  #"DYNorm",
  #"DYReshapeSyst",
  #"NonPromptNorm",
  #"OthersNorm",
  #"BTag",
]

m.Systematics = [ Systematic(Name="Central", Direction=0, Year=-1) ]
for s in tmp_Systematics:
  isCorr = IsCorrelated(s)
  if isCorr:
    m.Systematics.append( Systematic(Name=s, Direction=+1, Year=-1) )
    m.Systematics.append( Systematic(Name=s, Direction=-1, Year=-1) )
  else:
    if args.Year>0:
      m.Systematics.append( Systematic(Name=s, Direction=+1, Year=args.Year) )
      m.Systematics.append( Systematic(Name=s, Direction=-1, Year=args.Year) )
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
else:
  
  m.SetBinningFilepath(
    WORKING_DIR+'/data/'+dataset+'/'+str_Era+'/CR_rebins.txt',
    WORKING_DIR+'/data/'+dataset+'/'+str_Era+'/CR_xaxis.txt',
    WORKING_DIR+'/data/'+dataset+'/'+str_Era+'/CR_yaxis.txt',
  )


#### Predef samples
from PredefinedSamples import *

###############
#### WZ CR ####
###############

if args.Category==0:
  #### Define Samples
  if str_Era != 'YearCombined':
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_DY_%s, SampleGroup_TTLL_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra))
    exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_WZJJ_%s, SampleGroup_WGJJ_%s, SampleGroup_WpWp_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
#############Conversion variation#############
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_DYonly_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_WZJJ_%s, SampleGroup_WGJJ_%s, SampleGroup_WpWp_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_MG_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_WZJJ_%s, SampleGroup_WGJJ_%s, SampleGroup_WpWp_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_amcatnlo_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_WZJJ_%s, SampleGroup_WGJJ_%s, SampleGroup_WpWp_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_Sherpa_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_WZJJ_%s, SampleGroup_WGJJ_%s, SampleGroup_WpWp_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
    #exec('m.SampleGroups = [SampleGroup_NonPrompt_%s,SampleGroup_Conv_HT_%s, SampleGroup_CF_%s, SampleGroup_XG_%s, SampleGroup_WZJJ_%s, SampleGroup_WGJJ_%s, SampleGroup_WpWp_%s, SampleGroup_VV_%s,  SampleGroup_VVV_%s , SampleGroup_Other_%s  ]'%(m.DataEra,m.DataEra, m.DataEra, m.DataEra,m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra, m.DataEra))
##############################################
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

  PNs=["POGCR_UL"] #JH
  PNs=["HNL_UL"] #JH
  HistTags=["","_ConvMethodPt","_ConvMethodBackup"] #JH
  OutputTags=["_DYonly","_MG","_amcatnlo","_Sherpa","_HT"] #JH
  #### Define regions
  if SampleGroup_Conv_DYonly_2017 in m.SampleGroups:
    m.RegionsToDraw = [
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[0], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[0], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[1], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[1], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[2], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[2], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], OutputTags[0], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    ]
  elif SampleGroup_Conv_MG_2017 in m.SampleGroups:
    m.RegionsToDraw = [
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[0], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[0], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[1], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[1], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[2], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[2], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], OutputTags[1], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    ]
  elif SampleGroup_Conv_amcatnlo_2017 in m.SampleGroups:
    m.RegionsToDraw = [
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[0], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[0], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[1], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[1], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[2], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[2], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], OutputTags[2], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    ]
  elif SampleGroup_Conv_Sherpa_2017 in m.SampleGroups:
    m.RegionsToDraw = [
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[0], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[0], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[1], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[1], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[2], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[2], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], OutputTags[3], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    ]
  elif SampleGroup_Conv_HT_2017 in m.SampleGroups:
    m.RegionsToDraw = [
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[0], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[0], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[1], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[1], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0],HistTags[2], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0],HistTags[2], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], OutputTags[4], UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
    ]
  else:
	  m.RegionsToDraw = [

      #Region('HNL_WZ_ThreeLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WZ CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZ_ThreeLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WZ CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZ_ThreeLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WZ CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_ZZ_FourLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZZ CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_ZZ_FourLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZZ CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_ZZ_FourLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZZ CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_SSPresel_TwoLepton', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SSPresel}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_SSPresel_TwoLepton', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{SSPresel}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_SSPresel_TwoLepton', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{SSPresel}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_SSVBFPresel_TwoLepton', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{SSVBFPresel}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_SSVBFPresel_TwoLepton', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{SSVBFPresel}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_SSVBFPresel_TwoLepton', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{SSVBFPresel}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassSR1_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{HighMassCR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassSR1_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{HighMassCR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassSR1_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{HighMassCR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassSR3_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{HighMassCR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassSR3_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{HighMassCR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassSR3_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{HighMassCR3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassNP_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{NonPromptCR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassNP_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{NonPromptCR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassNP_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{NonPromptCR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassBJet_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{NonPromptCR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassBJet_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{NonPromptCR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassBJet_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{NonPromptCR1}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassCR2_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{HighMassCR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassCR2_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{HighMassCR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_HighMassCR2_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{HighMassCR2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWp_TwoLepton_CR1', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WWCR #Delta#phi_{ll} < 2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWp_TwoLepton_CR1', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WWCR #Delta#phi_{ll} < 2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWp_TwoLepton_CR1', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WWCR #Delta#phi_{ll} < 2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWp_TwoLepton_CR2', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WWCR #slash{E}_{T}^{miss} > 30 GeV}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWp_TwoLepton_CR2', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WWCR #slash{E}_{T}^{miss} > 30 GeV}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWp_TwoLepton_CR2', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WWCR #slash{E}_{T}^{miss} > 30 GeV}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WWCRNP}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WWCRNP}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WWCRNP}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP2_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WWCRNP2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP2_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WWCRNP2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP2_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WWCRNP2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP3_TwoLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WWCRNP3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP3_TwoLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WWCRNP3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WpWpNP3_TwoLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WWCRNP3}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZ2_ThreeLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WZ2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZ2_ThreeLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WZ2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZ2_ThreeLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WZ2}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZB_ThreeLepton_CR', 'MuMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WZB}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZB_ThreeLepton_CR', 'EMu', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WZB}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      #Region('HNL_WZB_ThreeLepton_CR', 'EE', PNs[0], '', '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WZB}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),

      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[0], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[0], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[0], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[1], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[1], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[1], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_ZG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{ZG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'MuMu', PNs[0], HistTags[2], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{#mu#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EMu', PNs[0], HistTags[2], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{e#mu}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),
      Region('HNL_WG_ThreeLepton_CR', 'EE', PNs[0], HistTags[2], '', UnblindData=True, Logy=0, TLatexAlias='#splitline{ee}{WG CR}', CutFlowCaption='Number of Events in Zmass Window (SingleMuon Trigger). Truth matching applied' ),

    ]

  m.PrintRegions()


#### Define Variables
m.VariablesToDraw = [
  Variable('Lep_1_pt', 'p_{T} of the leading lepton', 'GeV'), #JH
  Variable('Lep_2_pt', 'p_{T} of the second lepton', 'GeV'),
  Variable('Lep_3_pt', 'p_{T} of the third lepton', 'GeV'),
  Variable('Lep_4_pt', 'p_{T} of the fourth lepton', 'GeV'),
  Variable('Lep_1_eta', '#eta of the leading lepton', 'GeV'),
  Variable('Lep_2_eta', '#eta of the second lepton', 'GeV'),
  Variable('Lep_3_eta', '#eta of the third lepton', 'GeV'),
  Variable('Lep_4_eta', '#eta of the fourth lepton', 'GeV'),
  #Variable('N_AK4Jets', 'N_{j}', ''),
  #Variable('N_bjetsM', 'N_{bj}', ''),
  #Variable('N_AK8Jets', 'N_{J}', ''),
  #Variable('Lep_3_pt', 'm(ll)','GeV'),
  #Variable('NJets', 'N_{j}',''),
  #Variable('NBJets', 'N_{bj}',''),
  #Variable('nPV', 'N_{pv}',''),
  #Variable('PuppiMETType1XY', '#slash{E}_{T}^{miss} (GeV)', 'GeV'),

]
m.PrintVariables()

#### Draw
m.Draw()
print (str(m.Filename_prefix))

#m.DoCutFlow('NJets')
