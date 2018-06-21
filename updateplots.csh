rm *limits*.txt
cp limitsetting/theta/testexpTEST_h1t1b1defaultsigscale_1pbcenter.txt ./
cat testexpTEST_h1t1b1defaultsigscale_1pbcenter.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./cslimBAYESexpTEST.txt
python limit_plot_shape.py --inputFileExp=cslimBAYESexpTEST.txt  --inputFileObs=NONE --noTheory --useLog  -R center  --outputName=AllHadronic

rm *limits*.txt
cp limitsetting/theta/testexpTEST_h1t1b1defaultsigscale_1pbhigh.txt ./
cat testexpTEST_h1t1b1defaultsigscale_1pbhigh.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./cslimBAYESexpTEST.txt
python limit_plot_shape.py --inputFileExp=cslimBAYESexpTEST.txt  --inputFileObs=NONE --noTheory --useLog -R high  --outputName=AllHadronic

rm *limits*.txt
cp limitsetting/theta/testexpTEST_h1t1b1defaultsigscale_1pblow.txt ./
cat testexpTEST_h1t1b1defaultsigscale_1pblow.txt | grep -v "# x; y; band 0 low; band 0 high; band 1 low; band 1 high" >./cslimBAYESexpTEST.txt
python limit_plot_shape.py --inputFileExp=cslimBAYESexpTEST.txt  --inputFileObs=NONE --noTheory --useLog -R low --outputName=AllHadronic

