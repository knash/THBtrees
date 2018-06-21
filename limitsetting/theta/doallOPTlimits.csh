

rm -rf analysis
sed 's/RFILE/TEST_OPT_default.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py


rm -rf analysis
sed 's/RFILE/TEST_OPT_tau32_1.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_OPT_tau32_2.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_OPT_sjbtagt_2.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py

rm -rf analysis
sed 's/RFILE/TEST_OPT_sjbtagh_1.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py


rm -rf analysis
sed 's/RFILE/TEST_OPT_sjbtagh_2.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py


rm -rf analysis
sed 's/RFILE/TEST_OPT_sjbtagh_4.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py



rm -rf analysis
sed 's/RFILE/TEST_OPT_btag_2.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py


rm -rf analysis
sed 's/RFILE/TEST_OPT_btag_3.root/g' analysis_opt_limits.py > temp_limits.py
python run_theta.py --file=temp_limits.py




