rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronic --batch

rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p90p1.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p90p1.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p90p1.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p90p1.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p90p1 --batch


rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p80p2.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p80p2.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p80p2.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p80p2.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p80p2 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p70p3.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p70p3.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p70p3.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p70p3.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p70p3 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p60p4.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p60p4.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p60p4.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p60p4.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p60p4 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p40p6.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p40p6.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p40p6.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p40p6.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p40p6 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p30p7.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p30p7.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p30p7.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p30p7.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p30p7 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p20p8.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p20p8.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p20p8.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p20p8.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p20p8 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p10p9.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p10p9.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p10p9.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p10p9.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p10p9 --batch




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter0p01p0.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter0p01p0.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter0p01p0.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter0p01p0.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter0p01p0 --batch






rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter1p00p0.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter1p00p0.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter1p00p0.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter1p00p0.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronicTEST_h1t1b1defaultcenter1p00p0 --batch



