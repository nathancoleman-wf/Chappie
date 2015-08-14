from collections import defaultdict
from github import Github
from github import PullRequest
from settings import GITHUB_USERNAME, GITHUB_PASSWORD, REPOS, USERS
from slack_helper import send_message

PR_STATE_OPEN = 'open'
PR_STATE_CLOSED = 'closed'
PR_STATE_ALL = 'all'

g = Github(GITHUB_USERNAME, GITHUB_PASSWORD)
pending_notifications = set()


def check_repos():
	repos = get_repos(REPOS)
	for githubname in repos:
		for repo in repos.get(githubname):
			open_pulls = repo.get_pulls(state=PR_STATE_OPEN)
			check_pulls(open_pulls)
	process_pending_notifications()


def get_repos(repo_names):
	""" Get each repo in repo_names for each user in settings.USERS
	
	Return: {"github_username": [github.Repository.Repository]}
	"""

	repos = defaultdict(list)
	for user in USERS:
		for repo_name in repo_names:
			repo = g.get_user(user.githubname).get_repo(repo_name)
			if not repo:
				print 'Failed to retrieve {0}:{1}'.format(user.githubname, repo_name)
				continue
			repos[user.githubname].append(repo)
	return repos


def check_pulls(pull_requests):
	""" Check each pull in pull_requests to verify that it has 3 +1s
	after the latest commit. If not, add a pending Slack notification.
	"""

	for pull_request in pull_requests:
		if not isinstance(pull_request, PullRequest.PullRequest):
			print 'Incorrect type found for pull_request'
			return
		print '============================================================================'
		print pull_request.title
		print '============================================================================'
		print pull_request.html_url
		print # Empty line
		plus_ones = 0
		plus_oners = []
		comments = _get_latest_commit_comments(pull_request)
		for comment in comments:
			if '+1' in comment.body:
				plus_ones += 1
				plus_oners.append(comment.user.login)
		addition = (' by ' + ', '.join(plus_oners)) if plus_ones else ''
		print 'Pull request has {0} +1s{1}'.format(plus_ones, addition)
		if plus_ones < 3:
			do_not_notify = list(set([commit.author.login for commit in pull_request.get_commits()]))
			do_not_notify = do_not_notify + plus_oners
			_add_pending_notification(pull_request, (3 - plus_ones), do_not_notify)
		print # Empty line


def process_pending_notifications():
	""" Consolidate global pending_notifications list and separate by
	========================. Send consolidate message to Slack room.
	"""

	global pending_notifications
	grouped_notification = '\n\n============================\n\n'.join(pending_notifications)
	pending_notifications = set()
	print 'Processing pending notifications:'
	print # Empty line
	print grouped_notification
	send_message(grouped_notification)


def _get_latest_commit_comments(pull_request):
	""" Get the latest commit from pull_request and return comments
	that have occurred since.
	"""

	pull_commits = pull_request.get_commits().reversed
	latest_commit = None
	for commit in pull_commits:
		if not _is_master_merge_commit(pull_request.base.sha, commit):
			latest_commit = commit
			break
		else:
			print commit.sha, 'is master merge. Moving on.'
	if not latest_commit:
		print 'No non-master-merge commits found'
		return
	print 'Latest commit:'
	print '\tSHA:', latest_commit.sha
	print '\tCreated:', latest_commit.commit.author.date
	print '\tMessage:'
	print '\t########################################'
	print '\t', latest_commit.commit.message.replace('\n', '\n\t')
	print '\t########################################'
	print # Empty line
	comments = [comment for comment in pull_request.get_issue_comments() if comment.created_at > latest_commit.commit.author.date]
	print 'Found {0} comments for latest commit, {1}'.format(len(comments), latest_commit.sha)
	for comment in comments:
		print '\tID:', comment.id
		print '\tCreated:', comment.created_at
		print '\tUpdated:', comment.updated_at
		print '\tBody:'
		print '\t########################################'
		print '\t', comment.body.replace('\n', '\n\t')
		print '\t########################################'
		print # Empty line
	return comments


def _add_pending_notification(pull_request, required_plus_ones, do_not_notify):
	""" Add a message to the global pending_notifications list
	of the format:

	Pull Title
	Pull URL
	Needs (X) +1s
	Attn: @users who haven't +1d
	"""

	global pending_notifications
	do_notify = [user.slacktag for user in USERS if user.githubname not in do_not_notify]
	print 'Adding pending slack notification to', ', '.join(do_notify)
	title = pull_request.title
	url = pull_request.html_url
	message = '{0}\n{1}\nNeeds {2} +1s\nAttn: {3}'.format(title, url, required_plus_ones, ', '.join([slacktag for slacktag in do_notify]))
	print # Empty line
	pending_notifications.add(message)

def _is_master_merge_commit(base_sha, commit):
	is_merge_commit = len(commit.parents) > 1
	if not is_merge_commit:
		return False
	parent_shas = [c.sha for c in commit.parents]
	return base_sha in parent_shas
