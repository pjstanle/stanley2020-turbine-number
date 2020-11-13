import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import scipy.interpolate
    
## Main
if __name__ == "__main__":

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5
    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')

    cost = np.zeros(26)
    narr = np.zeros(26)

    for i in range(len(cost)):
        nturbs = i+1
        narr[i] = nturbs
        tcc = 2500*829*nturbs
        bos = BOS_func(nturbs)
        om = 44*nturbs*2500.0
        fcr = 0.097
        cost[i] = (tcc+bos)*fcr + om

    der = np.zeros(25)
    for i in range(len(der)):
        der[i] = cost[i+1]-cost[i]

    

    plt.figure(figsize=(4.3,2.5))
    plt.subplot(121)
    plt.plot(narr,cost/1E6)

    plt.subplot(122)
    plt.plot(der/1E6)
    plt.show()
    
    