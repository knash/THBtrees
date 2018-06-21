python THBkin_plotter.py -z h1t1b0 --batch &
python THBkin_plotter.py -z h1t1b1 --batch &

python THBkin_plotter.py -z h1t1b0 --batch -u off &
python THBkin_plotter.py -z h1t1b1 --batch -u off  &

python THBkin_plotter.py -z h1t1b0 -s QCD --batch &
python THBkin_plotter.py -z h1t1b1 -s QCD --batch &

python THBkinvar_plotter.py --batch &

python THBuncplotter.py --batch &

#source updateplots.csh 
source updateplots_unblind_toxsec.csh
source updateplots_unblind_toxsec_BRscan.csh
python limit_plot_shape_combiner.py
