import os,sys,ROOT,time
import mylib
import ctypes
import canvas_margin
import tdrstyle
import CMS_lumi, tdrstyle
import math
from array import array


## SampleGroup ##
class SampleGroup:
  def __init__(self, Name, Type, Samples, Era, Skim, Color=0, Style=1, Width=1, TLatexAlias="", LatexAlias="", Scale=1):

    self.Name = Name
    self.Type = Type
    self.Samples = Samples
    self.Era = Era
    if "16" in Era:
      self.Year = 2016
    elif Era == "YearCombined":
      print Name + " " + Era
      self.Year =Era
    else:
      self.Year=int(Era)
    self.Skim = Skim
    self.Color = Color
    self.Style = Style
    self.Width = Width
    self.TLatexAlias = TLatexAlias
    self.LatexAlias = LatexAlias
    self.Scale = Scale

  def Print(self):
    print ('Sample group name = '+self.Name)
    print (  'Type = ',self.Type)
    print (  'Samples = '),
    print (self.Samples)
    print (  'Year = '+str(self.Year))
    print (  'Era = '+str(self.Era))
    print (  'Color = '+str(self.Color))
    print (  'TLatexAlias = '+str(self.TLatexAlias))
    print (  'LatexAlias = '+str(self.LatexAlias))

## SignalInfo ##
class SignalInfo:
  def __init__(self, process, mN, Color=ROOT.kBlack):
    self.process = process
    self.mN = mN
    self.Color = Color
    self.xsec = 1.
    self.kfactor = 1.
    self.xsecScale = 1.
    self.Style = 3
    self.useOfficial = False

    self.TLatexAlias = "(m_{N}, Process) = (%d, %d) GeV"%(self.mN, self.Process)

  def Print(self):
    print ('( %d, %f, %f)'%( self.mN, self.xsec, self.kfactor))
  def GetTLatexAlias(self):
    if self.xsecScale!=1.:
      self.TLatexAlias = "%d #times (m_{N}) = (%d, %d) GeV"%(self.xsecScale, self.mN)

    return self.TLatexAlias

## Variable ##
class Variable:
  def __init__(self, Name, TLatexAlias, Unit):
    self.Name = Name
    self.TLatexAlias = TLatexAlias
    self.Unit = Unit
  def Print(self):
    print ('(%s, %s, %s)' % (self.Name, self.TLatexAlias, self.Unit))

## Region ##
class Region:
  #def __init__(self, Name, PrimaryDataset, PName, UnblindData=True, Logy=-1, TLatexAlias="", CutFlowCaption="Test"):
  def __init__(self, Name, PrimaryDataset, PName, InputDirectory, HistTag, OutputTag, UnblindData=False, Logy=-1, TLatexAlias="", CutFlowCaption="Test", DrawData=False, DrawRatio=True): #JH
    self.Name = Name
    self.PrimaryDataset = PrimaryDataset
    self.ParamName = PName
    self.HistTag = HistTag
    self.OutputTag = OutputTag
    self.UnblindData = UnblindData
    self.Logy = Logy
    self.TLatexAlias = TLatexAlias
    self.CutFlowCaption = CutFlowCaption
    self.InputDirectory = InputDirectory

    self.DrawData = DrawData
    self.DrawRatio = DrawRatio

  def Print(self):
    print ('(%s, %s, UnblindData=%s, Logy=%f, %s)'%(self.Name, self.PrimaryDataset, self.UnblindData, self.Logy, self.TLatexAlias))

## Systematic ##
class Systematic:
  def __init__(self, Name, Direction, Year):
    self.Name = Name
    self.Direction = Direction
    self.Year = Year ## if <0, it's correalted    

  def FullName(self):
    if self.Year>0:
      return 'Run'+str(self.Year)+'_'+self.Name
    else:
      return self.Name

  def Print(self):
    str_Direction = 'Up' if self.Direction>0 else 'Down'
    if self.Direction==0:
      str_Direction = "Central"
    print ('(%s, %s, %d)'%(self.Name, str_Direction, self.Year))

