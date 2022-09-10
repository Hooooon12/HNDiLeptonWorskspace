import os,ROOT
from Plotter import SampleGroup

#VV_incl", "DY","Xgamma", "VVV", "top", "WW_double","ttbar"

SampleGroup_Conv_2018 =  SampleGroup(
    Name='Conv',
    Type='Bkgd',
    Samples=['Conv'],
    Era = "2018",
    Color=74,
    Style=1,
    TLatexAlias='Conv.',
    LatexAlias='Conv.'
)

SampleGroup_CF_2016preVFP =  SampleGroup(
    Name='CF',
    Type='Bkgd',
    Samples=['CF'],
    Era = "2016preVFP",
    Color=74,
    Style=1,
    TLatexAlias='Charge MisID.',
    LatexAlias='Charge MisID.'
)

SampleGroup_CF_2017 =  SampleGroup(
    Name='CF',
    Type='Bkgd',
    Samples=['CF'],
    Era = "2017",
    Color=74,
    Style=1,
    TLatexAlias='Charge MisID.',
    LatexAlias='Charge MisID.'
)

SampleGroup_CF_2018 =  SampleGroup(
    Name='CF',
    Type='Bkgd',
    Samples=['CF'],
    Era = "2018",
    Color=64,
    Style=1,
    TLatexAlias='Charge MisID.',
    LatexAlias='Charge MisID.'
)


## TT+X

SampleGroup_Top_2016preVFP = SampleGroup(
    Name='Top',
    Type='Bkgd',
    Samples=['TTLL_powheg','ttWToLNu','ttWToQQ','ttZToLLNuNu','ttZToQQ'],
    Era = "2016preVFP",
    Color=ROOT.kRed,
    Style=1,
    TLatexAlias='t#bar{t}[powheg]',
    LatexAlias='$\\mathrm{t}\\bar{\\mathrm{t}}$[powheg]'
)

SampleGroup_Top_2017 = SampleGroup(
    Name='Top',
    Type='Bkgd',
    Samples=['TTLL_powheg','ttWToLNu','ttWToQQ','ttZToLLNuNu','ttZToQQ'],    
    Era = "2017",
    Color=ROOT.kRed,
    Style=1,
    TLatexAlias='t#bar{t}[powheg]',
    LatexAlias='$\\mathrm{t}\\bar{\\mathrm{t}}$[powheg]'
       
)

SampleGroup_Top_2018 = SampleGroup(
    Name='Top',
    Type='Bkgd',
    Samples=['TTLL_powheg','ttWToLNu','ttWToQQ','ttZToLLNuNu','ttZToQQ'],    
    Era = "2018",
    Color=ROOT.kRed,
    Style=1,
    TLatexAlias='t#bar{t}[powheg]',
    LatexAlias='$\\mathrm{t}\\bar{\\mathrm{t}}$[powheg]'
)

#VVV

SampleGroup_VVV_2016preVFP = SampleGroup(
    Name='VVV',
    Type='Bkgd',
    Samples=['WWW', 'WWZ', 'WZZ', 'ZZZ'],
    Era = "2016preVFP",
    Color=ROOT.kSpring+10,
    Style=1,
    TLatexAlias='VVV',
    LatexAlias='VVV'
)

SampleGroup_VVV_2017 = SampleGroup(
    Name='VVV',
    Type='Bkgd',
    Samples=['WWW', 'WWZ', 'WZZ', 'ZZZ'],
    Era = "2017",
    Color=ROOT.kSpring+10,
    Style=1,
    TLatexAlias='VVV',
    LatexAlias='VVV'
)

SampleGroup_VVV_2018 = SampleGroup(
    Name='VVV',
    Type='Bkgd',
    Samples=['WWW', 'WWZ', 'WZZ', 'ZZZ'],
    Era = "2018",
    Color=ROOT.kSpring+10,
    Style=1,
    TLatexAlias='VVV',
    LatexAlias='VVV'
)


