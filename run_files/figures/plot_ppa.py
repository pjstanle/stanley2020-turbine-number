import numpy as np
import matplotlib.pyplot as plt
import floris.tools as wfct
import scipy.interpolate



# PPA = ["25.0","30.0","40.0","50.0","60.0","70.0","80.0","90.0","100.0"]


# for i in range(len(PPA)):

#     ppa = PPA[i]
    
#     with open('../final_results2/ppa/%s_profit_profit.txt'%(ppa)) as my_file:
#         data = my_file.readlines()
#     for i in range(len(data)):
#         data[i] = float(data[i])

#     arg = np.argmin(data)
#     best = data[arg]

#     print("ppa: ", ppa)
#     print("value: ", best)
#     print("arg: ", arg)
#     print("_______________________________________")


x = [[   0.    ,     1094.73684211, 1600.  ,        505.26315789, 1600.,
  842.10526316 ,   0.  ,       1263.15789474 ,   0.    ,     1600.,
  421.05263158 , 757.89473684  ,  0.  ,       1600.    ,     1178.94736842,
  421.05263158, 1600.     ,       0.        ],
        [ 505.26315789, 1010.52631579, 1600.   ,         0.     ,    1431.57894737,
        757.89473684  ,  0.         ,1600.   ,       421.05263158, 1178.94736842,
            0.        , 1600.        ,  926.31578947 , 421.05263158, 1600.,
            0.        ,  589.47368421, 1600.  ,          0.    ,     1094.73684211,
        336.84210526, 1600.,         1178.94736842 , 757.89473684 ,   0.        ],
[   0.      ,    252.63157895,  842.10526316, 1347.36842105, 1600.,
 1094.73684211, 1431.57894737,  589.47368421,    0.        , 1600.,
  421.05263158,    0.        , 1263.15789474,  252.63157895, 1600.,
  757.89473684, 1010.52631579,    0.        , 1263.15789474, 1600.,
  673.68421053,    0.        , 1600.        ,  168.42105263, 1431.57894737,
  421.05263158,    0.        , 1600.        , 1178.94736842,  842.10526316,
  589.47368421,  252.63157895],
  [   0.      ,    252.63157895 , 505.26315789, 1010.52631579, 1263.15789474,
 1600.        ,  757.89473684, 1600.        , 1010.52631579,    0.,
  252.63157895, 1347.36842105,    0.        , 1600.        , 1178.94736842,
  252.63157895, 1600.        ,  673.68421053,    0.        ,  926.31578947,
    0.        , 1600.        , 1178.94736842,  336.84210526, 1600.,
  168.42105263,  421.05263158, 1347.36842105,  673.68421053,    0.,
  252.63157895, 1600.        , 1347.36842105, 1094.73684211,  842.10526316,
  505.26315789],
  [   0.      ,    252.63157895,  505.26315789,  842.10526316, 1094.73684211,
 1347.36842105, 1600.        ,  673.68421053, 1600.        , 1347.36842105,
    0.        ,  842.10526316,  252.63157895,    0.        , 1094.73684211,
 1600.        ,  421.05263158, 1347.36842105, 1600.        ,    0.,
  757.89473684,  505.26315789,    0.        , 1431.57894737, 1010.52631579,
  336.84210526, 1600.        , 1263.15789474,    0.        ,  842.10526316,
 1600.        ,  168.42105263,  421.05263158, 1178.94736842, 1431.57894737,
  926.31578947,  673.68421053 ,   0.        ],
[   0.       ,   252.63157895 , 505.26315789,  842.10526316 ,1094.73684211,
 1347.36842105, 1600.        ,  673.68421053, 1600.         ,1178.94736842,
  252.63157895,    0.        ,  926.31578947,  505.26315789 ,   0.,
 1263.15789474, 1600.        ,  757.89473684,  252.63157895 ,1600.,
 1347.36842105,    0.        , 1178.94736842,  505.26315789 , 168.42105263,
 1431.57894737, 1010.52631579,    0.        ,  757.89473684 ,1600.,
 1347.36842105,  336.84210526,  589.47368421, 1600.         , 168.42105263,
  421.05263158,  926.31578947, 1178.94736842, 1431.57894737 , 673.68421053,
    0.        ],
[   0.         , 336.84210526 , 673.68421053,  926.31578947, 1347.36842105,
 1600.         ,1178.94736842, 1600.        ,  926.31578947,  168.42105263,
  421.05263158 ,1347.36842105,  673.68421053,    0.        ,  252.63157895,
 1600.         ,1347.36842105,  926.31578947,    0.        ,  505.26315789,
 1600.         , 252.63157895, 1094.73684211,    0.        ,  589.47368421,
 1600.         ,1347.36842105,  168.42105263,  842.10526316, 1600.,
  421.05263158 ,   0.        , 1178.94736842, 1431.57894737,  673.68421053,
  252.63157895 ,1600.        , 1263.15789474,  926.31578947,  505.26315789,
    0.        ],
    [   0.        ,  252.63157895 , 505.26315789 , 842.10526316 ,1094.73684211,
 1347.36842105, 1600.        , 1600.        , 1347.36842105, 1094.73684211,
  589.47368421,  252.63157895,    0.        ,  842.10526316,    0.,
  252.63157895, 1347.36842105, 1600.        , 1094.73684211,  505.26315789,
  757.89473684, 1600.        ,  168.42105263, 1178.94736842,    0.,
  505.26315789, 1347.36842105, 1600.        ,  757.89473684,  252.63157895,
    0.        , 1600.        , 1347.36842105,  168.42105263,  842.10526316,
 1094.73684211,  589.47368421,    0.        ,  336.84210526, 1347.36842105,
 1600.     ,    1094.73684211,  842.10526316],
 [   0.        ,  252.63157895 , 505.26315789 , 757.89473684 ,1094.73684211,
 1347.36842105, 1600.        , 1600.        , 1347.36842105, 1094.73684211,
  589.47368421,  252.63157895,    0.        ,  842.10526316,    0.,
  252.63157895, 1347.36842105, 1600.        , 1094.73684211,  673.68421053,
 1600.        , 1347.36842105,  252.63157895,    0.        ,  926.31578947,
  505.26315789,    0.        ,  252.63157895, 1431.57894737,  673.68421053,
 1600.        , 1347.36842105, 1094.73684211,  252.63157895,    0.,
  505.26315789, 1600.        ,  926.31578947,    0.        ,  252.63157895,
 1178.94736842 ,1431.57894737 , 757.89473684,  505.26315789]
 ]

