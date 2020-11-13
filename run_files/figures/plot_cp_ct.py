import numpy as np
import matplotlib.pyplot as plt
    
if __name__ == "__main__":

    power = [
          0.107505187,
          0.266432492,
          0.361366981,
          0.411011467,
          0.437455945,
          0.45022894,
          0.456897044,
          0.459942317,
          0.461616131,
          0.462535865,
          0.460486872,
          0.459229395,
          0.444919913,
          0.413358199,
          0.371631559,
          0.323536723,
          0.281393087,
          0.246262316,
          0.216744328,
          0.19176151,
          0.170475284,
          0.152226469,
          0.136492055,
          0.122853483,
          0.110973096,
          0.100576469,
          0.091439014,
          0.08337573,
          0.076233299,
          0.069883932,
          0.064220542,
          0.059152935,
          0.054604782,
          0.050511195,
          0.046816775,
          0.04347403,
          0.04044209,
          0.037610286,
          0.034453066,
          0.031039586,
          0.027704511,
          0.024674821,
          0.02197923,
          0.019514782,
          0.017288499,
          0.015274894,
          0.013472875 
        ]

    thrust = [
          0.827,
          0.826,
          0.817,
          0.808,
          0.8,
          0.794,
          0.791,
          0.789,
          0.786,
          0.77,
          0.741,
          0.698,
          0.647,
          0.593,
          0.539,
          0.485,
          0.433,
          0.383,
          0.337,
          0.296,
          0.26,
          0.229,
          0.203,
          0.182,
          0.163,
          0.148,
          0.134,
          0.123,
          0.113,
          0.105,
          0.098,
          0.092,
          0.084,
          0.082,
          0.079,
          0.073,
          0.066,
          0.059,
          0.053,
          0.048,
          0.043,
          0.039,
          0.035,
          0.031,
          0.029,
          0.026,
          0.023
        ]

    wind_speed = [
          3,
          3.5,
          4,
          4.5,
          5,
          5.5,
          6,
          6.5,
          7,
          7.5,
          8,
          8.5,
          9,
          9.5,
          10,
          10.5,
          11,
          11.5,
          12,
          12.5,
          13,
          13.5,
          14,
          14.5,
          15,
          15.5,
          16,
          16.5,
          17,
          17.5,
          18,
          18.5,
          19,
          19.5,
          20,
          20.5,
          21,
          21.5,
          22,
          22.5,
          23,
          23.5,
          24,
          24.5,
          25,
          25.5,
          26
        ]
    
    plt.figure(figsize=(5.5,2))
    plt.subplot(121)
    plt.plot(wind_speed,power,label=r"$C_P$",color="C0")
    plt.plot(wind_speed,thrust,label=r"$C_T$",color="C3")
    plt.legend(fontsize=8)
    plt.xlabel("wind speed (m/s)")
    plt.subplots_adjust(top=0.99,bottom=0.22,right=0.99,left=0.08,wspace=0.3)
    

    power_curve = np.zeros(len(wind_speed))
    rho = 1.225
    A = 117.8**2/4*np.pi
    for i in range(len(power_curve)):
        power_curve[i] = 0.5*rho*A*wind_speed[i]**3*power[i]

    plt.subplot(122)
    plt.plot(wind_speed,power_curve/1E6,color="C1")
    plt.xlabel("wind speed (m/s)")
    plt.ylabel("power (MW)")
    

    plt.savefig("cp_ct.pdf",transparent=True)
    plt.show()