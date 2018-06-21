
rm -rf analysis
echo TEST_h1t1b1defaultcenter.root
sed 's/RFILE/TEST_h1t1b1defaultcenter.root/g' analysis_quick_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
echo TEST_h1t1b1defaultlow.root
sed 's/RFILE/TEST_h1t1b1defaultlow.root/g' analysis_quick_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
echo TEST_h1t1b1defaulthigh.root
sed 's/RFILE/TEST_h1t1b1defaulthigh.root/g' analysis_quick_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py
