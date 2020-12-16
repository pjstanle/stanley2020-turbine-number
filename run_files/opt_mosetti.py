import openmdao.api as om

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import time
from gradient_free import GeneticAlgorithm
import scipy.interpolate


def get_turbine_locs(turbine_exists):

    global xlocs
    global ylocs

    layout_x = np.zeros(int(np.sum(turbine_exists)))
    layout_y = np.zeros(int(np.sum(turbine_exists)))
    ind = 0
    for i in range(len(turbine_exists)):
        if int(turbine_exists[i]) == 1:
            layout_x[ind] = xlocs[i]
            layout_y[ind] = ylocs[i]
            ind += 1

    return layout_x, layout_y


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


def AEP_obj(x):

    global floris_model
    global function_calls

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter

    turbine_exists = x[:]

    layout_x, layout_y = get_turbine_locs(turbine_exists)

    if len(layout_x) > 1:
        spacing = calc_spacing(layout_x,layout_y)
        spacing_con = np.min(spacing) - minSpacing*rotor_diameter
    elif len(layout_x) == 1:
        spacing_con = 0.0
    else:
        spacing_con = -1.0

    if len(layout_x) < 1 or np.max(layout_x) > side or np.max(layout_y) > side or np.min(layout_x) < 0.0 or np.min(layout_y) < 0.0 or spacing_con < 0.0:
        AEP = 0.0

    else:
        function_calls += 1
        floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
        AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
        AEP = AEP/1E11
    
    return -AEP


