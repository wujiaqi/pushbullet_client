import requests

from requests.auth import AuthBase

PB_API = "https://api.pushbullet.com"

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

def push_to_channel(channel_tag, title, message, token):
	params = {
		"channel_tag": channel_tag,
		"type": "note",
		"title": title,
		"body": message,
	}
	r = requests.post(PB_API + "/v2/pushes", data = params, auth = PBAuth(token))
	if r.status_code == requests.codes.unauthorized:
		raise PBUnauthorizedException("Invalid token")
	elif r.status_code != requests.codes.ok:
		raise Exception
    
