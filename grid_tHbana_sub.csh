#! /bin/sh

python Flist.py --istree
tar czvf tarball.tgz Files*.txt THBcorr_QCD__PSET_default.root THBttree.py THBanalyzer.py Triggerweight_singlemu.root  WprimetoVlq_Functions.py  rootlogon.C THBrate.py THBrate_Maker*.root PileUp_Ratio_*.root 
mv Files*.txt temp

sed 's/RMODS//g' anadata.listOfJobs > temp.listOfJobs
sed 's/RMODS//g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS//g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-x off/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-u off/g' anadata.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-J up/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-J down/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R up/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R down/g' anattbar.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-J Mup/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-J Mdown/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R Mup/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R Mdown/g' anattbar.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-u off/g' anattbar.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-J up/g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-J down/g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R up/g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R down/g' anaSIG.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-J Mup/g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-J Mdown/g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R Mup/g' anaSIG.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-R Mdown/g' anaSIG.listOfJobs >> temp.listOfJobs





./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \temp.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q knash
