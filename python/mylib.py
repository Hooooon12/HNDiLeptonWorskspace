import os,ROOT
import math
from array import array

import ctypes

def AddHistograms(h_original, h_toAdd, option=''):
  if option=="L":

    h_out = h_original.Clone()
    for ix in range(0, h_original.GetXaxis().GetNbins()):
      y_original = h_original.GetBinContent(ix+1)
      e_original = h_original.GetBinError(ix+1)

      y_toAdd = h_toAdd.GetBinContent(ix+1)
      e_toAdd = h_toAdd.GetBinError(ix+1)

      h_out.SetBinContent(ix+1, y_original+y_toAdd)
      h_out.SetBinError(ix+1, e_original+e_toAdd)

    return h_out

  else:
    h_original.Add(h_toAdd)
    return h_original

def TotalLumiByEra(DataEra):
  
  if DataEra=="2016preVFP":
    return "19.5"
  if DataEra=="2016postVFP":
    return "16.8"
  if DataEra=="2017":
    return "41.5"
  if DataEra=="2018":
    return "59.8"

  if DataEra =="Run2":
    return str(19.52+16.81+41.48+59.83)

  else:
    print ("[mylib.py, TotalLumiByEra()] Wrong DataEra : %s"%DataEra)
    return str(19.52+16.81)
    
    
  
def TotalLumi(DataYear):
    
  if DataYear==2016:
    return "36.3"
  if DataYear==2017:
    return "41.5"
  if DataYear==2018:
    return "59.8"

  if DataYear<0:
    return "138"
  else:
    print ("[mylib.py, TotalLumi()] Wrong DataYear : %d"%DataYear)
    return ("36.3")

def LumiError(DataYear):

  print ("Setting Unc. from https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM")
  
  if DataYear == -1:
    return 0.016
  
  if DataYear==2016:
    return 0.012
  elif DataYear==2017:
      return 0.023
  elif DataYear==2018:
    return 0.025
  else:
    print ("[mylib.py, LumiError()] Wrong DataYear : %d"%DataYear)
    return 0.

def TotalLumi(DataYear):

  if DataYear==2016:
    return "35.92"
  if DataYear==2017:
    return "41.53"
  if DataYear==2018:
    return "59.74"
  if DataYear<0:
    return "138"
  else:
    print "[mylib.py, TotalLumi()] Wrong DataYear : %d"%DataYear
    return "35.9"

def LumiError(DataYear):

  #if DataYear==2016:
  #  return 0.025
  #elif DataYear==2017:
  #  return 0.023
  #elif DataYear==2018:
  #  return 0.025
  #else:
  #  print "[mylib.py, LumiError()] Wrong DataYear : %d"%DataYear
  #  return 0.


  return 0.018

