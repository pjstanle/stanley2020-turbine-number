import numpy as np
import matplotlib.pyplot as plt


side = 900.0

plt.figure(figsize=(3.,2.5))
plt.subplot(111,aspect="equal")


plt.axis("off")

n = 8
g = np.linspace(0,side,n)
for i in range(n):
    for j in range(n):
        plt.plot([g[i],g[i]],[0.0,side],color="black")
        plt.plot([0.0,side],[g[i],g[i]],color="black")
        

for i in range(n):
    for j in range(n):  
        plt.plot(g[i],g[j],"o",color="C0")


plt.savefig("mosetti_grid.pdf",transparent=True)
plt.show()