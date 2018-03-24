#!/usr/bin/env python
import os
import requests
import secrets
import urllib.request

ACCESS_TOKEN = secrets.ACCESS_TOKEN # replace this with your facebook access token 
photo_type = 'tagged'
r_url = 'https://graph.facebook.com/v2.12/me/photos?type=' + photo_type + '&access_token=' + ACCESS_TOKEN
r = requests.get(r_url)
photo_data = r.json()['data']
photo_ids = []


directory = 'facebook_pictures'
if not os.path.exists(directory):
    os.makedirs(directory)

print('locating tagged photos on facebook...')
while r_url:
	for d in photo_data:
		photo_ids.append(d['id'])
	if 'paging' in r.json() and 'next' in r.json()['paging']:
		r_url = r.json()['paging']['next']
		r = requests.get(r_url)
		photo_data = r.json()['data']
	else:
		if photo_type == 'tagged':
			print('locating uploaded pictures on facebook...')
			photo_type = 'uploaded'
			r_url = 'https://graph.facebook.com/v2.12/me/photos?type=' + photo_type + '&access_token=' + ACCESS_TOKEN
			r = requests.get(r_url)
			photo_data = r.json()['data']
		else:
			r_url = ""

print('downloading photos...')
for photo_id in photo_ids:
	photo_url = "https://graph.facebook.com/" + str(photo_id) + "/picture?access_token=" + ACCESS_TOKEN + "&type=normal"
	photo_name = photo_id + '.jpg'
	urllib.request.urlretrieve(photo_url, os.path.join(directory, photo_name))

print('successfully downloaded ' + str(len(photo_ids)) + ' photos')

