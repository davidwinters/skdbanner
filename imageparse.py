#lets do stuff to images!
__author__ = 'David'
import re

def is_image( str ):
    if (str.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and str.lower().startswith('http')):
	return True
    else:
        return False

def imgur_fix( str ):
    
    if "imgur" in str.lower() and "/a/" not in str.lower() and "gallery" not in str.lower():
	return True
    else:
        return False

   

    return str
def extract_link( str ):
    url_regex = "http[s]?://[^)|\s|,]+"
    links = []

    for match in re.findall(url_regex, str):
	if is_image(match):
            links.append(match)
        elif imgur_fix(match):
            links.append(match+".png")
    return links



