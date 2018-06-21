rm unblinded*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultcenter.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultcenter.txt ./
cat unblinded_expTEST_h1t1b1defaultcenter.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultcenter.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R center  --outputName=AllHadronic  --batch

rm unblinded*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultlow.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultlow.txt ./
cat unblinded_expTEST_h1t1b1defaultlow.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultlow.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R low  --outputName=AllHadronic  --batch



rm unblinded*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaulthigh.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaulthigh.txt ./
cat unblinded_expTEST_h1t1b1defaulthigh.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./xseclim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaulthigh.txt | grep -v "# x; y; yerror" >./xseclim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=xseclim_ub_BAYESexpTEST.txt  --inputFileObs=xseclim_ub_BAYESobsTEST.txt --useLog  -R high  --outputName=AllHadronic  --batch











