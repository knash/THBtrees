
rm -rf analysis
echo TEST_h1t1b1defaultsigscale_1pbcenter.root
sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbcenter.root/g' analysis_quick_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
echo TEST_h1t1b1defaultsigscale_1pblow.root
sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pblow.root/g' analysis_quick_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
echo TEST_h1t1b1defaultsigscale_1pbhigh.root
sed 's/RFILE/TEST_h1t1b1defaultsigscale_1pbhigh.root/g' analysis_quick_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py
