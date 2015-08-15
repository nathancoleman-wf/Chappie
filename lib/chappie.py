import time
import random
import github_helper
from datetime import datetime
import slack_helper
import utils

class Chappie:

	CMD_IDENTIFY = 'identify'
	MSG_IDENTIFY = 'I am Chappie!'

	CMD_IGNORE = 'ignore'
	MSG_IGNORE = 'If you say so, {0}. Chappie will ignore you for the rest of the day.'
	MSG_PREV_IGNORED = 'Chappie is already ignoring you, {0}. No need to hurt Chappie\'s feelings.\nIf you would like to talk to Chappie again, tell me to \'unignore\'.'

	CMD_UNIGNORE = 'unignore'
	MSG_UNIGNORE = 'Chappie will no longer ignore you, {0}. Chappie loves you, even if no one else does!'

	CMD_SPEAK = 'speak'
	MSG_SPEAK = ["No. I can't shoot people. Chappie no crimes!",
				 "I've got blings?... I've got blings!",
				 "I don't want to die. I want to live.",
				 "You've hurt my people!",
				 "Fuckmother!",
				 "Why did you build me to die maker?",
				 "I'm scared.",
				 "Now we are both black sheep, mommy."]

	def __init__(self, user_object, check_messages_interval, check_pull_requests_interval):
		self.user_object = user_object
		self.check_messages_interval = check_messages_interval
		self.check_pull_requests_interval = check_pull_requests_interval
		self.tick_counter = 0
		self.ignore_list = {}

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
			github_helper.check_repos()

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
			self.process_command(text, message.get(slack_helper.MSG_PROP_USER))

	def is_chappie_command(self, message_text):
		return message_text.startswith('<{0}>'.format(self.user_object.slackidtag))

	def process_command(self, command, slack_id):
		print 'Processing command', command

		if self.CMD_IDENTIFY in command:
			self.identify()

		elif self.CMD_SPEAK in command:
			self.speak()
		
		elif self.CMD_IGNORE in command:
			self.ignore(slack_id)

		elif self.CMD_UNIGNORE in command:
			self.stop_ignoring(slack_id)

	#===================================
	#	Commands
	#===================================

	def identify(self):
		slack_helper.send_message(self.MSG_IDENTIFY)

	def ignore(self, slack_id):
		user = slack_helper.user_from_slack_id(slack_id)
		if not user:
			print 'No user. Ignore failed.'
			return
		if self.ignore_list.get(user.slackname) is not None:
			print 'User already on ignore_list'
			slack_helper.send_message(self.MSG_PREV_IGNORED.format(user.firstname))
			return
		self.ignore_list[user.slackname] = datetime.now()
		print 'Adding {0} to the ignore list'.format(user.slackname)
		slack_helper.send_message(self.MSG_IGNORE.format(user.firstname))

	def stop_ignoring(self, slack_id):
		user = slack_helper.user_from_slack_id(slack_id)
		if not user:
			print 'No user. Unignore gailed.'
			return
		self.ignore_list[user.slackname] = None
		print 'Removing {0} from the ignore list'.format(user.slackname)
		slack_helper.send_message(self.MSG_UNIGNORE.format(user.firstname))

	def speak(self):
		slack_helper.send_message(random.choice(self.MSG_SPEAK))
