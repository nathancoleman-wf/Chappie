### Chappie
This is a Slack bot that uses the GitHub API to notify
team members when their +1 is needed on another team
member's pull request.

##### Getting Started
- Clone this repo
- ```make install```
- Rename ```ex_settings.py``` to ```settings.py```
- Create a channel in Slack for Chappie to post to
- Create a bot integration in [Slack](https://api.slack.com/bot-users) (this will give you a token for the next step)
- Add missing information to ```settings.py``` including your team members and credentials for Slack/GitHub
- ```make run```

##### References
- http://jacquev6.net/PyGithub/v1/reference.html
- https://api.slack.com/

##### Future Work
- Allow Chappie to receive messages from user
    - @Chappie ignore = 24 hours of no tagging
    - @Chappie add user
    - @Chappie private = message privately instead of in channel
    - @Chappie leave = exit the current channel/room
- Give Chappie the ability to handle multiple rooms
- Parse commits in PR until non-master-merge commit is found (currently fails if more than 1 master-merge in a row)
- Use decorators and RegEx matching for response functions
- Build out plugin architecture
