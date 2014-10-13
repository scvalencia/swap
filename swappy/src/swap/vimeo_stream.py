was_actioned = False
videos = []

def set_videos():
	global was_actioned
	was_actioned = True

def get_videos():
	global videos
	if was_actioned:
		return videos
	else:
		set_videos()