import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import json


class MyGraph:
    def __init__(self, name, access_token):
        self.name = name
        self.access_token = access_token

    def drawGraph(self, path):
        G = nx.Graph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for e in load_dict:
                G.add_edge(e[0], e[1], weight=e[2], length=10)
        plt.figure(1, figsize=(14, 7))  # 这里控制画布的大小，可以说改变整张图的布局
        pos = nx.spring_layout(G, k=0.8, iterations=20, scale=2)  # positions for all nodes
        # pos=nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='pink')
        nx.draw_networkx_edges(
            G, pos, width=1, alpha=0.9, edge_color="b"
        )
        nx.draw_networkx_labels(G, pos, font_size=10)
        plt.axis("off")
        matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
        plt.show()

    def drawDirectionGraphPR(self, path):
        G = nx.DiGraph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for e in load_dict:
                if e[2] == 'pr->merge':
                    G.add_edges_from([(e[0], e[1])], weight=0.6, name='m')
                if e[2] == 'commit->pr':
                    G.add_edges_from([(e[0], e[1])], weight=0.2, name='c')
        plt.figure(1, figsize=(14, 7))  # 这里控制画布的大小，可以说改变整张图的布局
        plt.subplot(111)
        # pos = nx.kamada_kawai_layout(G)
        # pos = nx.shell_layout(G)
        pos = nx.spring_layout(G, iterations=10)
        enlarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        small = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='pink')
        nx.draw_networkx_edges(G, pos, edgelist=enlarge, width=1, edge_color="r")
        nx.draw_networkx_edges(
            G, pos, width=1, edgelist=small, alpha=0.9, edge_color="g", style="dashed"
        )
        edge_labels = nx.get_edge_attributes(G, 'name')  # 获取边的name属性，
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.axis("off")
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        plt.show()

    def drawDirectionGraphMerge(self, path):
        G = nx.DiGraph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for e in load_dict:
                if e[2] == 'pr->merge':
                    G.add_edges_from([(e[0], e[1])], weight=0.6, name='m')
        plt.figure(1, figsize=(14, 7))  # 这里控制画布的大小，可以说改变整张图的布局
        plt.subplot(111)
        pos = nx.spring_layout(G, iterations=10, k=0.5)
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='pink')
        nx.draw_networkx_edges(G, pos, width=1, edge_color="b")
        edge_labels = nx.get_edge_attributes(G, 'name')  # 获取边的name属性，
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
        plt.axis("off")
        plt.show()

    def drawDirectionGraphCommit(self, path):
        G = nx.DiGraph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for e in load_dict:
                if e[2] == 'commit->pr':
                    G.add_edges_from([(e[0], e[1])], weight=0.2, name='c')
        plt.figure(2, figsize=(14, 7))  # 这里控制画布的大小，可以说改变整张图的布局
        plt.subplot(111)
        pos = nx.spring_layout(G, iterations=10, k=0.5)
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='pink')
        nx.draw_networkx_edges(
            G, pos, width=1, alpha=0.9, edge_color="b", style="dashed"
        )
        edge_labels = nx.get_edge_attributes(G, 'name')  # 获取边的name属性，
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.axis("off")
        matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
        plt.show()


g = MyGraph('twbs/bootstrap', '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')
g.drawGraph('../../resource/vue/pullRequest/prEdge.json')
g.drawDirectionGraphPR('../../resource/vue/pullRequest/DPREdge.json')
g.drawDirectionGraphMerge('../../resource/vue/pullRequest/DPREdge.json')
g.drawDirectionGraphCommit('../../resource/vue/pullRequest/DPREdge.json')