def MakeOverflowBin(hist):

  #### GetXaxis().SetRangeUser() should be done first

  #### 0     1                                          n_bin_origin
  ####     |===|===|===|===|===|===|===|===|===|===|===|===|===|
  ####           bin_first        bin_last
  ####             |===|===|===|===|===|
  #### |   |                                                   |   |
  #### under                                                   over
  #### flow                                                    flow
  #### |<=========>|                   |<=========================>|
  ####  all underflow                           all overflow

  #### Original NBins
  n_bin_origin = hist.GetXaxis().GetNbins()
  #### Changed NBins
  bin_first = hist.GetXaxis().GetFirst()
  bin_last = hist.GetXaxis().GetLast()
  n_bin_inrange = bin_last-bin_first+1

  x_first_lowedge = hist.GetXaxis().GetBinLowEdge(bin_first)
  x_last_upedge = hist.GetXaxis().GetBinUpEdge(bin_last)

  Allunderflows = hist.Integral(0, bin_first-1)
  Allunderflows_error = hist.GetBinError(0)
  Allunderflows_error = Allunderflows_error*Allunderflows_error
  for i in range(1, bin_first-1 +1):
    Allunderflows_error += (hist.GetBinError(i))*(hist.GetBinError(i))
  Allunderflows_error = math.sqrt(Allunderflows_error)

  Alloverflows = hist.Integral(bin_last+1, n_bin_origin+1)
  Alloverflows_error = hist.GetBinError(n_bin_origin+1)
  Alloverflows_error = Alloverflows_error*Alloverflows_error
  for i in range(bin_last+1, n_bin_origin +1):
    Alloverflows_error += (hist.GetBinError(i))*(hist.GetBinError(i))
  Alloverflows_error = math.sqrt(Alloverflows_error)

  #### Make X-bin array
  temp_xbins = [] ## size = n_bin_inrange+1
  counter=0
  for i in range(bin_first,bin_last +1):
    temp_xbins.append( hist.GetXaxis().GetBinLowEdge(i) )
    counter += 1
  temp_xbins.append( hist.GetXaxis().GetBinUpEdge(bin_last) )

  hist_out = ROOT.TH1D(hist.GetName()+'tmp', hist.GetTitle(), n_bin_inrange, array("d",temp_xbins))
  for i in range(1,n_bin_inrange+1):
    this_content = hist.GetBinContent(bin_first-1+i)
    this_error = hist.GetBinError(bin_first-1+i)
    #print '[%d,%d] : %f'%(hist_out.GetXaxis().GetBinLowEdge(i),hist_out.GetXaxis().GetBinUpEdge(i),this_content)

    #### underflows
    if i==1:
      this_content += Allunderflows
      this_error = math.sqrt( this_error*this_error + Allunderflows_error*Allunderflows_error )

    #### overflows
    if i==n_bin_inrange:
      this_content += Alloverflows
      this_error = math.sqrt( this_error*this_error + Alloverflows_error*Alloverflows_error )

    hist_out.SetBinContent(i, this_content)
    hist_out.SetBinError(i, this_error)

  hist_out.SetName(hist.GetName())
  return hist_out

def RebinNMass(hist, region, DataYear):

  lastbin = hist.GetXaxis().GetNbins()
  vec_bins = [100, 200, 300, 400, 500, 750, 1000, 2000,  8000]
  if "SR2" in region:
    vec_bins = [800, 1000, 1200, 1500, 1800, 8000]

  if ('LowWR' in region):
    tmp_vec_bins = [0, 50, 75]

def RebinWRMass(hist, region, DataYear):

  lastbin = hist.GetXaxis().GetNbins()
  vec_bins = [800, 1000, 1200, 1400, 1600, 2000, 2400, 2800, 3200, 8000]
  if "Boosted" in region:
    vec_bins = [800, 1000, 1200, 1500, 1800, 8000]

  #if ('LowWR' in region) or ('DYCR' in region):
  if ('LowWR' in region):
    tmp_vec_bins = [0, 200, 300, 400, 500, 600, 700, 800]

    for b in vec_bins:
      tmp_vec_bins.append(b)
    vec_bins = tmp_vec_bins

  n_bin = len(vec_bins)-1
  hist = hist.Rebin(n_bin, hist.GetName(), array("d", vec_bins) )
  return hist

  return ChangeGeVToTeVXaxis(hist)
  #return hist

def ChangeGeVToTeVXaxis(h):

  x_New = []
  x_New.append( h.GetXaxis().GetBinLowEdge(1)/1000. )
  for ix in range(0, h.GetXaxis().GetNbins()):
    iBin = ix+1
    x_New.append( h.GetXaxis().GetBinUpEdge(iBin)/1000. )
  h_New = ROOT.TH1D(h.GetName(), '', len(x_New)-1, array("d", x_New))

  targetBinWidth = 0.2#TeV

  for ix in range(0, h.GetXaxis().GetNbins()):
    iBin = ix+1

    new_BinContent = h.GetBinContent(iBin)
    new_BinError = h.GetBinError(iBin)

    #this_BinWidth = h_New.GetXaxis().GetBinUpEdge(iBin) - h_New.GetXaxis().GetBinLowEdge(iBin)
    #new_BinContent = new_BinContent/this_BinWidth * targetBinWidth
    #new_BinError = new_BinError/this_BinWidth * targetBinWidth

    h_New.SetBinContent(iBin, new_BinContent)
    h_New.SetBinError(iBin, new_BinError)

  return h_New


