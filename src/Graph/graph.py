import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
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
        edges = []
        for s in load_dict:
            commit = s['commitUserData']
            commitUser = []
            for i in range(len(commit)):
                commitUser.append(commit[i]['commit_author_name'])
            commitUser = list(set(commitUser))
            if len(commitUser) != 1:
                for i in range(len(commitUser) - 1):
                    for j in range(i + 1, len(commitUser)):
                        edges.append([commitUser[i], commitUser[j], 1])

        with open(newPath, "w") as dump_f:
            json.dump(edges, dump_f, indent=4)
        print('保存了所有一个pr中的用户合作边数据')

    def drawGraph(self, path):
        G = nx.Graph()
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
            for e in load_dict:
                G.add_edge(e[0], e[1], weight=e[2],length=10)
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]
        plt.figure(1, figsize=(14, 7))  # 这里控制画布的大小，可以说改变整张图的布局
        # pos = nx.spring_layout(G,iterations=20)  # positions for all nodes
        pos=nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
        nx.draw_networkx_edges(
            G, pos, width=1, edgelist=esmall, alpha=0.9, edge_color="y", style="dashed"
        )
        nx.draw_networkx_labels(G, pos, font_size=10)
        plt.axis("off")
        matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
        plt.show()

    def getPREdges(self, path, newPath):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        edges = []
        for s in load_dict:
            pr_user_name = s['pr_user_name']
            pr_mergedBy_user_name = s['pr_mergedBy_user_name']
            if pr_user_name != pr_mergedBy_user_name and pr_mergedBy_user_name is not None and pr_user_name is not None:
                edges.append([pr_mergedBy_user_name, pr_user_name, 'pr->merge'])
            commit = s['commitUserData']
            commitUser = []
            for i in range(len(commit)):
                commit_author_name = commit[i]['commit_author_name']
                if commit_author_name != pr_user_name and commit_author_name is not None and pr_user_name is not None:
                    edges.append([commit_author_name, pr_user_name, 'commit->pr'])
        with open(newPath, "w") as dump_f:
            json.dump(edges, dump_f, indent=4)
        print('保存了所有pr中的用户合作有向边数据')

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
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='b')
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
        # plt.plot(label='commit',color='g')
        # plt.plot(label='merge',color='r',linestyle='-->')
        # plt.legend()
        # plt.xlim(-0.8, 0.8)
        # plt.ylim(-0.8, 0.8)
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
        pos = nx.spring_layout(G, iterations=10)
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='b')
        nx.draw_networkx_edges(G, pos,width=1, edge_color="r")
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
        pos = nx.spring_layout(G, iterations=10)
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='b')
        nx.draw_networkx_edges(
            G, pos, width=1,alpha=0.9, edge_color="g", style="dashed"
        )
        edge_labels = nx.get_edge_attributes(G, 'name')  # 获取边的name属性，
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.axis("off")
        matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
        plt.show()

g = MyGraph('twbs/bootstrap', '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')
# g.getNodes('../../resource/vue/pullRequest/prUser.json','../../resource/vue/pullRequest/nodes.json')
# g.drawGraph02('../../resource/vue/pullRequest/nodes.json')
# g.drawTest()
# g.getEdges('../../resource/vue/pullRequest/prUser.json', '../../resource/vue/pullRequest/prEdge.json')
# g.deleteSameEdge('../../resource/vue/pullRequest/prEdge.json')
g.drawGraph('../../resource/vue/pullRequest/prEdge.json')
# g.getPREdges('../../resource/vue/pullRequest/prUser.json', '../../resource/vue/pullRequest/DPREdge.json')
g.drawDirectionGraphPR('../../resource/vue/pullRequest/DPREdge.json')
g.drawDirectionGraphMerge('../../resource/vue/pullRequest/DPREdge.json')
g.drawDirectionGraphCommit('../../resource/vue/pullRequest/DPREdge.json')
