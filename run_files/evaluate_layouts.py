import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import scipy.interpolate
    
## Main
if __name__ == "__main__":

    # unidirectional
    # ndirs = 1
    # windDirections = np.array([300.0])
    # windSpeeds = np.ones(ndirs)*10.0
    # windFrequencies = np.ones(ndirs)
    # windFrequencies = windFrequencies/sum(windFrequencies)

    # full rose
    ndirs_interp = 17
    windDirections_interp = np.linspace(0.0,360.,ndirs_interp)
    windFrequencies_interp = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0,2.0])
    freq_func = scipy.interpolate.interp1d(windDirections_interp, windFrequencies_interp, kind='cubic')
    ndirs = 72
    windDirections = np.linspace(0.0,360.-360./ndirs,ndirs)
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = freq_func(windDirections)
    windFrequencies = windFrequencies/sum(windFrequencies)

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5
    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')

    ppa = 30.0

    function_calls = 0

    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)


    layout_x = np.array([ 505.26315789, 1010.52631579, 1600.  ,          0.   ,      1431.57894737,
  757.89473684,    0.        , 1600.         , 421.05263158, 1178.94736842,
    0.        , 1600.        ,  926.31578947 , 421.05263158 ,1600.,
    0.        ,  589.47368421, 1600.         ,   0.         ,1094.73684211,
  336.84210526, 1600.        , 1178.94736842 , 757.89473684 ,  0.        ])
    layout_y = np.array([   0.       ,     0.   ,         0.   ,        84.21052632 , 168.42105263,
  252.63157895,  336.84210526,  336.84210526,  505.26315789,  505.26315789,
  589.47368421,  673.68421053,  757.89473684,  842.10526316,  926.31578947,
  926.31578947, 1178.94736842, 1178.94736842, 1263.15789474, 1347.36842105,
 1515.78947368, 1515.78947368, 1600.        , 1600.        , 1600.        ])

    nturbs = len(layout_x)
    floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om
    COE = (cost*1E6)/(AEP)
    profit = ((AEP/1E6)*ppa-cost)/1E6

    print("AEP: ", AEP/1E9)
    print("COE: ", COE)
    print("profit: ", profit)


    # SMALL
    # AEP           
    # greedy        252.5954590580077
    # mosetti       292.9095654445165
    # sweep         237.4578934749507
    # BG            300.67683188209986
    # GB            304.4387580376732

    # COE
    # greedy        23.06856778970299
    # mosetti       21.863596802863245
    # sweep         22.057515230075694
    # BG            22.15624359217908
    # GB            21.951418571833074

    # profit
    # greedy        1.827323064968818
    # mosetti       2.0267198623540486
    # sweep         1.6928745084466097
    # BG            1.8880672403519423
    # GB            1.9850677894378015


    # BIG UNI
    # AEP
    # greedy        669.9333519224112
    # mosetti       470.4592811231313
    # sweep         670.7910131131814
    # BG            731.1415314943723

    # COE
    # greedy        20.52028555653305
    # mosetti       20.93835614305752
    # sweep         20.46473212718152
    # BG            20.650184069795

    # profit
    # greedy        4.992934239211153
    # mosetti       3.508046174970378
    # sweep         4.917332821445804
    # BG            5.4351185809442715



    # BIG full
    # AEP           
    # greedy        567.9685243147904
    # mosetti       451.9642340399623
    # sweep         594.1742047427847
    # BG

    # COE
    # greedy        22.903885928622387
    # mosetti       22.95598067761145
    # sweep         22.827651104572183
    # BG

    # profit
    # greedy        2.5644860312522764
    # mosetti       2.32333399556982
    # sweep         2.590229077376589
    # BG