import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
   
ndirs_interp = 17
windDirections_interp = np.linspace(0.0,360.,ndirs_interp)
windFrequencies_interp = np.array([2.0,2.0,3.0,4.0,6.0,6.0,10.0,12.0,6.0,4.0,4.0,8.0,21.0,5.0,3.0,1.0,2.0])
freq_func = scipy.interpolate.interp1d(windDirections_interp, windFrequencies_interp, kind='cubic')
ndirs = 72
wd = np.linspace(0.0,360.-360./ndirs,ndirs)
ws = np.ones(ndirs)*10.0
wf = freq_func(wd)
wf = wf/sum(wf)

print("wd: ", wd)
print("wf: ", wf)

bottom = 0
width = (2.*np.pi) / float(ndirs)

# wd -= wd[np.argmax(wf*ws**3)]
wd += 270.
# wd +=180./float(nDirections)



plt.figure(figsize=(3,3))
ax = plt.gca(polar=True)
for i in range(ndirs):
   wd[i] = np.radians(wd[i])*-1.
"""wind rose"""
max_height = max(wf)

thetaticks = np.arange(0,360,45)
ax.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'],fontsize=8)
ax.set_thetagrids(thetaticks)
ax.set_rgrids([0.02,0.04], angle=35.)
ax.set_yticklabels(['0.02','0.04'],horizontalalignment='center',fontsize=8)
ax.set_ylim(0.,0.05)

bars = ax.bar(wd, wf, width=width, bottom=bottom, color='C0',alpha=1.0)


plt.savefig("windrose.pdf",transparent=True)
plt.show()