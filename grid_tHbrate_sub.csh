#! /bin/sh

python Flist.py --istree
tar czvf tarball.tgz Files*.txt THBttree.py THBanalyzer.py Triggerweight_singlemu.root  WprimetoVlq_Functions.py  rootlogon.C THBrate.py THBrate_Maker*.root PileUp_Ratio_*.root 
mv Files*.txt temp

sed 's/RMODS//g' rate.listOfJobs > temp.listOfJobs

./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \temp.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q knash
