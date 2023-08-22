from redminelib import Redmine
from redminelib import exceptions
import pandas as pd

# RedmineのURLとAPI_KEYの取得
import config
redmine_url = config.redmine_url
api_key = config.api_key

redmine = Redmine(redmine_url, key=api_key)

# ユーザ一覧の読み込み
df_users = pd.read_csv('data/user.csv')

# ユーザごとのプロジェクト一覧を取得
projects_set = set()

for index, row in df_users.iterrows():
    user_id = row['user_id']
    
    try:
        # ユーザが所属しているプロジェクトを取得
        user = redmine.user.get(user_id, include='memberships')
        for membership in user.memberships:
            project = membership.project
            print(project.values_list())
            projects_set.add((project.id, project.name))
    except exceptions.ResourceNotFoundError:
        print(f"ユーザID {user_id} は存在しないか、アクセスできません。")
    except Exception as e:
        print(f"ユーザID {user_id} の処理中にエラーが発生しました: {e}")

# データフレームに変換
df_projects = pd.DataFrame(list(projects_set), columns=['project_id', 'project_name'])

# CSVファイルに保存
df_projects.to_csv('data/top_projects.csv', index=False)

print("トップの親プロジェクト一覧がCSVファイルに保存されました。")
