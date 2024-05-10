# python ReadLimitFromTree_exo17028.py

from ROOT import *
import os
import commands as cmd

workdir = "/data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegion_Plotter/Batch/exo17028_noSSWW"
masses = ["100","125","200","250","300","400","500","600","700","800","900","1000","1100","1200","1500"]
channels = ["MuMu","EE"]

os.system("mkdir -p out/240503_exo17028_noSSWW")

for channel in channels:

  with open("out/240503_exo17028_noSSWW/"+channel+"_HNTightV2_Run2_Asym_limit.txt", 'w') as f:
    for mass in masses:
      if int(mass) <= 100:
  	    scale_ = 0.1
      elif int(mass) <= 300:
        scale_ = 1.
      elif int(mass) <=700:
        scale_ = 10.
      else:
        scale_ = 100.
      scale = scale_ * 0.0001
  
      this_name = "CombinedYears_"+channel+"_combined_SR1_SR2_N"+mass+"_Combined_HNTightV2"
      path = workdir+"/Asymptotic/"+this_name+"/output/"+this_name+"_Asymptotic.root"
  
      f_Asym = TFile.Open(path)
      tree_Asym = f_Asym.Get("limit")
  
      tree_Asym.GetEntry(2) # substitute for obs. limit for now
      f.write(mass+"\t"+str(scale*round(tree_Asym.limit,3))+"\t")
  
      for i in range(5): # expected limits
        tree_Asym.GetEntry(i)
        f.write(str(scale*round(tree_Asym.limit,3))+"\t")
      f.write("\n")
