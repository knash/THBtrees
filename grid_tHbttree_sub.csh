#! /bin/sh

python Flist.py
tar czvf tarball.tgz Files*.txt THBttree.py THBanalyzer.py Triggerweight_singlemu.root  WprimetoVlq_Functions.py  rootlogon.C THBrate.py  PileUp_Ratio_*.root 
mv Files*.txt temp
rm temp.listOfJobs
rm TTrees/*.root
#sed 's/Rcuts/sidebandTT/g' tagrate.listOfJobs > temp.listOfJobs
#sed 's/Rcuts/sidebandTTLOOSE/g' tagrate.listOfJobs >> temp.listOfJobs
sed 's/Rcuts/default/g' ttree.listOfJobs > temp.listOfJobs

./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \temp.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q knash
