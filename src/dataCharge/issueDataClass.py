import json

import requests
from github import Github


class IssueDataSet:
    def __init__(self, name, access_token):
        self.name = name
        self.access_token = access_token

    def getProjectIssueCounts(self):
        g = Github(self.access_token)
        repo = g.get_repo(self.name)
        print('项目创建者：' + repo.owner.login)
        issues = repo.get_issues(state='all')
        print('项目的issues数量：')
        print(issues.totalCount)

    def getAllIssueData(self, path, low, high):
        g = Github(self.access_token)
        repo = g.get_repo(self.name)
        issues = repo.get_issues(state='all')

        IssueUrlList = []
        IssueResList = []
        for x in issues[low:high]:
            IssueUrlList.append(x.url)
        print('获取所有issue的url成功')
        k = 1
        headers = {"Authorization": "token " + self.access_token}
        for i in IssueUrlList:
            res = requests.get(i, headers=headers).json()
            IssueResList.append(res)
            print(k)
            k += 1
            filename = path
        with open(filename, 'w') as file_obj:
            json.dump(IssueResList, file_obj, indent=4)
            print('项目Issue数据保存完成')

    def getJsonFileCounts(self, Path):
        k = 0
        with open(Path, 'r') as load_f:
            load_dict = json.load(load_f)
            for x in load_dict:
                k = k + 1
        print('文件数量：', k)

    def jsonFileMerge(self, totalPath, toMergedPath1, toMergedPath2):
        with open(toMergedPath1, 'r') as load_f:
            load_dict = json.load(load_f)
        with open(toMergedPath2, 'r') as load_m:
            load_data = load_dict + json.load(load_m)
        with open(totalPath, 'w') as file_obj:
            json.dump(load_data, file_obj, indent=4)
            print('文件合并完成')

    def getDataByUrl(self, url):
        headers = {"Authorization": "token " + self.access_token}
        res = requests.get(url, headers=headers).json()
        return res

    def FiltData(self, oldPath, newPath):
        with open(oldPath, 'r') as load_f:
            load_dict = json.load(load_f)
        newList = []
        k = 1
        for issue in load_dict[10000:11741]:
            if 'pull_request' not in issue and 'message' not in issue:
                new = {}
                new['id'] = issue['id']
                new['url'] = issue['url']
                new['state'] = issue['state']
                if issue['state'] == 'closed' and issue['closed_by'] is not None:
                    new['closed_user_id'] = issue['closed_by']['id']
                    new['closed_user_name'] = issue['closed_by']['login']
                else:
                    new['closed_user_id'] = None
                    new['closed_user_name'] = None
                new['number'] = issue['number']
                new['title'] = issue['title']
                new['body'] = issue['body']
                new['comments_counts'] = issue['comments']
                new['comments_url'] = issue['comments_url']

                comment = []
                if issue['comments'] != 0:
                    comments_url = issue['comments_url']
                    data = self.getDataByUrl(comments_url)
                    for c in data:
                        x = {}
                        x['comment_creator_id'] = c['user']['id']
                        x['comment_creator_name'] = c['user']['login']
                        x['comment_created_at'] = c['created_at']
                        x['comment_updated_at'] = c['updated_at']
                        x['comment_body'] = c['body']
                        comment.append(x)
                new['comment_detail'] = comment

                new['creator_id'] = issue['user']['id']
                new['creator_name'] = issue['user']['login']
                new['assignee'] = issue['assignee']

                new['created_at'] = issue['created_at']
                new['updated_at'] = issue['updated_at']
                new['closed_at'] = issue['closed_at']
                new['author_association'] = issue['author_association']

                newList.append(new)
            print(k)
            k += 1

        with open(newPath, "w") as dump_f:
            json.dump(newList, dump_f, indent=4)
        print('保存了所有issue数据')


# 对于一个项目，首先在dataCharge获取所有issue/pr数据（getAllIssueData/getAllPRData)，然后筛选数据(FiltData/getPRInfo)，
# 再到edgeAndNode获取全部的边信息（getAllEdges），再获取全部节点信息（getNodes），再删除相同的边（deleteSameEdges）
# 再到graph画图，画图时看看边数量与粗细或者权重表示
data = IssueDataSet('vuejs/vue', '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')
data.getProjectIssueCounts()
# data.getJsonFileCounts('../../resource/vue/issue/afterFilterAll.json')
# data.getJsonFileCounts('../../resource/vue/issue/afterFilter031.json')
# data.jsonFileMerge('../../resource/vue/issue/afterFilterAll.json','../../resource/vue/issue/afterFilterAll.json','../../resource/vue/issue/afterFilter031.json')
# data.getAllIssueData('../../resource/vue/issue/2.json', 4000, 8000)
data.getJsonFileCounts('../../resource/vue/issue/afterFilterAll.json')

# data.FiltData('../../resource/vue/issue/all.json', '../../resource/vue/issue/afterFilter031.json')