#Xgamma
SampleGroup_XG_2016preVFP = SampleGroup(
    Name='XG',
    Type='Bkgd',
    Samples=['ZGTo2LG_01J', 'WGToLNuG'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-7,
    Style=1,
    TLatexAlias='X+#gamma',
    LatexAlias='X+$\\gamma$'
)

SampleGroup_XG_2017 = SampleGroup(
    Name='XG',
    Type='Bkgd',
    Samples=['ZGTo2LG_01J', 'WGToLNuG'],
    Era = "2017",
    Color=ROOT.kSpring-7,
    Style=1,
    TLatexAlias='X+#gamma',
    LatexAlias='X+$\\gamma$'

)

SampleGroup_XG_2018 = SampleGroup(
    Name='XG',
    Type='Bkgd',
    Samples=['ZGToLLG', 'WGToLNuG'], #JH
    Era = "2018",
    Color=ROOT.kSpring-7,
    Style=1,
    TLatexAlias='X+#gamma',
    LatexAlias='X+$\\gamma$'
)

SampleGroup_ZG_2016preVFP = SampleGroup(
    Name='XG',
    Type='Bkgd',
    Samples=['ZGTo2LG_01J'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-7,
    Style=1,
    TLatexAlias='Z+#gamma',
    LatexAlias='Z+$\\gamma$'
)

SampleGroup_ZG_2017 = SampleGroup(
    Name='ZG',
    Type='Bkgd',
    Samples=['ZGTo2LG_01J'],
    Era = "2017",
    Color=ROOT.kSpring-7,
    Style=1,
    TLatexAlias='Z+#gamma',
    LatexAlias='Z+$\\gamma$'
)

SampleGroup_ZG_2018 = SampleGroup(
    Name='ZG',
    Type='Bkgd',
    Samples=['ZGTo2LG_01J'],
    Era = "2018",
    Color=ROOT.kSpring-7,
    Style=1,
    TLatexAlias='Z+#gamma',
    LatexAlias='Z+$\\gamma$'
)


SampleGroup_WG_2016preVFP = SampleGroup(
    Name='WG',
    Type='Bkgd',
    Samples=['WGToLNuG'],
    Era = "2016preVFP",
    Color=ROOT.kGreen-7,
    Style=1,
    TLatexAlias='W+#gamma',
    LatexAlias='W+$\\gamma$'
)

SampleGroup_WG_2017 = SampleGroup(
    Name='WG',
    Type='Bkgd',
    Samples=['WGToLNuG'],
    Era = "2017",
    Color=ROOT.kGreen-7,
    Style=1,
    TLatexAlias='W+#gamma',
    LatexAlias='W+$\\gamma$'
    
)

SampleGroup_WG_2018 = SampleGroup(
    Name='WG',
    Type='Bkgd',
    Samples=['WGToLNuG'],
    Era = "2018",
    Color=ROOT.kGreen-7,
    Style=1,
    TLatexAlias='W+#gamma',
    LatexAlias='W+$\\gamma$'

)

## VV

SampleGroup_VV_incl_2016preVFP = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZ_pythia', 'ZZ_pythia', 'WW_pythia'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Pythia]',
    LatexAlias='VV[Pythia]'
)

SampleGroup_VV_incl_2016postVFP = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZ_pythia', 'ZZ_pythia', 'WW_pythia'],
    Era = "2016postVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Pythia]',
    LatexAlias='VV[Pythia]'
)

SampleGroup_VV_incl_2017 = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZ_pythia', 'ZZ_pythia', 'WW_pythia'],
    Era = "2017",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Pythia]',
    LatexAlias='VV[Pythia]'
)
SampleGroup_VV_incl_2018 = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZ_pythia', 'ZZ_pythia', 'WW_pythia'],
    Era = "2018",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Pythia]',
    LatexAlias='VV[Pythia]'
)

## VV                                                                                                                                                                  

SampleGroup_WZ_powheg_2016preVFP = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_mllmin4p0_powheg'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Powheg] m > 4 GeV',
    LatexAlias='WZ[Powheg] m > 4 GeV'
)

SampleGroup_WZ_pythia_2016preVFP = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZ_pythia'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Pythia]',
    LatexAlias='WZ[Pythia]'
)
SampleGroup_WZ_mcatnlo_2016preVFP = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[amc@nlo]',
    LatexAlias='WZ[amc@nlo]'
)
SampleGroup_ZZ_powheg_2016preVFP = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_m_1toInf_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],

    Era = "2016preVFP",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg]',
    LatexAlias='ZZ[powheg]',
)

