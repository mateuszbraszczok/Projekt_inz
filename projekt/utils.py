from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

import base64
from io import BytesIO
from matplotlib.dates import DateFormatter
from pythonFiles.variables import params
from django.db.models import Avg, Max, Min

        
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

    plt.switch_backend('AGG')
    plt.title("Plot")

    fig = plt.figure()
    fig.set_size_inches(11, 8)
    ax = fig.add_subplot(111)

    label = params[variables[0]]
    type = label[0]['type']
    label = label[0]['label']
    lns1 = ax.plot(x, y, '-bo', markersize=6, label=label )
    lns = lns1

    ax.set_ylabel(label)
    ax.yaxis.label.set_color('blue')
    ax.tick_params(axis='y', colors='blue')
    if type == "bool":
            ax.set_ylim(-0.1, 1.1)

    if y2 is not None:
        ax2 = ax.twinx()
        label = params[variables[1]]
        type = label[0]['type']
        label = label[0]['label']
        
        lns2 = ax2.plot(x, y2, '-ro', markersize=4, label=label)
        lns += lns2
        ax2.set_ylabel(label)
        ax2.yaxis.label.set_color('red')
        ax2.tick_params(axis='y', colors='red')
        if type == "bool":
            ax2.set_ylim(-0.1, 1.1)

    if y3 is not None:
        ax3 = ax.twinx()
        ax3.spines['right'].set_position(("axes", 1.11))
        label = params[variables[2]]
        type = label[0]['type']
        label = label[0]['label']
        
        lns3 = ax3.plot(x, y3, '-go', markersize=3, label=label)
        lns += lns3
        ax3.set_ylabel(label)
        ax3.yaxis.label.set_color('green')
        ax3.tick_params(axis='y', colors='green')

        if type == "bool":
            ax3.set_ylim(-0.1, 1.1)


    # added these three lines

    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.13),
          fancybox=True, shadow=True, ncol=3)

    ax.grid()
    ax.set_xlabel("Time")
    

    # ax2.set_ylim(0, 35)
    # ax.set_ylim(-20,100)
    if y3 is not None:
        plt.subplots_adjust(left=0.06, right=0.85, top=0.9, bottom=0.05)
    else:
          plt.subplots_adjust(left=0.06, right=0.94, top=0.9, bottom=0.05)
   


    plt.xticks(rotation=45)
    plt.gcf().autofmt_xdate()
    ax = plt.gca()
    myFmt = DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(myFmt)
    
    plt.rcParams['axes.facecolor'] = 'lightgray'
    fig.patch.set_facecolor('darkgray')
    graph = get_graph()

    return graph

def getInfoList(variables, measurements_list):
    infoList = list()
    for el in variables:
        stats = list(measurements_list.aggregate(Avg(el), Max(el), Min(el)).values())
        infoList += [{"var": params[el][0]['label'], "values": stats}]
    return infoList