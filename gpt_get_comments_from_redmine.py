import config
import datetime
import os
import pandas as pd
from redminelib import Redmine

# Redmineの設定
redmine_url = config.redmine_url
api_key = config.api_key
redmine = Redmine(redmine_url, key=api_key)

# パラメータ
PROJECT_ID = 141
START_DATE = '2023-07-01'
END_DATE = '2023-07-31'
USER_ID = 1810

# 日付の変換
START_DATE = datetime.datetime.strptime(START_DATE, '%Y-%m-%d').date()
END_DATE = datetime.datetime.strptime(END_DATE, '%Y-%m-%d').date()

def fetch_data():
    # 期間内に作成されたイシューの取得
    print("Fetching issues created within the specified period...")
    created_issues = redmine.issue.filter(project_id=PROJECT_ID, created_on=f"><{START_DATE}|{END_DATE}")

    # 期間開始以降に更新されたイシューの取得
    print("Fetching issues updated after the start date...")
    updated_issues = redmine.issue.filter(project_id=PROJECT_ID, updated_on=f">={START_DATE}")

    issues_data = [{
		'id': issue.id,
		'subject': issue.subject,
		'description': issue.description,
		'created_on': issue.created_on,
		'author_id': issue.author.id  # この行を追加
	} for issue in created_issues]
    
    print("Fetching journals...")
    journals_data = []
    for issue in updated_issues:
        for journal in issue.journals:
            if hasattr(journal, 'notes') and journal.notes and START_DATE <= journal.created_on.date() <= END_DATE:
                journals_data.append({
                    'issue_id': issue.id,
                    'author_id': journal.user.id,
                    'notes': journal.notes,
                    'created_on': journal.created_on
                })

    # Save to CSV
    issues_df = pd.DataFrame(issues_data)
    journals_df = pd.DataFrame(journals_data)
    issues_df.to_csv(f"data/db_{PROJECT_ID}_issues.csv", index=False)
    journals_df.to_csv(f"data/db_{PROJECT_ID}_comments.csv", index=False)

def filter_by_user():
    print("Filtering by user...")
    issues_df = pd.read_csv(f"data/db_{PROJECT_ID}_issues.csv")
    comments_df = pd.read_csv(f"data/db_{PROJECT_ID}_comments.csv")

    user_issues_df = issues_df[issues_df['author_id'] == USER_ID]
    user_comments_df = comments_df[comments_df['author_id'] == USER_ID]

    user_issues_df.to_csv(f"data/db_{PROJECT_ID}_issues_{USER_ID}.csv", index=False)
    user_comments_df.to_csv(f"data/db_{PROJECT_ID}_comments_{USER_ID}.csv", index=False)

if __name__ == "__main__":
    fetch_data()
    filter_by_user()
    print("Process completed!")
