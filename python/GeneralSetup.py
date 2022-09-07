import os

def check_arg(_arg,tag, script):

   if _arg == None:
      print "#"*30
      print "Need input " + tag
      print "#"*30
      os.system("python " + script  + " -h")
      exit()
   return

def setupargs(version):

   if str(os.getenv("HNDILEPTONWORKSPACE_DIR")) == "None":
       print "setup enviroment...."
       exit()

   import argparse
   import datetime

   if version == "MakePlotter":
      parser = argparse.ArgumentParser(description='option')
      parser.add_argument('-n', dest='Name', default="")
      parser.add_argument('-c', dest='ConfigFile')
      parser.add_argument('--Plots', action='store_true')
      parser.add_argument('--Full', action='store_true')
      args = parser.parse_args()
      return args   
   if version == "MakeCard":
      parser = argparse.ArgumentParser(description='option')
      parser.add_argument('-n', dest='Name', default="")
      parser.add_argument('-c', dest='ConfigFile')
      parser.add_argument('--Plots', action='store_true')
      parser.add_argument('--Full', action='store_true')
      args = parser.parse_args()
      return args
   if version == "MergeCard":
      parser = argparse.ArgumentParser(description='option')
      parser.add_argument('-n', dest='Name', default="")
      parser.add_argument('-c', dest='ConfigFile')
      parser.add_argument('--OnlyCombineYears', action='store_true')
      parser.add_argument('--OnlyCombineBins', action='store_true')
      parser.add_argument('--Full', action='store_true')
      args = parser.parse_args()
      return args

   if version == "ReadCard":
      parser = argparse.ArgumentParser(description='option')
      parser.add_argument('-n', dest='Name', default="")
      parser.add_argument('-i', dest='indir')
      parser.add_argument('-c', dest='ConfigFile')
      parser.add_argument('-j', dest='job_type')
      parser.add_argument('--Full', action='store_true')
      args = parser.parse_args()
      return args


def GetFromConfig(tag):

   ConfigFile = os.environ['HNDILEPTONWORKSPACE_DIR'] + '/PlotterPy/Config.txt'
   ConfigLines = open(ConfigFile,'r').readlines()
   for line in ConfigLines:
      if tag+' ' in line:
         return line.split()[1]
   return ''


def check_limit_reader_path(input_dir,tag):
   file_limit_path= str(os.getenv("LIMIT_PATH"))
   if  input_dir == None:
      print "#"*30
      print "#"*30
      print "Need dir input from following... ad -i dirnam "
      print "#"*30
      print "#"*30
      _list = os.listdir(str(os.getenv("LIMIT_PATH")))
      for l in _list:
         if tag in l:
            print l
            
      exit()

   if not os.path.exists(os.getenv("LIMIT_PATH")+input_dir):
      print "#"*30
      print "#"*30
      print "Incorrect input directory... fix"
      print "#"*30
      print "#"*30
      exit()

def get_lxplus_host():
   os.system("cat ~/.ssh/config > check_connection.txt")

   ch_connect = open("check_connection.txt",'r')

   cpath="/tmp/"
   for line in ch_connect:
      if "ControlPath" in line:
         if "~/ssh" in line:
            cpath="~/"
         elif "/tmp/" in line:
            cpath="/tmp/"
         else:
            print "Modify the  connection since  ControlPath in ~/.ssh/cofig is set to something other than tmp or home dir"

   ch_connect.close()
   os.remove("check_connection.txt")


   os.system("ls " + cpath + " > check_snu_connection.txt")
   snu_connect = open("check_snu_connection.txt",'r')
   connected_lxplus=False
   
   connected_host=""
   for line in snu_connect:
      if "ssh-"+os.getenv("USER")+"@lxplus" in line:
         line_amend=line
         line_amend=line_amend[:-4]
         line_amend=line_amend.replace("ssh-"+os.getenv("USER")+"@","")
         connected_host=line_amend  

   os.remove("check_snu_connection.txt")
   return connected_host

def check_lxplus_connection():

   os.system("cat ~/.ssh/config > check_connection.txt")
    
   ch_connect = open("check_connection.txt",'r')
    
   cpath="/tmp/"
   for line in ch_connect:
      if "ControlPath" in line:
         if "~/ssh" in line:
            cpath="~/"
         elif "/tmp/" in line:
            cpath="/tmp/"
         else:
            print "Modify the  connection since  ControlPath in ~/.ssh/cofig is set to something other than tmp or home dir"
            
   ch_connect.close()
   os.remove("check_connection.txt")
   
    
   os.system("ls " + cpath + " > check_snu_connection.txt")
   snu_connect = open("check_snu_connection.txt",'r')
   connected_lxplus=False
   
   for line in snu_connect:
      if "ssh-"+os.getenv("USER")+"@lxplus" in line:
         connected_lxplus=True
            
   os.remove("check_snu_connection.txt")    
   if connected_lxplus == False:    
      print "No connection to lxplus please make connection in screen and run script again"
      quit()
