import numpy as np
import matplotlib.pyplot as plt
import scipy
from fuels import * #import everything in fuels.py

# define Properties class for fuels
class Properties():
    def __init__(self, dict):
        self.fif_den: float = dict['fif_den']
        self.bp: float = dict['bp']
        self.fp: float = dict['fp']
        self.k_vis: float = dict['k_vis']
        self.melt: float = dict['melt']
        self.fuel: str = dict['fuel']

# INPUT --- make class object of fuels
all_mats = [Properties(JetA), Properties(HEFA)]

# dictionary for printed property labels
prop_labels = {
    "fif_den": 'Density (15C)',
    "bp": 'Boiling Point',
    "fp": 'Flash Point',
    "k_vis": 'Kinematic Viscosity',
    "melt": 'Melting Point'
}

# dictionary for property units
unit_labels = {
    "fif_den": '$kg/m^3$',
    "bp": 'K',
    "fp": 'K',
    "k_vis": '$mm^2/s$',   
    "melt": 'K'
}

# INPUTS --- 
# weight vectors, tcomp (for LBV use), properties of interest
w_iters = [[0.01, 0.99], [0.2, 0.8], [0.5, 0.5], [0.7, 0.3]]
tcomp = [1, 0.9, 0.8, 0.7, 0.5, 0]
prop1 = 'bp'
prop2 = 'fif_den'

# set up storage arrays for results
res1 = np.zeros(len(tcomp))
res1c = list()
res2c = list()
f1c = list()
f2c = list()

# define LBV function
def LBV(v_frac, prop, materials):
        predict = (materials[0].__dict__[prop]*v_frac) + (materials[1].__dict__[prop]*(1-v_frac))

        return predict

# define error function - percent error squared
def error(v_frac, prop, tcomp, materials):
    
            err_2 = ((LBV(tcomp, prop, materials)-LBV(v_frac, prop, materials))/(LBV(tcomp, prop, materials)))**2

            return err_2 


# loop over every weight iteration
for idx2 in range(0, len(w_iters)):

        # loop over test compositions
        for idx in range(0, len(tcomp)):

                        # define objective function - weighted sum MOO
                        def obj(v_frac):
                                objective = (w_iters[idx2][0]*error(v_frac, prop1, tcomp[idx], all_mats))+(w_iters[idx2][1]*error(v_frac, prop2, tcomp[idx], all_mats))
                                return objective

                        # obtain fuel 1optimized volume fraction from scipy
                        result = scipy.optimize.minimize_scalar(obj)
                
                        # store fuel 1 optimized volume fraction
                        res1[idx] = result.x
        
        # calculate fuel 2 volume fraction
        res2 = [1-item for item in res1]

        # calculate objective value for each optimized volume fraction
        f1 = [obj(item) for item in res1]
        f2 = [obj(item) for item in res2]

        # store each optimized composition in same array
        res1c.append(res1)   
        res2c.append(res2) 

        # store each optimized objective value in same array
        f1c.append(f1)
        f2c.append(f2)

# open plotting figure
f, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True)

# plot decision and objective spaces for each weight vector
ax1.plot(res1c[0], res2c[0], 'o', color='blue')
ax2.plot(f1c[0], f2c[0], 'd', color='blue')
ax1.plot(res1c[1], res2c[1], 'o', color='red')
ax2.plot(f1c[1], f2c[1], 'd', color='red')
ax1.plot(res1c[2], res2c[2], 'o', color='green')
ax2.plot(f1c[2], f2c[2], 'd', color='green')
ax1.plot(res1c[3], res2c[3], 'o', color='yellow', markeredgecolor='black')
ax2.plot(f1c[3], f2c[3], 'd', color='yellow', markeredgecolor='black')
# add plot legend
ax2.legend(w_iters)
# add labels
ax1.set_xlabel( str(all_mats[0].fuel)+' Volume Fraction')
ax1.set_ylabel(str(all_mats[1].fuel)+' Volume Fraction')
ax2.set_xlabel(str(prop_labels[prop1])+' Error')
ax2.set_ylabel(str(prop_labels[prop2])+' Error')
ax1.set_title('Decision Space')
ax2.set_title('Objective Space')
# save plot as .png
plt.savefig(str(all_mats[0].fuel)+'_'+all_mats[1].fuel+'_'+prop1+'_'+prop2+'.png', dpi=600)
# show plot
plt.show()




