import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
    
if __name__ == "__main__":

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5


    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')
    BOSkw_func = scipy.interpolate.interp1d(capacity, cost_per_kw, kind='cubic')

    plt.figure(figsize=(3,2.5))
    x = np.linspace(2.5,200,1000)
    plt.plot(x,BOSkw_func(x))
    plt.xlabel("capacity (MW)")
    plt.ylabel("BOS costs ($/kW)")
    plt.subplots_adjust(left=0.2,right=0.99,bottom=0.2,top=0.99)
    plt.savefig("bos_fig.pdf",transparent=True)
    plt.show()