def COE_obj(x):

    global floris_model
    global function_calls
    global turbine_exists

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter

    turbine_exists = x[:]

    layout_x, layout_y = get_turbine_locs(turbine_exists)

    if len(layout_x) > 1:
        spacing = calc_spacing(layout_x,layout_y)
        spacing_con = np.min(spacing) - minSpacing*rotor_diameter
    elif len(layout_x) == 1:
        spacing_con = 0.0
    else:
        spacing_con = -1.0

    if len(layout_x) < 1 or np.max(layout_x) > side or np.max(layout_y) > side or np.min(layout_x) < 0.0 or np.min(layout_y) < 0.0 or spacing_con < 0.0:
        AEP = 0.0
        COE = 1E15

    else:
        function_calls += 1
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

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter
    global ppa
    global BOS_func

    turbine_exists = x[:]

    layout_x, layout_y = get_turbine_locs(turbine_exists)

    if len(layout_x) > 1:
            spacing = calc_spacing(layout_x,layout_y)
            spacing_con = np.min(spacing) - minSpacing*rotor_diameter
    elif len(layout_x) == 1:
        spacing_con = 0.0
    else:
        spacing_con = -1.0

    if len(layout_x) < 1 or np.max(layout_x) > side or np.max(layout_y) > side or np.min(layout_x) < 0.0 or np.min(layout_y) < 0.0 or spacing_con < 0.0:
        profit = 0.0

    else:
        function_calls += 1
        floris_model.reinitialize_flow_field(layout_array=(layout_x,layout_y))
        AEP = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)
        nturbs = len(layout_x)

        tcc = 2500*829*nturbs
        bos = BOS_func(nturbs)
        om = 44*nturbs*2500.0
        fcr = 0.097
        cost = (tcc+bos)*fcr + om

        profit = AEP/1.0E6*ppa - cost
        # print("AEP: ", AEP/1.0E6*ppa)
        # print("cost: ", cost)
        
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

    global xlocs
    global ylocs

    capacity = np.array([2.5,20,50,100,150,200,400,1000])
    cost_per_kw = np.array([950,699,515,420,386,363,304,280])
    BOS_cost = capacity*cost_per_kw*1000.0
    nturbs = capacity/2.5
    BOS_func = scipy.interpolate.interp1d(nturbs, BOS_cost, kind='cubic')

    

    function_calls = 0

    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)

    # one direction small farm
    ndirs = 1
    windDirections = np.array([300.0])
    windSpeeds = np.ones(ndirs)*10.0
    windFrequencies = np.ones(ndirs)
    windFrequencies = windFrequencies/sum(windFrequencies)
    side = 800.0
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    boundary = mpl.path.Path(edges)
    ppa = 30.0
    grid_size = 10

    # # wind rose bigger farm
    # ndirs = 16
    # windDirections = np.linspace(0.0,360.-360./ndirs,ndirs)
    # windSpeeds = np.ones(ndirs)*10.0
    # windFrequencies = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0])
    # windFrequencies = windFrequencies/sum(windFrequencies)
    # side = 2000.0
    # edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    # boundary = mpl.path.Path(edges)
    # grid_size = 25
    # ppa = 40.0

    # wind rose bigger farm 2
    # ndirs_interp = 17
    # windDirections_interp = np.linspace(0.0,360.,ndirs_interp)
    # windFrequencies_interp = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0,2.0])
    # freq_func = scipy.interpolate.interp1d(windDirections_interp, windFrequencies_interp, kind='cubic')
    # ndirs = 72
    # windDirections = np.linspace(0.0,360.-360./ndirs,ndirs)
    # windSpeeds = np.ones(ndirs)*10.0
    # windFrequencies = freq_func(windDirections)
    # windFrequencies = windFrequencies/sum(windFrequencies)
    # side = 1600.0
    # edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    # boundary = mpl.path.Path(edges)
    # grid_size = 20
    # ppa = 30.0

    # wind rose bigger farm unidirectional
    # ndirs = 1
    # windDirections = np.array([300.0])
    # windSpeeds = np.ones(ndirs)*10.0
    # windFrequencies = np.ones(ndirs)
    # windFrequencies = windFrequencies/sum(windFrequencies)
    # side = 1600.0
    # edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    # boundary = mpl.path.Path(edges)
    # grid_size = 20
    # ppa = 30.0


    x_grid = np.linspace(0.0,side,grid_size)
    y_grid = np.linspace(0.0,side,grid_size)

    xlocs, ylocs = np.meshgrid(x_grid,y_grid)
    xlocs = np.ndarray.flatten(xlocs)
    ylocs = np.ndarray.flatten(ylocs)

    minSpacing = 2.0 #rotor diameters
    rotor_diameter = 117.8

    nruns = 5

    save = True
    plot = True

    for i in range(nruns):
        # gradient-free optimization
        start_time = time.time()
        function_calls = 0

        ga = GeneticAlgorithm()
        ga.bits = np.zeros(grid_size*grid_size,dtype=int)
        ga.bounds = np.zeros((grid_size*grid_size,2))
        ga.variable_type = np.array([])
        for i in range(grid_size*grid_size):
            ga.variable_type = np.append(ga.variable_type,"int")
            ga.bounds[i] = (0,1)
        ga.population_size = grid_size*grid_size*10
        ga.max_generation = 1000
        ga.objective_function = COE_obj
        ga.crossover_rate = 0.1
        ga.mutation_rate = 0.02
        ga.convergence_iters = 25
        ga.tol = 1E-6

        # ga.population_size = 400
        # ga.convergence_iters = 100

        # ga.optimize_ga(initialize="limit")
        ga.optimize_ga(initialize="limit",crossover="chunk")
        # ga.optimize_ga(crossover="chunk")

        opt_val = ga.optimized_function_value
        DVopt = ga.optimized_design_variables

        run_time = time.time() - start_time
        print("opt_val: ", opt_val)
        print("time to run: ", run_time)
        print("function calls: ", function_calls)

        xf, yf = get_turbine_locs(DVopt)    

        print("opt number of turbs: ", len(xf))

        save_str = "COE"
        header_str = "small_uni"
        if save:
            file = open('final_results3/mosetti/%s_%s_%s.txt'%(header_str,save_str,save_str), 'a')
            file.write('%s'%(opt_val) + '\n')
            file.close()

            file = open('final_results3/mosetti/%s_%s_x.txt'%(header_str,save_str), 'a')
            file.write('%s'%(xf) + '\n')
            file.close()

            file = open('final_results3/mosetti/%s_%s_y.txt'%(header_str,save_str), 'a')
            file.write('%s'%(yf) + '\n')
            file.close()

            file = open('final_results3/mosetti/%s_%s_time.txt'%(header_str,save_str), 'a')
            file.write('%s'%(run_time) + '\n')
            file.close()

            file = open('final_results3/mosetti/%s_%s_calls.txt'%(header_str,save_str), 'a')
            file.write('%s'%(function_calls) + '\n')
            file.close()

            file = open('final_results3/mosetti/%s_%s_history.txt'%(header_str,save_str), 'a')
            file.write('%s'%(ga.solution_history) + '\n')
            file.close()





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

        plt.figure(2)
        plt.plot(ga.solution_history)

        plt.show()
