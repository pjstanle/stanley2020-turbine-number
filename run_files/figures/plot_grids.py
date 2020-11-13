import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(6.5,3))
plt.subplot(131,aspect="equal")

nrows = 6
spacing = 180.0
farm_width = (nrows-1)*spacing

outer_x = ([0.0,farm_width,farm_width,0.0,0.0])
outer_y = ([0.0,0.0,farm_width,farm_width,0.0])
plt.plot(outer_x,outer_y,"C1",linewidth=3)

for i in range(nrows):
    row_x = np.array([0.0,farm_width])
    row_y = np.array([spacing*i,spacing*i])

    col_y = np.array([0.0,farm_width])
    col_x = np.array([spacing*i,spacing*i])

    plt.plot(row_x,row_y,"C0",linewidth=0.5)
    plt.plot(col_x,col_y,"C0",linewidth=0.5)

for i in range(nrows):
    for j in range(nrows):
        plt.plot(spacing*i,spacing*j,"o",color="C0")



plt.text(-50,1050,"a",fontsize=10)

plt.axis("off")
plt.xlim(-250.0,1100)
plt.ylim(-500.0,1300)


plt.subplot(132,aspect="equal")

nrows = 7
ncols = 5
farm_width = 900.0
farm_height = 1200.0
xlocs = np.linspace(0.0,farm_width,ncols)
ylocs = np.linspace(0.0,farm_height,nrows)

center_x = 500.0
center_y = 400.0
shear = np.deg2rad(30.0)
rotation = np.deg2rad(20.0)

y_spacing = ylocs[1]-ylocs[0]
x_spacing = xlocs[1]-xlocs[0]

max_x = farm_width + (nrows-1)*y_spacing*np.tan(shear)
max_y = (nrows-1)*y_spacing
mean_x = 543.1686658980069
mean_y = 836.2038900585054

for i in range(nrows):
    row_x = np.array([0.0,farm_width])+ float(i)*y_spacing*np.tan(shear)
    row_y = np.array([y_spacing*i,y_spacing*i])
    # rotate
    rotate_x = np.cos(rotation)*row_x - np.sin(rotation)*row_y
    rotate_y = np.sin(rotation)*row_x + np.cos(rotation)*row_y
    # move center of grid
    rotate_x = (rotate_x - mean_x) + center_x
    rotate_y = (rotate_y - mean_y) + center_y

    plt.plot(rotate_x,rotate_y,linewidth=0.5,color="C0")


for i in range(ncols):
    col_x = np.array([x_spacing*i,x_spacing*i+farm_height*np.tan(shear)])
    col_y = np.array([0.0,farm_height])
    # rotate
    rotate_x = np.cos(rotation)*col_x - np.sin(rotation)*col_y
    rotate_y = np.sin(rotation)*col_x + np.cos(rotation)*col_y
    # move center of grid
    rotate_x = (rotate_x - mean_x) + center_x
    rotate_y = (rotate_y - mean_y) + center_y

    plt.plot(rotate_x,rotate_y,linewidth=0.5,color="C0")





plt.plot(center_x,center_y,"ok")
plt.text(center_x,center_y+50,"(cx,cy)",horizontalalignment="center")

plt.plot([center_x,center_x+500],[center_y,center_y],'--k')

from matplotlib import patches
e1 = patches.Arc((center_x, center_y), 800.0, 800.0,
                 linewidth=1,theta1=0.0,theta2=np.rad2deg(rotation))
plt.gca().add_patch(e1)
plt.text(center_x+450,center_y+75,r"$\theta$",horizontalalignment="center",verticalalignment="center")
L = 500.0
plt.plot([-43.16,-43.16-L*np.sin(rotation)],[-436.2,-436.2+L*np.cos(rotation)],'--k')
plt.plot([-43.16,-43.16+L*np.cos(rotation)],[-436.2,-436.2+L*np.sin(rotation)],'--k')
e2 = patches.Arc((-43.16, -436.2), 800.0, 800.0,
                 linewidth=1,theta1=90.0+np.rad2deg(rotation)-np.rad2deg(shear),theta2=90.0+np.rad2deg(rotation))
plt.gca().add_patch(e2)
plt.text(-80,40,r"$\phi$",horizontalalignment="center",verticalalignment="center")

plt.text(622,1068,"ncols",horizontalalignment="center",verticalalignment="bottom",rotation=np.rad2deg(rotation))
plt.plot([500,200],[1100,990],'-k',linewidth=0.5)
plt.plot([745,1040],[1190,1300],'-k',linewidth=0.5)

plt.text(63,450,"nrows",horizontalalignment="center",verticalalignment="bottom",rotation=80)
plt.plot([135,102],[918,744],'-k',linewidth=0.5)
plt.plot([43,-103],[430,-446],'-k',linewidth=0.5)

plt.axis("off")
plt.xlim(-250.0,1100)
plt.ylim(-500.0,1300)

plt.text(-50,1050,"b",fontsize=10)

plt.subplot(133,aspect="equal")

plt.plot(outer_x,outer_y,"C1",linewidth=3)



for i in range(nrows):
    row_x = np.array([0.0,farm_width])+ float(i)*y_spacing*np.tan(shear)
    row_y = np.array([y_spacing*i,y_spacing*i])
    # rotate
    rotate_x = np.cos(rotation)*row_x - np.sin(rotation)*row_y
    rotate_y = np.sin(rotation)*row_x + np.cos(rotation)*row_y
    # move center of grid
    rotate_x = (rotate_x - mean_x) + center_x
    rotate_y = (rotate_y - mean_y) + center_y

    plt.plot(rotate_x,rotate_y,linewidth=0.5,color="C0")


for i in range(ncols):
    col_x = np.array([x_spacing*i,x_spacing*i+farm_height*np.tan(shear)])
    col_y = np.array([0.0,farm_height])
    # rotate
    rotate_x = np.cos(rotation)*col_x - np.sin(rotation)*col_y
    rotate_y = np.sin(rotation)*col_x + np.cos(rotation)*col_y
    # move center of grid
    rotate_x = (rotate_x - mean_x) + center_x
    rotate_y = (rotate_y - mean_y) + center_y

    plt.plot(rotate_x,rotate_y,linewidth=0.5,color="C0")

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

for i in range(nturbs):
    if rotate_x[i] < 0.0 or rotate_x[i] > 900.0 or rotate_y[i] < 0.0 or rotate_y[i] > 900.0:
        color = "C3"
    else:
        color = "C0"
    plt.plot(rotate_x[i],rotate_y[i],"o",color=color)



plt.text(-50,1050,"c",fontsize=10)

plt.axis("off")
plt.xlim(-250.0,1100)
plt.ylim(-500.0,1300)

plt.subplots_adjust(top=0.99,bottom=0.01,left=0.01,right=0.99)


plt.savefig("grids_figure.pdf",transparent=True)
plt.show()