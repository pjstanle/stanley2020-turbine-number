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
    ndirs = 1
    windDirections = np.array([300.0])
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = np.ones(ndirs)
    windFrequencies = windFrequencies/sum(windFrequencies)
    side = 1600.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    ppa = 30.0

    floris_model.reinitialize_flow_field(layout_array=([0],[0]))
    AEP0 = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6

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

    nturbs_AEP = len(xf)
    AEP_AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs_AEP
    bos = BOS_func(nturbs_AEP)
    om = 44*nturbs_AEP*2500.0
    fcr = 0.097
    cost_AEP = (tcc+bos)*fcr + om

    COE_AEP = cost_AEP/AEP_AEP
    profit_AEP = AEP_AEP*ppa - cost_AEP



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

    nturbs_COE = len(xf)
    AEP_COE = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs_COE
    bos = BOS_func(nturbs_COE)
    om = 44*nturbs_COE*2500.0
    fcr = 0.097
    cost_COE = (tcc+bos)*fcr + om

    COE_COE = cost_COE/AEP_COE
    profit_COE = AEP_COE*ppa - cost_COE



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

    plt.figure(figsize=(5.5,1.9))
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
            if labels[i] == "24.46":
                plt.text(x,height-0.01,"24.46",verticalalignment="top",horizontalalignment="center",fontsize=6)
            elif labels[i] == "-2.16":
                plt.text(x,height-0.01,"-2.16",verticalalignment="top",horizontalalignment="center",fontsize=6)
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
        plt.text(x[i],-0.38,labels[i],horizontalalignment="center",rotation=45,fontsize=8)

    plt.subplots_adjust(top=0.96,bottom=0.27,left=0.01,right=0.99)
    ax.set_xlim(-0.5,8.0)

    plt.savefig("bars_big.pdf",transparent=True)
    plt.show()