from lib import github_helper
from lib import slack_helper
from settings import REPOS, USERS

repos = github_helper.get_repos(REPOS)
for githubname in repos:
	for repo in repos.get(githubname):
		open_pulls = repo.get_pulls(state=github_helper.PR_STATE_OPEN)
		github_helper.check_pulls(open_pulls)
github_helper.process_pending_notifications()
