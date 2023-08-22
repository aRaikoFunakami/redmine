from redminelib import Redmine

# RedmineのURLとAPI_KEYの取得
import config
redmine_url = config.redmine_url
api_key = config.api_key

# Redmineとの接続
redmine = Redmine(redmine_url, key=api_key)

ISSUE_ID = 264265

def get_issue_journal(issue_id):
    issue = redmine.issue.get(issue_id, include='journals')
    
    if not hasattr(issue, 'journals'):
        print(f"Issue {issue_id} has no journals.")
        return

    for journal in issue.journals:
        print(f"Updated on: {journal.created_on}")
        if hasattr(journal, 'notes'):
            print(f"Notes: {journal.notes}")
        for detail in journal.details:
            print(detail)  # この行でdetailの内容を単純に出力
        print("-" * 50)

if __name__ == "__main__":
    get_issue_journal(ISSUE_ID)
