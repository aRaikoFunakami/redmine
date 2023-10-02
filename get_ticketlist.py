from redminelib import Redmine
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

# 空のDataFrameを作成
df = pd.DataFrame(columns=['id', 'subject', 'journals', 'project_id', 'project_name'])

# 対象期間
start_date = '2000-09-20'
end_date = '2023-09-20'

# 文字列をクリーニングする関数
def clean_text(text):
    if text is None:
        return ""
    text = text.strip()  # 空白の削除
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)  # ASCII制御文字の削除
    return text


# 各プロジェクトに対して処理
for project_id, project_name in target_projects.items():
    print(f"project_id {project_id}")
    issues = redmine.issue.filter(project_id=project_id, created_on=f'><{start_date}|{end_date}')
    
    for issue in issues:
        journals = '; '.join([clean_text(str(journal.notes)) for journal in issue.journals])
        description = clean_text(issue.description)
        journals = f"{description}; {journals}"  # description を journals の一部として扱う
        new_row = pd.DataFrame({
            'id': [issue.id],
            'subject': [clean_text(issue.subject)],
            'journals': [journals],
            'project_id': [project_id],
            'project_name': [clean_text(project_name)]
        })
        df = pd.concat([df, new_row], ignore_index=True)

# ファイル名の生成
file_name = f"./issues/issues{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# CSVに保存
df.to_csv(file_name, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, escapechar='\\')
