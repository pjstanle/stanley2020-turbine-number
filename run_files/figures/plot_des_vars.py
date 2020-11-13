import numpy as np
import matplotlib.pyplot as plt


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

side = 900.0

plt.figure(figsize=(6.5,5))
plt.subplot(231,aspect="equal")

nrows = 6
spacing = 180.0
farm_width = (nrows-1)*spacing

outer_x = np.array([0.0,side,side,0.0,0.0])
outer_y = np.array([0.0,0.0,side,side,0.0])
plt.plot(outer_x,outer_y,"black",linewidth=1)
plt.plot(outer_x*0.8+0.1*side,outer_y*0.8+0.1*side,"C0",linewidth=2)
plt.text(775,450,r"$B$",verticalalignment="center",horizontalalignment="right")




plt.text(-50,1050,"a",fontsize=10)

plt.axis("off")
plt.xlim(-500.0,1100)
plt.ylim(-500.0,1300)


plt.subplot(232,aspect="equal")

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
plt.text(center_x,center_y+50,r"($cx$,$cy$)",horizontalalignment="center")

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

# plt.text(622,1068,"ncols",horizontalalignment="center",verticalalignment="bottom",rotation=np.rad2deg(rotation))
# plt.plot([500,200],[1100,990],'-k',linewidth=0.5)
# plt.plot([750,1040],[1190,1300],'-k',linewidth=0.5)

# plt.text(63,450,"nrows",horizontalalignment="center",verticalalignment="bottom",rotation=80)
# plt.plot([135,102],[918,744],'-k',linewidth=0.5)
# plt.plot([43,-103],[430,-446],'-k',linewidth=0.5)

plt.axis("off")
plt.xlim(-500.0,1100)
plt.ylim(-500.0,1300)

plt.plot([-43.16,-43.16-farm_height*np.sin(rotation)],[-436.2,-436.2+farm_height*np.cos(rotation)],'--k')
plt.plot([-43.16,-43.16+farm_width*np.cos(rotation)],[-436.2,-436.2+farm_width*np.sin(rotation)],'--k')

plt.text(-340,140,r"$h$",horizontalalignment="center",verticalalignment="bottom",rotation=20)
plt.text(450,-390,r"$w$",horizontalalignment="center",verticalalignment="bottom",rotation=20)

plt.text(-50,1050,"b",fontsize=10)

plt.subplot(233,aspect="equal")

plt.plot(outer_x,outer_y,"black",linewidth=1)





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

gx = np.array([])
gy = np.array([])
for i in range(nturbs):
    if rotate_x[i] < 90.0 or rotate_x[i] > 810.0 or rotate_y[i] < 90.0 or rotate_y[i] > 810.0:
        color = "C3"
    else:
        color = "C0"
        gx = np.append(gx,rotate_x[i])
        gy = np.append(gy,rotate_y[i])
    plt.plot(rotate_x[i],rotate_y[i],"o",color=color)


plt.plot(outer_x*0.8+0.1*side,outer_y*0.8+0.1*side,"C0",linewidth=2)

plt.text(-50,1050,"c",fontsize=10)

plt.axis("off")
plt.xlim(-500.0,1100)
plt.ylim(-500.0,1300)


plt.subplot(234,aspect="equal")

plt.plot(outer_x,outer_y,"black",linewidth=1)



plt.plot([-50,50],[0,0],"C3",linewidth=2)
plt.plot([-50,50],[300,300],"C3",linewidth=2)
plt.plot([0,0],[0,300],"C3",linewidth=2)

bx, by = makeBoundary(300.0,9)
plt.plot(bx,by,"o",color="C0")
plt.text(30,150,r"$s$")

plt.text(-50,1050,"d",fontsize=10)

plt.axis("off")
plt.xlim(-500.0,1100)
plt.ylim(-500.0,1300)


plt.subplot(235,aspect="equal")

plt.text(100.0,1300.0,"integer variables:",weight="bold")
plt.text(100.0,1180.0,"number of rows")
plt.text(100.0,1060.0,"number of columns")

m = 500
plt.text(-600.0,0.0+m,"integer variable:",weight="bold")
plt.text(-600.0,-120.0+m,"number of turbines")
plt.text(-600.0,-240.0+m,"on the boundary")

plt.axis("off")
plt.xlim(-500.0,1100)
plt.ylim(-500.0,1300)

plt.subplot(236,aspect="equal")

plt.plot(outer_x,outer_y,"black",linewidth=1)
plt.plot(gx,gy,"o",color="C0")
plt.plot(bx,by,"o",color="C0")

plt.text(-50,1050,"e",fontsize=10)

plt.axis("off")
plt.xlim(-500.0,1100)
plt.ylim(-500.0,1300)

plt.subplots_adjust(top=0.99,bottom=-0.12,left=-0.08,right=0.99,wspace=0.0,hspace=0.0)


plt.savefig("design_variables.pdf",transparent=True)
plt.show()