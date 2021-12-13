from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import numpy as np

import base64
from io import BytesIO
from matplotlib.dates import DateFormatter
from pythonFiles.variables import params

        

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(title, x, y, y2 = None, y3=None):
    plt.switch_backend('AGG')
    plt.figure(figsize=(12,8))
    plt.title(title)


    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.7)


    if y2 is not None:
        par1 = host.twinx()
        par2 = host.twinx()
        offset = 0
        new_fixed_axis = par1.get_grid_helper().new_fixed_axis
        par1.axis["right"] = new_fixed_axis(loc="right",
                                            axes=par1,
                                            offset=(offset, 0))

        par1.axis["right"].toggle(all=True)

    if y3 is not None:
        offset = 50
        new_fixed_axis = par2.get_grid_helper().new_fixed_axis
        par2.axis["right"] = new_fixed_axis(loc="right",
                                            axes=par2,
                                            offset=(offset, 0))
        par2.axis["right"].toggle(all=True)
    

    p1, = host.plot(x, y, label="Temperature")
    minY = min(y) * 0.8
    maxY = max(y) * 1.2
    host.set_ylim(minY, maxY)
    if y2 is not None:
        p2, = par1.plot(x, y2, label="Redox")
        minY2 = min(y2) * 0.8
        maxY2 = max(y2) * 1.4
        par1.set_ylim(minY2, maxY2)
    if y3 is not None:
        p3, = par2.plot(x, y3, label="Turbidity")
        minY3 = min(y3) * 0.7
        maxY3 = max(y3) * 1.4
        par2.set_ylim(minY3, maxY3)


    #host.set_xlabel("Time")
    host.legend()
    host.set_ylabel("Temperature")

    host.axis["left"].label.set_color(p1.get_color())
    host.grid()
    if y2 is not None:
        par1.axis["right"].label.set_color(p2.get_color())
        par1.set_ylabel("Redox")

    if y3 is not None:
        par2.axis["right"].label.set_color(p3.get_color())
        par2.set_ylabel("Turbidity")
    
    plt.tight_layout(pad=2)
    # plt.xticks([], [])
    # plt.yticks([], [])
    #plt.yticks([])
    # plt.grid()
    # plt.xticks(rotation=45)
    # plt.gcf().autofmt_xdate()
    # ax = plt.gca()
    # myFmt = DateFormatter('%H:%M:%S')
    # ax.xaxis.set_major_formatter(myFmt)
    # ax.set_ylim([0, 10])
    graph = get_graph()

    return graph