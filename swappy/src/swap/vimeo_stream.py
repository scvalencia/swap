import cx_Oracle
import time

terms = ['ocaml', 'lisp', 'haskell', 'wall street', 'finances', 'colombia', 
		 'functional programming', 'category theory', 'stock market', 'stock exchange',
		 'stanford', 'python', 'scala', 'logic programming']

was_actioned = False
videos_ids = []

CONSUMER_KEY = "c1f5add1d34817a6775d10b3f6821268"	
OAUTH_NONCE = "ee88b5bd5b8c1f65334f39d354642bce"
OAUTH_SIGNATURE = "HMAC-SHA1"
OAUTH_VERSION = "1.0"

class VimeoHelper(object):
	
	def __init__(self, consumer_key, oauth_key, crypto, api_version):
		self.consumer_key = consumer_key
		self.nonce = oauth_key		
		self.signature_method = crypto
		self.version = api_version
		self.base = ''		

	def generate_base(self):
		self.base += "GET&http%3A%2F%2Fvimeo.com%2Fapi%2Frest%2Fv2&format%3D"
		self.base += "json%26method%3Dvimeo.videos.search%26oauth_consumer_key%3D"
		self.base += self.consumer_key + "%26oauth_nonce%3D"
		self.base += self.nonce + "%26oauth_signature_method"
		self.base += "%3D" + self.signature_method + "%26oauth_timestamp%3D"

	def process_query(self, query):
		query = query.split()
		query_base = "%26query%3D" + "%2520".join(query)
		return (self.version + query_base)

	def generate_solicitude(self, query):
		self.generate_base()
		timestamp = str(int(time.time()))
		self.base += timestamp + "%26oauth_version%3D" + self.process_query(query)


class Video(object):
	pass
	# TODO


class DBVideoHelper(object):
	CONSUMER_KEY = "c1f5add1d34817a6775d10b3f6821268"	
	OAUTH_NONCE = "ee88b5bd5b8c1f65334f39d354642bce"
	OAUTH_SIGNATURE = "HMAC-SHA1"
	OAUTH_VERSION = "1.0"

	def __init__(self, db_username, db_password, server, port, sid, production):
		self.dsn_tns = cx_Oracle.makedsn(server, port, sid)
		self.production = production
		self.connection = None
		self.cursor = None
		self.vimeo = VimeoHelper(self.CONSUMER_KEY, self.OAUTH_NONCE, 
			self.OAUTH_SIGNATURE, self.OAUTH_VERSION)
		try:
			self.connection = cx_Oracle.connect(db_username, db_password, self.dsn_tns)
			try:
				self.cursor = self.connection.cursor()
				# PROCESS					
			finally:
				self.cursor.close()
		finally:
			if self.connection is not None:
				if self.production:
					self.connection.commit()
				self.connection.close()

	def create_table(self):
		query = ("CREATE TABLE VIDEO")

	def retrieve_videos(self):
		pass
		#TODO

	def 


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

vimeo = VimeoHelper(CONSUMER_KEY, OAUTH_NONCE, OAUTH_SIGNATURE, OAUTH_VERSION)
vimeo.generate_solicitude("logic programming")
#vimeo.generate_solicitude()
print vimeo.base