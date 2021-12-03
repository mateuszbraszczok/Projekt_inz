import matplotlib.pyplot as plt
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


def get_plot(x, y, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title(title)
    plt.plot(x,y, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('time')
    plt.ylabel(params[title])
    plt.grid()
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    ax = plt.gca()
    myFmt = DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_ylim([0, 10])
    graph = get_graph()
    return graph