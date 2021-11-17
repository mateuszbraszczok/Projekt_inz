import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    # print(image_png)


    graph = base64.b64encode(image_png)
    # print(graph)
    graph = graph.decode('utf-8')
    #print(graph)
    buffer.close()
    return graph


def get_plot(x, y, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title(title)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.grid()
    plt.tight_layout()
    ax = plt.gca()
    ax.set_ylim([0, 10])
    graph = get_graph()
    return graph