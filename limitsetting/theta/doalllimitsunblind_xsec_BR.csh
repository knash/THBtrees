
rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p40p6.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py


rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p80p2.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p60p4.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p20p8.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p70p3.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p30p7.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p10p9.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p90p1.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter1p00p0.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py


rm -rf analysis
sed 's/RFILE/TEST_h1t1b1defaultcenter0p01p0.root/g' analysis_quick_limits_unblind.py > temp_limits.py
python run_theta.py --file=temp_limits.py
