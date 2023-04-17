#include "Macros.h"
#include "canvas_margin.h"

//==== ReturnWhat = 0 : Obs
//==== ReturnWhat = 1 : Exp
//==== ReturnWhat = 2 : +- 1sd
//==== ReturnWhat = 3 : +- 2sd

void  HiggsCombindedLimit(int i=3, int j=1, TString dirname="", int ReturnWhat=0, bool RunFullCLs=true){

  bool DrawObserved = false;

  setTDRStyle();

  //gStyle->SetOptStat(0);
  
  TString WORKING_DIR =   getenv("HNDILEPTONWORKSPACE_DIR");  
  TString version = getenv("FLATVERSION");
  TString dataset = "";//getenv("CATANVERSION");
  TString ENV_FILE_PATH = WORKING_DIR;
  TString ENV_PLOT_PATH = getenv("PLOT_PATH");

  TString filepath = ENV_FILE_PATH+dataset+"/Limits/ReadLimits/Shape/out/";
  //TString plotpath = ENV_PLOT_PATH+dataset+"/Limits/";
  TString plotpath = ENV_FILE_PATH+dataset+"/src/LimitPlotter/out/";

  //if(dirname!=""){
  //
  //  filepath = ENV_FILE_PATH+dataset+"Limit/"+dirname+"/";
  //  }

  TString WhichYear = "2016";
  if (j==1) WhichYear = "2017";
  if (j==2) WhichYear = "2018";
  if (j==3) WhichYear = "Run2";
  TString WhichDirectoryInCutop = "MuMu_SSCombined";
  if(i==1) WhichDirectoryInCutop = "MuMu_Bin1";
  if(i==2) WhichDirectoryInCutop = "MuMu_Bin2";
  if(i==3) WhichDirectoryInCutop = "MuMu_SSCombined";
  if(i==4) WhichDirectoryInCutop = "EE_Bin1";
  if(i==5) WhichDirectoryInCutop = "EE_Bin2";
  if(i==6) WhichDirectoryInCutop = "EE_SSCombined";
  if(i==7) WhichDirectoryInCutop = "MuEl_Bin1";
  if(i==8) WhichDirectoryInCutop = "MuEl_Bin2";
  if(i==9) WhichDirectoryInCutop = "MuEl_SSCombined";
  if(i==10) WhichDirectoryInCutop = "MuMu_Bin3";
  if(i==12) WhichDirectoryInCutop = "MuMu_Bin4";
  if(i==13) WhichDirectoryInCutop = "MuMu_OSSSCombined";
  if(i==14) WhichDirectoryInCutop = "EE_Bin3";
  if(i==15) WhichDirectoryInCutop = "EE_Bin4";
  if(i==16) WhichDirectoryInCutop = "EE_OSSSCombined";
  if(i==17) WhichDirectoryInCutop = "MuEl_Bin3";
  if(i==18) WhichDirectoryInCutop = "MuEl_Bin4";
  if(i==19) WhichDirectoryInCutop = "MuEl_OSSSCombined";

  if(j==3){
    WhichDirectoryInCutop = WhichDirectoryInCutop.ReplaceAll("Combined","");
  }
  //filepath = filepath + WhichYear + "/"+ WhichDirectoryInCutop;
  //vector<TString> myWPs = {"InputForCombine","InputForCombine_beforeFixLowMass","Workshop","Workshop_FullRun2","Workshop_FullRun2_beforeFixLowMass"};
  //vector<TString> myWPs = {"Workshop_FixedSR1"};
  //vector<TString> myWPs = {"AddSyst_DividedBy1p87"};
  vector<TString> myWPs = {"KPS23Spr"};
  for(int i=0; i<myWPs.size(); i++){
    TString myWP = myWPs.at(i);
    TString this_filepath = filepath+myWP;

    TString channel = "MuMu";
    if(WhichDirectoryInCutop.Contains("EE")) channel = "EE";
    if(WhichDirectoryInCutop.Contains("MuEl")) channel = "MuEl";

    if( !gSystem->mkdir(plotpath, kTRUE) ){
      cout
      << "###################################################" << endl
      << "Directoy " << plotpath << " is created" << endl
      << "###################################################" << endl
      << endl;
    }
    

    cout << this_filepath << endl;
    TLatex latex_CMSPriliminary, latex_Lumi, latex_title;
    latex_CMSPriliminary.SetNDC();
    latex_Lumi.SetNDC();
    latex_title.SetNDC();

    //=== 13 TeV S-only channel

    string elline;
    if(WhichDirectoryInCutop.Contains("MuMu")) cout << this_filepath+"/"+WhichYear+"_MuMu_HNL_UL_Asym_limit.txt" << endl;
    else if(WhichDirectoryInCutop.Contains("EE")) cout << this_filepath+"/"+WhichYear+"_EE_HNL_UL_Asym_limit.txt" << endl;
    else if(WhichDirectoryInCutop.Contains("MuEl")) cout << this_filepath+"/"+WhichYear+"_EMu_HNL_UL_Asym_limit.txt" << endl;
    //cout << filepath+ "/2017_EE_HNL_UL_Asym_limit_fixed.txt" << endl;
    //cout << filepath+ "/2017_MuMu_HNL_UL_Asym_limit_fixed.txt" << endl;
    ifstream in;
    if(WhichDirectoryInCutop.Contains("MuMu")) in.open(this_filepath+"/"+WhichYear+"_MuMu_HNL_UL_Asym_limit.txt");
    else if(WhichDirectoryInCutop.Contains("EE")) in.open(this_filepath+"/"+WhichYear+"_EE_HNL_UL_Asym_limit.txt");
    else if(WhichDirectoryInCutop.Contains("MuEl")) in.open(this_filepath+"/"+WhichYear+"_EMu_HNL_UL_Asym_limit.txt");
    //ifstream in(filepath+ "/2017_EE_HNL_UL_Asym_limit_fixed.txt");
    //ifstream in(filepath+ "/2017_MuMu_HNL_UL_Asym_limit_fixed.txt");
    int n_central = 22; // 13; //28, but now removing 80 Gev
    double mass[n_central], obs[n_central], limit[n_central], onesig_left[n_central], onesig_right[n_central], twosig_left[n_central], twosig_right[n_central];

    int dummyint=0;
    double max_obs = 0., max_obs_mass = 0.;
    double min_obs = 9999., min_obs_mass = 0.;
    while(getline(in,elline)){
      cout << "ell line = " << elline << endl;
      if(elline.find("7500") != string::npos) continue; //FIXME JH : 7500 now has a xsec issue...
      std::istringstream is( elline );
      is >> mass[dummyint];
      is >> obs[dummyint];
      //is >> limit[dummyint];
      //is >> onesig_right[dummyint];
      //is >> onesig_left[dummyint];
      //is >> twosig_right[dummyint];
      //is >> twosig_left[dummyint];
      is >> twosig_left[dummyint];
      is >> onesig_left[dummyint];
      is >> limit[dummyint];
      is >> onesig_right[dummyint];
      is >> twosig_right[dummyint];

      //==== skip points
      if(obs[dummyint]<=0 || limit[dummyint]<=0 || onesig_left[dummyint]<=0 || onesig_right[dummyint]<=0 || twosig_left[dummyint]<=0 || twosig_right[dummyint]<=0){
        n_central--;
        continue;
      }
      
      double scale=0.01; //mixing squared is 0.01 now
      //if(mass[dummyint]<=60) scale *= 0.01;
      //else if(mass[dummyint]<=200) scale *= 0.001;
      //else if(mass[dummyint]<=600) scale *= 0.1;
      //else if(mass[dummyint]<=1000) scale *= 1.;
      //else scale *= 10.;

      //    scale*=  0.01; //FIXME

      //if(channel=="MuEl") scale *= 0.5;

      obs[dummyint] *= scale;

      limit[dummyint] *= scale;
      onesig_left[dummyint] *= scale;
      onesig_right[dummyint] *= scale;
      twosig_left[dummyint] *= scale;
      twosig_right[dummyint] *= scale;

      //==== skip points
      if(obs[dummyint]>1.0 || limit[dummyint]>1.0){
        //n_central--;
        //continue;
      }

      onesig_left[dummyint] = limit[dummyint]-onesig_left[dummyint];
      onesig_right[dummyint] = onesig_right[dummyint] - limit[dummyint];
      twosig_left[dummyint] = limit[dummyint]-twosig_left[dummyint];
      twosig_right[dummyint] = twosig_right[dummyint] - limit[dummyint];

      if(max_obs<obs[dummyint]){
        max_obs = obs[dummyint];
        max_obs_mass = mass[dummyint];
      }
      if(min_obs>obs[dummyint]){
        min_obs = obs[dummyint];
        min_obs_mass = mass[dummyint];
      }

      dummyint++;
    }

    cout << "n_central = " << n_central << " mass size = " << mass << endl;
    for(unsigned int k = 0; k < n_central ; k++){

      cout << "Mass = " << mass[k] << " expected = " << limit[k] << " + 1sigma = " << onesig_right[k] << " -1sigma = "  << onesig_left[k] << " + 2 sigma = " << twosig_right[k] << " - 2 sigam = " << twosig_left[k] << endl;
    }
    
    cout << "Max : " << max_obs_mass << "\t" << max_obs << endl;
    cout << "Min : " << min_obs_mass << "\t" << min_obs << endl;

    //TGraph *gr_13TeV_obs = new TGraph(n_central,mass,obs);
    TGraphAsymmErrors *gr_13TeV_obs = new TGraphAsymmErrors(n_central,mass,obs,0,0,0,0);
    gr_13TeV_obs->SetLineWidth(3);
    gr_13TeV_obs->SetLineColor(kBlack);

    //TGraph *gr_13TeV_exp = new TGraph(n_central,mass,limit);
    TGraphAsymmErrors *gr_13TeV_exp = new TGraphAsymmErrors(n_central,mass,limit,0,0,0,0);
    gr_13TeV_exp->SetLineWidth(3);
    gr_13TeV_exp->SetLineStyle(2);
    gr_13TeV_exp->SetFillColor(kWhite);

    TGraphAsymmErrors *gr_band_1sigma = new TGraphAsymmErrors(n_central, mass, limit, 0, 0, onesig_left, onesig_right);
    gr_band_1sigma->SetFillColor(kGreen+1);
    gr_band_1sigma->SetLineColor(kGreen+1);
    gr_band_1sigma->SetMarkerColor(kGreen+1);

    TGraphAsymmErrors *gr_band_2sigma = new TGraphAsymmErrors(n_central, mass, limit, 0, 0, twosig_left, twosig_right);
    gr_band_2sigma->SetFillColor(kOrange);
    gr_band_2sigma->SetLineColor(kOrange);
    gr_band_2sigma->SetMarkerColor(kOrange);


    //==== 13 TeV T added

    string elline_SandT;
    ifstream in_SandT("Limits/MuMu_Combined/result_VBF.txt");

    int n_SandT = 29; //30, but now removing 80 GeV
    //if(WhichDirectoryInCutop.Contains("Bin1")) n_SandT = n_SandT-1;
    double mass_SandT[n_SandT], obs_SandT[n_SandT], limit_SandT[n_SandT], onesig_left_SandT[n_SandT], onesig_right_SandT[n_SandT], twosig_left_SandT[n_SandT], twosig_right_SandT[n_SandT];
    dummyint=0;

    double max_obs_SandT = 0., max_obs_mass_SandT = 0.;
    double min_obs_SandT = 9999., min_obs_mass_SandT = 0.;
    while(getline(in_SandT,elline_SandT)){
      std::istringstream is( elline_SandT );

      is >> mass_SandT[dummyint];
      is >> obs_SandT[dummyint];
      is >> limit_SandT[dummyint];
      is >> onesig_left_SandT[dummyint];
      is >> onesig_right_SandT[dummyint];
      is >> twosig_left_SandT[dummyint];
      is >> twosig_right_SandT[dummyint];

      //==== skip points
      if(obs_SandT[dummyint]<=0 || limit_SandT[dummyint]<=0 || onesig_left_SandT[dummyint]<=0 || onesig_right_SandT[dummyint]<=0 || twosig_left_SandT[dummyint]<=0 || twosig_right_SandT[dummyint]<=0){
        n_SandT--;
        continue;
      }

      double scale=0.01; //mixing squared is 0.01 now
      if(mass_SandT[dummyint]<=60) scale *= 0.01;
      else if(mass_SandT[dummyint]<=100) scale *= 0.1;
      else if(mass_SandT[dummyint]<=300) scale *= 1.;
      else if(mass_SandT[dummyint]<=700) scale *= 10.;
      else scale *= 100.;

      scale *= 0.01; //FIXME

      if(channel=="MuEl") scale *= 0.5;

      obs_SandT[dummyint] *= scale;
      limit_SandT[dummyint] *= scale;
      onesig_left_SandT[dummyint] *= scale;
      onesig_right_SandT[dummyint] *= scale;
      twosig_left_SandT[dummyint] *= scale;
      twosig_right_SandT[dummyint] *= scale;

      //==== skip points
      if(obs_SandT[dummyint]>1.0 || limit_SandT[dummyint]>1.0){
        //n_SandT--;
        //continue;
      }

      cout << mass_SandT[dummyint] << "\t" << obs_SandT[dummyint] << endl;

      onesig_left_SandT[dummyint] = limit_SandT[dummyint]-onesig_left_SandT[dummyint];
      onesig_right_SandT[dummyint] = onesig_right_SandT[dummyint] - limit_SandT[dummyint];
      twosig_left_SandT[dummyint] = limit_SandT[dummyint]-twosig_left_SandT[dummyint];
      twosig_right_SandT[dummyint] = twosig_right_SandT[dummyint] - limit_SandT[dummyint];

      if(max_obs_SandT<obs_SandT[dummyint] && obs_SandT[dummyint]<1.){
        max_obs_SandT = obs_SandT[dummyint];
        max_obs_mass_SandT = mass_SandT[dummyint];
      }
      if(min_obs_SandT>obs_SandT[dummyint]){
        min_obs_SandT = obs_SandT[dummyint];
        min_obs_mass_SandT = mass_SandT[dummyint];
      }

      dummyint++;
    }
    cout << "Max : " << max_obs_mass_SandT << "\t" << max_obs_SandT << endl;
    cout << "Min : " << min_obs_mass_SandT << "\t" << min_obs_SandT << endl;

    //TGraph *gr_13TeV_obs_SandT = new TGraph(n_SandT,mass_SandT,obs_SandT);
    TGraphAsymmErrors *gr_13TeV_obs_SandT = new TGraphAsymmErrors(n_SandT,mass_SandT,obs_SandT,0,0,0,0);
    gr_13TeV_obs_SandT->SetLineWidth(3);
    gr_13TeV_obs_SandT->SetLineColor(kBlack);

    //TGraph *gr_13TeV_exp_SandT = new TGraph(n_SandT,mass_SandT,limit_SandT);
    TGraphAsymmErrors *gr_13TeV_exp_SandT = new TGraphAsymmErrors(n_SandT,mass_SandT,limit_SandT,0,0,0,0);
    gr_13TeV_exp_SandT->SetLineColor(kBlack);
    gr_13TeV_exp_SandT->SetLineWidth(3);
    gr_13TeV_exp_SandT->SetLineStyle(2);

    TGraphAsymmErrors *gr_band_1sigma_SandT = new TGraphAsymmErrors(n_SandT, mass_SandT, limit_SandT, 0, 0, onesig_left_SandT, onesig_right_SandT);
    gr_band_1sigma_SandT->SetFillColor(kGreen+1);
    gr_band_1sigma_SandT->SetLineColor(kGreen+1);
    gr_band_1sigma_SandT->SetMarkerColor(kGreen+1);

    TGraphAsymmErrors *gr_band_2sigma_SandT = new TGraphAsymmErrors(n_SandT, mass_SandT, limit_SandT, 0, 0, twosig_left_SandT, twosig_right_SandT);
    gr_band_2sigma_SandT->SetFillColor(kOrange);
    gr_band_2sigma_SandT->SetLineColor(kOrange);
    gr_band_2sigma_SandT->SetMarkerColor(kOrange);


    //=== EXO-17-028 overlay
    const int nm_17028 = 19;
    double mass_17028[nm_17028] = {
      100, 125, 150,200,
      250, 300, 400, 500,
      600, 700, 800, 900,
      1000, 1100, 1200, 1300,
      1400, 1500, 1700
    };

    
    double obs_17028[nm_17028], exp_17028[nm_17028];
    vector<double> tempvec_obs_17028, tempvec_exp_17028;
    vector<double> scales_17028;
    if(channel=="MuMu"){
      tempvec_exp_17028 = {
        175.333, 21.5041, 32.925, 56.3397,
        70.8081, 99.3095, 20.4264, 42.5126,
        60.1695, 116.721, 15.8605, 25.8407,
        38.43, 64.346, 100.265, 151.699,
        247.709, 340.424, 1340.34
      } ;
      scales_17028 = {
        0.001, 0.01, 0.01,0.01,0.01,0.01,0.1, 0.1,0.1,0.1,1,1,1,1,1,1,1,1,1,1
      };
      tempvec_obs_17028 = {
        215.218, 23.0424,41.8101,49.4399,57.1134,84.404,39.6932,
        44.5303,81.4561,195.31,16.3137,42.605,61.6358,103.589,150.295,
        220.286, 365.037, 516.2, 1408.5

      };
    }
    else   if(channel=="EE"){
      //https://github.com/jedori0228/HiggsAnalysis-CombinedLimit/blob/2016Data_HNDilepton_Limit/data/2016_HNDiLepton/Outputs_Tool/EE_Combined/result.txt
      tempvec_exp_17028 = {
        467.448, 65.4099, 90.4068, 159.838,216.957, 284.563, 59.74, 94.6793, 
        104.302, 183.121, 30.189, 47.1442, 72.0759, 117.305, 183.214,
        285.811, 434.08, 644.258, 2506.94
      };
      scales_17028 = {
        0.001, 0.01, 0.01,0.01,0.01,0.01,0.1, 0.1,0.1,0.1,1,1,1,1,1,1,1,1,1,1
      };
      tempvec_obs_17028 = {
        368.924, 63.3389, 61.9159, 151.2,
        206.654, 254.261, 68.8604, 95.9664, 
        123.0, 274.57, 24.8148, 46.0243,
        95.1426, 164.011, 252.706, 379.988,
        419.316, 631.767, 2486.31
        
      };
    }
    cout << "Channel " << channel << endl;
    for(unsigned int j=0; j<tempvec_obs_17028.size(); j++){
      
      obs_17028[j] = scales_17028[j]*tempvec_obs_17028.at(j)*0.01;
      exp_17028[j] = scales_17028[j]*tempvec_exp_17028.at(j)*0.01;
      cout << "mN = " << mass_17028[j] << " obs limit = " <<  scales_17028[j]*tempvec_obs_17028.at(j)*0.01 << endl;
    }

    TGraph *gr_17028_exp = new TGraph(nm_17028, mass_17028, exp_17028);
    gr_17028_exp->SetLineColor(kRed);
    gr_17028_exp->SetLineWidth(3);
    TGraph *gr_17028_obs = new TGraph(nm_17028, mass_17028, obs_17028);
    gr_17028_obs->SetLineColor(kRed);
    gr_17028_obs->SetLineWidth(3);

    //==== 8 TeV overlay

    const int nm = 16;
    double mass_8TeV[nm] = {
      40, 50, 60, 70, 80,
      90, 100, 125, 150, 175,
      200, 250, 300, 350, 400, 500
    };
    double obs_8TeV[nm], exp_8TeV[nm];

    vector<double> tempvec_obs_8TeV, tempvec_exp_8TeV;
    if(channel=="EE"){
      tempvec_obs_8TeV = {
        0.000153022, 0.000158927, 0.000330048, 0.00240212, 0.00732196,
        0.0219599, 0.0109256, 0.00787703, 0.00797621, 0.0113701,
        0.0158563, 0.0417892, 0.08102, 0.139453, 0.237897, 0.722283,
      };
      tempvec_exp_8TeV = {
        0.000117471, 0.000119376, 0.00025116, 0.00185047, 0.00558829,
        0.0164049, 0.00765044, 0.0076666, 0.0100238, 0.0143538,
        0.0202162, 0.0414845, 0.0692952, 0.111788, 0.192697, 0.58519,
      };
    }
    if(channel=="MuMu"){
      tempvec_obs_8TeV = {
        2.09584e-05, 2.58344e-05, 6.25064e-05, 0.000393122, 0.0010261,
        0.00513292, 0.00240843, 0.00182402, 0.00346005, 0.00833979,
        0.0125927, 0.0205839, 0.0403864, 0.0754627, 0.151591, 0.526906, 
      };
      tempvec_exp_8TeV = {
        2.82635E-05, 3.69206E-05, 8.52678E-05, 0.000618594, 0.00148793,
        0.00583953, 0.00257802, 0.00290533, 0.00449771, 0.00722055,
        0.0108741, 0.0194395, 0.0400305, 0.0708397, 0.149737, 0.497138
      };
    }
    if(channel=="MuEl"){
      tempvec_obs_8TeV = {
        6.64339e-05, 7.96033e-05, 0.0001717, 0.00135852, 0.00335107,
        0.00860876, 0.00485913, 0.0048582, 0.00523195, 0.00763538,
        0.00929436, 0.0205983, 0.0367042, 0.0716093, 0.132311, 0.455058, 
      };
      tempvec_exp_8TeV = {
        6.66795e-05, 8.00154e-05, 0.000171178, 0.00135744, 0.00288853,
        0.00703366, 0.0034261, 0.00332376, 0.00448255, 0.00653659,
        0.00795478, 0.0162876, 0.0247572, 0.0466464, 0.0847838, 0.285325,
      };
    }

    for(unsigned int j=0; j<tempvec_obs_8TeV.size(); j++){
      obs_8TeV[j] = tempvec_obs_8TeV.at(j);
      exp_8TeV[j] = tempvec_exp_8TeV.at(j);
    }

    TGraph *gr_8TeV_exp = new TGraph(nm, mass_8TeV, obs_8TeV);
    gr_8TeV_exp->SetLineColor(kRed);
    //gr_8TeV_exp->SetLineStyle(10);
    gr_8TeV_exp->SetLineWidth(3);

    //==== 8 and 13 TeV Combined
    //==== 8 TeV overlay

    const int nm8and13 = 28;
    double mass_8and13TeV[nm8and13] = {
      20, 30, 40, 50, 60, 70, 80, 
      90, 100, 125, 150, 200, 
      250, 300, 400, 500,
      600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1700, 2000,
    };
    double obs_8and13TeV[nm8and13], exp_8and13TeV[nm8and13];

    vector<double> tempvec_obs_8and13TeV, tempvec_exp_8and13TeV;
    if(channel=="EE"){
      tempvec_obs_8and13TeV = {
        0.00010476, 8.244e-05, 8.16e-05, 0.00010183, 0.000225, 0.0016379, 0.0043771, 0.0083341, 0.0039405, 0.004687, 0.004088, 0.008342, 0.019262, 0.022621, 0.03489, 0.0912, 0.08728, 0.16916, 0.1243, 0.177, 0.4212, 0.6272, 0.8493, 1.1492, 0.8259, 1.0344, 2.169, 4.3526, 
      };
      tempvec_exp_8and13TeV = {

      };
    }
    if(channel=="MuMu"){
      tempvec_obs_8and13TeV = {
        3.783e-05, 2.8e-05, 1.553e-05, 1.775e-05, 4.376e-05, 0.0003474, 0.0008412, 0.0023593, 0.0015521, 0.001285, 0.002622, 0.004085, 0.005141, 0.00714, 0.03481, 0.03547, 0.06339, 0.11797, 0.0802, 0.204, 0.2644, 0.3766, 0.4724, 0.6004, 0.878, 1.0681, 1.0893, 2.1158,
      };
      tempvec_exp_8and13TeV = {

      };
    }
    if(channel=="MuEl"){
      tempvec_obs_8and13TeV = {
        4.2565e-05, 3.68e-05, 2.524e-05, 3.843e-05, 0.000102995, 0.0007555, 0.0019562, 0.00209275, 0.00159395, 0.001789, 0.002613, 0.0071055, 0.0083965, 0.0128815, 0.02217, 0.022245, 0.06913, 0.0654, 0.1086, 0.0763, 0.10995, 0.13505, 0.1744, 0.2324, 0.31395, 0.4463, 1.1073, 1.77645, 
      };
      tempvec_exp_8and13TeV = {

      };
    }

    for(unsigned int j=0; j<tempvec_obs_8and13TeV.size(); j++){
      obs_8and13TeV[j] = tempvec_obs_8and13TeV.at(j);
      //exp_8and13TeV[j] = tempvec_exp_8and13TeV.at(j);
    }

    TGraph *gr_8and13TeV_obs = new TGraph(nm8and13, mass_8and13TeV, obs_8and13TeV);
    gr_8and13TeV_obs->SetLineColor(kRed);
    gr_8and13TeV_obs->SetLineWidth(2);

//  ======================================
    //==== LEP (L3)

    float L3[2][38];
    float L3_2[2][224];
    float DEL[2][39];
    float CMS[2][8];
 
    L3[0][0]  = 20.75; L3[1][0]  = 1.53e-4;
    L3[0][1]  = 23.75; L3[1][1]  = 1.56e-4;
    L3[0][2]  = 26.37; L3[1][2]  = 1.59e-4;
    L3[0][3]  = 29.30; L3[1][3]  = 1.64e-4;
    L3[0][4]  = 32.54; L3[1][4]  = 1.69e-4;
    L3[0][5]  = 35.61; L3[1][5]  = 1.75e-4;
    L3[0][6]  = 39.55; L3[1][6]  = 1.84e-4;
    L3[0][7]  = 43.61; L3[1][7]  = 1.98e-4;
    L3[0][8]  = 48.45; L3[1][8]  = 2.20e-4;
    L3[0][9]  = 52.23; L3[1][9]  = 2.44e-4;
    L3[0][10] = 55.90; L3[1][10] = 2.76e-4;
    L3[0][11] = 59.82; L3[1][11] = 3.13e-4;
    L3[0][12] = 62.12; L3[1][12] = 3.50e-4;
    L3[0][13] = 64.03; L3[1][13] = 4.02e-4;
    L3[0][14] = 66.49; L3[1][14] = 4.56e-4;
    L3[0][15] = 69.05; L3[1][15] = 5.28e-4;
    L3[0][16] = 71.19; L3[1][16] = 6.49e-4;
    L3[0][17] = 72.28; L3[1][17] = 7.25e-4;
    L3[0][18] = 74.51; L3[1][18] = 8.78e-4;
    L3[0][19] = 76.24; L3[1][19] = 1.06e-3;
    L3[0][20] = 78.02; L3[1][20] = 1.35e-3;
    L3[0][21] = 79.20; L3[1][21] = 1.63e-3;
    L3[0][22] = 80.46; L3[1][22] = 2.03e-3;
    L3[0][23] = 81.71; L3[1][23] = 2.46e-3;
    L3[0][24] = 83.00; L3[1][24] = 3.23e-3;
    L3[0][25] = 84.30; L3[1][25] = 4.18e-3;
    L3[0][26] = 84.98; L3[1][26] = 5.49e-3;
    L3[0][27] = 85.67; L3[1][27] = 6.95e-3;
    L3[0][28] = 86.36; L3[1][28] = 8.80e-3;
    L3[0][29] = 87.40; L3[1][29] = 1.23e-2;
    L3[0][30] = 88.44; L3[1][30] = 1.62e-2;
    L3[0][31] = 89.17; L3[1][31] = 2.28e-2;
    L3[0][32] = 89.90; L3[1][32] = 3.03e-2;
    L3[0][33] = 90.20; L3[1][33] = 3.76e-2;
    L3[0][34] = 90.68; L3[1][34] = 4.75e-2;
    L3[0][35] = 90.72; L3[1][35] = 6.38e-2;
    L3[0][36] = 90.78; L3[1][36] = 8.69e-2;
    L3[0][37] = 90.81; L3[1][37] = 9.93e-2;

    L3_2[0][0] = 8.07360406091370e+001;   L3_2[1][0] =    1.64216866767426e-003;
    L3_2[0][1] = 8.47563451776650e+001;   L3_2[1][1] =   2.48527439290502e-003;
    L3_2[0][2] = 8.53654822335025e+001;   L3_2[1][2] =   2.73626821837528e-003;
    L3_2[0][3] = 8.58527918781726e+001;   L3_2[1][3] =   2.75651933220772e-003;
    L3_2[0][4] = 8.63401015228426e+001;   L3_2[1][4] =   2.73610368475080e-003;
    L3_2[0][5] = 8.68274111675127e+001;   L3_2[1][5] =   2.65618155791328e-003;
    L3_2[0][6] = 8.85329949238579e+001;   L3_2[1][6] =   2.29035801398706e-003;
    L3_2[0][7] = 8.91421319796954e+001;   L3_2[1][7] =   2.20703835870127e-003;
    L3_2[0][8] = 8.96294416243655e+001;   L3_2[1][8] =   2.23989516299269e-003;
    L3_2[0][9] = 9.02385786802030e+001;   L3_2[1][9] =   2.37648371479660e-003;
    L3_2[0][10] = 9.06040609137056e+001;   L3_2[1][10] =   2.41188122901001e-003;
    L3_2[0][11] = 9.10913705583756e+001;   L3_2[1][11] =   2.34142970388094e-003;
    L3_2[0][12] = 9.25532994923858e+001;   L3_2[1][12] =   2.04910464264994e-003;
    L3_2[0][13] = 9.43807106598985e+001;   L3_2[1][13] =   1.74090720011271e-003;
    L3_2[0][14] = 9.46243654822335e+001;   L3_2[1][14] =   1.74088102904615e-003;
    L3_2[0][15] = 9.49898477157360e+001;   L3_2[1][15] =   1.76681129761304e-003;
    L3_2[0][16] = 9.64517766497462e+001;   L3_2[1][16] =   1.90241532453007e-003;
    L3_2[0][17] = 9.69390862944162e+001;   L3_2[1][17] =   2.07911009477572e-003;
    L3_2[0][18] = 9.75482233502538e+001;   L3_2[1][18] =   2.34049711644839e-003;
    L3_2[0][19] = 9.81573604060914e+001;   L3_2[1][19] =   2.41075748993192e-003;
    L3_2[0][20] = 9.94974619289340e+001;   L3_2[1][20] =   2.39277676176929e-003;
    L3_2[0][21] = 1.00228426395939e+002;   L3_2[1][21] =   2.22191916533212e-003;
    L3_2[0][22] = 1.00472081218274e+002;   L3_2[1][22] =   2.18922731423832e-003;
    L3_2[0][23] = 1.00837563451777e+002;   L3_2[1][23] =   2.23834675845749e-003;
    L3_2[0][24] = 1.01446700507614e+002;   L3_2[1][24] =   2.46440276951126e-003;
    L3_2[0][25] = 1.02421319796954e+002;   L3_2[1][25] =   2.65362722269690e-003;
    L3_2[0][26] = 1.03274111675127e+002;   L3_2[1][26] =   2.73324649183704e-003;
    L3_2[0][27] = 1.04005076142132e+002;   L3_2[1][27] =   2.89989775412225e-003;
    L3_2[0][28] = 1.04614213197970e+002;   L3_2[1][28] =   3.00914790101252e-003;
    L3_2[0][29] = 1.05223350253807e+002;   L3_2[1][29] =   2.87829038910166e-003;
    L3_2[0][30] = 1.05710659898477e+002;   L3_2[1][30] =   2.75314411524667e-003;
    L3_2[0][31] = 1.06197969543147e+002;   L3_2[1][31] =   2.69258601376476e-003;
    L3_2[0][32] = 1.06563451776650e+002;   L3_2[1][32] =   2.57553340959042e-003;
    L3_2[0][33] = 1.06928934010152e+002;   L3_2[1][33] =   2.28775993140507e-003;
    L3_2[0][34] = 1.07172588832487e+002;   L3_2[1][34] =   1.94385725892692e-003;
    L3_2[0][35] = 1.07659898477157e+002;   L3_2[1][35] =   1.72665021784635e-003;
    L3_2[0][36] = 1.08390862944162e+002;   L3_2[1][36] =   1.75232900484380e-003;
    L3_2[0][37] = 1.08878172588832e+002;   L3_2[1][37] =   1.75227631969861e-003;
    L3_2[0][38] = 1.09365482233503e+002;   L3_2[1][38] =   1.70109198371827e-003;
    L3_2[0][39] = 1.09730964467005e+002;   L3_2[1][39] =   1.75218412450604e-003;
    L3_2[0][40] = 1.10096446700508e+002;   L3_2[1][40] =   1.87287526805698e-003;
    L3_2[0][41] = 1.10218274111675e+002;   L3_2[1][41] =   2.00190976058399e-003;
    L3_2[0][42] = 1.10705583756345e+002;   L3_2[1][42] =   2.13978602197581e-003;
    L3_2[0][43] = 1.11314720812183e+002;   L3_2[1][43] =   2.04673407369398e-003;
    L3_2[0][44] = 1.11680203045685e+002;   L3_2[1][44] =   2.04668792102224e-003;
    L3_2[0][45] = 1.12167512690355e+002;   L3_2[1][45] =   2.15549295363718e-003;
    L3_2[0][46] = 1.12654822335025e+002;   L3_2[1][46] =   2.30394685288646e-003;
    L3_2[0][47] = 1.13873096446701e+002;   L3_2[1][47] =   2.33814091031860e-003;
    L3_2[0][48] = 1.14604060913706e+002;   L3_2[1][48] =   2.42620930950398e-003;
    L3_2[0][49] = 1.14969543147208e+002;   L3_2[1][49] =   2.59332757747740e-003;
    L3_2[0][50] = 1.15456852791878e+002;   L3_2[1][50] =   2.79253523521921e-003;
    L3_2[0][51] = 1.15822335025381e+002;   L3_2[1][51] =   2.73113121610214e-003;
    L3_2[0][52] = 1.16187817258883e+002;   L3_2[1][52] =   2.59313265580647e-003;
    L3_2[0][53] = 1.16553299492386e+002;   L3_2[1][53] =   2.51740566300458e-003;
    L3_2[0][54] = 1.16918781725888e+002;   L3_2[1][54] =   2.63169779218229e-003;
    L3_2[0][55] = 1.17162436548223e+002;   L3_2[1][55] =   2.83389547768448e-003;
    L3_2[0][56] = 1.17406091370558e+002;   L3_2[1][56] =   3.12016774116052e-003;
    L3_2[0][57] = 1.18015228426396e+002;   L3_2[1][57] =   3.64490099465068e-003;
    L3_2[0][58] = 1.18502538071066e+002;   L3_2[1][58] =   4.25791310694239e-003;
    L3_2[0][59] = 1.19111675126904e+002;   L3_2[1][59] =   5.04818725777358e-003;
    L3_2[0][60] = 1.19355329949239e+002;   L3_2[1][60] =   5.47644464689688e-003;
    L3_2[0][61] = 1.19598984771574e+002;   L3_2[1][61] =   5.51705873718600e-003;
    L3_2[0][62] = 1.19964467005076e+002;   L3_2[1][62] =   5.31643666005577e-003;
    L3_2[0][63] = 1.20208121827411e+002;   L3_2[1][63] =   4.97364986461281e-003;
    L3_2[0][64] = 1.20451776649746e+002;   L3_2[1][64] =   4.61864240777426e-003;
    L3_2[0][65] = 1.21182741116751e+002;   L3_2[1][65] =   4.35282572742742e-003;
    L3_2[0][66] = 1.22035532994924e+002;   L3_2[1][66] =   4.22558354508754e-003;
    L3_2[0][67] = 1.23010152284264e+002;   L3_2[1][67] =   4.35233498102418e-003;
    L3_2[0][68] = 1.23375634517767e+002;   L3_2[1][68] =   4.54993429494731e-003;
    L3_2[0][69] = 1.24106598984772e+002;   L3_2[1][69] =   4.65191575277598e-003;
    L3_2[0][70] = 1.24715736040609e+002;   L3_2[1][70] =   4.54955811215536e-003;
    L3_2[0][71] = 1.25081218274112e+002;   L3_2[1][71] =   4.31967810281806e-003;
    L3_2[0][72] = 1.25568527918782e+002;   L3_2[1][72] =   4.16256623322266e-003;
    L3_2[0][73] = 1.26055837563452e+002;   L3_2[1][73] =   4.35151719329958e-003;
    L3_2[0][74] = 1.26421319796954e+002;   L3_2[1][74] =   4.58288489149382e-003;
    L3_2[0][75] = 1.26664974619289e+002;   L3_2[1][75] =   4.61687221589291e-003;
    L3_2[0][76] = 1.27030456852792e+002;   L3_2[1][76] =   4.44898448115588e-003;
    L3_2[0][77] = 1.27517766497462e+002;   L3_2[1][77] =   4.10088941611898e-003;
    L3_2[0][78] = 1.28005076142132e+002;   L3_2[1][78] =   3.58911345708994e-003;
    L3_2[0][79] = 1.28248730964467e+002;   L3_2[1][79] =   3.16459603062618e-003;
    L3_2[0][80] = 1.28614213197970e+002;   L3_2[1][80] =   2.87413949588912e-003;
    L3_2[0][81] = 1.29223350253807e+002;   L3_2[1][81] =   2.68876356203647e-003;
    L3_2[0][82] = 1.29954314720812e+002;   L3_2[1][82] =   2.66880961425097e-003;
    L3_2[0][83] = 1.30685279187817e+002;   L3_2[1][83] =   2.81064532612032e-003;
    L3_2[0][84] = 1.31294416243655e+002;   L3_2[1][84] =   3.07167266322708e-003;
    L3_2[0][85] = 1.32147208121827e+002;   L3_2[1][85] =   3.18734630632389e-003;
    L3_2[0][86] = 1.32634517766497e+002;   L3_2[1][86] =   3.18725047625861e-003;
    L3_2[0][87] = 1.33487309644670e+002;   L3_2[1][87] =   3.43200320482984e-003;
    L3_2[0][88] = 1.34218274111675e+002;   L3_2[1][88] =   3.80666076160848e-003;
    L3_2[0][89] = 1.34827411167513e+002;   L3_2[1][89] =   4.06880391065743e-003;
    L3_2[0][90] = 1.35680203045685e+002;   L3_2[1][90] =   4.28501106805965e-003;
    L3_2[0][91] = 1.37385786802030e+002;   L3_2[1][91] =   4.75250216740549e-003;
    L3_2[0][92] = 1.38238578680203e+002;   L3_2[1][92] =   5.97830309169873e-003;
    L3_2[0][93] = 1.38604060913706e+002;   L3_2[1][93] =   6.43757759797191e-003;
    L3_2[0][94] = 1.38969543147208e+002;   L3_2[1][94] =   6.29602409744375e-003;
    L3_2[0][95] = 1.39335025380711e+002;   L3_2[1][95] =   5.89003237089811e-003;
    L3_2[0][96] = 1.39822335025381e+002;   L3_2[1][96] =   5.67580483455332e-003;
    L3_2[0][97] = 1.40553299492386e+002;   L3_2[1][97] =   5.84614527893421e-003;
    L3_2[0][98] = 1.41162436548223e+002;   L3_2[1][98] =   6.15688894579588e-003;
    L3_2[0][99] = 1.41893401015228e+002;   L3_2[1][99] =   6.29488841340989e-003;
    L3_2[0][100] = 1.42868020304569e+002;   L3_2[1][100] =   6.15624107922065e-003;
    L3_2[0][101] = 1.43598984771574e+002;   L3_2[1][101] =   5.71665115562675e-003;
    L3_2[0][102] = 1.44208121827411e+002;   L3_2[1][102] =   4.96629052236900e-003;
    L3_2[0][103] = 1.44573604060914e+002;   L3_2[1][103] =   4.64604510518223e-003;
    L3_2[0][104] = 1.44939086294416e+002;   L3_2[1][104] =   4.92943451049419e-003;
    L3_2[0][105] = 1.45304568527919e+002;   L3_2[1][105] =   5.38731682636837e-003;
    L3_2[0][106] = 1.45548223350254e+002;   L3_2[1][106] =   5.71596368423831e-003;
    L3_2[0][107] = 1.46035532994924e+002;   L3_2[1][107] =   5.63177810597449e-003;
    L3_2[0][108] = 1.46522842639594e+002;   L3_2[1][108] =   5.34717550725343e-003;
    L3_2[0][109] = 1.47010152284264e+002;   L3_2[1][109] =   4.67986761483261e-003;
    L3_2[0][110] = 1.47984771573604e+002;   L3_2[1][110] =   4.03551318835173e-003;
    L3_2[0][111] = 1.48593908629442e+002;   L3_2[1][111] =   3.94671845719036e-003;
    L3_2[0][112] = 1.49446700507614e+002;   L3_2[1][112] =   4.06513555676476e-003;
    L3_2[0][113] = 1.50055837563452e+002;   L3_2[1][113] =   4.74878848299695e-003;
    L3_2[0][114] = 1.50543147208122e+002;   L3_2[1][114] =   5.42559761962259e-003;
    L3_2[0][115] = 1.51395939086294e+002;   L3_2[1][115] =   5.11329981946695e-003;
    L3_2[0][116] = 1.51883248730964e+002;   L3_2[1][116] =   5.03799036581785e-003;
    L3_2[0][117] = 1.52614213197970e+002;   L3_2[1][117] =   5.26660019352337e-003;
    L3_2[0][118] = 1.53345177664975e+002;   L3_2[1][118] =   5.34492520873051e-003;
    L3_2[0][119] = 1.53954314720812e+002;   L3_2[1][119] =   5.71299991078399e-003;
    L3_2[0][120] = 1.54563451776650e+002;   L3_2[1][120] =   6.10642183118031e-003;
    L3_2[0][121] = 1.55294416243655e+002;   L3_2[1][121] =   5.79774589462011e-003;
    L3_2[0][122] = 1.55659898477157e+002;   L3_2[1][122] =   5.75484922508963e-003;
    L3_2[0][123] = 1.56025380710660e+002;   L3_2[1][123] =   6.47844986010003e-003;
    L3_2[0][124] = 1.56512690355330e+002;   L3_2[1][124] =   7.56801806481790e-003;
    L3_2[0][125] = 1.56878172588832e+002;   L3_2[1][125] =   8.97278684252325e-003;
    L3_2[0][126] = 1.57487309644670e+002;   L3_2[1][126] =   1.19760322830161e-002;
    L3_2[0][127] = 1.58340101522843e+002;   L3_2[1][127] =   1.34814638831120e-002;
    L3_2[0][128] = 1.59192893401015e+002;   L3_2[1][128] =   1.33813141819938e-002;
    L3_2[0][129] = 1.59680203045685e+002;   L3_2[1][129] =   1.29904433625631e-002;
    L3_2[0][130] = 1.60289340101523e+002;   L3_2[1][130] =   1.28941351413757e-002;
    L3_2[0][131] = 1.60898477157360e+002;   L3_2[1][131] =   1.31832411980912e-002;
    L3_2[0][132] = 1.61507614213198e+002;   L3_2[1][132] =   1.35789944950263e-002;
    L3_2[0][133] = 1.62116751269036e+002;   L3_2[1][133] =   1.34783228883051e-002;
    L3_2[0][134] = 1.62604060913706e+002;   L3_2[1][134] =   1.32798121088354e-002;
    L3_2[0][135] = 1.63335025380711e+002;   L3_2[1][135] =   1.34773098202910e-002;
    L3_2[0][136] = 1.63822335025381e+002;   L3_2[1][136] =   1.50598853570680e-002;
    L3_2[0][137] = 1.64187817258883e+002;   L3_2[1][137] =   1.67042872576638e-002;
    L3_2[0][138] = 1.64675126903553e+002;   L3_2[1][138] =   1.79874348120820e-002;
    L3_2[0][139] = 1.65406091370558e+002;   L3_2[1][139] =   1.73329496803663e-002;
    L3_2[0][140] = 1.66258883248731e+002;   L3_2[1][140] =   1.59764340313924e-002;
    L3_2[0][141] = 1.66989847715736e+002;   L3_2[1][141] =   1.41910104138897e-002;
    L3_2[0][142] = 1.67964467005076e+002;   L3_2[1][142] =   1.16190463265593e-002;
    L3_2[0][143] = 1.68451776649746e+002;   L3_2[1][143] =   1.06309534546901e-002;
    L3_2[0][144] = 1.68695431472081e+002;   L3_2[1][144] =   1.05523759102246e-002;
    L3_2[0][145] = 1.69182741116751e+002;   L3_2[1][145] =   1.17045109798434e-002;
    L3_2[0][146] = 1.69791878172589e+002;   L3_2[1][146] =   1.25105343053991e-002;
    L3_2[0][147] = 1.70401015228426e+002;   L3_2[1][147] =   1.22352608820488e-002;
    L3_2[0][148] = 1.70888324873096e+002;   L3_2[1][148] =   1.29814632719994e-002;
    L3_2[0][149] = 1.71131979695431e+002;   L3_2[1][149] =   1.47224300504785e-002;
    L3_2[0][150] = 1.71497461928934e+002;   L3_2[1][150] =   1.73264366974011e-002;
    L3_2[0][151] = 1.71862944162437e+002;   L3_2[1][151] =   1.83832771887633e-002;
    L3_2[0][152] = 1.72593908629442e+002;   L3_2[1][152] =   2.02396963375339e-002;
    L3_2[0][153] = 1.73324873096447e+002;   L3_2[1][153] =   2.34689190852153e-002;
    L3_2[0][154] = 1.73690355329949e+002;   L3_2[1][154] =   2.38184865540433e-002;
    L3_2[0][155] = 1.74299492385787e+002;   L3_2[1][155] =   2.14724580737784e-002;
    L3_2[0][156] = 1.74543147208122e+002;   L3_2[1][156] =   2.11565265075367e-002;
    L3_2[0][157] = 1.74908629441624e+002;   L3_2[1][157] =   2.19539031349350e-002;
    L3_2[0][158] = 1.75274111675127e+002;   L3_2[1][158] =   2.31211796982749e-002;
    L3_2[0][159] = 1.75761421319797e+002;   L3_2[1][159] =   2.56456085290872e-002;
    L3_2[0][160] = 1.76126903553299e+002;   L3_2[1][160] =   2.76157953889048e-002;
    L3_2[0][161] = 1.76370558375635e+002;   L3_2[1][161] =   3.01811814592575e-002;
    L3_2[0][162] = 1.76736040609137e+002;   L3_2[1][162] =   3.08583531944697e-002;
    L3_2[0][163] = 1.77345177664975e+002;   L3_2[1][163] =   2.97357743944966e-002;
    L3_2[0][164] = 1.77588832487310e+002;   L3_2[1][164] =   2.97353273764529e-002;
    L3_2[0][165] = 1.78197969543147e+002;   L3_2[1][165] =   3.20192196315258e-002;
    L3_2[0][166] = 1.78441624365482e+002;   L3_2[1][166] =   3.49936644689640e-002;
    L3_2[0][167] = 1.78685279187817e+002;   L3_2[1][167] =   3.57790822726035e-002;
    L3_2[0][168] = 1.79050761421320e+002;   L3_2[1][168] =   3.57782754749544e-002;
    L3_2[0][169] = 1.79538071065990e+002;   L3_2[1][169] =   3.52513276186468e-002;
    L3_2[0][170] = 1.80390862944162e+002;   L3_2[1][170] =   3.52494728866610e-002;
    L3_2[0][171] = 1.80756345177665e+002;   L3_2[1][171] =   3.34683880084021e-002;
    L3_2[0][172] = 1.81243654822335e+002;   L3_2[1][172] =   2.99495448280725e-002;
    L3_2[0][173] = 1.81609137055838e+002;   L3_2[1][173] =   2.86475725983867e-002;
    L3_2[0][174] = 1.82218274111675e+002;   L3_2[1][174] =   3.20112783628315e-002;
    L3_2[0][175] = 1.82705583756345e+002;   L3_2[1][175] =   3.39635777579971e-002;
    L3_2[0][176] = 1.82949238578680e+002;   L3_2[1][176] =   3.42154564680990e-002;
    L3_2[0][177] = 1.83436548223350e+002;   L3_2[1][177] =   3.37115260466601e-002;
    L3_2[0][178] = 1.84411167512690e+002;   L3_2[1][178] =   3.17708493064151e-002;
    L3_2[0][179] = 1.85873096446701e+002;   L3_2[1][179] =   2.90672832608436e-002;
    L3_2[0][180] = 1.86360406091371e+002;   L3_2[1][180] =   2.82182221991073e-002;
    L3_2[0][181] = 1.86604060913706e+002;   L3_2[1][181] =   2.82177979944333e-002;
    L3_2[0][182] = 1.86969543147208e+002;   L3_2[1][182] =   3.08388756590325e-002;
    L3_2[0][183] = 1.87335025380711e+002;   L3_2[1][183] =   3.37034183922107e-002;
    L3_2[0][184] = 1.87578680203046e+002;   L3_2[1][184] =   3.57594553603469e-002;
    L3_2[0][185] = 1.87944162436548e+002;   L3_2[1][185] =   3.57586490052733e-002;
    L3_2[0][186] = 1.88553299492386e+002;   L3_2[1][186] =   3.49718396264112e-002;
    L3_2[0][187] = 1.88796954314721e+002;   L3_2[1][187] =   3.57567675808119e-002;
    L3_2[0][188] = 1.89406091370558e+002;   L3_2[1][188] =   4.11561912958174e-002;
    L3_2[0][189] = 1.89771573604061e+002;   L3_2[1][189] =   4.23923137043059e-002;
    L3_2[0][190] = 1.90380710659898e+002;   L3_2[1][190] =   4.20780266387354e-002;
    L3_2[0][191] = 1.90624365482233e+002;   L3_2[1][191] =   4.30224499155085e-002;
    L3_2[0][192] = 1.91355329949239e+002;   L3_2[1][192] =   4.98866375797527e-002;
    L3_2[0][193] = 1.91842639593909e+002;   L3_2[1][193] =   5.13845919001389e-002;
    L3_2[0][194] = 1.92208121827411e+002;   L3_2[1][194] =   4.98840128178321e-002;
    L3_2[0][195] = 1.93426395939086e+002;   L3_2[1][195] =   4.39811274985747e-002;
    L3_2[0][196] = 1.93791878172589e+002;   L3_2[1][196] =   4.39801357495409e-002;
    L3_2[0][197] = 1.94644670050761e+002;   L3_2[1][197] =   5.37094165943240e-002;
    L3_2[0][198] = 1.95375634517767e+002;   L3_2[1][198] =   7.71946351078141e-002;
    L3_2[0][199] = 1.95741116751269e+002;   L3_2[1][199] =   8.56235840458290e-002;
    L3_2[0][200] = 1.96228426395939e+002;   L3_2[1][200] =   8.75440526286489e-002;
    L3_2[0][201] = 1.96715736040609e+002;   L3_2[1][201] =   9.01727523811539e-002;
    L3_2[0][202] = 1.97203045685279e+002;   L3_2[1][202] =   9.78209876472586e-002;
    L3_2[0][203] = 1.98177664974619e+002;   L3_2[1][203] =   1.14269425493516e-001;
    L3_2[0][204] = 1.98664974619289e+002;   L3_2[1][204] =   1.32502986799492e-001;
    L3_2[0][205] = 1.99274111675127e+002;   L3_2[1][205] =   1.59439233584269e-001;
    L3_2[0][206] = 1.99639593908629e+002;   L3_2[1][206] =   1.86255677804246e-001;
    L3_2[0][207] = 2.00248730964467e+002;   L3_2[1][207] =   2.30855798324400e-001;
    L3_2[0][208] = 2.00614213197970e+002;   L3_2[1][208] =   2.61814305867800e-001;
    L3_2[0][209] = 2.00857868020305e+002;   L3_2[1][209] =   2.73702931509858e-001;
    L3_2[0][210] = 2.01223350253807e+002;   L3_2[1][210] =   2.77779712405957e-001;
    L3_2[0][211] = 2.01588832487310e+002;   L3_2[1][211] =   2.86122800440038e-001;
    L3_2[0][212] = 2.01832487309645e+002;   L3_2[1][212] =   3.24495230396064e-001;
    L3_2[0][213] = 2.01954314720812e+002;   L3_2[1][213] =   3.46851805922331e-001;
    L3_2[0][214] = 2.02197969543147e+002;   L3_2[1][214] =   3.96291944782074e-001;
    L3_2[0][215] = 2.02441624365482e+002;   L3_2[1][215] =   4.59533733493136e-001;
    L3_2[0][216] = 2.02563451776650e+002;   L3_2[1][216] =   5.13506144309501e-001;
    L3_2[0][217] = 2.02685279187817e+002;   L3_2[1][217] =   5.48884904374619e-001;
    L3_2[0][218] = 2.02807106598985e+002;   L3_2[1][218] =   5.95453424610927e-001;
    L3_2[0][219] = 2.03050761421320e+002;   L3_2[1][219] =   7.00778579465140e-001;
    L3_2[0][220] = 2.03172588832487e+002;   L3_2[1][220] =   8.12617621404863e-001;
    L3_2[0][221] = 2.03294416243655e+002;   L3_2[1][221] =   8.81561765878811e-001;
    L3_2[0][222] = 2.03416243654822e+002;   L3_2[1][222] =   8.94706000334829e-001;
    L3_2[0][223] = 2.03416243654822e+002; L3_2[1][223] = 9.70621986828742e-001;

    DEL[0][0] = 10.1; DEL[1][0]   = 1.79e-5;
    DEL[0][1] = 11.2; DEL[1][1]   = 1.82e-5;
    DEL[0][2] = 12.7; DEL[1][2]   = 1.85e-5;
    DEL[0][3] = 15.1; DEL[1][3]   = 1.91e-5;
    DEL[0][4] = 17.8; DEL[1][4]   = 2.01e-5;
    DEL[0][5] = 19.8; DEL[1][5]   = 2.08e-5;
    DEL[0][6] = 21.8; DEL[1][6]   = 2.19e-5;
    DEL[0][7] = 23.5; DEL[1][7]   = 2.26e-5;
    DEL[0][8] = 25.5; DEL[1][8]   = 2.30e-5;
    DEL[0][9] = 27.4; DEL[1][9]   = 2.34e-5;
    DEL[0][10] = 29.6; DEL[1][10] = 2.37e-5;
    DEL[0][11] = 33.0; DEL[1][11] = 2.37e-5;
    DEL[0][12] = 36.0; DEL[1][12] = 2.41e-5;
    DEL[0][13] = 40.3; DEL[1][13] = 2.45e-5;
    DEL[0][14] = 44.5; DEL[1][14] = 2.53e-5;
    DEL[0][15] = 47.2; DEL[1][15] = 2.76e-5;
    DEL[0][16] = 50.7; DEL[1][16] = 3.05e-5;
    DEL[0][17] = 53.6; DEL[1][17] = 3.49e-5;
    DEL[0][18] = 56.0; DEL[1][18] = 4.07e-5;
    DEL[0][19] = 57.8; DEL[1][19] = 4.58e-5;
    DEL[0][20] = 59.4; DEL[1][20] = 5.25e-5;
    DEL[0][21] = 61.1; DEL[1][21] = 6.12e-5;
    DEL[0][22] = 62.8; DEL[1][22] = 7.25e-5;
    DEL[0][23] = 64.1; DEL[1][23] = 8.60e-5;
    DEL[0][24] = 65.6; DEL[1][24] = 1.00e-4;
    DEL[0][25] = 66.7; DEL[1][25] = 1.19e-4;
    DEL[0][26] = 67.8; DEL[1][26] = 1.41e-4;
    DEL[0][27] = 69.6; DEL[1][27] = 1.85e-4;
    DEL[0][28] = 70.8; DEL[1][28] = 2.30e-4;
    DEL[0][29] = 72.0; DEL[1][29] = 3.03e-4;
    DEL[0][30] = 73.2; DEL[1][30] = 3.84e-4;
    DEL[0][31] = 74.0; DEL[1][31] = 4.63e-4;
    DEL[0][32] = 75.2; DEL[1][32] = 5.77e-4;
    DEL[0][33] = 76.5; DEL[1][33] = 7.58e-4;
    DEL[0][34] = 76.9; DEL[1][34] = 8.98e-4;
    DEL[0][35] = 77.8; DEL[1][35] = 1.12e-3;
    DEL[0][36] = 78.2; DEL[1][36] = 1.33e-3;
    DEL[0][37] = 79.1; DEL[1][37] = 1.66e-3;
    DEL[0][38] = 79.9; DEL[1][38] = 2.03e-3;


    double massPointsAtlas_MuMu[25] = {100.237932 ,110.246164 ,119.409396 ,140.781448 ,160.210482 ,179.085100 ,199.904443 ,221.280479 ,239.880451 ,257.926575 ,282.358730 ,298.739614 ,324.006808 ,345.941813 ,365.100470 ,386.202713 ,409.248828 ,427.297514 ,442.847060 ,457.563558 ,471.447010 ,483.942430 ,491.994837 ,499.769752 ,499.769752};
    double limitsAtlas_MuMu[25] = {0.003474 ,0.002831 ,0.003084 ,0.004687 ,0.006876 ,0.009806 ,0.013886 ,0.019115 ,0.025217 ,0.031881 ,0.043279 ,0.052810 ,0.068711 ,0.086890 ,0.106042 ,0.132205 ,0.167192 ,0.198336 ,0.230308 ,0.265536 ,0.303980 ,0.340654 ,0.368393 ,0.395574 ,0.395574};

    double massPointsAtlas_EE[20] = {1.00455861406709e+002, 1.09809766214851e+002, 1.38752503310975e+002, 1.78574156906282e+002, 1.98797339797022e+002, 2.20886448743258e+002, 2.38308779169597e+002, 2.57287535385483e+002, 2.79378072245287e+002, 3.02092250356086e+002, 3.21384433600234e+002, 3.43787683531516e+002, 3.63702080113091e+002, 3.82682978199330e+002, 3.99174308979077e+002, 4.19400704675346e+002, 4.35581821232361e+002, 4.49584298662402e+002, 4.64520988544563e+002, 4.80079534785759e+002};
    double limitsAtlas_EE[20] = {4.04226688202133e-002, 2.87321017020558e-002, 3.33225809095133e-002, 5.51508368004247e-002, 6.92830498039127e-002, 9.05397993095326e-002, 1.11977313431971e-001, 1.38473609575320e-001, 1.75314576403352e-001, 2.16733719311297e-001, 2.55570350392377e-001, 3.13465143657095e-001, 3.72556547861380e-001, 4.39325988221587e-001, 5.10019175442642e-001, 5.96620239359251e-001, 6.76374403247621e-001, 7.60870825023857e-001, 8.49106552700366e-001, 9.62659703648251e-001};

    TGraph *gr_L3Limit = new TGraph(38, L3[0], L3[1]);
    gr_L3Limit->SetLineWidth(2);
    //gr_L3Limit->SetLineStyle(3);
    gr_L3Limit->SetLineColor(kViolet+1);

    TGraph *gr_L3_2Limit = new TGraph(224, L3_2[0], L3_2[1]);
    gr_L3_2Limit->SetLineWidth(2);
    //gr_L3_2Limit->SetLineStyle(3);
    gr_L3_2Limit->SetLineColor(kViolet);

    TGraph *gr_DELPHILimit = new TGraph(39, DEL[0], DEL[1]);
    gr_DELPHILimit->SetLineWidth(2);
    //gr_DELPHILimit->SetLineStyle(3);
    gr_DELPHILimit->SetLineColor(kMagenta);

    TGraph *gr_ATLAS_MuMu = new TGraph(25, massPointsAtlas_MuMu, limitsAtlas_MuMu);
    gr_ATLAS_MuMu->SetLineWidth(3);
    //gr_ATLAS_MuMu->SetLineStyle(3);
    gr_ATLAS_MuMu->SetLineColor(kBlue);

    TGraph *gr_ATLAS_EE = new TGraph(20, massPointsAtlas_EE, limitsAtlas_EE);
    gr_ATLAS_EE->SetLineWidth(3);
    //gr_ATLAS_EE->SetLineStyle(3);
    gr_ATLAS_EE->SetLineColor(kBlue);

//  =======================================

//  =======================================

    int temp_n_mass_trilep = 31;
    vector<double> temp_mass_trilep = {
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 30, 40, 50, 60, 70, 75, 85, 90, 95, 100, 130, 150, 200, 400, 600, 800, 1000, 1200,
    };
    vector<double> tmpvec_obs_trilep = {
      0.0163199, 0.00182936, 0.00059415, 0.000280499, 0.000149561, 0.000103852, 6.81653E-05, 4.97358E-05, 3.52154E-05, 3.12335E-05, 2.46796E-05, 2.13769E-05, 1.48506E-05, 1.76593E-05, 1.87597E-05, 1.80473E-05, 2.77739E-05, 0.000156184, 0.000742155, 0.00241651, 0.00289491, 0.00345643, 0.00431929, 0.00716543, 0.00796569, 0.00888232, 0.0301448, 0.0835229, 0.20645, 0.441043, 0.847844,
    };

    if(channel=="EE"){
      temp_n_mass_trilep = 30;
      temp_mass_trilep = {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 30, 40, 50, 60, 70, 75, 85, 90, 100, 130, 150, 200, 400, 600, 800, 1000, 1200,
      };
      tmpvec_obs_trilep = {
        0.0135784, 0.00151879, 0.000447416, 0.000223742, 0.00011303, 7.23346E-05, 5.10346E-05, 3.77547E-05, 2.72229E-05, 2.33201E-05, 1.8688E-05, 1.75216E-05, 1.20661E-05, 1.60735E-05, 2.19737E-05, 3.32274E-05, 6.70456E-05, 0.000564676, 0.00186338, 0.00629086, 0.00622036, 0.00652451, 0.010974, 0.014264, 0.0135633, 0.0523753, 0.167425, 0.428148, 0.949388, 1.83977,
      };
    }

    const int n_mass_trilep = temp_n_mass_trilep;
    double mass_trilep[n_mass_trilep];
    double obs_trilep[n_mass_trilep];
    for(unsigned int i=0; i<tmpvec_obs_trilep.size(); i++){
      mass_trilep[i] = temp_mass_trilep.at(i);
      obs_trilep[i] = tmpvec_obs_trilep.at(i);
      //cout << i << "\t" << temp_mass_trilep[i] << "\t" << obs_trilep[i] << endl;
    }
    TGraph *gr_trilepLimit = new TGraph(n_mass_trilep, mass_trilep, obs_trilep);
    gr_trilepLimit->SetLineWidth(3);
    gr_trilepLimit->SetLineStyle(4);
    gr_trilepLimit->SetLineColor(kRed);

//  =======================================

    //==== Double beta decay
    double allxrange[2]= {0.,999999.};
    double dbeta_ee[2];
    for(int i=0; i<2; i++){
      dbeta_ee[i] = 5e-8*allxrange[i];
    }
    TGraph *gr_dbeta = new TGraph(2, allxrange, dbeta_ee);
    gr_dbeta->SetLineColor(kViolet);

    //==== EWPD
    double EWPD_ee[2], EWPD_mm[2];
    for(int i=0; i<2; i++){
      //==== https://journals.aps.org/prd/pdf/10.1103/PhysRevD.78.013010
      //==== 90% CL
      EWPD_ee[i] = 0.003;
      EWPD_mm[i] = 0.003;
      //==== https://www.epj-conferences.org/articles/epjconf/pdf/2013/21/epjconf_lhcp2013_19008.pdf
      //==== 95% CL
      EWPD_ee[i] = 0.041*0.041;
      EWPD_mm[i] = 0.030*0.030;
    }
    TGraph *gr_EWPD_ee = new TGraph(2, allxrange, EWPD_ee);
    TGraph *gr_EWPD_mm = new TGraph(2, allxrange, EWPD_mm);
    gr_EWPD_ee->SetLineColor(kCyan);
    gr_EWPD_mm->SetLineColor(kCyan);
    gr_EWPD_ee->SetLineStyle(2);
    gr_EWPD_mm->SetLineStyle(2);
    gr_EWPD_ee->SetLineWidth(3);
    gr_EWPD_mm->SetLineWidth(3);


    //======================
    //==== S-ch only limit
    //======================

    //=== Legend
    cout << "S-ch only limit  " << endl;
    TLegend *lg = new TLegend(0.48, 0.15, 0.66, 0.45);
    lg->SetBorderSize(0);
    lg->SetFillStyle(0);
    TH1D *hist_emptylegend = new TH1D("hist_emptylegend","",1,0.,1.);
    hist_emptylegend->SetLineColor(0);

    if(DrawObserved) lg->AddEntry(gr_13TeV_obs,"Observed", "l");
    lg->AddEntry(gr_13TeV_exp,"Expected", "l");
    lg->AddEntry(gr_band_1sigma,"68% expected", "f");
    lg->AddEntry(gr_band_2sigma,"95% expected", "f");
    lg->AddEntry(hist_emptylegend,"","l");

    TLegend *lg_Alt = new TLegend(0.65, 0.15, 0.93, 0.48);
    lg_Alt->SetBorderSize(0);
    lg_Alt->SetFillStyle(0);
    if(channel=="MuMu"){
      //lg_Alt->AddEntry(gr_DELPHILimit, "DELPHI prompt", "l");
      //lg_Alt->AddEntry(gr_L3Limit, "L3", "l");

      //lg_Alt->AddEntry(gr_EWPD_mm, "EWPD (90% CL)", "l");
      lg_Alt->AddEntry(gr_EWPD_mm, "EWPD", "l");

      //lg_Alt->AddEntry(gr_ATLAS_MuMu, "ATLAS 8 TeV", "l");
      //lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton", "l");
      lg_Alt->AddEntry(gr_17028_obs, "CMS 13 TeV dilepton", "l");
      lg_Alt->AddEntry(gr_trilepLimit, "CMS 13 TeV trilepton", "l");
    }
    if(channel=="EE"){
      //lg_Alt->AddEntry(gr_DELPHILimit, "DELPHI prompt", "l");
      //lg_Alt->AddEntry(gr_L3_2Limit, "L3", "l");

      //lg_Alt->AddEntry(gr_EWPD_ee, "EWPD (90% CL)", "l");
      lg_Alt->AddEntry(gr_EWPD_ee, "EWPD", "l");

      //lg_Alt->AddEntry(gr_ATLAS_EE, "ATLAS 8 TeV", "l");
      //lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton", "l");
      lg_Alt->AddEntry(gr_17028_obs, "CMS 13 TeV dilepton", "l");
      lg_Alt->AddEntry(gr_trilepLimit, "CMS 13 TeV trilepton", "l");
      //lg_Alt->AddEntry(gr_dbeta, "Neutrino-less double beta dacay", "l");
    }
    if(channel=="MuEl"){
      lg_Alt->AddEntry(gr_8TeV_exp, "CMS 8 TeV", "l");
      lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
    }

    TLegend *lg_Alt_SandT = (TLegend *)lg_Alt->Clone();

    TCanvas *c_SOnly = new TCanvas("c_SOnly", "", 900, 800);
    canvas_margin(c_SOnly);
    c_SOnly->cd();
    c_SOnly->Draw();
    c_SOnly->SetLogy();

    TH1D *dummy = new TH1D("hist", "", 100000, 0., 100000.);
    //dummy->Draw("hist");
    hist_axis(dummy);
    dummy->GetYaxis()->SetTitleSize(0.06);
    if(channel=="EE") dummy->GetYaxis()->SetTitle("#||{V_{eN}}^{2}");
    if(channel=="MuMu") dummy->GetYaxis()->SetTitle("#||{V_{#muN}}^{2}");
    if(channel=="MuEl"){
      dummy->GetYaxis()->SetTitle("#frac{#||{ V_{eN}V_{#muN}^{*}}^{2}}{#||{ V_{eN} }^{2} + #||{ V_{#muN} }^{2}}");
      //dummy->GetYaxis()->SetTitle("#||{ V_{eN}V_{#muN}^{*}}^{2}#/#(){#||{ V_{eN} }^{2} + #||{ V_{#muN} }^{2}}");
      dummy->GetYaxis()->SetTitleOffset(1.95);
      dummy->GetYaxis()->SetTitleSize(0.04);
    }
    dummy->GetXaxis()->SetTitle("m_{N} (GeV)");
    //dummy->GetXaxis()->SetRangeUser(20., 1500);
    dummy->GetXaxis()->SetRangeUser(90., 25000); //JH
    dummy->GetYaxis()->SetRangeUser(1e-4, 1.);
    dummy->SetTitle("");
    dummy->Draw("hist");

    gr_band_2sigma->Draw("3same");
    gr_band_1sigma->Draw("3same");
    cout << "Drawing gr_13TeV_exp" << endl;
    gr_13TeV_exp->Draw("lsame");
    //gr_17028_exp->Draw("lsame");
    gr_17028_obs->Draw("lsame");
    //gr_8and13TeV_obs->Draw("lsame");
    if(channel=="MuMu"){
      //gr_L3Limit->Draw("lsame");
      //gr_DELPHILimit->Draw("lsame");
      gr_trilepLimit->Draw("lsame");
      gr_EWPD_mm->Draw("lsame");
      //gr_ATLAS_MuMu->Draw("lsame");
    }
    if(channel=="EE"){
      //gr_L3_2Limit->Draw("lsame");
      //gr_DELPHILimit->Draw("lsame");
      gr_trilepLimit->Draw("lsame");
      //gr_dbeta->Draw("lsame");
      gr_EWPD_ee->Draw("lsame");
      //gr_ATLAS_EE->Draw("lsame");
    }

    if(DrawObserved) gr_13TeV_obs->Draw("lsame");

    lg->Draw();
    lg_Alt->Draw();

    latex_Lumi.SetTextSize(0.035);
    latex_Lumi.SetTextFont(42);
    TString lumi = "36.5";
    if(j==1) lumi = "41.5";
    if(j==2) lumi = "59.9";
    if(j==3) lumi = "137.9";
    

    //latex_Lumi.DrawLatex(0.735, 0.96, "35.9 fb^{-1} (13 TeV)");
    latex_Lumi.DrawLatex(0.735, 0.96, lumi+" fb^{-1} (13 TeV)"); //JH
    latex_title.SetTextSize(0.04);
    latex_title.SetLineWidth(2);
    latex_title.DrawLatex(0.25, 0.84, "#font[41]{95% CL upper limit}");
    latex_title.SetTextSize(0.05);
    latex_title.DrawLatex(0.25, 0.88, "#font[62]{CMS}");

    c_SOnly->SetLogx();
    dummy->Draw("axissame");
    //  c_SOnly->SaveAs(plotpath+"/"+channel+"_13TeV_mixing_logx.pdf");
    //c_SOnly->SaveAs(plotpath+"/"+channel+"_13TeV_mixing_logx.png");

    //==== HighMass
    //dummy->GetXaxis()->SetRangeUser(90,1500);
    //dummy->GetXaxis()->SetRangeUser(90,200000); //JH
    //dummy->GetYaxis()->SetRangeUser(1E-4,1.);
    //dummy->Draw("axissame");
    //c_SOnly->SaveAs(plotpath+"/"+WhichYear+"_"+channel+"_13TeV_mixing_logx_HighMass_"+WhichDirectoryInCutop+"_"+myWP+".png");
  }

  return;

  /* //JH
  //==== S+T limit
  //======================

  //=== Legend
  TLegend * lg_SandT = new TLegend(0.43, 0.15, 0.66, 0.48);
  lg_SandT->SetBorderSize(0);
  lg_SandT->SetFillStyle(0);

  if(DrawObserved) lg_SandT->AddEntry(gr_13TeV_obs_SandT,"Observed", "l");
  lg_SandT->AddEntry(gr_13TeV_exp_SandT,"Expected", "l");
  lg_SandT->AddEntry(gr_band_1sigma_SandT,"68% expected", "f");
  lg_SandT->AddEntry(gr_band_2sigma_SandT,"95% expected", "f");
  //lg_SandT->AddEntry(gr_8and13TeV_obs, "CMS 8/13 TeV Combined", "l");
  lg_SandT->AddEntry(hist_emptylegend,"","l");
  lg_SandT->AddEntry(hist_emptylegend,"","l");


  TCanvas *c_SandT = new TCanvas("c_SandT", "", 900, 800);
  canvas_margin(c_SandT);
  c_SandT->cd();
  c_SandT->Draw();
  c_SandT->SetLogy();

  dummy->GetXaxis()->SetRangeUser(20., 2000);
  dummy->GetYaxis()->SetRangeUser(0.000005, 1.);
  dummy->Draw("hist");

  gr_band_2sigma_SandT->Draw("3same");
  gr_band_1sigma_SandT->Draw("3same");
  gr_13TeV_exp_SandT->Draw("lsame");
  gr_17028_exp->Draw("lsame");
  //gr_8and13TeV_obs->Draw("lsame");
  if(channel=="MuMu"){
    //gr_L3Limit->Draw("lsame");
    //gr_DELPHILimit->Draw("lsame");
    gr_trilepLimit->Draw("lsame");
    gr_EWPD_mm->Draw("lsame");
    //gr_ATLAS_MuMu->Draw("lsame");
  }
  if(channel=="EE"){
    //gr_L3_2Limit->Draw("lsame");
    //gr_DELPHILimit->Draw("lsame");
    gr_trilepLimit->Draw("lsame");
    //gr_dbeta->Draw("lsame");
    gr_EWPD_ee->Draw("lsame");
    //gr_ATLAS_EE->Draw("lsame");
  }
  if(DrawObserved) gr_13TeV_obs_SandT->Draw("lsame");

  lg_SandT->Draw();
  lg_Alt->Draw();

  latex_Lumi.SetTextSize(0.035);
  latex_Lumi.SetTextFont(42);
  latex_Lumi.DrawLatex(0.735, 0.96, "35.9 fb^{-1} (13 TeV)");
  latex_title.SetTextSize(0.04);
  latex_title.SetLineWidth(2);
  latex_title.DrawLatex(0.25, 0.84, "#font[41]{95% CL upper limit}");
  latex_title.SetTextSize(0.05);
  latex_title.DrawLatex(0.25, 0.88, "#font[62]{CMS}");

  c_SandT->SetLogx();
  dummy->Draw("axissame");
  c_SandT->SaveAs(plotpath+"/"+channel+"_13TeV_mixing_logx_SandT.pdf");
  c_SandT->SaveAs(plotpath+"/"+channel+"_13TeV_mixing_logx_SandT.png");

  return;
  */
}
