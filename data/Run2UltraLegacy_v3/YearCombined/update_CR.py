import os

which = "CR"

files = [
  which+'_rebins.txt',
  which+'_xaxis.txt',
  which+'_yaxis.txt',
]


lines = open('CRRegions.txt').readlines()
varlines = open('Variables.txt').readlines()

rebinlines= open(which+'_rebins.txt').readlines()

updated_rebinfile= open('tmp'+which+'_rebins.txt','w')


for line in lines:
  for varline in varlines:
    tag= line.split()[0] + '\t' + varline.split()[0]
    
    LineExists=False
    for rb in rebinlines:    
      if tag in rb:
        LineExists=True
        break
    
    if LineExists:
      updated_rebinfile.write(rb)
    else:
      updated_rebinfile.write(tag + '\t1\n')

updated_rebinfile.close()

os.system("mv " + 'tmp'+which+'_rebins.txt ' + which+'_rebins.txt') 


axis_lines = open('Xaxis.txt').readlines()
updated_axisfile= open('tmp'+which+'_xaxis.txt','w')
xaxis_regions = open('CR_xaxis.txt').readlines()

for line in lines:
  for axl in axis_lines:
  
    tag= line.split()[0] + '\t' + axl.split()[0] + '\t' + axl.split()[1] + '\t' + axl.split()[2]
    LineExists=False
    for axr in xaxis_regions:
      if tag in axr:
        LineExists=True
        break

    if LineExists:
      updated_axisfile.write(axr)
    else:
      updated_axisfile.write(tag + '\n')

    
updated_axisfile.close()
    

os.system("mv " + 'tmp'+which+'_xaxis.txt ' + which+'_xaxis.txt')
  



