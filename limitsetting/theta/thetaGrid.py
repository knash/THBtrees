# !/bin/python
import subprocess
import glob
import copy
import re
import sys

print 'arguments on the command line are'
print sys.argv

index = int(sys.argv[1]) - 1

print 'Processing index = ' + str(index)


# Unpack the configs
s = 'tar -zxvf analysis.tgz'
print 'executing ' + s
subprocess.call( [s], shell=True )


# Get the analysis files
anaFilesRaw = glob.glob( 'analysis/*quant*.cfg' )
anaFiles = sorted(anaFilesRaw)
print 'All analysis files are : '
print anaFiles
# Pick the one we're running on here. 
anaFile = anaFiles[index]
print 'Will be processing ' + anaFile

# Unpack the gridpack
print 'Unpacking the theta gridpack'
s = 'tar -zxvf gridpack_wpTemplate.tgz'
print 'executing ' + s
subprocess.call( [s], shell=True )


# Now get the name of the logfile and output file
strippedName = copy.copy(anaFile)
strippedNameIndex1 = strippedName.find('/') + 1
strippedNameIndex2 = strippedName.find('.c')
strippedName2 = strippedName[strippedNameIndex1:strippedNameIndex2]
print 'stripped name is ' + strippedName2

# Log file
logNameIndex1 = strippedName2.find('wp')
logNameIndex2 = strippedName2.find('--')
logName = 'debuglog' + strippedName2[logNameIndex1:logNameIndex2] + '.txt'
print 'log name is ' + logName

# Output file
outName = strippedName2 + '.db'
print 'output name is ' + outName


# Execute theta with the given config
s = 'bin/theta ' + anaFile + ' > /dev/null'
print 'executing ' + s
subprocess.call( [s], shell=True )

s = 'ls -trlh'
print 'executing ' + s
subprocess.call( [s], shell=True )

# tar up the results
print 'Tarring up the results to results.tgz'
s = 'tar -cz ' + logName + ' ' + outName + ' > ../results' + str(index)+'.tgz'
files1 = glob.glob( '*quant*.cfg' )
print files1
files1 = glob.glob( '*quant*.db' )
print files1
files1 = glob.glob( '*quant*.txt' )
print files1
print 'executing ' + s
subprocess.call( [s], shell=True )
