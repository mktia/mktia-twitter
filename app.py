# -*- coding: utf-8 -*-

import os
import tweepy
from flask import Flask, render_template, session, request

app = Flask(__name__)

app.secret_key = os.environ['secret_key']
url = 'http://mktia-twitter.herokuapp.com'

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
	return render_template('auth.html', url=url, redirect_url=redirect_url)

@app.route('/menu')
def select():
	try:
		session['verifier'] = request.args.get('oauth_verifier')
	except Exception as e:
		print(e)
		print('Error! Failed to set sesstion.(verifier)')
	return render_template('menu.html', url=url)

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
	
	owner = api.me()
	owner_id = owner.id
	owner_screen_name = owner.screen_name
	try:
		api.destroy_list(owner_id=owner_id, slug='kataomoi')
	except Exception as e:
		print(e)
	api.create_list(name='kataomoi', mode='private', description="あなたが片思いしているユーザー一覧です")
	
	not_friends = []
	num = 0
	cnt = 0
	
	for i in range(fr):
		for j in range(fo):
			if friends[i] == followers[j]:
				break
		else:
			not_friends.append(friends[i])
			num += 1
	for user in not_friends:
		if cnt < 150:
			try:
				api.add_list_member(user_id=user, owner_id=owner_id, slug='kataomoi')
				cnt += 1
			except Exception as e:
				print(e)
		else:
			break
	return render_template('finish.html', url=url, user=owner_screen_name, num=num, type=1)

@app.route('/notfollow')
def notfollow():
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
	
	owner = api.me()
	owner_id = owner.id
	owner_screen_name = owner.screen_name
	try:
		api.destroy_list(owner_id=owner_id, slug='notfollow')
	except Exception as e:
		print(e)
	api.create_list(name='notfollow', mode='private', description=u"あなたに片思いしているユーザー一覧です")
	
	not_follow = []
	num = 0
	cnt = 0
	
	for fo in followers:
		for fr in friends:
			if fo == fr:
				break
		else:
			not_follow.append(fo)
			num += 1
	for user in not_follow:
		if cnt < 150:
			try:
				api.add_list_member(user_id=user, owner_id=owner_id, slug='notfollow')
				cnt += 1
			except Exception as e:
				print(e)
		else:
			break
	return render_template('finish.html', url=url, user=owner_screen_name, num=num, type=2)
	
@app.route('/blankname')
def blank_name():
	token = session.get('request_token')
	verifier = session.get('verifier')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
	auth.request_token = token
	auth.get_access_token(verifier)
	access_token = auth.access_token
	access_token_secret = auth.access_token_secret
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	api.update_profile(name=u'ㅤ')
	return render_template('finish.html', url=url, user='', num='', type=4)
	
"""
@app.route('/teiki')
def teikicheck():
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

	owner_id = api.me().id
	api.create_list(name='teiki', mode='private', description="This list members tweet a lot of 'teiki' tweets.")
	
	teiki = []
	count = 0
	for fr in friends:
		user = api.get_user(fr).screen_name
		print user
		tl = api.user_timeline(fr)
		#count += 1
		#if count > 5:
		#	break
		for j in range(5):
			text1 = tl[j].text
			num1 = text1.find(u'定期')
			if num1 == -1:
				for k in range(1, 5):
					text2 = tl[j + k].text
					num2 = text2.find(u'定期')
					if num2 >= 0:
						break
				else:
					teiki.append(fr)
			else:
				break
	n = 0
	for user in teiki:
		if cnt < 150:
			try:
				api.add_list_member(user_id=user, owner_id=owner_id, slug='teiki')
				n += 1
			except Exception as e:
				print(e)
		else:
			break
			
	return render_template('finish.html', type=3)
"""
"""
@app.route('/teiki-mute')
def mute_teiki():
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
	
	mute = []
	cnt = 0
	
	tl = api.home_timeline()
	for line in tl:
		text = line.text
		user = line.user.id
		print user
		if text.find(u'定期') >= 0:
			#mute
	return render_template('finish.html', url=url, type=4)
"""
	
@app.route('/ver')
def show_ver():
	return render_template('ver.html', url=url)

if __name__ == "__main__":
	app.run()