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
    side = 800.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    ppa = 30.0

    floris_model.reinitialize_flow_field(layout_array=([0],[0]))
    AEP0 = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6

    xf = np.array([2.35015070e+02, 6.60582700e-15, 6.11748763e+02, 3.53540931e-16,
       4.71104510e+02, 7.16362700e+01, 2.45149184e+02, 6.52901480e+00,
       8.00000000e+02, 2.97985394e+02, 8.00000000e+02, 7.38779734e+02,
       5.64400000e+02, 7.95092677e+02, 4.47924021e+02, 5.00802981e+02,
       2.35569976e+02])
    yf = np.array([4.78488576e+02, 4.95101210e+02, 4.22735465e+02, 2.35509528e+02,
       2.33720751e+02, 7.19546924e+02, 3.88167204e+00, 3.12746040e-14,
       5.64400000e+02, 7.90497941e+02, 8.00000000e+02, 8.54093525e-02,
       8.00000000e+02, 2.29214851e+02, 5.95204956e+02, 1.31481553e-14,
       2.39286916e+02])

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



    xf = [  0.   ,      266.66666667 ,533.33333333,   0.   ,      533.33333333,
            0.   ,        0. ,        266.66666667, 533.33333333, 800.        ]

    yf = [  0.   ,        0.    ,      88.88888889, 266.66666667, 355.55555556,
            533.33333333, 800.    ,     800.    ,     800.   ,      800.        ]

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



    xf = [  0. ,        266.66666667, 622.22222222 ,  0. ,        355.55555556,
        711.11111111,  88.88888889 ,444.44444444, 800.    ,     177.77777778,
        533.33333333, 800.        ]

    yf = [  0. ,          0.   ,        0.   ,      266.66666667, 266.66666667,
        266.66666667 ,533.33333333 ,533.33333333 ,533.33333333 ,800.,
        800.      ,   800.        ]

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
            if labels[i] == "21.86":
                plt.text(x,height-0.01,"21.86",verticalalignment="top",horizontalalignment="center",fontsize=6)
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

    plt.savefig("bars_small.pdf",transparent=True)
    plt.show()