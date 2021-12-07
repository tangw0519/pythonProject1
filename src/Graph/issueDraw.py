import igraph as igraph
import json

import matplotlib
import networkx as nx
from matplotlib import pyplot as plt


class IssueGraph:
    def __init__(self):
        pass

    # 使用igraph绘制vue的issue图
    def draw(self, nodePath, edgePath, picturePath):
        g = igraph.Graph(directed=True)
        with open(nodePath, 'r') as load_f:
            load_dict = json.load(load_f)
        vertex = load_dict
        g.add_vertices(vertex)
        with open(edgePath, 'r') as load_f:
            load_d = json.load(load_f)
            for e in load_d:
                g.add_edges([(e[0], e[1])])
        color_map = {'close': 'blue', 'comment': 'red'}
        label_map = {'close': 'close', 'comment': 'comment'}

        visual_style = {}
        visual_style["vertex_size"] = 50
        visual_style["vertex_label"] = g.vs["name"]
        visual_style["vertex_label_cex"] = 18
        visual_style["vertex_color"] = 'pink'
        visual_style["edge_color"] = [color_map[e[3]] for e in load_d]
        visual_style["edge_label"] = [label_map[e[3]] for e in load_d]
        visual_style["edge_width"] = 3
        # visual_style["edge_arrow_size"] = 0.5
        visual_style["bbox"] = (1800, 1200)
        visual_style["margin"] = 100

        g.layout_circle(dim=2, order=None)
        idx = list(range(g.vcount()))
        g.vs["name"] = list(map(str, idx))
        igraph.plot(g, picturePath, **visual_style)

    # 使用network,适合节点与边较少时
    def drawGraph(self, path):
        G = nx.DiGraph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for e in load_dict:
                if e[3] == 'close':
                    G.add_edges_from([(e[0], e[1])], weight=1, name='close')
                if e[3] == 'comment':
                    G.add_edges_from([(e[0], e[1])], weight=2, name='comment')

        plt.figure(1, figsize=(14, 7))  # 这里控制画布的大小，可以说改变整张图的布局
        plt.subplot(111)
        pos = nx.spring_layout(G, iterations=10, k=0.5)

        first = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] >= 1]
        second = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] >= 2]

        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='pink')
        nx.draw_networkx_edges(G, pos, edgelist=first, width=1, edge_color="r")
        nx.draw_networkx_edges(G, pos, width=1, edgelist=second, edge_color="g")

        edge_labels = nx.get_edge_attributes(G, 'name')  # 获取边的name属性，
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
        plt.axis("off")
        plt.show()


graph = IssueGraph()
# graph.draw('../../resource/vue/demo/issueNodes01.json', '../../resource/vue/demo/issueEdges01.json',
#            'C:\\Users\\19101\\PycharmProjects\\pythonProject1\pictures\\issueDemo.png')
graph.drawGraph('../../resource/vue/demo/issueEdges01.json')
graph.drawGraph('../../resource/vue/demo/issueEdges02.json')
