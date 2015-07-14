import pytumblr, os, glob, sys, urllib, urllib2

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  '***',
  '***',
  '***',
  '***'
)

# Make the request
client.info()




def post_to_tumblr(img, authors, blog="skdbanners"):
    client.create_photo(blog, state="published", tags=["sketchdaily"], caption=authors, data=img)	
