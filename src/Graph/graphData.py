import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import json


class MyGraphData:
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

    def getNodes02(self, edgePath, newPath):
        with open(edgePath, 'r') as load_f:
            load_dict = json.load(load_f)
        nodes = []
        for x in load_dict:
            nodes.append(x[0])
            nodes.append(x[1])
        print(len(nodes))

        nodes = list(set(nodes))

        print(len(nodes))

        with open(newPath, "w") as dump_f:
            json.dump(nodes, dump_f, indent=4)
        print('保存了所有User数据')


g = MyGraphData('twbs/bootstrap', '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')
# g.getNodes('../../resource/vue/pullRequest/prUser.json','../../resource/vue/pullRequest/nodes.json')
# g.getEdges('../../resource/vue/pullRequest/prUser.json', '../../resource/vue/pullRequest/prEdge.json')
# g.getNodes02('../../resource/vue/pullRequest/DPREdge.json', '../../resource/vue/pullRequest/nodes.json')
g.getNodes02('../../resource/vue/pullRequest/prEdge.json', '../../resource/vue/pullRequest/CommitNodes.json')
