import json
from datetime import datetime


class IssueData:
    def __init__(self):
        pass

    def getJsonFileCounts(self, Path):
        k = 0
        with open(Path, 'r') as load_f:
            load_dict = json.load(load_f)
            for x in load_dict:
                k = k + 1
        print('文件数量：', k)

    def time_cmp_two(self, time, startTime, endTime):
        format_pattern = '%Y-%m-%dT%H:%M:%SZ'
        difference = (datetime.strptime(startTime, format_pattern) - datetime.strptime(time, format_pattern))
        difference01 = (datetime.strptime(endTime, format_pattern) - datetime.strptime(time, format_pattern))
        print(difference)
        if difference.days < 0 and difference01.days > 0:
            return True
        else:
            return False

    def getAllEdges(self, path, newPath):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        edges = []
        k = 1
        for s in load_dict:
            if s['state'] == 'closed':
                if s['closed_user_name'] != s['creator_name']:
                    edges.append([s['closed_user_name'], s['creator_name'], s['closed_at'], 'close', 1])
            if len(s['comment_detail']) != 0:
                for i in range(len(s['comment_detail'])):
                    if s['comment_detail'][i]['comment_creator_name'] != s['creator_name']:
                        edges.append([s['comment_detail'][i]['comment_creator_name'], s['creator_name'],
                                      s['comment_detail'][i]['comment_created_at'], 'comment', 1])
            print(k)
            k += 1
        with open(newPath, "w") as dump_f:
            json.dump(edges, dump_f, indent=4)
        print('保存了所有issue中的用户合作有向边数据')

    def deleteSameEdges(self, edgePath):
        with open(edgePath, 'r') as load_f:
            load_dict = json.load(load_f)
        res = []
        for i in load_dict:
            if i not in res:
                res.append(i)
        with open(edgePath, "w") as dump_f:
            json.dump(res, dump_f, indent=4)
        print('issueEdges,ok')

    def getNodes(self, edgePath, nodePath):
        with open(edgePath, 'r') as load_f:
            load_dict = json.load(load_f)
        nodes = []
        for x in load_dict:
            nodes.append(x[0])
            nodes.append(x[1])
        print(len(nodes))

        nodes = list(set(nodes))

        print(len(nodes))

        with open(nodePath, "w") as dump_f:
            json.dump(nodes, dump_f, indent=4)
        print('保存了所有节点数据')

    def filterEdgesByTime(self, path, newPath, startTime, endTime):
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        edges = []
        k = 1
        for s in load_dict:
            if self.time_cmp_two(s[2], startTime, endTime):
                edges.append(s)
            print(k)
            k += 1
        with open(newPath, "w") as dump_f:
            json.dump(edges, dump_f, indent=4)
        print('保存了指定时间段的有向边数据')


# 对于一个项目，首先在dataCharge获取所有issue/pr数据（getAllIssueData/getAllPRData)，然后筛选数据(FiltData/getPRInfo)，
# 再到edgeAndNode获取全部的边信息（getAllEdges），再获取全部节点信息（getNodes），再删除相同的边（deleteSameEdges）
# 再到graph画图，画图时看看边数量与粗细或者权重表示

data = IssueData()
# data.getAllEdges('../../resource/vue/issue/afterFilterAll.json', '../../resource/vue/issue/edges.json')
# data.getEdges('../../resource/vue/issue/afterFilterAll.json', '../../resource/vue/demo/issueEdges01.json')
# data.getJsonFileCounts('../../resource/vue/issue/edges.json')
# data.getNodes('../../resource/vue/demo/issueEdges01.json', '../../resource/vue/demo/issueNodes01.json')
# data.deleteSameEdges('../../resource/vue/issue/edges.json')
# data.getJsonFileCounts('../../resource/vue/issue/edges.json')
