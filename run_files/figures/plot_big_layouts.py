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

    # OLD FLORIS
    # xf = [1232.40519232, 1266.0908889,  1299.77658548, 1333.46228206, 1367.14797864,
    #     982.76110921, 1016.44680579, 1050.13250237, 1083.81819895, 1117.50389553,
    #     733.1170261  , 766.80272268,  800.48841926 , 834.17411584 , 867.85981242,
    #     483.47294299 , 517.15863957,  550.84433615 , 584.53003272 , 618.2157293,
    #     233.82885987 , 267.51455645,  301.20025303 , 334.88594961 , 368.57164619,
    #         0.       ,     0.      ,      0.       ,     0.       ,     0.,
    #     235.29411765 , 501.96078431,  768.62745098 ,1035.29411765 ,1301.96078431,
    #     1568.62745098, 1600.       ,  1600.        , 1600.        , 1600.,
    #     1600.        , 1600.       ,  1364.70588235, 1098.03921569,  831.37254902,
    #     564.70588235 , 298.03921569,   31.37254902 ,   0.        ]
    # yf = [ 374.95501574,  611.1215896 ,  847.28816346 ,1083.45473732, 1319.62131118,
    #     351.82208474,  587.9886586  , 824.15523246 ,1060.32180632 ,1296.48838018,
    #     328.68915373,  564.85572759 , 801.02230145 ,1037.18887531 ,1273.35544917,
    #     305.55622273,  541.72279659 , 777.88937045 ,1014.05594431 ,1250.22251817,
    #     282.42329172,  518.58986558 , 754.75643944 , 990.9230133  ,1227.08958716,
    #     501.96078431,  768.62745098 ,1035.29411765 ,1301.96078431 ,1568.62745098,
    #     1600.       ,  1600.        , 1600.        , 1600.        , 1600.,
    #     1600.       ,  1364.70588235, 1098.03921569,  831.37254902,  564.70588235,
    #     298.03921569,   31.37254902 ,   0.         ,   0.         ,   0.,
    #         0.      ,      0.    ,        0.    ,      235.29411765]
    # FIXED FLORIS
    xf = np.array([ 267.9211523 ,  496.83121049,  293.54465867,  522.45471685,
        751.36477503,  319.16816503,  548.07822321,  776.9882814 ,
       1005.89833958,  344.79167139,  573.70172957,  802.61178776,
       1031.52184594, 1260.43190413,  599.32523593,  828.23529412,
       1057.1453523 , 1286.05541049,  853.85880048, 1082.76885866,
       1311.67891685, 1108.39236502, 1337.30242321, 1362.92592957,
          0.        ,    0.        ,    0.        ,    0.        ,
          0.        ,  235.29411765,  501.96078431,  768.62745098,
       1035.29411765, 1301.96078431, 1568.62745098, 1600.        ,
       1600.        , 1600.        , 1600.        , 1600.        ,
       1600.        , 1364.70588235, 1098.03921569,  831.37254902,
        564.70588235,  298.03921569,   31.37254902,    0.        ])

    yf = np.array([ 471.94412336,  241.61962156,  731.08112773,  500.75662593,
        270.43212414,  990.2181321 ,  759.89363031,  529.56912851,
        299.24462672, 1249.35513647, 1019.03063468,  788.70613288,
        558.38163109,  328.05712929, 1278.16763905, 1047.84313725,
        817.51863546,  587.19413367, 1306.98014163, 1076.65563983,
        846.33113804, 1335.7926442 , 1105.46814241, 1364.60514678,
        501.96078431,  768.62745098, 1035.29411765, 1301.96078431,
       1568.62745098, 1600.        , 1600.        , 1600.        ,
       1600.        , 1600.        , 1600.        , 1364.70588235,
       1098.03921569,  831.37254902,  564.70588235,  298.03921569,
         31.37254902,    0.        ,    0.        ,    0.        ,
          0.        ,    0.        ,    0.        ,  235.29411765])

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

    plt.text(1800,600,"objective: AEP\nAEP: 721 GWh\nCOE: 27.23 $/MWh\nprofit: $1.99 million", horizontalalignment="left",verticalalignment="top",fontsize=8)



    plt.subplot(312)
    plt.axis("equal")
    plt.axis("off")

    # OLD FLORIS
    # xf = [   0.         , 252.63157895 ,1263.15789474 , 757.89473684,  336.84210526,
    #         84.21052632 ,1431.57894737 ,  84.21052632 ,1094.73684211, 1178.94736842,
    #         84.21052632 ,   0.         ,1263.15789474 ,1010.52631579,    0.,
    #         336.84210526, 1263.15789474, 1515.78947368, 1600.       ,  1347.36842105,
    #         589.47368421,   84.21052632]

    # yf = [   0.         ,   0.          ,168.42105263  ,252.63157895 , 252.63157895,
    #         252.63157895 , 421.05263158 , 505.26315789 , 505.26315789,  757.89473684,
    #         757.89473684 ,1010.52631579 ,1010.52631579 ,1263.15789474, 1347.36842105,
    #         1347.36842105, 1347.36842105, 1347.36842105, 1600.       ,  1600.,
    #         1600.        , 1600.        ]

    # FIXED FLORIS
    xf = np.array([   0.        ,  252.63157895,  589.47368421,  842.10526316,
       1094.73684211, 1347.36842105, 1600.        , 1600.        ,
       1347.36842105,    0.        , 1515.78947368, 1263.15789474,
       1263.15789474, 1515.78947368, 1600.        , 1347.36842105,
       1347.36842105, 1600.        , 1600.        , 1347.36842105])
    yf = np.array([   0.        ,    0.        ,    0.        ,    0.        ,
          0.        ,    0.        ,    0.        ,  252.63157895,
        252.63157895,  252.63157895,  589.47368421,  589.47368421,
        842.10526316,  842.10526316, 1094.73684211, 1094.73684211,
       1347.36842105, 1347.36842105, 1600.        , 1600.        ])

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

    plt.text(1800,600,"objective: COE\nAEP: 428 GWh\nCOE: 20.37 $/MWh\nprofit: $4.12 million", horizontalalignment="left",verticalalignment="top",fontsize=8)


    plt.subplot(313)
    plt.axis("equal")
    plt.axis("off")

    # OLD FLORIS
    # xf = [1170.33443309, 1211.30247876, 1252.27052443, 1293.23857011, 1334.20661578,
    #         245.99891188 , 286.96695756 , 327.93500323 , 368.9030489,   409.87109457,
    #             0.       ,     0.      ,      0.     ,       0.    ,        0.,
    #             0.       ,     0.      ,    266.66666667 , 533.33333333  ,800.,
    #         1066.66666667, 1333.33333333, 1600.  ,       1600.   ,      1600.,
    #         1600.        , 1600.       ,  1600.,         1600.  ,       1333.33333333,
    #         1066.66666667 , 800.       ,   533.33333333 , 266.66666667]

    # yf = [3.78200252e+02, 6.22245986e+02, 8.66291720e+02, 1.11033745e+03,
    #         1.35438319e+03, 2.55107869e+02, 4.99153603e+02, 7.43199338e+02,
    #         9.87245072e+02, 1.23129081e+03, 0.00000000e+00, 2.66666667e+02,
    #         5.33333333e+02, 8.00000000e+02, 1.06666667e+03, 1.33333333e+03,
    #         1.60000000e+03, 1.60000000e+03, 1.60000000e+03, 1.60000000e+03,
    #         1.60000000e+03, 1.60000000e+03, 1.60000000e+03, 1.33333333e+03,
    #         1.06666667e+03, 8.00000000e+02, 5.33333333e+02, 2.66666667e+02,
    #         9.09494702e-13, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    #         0.00000000e+00, 0.00000000e+00]

    # FIXED FLORIS
    xf = np.array([ 356.18337277,  450.71530685,  545.24724092,  736.40990714,
        830.94184121,  925.47377528, 1116.6364415 , 1211.16837557,
       1305.70030965,    0.        ,    0.        ,    0.        ,
        260.39215686,  527.05882353,  793.7254902 , 1060.39215686,
       1327.05882353, 1593.7254902 , 1600.        , 1600.        ,
       1600.        , 1600.        , 1600.        , 1600.        ,
       1339.60784314, 1072.94117647,  806.2745098 ,  539.60784314,
        272.94117647,    6.2745098 ,    0.        ,    0.        ,
          0.        ])
    yf = np.array([ 952.38711696,  661.44773972,  370.50836249, 1075.930207  ,
        784.99082977,  494.05145253, 1199.47329705,  908.53391981,
        617.59454258, 1060.39215686, 1327.05882353, 1593.7254902 ,
       1600.        , 1600.        , 1600.        , 1600.        ,
       1600.        , 1600.        , 1339.60784314, 1072.94117647,
        806.2745098 ,  539.60784314,  272.94117647,    6.2745098 ,
          0.        ,    0.        ,    0.        ,    0.        ,
          0.        ,    0.        ,  260.39215686,  527.05882353,
        793.7254902 ])
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

    plt.text(1800,600,"objective: profit\nAEP: 629 GWh\nCOE: 21.92 $/MWh\nprofit: $5.09 million", horizontalalignment="left",verticalalignment="top",fontsize=8)

    plt.subplots_adjust(hspace=0.05,top=0.99,bottom=0.01,left=0.01,right=0.99)

    plt.savefig("big_farms2.png",transparent=True)
    plt.show()