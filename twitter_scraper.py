## To run this program under command line: python Twitter_Pull_Timer.py "['Symantec, Norton']"

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import sys, ast
import os
ckey = '--------------'
csecret = '----------------'
atoken = '--------------'
asecret = '---------------'
currentHour = str(time.strftime("%H"))

class listener(StreamListener):

	def on_data(self, data):
		try:
			##print data
			global currentHour
			
			## Tweet Created Date/Time
			tweetCreatedate = data.split('{"created_at":"')[1].split('","id')[0]
			print tweetCreatedate
			## Tweet Text
			tweet = data.split(',"text":"')[1].split('","source')[0]
			print tweet
			## Tweeter User Name/ID
			tweetUsername = data.split(',"name":"')[1].split('","screen_name')[0]
			print tweetUsername
			tweetUserID = data.split('"user":{"id":')[1].split(',"id_str')[0]
			print tweetUserID
			## User Location
			location = data.split(',"location":"')[1].split('","url')[0]
			if len(location.strip())==0: location='N/A'
			print location
			## Followers Count
			followers_count = data.split(',"followers_count":')[1].split(',"friends_count')[0]
			if len(followers_count.strip())==0: followers_count='0'
			print followers_count
			# Friends Count
			friends_count = data.split(',"friends_count":')[1].split(',"listed_count')[0]
			if len(friends_count.strip())==0: friends_count='0'
			print friends_count
			# Retweet Count (if count>0 then retweet_status is true)
			retweet_count = data.split(',"retweet_count":')[1].split(',"favorite_count')[0]
			if len(retweet_count.strip())==0: retweet_count='0'
			print retweet_count
			# Twitter user ID this Tweet replies to
			replyUserID = data.split(',"in_reply_to_user_id":')[1].split(',"in_reply_to_user_id_str')[0]
			print replyUserID
			
			## %x: date; %X: time; %Y: year; %m: month; %U: week of the year; %w: weekday; %j: day of the year; %H: hour
			saveThis = str(time.strftime("%x"))+'\t'+str(time.strftime("%X"))+'\t'+str(time.strftime("%Y"))+'\t'+str(time.strftime("%m"))+'\t'+ \
					   str(time.strftime("%U"))+'\t'+str(time.strftime("%w"))+'\t'+str(time.strftime("%j"))+'\t'+str(time.strftime("%H"))+'\t'+ \
			           tweetUsername+'\t'+tweetUserID+'\t'+location+'\t'+followers_count+'\t'+friends_count+'\t'+retweet_count+'\t'+replyUserID+'\t'+tweet
			if currentHour != str(time.strftime("%H")): 
				currentHour = str(time.strftime("%H"))
				os.system("mv twitDB_*.csv /home/hdpuser/python/wip/")
			filename = "twitDB_"+str(time.strftime("%m_%d_%Y"))+"_Hr"+currentHour+".csv"
			saveFile = open(filename,'a')
			saveFile.write(saveThis)
			saveFile.write('\n')
			saveFile.close()
			return True
		except BaseException, e:
			print 'Failed: ',str(e)
			time.sleep(5)
			            
	def on_error(self, status):
		print status
            
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken,asecret)
twitterStream = Stream(auth, listener())
searchwords = ast.literal_eval(sys.argv[1])
print searchwords
twitterStream.filter(track=searchwords)