y = [
    [   0.     ,       0.    ,        0.  ,         84.21052632 , 252.63157895,
  336.84210526,  505.26315789,  505.26315789,  757.89473684,  842.10526316,
  926.31578947, 1094.73684211, 1347.36842105, 1347.36842105, 1431.57894737,
 1515.78947368, 1600. ,        1600.        ],
[   0.       ,     0.   ,         0.  ,         84.21052632 , 168.42105263,
  252.63157895,  336.84210526,  336.84210526,  505.26315789,  505.26315789,
  589.47368421,  673.68421053,  757.89473684,  842.10526316,  926.31578947,
  926.31578947, 1178.94736842, 1178.94736842, 1263.15789474, 1347.36842105,
 1515.78947368, 1515.78947368, 1600.     ,    1600.     ,    1600.        ],
[   0.       ,     0.        ,    0.     ,       0.     ,       0.,
   84.21052632,  252.63157895 , 252.63157895,  252.63157895,  421.05263158,
  421.05263158,  505.26315789 , 505.26315789,  589.47368421,  673.68421053,
  757.89473684,  842.10526316 , 926.31578947, 1010.52631579, 1010.52631579,
 1094.73684211, 1178.94736842 ,1263.15789474, 1347.36842105, 1431.57894737,
 1431.57894737, 1515.78947368 ,1600.        , 1600.        , 1600.,
 1600.  ,       1600.        ],
 [   0.    ,        0.      ,      0.     ,       0.    ,        0.,
    0.        ,   84.21052632 , 252.63157895,  252.63157895,  252.63157895,
  336.84210526,  421.05263158 , 505.26315789,  505.26315789,  589.47368421,
  589.47368421,  757.89473684 , 757.89473684,  757.89473684,  926.31578947,
 1010.52631579, 1010.52631579 ,1094.73684211, 1094.73684211, 1263.15789474,
 1263.15789474, 1347.36842105 ,1347.36842105, 1431.57894737, 1431.57894737,
 1515.78947368, 1515.78947368 ,1600.        , 1600.        , 1600.,
 1600.        ],
[   0.       ,     0.       ,     0.    ,        0.     ,       0.,
    0.        ,    0.        ,  168.42105263,  252.63157895,  252.63157895,
  252.63157895,  336.84210526,  421.05263158,  505.26315789,  505.26315789,
  505.26315789,  673.68421053,  673.68421053,  757.89473684,  757.89473684,
  842.10526316,  926.31578947, 1010.52631579, 1010.52631579, 1094.73684211,
 1178.94736842, 1178.94736842, 1263.15789474, 1263.15789474, 1347.36842105,
 1431.57894737, 1431.57894737, 1515.78947368, 1515.78947368, 1600.,
 1600.  ,       1600. ,        1600.        ],
 [   0.    ,        0.   ,         0.     ,       0.     ,       0.,
    0.   ,         0. ,         168.42105263 , 252.63157895,  252.63157895,
  252.63157895,  252.63157895,  336.84210526,  421.05263158,  505.26315789,
  505.26315789,  505.26315789,  589.47368421,  673.68421053,  757.89473684,
  757.89473684,  757.89473684,  926.31578947,  926.31578947, 1010.52631579,
 1010.52631579, 1094.73684211, 1178.94736842, 1178.94736842, 1178.94736842,
 1263.15789474, 1263.15789474, 1347.36842105, 1431.57894737, 1431.57894737,
 1515.78947368, 1515.78947368, 1515.78947368 ,1600.  ,       1600.,
 1600.        ],
 [   0.        ,    0.      ,      0.       ,     0.       ,     0.,
    0.         , 168.42105263,  252.63157895,  252.63157895,  252.63157895,
  336.84210526 , 336.84210526,  421.05263158,  421.05263158,  505.26315789,
  505.26315789 , 589.47368421,  589.47368421,  673.68421053,  673.68421053,
  757.89473684 , 757.89473684,  842.10526316, 1010.52631579, 1010.52631579,
 1010.52631579 ,1094.73684211, 1178.94736842, 1178.94736842, 1263.15789474,
 1263.15789474 ,1347.36842105, 1347.36842105, 1431.57894737, 1431.57894737,
 1431.57894737, 1600. ,        1600.   ,      1600.   ,      1600.,
 1600.        ],
 [   0.     ,       0.     ,       0.       ,     0.     ,       0.,
    0.        ,    0.        ,  252.63157895,  252.63157895,  252.63157895,
  252.63157895,  252.63157895,  252.63157895,  336.84210526,  505.26315789,
  505.26315789,  505.26315789,  505.26315789,  589.47368421,  589.47368421,
  673.68421053,  757.89473684,  757.89473684,  842.10526316,  926.31578947,
 1010.52631579, 1010.52631579, 1010.52631579, 1094.73684211, 1094.73684211,
 1178.94736842, 1263.15789474, 1263.15789474, 1347.36842105, 1347.36842105,
 1347.36842105, 1431.57894737, 1515.78947368, 1515.78947368, 1515.78947368,
 1515.78947368, 1600.   ,      1600.        ],
 [   0.     ,       0.    ,        0.      ,      0.     ,       0.,
    0.        ,    0.        ,  252.63157895,  252.63157895,  252.63157895,
  252.63157895,  252.63157895,  252.63157895,  336.84210526,  505.26315789,
  505.26315789,  505.26315789,  505.26315789,  589.47368421,  673.68421053,
  757.89473684,  757.89473684,  757.89473684,  757.89473684,  842.10526316,
  926.31578947, 1010.52631579, 1010.52631579, 1010.52631579, 1178.94736842,
 1178.94736842, 1263.15789474, 1263.15789474, 1263.15789474, 1263.15789474,
 1347.36842105, 1431.57894737, 1431.57894737, 1515.78947368, 1515.78947368,
 1515.78947368, 1600.        , 1600.        , 1600.        ]
]



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


