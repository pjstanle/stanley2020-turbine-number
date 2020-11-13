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

    ppa = 100.0

    function_calls = 0

    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)

    ndirs = 1
    windDirections = np.array([270.0])
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = np.ones(ndirs)
    windFrequencies = windFrequencies/sum(windFrequencies)

    farm_length = 25000.0
    AEP = np.zeros(50)
    narr = np.zeros(len(AEP))
    cost = np.zeros(len(AEP))
    for i in range(len(AEP)):
        nturbs = i+5
        narr[i] = nturbs
        layout_x = np.linspace(0,farm_length,nturbs)
        layout_y = np.zeros(nturbs)
        floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
        AEP[i] = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)

        tcc = 2500*829*nturbs
        bos = BOS_func(nturbs)
        om = 44*nturbs*2500.0
        fcr = 0.097
        cost[i] = (tcc+bos)*fcr + om

    

    plt.figure(figsize=(6.5,2.5))
    plt.subplot(131)
    plt.plot(narr,AEP/1E9)
    i = np.argmax(AEP)
    mx = np.max(AEP)/1E9
    mn = np.min(AEP)/1E9
    plt.plot([narr[i],narr[i]],[mn-100,mx],'--',color="C0")
    plt.plot([0.0,narr[i]],[mx,mx],'--',color="C0")
    plt.ylabel("AEP (GWh)",labelpad=-0.2)
    plt.xlabel("number of turbines",labelpad=-0.2)
    plt.gca().set_xticks([5,narr[i],27])
    plt.xlim(5,27)
    plt.ylim(100,325)
    # plt.gca().set_yticks([100,200,np.ceil(mx)])

    plt.subplot(132)
    COE = (cost*1E6)/(AEP)
    plt.plot(narr,COE)
    i = np.argmin(COE)
    mx = np.max(COE)
    mn = np.min(COE)
    plt.plot([narr[i],narr[i]],[5,mn],'--',color="C0")
    plt.plot([0.0,narr[i]],[mn,mn],'--',color="C0")
    plt.ylim(16,41)
    plt.gca().set_xticks([5,narr[i],27])
    plt.xlim(5,27)


    p = ((AEP/1E6)*50-cost)/1E6
    print(p[i])
    print(p[i]/np.max(p))
    print(np.max(p))

    plt.ylabel("COE ($/MWh)",labelpad=-0.2)
    plt.xlabel("number of turbines",labelpad=-0.2)

    plt.subplot(133)
    # ppa = np.array([60,50,40,30])
    ppa = np.array([90,70,50,30])
    for j in range(len(ppa)):
        profit = ((AEP/1E6)*ppa[j]-cost)/1E6
        plt.plot(narr,profit,label="%s"%ppa[j],color="C%s"%j)
        i = np.argmax(profit)
        mx = np.max(profit)
        mn = np.min(profit)
        plt.plot([narr[i],narr[i]],[-4,mx],'--',color="C%s"%j)
        plt.plot([0.0,narr[i]],[mx,mx],'--',color="C%s"%j)
    plt.legend(loc=1,fontsize=6,title="$/MWh",title_fontsize=6)
    plt.ylabel("annual profit ($MM)",labelpad=-0.7)
    plt.xlabel("number of turbines",labelpad=-0.2)
    # plt.ylim(-2,18)
    # plt.xticks(fontsize=8,rotation=90)
    plt.gca().set_xticks([5,13,18,27])
    plt.xlim(5,27)
    plt.ylim(-4,25)
    # plt.text(15,-2.5,"15",horizontalalignment="center",verticalalignment="bottom")
    # plt.text(17,-3.9,"17",horizontalalignment="center",verticalalignment="bottom")


    plt.subplots_adjust(left=0.1,right=0.98,wspace=0.4,bottom=0.2,top=0.95)
    # plt.savefig("sweep1d_90.pdf", transparent=True)
    plt.show()

    # nturbs = np.arange(10)+10
    # for j in range(len(nturbs)):
    #     layout_x = np.linspace(0,farm_length,nturbs[j])
    #     layout_y = np.zeros(nturbs[j])
    #     floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    #     floris_model.reinitialize_flow_field(wind_direction=270.0)
    #     floris_model.reinitialize_flow_field(wind_speed=8.0)
    #     floris_model.calculate_wake()
    #     speeds = np.zeros(nturbs[j])
    #     for i in range(nturbs[j]):
    #         print(floris_model.floris.farm.turbines[i].average_velocity)
    #         speeds[i] = floris_model.floris.farm.turbines[i].average_velocity
    #     plt.plot(layout_x,speeds)
    # plt.show()

    # nturbs = 16
    # layout_x = np.linspace(0,farm_length,nturbs)
    # layout_y = np.zeros(nturbs)
    # floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    # floris_model.reinitialize_flow_field(wind_direction=270.0)
    # floris_model.reinitialize_flow_field(wind_speed=8.0)
    # floris_model.calculate_wake()
    # hor_plane = floris_model.get_hor_plane()
    # plt.figure(figsize=(6,6))
    # ax = plt.gca()
    # wfct.visualization.visualize_cut_plane(hor_plane, ax=ax)
    # plt.show()