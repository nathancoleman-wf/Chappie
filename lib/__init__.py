class User:
	def __init__(self, name, slack_username, github_username):
		self.name = name
		self.slack_username = slack_username
		self.github_username = github_username

	@property
	def firstname(self):
		namesplit = self.name.split(' ')
		return namesplit[0] if len(namesplit) else None

	@property
	def lastname(self):
		namesplit = self.name.split(' ')
		return namesplit[1] if len(namesplit) > 1 else None

	@property
	def githubname(self):
		return self.github_username

	@property
	def githubtag(self):
		return '@' + self.github_username

	@property
	def slackname(self):
		return self.slack_username

	@property
	def slacktag(self):
		return '@' + self.slack_username
