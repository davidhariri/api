import os
import twitter

CHAR_LIMIT = 246
URL_STR = "life.dhariri.com/posts/{}"

twitter_api = twitter.Api(consumer_key=os.getenv("TWITTER_KEY"),
	consumer_secret=os.getenv("TWITTER_SECRET"),
	access_token_key=os.getenv("TWITTER_ACCESS_KEY"),
	access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"))

def post_post_as_tweet(post):
	"""
	Takes a post and formats it as a tweet, then sends the tweet to Twitter

	TODO:
	2. Log id to database against Post object

	"""
	status = ""
	post_url = URL_STR.format(post.slug)

	if post.comment:
		if len(post.comment) <= CHAR_LIMIT:
			status = post.comment
		else:
			status = post.comment[:CHAR_LIMIT] + "…"
		
		status += "\n\n"
		status += post_url
	
	else:
		status = post_url

	if post.media:
		try:
			# Will fail if too big
			return twitter_api.PostUpdate(status, media=post.media[:4])
		except:
			return twitter_api.PostUpdate(status)

	return twitter_api.PostUpdate(status)
