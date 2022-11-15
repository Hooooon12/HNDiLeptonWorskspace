import os 


if os.getenv("FILE_MERGED_PATH") == "NULL":
    print("Env not set.....")
    exit()


eras = ["2016preVFP", "2016postVFP", "2017", "2018"]
eras = ["2017"]
#eras = ["2018"]
paramNames = ["POGCR_UL", "HNL_UL"]
paramNames = ["HNL_UL"] #JH

MergeData=False
MergeFake=False
MergeCF=  False
MergeConv=True
CopyMC=   False

MergeMC=False
MergeBkg=False

Analyser="HNL_ControlRegionPlotter"
InputPath=os.getenv("SKFlatOutputDir")+"/"+os.getenv("SKFlatV") + "/"+Analyser+"/"
OutputPath=os.getenv("FILE_MERGED_PATH")+"/"+Analyser+"/"

if not os.path.exists(OutputPath):
    os.system("mkdir -p " + OutputPath)

for era in eras:

    if not os.path.exists(OutputPath + era):
        os.system("mkdir -p " + OutputPath + era)

if MergeFake:

    for era in eras:
        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_NonPrompt.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)
        
        os.system("hadd " + OutFile + "  " + InputPath + "/"+era+"//RunFake__/DATA/*")


if MergeMC:

    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_MC.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " + OutFile + "  " + InputPath + "/"+era+"/*HNMu*")

if CopyMC:

    for era in eras:

        OutFile=OutputPath + era + "/"

        os.system("cp " + InputPath + "/"+era+"/*HNMu*.root " + OutFile) #JH


if MergeCF:

    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_CF.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " + OutFile + "  " + InputPath + "/"+era+"//RunCF__/DATA/*") #JH

       
if MergeConv:

    for era in eras:

        Conv_dict = {
                     'Conv' : " "+InputPath+"/"+era+"/RunConv__/*G.root", #JH : when testing WG_LO without DY, WJet
                     #'Conv' : " "+InputPath+"/"+era+"/RunConv__/*G.root"+" "+InputPath+"/"+era+"/RunConv__/*DYJets.root", #JH : final version (maybe)
                     'DYonly' : " "+InputPath+"/"+era+"/RunConv__/*G.root"+" "+InputPath+"/"+era+"/RunConv__/*DYJets.root",
                     'MG' : " "+InputPath+"/"+era+"/RunConv__/*G.root"+" "+InputPath+"/"+era+"/RunConv__/*DYJets.root"+" "+InputPath+"/"+era+"/RunConv__/*WJets_MadGraph.root",
                     'amcatnlo' : " "+InputPath+"/"+era+"/RunConv__/*G.root"+" "+InputPath+"/"+era+"/RunConv__/*DYJets.root"+" "+InputPath+"/"+era+"/RunConv__/*WJets_amcatnlo.root",
                     'Sherpa' : " "+InputPath+"/"+era+"/RunConv__/*G.root"+" "+InputPath+"/"+era+"/RunConv__/*DYJets.root"+" "+InputPath+"/"+era+"/RunConv__/*WJets_Sherpa.root",
                     'HT' : " "+InputPath+"/"+era+"/RunConv__/*G.root"+" "+InputPath+"/"+era+"/RunConv__/*DYJets.root"+" "+InputPath+"/"+era+"/RunConv__/*WJetsToLNu_HT*.root",
                    }

        OutFiles = []

        OutFiles.append(OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv.root")
        #OutFiles.append(OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv_DYonly.root")
        #OutFiles.append(OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv_MG.root")
        #OutFiles.append(OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv_amcatnlo.root")
        #OutFiles.append(OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv_Sherpa.root")
        #OutFiles.append(OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv_HT.root")

        for OutFile in OutFiles:

          Conv_tag = OutFile.split('_')[-1][0:-5]

          if os.path.exists(OutFile):
              os.system("rm " + OutFile)

          os.system("hadd " +OutFile+Conv_dict[Conv_tag]) #JH



if MergeBkg:
    
    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Bkg.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " +OutFile+  "   " + OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep*")

    #os.system("python MergeSignal.py")
    #os.system("python MergeSignal16.py")
    #os.system("python Merge16.py")
    #os.system("python MergeSignalFull.py") #JH

if MergeData:

    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_data.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " +OutFile + "   " + InputPath + "/"+era+"/DATA/*")
