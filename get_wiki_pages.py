from redminelib import Redmine
import redminelib.exceptions
import pandas as pd
from datetime import datetime
import config
import csv
import re  # 正規表現ライブラリ

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

# get_projects.py でプロジェクトIDを作成する
# CSVからプロジェクトIDを読み込む
df_project_ids = pd.read_csv('project_ids.csv')
all_project_ids = df_project_ids['project_id'].tolist()

# 空のDataFrameを作成
df = pd.DataFrame(columns=['id', 'subject', 'journals', 'project_id', 'project_name'])

# 文字列をクリーニングする関数
def clean_text(text):
    if text is None:
        return ""
    text = text.strip()
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

# 収集した全てのプロジェクトIDで処理
for project_id in all_project_ids:
    project = redmine.project.get(project_id)
    
    try:
        wiki_pages = redmine.wiki_page.filter(project_id=project_id)
        if wiki_pages is None:
            break
        
        for page in wiki_pages:
            new_row = pd.DataFrame({
                'id':  [project.identifier],
                'subject': [page.title],
                'journals': [clean_text(page.text)],
                'project_id': [project_id],
                'project_name': [project.name],
            })
            
            df = pd.concat([df, new_row], ignore_index=True)
    except redminelib.exceptions.ForbiddenError:
        print(f"Permission denied for project_id {project_id}, {project.identifier}, {project.name}. Skipping.")
    except Exception as e:
        print(f"An unexpected error occurred for project_id {project_id}, {project.identifier}, {project.name}: {e}. Skipping.")

# ファイル名の生成
file_name = f"./issues/issues{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# CSVに保存
df.to_csv(file_name, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')
