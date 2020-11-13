import openmdao.api as om

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import floris.tools as wfct
import time
from gradient_free import GeneticAlgorithm
import scipy.interpolate


def find_lengths(x,y,nPoints):
    length = np.zeros(len(x)-1)
    for i in range(nPoints):
        length[i] = np.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2)
    return length


def makeBoundary(start,nTurbs):

    global side

    nTurbs = int(nTurbs)
    edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    xBounds = edges[:,0]
    yBounds = edges[:,1]

    if xBounds[-1] != xBounds[0]:
        xBounds = np.append(xBounds,xBounds[0])
        yBounds = np.append(yBounds,yBounds[0])

    nBounds = len(xBounds)
    lenBound = find_lengths(xBounds,yBounds,len(xBounds)-1)
    circumference = sum(lenBound)
    x = np.zeros(nTurbs)
    y = np.zeros(nTurbs)

    bound_loc = np.linspace(start,start+circumference-circumference/float(nTurbs),nTurbs)
    for i in range(nTurbs):
        if bound_loc[i] > circumference:
            bound_loc[i] = bound_loc[i]%circumference
        while bound_loc[i] < 0.:
            bound_loc[i] += circumference

    for i in range(nTurbs):
        done = False
        for j in range(nBounds):
            if done == False:
                if bound_loc[i] < sum(lenBound[0:j+1]):
                    point_x = xBounds[j] + (xBounds[j+1]-xBounds[j])*(bound_loc[i]-sum(lenBound[0:j]))/lenBound[j]
                    point_y = yBounds[j] + (yBounds[j+1]-yBounds[j])*(bound_loc[i]-sum(lenBound[0:j]))/lenBound[j]
                    done = True
                    x[i] = point_x
                    y[i] = point_y

    return x,y

    