SampleGroup_ZZ_powheg_m1toInf_2016preVFP = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_m_1toInf_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2016preVFP",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg] m > 1 GeV',
    LatexAlias='ZZ[powheg] m > 1 GeV',
)


SampleGroup_WZ_powheg_2016postVFP = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_mllmin4p0_powheg'],
    Era = "2016postVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Powheg] m > 4 GeV',
    LatexAlias='WZ[Powheg] m > 4 GeV'
)

SampleGroup_WZ_pythia_2016postVFP = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZ_pythia'],
    Era = "2016postVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Pythia]',
    LatexAlias='WZ[Pythia]'
)
SampleGroup_WZ_mcatnlo_2016postVFP = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo'],
    Era = "2016postVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[amc@nlo]',
    LatexAlias='WZ[amc@nlo]'
)
SampleGroup_ZZ_powheg_2016postVFP = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_m_1toInf_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],

    Era = "2016postVFP",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg]',
    LatexAlias='ZZ[powheg]',
)

SampleGroup_ZZ_powheg_m1toInf_2016postVFP = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_m_1toInf_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2016postVFP",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg] m > 1 GeV',
    LatexAlias='ZZ[powheg] m > 1 GeV',
)

SampleGroup_WZ_powheg_2017 = SampleGroup(
  Name='WZ',
  Type='Bkgd',
    Samples=['WZTo3LNu_mllmin4p0_powheg'],
  Era = "2017",
  Color=ROOT.kSpring-1,
  Style=1,
  TLatexAlias='WZ[Powheg] m > 4 GeV',
  LatexAlias='WZ[Powheg] m > 4 GeV'
)
SampleGroup_WZ_pythia_2017 = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZ_pythia'],
    Era = "2017",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Pythia]',
    LatexAlias='WZ[Pythia]'
)
SampleGroup_WZ_mcatnlo_2017 = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo'],
    Era = "2017",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[amc@nlo]',
    LatexAlias='WZ[amc@nlo]'
)
SampleGroup_ZZ_powheg_2017 = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],

    Era = "2017",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg]',
    LatexAlias='ZZ[powheg]',
)

SampleGroup_ZZ_powheg_m1toInf_2017 = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_m_1toInf_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2017",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg] m > 1 GeV',
    LatexAlias='ZZ[powheg] m > 1 GeV',
)

SampleGroup_WZ_powheg_2018 = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_mllmin4p0_powheg'],
    Era = "2018",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Powheg] m > 4 GeV',
    LatexAlias='WZ[Powheg] m > 4 GeV'
)
SampleGroup_WZ_pythia_2018 = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZ_pythia'],
    Era = "2018",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[Pythia]',
    LatexAlias='WZ[Pythia]'
)
SampleGroup_WZ_mcatnlo_2018 = SampleGroup(
    Name='WZ',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo'],
    Era = "2018",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='WZ[amc@nlo]',
    LatexAlias='WZ[amc@nlo]'
)
SampleGroup_ZZ_powheg_2018 = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],

    Era = "2018",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg]',
    LatexAlias='ZZ[powheg]',
)

SampleGroup_ZZ_powheg_m1toInf_2018 = SampleGroup(
    Name='ZZ',
    Type='Bkgd',
    Samples=['ZZTo4L_m_1toInf_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2018",
    Color=ROOT.kBlue-1,
    Style=1,
    TLatexAlias='ZZ[powheg] m > 1 GeV',
    LatexAlias='ZZ[powheg] m > 1 GeV',
)




SampleGroup_VV_2016preVFP = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo','ZZTo4L_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2016preVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Powheg]',
    LatexAlias='VV[Powheg]'
)

SampleGroup_VV_2016postVFP = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo','ZZTo4L_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2016postVFP",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Powheg]',
    LatexAlias='VV[Powheg]'
)



