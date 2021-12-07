from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import json


class MyGraphData:
    def __init__(self, name, access_token):
        self.name = name
        self.access_token = access_token

    def getJsonFileCounts(self, Path):
        k = 0
        with open(Path, 'r') as load_f:
            load_dict = json.load(load_f)
            for x in load_dict:
                k = k + 1
        print('文件数量：', k)

    def getAllEdges(self, path, newPath):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        edges = []
        for s in load_dict:
            if s['pr_creator_name'] is not None:
                pr_creator_name = s['pr_creator_name']
                if s['merge'] and s['pr_mergedBy_user_name'] is not None and s[
                    'pr_mergedBy_user_name'] != pr_creator_name:
                    edges.append([s['pr_mergedBy_user_name'], pr_creator_name, s['merged_at'], 'merge', 1])

                if len(s['commitData']) != 0:
                    commit = s['commitData']
                    for m in commit:
                        if m['commit_author_name'] is not None and m['commit_author_name'] != pr_creator_name:
                            edges.append(
                                [m['commit_author_name'], pr_creator_name, m['commit_author_date'], 'commit', 1])
                if 'commentData' in s:
                    if len(s['commentData']) != 0:
                        comment = s['commentData']
                        for com in comment:
                            if com['comment_creator'] is not None and com['comment_creator'] != pr_creator_name:
                                edges.append([com['comment_creator'], pr_creator_name, com['created_at'], 'comment', 1])
                if 'reviewData' in s:
                    if len(s['reviewData']) != 0:
                        review = s['reviewData']
                        for re in review:
                            if re['review_comment_creator'] is not None and re[
                                'review_comment_creator'] != pr_creator_name:
                                edges.append(
                                    [re['review_comment_creator'], pr_creator_name, re['created_at'], 'review', 1])

        with open(newPath, "w") as dump_f:
            json.dump(edges, dump_f, indent=4)
        print('保存了所有pr中的用户合作有向边数据')

    # def getCommitEdges(self, path, newPath):
    #     with open(path, 'r') as load_f:
    #         load_dict = json.load(load_f)
    #     edges = []
    #     for s in load_dict[0:2]:
    #         commit = s['commitUserData']
    #         commitUser = []
    #         for i in range(len(commit)):
    #             commitUser.append(commit[i]['commit_author_name'])
    #         commitUser = list(set(commitUser))
    #         if len(commitUser) != 1:
    #             for i in range(len(commitUser) - 1):
    #                 for j in range(i + 1, len(commitUser)):
    #                     edges.append([commitUser[i], commitUser[j], 1])
    #
    #     with open(newPath, "w") as dump_f:
    #         json.dump(edges, dump_f, indent=4)
    #     print('保存了所有一个pr中的用户合作边数据')

    def getNodes(self, edgePath, newPath):
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

    def deleteSameEdges(self, edgePath):
        with open(edgePath, 'r') as load_f:
            load_dict = json.load(load_f)
        res = []
        for i in load_dict:
            if i not in res:
                res.append(i)
        with open(edgePath, "w") as dump_f:
            json.dump(res, dump_f, indent=4)
        print('ggf')

    def time_cmp_two(self, time, startTime, endTime):
        format_pattern = '%Y-%m-%dT%H:%M:%SZ'
        difference = (datetime.strptime(startTime, format_pattern) - datetime.strptime(time, format_pattern))
        difference01 = (datetime.strptime(endTime, format_pattern) - datetime.strptime(time, format_pattern))
        if difference.days < 0 and difference01.days > 0:
            return True
        else:
            return False

    def getEdgesByTime(self, path, newPath, startTime, endTime):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        edges = []
        for s in load_dict:
            if self.time_cmp_two(s[2], startTime, endTime):
                edges.append(s)
        with open(newPath, "w") as dump_f:
            json.dump(edges, dump_f, indent=4)
        print('保存了指定时间段的有向边数据')


# 对于一个项目，首先在dataCharge获取所有issue/pr数据（getAllIssueData/getAllPRData)，然后筛选数据(FiltData/getPRInfo)，
# 再到edgeAndNode获取全部的边信息（getAllEdges），再获取全部节点信息（getNodes），再删除相同的边（deleteSameEdges）
# 再到graph画图，画图时看看边数量与粗细或者权重表示
g = MyGraphData('twbs/bootstrap', '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')
# g.getAllEdges('../../resource/vue/pullRequest/afterFilter.json', '../../resource/vue/pullRequest/edges.json')
# g.getNodes('../../resource/vue/pullRequest/edges.json','../../resource/vue/pullRequest/nodes.json')
# g.getJsonFileCounts('../../resource/vue/pullRequest/nodes.json')
# g.getEdgesByTime('../../resource/vue/pullRequest/edges.json', '../../resource/vue/demo/PREdges01.json', '2013-03-05T00:00:00Z',
#             '2014-03-05T00:00:00Z')
# g.getJsonFileCounts('../../resource/vue/demo/PREdges01.json')
#
g.getEdgesByTime('../../resource/vue/pullRequest/edges.json', '../../resource/vue/demo/PREdges01.json',
                 '2013-03-05T00:00:00Z',
                 '2014-03-05T00:00:00Z')
g.getJsonFileCounts('../../resource/vue/demo/PREdges01.json')
g.getEdgesByTime('../../resource/vue/pullRequest/edges.json', '../../resource/vue/demo/PREdges02.json',
                 '2014-03-05T00:00:00Z',
                 '2014-04-05T00:00:00Z')
g.getJsonFileCounts('../../resource/vue/demo/PREdges02.json')
# g.deleteSameEdges('../../resource/vue/pullRequest/edges.json')
