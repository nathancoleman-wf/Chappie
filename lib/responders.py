import random
import slack_helper

responders = {}


MSG_IDENTIFY = 'I am Chappie!'
def identify_responder(slack_id, channel):
	slack_helper.client.rtm_send_message(channel, MSG_IDENTIFY)
responders['identify'] = identify_responder


MSG_UNKNOWN = 'Chappie doesn\'t know that command, {0}.\nTell Chappie to \'help\' if you would like help.'
def unknown_responder(slack_id, channel):
	user = slack_helper.user_from_slack_id(slack_id)
	if not user:
		print 'No user'
		return
	slack_helper.client.rtm_send_message(channel, MSG_UNKNOWN.format(user.firstname))
responders['unknown'] = unknown_responder


MSG_SPEAK = ["No. I can't shoot people. Chappie no crimes!",
			 "I've got blings?... I've got blings!",
			 "I don't want to die. I want to live.",
			 "You've hurt my people!",
			 "Fuckmother!",
			 "Why did you build me to die maker?",
			 "I'm scared.",
			 "Now we are both black sheep, mommy."]
def speak_responder(slack_id, channel):
	slack_helper.client.rtm_send_message(channel, random.choice(MSG_SPEAK))
responders['speak'] = speak_responder


MSG_IGNORE = 'If you say so, {0}. Chappie will ignore you for the rest of the day.'
MSG_PREV_IGNORED = 'Chappie is already ignoring you, {0}. No need to hurt Chappie\'s feelings.\nIf you would like to talk to Chappie again, tell me to \'unignore\'.'
def ignore_responder(slack_id, channel):
	user = slack_helper.user_from_slack_id(slack_id)
	if not user:
		print 'No user. Ignore failed.'
		return
	# if self.ignore_list.get(user.slackname) is not None:
	# 	print 'User already on ignore_list'
	# 	slack_helper.client.rtm_send_message(channel, self.MSG_PREV_IGNORED.format(user.firstname))
	# 	return
	# self.ignore_list[user.slackname] = datetime.now()
	print 'Adding {0} to the ignore list'.format(user.slackname)
	slack_helper.client.rtm_send_message(channel, MSG_IGNORE.format(user.firstname))
responders['ignore'] = ignore_responder


MSG_UNIGNORE = 'Chappie will no longer ignore you, {0}. Chappie loves you, even if no one else does!'
def unignore_responder(slack_id, channel):
	user = slack_helper.user_from_slack_id(slack_id)
	if not user:
		print 'No user. Unignore gailed.'
		return
	# self.ignore_list[user.slackname] = None
	print 'Removing {0} from the ignore list'.format(user.slackname)
	slack_helper.client.rtm_send_message(channel, MSG_UNIGNORE.format(user.firstname))
responders['unignore'] = unignore_responder


def help_responder(slack_id, channel):
	slack_helper.client.rtm_send_message(channel, '\n'.join(responders.keys()))
responders['help'] = help_responder
