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


def get_plot(variables, x, y, y2 = None, y3=None):
    # plt.switch_backend('AGG')
    # plt.figure(figsize=(12,8))
    # plt.title("Plot")

    # host = host_subplot(111, axes_class=AA.Axes)
    # plt.subplots_adjust(right=0.7)

    # if y2 is not None:
    #     par1 = host.twinx()
    #     par2 = host.twinx()
    #     offset = 0
    #     new_fixed_axis = par1.get_grid_helper().new_fixed_axis
    #     par1.axis["right"] = new_fixed_axis(loc="right",
    #                                         axes=par1,
    #                                         offset=(offset, 0))

    #     par1.axis["right"].toggle(all=True)

    # if y3 is not None:
    #     offset = 50
    #     new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    #     par2.axis["right"] = new_fixed_axis(loc="right",
    #                                         axes=par2,
    #                                         offset=(offset, 0))
    #     par2.axis["right"].toggle(all=True)
    

    # p1, = host.plot(x, y, label=params[variables[0]])   
    # minY = min(y) * 0.8
    # maxY = max(y) * 1.2
    # host.set_ylim(minY, maxY)

    # if y2 is not None:
    #     p2, = par1.plot(x, y2, label=params[variables[1]])
    #     minY2 = min(y2) * 0.8
    #     maxY2 = max(y2) * 1.4
    #     par1.set_ylim(minY2, maxY2)
    # if y3 is not None:
    #     p3, = par2.plot(x, y3, label=params[variables[2]])
    #     minY3 = min(y3) * 0.7
    #     maxY3 = max(y3) * 1.4
    #     par2.set_ylim(minY3, maxY3)


    # #host.set_xlabel("Time")
    # host.legend()
    # host.set_ylabel(params[variables[0]])

    # host.axis["left"].label.set_color(p1.get_color())
    # host.grid()
    # host.axis('off')
    # if y2 is not None:
    #     par1.axis["right"].label.set_color(p2.get_color())
    #     par1.set_ylabel(params[variables[1]])

    # if y3 is not None:
    #     par2.axis["right"].label.set_color(p3.get_color())
    #     par2.set_ylabel(params[variables[2]])
    
    # plt.tight_layout(pad=2)
    # plt.plot(x, y, label=params[variables[0]])
    # plt.xticks([], [])
    # #plt.yticks([], [])
    # #plt.yticks([])
    # # plt.grid()
    # # plt.xticks(rotation=45)
    # # plt.gcf().autofmt_xdate()
    # # ax = plt.gca()
    # # myFmt = DateFormatter('%H:%M:%S')
    # # ax.xaxis.set_major_formatter(myFmt)
    # # ax.set_ylim([0, 10])



    time = np.arange(10)
    temp = np.random.random(10)*30
    Swdown = np.random.random(10)*100-10
    Rn = np.random.random(10)*100-10

    plt.switch_backend('AGG')
    plt.figure(figsize=(10,8))
    plt.title("Plot")

    host = host_subplot(111, axes_class=AA.Axes)

    fig = plt.figure()
    fig.set_size_inches(12, 8)
    ax = fig.add_subplot(111)

    label = params[variables[0]]
    label = label[0]['label']
    lns1 = ax.plot(x, y, '-bo', markersize=6, label=label )
    
    lns = lns1
    
    ax.set_ylabel(label)
    ax.yaxis.label.set_color('blue')
    if y2 is not None:
        ax2 = ax.twinx()
        label = params[variables[1]]
        label = label[0]['label']
        lns2 = ax2.plot(x, y2, '-ro', markersize=4, label=label)
        lns += lns2
        ax2.set_ylabel(label)
        ax2.yaxis.label.set_color('red')

    if y3 is not None:
        ax3 = ax.twinx()
        label = params[variables[2]]
        label = label[0]['label']
        ax3.spines['right'].set_position(("axes", 1.12))

        lns3 = ax3.plot(x, y3, '-go', markersize=3, label=label)
        lns += lns3
        ax3.set_ylabel(label)
        ax3.yaxis.label.set_color('green')

    # added these three lines

    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.grid()
    ax.set_xlabel("Time")
    

    # ax2.set_ylim(0, 35)
    # ax.set_ylim(-20,100)
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.05)

    plt.xticks(rotation=45)
    plt.gcf().autofmt_xdate()
    ax = plt.gca()
    myFmt = DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(myFmt)
    graph = get_graph()

    return graph