def get_turbine_locs(nrows,ncols,farm_width,farm_height,shear,rotation,center_x,center_y,boundary_mult):

    global side

    # create grid
    nrows = int(nrows)
    ncols = int(ncols)
    xlocs = np.linspace(0.0,farm_width,ncols)
    ylocs = np.linspace(0.0,farm_height,nrows)
    y_spacing = ylocs[1]-ylocs[0]
    nturbs = nrows*ncols
    layout_x = np.zeros(nturbs)
    layout_y = np.zeros(nturbs)
    turb = 0
    for i in range(nrows):
        for j in range(ncols):
            layout_x[turb] = xlocs[j] + float(i)*y_spacing*np.tan(shear)
            layout_y[turb] = ylocs[i]
            turb += 1
    
    # rotate
    rotate_x = np.cos(rotation)*layout_x - np.sin(rotation)*layout_y
    rotate_y = np.sin(rotation)*layout_x + np.cos(rotation)*layout_y

    # move center of grid
    rotate_x = (rotate_x - np.mean(rotate_x)) + center_x
    rotate_y = (rotate_y - np.mean(rotate_y)) + center_y

    # delete desired turbines
    delete_arr = np.array([],dtype=int)
    # for i in range(nrows*ncols):
    #     if int(turbine_exists[i]) == 0:
    #         delete_arr = np.append(delete_arr,i)
    
    delete_x = np.delete(rotate_x,delete_arr)
    delete_y = np.delete(rotate_y,delete_arr)

    # get rid of points outside of boundary
    turbs = np.zeros((len(delete_x),2))
    turbs[:,0] = delete_x[:]
    turbs[:,1] = delete_y[:]

    boundary_cutoff = 1.0 - (1.0-boundary_mult)/2.0
    edges = np.array([(1.0-boundary_cutoff)*side,(1.0-boundary_cutoff)*side, (1.0-boundary_cutoff)*side,boundary_cutoff*side, boundary_cutoff*side,boundary_cutoff*side, boundary_cutoff*side,(1.0-boundary_cutoff)*side]).reshape(4,2)
    boundary = mpl.path.Path(edges)
    in_bounds = boundary.contains_points(turbs)

    return_x = np.zeros(sum(in_bounds))
    return_y = np.zeros(sum(in_bounds))
    ind = 0
    for i in range(len(delete_x)):
        if in_bounds[i]:
            return_x[ind] = delete_x[i]
            return_y[ind] = delete_y[i]
            ind += 1

    return return_x, return_y


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
    global turbine_exists

    global windDirections
    global windSpeeds
    global windFrequencies
    global side
    global minSpacing
    global rotor_diameter

    nrows = x[0]
    ncols = x[1]
    farm_width = x[2]
    farm_height = x[3]
    shear = x[4]
    rotation = x[5]
    center_x = x[6]
    center_y = x[7]
    boundary_mult = x[8]
    start = x[9]
    n_boundary = x[10]

    function_calls += 1
    x_grid, y_grid = get_turbine_locs(nrows,ncols,farm_width,farm_height,shear,rotation,center_x,center_y,boundary_mult)
    x_bound,y_bound = makeBoundary(start,n_boundary)

    layout_x = np.append(x_grid,x_bound)
    layout_y = np.append(y_grid,y_bound)

    if len(layout_x) > 1:
        spacing = calc_spacing(layout_x,layout_y)
        spacing_con = np.min(spacing) - minSpacing*rotor_diameter
    elif len(layout_x) == 1:
        spacing_con = 0.0
    else:
        spacing_con = -1.0

    if len(layout_x) < 1 or np.max(layout_x) > side or np.max(layout_y) > side or np.min(layout_x) < 0.0 or np.min(layout_y) < 0.0 or spacing_con < 0.0:
        AEP = -1000000.0

    else:
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

    nrows = x[0]
    ncols = x[1]
    farm_width = x[2]
    farm_height = x[3]
    shear = x[4]
    rotation = x[5]
    center_x = x[6]
    center_y = x[7]
    boundary_mult = x[8]
    start = x[9]
    n_boundary = x[10]

    function_calls += 1
    x_grid, y_grid = get_turbine_locs(nrows,ncols,farm_width,farm_height,shear,rotation,center_x,center_y,boundary_mult)
    x_bound,y_bound = makeBoundary(start,n_boundary)

    layout_x = np.append(x_grid,x_bound)
    layout_y = np.append(y_grid,y_bound)

    if len(layout_x) > 1:
        spacing = calc_spacing(layout_x,layout_y)
        spacing_con = np.min(spacing) - minSpacing*rotor_diameter
    elif len(layout_x) == 1:
        spacing_con = 0.0
    else:
        spacing_con = -1.0

    if len(layout_x) < 1 or np.max(layout_x) > side or np.max(layout_y) > side or np.min(layout_x) < 0.0 or np.min(layout_y) < 0.0 or spacing_con < 0.0:
        COE = 1E15

    else:
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

    nrows = x[0]
    ncols = x[1]
    farm_width = x[2]
    farm_height = x[3]
    shear = x[4]
    rotation = x[5]
    center_x = x[6]
    center_y = x[7]
    boundary_mult = x[8]
    start = x[9]
    n_boundary = x[10]

    function_calls += 1
    x_grid, y_grid = get_turbine_locs(nrows,ncols,farm_width,farm_height,shear,rotation,center_x,center_y,boundary_mult)
    x_bound,y_bound = makeBoundary(start,n_boundary)

    layout_x = np.append(x_grid,x_bound)
    layout_y = np.append(y_grid,y_bound)

    if len(layout_x) > 1:
        spacing = calc_spacing(layout_x,layout_y)
        spacing_con = np.min(spacing) - minSpacing*rotor_diameter
    elif len(layout_x) == 1:
        spacing_con = 0.0
    else:
        spacing_con = -1.0

    if len(layout_x) < 1 or np.max(layout_x) > side or np.max(layout_y) > side or np.min(layout_x) < 0.0 or np.min(layout_y) < 0.0 or spacing_con < 0.0:
        return 1E6

    else:
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

    # 30 for small 40 for big?
    # ppa = 40.0

    function_calls = 0

    floris_model = wfct.floris_interface.FlorisInterface("model_discrete.json")
    floris_model.set_gch(False)

    # small unidirectional case
    # ndirs = 1
    # windDirections = np.array([300.0])
    # windSpeeds = np.ones(ndirs)*10.0
    # windFrequencies = np.ones(ndirs)
    # windFrequencies = windFrequencies/sum(windFrequencies)
    # side = 800.0
    # edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    # boundary = mpl.path.Path(edges)
    # ppa = 30.0

    # ndirs = 16
    # windDirections = np.linspace(0.0,360.-360./ndirs,ndirs)
    # windSpeeds = np.ones(ndirs)*10.0
    # windFrequencies = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0])
    # windFrequencies = windFrequencies/sum(windFrequencies)
    # side = 2000.0
    # edges = np.array([0.0,0.0, 0.0,side, side,side, side,0.0]).reshape(4,2)
    # boundary = mpl.path.Path(edges)
    # ppa = 40.0

    # wind rose bigger farm 2
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
    boundary = mpl.path.Path(edges)
    grid_size = 20
    ppa = 30.0

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

    minSpacing = 2.0 #rotor diameters
    rotor_diameter = 117.8

    nruns = 1


    save = True
    plot = True
    
    for i in range(nruns):
        # gradient-free optimization
        start_time = time.time()
        function_calls = 0

        ga = GeneticAlgorithm()
        # ga.bits = np.array([16,16,16,16,16,16,16,16,16,16,16])
        ga.bits = np.array([8,8,8,8,8,8,8,8,8,8,8])
        ga.bounds = np.array([(2.0,6.0),(2.0,6.0),(1.0,2*side),(1.0,2*side),(-np.pi,np.pi),(0.0,2.0*np.pi),(0.0,side),(0.0,side),(0.5,1.0),(0.0,side),(0,50)])
        ga.variable_type = np.array(["int","int","float","float","float","float","float","float","float","float","int"])
        ga.population_size = 200
        ga.max_geneneration = 1000
        # ga.max_geneneration = 5
        ga.objective_function = profit_obj
        ga.crossover_rate = 0.1
        ga.mutation_rate = 0.02
        ga.convergence_iters = 50
        ga.tol = 1E-6

        ga.optimize_ga(crossover="chunk")

        opt_val = ga.optimized_function_value
        DVopt = ga.optimized_design_variables

        run_time = time.time() - start_time
        print("opt_val: ", opt_val)
        print("time to run: ", run_time)
        print("function calls: ", function_calls)

        xg, yg = get_turbine_locs(DVopt[0],DVopt[1],DVopt[2],DVopt[3],DVopt[4],DVopt[5],DVopt[6],DVopt[7],DVopt[8])    
        xb, yb = makeBoundary(DVopt[9],DVopt[10])
        xf = np.append(xg,xb)
        yf = np.append(yg,yb)

        print("number of turbines: ", len(xf))

        save_str = "profit"
        header_str = "big"
        if save:
            file = open('final_results2/bg/%s_%s_%s.txt'%(header_str,save_str,save_str), 'a')
            file.write('%s'%(opt_val) + '\n')
            file.close()

            file = open('final_results2/bg/%s_%s_x.txt'%(header_str,save_str), 'a')
            file.write('%s'%(xf) + '\n')
            file.close()

            file = open('final_results2/bg/%s_%s_y.txt'%(header_str,save_str), 'a')
            file.write('%s'%(yf) + '\n')
            file.close()

            file = open('final_results2/bg/%s_%s_time.txt'%(header_str,save_str), 'a')
            file.write('%s'%(run_time) + '\n')
            file.close()

            file = open('final_results2/bg/%s_%s_calls.txt'%(header_str,save_str), 'a')
            file.write('%s'%(function_calls) + '\n')
            file.close()

            file = open('final_results2/bg/%s_%s_history.txt'%(header_str,save_str), 'a')
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