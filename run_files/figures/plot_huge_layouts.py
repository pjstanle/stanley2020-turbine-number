import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import scipy.interpolate
    
## Main
if __name__ == "__main__":

    wd1 = 270.0
    wd2 = 150.0

    vm = 1.0

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5
    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')

    



    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)

    ndirs_interp = 17
    windDirections_interp = np.linspace(0.0,360.,ndirs_interp)
    windFrequencies_interp = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0,2.0])
    freq_func = scipy.interpolate.interp1d(windDirections_interp, windFrequencies_interp, kind='cubic')
    ndirs = 72
    windDirections = np.linspace(0.0,360.-360./ndirs,ndirs)
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = freq_func(windDirections)
    windFrequencies = windFrequencies/sum(windFrequencies)
    side = 1600.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    ppa = 30.0


    plt.figure(figsize=(6.0,5.5))

    # OLD FLORIS
    # xf =   [1368.57821083, 1354.40775829, 1340.23730576, 1326.06685322, 1311.89640069,
    #         1157.9976943 , 1143.82724177, 1129.65678923, 1115.4863367 , 1101.31588416,
    #         933.24672524 , 919.0762727  , 904.90582017 , 890.73536763 , 876.5649151,
    #         722.66620871 , 708.49575618 , 694.32530364 , 680.1548511  , 665.98439857,
    #         497.91523965 , 483.74478711 , 469.57433458 , 455.40388204 , 441.23342951,
    #         287.33472312 , 273.16427058 , 258.99381805 , 244.82336551 , 230.65291298,
    #             0.       ,     0.       ,     0.       ,     3.1372549,   269.80392157,
    #         536.47058824 , 803.1372549  ,1069.80392157 ,1336.47058824 ,1600.,
    #         1600.        , 1600.        , 1600.        , 1600.        , 1600.,
    #         1596.8627451 , 1330.19607843, 1063.52941176,  796.8627451 ,  530.19607843,
    #         263.52941176 ,   0.         ,   0.         ,   0.        ]
    # yf =  [ 338.70561438 , 594.04408227 , 849.38255015 ,1104.72101803 ,1360.05948591,
    #         217.12689648 , 472.46536436 , 727.80383225 , 983.14230013 ,1238.48076801,
    #         350.88664646 , 606.22511434 , 861.56358222 ,1116.90205011 ,1372.24051799,
    #         229.30792856 , 484.64639644 , 739.98486432 , 995.3233322  ,1250.66180009,
    #         363.06767854 , 618.40614642 , 873.7446143  ,1129.08308218 ,1384.42155007,
    #         241.48896063 , 496.82742851 , 752.1658964  ,1007.50436428 ,1262.84283216,
    #         803.1372549  ,1069.80392157 ,1336.47058824 ,1600.         ,1600.,
    #         1600.        , 1600.        , 1600.        , 1600.        , 1596.8627451,
    #         1330.19607843, 1063.52941176,  796.8627451 ,  530.19607843,  263.52941176,
    #             0.       ,     0.       ,     0.       ,     0.       ,     0.,
    #             0.       ,     3.1372549,   269.80392157,  536.47058824]
    # FIXED FLORIS
    xf = np.array([1102.64269501, 1310.96531776,  684.88422279,  893.20684555,
       1101.52946831, 1309.85209107,  267.12575058,  475.44837334,
        683.77099609,  892.09361885, 1100.41624161, 1308.73886437,
        266.01252388,  474.33514664,  682.6577694 ,  890.98039216,
       1099.30301492, 1307.62563767,  264.89929718,  473.22191994,
        681.5445427 ,  889.86716546, 1098.18978822, 1306.51241098,
        263.78607049,  472.10869325,  680.431316  ,  888.75393876,
        262.67284379,  470.99546655,    0.        ,    0.        ,
          0.        ,    0.        ,   25.09803922,  291.76470588,
        558.43137255,  825.09803922, 1091.76470588, 1358.43137255,
       1600.        , 1600.        , 1600.        , 1600.        ,
       1600.        , 1600.        , 1574.90196078, 1308.23529412,
       1041.56862745,  774.90196078,  508.23529412,  241.56862745,
          0.        ,    0.        ])
    yf = np.array([ 231.25641594,  356.72055009,  233.6915047 ,  359.15563885,
        484.61977299,  610.08390714,  236.12659346,  361.5907276 ,
        487.05486175,  612.51899589,  737.98313004,  863.44726418,
        489.48995051,  614.95408465,  740.4182188 ,  865.88235294,
        991.34648709, 1116.81062123,  742.85330755,  868.3174417 ,
        993.78157584, 1119.24570999, 1244.70984413, 1370.17397828,
        996.2166646 , 1121.68079875, 1247.14493289, 1372.60906704,
       1249.58002165, 1375.04415579,  558.43137255,  825.09803922,
       1091.76470588, 1358.43137255, 1600.        , 1600.        ,
       1600.        , 1600.        , 1600.        , 1600.        ,
       1574.90196078, 1308.23529412, 1041.56862745,  774.90196078,
        508.23529412,  241.56862745,    0.        ,    0.        ,
          0.        ,    0.        ,    0.        ,    0.        ,
         25.09803922,  291.76470588])

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))

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

    plt.subplot(321)
    plt.axis("equal")
    plt.axis("off")

    floris_model.reinitialize_flow_field(wind_direction=wd1)
    floris_model.reinitialize_flow_field(wind_speed=10.0)
    floris_model.calculate_wake()

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-200.0,3200.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=wd1)

    bx = edges[:,0]
    by = edges[:,1]
    bx = np.append(bx,bx[0])
    by = np.append(by,by[0])
    plt.plot(bx,by,"--k",linewidth=0.5)

    


    plt.subplot(322)
    plt.axis("equal")
    plt.axis("off")

    floris_model.reinitialize_flow_field(wind_direction=wd2)
    floris_model.reinitialize_flow_field(wind_speed=10.0)
    floris_model.calculate_wake()

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-1600.0,1800.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=wd2)

    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(-1500,600,"objective: AEP\nAEP: 627 GWh\nCOE: 35.02 $/MWh\nprofit: -$3.15 million", horizontalalignment="left",verticalalignment="top",fontsize=8,color="white")






    # OLD FLORIS
    # xf =  [  84.21052632, 1600.   ,       505.26315789, 1010.52631579, 1600.,
    #         0.       ,  1515.78947368 ,   0.  ,        336.84210526,  842.10526316,
    #     1431.57894737 ,   0.        ]
    # yf =  [   0.          ,  0.        ,   84.21052632,  252.63157895 , 421.05263158,
    #     589.47368421 ,1010.52631579, 1094.73684211, 1263.15789474, 1431.57894737,
    #     1600.       ,  1600.        ]
    # FIXED FLORIS
    xf = np.array([   0.        ,  757.89473684, 1515.78947368, 1600.        ,
          0.        , 1600.        , 1600.        ,    0.        ,
          0.        , 1600.        ,  336.84210526, 1600.        ,
          0.        , 1600.        ,  673.68421053])
    yf = np.array([   0.        ,    0.        ,    0.        ,  252.63157895,
        421.05263158,  505.26315789,  757.89473684,  757.89473684,
       1010.52631579, 1094.73684211, 1347.36842105, 1347.36842105,
       1515.78947368, 1600.        , 1600.        ])

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))

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

    plt.subplot(323)
    plt.axis("equal")
    plt.axis("off")

    floris_model.reinitialize_flow_field(wind_direction=wd1)
    floris_model.reinitialize_flow_field(wind_speed=10.0)
    floris_model.calculate_wake()

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-200.0,3200.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=wd1)

    plt.plot(bx,by,"--k",linewidth=0.5)

   


    plt.subplot(324)
    plt.axis("equal")
    plt.axis("off")

    floris_model.reinitialize_flow_field(wind_direction=wd2)
    floris_model.reinitialize_flow_field(wind_speed=10.0)
    floris_model.calculate_wake()

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-1600.0,1800.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=wd2)

    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(-1500,600,"objective: COE\nAEP: 299 GWh\nCOE: 22.57 $/MWh\nprofit: $2.22 million", horizontalalignment="left",verticalalignment="top",fontsize=8,color="white")



    # OLD FLORIS
    # xf =  [ 505.26315789, 1010.52631579, 1600.          ,  0. ,        1431.57894737,
    #         757.89473684,    0.        , 1600.          ,421.05263158, 1178.94736842,
    #             0.      ,   1600.      ,    926.31578947,  421.05263158, 1600.,
    #             0.      ,    589.47368421, 1600.      ,      0.        , 1094.73684211,
    #         336.84210526, 1600.         ,1178.94736842,  757.89473684  ,  0.        ]
    # yf =  [   0.        ,    0.          ,  0.        ,   84.21052632 , 168.42105263,
    #         252.63157895,  336.84210526  ,336.84210526,  505.26315789 , 505.26315789,
    #         589.47368421,  673.68421053  ,757.89473684,  842.10526316 , 926.31578947,
    #         926.31578947, 1178.94736842, 1178.94736842, 1263.15789474 ,1347.36842105,
    #         1515.78947368, 1515.78947368, 1600. ,        1600.        , 1600.        ]
    # FIXED FLORIS
    xf = np.array([   0.        ,  421.05263158, 1094.73684211, 1600.        ,
       1263.15789474, 1600.        ,    0.        ,  673.68421053,
          0.        , 1600.        ,  252.63157895, 1263.15789474,
          0.        , 1600.        ,  589.47368421,    0.        ,
       1600.        ,    0.        ,  842.10526316, 1431.57894737,
       1600.        , 1094.73684211,  421.05263158,    0.        ])
    yf = np.array([   0.        ,    0.        ,    0.        ,    0.        ,
        168.42105263,  252.63157895,  252.63157895,  421.05263158,
        505.26315789,  505.26315789,  673.68421053,  757.89473684,
        842.10526316,  926.31578947, 1010.52631579, 1094.73684211,
       1178.94736842, 1347.36842105, 1347.36842105, 1431.57894737,
       1600.        , 1600.        , 1600.        , 1600.        ])

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))

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

    plt.subplot(325)
    plt.axis("equal")
    plt.axis("off")

    floris_model.reinitialize_flow_field(wind_direction=wd1)
    floris_model.reinitialize_flow_field(wind_speed=10.0)
    floris_model.calculate_wake()

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-200.0,3200.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=wd1)

    plt.plot(bx,by,"--k",linewidth=0.5)

    


    plt.subplot(326)
    plt.axis("equal")
    plt.axis("off")

    floris_model.reinitialize_flow_field(wind_direction=wd2)
    floris_model.reinitialize_flow_field(wind_speed=10.0)
    floris_model.calculate_wake()

    hor_plane = floris_model.get_hor_plane(x_resolution=500,y_resolution=500,x_bounds=(-1600.0,1800.0),y_bounds=(-200.0,1800.0))

    ax = plt.gca()
    wfct.visualization.visualize_cut_plane(hor_plane, ax=ax,maxSpeed=10.0,minSpeed=vm)
    wfct.visualization.plot_turbines(ax,xf,yf,np.zeros(len(xf)),117.8,wind_direction=wd2)

    plt.plot(bx,by,"--k",linewidth=0.5)

    plt.text(-1500,600,"objective: profit\nAEP: 435 GWh\nCOE: 23.63 $/MWh\nprofit: $2.77 million", horizontalalignment="left",verticalalignment="top",fontsize=8,color="white")




    

    

    plt.subplots_adjust(hspace=0.05,wspace=0.02,top=0.99,bottom=0.01,left=0.01,right=0.99)

    plt.savefig("huge_farms2.png",transparent=True)
    plt.show()