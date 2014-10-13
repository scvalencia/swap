import time

terms = ['ocaml', 'lisp', 'haskell', 'wall street', 'finances', 'colombia', 
		 'functional programming', 'category theory', 'stock market', 'stock exchange',
		 'stanford', 'python', 'scala', 'logic programming']

was_actioned = False
videos_ids = []

class VimeoHelper(object):
	
	def __init__(self, consumer_key, oauth_key, crypto, api_version, query):
		self.consumer_key = consumer_key
		self.nonce = oauth_key		
		self.signature_method = crypto
		self.version = api_version
		self.query = query.split()
		self.base = ''		

	def generate_base(self):
		self.base += "GET&http%3A%2F%2Fvimeo.com%2Fapi%2Frest%2Fv2&format%3D"
		self.base += "json%26method%3Dvimeo.videos.search%26oauth_consumer_key%3D"
		self.base += self.consumer_key + "%26oauth_nonce%3D"
		self.base += self.nonce + "%26oauth_signature_method"
		self.base += "%3D" + self.signature_method + "%26oauth_timestamp%3D"

		#base += "1413237330%26oauth_version%3D"
		#base += self.version + "%26query%3Dlogic%2520programming"

		return base

	def process_query(self):
		


	def generate_solicitude(self):
		timestamp = int(time.time())
		print timestamp

class DBVideoHelper(object):
	CONSUMER_KEY = "c1f5add1d34817a6775d10b3f6821268"	
	OAUTH_NONCE = "ee88b5bd5b8c1f65334f39d354642bce"
	OAUTH_SIGNATURE = "HMAC-SHA1"
	OAUTH_VERSION = "1.0"

	def __init__(self, db_username, db_password):




def set_videos():
	global was_actioned
	was_actioned = True

def get_videos():
	global videos_ids
	if was_actioned:
		return videos_ids
	else:
		set_videos()



CONSUMER_SIGNATURE = "HM0Mgax7ny8W3PBEHzYl0rmTB0E%3D"

vimeo = VimeoHelper()
#vimeo.generate_solicitude()
print vimeo.generate_base()