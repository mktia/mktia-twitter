# -*- coding: utf-8 -*-

import os
import tweepy
from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
callback_url = 'http://mktia-twitter.herokuapp.com/menu'

@app.route('/')
def auth():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
		print('Error! Failed to get request token.')
	try:
		session['request_token'] = auth.request_token
	except Exception as e:
		print(e)
		print('Error! Failed to set session.')
	return render_template('auth.html', redirect_url=redirect_url)

@app.route('/menu')
def select():
	try:
		session['verifier'] = request.args.get('oauth_verifier')
	except Exception as e:
		print(e)
		print('Error! Failed to set sesstion.(verifier)')
	return render_template('menu.html')

@app.route('/ffcheck')
def ffcheck():
	token = session.get('request_token')
	verifier = session.get('verifier')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
	auth.request_token = token
	auth.get_access_token(verifier)
	access_token = auth.access_token
	access_token_secret = auth.access_token_secret
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	friends = []
	for friend in tweepy.Cursor(api.friends_ids).items():
		friends.append(friend)
	followers = []
	for follower in tweepy.Cursor(api.followers_ids).items():
		followers.append(follower)
	fr = len(friends)
	fo = len(followers)
	
	owner_id = api.me().id
	api.create_list(name='kataomoi', mode='private', description='Initialized.')
	
	not_friends = []
	cnt = 0
	
	for i in range(fr):
		for j in range(fo):
			if friends[i] == followers[j]:
				break
		else:
			not_friends.append(friends[i])
	for user in not_friends:
		if cnt < 180:
			try:
				api.add_list_member(user_id=user, owner_id=owner_id, slug='kataomoi')
				cnt += 1
			except Exception as e:
				print(e)
		else:
			break
	
	return render_template('finish.html', type=1)

if __name__ == "__main__":
	app.run()
