import openmdao.api as om

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import time
import scipy.interpolate
from scipy.optimize import minimize


def calc_spacing(layout_x,layout_y):

        nTurbs = len(layout_x)
        npairs = int((nTurbs*(nTurbs-1))/2)
        spacing = np.zeros(npairs)

        ind = 0
        for i in range(nTurbs):
            for j in range(i,nTurbs):
                if i != j:
                    spacing[ind] = np.sqrt((layout_x[i]-layout_x[j])**2+(layout_y[i]-layout_y[j])**2)
                    ind += 1

        return spacing


def spacing_func(x):
    global minSpacing
    global rotor_diameter

    nturbs = int(len(x)/2)
    layout_x = x[0:nturbs]
    layout_y = x[nturbs:2*nturbs]
    spacing = calc_spacing(layout_x,layout_y)

    return spacing - minSpacing*rotor_diameter


def AEP_obj(x):

    global floris_model
    global function_calls

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter

    nturbs = int(len(x)/2)
    layout_x = x[0:nturbs]
    layout_y = x[nturbs:2*nturbs]

    function_calls += 1

    floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
    AEP = AEP/1E11
    
    return -AEP


def COE_obj(x):

    global floris_model
    global function_calls

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter

    function_calls += 1

    nturbs = int(len(x)/2)
    layout_x = x[0:nturbs]
    layout_y = x[nturbs:2*nturbs]
    floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
    nturbs = len(layout_x)
    
    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om

    COE = cost*1E5/AEP
    
    return COE


def profit_obj(x):

    global floris_model
    global function_calls
    global turbine_exists

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter
    global ppa
    global BOS_func



    function_calls += 1

    nturbs = int(len(x)/2)
    layout_x = x[0:nturbs]
    layout_y = x[nturbs:2*nturbs]

    floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
    nturbs = len(layout_x)

    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om
    profit = AEP/1.0E6*ppa - cost

    return -profit/1E6


## Main
if __name__ == "__main__":

    global floris_model
    global function_calls
    global turbine_exists
    global boundary
    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter
    global ppa
    global BOS_func

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5
    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')

    function_calls = 0

    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)


    ndirs = 1
    windDirections = np.array([300.0])
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = np.ones(ndirs)
    windFrequencies = windFrequencies/sum(windFrequencies)
    side = 800.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    boundary = mpl.path.Path(edges)
    ppa = 30.0

    # # ndirs = 16
    # # windDirections = np.linspace(0.0,360.-360./ndirs,ndirs)
    # # windSpeeds = np.ones(ndirs)*10.0
    # # windFrequencies = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0])
    # # windFrequencies = windFrequencies/sum(windFrequencies)
    # # side = 2000.0
    # # edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    # # boundary = mpl.path.Path(edges)
    # # ppa = 40.0

    minSpacing = 2.0 #rotor diameters
    rotor_diameter = 117.8


    nruns = 50


    save = False
    plot = True

    # nturbs = 10
    # nturbines = [18,19]
    # nturbines = [15,16,17,18,19,20,21,22,23,24,25]
    nturbines = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    niters = 25

    start_time = time.time()
    function_calls = 0
    spacing_con = ({"type": "ineq",
                            "fun": spacing_func})
    best_solution = 10000000.0
    

    for i in range(len(nturbines)):

        nturbs = nturbines[i]
        bnds = []
        for k in range(2*nturbs):
            bnds.append((0.0,side))

        for j in range(niters):
            x0 = np.random.rand(2*nturbs)*side
            res = minimize(COE_obj, x0, method='SLSQP', bounds=bnds, constraints=(spacing_con),tol=1E-6,options={'disp': False})
            if res.fun < best_solution and min(spacing_func(res.x)) >= -1E-4:
                best_solution = res.fun
                xf = res.x[0:nturbs]
                yf = res.x[nturbs:2*nturbs]
                
                run_time = time.time() - start_time
                print("best function value: ", best_solution)
                print("best number of turbines: ", len(xf))
                print("best x: ", repr(xf))
                print("best y: ", repr(yf))
                print("time to run: ", run_time)
                print("function calls: ", function_calls)

    print("total time: ", time.time() - start_time)
    print("total function calls: ", function_calls)


    
    # for i in range(nruns):
    #     start_time = time.time()
    #     function_calls = 0

    #     x0 = np.random.rand(2*nturbs)*side

    #     layout_x = x0[0:nturbs]
    #     layout_y = x0[nturbs:2*nturbs]
    #     floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
    #     AEP0 = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
    #     AEP0 = AEP0/1E11
    #     print("start AEP: ", AEP0)

    #     bnds = []
    #     for i in range(2*nturbs):
    #         bnds.append((0.0,side))

    #     spacing_con = ({"type": "ineq",
    #                     "fun": spacing_func})
                        
    #     res = minimize(AEP_obj, x0, method='SLSQP', bounds=bnds, constraints=(spacing_con),tol=1E-6,options={'disp': False})

    #     print("optimal function value: ", res.fun)
    #     print("optimized AEP: ", AEP_obj(res.x))
    #     xf = res.x[0:nturbs]
    #     yf = res.x[nturbs:2*nturbs]

    #     run_time = time.time() - start_time
    #     print("time to run: ", run_time)
    #     print("function calls: ", function_calls)
    #     print("spacing constraint: ", min(spacing_func(res.x)))


    #     print("number of turbines: ", len(xf))


    #     if save:
    #         file = open('final_results/bg_greedy/big_AEP_AEP.txt', 'a')
    #         file.write('%s'%(opt_val) + '\n')
    #         file.close()

    #         file = open('final_results/bg_greedy/big_AEP_x.txt', 'a')
    #         file.write('%s'%(xf) + '\n')
    #         file.close()

    #         file = open('final_results/bg_greedy/big_AEP_y.txt', 'a')
    #         file.write('%s'%(yf) + '\n')
    #         file.close()

    #         file = open('final_results/bg_greedy/big_AEP_time.txt', 'a')
    #         file.write('%s'%(run_time) + '\n')
    #         file.close()

    #         file = open('final_results/bg_greedy/big_AEP_calls.txt', 'a')
    #         file.write('%s'%(function_calls) + '\n')
    #         file.close()

    #         file = open('final_results/bg_greedy/big_AEP_history.txt', 'a')
    #         file.write('%s'%(ga.solution_history) + '\n')
    #         file.close()


    if plot:
        floris_model.reinitialize_flow_field(layout_array=(xf,yf))
        floris_model.reinitialize_flow_field(wind_direction=windDirections[0])
        floris_model.reinitialize_flow_field(wind_speed=windSpeeds[0])
        floris_model.calculate_wake()
        hor_plane = floris_model.get_hor_plane()

        # Plot and show
        # fig, ax = plt.subplots()
        plt.figure(figsize=(6,6))
        ax = plt.gca()
        wfct.visualization.visualize_cut_plane(hor_plane, ax=ax)

        bx = edges[:,0]
        by = edges[:,1]
        bx = np.append(bx,bx[0])
        by = np.append(by,by[0])
        plt.plot(bx,by,"--k")


        plt.show()