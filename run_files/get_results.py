import numpy as np
import matplotlib.pyplot as plt
import floris.tools as wfct



sizes = ["big"]
objectives = ["AEP","COE","profit"]
methods = ["greedy","mosetti","sweep","bg"]

for j in range(len(sizes)):
    for m in range(len(methods)):
        for k in range(len(objectives)):

            size = sizes[j]
            objective = objectives[k]
            method = methods[m]
            
            with open('final_results2/%s/%s_%s_%s.txt'%(method,size,objective,objective)) as my_file:
                data = my_file.readlines()
            for i in range(len(data)):
                data[i] = float(data[i])

            arg = np.argmin(data[0:5])
            best = data[arg]

            metric = "time"
            with open('final_results2/%s/%s_%s_%s.txt'%(method,size,objective,metric)) as my_file:
                data = my_file.readlines()
            for i in range(len(data)):
                data[i] = float(data[i])
            time = np.sum(data[0:5])

            metric = "calls"
            with open('final_results2/%s/%s_%s_%s.txt'%(method,size,objective,metric)) as my_file:
                data = my_file.readlines()
            for i in range(len(data)):
                data[i] = float(data[i])
            calls = np.sum(data[0:5])

            print("size: ", size)
            print("objective: ", objective)
            print("method: ", method)
            # print("value: ", best)
            # print("time: ", time)
            # print("calls: ", calls)
            print("arg: ", arg)
            print("_______________________________________")

