import os
import twitter
from sentry_sdk import capture_exception

CHAR_LIMIT = 246
URL_STR = "little.site/posts/{}"

twitter_api = twitter.Api(consumer_key=os.getenv("TWITTER_KEY"),
	consumer_secret=os.getenv("TWITTER_SECRET"),
	access_token_key=os.getenv("TWITTER_ACCESS_KEY"),
	access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"))

def process_media(media):
	optimized_urls = []

	for url in media:
		file_type = url.split(".")[-1]

		if file_type in ["gif"]:
			optimized_urls.append(url.replace(".gif", ".thumb.mp4"))

		elif file_type in ["jpg", "jpeg", "png"]:
			optimized_urls.append(url.replace(".{}".format(file_type), ".thumb.jpeg"))
	
	return optimized_urls

def post_post_as_tweet(post):
	"""
	Takes a post and formats it as a tweet, then sends the tweet to Twitter
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
			return twitter_api.PostUpdate(status, media=process_media(post.media)[:4])
		except Exception as e:
			capture_exception(e)
			
			return twitter_api.PostUpdate(status)

	return twitter_api.PostUpdate(status)
