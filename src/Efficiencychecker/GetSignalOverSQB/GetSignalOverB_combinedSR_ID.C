#include "base_functions.h"
#include "Macros.h"
#include "mylib.h"
#include "canvas_margin.h"
#include <fstream>


void GetSignalOverB_combinedSR_IDMAIN(vector<TString> IDs, TString _y = "2016",TString isotag="_iso_", TString suffix="ipB", TString smass="100", double mass=100, TString channel="EE");
std::vector<TString>	GetIDList();

void GetSignalOverB_combinedSR_ID(){

  vector<TString> years={"2016"};//,"2017","2018"};
  
  for (auto y : years) {
    vector <TString> masses = {"300"};//,"500","1000"};                                                                                                                                    
    vector <double> d_masses = {300.};//,500.,1000.};                                                                                                                                       

    vector<TString> IDnames = GetIDList();
    
    for(int i = 0; i <  masses.size(); i++){
      GetSignalOverB_combinedSR_IDMAIN(IDnames,y,"", "FullOpt_iso", masses[i], d_masses[i]);
      GetSignalOverB_combinedSR_IDMAIN(IDnames,y,"", "FullOpt_Miniiso", masses[i], d_masses[i]);
      
    }
  }

}


std::vector<TString> GetIDList(){

  TString ENV_MERGEDFILE_PATH = getenv("INFILE_MERGED_PATH");
  TString analysername="HNDilepton" ;
  
  TString promptpath1 = ENV_MERGEDFILE_PATH+ analysername+"/2016/"+analysername+"_SkimTree_SSHN_DoubleEG_ID.root";

  
  TFile * _file1 = new TFile(promptpath1);
  TH1* h_id  = (TH1*)_file1->Get("FillEventCutflow/Fullopt_testhist_events");

  vector<TString> IDs;
  for(unsigned int i=1 ; i < h_id->GetNbinsX()+1; i++){

    TString hname = h_id->GetXaxis()->GetBinLabel(i);
    IDs.push_back(hname);
    if(! (i % 1000)) cout << hname << " i " << i << endl;
  }


  cout << "Number of IDs = " << IDs.size() << endl;

  return IDs;

}

