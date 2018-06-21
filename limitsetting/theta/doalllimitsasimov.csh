

rm -rf analysis
echo TEST_h1t1b1defaultsigscale_1pbcenter.root
sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbcenter.root/g' analysis_quick_limits_asim_bkg.py > temp_limits.py
python run_theta.py --file=temp_limits.py


#rm -rf analysis
#echo TEST_h1t1b1defaultsigscale_1pbcenter.root
#sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbcenter.root/g' analysis_quick_limits_asim.py > temp_limits.py
#python run_theta.py --file=temp_limits.py


#rm -rf analysis
#echo TEST_h1t1b1defaultsigscale_1pbcenter.root
#sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbcenter.root/g' analysis_quick_limits_asim_ttsflow.py > temp_limits.py
#python run_theta.py --file=temp_limits.py



#rm -rf analysis
#echo TEST_h1t1b1defaultsigscale_1pbcenter.root
#sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbcenter.root/g' analysis_quick_limits_asim_ttsfhigh.py > temp_limits.py
#python run_theta.py --file=temp_limits.py




#rm -rf analysis
#echo TEST_h1t1b1defaultsigscale_1pbcenter.root
#sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbcenter.root/g' analysis_quick_limits_asim_bkg.py > temp_limits.py
#python run_theta.py --file=temp_limits.py


#rm -rf analysis
#echo TEST_h1t1b1defaultcenter.root
#sed 's/RFILE/TEST_h1t1b1defaultcenter.root/g' analysis_quick_limits_asim_signomxs.py > temp_limits.py
#python run_theta.py --file=temp_limits.py



