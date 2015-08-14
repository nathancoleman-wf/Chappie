### Chappie
This is a Slack bot that uses the GitHub API to notify
team members when their +1 is needed on another team
member's pull request.

##### Getting Started
- Clone this repo
- Create a virtual environment for Chappie to run in
- Inside the virtual environment: ```pip install -r requirements.txt```
- Rename ```ex_settings.py``` to ```settings.py```
- Add missing information to ```settings.py``` including your team members and credentials for Slack/GitHub
- ```python main.py```

##### References
- http://jacquev6.net/PyGithub/v1/reference.html
- https://api.slack.com/

##### Future Work
- Allow Chappie to receive messages from user
    - @Chappie ignore = 24 hours of no tagging
    - @Chappie add user
    - @Chappie private = message privately instead of in channel
- Parse commits in PR until non-master-merge commit is found (currently fails if more than 1 master-merge in a row)