def RebinJetPt(hist, region, DataYear):

  lastbin = hist.GetXaxis().GetNbins()
  vec_bins = [0, 40, 100, 200, 400, 600, 800, 1000, 1500, 2000]
  if "Boosted" in region:
    vec_bins = [0, 200, 400, 600, 800, 1000, 2000]

  n_bin = len(vec_bins)-1
  hist = hist.Rebin(n_bin, hist.GetName(), array("d", vec_bins) )
  return hist

def GetMaximum(a, ErrorScale=1.):

  NX = a.GetN()

  maxval = -9999.
  for i in range(0,NX):

    x = ctypes.c_double(0.)
    y = ctypes.c_double(0.)
    #x = ROOT.Double(0.)
    #y = ROOT.Double(0.)

    a.GetPoint(i, x, y)
    yerr_low  = a.GetErrorYlow(i)
    yerr_high = a.GetErrorYhigh(i)

    if (y.value+ErrorScale*yerr_high > maxval):
      maxval = y.value+ErrorScale*yerr_high


  return maxval

def GetAsymmError(MC_stacked_allerr_Up, MC_stacked_allerr_Down):

  NBin = MC_stacked_allerr_Up.GetXaxis().GetNbins()
  x = []
  x_lerr = []
  x_rerr = []
  y = []
  y_lerr = []
  y_rerr = []

  for i in range(0,NBin):

    x.append( MC_stacked_allerr_Up.GetXaxis().GetBinCenter(i+1) )
    x_lerr.append( x[i] - MC_stacked_allerr_Up.GetXaxis().GetBinLowEdge(i+1) )
    x_rerr.append( MC_stacked_allerr_Up.GetXaxis().GetBinUpEdge(i+1) - x[i] )

    y.append( MC_stacked_allerr_Up.GetBinContent(i+1) )
    y_lerr.append( MC_stacked_allerr_Down.GetBinError(i+1) )
    y_rerr.append( MC_stacked_allerr_Up.GetBinError(i+1) )

  out = ROOT.TGraphAsymmErrors(NBin, array("d", x), array("d", y),  array("d", x_lerr), array("d", x_rerr), array("d", y_lerr), array("d", y_rerr))
  return out

