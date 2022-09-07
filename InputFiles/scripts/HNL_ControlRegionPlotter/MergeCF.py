import os 

eras = ["2016preVFP", "2016postVFP", "2017", "2018"]

eras = ["2018"]

# This script will merge CF root files

Analyser="HNL_ControlRegionPlotter"

for era in eras:
    
    if os.getenv("FILE_MERGED_PATH") == "NULL":
        print("Env not set.....")
        exit()
    
    FilePath=  os.getenv("FILE_MERGED_PATH")+"/"+Analyser+"/"+era

    if os.path.exists(FilePath+"/HNL_ControlRegionPlotter_SkimTree_Dilepton_CF.root"):
        os.system("rm " + FilePath+"/HNL_ControlRegionPlotter_SkimTree_Dilepton_CF.root")

    os.system("hadd " + FilePath+"/HNL_ControlRegionPlotter_SkimTree_Dilepton_CF.root  /data6/Users/jalmond/SKFlatOutput//Run2UltraLegacy_v3/HNL_ControlRegionPlotter/"+era+"/RunCF__/HNL_ControlRegionPlotter_SkimTree_Dilepton_*")
