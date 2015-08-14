import time
import github_helper
import slack_helper

class Chappie:

	def __init__(self, name, check_messages_interval, check_pull_requests_interval):
		self.name = name
		self.check_messages_interval = check_messages_interval
		self.check_pull_requests_interval = check_pull_requests_interval
		self.tick_counter = 0

	def start(self):
		slack_helper.connect()
		while True:
			self.tick()

	def tick(self):
		self.tick_counter += self.check_messages_interval
		self.check_messages()

		if self.tick_counter == self.check_pull_requests_interval:
			github_helper.check_repos()

		time.sleep(self.check_messages_interval)

	def check_messages(self):
		for message in slack_helper.client.rtm_read():
			self.process_message(message)

	def process_message(self, message):
		if message.get('type') == slack_helper.EVENT_TYPE_MESSAGE:
			text = message.get('text')
			command = text.replace('<@U09401LGJ>', '')
			command = command[2:] if command[0] == ':' else command[1:]
			if command == text:
				return

			print 'Chappie received a message!'
			self.process_command(command)

	def process_command(self, command):
		print 'Processing command', command