ppa = np.array([25,30,40,50,60,70,80,90,100])
pro = np.zeros(len(ppa))
AEP = np.zeros(len(ppa))
COE = np.zeros(len(ppa))

for i in range(len(ppa)):
    floris_model.reinitialize_flow_field(layout_array=(x[i],y[i]))
    nturbs = len(x[i])
    AEP[i] = floris_model.get_farm_AEP(windDirections, windSpeeds, windFrequencies, limit_ws=True)/1E6
    tcc = 2500*829*nturbs
    bos = BOS_func(nturbs)
    om = 44*nturbs*2500.0
    fcr = 0.097
    cost = (tcc+bos)*fcr + om

    COE[i] = cost/AEP[i]
    pro[i] = AEP[i]*ppa[i] - cost



print("profit: ", pro)




profit = np.array([0.7439636450751536,2.7498561696183996,7.525767464436829,12.953626969420991,18.690546970579312,
            24.12682943786563,30.202910591198922,35.41446232800483,41.672003147517636])

nturbs = np.array([18,25,32,36,38,41,41,43,44])

D = 117.8
side = 1600.0

spacing = side/((nturbs**0.5-1)*D)

plt.figure(figsize=(3.0,6))

plt.subplot(411)
plt.plot(ppa,nturbs,"o",markersize=5)
ax = plt.gca()
ax.set_xticks([40,60,80,100])
ax.set_xticklabels(["","","",""])

ax.set_ylabel("number of turbines")
# ax.set_yticks([])
# ax.set_yticklabels([])

plt.subplot(412)
plt.plot(ppa,profit,"o",markersize=5)
ax = plt.gca()
ax.set_xticks([40,60,80,100])
ax.set_xticklabels(["","","",""])

ax.set_ylabel("profit ($MM)")
ax.set_yticks([0,20,40])
ax.set_yticklabels(["0","20","40"])

plt.subplot(413)
plt.plot(ppa,AEP,"o",markersize=5)
ax = plt.gca()
ax.set_xticks([40,60,80,100])
ax.set_xticklabels(["","","",""])

ax.set_ylabel("AEP (GWh)")
ax.set_yticks([400000,500000,600000])
ax.set_yticklabels(["400","500","600"])

plt.subplot(414)
plt.plot(ppa,COE,"o",markersize=5)
ax = plt.gca()
ax.set_xticks([40,60,80,100])
ax.set_xlabel("PPA ($/MWh")

ax.set_ylabel("COE ($/MWh)")
ax.set_yticks([22,26,30])
ax.set_yticklabels(["22","26","30"])


plt.subplots_adjust(left=0.2,right=0.98,top=0.99,hspace=0.1)
plt.savefig("varied_ppa.pdf",transparent=True)
plt.show()