SampleGroup_VV_2017 = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo','ZZTo4L_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2017",
    Color=ROOT.kSpring-1,
    Style=1,
    TLatexAlias='VV[Pythia]',
    LatexAlias='VV[Pythia]'
)
SampleGroup_VV_2018 = SampleGroup(
    Name='VV',
    Type='Bkgd',
    Samples=['WZTo3LNu_amcatnlo','ZZTo4L_powheg','GluGluToZZto2e2mu','GluGluToZZto4e','GluGluToZZto4mu'],
    Era = "2018",
    Color=ROOT.kSpring-1,
    Style=1,
    #TLatexAlias='VV[powheg]',
    TLatexAlias='VV',
    #LatexAlias='VV[Powheg]'
    LatexAlias='VV' #JH
)


SampleGroup_Other_2016preVFP = SampleGroup(
    Name='Other',
    Type='Bkgd',
    Samples=['WpWp_EWK','WpWp_QCD','TTZZ','TTTT','VBF_HToZZTo4L','VHToNonbb','tHq','ttHToNonbb','ttWToLNu','ttZToLLNuNu'],
    Era = "2016preVFP",
    Color=ROOT.kGray,
    Style=1,
    TLatexAlias='Other',
    LatexAlias='Other'
)

SampleGroup_Other_2016postVFP = SampleGroup(
    Name='Other',
    Type='Bkgd',
    Samples=['WpWp_EWK','WpWp_QCD','TTZZ','TTTT','VBF_HToZZTo4L','VHToNonbb','tHq','ttHToNonbb','ttWToLNu','ttZToLLNuNu'],
    Era = "2016postVFP",
    Color=ROOT.kGray,
    Style=1,
    TLatexAlias='Other',
    LatexAlias='Other'
)
SampleGroup_Other_2017 = SampleGroup(
    Name='Other',
    Type='Bkgd',
    Samples=['WpWp_EWK','WpWp_QCD','TTZZ','TTTT','VBF_HToZZTo4L','VHToNonbb','tHq','ttHToNonbb','ttWToLNu','ttZToLLNuNu'],
    Era = "2017",
    Color=ROOT.kGray,
    Style=1,
    TLatexAlias='Other',
    LatexAlias='Other'
)
SampleGroup_Other_2018 = SampleGroup(
    Name='Other',
    Type='Bkgd',
    Samples=['WpWp_EWK','WpWp_QCD','TTZZ','TTTT','VBF_HToZZTo4L','VHToNonbb','tHq','ttHToNonbb','ttWToLNu','ttZToLLNuNu'],
    Era = "2018",
    Color=ROOT.kGray,
    Style=1,
    TLatexAlias='Other',
    LatexAlias='Other'
)


## DY
SampleGroup_DY_2016preVFP = SampleGroup(
  Name='DY',
    Type='Bkgd',
    Samples=['DYJets'],
    Era = "2016preVFP",
    Color=ROOT.kYellow,
    Style=1,
    TLatexAlias='DY#rightarrow l l ',
    LatexAlias='DY$\\rightarrow \\ell\\ell$'
)


SampleGroup_DY_2016postVFP = SampleGroup(
  Name='DY',
    Type='Bkgd',
    Samples=['DYJets'],
    Era = "2016postVFP",
    Color=ROOT.kYellow,
    Style=1,
    TLatexAlias='DY#rightarrow l l ',
    LatexAlias='DY$\\rightarrow \\ell\\ell$'
)
SampleGroup_DY_2017 = SampleGroup(
  Name='DY',
  Type='Bkgd',
  Samples=['DYJets'],
  Era = "2017",
  Color=ROOT.kYellow,
  Style=1,
    TLatexAlias='DY#rightarrow l l ',
  LatexAlias='DY$\\rightarrow \\ell\\ell$'


)
SampleGroup_DY_2018 = SampleGroup(
  Name='DY',
  Type='Bkgd',
  Samples=['DYJets'],
  Era = "2018",
  Color=ROOT.kYellow,
  Style=1,
    TLatexAlias='DY#rightarrow l l ',
  LatexAlias='DY$\\rightarrow \\ell\\ell$'


)

SampleGroup_DY_MG_2016preVFP = SampleGroup(
  Name='DY_MG',
    Type='Bkgd',
    Samples=['DY_MGJets'],
    Era = "2016preVFP",
    Color=ROOT.kYellow,
    Style=1,
    TLatexAlias='DY_MG#rightarrow l l ',
    LatexAlias='DY_MG$\\rightarrow \\ell\\ell$'
)


