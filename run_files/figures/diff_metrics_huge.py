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

    floris_model.reinitialize_flow_field(layout_array=([0],[0]))
    AEP0 = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6

    xf =   [1368.57821083, 1354.40775829, 1340.23730576, 1326.06685322, 1311.89640069,
            1157.9976943 , 1143.82724177, 1129.65678923, 1115.4863367 , 1101.31588416,
            933.24672524 , 919.0762727  , 904.90582017 , 890.73536763 , 876.5649151,
            722.66620871 , 708.49575618 , 694.32530364 , 680.1548511  , 665.98439857,
            497.91523965 , 483.74478711 , 469.57433458 , 455.40388204 , 441.23342951,
            287.33472312 , 273.16427058 , 258.99381805 , 244.82336551 , 230.65291298,
                0.       ,     0.       ,     0.       ,     3.1372549,   269.80392157,
            536.47058824 , 803.1372549  ,1069.80392157 ,1336.47058824 ,1600.,
            1600.        , 1600.        , 1600.        , 1600.        , 1600.,
            1596.8627451 , 1330.19607843, 1063.52941176,  796.8627451 ,  530.19607843,
            263.52941176 ,   0.         ,   0.         ,   0.        ]
    yf =  [ 338.70561438 , 594.04408227 , 849.38255015 ,1104.72101803 ,1360.05948591,
            217.12689648 , 472.46536436 , 727.80383225 , 983.14230013 ,1238.48076801,
            350.88664646 , 606.22511434 , 861.56358222 ,1116.90205011 ,1372.24051799,
            229.30792856 , 484.64639644 , 739.98486432 , 995.3233322  ,1250.66180009,
            363.06767854 , 618.40614642 , 873.7446143  ,1129.08308218 ,1384.42155007,
            241.48896063 , 496.82742851 , 752.1658964  ,1007.50436428 ,1262.84283216,
            803.1372549  ,1069.80392157 ,1336.47058824 ,1600.         ,1600.,
            1600.        , 1600.        , 1600.        , 1600.        , 1596.8627451,
            1330.19607843, 1063.52941176,  796.8627451 ,  530.19607843,  263.52941176,
                0.       ,     0.       ,     0.       ,     0.       ,     0.,
                0.       ,     3.1372549,   269.80392157,  536.47058824]

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))

    nturbs_AEP = len(xf)
    AEP_AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs_AEP
    bos = BOS_func(nturbs_AEP)
    om = 44*nturbs_AEP*2500.0
    fcr = 0.097
    cost_AEP = (tcc+bos)*fcr + om

    COE_AEP = cost_AEP/AEP_AEP
    profit_AEP = AEP_AEP*ppa - cost_AEP



    xf =  [  84.21052632, 1600.   ,       505.26315789, 1010.52631579, 1600.,
            0.       ,  1515.78947368 ,   0.  ,        336.84210526,  842.10526316,
        1431.57894737 ,   0.        ]
    yf =  [   0.          ,  0.        ,   84.21052632,  252.63157895 , 421.05263158,
        589.47368421 ,1010.52631579, 1094.73684211, 1263.15789474, 1431.57894737,
        1600.       ,  1600.        ]

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))

    nturbs_COE = len(xf)
    AEP_COE = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs_COE
    bos = BOS_func(nturbs_COE)
    om = 44*nturbs_COE*2500.0
    fcr = 0.097
    cost_COE = (tcc+bos)*fcr + om

    COE_COE = cost_COE/AEP_COE
    profit_COE = AEP_COE*ppa - cost_COE



    xf =  [ 505.26315789, 1010.52631579, 1600.          ,  0. ,        1431.57894737,
            757.89473684,    0.        , 1600.          ,421.05263158, 1178.94736842,
                0.      ,   1600.      ,    926.31578947,  421.05263158, 1600.,
                0.      ,    589.47368421, 1600.      ,      0.        , 1094.73684211,
            336.84210526, 1600.         ,1178.94736842,  757.89473684  ,  0.        ]
    yf =  [   0.        ,    0.          ,  0.        ,   84.21052632 , 168.42105263,
            252.63157895,  336.84210526  ,336.84210526,  505.26315789 , 505.26315789,
            589.47368421,  673.68421053  ,757.89473684,  842.10526316 , 926.31578947,
            926.31578947, 1178.94736842, 1178.94736842, 1263.15789474 ,1347.36842105,
            1515.78947368, 1515.78947368, 1600. ,        1600.        , 1600.        ]

    floris_model.reinitialize_flow_field(layout_array=(xf,yf))

    nturbs_profit = len(xf)
    AEP_profit = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs_profit
    bos = BOS_func(nturbs_profit)
    om = 44*nturbs_profit*2500.0
    fcr = 0.097
    cost_profit = (tcc+bos)*fcr + om

    COE_profit = cost_profit/AEP_profit
    profit_profit = AEP_profit*ppa - cost_profit


    # AEP
    # COE
    # profit
    # nturbs
    # cost
    # spacing
    # power density
    # wake loss

    D = 117.8
    spacing_AEP = side/D/(np.sqrt(nturbs_AEP)-1.0)
    spacing_COE = side/D/(np.sqrt(nturbs_COE)-1.0)
    spacing_profit = side/D/(np.sqrt(nturbs_profit)-1.0)

    wake_loss_AEP = 1.0 - (AEP_AEP/(nturbs_AEP*AEP0))
    wake_loss_COE = 1.0 - (AEP_COE/(nturbs_COE*AEP0))
    wake_loss_profit = 1.0 - (AEP_profit/(nturbs_profit*AEP0))
    
    labels = ['AEP\n(GWh)', 'COE\n($/MWh)', 'profit\n($MM/yr)', 'num.\nturbines', 'cost\n($MM)', 'spacing\n(D)', 'wake\nloss (%)']
    AEP_arr = np.array([AEP_AEP/AEP_AEP, COE_AEP/COE_AEP, profit_AEP/profit_profit, nturbs_AEP/nturbs_AEP, cost_AEP/cost_AEP, spacing_AEP/spacing_COE, wake_loss_AEP/wake_loss_AEP])
    COE_arr = np.array([AEP_COE/AEP_AEP, COE_COE/COE_AEP, profit_COE/profit_profit, nturbs_COE/nturbs_AEP, cost_COE/cost_AEP, spacing_COE/spacing_COE, wake_loss_COE/wake_loss_AEP])
    profit_arr = np.array([AEP_profit/AEP_AEP, COE_profit/COE_AEP, profit_profit/profit_profit, nturbs_profit/nturbs_AEP, cost_profit/cost_AEP, spacing_profit/spacing_COE, wake_loss_profit/wake_loss_AEP])

    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars

    plt.figure(figsize=(5.5,3))
    ax = plt.gca()
    rects1 = ax.bar(x - width, AEP_arr, width, label='AEP',color="C0")
    rects2 = ax.bar(x, COE_arr, width, label='COE',color="C1")
    rects3 = ax.bar(x + width, profit_arr, width, label='profit',color="C3")

    def autolabel(rects,labels):
        """Attach a text label above each bar in *rects*, displaying its height."""
        i = 0
        for rect in rects:
            height = rect.get_height()
            x = rect.get_x() + width/2.0
            if labels[i] == "22.9":
                plt.text(x,height-0.01,"22.90",verticalalignment="top",horizontalalignment="center",fontsize=6)
            elif labels[i] == "-3.11":
                plt.text(x,height-0.01,"-3.11",verticalalignment="top",horizontalalignment="center",fontsize=6)
            else:   
                plt.text(x,height+0.01,labels[i],verticalalignment="bottom",horizontalalignment="center",fontsize=6)
            i += 1
            

    AEP_arr = np.array([str(int(AEP_AEP/1E3)), str(np.round(COE_AEP,2)), str(np.round(profit_AEP/1E6,2)), str(int(nturbs_AEP)), str(np.round(cost_AEP/1E6,2)), str(np.round(spacing_AEP,2)), str(np.round(wake_loss_AEP*100,2))])
    COE_arr = np.array([str(int(AEP_COE/1E3)), str(np.round(COE_COE,2)), str(np.round(profit_COE/1E6,2)), str(int(nturbs_COE)), str(np.round(cost_COE/1E6,2)), str(np.round(spacing_COE,2)), str(np.round(wake_loss_COE*100,2))])
    profit_arr = np.array([str(int(AEP_profit/1E3)), str(np.round(COE_profit,2)), str(np.round(profit_profit/1E6,2)), str(int(nturbs_profit)), str(np.round(cost_profit/1E6,2)), str(np.round(spacing_profit,2)), str(np.round(wake_loss_profit*100,2))])
    print(str(np.round(COE_COE,2)))
    autolabel(rects1,AEP_arr)
    autolabel(rects2,COE_arr)
    autolabel(rects3,profit_arr)

    plt.axis("off")
    ax.legend(loc=1,fontsize=8,title="objective",title_fontsize=8)

    for i in range(len(labels)):
        plt.text(x[i],-0.37,labels[i],horizontalalignment="center",rotation=45,fontsize=8)

    plt.subplots_adjust(top=0.99,bottom=0.01,left=0.01,right=0.99)
    ax.set_xlim(-0.5,8.0)

    plt.savefig("bars_huge.pdf",transparent=True)
    plt.show()