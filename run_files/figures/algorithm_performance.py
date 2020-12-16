import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":

    # small (AEP,COE,profit) big (AEP,COE,profit) huge (AEP,COE,profit)
    greedy = np.array([0.792,1.015,0.918,0.920,1.007,0.979,0.928,1.002,0.967])
    mosetti = np.array([0.973,1.000,0.971,0.624,1.031,0.655,0.685,1.015,0.921])
    sweep = np.array([0.897,1.002,0.860,0.985,1.000,0.970,0.964,1.000,1.000])
    bg = np.array([1.000,1.014,0.905,1.000,1.018,1.000,1.000,1.007,0.936])

    gradient = np.array([0.993,1.004,1.000])

    greedy_calls = np.array([2267,1860,2208,34012,28393,31902,35680,21561,29538])
    mosetti_calls = np.array([105872,106755,95687,44095,63104,47977,48739,46823,47266])
    sweep_calls = np.array([204,656,341,1220,4895,2528,1166,7812,4201])
    bg_calls = np.array([50519,26604,36510,48824,35814,52869,41175,37071,40959])

    gradient_calls = np.array([651265,655392,702650])

    x = np.arange(3)
    width = 0.8

    plt.figure(figsize=(5.5,4))
    ax = plt.subplot(211)
    ax2 = plt.subplot(212)

    # PLOT AEP
    ax.plot(x,[greedy[0],greedy[3],greedy[6]],'-o',color="C0",label="greedy grid")
    ax.plot(x,[mosetti[0],mosetti[3],mosetti[6]],'-o',color="C1",label="genetic grid")
    ax.plot(x,[sweep[0],sweep[3],sweep[6]],'-o',color="C3",label="sweep grid")
    ax.plot(x,[bg[0],bg[3],bg[6]],'-o',color="C2",label="genetic BG")

    ax.plot(x[0],gradient[0],"o",color="black",label="gradient-based")


    # PLOT COE
    ax.plot(x+3,[greedy[1],greedy[4],greedy[7]],'-o',color="C0")
    ax.plot(x+3,[mosetti[1],mosetti[4],mosetti[7]],'-o',color="C1")
    ax.plot(x+3,[sweep[1],sweep[4],sweep[7]],'-o',color="C3")
    ax.plot(x+3,[bg[1],bg[4],bg[7]],'-o',color="C2")

    ax.plot(x[0]+3,gradient[1],"o",color="black")


    # PLOT profit
    ax.plot(x+6,[greedy[2],greedy[5],greedy[8]],'-o',color="C0")
    ax.plot(x+6,[mosetti[2],mosetti[5],mosetti[8]],'-o',color="C1")
    ax.plot(x+6,[sweep[2],sweep[5],sweep[8]],'-o',color="C3")
    ax.plot(x+6,[bg[2],bg[5],bg[8]],'-o',color="C2")

    ax.plot(x[0]+6,gradient[2],"o",color="black")


    ax.legend(fontsize=8)


    # PLOT AEP
    ax2.semilogy(x,[greedy_calls[0],greedy_calls[3],greedy_calls[6]],'-o',color="C0",label="greedy grid")
    ax2.semilogy(x,[mosetti_calls[0],mosetti_calls[3],mosetti_calls[6]],'-o',color="C1",label="genetic grid")
    ax2.semilogy(x,[sweep_calls[0],sweep_calls[3],sweep_calls[6]],'-o',color="C3",label="sweep grid")
    ax2.semilogy(x,[bg_calls[0],bg_calls[3],bg_calls[6]],'-o',color="C2",label="genetic BG")

    # 2PLOT COE
    ax2.semilogy(x+3,[greedy_calls[1],greedy_calls[4],greedy_calls[7]],'-o',color="C0")
    ax2.semilogy(x+3,[mosetti_calls[1],mosetti_calls[4],mosetti_calls[7]],'-o',color="C1")
    ax2.semilogy(x+3,[sweep_calls[1],sweep_calls[4],sweep_calls[7]],'-o',color="C3")
    ax2.semilogy(x+3,[bg_calls[1],bg_calls[4],bg_calls[7]],'-o',color="C2")


    # PLOT profit
    ax2.semilogy(x+6,[greedy_calls[2],greedy_calls[5],greedy_calls[8]],'-o',color="C0")
    ax2.semilogy(x+6,[mosetti_calls[2],mosetti_calls[5],mosetti_calls[8]],'-o',color="C1")
    ax2.semilogy(x+6,[sweep_calls[2],sweep_calls[5],sweep_calls[8]],'-o',color="C3")
    ax2.semilogy(x+6,[bg_calls[2],bg_calls[5],bg_calls[8]],'-o',color="C2")

    ax2.plot(x[0],gradient_calls[0],"o",color="black",label="gradient-based")
    ax2.plot(x[0]+3,gradient_calls[1],"o",color="black")
    ax2.plot(x[0]+6,gradient_calls[2],"o",color="black")

    # ax.plot(x,greedy,"-o",color="C0",markersize=5)
    # ax.plot(x,mosetti,"-o",color="C1",markersize=5)
    # ax.plot(x,sweep,"-o",color="C3",markersize=5)
    # ax.plot(x,bg,"-o",color="C2",markersize=5)

    
    ax.set_ylabel("normalized optimal\nvalue")
    ax2.set_ylabel("number of function\ncalls")
    ax.set_xticks([0,1,2,3,4,5,6,7,8])
    ax.set_xticklabels(["","","","","","","","",""])

    ax2.set_xticks([0,1,2,3,4,5,6,7,8])
    ax2.set_xticklabels(["small uni","large uni","large full","small uni","large uni","large full","small uni","large uni","large full"],rotation=60,fontsize=6)

    ax2.text(1,3.5,"AEP objective",horizontalalignment="center")
    ax2.text(4,3.5,"COE objective",horizontalalignment="center")
    ax2.text(7,3.5,"profit objective",horizontalalignment="center")
    ax.set_ylim(0.85,1.05)

    plt.subplots_adjust(top=0.98,bottom=0.2,right=0.98,hspace=0.15,left=0.15)

    plt.savefig("algorithms.pdf",transparent=True)
    plt.show()