import pandas as pd
from redminelib import Redmine
import config

# Redmineサーバーへの接続設定
redmine_url = config.redmine_url
api_key = config.api_key

redmine = Redmine(redmine_url, key=api_key)

# プロジェクトID 141に所属するユーザ情報を取得
memberships = redmine.project_membership.filter(project_id=141)

# ユーザ情報をデータフレームに格納
user_data = []
for membership in memberships:
    if hasattr(membership, 'user'):
        user_id = membership.user.id
        user_name = membership.user.name
        user_data.append({
            'user_id': user_id,
            'user_name': user_name
        })

df = pd.DataFrame(user_data)

# データフレームをCSVファイルに保存
df.to_csv("data/user.csv", index=False)
