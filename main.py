__author__ = 'David'
import re, praw, requests, os, glob, sys, urllib, urllib2, cStringIO, time, pickle
import BeautifulSoup
from random import shuffle
from PIL import Image


#my image thing
from imageparse import extract_link
from tumblrstuff import post_to_tumblr

r = praw.Reddit(user_agent='Image Collector 1.0 by u/davidwinters', site_name="sketchdaily bot")
r.config.decode_html_entities = True #this fixes some sillyness with encoding when we get and set the CSS


## grab saved token
f = open(os.path.dirname(os.path.abspath(__file__))+'/store.pckl')
info = pickle.load(f)
f.close()

try:
    ## retreive new token
    info = r.refresh_access_information(info['refresh_token'])
    info = r.refresh_access_information()

except Exception as e:
    exc = e._raw
    print("Some thing bad happened! HTTPError", exc.status_code)

## save token
f = open(os.path.dirname(os.path.abspath(__file__))+'/store.pckl', 'w')
pickle.dump(info, f)
f.close()

try:
    r.set_access_credentials('identity modconfig read', info['access_token'], info['refresh_token'])
except Exception as e:
    exc = e._raw
    print("ugh", exc.status_code)

#r.set_access_credentials(info['scope'], info['access_token'], info['refresh_token'])





subreddit = r.get_subreddit('sketchdaily')

posts = [ ]
keywords = ['imgur', 'jpg', 'gif', 'png']
links = [ ]
authors = ''
## CREATE IMAGE HERE
banner_image = Image.new('RGB', (1920, 166))
last_image_edge = 0

#lets put the top two in a list, we'll only need the 2nd one in the list which is yesterday
for post in subreddit.get_new(limit=2):
        posts.append(post.id)

# posts[1] stores yesterday's post id

submission = r.get_submission(submission_id=posts[1])

# if its a sticky post we don't want it
if submission.stickied == True:
	submission = r.get_submission(submission_id=posts[2])

flat_comments = praw.helpers.flatten_tree(submission.comments)

shuffle(flat_comments)
for comment in flat_comments:
    
    if not hasattr(comment, 'body'):
        continue
    
    if comment.is_root == False:
        continue
    
    #link = re.search('(http://i.imgur[^ ]+g)', comment.body)
    link_list = extract_link(comment.body) #should return a list
    NSFW = re.search('nsfw', comment.body.lower())


    if last_image_edge >= 1920 :
        continue
    
    if NSFW != None:
	continue

    if not link_list:
        continue

    #for link in link_list:
    link = link_list[0]
    links.append(link)
    print link
    file_in_memory = cStringIO.StringIO(urllib.urlopen(link).read())
    temp_img = Image.open(file_in_memory)
    temp_img.thumbnail((900,166))
    
    #adding author to list 
    authors += "<a href='"+link+"'>"+str(comment.author)+"</a>, "
    banner_image.paste(temp_img,(last_image_edge, 0))
    width, height = temp_img.size
    last_image_edge += width

    del temp_img


banner_image.save("headerimg.jpg")
print "pausing a sec"

image_path = os.path.dirname(os.path.abspath(__file__))+'/headerimg.jpg' 

time.sleep(5.5)

r.upload_image('sketchdaily', image_path)
post_to_tumblr(image_path, authors)

## refresh stylesheet to show new banner
ss = r.get_stylesheet('sketchdaily')['stylesheet']

r.set_stylesheet('sketchdaily',ss)


#print links
print authors
