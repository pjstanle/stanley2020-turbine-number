import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import scipy.interpolate
    
## Main
if __name__ == "__main__":

    vm = 1.0

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5
    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')

    ppa = 30.0

    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)

    ndirs = 1
    windDirections = np.array([300.0])
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = np.ones(ndirs)
    windFrequencies = windFrequencies/sum(windFrequencies)

    side = 800.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)


    plt.figure(figsize=(3.0,5.5))
    plt.subplot(311)
    plt.axis("equal")
    plt.axis("off")

    # old floris
    # xf = np.array([2.35015070e+02, 6.60582700e-15, 6.11748763e+02, 3.53540931e-16,
    #    4.71104510e+02, 7.16362700e+01, 2.45149184e+02, 6.52901480e+00,
    #    8.00000000e+02, 2.97985394e+02, 8.00000000e+02, 7.38779734e+02,
    #    5.64400000e+02, 7.95092677e+02, 4.47924021e+02, 5.00802981e+02,
    #    2.35569976e+02])
    # yf = np.array([4.78488576e+02, 4.95101210e+02, 4.22735465e+02, 2.35509528e+02,
    #    2.33720751e+02, 7.19546924e+02, 3.88167204e+00, 3.12746040e-14,
    #    5.64400000e+02, 7.90497941e+02, 8.00000000e+02, 8.54093525e-02,
    #    8.00000000e+02, 2.29214851e+02, 5.95204956e+02, 1.31481553e-14,
    #    2.39286916e+02])
    # FIXED FLORIS
    xf = np.array([562.57270716, 554.16502215, 245.55842624, 237.15074124,
         0.        ,   0.        ,   0.        , 250.98039216,
       517.64705882, 784.31372549, 800.        , 800.        ,
       800.        , 549.01960784, 282.35294118,  15.68627451])
    yf = np.array([272.89109995, 545.7821999 , 263.12399426, 536.01509422,
       250.98039216, 517.64705882, 784.31372549, 800.        ,
       800.        , 800.        , 549.01960784, 282.35294118,
        15.68627451,   0.        ,   0.        ,   0.        ])

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))
    floris_model.reinitialize_flow_field(wind_direction=windDirections[0])
    floris_model.reinitialize_flow_field(wind_speed=windSpeeds[0])
    floris_model.calculate_wake()

    nturbs = len(xf)
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om

    COE = cost/AEP
    profit = AEP*ppa - cost
    print(AEP)
    print(COE)
    print(profit)

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-100.0,1600.0),y_bounds=(-100.0,900.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=300)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(900,300,"objective: AEP\nAEP: 301 GWh\nCOE: 23.76 $/MWh\nprofit: $1.88 million", horizontalalignment="left",verticalalignment="top",fontsize=8)



    plt.subplot(312)
    plt.axis("equal")
    plt.axis("off")

    # old floris
    # xf = [  0.   ,      266.66666667 ,533.33333333,   0.   ,      533.33333333,
    #         0.   ,        0. ,        266.66666667, 533.33333333, 800.        ]

    # yf = [  0.   ,        0.    ,      88.88888889, 266.66666667, 355.55555556,
    #         533.33333333, 800.    ,     800.    ,     800.   ,      800.        ]
    # FIXED FLORIS
    xf = np.array([  0. ,        266.66666667, 711.11111111,   0.   ,      266.66666667,
            533.33333333, 800.   ,        0.  ,       266.66666667, 533.33333333,
            800.        ])
    yf = np.array([  0.  ,         0.    ,       0.  ,       266.66666667 ,355.55555556,
            444.44444444, 533.33333333, 622.22222222, 711.11111111, 800.,
            800.        ])

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))
    floris_model.reinitialize_flow_field(wind_direction=windDirections[0])
    floris_model.reinitialize_flow_field(wind_speed=windSpeeds[0])
    floris_model.calculate_wake()

    nturbs = len(xf)
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om

    COE = cost/AEP
    profit = AEP*ppa - cost
    print(AEP)
    print(COE)
    print(profit)
    
    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-100.0,1600.0),y_bounds=(-100.0,900.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=300)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(900,300,"objective: COE\nAEP: 235 GWh\nCOE: 21.84 $/MWh\nprofit: $1.91 million", horizontalalignment="left",verticalalignment="top",fontsize=8)


    plt.subplot(313)
    plt.axis("equal")
    plt.axis("off")

    # old floris
    # xf = [  0. ,        266.66666667, 622.22222222 ,  0. ,        355.55555556,
    #     711.11111111,  88.88888889 ,444.44444444, 800.    ,     177.77777778,
    #     533.33333333, 800.        ]

    # yf = [  0. ,          0.   ,        0.   ,      266.66666667, 266.66666667,
    #     266.66666667 ,533.33333333 ,533.33333333 ,533.33333333 ,800.,
    #     800.      ,   800.        ]
    # FIXED FLORIS
    xf = np.array([507.0005753 , 800.        , 472.07504191,   5.98993809,
       237.05594737, 628.20600253,   1.68871491, 329.00857681,
       271.2310964 ,  16.94695977, 208.91332128, 564.50410731,
       800.        ])
    yf = np.array([2.70444765e+02, 7.99987880e+02, 1.62869968e-14, 7.42217142e+02,
       1.65518265e+01, 5.35111322e+02, 2.70374890e+01, 8.00000000e+02,
       3.02437754e+02, 3.52699159e+02, 5.34819999e+02, 7.92984380e+02,
       3.32728195e+02])

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))
    floris_model.reinitialize_flow_field(wind_direction=windDirections[0])
    floris_model.reinitialize_flow_field(wind_speed=windSpeeds[0])
    floris_model.calculate_wake()

    nturbs = len(xf)
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om

    COE = cost/AEP
    profit = AEP*ppa - cost
    print(AEP)
    print(COE)
    print(profit)


    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-100.0,1600.0),y_bounds=(-100.0,900.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=300)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(900,300,"objective: profit\nAEP: 266 GWh\nCOE: 22.33 $/MWh\nprofit: $2.04 million", horizontalalignment="left",verticalalignment="top",fontsize=8)

    plt.subplots_adjust(hspace=0.05,top=0.99,bottom=0.01,left=0.01,right=0.99)

    plt.savefig("small_farms2.png",transparent=True)
    plt.show()