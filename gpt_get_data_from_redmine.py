import config
from redminelib import Redmine
import pandas as pd
from datetime import datetime
from ast import literal_eval

redmine_url = config.redmine_url
api_key = config.api_key

redmine = Redmine(redmine_url, key=api_key)

start_date = config.start_date
end_date = config.end_date

# Fetching data from Redmine
# updated_on は最後の日時になるため start は指定できるが end は指定してはいけない
issues = redmine.issue.filter(project_id='*', 
                              status_id='*',
                              updated_on=">={0}".format(start_date.strftime('%Y-%m-%d')))

data = []

for issue in issues:
    if hasattr(issue, 'author'):
        for journal in issue.journals:
            if journal.user.id in config.exclude_author_ids:
                print(f"skip exclude_author_ids: {journal.user.id}")
                continue
            if hasattr(journal, 'notes') and journal.created_on >= start_date and journal.created_on <= end_date:
                try:
                    comment_length = len(journal.notes) if hasattr(journal, 'notes') and journal.notes is not None else 0
                    comment_date = journal.created_on
                except AttributeError:
                    comment_length = 0
                    comment_date = None
                
                data.append({
                    'issue_id': issue.id,
                    'user_id': journal.user.id,
                    'issue_description_length': len(issue.description) if hasattr(issue, 'description') and issue.description is not None else 0,
                    'comment_length': comment_length,
                    'comment_date': comment_date
                })

df = pd.DataFrame(data)
df.to_csv("data/step1_data.csv", index=False)

print("Data saved successfully!")
