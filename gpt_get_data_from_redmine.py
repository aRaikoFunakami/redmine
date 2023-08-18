import login
from redminelib import Redmine
import pandas as pd
from datetime import datetime
from ast import literal_eval

redmine_url = login.redmine_url
api_key = login.api_key

redmine = Redmine(redmine_url, key=api_key)

start_date = datetime(2022, 8, 1)
end_date = datetime(2023, 7, 31)

# Fetching data from Redmine
issues = redmine.issue.filter(project_id=141, 
                              status_id='*',
                              updated_on="><{0}|{1}".format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

data = []

for issue in issues:
    if hasattr(issue, 'author') and issue.author.id != 1713:
        for journal in issue.journals:
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
