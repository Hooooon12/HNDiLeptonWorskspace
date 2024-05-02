#!/bin/bash

export VERSION="UltraLegacyV1"
export FLATVERSION=${SKFlatV}
export HNDILEPTONWORKSPACE_DIR=$PWD
export PLOT_PATH=$PWD/Output/Plots/
export OUTFILE_PATH=$HNDILEPTONWORKSPACE_DIR/Output/rootfiles/
export DATACARD_SHAPE_PATH=$HNDILEPTONWORKSPACE_DIR/Limits/DataCardsShape/
export INFILE_MERGED_PATH=$HNDILEPTONWORKSPACE_DIR/Output/OutputTool/MergedFiles/
export SCRIPT_DIR=$HNDILEPTONWORKSPACE_DIR/script/
export HTML_DIR=$PWD/script/HTML

export FILE_MERGED_PATH=$HNDILEPTONWORKSPACE_DIR/InputFiles/MergedFiles/$FLATVERSION/
if [[ ! -d $FILE_MERGED_PATH ]]; then mkdir $FILE_MERGED_PATH ; fi

export FILE_PATH=$HNDILEPTONWORKSPACE_DIR/InputFiles/rootfiles/$FLATVERSION/
export OUTFILE_PATH=$HNDILEPTONWORKSPACE_DIR/Output/rootfiles/$FLATVERSION/


export ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:$HNDILEPTONWORKSPACE_DIR/include/:$HNDILEPTONWORKSPACE_DIR/src/:$HNDILEPTONWORKSPACE_DIR/SignalEfficiency:$HNDILEPTONWORKSPACE_DIR/SignalRegionPlotter:$HNDILEPTONWORKSPACE_DIR/Limit/MakeCards:$HNDILEPTONWORKSPACE_DIR/Output/OutputTool

export PYTHONPATH=$PYTHONPATH:$HNDILEPTONWORKSPACE_DIR/python/:$HNDILEPTONWORKSPACE_DIR/include/
export SCRIPT_DIR=$HNDILEPTONWORKSPACE_DIR/script/

#if [[ $HOSTNAME == "tamsa1" ]];
#then
#    
#    export INFILE_PATH=$SKFlatOutputDir/$SKFlatV/
#    export LIMIT_PATH=$HNDILEPTONWORKSPACE_DIR/LimitCode/CMS-StatisticalTools/:$HNDILEPTONWORKSPACE_DIR/Limits/MakeShapeInput:"/data6/Users/jalmond/Limits/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/data/2016_HNDiLepton/batch/"
#    
#
#else
#
#
#    export PLOT_PATH=/Users/john/Dropbox/HNL_13TeV/DiLepton/plots/
#    export WWW_PLOT_PATH=/tmp/www/html/HNL_13TeV/
#    alias pl='rsync -auv --delete-excluded '$PLOT_PATH/$FLATVERSION' '$WWW_PLOT_PATH
#    alias plforce='rsync -auv -I --delete-excluded output/'$FLATVERSION' '$WWW_PLOT_PATH
#  
#fi


alias lqout='cd '$PLOT_PATH
alias webout='cd '$WWW_PLOT_PATH
alias makehtml='make_html_master --To=HNL_13TeV'
alias makehtml2='make_html_master --To=HNL_13TeV --From=*/'
CurrentGitBranch=`git branch | grep \* | cut -d ' ' -f2`
source bin/BashColorSets.sh

printf "@@@@ Current HNL_Plotter branch : "${BGreen}$CurrentGitBranch${Color_Off}"\n"

alias run="bash "$SCRIPT_DIR"/run.sh"
alias skout='cd '$PLOT_PATH

python python/UsefulTwiki_sites.py
