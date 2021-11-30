import matplotlib.pyplot as plt
import networkx as nx
import json


class MyGraph:
    def __init__(self, name, access_token):
        self.name = name
        self.access_token = access_token

    def getUserInfo(self, oldPath, newPath):

        with open(oldPath, 'r') as load_f:
            load_dict = json.load(load_f)
        pullResList = []
        for x in load_dict:
            new = {}
            new['pr_user_name'] = x['pr_user_name']
            # new['merged_at'] = x['merged_at']
            new['pr_mergedBy_user_name'] = x['pr_mergedBy_user_name']
            commitDetail = x['commitData']

            commitUser = []

            for s in commitDetail:
                com = {}
                com['commit_author_name'] = s['commit_author']['name']
                com['commit_committer_name'] = s['commit_committer']['name']
                commitUser.append(com)
            new['commitUserData'] = commitUser
            pullResList.append(new)

        with open(newPath, "w") as dump_f:
            json.dump(pullResList, dump_f, indent=4)
        print('保存了所有User数据')

    def getNodes(self, oldPath, newPath):
        with open(oldPath, 'r') as load_f:
            load_dict = json.load(load_f)
        nodes = []
        for x in load_dict:
            pr_user_name = x['pr_user_name']
            pr_mergedBy_user_name = x['pr_mergedBy_user_name']
            nodes.append(pr_user_name)
            nodes.append(pr_mergedBy_user_name)
            commitUserData = x['commitUserData']
            for s in commitUserData:
                commit_author_name = s['commit_author_name']
                commit_committer_name = s['commit_committer_name']
                nodes.append(commit_author_name)
                nodes.append(commit_committer_name)
        print(len(nodes))

        nodes = list(set(nodes))

        print(len(nodes))

        with open(newPath, "w") as dump_f:
            json.dump(nodes, dump_f, indent=4)
        print('保存了所有User数据')

    def getEdges(self, path, newPath):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)


    def drawGraph(self, path):
        G = nx.Graph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for i in range(0, 20):
                G.add_edge(load_dict[i], load_dict[i + 1], weight=0.9)
                G.add_edge(load_dict[i], load_dict[i + 2], weight=0.9)
            # G.add_edge("a", "c", weight=0.2)
            # G.add_edge("c", "d", weight=0.1)
            # G.add_edge("c", "e", weight=0.7)
            # G.add_edge("c", "f", weight=0.9)
            # G.add_edge("a", "d", weight=0.3)

        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

        pos = nx.spring_layout(G)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=1000)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
        nx.draw_networkx_edges(
            G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
        )

        # labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

        plt.axis("off")
        plt.show()

    def drawGraph02(self, path):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        nodes = load_dict
        G = nx.DiGraph()
        for node in nodes[0:10]:
            G.add_node(node)
        # with open("../entity/edge.txt", 'r') as load_f:
        #     load_edge = json.load(load_f)
        #     print(load_edge)
        # edges = load_edge
        edges = [
            ('David Yu', 'Miccy.Wei'),
            ('Mateus Velleda Vellar', 'Miccy.Wei'),
            ('Bogdan Luca', 'Brendan Bowidas'),
            ('Brendan Bowidas', 'yantene'),
            ('Alex Ivasyuv', 'yantene'),
            ('Dmitry Vakhnenko', 'Alex Ivasyuv'),
            ('kingwl', 'Brendan Bowidas'),
            ('Miccy.Wei', 'Bogdan Luca'),
            ('niris', 'Mateus Velleda Vellar'),
            ('kingwl', 'Dmitry Vakhnenko'),
            ('Alex Ivasyuv', 'CodinCat'),
            ('niris', 'Alex Ivasyuv')
        ]

        r = G.add_edges_from(edges)
        nx.draw(G, with_labels=True, node_color='y', )
        plt.show()


g = MyGraph('twbs/bootstrap', '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')
# g.getNodes('../../resource/vue/pullRequest/prUser.json','../../resource/vue/pullRequest/nodes.json')
g.drawGraph02('../../resource/vue/pullRequest/nodes.json')