SampleGroup_DY_MG_2016postVFP = SampleGroup(
  Name='DY_MG',
    Type='Bkgd',
    Samples=['DY_MGJets'],
    Era = "2016postVFP",
    Color=ROOT.kYellow,
    Style=1,
    TLatexAlias='DY_MG#rightarrow l l ',
    LatexAlias='DY_MG$\\rightarrow \\ell\\ell$'
)
SampleGroup_DY_MG_2017 = SampleGroup(
  Name='DY_MG',
  Type='Bkgd',
  Samples=['DY_MGJets'],
  Era = "2017",
  Color=ROOT.kYellow,
  Style=1,
    TLatexAlias='DY_MG#rightarrow l l ',
  LatexAlias='DY_MG$\\rightarrow \\ell\\ell$'


)
SampleGroup_DY_MG_2018 = SampleGroup(
  Name='DY_MG',
  Type='Bkgd',
  Samples=['DY_MGJets'],
  Era = "2018",
  Color=ROOT.kYellow,
  Style=1,
    TLatexAlias='DY_MG#rightarrow l l ',
  LatexAlias='DY_MG$\\rightarrow \\ell\\ell$'


)



## WJets_MG_HT
SampleGroup_WJets_2016preVFP = SampleGroup(
  Name='WJets_MG',
  Type='Bkgd',
  Samples=['WJets_MG'],
  Era = "2016preVFP",
  Color=ROOT.kGreen,
  Style=1,
    TLatexAlias='W#rightarrow l  #nu',
  LatexAlias='W$\\rightarrow \\ell \\nu$'
)

## WJets_MG_HT                                                                                                                                                                                                                             
SampleGroup_WJets_2016postVFP = SampleGroup(
  Name='WJets_MG',
  Type='Bkgd',
  Samples=['WJets_MG'],
  Era = "2016postVFP",
  Color=ROOT.kGreen,
  Style=1,
    TLatexAlias='W#rightarrow l  #nu',
  LatexAlias='W$\\rightarrow \\ell \\nu$'
)

SampleGroup_WJets_2017 = SampleGroup(
  Name='WJets_MG',
  Type='Bkgd',
  Samples=['WJets_MG'],
  Era = "2017",
  Color=ROOT.kGreen,
  Style=1,
    TLatexAlias='W#rightarrow l  #nu',
  LatexAlias='W$\\rightarrow \\ell \\nu$'

)
SampleGroup_WJets_2018 = SampleGroup(
  Name='WJets_MG',
  Type='Bkgd',
  Samples=['WJets_MG'],
  Era = "2018",
  Color=ROOT.kGreen,
  Style=1,
    TLatexAlias='W#rightarrow l  #nu',
  LatexAlias='W$\\rightarrow \\ell \\nu$'

)

## NonPrompt
SampleGroup_NonPrompt_MuMu_2016preVFP = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_MuMu'],
  Era = "2016preVFP",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_NonPrompt_MuMu_2016postVFP = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_MuMu'],
  Era = "2016postVFP",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_NonPrompt_MuMu_2017 = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_MuMu'],
  Era = "2017",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)
SampleGroup_NonPrompt_MuMu_2018 = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_MuMu'],
  Era = "2018",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_NonPrompt_EE_2016preVFP = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_EE'],
  Era = "2016preVFP",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_NonPrompt_EE_2016postVFP = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_EE'],
  Era = "2016postVFP",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)


SampleGroup_NonPrompt_EE_2017 = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_EE'],
  Era = "2017",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)
SampleGroup_NonPrompt_EE_2018 = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_EE'],
  Era = "2018",
  Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)



SampleGroup_NonPrompt_2016preVFP = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_Lepton'],
    Era = "2016preVFP",
    Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)


SampleGroup_NonPrompt_2016postVFP = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_Lepton'],
    Era = "2016postVFP",
    Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)

SampleGroup_NonPrompt_2017 = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  Samples=['NonPrompt_Lepton'],
  Era = "2017",
    Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)
SampleGroup_NonPrompt_2018 = SampleGroup(
  Name='NonPrompt',
  Type='Bkgd',
  #Samples=['NonPrompt_Lepton'],
  Samples=['NonPrompt'], #JH
  Era = "2018",
    Color=870,
  Style=1,
  TLatexAlias='Nonprompt',
  LatexAlias='NonPrompt'
)


