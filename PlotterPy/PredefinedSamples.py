import os,ROOT
from Plotter import SampleGroup

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/SNUHNTypeISeeSawDileptonRun2Legacy#Plot_Formatting

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
  Samples=['TG', 'TTG', 'WWG', 'WZG', 'WGJJToLNu', 'WGToLNuG_MG', 'ZGToLLG'],
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

SampleGroup_VV_2017 = SampleGroup(
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
           'ttWToLNu','ttWToQQ','ttZToLLNuNu','ttZToQQ_ll','tZq',
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
  Skim='_SkimTree_Dilepton',
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
  Skim='_SkimTree_Dilepton',
  Color=ROOT.kYellow,
  Style=1,
  TLatexAlias='DY',
  LatexAlias='DY'
)

SampleGroup_TTLL_2017 = SampleGroup(
  Name='TTLL',
  Type='MC',
  Samples=['TTLL_powheg'],
  Era = "2017",
  Skim='_SkimTree_Dilepton',
  Color=ROOT.kRed,
  Style=1,
  TLatexAlias='TTLL',
  LatexAlias='TTLL'
)

SampleGroup_VV_pythia_2017 = SampleGroup(
  Name='VV',
  Type='MC',
  Samples=['WW_pythia','WZ_pythia','ZZ_pythia'],
  Era = "2017",
  Skim='_SkimTree_Dilepton',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='VV',
  LatexAlias='VV'
)

