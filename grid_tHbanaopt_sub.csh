#! /bin/sh

python Flist.py --istree
tar czvf tarball.tgz Files*.txt THBttree.py THBanalyzer.py Triggerweight_singlemu.root  WprimetoVlq_Functions.py  rootlogon.C THBrate.py THBrate_Maker*.root PileUp_Ratio_*.root 
mv Files*.txt temp

sed 's/RMODS/-c tau32_3/g' anaQCD.listOfJobs > temp.listOfJobs
sed 's/RMODS/-c tau32_3/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c tau32_3/g' anaSIGsmall.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-c tau32_2/g' anaQCD.listOfJobs > temp.listOfJobs
sed 's/RMODS/-c tau32_2/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c tau32_2/g' anaSIGsmall.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-c tau32_1/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c tau32_1/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c tau32_1/g' anaSIGsmall.listOfJobs >> temp.listOfJobs


sed 's/RMODS/-c sjbtagt_0/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagt_0/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagt_0/g' anaSIGsmall.listOfJobs >> temp.listOfJobs

sed 's/RMODS/-c sjbtagt_2/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagt_2/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagt_2/g' anaSIGsmall.listOfJobs >> temp.listOfJobs


sed 's/RMODS/-c sjbtagh_1/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagh_1/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagh_1/g' anaSIGsmall.listOfJobs >> temp.listOfJobs



sed 's/RMODS/-c sjbtagh_2/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagh_2/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagh_2/g' anaSIGsmall.listOfJobs >> temp.listOfJobs



sed 's/RMODS/-c sjbtagh_4/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagh_4/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c sjbtagh_4/g' anaSIGsmall.listOfJobs >> temp.listOfJobs




sed 's/RMODS/-c btag_2/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c btag_2/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c btag_2/g' anaSIGsmall.listOfJobs >> temp.listOfJobs



sed 's/RMODS/-c btag_3/g' anaQCD.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c btag_3/g' anattbar.listOfJobs >> temp.listOfJobs
sed 's/RMODS/-c btag_3/g' anaSIGsmall.listOfJobs >> temp.listOfJobs







./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz \temp.listOfJobs commands.cmd
./runManySections.py --submitCondor commands.cmd
condor_q knash