void GetSignalOverB_combinedSR_IDMAIN(vector<TString> IDs, TString _y = "2016",TString isotag="_iso_",TString suffix="ipB",TString smass, double mass, TString channel="EE"){ 

  bool debug(true);
  // basic declarations 
  TString ptbin="";  TString _chan = "Schannel"; TString analysername="HNDilepton" ;

  // check which pc is running script to setup local paths
  TString s_hostname = GetHostname();

  ofstream myfile;
  myfile.open (_y+suffix+smass+isotag+".txt");
  
  vector<TString> code_names= {"HNDilepton"};

  if(std::find(code_names.begin(), code_names.end(), analysername) != code_names.end()) cout << "Running with code " << analysername << endl;
  else {cout << "Error in input of analyzer: " << analysername << endl; for (auto i: code_names)   std::cout << i << ' '; return; }

  
  // local path names
  TString ENV_FILE_PATH= (getenv("INFILE_PATH"));
  TString ENV_MERGEDFILE_PATH = getenv("INFILE_MERGED_PATH");
  TString ENV_PLOT_PATH = getenv("PLOT_PATH");
  TString FLATVERSION = getenv("FLATVERSION");
  
  MakeDir(ENV_PLOT_PATH + FLATVERSION);
  TString input_path = ENV_FILE_PATH + FLATVERSION+"/"+analysername+"/";
  TString output = ENV_PLOT_PATH + FLATVERSION + "/"+analysername+"/";

  MakeDir(output);
  output+="/SignalOverBackground/";  MakeDir(output);
  output+="/Combined/";              MakeDir(output);
  output+="SignalRegions/";          MakeDir(output);

  myfile << "GetSignalEfficiency_combinedSR::LOG Output dir = " << output << endl;
  
  if(s_hostname == "JohnMB2018s-MacBook-Pro.local")    input_path = "/Users/john/HNDiLeptonWorskspace/OutputTool/MergedFiles/";

  // Set Plotting style
  setTDRStyle();
  gStyle->SetPalette(1);



  //************************************************************************************
  //************************************************************************************
  // MACRO STARTS HERE
  //************************************************************************************
  //************************************************************************************

  // combine punzi for rach signal regions
  vector<TString> SR = {"SR1","SR2"};
  // combine punzi for different pt bins
  vector<TString> PTBins = {"_HighPt","_LowPt"};


  vector <TString> masses = {smass};//,"300","500","1000"};
  vector <double> d_masses = {mass};//,300.,500.,1000.};
  if (mass == 0.) d_masses = {100., 300.};
  TString _channel = channel;
  
  // hist leg
  TLegend *legend = MakeLegend(0.65, 0.65, 0.9, 0.92);
  // graph leg
  TLegend *legend_g = MakeLegend(0.65, 0.65, 0.9, 0.92);

  std::string input_user;
  
  TString promptpath1 = ENV_MERGEDFILE_PATH+ analysername+"/2016/"+analysername+"_SkimTree_SSHN_Muon.root";
  if(channel=="EE") promptpath1 = ENV_MERGEDFILE_PATH+ analysername+"/2016/"+analysername+"_SkimTree_SSHN_DoubleEG.root";

  myfile << "---------------------------------------------------------" << endl;
  myfile << "Channel : " << channel << " , datafile = " << promptpath1 << endl;
  myfile << "---------------------------------------------------------" << endl;
  myfile << "Is this correct? Type Y if correct. " << endl;

  if(!debug){
    cin >> input_user ;
    
    if( TString(input_user) != "Y") return;
  }
  
  TFile * _file1 = new TFile(promptpath1);
  
  myfile << "---------------------------------------------------------" << endl;
  myfile << "List of signals = " << endl;
  vector<TString> years={"2016","2017","2018"};
  if (_y != "") years = {_y};
  for (auto y : years)  for (auto im : masses) {
      TString sigpathS = ENV_MERGEDFILE_PATH+ "/"+analysername+"/"+y+"/SIG/"+analysername+"_DYTypeI_SS_"+_channel+"_M"+im+".root";
      myfile << sigpathS << endl;
    }
  
  myfile << "Is this correct? Type Y if correct. " << endl;
  if(!debug){
    cin >> input_user ;
    if( TString(input_user) != "Y") return;
  }

  
  vector<double> binvalues;
  
  //-- loop over masses and IDs to fill all 2D bin values as 0.;
  for (auto  id: IDs)   for (auto  im: masses) binvalues.push_back(0.);
  
  //-- Simply naming the 2D histogram
  TString histlabel= _channel +  +"_highmass_"+analysername;

  //  TH2D* hist2 = new TH2D(histlabel,histlabel,masses.size()+1,0,masses.size()+1., IDs.size(),0., IDs.size());

  //-- create map with ID/mass punzi value and string connected 
  map<double, TString> map_punzi;
  map<TString, double> map_id;

  for (auto year : years){
    //** Loop over SRs [SR1+SR2]
    for(auto _sr : SR){

      //*** loop over low and high pt bins
      for(auto ptbin : PTBins){
	
	//-- to make processing faster some assumptions can be made and some bins skipped

	if(ptbin == "_LowPt" && _sr == "SR2") continue;
	
	//-- vector of IDvalues
	vector<double> IDvalues;	

	//-- Make string for data file
	TString promptpath = ENV_MERGEDFILE_PATH+ analysername+"/"+year+"/"+analysername+"_SkimTree_SSHN_DoubleEG.root";
	if(channel=="EE"&&year=="2018") promptpath = ENV_MERGEDFILE_PATH+ analysername+"/"+year+"/"+analysername+"_SkimTree_SSHN_EGamma.root";
	
	TFile * file_prompt = new TFile((promptpath).Data());

	
	//**** loop over IDs to get integrate hists

	
	TString n_sr_hist ="PreselEEYields/"+suffix+ptbin+"_"+_sr+"_events";
	TString n_sr_hist_def ="PreselEEYields/FullOpt_StandardIDs"+ptbin+"_"+_sr+"_events";
	
	//-- access histogram in bkg file                                                                                                                                    
	cout << n_sr_hist << endl;
	TH1D* hpass = (TH1D*)(file_prompt->Get(n_sr_hist));
	TH1D* hpass2 = (TH1D*)(file_prompt->Get(n_sr_hist_def));
	hpass->Add(hpass2);
	  
	int id_counter(0);
	for(unsigned int ibin=1; ibin  < IDs.size()+1; ibin++){
	  id_counter++;
	  
	  double total_p = hpass->GetBinContent(ibin);
	  double total_b = sqrt(total_p);

	  //-- useful OUTPUT message showing ID and sqrtB
	  myfile << _sr << " " << ptbin << " : " <<  id_counter << " / " << IDs.size() << " "  << IDs[id_counter-1] << " sqrt B = "  << total_b << endl;
	  cout  << _sr << " " << ptbin << " : " <<  id_counter << " / " << IDs.size() << " "  << IDs[id_counter-1] << " sqrt B = "  << total_b << endl;
	  IDvalues.push_back(total_b);
	  //-- IDvalues  contains bkg numbers for this SR/ptbin  
	  
	}//**** END ID loop
	
      
	//-- ibin int keeps track of 2D bin number                                                                                                                                                              
	int ibin(0);
	
	//**** Loop over the masses 
	int mass_counter(0);
	for (auto im : masses){

	  mass_counter++;
	  
	  //-- mass_values gets signal yield for this mass 
	  vector<double> mass_values;

	  double total_mass_value(0.);

	  //-- set x axis label
	  //hist2->GetXaxis()->SetBinLabel(mass_counter, im);


	  ///-- Get signal file
	  TString sigpathS = ENV_MERGEDFILE_PATH+ "/"+analysername+"/"+year+"/SIG/"+analysername+"_DYTypeI_SS_"+_channel+"_M"+im+".root";
	  //TString sigpathT = ENV_MERGEDFILE_PATH+ "/"+analysername+"/"+year+"/SIG/"+analysername+"_VBFTypeI_SS_"+_channel+"_M"+im+".root";
	  TFile * filemm = new TFile((sigpathS).Data());
	  //TFile * filemmT = new TFile((sigpathT).Data());

	  //-- Check file is ok to read IF not set mass value to 0.
	  if(CheckFile(filemm) > 0) {
	    mass_values.push_back(0.);

	    filemm->Close();
	    delete filemm;

	    continue; 	    
	  }
	  
	  
	  //***** loop over IDs for this signal mass
	  
	  int sig_id_counter(0);


	  TH1D* hsigS = (TH1D*)(filemm->Get(n_sr_hist));
	  TH1D* hsigS2 = (TH1D*)(filemm->Get(n_sr_hist_def));
	  if(hsigS)	  hsigS->Add(hsigS2);
	  //	  if(im != "100") {
	  // //TH1D* hsigT = (TH1D*)(filemmT->Get(n_sr_hist));
	  //TH1D* hsigT2 = (TH1D*)(filemmT->Get(n_sr_hist_def));
	    //  hsigS->Add(hsigT2);
	    // }

	  
	  for(unsigned int ibin=1; ibin  < IDs.size()+1; ibin++){

	    TString _id = IDs[ibin-1];

	    sig_id_counter++;

	    ///-- set histogram name for signal

	    //-- Get number of signal events
	    float nsig= 1.;
	    
	    double err ;  double  punzi = 0.;
	    if(hsigS){
      
	      float nsig= hsigS->GetBinContent(ibin);
	      punzi = (IDvalues[sig_id_counter-1] > 0) ?  (nsig) /IDvalues[sig_id_counter-1] : 0.;
	      
	      //-- useful OUTPUT message showing ID and punzi                                                                                                                                                           
	      myfile << _sr << " " << ptbin << " : " << IDs[sig_id_counter-1] << " " << nsig << " / " << IDvalues[sig_id_counter-1] <<  " punzi =" << punzi<< endl;
	      cout << _sr << " " << ptbin << " : " << IDs[sig_id_counter-1] << " " << nsig << " / " << IDvalues[sig_id_counter-1] <<  " punzi =" << punzi<< endl;
	    }
	    else {
	      
	      myfile << _sr << " " << ptbin << " : " << IDs[sig_id_counter-1] << " 0.  " << IDvalues[sig_id_counter-1] <<  " " << punzi<< endl;
		      
	    }
	    
	    mass_values.push_back(punzi);
	    total_mass_value+= punzi;
	    
	    //map_punzi[punzi] = _id;
	    map<TString, double>::iterator mit = map_id.find(_id);
	    if (mit == map_id.end())     map_id[_id]      = punzi;
	    else  map_id[_id]      = punzi + mit->second;
	    
	  }//***** end of signal ID loop

	  ///-- close file
	  filemm->Close();
	  delete filemm;
	  //filemmT->Close();
          //delete filemmT;
      	  
	} //**** mass loop
      } //*** ptbin loop
    }//** SR loop
  }
  
  // Now redo histogram to get average
  
  for(auto mit : map_id) map_punzi[mit.second] = mit.first;
  
  for(auto mit : map_punzi) myfile << mit.second << " s/sqrt(B) = " << mit.first << endl;
  for(auto mit : map_punzi) cout << mit.second << " s/sqrt(B) = " << mit.first << endl; 
    
  //myfile << " MAX ID = " << IDs[_max_id] << "  " << max_punzi  << endl;


  TString canvasname2="SR12_highmass_njets_"+analysername+"_JA_"+_channel+ptbin+channel;
  
  TCanvas* c2 = new TCanvas(canvasname2,canvasname2, 800,800);
  c2->cd();
  
  TString outfile = output  +  "/TH2D_"+ptbin+"SR12highmass_signaloverbackground_"+analysername+"_"+_chan+"_"+channel+suffix+_y+".root";
  TFile* fout = new TFile(outfile.Data(),"RECREATE");
  
  //hist2->Draw("colztext");
  //hist2->Write();
  
  TString save_sg= output + "/TH2D_"+ptbin+"SR12highmass_signaloverbackground_"+analysername+"_"+_chan+"_"+channel+suffix+_y+"_mN"+smass+".pdf";
  
  c2->SaveAs(save_sg);
  
  myfile.close();

  return;
      
    
}
