from redminelib import Redmine
import pandas as pd
import config
import csv

# Redmineの設定
redmine_url = config.redmine_url
api_key = config.api_key
redmine = Redmine(redmine_url, key=api_key)

# 対象となるプロジェクトID
target_projects = {
    141: "NFB{NX,BE}",
    1833: "WebPlatformQMS(WPQMS)",
    268: "WebPlatformDev1",
    1679: "WebPlatformDev4(WP4)",
    1719: "WebPlatformDev4-OJT",
    1447: "Webプラットフォーム事業部開発部2課",
    629: "1seg/12seg BML",
    1757: "WOVEN案件",
}

# プロジェクトとその子プロジェクトのIDを格納するセット
all_project_ids = set()

# 各プロジェクトでIssueを取得し、関連するプロジェクトIDを収集
for project_id in target_projects.keys():
    issues = redmine.issue.filter(project_id=project_id)
    for issue in issues:
        all_project_ids.add(issue.project.id)

# 空のDataFrameを作成
df = pd.DataFrame(columns=['project_id'])

# 収集したプロジェクトIDをDataFrameに追加
for project_id in all_project_ids:
    new_row = pd.DataFrame({'project_id': [project_id]})
    df = pd.concat([df, new_row], ignore_index=True)

# CSVに保存
df.to_csv('project_ids.csv', index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
