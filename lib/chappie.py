import time
import random
import github_helper
from datetime import datetime
from responders import responders
import slack_helper


class Chappie:

	def __init__(self, user_object, check_messages_interval, check_pull_requests_interval):
		self.user_object = user_object
		self.check_messages_interval = check_messages_interval
		self.check_pull_requests_interval = check_pull_requests_interval
		self.tick_counter = 0
		self.ignore_list = {}
		self.latest_exception = None

	@property
	def name(self):
		return self.user_object.name

	def start(self):
		slack_helper.connect()
		slack_helper.cache_slack_id(self.user_object)
		while True:
			self.tick()

	def tick(self):
		self.tick_counter += self.check_messages_interval
		self.check_messages()

		if self.tick_counter == self.check_pull_requests_interval:
			try:
				github_helper.check_repos()
			except:
				pass

		time.sleep(self.check_messages_interval)

	#===================================
	#	Message processing
	#===================================

	def check_messages(self):
		for message in slack_helper.client.rtm_read():
			self.process_message(message)

	def process_message(self, message):
		if message.get(slack_helper.EVENT_PROP_TYPE) == slack_helper.EVENT_TYPE_MESSAGE:
			text = message.get(slack_helper.MSG_PROP_TEXT)
			if not text or not self.is_chappie_command(text):
				return
			print 'Chappie received a message!'
			command = text[text.find(' '):].lower()
			sender_slack_id = message.get(slack_helper.MSG_PROP_USER)
			channel = message.get(slack_helper.MSG_PROP_CHANNEL)
			try:
				self.process_command(text, sender_slack_id, channel)
			except Exception, e:
				print 'Encountered exception:\n\t', e
				slack_helper.client.rtm_send_message(channel, 'Chappie encountered an error.')
				self.latest_exception = e

	def is_chappie_command(self, message_text):
		return message_text.startswith('<{0}>'.format(self.user_object.slackidtag))

	def process_command(self, command, slack_id, channel):
		print 'Processing command {0} in channel {1}'.format(command, channel)

		default_responder = responders.get('unknown')
		for identifier, responder in responders.iteritems():
			if identifier in command:
				responder(slack_id, channel)
				return
		default_responder(slack_id, channel)
