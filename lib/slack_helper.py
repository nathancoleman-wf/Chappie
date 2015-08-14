from settings import SLACK_ROOM_NAME, SLACK_TOKEN
from slackclient import SlackClient

EVENT_TYPE_MESSAGE = 'message'
EVENT_PROP_TEXT = 'text'

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
