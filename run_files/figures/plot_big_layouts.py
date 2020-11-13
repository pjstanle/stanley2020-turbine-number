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

    side = 1600.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)


    plt.figure(figsize=(3.0,5.5))
    plt.subplot(311)
    plt.axis("equal")
    plt.axis("off")

    xf = [1232.40519232, 1266.0908889,  1299.77658548, 1333.46228206, 1367.14797864,
        982.76110921, 1016.44680579, 1050.13250237, 1083.81819895, 1117.50389553,
        733.1170261  , 766.80272268,  800.48841926 , 834.17411584 , 867.85981242,
        483.47294299 , 517.15863957,  550.84433615 , 584.53003272 , 618.2157293,
        233.82885987 , 267.51455645,  301.20025303 , 334.88594961 , 368.57164619,
            0.       ,     0.      ,      0.       ,     0.       ,     0.,
        235.29411765 , 501.96078431,  768.62745098 ,1035.29411765 ,1301.96078431,
        1568.62745098, 1600.       ,  1600.        , 1600.        , 1600.,
        1600.        , 1600.       ,  1364.70588235, 1098.03921569,  831.37254902,
        564.70588235 , 298.03921569,   31.37254902 ,   0.        ]
    yf = [ 374.95501574,  611.1215896 ,  847.28816346 ,1083.45473732, 1319.62131118,
        351.82208474,  587.9886586  , 824.15523246 ,1060.32180632 ,1296.48838018,
        328.68915373,  564.85572759 , 801.02230145 ,1037.18887531 ,1273.35544917,
        305.55622273,  541.72279659 , 777.88937045 ,1014.05594431 ,1250.22251817,
        282.42329172,  518.58986558 , 754.75643944 , 990.9230133  ,1227.08958716,
        501.96078431,  768.62745098 ,1035.29411765 ,1301.96078431 ,1568.62745098,
        1600.       ,  1600.        , 1600.        , 1600.        , 1600.,
        1600.       ,  1364.70588235, 1098.03921569,  831.37254902,  564.70588235,
        298.03921569,   31.37254902 ,   0.         ,   0.         ,   0.,
            0.      ,      0.    ,        0.    ,      235.29411765]

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

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-200.0,3200.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=300)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(1800,600,"objective: AEP\nAEP: 731 GWh\nCOE: 27.40 $/MWh\nprofit: $1.90 million", horizontalalignment="left",verticalalignment="top",fontsize=8)



    plt.subplot(312)
    plt.axis("equal")
    plt.axis("off")

    xf = [   0.         , 252.63157895 ,1263.15789474 , 757.89473684,  336.84210526,
            84.21052632 ,1431.57894737 ,  84.21052632 ,1094.73684211, 1178.94736842,
            84.21052632 ,   0.         ,1263.15789474 ,1010.52631579,    0.,
            336.84210526, 1263.15789474, 1515.78947368, 1600.       ,  1347.36842105,
            589.47368421,   84.21052632]

    yf = [   0.         ,   0.          ,168.42105263  ,252.63157895 , 252.63157895,
            252.63157895 , 421.05263158 , 505.26315789 , 505.26315789,  757.89473684,
            757.89473684 ,1010.52631579 ,1010.52631579 ,1263.15789474, 1347.36842105,
            1347.36842105, 1347.36842105, 1347.36842105, 1600.       ,  1600.,
            1600.        , 1600.        ]

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
    
    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-200.0,3200.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=300)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(1800,600,"objective: COE\nAEP: 465 GWh\nCOE: 20.45 $/MWh\nprofit: $4.44 million", horizontalalignment="left",verticalalignment="top",fontsize=8)


    plt.subplot(313)
    plt.axis("equal")
    plt.axis("off")


    xf = [1170.33443309, 1211.30247876, 1252.27052443, 1293.23857011, 1334.20661578,
            245.99891188 , 286.96695756 , 327.93500323 , 368.9030489,   409.87109457,
                0.       ,     0.      ,      0.     ,       0.    ,        0.,
                0.       ,     0.      ,    266.66666667 , 533.33333333  ,800.,
            1066.66666667, 1333.33333333, 1600.  ,       1600.   ,      1600.,
            1600.        , 1600.       ,  1600.,         1600.  ,       1333.33333333,
            1066.66666667 , 800.       ,   533.33333333 , 266.66666667]

    yf = [3.78200252e+02, 6.22245986e+02, 8.66291720e+02, 1.11033745e+03,
            1.35438319e+03, 2.55107869e+02, 4.99153603e+02, 7.43199338e+02,
            9.87245072e+02, 1.23129081e+03, 0.00000000e+00, 2.66666667e+02,
            5.33333333e+02, 8.00000000e+02, 1.06666667e+03, 1.33333333e+03,
            1.60000000e+03, 1.60000000e+03, 1.60000000e+03, 1.60000000e+03,
            1.60000000e+03, 1.60000000e+03, 1.60000000e+03, 1.33333333e+03,
            1.06666667e+03, 8.00000000e+02, 5.33333333e+02, 2.66666667e+02,
            9.09494702e-13, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
            0.00000000e+00, 0.00000000e+00]

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


    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-200.0,3200.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=300)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(1800,600,"objective: profit\nAEP: 654 GWh\nCOE: 21.68 $/MWh\nprofit: $5.44 million", horizontalalignment="left",verticalalignment="top",fontsize=8)

    plt.subplots_adjust(hspace=0.05,top=0.99,bottom=0.01,left=0.01,right=0.99)

    plt.savefig("big_farms.png",transparent=True)
    plt.show()