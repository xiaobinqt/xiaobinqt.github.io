import json
import signal
import sys
import time

import requests

site_url = "https://xiaobinqt.github.io"

if len(sys.argv) != 4:
    print("Usage:")
    print(sys.argv[0], "token username repo_name")
    sys.exit()

token = sys.argv[1]
username = sys.argv[2]
repo_name = sys.argv[3]
issue_titles = []  ## issue 的标题
post_complex_titles = []  # 所有文章的标题组合


# print("token: %s ,username: %s repo_name: %s" % (token, username, repo_name))

def quit(signum, frame):
    print('stop ................')
    sys.exit(1)


def get_issues(token, username, repo_name):
    for i in range(1, 150):  # 15000 个 issue 基本够用了
        issues, ret = get_issue(i)
        time.sleep(2)
        if ret == -1:
            break


# 获取所有 label 为 gitalk 的 issue
def get_issue(page=1):
    url = 'https://api.github.com/repos/%s/%s/issues?labels=Gitalk&per_page=100&page=%d' % (username, repo_name, page)
    print("get_issues url: %s" % url)
    r = requests.get(url, headers={
        "Authorization": "token %s" % token,
        "Accept": "application/vnd.github.v3+json"
    })

    if r.json() == []:
        return (issue_titles, -1)

    for issue in r.json():
        if issue['title'] not in issue_titles and issue["title"] != "":
            issue_titles.append(issue['title'])

    return (issue_titles, 0)


# 通过 public/index.json 获取所有的文章
def get_titles():
    with open(file='public/index.json', mode='r', encoding='utf-8') as f:
        file_data = f.read()
        if file_data == "" or file_data == [] or file_data == {}:
            return post_complex_titles

        file_data = json.loads(file_data)
        for data in file_data:
            complex_title = "%s_XXX_%s_XXX_%s" % (data['title'], data['uri'], data['date'])
            if complex_title not in post_complex_titles:
                post_complex_titles.append(complex_title)

    return post_complex_titles


def create_issue(title="", uri="", date=""):
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    if title == "":
        return

    url = 'https://api.github.com/repos/%s/%s/issues' % (username, repo_name)
    print("create_issue title: %s uri: %s date: %s" % (title, uri, date))
    data = {
        'title': title,
        'body': '%s%s' % (site_url, uri),
        'labels': [
            'Gitalk',
            "%sT00:00:00Z" % date
        ]
    }
    print("create_issue req json: %s" % json.dumps(data))
    r = requests.post(url, data=json.dumps(data), headers={
        "Authorization": "token %s" % token,
    }, verify=False)

    if r.status_code == 201:
        print("create_issue success")
    else:
        print("create_issue fail, status_code: %d,title: %s" % r.status_code, title)


# 创建 gitalk 创建 issue,如果 issue 已经存在，则不创建
def init_gitalk():
    for complex_title in post_complex_titles:
        title = complex_title.split("_XXX_")[0]
        uri = complex_title.split("_XXX_")[1]
        date = complex_title.split("_XXX_")[2]
        if title not in issue_titles:
            print("title: %s issue 不存在,创建..." % title)
            create_issue(title, uri, date)
            time.sleep(2)


# def main():
#     # 暂停5分钟，主要是为了等待 vercel 编译新的文章
#     print('sleep 300s for waiting hugo build...')
#     time.sleep(300)
#     session = requests.Session()
#     session.auth = (username, token)
#     session.headers = {
#         'Accept': 'application/vnd.github.v3+json',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30'
#     }
#
#     existing_comments = get_comments(session=session)
#     post_urls = get_posts()
#     not_initialized = list(set(post_urls) ^ set(existing_comments))
#
#     init_gitalk(session=session, not_initialized=not_initialized)
#
#
# main()


if __name__ == "__main__":
    create_issue("禁止Google浏览器强制跳转https", "/stop_chrome_auto_redirect_2_https/", "2022-03-29")
