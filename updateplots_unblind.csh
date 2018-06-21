rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultsigscale_1pbcenter.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultsigscale_1pbcenter.txt ./
cat unblinded_expTEST_h1t1b1defaultsigscale_1pbcenter.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./cslim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultsigscale_1pbcenter.txt | grep -v "# x; y; yerror" >./cslim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=cslim_ub_BAYESexpTEST.txt  --inputFileObs=cslim_ub_BAYESobsTEST.txt --noTheory --useLog  -R center  --outputName=AllHadronic




rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultsigscale_1pbhigh.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultsigscale_1pbhigh.txt ./
cat unblinded_expTEST_h1t1b1defaultsigscale_1pbhigh.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./cslim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultsigscale_1pbhigh.txt | grep -v "# x; y; yerror" >./cslim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=cslim_ub_BAYESexpTEST.txt  --inputFileObs=cslim_ub_BAYESobsTEST.txt --noTheory --useLog  -R high  --outputName=AllHadronic


rm *limits*.txt
cp limitsetting/theta/unblinded_expTEST_h1t1b1defaultsigscale_1pblow.txt ./
cp limitsetting/theta/unblinded_obsTEST_h1t1b1defaultsigscale_1pblow.txt ./
cat unblinded_expTEST_h1t1b1defaultsigscale_1pblow.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./cslim_ub_BAYESexpTEST.txt
cat unblinded_obsTEST_h1t1b1defaultsigscale_1pblow.txt | grep -v "# x; y; yerror" >./cslim_ub_BAYESobsTEST.txt
python limit_plot_shape_unblind.py --inputFileExp=cslim_ub_BAYESexpTEST.txt  --inputFileObs=cslim_ub_BAYESobsTEST.txt --noTheory --useLog  -R low  --outputName=AllHadronic








