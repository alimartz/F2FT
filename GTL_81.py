import numpy as np
import matplotlib.pyplot as plt
import scipy


class material():
    def __init__(self, rel_den, fif_den, compound):
        self.rel_den: float = rel_den
        self.fif_den: float = fif_den
        self.compound: str = compound







'''hello'''
'''# Shell GTL
s1_dict = {
    "fif_den": 736, #kg/m3
    "bp": 195.2+273.15, #K
    "fp": 43+273.15, #K
    "k_vis": 2.49, #mm2/s
    "melt": -53.8+273.15 #K
}

# JP 8-1
s2_dict= {
    "fif_den": 799.9, #kg/m3
    "bp": 268.1+273.15, #K
    "fp": 47.1+273.15, #K
    "k_vis": 4.347, #mm2/s
    "melt": -50.8+273.15 #K
}
'''

# Jet-A
s1_dict = {
    "rel_den": 0.811,
    "fif_den": 0.8108,
    "bp": 558.15,
    "fp": 318.15,
    "k_vis": 4.502,
    "melt": -42+273.15
}

# HEFA
s2_dict= {
    "rel_den": 0.7615,
    "fif_den": 0.7612,
    "bp": 542.45,
    "fp": 314.15,
    "k_vis": 5.571,
    "melt": -47+273.15
}

all_mats = [material(0.811, 0.8108, 'Jet-A'), material(0.7615, 0.7612, 'HEFA')]



w_iters = [[0.01, 0.99], [0.2, 0.8], [0.5, 0.5], [0.7, 0.3]]
tcomp = [1, 0.9, 0.8, 0.7, 0.5, 0]
prop1 = 'rel_den'
prop2 = 'fif_den'
res1 = np.zeros(len(tcomp))
color = ['blue', 'red']
res1c = list()
res2c = list()
f1c = list()
f2c = list()

def LBV(v_frac, prop, materials):
        predict = (materials[0].__dict__[prop]*v_frac) + (materials[1].__dict__[prop]*(1-v_frac))

        return predict

def error(v_frac, prop, tcomp, materials):
    
            err_2 = ((LBV(tcomp, prop, materials)-LBV(v_frac, prop, materials))/(LBV(tcomp, prop, materials)))**2

            return err_2 


for idx2 in range(0, len(w_iters)):

        for idx in range(0, len(tcomp)):

                        def obj(v_frac):
                                objective = (w_iters[idx2][0]*error(v_frac, prop1, tcomp[idx], all_mats))+(w_iters[idx2][1]*error(v_frac, prop2, tcomp[idx], all_mats))
                                return objective

                        result = scipy.optimize.minimize_scalar(obj)
                
                        res1[idx] = result.x
        
        res2 = [1-item for item in res1]

        f1 = [obj(item) for item in res1]
        f2 = [obj(item) for item in res2]

        res1c.append(res1)   
        res2c.append(res2) 

        f1c.append(f1)
        f2c.append(f2)

        
f, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True)

ax1.plot(res1c[0], res2c[0], 'o', color='blue')
ax2.plot(f1c[0], f2c[0], 'd', color='blue')
ax1.plot(res1c[1], res2c[1], 'o', color='red')
ax2.plot(f1c[1], f2c[1], 'd', color='red')
ax1.plot(res1c[2], res2c[2], 'o', color='green')
ax2.plot(f1c[2], f2c[2], 'd', color='green')
ax1.plot(res1c[3], res2c[3], 'o', color='yellow', markeredgecolor='black')
ax2.plot(f1c[3], f2c[3], 'd', color='yellow', markeredgecolor='black')
ax2.legend(w_iters)
ax1.set_xlabel('Jet A Volume Fraction')
ax1.set_ylabel('HEFA Volume Fraction')
ax2.set_xlabel('Boiling Point Error')
ax2.set_ylabel('Density (15C) Error')
ax1.set_title('Decision Space')
ax2.set_title('Objective Space')
#plt.savefig('HEFA_JetA_bpfifden.png', dpi=600)
plt.show()



'''for idx3 in range(0, len(w_iters)):
        ax1.plot(res1c[idx3], res2c[idx3], 'o', color=color[idx3], markersize=10, hold='on')
        ax2.plot(f1c[idx3], f2c[idx3], 'd', color=color[idx3], markersize=10, hold='on')'''


