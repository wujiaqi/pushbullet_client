import requests
import logging
import logging.handlers
import json
import sys

from requests.auth import AuthBase

PB_API = "https://api.pushbullet.com"

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
_logger.addHandler(consoleHandler)


class PBAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = "Bearer " + self.token
        return r

class PBUnauthorizedException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def push_note_to_channel(channel_tag, title, message, token):
	params = {
		"channel_tag": channel_tag,
		"type": "note",
		"title": title,
		"body": message,
	}
	r = requests.post(PB_API + "/v2/pushes", data = params, auth = PBAuth(token))
	if r.status_code == requests.codes.unauthorized:
		_logger.error("Request unauthorized. Token invalid")
		raise PBUnauthorizedException("Invalid Pushbullet access token")
	elif r.status_code != requests.codes.ok:
		_logger.error("Error occured making request to " + PB_API + "/v2/pushes. Status code: " + r.status_code)
		raise Exception("Request Failed with status code " + r.status_code)
	_logger.info("Message pushed to channel " + channel_tag)
	_logger.debug("\nMessage Contents\n\ttitle: " + title + "\n\tmessage: " + message)

#returns object representing JSON return value of GET channel-info
def get_channel_info(channel_tag, token):
	query_params = {
		"tag": channel_tag,
	}
	r = requests.get(PB_API + "/v2/channel-info", params=query_params, auth = PBAuth(token))
	if r.status_code == requests.codes.unauthorized:
		_logger.error("Request unauthorized. Token invalid")
		raise PBUnauthorizedException("Invalid Pushbullet access token")
	elif r.status_code != requests.codes.ok:
		_logger.error("Error occured making request to " + PB_API + "/v2/channel-info. Status code: " + r.status_code)
		raise Exception("Request Failed with status code " + r.status_code)
	_logger.info("Latest pulled from channel " + channel_tag)
	response_body = r.text
	channel_info = json.loads(unicode(response_body))
	_logger.debug("Received contents from channel " + channel_tag + ":\n" + response_body)
	return channel_info