## Error from shape
SampleGroup_total_background_2016preVFP = SampleGroup(
  Name='total_background',
  Type='Bkgd',
  Samples=['total_background'],
  Era = "2016preVFP",
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='W+Jets',
  LatexAlias='total_background'
)

SampleGroup_total_background_2016postVFP = SampleGroup(
  Name='total_background',
  Type='Bkgd',
  Samples=['total_background'],
  Era = "2016postVFP",
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='W+Jets',
  LatexAlias='total_background'
)




SampleGroup_total_background_2017 = SampleGroup(
  Name='total_background',
  Type='Bkgd',
  Samples=['total_background'],
  Era = "2017",
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='W+Jets',
  LatexAlias='total_background'
)
SampleGroup_total_background_2018 = SampleGroup(
  Name='total_background',
  Type='Bkgd',
  Samples=['total_background'],
  Era = "2018",
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='W+Jets',
  LatexAlias='total_background'
)
SampleGroup_total_background_YearCombined = SampleGroup(
  Name='total_background',
  Type='Bkgd',
  Samples=['total_background'],
  Era = 'YearCombined',
  Color=ROOT.kGreen+1,
  Style=1,
  TLatexAlias='W+Jets',
  LatexAlias='total_background'
)

## TTLL
SampleGroup_TTLL_2016preVFP = SampleGroup(
  Name='TTLL',
  Type='Bkgd',
  Samples=['TTLL_powheg'],
  Era = "2016preVFP",
  Color=ROOT.kRed,
  Style=1,
  TLatexAlias='t#bar{t}',
  LatexAlias='tt'
)


SampleGroup_TTLL_2016postVFP = SampleGroup(
  Name='TTLL',
  Type='Bkgd',
  Samples=['TTLL_powheg'],
  Era = "2016postVFP",
  Color=ROOT.kRed,
  Style=1,
  TLatexAlias='t#bar{t}',
  LatexAlias='tt'
)
SampleGroup_TTLL_2017 = SampleGroup(
  Name='TTLL',
  Type='Bkgd',
  Samples=['TTLL_powheg'],
  Era = "2017",
  Color=ROOT.kRed,
  Style=1,
  TLatexAlias='t#bar{t}',
  LatexAlias='tt'
)
SampleGroup_TTLL_2018 = SampleGroup(
  Name='TTLL',
  Type='Bkgd',
  Samples=['TTLL_powheg'],
  Era = "2018",
  Color=ROOT.kRed,
  Style=1,
  TLatexAlias='t#bar{t}',
  LatexAlias='tt'
)


## TW
SampleGroup_TW_2016preVFP = SampleGroup(
  Name='TW',
  Type='Bkgd',
  Samples=['SingleTop_tW_antitop_NoFullyHad','SingleTop_tW_top_NoFullyHad'],
  Era = "2016preVFP",
  Color=ROOT.kGray,
  Style=1,
  TLatexAlias='tW',
  LatexAlias='tW'
)
SampleGroup_TW_2016postVFP = SampleGroup(
  Name='TW',
  Type='Bkgd',
  Samples=['SingleTop_tW_antitop_NoFullyHad','SingleTop_tW_top_NoFullyHad'],
  Era = "2016postVFP",
  Color=ROOT.kGray,
  Style=1,
  TLatexAlias='tW',
  LatexAlias='tW'
)


SampleGroup_TW_2017 = SampleGroup(
  Name='TW',
  Type='Bkgd',
  Samples=['SingleTop_tW_antitop_NoFullyHad','SingleTop_tW_top_NoFullyHad'],
  Era = "2017",
  Color=ROOT.kGray,
  Style=1,
  TLatexAlias='tW',
  LatexAlias='tW'
)
SampleGroup_TW_2018 = SampleGroup(
  Name='TW',
  Type='Bkgd',
  Samples=['SingleTop_tW_antitop_NoFullyHad','SingleTop_tW_top_NoFullyHad'],
  Era = "2018",
  Color=ROOT.kGray,
  Style=1,
  TLatexAlias='tW',
  LatexAlias='tW'
)
