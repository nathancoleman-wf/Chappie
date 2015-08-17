from settings import SLACK_ROOM_NAME, SLACK_TOKEN, USERS
from slackclient import SlackClient

EVENT_PROP_TYPE = 'type'
EVENT_TYPE_MESSAGE = 'message'
MSG_PROP_CHANNEL = 'channel'
MSG_PROP_TEXT = 'text'
MSG_PROP_USER = 'user'

client = None


def connect():
	global client
	client = SlackClient(SLACK_TOKEN)
	client.rtm_connect()


def send_message(message, debug=False):
	global client
	if debug:
		print 'Sending message:', message
	client.rtm_send_message(SLACK_ROOM_NAME, message)


def user_from_slack_id(slack_id):
	print 'Attempting to fetch user with slack_id', slack_id
	# Have we cached this user's slack_id already?
	local_matches = [user for user in USERS if user.slack_id == slack_id]
	if local_matches:
		print slack_id, 'cached already. Returning...'
		return local_matches[0]
	
	# If not, find match on the slack server and cache slack_id
	print 'Searching the slack server for', slack_id
	match = client.server.users.find(slack_id)
	local_matches = [user for user in USERS if user.slackname == match.name]
	if not local_matches:
		print slack_id, 'does not belong to any known team members'
		return
	print 'Found match. Caching for', local_matches[0].slackname
	local_matches[0].slack_id = match.id
	return local_matches[0]


def cache_slack_id(user):
	print 'Attempting to cache slack_id for', user.slackname
	matches = [u for u in client.server.users if u.name == user.slackname]
	if not matches:
		print 'No match found for', user.slackname
		return None
	match = matches[0]
	print 'Found match. ID is {0}. Caching...'.format(match.id)
	user.slack_id = match.id


def user_from_slacktag(slacktag):
	print 'Attempting to fetch user with slacktag', slacktag
	matches = [user for user in USERS if user.slacktag == slacktag]
	if not matches:
		print 'No matches found for', slacktag
		return None
	elif len(matches) > 1:
		print 'Multiple matches found for {0}. Returning 1st'.format(slacktag)
	else:
		print 'User found'
	return matches[0]
