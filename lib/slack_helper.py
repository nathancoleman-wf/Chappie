from settings import SLACK_ROOM_NAME, SLACK_TOKEN
from slackclient import SlackClient

sc = SlackClient(SLACK_TOKEN)
sc.rtm_connect()

def send_message(message, debug=False):
	if debug:
		print 'Sending message:', message
	sc.rtm_send_message(SLACK_ROOM_NAME, message)
