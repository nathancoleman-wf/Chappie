from lib import User

USERS = [User('Chappie', 'chappie', ''), # Leave this line. Chappie must be the first user
		 User('Real Name', 'slack username', 'github username')]
REPOS = ['repository', 'names']

# Slack Settings
SLACK_TOKEN = 'token'
SLACK_ROOM_NAME = 'room name for notifications'
CHECK_MESSAGES_INTERVAL = 1

# GitHub Settings
GITHUB_USERNAME = 'github username'
GITHUB_PASSWORD = 'github password'
CHECK_PULL_REQUESTS_INTERVAL = 3000
