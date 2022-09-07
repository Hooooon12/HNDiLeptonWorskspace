import os 


if os.getenv("FILE_MERGED_PATH") == "NULL":
    print("Env not set.....")
    exit()


eras = ["2016preVFP", "2016postVFP", "2017", "2018"]

MergeFake=True
MergeCF=True
MergeConv=True
MergeMC=True
MergeBkg=True

Analyser="HNL_ControlRegionPlotter"
InputPath=os.getenv("SKFlatOutputDir")+"/"+os.getenv("SKFlatV") + "/"+Analyser+"/"
OutputPath=os.getenv("FILE_MERGED_PATH")+"/"+Analyser+"/"

if not os.path.exists(OutputPath):
    os.system("mkdir " + OutputPath)

for era in eras:

    if not os.path.exists(OutputPath + era):
        os.system("mkdir " + OutputPath + era)

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



if MergeCF:

    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_CF.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " + OutFile + "  " + InputPath + "/"+era+"//RunCF__/*")

       
if MergeConv:

    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Conv.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " +OutFile+  "   " + InputPath + "/"+era+"//RunConv__/*")



if MergeBkg:
    
    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_Bkg.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " +OutFile+  "   " + OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep*")

    os.system("python MergeSignal.py")
    os.system("python MergeSignal16.py")
    os.system("python Merge16.py")
    os.system("python MergeSignalFull.py")

MergeData=False
if MergeData:

    for era in eras:

        OutFile=OutputPath + era + "/"+Analyser+"_SkimTree_HNMultiLep_data.root"
        if os.path.exists(OutFile):
            os.system("rm " + OutFile)

        os.system("hadd " +OutFile + "   " + InputPath + "/"+era+"/DATA/*")