def GetDYNormSF(DataYear, channel):

  DYNorm = 1.
  DYNorm_err = 0.

  if "_EMu_" in channel:
    return 1., 0.

  int_channel = -1 ## 0 : ee, 1 : mm
  if "Electron" in channel:
    int_channel = 0
  elif "Muon" in channel:
    int_channel = 1
  else:
    print ('Wrong channel name '+channel)
    exit()

  int_region = -1 ## 0 : SR1, 1 : SR2
  if "SR1" in channel:
    int_region = 0;
  elif "SR2" in channel:
    int_region = 1;
  elif "SR3" in channel:
    int_region = 2;
    
  else:
    print ('Wrong region name '+channel)
    exit()

  #print '%s -> int_channel = %d, int_region = %d'%(channel,int_channel,int_region)

  if DataYear==2016:
    if int_channel==0:
      if int_region==0:
        DYNorm = 0.985967
        DYNorm_err = 0.0472367
      elif int_region==1:
        DYNorm = 1.18924
        DYNorm_err = 0.0593071
      else:
        print ("Wrong DY Norm")
        exit()
    elif int_channel==1:
      if int_region==0:
        DYNorm = 0.971114
        DYNorm_err = 0.0382234
      elif int_region==1:
        DYNorm = 1.00351
        DYNorm_err = 0.0507593
      else:
        print ("Wrong DY Norm")
        exit()
    else:
      print ("Wrong DY Norm")
      exit()
  elif DataYear==2017:
    if int_channel==0:
      if int_region==0:
        DYNorm = 1.03281
        DYNorm_err = 0.0502737
      elif int_region==1:
        DYNorm = 1.30754
        DYNorm_err = 0.0653227
      else:
        print ("Wrong DY Norm")
        exit()
    elif int_channel==1:
      if int_region==0:
        DYNorm = 1.03805
        DYNorm_err = 0.0405121
      elif int_region==1:
        DYNorm = 1.19954
        DYNorm_err = 0.0592457
      else:
        print ("Wrong DY Norm")
        exit()
    else:
      print ("Wrong DY Norm")
      exit()
  elif DataYear==2018:
    if int_channel==0:
      if int_region==0:
        DYNorm = 1.00002
        DYNorm_err = 0.05551
      elif int_region==1:
        DYNorm = 1.30778
        DYNorm_err = 0.0581163
      else:
        print ("Wrong DY Norm")
        exit()
    elif int_channel==1:
      if int_region==0:
        DYNorm = 1.02359
        DYNorm_err = 0.0481667
      elif int_region==1:
        DYNorm = 1.16497
        DYNorm_err = 0.0496011
      else:
        print ("Wrong DY Norm")
        exit()
    else:
      print ("Wrong DY Norm")
      exit()

  return DYNorm, DYNorm_err

  #if 'DYCR' in channel:
  #  return DYNorm, DYNorm_err
  #  return DYNorm, 0.30*DYNorm
  #else:
  #  return DYNorm, 0.30*DYNorm

def GetSignalXsec(filepath,  mN):

  lines = open(filepath).readlines()
  for line in lines:
    words = line.split()

    if len(words) != 2:
      continue
    if ( int(words[0])==int(mN) ):
      return float(words[1])
  print ('Xsec not found for mN=%d'%(mN))



def GetMCUncertainty(SampleName):
  
  if "DY" in SampleName:
    return 0.08
  elif "WZ" in SampleName:
    return 0.1
  elif "ZZ" in SampleName:
    return 0.1
  elif "Top" in SampleName:
    return 0.1
  else:
    return 0.3

      
def GetNormSF(DataYear, sample):

  WORKING_DIR = os.environ["HNDILEPTONWORKSPACE_DIR"]
  CorrFile = WORKING_DIR + '/data/'+os.getenv("SKFlatV")+'/'+str(DataYear)+'/MCSF.txt'

  lines = open(CorrFile).readlines()
  MCSF=1.
  for line in lines:
    words = line.strip('\n').split()
    if words[0] == sample:
      MCSF = words[1]


  print "GetNormSF : " + sample + " " + str(MCSF)
  return float(MCSF)

def GetKFactor(mN, Era='2016preVFP', lepch=0):

  ##==== lepch : 0=ee, 1=mm, 2=em

  WORKING_DIR = os.environ["PLOTTER_WORKING_DIR"]
  dataset =  os.environ["SKANVERSION"]
  ENV_PLOT_PATH =  os.environ["PLOT_PATH"]

  massstring = "mN"+str(mN)

  ##==== get averaged kfactor
  lines = open(WORKING_DIR+"/data/"+dataset+"/"+str(Year)+"/AveragedKFactor.txt").readlines()
  this_avg_kfactor = -1.;
  for line in lines:
    words = line.strip('\n').split()
    this_mass = words[0]
    avg_k_ee = float(words[1])
    avg_k_mm = float(words[2])

    if massstring==this_mass:
      if lepch==0:
        this_avg_kfactor = avg_k_ee;
      elif lepch==1:
        this_avg_kfactor = avg_k_mm;
      else:
        print ("[mylib.py][GetKFactor] Wrong lepch = "+str(lepch))
      break

  if this_avg_kfactor<0:
    print ("[mylib.h][GetKFactor] this_avg_kfactor = "+str(this_avg_kfactor))

  return this_avg_kfactor


