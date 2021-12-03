import igraph as igraph
import json


class MyNewGraph:
    def __init__(self):
        pass

    def drawMergeAndCommit(self, nodePath, edgePath, picturePath):
        g = igraph.Graph(directed=True)
        with open(nodePath, 'r') as load_f:
            load_dict = json.load(load_f)
        vertex = load_dict
        g.add_vertices(vertex)
        with open(edgePath, 'r') as load_f:
            load_d = json.load(load_f)
            for e in load_d:
                g.add_edges([(e[0], e[1])])
        color_map = {'pr->merge': 'blue', 'commit->pr': 'red'}
        label_map={'pr->merge': 'm', 'commit->pr': 'c'}
        visual_style = {}
        visual_style["vertex_size"] = 30
        visual_style["vertex_label"] = g.vs["name"]
        visual_style["vertex_color"] = 'pink'
        visual_style["edge_color"] = [color_map[e[2]] for e in load_d]
        visual_style["edge_label"] = [label_map[e[2]] for e in load_d]
        visual_style["edge_width"] = 3
        visual_style["bbox"] = (2800, 1800)
        visual_style["margin"] = 30
        g.layout('kk')
        idx = list(range(g.vcount()))
        g.vs["name"] = list(map(str, idx))
        igraph.plot(g, picturePath, **visual_style)

    def drawCommit(self, nodePath, edgePath, picturePath):
        g = igraph.Graph()
        with open(nodePath, 'r') as load_f:
            load_dict = json.load(load_f)
        vertex = load_dict
        g.add_vertices(vertex)
        with open(edgePath, 'r') as load_f:
            load_d = json.load(load_f)
            for e in load_d:
                g.add_edges([(e[0], e[1])])
        # color_map = {'pr->merge': 'blue', 'commit->pr': 'red'}
        # label_map={'pr->merge': 'm', 'commit->pr': 'c'}
        visual_style = {}
        visual_style["vertex_size"] = 30
        visual_style["vertex_label"] = g.vs["name"]
        visual_style["vertex_color"] = 'pink'
        # visual_style["edge_color"] = [color_map[e[2]] for e in load_d]
        # visual_style["edge_label"] = [label_map[e[2]] for e in load_d]
        visual_style["edge_width"] = 3
        visual_style["bbox"] = (2800, 1800)
        visual_style["margin"] = 30
        g.layout('kk')
        idx = list(range(g.vcount()))
        g.vs["name"] = list(map(str, idx))
        igraph.plot(g, picturePath, **visual_style)

graph = MyNewGraph()
# graph.drawMergeAndCommit('../../resource/vue/pullRequest/nodes.json', '../../resource/vue/pullRequest/DPREdge.json',
#                          'C:\\Users\\19101\\PycharmProjects\\pythonProject1\pictures\\1.png')
graph.drawCommit('../../resource/vue/pullRequest/CommitNodes.json', '../../resource/vue/pullRequest/prEdge.json',
                         'C:\\Users\\19101\\PycharmProjects\\pythonProject1\pictures\\2.png')