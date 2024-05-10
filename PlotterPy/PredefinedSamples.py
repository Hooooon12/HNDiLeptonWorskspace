import os,ROOT
from Plotter import SampleGroup

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/SNUHNTypeISeeSawDileptonRun2Legacy#Plot_Formatting

SampleGroup_TypeI_2017_M500 = SampleGroup( # For JA
  Name='TypeI',
  Type='Signal',
  Samples=['TypeI_M500_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kRed,
  Style=1,
  Width=2,
  Marker=20,
  TLatexAlias='Signal M500',
  LatexAlias='Signal M500',
  Scale=1
)

SampleGroup_TypeI_2017_M1000 = SampleGroup( # For JA
  Name='TypeI',
  Type='Signal',
  Samples=['TypeI_M1000_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange+8,
  Style=1,
  Width=2,
  Marker=21,
  TLatexAlias='Signal M1000',
  LatexAlias='Signal M1000',
  Scale=2.5
)

SampleGroup_TypeI_2017_M2000 = SampleGroup( # For JA
  Name='TypeI',
  Type='Signal',
  Samples=['TypeI_M2000_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue,
  Style=1,
  Width=2,
  Marker=22,
  TLatexAlias='Signal M2000',
  LatexAlias='Signal M2000',
  Scale=5
)

SampleGroup_SSWWTypeI_2017_M1000 = SampleGroup(
  Name='SSWWTypeI',
  Type='Signal',
  Samples=['SSWWTypeI_SF_M1000_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue,
  Style=1,
  Width=1,
  TLatexAlias='SSWW M1000',
  LatexAlias='SSWW M1000',
  Scale=10
)

SampleGroup_VBFTypeI_2017_M1000 = SampleGroup(
  Name='W#gamma',
  Type='Signal',
  Samples=['VBFTypeI_DF_M1000_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange,
  Style=1,
  Width=1,
  TLatexAlias='W#gamma M1000',
  LatexAlias='W#gamma M1000',
  Scale=1000
)

SampleGroup_DYTypeI_2017_M1000 = SampleGroup(
  Name='DYTypeI',
  Type='Signal',
  Samples=['DYTypeI_DF_M1000_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kRed,
  Style=1,
  Width=1,
  TLatexAlias='DY M1000',
  LatexAlias='DY M1000',
  Scale=1000
)

SampleGroup_DYTypeI_2017_M100 = SampleGroup(
  Name='DYTypeI',
  Type='Signal',
  Samples=['DYTypeI_DF_M100_private'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange,
  Style=3,
  TLatexAlias='DY M100',
  LatexAlias='DY M100',
  Scale=0.005
)

SampleGroup_Fake_2017 = SampleGroup(
  Name='Fake',
  Type=['Fake','Data'],
  Samples=['Fake'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_CF_2017 = SampleGroup(
  Name='CF',
  Type=['CF','Data'],
  Samples=['CF'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kYellow,
  Style=1,
  TLatexAlias='ChargeFlip',
  LatexAlias='ChargeFlip'
)

SampleGroup_WZ_2017 = SampleGroup(
  Name='WZ',
  Type='MC',
  Samples=['WZTo3LNu_amcatnlo'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen,
  Style=1,
  TLatexAlias='WZ',
  LatexAlias='WZ'
)

SampleGroup_ZZ_2017 = SampleGroup(
  Name='ZZ',
  Type='MC',
  Samples=['ZZTo4L_powheg'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kRed-7,
  Style=1,
  TLatexAlias='ZZ',
  LatexAlias='ZZ'
)

SampleGroup_WpWp_2017 = SampleGroup(
  Name='WpWp',
  Type='MC',
  Samples=['WpWp_EWK','WpWp_QCD'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kPink+6,
  Style=1,
  TLatexAlias='W#pmW#pm',
  LatexAlias='W#pmW#pm'
)

SampleGroup_WZ_EWK_2017 = SampleGroup(
  Name='WZ_EWK',
  Type='Prompt',
  Samples=['WZ_EWK'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen,
  Style=1,
  TLatexAlias='WZ_EWK',
  LatexAlias='WZ_EWK'
)

SampleGroup_ZG_2017 = SampleGroup(
  Name='ZG',
  Type='Conv',
  Samples=['ZGToLLG'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kViolet,
  Style=1,
  TLatexAlias='ZG',
  LatexAlias='ZG'
)

SampleGroup_WG_2017 = SampleGroup(
  Name='WG',
  Type='Conv',
  Samples=['WGToLNuG_MG'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange,
  Style=1,
  TLatexAlias='WG',
  LatexAlias='WG'
)

SampleGroup_Conv_2017 = SampleGroup(
  Name='Conv',
  Type='Conv',
  #Samples=['TG', 'TTG', 'WWG', 'WZG', 'WGJJToLNu', 'WGToLNuG_MG', 'ZGToLLG'],
  Samples=['Conv'], # Which one would be nicer?
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+3,
  Style=1,
  TLatexAlias='Conv',
  LatexAlias='Conv'
)

SampleGroup_MC_2017 = SampleGroup(
  Name='MC',
  Type='Prompt',
  Samples=['MC'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='MC',
  LatexAlias='MC'
)

SampleGroup_VV_Prompt_2017 = SampleGroup(
  Name='VV',
  Type='Prompt',
  Samples=['WZTo3LNu_amcatnlo', 'ZZTo4L_powheg'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='VV',
  LatexAlias='VV'
)

SampleGroup_Others_2017 = SampleGroup(
  Name='Others',
  Type='Prompt',
  Samples=['GluGluHToTauTau_M125','GluGluHToZZTo4L','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu','TTTT',
           'ttWToLNu','ttZToLLNuNu','tZq', #'ttWToQQ', 'ttZToQQ_ll' : no events
           'TTZZ','WWTo2L2Nu_DS','WWW','WWZ','WZZ','ZZZ'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange-3,
  Style=1,
  TLatexAlias='Others',
  LatexAlias='Others'
)

# OS2l CR

SampleGroup_FakeOS_2017 = SampleGroup(
  Name='Fake',
  Type='Fake',
  Samples=['Fake'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_DY_2017 = SampleGroup(
  Name='DY',
  Type='MC',
  Samples=['DYJets'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kYellow,
  Style=1,
  TLatexAlias='DY',
  LatexAlias='DY'
)

SampleGroup_DYtau_2017 = SampleGroup(
  Name='DYtau',
  Type='MC',
  Samples=['DYJets'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kOrange-3,
  Style=1,
  TLatexAlias='DYto#tau#tau',
  LatexAlias='DYto#tau#tau'
)

SampleGroup_WJets_MG_OS_2017 = SampleGroup(
  Name='WJets_MG',
  Type='MC',
  Samples=['WJets_MG'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kBlue,
  Style=1,
  TLatexAlias='WJets_MG',
  LatexAlias= 'WJets_MG'
)

SampleGroup_WG_OS_2017 = SampleGroup(
  Name='WG',
  Type='MC',
  Samples=['WGToLNuG'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kBlue-5,
  Style=1,
  TLatexAlias='W#gamma',
  LatexAlias= 'W#gamma'
)

SampleGroup_ZG_OS_2017 = SampleGroup(
  Name='ZG',
  Type='MC',
  Samples=['ZGToLLG'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kBlue+4,
  Style=1,
  TLatexAlias='Z#gamma',
  LatexAlias= 'Z#gamma'
)

SampleGroup_TTLL_2017 = SampleGroup(
  Name='TTLL',
  Type='MC',
  Samples=['TTLL_powheg'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kRed,
  Style=1,
  TLatexAlias='TTLL',
  LatexAlias='TTLL'
)

SampleGroup_VV_pythia_OS_2017 = SampleGroup(
  Name='VV',
  Type='MC',
  Samples=['WW_pythia','WZ_pythia','ZZ_pythia'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='VV',
  LatexAlias='VV'
)

SampleGroup_VV_OS_2017 = SampleGroup(
  Name='VV',
  Type='MC',
  Samples=['WWTo2L2Nu_powheg','WZ_pythia','ZZ_pythia'],
  Era = "2017",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='VV',
  LatexAlias='VV'
)

#SampleGroup_SingleTop_2017 = SampleGroup(
#  Name='SingleTop',
#  Type='MC',
#  Samples=['SingleTop_sch_Lep','SingleTop_tch_antitop_Incl','SingleTop_tch_top_Incl', 'SingleTop_tW_antitop_NoFullyHad', 'SingleTop_tW_top_NoFullyHad'],
#  Era = "2017",
#  Skim='',
#  Color=ROOT.kViolet+1,
#  Style=1,
#  TLatexAlias='SingleTop',
#  LatexAlias='SingleTop'
#)

SampleGroup_tW_2017 = SampleGroup(
  Name='tW',
  Type='MC',
  Samples=['SingleTop_tW_antitop_NoFullyHad', 'SingleTop_tW_top_NoFullyHad'],
  Era = "2017",
  Skim='',
  Color=ROOT.kViolet+1,
  Style=1,
  TLatexAlias='tW',
  LatexAlias= 'tW'
)


SampleGroup_Conv_2017 = SampleGroup(
  Name='Conv',
  Type='Conv',
  Samples=['TG', 'TTG', 'WWG', 'WZG', 'WGJJToLNu', 'WGToLNuG_MG', 'ZGToLLG', 'DYJets_MG'],
  #Samples=['Conv'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+3,
  Style=1,
  TLatexAlias='Conv',
  LatexAlias='Conv'
)

#SampleGroup_DYJets_MG_2017 = SampleGroup( # merged into the Conv
#  Name='DYJets_MG',
#  Type='Conv',
#  Samples=['DYJets_MG'],
#  Era = "2017",
#  Skim='_SkimTree_HNMultiLepBDT',
#  Color=ROOT.kBlue,
#  Style=1,
#  TLatexAlias='DYJets_MG',
#  LatexAlias= 'DYJets_MG'
#)

SampleGroup_VV_2017 = SampleGroup(
  Name='VV',
  Type='Prompt',
  Samples=['WZTo3LNu_amcatnlo','ZZTo4L_powheg'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='VV',
  LatexAlias='VV'
)

SampleGroup_VVV_2017 = SampleGroup(
  Name='VVV',
  Type='Prompt',
  Samples=['WWW','WWZ','WZZ','ZZZ'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+2,
  Style=1,
  TLatexAlias='VVV',
  LatexAlias='VVV'
)

SampleGroup_SingleTop_2017 = SampleGroup(
  Name='SingleTop',
  Type='Prompt',
  Samples=['SingleTop_sch_Lep','SingleTop_tch_antitop_Incl','SingleTop_tch_top_Incl','SingleTop_tW_antitop_NoFullyHad','SingleTop_tW_top_NoFullyHad'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kTeal+6,
  Style=1,
  TLatexAlias='SingleTop',
  LatexAlias='SingleTop'
)

SampleGroup_ttV_2017 = SampleGroup(
  Name='ttV',
  Type='Prompt',
  Samples=['ttWToLNu','ttZToLLNuNu'], #'ttWToQQ', 'ttZToQQ_ll' : no entries
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kAzure+7,
  Style=1,
  TLatexAlias='ttV',
  LatexAlias='ttV'
)

SampleGroup_TTXX_2017 = SampleGroup(
  Name='TTXX',
  Type='Prompt',
  Samples=['TTTT','TTZZ'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kViolet,
  Style=1,
  TLatexAlias='TTXX',
  LatexAlias='TTXX'
)

SampleGroup_tZq_2017 = SampleGroup(
  Name='tZq',
  Type='Prompt',
  Samples=['tZq'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kPink+6,
  Style=1,
  TLatexAlias='tZq',
  LatexAlias='tZq'
)

SampleGroup_Higgs_2017 = SampleGroup(
  Name='Higgs',
  Type='Prompt',
  Samples=['ttHToNonbb','tHq','VHToNonbb'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue,
  Style=1,
  TLatexAlias='Higgs',
  LatexAlias='Higgs'
)

SampleGroup_VBFHiggs_2017 = SampleGroup(
  Name='VBFHiggs',
  Type='Prompt',
  Samples=['VBFHToWWTo2L2Nu','VBF_HToZZTo4L'], #VBFHToTauTau_M125 : no events
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue-6,
  Style=1,
  TLatexAlias='VBFHiggs',
  LatexAlias='VBFHiggs'
)

SampleGroup_WW_2017 = SampleGroup(
  Name='WW',
  Type='Prompt',
  Samples=['WpWp_EWK','WpWp_QCD','WWTo2L2Nu_DS','WWTo2L2Nu_powheg'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kPink-8,
  Style=1,
  TLatexAlias='WW',
  LatexAlias='WW'
)

SampleGroup_WZ_EWK_2017 = SampleGroup(
  Name='WZ_EWK',
  Type='Prompt',
  Samples=['WZ_EWK'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange+8,
  Style=1,
  TLatexAlias='WZ_EWK',
  LatexAlias='WZ_EWK'
)

SampleGroup_ggH_2017 = SampleGroup(
  Name='ggH',
  Type='Prompt',
  Samples=['GluGluHToTauTau_M125','GluGluHToWWTo2L2Nu','GluGluHToZZTo4L'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kSpring+8,
  Style=1,
  TLatexAlias='ggH',
  LatexAlias='ggH'
)

SampleGroup_ggZZ_2017 = SampleGroup(
  Name='ggZZ',
  Type='Prompt',
  Samples=['GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
  Era = "2017",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kCyan,
  Style=1,
  TLatexAlias='ggZZ',
  LatexAlias='ggZZ'
)




####################### 2018 ##############################

SampleGroup_Fake_2018 = SampleGroup(
  Name='Fake',
  Type=['Fake','Data'],
  Samples=['Fake'],
  Era = "2018",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_CF_2018 = SampleGroup(
  Name='CF',
  Type=['CF','Data'],
  Samples=['CF'],
  Era = "2018",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kYellow,
  Style=1,
  TLatexAlias='ChargeFlip',
  LatexAlias='ChargeFlip'
)

SampleGroup_Conv_2018 = SampleGroup(
  Name='Conv',
  Type='Conv',
  #Samples=['TG', 'TTG', 'WWG', 'WZG', 'WGJJToLNu', 'WGToLNuG_MG', 'ZGToLLG'],
  Samples=['Conv'],
  Era = "2018",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+3,
  Style=1,
  TLatexAlias='Conv',
  LatexAlias='Conv'
)

SampleGroup_DYJets_MG_2018 = SampleGroup(
  Name='DYJets_MG',
  Type='Conv',
  Samples=['DYJets_MG'],
  Era = "2018",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue,
  Style=1,
  TLatexAlias='DYJets_MG',
  LatexAlias= 'DYJets_MG'
)

SampleGroup_MC_2018 = SampleGroup(
  Name='MC',
  Type='Prompt',
  Samples=['MC'],
  Era = "2018",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='MC',
  LatexAlias='MC'
)

####################### 2016a ##############################

SampleGroup_Fake_2016preVFP = SampleGroup(
  Name='Fake',
  Type=['Fake','Data'],
  Samples=['Fake'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_CF_2016preVFP = SampleGroup(
  Name='CF',
  Type=['CF','Data'],
  Samples=['CF'],
  Era = "2016preVFP",
  Skim='_SkimTree_DileptonBDT',
  Color=ROOT.kYellow,
  Style=1,
  TLatexAlias='ChargeFlip',
  LatexAlias='ChargeFlip'
)

SampleGroup_Conv_2016preVFP = SampleGroup(
  Name='Conv',
  Type='Conv',
  #Samples=['TG', 'TTG', 'WWG', 'WZG', 'WGJJToLNu', 'WGToLNuG_MG', 'ZGToLLG'],
  Samples=['Conv'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+3,
  Style=1,
  TLatexAlias='Conv',
  LatexAlias='Conv'
)

SampleGroup_DYJets_MG_2016preVFP = SampleGroup(
  Name='DYJets_MG',
  Type='Conv',
  Samples=['DYJets_MG'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue,
  Style=1,
  TLatexAlias='DYJets_MG',
  LatexAlias= 'DYJets_MG'
)

SampleGroup_MC_2016preVFP = SampleGroup(
  Name='MC',
  Type='Prompt',
  Samples=['MC'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='MC',
  LatexAlias='MC'
)

SampleGroup_VV_2016preVFP = SampleGroup(
  Name='VV',
  Type='Prompt',
  Samples=['WZTo3LNu_amcatnlo','ZZTo4L_powheg'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='VV',
  LatexAlias='VV'
)

SampleGroup_VVV_2016preVFP = SampleGroup(
  Name='VVV',
  Type='Prompt',
  Samples=['WWW','WWZ','WZZ','ZZZ'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kGreen+2,
  Style=1,
  TLatexAlias='VVV',
  LatexAlias='VVV'
)

SampleGroup_SingleTop_2016preVFP = SampleGroup(
  Name='SingleTop',
  Type='Prompt',
  Samples=['SingleTop_sch_Lep','SingleTop_tch_antitop_Incl','SingleTop_tch_top_Incl','SingleTop_tW_antitop_NoFullyHad','SingleTop_tW_top_NoFullyHad'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kTeal+6,
  Style=1,
  TLatexAlias='SingleTop',
  LatexAlias='SingleTop'
)

SampleGroup_ttV_2016preVFP = SampleGroup(
  Name='ttV',
  Type='Prompt',
  Samples=['ttWToLNu','ttZToLLNuNu'], #'ttWToQQ', 'ttZToQQ_ll' : no entries
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kAzure+7,
  Style=1,
  TLatexAlias='ttV',
  LatexAlias='ttV'
)

SampleGroup_TTXX_2016preVFP = SampleGroup(
  Name='TTXX',
  Type='Prompt',
  Samples=['TTTT','TTZZ'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kViolet,
  Style=1,
  TLatexAlias='TTXX',
  LatexAlias='TTXX'
)

SampleGroup_tZq_2016preVFP = SampleGroup(
  Name='tZq',
  Type='Prompt',
  Samples=['tZq'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kPink+6,
  Style=1,
  TLatexAlias='tZq',
  LatexAlias='tZq'
)

SampleGroup_Higgs_2016preVFP = SampleGroup(
  Name='Higgs',
  Type='Prompt',
  Samples=['ttHToNonbb','tHq','VHToNonbb'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue,
  Style=1,
  TLatexAlias='Higgs',
  LatexAlias='Higgs'
)

SampleGroup_VBFHiggs_2016preVFP = SampleGroup(
  Name='VBFHiggs',
  Type='Prompt',
  Samples=['VBFHToWWTo2L2Nu','VBF_HToZZTo4L'], #VBFHToTauTau_M125 : no events
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kBlue-6,
  Style=1,
  TLatexAlias='VBFHiggs',
  LatexAlias='VBFHiggs'
)

SampleGroup_WW_2016preVFP = SampleGroup(
  Name='WW',
  Type='Prompt',
  Samples=['WpWp_EWK','WpWp_QCD','WWTo2L2Nu_DS','WWTo2L2Nu_powheg'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kPink-8,
  Style=1,
  TLatexAlias='WW',
  LatexAlias='WW'
)

SampleGroup_WZ_EWK_2016preVFP = SampleGroup(
  Name='WZ_EWK',
  Type='Prompt',
  Samples=['WZ_EWK'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kOrange+8,
  Style=1,
  TLatexAlias='WZ_EWK',
  LatexAlias='WZ_EWK'
)

SampleGroup_ggH_2016preVFP = SampleGroup(
  Name='ggH',
  Type='Prompt',
  Samples=['GluGluHToTauTau_M125','GluGluHToWWTo2L2Nu','GluGluHToZZTo4L'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kSpring+8,
  Style=1,
  TLatexAlias='ggH',
  LatexAlias='ggH'
)

SampleGroup_ggZZ_2016preVFP = SampleGroup(
  Name='ggZZ',
  Type='Prompt',
  Samples=['GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
  Era = "2016preVFP",
  Skim='_SkimTree_HNMultiLepBDT',
  Color=ROOT.kCyan,
  Style=1,
  TLatexAlias='ggZZ',
  LatexAlias='ggZZ'
)

