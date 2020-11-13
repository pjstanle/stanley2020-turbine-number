import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import pandas
import math
import datetime
    
if __name__ == "__main__":

    data = pandas.read_excel("data.xlsx",sheet_name="Wind PPAs by Project",header=23)
    date = data.Date
    east = data.East
    west = data.West
    cent = data.Central

    since10 = np.array([])
    for i in range(len(date)):
        if date[i].year >= 2010:
            if not math.isnan(east[i]):
                since10 = np.append(since10,east[i])
            if not math.isnan(cent[i]):
                since10 = np.append(since10,cent[i])
            if not math.isnan(west[i]):
                since10 = np.append(since10,west[i])

    since17 = np.array([])
    for i in range(len(date)):
        if date[i].year >= 2017:
            if not math.isnan(east[i]):
                since17 = np.append(since17,east[i])
            if not math.isnan(cent[i]):
                since17 = np.append(since17,cent[i])
            if not math.isnan(west[i]):
                since17 = np.append(since17,west[i])

    alldata = np.array([])
    w = np.array([])
    c = np.array([])
    e = np.array([])
    wd = np.array([])
    cd = np.array([])
    ed = np.array([])
    datedata = np.array([])
    for i in range(len(date)):
        if not math.isnan(east[i]):
            alldata = np.append(alldata,east[i])
            datedata = np.append(datedata,date[i])
            e = np.append(e,east[i])
            ed = np.append(ed,date[i])
        if not math.isnan(cent[i]):
            alldata = np.append(alldata,cent[i])
            datedata = np.append(datedata,date[i])
            c = np.append(c,cent[i])
            cd = np.append(cd,date[i])
        if not math.isnan(west[i]):
            alldata = np.append(alldata,west[i])
            datedata = np.append(datedata,date[i])
            w = np.append(w,west[i])
            wd = np.append(wd,date[i])

    plt.figure(figsize=(5,3))
    # plt.plot(datedata,alldata,"o",markersize=3)
    plt.plot(wd,w,"o",markersize=3,color="C0",label="west")
    plt.plot(cd,c,"o",markersize=3,color="C1",label="central")
    plt.plot(ed,e,"o",markersize=3,color="C3",label="east")
    plt.legend()
    plt.xlim(datetime.date(2010,1,1),datetime.date(2020,1,1))
    plt.gca().set_xticks([datetime.date(2010,1,1),datetime.date(2012,1,1),datetime.date(2014,1,1),datetime.date(2016,1,1),datetime.date(2018,1,1),datetime.date(2020,1,1)])
    plt.gca().set_xticklabels(["2010","2012","2014","2016","2018","2020"])
    plt.ylim(0,130)
    plt.xlabel("PPA execution data")
    plt.ylabel("Levelzed PPA ($/MWh)")
    plt.title("PPAs of U.S. Wind Farms since 2010",fontsize=10)
    plt.tight_layout()
    plt.savefig("historical_ppa.pdf", transparent=True)
    plt.show()