## Plotter ##
class Plotter:

  def __init__(self):

    self.DoDebug = False
    self.Lxplus_User=''
    self.Lxplus_Dir=''
    self.DataYear = 2016
    self.DataEra = ""
    self.DataDirectory = "2016"

    self.SampleGroups = []
    self.RegionsToDraw = []
    self.VariablesToDraw = []
    self.SignalsToDraw = []

    self.Systematics = []
    self.Filename_prefix = ""
    self.Filename_suffix = ""
    self.Filename_data_skim = ""
    self.OutputDirectory = ""
    self.OutputDirectoryLocal = ""

    self.ScaleMC = False

    self.ExtraLines = ""

    self.ErrorFromShape = False
    self.AddErrorLinear = False

    self.NoErrorBand = False #JH tmp

  def PrintBorder(self):
    print ('--------------------------------------------------------------------------')
    
  def PrintSamples(self):
    self.PrintBorder()
    print ('[Plotter.PrintSamples()] Printing samples')
    for s in self.SampleGroups:
      s.Print()
    self.PrintBorder()

  def PrintRegions(self):
    self.PrintBorder()
    print ('[Plotter.PrintRegions()] Printing regions to be drawn')
    for s in self.RegionsToDraw:
      s.Print()
    self.PrintBorder()

  def PrintVariables(self):
    self.PrintBorder()
    print ('[Plotter.PrintVariables()] Printing variables to be drawn')
    for s in self.VariablesToDraw:
      s.Print()
    self.PrintBorder()

  def PrintSystematics(self):
    self.PrintBorder()
    print ('[Plotter.PrintSystematics()] Printing systematics')
    for s in self.Systematics:
      s.Print()
    self.PrintBorder()

  ## Benning related

  def SetBinningFilepath(self, RebinFilepath, XaxisFilepath, YaxisFilepath):
    self.RebinFilepath = RebinFilepath
    self.XaxisFilepath = XaxisFilepath
    self.YaxisFilepath = YaxisFilepath

  def ReadBinningInfo(self, Region):
    ## Rebin
    Rebins = dict()
    
    for line in open(self.RebinFilepath).readlines():
      if "#" in line: continue
      words = line.split()
      if Region!=words[0]:
        continue
      Rebins[words[1]] = int(words[2])
      if self.DoDebug:
        print ("Setting rebin " + str(words[1]) + " " + str(words[2]))



    if len(Rebins) == 0:
      print("No bin width set for " +str(Region) ) #JH

    ## xaxis
    XaxisRanges = dict()

    for line in open(self.XaxisFilepath).readlines():
      words = line.split()
      if Region!=words[0]:
        continue
      XaxisRanges[words[1]] = [float(words[2]), float(words[3])]

    if len(XaxisRanges) == 0:
      print("No bin range set for " +str(Region) ) #JH

    return Rebins, XaxisRanges
  def Rebin(self, hist, region, var, nRebin):
    if var=='NCand_Mass':
      return mylib.RebinNMass(hist, region, self.DataYear)
    elif var=='ToBeCorrected_Jet_Pt':
      return mylib.RebinJetPt(hist, region, self.DataYear)
    else:
      if nRebin>0:
        hist.Rebin(nRebin)
        return hist
      else:
        return hist
  def ZeroDataCheckCut(self,var,xlow,xhigh):
    ## TODO
    return False


  def DoCutFlow(self,Hist_Name):

    nprec = 0
    print ('[Plotter.Cutflow()] ')

    CutFlowDir= os.getenv("HNDILEPTONWORKSPACE_DIR")+'/CutFlow/'
    
    if os.path.exists(CutFlowDir+'/Cutflow.sh'):
      os.system('rm '+CutFlowDir+'/Cutflow.sh')
    
    ROOT.gErrorIgnoreLevel = ROOT.kFatal

    tdrstyle.setTDRStyle()
    ROOT.TH1.AddDirectory(False)


    for Region in self.RegionsToDraw:
      print Region.Name
      Indir = Region.InputDirectory
      Outdir = self.OutputDirectoryLocal+'/'+Region.ParamName+'/'+Region.Name+'/' #JH
      if self.ScaleMC:
        Outdir = self.OutputDirectoryLocal+'/ScaleMC/'+Region.Name+'/'
      os.system('mkdir -p '+Outdir)

      print("self.Filename_prefix " + str(self.Filename_prefix))
      #f_Data = ROOT.TFile(Indir+'/'+self.DataDirectory+'/'+self.Filename_prefix+self.Filename_data_skim+'_data_'+Region.PrimaryDataset+self.Filename_suffix+'.root')
      f_Data = ROOT.TFile(Indir+'/'+self.DataDirectory+'/'+self.Filename_prefix+self.Filename_data_skim+self.Filename_suffix+'.root')
      print (Region.PrimaryDataset + '/'+ Region.ParamName + '/'+ Region.Name+'/'+Hist_Name) #######
      h_Data = f_Data.Get(Region.PrimaryDataset + '/'+ Region.ParamName + '/'+ Region.Name+'/'+Hist_Name)
      if not h_Data:
        print (Indir+'/'+self.DataDirectory+'/'+self.Filename_prefix+self.Filename_data_skim+'_data_'+Region.PrimaryDataset+self.Filename_suffix+'.root missing ' +Region.PrimaryDataset + '/'+ Region.ParamName + '/'+ Region.Name+'/'+Hist_Name)
        print (Region.PrimaryDataset + '/'+ Region.ParamName + '/'+ Region.Name+'/'+Hist_Name)
        print (Hist_Name+'_'+Region.Name+'.pdf ==> No data, skipped')
        print ('---- ' + Indir+'/'+self.DataDirectory+'/'+self.Filename_prefix+self.Filename_data_skim+'_data_'+Region.PrimaryDataset+self.Filename_suffix+'.root')
        continue
      data_integral=h_Data.Integral()
      data_error  = ctypes.c_double(0.)
      integral = h_Data.IntegralAndError(0,h_Data.GetNbinsX(),data_error,"");

      total_bkg_integral=0.
      total_bkg_staterror=0.
      sys_total_bkg_up=0
      sys_total_bkg_down=0
      
      CFName=Region.PrimaryDataset+"_"+Region.Name
      CutFlowLatexFile = open (CutFlowDir+'/Cutflow_'+CFName+'.tex','w')
      CutFlowLatexFile.write('\\documentclass[10pt]{article}\n')
      CutFlowLatexFile.write('\\usepackage{epsfig,subfigure,setspace,xtab,xcolor,array,colortbl}\n')
      CutFlowLatexFile.write('\providecommand{\\cmsTable}[1]{\\resizebox{\\textwidth}{!}{#1}}\n')
      CutFlowLatexFile.write('\\begin{document}\n')
      CutFlowLatexFile.write('\\input{"'+CutFlowDir+'/Tables/Cutflow_'+self.DataDirectory+'_'+CFName+'Table.txt"}\n')
      CutFlowLatexFile.write('\\end{document}\n')
      CutFlowLatexFile.close()
      caption=Region.CutFlowCaption
      print ("Caption = " + caption)
      CutFlowLatexTableFile = open (CutFlowDir+'/Tables/Cutflow_'+self.DataDirectory+'_'+CFName+'Table.txt','w')
      CutFlowLatexTableFile.write("\\begin{table}[ptb]\n" )
      CutFlowLatexTableFile.write("\\centering\n" )
      CutFlowLatexTableFile.write("\\cmsTable{\n" )
      CutFlowLatexTableFile.write("\\begin{tabular}{lcccc}\n" )
      CutFlowLatexTableFile.write("\\hline\n" )
      CutFlowLatexTableFile.write("\\hline\n" )   
      CutFlowLatexTableFile.write("Source & \\multicolumn{4}{c}{} \\\\ \n" )
      CutFlowLatexTableFile.write("\\hline\n" )   
      
      
      for SampleGroup in self.SampleGroups:

        bkg_integral=0.
        bkg_staterror=0.

        
        for Sample in SampleGroup.Samples:
          if self.DoDebug:
            print ('[DEBUG] Trying to make histogram for Sample = '+Sample)
            
          f_Sample = ROOT.TFile(Indir+'/'+str(SampleGroup.Era)+'/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root')
          h_Sample = 0
          #if (Syst.Year>0) and (Syst.Year!=SampleGroup.Year):
          #  tmp_dirName = Region.Name
          #  h_Sample = f_Sample.Get(tmp_dirName+'/'+Hist_Name+'_'+tmp_dirName)
          #elif (Syst.Name in ["Lumi", "DYNorm", "NonPromptNorm", "OthersNorm"]):
          #  tmp_dirName = Region.Name
          #  h_Sample = f_Sample.Get(tmp_dirName+'/'+Hist_Name+'_'+tmp_dirName)
          #  ## For all other cases
          #else:
          dirName = Region.Name

          h_Sample = f_Sample.Get(Region.PrimaryDataset + '/'+ Region.ParamName + '/'+ Region.Name+'/'+Hist_Name)

          if not h_Sample:
            continue


          ## Scale
          MCSF, MCSFerr = 1., 0.
          #if self.ScaleMC:
          #  if "DYJets" in Sample:
          MCSF= mylib.GetNormSF(SampleGroup.Year, Sample)
          
          print "MCSF = " + str(MCSF)
          h_Sample.Scale( MCSF )

          stat_error  = ctypes.c_double(0.)
          integral = h_Sample.IntegralAndError(0,h_Sample.GetNbinsX(),stat_error,"");
          bkg_integral += h_Sample.Integral()
          total_bkg_integral += h_Sample.Integral()
          bkg_staterror = math.sqrt(bkg_staterror*bkg_staterror + stat_error.value*stat_error.value)
          total_bkg_staterror = math.sqrt(total_bkg_staterror*total_bkg_staterror + stat_error.value*stat_error.value)
          
        print (Sample + " integral = " + str(bkg_integral))
        bkg_integral=round(bkg_integral,nprec)
        bkg_staterror=round(bkg_staterror,nprec)
        sys_bkg_up =  mylib.GetMCUncertainty(SampleGroup.Name)*bkg_integral
        sys_bkg_down = mylib.GetMCUncertainty(SampleGroup.Name)*bkg_integral
        sys_total_bkg_up = math.sqrt(sys_total_bkg_up*sys_total_bkg_up+sys_bkg_up*sys_bkg_up)
        sys_total_bkg_down = math.sqrt(sys_total_bkg_down*sys_total_bkg_down+sys_bkg_down*sys_bkg_down)
        
        if bkg_integral > 0:
          CutFlowLatexTableFile.write( SampleGroup.LatexAlias + "& " +  str(bkg_integral) + "& $\\pm$ & "  + str(bkg_staterror)  +  "&$^{+"+str(sys_bkg_up)+"}_{-"+str(sys_bkg_down)+"}$ \\\\\n" )

      sys_total_bkg_up   = int(round(sys_total_bkg_up))
      sys_total_bkg_down   = int(round(sys_total_bkg_down))
      total_bkg_integral=   int(round(total_bkg_integral,nprec))
      total_bkg_staterror = int(round(total_bkg_staterror,nprec))

      CutFlowLatexTableFile.write('\\hline\n')

      significance_up = (data_integral - total_bkg_integral) / (math.sqrt(total_bkg_staterror*total_bkg_staterror+sys_total_bkg_up*sys_total_bkg_up + data_error.value*data_error.value ))
      significance_down = (data_integral - total_bkg_integral) / (math.sqrt(total_bkg_staterror*total_bkg_staterror+sys_total_bkg_down*sys_total_bkg_down + data_error.value*data_error.value ))
      significance=significance_up
      if significance_down > significance_up:
        significance=significance_down


      sys_total_bkg_up=int(round(sys_total_bkg_up,nprec))
      sys_total_bkg_down=int(round(sys_total_bkg_down,nprec))
      CutFlowLatexTableFile.write('Total& ' + str(total_bkg_integral)  + "& $\\pm$ & "  + str(total_bkg_staterror)  +  "&$^{+"+str(sys_total_bkg_up)+"}_{-"+str(sys_total_bkg_down)+"}$ \\\\\n" )
      CutFlowLatexTableFile.write('\\hline\n')
      CutFlowLatexTableFile.write('Data& \\multicolumn{4}{c}{$' + str(int(data_integral)) + '$}\\\\ \n')
      CutFlowLatexTableFile.write('\\hline\n')
      significance=round(significance,nprec)
      if significance < 0:
        CutFlowLatexTableFile.write("Significance&  \\multicolumn{4}{c}{$" + str(significance) + "\\sigma$}\\\\ \n")
      else:
        CutFlowLatexTableFile.write("Signifficance&  \\multicolumn{4}{c}{$" + str(significance) + "\\sigma$}\\\\ \n")

      CutFlowLatexTableFile.write('\\hline\n')
      CutFlowLatexTableFile.write('\\hline\n')
      CutFlowLatexTableFile.write('\end{tabular}\n')
      CutFlowLatexTableFile.write('}\n')
      CutFlowLatexTableFile.write("\\caption{"+caption+"}\n")
      CutFlowLatexTableFile.write('\end{table}\n')

      print "#"*50
      print "#"*50
      print ("Starting process for Cutflow:")
      
      print ("Moving to Cutflow dir")
      
      cdir=os.getenv("PWD")

      os.chdir(CutFlowDir)
      #print ('CutFlowDir='+CutFlowDir)
      
      latex_command = "latex " +  CutFlowDir+"/Cutflow_"+CFName+".tex"
      os.system("ls  " + CutFlowDir)
      time.sleep(5)
      dvi_command = "dvipdf "+ CutFlowDir +"/Cutflow_"+CFName+".dvi"
      mv_command = "mv " + CutFlowDir+"/Cutflow_"+CFName+".pdf  " + Outdir

      print ('DoCutFlow: source '+CutFlowDir+"/Cutflow"+CFName+".sh") 
      run_latex = open(CutFlowDir+"/Cutflow"+CFName+".sh","a")
      run_latex.write('cd ' + CutFlowDir+'\n')
      run_latex.write(latex_command + '\n')
      run_latex.write(dvi_command + '\n')
      run_latex.write(mv_command + '\n')
      print '-'*40
      print '-'*40
      print(latex_command)
      print '-'*40
      print(dvi_command)
      print '-'*40
      print(mv_command)
      run_latex.write('rm Cutflow_'+CFName+'.aux\n')
      run_latex.write('rm Cutflow_'+CFName+'.tex\n')
      run_latex.write('rm Cutflow_'+CFName+'.dvi\n')
      
      run_latex.write('cd -')
      run_latex.close()

      cwd= os.getenv("PWD")
      os.chdir(CutFlowDir)
      os.system(latex_command)
      os.system(dvi_command)
      os.system(mv_command)
      #os.system('rm Cutflow'+Region.Name+'.aux\n')                                                                                    
      #os.system('rm Cutflow'+Region.Name+'.tex\n')                                                                                   
      #os.system('rm Cutflow'+Region.Name+'.dvi\n')                                                                                    
      os.chdir(cwd)
            
      print ('Table ==> ' + Outdir + '/Cutflow'+CFName+'.pdf')

      
      if not self.OutputDirectory =="":
        OutdirLXPLUS= self.OutputDirectory +'/'+Region.Name+'/'
        if self.ScaleMC:
          os.system("ssh jalmond@lxplus.cern.ch 'mkdir -p " + self.OutputDirectory +"/ScaleMC/'")
          OutdirLXPLUS= self.OutputDirectory +'/ScaleMC/'+Region.Name+'/'
          
      print( 'scp ' + Outdir + '/Cutflow_'+CFName+'.pdf  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
      os.system('scp ' + Outdir + '/Cutflow_'+CFName+'.pdf  '+ self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')

###########################################################################################################################################################
  def Draw(self):

    ROOT.gErrorIgnoreLevel = ROOT.kFatal

    tdrstyle.setTDRStyle()
    ROOT.TH1.AddDirectory(False)
    lxplus_dir=[]
    for Region in self.RegionsToDraw:

      print ('## Drawing '+Region.Name)

      ## Read binning data
      Rebins, XaxisRanges = self.ReadBinningInfo(Region.Name)
      if self.DoDebug:
        print ('[DEBUG] Use rebin : ')
        print Rebins
        print ('[DEBUG] Use Xaxis range : ')
        print XaxisRanges

      ## Input/Output directotry
      Indir = Region.InputDirectory
      Outdir = self.OutputDirectoryLocal+'/'+Region.ParamName+'/'+Region.Name+'/'+Region.PrimaryDataset+'/' #JH : /data6/Users/jihkim/HNDiLeptonWorskspace/Output/Plots/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/MVAUL_UL/DiJetSR3/MuMu
      if self.ScaleMC:
        Outdir = self.OutputDirectoryLocal+'/ScaleMC/'+Region.Name+'/'

      if not self.OutputDirectory =="":
        OutdirLXPLUS= self.OutputDirectory +'/'+Region.Name+'/'
        os.system("ssh "+self.Lxplus_User + "@lxplus.cern.ch 'mkdir -p " + OutdirLXPLUS + "'")
        if self.ScaleMC:
          os.system("ssh "+self.Lxplus_User + "@lxplus.cern.ch 'mkdir -p " + self.OutputDirectory +"/ScaleMC/'")
          OutdirLXPLUS= self.OutputDirectory +'/ScaleMC/'+Region.Name+'/'
          os.system("ssh "+self.Lxplus_User + "@lxplus.cern.ch 'mkdir -p " + OutdirLXPLUS + "'")


      print ('##   Outputs => '+Outdir)
      
      os.system('mkdir -p '+Outdir)
      if not self.OutputDirectory =="":
        print('scp ' + os.getenv('HTML_DIR') + '/index.php ' + ''+self.Lxplus_User + '@lxplus.cern.ch:'+ OutdirLXPLUS+'/')
        os.system('scp ' + os.getenv('HTML_DIR') + '/index.php ' + ''+self.Lxplus_User + '@lxplus.cern.ch:'+ OutdirLXPLUS+'/')


      ## Data file
      datapath = Indir+'/'+self.DataDirectory+'/'+self.Filename_prefix+self.Filename_data_skim+'_DATA'+self.Filename_suffix+'.root' #JH : /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_ControlRegionPlotter/2017/DATA/HNL_ControlRegionPlotter_SkimTree_HNMultiLep_DATA.root
      f_Data = ROOT.TFile(datapath)
      if self.DoDebug:
        print ('[DEBUG] Trying to read from data file ' + datapath)


      ## Loop over variables

      for Variable in self.VariablesToDraw:

        ## BinInfo
        nRebin = 1
        
        if  Variable.Name in  Rebins.keys():
          print(Variable.Name + ' rebinning to ' + str(Rebins[Variable.Name]))
          nRebin = Rebins[Variable.Name]

        xMin= 0
        xMax=100000.

        if  Variable.Name in  XaxisRanges.keys():
          xMin = XaxisRanges[Variable.Name][0]
          xMax = XaxisRanges[Variable.Name][1]
        yMax = -999

        if self.DoDebug:
          print ('[DEBUG] Trying to draw variable = '+Variable.Name)
          print ('[DEBUG] (xMin,xMax) = (%s,%s)'%(xMin,xMax))

        ## xtitle
        xtitle = Variable.TLatexAlias
        if Variable.Name=="NCand_Mass":
          if "Resolved" in Region.Name:
            xtitle = "m_{ljj} (GeV)"
          else:
            xtitle = "m_{lJ} (GeV)"

        ## Save hists
        ## For legend later..
        HistsToDraw = dict()

        ## Loop over samples
        ## For Legend, save 
        HistsForLegend = []
        AliasForLegend = [] ## Prevent double-counting
        stack_Bkgd = ROOT.THStack("stack_Bkgd", "") # This is the total background which will be drawn
        h_Bkgd = 0
        ## Save systematic
        SystematicUps = dict()
        SystematicDowns = dict()
        ## If we take errors from shapes
        h_TotalBackgroundFromShape = 0

        ## Loop over systematics
        for Syst in self.Systematics:

          if self.DoDebug:
            print ('[DEBUG] Trying to make histogram for Syst = '),
            Syst.Print()

          h_Bkgd_ForSyst = 0
          paramName = Region.ParamName

          if Syst.Name!="Central":

            if Syst.Direction>0:
              paramName = "Syst_"+Syst.Name+"Up"+Region.ParamName #Syst_JetResUpMVAUL_UL
            else:
              paramName = "Syst_"+Syst.Name+"Down"+Region.ParamName

          ## Loop over sample groups
          for SampleGroup in self.SampleGroups:
            Color = SampleGroup.Color
            LegendAdded = False

            if 'Data' in SampleGroup.Type: paramName = Region.ParamName #JH : no syst hist for data-driven bkg.

            ## Loop over samples in each sample group
            for Sample in SampleGroup.Samples:

              if self.DoDebug:
                print ('[DEBUG] Trying to make histogram for Sample = '+Sample)

              if 'Fake' in SampleGroup.Type: samplepath = Indir+'RunFake__/DATA/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root' # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/RunFake__/DATA
              elif 'CF' in SampleGroup.Type: samplepath = Indir+'RunCF__/DATA/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root' # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/RunCF__/DATA
              elif 'Conv' in SampleGroup.Type: samplepath = Indir+'RunConv__/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root' # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/RunConv__
              elif 'Prompt' in SampleGroup.Type: samplepath = Indir+'RunPrompt__/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root' # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/RunConv__
              else: samplepath = Indir+'/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root' # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/HNL_SignalRegionPlotter_SkimTree_HNMultiLep_WZTo3LNu_amcatnlo.root
              f_Sample = ROOT.TFile(samplepath)
              print "opening", samplepath, '...'

              h_Sample = 0
              histpath = 0
              #print Syst.Year, SampleGroup.Year
              ## Uncorrelated sources has Syst.Year = 2016 or 2017 or 2018
              ## For this cases, SampleGroup.Year should be matched
              if (Syst.Year>0): #and (Syst.Year==SampleGroup.Year): #JH : Do I need this?
                if "LimitInput" in Region.Name and not "BDT" in Region.Name:
                  histpath = Region.Name+'/'+paramName+'/FillEventCutflow/'+Region.PrimaryDataset #JH : "LimitInput/Syst_JetResUpMVAUL_UL/FillEventCutflow/MuonSR"
                elif "LimitInput" in Region.Name and "BDT" in Region.Name:
                  histpath = Region.Name.split('_')[0]+'/'+paramName+'/'+Region.Name.split('_')[1]+'/FillEventCutflow/'+Region.PrimaryDataset #JH : "LimitInputBDT/Syst_JetResUpMVAUL_UL/M100/FillEventCutflow/MuonSR"
                else:
                  histpath = Region.PrimaryDataset + '/'+ paramName + '/RegionPlots_'+ Region.Name+'/'+Variable.Name # MuMu/Syst_JetResUpMVAUL_UL/RegionPlots_DiJetSR3/Lep_1_Pt
                h_Sample = f_Sample.Get(histpath)

              ## 1) Lumi, MC normalizaion
              ## Use central and scale them later
              elif (Syst.Name in ["Lumi"]): # Lumi is set correlated, so Syst.Year == -1.
                h_Sample = f_Sample.Get(Region.PrimaryDataset + '/'+ paramName + '/'+ Region.Name+'/'+Variable.Name)
              ## For all other cases
              elif (Syst.Name in ["GetMCUncertainty"]):
                h_Sample = f_Sample.Get(Region.PrimaryDataset + '/'+ paramName + '/'+ Region.Name+'/'+Variable.Name)
              else: # Central
                if 'CR' in Region.Name or 'Presel' in Region.Name: histpath = Region.Name+'/' + Region.PrimaryDataset + '/'+ Region.ParamName + '/RegionPlots_' + Region.PrimaryDataset + '/' + Region.HistTag + '/' + Variable.Name #JH : CR naming convention
                elif 'SR' in Region.Name: histpath = Region.Name+'/' + Region.PrimaryDataset + '_Channel/'+ Region.ParamName + '/RegionPlots_' + Region.PrimaryDataset + '/' + Region.HistTag + '/' + Variable.Name #JH : SR naming convention
                #if "LimitInput" in Region.Name and not "BDT" in Region.Name:
                #  histpath = Region.Name+'/'+paramName+'/FillEventCutflow/'+Region.PrimaryDataset #JH : "LimitInput/Syst_JetResUpMVAUL_UL/FillEventCutflow/MuonSR"
                #elif "LimitInput" in Region.Name and "BDT" in Region.Name:
                #  histpath = Region.Name.split('_')[0]+'/'+paramName+'/'+Region.Name.split('_')[1]+'/FillEventCutflow/'+Region.PrimaryDataset #JH : "LimitInputBDT/Syst_JetResUpMVAUL_UL/M100/FillEventCutflow/MuonSR"
                #else:
                #  histpath = Region.PrimaryDataset + '/'+ paramName + '/RegionPlots_'+ Region.Name+'/'+Variable.Name # MuMu/Syst_JetResUpMVAUL_UL/RegionPlots_DiJetSR3/Lep_1_Pt
                h_Sample = f_Sample.Get(histpath)
              print "opening",histpath,"..."

              print h_Sample
              if not h_Sample:
                print 'No hist : %s %s'%(Syst.Name,Sample)
                continue

              ## Make overflow
              h_Sample.GetXaxis().SetRangeUser(xMin,xMax)
              h_Sample = mylib.MakeOverflowBin(h_Sample)

              h_Sample = self.Rebin(h_Sample, Region.Name, Variable.Name, nRebin)
              h_Sample.SetLineColor(Color)
              h_Sample.SetLineWidth(1)
              h_Sample.SetFillColor(Color)

              ## Scale MC
              MCSF, MCSFerr = 1., 0.
              if self.ScaleMC:
                ## now, only for DY
                if "DYJets" in Sample:
                  #MCSF, MCSFerr = mylib.GetDYNormSF(SampleGroup.Year, Region.Name)
                  MCSF, MCSFerr = mylib.GetDYNormSF(self.DataYear, Region.Name) #JH : Do we really need SampleGroup.Year?

              #MCSF= mylib.GetNormSF(SampleGroup.Year, Sample)
              MCSF= mylib.GetNormSF(self.DataYear, Sample)
              h_Sample.Scale( MCSF )

              ## Manual systematic
              ## 1) [Lumi] Uncorrelated
              if (Syst.Name=="Lumi") and (Syst.Year==SampleGroup.Year):
                lumierr = mylib.LumiError(Syst.Year)
                for ix in range(0,h_Sample.GetXaxis().GetNbins()):
                  y = h_Sample.GetBinContent(ix+1)
                  y_new = y + y*float(Syst.Direction)*lumierr
                  h_Sample.SetBinContent(ix+1, y_new)
                  
              #if (Syst.Name=="GetMCUncertainty") and (Syst.Year==SampleGroup.Year):
              if (Syst.Name=="GetMCUncertainty") and (Syst.Year==self.DataYear):
                mcerr = mylib.GetMCUncertainty(SampleGroup.Name)
                for ix in range(0,h_Sample.GetXaxis().GetNbins()):
                  y = h_Sample.GetBinContent(ix+1)
                  y_new = y + y*float(Syst.Direction)*mcerr
                  h_Sample.SetBinContent(ix+1, y_new)
                  
                  
                  
              ## AddError option
              AddErrorOption = ''
              if self.AddErrorLinear:
                AddErrorOption = 'L'

              ## If central, add to h_Bkgd
              if Syst.Name=="Central" and Sample=='total_background':
                if not h_TotalBackgroundFromShape:
                  h_TotalBackgroundFromShape = h_Sample.Clone()
                else:
                  h_TotalBackgroundFromShape = mylib.AddHistograms( h_TotalBackgroundFromShape, h_Sample, AddErrorOption )
                HistsToDraw[Sample] = h_Sample.Clone()

              elif Syst.Name=="Central":
                stack_Bkgd.Add( h_Sample ) # add sample to stack_Bkgd
                if not h_Bkgd:
                  h_Bkgd = h_Sample.Clone()
                else:
                  h_Bkgd = mylib.AddHistograms( h_Bkgd, h_Sample, AddErrorOption) # and also add sample to h_Bkgd

                HistsToDraw[Sample] = h_Sample.Clone()
                if (not LegendAdded) and (SampleGroup.TLatexAlias not in AliasForLegend):
                  HistsForLegend.append( [HistsToDraw[Sample],SampleGroup.TLatexAlias] )
                  AliasForLegend.append(SampleGroup.TLatexAlias)
                  LegendAdded = True
              ## else (i.e., systematic), add to h_Bkgd_ForSyst
              else:
                print ("Adding hist to syst " + Syst.Name + ", direction : " + str(Syst.Direction))
                if not h_Bkgd_ForSyst:
                  h_Bkgd_ForSyst = h_Sample.Clone()
                else:
                  h_Bkgd_ForSyst = mylib.AddHistograms(h_Bkgd_ForSyst, h_Sample, AddErrorOption)

              ## Close file
              f_Sample.Close()

            ##==>End Sample loop
          ##==>End SampleGroup loop

          if Syst.Name!="Central":
            if Syst.Direction>0:
              SystematicUps[Syst.FullName()] = h_Bkgd_ForSyst
            else:
              SystematicDowns[Syst.FullName()] = h_Bkgd_ForSyst

        ##==>End Syst loop
        #print SystematicUps
        #print SystematicDowns

        ## Syst Up/Down . Max/Min
        if not h_Bkgd:
          print "No h_Bkgd ==> Skipping ..."
          continue
        h_Bkgd_TotErr_Max = h_Bkgd.Clone() #JH : h_Bkgd now has included all backgrounds
        h_Bkgd_TotErr_Min = h_Bkgd.Clone()
        for SystKey in SystematicUps:
          h_Up = SystematicUps[SystKey]
          h_Down = SystematicDowns[SystKey]
          for ix in range(0,h_Bkgd.GetXaxis().GetNbins()):
            x_l = h_Bkgd.GetXaxis().GetBinLowEdge(ix+1)
            x_r = h_Bkgd.GetXaxis().GetBinUpEdge(ix+1)
            y_Central = h_Bkgd.GetBinContent(ix+1)
            y_Up = h_Up.GetBinContent(ix+1)
            y_Down = h_Down.GetBinContent(ix+1)
            ## -.
            y_Max = max( max(y_Central,y_Up), y_Down)
            y_Min = min( min(y_Central,y_Up), y_Down) #JH : with each systematic source, get y_max and y_min
            #print '[%d,%d] : %f, (Max,Min) = (%f,%f)'%(x_l,x_r,y_Central,y_Up,y_Down)

            ## Update Max
            err_Max_Current = h_Bkgd_TotErr_Max.GetBinError(ix+1) #JH : get current error (initially : stat error)
            err_Max_ToAdd = y_Max-y_Central
            err_Max_Updated = math.sqrt( err_Max_Current*err_Max_Current + err_Max_ToAdd*err_Max_ToAdd )
            h_Bkgd_TotErr_Max.SetBinError(ix+1, err_Max_Updated) #JH : update the max error. Note that contents are the same with the original. Only errors updated.
            ## Update Min
            err_Min_Current = h_Bkgd_TotErr_Min.GetBinError(ix+1)
            err_Min_ToAdd = y_Central-y_Min
            err_Min_Updated = math.sqrt( err_Min_Current*err_Min_Current + err_Min_ToAdd*err_Min_ToAdd )
            h_Bkgd_TotErr_Min.SetBinError(ix+1, err_Min_Updated)
        ##==>End Systematic loop

        ## Now call data hist
        if not Region.UnblindData:
          #h_Data = h_Bkgd.Clone(h_Data.GetName())
          h_Data = h_Bkgd.Clone() #JH : data is now the same with the total bkgds
          h_Data.SetMarkerStyle(20)
          h_Data.SetMarkerSize(1.2)
          h_Data.SetMarkerColor(ROOT.kBlack)
          h_Data.SetLineColor(ROOT.kBlack)
        else:
          if self.DoDebug:
            print ('[DEBUG] Trying to get data histogram..')
            print (Region.Name+'/'+'RegionPlots_'+Region.PrimaryDataset + '/'+ Region.ParamName + '/'+Variable.Name)

          histpath = Region.Name+'/' + Region.PrimaryDataset + '/'+ Region.ParamName + '/RegionPlots_' + Region.PrimaryDataset + '/' + Region.HistTag + '/' + Variable.Name #JH : CR naming convention
          #histpath = Region.PrimaryDataset+'/'+Region.ParamName+'/RegionPlots_'+Region.Name+'/'+Variable.Name #JH : MuMu/MVAUL_UL/RegionPlots_DiJetSR3/Lep_1_Pt; SR naming convention.
          #if "LimitInput" in Region.Name and not "BDT" in Region.Name:
          #  histpath = Region.Name+'/'+Region.ParamName+'/FillEventCutflow/'+Region.PrimaryDataset #JH : "LimitInput/MVAUL_UL/FillEventCutflow/MuonSR"
          #elif "LimitInput" in Region.Name and "BDT" in Region.Name:
          #  histpath = Region.Name.split('_')[0]+'/'+Region.ParamName+'/'+Region.Name.split('_')[1]+'/FillEventCutflow/'+Region.PrimaryDataset #JH : "LimitInputBDT/MVAUL_UL/M100/FillEventCutflow/MuonSR"
          #else:
          #  histpath = Region.PrimaryDataset + '/'+ Region.ParamName + '/RegionPlots_'+ Region.Name+'/'+Variable.Name # MuMu/Syst_JetResUpMVAUL_UL/RegionPlots_DiJetSR3/Lep_1_Pt
          h_Data = f_Data.Get(histpath)
          if not h_Data:
            print ("in "+datapath+",") #JH
            print ("No "+histpath)
            print ("==> Skipping ...")
            continue

          ## Make overflow
          h_Data.GetXaxis().SetRangeUser(xMin,xMax)
          h_Data = mylib.MakeOverflowBin(h_Data)

          ## Rebin
          h_Data = self.Rebin(h_Data, Region.Name, Variable.Name, nRebin)

          ### Att data histogram
          h_Data.SetMarkerStyle(20)
          h_Data.SetMarkerSize(1.2)
          h_Data.SetMarkerColor(ROOT.kBlack)
          h_Data.SetLineColor(ROOT.kBlack)

          if self.DoDebug:
            print ('[DEBUG] data histogram finished')
            print ('Data:')
            for z in range(0,h_Data.GetXaxis().GetNbins()):
              x_l = h_Data.GetXaxis().GetBinLowEdge(z+1)
              x_r = h_Data.GetXaxis().GetBinUpEdge(z+1)
              y = h_Data.GetBinContent(z+1)
              print ('[%f,%f] : %f +- %f'%(x_l,x_r,y,h_Data.GetBinError(z+1)))

        ## Copy data axis
        dataAxis = h_Data.GetXaxis()
        nBin = dataAxis.GetNbins()
        xBins = [dataAxis.GetBinLowEdge(1)]
        for ix in range(0,nBin):
          xBins.append( dataAxis.GetBinUpEdge(ix+1) )
        xBins = array("d",xBins)

        ## hist => gr
        gr_Bkgd_TotErr = mylib.GetAsymmError(h_Bkgd_TotErr_Max,h_Bkgd_TotErr_Min) # stat + syst error contained with total bkgd contents
        gr_Data = ROOT.TGraphAsymmErrors(h_Data)

        ## Error from shape # FIXME False as default
        if self.ErrorFromShape:
          if self.DoDebug:
            print ('Total background :')
            for z in range(0,h_TotalBackgroundFromShape.GetXaxis().GetNbins()):
              x_l = h_TotalBackgroundFromShape.GetXaxis().GetBinLowEdge(z+1)
              x_r = h_TotalBackgroundFromShape.GetXaxis().GetBinUpEdge(z+1)
              y = h_TotalBackgroundFromShape.GetBinContent(z+1)
              print ('[%f,%f] : %f +- %f'%(x_l,x_r,y,h_TotalBackgroundFromShape.GetBinError(z+1)))
          gr_Bkgd_TotErr = ROOT.TGraphAsymmErrors(h_TotalBackgroundFromShape)

        err_up_tmp = []
        err_down_tmp = []
        alpha = 1. - 0.6827
        for i in range(0, gr_Data.GetN()): #JH : XXX I don't get this...
          N = gr_Data.GetY()[i]

          L = 0.                                          if (N==0.) else (ROOT.Math.gamma_quantile(alpha/2.,N,1.))
          U = ( ROOT.Math.gamma_quantile_c(alpha,N+1,1) ) if (N==0.) else (ROOT.Math.gamma_quantile_c(alpha/2.,N+1.,1.))

          #print '%d - %f + %f'%(N, N-L, U-N)

          if N!=0:
            gr_Data.SetPointEYlow(i, N-L )
            gr_Data.SetPointEYhigh(i, U-N )
            err_down_tmp.append(N-L)
            err_up_tmp.append(U-N)
            if Variable.Name!="NCand_Mass":
              gr_Data.SetPointEXlow(i, 0)
              gr_Data.SetPointEXhigh(i, 0)
          else:
            zerodata_err_low = 0.1
            zerodata_err_high = 1.8

            xlow = gr_Data.GetX()[i]-gr_Data.GetEXlow()[i]
            xhigh = gr_Data.GetX()[i]+gr_Data.GetEXhigh()[i]
            if self.ZeroDataCheckCut(Variable.Name,xlow,xhigh):
              zerodata_err_low = 0.
              zerodata_err_high = 0.

            gr_Data.SetPointEYlow(i, zerodata_err_low)
            gr_Data.SetPointEYhigh(i, zerodata_err_high)
            err_down_tmp.append(zerodata_err_low)
            err_up_tmp.append(zerodata_err_high)
            if Variable.Name!="NCand_Mass":
              gr_Data.SetPointEXlow(i, 0)
              gr_Data.SetPointEXhigh(i, 0)

        ## Legend
        lg = 0
        ## No signal
        if len(self.SignalsToDraw)==0:
          #lg = ROOT.TLegend(0.55, 0.45, 0.92, 0.90)
          lg = ROOT.TLegend(0.6, 0.55, 0.92, 0.90)
        ## With Signal
        else:
          if Region.DrawRatio:
            #lg = ROOT.TLegend(0.55, 0.46, 0.92, 0.90)
            lg = ROOT.TLegend(0.7, 0.56, 0.92, 0.90) #JH
          else:
            lg = ROOT.TLegend(0.50, 0.56, 0.92, 0.90)
        lg.SetBorderSize(0)
        lg.SetFillStyle(0)

        if not self.NoErrorBand:
          lg.AddEntry(gr_Bkgd_TotErr, "Stat.+syst. uncert.", "f")
        ## dummy graph for legend..
        ## this is because h_Data does not have horizontal error bars,
        ## and gr_data does not have points
        gr_Data_dummy = ROOT.TGraphAsymmErrors(gr_Data)
        gr_Data_dummy.SetMarkerStyle(20)
        gr_Data_dummy.SetMarkerSize(1.2) #JH
        dataLegendGOption="ep"
        if Variable.Name=="NCand_Mass":
          dataLegendGOption="lpe"
        if Region.DrawData:
          if Region.UnblindData:
            lg.AddEntry(gr_Data_dummy, "Data", dataLegendGOption)
          else:
            lg.AddEntry(gr_Data_dummy, "Total background", dataLegendGOption)
        for i_lg in range(0,len(HistsForLegend)):
          #h_lg = HistsForLegend[ len(HistsForLegend)-1-i_lg ][0]
          #tlatexaliax = HistsForLegend[ len(HistsForLegend)-1-i_lg ][1]
          h_lg = HistsForLegend[ i_lg ][0]
          tlatexaliax = HistsForLegend[ i_lg ][1]
          lg.AddEntry(h_lg,tlatexaliax,"f")

        ## Prepare canvas
        c1 = ROOT.TCanvas('c1', '', 800, 800)

        c1_up = ROOT.TPad("c1_up", "", 0, 0.25, 1, 1)
        c1_down = ROOT.TPad("c1_down", "", 0, 0, 1, 0.25)
        if Region.DrawRatio:
          c1, c1_up, c1_down = canvas_margin.canvas_margin(c1, c1_up, c1_down)
          c1.Draw()
          c1_up.Draw()
          c1_down.Draw()

          c1_up.cd()
          if Region.Logy>0:
            c1_up.SetLogy(True)

        else:
          c1_up = ROOT.TPad("c1_up", "", 0, 0, 1, 1)
          c1_up.SetTopMargin( 0.052 )
          c1_up.SetBottomMargin( 0.13 )
          c1_up.SetRightMargin( 0.032 )
          c1_up.SetLeftMargin( 0.15 )
          c1.Draw()
          c1_up.Draw()
          c1_up.cd()

          if Region.Logy>0:
            c1_up.SetLogy(True)

        c1.cd()

        latex_CMSPriliminary = ROOT.TLatex()
        latex_Lumi = ROOT.TLatex()

        latex_CMSPriliminary.SetNDC()
        latex_Lumi.SetNDC()
        latex_CMSPriliminary.SetTextSize(0.035)
        latex_CMSPriliminary.DrawLatex(0.15, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")

        latex_Lumi.SetTextSize(0.035)
        latex_Lumi.SetTextFont(42)
        latex_Lumi.DrawLatex(0.73, 0.96, mylib.TotalLumiByEra(str(self.DataEra))+" fb^{-1} (13 TeV)")

        #### axis histograms

        h_dummy_up = ROOT.TH1D('h_dummy_up', '', nBin, xBins)
        h_dummy_up.GetXaxis().SetRangeUser(xMin, xMax)
        if nRebin>0:
          binsize = h_dummy_up.GetXaxis().GetBinUpEdge(1)-h_dummy_up.GetXaxis().GetBinLowEdge(1)
          str_binsize = '%d'%(binsize)
          if binsize!=int(binsize):
            str_binsize = '%1.2f'%(binsize)
          h_dummy_up.GetYaxis().SetTitle('Events / '+str_binsize+' '+Variable.Unit)
        else:
          h_dummy_up.GetYaxis().SetTitle('Events / bin')
        if Variable.Name=='NCand_Mass':
          h_dummy_up.GetYaxis().SetTitle('Events / bin')

        h_dummy_down = ROOT.TH1D('h_dumy_down', '', nBin, xBins)
        #h_dummy_down.GetYaxis().SetRangeUser(0.,2.)
        h_dummy_down.GetYaxis().SetRangeUser(0.5,1.5)

        if ('DYCR' in Region.Name):
          h_dummy_down.GetYaxis().SetRangeUser(0.70,1.30)
        if ('DYCR2' in Region.Name):
          h_dummy_down.GetYaxis().SetRangeUser(0.50,1.60)

        if (self.ErrorFromShape):
          #if ('DYCR' in Region.Name) and ('PostFit' in self.OutputDirectory):
          if ('DYCR' in Region.Name):
            h_dummy_down.GetYaxis().SetRangeUser(0.70,1.30)
            #h_dummy_down.GetYaxis().SetRangeUser(0.0,2.0)
          else:
            h_dummy_down.GetYaxis().SetRangeUser(0.,2.8)
            #h_dummy_down.GetYaxis().SetRangeUser(0.0,2.0)

        h_dummy_down.SetNdivisions(504,"Y")
        h_dummy_down.GetXaxis().SetRangeUser(xMin, xMax)
        h_dummy_down.GetXaxis().SetTitle(xtitle)
        h_dummy_down.GetYaxis().SetTitle("#frac{Data}{Sim.}")
        h_dummy_down.SetFillColor(0)
        h_dummy_down.SetMarkerSize(0)
        h_dummy_down.SetMarkerStyle(0)
        h_dummy_down.SetLineColor(ROOT.kWhite)

        if Region.DrawRatio:
          h_dummy_up, h_dummy_down = canvas_margin.hist_axis(h_dummy_up, h_dummy_down)
        else:
          h_dummy_up.SetTitle("")
          h_dummy_up.GetYaxis().SetLabelSize(0.04)
          h_dummy_up.GetYaxis().SetTitleSize(0.054)
          h_dummy_up.GetYaxis().SetTitleOffset(1.30)
          h_dummy_up.GetXaxis().SetLabelSize(0.035)
          h_dummy_up.GetXaxis().SetTitleSize(0.055)
          h_dummy_up.GetXaxis().SetTitle(xtitle)

        ## Get Y maximum
        yMax = max( yMax, mylib.GetMaximum(gr_Data) ) #JH
        yMax = max( yMax, mylib.GetMaximum(gr_Bkgd_TotErr) )
        ## Yaxis range
        yMin = 0.
        yMaxScale = 1.2
        if "METPhi" in Variable.Name:
          yMaxScale = 2.

        if Region.Logy>0:
          yMaxScale = 10
          yMin = Region.Logy
        h_dummy_up.GetYaxis().SetRangeUser( yMin, yMaxScale*yMax )

        ## Exception control

        if (Variable.Name=="NCand_Mass"):

          if ("_SR" in Region.Name) and ("EMu" not in Region.Name):
            if ("Resolved" in Region.Name):
              h_dummy_up.GetYaxis().SetRangeUser( 1E-1, yMaxScale*yMax )
            else:
              h_dummy_up.GetYaxis().SetRangeUser( 1, yMaxScale*yMax )
          elif ("_DYCR" in Region.Name):
            if ("Resolved" in Region.Name):
              h_dummy_up.GetYaxis().SetRangeUser( yMin, yMaxScale*yMax )
            else:
              h_dummy_up.GetYaxis().SetRangeUser( yMin, 50*yMax )
          elif ("NoBJet" in Region.Name):
            h_dummy_up.GetYaxis().SetRangeUser( 1E-2, 4*yMax )

        if (Variable.Name=="ZCand_Mass" or Variable.Name=="DiJet_Mass") and ("_DYCR" in Region.Name):
          h_dummy_up.GetYaxis().SetRangeUser(10, 2E5)
        if (Variable.Name=="ZCand_Pt" or Variable.Name=="DiJet_Pt") and ("_DYCR" in Region.Name):
          if ("Resolved" in Region.Name):
            h_dummy_up.GetYaxis().SetRangeUser(10, 5E6)
          else:
            h_dummy_up.GetYaxis().SetRangeUser(10, 2E5)

        if self.DoDebug:
          print ('[DEBUG] Canvas is ready')

        ## Draw up
        c1_up.cd()

        h_dummy_up.Draw("histsame")
        stack_Bkgd.Draw("histsame")

        gr_Bkgd_TotErr.SetMarkerColor(0)
        gr_Bkgd_TotErr.SetMarkerSize(0)
        gr_Bkgd_TotErr.SetFillStyle(3013)
        gr_Bkgd_TotErr.SetFillColor(ROOT.kBlack)
        gr_Bkgd_TotErr.SetLineColor(0)
        if not self.NoErrorBand:
          gr_Bkgd_TotErr.Draw("sameE2")

        gr_Data.SetLineWidth(2)
        gr_Data.SetMarkerSize(0.)
        gr_Data.SetMarkerColor(ROOT.kBlack)
        gr_Data.SetLineColor(ROOT.kBlack)
        if Region.DrawData:
          h_Data.Draw("phistsame")
          gr_Data.Draw("p0same")

        #### 2020/10/14 For the ARC comments
        #for ix in range(0,h_Data.GetXaxis().GetNbins()):
        #  iBin = ix+1
        #  x_l = h_Data.GetXaxis().GetBinLowEdge(iBin)
        #  x_r = h_Data.GetXaxis().GetBinUpEdge(iBin)
        #  y_Data = h_Data.GetBinContent(iBin)
        #  y_Bkgd = h_Bkgd.GetBinContent(iBin)
        #  ratio = y_Data/y_Bkgd
        #  print '%s\t%d\t%d\t%1.2f\t%1.2f\t%1.2f'%(Region.Name, x_l, x_r, y_Data, y_Bkgd, ratio)

        ## Signal
        for Sig in self.SignalsToDraw:
          fpullpath_Sig = Indir+'/'+self.Filename_prefix+Sig.Skim+'_'+Sig.Samples[0]+self.Filename_suffix+'.root'

          f_Sig = ROOT.TFile(fpullpath_Sig)
          #h_Sig = f_Sig.Get(Region.PrimaryDataset+'/'+Region.ParamName+'/RegionPlots_'+Region.Name+'/'+Variable.Name)
          h_Sig = f_Sig.Get(Region.Name+'/' + Region.PrimaryDataset + '_Channel/'+ Region.ParamName + '/RegionPlots_' + Region.PrimaryDataset + '/' + Region.HistTag + '/' + Variable.Name) #JH : SR naming convention
          if not h_Sig:
            print "no",(fpullpath_Sig),"==> Skipping ..."
            #print (Region.PrimaryDataset + '/'+ paramName + '/'+ Region.Name+'/'+Variable.Name)
            continue

          ## Make overflow
          h_Sig.GetXaxis().SetRangeUser(xMin,xMax)
          h_Sig = mylib.MakeOverflowBin(h_Sig)

          ## Rebin
          h_Sig = self.Rebin(h_Sig, Region.Name, Variable.Name, nRebin)

          ## Scale
          h_Sig.Scale( Sig.Scale )
          
          ## Att
          h_Sig.SetLineColor(Sig.Color)
          h_Sig.SetLineStyle(Sig.Style)
          h_Sig.SetLineWidth(Sig.Width)

          ## legend
          lg.AddEntry(h_Sig, Sig.TLatexAlias + ' (V=1) #times'+str(float(Sig.Scale)), 'l')

          ## Draw
          h_Sig.Draw("histsame")

        h_dummy_up.Draw("axissame")

        ## Legend
        lg.Draw()

        ## Draw down
        c1_down.cd()
        h_dummy_down.Draw("histsame")

        ## values must be set later
        h_Data_Ratio = h_Data.Clone('h_Data_Ratio')
        ## BinContent set by divide here, but errors must be set later
        tmp_h_Data_Ratio = h_Data.Clone()
        tmp_h_Data_Ratio.Divide(h_Bkgd)
        gr_Data_Ratio = ROOT.TGraphAsymmErrors(tmp_h_Data_Ratio)
        gr_Data_Ratio.SetName('gr_Data_Ratio')
        gr_Data_Ratio.SetLineWidth(2)
        gr_Data_Ratio.SetMarkerSize(0.)
        gr_Data_Ratio.SetLineColor(ROOT.kBlack)
        ## values must be set later, but BinContent will be simply 1
        gr_Bkgd_Ratio = gr_Bkgd_TotErr.Clone('gr_Bkgd_Ratio')

        for i in range(1,h_Data_Ratio.GetXaxis().GetNbins()+1):

          ## FIXME for zero? how?
          if h_Bkgd.GetBinContent(i)!=0:

            ## ratio point
            ## BinContent = Data/Bkgd
            ## BinError = DataError/Bkgd
            h_Data_Ratio.SetBinContent( i, h_Data_Ratio.GetBinContent(i) / h_Bkgd.GetBinContent(i) )
            h_Data_Ratio.SetBinError ( i, h_Data_Ratio.GetBinError(i) / h_Bkgd.GetBinContent(i) )

            if err_down_tmp[i-1]!=0.:
              gr_Data_Ratio.SetPointEYlow(i-1, err_down_tmp[i-1] / h_Bkgd.GetBinContent(i) )
              gr_Data_Ratio.SetPointEYhigh(i-1, err_up_tmp[i-1] / h_Bkgd.GetBinContent(i))
              if Variable.Name!="NCand_Mass":
                gr_Data_Ratio.SetPointEXlow(i-1, 0)
                gr_Data_Ratio.SetPointEXhigh(i-1, 0)
            else:
              gr_Data_Ratio.SetPointEYlow(i-1, 0)
              gr_Data_Ratio.SetPointEYhigh(i-1, 1.8 / h_Bkgd.GetBinContent(i))
              if Variable.Name!="NCand_Mass":
                gr_Data_Ratio.SetPointEXlow(i-1, 0)
                gr_Data_Ratio.SetPointEXhigh(i-1, 0)

            ## ratio allerr
            ## BinContent = 1
            ## BinError = Bkgd(Stat+Syst)Error/Bkgd
            gr_Bkgd_Ratio.SetPoint(i-1,h_Bkgd.GetXaxis().GetBinCenter(i), 1.)
            gr_Bkgd_Ratio.SetPointEYhigh( i-1, gr_Bkgd_Ratio.GetErrorYhigh(i-1) / h_Bkgd.GetBinContent(i) )
            gr_Bkgd_Ratio.SetPointEYlow( i-1,  gr_Bkgd_Ratio.GetErrorYlow(i-1) / h_Bkgd.GetBinContent(i) )

          elif h_Bkgd.GetBinContent(i)==0. and h_Data_Ratio.GetBinContent(i)==0.:

            h_Data_Ratio.SetBinContent( i, 0 )
            h_Data_Ratio.SetBinError ( i, 0 )
            gr_Data_Ratio.SetPoint(i-1, 0, 0)
            gr_Data_Ratio.SetPointEYlow(i-1, 0)
            gr_Data_Ratio.SetPointEYhigh(i-1, 0)

            gr_Bkgd_Ratio.SetPoint(i-1,h_Bkgd.GetXaxis().GetBinCenter(i), 1.)
            gr_Bkgd_Ratio.SetPointEYhigh( i-1, 0. )
            gr_Bkgd_Ratio.SetPointEYlow( i-1, 0. )

            if Variable.Name!="NCand_Mass":
              gr_Data_Ratio.SetPointEXlow(i-1, 0)
              gr_Data_Ratio.SetPointEXhigh(i-1, 0)

          ## If bkgd <= 0
          else:
            this_max_ratio = 20.0
            this_data = h_Data_Ratio.GetBinContent(i)
            this_data_err = h_Data_Ratio.GetBinError(i)

            h_Data_Ratio.SetBinContent( i, this_max_ratio )
            h_Data_Ratio.SetBinError ( i, this_data_err*this_max_ratio/this_data )

            tmp_x = ctypes.c_double(0.)
            tmp_y = ctypes.c_double(0.)
            #            tmp_x = ROOT.Double(0.)
            #tmp_y = ROOT.Double(0.)
            gr_Data_Ratio.GetPoint(i-1, tmp_x, tmp_y)
            gr_Data_Ratio.SetPoint(i-1, tmp_x, this_max_ratio)
            gr_Data_Ratio.SetPointEYlow(i-1, err_down_tmp[i-1]*this_max_ratio/this_data)
            gr_Data_Ratio.SetPointEYhigh(i-1, err_up_tmp[i-1]*this_max_ratio/this_data)

            gr_Bkgd_Ratio.SetPoint(i-1,h_Bkgd.GetXaxis().GetBinCenter(i), 1.)
            gr_Bkgd_Ratio.SetPointEYhigh( i-1, 0. )
            gr_Bkgd_Ratio.SetPointEYlow( i-1, 0. )

            if Variable.Name!="NCand_Mass":
              gr_Data_Ratio.SetPointEXlow(i-1, 0)
              gr_Data_Ratio.SetPointEXhigh(i-1, 0)
        ##==>End bin loop

        gr_Bkgd_Ratio.SetMarkerColor(0)
        gr_Bkgd_Ratio.SetMarkerSize(0)
        gr_Bkgd_Ratio.SetFillStyle(3013)
        gr_Bkgd_Ratio.SetFillColor(ROOT.kBlack)
        gr_Bkgd_Ratio.SetLineColor(0)
        gr_Bkgd_Ratio.Draw("sameE2") # tot Bkg error / tot Bkg

        h_Data_Ratio.Draw("p9histsame")
        gr_Data_Ratio.Draw("p0same") # data error / tot Bkg

        ## y=1 graph
        g1_x = [-9000, 9000]
        g1_y = [1, 1]
        g1 = ROOT.TGraph(2, array("d", g1_x ), array("d", g1_y ))
        g1.Draw("same")

        ## TLatex
        c1.cd()
        channelname = ROOT.TLatex()
        channelname.SetNDC()
        channelname.SetTextSize(0.037)
        channelname.DrawLatex(0.2, 0.88, "#font[42]{"+Region.TLatexAlias+"}")
        if not Region.UnblindData:
          this_TLatexAlias = Region.TLatexAlias[0:-1]+" (Blinded)}"
          channelname.DrawLatex(0.2, 0.88, "#font[42]{"+this_TLatexAlias+"}") #JH

        ## Extra lines
        exec(self.ExtraLines)

        ## Save
        #c1.SaveAs(Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+Region.HistTag+Region.OutputTag+'.pdf')
        c1.SaveAs(Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'_'+Region.ParamName+Region.OutputTag+'.png') #JH
        print (Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'_'+Region.ParamName+Region.OutputTag+'.png ==> Saved.')

        print(str(self.OutputDirectory))
        if not self.OutputDirectory =="":
          print ('scp ' + Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'.pdf  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
          os.system('scp ' + Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'.pdf  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
          os.system('scp ' + Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'.png  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
          lxplus_dir.append(OutdirLXPLUS)
          

        c1.Close()

      ##==>End Variable loop
      
      if self.DoDebug:
        print ('[DEBUG] All variables are done for this region, closing data TFile')
      f_Data.Close()

    ##==>End Region loop

    print ("List of output dir:")
    for _dir in lxplus_dir:
      htmlname=_dir
      htmlname.replace('/afs/cern.ch/user/j/jalmond/www/','https://jalmond.web.cern.ch/jalmond/')
      print htmlname
    if self.DoDebug:
      print ('[DEBUG] All regions are done.')


###########################################################################################################################################################
  def DoSystCheck(self):

    ObjectTypes = {
                   "DeltaR"  : ["dR_ll"],
                   "Leptons" : ["BScore_BB","BScore_EC","Lep_1_pt","Lep_1_eta","Lep_2_pt","Lep_2_eta"],
                   "Mass"    : ["DiJet_M_W","DiJet_M_l1W","DiJet_M_l2W","DiJet_M_llW"],
                   "NObj"    : ["N_AK4J","N_El","N_Mu"],
                   "SKEvent" : ["Ev_MET","Ev_MET2_ST","Ev_PuppiMET_T1","Ev_PuppiMET_T1ULxyCorr","HToLepPt1","Mt_lep1"],
                   ""        : ["MuonCR","ElectronCR","ElectronMuonCR","MuonSR","ElectronSR","ElectronMuonSR"],
                  }

    # Error print verbosity
    ROOT.gErrorIgnoreLevel = ROOT.kFatal

    tdrstyle.setTDRStyle()
    ROOT.TH1.AddDirectory(False)
    lxplus_dir=[]

    # Loop over regions
    for Region in self.RegionsToDraw:

      print ('## Drawing '+Region.Name)

      ## Read binning data
      Rebins, XaxisRanges = self.ReadBinningInfo(Region.Name)
      if self.DoDebug:
        print ('[DEBUG] Use rebin : ')
        print Rebins
        print ('[DEBUG] Use Xaxis range : ')
        print XaxisRanges

      ## Input/Output directotry
      Indir = Region.InputDirectory
      Outdir = self.OutputDirectoryLocal+'/'+Region.ParamName+'/'+Region.Name+'/'+Region.PrimaryDataset+'/' #JH : /data6/Users/jihkim/HNDiLeptonWorskspace/Output/Plots/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/HNL_ULID/LimitInput/MuMu
      if self.ScaleMC:
        Outdir = self.OutputDirectoryLocal+'/ScaleMC/'+Region.Name+'/'

      if not self.OutputDirectory =="":
        OutdirLXPLUS= self.OutputDirectory +'/'+Region.Name+'/'
        os.system("ssh "+self.Lxplus_User + "@lxplus.cern.ch 'mkdir -p " + OutdirLXPLUS + "'")
        if self.ScaleMC:
          os.system("ssh "+self.Lxplus_User + "@lxplus.cern.ch 'mkdir -p " + self.OutputDirectory +"/ScaleMC/'")
          OutdirLXPLUS= self.OutputDirectory +'/ScaleMC/'+Region.Name+'/'
          os.system("ssh "+self.Lxplus_User + "@lxplus.cern.ch 'mkdir -p " + OutdirLXPLUS + "'")

      print ('##   Outputs => '+Outdir)
      
      os.system('mkdir -p '+Outdir)
      if not self.OutputDirectory =="":
        print('scp ' + os.getenv('HTML_DIR') + '/index.php ' + ''+self.Lxplus_User + '@lxplus.cern.ch:'+ OutdirLXPLUS+'/')
        os.system('scp ' + os.getenv('HTML_DIR') + '/index.php ' + ''+self.Lxplus_User + '@lxplus.cern.ch:'+ OutdirLXPLUS+'/')

      ## Call the data file
      datapath = Indir+'/'+self.DataDirectory+'/'+self.Filename_prefix+'_'+self.Filename_data_skim+'_DATA'+self.Filename_suffix+'.root' #JH : /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_ControlRegionPlotter/2017/DATA/HNL_ControlRegionPlotter_SkimTree_HNMultiLep_DATA.root
      f_Data = ROOT.TFile(datapath)
      if self.DoDebug:
        print ('[DEBUG] Trying to read from data file ' + datapath)

      ## Loop over variables
      for Variable in self.VariablesToDraw:

        ## BinInfo
        nRebin = 1
        
        # Rebin if variable is explicitly defined
        if  Variable.Name in  Rebins.keys():
          print(Variable.Name + ' rebinning to ' + str(Rebins[Variable.Name]))
          nRebin = Rebins[Variable.Name]

        xMin= 0
        xMax=100000.

        # Set X axis range if explicitly defined
        if  Variable.Name in  XaxisRanges.keys():
          xMin = XaxisRanges[Variable.Name][0]
          xMax = XaxisRanges[Variable.Name][1]

        if self.DoDebug:
          print ('[DEBUG] Trying to draw variable = '+Variable.Name)
          print ('[DEBUG] (xMin,xMax) = (%s,%s)'%(xMin,xMax))

        ## xtitle
        xtitle = Variable.TLatexAlias
        if Variable.Name=="NCand_Mass":
          if "Resolved" in Region.Name:
            xtitle = "m_{ljj} (GeV)"
          else:
            xtitle = "m_{lJ} (GeV)"

        # Extra controls for LimitBins
        if "Muon"         in Variable.Name and "Electron" not in Variable.Name and "MuMu" not in Region.PrimaryDataset: continue
        if "Electron"     in Variable.Name and "Muon"     not in Variable.Name and "EE"   not in Region.PrimaryDataset: continue
        if "ElectronMuon" in Variable.Name                                     and "EMu"  not in Region.PrimaryDataset: continue

        # Extra control for Object hist directory matching
        TestInt = 0
        for ObjectType in ObjectTypes.keys():
          if Variable.Name in ObjectTypes[ObjectType]:
            Region.HistTag = ObjectType
            TestInt += 1
        if not TestInt:
          print "[ERROR] There is no matched variable",Variable.Name,"in Object directories."
          print "[ERROR] Please check. Exiting..."
          sys.exit()

        ## Save hists
        ## For legend later..
        HistsToDraw = dict()

        ## Loop over samples
        ## For Legend, save 
        HistsForLegend = []
        AliasForLegend = [] ## Prevent double-counting
        stack_Bkgd = ROOT.THStack("stack_Bkgd", "") # THStack for stacking the backgrounds
        h_Bkgd = 0 # This is also TH1 for total background, will be useful later with total error calculation, ratio devision, ...

        ## Save systematic
        SystematicUps = dict()
        SystematicDowns = dict()
        ## If we take errors from shapes
        h_TotalBackgroundFromShape = 0

        ## Loop over each sample group.
        for SampleGroup in self.SampleGroups:
          Color = SampleGroup.Color
          LegendAdded = False

          ## Loop over each sample in this sample group.
          for Sample in SampleGroup.Samples:

            if self.DoDebug:
              print ('[DEBUG] Trying to make histogram for Sample = '+Sample)

            if 'Fake' in SampleGroup.Type: samplepath = Indir+'RunFake__/DATA/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root'
            elif 'CF' in SampleGroup.Type: samplepath = Indir+'RunCF__/DATA/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root' # /data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/RunCF__/DATA/HNL_SignalRegionPlotter_SkimTree_DileptonBDT_CF.root
            elif 'Conv' in SampleGroup.Type: samplepath = Indir+'RunConv__/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root'
            elif 'Prompt' in SampleGroup.Type: samplepath = Indir+'RunPrompt__/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root'
            else: samplepath = Indir+'/'+self.Filename_prefix+SampleGroup.Skim+'_'+Sample+self.Filename_suffix+'.root'
            f_Sample = ROOT.TFile(samplepath)
            print "opening", samplepath, '...'

            h_Sample = 0

            ## Loop over systematics
            for Syst in self.Systematics:

              if self.DoDebug:
                print ('[DEBUG] Trying to make histogram for Syst = '),
                Syst.Print()

              paramName = Region.ParamName

              # if syst is defined, then call Up or Down shape depending on its Direction.
              if Syst.Name!="Central":
                if not ('Data' in SampleGroup.Type or Syst.Name=="Lumi" or Syst.Name=="GetMCUncertainty"): # Data Bkg has no shape uncertainty. Also Lumi and MC uncert is flat.
                  if Syst.Direction>0:
                    paramName = "Syst_"+Syst.Name+"Up"+Region.ParamName #Syst_JetResUpHNL_ULID
                  else:
                    paramName = "Syst_"+Syst.Name+"Down"+Region.ParamName

              # Define the hist path
              if "LimitInput" in Region.Name and not "BDT" in Region.Name:
                histpath = Region.Name+'/'+Region.PrimaryDataset+'/'+paramName+'/LimitBins/'+Variable.Name #JH : "LimitInput/MuMu/Syst_JetResUpHNL_ULID/LimitBins/MuonSR"
              elif "LimitInput" in Region.Name and "BDT" in Region.Name:
                histpath = Region.Name.split('_')[0]+'/'+Region.PrimaryDataset+'/'+paramName+'/'+Region.Name.split('_')[1]+'/LimitBins/'+Variable.Name #JH : "LimitInputBDT/MuMu/Syst_JetResUpHNL_ULID/M100/LimitBins/MuonSR"
              else:
                histpath = Region.Name+'/'+Region.PrimaryDataset+'/'+paramName+'/RegionPlots_'+Region.PrimaryDataset+'/'+Region.HistTag+'/'+Variable.Name # DiJetSR3/MuMu/Syst_JetResUpHNL_ULID/RegionPlots_MuMu/Leptons/Lep_1_pt

              ## Correlated sources has Syst.Year = -1
              ## Uncorrelated sources has Syst.Year = 2016 or 2017 or 2018
              ## For this cases, SampleGroup.Year should be matched
              if (Syst.Year>0) and (Syst.Year!=SampleGroup.Year):
                print "Systematic year doesn't match to Sample year :"
                print Syst.Year,"vs",SampleGroup.Year
                print "Exiting..."
                sys.exit()
              else:
                h_Sample = f_Sample.Get(histpath)
              print "opening",histpath,"..."

              print h_Sample
              if not h_Sample:
                print 'No hist : %s %s'%(Syst.Name,Sample)
                continue

              ## Make overflow
              h_Sample.GetXaxis().SetRangeUser(xMin,xMax)
              h_Sample = mylib.MakeOverflowBin(h_Sample)

              h_Sample = self.Rebin(h_Sample, Region.Name, Variable.Name, nRebin)
              h_Sample.SetLineColor(Color)
              h_Sample.SetLineWidth(1)
              h_Sample.SetFillColor(Color)

              ## Scale
              MCSF, MCSFerr = 1., 0.
              if self.ScaleMC:
                ## now, only for DY
                if "DYJets" in Sample:
                  MCSF, MCSFerr = mylib.GetDYNormSF(SampleGroup.Year, Region.Name)

              MCSF= mylib.GetNormSF(SampleGroup.Year, Sample)
              h_Sample.Scale( MCSF )

              ## Manual systematic
              ## 1) [Lumi] Uncorrelated
              if Syst.Name=="Lumi":
                lumierr = mylib.LumiError(Syst.Year)
                for ix in range(0,h_Sample.GetXaxis().GetNbins()):
                  y = h_Sample.GetBinContent(ix+1)
                  y_new = y + y*float(Syst.Direction)*lumierr
                  h_Sample.SetBinContent(ix+1, y_new) 
              ## 2) [GetMCUncertainty]
              elif Syst.Name=="GetMCUncertainty":
                mcerr = mylib.GetMCUncertainty(SampleGroup.Name)
                for ix in range(0,h_Sample.GetXaxis().GetNbins()):
                  y = h_Sample.GetBinContent(ix+1)
                  y_new = y + y*float(Syst.Direction)*mcerr
                  h_Sample.SetBinContent(ix+1, y_new)
                  
              ## AddError option
              AddErrorOption = ''
              if self.AddErrorLinear:
                AddErrorOption = 'L'

              ## If central, add to h_Bkgd
              if Syst.Name=="Central" and Sample=='total_background': #FIXME Not used for now.
                if not h_TotalBackgroundFromShape:
                  h_TotalBackgroundFromShape = h_Sample.Clone()
                else:
                  h_TotalBackgroundFromShape = mylib.AddHistograms( h_TotalBackgroundFromShape, h_Sample, AddErrorOption )
                HistsToDraw[Sample] = h_Sample.Clone()

              elif Syst.Name=="Central":
                stack_Bkgd.Add( h_Sample ) # Add this sample to the THStack.
                if not h_Bkgd:
                  h_Bkgd = h_Sample.Clone()
                else:
                  h_Bkgd = mylib.AddHistograms( h_Bkgd, h_Sample, AddErrorOption) # Add this sample to the h_Bkgd.

                HistsToDraw[Sample] = h_Sample.Clone()
                if (not LegendAdded) and (SampleGroup.TLatexAlias not in AliasForLegend):
                  HistsForLegend.append( [HistsToDraw[Sample],SampleGroup.TLatexAlias] )
                  AliasForLegend.append(SampleGroup.TLatexAlias)
                  LegendAdded = True
              ## else (i.e., systematic), add to Total SystUp/Down
              else:
                print ("Adding "+SampleGroup.Name+" to syst " + Syst.Name + ", direction : " + str(Syst.Direction))
                if Syst.Direction>0:
                  if not (Syst.FullName() in SystematicUps.keys()):
                    SystematicUps[Syst.FullName()] = h_Sample.Clone()
                  else:
                    SystematicUps[Syst.FullName()] = mylib.AddHistograms(SystematicUps[Syst.FullName()], h_Sample, AddErrorOption)
                else:
                  if not (Syst.FullName() in SystematicDowns.keys()):
                    SystematicDowns[Syst.FullName()] = h_Sample.Clone()
                  else:
                    SystematicDowns[Syst.FullName()] = mylib.AddHistograms(SystematicDowns[Syst.FullName()], h_Sample, AddErrorOption)

            ##==>End Syst loop

            ## Close file
            f_Sample.Close()

          ##==>End Sample loop
        ##==>End SampleGroup loop
 
        ## Now call data hist
        if not Region.UnblindData:
          h_Data = h_Bkgd.Clone() # Data is now the same with the total bkgds
          h_Data.SetMarkerStyle(20)
          h_Data.SetMarkerSize(1.2)
          h_Data.SetMarkerColor(ROOT.kBlack)
          h_Data.SetLineColor(ROOT.kBlack)
        else:
          h_Data = f_Data.Get(histpath)
          if not h_Data:
            print ("in "+datapath+",")
            print ("No "+histpath)
            print ("==> Skipping ...")
            continue

          ## Make overflow
          h_Data.GetXaxis().SetRangeUser(xMin,xMax)
          h_Data = mylib.MakeOverflowBin(h_Data)

          ## Rebin
          h_Data = self.Rebin(h_Data, Region.Name, Variable.Name, nRebin)

          ### Att data histogram
          h_Data.SetMarkerStyle(20)
          h_Data.SetMarkerSize(1.2)
          h_Data.SetMarkerColor(ROOT.kBlack)
          h_Data.SetLineColor(ROOT.kBlack)

          if self.DoDebug:
            print ('[DEBUG] data histogram finished')
            print ('Data:')
            for z in range(0,h_Data.GetXaxis().GetNbins()):
              x_l = h_Data.GetXaxis().GetBinLowEdge(z+1)
              x_r = h_Data.GetXaxis().GetBinUpEdge(z+1)
              y = h_Data.GetBinContent(z+1)
              print ('[%f,%f] : %f +- %f'%(x_l,x_r,y,h_Data.GetBinError(z+1)))

        ## Copy data axis
        dataAxis = h_Data.GetXaxis()
        nBin = dataAxis.GetNbins()
        xBins = [dataAxis.GetBinLowEdge(1)]
        for ix in range(0,nBin):
          xBins.append( dataAxis.GetBinUpEdge(ix+1) )
        xBins = array("d",xBins)

        ## hist => gr
        gr_Data = ROOT.TGraphAsymmErrors(h_Data)

        err_up_tmp = []
        err_down_tmp = []
        alpha = 1. - 0.6827
        for i in range(0, gr_Data.GetN()):
          N = gr_Data.GetY()[i]

          L = 0.                                          if (N==0.) else (ROOT.Math.gamma_quantile(alpha/2.,N,1.))
          U = ( ROOT.Math.gamma_quantile_c(alpha,N+1,1) ) if (N==0.) else (ROOT.Math.gamma_quantile_c(alpha/2.,N+1.,1.))

          #print '%d - %f + %f'%(N, N-L, U-N)

          if N!=0:
            gr_Data.SetPointEYlow(i, N-L )
            gr_Data.SetPointEYhigh(i, U-N )
            err_down_tmp.append(N-L)
            err_up_tmp.append(U-N)
            if Variable.Name!="NCand_Mass":
              gr_Data.SetPointEXlow(i, 0)
              gr_Data.SetPointEXhigh(i, 0)
          else:
            zerodata_err_low = 0.1
            zerodata_err_high = 1.8

            xlow = gr_Data.GetX()[i]-gr_Data.GetEXlow()[i]
            xhigh = gr_Data.GetX()[i]+gr_Data.GetEXhigh()[i]
            if self.ZeroDataCheckCut(Variable.Name,xlow,xhigh):
              zerodata_err_low = 0.
              zerodata_err_high = 0.

            gr_Data.SetPointEYlow(i, zerodata_err_low)
            gr_Data.SetPointEYhigh(i, zerodata_err_high)
            err_down_tmp.append(zerodata_err_low)
            err_up_tmp.append(zerodata_err_high)
            if Variable.Name!="NCand_Mass":
              gr_Data.SetPointEXlow(i, 0)
              gr_Data.SetPointEXhigh(i, 0)

        ## Prepare canvas
        c1 = ROOT.TCanvas('c1', '', 800, 800)

        c1_up = ROOT.TPad("c1_up", "", 0, 0.25, 1, 1)
        c1_down = ROOT.TPad("c1_down", "", 0, 0, 1, 0.25)
        if Region.DrawRatio:
          c1, c1_up, c1_down = canvas_margin.canvas_margin(c1, c1_up, c1_down)
          c1.Draw()
          c1_up.Draw()
          c1_down.Draw()

          c1_up.cd()
          if Region.Logy>0:
            c1_up.SetLogy(True)

        else:
          c1_up = ROOT.TPad("c1_up", "", 0, 0, 1, 1)
          c1_up.SetTopMargin( 0.052 )
          c1_up.SetBottomMargin( 0.13 )
          c1_up.SetRightMargin( 0.032 )
          c1_up.SetLeftMargin( 0.15 )
          c1.Draw()
          c1_up.Draw()
          c1_up.cd()

          if Region.Logy>0:
            c1_up.SetLogy(True)

        c1.cd()

        latex_CMSPriliminary = ROOT.TLatex()
        latex_Lumi = ROOT.TLatex()

        latex_CMSPriliminary.SetNDC()
        latex_Lumi.SetNDC()
        latex_CMSPriliminary.SetTextSize(0.035)
        latex_CMSPriliminary.DrawLatex(0.15, 0.96, "#font[62]{CMS} #font[42]{#it{#scale[0.8]{Preliminary}}}")

        latex_Lumi.SetTextSize(0.035)
        latex_Lumi.SetTextFont(42)
        latex_Lumi.DrawLatex(0.73, 0.96, mylib.TotalLumiByEra(str(self.DataEra))+" fb^{-1} (13 TeV)")

        #### axis histograms
        h_dummy_up = ROOT.TH1D('h_dummy_up', '', nBin, xBins)
        h_dummy_up.GetXaxis().SetRangeUser(xMin, xMax)
        if nRebin>0:
          binsize = h_dummy_up.GetXaxis().GetBinUpEdge(1)-h_dummy_up.GetXaxis().GetBinLowEdge(1)
          str_binsize = '%d'%(binsize)
          if binsize!=int(binsize):
            str_binsize = '%1.2f'%(binsize)
          h_dummy_up.GetYaxis().SetTitle('Events / '+str_binsize+' '+Variable.Unit)
        else:
          h_dummy_up.GetYaxis().SetTitle('Events / bin')
        if Variable.Name=='NCand_Mass':
          h_dummy_up.GetYaxis().SetTitle('Events / bin')

        h_dummy_down = ROOT.TH1D('h_dumy_down', '', nBin, xBins)
        #h_dummy_down.GetYaxis().SetRangeUser(0.9,1.1)
        h_dummy_down.GetYaxis().SetRangeUser(0,2) #FIXME

        if ('DYCR' in Region.Name):
          h_dummy_down.GetYaxis().SetRangeUser(0.70,1.30)
        if ('DYCR2' in Region.Name):
          h_dummy_down.GetYaxis().SetRangeUser(0.50,1.60)

        if (self.ErrorFromShape):
          #if ('DYCR' in Region.Name) and ('PostFit' in self.OutputDirectory):
          if ('DYCR' in Region.Name):
            h_dummy_down.GetYaxis().SetRangeUser(0.70,1.30)
            #h_dummy_down.GetYaxis().SetRangeUser(0.0,2.0)
          else:
            h_dummy_down.GetYaxis().SetRangeUser(0.,2.8)
            #h_dummy_down.GetYaxis().SetRangeUser(0.0,2.0)

        h_dummy_down.SetNdivisions(504,"Y")
        h_dummy_down.GetXaxis().SetRangeUser(xMin, xMax)
        h_dummy_down.GetXaxis().SetTitle(xtitle)
        h_dummy_down.GetYaxis().SetTitle("#scale[0.8]{#frac{Syst.}{Central}}") #JH
        h_dummy_down.SetFillColor(0)
        h_dummy_down.SetMarkerSize(0)
        h_dummy_down.SetMarkerStyle(0)
        h_dummy_down.SetLineColor(ROOT.kWhite)

        if Region.DrawRatio:
          h_dummy_up, h_dummy_down = canvas_margin.hist_axis(h_dummy_up, h_dummy_down)
        else:
          h_dummy_up.SetTitle("")
          h_dummy_up.GetYaxis().SetLabelSize(0.04)
          h_dummy_up.GetYaxis().SetTitleSize(0.054)
          h_dummy_up.GetYaxis().SetTitleOffset(1.30)
          h_dummy_up.GetXaxis().SetLabelSize(0.035)
          h_dummy_up.GetXaxis().SetTitleSize(0.055)
          h_dummy_up.GetXaxis().SetTitle(xtitle)

        ## Exception control
        if (Variable.Name=="NCand_Mass"):

          if ("_SR" in Region.Name) and ("EMu" not in Region.Name):
            if ("Resolved" in Region.Name):
              h_dummy_up.GetYaxis().SetRangeUser( 1E-1, yMaxScale*yMax )
            else:
              h_dummy_up.GetYaxis().SetRangeUser( 1, yMaxScale*yMax )
          elif ("_DYCR" in Region.Name):
            if ("Resolved" in Region.Name):
              h_dummy_up.GetYaxis().SetRangeUser( yMin, yMaxScale*yMax )
            else:
              h_dummy_up.GetYaxis().SetRangeUser( yMin, 50*yMax )
          elif ("NoBJet" in Region.Name):
            h_dummy_up.GetYaxis().SetRangeUser( 1E-2, 4*yMax )

        if (Variable.Name=="ZCand_Mass" or Variable.Name=="DiJet_Mass") and ("_DYCR" in Region.Name):
          h_dummy_up.GetYaxis().SetRangeUser(10, 2E5)
        if (Variable.Name=="ZCand_Pt" or Variable.Name=="DiJet_Pt") and ("_DYCR" in Region.Name):
          if ("Resolved" in Region.Name):
            h_dummy_up.GetYaxis().SetRangeUser(10, 5E6)
          else:
            h_dummy_up.GetYaxis().SetRangeUser(10, 2E5)

        if self.DoDebug:
          print ('[DEBUG] Canvas is ready')

        ## Loop over systematic sources ==> Why we need syst loop twice? The first one is just calling, then this is to draw it...
        for SystKey in SystematicUps:
          #print SystematicUps
          #print SystKey
          this_systName = SystKey.split('_')[1]

          ## Stat. + Syst. err band
          h_Bkgd_ThisErr_Max = h_Bkgd.Clone()
          h_Bkgd_ThisErr_Min = h_Bkgd.Clone()
          h_Up = SystematicUps[SystKey]
          h_Down = SystematicDowns[SystKey]
          for ix in range(0,h_Bkgd.GetXaxis().GetNbins()):
            x_l = h_Bkgd.GetXaxis().GetBinLowEdge(ix+1)
            x_r = h_Bkgd.GetXaxis().GetBinUpEdge(ix+1)
            y_Central = h_Bkgd.GetBinContent(ix+1)
            y_Up = h_Up.GetBinContent(ix+1)
            y_Down = h_Down.GetBinContent(ix+1)
            ## -.
            y_Max = max( max(y_Central,y_Up), y_Down)
            y_Min = min( min(y_Central,y_Up), y_Down)
            #print '[%d,%d] : %f, (Max,Min) = (%f,%f)'%(x_l,x_r,y_Central,y_Up,y_Down)

            ## Update Max
            err_Max_Current = h_Bkgd_ThisErr_Max.GetBinError(ix+1)
            err_Max_ToAdd = y_Max-y_Central
            err_Max_Updated = math.sqrt( err_Max_Current*err_Max_Current + err_Max_ToAdd*err_Max_ToAdd )
            h_Bkgd_ThisErr_Max.SetBinError(ix+1, err_Max_Updated)
            ## Update Min
            err_Min_Current = h_Bkgd_ThisErr_Min.GetBinError(ix+1)
            err_Min_ToAdd = y_Central-y_Min
            err_Min_Updated = math.sqrt( err_Min_Current*err_Min_Current + err_Min_ToAdd*err_Min_ToAdd )
            h_Bkgd_ThisErr_Min.SetBinError(ix+1, err_Min_Updated)

          gr_Bkgd_ThisErr = mylib.GetAsymmError(h_Bkgd_ThisErr_Max,h_Bkgd_ThisErr_Min)

          ## Get Y maximum according to this stat. + syst. error
          yMax = mylib.GetMaximum(gr_Bkgd_ThisErr)
          ## Yaxis range
          yMin = 0.
          yMaxScale = 1.2
          if "METPhi" in Variable.Name:
            yMaxScale = 2.

          if Region.Logy>0:
            yMaxScale = 10
            yMin = Region.Logy
          h_dummy_up.GetYaxis().SetRangeUser( yMin, yMaxScale*yMax )

          ## Set legend
          lg = 0
          ## No signal
          if len(self.SignalsToDraw)==0:
            #lg = ROOT.TLegend(0.55, 0.45, 0.92, 0.90)
            lg = ROOT.TLegend(0.67, 0.55, 0.92, 0.90)
          ## With Signal
          else:
            if Region.DrawRatio:
              #lg = ROOT.TLegend(0.55, 0.46, 0.92, 0.90)
              lg = ROOT.TLegend(0.65, 0.56, 0.95, 0.90)
            else:
              lg = ROOT.TLegend(0.50, 0.56, 0.92, 0.90)
          lg.SetBorderSize(0)
          lg.SetFillStyle(0)

          if not self.NoErrorBand:
            lg.AddEntry(gr_Bkgd_ThisErr, "Stat.+syst. uncert.", "f")
          ## dummy graph for legend..
          ## this is because h_Data does not have horizontal error bars,
          ## and gr_data does not have points
          gr_Data_dummy = ROOT.TGraphAsymmErrors(gr_Data)
          gr_Data_dummy.SetMarkerStyle(20)
          gr_Data_dummy.SetMarkerSize(1.2)
          dataLegendGOption="ep"
          if Variable.Name=="NCand_Mass":
            dataLegendGOption="lpe"
          if Region.DrawData:
            if Region.UnblindData:
              lg.AddEntry(gr_Data_dummy, "Data", dataLegendGOption)
            else:
              lg.AddEntry(gr_Data_dummy, "Total background", dataLegendGOption)
          for i_lg in range(0,len(HistsForLegend)):
            h_lg = HistsForLegend[ len(HistsForLegend)-1-i_lg ][0]
            tlatexaliax = HistsForLegend[ len(HistsForLegend)-1-i_lg ][1]
            lg.AddEntry(h_lg,tlatexaliax,"f")

          lg.AddEntry(h_Up,   this_systName+" Up", 'l')
          lg.AddEntry(h_Down, this_systName+" Down", 'l')

          ## Draw up
          c1_up.cd()

          h_dummy_up.Draw("hist")
          stack_Bkgd.Draw("histsame")

          h_Up = SystematicUps[SystKey]
          h_Up.SetFillColor(0)
          h_Up.SetLineWidth(2)
          h_Up.SetLineColor(ROOT.kRed)
          h_Up.Draw("histsame")
          h_Down = SystematicDowns[SystKey]
          h_Down.SetFillColor(0)
          h_Down.SetLineWidth(2)
          h_Down.SetLineColor(ROOT.kBlue)
          h_Down.Draw("histsame")
          #print SystKey
          #print h_Up
          #for i in range(h_Up.GetNbinsX()) : print h_Up.GetBinContent(i)

          gr_Bkgd_ThisErr.SetMarkerColor(0)
          gr_Bkgd_ThisErr.SetMarkerSize(0)
          gr_Bkgd_ThisErr.SetFillStyle(3013)
          gr_Bkgd_ThisErr.SetFillColor(ROOT.kBlack)
          gr_Bkgd_ThisErr.SetLineColor(0)
          if not self.NoErrorBand:
            gr_Bkgd_ThisErr.Draw("sameE2")

          gr_Data.SetLineWidth(2)
          gr_Data.SetMarkerSize(0.)
          gr_Data.SetMarkerColor(ROOT.kBlack)
          gr_Data.SetLineColor(ROOT.kBlack)
          if Region.DrawData:
            h_Data.Draw("phistsame")
            gr_Data.Draw("p0same")

          h_dummy_up.Draw("axissame")

          ## Legend
          lg.Draw()

          ## Draw down
          c1_down.cd()
          #h_dummy_down.Draw("histsame")
          h_dummy_down.Draw("hist")

          h_SystUp_Ratio = SystematicUps[SystKey].Clone()
          h_SystUp_Ratio.Divide(h_Bkgd)
          h_SystUp_Ratio.SetMarkerSize(0.)
          h_SystUp_Ratio.SetLineColor(ROOT.kRed)
          h_SystUp_Ratio.SetLineWidth(2)
          h_SystUp_Ratio.Draw("histsame")
          h_SystDown_Ratio = SystematicDowns[SystKey].Clone()
          h_SystDown_Ratio.Divide(h_Bkgd)
          h_SystDown_Ratio.SetMarkerSize(0.)
          h_SystDown_Ratio.SetLineColor(ROOT.kBlue)
          h_SystDown_Ratio.SetLineWidth(2)
          h_SystDown_Ratio.Draw("histsame")

          ## y=1 graph
          g1_x = [-9000, 9000]
          g1_y = [1, 1]
          g1 = ROOT.TGraph(2, array("d", g1_x ), array("d", g1_y ))
          g1.Draw("same")

          ## TLatex
          c1.cd()
          channelname = ROOT.TLatex()
          channelname.SetNDC()
          channelname.SetTextSize(0.037)
          channelname.DrawLatex(0.2, 0.88, "#font[42]{"+Region.TLatexAlias+"}")
          if not Region.UnblindData:
            this_TLatexAlias = Region.TLatexAlias[0:-1]+" (Blinded)}"
            channelname.DrawLatex(0.2, 0.88, "#font[42]{"+this_TLatexAlias+"}")

          ## Signal
          for Sig in self.SignalsToDraw:
            fpullpath_Sig = Indir+'/'+self.Filename_prefix+Sig.Skim+'_'+Sig.Samples[0]+self.Filename_suffix+'.root' #/data6/Users/jihkim/SKFlatOutput/Run2UltraLegacy_v3/HNL_SignalRegionPlotter/2017/HNL_SignalRegionPlotter_SkimTree_HNMultiLepBDT_DYTypeI_DF_M1000_private.root

            # if syst is defined, then call Up or Down shape depending on its Direction.
            paramName_Sig = Region.ParamName
            paramNameUp_Sig = "Syst_"+this_systName+"Up"+Region.ParamName #Syst_JetResUpHNL_ULID
            paramNameDown_Sig = "Syst_"+this_systName+"Down"+Region.ParamName

            # Define the hist path
            if "LimitInput" in Region.Name and not "BDT" in Region.Name:
              histpath_Sig = Region.Name+'/'+Region.PrimaryDataset+'/'+paramName_Sig+'/LimitBins/'+Variable.Name #JH : "LimitInput/MuMu/HNL_ULID/LimitBins/MuonSR"
            elif "LimitInput" in Region.Name and "BDT" in Region.Name:
              histpath_Sig = Region.Name.split('_')[0]+'/'+Region.PrimaryDataset+'/'+paramName_Sig+'/'+Region.Name.split('_')[1]+'/LimitBins/'+Variable.Name #JH : "LimitInputBDT/MuMu/HNL_ULID/M100/LimitBins/MuonSR"
            else:
              histpath_Sig = Region.Name+'/'+Region.PrimaryDataset+'/'+paramName_Sig+'/RegionPlots_'+Region.PrimaryDataset+'/'+Region.HistTag+'/'+Variable.Name # DiJetSR3/MuMu/HNL_ULID/RegionPlots_MuMu/Leptons/Lep_1_pt
            histpathUp_Sig   = histpath_Sig.replace(paramName_Sig,paramNameUp_Sig)
            histpathDown_Sig = histpath_Sig.replace(paramName_Sig,paramNameDown_Sig)

            f_Sig = ROOT.TFile(fpullpath_Sig)
            h_Sig = f_Sig.Get(histpath)
            h_SigUp = f_Sig.Get(histpathUp)
            h_SigDown = f_Sig.Get(histpathDown)
            if not h_Sig:
              print "no", histpath, "in", fpullpath_Sig,"==> Skipping ..."
              continue

            ## Make overflow
            h_Sig.GetXaxis().SetRangeUser(xMin,xMax)
            h_Sig = mylib.MakeOverflowBin(h_Sig)
            h_SigUp.GetXaxis().SetRangeUser(xMin,xMax)
            h_SigUp = mylib.MakeOverflowBin(h_SigUp)
            h_SigDown.GetXaxis().SetRangeUser(xMin,xMax)
            h_SigDown = mylib.MakeOverflowBin(h_SigDown)

            ## Rebin
            h_Sig = self.Rebin(h_Sig, Region.Name, Variable.Name, nRebin)
            h_SigUp = self.Rebin(h_SigUp, Region.Name, Variable.Name, nRebin)
            h_SigDown = self.Rebin(h_SigDown, Region.Name, Variable.Name, nRebin)

            ## Scale
            h_Sig.Scale( Sig.Scale )
            h_SigUp.Scale( Sig.Scale )
            h_SigDown.Scale( Sig.Scale )
            
            ## Att
            h_Sig.SetLineWidth(3)
            h_Sig.SetLineColor(ROOT.kViolet)
            h_SigUp.SetLineWidth(3)
            h_SigUp.SetLineStyle(3)
            h_SigUp.SetLineColor(ROOT.kRed)
            h_SigDown.SetLineWidth(3)
            h_SigDown.SetLineStyle(3)
            h_SigDown.SetLineColor(ROOT.kBlue)

            ## signal legend
            lg.AddEntry(h_Sig, Sig.TLatexAlias + ' (V=1) #times'+str(float(Sig.Scale)), 'l') # Note that the signal xsec were already set to V=1, even though not generated so.

            ## Draw signal
            h_SigUp.Draw("histsame")
            h_SigDown.Draw("histsame")
            h_Sig.Draw("histsame")

            """
          SigSystUp_Ratios = []
          SigSystDown_Ratios = []
          ## Signal
          for Sig in self.SignalsToDraw:
            fpullpath_Sig = Indir+'/'+self.Filename_prefix+Sig.Skim+'_'+Sig.Samples[0]+self.Filename_suffix+'.root'

            f_Sig = ROOT.TFile(fpullpath_Sig)
            h_Sig = f_Sig.Get(Region.PrimaryDataset+'/'+Region.ParamName+'/RegionPlots_'+Region.Name+'/'+Variable.Name)
            h_SigUp = f_Sig.Get(Region.PrimaryDataset+'/'+'Syst_'+SystKey.split('_')[1]+'Up'+Region.ParamName+'/RegionPlots_'+Region.Name+'/'+Variable.Name)
            h_SigDown = f_Sig.Get(Region.PrimaryDataset+'/'+'Syst_'+SystKey.split('_')[1]+'Down'+Region.ParamName+'/RegionPlots_'+Region.Name+'/'+Variable.Name)
            if not h_Sig:
              print "no",(fpullpath_Sig),"==> Skipping ..."
              continue

            ## Make overflow
            h_Sig.GetXaxis().SetRangeUser(xMin,xMax)
            h_Sig = mylib.MakeOverflowBin(h_Sig)
            h_SigUp.GetXaxis().SetRangeUser(xMin,xMax)
            h_SigUp = mylib.MakeOverflowBin(h_SigUp)
            h_SigDown.GetXaxis().SetRangeUser(xMin,xMax)
            h_SigDown = mylib.MakeOverflowBin(h_SigDown)

            ## Rebin
            h_Sig = self.Rebin(h_Sig, Region.Name, Variable.Name, nRebin)
            h_SigUp = self.Rebin(h_SigUp, Region.Name, Variable.Name, nRebin)
            h_SigDown = self.Rebin(h_SigDown, Region.Name, Variable.Name, nRebin)

            ## Scale
            h_Sig.Scale( Sig.Scale )
            h_SigUp.Scale( Sig.Scale )
            h_SigDown.Scale( Sig.Scale )
            #h_Sig.Scale( Sig.xsec * Sig.kfactor * Sig.xsecScale )
            #if Region.PrimaryDataset != "EMu":
            #  print("Scaling xsec by 2. since Signals have E+Mu coupling")
            #  h_Sig.Scale(2.)
            
            ## Att
            h_Sig.SetLineWidth(3)
            #h_Sig.SetLineColor(Sig.Color) #JH : use this option when adding all signals in one plot.
            h_Sig.SetLineColor(ROOT.kViolet) #JH : use specified color for single signal
            #h_SigUp.SetLineWidth(3)
            h_SigUp.SetLineStyle(3)
            h_SigUp.SetLineColor(ROOT.kRed)
            #h_SigDown.SetLineWidth(3)
            h_SigDown.SetLineStyle(3)
            h_SigDown.SetLineColor(ROOT.kBlue)

            h_SigSystUp_Ratio = h_SigUp.Clone()
            h_SigSystUp_Ratio.Divide(h_Sig)
            h_SigSystUp_Ratio.SetMarkerSize(0.)
            h_SigSystUp_Ratio.SetLineColor(ROOT.kRed)
            h_SigSystUp_Ratio.SetLineStyle(3)
            h_SigSystUp_Ratio.SetLineWidth(2)
            h_SigSystDown_Ratio = h_SigDown.Clone()
            h_SigSystDown_Ratio.Divide(h_Sig)
            h_SigSystDown_Ratio.SetMarkerSize(0.)
            h_SigSystDown_Ratio.SetLineColor(ROOT.kBlue)
            h_SigSystUp_Ratio.SetLineStyle(3)
            h_SigSystDown_Ratio.SetLineWidth(2)
            SigSystUp_Ratios.append(h_SigSystUp_Ratio)
            SigSystDown_Ratios.append(h_SigSystDown_Ratio)

            ## legend
            if 'SSWW' in Sig.Name:
              lg.AddEntry(h_Sig, Sig.TLatexAlias + ' (V=1) #times'+str(float(Sig.Scale)), 'l')
            else:
              lg.AddEntry(h_Sig, Sig.TLatexAlias + ' (V=1) #times'+str(Sig.Scale/10000.), 'l')

            ## Draw
            h_SigUp.Draw("histsame")
            h_SigDown.Draw("histsame")
            h_Sig.Draw("histsame")
            """

            h_SigSystUp_Ratio = h_SigUp.Clone()
            h_SigSystUp_Ratio.Divide(h_Sig)
            h_SigSystUp_Ratio.SetMarkerSize(0.)
            h_SigSystUp_Ratio.SetLineColor(ROOT.kRed)
            h_SigSystUp_Ratio.SetLineStyle(3)
            h_SigSystUp_Ratio.SetLineWidth(3)
            h_SigSystUp_Ratio.Draw("histsame")
            h_SigSystDown_Ratio = h_SigDown.Clone()
            h_SigSystDown_Ratio.Divide(h_Sig)
            h_SigSystDown_Ratio.SetMarkerSize(0.)
            h_SigSystDown_Ratio.SetLineColor(ROOT.kBlue)
            h_SigSystDown_Ratio.SetLineStyle(3)
            h_SigSystDown_Ratio.SetLineWidth(3)
            h_SigSystDown_Ratio.Draw("histsame")

            ## Extra lines
            exec(self.ExtraLines)

            ## Save
            outname = Region.Name+'_'+Region.PrimaryDataset+'_'+this_systName+'_'+Sig.Samples[0]+Region.HistTag+Region.OutputTag+'_'+Variable.Name+'.png'
            c1.SaveAs(Outdir+outname)
            print (outname+' ==> Saved.')
          ##==>End Signal loop

          print(str(self.OutputDirectory))
          if not self.OutputDirectory =="":
            print ('scp ' + Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'.pdf  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
            os.system('scp ' + Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'.pdf  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
            os.system('scp ' + Outdir+Variable.Name+'_'+Region.PrimaryDataset+'_'+Region.Name+'.png  '+self.Lxplus_User + '@lxplus.cern.ch:'+OutdirLXPLUS+'/')
            lxplus_dir.append(OutdirLXPLUS)
           
          # Save with no signal
          outname = Region.Name+'_'+Region.PrimaryDataset+'_'+this_systName+'_'+Region.HistTag+Region.OutputTag+Variable.Name+'.png'
          c1.SaveAs(Outdir+outname)
          print (outname+' ==> Saved.')

        ##==>End Syst loop
        c1.Close()

      ##==>End Variable loop
      
      if self.DoDebug:
        print ('[DEBUG] All variables are done for this region, closing data TFile')
      f_Data.Close()

    ##==>End Region loop

    print ("List of output dir:")
    for _dir in lxplus_dir:
      htmlname=_dir
      htmlname.replace('/afs/cern.ch/user/j/jalmond/www/','https://jalmond.web.cern.ch/jalmond/')
      print htmlname
    if self.DoDebug:
      print ('[DEBUG] All regions are done.')
