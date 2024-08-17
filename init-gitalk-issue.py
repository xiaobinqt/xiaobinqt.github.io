import hashlib
import json
import sys
import time

import requests
from algoliasearch.search.client import SearchClient

site_url = "https://xiaobinqt.github.io"

if len(sys.argv) != 6:
    print("Usage:")
    print(sys.argv[0], "token username repo_name aligolia_app_id aligolia_admin_api_key")
    sys.exit(1)

# issue 的 body 就是文章的 URL

token = sys.argv[1]
username = sys.argv[2]
repo_name = sys.argv[3]
algolia_app_id = sys.argv[4]
algolia_admin_api_key = sys.argv[5]
issue_map = dict()  ## [issue_body] = {"issue_number": issue_number, "issue_title": issue_title}
posts_map = dict()  # [post_url] = {"post_uri":uri,"post_date":date,"post_title":title}


def get_all_gitalk_issues(token, username, repo_name):
    for i in range(1, 150):  # 15000 个 issue 基本够用了,不够可以再加
        _, ret = get_issues_page(i)
        time.sleep(5)
        if ret == -1:
            break


## 删除的文章不管....
## 文章 title 修改了的文章该怎么处理？ 标题可能修改,但是 uri 不变,issue 的 body 是文章地址,只要文章地址不变，就可以直接 update issue title
## uri 如果也变了，相当于是文件的重命名了，这时只能去手动 update issue title 了?.....
def update_issue(issue_number, title):
    if title == "":
        return

    url = 'https://api.github.com/repos/%s/%s/issues/%d' % (username, repo_name, issue_number)
    print("update_issue url: %s" % url)
    data = {
        'title': title,
    }
    print("create_issue req json: %s" % json.dumps(data))
    r = requests.patch(url, data=json.dumps(data), headers={
        "Authorization": "token %s" % token,
    }, verify=False)

    if r.status_code == 200:
        print("update_issue success")
    else:
        print("update_issue fail, status_code: %d,title: %s,issue_number: %d" %
              (r.status_code, title, issue_number))


# 获取所有 label 为 gitalk 的 issue
def get_issues_page(page=1):
    url = 'https://api.github.com/repos/%s/%s/issues?labels=Gitalk&per_page=100&page=%d' % (username, repo_name, page)
    print("get_issues url: %s" % url)
    r = requests.get(url, headers={
        "Authorization": "token %s" % token,
        "Accept": "application/vnd.github.v3+json"
    })

    if r.status_code != 200:
        print("get_issues_page fail, status_code: %d" % r.status_code)
        sys.exit(2)

    if r.json() == []:
        return (issue_map, -1)

    for issue in r.json():
        if issue['body'] not in issue_map and issue["body"] != "":
            issue_map[issue['body']] = {
                "issue_number": issue['number'],
                "issue_title": issue['title']
            }

    return (issue_map, 0)


# 通过 public/index.json 获取所有的文章
def get_post_titles():
    with open(file='public/index.json', mode='r', encoding='utf-8') as f:
        file_data = f.read()
        if file_data == "" or file_data == [] or file_data == {}:
            return posts_map

        file_data = json.loads(file_data)
        for data in file_data:
            origin_uri = data['uri']
            if origin_uri == "":
                continue
            x = origin_uri.split('#')
            if len(x) < 1:
                continue
            uri = x[0]
            if uri == "":
                continue

            key = "%s%s" % (site_url, uri)
            if key not in posts_map:
                posts_map[key] = {
                    "post_uri": uri,
                    "post_date": data['date'],
                    "post_title": data['title']
                }

    return posts_map


def create_issue(title="", uri="", date=""):
    if title == "":
        return

    url = 'https://api.github.com/repos/%s/%s/issues' % (username, repo_name)
    print("create_issue title: %s uri: %s date: %s" % (title, uri, date))
    m = hashlib.md5()
    m.update(uri.encode('utf-8'))
    urlmd5 = m.hexdigest()
    data = {
        'title': title,
        'body': '%s%s' % (site_url, uri),
        'labels': [
            'Gitalk',
            urlmd5
        ]
    }
    print("create_issue req json: %s" % json.dumps(data))
    r = requests.post(url, data=json.dumps(data), headers={
        "Authorization": "token %s" % token,
    })

    if r.status_code == 201:
        print("create_issue success")
    else:
        print("create_issue fail, status_code: %d,title: %s,req url: %s \n" % (r.status_code, title, url))


# 创建 gitalk 创建 issue,如果 issue 已经存在，则不创建
def init_gitalk():
    for post_url, item in posts_map.items():
        ## 标题被修改了
        if post_url in issue_map and item['post_title'] != issue_map[post_url]['issue_title']:
            update_issue(issue_map[post_url]["issue_number"], item['post_title'])
        elif post_url not in issue_map:  # 新增的文章
            print("title: [%s] , body [%s] issue 不存在,创建..." % (item["post_title"], post_url))
            create_issue(item["post_title"], item["post_uri"], item["post_date"])
            # 延迟 5 秒，防止 github api 请求过于频繁： https://docs.github.com/en/rest/guides/best-practices-for-integrators#dealing-with-secondary-rate-limits
            time.sleep(5)


def get_uri_md5(uri):
    m = hashlib.md5()
    m.update(uri.encode('utf-8'))
    return m.hexdigest()


# algolia 删除索引
def delete_index():
    client = SearchClient.create(algolia_app_id, algolia_admin_api_key)
    index = client.init_index('xiaobinqt.io')
    index.delete()
    print("algolia delete_index success")


if __name__ == "__main__":
    # print(get_uri_md5("/new-make-difference/"))
    ## 执行....
    delete_index()
    get_all_gitalk_issues(token, username, repo_name)
    get_post_titles()
    init_gitalk()
