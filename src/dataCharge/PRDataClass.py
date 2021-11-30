import json

import requests
from github import Github


class DataSet:
    def __init__(self, name, access_token):
        self.name = name
        self.access_token = access_token

    def getProjectPRCounts(self):
        g = Github(self.access_token)
        repo = g.get_repo(self.name)
        print('项目创建者：' + repo.owner.login)
        pulls = repo.get_pulls('all')
        print('项目的pulls数量：', pulls.totalCount)

    def getAllPRData(self, path, low, high):
        g = Github(self.access_token)
        repo = g.get_repo(self.name)
        pulls = repo.get_pulls('all')

        pullUrlList = []
        pullResList = []

        for x in pulls[low:high]:
            print(x.url)
            pullUrlList.append(x.url)

        headers = {"Authorization": "token " + self.access_token}
        for i in pullUrlList:
            res = requests.get(i, headers=headers).json()
            pullResList.append(res)
            filename = path
        with open(filename, 'w') as file_obj:
            json.dump(pullResList, file_obj, indent=4)
            print('项目PR数据保存完成')

    def jsonFileMerge(self, totalPath, toMergedPath):
        with open(totalPath, 'r') as load_f:
            load_dict = json.load(load_f)
        with open(toMergedPath, 'r') as load_m:
            load_data = load_dict + json.load(load_m)
        with open(totalPath, 'w') as file_obj:
            json.dump(load_data, file_obj, indent=4)
            print('文件合并完成')

    def getJsonFileCounts(self, Path):
        k = 0
        with open(Path, 'r') as load_f:
            load_dict = json.load(load_f)
            for x in load_dict:
                k = k + 1
        print('文件数量：', k)

    def getCommitsNotOnePR(self, oldPath, newPath):
        k = 0
        with open(oldPath, 'r') as load_f:
            load_dict = json.load(load_f)
            for x in load_dict:
                commits = x['commits']
                if commits != 1:
                    k = k + 1
        print(k)
        s = 0
        load_n = [item for item in load_dict if item["commits"] != 1]
        for m in load_n:
            s = s + 1
        with open(newPath, "w") as dump_f:
            json.dump(load_n, dump_f, indent=4)
        print('更新成功，删除了commit为1的pullRequest数据')

    def getMergedPR(self, oldPath, newPath):
        with open(oldPath, 'r') as load_f:
            load_dict = json.load(load_f)
            print(len(load_dict))
            load_n = [item for item in load_dict if item["merged"]]
            with open(newPath, "w") as dump_f:
                json.dump(load_n, dump_f, indent=4)
            print('更新成功，删除了没有合并的pullRequest数据')

    def getCommitDataByUrl(self, commit_url):
        headers = {"Authorization": "token " + self.access_token}
        res = requests.get(commit_url, headers=headers).json()
        return res

    def getUserNameByUrl(self, user_url):
        headers = {"Authorization": "token " + self.access_token}
        res = requests.get(user_url, headers=headers).json()
        name = res['name']
        return name

    def getCommitData(self, mergedPath, newPath):
        with open(mergedPath, 'r') as load_f:
            load_dict = json.load(load_f)

        pullResList = []
        for x in load_dict:
            new = {}
            new['pr_id'] = x['id']
            new['pr_number'] = x['number']
            new['pr_state'] = x['state']
            new['pr_title'] = x['title']
            new['created_at'] = x['created_at']
            new['updated_at'] = x['updated_at']
            new['closed_at'] = x['closed_at']
            new['pr_user_id'] = x['user']['id']
            new['pr_user_login'] = x['user']['login']
            user_url = x['user']['url']
            new['pr_user_url'] = user_url
            new['pr_user_name'] = self.getUserNameByUrl(user_url)

            new['pr_merged'] = x['merged']
            new['merged_at'] = x['merged_at']
            new['pr_mergedBy_user_id'] = x['merged_by']['id']
            new['pr_mergedBy_user_name'] = x['merged_by']['login']
            new['pr_commits_counts'] = x['commits']
            new['pr_changed_files'] = x['changed_files']
            commits_url = x['commits_url']
            new['commits_url'] = commits_url
            print(commits_url)
            commitData = self.getCommitDataByUrl(commits_url)
            commitDetail = []
            for s in commitData:
                com = {}
                com['commit_author'] = (s['commit'])['author']
                com['commit_committer'] = (s['commit'])['committer']
                com['commit_message'] = (s['commit'])['message']
                commitDetail.append(com)
            new['commitData'] = commitDetail
            pullResList.append(new)

        with open(newPath, "w") as dump_f:
            json.dump(pullResList, dump_f, indent=4)
        print('保存了所有commits数据')


data = DataSet('twbs/bootstrap', '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')
data.getJsonFileCounts('../../resource/vue/pullRequest/mergedAndNotOne.json')
# data.getMergedPR('../../resource/vue/pullRequest/all.json','../../resource/vue/pullRequest/merged.json')
# data.getCommitData('../../resource/vue/pullRequest/mergedAndNotOne.json', '../../resource/vue/pullRequest/commit.json')
