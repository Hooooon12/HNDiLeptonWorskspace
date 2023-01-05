from ROOT import *
import os

paths = [
        "/data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/2023_01_04_172956/higgsCombinecard_2017_MuMu_M500_HNL_UL.root_exp0.025.HybridNew.mH120.quant0.025.root",
        "/data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/2023_01_04_174359/higgsCombinecard_2017_MuMu_M500_HNL_UL.root_exp0.160.HybridNew.mH120.quant0.160.root",
        "/data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/2023_01_04_182759/higgsCombinecard_2017_MuMu_M500_HNL_UL.root_exp0.500.HybridNew.mH120.quant0.500.root",
        "/data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/2023_01_04_184919/higgsCombinecard_2017_MuMu_M500_HNL_UL.root_exp0.840.HybridNew.mH120.quant0.840.root",
        "/data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/2023_01_04_185328/higgsCombinecard_2017_MuMu_M500_HNL_UL.root_exp0.975.HybridNew.mH120.quant0.975.root",
        #"test",
        ]

f_2sdDown = TFile.Open(paths[0])
f_1sdDown = TFile.Open(paths[1])
f_Central = TFile.Open(paths[2])
f_1sdUp   = TFile.Open(paths[3])
f_2sdUp   = TFile.Open(paths[4])

tree_2sdDown = f_2sdDown.Get("limit")
tree_1sdDown = f_1sdDown.Get("limit")
tree_Central = f_Central.Get("limit")
tree_1sdUp   = f_1sdUp.Get("limit")
tree_2sdUp   = f_2sdUp.Get("limit")

tree_2sdDown.GetEntry(0)
tree_1sdDown.GetEntry(0)
tree_Central.GetEntry(0)
tree_1sdUp.GetEntry(0)
tree_2sdUp.GetEntry(0)

with open("expected_limit.txt", 'w') as f:
  f.write(str(round(tree_2sdDown.limit,3))+"\n")
  f.write(str(round(tree_1sdDown.limit,3))+"\n")
  f.write(str(round(tree_Central.limit,3))+"\n")
  f.write(str(round(tree_1sdUp.limit,3))+"\n")
  f.write(str(round(tree_2sdUp.limit,3))+"\n")
