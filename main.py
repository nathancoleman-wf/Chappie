from lib import github_helper
from lib import slack_helper
from settings import USERS

repos = github_helper.get_repos(['bigsky'])
for githubname in repos:
	for repo in repos.get(githubname):
		print 'Retrieving open pull requests for {0}:{1}'.format(githubname, repo.name)
		open_pulls = repo.get_pulls(state=github_helper.PR_STATE_OPEN)
		github_helper.check_pulls(open_pulls)
